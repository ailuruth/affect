"""Diagnostic (not a test): why does rollout with the threshold base lose to the threshold rule? Seeds 0-29.
Variants of the thresh-base rollout: (a) as run; (b) exploration off; (c) exploration off and horizon 20. Compared with the certificate (ES12 test seeds)."""
import json, math
import numpy as np
base_src = open("sim_es15_multibase.py").read().split("arm = sys.argv[1]")[0]
out = {}
cert = np.array(json.load(open("out/es12_certificate.json"))["costs"][:30])
for name, repl in (("as_run", []), ("no_explore", [("re.random() < 0.1", "False")]), ("no_explore_H20", [("re.random() < 0.1", "False"), ("H_, M_ = 6, 4", "H_, M_ = 20, 4")])):
    s = base_src
    for a, b in repl: assert a in s; s = s.replace(a, b)
    ns = {}; exec(s, ns); c = np.array([ns["run15"](sd, "thresh") for sd in range(30)])
    lr = np.log(c / cert); out[name] = dict(median=float(np.median(c)), geo_vs_cert=float(np.exp(lr.mean())), wins=int((lr < 0).sum()))
print(json.dumps(out, indent=1))
