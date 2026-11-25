"""[tiefix: exact ties broken at random via a separate stream] ES7c: need 2 fills only on reply; reply-conditional vs reply-weighted valuation. See PREDICTIONS.md."""
import json, math
import numpy as np
from scipy.stats import spearmanr
from scipy.special import expit
NT, T, F = 30, 2000, 8
def run(seed, arm):
    r = np.random.default_rng(seed); Y = r.standard_normal((NT, 6)); B = r.standard_normal((F, 6)) / math.sqrt(6); TT = Y @ B.T + 0.3 * r.standard_normal((NT, F))
    g = expit(2.5 * Y[:, 4] + 1.5 * Y[:, 5]); w = r.standard_normal(4); mu2 = 0.3 * Y[:, :4] @ w
    re = np.random.default_rng(seed + 2000); rt = np.random.default_rng(seed + 4000); Phi = np.concatenate([np.ones((NT, 1)), TT], 1); G = np.eye(F + 1); H = np.zeros(F + 1)
    b = np.zeros(2); counts = np.zeros(NT); c2 = []
    for t in range(T):
        b = np.minimum(b - 0.05, 1.0); e = np.maximum(-b, 0)
        pred = np.stack([np.full(NT, 0.3), Phi @ np.linalg.solve(G, H)], 1); val = pred @ e
        explore = np.linalg.norm(e) > 0.1 and re.random() < 0.1
        k = int(re.integers(0, NT)) if explore else (int(rt.choice(np.flatnonzero(val >= val.max() - 1e-12))) if val.max() > 0.01 else -1)
        if t >= 500:
            c2.append(0.5 * e[1] ** 2)
            if k >= 0: counts[k] += 1
        if k >= 0:
            reply = re.random() < g[k]; f2 = (mu2[k] + 0.15 * re.standard_normal()) if reply else 0.0
            b = np.minimum(b + np.array([0.3, f2]), 1.0)
            if arm == "weighted" or reply: G += np.outer(Phi[k], Phi[k]); H += Phi[k] * f2
    rho = spearmanr(counts, g).statistic if counts.sum() > 0 else 0.0
    return float(rho), float((counts @ g) / counts.sum() / g.mean()) if counts.sum() > 0 else 1.0, float(np.mean(c2))
out = {}
for arm in ("conditional", "weighted"):
    R = np.array([run(s, arm) for s in range(40)]); se = lambda x: x.std(ddof=1) / math.sqrt(len(x))
    out[arm] = dict(rho_mean=float(R[:, 0].mean()), rho_ci=[float(R[:, 0].mean() - 1.96 * se(R[:, 0])), float(R[:, 0].mean() + 1.96 * se(R[:, 0]))],
                    gain_mean=float(R[:, 1].mean()), gain_ci=[float(R[:, 1].mean() - 1.96 * se(R[:, 1])), float(R[:, 1].mean() + 1.96 * se(R[:, 1]))], need2_cost_median=float(np.median(R[:, 2])))
print(json.dumps(out, indent=1))
