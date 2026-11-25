"""CS3: costate field dimensionality and per-entity-anticipation ablation. See PREDICTIONS.md."""
import json
import numpy as np
from env_t1 import K_A, K_P, B_STAR, RHO
STEP = 5; DH = STEP / 60; H = 72  # 6h horizon in 5-min steps
r = np.random.default_rng(0); T = 7 * 24 * 12
pres = np.zeros((3, T), dtype=int)
for p in range(3):
    for d in range(7):
        if r.random() < 0.5:
            start = d * 288 + int(r.uniform(8, 20) * 12); dur = int(r.uniform(1, 3) * 12)
            pres[p, start:start + dur] = 1
b = np.zeros((3, T)); x = np.full(3, 0.5)
for t in range(T):
    b[:, t] = x
    x = x + DH * np.where(pres[:, t] == 1, K_P * (1 - x), -K_A * x)
def V(b0, fut):
    v, xx = 0.0, b0
    for k in range(len(fut)):
        xx = xx + DH * (K_P * (1 - xx) if fut[k] else -K_A * xx); v += np.exp(-RHO * DH * (k + 1)) * (xx - B_STAR) ** 2 * DH
    return v
def mu(b0, fut, e=1e-4): return -(V(b0 + e, fut) - V(b0 - e, fut)) / (2 * e)
M = np.zeros((3, T - H)); Dd = np.zeros((3, T - H))
for t in range(T - H):
    for p in range(3):
        M[p, t] = mu(b[p, t], pres[p, t:t + H]); Dd[p, t] = 2 * (B_STAR - b[p, t])
alpha = (M - Dd).mean(0); Q = Dd + alpha
absent2 = (pres[:, :T - H] == 0).sum(0) >= 2
diff = (np.argmax(M, 0) != np.argmax(Q, 0))[absent2]
def pr(X):
    ev = np.linalg.eigvalsh(np.cov(X)); return float(ev.sum() ** 2 / (ev ** 2).sum())
print(json.dumps(dict(CS3_1_frac_top_differs=float(diff.mean()), n_steps_two_absent=int(absent2.sum()), CS3_2_PR_costate=pr(M), CS3_3_PR_deficit=pr(Dd)), indent=1))
