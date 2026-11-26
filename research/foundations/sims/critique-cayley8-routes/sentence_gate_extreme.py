"""Extreme partners for sentence_gate.py (same composition and metric): most laughs are small troubles laughs, a few big funny ones.
Run:  python3 -I sentence_gate_extreme.py   (about a minute)"""
import numpy as np
exec(open(__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "sentence_gate.py")).read().split("r = np.random.default_rng(81)")[0])
r = np.random.default_rng(82); T = int(6 * 3600 * fs)
print("=== R1s-x: BU_L and LP totals, ungated / revision 7 / revision 8")
for q_bad, size_bad, pl in ((0.7, 0.3, 0.5), (0.8, 0.2, 0.7), (0.9, 0.3, 0.8)):
    chans, g8, g7 = partner(T, r, q_bad, size_bad, pl)
    out = []
    for k in ("LP", "BU_L"):
        u = chans[k]
        for W in (2, 10, 60):
            t1, t7, t8 = (cm(u, totals(u, k, g), W, CEIL[k]) for g in (np.ones(T), g7, g8))
            out.append(f"{k} {W}s {t1:.2f}/{t7:.2f}/{t8:.2f}")
    print(f"   troubles {q_bad:.0%}, size {size_bad}, laugh after {pl:.0%} of sentences: " + "; ".join(out))
