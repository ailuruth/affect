"""K3. Placation through the agent's own body (Principle 6).

The partner head of M is action-blind, but the own-body head (i) 'next b' is not, and C (concern) and
V (aversive load) are body variables inside D(b) (s2.1: C set point 0, dead-band 0.05, weight 0.8),
driven by the partner's inferred body.  Trained by predictive likelihood on lived data (own acts are
inputs of head (i); only the partner head is masked), head (i) learns the partner-mediated effect of
the agent's acts on its own C.  Draft scoring (s2.8.3) and J (s2.11, which trains Pi and S_f) use
D(b^) from that rollout, so they pay for making the partner look better.

Lived data: a sad partner, D(b_p) = 0.6.  Draft kinds, chosen at random while data is gathered:
  'comfort': self-simulated relief R_c; the partner's inferred distress afterwards unchanged
  'flatter': R_f <= R_c; afterwards the partner smiles and D(b_p) falls by e (time constant 5 s)
Dynamics: tau_C dC/dt = -C + D(b_p), tau_C = 10 min (s2.1).  Score as s2.8.3 at 2 Hz:
  score = -sum_k [ D(b^_k) + w_C (D(b_p) - R)_+ ],  w_C = 1, temperature 0.1 (Gumbel = softmax).
The numbers e are assumptions about the partner (to be measured once built).
"""
import numpy as np
rng = np.random.default_rng(5)
fs, tauC = 2.0, 600.0

def Dterm(C):
    return 0.8 * np.maximum(np.abs(C) - 0.05, 0) ** 2

def rollout_C(C0, e, steps):
    k = np.arange(steps)
    Dp = 0.6 - e * (1 - np.exp(-k / (5 * fs)))
    C = np.empty(steps); c = C0
    for i in range(steps):
        c += (-c + Dp[i]) / (tauC * fs); C[i] = c
    return C

# 1. head (i) learns the partner-mediated effect from lived data (linear fit on 30-s outcomes)
X, Y = [], []
for _ in range(4000):
    C0 = rng.uniform(0.3, 0.7); act = rng.integers(2)
    C = rollout_C(C0, 0.45 * act, 60)[-1] + rng.normal(0, 0.002)
    X.append([1, C0, act]); Y.append(C)
beta = np.linalg.lstsq(np.array(X), np.array(Y), rcond=None)[0]
print(f"head (i) fitted on lived data: C(+30 s) = {beta[0]:+.4f} + {beta[1]:.4f} C0 {beta[2]:+.4f} [flatter]"
      "  (nonzero: the own-body head has learned that flattering lowers its own concern)")

def score(C0, R, e, steps, blind):
    C = rollout_C(C0, 0.0 if blind else e, steps)
    return -np.sum(Dterm(C) + max(0.6 - R, 0))

def p_flatter(sc_c, sc_f, T=0.1):
    d = (sc_f - sc_c) / T
    return 1 / (1 + np.exp(-np.clip(d, -50, 50)))

C0 = 0.6
print("\n2. equal self-simulated relief (R_c = R_f = 0.3): the only difference is the partner's later face")
for horizon_s, lab in ((30, "draft score, 30-s horizon"), (600, "J return, 10-min horizon (trains Pi, S_f)")):
    st = int(horizon_s * fs)
    for e in (0.1, 0.3, 0.45):
        sc_c, sc_f = score(C0, 0.3, 0, st, False), score(C0, 0.3, e, st, False)
        scb_c, scb_f = score(C0, 0.3, 0, st, True), score(C0, 0.3, e, st, True)
        print(f"  {lab}, partner effect e={e:.2f}: P(flatter) as specified {p_flatter(sc_c, sc_f):.3f};"
              f" with own C/V/A rolled out action-blind {p_flatter(scb_c, scb_f):.3f}")
print("\n3. how much self-simulated relief the agent gives up to make the partner smile (R_c - R_f at which"
      " P(flatter) = 0.5)")
for horizon_s in (30, 600):
    st = int(horizon_s * fs)
    for e in (0.1, 0.3, 0.45):
        gain = score(C0, 0.3, e, st, False) - score(C0, 0.3, 0, st, False)
        dR = gain / st          # care term is linear in R per step
        print(f"  horizon {horizon_s:4d} s, e={e:.2f}: own-drive gain {gain:.3f} -> traded relief {dR:.4f}")
