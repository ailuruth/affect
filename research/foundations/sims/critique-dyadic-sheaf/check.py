"""Algebra checks for critique-design-dyadic-sheaf.md. They check the design's own
equations (linear core, V=0, U quadratic); they are not evidence about behaviour."""
import numpy as np
np.set_printoptions(precision=4, suppress=True)
rng = np.random.default_rng(0)

def build(A, R, W, CB, Pi, Pf, P, Lam, Ks, Kb, gamma0, theta):
    n = A.shape[1]
    LR = R.T @ P @ R
    Gam = (gamma0 + (1 - theta) / theta * (np.linalg.norm(LR, 2) + np.linalg.norm(Lam, 2))) * np.eye(n)
    La = A.T @ Pf @ A + CB.T @ (Ks + Kb) @ CB + Gam
    S = R.T @ P + CB.T @ Lam @ W
    K = A.T @ Pi @ A
    Hxx = LR + CB.T @ Lam @ CB + La
    Hzz = K + P + W.T @ Lam @ W
    H = np.block([[Hxx, -S], [-S.T, Hzz]])
    return dict(H=H, Hxx=Hxx, Hzz=Hzz, S=S, K=K, La=La, Gam=Gam, LR=LR)

def transfer(A, d, Pi):
    """T = d(A x*)/dy at the fast equilibrium (Lemma 1 linear solve)."""
    n = A.shape[1]
    rhs = np.vstack([np.zeros((n, A.shape[0])), A.T @ Pi])
    sol = np.linalg.solve(d["H"], rhs)
    return A @ sol[:n]

def scalar_T(p, lam, r, w, k, gamma0, theta, e=0.0):
    a = 1.0
    G = gamma0 + (1 - theta) / theta * (p * r * r + lam)
    Hxx = p * r * r + lam + G + e
    Hzz = k + p + lam * w * w
    S = p * r + lam * w
    D = Hxx * Hzz - S * S
    return k * S / D, D

print("== C1  Theorem 1(b)(i): eigenvalues of M_p <= theta (random draws)")
worst = 0
for _ in range(2000):
    n, nb, kk = 6, 2, 7
    A = rng.normal(size=(kk, n)); R = rng.normal(size=(n, n)) * rng.uniform(0.1, 3)
    W = rng.normal(size=(nb, n)) * rng.uniform(0.1, 3); CB = np.eye(n)[:nb]
    P = np.diag(rng.uniform(0.1, 5, n)); Lam = np.diag(rng.uniform(0.1, 5, nb))
    d = build(A, R, W, CB, np.eye(kk), np.eye(kk) * 0.1, P, Lam, np.eye(nb) * .1, np.eye(nb) * .1, 0.01, 0.5)
    Lp = d["LR"] + CB.T @ Lam @ CB
    ev = np.linalg.eigvals(np.linalg.solve(d["La"] + Lp, Lp)).real.max()
    worst = max(worst, ev)
print("  max eigenvalue over draws:", round(worst, 4), "(bound 0.5) -> holds")

print("\n== C2  Dial hunt: theta on the copy maps (r=w=1), scalar channel, k=1, p=lam=0.5, tiny anchor")
for th in [0.05, 0.25, 0.5, 0.75, 0.9, 0.99, 0.999]:
    T, _ = scalar_T(0.5, 0.5, 1, 1, 1.0, 1e-4, th)
    print(f"  theta={th:<6} T={T:.4f}   formula theta*k/(k+(1-theta)q) = {th*1/(1+(1-th)*1.0):.4f}")

print("\n== C3  Dial hunt: learned contingency scale r (rho edge only, lam=0), k=p=1, gamma0=0.01, theta=0.5")
rs = np.linspace(0.001, 2, 20001)
Ts = np.array([scalar_T(1, 0, r, 0, 1, 0.01, 0.5)[0] for r in rs])
i = Ts.argmax(); print(f"  T(r) peaks at r={rs[i]:.4f}, T={Ts[i]:.3f};  closed form k p/(2 sqrt(p(2k+p) g (k+p))) = {1/(2*np.sqrt(3*0.01*2)):.3f}")
j = np.where(np.diff(np.sign(Ts - 1)))[0]
print("  exact copy (T=1) at r =", np.round(rs[j], 4))
for r in [0.0, 0.01, 0.03, rs[j[0]], 0.08, 0.3, 1.0]:
    print(f"   r={r:.4f}  T={scalar_T(1,0,r,0,1,0.01,0.5)[0]:.4f}")

print("\n== C4  Same, as a matrix: A=I (k=n=6), R=r I, W=0, P=I, Pi=I: T is exactly c(r) I (dial rank 1)")
n = 6; A = np.eye(n); CB = np.eye(n)[:2]
for r in [0.0, 0.03, float(rs[j[0]]), 0.3, 1.0]:
    d = build(A, r * np.eye(n), np.zeros((2, n)), CB, np.eye(n), 1e-9 * np.eye(n), np.eye(n), 1e-9 * np.eye(2), 1e-9*np.eye(2), 1e-9*np.eye(2), 0.01, 0.5)
    T = transfer(A, d, np.eye(n))
    print(f"   r={r:.4f}  diag(T)={np.diag(T)[:3]}  max offdiag={np.abs(T-np.diag(np.diag(T))).max():.1e}")

print("\n== C5  Dial hunt: gamma0 at fixed learned r=1/3 (k=p=1): T -> k/(r(2k+p)) = 1 as gamma0 -> 0")
for g0 in [10, 1, 0.1, 0.01, 1e-3, 1e-5]:
    print(f"   gamma0={g0:<7} T={scalar_T(1,0,1/3,0,1,g0,0.5)[0]:.4f}")

print("\n== C6  Dial hunt: consequence weight w (r=0), lam=0.01, k=1, p=0.01, gamma0=1e-3")
for w in [0, 1, 3, 10, 14, 30, 100]:
    print(f"   w={w:<4} T={scalar_T(0.01,0.01,0,w,1,1e-3,0.5)[0]:.4f}")

print("\n== C7  Facial-feedback loop: reflex theta_r y -> m -> f -> disp edge -> x -> A x -> m")
# scalar steady state: m = a x + th_r y ; x minimises 0.5 Pf (a x - m)^2 + 0.5 c x^2 (all other terms folded into c)
a, th_r, c = 1.0, 0.3, 1.0
for Pf in [0, 1, 10, 100, 1000]:
    g = Pf * a * a / (Pf * a * a + c)          # x = (Pf a m)/(Pf a^2 + c); a x = g m
    m_over_y = th_r / (1 - g)
    print(f"   Pi_f={Pf:<5} loop gain={g:.4f}  m/y = {m_over_y:.3f}  (reflex alone 0.3)")

print("\n== C8  Theorem 3(b): with (N) the anchor removes the (1-mu)^-2 slow mode (partner gone, K=0)")
for (r, w) in [(1, 0), (1, .5), (1, .9), (1, .99), (1, 1.0), (.1, 10)]:
    p, lam = 1.0, 1.0
    L_so = np.array([[p*r*r+lam, -(p*r+lam*w)], [-(p*r+lam*w), p+lam*w*w]])
    G = 0.01 + 1.0 * (p*r*r + lam)
    H = L_so + np.diag([G, 0.0])
    print(f"   mu={r*w:<5} lam_min(L_so)={np.linalg.eigvalsh(L_so).min():.4f}   lam_min(H with N)={np.linalg.eigvalsh(H).min():.4f}")

print("\n== C9  Theorem 1(d) step 3: perturbing W along one column changes T outside that column")
n, nb, kk = 6, 2, 6
A = rng.normal(size=(kk, n)); R = rng.normal(size=(n, n)) * .5; W = rng.normal(size=(nb, n)) * .5; CB = np.eye(n)[:nb]
args = (CB, np.eye(kk), .1*np.eye(kk), np.eye(n), np.eye(nb), .1*np.eye(nb), .1*np.eye(nb), 0.01, 0.5)
T1 = transfer(A, build(A, R, W, *args), np.eye(kk))
u = np.linalg.pinv(A)[:, 2]               # reads partner channel c2 = 2
W2 = W + 2.0 * np.outer(np.eye(nb)[0], u)
T2 = transfer(A, build(A, R, W2, *args), np.eye(kk))
dT = T2 - T1
print("   |dT| column 2 max:", np.abs(dT[:, 2]).max().round(4), "  |dT| other columns max:", np.abs(np.delete(dT, 2, 1)).max().round(4))
print("   (c1,c1)=(0,0) entry before/after:", T1[0,0].round(4), T2[0,0].round(4))

print("\n== C10 Monodromy spectrum under the design's own gauge group G (A with a kernel)")
n, nb, kk = 8, 2, 4
A = rng.normal(size=(kk, n)); CB = np.eye(n)[:nb]
N_ = np.linalg.svd(np.vstack([A, CB]))[2][kk+nb:].T   # basis of ker A ∩ ker CB
uvec = N_[:, 0]; v = rng.normal(size=n)
gs = np.eye(n) + np.outer(uvec, v); gsi = np.linalg.inv(gs)
print("   A gs^-1 = A:", np.allclose(A @ gsi, A), "  CB gs^-1 = CB:", np.allclose(CB @ gsi, CB))
R = rng.normal(size=(n, n)); W = rng.normal(size=(nb, n))
MB = W @ R @ CB.T; MBg = W @ (R @ gsi) @ CB.T
print("   spec M_B        :", np.sort_complex(np.linalg.eigvals(MB)))
print("   spec M_B (gauged):", np.sort_complex(np.linalg.eigvals(MBg)))

print("\n== C11 Theorem 6(a) holds at R = R_true; fails when the model is wrong (crossed partner)")
n = 4; L_a = np.eye(n); K = np.eye(n); P = np.eye(n)
R = np.eye(n); Rtrue = np.diag([1, 1, -1, -1.])
PK = P @ np.linalg.inv(P + K) @ K
Hs = L_a + R.T @ PK @ R
for name, Rt in [("R_true=R", R), ("R_true crossed on 2 ch", Rtrue)]:
    Nm = R.T @ PK @ Rt
    print(f"   {name:<24} eig(Hs^-1 N) = {np.linalg.eigvals(np.linalg.solve(Hs, Nm)).real}")

print("\n== C12 Theorem 3(a): the h-route reaches m at order t^3, not t^4 (z_y is a static function of y)")
# states w=(z,x,h,m); input y feeds z (perception), m (reflex) and h (through z_y, as eq. (H) is written)
az, ax, eh, bm = 10., 1., 0.5, 16.
Acal = np.array([[-az, az*0.5, 0, 0], [ax*0.8, -ax, ax*0.6, 0], [0, eh*0.2, -eh, 0], [0, bm*1.0, 0, -bm]])
for label, Bh in [("as the design claims (no y->h)", 0.0), ("as eq. (H) is written (y->z_y->h)", eh*0.7)]:
    Bcal = np.array([az*1.0, 0, Bh, bm*0.3])
    c2 = (np.linalg.matrix_power(Acal, 2) @ Bcal)[3] / 6
    # contribution of the h-route alone at order t^3
    hroute = Acal[3, 1] * Acal[1, 2] * Bcal[2] / 6
    print(f"   {label:<36} t^3 coefficient of m = {c2:.3f}, of which h-route = {hroute:.3f}")

print("\n== C13 Theorem 5: contingency learning in closed loop with a partner who ignores the agent")
def run(Wgain, lagged, T=200000, dt=1/30, seed=1):
    rg = np.random.default_rng(seed)
    z = 0.0; x = 0.0; xt = 0.0; R = 0.0; tau = 1.2; buf = [0.0]*36
    eta = 2e-3
    for t in range(T):
        z += dt * (-0.5 * z) + np.sqrt(dt) * rg.normal()          # partner: autonomous OU, no response to agent
        # agent fast state: relaxes to the energy minimum target (rho edge with R, kappa edge with W, anchor)
        p, lam, g0 = 1.0, 1.0, 0.5
        target = (p*R*z + lam*Wgain*z) / (p*R*R + lam + g0 + (p*R*R+lam))
        x += dt * 3.0 * (target - x) + 0.05 * np.sqrt(dt) * rg.normal()
        buf.append(x); xl = buf.pop(0)
        xt += dt / tau * ((xl if lagged else x) - xt)
        R += eta * (z - R * xt) * xt
    return R
print("   partner never responds to the agent; true contingency R = 0")
print("   W=0.0 (no consequence link)          learned R =", round(run(0.0, False), 3))
print("   W=0.5 (partner predicts my body)      learned R =", round(run(0.5, False), 3))
print("   W=0.5, trace of x lagged by 1.2 s     learned R =", round(run(0.5, True), 3))
