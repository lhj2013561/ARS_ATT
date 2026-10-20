"""
배포 전 점검 스크립트

    python check_launch_ready.py           # 문항·설명문 원문이 모두 입력되었는지 확인
    python check_launch_ready.py --server  # 운영 서버의 환경변수 설정까지 확인

남은 항목이 있으면 목록을 보여 주고 종료 코드 1로 끝납니다.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MARK = '【입력 필요】'

SERVER_ENV = {
    'OTREE_PRODUCTION': lambda v: v not in (None, '', '0'),
    'OTREE_AUTH_LEVEL': lambda v: v == 'STUDY',
    'OTREE_ADMIN_PASSWORD': bool,
    'OTREE_SECRET_KEY': bool,
}


def unfilled_content():
    files = sorted(
        {*ROOT.glob('*/*.py'), *ROOT.glob('*/*.html'), *ROOT.glob('_templates/**/*.html')}
        - {ROOT / 'ai_survey' / 'tests.py', ROOT / 'research_consent' / 'tests.py'}
    )
    found = {}
    for path in files:
        for line_no, line in enumerate(path.read_text(encoding='utf-8').splitlines(), start=1):
            if MARK in line and not line.lstrip().startswith(('#', '{#')):
                found.setdefault(path.relative_to(ROOT), []).append(line_no)
    return found


def main():
    ok = True
    found = unfilled_content()
    if found:
        ok = False
        print(f'원문이 입력되지 않은 자리가 {sum(map(len, found.values()))}곳 있습니다 ({MARK}):')
        for path, line_numbers in found.items():
            print(f'  {path}: {len(line_numbers)}곳 (줄 {", ".join(map(str, line_numbers[:5]))}'
                  f'{" ..." if len(line_numbers) > 5 else ""})')
    else:
        print('문항·설명문: 입력되지 않은 자리가 없습니다.')

    if '--server' in sys.argv:
        for name, is_valid in SERVER_ENV.items():
            valid = is_valid(os.environ.get(name))
            ok = ok and valid
            print(f"  [{'OK' if valid else '확인 필요'}] {name}")

    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
