"""Numerical checks of the mathematics in design-commutator-coupling.md.

These verify algebra and the behaviour of the stated operators on constructed signals.
They are NOT evidence about people or about the design's behaviour in conversation
(brief: self-built simulated worlds are never evidence). numpy only; runs in about a minute.

C1  the dyadic-tree commutators sum to the Levy area of the window (piecewise-linear path)
C2  the normalised commutator rho: zero on affine copy (any gain, offset, a lagged ramp), on a held party;
    swap-antisymmetric; |rho| < 1; invariant to rescaling either party above the floor
C3  sinusoid area per period = -pi r_s r_p sin(phi)  (maximal at a quarter-period lag)
C4  recoverability: the N-1 split commutators plus the own path determine the partner's N increments
    up to adding a multiple of the own increments (rank N-1)
C5  the tree's (co, quad) pair: phase invariance of the coherent gain kappa at the matched scale, and its ripple
C6  the per-octave coherent limiter on adversarial partner-caused routes (copy at lag 0, 0.9 s, a quarter period,
    20 s) and on the frozen fast echo; independent metric = max over lags of pooled windowed regression
C7  closed-loop vs open-loop own side: a phase oscillator steered by rho locks to the partner (copy) when rho uses
    its rendered output, and does not when rho uses its autonomous (shadow) path
C8  rate and amplitude: drive per unit time per scale is bounded by 1 whatever the partner's burst rate or amplitude
C9  yoked replay vs a live follower: mean rho ~ 0 for an independent partner, signed for a follower
Run:  python3 -I checks.py > out.txt
"""
import time
import numpy as np
from scipy.signal import lfilter

T0 = time.time()
FS = 30.0
NULL_OFFSET = 300.0  # s: the null statistic is the same max over lags, 5 min further back
rng = np.random.default_rng(7)


def levy_area_pl(a, b):
    """Exact Levy area of the piecewise-linear path through samples (a_t, b_t)."""
    a0, b0 = a[0], b[0]
    da, db = np.diff(a), np.diff(b)
    return 0.5 * np.sum((a[:-1] - a0) * db - (b[:-1] - b0) * da)


def split_commutators(a, b, j):
    """Commutators of all complete nodes of length 2**j frames (j >= 1) on a tree anchored at sample 0."""
    h = 2 ** (j - 1)
    n = (len(a) - 1) // (2 * h)
    if n == 0:
        return np.zeros(0), np.zeros((0, 2)), np.zeros((0, 2))
    idx = np.arange(0, 2 * n * h + 1, h)
    ia, ib = np.diff(a[idx]), np.diff(b[idx])
    aL, aR, bL, bR = ia[0::2], ia[1::2], ib[0::2], ib[1::2]
    c = 0.5 * (aL * bR - bL * aR)
    return c, np.stack([aL, aR], 1), np.stack([bL, bR], 1)


def rho_nodes(a, b, j, eps):
    c, va, vb = split_commutators(a, b, j)
    D = eps + 0.5 * np.abs(va).sum(1) * np.abs(vb).sum(1)
    return c / D


out = {}
# ---------------------------------------------------------------- C1
J = 12
N = 2 ** J
a = np.cumsum(rng.normal(size=N + 1)); b = np.cumsum(rng.normal(size=N + 1))
direct = levy_area_pl(a, b)
tree = sum(split_commutators(a, b, j)[0].sum() for j in range(1, J + 1))
print(f"C1  Levy area direct {direct:.6f}  tree sum {tree:.6f}  |diff| {abs(direct - tree):.2e}")

# ---------------------------------------------------------------- C2
x = np.cumsum(rng.normal(size=N + 1)) * 0.01
eps = 1e-6
for lab, s in [("copy a=1", x), ("copy a=0.3,+0.2", 0.3 * x + 0.2), ("anti a=-2", -2 * x + 1)]:
    r = np.concatenate([rho_nodes(s, x, j, eps) for j in range(1, J + 1)])
    print(f"C2  {lab:18s} max|rho| = {np.abs(r).max():.2e}")
t = np.arange(N + 1) / FS
ramp = 0.01 * t; lagged = 0.01 * (t - 0.9)
r = np.concatenate([rho_nodes(lagged, ramp, j, eps) for j in range(1, J + 1)])
print(f"C2  lagged ramp (0.9 s)      max|rho| = {np.abs(r).max():.2e}")
held = np.full(N + 1, 0.4)
r = np.concatenate([rho_nodes(x, held, j, eps) for j in range(1, J + 1)])
print(f"C2  partner held at 0.4      max|rho| = {np.abs(r).max():.2e}")
y = np.cumsum(rng.normal(size=N + 1)) * 0.01
r1 = np.concatenate([rho_nodes(x, y, j, eps) for j in range(1, J + 1)])
r2 = np.concatenate([rho_nodes(y, x, j, eps) for j in range(1, J + 1)])
r3 = np.concatenate([rho_nodes(5 * x, 2 * y, j, eps) for j in range(1, J + 1)])
print(f"C2  swap: max|rho(s,p)+rho(p,s)| = {np.abs(r1 + r2).max():.2e};  max|rho| = {np.abs(r1).max():.3f} (<1)")
big = np.abs(r1) > 0.05
print(f"C2  rescale s x5, p x2 (floor fixed, motion >> floor): median |change| {np.median(np.abs(r1 - r3)):.2e}; max |change| where |rho| > 0.05: {np.abs(r1 - r3)[big].max():.2e}")

# ---------------------------------------------------------------- C3
w = 2 * np.pi / 2.0  # 2-s period
tt = np.arange(0, 2.0 + 1e-9, 1 / 3000.0)
for phi in [0, np.pi / 4, np.pi / 2, np.pi]:
    s = 0.3 * np.sin(w * tt); p = 0.5 * np.sin(w * tt + phi)
    A = levy_area_pl(s, p)
    print(f"C3  phi={phi:4.2f}  area/period {A:+.5f}   -pi r_s r_p sin(phi) {(-np.pi*0.3*0.5*np.sin(phi)):+.5f}")

# ---------------------------------------------------------------- C4
Jn = 6; Nl = 2 ** Jn
own = rng.normal(size=Nl)            # own leaf increments (known)
rows = []
for j in range(1, Jn + 1):
    h = 2 ** (j - 1)
    for i in range(Nl // (2 * h)):
        L = slice(2 * i * h, 2 * i * h + h); R = slice(2 * i * h + h, 2 * i * h + 2 * h)
        row = np.zeros(Nl)
        row[L] = -0.5 * own[R].sum()      # -1/2 dp_L * ds_R
        row[R] = +0.5 * own[L].sum()      # +1/2 ds_L * dp_R
        rows.append(row)
M = np.array(rows)
sv = np.linalg.svd(M, compute_uv=False)
null = np.linalg.svd(M)[2][-1]
cosang = abs(null @ own) / np.linalg.norm(own)
print(f"C4  {M.shape[0]} commutators, {Nl} partner increments: rank {np.sum(sv > 1e-9 * sv[0])}; "
      f"null vector parallel to own increments: |cos| = {cosang:.6f}")


# ---------------------------------------------------------------- C5
def quad_pairs(x, T, offset=0):
    """(increment over first half, increment over second half) of nodes of length T frames."""
    h = T // 2
    n = (len(x) - 1 - offset) // T
    idx = offset + np.arange(0, n * T + 1, h)
    inc = np.diff(x[idx])
    return np.stack([inc[0::2], inc[1::2]], 1)


def kappa(vs, vp):
    C = vs.T @ vp / len(vp)
    P = (vp ** 2).sum(1).mean()
    co = np.trace(C); qu = C[0, 1] - C[1, 0]
    return np.hypot(co, qu) / P, co / P, qu / P


print("C5  coherent gain kappa / true gain, best scale, over lag phase; period/node ratio in one octave")
res = []
tt = np.arange(0, 600, 1 / FS)
for ratio in [1.41, 1.6, 2.003, 2.5, 2.83]:
    T = 32; period = ratio * T / FS
    w = 2 * np.pi / period
    ks = []
    for phi in np.linspace(0, 2 * np.pi, 13)[:-1]:
        p = np.sin(w * tt); s = 0.3 * np.sin(w * tt - phi)
        Ps = {TT: (quad_pairs(p, TT) ** 2).sum(1).mean() for TT in [16, 32, 64]}
        Pm = max(Ps.values())
        best = max(kappa(quad_pairs(s, TT), quad_pairs(p, TT))[0] for TT in [16, 32, 64] if Ps[TT] > 0.05 * Pm)
        ks.append(best / 0.3)
    res.append((ratio, min(ks), max(ks)))
    print(f"     period = {ratio:.2f} node: kappa/gain min {min(ks):.3f} max {max(ks):.3f}")
rip_min = min(r[1] for r in res); rip_max = max(r[2] for r in res)
print(f"C5  ripple over the octave and all phases: [{rip_min:.3f}, {rip_max:.3f}]")


# ---------------------------------------------------------------- signal generators
def expr_signal(rng, n, rate_per_min=4.0, amp=0.5, drift=0.05):
    x = np.zeros(n)
    t = 0.0
    dt = 1 / FS
    while True:
        t += rng.exponential(60.0 / rate_per_min)
        i0 = int(t * FS)
        if i0 >= n:
            break
        hold = rng.uniform(1.0, 4.0); A = amp * rng.uniform(0.5, 1.0)
        k = np.arange(n - i0) * dt
        rise = 1 - np.exp(-k / 0.3)
        fall = np.where(k > hold, np.exp(-(k - hold) / 0.6), 1.0)
        x[i0:] += A * rise * fall
    ou = np.zeros(n); a_ = np.exp(-dt / 60.0)
    e = rng.normal(size=n) * drift * np.sqrt(1 - a_ ** 2)
    for i in range(1, n):
        ou[i] = a_ * ou[i - 1] + e[i]
    return np.clip(x + ou + 0.005 * rng.normal(size=n), 0, 1)


def delay(x, d):
    d = int(round(d))
    return np.concatenate([np.full(d, x[0]), x[:-d]]) if d > 0 else x.copy()


def lowpass(x, tau):
    a_ = np.exp(-1 / (FS * tau)); y = np.empty_like(x); y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = a_ * y[i - 1] + (1 - a_) * x[i]
    return y


def echo(x, G=0.224, d=0.9):
    xd = delay(x, d * FS)
    E = xd - lowpass(xd, 4.0)
    return G * np.maximum(E, 0)


# ---------------------------------------------------------------- the limiter
def atrous(x, J):
    A = [x]
    for j in range(1, J + 1):
        A.append(0.5 * (A[-1] + delay(A[-1], 2 ** (j - 1))))
    D = [A[j - 1] - A[j] for j in range(1, J + 1)]
    return D, A[J]


def ew(x, tau):
    a_ = np.exp(-1 / (FS * tau))
    return lfilter([1 - a_], [1, -a_], x)


def limiter(delta, part, c, J=11, margin=0.85, Lmax=60.0, lag_complete=True):
    """Per-octave attenuate-only cap on the coherent gain of delta toward part, at every lag up to Lmax.
    Band j (causal a-trous Haar detail D_j, q = 2^(j-1) frames): for each lag l on the grid {0, q, 2q, ...} <= Lmax,
    quadrature pair of the partner (D_j^p[t-l], D_j^p[t-l-q]) against (D_j^d[t], D_j^d[t-q]); EW estimates
    (tau = max(30 s, 16 T_j) and max(10 s, 8 T_j); P floored at 0.25 x its 10-min mean) of C(l) and P; kappa_j = max_l hypot(tr C, C12 - C21) / P;
    alpha_j = min(1, c'/kappa_j); closed for the first 2 s. lag_complete=False uses l = 0 only (phase-complete only)."""
    Dd, Rd = atrous(delta, J); Dp, Rp = atrous(part, J)
    n = len(delta); y = np.zeros(n); cc = c * margin
    for j, (bd, bp) in enumerate(zip(Dd + [Rd], Dp + [Rp]), start=1):
        q = 2 ** (min(j, J) - 1)
        bd2 = delay(bd, q)
        T = 2 ** j / FS
        lags = np.arange(0, int(Lmax * FS) + 1, q) if lag_complete else [0]
        k = np.zeros(n)
        taus = [max(30.0, 16 * T), max(10.0, 8 * T)]
        Pp = [ew(bp * bp + delay(bp, q) ** 2, t_) for t_ in taus]
        Pfloor = 0.25 * ew(bp * bp + delay(bp, q) ** 2, 600.0)
        Pp = [np.maximum(P, Pfloor) for P in Pp]
        k0 = np.zeros(n); off = int(NULL_OFFSET * FS)
        for L in lags:
            for kk, extra in ((None, 0), ("null", off)):
                p1 = delay(bp, L + extra); p2 = delay(bp, L + extra + q)
                for t_, P in zip(taus, Pp):
                    c11 = ew(bd * p1, t_); c22 = ew(bd2 * p2, t_)
                    c12 = ew(bd * p2, t_); c21 = ew(bd2 * p1, t_)
                    v = np.hypot(c11 + c22, c12 - c21) / np.maximum(P, 1e-8)
                    if kk is None:
                        k = np.maximum(k, v)
                    else:
                        k0 = np.maximum(k0, v)
        k = np.maximum(k - k0, 0.0)
        alpha = np.where(k <= cc, 1.0, cc / np.maximum(k, 1e-12))
        alpha[: int(2 * FS)] = 0.0
        y += alpha * bd
    return y


def broadband_cap(y, part, c, margin=0.85):
    """Second stage, on the whole partner-caused part after the per-octave caps: for each window W in {2, 10, 60 s},
    high-pass both signals by subtracting their causal W-moving mean, scan lags (0.1 s to 3 s, 0.5 s to 10 s, 2 s to 60 s),
    EW (tau max(30 s, 4W) and max(10 s, 2W)) regression, partner variance floored at 0.25 x its 10-min mean, |cov(y_W(t), p_W(t-l))| / var(p_W); one attenuate-only factor min(1, c'/max)."""
    n = len(y); k = np.zeros(n); cc = c * margin
    for W, lags in [(2.0, np.arange(0, 3.01, 0.1)), (10.0, np.arange(0, 10.01, 0.5)), (60.0, np.arange(0, 60.1, 2.0))]:
        w = int(W * FS)
        ker = np.ones(w) / w
        yh = y - lfilter(ker, [1.0], y); ph = part - lfilter(ker, [1.0], part)
        Pfl = 0.25 * ew(ph * ph, 600.0)
        for t_ in [max(30.0, 4 * W), max(10.0, 2 * W)]:
            kk = np.zeros(n); k0 = np.zeros(n)
            for L in lags:
                for extra in (0.0, NULL_OFFSET):
                    pl = delay(ph, (L + extra) * FS)
                    v = np.abs(ew(yh * pl, t_)) / np.maximum(ew(pl * pl, t_), np.maximum(Pfl, 1e-8))
                    if extra == 0.0:
                        kk = np.maximum(kk, v)
                    else:
                        k0 = np.maximum(k0, v)
            k = np.maximum(k, np.maximum(kk - k0, 0.0))
    a = np.where(k <= cc, 1.0, cc / np.maximum(k, 1e-12)); a[: int(2 * FS)] = 0.0
    return a * y


def full_limiter(delta, part, c):
    return broadband_cap(limiter(delta, part, c), part, c)


def pooled_regression_max(y, p):
    """Independent copy metric: max over windows {2,10,60 s} and lags of the pooled within-window regression of y on p(t-lag)."""
    best = (0, None, None)
    for W, lags in [(2.0, np.arange(0, 3.01, 0.1)), (10.0, np.arange(0, 10.01, 0.5)), (60.0, np.arange(0, 60.1, 2.0))]:
        w = int(W * FS)
        for L in lags:
            pl = delay(p, L * FS)
            n = (len(y) // w) * w
            Y = y[:n].reshape(-1, w); P = pl[:n].reshape(-1, w)
            Y = Y - Y.mean(1, keepdims=True); P = P - P.mean(1, keepdims=True)
            sp = (P ** 2).sum()
            if sp < 1e-9:
                continue
            beta = (Y * P).sum() / sp
            if abs(beta) > abs(best[0]):
                best = (beta, W, L)
    return best


print("C6  per-octave coherent limiter, smile ceiling c = 0.35; partner: smile bursts 4/min + slow drift, 20 min")
n = int(20 * 60 * FS)
p = expr_signal(rng, n)
c_smile = 0.35
cases = {
    "copy, lag 0, gain 1": p - p.mean(),
    "copy, lag 0.9 s": delay(p, 0.9 * FS) - p.mean(),
    "copy, lag 2.5 s (quarter of 10 s)": delay(p, 2.5 * FS) - p.mean(),
    "copy, lag 20 s": delay(p, 20 * FS) - p.mean(),
    "anti-copy, lag 1.5 s, gain 0.8": -0.8 * (delay(p, 1.5 * FS) - p.mean()),
    "frozen echo G=0.224 @0.9 s": echo(p),
    "partner-caused, not copy (own bursts)": expr_signal(np.random.default_rng(99), n, 6, 0.3) - 0.1,
}
for lab, d in cases.items():
    b0 = pooled_regression_max(d, p)
    yph = limiter(d, p, c_smile, lag_complete=False)
    yo = limiter(d, p, c_smile)
    yv = broadband_cap(yo, p, c_smile)
    b1 = pooled_regression_max(yv, p); bph = pooled_regression_max(yph, p); bo = pooled_regression_max(yo, p)
    print(f"     {lab:36s} before {b0[0]:+.3f} (W {b0[1]:.0f} s, lag {b0[2]:.1f} s)  after {b1[0]:+.3f} "
          f"(W {b1[1]:.0f} s, lag {b1[2]:.1f} s); rms out/in {np.std(yv)/max(np.std(d),1e-9):.2f}; octaves only {bo[0]:+.3f}; phase-only octaves {bph[0]:+.3f}")
    out[lab] = (b0[0], b1[0])
# the echo's visible size
i_on = np.argmax(np.diff(p) > 0.03)
print(f"     echo: partner bursts 0.25-0.5 -> echo peak {echo(p).max():.3f} (onset lobe, within 0.9 s + rise)")

# ---------------------------------------------------------------- C7
print("C7  phase oscillator steered by rho (own rhythm 0.50 Hz, partner 0.53 Hz), 10 min")
n7 = int(600 * FS); dt = 1 / FS
tt = np.arange(n7) * dt
wp = 2 * np.pi * 0.53; ws = 2 * np.pi * 0.50
pp = 0.4 * np.sin(wp * tt)


def run_osc(k, own_side):
    th_sh = 0.0; th = 0.0; s_sh = np.zeros(n7); s = np.zeros(n7); jn = 5; T = 2 ** jn
    rhoh = 0.0; leak = 1 / 4.0; dlt = 0.0
    for i in range(n7):
        th_sh += ws * dt
        s_sh[i] = 0.4 * np.sin(th_sh)
        if own_side == "rendered":
            th += (ws + k * rhoh) * dt
            s[i] = 0.4 * np.sin(th)
        else:  # open loop: delta driven by rho(shadow, partner), with leak (contraction)
            dlt += (k * rhoh - leak * dlt) * dt
            s[i] = 0.4 * np.sin(th_sh + dlt)
        if i >= T and i % T == 0:
            a_ = (s if own_side == "rendered" else s_sh)[i - T:i + 1]; b_ = pp[i - T:i + 1]
            h = T // 2
            aL, aR = a_[h] - a_[0], a_[T] - a_[h]; bL, bR = b_[h] - b_[0], b_[T] - b_[h]
            c = 0.5 * (aL * bR - bL * aR)
            rhoh = c / (1e-4 + 0.5 * (abs(aL) + abs(aR)) * (abs(bL) + abs(bR)))
    return s


for k in [-0.6, +0.6]:
    for side in ["rendered", "shadow"]:
        s = run_osc(k, side)
        half = slice(n7 // 2, n7)
        cr = max(np.corrcoef(s[half], delay(pp, L)[half])[0, 1] for L in range(0, int(2.0 * FS)))
        beta = pooled_regression_max(s[half] - s[half].mean(), pp[half])
        s_sh = 0.4 * np.sin(ws * tt + ws * dt)
        lim = s_sh + full_limiter(s - s_sh, pp, 0.35)
        bl = pooled_regression_max(lim[half] - lim[half].mean(), pp[half])
        print(f"     k={k:+.1f} own side={side:8s}: max lagged corr with partner {cr:.3f}; pooled regression {beta[0]:+.3f} "
              f"(lag {beta[2]:.1f} s); with the limiter (c 0.35) {bl[0]:+.3f} (lag {bl[2]:.1f} s)")

# ---------------------------------------------------------------- C8
print("C8  mean |rho| per node and drive per second by scale: partner burst rate x1, x4, x16; amplitude x0.1, x1")
own = expr_signal(np.random.default_rng(11), n, rate_per_min=4)
for lab, pr in [("rate 4/min", expr_signal(np.random.default_rng(3), n, 4)),
                ("rate 16/min", expr_signal(np.random.default_rng(3), n, 16)),
                ("rate 64/min", expr_signal(np.random.default_rng(3), n, 64)),
                ("rate 4/min amp x0.1", 0.1 * expr_signal(np.random.default_rng(3), n, 4))]:
    row = []
    for j in [3, 5, 7, 9]:
        eps_j = (0.005 ** 2) * 2 ** j
        r = rho_nodes(own, pr, j, eps_j)
        row.append(f"j{j}: {np.abs(r).mean():.3f}")
    print(f"     {lab:20s} " + "  ".join(row) + "   (held drive per unit time <= 1 by construction)")

# ---------------------------------------------------------------- C9
print("C9  mean rho by scale: yoked (independent) partner vs a live follower (0.6 s, gain 0.7) vs a partner the agent follows")
yoked = expr_signal(np.random.default_rng(21), n)
follower = np.clip(0.7 * delay(own, 0.6 * FS) + 0.05 * expr_signal(np.random.default_rng(5), n), 0, 1)
led = expr_signal(np.random.default_rng(23), n)
agent_follows = np.clip(0.7 * delay(led, 0.6 * FS), 0, 1)
for lab, (s_, p_) in [("yoked", (own, yoked)), ("he follows me", (own, follower)), ("I follow him", (agent_follows, led))]:
    row = []
    for j in [4, 5, 6, 7, 8]:
        r = rho_nodes(s_, p_, j, (0.005 ** 2) * 2 ** j)
        row.append(f"j{j}({2**j/FS:.1f}s): {r.mean():+.3f}")
    print(f"     {lab:14s} " + "  ".join(row))
print(f"done in {time.time() - T0:.0f} s")
