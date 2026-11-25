"""ES2b: anticipation without the memory option. Reuses ES2's run() with both arms memoryless. See PREDICTIONS.md."""
import json
import numpy as np
src = open("sim_es2_relations_memory.py").read().split("out = {}")[0]
src = src.replace('usemem = arm != "nomem"', 'usemem = arm not in ("nomem", "rr_nomem")'); exec(src)
out = {}
for world in ("companion", "random"):
    for arm in ("nomem", "rr_nomem"):
        c = [run(s, arm, world)["cost"] for s in range(20)]
        out[f"{world}/{arm}"] = dict(median_cost=float(np.median(c)), mean_cost=float(np.mean(c)), runaway=int(sum(x > 5 for x in c)), costs=[round(x, 4) for x in c])
out["checks"] = {w: out[f"{w}/nomem"]["median_cost"] / out[f"{w}/rr_nomem"]["median_cost"] for w in ("companion", "random")}
print(json.dumps(out, indent=1))
