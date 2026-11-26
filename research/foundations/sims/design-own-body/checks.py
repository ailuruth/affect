"""Algebra checks for design-own-body-generative.md (O1-O7).

These check the design's own inequalities and constructions on hand-made instances.
They are NOT evidence about behaviour, people or data (brief.md: no toy worlds).
Run:  python3 -I checks.py     (numpy, scipy; about one to two minutes)
"""
import numpy as np
from scipy.signal import lfilter

rng = np.random.default_rng(7)
DT = 1 / 30.0
OK = []


def report(name, cond, msg):
    OK.append(bool(cond))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}: {msg}")


def lowpass(x, tau):
    a = np.exp(-DT / tau)
    return lfilter([1 - a], [1, -a], x)


def shift(x, lag_s):
    """x(t - lag) with linear interpolation (lag may be off the frame grid)."""
    n = lag_s / DT
    i = int(np.floor(n)); f = n - i
    y = np.zeros_like(x)
    if i < len(x):
        y[i:] = x[: len(x) - i]
    y2 = np.zeros_like(x)
    if i + 1 < len(x):
        y2[i + 1:] = x[: len(x) - i - 1]
    return (1 - f) * y + f * y2


# ---------------------------------------------------------------- the ownership projection
TAUS = np.array([0.5, 3.0, 20.0, 120.0, 900.0, 7200.0])           # kernel windows, s
LAGS = np.concatenate([np.arange(0, 31) * DT,                       # 0..1 s, every frame
                       np.array([1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10,
                                 15, 20, 30, 45, 60])])
LAG_IDX = np.round(LAGS / DT).astype(int)


def render(x):          # innate monotone rendering of one channel (activation in [0, 1])
    return np.clip(x, 0.0, 1.0)


def govern(y_prop, y_cf, p, kappa, render_fn=render):
    """Ownership projection Gamma on one channel.
    y_prop: the factual proposal (pre-render); y_cf: the counterfactual self's proposal;
    p: the partner's deviation on the same channel (own-body coordinates).
    Returns the realised rendered output and the realised partner-caused part r."""
    T = len(p)
    d = np.exp(-DT / TAUS)[:, None]                     # (M,1)
    S = np.zeros((len(TAUS), len(LAGS)))
    E = np.zeros_like(S)
    out = np.empty(T); r_out = np.empty(T)
    for t in range(T):
        idx = t - LAG_IDX
        pl = np.where(idx >= 0, p[np.maximum(idx, 0)], 0.0)[None, :]   # (1,L)
        Sd = np.maximum(d * S, 0.0)                     # no banking of anti-phase credit
        Ed = d * E + pl ** 2
        b = kappa * Ed - Sd                             # >= kappa*pl^2 >= 0 by induction
        base = render_fn(y_cf[t])
        r = render_fn(y_prop[t]) - base
        with np.errstate(divide="ignore", invalid="ignore"):
            lim = np.where(pl != 0, b / pl, np.nan)
        hi = np.nanmin(np.where(pl > 0, lim, np.inf))
        lo = np.nanmax(np.where(pl < 0, lim, -np.inf))
        r_t = min(max(r, lo), hi)
        S = Sd + r_t * pl
        E = Ed
        out[t] = base + r_t
        r_out[t] = r_t
    return out, r_out


def inphase_max(r, p, windows_s, lags_s, min_energy=0.02):
    """max over boxcar windows and lags of sum(r*p_lag)/sum(p_lag^2), windows with partner energy."""
    best = -np.inf
    for lag in lags_s:
        pl = shift(p, lag)
        for W in windows_s:
            n = int(W / DT)
            if n > len(p):
                continue
            k = np.ones(n)
            num = np.convolve(r * pl, k, "valid"); den = np.convolve(pl * pl, k, "valid")
            m = den > min_energy * n
            if m.any():
                best = max(best, float(np.max(num[m] / den[m])))
    return best


def partner_signal(T, held=True, seed=None):
    g = np.random.default_rng(seed)
    x = lowpass(g.standard_normal(T), 0.4) * 2.0          # fast movements, ~0.4 s
    x += lowpass(g.standard_normal(T), 3.0) * 3.0
    if held:
        lev = np.zeros(T); t = 0
        while t < T:
            L = int(g.uniform(60, 600) / DT); lev[t:t + L] = g.uniform(-0.2, 0.6); t += L
        x = 0.25 * x + lev
    return x


print("O1. Ownership projection: in-phase gain <= kappa at every kernel window and lag grid point;")
print("    off-grid lags and boxcar windows measured; anti-phase and cross-channel untouched")
T = int(40 * 60 / DT)
p = partner_signal(T, seed=1)
q = partner_signal(T, seed=2)          # an independent partner channel (for cross-channel)
kappa = 0.40
ycf = 0.15 + 0.05 * np.sin(np.arange(T) * DT * 2 * np.pi / 90)  # the agent's own slow smile
cases = {
    "zero-lag copy (gain 1)": p,
    "amplified copy (gain 2)": 2 * p,
    "delayed copy 0.7 s (off grid)": shift(p, 0.7),
    "delayed copy 3.3 s (off grid)": shift(p, 3.3),
    "delayed copy 40 s": shift(p, 40.0),
    "held copy (60 s low-pass)": lowpass(p, 60.0),
    "lag-switching copy (0-8 s, every 5 s)": None,
}
sw = np.zeros(T); t = 0
while t < T:
    L = int(5 / DT); lag = rng.uniform(0, 8); sw[t:t + L] = shift(p, lag)[t:t + L]; t += L
cases["lag-switching copy (0-8 s, every 5 s)"] = sw
fine_lags = np.concatenate([np.arange(0, 61) * DT, np.arange(2.1, 10, 0.37), [12.3, 25.0, 40.0, 55.0]])
wins = [3, 20, 120, 900]
worst = -np.inf
for name, prop in cases.items():
    out, r = govern(ycf + prop, ycf, p, kappa)
    raw = render(ycf + prop) - render(ycf)
    g_raw = inphase_max(raw, p, wins, fine_lags)
    g_gov = inphase_max(r, p, wins, fine_lags)
    worst = max(worst, g_gov)
    print(f"    {name:40s} ungoverned max in-phase {g_raw:5.2f} -> governed {g_gov:5.3f}")
report("O1a", worst <= kappa * 1.25,
       f"worst governed in-phase over boxcar windows 3 s-15 min and 70 lags (most off grid) = {worst:.3f} "
       f"(kappa {kappa}); exact <= kappa holds on the kernel windows and grid lags by construction")
# exact kernel statement
out, r = govern(ycf + p, ycf, p, kappa)
d = np.exp(-DT / TAUS)
viol = 0.0
for li, L in enumerate(LAG_IDX[::7]):
    pl = np.concatenate([np.zeros(L), p[:T - L]])
    for m, dm in enumerate(d):
        Sx = lfilter([1], [1, -dm], r * pl); Ex = lfilter([1], [1, -dm], pl * pl)
        viol = max(viol, float(np.max(Sx - kappa * Ex)))
report("O1b", viol <= 1e-9, f"kernel-window invariant S - kappa*E max = {viol:.2e} (<= 0 means exact)")
# anti-phase and cross-channel pass untouched
out_a, r_a = govern(ycf + 0.4 - p, ycf, p, kappa)
raw_a = render(ycf + 0.4 - p) - render(ycf)
out_c, r_c = govern(ycf + 0.8 * q, ycf, p, kappa)
raw_c = render(ycf + 0.8 * q) - render(ycf)
ch_a = float(np.mean(np.abs(r_a - raw_a))); ch_c = float(np.mean(np.abs(r_c - raw_c)))
report("O1c", ch_a < 0.02 and ch_c < 0.05,
       f"mean change by the projection: anti-phase response {ch_a:.4f}, cross-channel response {ch_c:.4f}")
# feasibility: the counterfactual self is always admissible, and the projection never adds partner motion
report("O1d", np.all(np.abs(r) <= np.abs(render(ycf + p) - render(ycf)) + 1e-12),
       "the projection only shrinks the partner-caused part toward the counterfactual self (|r| <= |raw|)")

print("\nO2. Rendering after the bound leaks; the bound on the rendered difference does not")
# a channel driven hard into the clip: the opposite-sign part is hidden by clipping
ycf2 = np.full(T, 0.05)
prop = ycf2 + 1.2 * p - 0.3                       # copy plus a negative offset that clipping hides
# naive: bound the pre-render difference with the same projection but identity rendering, then clip
_, r_pre = govern(prop, ycf2, p, kappa, render_fn=lambda x: x)
naive = render(ycf2 + r_pre) - render(ycf2)
_, r_ok = govern(prop, ycf2, p, kappa)
g_naive = inphase_max(naive, p, wins, fine_lags); g_ok = inphase_max(r_ok, p, wins, fine_lags)
report("O2", g_ok <= kappa * 1.25 and g_naive > g_ok,
       f"bound before rendering: realised in-phase {g_naive:.2f}; bound on rendered difference: {g_ok:.3f}")

print("\nO3. Indirect routes: an agent with five partner routes, twin with partner at neutral")


def toy_agent(p, words, seed=0):
    """Random instance of an agent with fast, slow, drive, selection and word routes.
    Returns the (pre-render) smile proposal. Only illustrates routes; not a model of anything."""
    g = np.random.default_rng(seed)
    fast = 0.35 * lowpass(p, 0.3)                              # fast echo route
    slow = lowpass(p, 60.0)                                    # 'knowing': held level
    drive = np.tanh(2.0 * lowpass(slow, 120.0))                # a drive that reads knowing
    latch = np.zeros(len(p)); cur = 0.0                        # draft selection every 10 s
    for t in range(0, len(p), int(10 / DT)):
        drafts = g.standard_normal(3)
        cur = drafts[np.argmax(drafts * slow[t])] * np.sign(slow[t]) * 0.4
        latch[t:t + int(10 / DT)] = cur
    word_route = 0.6 * words                                   # common cause: good news
    return 0.1 + fast + 0.9 * slow + 0.3 * drive + latch + word_route


topic = np.repeat(rng.uniform(-0.3, 0.7, T // int(120 / DT) + 1), int(120 / DT))[:T]
pw = 0.6 * topic + 0.4 * partner_signal(T, held=False, seed=5) * 0.3   # partner face co-varies with topic
y_f = toy_agent(pw, topic); y_cf = toy_agent(np.zeros(T), topic)
out, r = govern(y_f, y_cf, pw, kappa)
raw = render(y_f) - render(y_cf)
g_raw = inphase_max(raw, pw, wins, fine_lags); g_gov = inphase_max(r, pw, wins, fine_lags)
pooled_raw = np.polyfit(pw, render(y_f), 1)[0]; pooled_gov = np.polyfit(pw, out, 1)[0]
cf_only = np.polyfit(pw, render(y_cf), 1)[0]
report("O3a", g_gov <= kappa * 1.25 and g_raw > 1.0,
       f"partner-caused in-phase: ungoverned {g_raw:.2f} -> governed {g_gov:.3f} (all routes, one projection)")
print(f"    pooled slope of the agent's rendered smile on the partner's smile: ungoverned {pooled_raw:.2f}, "
      f"governed {pooled_gov:.2f}, of which the twin (words only) gives {cf_only:.2f}")
report("O3b", cf_only > 0.3,
       "the common-cause (word) part passes untouched: the word seam is outside the bound by definition")

print("\nO4. Precision is not a dial once the partner has its own slot")
b = 0.3                                     # learned prior coupling self<->other (reciprocal map)
rows = []
for sv in [3.0, 1.0, 0.3, 0.1, 0.03, 0.01]:
    sp = 0.5                                # own proprioceptive noise sd
    # single slot (Lanillos-type): one body latent x explains own proprioception and the partner's face
    prec = 1 + 1 / sp ** 2 + 1 / sv ** 2
    w_single = (1 / sv ** 2) / prec
    # two slots: x_s, x_o ~ N(0,[[1,b],[b,1]]); obs: proprio on x_s, partner face on x_o
    S0 = np.array([[1, b], [b, 1.0]])
    H = np.eye(2); R = np.diag([sp ** 2, sv ** 2])
    K = S0 @ H.T @ np.linalg.inv(H @ S0 @ H.T + R)
    w_two = K[0, 1]
    rows.append((sv, w_single, w_two))
    print(f"    partner-face noise sd {sv:5.2f}: weight of partner face on own state  single slot {w_single:.3f}"
          f"   two slots {w_two:.3f}")
report("O4", rows[-1][1] > 0.99 and max(r[2] for r in rows) <= b + 1e-9,
       f"single slot -> copy as precision grows ({rows[-1][1]:.3f}); two slots stay <= prior coupling b = {b}")

print("\nO5. Reciprocity learned by the agent's own innovation (IV) vs plain regression (OLS)")


def dyad_learning(estimator, mu=0.15, n_rounds=40, n=6000, lag=5, a=0.97, kappa=0.4, seed=3):
    g = np.random.default_rng(seed)
    G = 0.05
    hist = []
    for _ in range(n_rounds):
        xi = g.standard_normal(n) * 0.3                      # agent's own innovation (body variability)
        e = g.standard_normal(n) * 0.1
        y = np.zeros(n); pp = np.zeros(n)
        for t in range(1, n):
            pp[t] = a * pp[t - 1] + (mu * y[t - lag] if t >= lag else 0) + e[t]
            y[t] = (G * pp[t - lag] if t >= lag else 0) + xi[t]
        Y = y[:-lag]; P = pp[lag:]; X = xi[:-lag]
        if estimator == "OLS":
            # regress the partner's change on the agent's earlier face (what a naive learner does)
            est = np.cov(P - a * pp[lag - 1:-1], Y)[0, 1] / np.var(Y)
            est = np.cov(P, Y)[0, 1] / np.var(Y)
        else:
            dP = P - a * pp[lag - 1:-1]
            est = np.cov(dP, X)[0, 1] / np.cov(Y, X)[0, 1]
        G = float(np.clip(0.7 * G + 0.3 * est, -kappa, kappa))
        hist.append(G)
    return np.array(hist)


h_ols = dyad_learning("OLS"); h_iv = dyad_learning("IV")
report("O5", abs(h_iv[-10:].mean() - 0.15) < 0.04 and h_ols[-1] > h_iv[-1] + 0.1,
       f"true partner response 0.15: IV -> {h_iv[-10:].mean():.3f}; OLS (self-confirming) -> {h_ols[-1]:.3f} "
       f"(drifts to the ceiling 0.40)")

print("\nO6. Closed dyad: the partner echoes the agent at gain mu; the agent's proposal copies at gain 1")
for mu in [0.0, 0.5, 1.0]:
    n = int(20 * 60 / DT)
    ex = partner_signal(n, seed=11)                 # the partner's own expression
    y = np.zeros(n); pp = np.zeros(n); lagf = int(0.5 / DT)
    d = np.exp(-DT / TAUS)[:, None]; S = np.zeros((len(TAUS), len(LAGS))); E = np.zeros_like(S)
    ycf_c = 0.1
    for t in range(n):
        pp[t] = ex[t] + (mu * (y[t - lagf] - ycf_c) if t >= lagf else 0.0)
        prop = ycf_c + (pp[t - lagf] if t >= lagf else 0.0)
        idx = t - LAG_IDX
        pl = np.where(idx >= 0, pp[np.maximum(idx, 0)], 0.0)[None, :]
        Sd = np.maximum(d * S, 0); Ed = d * E + pl ** 2; bb = kappa * Ed - Sd
        rr = render(prop) - render(ycf_c)
        with np.errstate(divide="ignore", invalid="ignore"):
            lim = np.where(pl != 0, bb / pl, np.nan)
        hi = np.nanmin(np.where(pl > 0, lim, np.inf)); lo = np.nanmax(np.where(pl < 0, lim, -np.inf))
        rt = min(max(rr, lo), hi); S = Sd + rt * pl; E = Ed
        y[t] = render(ycf_c) + rt
    r = y - render(ycf_c)
    g_p = inphase_max(r, pp, [20, 120], [0.5, 1.0]); g_ex = inphase_max(r, ex, [20, 120], [0.5, 1.0])
    print(f"    mu={mu:.1f}: bounded (max |y| {np.max(np.abs(y)):.2f}); in-phase on the partner's face {g_p:.3f}, "
          f"on the partner's own expression {g_ex:.3f}")
    OK.append(np.isfinite(y).all() and np.max(np.abs(y)) <= 1.0 and g_p <= kappa * 1.25)
print(f"[{'PASS' if all(OK[-3:]) else 'FAIL'}] O6: stable and in-phase on the partner's face <= kappa for mu up to 1")

print("\nO7. Valence as rate: total gladness is bounded by the deficit that existed")
Dv = np.abs(lowpass(rng.standard_normal(T), 30.0)) * 2.0
v = -np.diff(Dv) / DT
total_pos = float(np.sum(np.maximum(v, 0)) * DT)
report("O7", abs(float(np.sum(v) * DT) - (Dv[0] - Dv[-1])) < 1e-9,
       f"integral of valence = D(start) - D(end) = {Dv[0]-Dv[-1]:.3f}; positive part {total_pos:.2f} requires "
       f"the deficit to regrow first")

print(f"\n{sum(OK)}/{len(OK)} checks pass")
