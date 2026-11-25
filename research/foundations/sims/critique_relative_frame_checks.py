import numpy as np
from scipy.linalg import expm, logm
rng = np.random.default_rng(0)
K = 8

def Xi(r, m, yt):
    eps = (r @ m).real - yt
    return 0.5*(r.conj().T @ np.outer(eps, m) - np.outer(m, eps) @ r)

print("== C1: O(K) is invariant under the relation flow (G) from r=I ==")
r = np.eye(K, dtype=complex)
beta = 0.5
for t in range(20000):
    m = rng.standard_normal(K)
    yt = beta*m + 0.3*rng.standard_normal(K)
    r = r @ expm(-0.01*Xi(r, m, yt))
print("max|Im r| after 20000 steps from I:", np.abs(r.imag).max())
print("sing. values of Re r:", np.round(np.linalg.svd(r.real, compute_uv=False), 3))
print("loss at r:", np.mean([np.sum(((r@m).real - beta*m)**2) for m in rng.standard_normal((2000,K))]))
print("loss at M*=0.5 I (global min over ball):", np.mean([np.sum((0.5*m - beta*m)**2) for m in rng.standard_normal((2000,K))]))

print("\n== C2: same flow, uncorrelated target (partner predicts nothing): random walk in SO(K), full enactment ==")
r = np.eye(K, dtype=complex)
for t in range(20000):
    m = rng.standard_normal(K); yt = rng.standard_normal(K)
    r = r @ expm(-0.01*Xi(r, m, yt))
print("max|Im r|:", np.abs(r.imag).max(), " ||Re r - I||_F:", np.linalg.norm(r.real-np.eye(K)).round(3),
      " sing vals Re r:", np.round(np.linalg.svd(r.real, compute_uv=False),3))

print("\n== C3: escape from O(K) after a 1e-12 imaginary perturbation (beta=0.5) ==")
A0 = rng.standard_normal((K,K)); A0 = A0+A0.T
r = expm(1j*1e-12*A0)
for t in range(1, 40001):
    m = rng.standard_normal(K); yt = 0.5*m + 0.3*rng.standard_normal(K)
    r = r @ expm(-0.01*Xi(r, m, yt))
    if t in (1000, 5000, 10000, 20000, 40000):
        print(t, "max|Im r| =", "%.2e" % np.abs(r.imag).max(), " sv(Re r) =", np.round(np.linalg.svd(r.real, compute_uv=False),2))

print("\n== C4: the derived dial: target ytilde = kappa*P m (rank-4 synergy subspace); minimiser = min(kappa,1) on P ==")
P = np.zeros((K,K)); P[:4,:4] = np.eye(4)
for kappa in (0.0, 0.3, 0.7, 1.0, 2.0):
    A0 = rng.standard_normal((K,K)); A0 = A0+A0.T
    r = expm(1j*0.3*A0/np.linalg.norm(A0,2))   # start off O(K)
    for t in range(30000):
        m = rng.standard_normal(K); yt = kappa*(P@m) + 0.1*rng.standard_normal(K)
        r = r @ expm(-0.02*Xi(r, m, yt))
    M = r.real
    print("kappa=%.1f  diag(Re r)[:4]=%s  ||Re r on P^perp||=%.3f" % (kappa, np.round(np.diag(M)[:4],2), np.linalg.norm(M[4:,4:],2)))

print("\n== C5: H2 counterexample: real relation, match->counter passes through cross-channel enactment, not holding ==")
L = np.zeros((K,K)); L[0,1]=-np.pi; L[1,0]=np.pi
m = np.zeros(K); m[0]=1
for s in (0,0.25,0.5,0.75,1.0):
    z = expm(s*L) @ m
    print("s=%.2f enacted=%s held_norm=%.2f" % (s, np.round(z[:2],2), 0.0))

print("\n== C6: theorem 3b crossing times ==")
tau=1.2
for th in (np.pi, 2*np.pi/3):
    print(th, tau*np.log(1/(1-np.pi/(2*th))))

print("\n== C7: surprise ratio concentrates at ~1/2 when sigma^2 = running mean of ||e||^2 (K=32) ==")
K2=32; e2 = np.sum(rng.standard_normal((100000,K2))**2,1); sig = e2.mean()
rat = e2/(sig+e2); print("Gaussian errors: mean ratio %.3f sd %.3f" % (rat.mean(), rat.std()))
e2 = np.sum(rng.standard_t(2.5,(100000,K2))**2,1); sig=e2.mean(); rat=e2/(sig+e2)
print("t(2.5) errors : mean ratio %.3f sd %.3f" % (rat.mean(), rat.std()))
for nu0 in (0.25, 0.5, 1, 2, 5):
    s = 1/(1+0.5*nu0*tau)
    print("nu0=%.2f s*=%.2f  enacted share hold-relation cos(pi/2 s*)=%.2f  counter cos(pi s*)=%.2f" % (nu0, s, np.cos(np.pi/2*s), np.cos(np.pi*s)))

print("\n== C8: T1d Hessian formula check at I (random S symmetric) ==")
K=6
Smm = np.eye(K); Bt = rng.standard_normal((K,K)); Smy = 0.4*(Bt+Bt.T)/2 + 0.6*np.eye(K)
Lam = Smm - (Smy+Smy.T)/2
def lbar(r):  # E||Re(r m)-y||^2 with Sigma_mm=I, Sigma_my given, E||y||^2 irrelevant const
    M = r.real; return np.trace(M@Smm@M.T) - 2*np.trace(M@Smy)
B = rng.standard_normal((K,K)); B=B-B.T; A = rng.standard_normal((K,K)); A=A+A.T
X = B+1j*A; eps=1e-3
num = (lbar(expm(eps*X)) - lbar(np.eye(K)))/eps**2
pred = np.trace(B.T@B@((Smy+Smy.T)/2)) - np.trace(A@Lam@A)
print("numeric %.4f  predicted %.4f" % (num, pred))

print("\n== C9: T1c.1: Re r invertible contraction generic (GL frame) ==")
A0 = rng.standard_normal((K,K)); A0=A0+A0.T; B0=rng.standard_normal((K,K)); B0=B0-B0.T
r = expm(B0+0.5j*A0); print("sv(Re r)", np.round(np.linalg.svd(r.real,compute_uv=False),3))
