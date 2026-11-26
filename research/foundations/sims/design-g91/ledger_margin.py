"""Revision 9.1 confirmation run (copy of sims/check-cayley9/ledger_margin.py, logic unchanged). Checker item 4: can the ledger's residual above c
(1.03-1.20 c at delays 0-120 s; 1.17-1.34 c at 150-240 s, block-mean metric) be closed by one uniform change,
with no situation-specific rule?  Candidate: the ledger enforces kappa*c instead of c on every channel and every
(window, lag) constraint (a uniform margin on the per-expression ceiling, the same for every situation).
Reuses ledger_lag120.py's definitions and partners verbatim (as ledger_lag300.py does), with revision 9's 61 keys.
K1: uncounted gain-1 delayed copies; K2: counted routes (fast gear 0.45 s + held 2-min route 0.22 c): frames changed.
Run (9.1):  python3 -I ledger_margin.py 0.70 > ledger_margin070.out.txt   (about 3 min; lags 10, 90, 120, 240 s)
      python3 -I ledger_margin.py 0.70 240 > ledger_margin070.out.txt   (about 1.5 min)
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
G9 = os.path.join(HERE, "..", "design-g9")
src = open(os.path.join(G9, "ledger_lag120.py")).read()
src = src[: src.index('print(f"partners')].replace("HERE = os.path.dirname(os.path.abspath(__file__))", f"HERE = {G9!r}")
g = {"__name__": "defs"}
exec(src, g)
T0 = time.time()
KEYS = ([(2.0, l) for l in (0.0, 0.5, 1.0, 2.0, 3.0)] + [(10.0, float(l)) for l in range(0, 121, 5)]
        + [(60.0, float(l)) for l in range(0, 301, 10)])
ledger9, delay, fmt, worst, fast, lp = (g[k] for k in ("ledger9", "delay", "fmt", "worst", "fast", "lp"))
u, u2, c = g["u"], g["u2"], g["c"]
kappa = float(sys.argv[1]) if len(sys.argv) > 1 else 0.80
LS = tuple(int(v) for v in sys.argv[2].split(",")) if len(sys.argv) > 2 else (10, 90, 120, 240)
print(f"61 keys; ledger target kappa*c = {kappa}*{c} = {kappa*c:.3f}; ceiling c = {c}; ratio = worst slope / c")
print("K1 uncounted gain-1 copy delayed by L (worst block-mean slope over lags 0-300 s at W 2/10/60 s)")
for name, uu in (("mood blocks 5 min", u), ("mood blocks 30 s", u2)):
    for L in LS:
        x = delay(uu, L * g["fs"]) - uu.mean()
        o, h, gr, fl = ledger9(KEYS, uu, x, kappa * c)
        ws = worst(uu, o, 300); mx = max(s for s, _ in ws)
        print(f"   {name:<17} L {L:>3} s | {fmt(ws)} | max/c {mx / c:.2f} | changed {h:.2f} grow {gr:.3f} flip {fl:.3f}",
              flush=True)
print("K2 counted routes (fast gear 0.45 s + held 2-min route 0.22 c), frames changed")
for name, uu in (("mood blocks 5 min", u), ("mood blocks 30 s", u2)):
    y = fast(uu, 0.224, 0.45) + 0.22 * c * lp(uu - uu.mean(), 120.0)
    o, h, _, _ = ledger9(KEYS, uu, y, kappa * c)
    print(f"   {name:<17} frames changed {h:.3f} | after {fmt(worst(uu, o, 300))}", flush=True)
print(f"done in {time.time() - T0:.0f} s")
