"""K6. Is G9's 'fast band below surrogate' (C1) systematic or one draw? Re-run G9's own code over 40 seeds."""
import numpy as np
from scipy.signal import lfilter, coherence, butter, filtfilt

fs, T = 30, 30 * 600
def band(x, lo, hi):
    bb, aa = butter(2, [lo / (fs / 2), hi / (fs / 2)], "band")
    return filtfilt(bb, aa, x)
def run(seed, gate):
    rng = np.random.default_rng(seed)
    def partner():
        burst = (lfilter([0.02], [1, -0.98], rng.normal(size=T)) > 0.05).astype(float)
        return band(rng.normal(size=T), 2.6, 6.5) * burst + band(rng.normal(size=T), 0.2, 1.1)
    def agent(pv):
        env = np.abs(band(pv, 2.6, 6.5)); env = lfilter([0.05], [1, -0.95], env)
        g = 1 / (1 + gate * env / (env.mean() + 1e-9)) if gate else 1.0
        own = band(rng.normal(size=T), 2.6, 6.5) * g
        slow = 0.2 * np.roll(band(pv, 0.2, 1.1), 15) + band(rng.normal(size=T), 0.2, 1.1)
        return own + slow
    def coh(x, y):
        f, C = coherence(x, y, fs=fs, nperseg=256)
        return C[(f >= 2.6) & (f <= 6.5)].mean()
    p1, p2 = partner(), partner()
    a1 = agent(p1)
    return coh(a1, p1), coh(a1, p2)
for gate in (4.0, 0.0):
    r = np.array([run(s, gate) for s in range(40)])
    d = r[:, 0] - r[:, 1]
    print(f"gate {gate}: fast-band coherence real {r[:,0].mean():.4f} vs surrogate {r[:,1].mean():.4f}; "
          f"real < surrogate in {np.mean(d<0)*100:.0f}% of seeds; mean diff {d.mean():+.4f} +- {d.std()/np.sqrt(40):.4f}")
