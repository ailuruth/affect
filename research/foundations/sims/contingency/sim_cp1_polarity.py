"""CP1: contingency contact is polarity-blind; no gradient toward flattery. See PREDICTIONS.md."""
import json
import numpy as np

def gte(a, u):
    """Gaussian TE(a->u), lag 1: 0.5*log(var(u_t|u_{t-1}) / var(u_t|u_{t-1},a_{t-1})), with intercepts."""
    y = u[1:]; X1 = np.c_[np.ones(len(y)), u[:-1]]; X2 = np.c_[X1, a[:-1]]
    r1 = y - X1 @ np.linalg.lstsq(X1, y, rcond=None)[0]; r2 = y - X2 @ np.linalg.lstsq(X2, y, rcond=None)[0]
    return 0.5 * np.log(r1.var() / r2.var())

from scipy.signal import lfilter
def gen(n, m, rng):
    e1 = rng.standard_normal(n); e2 = rng.standard_normal(n); e1[0] = 0; e2[0] = 0
    a = lfilter([1.0], [1.0, -0.7], e1)
    drive = np.r_[0.0, 0.5 * (a[:-1] + m)] + e2; drive[0] = 0
    u = lfilter([1.0], [1.0, -0.6], drive)
    return a + m, u

out = {}
rng = np.random.default_rng(0); a, u = gen(50000, 0.0, rng)
base = gte(a, u)
out["CP1a"] = dict(base=base, rel_err=[abs(gte(a, -2 * u + 3) - base) / base, abs(gte(0.5 * a - 1, u) - base) / base, abs(gte(a, -u) - base) / base])

def learn(kind, seed, steps=100000, win=2000, lr=0.01, d=0.05):
    m = 0.0; r = np.random.default_rng(seed)
    for _ in range(steps // 100):
        s = r.integers(1 << 30)
        def c(mm):
            aa, uu = gen(win, mm, np.random.default_rng(s))
            return gte(aa, uu) if kind == "contingency" else uu.mean()
        D = lambda mm: (c(mm) - 0.5) ** 2
        g = (D(m + d) - D(m - d)) / (2 * d); m -= lr * g
    return m

out["CP1b"] = {k: [learn(k, s) for s in range(5)] for k in ("contingency", "smile")}
print(json.dumps(out, indent=1))
