"""The scripted 10-minute full-load session for the M1 timing checks (spec §6: "full load" = every process of §2.1
running, with a scripted 10-min session).

What runs today: the M4 offline core (factual and shadow runs, ledger, assertions) stepped in real time at 30 Hz on
a scripted synthetic partner with scripted utterances (`core`), in its own process; with `--with-models` (after Q34
items 4, 5 and 10) also the two recognisers looping over a synthetic noise buffer (`asr_stream`, `asr_utterance`).
The other §2.1 processes (`voice`, `tts`, `omega`, the page) are added here as they are built (M2, M5, M6); each
check records the components that were running, so a number measured under a partial load says so.

Start it in its own Terminal window, then run the checks in another:
    uv run python -m tools.week0.load_session [--seconds 600] [--with-models]
It stops by itself after the session (or on Ctrl-C) and stops its worker processes.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time

from tools.week0 import common


def scripted_core(seconds: float, fs: float = 30.0) -> None:
    """The engine core in real time: one scripted partner (slow level changes and bursts), one utterance every
    8 s and one own reply every 13 s."""
    import numpy as np
    from engine.routes.learned_t import Learned, randomise_for_trace
    from engine.shadow.shadow import Frame, ShadowPair
    from engine.state.body import Session
    from engine.state.types import Utterance, heard_at_playback
    r = np.random.default_rng(0)
    N = 33
    pair = ShadowPair(Session(K=0.6), np.full(N + 3, 0.1), randomise_for_trace(Learned(), 5), fs=fs)
    t0 = time.perf_counter()
    n = 0
    while True:
        t = n / fs
        if t >= seconds:
            return
        u = np.clip(0.1 + 0.05 * np.sin(2 * np.pi * 0.02 * t + np.arange(N)) + 0.02 * r.standard_normal(N), -1, 1)
        if n % int(8 * fs) == int(4 * fs):
            pair.push_utterance(Utterance("him", (), "some scripted words", t, "some scripted words"))
        if n % int(13 * fs) == int(6 * fs):
            pair.push_own_heard(heard_at_playback(["a", "scripted", "reply"], [t - 0.6, t - 0.3, t], "statement", t - 0.9))
        pair.step(Frame.from_u(t, u))
        n += 1
        delay = t0 + n / fs - time.perf_counter()
        if delay > 0:
            time.sleep(delay)


def asr_loop(kind: str, seconds: float) -> None:
    """A recogniser kept busy on a looped synthetic noise buffer (no recording)."""
    import numpy as np
    from tools.week0 import asr_common
    audio = (0.01 * np.random.default_rng(1).standard_normal(16000 * 10)).astype(np.float32)
    t_end = time.time() + seconds
    rec = asr_common.utterance_recogniser() if kind == "asr_utterance" else asr_common.stream_recogniser()
    while time.time() < t_end:
        rec(audio)


def main(argv=None) -> int:
    p = common.parser(__doc__)
    p.add_argument("--seconds", type=float, default=600.0)
    p.add_argument("--with-models", action="store_true", help="also load the two recognisers (Q34 items 4, 5, 10)")
    p.add_argument("--worker", choices=("core", "asr_stream", "asr_utterance"), help=argparse_hidden())
    args = p.parse_args(argv)
    if args.worker == "core":
        scripted_core(args.seconds)
        return 0
    if args.worker:
        asr_loop(args.worker, args.seconds)
        return 0
    components = ["core"]
    if args.with_models:
        common.require_approval("downloads_approved", "conversation_language", "hub_offline_after_download")
        components += ["asr_stream", "asr_utterance"]
    env = dict(os.environ, HF_HUB_OFFLINE="1", HF_HUB_DISABLE_TELEMETRY="1")
    procs = [subprocess.Popen([sys.executable, "-m", "tools.week0.load_session", "--worker", c,
                               "--seconds", str(args.seconds)], cwd=common.ROOT, env=env) for c in components]
    stop = {"now": False}
    signal.signal(signal.SIGTERM, lambda *a: stop.update(now=True))
    t_end = time.time() + args.seconds
    print(f"load session: {'+'.join(components)} for {args.seconds:.0f} s (Ctrl-C to stop)")
    try:
        while time.time() < t_end and not stop["now"] and all(pr.poll() is None for pr in procs):
            hb = {"t": time.time(), "components": components, "pids": [os.getpid()] + [pr.pid for pr in procs],
                  "ends": t_end}
            common.local_path(common.HEARTBEAT.name).write_text(json.dumps(hb))
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        for pr in procs:
            if pr.poll() is None:
                pr.terminate()
        for pr in procs:
            try:
                pr.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pr.kill()
        try:
            common.HEARTBEAT.unlink()
        except OSError:
            pass
    bad = [pr.returncode for pr in procs if pr.returncode not in (0, -signal.SIGTERM)]
    print("load session ended" + (f" (a worker exited with {bad})" if bad else ""))
    return 1 if bad else 0


def argparse_hidden():
    import argparse
    return argparse.SUPPRESS


if __name__ == "__main__":
    sys.exit(main())
