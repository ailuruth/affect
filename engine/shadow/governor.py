"""The scaled safety net, revision 2: a multiplicative, attenuate-only gain governor per channel in front of the
unchanged shadow ledger (spec §1.6; research/foundations/design-scaled-safety-net.md §7.2, §7.7; Q35, D104).

Per channel k, with exponential window means ubar_W of his counterpart (started at the neutral input u0 = b_id, the
shadow's own input) and rbar_W of the raw partner-caused part r = y - ybar (started at 0), for every key
(W, kind, L) and memory tau:
  his signal   pi  = ubar_W(t - L)  (level)   or  ubar_W(t - L) - ubar_W(t - L - W)  (step)
  output       rho = rbar_W(t)      (level)   or  rbar_W(t) - rbar_W(t - W)          (step)
  sums         only ticks with t >= L + start_W W enter (no pre-session history); exponentially weighted covariance
               and variance WITH an intercept (West's incremental update), decay exp(-1/(tau f_g))
  beta         C / max(E, sigma0^2 W_t)
  evidence     batch sandwich over batches of batch_W W: n = (sum w_b E_b)^2 / sum w_b^2 E_b^2 independent batches,
               se^2 = (A11 - 2 beta A12 + beta^2 A22) / Ebar^2 n / (n - 1)
  latch        [n >= n_req and beta - t_{n-1}(z) se > kappa_g c_k] or [latched and beta > kappa_g c_k]
  gain         a_k(t) = min(a_k(t-1), kappa_g c_k / max over latched keys and memories of beta)  (ratchet)
  output       x_k = a_k r_k, the ledger's input.
Every output-side threshold is a multiple of the channel's own ceiling c_k; the absolute quantities are on his signal
(sigma0) or on time. On a zero-ceiling channel the target is 0, so a_k is 1 or 0. No rule names a situation, partner,
channel or time of day (D88). Nothing persists across sessions: reset() at session start.

Rates: window means are updated at the input rate f_s; the sums, batches, latches and the gain at the governor rate
f_g = 10 Hz (every f_s / f_g-th frame, starting with the first), a held between updates. Lags, batches, memories and
the start rule are in seconds, so they do not depend on f_s. At f_s = 10 Hz this is `Governor2` of
research/foundations/sims/scaled-safety-net/rev2_lib.py with the same floating-point operations in the same order,
so it is bit-identical to it (tests/test_governor.py). The three memories are stacked on a leading axis; every per-key
quantity is element-wise and combined only by max, so the stacking does not change a bit.
"""
from __future__ import annotations

import numpy as np

from engine.config.innate import ENTRIES


def _cfg() -> dict:
    v = lambda n: ENTRIES[n].value
    return dict(
        kappa_g=float(v("governor_kappa")),
        z=float(v("governor_z")),
        t_crit=bool(v("governor_t_test")),
        n_req=float(v("governor_n_req")),
        batch_W=float(v("governor_batch_W")),
        start_W=float(v("governor_start_W")),
        sigma0=float(v("governor_sigma0")),
        taus=tuple(float(t) for t in v("governor_taus_s")),
        sets=tuple((float(k["window_s"]), str(k["kind"]), float(k["lag_step_s"])) for k in v("governor_keys")["sets"]),
        max_lag_s=float(v("governor_keys")["max_lag_s"]),
        ratchet=bool(v("governor_ratchet")),
        rate_hz=float(v("governor_rate_hz")),
    )


GOVERNOR = _cfg()


def t_multiplier(z, df):
    """Student-t quantile at the one-sided level of the normal multiplier z with df degrees of freedom: the
    Cornish-Fisher expansion (Abramowitz-Stegun 26.7.5). Within a few % of the exact quantile for df >= 3 and below it
    for df < 3, where the n_req floor of 2 batches is the binding guard."""
    df = np.maximum(df, 1.0)
    g1 = (z ** 3 + z) / 4
    g2 = (5 * z ** 5 + 16 * z ** 3 + 3 * z) / 96
    g3 = (3 * z ** 7 + 19 * z ** 5 + 17 * z ** 3 - 15 * z) / 384
    g4 = (79 * z ** 9 + 776 * z ** 7 + 1482 * z ** 5 - 1920 * z ** 3 - 945 * z) / 92160
    return z + g1 / df + g2 / df ** 2 + g3 / df ** 3 + g4 / df ** 4


class Governor:
    """Streaming governor over n channels. `ceilings` c_k [n]; `u_neutral` the neutral input u0 [n] (b_id[:33] in the
    engine, never the session mean); `fs` the input frame rate (an integer multiple of the governor rate)."""

    def __init__(self, ceilings, fs: float, u_neutral, cfg: dict | None = None):
        self.p = p = dict(GOVERNOR if cfg is None else cfg)
        p.setdefault("rate_hz", GOVERNOR["rate_hz"])
        self.c = np.asarray(ceilings, dtype=np.float64)
        self.n = self.c.shape[0]
        self.fs = float(fs)
        self.fg = float(p["rate_hz"])
        m = self.fs / self.fg
        if m < 1 or abs(m - round(m)) > 1e-9:
            raise ValueError(f"input rate {fs} Hz is not an integer multiple of the governor rate {self.fg} Hz")
        self.every = int(round(m))
        fg = self.fg
        self.wins = sorted({w for w, _, _ in p["sets"]})
        self.Wf = {w: int(round(w * fg)) for w in self.wins}
        self.aW = {w: 1 - np.exp(-1 / (w * self.fs)) for w in self.wins}      # window means at the input rate
        self.H = int(p["max_lag_s"] * fg) + max(self.Wf.values()) + 1
        self.ds = np.array([np.exp(-1 / (tau * fg)) for tau in p["taus"]])
        self.sets = []
        for (w, kind, step) in p["sets"]:
            lags = np.arange(0, int(p["max_lag_s"] * fg) + 1, int(round(step * fg)))
            B = int(round(p["batch_W"] * w * fg))
            start = lags + int(round(p["start_W"] * w * fg))
            self.sets.append(dict(w=w, kind=kind, lags=lags, B=B, start=start,
                                  d=self.ds[:, None, None],
                                  dB=np.array([d ** B for d in self.ds])[:, None, None],
                                  d2B=np.array([d ** (2 * B) for d in self.ds])[:, None, None]))
        self.tgt = (p["kappa_g"] * self.c)[:, None]
        self.reset(u_neutral)

    # ------------------------------------------------------------------------------------------------ state
    def reset(self, u_neutral=None) -> None:
        """Session start: ring buffers of ubar_W at u0, of rbar_W at 0, every sum 0, a = 1."""
        if u_neutral is not None:
            self.u0 = np.array(u_neutral, dtype=np.float64).reshape(self.n)
        n, H, M = self.n, self.H, len(self.ds)
        self.uW = {w: self.u0.copy() for w in self.wins}
        self.rW = {w: np.zeros(n) for w in self.wins}
        self.uring = {w: np.repeat(self.u0[None, :], H, 0) for w in self.wins}
        self.rring = {w: np.zeros((H, n)) for w in self.wins}
        self.ptr = 0
        self.t = 0                      # governor ticks
        self.frame = 0                  # input frames
        for S in self.sets:
            K = len(S["lags"])
            z = lambda: np.zeros((M, n, K))
            S.update(Wt=np.zeros((M, 1, K)), mp=z(), mr=z(), C=z(), E=z(), bP=z(), bE=z(), A11=z(), A12=z(), A22=z(),
                     Eb=z(), latch=np.zeros((M, n, K), dtype=bool), beta=z(), se=z(), neff=z(), zz=z())
        self.a = np.ones(n)
        self.prev_a = np.ones(n)
        self.ever_latched = np.zeros(n, dtype=bool)     # some key of the channel has latched this session
        self.engaged = np.zeros(n, dtype=np.int64)      # frames with a < 1
        self.first = np.full(n, -1.0)                   # time (s) a first went below 1

    # ------------------------------------------------------------------------------------------------ frame
    def step(self, u, r) -> np.ndarray:
        """One input frame. u: his channels [n]; r: the raw partner-caused part [n]. Returns x = a * r."""
        u = np.asarray(u, dtype=np.float64)
        r = np.asarray(r, dtype=np.float64)
        for w in self.wins:
            self.uW[w] += self.aW[w] * (u - self.uW[w])
            self.rW[w] += self.aW[w] * (r - self.rW[w])
        self.prev_a = self.a
        if self.frame % self.every == 0:
            self._tick()
        if (self.first < 0).any():
            lowered = (self.a < 1.0) & (self.first < 0)
            self.first[lowered] = self.frame / self.fs
        self.engaged += self.a < 1.0
        self.frame += 1
        return self.a * r

    def _tick(self) -> None:
        p, H = self.p, self.H
        self.ptr = (self.ptr + 1) % H
        q = self.ptr
        for w in self.wins:
            self.uring[w][q] = self.uW[w]
            self.rring[w][q] = self.rW[w]
        tgt = self.tgt
        bmax = np.zeros(self.n)
        for S in self.sets:
            w, lags = S["w"], S["lags"]
            Wf = self.Wf[w]
            if S["kind"] == "level":
                pi = self.uring[w][(q - lags) % H].T
                rho = self.rW[w][:, None]
            else:
                pi = (self.uring[w][(q - lags) % H] - self.uring[w][(q - lags - Wf) % H]).T
                rho = (self.rW[w] - self.rring[w][(q - Wf) % H])[:, None]
            v = (self.t >= S["start"]).astype(float)
            batch_end = (self.t + 1) % S["B"] == 0
            d = S["d"]
            S["Wt"] = d * S["Wt"] + v
            inv = np.where(S["Wt"] > 0, v / np.maximum(S["Wt"], 1e-12), 0.0)
            dp = pi - S["mp"]
            S["mp"] += dp * inv
            dr = rho - S["mr"]
            S["mr"] += dr * inv
            inc_c = v * dp * (rho - S["mr"])
            inc_e = v * dp * (pi - S["mp"])
            S["C"] = d * S["C"] + inc_c
            S["E"] = d * S["E"] + inc_e
            S["bP"] += inc_c
            S["bE"] += inc_e
            if batch_end:
                S["A11"] = S["d2B"] * S["A11"] + S["bP"] ** 2
                S["A12"] = S["d2B"] * S["A12"] + S["bP"] * S["bE"]
                S["A22"] = S["d2B"] * S["A22"] + S["bE"] ** 2
                S["Eb"] = S["dB"] * S["Eb"] + S["bE"]
                S["bP"][:] = 0.0
                S["bE"][:] = 0.0
            Ef = np.maximum(S["E"], p["sigma0"] ** 2 * S["Wt"] + 1e-15)
            beta = S["C"] / Ef
            neff = S["Eb"] ** 2 / np.maximum(S["A22"], 1e-300)
            Ebf = np.maximum(S["Eb"], 1e-30)
            var = np.maximum(S["A11"] - 2 * beta * S["A12"] + beta * beta * S["A22"], 0) / (Ebf * Ebf)
            se = np.sqrt(var * neff / np.maximum(neff - 1.0, 1e-9))
            enough = neff >= p["n_req"]
            zz = t_multiplier(p["z"], neff - 1.0) if p["t_crit"] else np.full_like(neff, p["z"])
            S["latch"] = (enough & (beta - zz * se > tgt)) | (S["latch"] & (beta > tgt))
            S["beta"], S["se"], S["neff"], S["zz"] = beta, se, neff, zz
            bmax = np.maximum(bmax, np.max(np.where(S["latch"], beta, 0.0), axis=(0, 2)))
            self.ever_latched |= S["latch"].any(axis=(0, 2))
        target = np.clip(np.where(bmax > 0, tgt[:, 0] / np.where(bmax > 0, bmax, 1.0), 1.0), 0.0, 1.0)
        self.a = np.minimum(self.a, target) if p["ratchet"] else target
        self.t += 1

    # ------------------------------------------------------------------------------------------------ logging
    @property
    def beta(self) -> list:
        """Per key set: slopes [memories, n, keys]."""
        return [S["beta"] for S in self.sets]

    @property
    def se(self) -> list:
        return [S["se"] for S in self.sets]

    @property
    def neff(self) -> list:
        return [S["neff"] for S in self.sets]

    def latched_key(self) -> list:
        """Per channel: None, or (window s, kind, lag s, memory tau s, beta, se, n) of the latched key with the
        largest slope (the binding key), for the per-minute log and the asserts."""
        best = [None] * self.n
        top = np.zeros(self.n)
        for S in self.sets:
            b = np.where(S["latch"], S["beta"], -np.inf)
            for k in range(self.n):
                m, j = np.unravel_index(int(np.argmax(b[:, k, :])), b[:, k, :].shape)
                if np.isfinite(b[m, k, j]) and (best[k] is None or b[m, k, j] > top[k]):
                    top[k] = b[m, k, j]
                    best[k] = (S["w"], S["kind"], float(S["lags"][j] / self.fg), float(self.p["taus"][m]),
                               float(S["beta"][m, k, j]), float(S["se"][m, k, j]), float(S["neff"][m, k, j]))
        return best

    def any_latched(self) -> np.ndarray:
        """[n]: some key of the channel is latched now."""
        out = np.zeros(self.n, dtype=bool)
        for S in self.sets:
            out |= S["latch"].any(axis=(0, 2))
        return out


# ---------------------------------------------------------------------------------------------------- the net
NET_MODES = ("scaled_rev2_with_floor", "scaled_rev2", "ledger_only")


def evidence_floor(fs: float) -> float:
    """The ledger's evidence floor E0 at frame rate fs: `ledger_evidence_floor` is one minute of his window-mean
    movement at 0.03 counted at the ledger's 10-Hz reference rate (600 frames x 0.03^2 = 0.54); the ledger's E sums
    one term per frame, so at fs it is the same minute, E0 x fs / 10."""
    return ENTRIES["ledger_evidence_floor"].value * float(fs) / 10.0


def ledger_floor_for(fs: float, mode: str | None = None) -> float:
    """E0 of the ledger stage under the net `mode` (default: the operator switch)."""
    mode = net_mode() if mode is None else mode
    return evidence_floor(fs) if mode == "scaled_rev2_with_floor" else 0.0


def net_mode(switches: dict | None = None) -> str:
    from engine.config.operator import require
    mode = require("safety_net", switches=switches)["safety_net"]
    if mode not in NET_MODES:
        raise ValueError(f"safety_net = {mode!r}; expected one of {NET_MODES}")
    return mode


def build_net(ceilings, fs: float, u_neutral, mode: str | None = None, **ledger_kw):
    """The safety net's two stages per the operator switch `safety_net` (D104): (governor or None, ledger).
    'scaled_rev2_with_floor': Governor -> Ledger with the evidence floor (the answer to Q35);
    'scaled_rev2': Governor -> Ledger without it; 'ledger_only': the ledger of revision 9.2 alone (tests, lesions)."""
    from engine.shadow.ledger import Ledger
    mode = net_mode() if mode is None else mode
    if mode not in NET_MODES:
        raise ValueError(mode)
    gov = None if mode == "ledger_only" else Governor(ceilings, fs, u_neutral)
    ledger_kw.setdefault("evidence_floor", ledger_floor_for(fs, mode))
    return gov, Ledger(ceilings, fs, **ledger_kw)
