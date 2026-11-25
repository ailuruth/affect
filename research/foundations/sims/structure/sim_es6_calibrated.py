"""ES6: ES5 with drift scale calibrated on the oracle only. See PREDICTIONS.md."""
import json, sys
import numpy as np
src = open("sim_es5_field.py").read().split("part = sys.argv")[0]
a = "rp = r.uniform(0.02, 0.05, N)"; assert a in src; src = src.replace(a, "rp = DRIFT_SCALE * r.uniform(0.02, 0.05, N)")
a = "elif arm in (\"learned\", \"identity\", \"oracle\", \"myopic\"): ch = greedy(Kh, b, be, P)"; assert a in src
src = src.replace(a, "elif arm in (\"learned\", \"identity\", \"oracle\", \"myopic\", \"oracle_myopic\"): ch = greedy(K if arm == \"oracle_myopic\" else Kh, b, be, P)")
DRIFT_SCALE = 1.0; exec(src)
out = {"calibration": {}}
for part, budget, oarm, seeds in (("a", False, "oracle", range(40)), ("b", True, "oracle_myopic", range(120))):
    chosen = None
    for s in (1.0, 0.5, 0.25, 0.125):
        DRIFT_SCALE = s; c = [run(sd, oarm, budget)[0] for sd in range(1000, 1020)]
        ok = float(np.median(c)) <= 0.5 and max(c) <= 5; out["calibration"][f"{part}/s={s}"] = dict(median=float(np.median(c)), max=float(max(c)), ok=ok)
        if ok: chosen = s; break
    out["calibration"][f"{part}/chosen"] = chosen
    if chosen is None: continue
    DRIFT_SCALE = chosen; arms = ("learned", "identity", "wta", "global", "oracle") if part == "a" else ("myopic", "rollout")
    for arm in arms:
        R = [run(sd, arm, budget) for sd in seeds]
        out[f"{part}/{arm}"] = dict(costs=[c for c, _, _ in R], agree=float(np.mean([x for _, x, _ in R if x is not None])) if any(x is not None for _, x, _ in R) else None, app_rate=float(np.mean([n for _, _, n in R])))
if out["calibration"]["a/chosen"]:
    g = lambda k: out[f"a/{k}"]["costs"]
    out["checks_a"] = dict(ES6a_1=paired(g("learned"), g("global")), ES6a_2=paired(g("learned"), g("wta")), ES6a_3=paired(g("learned"), g("identity")), ES6a_4=out["a/learned"]["agree"])
if out["calibration"]["b/chosen"]:
    out["checks_b"] = dict(ES6b_1=paired(out["b/rollout"]["costs"], out["b/myopic"]["costs"]), ES6b_2_app_ratio=out["b/rollout"]["app_rate"] / out["b/myopic"]["app_rate"])
print(json.dumps(out, indent=1))
