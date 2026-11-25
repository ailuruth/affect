"""TH5: emotions as metastable sets of a transfer operator. See PREDICTIONS.md."""
import json
import numpy as np
from scipy.cluster.vq import kmeans2
C = np.array([[0, 0], [2, 0], [1, 1.8]]); DEPTH = np.array([3.4, 3.0, 3.0])
def U(z):
    e = -sum(DEPTH[j] * np.exp(-np.sum((z - C[j]) ** 2, -1) / 0.5) for j in range(3))
    return e + 0.1 * np.sum((z - np.array([1, 0.6])) ** 2, -1)
def gradU(z):
    g = 0.2 * (z - np.array([1, 0.6]))
    for j in range(3):
        g = g + DEPTH[j] * np.exp(-np.sum((z - C[j]) ** 2, -1, keepdims=True) / 0.5) * 2 * (z - C[j]) / 0.5
    return g
# barrier heights on a grid (min over paths approximated by flooding)
xs = np.linspace(-1.5, 3.5, 251); ys = np.linspace(-1.5, 3.3, 241); X, Y = np.meshgrid(xs, ys, indexing="ij")
G = U(np.stack([X, Y], -1))
def basin_of(z):
    for _ in range(400): z = z - 0.01 * gradU(z)
    return np.argmin(np.sum((z[:, None, :] - C[None]) ** 2, -1), 1)
def barrier(j):
    # lowest saddle level at which well j's flood region connects to another well (grid flooding)
    from scipy import ndimage
    ij = [tuple(np.unravel_index(np.argmin(np.sum((np.stack([X, Y], -1) - C[w]) ** 2, -1)), X.shape)) for w in range(3)]
    for level in np.linspace(G.min(), G.max(), 2000):
        lab, _ = ndimage.label(G <= level)
        if lab[ij[j]] and any(lab[ij[j]] == lab[ij[w]] for w in range(3) if w != j): return level - G[ij[j]]
    return None
deep = int(np.argmax(DEPTH)); dU = float(barrier(deep))
def simulate(T, n=200000, dt=0.01, seed=0):
    r = np.random.default_rng(seed); z = C[deep].copy(); out = np.zeros((n, 2))
    for i in range(n):
        z = z - gradU(z[None])[0] * dt + np.sqrt(2 * T * dt) * r.standard_normal(2); out[i] = z
    return out
res = {"barrier_deepest": dU}
rates = []
for T in (0.25, 0.3, 0.35, 0.4):
    traj = simulate(T)
    lab = basin_of(traj[::10].copy())
    # exits from the deepest basin
    in_deep = lab == deep; exits = int(np.sum(in_deep[:-1] & ~in_deep[1:])); time_deep = in_deep.sum() * 0.1
    rates.append((T, exits / max(time_deep, 1e-9), exits))
    if T == 0.3:
        sub = traj[::10]; cent, st = kmeans2(sub, 100, seed=1, minit="++")
        lag = 10; Cm = np.zeros((100, 100))
        for a_, b_ in zip(st[:-lag], st[lag:]): Cm[a_, b_] += 1
        Cs = Cm + Cm.T; P = Cs / np.maximum(Cs.sum(1, keepdims=True), 1)
        w, v = np.linalg.eig(P); o = np.argsort(-w.real); w = w.real[o]; v = v.real[:, o]
        gaps = [w[k] - w[k + 1] for k in range(0, 6)]
        res["TH5a_eigs"] = w[:7].tolist(); res["TH5a_K"] = int(np.argmax(gaps[1:6]) + 2)
        _, memb = kmeans2(v[:, :3], 3, seed=2, minit="++")
        from itertools import permutations
        pred = memb[st]
        def ari(a, b):
            from math import comb
            ct = np.zeros((a.max() + 1, b.max() + 1))
            for x, y in zip(a, b): ct[x, y] += 1
            s = sum(comb(int(n_), 2) for n_ in ct.ravel()); sa = sum(comb(int(n_), 2) for n_ in ct.sum(1)); sb = sum(comb(int(n_), 2) for n_ in ct.sum(0))
            N = comb(len(a), 2); e = sa * sb / N; return (s - e) / (0.5 * (sa + sb) - e)
        res["TH5b_ARI"] = float(ari(lab, pred))
res["TH5c_rates"] = rates
ok = [(1 / T, np.log(r_)) for T, r_, e in rates if e > 0]
if len(ok) >= 2:
    sl = np.polyfit([a for a, _ in ok], [b for _, b in ok], 1)[0]; res["TH5c_slope"] = float(sl); res["TH5c_minus_dU"] = -dU
print(json.dumps(res, indent=1))
