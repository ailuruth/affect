"""ES3: reliability-weighted anticipation. Reuses ES2's run() with a prequential-R2 weight. See PREDICTIONS.md."""
import json
import numpy as np
src = open("sim_es2_relations_memory.py").read().split("out = {}")[0]
for a, b in [
    ("pending = None; last = None", "pending = None; last = None; SSE = 0.0; SX = np.zeros(F); SXX = 0.0; w = 1.0"),
    ("P[0] = pending; MtM +=", "P[0] = pending; _pe = X[pending] - np.linalg.solve(MtM, MtY).T @ X[last]; SSE += _pe @ _pe; SX += X[pending]; SXX += X[pending] @ X[pending]; MtM +="),
    ("ph = (n_arr + 1) / (n_app + 2)", "ph = (n_arr + 1) / (n_app + 2); w = (max(0.0, 1 - SSE / max(SXX - SX @ SX / max(n_arr, 1), 1e-9)) if n_arr > 10 else 0.0) if arm.endswith('_rw') else 1.0"),
    ("val = direct + (ph * np.maximum(0, comp) if antic else 0)", "val = direct + (ph * np.maximum(0, w * comp) if antic else 0)"),
    ('antic = arm in ("costate", "scalar", "nomem")', 'antic = arm in ("costate", "scalar", "nomem", "nomem_rw")'),
    ('usemem = arm != "nomem"', 'usemem = arm not in ("nomem", "rr_nomem", "nomem_rw")'),
    ("return dict(cost=float(np.mean(cost)),", "return dict(w=float(w), cost=float(np.mean(cost)),"),
]:
    assert a in src, a; src = src.replace(a, b, 1)
exec(src)
out = {}
for world in ("companion", "random"):
    for arm in ("nomem_rw", "rr_nomem"):
        Rs = [run(s, arm, world) for s in range(20)]; c = [x["cost"] for x in Rs]
        out[f"{world}/{arm}"] = dict(median_cost=float(np.median(c)), mean_cost=float(np.mean(c)), runaway=int(sum(x > 5 for x in c)), w_end=float(np.mean([x["w"] for x in Rs])), costs=[round(x, 4) for x in c])
out["checks"] = {w: dict(median_ratio=out[f"{w}/nomem_rw"]["median_cost"] / out[f"{w}/rr_nomem"]["median_cost"], mean_ratio=out[f"{w}/nomem_rw"]["mean_cost"] / out[f"{w}/rr_nomem"]["mean_cost"], w_end=out[f"{w}/nomem_rw"]["w_end"]) for w in ("companion", "random")}
print(json.dumps(out, indent=1))
