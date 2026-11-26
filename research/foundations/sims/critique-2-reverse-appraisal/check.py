"""Counterexample checks for critique-2-design-reverse-appraisal.md (revision 2 of RAB).
They run the design's own local linear-Gaussian equations (T1(a): Gamma = J_A C_AP J_P^T (J_P V_P J_P^T + R)^-1)
on hand-set instances. They test the document's algebra and claims, not behaviour or people.
Run from sims/:  uv run python critique-2-reverse-appraisal/check.py"""
import numpy as np
np.set_printoptions(precision=4, suppress=True)


def transfer(S, H, Rz, AA, AP, JA, JP, R):
    """Local model: prior N(0,S) over s, non-face evidence z = H s + noise(Rz), alpha_A = AA s, alpha_P = AP s,
    her face y = JP alpha_P + noise(R). Returns Gamma and the conditional covariances."""
    if H is None:
        Se = S
    else:
        K = S @ H.T @ np.linalg.inv(H @ S @ H.T + Rz)
        Se = S - K @ H @ S
    VA, VP, CAP = AA @ Se @ AA.T, AP @ Se @ AP.T, AA @ Se @ AP.T
    G = JA @ CAP @ JP.T @ np.linalg.inv(JP @ VP @ JP.T + R)
    return G, VA, VP, CAP


def defect_U(G, U, W=None):
    """operator copy defect on the input subspace U (columns), min_c ||(G - cI)|_U|| / ||G|_U||."""
    if W is None:
        W = np.eye(G.shape[0])
    Gw = W @ G @ np.linalg.inv(W)
    Q, _ = np.linalg.qr(W @ U)
    M = Gw @ Q
    nrm = np.linalg.norm(M, 2)
    if nrm < 1e-15:
        return np.nan, 0.0
    cs = np.linspace(-2, 2, 8001)
    d = min(np.linalg.norm(M - c*Q, 2) for c in cs)
    return d/nrm, nrm


def prosp_model(n, sA, sP, rho, lamA, lamP, rf, oP_var=None, eps=1e-9):
    """s = (o_A, o_P, f_A, fP~) per concern; only (f_A,j, fP~_j) correlated (corr rho_j).
    alpha = (l(n), w(n)); l_A felt exactly. Returns S, H, Rz, AA, AP (agency/world blocks omitted:
    they are independent and render on disjoint channels in these instances)."""
    sA, sP, rho = (np.broadcast_to(np.asarray(x, float), (n,)) for x in (sA, sP, rho))
    lamA, lamP = (np.broadcast_to(np.asarray(x, float), (n,)) for x in (lamA, lamP))
    oPv = np.ones(n) if oP_var is None else np.broadcast_to(np.asarray(oP_var, float), (n,))
    m = 4*n
    S = np.zeros((m, m))
    for j in range(n):
        iA, iP, ifA, ifP = j, n+j, 2*n+j, 3*n+j
        S[iA, iA] = 1.0; S[iP, iP] = oPv[j] + eps
        c = rho[j]*np.sqrt(sA[j]*sP[j])
        S[np.ix_([ifA, ifP], [ifA, ifP])] = [[sA[j] + eps, c], [c, sP[j] + eps]]
    H = np.zeros((2*n, m)); H[:n, :n] = np.eye(n); H[n:, 2*n:3*n] = np.eye(n)
    Rz = np.diag(np.r_[1e-10*np.ones(n), rf*np.ones(n)])
    AA = np.zeros((2*n, m)); AP = np.zeros((2*n, m))
    AA[:n, :n] = -np.diag(lamA); AA[n:, 2*n:3*n] = -np.diag(lamA)
    AP[:n, n:2*n] = -np.diag(lamP); AP[n:, 3*n:] = -np.diag(lamP)
    return S, H, Rz, AA, AP


print("X1  T2 corollary, step 3 (||e_e^T J_A|| <= Lbar) fails when two synergies driven by one appraisal")
print("    coordinate load the same channel (AU4 in both the confrontation and withdrawal synergies of S_A).")
# attribution block only: s = (g, gt, q, qt); a_A = g - q, a_P = -gt - qt; no own causal record.
v_g, a_g, w_p, psi, v_q, v_qt = 1.0, 1.0, 1e-4, -1.0, 1e-4, 1e-6
Vgt = a_g**2*v_g + w_p
S = np.array([[v_g, a_g*v_g, psi*a_g*v_g, 0],
              [a_g*v_g, Vgt, psi*Vgt, 0],
              [psi*a_g*v_g, psi*Vgt, psi**2*Vgt + v_q, 0],
              [0, 0, 0, v_qt]])
AA = np.array([[1., 0, -1, 0]]); AP = np.array([[0., -1, 0, -1]])
vbar_g, vbar_q = v_g, psi**2*Vgt + v_q            # the clips are met with equality
Lbar = 1.0
sig_bar2 = Lbar**2 * 2*(vbar_g + vbar_q)          # corollary's sigma-bar^2 (other innate terms taken small)
r_delta = sig_bar2                                # corollary's floor
JA = np.array([[np.sqrt(2.0)]])                   # dh_A/da = (1/sqrt2, 1/sqrt2): column norm 1 = Lbar; both load AU4 with 1
_, _, VP, _ = transfer(S, None, None, AA, AP, JA, np.array([[1.0]]), np.array([[r_delta]]))
JP = np.array([[np.sqrt(r_delta/VP[0, 0])]])     # her loading that maximises the entry
G, VA, VP, CAP = transfer(S, None, None, AA, AP, JA, JP, np.array([[r_delta]]))
print(f"    sigma_A,e = {np.sqrt(JA[0,0]**2*VA[0,0]):.3f} > sigma_bar = {np.sqrt(sig_bar2):.3f};  "
      f"|Gamma_AU4,AU4'| = {abs(G[0,0]):.3f}  (claimed ceiling 0.5)")

print("X2  T4(ii) is false under the design's own (eta, eps) dial definition: a scalar entering ONLY group 1")
print("    (her inferred need on concern 1, lamP_1) runs a 2-dim subspace from flat to copy by explaining away in N.")
n = 3
# her channels: A (AU12: loaded by her l_P,1 via the Duchenne synergy and by w_P,2 via the social smile),
#               B (a brow channel: loaded by w_P,1 and w_P,3). Agent renders w_A,2 -> A, w_A,3 -> B, w_A,1 -> C.
k = 3
JP = np.zeros((k, 2*n)); JP[0, 0] = 1.0; JP[0, n+1] = 1.0; JP[1, n+0] = 1.0; JP[1, n+2] = 1.0
JA = np.zeros((k, 2*n)); JA[0, n+1] = 1.0; JA[1, n+2] = 1.0; JA[2, n+0] = 1.0
R = 0.05*np.eye(k)
U = np.eye(k)[:, :2]
for lp1 in [30.0, 10.0, 3.0, 1.0, 0.3, 0.1, 0.0]:
    S, H, Rz, AA_, AP_ = prosp_model(n, sA=1.0, sP=0.2, rho=[0.0, 0.8, 0.8], lamA=1.0,
                                     lamP=[lp1, 1.0, 1.0], rf=1e9, oP_var=[1.0, 1.0, 1.0])
    G, *_ = transfer(S, H, Rz, AA_, AP_, JA, JP, R)
    d, nrm = defect_U(G, U)
    print(f"    lamP_1 = {lp1:5.1f}:  ||Gamma|_U|| = {nrm:.4f}   copy defect on U = {d:.4f}")

print("X3  A common variance head (prior network: one scale kappa on Var f_A,j for all j) is a flat-to-copy dial")
print("    on the whole prospective subspace; T4's list of multi-group quantities omits it. Dedicated channels, J_A = J_P.")
n = 4
k = 2*n
JP = np.zeros((k, 2*n)); JP[:n, :n] = np.eye(n); JP[n:, n:] = np.eye(n)   # l channels (C0) and w channels
JA = JP.copy()
lamA = 1.0; lamP = 1.0; sbar = 1.0; sP = 1.0
sig_bar2 = n*lamA**2*sbar                         # corollary floor, prospective part only, Lbar = 1
U = np.eye(k)[:, n:]                              # prospective subspace (social smile, brows, head, F0 ...)
for label, rho in [("uniform corr .9", [0.9]*n), ("corr in [.80, .95]", [0.80, 0.85, 0.90, 0.95])]:
    print(f"    {label}; display floor r_delta = sigma_bar^2 = {sig_bar2}:")
    for kap in [1e-4, 1e-2, 0.1, 0.3, 1.0]:
        S, H, Rz, AA_, AP_ = prosp_model(n, sA=kap*sbar, sP=sP*sig_bar2, rho=rho, lamA=lamA, lamP=lamP, rf=1e9)
        G, *_ = transfer(S, H, Rz, AA_, AP_, JA, JP, sig_bar2*np.eye(k))
        d, nrm = defect_U(G, U)
        print(f"      kappa = {kap:7.4f}:  ||Gamma|_U|| = {nrm:.4f}   copy defect = {d:.4f}   max entry {np.abs(G).max():.4f}")
print("    Same sweep with a small floor (r_delta = 0.05), to show the shape of the dial without the worst-case floor:")
for kap in [1e-4, 1e-2, 0.1, 1.0]:
    S, H, Rz, AA_, AP_ = prosp_model(n, sA=kap, sP=0.05, rho=[0.9]*n, lamA=1.0, lamP=1.0, rf=1e9)
    G, *_ = transfer(S, H, Rz, AA_, AP_, JA, JP, 0.05*np.eye(k))
    d, nrm = defect_U(G, U)
    print(f"      kappa = {kap:7.4f}:  ||Gamma|_U|| = {nrm:.4f}   copy defect = {d:.4f}")

print("X4  T3's floor sqrt(e0/e) uses the model-implied energy Sigma~ = W J_P V_P J_P^T W, which is state-dependent:")
print("    as the prior network becomes sure of her realised outcome (Var o_P | E -> 0), e0/e -> 0 and the")
print("    energy-weighted whole-face defect follows it down to the prospective copy above.")
n = 4; k = 2*n
JP = np.zeros((k, 2*n)); JP[:n, :n] = np.eye(n); JP[n:, n:] = np.eye(n); JA = JP.copy()
P0 = np.diag(np.r_[np.ones(n), np.zeros(n)])
for ov in [1.0, 0.1, 1e-2, 1e-3, 1e-5]:
    S, H, Rz, AA_, AP_ = prosp_model(n, sA=0.3, sP=0.05, rho=[0.9]*n, lamA=1.0, lamP=1.0, rf=1e9, oP_var=ov)
    R = 0.05*np.eye(k)
    G, VA, VP, CAP = transfer(S, H, Rz, AA_, AP_, JA, JP, R)
    W = np.diag(1/np.sqrt(np.diag(R)))
    Sig = W @ JP @ VP @ JP.T @ W
    ev, Uv = np.linalg.eigh(Sig); Sh = Uv @ np.diag(np.sqrt(np.clip(ev, 0, None))) @ Uv.T
    Gw = W @ G @ np.linalg.inv(W)
    c = np.trace(Gw @ Sig)/np.trace(Sig)  # optimal c for the Frobenius defect
    dS = np.linalg.norm((Gw - c*np.eye(k)) @ Sh)/np.linalg.norm(Gw @ Sh)
    e0e = np.trace(P0 @ Sig)/np.trace(Sig)
    print(f"    Var(o_P|E) = {ov:7.0e}:  sqrt(e0/e) = {np.sqrt(e0e):.4f}   whole-face delta_Sigma = {dS:.4f}   ||P0 Gamma|| = {np.linalg.norm(P0@G):.1e}")

print("X5  T3 lemma in the full system: h_H(l, b) and E_self m. Her face -> prospective voice (F0/tempo) ->")
print("    vocal-effort body variable -> h_H(., b) -> liking channels. DC gain of the leak, linearised:")
rng = np.random.default_rng(7)
Gam_P = 0.3*rng.normal(size=(3, 4))        # prospective voice rows of Gamma (bounded by T2)
E_self = np.zeros((8, 3)); E_self[5, :] = 0.5     # vocal output costs vocal effort (body variable 6)
A_b = np.diag(np.full(8, 0.2))
dhH_db = np.zeros((4, 8)); dhH_db[:, 5] = 0.4     # sighs / cry-like bursts depend on effort through h_H(l, b)
S_H = np.eye(4)
leak = S_H @ dhH_db @ np.linalg.inv(A_b) @ E_self @ Gam_P
print(f"    ||P0 Gamma_total|| = {np.linalg.norm(leak):.3f}  (T3 lemma claims exactly 0)")

print("X6  Assumption H fails beyond 2.9 s: her slow contagion of the agent's prospective display (lag > Q_p window)")
print("    makes the relation M-step learn shared prospects c > 0 from the agent's own echo (true c = 0).")
rng = np.random.default_rng(11)
N = 200000
sA, sP, rf, lamA, lamP, R = 1.0, 1.0, 0.5, 1.0, 1.0, 0.3
for q in [0.0, 0.2, 0.5]:
    c = 0.0
    fA = rng.normal(0, np.sqrt(sA), N); zf = fA + rng.normal(0, np.sqrt(rf), N)
    fP = rng.normal(0, np.sqrt(sP), N)                           # her own prospects: independent of fA
    d = -lamA*(sA/(sA + rf))*zf                                   # agent display of its own w_A = -lamA E[f_A]
    y = -lamP*fP + q*d + rng.normal(0, np.sqrt(R), N)             # her face, > 2.9 s later; echo not subtracted
    for it in range(60):
        # agent's model: (fA, fP) ~ N(0, [[sA, c],[c, sP]]), y = -lamP fP + noise(R); fA later felt exactly.
        # E[fP | fA, y]: condition fP on fA first, then on y.
        mP = c/sA*fA; vP = sP - c**2/sA
        k_ = vP*(-lamP)/(lamP**2*vP + R)
        EfP = mP + k_*(y - (-lamP)*mP)
        c_new = np.mean(fA*EfP)                                   # M-step with posterior moments (fA exact)
        c = np.clip(c_new, -0.999*np.sqrt(sA*sP), 0.999*np.sqrt(sA*sP))
    print(f"    her slow echo gain q = {q:.1f}:  learned c* = {c:+.3f}   (corr {c/np.sqrt(sA*sP):+.3f})")
