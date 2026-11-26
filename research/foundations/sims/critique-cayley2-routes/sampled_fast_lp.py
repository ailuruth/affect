"""K2. Phrase-onset sampling of the *bounded* fast path.  The TTS takes F0 level, F0 range, energy,
rate and pause from y at the agent's phrase onset and holds them for the phrase (s2.8.5).  The wrap
bounds the fast path in l2 (energy), not pointwise.  Partner voice channels are zero-order held per
phrase, so the partner's input is a step at each of its phrase onsets.

LP: over every LTI closed loop the design allows on one kappa = 0.3 channel with the slow block off,
i.e. T_n(w) = S/(1+S) with |S(w)| <= gf |H_i(w)| |H_o(w)| (fast block between the two 4-s high-passes;
Apollonius disc, inner 24-gon), maximise the worst sampled value 2k * step_response(t*) over
t* in a window after the partner's last step.  10 Hz, FIR 30 s, strictly causal (h[0] = 0).
"""
import numpy as np
from scipy.optimize import linprog
fs, N, K, GF = 10.0, 300, 0.30, 0.45
M, P = 500, 24
w = np.linspace(0, np.pi, M)
a = 1 - np.exp(-1 / (4.0 * fs)); z = np.exp(1j * w)
HP = 1 - a / (1 - (1 - a) / z)
rho = GF * np.abs(HP) ** 2
c = -rho ** 2 / (1 - rho ** 2); R = rho / (1 - rho ** 2)
n = np.arange(N)
E = np.exp(-1j * np.outer(w, n))          # H(w) = E h
def solve(t1, t2):
    rows, rhs = [], []
    for j in range(P):
        th = 2 * np.pi * j / P
        # Re((H - c) e^{-i th}) <= R cos(pi/P)
        rows.append(np.real(E * np.exp(-1j * th))); rhs.append(R * np.cos(np.pi / P) + c * np.cos(th))
    Aub = np.vstack(rows); bub = np.concatenate(rhs)
    # epigraph: maximise zeta s.t. zeta <= step(t) for t in window
    win = np.arange(int(t1 * fs), int(t2 * fs) + 1)
    step = np.array([(n <= k).astype(float) for k in win])
    A2 = np.hstack([-step, np.ones((len(win), 1))])
    Aub = np.hstack([Aub, np.zeros((Aub.shape[0], 1))])
    Aub = np.vstack([Aub, A2]); bub = np.concatenate([bub, np.zeros(len(win))])
    bounds = [(0, 0)] + [(None, None)] * (N - 1) + [(None, None)]
    cost = np.zeros(N + 1); cost[-1] = -1
    r = linprog(cost, A_ub=Aub, b_ub=bub, bounds=bounds, method="highs")
    h = r.x[:N]
    return 2 * K * r.x[-1], h
for (t1, t2) in [(2.0, 2.0), (1.0, 3.0), (2.0, 5.0)]:
    v, h = solve(t1, t2)
    Hh = E @ h
    print(f"sample window {t1:.0f}-{t2:.0f} s after the partner's last phrase step: worst sampled y / step = {v:+.3f}"
          f"   (check: max |S| / allowed = {np.max(np.abs(Hh/(1-Hh)) / np.maximum(rho,1e-9)):.3f}; "
          f"max Re y-gain {2*K*np.max(Hh.real):+.3f})")
print("design claims on this channel: zero-lag in-phase <= 0.198, fast lag broadband <= 0.339")
