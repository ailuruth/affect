"""CP5: S1 dyad steering with water-filled supply. See PREDICTIONS.md."""
import json, sys
import numpy as np
from scipy.stats import spearmanr
from scipy.signal import lfilter
sys.path.insert(0, "..")
from synchrony import wcc_score, surrogates
FS = 30; NU = np.array([0.1, 0.2, 0.4, 0.8, 1.6, 3.2]); DELAY = int(0.4 * FS)

def waterfill(P):
    if P <= 0: return np.zeros(6)
    lo, hi = 0.0, P + NU.max()
    for _ in range(100):
        mu = (lo + hi) / 2
        if np.maximum(mu - NU, 0).sum() > P: hi = mu
        else: lo = mu
    return np.maximum(lo - NU, 0)

def ou(n, tau, sd, rng):
    a = np.exp(-1 / (FS * tau)); e = rng.standard_normal(n) * sd * np.sqrt(1 - a ** 2)
    return lfilter([1.0], [1.0, -a], e)

def run(n_need, seed, minutes=10, lesion=False):
    r = np.random.default_rng(seed); N = minutes * 60 * FS
    K2 = np.zeros(6) if lesion else waterfill(4 * max(n_need, 0.0))
    yt = ou(N + DELAY, 2.0, 1.0, r); own = ou(N, 1.0, 0.5, r)
    ya = np.sqrt(K2[0]) * yt[:N] + own; partner = yt[DELAY:N + DELAY]
    # agent responds to the partner's past: agent(t) depends on partner(t - delay)
    A = partner[::3]; B = ya[::3]
    return A, B

r0 = np.random.default_rng(42); u = r0.standard_normal(8); u /= np.linalg.norm(u)
levels = [-0.4, -0.2, 0.0, 0.2, 0.4]; out = {}
for name in ("derived", "random"):
    S, Sc = [], []
    for li, s in enumerate(levels):
        for k in range(20):
            seed = 100 * li + k + (0 if name == "derived" else 9999)
            d = u if name == "derived" else (lambda v: v / np.linalg.norm(v))(np.random.default_rng(seed + 3).standard_normal(8))
            A, B = run(0.3 + s * float(u @ d), seed); S.append(s); Sc.append(wcc_score(A, B))
    rho, p = spearmanr(S, Sc); means = [float(np.mean([c for s_, c in zip(S, Sc) if s_ == L])) for L in levels]
    out[name] = dict(spearman_rho=float(rho), p_two_sided=float(p), means=means)
rs = np.random.default_rng(5); A, B = run(-0.1, 4242); seg = surrogates(A, B, "segment", 1000, rs)
out["past_satiety_seg95"] = float(np.percentile(seg, 95)); out["past_satiety_score"] = wcc_score(A, B)
for name, les in (("s1a_intact", False), ("s1c_lesion", True)):
    rows = []
    for k in range(5):
        A, B = run(0.3, 700 + k, lesion=les); obs = wcc_score(A, B); rs = np.random.default_rng(31 + k)
        seg = surrogates(A, B, "segment", 1000, rs); sld = surrogates(A, B, "sliding", 1000, rs)
        rows.append(dict(score=obs, beats_seg=bool(obs > np.percentile(seg, 95)), beats_sld=bool(obs > np.percentile(sld, 95))))
    out[name] = rows
print(json.dumps(out, indent=1))
