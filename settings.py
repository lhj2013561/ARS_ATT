from os import environ

SESSION_CONFIGS = [
    dict(
        name='ai_research_survey',
        display_name='AI 관계대체 신념과 AI 애착 온라인 설문',
        app_sequence=['research_consent', 'ai_survey'],
        num_demo_participants=1,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# consent_ok: 두 동의를 모두 했는지 여부. 본 설문 페이지의 진입 검증에 사용합니다.
PARTICIPANT_FIELDS = ['consent_ok']
SESSION_FIELDS = []

LANGUAGE_CODE = 'ko'

REAL_WORLD_CURRENCY_CODE = 'KRW'
USE_POINTS = False

# 온라인 배포용 고정 링크: https://<서버 주소>/room/ai_survey
ROOMS = [
    dict(name='ai_survey', display_name='AI 관계 연구 온라인 설문'),
]

ADMIN_USERNAME = 'admin'
# 관리자 비밀번호는 서버 환경변수 OTREE_ADMIN_PASSWORD로 설정합니다 (README 참고).
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
AI 관계대체 신념과 AI 애착의 관계: 관계적 행동과 심리적 웰빙에 대한 함의 (온라인 설문)
"""

SECRET_KEY = environ.get('OTREE_SECRET_KEY', '1090813662826')

# 운영 모드(OTREE_PRODUCTION=1)에서는 관리자 화면과 데이터 내보내기가 반드시 비밀번호로 보호되어야 합니다.
# OTREE_AUTH_LEVEL이 비어 있으면 oTree는 데이터 내보내기 API까지 누구에게나 열어 두므로 서버를 시작하지 않습니다.
if environ.get('OTREE_PRODUCTION') not in [None, '', '0']:
    if environ.get('OTREE_AUTH_LEVEL') != 'STUDY' or not ADMIN_PASSWORD:
        raise RuntimeError(
            '운영 서버에서는 환경변수 OTREE_AUTH_LEVEL=STUDY 와 OTREE_ADMIN_PASSWORD 를 반드시 설정해야 합니다. '
            'README의 "서버 배포" 항목을 참고하세요.'
        )
