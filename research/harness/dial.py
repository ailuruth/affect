"""Dial analysis, v2 (fixes REVIEW-1 B4, B5; adds own-lag controls; generic condition labels). The project's own
analysis; no accepted benchmark exists. Fixed before any data beyond the one local sample pair was seen.

Question: across conditions (familiar vs stranger; or repeat vs first meeting), does a listener's response to the
partner change only in gain (one dial) or also in profile?

Per interaction and direction (listener L, speaker S), on rows whose frames t-30..t are valid for BOTH people:
  partner features  X_t = mean of z(S) over lags 1-10, 11-20, 21-30 (69)
  own-lag controls  C_t = mean of z(L) over lags 1-10, 11-20, 21-30 (69)   (Granger-style; REVIEW-1 note)
  target            Y_t = z(L_t); z-statistics from jointly valid frames only; X, C, Y centred on kept rows.
  [B_x; B_c] = ridge([X C], Y, lam = LAM * n / 1000); gain g = ||B_x||_F (SD units), profile P = B_x / g.
Aggregation: P and log g are averaged per SESSION (all of a listener's interactions in one session share a partner).
Test, within person, at the session level (REVIEW-1 B4):
  persons with >= 1 session in each condition and >= 3 sessions in total (permutation group non-trivial);
  D_profile = mean over persons of || mean_sessions P(c1) - mean_sessions P(c2) ||_F ; D_gain likewise on log g;
  null: permute session condition labels within each person, 1000 times, seed 0.
Persons with exactly one session per condition carry no permutation information; they are reported descriptively.
Partner identity is confounded with condition (each session has one partner)."""
import numpy as np
LAGBINS = ((1, 10), (11, 20), (21, 30)); LAM = 100.0; MAXLAG = 30

def _lagbins(z, T):
    cs = np.concatenate([np.zeros((1, z.shape[1])), np.cumsum(z, 0)]); t = np.arange(MAXLAG, T)
    return np.concatenate([(cs[t - a + 1] - cs[t - b]) / (b - a + 1) for a, b in LAGBINS], 1)

def design(lis, spk, valid_l, valid_s):
    T = min(len(lis), len(spk)); lis, spk = lis[:T].astype(float), spk[:T].astype(float)
    ok = np.asarray(valid_l[:T], bool) & np.asarray(valid_s[:T], bool)
    def z(a):
        m, s = a[ok].mean(0), a[ok].std(0); s[s == 0] = 1; return (a - m) / s
    zl, zs = z(lis), z(spk)
    X, C, Y = _lagbins(zs, T), _lagbins(zl, T), zl[MAXLAG:]
    bad = np.concatenate([[0], np.cumsum(~ok)]); t = np.arange(MAXLAG, T)
    keep = (bad[t + 1] - bad[t - MAXLAG]) == 0
    X, C, Y = X[keep], C[keep], Y[keep]
    return X - X.mean(0), C - C.mean(0), Y - Y.mean(0)

def response(lis, spk, valid_l, valid_s, lam=LAM):
    X, C, Y = design(lis, spk, valid_l, valid_s)
    if len(X) < 500: return None  # same minimum length as E3
    Z = np.concatenate([X, C], 1)
    B = np.linalg.solve(Z.T @ Z + lam * len(Z) / 1000 * np.eye(Z.shape[1]), Z.T @ Y)[:X.shape[1]]
    g = float(np.linalg.norm(B)); return g, B / g

def within_person_test(records, conds=("familiar", "stranger"), n_perm=1000, seed=0):
    """records: (person, session, condition, g, P) per interaction-direction. Returns stats, p-values and counts."""
    c1, c2 = conds; sess = {}
    for p, s, c, g, P in records:
        if c in conds: sess.setdefault((p, s, c), []).append((np.log(g), P))
    by = {}
    for (p, s, c), v in sess.items():
        by.setdefault(p, []).append((c, np.mean([x[0] for x in v]), np.mean([x[1] for x in v], 0)))
    both = {p: v for p, v in by.items() if {c for c, _, _ in v} >= {c1, c2}}
    testable = {p: v for p, v in both.items() if len(v) >= 3}
    one_one = len(both) - len(testable)
    def stats(lab, group):
        dp, dg = [], []
        for p, v in group.items():
            L = lab[p]; I1 = [i for i, c in enumerate(L) if c == c1]; I2 = [i for i, c in enumerate(L) if c == c2]
            Pm = lambda I: np.mean([v[i][2] for i in I], 0); gm = lambda I: np.mean([v[i][1] for i in I])
            dp.append(np.linalg.norm(Pm(I1) - Pm(I2))); dg.append(abs(gm(I1) - gm(I2)))
        return float(np.mean(dp)), float(np.mean(dg))
    out = dict(n_persons_both=len(both), n_testable=len(testable), n_one_session_each=one_one)
    if one_one: out["descriptive_one_one"] = stats({p: [c for c, _, _ in v] for p, v in both.items() if len(v) < 3},
                                                  {p: v for p, v in both.items() if len(v) < 3})
    if not testable: out["warning"] = "no person with a non-trivial permutation group"; return out
    lab = {p: [c for c, _, _ in v] for p, v in testable.items()}; obs = stats(lab, testable)
    rng = np.random.default_rng(seed)
    null = np.array([stats({p: list(rng.permutation(L)) for p, L in lab.items()}, testable) for _ in range(n_perm)])
    out.update(D_profile=obs[0], p_profile=float((1 + (null[:, 0] >= obs[0]).sum()) / (n_perm + 1)),
               D_gain=obs[1], p_gain=float((1 + (null[:, 1] >= obs[1]).sum()) / (n_perm + 1)))
    return out
