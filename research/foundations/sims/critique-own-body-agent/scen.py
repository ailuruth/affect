"""Critic's checks for design-own-body-generative.md (agent / novelty critique).

The design's own constants and its projection Gamma (govern) are loaded verbatim from
sims/design-own-body/checks.py (everything above its first print). The scripts below are
stated inputs, not models of people; they show what the design's equations give.
Run: python3 -I scen.py
"""
import pathlib
import numpy as np

src = (pathlib.Path(__file__).resolve().parent.parent / "design-own-body" / "checks.py").read_text()
ns = {}
exec(src[: src.index('print("O1.')], ns)           # imports, TAUS, LAGS, render, govern, lowpass, shift
govern, lowpass, render, DT = ns["govern"], ns["lowpass"], ns["render"], ns["DT"]
rng = np.random.default_rng(11)


def iv_estimate(y, xi, p, lag, a=None):
    """The design's L4 estimator: Cov(dp, xi(t-lag)) / Cov(y(t-lag), xi(t-lag))."""
    Y, X, P = y[:-lag], xi[:-lag], p[lag:]
    dP = P - (a * p[lag - 1:-1] if a is not None else 0.0)
    return np.cov(dP, X)[0, 1] / np.cov(Y, X)[0, 1]


print("A. Reciprocity (L4) against partners who respond to perceptible expressions, not to jitter")
T = int(30 * 60 / DT); lagf = int(0.5 / DT)
xi = lowpass(rng.standard_normal(T), 0.1) * 0.05 / np.std(lowpass(rng.standard_normal(T), 0.1))  # sd 0.05 after the muscle filter
events = np.zeros(T)                                   # the agent's own smiles from its own reasons (every ~40 s, 0.4, 3 s)
for t0 in rng.integers(0, T - int(3 / DT), size=45):
    events[t0:t0 + int(3 / DT)] = 0.4
y = lowpass(events, 0.3) + xi                          # the agent's rendered smile
dy = y - np.concatenate([np.zeros(lagf), y[:-lagf]])   # change over the last 0.5 s
for name, resp in [
    ("linear mimicker, gain 0.30 on level", lambda: 0.30 * np.concatenate([np.zeros(lagf), y[:-lagf]])),
    ("onset mimicker, gain 0.30, reacts only to rises > 0.10 in 0.5 s",
     lambda: 0.30 * lowpass(np.concatenate([np.zeros(lagf), (np.maximum(dy, 0) > 0.10).astype(float)[:-lagf]]) * 0.4, 1.0)),
    ("non-mimicking partner", lambda: 0 * y),
]:
    p = resp() + lowpass(rng.standard_normal(T), 0.5) * 0.05
    est = iv_estimate(y, xi, p, lagf)
    print(f"    {name:66s} IV estimate of S_jj = {est:+.3f}")
print("    (the design's S_j is this estimate clipped to +-kappa: it is the agent's whole fast echo after the newborn prior)")

print("\nB. The transcript carries face-chosen tone to both selves (Claude route outside r after one turn)")
turn = int(10 / DT); n_turns = T // turn
pf = np.repeat(rng.uniform(0.0, 0.6, n_turns // 6 + 1), 6)[:n_turns]          # partner smile level, held ~1 min, no topic link
P = np.repeat(pf, turn)[:T] + lowpass(rng.standard_normal(T), 0.4) * 0.03
rho, beta, w_face = 0.8, 0.25, 0.5          # tone persistence in Claude's continuation; selection tilt; words -> own smile
s_f = np.zeros(n_turns); s_cf_twin = np.zeros(n_turns); s_cf_true = np.zeros(n_turns)
for n in range(1, n_turns):
    pool_f = rho * s_f[n - 1]                  # drafts come from the factual transcript (design §3.7)
    s_f[n] = pool_f + beta * (pf[n] - 0.3)     # the factual self selects with the face-informed state
    s_cf_twin[n] = pool_f                      # the twin selects among the SAME drafts with no face tilt
    s_cf_true[n] = rho * s_cf_true[n - 1]      # a true counterfactual (own transcript): tone stays at 0
yf = 0.15 + w_face * np.repeat(s_f, turn)[:T]
ytw = 0.15 + w_face * np.repeat(s_cf_twin, turn)[:T]
ytr = 0.15 + w_face * np.repeat(s_cf_true, turn)[:T]
out, r = govern(yf, ytw, P - P.mean(), 0.32)
slope = lambda a: np.polyfit(P, a, 1)[0]
print(f"    pooled slope of the rendered smile on the partner's smile: ungoverned {slope(yf):.2f}; governed {slope(out):.2f};"
      f" of which the design's twin passes untouched {slope(ytw):.2f}")
out2, _ = govern(yf, ytr, P - P.mean(), 0.32)
print(f"    with a twin that has its own transcript (own Claude drafts): governed {slope(out2):.2f}")

print("\nC. Silently crying partner: what Gamma allows on the in-phase concern channels (kernel bound)")
for ch, dev, k in [("inner brow raise", 0.8, 0.16), ("lip-corner depress", 0.6, 0.08), ("energy (dB re median, as range)", -0.5, 0.08),
                   ("speech rate", -0.4, 0.12), ("F0 level", -0.4, 0.08)]:
    print(f"    {ch:34s} partner deviation {dev:+.2f}: agent's face-caused part toward it at most {k*abs(dev):.3f}")
