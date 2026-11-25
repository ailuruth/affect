"""CP4: contingency field over partner x channel. See PREDICTIONS.md."""
import json
import numpy as np
T = 0.05
q = {("A", "face"): 40 / 50, ("A", "voice"): 5 / 50, ("B", "face"): 5 / 50, ("B", "voice"): 40 / 50}
c = {"face": 0.2, "voice": 0.2}; F = {k: 2 * (0.6 - c[k[1]]) for k in q}
def att(vals):
    v = np.array(vals) / T; v -= v.max(); p = np.exp(v); return p / p.sum()
out = {}
for who in ("A", "B"):
    keys = [(who, "face"), (who, "voice")]
    p = att([F[k] * q[k] * 0.3 for k in keys])
    Fc = 2 * (0.6 - np.mean(list(c.values()))); qc = np.mean(list(q.values()))
    pc = att([Fc * qc * 0.3 for _ in keys])
    out[f"present_{who}"] = dict(field_face=float(p[0]), field_voice=float(p[1]), collapsed_face=float(pc[0]))
cues = list(q.keys())
pf = att([F[k] * q[k] * 0.3 for k in cues]); pcol = att([2 * (0.6 - 0.2) * np.mean(list(q.values())) * 0.3 for k in cues])
out["cues_field"] = dict(zip([f"{a}_{b}" for a, b in cues], pf.round(4).tolist())); out["cues_collapsed"] = dict(zip([f"{a}_{b}" for a, b in cues], pcol.round(4).tolist()))
out["CP4-3_field_Aface_plus_Bvoice"] = float(pf[0] + pf[3])
print(json.dumps(out, indent=1))
