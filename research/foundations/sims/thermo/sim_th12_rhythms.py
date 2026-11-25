"""TH12: Boltzmann-preserving circulation vs limit-cycle rhythm. See PREDICTIONS.md seventh batch."""
import json
import numpy as np
T, DT, TAU = 0.5, 0.01, 10.0; NSTEP = int(TAU / DT)
def gradU(z, o):
    g = z - o; g[:, 0] += 0.4 * z[:, 0] * z[:, 1] ** 2; g[:, 1] += 0.4 * z[:, 1] * z[:, 0] ** 2; return g
rot = lambda v: np.stack([-v[:, 1], v[:, 0]], 1)
def run(proto, arm, n=2000, seed=0):
    r = np.random.default_rng(seed); z = np.zeros((n, 2)); W = []
    for c in range(60):
        w = np.zeros(n)
        for k in range(NSTEP):
            o, od = proto(k * DT)
            if c >= 20: w += -np.sum((z - o) * od, 1) * DT
            g = gradU(z, o)
            if arm == 1: drift = -g - rot(g)
            else:
                d = z - o; drift = -g + (1 - np.sum(d * d, 1, keepdims=True)) * d + rot(d)
            z = z + drift * DT + np.sqrt(2 * T * DT) * r.standard_normal(z.shape)
        if c >= 20: W.append(w.mean())
    v = -np.array(W) / TAU; return float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(v)))
def rotp(r_, w):
    return lambda t: (np.array([r_ * np.cos(w * t), r_ * np.sin(w * t)]), np.array([-r_ * w * np.sin(w * t), r_ * w * np.cos(w * t)]))
def fourier(seed):
    r = np.random.default_rng(seed); a = r.normal(0, 0.5, (2, 3)); b = r.normal(0, 0.5, (2, 3)); w = 2 * np.pi / TAU * np.arange(1, 4)
    return lambda t: ((a * np.cos(w * t) + b * np.sin(w * t)).sum(1), (-a * w * np.sin(w * t) + b * w * np.cos(w * t)).sum(1))
out = {}
for arm in (1, 2):
    res = {}
    for r_ in (1.0, 2.0):
        for w in (0.5, -0.5): res[f"rot_r{r_}_w{w}"] = run(rotp(r_, w), arm)
    rnd = [run(fourier(100 + s), arm, n=1000) for s in range(20)]
    res["random_max_v_over_se"] = float(max(m / se for m, se in rnd)); res["random_n_pos_2se"] = int(sum(m > 2 * se for m, se in rnd))
    out[f"arm{arm}"] = res
print(json.dumps(out, indent=1))
