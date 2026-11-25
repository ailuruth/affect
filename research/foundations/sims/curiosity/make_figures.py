"""Figure for the shared curiosity toy and TH7, plotted from out/ files."""
import json, sys
import numpy as np
sys.path.insert(0, ".."); from figstyle import setup, save, S1, S2, S3
import matplotlib.pyplot as plt
setup()
th7 = json.load(open("../thermo/out/th7.json")); lp = json.load(open("out/lp.json"))
v = lp["visits"]; tot = sum(v.values())
agents = {"surprisal minimizer": [th7["agent1"]["L"], th7["agent1"]["N"], th7["agent1"]["B"]],
          "predictability set point": [th7["agent2"]["L"], th7["agent2"]["N"], th7["agent2"]["B"]],
          "learning-progress drive": [(v["L1"] + v["L2"]) / tot, v["N"] / tot, v["B"] / tot]}
fig, ax = plt.subplots(figsize=(6, 3))
x = np.arange(3)
for i, (c, lab) in enumerate(zip([S1, S2, S3], ["learnable", "noise (noisy TV)", "boring (dark room)"])):
    ax.bar(x + (i - 1) * 0.26, [agents[a][i] for a in agents], 0.24, color=c, label=lab)
ax.set_xticks(x); ax.set_xticklabels(list(agents), fontsize=9); ax.set_ylabel("share of choices"); ax.legend(fontsize=8)
ax.set_title("Curiosity: only the learning-progress drive avoids both traps"); save(fig, "figs/curiosity_traps.png")
print("ok")
