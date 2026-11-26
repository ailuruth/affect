"""Algebra checks for derivation-self-invariant-maps.md (S1-S6).
Hand-made instances only; they verify mathematics, not behaviour (brief: no toy worlds)."""
import numpy as np
rng = np.random.default_rng(0)
fs = 10.0  # Hz (downsampled from 30 for speed; nothing depends on it)

def ou(T, tau, rng):
    a = np.exp(-1/(fs*tau)); x = np.zeros(T); e = rng.standard_normal(T)*np.sqrt(1-a*a)
    for t in range(1, T): x[t] = a*x[t-1] + e[t]
    return x

def lagmat(x, lags):
    T = len(x); X = np.zeros((T, len(lags)))
    for i, L in enumerate(lags): X[L:, i] = x[:T-L] if L > 0 else x
    return X

def expfilt(x, tau):
    a = np.exp(-1/(fs*tau)); y = np.zeros_like(x)
    for t in range(1, len(x)): y[t] = a*y[t-1] + (1-a)*x[t]
    return y

def basis(A, fast_lags=(1,2,3,5,8,12,20,30), slow_taus=(5.,20.,60.)):
    cols = []
    for c in range(A.shape[1]):
        cols.append(lagmat(A[:, c], fast_lags))
        if slow_taus: cols.append(np.stack([expfilt(A[:, c], tau) for tau in slow_taus], 1))
    return np.hstack(cols)

def ols_resid(Phi, p):
    w, *_ = np.linalg.lstsq(Phi, p, rcond=None); return p - Phi @ w

def recursive_residuals(Phi, p, lam=1.0):
    """exact (pseudo-inverse during burn-in) a-priori RLS errors, normalised by sqrt(1+h)."""
    T, M = Phi.shape; out = np.full(T, np.nan); G = np.zeros((M, M)); b = np.zeros(M)
    for t in range(T):
        f = Phi[t]
        if t >= M and np.linalg.matrix_rank(G) == M:
            w = np.linalg.solve(G, b); h = f @ np.linalg.solve(G, f); out[t] = (p[t] - f @ w)/np.sqrt(1 + h)
        G = lam*G + np.outer(f, f); b = lam*b + f*p[t]
    return out

print("S1  exact invariance of the quotient coordinates (linear lagged class)")
T = 1200; A = np.stack([ou(T, 2.0, rng) for _ in range(2)], 1); Phi = basis(A); M = Phi.shape[1]
p = ou(T, 3.0, rng); K = rng.standard_normal(M)
r0, r1 = ols_resid(Phi, p), ols_resid(Phi, p + Phi @ K)
print(f"    M={M}; max|OLS residual change| = {np.max(np.abs(r0-r1)):.2e}")
w0, w1 = recursive_residuals(Phi, p), recursive_residuals(Phi, p + Phi @ K)
ok = ~np.isnan(w0)
print(f"    recursive residuals: first defined at t={np.argmax(ok)} (burn-in = M), max change {np.nanmax(np.abs(w0-w1)):.2e}")
t0 = np.argmax(ok); rss0 = np.sum(ols_resid(Phi[:t0], p[:t0])**2)
print(f"    RSS(burn-in) + sum w^2 = {rss0 + np.nansum(w0**2):.6f}; RSS(full) = {np.sum(r0**2):.6f}; |p|^2 = {np.sum(p**2):.3f}  (isometry onto quotient, nonexpansive)")
# LMS: not invariant, transient
def lms(Phi, p, eta=0.5):
    w = np.zeros(Phi.shape[1]); e = np.zeros(len(p))
    for t in range(len(p)):
        f = Phi[t]; e[t] = p[t] - w @ f; w += eta*e[t]*f/(1 + f @ f)
    return e
d = lms(Phi, p + Phi @ K) - lms(Phi, p)
q = len(d)//4
print("    NLMS innovations change under the same g, rms by quarter:", " ".join(f"{np.sqrt(np.mean(d[i*q:(i+1)*q]**2)):.3f}" for i in range(4)))

print("S2  no-go: nonlinear (Lipschitz) class at horizon 0 shatters a realised path")
a = rng.standard_normal((T, 2)); pp = rng.standard_normal(T)
D = np.sqrt(((a[:, None, :]-a[None, :, :])**2).sum(-1)); np.fill_diagonal(D, np.inf)
L = np.max(np.abs(pp[:, None]-pp[None, :])/D)
print(f"    min distance between own samples {D.min():.2e} > 0; McShane extension g(x)=min_s(-p_s+L|x-a_s|), L={L:.0f}")
g = lambda x: np.min(-pp + L*np.sqrt(((a - x)**2).sum(1)))
print(f"    max |p_t + g(a_t)| = {max(abs(pp[t]+g(a[t])) for t in range(0, T, 7)):.1e} -> (a,p) and (a,0) are in one orbit")
# kernel smoother residual: invariance error vs information kept
X = a; Kxx = np.exp(-((X[:, None, :]-X[None, :, :])**2).sum(-1)/0.5)
gs = np.sin(2*X[:, 0]) * X[:, 1]       # a smooth partner response g(a)
for lamb in (1e-6, 1e-3, 1e-1, 1e1):
    S = Kxx @ np.linalg.inv(Kxx + lamb*np.eye(T))
    R = np.eye(T) - S
    print(f"    kernel ridge lambda={lamb:g}: kept |R p|^2/|p|^2 = {np.sum((R@pp)**2)/np.sum(pp**2):.3f}; "
          f"leak of g |R g|^2/|g|^2 = {np.sum((R@gs)**2)/np.sum(gs**2):.4f}")

print("S3  infinite-horizon LTI class: Toeplitz(a) invertible -> every p is h*a")
a1 = rng.standard_normal(300); Tz = np.array([[a1[i-j] if i >= j else 0 for j in range(300)] for i in range(300)])
print(f"    det(Toeplitz) = a_0^T = ({a1[0]:.3f})^300 != 0 -> V_T(a) = R^T; but cond = {np.linalg.cond(Tz):.1e}: the filter that does it is enormous (unstable inverse)")

print("S4  spurious absorption of the partner's independent slow drift (OLS quotient, 10-min window)")
for slow in ((5., 20., 60.), ()):
    fr = []
    for s in range(20):
        r = np.random.default_rng(100+s); T4 = int(600*fs)
        A4 = np.stack([ou(T4, 2.0, r) + 0.7*ou(T4, 60.0, r) for _ in range(4)], 1)
        P4 = basis(A4, slow_taus=slow)
        eps = ou(T4, 60.0, r)                      # partner's own slow content, independent of the agent
        res = ols_resid(P4, eps); fr.append(1 - np.var(res)/np.var(eps))
    print(f"    slow filters {slow or 'none'}: M={P4.shape[1]}, fraction of independent slow partner variance removed = {np.mean(fr):.2f} (sd {np.std(fr):.2f})")

print("S5  closed loop: agent echoes partner news (gain 0.25, lag 1 s); OLS vs IV representative")
T5 = int(1800*fs); r = np.random.default_rng(7)
eps = ou(T5, 20.0, r); bexo = ou(T5, 1.0, r)       # partner news; agent's own exogenous variation (logged)
a5 = bexo + 0.25*np.r_[np.zeros(10), eps[:-10]]   # agent echoes partner 1 s late
Ktrue = 0.5; p5 = eps + Ktrue*np.r_[np.zeros(5), a5[:-5]]    # partner also follows agent at 0.5 s
lags = (1, 3, 5, 8, 12, 20, 30, 50)
Phi5, Z5 = lagmat(a5, lags), lagmat(bexo, lags)
r_ols = ols_resid(Phi5, p5)
Kiv = np.linalg.solve(Z5.T @ Phi5, Z5.T @ p5); r_iv = p5 - Phi5 @ Kiv
for name, rr in (("OLS", r_ols), ("IV ", r_iv)):
    print(f"    {name}: corr(rep, partner news) = {np.corrcoef(rr, eps)[0,1]:.3f}; var(rep)/var(news) = {np.var(rr)/np.var(eps):.3f}")
Piv = Phi5 @ np.linalg.solve(Z5.T @ Phi5, Z5.T); 
# operator norm of I - P_iv on a subsample (oblique projection > 1)
idx = slice(0, 1500); Q, _ = np.linalg.qr(Phi5[idx]); Zq, _ = np.linalg.qr(Z5[idx])
cosmin = np.linalg.svd(Q.T @ Zq, compute_uv=False).min()
print(f"    ||I - P_IV|| = 1/cos(max principal angle) = {1/cosmin:.2f}  (OLS: 1.00); invariance of IV rep: "
      f"{np.max(np.abs((p5 + Phi5@np.ones(len(lags)) - Phi5@np.linalg.solve(Z5.T@Phi5, Z5.T@(p5+Phi5@np.ones(len(lags))))) - r_iv)):.1e}")
bw = 0.1*bexo   # weak instrument
Z6 = lagmat(bw + 0.0, lags); a6 = bw + 0.25*np.r_[np.zeros(10), eps[:-10]] + 0.3*ou(T5, 2.0, r)
Q6, _ = np.linalg.qr(lagmat(a6, lags)[idx]); Z6q, _ = np.linalg.qr(Z6[idx])
print(f"    weak instrument (own exogenous share ~4% of variance): ||I - P_IV|| = {1/np.linalg.svd(Q6.T@Z6q, compute_uv=False).min():.1f}")

print("S6  contingency echo normalised by its own estimate: loop gain kappa*K/(K+s) < kappa for every K")
kap, s = 0.3, 0.2
for Kp in (0.2, 1.0, 3.0, 10.0):
    x = np.zeros(4000); own = ou(4000, 2.0, np.random.default_rng(3)); pr = np.zeros(4000)
    for t in range(6, 4000):
        pr[t] = Kp*x[t-5]                               # partner returns the agent's expression 0.5 s later
        x[t] = own[t] + kap*pr[t-1]/(Kp + s)            # agent's bounded echo of the returned expression
    print(f"    K={Kp:5.1f}: loop gain {kap*Kp/(Kp+s):.3f}; std(agent)/std(own) = {np.std(x)/np.std(own):.3f}; std(agent - own)/std(own) = {np.std(x-own)/np.std(own):.3f} <= small-gain bound g/(1-g) = {(kap*Kp/(Kp+s))/(1-kap*Kp/(Kp+s)):.3f}")
