"""Algebra checks for critique-design-partner-regulator.md.

Each check runs the design's own equation (*) on a small hand-set instance:
  xdot = [J0 + pi*Omega(c) - R0(x) - pi*D(c)] h(x) + additive inputs.
They test the design's algebra and the critique's counterexamples. They are not
evidence about behaviour or about people.
"""
import numpy as np
from scipy.integrate import solve_ivp

np.set_printoptions(precision=4, suppress=True)
rng = np.random.default_rng(0)


def hdr(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ---------------------------------------------------------------------------
hdr("C1  T0(b) plateau numbers (design: d=-1 -> 0.87, d=-2 -> 1.74)")
# need-act loop, q=1, no walls: z' = [[-(rN+d+k|z|^2), -w], [w, -(rM+k|z|^2)]] z
rN, rM, w, ks = 0.2, 2.0, 1.0, 0.5


def loop(t, z, d, rN=rN, rM=rM, w=w, ks=ks):
    s = ks * (z @ z)
    return np.array([-(rN + d + s) * z[0] - w * z[1], w * z[0] - (rM + s) * z[1]])


for d in (-1.0, -2.0):
    sol = solve_ivp(loop, (0, 400), [1e-3, 0.0], args=(d,), rtol=1e-9, atol=1e-12)
    zf = sol.y[:, -1]
    a = rN + d
    # analytic: det=0 at s: (a+s)(rM+s)+w^2=0
    s = np.roots([1, a + rM, a * rM + w * w]).max()
    print(f"d={d}: sim |z|={np.linalg.norm(zf):.4f}  analytic {np.sqrt(s / ks):.4f}  "
          f"equilibrium z={zf}  (x* is no longer the attractor)")

# ---------------------------------------------------------------------------
hdr("C2  T0(a) fails once the learned interoceptive term -K_b C_b x_N is in the loop")
# Same loop, no partner contagion (d=+0.1, 'bounded contagion' holds), b held at b*=0.
# The term K_b(b - C_b x_N) = -K_b C_b x_N is linear in x with learned, unconstrained K_b, C_b.
for KbCb in (0.0, -1.0):
    def f(t, z):
        base = loop(t, z, 0.1, ks=0.0)          # T0(a) setting: no saturation needed
        base[0] += -KbCb * z[0]                  # additive 'input' that is really feedback
        return base
    sol = solve_ivp(f, (0, 60), [0.1, 0.0], rtol=1e-9)
    J = np.array([[-(rN + 0.1) - KbCb, -w], [w, -rM]])
    print(f"K_b C_b={KbCb:+.1f}: |z(60)|={np.linalg.norm(sol.y[:, -1]):.3e}  "
          f"eig={np.linalg.eigvals(J)}")

# ---------------------------------------------------------------------------
hdr("C3  P6 'stable iff d > -r_N,eff; trace then negative' misses the Hopf branch")
rN2, rM2, w2, d2 = 0.2, 0.5, 2.0, -1.5
A = np.array([[-(rN2 + d2), -w2], [w2, -rM2]])
print(f"r_N={rN2}, r_M={rM2}, omega={w2}, d={d2}; -r_N,eff = {-(rN2 + w2**2 / rM2):.2f}")
print(f"det={np.linalg.det(A):.3f} (>0), trace={np.trace(A):.3f} (>0!) eig={np.linalg.eigvals(A)}")
sol = solve_ivp(loop, (0, 200), [1e-3, 0.0], args=(d2, rN2, rM2, w2, 0.5), rtol=1e-9,
                dense_output=True)
tt = np.linspace(150, 200, 2000)
zz = sol.sol(tt)
print(f"with saturation k_s=0.5: late z_N range [{zz[0].min():.3f}, {zz[0].max():.3f}] "
      f"-> a limit cycle whose sign alternates (not a plateau with the initial sign)")
print(f"correct threshold: d > -r_N - min(r_M, omega^2/r_M) = {-rN2 - min(rM2, w2**2 / rM2):.2f}")

# ---------------------------------------------------------------------------
hdr("C4  Dial at a tonic drive: steady-state copy with gain ~ a_bar * u_N")
# N = 1 need, M = 2 acts (smile, frown). Dictionary q=1,2: Omega_q = e_N e_Mq^T - e_Mq e_N^T,
# alpha_q(o) = -a_bar * tanh(o_q)  (the design's own P5 example, alpha(o) = -o_k).
# Tonic additive drive u_N > 0 (body drift of the contingency deficit via K_b; or G s).
rN, rM = 0.2, 2.0


def Fmat(o, abar):
    al = -abar * np.tanh(o)
    F = np.zeros((3, 3))
    for q in range(2):
        F[0, 1 + q] += al[q]        # Omega_q row N
        F[1 + q, 0] -= al[q]        # Omega_q row M_q
    F -= np.diag([rN, rM, rM])
    return F


uN = 0.3
O = rng.normal(0, 0.7, size=(400, 2))
for abar in (0.0, 0.1, 0.5, 1.0):
    Z = np.array([np.linalg.solve(Fmat(o, abar), -np.array([uN, 0, 0])) for o in O])
    X = np.tanh(O)
    Gam, *_ = np.linalg.lstsq(X, Z[:, 1:], rcond=None)
    pred = X @ Gam
    r2 = 1 - ((Z[:, 1:] - pred) ** 2).sum() / max(((Z[:, 1:] - Z[:, 1:].mean(0)) ** 2).sum(), 1e-30)
    print(f"a_bar={abar:.1f}: steady acts = Gamma tanh(o), Gamma=\n{Gam.T}  R^2={r2:.3f}")
print("-> a_bar (or u_N, or pi) runs the steady partner->self transfer from 0 to a diagonal copy.")

# same, with uN = 0 (the theorem's setting): flat for every a_bar
Z0 = np.array([np.linalg.solve(Fmat(o, 1.0), np.zeros(3)) for o in O[:5]])
print(f"u_N = 0: steady acts {np.abs(Z0).max():.1e} for every o (T1(i) holds only here)")

# time-varying partner: does the agent track the partner like a filtered copy?
T = 120.0
tgrid = np.linspace(0, T, 3601)
raw = rng.normal(size=(3601, 2))
from scipy.ndimage import gaussian_filter1d
o_t = gaussian_filter1d(raw, 60, axis=0) * 8


def track(abar):
    def f(t, z):
        i = min(int(t / T * 3600), 3600)
        return Fmat(o_t[i], abar) @ z + np.array([uN, 0, 0])
    s = solve_ivp(f, (0, T), [uN / rN, 0, 0], t_eval=tgrid, max_step=0.05)
    c = [np.corrcoef(s.y[1 + q, 300:], np.tanh(o_t[300:, q]))[0, 1] for q in range(2)]
    return c, np.std(s.y[1:, 300:])


for abar in (0.0, 0.2, 1.0):
    c, sd = track(abar)
    print(f"a_bar={abar}: corr(own act_q, partner tanh o_q) = {np.round(c, 3)}  act sd={sd:.3f}")

# ---------------------------------------------------------------------------
hdr("C5  Net contagion: the partner's context chooses the attractor direction")
# N = 1, M = 2. Context A routes need->smile, B routes need->frown; both remove damping on N.


def contagion(ctx, sign0):
    al = np.array([1.0, 0.0]) if ctx == "A" else np.array([0.0, 1.0])
    d = -1.0

    def f(t, z):
        s = 0.5 * (z @ z)
        F = np.zeros((3, 3))
        for q in range(2):
            F[0, 1 + q] -= al[q]
            F[1 + q, 0] += al[q]
        F -= np.diag([rN + d + s, rM + s, rM + s])
        return F @ z
    return solve_ivp(f, (0, 300), [sign0 * 1e-3, 0, 0], rtol=1e-9).y[:, -1]


for ctx in "AB":
    for s0 in (+1, -1):
        print(f"context {ctx}, initial sign {s0:+d}: equilibrium (z_N, smile, frown) = {contagion(ctx, s0)}")
print("-> equilibrium set = {x*} U {+-z_e(c)}; z_e's direction is set by the partner context.")

# ---------------------------------------------------------------------------
hdr("C6  At satiety, an innate seed + learned routing: the partner's content sets the sign")
# x starts at x* (sated). Mutual gaze (innate, fixed sign) pushes N through G s.
# alpha(o) routes N into the smile act with a sign that depends on the partner's expression.
Gs = 0.2
for label, al_smile in (("partner smiles (alpha=-1)", -1.0), ("partner angry, cooperative (alpha=-1)", -1.0),
                        ("partner angry, rival (alpha=+1)", +1.0)):
    def f(t, z):
        F = np.array([[-rN, al_smile], [-al_smile, -rM]])
        return F @ z + np.array([Gs, 0.0])
    s = solve_ivp(f, (0, 30), [0.0, 0.0], t_eval=[0.1, 0.5, 1.0, 3.0, 30.0], rtol=1e-9)
    print(f"{label:40s} smile act at t=0.1,0.5,1,3,30 s: {s.y[1]}")
print("-> response at satiety is not zero in the full system; it grows ~t^2 at onset;")
print("   its sign is fixed by alpha(o, r_j), i.e. by the partner's content and relation.")

# ---------------------------------------------------------------------------
hdr("C7  T1(v) oddness fails once the episode code e depends on h (design 5.7 retrieval)")
h_mu = np.array([1.0, 0.0, 0.0])


def run_with_retrieval(z0):
    def f(t, z):
        cos = z @ h_mu / (np.linalg.norm(z) + 1e-12)
        al = np.tanh(2 * cos)                       # alpha depends on e, e on cos(h, h_mu)
        F = np.array([[-rN, -al, 0], [al, -rM, 0], [0, 0, -rM]])
        F[0, 2], F[2, 0] = -0.5, 0.5
        return F @ z
    return solve_ivp(f, (0, 3), z0, t_eval=[3.0], rtol=1e-10).y[:, -1]


z0 = np.array([0.5, 0.2, -0.1])
a, b = run_with_retrieval(z0), run_with_retrieval(-z0)
print(f"z(3; z0)={a}  z(3; -z0)={b}  sum={a + b} (zero iff odd)")

# ---------------------------------------------------------------------------
hdr("C8  T4(b): dim V <= 4K is false for small K; the block bound gives 128 at K=32")
nN, nMC = 64, 192
for K in (1, 4, 32):
    cols = []
    for q in range(K):
        U = np.vstack([rng.normal(size=(nN, 2)), np.zeros((nMC, 2))])
        V = np.vstack([np.zeros((nN, 2)), rng.normal(size=(nMC, 2))])
        Aq = np.vstack([rng.normal(size=(nN, 2)), np.zeros((nMC, 2))])
        cols += [U, V, Aq]
    rk = np.linalg.matrix_rank(np.hstack(cols))
    print(f"K={K:2d}: dim V = {rk}, design's bound 4K = {4 * K}, block bound min(64,4K)+min(192,2K) = "
          f"{min(64, 4 * K) + min(192, 2 * K)}")
# reachability: a private direction (C coordinate outside span V) is still moved by the partner
# through J0's N-C block.
def priv(dval):
    def f(t, z):  # z = (N, M, C_private)
        F = np.array([[-(0.2 + dval), -1.0, -0.3], [1.0, -2.0, 0.0], [0.3, 0.0, -0.05]])
        return F @ z
    return solve_ivp(f, (0, 20), [1.0, 0, 0], t_eval=[20.0]).y[2, -1]
print(f"private C coordinate at t=20 with partner damping d=0: {priv(0.0):.4f}, d=0.5: {priv(0.5):.4f}"
      " -> not 'unreachable', only not directly actuated")

# ---------------------------------------------------------------------------
hdr("C9  T3 ladder numbers, and the role of r_C")
for rC in (0.0, 1e-5, 1e-3):
    Jp = np.zeros((3, 3))
    Jp[0, 1], Jp[1, 0] = -1.0, 1.0
    Jp[0, 2], Jp[2, 0] = -0.002, 0.002
    M = Jp - np.diag([0.05, 20.0, rC])
    ev = np.sort(np.linalg.eigvals(M).real)
    print(f"r_C={rC:g}: eig = {np.array2string(ev, formatter={'float_kind': lambda v: f'{v:.3e}'})}  slowest rate vs r_C + w_NC^2/r_N,eff = {rC + 0.002**2 / 0.1:.2e}")
print("-> the design's 7 h mode needs r_C ~ 0, but A2 requires R_min > 0 and T0(a)'s rate is min(.., r_C).")

# T3(c): pi vs pi^2
w0, aq, wq, piv = 1.0, 0.5, 1.0, 0.5
exact = ((w0 + piv * aq * wq) ** 2 - w0 ** 2) / 2.0
design = piv * ((w0 + aq * wq) ** 2 - w0 ** 2) / 2.0
print(f"T3(c) Delta r_N,eff at pi=0.5: exact {exact:.4f}, design formula {design:.4f}")

# ---------------------------------------------------------------------------
hdr("C10 P7 protest peak t* = tau_N ln(1 + tau_pi/tau_N)")
tN, tp = 60.0, 120.0
t = np.linspace(0, 400, 400001)
A_ = np.exp(-t / tp) * (1 - np.exp(-t / tN))
print(f"numeric {t[A_.argmax()]:.3f} s, formula {tN * np.log(1 + tp / tN):.3f} s")
# with the generic routing J0 also present, act drive = (w0 + pi*w_j) h_N: no despair if w0 > 0
for w0 in (0.0, 0.3):
    Ad = (w0 + np.exp(-t / tp)) * (1 - np.exp(-t / tN))
    print(f"generic routing w0={w0}: act drive at peak {Ad.max():.3f}, at t=400 s {Ad[-1]:.3f}")
