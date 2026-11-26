"""Critique check K2: is the gate Gamma invariant to the sign of the partner's PHYSICAL fast band?

Theorem 2 needs Gamma(sigma.p) = Gamma(p), where sigma flips c^f = F_f p with r = p - c^f fixed.
For causal complementary filters F_f is not idempotent (F_f^2 != F_f), so the percept r + sigma c^f
does not decompose back into (r, sigma c^f). Here: flip a 3 Hz head-pitch component (inside C1's
2.6-6.5 Hz band) of a partner signal and compare the gate outputs; then run a router-style copy of the
mid band (W=0.2, lag 0.5 s) with no other agent motion at 3 Hz and measure coherence at 3 Hz.
First-order bank (satisfies ||F_beta||_inf <= 1) and 2nd-order Butterworth bank.
Not evidence about behaviour. Run: python3 -I filter_leak.py
"""
import numpy as np
from scipy.signal import butter, lfilter, coherence

fs, T = 30.0, 30 * 1200
r = np.random.default_rng(0)
t = np.arange(T) / fs
slow = lfilter(*butter(1, 0.3, fs=fs), r.normal(size=T)) * 3
env = 0.5 + np.abs(lfilter(*butter(1, 0.2, fs=fs), r.normal(size=T))) * 2
fast = env * np.sin(2 * np.pi * 3.0 * t + 0.3 * np.cumsum(r.normal(size=T)) / np.sqrt(fs))
d = lfilter(*butter(2, [0.05, 1.0], btype="band", fs=fs), r.normal(size=T))
d *= 0.15 / d.std()


def bank(order):
    lo04 = butter(order, 0.4, fs=fs); lo2 = butter(order, 2.0, fs=fs)
    Fs = lambda x: lfilter(*lo04, x)
    Fm = lambda x: lfilter(*lo2, x) - lfilter(*lo04, x)
    Ff = lambda x: x - lfilter(*lo2, x)
    return Fs, Fm, Ff


for order in (1, 2):
    Fs, Fm, Ff = bank(order)
    out = {}
    for sgn in (+1, -1):
        p = slow + sgn * fast
        cf = Ff(p); rr = p - cf
        out[sgn] = dict(um=Fm(rr), eps=lfilter(*butter(1, 1.0, fs=fs), np.abs(cf)), cf=cf)
    dum = out[1]["um"] - out[-1]["um"]
    deps = out[1]["eps"] - out[-1]["eps"]
    leak = np.std(dum) / 2 / np.std(fast)
    # abstract action: F_f(r + sigma c^f) vs sigma c^f
    p = slow + fast; cf = Ff(p); rr = p - cf
    idem = np.std(Ff(rr - cf) + cf) / np.std(cf)
    # router copy of the mid band at W=0.2, lag 0.5 s, output through F_m, plus own variation d
    lag = 15
    y = np.zeros(T); y[lag:] = 0.2 * out[1]["um"][:-lag]
    y = Fm(y) + d
    f, C = coherence(slow + fast, y, fs=fs, nperseg=512)
    band = (f >= 2.6) & (f <= 3.4)
    # surrogate: same agent output against a different partner realisation
    p2 = lfilter(*butter(1, 0.3, fs=fs), r.normal(size=T)) * 3 + env[::-1] * np.sin(2 * np.pi * 3.0 * t + 1.0)
    _, C2 = coherence(p2, y, fs=fs, nperseg=512)
    print(f"order {order}: sign flip of 3 Hz band changes u^m by {leak:.3f} x its amplitude "
          f"(eps changes by {np.std(deps)/np.mean(out[1]['eps']):.3f} rel.); "
          f"||F_f(r - c^f) + c^f||/||c^f|| = {idem:.3f} (0 if F_f idempotent); "
          f"coherence 2.6-3.4 Hz with router-only agent: {C[band].mean():.2f} (surrogate {C2[band].mean():.2f})")
