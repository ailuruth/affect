"""CP6: legibility bound for any namer. See PREDICTIONS.md."""
import json
import numpy as np
r = np.random.default_rng(0); n = 20000
Q, _ = np.linalg.qr(r.standard_normal((8, 8))); Q = Q.T  # rows = orthonormal directions
def run(rank):
    A = r.standard_normal((12, rank)); E = A @ Q[:rank]
    z = r.standard_normal((n, 8)); f = z @ E.T + 0.01 * r.standard_normal((n, 12))
    idx = np.c_[np.tanh(z @ Q[rank]), np.tanh(z @ Q[rank + 1])]
    X = np.c_[np.ones(n), f, idx]; tr, te = slice(0, n // 2), slice(n // 2, n)
    r2s = []
    for k in range(8):
        y = z @ Q[k]; w = np.linalg.lstsq(X[tr], y[tr], rcond=None)[0]; yh = X[te] @ w
        r2s.append(float(1 - np.sum((yh - y[te]) ** 2) / np.sum((y[te] - y[te].mean()) ** 2)))
    return r2s
out = {"rank4_r2_by_direction": run(4), "rank2_r2_by_direction": run(2)}
out["rank4_n_decodable"] = sum(x >= 0.8 for x in out["rank4_r2_by_direction"]); out["rank2_n_decodable"] = sum(x >= 0.8 for x in out["rank2_r2_by_direction"])
print(json.dumps(out, indent=1))
