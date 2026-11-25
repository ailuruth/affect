"""TH10: attention with keys learned from content. See PREDICTIONS.md."""
import json
import numpy as np
BSTAR = np.array([0.8, 0.8, 0.8, 0.6, 0.6]); T = 0.05; b = np.array([0.95, 0.0, 0.15, 0.98, 0.0])
def content(person, topic, r):
    c = np.zeros(8); c[person] = 1; c[3 + topic] = 1; c[5:] = r.standard_normal(3); return c
def effect(person, topic, r):
    e = np.zeros(5); e[person] = 0.3; e[3 + topic] = 0.2; return e + r.normal(0, 0.05, 5)
def att(q, keys):
    s = np.array([q @ k for k in keys]) / T; s -= s.max(); p = np.exp(s); return p / p.sum()
res = []
for seed in range(10):
    r = np.random.default_rng(seed)
    ev = [(int(r.integers(3)), int(r.integers(2))) for _ in range(200)]
    C = np.array([content(p, t, r) for p, t in ev]); E = np.array([effect(p, t, r) for p, t in ev])
    Ecol = np.c_[E[:, :3].mean(1), E[:, 3:].mean(1)]
    Kf = np.linalg.lstsq(C, E, rcond=None)[0]; Kc = np.linalg.lstsq(C, Ecol, rcond=None)[0]
    eps = [(p, int(r.integers(2))) for p in range(3) for _ in range(20)]
    Ce = np.array([content(p, t, r) for p, t in eps])
    qf = 2 * (BSTAR - b); bc = np.array([b[:3].mean(), b[3:].mean()]); qc = 2 * (np.array([0.8, 0.6]) - bc)
    pf = att(qf, Ce @ Kf); pc = att(qc, Ce @ Kc)
    tf = [eps[i][0] for i in np.argsort(-pf)[:5]]; tc = [eps[i][0] for i in np.argsort(-pc)[:5]]
    res.append(dict(seed=seed, field_B_top5=tf.count(1), collapsed_B_top5=tc.count(1)))
print(json.dumps(dict(n_field_ge4=sum(x["field_B_top5"] >= 4 for x in res), mean_collapsed_B=float(np.mean([x["collapsed_B_top5"] for x in res])), runs=res), indent=1))
