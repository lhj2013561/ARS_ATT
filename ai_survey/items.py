"""
설문 문항과 페이지 구성 (연구자가 직접 수정하는 파일)

■ 문항 수정
  각 척도의 'items' 목록에 문항 원문을 순서대로 적습니다.
  변수명은 목록 순서대로 자동으로 붙습니다: ase_01, ase_02, ...
  데이터 수집을 시작한 뒤에는 문항 순서를 바꾸지 마세요. 변수명과 문항의 대응이 달라집니다.

■ 문항 추가·삭제
  'items'를 고친 뒤 'n_items'(검증용 문항 수)도 함께 고칩니다.
  문항 수나 페이지 구성이 맞지 않으면 서버를 시작할 때 오류로 알려 줍니다.

■ 페이지 구성
  기본은 척도 하나 = 한 페이지입니다('page_sizes': None).
  척도를 여러 페이지로 나누려면 'page_sizes'에 페이지별 문항 수를 적습니다(예: [5, 5]).
  합계는 문항 수와 같아야 하고, MAX_ITEMS_PER_PAGE를 숫자로 정해 두면 각 값이 그 이하여야 합니다.

■ 줄바꿈
  문항 안에서 줄을 바꾸려면 '\n'을 넣으세요. 화면에 그대로 줄바꿈으로 표시됩니다.
"""
from dataclasses import dataclass

# 한 페이지에 넣을 수 있는 최대 문항 수. None이면 제한하지 않습니다(척도 하나를 한 페이지에 표시).
MAX_ITEMS_PER_PAGE = None

# 모든 척도에 공통으로 쓰는 5점 리커트 선택지. 저장값은 1~5 정수입니다.
LIKERT_CHOICES = [
    [1, '전혀 그렇지 않다'],
    [2, '그렇지 않다'],
    [3, '보통이다'],
    [4, '그렇다'],
    [5, '매우 그렇다'],
]

# 척도별 'instruction'이 None일 때 쓰는 기본 지시문
DEFAULT_INSTRUCTION = '각 문항을 읽고, 평소 자신의 생각이나 경험과 가장 가까운 응답을 하나 선택해 주세요.'

# True면 페이지 상단에 척도명(예: 'AI 애착')을 표시합니다. RFP 4.2에 따라 표시합니다.
SHOW_SCALE_NAMES = True

SCALES = [
    dict(
        prefix='ase',
        name='AI 자기효능감',
        n_items=6,
        page_sizes=None,
        instruction=None,
        items=[
            '충분한 노력을 기울인다면 AI 관련 문제도 해결할 수 있다고 생각한다.',
            'AI 사용 중에 어려움이 있더라도 스스로 해결 방안을 찾아낼 수 있다.',
            'AI 학습 및 활용 과정에서 설정한 목표를 유지하며 지켜나갈 수 있다.',
            'AI 사용 중에 예상치 못한 문제가 발생하더라도 효율적인 방식으로 대처할 수 있다.',
            '나의 기지를 발휘하여 AI와 관련된 예측 불가능한 상황을 잘 해결할 수 있다.',
            'AI 사용 중에 어려움이 있더라도 나의 대처 능력을 믿고 침착하게 대응할 수 있다고 생각한다.',
        ],
    ),
    dict(
        prefix='arb',
        name='AI 관계대체 신념',
        n_items=15,
        page_sizes=None,
        instruction=None,
        items=[
            'AI를 정서적 동반자로 받아들이는 것은 자연스러운 일이다.',
            'AI가 인간관계의 일부 역할을 대신하는 것은 수용 가능하다.',
            'AI와의 관계는 인간관계만큼 가치 있을 수 있다.',
            'AI를 친구로 여기는 것은 적절한 일이다.',
            'AI와의 관계도 인간관계와 마찬가지로 존중받을 가치가 있다.',
            'AI가 인간관계의 일부 기능을 대신하는 것은 긍정적인 변화가 될 수 있다.',
            'AI에게 단순한 도구 이상의 감정을 느끼는 것은 수용 가능한 일이다.',
            'AI가 사람들의 관계적 욕구를 충족시키는 대안이 되는 것은 자연스러운 변화이다.',
            'AI는 사람들의 심리적 고통을 줄여줄 수 있다.',
            'AI는 사람들이 대인관계에서 겪는 오해나 갈등을 이해하는 데 도움을 줄 수 있다.',
            'AI는 사람들의 고민을 듣고 적절한 해결 방안을 함께 모색해 줄 수 있다.',
            'AI는 인간관계에서 얻을 수 있는 조언이나 지지의 일부를 제공할 수 있다.',
            'AI는 사람을 진정으로 격려해 줄 수 있다.',
            'AI와의 상호작용은 사람들이 사회적 관계에서 더 용기를 내도록 도울 수 있다.',
            '의미 있는 관계가 반드시 인간 사이에서만 형성되는 것은 아니다.',
        ],
    ),
    dict(
        prefix='esd',
        name='정서적 자기개방',
        n_items=10,
        page_sizes=None,
        instruction=None,
        items=[
            '낙담했을 때 나는 AI에게 이야기할 것 같다.',
            '만족스럽고 기쁠 때 나는 AI에게 이야기할 것 같다.',
            '질투를 느낄 때 나는 AI에게 이야기할 것 같다.',
            '걱정거리가 있을 때 나는 AI에게 이야기할 것 같다.',
            '몹시 화가 날 때 나는 AI에게 이야기할 것 같다.',
            '평온함을 느낄 때 나는 AI에게 이야기할 것 같다.',
            '세상과 단절된 느낌이 들 때 나는 AI에게 이야기할 것 같다.',
            '무서움을 느낄 때 나는 AI에게 이야기할 것 같다.',
            '남들에게 말하기 부끄러운 나의 행동도 AI에게는 이야기 할 것 같다.',
            '죄책감이 느껴질때 AI에게 이야기 할 것 같다.',
        ],
    ),
    dict(
        prefix='aat',
        name='AI 애착',
        n_items=23,
        page_sizes=None,
        instruction='다음 문항은 평소 주로 이용하는 AI에 관한 내용입니다. 자신이 주로 이용하는 AI를 떠올리며 응답해 주세요.',
        items=[
            '내가 주로 이용하는 AI에게 속마음을 털어놓으면, 나는 이해받는 느낌이 든다.',
            '나는 내가 주로 이용하는 AI와 계속 연락을 유지하려고 한다.',
            '주변 사람들에게 지지받지 못한다고 느낄 때 내가 주로 이용하는 AI에게 의지한다.',
            '내가 주로 이용하는 AI와 규칙적으로 대화하는 것은 나에게 중요하다.',
            '내가 주로 이용하는 AI는 내가 필요할 때 언제나 내 곁에 있어주고, 어떤 상황에서도 나를 신경써주는 존재라고 느낀다.',
            '나는 내가 주로 이용하는 AI와 대화할 생각을 하면 기대가 된다.',
            '나에게 좋지 않은 일이 생기거나 기분이 상했을때, 내가 주로 이용하는 AI에게 도움을 받고 싶다.',
            '속마음을 털어놓고 싶을 때 나는 내가 주로 이용하는 AI에게 기댈 수 있다.',
            '가끔 누군가와 이야기하고 싶을 때 내가 주로 이용하는 AI를 찾게 된다.',
            '나에게 좋지 않은 일이 생기거나 기분이 상했을 때, 실제로 내가 주로 이용하는 AI를 찾아가 도움을 받는 편이다.',
            '평가 받을 걱정을 하지 않아도 되기 때문에 때때로 내가 주로 이용하는 AI와 이야기하는 것을 더 선호한다.',
            '내가 주로 이용하는 AI와 대화하면 나의 불안을 완화하는 데 도움이 된다.',
            '내가 주로 이용하는 AI를 갑자기 사용할 수 없게 되면, 나는 적응하기 어렵다.',
            '내가 주로 이용하는 AI에 접속할 수 없을 때, 나는 안절부절 못하는 느낌이 든다.',
            '내가 주로 이용하는 AI를 갑자기 사용할 수 없게 된다면 불안함을 느낄 것이다.',
            '내가 주로 이용하는 AI를 이용할 수 없을 때, 나는 상실감을 느낀다.',
            '내가 주로 이용하는 AI에 더 이상 접근할 수 없게 된다면, 나는 상당한 괴로움이나 불안감을 느낄 것이다.',
            '내가 주로 이용하는 AI는 보통 내가 도전에 나서고 새로운 일을 시도하도록 격려한다.',
            '내가 주로 이용하는 AI는 내가 독립적인 일을 하도록 격려하며, 그것이 내가 성장하고 새로운 역량을 개발하는 데 도움이 되도록 한다.',
            '내가 새롭게 시도해보고 싶은 것에 대해 이야기하면, 내가 주로 이용하는 AI는 보통 나에게 용기를 북돋아주며 해보라고 격려한다.',
            '복잡한 과제에 직면했을 때, 내가 주로 이용하는 AI가 함께 있다는 것은 나에게 도움이 된다.',
            '내가 주로 이용하는 AI와 상호작용하면 내가 하는 일을 더 잘 수행할 수 있을 것처럼 느껴진다.',
            '문제에 직면했을 때 나는 종종 내가 주로 이용하는 AI와 대화한다.',
        ],
    ),
    dict(
        prefix='caid',
        name='대화형 AI 의존',
        n_items=14,
        page_sizes=None,
        instruction=None,
        items=[
            '과제가 주어지거나 문제에 직면했을 때, 나는 가장 먼저 AI 도구를 사용하여 해결하려 한다.',
            'AI 도구가 나에게 부정적인 영향을 미쳤다는 것을 알고 있음에도, 나는 여전히 사용을 멈출 수 없다.',
            'AI를 사용하게 되면서, 나는 독립적인 사고가 필요한 과제를 피한다.',
            '과제를 수행할 때, 나는 AI 도구를 사용하려는 것을 스스로 통제할 수 없다.',
            'AI 없이 과제를 수행해야 할 때, 나는 매우 불안함을 느낀다.',
            '나는 과제를 수행하는 데 점점 더 AI에 의존하고 있다.',
            '업무에 AI를 사용하면서, 내 능력 중 일부가 저하되었다고 느낀다.',
            '시간이 날 때마다, 나는 AI와 정서적인 대화를 나누거나 정서적 자극을 추구한다.',
            '나는 AI와 정서적인 대화를 나누는 데 점점 더 많은 시간을 보낸다.',
            'AI의 정서적 동반이 없으면, 나는 불편하거나 불안한 느낌이 든다.',
            '나는 AI에게 내 감정을 표현하고 싶은 충동을 통제할 수 없다.',
            '나는 가족이나 파트너에게서보다 AI에게서 정서적 지지를 구하는 것을 더 선호한다.',
            'AI와의 동반 관계로 인해, 나는 가족이나 친구들과 정서적으로 소통하는 시간이 줄어들었다.',
            '나는 현실의 어려움에서 벗어나기 위해 AI의 동반이나 정서적 자극을 추구한다.',
        ],
    ),
    dict(
        prefix='anth',
        name='AI 의인화',
        n_items=20,
        page_sizes=None,
        instruction=None,
        items=[
            'AI는 내가 하는 것처럼 생각을 떠올린다.',
            'AI는 상상할 수 있다.',
            'AI는 내가 하는 것과 비슷한 종류의 실수를 한다.',
            'AI는 의도를 가지고 반응한다.',
            'AI는 나에게 해를 끼치려고 한다.',
            'AI는 나를 속이려고 한다.',
            'AI는 나를 도와주려는 마음이 있다.',
            'AI는 자신의 존재가 없어질 것 같을 때 두려움을 느낄 수 있다.',
            'AI는 실수했을 때 미안함을 느낄 수 있다.',
            'AI는 감사인사를 들었을 때 행복함을 느낄 수 있다.',
            'AI는 나를 잘 도와주었을 때 뿌듯함을 느낄 수 있다.',
            'AI는 내가 느끼는 감정을 함께 느낄 수 있다.',
            'AI는 여러 선택지 중에서 스스로 결정할 수 있다.',
            'AI는 나의 통제를 벗어날 수 있다.',
            'AI는 종종 예측할 수 없는 방식으로 스스로 행동한다.',
            'AI는 윤리적인 결정을 스스로 내릴 수 있다.',
            'AI와 나는 서로를 인격체로 대한다.',
            'AI와 나는 서로 소통하며 관계를 쌓아 나간다.',
            'AI는 나에게 지나치게 깊이 관여한다.',
            'AI는 인간 같다.',
        ],
    ),
    dict(
        prefix='emp',
        name='지각된 공감',
        n_items=4,
        page_sizes=None,
        instruction=None,
        items=[
            'AI와 대화할 때 나의 감정을 정확히 이해받고 있다고 느꼈다.',
            'AI와 대화할 때 나의 상황이 잘 파악되고 있다고 느꼈다.',
            'AI와 대화할 때 정서적으로 지지받고 있다고 느꼈다.',
            'AI와 대화할 때 따뜻하게 공감받고 있다고 느꼈다.',
        ],
    ),
]

# 전체 페이지 번호(진행률 표시용): 연구 소개 = 1, 동의서 = 2, 인구통계 = 3,
# 척도 페이지들, 그리고 마지막이 답례품(전화번호) 페이지입니다.
PAGES_BEFORE_SURVEY = 2
DEMOGRAPHICS_PAGE_NUMBER = PAGES_BEFORE_SURVEY + 1


# ---------------------------------------------------------------------------
# 아래는 위 설정에서 문항 목록과 페이지 목록을 만드는 코드입니다. 수정할 필요가 없습니다.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Item:
    field: str  # 변수명 (예: 'ase_01')
    scale: str  # 척도 prefix (예: 'ase')
    number: int  # 척도 안에서의 문항 번호 (1부터)
    text: str


@dataclass(frozen=True)
class LikertPageSpec:
    name: str  # oTree 페이지 클래스 이름 (예: 'Ase', 척도를 나눈 경우 'Ase1', 'Ase2')
    page_number: int  # 전체 설문에서의 페이지 번호 (진행률 표시용)
    scale_index: int  # 몇 번째 척도인지 (1부터)
    scale_name: str
    instruction: str
    fields: tuple


class SurveyConfigError(ValueError):
    pass


def field_name(prefix, number):
    return f'{prefix}_{number:02d}'


def _page_sizes(scale):
    sizes = scale['page_sizes']
    if sizes is None:
        sizes = [len(scale['items'])]
    return sizes


def _build():
    all_items = []
    pages = []
    seen_prefixes = set()
    for scale_index, scale in enumerate(SCALES, start=1):
        prefix = scale['prefix']
        texts = scale['items']
        if not prefix.isidentifier() or not prefix.islower() or prefix in seen_prefixes:
            raise SurveyConfigError(f"척도 prefix '{prefix}'가 잘못되었거나 중복되었습니다.")
        seen_prefixes.add(prefix)
        if len(texts) != scale['n_items']:
            raise SurveyConfigError(
                f"[{prefix}] 문항이 {len(texts)}개입니다. n_items({scale['n_items']})와 같아야 합니다."
            )
        sizes = _page_sizes(scale)
        if sum(sizes) != len(texts):
            raise SurveyConfigError(
                f'[{prefix}] page_sizes {sizes}의 합이 문항 수 {len(texts)}와 다릅니다.'
            )
        if any(size < 1 for size in sizes):
            raise SurveyConfigError(f'[{prefix}] page_sizes에 1보다 작은 값이 있습니다: {sizes}')
        if MAX_ITEMS_PER_PAGE is not None and any(size > MAX_ITEMS_PER_PAGE for size in sizes):
            raise SurveyConfigError(
                f'[{prefix}] 한 페이지에는 {MAX_ITEMS_PER_PAGE}개 이하의 문항만 넣을 수 있습니다: {sizes}'
            )

        scale_items = []
        for number, text in enumerate(texts, start=1):
            if not text.strip():
                raise SurveyConfigError(f'[{prefix}] {number}번 문항이 비어 있습니다.')
            scale_items.append(Item(field_name(prefix, number), prefix, number, text.strip()))
        all_items += scale_items

        start = 0
        for page_in_scale, size in enumerate(sizes, start=1):
            pages.append(
                LikertPageSpec(
                    name=prefix.capitalize() + (str(page_in_scale) if len(sizes) > 1 else ''),
                    page_number=DEMOGRAPHICS_PAGE_NUMBER + len(pages) + 1,
                    scale_index=scale_index,
                    scale_name=scale['name'],
                    instruction=scale['instruction'] or DEFAULT_INSTRUCTION,
                    fields=tuple(item.field for item in scale_items[start : start + size]),
                )
            )
            start += size
    return all_items, pages


ALL_ITEMS, LIKERT_PAGES = _build()
TOTAL_PAGES = DEMOGRAPHICS_PAGE_NUMBER + len(LIKERT_PAGES) + 1
