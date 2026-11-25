"""ES10b: ES10 with fair controls (one-scale Kalman with elapsed time; bias-corrected slow EMA). See PREDICTIONS.md."""
import json, math
import numpy as np
NP, T, K = 20, 3000, 4
W = 0.5 * np.array([[1, 0.8, 0, 0], [0, 0, 1, 0.8]]); A_F = math.exp(-1 / 40); SF = 0.5; QS = 0.01 ** 2; R = 0.1 ** 2
def run(seed, arm):
    rw = np.random.default_rng(seed); MU = rw.standard_normal((NP, 4)) @ W.T; S = np.zeros((NP, 2)); ep = np.zeros(NP, int); post = np.zeros(NP, int)
    pres = [rw.choice(NP, K, replace=False) for _ in range(T)]; steps_s = 0.01 * rw.standard_normal((T, NP, 2)); epstart = rw.random((T, NP)) < 0.003
    re = np.random.default_rng(seed + 2000); b = np.zeros(2); d = lambda v: 0.5 * (v * v).sum(-1)
    m = np.zeros((NP, 2, 2)); P = np.tile(np.diag([0.25, SF ** 2]), (NP, 1, 1)); Fm = np.diag([1.0, A_F]); Q = np.diag([QS, (1 - A_F ** 2) * SF ** 2])
    ema = np.zeros((NP, 2)); tot = np.zeros((NP, 2)); cnt = np.zeros(NP)
    m1 = np.zeros((NP, 2)); P1 = np.full(NP, 0.25 + SF ** 2); Q1 = QS + (1 - A_F ** 2) * SF ** 2
    cost = []; ph = {k: [0, 0] for k in ("normal", "episode", "post")}
    for t in range(T):
        S += steps_s[t]; post = np.maximum(post - 1, 0); ending = ep == 1; post[ending] = 40; ep = np.maximum(ep - 1, 0)
        new = epstart[t] & (ep == 0); ep[new] = 40; post[new] = 0
        truth = MU + S + np.where((ep > 0)[:, None], -1.5 * MU, 0.0)
        m = m @ Fm.T; P = Fm @ P @ Fm.T + Q; P1 = P1 + Q1
        drift = np.array([0.2, 0.02]) if (t // 50) % 2 == 0 else np.array([0.02, 0.2]); b = b - drift; Pp = pres[t]
        if arm == "oracle": est = truth[Pp]
        elif arm == "kalman": est = m[Pp].sum(-1)
        elif arm == "kalman1": est = m1[Pp]
        elif arm == "ema_fast": est = ema[Pp]
        elif arm == "ema_slow_bc": est = np.where(cnt[Pp, None] > 0, ema[Pp] / np.maximum(1 - 0.95 ** cnt[Pp, None], 1e-9), 0.0)
        else: est = np.where(cnt[Pp, None] > 0, tot[Pp] / np.maximum(cnt[Pp, None], 1), 0.0)
        explore = np.linalg.norm(np.maximum(-b, 0)) > 0.1 and re.random() < 0.1
        if explore: ch = int(re.integers(0, K))
        else:
            v = d(b) - d(b + est); ch = int(np.argmax(v)) if v.max() > 0.01 else -1
        if t >= 500:
            cost.append(d(b))
            for j, p in enumerate(Pp):
                k = "episode" if ep[p] > 0 else ("post" if post[p] > 0 else "normal"); ph[k][0] += int(ch == j and not explore); ph[k][1] += 1
        if ch >= 0:
            p = Pp[ch]; y = truth[p] + 0.1 * re.standard_normal(2); b = b + truth[p] + (y - truth[p]) * 0  # body gets true effect
            for n in range(2):
                Pn = P[p]; Sg = Pn.sum() + R; Kg = Pn.sum(1) / Sg; m[p, n] = m[p, n] + Kg * (y[n] - m[p, n].sum()); 
            P[p] = P[p] - np.outer(P[p].sum(1), P[p].sum(0)) / (P[p].sum() + R)
            a = 0.5 if arm == "ema_fast" else 0.05; ema[p] += a * (y - ema[p]); tot[p] += y; cnt[p] += 1
            Kk = P1[p] / (P1[p] + R); m1[p] += Kk * (y - m1[p]); P1[p] *= (1 - Kk)
    rate = {k: (v[0] / v[1] if v[1] else float("nan")) for k, v in ph.items()}
    return float(np.mean(cost)), rate
out = {}
for arm in ("kalman", "kalman1", "ema_slow_bc", "ema_fast"):
    R_ = [run(s, arm) for s in range(120)]; out[arm] = dict(costs=[c for c, _ in R_], median=float(np.median([c for c, _ in R_])), runaway=int(sum(c > 5 for c, _ in R_)))
def paired(a, b):
    lr = np.log(np.array(out[a]["costs"]) / np.array(out[b]["costs"])); mm, se = lr.mean(), lr.std(ddof=1) / math.sqrt(len(lr))
    return dict(geo_ratio=float(np.exp(mm)), ci=[float(np.exp(mm - 1.96 * se)), float(np.exp(mm + 1.96 * se))], wins=int((lr < 0).sum()), n=len(lr))
out["checks"] = dict(ES10b_1=paired("kalman", "kalman1"), ES10b_2=paired("kalman", "ema_slow_bc"), ES10b_3=paired("kalman", "ema_fast"))
print(json.dumps(out, indent=1))
