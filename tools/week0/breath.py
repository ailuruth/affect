"""Check 6: breathing rate error and hold detection (design §3.17 item 15), silent and while talking.

Protocol (the prompts are printed; the microphone records each part, kept in ~/.affect-week0 or deleted with
--delete-recordings):
  silent:  paced 6 /min for 2 min; paced 12 /min for 2 min; 10 breath holds (15 s each, 20 s normal breathing
           between); rest 3 min; rest 3 min again.
  talking: paced 6 /min and 12 /min for 2 min each while reading tools/week0/reading.txt aloud, breathing in at
           the cues.
Scored per 30-s window: rate error = the estimator's median rate in the window minus the paced rate. A hold is
detected if the estimator flags a hold during it. Test-retest r: Pearson r of the window rates of rest 1 and rest 2,
paired in order (the spec does not define the pairing further; for the spec owner).

The estimator is the engine's own breathing feature (engine/boundary/breath.py, M2): `estimate(audio, rate)` ->
{"t": 10-Hz times, "rate_per_min": [...], "hold": [...]}. Until it exists this check refuses. Run:
    uv run python -m tools.week0.breath [--delete-recordings]
"""
from __future__ import annotations

import sys
import threading
import time

from tools.week0 import asr_common, common, measure, thresholds

RATE = 16000
WINDOW_S = thresholds.TH["breath"]["window_s"]
SILENT_PACED = ((6.0, 120.0), (12.0, 120.0))
HOLDS, HOLD_S, BETWEEN_S = 10, 15.0, 20.0
REST_S = 180.0


def _cues(per_min: float, seconds: float, stop: threading.Event) -> None:
    period = 60.0 / per_min
    t0 = time.time()
    while not stop.is_set() and time.time() - t0 < seconds:
        phase = ((time.time() - t0) % period) / period
        print("\r  " + ("IN " if phase < 0.5 else "OUT") + f"  {seconds - (time.time() - t0):5.0f} s left ", end="")
        time.sleep(0.1)
    print()


def _hold_cues(seconds: float, stop: threading.Event) -> None:
    t0 = time.time()
    while not stop.is_set() and time.time() - t0 < seconds:
        k = (time.time() - t0) % (HOLD_S + BETWEEN_S)
        print("\r  " + ("HOLD   " if k >= BETWEEN_S else "breathe") + f"  {seconds - (time.time() - t0):5.0f} s left ", end="")
        time.sleep(0.1)
    print()


def _part(label: str, seconds: float, per_min: float | None = None, holds: bool = False):
    input(f"\n{label} ({seconds:.0f} s). Press Return to start.")
    stop = threading.Event()
    th = (threading.Thread(target=_cues, args=(per_min, seconds, stop)) if per_min else
          threading.Thread(target=_hold_cues, args=(seconds, stop)) if holds else None)
    if th:
        th.start()
    x = asr_common.record(seconds, RATE)
    stop.set()
    if th:
        th.join()
    asr_common.save_wav(common.local_path(f"breath_{label.split()[0]}_{int(time.time())}.wav"), x, RATE)
    return x


def _windows(est, seconds: float):
    """Median estimated rate per WINDOW_S window."""
    out = []
    t, r = est["t"], est["rate_per_min"]
    for w0 in range(0, int(seconds - WINDOW_S) + 1, int(WINDOW_S)):
        vals = sorted(rr for tt, rr in zip(t, r) if w0 <= tt < w0 + WINDOW_S)
        if vals:
            out.append(vals[len(vals) // 2])
    return out


def main(argv=None) -> int:
    p = common.parser(__doc__)
    p.add_argument("--delete-recordings", action="store_true")
    args = p.parse_args(argv)
    common.require_approval("conversation_language", "hub_offline_after_download")
    common.require_mac()
    load = common.require_full_load(args)
    try:
        from engine.boundary import breath as estimator           # M2
    except ImportError:
        raise common.Refused("the breathing feature engine/boundary/breath.py (M2) is not built yet") from None
    est = lambda x: estimator.estimate(x, RATE)
    silent_err, talk_err, holds_hit = [], [], 0
    for per_min, secs in SILENT_PACED:
        silent_err += [w - per_min for w in _windows(est(_part(f"silent paced {per_min:.0f}/min", secs, per_min)), secs)]
    hold_x = _part("holds: hold your breath at HOLD, 10 times", HOLDS * (HOLD_S + BETWEEN_S), holds=True)
    e = est(hold_x)
    for i in range(HOLDS):
        a = BETWEEN_S + i * (HOLD_S + BETWEEN_S)
        holds_hit += any(h for tt, h in zip(e["t"], e["hold"]) if a <= tt < a + HOLD_S)
    rest = [_windows(est(_part(f"rest {i + 1}: breathe normally, silent", REST_S)), REST_S) for i in range(2)]
    for per_min, secs in SILENT_PACED:
        talk_err += [w - per_min for w in _windows(est(_part(f"talking paced {per_min:.0f}/min: read aloud", secs, per_min)), secs)]
    n = min(len(rest[0]), len(rest[1]))
    r = round(measure.pearson(rest[0][:n], rest[1][:n]), 4)
    v = thresholds.breath(silent_err, holds_hit, HOLDS, r, talk_err)
    rc = common.finish(v, args, load=load, note=f"{len(silent_err)} silent and {len(talk_err)} talking windows")
    if args.delete_recordings:
        for f in common.WEEK0_DIR.glob("breath_*.wav"):
            f.unlink()
        print("local recordings deleted")
    return rc


if __name__ == "__main__":
    sys.exit(main())
