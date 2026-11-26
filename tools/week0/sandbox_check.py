"""Check 10 (A16): network connections from sandboxed processes over 10 minutes.

Starts the engine core (the load session's `core` worker) under `sandbox-exec -f engine/config/sandbox.sb`, with the
hub offline, and for 10 minutes: (a) lists its sockets with `lsof` every 5 s and counts each distinct connection
whose remote end is not loopback; (b) at the start and every minute, a sandboxed probe tries to open a connection to
a public address (1.1.1.1:443) and must fail. Count = distinct non-loopback connections + successful probes; any is a
fail. Without sandbox-exec, the spec's fallback (a pf anchor) is an Ask: reported. Run:
    uv run python -m tools.week0.sandbox_check [--minutes 10]
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time

from tools.week0 import common, thresholds

PROFILE = common.ROOT / "engine" / "config" / "sandbox.sb"
PROBE = ("import socket,sys\n"
         "s=socket.socket(); s.settimeout(3)\n"
         "try:\n s.connect(('1.1.1.1',443)); print('CONNECTED')\n"
         "except OSError: print('BLOCKED')\n")
LOOPBACK = ("127.", "[::1]", "::1", "localhost")


def non_local(lsof_out: str) -> set:
    """Distinct remote endpoints of TCP/UDP sockets in `lsof -nP -i` output that are not loopback."""
    out = set()
    for line in lsof_out.splitlines()[1:]:
        name = line.split()[-1] if line.split() else ""
        if line.rstrip().endswith(")"):                  # "... TCP a->b (ESTABLISHED)"
            name = line.split()[-2]
        if "->" in name:
            remote = name.split("->", 1)[1]
            if not remote.startswith(LOOPBACK):
                out.add(remote)
    return out


def main(argv=None) -> int:
    p = common.parser(__doc__)
    p.add_argument("--minutes", type=float, default=thresholds.TH["sandbox_minutes"])
    args = p.parse_args(argv)
    common.require_approval("hub_offline_after_download")
    common.require_mac()
    sx = shutil.which("sandbox-exec")
    if sx is None:                                       # fallback of spec §7.5: a pf anchor, an Ask
        return common.finish(thresholds.sandbox(0, sandbox_available=False), args, load="-")
    env = dict(os.environ, HF_HUB_OFFLINE="1", HF_HUB_DISABLE_TELEMETRY="1")
    secs = 60.0 * args.minutes
    core = subprocess.Popen([sx, "-f", str(PROFILE), sys.executable, "-m", "tools.week0.load_session", "--worker",
                             "core", "--seconds", str(secs)], cwd=common.ROOT, env=env)
    seen, probes_ok, probes = set(), 0, 0
    t0, next_probe = time.time(), 0.0
    try:
        while core.poll() is None and time.time() - t0 < secs + 30:
            out = subprocess.run(["lsof", "-nP", "-i", "-a", "-p", str(core.pid)], capture_output=True, text=True).stdout
            seen |= non_local(out)
            if time.time() - t0 >= next_probe:
                r = subprocess.run([sx, "-f", str(PROFILE), sys.executable, "-c", PROBE], capture_output=True,
                                   text=True, timeout=30)
                probes += 1
                probes_ok += "CONNECTED" in r.stdout
                next_probe += 60.0
            time.sleep(5.0)
    finally:
        if core.poll() is None:
            core.terminate()
            core.wait(timeout=10)
    v = thresholds.sandbox(len(seen) + probes_ok)
    return common.finish(v, args, load="core under sandbox-exec",
                         note=f"{probes} probes, {probes_ok} connected; {len(seen)} non-loopback sockets")


if __name__ == "__main__":
    sys.exit(main())
