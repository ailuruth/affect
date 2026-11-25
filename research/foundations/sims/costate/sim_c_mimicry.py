"""C: mimicry as shrinkage onto the agent's own expressive repertoire. Parameters in PREDICTIONS.md."""
import json
import numpy as np

rng = np.random.default_rng(7)
NA, NX, C, TAU, FS = 12, 8, 4.0, 1.0, 30
s = np.array([0.1, 0.3, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0])
U, _ = np.linalg.qr(rng.standard_normal((NA, NA))); Vv, _ = np.linalg.qr(rng.standard_normal((NX, NX)))
G = U[:, :NX] @ np.diag(s) @ Vv.T
null = U[:, NX]  # orthogonal to range(G)


def simulate(ytil, w, noise=0.0, seed=0):
    r = np.random.default_rng(seed); x = np.zeros(NX); dt = 1 / FS; Y = []
    for t in range(len(ytil)):
        dx = (-C * x + w * G.T @ (ytil[t] - G @ x)) / TAU
        x = x + dt * dx + (noise * np.sqrt(dt) * r.standard_normal(NX) if noise else 0)
        Y.append(G @ x)
    return np.array(Y)


out = {}
T = 3 * FS
gains = []
for i in range(NX):
    Y = simulate(np.tile(U[:, i], (T, 1)), 4.0)
    gains.append(float(Y[-1] @ U[:, i]))
pred = 4 * s ** 2 / (C + 4 * s ** 2)
out["CM1_max_abs_gain_error"] = float(np.max(np.abs(np.array(gains) - pred)))
out["CM1_gains"] = gains; out["CM1_pred"] = pred.tolist()
Yn = simulate(np.tile(null, (T, 1)), 4.0); out["CM2_null_gain"] = float(np.linalg.norm(Yn[-1]))
Y1 = simulate(np.tile(U[:, 4], (T, 1)), 4.0); proj = Y1 @ U[:, 4]
out["CM3_fraction_complete_500ms"] = float(proj[int(0.5 * FS) - 1] / proj[-1])
g_hi = simulate(np.tile(U[:, 2], (T, 1)), 4.0)[-1] @ U[:, 2]; g_lo = simulate(np.tile(U[:, 2], (T, 1)), 1.0)[-1] @ U[:, 2]
out["CM4_gain_ratio_w4_over_w1_s0.5"] = float(g_hi / g_lo)

# C-M5: E3 synchrony test with surrogates
Tn = 10 * 60 * FS; dt = 1 / FS; r = np.random.default_rng(11); yt = np.zeros((Tn, NA)); z = np.zeros(NA)
for t in range(Tn):
    z = z + dt * (-z / 2.0) + np.sqrt(2 * dt / 2.0) * r.standard_normal(NA); yt[t] = z


def wcc_score(a, b, W=300, winc=50, L=50):
    zs = []
    for w0 in range(L, len(a) - W - L, winc):
        x = a[w0:w0 + W]; x = (x - x.mean()) / x.std()
        for lag in range(-L, L + 1):
            y = b[w0 + lag:w0 + lag + W]; y = (y - y.mean()) / y.std()
            rr = np.clip((x * y).mean(), -0.999999, 0.999999); zs.append(abs(np.arctanh(rr)))
    return float(np.mean(zs))


def surrogates(a, b, kind, n, rng):
    out = []
    for _ in range(n):
        if kind == "segment":
            m = 300; segs = [b[i:i + m] for i in range(0, len(b) - len(b) % m, m)]; rng.shuffle(segs); bb = np.concatenate(segs)
            aa = a[:len(bb)]
        else:
            cut = rng.integers(int(0.2 * len(b)), int(0.8 * len(b))); bb = np.concatenate([b[cut:], b[:cut]]); aa = a
        out.append(wcc_score(aa, bb))
    return np.array(out)


for name, w in [("intact_w4", 4.0), ("lesion_w0", 0.0)]:
    Y = simulate(yt, w, noise=0.05, seed=3)
    a = (yt @ U[:, 7])[::3]; b = (Y @ U[:, 7])[::3]  # 10 Hz
    obs = wcc_score(a, b)
    rs = np.random.default_rng(5)
    seg = surrogates(a, b, "segment", 1000, rs); sld = surrogates(a, b, "sliding", 1000, rs)
    out[f"CM5_{name}"] = dict(score=obs, seg95=float(np.percentile(seg, 95)), slide95=float(np.percentile(sld, 95)),
                              beats_both=bool(obs > np.percentile(seg, 95) and obs > np.percentile(sld, 95)),
                              beats_either=bool(obs > np.percentile(seg, 95) or obs > np.percentile(sld, 95)))
print(json.dumps(out, indent=1))
