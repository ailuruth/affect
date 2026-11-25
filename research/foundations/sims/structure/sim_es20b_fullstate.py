"""ES20b: factored per-need values vs full-state linear monolithic value under need drift. See PREDICTIONS.md."""
import json, math
import numpy as np
T = 3000
def run(seed, arm, N, P):
    r = np.random.default_rng(seed); re = np.random.default_rng(seed + 2000); rt = np.random.default_rng(seed + 4000)
    E = np.full((N, N), 0.02); np.fill_diagonal(E, 0.3)  # E[o] effect of option o
    fast = [int(r.integers(0, N)) for _ in range(T // P + 1)]; noise = 0.05 * r.standard_normal((T, N))
    d = lambda v: 0.5 * float(v @ v); b = np.zeros(N); S = np.zeros((N, N)); C = np.zeros(N); Wq = np.zeros((N, 2 * N + 1)); cost = []
    phi = lambda v: np.concatenate([[1.0], v, v * v])
    for t in range(T):
        dr = np.full(N, 0.02); dr[fast[t // P]] = 0.15; b = b - dr
        explore = np.linalg.norm(np.maximum(-b, 0)) > 0.1 and re.random() < 0.1
        if explore: o = int(re.integers(0, N))
        else:
            if arm == "factored":
                Eh = np.where(C[:, None] > 0, S / np.maximum(C[:, None], 1), 0.0); v = np.array([d(b) - d(b + Eh[k]) for k in range(N)])
            else:
                v = Wq @ phi(b)
            o = int(rt.choice(np.flatnonzero(v >= v.max() - 1e-12))) if v.max() > 0.002 else -1
        if t >= 500: cost.append(d(b))
        if o >= 0:
            s = int(np.argmin(b)); db = E[o] + noise[t]; rew = d(b) - d(b + db); b = b + db
            p = phi(b - db); S[o] += db; C[o] += 1; Wq[o] += 0.1 * (rew - Wq[o] @ p) * p / (1 + p @ p)
    return float(np.mean(cost))
out = {}; LR = {}
for N in (2, 8):
    for P in (200, 25):
        f = np.array([run(s, "factored", N, P) for s in range(40)]); m = np.array([run(s, "mono", N, P) for s in range(40)])
        lr = np.log(f / m); LR[(N, P)] = lr; mu, se = lr.mean(), lr.std(ddof=1) / math.sqrt(40)
        out[f"N{N}_P{P}"] = dict(median_factored=float(np.median(f)), median_mono=float(np.median(m)), geo_ratio=float(np.exp(mu)), ci=[float(np.exp(mu - 1.96 * se)), float(np.exp(mu + 1.96 * se))], wins=int((lr < 0).sum()))
def diff(a, b):
    x = LR[a] - LR[b]; mu, se = x.mean(), x.std(ddof=1) / math.sqrt(40); return dict(mean_logdiff=float(mu), ci=[float(mu - 1.96 * se), float(mu + 1.96 * se)])
out["ES20_2_N8_minus_N2_at_P25"] = diff((8, 25), (2, 25)); out["ES20_3_P25_minus_P200_at_N8"] = diff((8, 25), (8, 200))
print(json.dumps(out, indent=1))
