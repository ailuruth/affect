"""Algebra checks for design-partner-regulator.md revision 3 (hand-set instances; NOT evidence about behaviour or people).
Run from research/foundations/sims:  uv run python -I partner-regulator-r3/check.py
"""
import numpy as np
from scipy.optimize import fsolve
rng = np.random.default_rng(0)
def hdr(s): print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)
def skew(n, r):
    M = r.normal(size=(n, n)); return M - M.T

# ---------------------------------------------------------------------------
hdr("S1  L4: linear own-model observer with gradient gain L = l Q^-1 E'^T; incremental gain y -> h_hat")
# claim: L2 / H-inf gain <= 0.5*sqrt(l/r_min); Linf gain <= 0.5*sqrt(q_hi*l/(q_lo*r_min)); independent of E', J, R_l
worst2, worstinf = 0.0, 0.0
for s in range(300):
    r = np.random.default_rng(s); n, m = 8, 5
    q = r.uniform(0.5, 2.0, n); Q = np.diag(q); Qi = np.diag(1 / q)
    J = skew(n, r); J *= r.uniform(0, 3) / np.linalg.norm(J, 2)
    rmin = 0.5; B = r.normal(size=(n, n)) * r.uniform(0, 1); R = rmin * np.eye(n) + B @ B.T
    Ep = r.normal(size=(m, n)) * r.uniform(0.1, 10); l = r.uniform(0.1, 4.0)
    A = (J - R) @ Q - l * Qi @ Ep.T @ Ep; L = l * Qi @ Ep.T
    g = max(np.linalg.norm(Q @ np.linalg.solve(1j * w * np.eye(n) - A, L), 2) for w in np.r_[0, np.logspace(-3, 3, 60)])
    worst2 = max(worst2, g / (0.5 * np.sqrt(l / rmin)))
print(f"max over 300 random instances of (H-inf gain y->h_hat) / (0.5*sqrt(l/r_min)) = {worst2:.3f}  (must be <= 1)")

# ---------------------------------------------------------------------------
hdr("S2  Critique K1 instance under the revision-3 innate caps: loop same-group DC gain vs the innate ceiling")
# K1: n' = -(rN+beta(y)) n - w m + u ; m' = w n - rM m ; e = Ep m ; beta = -bm*tanh(k y).
# Copy entry at DC = Ep*(w/rM)*h0/rN_eff * |dbeta/dy|.  Rev 3 caps: |dbeta/dy| <= beta'_max (L4 x L_beta x p_bar),
# h0 <= h_bar (C_b-free T0), Ep*w/rM <= kappa_NE.  Ceiling: kappa_NE * h_bar * beta'_max * Dbar / rho.
rN, rM, w, Ep = 0.5, 20.0, 3.0, 10.0
kNE = Ep * w / rM                       # = 1.5 in K1; design cap below
for (kNE_cap, bprime, hbar) in [(1.5, 0.9, 1.05), (0.4, 0.2, 1.0), (0.4, 0.1, 1.0)]:
    rho = rN                              # dissipation floor on N (A3 keeps r_N - b_minus*Dbar > 0)
    ceiling = kNE_cap * hbar * bprime / rho
    # worst case inside the caps: rN_eff as small as allowed = rN + w^2/rM (no contagion at operating point)
    rNeff = rN + w * w / rM
    actual = kNE_cap * hbar * bprime / rNeff
    print(f"kappa_NE={kNE_cap:4.2f} beta'_max={bprime:4.2f} h_bar={hbar:4.2f}: actual DC copy entry={actual:.3f}  innate ceiling={ceiling:.3f}")
print("  -> with K1's own (uncapped) numbers the entry is 1.49 and the formula's ceiling 2.8 says nothing;\n"
      "     under the rev-3 innate design caps (0.4, 0.1, 1) the entry is 0.04 and the ceiling 0.08.")

# ---------------------------------------------------------------------------
hdr("S3  L5: a route through a scalar (rank one) has copy fraction <= max_g a_g")
groups = [3, 3, 3, 3, 3, 2]; idx = np.cumsum([0] + groups)
def copy_frac(G):
    num = sum(np.linalg.norm(G[idx[g]:idx[g+1], idx[g]:idx[g+1]]) ** 2 for g in range(len(groups)))
    return num / np.linalg.norm(G) ** 2
S = np.r_[0.6, 0.6, 0.6, -0.5, -0.5, -0.5, 0.3, 0.3, 0.3, 0, 0, 0, 0, 0, 0, 0.4, 0.4]   # regard synergy (illustrative)
a = np.array([np.sum(S[idx[g]:idx[g+1]] ** 2) for g in range(len(groups))]) / np.sum(S ** 2)
worst = max(copy_frac(np.outer(S, rng.normal(size=17))) for _ in range(20000))
best_v = max(copy_frac(np.outer(S, S * (np.arange(17) < 3))) for _ in range(1))
print(f"max_g a_g = {a.max():.3f}; max copy fraction over 20000 random rank-one routes S v^T = {worst:.3f}; "
      f"attained by v on the largest group: {best_v:.3f}")

# ---------------------------------------------------------------------------
hdr("S4  T8: the critique's K6 bistability vs the innate small-gain cap (SG)")
r = np.random.default_rng(31)
rN_, rM_ = r.uniform(0.05, 1), r.uniform(1, 20)
av = r.normal(size=2); av /= np.linalg.norm(av); D = np.outer(av, av)
j = r.normal(0, 1.5, 2); k_full = r.normal(0, 3); _ = r.uniform(-1, 1); _ = r.normal(0, 2, 2)
u = np.r_[r.normal(0, 2, 2), 0.0]
rho = min(rN_, rM_); hbar = np.linalg.norm(u) / rho
k_SG = rho ** 2 / (np.sqrt(2) * np.linalg.norm(D, 2) * np.linalg.norm(u))
def Fk(x, k):
    hN, hm = x[:2], x[2]; C = k * D @ hN
    return np.r_[-rN_ * hN - j * hm + C * hm, j @ hN - C @ hN - rM_ * hm] + u
print(f"rho*={rho:.3f}, |u|={np.linalg.norm(u):.3f}, h_bar=|u|/rho*={hbar:.2f}; (SG) holds for |k| < k_SG = {k_SG:.4f}; K6 uses |k| up to {abs(k_full):.3f}")
for frac in (0.0, k_SG / abs(k_full) * 0.99, 0.05, 0.25, 0.5, 1.0):
    k = frac * k_full; sols = {}
    for g in np.random.default_rng(1).normal(0, 4, (400, 3)):
        x, info, ier, _ = fsolve(lambda z: Fk(z, k), g, full_output=True)
        if ier == 1 and np.abs(Fk(x, k)).max() < 1e-9:
            Jn = np.column_stack([(Fk(x + 1e-6 * e, k) - Fk(x - 1e-6 * e, k)) / 2e-6 for e in np.eye(3)])
            sols[tuple(float(v) for v in np.round(x, 3))] = np.linalg.eigvals(Jn).real.max()
    st = sum(v < 0 for v in sols.values())
    print(f"|k| = {abs(k):7.4f} ({'inside' if abs(k) < k_SG else 'outside'} SG): {len(sols)} equilibria, {st} stable")
# first |k| with more than one equilibrium
ks = np.linspace(0, abs(k_full), 200); onset = None
for kk in ks:
    k = np.sign(k_full) * kk; sols = set()
    for g in np.random.default_rng(2).normal(0, 4, (150, 3)):
        x, info, ier, _ = fsolve(lambda z: Fk(z, k), g, full_output=True)
        if ier == 1 and np.abs(Fk(x, k)).max() < 1e-9: sols.add(tuple(np.round(x, 3)))
    if len(sols) > 1: onset = kk; break
print(f"bistability onset at |k| ~ {onset:.3f}; SG threshold {k_SG:.4f} (sufficient, conservative by x{onset / k_SG:.0f})")

# ---------------------------------------------------------------------------
hdr("S5  T9: learning is open-loop in the agent's own following (own-part targets) -> no copy reinforcement")
# Scalar dyad on a 10 Hz grid. Partner own part y_own: AR(1) a. Agent act eps_t = f*y_{t-1} + zeta_t (following f).
# Partner actual y_t = y_own_t + kp*eps_{t-1} (partner answers the agent).  Body (innate port): b_t = g*y_t + noise.
# Naive consequence fit (OLS of b_t on eps_{t-1}) and total IV (zeta) both learn 'my act relieves/changes my body via you';
# rev 3 fits b_own_t = b_t - g*kp_hat*eps_{t-1}: the partner-mediated path is removed, so the estimate is ~0 for every f.
def run(f, kp, T=60000, a=0.8, g=0.7, seed=0):
    r = np.random.default_rng(seed)
    yown = np.zeros(T); eps = np.zeros(T); y = np.zeros(T); zeta = r.normal(0, 1, T)
    for t in range(1, T):
        yown[t] = a * yown[t-1] + r.normal(0, 0.6)
        y[t] = yown[t] + kp * eps[t-1]
        eps[t] = f * y[t-1] + zeta[t]
    b = g * y + r.normal(0, 0.5, T)
    E1, B, Z1 = eps[1:-1], b[2:], zeta[1:-1]
    naive = np.dot(E1 - E1.mean(), B - B.mean()) / np.dot(E1 - E1.mean(), E1 - E1.mean())
    iv_total = np.dot(Z1, B) / np.dot(Z1, E1)
    kp_hat = np.dot(zeta[1:-1], y[2:]) / np.dot(zeta[1:-1], eps[1:-1])     # T5 kernel on y
    bown = b[2:] - g * kp_hat * eps[1:-1]
    iv_own = np.dot(Z1, bown) / np.dot(Z1, E1)
    return naive, iv_total, iv_own, kp_hat
for kp in (0.0, 0.5):
    for f in (0.0, 0.4, 0.8):
        nv, it, io, kh = run(f, kp)
        print(f"partner answers kp={kp:.1f}, agent follows f={f:.1f}: naive={nv:+.3f}  IV total={it:+.3f}  IV own-part (rev 3)={io:+.3f}  (kp_hat={kh:+.3f})")
print("  -> naive grows with f (self-reinforcing: following -> 'you answer me' -> wanting -> more following);\n"
      "     IV total = g*kp (wanting the partner's response: the Principle 6 hazard); own-part ~ 0 for all (f, kp).")

# ---------------------------------------------------------------------------
hdr("S6  T6 corrected: onset exponents of the same-group routes (step in the partner's smile at t'=0)")
dt = 1e-5; ts = np.arange(dt, 0.3, dt)
def cascade(stages, inp):
    """stages: list of ('int', gain) integrator or ('lp', tau) low-pass; inp: 'step' or 'ramp'"""
    x = [0.0] * len(stages); out = []
    for t in ts:
        u = 1.0
        for i, (kind, p) in enumerate(stages):
            if kind == 'int': x[i] += dt * p * u
            else: x[i] += dt * (u - x[i]) / p
            u = x[i]
        out.append(u)
    return np.array(out)
routes = {
  "innate match (band-pass then muscle)": [('lp', 0.15), ('lp', 0.1)],
  "port s7 -> N -> M_g -> muscle": [('int', 1.0), ('int', 1.0), ('lp', 0.1)],
  "observer -> beta trace -> regard low-pass -> muscle": [('int', 1.0), ('lp', 1.5), ('lp', 0.1)],
  "observer -> beta -> N -> M_g -> muscle (learned loop)": [('int', 1.0), ('int', 1.0), ('int', 1.0), ('lp', 0.1)],
}
for name, st in routes.items():
    o = cascade(st, 'step'); i1, i2 = int(0.002 / dt), int(0.004 / dt)
    print(f"{name:55s} local log-log slope near t'=3 ms: {np.log(o[i2] / o[i1]) / np.log(2):.2f}")
