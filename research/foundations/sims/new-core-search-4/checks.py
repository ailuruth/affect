"""Algebra/mechanism checks for new-core-search-4-synthesis.md (Direction 1: transition-keyed
contingency head). numpy only. Hand-made instances; NOT evidence about behaviour or people.

Head: p_hat_t = sum_s softmax_s(<phi(a_{s-d}), phi(a_{t-d})>/tau) p_s over stored s < t - excl.
Residual r_t = p_t - p_hat_t. Contingency mass c_t = max_s attention weight * n (peakedness).
Reported: fraction of partner variance left in r (after burn-in), per partner type.
"""
import numpy as np

rng = np.random.default_rng(0)
T, D, d = 3000, 6, 3          # steps, channels, key shift (events)

def ar1(T, D, rho):
    x = np.zeros((T, D)); e = rng.standard_normal((T, D)) * np.sqrt(1 - rho**2)
    for t in range(1, T):
        x[t] = rho * x[t-1] + e[t]
    return x

def head(a, p, tau, excl, burn=500):
    keys = np.vstack([np.zeros((d, a.shape[1])), a[:-d]])     # a_{t-d}
    keys = keys / (np.linalg.norm(keys, axis=1, keepdims=True) + 1e-9)
    res, mass = [], []
    for t in range(burn, len(a)):
        hi = t - excl
        if hi < 10: continue
        s = keys[:hi] @ keys[t] / tau
        w = np.exp(s - s.max()); w /= w.sum()
        res.append(p[t] - w @ p[:hi]); mass.append(w.max() * hi)
    res = np.array(res)
    return res.var() / p[burn:].var(), np.median(mass)

def W(D):  # fixed mixing for a nonlinear partner response
    return rng.standard_normal((D, D)) / np.sqrt(D)
Wm = W(D)

print("C1-C3: residual variance fraction (1 = partner fully kept, 0 = fully cancelled)")
for rho_a in (0.5, 0.98):
    a = ar1(T, D, rho_a)
    lag = np.vstack([np.zeros((d, D)), a[:-d]])
    cs = {
        "mirror": lag,
        "nonlin-answer": np.tanh(lag @ Wm) + 0.3 * rng.standard_normal((T, D)),
        "indep-slow": ar1(T, D, 0.98),
        "indep-fast": ar1(T, D, 0.5),
    }
    for excl in (1, 60):
        for tau in (0.05, 0.3):
            row = []
            for name, p in cs.items():
                f, m = head(a, p, tau, excl)
                row.append(f"{name} {f:5.2f}")
            print(f"own-act rho={rho_a:4.2f} excl={excl:3d} tau={tau:4.2f} | " + " | ".join(row))
