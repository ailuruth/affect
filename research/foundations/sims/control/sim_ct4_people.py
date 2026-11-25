"""CT4: per-person internal models vs one shared model. See PREDICTIONS.md."""
import json
import numpy as np
DT, TEND = 0.01, 1200.0; C = {"A": 0.8, "B": 0.1, "C": 0.4}; F = {"A": 1.57, "B": 1.2, "C": 2.0}; order = ["A", "B", "C"]
def run(field, seed=0):
    r = np.random.default_rng(seed); n = int(TEND / DT); b = m = 0.0; yh = 0.0
    ch = {p: 0.5 for p in order}; shared = 0.5; E = np.empty(n); amp = {p: [] for p in order}
    for k in range(n):
        t = k * DT; p = order[int(t // 20) % 3]; yu = np.sin(F[p] * t); y = yu + 0.1 * r.standard_normal()
        yh += (y - yh) * DT / 0.05
        cur = ch[p] if field else shared
        u = -1.0 * b - 0.1 * m - cur * yh
        if field: ch[p] += (0.5 * b * yh - 0.001 * ch[p]) * DT
        else: shared += (0.5 * b * yh - 0.001 * shared) * DT
        b += (-0.1 * b + u + C[p] * yu) * DT; m += b * DT; E[k] = b
        if t > TEND - 400: amp[p].append(0.3 * cur * yh)
    return float(np.sqrt(np.mean(E[-int(400 / DT):] ** 2))), {p: float(np.std(v)) for p, v in amp.items()}
rf, af = run(True); rc, ac = run(False)
print(json.dumps(dict(field_rms=rf, collapsed_rms=rc, rms_ratio=rc / rf, field_amp=af, collapsed_amp=ac, field_A_over_B=af["A"] / af["B"], collapsed_A_over_B=ac["A"] / ac["B"]), indent=1))
