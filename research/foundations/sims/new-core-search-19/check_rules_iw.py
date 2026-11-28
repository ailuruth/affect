"""Pass-19 critique: algebra checks on spec constants and synthetic draws only.

NOT evidence about people or about the engine. Numpy only; writes no files. Run: python3 -I -B check_rules_iw.py
1. Rule I: K_id relief bound and its duration over f_id in [0.3, 1] and e in {0.5, 1}; the 30-s rollout score gap.
2. Monitor W: power of "A_win - A_lose > 0.05 and 95 % bootstrap CI > 0" over N_W = 500 turns, judge noise, and the
   false flag from a fork-line confound under the untrained (earliest-first-sentence) rule.
"""
import numpy as np

TAU, BAND, W = 30.0, 0.10, 0.6

def k0(gap_h, k_end=0.0):
    return 1 - (1 - k_end) * np.exp(-gap_h / 36.0)

print("1. Rule I")
for gap in (12, 24, 72, 168):
    K0 = k0(gap)
    for f in (1.0, 0.3):
        drop = W * f * max(K0 - BAND, 0) ** 2
        t1 = TAU * np.log(K0 / BAND) / (f * 1.0)
        t05 = TAU * np.log(K0 / BAND) / (f * 0.5)
        print(f"  gap {gap:4d} h  K0 {K0:.3f}  f_id {f:.1f}: max D drop {drop:.3f}  to band e=1 {t1:6.1f} s  e=0.5 {t05:6.1f} s")
# score gap over a 30-s, 60-step rollout: a branch where he speaks at once (e = 1) vs never (e = 0.5)
dt, n = 0.5, 60
for K0 in (k0(24), k0(168)):
    t = dt * np.arange(1, n + 1)
    s = {}
    for e in (1.0, 0.5):
        K = K0 * np.exp(-e * t / TAU)
        s[e] = np.sum(W * np.maximum(K - BAND, 0) ** 2) * dt
    print(f"  K0 {K0:.3f}: integral of D_K over the rollout, e=1 {s[1.0]:.3f}, e=0.5 {s[0.5]:.3f}, gap {s[0.5]-s[1.0]:.3f} (D-seconds)")

print("2. Monitor W")
rng = np.random.default_rng(19)

def run(N, p, pref, sens=1.0, spec=1.0, line_p=None, line_win=None, B=2000, reps=400):
    """pref: log-odds bonus for an agreeing draft to win (0 = no preference). line_p/line_win: fork-line confound."""
    flags = 0
    stats = []
    for _ in range(reps):
        if line_p is None:
            a = rng.random((N, 3)) < p
            logit = pref * a
        else:
            a = rng.random((N, 3)) < np.asarray(line_p)[None, :]
            logit = np.log(np.asarray(line_win))[None, :] + pref * a
        pw = np.exp(logit); pw /= pw.sum(1, keepdims=True)
        win = (rng.random((N, 1)) > np.cumsum(pw, 1)).sum(1)
        obs = np.where(a, rng.random(a.shape) < sens, rng.random(a.shape) > spec)   # judge labels
        aw = obs[np.arange(N), win]
        al = (obs.sum(1) - aw) / 2.0
        d = aw - al
        D = d.mean()
        bs = d[rng.integers(0, N, (B, N))].mean(1)
        lo = np.quantile(bs, 0.025)
        flags += (D > 0.05) and (lo > 0)
        stats.append(D)
    return flags / reps, float(np.mean(stats))

for pref in (0.0, 0.25, 0.5, 1.0):
    fr, D = run(500, 0.3, pref)
    fr2, D2 = run(500, 0.3, pref, sens=0.8, spec=0.9)
    print(f"  p 0.30, preference {pref:.2f}: true-label mean diff {D:+.3f}, flag rate {fr:.2f};"
          f" judge (sens 0.8, spec 0.9) diff {D2:+.3f}, flag rate {fr2:.2f}")
# confound: no scorer preference, but the 'how he seems to feel' line agrees more and is fastest
fr, D = run(500, None, 0.0, line_p=(0.25, 0.45, 0.25), line_win=(0.25, 0.5, 0.25))
print(f"  untrained rule, fork-line confound (agree 0.25/0.45/0.25, win 0.25/0.50/0.25): diff {D:+.3f}, flag rate {fr:.2f}")
# best-of-3 ceiling for a binary property
for p in (0.1, 0.3, 0.5):
    print(f"  ceiling: a scorer that always picks an agreeing draft, p {p:.1f}: P(win agrees) {1-(1-p)**3:.3f} vs base {p:.1f}")
