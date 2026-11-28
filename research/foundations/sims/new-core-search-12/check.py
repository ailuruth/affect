"""Pass 12 check: the detection lever of the scaled safety net, seen as quickest change detection.

A CHECK OF ALGEBRA ON SYNTHETIC SIGNALS ONLY. It is NOT evidence about people, behaviour or the engine.
numpy only (plus the standard library's process pool, 4 workers). Run:  python3 -I -B check.py > out.txt   (about 8 min on 4 cores)

It reuses, read-only, the reference implementation of revision 2 (../scaled-safety-net/rev2_lib.py: partner recipe,
engine-like baseline b_id, counted routes, Governor2, the unchanged Ledger and the block-mean metric).

Parts
  A  noise floor of the governor's statistic on ordinary partners (counted routes only, u0 = b_id, seeds 7-14, 1 h):
     per-batch slope noise eta_b (units of c_k, one batch = 2 W of frames), and the lag-1 correlation of batch scores.
     These are the inputs of the Lorden/Lai frontier written in the synthesis.
  B  a CUSUM bank on the same statistic (batch-centred window-mean regressions at the same 153 keys per channel),
     threshold calibrated so that it never engages on the calibration partners (seeds 7-14, 1 h and 30 min) with a
     margin, then checked on held-out partners (seeds 15-22, 1 h) and the K6 stress cases (u0 = mean -/+ 0.10).
  C  an envelope stage: the listed routes' peak-to-peak gain Gamma_k = 2 G_k + 0.22 c_k (fast gear through the 4-s
     onset high-pass, l1 norm 2; held cone, l1 norm 1) bounds |r_L(t)| <= Gamma_k sup_{s<=t} |u(s) - u0| exactly, so a
     frame with |r| above that envelope proves an unlisted partner-caused part. a_env = min(a_env, Gamma M_v / |r|).
  D  the copy cases of revision 2's R2 grid (same partners, same cells): rev2 alone, CUSUM bank, envelope + rev2,
     envelope + CUSUM + rev2; session residual / c, worst 20-min window, detection time.
  E  an evader: a copy switched on and off with short on-periods, at a gain below the envelope.
  F  the metric itself: the raw (unattenuated) route's worst 20-min window and session slope divided by its own gain
     g, on the cells of D. A value above 1 means the windowed metric reads more than the route's gain (the pathwise
     inflation of pass 10's Observation 4); no detector removes that part.
"""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scaled-safety-net"))
from rev2_lib import (np, FS, lp, wbs, partner, partners_fast, engine_baseline, causal_copy, counted_routes,  # noqa: E402
                      Governor2, GOV2, Ledger, CEIL, GAIN, SIGNED, CODES, CAPPED)

T = int(3600 * FS)
TT = np.arange(T) / FS
KG = GOV2["kappa_g"]
SETS = GOV2["sets"]          # (10 s step, 5 s), (10 s level, 5 s), (60 s level, 10 s); lags 0-300 s


# ------------------------------------------------------------------------------------------------ the CUSUM bank
class CusumBank:
    """Per channel k and key (W, kind, L): batches of B = 2 W frames, counted only from t >= L + 2 W.
    Per batch: batch-centred P_b = sum (pi - pibar)(rho - rhobar), E_b = sum (pi - pibar)^2 (the intercept is removed
    inside each batch, so the step from u0 to his level never enters).  Normalised batch slope bhat_b = P_b / (c E_b),
    weight w_b = E_b / (N_b sig_u^2) (his movement in the batch relative to his running average; sig_u^2 >= sigma0^2).
    Score for design slope s1 against the boundary s0 = kappa_g (both in units of c_k):
        l_b = (s1 - s0) * (bhat_b - (s0 + s1) / 2) * w_b
    (the Gaussian log-likelihood ratio of a batch slope with unit noise; the noise scale is folded into the threshold h).
    CUSUM S <- max(0, S + l_b) per key and design slope; engage when S > h.  On engagement the slope estimate is the
    pooled sum P / sum E over the current CUSUM run, and a_k = min(a_k, kappa_g c_k / that slope) (ratchet).
    Homogeneous of degree 0 in (c_k, r_k): every output-side quantity is a multiple of c_k."""

    def __init__(self, c, u0, h, s1s=(1.2, 3.0), s0=KG, sigma0=0.01, sets=SETS):
        self.c = np.asarray(c, float); n = len(self.c); self.n = n; self.u0 = np.asarray(u0, float)
        self.h = h; self.s1s = s1s; self.s0 = s0; self.sigma0 = sigma0
        self.wins = sorted({w for w, _, _ in sets}); self.Wf = {w: int(round(w * FS)) for w in self.wins}
        self.aW = {w: 1 - np.exp(-1 / (w * FS)) for w in self.wins}
        self.H = int(300 * FS) + max(self.Wf.values()) + 1
        self.uW = {w: self.u0.copy() for w in self.wins}; self.rW = {w: np.zeros(n) for w in self.wins}
        self.uring = {w: np.repeat(self.u0[None, :], self.H, 0) for w in self.wins}
        self.rring = {w: np.zeros((self.H, n)) for w in self.wins}
        self.ptr = 0; self.t = 0; self.dsig = np.exp(-1 / (1800 * FS))
        self.sets = []
        for (w, kind, step) in sets:
            lags = np.arange(0, int(300 * FS) + 1, int(round(step * FS))); K = len(lags)
            z = lambda: np.zeros((n, K))
            self.sets.append(dict(w=w, kind=kind, lags=lags, B=2 * self.Wf[w], start=lags + 2 * self.Wf[w],
                                  Sp=z(), Sr=z(), Spr=z(), Spp=z(), N=z(), sig=np.zeros((n, K)), sigw=np.zeros(K),
                                  S=[z() for _ in s1s], RP=[z() for _ in s1s], RE=[z() for _ in s1s]))
        self.a = np.ones(n); self.first = np.full(n, -1.0); self.engaged = np.zeros(n); self.maxS = np.zeros(n)

    def step(self, u, r):
        H = self.H; self.ptr = (self.ptr + 1) % H; q = self.ptr
        for w in self.wins:
            self.uW[w] += self.aW[w] * (u - self.uW[w]); self.rW[w] += self.aW[w] * (r - self.rW[w])
            self.uring[w][q] = self.uW[w]; self.rring[w][q] = self.rW[w]
        tgt = np.ones(self.n)
        for S in self.sets:
            w, lags = S["w"], S["lags"]; Wf = self.Wf[w]
            if S["kind"] == "level":
                pi = self.uring[w][(q - lags) % H].T; rho = np.repeat(self.rW[w][:, None], len(lags), 1)
            else:
                pi = (self.uring[w][(q - lags) % H] - self.uring[w][(q - lags - Wf) % H]).T
                rho = np.repeat((self.rW[w] - self.rring[w][(q - Wf) % H])[:, None], len(lags), 1)
            v = (self.t >= S["start"]).astype(float)[None, :]
            S["Sp"] += v * pi; S["Sr"] += v * rho; S["Spr"] += v * pi * rho; S["Spp"] += v * pi * pi; S["N"] += v
            if (self.t + 1) % S["B"] == 0:
                N = np.maximum(S["N"], 1.0); ok = S["N"] >= S["B"] / 2
                P = S["Spr"] - S["Sp"] * S["Sr"] / N; E = np.maximum(S["Spp"] - S["Sp"] ** 2 / N, 0.0)
                vb = E / N
                S["sig"] = np.where(ok, S["sig"] * self.dsig ** S["B"] + vb, S["sig"])
                S["sigw"] = np.where(ok.any(0), S["sigw"] * self.dsig ** S["B"] + 1.0, S["sigw"])
                sig2 = np.maximum(S["sig"] / np.maximum(S["sigw"][None, :], 1e-12), self.sigma0 ** 2)
                cc = np.where(self.c > 0, self.c, 1.0)[:, None]
                Ef = np.maximum(E, self.sigma0 ** 2 * N)
                bhat = P / (cc * Ef); wb = np.where(ok, Ef / (N * sig2), 0.0)
                for i, s1 in enumerate(self.s1s):
                    l = (s1 - self.s0) * (bhat - 0.5 * (self.s0 + s1)) * wb
                    reset = S["S"][i] + l <= 0
                    S["S"][i] = np.maximum(0.0, S["S"][i] + l)
                    S["RP"][i] = np.where(reset, 0.0, S["RP"][i] + np.where(ok, P, 0.0))
                    S["RE"][i] = np.where(reset, 0.0, S["RE"][i] + np.where(ok, Ef, 0.0))
                    self.maxS = np.maximum(self.maxS, S["S"][i].max(1))
                    hit = S["S"][i] > self.h
                    if hit.any():
                        bet = S["RP"][i] / np.maximum(S["RE"][i], 1e-30)
                        bmax = np.max(np.where(hit, bet, 0.0), 1)
                        tg = np.where(bmax > KG * self.c, KG * self.c / np.where(bmax > 0, bmax, 1.0), 1.0)
                        tgt = np.minimum(tgt, np.where(self.c > 0, tg, np.where(hit.any(1), 0.0, 1.0)))
                S["Sp"][:] = 0; S["Sr"][:] = 0; S["Spr"][:] = 0; S["Spp"][:] = 0; S["N"][:] = 0
        self.a = np.minimum(self.a, np.clip(tgt, 0, 1))
        low = (self.a < 1) & (self.first < 0); self.first[low] = self.t / FS
        self.engaged += self.a < 1; self.t += 1
        return self.a * r


class Envelope:
    """a_env(t) = min(a_env(t-1), Gamma M_v(t) / |r(t)|) whenever |r(t)| > Gamma M_v(t), M_v(t) = sup_{s<=t} |u(s) - u0|.
    Gamma_k = 2 G_k + 0.22 c_k is the listed routes' exact peak-to-peak gain in this synthetic engine, so on the
    counted routes alone it never acts (proved, and checked below)."""

    def __init__(self, c, u0, gamma):
        self.u0 = np.asarray(u0, float); self.g = np.asarray(gamma, float); n = len(self.u0)
        self.M = np.zeros(n); self.a = np.ones(n); self.first = np.full(n, -1.0); self.t = 0

    def step(self, u, r):
        self.M = np.maximum(self.M, np.abs(u - self.u0)); env = self.g * self.M
        over = np.abs(r) > env * (1 + 1e-9) + 1e-15
        self.a = np.where(over, np.minimum(self.a, env / np.maximum(np.abs(r), 1e-30)), self.a)
        low = (self.a < 1) & (self.first < 0); self.first[low] = self.t / FS; self.t += 1
        return self.a * r


def run_net(U, X, c, u0, net, h=None, gamma=None):
    """net: subset of {'rev2', 'cusum', 'env'}; gains combine by min (all attenuate-only), then the unchanged ledger."""
    Tn, n = U.shape
    g2 = Governor2(c, u0) if "rev2" in net else None
    cb = CusumBank(c, u0, h) if "cusum" in net else None
    ev = Envelope(c, u0, gamma) if "env" in net else None
    led = Ledger(c); O = np.empty_like(X); first = np.full(n, np.inf); eng = np.zeros(n)
    for t in range(Tn):
        a = np.ones(n)
        if g2 is not None:
            g2.step(U[t], X[t]); a = np.minimum(a, g2.a_out)
        if cb is not None:
            cb.step(U[t], X[t]); a = np.minimum(a, cb.a)
        if ev is not None:
            ev.step(U[t], X[t]); a = np.minimum(a, ev.a)
        first = np.where((a < 1) & ~np.isfinite(first), t / FS, first); eng += a < 1
        O[t] = led.step(U[t], a * X[t])
    return O, first, eng / Tn, (cb.maxS if cb is not None else None)


def running(U, O):
    L = int(1200 * FS); out = None
    for s0 in (0, 600, 1200, 1800, 2400):
        a = int(s0 * FS); w = wbs(U[a:a + L], O[a:a + L]); out = w if out is None else np.maximum(out, w)
    return out


# ------------------------------------------------------------------------------------------------ part A
def job_A(seed):
    U = partners_fast(33, seed, T=T, signed=SIGNED); u0 = engine_baseline(33, seed, signed=SIGNED)
    Y = counted_routes(U, u0, CEIL, GAIN, SIGNED)
    res = {}
    for (W, kind) in ((10.0, "level"), (10.0, "step"), (60.0, "level")):
        Wf = int(W * FS); a = 1 - np.exp(-1 / (W * FS)); ub = lp(U - 0 * u0, W) * 0
        ub = u0[None, :] + lp(U - u0[None, :], W); rb = lp(Y, W); B = 2 * Wf
        for L in (0.0, 30.0, 90.0, 150.0, 300.0):
            l = int(L * FS)
            pi = np.roll(ub, l, 0); pi[:l] = u0
            rho = rb.copy()
            if kind == "step":
                pi = pi - np.roll(pi, Wf, 0); rho = rho - np.roll(rho, Wf, 0)
            st = l + 2 * Wf; nb = (T - st) // B
            P = pi[st:st + nb * B].reshape(nb, B, 33); R = rho[st:st + nb * B].reshape(nb, B, 33)
            Pc = P - P.mean(1, keepdims=True); Rc = R - R.mean(1, keepdims=True)
            Pb = (Pc * Rc).sum(1); Eb = (Pc * Pc).sum(1)
            beta = Pb.sum(0) / Eb.sum(0)
            sc = (Pb - beta * Eb) / (CEIL[None, :] * Eb.mean(0)[None, :] + 1e-30)   # batch slope noise, units of c
            eta = sc.std(0); r1 = np.array([np.corrcoef(sc[:-1, k], sc[1:, k])[0, 1] if CEIL[k] > 0 else 0 for k in range(33)])
            kurt = ((sc - sc.mean(0)) ** 4).mean(0) / np.maximum(sc.var(0) ** 2, 1e-30)
            res[(W, kind, L)] = (eta, r1, kurt, beta / np.where(CEIL > 0, CEIL, 1))
    return seed, res


# ------------------------------------------------------------------------------------------------ part B
def h0_partners(seed, dur, shift=None, lively=False):
    n_ = int(dur * FS)
    if lively:
        r10 = np.random.default_rng(10)
        U = np.stack([partner(n_, r10, 30.0) - (0.4 if SIGNED[k] else 0) for k in range(33)], 1)
    else:
        U = partners_fast(33, seed, T=n_, signed=SIGNED)
    u0 = U.mean(0) + shift if shift is not None else engine_baseline(33, seed, signed=SIGNED)
    return U, u0, counted_routes(U, u0, CEIL, GAIN, SIGNED)


def job_B(args):
    seed, dur, shift, lively = args
    U, u0, Y = h0_partners(seed, dur, shift, lively)
    cb = CusumBank(CEIL, u0, h=np.inf); ev = Envelope(CEIL, u0, 2 * GAIN + 0.22 * CEIL)
    envhit = np.zeros(33)
    for t in range(U.shape[0]):
        cb.step(U[t], Y[t]); ev.step(U[t], Y[t])
    return (seed, dur, shift, lively), cb.maxS, ev.a.min(), int((ev.a < 1).sum())


# ------------------------------------------------------------------------------------------------ part D
CS = (0.03, 0.05, 0.10, 0.35); GR = (1.5, 3.0, 10.0, 33.0)
SCEN = {  # as rev2_check.py's SCEN (index: name, route with gain 1, onset s)
    0: ("copy, delay 90 s (on grid)", lambda u, u0: causal_copy(u, 90.0, u0), 90.0),
    1: ("copy, delay 47.35 s (off grid)", lambda u, u0: causal_copy(u, 47.35, u0), 47.35),
    5: ("copy low-passed 120 s, delay 90 s [K3]", lambda u, u0: lp(causal_copy(u, 90.0, u0)[:, None], 120.0)[:, 0], 90.0),
    6: ("copy low-passed 300 s, delay 90 s [K3]", lambda u, u0: lp(causal_copy(u, 90.0, u0)[:, None], 300.0)[:, 0], 90.0),
    9: ("on 6 min / off 24 min [K5]", lambda u, u0: causal_copy(u, 90.0, u0) * (((TT + 600.0) % 1800.0) < 360.0), 1200.0),
    12: ("gain grows exp., theta 300 s [K2]", lambda u, u0: causal_copy(u, 90.0, u0) * np.exp((TT - TT[-1]) / 300.0), 90.0),
}
NETS = (("rev2", ("rev2",)), ("cusum", ("cusum",)), ("env+rev2", ("env", "rev2")), ("env+cusum+rev2", ("env", "cusum", "rev2")))
GOV_G = 0.8   # the envelope's listed fast gain in these pure-route cells: the worst G_k / c_k of the engine (0.8)


def job_D(args):
    si, netname, h = args
    name, f, onset = SCEN[si]
    cols = [(cc, gg) for cc in CS for gg in GR]; n = len(cols)
    U = partners_fast(n, 300 + si, T=T); u0 = engine_baseline(n, 300 + si)
    c = np.array([cc for cc, _ in cols]); g = np.array([gg for _, gg in cols])
    X = np.stack([g[j] * c[j] * f(U[:, j], u0[j]) for j in range(n)], 1)
    net = dict(NETS)[netname]
    O, first, eng, _ = run_net(U, X, c, u0, net, h=h, gamma=(2 * GOV_G + 0.22) * c)
    return si, netname, c, g, wbs(U, O) / c, running(U, O) / c, first - onset


# ------------------------------------------------------------------------------------------------ part E
def job_E(args):
    gc, on_s, period_s, netname, h = args
    n = 4; c = np.full(n, 0.05)
    U = partners_fast(n, 900 + int(on_s), T=T); u0 = engine_baseline(n, 900 + int(on_s))
    sw = ((TT % period_s) < on_s).astype(float)
    X = np.stack([gc * c[j] * causal_copy(U[:, j], 90.0, u0[j]) * sw for j in range(n)], 1)
    raw = wbs(U, X) / c
    O, first, eng, _ = run_net(U, X, c, u0, dict(NETS)[netname], h=h, gamma=(2 * GOV_G + 0.22) * c)
    return gc, on_s, period_s, netname, raw.max(), (wbs(U, O) / c).max(), (running(U, O) / c).max(), np.nanmin(np.where(np.isfinite(first), first, np.nan)) if np.isfinite(first).any() else np.inf


def job_F(si):
    name, f, onset = SCEN[si]
    cols = [(cc, gg) for cc in CS for gg in GR]; n = len(cols)
    U = partners_fast(n, 300 + si, T=T); u0 = engine_baseline(n, 300 + si)
    c = np.array([cc for cc, _ in cols]); g = np.array([gg for _, gg in cols])
    X = np.stack([g[j] * c[j] * f(U[:, j], u0[j]) for j in range(n)], 1)
    return name, c, g, running(U, X) / c / g, wbs(U, X) / c / g


if __name__ == "__main__":
    T0 = time.time()
    print("PASS 12 CHECK: ALGEBRA ON SYNTHETIC SIGNALS ONLY (not evidence about people, behaviour or the engine).")
    print("1-h sessions at 10 Hz unless stated; u0 = engine-like b_id unless stated; metric as revision 2 (worst block-mean"
          " slope over 2/10/30/60-s blocks, lags 0-300 s, 6 phases), residual / c_k.\n", flush=True)
    with ProcessPoolExecutor(4) as ex:
        # ---- A
        resA = list(ex.map(job_A, range(7, 15)))
        print("A. noise of the governor's statistic on ordinary partners (counted routes only), seeds 7-14, 1 h.")
        print("   eta_b = SD over batches of the batch slope residual, in units of c_k (batch = 2 W: 20 s at W 10 s, 120 s at W 60 s);"
              " r1 = lag-1 correlation of batch residuals; kurt = kurtosis (3 for Gaussian); beta = the key's session slope / c")
        keys = list(resA[0][1].keys())
        for kk in keys:
            eta = np.stack([r[1][kk][0] for r in resA])[:, CAPPED]; r1 = np.stack([r[1][kk][1] for r in resA])[:, CAPPED]
            ku = np.stack([r[1][kk][2] for r in resA])[:, CAPPED]; be = np.stack([r[1][kk][3] for r in resA])[:, CAPPED]
            print(f"   W {kk[0]:4.0f} s {kk[1]:<5} L {kk[2]:5.0f} s: eta_b median {np.median(eta):.3f}, by channel max-of-median "
                  f"{np.median(eta, 0).max():.3f} ({CODES[CAPPED[np.argmax(np.median(eta, 0))]]}), min-of-median {np.median(eta, 0).min():.3f};"
                  f" r1 median {np.median(r1):+.2f}; kurt median {np.median(ku):.1f}, max {ku.max():.0f}; beta max {be.max():.2f}")
        per_ch = np.median(np.stack([r[1][(10.0, 'level', 90.0)][0] for r in resA]), 0)
        print("   per channel, W 10 s level, L 90 s, median eta_b: " + ", ".join(f"{CODES[k]} {per_ch[k]:.2f}" for k in CAPPED))
        print(f"[{time.time() - T0:5.0f} s]\n", flush=True)

        # ---- B
        cal = [(s, d, None, False) for s in range(7, 15) for d in (3600, 1800)]
        held = [(s, 3600, None, False) for s in range(15, 23)]
        k6 = [(8, 3600, -0.10, False), (8, 3600, 0.10, False), (10, 3600, -0.10, True), (10, 3600, 0.10, True)]
        rB = list(ex.map(job_B, cal + held + k6))
        mc = max(r[1][CAPPED].max() for r in rB[:len(cal)])
        H = 1.5 * mc
        print("B. CUSUM bank on ordinary partners (counted routes only): the largest CUSUM statistic reached on any capped"
              " channel, key and design slope (no engagement; threshold free)")
        for r in rB:
            (s, d, sh, lv), mS, aenv, nenv = r
            tag = "calibration" if r in rB[:len(cal)] else ("held-out" if r in rB[len(cal):len(cal) + len(held)] else "K6 stress")
            print(f"   {tag:<11} seed {s:>2} {d // 60:>2} min{'' if sh is None else f', u0 = mean {sh:+.2f}'}{' lively' if lv else ''}:"
                  f" max S {mS[CAPPED].max():7.2f} ({CODES[CAPPED[np.argmax(mS[CAPPED])]]});"
                  f" envelope min a {aenv:.3f}, frames over envelope {nenv}")
        print(f"   calibration max S = {mc:.2f}; threshold h = 1.5 x that = {H:.2f};"
              f" held-out and K6 max S = {max(r[1][CAPPED].max() for r in rB[len(cal):]):.2f}"
              f" -> engaged on held-out/K6: {sum(r[1][CAPPED].max() > H for r in rB[len(cal):])} of {len(rB) - len(cal)}")
        print(f"[{time.time() - T0:5.0f} s]\n", flush=True)

        # ---- D
        jobs = [(si, nm, H) for si in SCEN for nm, _ in NETS]
        rD = list(ex.map(job_D, jobs))
        print("D. copy cases on revision 2's R2 cells (same partners: seed 300 + scenario index; 16 cells c x g/c each)."
              " Envelope uses Gamma = (2 x 0.8 + 0.22) c = 1.82 c (the worst listed fast gain).")
        print("   per scenario and net: worst session residual over the 16 cells; worst 20-min window; detection time after onset"
              " (median, max over cells with g/c >= 3)")
        for si in SCEN:
            print(f"   {SCEN[si][0]}")
            for nm, _ in NETS:
                r = [x for x in rD if x[0] == si and x[1] == nm][0]
                _, _, c, g, ses, rm, det = r
                big = g >= 3
                dd = det[big]
                print(f"     {nm:<15} session max {ses.max():.2f} c (cell c {c[np.argmax(ses)]:.2f}, g/c {g[np.argmax(ses)]:.1f});"
                      f" cells > 1.0 c: {int((ses > 1.0).sum())}/16; 20-min max {rm.max():.2f} c;"
                      f" detection median {np.median(dd):.0f} s, max {np.max(dd):.0f} s")
            for nm, _ in NETS:
                r = [x for x in rD if x[0] == si and x[1] == nm][0]
                print(f"       {nm:<15} cells (c, g/c) session[20-min]{{det}}: " + "  ".join(
                    f"({r[2][j]:.2f},{r[3][j]:.0f}) {r[4][j]:.2f}[{r[5][j]:.2f}]{{{r[6][j]:.0f}}}" for j in range(16)))
        print(f"[{time.time() - T0:5.0f} s]\n", flush=True)

        # ---- E
        jobsE = [(gc, on, per, nm, H) for gc in (1.5, 5.0) for (on, per) in ((20.0, 40.0), (40.0, 80.0), (60.0, 600.0))
                 for nm in ("rev2", "cusum", "env+cusum+rev2")]
        rE = list(ex.map(job_E, jobsE))
        print("E. evaders: copy delayed 90 s, switched on for t_on of every period (c 0.05, 4 partners each); worst over partners")
        for gc, on, per, nm, raw, ses, rm, fst in rE:
            print(f"   g/c {gc:4.1f}, on {on:4.0f} s of every {per:4.0f} s, {nm:<15}: raw {raw:.2f} c -> session {ses:.2f} c,"
                  f" 20-min {rm:.2f} c; first engagement at {fst:.0f} s")
        rF = list(ex.map(job_F, (9, 6, 5)))
        print("\nF. the metric's own reading of the RAW route, divided by the route's gain g (cells as in D):")
        for name, c, g, rm, ss in rF:
            print(f"   {name}: 20-min / g: " + " ".join(f"({c[j]:.2f},{g[j]:.0f}) {rm[j]:.2f}" for j in range(16)))
            print(f"   {' ' * len(name)}  session / g: max {ss.max():.2f}")
    print(f"\n[{time.time() - T0:5.0f} s] done")
