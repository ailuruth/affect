"""ES16: does the shared relevance prior C-hat help regulate new people; is a wrong prior corrected? See PREDICTIONS.md."""
import json, math
import numpy as np
DT, LAM, K, GAM, SIG, TAU = 0.05, 0.1, 1.0, 0.05, 0.01, 2.0
W = 0.5 * np.array([[1, 0.8, 0, 0], [0, 0, 1, 0.8]]); a_ou = math.exp(-DT / TAU)
def visit(r, c, chat, steps):
    b = np.zeros(2); y = r.standard_normal(2); costs = []
    for k in range(steps):
        y = a_ou * y + math.sqrt(1 - a_ou ** 2) * r.standard_normal(2)
        u = -K * b - chat * y; b = b + DT * (-LAM * b + u + c * y); chat = chat + DT * (GAM * b * y - SIG * chat); costs.append(0.5 * b @ b)
    return np.array(costs), chat
def run(seed, arm):
    r = np.random.default_rng(seed); A = r.standard_normal((8, 4)) / 2; Z = r.standard_normal((30, 4)); X = Z @ A.T + 0.3 * r.standard_normal((30, 8)); C = Z @ W.T
    rv = np.random.default_rng(seed + 500); XX, CC = [], []; early = []
    for p in range(30):
        if arm == "prior" and XX:
            Xa = np.array(XX); Ya = np.array(CC); Wh = np.linalg.solve(Xa.T @ Xa + np.eye(8), Xa.T @ Ya); c0 = X[p] @ Wh
        else: c0 = np.zeros(2)
        costs, chat = visit(rv, C[p], c0.copy(), int(120 / DT)); XX.append(X[p]); CC.append(chat)
        if p >= 9: early.append(costs[: int(30 / DT)].mean())
    ratio = None
    if arm == "prior":
        j = int(np.argmax(np.linalg.norm(C, axis=1))); xs = X[j] + 0.3 * r.standard_normal(8)
        Xa = np.array(XX); Ya = np.array(CC); Wh = np.linalg.solve(Xa.T @ Xa + np.eye(8), Xa.T @ Ya); c0 = xs @ Wh
        _, chat = visit(rv, np.zeros(2), c0.copy(), int(60 / DT)); ratio = float(np.linalg.norm(chat) / max(np.linalg.norm(c0), 1e-12))
    return float(np.mean(early)), ratio
P = [run(s, "prior") for s in range(40)]; Zr = [run(s, "zero") for s in range(40)]
lr = np.log(np.array([p[0] for p in P]) / np.array([z[0] for z in Zr])); m, se = lr.mean(), lr.std(ddof=1) / math.sqrt(40)
out = dict(early_cost_prior=float(np.median([p[0] for p in P])), early_cost_zero=float(np.median([z[0] for z in Zr])),
           ES16_1=dict(geo_ratio=float(np.exp(m)), ci=[float(np.exp(m - 1.96 * se)), float(np.exp(m + 1.96 * se))], wins=int((lr < 0).sum()), n=40),
           ES16_2_median_ratio=float(np.median([p[1] for p in P])), ES16_2_leak_only=math.exp(-SIG * 60), stranger_ratios=[round(p[1], 3) for p in P])
print(json.dumps(out, indent=1))
