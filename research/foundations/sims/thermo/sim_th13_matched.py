"""TH13: parameter-matched collapsed ablation. See PREDICTIONS.md seventh batch."""
import json
import numpy as np
BSTAR = np.array([0.8, 0.8, 0.8, 0.6, 0.6]); T = 0.05; b = np.array([0.95, 0.0, 0.15, 0.98, 0.0])
def content(p, t, r):
    c = np.zeros(8); c[p] = 1; c[3 + t] = 1; c[5:] = r.standard_normal(3); return c
def effect(p, t, r):
    e = np.zeros(5); e[p] = 0.3; e[3 + t] = 0.2; return e + r.normal(0, 0.05, 5)
def att(q, keys):
    s = np.array([q @ k for k in keys]) / T; s -= s.max(); p = np.exp(s); return p / p.sum()
res = []
for seed in range(10):
    r = np.random.default_rng(seed)
    ev = [(int(r.integers(3)), int(r.integers(2))) for _ in range(200)]
    C = np.array([content(p, t, r) for p, t in ev]); E = np.array([effect(p, t, r) for p, t in ev])
    Ecol = np.c_[E[:, :3].mean(1), E[:, 3:].mean(1)]
    Wf = np.random.default_rng(1000 + seed).standard_normal((8, 12))
    feat = lambda X: np.c_[X, np.tanh(X @ Wf)]
    Kf = np.linalg.lstsq(C, E, rcond=None)[0]; Kc = np.linalg.lstsq(feat(C), Ecol, rcond=None)[0]
    eps = [(p, int(r.integers(2))) for p in range(3) for _ in range(20)]
    Ce = np.array([content(p, t, r) for p, t in eps])
    qf = 2 * (BSTAR - b); qc = 2 * (np.array([0.8, 0.6]) - np.array([b[:3].mean(), b[3:].mean()]))
    pf = att(qf, Ce @ Kf); pc = att(qc, feat(Ce) @ Kc)
    res.append(dict(field_B=[eps[i][0] for i in np.argsort(-pf)[:5]].count(1), coll_B=[eps[i][0] for i in np.argsort(-pc)[:5]].count(1), params_field=int(Kf.size), params_coll=int(Kc.size)))
print(json.dumps(dict(n_field_ge4=sum(x["field_B"] >= 4 for x in res), mean_coll_B=float(np.mean([x["coll_B"] for x in res])), params=(res[0]["params_field"], res[0]["params_coll"]), runs=res), indent=1))
