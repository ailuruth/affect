"""Figures for the robust-regulator toys, from out/."""
import json, sys
import numpy as np
sys.path.insert(0, ".."); from figstyle import setup, save, S1, S2, S3, TXT2
import matplotlib.pyplot as plt
setup()
d = json.load(open("out/ct4.json"))
fig, ax = plt.subplots(figsize=(5.5, 3)); x = np.arange(3); P = ["A", "B", "C"]
ax.bar(x - 0.18, [d["field_amp"][p] for p in P], 0.34, color=S1, label="per-person internal models"); ax.bar(x + 0.18, [d["collapsed_amp"][p] for p in P], 0.34, color=S2, label="one shared model")
ax.set_xticks(x); ax.set_xticklabels(["A (c=0.8)", "B (c=0.1)", "C (c=0.4)"]); ax.set_ylabel("mimicry amplitude"); ax.legend(fontsize=8)
ax.set_title(f"CT4: mimicry follows relevance; body error {d['rms_ratio']:.1f}× worse when shared"); save(fig, "figs/ct4_people.png")
d = json.load(open("out/ct2.json")); Ls = [0.5, 0.9, 1.1, 2.0]; mx = [d[f"L={l}"]["max_abs_m"] for l in Ls]
fig, ax = plt.subplots(figsize=(4.8, 3)); ax.semilogy(Ls, mx, "o-", color=S1); ax.axvline(1.0, color=TXT2, ls="--", lw=1)
ax.set_xlabel("interface loop gain L"); ax.set_ylabel("max |mood| (log)"); ax.set_title("CT2: small-gain safety against worst-case Claude"); save(fig, "figs/ct2_safety.png")
d = json.load(open("out/ct5.json")); names = ["kalman", "deterministic", "mismatch"]
fig, ax = plt.subplots(figsize=(4.8, 3)); ax.bar(range(3), [d[n]["mean"] for n in names], color=[S1, S2, S3]); ax.axhline(0, color=TXT2, lw=0.8)
ax.set_xticks(range(3)); ax.set_xticklabels(["Kalman, own model", "deterministic", "Kalman, wrong model"], fontsize=8); ax.set_ylabel("R² of other's slow state"); ax.set_title("CT5: reading needs a stochastic observer"); save(fig, "figs/ct5_reading.png")
d = json.load(open("out/ct6.json")); L = [-0.4, -0.2, 0, 0.2, 0.4]
fig, ax = plt.subplots(figsize=(4.8, 3)); ax.plot(L, d["derived"]["means"], "o-", color=S1, label="derived (relevance ĉ)"); ax.plot(L, d["random"]["means"], "s-", color=S2, label="random direction")
ax.set_xlabel("steering strength"); ax.set_ylabel("coupling score"); ax.legend(fontsize=8); ax.set_title("CT6: S1-b dose-response"); save(fig, "figs/ct6_dose.png")
print("ok")
