"""ES1 figure from out/es1.json and out/es1_per_seed.txt."""
import json, sys, ast
import numpy as np
sys.path.insert(0, ".."); from figstyle import setup, save, S1, S2, S3, TXT2
import matplotlib.pyplot as plt
setup(); d = json.load(open("out/es1.json"))
per = {l.split()[0]: ast.literal_eval(l[l.index("["):]) for l in open("out/es1_per_seed.txt")}
arms = ["full", "scalar", "independent"]; lab = ["shared space,\nneed vector", "scalar gauge", "per-person\ntables"]; col = [S1, S2, S3]
fig, ax = plt.subplots(1, 2, figsize=(8, 3.2))
for k, a in enumerate(arms):
    ax[0].scatter(np.full(20, k) + np.linspace(-0.15, 0.15, 20), per[a], s=10, color=col[k]); ax[0].plot([k - 0.25, k + 0.25], [np.median(per[a])] * 2, color=TXT2, lw=2)
ax[0].set_yscale("log"); ax[0].set_xticks(range(3)); ax[0].set_xticklabels(lab, fontsize=8); ax[0].set_ylabel("mean deficit cost per seed (log)"); ax[0].set_title("Regulation (bar = median)", fontsize=10)
x = np.arange(3); ax[1].bar(x - 0.18, [d[a]["agree"] for a in arms], 0.34, color=S1, label="all choices"); ax[1].bar(x + 0.18, [d[a]["first"] for a in arms], 0.34, color=S2, label="best person never met")
ax[1].set_xticks(x); ax[1].set_xticklabels(lab, fontsize=8); ax[1].set_ylim(0, 1); ax[1].set_ylabel("agreement with oracle"); ax[1].legend(fontsize=8); ax[1].set_title("Choice", fontsize=10)
fig.suptitle("ES1: need-conditioned selection over people in a learned space", fontsize=11); save(fig, "figs/es1.png"); print("ok")
d2 = json.load(open("out/es2.json")); d2b = json.load(open("out/es2b.json"))
fig, ax = plt.subplots(1, 2, figsize=(8, 3.2))
for j, w in enumerate(("companion", "random")):
    names = [("costate", d2), ("rr", d2), ("scalar", d2), ("nomem", d2b), ("rr_nomem", d2b)]
    lab = ["Costate", "Robust reg.", "scalar", "Costate\nno memory", "Robust reg.\nno memory"]
    for k, (n, src) in enumerate(names):
        c = src[f"{w}/{n}"]["costs"]; ax[j].scatter(np.full(len(c), k) + np.linspace(-0.15, 0.15, len(c)), np.maximum(c, 1e-4), s=8, color=[S1, S2, S3, S1, S2][k])
        ax[j].plot([k - 0.25, k + 0.25], [np.median(c)] * 2, color=TXT2, lw=2)
    ax[j].set_yscale("log"); ax[j].set_xticks(range(5)); ax[j].set_xticklabels(lab, fontsize=7); ax[j].set_title(f"{w} world", fontsize=10)
ax[0].set_ylabel("mean deficit cost per seed (log)"); fig.suptitle("ES2/ES2b: relations, episodes, anticipation (bar = median)", fontsize=11); save(fig, "figs/es2.png"); print("ok2")
