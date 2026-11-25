"""TH3: which lesion removes the human's following. See PREDICTIONS.md."""
import json, sys
import numpy as np
sys.path.insert(0, "..")

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

from synchrony import wcc_score, surrogates

out = {}
out["TH3a_analytic_intact"] = lyap_analytic(KAP, KAP)
out["TH3a_analytic_mimicry_lesion"] = lyap_analytic(0.0, KAP)
# numerical check without pulses (long run)
for arm in ("intact", "mimicry_lesion"):
    A, H = simulate(arm, 99, minutes=60, pulses=False)
    out[f"TH3a_sim_zero_lag_rho_{arm}"] = float(np.corrcoef(A, H)[0, 1])
for arm in ("intact", "mimicry_lesion", "emotional_lesion"):
    rows = []
    for seed in range(10):
        A, H = simulate(arm, seed)
        if A.std() == 0: rows.append(dict(score=0, beats_both=False)); continue
        obs = wcc_score(A, H); rs = np.random.default_rng(100 + seed)
        seg = surrogates(A, H, "segment", 1000, rs); sld = surrogates(A, H, "sliding", 1000, rs)
        rows.append(dict(score=obs, seg95=float(np.percentile(seg, 95)), sld95=float(np.percentile(sld, 95)),
                         beats_both=bool(obs > np.percentile(seg, 95) and obs > np.percentile(sld, 95))))
    out[f"TH3b_{arm}"] = dict(n_beats_both=sum(r_["beats_both"] for r_ in rows), mean_score=float(np.mean([r_["score"] for r_ in rows])), runs=rows)
print(json.dumps(out, indent=1))
