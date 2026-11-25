"""Critique 2 of design-partner-regulator.md (revision 2): algebra checks on hand-set instances.
Not evidence about behaviour or people.  Run from research/foundations/sims:
    uv run python -I critique-2-partner-regulator/check.py
"""
import numpy as np
from scipy.integrate import solve_ivp
rng = np.random.default_rng(0)
def hdr(s): print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)

# -----------------------------------------------------------------------------
hdr("K1  The W-loop reaches a PURE same-group copy at DC under the mask and (A3)")
# Two needs n1, n2; two act groups (smile m1 driven by n1, brow m2 driven by n2); partner smile ys, brow yb.
# Mask respected: no learned term in the m-rows reads the partner at all (B_M = 0).
# Partner enters only through damping coefficients on N: beta_1 = -bm*tanh(k*ys), beta_2 = -bm*tanh(k*yb)
# (contagious sign; beta reads the FULL observer, which (S2) allows because D acts on N only).
# (A3): bm*||D|| < r_N.  Tonic input u keeps the operating drive h_N0 > 0.
rN, rM, w, Ep = 0.5, 20.0, 3.0, 10.0
def rhs(t, x, bm, k, u, ys, yb):
    n1, n2, m1, m2 = x
    b1, b2 = -bm * np.tanh(k * ys(t)), -bm * np.tanh(k * yb(t))
    return [-(rN + b1) * n1 - w * m1 + u, -(rN + b2) * n2 - w * m2 + u, w * n1 - rM * m1, w * n2 - rM * m2]
def dc_transfer(bm, k, u, eps=1e-4):
    def eq(ys, yb):
        b1, b2 = -bm * np.tanh(k * ys), -bm * np.tanh(k * yb)
        n1 = u / (rN + b1 + w * w / rM); n2 = u / (rN + b2 + w * w / rM)
        return Ep * np.array([w * n1 / rM, w * n2 / rM])
    e0 = eq(0, 0)
    return np.column_stack([(eq(eps, 0) - e0) / eps, (eq(0, eps) - e0) / eps])
for bm in (0.0, 0.1, 0.25, 0.45):
    for u in (0.5, 1.0):
        G = dc_transfer(bm, 2.0, u)
        h0 = u / (rN + w * w / rM)
        cd = np.abs(G[[0, 1], [1, 0]]).max() / max(np.abs(G).max(), 1e-12)
        print(f"b-_bar={bm:4.2f} (A3: < r_N={rN})  tonic u={u}  h_N0={h0:.2f}:  DC transfer =\n"
              f"   {np.round(G, 3).tolist()}   off-diagonal/diagonal = {cd:.1e}")
# Large-signal: slow independent partner signals; does my expression follow them channel by channel?
def ou(T, tau, seed, dt=0.05):
    r = np.random.default_rng(seed); n = int(T / dt) + 2; y = np.zeros(n)
    for i in range(1, n): y[i] = y[i - 1] - dt * y[i - 1] / tau + np.sqrt(2 * dt / tau) * r.normal()
    ts = np.arange(n) * dt
    return lambda t: np.interp(t, ts, y)
for tau in (20.0, 0.3):
    ys, yb = ou(600, tau, 1), ou(600, tau, 2)
    sol = solve_ivp(rhs, (0, 600), [1, 1, 0, 0], args=(0.45, 2.0, 1.0, ys, yb), max_step=0.02, t_eval=np.arange(50, 600, 0.1))
    es, eb = Ep * sol.y[2], Ep * sol.y[3]
    Ys, Yb = ys(sol.t), yb(sol.t)
    c = lambda a, b: np.corrcoef(a, b)[0, 1]
    X = np.column_stack([Ys, Yb, np.ones_like(Ys)])
    Bfit = np.linalg.lstsq(X, np.column_stack([es, eb]), rcond=None)[0][:2].T
    print(f"partner signals with correlation time {tau:5.1f} s: corr(my smile, partner smile)={c(es, Ys):.3f}, "
          f"corr(my smile, partner brow)={c(es, Yb):.3f}, corr(my brow, partner brow)={c(eb, Yb):.3f}; fitted transfer {np.round(Bfit, 3).tolist()}")
# frequency response of the copy entry
for om in (0.0, 0.1, 0.3, 1.0, 3.0, 10.0):
    bm, k, u = 0.45, 2.0, 1.0
    h0 = u / (rN + w * w / rM)
    A = np.array([[-rN, -w], [w, -rM]]); Bv = np.array([bm * k * h0, 0.0])
    g = Ep * np.linalg.solve(1j * om * np.eye(2) - A, Bv)[1]
    print(f"  omega={om:5.1f} rad/s: |copy entry| = {abs(g):.3f}")
print("  -> one scalar (b-_bar, the reading slope k, or the tonic drive h_N0) runs the sustained transfer from 0 to a\n"
      "     block-diagonal (copy-pattern) map with zero cross-group part: the copy defect of the TOTAL transfer is 0 at DC.")

# -----------------------------------------------------------------------------
hdr("K2  Slow learned context r_j is a functional of the partner's same group: the mask is bypassed")
# alpha for the smile atom reads c^(smile) = (masked observer, r_j, ...).  (S2) admits r_j.
# r_j is updated online (every 5 s) by the body-prediction loss, whose rollout uses beta(c^beta) with c^beta
# built from the FULL observer (which sees the partner's smile).  Minimal misspecified instance:
# true body target b = c0 (partner-independent); model b_hat = tanh(ys + r); LMS on r.
c0, lr = 0.3, 0.02
for mu in (-0.4, 0.0, 0.4):
    r_ = 0.0; rr = np.random.default_rng(3)
    for step in range(20000):
        ys = mu + 0.3 * rr.normal()
        bh = np.tanh(ys + r_)
        r_ -= lr * (bh - c0) * (1 - bh ** 2)
    abar, v, hN0, omg, rMm = 0.5, 1.0, 1.0, 1.0, 20.0
    alpha = abar * np.tanh(v * r_)
    my_smile = Ep * alpha * omg * hN0 / rMm
    print(f"partner's mean smile in the session mu={mu:+.1f}: learned r_j={r_:+.3f}  -> sustained own smile via alpha(r_j) = {my_smile:+.3f}")
print("  -> d(own smile)/d(partner mean smile) != 0 with no path through W: a direct same-group route at the time\n"
      "     scale of r_j's updates (minutes). T1'(b) holds only with r_j, adapters and kernels frozen.")

# -----------------------------------------------------------------------------
hdr("K3  T6(a) misses the direct innate port into N: same-group onset ~ t'^3, not t'^4")
# Partner's smile steps at t'=0.  Observer surprise s7 = |y - E(x_hat)| (full observer) steps at once
# (first-order change (nu0/|nu0|)^T dy for a nonzero baseline innovation nu0). (*') feeds G s directly into N.
G7, wbar, Epp, tau_m, lam_o, c_inj = 0.5, 1.0, 10.0, 0.1, 2.0, 0.5
dt = 1e-4; ts = np.arange(0, 0.6, dt)
xN = xM = m = 0.0; out = []
for t in ts:
    xN += dt * (-0.5 * xN + G7 * 1.0)         # step injection into N through the innate port
    xM += dt * (-20.0 * xM + wbar * xN)       # learned routing N -> own smile (A_gW)
    m += dt * (Epp * xM - m) / tau_m          # muscle
    out.append(m)
out = np.array(out)
Lam = lam_o * c_inj * wbar * Epp / tau_m      # T6's Lambda_g (no G term)
for tt in (0.05, 0.1, 0.2, 0.3, 0.5):
    i = int(tt / dt)
    print(f"t'={tt:4.2f}s port route={out[i]:.2e}  T6(a) bound a*Lam*t'^4/24={Lam * tt ** 4 / 24:.2e}  ratio={out[i] / (Lam * tt ** 4 / 24):6.1f}"
          f"  (t'^3 law G*wbar*E'/tau_m*t'^3/6={G7 * wbar * Epp / tau_m * tt ** 3 / 6:.2e})")

# -----------------------------------------------------------------------------
hdr("K4  The concern target is the agent's own resting face E(0), not the partner's rest")
# scalar observer: x_hat' = -(r) x_hat + L (y - E(x_hat)),  E(z) = S*sigmoid(wz + b).  Steady x_hat for a partner face y.
from scipy.optimize import brentq
S, wE, L, r_o = 1.0, 2.0, 3.0, 1.0
sig = lambda z: 1 / (1 + np.exp(-z))
for b in (-3.0, -1.0, 0.0):
    E = lambda z: S * sig(wE * z + b)
    xs = lambda y: brentq(lambda z: -r_o * z + L * (y - E(z)), -20, 20)
    y_neutral = 0.02                           # a human neutral smile blendshape value
    print(f"E bias b={b:+.1f}: E(0)={E(0):.3f}; partner neutral face (smile={y_neutral}) read as x_hat={xs(y_neutral):+.3f} "
          f"(H_hat={0.5 * xs(y_neutral) ** 2:.3f}); concern drive vanishes only at partner face y=E(0)={E(0):.3f} (x_hat={xs(E(0)):+.1e})")

# -----------------------------------------------------------------------------
hdr("K5  (A6) is not implied: random search for an unstable operating point with J_soc and tonic input")
# n = (n1, n2, m).  F(x) = J0 + J_soc(h_N) - R, J_soc = [[0, C],[-C^T, 0]], C = k * D h_N (D = a a^T),
# alpha context depends on h_N (episode code): J0_NM column scaled by (1 + c_ep * tanh(p . h_N)).
# (A2)-(A3) hold (R >= floors, skew J), so T0 holds; we look for Re(lambda) > 0 of the Jacobian at an equilibrium.
from scipy.optimize import fsolve
found = None; tried = 0
for s in range(4000):
    r = np.random.default_rng(s)
    rN_, rM_ = r.uniform(0.05, 1), r.uniform(1, 20)
    a = r.normal(size=2); a /= np.linalg.norm(a); D = np.outer(a, a)
    j = r.normal(0, 1.5, 2); k = r.normal(0, 3); cep = r.uniform(-1, 1); p = r.normal(0, 2, 2)
    u = np.r_[r.normal(0, 2, 2), 0.0]
    def F(x):
        hN, hm = x[:2], x[2]
        jj = j * (1 + cep * np.tanh(p @ hN))
        C = k * D @ hN
        xN = -rN_ * hN - jj * hm + C * hm
        xm = jj @ hN - C @ hN - rM_ * hm
        return np.r_[xN, xm] + u
    x0 = fsolve(F, np.zeros(3), full_output=True)
    if x0[2] != 1: continue
    xe = x0[0]; tried += 1
    Jn = np.column_stack([(F(xe + 1e-6 * e) - F(xe - 1e-6 * e)) / 2e-6 for e in np.eye(3)])
    lam = np.linalg.eigvals(Jn)
    if lam.real.max() > 1e-3:
        found = (s, xe, lam); break
if found:
    s, xe, lam = found
    print(f"seed {s} (after {tried} equilibria): x_eq={np.round(xe, 3).tolist()}, eigenvalues={np.round(lam, 3).tolist()}"
          " -> an unstable operating point although (A2)-(A3) hold; T1' and T6 do not apply there.")
else:
    print(f"no unstable operating point in {tried} equilibria (A6 not refuted on this family)")

# -----------------------------------------------------------------------------
hdr("K6  J_soc's state dependence makes the operating point non-unique under (A2)-(A3) (T1'(f)(i) says unique)")
# Same family as K5 with the episode term removed (c_ep = 0): only J0 (constant skew), J_soc(h_N), floors, tonic u.
r = np.random.default_rng(31)
rN_, rM_ = r.uniform(0.05, 1), r.uniform(1, 20)
a = r.normal(size=2); a /= np.linalg.norm(a); D = np.outer(a, a)
j = r.normal(0, 1.5, 2); k_full = r.normal(0, 3); _ = r.uniform(-1, 1); _ = r.normal(0, 2, 2)
u = np.r_[r.normal(0, 2, 2), 0.0]
def Fk(x, k):
    hN, hm = x[:2], x[2]; C = k * D @ hN
    return np.r_[-rN_ * hN - j * hm + C * hm, j @ hN - C @ hN - rM_ * hm] + u
for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
    k = frac * k_full; sols = {}
    for g in np.random.default_rng(1).normal(0, 4, (300, 3)):
        x, info, ier, _ = fsolve(lambda z: Fk(z, k), g, full_output=True)
        if ier == 1 and np.abs(Fk(x, k)).max() < 1e-9:
            Jn = np.column_stack([(Fk(x + 1e-6 * e, k) - Fk(x - 1e-6 * e, k)) / 2e-6 for e in np.eye(3)])
            sols[tuple(float(v) for v in np.round(x, 3))] = np.linalg.eigvals(Jn).real.max()
    st = sum(v < 0 for v in sols.values())
    print(f"concern strength k = {frac:.2f} x {k_full:.2f}: {len(sols)} equilibria, {st} stable; "
          + "; ".join(f"{list(x)} maxRe={v:+.2f}" for x, v in sorted(sols.items())))
print("  -> the concern scale (set by the partner's read distress and kappa_bar) takes the agent from one operating point\n"
      "     to bistability; which state it sits in depends on history. H still decreases outside a ball (T0 is intact).")
