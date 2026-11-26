"""Check 3: does the browser give a capture time on the local camera stream (`captureTime`)? If not, the spread (SD)
of the measured offset of the `expectedDisplayTime` fallback (spec §1.2.1).

Run with the page open. The page sends {"kind": "clock", "values": [{"capture_time": bool, "offset_ms": float},
...]} for 1,800 frames (1 min at 30 Hz); offset_ms is expectedDisplayTime minus the page-to-engine mapped frame time.
    uv run python -m tools.week0.clock [--from-file samples.json]
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

from tools.week0 import common, page_checks, thresholds

FRAMES = 1800


def main(argv=None) -> int:
    p = page_checks.args_with_file(__doc__)
    args = p.parse_args(argv)
    load = page_checks.prepare(args)
    if args.from_file:
        xs = json.loads(Path(args.from_file).read_text())
    else:
        common.require_page()
        xs = common.receive_page_samples("clock", FRAMES, timeout_s=FRAMES / 30.0 + 60)
    if len(xs) < 0.9 * FRAMES:
        raise common.Refused(f"only {len(xs)} of {FRAMES} frames received")
    present = all(bool(x.get("capture_time")) for x in xs)
    offsets = [float(x["offset_ms"]) for x in xs if x.get("offset_ms") is not None]
    sd = round(statistics.stdev(offsets), 3) if len(offsets) > 1 else None
    v = thresholds.clock(present, sd)
    return common.finish(v, args, load=load, note=f"{len(xs)} frames")


if __name__ == "__main__":
    sys.exit(main())
