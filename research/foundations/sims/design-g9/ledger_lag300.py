"""Option for revision 9: also scan the 60-s window to 300 s (10-s steps), so that copies delayed 150-240 s are held too.
Reuses the definitions and partners of ledger_lag120.py (its text up to its first print, executed here), and adds one
key set. N3b: the copies delayed 150 s and 240 s; N2b: the counted routes (fast gear, held 2-min route) untouched?
Run:  python3 -I ledger_lag300.py > ledger_lag300.out.txt     (a few minutes)
"""
import os, time
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "ledger_lag120.py")).read()
src = src[: src.index('print(f"partners')].replace("HERE = os.path.dirname(os.path.abspath(__file__))", f"HERE = {HERE!r}")
g = {"__name__": "ledger_lag120_defs"}
exec(src, g)
T0 = time.time()
KEYS = ([(2.0, l) for l in (0.0, 0.5, 1.0, 2.0, 3.0)] + [(10.0, float(l)) for l in range(0, 121, 5)]
        + [(60.0, float(l)) for l in range(0, 301, 10)])
ledger9, delay, fmt, worst, fast, lp = (g[k] for k in ("ledger9", "delay", "fmt", "worst", "fast", "lp"))
u, u2, c, fs = g["u"], g["u2"], g["c"], g["fs"]
print(f"keys {len(KEYS)}: 2-s window lags 0-3 s; 10-s window 0-120 s; 60-s window 0-300 s")
print("N3b uncounted gain-1 copy delayed by L (worst slope over lags 0-300 s)")
for name, uu in (("mood blocks 5 min", u), ("mood blocks 30 s", u2)):
    for L in (90, 150, 240):
        x = delay(uu, L * fs) - uu.mean()
        o, h, gr, fl = ledger9(KEYS, uu, x, c)
        print(f"   {name:<17} L {L:>3} s | {fmt(worst(uu, o, 300))} | frames changed {h:.2f}, grow {gr:.3f}, flip {fl:.3f}",
              flush=True)
print("N2b counted routes (frames changed)")
for name, uu in (("mood blocks 5 min", u), ("mood blocks 30 s", u2)):
    y = fast(uu, 0.224, 0.45) + 0.22 * c * lp(uu - uu.mean(), 120.0)
    o, h, _, _ = ledger9(KEYS, uu, y, c)
    print(f"   {name:<17} fast gear + held 2-min route: frames changed {h:.3f} | after {fmt(worst(uu, o, 300))}", flush=True)
print(f"done in {time.time() - T0:.0f} s")
