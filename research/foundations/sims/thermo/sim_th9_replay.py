"""TH9: importance-weighted replay by |work|. See PREDICTIONS.md."""
import json
import numpy as np
def experiment(eta_sd, reps=2000, N=1000, m=50, seed=0):
    r = np.random.default_rng(seed)
    W = r.lognormal(0, 1, N); g = W * r.normal(1, eta_sd, N); true = g.mean()
    p = np.abs(W) / np.abs(W).sum()
    u = np.array([g[r.integers(0, N, m)].mean() for _ in range(reps)])
    imp = []
    for _ in range(reps):
        idx = r.choice(N, m, p=p); imp.append(np.mean(g[idx] / (N * p[idx])))
    imp = np.array(imp)
    return dict(true=float(true), mean_uniform=float(u.mean()), se_uniform=float(u.std() / np.sqrt(reps)), mean_imp=float(imp.mean()),
                se_imp=float(imp.std() / np.sqrt(reps)), var_ratio=float(imp.var() / u.var()), corr_absW_absg=float(np.corrcoef(np.abs(W), np.abs(g))[0, 1]))
print(json.dumps(dict(sd05=experiment(0.5), sd2=experiment(2.0)), indent=1))
