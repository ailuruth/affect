"""TH8: work cost of regulation vs time allowed. See PREDICTIONS.md."""
import json
import numpy as np
T, DT = 0.25, 0.001
def run(tau, n=2000, seed=0):
    r = np.random.default_rng(seed); steps = int(tau / DT)
    # equilibrium start at lambda=-0.5: long burn-in
    x = -np.ones(n); lam0 = -0.5
    for _ in range(20000):
        x += -(4 * x * (x * x - 1) - lam0) * DT + np.sqrt(2 * T * DT) * r.standard_normal(n)
    W = np.zeros(n); lamdot = 1.0 / tau
    for k in range(steps):
        lam = -0.5 + k * DT / tau
        W += (-x) * lamdot * DT
        x += -(4 * x * (x * x - 1) - lam) * DT + np.sqrt(2 * T * DT) * r.standard_normal(n)
    return float(W.mean()), float(W.std(ddof=1) / np.sqrt(n)), float((x > 0).mean())
out = {}
for tau in (0.5, 1, 2, 4, 8, 16):
    m, se, fr = run(tau); out[str(tau)] = dict(W=m, se=se, frac_right=fr, excess_times_tau=m * tau)
print(json.dumps(out, indent=1))
