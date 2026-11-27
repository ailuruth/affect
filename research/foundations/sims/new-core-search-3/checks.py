"""Algebra checks for research/new-core-search-3-synthesis.md (numpy only).

These verify only the mathematics stated in the synthesis, on hand-made
instances. They are not evidence about behaviour or about people.
Run: python3 -I checks.py
"""
import numpy as np

rng = np.random.default_rng(0)


def expm_skew(A):
    # exact exponential of a real antisymmetric matrix via eigh of A^T A trick
    w, V = np.linalg.eig(A)
    return (V @ np.diag(np.exp(w)) @ np.linalg.inv(V)).real


def rot(M, X, h):
    U = expm_skew(h * X)
    return U @ M @ U.T


def sym(A):
    return 0.5 * (A + A.T)


def skew(A):
    return 0.5 * (A - A.T)


n, m = 6, 3
def E(i, j):
    Z = np.zeros((n, n)); Z[i, j] = 1.0; return Z

# block generators: expression channel k paired with internal mode k+m
A_block = [E(k, k + m) - E(k + m, k) for k in range(m)]
# mixed generators: rotations among the expression channels themselves
A_mix = [E(k, (k + 1) % m) - E((k + 1) % m, k) for k in range(m)]

print("S1  partner port is isospectral and trace-preserving for any weights/signals")
M = sym(rng.normal(size=(n, n)))
lam0 = np.sort(np.linalg.eigvalsh(M))
for t in range(2000):
    p = rng.normal(size=m) * 5
    w = rng.uniform(-3, 3, size=m) * np.tanh(M[0, 1])  # state-dependent, sign-flipping
    X = sum(w[k] * p[k] * (A_block[k] + A_mix[k]) for k in range(m))
    M = rot(M, X, 0.01)
lam1 = np.sort(np.linalg.eigvalsh(M))
print("    max |eig change| =", np.abs(lam1 - lam0).max())

print("S2  Schur-Horn: diagonal stays in the permutohedron (check top-j partial sums)")
d = np.sort(np.diag(M))[::-1]; l = lam1[::-1]
print("    partial sums diag <= eig:", all(np.cumsum(d)[j] <= np.cumsum(l)[j] + 1e-9 for j in range(n)),
      " trace equal:", np.isclose(d.sum(), l.sum()))

print("S3  leverage at rest: if M is diagonal, d diag/dt from any partner X is 0")
M = np.diag(rng.normal(size=n))
X = skew(rng.normal(size=(n, n)))
print("    |d diag| =", np.abs(np.diag(X @ M - M @ X)).max())

print("S4  Larmor (so(3)): uniform weights conserve the overlap <mu,P>; per-expression weights do not")
# overlap for coadjoint form: use generic Lie-algebra form on so(3) as in the text
def hat(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
mu = rng.normal(size=3); P = rng.normal(size=3)
for wts in ([1.0, 1.0, 1.0], [1.0, 0.3, -0.5]):
    X = np.array(wts) * P      # X = sum_k w_k p_k e_k
    dmu = np.cross(mu, X)      # Lie-Poisson on so(3)*: mu_dot = mu x X
    print("    weights", wts, " d<mu,P>/dt =", round(float(dmu @ P), 6))

print("S5  fast partner rotation + own damping: does the agent copy the partner's sign?")
def run(gens, wgain, theta0, pconst, T=60.0, h=0.002, gamma=1.0):
    lam = np.array([3.0, 2.5, 2.0, 0.0, 0.2, 0.4])
    M = np.diag(lam)
    # own target N: diagonal target rotated by theta0 in each block -> own resting angle
    R = np.eye(n)
    for k in range(m):
        c, s = np.cos(theta0), np.sin(theta0)
        R[k, k] = c; R[k, k + m] = -s; R[k + m, k] = s; R[k + m, k + m] = c
    N = R @ np.diag(lam) @ R.T
    ys = []
    for i in range(int(T / h)):
        X = sum(wgain * pconst[k] * gens[k] for k in range(m))
        B = M @ N - N @ M                    # double bracket: M_dot = [[M,N],M]... sign below
        Xd = -gamma * B                     # M_dot = [Xd, M] with Xd = -gamma[M,N]  -> gradient toward N
        M = rot(M, X + Xd, h)
        if i * h > T / 2:
            ys.append(np.diag(M)[:m].copy())
    return np.mean(ys, axis=0)

base0 = run(A_block, 0.0, 0.0, np.zeros(m))
for th in (0.0, np.pi / 8):
    base = run(A_block, 0.0, th, np.zeros(m))
    up = run(A_block, 1.0, th, np.array([1.0, 0.0, 0.0]) )
    dn = run(A_block, 1.0, th, np.array([-1.0, 0.0, 0.0]))
    print(f"    block, own angle {th:.3f}: y1 rest {base[0]:.3f}, partner +1 -> {up[0]:.3f}, partner -1 -> {dn[0]:.3f}")
for wg in (0.5, 2.0, 8.0):
    up = run(A_block, wg, np.pi / 8, np.array([1.0, 0, 0]))
    print(f"    block, own angle pi/8, gain {wg}: y1 = {up[0]:.3f}  (range of block 1: [0.000, 3.000])")
# mixed generators: partner channel 1 rotates expression channels 1<->2
for sgn in (+1, -1):
    y = run(A_mix, 4.0, 0.0, sgn * np.array([1.0, 0, 0]))
    print(f"    mixed, partner ch1 {sgn:+d}: y = {np.round(y,3)} (rest {np.round(base0,3)})")

print("S6  Gelfand-Tsetlin: a rotation inside the leading j modes keeps the spectra of every")
print("    leading k x k submatrix with k >= j; Cauchy interlacing bounds the j-level ones")
M = sym(rng.normal(size=(n, n)))
j = 2
Xj = np.zeros((n, n)); Xj[:j, :j] = skew(rng.normal(size=(j, j)))
M2 = rot(M, Xj, 0.7)
for k in range(1, n + 1):
    a = np.linalg.eigvalsh(M[:k, :k]); b = np.linalg.eigvalsh(M2[:k, :k])
    print(f"    k={k}: spectrum change {np.abs(a-b).max():.2e}")
l2 = np.linalg.eigvalsh(M2[:2, :2]); l1 = M2[0, 0]
print("    M11 within [eig_min, eig_max] of leading 2x2:", l2[0] - 1e-12 <= l1 <= l2[1] + 1e-12)

print("S7  pair orbit: Q = (U^T V)o(U^T V) is doubly stochastic, invariant under joint")
print("    conjugation, and tr(MP) = lam^T Q gam (von Neumann bound at a sorted permutation)")
M = sym(rng.normal(size=(n, n))); P = sym(rng.normal(size=(n, n)))
lam, U = np.linalg.eigh(M); gam, V = np.linalg.eigh(P)
Q = (U.T @ V) ** 2
W = expm_skew(skew(rng.normal(size=(n, n))))
lam2, U2 = np.linalg.eigh(W @ M @ W.T); gam2, V2 = np.linalg.eigh(W @ P @ W.T)
Q2 = (U2.T @ V2) ** 2
print("    rows/cols sum to 1:", np.allclose(Q.sum(0), 1), np.allclose(Q.sum(1), 1),
      " joint-conjugation invariant:", np.allclose(Q, Q2, atol=1e-8))
print("    tr(MP) =", round(np.trace(M @ P), 6), " lam^T Q gam =", round(lam @ Q @ gam, 6),
      " bound sum lam_i gam_i (sorted) =", round(np.sort(lam) @ np.sort(gam), 6))
# copy in a frame: P = R M R^T with R commuting... simplest: P = M -> Q = identity
lam, U = np.linalg.eigh(M); Q3 = (U.T @ U) ** 2
print("    copy (P = M): Q is the identity permutation:", np.allclose(Q3, np.eye(n)))
