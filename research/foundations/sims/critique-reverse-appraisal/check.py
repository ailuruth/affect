"""Critic's algebra checks for design-reverse-appraisal.md (K1-K11).
They run the design's own local linear-Gaussian equations on hand-set instances.
They are algebra checks and counterexamples, not evidence about behaviour or people.
Run from sims/:  uv run python critique-reverse-appraisal/check.py"""
import numpy as np
np.set_printoptions(precision=4, suppress=True)

def blk(*Ms):
    n = sum(M.shape[0] for M in Ms); out = np.zeros((n, n)); i = 0
    for M in Ms:
        k = M.shape[0]; out[i:i+k, i:i+k] = M; i += k
    return out

def model(n=3, k=8, lamA=None, lamP=None, rho=None, rhoP=None, C=None, sA=1.0, sP=1.0,
          v=1.0, w=0.5, vh=1.0, wh=0.5, psi=0.0, rA=0.5, rg=0.5, zeta=1.0, JP=None, JA=None,
          ineq=None, seed=0):
    """s = (oA(n), oP(n), g, gt, h, ht); alpha = (u(n), agency, world) as in the design's check.py.
    ineq: None (iota = 0) or (cs_A, co_A, cs_P, co_P) per-concern regime coefficients of the
    piecewise-linear appraisal (own coefficient, other coefficient) for agent and partner."""
    r = np.random.default_rng(seed)
    lamA = np.ones(n) if lamA is None else np.asarray(lamA, float)
    lamP = np.ones(n) if lamP is None else np.asarray(lamP, float)
    rho = np.zeros(n) if rho is None else np.asarray(rho, float)
    rhoP = np.zeros(n) if rhoP is None else np.asarray(rhoP, float)
    C = np.zeros((n, n)) if C is None else C
    m = 2*n + 4
    So = np.block([[sA*np.eye(n), C], [C.T, sP*np.eye(n)]])
    Sg = np.array([[v, v], [v, v + w]]); Sh = np.array([[vh, vh], [vh, vh + wh]])
    Sigma = blk(So, Sg, Sh)
    iA = np.arange(n); iP = np.arange(n, 2*n); ig, igt, ih, iht = 2*n, 2*n+1, 2*n+2, 2*n+3
    d = n + 2
    if ineq is None:
        csA, coA, csP, coP = np.ones(n), rho, np.ones(n), rhoP
    else:
        csA, coA, csP, coP = ineq
    AP = np.zeros((d, m)); AP[:n, iP] = -np.diag(csP*lamP); AP[:n, iA] = -np.diag(coP*lamA)
    AP[n, igt] = -1.0; AP[n+1, iht] = 1.0
    AA = np.zeros((d, m)); AA[:n, iA] = -np.diag(csA*lamA); AA[:n, iP] = -np.diag(coA*lamP)
    AA[n, ig] = 1.0; AA[n+1, ih] = 1.0
    Phi = np.zeros((d, d)); Phi[n, n] = psi
    AA = AA + Phi @ AP
    JP = r.normal(size=(k, d)) if JP is None else JP
    JA = JP if JA is None else JA
    R = np.diag(r.uniform(0.5, 2.0, size=k)) / zeta
    Hz = np.zeros((n+1, m)); Hz[:n, iA] = np.eye(n); Hz[n, ig] = 1.0
    Rz = np.diag(np.r_[rA*np.ones(n), rg])
    return dict(n=n, d=d, Sigma=Sigma, AP=AP, AA=AA, JP=JP, JA=JA, R=R, Hz=Hz, Rz=Rz)

def gamma(M):
    Q = np.linalg.inv(M['Sigma']) + M['Hz'].T @ np.linalg.inv(M['Rz']) @ M['Hz']
    Sz = np.linalg.inv(Q)
    V = M['AP'] @ Sz @ M['AP'].T
    B = M['AA'] @ Sz @ M['AP'].T @ np.linalg.pinv(V)
    Ka = V @ M['JP'].T @ np.linalg.inv(M['JP'] @ V @ M['JP'].T + M['R'])
    return M['JA'] @ B @ Ka, B, V

def defect(G, M, tol=1e-9):
    """relative copy defect min_c ||G|_E - c I|| / ||G|_E|| in the R^{-1/2} metric, E = im(J_P) (true rank)."""
    W = np.diag(1/np.sqrt(np.diag(M['R'])))
    U, s, _ = np.linalg.svd(W @ M['JP'], full_matrices=False)
    U = U[:, s > tol*s.max()]
    GE = U.T @ (W @ G @ np.linalg.inv(W)) @ U
    cs = np.linspace(-4, 4, 3201)
    vals = [np.linalg.norm(GE - c*np.eye(GE.shape[0]), 2) for c in cs]
    i = int(np.argmin(vals)); nrm = np.linalg.norm(GE, 2)
    return vals[i]/max(nrm, 1e-15), cs[i], nrm, U.shape[1]

n = 3
print("K1  rank of the partner-appraisal map for the design's full alpha = (u, pi, g, h, kappa)")
# pi = u - E_pre[u] (E_pre fixed before the event), kappa constant within an event
M = model(n=n)
AP_full = np.vstack([M['AP'][:n], M['AP'][:n], M['AP'][n:], np.zeros((1, M['AP'].shape[1]))])
print(f"    d_alpha = {AP_full.shape[0]}, rank A_P = {np.linalg.matrix_rank(AP_full)}  -> V_alpha singular; "
      f"(n=8 in the design: d_alpha = 19, rank = 10)")

print("K2  private block with the design's innate inequity weights iota = 0.3 (T1g claims |B| = |rho| <= 0.6 < 1)")
io = 0.3
for rho_, regime in [(-0.6, 'agent behind'), (0.6, 'agent behind'), (0.6, 'agent ahead'), (-0.6, 'agent ahead')]:
    if regime == 'agent behind':   # agent: w_o > w_s ; partner ahead
        cs, co, csP, coP = 1+io, rho_-io, 1-io, 0.0+io
    else:
        cs, co, csP, coP = 1-io, rho_+io, 1+io, 0.0-io
    M = model(n=n, rho=rho_*np.ones(n), C=np.zeros((n, n)), rA=1e-9,
              ineq=(cs*np.ones(n), co*np.ones(n), csP*np.ones(n), coP*np.ones(n)))
    _, B, _ = gamma(M)
    print(f"    rho = {rho_:+.1f}, {regime:12s}: B_uu diag = {np.diag(B[:n, :n])}  closed form {co/csP:+.3f}")

print("K3  T1g second term: own outcome not yet realised (the design gives it zero precision), outcomes private (C = 0),")
print("    rho = 0, partner regard rho_P = 0.5 on every concern. Sweep the agent's uniform need scale gamma (listed as NOT a dial).")
JP0 = np.random.default_rng(3).normal(size=(8, n+2)); JP0g = JP0.copy(); JP0g[:, n:] = 0.0   # G0: no agency/world columns
for label, JP in [("G0-like J (agency, world not expressible)", JP0g), ("full-rank J", JP0)]:
    print(f"    {label}:")
    for gam in [0.0, 0.3, 1, 3, 10, 30]:
        M = model(n=n, lamA=gam*np.ones(n), rhoP=0.5*np.ones(n), C=np.zeros((n, n)), rA=1e9, rg=0.5,
                  JP=JP, zeta=1e3, psi=0.0)
        G, B, _ = gamma(M); dfc, c, nrm, rk = defect(G, M)
        print(f"      gamma={gam:5.1f}: B_uu diag {np.diag(B[:n,:n])}, ||Gamma_E|| {nrm:.3f}, rel. copy defect {dfc:.3f} at c={c:.2f} (dim E={rk})")

print("K3b same regime, sweep the partner's own stake s_P (how much the event is about her) at gamma = 1")
for sP in [10, 1, 0.1, 0.01, 0.001]:
    M = model(n=n, rhoP=0.5*np.ones(n), sP=sP, C=np.zeros((n, n)), rA=1e9, JP=JP0g, zeta=1e3)
    G, B, _ = gamma(M); dfc, c, nrm, rk = defect(G, M)
    print(f"      s_P={sP:6.3f}: B_uu {B[0,0]:.3f}, rel. copy defect {dfc:.3f} at c={c:.2f}")

print("K4  R2: uniform regard r*1 with own outcome known, C ~ 0: scaled copy on the conduciveness subspace (c = r > 0)")
for r_ in [0.0, 0.2, 0.4, 0.6]:
    M = model(n=n, rho=r_*np.ones(n), C=0.02*np.eye(n), rA=1e-6, JP=JP0g, zeta=1e3)
    G, B, _ = gamma(M); dfc, c, nrm, rk = defect(G, M)
    print(f"      r={r_:.1f}: ||Gamma_E|| {nrm:.3f}, rel. copy defect {dfc:.3f} at c={c:.2f}")

print("K5  T1f near-degenerate sharing: B_uu stays near c/s_P until r_A << s_A(1 - corr^2)")
for corr in [0.8, 0.99]:
    out = []
    for rA in [10, 1, 0.1, 0.01, 0.001]:
        out.append(corr*rA/(1 + rA - corr**2))
    print(f"      corr={corr}: B at r_A=10..0.001: {np.round(out, 3)}")

print("K6  T4(a) scope: a kernel perturbation of J_P^T R^-1 generally has a component on the reflex synergies S0")
M = model(n=n, rho=np.array([.3, -.2, .1]), psi=0.4, seed=11)
Mx = M['JP'].T @ np.linalg.inv(M['R']); _, _, Vt = np.linalg.svd(Mx); kern = Vt[Mx.shape[0]:].T
S0 = [0, 1]   # say channel 0 = smile synergy, channel 1 = brow-lowering
print(f"    max |S0 component| over unit kernel basis vectors = {np.abs(kern[S0]).max():.3f}; "
      f"a step of that vector fires the reflex (peak lambda0*a) and the onset/event detector")

print("K7  T1(i) 'DC gain 0': rectified derivative of a constant but noisy smile (30 Hz, heteroscedastic jitter)")
rng = np.random.default_rng(0); fs = 30.0; dt = 1/fs; T = 600.0; t = np.arange(0, T, dt)
lam0, taur = 0.15, 0.5
for level in [0.0, 0.3, 0.7]:
    sd = 0.01 + 0.03*level                           # jitter grows with activation
    y = level + sd*rng.standard_normal(len(t))
    dy = np.r_[0, np.diff(y)]/dt
    m = np.zeros_like(t)
    for i in range(1, len(t)):
        m[i] = m[i-1] + dt*(-m[i-1]/taur + lam0*max(dy[i], 0))
    print(f"    steady smile level {level:.1f}: mean reflex {m[300:].mean():.4f}  (step-onset peak lam0*a = {lam0*level:.3f})")

print("K8  AR(1) frame noise: the design's per-frame update treats frames as independent")
for phi in [0.5, 0.8, 0.9, 0.95]:
    print(f"    phi={phi}: over-counted information factor (1+phi)/(1-phi) = {(1+phi)/(1-phi):.1f};"
          f"  t_1/2 of the filter as written is shorter than T3(b)'s by this factor")

print("K9  T2(d): at the agent's satiety (lambda_A = 0), u = rho*w_o - iota terms != 0")
lamA = 0.0; lamP = 1.0; oP = -1.0; rho_ = 0.4
w_s = -lamA*0.0; w_o = -lamP*oP
u = w_s + rho_*w_o - io*max(w_o - w_s, 0) - io*max(w_s - w_o, 0)
print(f"    partner gained (o_P = -1 in drive units): u = {u:+.2f} (T2d claims 0)")

print("K10 learning path: G0 gives one smile axis; a partner whose smile tracks the agent's overall fortune")
print("    teaches a uniform rho_P under the design's conjugate Gaussian update (exchangeable prior)")
rng = np.random.default_rng(1); N = 400; lam = np.ones(n); wsm = np.ones(n)    # G0: every u_j loads the smile equally
kappa_true = 0.5
oA = rng.normal(size=(N, n)); oP = rng.normal(size=(N, n))
smile = -(wsm*lam*oP).sum(1) - kappa_true*(lam*oA).sum(1) + 0.5*rng.normal(size=N)   # her face, read on the G0 axis
X = -(wsm*lam)[None, :]*oA                       # regressors for rho_P,j
yv = smile + (wsm*lam*oP).sum(1)                 # her own-outcome part removed (posterior o_P taken as known)
P0 = 0.25*np.eye(n); m0 = np.zeros(n)
Pn = np.linalg.inv(np.linalg.inv(P0) + X.T @ X/0.25); mn = Pn @ (np.linalg.inv(P0) @ m0 + X.T @ yv/0.25)
print(f"    posterior mean rho_P = {mn}  (uniform; then K3 gives B_uu -> (1/rho_P) I = {1/mn.mean():.2f} I)")

print("K11 dial definition: exact membership vs approximate. Face-precision sweep on the C7 co-appraisal point")
print("    reaches the cone only as zeta -> inf; relative defect at zeta = 1e2, 1e3, 1e4:")
n3 = 3; JPc = np.random.default_rng(7).normal(size=(8, n3+2))
for z in [1e2, 1e3, 1e4]:
    M = model(n=n3, C=0.999*np.eye(n3), rA=1e6, rg=1e6, w=1e-6, wh=1e-6, psi=2.0, JP=JPc, zeta=z, seed=7)
    G, _, _ = gamma(M); print(f"      zeta={z:.0e}: defect {defect(G, M)[0]:.4f}")

print("K3c in the K3 regime (gamma = 10, G0-like J), face precision zeta becomes a flat-to-copy dial")
for z in [1e-3, 1e-2, 1e-1, 1, 10, 1e2, 1e3]:
    M = model(n=n, lamA=10*np.ones(n), rhoP=0.5*np.ones(n), C=np.zeros((n, n)), rA=1e9, JP=JP0g, zeta=z)
    G, B, _ = gamma(M); dfc, c, nrm, rk = defect(G, M)
    print(f"      zeta={z:7.3f}: ||Gamma_E|| {nrm:.3f}, rel. copy defect {dfc:.3f} at c={c:.2f}")

print("K3d same regime (gamma = 10, G0-like J, zeta = 100): own-evidence noise r_A (listed as NOT a dial) runs flat -> copy")
for rA in [1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 1e3]:
    M = model(n=n, lamA=10*np.ones(n), rhoP=0.5*np.ones(n), C=np.zeros((n, n)), rA=rA, JP=JP0g, zeta=100)
    G, B, _ = gamma(M); dfc, c, nrm, rk = defect(G, M)
    print(f"      r_A={rA:8.4f}: B_uu {B[0,0]:.3f}, ||Gamma_E|| {nrm:.3f}, rel. copy defect {dfc:.3f} at c={c:.2f}")
