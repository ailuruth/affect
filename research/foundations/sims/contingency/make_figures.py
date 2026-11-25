"""Figures for the contingency toys, plotted from out/."""
import json, sys
import numpy as np
sys.path.insert(0, ".."); from figstyle import setup, save, S1, S2, S3, TXT2
import matplotlib.pyplot as plt
setup()
d = json.load(open("out/cp1.json"))["CP1b"]
fig, ax = plt.subplots(figsize=(4.8, 3))
for i, (k, c, lab) in enumerate([("contingency", S1, "contact = contingency"), ("smile", S2, "contact = user's smiles (forbidden)")]):
    ax.scatter(np.full(5, i) + np.linspace(-0.1, 0.1, 5), d[k], color=c, s=22, label=lab)
ax.set_xticks([0, 1]); ax.set_xticklabels(["contingency", "smile-refilled"]); ax.set_ylabel("learned mean-expression shift m"); ax.legend(fontsize=8, loc="upper left")
ax.set_title("CP1: no gradient toward flattery"); save(fig, "figs/cp1_flattery.png")
d = json.load(open("out/cp2.json")); nu = np.array([0.1, 0.2, 0.4, 0.8, 1.6, 3.2])
fig, ax = plt.subplots(figsize=(4.8, 3))
ax.bar(np.arange(6) - 0.18, d["waterfill"], 0.34, color=S1, label="water-filling (analytic)"); ax.bar(np.arange(6) + 0.18, d["example"]["diag"], 0.34, color=S2, label="optimized gain K_ii²")
ax.set_xticks(range(6)); ax.set_xticklabels([f"ν={v}" for v in nu], fontsize=8); ax.set_ylabel("mimicry power per channel"); ax.legend(fontsize=8)
ax.set_title("CP2: mimicry is water-filled over motor noise"); save(fig, "figs/cp2_waterfill.png")
d = json.load(open("out/cp6.json"))
fig, ax = plt.subplots(figsize=(5.2, 3))
ax.bar(np.arange(8) - 0.18, d["rank4_r2_by_direction"], 0.34, color=S1, label="face rank 4"); ax.bar(np.arange(8) + 0.18, d["rank2_r2_by_direction"], 0.34, color=S2, label="face rank 2")
ax.set_xticks(range(8)); ax.set_xticklabels([f"z{i}" for i in range(8)]); ax.set_ylabel("best-decoder R²"); ax.legend(fontsize=8); ax.set_ylim(-0.05, 1.05)
ax.set_title("CP6: what any namer can recover from face + index"); save(fig, "figs/cp6_legibility.png")
# S1 dyad: contingency CP5 vs Costate CS2 (small multiples, one axis each)
cp5 = json.load(open("out/cp5.json")); cs2 = json.load(open("../costate/out/cs2.json"))
fig, axs = plt.subplots(1, 2, figsize=(8, 3))
for ax, dd, L, title in ((axs[0], cs2, [-0.2, -0.1, 0, 0.1, 0.2], "Costate CS2 (gain steering)"), (axs[1], cp5, [-0.4, -0.2, 0, 0.2, 0.4], "Contingency CP5 (supply steering)")):
    ax.plot(L, dd["derived"]["means"], "o-", color=S1, label="derived direction"); ax.plot(L, dd["random"]["means"], "s-", color=S2, label="random direction")
    ax.set_xlabel("steering strength s"); ax.set_title(title, fontsize=10)
axs[0].set_ylabel("coupling score"); axs[1].legend(fontsize=8); save(fig, "figs/s1_dose_comparison.png")
print("ok")
