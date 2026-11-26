"""Counterexample checks for critique-design-own-body-generative-routes.md (sections X1-X7).

Constructed partners and agents, not evidence about people (brief.md: no toy worlds).
They use the design's own Gamma (copied from sims/design-own-body/checks.py), its windows,
lag grid and ceilings, and test what the rendered output does.
Run:  python3 -I checks.py   (numpy, scipy; a few minutes)
"""
import numpy as np
from scipy.signal import lfilter

DT = 1 / 30.0
rng = np.random.default_rng(11)

TAUS = np.geomspace(0.3, 7200.0, 12)
LAGS = np.concatenate([np.arange(0, 31) * DT,
                       np.array([1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 15, 20, 30, 45, 60])])
LAG_IDX = np.round(LAGS / DT).astype(int)
LP_LAG = LAGS >= 15          # design: lags of 15 s and more act on 0.1-Hz low-passed percepts


def lowpass(x, tau):
    a = np.exp(-DT / tau)
    return lfilter([1 - a], [1, -a], x)


def render(x):
    return np.clip(x, 0.0, 1.0)


def govern(y_prop, y_cf, p, kappa, taus=None, pair_ratio=None):
    """The design's Gamma, one channel (as in design-own-body/checks.py, plus the 0.1-Hz
    low-passed percept on lags >= 15 s as the design specifies).
    taus / pair_ratio: only for the repaired variant of X3 (windows from taus; a (window, lag)
    pair is used only when tau >= lag / pair_ratio)."""
    T = len(p)
    taus = TAUS if taus is None else taus
    p_lp = lowpass(p, 1 / (2 * np.pi * 0.1))
    d = np.exp(-DT / taus)[:, None]
    mask = np.ones((len(taus), len(LAGS)), bool) if pair_ratio is None else (taus[:, None] >= LAGS[None, :] / pair_ratio)
    S = np.zeros((len(taus), len(LAGS))); E = np.zeros_like(S)
    out = np.empty(T); r_out = np.empty(T)
    for t in range(T):
        idx = t - LAG_IDX
        ok = idx >= 0
        src = np.where(LP_LAG, p_lp[np.maximum(idx, 0)], p[np.maximum(idx, 0)])
        pl = np.where(mask, np.where(ok, src, 0.0)[None, :], 0.0)
        Sd = np.maximum(d * S, 0.0); Ed = d * E + pl ** 2
        b = kappa * Ed - Sd
        base = render(y_cf[t]); r = render(y_prop[t]) - base
        with np.errstate(divide="ignore", invalid="ignore"):
            lim = np.where(pl != 0, b / pl, np.nan)
        hi = np.nanmin(np.where(pl > 0, lim, np.inf)); lo = np.nanmax(np.where(pl < 0, lim, -np.inf))
        r_t = min(max(r, lo), hi)
        S = Sd + r_t * pl; E = Ed
        out[t] = base + r_t; r_out[t] = r_t
    return out, r_out


def shift(x, lag_s):
    n = int(round(lag_s / DT)); y = np.zeros_like(x)
    if n < len(x):
        y[n:] = x[:len(x) - n]
    return y


def win_slopes(y, p, W=60.0, centered=True):
    """slope of y on p in consecutive boxcar windows of W s (centered = ordinary regression)."""
    n = int(W / DT); out = []
    for s in range(0, len(p) - n + 1, n):
        a = p[s:s + n]; b = y[s:s + n]
        if centered:
            a = a - a.mean(); b = b - b.mean()
        den = np.sum(a * a)
        if den > 1e-6 * n:
            out.append(np.sum(a * b) / den)
    return np.array(out)


def kernel_ratio_max(r, p, lag_s):
    """max over the design's kernel windows of sum d^(t-s) r p_lag / sum d^(t-s) p_lag^2 (uncentered)."""
    pl = shift(p, lag_s); best = -np.inf
    for tau in TAUS[:9]:
        dm = np.exp(-DT / tau)
        num = lfilter([1], [1, -dm], r * pl); den = lfilter([1], [1, -dm], pl * pl)
        m = den > 0.02 * tau / DT * 0.01
        best = max(best, float(np.max(num[m] / den[m])))
    return best


def topic_track(T, seg=(60, 180), lo=-0.2, hi=0.5, g=None):
    g = g or rng
    x = np.zeros(T); t = 0
    while t < T:
        L = int(g.uniform(*seg) / DT); x[t:t + L] = g.uniform(lo, hi); t += L
    return x



T = int(10 * 60 / DT)


def gain(r, ref):
    return float(np.sum(r * ref) / np.sum(ref * ref))


# ------------------------------------------------------------------ X1
print("X1. Word seam and Gamma together: his smile tracks topic; the twin's word-driven smile has gain beta;")
print("    one internal weight alpha blends his face into the proposal")
topic = topic_track(T, g=np.random.default_rng(1))
fast = lowpass(np.random.default_rng(2).standard_normal(T), 0.5); fast = fast / fast.std() * 0.05
p_face = topic + fast
base = 0.15
words = lowpass(shift(topic, 1.0), 0.8)          # ASR lag 1 s, then the agent's own appraisal
for beta in [0.0, 0.71, 0.9]:
    ycf = base + beta * words
    for alpha in [0.32, 1.0]:
        yprop = (1 - alpha) * ycf + alpha * (base + p_face)
        out, r = govern(yprop, ycf, p_face, 0.32)
        cd = np.linalg.norm(out - base - p_face) / np.linalg.norm(p_face)
        cdt = np.linalg.norm(ycf - base - p_face) / np.linalg.norm(p_face)
        print(f"    beta {beta:4.2f} alpha {alpha:4.2f}: pooled slope rendered {np.polyfit(p_face, out, 1)[0]:4.2f}"
              f" (twin {np.polyfit(p_face, ycf, 1)[0]:4.2f}, governed part {np.polyfit(p_face, r, 1)[0]:4.2f})"
              f" | copy defect {cd:4.2f} (twin alone {cdt:4.2f})")
print("    design 4.5: 'copy defect >= 0.68 for any partner expression'")

# ------------------------------------------------------------------ X2
print("\nX2. Uncentered bound: while he holds a level above his neutral, every movement around it")
print("    is copied at gain ~1 and passes (twin constant, no words)")
for (lo, hi, sd) in [(0.15, 0.45, 0.08), (0.30, 0.60, 0.04)]:
    g2 = np.random.default_rng(3)
    held = topic_track(T, seg=(60, 300), lo=lo, hi=hi, g=g2)
    mov = lowpass(g2.standard_normal(T), 0.4); mov = mov / mov.std() * sd
    p2 = held + mov
    rstar = p2 - lowpass(p2, 30.0)                       # copy of his movements, gain 1
    out, r = govern(0.2 + rstar, np.full(T, 0.2), p2, 0.32)
    mv = p2 - lowpass(p2, 30.0)
    print(f"    held {lo:.2f}-{hi:.2f}, movement sd {sd:.2f}: median 1-min slope of governed r on his movements"
          f" {np.median(win_slopes(r, mv)):4.2f} | uncentered kernel ratio max {kernel_ratio_max(r, p2, 0.0):4.2f}"
          f" (kappa 0.32)")

# ------------------------------------------------------------------ X3
print("\nX3. Over-clamp: on fast, zero-mean movement (no held level) the 0.3-s windows at 46 lags leave")
print("    almost no room for any partner-caused response, in phase, away or cross-channel (kappa 0.16)")
g3 = np.random.default_rng(12)
z = lowpass(g3.standard_normal(T), 0.4); z = z / z.std() * 0.08
q = lowpass(g3.standard_normal(T), 0.4); q = q / q.std() * 0.08
ycf3 = np.full(T, 0.4)
tests = [("innate echo 0.10 at 0.45 s", 0.10 * shift(z, 0.45), shift(z, 0.45)),
         ("echo at ceiling 0.16 at 0.45 s", 0.16 * shift(z, 0.45), shift(z, 0.45)),
         ("away, -0.5 at 0.45 s", -0.5 * shift(z, 0.45), shift(z, 0.45)),
         ("cross-channel, 0.5 x his other channel", 0.5 * q, q),
         ("copy at 7 s", shift(z, 7.0), shift(z, 7.0)),
         ("copy at 12 s", shift(z, 12.0), shift(z, 12.0))]
for variant, kw in [("as specified", {}),
                    ("repaired windows (tau >= 1 s, tau >= lag/3)", dict(taus=np.geomspace(1.0, 7200, 10), pair_ratio=3.0))]:
    print(f"    Gamma {variant}:")
    for name, rs, ref in tests:
        out, r = govern(ycf3 + rs, ycf3, z, 0.16, **kw)
        print(f"      {name:40s} kept {np.sum(r * rs) / np.sum(rs * rs):5.3f} | realised gain on its reference {gain(r, ref):6.3f}"
              f" | worst 10-s window {np.max(win_slopes(r, ref, W=10, centered=False)):5.2f}")
# smile flashes on a near-neutral face
g3b = np.random.default_rng(9)
fl = np.zeros(T); t = 0
env = np.concatenate([np.linspace(0, 1, 9), np.ones(30), np.linspace(1, 0, 15)])
while t < T:
    t += int(g3b.exponential(4.0) / DT) + 30
    if t + len(env) < T:
        fl[t:t + len(env)] += g3b.uniform(0.2, 0.5) * env
fl += 0.01 * g3b.standard_normal(T)
for gk in [0.10, 0.32]:
    rs = gk * shift(fl, 0.45)
    out, r = govern(0.15 + rs, np.full(T, 0.15), fl, 0.32)
    print(f"    smile flashes (0.2-0.5, 1.8 s, every ~5 s): echo {gk:.2f} at 0.45 s realised {gain(r, shift(fl, 0.45)):5.3f}"
          f" (kappa_LP 0.32)")

# ------------------------------------------------------------------ X4
print("\nX4. The twin's neutral n_j drifts with his weeks-long mood; whatever the agent does with")
print("    his held face, the twin does with n_j, outside Gamma")
g4 = np.random.default_rng(5)
days = 365
mood = np.zeros(days); d = 0
while d < days:
    L = int(g4.uniform(20, 60)); mood[d:d + L] = g4.choice([0.0, 0.35]); d += L   # inner-brow (sad) months
sess = mood + g4.normal(0, 0.05, days)          # his session-mean inner-brow raise
n = 0.0; hist = []; nj = []
for dd in range(days):
    nj.append(n)
    hist.append(sess[dd]); med = np.median(hist[-7:])
    n = n + np.clip(med - n, -0.02, 0.02)       # bounded nightly step 0.02
nj = np.array(nj)
for g in [0.3, 0.8]:
    ybar = 0.05 + g * nj                          # twin: any route from held face to own brow, fed n_j
    # Gamma at the session scale (held levels): the partner-caused part r = g (sess - n_j) is in phase
    # with p = sess - n_j whatever its sign, so it is cut to kappa (sess - n_j); the twin part is untouched
    y = ybar + min(g, 0.16) * (sess - nj)
    sl = np.polyfit(sess, y, 1)[0]
    lo_m = mood == 0.35
    print(f"    route gain {g:3.1f}: session-pooled slope of agent inner brow on his {sl:5.2f} (kappa 0.16);"
          f" agent brow in sad months {y[lo_m].mean():.3f} vs other {y[~lo_m].mean():.3f}; n_j reaches {nj.max():.2f}")

# ------------------------------------------------------------------ X5
print("\nX5. One ELBO over both slots: the shared word-conditioned prior learns his topic faces;")
print("    the self slot acts its own prior out; the twin shares theta and words, so r = 0")
K = 12
g5 = np.random.default_rng(6)
f = g5.uniform(-0.3, 0.6, K)          # his habitual smile per topic (and a disgust topic below)
gown = g5.uniform(-0.1, 0.3, K)       # the agent's own appraisal-driven smile per topic
for lam in [0.5, 0.8, 0.95]:
    for rho in [0.3, 0.5]:
        a = gown.copy()
        for night in range(400):
            mu = (1 - rho) * a + rho * f + g5.normal(0, 0.01, K)   # pooled least-squares prior per topic
            a = lam * mu + (1 - lam) * gown
        sl = np.polyfit(f, a, 1)[0]
        print(f"    prior weight lambda {lam:4.2f}, partner data share rho {rho:3.1f}: slope of agent's topic face on his"
              f" {sl:5.2f} (start {np.polyfit(f, gown, 1)[0]:5.2f})")
fw = 0.4; lam, rho = 0.8, 0.5
aw = (lam * rho * fw) / (1 - lam * (1 - rho))
print(f"    nose wrinkle (kappa 0) at a topic where he wrinkles {fw}: agent converges to {aw:.2f}; Gamma sees r = 0")

# ------------------------------------------------------------------ X6
print("\nX6. Tempo through the kept turn-event times: the twin sees the same event times")
g6 = np.random.default_rng(7)
nt = 3000
lat = np.zeros(nt); s = 0.0
for i in range(nt):
    s = 0.98 * s + 0.2 * g6.standard_normal(); lat[i] = 0.6 * np.exp(0.5 * s)   # his reply latency per turn, s
ema = np.zeros(nt); e = lat[0]
for i in range(nt):
    e = 0.8 * e + 0.2 * lat[i]; ema[i] = e                                      # a fixed recurrence on event times
for w in [0.08, 0.5, 1.0]:
    ag = 0.5 + w * (ema - ema.mean()); ag_cf = ag.copy()
    print(f"    decoder weight {w:4.2f}: twin difference {np.max(np.abs(ag - ag_cf)):.1f} | slope of agent reply latency on his"
          f" {np.polyfit(lat[1:], ag[:-1] * 0 + ag[1:], 1)[0]:4.2f} (onset-latency ceiling 0.08 never applied)")

# ------------------------------------------------------------------ X7
print("\nX7. Reciprocity by own innovation (sd 0.05) when his response is a smooth level response")


def iv_run(mu, tau_r, xi_sd=0.05, minutes=10, lag=13, seed=0):
    g = np.random.default_rng(seed)
    n = int(minutes * 60 / DT)
    xi = lowpass(g.standard_normal(n), 0.1); xi = xi / xi.std() * xi_sd        # muscle-filtered innovation
    y = 0.15 + xi
    own = lowpass(g.standard_normal(n), 0.5); own = own / own.std() * 0.10
    resp = mu * lowpass(shift(xi, lag * DT), tau_r) if tau_r > 0 else mu * shift(xi, lag * DT)
    p = own + resp
    a = np.sum(p[1:] * p[:-1]) / np.sum(p[:-1] ** 2)
    dp = p[1:] - a * p[:-1]                    # dp[i] is his innovation at frame i+1
    xl = shift(xi, lag * DT)[1:]               # xi(t - lag) aligned with dp
    yl = shift(y - 0.15, lag * DT)[1:]
    return np.cov(dp, xl)[0, 1] / np.cov(yl, xl)[0, 1]


for mu in [0.15, 0.30]:
    for tau_r in [0.0, 0.15, 0.3]:
        est = np.array([iv_run(mu, tau_r, seed=s) for s in range(30)])
        print(f"    his level response {mu:4.2f}, response time constant {tau_r:4.2f} s: estimate {est.mean():6.3f} +- {est.std():5.3f}"
              f" ({est.mean() / mu:4.2f} of true)")
