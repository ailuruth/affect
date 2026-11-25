"""CS2: dyad coupling under costate steering (E2) and lesion (E1). Parameters in PREDICTIONS.md."""
import json, sys
import numpy as np
from scipy.stats import spearmanr
sys.path.insert(0, "..")
from synchrony import wcc_score, surrogates

NA, NX, C, TAU, FS = 12, 8, 4.0, 1.0, 30
rng0 = np.random.default_rng(7)
s_ = np.array([0.1, 0.3, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0])
U, _ = np.linalg.qr(rng0.standard_normal((NA, NA))); Vv, _ = np.linalg.qr(rng0.standard_normal((NX, NX)))
G = U[:, :NX] @ np.diag(s_) @ Vv.T

def run(w, seed, minutes=10):
    r = np.random.default_rng(seed); n = minutes * 60 * FS; dt = 1 / FS
    z = np.zeros(NA); x = np.zeros(NX); A, B = [], []
    for t in range(n):
        z = z + dt * (-z / 2.0) + np.sqrt(2 * dt / 2.0) * r.standard_normal(NA)
        x = x + dt * (-C * x + w * G.T @ (z - G @ x)) / TAU + 0.05 * np.sqrt(dt) * r.standard_normal(NX)
        if t % 3 == 0: A.append(z @ U[:, 7]); B.append((G @ x) @ U[:, 7])
    return np.array(A), np.array(B)

def mu_after(s, d, u): return 0.3 + s * float(u @ d)

out = {}
r = np.random.default_rng(123); u = r.standard_normal(8); u /= np.linalg.norm(u)
levels = [-0.2, -0.1, 0.0, 0.1, 0.2]
for name in ("derived", "random"):
    S, Sc = [], []
    for li, s in enumerate(levels):
        for k in range(20):
            seed = 1000 * li + k + (0 if name == "derived" else 50000)
            d = u if name == "derived" else (lambda v: v / np.linalg.norm(v))(np.random.default_rng(seed + 7).standard_normal(8))
            w = 4 * mu_after(s, d, u) / 0.3
            A, B = run(w, seed); S.append(s); Sc.append(wcc_score(A, B))
    rho, p = spearmanr(S, Sc)
    means = [float(np.mean([c for s, c in zip(S, Sc) if s == L])) for L in levels]
    out[name] = dict(spearman_rho=float(rho), p_two_sided=float(p), means=means)
for name, w in (("s1a_intact", 4.0), ("s1c_lesion", 0.0)):
    rows = []
    for k in range(5):
        A, B = run(w, 900 + k); obs = wcc_score(A, B); rs = np.random.default_rng(77 + k)
        seg = surrogates(A, B, "segment", 1000, rs); sld = surrogates(A, B, "sliding", 1000, rs)
        rows.append(dict(score=obs, beats_seg=bool(obs > np.percentile(seg, 95)), beats_sld=bool(obs > np.percentile(sld, 95))))
    out[name] = rows
print(json.dumps(out, indent=1))
