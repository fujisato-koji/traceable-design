"""Keep the copies of the tool and the skill in step with their sources.

usage: python tools/sync_copies.py          copy each source over its copies
       python tools/sync_copies.py --check  exit 1 if any copy differs

Run from the repository root. Standard library only.
"""
import sys
from pathlib import Path

COPIES = [
    ('tools/tdr.py', 'template/tools/tdr.py'),
    ('tools/tdr.py', 'skill/traceable-design/scripts/tdr.py'),
    ('skill/traceable-design/SKILL.md', 'template/.claude/skills/traceable-design/SKILL.md'),
]


def main():
    check = '--check' in sys.argv[1:]
    bad = 0
    for src, dst in COPIES:
        data = Path(src).read_bytes()
        target = Path(dst)
        if check:
            if not target.exists() or target.read_bytes() != data:
                print(f'differs: {dst} (source {src})')
                bad += 1
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            print(f'copied: {src} -> {dst}')
    if check and not bad:
        print('ok')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
