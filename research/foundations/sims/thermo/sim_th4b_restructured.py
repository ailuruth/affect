"""TH4b: valence on the restructured flow (body as input). See PREDICTIONS.md sixth batch."""
import json
import numpy as np
DT, T = 0.001, 0.05; e = np.array([1.0, 0.5])
def run_schedule(present_fn, Tend, n=100, seed=0):
    r = np.random.default_rng(seed); steps = int(Tend / DT)
    b = 0.8; z = np.zeros((n, 2)); V = np.zeros((steps, n)); VD = np.zeros(steps)
    for k in range(steps):
        s = 1.0 if present_fn(k * DT) else 0.0
        bdot = -0.5 * b + s * (1.6 - 1.5 * b)
        zstar = (b - 0.8) * e
        V[k] = -(2 * (b - 0.8) + (z - zstar) @ (-e)) * bdot   # -dU/dt|_z, with dz*/db = e so d/db of 0.5|z-z*|^2 = -(z-z*).e
        VD[k] = -2 * (b - 0.8) * bdot
        b += bdot * DT
        z += -(z - zstar) * DT + np.sqrt(2 * T * DT) * r.standard_normal((n, 2))
    return V, VD
pres = lambda t: t < 20 or t >= 60
V, VD = run_schedule(pres, 80.0)
w = lambda lo, hi: float(V[int(lo / DT):int(hi / DT)].mean(1).sum() * DT)
out = dict(TH4b1_after_return_60_62=w(60, 62), TH4b2_after_departure_20_22=w(20, 22), whole_absence_20_60=w(20, 60))
per = lambda t: (t % 80) < 40
Vp, VDp = run_schedule(per, 25 * 80.0, n=50, seed=1)
burn = int(5 * 80 / DT); cyc = int(80 / DT)
cv = [Vp[burn + i * cyc: burn + (i + 1) * cyc].mean() for i in range(20)]
cd = [VDp[burn + i * cyc: burn + (i + 1) * cyc].mean() for i in range(20)]
out["TH4b3_mean_total_v"] = float(np.mean(cv)); out["TH4b3_se_total"] = float(np.std(cv, ddof=1) / np.sqrt(20))
out["TH4b3_mean_D_part"] = float(np.mean(cd)); out["TH4b3_se_D"] = float(np.std(cd, ddof=1) / np.sqrt(20))
print(json.dumps(out, indent=1))
