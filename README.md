# AI 관계대체 신념과 AI 애착 — oTree 온라인 설문

연구 제목: **AI 관계대체 신념과 AI 애착의 관계: 관계적 행동과 심리적 웰빙에 대한 함의**

oTree 6.x 기반 온라인 설문입니다. 연구 소개 → 두 가지 동의 → 성별·연령 → 7개 척도 92문항(5점 리커트) → 답례품용 휴대전화번호(선택) 순서로 진행됩니다.

> 문항이나 설명문을 고친 뒤에는 `python check_launch_ready.py`로 원문이 빠진 자리(`【입력 필요】`)가 없는지 확인하세요.

---

## 1. 화면 구성

| 쪽 | 화면 | oTree 페이지 | 문항 |
|---:|---|---|---:|
| 1 | 연구 소개(연구대상자 설명문) | `research_consent.Introduction` | – |
| 2 | 연구참여 동의 + 개인정보 수집·이용 동의 | `research_consent.Consent` | 동의 2 |
| – | (비동의 시) 참여 불가 안내 | `research_consent.ConsentDeclined` | – |
| 3 | 성별·연령 | `ai_survey.Demographics` | 2 |
| 4 | AI 자기효능감 | `ai_survey.Ase` | 6 |
| 5 | AI 관계대체 신념 | `ai_survey.Arb` | 15 |
| 6 | 정서적 자기개방 | `ai_survey.Esd` | 10 |
| 7 | AI 애착 | `ai_survey.Aat` | 23 |
| 8 | 대화형 AI 의존 | `ai_survey.Caid` | 14 |
| 9 | AI 의인화 | `ai_survey.Anth` | 20 |
| 10 | 지각된 공감 | `ai_survey.Emp` | 4 |
| 11 | 답례품 지급용 전화번호 | `ai_survey.PhoneNumber` | 선택 1 |
| (11) | 제출 완료 | `ai_survey.Completed` | – |

- **척도 하나를 한 페이지에 모두 표시합니다.** 한 페이지에 두 척도가 섞이지 않고, 한 척도가 여러 페이지로 나뉘지도 않습니다. 전체 11쪽입니다.
- 별도 종료 페이지는 없습니다. 제출하면 같은 화면 구성(같은 템플릿)에 완료 메시지가 표시됩니다. oTree 구조상 내부 페이지 이름만 `Completed`로 바뀝니다.
- 척도 페이지(4–10쪽)와 전화번호 페이지에는 **이전** 버튼이 있습니다. 돌아가면 저장된 응답이 선택된 상태로 표시됩니다. 아직 제출하지 않은 현재 페이지의 선택도 브라우저 탭 안에서 유지되므로, 긴 척도 페이지에서 새로고침해도 선택이 남아 있습니다.
- 성별·연령 페이지(3쪽)에는 이전 버튼이 없습니다. 동의 단계로 되돌아가 동의를 바꿀 수 없게 하기 위함입니다.
- 척도 페이지 상단에는 `파트 2 / 7 · AI 관계대체 신념`처럼 순서와 척도명이 표시됩니다. 척도명을 숨기려면 `items.py`의 `SHOW_SCALE_NAMES = False`로 바꾸세요.

## 2. 폴더 구조

```text
ai_research_survey/
├── settings.py                 세션 설정, 언어(ko), 배포용 Room, 운영 모드 보안 검사
├── requirements.txt
├── Procfile                    Heroku 배포용
├── check_launch_ready.py       배포 전 점검(원문 입력 여부, 서버 환경변수)
├── _static/css/survey.css      화면 스타일(모바일 우선)
├── _static/js/survey.js        미응답 안내, 중복 제출 방지, 전화번호 형식 보조
├── _templates/global/          공통 레이아웃(Page.html), 진행률 표시줄(Progress.html)
├── research_consent/           연구 소개 + 동의 앱
│   ├── __init__.py             동의 변수, 동의 검증, 비동의 처리
│   ├── Introduction.html / Consent.html / ConsentDeclined.html
│   └── tests.py                동의 관련 자동 테스트(봇)
└── ai_survey/                  본 설문 앱
    ├── items.py                ★ 문항 텍스트·척도·페이지 구성 (연구자가 수정하는 파일)
    ├── __init__.py             변수, 페이지, 전화번호 처리, CSV 내보내기
    ├── Demographics.html / LikertPage.html(모든 척도 공통) / PhoneNumber.html
    └── tests.py                설문·저장·내보내기 자동 테스트(봇)
```

## 3. 로컬에서 실행하기

Python 3.10 이상이 필요합니다(Python 3.14 + oTree 6.0.15에서 테스트했습니다).

```bash
cd ai_research_survey
pip install -r requirements.txt
otree devserver
```

브라우저에서 <http://localhost:8000> 을 열고 **Demo → AI 관계대체 신념과 AI 애착 온라인 설문**을 누르면 참여자 화면을 볼 수 있습니다. 개발 모드에서는 화면 아래에 *Debug info*가 보이며, 운영 모드에서는 보이지 않습니다.

> **`otree devserver`가 아무 메시지 없이 바로 끝나는 경우**
> PATH의 `otree` 명령이 다른(지워진) Python 설치를 가리키는 경우입니다. `where otree`로 확인한 뒤, oTree를 설치한 Python의 `Scripts\otree.exe`가 먼저 오도록 PATH를 고치세요.
> (`otree devserver`는 내부에서 PATH의 `otree`를 다시 호출합니다.)

## 4. 문항·문구 수정

### 문항 입력/수정 — `ai_survey/items.py`

```python
dict(
    prefix='ase',             # 변수명 접두어 → ase_01, ase_02, ...
    name='AI 자기효능감',       # 척도명 (페이지 상단에 표시)
    n_items=6,                # 검증용 문항 수
    page_sizes=None,          # None = 척도 전체를 한 페이지에 표시
    instruction=None,         # 척도별 지시문 (None이면 DEFAULT_INSTRUCTION)
    items=[
        '첫 번째 문항 원문',
        '두 번째 문항 원문',
        ...
    ],
),
```

- `items`의 순서가 곧 변수 번호입니다. **데이터 수집을 시작한 뒤에는 순서를 바꾸거나 문항을 추가·삭제하지 마세요.** 변수 구성이 바뀌면 DB를 초기화해야 합니다.
- 문항 수가 `n_items`와 다르거나 변수명이 겹치면 서버가 시작될 때 한국어 오류 메시지로 알려 줍니다.
- 문항 안에서 줄을 바꾸려면 `\n`을 넣습니다. 문항 텍스트는 HTML로 해석되지 않고 그대로 표시됩니다.
- 나중에 한 척도를 여러 페이지로 나누고 싶다면 `page_sizes`에 페이지별 문항 수를 적습니다(예: `[3, 3]`, 합계 = 문항 수). 페이지당 최대 문항 수를 강제하려면 `MAX_ITEMS_PER_PAGE`를 숫자로 정합니다(현재는 `None`, 제한 없음).

### 설명문·동의서 문구

- 연구 소개: `research_consent/Introduction.html`
- 동의서: `research_consent/Consent.html`
- 거부 안내 문구, 연구 제목, 동의서 버전: `research_consent/__init__.py`의 `C` 클래스

설명문·동의서 문구는 RFP에 적힌 문장을 그대로 옮겼습니다. 배포 전에 IRB 승인본과 한 번 더 대조해 주세요. **문구를 바꾸면 `C.CONSENT_VERSION`을 올려 주세요.** 참여자별로 동의한 버전이 저장됩니다.

### 연령 입력 범위

`ai_survey/__init__.py`의 `C.AGE_MIN`, `C.AGE_MAX`(기본 1–120)는 오입력을 막기 위한 범위입니다. 참여 자격 기준(예: 만 19세 이상)이 있으면 이 값을 조정하세요.

## 5. 테스트

```bash
otree test ai_research_survey     # 자동 봇 테스트 (6개 시나리오)
python check_launch_ready.py      # 원문 미입력 자리 점검
```

봇 테스트가 확인하는 내용:

| 영역 | 확인 항목 |
|---|---|
| 동의 | 첫 화면이 연구 소개 / 두 동의서 모두 표시 / 기본 선택 없음 / 미선택·한쪽만 선택 시 진행 불가 / 연구참여만, 개인정보만, 둘 다 비동의 시 안내 화면에서 멈춤 / 비동의 후 동의서로 돌아가 다시 동의 가능 / 동의 시각(KST)·버전 기록 |
| 접근 차단 | 비동의 참여자가 설문 페이지 URL에 직접 GET·POST해도 현재 위치로 되돌려지고 아무 응답도 저장되지 않음 |
| 설문 | 92문항이 원래 순서대로 빠짐없이·중복 없이 표시 / 척도 하나 = 한 페이지(척도가 섞이거나 나뉘지 않음) / 모든 문항이 1–5 선택지 5개 / 처음엔 선택 없음 / 미응답·범위 밖 값(0, 6)이면 진행 불가 / 성별·연령 필수, 연령은 정수·범위 검사 / 이전 버튼으로 돌아가면 응답 유지 / 진행률 표시 |
| 제출·데이터 | 전화번호 없이 제출 가능 / 입력 시 `010-1234-5678` 형식으로 저장 / 잘못된 형식 거부 / 같은 제출을 다시 보내도 중복 저장 없음 / 제출 후 이전 페이지 응답 수정 불가 / 완료 메시지 표시 / 분석용 CSV에 전화번호 없음 / 답례품 명단에 참여자 코드 없음 |

배포 전에 휴대전화와 PC에서 직접 한 번씩 끝까지 응답해 보는 것을 권장합니다.

## 6. 서버 배포

### 필수 환경변수

| 변수 | 값 | 설명 |
|---|---|---|
| `OTREE_PRODUCTION` | `1` | 운영 모드 (Debug info 숨김) |
| `OTREE_AUTH_LEVEL` | `STUDY` | 관리자 화면·데이터 내보내기를 비밀번호로 보호. **비어 있으면 누구나 데이터를 내려받을 수 있습니다.** |
| `OTREE_ADMIN_PASSWORD` | 긴 비밀번호 | 관리자(`admin`) 비밀번호 |
| `OTREE_SECRET_KEY` | 임의의 긴 문자열 | 세션 서명 키 |
| `DATABASE_URL` | (선택) `postgres://...` | 지정하지 않으면 프로젝트 폴더의 `db.sqlite3` 사용 |

`settings.py`는 `OTREE_PRODUCTION=1`인데 `OTREE_AUTH_LEVEL=STUDY` 또는 관리자 비밀번호가 없으면 **서버를 시작하지 않습니다.** 서버에서 `python check_launch_ready.py --server`로 환경변수를 점검할 수 있습니다.

### 방법 A: oTree Hub + Heroku

1. `otree zip`으로 `ai_research_survey.otreezip`을 만듭니다.
2. [oTree Hub](https://www.otreehub.com)에서 Heroku 앱을 연결하고 zip을 업로드합니다.
3. Heroku *Config Vars*에 위 환경변수를 넣습니다. Heroku는 PostgreSQL(`DATABASE_URL`)을 자동으로 씁니다.

### 방법 B: 직접 운영하는 서버(Linux)

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export OTREE_PRODUCTION=1 OTREE_AUTH_LEVEL=STUDY OTREE_ADMIN_PASSWORD='...' OTREE_SECRET_KEY='...'
otree prodserver 8000
```

- **HTTPS가 필요합니다.** Caddy·nginx 같은 리버스 프록시로 443 포트를 받아 `localhost:8000`으로 넘기세요. 웹소켓도 전달하도록 설정해야 합니다. 예: Caddy는 `example.ac.kr { reverse_proxy localhost:8000 }`.
- systemd 등으로 프로세스를 상시 실행하세요.
- 처음 실행할 때 DB 테이블이 자동으로 만들어집니다.
- SQLite(기본)를 쓰면 `db.sqlite3` 파일이 곧 연구자료입니다. 정기적으로 백업하고 접근 권한을 제한하세요.

> ⚠️ **데이터 수집을 시작한 뒤에는 `otree resetdb`를 실행하지 마세요.** 모든 응답이 삭제됩니다.

### 참여 링크 배포

1. 관리자 화면 → **Rooms** → *AI 관계 연구 온라인 설문* → 세션 만들기.
2. 참여자 수는 목표(400명)보다 넉넉하게 잡습니다(예: 600). 비동의·중도 이탈자도 한 자리를 쓰기 때문입니다.
3. 참여자에게는 **`https://<서버 주소>/room/ai_survey`** 링크 하나만 배포합니다.
   - 같은 브라우저로 다시 접속하면 하던 곳부터 이어집니다.
   - 자리가 모두 차면 새 접속자는 참여할 수 없으니 관리자 화면에서 진행 상황을 확인하세요.

## 7. 데이터 내보내기

관리자 화면 → **Data** → **Custom exports**에서 내려받습니다. 엑셀에서 열 때는 한글이 깨지지 않도록 **Excel CSV**를 고르세요.

| 파일 | 내용 |
|---|---|
| `ai_survey: custom_export_analysis` | **분석용 CSV.** 링크에 접속한 참여자 1명당 1행. 전화번호 없음 |
| `ai_survey: custom_export_reward_list` | **답례품 지급 명단.** 휴대전화번호만 있고 참여자 코드·응답과 연결되지 않음 |

### 분석용 CSV 코드북

| 변수 | 값 |
|---|---|
| `participant_code` | oTree 참여자 고유 코드 |
| `session_code` | 세션 코드 |
| `research_consent`, `privacy_consent` | `yes` / `no` (빈칸 = 동의 단계에 도달하지 않음) |
| `consent_timestamp` | 동의 제출 시각, 한국 시간 ISO 8601 (예: `2026-11-03T14:22:05+09:00`) |
| `consent_version` | 동의 시점의 동의서 버전 |
| `gender` | 1 = 남성, 2 = 여성, 3 = 기타, 4 = 응답하고 싶지 않음 |
| `age` | 만 나이(정수) |
| `ase_01`–`ase_06` | AI 자기효능감 |
| `arb_01`–`arb_15` | AI 관계대체 신념 |
| `esd_01`–`esd_10` | 정서적 자기개방 |
| `aat_01`–`aat_23` | AI 애착 |
| `caid_01`–`caid_14` | 대화형 AI 의존 |
| `anth_01`–`anth_20` | AI 의인화 |
| `emp_01`–`emp_04` | 지각된 공감 |
| `survey_completed` | 1 = 최종 제출 완료, 0 = 미완료 |
| `completion_timestamp` | 최종 제출 시각(KST) |
| `participation_status` | `completed` / `in_progress`(동의 후 미완료) / `declined`(하나 이상 비동의) / `consent_pending`(동의 전 이탈) |
| `last_page` | 마지막으로 머문 oTree 페이지 이름(이탈 위치 확인용) |

- 리커트 문항은 1 = 전혀 그렇지 않다 … 5 = 매우 그렇다 인 **원점수**입니다. 역채점·총점·평균은 계산하지 않습니다.
- **결측은 빈칸**입니다. 0으로 채우지 않습니다.

### 답례품 지급 명단

| 열 | 내용 |
|---|---|
| `no` | 일련번호(전화번호 순 정렬. 제출 순서가 아님) |
| `phone_number` | `010-1234-5678` 형식 |
| `submitted_date` | 제출 날짜(시각은 저장하지 않음) |
| `same_number_count` | 같은 번호가 명단에 나온 횟수. 2 이상이면 중복 참여 여부를 확인하세요 |

### 전화번호 처리 방식

- 전화번호는 응답 테이블(`Player`)에 저장하지 않습니다. 제출 순간 별도 테이블(`RewardContact`)로 옮기고, 응답 쪽 칸은 비웁니다.
- `RewardContact`에는 참여자 연결 정보가 없고 세션 단위로만 묶입니다. 날짜만 저장하고 시각은 저장하지 않습니다.
- 따라서 분석 자료와 답례품 명단을 서로 짝지을 수 없습니다. 응답 품질에 따라 답례품 지급을 달리하는 운영은 이 구조로는 할 수 없습니다.
- 잘못된 형식의 오류 메시지에 입력값을 다시 넣지 않습니다. 오류가 나도 입력칸을 미리 채워 두지 않으며, 전화번호를 URL이나 브라우저 저장소에 남기지 않습니다.
- oTree 기본 내보내기(*All apps*, *ai_survey*)에도 `phone_number` 열이 있지만 **항상 비어 있습니다.**
- oTree에는 관리자 계정이 하나뿐입니다. 답례품 명단 다운로드 권한은 관리자 비밀번호를 가진 사람으로 한정됩니다. 비밀번호는 연구책임자만 관리하는 것을 권장합니다.

## 8. 동의 검증 규칙

| 연구참여 동의 | 개인정보 동의 | 처리 |
|---|---|---|
| 동의 | 동의 | 설문 시작 |
| 동의 | 비동의 | 안내 화면에서 멈춤 |
| 비동의 | 동의 | 안내 화면에서 멈춤 |
| 비동의 | 비동의 | 안내 화면에서 멈춤 |
| 미선택 | – | 해당 항목에 "동의 여부를 선택해 주세요" 표시, 진행 불가 |

- "동의하지 않음"을 고르는 즉시 *"동의하지 않으신 경우 연구에 참여하실 수 없습니다. 참여하지 않으셔도 불이익은 없습니다."*가 표시됩니다.
- 비동의로 제출하면 같은 문구가 담긴 안내 화면으로 이동합니다. 안내 화면에서는 어떤 요청으로도 다음 단계로 갈 수 없고, **동의서로 돌아가기**만 가능합니다(잘못 누른 경우 대비).
- 본 설문의 모든 페이지는 서버에서 동의 여부를 다시 확인합니다(`is_displayed`). 또한 oTree는 참여자가 자기 현재 페이지 외의 URL에 접근하면 현재 페이지로 되돌립니다.
- 비동의자는 동의 여부·시각·버전만 기록됩니다. 인구통계·척도 자료는 수집되지 않습니다.
