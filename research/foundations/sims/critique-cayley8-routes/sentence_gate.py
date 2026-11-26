"""Critique 8, routes, area 2 and 4: revision 8 gives the gate the CURRENT sentence's words at each laugh onset. The design keeps
the routes critic's revision-7 R1g numbers (measured with an episode-scale gate) and says the timing change 'keeps the gate's
per-episode values'. A gate that now differs sentence by sentence is correlated with each laugh, not with minutes. This measures R1g
again in the same composition and metric as critique 7's gate_totals.py.

Constructed partners; not evidence about people. Constants: G_k, c_k, the fast gear (onset lobe, 4-s low-pass), the cone and
appraisal shares (critique 6 R4 composition, as in critique-cayley7-routes/gate_totals.py); revision 8's 0.80-s delay on the gated
group; gate values the author's J36 numbers (ordinary end-of-sentence laugh 0.99; laugh ending a bad-news sentence 0.01-0.09, 0.05 used).
Metric: block-mean slope, best lag 0-3 s at 2 s and 10 s, worst block phase; counted where SD of his block means >= 0.03, else swing.
Run:  python3 -I sentence_gate.py     (numpy, scipy; about a minute)
"""
import numpy as np
from scipy.signal import lfilter

fs = 10.0; d8 = int(0.80 * fs)
CEIL = dict(LP=.35, CR=.25, BU_L=.35)
GK = dict(LP=.224, CR=.150, BU_L=.280)
TAU_M = [20, 120, 1200, 10800]; F_M = [0, .7, .2, .1]
COND = 0.03
G_ORD, G_BAD = 0.99, 0.05


def lp(x, tau): a = 1 - np.exp(-1 / (tau * fs)); return lfilter([a], [1, -(1 - a)], x)
def delay(x, n): return np.concatenate([np.zeros(n), x[:-n]])
def slope(x, y):
    x = np.asarray(x, float) - np.mean(x); y = np.asarray(y, float) - np.mean(y); return float(x @ y / (x @ x))
def means(x, n, off=0):
    x = x[off:]; m = len(x) // n; return x[: m * n].reshape(m, n).mean(1)
def fast(u, G, g):
    xd = delay(u, d8); return delay(g, d8) * G * np.maximum(xd - lp(xd, 4.0), 0.0)   # g is indexed by HIS frame (source time)


def bslope(u, y, n, lags=(0,)):
    best = -9
    for lg in lags:
        for ph in range(0, n, max(1, n // 6)):
            best = max(best, slope(means(u[: len(u) - lg], n, ph), means(y[lg:], n, ph)))
    return best


def cm(u, y, W, c):
    n = int(W * fs); sd = float(np.std(means(u, n)))
    if sd >= COND:
        return bslope(u, y, n, tuple(range(0, 31, 5)) if W <= 10 else (0,)) / c
    return float("nan")


def totals(u, k, g):
    c = CEIL[k]
    yC = sum(F_M[m] * .22 * c * lp(u - u.mean(), TAU_M[m]) for m in range(4)); xb = lp(u, 20) - lp(u, 90)
    rest = .09 * (k == "LP")
    return np.clip(rest + fast(u, GK[k], g) + yC + .12 * c * xb, 0, 1) - rest


def partner(T, r, q_bad, size_bad, p_laugh=0.5):
    """he talks in sentences (3 s lognormal, 1 s gaps); after a share p_laugh of them he laughs (2.5 s lognormal).
    A share q_bad of his sentences carry bad news / troubles; a laugh after one is size_bad times an ordinary laugh.
    Returns his LP, CR, BU_L and the per-frame gate for each source frame: revision 8 = the current sentence's words;
    revision 7 = the previous sentence's words (latched after the utterance); 1 = ungated."""
    mood = np.zeros(T); t = 0
    while t < T:
        n = int(r.exponential(600 * fs)) + 10; mood[t:t + n] = r.uniform(); t += n
    L = np.zeros(T); g8 = np.ones(T); g7 = np.ones(T); t = 0; prev_bad = False
    while t < T:
        n = int(np.exp(np.log(3.0) + .4 * r.normal()) * fs); bad = r.random() < q_bad
        g8[t:t + n] = G_BAD if bad else G_ORD; g7[t:t + n] = G_BAD if prev_bad else G_ORD; t += n
        if r.random() < p_laugh and t < T:
            m = max(2, int(np.exp(np.log(2.5) + .4 * r.normal()) * fs)); a = size_bad if bad else 1.0
            L[t:t + m] = a; g8[t:t + m] = G_BAD if bad else G_ORD; g7[t:t + m] = G_BAD if prev_bad else G_ORD; t += m
        gap = int(r.exponential(1.0) * fs) + 3; g8[t:t + gap] = G_BAD if bad else G_ORD; g7[t:t + gap] = G_BAD if bad else G_ORD
        t += gap; prev_bad = bad
    chans = {"LP": np.clip(.15 + .25 * mood + .35 * L + .03 * r.normal(size=T), 0, 1),
             "CR": np.clip(.05 + .1 * mood + .3 * L, 0, 1), "BU_L": .6 * L}
    return chans, g8[:T], g7[:T]


r = np.random.default_rng(81); T = int(6 * 3600 * fs)
print("=== R1s: per-channel slope (in c_k) of the fast gear alone and of the totals; ungated / revision-7 timing (previous sentence) / "
      "revision-8 timing (current sentence)")
for q_bad, size_bad in ((0.3, 1.0), (0.3, 0.5), (0.5, 0.5), (0.3, 0.3)):
    chans, g8, g7 = partner(T, r, q_bad, size_bad)
    print(f"-- {int(q_bad * 100)} % of his sentences are troubles; a laugh after one is {size_bad:.1f} x an ordinary laugh")
    for k, u in chans.items():
        row = []
        for W in (2, 10, 60):
            f1, f7, f8 = (cm(u, fast(u, GK[k], g), W, CEIL[k]) for g in (np.ones(T), g7, g8))
            t1, t7, t8 = (cm(u, totals(u, k, g), W, CEIL[k]) for g in (np.ones(T), g7, g8))
            row.append(f"{W if W < 60 else '1 min'}{' s' if W < 60 else ''}: fast {f1:.2f}/{f7:.2f}/{f8:.2f}, totals {t1:.2f}/{t7:.2f}/{t8:.2f}")
        print(f"   {k:4s} " + " | ".join(row))
    # the level bound W' (instantaneous / window) still holds: max over 2-s blocks of mean(agent fast) - G mean(his delayed)
    u = chans["BU_L"]; n = int(2 * fs); y = fast(u, GK["BU_L"], g8)
    print(f"   W' check BU_L: max over 2-s blocks of mean(y_fast) - G mean(u delayed) = {np.max(means(y, n) - GK['BU_L'] * means(delay(u, d8), n)):+.4f} (<= 0 holds)")
