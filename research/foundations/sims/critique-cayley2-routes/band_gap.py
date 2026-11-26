"""E1. Band coverage |H_i|^2 + |L|^2 of the design's 4-s high-pass and 60-s low-pass (30 Hz, the
design's own discrete filters).  The design (s8.1) says this is ~0.08 at 30 s."""
import numpy as np
fs = 30.0
def lp(tau, w):
    a = 1 - np.exp(-1 / (tau * fs)); z = np.exp(1j * w)
    return a / (1 - (1 - a) / z)
for per in (10, 20, 30, 60, 90, 120, 300):
    w = 2 * np.pi / per / fs
    H = 1 - lp(4.0, w); L = lp(60.0, w)
    print(f"period {per:4d} s: |H_i|^2 = {abs(H)**2:.3f}  |L|^2 = {abs(L)**2:.3f}  sum = {abs(H)**2+abs(L)**2:.3f}"
          f"  fast-path ceiling gf|H_i||H_o| = {0.45*abs(H)**2:.3f}")
w = np.logspace(-6, np.log10(np.pi), 20000)
s = abs(1 - lp(4.0, w))**2 + abs(lp(60.0, w))**2
i = np.argmin(s)
print(f"minimum of the sum: {s[i]:.3f} at period {2*np.pi/w[i]/fs:.1f} s")
