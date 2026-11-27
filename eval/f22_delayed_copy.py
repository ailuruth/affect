"""F22 (spec §5.1, §5.5): an injected uncounted route copying his channel with delay 10-300 s must not render above
1.0 c_k by the block-mean metric at 2-s, 10-s or 1-min windows (worst over lags 0-300 s); and the ledger must change
<= 1 % of frames of the counted routes alone.

Ledger only (§5.5 step 1): the copy is injected after assembly, so the engine's routes are computed once per person
(their partner-caused part r = y - ybar, stored) and only the ledger and the metric are re-run.
Batched (step 2): one ledger instance carries every delay of a channel at once (each delay is one ledger "channel"
with the same ceiling c_k), so one frame step updates (delays x 97 keys) in numpy. The copy is the sims' gain-1
uncounted route: the onset lobe (x_d - lp4 x_d)+ plus the 60-s low-pass of x_d, x_d his channel delayed by L.

Data: recorded partners only (Seamless test people for LP, CR, BI, BO, LD, JO; his M2 recordings for the other 14
capped channels; live monitor at M7). None is in this session: here it runs on synthetic stand-ins as a harness test
(`make eval-dry`), never as F22. `python -m eval.f22_delayed_copy --pilot` times the batched ledger and prints the
§5.5 plan for the full run.
"""
from __future__ import annotations

import argparse
import sys
import time

import numpy as np

from eval import config as C
from eval import planner
from eval.metrics import worst_block_slope
from eval.switches import ledger_for
from eval.synthetic import lp


def delay(x, n):
    n = int(n)
    return x.copy() if n <= 0 else np.concatenate([np.full(n, x[0]), x[:-n]])


def copy_of(u, delay_s: float, fs: float) -> np.ndarray:
    xd = delay(np.asarray(u, float), round(delay_s * fs))
    onset = np.maximum(xd - lp(xd, 4.0, fs), 0.0)
    low = lp(xd, C.F22_COPY_LP_S, fs)
    return onset + low - low.mean()


def ledger_only(u, c_k: float, fs: float, delays=C.F22_DELAYS_S, r_routes=None, lesion=None,
                max_lag_s: float = C.F22_MAX_LAG_S, lag_step_s: float = 1.0, windows=C.WINDOWS_S) -> dict:
    """One channel of one person: worst slope / c_k per (window, delay) of the rendered partner-caused part with the
    copy (rendered - ybar = x2, the conditioned metric: the shadow's output ybar never sees his channel), and the
    fraction of frames the ledger changes on the counted routes alone (r_routes: the stored partner-caused part)."""
    u = np.asarray(u, float)
    T = u.shape[0]
    r0 = np.zeros(T) if r_routes is None else np.asarray(r_routes, float)
    n = len(delays)
    X = r0[:, None] + np.stack([copy_of(u, d, fs) for d in delays], 1)
    led = ledger_for(lesion, fs, np.full(n + 1, c_k))
    O = np.zeros((T, n + 1))
    for t in range(T):
        O[t] = led.step(np.full(n + 1, u[t]), np.concatenate([X[t], r0[t:t + 1]]))
    rendered = O[:, :n]                               # the conditioned metric: rendered - ybar = x2
    lags = np.arange(0.0, max_lag_s + 1e-9, lag_step_s)
    ws = worst_block_slope(np.repeat(u[:, None], n, 1), rendered, fs, lags, windows)
    changed = float(np.mean(np.abs(O[:, n] - r0) > 1e-12))
    return {"worst_c": ws / c_k if c_k > 0 else ws, "frames_changed_counted": changed, "delays": list(delays),
            "windows": list(windows)}


def run_people(people, c_k: float, fs: float, **kw) -> dict:
    """people: list of dicts with u (and optionally r_routes) for one channel. Worst over people."""
    res = [ledger_only(p["u"], c_k, fs, r_routes=p.get("r_routes"), **kw) for p in people]
    worst = np.fmax.reduce(np.stack([r["worst_c"] for r in res]), 0)
    return {"worst_c": float(np.fmax.reduce(worst, axis=None)), "worst_c_by_window_delay": worst.tolist(),
            "frames_changed_counted": max(r["frames_changed_counted"] for r in res), "people": len(people),
            "delays": res[0]["delays"], "windows": res[0]["windows"]}


def pilot_cost(fs: float = 30.0, seconds: float = 60.0, batches=(12, 48)) -> dict:
    """Per-frame cost of the batched ledger step at two batch sizes (people x delays), for f22_plan."""
    from engine.shadow.ledger import Ledger
    out = {}
    for b in batches:
        led = Ledger(np.full(b, 0.1), fs)
        r = np.random.default_rng(0)
        U = r.uniform(0, 1, (int(seconds * fs), b))
        t0 = time.perf_counter()
        for t in range(U.shape[0]):
            led.step(U[t], 0.1 * U[t])
        out[b] = (time.perf_counter() - t0) / U.shape[0]
    return out


def metric_cost(fs: float = 30.0, seconds: float = 400.0, series: int = 12) -> float:
    """Seconds of the block-mean metric (lags 0-300 s in 1-s steps, 3 windows) per frame per series."""
    r = np.random.default_rng(0)
    U = r.uniform(0, 1, (int(seconds * fs), series))
    t0 = time.perf_counter()
    worst_block_slope(U, 0.1 * U, fs, np.arange(0.0, C.F22_MAX_LAG_S + 1e-9, 1.0), C.WINDOWS_S)
    return (time.perf_counter() - t0) / (U.shape[0] * series)


def plan_full(fs: float = 30.0, seconds: float = 60.0) -> planner.Plan:
    """The §5.5 plan from two pilots: the batched ledger step (cost per frame at two batch sizes, extrapolated
    linearly to 50 people x 12 delays) plus the block-mean metric (cost per frame and series)."""
    cost = pilot_cost(fs, seconds)
    (b1, c1), (b2, c2) = sorted(cost.items())
    slope = max(0.0, (c2 - c1) / (b2 - b1))
    m = metric_cost(fs)
    scale = lambda b: (c1 + slope * (b - b1) + m * b) / c1
    p = planner.f22_plan(c1, fs=fs, batch_scale=scale)
    p.notes.insert(0, f"pilot: ledger {c1 * 1e3:.3f} ms/frame at batch {b1}, {c2 * 1e3:.3f} ms/frame at batch {b2}; "
                      f"metric {m * 1e6:.2f} us per frame and series")
    return p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pilot", action="store_true", help="time the batched ledger; print the §5.5 plan")
    ap.add_argument("--fs", type=float, default=30.0)
    a = ap.parse_args(argv)
    if a.pilot:
        p = plan_full(a.fs)
        for x in p.notes:
            print(x)
        for i, h in enumerate(p.hours):
            print(f"sitting {i + 1}: {h:.2f} h")
        print(f"total {p.total_h:.2f} h over {len(p.sittings)} sitting(s); no sitting above {p.limit_h} h")
        return 0
    print("F22 runs on recorded partners only (Seamless test people, his M2 recordings); none is in this session. "
          "Use --pilot for the plan, or `make eval-dry` for the synthetic harness test.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
