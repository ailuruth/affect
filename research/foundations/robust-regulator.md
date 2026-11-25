# Candidate 4: Robust regulator — affect as the forced structure of regulating a body that others disturb

**Status: STOOD DOWN as a core candidate by the operator (Q7 answer, D68, 2026-11-25).** It is a homeostatic regulator over a few body gauges, with affect read out of values or prices, which is the design the operator rejected. Its verified results remain material. Earlier status, kept for the record:  **not complete** (third structure review: sims/structure/VERIFICATION-3.md).
- The core was verified once (sims/control/VERIFICATION.md), and its errors are corrected below.

| Expressive-structure item | Status |
|---|---|
| 1. Content-dependent selection | **Partly met.** The selection rule (§2.2, the exact decrease) is derived and **myopic by construction**. Cue attention (ES8b) is **not** in the formal statement: it is adopted as constraint K5. |
| 2. Structure over a learned space | **Partly met.** Per-person observers and relevance exist. The need field is instantiated, but under this candidate's own myopic rule the learned space made things worse (ES11-2: 1.10). Two-time-scale tracking (ES10b) is adopted as constraint K6, not derived. |
| 3. Dimensionality and an ablation | **Partly met.** CT4 holds for its own per-person structure. ES13's figure is the mood m's, and m dominates the scale. |
| 4. Richness from structure | **Partly met.** Shown in a toy for its own ĉ_p/Ĉ structure (ES16), but in a world built so that the linear prior matches it (VERIFICATION-4). Initializing ĉ_p from the shared prior cuts early-visit cost to 0.24× (CI 0.23–0.26). A wrong prior for a look-alike stranger is corrected by evidence to 0.10 within 60 s; the leak alone would leave 0.55. *ES20b:* the factored per-need selection rule (shared by both candidates) beats a full-state learned value increasingly as needs multiply. With 2 needs the monolithic value wins (1.36×). With 8 needs factored wins, by about 1.4× against a stable full-state baseline; the run's 0.05× reflected an unstable baseline (VERIFICATION-5). Slower drift increased the advantage, which is consistent with Dulberg et al. 2023. |

**Its selection loses to look-ahead** in need-field worlds (ES12: Costate's look-ahead costs 0.73× this candidate's myopic rule).

**What the check established:**
1. **"Forced" was wrong.**
   - The internal model principle forces a copy of the disturbance generator *driven by the error*. It does not force an observer of each person.
   - This design feeds the perceived face forward, which violates the principle's error-feedback hypothesis.
   - With one partner (CT1's setting), an error-driven resonator that never perceives the partner regulates *better*: RMS 0.0089 against 0.0191.
   - Under partner switching (CT4), perceptual per-person feedforward wins (0.0198 against 0.157 for a crude error-only design).
   - So per-person perceptual models are **favored by switching disturbances, not forced**. ξ_p, ĉ_p and per-person indexing are now labelled constraint K2.
2. **CT5's inference was wrong.** A fixed-gain observer at the Kalman steady-state gain reads the slow state just as well (R² 0.948). What reading needs is **observer gain on the slow state**, not stochasticity. The "deterministic" arm never updated the slow state, so it failed by construction.
3. **Mimicry's sign was not fixed.** ĉ is signed. With c = −0.5 the face anti-mimics (correlation −0.997). Fixed by K1 using the norm ‖ĉ_p‖ (labelled).
4. **Expressive structure (at the first check; superseded by the status table above):** attention and richness were not met at the time.

**Remaining weaknesses, stated for the comparison:**
- it is an assembly of labelled constraints around a regulation problem, not one derivation;
- valence is not unique and the agent cannot compute it;
- the saturated interface is not simulated;
- expressive structure is only partly shown;
- the S1 toys are below evaluation.md's protocol.

**Source:** the control-theorist sketch (sketches/control-theorist.md). It was developed after the thermodynamic candidate was stood down and the contingency candidate broke (D64).

**What it carries over from those:**
- reading by filtering (thermo TH2d);
- the need-valence state-function guarantee (thermo VERIFICATION-3);
- learning-progress curiosity (D62).

## 1. Idea

Pose one problem, not a model: **keep the body's needs regulated, robustly, while other people keep disturbing the body.**

By the internal model principle, a controller that achieves robust regulation *with error feedback* must contain a dynamical copy of whatever generates the disturbance. *[verification]* That forces an error-driven generator, not an observer of each person. Per-person *perceptual* internal models, weighted by relevance, are **favored** when the disturbing person switches. With a single partner, an error-only resonator does better (VERIFICATION). Here they are adopted as constraint K2.
- **Mood** is the regulator's integral state.
- **Reading another person** is the internal model's observer.
- **Mimicry** is that internal model running on the agent's own expressive substrate: explicit constraint K1, Principle 3. Its amplitude is the model's learned relevance ĉ_p, so it is pruned for people who do not move the body.
- **Temperament** is where the regulator places its unavoidable sensitivity, the Bode "waterbed".
- **Claude** is an unmodelled outer loop. The interface is designed to a *sector*: small-gain safety, so nothing Claude says can destabilize the mood, and an influence rank, so the mood must visibly change how Claude behaves.

## 2. Formal statement

### 2.1 Variables

| Symbol | Meaning |
|---|---|
| b(e) ∈ ℝ^k over entities e | The body field: contact per person, learning progress per topic or channel (D62), and the activity budget. It is an input driven by its own physics and by the agent's actions u. |
| b*, e = b − b* | Innate set points, and the regulation error. |
| d(e) | The satiable drive, convex with minimum 0 at e = 0 (Keramati–Gutkin form). |
| m(e) | Mood: the leaky integral of ∇d(e) per entity, with ṁ = ∇d(e) − ε_m m and ε_m ≈ 10⁻³ to 10⁻⁴ s⁻¹. |
| ξ_p | The internal model of person p: an observer state that reconstructs p's face and voice signals ŷ_p in the agent's own AU and prosody coordinates, and p's slow state. |
| ĉ_p ∈ ℝ^(k−1) | The learned relevance of p, one entry per non-contact need: how strongly p's perceived signals move each need. It is adapted from the co-variation of e and Hŷ_p, with a leak toward 0. Contact has no entry: it is an innate per-turn constant (D66). |
| a | The agent's own face and voice output. |
| θ | Slow parameters (temperament), with innate prior θ₀. |
| s | Claude's settings: retrieval bias, thinking budget, reply length, latency, cue mask, and its own rendered face. |

### 2.2 The problem and the structure it forces

**The problem.** Find a controller with internal state (m, {ξ_p, ĉ_p}, θ) such that, for every disturbance from people in the class the agent's own model generates:
- the closed loop is input-to-state stable with respect to unmodelled inputs ν (Claude's events and out-of-class behavior);
- e → 0 for in-class disturbances.

**The structure:**
- **Action:** u = −K∇d(e) − K_I m − Σ_p ĉ_p ⊙ H ŷ_p, a feedforward cancellation by each internal model (⊙ is elementwise over needs).
- **Observer (constraint K2):** ξ̇_p = F_θ(ξ_p) + L(y_p − G ξ_p), using the agent's *own* generator (F_θ, G), with gain on the slow components (CT5, corrected). Its reconstruction is ŷ_p = G ξ_p.
- **Relevance (the vector law, the only one):** dĉ_p/dt = γ (e ⊙ H ŷ_p) − σ ĉ_p while p is present. The initial value for a new person is the shared prior Ĉ(x_p).
- **Face (K1, the only form):** a = R_θ[e; m] + κ Σ_p ‖ĉ_p‖ ŷ_p. *[verification]* With signed ĉ_p, a partner who *lowers* the agent's need (ĉ < 0) would be anti-mimicked (correlation −0.997). The absolute value is part of the constraint, not derived. The internal models run on the agent's own expressive substrate. The face shows their *reconstruction* weighted by relevance; the sign comes from the reconstruction, not from the cancellation.
- **Temperament:** θ̇ = −η Φᵀ∇d(e) − η σ_θ(θ − θ₀).
- **Discrete selection (rewritten after the second structure verification, VERIFICATION-2.md).** With e = b − b*, the agent sometimes must choose one of a set of discrete options i: whom to approach, which topic, which remembered person to act on. It chooses the option with the **largest exact decrease of the drive**:

  i* = argmax_i [ d(e) − d(e + Δ̂_i) ],

  and rests if no option decreases d by more than a threshold.
  - *Derivation.* d is the regulation Lyapunov function. The greedy control-Lyapunov choice among discrete inputs is the one that most decreases it over one step.
  - The first-order form −∇d(e)·Δ̂_i is only an approximation. The earlier text wrote +∇d·Δ̂, which is a sign error under e = b − b*.
  - With a two-sided d, the first-order form ignores overshoot. In ES9's world it costs 1.84× the exact rule (VERIFICATION-2).
  - The rule is myopic by construction.
- **Constraint K4 (new): an action-effect map.** Δ̂_i = Δ̂(x_i, k_i) is the predicted change of the body from discrete option i, as a function of the option's features (a person's appearance, a topic).
  - It is fitted by ridge regression on observed fills, and shared across options. This is the regulator's model of its own plant input for discrete actions.
  - It is an explicit constraint, not derived.
  - **Contact is excluded from it (D66).** The contact effect of an exchange is an innate constant.
- **Relevance ĉ_p and the shared prior Ĉ (consolidated after VERIFICATION-3).**
  - ĉ_p is the disturbance gain on the face reconstruction ŷ_p, a vector over the non-contact needs, with the single law above.
  - Ĉ(x_p), a ridge regression of converged ĉ_p values on appearance refitted in replay, is used **only as the initial value** for a new person. The leak is toward 0, as before.
  - A stranger who resembles a relevant person therefore starts with transferred relevance. It is mimicked *only until* the evidence decays it, not permanently. The earlier leak toward Ĉ made that mimicry permanent; it is withdrawn.
  - Δ̂ (K4) and ĉ_p are different objects: one is the effect of the agent's discrete action, the other a gain on a perceived signal.
- **Constraint K5 (cue attention, adopted, not derived).** With a perceptual budget, observe the cues with the largest √(eᵀΣ̂e), the need-projected uncertainty (ES8b).
- **Constraint K7 (no tampering routes, D67).**
  - b changes only through innate event detectors. These read raw input before attention or the cue mask, with the agent's own output removed.
  - No learned parameter enters d.
  - Any slow parameter, such as θ or the ĉ_p leak, is frozen within a selection step.
  - Learning-progress and predictability needs come from an innate predictor that the agent's attention and replay cannot steer. Otherwise those needs are declared open to tampering.
- **Constraint K6 (time, adopted, not derived).** ξ_p tracks each person's effect at two time scales, propagated by elapsed time (ES10b).
- **Claude:** s = Γ(m, {ĉ_p}).

### 2.3 Readouts, never set

- **Valence:** −dV/dt for the ISS-Lyapunov function V of the closed loop. *[verification]* V is not unique, and the agent cannot compute it online. The computable readout adopted is the need part, −Σ ∂d/∂b·ḃ, which also carries the state-function guarantee. *Carried over from the thermodynamic candidate:* the need part, −Σ ∂d/∂b · ḃ, averages to zero over any bounded body trajectory, whoever drives the body, because Σ d(b) is a state function. Need-valence cannot be pumped.
- **Arousal:** the instantaneous loop gain ‖∂u/∂e‖, which rises with deficit because ∇²d grows. *[verification]* This needs a non-quadratic d (the Keramati–Gutkin form with n > m > 1; corrected from m > n > 1, see research/keramati-gutkin-2014-homeostatic-rl.md). For quadratic d the gain is constant, which is what the linear toys use.
- **Emotion types:** recurrent regimes of the closed loop: which entities are in error, which internal models are active, and the sign of valence. Not counted by the core. Named by Claude from replays.

## 3. Derivations of the Principle 10 components

- **Homeostasis.** e → 0 is the problem itself. At e = 0 with no disturbance, u = 0, and overshoot raises d. Satiable per entity.
- **Mood.** Robust regulation against step-like disturbances forces an integrator, m. *[verification]* The *leak* ε_m, which makes it bounded and mood-like, is not forced. It is constraint K3. No toy exercises the leak yet.
- **Reading others.** Robust regulation against structured disturbances forces an internal model, ξ_p.
  - Building it from the agent's own generator makes perception an observer that inverts the agent's own map.
  - CT1 reads the partner's face rhythm (correlation 0.998).
  - **CT5, corrected after verification.** The partner's slow state is read when the observer has **gain on the slow state**:
    - a Kalman filter reads it at R² 0.948, and a fixed-gain observer at the Kalman steady-state gain does equally well;
    - the "deterministic" arm, which never corrected the slow state, reads −0.06 by construction;
    - a mismatched model reads −3.09.
- **Mimicry (K1, with derived properties).** The face shows κ ‖ĉ_p‖ ŷ_p. *Derived:*
  - its amplitude follows the learned relevance (CT1-3, linear in c, by construction of K1);
  - it is pruned for people who do not move the body (CT1-4);
  - its sign is set by reconstruction, so it is mimicry, not anti-mimicry. That is the failure mode of the contingency candidate.
- **Valence and arousal.** §2.3.
- **Temperament (CT3).** For an open-loop-stable plant whose loop has relative degree ≥ 2, the Bode integral ∫ln|S(jω)|dω is zero (Stein 2003; research/stein-2003-respect-the-unstable.md). Temperament is where θ puts the bulge. CT3: two controllers with the same total, peaks 3.1× apart in frequency.
  - *Scope (from the sources).* For a minimum-phase loop, the bulge can be spread thinly over an unbounded band: "the waterbed effect applies to non-minimum-phase plants only" (DFT). The waterbed therefore binds only with an explicit finite bandwidth Ω_a. The engine's fast loop has one, its 30 Hz frame rate and actuator limits. This is a stated constraint, not derived.
- **Curiosity.** The learning-progress body variable (D62), regulated like any other need. Its error enters e, and the action that reduces it is attending where learning progress is expected. With the myopic query this is the shared curiosity toy's selection rule (sims/curiosity/: noisy TV 3.3%, dark room 3.6%). No separate toy in this formalism, because the rule is identical.
- **Regulation by Claude.** Claude is an output-feedback outer loop. Its words enter y as context, which changes the internal models' innovations and so the predicted disturbance: that is reappraisal, changing the estimate of the other rather than the body. Its voluntary face enters a.
- **The Claude interface sector (CT2).**
  - *Safety:* with Claude bounded by gain g_C, the loop m → s → Claude → body → m is stable whenever g_s·g_C·(1/a)(1/ε_m) < 1, against even a worst-case Claude. CT2a: bounded at L = 0.5 and 0.9; runaway at 1.1 and 2.
    - *From the sources (research/sontag-iss-small-gain.md):* the small-gain theorem for ISS interconnections gives practical stability, with residual offsets.
    - **A frozen language model has no certified gain.** The design must therefore **hard-saturate Claude's channel into the body**, |ν| ≤ U. ISS of the regulator then bounds the mood for *any* Claude behavior. That buys boundedness, not convergence.
  - *Influence:* Claude's behavior can carry at most as many independent dimensions of the slow state as there are independently modulated settings (CT2b). The rank of Γ is a design quantity. One setting, such as the thinking budget alone, carries one mixture of the mood.
- **Replay.** The adaptive laws for ĉ_p and θ run offline on stored feature streams. Persistence of excitation selects which segments to replay: the most informative are those where the regressors moved most.
  - **CT8:** excitation-selected replay halves the error in ĉ against uniform replay (ratio 0.517). The pre-registered ≤ 0.5 was missed narrowly.
- **Perception of face and voice.** The observer is perception:
  - the coarse route is a high-gain, low-dimensional observer channel (fast, amplifying noise);
  - the dynamic route is the observer's temporal model F_θ;
  - the body route is G, the agent's own AU coordinates.
  
  CONSPEC is the innate initial observer for faces.

## 4. Expressive structure (brief.md)

- **Structure over people.** One internal model ξ_p and one relevance vector ĉ_p per person, initialized from a shared prior Ĉ(x_p) over appearance and leaking toward 0 (§2.2). There is also an action-effect map Δ̂ shared across options (K4), and a body field over entities (not yet instantiated in a toy).
- **What the low-dimensional version cannot do (CT4).**
  - One shared internal model for three people with different relevance regulates the body **5.0× worse** (RMS 0.100 against 0.020). That is a functional consequence, not one that holds by construction.
  - Per-person models mimic the person who matters 8.2× more than the one who does not. The shared model's ratio is 1.53.
- **Content-dependent attention.**
  - The observer gain L_p and the cue mask passed to Claude are allocated where the regulation error is most sensitive: to the internal model whose prediction error most affects e.
  - **CT7:** with a fixed observer budget, allocating it ∝ ĉ_p·(prediction-error variance) puts 77% on the partner who matters and cuts the body error to 0.66× an equal split.
- **Effective dimensionality.** Σ_p dim ξ_p, plus the body field, plus m. It grows with the number of people who matter, and is pruned for those who do not.
- **Richness from structure.** The same F_θ and G serve every person. Only ξ_p and ĉ_p are added per person.

## 5. Propositions

- **P1 (mimicry amplitude follows relevance; after the sketch).**
  - *Setup:* the linearized loop ḃ = −λb + u + c·y_u, with y_u generated by a neutrally stable finite-dimensional exosystem.
  - *Claim:* every robust regulator contains a generator whose output converges to −c·y_u. If the generator is realized on the agent's motor substrate (K1), the expressed reconstruction has amplitude ∝ c.
  - *Proof idea:* the regulator (Sylvester) equations have a unique solution under non-resonance, u_ss = λb* − c·y_u. The internal model principle requires that this signal be generated internally.
  - *Sources (research/francis-wonham-1976-internal-model-principle.md; the 1976 primary was inaccessible, and Wonham 2018, Bin et al. 2022 and DFT §3.3 were read instead).* "Structurally stable (or 'robust') perfect regulation ⇒ Error feedback + Internal Model".
  - **The scope is narrower than the sketch said:**
    - robustness is over the plant, "most definitely not the controller subsystem";
    - the exosystem must be persistent, with "no stable modes", or Poisson-stable in the nonlinear case;
    - "no finite-dimensional robust regulator exists if unstructured perturbations are considered".
  - **What it forces is the cancelling input u(w), not a copy of the other's behavior.** Outward mimicry is therefore *not* forced by the principle. It stays the explicit constraint K1, as stated.
  - **A responsive human is not an autonomous exosystem**, and the theorems read do not cover that case.
- **P2 (interface safety).** Small gain for ISS interconnections. CT2a is the scalar case.
- **P3 (influence rank).** The dimension of the slow state recoverable from Claude's behavior is ≤ rank(HΓ). CT2b.
- **P4 (temperament conservation).** The Bode integral. CT3. *[verification]* At mood time scales the constraint barely binds: it raises mean sensitivity only to 1.00024. Temperament-as-placement is therefore re-grounded only at the fast loop's bandwidth, and it is a weak claim at mood scales.

## 6. Predictions for the stage claims

- **S1-a (E3).** The face's mimicry term couples to the partner beyond surrogates whenever ĉ_p > 0 (CT1-3: correlation 0.998).
- **S1-c (E1).** Lesioning K1 (κ = 0) removes the coupling. Lesioning the internal model (ĉ = 0) removes both the coupling and the cancellation: the body error rises from 10% to 100% of PI-only (CT1).
- **S1-b (E2).** Steering ĉ_p, the relevance, scales the partner-driven share of the face.
  - **CT6:** with the agent's own expressive variance included, the dose-response is strictly monotone (0.171 to 0.219, ρ 0.76), and a random direction is flat (p = 0.056).
- **Distinctive prediction for S5 and S6.** Mimicry of a specific person tracks how much that person moves the agent's body, and is pruned for people who do not. **The agent mimics the people who matter to it, and that ordering is learned.** This is testable, at S6, against the operator's relationship-specificity claim.

## 7. Failure modes and critiques

- **The internal model principle is exact only for neutrally stable, finite-dimensional disturbance classes.** People are neither, so outside that class "forced" weakens to "favored".
- **A perfect regulator would be affectless.** Affect lives in transients and the waterbed. Gains that are too high make a flat agent.
- **Mimicry is a constraint (K1), as in every candidate so far.** What is derived is its relevance scaling and pruning, not its existence.
- **Strongest critique: set-point homeostasis against allostasis.**
  - Sterling 2012 (research/sterling-2012-allostasis.md; abstract only, the body unverified): "homeostasis (error-correction by feedback) is inherently inefficient … could not possibly serve as the primary regulatory mechanism".
  - Ramsay & Woods 2014 (research/ramsay-woods-2014-homeostasis-allostasis.md) push back. Neither Bernard nor Cannon "considered … an invariant level or set point", and "anticipatory responses do not distinguish allostasis".
  - **How this candidate answers:**
    - once locked on, its internal models cancel predictable disturbances *before* they produce error. That is feedforward, not pure error correction;
    - its set points are innate but its θ drifts, which allows a slowly adapting operating point.
  - **What it cannot answer:** Sterling's broader claim that regulation should be predictive *by default*, and a costate-style anticipation that acts on forecasts the agent has never yet experienced as errors. Costate does that; this candidate does not.

## 7b. Realization on this Mac, and data (added after verification)

- **Per-person internal models.** A shared state-space model F_θ and G, the agent's own generator learned by self-babbling against the placeholder renderer, needing no user data. One observer state ξ_p per known person, run as a fixed-gain observer at 30 Hz. CPU cost is linear in the number of present people.
- **Relevance ĉ_p.** One adaptive vector per person (one entry per non-contact need), initialized from the shared prior Ĉ(x_p), leaking toward 0, and consolidated in replay (CT8: excitation-selected).
- **Action-effect map Δ̂ (K4).** A ridge regression over option features, with contact excluded (D66).
- **Regulator.** Fixed innate gains K, K_I and the leak ε_m. Learned θ (temperament) with a leak toward θ₀.
- **The Claude interface.** Γ is a fixed map from (m, {‖ĉ_p‖}) to the settings. A hard saturation bounds how strongly Claude's words enter as context, which is the ISS requirement, not yet simulated.
- **Data.** From the operator: the ĉ_p vectors, the shared maps Ĉ and Δ̂ (tens of parameters), and the slow θ. That is the candidate's main strength under data scarcity.

## Expressive structure: evidence from the shared test bed (sims/structure/; consolidated 2026-11-25 after VERIFICATION-3)

This section replaces the earlier appended notes. It states only what survived three independent reviews (sims/structure/VERIFICATION.md, -2, -3). Numbers are paired geometric-mean cost ratios with 95% CIs unless stated.

**What the toys show, and their limits.**
- **Content-dependent selection by the need vector.** Selection by the need vector beats the fair low-dimensional ablation, winner-take-all on the most-depleted need:
  - people in a learned person space: ES1, 0.37 (CI 0.17–0.78);
  - a two-sided drive: ES9, 0.12 (CI 0.09–0.18).
  - Further: person × topic composition (ES4, 0.39 against additive) and attention over perceived cues (ES8b, with learned statistics).
  - *Limits:* the worlds match the model class (by construction). The selection rule is myopic in all of these.
- **Items in a learned space.** People, topics and a relation map are learned from appearance and generalize to strangers (ES1, ES2-5, ES4).
- **Needs as a field over a learned space.** Instantiated in ES11, a world certified feasible:
  - the field beats winner-take-all (0.59) and the global gauge (0.02, which ran away in 38 of 40 seeds);
  - **but the learned space added no benefit:** 1.10× under the myopic rule (ES11-2) and 0.998× under look-ahead (ES12-3).
  - **The field over a learned space is instantiated, without demonstrated benefit.**
- **Decision rule against representation.** In ES11/ES12 the policy mattered far more than the representation:
  - myopic 0.206, model-based look-ahead 0.148, and a no-learning threshold rule 0.125 (that rule's figure from ES12's test seeds; ES11 compared it on calibration seeds only);
  - **a threshold rule neither candidate derives beats both** (ES12-2: 1.19).
- **Time.** Per-person two-time-scale tracking, propagated by elapsed time:
  - 0.52 against a one-scale tracker with matched variance (ES10b);
  - 0.68 (CI 0.56–0.82) against a one-scale tracker tuned on held-out seeds (VERIFICATION-3's probe);
  - the earlier ES10 figures (0.45 and others) are superseded.
- **Dimensionality (ES13).** The participation ratios are dominated by the world's 4-cluster kernel, not by the candidates:
  - the body field scores 5.0 even under the no-learning rule, and the kernel alone 4.1;
  - **ES13 does not separate a candidate from its own ablation** and is not evidence for item 3. The behavioral ablations above are.
- **Principle 6 contact (ES7b).** With contact as an innate per-turn constant outside the learned maps, topic choice shows no engagement gradient (gain 0.92). That holds **by construction of the exclusion.**
  - Under the reply-weighted rules VERIFICATION-3 probed, the gradient returns through any other need whose fill needs the partner's reply: learning progress, gain 1.44.
  - D66 is therefore generalized to every need (D66, second amendment).
  - **ES7c/ES19 after the tie-breaking fix (VERIFICATION-4):**
    - reply-conditional valuation shows no engagement-seeking gradient over topics (gain 0.82);
    - but it does **not** stop the agent learning to raise its own expression (0.73–0.78);
    - only D66's exclusion of the agent's expression from the learned maps does.

## 8. Relation to the other candidates

- **Costate.** Both regulate a satiable body field. Costate optimizes a discounted cost-to-go and prices actions by the costate. This candidate guarantees regulation with a structured controller, adding the forced internal models, the integral mood, and the interface sector.
- **Thermodynamic (stood down).** Carried over:
  - filtering as reading;
  - the need-valence state-function guarantee;
  - metastable sets, as a possible definition of the regimes.
- **Contingency (broken).** Its failure, mimicry's sign ambiguity, is avoided here because the face expresses the reconstruction, not a supply optimum.

## 9. Independent verification

Pending.
