"""Check 1: FaceLandmarker (partner instance) time per frame, p99, at full load, with the own-face instance at
10 Hz; above 30 ms, set the own instance to 5 Hz in the page and run again with --after-branch.

Sit in front of the camera with the page open (web/index.html, served from localhost). The page sends
{"kind": "track_ms", "values": [...]} (one value per partner frame, ms). 9,000 frames = 5 min at 30 Hz. Run:
    uv run python -m tools.week0.tracker [--after-branch] [--from-file samples.json]
"""
from __future__ import annotations

import sys

from tools.week0 import common, page_checks, record, thresholds

FRAMES = 9000


def main(argv=None) -> int:
    p = page_checks.args_with_file(__doc__)
    p.add_argument("--after-branch", action="store_true", help="the own-face instance is now at 5 Hz")
    args = p.parse_args(argv)
    load = page_checks.prepare(args)
    xs = common.samples_from(args, "track_ms", FRAMES, timeout_s=FRAMES / 30.0 + 120)
    if len(xs) < 0.9 * FRAMES:
        raise common.Refused(f"only {len(xs)} of {FRAMES} frames received")
    p99 = round(thresholds.percentile(xs, 99), 3)
    if args.after_branch:
        prev = [r for r in record.parse() if r["check"] == "tracker"]
        if not prev:
            raise common.Refused("--after-branch needs the first tracker measurement in week0.md")
        v = thresholds.tracker(prev[-1]["measured"]["p99_ms"], p99)
    else:
        v = thresholds.tracker(p99)
    rc = common.finish(v, args, load=load, note=f"{len(xs)} frames; own instance {'5' if args.after_branch else '10'} Hz")
    if v.outcome == "remeasure":
        print("next: set the own-face instance to 5 Hz in the page, then run: "
              "uv run python -m tools.week0.tracker --after-branch")
    return rc


if __name__ == "__main__":
    sys.exit(main())
