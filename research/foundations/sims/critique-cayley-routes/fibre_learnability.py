"""K3. The fibre cannot learn context- or relationship-dependent signs from its own training signal.

design-cayley-ledger.md §2.9: the fibre (REN, attention, phi_k) is trained nightly to predict the
agent's own display 1-2 s ahead, from X^s (upsampled, noise sd 7.1 per release) and context c.
Replay never stores u. At run time the fibre is applied to the clean u through F and R.

We give the learner the most favourable case: the own display really does follow the partner's
smile transients with a context-set sign (+0.5 in 'friendly', -0.5 in 'opposed'), lag 1 s,
and the learner is the best linear causal filter (8 taps = 4 s at 2 Hz) per context, fitted by
least squares on 30 nights x 8 h of data. We then apply the learned filter to the CLEAN partner
stream (what the fibre sees at run time) and report its gain, against the target +-0.5.
Then the innate pull: the equilibrium of phi under pull lambda_phi = 0.5 and the mean gradient.
Not evidence about people.
"""
import numpy as np
from scipy.signal import lfilter

rng = np.random.default_rng(11)
fr, tau_h, sig = 2.0, 3.2, 7.1
a2 = np.exp(-1 / (tau_h * fr))


def hp(x):
    return lfilter([1, -1], [1, -a2], x) * (1 + a2) / 2


hours = 30 * 8
T = int(hours * 3600 * fr)
# partner smile transients: 2-4 s bumps every ~15 s, amplitude ~0.3 (normalised units)
p = np.zeros(T)
idx = np.cumsum(rng.exponential(15 * fr, size=int(T / (15 * fr)) + 10)).astype(int)
idx = idx[idx < T - 10]
for i in idx:
    p[i:i + 6] += 0.3 * rng.uniform(0.5, 1.0)
pc = hp(p)
ctx = (np.floor(np.arange(T) / (600 * fr)) % 2).astype(int)        # context flips every 10 min
sign = np.where(ctx == 0, 0.5, -0.5)
lag = 2
target = sign * np.roll(pc, lag) + 0.05 * rng.normal(size=T)        # own display 1 s later
xs = pc + sig * rng.normal(size=T)                                  # released stream
ntap = 8
def design(x):
    return np.stack([np.roll(x, k) for k in range(ntap)], 1)
Xn, Xc = design(xs), design(pc)
for c, true in [(0, 0.5), (1, -0.5)]:
    m = ctx == c
    w_noisy = np.linalg.lstsq(Xn[m], target[m], rcond=None)[0]
    w_clean = np.linalg.lstsq(Xc[m], target[m], rcond=None)[0]
    # run-time gain on the clean stream: regression of learned output on the true lagged signal
    out_n = Xc[m] @ w_noisy
    ref = np.roll(pc, lag)[m]
    g_n = out_n @ ref / (ref @ ref)
    g_c = (Xc[m] @ w_clean) @ ref / (ref @ ref)
    print(f"context {'friendly' if c == 0 else 'opposed '} target gain {true:+.2f}: learned from X^s -> run-time gain {g_n:+.4f}; "
          f"learned from clean u (forbidden by the design) -> {g_c:+.3f}")
rel = pc.var() / (pc.var() + sig ** 2)
print(f"per-sample reliability var(signal)/(var+sigma^2) = {rel:.2e}; attenuation does not shrink with more data")
# innate pull: phi* - phi0 = -E[grad]/lambda. The mean gradient on a gain logit is ~ (target gain - current) x
# reliability x var(signal), i.e. tiny; the pull dominates.
g_mean = 0.5 * rel
print(f"phi equilibrium shift under pull 0.5: |dphi| ~ {g_mean/0.5:.1e} (ball radius 2): phi stays at phi0, gamma_k ~ 0.37")
