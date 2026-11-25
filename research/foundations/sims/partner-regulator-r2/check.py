"""Algebra checks for design-partner-regulator.md revision 2 (not evidence; hand-set instances).
Run from research/foundations/sims:  uv run python -I partner-regulator-r2/check.py
"""
import numpy as np
from scipy.linalg import expm, solve_continuous_lyapunov
rng = np.random.default_rng(0)
def hdr(s): print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)

# ---------------------------------------------------------------------------
hdr("R1  P6 corrected: stable iff d > -r_N - min(r_M, w^2/r_M); Hopf when w > r_M")
for (rN, rM, w) in [(0.2, 2.0, 1.0), (0.2, 0.5, 2.0)]:
    dstar = -rN - min(rM, w**2 / rM)
    for d in (dstar + 0.01, dstar - 0.01):
        ev = np.linalg.eigvals(np.array([[-(rN + d), -w], [w, -rM]]))
        print(f"rN={rN} rM={rM} w={w}: d*={dstar:+.3f}  d={d:+.3f}  max Re={ev.real.max():+.4f}  "
              f"Im={abs(ev.imag).max():.3f}")
ev = np.linalg.eigvals(np.array([[-(0.2 - 1.5), -2.0], [2.0, -0.5]]))
print("critique C3 instance (d=-1.5):", np.round(ev, 3), "-> unstable, as the corrected threshold says")

# ---------------------------------------------------------------------------
hdr("R2  Critique C4 with the effector mask: atom q reads only the OTHER act's partner channel")
rN, rM, uN = 0.2, 2.0, 0.3
def Fmat(o, abar, masked):
    src = o[::-1] if masked else o          # masked: alpha_1 reads o_2, alpha_2 reads o_1
    al = -abar * np.tanh(src)
    F = np.zeros((3, 3))
    for q in range(2):
        F[0, 1 + q] += al[q]; F[1 + q, 0] -= al[q]
    return F - np.diag([rN, rM, rM])
O = rng.normal(0, 0.7, size=(400, 2))
for masked in (False, True):
    for abar in (0.1, 0.5, 1.0):
        Z = np.array([np.linalg.solve(Fmat(o, abar, masked), -np.array([uN, 0, 0])) for o in O])
        X = np.tanh(O)
        Gam, *_ = np.linalg.lstsq(np.column_stack([X, np.ones(len(X))]), Z[:, 1:], rcond=None)
        Gm = Gam[:2].T
        print(f"masked={masked!s:5} a_bar={abar}: fitted transfer (rows: own smile, frown) =\n{np.round(Gm, 4)}")
# Jacobian (linear-response) check at operating points, masked: pointwise same-channel entries
abar = 1.0
diag_abs, off_abs = [], []
for o in O[:200]:
    F = Fmat(o, abar, True); h0 = np.linalg.solve(F, -np.array([uN, 0, 0]))
    eps = 1e-6; Gcol = []
    for l in range(2):
        do = np.zeros(2); do[l] = eps
        Gcol.append((np.linalg.solve(Fmat(o + do, abar, True), -np.array([uN, 0, 0])) - h0)[1:] / eps)
    G = np.array(Gcol).T
    diag_abs.append(np.abs(np.diag(G)).max()); off_abs.append(np.abs(G[[0, 1], [1, 0]]).max())
print(f"masked, a_bar=1, 200 operating points: same-channel |dz_k/do_k| mean {np.mean(diag_abs):.4f} max {np.max(diag_abs):.4f};"
      f" crossed |dz_k/do_l| mean {np.mean(off_abs):.4f} max {np.max(off_abs):.4f}")
print("  -> pointwise the same-channel part is not zero: it is the loop through the single need (bounded in R3);"
      " it is odd in o and averages out in the regression above")

# ---------------------------------------------------------------------------
hdr("R3  Loop bound (T1'(c)): ||P_C G(iw)||_F <= ||E'|| a /nu_M(w) * 1/mu(w) * (a||B_M||_F/nu_M + ||B_W||_F)")
def instance(seed, nN=8, nC=4, G=3, dg=2, py=2):
    r = np.random.default_rng(seed)
    nM = G * dg; n = nN + nM + nC
    iN, iM, iC = np.arange(nN), nN + np.arange(nM), nN + nM + np.arange(nC)
    J = np.zeros((n, n))
    W = np.concatenate([iN, iC])
    Jfull = r.normal(0, 0.6, (n, n)); Jfull = Jfull - Jfull.T
    J[:, :] = Jfull; J[np.ix_(iM, iM)] = 0.0             # acts do not route among themselves
    rho, rMf = 0.15, 6.0
    L = r.normal(0, 0.3, (len(W), len(W))); RW = rho * np.eye(len(W)) + L @ L.T
    R = np.zeros((n, n)); R[np.ix_(W, W)] = RW
    for g in range(G):
        idx = iM[g * dg:(g + 1) * dg]; Lg = r.normal(0, 0.5, (dg, dg))
        R[np.ix_(idx, idx)] = rMf * np.eye(dg) + Lg @ Lg.T
    A = J - R
    m = G * py
    B = r.normal(0, 1.0, (n, m))
    for g in range(G):                                    # mask: act group g never reads partner group g
        B[np.ix_(iM[g * dg:(g + 1) * dg], np.arange(g * py, (g + 1) * py))] = 0.0
    Ep = np.zeros((m, n))
    for g in range(G):
        Ep[np.ix_(np.arange(g * py, (g + 1) * py), iM[g * dg:(g + 1) * dg])] = r.normal(0, 2.0, (py, dg))
    return A, B, Ep, iM, W, rho, rMf, G, py, J, R
worst = 0.0
for seed in range(200):
    A, B, Ep, iM, W, rho, rMf, G, py, J, R = instance(seed)
    n = A.shape[0]
    a = np.linalg.norm(A[np.ix_(iM, W)], 2)
    Js = np.linalg.norm(J, 2)
    BM, BW = np.linalg.norm(B[iM], 'fro'), np.linalg.norm(B[W], 'fro')
    for w in (0.0, 0.3, 1.0, 3.0, 10.0, 30.0):
        Gw = Ep @ np.linalg.solve(1j * w * np.eye(n) - A, B)
        mask = np.zeros_like(Gw, dtype=bool)
        for g in range(G):
            mask[g * py:(g + 1) * py, g * py:(g + 1) * py] = True
        copy = np.linalg.norm(Gw[mask])
        # direct part E' T_MM^-1 B_M has no copy-pattern entries
        TMM = 1j * w * np.eye(len(iM)) - A[np.ix_(iM, iM)]
        Gd = Ep[:, iM] @ np.linalg.solve(TMM, B[iM])
        assert np.abs(Gd[mask]).max() < 1e-12
        TMW, TWM = -A[np.ix_(iM, W)], -A[np.ix_(W, iM)]
        SW = 1j * w * np.eye(len(W)) - A[np.ix_(W, W)] - TWM @ np.linalg.solve(TMM, TMW)
        loop = Ep[:, iM] @ np.linalg.solve(TMM, TMW @ np.linalg.solve(SW, TWM @ np.linalg.solve(TMM, B[iM]) - B[W]))
        assert np.allclose(Gd + loop, Gw), "Schur decomposition identity"
        nuM = np.sqrt(w**2 + rMf**2)                     # A_MM symmetric, <= -rMf
        mu = max(rho, abs(w) - Js)
        bound = np.linalg.norm(Ep[:, iM], 2) * a / nuM / mu * (a * BM / nuM + BW)
        worst = max(worst, copy / bound)
print(f"200 random masked instances x 6 frequencies: G = direct + loop (asserted); direct copy-pattern entries = 0 (asserted);"
      f" max(actual copy-pattern / bound) = {worst:.3f}  (<= 1 required)")
A, B, Ep, iM, W, rho, rMf, G, py, J, R = instance(3)
n = A.shape[0]
for w in (0.0, 0.1, 1.0, 3.0, 10.0):
    Gw = Ep @ np.linalg.solve(1j * w * np.eye(n) - A, B)
    mask = np.zeros_like(Gw, dtype=bool)
    for g in range(G): mask[g * py:(g + 1) * py, g * py:(g + 1) * py] = True
    print(f"w={w:5.1f} s^-1: copy-pattern fraction ||P_C G||/||G|| = {np.linalg.norm(Gw[mask]) / np.linalg.norm(Gw):.3f}")

# ---------------------------------------------------------------------------
hdr("R4  T5: identifying the partner's response kernel from own logged randomness, under following")
def iv_sim(T, K, seed, follow=0.6, aP=0.7, sd_read=0.5, hid=0.4):
    r = np.random.default_rng(seed)
    p = 2; D = len(K)
    y = np.zeros((T, p)); e = np.zeros((T, p)); h = np.zeros(T)
    zeta = 0.3 * r.normal(size=(T, p)); xi = np.zeros((T, p))
    Ff = follow * np.eye(p) + 0.1 * np.array([[0, 1], [1, 0]])   # agent follows (copy-like)
    for t in range(1, T):
        h[t] = 0.98 * h[t - 1] + 0.2 * r.normal()
        xi[t] = 0.7 * xi[t - 1] + zeta[t]                           # coloured; zeta is logged
        resp = sum(K[d] @ e[t - d] for d in range(D) if t - d >= 0)
        y[t] = aP * y[t - 1] + resp + hid * h[t] * np.ones(p) + 0.3 * r.normal(size=p)
        e[t] = Ff @ y[t - 1] + hid * h[t] * np.ones(p) + xi[t]
    yo = y + sd_read * r.normal(size=y.shape)
    return yo, e, zeta
def cov_lag(a, b, lag):                      # Cov(a_t, b_{t-lag})
    a0, b0 = a - a.mean(0), b - b.mean(0)
    return a0[lag:].T @ b0[:len(b0) - lag] / (len(a0) - lag)
def iv_deconv(yo, e, zeta, D, tau0=0):
    Sz = np.cov(zeta.T)
    kap = [cov_lag(e, zeta, tau) for tau in range(D + tau0 + 1)]   # Cov(e_{t+tau}, zeta_t)
    C = [cov_lag(yo, zeta, d) for d in range(D + tau0 + 1)]
    Kh = []
    for d in range(D):
        acc = C[d + tau0] - sum(Kh[dp] @ kap[d + tau0 - dp] for dp in range(d))
        Kh.append(acc @ np.linalg.inv(kap[tau0]))
    return Kh
def naive(yo, e, D):
    T = len(yo); X = np.column_stack([e[D - d:T - d] for d in range(D)]); Y = yo[D:]
    X = np.column_stack([X, np.ones(len(X))])
    Bc = np.linalg.lstsq(X, Y, rcond=None)[0]
    return [Bc[2 * d:2 * d + 2].T for d in range(D)]
D = 12
for name, K in (("autonomous partner (K = 0)", [np.zeros((2, 2))] * D),
                ("crossed responder (K(2) = [[0,.3],[.3,0]])",
                 [np.zeros((2, 2)), np.zeros((2, 2)), np.array([[0, .3], [.3, 0]]), np.zeros((2, 2))])):
    errs_iv, errs_nv, Ks = [], [], []
    for seed in range(20):
        yo, e, zeta = iv_sim(36000, K, seed)
        Kh = iv_deconv(yo, e, zeta, D); Kn = naive(yo, e, D)
        Ks.append(Kh[2])
        Kp = list(K) + [np.zeros((2, 2))] * (D - len(K))
        Kt = [sum(0.7 ** k * Kp[d - k] for k in range(d + 1)) for d in range(D)]   # total causal kernel (persistence aP=0.7)
        errs_iv.append(max(np.abs(Kh[d] - Kt[d]).max() for d in range(D)))
        errs_nv.append(max(np.abs(Kn[d] - Kt[d]).max() for d in range(D)))
    print(f"{name}: max|K_hat - K_total| over lags, mean (sd) of 20 seeds: IV {np.mean(errs_iv):.3f} ({np.std(errs_iv):.3f})"
          f"   naive lagged OLS {np.mean(errs_nv):.3f}")
    print("   IV estimate of K(2), seed mean:", np.round(np.mean(Ks, 0), 3).tolist(), " true total K(2):", np.round(sum(0.7 ** k * K[2 - k] for k in range(3)), 3).tolist())
# echo removal: own-state residual uncorrelated with zeta at the identified kernel
yo, e, zeta = iv_sim(18000, [np.zeros((2, 2)), np.zeros((2, 2)), np.array([[0, .3], [.3, 0]]), np.zeros((2, 2))], 1)
Kh = iv_deconv(yo, e, zeta, D)
own = yo.copy()
for d in range(D): own[d:] -= e[:len(e) - d] @ Kh[d].T

print("max |Cov(partner own-part, zeta lag d)|, d=0,2,..,10:",
      np.round([np.abs(cov_lag(own, zeta, d)).max() for d in range(0, 12, 2)], 4).tolist(),
      " vs raw:", np.round([np.abs(cov_lag(yo, zeta, d)).max() for d in range(0, 12, 2)], 4).tolist())

# ---------------------------------------------------------------------------
hdr("R5  Two time scales (T6): phasic innate match (~t^2 onset) vs same-channel learned path (<= t^4 onset)")
dt = 1e-3; T = 8.0; ts = np.arange(0, T, dt); td = 0.17
lam_o, c_inj, rN_, wbar, rM_, Ep_, tau_m, tau_a, tau_h, g_inn = 2.0, 0.5, 0.5, 1.0, 20.0, 10.0, 0.1, 0.15, 3.0, 0.3
def run(sign=+1.0):
    xo = xN = xM = mL = aF = aS = mI = 0.0; out = []
    for t in ts:
        y = 1.0 if t >= td else 0.0
        xo += dt * lam_o * (y - xo)                 # observer state (unit steady gain), rate lam_o
        xN += dt * (-rN_ * xN + sign * c_inj * xo)  # drive-scaled coefficient change injects into a need
        xM += dt * (-rM_ * xM + wbar * xN)          # need -> own same-channel act (reciprocity)
        mL += dt * (Ep_ * xM - mL) / tau_m          # muscle
        aF += dt * (y - aF) / tau_a                 # innate band-pass: fast low-pass minus slow low-pass
        aS += dt * (y - aS) / tau_h
        mI += dt * (g_inn * (aF - aS) - mI) / tau_m
        out.append((t, mI, mL))
    return np.array(out)
out = run(+1.0); outn = run(-1.0)
Lam = lam_o * c_inj * wbar * Ep_ / tau_m        # product of the stage gains (impulse-response bounds)
for tt in (0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0 - dt):
    i = int(tt / dt); tp = max(tt - td, 0)
    print(f"t={tt:3.1f}s innate={out[i,1]:+.4f} learned(match)={out[i,2]:+.4f} total={out[i,1]+out[i,2]:+.4f}"
          f"  learned(counter) total={outn[i,1]+outn[i,2]:+.4f}  bound={min(Lam*tp**4/24, 9.99):.4f}")
print(f"learned steady gain = {c_inj/rN_*wbar/rM_*Ep_:.3f}; innate steady gain = 0 (band-pass), peak {out[:,1].max():.3f}"
      f" at t={ts[out[:,1].argmax()]:.2f}s")
eps = 0.2
print(f"bound-guaranteed window: learned <= {eps} x innate peak until t' = (24 eps peak / Lam)^(1/4) ="
      f" {(24*eps*out[:,1].max()/Lam)**0.25:.2f} s after detection (conservative)")
i20 = np.argmax(np.abs(out[:, 2]) >= eps * out[:, 1].max())
print(f"simulated: learned reaches {eps} x innate peak at t={ts[i20]:.2f}s")
xo = xM = mC = 0.0; outc = []
for t in ts:
    y = 1.0 if t >= td else 0.0
    xo += dt * lam_o * (y - xo); xM += dt * (-rM_ * xM + c_inj * 4 * xo); mC += dt * (Ep_ * xM - mC) / tau_m
    outc.append(mC)
outc = np.array(outc)
for tt in (0.5, 1.0, 2.0):
    print(f"t={tt}s cross-channel learned response={outc[int(tt/dt)]:.4f} (same-channel {out[int(tt/dt),2]:.4f})")

# ---------------------------------------------------------------------------
hdr("R6  Interoception lemma: |G^1/2 C h| <= |G^1/2 b| for any learned C; partner shift on measured needs <= |inj|/sqrt(g r)")
worst1 = worst2 = 0.0
for s in range(500):
    r = np.random.default_rng(s); nN, nb = 6, 3
    C = r.normal(0, r.uniform(0.1, 10), (nb, nN)); Gm = np.diag(r.uniform(0.1, 2, nb))
    Jn = r.normal(size=(nN, nN)); Jn -= Jn.T; Rn = 0.2 * np.eye(nN) + (lambda L: L @ L.T)(r.normal(0, .3, (nN, nN)))
    b = r.normal(size=nb)
    h = np.linalg.solve(-(Jn - Rn) + C.T @ Gm @ C, C.T @ Gm @ b)
    sq = np.sqrt(Gm)
    worst1 = max(worst1, np.linalg.norm(sq @ C @ h) / np.linalg.norm(sq @ b))
    gam = r.uniform(0.1, 50); inj = r.normal(size=nN); Cn = C / np.linalg.norm(C, 2)
    dh = np.linalg.solve(-(Jn - Rn) + gam * Cn.T @ Cn, inj)
    worst2 = max(worst2, np.linalg.norm(Cn @ dh) / (np.linalg.norm(inj) / np.sqrt(gam * 0.2)))
print(f"max ratio (must be <= 1): body lemma {worst1:.3f}; social-referencing bound {worst2:.3f}")

# ---------------------------------------------------------------------------
hdr("R7  Concern route: the M-row of J_soc is minus the gradient of the weighted partner need energy")
r = np.random.default_rng(7); nN, nM, nP, K = 5, 4, 5, 3
A = r.normal(size=(K, nN)); hN = r.normal(size=nN); hP = r.normal(size=nP)      # my drive, partner read drive
dB = -np.abs(r.normal(size=(K, nP)))           # d beta_q / d H_hat_i <= 0 (monotone guard)
kap = r.normal(size=(nP, nM))                  # IV kernel: my act -> partner state (dc)
Cj = -sum(np.outer(A[q] * (A[q] @ hN), dB[q] * hP) for q in range(K)) @ kap   # (D_q h_N)(grad beta)^T J_H kappa
wts = -sum(dB[q] * (A[q] @ hN) ** 2 for q in range(K))                          # >= 0
Mrow = -Cj.T @ hN
grad = kap.T @ (wts * hP)                       # d/d(act) of sum_i w_i H_i(x_hat + kappa act), H_i = x^2/2
print("M-row == -grad(sum w_i H_i):", np.allclose(Mrow, -grad), "  weights >= 0:", bool((wts >= 0).all()))
