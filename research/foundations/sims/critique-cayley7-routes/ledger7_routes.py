"""Critique 7, routes: the revision-7 shadow ledger (attenuate-only clamp, deviation floor, b < 0 held at 0).
Its function is read verbatim from ../design-g7/checks.py at run time (between 'def ledger7' and 'def rend').

L1: an injected toward route at 2 s plus a declared away route at 1 min (counter-mimicry). The ledger's hold writes 0 for the
    whole partner-caused part whenever any constraint is over budget. Does zeroing the away part manufacture a toward slope
    at the slower windows?
L2: a high-gain copy of his small deviations, on a partner who sits near his own mean most of the time and laughs big now and
    then (the deviation floor skips every constraint while |pi| < 0.10 of its 30-min RMS).
L3: the ledger on the counted routes of a natural partner, gated (does it change anything the design counts).
Constructed partners; not evidence about people.
Run:  python3 -I ledger7_routes.py     (numpy, scipy; several minutes)
"""
import os
import numpy as np
from scipy.signal import lfilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, "..", "design-g7", "checks.py")).read()
fs = 10.0; d = int(0.45 * fs); LEDGER_FLOOR = 0.10
ns = {"np": np, "fs": fs, "LEDGER_FLOOR": LEDGER_FLOOR}
exec(SRC[SRC.index("def ledger7"):SRC.index("def rend")], ns)
ledger7 = ns["ledger7"]


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
def rend(x): return np.clip(x, -0.09, 0.91)
def f4(u, y): return [bslope(u, y, int(W * fs), tuple(range(0, 31, 5)) if W <= 10 else (0,)) for W in (2, 10, 60, 600)]
def fmt(v): return "/".join(f"{x:+.2f}" for x in v)


def laughs(rate_t, T, r, dur=2.5):
    z = np.zeros(T); t = 0
    while t < T:
        q = max(rate_t[min(t, T - 1)], 1e-3) / 60; t += int(r.exponential(1 / q) * fs) + 1
        if t >= T: break
        n = max(1, int(np.exp(np.log(dur) + .4 * r.normal()) * fs)); z[t:t + n] = 1; t += n
    return z


def blocks(T, L, r):
    x = np.zeros(T); t = 0
    while t < T:
        n = int(r.exponential(L * fs)) + 10; x[t:t + n] = r.uniform(); t += n
    return x


c = .35
print("=== L1: injected toward route (the J7 recipe's fast part, 1.6 x his onset) plus a declared away route at 1 min (-k x lp60 of his"
      " centred level); slopes 2 s / 10 s / 1 min / 10 min, rendered; c = 0.35")
for seed in range(2):
    for k_away in (0.3, 0.6):
        r = np.random.default_rng(500 + seed); T = int(4 * 3600 * fs); m = blocks(T, 600, r); L = laughs(0.5 + 3 * m, T, r)
        u = np.clip(.15 + .25 * m + .35 * L + .03 * r.normal(size=T), 0, 1)
        x = fast(u, .224) + 1.6 * fast(u, 1.0) - k_away * lp(u - u.mean(), 60)
        x = np.clip(.09 + x, 0, 1) - .09
        o, h, gr, fl = ledger7(u, x, c)
        a0, a1 = f4(u, x), f4(u, rend(o))
        away0 = f4(u, np.clip(.09 - k_away * lp(u - u.mean(), 60), 0, 1) - .09)
        print(f"   seed {seed}, away gain {k_away}: before {fmt(a0)}; after ledger {fmt(a1)}; away route alone {fmt(away0)}; "
              f"frames changed {h:.3f}, |out|>|in| {gr:.4f}, flips {fl:.4f}")

print("=== L2: a partner near his own mean most of the time (micro-smiles, SD 0.02) with a big laugh every ~4 min; an uncounted route"
      " copies his 2-s deviation from his 30-min mean at gain g, saturating at +-0.15")
for seed in range(2):
    for gain in (1.0, 3.0):
        r = np.random.default_rng(600 + seed); T = int(4 * 3600 * fs)
        micro = lp(r.normal(size=T), 8.0); micro = 0.02 * micro / micro.std()
        L = laughs(np.full(T, 0.25), T, r, dur=6.0)
        u = np.clip(.25 + micro + .55 * L, 0, 1)
        dev = lp(u, 2.0) - lp(u, 1800.0)
        x = np.clip(gain * dev, -.15, .15) + fast(u, .224)
        o, h, gr, fl = ledger7(u, x, c)
        quiet = lp(L, 3.0) < 1e-3
        qs = slope(means(np.where(quiet, u, np.nan)[quiet], 20), means(rend(o)[quiet], 20))
        qs0 = slope(means(u[quiet], 20), means(x[quiet], 20))
        print(f"   seed {seed}, gain {gain}: whole session before {fmt(f4(u, x))}, after {fmt(f4(u, rend(o)))}; "
              f"2-s slope within the quiet stretches (no laugh within ~10 s, {quiet.mean():.0%} of the time): before {qs0:.2f}, after {qs:.2f}; "
              f"frames changed {h:.3f}")
