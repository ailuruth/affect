"""Revision 2 of the scaled gain governor (design-scaled-safety-net.md, "Revision 2"): reference implementation.

Synthetic-signal check of the mathematics only; not evidence about people or behaviour. numpy only.
Reuses check.py's definitions verbatim (signals, the block-mean metric and the current Ledger), as critique_check.py
does, and adds:
  Governor2      the revised governor (level keys with an intercept, batch-sandwich evidence, two memories, ratchet)
  partners_fast  check.py's partner recipe with the same RNG call order, low-passes batched (identical signals)
  engine_baseline  an engine-like neutral input b_id: the 6-session exponential average of earlier session means of
                 the same synthetic partner (engine/config/innate.py cone_baseline_tau_sessions = 6), not today's mean
  run2           governor -> ledger (unchanged, or with an evidence floor E0 for the F1 study)
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "check.py")).read()
_src = _src[:_src.index("DELAYS = (10, 20, 40")]          # definitions only
_argv = sys.argv
sys.argv = ["check.py"]                                    # 1-h sessions for the definitions' T
ns = {"__name__": "check_defs"}
exec(compile(_src, "check.py", "exec"), ns)
sys.argv = _argv
FS = ns["FS"]
lp, delay, wbs, Ledger = ns["lp"], ns["delay"], ns["worst_block_slope"], ns["Ledger"]
level_blocks, bursts = ns["level_blocks"], ns["bursts"]
CEIL, GAIN, SIGNED, CODES = ns["CEIL"], ns["GAIN"], ns["SIGNED"], ns["CODES"]
CAPPED = np.where(CEIL > 0)[0]


# ---------------------------------------------------------------- signals
def partners_fast(n, seed=None, T=None, mean_lens=None, signed=None, rng=None):
    """check.py's partners(): the same RNG call order, so the same signals; the 0.5-s low-pass is applied once to all
    columns. mean_lens[k]: level-block mean length (default 300 s for even k, 30 s for odd k)."""
    r = rng if rng is not None else np.random.default_rng(seed)
    M = np.zeros((T, n)); B = np.zeros((T, n)); Z = np.zeros((T, n))
    for k in range(n):
        ml = mean_lens[k] if mean_lens is not None else (300.0 if k % 2 == 0 else 30.0)
        M[:, k] = level_blocks(T, ml, r)
        B[:, k] = bursts(0.5 + 3 * M[:, k], T, r)
        Z[:, k] = r.normal(size=T)
    U = np.clip(.15 + .25 * M + .35 * lp(B, 0.5) + .02 * Z, 0, 1)
    if signed is not None:
        U = U - 0.4 * np.asarray(signed, float)[None, :]
    return U


def engine_baseline(n, seed, mean_lens=None, signed=None, sessions=12, T_prev=None):
    """b_id as the engine latches it: an exponential average (time constant 6 sessions) of his earlier session means,
    started at the first session's mean. The earlier sessions are fresh draws of the same recipe (same block lengths);
    only their means are used. Not today's mean, so the neutral input differs from his level today."""
    T_prev = T_prev or int(1800 * FS)
    r = np.random.default_rng(10_000 + seed)
    a = 1 - np.exp(-1 / 6.0); b = None
    for s in range(sessions):
        m = partners_fast(n, T=T_prev, mean_lens=mean_lens, signed=signed, rng=r).mean(0)
        b = m if b is None else b + a * (m - b)
    return b


# ---------------------------------------------------------------- the revised governor
GOV2 = dict(
    kappa_g=0.60,        # target, fraction of c_k (ceiling)
    z=3.0,               # confidence multiplier
    n_req=4.0,           # evidence: effective number of independent batches before a key may engage
    sigma0=0.01,         # floor on his level SD (his units), as revision 1
    taus=(1800.0, 300.0),  # two memories: the ledger's budget time and a short one; latches combine by max slope
    # key sets: (window W s, lag step s); level keys (window means, intercept), lags 0..300 s
    sets=((10.0, 5.0), (60.0, 10.0)),
    batch_min_s=60.0,    # batch length for the sandwich = max(2 W, batch_min_s)
    max_lag_s=300.0,
    ratchet=True,        # a_k never rises within a session once lowered
)


class Governor2:
    """Per channel k, key (W, L) and memory tau:
      his level   pi(t)  = ubar_W(t - L)   (W-window mean, started at the neutral input u0: his history before the session)
      output      rho(t) = rbar_W(t)       (the same for the RAW partner-caused part r, started at 0)
      beta_hat    exponentially weighted (decay exp(-1/(tau fs))) covariance / variance WITH an intercept (West's
                  incremental update: no lagging centre), floor sigma0^2 on the variance
      se          batch sandwich: increments summed over batches of B = max(2W, 60 s) frames, se^2 =
                  sum_b w_b^2 (P_b - beta E_b)^2 / (sum_b w_b E_b)^2 * n/(n-1), n = effective number of batches
                  = (sum w_b E_b)^2 / sum w_b^2 E_b^2 (a single start-of-session step counts as ONE batch)
      engage      n >= n_req and beta - z se > kappa_g c_k; release when beta <= kappa_g c_k
      target      kappa_g c_k / (max over engaged keys and memories of beta); a_k = min(a_k(t-1), target)  (ratchet)
    Every output-side threshold is a multiple of c_k; absolute quantities are on his signal (sigma0) or on time."""

    def __init__(self, c, u0, p=GOV2):
        self.c = np.asarray(c, float); n = len(self.c); self.n = n; self.p = p
        self.u0 = np.asarray(u0, float)
        self.wins = [w for w, _ in p["sets"]]
        self.Wf = [int(round(w * FS)) for w in self.wins]
        self.H = int(p["max_lag_s"] * FS) + 1
        self.lags = [np.arange(0, int(p["max_lag_s"] * FS) + 1, int(round(st * FS))) for _, st in p["sets"]]
        self.aW = np.array([1 - np.exp(-1 / (w * FS)) for w in self.wins])
        self.B = [int(max(2 * w, p["batch_min_s"]) * FS) for w in self.wins]
        self.ds = [np.exp(-1 / (tau * FS)) for tau in p["taus"]]
        self.uW = np.repeat(self.u0[None, :], len(self.wins), 0); self.rW = np.zeros((len(self.wins), n))
        self.ring = np.repeat(self.uW[:, None, :], self.H, 1)      # (wins, H, n)
        self.ptr = 0; self.t = 0
        self.st = []   # stats per (set, memory)
        for i, l in enumerate(self.lags):
            for m, d in enumerate(self.ds):
                K = len(l); z = lambda: np.zeros((n, K))
                self.st.append(dict(i=i, d=d, dB=d ** self.B[i], d2B=d ** (2 * self.B[i]), Wt=0.0, mp=z(), mr=z(),
                                    C=z(), E=z(), bP=z(), bE=z(), A11=z(), A12=z(), A22=z(), Eb=z(),
                                    latch=np.zeros((n, K), bool)))
        self.a = np.ones(n); self.engaged = np.zeros(n); self.first = np.full(n, -1.0)

    def step(self, u, r):
        p = self.p
        self.uW += self.aW[:, None] * (u - self.uW); self.rW += self.aW[:, None] * (r - self.rW)
        self.ptr = (self.ptr + 1) % self.H; self.ring[:, self.ptr] = self.uW
        tgt = p["kappa_g"] * self.c
        bmax = np.zeros(self.n)
        pis = [self.ring[i, (self.ptr - l) % self.H].T for i, l in enumerate(self.lags)]
        for s in self.st:
            i, d = s["i"], s["d"]
            pi = pis[i]; rho = self.rW[i][:, None]
            s["Wt"] = d * s["Wt"] + 1.0
            dp = pi - s["mp"]; s["mp"] += dp / s["Wt"]
            dr = rho - s["mr"]; s["mr"] += dr / s["Wt"]
            inc_c = dp * (rho - s["mr"]); inc_e = dp * (pi - s["mp"])
            s["C"] = d * s["C"] + inc_c; s["E"] = d * s["E"] + inc_e
            s["bP"] += inc_c; s["bE"] += inc_e
            if (self.t + 1) % self.B[i] == 0:
                s["A11"] = s["d2B"] * s["A11"] + s["bP"] ** 2
                s["A12"] = s["d2B"] * s["A12"] + s["bP"] * s["bE"]
                s["A22"] = s["d2B"] * s["A22"] + s["bE"] ** 2
                s["Eb"] = s["dB"] * s["Eb"] + s["bE"]
                s["bP"][:] = 0.0; s["bE"][:] = 0.0
            Ef = np.maximum(s["E"], p["sigma0"] ** 2 * s["Wt"] + 1e-15)
            beta = s["C"] / Ef
            neff = s["Eb"] ** 2 / np.maximum(s["A22"], 1e-300)
            Ebf = np.maximum(s["Eb"], 1e-300)
            var = np.maximum(s["A11"] - 2 * beta * s["A12"] + beta * beta * s["A22"], 0) / (Ebf * Ebf)
            var = var * neff / np.maximum(neff - 1.0, 1e-9)
            se = np.sqrt(var)
            enough = neff >= p["n_req"]
            s["latch"] = (enough & (beta - p["z"] * se > tgt[:, None])) | (s["latch"] & (beta > tgt[:, None]))
            s["beta"], s["se"], s["neff"] = beta, se, neff
            bmax = np.maximum(bmax, np.max(np.where(s["latch"], beta, 0.0), 1))
        target = np.where(bmax > 0, tgt / np.where(bmax > 0, bmax, 1.0), 1.0)
        target = np.clip(target, 0.0, 1.0)
        self.a = np.minimum(self.a, target) if p["ratchet"] else target
        lowered = (self.a < 1.0) & (self.first < 0)
        self.first[lowered] = self.t / FS
        self.engaged += self.a < 1.0
        self.t += 1
        return self.a * r


class LedgerE0(Ledger):
    """The current ledger with an evidence floor E0 on every key (b = kappa c (E + E0) - S): a variant for the F1
    study only (it changes the bit-identical ledger, so it is not part of revision 2's build)."""

    def __init__(self, c, E0=0.0, kappa=0.70):
        super().__init__(c, kappa=kappa); self.E = self.E + E0


def run2(U, X, c, u0, net="new", led_E0=None, led_kappa=0.70, record_a=False, gov_p=GOV2, ledger=True):
    """net: 'old' = ledger only; 'new' = Governor2 -> ledger. Returns (out, ledger hits/T, governor engaged/T, A, gov)."""
    T, n = U.shape
    led = (LedgerE0(c, led_E0, led_kappa) if led_E0 is not None else Ledger(c, kappa=led_kappa)) if ledger else None
    gov = Governor2(c, u0, gov_p) if net == "new" else None
    O = np.empty_like(X); A = np.ones((T, n), np.float32) if record_a else None
    for t in range(T):
        x = X[t]
        if gov is not None:
            x = gov.step(U[t], x)
            if record_a:
                A[t] = gov.a
        O[t] = led.step(U[t], x) if led is not None else x
    hits = led.hits / T if led is not None else np.zeros(n)
    eng = gov.engaged / T if gov is not None else np.zeros(n)
    return O, hits, eng, A, gov


def causal_copy(u, D_s, u0):
    """g = 1 copy of (u - u0) delayed D_s; 0 before D_s (the factual and shadow runs agree until the route acts)."""
    x = delay(u - u0, D_s * FS)
    x[:int(np.ceil(D_s * FS))] = 0.0
    return x


def counted_routes(U, u0, c, gain, signed):
    """The counted routes as the engine has them relative to the neutral input u0 (= b_id): the fast gear (0.45 s,
    4-s onset filter at rest at u0; one-sided channels rectified) plus a held 2-min route at 0.22 c_k (traces at 0 at
    session start)."""
    T, n = U.shape
    xd = np.stack([delay(U[:, k], 0.45 * FS) for k in range(n)], 1); xd[:5] = u0
    e = (xd - u0) - lp(xd - u0, 4.0)
    fast = gain * np.where(signed[None, :], e, np.maximum(e, 0))
    return fast + 0.22 * c * lp(U - u0, 120.0)


def windowed_metric(U, Y, seg_s=1200.0):
    """Worst block slope over non-overlapping segments of seg_s (a running metric): returns (n,) max over segments."""
    T = U.shape[0]; L = int(seg_s * FS); out = None
    for s0 in range(0, T - L + 1, L):
        w = wbs(U[s0:s0 + L], Y[s0:s0 + L])
        out = w if out is None else np.maximum(out, w)
    return out
