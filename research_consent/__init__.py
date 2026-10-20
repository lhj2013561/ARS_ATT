from datetime import datetime, timedelta, timezone

from otree.api import *

doc = """
연구 소개(연구대상자 설명문)와 두 가지 동의(연구참여 동의, 개인정보 수집·이용 동의).
두 항목에 모두 동의한 참여자만 본 설문(ai_survey)으로 넘어갑니다.
"""

KST = timezone(timedelta(hours=9), name='KST')


class C(BaseConstants):
    NAME_IN_URL = 'consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    STUDY_TITLE = 'AI 관계대체 신념과 AI 애착의 관계: 관계적 행동과 심리적 웰빙에 대한 함의'
    # 설명문·동의서 문구가 바뀌면(재승인 등) 버전을 올려 주세요. 동의 시점의 버전이 응답과 함께 저장됩니다.
    CONSENT_VERSION = 'v1.0'
    DECLINE_MESSAGE = '동의하지 않으신 경우 연구에 참여하실 수 없습니다. 참여하지 않으셔도 불이익은 없습니다.'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    research_consent = models.StringField(
        label='연구참여 동의',
        choices=[['yes', '연구 참여에 동의함'], ['no', '연구 참여에 동의하지 않음']],
        widget=widgets.RadioSelect,
    )
    privacy_consent = models.StringField(
        label='개인정보 수집·이용 동의',
        choices=[['yes', '개인정보 수집 및 이용에 동의함'], ['no', '개인정보 수집 및 이용에 동의하지 않음']],
        widget=widgets.RadioSelect,
    )
    consent_timestamp = models.StringField(blank=True)
    consent_version = models.StringField(blank=True)


# PAGES


class Introduction(Page):
    use_blank_layout = True


class Consent(Page):
    form_model = 'player'
    form_fields = ['research_consent', 'privacy_consent']
    use_blank_layout = True
    allow_back_button = True

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.consent_version = C.CONSENT_VERSION
        player.consent_timestamp = datetime.now(KST).isoformat(timespec='seconds')
        # ai_survey 앱의 모든 페이지가 이 값으로 진입 여부를 판단합니다.
        player.participant.consent_ok = (
            player.research_consent == 'yes' and player.privacy_consent == 'yes'
        )


class ConsentDeclined(Page):
    """동의하지 않은 참여자에게 안내만 보여 주고 더 진행하지 못하게 합니다."""

    use_blank_layout = True
    # 잘못 선택한 경우 동의서로 돌아가 다시 선택할 수 있습니다.
    allow_back_button = True

    @staticmethod
    def is_displayed(player):
        return player.participant.vars.get('consent_ok') is not True

    @staticmethod
    def error_message(player, values):
        # 이 페이지에서는 어떤 제출 요청도 다음 단계로 넘어가지 못합니다.
        return C.DECLINE_MESSAGE


page_sequence = [Introduction, Consent, ConsentDeclined]
