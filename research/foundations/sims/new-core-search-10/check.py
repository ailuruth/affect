"""Pass 10 check: does a certified incremental l2 gain on a learned route imply the
ledger's block-mean slope bound?  A check of the algebra on synthetic signals only.
It is NOT evidence about people, behaviour or the engine.

Run: python3 -I check.py > out.txt   (numpy only, about 3-5 min)

Setting (all at 1 Hz):
  his counterpart p_t in [0,1], neutral input u0 (constant, != his mean),
  partner deviation d_t = p_t - u0, prefilter F (innate, linear), e = F d,
  a learned route certified by construction:  ||Dy||_win^2 <= g^2 (||De||_win^2
      + sum_{k<s} abar^{2(s-1-k)} |De_k|^2)      (windowed form of a robust REN bound)
  metric: block means (b = 10 s) over the last W = 1200 s, slope of the partner-caused
      part on his centred block means at lags 0..300 s, floor sigma0 = 0.03.
Part A: the amplification factor Phi(F) = sup over admissible paths of
      sqrt(numerator energy) / (sqrt(b) max(||P~||, sqrt(N) sigma0)), bounded above by a
      generalised eigenvalue (box relaxed to a ball; factor sqrt 2 from the max).
      A feasible path built from the top eigenvector gives a lower estimate.
Part C: a lag-aimed, non-stationary partner against a plain linear copy (no learning).
Part B: toy certified routes (contracting, 1-Lipschitz stages, gain <= 1 by
      construction) driven by aimed and natural partners; measured worst slope / c.
"""
import numpy as np

rng = np.random.default_rng(10)
T, W, b, s0 = 3600, 1200, 10, 0.03
s = T - W
N = W // b
u0 = 0.30
amax = max(u0, 1 - u0)
LAGS = list(range(0, 301, 10))


def lp(x, tau):
    a = np.exp(-1.0 / tau)
    y = np.zeros_like(x)
    acc = 0.0
    for t in range(len(x)):
        acc = a * acc + (1 - a) * x[t]
        y[t] = acc
    return y


def filt_matrix(kind):
    I = np.eye(T)
    if kind == "identity":
        return I
    cols = []
    for j in range(T):
        x = I[:, j]
        if kind == "LP10":
            y = lp(x, 10.0)
        elif kind == "BP10-120":
            y = lp(x, 10.0) - lp(x, 120.0)
        elif kind == "BP10-600":
            y = lp(x, 10.0) - lp(x, 600.0)
        cols.append(y)
    return np.array(cols).T


def blockmean_centred(L):
    """C_L: maps the full path d (length T) to centred block means of d(t-L) over the window."""
    C = np.zeros((N, T))
    for n in range(N):
        t0 = s + n * b - L
        C[n, t0:t0 + b] = 1.0 / b
    C = C - C.mean(axis=0, keepdims=True)
    return C


def numerator_weights(tau_mem):
    abar = np.exp(-1.0 / tau_mem)
    w = np.ones(T)
    k = np.arange(s)
    w[:s] = abar ** (s - 1 - k)
    return w


def phi(F, tau_mem, L, cross=False):
    w = numerator_weights(tau_mem)
    A = w[:, None] * F
    M = A.T @ A
    eps = N * s0 ** 2 / (T * amax ** 2)
    if cross:
        # his other channel q drives the route; the metric's regressor is his counterpart,
        # which he holds at the floor: denominator = sqrt(b N) s0, numerator sup over box.
        ev = np.linalg.eigvalsh(M)[-1]
        return np.sqrt(ev * T * amax ** 2) / (np.sqrt(b * N) * s0), None
    C = blockmean_centred(L)
    B = b * (C.T @ C) + b * eps * np.eye(T)
    # generalised eigenproblem M v = lam B v ; B is positive definite
    Lc = np.linalg.cholesky(B)
    Li = np.linalg.inv(Lc)
    S = Li @ M @ Li.T
    lam, V = np.linalg.eigh(S)
    up = np.sqrt(2 * lam[-1])
    v = Li.T @ V[:, -1]
    v = v / np.max(np.abs(v)) * amax * 0.999           # feasible path in the box
    num = np.linalg.norm(A @ v)
    den = np.sqrt(b) * max(np.linalg.norm(C @ v), np.sqrt(N) * s0)
    return up, num / den


def slope_worst(D, p, lags=LAGS, windows=None):
    """worst block-mean slope of partner-caused part D on his counterpart p, over lags and windows."""
    if windows is None:
        windows = [(s, T)]
    worst = 0.0
    for (a, e) in windows:
        n = (e - a) // b
        Db = D[a:a + n * b].reshape(n, b).mean(1)
        Db = Db - Db.mean()
        for L in lags:
            if a - L < 0:
                continue
            Pb = p[a - L:a - L + n * b].reshape(n, b).mean(1)
            Pb = Pb - Pb.mean()
            beta = (Db @ Pb) / n / max(Pb.var(), s0 ** 2)
            worst = max(worst, abs(beta))
    return worst


def certified_chain(e, taus):
    """cascade of one-pole stages x <- a x + (1-a) phi(input); each stage has l2 gain <= 1
    (kernel l1 norm = 1, phi 1-Lipschitz). Returns the last stage."""
    x = e
    for tau in taus:
        x = lp(x, tau)
    return x


def run_partner(kind):
    t = np.arange(T)
    if kind == "natural":       # OU around his mean 0.44 (u0 = 0.30 is not his mean)
        z = np.zeros(T); x = 0.0
        for i in range(T):
            x += -x / 60.0 + 0.012 * rng.standard_normal(); z[i] = x
        return np.clip(0.44 + z, 0, 1)
    if kind == "aimed-floor":   # block levels alternate by +-s0 every 60 s around 0.44
        return 0.44 + s0 * np.sign(np.sin(2 * np.pi * t / 120.0 + 0.1))
    if kind == "wiggle":        # constant block means; 2-s wiggle on in alternate 60-s blocks
        on = (np.floor(t / 60.0) % 2 == 0).astype(float)
        return 0.44 + 0.25 * on * np.sign(np.sin(2 * np.pi * t / 2.0 + 0.3)) + s0 * (2 * on - 1)
    raise ValueError(kind)


def main():
    np.set_printoptions(precision=3, suppress=True)
    print("PART A  amplification factor Phi (upper bound | feasible lower estimate)")
    print("  F           tau_mem  L=0            L=120          L=300")
    for kind in ["identity", "LP10", "BP10-120", "BP10-600"]:
        F = filt_matrix(kind)
        for tau in [60.0, 300.0]:
            row = []
            for L in [0, 120, 300]:
                up, lo = phi(F, tau, L)
                row.append(f"{up:6.2f} | {lo:5.2f}")
            print(f"  {kind:10s}  {tau:5.0f}   " + "   ".join(row))
    for kind in ["LP10", "BP10-120"]:
        F = filt_matrix(kind)
        up, _ = phi(F, 60.0, 0, cross=True)
        print(f"  cross-channel input, {kind}, tau_mem 60: Phi_cross <= {up:6.2f} (floor-only denominator)")

    print("\nPART B  toy certified routes, gain g = c (so the bound reads Phi * c); worst slope / c")
    print("        lags 0..300 s; final 20-min window and all 20-min windows every 5 min")
    wins = [(a, a + W) for a in range(600, T - W + 1, 300)]
    c = 0.05
    sched_on = ((np.arange(T) % 1800) < 360).astype(float)          # 6 min on, 24 off
    ramp = np.linspace(0, 1, T)                                      # own-context ramp
    for pk in ["natural", "aimed-floor", "wiggle"]:
        p = run_partner(pk)
        d = p - u0
        print(f"  partner: {pk}")
        for fk in ["identity", "LP10", "BP10-120"]:
            if fk == "identity":
                e = d
            elif fk == "LP10":
                e = lp(d, 10.0)
            else:
                e = lp(d, 10.0) - lp(d, 120.0)
            routes = {
                "copy (1 stage, 5 s)": certified_chain(e, [5.0]),
                "slow copy (12 x 10 s, ~120 s late)": certified_chain(e, [10.0] * 12),
                "envelope |e| (demodulator)": lp(np.abs(e), 20.0),
                "switched copy 6/24 min": sched_on * certified_chain(e, [5.0]),
                "growing copy (own ramp 0..1)": ramp * certified_chain(e, [5.0]),
                "sign by block parity (own ctx)": np.sign(np.sin(2 * np.pi * np.arange(T) / 120.0 + 0.1)) * certified_chain(e, [5.0]),
            }
            for name, h in routes.items():
                D = c * h
                r_final = slope_worst(D, p) / c
                r_all = slope_worst(D, p, windows=wins) / c
                print(f"    F={fk:9s} {name:36s} final {r_final:6.2f}   any window {r_all:6.2f}")


if __name__ == "__main__":
    main()


def part_c(PB=10):
    globals()["PB"]=PB
    """Lag-aimed, non-stationary partner against a plain LTI copy (no learning, no
    nonlinearity): he is flat except a +-s0 block pattern in [T-2L, T-L] and the same
    pattern at amplitude A in [T-L, T].  The slope at lag L in the final window then reads
    about g * (L/W) * (A/s0) whatever the route's nonlinearity."""
    print(f"\nPART C (pattern blocks {PB} s)  lag-aimed partner vs a plain copy of gain g = 0.5 c (worst slope / c, final window)")
    c = 0.05
    for L in [60, 120, 300]:
        for A in [0.10, 0.30]:
            p = np.full(T, 0.44)
            pat = np.repeat(np.sign(np.sin(np.arange(L // PB) * 2.1 + 0.4)), PB)
            p[T - 2 * L:T - L] += s0 * pat
            p[T - L:] += A * pat
            d = p - u0
            for fk in ["identity", "BP10-120"]:
                e = d if fk == "identity" else lp(d, 10.0) - lp(d, 120.0)
                D = 0.5 * c * lp(e, 1.0)
                r = slope_worst(D, p, lags=[L]) / c
                pred = 0.5 * (L / W) * (A / s0)
                print(f"    L={L:3d} s  A={A:.2f}  F={fk:9s}  slope/c {r:6.2f}   g(L/W)(A/s0)/c = {pred:5.2f}")


if __name__ == "__main__":
    part_c(10)
    part_c(60)
