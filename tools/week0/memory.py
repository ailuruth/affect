"""Check 9: peak memory of all processes of the load session (and their children), summed, over the session.

Samples the resident size with macOS's `ps` once a second until the load session ends. Above 6.0 GB the table's
steps apply in order (4-bit Kyutai, then a Claude pool of 2, then 1); run again with --step for each. Run while the
load session runs (start both together):
    uv run python -m tools.week0.memory [--step plan_a|kyutai_4bit|pool_2|pool_1]
"""
from __future__ import annotations

import subprocess
import sys
import time

from tools.week0 import common, thresholds


def tree_rss_kb(roots) -> int:
    """Sum of RSS (KB) of the given pids and all their descendants, from one `ps` snapshot."""
    out = subprocess.run(["ps", "-A", "-o", "pid=,ppid=,rss="], capture_output=True, text=True, check=True).stdout
    rows = [tuple(int(v) for v in line.split()) for line in out.splitlines() if line.strip()]
    return tree_sum(rows, roots)


def tree_sum(rows, roots) -> int:
    kids = {}
    for pid, ppid, _ in rows:
        kids.setdefault(ppid, []).append(pid)
    rss = {pid: r for pid, _, r in rows}
    seen, stack = set(), list(roots)
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        stack += kids.get(p, [])
    return sum(rss.get(p, 0) for p in seen)


def main(argv=None) -> int:
    p = common.parser(__doc__)
    p.add_argument("--step", choices=thresholds.MEMORY_STEPS, default="plan_a")
    args = p.parse_args(argv)
    common.require_mac()
    load = common.require_full_load(args)
    peak_kb, n = 0, 0
    while True:
        hb = common.load_status()
        if hb is None:
            break
        peak_kb = max(peak_kb, tree_rss_kb(hb["pids"]))
        n += 1
        time.sleep(1.0)
    if n < 60:
        raise common.Refused(f"only {n} samples: start this check together with the load session")
    v = thresholds.memory(round(peak_kb / 1e6, 3), args.step)
    return common.finish(v, args, load=load, note=f"{n} samples; Claude pool not built yet (M6)")


if __name__ == "__main__":
    sys.exit(main())
