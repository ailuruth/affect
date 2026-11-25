"""Regenerates out/es1_per_seed.txt (per-seed ES1 costs) from sim_es1_social_space.run."""
import numpy as np
src = open("sim_es1_social_space.py").read().split("out = {}")[0]; exec(src)
with open("out/es1_per_seed.txt", "w") as f:
    for arm in ("full", "scalar", "independent"):
        c = [run(s, arm)["cost"] for s in range(20)]
        f.write(f"{arm} median {round(float(np.median(c)), 3)} n>5: {sum(x > 5 for x in c)} {[round(x, 2) for x in c]}\n")
