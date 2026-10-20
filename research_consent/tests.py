import re

from otree.api import Bot, Submission, SubmissionMustFail, expect

from . import C, Consent, ConsentDeclined, Introduction

# 두 앱(research_consent, ai_survey)의 봇이 같은 케이스 목록을 씁니다.
# 값: (research_consent, privacy_consent) 최종 선택
BOT_CASES = {
    'complete_with_phone': ('yes', 'yes'),
    'complete_without_phone': ('yes', 'yes'),
    'research_consent_only': ('yes', 'no'),
    'privacy_consent_only': ('no', 'yes'),
    'both_declined': ('no', 'no'),
    # 거부 후 '동의서로 돌아가기'로 돌아가 두 항목 모두 동의하는 경우
    'reconsider_after_decline': ('yes', 'yes'),
}


def checked_radios(html):
    return re.findall(r'<input[^>]*type="radio"[^>]*\schecked', html)


class PlayerBot(Bot):
    cases = list(BOT_CASES)

    def play_round(self):
        # 첫 화면: 연구 소개
        expect('/Introduction/', 'in', self.participant_bot.path)
        expect(C.STUDY_TITLE, 'in', self.html)
        expect('다음: 동의서 확인', 'in', self.html)
        expect('IRB사무국', 'in', self.html)
        yield Introduction

        # 두 번째 화면: 두 동의서 모두 표시, 미리 선택된 항목 없음
        expect('연구참여 동의서', 'in', self.html)
        expect('연구참여자 개인정보 수집·이용 동의서', 'in', self.html)
        expect(checked_radios(self.html), [])

        # 미선택 → 진행 불가
        yield SubmissionMustFail(Consent, {}, error_fields=['research_consent', 'privacy_consent'])
        yield SubmissionMustFail(Consent, dict(research_consent='yes'), error_fields=['privacy_consent'])
        yield SubmissionMustFail(Consent, dict(privacy_consent='yes'), error_fields=['research_consent'])
        # 정의되지 않은 값 → 진행 불가
        yield SubmissionMustFail(
            Consent, dict(research_consent='maybe', privacy_consent='yes'), error_fields=['research_consent']
        )

        research, privacy = BOT_CASES[self.case]
        if self.case == 'reconsider_after_decline':
            research = 'no'
        yield Consent, dict(research_consent=research, privacy_consent=privacy)

        expect(self.player.research_consent, research)
        expect(self.player.privacy_consent, privacy)
        expect(self.player.consent_version, C.CONSENT_VERSION)
        expect(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+09:00', self.player.consent_timestamp) is not None, True)

        if research == 'yes' and privacy == 'yes':
            expect(self.participant.vars['consent_ok'], True)
            return

        # 한 항목이라도 동의하지 않음 → 안내 화면에서 더 진행 불가
        expect(self.participant.vars['consent_ok'], False)
        expect('/ConsentDeclined/', 'in', self.participant_bot.path)
        expect(C.DECLINE_MESSAGE, 'in', self.html)
        yield SubmissionMustFail(ConsentDeclined, check_html=False)

        if self.case == 'reconsider_after_decline':
            yield Submission(ConsentDeclined, {'back_button': '{}'}, check_html=False)
            # 이전 선택이 그대로 표시된 동의서로 돌아옴
            expect(len(checked_radios(self.html)), 2)
            yield Consent, dict(research_consent='yes', privacy_consent='yes')
            expect(self.participant.vars['consent_ok'], True)
