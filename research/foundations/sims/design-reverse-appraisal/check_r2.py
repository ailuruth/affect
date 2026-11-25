"""Algebra checks for revision 2 of design-reverse-appraisal.md (D1-D9).
They run the revised local linear-Gaussian equations on random and hand-set instances.
They check the document's own algebra. They are not evidence about behaviour or people.
Run from sims/:  uv run python design-reverse-appraisal/check_r2.py"""
import numpy as np
np.set_printoptions(precision=4, suppress=True)


def build(n=3, k=16, lamA=None, lamP=None, conc=None, v=1.0, w=0.5, a_g=1.0, psi=0.0, vq=0.2,
          vh=1.0, wh=0.5, a_h=1.0, rg=0.5, rf=1.0, rdelta=0.05, reps=0.0, JP=None, JA=None, seed=0):
    """Revised object. s = (oA, oP, fA, fP, g, gt, q, h, ht), per-concern 4x4 blocks conc[j].
    alpha = (l, w, agency, world) for each person; l_A is felt (observed exactly)."""
    r = np.random.default_rng(seed)
    lamA = np.ones(n) if lamA is None else np.asarray(lamA, float)
    lamP = np.ones(n) if lamP is None else np.asarray(lamP, float)
    if conc is None:
        conc = []
        for _ in range(n):
            Mx = r.normal(size=(4, 4)); conc.append(Mx @ Mx.T / 4 + 0.05*np.eye(4))
    m = 4*n + 5
    iA, iP, ifA, ifP = (np.arange(n) + b*n for b in range(4))
    ig, igt, iq, ih, iht = 4*n, 4*n+1, 4*n+2, 4*n+3, 4*n+4
    S = np.zeros((m, m))
    for j in range(n):
        idx = [iA[j], iP[j], ifA[j], ifP[j]]
        S[np.ix_(idx, idx)] = conc[j]
    # attribution block: gt = a_g g + eta (w);  q = psi * gt + eta_q (vq)
    Vgt = a_g**2*v + w
    Satt = np.array([[v, a_g*v, psi*a_g*v],
                     [a_g*v, Vgt, psi*Vgt],
                     [psi*a_g*v, psi*Vgt, psi**2*Vgt + vq]])
    S[np.ix_([ig, igt, iq], [ig, igt, iq])] = Satt
    S[np.ix_([ih, iht], [ih, iht])] = np.array([[vh, a_h*vh], [a_h*vh, a_h**2*vh + wh]])
    d = 2*n + 2
    AA = np.zeros((d, m)); AP = np.zeros((d, m))
    AA[:n, iA] = -np.diag(lamA); AA[n:2*n, ifA] = -np.diag(lamA); AA[2*n, ig] = 1; AA[2*n, iq] = -1; AA[2*n+1, ih] = 1
    AP[:n, iP] = -np.diag(lamP); AP[n:2*n, ifP] = -np.diag(lamP); AP[2*n, igt] = -1; AP[2*n+1, iht] = 1
    # non-face evidence: felt o_A (exact), own causal record on g, own prospective evidence on f_A
    Hz = np.zeros((2*n + 1, m)); Hz[:n, iA] = np.eye(n); Hz[n:2*n, ifA] = np.eye(n); Hz[2*n, ig] = 1
    Rz = np.diag(np.r_[1e-10*np.ones(n), rf*np.ones(n), rg])
    # block-sparse expression map: channels 0..2 hedonic-exclusive (E0)
    def sparse_J(rr):
        J = np.zeros((k, d))
        J[0:7, :n] = rr.normal(size=(7, n))           # H family (liking): channels 0-6
        J[3:12, n:2*n] = rr.normal(size=(9, n))       # P family (prospective): channels 3-11
        J[8:k, 2*n:] = rr.normal(size=(k-8, 2))       # A family (attribution): channels 8-15
        return J * 0.2
    JP = sparse_J(r) if JP is None else JP
    if JA is None:
        JA = JP + (sparse_J(r) * 0.15)
    Rdelta = np.diag(rdelta * r.uniform(1.0, 2.0, size=k))
    Reff = Rdelta + reps*np.eye(k)
    return dict(n=n, k=k, d=d, S=S, AA=AA, AP=AP, Hz=Hz, Rz=Rz, JP=JP, JA=JA, R=Reff,
                v=v, w=w, a_g=a_g, psi=psi, rg=rg, rdelta_min=rdelta)


def post_nonface(M):
    Q = np.linalg.inv(M['S']) + M['Hz'].T @ np.linalg.inv(M['Rz']) @ M['Hz']
    return np.linalg.inv(Q)


def transfer(M):
    Se = post_nonface(M)
    VA = M['AA'] @ Se @ M['AA'].T; VP = M['AP'] @ Se @ M['AP'].T; CAP = M['AA'] @ Se @ M['AP'].T
    Vy = M['JP'] @ VP @ M['JP'].T + M['R']
    G = M['JA'] @ CAP @ M['JP'].T @ np.linalg.inv(Vy)
    return G, VA, VP, CAP


def whole_face_defect(G, M):
    """energy-weighted Frobenius copy defect, energy = covariance of her signal (after noise-whitening)."""
    _, _, VP, _ = transfer(M)
    W = np.diag(1/np.sqrt(np.diag(M['R'])))
    Gw = W @ G @ np.linalg.inv(W)
    Sig = W @ M['JP'] @ VP @ M['JP'].T @ W
    ev, U = np.linalg.eigh(Sig); Sh = U @ np.diag(np.sqrt(np.clip(ev, 0, None))) @ U.T
    c = np.trace(Gw @ Sig) / np.trace(Sig)
    num = np.linalg.norm((Gw - c*np.eye(len(Sig))) @ Sh); den = np.linalg.norm(Gw @ Sh)
    # E0 = orthogonal complement (whitened) of the span of my non-hedonic columns
    n = M['n']; B = W @ M['JA'][:, n:]
    Qb, _ = np.linalg.qr(B); P0 = np.eye(len(Sig)) - Qb @ Qb.T
    e0 = np.trace(P0 @ Sig); e = np.trace(Sig)
    return num/max(den, 1e-15), np.sqrt(e0/e), np.linalg.norm(P0 @ Gw)


print("D1  true rank of the partner appraisal map: rank A_P = 2m + 2, m = #{j: lamP_j != 0}")
for lamP in [np.ones(3), np.array([1., 0., 2.]), np.zeros(3)]:
    M = build(lamP=lamP, seed=1)
    print(f"    lamP = {lamP}: d_alpha = {M['AP'].shape[0]}, rank A_P = {np.linalg.matrix_rank(M['AP'])}, "
          f"2m+2 = {2*int((lamP != 0).sum()) + 2}")

print("D2  factorisation Gamma = J_A B K_alpha with B = C_AP V_P^+ (pseudo-inverse on the true range), 200 instances")
err = 0.0
for s in range(200):
    lamP = np.where(np.random.default_rng(s).uniform(size=3) < 0.2, 0.0, 1.0)
    M = build(lamP=lamP, seed=s, psi=0.5, a_g=0.7)
    G, VA, VP, CAP = transfer(M)
    B = CAP @ np.linalg.pinv(VP, rcond=1e-10)
    Ka = VP @ M['JP'].T @ np.linalg.inv(M['JP'] @ VP @ M['JP'].T + M['R'])
    err = max(err, np.abs(G - M['JA'] @ B @ Ka).max())
print(f"    max |Gamma - J_A B K_alpha| = {err:.1e}")

print("D3  felt outcomes carry no face transfer: B rows of l_A are 0, and P0 Gamma = 0 (hedonic-exclusive channels)")
mx_rows, mx_P0 = 0.0, 0.0
for s in range(200):
    M = build(seed=s, psi=0.3)
    G, VA, VP, CAP = transfer(M)
    mx_rows = max(mx_rows, np.abs(CAP[:M['n']]).max())
    mx_P0 = max(mx_P0, whole_face_defect(G, M)[2])
print(f"    max |Cov(l_A, alpha_P | E)| = {mx_rows:.1e};  max ||P0 Gamma|| = {mx_P0:.1e}")

print("D4  half-sd ceiling: ||row_e(Gamma) R^{1/2}|| <= 1/2 sd(y_A,e | E), random and adversarial instances")
worst = 0.0
rng = np.random.default_rng(5)
for s in range(400):
    scale = 10**rng.uniform(-3, 2)              # her stake scale (tiny to large)
    gam = 10**rng.uniform(-1, 2)                # agent need scale
    conc = []
    for _ in range(3):
        a = rng.normal(size=(4, 4)); C4 = a @ a.T/4 + 1e-3*np.eye(4)
        D = np.diag([1, np.sqrt(scale), 1, np.sqrt(scale)]); conc.append(D @ C4 @ D)
    M = build(seed=s, conc=conc, lamA=gam*np.ones(3), rf=10**rng.uniform(-3, 9),
              rdelta=10**rng.uniform(-4, 0), psi=rng.normal(), a_g=rng.normal())
    G, VA, VP, CAP = transfer(M)
    sdA = np.sqrt(np.diag(M['JA'] @ VA @ M['JA'].T))
    Rh = np.diag(np.sqrt(np.diag(M['R'])))
    rows = np.linalg.norm(G @ Rh, axis=1)
    ok = sdA > 1e-12
    worst = max(worst, (rows[ok] / sdA[ok]).max())
print(f"    max over 400 instances of ||row_e(Gamma) R^1/2|| / sd(y_A,e|E) = {worst:.4f}  (bound 0.5)")

print("D5  whole-face energy-weighted copy defect >= sqrt(e0/e), for every parameter value tried")
gap = np.inf; vals = []
for s in range(300):
    rr = np.random.default_rng(1000+s)
    M = build(seed=1000+s, lamA=10**rr.uniform(-1, 2)*np.ones(3), rf=10**rr.uniform(-3, 9),
              rdelta=10**rr.uniform(-4, 0), psi=rr.normal(), a_g=rr.normal())
    G, *_ = transfer(M)
    dfc, bound, _ = whole_face_defect(G, M)
    gap = min(gap, dfc - bound); vals.append((dfc, bound))
vals = np.array(vals)
print(f"    min(defect - bound) = {gap:.2e};  median defect {np.median(vals[:,0]):.3f}, median bound {np.median(vals[:,1]):.3f}")

print("D6  the critic's K3 regime in the revised object: private realised outcomes, no own prospective evidence,")
print("    her prospects tied to the agent's future (corr .99), her own stake small; sweep the agent's need gamma")
rd = 0.05
for gam in [0.1, 1, 3, 10, 30, 100]:
    conc = []
    for _ in range(3):
        sP = 0.01
        cf = 0.99*np.sqrt(1.0*sP)
        conc.append(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, cf], [0, 0, cf, sP]]) + 1e-6*np.eye(4))
    M = build(seed=3, conc=conc, lamA=gam*np.ones(3), lamP=np.ones(3), rf=1e9, rdelta=rd)
    G, VA, VP, CAP = transfer(M)
    B = CAP @ np.linalg.pinv(VP, rcond=1e-12)
    n = 3
    sdA = np.sqrt(np.diag(M['JA'] @ VA @ M['JA'].T))
    ceil = 0.5*sdA/np.sqrt(M['rdelta_min'])
    rowmax = np.abs(G).max(axis=1)
    dfc, bnd, _ = whole_face_defect(G, M)
    print(f"    gamma={gam:6.1f}: appraisal regression B_ww diag {np.diag(B[n:2*n, n:2*n]).round(1)}, "
          f"max |Gamma_ee'| {rowmax.max():.3f} <= ceiling {ceil.max():.3f}; whole-face defect {dfc:.3f} >= {bnd:.3f}")
print("    (B grows with need; the face-to-face transfer stays under the ceiling set by own response sd / display floor)")

print("D7  agency entry with partner attribution loading a_g: B = psi - a_g v'/(a_g^2 v' + w)")
err = 0.0
for s in range(200):
    rr = np.random.default_rng(2000+s)
    v, w, rg, psi, a_g = rr.uniform(0.2, 2), rr.uniform(0.05, 2), rr.uniform(0.05, 2), rr.normal(), rr.normal()
    M = build(seed=2000+s, v=v, w=w, rg=rg, psi=psi, a_g=a_g, vq=1e-9)
    _, _, VP, CAP = transfer(M)
    B = CAP @ np.linalg.pinv(VP, rcond=1e-12)
    vp = 1/(1/v + 1/rg)
    closed = psi - a_g*vp/(a_g**2*vp + w)
    err = max(err, abs(B[2*3, 2*3] - closed))
print(f"    max |B_gA,aP - closed form| = {err:.1e}")

print("D8  context latency with an event-level display floor: t_1/2 = r'/(r_delta + J^2/P0)")
for (P0, J, rdel, rp) in [(1.0, 1.0, 0.0, 0.5), (1.0, 1.0, 0.1, 0.5), (4.0, 0.5, 0.05, 0.2)]:
    t = np.linspace(1e-4, 200, 2_000_001)
    I = J**2/(rdel + rp/t); wgt = I/(P0 + I)
    Iinf = (J**2/rdel) if rdel > 0 else np.inf
    winf = Iinf/(P0 + Iinf) if np.isfinite(Iinf) else 1.0
    t_num = t[np.argmax(wgt >= winf/2)]
    t_formula = rp/(rdel + J**2/P0)
    print(f"    P0={P0}, J={J}, r_delta={rdel}, r'={rp}: numeric {t_num:.4f}  formula {t_formula:.4f}")

print("D9  the critic's K10 partner in the revised object: her smile tracks the agent's overall fortune.")
print("    (a) fortune already felt: her smile is explained by l_A in E, so it moves nothing.")
print("    (b) fortune not yet felt: one smile channel informs one direction; the P-block transfer has rank 1.")
n = 3; k = 16
JP = np.zeros((k, 2*n + 2)); JP[0:3, :n] = 0.2*np.eye(3)
JP[3, n:2*n] = 0.2                        # every prospective coordinate loads one smile channel (G0-like collapse)
JP[8, 2*n] = 0.2; JP[9, 2*n+1] = 0.2
for felt, label in [(True, "(a)"), (False, "(b)")]:
    conc = []
    for _ in range(n):
        # her prospects track the agent's realised (felt) or future outcome
        if felt:
            C4 = np.array([[1, 0, 0, .7], [0, 1, 0, 0], [0, 0, 1, 0], [.7, 0, 0, 1]])
        else:
            C4 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, .7], [0, 0, .7, 1]])
        conc.append(C4 + 1e-6*np.eye(4))
    M = build(n=n, k=k, seed=4, conc=conc, rf=1e9, JP=JP, JA=JP.copy(), rdelta=0.05)
    G, VA, VP, CAP = transfer(M)
    GP = G[3:8, :]                         # agent's prospective (P-family) output rows
    sv = np.linalg.svd(GP, compute_uv=False)
    print(f"    {label}: P-family rows of Gamma: norm {sv[0]:.4f}, singular values {sv[:3].round(4)}"
          f"  (rows of the attribution channels unchanged: {np.linalg.norm(G[8:10]):.4f})")

print("D10 innate ceiling 1/2: display floor r_delta set to the largest innate own-response variance sigma_bar^2")
print("     (computed at lam_A = lam_bar with no own prospective evidence); sweep need up to lam_bar in the K3 regime")
lam_bar = 10.0
def k3(gam, rdel):
    conc = []
    for _ in range(3):
        sP = 0.01; cf = 0.99*np.sqrt(sP)
        conc.append(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, cf], [0, 0, cf, sP]]) + 1e-6*np.eye(4))
    return build(seed=3, conc=conc, lamA=gam*np.ones(3), lamP=np.ones(3), rf=1e9, rdelta=rdel)
Mb = k3(lam_bar, 1.0); _, VAb, _, _ = transfer(Mb)
sig_bar = np.sqrt(np.diag(Mb['JA'] @ VAb @ Mb['JA'].T)).max()
for gam in [0.1, 1, 3, 10]:
    M = k3(gam, sig_bar**2)
    M['R'] = np.diag(sig_bar**2*np.ones(M['k']))
    G, *_ = transfer(M)
    print(f"    gamma={gam:5.1f}: max |Gamma_ee'| = {np.abs(G).max():.3f}  (ceiling 0.5)")
