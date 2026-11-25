"""Regenerates out/es_paired_exploratory.txt: exploratory paired per-seed log ratios for ES2b and ES3 (not pre-registered)."""
import json, math, statistics as st
b = json.load(open("out/es2b.json")); c = json.load(open("out/es3.json")); lines = []
def paired(x, y, name):
    lr = [math.log(a / b_) for a, b_ in zip(x, y) if a > 0 and b_ > 0]; n = len(lr); m = st.mean(lr); se = st.stdev(lr) / math.sqrt(n)
    lines.append(f"{name}: n={n} median ratio={math.exp(st.median(lr)):.3f} geo-mean ratio={math.exp(m):.3f} (95% CI {math.exp(m-1.96*se):.3f}-{math.exp(m+1.96*se):.3f}) seeds where first arm lower: {sum(v < 0 for v in lr)}/{n}")
for w in ("companion", "random"):
    paired(b[f"{w}/nomem"]["costs"], b[f"{w}/rr_nomem"]["costs"], f"ES2b {w}: Costate vs Robust reg.")
    paired(c[f"{w}/nomem_rw"]["costs"], c[f"{w}/rr_nomem"]["costs"], f"ES3  {w}: Costate-rw vs Robust reg.")
open("out/es_paired_exploratory.txt", "w").write("\n".join(lines) + "\n")
