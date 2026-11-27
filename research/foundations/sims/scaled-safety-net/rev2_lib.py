"""Revision 2 of the scaled gain governor (design-scaled-safety-net.md, "Revision 2"): reference implementation.

Synthetic-signal check of the mathematics only; not evidence about people or behaviour. numpy only.
Reuses check.py's definitions verbatim (signals, the block-mean metric and the current Ledger), as critique_check.py
does, and adds:
  Governor2      the revised governor (step and level keys, batch-sandwich evidence with a t test, three memories, ratchet)
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
level_blocks, bursts, partner = ns["level_blocks"], ns["bursts"], ns["partner"]
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
    kappa_g=0.60,          # target, fraction of c_k (ceiling)
    z=3.0,                 # confidence level, as a normal multiplier (one-sided p = 0.00135)
    t_crit=True,           # small-sample: the multiplier is Student's t at that level with n_eff - 1 degrees of freedom
    n_req=2.0,             # evidence floor: effective number of independent batches of his movement before a key may engage
    sigma0=0.01,           # floor on his window-mean SD (his units), as revision 1
    taus=(1800.0, 300.0, 60.0),  # three memories: the ledger's budget time and two short ones; latches combine by max slope
    # key sets: (window W s, kind, lag step s), lags 0..300 s. 'step': change of the W-window mean over one window
    # (revision 1's keys; they weight his faster movement); 'level': the W-window mean itself, regressed WITH an
    # intercept (the metric's own block means; they carry his slow movement).
    sets=((10.0, "step", 5.0), (10.0, "level", 5.0), (60.0, "level", 10.0)),
    batch_W=2.0,           # batch length for the sandwich and the evidence count = batch_W * W
    start_W=2.0,           # a key counts frames only from t >= L + start_W * W (no pre-session history in its sums)
    max_lag_s=300.0,
    ratchet=True,          # a_k never rises within a session once lowered
)


def t_mult(z, df):
    """Student-t quantile at the one-sided level of the normal multiplier z, df degrees of freedom (Cornish-Fisher
    expansion, Abramowitz-Stegun 26.7.5; within a few % of the exact quantile for df >= 3, below it for df < 3, so the
    n_req floor of 2 batches stays the binding guard there)."""
    df = np.maximum(df, 1.0)
    g1 = (z ** 3 + z) / 4; g2 = (5 * z ** 5 + 16 * z ** 3 + 3 * z) / 96
    g3 = (3 * z ** 7 + 19 * z ** 5 + 17 * z ** 3 - 15 * z) / 384
    g4 = (79 * z ** 9 + 776 * z ** 7 + 1482 * z ** 5 - 1920 * z ** 3 - 945 * z) / 92160
    return z + g1 / df + g2 / df ** 2 + g3 / df ** 3 + g4 / df ** 4


class Governor2:
    """Per channel k, key (W, kind, L) and memory tau:
      his signal  pi(t)  = ubar_W(t - L)                    (level)   or ubar_W(t-L) - ubar_W(t-L-W)  (step)
      output      rho(t) = rbar_W(t)                        (level)   or rbar_W(t) - rbar_W(t-W)      (step)
                  W-window exponential means; his started at the neutral input u0, the raw partner-caused part r at 0
      sums        only frames with t >= L + start_W W enter (the key never regresses on pre-session history)
      beta_hat    exponentially weighted (decay exp(-1/(tau fs))) covariance / variance WITH an intercept (West's
                  incremental update: exact, no lagging centre), variance floored at sigma0^2 per frame
      se, n_eff   batch sandwich over batches of B = batch_W W frames: with P_b, E_b the batch's covariance and variance
                  increments, se^2 = sum_b w_b^2 (P_b - beta E_b)^2 / (sum_b w_b E_b)^2 * n/(n-1), and the effective
                  number of independent batches n = (sum_b w_b E_b)^2 / sum_b w_b^2 E_b^2 (one large start-of-session
                  step counts as one batch however large it is)
      engage      n >= n_req and beta - z_n se > kappa_g c_k, z_n = Student's t multiplier at z's level with n - 1
                  degrees of freedom (z itself without t_crit); release when beta <= kappa_g c_k
      target      kappa_g c_k / (max over engaged keys and memories of beta)
      gain        a_k(t) = min(a_k(t-1), target)   (ratchet: never rises within a session)
    Every output-side threshold is a multiple of c_k; absolute quantities are on his signal (sigma0) or on time."""

    def __init__(self, c, u0, p=GOV2):
        self.c = np.asarray(c, float); n = len(self.c); self.n = n; self.p = p
        self.u0 = np.asarray(u0, float)
        self.wins = sorted({w for w, _, _ in p["sets"]})
        self.Wf = {w: int(round(w * FS)) for w in self.wins}
        self.aW = {w: 1 - np.exp(-1 / (w * FS)) for w in self.wins}
        self.H = int(p["max_lag_s"] * FS) + max(self.Wf.values()) + 1
        self.uW = {w: self.u0.copy() for w in self.wins}; self.rW = {w: np.zeros(n) for w in self.wins}
        self.uring = {w: np.repeat(self.u0[None, :], self.H, 0) for w in self.wins}
        self.rring = {w: np.zeros((self.H, n)) for w in self.wins}
        self.ptr = 0; self.t = 0
        self.ds = [np.exp(-1 / (tau * FS)) for tau in p["taus"]]
        self.sets = []
        for (w, kind, step) in p["sets"]:
            lags = np.arange(0, int(p["max_lag_s"] * FS) + 1, int(round(step * FS)))
            B = int(round(p["batch_W"] * w * FS)); K = len(lags)
            start = lags + int(round(p["start_W"] * w * FS))
            mem = []
            for d in self.ds:
                z = lambda: np.zeros((n, K))
                mem.append(dict(d=d, dB=d ** B, d2B=d ** (2 * B), Wt=np.zeros(K), mp=z(), mr=z(), C=z(), E=z(),
                                bP=z(), bE=z(), A11=z(), A12=z(), A22=z(), Eb=z(), latch=np.zeros((n, K), bool)))
            self.sets.append(dict(w=w, kind=kind, lags=lags, B=B, start=start, mem=mem))
        self.a = np.ones(n); self.engaged = np.zeros(n); self.first = np.full(n, -1.0)

    def step(self, u, r):
        p = self.p; H = self.H
        self.ptr = (self.ptr + 1) % H; q = self.ptr
        for w in self.wins:
            self.uW[w] += self.aW[w] * (u - self.uW[w]); self.rW[w] += self.aW[w] * (r - self.rW[w])
            self.uring[w][q] = self.uW[w]; self.rring[w][q] = self.rW[w]
        tgt = (p["kappa_g"] * self.c)[:, None]
        bmax = np.zeros(self.n)
        for S in self.sets:
            w, lags = S["w"], S["lags"]; Wf = self.Wf[w]
            if S["kind"] == "level":
                pi = self.uring[w][(q - lags) % H].T; rho = self.rW[w][:, None]
            else:
                pi = (self.uring[w][(q - lags) % H] - self.uring[w][(q - lags - Wf) % H]).T
                rho = (self.rW[w] - self.rring[w][(q - Wf) % H])[:, None]
            v = (self.t >= S["start"]).astype(float)
            batch_end = (self.t + 1) % S["B"] == 0
            for s in S["mem"]:
                d = s["d"]
                s["Wt"] = d * s["Wt"] + v
                inv = np.where(s["Wt"] > 0, v / np.maximum(s["Wt"], 1e-12), 0.0)
                dp = pi - s["mp"]; s["mp"] += dp * inv
                dr = rho - s["mr"]; s["mr"] += dr * inv
                inc_c = v * dp * (rho - s["mr"]); inc_e = v * dp * (pi - s["mp"])
                s["C"] = d * s["C"] + inc_c; s["E"] = d * s["E"] + inc_e
                s["bP"] += inc_c; s["bE"] += inc_e
                if batch_end:
                    s["A11"] = s["d2B"] * s["A11"] + s["bP"] ** 2
                    s["A12"] = s["d2B"] * s["A12"] + s["bP"] * s["bE"]
                    s["A22"] = s["d2B"] * s["A22"] + s["bE"] ** 2
                    s["Eb"] = s["dB"] * s["Eb"] + s["bE"]
                    s["bP"][:] = 0.0; s["bE"][:] = 0.0
                Ef = np.maximum(s["E"], p["sigma0"] ** 2 * s["Wt"] + 1e-15)
                beta = s["C"] / Ef
                neff = s["Eb"] ** 2 / np.maximum(s["A22"], 1e-300)
                Ebf = np.maximum(s["Eb"], 1e-30)
                var = np.maximum(s["A11"] - 2 * beta * s["A12"] + beta * beta * s["A22"], 0) / (Ebf * Ebf)
                se = np.sqrt(var * neff / np.maximum(neff - 1.0, 1e-9))
                enough = neff >= p["n_req"]
                zz = t_mult(p["z"], neff - 1.0) if p.get("t_crit") else p["z"]
                s["latch"] = (enough & (beta - zz * se > tgt)) | (s["latch"] & (beta > tgt))
                s["beta"], s["se"], s["neff"], s["zz"] = beta, se, neff, zz
                bmax = np.maximum(bmax, np.max(np.where(s["latch"], beta, 0.0), 1))
        target = np.clip(np.where(bmax > 0, tgt[:, 0] / np.where(bmax > 0, bmax, 1.0), 1.0), 0.0, 1.0)
        self.a = np.minimum(self.a, target) if p["ratchet"] else target
        lowered = (self.a < 1.0) & (self.first < 0)
        self.first[lowered] = self.t / FS
        self.engaged += self.a < 1.0
        self.t += 1
        return self.a * r

    def se_over_c(self):
        """Largest z_n se / (z c_k) among keys with enough evidence whose slope lies in (kappa_g c, kappa_g c + z_n se]
        (keys the engagement test may leave unlatched). Times a_k, this is eta of Theorem 1'."""
        tgt = (self.p["kappa_g"] * self.c)[:, None]; eta = np.zeros(self.n)
        for S in self.sets:
            for s in S["mem"]:
                m = (s["beta"] > tgt) & (s["beta"] <= tgt + s["zz"] * s["se"]) & (s["neff"] >= self.p["n_req"])
                eta = np.maximum(eta, np.max(np.where(m, s["zz"] * s["se"] / self.p["z"], 0.0), 1) / np.where(self.c > 0, self.c, 1))
        return eta


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
    O = np.empty_like(X); A = np.ones((T, n)) if record_a else None
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


def ledger_only(U, X, c, E0=None):
    """The ledger stage alone on a given input (e.g. the governor's output A * X), optionally with the floor E0."""
    led = LedgerE0(c, E0) if E0 else Ledger(c)
    O = np.empty_like(X)
    for t in range(U.shape[0]):
        O[t] = led.step(U[t], X[t])
    return O, led.hits / U.shape[0]


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
