"""Independent check of revision 9.1 (check-cayley-ledger-9.1.md), item 1: the 2 % residual at a 240-s delay.
Reuses ../design-g9/ledger_lag120.py's definitions and partners verbatim (as ../design-g91/ledger_margin.py does).
Usage: python3 -I ledger_close.py KAPPA SCAN LAGS PARTNERS K2
  KAPPA    uniform ledger target kappa*c on every channel, window and lag
  SCAN     'base' = revision 9.1's 61 keys (2-s window lags 0-3 s, 10-s 0-120 s, 60-s 0-300 s);
           'w10'  = base + the 10-s window scanned 125-300 s in 5-s steps (36 more keys)
  LAGS     comma list of copy delays (s); PARTNERS '5', '30' or '5,30' (mood-block length, s x 60 or s); K2 1/0
Constructed partners: mechanism exhibits only, not evidence about people.
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
G9 = os.path.join(HERE, "..", "design-g9")
src = open(os.path.join(G9, "ledger_lag120.py")).read()
src = src[: src.index('print(f"partners')].replace("HERE = os.path.dirname(os.path.abspath(__file__))", f"HERE = {G9!r}")
g = {"__name__": "defs"}; exec(src, g)
T0 = time.time()
ledger9, delay, fmt, worst, fast, lp = (g[k] for k in ("ledger9", "delay", "fmt", "worst", "fast", "lp"))
c, fs = g["c"], g["fs"]
kappa = float(sys.argv[1]); scan = sys.argv[2]
LS = [int(v) for v in sys.argv[3].split(",")]
P = {"5": ("mood blocks 5 min", g["u"]), "30": ("mood blocks 30 s", g["u2"])}
parts = [P[p] for p in sys.argv[4].split(",")]; k2 = sys.argv[5] == "1"
KEYS = ([(2.0, l) for l in (0.0, 0.5, 1.0, 2.0, 3.0)] + [(10.0, float(l)) for l in range(0, 121, 5)]
        + [(60.0, float(l)) for l in range(0, 301, 10)])
if scan == "w10": KEYS += [(10.0, float(l)) for l in range(125, 301, 5)]
print(f"kappa {kappa}, scan {scan} ({len(KEYS)} keys); ratio = worst block-mean slope over lags 0-300 s / c")
for name, uu in parts:
    for L in LS:
        x = delay(uu, L * fs) - uu.mean()
        o, h, gr, fl = ledger9(KEYS, uu, x, kappa * c)
        ws = worst(uu, o, 300); mx = max(s for s, _ in ws)
        print(f"  K1 {name:<17} L {L:>3} s | {fmt(ws)} | max/c {mx / c:.3f} | changed {h:.2f} grow {gr:.3f} flip {fl:.3f}", flush=True)
if k2:
    for name, uu in parts:
        y = fast(uu, 0.224, 0.45) + 0.22 * c * lp(uu - uu.mean(), 120.0)
        o, h, _, _ = ledger9(KEYS, uu, y, kappa * c)
        print(f"  K2 {name:<17} counted routes frames changed {h:.3f} | after {fmt(worst(uu, o, 300))}", flush=True)
print(f"done in {time.time() - T0:.0f} s")
