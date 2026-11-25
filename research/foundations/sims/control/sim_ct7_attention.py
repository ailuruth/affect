"""CT7: observer budget allocated by regulation sensitivity. See PREDICTIONS.md second batch."""
import json
import numpy as np
DT = 0.01; T = 600.0
def run(seed, rule):
    r = np.random.default_rng(seed); n = int(T / DT); b = m = 0.0; yh = {"A": 0.0, "B": 0.0}; ch = {"A": 0.5, "B": 0.5}
    c = {"A": 0.8, "B": 0.1}; w = {"A": 1.57, "B": 1.1}; pev = {"A": 1.0, "B": 1.0}; L = {"A": 5.0, "B": 5.0}; E = []; LA = []
    for k in range(n):
        t = k * DT; yu = {p: np.sin(w[p] * t) for p in "AB"}
        for p in "AB":
            y = yu[p] + 0.3 * r.standard_normal(); err = y - yh[p]; yh[p] += L[p] * err * DT; pev[p] += (err ** 2 - pev[p]) * DT / 2
        if rule and k % 100 == 0:
            sc = {p: ch[p] * pev[p] for p in "AB"}; tot = sum(sc.values()); L = {p: 10 * sc[p] / tot for p in "AB"}
        u = -b - 0.1 * m - sum(ch[p] * yh[p] for p in "AB")
        for p in "AB": ch[p] += (0.5 * b * yh[p] - 0.001 * ch[p]) * DT
        b += (-0.1 * b + u + sum(c[p] * yu[p] for p in "AB")) * DT; m += b * DT
        if t > T - 300: E.append(b); LA.append(L["A"] / 10)
    return float(np.sqrt(np.mean(np.square(E)))), float(np.mean(LA))
R = [run(s, True) for s in range(10)]; U = [run(s, False) for s in range(10)]
print(json.dumps(dict(rule_rms=float(np.mean([x[0] for x in R])), equal_rms=float(np.mean([x[0] for x in U])), ratio=float(np.mean([x[0] for x in R]) / np.mean([x[0] for x in U])), rule_share_A=float(np.mean([x[1] for x in R]))), indent=1))
