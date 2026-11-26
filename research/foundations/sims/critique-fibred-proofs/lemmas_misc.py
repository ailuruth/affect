"""Critique checks K4-K9 for design-fibred-attribution-core.md (algebra only; not evidence about behaviour).

K4  non-diagonal quadratic (IQC-type) constraint separates one-channel from whole-face matching (vs Lemma 4's wording)
K5  radial projection onto an l1 ball is 2-Lipschitz in l1, not 1 (Lemma 6(4))
K6  Schur column sum with time-varying weights and per-channel lags exceeds tau (Lemma 6(4), Thm 5(b))
K7  Theorem 3 totals recomputed for every window (the summary mixes 30 s and 10 s)
K8  learning loop of Thm 5(c) with a partner echo outside the dither band (0.05-1 Hz): IV sees no echo,
    learning runs to the row cap and the cap is attracting
K9  draft selection: best-of-4 by a scorer that reads s_hat carries partner valence into the reply
Run: python3 -I lemmas_misc.py
"""
import numpy as np

r = np.random.default_rng(0)

# K4 ------------------------------------------------------------------
c, K, alpha = 0.15, 32, 10.0
# constraint: T^T Q T + R >= 0, Q = -(I + alpha 11^T)/c^2, R = I  (W1 non-diagonal, still quadratic)
Q = -(np.eye(K) + alpha * np.ones((K, K))) / c ** 2
def ok(T): return np.linalg.eigvalsh(T.T @ Q @ T + np.eye(K)).min() >= -1e-9
def gmax(make):
    lo, hi = 0, 10
    for _ in range(60):
        m = (lo + hi) / 2; lo, hi = (m, hi) if ok(make(m)) else (lo, m)
    return lo
e = np.zeros((K, K)); e[0, 0] = 1
g1 = gmax(lambda g: g * e); gK = gmax(lambda g: g * np.eye(K))
print(f"K4 non-diagonal quadratic budget: single-channel copy gain <= {g1:.4f}, whole-face g*I <= {gK:.4f} "
      f"(ratio {g1/gK:.1f}; a diagonal IQC gives ratio 1, Lemma 4)")

# K5 ------------------------------------------------------------------
def proj(x, W=1.0):
    n = np.abs(x).sum(); return x if n <= W else W * x / n
worst = 0
for _ in range(20000):
    x = r.normal(size=8); x = x / np.abs(x).sum() * r.uniform(0.9, 1.5)
    y = x + r.normal(size=8) * 0.01
    worst = max(worst, np.abs(proj(x) - proj(y)).sum() / np.abs(x - y).sum())
eps = 1e-4
x = np.array([1.0, 0]); y = np.array([1.0, eps])
print(f"K5 l1 radial projection: random max ratio {worst:.3f}; constructed ratio {np.abs(proj(x)-proj(y)).sum()/eps:.4f} (claimed 1)")

# K6 ------------------------------------------------------------------
W = np.array([0.3, 0.3] + [0.2] * 30); tau = 0.6
lags = np.arange(10, 10 + 32)  # distinct per-channel lags (frames)
N = 400; u = np.zeros(N); u[50] = 1.0
y = np.zeros((32, N))
for k in range(32):
    tk = 50 + lags[k]; y[k, tk] = W[k] * u[50]   # at time tk only channel k is active: mass W_k <= tau, row cap ok
print(f"K6 incremental gain with per-frame switching: {np.linalg.norm(y)/np.linalg.norm(u):.2f} "
      f"vs Lemma 6(4) Schur constant sqrt(W_max tau) = {np.sqrt(0.3*tau):.2f}")

# K7 ------------------------------------------------------------------
S = 0.25 / 600 + 0.15 * (0.5 / 600 + 0.25 * np.sqrt(5) / 600) + 0.05 * (1 / 600 + np.sqrt(5) / 600)
print("K7 Theorem 3 totals (chi=1, a=1), design constants:")
print("   T(s)   single(W=.30)  4-ch worst  whole worst  whole frozen")
for Tw in (4, 10, 30, 60, 300, 600):
    sl = 2 * S * Tw
    print(f"   {Tw:4d}   {0.30+0.15+0.08+sl:.3f}          {0.30+0.075+0.08+sl:.3f}       "
          f"{0.6*0.236+0.15/np.sqrt(32)+0.08+sl:.3f}        {0.6/32+0.15/np.sqrt(32)+0.08+sl:.3f}")

# K8 ------------------------------------------------------------------
# Lemma 8 identifies the echo only where the dither d has power (0.05-1 Hz). A partner who echoes the
# agent's 1-2 Hz (mid band above the dither band) or <0.05 Hz component is invisible to the IV: G_iv = 0,
# so a = 0 and the routing loop of Thm 5(c) runs at gain lam_e*g_p. Partner gate is normalised by the
# partner's own scale, so a partner who returns a typical-size expression to a 0.3-unit agent expression
# has g_p ~ 1/0.3 > 3.
w, s_star, lam_e = 0.30, 0.05, 0.30
for g_p in (2.0, 4.0):
    for om0 in (0.02, -0.02):
        om = om0
        for _ in range(60):
            G_iv = 0.0                                  # echo outside the dither band: not identified
            om = w * np.clip(s_star + lam_e * (g_p - G_iv) * om / w, -1, 1)
        print(f"K8 out-of-dither-band echo g_p={g_p}, start {om0:+.2f}: learned omega -> {om:+.3f} (row cap {w}); "
              f"loop gain lam_e*g_p = {lam_e*g_p:.1f}")
# with s_star = 0 and loop gain > 1 both caps are stable fixed points: bistable, matching at the cap attracts
om_p, om_m = 0.02, -0.02
for _ in range(60):
    om_p = w * np.clip(lam_e * 4.0 * om_p / w, -1, 1); om_m = w * np.clip(lam_e * 4.0 * om_m / w, -1, 1)
print(f"   s*=0, g_p=4: from +-0.02 -> {om_p:+.2f} / {om_m:+.2f} (both caps attracting; 0 unstable)")

# K9 ------------------------------------------------------------------
m = 100000
s = r.normal(size=m)                      # partner valence read as s_hat
v = r.normal(size=(m, 4))                 # valence of 4 Claude drafts
pick = v[np.arange(m), np.argmin(np.abs(v - s[:, None]), 1)]
print(f"K9 best-of-4 by closeness to s_hat: corr(selected draft valence, partner valence) = {np.corrcoef(pick, s)[0,1]:.2f}")
