"""Diagnostic (not a test): oracle cost on calibration seeds with exploration gated on ||b|| (as ES5/ES6) vs on deficit ||max(-b,0)|| vs off."""
import json
import numpy as np
base = open("sim_es5_field.py").read().split("part = sys.argv")[0]
a = "explore = len(P) > 0 and np.linalg.norm(b) > 0.3 and re.random() < 0.1"; assert a in base
out = {}
for name, rule in (("norm_b (as run)", a), ("deficit", "explore = len(P) > 0 and np.linalg.norm(np.maximum(-b, 0)) > 0.3 and re.random() < 0.1"), ("off", "explore = False")):
    ns = {}; exec(base.replace(a, rule), ns)
    for budget in (False, True):
        c = [ns["run"](sd, "oracle", budget)[0] for sd in range(1000, 1020)]
        out[f"{name}/budget={budget}"] = dict(median=float(np.median(c)), max=float(max(c)))
print(json.dumps(out, indent=1))
