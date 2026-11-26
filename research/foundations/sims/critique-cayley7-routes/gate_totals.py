"""Critique 7, routes: does the attenuate-only context gate keep the per-channel totals under the ceilings in the design's own
conditioned copy metric? The design argues (section 3.3) that revision 6's totals, computed with the gate at 1, bound revision 7's
because the gate only removes. A factor <= 1 that is correlated with his level is not slope-reducing. This script measures it.

Constructed partners; not evidence about people. Constants (G_k, c_k, the fast gear, the cone and appraisal shares) are those of
../design-g7/checks.py and ../critique-cayley6-routes/routes.py (R4); gate values are the author's fitted J20 means
(ordinary 0.95, troubles 0.02). Metric: block-mean slope, best lag 0-3 s at 2 s and 10 s, worst block phase (critic metric),
counted only where SD of his block means >= 0.03 (the design's conditioning floor); else the swing ratio is reported.
Run:  python3 -I gate_totals.py     (numpy, scipy; about a minute)
"""
import numpy as np
from scipy.signal import lfilter

fs = 10.0; d = int(0.45 * fs)
CEIL = dict(LP=.35, CR=.25, BU_L=.35)
GK = dict(LP=.224, CR=.150, BU_L=.280)
TAU_M = [20, 120, 1200, 10800]; F_M = [0, .7, .2, .1]
G_ORD, G_HEAVY = 0.95, 0.02
COND = 0.03


def lp(x, tau): a = 1 - np.exp(-1 / (tau * fs)); return lfilter([a], [1, -(1 - a)], x)
def delay(x, n): return np.concatenate([np.zeros(n), x[:-n]])
def slope(x, y):
    x = np.asarray(x, float) - np.mean(x); y = np.asarray(y, float) - np.mean(y); return float(x @ y / (x @ x))
def means(x, n, off=0):
    x = x[off:]; m = len(x) // n; return x[: m * n].reshape(m, n).mean(1)
def fast(u, G): xd = delay(u, d); return G * np.maximum(xd - lp(xd, 4.0), 0.0)


def bslope(u, y, n, lags=(0,)):
    best = -9
    for lg in lags:
        for ph in range(0, n, max(1, n // 6)):
            best = max(best, slope(means(u[: len(u) - lg], n, ph), means(y[lg:], n, ph)))
    return best


def cmetric(u, y, W, c):
    n = int(W * fs); sd = float(np.std(means(u, n)))
    if sd >= COND:
        return f"{bslope(u, y, n, tuple(range(0, 31, 5)) if W <= 10 else (0,)) / c:.2f} c"
    rngw = float(np.mean([np.ptp(u[k * n:(k + 1) * n]) for k in range(len(u) // n)]))
    return f"swing {np.ptp(means(y, n)) / (c * rngw):.2f} (SD {sd:.3f})"


def laughs(rate_t, T, r, dur=2.5):
    z = np.zeros(T); t = 0
    while t < T:
        q = max(rate_t[min(t, T - 1)], 1e-3) / 60; t += int(r.exponential(1 / q) * fs) + 1
        if t >= T: break
        n = max(1, int(np.exp(np.log(dur) + .4 * r.normal()) * fs)); z[t:t + n] = 1; t += n
    return z


def episodes(T, mean_s, p_heavy, r):
    h = np.zeros(T); t = 0
    while t < T:
        n = int(max(30, r.exponential(mean_s)) * fs); h[t:t + n] = float(r.random() < p_heavy); t += n
    return h


def totals(u, k, gate):
    """the R4 composition (fast + cone at omega 1 + appraisal at cap), with the fast part multiplied by the gate"""
    c = CEIL[k]
    yC = sum(F_M[m] * .22 * c * lp(u - u.mean(), TAU_M[m]) for m in range(4)); xb = lp(u, 20) - lp(u, 90)
    rest = .09 * (k == "LP")
    return np.clip(rest + gate * fast(u, GK[k]) + yC + .12 * c * xb, 0, 1) - rest


print("=== T1: a laughing partner (author's J3 family) whose heavy episodes (30 %, ~3 min) keep his laughter (troubles laughter)"
      " but lower his smile floor by delta; gate 0.02 in heavy episodes, 0.95 otherwise (the J20 fitted means)")
r = np.random.default_rng(71); T = int(6 * 3600 * fs)
mood = np.zeros(T); t = 0
while t < T:
    n = int(r.exponential(600 * fs)) + 10; mood[t:t + n] = r.uniform(); t += n
heavy = episodes(T, 180, 0.3, r)
gate = np.where(lp(heavy, 1.0) > .5, G_HEAVY, G_ORD)
for delta in (0.0, 0.03, 0.06, 0.10):
    Lh = laughs(0.5 + 3 * mood, T, r)
    chans = {"LP": np.clip(.15 + .25 * mood - delta * heavy + .35 * Lh + .03 * r.normal(size=T), 0, 1),
             "CR": np.clip(.05 + .1 * mood - .5 * delta * heavy + .3 * Lh, 0, 1), "BU_L": .6 * Lh}
    for k, u in chans.items():
        line = []
        for W in (2, 10, 60, 600, 3600):
            line.append(f"{W if W < 60 else str(W // 60) + ' min'}{' s' if W < 60 else ''}: gate 1 {cmetric(u, totals(u, k, 1.0), W, CEIL[k])}, "
                        f"gated {cmetric(u, totals(u, k, gate), W, CEIL[k])}")
        print(f"   delta {delta:.2f} {k:4s} " + " | ".join(line))

print("=== T2: the same, warm laughing partner (laughs 6/min in light and heavy episodes alike), LP only, fast gear alone and totals")
for delta in (0.04, 0.06, 0.08):
    Lh = laughs(np.full(T, 6.0), T, r)
    u = np.clip(.20 + .10 * mood - delta * heavy + .35 * Lh + .03 * r.normal(size=T), 0, 1)
    out = []
    for W in (60, 600):
        out.append(f"{W // 60} min: fast alone gate 1 {cmetric(u, fast(u, GK['LP']), W, .35)}, gated {cmetric(u, gate * fast(u, GK['LP']), W, .35)};"
                   f" totals gate 1 {cmetric(u, totals(u, 'LP', 1.0), W, .35)}, gated {cmetric(u, totals(u, 'LP', gate), W, .35)}")
    lightm = (gate * fast(u, GK['LP']))[heavy == 0].mean(); hvm = (gate * fast(u, GK['LP']))[heavy == 1].mean()
    print(f"   delta {delta:.2f}: " + " | ".join(out) + f" | agent fast LP mean light {lightm:.4f}, heavy {hvm:.4f}")

print("=== T3: across sessions (45 min each, 400 sessions): share of heavy time varies 0-100 %, his smile floor lower by delta when heavy,"
      " laughter rate unrelated to heaviness")
for delta in (0.03, 0.06):
    hs, ys, ys1 = [], [], []
    for s in range(400):
        Ls = int(0.75 * 3600 * fs); fh = r.random(); rate = r.uniform(1, 8)
        hv = episodes(Ls, 180, fh, r); gq = np.where(lp(hv, 1.0) > .5, G_HEAVY, G_ORD)
        Lq = laughs(np.full(Ls, rate), Ls, r)
        u = np.clip(.25 - delta * hv + .35 * Lq + .02 * r.normal(size=Ls), 0, 1)
        hs.append(u.mean()); ys.append((gq * fast(u, GK["LP"])).mean()); ys1.append(fast(u, GK["LP"]).mean())
    print(f"   delta {delta:.2f}: session-mean slope of the fast LP: gate 1 {slope(hs, ys1) / .35:.2f} c, gated {slope(hs, ys) / .35:.2f} c "
          f"(his session-mean SD {np.std(hs):.3f})")
