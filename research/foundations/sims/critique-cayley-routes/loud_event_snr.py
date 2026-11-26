"""K5. What the slow mind (arousal load A, aversive load V, 𝓜) can see of a loud shout or of a held face.

Release as the design (30 Hz -> HP 3.2 s -> LP 1 Hz -> 2 Hz, + N(0, 7.1^2)). Audio energy is one
coordinate, normalised to [0,1]. A shout: +1 (full range) for d seconds.
Ideal detector (matched filter, known onset time): SNR = ||release mean||/sigma.
Also: a full-range held face+voice episode of any length (the design's own neighbouring pair).
"""
import numpy as np
from scipy.signal import lfilter
from scipy.stats import norm
fs, fr, sig = 30.0, 2.0, 7.1
a_hp = np.exp(-1 / (3.2 * fs)); a_lp = np.exp(-2 * np.pi / fs)
def rel(x):
    h = lfilter([1, -1], [1, -a_hp], x) * (1 + a_hp) / 2
    return lfilter([1 - a_lp], [1, -a_lp], h)[:: int(fs / fr)]
for d in (0.5, 1.0, 3.0):
    x = np.zeros(int(60 * fs)); x[int(5 * fs): int((5 + d) * fs)] = 1.0
    snr = np.linalg.norm(rel(x)) / sig
    print(f"shout of full-range energy for {d:.1f} s: matched-filter SNR {snr:.2f}; "
          f"detection at 5% false alarms: {norm.cdf(snr - 1.645):.2f}")
mu = np.sqrt(0.116)
print(f"held face+voice offset of norm 1, any duration: GDP mu {mu:.2f}; best balanced accuracy {norm.cdf(mu/2):.3f}; "
      f"power at 5% false alarms {norm.cdf(mu-1.645):.3f}")
# prediction-error magnitude that drives A: dominated by the release noise
e2 = sig**2 * 17
print(f"E||prediction error on X^s||^2 from noise alone = {e2:.0f} per release; a full-range edge adds at most "
      f"{np.max(rel(np.r_[np.zeros(60), np.ones(600)]))**2:.2f} on one coordinate ({100*np.max(rel(np.r_[np.zeros(60), np.ones(600)]))**2/e2:.2f}%)")
