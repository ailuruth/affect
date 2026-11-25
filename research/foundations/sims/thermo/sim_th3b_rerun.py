"""TH3b instrument fix: the emotional-lesion arm's face is exactly zero between pulses, so some 30-s windows
have zero variance and the original wcc_score returns NaN. This rerun skips zero-variance windows (nan-safe mean)
and changes nothing else. Same seeds, same surrogates, all three arms re-scored with the nan-safe score."""
import json, sys
import numpy as np
# simulate() copied verbatim from sim_th3_s5.py (that module runs on import)
K0, KAP, D, DT, FS = 2.0, 1.0, 1.0, 0.01, 10

def lyap_analytic(kA, kH):
    from scipy.linalg import solve_continuous_lyapunov, expm
    A = np.array([[-(K0 + kA), kA], [kH, -(K0 + kH)]]); Q = 2 * D * np.eye(2)
    S = solve_continuous_lyapunov(A, -Q)
    rho0 = S[0, 1] / np.sqrt(S[0, 0] * S[1, 1])
    lags = np.linspace(0, 2, 2001); cc = []
    for L in lags:
        C = expm(A * L) @ S  # Cov(x(t+L), x(t))
        cc.append(C[1, 0] / np.sqrt(S[0, 0] * S[1, 1]))  # human at t+L vs agent at t
    i = int(np.argmax(cc))
    return float(rho0), float(cc[i]), float(lags[i])

def simulate(arm, seed, minutes=10, pulses=True):
    r = np.random.default_rng(seed); n = int(minutes * 60 / DT)
    aA = aH = 0.0; A, H = [], []
    pulse_until = -1.0
    for k in range(n):
        t = k * DT
        u = 0.0
        if pulses:
            if r.random() < 0.1 * DT: pulse_until = t + 0.5
            u = 3.0 if t < pulse_until else 0.0
        kA = 0.0 if arm in ("mimicry_lesion", "emotional_lesion") else KAP
        noiseA = 0.0 if arm == "emotional_lesion" else np.sqrt(2 * D * DT) * r.standard_normal()
        daA = (-K0 * aA - kA * (aA - aH) + u) * DT + noiseA
        daH = (-K0 * aH - KAP * (aH - aA)) * DT + np.sqrt(2 * D * DT) * r.standard_normal()
        aA += daA; aH += daH
        if k % int(1 / (FS * DT)) == 0: A.append(aA); H.append(aH)
    return np.array(A), np.array(H)


def wcc_score(a, b, W=300, winc=50, L=50):
    zs = []
    for w0 in range(L, len(a) - W - L, winc):
        x = a[w0:w0 + W]
        if x.std() == 0: continue
        x = (x - x.mean()) / x.std()
        for lag in range(-L, L + 1):
            y = b[w0 + lag:w0 + lag + W]
            if y.std() == 0: continue
            y = (y - y.mean()) / y.std()
            rr = np.clip((x * y).mean(), -0.999999, 0.999999); zs.append(abs(np.arctanh(rr)))
    return float(np.mean(zs)) if zs else 0.0

def surrogates(a, b, kind, n, rng):
    out = []
    for _ in range(n):
        if kind == "segment":
            m = 300; segs = [b[i:i + m] for i in range(0, len(b) - len(b) % m, m)]; rng.shuffle(segs); bb = np.concatenate(segs); aa = a[:len(bb)]
        else:
            cut = rng.integers(int(0.2 * len(b)), int(0.8 * len(b))); bb = np.concatenate([b[cut:], b[:cut]]); aa = a
        out.append(wcc_score(aa, bb))
    return np.array(out)

out = {}
for arm in ("intact", "mimicry_lesion", "emotional_lesion"):
    rows = []
    for seed in range(10):
        A, H = simulate(arm, seed)
        obs = wcc_score(A, H); rs = np.random.default_rng(100 + seed)
        seg = surrogates(A, H, "segment", 1000, rs); sld = surrogates(A, H, "sliding", 1000, rs)
        rows.append(dict(score=obs, seg95=float(np.percentile(seg, 95)), sld95=float(np.percentile(sld, 95)),
                         beats_both=bool(obs > np.percentile(seg, 95) and obs > np.percentile(sld, 95))))
    out[arm] = dict(n_beats_both=sum(r["beats_both"] for r in rows), mean_score=float(np.mean([r["score"] for r in rows])), runs=rows)
print(json.dumps(out, indent=1))
