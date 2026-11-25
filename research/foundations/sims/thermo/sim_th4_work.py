"""TH4: valence as work vs Costate-style -dV/dt. See PREDICTIONS.md."""
import json
import numpy as np
from scipy.special import expit
DT = 0.001; Tend = 80.0; k = 50.0; RHO = 0.1
def s_of(t):
    on = lambda c: expit(k * (t - c))
    return 1.0 - on(20.0) + on(60.0)
def ds_of(t):
    d = lambda c: k * expit(k * (t - c)) * (1 - expit(k * (t - c)))
    return -d(20.0) + d(60.0)
r = np.random.default_rng(0); n = int(Tend / DT)
b = 0.8; B, V, A = [], [], []
for i in range(n):
    t = i * DT
    s, ds = s_of(t), ds_of(t)
    V.append(-(-ds * b))           # valence = -dU/dt at fixed b, U = 0.5(b-0.8)^2 - s b
    gradU = (b - 0.8) - s
    A.append(gradU ** 2)
    B.append(b)
    b += (-0.5 * b - gradU) * DT + 0.05 * np.sqrt(DT) * r.standard_normal()
B, V, A = map(np.array, (B, V, A)); t = np.arange(n) * DT
win = lambda lo, hi: (t >= lo) & (t < hi)
out = {}
out["TH4a_integral_v_departure_19_21"] = float(V[win(19, 21)].sum() * DT)
out["TH4a_integral_v_return_59_61"] = float(V[win(59, 61)].sum() * DT)
out["TH4a_max_abs_v_between_switches"] = float(np.abs(V[win(22, 58)]).max())
out["TH4a_b_at_departure"] = float(B[int(20 / DT)]); out["TH4a_b_at_return"] = float(B[int(60 / DT)])
out["TH4b_min_arousal_absence_22_58"] = float(A[win(22, 58)].min())
# Costate-style V: discounted cost-to-go of 0.5(b-0.8)^2 along the realized path (deterministic future)
stride = 10; bs = B[::stride]; dts = DT * stride; g = np.exp(-RHO * dts); acc = 0.0; Vc = np.zeros(len(bs))
for i in range(len(bs) - 1, -1, -1):
    acc = 0.5 * (bs[i] - 0.8) ** 2 * dts + g * acc; Vc[i] = acc
vc = -np.diff(Vc) / dts; tc = np.arange(len(vc)) * dts
out["TH4c_costate_style_abs_integral_25_55"] = float(np.abs(vc[(tc >= 25) & (tc < 55)]).sum() * dts)
print(json.dumps(out, indent=1))
