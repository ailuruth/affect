# Synthesis: telling what answers me from what I follow

Scope: how infants, robots and identification theory separate events that are contingent on one's own acts from events one merely follows, and how an agent can learn a causal partner model from its own interventions during live interaction. Written for the closed-loop flaw found in critique-design-dyadic-sheaf.md (Theorem 5(b), counterexample C13): a regression of the partner on the agent's own trace learned R = 9.5 from a partner who never responds, and R = 2.1 even with a strictly lagged trace. Any engine that learns mimicry and reading of others by living (brief.md, Long-term goal; face-development-synthesis.md §3-4) faces the same flaw.

Notes from this pass (each says how much of its source was read):
- Infant side: watson-1997-contingency-two-indices.md, bahrick-watson-1985-proprioceptive-visual-contingency.md (rewritten from the primary; the earlier version was secondary-only), rochat-morgan-1995-spatial-self-perception.md (with Rochat 1998), beebe-2016-self-interactive-contingency.md (stand-in for Tarabulsy, Tessier & Kappas 1996, abstract only), nadel-1999-expectancies-social-contingency.md (abstract only), murray-trevarthen-1985-double-video.md (primaries unread; paradigm from replications), rochat-neisser-marian-1998-interpersonal-contingency.md, striano-2005-social-contingency-1-3-months.md.
- Robots: gold-scassellati-2009-robot-self-recognition.md, stoytchev-2011-self-detection-temporal-contingency.md.
- Identification and causal inference: forssell-ljung-1999-closed-loop-identification.md, hernan-robins-2020-what-if-iv-gmethods.md, scholkopf-2021-causal-representation-learning.md, jaques-2019-social-influence-intrinsic-motivation.md, seitzer-2021-causal-influence-detection.md.
- Earlier notes used: gergely-watson-1996-social-biofeedback.md, barnett-barrett-seth-2009-granger-te-equivalence.md, james-barnett-crutchfield-2016-information-flows-critique.md, oudeyer-kaplan-hafner-2007-iac.md, burda-2019-large-scale-curiosity.md, ray-heyes-2011-wealth-of-the-stimulus.md, cook-2014-mirror-neurons-origin.md, murray-2016-functional-architecture-mother-infant.md.

## 1. The confound, stated formally

Discrete time, scalar for clarity (each symbol becomes a matrix per channel in the engine):

- Agent: x_t = f·z_{t−1} + g·h_t + b_t. Here f is the agent's own following (reflex mimicry, the ρ/κ pulls, facial feedback), h_t is a hidden common driver (topic, room sound, Claude's words that both people hear), and b_t is the agent's own exogenous variation.
- Partner: z_t = r·x_{t−d} + a·z_{t−1} + c·h_t + ε_t. Here r is the partner's causal response to the agent at lag d (the quantity wanted), a is the partner's own persistence, and ε_t is the partner's own innovation.
- Agent's reading of the partner: ẑ_t = z_t + ν_t.

The target is r = ∂E[z_t | do(x_{t−d})]/∂x. In closed-loop identification terms (forssell-ljung) the partner is the plant, the agent's following is the regulator, the partner's own dynamics are coloured noise, and b is the external reference signal.

**Naive regression** (the design's (L_R)). With r = 0, c = g = 0, ν = 0, z is AR(1) with variance σ_z² = σ_ε²/(1 − a²), and

  r̂_naive = Cov(z_t, x_{t−d}) / Var(x_{t−d}) = f·a^{d+1}·σ_z² / (f²σ_z² + σ_b²).

This is nonzero at every lag, because the partner's persistence a carries the agent's following of the past partner into correlation with the present partner. As σ_b → 0 it tends to a^{d+1}/f: the agent's own following, inverted and discounted by the partner's autocorrelation. That is exactly the critique's diagnosis. Lagging further only multiplies by a per step, which is why a strictly lagged trace still gave R = 2.1 in C13. Our toy check (a = .95, f = .8, d = 3) predicts 0.883 at lag d and 0.719 at lag d + 4; the simulation gives 0.883 and 0.719 (§5).

The general version is Forssell & Ljung's bias pull for the direct method, B = (H₀ − H_θ)Φ_eu Φ_u⁻¹. It is zero in open loop (Φ_eu = 0) and, in closed loop, only when the model of the partner's own dynamics H is exactly right. Their variance result says the same thing from the other side: Cov Ĝ ≈ (n/N)·Φ_v/Φ_u^r. **Only the part of the agent's expression that comes from the external reference (b) carries information about the partner's response; the part produced by following carries none.**

**Watson's indices do not escape it.** Sufficiency P(partner event in (τ, τ+t] | own act at τ) and necessity P(own act in [τ−t, τ) | partner event) are each compared with an unconditional base rate (watson-1997). Necessity drops when the partner's events have other causes. It does not ask whether the agent's act was itself caused by the partner. With following plus bursty partner behaviour, sufficiency rises above base rate with no path from agent to partner. Watson's examples (kicking a mobile, an experimenter pulling a ribbon) all assume that the response is generated independently of the stimulus. That assumption is the identifying condition.

**Conditioning on the partner's past (Granger/ARX) is not enough either.** It removes the C13 route when the partner's state is fully observed. It reopens bias in two common cases:
- A hidden, persistent partner state U makes z_{t−1} a collider on x_{t−d−1} → z_{t−1} ← U → z_t (hernan-robins ch. 20, treatment–confounder feedback; Table 20.1: true effect 0, stratified −8, g-methods 0).
- The agent reads the partner with noise, so the control is incomplete (errors in variables).
- Same-frame coupling is invisible to any lagged method.

## 2. Identification strategies

Ordered by how much they assume. The first four are the ones that work under hidden partner state.

1. **Own exogenous variation as an instrument** (forssell-ljung, the IV/projection route; hernan-robins ch. 16).

   r̂_IV = Cov(ẑ_t, b_{t−d}) / Cov(x_{t−d}, b_{t−d}),  matrix form R_IV = Σ_{z b}(d) Σ_{x b}(d)⁻¹.

   With r = 0, Cov(z_t, b_{t−d}) = 0 exactly, whatever the following gain, the partner's persistence, hidden drivers or reading noise. The agent can do this where an outside observer cannot, because it owns b: it is logged by efference, not inferred. Conditions, translated:
   - **Exchangeability:** b is drawn independently of the partner. Use a dedicated random source. Do not use a body rhythm that can entrain to the partner, such as breathing, or anything computed from partner input.
   - **Exclusion:** b reaches the partner only through the modelled channels. If b moves voice or head as well as face, either include those channels in x or give each channel its own independent b.
   - **Relevance:** Cov(x, b) must be large; track the first-stage F per channel and do not update R when F is small (F ≪ 10 makes IV useless; hernan-robins; fork C's numpy run with σ_b = 0.05 gave F ≈ 1.5).
   - **Visibility, a fourth condition specific to this setting:** b must be perceptible to the partner. Invisible micro-variations identify r = 0 for the invisible margin even when the partner responds to larger expressions. The IV estimand is local to where b moves x (a LATE-like weighted effect), so probes are needed at more than one amplitude.
   - Controls are allowed if they are not descendants of b: partner history up to t − d_min, the shortest response lag. They do not restore bias and they shrink variance (§5, "IV + controls").
   - The online form is a one-symbol change to the design's rule. The design uses dR/dt = η P (z_y − R x̃_τ) x̃_τᵀ. The instrumental version is dR/dt = η P (z_y − R x̃_τ) b̃_τᵀ (recursive or instrumental LMS). Its fixed point is E[(z − Rx) bᵀ] = 0, that is, R = Σ_zb Σ_xb⁻¹. Because b enters x additively, Σ_xb = Σ_b ≻ 0 and the update is well posed.

2. **The agent knows its own policy** (hernan-robins ch. 19-21; forssell-ljung's indirect method with a known regulator). If x_k = g(history) + b_k with a known density for b, the propensity f(x_k | history) is known exactly. Inverse-probability weighting, W = ∏ 1/f(x_k | history), then identifies the effect without any model of the partner's dynamics. Sequential exchangeability holds by construction. **Positivity:** the agent must never follow deterministically, because every expression level needs nonzero probability in every history.

3. **Breaks in the loop.** Each removes or changes one arrow while keeping marginal statistics:
   - **Partner replay**, the double video (murray-trevarthen; nadel-1999; rochat-neisser-marian-1998). The partner's recorded stream is shown with form, rate and affect unchanged and dependence on the agent removed. A correct estimator must collapse to about 0. The trace regression will not, because the agent still follows the replay.
   - **Self replay**, the 1986 mother condition. The partner is shown the agent's earlier face, so any remaining "responds to me" is the confound measured directly. This deceives the person, so use it only offline with consenting testers.
   - **Delay probe** (Henning & Striano, in the double-video note). A 1-s delay of one stream should shift a real response lag by 1 s. An artefact of autocorrelation barely moves.
   - **Natural breaks.** Whenever the partner cannot see the agent (gaze off-screen, camera blocked), the visual arrow agent → partner is cut. R_visual estimated in those stretches should be about 0, which gives a free online test.
   - **Agent-side breaks.** Switching the following gain f between regimes, or a nonlinear regulator, makes closed-loop data informative (forssell-ljung). Brief holds (do(x = const)) are the agent's own still face.

4. **The invariance self-check** (scholkopf-2021, independent mechanisms). The partner's mechanism z | do(x) must not change when only the agent's own mechanism changes. Refit R in high-following and low-following stretches. A difference means the agent's following has leaked into R.

5. **Lag structure with the partner's own history** (beebe-2016; ARX/Granger). Predict the partner from their own past and the agent's past in one model. This is cheap, interpretable, and right when the partner's state is fully observed. Use it as a first pass and as a cross-check against IV; disagreement signals hidden partner state. It cannot handle common drivers, noisy reading or same-frame coupling (§1, §5). Transfer entropy inherits the same limits (barnett-barrett-seth: F = 2·TE for Gaussians; james-barnett-crutchfield).

6. **Self by perfect contingency at a known delay** (bahrick-watson, watson-1997, stoytchev-2011, gold-scassellati-2009). For the self channel the problem is easy because the agent's efference is observed. The steps:
   - learn the efferent-afferent delay alone (Stoytchev: μ = 1.03 s from babbling, unchanged with an uncorrelated second robot in view);
   - freeze it, because a 0.66-s mimic present during learning made the delay histogram bimodal and gave a wrong μ = 1.36 s, while with μ frozen the mimic's indices were near 0;
   - label as self what has sufficiency ≈ necessity ≈ 1 inside a ±25% window, computed per command type and corrected for visibility.

   Gold & Scassellati score self as P(M_t | Φ_t) with the own motor command Φ observed, and other as the same model with Φ hidden, over the whole history.

7. **Counterfactual influence as a readout** (jaques-2019, seitzer-2021). Two measures:
   - Jaques: c = Σ_j KL[p(z | x, s) ‖ Σ_x̃ p(z | x̃, s)p(x̃)];
   - Seitzer: C(s) = I(S′; A | S = s).

   Both are the right quantities for "how much do I move this partner, here". Both are causal only if the conditional model was fitted on exogenous or probe variation. Fitted on closed-loop data they inherit §1's bias.

## 3. What infants appear to use

- **Self-generated, independently timed acts.** In Watson's mobile, Bahrick & Watson's leg display and Rochat & Morgan's set-up, the contingency is tested on spontaneous kicking, so the infant's motor variability is the instrument. Infants also probe: they kick more while looking at the spatially reversed view (rochat-morgan). That is self-generated variation increasing exactly where the relation is uncertain, as in IAC (oudeyer-kaplan-hafner).
- **Felt-to-seen matching through efference and proprioception.** Bahrick & Watson's 5-month-olds looked .65-.69 of the time at the non-contingent display, with their direct view of their own body blocked. The comparison is proprioceptive and motor against visual, not visual against visual.
- **Mapping and form, not only timing.** With timing perfect, a left-right reversal is detected (looking 58-59% vs 41-42%, F(1,18) = 5.39). Delays of 0.5-3 s were not told apart from live feedback between 1 and 5 months (rochat-morgan). Contingency for the infant is a structured map, not coincidence.
- **Perfect versus high-but-imperfect contingency.** At 5 months, infants prefer the non-self (imperfect) display. 3-month-olds split bimodally: of 29 infants, 14 below .4 and 12 above .6, with no group preference. This corrects Gergely & Watson's summary that 3-month-olds preferred perfect contingency (bahrick-watson, now read).
- **A copier is not the best partner.** At 3 months, being imitated raised gaze (83.0% vs 75.9%) but lowered smiling (5.9% vs 12.4%) compared with normal reciprocal interaction. 1-month-olds showed no difference (striano-2005).
- **Social contingency breaks: the still face is robust; replay is contested at 2 months.** Murray & Trevarthen's live/replay effect came from 4 infants, with order fixed and live run to a peak. With order counterbalanced, gaze was 75.8% vs 75.3% (p = .94) (rochat-neisser-marian). Nadel et al.'s live–replay–live design (n = 10) found lower gaze and smiling in replay, with recovery in 7 of 10 (abstract only). A 1-s delay lowered gaze at 3 and 6 months but not smiling.
- **In infancy the confound is mostly avoided by the roles.** The mother follows far more than the infant does: 2.4× (gaze) to 5.7× (engagement) in partner-effect size (beebe-2016). Mothers imitate infants about once a minute, 79% of imitation episodes (face-development-synthesis). The infant's own following is weak (standardized β .025-.050). So an infant who regresses the mother on its own acts is close to open-loop and the naive estimate is roughly right. **For the engine the roles are reversed.** It has reflex mimicry and feedback loops that follow strongly, and an adult operator who follows weakly. The engine is in the regime where the naive estimate is worst, so it needs an identification strategy the infant can mostly do without.

## 4. Design implications

1. **Replace the partner-model update with an instrumental one.** Use the IV form of (L_R) in §2.1. Generate b per channel from a logged random source, at an amplitude the partner can perceive. Keep controls to partner history before t − d_min. Do not update when the first-stage F is weak.
   - This answers the critique's top fix. Its fixed point is the partner's causal response under hidden partner state and noisy reading, which Granger-style conditioning is not (§5).
2. **Keep following stochastic.** For positivity, the agent's following gain stays below 1 and b is always present. This also gives the IP-weighting route (§2.2) for free.
3. **Make innate variation a body property with a known source.** Innate micro-variation is the agent's analogue of spontaneous kicking. Its amplitude trades identifiability against naturalness: invisible variation is a weak instrument. Record the trade-off as an explicit parameter with a measured first-stage F, not a hidden constant.
4. **Learn the self channel first, then freeze its delay.** Calibrate the efferent-afferent delay of the rendered face and voice in a solo period (no partner), then freeze it. Label as self whatever passes sufficiency ≈ necessity ≈ 1 at that delay. Subtract the efference-predicted self component (including the reflex and viseme parts) before anything reaches the partner model or the disp edge. This matches critique fix 3 and Stoytchev's corruption result.
5. **Gate partner learning by visibility.** Update the visual partner map only while the partner's gaze is on the agent. The off-gaze estimate should be about 0, which is a continuous self-test.
6. **Prior on size.** Human partner effects at 1-s resolution are standardized β ≈ .02-.14, with self-effects 4-52× larger (beebe-2016). A learned partner gain of order 1 or more is a red flag, not a discovery.
7. **Treat a perfect fixed-lag copier as its own category.** A copier scores near self (Gold & Scassellati: P(self) > 0.5 in 9 of 10 runs for a human mirroring from switch-on). It should not count as the most responsive partner for any contingency need (Striano; Principle 6). Evidence of independent partner motion breaks the ambiguity: Gold & Scassellati found that 5 s of independent motion kept P(self) < 0.1 for 30 s.
8. **Use influence measures as readouts, not rewards.** Compute counterfactual influence (Jaques KL, Seitzer CAI) from the identified R, as a controllability or agency readout. Do not reward it: maximizing influence on a person is the flattery and provocation route Principle 6 forbids (jaques note; contingency-parity.md "What breaks", item 2).
9. **Acceptance tests for any partner-model learner.** Run these before trusting it in a design:
   - (a) **Autonomous-partner test.** This is C13: a partner who never responds must give R̂ → 0 within the error budget.
   - (b) **Replay test.** On a recorded partner, the estimate must collapse. Counterbalance replay order, fix interval lengths in advance, and include a live-live time control (rochat-neisser-marian).
   - (c) **Delay probe.** Delaying one stream by 1 s must shift the learned lag by 1 s.
   - (d) **Invariance under the agent's own following gain** (§2.4).
   - (e) **Hidden-driver test.** A shared slow driver with r = 0 must give R̂ ≈ 0. Granger/ARX fails this test (§5).
   - (f) **Crossed-partner test.** A partner who responds on a crossed channel must give a crossed R and, by the face-development prediction, counter-mimicry (cook, ray-heyes).

## 5. Toy check (ours; not evidence about humans)

Scalar model of §1, response lag d = 3 steps, k = 5 partner lags as controls, 50 seeds. Mean (sd) of r̂:

| case (true r) | naive | lag + 4 | Granger/ARX | IV(b) | IV(b) + controls |
|---|---|---|---|---|---|
| A: autocorrelated partner, agent follows (0) | 0.883 (0.014) | 0.719 (0.021) | 0.000 (0.007) | −0.004 (0.023) | 0.000 (0.007) |
| B: + hidden common driver (0) | 1.120 (0.002) | 1.098 (0.004) | 0.153 (0.006) | −0.018 (0.104) | 0.000 (0.007) |
| C: + noisy reading of partner, sd .5 (0) | 0.883 (0.015) | 0.720 (0.021) | 0.103 (0.013) | −0.003 (0.027) | 0.001 (0.017) |
| D: responsive partner, hidden driver + noisy reading (0.3) | 1.213 (0.008) | 1.153 (0.012) | 0.570 (0.013) | 0.297 (0.030) | 0.300 (0.017) |
| F: responsive partner, plain (0.3) | 0.449 (0.010) | 0.180 (0.014) | 0.300 (0.007) | 0.300 (0.009) | 0.300 (0.007) |
| E: weak instrument, σ_b = .1 (0) | 1.001 (0.010) | 0.815 (0.019) | 0.001 (0.020) | −0.014 (0.071) | 0.001 (0.020) |

The table shows 18,000 steps (30 min at 10 Hz). At 3,000 steps (5 min) the IV(b) + controls sds are 0.019-0.058 across cases. Parameters: a = .95, f = .8 (A-C, E); a = .6, f = .5 (D, F); σ_ε = .3, σ_b = .3 unless stated; hidden driver AR(.98) entering the partner at .3 and the agent at .5.

Reading:
- The naive and lagged regressions reproduce the critique's failure and the closed-form bias of §1.
- Granger/ARX fixes the simple case but is biased by hidden drivers and noisy reading. In D it nearly doubles the true response.
- IV on the agent's own logged variation is unbiased in every case. Partner-history controls cut its sd by 1.3-15× (most in case B).
- Fork C's independent numpy run (forssell-ljung note) agrees. ARX gave 0.03 for a true 0.2 under a hidden slow drive, and IV gave 0.02-0.35 over 5 seeds: unbiased but noisy without controls.

Core of the script (the full 45-line version adds the case table and loops over 50 seeds; run it from research/foundations/sims with `uv run python -I <path>`, since numpy lives in that project's environment):

```python
import numpy as np
def sim(T, R, a=0.95, f=0.8, d=3, sb=0.3, ch=0.0, gh=0.0, snu=0.0, seed=0):
    rng = np.random.default_rng(seed)
    z = np.zeros(T); x = np.zeros(T); h = np.zeros(T)
    b = sb * rng.standard_normal(T); eps = 0.3 * rng.standard_normal(T)
    for t in range(1, T):
        h[t] = 0.98 * h[t-1] + 0.2 * rng.standard_normal()
        z[t] = a * z[t-1] + (R * x[t-d] if t >= d else 0) + ch * h[t] + eps[t]
        x[t] = f * z[t-1] + gh * h[t] + b[t]
    return z + snu * rng.standard_normal(T), x, b
def ols(y, X):
    X = np.column_stack([np.ones(len(y))] + X); return np.linalg.lstsq(X, y, rcond=None)[0][1]
def estimates(zo, x, b, d=3, k=5):
    t = np.arange(max(d, k) + 1, len(zo))
    C = np.column_stack([np.ones(len(t))] + [zo[t-j] for j in range(1, k+1)])
    res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]
    return (ols(zo[t], [x[t-d]]), ols(zo[t], [x[t-d-4]]),
            ols(zo[t], [x[t-d]] + [zo[t-j] for j in range(1, k+1)]),
            np.cov(zo[t], b[t-d])[0, 1] / np.cov(x[t-d], b[t-d])[0, 1],
            np.cov(res(zo[t]), b[t-d])[0, 1] / np.cov(res(x[t-d]), b[t-d])[0, 1]))
```

## 6. Open problems

- **Speed versus identifiability.** IV needs minutes of data per channel (sd ≈ .02 after 5 min at σ_b equal to the partner's innovation). Some partner changes happen in seconds (Hofman's withdrawn smile return, in the critique's list). A fast detector of change (CUSUM on the IV moment) plus a slow estimator is one answer; it is untested.
- **Visibility versus naturalness of b.** Infants' spontaneous variability is large; an engine's acceptable micro-variation may be too small to be a strong instrument. Measure the first-stage F in real sessions before relying on it. This repeats face-development-synthesis's warning about adult partners' sparse mirroring.
- **Nonlinear and thresholded responses.** IV identifies a local average effect where b moves x. The response to a full expression may differ and needs multi-amplitude probes or a nonlinear IV.
- **Entrainment of b.** If the agent's innate variation comes from a body that couples to the partner (breathing, arousal), exchangeability fails. The random source must be outside every coupled loop, or its partner-driven part must be removed by efference.
- **Infant evidence is thinner than often cited.**
  - The 2-month replay effect is contested. Nadel 1999 and the Murray & Trevarthen primaries were not read in full.
  - Tarabulsy 1996 was read only as an abstract, and Watson's 1979/1985/1994 chapters not at all; Watson 1997 stands in for them.
