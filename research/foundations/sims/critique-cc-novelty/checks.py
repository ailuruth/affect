"""Independent critic's checks for design-commutator-coupling.md (novelty and agent critique).

Mathematics on constructed signals only; NOT evidence about people (brief: self-built worlds are never evidence).
numpy + scipy; runs in a few seconds.  Run: python3 -I checks.py > out.txt

K1  The expected node commutator at scale j depends only on the quadrature (imaginary) cross-spectrum:
    E[c_j] = -∫ |G_h(f)|^2 sin(2π f h) Im S_ax(f) df, h = 2^(j-1) frames, G_h(f) = e^{i2πfh} - 1.
    So the mean ρ array is a Haar-band imaginary coherency / quadrature spectrum (Nolte 2004; Stam 2007 PLI family).
K2  Sign confound (Bennett et al. 2022): 'he follows me, same direction' and 'I follow him, opposite direction'
    give the same sign of ρ. The sign is (lead direction) x (sign of association), not who led.
K3  Phase aliasing: a lag of 3/4 period reads as the opposite lead direction to a 1/4-period lag.
K4  Node completions: which scales ever complete in recorded dyad sessions and in a first year of living.
K5  One follower (0.6 s lag) gives opposite signs at adjacent scales.
K6  With the own channel drifting (a ramp), rho becomes a normalised readout of the partner's own Haar curvature.
"""
import numpy as np
from scipy.signal import lfilter, csd

rng = np.random.default_rng(3)
FS = 30.0


def commutators(a, x, j):
    h = 2 ** (j - 1)
    n = (len(a) - 1) // (2 * h)
    idx = np.arange(0, 2 * n * h + 1, h)
    da, dx = np.diff(a[idx]), np.diff(x[idx])
    aL, aR, xL, xR = da[0::2], da[1::2], dx[0::2], dx[1::2]
    c = 0.5 * (aL * xR - xL * aR)
    D = 1e-9 + 0.5 * (np.abs(aL) + np.abs(aR)) * (np.abs(xL) + np.abs(xR))
    return c, c / D


def smooth_noise(n, tau_s):
    a = np.exp(-1.0 / (tau_s * FS))
    return lfilter([1 - a], [1, -a], rng.standard_normal(n))


def lag(sig, frames):
    return np.concatenate([np.zeros(frames), sig[:-frames]]) if frames > 0 else sig


print("K1: E[c_j] from data vs from the quadrature spectrum alone")
N = 2 ** 21
src = smooth_noise(N + 200, 0.3) + 0.5 * smooth_noise(N + 200, 2.0)
a = src[200:]
x = 0.7 * lag(src, 18)[200:] + 0.3 * smooth_noise(N, 0.5)   # x follows a at 0.6 s, partly
f, S = csd(a, x, fs=1.0, nperseg=2 ** 14)    # S_ax with R_ax(tau)=E[a(t) x(t+tau)] (scipy: conj(A) X)
# one-sided -> two-sided integral of the odd part: 2 * sum over f>0
for j in (2, 4, 6, 8, 10):
    h = 2 ** (j - 1)
    c, _ = commutators(a, x, j)
    G2 = np.abs(np.exp(2j * np.pi * f * h) - 1) ** 2
    df = f[1] - f[0]
    # S from csd is one-sided (density doubled); two-sided integral of odd*odd = even integrand -> use one-sided as is
    pred_q = -np.sum(G2 * np.sin(2 * np.pi * f * h) * np.imag(S)) * df / 2 * 2
    pred_c = -np.sum(G2 * np.sin(2 * np.pi * f * h) * np.real(S)) * df   # real (co-)spectrum alone, for contrast
    print(f"  j={j:2d} ({h*2/FS:6.2f} s node): data E[c]={c.mean():+.5f}  quad-only prediction={pred_q:+.5f}"
          f"  (co-spectrum alone would give {pred_c:+.5f}; n={c.size})")

print("\nK2: sign confound, same channel, 0.6 s lag, mean rho at j=5 (1.07 s node)")
base = smooth_noise(2 ** 20, 0.3)
cases = {
    "partner follows agent, +gain": (base, 0.8 * lag(base, 18)),
    "agent follows partner, +gain": (0.8 * lag(base, 18), base),
    "partner follows agent, -gain (countering)": (base, -0.8 * lag(base, 18)),
    "agent follows partner, -gain (countering)": (-0.8 * lag(base, 18), base),
}
for k, (aa, xx) in cases.items():
    _, r = commutators(aa + 0.02 * rng.standard_normal(aa.size), xx + 0.02 * rng.standard_normal(aa.size), 5)
    print(f"  {k:45s} mean rho = {r.mean():+.3f}")

print("\nK3: phase aliasing on a rhythmic channel (period 2 s), partner follows agent at lag L, mean rho at the matched scale")
t = np.arange(2 ** 18) / FS
for frac in (0.25, 0.5, 0.75):
    L = int(frac * 2.0 * FS)
    aa = np.sin(2 * np.pi * t / 2.0)
    xx = lag(aa, L)
    _, r = commutators(aa, xx, 5)  # node 32 frames ~ 1.07 s ~ half period
    print(f"  lag = {frac:.2f} period: mean rho = {r.mean():+.3f}")

print("\nK4: node completions (contact time, 30 Hz)")
for minutes in (10, 20, 60):
    frames = minutes * 60 * FS
    jmax = int(np.floor(np.log2(frames)))
    print(f"  one {minutes}-min recorded session: deepest scale completing at least once = {jmax} ({2**jmax/FS/60:.1f} min)")
for h_per_day in (1.0, 2.0):
    frames_year = 365 * h_per_day * 3600 * FS
    row = []
    for j in (16, 18, 20, 22, 24):
        row.append(f"j={j}: {frames_year / 2**j:6.1f}")
    print(f"  first year at {h_per_day:.0f} h/day, completed nodes per scale: " + "; ".join(row))

print("\nK5: one relationship, many scales: partner follows agent at +gain, lag 0.6 s; mean rho by scale")
for tau in (0.1, 0.3, 1.0):
    base = smooth_noise(2 ** 20, tau)
    aa = base + 0.02 * rng.standard_normal(base.size)
    xx = 0.8 * lag(base, 18) + 0.02 * rng.standard_normal(base.size)
    row = []
    for j in range(1, 10):
        _, r = commutators(aa, xx, j)
        row.append(f"{2**j/FS:5.2f}s:{r.mean():+.2f}")
    print(f"  own motion smoothed tau={tau:.1f} s | " + " ".join(row))

print("\nK6: own channel drifting slowly (a mood display), partner moving on his own; is rho a lead-lag or a partner-only readout?")
n = 2 ** 20
xp = np.zeros(n)
on = rng.random(n) < 4 / 60 / FS                    # smile bursts ~4/min
xp = lfilter([1.0], [1, -0.97], on * rng.uniform(0.25, 0.5, n))
xp = np.clip(xp, 0, 1) + 0.003 * rng.standard_normal(n)  # tracker jitter
for drift_per_min in (0.002, 0.02, 0.2):
    own = (drift_per_min / 60 / FS) * np.arange(n) + 0.0005 * rng.standard_normal(n)  # tiny renderer noise
    for j in (6, 9, 12):
        h = 2 ** (j - 1)
        nn = (n - 1) // (2 * h)
        idx = np.arange(0, 2 * nn * h + 1, h)
        dx = np.diff(xp[idx]); xL, xR = dx[0::2], dx[1::2]
        eps = 0.0005 * 0.003 * 2 ** j
        da = np.diff(own[idx]); aL, aR = da[0::2], da[1::2]
        c = 0.5 * (aL * xR - xL * aR)
        rho = c / (eps + 0.5 * (np.abs(aL) + np.abs(aR)) * (np.abs(xL) + np.abs(xR)))
        partner_only = (xR - xL) / (2 * (np.abs(xL) + np.abs(xR)) + 1e-12)
        r = np.corrcoef(rho, partner_only)[0, 1]
        print(f"  own drift {drift_per_min:5.3f}/min, node {2**j/FS:7.1f} s: corr(rho, his own Haar curvature) = {r:+.3f}, "
              f"mean|rho| = {np.abs(rho).mean():.3f}")
