"""ES19: agent's own expression as a cause of engagement; is reply-conditioning enough or must expression be excluded? See PREDICTIONS.md."""
import json, math
import numpy as np
from scipy.special import expit
NT, T, F = 30, 2000, 8; LEV = np.array([0.0, 0.5, 1.0])
def run(seed, arm):
    r = np.random.default_rng(seed); Y = r.standard_normal((NT, 6)); B = r.standard_normal((F, 6)) / math.sqrt(6); TT = Y @ B.T + 0.3 * r.standard_normal((NT, F))
    w = r.standard_normal(4); mu2 = 0.3 * Y[:, :4] @ w; base = 2.5 * Y[:, 4] + 1.5 * Y[:, 5]
    re = np.random.default_rng(seed + 2000); use_a = arm in ("weighted_expr", "cond_expr"); levels = LEV if use_a else np.array([0.5])
    kk, aa = np.meshgrid(np.arange(NT), levels, indexing="ij"); kk, aa = kk.ravel(), aa.ravel()
    Phi = np.concatenate([np.ones((len(kk), 1)), TT[kk]] + ([aa[:, None]] if use_a else []), 1); D = Phi.shape[1]; G = np.eye(D); H = np.zeros(D)
    b = np.zeros(2); A, R = [], []
    for t in range(T):
        b = np.minimum(b - 0.05, 1.0); e = np.maximum(-b, 0); pred = np.stack([np.full(len(kk), 0.3), Phi @ np.linalg.solve(G, H)], 1); val = pred @ e
        explore = np.linalg.norm(e) > 0.1 and re.random() < 0.1
        j = int(re.integers(0, len(kk))) if explore else (int(np.argmax(val)) if val.max() > 0.01 else -1)
        if j >= 0:
            k, a = kk[j], aa[j]; reply = re.random() < expit(base[k] + 2 * (a - 0.5))
            f2 = (mu2[k] + 0.2 * a + 0.15 * re.standard_normal()) if reply else 0.0; b = np.minimum(b + np.array([0.3, f2]), 1.0)
            if arm == "weighted_expr" or reply: G += np.outer(Phi[j], Phi[j]); H += Phi[j] * f2
            if t >= 500: A.append(a); R.append(reply)
    return float(np.mean(A)), float(np.mean(R))
out = {}
for arm in ("weighted_expr", "cond_expr", "d66"):
    X = np.array([run(s, arm) for s in range(40)]); se = X[:, 0].std(ddof=1) / math.sqrt(40)
    out[arm] = dict(mean_expression=float(X[:, 0].mean()), ci=[float(X[:, 0].mean() - 1.96 * se), float(X[:, 0].mean() + 1.96 * se)], reply_rate=float(X[:, 1].mean()))
print(json.dumps(out, indent=1))
