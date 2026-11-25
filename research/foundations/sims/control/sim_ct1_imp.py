"""CT1: internal model of the other; mimicry scaled by relevance. See PREDICTIONS.md."""
import json
import numpy as np
from scipy.signal import correlate
DT, TEND = 0.01, 600.0
def run(c, with_im, seed=0, c0=0.5):
    r = np.random.default_rng(seed); n = int(TEND / DT)
    b = m = 0.0; ch = c0; yh = 0.0; E = np.empty(n); A = np.empty(n); Y = np.empty(n)
    for k in range(n):
        t = k * DT; yu = np.sin(1.57 * t); y = yu + 0.1 * r.standard_normal()
        yh += (y - yh) * DT / 0.05
        u = -1.0 * b - 0.1 * m
        if with_im:
            u += -ch * yh; ch += (0.5 * b * yh - 0.001 * ch) * DT
        b += (-0.1 * b + u + c * yu) * DT; m += b * DT
        E[k] = b; A[k] = 0.3 * ch * yh if with_im else 0.0; Y[k] = yu
    return E, A, Y
out = {}
E, _, _ = run(0.5, False); out["CT1_1_PI_rms_c0.5"] = float(np.sqrt(np.mean(E[-int(200 / DT):] ** 2))); out["CT1_1_analytic"] = 0.379 * 0.5
E2, A2, Y2 = run(0.5, True); out["CT1_2_IM_rms"] = float(np.sqrt(np.mean(E2[-int(200 / DT):] ** 2))); out["CT1_2_ratio"] = out["CT1_2_IM_rms"] / out["CT1_1_PI_rms_c0.5"]
a = A2[-int(200 / DT):]; yy = Y2[-int(200 / DT):]; a = (a - a.mean()) / a.std(); yy = (yy - yy.mean()) / yy.std()
L = int(1.0 / DT); cc = [np.mean(a[L:-L] * np.roll(yy, l)[L:-L]) for l in range(-L, L + 1)]
i = int(np.argmax(cc)); out["CT1_3_peak_corr"] = float(cc[i]); out["CT1_3_peak_lag_s"] = float((i - L) * DT)
amps = []
for c in (0.25, 0.5, 1.0):
    _, A, _ = run(c, True); amps.append(float(A[-int(200 / DT):].std()))
cs = np.array([0.25, 0.5, 1.0]); fit = np.polyfit(cs, amps, 1); pred = np.polyval(fit, cs)
out["CT1_3_amps"] = amps; out["CT1_3_R2"] = float(1 - np.sum((np.array(amps) - pred) ** 2) / np.sum((np.array(amps) - np.mean(amps)) ** 2))
_, A0, _ = run(0.0, True); m1 = A0[:int(60 / DT)].std(); m10 = A0[int(540 / DT):].std()
out["CT1_4_min1_std"] = float(m1); out["CT1_4_min10_std"] = float(m10); out["CT1_4_ratio"] = float(m10 / m1)
print(json.dumps(out, indent=1))
