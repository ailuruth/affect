# Synthesis: controllability, agency attribution, and wanting against liking in one core

Scope: the two derivation obligations that emotion-elements-synthesis.md marks as hardest (rows 9 and 11):
- (a) agency and coping potential;
- (b) the dissociation of wanting from liking.

For each, this note sets out which precise computational definitions exist, how each could fall out of a single core's equations with satiable drives and no named emotion variables (Principles 1, 2, 5, 6, 10), the ablation that separates it, and what stays open.

Notes from this pass (each states how much of its source was read):
- Controllability: maier-seligman-2016-learned-helplessness-at-fifty.md, huys-dayan-2009-bayesian-behavioral-control.md, dorfman-gershman-2019-controllability-pavlovian-instrumental.md, ligneul-2022-stress-sensitive-controllability-inference.md.
- Agency: blakemore-wolpert-frith-2002-awareness-of-action.md, synofzik-2008-2013-agency-cue-integration.md, haggard-2017-sense-of-agency.md.
- Appraisal, as measured: smith-ellsworth-1985-appraisal-patterns.md, kuppens-2003-appraisal-basis-anger.md, lerner-keltner-2001-fear-anger-risk.md.
- Wanting and liking: dayan-berridge-2014-model-based-pavlovian.md, berridge-2012-prediction-error-to-incentive-salience.md, robinson-berridge-2008-incentive-sensitization.md.
- Earlier notes used: zhang-berridge-2009-incentive-salience-model.md, berridge-2004-motivation-concepts.md, berridge-kringelbach-2015-pleasure-systems.md, moors-2013-appraisal-theories.md, watson-1997-contingency-two-indices.md, contingency-causal-synthesis.md, yoshida-sprekeler-gutkin-2025-hrrl.md, hesp-2021-deeply-felt-affect.md.

## 0. Setting

The minimal core assumed below:
- **Body and drive.** A body state b ∈ ℝⁿ with satiable drive D(b), for example D(b) = Σ_i d_i(b_i − b_i*) with d_i convex and minimal at the setpoint (HRRL form).
- **Learned generative model:** p(x_{t+1}, b_{t+1} | x_t, b_t, u_t, a_t^p; G, θ). Here x is the exteroceptive and partner state, u the agent's own action, and a^p the partner's action as the agent infers it.
- **Causal structure G.** G marks which parents (u, a^p, an exogenous or "world" term) feed which children (each b_i, and the partner's expressive channels).
- **Policy and inference.** Policies are chosen by expected drive reduction under the posterior over (G, θ), with a precision (inverse temperature) γ. Perception is posterior inference in the same model.

Nothing below adds a variable outside this. Every quantity is a posterior, an expectation or a gradient of D under the model.

## 1. Controllability and coping potential: available definitions

| # | Definition | Source | What it measures | Valence-free? |
|---|---|---|---|---|
| C1 | ΔP = P(O\|R) − P(O\|¬R) | Maier & Seligman 2016 (the 1976 definition); Watson's two indices | Contingency of one outcome on one response | yes |
| C2 | TE = H(S'\|S) − H(S'\|S,A) = I(A; S' \| S). Online proxy: Ω ← Ω + α_Ω(P(s'\|s,a) − P(s'\|s) − Ω), ω = σ(β_Ω(Ω − thres_Ω)) | Ligneul et al. 2022 | How much one's action adds to predicting the next state, beyond the state itself; separates control from predictability | yes |
| C3 | Posterior log-odds of an action-free against an action-conditioned predictor, L, with w = σ(L) weighting Pavlovian (cue) against instrumental value | Dorfman & Gershman 2019 | Bayesian structure comparison; the weight on cue-driven value | yes |
| C4 | χ = share of reinforcement (punishment folded in as safety) reachable by a reliable action; hierarchical prior p(χ) shared across environments | Huys & Dayan 2009 | Controllability of *value*, with a generalising prior ("locus of control") | reinforcement-weighted |
| C5 | Prospective coping potential C = E[max_π Q(π)] − E[Q(π_rest)], separate from retrospective "was my past act causal" | My definition, from Kuppens 2003 (anger goes with future, not past, control) and Smith & Ellsworth's anticipated effort (anger 0.53, sadness −0.14) | Whether acting now can still reduce the need | in drive units |

**Agency attribution, available definitions:**
- A1: forward-model comparator e = y − ŷ(u). Small e means self-caused (Blakemore, Wolpert & Frith).
- A2: reliability-weighted posterior over authors P(k | cues) ∝ P(k)·Π_i p(cue_i | k) (Synofzik et al. 2013). Two levels: the feeling (sensorimotor likelihoods) and the judgement (priors from context and belief).
- A3: partner agency as I(A^p; S' | S, A_self). This extends C2 by conditioning on the partner's act (the Ligneul fork's extension; not in the paper).
- A4: the measured human structure. Agency is two axes (Smith & Ellsworth 1985): self against other responsibility/control, and situational (impersonal) control.
  - Sadness: situational control +1.15. Anger: −0.94 on self-responsibility, i.e. other-caused, and −0.96 on situational control.
  - Situational control alone classifies the six core unpleasant emotions at 40.6%, against 41.7% with all six dimensions (chance 16.7%).

Haggard (2017) separates three things that these definitions mix:
- instrumental agency (C1–C3);
- social attribution (A1–A4);
- self-efficacy (C4–C5), which he excludes.

The core must produce all three, and they come apart under ablation.

## 2. How (a) falls out of the core: one object, edge posteriors in G

The proposal: **controllability and agency attribution are both posteriors over edges in the core's causal structure G.** Coping potential is the value of acting under that posterior.

1. **Instrumental controllability of need i:** χ_i := P(u → b_i | data), or its graded form I(U; Δb_i | x, b) under the posterior model.
   - This is C2 restricted to need-relevant children and C3 computed per channel.
   - Because it is computed per child b_i, it is need-specific for free, matching the per-need κ_i in Zhang & Berridge.
   - The hierarchical prior over edge strengths, shared across contexts, is Huys & Dayan's χ prior. It produces helplessness transfer, immunization (Maier) and the carry-over bias (Lerner & Keltner) without new machinery.
2. **Agency attribution of a change Δ:** the responsibility of each parent for Δ under the posterior, r_k = P(parent k explains Δ | data) for k ∈ {self, partner, world}.
   - This is A2 with the precisions the core already carries (element 7).
   - A3 gives the graded partner term.
   - The comparator of A1 is the special case where only the self channel has a sharp likelihood (efference copy). That explains why the self is appraised first: "the self is only responsible when the situation is not".
3. **Coping potential:** C_i = E_{G,θ}[max_π E(−ΔD | π)] − E_{G,θ}[E(−ΔD | π_rest)], minus action cost.
   - As χ_i → 0 the Q-values flatten (Huys & Dayan), and C_i falls to minus the action cost. With any positive cost of acting, rest becomes optimal. This is passivity derived, not added.
4. **Pavlovian against instrumental balance is model averaging.** If the action value is the posterior mixture over G, then V = P(no u-edge)·V_cue + P(u-edge)·V_instr. This is exactly Dorfman & Gershman's w = σ(L) arbitration. Low control raises cue-driven responding with no arbitration module.
5. **Anger-like against sadness-like regions as readouts.** After a goal-incongruent change in need i:
   - High r_partner with high C_i is the approach or protest region.
   - High r_world with low C_i is the withdrawal region.
   - High uncertainty with low C_i is the vigilance or avoidance region (fear; Lerner & Keltner: individual-control appraisal 0.68 against −0.51, F(1, 59) = 28.37).
   - None of these is a variable. Each is a region of the (r, C, uncertainty) part of the posterior, and the face and policy read them out.
   - Kuppens 2003 adds that the mapping must be **soft**: no component is necessary or sufficient (all φ well below 1).
6. **Developmental order comes for free.** Before the partner and world parents are separated in G (early in learning), r_partner and r_world are not identifiable. Distress is then one region, and it splits only once the structure is learned. This is the Moors 2013 prediction, now a consequence of structure learning.

**Ablations for (a), each derived from the equations above:**

| Ablation | Predicted change | Human or animal anchor |
|---|---|---|
| Remove the u-parent (spectator model only) | No controllability estimate. No switch between controllable and uncontrollable regimes. No helplessness transfer. Behaviour insensitive to contingency | Ligneul: actor-only model loses 72.1% to 66.5% tracking |
| Merge the partner and world parents | Protest and withdrawal after losses become indistinguishable in the latent. Decoding of approach against withdraw falls toward chance | Smith & Ellsworth Table 7 (situational control does the work) |
| Use I(A; S') (mutual information) instead of I(A; S' \| S) | The agent credits itself with control over a mimicking partner or a shared driver | contingency-causal-synthesis.md (closed-loop bias) |
| Remove the efference copy from ŷ | The partner's mirroring of the agent is not attenuated and is classed as partner-initiated | Blakemore et al.: passivity, lack of self-tickle attenuation |
| Make the χ prior per-context (no shared node) | No immunization, no helplessness transfer, no carry-over to unrelated forecasts | Maier (PL protein-synthesis block removes immunization only); Lerner & Keltner |
| Fix the mixture weight on V_cue | Pavlovian bias no longer tracks controllability | Dorfman & Gershman (fixed-w model loses, exceedance probability > .99) |
| Set action cost to 0 | Low control no longer produces passivity; only exploration stops | Maier: passivity requires the default integrator |
| Remove the prospective (action-conditional) prior and keep only realized outcomes | Attribution follows each outcome and loses its dependence on block contingency | Haggard: schizophrenia loses the 75%-vs-50% prospective effect |

## 3. Wanting against liking: available definitions

- **W1 (Zhang et al. 2009; Berridge 2012):** Ṽ(s_t) = r̃(r_t, κ) + γV(s_{t+1}), with r̃ = κ·r (gain) or r + log κ (sign-flipping, rank-preserving). κ is need-specific and applied at retrieval; the cached V is not rewritten.
- **W2 (Dayan & Berridge 2014):** model-based Pavlovian value V(s_t, m̃) = Σ_τ T^τ r(s_{t+τ}, m̃), the outcome value recomputed under the current motivational state m̃.
  - κ is then a one-step shortcut that requires the outcome's identity.
  - Salt-cue approach rose more than 10× on the first trial of a never-experienced salt appetite, with no relearning.
- **W3 (Robinson & Berridge 2008):** sensitization is a rise in the gain on cue-triggered wanting that is spaced-exposure-dependent, context-gated and long-lasting, with liking unchanged.
- **Liking (Berridge & Kringelbach 2015; Berridge 2012):** the hedonic impact at consumption, computed in hotspots. It is intact after the loss of about 98–99% of dopamine, while wanting is gone.

## 4. How (b) falls out of the core

Two quantities share the same drive D but enter at different places.
- **Liking, realised:** ℓ_t = D(b_t) − D(b_{t+1}) at consumption, the realised drive reduction (HRRL reward). It is the learning signal: the cached predictions Ê are updated only from ℓ.
- **Wanting, anticipated and cue-triggered:** w(c) = g · E_{model}[ℓ | c, b_t] ≈ g · (−∇_b D(b_t) · Δ_{o(c)}) to first order.
  - Δ_{o(c)} is the predicted body effect of the outcome the cue c signals.
  - The gradient term is Zhang's κ, derived: it is the slope of the drive along the outcome's effect. It is automatically need-specific, zero at the setpoint (satiable) and sign-flipping past the setpoint. It needs outcome identity, which is Dayan & Berridge's point: a model-free cached scalar cannot produce it.
  - g is a gain on cue-triggered predicted value that steers attention and approach. It does not multiply ℓ.

Why this is one core and not two modules:
- Both terms are functions of the same D and the same generative model.
- They differ only in (i) evaluation time (predicted against realised), (ii) representation (model-based identity against sensed body change), and (iii) the gain g, which acts only on the predicted term.
- When g = 1 and the body state equals the training state, w is exactly the expected ℓ. In ordinary conditions wanting looks like learned prediction, which is why Berridge says only a never-seen body state or a gain manipulation separates them.

**Where g comes from without naming it.** The best-grounded candidate is the **precision of the cue-to-outcome prediction used in action and attention selection**: the policy precision γ of active inference, or the inverse temperature of the softmax over cue values.
- This is a core variable, updated from prediction reliability.
- Berridge 2012 constrains its form: a dopamine rise alone did not create wanting without a cue, so g multiplies the cue's prediction and is not added as general arousal.
- A second, independent contribution comes from §2.4: under low controllability, model averaging shifts weight onto cue-driven value. So (a) and (b) interact: uncontrollable situations amplify cue-triggered wanting relative to instrumental value.

**Double-dissociation ablation.** Run it in a body state never experienced in training (first-ever depletion of one need), because that is the only regime where wanting and expected liking can diverge without a gain manipulation.
- (i) Set g → 0 on the predicted term. No approach to the cue and no cue-driven boost to ongoing action (PIT). ℓ on contact and new learning stay intact. This is the 6-OHDA pattern.
- (ii) Remove the realised term (no ℓ readout and no update from it). Approach to the cue continues on the first trials, because w is computed from the model, then fades as nothing refreshes Ê. The readout on contact is gone.
- (iii) Replace the model-based gradient term with a cached scalar. No first-trial revaluation under a novel need. Selectivity across needs is lost: one shared κ raises every cue.
- (iv) Drive-shape test, a prediction from the Dayan & Berridge note's derivation. With a quadratic d_i, the rank order of intensities of the same outcome (mild against intense salt) can invert under large deficits. Berridge reports the rank preserved. That favours a shape whose gradient scales intensities monotonically, or the log-additive form r + log κ.

**Principle 6 hazard.** Robinson & Berridge describe exactly the non-satiable term Principle 6 forbids: a gain that grows with repeated, spaced cue exposure and lasts for years. If the partner is a cue, a g that rises with exposure to the partner is a flattery and attachment trap. Required constraints:
- g may depend on prediction reliability and on controllability, but not on exposure count.
- g must stay bounded by the drive gradient, so that w → 0 at the setpoint whatever g is.
- A logged check: with the body at setpoint and repeated partner cues, the ratio of wanting to liking must not drift upward.

## 5. How (a) and (b) meet

- Coping potential supplies the means and wanting supplies the goal (Robinson & Berridge's distinction). In one action value: Q(u) = P(u-edge)·Q_instr(u) + P(no u-edge)·g·V_cue.
- The four corners are regions, not labels:
  - High g, low control: cue-driven pursuit without an effective means. A craving-like or protest-like region.
  - Low g, low control: passivity. A helplessness-like region.
  - High g, high control: effortful approach.
  - Low g, high control: indifference with capacity intact.
- Maier's finding that control changes behaviour and DRN 5-HT but not the HPA axis has a counterpart here. Controllability acts on the policy and on the approach/withdraw readout. It does not act on D. **The body variables' setpoints and the drive are not changed by control. Only what the agent does about them is.** This is a strong, testable constraint: an engine in which controllability feeds back into D violates it.

## 6. Open problems

1. **Which prior?** Maier says passivity is the unlearned default and control is learned. Huys & Dayan's normative account favours a prior of high control. With a positive action cost and an infant that starts with no learned edges (Haggard Box 2), the core reproduces Maier's default. The prior and the action cost are then free parameters with large behavioural consequences, and no source fixes their values.
2. **The exploration trap.** Estimating I(U; S' | S) needs varied actions. A low-control agent stops acting and so stops collecting the evidence that would correct its belief: helplessness is self-sealing. This is faithful to humans, but in the engine it would freeze a mistaken belief that the partner cannot be influenced. Whether a curiosity term (another derivation obligation) breaks the trap without becoming a reward for the partner's attention is not settled.
3. **Closed-loop identifiability with a mimicking partner.** Conditioning on S removes some confounding, but a partner who reflexively follows the agent still inflates both the self edge and the partner edge. contingency-causal-synthesis.md's instrument (the agent's own exogenous variation) is needed, and it is reduced exactly when controllability is low (problem 2).
4. **Where liking lives in an active-inference core.** Hesp et al.'s affective charge is a change in policy precision, so it sits on the *wanting* (g) side of §4. If the project reads valence from it, valence will track wanting, against Berridge's evidence that pleasure survives the loss of dopamine. A separate readout of the realised ℓ is needed, and the core must say which one the face shows.
5. **Retrospective against prospective control.** Kuppens's data suggest that "could I have changed it" goes with shame and "can I still change it" with anger. Both are computable: the self edge's responsibility for the past change, and C_i. Whether the core's readouts keep them apart, or blur them, is untested.
6. **Valence as an agency cue.** Synofzik et al. and Haggard report that positive outcomes raise self-attribution. In a precision-weighted posterior this can arise if valence modulates precision. It would also produce self-serving attribution of bad outcomes to the partner, which feeds the protest region. It has to be measured, not tuned away or tuned in.
7. **Evaluation without toy worlds.** The brief rules out self-built worlds. The candidate published tests are tasks used as published:
   - Dorfman & Gershman's Go/No-Go with varied controllability;
   - Ligneul's counterfactual-prediction task;
   - Huys & Dayan's helplessness transfer paradigm;
   - Berridge-style first-ever-depletion revaluation, which has no human published task with open data that I found.

   Whether their data are released was not checked. For the dyadic case, no published dataset carries ground-truth controllability or attribution labels. Partner agency and controllability in Seamless-type data can only be tested indirectly, for example by checking that the agent's estimate tracks surrogate-shuffled contingency.
8. **Social attribution against instrumental agency: which comes first?** Haggard leaves it open. In the core, both are edges of G learned together. Whether self-edge learning must precede partner-edge learning, as Moors's developmental claim and the comparator's precision advantage suggest, is a prediction, not an assumption.
