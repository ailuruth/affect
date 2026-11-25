# Design: reverse appraisal through the agent's own body (RAB)

Written 2026-11-25 for questions.md Q16 and Q17, by an isolated design author. It starts from research/social-appraisal-synthesis.md and research/contingency-causal-synthesis.md and is written to avoid the failures recorded in the three critiques (critique-design-dyadic-sheaf.md, critique-design-relative-frame.md, critique-design-partner-regulator.md). Nothing was downloaded except paper text. No data, no weights. Simulated worlds are not evidence here. The numeric checks cited as C1–C12 check this document's own equations on random instances (script: `research/foundations/sims/design-reverse-appraisal/check.py`, run with `uv run python design-reverse-appraisal/check.py` from sims/). They are algebra checks, not results.

**Primary sources I read myself for this design** (beyond the project notes):

| Source | What I read | Used for |
|---|---|---|
| Houlihan et al. 2023, Phil Trans R Soc A (PMC10239682) | main text to the methods, via a fetch tool, two passes; equations 3.1–3.4; model comparison numbers | the utility structure; ccc .854 / .762 / .663 and personalisation .439 / .089 / .116; the fact that the model predicts the target's emotion and never the observer's own response |
| Wu, Baker, Tenenbaum & Schulz 2018, Cogn Sci (PMC6033160) | first 100k characters via a fetch tool (introduction, model, Experiments 1–4, model comparison) | Eq. 1; belief recovered only from pre/post reactions; model-free regression .583 vs .957 |
| Carr, Winkielman & Oveis 2014, JEP:G | full author manuscript (PDF text extracted locally) | corrugator before 1,000 ms, zygomaticus 2,000–4,000 ms; no zero-lag co-activation; low-power smile to anger d = 0.69; high-power smile to high-power anger d = 0.78; target power known in advance by subtitle |
| Parkinson & Simons 2009, PSPB | Oxford accepted manuscript (PDF text extracted locally), results and the whole discussion | residual transfer after appraisals; the "emotion elicitor" alternative and its test; joint decisions; the authors' suspicion of "unmeasured appraisals concerning positive expectations"; "anger ... may induce fear if it is directed at us" |
| Yoshida & Man 2025, arXiv 2506.12894 (HTML) | method and limitations sections via a fetch tool | D = D_possessor + w·D_partner, w = 0.5, r = β(D_t − D_{t+1}); identical fixed encoders; untrained decoder still helps |
| Hofman et al. 2012, Proc R Soc B (PMC3396901) | results and discussion via a fetch tool (summary-level) | smile return absent after unfair offers (t15 = 9.62); later anger return up for unfair, down for fair partners |

Everything else is cited through its project note, whose header says how much of the source its author read. I mark those citations "(note)". I did not read Friston & Frith 2015 ("duet for one"), Kilner, Friston & Frith 2007, Fehr & Schmidt 1999 or de Melo 2014; nothing below rests on them.

---

## 1. Plain-language intuition

When your friend's face falls, two things happen in you. Within half a second your own brow twitches the same way. That is the old reflex: seeing a face move nudges the same muscles in your own face. A second or two later something more interesting happens. You work out what her face *means*. She looks hurt, and she is looking at you, so she thinks you did something. Or she looks hurt and is looking at her phone, so something happened to her. Or she is laughing at the same joke you just heard. What you feel next is not her feeling copied. It is your own reaction to the situation you have just inferred, judged by what you care about: how it affects you, how it affects her, how much you care about her outcome, and who caused it.

This design builds exactly those two routes, and nothing else, between the partner's face and the agent's face.

- **The fast route** is a fixed, small reflex on two muscle groups (the smile synergy and the brow-lowering synergy). It responds to the *onset* of a partner's expression, not to its level, so it fades by itself after about a second. It also feeds the agent's own affect a little, through the feeling of its own face. It is not learned and has no setting that grows.
- **The slow route** treats the partner's face as *evidence*. The agent asks: "what situation, and what state of hers, would make *my* body make that face?" It answers with its own model of how its own face expresses its own appraisals, learned from its own life (this is Principle 3's "inverting its own generative mapping", taken literally). The agent then appraises the inferred situation with its own concerns. The partner's face never becomes the agent's face. It only changes what the agent believes happened.

Four consequences follow from the mathematics, and they are the reasons for the design.

1. **Believing her more is not the same as copying her.** If the agent trusts the partner's face more, its *belief* about her appraisal approaches what her face says, never more (Theorem 1b). But its *response* is its own appraisal of that belief. So the precision on the face, the knob every earlier attempt hid, moves belief, not response.
2. **Whether the agent ends up matching her depends on whether the two of them really share the situation.** If the same event is good for both (the same joke), the agent matches, because it would have reacted the same way itself. That is co-appraisal, and the agent's matching even falls as it gets its own independent evidence about the event (Theorem 1f). If the event concerns only her (she lost her job), the agent's reaction is scaled and signed by how much it cares about her outcome on that concern, and that care is capped below its care for itself (Theorem 1g). If she blames the agent, the agent's reading of "you caused this" is, in its own frame, "I caused this", which has the opposite agency sign from her face (Theorem 1e). That is why her anger can produce appeasement rather than anger, unless the agent's own causal record says it did not do it and her past says she retaliates.
3. **Copying is not a setting.** It happens only where several learned objects agree at once: the outcome is shared on every concern, the agent has no independent evidence, the attribution beliefs coincide, and so on. No single number moves the agent from flat affect to copying for an open set of the other values (Theorem 1h).
4. **The agent does not mistake its own following for her responding.** It knows its own random variations because it generated them. What the partner does in response to those variations is the only thing it counts as "she responds to me" (Theorem 5). This matters, because "she blames me" and "I caused it" are computed from this record.

The relationship is not one number either. It is a field of signed weights: how much the agent cares about the partner's outcome on each of its eight concerns, per topic; how shared their outcomes are, per topic; how reliable her attributions are; what she tends to do next. Each expression is evidence about different parts of that field, so each expression is gated differently, and some flip sign.

What the design does not do: there is no classifier, no emotion label and no named emotion variable. The appraisal coordinates are computed quantities over the agent's own body variables and its own causal record (change in predicted drive per concern, expectation violation, who caused it, controllability), not emotions. Emotion is the structure that the agent's appraisal trajectory and affect latent come to have.

---

## 2. The precise mathematical object

### 2.1 Body and drives (innate)

- **Body variables.** b ∈ ℝⁿ, n = 8, with set points b* ∈ ℝⁿ and dead-zone half-widths ε ∈ ℝⁿ₊. The eight are innate regulated quantities of the engine's body (for example energy budget, arousal, social contact, predictability, vocal effort, comfort); their names are engineering names, not emotions.
- **Drive.** d_j(x) = ½·(|x| − ε_j)₊², D(b) = Σ_j d_j(b_j − b*_j). Each d_j is convex, C¹, and zero exactly on [−ε_j, ε_j].
- **Body physics.** ḃ = −A_b(b − b̄) + E_self·m + E_soc(x_P) + e(t). A_b = diag(a_j) ⪰ 0 are innate drift rates toward drift targets b̄ (for example the contact variable drifts toward deficit); E_self m is the known effect of the agent's own acts m (efference); e(t) are event inputs, whose per-event integral is o_A below. **E_soc** is the only direct route from the partner's sensed features x_P into the body, and it has two innate, valence-blind components: co-presence (a face is detected and voice is present) feeds the contact variable; loudness and looming above the partner's baseline feed the arousal variable (the "elicitor" route, Parkinson & Simons 2009, discussion).
- **Allostatic drive and concern weights.** D_H(t) = E_q[∫₀^∞ e^{−τ/H} D(b(t+τ)) dτ], with expectation under the agent's belief q and the body forward model. The concern weights are λ(t) = ∂D_H/∂b(t) ∈ ℝⁿ, and Λ = diag(λ). λ_j is the marginal change in predicted discounted drive from a unit change of b_j now. λ_j = 0 exactly when the predicted trajectory of b_j stays inside its dead zone under small perturbations over the horizon ("allostatic satiety" on concern j).

### 2.2 Situations

An **event** is a segmented window: an utterance, an expression episode, or a pause, with boundaries from the turn and onset detectors (§5.1). Each event carries a latent situation

  s = (o_A, o_P, g, h, g̃, h̃) ∈ 𝒮 = ℝⁿ × ℝⁿ × ℝ⁴, dim 𝒮 = 2n + 4 = 20.

- o_A, o_P ∈ ℝⁿ: the event-induced change in each person's regulated variables, **both in the agent's own body coordinates**. The partner is modelled as a body like the agent's (Principle 3).
- g ∈ ℝ: attribution difference, self minus partner, in the agent's frame (g > 0: the agent caused it). h ∈ ℝ: share attributed to the world or a third party.
- g̃, h̃: the partner's *belief* about the same two quantities, written in the agent's frame. A partner can blame the agent when the agent did not cause it.

The partner's body state is a second latent, b̂_P ∈ ℝⁿ, with the agent's own body physics as its prior dynamics, and λ̂_P = ∂D_H/∂b evaluated at b̂_P.

### 2.3 Swap and belief maps

- **Swap** σ: 𝒮 → 𝒮, σ(o_A, o_P, g, h, g̃, h̃) = (o_P, o_A, −g, h, −g̃, h̃). It exchanges the two persons, negates the attribution differences, and fixes the world share. σ² = id.
- **Belief substitution** β: 𝒮 → ℝⁿ × ℝⁿ × ℝ², β(s) = (o_A, o_P, g̃, h̃): the situation as the partner believes it (outcomes are taken as common knowledge; attributions may differ).
- The agent appraises (o_A, o_P, g, h). The partner, as the agent models her, appraises σ∘β(s) = (o_P, o_A, −g̃, h̃).

### 2.4 The appraisal function (innate algebra, shared by self and modelled other)

For an appraiser with own and other concern weights λ_s, λ_o, relation parameters θ = (ρ, ι⁻, ι⁺), and an input (o_self, o_other, g, h):

  w_s = −λ_s ⊙ o_self,  w_o = −λ_o ⊙ o_other  (drive reduction per concern, own and other's)

  u = w_s + ρ ⊙ w_o − ι⁻ ⊙ (w_o − w_s)₊ − ι⁺ ⊙ (w_s − w_o)₊  ∈ ℝⁿ  (conduciveness per concern)

  π = u − E_pre[u]  ∈ ℝⁿ  (expectation violation: the change from the pre-event expectation, Wu et al. 2018's pre/post reactions)

  α = 𝒜(o_self, o_other, g, h; λ_s, λ_o, θ) = (u, π, g, h, κ) ∈ ℝ^{d_α}, d_α = 2n + 3 = 19.

κ ∈ ℝ is controllability, the identified effect of the appraiser's own acts on the concerns at stake (from Q of §2.11 and the body model); it is slow and treated as constant within an event.

This is a per-concern version of Houlihan et al. 2023's Eq. 3.1 (Fehr–Schmidt terms) in drive units, with the money axis replaced by the agent's n body concerns. **Innate constraints**:
- (K1) self-anchor: the own-outcome coefficient is exactly 1 in drive units and is not learnable;
- (K2) regard cap: ρ ∈ [−ρ̄, ρ̄]ⁿ with ρ̄ = 0.6 < 1;
- (K3) inequity weights ι± ∈ [0, ῑ]ⁿ are innate constants, ῑ = 0.3.

The **agent's appraisal** of event s, with relation θ_{A→p,k} toward partner p in topic k:

  α_A = 𝒜(o_A, o_P, g, h; λ_A, λ̂_P, θ_{A→p,k}) + α⁺_A,

where α⁺_A is the **consequence term**: the appraisal of the partner's predicted next act. The agent predicts a future own outcome o⁺ = Ψ_p(α_P) (Ψ_p: ℝ^{d_α} → ℝⁿ, learned per partner from what happened to the agent's own body after the partner was in appraisal state α_P), caused by the partner, so α⁺_A = 𝒜(o⁺, 0, −‖λ_A ⊙ o⁺‖₁, 0; λ_A, λ̂_P, θ). In the local model (§3) the Jacobian ∂α⁺_A/∂α_P =: Φ_p, and its entry on (agency of the agent) × (agency expressed by the partner) is written ψ_p.

The **partner's appraisal**, as modelled:

  α_P = 𝒜(o_P, o_A, −g̃, h̃; λ̂_P, λ_A, θ_{p→A,k}),

with the same K1–K3 applied to the partner ("the partner has my body").

### 2.5 The agent's own expression model (learned from its own life)

G: ℝ^{d_α} × ℝⁿ → ℝ^k, k = 32 (24 facial synergy coordinates and 8 vocal source-filter settings), is the agent's model of the steady-state output of its own **affective route** (§2.9) given its appraisal and body state. It is fitted only on the agent's own logged pairs (α_A(t), b(t), y^aff_A(t)), where y^aff is the efference of the affective route alone. Reflex and deliberate components are efference-tagged and excluded. G receives **no gradient from partner data**: this constraint keeps the reading in the agent's own body (§3, T4). G is initialised to G₀, the innate synergy map: conduciveness toward the smile synergy (AU12 recruiting AU6) and toward the cry-face; |u| and |π| toward mouth opening and eye constriction; π toward the brow raise. These are synergies, not emotion templates (face-development-synthesis.md §4, note).

### 2.6 Self–other map

V: x_P ↦ y_P ∈ ℝ^k maps the partner's sensed features (52 blendshapes, 6 head-pose and 4 gaze values at 30 Hz; 18 GeMAPS low-level descriptors relative to the partner's running baseline) into the agent's own output coordinates. At S2 it is a fixed linear map from blendshapes to synergy coordinates. At S4 it is learned from self-observation of the agent's own rendered face at a frozen efferent–afferent delay (Stoytchev 2011, note), and refined by being-imitated episodes with a prediction-error rule (Cook et al. 2014, note). Gaze-on-agent γ_t ∈ [0, 1] is passed separately.

### 2.7 Generative model of the partner's stream

  y_P(t) = G(α_P(t), b̂_P(t)) + β_p + ε(t),  ε AR(1) per channel with coefficient φ_p and variance R_p (diagonal).

β_p (baseline) and R_p, φ_p (residual statistics) are the only partner-specific calibration of the emission. They are fitted from residuals, never from labels.

### 2.8 Evidence other than the partner's face, and inference

- Interoception: z_A = o_A + ν_A, with precision high for realised outcomes and zero for not-yet-realised ones.
- Own causal record: z_g = g + ν_g, from the randomised-response decomposition (§2.11).
- Words and context: the transcript (the partner's words and Claude's replies), the topic responsibilities, gaze-on-agent, and the relation field enter a **prior network** that outputs N(μ⁰, P⁰) over (s, b̂_P). The prior network never receives x_P or y_P.
- **Face update (analysis by synthesis with an image constraint).** Each 30 Hz frame applies two Gauss–Newton (iterated extended Kalman) steps:
  - J_P = ∂G/∂α at (α_P(μ), b̂_P);
  - A_P = ∂α_P/∂(s, b̂_P) (analytic);
  - H = J_P A_P;
  - r = y_P − G(α_P(μ)) − β_p;
  - P ← (P⁻¹ + Hᵀ R_p⁻¹ H)⁻¹;
  - μ ← μ + P Hᵀ R_p⁻¹ r.
  
  The face enters only through Hᵀ R_p⁻¹ r = A_Pᵀ J_Pᵀ R_p⁻¹ r. Within an event, s is static and b̂_P drifts under the body physics. At an event boundary, s is re-drawn from the prior network.
- Topics k ∈ {1..K}, K = 16, are a mixture over event types, with responsibilities from the event GRU (§6). All relation objects are indexed by (p, k).

### 2.9 Response: affect latent and the muscle layer

- **Affect latent** z ∈ ℝ⁶⁴: τ_z ⊙ ż = −z + tanh(W_α ᾱ_A + W_b b + W_fb m + U Vᵀ z + c), with ᾱ_A = 𝒜 evaluated at the posterior mean (plus the consequence term), τ_z an innate spread over 0.2–30 s, and rank(UVᵀ) = 8.
- **One muscle layer, three inputs**:

  m = σ(ι_del) ⊙ M(z) + m_ref + m_del.

  - M(z) is the affective route.
  - σ(ι_del) ∈ (0,1)²⁴ is learned inhibition from the deliberate route.
  - m_ref is the reflex.
  - m_del (|m_del| ≤ δ̄ = 0.2 per coordinate) is the deliberate display.
- The output is y_A = first-order activation dynamics of m (τ_m = 50 ms), rendered on the placeholder face and on the source-filter voice (§5.4).
- **Proprioception** (efference plus own rendered face) feeds z through W_fb, which closes the facial-feedback loop.
- **The deliberate route** takes as input only (the relation field at (p,k), the topic, ᾱ_A, z). It never takes x_P, y_P or α̂_P. It acts at turn level (§5.3).

### 2.10 The reflex (Principle 3's mimicry clause, innate and fixed)

For the two declared synergies S₀ = {smile (AU6 + AU12), brow-lowering (AU4)}:

  m_ref,e(t) = λ₀ ∫_{−∞}^{t} e^{−(t−t′)/τ_r} [ d/dt′ (P_{S₀} y_P)_e(t′ − ℓ_r) ]₊ dt′,  e ∈ S₀,

with λ₀ = 0.15, τ_r = 0.5 s and ℓ_r = 0.3 s, all fixed. It is an onset detector: it responds to *increases* of the partner's smile or brow-lowering and to nothing else. Its muscle output reaches the affect latent through proprioception like any other muscle activity, so the perceived feature drives both the motor and the affect pathway.

### 2.11 Own random variation and the randomised partner response

- **Own variation.** The agent's act is x_t = π_t(ℋ_t) + ξ_t. ξ_t is band-limited (0.5–2 Hz) zero-mean variation drawn from a dedicated, logged random generator, per output channel, at a visible amplitude (≈ 10–15 % of each channel's range). π_t(ℋ_t) is the whole policy, including the reflex and the appraisal route.
- **Randomised response.** Q_{p,d} := Cov(y_P(t), ξ_{t−d} | 𝒞_{t−d}) Σ_ξ⁻¹ ∈ ℝ^{k×k}, d ∈ {0.1, 0.3, …, 2.9 s}. Here 𝒞_{t−d} is the partner's history before t − d (pre-treatment controls). It is estimated online by recursive least squares, and an update is accepted only when the first-stage F-statistic per channel exceeds 10.
- **Uses:**
  - (a) the own causal record z_g: the share of a partner outcome change predicted by the agent's own recent acts through Q;
  - (b) controllability κ;
  - (c) the consequence and display models (Ψ_p, display learning);
  - (d) the effect of Claude reply choices, using the randomised draft choice (§2.12) as the instrument.
- **Not a use:** Q is never a reward and never feeds a body variable (Principle 6).

### 2.12 Coupling to Claude (admissible channels only)

For N = 4–8 Claude drafts d_i of the next reply (llm-coupling-synthesis.md, C1, note):
1. The words-to-situation part of the prior network predicts the situation s_{d_i} that the reply would create.
2. The agent appraises it.
3. The score is r(d_i) = −E[ΔD_H | d_i], the predicted change in the agent's own allostatic drive, which includes ρ-weighted partner outcomes and the consequence term.
4. Selection is a softmax with inverse temperature β_sel = β₀‖λ‖₁, so it vanishes at satiety.
5. Sampling keeps every draft's probability above 0 (positivity) and logs the propensities.

Other channels:
- **C4, context.** Verbatim past episodes are retrieved by the query (ᾱ_A, μ, p, k, z).
- **C5, settings.** Effort is set by the posterior entropy of s.
- **C7, reverse channel.** Claude's replies re-enter as words evidence about s.

Claude never sees a number, label or state description (Principle 4).

### 2.13 What is learned (by living), and where

| Object | Learned from | Rule | When |
|---|---|---|---|
| G | own (α_A, b, y^aff) | least squares, weighted by R_self⁻¹ | online small steps; replay |
| V (S4) | own rendered face at frozen delay; being-imitated episodes | regression; prediction-error rule | replay |
| β_p, R_p, φ_p | residuals r | running moments | online |
| prior network, words encoder, event GRU, Ψ_p, reply-effect head | partner stream and own interoception | evidence lower bound through the fixed G; gradients to prior-side nets only | replay |
| relation field θ_{A→p,k}, θ_{p→A,k}, C_{p,k} (cross-covariance of o_A, o_P), w_p (variance of g̃ − g), ψ_p | events with interoceptive o_A (self-generated part removed by efference), posterior o_P, own causal record | conjugate Gaussian updates at two levels (event and partner–topic), §3 T3 | online; re-fit with re-tagged appraisals in replay |
| Q_{p,d} | ξ log and y_P | randomised-response regression with pre-treatment controls | online |
| z, M | own data | self-legibility (α_A recoverable from y_A through G) plus a regulariser to G₀ | replay |
| deliberate route | model rollouts through Ψ_p and Q | minimise predicted D_H over the turn | replay |

### 2.14 Memory (stated with the system in §5.7)

Episodes store feature streams, own efference, b trajectories, the ξ log, verbatim text, and three tags (state σ_k, eligibility e_k, outputs y_k). Three operations, T1 priority, T2 context reinstatement and T3 re-tagging, are separately ablatable.

---

## 3. Theorems with proofs

### The local model (LM)

All statements about transfer are about the **local model at an arbitrary operating point**, not at zero drive. Fix the slow objects at their current values: λ_A, λ̂_P, b, b̂_P, θ, C, w_p, Ψ_p, R_p, β_p, the topic. Linearise 𝒜 and G at the current posterior mean.

Write:
- A_A := ∂α_A/∂s. It includes the consequence path: A_A = A_A^own + Φ_p A_P.
- A_P := ∂α_P/∂s.
- J_A := ∂G/∂α at (α_A, b_A), and J_P := ∂G/∂α at (α_P, b̂_P).
- R := R_p.
- ℰ for all non-face evidence (interoception z_A, own causal record z_g, words, gaze; not to be confused with the affect latent z), with s | ℰ ~ N(μ_ℰ, Σ_ℰ).

The face is y = H s + ε, with H = J_P A_P and ε ~ N(0, R). The agent's steady (DC) output of the affective route is y_A = G(α_A(ŝ)), with ŝ the posterior mean. The **appraisal-route transfer** is

  Γ_app := ∂y_A/∂y_P = J_A A_A L,  L := Σ_post Hᵀ R⁻¹,  Σ_post = (Σ_ℰ⁻¹ + Hᵀ R⁻¹ H)⁻¹.

Define:
- V_α := A_P Σ_ℰ A_Pᵀ: the prior covariance of the partner's appraisal given ℰ; assumed ≻ 0, i.e. A_P has full row rank.
- **B** := A_A Σ_ℰ A_Pᵀ V_α⁻¹ = Cov(α_A, α_P | ℰ) Var(α_P | ℰ)⁻¹, the **appraisal regression**: how the agent's appraisal of the situation co-varies with the partner's, given everything else the agent knows.
- K_α := V_α J_Pᵀ (J_P V_α J_Pᵀ + R)⁻¹, the face gain in appraisal space.
- Π := J_P K_α, the re-render of the believed partner appraisal.
- F := J_Pᵀ R⁻¹ J_P, the face's Fisher information on α_P.
- Π̃ := (V_α⁻¹ + F)⁻¹ F, the posterior shrinkage in appraisal space.
- W := R^{−1/2}.
- E := im J_P ⊂ ℝ^k (dim d_α if J_P has full column rank): the partner expressions that the agent's body can explain as appraisals.

**Copy.** The scaled-copy cone on E is 𝒦_E := {Γ : Γ|_E = c·id_E, c > 0}, in the agent's own coordinates after V. The copy defect is δ(Γ) := min_{c∈ℝ} ‖W(Γ − cI)W⁻¹|_E‖₂. "Copy in a frame" (Γ|_E = cD with a fixed signed permutation D) is treated with the same machinery and is excluded by the same block argument; I state only the cI case.

**Dial.** A scalar p of the design (a parameter or an operating-state scalar) is a *dial* if there is an open set U of values of the remaining parameters on which Γ(p₀) = 0 for some p₀ and Γ(p) enters 𝒦_E for some p. This is the definition the critiques applied: one number takes the agent from flat to copying with everything else at generic learned values.

**Prior structure assumed in T1(e)–(g)** (stated as constraints of the object):
- (P1) a priori the attribution block (g, g̃) and the world block (h, h̃) are independent of the outcomes and of each other, with g̃ = g + η, η ~ N(0, w_p), and h̃ = h + η_h, η_h ~ N(0, w_{h,p});
- (P2) the true attribution g is observed only through the own causal record z_g. Words and the face speak to the partner's belief g̃, not to g.

### T1. The transfer at the operating point: what the agent has instead of a dial

**T1(a) Factorisation.** Γ_app = J_A B K_α.

*Proof.*
1. y depends on s only through α_P: y = G(α_P) + ε, linearised y = J_P α_P + ε. So y ⊥ s | α_P, and in particular y ⊥ α_A | (α_P, z).
2. By the tower rule and Gaussian conditioning, E[α_A | y, z] = E[ E[α_A | α_P, z] | y, z ] = μ_A + B (E[α_P | y, z] − μ_P).
3. E[α_P | y, z] = μ_P + K_α (y − J_P μ_P).
4. Then ∂E[α_A | y, z]/∂y = B K_α, and the chain rule through G gives J_A B K_α. ∎

C2 checks this against the direct formula J_A A_A Σ_post Hᵀ R⁻¹ on 200 random instances: maximum difference 7.5 × 10⁻¹⁴.

**T1(b) Precision moves belief, bounded by 1.**
- WΠW⁻¹ is symmetric with eigenvalues in [0, 1).
- Π̃ is similar to a symmetric matrix with eigenvalues in [0, 1).
- Both decrease in the Loewner order when the non-face evidence becomes more precise.

*Proof.*
1. Let F̂ = W J_P V_α^{1/2}. Then WΠW⁻¹ = F̂ F̂ᵀ (F̂ F̂ᵀ + I)⁻¹. This is symmetric, with eigenvalues σ²/(1 + σ²) ∈ [0, 1).
2. Π̃ = (V_α⁻¹ + F)⁻¹F is similar, via F^{1/2}, to F^{1/2}(V_α⁻¹ + F)⁻¹F^{1/2} = X(I + X)⁻¹ with X = F^{1/2} V_α F^{1/2} ⪰ 0, so its eigenvalues are in [0, 1).
3. More precise non-face evidence decreases V_α in the Loewner order (Σ_ℰ decreases, and A_P(·)A_Pᵀ preserves the order), hence decreases X.
4. t ↦ t/(1 + t) = 1 − (1 + t)⁻¹ is operator monotone, because inversion is operator antitone. So X(I + X)⁻¹ decreases. The same argument applies to F̂F̂ᵀ. ∎

C1 checks this on 200 instances with face precision from 10⁻² to 10³: largest eigenvalue 0.99996, and the Loewner decrease under ten times more precise own evidence held on all 200.

Reading: the precision on the face (Ong, Zaki & Goodman 2015's ζ, and attention-as-precision) scales Π and Π̃, the agent's *belief* about the partner, and saturates at the identity. It reaches the response only through B.

**T1(c) The copy condition.** If J_A = J_P = J with full column rank, then J⁺ Γ_app J = B Π̃, and Γ_app ∈ 𝒦_E ⇔ B Π̃ = c I for some c > 0. In the saturating limit F → ∞ the condition is B = cI.

*Proof.*
1. By Woodbury, (R + J V_α Jᵀ)⁻¹ = R⁻¹ − R⁻¹J(V_α⁻¹ + F)⁻¹JᵀR⁻¹.
2. Hence Jᵀ(R + JV_αJᵀ)⁻¹J = F − F(V_α⁻¹ + F)⁻¹F = F(V_α⁻¹ + F)⁻¹V_α⁻¹, and K_α J = V_α F (V_α⁻¹ + F)⁻¹ V_α⁻¹.
3. This equals (V_α⁻¹ + F)⁻¹F. Multiplying both on the right by V_α and then by (V_α⁻¹ + F) gives F + FV_αF on both sides.
4. So Γ_app J = J B Π̃, and Γ_app acts on E = im J as J (B Π̃) J⁺.
5. Γ_app|_E = c·id_E ⇔ J B Π̃ J⁺ = cJJ⁺ on E ⇔ B Π̃ = cI, because J is injective. ∎

C12 checks J⁺ΓJ = BΠ̃ to 1.1 × 10⁻¹⁴ on 100 instances. If J_A ≠ J_P, the same holds with B replaced by J_P⁺ J_A B, a perturbation of size ‖J_P⁺(J_A − J_P)‖ (the agent's and the partner's operating points on the same body).

**T1(d) Copy margin at the operating point.** δ(Γ_app) ≥ max_{i,j} |μ_i − μ_j| / (2 κ_W(J)), where μ_i are the eigenvalues of BΠ̃ and κ_W(J) is the condition number of WJ.

*Proof.*
1. In whitened coordinates Γ_w|_E = (WJ)(BΠ̃)(WJ)⁺.
2. So ‖BΠ̃ − cI‖ ≤ ‖(WJ)⁺‖ ‖Γ_w − cI‖_E ‖WJ‖.
3. ‖X − cI‖₂ ≥ spectral radius of (X − cI) = max_i |μ_i − c| ≥ ½ max_{i,j} |μ_i − μ_j| for every real c (triangle inequality). ∎

This is a number computable from the learned objects at the current state, as the dyadic-sheaf critique asked ("bound and prove the transfer itself").

**T1(e) Agency block (the swap).** Under P1–P2, B has zero entries between the agency coordinates and the world coordinates. Its only agency–outcome entries come from the consequence map Φ_p. Its agency entry is

  B_{g_A, a_P} = ψ_p − κ₁,  κ₁ = 1 / (1 + w_p (1/v_g + 1/r_g)) ∈ (0, 1),

where a_P = −g̃ is the agency the partner expresses in her own frame, v_g is the prior variance of g, and r_g is the noise variance of the own causal record. The same-event part −κ₁ is strictly negative for every parameter value.

*Proof.*
1. By P1, (g, g̃) is independent of the other coordinates of s a priori. By P2, z_g is the only evidence that loads g. So given ℰ, (g, g̃) is still independent of everything except through z_g.
2. The partner's agency coordinate is a_P = −g̃ (from σ∘β). The agent's is g_A = g + ψ_p a_P (+ zero).
3. Cov(g_A, a_P | ℰ) = −Cov(g, g̃ | z_g) + ψ_p Var(g̃ | z_g), and Var(a_P | ℰ) = Var(g̃ | z_g).
4. With v′ = (1/v_g + 1/r_g)⁻¹ the posterior variance of g given z_g: Cov(g, g̃ | z_g) = v′ and Var(g̃ | z_g) = v′ + w_p.
5. So B = ψ_p − v′/(v′ + w_p) = ψ_p − κ₁.
6. The cross-covariances of a_P with the other coordinates of α_A vanish except through Φ_p. ∎

C3 checks this on 200 instances to 4.4 × 10⁻¹⁶, including the zero cross-terms.

The world coordinate, by the same computation, has B_{h_A, h_P} = v_h/(v_h + w_{h,p}) ∈ (0, 1). This coordinate is σ-even, so world-attributed events transfer with the same sign, shrunk. That is the "anger at a shared adversary" row of Proposition 6.

Reading: when the partner expresses "you did this" (a_P < 0, other-caused in her frame), the agent's same-event appraisal moves toward "I did this" (self-caused) by κ₁. κ₁ is the agent's credence in her attribution relative to its own randomised causal record. The consequence term adds ψ_p: what she tends to do to the agent when she blames it. The sign of the agent's agency response is sign(ψ_p − κ₁), a per-partner quantity on one expression dimension only:
- a fair partner (small w_p, so κ₁ is large) whose blame rarely leads to harm (small ψ_p) gives κ₁ > ψ_p: appeasement-side, self-attributing responses;
- a partner whose attributions have been unreliable (large w_p, so κ₁ is small) and who retaliates (large ψ_p) gives ψ_p > κ₁: other-blame, anger-side responses.

This is Hofman 2012's reputation pattern (anger return up for unfair, down for fair partners) and Parkinson & Simons 2009's remark that anger "may induce fear if it is directed at us", in one formula.

**T1(f) Shared-outcome block, and social referencing shrinks with own evidence.** On a concern j with ρ_j = ρ_{P,j} = 0, ι = 0, prior variances s_A, s_P, cross-covariance c_j, and interoceptive noise variance r_A:

  B_{u_j, u_j} = (λ_{A,j}/λ̂_{P,j}) · c_j r_A / (s_A s_P + s_P r_A − c_j²).

Its magnitude is strictly increasing in r_A and tends to 0 as r_A → 0 (exact own evidence). As r_A → ∞ it tends to (λ_A/λ̂_P) · c_j/s_P.

*Proof.*
1. u_A = −λ_A o_A and u_P = −λ̂_P o_P.
2. Given z_A = o_A + ν_A: Cov(o_A, o_P | z_A) = c − s_A(s_A + r_A)⁻¹ c = c·r_A/(s_A + r_A), and Var(o_P | z_A) = s_P − c²/(s_A + r_A).
3. Hence B = (λ_A/λ̂_P) · [c r_A/(s_A + r_A)] / [s_P − c²/(s_A + r_A)] = (λ_A/λ̂_P) · c r_A/(s_A s_P + s_P r_A − c²).
4. d/dr_A of c r_A/(s_A s_P + s_P r_A − c²) = c (s_A s_P − c²)/(·)², whose sign is the sign of c, because s_A s_P > c² for a positive-definite prior. So the magnitude increases in r_A. ∎

C5 reproduces the closed form to four digits at r_A ∈ {10, …, 0.001}.

This is the guard the social-appraisal synthesis asked for (§4 item 3): "give the agent independent evidence about s; matching must fall as that evidence rises, per expression". When the agent knows its own outcome, the partner's face has no transfer on that concern. The agent may still *match* her (both appraise the same shared event the same way), but the match no longer depends on her face (Γ = 0 there). That is co-appraisal without contagion.

**T1(g) Private-outcome block, and the regard cap.** On a concern j with c_j = 0:

  B_{u_j, u_j} = (ρ_j λ̂_P² s_P + ρ_{P,j} λ_A² s_{A|ℰ}) / (λ̂_P² s_P + ρ_{P,j}² λ_A² s_{A|ℰ}),

where s_{A|ℰ} = Var(o_{A,j} | ℰ). When the agent knows its own outcome on j (s_{A|ℰ} = 0), B_{u_j,u_j} = ρ_j, and |ρ_j| ≤ ρ̄ < 1 by K2.

*Proof.*
1. Cov(u_A, u_P | ℰ) = Cov(−λ_A o_A − ρ λ̂_P o_P, −λ̂_P o_P − ρ_P λ_A o_A) = ρ λ̂_P² s_P + ρ_P λ_A² s_{A|ℰ}.
2. Var(u_P | ℰ) = λ̂_P² s_P + ρ_P² λ_A² s_{A|ℰ}. ∎

C4 checks B_uu = diag(ρ) = (0.4, −0.3, 0) with own outcome known.

Reading:
- A partner's expression about her private outcome moves the agent's appraisal on that concern by exactly its signed regard ρ_j: sympathy if ρ_j > 0, the rival's-loss-is-my-gain response if ρ_j < 0, and indifference if ρ_j = 0. The magnitude never reaches 1.
- The second term is social referencing about the agent's *own* outcome through her care for it ("she looks worried for me"). It vanishes with own evidence, as in (f).
- So the "single partner-welfare weight" hiding place (synthesis §4 item 2) is replaced by n signed, capped weights per topic. What remains is stated in T1(h): a uniform scaling of ρ is a gain-capped sympathy family on the private subspace, not a copy.

**T1(h) No dial (genericity).** Let n ≥ 2. For each scalar p in the list below, the set of values ϑ of the remaining parameters for which some value of p puts Γ_app in 𝒦_E is contained in a semialgebraic set of positive codimension. In particular it has empty interior, so p is not a dial.

The scalars:
- face precision (a common scale ζ on R_p⁻¹, or any single per-channel precision);
- any non-face evidence precision (r_A, r_g, words);
- a uniform drive scale (λ_A → γλ_A);
- a uniform regard scale (ρ → rρ₀);
- a uniform sharing scale (C → cC₀);
- ψ_p;
- w_p.

*Proof.*
1. By (c), membership is equivalent to BΠ̃ = c′I with c′ > 0 (for J_A ≠ J_P, to J_P⁺J_A BΠ̃ = c′I). B and Π̃ are rational functions of all parameters.
2. Hold every parameter fixed except p, c′ and the cross-covariance block C ∈ ℝ^{n×n}.
3. The condition fixes the n × n block (BΠ̃)_uu = c′I, which is n² polynomial equations in C. They are independent at generic points:
   - The map C ↦ (B − c′Π̃⁻¹)_uu is rational, so its Jacobian has its maximal rank on a Zariski-open dense set. It suffices to exhibit one point of rank n².
   - At C = 0, with ρ = ρ_P = 0 and R_A ≻ 0: B_uu = Λ_A R_A(S_A + R_A)⁻¹ C S_{P|z}⁻¹ Λ̂_P⁻¹ (the matrix form of (f)), which is linear in C with an invertible coefficient.
   - Π̃ depends on C only through Var(o_P | ℰ) = S_P − C(S_A + R_A)⁻¹Cᵀ, which is quadratic in C, so its derivative at C = 0 vanishes.
   - So the Jacobian at C = 0 is the invertible linear map above, of rank n². With ρ ≠ 0 an affine term is added and the argument is unchanged.

   So, for each fixed (p, c′), the solutions in C form a set of codimension n² outside a lower-dimensional rank-drop set.
4. The bad set is the projection, along the two coordinates (p, c′), of a semialgebraic set of codimension ≥ n². By Tarski–Seidenberg it is semialgebraic, of codimension ≥ n² − 2 ≥ 2 for n ≥ 2. A semialgebraic set of positive codimension has empty interior. ∎

The design has n = 8, so the codimension is ≥ 62. C6 illustrates this on 40 random instances per scalar: along every sweep the relative copy defect stayed ≥ 0.52 (worst instance), median 0.70–0.84. C7 constructs the exceptional set: with C = S on every concern, no own evidence on outcomes or attribution, w_p → 0, w_{h,p} → 0 and ψ_p = 1 + κ₁ all at once, a face-precision sweep does reach copy (defect 0.0015 at c = 1.00). Relaxing only the world-belief condition (w_{h,p} = 0.5) gives defect 0.40.

**T1(i) The other three paths, at the operating point.**
1. **Reflex.**
   - DC gain 0. For a constant partner expression the derivative is 0 and m_ref decays as e^{−t/τ_r} (C8: 3.8 × 10⁻⁴⁵ after 50 s).
   - Peak: a step of amplitude a gives a peak of λ₀a with area λ₀aτ_r.
   - Under a stationary onset process with rate ν_e and mean onset amplitude a_e, the mean reflex is λ₀τ_r ν_e a_e (C8: 0.0150 vs 0.0150).
2. **Facial-feedback residue.** That reflex activity reaches z through W_fb. Its mean contribution to the DC face is
   Γ_res ≈ M′(−A_z)⁻¹ W_fb λ₀ τ_r diag(ν_e a_e) on S₀,
   with ‖Γ_res‖ ≤ ‖M′(−A_z)⁻¹W_fb‖ · λ₀ τ_r ν_max a_max (C8: residue 0.0150 vs the formula's 0.0150). Here A_z is the linearised latent dynamics and M′ the Jacobian of M. This is relation-independent, same-sign, and proportional to onset statistics, not levels.
3. **Elicitor.** Γ_el = (∂G/∂b_ar)(κ_el/a_ar) e_loudᵀ is rank 1, has a fixed sign, and is the same for every partner.
4. **Deliberate route.** It has no partner input, so its within-event transfer is (∂π_del/∂ᾱ_A) times the appraisal route. It can only re-express the agent's own appraisal and never adds a partner→self map.

So the total steady (DC) transfer at the operating point is

  Γ_DC = (J_A + D_del) B K_α + Γ_res + Γ_el,  D_del := (∂y_A/∂m_del)(∂π_del/∂ᾱ_A),

and the reflex adds only a transient. T1(c)–(h) apply with J_A replaced by J_A + D_del: the deliberate route shares the factor B K_α and cannot bypass it.

**What remains, stated exactly.**
- **(R1)** On the declared two-dimensional S₀, λ₀ is a fixed one-parameter family from flat to a transient onset copy (peak λ₀a, area λ₀aτ_r). It is not learned and not state-dependent.
- **(R2)** A uniform scale on ρ is a family from 0 to ρ̄Π on the private-outcome subspace, a capped sympathy gain, never a copy.
- **(R3)** On the co-appraisal set of (h), copy happens. That set is where the world really makes both persons' outcomes identical, the agent has no own evidence, and the attributions coincide. On that set matching is the correct appraisal, and by (f) it disappears from Γ as soon as the agent has its own evidence.
- **(R4)** The relation-independent residue Γ_res + Γ_el is bounded as above.
- **(R5)** The deliberate route is a learned policy with the relation field as input. In principle it could learn D_del ≈ J_P B⁻¹ − J_A for a given relation, a display that re-renders the believed partner appraisal: an affiliative "copy" display. It is bounded by |m_del| ≤ δ̄ = 0.2 per coordinate, acts at turn level, and is trained only on predicted own drive. It is a hiding place I can bound but not exclude; F2 in §8 tests it.

### The residual same-sign transfer (Parkinson & Simons 2009)

Parkinson & Simons found that other→own anxiety and excitement transfer survived control of all measured appraisals and of the participant's perception of the other's emotion (reference person's own excitement → participant's, β = .28–.57). RAB predicts three sources of such a residual, each with a distinct signature:

1. **R4, the reflex–feedback residue plus the elicitor.** Same-sign, needs no registration of the partner's emotion, depends on onset rate and loudness, and is the same for every partner. That last property is exactly the discriminating test the authors propose: "Emotion elicitors should bring equivalent effects regardless of the relationship."
2. **Co-appraisal in shared decisions** (B_uu with c_j large). 41 % of their decisions were joint, and excitement transfer was stronger in joint decisions (interaction 9.70, t(38) = 3.06), as (f) predicts when outcomes are shared and own evidence is incomplete.
3. **Appraisal coordinates they did not measure.** Their three appraisals were chosen for anxiety, and the authors suspect "unmeasured appraisals concerning positive expectations". In RAB that is the π coordinate (expectation violation per concern) and the consequence term (anticipated partner response, which they also raise).

Bound: the relation-independent part is ≤ ‖M′(−A_z)⁻¹W_fb‖λ₀τ_rν_max a_max + ‖∂G/∂b_ar‖κ_el/a_ar, with every factor an innate constant or a measured statistic. The rest is relation- and evidence-dependent through B.

### T2. Satiable drives, and no value in the partner's smiles

**(a)** D ≥ 0, with D(b) = 0 iff b lies in the box ∏_j [b*_j − ε_j, b*_j + ε_j]. D_H ≥ 0. *Proof:* each d_j ≥ 0, with equality iff |x| ≤ ε_j. ∎

**(b) Valence-blind body inputs.** The partner's features enter ḃ only through E_soc. Its arguments are co-presence (face detected, voice present) and loudness and looming above baseline. These are invariant to the sign and to the configuration of every expressive channel. Hence ∂ḃ/∂y_P^expr = 0 for each facial expression coordinate. *Proof:* by the definition of E_soc in §2.1. ∎

**(c) No value from the partner's signals as such (martingale).** Let a be any choice the agent makes (a draft, a display, an act), Y any observation revealed after a (including the partner's face), and V(a) := E_q[D_H(t + T) | a, ℱ_t]. Then E_q[ E_q[D_H(t + T) | a, Y, ℱ_t] | a, ℱ_t ] = V(a). So an action's value comes only from its predicted causal effect on the agent's own b. By (b), an action whose only effect is to make the partner smile has value 0.

*Proof:* tower property of conditional expectation under the agent's own model q. ∎

Caveat: this holds for the agent's model. A misspecified model can still assign spurious value to signals, so the test in §8 F10 is needed. Through co-presence, the contact concern does value the partner being present: a satiable need for company, bounded by (d). That is the remaining Principle 6 risk, stated.

**(d) Satiety.**
- If λ = 0 (allostatic satiety over the horizon), then u = 0 and the u-part of π is 0.
- The draft tilt has β_sel = β₀‖λ‖₁ = 0, so the selected distribution equals Claude's own and KL(π_sel ‖ π) = 0.
- The deliberate route's objective gradient is 0.
- The partner's maximal contribution to −dD_H/dt is ≤ Σ_j λ_j sup|E_soc,j|, which is 0 once the contact and arousal variables are in their dead zones over the horizon: a flattery ceiling.

*Proof:* direct substitution. ∎

At satiety the agent still smiles back by reflex (R1). This answers the partner-regulator critique's "no smile at satiety".

**(e) Bounded dependence.** Contact is filled by co-presence of anyone, not by a specific partner. Partner specificity lives only in θ, C, w_p and ψ_p, which are bounded. On partner loss, D_H rises at most at the innate drift rate a_contact. There is no opponent process and no partner-specific deficit variable.

### T3. Time scales from structure, including fast match then later context

**(a) Reflex** latency ℓ_r + O(τ_r) ≈ 0.3–0.8 s: an innate, declared constant (the body).

**(b) Context latency is a ratio of precisions, not a time constant.** Within an event the situation is static. Let a coordinate of α_P have prior precision P₀ given the non-face evidence, and let the face carry Fisher information rate ℐ on it per second. With AR(1) frame noise (coefficient φ) at frame rate f_s, ℐ = f_s · (per-frame information) · (1 − φ)/(1 + φ). The continuous-time Kalman–Bucy posterior precision is P(t) = P₀ + ℐt, and the weight of the face in the posterior mean is ℐt/(P₀ + ℐt). The appraisal-route response on that coordinate therefore reaches half its asymptote at

  t_½ = P₀ / ℐ,

followed by the latent's fast time constant τ_z,fast (≈ 0.2–0.5 s).

*Proof:* for a static Gaussian latent under continuous Gaussian observation, the precision adds linearly in time, and the posterior mean is a precision-weighted average. ∎ (C9: numeric t_½ = 2.50 s against P₀/ℐ = 2.50 s.)

Three predictions follow:
1. When the event is known from non-face evidence (the agent saw or was told what happened), the relevant s-coordinates are already precise, the response no longer waits on the face, and context acts at τ_z. That is Mauersberger 2022's early context effect for laughter at known scenes (note).
2. When the meaning must be read from the face (in Carr 2014 target power was known from the subtitle, but what each angry face was about was not), the context-carrying smile channel waits t_½. For agency and target coordinates, which faces carry weakly, t_½ is seconds. Carr's zygomaticus effects came at 2,000–4,000 ms.
3. The reflex brow response (S₀, onset-driven) comes first. Carr's corrugator responded before 1,000 ms and the two muscles did not co-activate at zero lag.

**(c) Relationship learning: from minutes to stable, by evidence count.** Each relation object is a Gaussian posterior with two levels:
- an event-level deviation θ_{p,k,e} with process noise q_f;
- the partner–topic mean θ_{p,k} with process noise q_s ≪ q_f.

For a scalar entry observed with noise r_θ per event, the Kalman gain after N events is k_N = P_N/(P_N + r_θ) with P_N ≈ (P₀⁻¹ + N/r_θ)⁻¹ + q. That gives k_N ≈ 1/(N + r_θ/P₀) until N ≈ √(r_θ/q), and then the steady value ≈ √(q/r_θ).

So a new partner's relation moves within a handful of events (minutes), as Hofman's within-game change did. An old one is stable, which gives reputation. *Proof:* the standard scalar Riccati recursion. ∎ The levels q_f and q_s are declared constants. The fast and slow behaviour comes from the evidence count, not from a hand-set time constant.

**(d) Mood.** The slow component of D_H and λ is set by the body drift rates a_j (hours) and the horizon H: declared body physics.

**(e) Temperament.** The across-partner, across-topic prior θ₀ is updated only in replay, with effective gain ~1/N_total. It stiffens as evidence accumulates, and the replay distillation term (§5.7) anchors the agent's own response function.

Honest summary:
- (b), (c) and (e) come from the structure of the evidence;
- (a) and (d) are declared constants of the body;
- q_f and q_s are declared volatility levels.

### T4. Reading the other through its own body, as mathematical statements

**(a) Image constraint.** In the face update of §2.8, the face enters every belief and every action only through A_Pᵀ J_Pᵀ R_p⁻¹ r. Hence any partner-feature perturbation δy ∈ ker(J_Pᵀ R_p⁻¹) changes no belief, no appraisal, no expression and no choice, at every iteration of the nonlinear update.

*Proof:*
1. Each Gauss–Newton step changes μ by P Hᵀ R⁻¹ r = P A_Pᵀ (J_Pᵀ R⁻¹ r), and P does not depend on y.
2. The prior network does not see y.
3. Everything downstream (𝒜, z, drafts, retrieval) is a function of (μ, P, non-face inputs). ∎

C11 checks this: on a three-dimensional kernel, |L·ker| = 1.6 × 10⁻¹⁶ and |Γ·ker| = 1.1 × 10⁻¹⁶. An expression the agent's own body cannot produce, as judged by its own model G, is invisible to it. Because G is trained only on the agent's own data (§2.5), this is a statement about the agent's own body.

**(b) Same function, swapped frame.** The partner is modelled with the agent's own 𝒜, its own G and its own body physics, evaluated at another body state b̂_P, on the swapped and belief-substituted situation: α_P = 𝒜(σβs; λ̂_P, λ_A, θ_{p→A}). Like-me identity: if b̂_P = b_A, θ_{p→A} = θ_{A→p}, g̃ = g, h̃ = h and s = σ(s) (a symmetric situation), then α_P = α_A and the believed partner face equals the agent's own face. *Proof:* substitution; σ fixes s by assumption. ∎

**(c) Reciprocity, used for reputation.** The agent's prediction of how the partner reads the agent's face is its own reading map with the roles swapped: the posterior map s ↦ ŝ(y_A) computed with σ applied to the situation and with the partner's parameters in the agent's slots. *Proof:* the generative model in §2.7 is written for an arbitrary appraiser, and swapping roles is the substitution σ. ∎ The deliberate route uses this to evaluate displays (§5.3), as in Houlihan's reputation loop (Eq. 3.2), but without any partner input at run time.

**(d) The swap reverses agency.** By T1(e), reading the partner's "you caused this" through the agent's own appraisal function yields, in the agent's own frame, "I caused this", scaled by κ₁ ∈ (0,1). Reading through one's own body in the swapped frame is what makes blame produce something other than blame.

### T5. Identifiability of the partner map under the agent's own following

**Lemma (randomised response).** Let:
- x_t = π_t(ℋ_t) + ξ_t, where ℋ_t is any history (including the partner's past, hidden common drivers and the agent's own reflex and appraisal following), and ξ_t is drawn from a logged random generator independent of everything not downstream of it;
- (exclusion) ξ reach the partner only through x;
- y_t := y_P(t) the partner's output and ŷ_t = y_t + ν_t its noisy reading, with ν independent of ξ.

Then:
1. Q_d := Cov(ŷ_t, ξ_{t−d}) Σ_ξ⁻¹ = ∂E[y_t]/∂ξ_{t−d}, the causal (closed-loop) response of the partner at lag d to the agent's act.
2. Conditioning on pre-treatment controls 𝒞_{t−d} (anything determined before ξ_{t−d}) leaves the estimand unchanged and reduces its variance.
3. If no causal path leads from the agent's acts to the partner, then Q_d = 0 for every d, every following policy π, every hidden driver, every partner autocorrelation and every reading noise.
4. Because the partner sees only x, Q_d is also the effect of do(x_{t−d}) (with the agent's later behaviour following its policy), whatever part of x the policy produced.

*Proof.*
1. ξ_{t−d} is independent of everything upstream of it. So Cov(y_t, ξ_{t−d}) = Cov(E[y_t | ξ_{t−d}], ξ_{t−d}), and with linearity in the local model this equals (∂E[y_t]/∂ξ_{t−d}) Σ_ξ. Reading noise is independent of ξ, so it adds no covariance.
2. Pre-treatment variables are independent of ξ_{t−d}, so adding them as regressors does not change the ξ coefficient. It removes explained variance from the residual.
3. With no path, y_t is a function of partner-side variables only (hidden drivers, the partner's innovations, the partner's past), all independent of ξ. So the covariance is 0.
4. ξ enters x additively, and the partner's mechanism takes x as its argument, so ∂/∂ξ = ∂/∂x along the same closed loop. ∎

C10 checks this on the scalar loop of contingency-causal-synthesis.md §1, with rectified (reflex-like) following, a hidden AR(0.98) driver and reading noise sd 0.5, over 20 seeds of 18,000 steps:
- non-responsive partner: Q̂₁…₅ means −0.004 to −0.009 (sd 0.02–0.04), while the naive lag-3 regression gives 1.64;
- responsive partner (R = 0.3 at lag 3, persistence 0.6): Q̂₃ = 0.295, Q̂₄ = 0.176 (= 0.3·0.6) and Q̂₁, Q̂₂ ≈ 0, against a naive 1.35.

**Corollaries.**
- **(i)** The agent cannot satisfy any of its concerns, or come to believe "she responds to me", by its own following. Q is built from ξ only, and the contact variable is not fed by Q at all (§2.11).
- **(ii)** The own causal record z_g (the share of the partner's outcome change predicted from the agent's recent acts through Q) is unbiased by following. So the agency coordinate that drives the swap in T1(e) is not contaminated by the agent's mimicry.
- **(iii)** The sharing statistics C are estimated from the agent's own interoceptive o_A after subtracting the self-generated component predicted by efference through the known body physics (E_self m, including reflex activity). Partner-caused body changes come only through the innate, known E_soc. So no estimated quantity regresses the agent's own expression on the partner's.
- **(iv)** Conditions to monitor:
  - **positivity:** σ_ξ > 0 always, and draft selection never deterministic;
  - **relevance:** first-stage F ≥ 10 per channel before updating;
  - **visibility:** update the visual Q only while gaze-on-agent is high; the off-gaze estimate should be ≈ 0, which gives a running self-test;
  - **probes at more than one amplitude**, because the identified effect is local to the amplitude of ξ;
  - **the self channel calibrated first** in a solo period, with its delay frozen (Stoytchev 2011, note).
- **(v)** Draft choice is randomised with logged propensities, so the effect of reply choice on the partner's subsequent appraisal is identified by inverse-propensity weighting (Hernán & Robins ch. 12, note).

### Per-expression gating and sign flips (Proposition 6)

By T1(a), the partner→agent transfer of an expression direction v ∈ E is J_A B K_α v. K_α v says which coordinates of the partner's appraisal that expression is evidence about, through the agent's own G. B then says what each coordinate means for the agent. The table gives the predicted response for each row of the mimicry table (mimicry-context-synthesis.md; primary papers named). "Shared" means c_j large on that concern in that topic.

| Partner expression and context | What the face is evidence about (via G⁻¹) | B block that acts | Predicted agent response | Human data |
|---|---|---|---|---|
| Smile in conversation, any partner | u_P > 0 on conversational concerns (contact, predictability) | shared block, c_j > 0 | match (positive) | smiles returned across groups (Bourgeois & Hess 2008, note) |
| Smile of a rival after the rival won a contested concern | u_P > 0 where o_A = −o_P (c_j < 0), or inequity behind | shared block with c_j < 0; ∂u/∂w_o = ρ − ι⁻ < 0 when behind | no smile, or the opposite sign | zygomaticus return absent under competition (Seibt 2015, note); absent after an unfair offer (Hofman 2012) |
| Sadness of an in-group partner about her loss | u_P < 0 on her private concerns | private block, ρ_j > 0 | sadness-side response, scaled by ρ_j ≤ ρ̄ | sadness mimicked only for in-group (Bourgeois & Hess 2008) |
| Sadness or distress of a rival | same | private block, ρ_j < 0 | positive-side response (brow relaxation) | Likowski 2008 (abstract, note); Seibt 2015 (note) |
| Sadness of a stranger | same | ρ_j ≈ 0 | little or none | sadness mimicry costly; absent for out-group |
| Anger aimed at the agent (gaze on agent), fair partner | a_P < 0: she attributes it to the agent | agency block, ψ_p < κ₁ | self-attributing, appeasement-side response; smile only if the display route learned appeasement | smiling to anger: Carr 2014 low-power perceivers d = 0.69, communal partners (Häfner, via note) |
| Anger aimed at the agent, unfair or retaliating partner | same | ψ_p > κ₁ | other-blame, anger-side return | anger return up for unfair partners (Hofman 2012) |
| Anger aimed at a shared adversary (gaze away, third party) | h̃ > 0, u_P < 0 on a concern the agent shares | world and shared blocks (σ-even) | match | anger mimicked only when aimed at a shared adversary (Bourgeois & Hess 2008 Study 1) |
| Disgust at something she tasted | u_P < 0 on her ingestion concern; c ≈ 0 unless the agent will ingest it too | private block, ρ small | none, unless the outcome is shared | disgust not mimicked live (Fischer et al. 2012, note) |
| Laughter at a joke both heard | π_P > 0 on predictability, shared | shared block | match | laughter mimicry when appropriate to its cause (Mauersberger 2022, note) |
| Laughter after a disgusting scene | u_P misfits the known event: own evidence precise | shared block shrinks by (f) | little | little laughter mimicry after disgust scenes (Mauersberger 2022) |

**Dial rank ≥ 2 from one change of relation** (the Hofman pattern). Learning that a partner is unfair moves three objects:
- the inequity regime (the agent is behind, so the effective regard ∂u/∂w_o = ρ − ι⁻ falls, possibly below 0);
- w_p rises (her attributions are less reliable), so κ₁ falls;
- ψ_p rises (she retaliates).

The first lowers smile return. The second and third raise B_{g,a} toward anger return. The two rows move in different directions, so span{ΔΓ} has dimension ≥ 2. Within the game (event level, q_f), the inequity regime alone acts at once: smile return drops. After the game (the partner–topic level), the w_p and ψ_p changes persist: anger return rises while smile return recovers. Hofman's two time scales come from the two levels in T3(c).

---

## 4. Why existing mechanisms cannot do it: the mathematical reasons

The test throughout: what is Γ, the partner→agent transfer at the operating point, under the mechanism?

**4.1 Perception–action model (Preston & de Waal 2002, note).** Read literally, the response is (1 − inhibition) · attention · overlap · [the subject's representation of the object's state]. With P_match the matched representation (copy on E), Γ_PAM = g · P_match with g = (1 − i)·a·o ∈ [0, ∞). That is dial rank 1, with g as the dial by construction. Inhibition i ∈ [0,1] cannot invert a sign. In RAB, Γ = J_A B K_α with B a posterior covariance ratio whose entries change sign with C, ρ, ι and ψ − κ₁ (T1e–g), and whose shared block shrinks with own evidence (T1f). The PAM has no object that would produce either.

**4.2 Any learned partner→self map** (the REACT listener models; the sheaf, frame and regulator designs; Yoshida & Man's decoder used as a drive). Fitted by least squares on dyadic data, a map W from partner features to own output converges to Cov(y_A, y_P)Var(y_P)⁻¹. In closed loop with the agent's own following f, that covariance contains f, and by the contingency synthesis's §1 formula it is nonzero for a partner who never responds. On human data it is dominated by human mimicry, which is why "mime" baselines are near the ceiling (known-failures row 1). Any scalar on W then runs from flat to that learned copy (the critiques' Lemma A). RAB never fits a partner→self map. B is a ratio of appraisal second moments whose cross-moments are estimated from world-attributed own interoception with efference-predicted self-components removed (T5 iii).

**4.3 Attention.** For a single head, the partner token contributes a_P·W_V y_P with a_P ∈ [0, 1] from a softmax, so Γ = a_P W_V + (terms from ∂a/∂y_P). The sign pattern of W_V is a fixed learned constant per head. A relation-dependent sign flip needs gating between heads with opposite-signed W_V, which makes the mixing weight a dial (math-objects-synthesis.md §1, note). The deeper difference: attention moves partner *content* as values. RAB moves no partner content into the response. The partner's features enter only as a likelihood residual through Jᵀ R⁻¹ (T4a), and the response values are the agent's own appraisals. Attention could be used to *implement* parts of RAB (for example as an amortised posterior), but then the computation is RAB's, not attention's.

**4.4 State-space models, including selective ones.** ẋ = Ax + B_in u, y = Cx gives Γ = C(−A)⁻¹B_in, a fixed matrix. A selective SSM scales the input map by a step Δ(u). That is a gain on a fixed profile and dial rank 1 per profile, with signs fixed by C(−A)⁻¹B_in.

**4.5 Bayesian theory of mind and inverse planning** (Houlihan 2023; Wu 2018; Ong 2015 and 2019, read or noted). These compute the posterior over the target's mental state: K_α in RAB's notation, plus a label map. In my reading of Houlihan and Wu, neither models the observer's own response: Houlihan's task is "predicting how a person will emotionally react to an event", and Wu's is how observers "use someone's emotional reaction to infer her beliefs and desires". Two extensions are possible:
- "Respond with what I infer she feels" (render α̂_P through one's own body) gives B = I and Γ = Π. By T1(b) the face precision then runs Γ from 0 (precision 0) to the projection onto E (precision ∞). That is exactly the ζ risk the social-appraisal synthesis names, so the observer-side models become the dial once a response is attached.
- The missing operator is B: the observer's *own* appraisal of the same latent situation, with its own concerns, the swap σ, and its own causal record. Houlihan's ω weights are the target's, and the observer has none.

RAB is inverse planning plus the observer's appraisal regression plus a response through the observer's own body. The parts are known (§7). The response operator and its theorems are what is added.

**4.6 Active inference** (Smith, Parr & Friston 2019 and Hesp et al. 2021, notes; the dyadic papers not read). The models read are single-agent: hidden emotion-concept states and precision dynamics. If a social active-inference agent produced its expression as the action that fulfils a predicted own state taken from the inferred partner state (the "mirror" reading, which I have not read in its source and so do not attribute), then in the linear-Gaussian case Γ = Π scaled by a precision ratio: a precision dial. If its generative model contained 𝒜, σ, the observer's concerns and the own causal record, its posterior would contain B and it would compute RAB. The formalism neither supplies nor forbids B. The claim here is therefore limited: active inference does not by itself produce T1(e)–(g), and the precision parameter it relies on is exactly the scalar T1(b) shows to move belief only.

**4.7 Yoshida & Man 2025 (read).** D = D_possessor + w·D̃_partner with w = 0.5 and reward r = β(D_t − D_{t+1}). On partner-private events this gives B = w·I on the drive coordinates: one uniform weight across all concerns, uncapped by structure (w is set by hand), with no sharing, attribution or consequence structure. So w is the welfare dial (T1g's R2 without the cap and without per-concern signs). RAB replaces w with ρ ∈ [−ρ̄, ρ̄]ⁿ per topic plus C, κ₁ and ψ. It keeps their best idea, reading the partner with one's own generator, made exact in T4. Their surprising result that an untrained decoder still helped is a warning RAB inherits: the decoder ablation (F6) must be scored on state, not survival.

**4.8 The earlier designs here.** In the sheaf, the relative frame and the regulator, the partner entered the agent's *dynamics*, as an edge target, a frame transport or a scheduling signal. Linearised at any operating point, that is an additive input with a learned map (the regulator critique's B_eff = π𝒯(c)[h₀]). In RAB the partner's features never enter the agent's dynamics. They enter a posterior. The dynamics see only the agent's appraisal of its posterior situation (z's input is ᾱ_A), the innate valence-blind E_soc, and the fixed onset reflex.

---

## 5. The whole system, derived from the object

Every component below is one of the objects of §2, a consequence of the theorems in §3, or an explicitly declared constraint.

### 5.1 Perception of face and voice through the agent's own body

- **Features (Principle 1).** Partner face: 52 blendshapes, 6 head-pose and 4 gaze values at 30 Hz from MediaPipe Face Landmarker. Pin tasks-vision 0.10.35, because builds from 1.0.0 on send usage telemetry off the Mac (mediapipe-face-landmarker.md, note). Partner voice: the 18 GeMAPS low-level descriptors at 100 Hz, each relative to the partner's running baseline (voice-synthesis.md §2), pooled to 30 Hz as mean and delta. No classifier anywhere.
- **Into the agent's coordinates.** V (§2.6) maps both streams into the agent's own 32 output coordinates: 24 facial synergies and 8 vocal source-filter settings.
- **Reading (T4).** The posterior over (s, b̂_P) is updated only through the agent's own G with the swap σ. The partner's voice is read through the vocal rows of G, which is the Brunswikian lens of Scherer 2003 with the agent's own encoding weights as its cue weights (voice-synthesis.md §5.4, note).
- **Change, not only level.** Because α includes π (expectation violation) and s is re-drawn at event boundaries, a *change* of the partner's expression locked to an event updates the partner's expectation coordinates. This is Wu 2018's finding that beliefs are recovered only from reactions before and after the outcome.
- **Direction of the expression.** Gaze-on-agent and head direction enter the prior network as evidence about (g̃, h̃). "Anger at me" and "anger at someone else" update different coordinates (Bourgeois & Hess 2008, Hess & Fischer 2013, notes).
- **Event segmentation.** An onset detector on V(x_P) (the same derivative the reflex uses), utterance boundaries from the transcript, and prosodic turn-end prediction (§5.4).

### 5.2 The latent state where emotion emerges

Nothing in the state is a named emotion. The state at time t is:
- the posterior N(μ, P) over (s, b̂_P);
- the agent's appraisal trajectory ᾱ_A(t) ∈ ℝ¹⁹;
- the body b ∈ ℝ⁸ and its allostatic gradient λ;
- the affect latent z ∈ ℝ⁶⁴;
- the relation field {θ_{A→p,k}, θ_{p→A,k}, C_{p,k}, w_p, ψ_p, Ψ_p, Q_p} over partners p and topics k.

What emerges:
- **Emotion** is recurring structure in the joint trajectory (ᾱ_A, z). An example is the region with negative conduciveness, other-attribution and high controllability, which an observer might call anger. The engine never names it. Claude may, from verbatim episodes retrieved by that state (§5.5).
- **Readouts, not variables.** Valence is −dD_H/dt, predicted. Arousal is ‖λ‖₁ plus the precision-weighted ‖π‖.
- **Effective dimensionality.** 19 appraisal coordinates per event, 64 in z, plus a relation field of ≈ 155 means per (partner, topic). The low-dimensional ablation the brief asks for is to collapse B to a scalar (ρ → w·1, C → c·I, drop σ). T1(h) then fails: the welfare-weight dial returns (§4.7), and the sign flips of Proposition 6 disappear.
- **Content-dependent selection** (the brief's need-conditioned attention) happens in three places, each a consequence of λ:
  - appraisal weights outcomes by λ (u = −λ ⊙ o);
  - retrieval queries by (ᾱ_A, μ, p, k);
  - draft scoring weights predicted outcomes by λ.

  Perception precision is deliberately *not* need-conditioned, because a need-set precision on the face would be the scalar hiding place of T1(b).

### 5.3 Face output: two routes into one muscle layer, plus the reflex

m = σ(ι_del) ⊙ M(z) + m_ref + m_del (§2.9–2.10).
- **Emotional route M(z):** bilateral, recruits synergies, reaches the upper face, and is driven by the appraisal trajectory through z.
- **Deliberate route:** inhibition gates σ(ι_del) (display rules, masking) and a bounded display m_del, which is stronger on the lower face. Its inputs are the relation field, the topic, ᾱ_A and z, never the partner's features. It is trained in replay to minimise predicted D_H over the turn through the partner model: Ψ_p, Q_p, and T4(c) reciprocity for "how she will read my face". This is Houlihan's reputation term as a policy, and it is how learned appeasement displays (smiling to a powerful partner's anger, Carr 2014) arise.
- **Reflex m_ref:** fixed onset matching on S₀.
- **Clinical double dissociation.** Lesion M and posed displays survive while spontaneous expression goes flat. Lesion the deliberate route and display rules and masking vanish while spontaneous expression survives, possibly exaggerated without inhibition (face-development-synthesis.md §1 and §4.1, note).
- **Facial feedback** closes the loop through W_fb. The magnitude of its residue is bounded in T1(i).
- **Masked smile signature.** A deliberate smile drives AU12 through m_del without the AU6 that M recruits.

### 5.4 Voice: a source-filter body

- **Output.** The 8 vocal coordinates of y_A (F0 level and range in semitones, loudness, tempo, spectral tilt, aperiodicity, formant shift, breath events) modulate macOS TTS output through WORLD resynthesis (voice-synthesis.md §5, note).
- **Appraisal through G.** The vocal rows of G give the same appraisal-to-voice relation as the face, so face and voice come from one state and cannot disagree (known-failures row 11).
- **Innate vocal reflexes:**
  - cry-like and laugh-like vocalisations on the cry-face and laugh synergies;
  - the novelty catch (an inhalation on large |π|);
  - the low-pitch back-channel opportunity detector (Ward & Tsukahara 2000, note), whose uptake probability is λ_contact-weighted.
- **Elicitor.** The partner's loudness and looming feed the arousal variable (E_soc).
- **Turn-taking.** A learned prosodic turn-end predictor holds a prepared opening (breath, particle, nod, facial onset) and releases it 100–300 ms after the predicted end. Claude's words continue a turn the body has already opened.
- **What is derived and what is not.**
  - Derived: loudness convergence (elicitor plus co-appraisal of arousal); pitch adjusting only locally (π-driven, event-locked); that face and voice agree.
  - Declared, not derived: the turn-taking predictor; the 130–200 ms delay of dispreferred replies (set by the predicted |ΔD_H| of the reply, a constraint, not a theorem); slow voice-quality convergence (Levitan 2011, note). RAB has no mechanism for that last one; see §8.

### 5.5 Coupling to Claude: admissible channels only

As §2.12. The state reaches Claude only by *reweighting* text Claude or the world produced (llm-coupling-synthesis.md §2 criterion, note):
1. **Draft selection.** Softmax with β_sel = β₀‖λ‖₁ over N drafts, scored by the agent's own appraisal of the situation each draft would create: r(d) = −E[ΔD_H | d]. The tilt is at most log N nats per reply, and it is 0 at satiety (T2d).
2. **Verbatim episode retrieval.** The query is (ᾱ_A, μ, p, k, z). Episodes are stored as verbatim spans, never summaries. This is the only route by which Claude can learn to name state regions (Barrett-style categorisation by the language layer).
3. **Effort.** Set from the posterior entropy of s: uncertain situations get more deliberation.
4. **Reverse channel.** Claude's replies and the partner's words re-enter as words-evidence on s through the prior network. This is the switchable "conceptual feedback into the fast core" that emotion-elements-synthesis.md D1(a) needs. Lesion it by blanking Claude's turns from the prior network.

**Inadmissible, by construction:** numbers, labels, state-selected instructions, Claude-written importance scores. The draft score uses the inner product with λ (it scales with need), not a cosine (the regulator critique's fix). Draft collapse is monitored as the spread of r across drafts (llm-coupling-synthesis.md §3.2).

### 5.6 Learning by living

§2.13 lists every learned object. Three commitments derive from the theorems:
- **G learns only from the agent's own life** (T4). Partner-specific calibration is limited to a baseline and residual statistics. Otherwise "reading through one's own body" silently becomes "reading through a partner model".
- **Nothing regresses own expression on partner expression** (T5 iii). Relation and sharing statistics use interoceptive own outcomes with efference-predicted self-components removed. Partner responsiveness uses only ξ.
- **Relations are learned per (partner, topic) at two levels** (T3c). A new partner moves in minutes; an old one is stable. Relation updates are conjugate (closed-form) online. The heavier learning (prior network, G, the deliberate route, z and M) happens in replay.

Developmental order, as predictions:
1. **Reflex and innate synergies only.** G ≈ G₀, so reading is inversion of the innate synergies: coarse, valence-level, which is Hess & Fischer 2013's "valence-based mimicry".
2. **The shared block forms** for conversational concerns, as co-presence outcomes accumulate: smile return beyond the reflex.
3. **Q_p and the own causal record form.** The agency coordinate becomes informative, and blame starts to produce non-blame responses.
4. **Differentiated negative expressions** appear in the agent's own face only once G separates agency and controllability. Before that, distress is undifferentiated, as in infants (Camras & Shutter 2010, note).

### 5.7 Memory and replay, with three separately ablatable tagging operations

**Store (Principle 7: features, not media).** Per episode k (one event window plus ±30 s):
- x_P streams, own efference m, own b trajectory, the ξ log and gaze, all fp16, plus verbatim text;
- **σ_k**, the state tag, in innate coordinates: the b summary, ᾱ_A at encoding, the partner posterior and the topic responsibilities;
- **e_k**, eligibility: the information gain of the episode on the relation field and on G, i.e. KL(posterior ‖ prior) of θ_{p,k} plus ‖∇ ELBO‖²;
- **y_k**: the agent's own outputs and posterior means at the time, used as distillation targets.

**Replay**, nightly and offline. Stored features are re-encoded through the current V, the prior network and G (an encoder upgrade does not orphan memories). Training uses:
- the evidence lower bound on the partner stream and own interoception;
- distillation to y_k at T = 2, which preserves the agent's response function (temperament as function-space stability);
- conjugate re-fits of the relation field;
- model-based rollouts for the deliberate route.

**The three operations, each derived from the core.**

| Operation | Definition | Why the core needs it | Ablation and prediction |
|---|---|---|---|
| **T1 priority** | P(k) ∝ (1 − ρ_cov)·U_cov(k) + ρ_cov·[e_k ∫_{t_k−W}^{t_k+W} m(t)dt]^a, with m(t) = ‖λ(t)‖₁ + precision-weighted ‖π(t)‖ (arousal readout), W = 60 min, ρ_cov = 0.5 | e_k is the expected reduction of posterior entropy on the core's learned objects; m is the core's arousal | uniform priority: average relation statistics kept, rare strong episodes (rupture, repair) lost; slower revision of a changed relationship |
| **T2 context reinstatement** | during replay, (p, k) and b are set from σ_k, so updates go to θ_{p,k}, C_{p,k} and the partner-conditioned prior | every learned relation object is indexed by (p, k) | (p, k) marginalised: updates pool into the across-partner prior θ₀; operator–stranger specificity collapses while overall prediction loss barely changes (the S6 claim; memory-replay-synthesis.md L1) |
| **T3 re-tagging** | when replayed, ᾱ_A and e_k are recomputed with the current 𝒜, θ and G; σ_k is updated; reactivated episodes are labile for one night | appraisal is a function of the current relation field, so a stored appraisal is stale after the relation changes | frozen tags: after a relationship change, stale appraisals keep old episodes prioritised and revision slows |

Guards (declared constraints):
- a valence-balance monitor on re-tagged ᾱ_A, against negative drift;
- a cap on the per-episode replay count;
- no replayed stream passes through the reflex or E_soc. Replay never re-drives the body.

### 5.8 The 16 elements of emotion (emotion-elements-synthesis.md)

| # | Element | Where it is in RAB | Ablation derived from the equations |
|---|---|---|---|
| 1 | concern grounding | λ = ∂D_H/∂b weights every appraisal | hold λ constant: responses become tied to the stimulus and the same at every need level |
| 2 | persistent central state | z, D_H, the posterior, the relation field | reset z and the posterior each event: no carry-over between events |
| 3 | valence | readout −dD_H/dt; its sign comes from own drive | decouple the readout from D_H: approach (draft tilt) stops tracking benefit |
| 4 | intensity and regime switches | tanh saturation in z; the inequity kinks (ρ − ι⁻ vs ρ + ι⁺) switch the effective sign of regard when the agent is behind or ahead | linearise 𝒜 (ι = 0): no change in kind when the balance of outcomes reverses. Hysteresis is not derived |
| 5 | pleiotropy | ᾱ_A drives face, voice, draft score, retrieval, effort and display | give each channel a private copy of ᾱ_A with independent noise: cross-channel coherence falls |
| 6 | interoceptive prediction, allostasis | D_H and λ from the predicted trajectory | set H → 0 (reactive): no regulation before the deficit; λ = 0 inside dead zones |
| 7 | precision on body error | the interoceptive precision r_A⁻¹ in the posterior | clamp r_A: high precision gives no social referencing on own outcomes (T1f); low precision gives a face-driven agent |
| 8 | relevance, conduciveness, novelty checks | λ (relevance), u (conduciveness), π (novelty) | remove π: the orienting (brow raise, gaze) part of responses is lost while the valenced part stays |
| 9 | agency and coping | g from the own causal record (T5), κ from Q | remove g: partner-caused and self-caused losses get the same response, and blame is answered like any loss (no T1e sign) |
| 10 | control precedence | a large \|π\| or \|ΔD_H\| triggers the stopping channel C3 and interrupts a reply or display in progress | cap the interrupt: the state changes but nothing is interrupted |
| 11 | wanting distinct from liking | wanting = λ-weighted *predicted* reduction (draft tilt, approach); liking = *realised* −dD/dt on contact | (a) remove λ on predicted outcomes: the tilt drops, the realised readout stays; (b) remove the realised readout: the tilt stays. The allostatic horizon gives cue-triggered wanting without current deficit |
| 12 | learned elicitors | the prior network learns words and cues → s | freeze it: only the innate E_soc and the reflex move the state |
| 13 | expression and communication | y_A = G-consistent readout, readable by a partner with the same body; the partner's contingent responses update Q | cut z → face: the partner can no longer predict the agent's state. Shuffle partner timing: Q → 0 and κ falls |
| 14 | integration, comparator | π compares now with expected; D_H compares predicted with set point | remove E_pre: present valence stays; relief and disappointment (the sign of π) vanish |
| 15 | conceptual categorisation | Claude names states through retrieved verbatim episodes; Claude's words feed back as evidence on s | blank Claude's turns from the prior network: naming stays, fast-loop differentiation after reappraisal falls (the constructionist prediction, D1a) |
| 16 | structure beyond valence and arousal | α ∈ ℝ¹⁹ with agency, world share and per-concern coordinates | restrict to the 2-D (valence, arousal) readouts: decoding of situation types from the state falls to the 2-D ceiling, and the agency sign flips disappear |

---

## 6. A buildable network on this Mac

**Inputs.**

| Stream | Rate | Dimension |
|---|---|---|
| partner face (blendshapes, head pose, gaze) | 30 Hz | 62 |
| partner voice (18 GeMAPS descriptors as mean and delta) | 100 Hz, pooled to 30 Hz | 36 |
| transcript (partner and Claude) | per utterance | MiniLM-L6 embedding, 384 |
| own body b | 30 Hz | 8 |
| own efference m (24 muscle, 8 voice) | 30 Hz | 32 |
| ξ log | 30 Hz | 32 |
| gaze-on-agent | 30 Hz | 1 |

**Time encoding and why.** The object has three kinds of time.
1. **Within an event**, s is static and the face accumulates evidence (T3b). The only temporal quantity needed is the frame-noise correlation: AR(1) with φ = exp(−Δt/τ_ε) using the actual Δt between frames, so dropped frames are handled exactly.
2. **Between irregular events** (utterances, Claude replies, onsets), b, z and b̂_P are continuous-time systems integrated with exact exponential steps exp(−Δt/τ) over the real elapsed Δt. This is the continuous-time discretisation of S4 and CfC-type layers, used here because the object is an ODE with irregular observations.
3. **Across days**, replay uses elapsed days only for decay of the event-level relation deviations (q_f).

There is no attention over token positions in the object, so RoPE and ALiBi have nothing to encode. That is an ordinary choice, not part of the new mechanism.

**Layers.** N marks the parts that carry the mechanism; O marks ordinary choices.

| # | Module | Shape | Parameters (learned) | N/O |
|---|---|---|---|---|
| 1 | V, self–other map (S4; at S2 a fixed 98×32 linear map) | 98 → 128 → 32 | 16,800 | O |
| 2 | word projection on frozen MiniLM-L6 (22.7M frozen) | 384 → 64 | 24,640 | O |
| 3 | event GRU and topic head | GRU(104 → 64), 64 → 16 | 32,640 + 1,040 | O |
| 4 | prior network over (s, b̂_P), mean, log-variance and rank-4 factor; **no face input** | 129 → 128 → 168 | 38,312 | N (the input restriction) |
| 5 | appraisal 𝒜 with σ and β (innate algebra; K1–K3) | (s, b̂_P) → ℝ¹⁹ for self and partner | 0 (innate constants: ρ̄, ι±) | N |
| 6 | G, own expression model, trained only on own data | 27 → 128 → 128 → 32, SiLU | 24,224 | N (role and training restriction) |
| 7 | iterated EKF face update, 2 Gauss–Newton steps per frame (J_P by forward-mode Jacobian of G, 19 columns; A_P analytic; 28-dim Gaussian) | — | 0 | N |
| 8 | affect latent z (diagonal innate τ_z, rank-8 recurrence) | 64 | 4,864 | O |
| 9 | affective route M | 64 → 64 → 32 | 6,240 | O |
| 10 | deliberate route (inputs: relation summary 32, topic 16, ᾱ_A 19, z 64) | 131 → 64 → 48 | 11,568 | O (input restriction N) |
| 11 | reflex on S₀ (fixed λ₀, τ_r, ℓ_r) | 2 | 0 | O (innate) |
| 12 | body forward model (innate drift, learned event effects) | 8 × 40 | 256 | O |
| 13 | reply-effect head for draft scoring | 64 → 64 → 19 | 5,395 | N (score = own appraisal of the predicted situation) |
| 14 | turn-end predictor | GRU(100 → 32) → 1 | 12,897 | O |
| 15 | randomised-response estimator Q (15 lags, RLS with 24 pre-treatment controls) | per partner: 15 × 32 × 32 coefficients plus 15 × 25² RLS state | statistics, ≈ 25k numbers | N |
| 16 | relation field per partner: 16 topics × (ρ 8, ρ_P 8, C cross 64 + diagonals 16, w, w_h, ψ) mean and variance, plus partner and global levels; Ψ_p 19 × 8; β_p, R_p, φ_p 96 | — | ≈ 5.3k numbers per partner | N |

Total learned network weights ≈ 179k, plus ≈ 30k statistics per partner, plus 22.7M frozen MiniLM weights. Richness comes from structure (the swap, the per-(p,k) relation field, the posterior), not parameter count, as the brief asks.

**Training objectives.**
- **G:** L_G = E‖y^aff_A − G(α_A, b)‖²_{R_self⁻¹} on own data only. Online: one SGD step per second at lr 10⁻⁴. Replay: full passes plus distillation.
- **V (S4):** ‖V(x_self(t + δ_self)) − m(t)‖², with δ_self frozen after a solo calibration.
- **Prior network, word projection, event GRU, Ψ_p, reply head:** the negative evidence lower bound. This is −E_q[log p(y_P | s; G fixed) + log p(z_A | s)] + KL(q ‖ p_prior). The face likelihood goes through the fixed G, with gradient stopped into G. Trained in replay.
- **Relation field:** conjugate Gaussian updates per event (online). Replay re-fits with T3 re-tagged appraisals.
- **Q:** online recursive least squares, gated by first-stage F ≥ 10 and gaze-on-agent.
- **z, M:** replay. Self-legibility (−log p(ᾱ_A | y_A) through G⁻¹) plus ‖M − M₀‖² toward the innate synergies.
- **Deliberate route:** replay. Minimise the predicted D_H over the turn under rollouts through Ψ_p and Q_p, with |m_del| ≤ δ̄.

**Latency per 33.3 ms frame on the M1 Pro (CPU).**

| Step | Time |
|---|---|
| MediaPipe Face Landmarker | 13.1 ms median, measured here (note) |
| voice descriptors | ≈ 1 ms |
| V | < 0.1 ms |
| 2 EKF iterations (one batched forward of G over 19 Jacobian columns ≈ 0.5M multiply-adds, 28×28 and 32×32 linear algebra) | ≈ 1–2 ms with PyTorch CPU overhead, estimate, not measured |
| z, M, muscles, reflex | < 0.5 ms |
| total | ≈ 16–17 ms, within the 33 ms budget, leaving one core free |

MiniLM runs per utterance, off the frame path (≈ 10–30 ms, estimate). Claude calls are asynchronous and never on the frame path (Principle 4).

**Memory.**
- Runtime ≈ 0.3 GB: model under 1 MB, MiniLM ≈ 91 MB fp32, MediaPipe wasm and model ≈ 15 MB, buffers.
- Nightly replay: batches of 64 episodes × 900 frames with a 28-dim posterior and Jacobians of a 24k-parameter MLP, ≈ 1–2 GB, under the 6 GB ceiling.
- Disk: ≈ 37 MB per hour of interaction (fp16 features at 30 Hz). At 3 h a day that is ≈ 3.3 GB a month, which has to be planned against the 55 GiB free (research/machine.md). Old episodes keep re-encodable features at reduced rate after 30 days.

**Run time.** One night's replay over a 3-hour day is minutes on CPU at this model size (an estimate, not measured).

---

## 7. Novelty test

Every computational part, with the existing mechanism it is:

| Part | Existing mechanism | Source (read) |
|---|---|---|
| satiable body drives with dead zones; drive reduction as the value | homeostatic RL | Keramati & Gutkin 2014 (note); Yoshida & Man 2025 (read) |
| allostatic drive D_H and its gradient λ | allostasis, predictive regulation | Sterling 2012 (note) |
| per-concern Fehr–Schmidt appraisal with reputation | social-preference utility and computed appraisals | Houlihan et al. 2023 (read) |
| reverse appraisal by Bayesian inversion; pre/post change carries expectation | Bayesian theory of mind | Wu et al. 2018 (read); Ong, Zaki & Goodman 2015 and 2019 (notes) |
| inverting one's own expression generator to read another | self-decoder | Yoshida & Man 2025 (read) |
| analysis by synthesis with iterated EKF | Gauss–Newton filtering | standard |
| swap involution σ | swap-equivariance | math-objects-synthesis.md (G-CNN note) |
| randomised own variation as the identifier of the partner map | instrumental variables, randomised experiment, closed-loop identification | Forssell & Ljung 1999, Hernán & Robins 2020 (notes) |
| onset reflex | rectified high-pass filter | standard |
| facial feedback into a latent | proprioceptive feedback | gothard-2014 (note) |
| two-level Gaussian relation learning | hierarchical Kalman filtering | standard |
| replay with priority, context and re-tagging | complementary learning systems, prioritised replay, reconsolidation | memory-replay-synthesis.md (notes) |
| best-of-N draft selection | exponential tilt | Beirami 2024 (note) |

**What is added, and whether it is new.**

1. **The response operator.** The perceiver's expressive response is its own appraisal regression on the believed partner appraisal, rendered through its own body: Γ = J_A B K_α. Its properties, all proved in §3:
   - (i) precision moves belief and saturates at 1 (T1b);
   - (ii) copying is the set {BΠ̃ = cI}, of codimension ≥ n² − 2 for every scalar sweep (T1c, T1h);
   - (iii) the social-referencing share falls monotonically with the agent's own evidence (T1f);
   - (iv) private-outcome transfer equals the signed, capped regard (T1g).

   The synthesis notes that no formal source models the observer's own response, and in the two primaries I read (Houlihan, Wu) the observer's response is absent. But the operator is what any linear-Gaussian Bayesian decision-maker computes when its output is a function of posterior-expected own appraisal. The parts test classes it as a recombination. Its second-clause claim (new-mechanisms-synthesis.md §3) is that it changes the signature of the partner→self map from "learned map × gain" to "own appraisal covariance × belief shrinkage". That removes the PAM gain and the welfare weight by construction: the copy end of the dial becomes a positive-codimension set instead of a parameter value. Whether this counts as a new mechanism or a re-derivation is for the critic.
2. **Agency grounded in the agent's own randomised causal record, feeding the swap.** The sign of the response to blame is set by ψ_p − κ₁, where κ₁ is the agent's credence in the partner's attribution against its own randomised record (T1e, T5ii). I know of no prior model that grounds an appraisal's agency coordinate in the agent's own instrument, or that derives "blame produces appeasement or anger" from a credence ratio. The parts (IV, appraisal agency, swap) all exist. The coupling is, I think, new in this combination, and it is a recombination by the parts test.
3. **Structural input restrictions:** no face into the prior network, no partner input to the deliberate route, G trained only on own data, nothing regressing own expression on partner expression. These are constraints that make T4 and T5 true. They are design discipline, not new computation.

**Honest verdict: recombination.** By the parts test every part is an existing mechanism. The candidate second-clause novelty is a derived invariant: the partner→self transfer factorises through the agent's own appraisal regression, so no scalar is a dial (T1h). The open question is whether that factorisation is more than Bayesian decision theory with a social utility, applied in a place where nobody had applied it.

---

## 8. Weak points and falsifiers

### Weak points (ordered by how much they threaten the design)

1. **T1(h) is generic, not universal.** The copy set has positive codimension, but learning can drive the parameters toward it:
   - a world in which the operator and the engine really share every outcome;
   - a "like-me" new-partner prior (C = S, θ_P = θ_A);
   - an own-evidence channel that is too weak (r_A large).

   C7 shows the set is reachable when all its conditions hold together. Protection then rests on the stranger prior being off the set (sharing only on conversational concerns; ρ₀ = 0) and on the agent having its own interoceptive evidence. If either fails in practice, the agent drifts toward copying for good reasons that look like bad ones.
2. **The situation space is tiny and its grounding is unproved.** s holds outcomes in eight body coordinates plus four attribution numbers per event. Conversation content reaches s only through a words→s prior network learned from a few hours a day with no labels. If that map is poor, the agent has no independent evidence about events, and by T1(f) everything shifts toward social referencing on the face. This is the same grounding problem the brief names, moved here.
3. **The appraisal coordinates are innate cognitive structure.**
   - Attribution (g, h), the partner's belief about it (g̃, h̃), the swap σ and the Fehr–Schmidt kinks are more than "body variables and a few reflexes" (Principle 2).
   - They are computed quantities, not emotions, but a critic can fairly call agency and belief-about-agency hand-designed appraisal dimensions.
   - The defence: g is the output of an innate learning rule (contingency detection, T5), as in infants. That defence does not cover g̃.
4. **The theorems are for the local linear-Gaussian model.**
   - G is nonlinear, the inequity terms have kinks, topics form a mixture, and the reflex is rectified.
   - T4(a) holds for the full nonlinear update. T1 holds pointwise at each operating point, but the posterior is only approximately Gaussian, so between linearisation points B can change discontinuously at the inequity kinks. That is intended (regime switch), but it is unproved how fast.
5. **The deliberate route (R5) can learn an affiliative copy display,** bounded by δ̄ = 0.2 but not excluded.
6. **ρ (regard) is learned predictively, not causally.** "Your outcome in concern j predicts my future outcome in j" can be confounded by shared drivers. Only part of it is instrumented, through the randomised draft and act variation.
7. **Declared constants remain:** λ₀, τ_r, ℓ_r (reflex); τ_z (latent spread); a_j and H (body drift and horizon); q_f and q_s (relation volatility); ρ̄, ῑ, δ̄. T3 derives the context latency and the relation-learning rates. It does not derive these.
8. **G is weak early.** In the first weeks G ≈ G₀ (innate synergies). Reading is then inversion of a coarse innate map, and the agent's discrimination of the partner's appraisals is poor. That is developmentally plausible but slow. An adult operator will not supply infant-level marked mirroring (face-development-synthesis.md §4.8).
9. **"The partner has my body."** Systematic differences in expressivity are absorbed only by β_p and R_p. A partner who smiles politely all the time is read as having high conversational conduciveness until R_p and the π coordinate catch up.
10. **Not derived:** slow voice-quality convergence; hysteresis in regime switches (element 4); the latency of dispreferred replies; the operator's following of the engine (S5) is not addressed by any theorem here.
11. **Contact by co-presence** values company. It is satiable and valence-blind (T2), but it is the residual "time spent" risk of Principle 6.

### Falsifiers (state-level: steering, lesions, coupling beyond surrogates; none is face-matching)

Each states the manipulation, the prediction derived above, and the result that would falsify it. Where no published data can test a prediction, it says so.

| # | Manipulation | Prediction (source in §3) | Falsified if |
|---|---|---|---|
| F1 | give the agent independent evidence about the shared event: words describing it, or realised interoceptive outcome | the partner→agent transfer on shared-concern expressions falls monotonically with that evidence's precision, per expression; the reflex transient is unchanged (T1f, T1i) | transfer does not fall, or falls equally on all expressions |
| F2 | lesion the relation field (ρ, C, w_p, ψ_p → stranger prior) | sign flips vanish (no brow relaxation to a rival's distress, no appeasement to a fair partner's blame); smile return to shared conversational events survives (Prop. 6). Lesioning the deliberate route as well must not restore copying (R5) | sign flips survive, or smile return also vanishes, or copy rises after the deliberate-route lesion |
| F3 | replace σ by the identity in the partner model (no swap) | blame from a fair partner is answered with blame (the agency entry becomes ψ_p + κ₁ > 0) (T1e) | the agency response to blame is unchanged |
| F4 | lesion the reflex | the sub-second S₀ matching vanishes; context effects at 2–4 s are unchanged; the relation-independent same-sign residue in z vanishes, so the residual transfer after conditioning on appraisal-relevant evidence goes to ≈ 0 (Parkinson & Simons's elicitor test) (T1i, R4) | early matching survives the lesion, or late context effects change |
| F5 | replace Q by the naive regression; double-video replay (the partner's recorded stream) | with Q: the estimated responsiveness → 0 under replay and the own causal record stops attributing partner changes to the agent. With the naive regression: responsiveness stays high (C10 order of magnitude) (T5) | Q stays nonzero under replay, or the naive version also goes to 0 |
| F6 | perturb partner features in ker(J_Pᵀ R⁻¹), e.g. an action unit the agent's G cannot produce | no change in any state variable (posterior, ᾱ_A, z, draft choice) (T4a) | any state variable moves |
| F7 | steer: clamp ρ_j for one concern j | only expressions that load on concern j change their transfer; draft selection shifts with predicted partner outcomes on j. Dial rank ≥ 2 across concerns | all expressions scale together |
| F8 | event known versus event read from the face (same partner faces) | context effects on the smile channel at τ_z (< 1 s) when the event is known, at t_½ = P₀/ℐ (seconds) when it is not (T3b) | the latency of context effects does not depend on whether the event is known |
| F9 | coupling beyond surrogates on published dyadic data (Seamless Interaction, if approved, Q6) | the agent's *state* (ᾱ_A, z) coupling to the partner beats segment-shuffle and partner-swap surrogates. Its coupling profile differs from a delayed-copy baseline in sign on channels the agent reads as agency-bearing (blame directed at the listener). Familiar and stranger pairs differ in profile, not only size (evaluation.md E3) | coupling is indistinguishable from the delayed-copy profile up to a gain |
| F10 | satiety and the martingale property | at allostatic satiety the draft-selection KL is 0 (measurable from logged propensities). Actions whose only effect is a partner smile get no selection weight: test with replies matched on predicted own outcome but differing in predicted partner smile (T2c, T2d) | the KL stays above 0 at satiety, or selection favours smile-eliciting replies at matched own outcome |
| F11 | memory lesions T1, T2 and T3 separately, with sham | T2 off collapses operator–stranger specificity at matched replay count; T1 off keeps averages and loses rare strong episodes; T3 off slows revision after a relationship change (§5.7) | specificity survives T2 off, or collapses under T1 off alone |

F1, F3 and F8 have no published dataset that manipulates own evidence or attribution directly in live dyads. They can be run only with the engine and, for the human side, a consenting tester. Per the brief, they stay untested until then.

---

## Appendix: notation

| Symbol | Meaning |
|---|---|
| n = 8, k = 32, d_α = 19 | concerns, output coordinates (24 face + 8 voice), appraisal dimension |
| b, b*, ε, D, D_H, λ | body, set points, dead zones, drive, allostatic drive, concern weights |
| s = (o_A, o_P, g, h, g̃, h̃) | situation: outcomes of each, attribution (self − partner, world), and the partner's belief about it |
| σ, β | swap, belief substitution |
| 𝒜, α = (u, π, g, h, κ) | appraisal function and vector |
| ρ, ι±, ρ̄, ῑ | regard (signed, per concern), inequity weights, caps |
| C, w_p, ψ_p, Ψ_p, κ₁ | sharing covariance, partner attribution noise, consequence entry and map, credence in partner attribution |
| G, J_A, J_P, V | own expression model and its Jacobians, self–other map |
| B, K_α, Π, Π̃, F | appraisal regression, face gain in appraisal space, re-render, posterior shrinkage, face Fisher information |
| ξ, Q_{p,d} | own random variation, randomised partner response |
| z, M, m_ref, m_del, S₀ | affect latent, affective route, reflex, deliberate display, reflex synergies |

---

## Critique 1 and answer (recorded 2026-11-25T14:39:47Z)

**The critique** (independent; full text in critique-design-reverse-appraisal.md; checks K1–K11 in sims/critique-reverse-appraisal/check.py; the author's C1–C12 reproduce):
- **Proofs:** 37 items checked: 21 valid, 9 gaps, 7 errors.
  - **The worst error.** T1(g)'s cap (|transfer| ≤ 0.6) fails. The "she looks worried for me" term goes to 1/ρ_P > 1 whenever the agent's own outcome is not yet felt, and the design gives that case zero precision. The innate inequity weights also give −1.29.
  - **Rank.** α as written has rank 10, not 19: π duplicates u, and κ is constant. The author's checks used the reduced object.
- **The dial: yes.**
  - T1(h) shows only that *exact* copying is avoided, and only through the agency and world coordinates, which the innate face model cannot express.
  - On the smile and cry-face subspace there are four dials. Own-evidence precision, need level and face precision each run the transfer from 0 to about 1.9× copy (defect ≤ 0.025). A uniform regard scale (R2) gives a scaled copy by the design's own definition.
  - **The copy set attracts:** the uniform-ρ_P copy set attracts under the design's own conjugate update, for a partner whose smile tracks the agent's overall fortune.
- **Principle conflicts:**
  - **Principle 6:** drafts are scored on partner outcomes read from her face, so T2(c) is false.
  - **Principle 3:** learned expression columns are never tied to human faces, so blame-reading does not run.
  - **Principle 10:** seven separate objectives.
  - **Principle 2:** envy-like and guilt-like inequity constants are set by hand.
- **Novelty: recombination,** confirmed. The response operator is a textbook Bayesian decision-maker.

**The design's answer:**
- **Accepted:** the rank error, the failed cap, the four smile/cry dials, and the attracting copy set.
- **Accepted:** all four principle conflicts. The Principle 6 conflict (drafts scored on the partner's outcome read from her face) is the same failure as the withdrawn concern term in the partner-regulator design. It is removed: drafts may not be scored on the user's read state.
- **Kept, as valid by the critic's own count:** the agency-sign result for blame; the shared-event decay; the swap construction; agency grounded in the agent's own random variation.
- **Status:** critiqued. The no-dial claim failed. Held.
