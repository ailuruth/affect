"""Check 8: the 2-Hz tick (body, readers, gate inputs, appraisal, the shadow's T state, A5, A14), p99, at full load.
Run (5 min by default):
    uv run python -m tools.week0.slow_tick [--seconds 300]
"""
from __future__ import annotations

import sys

from tools.week0 import common, thresholds, ticks


def main(argv=None) -> int:
    p = common.parser(__doc__)
    p.add_argument("--seconds", type=float, default=300.0)
    args = p.parse_args(argv)
    if not args.dry_run:
        common.require_mac()
    load = common.require_full_load(args)
    _, slow_ms = ticks.run(args.seconds)
    v = thresholds.slow_tick(round(thresholds.percentile(slow_ms, 99), 3))
    return common.finish(v, args, load=load, note=f"{len(slow_ms)} ticks (M untrained, not built at M4)")


if __name__ == "__main__":
    sys.exit(main())
