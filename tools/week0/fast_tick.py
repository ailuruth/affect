"""Check 7: the 30-Hz engine tick, p99, at full load (Plan A, numpy). Above 5 ms the table selects Plan B (a native
extension, spec §2.1), measured again with --plan B once it exists. Run (5 min by default):
    uv run python -m tools.week0.fast_tick [--seconds 300] [--plan B]
"""
from __future__ import annotations

import sys

from tools.week0 import common, thresholds, ticks


def main(argv=None) -> int:
    p = common.parser(__doc__)
    p.add_argument("--seconds", type=float, default=300.0)
    p.add_argument("--plan", choices=("A", "B"), default="A")
    args = p.parse_args(argv)
    if args.plan == "B":
        raise common.Refused("Plan B (the native extension of spec §2.1) is not built yet")
    if not args.dry_run:
        common.require_mac()
    load = common.require_full_load(args)
    fast_ms, _ = ticks.run(args.seconds)
    v = thresholds.fast_tick(round(thresholds.percentile(fast_ms, 99), 3), args.plan)
    return common.finish(v, args, load=load, note=f"{len(fast_ms)} frames; fast and slow parts in one process (M4 core)")


if __name__ == "__main__":
    sys.exit(main())
