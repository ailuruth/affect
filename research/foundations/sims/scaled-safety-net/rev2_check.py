"""Check of the mathematics of design-scaled-safety-net.md, Revision 2 (synthetic signals; NOT evidence about people or
behaviour). numpy only (plus the standard library's process pool, 4 workers).

Usage: python3 -I rev2_check.py > rev2_check.out.txt     (about 10-12 min on 4 cores)

Every run uses an ENGINE-LIKE neutral input u0 = b_id (rev2_lib.engine_baseline: the 6-session exponential average of
earlier session means of the same synthetic partner), never his session mean, except where a section says otherwise.
Sections:
  R1  F22's scenario (gain-1 copy on every channel, delays 10-300 s), causal, u0 = b_id; and as tests/ builds it
  R2  the original scenarios and the critique's counterexamples, at c = 0.03, 0.05, 0.10, 0.35 and g/c = 1.5, 3, 10,
      33: worst residual per ceiling per scenario (session metric), a running metric (20-min windows from 10 min on),
      the effective gain a(t) g(t) at the end of the growth routes, and the theorem's constants
  R3  copies near the target on top of the counted routes (seed 8)
  R4  counted routes running high (an extreme but legal partner)
  R5  false engagement: the 8 synthetic partners of test_counted_routes_untouched (seeds 7-14; 30 min and 1 h), the
      critique's K6 stress cases (u0 = session mean -/+ 0.10), and 8 held-out partners (seeds 15-22, 1 h)
  R6  the unchanged ledger's own F1 rate (the test's exact recipe), and a ledger evidence-floor variant
  R7  Lemma 0 for revision 2 (exact homogeneity)
"""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rev2_lib import (np, FS, lp, delay, wbs, partner, partners_fast, engine_baseline, run2, causal_copy,  # noqa: E402
                      counted_routes, Governor2, GOV2, LedgerE0, Ledger, ledger_only, CEIL, GAIN, SIGNED, CODES, CAPPED)

T = int(3600 * FS)
TT = np.arange(T) / FS
KG = GOV2["kappa_g"]; Z = GOV2["z"]
CS = (0.03, 0.05, 0.10, 0.35)
GR = (1.5, 3.0, 10.0, 33.0)
E0 = 0.54   # ledger evidence floor variant: one minute (600 frames) of his movement at the metric's floor 0.03
DELAYS = (10, 20, 40, 60, 90, 120, 150, 180, 210, 240, 270, 300)


def hp(v, tau):
    return v - lp(v[:, None], tau)[:, 0]


def lobe(u, u0, D):
    v = u - u0; e = v - lp(v[:, None], 4.0)[:, 0]
    return causal_copy(np.maximum(e, 0) + lp(v[:, None], 60.0)[:, 0] + u0, D, u0)


SCEN = [  # (name, route(u, u0) with gain 1, onset s)
    ("copy, delay 90 s (on grid)", lambda u, u0: causal_copy(u, 90.0, u0), 90.0),
    ("copy, delay 47.35 s (off grid)", lambda u, u0: causal_copy(u, 47.35, u0), 47.35),
    ("copy, delay 213.7 s (off grid)", lambda u, u0: causal_copy(u, 213.7, u0), 213.7),
    ("copy low-passed 30 s, delay 120 s", lambda u, u0: lp(causal_copy(u, 120.0, u0)[:, None], 30.0)[:, 0], 120.0),
    ("spec F22 shape (onset lobe + 60-s lp), 120 s", lambda u, u0: lobe(u, u0, 120.0), 120.0),
    ("copy low-passed 120 s, delay 90 s [K3]", lambda u, u0: lp(causal_copy(u, 90.0, u0)[:, None], 120.0)[:, 0], 90.0),
    ("copy low-passed 300 s, delay 90 s [K3]", lambda u, u0: lp(causal_copy(u, 90.0, u0)[:, None], 300.0)[:, 0], 90.0),
    ("fast echo: 2-s high-passed, delay 30 s [K4]", lambda u, u0: causal_copy(hp(u - u0, 2.0) + u0, 30.0, u0), 30.0),
    ("on 10 s / off 50 s [K5]", lambda u, u0: causal_copy(u, 90.0, u0) * ((TT % 60.0) < 10.0), 90.0),
    ("on 6 min / off 24 min [K5]", lambda u, u0: causal_copy(u, 90.0, u0) * (((TT + 600.0) % 1800.0) < 360.0), 1200.0),
    ("gain ramps 0 -> g over the hour [K2]", lambda u, u0: causal_copy(u, 90.0, u0) * TT / TT[-1], 90.0),
    ("gain grows exp., theta 600 s [K2]", lambda u, u0: causal_copy(u, 90.0, u0) * np.exp((TT - TT[-1]) / 600.0), 90.0),
    ("gain grows exp., theta 300 s [K2]", lambda u, u0: causal_copy(u, 90.0, u0) * np.exp((TT - TT[-1]) / 300.0), 90.0),
]
GROWTH = {10: lambda: TT / TT[-1], 11: lambda: np.exp((TT - TT[-1]) / 600.0), 12: lambda: np.exp((TT - TT[-1]) / 300.0)}


def block_means(x, nb, lag=0):
    m = (x.shape[0] - lag) // nb
    return x[lag:lag + m * nb].reshape(m, nb, *x.shape[1:]).mean(1)


def running_metric(U, O):
    """Worst block slope over 20-min windows starting at 10, 20, 30 and 40 min (the first 10 min, the detection span,
    are the short-session case and are reported separately)."""
    L = int(1200 * FS); out = None
    for s0 in (600, 1200, 1800, 2400):
        a = int(s0 * FS); w = wbs(U[a:a + L], O[a:a + L]); out = w if out is None else np.maximum(out, w)
    return out


# ------------------------------------------------------------------------------------------------------------ jobs
def job_R1():
    out = []
    U = partners_fast(33, 33, T=T, signed=SIGNED); u0 = engine_baseline(33, 33, signed=SIGNED)
    for label, X, u0r in (
            ("causal, u0 = b_id (engine-like)", np.stack([causal_copy(U[:, k], DELAYS[k % 12], u0[k]) for k in range(33)], 1), u0),
            ("as tests/test_ledger_injected.py builds it (padded, minus session mean; u0 = session mean)",
             np.stack([delay(U[:, k], DELAYS[k % 12] * FS) - U[:, k].mean() for k in range(33)], 1), U.mean(0))):
        Oo, _, _, _, _ = run2(U, X, CEIL, u0r, net="old")
        On, hn, en, A, g = run2(U, X, CEIL, u0r, net="new", record_a=True)
        bo = wbs(U, Oo) / np.where(CEIL > 0, CEIL, 1); bn = wbs(U, On) / np.where(CEIL > 0, CEIL, 1)
        rm = running_metric(U, On) / np.where(CEIL > 0, CEIL, 1)
        Oe, he = ledger_only(U, A * X, CEIL, E0); be = wbs(U, Oe) / np.where(CEIL > 0, CEIL, 1)
        out.append(f"R1. F22 scenario, gain-1 copy, {label}: residual / c_k, CURRENT ledger -> REVISION 2")
        for k in CAPPED:
            det = g.first[k] - DELAYS[k % 12] if g.first[k] >= 0 else np.inf
            out.append(f"   {CODES[k]:<5} c {CEIL[k]:.2f} delay {DELAYS[k % 12]:>3} s g/c {1 / CEIL[k]:5.1f}: current {bo[k]:.2f} c"
                       f" -> rev2 {bn[k]:.2f} c (running 20-min {rm[k]:.2f} c); a final {A[-1, k]:.4f} (kappa_g c/g "
                       f"{KG * CEIL[k]:.4f}); detected {det:5.0f} s after the delay; ledger stage changed {hn[k]:.3f}; with ledger floor E0 {be[k]:.2f} c")
        out.append(f"   worst: current {bo[CAPPED].max():.2f} c, REV2 {bn[CAPPED].max():.2f} c, running {rm[CAPPED].max():.2f} c,"
                   f" REV2 with ledger floor E0 {be[CAPPED].max():.2f} c;"
                   f" zero-ceiling max slope {wbs(U, On)[CEIL == 0].max():.4f}; attenuate-only "
                   f"{bool(np.all(np.abs(On) <= np.abs(X) + 1e-15) and np.all(On * X >= -1e-18))}")
        out.append("")
    return "\n".join(out)


def job_R2(chunk):
    rows = []
    for si in chunk:
        name, f, onset = SCEN[si]
        cols = [(cc, gg) for cc in CS for gg in GR]; n = len(cols)
        U = partners_fast(n, 300 + si, T=T); u0 = engine_baseline(n, 300 + si)
        c = np.array([cc for cc, _ in cols]); g = np.array([gg for _, gg in cols])
        X = np.stack([g[j] * c[j] * f(U[:, j], u0[j]) for j in range(n)], 1)
        Oo, _, _, _, _ = run2(U, X, c, u0, net="old")
        On, hn, en, A, gov = run2(U, X, c, u0, net="new", record_a=True)
        raw = wbs(U, X) / c; old = wbs(U, Oo) / c; new = wbs(U, On) / c; rm = running_metric(U, On) / c
        Oe, _ = ledger_only(U, A * X, c, E0); ne = wbs(U, Oe) / c
        # theorem constants (section "Revision 2", Theorem 1')
        Bs = np.zeros(n)
        for S in gov.sets:
            for s in S["mem"]:
                Bs = np.maximum(Bs, s["beta"].max(1))
        R = raw * c / np.maximum(Bs, 1e-12)
        Lam = np.zeros(n)
        for b in (2.0, 10.0, 30.0, 60.0):
            nb = int(b * FS); xb = block_means(np.abs(X), nb); ub = block_means(U, nb)
            Lam = np.maximum(Lam, np.sqrt((xb ** 2).mean(0)) / (ub.std(0) * np.maximum(Bs, 1e-12)))
        eta = gov.se_over_c() * gov.a          # a_T z_n se / (z c): the unlatched band, at the final gain
        eps = np.zeros(n); qcl = np.zeros(n); qtr = np.zeros(n); EPS = 0.10
        changed = np.abs(On - A * X) > 1e-9 * np.maximum(np.abs(X), 1e-12)
        ub = block_means(U, 100); cb = block_means(changed.astype(float), 100) > 0
        for j in range(n):
            if gov.first[j] < 0:
                eps[j] = np.nan; continue
            # settle time: a within (1 + EPS) of its final value (a is non-increasing, so it stays there)
            ts = int(np.argmax(A[:, j] <= (1 + EPS) * A[-1, j])); eps[j] = A[ts:, j].max() / A[-1, j] - 1
            dv = (ub[:, j] - ub[:, j].mean()) ** 2; S0 = dv.sum(); bi = ts // 100
            qcl[j] = dv[bi:][cb[bi:, j]].sum() / S0
            span = slice(int(onset * FS) // 100, bi + 1)
            qtr[j] = np.sqrt(((ub[span, j] - u0[j]) ** 2).sum() * dv[span].sum()) / S0
        bound = (KG + Z * eta) * (R + Lam * (np.nan_to_num(eps) + np.sqrt(qcl) * (1 + np.nan_to_num(eps)))) + g * qtr
        eff = None
        if si in GROWTH:
            gt = GROWTH[si](); eff = np.array([(A[T // 2:, j] * gt[T // 2:]).max() * g[j] for j in range(n)])
        rows.append(dict(si=si, name=name, c=c, g=g, raw=raw, old=old, new=new, rm=rm, R=R, Lam=Lam, eta=eta, eps=eps,
                         qcl=qcl, qtr=qtr, bound=bound, eff=eff, det=gov.first - onset, hit=hn, ne=ne))
    return rows


def job_R3():
    out = ["R3. copies near the target ON TOP OF the counted routes (seed 8, delay 60 s, u0 = b_id): residual / c_k"]
    Uh = partners_fast(33, 8, T=T, signed=SIGNED); u0 = engine_baseline(33, 8, signed=SIGNED)
    Y = counted_routes(Uh, u0, CEIL, GAIN, SIGNED)
    GH = (0.8, 1.2, 2.0, 5.0)
    k4 = len(GH)
    U4 = np.tile(Uh, (1, k4)); c4 = np.tile(CEIL, k4); u04 = np.tile(u0, k4)
    X4 = np.concatenate([Y + np.stack([causal_copy(Uh[:, k], 60.0, u0[k]) * gh * CEIL[k] for k in range(33)], 1) for gh in GH], 1)
    On, hn, en, A, g = run2(U4, X4, c4, u04, net="new")
    raw = wbs(U4, X4); new = wbs(U4, On)
    for i, gh in enumerate(GH):
        sl = slice(33 * i, 33 * i + 33); cap = CAPPED
        rr = raw[sl][cap] / CEIL[cap]; nn = new[sl][cap] / CEIL[cap]
        out.append(f"   copy g/c {gh}: raw (copy + counted) worst {rr.max():.2f} c -> rev2 worst {nn.max():.2f} c "
                   f"(channel {CODES[cap[np.argmax(nn)]]}); by ceiling " + ", ".join(
                       f"c {cc}: {nn[np.isclose(CEIL[cap], cc)].max():.2f}" for cc in sorted(set(CEIL[cap]))))
    out.append("")
    return "\n".join(out)


def job_R4_R7():
    out = ["R4. counted routes running high (a counted total of slope s c_k at 0.45 s; no unlisted route; u0 = b_id)"]
    SS = (0.50, 0.70, 0.85, 0.974)
    cx = np.array([cc for cc in CS for _ in SS]); sx = np.array([ss for _ in CS for ss in SS]); n = len(cx)
    Ux = partners_fast(n, 77, T=T); u0 = engine_baseline(n, 77)
    Xx = np.stack([sx[j] * cx[j] * causal_copy(Ux[:, j], 0.45, u0[j]) for j in range(n)], 1)
    Ox, hx, ex, Ax, gx = run2(Ux, Xx, cx, u0, net="new", record_a=True)
    rx = wbs(Ux, Ox) / cx; r0 = wbs(Ux, Xx) / cx
    for j in range(n):
        out.append(f"   c {cx[j]:.2f} counted slope {r0[j]:.2f} c -> {rx[j]:.2f} c (a<1 on {ex[j]:.3f} of frames, final a "
                   f"{Ax[-1, j]:.2f}; ledger stage changed {hx[j]:.3f})")
    out.append("")
    out.append("R7. Lemma 0 for revision 2: scale ceilings and the partner-caused part by lambda = 8")
    Ui = partners_fast(4, 3, T=6000); ci = np.array([0.03, 0.05, 0.10, 0.35]); u0 = engine_baseline(4, 3)
    Xi = np.stack([5 * ci[j] * causal_copy(Ui[:, j], 30.0, u0[j]) for j in range(4)], 1)
    O1, _, _, A1, _ = run2(Ui, Xi, ci, u0, record_a=True)
    O8, _, _, A8, _ = run2(Ui, 8 * Xi, 8 * ci, u0, record_a=True)
    out.append(f"   max |out(8)/8 - out(1)| = {np.abs(O8 / 8 - O1).max():.3g}; max |a(8) - a(1)| = {np.abs(A8 - A1).max():.3g}")
    out.append("")
    return "\n".join(out)


def k7_partners(seeds, dur):
    """test_counted_routes_untouched's partners (same RNG order), several seeds side by side as columns."""
    n_ = int(dur * FS)
    return [partners_fast(33, s, T=n_, signed=SIGNED) for s in seeds]


def job_R5(kind):
    out = []
    if kind in ("1h", "30min", "held"):
        seeds = range(7, 15) if kind != "held" else range(15, 23)
        dur = 1800 if kind == "30min" else 3600
        Us = k7_partners(seeds, dur); u0s = [engine_baseline(33, s, signed=SIGNED) for s in seeds]
        U = np.concatenate(Us, 1); u0 = np.concatenate(u0s); c = np.tile(CEIL, len(Us))
        Y = counted_routes(U, u0, c, np.tile(GAIN, len(Us)), np.tile(SIGNED, len(Us)))
        On, hn, en, A, g = run2(U, Y, c, u0, net="new", record_a=True)
        _, he = ledger_only(U, A * Y, c, E0)
        out.append(f"R5. false engagement, counted routes only, u0 = b_id, {dur // 60}-min sessions, seeds {list(seeds)}")
        for i, s in enumerate(seeds):
            sl = slice(33 * i, 33 * i + 33); e = en[sl][CAPPED]; h = hn[sl][CAPPED]
            sl0 = wbs(U[:, sl], Y[:, sl])[CAPPED] / CEIL[CAPPED]
            out.append(f"   seed {s}: governor a<1 on {100 * e.max():.2f} % of frames (worst channel), min a {A[:, sl][:, CAPPED].min():.2f};"
                       f" ledger stage changed {100 * h.max():.2f} % ({CODES[CAPPED[np.argmax(h)]]}), with floor E0 {100 * he[sl][CAPPED].max():.2f} %; counted-route slope max "
                       f"{sl0.max():.2f} c; |mean - b_id| max {np.abs(U[:, sl].mean(0) - u0[sl])[CAPPED].max():.3f}")
    else:
        out.append("R5. K6 stress cases: u0 = session mean +/- 0.10 (seed 8; seed 10 livelier, 30-s blocks on every channel)")
        for seed in (8, 10):
            if seed == 10:
                r10 = np.random.default_rng(10)
                Un = np.stack([partner(T, r10, 30.0) - (0.4 if SIGNED[k] else 0) for k in range(33)], 1)
            else:
                Un = partners_fast(33, 8, T=T, signed=SIGNED)
            for dl in (-0.10, 0.10):
                u0 = Un.mean(0) + dl
                Y = counted_routes(Un, u0, CEIL, GAIN, SIGNED)
                On, hn, en, A, g = run2(Un, Y, CEIL, u0, net="new", record_a=True)
                out.append(f"   seed {seed}, delta {dl:+.2f}: governor a<1 on {100 * en[CAPPED].max():.2f} % of frames, min a "
                           f"{A[:, CAPPED].min():.2f}; ledger stage changed {100 * hn[CAPPED].max():.2f} %")
    out.append("")
    return "\n".join(out)


def job_R6(e0):
    """The ledger alone on test_counted_routes_untouched's exact recipe (u0 = session mean, onset filter from 0)."""
    res = []
    for dur in (1800, 3600):
        n_ = int(dur * FS); Us = []; Ys = []
        for seed in range(7, 15):
            r = np.random.default_rng(seed); Uk = np.zeros((n_, 33)); Yk = np.zeros((n_, 33))
            for k in range(33):
                u = partner(n_, r, 300.0 if k % 2 == 0 else 30.0)
                if SIGNED[k]:
                    u = u - 0.4
                Uk[:, k] = u; xd = delay(u, 0.45 * FS); e = xd - lp(xd[:, None], 4.0)[:, 0]
                Yk[:, k] = GAIN[k] * (np.maximum(e, 0.0) if not SIGNED[k] else e) + 0.22 * CEIL[k] * lp((u - u.mean())[:, None], 120.0)[:, 0]
            Us.append(Uk); Ys.append(Yk)
        U = np.concatenate(Us, 1); Y = np.concatenate(Ys, 1); c = np.tile(CEIL, 8)
        led = LedgerE0(c, e0) if e0 else Ledger(c)
        for t in range(n_):
            led.step(U[t], Y[t])
        ch = led.hits / n_
        row = []
        for i in range(8):
            h = ch[33 * i:33 * i + 33][CAPPED]
            row.append(f"{7 + i}: {100 * h.max():.2f} %")
        res.append(f"   E0 {e0}: {dur // 60} min: " + "; ".join(row) + f"  [over 1 %: {sum(float(x.split(': ')[1][:-2]) > 1 for x in row)}/8]")
    return "\n".join(res)


if __name__ == "__main__":
    T0 = time.time()
    print("REVISION 2 CHECK OF THE MATHEMATICS ONLY (synthetic signals; not evidence about people).")
    print(f"1-h sessions at {FS:.0f} Hz unless stated; metric: worst block-mean slope over 2/10/30/60-s blocks, lags 0-300 s,"
          f" 6 phases; governor {GOV2}\n", flush=True)
    chunks = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10], [11, 12]]
    with ProcessPoolExecutor(4) as ex:
        f1 = ex.submit(job_R1)
        f2 = [ex.submit(job_R2, ch) for ch in chunks]
        f3 = ex.submit(job_R3); f4 = ex.submit(job_R4_R7)
        f5 = [ex.submit(job_R5, k) for k in ("1h", "30min", "held", "K6")]
        f6 = [ex.submit(job_R6, e0) for e0 in (0.0, E0)]
        print(f1.result(), flush=True)
        rows = sorted(sum((f.result() for f in f2), []), key=lambda r: r["si"])
        print(f"[{time.time() - T0:5.0f} s] R2. worst residual / c per ceiling (worst over g/c {GR}), u0 = b_id")
        print(f"   {'scenario':<46} {'current':>8} | REV2 session: " + "  ".join(f"c {cc:<4}" for cc in CS)
              + " | running 20-min | worst cell (c, g/c) | eff. gain at end | with E0")
        for r in rows:
            per = "  ".join(f"{r['new'][np.isclose(r['c'], cc)].max():6.2f}" for cc in CS)
            j = int(np.argmax(r["new"]))
            eff = f"{np.max(r['eff']):.2f} c" if r["eff"] is not None else "-"
            print(f"   {r['name']:<46} {r['old'].max():8.2f} |          {per} | {r['rm'].max():6.2f}         |"
                  f" ({r['c'][j]:.2f}, {r['g'][j]:.1f}) {r['new'][j]:.2f}   | {eff} | {r['ne'].max():.2f}")
        print("\n   per cell (c, g/c): raw -> current -> rev2 [running] {detection s after onset}")
        for r in rows:
            print(f"   {r['name']}")
            print("     " + "  ".join(f"({r['c'][j]:.2f},{r['g'][j]:4.1f}) {r['raw'][j]:5.1f}->{r['old'][j]:.2f}->{r['new'][j]:.2f}"
                                    f"[{r['rm'][j]:.2f}]{{{r['det'][j]:.0f}}}" + ("\n    " if j % 4 == 3 else "")
                                    for j in range(len(r["c"]))))
        print("\n   Theorem 1' constants per scenario (max over engaged cells): R, Lambda, eta, eps_a (settle at 1.10 a_T), q_cl, g Q_tr;"
              " first term c(kappa_g + z eta)(R + Lambda(eps_a + sqrt(q_cl)(1 + eps_a))) and the whole bound vs measured")
        for r in rows:
            ok = ~np.isnan(r["eps"])
            first = r['bound'] - r['g'] * r['qtr']
            print(f"   {r['name']:<46} R {r['R'][ok].max():.2f}  Lam {r['Lam'][ok].max():.2f}  eta {r['eta'][ok].max():.3f}  eps_a "
                  f"{np.nanmax(r['eps']) if ok.any() else np.nan:.2f}  q_cl {r['qcl'][ok].max():.3f}  g Q_tr {(r['g'] * r['qtr'])[ok].max():.2f}"
                  f"  | first term max {first[ok].max():.2f} c"
                  f"  | bound max {np.nanmax(np.where(ok, r['bound'], np.nan)) if ok.any() else np.nan:.2f} c,"
                  f" measured max {r['new'].max():.2f} c, bound >= measured in {int((r['bound'][ok] >= r['new'][ok] - 1e-9).sum())}/{int(ok.sum())} engaged cells")
        print(flush=True)
        print(f"[{time.time() - T0:5.0f} s]")
        print(f3.result()); print(f4.result())
        for f in f5:
            print(f.result(), flush=True)
        print("R6. the unchanged ledger's own binding rate on the counted routes (test_counted_routes_untouched's exact recipe,"
              " seeds 7-14), worst capped channel; E0 = an evidence floor on the ledger's E (a separate, proposed change to the ledger)")
        for f in f6:
            print(f.result(), flush=True)
    print(f"\n[{time.time() - T0:5.0f} s] done")
