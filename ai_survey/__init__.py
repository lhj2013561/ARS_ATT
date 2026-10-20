import re
from collections import Counter
from datetime import datetime, timedelta, timezone

from otree.api import *

from . import items

doc = """
본 설문: 성별·연령, 7개 심리척도 92문항(5점 리커트), 답례품용 휴대전화번호(선택).
문항 텍스트와 페이지 구성은 items.py에서 관리합니다.
"""

KST = timezone(timedelta(hours=9), name='KST')

# 휴대전화번호: 010-XXXX-XXXX 또는 (구)011/016/017/018/019-XXX(X)-XXXX
PHONE_RE = re.compile(r'^(01[016789])(\d{3,4})(\d{4})$')


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # 연령 입력 허용 범위(만 나이). 만 18세 미만은 참여할 수 없습니다.
    AGE_MIN = 18
    AGE_MAX = 120
    GENDER_CHOICES = [[1, '남성'], [2, '여성'], [3, '기타'], [4, '응답하고 싶지 않음']]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def likert_field(item):
    return models.IntegerField(
        label=item.text,
        # 척도 안의 문항 번호. LikertPage.html에서 문항 번호로 표시합니다.
        help_text=str(item.number),
        choices=items.LIKERT_CHOICES,
        widget=widgets.RadioSelect,
    )


class Player(BasePlayer):
    gender = models.IntegerField(
        label='성별', choices=C.GENDER_CHOICES, widget=widgets.RadioSelect
    )
    age = models.IntegerField(label='연령 (만 나이)', min=C.AGE_MIN, max=C.AGE_MAX)

    # 심리척도 문항(ase_01 ~ emp_04)은 items.py에서 자동으로 만듭니다.
    vars().update({item.field: likert_field(item) for item in items.ALL_ITEMS})

    # 입력을 받기 위한 칸입니다. 제출 시 RewardContact로 옮기고 비우므로 응답 데이터에는 남지 않습니다.
    phone_number = models.StringField(blank=True, label='휴대전화번호 (선택)')
    survey_completed = models.BooleanField(initial=False)
    completion_timestamp = models.StringField(blank=True)


class RewardContact(ExtraModel):
    """답례품 지급용 연락처. 응답자(Player)와 연결하지 않고 세션 단위로만 저장합니다."""

    subsession = models.Link(Subsession)
    phone_number = models.StringField()
    # 시각까지 저장하면 completion_timestamp로 응답과 짝지을 수 있으므로 날짜만 저장합니다.
    submitted_date = models.StringField()


# FUNCTIONS


def now_kst():
    return datetime.now(KST).isoformat(timespec='seconds')


def normalize_phone(raw):
    """하이픈·공백·점을 지우고 형식을 검사해 '010-1234-5678' 꼴로 돌려줍니다. 형식이 틀리면 None."""
    digits = re.sub(r'[\s.\-]', '', raw or '')
    match = PHONE_RE.match(digits)
    if not match or (match.group(1) == '010' and len(match.group(2)) != 4):
        return None
    return '-'.join(match.groups())


def phone_number_error_message(player, value):
    if value and value.strip() and normalize_phone(value) is None:
        # 입력값을 메시지에 다시 넣지 않습니다.
        return '휴대전화번호 형식이 올바르지 않습니다. 예: 010-1234-5678'


def consent_given(player):
    # research_consent 앱의 Consent 페이지에서 두 동의를 모두 '동의함'으로 제출한 경우에만 True
    return player.participant.vars.get('consent_ok') is True


def missing_required_fields(player):
    required = ['gender', 'age'] + [item.field for item in items.ALL_ITEMS]
    return [name for name in required if player.field_maybe_none(name) is None]


def progress(page_number):
    total = items.TOTAL_PAGES
    return dict(current=page_number, total=total, percent=round(page_number / total * 100))


# PAGES


class SurveyPage(Page):
    """본 설문 페이지 공통 설정. 두 동의를 모두 한 참여자에게만 표시합니다(서버 측 검증)."""

    form_model = 'player'
    use_blank_layout = True

    @staticmethod
    def is_displayed(player):
        return consent_given(player) and not player.survey_completed


class Demographics(SurveyPage):
    form_fields = ['gender', 'age']
    preserve_unsubmitted_inputs = True

    @staticmethod
    def vars_for_template(player):
        return dict(progress=progress(items.DEMOGRAPHICS_PAGE_NUMBER))


class LikertPage(SurveyPage):
    """모든 척도 페이지가 함께 쓰는 리커트 페이지. 실제 페이지는 make_likert_page()가 만듭니다."""

    template_name = 'ai_survey/LikertPage.html'
    allow_back_button = True
    # '이전'으로 돌아갔다 와도 아직 제출하지 않은 이 페이지의 선택이 유지되도록 합니다.
    preserve_unsubmitted_inputs = True


def make_likert_page(spec):
    def vars_for_template(player):
        return dict(
            spec=spec,
            scale_count=len(items.SCALES),
            show_scale_name=items.SHOW_SCALE_NAMES,
            progress=progress(spec.page_number),
        )

    return type(
        spec.name,
        (LikertPage,),
        dict(
            __module__=__name__,
            form_fields=list(spec.fields),
            vars_for_template=staticmethod(vars_for_template),
        ),
    )


LIKERT_PAGES = [make_likert_page(spec) for spec in items.LIKERT_PAGES]


class PhoneNumber(SurveyPage):
    form_fields = ['phone_number']
    allow_back_button = True

    @staticmethod
    def vars_for_template(player):
        return dict(progress=progress(items.TOTAL_PAGES), completed=False)

    @staticmethod
    def error_message(player, values):
        missing = missing_required_fields(player)
        if missing:
            return (
                f'저장되지 않은 응답이 {len(missing)}개 있습니다. '
                "'이전' 버튼으로 돌아가 응답을 확인해 주세요."
            )

    @staticmethod
    def before_next_page(player, timeout_happened):
        raw = player.field_maybe_none('phone_number') or ''
        player.phone_number = None
        if raw.strip():
            RewardContact.create(
                subsession=player.subsession,
                phone_number=normalize_phone(raw),
                submitted_date=datetime.now(KST).date().isoformat(),
            )
        player.survey_completed = True
        player.completion_timestamp = now_kst()


class Completed(Page):
    """제출 완료 상태. 전화번호 페이지와 같은 템플릿을 써서 같은 화면에 완료 메시지를 보여 줍니다."""

    template_name = 'ai_survey/PhoneNumber.html'
    use_blank_layout = True

    @staticmethod
    def is_displayed(player):
        return consent_given(player) and player.survey_completed

    @staticmethod
    def vars_for_template(player):
        return dict(progress=progress(items.TOTAL_PAGES), completed=True)

    @staticmethod
    def error_message(player, values):
        # 마지막 화면입니다. 제출 이후에는 어떤 요청으로도 진행하거나 응답을 바꿀 수 없습니다.
        return '설문이 이미 제출되었습니다.'


page_sequence = [Demographics, *LIKERT_PAGES, PhoneNumber, Completed]


# DATA EXPORT (관리자 화면 Data 탭의 custom export)

ANALYSIS_COLUMNS = (
    [
        'participant_code',
        'session_code',
        'research_consent',
        'privacy_consent',
        'consent_timestamp',
        'consent_version',
        'gender',
        'age',
    ]
    + [item.field for item in items.ALL_ITEMS]
    + ['survey_completed', 'completion_timestamp', 'participation_status', 'last_page']
)


def participation_status(research_consent, privacy_consent, completed):
    if completed:
        return 'completed'
    if research_consent is None or privacy_consent is None:
        return 'consent_pending'
    if research_consent == 'yes' and privacy_consent == 'yes':
        return 'in_progress'
    return 'declined'


def custom_export_analysis(players):
    """분석용 CSV: 링크에 접속한 참여자 1명당 1행. 휴대전화번호는 넣지 않습니다."""
    # 동의 응답은 research_consent 앱에 저장되어 있습니다.
    from research_consent import Player as ConsentPlayer

    yield ANALYSIS_COLUMNS
    for player in players:
        participant = player.participant
        if not participant.visited:
            continue
        consent = ConsentPlayer.objects_get(participant=participant)
        research = consent.field_maybe_none('research_consent')
        privacy = consent.field_maybe_none('privacy_consent')
        completed = bool(player.survey_completed)
        yield (
            [
                participant.code,
                player.session.code,
                research,
                privacy,
                consent.field_maybe_none('consent_timestamp'),
                consent.field_maybe_none('consent_version'),
                player.field_maybe_none('gender'),
                player.field_maybe_none('age'),
            ]
            + [player.field_maybe_none(item.field) for item in items.ALL_ITEMS]
            + [
                int(completed),
                player.field_maybe_none('completion_timestamp'),
                participation_status(research, privacy, completed),
                participant._current_page_name,
            ]
        )


def custom_export_reward_list(players):
    """답례품 지급 명단: 휴대전화번호만 담고 응답 자료와는 연결하지 않습니다."""
    subsession_ids = {player.subsession_id for player in players}
    contacts = [c for c in RewardContact.filter() if c.subsession_id in subsession_ids]
    counts = Counter(c.phone_number for c in contacts)
    yield ['no', 'phone_number', 'submitted_date', 'same_number_count']
    # 제출 순서로 응답과 짝지을 수 없도록 번호순으로 정렬합니다.
    contacts.sort(key=lambda c: (c.phone_number, c.submitted_date))
    for no, contact in enumerate(contacts, start=1):
        yield [no, contact.phone_number, contact.submitted_date, counts[contact.phone_number]]
