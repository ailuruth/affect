"""Side item for the critique of design-commutator-coupling.md: the frozen Cayley-ledger shadow ledger (revision 7 form,
kept unchanged in 8.3) constrains lags 0-3 s at its 2-s window and only lag 0 at its 10-s and 60-s windows.
Its function is read verbatim from ../design-g7/checks.py at run time (between 'def ledger7' and 'def rend'),
as the revision-7 routes critic did.

K1: an UNCOUNTED within-session route that copies his channel at gain 1 with a pure delay L. What does the ledger
    leave, by the critics' metric (block-mean slope, lags 0-3 s) and by the same metric with lags 0-120 s?
K2: the COUNTED fast gear (frozen onset lobe, G 0.224, delay 0.45 s; the 0.80-s gated delay is the same shape) on a
    natural partner: its block-mean slope at lags 0-3 s against its best slope over lags 0-120 s (does any counted
    nonlinear route carry more toward slope at a lag the ledger does not scan?).
Constructed partners; mechanism exhibits only, not evidence about people.
Run:  python3 -I cayley_ledger_lag.py     (numpy, scipy; about 1 min)
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
exec(SRC[SRC.index("def ledger7"):SRC.index("def rend")], ns)
ledger7 = ns["ledger7"]


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


SHORT = tuple(range(0, 31, 5))                 # 0-3 s: the critics' metric and the ledger's 2-s scan
LONG = tuple(range(0, 1201, 10))               # 0-120 s in 1-s steps


def report(u, y):
    out = []
    for W in (2, 10, 60):
        s0, _ = bslope(u, y, int(W * fs), SHORT)
        s1, l1 = bslope(u, y, int(W * fs), LONG)
        out.append(f"W {W:>2} s: lag0-3s {s0:+.2f} | best lag0-120s {s1:+.2f} @ {l1:5.1f} s")
    return "; ".join(out)


c = 0.35
r = np.random.default_rng(910); T = int(2 * 3600 * fs)
m = blocks(T, 300, r); Lg = laughs(0.5 + 3 * m, T, r)
u = np.clip(.15 + .25 * m + .35 * lp(Lg, 0.5) + .02 * r.normal(size=T), 0, 1)
print(f"partner: smile level in mood blocks (mean 5 min) plus laughs; 2 h at {fs:.0f} Hz; ceiling c = {c} (lip pull)")
print("K1  uncounted route = gain-1 copy of his channel delayed by L (centred at his session mean); after the ledger")
for L in (0, 2, 5, 10, 20, 40, 90):
    x = delay(u, L * fs) - u.mean()
    o, h, gr, fl = ledger7(u, x, c)
    print(f"   L {L:>3} s: frames changed {h:.2f}; rms out/in {np.std(o)/np.std(x):.2f}; {report(u, o)}")
print("K1b the same with a livelier partner (mood blocks of mean 30 s instead of 5 min)")
m2 = blocks(T, 30, r); Lg2 = laughs(0.5 + 3 * m2, T, r)
u2 = np.clip(.15 + .25 * m2 + .35 * lp(Lg2, 0.5) + .02 * r.normal(size=T), 0, 1)
for L in (0, 10, 20, 40, 90):
    x = delay(u2, L * fs) - u2.mean()
    o, h, gr, fl = ledger7(u2, x, c)
    print(f"   L {L:>3} s: frames changed {h:.2f}; rms out/in {np.std(o)/np.std(x):.2f}; {report(u2, o)}")
print("K2  counted fast gear (G 0.224, onset lobe), no ledger: is the toward slope larger at a lag the ledger does not scan?")
for dl in (0.45, 0.80):
    print(f"   delay {dl:.2f} s: {report(u, fast(u, 0.224, dl))}")
print(f"done in {time.time() - T0:.0f} s")
