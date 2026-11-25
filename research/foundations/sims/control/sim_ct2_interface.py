"""CT2: interface sector — small-gain safety and observability of influence. See PREDICTIONS.md."""
import json
import numpy as np
out = {}
for gs in (0.05, 0.09, 0.11, 0.2):
    e = 0.0; m = 1.0; dt = 0.01; mx = 0.0
    for k in range(int(1000 / dt)):
        s = gs * m; d = 1.0 * abs(s) * np.sign(m)
        e += (-e + d) * dt; m += (-0.1 * m + e) * dt; mx = max(mx, abs(m))
        if mx > 1e6: break
    out[f"L={10*gs:.1f}"] = dict(max_abs_m=float(mx))
r = np.random.default_rng(0); M = r.standard_normal((5000, 3)); H = r.standard_normal((6, 3))
def r2s(G):
    F = M @ (H @ G).T + 0.05 * r.standard_normal((5000, 6)); X = np.c_[np.ones(5000), F]; res = []
    for j in range(3):
        w = np.linalg.lstsq(X[:2500], M[:2500, j], rcond=None)[0]; yh = X[2500:] @ w; y = M[2500:, j]
        res.append(float(1 - np.sum((yh - y) ** 2) / np.sum((y - y.mean()) ** 2)))
    return res
out["CT2b_rank3"] = r2s(r.standard_normal((3, 3))); g = r.standard_normal((3, 1)) @ r.standard_normal((1, 3)); out["CT2b_rank1"] = r2s(g)
print(json.dumps(out, indent=1))
