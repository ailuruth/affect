"""Last step of M1: rewrite the summary of research/build/week0.md (the latest number of each check and the branch it
selects, the combined recogniser plan of checks 4 and 5, and M1's status: complete, open or stopped). Run:
    uv run python -m tools.week0.report
"""
from __future__ import annotations

import sys

from tools.week0 import common, record


def main(argv=None) -> int:
    p = common.parser(__doc__)
    args = p.parse_args(argv)
    if args.dry_run:
        s = record.summary(record.parse())
    else:
        s = record.write_summary()
    print(f"M1 status: {s['status']}")
    for k in ("failed", "open", "missing"):
        if s[k]:
            print(f"  {k}: {', '.join(s[k])}")
    if "asr_plan" in s:
        print(f"  recognisers: {s['asr_plan'].outcome} -> {s['asr_plan'].selects}")
    return 1 if s["status"] == "stopped" else 0


if __name__ == "__main__":
    sys.exit(main())
