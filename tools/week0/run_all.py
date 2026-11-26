"""`make week0`: the M1 checks in order, on the operator's Mac (research/build/handoff.md step 7).

1. env_check, then download_models (refuses until Q34 item 4).
2. Starts the load session (15 min) and, beside it, the memory check (which samples until the load session ends).
3. Under that load, in order: fast_tick, slow_tick, tracker, clock, asr_stream, asr_utterance, breath (these prompt
   you where they need you; each refuses, and the run goes on, until its approvals are recorded).
4. Stops the load session; then sandbox_check (10 min, its own sandboxed core) and the five Claude checks (refuse
   until `claude_test_calls_m1`).
5. report: the summary in research/build/week0.md.
The echo rig (check 2) is analysed separately from its video: `python -m tools.week0.echo_rig VIDEO ...`.
`--only a,b` runs only the named checks (the load session is started if any of them needs it).
"""
from __future__ import annotations

import subprocess
import sys
import time

from tools.week0 import common

BEFORE = ("env_check", "download_models")
UNDER_LOAD = ("fast_tick", "slow_tick", "tracker", "clock", "asr_stream", "asr_utterance", "breath")
AFTER = ("sandbox_check", "claude_checks resume", "claude_checks thinking", "claude_checks latency",
         "claude_checks compaction", "claude_checks tokens")
LOAD_S = 900


def _run(step: str) -> int:
    print(f"\n=== {step} ===", flush=True)
    mod, *rest = step.split()
    return subprocess.call([sys.executable, "-m", f"tools.week0.{mod}", *rest], cwd=common.ROOT)


def main(argv=None) -> int:
    p = common.parser(__doc__)
    p.add_argument("--only", help="comma-separated check names")
    args = p.parse_args(argv)
    only = set(args.only.split(",")) if args.only else None
    pick = lambda steps: [s for s in steps if only is None or s.split()[0] in only or s in only]
    results = {}
    for s in pick(BEFORE):
        results[s] = _run(s)
    under = pick(UNDER_LOAD)
    want_memory = only is None or "memory" in only
    if under or want_memory:
        load = subprocess.Popen([sys.executable, "-m", "tools.week0.load_session", "--seconds", str(LOAD_S)], cwd=common.ROOT)
        mem = None
        try:
            for _ in range(30):
                if common.load_status():
                    break
                time.sleep(1.0)
            if want_memory:
                mem = subprocess.Popen([sys.executable, "-m", "tools.week0.memory"], cwd=common.ROOT)
            for s in under:
                results[s] = _run(s)
        finally:
            if load.poll() is None:
                load.terminate()
            load.wait(timeout=30)
            if mem is not None:
                results["memory"] = mem.wait(timeout=60)
    for s in pick(AFTER):
        results[s] = _run(s)
    print("\n=== summary ===")
    for s, rc in results.items():
        print(f"  {s}: " + {0: "measured", 1: "measured (fail)", 2: "refused (see its message)"}.get(rc, f"exit {rc}"))
    return _run("report")


if __name__ == "__main__":
    sys.exit(main())
