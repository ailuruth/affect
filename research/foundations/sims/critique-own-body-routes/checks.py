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


def govern(y_prop, y_cf, p, kappa):
    """The design's Gamma, one channel (as in design-own-body/checks.py, plus the 0.1-Hz
    low-passed percept on lags >= 15 s as the design specifies)."""
    T = len(p)
    p_lp = lowpass(p, 1 / (2 * np.pi * 0.1))
    d = np.exp(-DT / TAUS)[:, None]
    S = np.zeros((len(TAUS), len(LAGS))); E = np.zeros_like(S)
    out = np.empty(T); r_out = np.empty(T)
    for t in range(T):
        idx = t - LAG_IDX
        ok = idx >= 0
        src = np.where(LP_LAG, p_lp[np.maximum(idx, 0)], p[np.maximum(idx, 0)])
        pl = np.where(ok, src, 0.0)[None, :]
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

# ------------------------------------------------------------------ X1
print("X1. The word seam funds Gamma: a full copy y = base + p passes when the twin's word-driven")
print("    expression already co-varies with the partner's face (common cause)")
topic = topic_track(T, g=np.random.default_rng(1))
fast = lowpass(np.random.default_rng(2).standard_normal(T), 0.5) * 0.05 / 0.09   # sd ~0.05
p_face = topic + fast                       # partner smile deviation tracks topic (his face, his words)
base = 0.15
words = lowpass(shift(topic, 1.0), 0.8)     # the twin hears the words (ASR lag 1 s) and appraises them
print("    beta = twin's word-driven gain; alpha = one internal weight blending the partner's face into output")
print("    columns: Gamma clip fraction | governed 1-min centered slope of rendered smile on his smile (median)")
print("             | copy defect ||y - base - p|| / ||p|| | twin-only slope")
for beta in [0.0, 0.5, 0.71, 0.9]:
    ycf = base + beta * words
    for alpha in [0.32, 0.6, 1.0]:
        yprop = (1 - alpha) * ycf + alpha * (base + p_face)
        out, r = govern(yprop, ycf, p_face, 0.32)
        clip = np.mean(np.abs(r - (render(yprop) - render(ycf))) > 1e-4)
        sl = np.median(win_slopes(out, p_face))
        cd = np.linalg.norm(out - base - p_face) / np.linalg.norm(p_face)
        tw = np.median(win_slopes(render(ycf), p_face))
        print(f"    beta {beta:4.2f} alpha {alpha:4.2f}: clipped {clip:5.3f} | slope {sl:5.2f} | copy defect {cd:5.2f}"
              f" | twin {tw:5.2f}")
print("    design claim (4.5): in-phase gain of the partner-caused part <= 0.32, copy defect >= 0.68")

# ------------------------------------------------------------------ X2
print("\nX2. Uncentered bound: while the partner holds a non-neutral level, copying every movement")
print("    around it at gain 1 passes Gamma (no word seam, twin constant)")
g2 = np.random.default_rng(3)
held = topic_track(T, seg=(60, 300), lo=0.15, hi=0.45, g=g2)   # held smile above his 7-day neutral
mov = lowpass(g2.standard_normal(T), 0.4) * 0.08 / 0.11
p2 = held + mov
ycf2 = np.full(T, 0.2)
cases = {
    "movements only, gain 1  (r* = p - lp30(p))": p2 - lowpass(p2, 30.0),
    "movements gain 1, level anti 0.5": (p2 - lowpass(p2, 30.0)) - 0.5 * lowpass(p2, 30.0),
    "full copy minus a constant 0.25 (twin offset)": p2 - 0.25,
}
for name, rstar in cases.items():
    out, r = govern(ycf2 + rstar, ycf2, p2, 0.32)
    mv = p2 - lowpass(p2, 30.0)
    s_c = np.median(win_slopes(r, p2)); s_m = np.median(win_slopes(r, mv))
    unc = kernel_ratio_max(r, p2, 0.0)
    clip = np.mean(np.abs(r - rstar) > 1e-4)
    print(f"    {name:46s} clipped {clip:5.3f} | centered 1-min slope on p {s_c:5.2f}, on his movements {s_m:5.2f}"
          f" | uncentered kernel max {unc:5.2f}")
print("    ceiling kappa_LP = 0.32")

# ------------------------------------------------------------------ X3
print("\nX3. Lag grid gaps: fast movements copied at a lag between grid points (or past 10 s / 60 s)")
g3 = np.random.default_rng(4)
# brow flashes / smile pulses: 0.4-s pulses at random times, no held level
pul = np.zeros(T); t = 0
while t < T:
    t += int(g3.exponential(2.5) / DT) + 5
    if t < T:
        pul[t:t + 12] += g3.uniform(0.2, 0.5)
p3 = lowpass(pul, 0.15)
ycf3 = np.full(T, 0.1)
for lag in [0.5, 3.3, 7.0, 12.0, 90.0]:
    out, r = govern(ycf3 + shift(p3, lag), ycf3, p3, 0.16)
    g_lag = np.median(win_slopes(r, shift(p3, lag), centered=False))
    clip = np.mean(np.abs(r - shift(p3, lag)) > 1e-4)
    print(f"    copy at lag {lag:5.1f} s: clipped {clip:5.3f} | 1-min in-phase gain at that lag {g_lag:5.2f} (kappa 0.16)")

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
print("\nX6. Tempo through the kept turn-event times: twin identical, agent latency follows his")
g6 = np.random.default_rng(7)
nt = 2000
his_lat = np.exp(lowpass(g6.standard_normal(nt), 30 * DT * 30) * 3 + np.log(0.6))   # drifting latency, s
ema = lowpass(his_lat, 5 * DT * 30)   # a fixed diagonal recurrence of the event times (5-turn time constant)
for w in [0.08, 0.5, 1.0]:
    ag = 0.5 + w * (ema - ema.mean())
    ag_cf = 0.5 + w * (ema - ema.mean())          # twin sees the same event times
    print(f"    decoder weight {w:4.2f}: r = {np.max(np.abs(ag - ag_cf)):.1f}; slope of agent reply latency on his "
          f"{np.polyfit(his_lat, ag, 1)[0]:5.2f} (kappa_latency 0.08, not applied)")

# ------------------------------------------------------------------ X7
print("\nX7. Reciprocity estimate with the specified innovation (sd 0.05) and a smooth human response")
g7 = np.random.default_rng(8)


def iv_run(mu, tau_r, xi_sd=0.05, minutes=10, lag=13, seed=0):
    g = np.random.default_rng(seed)
    n = int(minutes * 60 / DT)
    xi = lowpass(g.standard_normal(n), 0.1) * xi_sd / 0.12          # muscle-filtered innovation
    y = 0.15 + xi                                                       # agent's channel (no echo)
    own = lowpass(g.standard_normal(n), 0.5) * 0.10 / 0.09              # his own smile movements, sd 0.1
    resp = lowpass(shift(y - 0.15, lag * DT), tau_r) * mu               # his level response mu, smooth
    p = own + resp
    a = np.sum(p[1:] * p[:-1]) / np.sum(p[:-1] ** 2)                   # his own-past predictor (AR1)
    dp = p[1:] - a * p[:-1]
    X = xi[:-1]; Y = y[:-1]
    Xl = np.zeros_like(X); Xl[lag:] = X[:-lag]; Yl = np.zeros_like(Y); Yl[lag:] = Y[:-lag]
    return np.cov(dp, Xl)[0, 1] / np.cov(Yl, Xl)[0, 1]


for mu in [0.0, 0.15, 0.30]:
    for tau_r in [0.033, 0.3]:
        est = np.array([iv_run(mu, tau_r, seed=s) for s in range(40)])
        print(f"    true level response {mu:4.2f}, response time constant {tau_r:5.3f} s: 10-min IV estimate mean "
              f"{est.mean():6.3f}, sd {est.std():5.3f}; P(|est| clipped at 0.32) {np.mean(np.abs(est) > 0.32):.2f}")
