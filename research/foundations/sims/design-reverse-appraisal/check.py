"""Algebra checks for design-reverse-appraisal.md (C1-C8).
These check the design's own equations on random local instances. They are not evidence
about behaviour or people. Run from sims/:  uv run python design-reverse-appraisal/check.py"""
import numpy as np
np.set_printoptions(precision=4, suppress=True)
rng = np.random.default_rng(0)

def blk(*Ms):
    n = sum(M.shape[0] for M in Ms); out = np.zeros((n, n)); i = 0
    for M in Ms:
        k = M.shape[0]; out[i:i+k, i:i+k] = M; i += k
    return out

def instance(n=3, k=8, rho=None, rhoP=None, C=None, v=1.0, w=0.5, vh=1.0, wh=0.5,
             psi=0.0, lamA=None, lamP=None, rA=0.5, rg=0.5, zeta=1.0, seed=None, JP=None, JA=None):
    r = np.random.default_rng(seed)
    lamA = np.ones(n) if lamA is None else lamA
    lamP = np.ones(n) if lamP is None else lamP
    rho = np.zeros(n) if rho is None else rho
    rhoP = np.zeros(n) if rhoP is None else rhoP
    SA = np.eye(n); SP = np.eye(n)
    C = 0.3 * np.eye(n) if C is None else C
    m = 2 * n + 4                       # s = (oA, oP, g, h, gt, ht)
    So = np.block([[SA, C], [C.T, SP]])
    Sg = np.array([[v, v], [v, v + w]]); Sh = np.array([[vh, vh], [vh, vh + wh]])
    # order: oA(n), oP(n), g, gt, h, ht
    Sigma = blk(So, Sg, Sh)
    iA = np.arange(n); iP = np.arange(n, 2*n); ig, igt, ih, iht = 2*n, 2*n+1, 2*n+2, 2*n+3
    d = n + 2
    # partner appraisal alpha_P = (uP, aP, hP)
    AP = np.zeros((d, m))
    AP[:n, iP] = -np.diag(lamP); AP[:n, iA] = -np.diag(rhoP * lamA)
    AP[n, igt] = -1.0           # agency in partner frame: swap negates
    AP[n+1, iht] = 1.0
    # agent appraisal alpha_A = (uA, gA, hA) + consequence Phi alpha_P
    AA = np.zeros((d, m))
    AA[:n, iA] = -np.diag(lamA); AA[:n, iP] = -np.diag(rho * lamP)
    AA[n, ig] = 1.0; AA[n+1, ih] = 1.0
    Phi = np.zeros((d, d)); Phi[n, n] = psi      # g_A += psi * a_P
    AAt = AA + Phi @ AP
    JP = r.normal(size=(k, d)) if JP is None else JP
    JA = JP + 0.2 * r.normal(size=(k, d)) if JA is None else JA
    R = np.diag(r.uniform(0.5, 2.0, size=k)) / zeta
    # other evidence: own interoception on oA, own causal record on g
    Hz = np.zeros((n + 1, m)); Hz[:n, iA] = np.eye(n); Hz[n, ig] = 1.0
    Rz = np.diag(np.r_[rA * np.ones(n), rg])
    return dict(n=n, k=k, d=d, m=m, Sigma=Sigma, AP=AP, AAt=AAt, JP=JP, JA=JA, R=R, Hz=Hz, Rz=Rz,
                v=v, w=w, rg=rg, psi=psi)

def gamma_direct(I):
    H = I['JP'] @ I['AP']
    Q = np.linalg.inv(I['Sigma']) + I['Hz'].T @ np.linalg.inv(I['Rz']) @ I['Hz']
    Spost = np.linalg.inv(Q + H.T @ np.linalg.inv(I['R']) @ H)
    L = Spost @ H.T @ np.linalg.inv(I['R'])
    return I['JA'] @ I['AAt'] @ L, H @ L, L

def gamma_factored(I):
    # condition on z first (posterior before the face), then regress alpha_A on alpha_P
    Q = np.linalg.inv(I['Sigma']) + I['Hz'].T @ np.linalg.inv(I['Rz']) @ I['Hz']
    Sz = np.linalg.inv(Q)
    VP = I['AP'] @ Sz @ I['AP'].T
    CAP = I['AAt'] @ Sz @ I['AP'].T
    B = CAP @ np.linalg.inv(VP)
    Ka = VP @ I['JP'].T @ np.linalg.inv(I['JP'] @ VP @ I['JP'].T + I['R'])
    return I['JA'] @ B @ Ka, B, Ka

def copy_defect(G, I):
    """min_c ||P_E (G - c I) P_E|| in the R^{-1/2}-whitened metric, relative to ||P_E G P_E||, E = im JP."""
    W = np.diag(1/np.sqrt(np.diag(I['R'])))
    Gw = W @ G @ np.linalg.inv(W)
    U, _ = np.linalg.qr(W @ I['JP'])
    GE = U.T @ Gw @ U
    cs = np.linspace(-3, 3, 1201)
    vals = [np.linalg.norm(GE - c*np.eye(GE.shape[0]), 2) for c in cs]
    i = int(np.argmin(vals)); nrm = np.linalg.norm(GE, 2)
    return vals[i] / max(nrm, 1e-12), cs[i], nrm

print("C1  hat-matrix spectrum: eig(R^-1/2 Pi R^1/2) in [0,1), falls with other evidence")
worst = 0; mono_ok = True
for s in range(200):
    I = instance(seed=s, zeta=10**rng.uniform(-2, 3))
    _, Pi, _ = gamma_direct(I)
    W = np.diag(1/np.sqrt(np.diag(I['R'])))
    ev = np.linalg.eigvals(W @ Pi @ np.linalg.inv(W)).real
    worst = max(worst, ev.max())
    I2 = dict(I); I2['Rz'] = I['Rz'] * 0.1      # 10x more precise own evidence
    _, Pi2, _ = gamma_direct(I2)
    S1 = W @ Pi @ np.linalg.inv(W); S2 = W @ Pi2 @ np.linalg.inv(W)
    if np.linalg.eigvalsh((S1 + S1.T)/2 - (S2 + S2.T)/2).min() < -1e-9: mono_ok = False
    assert ev.min() > -1e-9
print(f"    max eigenvalue over 200 instances = {worst:.6f} (<1);  Loewner-monotone in own evidence: {mono_ok}")

print("C2  factorization Gamma = J_A B K_alpha equals the direct posterior formula")
err = 0
for s in range(200):
    I = instance(seed=s, rho=rng.uniform(-0.5, 0.5, 3), rhoP=rng.uniform(-0.5, 0.5, 3), psi=rng.uniform(-1, 1),
                 C=rng.uniform(-0.6, 0.6)*np.eye(3), zeta=10**rng.uniform(-1, 2))
    Gd, _, _ = gamma_direct(I); Gf, _, _ = gamma_factored(I)
    err = max(err, np.abs(Gd - Gf).max())
print(f"    max |difference| = {err:.2e}")

print("C3  agency block: B[g_A, a_P] = psi - kappa1, kappa1 = 1/(1 + w(1/v + 1/r_g))")
err = 0
for s in range(200):
    v, w, rg, psi = rng.uniform(0.2, 2), rng.uniform(0.05, 3), rng.uniform(0.05, 3), rng.uniform(-1, 1)
    I = instance(seed=s, v=v, w=w, rg=rg, psi=psi, rho=rng.uniform(-.5, .5, 3), C=0.4*np.eye(3))
    _, B, _ = gamma_factored(I)
    n = I['n']; kap = 1/(1 + w*(1/v + 1/rg))
    err = max(err, abs(B[n, n] - (psi - kap)), np.abs(B[n, :n]).max(), np.abs(B[:n, n]).max())
print(f"    max error (incl. zero cross-terms to the outcome block) = {err:.2e}")

print("C4  private-outcome block (C = 0): B_uu = diag(rho * lamP / lamP) = diag(rho); |entries| <= rho_bar")
I = instance(seed=1, rho=np.array([0.4, -0.3, 0.0]), C=np.zeros((3, 3)), rA=1e-6)
_, B, _ = gamma_factored(I); print("    B_uu diag =", np.diag(B[:3, :3]), " (rho = [0.4,-0.3,0])")

print("C5  shared block shrinks monotonically as own interoceptive precision rises (social referencing guard)")
vals = []
for rA in [10, 3, 1, 0.3, 0.1, 0.03, 0.01, 0.001]:
    I = instance(seed=2, C=0.8*np.eye(3), rA=rA)
    _, B, _ = gamma_factored(I); vals.append(B[0, 0])
print("    B_u1u1 for r_A = 10 .. 0.001:", np.round(vals, 4), " monotone:", all(np.diff(vals) <= 1e-12))
# closed form, scalar (sA = sP = 1, lam = 1, rho = rhoP = 0): B = c*rA/(1 + rA - c^2)
print("    closed form c*rA/(1+rA-c^2):", np.round([0.8*r/(1+r-0.64) for r in [10, 3, 1, .3, .1, .03, .01, .001]], 4))

print("C6  dial sweeps on random instances: relative copy defect along each scalar sweep")
def sweep(make, grid):
    return min(copy_defect(gamma_direct(make(x))[0], make(x))[0] for x in grid)
mins = {k: [] for k in ['face precision', 'drive scale', 'uniform rho', 'sharing scale', 'psi']}
for s in range(40):
    r = np.random.default_rng(100 + s)
    base = dict(seed=s, rho=r.uniform(-.4, .4, 3), rhoP=r.uniform(-.4, .4, 3), C=np.diag(r.uniform(-.6, .8, 3)),
                psi=r.uniform(-.5, .5), w=r.uniform(.2, 2), rA=r.uniform(.2, 2), rg=r.uniform(.2, 2))
    mins['face precision'].append(sweep(lambda x: instance(**{**base, 'zeta': x}), np.logspace(-2, 4, 25)))
    mins['drive scale'].append(sweep(lambda x: instance(**{**base, 'lamA': x*np.ones(3)}), np.logspace(-2, 2, 25)))
    mins['uniform rho'].append(sweep(lambda x: instance(**{**base, 'rho': x*np.ones(3)}), np.linspace(-.9, .9, 25)))
    mins['sharing scale'].append(sweep(lambda x: instance(**{**base, 'C': x*np.eye(3)}), np.linspace(-.95, .95, 25)))
    mins['psi'].append(sweep(lambda x: instance(**{**base, 'psi': x}), np.linspace(-3, 3, 25)))
for k_, v_ in mins.items():
    print(f"    {k_:15s}: min over sweep, worst instance = {min(v_):.3f}; median = {np.median(v_):.3f}")

print("C7  constructed co-appraisal instance (B = I on E): face precision alone then reaches copy")
n = 3; JP = np.random.default_rng(7).normal(size=(8, n+2))
I = instance(seed=7, JP=JP, JA=JP, rho=np.zeros(3), rhoP=np.zeros(3), C=0.999*np.eye(3), rA=1e6, rg=1e6,
             w=1e-6, wh=1e-6, psi=2.0, zeta=1e4)
G, _, _ = gamma_direct(I); print('    with every condition met:', np.round(copy_defect(G, I)[:2], 4))
I = instance(seed=7, JP=JP, JA=JP, rho=np.zeros(3), rhoP=np.zeros(3), C=0.999*np.eye(3), rA=1e6, rg=1e6,
             w=1e-6, wh=0.5, psi=2.0, zeta=1e4)
# psi - kappa1 with w->0, rg large: kappa1 -> 1, so B_gg = psi - 1 = 1
G, _, _ = gamma_direct(I); dfc = copy_defect(G, I)
print(f"    relative copy defect = {dfc[0]:.4f} at c = {dfc[1]:.2f}  (same, but partner's world-attribution belief noisy, w_h = 0.5)")

print("C8  reflex: DC transfer zero; rectified onset reflex leaves residue lambda0*tau_r*nu*a in a slow integrator")
dt = 0.01; T = 600.0; t = np.arange(0, T, dt)
lam0, taur, lr, Tz, gfb = 0.15, 0.5, 0.3, 20.0, 1.0
def run(yP):
    dy = np.gradient(yP, dt); dy = np.r_[np.zeros(int(lr/dt)), dy[:-int(lr/dt)]]
    m = np.zeros_like(t); z = np.zeros_like(t)
    for i in range(1, len(t)):
        m[i] = m[i-1] + dt*(-m[i-1]/taur + lam0*max(dy[i], 0))
        z[i] = z[i-1] + dt*(-z[i-1]/Tz + gfb*m[i]/Tz)
    return m, z
step = (t > 10).astype(float)
m, z = run(step)
print(f"    step: peak reflex {m.max():.3f} (lam0*a = {lam0:.3f}), reflex at t=60 s: {m[int(60/dt)]:.2e}")
nu, a, width = 0.2, 1.0, 2.0
pulses = (((t % (1/nu)) < width) & (t > 5)).astype(float) * a
m, z = run(pulses)
print(f"    pulse train nu={nu}/s: mean reflex {m[int(100/dt):].mean():.4f} vs lam0*tau_r*nu*a = {lam0*taur*nu*a:.4f};"
      f" mean residue in z {z[int(100/dt):].mean():.4f} vs gfb*lam0*tau_r*nu*a = {gfb*lam0*taur*nu*a:.4f}")

print("C9  context latency: Kalman-Bucy weight on the face reaches 1/2 at t = P0/I")
P0, Irate = 2.0, 0.8
tt = np.linspace(0, 10, 1001); wgt = Irate*tt/(P0 + Irate*tt)
print(f"    t_half numeric = {tt[np.argmin(abs(wgt-0.5))]:.2f} s, P0/I = {P0/Irate:.2f} s")

print("C10 randomized-response estimand Q_d = Cov(z_t, b_{t-d})/Var(b), with pre-treatment partner controls; 20 seeds")
def closed_loop(Rtrue, T=18000, a=0.95, f=0.8, d=3, sb=0.3, seed=0):
    r = np.random.default_rng(seed); z = np.zeros(T); x = np.zeros(T); h = np.zeros(T)
    b = sb*r.standard_normal(T); e = 0.3*r.standard_normal(T)
    for t_ in range(1, T):
        h[t_] = 0.98*h[t_-1] + 0.2*r.standard_normal()
        z[t_] = a*z[t_-1] + (Rtrue*x[t_-d] if t_ >= d else 0) + 0.3*h[t_] + e[t_]
        x[t_] = f*max(z[t_-1], 0) + 0.5*h[t_] + b[t_]          # rectified, reflex-like following
    return z + 0.5*r.standard_normal(T), x, b
def Qhat(zo, b, d, k=5):
    t_ = np.arange(d + k + 1, len(zo))
    X = np.column_stack([np.ones(len(t_)), b[t_-d]] + [zo[t_-d-j] for j in range(1, k+1)])
    return np.linalg.lstsq(X, zo[t_], rcond=None)[0][1]
for Rtrue, a, f in [(0.0, 0.95, 0.8), (0.3, 0.6, 0.5)]:
    Qs = []; naive = []
    for sd in range(20):
        zo, x, b = closed_loop(Rtrue, a=a, f=f, seed=sd)
        Qs.append([Qhat(zo, b, d) for d in (1, 2, 3, 4, 5)])
        naive.append(np.cov(zo[3:], x[:-3])[0, 1]/np.var(x))
    Qs = np.array(Qs)
    print(f"    R={Rtrue} (a={a}, f={f}): Q_1..5 mean {np.round(Qs.mean(0), 3)} sd {np.round(Qs.std(0), 3)};"
          f" naive lag-3 regression {np.mean(naive):.3f}")

print("C11 T4 image constraint: a partner-face perturbation in ker(J_P^T R^-1) moves no belief and no response")
I = instance(seed=11, rho=np.array([.3, -.2, .1]), psi=0.4)
Gd, _, L = gamma_direct(I)
Rinv = np.linalg.inv(I['R']); M = I['JP'].T @ Rinv
_, _, Vt = np.linalg.svd(M); kern = Vt[M.shape[0]:].T          # basis of ker(J_P^T R^-1)
print(f"    dim ker = {kern.shape[1]};  max |L @ kern| = {np.abs(L @ kern).max():.2e};  max |Gamma @ kern| = {np.abs(Gd @ kern).max():.2e}")

print("C12 Gamma_E similar to B * Pi_tilde (Pi_tilde = (V^-1 + F)^-1 F) when J_A = J_P = J")
err = 0
for s in range(100):
    r = np.random.default_rng(500 + s); JP = r.normal(size=(8, 5))
    I = instance(seed=s, JP=JP, JA=JP, rho=r.uniform(-.5, .5, 3), C=np.diag(r.uniform(-.6, .6, 3)), psi=r.uniform(-1, 1))
    G, B, Ka = gamma_factored(I)
    Q = np.linalg.inv(I['Sigma']) + I['Hz'].T @ np.linalg.inv(I['Rz']) @ I['Hz']; V = I['AP'] @ np.linalg.inv(Q) @ I['AP'].T
    F = JP.T @ np.linalg.inv(I['R']) @ JP; Pt = np.linalg.inv(np.linalg.inv(V) + F) @ F
    err = max(err, np.abs(np.linalg.pinv(JP) @ G @ JP - B @ Pt).max())
    assert np.abs(np.linalg.eigvals(Pt)).max() < 1
print(f"    max |J^+ Gamma J - B Pi_tilde| = {err:.2e}; eig(Pi_tilde) in [0,1): checked")
