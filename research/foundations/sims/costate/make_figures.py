"""Figures for the Costate toys, plotted from out/ (no result is recomputed except where noted)."""
import json, glob, sys
import numpy as np
sys.path.insert(0, ".."); from figstyle import setup, save, S1, S2, S3, TXT2
import matplotlib.pyplot as plt
setup()
# T1 vs T1b departure difference per seed
T1 = [json.loads(l) for f in sorted(glob.glob("out/t1_*.jsonl")) for l in open(f)]
T1b = [json.loads(l) for f in sorted(glob.glob("out/t1b_*.jsonl")) for l in open(f)]
fig, ax = plt.subplots(figsize=(5.5, 3.2))
for i, (rows, c, name) in enumerate([(T1, S1, "T1 model-free"), (T1b, S2, "T1b model-based")]):
    y = [r["diff"] for r in rows]; ax.scatter(np.full(len(y), i) + np.linspace(-0.12, 0.12, len(y)), y, color=c, s=18, label=name)
ax.axhline(0.254, color=TXT2, ls="--", lw=1); ax.text(1.35, 0.258, "analytic 0.254", va="bottom", color=TXT2, fontsize=8)
ax.axhline(0.10, color=TXT2, ls=":", lw=1); ax.text(1.35, 0.104, "threshold 0.10", va="bottom", color=TXT2, fontsize=8)
ax.set_xticks([0, 1]); ax.set_xticklabels(["T1 model-free", "T1b model-based"]); ax.set_xlim(-0.5, 1.9)
ax.set_ylabel("μ_bye − μ_brb at b = b*"); ax.set_title("Departure costate difference, 20 seeds each")
save(fig, "figs/t1_t1b_departure.png")
# C: mimicry gains vs formula
c = json.load(open("out/c.json")); s = np.array([0.1, 0.3, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]); ss = np.linspace(0, 2.1, 200)
fig, ax = plt.subplots(figsize=(5, 3.2))
ax.plot(ss, 4 * ss**2 / (4 + 4 * ss**2), color=S1, label="w s²/(c + w s²), w = 4, c = 4")
ax.scatter(s, c["CM1_gains"], color=S2, zorder=3, label="simulated steady-state gain")
ax.set_xlabel("singular value s of own face map"); ax.set_ylabel("mimicry gain"); ax.legend(loc="lower right"); ax.set_title("Mimicry as shrinkage onto the own repertoire")
save(fig, "figs/c_mimicry_gain.png")
# CS2 dose-response
d = json.load(open("out/cs2.json")); L = [-0.2, -0.1, 0, 0.1, 0.2]
fig, ax = plt.subplots(figsize=(5, 3.2))
ax.plot(L, d["derived"]["means"], "o-", color=S1, label="derived direction"); ax.plot(L, d["random"]["means"], "s-", color=S2, label="random direction")
ax.set_xlabel("steering strength s"); ax.set_ylabel("coupling score (mean |Fisher z|)"); ax.legend(); ax.set_title("CS2: steering dose-response (refuted)")
save(fig, "figs/cs2_dose.png")
print("ok")
