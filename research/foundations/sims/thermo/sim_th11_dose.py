"""TH11: S1-b dose-dependence via own-expression stiffness. See PREDICTIONS.md."""
import json, sys
import numpy as np
from scipy.stats import spearmanr
from scipy.signal import lfilter
sys.path.insert(0, ".."); from synchrony import wcc_score
FS = 30; DT = 1 / FS
def run(h1, seed, minutes=10):
    r = np.random.default_rng(seed); n = minutes * 60 * FS
    a_ = np.exp(-DT / 2.0); p = lfilter([1.0], [1.0, -a_], r.standard_normal(n) * np.sqrt(1 - a_ * a_))
    ka = 2.0 * np.exp(-h1); kap = 1.0; a = 0.0; A = np.empty(n)
    noise = r.standard_normal(n) * 0.5 * np.sqrt(DT)
    for t in range(n):
        a += (-ka * a - kap * (a - p[t])) * DT + noise[t]; A[t] = a
    return p[::3], A[::3]
r0 = np.random.default_rng(1); u = np.zeros(8); u[0] = 1.0
levels = [-0.6, -0.3, 0.0, 0.3, 0.6]; out = {}
for name in ("derived", "random"):
    S, Sc = [], []
    for li, s in enumerate(levels):
        for k in range(20):
            seed = 100 * li + k + (0 if name == "derived" else 7777)
            d = u if name == "derived" else (lambda v: v / np.linalg.norm(v))(np.random.default_rng(seed + 5).standard_normal(8))
            P, A = run(s * float(u @ d), seed); S.append(s); Sc.append(wcc_score(P, A))
    rho, pv = spearmanr(S, Sc); out[name] = dict(spearman_rho=float(rho), p_two_sided=float(pv), means=[float(np.mean([c for s_, c in zip(S, Sc) if s_ == L])) for L in levels])
print(json.dumps(out, indent=1))
