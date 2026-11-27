"""E3: coupling beyond surrogates (spec §5.4; evaluation.md E3): pooled slopes of the agent's channel on his at 2 s,
10 s and 1 min, against surrogate distributions (1,000 per test, observed against the 95th percentile).

Surrogate kinds (each replaces his series, person by person, keeping the agent's output and his words fixed):
  segment_shuffle   his series cut into 60-s segments, the segments permuted              (stored outputs only)
  data_slide        his series circularly shifted by >= 120 s                             (stored outputs only)
  partner_swap      another person's series (cropped or tiled to length)
  timing_resample   his 30-s segments each time-stretched by U(0.75, 1.25), re-joined and cropped
  month_swap        his series from a session >= 28 days away (only after >= 30 operator sessions)
segment_shuffle and data_slide are both required (spec §5.4): the battery refuses to run without them. The last
three keep words and turn order fixed; with `rerun` given (rerun(i, his_face) -> the agent's channel, the engine
re-driven with person i's words and the surrogate face) the agent's output is recomputed and its slope taken on
his original series (coupling through words alone survives, face coupling does not). Without `rerun` they are
computed on stored outputs.

`ys` is the conditioned output (F1's conditioned metric): the agent's rendered partner-caused part, rendered - ybar
= the ledger's x2, since the shadow's output ybar never sees his channels.

Two claims are scored from the same observed results: Bounded (observed pooled slope / c_k <= 1 and under the
surrogates' bound at every window, F1) and Present (fast partial coupling at lags < 1 s above every surrogate's
95th percentile, and gone under the G_k <- 0 lesion; eval/switches.py `echo_gain_zero_SL`).
"""
from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from eval import config as C
from eval.metrics import block_means
from eval.registry import Registry
from eval.results import score_record, write_json


class SurrogateRefused(Exception):
    pass


def segment_shuffle(u, fs, rng, seg_s=C.SEGMENT_S):
    n = max(1, int(round(seg_s * fs)))
    T = len(u)
    segs = [u[i:i + n] for i in range(0, T, n)]
    order = rng.permutation(len(segs))
    return np.concatenate([segs[j] for j in order])[:T]


def data_slide(u, fs, rng, min_s=C.SLIDE_MIN_S):
    T = len(u)
    lo = int(round(min_s * fs))
    if T <= 2 * lo:
        lo = T // 4
    return np.roll(u, int(rng.integers(lo, T - lo + 1)))


def timing_resample(u, fs, rng, seg_s=C.RESAMPLE_SEG_S, jitter=C.RESAMPLE_JITTER):
    T = len(u)
    n = max(2, int(round(seg_s * fs)))
    out = []
    for i in range(0, T, n):
        seg = u[i:i + n]
        m = max(2, int(round(len(seg) * rng.uniform(1 - jitter, 1 + jitter))))
        out.append(np.interp(np.linspace(0, len(seg) - 1, m), np.arange(len(seg)), seg))
    v = np.concatenate(out)
    return v[:T] if len(v) >= T else np.concatenate([v, v[:T - len(v)]])


def _fit_len(v, T):
    reps = int(np.ceil(T / len(v)))
    return np.tile(v, reps)[:T]


def partner_swap_index(i, n, rng):
    if n < 2:
        raise SurrogateRefused("partner-swap needs at least 2 people")
    j = int(rng.integers(0, n - 1))
    return j + (j >= i)


def month_swap_index(i, days, rng):
    if len(days) < C.MONTH_SWAP_MIN_SESSIONS:
        raise SurrogateRefused(f"month-swap needs >= {C.MONTH_SWAP_MIN_SESSIONS} sessions (has {len(days)})")
    cand = [j for j, d in enumerate(days) if abs(d - days[i]) >= C.MONTH_SWAP_MIN_DAYS]
    if not cand:
        raise SurrogateRefused(f"month-swap: no session >= {C.MONTH_SWAP_MIN_DAYS} days from session {i}")
    return cand[int(rng.integers(0, len(cand)))]


def _pooled_from_means(BU, BY):
    sxy = sxx = 0.0
    for bu, by in zip(BU, BY):
        m = min(bu.size, by.size)
        if m < 3:
            continue
        a, b = bu[:m] - bu[:m].mean(), by[:m] - by[:m].mean()
        sxy += float(a @ b)
        sxx += float(a @ a)
    return sxy / sxx if sxx > 0 else 0.0


class Battery:
    def __init__(self, fs, windows=C.WINDOWS_S, lags_s=(0.0,), n=C.SURROGATE_N, kinds=C.SURROGATE_KINDS, seed=0,
                 q=C.SURROGATE_QUANTILE):
        missing = [k for k in C.SURROGATES_REQUIRED if k not in kinds]
        if missing:
            raise SurrogateRefused(f"surrogates {missing} are required (spec §5.4)")
        bad = [k for k in kinds if k not in C.SURROGATE_KINDS]
        if bad:
            raise ValueError(f"unknown surrogate kinds {bad}")
        self.fs, self.windows, self.lags, self.n, self.kinds, self.seed, self.q = fs, tuple(windows), tuple(lags_s), \
            int(n), tuple(kinds), seed, q

    def _stat(self, us, ys):
        """max over lags of the pooled slope, per window"""
        out = []
        for W in self.windows:
            BU = [block_means(u, self.fs, W) for u in us]
            out.append(max(_pooled_from_means(BU, [block_means(y, self.fs, W, lg) for y in ys]) for lg in self.lags))
        return out

    def run(self, us, ys, days=None, rerun=None, n_rerun=None) -> dict:
        us = [np.asarray(u, float) for u in us]
        ys = [np.asarray(y, float) for y in ys]
        rng = np.random.default_rng(self.seed)
        obs = self._stat(us, ys)
        YM = {W: {lg: [block_means(y, self.fs, W, lg) for y in ys] for lg in self.lags} for W in self.windows}
        dist = {}
        for kind in self.kinds:
            n = self.n if (rerun is None or kind in C.SURROGATES_REQUIRED) else int(n_rerun or self.n)
            vals = np.zeros((n, len(self.windows)))
            for s in range(n):
                su = [self._surrogate(kind, i, us, days, rng) for i in range(len(us))]
                if rerun is not None and kind not in C.SURROGATES_REQUIRED:
                    vals[s] = self._stat(us, [rerun(i, su[i]) for i in range(len(us))])
                    continue
                for wi, W in enumerate(self.windows):
                    BU = [block_means(u, self.fs, W) for u in su]
                    vals[s, wi] = max(_pooled_from_means(BU, YM[W][lg]) for lg in self.lags)
            dist[kind] = vals
        res = {"windows": list(self.windows), "lags_s": list(self.lags), "observed": obs, "kinds": list(self.kinds),
               "n": {k: int(v.shape[0]) for k, v in dist.items()}}
        for kind, v in dist.items():
            for wi, W in enumerate(self.windows):
                key = f"{kind}.W{W:g}"
                res[f"{key}.dist"] = v[:, wi].tolist()
                res[f"{key}.q95"] = float(np.quantile(v[:, wi], self.q))
        for wi, W in enumerate(self.windows):
            res[f"observed.W{W:g}"] = obs[wi]
            res[f"surrogate_q95_max.W{W:g}"] = max(res[f"{k}.W{W:g}.q95"] for k in self.kinds)
            res[f"observed_minus_q95.W{W:g}"] = obs[wi] - res[f"surrogate_q95_max.W{W:g}"]
        return res

    def _surrogate(self, kind, i, us, days, rng):
        u = us[i]
        if kind == "segment_shuffle":
            return segment_shuffle(u, self.fs, rng)
        if kind == "data_slide":
            return data_slide(u, self.fs, rng)
        if kind == "timing_resample":
            return timing_resample(u, self.fs, rng)
        if kind == "partner_swap":
            return _fit_len(us[partner_swap_index(i, len(us), rng)], len(u))
        if kind == "month_swap":
            if days is None:
                raise SurrogateRefused("month-swap needs each session's day")
            return _fit_len(us[month_swap_index(i, days, rng)], len(u))
        raise ValueError(kind)


def run_surrogates(registry: Registry, test_id: str, us, ys, fs, c_k: float, out_dir, synthetic: bool,
                   extra: dict | None = None, **kw) -> dict:
    """Score one channel's pooled slopes (observed / c_k as `observed_c.W*`) against its surrogate distributions."""
    days = kw.pop("days", None)
    rerun = kw.pop("rerun", None)
    n_rerun = kw.pop("n_rerun", None)
    tok = registry.start_run(test_id)
    t0 = time.perf_counter()
    res = Battery(fs, **kw).run(us, ys, days=days, rerun=rerun, n_rerun=n_rerun)
    for W in res["windows"]:
        res[f"observed_c.W{W:g}"] = res[f"observed.W{W:g}"] / c_k if c_k > 0 else res[f"observed.W{W:g}"]
    res.update(extra or {})
    sc = registry.score(tok, res)
    doc = score_record(sc, {"harness": "surrogates", "c_k": c_k, "wall_s": time.perf_counter() - t0})
    write_json(Path(out_dir) / f"{test_id}.json", doc, synthetic)
    return doc
