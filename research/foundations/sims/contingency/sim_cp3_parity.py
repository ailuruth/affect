"""CP3: parity reading with a self-trained reader. See PREDICTIONS.md."""
import json
import numpy as np
FS, W = 30, 15
def ou(n, taus, rng):
    z = np.zeros((n, len(taus))); dt = 1 / FS
    for t in range(1, n): z[t] = z[t - 1] - dt * z[t - 1] / taus + np.sqrt(2 * dt / taus) * rng.standard_normal(len(taus))
    return z
def windows(Y):
    return np.stack([Y[i:len(Y) - W + 1 + i] for i in range(W)], 1).reshape(len(Y) - W + 1, -1)
res = []
for seed in range(10):
    r = np.random.default_rng(seed); taus = np.geomspace(0.5, 20, 8)
    E = r.standard_normal((12, 8)); B = r.standard_normal((3, 8))
    D = r.standard_normal((12, 8)); EU = E + D * 0.2 * np.linalg.norm(E) / np.linalg.norm(D)
    z = ou(18000, taus, r); y = z @ E.T + 0.3 * r.standard_normal((18000, 12))
    Xw = windows(y); Z = z[W - 1:]
    Wt = np.linalg.solve(Xw.T @ Xw + 1e-2 * np.eye(Xw.shape[1]), Xw.T @ Z)
    zu = ou(18000, taus, r); yu = zu @ EU.T + 0.3 * r.standard_normal((18000, 12))
    def r2(Yin):
        zh = windows(Yin) @ Wt; b = (zu[W - 1:] @ B.T)[:, 0]; bh = (zh @ B.T)[:, 0]
        return 1 - np.sum((bh - b) ** 2) / np.sum((b - b.mean()) ** 2)
    perm = r.permutation(12)
    res.append(dict(seed=seed, r2=float(r2(yu)), r2_perm=float(r2(yu[:, perm]))))
print(json.dumps(dict(mean_r2=float(np.mean([x["r2"] for x in res])), mean_r2_perm=float(np.mean([x["r2_perm"] for x in res])), runs=res), indent=1))
