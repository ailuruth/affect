"""Critic's checks for the isospectral core as a Q35 safety net (numpy only, ~seconds).

Constructions only: each exhibits a concrete mechanism failure on a hand-made 2x2 block (one expression
channel k paired with one internal mode), integrated with exact rotations so the spectrum is preserved to
round-off wherever the design says it is. Not evidence about behaviour or people.
Ceiling metric, as the ledger's: toward slope of the agent's channel on the partner's channel, read on
30-s block means at the copy's lag, divided by c_k.  Run: python3 -I checks.py
"""
import numpy as np

fs, T = 10.0, 3600.0                 # 10 Hz, 1 h
dt, N = 1 / fs, int(3600 * 10)
rng = np.random.default_rng(35)
J = np.array([[0.0, -1.0], [1.0, 0.0]])


def rot(M, ang):
    c, s = np.cos(ang), np.sin(ang)
    R = np.array([[c, -s], [s, c]])
    return R @ M @ R.T


def ou(tau, sd, n):
    x = np.zeros(n); a = np.exp(-dt / tau)
    for t in range(1, n):
        x[t] = a * x[t - 1] + sd * np.sqrt(1 - a * a) * rng.normal()
    return x


def slope(y, p, lag_s, block_s=30.0):
    L = int(lag_s * fs); b = int(block_s * fs)
    yy, pp = y[L:], p[:len(p) - L]
    n = len(yy) // b
    yb = yy[:n * b].reshape(n, b).mean(1); pb = pp[:n * b].reshape(n, b).mean(1)
    pb = pb - pb.mean(); yb = yb - yb.mean()
    return float(yb @ pb / (pb @ pb))


def angle(M):
    w, V = np.linalg.eigh(M)
    v = V[:, 1]                      # top eigenvector
    return np.arctan2(v[1], v[0])


# reserved partner on lid droop: slow OU (tau 60 s), sd 0.08 (inside a 0..1 own range)
p = ou(60.0, 0.08, N)
lam = np.array([1.0, 0.0])           # agent's own range on the block: lid droop 0..1 (body: drowsiness)
c_LD = 0.05                          # innate ceiling toward the partner (engine/config/channels.py)
th0, kappa = np.pi / 8, 0.5          # own resting angle and own locking stiffness


def run(w=-c_LD, own_fb=0.0, fb_lag_s=0.0, unlisted=0.0, un_lag_s=0.0, body_eta=0.0, kappa=kappa):
    """Partner port: angular rate w*p (|w| <= c). own_fb: own rotation that reads the agent's own delayed angle
    (Omega(M(t-L)), an 'own' term by type). unlisted: a partner-derived feature that reached Omega via context
    (the typing violation a net must catch). body_eta: body b follows the agent's own expression (proprioception /
    effort), and the spectral source S drives the top eigenvalue toward a b-set level."""
    M = rot(np.diag(lam), th0)
    lt, ys, lams, ths = lam.copy(), np.empty(N), np.empty(N), np.empty(N)
    b = M[0, 0]
    Lf, Uf = int(fb_lag_s * fs), int(un_lag_s * fs)
    for t in range(N):
        th = angle(M)
        th = th0 + (th - th0 + np.pi / 2) % np.pi - np.pi / 2     # eigenvector sign: angle mod pi
        ths[t] = th
        om = -kappa * np.sin(2 * (th - th0))
        if own_fb:
            om += own_fb * (ths[t - Lf] - th0 if t >= Lf else 0.0)
        if unlisted:
            om += unlisted * (p[t - Uf] if t >= Uf else 0.0)
        om += w * p[t]
        M = rot(M, om * dt)
        if body_eta:
            b += dt / 20.0 * (M[0, 0] - b)                  # body follows own expression (tau 20 s)
            w_, V = np.linalg.eigh(M)
            target = np.array([0.0, 1.0 + body_eta * (b - 0.85)])   # S: top eigenvalue toward body-set level
            w_ = w_ + dt / 30.0 * (target - w_)
            M = V @ np.diag(w_) @ V.T
        ys[t] = M[0, 0]
        lams[t] = np.linalg.eigvalsh(M)[1]
    return ys, lams


def report(name, ys, lams, lags=(0, 60)):
    s = [slope(ys, p, L) for L in lags]
    print(f"  {name:62s} " + "  ".join(f"lag {L:3d}s: {v / c_LD:6.2f} c" for L, v in zip(lags, s))
          + f"   eig range {lams.min():.4f}-{lams.max():.4f}")


print("(sign of w is free by design; w = -c gives the toward sign at theta0 = pi/8)")
print("F0 listed port only, |w| = c, innate kappa: within the ceiling")
report("listed port w=c, kappa 0.5", *run())
print("F1 listed port only, kappa learned smaller (Omega is learned): same |w|, larger slope")
for k in (0.1, 0.02):
    report(f"listed port w=c, kappa {k}", *run(kappa=k))
print("F2 own rotation reading own delayed state (typed 'own'), listed port unchanged |w| = c")
for a, L in ((0.8, 0), (0.9, 60), (0.98, 60)):
    report(f"own feedback a={a} x 2kappa at lag {L}s", *run(own_fb=a * 2 * kappa, fb_lag_s=L))
print("F3 unlisted partner feature in Omega, delayed 60 s (the route the net must catch)")
for u in (0.05, 0.5):
    report(f"unlisted rate {u} on p(t-60s)", *run(unlisted=-u, un_lag_s=60))
print("F4 body follows own expression; spectrum now carries the partner (T1 broken)")
ys, lams = run(body_eta=1.0)
report("body loop eta 1", ys, lams)
print(f"    corr(top eigenvalue, partner) on 30-s blocks: "
      f"{np.corrcoef(lams[:N//300*300].reshape(-1,300).mean(1), p[:N//300*300].reshape(-1,300).mean(1))[0,1]:.2f}")
print("F5 what the spectral budget allows on this channel vs the ceiling")
print(f"    Schur-Horn admits y_LD anywhere in [{lam.min()}, {lam.max()}]; partner block-mean sd "
      f"{p.reshape(-1,300).mean(1).std():.3f}; full-range following = slope "
      f"{(lam.max()-lam.min())/(4*p.reshape(-1,300).mean(1).std())/c_LD:.0f} c (range/4 sd)")
print("F6 fast mimicry from internal rest (theta0 = 0): first-order leverage 0 (D81 needs it)")
th0_save = th0; th0 = 0.0
ys, lams = run()
print(f"    lag 0 slope at rest angle 0: {slope(ys, p, 0) / c_LD:.3f} c"); th0 = th0_save
