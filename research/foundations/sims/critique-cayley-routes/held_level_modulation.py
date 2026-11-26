"""K2. A held level that is not a pure additive offset costs privacy in proportion to its duration.

design-cayley-ledger.md §2.4 prices a held episode by its two edges (E_h = 5.85, eps_L(2) = 0.116)
'however long it lasts'. That holds for P' = P + Delta*v*1_W exactly. Two realistic departures:

(a) Multiplicative modulation by a KNOWN signal. While the partner speaks, articulation lowers the
    measured value of a held expression on some channels (lip-corner pull, cheek raise) by a
    fraction beta of the held level: x_t = l * (1 - beta * s_t), s_t = partner-speaking indicator.
    s_t is in Q (turn start/end times, noise-free). The mind can matched-filter X^s against h_s * s.
(b) Face-tracking dropouts (face turned away, hand over mouth, leaving the frame) or session starts
    with the feature reset to rest (0) rather than held: every dropout is a new pair of edges.

Release exactly as the design: 30 Hz -> high-pass tau 3.2 s -> low-pass 1 Hz -> 2 Hz, + N(0, 7.1^2).
We report the realised eps(2) of the full-range pair (l = 1 vs l = 0) and the matched-filter
correlation with l ~ U[0,1], against the design's 0.116 and rho_L = 0.25.
Not evidence about people; beta and dropout rates are assumptions to be measured.
"""
import numpy as np
from scipy.signal import lfilter
from scipy.stats import norm

rng = np.random.default_rng(3)
fs, fr, tau_h, sig = 30.0, 2.0, 3.2, 7.1
a_hp = np.exp(-1 / (tau_h * fs))
a_lp = np.exp(-2 * np.pi * 1.0 / fs)


def release_mean(x):
    hp = lfilter([1, -1], [1, -a_hp], x) * (1 + a_hp) / 2
    lp = lfilter([1 - a_lp], [1, -a_lp], hp)
    return lp[:: int(fs / fr)]


def speaking(T):
    s = np.zeros(T)
    t, on = 0, rng.random() < 0.5
    while t < T:
        d = int(rng.exponential(6.0) * fs) + int(fs)
        s[t:t + d] = 1.0 if on else 0.0
        on = not on
        t += d
    return s


def eps2(delta):           # Gaussian RDP at alpha = 2: ||delta||^2 / sigma^2
    return np.sum(delta ** 2) / sig ** 2


print("(a) known multiplicative modulation by partner speech (template from Q's turn times)")
for beta in (0.1, 0.3):
    for minutes in (10, 60, 180):
        T = int(minutes * 60 * fs)
        pad = int(30 * fs)
        s = speaking(T)
        x1 = np.r_[np.zeros(pad), 1.0 * (1 - beta * s), np.zeros(pad)]   # held l = 1 in window
        d = release_mean(x1)                                               # l = 0 gives 0
        e = eps2(d)
        mu = np.sqrt(e)          # GDP mu for a Gaussian mechanism: eps(alpha) = alpha mu^2 / 2
        acc = norm.cdf(mu / 2)
        # correlation of the matched-filter estimate with l ~ U[0,1]: sd(l)/sqrt(var l + 1/mu^2)
        corr = np.sqrt(1 / 12) / np.sqrt(1 / 12 + 1 / mu ** 2)
        print(f"  beta {beta:.1f}, hold {minutes:4d} min: eps(2) = {e:6.3f} (design 0.116), GDP mu = {mu:.2f}, "
              f"best balanced acc = {acc:.3f} (design <= 0.567), matched-filter corr(l) = {corr:.2f} (design <= 0.25)")

# Monte Carlo check of one row (beta 0.3, 60 min): matched filter with the known template
beta, minutes, trials = 0.3, 60, 60
ests, ls = [], []
for _ in range(trials):
    T = int(minutes * 60 * fs)
    s = speaking(T)
    l = rng.uniform()
    tmpl = release_mean(-beta * s)              # the part of the release that the mind can predict from Q
    edge_free = tmpl                            # (we drop the two edges; they add the design's 0.116)
    rel = release_mean(l * (1 - beta * s)) + sig * rng.normal(size=len(tmpl))
    est = rel @ edge_free / (edge_free @ edge_free)
    ests.append(est)
    ls.append(l)
print(f"  Monte Carlo (beta 0.3, 60 min, {trials} partners, l ~ U[0,1]): corr(l, estimate) = {np.corrcoef(ls, ests)[0,1]:.2f}")

print("(b) dropouts or session starts reset to rest: each one adds a pair of edges")
for k, label in [(1, "one session, no dropout"), (20, "1 h with a dropout every 3 min"),
                 (30, "30 sessions over a month, no dropouts"), (600, "30 sessions x 20 dropouts")]:
    e = 0.116 * k
    mu = np.sqrt(e)
    print(f"  {label:38s}: eps(2) = {e:7.2f}, GDP mu = {mu:5.2f}, best balanced acc {norm.cdf(mu/2):.3f}")
