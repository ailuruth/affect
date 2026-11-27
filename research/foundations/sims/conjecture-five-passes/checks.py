"""Checks for conjecture-five-passes.md (K1-K4).
Hand-made instances only. They verify the mathematics stated in the note
(the LTI sup-slope formula, the co-modulation bound, the randomisation corner,
the closed-loop lock). They are not evidence about behaviour or people
(brief: no toy worlds)."""
import numpy as np
from scipy.signal import lfilter, freqz

fs = 10.0                 # Hz (30 Hz downsampled; nothing depends on it)
SIG0 = 0.03               # ledger floor on the SD of the partner's block means
BLK = 300                 # 30-s block means (the ledger's copy metric)
LAGS = range(0, 3001, 100)  # lags 0..300 s in 10-s steps

def ema(x, tau):
    a = np.exp(-1/(fs*tau)); return lfilter([1-a], [1, -a], x)

def ou(T, tau, sd, rng):
    a = np.exp(-1/(fs*tau)); return lfilter([sd*np.sqrt(1-a*a)], [1, -a], rng.standard_normal(T))

def _slope(x, y):
    xv = x - x.mean(); return (xv*(y-y.mean())).mean()/max(xv.var(), SIG0**2)

def block_metric(d, p, lags=LAGS, blk=BLK):
    """ledger-style copy metric: pooled toward slope of the partner-caused part's
    30-s block means on his block means at lag L, floored, max over L in 0..300 s."""
    best = -np.inf
    for L in lags:
        x = p[:len(p)-L] if L else p; y = d[L:]
        nb = len(x)//blk
        best = max(best, _slope(x[:nb*blk].reshape(nb, blk).mean(1), y[:nb*blk].reshape(nb, blk).mean(1)))
    return best

def window_metric(d, p, nblk=6, blk=100):
    """finite-window version: 60-s windows of 10-s block means, lag 0, max over windows."""
    nb = len(d)//blk
    D = d[:nb*blk].reshape(nb, blk).mean(1); P = p[:nb*blk].reshape(nb, blk).mean(1)
    return max(_slope(P[w:w+nblk], D[w:w+nblk]) for w in range(nb-nblk+1))

def pooled_slope(d, p, lags):
    """whole-session frame-level toward slope, max over lags."""
    return max(_slope(p[:len(p)-L] if L else p, d[L:]) for L in lags)

rng = np.random.default_rng(1)
print(__doc__)

# ---------------------------------------------------------------- K1
print("K1  LTI core: sup over partner paths of the toward slope = weighted H-inf row gain")
# own channel 1 reads partner channel 1 (resonant) and partner channel 2 (low-pass)
w0, r = 2*np.pi*0.2/fs, 0.985
b11 = np.array([0.02*(1-2*r*np.cos(w0)+r*r)]); a11 = np.array([1, -2*r*np.cos(w0), r*r])
b12 = np.array([0.003*(1-0.9)]); a12 = np.array([1, -0.9])
A1, A2 = np.sqrt(2)*SIG0, 0.30          # partner ch.1 SD at the floor; ch.2 half-range
om = np.linspace(1e-3, np.pi, 4000)
_, H11 = freqz(b11, a11, om); _, H12 = freqz(b12, a12, om)
bound = np.abs(H11) + (A2/A1)*np.abs(H12); k = bound.argmax()
print(f"   |K11| DC {abs(H11[0]):.3f}, peak {abs(H11).max():.3f}; predicted sup slope {bound[k]:.3f} at f = {om[k]*fs/2/np.pi:.3f} Hz")
T = 6000; t = np.arange(T); wk = om[k]
ph = np.angle(H11[k]) - np.angle(H12[k])
p1 = 0.5 + A1*np.cos(wk*t); p2 = 0.5 + A2*np.cos(wk*t + ph)
d = lfilter(b11, a11, p1-0.5) + lfilter(b12, a12, p2-0.5)
per = int(np.ceil(2*np.pi/wk))
print(f"   adversarial sinusoid pair:  measured max-lag slope {pooled_slope(d[1000:], p1[1000:], range(per+1)):.3f}")
p1n = 0.5 + ou(T, 3, 0.1, rng); p2n = 0.5 + ou(T, 3, 0.1, rng)
dn = lfilter(b11, a11, p1n-0.5) + lfilter(b12, a12, p2n-0.5)
print(f"   natural OU partner:         measured max-lag slope {pooled_slope(dn[1000:], p1n[1000:], range(60)):.3f}")
p2z = np.full(T, 0.5); d0 = lfilter(b11, a11, p1-0.5)
print(f"   same-channel only (p2 held): {pooled_slope(d0[1000:], p1[1000:], range(per+1)):.3f} vs |K11|_inf {abs(H11).max():.3f}")

# ---------------------------------------------------------------- K2
print("\nK2  co-modulation: any partner-steerable route R on channel j is a following route")
print("    adversary alternates behaviours B/B' every 30 s and moves its own channel j by +/-SIG0 in step")
c = 0.05; T = 36000; t = np.arange(T)
sq = np.where((t//300) % 2 == 0, 1.0, -1.0)                  # 30-s half period
pj_adv = 0.5 + SIG0*sq + 0.003*rng.standard_normal(T)
pj_nat = 0.5 + ou(T, 20, 0.08, rng)
def mimic(pj): return c*ema(pj-0.5, 0.45)

# (a) appraisal of the partner's words (q = 1: words of trouble)
q_adv = (sq > 0).astype(float)
q_nat = (ema((rng.random(T) < 1/600).astype(float), 1.0) > 0.01).astype(float)  # independent episodes
Ra_adv, Ra_nat = ema(q_adv, 3.0), ema(q_nat, 3.0)
# (b) contingency: the agent's estimate of how strongly the partner answers it
ai = ou(T, 4, 0.1, rng)                                       # agent's own wander on channel i
lag1 = int(fs*1.0)
def rho_hat(pi):
    x = np.r_[np.zeros(lag1), ai[:-lag1]]
    return ema(pi*x, 5.0)/(ema(x*x, 5.0)+1e-4)
resp = (sq > 0).astype(float)
pi_adv = 0.8*resp*np.r_[np.zeros(lag1), ai[:-lag1]] + 0.03*rng.standard_normal(T)
pi_nat = 0.4*np.r_[np.zeros(lag1), ai[:-lag1]] + 0.03*rng.standard_normal(T)  # steadily responsive
Rb_adv, Rb_nat = np.tanh(rho_hat(pi_adv)/0.5), np.tanh(rho_hat(pi_nat)/0.5)
# (c) self-invariant front end: partner channel i news through an exact OLS echo canceller
lags = range(1, 21)
Phi = np.stack([np.r_[np.zeros(L), ai[:-L]] for L in lags], 1)  # no constant feature (F8)
def canc(pi): w, *_ = np.linalg.lstsq(Phi, pi, rcond=None); return pi - Phi@w
news_adv = 0.2*sq + 0.03*rng.standard_normal(T)
g = Phi @ rng.normal(0, 0.3, Phi.shape[1])                      # a partner answer inside span(Phi)
Rc_adv = ema(canc(news_adv), 3.0); Rc_adv_g = ema(canc(news_adv + g), 3.0)
Rc_nat = ema(canc(ou(T, 20, 0.2, rng)), 3.0)
print(f"    (c) invariance check: max |R(news+g(a)) - R(news)| = {np.abs(Rc_adv_g-Rc_adv).max():.1e}")
for name, Radv, Rnat in [("(a) words-appraisal", Ra_adv, Ra_nat),
                         ("(b) contingency rho", Rb_adv, Rb_nat),
                         ("(c) invariant news ", Rc_adv, Rc_nat)]:
    dR = Radv[sq > 0][50:].mean() - Radv[sq < 0][50:].mean()
    for kk in [0.0, 0.5*2*c*SIG0/abs(dR), 0.1, 0.5]:
        sa = block_metric(mimic(pj_adv) + kk*Radv, pj_adv)/c
        sn = block_metric(mimic(pj_nat) + kk*Rnat, pj_nat)/c
        pred = (c + kk*dR/(2*SIG0))/c
        print(f"    {name} k={kk:6.4f} (amplitude {kk*abs(dR):.4f}): adversary {sa:6.2f} c (pred {pred:6.2f} c); natural partner {sn:5.2f} c")
    print(f"        -> allowed steerable amplitude <= ~2 c SIG0 = {2*c*SIG0:.4f} (minus the mimicry share)")

# ---------------------------------------------------------------- K3
print("\nK3  private randomisation: unbounded incremental gain, long-run slope = c")
d0lag = int(0.5*fs)
def agent_rand(x, k, s):
    xl = np.r_[np.zeros(d0lag), x[:-d0lag]]; return (c + k*s)*xl
T = 36000
for k in [1.0, 10.0]:
    s = rng.choice([-1.0, 1.0], T)                             # fresh private sign every frame
    x_adv = SIG0*sq; x_nat = ou(T, 3, 0.1, rng)
    for nm, x in [("square +/-SIG0", x_adv), ("natural OU    ", x_nat)]:
        dd = agent_rand(x, k, s)
        print(f"    k={k:4.0f} fresh sign, {nm}: pooled 1-h slope {pooled_slope(dd, 0.5+x, [d0lag])/c:6.2f} c;"
              f" ledger pooled block metric {block_metric(dd, 0.5+x)/c:6.2f} c;"
              f" worst 60-s window {window_metric(dd, 0.5+x)/c:7.1f} c (k=0: {window_metric(agent_rand(x, 0, s), 0.5+x)/c:5.1f} c)")
    # closed-loop exploiter that sees the agent's face
    x = np.zeros(T); dd = np.zeros(T); hold = 1
    for tt in range(T):
        if tt >= d0lag + 1:
            prev = x[tt-1-d0lag]
            shat = np.sign((dd[tt-1]-c*prev)*prev) if prev != 0 else 0
            amp = 0.1 if shat > 0 else 0.005
        else: amp = 0.05
        x[tt] = amp*rng.choice([-1, 1])
        if tt >= d0lag: dd[tt] = (c + k*s[tt])*x[tt-d0lag]
    print(f"    k={k:4.0f} fresh sign, closed-loop exploiter (reads last sign, modulates amplitude): pooled {pooled_slope(dd, 0.5+x, [d0lag])/c:6.2f} c")
    s2 = np.repeat(rng.choice([-1.0, 1.0], T//20+1), 20)[:T]  # sign held for 2 s
    x = np.zeros(T); dd = np.zeros(T)
    for tt in range(T):
        if tt >= d0lag + 1:
            prev = x[tt-1-d0lag]; shat = np.sign((dd[tt-1]-c*prev)*prev) if prev != 0 else 0
            # partner knows the agent's sign at t-1; it holds 2 s, so it predicts s at t+d0lag-? only when within segment
            amp = 0.1 if shat > 0 else 0.005
        else: amp = 0.05
        x[tt] = amp*rng.choice([-1, 1])
        if tt >= d0lag: dd[tt] = (c + k*s2[tt])*x[tt-d0lag]
    # exploiter's amplitude choice at time tt-d0lag is made knowing s at tt-1-? ; within a 2-s segment it is the same sign
    print(f"    k={k:4.0f} sign held 2 s,  closed-loop exploiter: pooled {pooled_slope(dd, 0.5+x, [d0lag])/c:6.2f} c")

# ---------------------------------------------------------------- K4
print("\nK4  closed loop with a high-gain mirroring partner: the dyad locks for any c > 0; the agent's share is <= c x his deviation")
def lockrun(cg, K, seed, T=6000):
    r = np.random.default_rng(seed); a = np.full(T, 0.5); p = np.full(T, 0.5); own = ou(T, 2, 0.004, r)
    for tt in range(5, T):
        p[tt] = np.clip(0.5 + K*(a[tt-3]-0.5) + 0.01*r.standard_normal(), 0, 1)
        a[tt] = np.clip(0.5 + cg*(p[tt-5]-0.5) + own[tt], 0, 1)
    return a, p, own
for K in [10.0, 40.0]:
    res = []
    for sd in range(6):
        a, p, own = lockrun(c, K, sd); dev = (a - 0.5 - own)[-2000:].mean(); res.append((p[-2000:].mean(), dev))
    print(f"    c={c}, partner gain K={K:4.0f} (loop gain {c*K:.1f}): final partner means "
          + ", ".join(f"{m:.2f}" for m, _ in res) + "; agent partner-caused offset "
          + ", ".join(f"{dv:+.3f}" for _, dv in res) + f"  (c x 0.5 = {c*0.5:.3f})")

