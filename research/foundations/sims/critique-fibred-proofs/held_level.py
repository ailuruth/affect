"""Critique check K3: can the budgeted event port plus the slew display track the partner's held face?

Admissible parameters (all inside Theta of design-fibred-attribution-core.md):
- base: 5 wells on a line along e1 at -1,-0.5,0,0.5,1 (|mu|<=1, separation 0.5 = d_min); eps_b = 0.2.
- event proposals pi^ev are REN outputs; the REN sees the levels l and the displayed base b~.
  Learned proposal: "up" = transient * [l > level(b~)+0.25], "down" = transient * [l < level(b~)-0.25].
  Transients: any partner movement onset (Poisson, mean 15 s), so the 10-s high-pass re-arms.
- partner bucket: capacity 2, refill 1/60 s; refractory 2 s; jump +-0.5 e1 (|J| <= 0.6); weight 1 (a=0).
- display: b~ slew <= 1/600 per s; H_k = A_k tanh(P_k * 2 b~_1), A_k = 0.25, |P_k| <= 0.5 (1-Lipschitz).
- partner: whole-face held expression L_k(t) = P_k * l(t), l piecewise constant in {-1,-.5,0,.5,1},
  durations Exp(mean 8 min). Own variation d: band 0.05-1 Hz, sigma_0 = 0.15 on every channel.
Measured on 1-min means (mood scale): defect and pooled gain of agent face vs partner face, 16 channels.
Not evidence about behaviour. Run: python3 -I held_level.py [mean_hold_seconds]   (default 480; out.txt also has 1200)
"""
import numpy as np
import sys
MEAN_HOLD = float(sys.argv[1]) if len(sys.argv) > 1 else 480.0  # mean held duration (s)
from scipy.signal import butter, lfilter

fs = 1.0  # 1 Hz is enough for the base and display; d is generated at 30 Hz and averaged
r = np.random.default_rng(3)
H = 6 * 3600
levels = np.array([-1, -.5, 0, .5, 1.0])
P = r.choice([-1, 1], 16) * r.uniform(0.25, 0.5, 16)

# partner held level
l = np.zeros(H); t = 0
while t < H:
    dur = int(r.exponential(MEAN_HOLD)) + 30; l[t:t + dur] = r.choice(levels); t += dur
trans = r.uniform(size=H) < 1 / 15


def simulate(track=True, noise=0.0):
    b = 0.0; bt = 0.0; tok = 2.0; last = -10; ev = 0
    out = np.zeros(H)
    for s in range(H):
        tok = min(2.0, tok + 1 / 60)
        lev = bt  # base axis b_1 in [-1,1] corresponds to l
        if track and trans[s] and s - last >= 2 and tok >= 1:
            if l[s] > lev + 0.25: b += 0.5; tok -= 1; last = s; ev += 1
            elif l[s] < lev - 0.25: b -= 0.5; tok -= 1; last = s; ev += 1
        for _ in range(30):  # gradient flow at 30 Hz
            a = -200 * (b - levels) ** 2 / 2; p = np.exp(a - a.max()); p /= p.sum()
            b += -0.2 * np.sum(p * (b - levels)) / 30 + noise * np.sqrt(1 / 30) * r.normal()
        bt += np.clip(b - bt, -1 / 600, 1 / 600)
        out[s] = bt
    return out, ev


d30 = lfilter(*butter(2, [0.05, 1.0], btype="band", fs=30), r.normal(size=(H * 30, 16)), axis=0)
d30 *= 0.15 / d30.std(0)
d1 = d30.reshape(H, 30, 16).mean(1)  # per-second means

for track, noise in ((True, 0.0), (False, 0.0)):
    bt, ev = simulate(track, noise)
    y = 0.25 * np.tanh(np.outer(2 * bt, P)) + d1          # agent display + own variation
    L = np.outer(l, P)                                       # partner held face
    ym = y.reshape(-1, 60, 16).mean(1); Lm = L.reshape(-1, 60, 16).mean(1)
    best = None
    for lag in range(0, 11):
        a, b_ = ym[lag:], Lm[:len(Lm) - lag]
        rho = np.sum(a * b_) / np.sqrt(np.sum(a * a) * np.sum(b_ * b_))
        g = np.sum(a * b_) / np.sum(b_ * b_)
        if best is None or rho > best[1]: best = (lag, rho, g)
    lag, rho, g = best
    print(f"tracking={track}: partner events used {ev} (budget 2+T/60 = {2+H//60}); best lag {lag} min; "
          f"whole-face (16 ch) 1-min uncentred corr {rho:.3f}, defect {np.sqrt(max(0,1-rho**2)):.3f}, pooled gain {g:.3f}")
# design's own Theorem 4 floor and Theorem 3 pooled bound at a 10-min window
S = 0.25 / 600 + 0.15 * (0.5 / 600 + 0.25 * np.sqrt(5) / 600) + 0.05 * (1 / 600 + np.sqrt(5) / 600)
print(f"design Theorem 3 whole-face bound at T=600 s: {0.6*0.236+0.15/np.sqrt(32)+0.08+2*S*600:.2f} (vacuous); "
      f"Theorem 4 floor at gain 0.1: {0.15/np.sqrt(0.01+0.0225):.2f} (needs d, which 1-min means remove)")
