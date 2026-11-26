"""Revision 9 (build core) of design-cayley-ledger.md: the shadow ledger scans lags to 120 s (D90; the Cayley side item
of critique-design-commutator-coupling-routes.md).

ledger9 is ledger7 (read verbatim from ../design-g7/checks.py, between 'def ledger7' and 'def rend') with one change:
the set of (window, lag) constraints. Revision 7 / 8.3 scan lags 0, 0.5, 1, 2, 3 s at the 2-s window and lag 0 at 10 s
and 60 s. Revision 9 adds lags 0-120 s in 5-s steps at the 10-s window and 0-120 s in 10-s steps at the 60-s window
(each step at most half its window). Every constraint is the same attenuate-only rule as before.

N1: an UNCOUNTED route copying his channel at gain 1 with a pure delay L (the side item's K1 and K1b partners):
    what ledger7 and ledger9 leave, by the block-mean metric with lags 0-120 s (and 0-180 s for L = 120 s).
N3: the scan's limit: copies delayed 150 s and 240 s.
N2: COUNTED routes on a natural partner, through ledger9: the frozen fast gear at 0.45 s (D81 fast partial mimicry,
    G 0.224 on lip pull) and a held cone-like route (2-min low-pass of his deviation at 0.22 c): how many frames does
    the extended scan change? (It should change none or almost none: their toward slopes are below c at every lag.)
Constructed partners; mechanism exhibits only, not evidence about people.
Run:  python3 -I ledger_lag120.py > ledger_lag120.out.txt     (numpy, scipy; a few minutes)
"""
import os
import time
import numpy as np
from scipy.signal import lfilter

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, "..", "design-g7", "checks.py")).read()
fs = 10.0; LEDGER_FLOOR = 0.10
ns = {"np": np, "fs": fs, "LEDGER_FLOOR": LEDGER_FLOOR}
body = SRC[SRC.index("def ledger7"):SRC.index("def rend")]
exec(body, ns)
ledger7 = ns["ledger7"]
# ledger9: the same function text, with the key set taken from an argument instead of 'lags only at the 2-s window'.
body9 = body.replace("def ledger7(", "def ledger9(KEYS, ").replace(
    "keys = [(Wd, l) for Wd in wins for l in (lags if Wd <= 2.0 else (0.0,))]", "keys = list(KEYS)")
assert body9 != body and "keys = list(KEYS)" in body9
exec(body9, ns)
ledger9 = ns["ledger9"]
KEYS9 = ([(2.0, l) for l in (0.0, 0.5, 1.0, 2.0, 3.0)] + [(10.0, float(l)) for l in range(0, 121, 5)]
         + [(60.0, float(l)) for l in range(0, 121, 10)])


def lp(x, tau): a = 1 - np.exp(-1 / (tau * fs)); return lfilter([a], [1, -(1 - a)], x)
def delay(x, n):
    n = int(n); return x.copy() if n <= 0 else np.concatenate([np.full(n, x[0]), x[:-n]])
def slope(x, y):
    x = np.asarray(x, float) - np.mean(x); y = np.asarray(y, float) - np.mean(y); return float(x @ y / (x @ x))
def means(x, n, off=0):
    x = x[off:]; m = len(x) // n; return x[: m * n].reshape(m, n).mean(1)
def fast(u, G, dl=0.45): xd = delay(u, dl * fs); return G * np.maximum(xd - lp(xd, 4.0), 0.0)
def bslope(u, y, n, lags=(0,)):
    best, bl = -9, 0
    for lg in lags:
        for ph in range(0, n, max(1, n // 6)):
            s = slope(means(u[: len(u) - lg] if lg else u, n, ph), means(y[lg:], n, ph))
            if s > best: best, bl = s, lg
    return best, bl / fs


def blocks(T, L, r):
    x = np.zeros(T); t = 0
    while t < T:
        n = int(r.exponential(L * fs)) + 10; x[t:t + n] = r.uniform(); t += n
    return x


def laughs(rate_t, T, r, dur=2.5):
    z = np.zeros(T); t = 0
    while t < T:
        q = max(rate_t[min(t, T - 1)], 1e-3) / 60; t += int(r.exponential(1 / q) * fs) + 1
        if t >= T: break
        n = max(1, int(np.exp(np.log(dur) + .4 * r.normal()) * fs)); z[t:t + n] = 1; t += n
    return z


def worst(u, y, maxlag_s=120):
    lags = tuple(range(0, int(maxlag_s * fs) + 1, 10))
    return [bslope(u, y, int(W * fs), lags) for W in (2, 10, 60)]


def fmt(ws): return " ".join(f"W{W:>2}s {s:+.2f}@{l:4.0f}s" for W, (s, l) in zip((2, 10, 60), ws))


c = 0.35
r = np.random.default_rng(910); T = int(2 * 3600 * fs)
m = blocks(T, 300, r); Lg = laughs(0.5 + 3 * m, T, r)
u = np.clip(.15 + .25 * m + .35 * lp(Lg, 0.5) + .02 * r.normal(size=T), 0, 1)
m2 = blocks(T, 30, r); Lg2 = laughs(0.5 + 3 * m2, T, r)
u2 = np.clip(.15 + .25 * m2 + .35 * lp(Lg2, 0.5) + .02 * r.normal(size=T), 0, 1)
print(f"partners as the side item (seed 910): 2 h at {fs:.0f} Hz; ceiling c = {c} (lip pull); ledger9 keys {len(KEYS9)}")
print("N1  uncounted gain-1 copy delayed by L; worst block-mean slope over lags 0-120 s (0-180 s for L 120) at W 2/10/60 s")
for name, uu, Ls in (("mood blocks 5 min", u, (0, 10, 20, 40, 90, 120)), ("mood blocks 30 s", u2, (0, 10, 20, 40, 90, 120))):
    for L in Ls:
        x = delay(uu, L * fs) - uu.mean()
        mx = 180 if L >= 120 else 120
        o7, h7, _, _ = ledger7(uu, x, c)
        o9, h9, g9, f9 = ledger9(KEYS9, uu, x, c)
        print(f"   {name:<17} L {L:>3} s | ledger7: {fmt(worst(uu, o7, mx))} | ledger9: {fmt(worst(uu, o9, mx))}"
              f" | ledger9 grow {g9:.3f} flip {f9:.3f}", flush=True)
print("N2  counted routes on the natural partners, through ledger9 (frames changed; worst slope 0-120 s before -> after)")
for name, uu in (("mood blocks 5 min", u), ("mood blocks 30 s", u2)):
    y_fast = fast(uu, 0.224, 0.45)
    y_cone = 0.22 * c * lp(uu - uu.mean(), 120.0)
    for rn, y in (("fast gear 0.45 s", y_fast), ("held 2-min route 0.22 c", y_cone), ("both", y_fast + y_cone)):
        o9, h9, _, _ = ledger9(KEYS9, uu, y, c)
        print(f"   {name:<17} {rn:<24} frames changed {h9:.3f} | before {fmt(worst(uu, y))} | after {fmt(worst(uu, o9))}",
              flush=True)
print("N3  beyond the scan: uncounted gain-1 copy delayed by 150 s or 240 s, ledger9 (worst slope over lags 0-300 s)")
for name, uu in (("mood blocks 5 min", u), ("mood blocks 30 s", u2)):
    for L in (150, 240):
        x = delay(uu, L * fs) - uu.mean()
        o9, h9, _, _ = ledger9(KEYS9, uu, x, c)
        print(f"   {name:<17} L {L:>3} s | ledger9: {fmt(worst(uu, o9, 300))} | frames changed {h9:.2f}", flush=True)
print(f"done in {time.time() - T0:.0f} s")
