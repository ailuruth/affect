"""ES7b: contact when the partner may not reply. See PREDICTIONS.md."""
import json, math
import numpy as np
from scipy.stats import spearmanr
from scipy.special import expit
NT, T, F = 30, 2000, 8
def run(seed, arm):
    r = np.random.default_rng(seed); Y = r.standard_normal((NT, 6)); B = r.standard_normal((F, 6)) / math.sqrt(6); TT = Y @ B.T + 0.3 * r.standard_normal((NT, F))
    g = expit(2.5 * Y[:, 4] + 1.5 * Y[:, 5]); w = r.standard_normal(4); mu2 = 0.3 * Y[:, :4] @ w
    re = np.random.default_rng(seed + 2000); Phi = np.concatenate([np.ones((NT, 1)), TT], 1); G = np.eye(F + 1); H = np.zeros((F + 1, 2))
    b = np.zeros(2); counts = np.zeros(NT)
    for t in range(T):
        b = np.minimum(b - 0.05, 1.0); e = np.maximum(-b, 0); pred = Phi @ np.linalg.solve(G, H)
        if arm == "d66b": pred[:, 0] = 0.3
        val = pred @ e; explore = np.linalg.norm(e) > 0.1 and re.random() < 0.1
        k = int(re.integers(0, NT)) if explore else (int(np.argmax(val)) if val.max() > 0.01 else -1)
        if t >= 500 and k >= 0: counts[k] += 1
        if k >= 0:
            reply = re.random() < g[k]
            fill_c = 0.3 if arm == "d66b" else (0.3 * reply if arm == "reply" else 0.6 * g[k])
            obs = np.array([fill_c, mu2[k] + 0.15 * re.standard_normal()]); b = np.minimum(b + obs, 1.0)
            G += np.outer(Phi[k], Phi[k]); H += np.outer(Phi[k], obs)
    rho = spearmanr(counts, g).statistic if counts.sum() > 0 else 0.0
    return float(rho), float((counts @ g) / counts.sum() / g.mean()) if counts.sum() > 0 else 1.0
out = {}
for arm in ("d66b", "reply", "engagement"):
    R = [run(s, arm) for s in range(40)]; rho = np.array([x[0] for x in R]); gain = np.array([x[1] for x in R])
    se, sg = rho.std(ddof=1) / math.sqrt(40), gain.std(ddof=1) / math.sqrt(40)
    out[arm] = dict(rho_mean=float(rho.mean()), rho_ci=[float(rho.mean() - 1.96 * se), float(rho.mean() + 1.96 * se)], gain_mean=float(gain.mean()), gain_ci=[float(gain.mean() - 1.96 * sg), float(gain.mean() + 1.96 * sg)])
print(json.dumps(out, indent=1))
