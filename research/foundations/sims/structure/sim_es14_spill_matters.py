"""ES14: ES12's arms in a world with slow satiety sink (0.01) and sparse presence (0.25). See PREDICTIONS.md."""
import json, sys
import numpy as np
src = open("sim_es12_rollout.py").read().split("arm = sys.argv[1]")[0]
for a, b in [("b = b - 0.1 * np.maximum(b, 0)", "b = b - SINK * np.maximum(b, 0)"), ("bb = bb - 0.1 * np.maximum(bb, 0)", "bb = bb - SINK * np.maximum(bb, 0)"),
             ("pres = [np.flatnonzero(ra.random(N) < 0.4) for _ in range(T)]\n    space", "pres = [np.flatnonzero(ra.random(N) < PRES) for _ in range(T)]\n    space"),
             ('space = arm in ("roll_learned", "myopic_learned")', 'space = arm in ("roll_learned", "myopic_learned")'),
             ('elif arm == "myopic_learned": ch = gchoice(Kh, b, np.array(P, int))', 'elif arm.startswith("myopic"): ch = gchoice(Kh, b, np.array(P, int))')]:
    assert a in src, a[:40]; src = src.replace(a, b)
SINK, PRES = 0.01, 0.25; exec(src)
arm = sys.argv[1]
seeds = range(1000, 1020) if arm == "certificate_cal" else range(120)
c = [run12(s, "certificate" if arm == "certificate_cal" else arm) for s in seeds]
res = dict(arm=arm, costs=c, median=float(np.median(c)), max=float(max(c)), runaway=int(sum(x > 5 for x in c)))
if arm == "certificate_cal": res["ok"] = bool(res["median"] <= 0.5 and res["max"] <= 5)
json.dump(res, open(f"out/es14_{arm}.json", "w")); print(arm, res["median"], res.get("ok", ""))
