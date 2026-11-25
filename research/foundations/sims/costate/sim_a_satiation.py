"""A: satiation as monotonicity of the costate; invariance of valence and arousal. Parameters in PREDICTIONS.md."""
import json
import numpy as np

DT = 1 / 60; GAM = np.exp(-1.0 * DT)
US = np.array([0, .25, .5, .75, 1.0])


def make(S=(1.0, 1.0)):
    sb, se = S
    bg = np.linspace(0, 3, 151) * sb; eg = np.linspace(-1.5, 1, 126) * se
    def step(b, e, u):  # dynamics in scaled coordinates
        return b + DT * (-1.0 * b + 3 * u * sb), e + DT * (-0.5 * u * se + 0.2 * (1 * se - e))
    return bg, eg, step


def interp(V, bg, eg, b, e):
    b = np.clip(b, bg[0], bg[-1]); e = np.clip(e, eg[0], eg[-1])
    ib = np.clip(np.searchsorted(bg, b) - 1, 0, len(bg) - 2); ie = np.clip(np.searchsorted(eg, e) - 1, 0, len(eg) - 2)
    tb = (b - bg[ib]) / (bg[ib + 1] - bg[ib]); te = (e - eg[ie]) / (eg[ie + 1] - eg[ie])
    return ((1 - tb) * (1 - te) * V[ib, ie] + tb * (1 - te) * V[ib + 1, ie] + (1 - tb) * te * V[ib, ie + 1] + tb * te * V[ib + 1, ie + 1])


def solve(cost, S=(1.0, 1.0), sweeps=4000):
    bg, eg, step = make(S)
    B, E = np.meshgrid(bg, eg, indexing="ij")
    c = cost(B / S[0], E / S[1]) * DT
    nxt = [step(B, E, u) for u in US]
    V = np.zeros_like(B)
    for _ in range(sweeps):
        Q = np.stack([c + GAM * interp(V, bg, eg, *n) for n in nxt])
        V = Q.min(0)
    pol = US[Q.argmin(0)]
    return bg, eg, step, V, pol


homeo = lambda b, e: (b - 0.8) ** 2 + (e - 1) ** 2
maxim = lambda b, e: -b + (e - 1) ** 2


def rollout(bg, eg, step, V, cost, S, hours=48):
    b, e = 0.0, 1.0 * S[1]; traj = []
    for _ in range(int(hours * 60)):
        q = [cost(*(np.array(step(b, e, u)) / np.array(S))) * DT + GAM * interp(V, bg, eg, *step(b, e, u)) for u in US]
        u = US[int(np.argmin(q))]
        traj.append((b, e, u)); b, e = step(b, e, u)
    return np.array(traj)


def grad(V, bg, eg, b, e, h=1e-3):
    db = (interp(V, bg, eg, b + h * (bg[1]-bg[0]) / .02, e) - interp(V, bg, eg, b - h * (bg[1]-bg[0]) / .02, e)) / (2 * h * (bg[1]-bg[0]) / .02)
    de = (interp(V, bg, eg, b, e + h * (eg[1]-eg[0]) / .02) - interp(V, bg, eg, b, e - h * (eg[1]-eg[0]) / .02)) / (2 * h * (eg[1]-eg[0]) / .02)
    return -np.array([db, de])


out = {}
bg, eg, step, V, pol = solve(homeo)
d2 = V[2:, :] - 2 * V[1:-1, :] + V[:-2, :]
out["A1_min_second_diff_b"] = float(d2.min())
mu_b = -(V[1:, :] - V[:-1, :]) / (bg[1] - bg[0])
out["A2_max_increase_mu_b"] = float(np.diff(mu_b, axis=0).max())
tr = rollout(bg, eg, step, V, homeo, (1, 1))
out["A3_bids_at_b_ge_0.9_policy_cells"] = int(((pol > 0) & (bg[:, None] >= 0.9)).sum())
out["A3_bids_at_b_ge_0.9_trajectory"] = int(((tr[:, 2] > 0) & (tr[:, 0] >= 0.9)).sum())
out["A3_mean_b_last24h"] = float(tr[-1440:, 0].mean())
bgm, egm, stepm, Vm, polm = solve(maxim)
trm = rollout(bgm, egm, stepm, Vm, maxim, (1, 1))
out["A4_maximizer_mean_b_last24h"] = float(trm[-1440:, 0].mean())
out["A4_ratio"] = out["A4_maximizer_mean_b_last24h"] / out["A3_mean_b_last24h"]
# A5 invariance: re-solve in rescaled units, evaluate along the same physical trajectory
S = (10.0, 0.1)
bgs, egs, steps_, Vs, pols = solve(homeo, S)
vals = np.array([interp(V, bg, eg, b, e) for b, e, _ in tr]); vals_s = np.array([interp(Vs, bgs, egs, b * S[0], e * S[1]) for b, e, _ in tr])
val = -np.diff(vals) / DT; val_s = -np.diff(vals_s) / DT
out["A5_valence_max_rel_err"] = float(np.max(np.abs(val - val_s)) / np.max(np.abs(val)))
Sig = np.diag([0.05 ** 2, 0.05 ** 2]); SigS = np.diag(S) @ Sig @ np.diag(S)
ar, ar_s, n, n_s = [], [], [], []
for b, e, _ in tr[::30]:
    m = grad(V, bg, eg, b, e); ms = grad(Vs, bgs, egs, b * S[0], e * S[1])
    ar.append(np.sqrt(m @ Sig @ m)); ar_s.append(np.sqrt(ms @ SigS @ ms)); n.append(np.linalg.norm(m)); n_s.append(np.linalg.norm(ms))
ar, ar_s, n, n_s = map(np.array, (ar, ar_s, n, n_s))
out["A5_arousal_max_rel_err"] = float(np.max(np.abs(ar - ar_s)) / np.max(ar))
out["A5_rawnorm_ratio_range"] = [float((n_s / n).min()), float((n_s / n).max())]
print(json.dumps(out, indent=1))
