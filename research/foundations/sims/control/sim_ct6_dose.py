"""CT6: S1-b steering relevance with own expressive variance. See PREDICTIONS.md second batch."""
import json, sys
import numpy as np
from scipy.stats import spearmanr
from scipy.signal import lfilter
sys.path.insert(0, ".."); from synchrony import wcc_score
FS = 30
def ou(n, tau, sd, r):
    a = np.exp(-1 / (FS * tau)); return lfilter([1.0], [1.0, -a], r.standard_normal(n) * sd * np.sqrt(1 - a * a))
def run(ch, seed):
    r = np.random.default_rng(seed); n = 600 * FS; p = ou(n, 2.0, 1.0, r); own = ou(n, 1.0, 0.5, r)
    a = 0.3 * ch * p + own; return p[::3], a[::3]
u = np.zeros(8); u[0] = 1; levels = [-0.4, -0.2, 0, 0.2, 0.4]; out = {}
for name in ("derived", "random"):
    S, Sc = [], []
    for li, s in enumerate(levels):
        for k in range(20):
            seed = 100 * li + k + (0 if name == "derived" else 5555)
            d = u if name == "derived" else (lambda v: v / np.linalg.norm(v))(np.random.default_rng(seed + 9).standard_normal(8))
            P, A = run(max(0.0, 0.5 + s * float(u @ d)), seed); S.append(s); Sc.append(wcc_score(P, A))
    rho, pv = spearmanr(S, Sc); out[name] = dict(rho=float(rho), p_two=float(pv), means=[float(np.mean([c for s_, c in zip(S, Sc) if s_ == L])) for L in levels])
print(json.dumps(out, indent=1))
