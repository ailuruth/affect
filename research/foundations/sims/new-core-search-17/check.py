"""Pass-17 critique checks of the pass-16 replay proposals (research/new-core-search-16-synthesis.md §9).

numpy only. Run: python3 -I -B check.py > out.txt (about 1 s).
These are algebra checks on synthetic signals. They are NOT evidence about people, about behaviour, or about the
engine as built; the engine's code was read, not run, for every claim about the code.
"""
import numpy as np

np.set_printoptions(precision=4, suppress=True)
rng = np.random.default_rng(17)


def head(s):
    print("\n" + "=" * 8 + " " + s)


# ---------------------------------------------------------------- C1 shares and 30-night totals
head("C1 share of the weighted loss, and 30-night totals")
for p in (0.02, 0.05, 0.10, 0.20):
    print(f"p = {p:.2f}: share 4p/(1+3p) = {4 * p / (1 + 3 * p):.4f}")
c = np.arange(30)
w_R = 1 + 3 / (1 + c / 3)
print("Change R nightly weights at nights 1,2,4,8,15,30:", w_R[[0, 1, 3, 7, 14, 29]])
print(f"totals over 30 nights: kappa {4 * 30}, Change R {w_R.sum():.3f}, uniform 30;"
      f" ratio R/uniform {w_R.sum() / 30:.3f}")
print("BUT as built (engine/memory/replay.py loads only sessions not yet replayed, then marks them):"
      " every moment is replayed once, so c_k = 0 always and gamma = 1: totals kappa 4, Change R 1 + 3 s u, uniform 1")
# influence of night-n gradient on the parameters after the window, with the per-night contraction of the pull
lr, steps, lam = 0.05, 200, 0.1
rho = (1 - lr * lam) ** steps
print(f"per-night contraction of the theta_0 pull alone: (1 - lr*lam)^steps = {rho:.4f}"
      " (so a sum of weights over nights is not a sum of influence: night n's step is shrunk by rho^(30-n))")
infl_k = sum(4 * rho ** (29 - n) for n in range(30))
infl_R = sum(w_R[n] * rho ** (29 - n) for n in range(30))
infl_u = sum(1 * rho ** (29 - n) for n in range(30))
print(f"pull-discounted influence at night 30 (whole-window replay): kappa {infl_k:.3f}, Change R {infl_R:.3f},"
      f" uniform {infl_u:.3f}; ratio kappa/uniform {infl_k / infl_u:.2f}, R/uniform {infl_R / infl_u:.2f}")

# ---------------------------------------------------------------- C2 stationary spread under the pull
head("C2 stationary spread of theta under theta <- theta - eta (clip(g) + lam (theta - theta0))")
eta, lam, sig = 0.05, 0.1, 1.0
T = 200_000
e, xs = 0.0, []
for t in range(T):
    g = sig * rng.standard_normal()
    e = e - eta * (g + lam * e)
    if t > 5000:
        xs.append(e)
print(f"i.i.d. noise per step: simulated var {np.var(xs):.4f}, eta sig^2/(2 lam) = {eta * sig ** 2 / (2 * lam):.4f},"
      f" exact eta sig^2/(lam (2 - eta lam)) = {eta * sig ** 2 / (lam * (2 - eta * lam)):.4f}")
# per-night noise: the same full-batch gradient for all 200 steps of a night (the code's _descend)
nights, e, xs = 20_000, 0.0, []
for n in range(nights):
    g = sig * rng.standard_normal()
    for _ in range(steps):
        e = e - eta * (g + lam * e)
    if n > 100:
        xs.append(e)
r = (1 - eta * lam) ** steps
pred = (sig / lam) ** 2 * (1 - r) / (1 + r)
print(f"noise fixed within a night (200 full-batch steps): simulated var {np.var(xs):.4f};"
      f" AR(1) prediction (sig/lam)^2 (1-r)/(1+r) = {pred:.4f}; eta sig^2/(2 lam) = {eta * sig ** 2 / (2 * lam):.4f}")
print(f"deterministic bound with clip norm 1: |theta - theta0| <= clip/lam = {1 / lam:.1f} per parameter group")

# ---------------------------------------------------------------- C3 endogenous weight bias in a reader
head("C3 reader fitted with a weight that is a function of its own target (H_id-like)")
n = 20000
x = rng.standard_normal((n, 3))
beta = np.array([0.10, 0.05, 0.0])
y = np.clip(0.12 + x @ beta + 0.08 * rng.standard_normal(n), 0, 1)       # V-like target, mostly low
Dp = 0.8 * np.maximum(y - 0.05, 0) ** 2
w = 1 + 3 * np.minimum(1, Dp / 0.05)


def ridge(X, Y, W, lam):
    Xa = np.c_[X, np.ones(len(X))]
    A = Xa.T @ (W[:, None] * Xa) / W.sum() + lam * np.diag([1, 1, 1, 0]) / len(X)
    return np.linalg.solve(A, Xa.T @ (W * Y) / W.sum())


b_u = ridge(x, y, np.ones(n), 2.0)
b_w = ridge(x, y, w, 2.0)
b_is = ridge(x, y, w * (1 / w) / np.mean(1 / w), 2.0)
lo = np.abs(x @ beta) < 0.05
print(f"share of moments at full weight {np.mean(w > 3.999):.3f}; weighted share {np.sum(w[w > 3.999]) / w.sum():.3f}")
print("unweighted fit (slopes, intercept):", b_u)
print("S48-weighted fit                  :", b_w)
print("weighted then 1/w importance-corr.:", b_is, "(identical to unweighted: full-batch, no sampling)")
print(f"mean read V on ordinary moments: unweighted {np.mean(np.c_[x[lo], np.ones(lo.sum())] @ b_u):.4f},"
      f" weighted {np.mean(np.c_[x[lo], np.ones(lo.sum())] @ b_w):.4f}, true {np.mean(y[lo]):.4f}")

# ---------------------------------------------------------------- C4 Change R's need term and session length
head("C4 u = 0.25 + 0.75 x fraction of his last 7 sessions in which the topic was addressed")
p_topic = 1 / 16
for m in (5, 10, 25, 50, 100, 200):
    q = 1 - (1 - p_topic) ** m
    print(f"{m:4d} utterances per session, same topic mix: P(addressed in a session) = {q:.3f}, E[u] = {0.25 + 0.75 * q:.3f}")
print("length-invariant variant: u = 0.25 + 0.75 min(1, share of his last 200 utterances on the topic / s_ref);"
      " it depends on the topic mix only, not on how long or how often he stays")

# ---------------------------------------------------------------- C5 Pi-tilde / Delta co-adaptation and the anchor
head("C5 linear Pi-tilde / Delta alternation, with and without the Pi_0 data anchor")
m, k = 10, 3
P0 = rng.standard_normal((m, k)) * 0.5                       # innate rows: state (3) -> face (10)
U, _, _ = np.linalg.svd(P0, full_matrices=True)
Pspan, Pperp = U[:, :k] @ U[:, :k].T, U[:, k:] @ U[:, k:].T
W0 = np.linalg.pinv(P0)                                     # Pi-tilde_0 (3 x 10)


def run(alpha, nights=60, lam=0.1, noise_span=0.6, noise_perp=0.05):
    W, D = W0.copy(), np.zeros((m, k))
    S_anchor = np.eye(k) * 0.5
    F_anchor = (P0 @ S_anchor.T).T
    for _ in range(nights):
        s = np.abs(rng.standard_normal((400, k))) * 0.3
        z = s + 0.05 * rng.standard_normal(s.shape)           # Delta's T inputs carry the state
        nz = noise_span * rng.standard_normal((400, m)) @ Pspan + noise_perp * rng.standard_normal((400, m)) @ Pperp
        F = s @ P0.T + z @ D.T + nz                           # the observed own face
        # step 2: Pi-tilde by ridge to W0, with an optional anchor share alpha of the loss
        A = (1 - alpha) * F.T @ F / len(F) + alpha * F_anchor.T @ F_anchor / k + lam * np.eye(m)
        B = (1 - alpha) * s.T @ F / len(F) + alpha * S_anchor.T @ F_anchor / k + lam * W0
        W = np.linalg.solve(A, B.T).T
        # step 5: Delta so that W (base + D z) matches s, ridge to 0
        base = s @ P0.T + nz
        R = s - base @ W.T                                     # residual Delta must explain: R ~ (W D) z
        Z = z
        WD = np.linalg.solve(Z.T @ Z / len(Z) + lam * np.eye(k), Z.T @ R / len(Z)).T
        D = np.linalg.pinv(W) @ WD
    return W, D


for alpha in (0.0, 0.25, 0.5):
    W, D = run(alpha)
    on = np.linalg.norm(W @ P0 - np.eye(k))
    perp = np.linalg.norm(W @ Pperp)
    his = rng.standard_normal((2000, m)) * 0.3                 # his face: energy in every direction
    drift_his = np.mean(np.abs((his @ (W - W0).T)))
    print(f"anchor share {alpha:.2f}: |W P0 - I| = {on:.3f} (on Pi_0's span), |W P_perp| = {perp:.3f},"
          f" mean |reading of his face - newborn reading| = {drift_his:.3f}")
print("(in this linear toy the drift is mostly on the span, from the noisy own face (errors in variables),"
      " not a private off-span code; the anchor reduces it but does not remove it at 0.25)")

# what the anchor does off the span, exactly: anchor faces lie in span(Pi_0), so off the span it acts only by
# down-weighting the own data, i.e. as a stronger pull lam/(1 - alpha) toward W0
s = np.abs(rng.standard_normal((4000, k))) * 0.3
F = s @ P0.T + 0.3 * rng.standard_normal((4000, m)) @ Pperp     # own data with energy off the span only
F = F + 0.2 * rng.standard_normal((4000, m)) @ Pspan
S_a = np.eye(k) * 0.5
F_a = (P0 @ S_a.T).T
lam = 0.1
for alpha in (0.25, 0.5):
    A = (1 - alpha) * F.T @ F / len(F) + alpha * F_a.T @ F_a / k + lam * np.eye(m)
    B = (1 - alpha) * s.T @ F / len(F) + alpha * S_a.T @ F_a / k + lam * W0
    Wa = np.linalg.solve(A, B.T).T
    A2 = F.T @ F / len(F) + lam / (1 - alpha) * np.eye(m)
    B2 = s.T @ F / len(F) + lam / (1 - alpha) * W0
    Wb = np.linalg.solve(A2, B2.T).T
    print(f"alpha {alpha}: off-span weights with the anchor {np.linalg.norm(Wa @ Pperp):.4f};"
          f" without it at pull lam/(1-alpha) = {lam / (1 - alpha):.3f}: {np.linalg.norm(Wb @ Pperp):.4f};"
          f" no anchor, pull lam: {np.linalg.norm(np.linalg.solve(F.T @ F / len(F) + lam * np.eye(m), (s.T @ F / len(F) + lam * W0).T).T @ Pperp):.4f}")
print("reading: off the span the anchor is worth a pull of lam/(1 - alpha) (x1.33 at a quarter share), nothing more;"
      " on the span it pins Pi-tilde toward the innate inverse with weight alpha")
