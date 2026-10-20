import html as html_lib
import re

from otree.api import Bot, Submission, SubmissionMustFail, expect

import research_consent
from research_consent.tests import BOT_CASES

from . import (
    C,
    LIKERT_PAGES,
    Completed,
    Demographics,
    PhoneNumber,
    RewardContact,
    custom_export_analysis,
    custom_export_reward_list,
    items,
    page_sequence,
)

# 척도별 문항 수와 페이지 구성: 척도 하나를 한 페이지에 모두 표시
EXPECTED_SCALES = {
    'ase': [6],
    'arb': [15],
    'esd': [10],
    'aat': [23],
    'caid': [14],
    'anth': [20],
    'emp': [4],
}

# 케이스별 (입력값, 저장될 값)
PHONE_INPUT = {
    'complete_with_phone': ('010 1234 5678', '010-1234-5678'),
    'complete_without_phone': ('', None),
    'reconsider_after_decline': ('01098765432', '010-9876-5432'),
}

INVALID_PHONES = ['010-123-45', '02-123-4567', '0101234567', 'abcdefghijk', '010-1234-56789']


def answer_for(field):
    # 문항마다 1~5 값을 고르게 섞어 응답합니다.
    return [item.field for item in items.ALL_ITEMS].index(field) % 5 + 1


def radio_inputs(html):
    """[(name, value, checked)]"""
    found = []
    for tag in re.findall(r'<input[^>]*type="radio"[^>]*>', html):
        name = re.search(r'name="([^"]+)"', tag).group(1)
        value = re.search(r'value="([^"]+)"', tag).group(1)
        found.append((name, value, bool(re.search(r'\schecked', tag))))
    return found


def normalize_space(text):
    return re.sub(r'\s+', ' ', text)


class PlayerBot(Bot):
    cases = list(BOT_CASES)

    def play_round(self):
        if BOT_CASES[self.case] != ('yes', 'yes'):
            self.check_survey_locked_without_consent()
            return

        self.check_item_config()

        # 성별·연령: 필수, 정수, 범위 검증
        expect(f'{items.DEMOGRAPHICS_PAGE_NUMBER} / {items.TOTAL_PAGES}', 'in', self.html)
        yield SubmissionMustFail(Demographics, {}, error_fields=['gender', 'age'])
        yield SubmissionMustFail(Demographics, dict(gender=2, age='25.5'), error_fields=['age'])
        yield SubmissionMustFail(Demographics, dict(gender=2, age=C.AGE_MAX + 1), error_fields=['age'])
        # 만 18세 미만은 진행 불가
        expect(C.AGE_MIN, 18)
        yield SubmissionMustFail(Demographics, dict(gender=2, age=17), error_fields=['age'])
        yield SubmissionMustFail(Demographics, dict(gender=9, age=30), error_fields=['gender'])
        yield Demographics, dict(gender=2, age=30)

        shown_fields = []
        answers = {}
        for index, PageClass in enumerate(LIKERT_PAGES):
            fields = PageClass.form_fields
            page_answers = {name: answer_for(name) for name in fields}
            self.check_likert_page(PageClass, fields)

            # 한 문항이라도 비면 진행 불가, 1~5 밖의 값도 불가
            yield SubmissionMustFail(
                PageClass, {k: v for k, v in page_answers.items() if k != fields[-1]}, error_fields=[fields[-1]]
            )
            yield SubmissionMustFail(PageClass, {**page_answers, fields[0]: 6}, error_fields=[fields[0]])
            yield SubmissionMustFail(PageClass, {**page_answers, fields[0]: 0}, error_fields=[fields[0]])
            yield PageClass, page_answers
            shown_fields += fields
            answers.update(page_answers)

            if index == 1:
                # '이전'으로 돌아가면 저장된 응답이 선택된 상태로 표시되어야 함
                yield Submission(LIKERT_PAGES[2], {'back_button': '{}'}, check_html=False)
                expect(f'/{PageClass.__name__}/', 'in', self.participant_bot.path)
                self.expect_checked(page_answers)
                yield PageClass, page_answers

        expect(shown_fields, [item.field for item in items.ALL_ITEMS])
        expect(len(shown_fields), 92)

        # 전화번호 페이지에서도 '이전' 이동과 응답 유지 확인
        expect(f'{items.TOTAL_PAGES} / {items.TOTAL_PAGES}', 'in', self.html)
        yield Submission(PhoneNumber, {'back_button': '{}'}, check_html=False)
        last_page_answers = {name: answers[name] for name in LIKERT_PAGES[-1].form_fields}
        self.expect_checked(last_page_answers)
        yield LIKERT_PAGES[-1], last_page_answers

        for invalid in INVALID_PHONES:
            yield SubmissionMustFail(PhoneNumber, dict(phone_number=invalid), error_fields=['phone_number'])
        expect(self.player.survey_completed, False)

        phone_path = self.participant_bot.path
        raw_phone, stored_phone = PHONE_INPUT[self.case]
        yield PhoneNumber, dict(phone_number=raw_phone)

        # 같은 화면 구성으로 완료 메시지 표시
        expect(f'/{Completed.__name__}/', 'in', self.participant_bot.path)
        expect('설문 제출이 완료되었습니다', 'in', self.html)
        expect(self.player.survey_completed, True)
        expect(self.player.field_maybe_none('phone_number'), None)

        contacts = RewardContact.filter(subsession=self.subsession)
        expect([c.phone_number for c in contacts], [stored_phone] if stored_phone else [])

        self.check_no_resubmission(phone_path, answers)
        self.check_exports(answers, stored_phone)

    def check_item_config(self):
        expect(len(items.ALL_ITEMS), 92)
        actual = {}
        for spec in items.LIKERT_PAGES:
            actual.setdefault(spec.fields[0].rsplit('_', 1)[0], []).append(len(spec.fields))
        expect(actual, EXPECTED_SCALES)
        expect(items.TOTAL_PAGES, 11)
        expect([choice[0] for choice in items.LIKERT_CHOICES], [1, 2, 3, 4, 5])

    def check_likert_page(self, PageClass, fields):
        html = self.html
        expect(f'/{PageClass.__name__}/', 'in', self.participant_bot.path)
        # 한 페이지에는 한 척도의 문항만 있어야 함
        expect(len({name.rsplit('_', 1)[0] for name in fields}), 1)
        radios = radio_inputs(html)
        expect(sorted({name for name, _, _ in radios}), sorted(fields))
        for name in fields:
            expect([value for n, value, _ in radios if n == name], ['1', '2', '3', '4', '5'])
        # 처음 방문 시 선택된 값이 없어야 함
        expect([r for r in radios if r[2]], [])
        for _, label in items.LIKERT_CHOICES:
            expect(label, 'in', html)
        # 문항 텍스트가 생략 없이 표시되어야 함
        for item in items.ALL_ITEMS:
            if item.field in fields:
                expect(normalize_space(html_lib.escape(item.text)), 'in', html)

    def expect_checked(self, page_answers):
        checked = {name: value for name, value, is_checked in radio_inputs(self.html) if is_checked}
        expect(checked, {name: str(value) for name, value in page_answers.items()})

    def check_survey_locked_without_consent(self):
        """동의하지 않은 참여자는 설문 URL에 직접 접근하거나 응답을 보낼 수 없어야 함."""
        for PageClass in page_sequence:
            expect(PageClass.is_displayed(self.player), False)

        client = self.participant_bot.client
        current_url = self.participant._url_i_should_be_on()
        expect('/ConsentDeclined/', 'in', current_url)
        first_index = len(research_consent.page_sequence) + 1
        for offset, PageClass in enumerate([Demographics, LIKERT_PAGES[0]]):
            url = f'/p/{self.participant.code}/{C.NAME_IN_URL}/{PageClass.__name__}/{first_index + offset}'
            response = client.get(url, allow_redirects=False)
            expect(response.status_code, 302)
            expect(response.headers['location'], current_url)
            response = client.post(url, data=dict(gender='1', age='30', ase_01='3'), allow_redirects=False)
            expect(response.status_code, 302)

        expect(self.player.field_maybe_none('gender'), None)
        expect(self.player.field_maybe_none('age'), None)
        expect(self.player.field_maybe_none('ase_01'), None)

    def check_no_resubmission(self, phone_path, answers):
        """제출 후에는 같은 제출을 반복하거나 이전 응답을 고칠 수 없어야 함."""
        client = self.participant_bot.client
        before = len(RewardContact.filter(subsession=self.subsession))
        response = client.post(phone_path, data=dict(phone_number='010-1111-2222'), allow_redirects=False)
        expect(response.status_code, 302)
        expect(len(RewardContact.filter(subsession=self.subsession)), before)

        first_likert_index = len(research_consent.page_sequence) + 2
        first_page_path = (
            f'/p/{self.participant.code}/{C.NAME_IN_URL}/{LIKERT_PAGES[0].__name__}/{first_likert_index}'
        )
        response = client.post(first_page_path, data=dict(ase_01='5', ase_02='5', ase_03='5'), allow_redirects=False)
        expect(response.status_code, 302)
        expect(self.player.ase_01, answers['ase_01'])

    def check_exports(self, answers, stored_phone):
        rows = list(custom_export_analysis([self.player]))
        header, values = rows[0], rows[1]
        expect(len(rows), 2)
        expect('phone_number', 'not in', header)
        row = dict(zip(header, values))
        for name in ['participant_code', 'gender', 'age', 'research_consent', 'privacy_consent',
                     'consent_timestamp', 'consent_version', 'survey_completed', 'completion_timestamp']:
            expect(name, 'in', header)
        expect(row['participant_code'], self.participant.code)
        expect(row['research_consent'], 'yes')
        expect(row['privacy_consent'], 'yes')
        expect(row['gender'], 2)
        expect(row['age'], 30)
        expect({name: row[name] for name in answers}, answers)
        expect(row['survey_completed'], 1)
        expect(row['participation_status'], 'completed')
        if stored_phone:
            expect(stored_phone, 'not in', [str(v) for v in values])

        reward_rows = list(custom_export_reward_list([self.player]))
        expect(reward_rows[0], ['no', 'phone_number', 'submitted_date', 'same_number_count'])
        expect([r[1] for r in reward_rows[1:]], [stored_phone] if stored_phone else [])
        expect(self.participant.code, 'not in', [str(v) for r in reward_rows for v in r])
