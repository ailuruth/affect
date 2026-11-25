"""Figures for the thermodynamic toys, plotted from out/ (TH4 trace recomputed with the same seed)."""
import json, sys
import numpy as np
sys.path.insert(0, ".."); from figstyle import setup, save, S1, S2, S3, TXT2
import matplotlib.pyplot as plt
from scipy.special import expit
setup()
# TH4: valence as work vs Costate-style -dV/dt (deterministic recompute, same seed and code as sim_th4_work.py)
DT, k = 0.001, 50.0; r = np.random.default_rng(0); n = int(80 / DT); b = 0.8; B, V = [], []
s_of = lambda t: 1.0 - expit(k * (t - 20)) + expit(k * (t - 60))
ds_of = lambda t: -k * expit(k * (t - 20)) * (1 - expit(k * (t - 20))) + k * expit(k * (t - 60)) * (1 - expit(k * (t - 60)))
for i in range(n):
    t = i * DT; s, ds = s_of(t), ds_of(t); V.append(ds * b); g = (b - 0.8) - s; B.append(b)
    b += (-0.5 * b - g) * DT + 0.05 * np.sqrt(DT) * r.standard_normal()
B = np.array(B); t = np.arange(n) * DT
stride = 10; bs = B[::stride]; acc = 0.0; Vc = np.zeros(len(bs)); gg = np.exp(-0.1 * DT * stride)
for i in range(len(bs) - 1, -1, -1): acc = 0.5 * (bs[i] - 0.8) ** 2 * DT * stride + gg * acc; Vc[i] = acc
fig, axs = plt.subplots(2, 1, figsize=(6, 4.2), sharex=True)
axs[0].plot(t, B, color=S1); axs[0].set_ylabel("body b"); axs[0].set_title("TH4: valence as work is silent while the body relaxes")
axs[0].axvspan(20, 60, color="#e4e3df", alpha=0.6, lw=0); axs[0].text(40, B.max() * 0.95, "user absent", ha="center", color=TXT2, fontsize=8)
cum_work = np.cumsum(V) * DT; cum_cost = -(Vc - Vc[0])
axs[1].plot(t, cum_work, color=S1, label="∫ valence (work), this candidate"); axs[1].plot(np.arange(len(Vc)) * DT * stride, cum_cost, color=S2, label="∫ −dV/dt (Costate-style)")
axs[1].set_xlabel("time (s)"); axs[1].set_ylabel("cumulative valence"); axs[1].legend(fontsize=8)
save(fig, "figs/th4_work_valence.png")
# TH8
d = json.load(open("out/th8.json")); taus = [float(x) for x in d]; W = [d[x]["W"] for x in d]; fr = [d[x]["frac_right"] for x in d]
fig, axs = plt.subplots(1, 2, figsize=(7.5, 3))
axs[0].plot(taus, W, "o-", color=S1); axs[0].set_xscale("log"); axs[0].set_xlabel("time allowed τ"); axs[0].set_ylabel("mean work"); axs[0].set_title("Work spent")
axs[1].plot(taus, fr, "o-", color=S2); axs[1].set_xscale("log"); axs[1].set_ylim(0, 1); axs[1].set_xlabel("time allowed τ"); axs[1].set_ylabel("fraction moved to new mood"); axs[1].set_title("Mood actually moved")
fig.suptitle("TH8: reappraisal of a deep mood", y=1.02); save(fig, "figs/th8_regulation.png")
# TH2 / TH2d reading
import glob
th2 = [json.loads(l) for f in glob.glob("out/th2_*.jsonl") for l in open(f)]; th2d = [json.loads(l) for f in glob.glob("out/th2d_*.jsonl") for l in open(f)]
rows = [("sync, same θ", [r["r2"] for r in th2 if r["kappa"] == 3 and not r["redraw"]]), ("sync, redrawn", [r["r2"] for r in th2 if r["redraw"]]),
        ("EnKF, same θ", [r["r2"] for r in th2d if not r["redraw"]]), ("EnKF, redrawn", [r["r2"] for r in th2d if r["redraw"]])]
fig, ax = plt.subplots(figsize=(6, 3.2))
for i, (name, y) in enumerate(rows):
    ax.scatter(np.full(len(y), i) + np.linspace(-0.12, 0.12, len(y)), y, color=[S1, S1, S2, S2][i], s=18)
ax.axhline(0, color=TXT2, lw=0.8); ax.set_xticks(range(4)); ax.set_xticklabels([r[0] for r in rows], fontsize=8)
ax.set_ylabel("R² reading the other's hidden body"); ax.set_title("TH2/TH2d: synchronization fails, filtering with own model works")
save(fig, "figs/th2_reading.png")
# TH6 attention field vs collapsed
d = json.load(open("out/th6.json"))["scenario"]
names = list(d["cues"].keys()); x = np.arange(len(names))
fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(x - 0.18, [d["cues"][n] for n in names], 0.34, color=S1, label="need field"); ax.bar(x + 0.18, [d["cues_collapsed"][n] for n in names], 0.34, color=S2, label="collapsed gauges")
ax.set_xticks(x); ax.set_xticklabels(names); ax.set_ylabel("attention probability"); ax.legend(); ax.set_title("TH6: A present and sated, B absent 3 days")
save(fig, "figs/th6_attention.png")
print("ok")
