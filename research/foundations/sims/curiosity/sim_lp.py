"""Shared curiosity toy: learning progress as a satiable body variable. See PREDICTIONS.md."""
import json
import numpy as np
r = np.random.default_rng(0)
def err(ch, n):
    if ch == "L1": return 0.05 + 0.95 * np.exp(-n / 20)
    if ch == "L2": return 0.05 + 0.95 * np.exp(-n / 80)
    if ch == "N": return 1.0 + 0.3 * r.standard_normal()
    return 0.05 + 0.01 * r.standard_normal()
CH = ["L1", "L2", "N", "B"]
def lp_est(hist):
    if len(hist) < 10: return 0.2
    return float(np.mean(hist[-10:-5]) - np.mean(hist[-5:]))
def agent_lp(T=600):
    n = {c: 0 for c in CH}; hist = {c: [] for c in CH}; blp = 0.0; seq = []; learned_at = None
    for t in range(T):
        mu = -2 * (blp - 0.01)
        ch = max(CH, key=lambda c: mu * (lp_est(hist[c]) - blp))
        e = err(ch, n[ch]); n[ch] += 1; hist[ch].append(e)
        got = lp_est(hist[ch]) if len(hist[ch]) >= 10 else 0.0
        blp += (got - blp) / 10; seq.append(ch)
    return seq, n
def agent_pred(T=600):
    n = {c: 0 for c in CH}; bp = 0.95; seq = []
    for t in range(T):
        exp_err = {"L1": 0.05 + 0.95 * np.exp(-n["L1"] / 20), "L2": 0.05 + 0.95 * np.exp(-n["L2"] / 80), "N": 1.0, "B": 0.05}
        mu = -2 * (bp - 0.6); ch = max(CH, key=lambda c: mu * ((1 - exp_err[c]) - bp) / 10)
        e = err(ch, n[ch]); n[ch] += 1; bp += ((1 - e) - bp) / 10; seq.append(ch)
    return seq
def agent_surp(T=600, H=200, g=0.99):
    n = {c: 0 for c in CH}; seq = []
    def fc(c):
        tot, m = 0.0, n[c]
        for k in range(H):
            e = {"L1": 0.05 + 0.95 * np.exp(-m / 20), "L2": 0.05 + 0.95 * np.exp(-m / 80), "N": 1.0, "B": 0.05}[c]; tot += g ** k * e
            if c in ("L1", "L2"): m += 1
        return tot
    for t in range(T):
        ch = min(CH, key=fc); n[ch] += 1; seq.append(ch)
    return seq
seq, n = agent_lp()
e_now = lambda c, m: 0.05 + 0.95 * np.exp(-m / (20 if c == "L1" else 80))
# phase while any learnable channel has e > 0.1
cnt = {c: 0 for c in CH}; phase1 = []; learned_step = None
for t, c in enumerate(seq):
    if learned_step is None and e_now("L1", cnt["L1"]) <= 0.1 and e_now("L2", cnt["L2"]) <= 0.1: learned_step = t
    (phase1 if learned_step is None else []).append(c); cnt[c] += 1
def first_majority(c, w=20):
    for t in range(len(seq) - w):
        if sum(x == c for x in seq[t:t + w]) > w / 2: return t
    return None
post = seq[learned_step:] if learned_step is not None else []
res = dict(LP1=dict(N_frac=float(np.mean([x == "N" for x in phase1])) if phase1 else None, B_frac=float(np.mean([x == "B" for x in phase1])) if phase1 else None, phase1_len=len(phase1)),
           LP2=dict(e_L1_final=float(e_now("L1", n["L1"])), e_L2_final=float(e_now("L2", n["L2"])), first_major_L1=first_majority("L1"), first_major_L2=first_majority("L2")),
           LP3=dict(learned_step=learned_step, post_fracs={c: float(np.mean([x == c for x in post])) for c in CH} if post else None),
           LP4=dict(pred_N_frac=float(np.mean([x == "N" for x in agent_pred()])), surp_B_frac=float(np.mean([x == "B" for x in agent_surp()]))),
           visits=n)
print(json.dumps(res, indent=1))
