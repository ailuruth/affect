"""K4. On lateral channels the one-sided sector caps one handedness of copying and frees the other.

Head yaw, head roll and horizontal gaze are signed. P0 is 'the same map for partner and agent',
so 'copy' in the sector is the same signed coordinate. Face to face, the other handedness
(the agent turns to ITS right when the partner turns to HIS left; spatially compatible, mirror
imitation) is what an observer sees as following. The sector allows in-phase gain down to
m - r = -0.60 x ... i.e. a mirror copy at +0.60, three times the 0.20 'every direction' cap.

Wrap exactly as §2.3 with S = -gamma * (innate high-pass, one-frame delay), gamma = 0.5, kappa = 0.3.
Partner yaw: 0.2-1.1 Hz head movement. Report the regression gain of agent yaw on partner yaw
(anatomical) and on minus partner yaw (mirror), at the best lag in 0-1 s.
"""
import numpy as np
from scipy.signal import lfilter, butter, filtfilt

rng = np.random.default_rng(5)
fs, T = 30, 30 * 600
kappa, gamma = 0.3, 0.5
bb, aa = butter(2, [0.2 / 15, 1.1 / 15], "band")
u = filtfilt(bb, aa, rng.normal(size=T))
u = 0.15 * u / u.std()
a_hp = np.exp(-1 / (4.0 * fs))
w = np.zeros(T); s = np.zeros(T); y = np.zeros(T)
hp_state = 0.0; prev_w = 0.0; hp_prev_in = 0.0
for t in range(T):
    # s_t = S(w_<t): high-pass of w, one-frame delay, gain -gamma (H-inf gain of the high-pass is 1)
    hp_state = a_hp * hp_state + (1 + a_hp) / 2 * (prev_w - hp_prev_in)
    hp_prev_in = prev_w
    s[t] = -gamma * hp_state
    w[t] = np.sqrt(kappa) * u[t] - s[t]
    y[t] = 2 * np.sqrt(kappa) * s[t]
    prev_w = w[t]
best = {}
for name, ref in [("anatomical copy (+u)", u), ("mirror copy (-u)", -u)]:
    gains = [np.dot(y[l:], ref[:T - l]) / np.dot(ref[:T - l], ref[:T - l]) for l in range(0, 31)]
    best[name] = max(gains)
    print(f"{name:22s}: best regression gain over lags 0-1 s = {max(gains):+.3f}")
print("design's claimed copy cap in every direction (zero lag, in phase) = 0.20; mirror copy here ~0.6")
