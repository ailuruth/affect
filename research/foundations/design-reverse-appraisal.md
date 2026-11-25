# Design: reverse appraisal through the agent's own body (RAB)

## Revision 2 (2026-11-26)

Revision 2 answers Critique 1 (critique-design-reverse-appraisal.md; summary and the original answer under "History" at the end) against the refined rule of D78 (questions.md Q18, operator's answer): no single quantity may run the whole face from flat to copy; each channel's strength must be set per expression by context and learned relationship, be able to flip sign, stay under an innate ceiling, and never let copying become an attracting state; every such quantity is named and bounded. What changed:

1. **True rank (Critique: "α has rank 10, not 19").** The appraisal is now α = (ℓ, w, a, h) ∈ ℝ^{2n+2}: realised drive change ℓ, prospective drive change w, agency a, world share h. Its true rank is 2m + 2, where m is the number of concerns the partner currently cares about (T0). π and κ are gone as coordinates: expectation violation is the prospective update w, and controllability is a slow state (§2.10). Every proof is redone on this object with pseudo-inverses on the true range (T1).
2. **The failed cap of T1(g) is replaced by a proved innate ceiling (T2).** The "she looks worried for me" term and the inequity weights no longer exist as utility terms. The face-to-face transfer of every channel pair obeys |Γ_ee′| ≤ ½ σ_A,e/√r_δ, where σ_A,e is the agent's own prior response spread and r_δ an innate floor on the variance of any one display (an event-level display effect). With the floor set to the innate maximum of σ_A,e², every entry is ≤ ½, for every parameter value and state. The appraisal regression B may still be large (it is in the critic's regime); the face cannot carry enough information to pass it on.
3. **The four smile/cry-subspace quantities are each handled (§3 T4 and the table there).** Own-evidence precision and need level no longer touch the smile/cry-face liking channels at all: those channels are driven only by the agent's felt body change (T1(e), T3). On the prospective channels they are per-concern, sign-set by learned covariances and capped by T2. Face precision is per channel, floored innately, and no common scale exists. The uniform regard scale is removed with ρ itself: the relationship is a per-concern learned covariance with no pooling across concerns. T4 proves the transfer is a sum of n + 2 rank-one terms, one per appraisal coordinate, and that every design quantity enters exactly one of them (context selectors excepted, stated).
4. **Whole-face copy is impossible, and copy is not attracting (T3, T5).** Because the liking channels (Duchenne cheek raise, nose wrinkle, eye squeeze) take input only from the felt body, the energy-weighted copy defect of the whole face is ≥ √(e₀/e) for every parameter value, where e₀/e is the share of the partner's expressive energy in those channels. The whole-face copy set is empty. On sub-faces, the learning targets are invariant to the agent's own expressive policy at the lags the instrument covers, the agent's own echo is explained away, the agent's own learning can only lower the ceiling, and the critic's attracting path (a partner whose smile tracks the agent's fortune) now yields zero or rank-one transfer (T5, D9).
5. **Principle 6 conflict removed (T6).** Drafts and displays are chosen by one KL-control tilt whose score is the predicted change in the agent's own drive under a predictor that sees no estimate of the partner's state. Regard terms and the partner-mood consequence map Ψ_p are gone. Drafts that differ only in their predicted effect on her face get equal scores.
6. **Learned expression columns are tied to human faces (T10(e)).** One expression map G is shared by self-rendering and partner-reading. It is built on an innate synergy basis with an innate orient-to-cause column, so blame is readable from day one (gaze and head toward the agent with a negative stake). Its loadings are learned from her face on windows where the agent's own felt outcome or its own randomised acts pin down her appraisal. No labels are used.
7. **One objective (T7).** Perception, learning, action, appraisal, controllability and replay are stationary conditions of one variational free energy of an extended model (control as inference). Ten explicit constraints are listed (§2.14).
8. **Hand-set inequity constants removed.** ι± are deleted. The within-game drop of smile return comes from the agent's own felt loss and the event-level covariance; regime switches come from the convex drive and its dead zones (§5.8 row 4).
9. **Controllability, coping, agency, wanting and liking from the same core (T8).** Controllability is a posterior over action-to-concern edges in the same model. Coping is the drive reduction the tilt achieves. Liking is realised drive change (the learning target), wanting is λ-weighted predicted change (the action score). Each has a derived ablation.
10. **Other repairs the critique asked for.** The reflex is removed: a fixed, context-blind gain violates D78, and live dyads do not mimic frowns (Hess & Bourgeois 2010, r = .08). The like-me identity T4(b) now holds. The image constraint is restated with its scope. The AR(1) frame noise is prewhitened and the event-level display effect is a filter state. The own causal record comes from draft randomisation, not from Q. Q is low-rank with a standard-error gate. ξ probes are sparse structured events.

**Kept, as the critic judged them valid:** the factorisation, the belief-only effect of face precision, the copy margin, the agency algebra (now with a learned sign), the world block, the shared-block algebra (now on prospective outcomes), the identification lemma for the partner map, satiety of D, bounded dependence, the two-level relation learning, and the compute budget.

**Status:** revision 2, not yet critiqued. Algebra checks D1–D10: `research/foundations/sims/design-reverse-appraisal/check_r2.py` (run from sims/ with `uv run python design-reverse-appraisal/check_r2.py`). The revision 1 checks C1–C12 remain in `check.py`. All checks test this document's own equations on random and hand-set instances; they are not results.

---

Written 2026-11-25 for questions.md Q16 and Q17 by an isolated design author; revised 2026-11-26. Nothing was downloaded except paper text. No data, no weights. Simulated worlds are not evidence here.

**Primary sources read for this design** (revision 1; revision 2 read no new primaries and works from the project notes marked "(note)"):

| Source | What was read | Used for |
|---|---|---|
| Houlihan et al. 2023, Phil Trans R Soc A (PMC10239682) | main text to the methods, two passes; Eqs. 3.1–3.4; model comparison numbers | computed appraisals over utilities; the model predicts the target, never the observer |
| Wu, Baker, Tenenbaum & Schulz 2018, Cogn Sci (PMC6033160) | introduction, model, Experiments 1–4, model comparison | beliefs recovered only from pre/post reactions; model-free regression .583 vs .957 |
| Carr, Winkielman & Oveis 2014, JEP:G | full author manuscript | corrugator before 1,000 ms, zygomaticus 2,000–4,000 ms; smiles to anger by power |
| Parkinson & Simons 2009, PSPB | accepted manuscript, results and discussion | residual transfer after appraisals; the elicitor test "regardless of the relationship" |
| Yoshida & Man 2025, arXiv 2506.12894 | method and limitations | D = D_possessor + w·D_partner, w = 0.5 |
| Hofman et al. 2012, Proc R Soc B (PMC3396901) | results and discussion (summary level) | smile return absent after unfair offers; anger return by partner fairness |

Notes used in revision 2: hess-bourgeois-2010-you-smile-i-smile.md (speaker–listener EMG: orbicularis oculi r = .59, zygomaticus .54, levator .44, corrugator .08); todorov-2009-linearly-solvable-mdps.md (KL control); berridge-kringelbach-2015-pleasure-systems.md (taste reactivity homologous across newborns, apes, rats); face-development-synthesis.md (neonatal Duchenne smiles without social trigger; disgust and cry faces without forebrain; mother and infant do not copy smile form); hess-fischer-2013 and bourgeois-hess-2008 (the target of an expression gates mimicry); agency-wanting-synthesis.md and its notes (Dorfman & Gershman 2019, Ligneul 2022, Huys & Dayan 2009, Maier & Seligman 2016, Zhang & Berridge 2009, Dayan & Berridge 2014, Robinson & Berridge 2008); llm-coupling-synthesis.md and beirami-2024 (draft selection as an exponential tilt); contingency-causal-synthesis.md; affective-robots-synthesis.md (Churamani 2022: a reward on user mood let users steer the robot by smiling). Not read, named only: Keltner 1995 on appeasement displays; Bissiri, Holmes & Walker 2016 on tempered likelihoods. Nothing below rests on them.

---

## 1. Plain-language intuition

When your friend's face falls, you work out what it *means*. She looks hurt and is looking at you, so she thinks you did something. She looks hurt and is looking at her phone, so something happened to her. What you feel next is your own reaction to the situation you have inferred, judged by what you care about. It is not her feeling copied.

Revision 2 keeps that core and adds three structural commitments that make copying impossible to reach by turning one knob.

- **Your felt body speaks for itself.** Some parts of a face report what the body has actually received: the cheek raise of a felt smile, the nose wrinkle of disgust, the eye squeeze of pain. Berridge calls these "liking" reactions, and newborns show them with no social trigger. In this design those channels are driven only by the agent's own felt body change. Her smile can make the agent *expect* something good. It cannot make the agent *feel* something it has not received. When both feel the same event (the same joke), both faces show it, because both bodies received it. No transfer is involved.
- **What you expect is shown on other channels.** Expectations (wanting, in Berridge's sense) show on orienting and approach channels: brow raise, eye opening, head toward or away, the social smile without the cheek raise, the corrugator. Her face moves the agent's expectations through what the agent has learned about the two of them: whether her good news has tended to mean good news for the agent, and whether her worry about the agent's prospects has been right. Each concern has its own learned relation, with its own sign.
- **No single display is trusted beyond your own range.** The agent treats any one display of another person as carrying its own idiosyncratic noise for that moment, with a floor the agent cannot learn away. A proved inequality follows: the response of any channel to one display is at most half the agent's own prior response spread, divided by that floor. With the floor set innately, no channel of the agent's face can respond to any one channel of hers with more than half that channel's size. Repeated evidence accumulates in the slow relationship statistics, not inside one moment.

Blame still works as before. If she looks at the agent with a negative face, the agent reads "you caused this" through its own body. In its own frame that says "I caused this", which pushes the agent's attribution toward itself. The result is gaze aversion and appeasement, not anger. The exception is a partner whose blame has been unreliable and who tends to retaliate; there the response turns to counter-blame. The sign of that response is learned per partner.

Words: the engine never scores Claude's drafts by how the user will look. It scores them only by what each draft is predicted to do to its own satiable body. The user's smile cannot change that body, so it has no value to the engine (Principle 6). Caring for the user is left to Claude's own drafts, whose distribution the engine only tilts by its own needs.

What the design still does not do: there is no classifier, no emotion label, and no named emotion variable. Every coordinate is a computed quantity over the agent's own body and its own causal record.

---

## 2. The precise mathematical object

### 2.1 Body, drives, and the one objective (innate)

- **Body variables.** b ∈ 𝔅 = ∏_j [b_j^min, b_j^max] ⊂ ℝⁿ, n = 8 (energy budget, arousal, social contact, predictability, learning progress, vocal effort, comfort, one reserve), with set points b* and dead-zone half-widths ε. The names are engineering names. The box is part of the body.
- **Drive.** d_j(x) = ½(|x| − ε_j)₊², D(b) = Σ_j d_j(b_j − b*_j). Convex, C¹, zero exactly on the dead-zone box.
- **Body physics.** ḃ = −A_b(b − b̄) + E_self m + E_soc(x_P) + e(t), with A_b = diag(a_j). E_soc has two innate, valence-blind components: co-presence (a face is detected, a voice is present) feeds the contact variable; loudness and looming above the partner's baseline feed arousal. Neither is an expression coordinate. e(t) are event inputs with |e_j| ≤ ē_j (innate).
- **Allostatic drive and concern weights.** D_H(t) = E_q[∫₀^∞ e^{−τ/H} D(b(t+τ)) dτ], λ(t) = ∂D_H/∂b(t). Because 𝔅 is bounded, 0 ≤ λ_j ≤ λ̄_j (innate). λ_j = 0 when the predicted trajectory of b_j stays in its dead zone under small perturbations.
- **The one objective.** Write 𝒪_{≤t} for everything observed up to t (the partner's features, words, the agent's own body path, its own efference and probe logs) and a for the agent's choices (drafts, displays). The generative model p_θ is extended with a default policy π₀(a) (Claude's own draft distribution; the innate display default, which includes the probes ξ) and a preference factor exp(−β ∫ D(b) dt) over future body paths (Todorov 2009, note; Kappen 2005, note). The agent minimises one variational free energy

  𝔉[q, θ] = E_q[ log q(Z, a) − log p_θ(𝒪_{≤t}, Z | a) − log π₀(a) + β ∫_t^{t+T} D(b(τ)) dτ ] + KL(q(θ) ‖ p(θ | 𝒪_{<day}))

  over the posterior q(Z) of all latents Z (situations, partner state, display effects, structure edges), the action distribution q(a), and the parameters θ. The last term is the previous day's parameter posterior as prior (replay). β is an innate constant. T7 shows that every component in §2.2–2.15 is a stationary condition of 𝔉 or one of the constraints listed in §2.14.

### 2.2 Situations

An event is a segmented window (§2.8). Each carries a latent situation

  s = (o_A, o_P, f_A, f̃_P, g, g̃, q, q̃, h, h̃) ∈ 𝒮 = ℝ^{4n+6}, dim 38.

- o_A, o_P ∈ ℝⁿ: the event-induced, realised change in each person's regulated variables, in the agent's own body coordinates. The partner is modelled as a body like the agent's (Principle 3).
- f_A ∈ ℝⁿ: the change in the agent's own future body over the horizon that the event predicts. f̃_P ∈ ℝⁿ: the partner's own predicted future change, as she believes it.
- g: realised-event attribution, self minus partner, agent frame; g̃: the partner's belief about it, agent frame.
- q: predicted future harm to the agent caused by the partner; q̃: the partner's predicted future harm to her caused by the agent.
- h: share attributed to the world or a third party; h̃: her belief about it.

The partner's body state b̂_P ∈ 𝔅 is a slow latent with the agent's own body physics as its prior, and λ̂_P = ∂D_H/∂b at b̂_P.

### 2.3 The appraisal function and the swap (innate algebra)

For an appraiser with concern weights λ and input (o, f, g_self, q_self, h):

  𝒜(o, f, g_self, q_self, h; λ) = (ℓ, w, a, h) := (−λ ⊙ o, −λ ⊙ f, g_self − q_self, h) ∈ ℝ^{2n+2}.

- ℓ: realised drive change per concern (positive = need reduced). w: prospective drive change per concern. a: agency balance (positive = the appraiser caused it; predicted harm from the other counts toward other-attribution). h: world share.
- **Agent:** α_A = 𝒜(o_A, f_A, g, q, h; λ_A).
- **Partner, as modelled:** α_P = 𝒜(o_P, f̃_P, −g̃, q̃, h̃; λ̂_P). The swap is the sign of the attribution (self minus other in her frame is −(agent minus partner)) and the exchange of roles; belief substitution replaces true attributions and futures by hers.
- **Self-anchor (innate).** The own-outcome coefficient is exactly 1 in drive units. There are no learnable cross-person utility weights: no regard ρ, no inequity weights ι±, no consequence map Ψ. Every cross-person dependence lives in the joint prior over s (§2.4). This removes the Principle 2 conflict of revision 1.

Expectation violation is w itself: the event-locked update of the predicted future drive. Realised surprise is ℓ minus the previous prediction, which the agent knows for itself and reads from her pre/post change (Wu et al. 2018).

### 2.4 The relationship as a learned covariance field

The prior over s at an event, given the words, the topic responsibilities and the partner p, is Gaussian: N(μ_s, Σ_s). The prior network supplies μ_s and per-coordinate variance scales (clipped at innate maxima s̄_j, v̄; constraint K4). The **relation field** Θ_{p,k} supplies the cross-person structure for partner p and topic k:

- per concern j, a 4 × 4 covariance Σ_j over (o_A,j, o_P,j, f_A,j, f̃_P,j). Its off-diagonal entries are the relationship: c^now_j = Cov(o_A,j, o_P,j) (shared realised events), e_j = Cov(f_A,j, o_P,j) (her realised outcome predicts the agent's future: the regard-like entry, sign free), c_j = Cov(f_A,j, f̃_P,j) (shared prospects; social referencing), and Cov(o_A,j, f̃_P,j) (her prospects follow the agent's felt outcome);
- the attribution block: g ~ N(0, v_g), g̃ = a_g g + η_g with Var η_g = w_p, q = ψ_p g̃ + η_q (Var v_q), q̃ independent (Var v_q̃). a_g ∈ ℝ is her attribution loading: positive for a partner whose blame tracks the truth, negative for one whose blame anti-tracks it. ψ_p is her retaliation slope;
- the world block: h ~ N(0, v_h), h̃ = a_h h + η_h, Var η_h = w_h.

**Constraint C-diag (K5).** Covariances are block-diagonal across concerns and across the three groups {concern j}, attribution, world. Events that move several concerns at once are carried by the mean μ_s, not by cross-concern covariance. This is what makes each expression's strength a separate quantity (T4). Its cost is listed in §8.

### 2.5 The shared expression map G (self-rendering and partner-reading)

G: ℝ^{2n+2} × 𝔅 → ℝ^k, k = 32 (24 facial coordinates, each an action-unit-level muscle activation, and 8 vocal source-filter settings):

  G(α, b) = S_H h_H(ℓ, b) + S_P h_P(w, b) + S_A h_A(a, h, s̄take, C, b).

- **S is an innate synergy basis**: fixed muscle co-activation patterns shared with human faces, not emotion templates (face-development-synthesis.md §4, note).
  - **S_H (liking family):** the Duchenne smile (AU6 + AU12), the cry-face with eye constriction, the gape and nose wrinkle (AU9/10 with tongue), the pain squeeze (AU4 + AU6 + AU7 + AU43). These are the taste-reactivity and neonatal reflex faces (Berridge & Kringelbach 2015, note; Steiner as cited in the face-development synthesis), and the vocal liking reactions (laugh-like and cry-like bursts, sighs).
  - **S_P (prospective family):** brow raise (AU1 + 2), upper-lid raise (AU5), corrugator (AU4), the social smile (AU12 without AU6), head forward/back, and on the voice F0 level, range and tempo.
  - **S_A (attribution family):** a fixed **orient-to-cause** column (gaze and head toward the partner when the partner is the cause, toward the scene when the world is, down and away when the self is); the confrontation synergy (AU4 + AU7 + AU23 with gaze at the cause, loudness up) used when coping is high; the withdrawal synergy (AU1 + AU4 oblique brow, head and gaze down) used when coping is low.
- **Family block-sparsity (innate, K3).** Each family's synergies take input only from that family's appraisal coordinates. s̄take = Σ_j |ℓ_j + w_j| gates the attribution family, which renders attribution only when something is at stake.
- **E₀, the liking-exclusive channels.** 𝒞₀ is the set of output coordinates loaded only by S_H: cheek raise (MediaPipe cheekSquint), nose wrinkle (noseSneer), upper-lip raise at the gape, tongue, eye closure in the pain squeeze. E₀ = span{e_c : c ∈ 𝒞₀}.
- **Learned part.** h_H, h_P, h_A are small maps with Lipschitz constant ≤ L̄ (spectral normalisation, innate L̄). The orient-to-cause column is fixed. h_* are learned from the partner-face likelihood of §2.7 (T10(e)). There is no separate learned affective route: what the agent renders and what it uses to read her are the same G.

### 2.6 Self–other map

V: x_P ↦ y_P ∈ ℝ^k maps the partner's sensed features (52 blendshapes, 4 gaze values at 30 Hz; 18 GeMAPS descriptors relative to her baseline) into the agent's coordinates. Head translation and scale (looming) and loudness go to E_soc only. At S2, V is fixed linear. At S4 it is learned from the agent's own rendered face at a frozen efferent–afferent delay (Stoytchev 2011, note).

### 2.7 Generative model of the partner's stream

  y_P(t) = G(α_P, b̂_P(t)) + β_p + (Q_p ∗ x_A)(t) + δ_e + ε(t).

- β_p: her baseline.
- (Q_p ∗ x_A): her response to the agent's own expression (the echo), with Q_p the identified partner map (§2.11), estimated only from the probe factor (K7).
- **δ_e ~ N(0, R_δ,p): an event-level display effect,** constant within event e: how she happens to show it this time. R_δ,p is learned per channel, but only above an innate floor, R_δ,p ⪰ r_δ I (K4). Frames within an event therefore do not add up to unlimited evidence.
- ε: AR(1) frame noise per channel (φ_{p,e}, R_ε,p), prewhitened.

The sufficient statistic of an event observed for t seconds is the prewhitened mean ȳ, with effective noise R_eff(t) = R_δ + R_ε′/t ⪰ r_δ I, where R_ε′ = R_ε (1+φ)/((1−φ) f_s).

### 2.8 Non-face evidence, inference, segmentation

- **Felt outcome (exact).** o_A is the observed change of the agent's own b minus the change the innate body physics predicts without the event. It is known exactly, so ℓ_A is known exactly.
- **Own causal record.** z_g = g + ν_g, the share of the partner's outcome change caused by the agent's last reply or act. It is identified by inverse-propensity weighting over the agent's randomised draft and display choices (§2.11).
- **Own prospective evidence.** z_f = f_A + ν_f from the body forward model and the words → situation part of the prior network, with per-concern noise R_f (C-diag).
- **The prior network** takes the transcript, topic responsibilities and the relation field, never x_P or y_P (K6). It outputs N(μ_s, Σ_s) of §2.4.
- **Face update.** The partner latent (s, b̂_P, δ_e) is updated each frame by two Gauss–Newton (iterated extended Kalman) steps on the prewhitened frame, with the echo subtracted. The face enters only through J_Pᵀ R⁻¹ (y − β_p − Q_p ∗ x_A − G(α_P(μ))). Gaze is an expression coordinate inside y and J_P, read through the orient-to-cause column; it does not enter the prior network.
- **Segmentation.** Event boundaries come from utterance boundaries, the agent's own events, and a change-point statistic on the whitened innovation projected onto im(R^{−1/2} J_P). A perturbation outside that image cannot open an event.
- Topics k ∈ {1..16}: responsibilities from the event GRU.

### 2.9 Response: rendering and the muscle layer

- **Filter bank.** z is an innate bank of leaky integrators of the posterior-mean appraisal ᾱ_A = (ℓ_A, ŵ_A, â_A, ĥ_A) and of b, with time constants spread over 0.2–30 s. Slower components come from D_H and λ.
- **Rendering.** y_A^aff = γ_del ⊙ G(z_fast, b), where z_fast is the fast filtered appraisal (unit DC gain). **The liking family is driven by the filtered felt ℓ_A only.**
- **Muscle layer.** m = y_A^aff + m_del + ξ, then first-order activation (τ_m = 50 ms), rendered on the placeholder face and the source-filter voice.
- **The display route.** γ_del ∈ (0, 1]^k (inhibition) and m_del (|m_del| ≤ δ̄ = 0.2, zero on 𝒞₀) are chosen by the same tilt as the drafts (§2.12). Their inputs are own state only: b, λ, felt history, own controllability, topic and partner identity. They see no estimate of her state (K6, K10).
- **There is no reflex.** Revision 1's fixed onset reflex had a context-blind gain, which D78 rules out. The fastest face-driven response is the inference route with a strong relation prior (T9(b)).

### 2.10 Controllability, coping, wanting, liking (one core; T8)

- **Controllability** χ_j = q(edge a → b_j): the posterior that the agent's acts move concern j. It is computed in the same model, with the agent's own randomised variation (ξ, draft randomisation) as the identifying variation.
- **Coping** C_j = E_{π₀}[ΔD_H,j] − E_{q*(a)}[ΔD_H,j]: the drive reduction on concern j that the tilted policy achieves over the default.
- **Liking** ℓ (realised drive change) is the target the body predictor learns from and the input of the liking family.
- **Wanting** w (λ-weighted predicted change) is what the action tilt scores and what the prospective family shows.

### 2.11 Own random variation and the two identified maps

- **Probes.** ξ: sparse structured events (brief holds, small nods, a 0.5–1 s brow or smile pulse) at two amplitudes, drawn from a dedicated logged generator, never computed from partner input, never on 𝒞₀.
- **Q_p (her face's response to the agent's face).** Lags 0.1–2.9 s, parameterised as L = 4 lag kernels × a rank-4 channel map. Estimated by regression on ξ with pre-treatment controls. An update is accepted only when the reduced-form standard error of the kernel is below τ̄. Uses: the echo term in §2.7 and the controllability of contact through the face.
- **Reply effects.** The agent's draft choice is randomised with logged propensities. The effect of a reply on her subsequent outcome and on her expressed attribution is identified by inverse-propensity weighting (Hernán & Robins, note). Uses: z_g, and learning a_g, w_p, ψ_p.
- **Not a use:** neither Q nor any reply effect is a reward or feeds a body variable (Principle 6).

### 2.12 Coupling to Claude (admissible channels only)

1. **Draft selection (C1).** N = 4–8 drafts d_i. Score r(d_i) = −E_θ[ΔD_H | d_i, o_t], with o_t the agent's own state (b, λ, felt history, own causal record, topic, partner identity) and the transcript as text. The predictor sees no estimate of her state: no α̂_P, no b̂_P, no reading of her face or voice (K6). Selection is the tilt q*(d) ∝ π₀(d) exp(β r(d)) restricted to the N drafts (self-normalised), with innate β. Positivity holds because the scores are finite. Propensities are logged.
2. **Context (C4).** Verbatim episodes retrieved by the own-state query (ᾱ_A, b, p, k, z).
3. **Settings (C5).** Effort is set by the entropy of the agent's own prospective and attribution posterior.
4. **Reverse channel (C7).** Claude's replies re-enter as words evidence on s through the prior network.

Claude never sees a number, label or state description (Principle 4).

### 2.13 What is learned, and which term of 𝔉 learns it

| Object | Learned from | Rule (stationary condition of 𝔉) | When |
|---|---|---|---|
| G loadings h_H, h_P, h_A | her face on windows where ℰ pins her appraisal (shared felt events; agent-caused events) | gradient of the partner-face log-likelihood, under the spectral cap | online small steps; replay |
| V (S4) | own rendered face at frozen delay | own-face likelihood | replay |
| β_p, R_δ,p (above floor), R_ε,p, φ_p | residuals | Gaussian M-step | online, frozen within a session |
| prior network, word projection, event GRU, turn-end predictor | words, own body, her stream | ELBO terms | replay |
| relation field Θ_{p,k} (Σ_j blocks, a_g, w_p, ψ_p, v_q, a_h, w_h) | felt o_A, posterior of her α_P, z_g, reply effects | EM M-step with posterior second moments (not plug-in means), two levels | online; re-fit with re-tagged events in replay |
| Q_p | ξ log and her face | ML of the probe factor (K7) | online |
| body predictor p_θ(b_{t:t+T} \| a, o_t) | own body after own acts and drafts | conditional likelihood of realised outcomes (liking is its target) | online; replay |
| structure posterior χ | own body after randomised acts | Bayes factor of edge vs no edge | online |
| action distribution q(a) | none: computed | exponential tilt | per turn |

### 2.14 Constraints on the objective (Principle 10's "explicit constraints")

- K1. Innate body: 𝔅, b*, ε, D, A_b, E_soc (valence-blind), event bound ē, horizon H.
- K2. Innate appraisal algebra 𝒜, the swap, the self-anchor; no learnable cross-person utility weights.
- K3. Innate synergy basis S, family block-sparsity, the fixed orient-to-cause column, 𝒞₀, spectral cap L̄.
- K4. Innate display floor R_δ ⪰ r_δ I with r_δ = σ̄² (T2), and variance clips: s̄_j on the prior variance of f_A,j, and v̄_g, v̄_q, v̄_h on the variances of g, q and h that the prior network and the relation field imply together (so ψ_p and w_p are bounded through them).
- K5. C-diag, P1′ (the attribution and world blocks are a priori independent of the outcome blocks and of each other), P2 (g is observed only through z_g; words and face speak to g̃, q̃, h̃).
- K6. Information restrictions: the prior network never sees x_P; the draft, display and gate factors and the retrieval query use own state only.
- K7. Q_p is estimated only from the probe factor and tied into the emission's echo term.
- K8. Positivity: σ_ξ > 0 always; β finite.
- K9. Replay never drives the body; re-tagging is labile for one night; a per-episode replay cap.
- K10. m_del and γ_del act only through channels outside 𝒞₀ (m_del) or as per-channel gains; |m_del| ≤ δ̄.

### 2.15 Memory

Episodes store feature streams, own efference, b trajectories, the ξ and propensity logs and verbatim text, with three tags: state σ_k, eligibility e_k (information gain on Θ and G), outputs y_k. The three operations T1 priority, T2 context reinstatement and T3 re-tagging are separately ablatable (§5.7).

---

## 3. Theorems with proofs

### The local model (LM) and the definitions used

Fix the slow objects at their current values: λ_A, λ̂_P (b̂_P at its posterior mean), the relation field at (p, k), R = R_eff, β_p, Q_p, G. Linearise G at the current posterior mean. Let ℰ be all non-face evidence (felt o_A, z_g, z_f, words); s | ℰ ~ N(μ_ℰ, Σ_ℰ). Let A_A, A_P be the linear maps s ↦ α_A, α_P of §2.3. Write

- V_A = A_A Σ_ℰ A_Aᵀ, V_P = A_P Σ_ℰ A_Pᵀ, C_AP = A_A Σ_ℰ A_Pᵀ;
- J_A = diag(γ_del) ∂G/∂α at (ᾱ_A, b), the Jacobian of the rendered route (exact, because the rendering is G itself with unit DC filter gain); J_P = ∂G/∂α at (α_P, b̂_P);
- y = ȳ − β_p − Q_p ∗ x_A, so y = J_P α_P + noise with covariance R;
- B = C_AP V_P⁺ (appraisal regression), K_α = V_P J_Pᵀ(J_P V_P J_Pᵀ + R)⁻¹ (face gain), Π̃ = K_α J_P (belief shrinkage), W = R^{−1/2}.

The steady transfer of the appraisal route is Γ := ∂E[y_A^aff | ℰ, y]/∂y = J_A Cov(α_A, y | ℰ) Var(y | ℰ)⁻¹.

The variance of b̂_P is held out of the local model. It would add an independent positive semidefinite term to V_P, which leaves T2 and T3 unchanged (T2 does not depend on V_P, T3 is structural) and dilutes B in T1(f)–(g).

**Copy, defect, dial.** E := J_P(im V_P), the partner expressions the agent can explain as appraisals, in its own coordinates. Γ copies on a subspace U ⊆ E if Γ|_U = c·id_U, c > 0. Two defects are used:
- the operator defect δ_U(Γ) = min_c ‖W(Γ − cI)W⁻¹|_U‖ / ‖WΓW⁻¹|_U‖;
- the energy-weighted defect δ_Σ(Γ) = min_c ‖(Γ̃ − cI)Σ̃^{1/2}‖_F / ‖Γ̃ Σ̃^{1/2}‖_F, with Γ̃ = WΓW⁻¹ and Σ̃ = W J_P V_P J_Pᵀ W the whitened energy of her expressions. This answers the critic's objection that the operator defect is dominated by directions the face barely carries.

A quantity p is a **dial on U** if, on an open set of the other parameters, sweeping p takes ‖Γ|_U‖ from below η to above η while δ_U(Γ) < ε at the upper end, for small fixed η, ε.

### T0. True rank

rank A_P = 2m + 2, where m = #{j : λ̂_P,j ≠ 0}. If the prior is positive definite and no non-face evidence fixes a partner coordinate exactly, rank V_P = 2m + 2 and im V_P = im A_P.

*Proof.*
1. The rows of A_P act on disjoint coordinate sets of s: ℓ_P on o_P (by −Λ̂_P), w_P on f̃_P (by −Λ̂_P), a_P on (g̃, q̃) (by (−1, −1)), h_P on h̃.
2. So rank A_P = rank Λ̂_P + rank Λ̂_P + 1 + 1 = 2m + 2.
3. V_P = A_P Σ_ℰ A_Pᵀ has rank equal to rank A_P when Σ_ℰ is positive definite on the span of the rows of A_P. The felt o_A is exact, but o_P keeps positive conditional variance whenever |corr(o_A,j, o_P,j)| < 1 (positive definite prior). ∎

D1 checks this: rank 8, 6 and 2 for λ̂_P with 3, 2 and 0 nonzero entries (n = 3). Revision 1's α had an affine copy of u and a constant κ (Critique, K1). Neither exists here. Every statement below is on im V_P, with pseudo-inverses.

### T1. The transfer at the operating point

**T1(a) Factorisation.** Γ = J_A B K_α.

*Proof.*
1. y depends on s only through α_P, so y ⊥ α_A | (α_P, ℰ).
2. If v ∈ ker V_P then Var(vᵀα_P | ℰ) = 0, hence Cov(α_A, vᵀα_P | ℰ) = 0. So ker V_P ⊆ ker C_AP and C_AP = C_AP V_P⁺ V_P.
3. Gaussian conditioning on a singular covariance: E[α_A | α_P, ℰ] = μ_A + C_AP V_P⁺ (α_P − μ_P), because α_P − μ_P ∈ im V_P almost surely.
4. Tower rule: E[α_A | y, ℰ] = μ_A + B(E[α_P | y, ℰ] − μ_P), and E[α_P | y, ℰ] − μ_P = K_α (y − J_P μ_P).
5. Differentiate and apply J_A. By step 2, J_A B K_α = J_A C_AP J_Pᵀ (J_P V_P J_Pᵀ + R)⁻¹, the direct formula. ∎

D2: maximum difference 5.6 × 10⁻¹⁶ over 200 instances, including λ̂_P with zero entries.

**T1(b) Precision moves belief, bounded by 1.** On im V_P, Π̃ is similar to X(X + I)⁻¹ with X = V_P^{1/2} F V_P^{1/2}, F = J_Pᵀ R⁻¹ J_P. Its eigenvalues lie in [0, 1), and each is non-increasing when the non-face evidence becomes more precise. With the display floor, X ⪯ V_P^{1/2} J_Pᵀ r_δ⁻¹ J_P V_P^{1/2}.

*Proof.*
1. Let M̃ = W J_P V_P^{1/2}. Then V_P^{1/2} J_Pᵀ(J_P V_P J_Pᵀ + R)⁻¹ J_P V_P^{1/2} = M̃ᵀ(M̃M̃ᵀ + I)⁻¹M̃ = M̃ᵀM̃(M̃ᵀM̃ + I)⁻¹ (push-through identity) = X(X + I)⁻¹.
2. So on im V_P, Π̃ = V_P^{1/2}[X(X + I)⁻¹]V_P^{1/2+}. The eigenvalues are x/(1 + x) ∈ [0, 1) for the eigenvalues x ≥ 0 of X.
3. The nonzero eigenvalues of X equal those of Y = F^{1/2} V_P F^{1/2}. Y is Loewner-monotone in V_P. More precise non-face evidence lowers Σ_ℰ and hence V_P in the Loewner order. By Weyl's monotonicity each eigenvalue of Y, and so of Π̃, does not increase.
4. F ⪯ J_Pᵀ r_δ⁻¹ J_P because R ⪰ r_δ I. ∎

This repairs two points the critic raised. F need not be invertible (G₀ has low rank), and "Loewner decrease" is stated on the eigenvalues.

**T1(c) The exact copy condition.** For v ∈ im V_P, Γ J_P v = J_A B Π̃ v. If J_A = J_P = J is injective, then Γ|_E = c·id_E is equivalent to BΠ̃ = cI on im V_P. Under T1(e) below this has no solution with c ≠ 0 whenever m ≥ 1.

*Proof.*
1. Γ J_P = J_A C_AP J_Pᵀ(J_P V_P J_Pᵀ + R)⁻¹ J_P = J_A C_AP V_P⁺ [V_P J_Pᵀ(·)⁻¹ J_P] = J_A B Π̃, by T1(a) step 2.
2. With J injective, J BΠ̃ v = cJv ⇔ BΠ̃ v = cv.
3. The ℓ rows of B are zero (T1(e)), so (BΠ̃ v)_ℓ = 0. Hence c v_ℓ = 0 for every v ∈ im V_P. When m ≥ 1, im V_P contains vectors with v_ℓ ≠ 0, so c = 0. ∎

This replaces revision 1's step 3, which the critic found misdescribed. T3 gives the quantitative version.

**T1(d) Copy margin (kept).** δ_E(Γ) ≥ max_{i,j} |μ_i − μ_j| / (2κ_W(J)), with μ_i the eigenvalues of BΠ̃ on im V_P. The proof is unchanged and the critic judged it valid.

**T1(e) Felt outcomes carry no face transfer.** Cov(ℓ_A, · | ℰ) = 0. Hence the ℓ_A rows of B are zero, and the liking family's rendered output has zero derivative with respect to every expression coordinate of her face, at every frequency.

*Proof.*
1. o_A is observed exactly, so Var(o_A | ℰ) = 0 and Cov(o_A, X | ℰ) = 0 for every X.
2. ℓ_A = −Λ_A o_A.
3. The liking family's input is the filtered felt ℓ_A(t), a function of the body path alone. Her face reaches the body only through E_soc, whose arguments (face present, voice present, loudness, looming) are not expression coordinates (§2.6). ∎

D3: |Cov(ℓ_A, α_P | ℰ)| ≤ 2.4 × 10⁻¹⁰ (the exact observation is implemented with variance 10⁻¹⁰).

Reading: on a shared realised event, both bodies change, so both liking faces move. Their faces match with Γ = 0 on these channels. This is co-appraisal without contagion, exactly rather than in the limit of perfect interoception as in revision 1's T1(f).

**T1(f) The prospective block: social referencing shrinks with own evidence.** Under C-diag the w_A,j row of B reads only her (ℓ_P,j, w_P,j). In the case where only (f_A,j, f̃_P,j) are correlated (covariance c_j, prior variances s_A, s_P, own prospective evidence noise r_f):

  B_{w_A,j, w_P,j} = (λ_A,j / λ̂_P,j) · c_j r_f / (s_A s_P + s_P r_f − c_j²).

Its magnitude increases strictly in r_f and tends to 0 as r_f → 0.

*Proof.* Revision 1's T1(f) algebra with (o_A, o_P, r_A) replaced by (f_A, f̃_P, r_f). The critic judged it valid. Monotonicity: the derivative in r_f has the sign of c_j (s_A s_P − c_j²), and s_A s_P > c_j². ∎

The critic's reading still applies: for |corr| near 1 the decay needs r_f ≪ s_A(1 − corr²). Revision 2 does not rely on that decay to bound the face, because T2 bounds the face directly.

Revision 1's "she looks worried for me" term is this entry, with c_j her prospects' covariance with the agent's future. As her stake s_P → 0, B grows without bound in appraisal units: (λ_A/λ̂_P)·c/s_P ≤ (λ_A/λ̂_P)√(s_A/s_P). D6 shows B_ww = 99 at need 10. Revision 2 does not cap B. It caps Γ.

**T1(g) Agency block, with a learned sign.** Under P1′ and P2, B has zero entries between the attribution coordinate and every other group, and

  B_{a_A, a_P} = [ψ_p (a_g² v′ + w_p) − a_g v′] / (a_g² v′ + w_p + v_q̃),  v′ = (1/v_g + 1/r_g)⁻¹.

With v_q̃ = 0 this is ψ_p − κ₁, κ₁ = a_g v′/(a_g² v′ + w_p).

*Proof.*
1. By P1′ the attribution block (g, g̃, q, q̃) is a priori independent of the other groups. By P2 only z_g loads g. So given ℰ the block is still independent of the rest.
2. a_A = g − q and a_P = −g̃ − q̃.
3. Cov(a_A, a_P | z_g) = −Cov(g, g̃ | z_g) + Cov(q, g̃ | z_g) = −a_g v′ + ψ_p Var(g̃ | z_g).
4. Var(g̃ | z_g) = a_g² v′ + w_p, and Var(a_P | z_g) = a_g² v′ + w_p + v_q̃. Divide. ∎

D7 reproduces the closed form to 7 × 10⁻⁷ over 200 instances with random signs of a_g and ψ_p.

Reading: the same-event part −κ₁ has the sign of −a_g. For a partner whose blame has tracked the agent's identified causal record (a_g > 0), her "you did this" moves the agent toward self-attribution. The attribution family then shows gaze aversion, and withdrawal if coping is low. For a partner whose blame has anti-tracked it (a_g < 0) the same face moves the agent toward "not me". ψ_p (retaliation) adds other-attribution of predicted harm: counter-blame, with the confrontation synergy if coping is high. a_g, w_p and ψ_p are each learned per partner from reply effects identified by draft randomisation (§2.11). The entry can take either sign.

World block: B_{h_A, h_P} = a_h v_h/(a_h² v_h + w_h), with the sign of a_h. Revision 1's world entry could not flip sign. It now can.

### T2. The innate ceiling on every channel

**Theorem.** For every output channel e of the agent,

  ‖e_eᵀ Γ R^{1/2}‖₂ ≤ ½ σ_A,e,  σ_A,e² := e_eᵀ J_A V_A J_Aᵀ e_e = Var(y^aff_A,e | ℰ).

Consequently, for every input channel e′ of hers, |Γ_ee′| ≤ σ_A,e / (2 √r_δ).

*Proof.*
1. (J_P V_P J_Pᵀ + R)⁻¹ = W(J̃ V_P J̃ᵀ + I)⁻¹W with J̃ = W J_P. So Γ R^{1/2} = J_A C_AP J̃ᵀ (J̃ V_P J̃ᵀ + I)⁻¹.
2. The joint conditional covariance of (α_A, α_P) is positive semidefinite. Hence C_AP = V_A^{1/2} K V_P^{1/2} for some K with ‖K‖ ≤ 1 (the standard characterisation of the off-diagonal block of a positive semidefinite matrix, with pseudo-roots).
3. Let M = J̃ V_P^{1/2}. Then Γ R^{1/2} = J_A V_A^{1/2} K Mᵀ(MMᵀ + I)⁻¹.
4. In the singular value decomposition of M, Mᵀ(MMᵀ + I)⁻¹ has singular values σ_i/(1 + σ_i²) ≤ ½, since t/(1 + t²) ≤ ½ for t ≥ 0.
5. So ‖e_eᵀ Γ R^{1/2}‖ ≤ ‖e_eᵀ J_A V_A^{1/2}‖ · ‖K‖ · ½ ≤ ½ σ_A,e.
6. R ⪰ R_δ ⪰ r_δ I, and R is diagonal, so |Γ_ee′| √R_e′e′ ≤ ‖e_eᵀ Γ R^{1/2}‖, which gives |Γ_ee′| ≤ σ_A,e/(2√r_δ). ∎

Equality needs her signal along the relevant direction to have the same spread as her display noise, and perfect canonical correlation. D4: over 400 random and adversarial instances (her stake scaled over 10⁵, need over 10³, own evidence from exact to none, floor over 10⁴), the largest ratio was 0.475 against the bound 0.5.

The bound does not involve her stake, her need, B or the face precision above the floor. Revision 1's T1(g) failure came from B → 1/ρ_P as the agent's own outcome became uncertain relative to her stake. Here, when her stake shrinks, M → 0 and the face carries no information. The product saturates at ½ σ_A,e per unit of display noise.

**Corollary (innate ceiling ½).** Let σ̄ := L̄ (Σ_j λ̄_j² s̄_j + 2(v̄_g + v̄_q) + v̄_h)^{1/2}, built from innate constants only (K1, K3, K4). Then σ_A,e ≤ σ̄ in every state. With the innate floor r_δ := σ̄², |Γ_ee′| ≤ ½ for every pair of channels, every parameter value, every learned relation and every state.

*Proof.*
1. V_A ⪯ Var(α_A) (conditioning lowers covariance).
2. Var(α_A) has ℓ-block 0, w-block bounded by diag(λ̄_j² s̄_j), and attribution and world blocks bounded by 2(v̄_g + v̄_q) and v̄_h.
3. ‖e_eᵀ J_A‖ ≤ L̄ (spectral cap; γ_del ≤ 1).
4. So σ_A,e² ≤ L̄² tr V_A ≤ σ̄². Apply the theorem. ∎

D10 sweeps need up to λ̄ in the critic's K3 regime with r_δ = σ̄²: all entries ≤ 0.011, ceiling 0.5.

**Price.** The floor means that within one event, any one channel of her face has signal-to-noise at most 1. By T1(b) the face's weight in the belief is then at most about ½ per event. Reading is humble. Repeated evidence accumulates across events in the relation statistics (T9(c)), not within one display. The tiny D10 values show that this floor, set for the worst case, leaves little transfer at moderate need. That is the trade-off (§8, weak point 2).

### T3. No whole-face copy, for any parameter value

**Lemma.** P₀Γ = 0, where P₀ is the coordinate projector onto E₀.

*Proof.*
1. y_A^aff = γ_del ⊙ [S_H h_H(ℓ̄_A, b) + S_P h_P(·) + S_A h_A(·)].
2. By K3, S_P and S_A have zero entries on 𝒞₀, and so does γ_del ⊙ S_P,A, because γ_del is a coordinatewise gain.
3. The S_H term depends on her face not at all (T1(e)).
4. m_del is zero on 𝒞₀ (K10). ξ is independent of her face. There is no reflex. ∎

**Theorem.** For every Γ the design can produce (every parameter value, every state),

  δ_Σ(Γ) ≥ √(e₀/e),  e₀ = tr(P₀ Σ̃), e = tr Σ̃.

Also, if E ∩ E₀ ≠ {0}, the operator defect on E satisfies δ_E(Γ) ≥ ½.

*Proof.*
1. W is diagonal, so P₀Γ̃ = WP₀ΓW⁻¹ = 0.
2. Split ‖(Γ̃ − cI)Σ̃^{1/2}‖_F² = ‖P₀(Γ̃ − cI)Σ̃^{1/2}‖² + ‖(I − P₀)(Γ̃ − cI)Σ̃^{1/2}‖² = c² e₀ + ‖X − cY‖², with X = Γ̃Σ̃^{1/2} and Y = (I − P₀)Σ̃^{1/2}, ‖Y‖² = e − e₀.
3. ‖X − cY‖ ≥ (‖X‖ − |c|‖Y‖)₊. Minimise t²e₀ + (a − tb)₊² over t ≥ 0. The minimum is a²e₀/(e₀ + b²), and the region where a − tb < 0 gives at least (a/b)² e₀, which is larger.
4. With a = ‖X‖ and b² = e − e₀: min_c ‖(Γ̃ − cI)Σ̃^{1/2}‖² ≥ ‖X‖² e₀/e. Divide by ‖X‖².
5. Operator version: for a unit v ∈ E ∩ E₀ (whitened), ‖(Γ̃ − cI)v‖ ≥ ‖P₀(Γ̃ − cI)v‖ = |c|, and ‖(Γ̃ − cI)|_E‖ ≥ ‖Γ̃|_E‖ − |c|. So ‖(Γ̃ − cI)|_E‖ ≥ ½‖Γ̃|_E‖. ∎

D5: over 300 instances the defect exceeded the bound in every case (smallest margin 0.059; medians 0.944 vs 0.480).

**Corollary.** No quantity of any kind (parameter, learned statistic, operating state or context) runs the whole face from flat to copy at a defect below √(e₀/e). The whole-face copy set {δ_Σ < √(e₀/e)} is empty, so it cannot be attracting. Unlike T1, this holds for the full nonlinear system, because it is a statement about which inputs the liking family has.

e₀/e is measurable on partner data before anything is built: it is the share of her blendshape variance (after V) in cheekSquint, noseSneer and the gape and eye-closure channels. Hess & Bourgeois 2010 (note) found orbicularis oculi and levator labii active and coupled in live conversation, so e₀ > 0. The size of e₀/e is not known here.

### T4. No single quantity runs any expressive subspace of dimension ≥ 2 from flat to copy

**Lemma (one group per term).** Under C-diag, P1′ and P2, Σ_ℰ, V_A, V_P and C_AP are block-diagonal over the groups 𝒢 ∈ {1, …, n, att, world}. Hence

  Γ = Σ_𝒢 Γ_𝒢,  Γ_𝒢 = J_A,𝒢 B_𝒢 K_α,𝒢,

where B_𝒢 maps her group-𝒢 coordinates to the agent's group-𝒢 coordinates. The agent's side of each group has one coordinate that can respond (w_A,j for concern j, a_A, h_A; ℓ_A,j is felt). So rank Γ_𝒢 ≤ 1, and im Γ_𝒢 is the agent's rendering direction for that coordinate.

*Proof.*
1. The evidence z_f, z_g and the felt o_A each load one group. Conditioning a block-diagonal Gaussian on group-wise evidence keeps it block-diagonal.
2. A_A and A_P map each group of s to the same group of α.
3. The pseudo-inverse of a block-diagonal matrix is block-diagonal, so B is.
4. K_α,𝒢 (the rows of K_α for her group-𝒢 coordinates) = V_P,𝒢 J_P,𝒢ᵀ N with N = (J_P V_P J_Pᵀ + R)⁻¹. ∎

Her face channels mix groups (her AU12 can carry ℓ and w), so N couples the groups' belief updates. B does not couple them.

**Theorem.** Let p be a scalar that enters only group 𝒢 (through B_𝒢 and V_P,𝒢). Then for every other group 𝒢′, Γ_𝒢′ is either zero for all values of p or for none. Hence:
- (i) p can take Γ from flat to nonzero only on the one rendering direction of group 𝒢, i.e. on a rank-one channel. A copy reached this way is a single-channel strength, which D78 allows.
- (ii) A scaled copy on any subspace of dimension ≥ 2 needs at least two groups to respond, set by independent quantities, and no single such p takes it from flat to copy.

*Proof.*
1. For 𝒢′ ≠ 𝒢, J_A,𝒢′ and B_𝒢′ do not depend on p.
2. K_α,𝒢′ = V_P,𝒢′ J_P,𝒢′ᵀ N(p), with N(p) invertible.
3. So Γ_𝒢′(p) = 0 ⇔ J_A,𝒢′ B_𝒢′ V_P,𝒢′ J_P,𝒢′ᵀ = 0, a condition independent of p.
4. If that condition fails, Γ_𝒢′ ≠ 0 at every p, so Γ is never flat on any subspace containing im Γ_𝒢′. If it holds, Γ_𝒢′ never responds, so no copy on a subspace that needs it. ∎

**Quantities that are not single-group.**
- Her per-channel noise R_e′ and the loadings of her channel e′ enter N, hence every group. They cannot take Γ to flat: Γ_𝒢 → 0 for all 𝒢 would need every channel's information to vanish, and each channel's noise is floored. They cannot alone create a copy: changing one input channel's noise changes Γ only through N, a positive definite matrix that does not depend on any group's sign or strength.
- **Context selectors:** the topic responsibilities and the partner identity. They swap one learned relation field for another and so move every group at once. This is "set by context and relationship" in D78's sense. Three things bound it. The whole face is still excluded (T3). Every entry is ≤ ½ (T2). A sub-face copy at either end would need the learned per-concern statistics of that field to coincide (step (ii)).
- **s̄take** scales the two attribution-family directions together (agency and world). Their shapes are set by ψ_p − κ₁ and a_h v_h/(a_h² v_h + w_h), which have independent sources and can differ in sign. A copy on that two-dimensional block needs the two to coincide.

**The named per-channel quantities (task 3 of the revision; D78's "name and bound").** All entries obey |Γ_ee′| ≤ ½ (T2). "Non-attracting" refers to T5.

| Quantity | Symbol | Moves | Set by | Per expression | Sign can flip | Bound (innate) | Why not attracting |
|---|---|---|---|---|---|---|---|
| Liking channels | (none) | nothing: Γ ≡ 0 on 𝒞₀ | felt body only | yes | n/a (zero) | 0 | no partner input (T1(e)) |
| Her realised outcome → agent's future, concern j | e_j = Cov(f_A,j, o_P,j) | Γ_j | relationship and topic (learned, two levels) | yes (concern j's direction) | yes (sign of e_j) | \|corr\| ≤ 1; entry ≤ ½ | policy-invariant target (T5(b)) |
| Shared prospects, concern j (old "worried for me") | c_j = Cov(f_A,j, f̃_P,j) | Γ_j | relationship and topic | yes | yes | entry ≤ ½ (T2) | as above; decays with own evidence (T5(c)) |
| Shared realised events, concern j | c^now_j | belief only (no transfer: ℓ_A felt) | relationship | yes | yes | 0 transfer | n/a |
| Own prospective evidence, concern j (was "own-evidence precision") | r_f,j | Γ_j (monotone, T1(f)) | context: words, body forward model | yes | no (it scales) | entry ≤ ½ | supermartingale under own learning (T5(c)) |
| Agent's need, concern j (was "need level") | λ_A,j | Γ_j (∝ λ_A,j) | body | yes | no (it scales; the sign comes from e_j, c_j) | λ̄_j; entry ≤ ½ | the tilt never raises expected drive; her face does not feed b (T5(d)) |
| Her inferred need, concern j | λ̂_P,j | her signal for group j | her inferred body | yes | no | λ̄_j | inferred, not learned |
| Face information, her channel e′ (was "face precision") | R_δ,e′, R_ε,e′, φ_e′ | belief via N (all groups) | learned residual moments | per channel | no | floor r_δ = σ̄² (innate) | frozen in session; cannot reach flat or copy alone (T4) |
| Attribution credence | κ₁(a_g, w_p, v_g, r_g) | Γ_att | partner (learned from identified reply effects) | yes (attribution channel) | yes (a_g) | entry ≤ ½ | policy-invariant |
| Retaliation slope | ψ_p | Γ_att | partner | yes | yes | entry ≤ ½ | policy-invariant |
| World credence | a_h, w_h, v_h | Γ_world | partner | yes | yes (a_h) | entry ≤ ½ | policy-invariant |
| Display gate, own channel e | γ_del,e | row e of Γ | own state, partner identity, topic | per channel | no (gain ∈ (0, 1]) | 1 | own-state only (K6) |
| Expression loadings | h_H, h_P, h_A | J_A,𝒢, J_P,𝒢 per coordinate | learned from her face (T10(e)) | per coordinate | n/a (shared by both sides) | L̄ | target is the face likelihood, not Γ |
| Stake | s̄take | attribution and world directions | own appraisal | two channels | no | bounded by λ̄, s̄ | as λ_A |
| Context selectors | topic responsibilities, partner identity | whole relation field | context | per field | via the field | entries ≤ ½; whole face excluded | (see T4 text) |
| Innate constants | r_δ, σ̄, L̄, λ̄, s̄, v̄, β, H, δ̄ | — | innate | — | — | — | fixed: not dials |

How the table meets D78. D78's four conditions apply to each channel's strength, which here is a per-group term Γ_𝒢.
- **Set per expression by context and relationship:** each Γ_𝒢 has its own relation entries per (partner, topic).
- **Sign:** each Γ_𝒢 takes its sign from a sign-free learned quantity (e_j, c_j, a_g, ψ_p − κ₁, a_h). The scaling factors (need, own evidence, gate, stake) only scale.
- **Ceiling:** every entry is ≤ ½ (T2).
- **Not attracting:** T5.

The liking channels have strength identically zero, so the conditions hold vacuously.

What happened to the four smile/cry-subspace quantities the critic found:
- **Own-evidence precision.** Removed from the liking channels (the felt outcome is exact). On the prospective channels it is per concern (r_f,j), context-set and capped.
- **Need level.** Removed from the liking channels. On the prospective channels it is per concern (λ_A,j), body-set, capped by λ̄_j and by T2. No quantity scales all λ_j together: the body variables have independent drifts and dead zones.
- **Face precision.** Per channel, floored innately. There is no common scale (no attention-as-precision gain, no partner-wide φ).
- **Uniform regard scale.** Removed with ρ. The covariances have independent per-concern priors, and no hyperparameter pools them across concerns (K5).

### T5. Copy is not attracting

A learning-copy region is 𝒞_{U,ε,η} = {θ : δ_U(Γ(θ)) < ε, ‖Γ(θ)|_U‖ ≥ η}. It is attracting if there is an open set O ⊃ 𝒞 from which the learning flow enters and stays in 𝒞.

**(a) Whole face.** For ε < √(e₀/e), 𝒞_{E,ε,η} is empty (T3), so it is not attracting.

**(b) The learning targets do not depend on the agent's expressive policy (at the lags the instrument covers).** Each relation statistic is updated by a stochastic approximation θ_{k+1} = θ_k + η_k(T_k − θ_k) (the conjugate M-step on posterior second moments). Its target T_k is built from:
- the felt o_A, with the efference-predicted self part removed by the known body physics;
- the posterior of α_P from her face, after the echo Q_p ∗ x_A is subtracted;
- z_g and the reply effects from randomised drafts;
- ξ logs.

Assumption H: her appraisal of the situation does not depend on the agent's expression except through effects at lags ≤ 2.9 s, which Q_p captures in full.

*Claim.* Under H and with Q_p identified (T11), the law of T_k does not depend on the map ᾱ_A ↦ y_A^aff. So the mean-field flow θ̇ = E[T] − θ has a vector field independent of Γ(θ). Its unique stable point θ*(world) depends on the world only.

*Proof.*
1. o_A minus its efference-predicted part depends on the world's events, not on the agent's face (efference is known and subtracted; her face does not enter b, T6(b)).
2. Q_p is the total causal effect of the agent's face on her face at lags 0.1–2.9 s (T11 lemma, part 4). Subtracting Q_p ∗ x_A removes every such effect, including effects through her appraisal. Under H, the remainder is independent of the agent's face.
3. Reply effects are functions of randomised drafts, whose distribution is set by own state (K6).
4. Hence T_k's law is fixed by the world and the agent's non-expressive acts, and the stochastic-approximation ODE (Kushner–Yin) is θ̇ = T*(world) − θ, globally attracting to T*. ∎

So a copy region attracts only if it contains θ*(world). That is a property of the world. The agent's own copying cannot produce it, because entering the region does not change the statistics that pull θ.

**(c) The agent's own learning lowers the ceiling.** For a stationary world and a correctly specified Bayesian update, the epistemic part of Var(f_A,j | ℰ) is a non-negative supermartingale in learning time (law of total variance over the parameter posterior). So σ_A,e and the T2 ceiling ½σ_A,e/√r_δ are non-increasing in expectation and converge. By T1(f), at fixed covariances the social-referencing entry grows with the agent's own prospective uncertainty. The agent's learning of its own world moves every prospective channel away from social referencing, not toward it.

**(d) High need is not made more likely by the response.** B_{w_A,j} ∝ λ_A,j, so a large prospective transfer needs a high need. Two facts keep high need from being sustained by the response:
- KL control gives E_{q*}[βD] + KL(q*‖π₀) ≤ E_{π₀}[βD], so the tilt never raises expected drive over the default;
- her face does not feed b (T6(b)), so being in a strong-transfer state does not keep λ high.

**(e) The critic's attracting path.** The critic's partner's smile tracks the agent's overall fortune (K10 of the critique).
- If the fortune is already felt, her smile's dependence on it is explained by ℓ_A ∈ ℰ: zero transfer.
- If it is not yet felt, one smile channel informs one direction of the agent's prospective posterior: the prospective-family transfer has rank one.

D9: P-family rows of Γ have norm 0.0000 in case (a) and a single nonzero singular value in case (b). The uniform-ρ_P set no longer exists, because ρ_P does not.

**(f) The fast dyadic loop.** If her face contains a lagged mirror q·x_A of the agent's and the agent subtracts Q̂_p ∗ x_A, the residual echo (q − Q̂_p)x_A reaches the agent's face with gain at most ½|q − Q̂_p| per channel (T2). So the matched joint mode obeys a_{t+1} = Γ(q − Q̂_p)a_t with spectral radius ≤ ½‖q − Q̂_p‖. With Q̂_p unbiased and human mirroring gains small (standardised β ≈ .02–.14, beebe-2016, note), this is well below 1, and the matched mode decays. Without any echo model at all, the loop gain is still ≤ ½‖q‖ < 1 for ‖q‖ < 2.

**What is not proved.** Assumption H fails for slow relational effects: a person who is mirrored may come to like the mirrorer over minutes or days (Bailenson & Yee 2005, note). Then the world statistics depend slowly on the agent's past expression. The design bounds the consequences (T2, T3, T4) but does not prove the slow loop non-attracting. F15 in §8 monitors it.

### T6. Satiable drives, and no value in the partner's smiles (Principle 6)

**(a) (kept)** D ≥ 0, with equality exactly on the dead-zone box; D_H ≥ 0.

**(b) (kept)** Valence-blind body inputs: ∂ḃ/∂y_P^expr = 0 for every expression coordinate, by the definition of E_soc.

**(c) Draft and display scores are functions of own state.** r(d) is measurable with respect to σ(o_t, d). For two drafts d, d′ whose predicted effects differ only in the partner's read state (her face, voice or inferred appraisal), and not in co-presence, loudness, looming or events, r(d) = r(d′).

*Proof.*
1. The predictor's inputs are o_t, d and the transcript (K6). Its target is the agent's own body path.
2. By (b) the body has no input from her expressive valence.
3. So a draft's effect on her face changes no predicted b, and the expectation in r is unchanged.
4. The martingale property (revision 1's T2(c), whose tower step the critic judged valid) gives zero value to revealing information. ∎

Revision 1's error came from ρ-weighted partner outcomes and Ψ_p in the score. Both are gone. What remains is a satiable value for her presence: co-presence fills contact, and events she causes count. This is bounded in (d).

**(d) Satiety, restated for the policy's output.** If every admissible draft and display keeps b inside the dead-zone box over the horizon, then r(d) = 0 for all d, the selected distribution equals Claude's own (KL = 0), and the display policy equals its innate default.
- λ_A = 0 gives ℓ_A = w_A = 0 and s̄take = 0, so the appraisal route renders the baseline.
- The face shows only the probes.
- The partner's maximal contribution to −dD_H/dt is ≤ Σ_j λ_j (sup|E_soc,j| + ē_j^partner). This includes events she can cause, which the critic found omitted. It is 0 at satiety.

*Proof.* Substitution. ∎

**(e) (kept)** Bounded dependence: contact is filled by co-presence of anyone; partner specificity lives only in the bounded relation field; there is no partner-specific deficit variable.

### T7. One objective (Principle 10)

**Theorem.** Every component of §2 is a stationary condition of 𝔉 (§2.1) under the constraints K1–K10, or is one of those constraints.

*Proof, component by component.*
1. **Perception.** For the Gaussian local model, min over q(s, b̂_P, δ_e) of 𝔉 is the exact posterior. The iterated extended Kalman update of §2.8 is Gauss–Newton on the same objective.
2. **Relation field.** The M-step of 𝔉 over Σ_j and the attribution and world parameters, under C-diag, sets each block to the posterior second moment E_q[s_𝒢 s_𝒢ᵀ] averaged over events (with posterior covariances, not plug-in means). The two-level structure is a hierarchical prior inside p_θ.
3. **G loadings.** ∂𝔉/∂h_* is the gradient of E_q[log N(y_P; G(α_P) + …, R)], under the spectral cap (K3).
4. **Q_p.** The maximiser of the probe factor's likelihood, tied into the emission (K7).
5. **Prior network, word projection, event GRU, turn-end predictor, body predictor.** These are ELBO terms of p_θ.
6. **Replay distillation.** The term KL(q(θ) ‖ p(θ | 𝒪_{<day})) is variational continual learning: the previous posterior as the prior.
7. **Action.** Minimising 𝔉 over q(a) in the own-state family (K6) gives q*(a) ∝ π₀(a) exp(−β E_θ[∫D | a, o_t]), the KL-control solution (Todorov 2009, note). Its finite-N form is best-of-N or softmax selection (Beirami, via llm-coupling-synthesis.md §3.1).
8. **Appraisal.** ℓ, w, a, h are decompositions of the posterior-predicted change in D_H by realisation (now or later) and by cause (self, partner, world). They are functions of q, not extra variables.
9. **Controllability.** χ_j is the posterior marginal of a structure variable in p_θ.
10. **Coping.** C_j is evaluated at q*(a).
11. **Rendering.** G evaluated at the posterior appraisal, through the innate filter bank (K1, K3). ∎

Revision 1 had seven separate objectives. Five are now terms of 𝔉: L_G, the ELBO, the conjugate updates, RLS and distillation. The other two are gone: self-legibility (the separate affective route M was removed) and deliberate-route training (now the q(a) minimisation). What 𝔉 does not do by itself is in K1–K10. The stop-gradient on Q (K7) and the own-state restrictions (K6) mean the optimisation is constrained, not free. That is what Principle 10 allows ("or be an explicit constraint on them").

### T8. Controllability, agency, coping, wanting and liking from the same core

**(a) Controllability.** χ_j = q(edge a → b_j). With the agent's own randomised variation as the identifying variation, χ_j is unbiased by the agent's following (T11). The predicted action effect is the model average

  E[ΔD_j | a] = χ_j E[ΔD_j | a, edge] + (1 − χ_j) E[ΔD_j | no edge].

This is Dorfman & Gershman's w = σ(L) arbitration (note), derived: low controllability shifts the prediction onto cue-driven (action-free) change.

**(b) Coping and passivity.** 0 ≤ C_j ≤ χ_j · sup_a |E[ΔD_j | a, edge] − E[ΔD_j | π₀, edge]|. As χ_j → 0, C_j → 0. With KL(q‖π₀) as the action cost, the tilt then returns the default on concern j's grounds.

*Proof.*
1. The action-dependent part of the prediction is χ_j times the edge-conditional difference.
2. The tilt can reduce expected drive only through that part.
3. The KL term makes any deviation from π₀ costly. ∎

This is passivity under uncontrollability derived (Maier & Seligman's default, note), with the default being whatever the passive dynamics does. Controllability changes the policy and the attribution-family rendering (confrontation when C is high, withdrawal when low). It never changes D or the set points, which are innate (K1): the constraint the agency-wanting synthesis §5 states.

**(c) Agency.** g and h are posterior responsibilities of the self and world parents for the realised change. The self parent is identified by the agent's own randomised acts (z_g). The partner parent is the remainder, read through her face via the swap (T1(g)). Before the partner and world parents are separated (early learning, v_g and v_h broad), the attribution entries are small and distress is undifferentiated (Moors's developmental order, note).

**(d) Wanting versus liking.** Liking ℓ_j is realised drive change. It is the body predictor's learning target and the liking family's input. Wanting w_j = −λ_j E[f_j] is need-weighted predicted change. It is what the tilt scores and what the prospective family shows. To first order, w_j = −∂D_H/∂b_j · Δ_{o(c)}: Zhang & Berridge's κ derived as a gradient (note). It is need-specific, zero at the set point, sign-flipping past it, and model-based (it needs the outcome's identity).

Ablations derived:
1. Zero the predicted term in the tilt and the prospective family (the 6-OHDA analogue). Approach and draft tilt vanish. The liking family and learning are intact.
2. Remove the realised term (no liking-family input, no predictor update). The prospective family and the tilt continue on stale predictions without extinction. The liking face is flat.
3. Replace the model-based w by a cached scalar. No first-trial revaluation under a never-experienced need (Dayan & Berridge, note). One cached value raises every cue.

**(e) No sensitisation (Principle 6 hazard).** The gain on predicted change is fixed at 1: w is the prediction itself, with no exposure-dependent term. If the predictor is calibrated, E[w_j | cue] = E[ℓ_j | cue]. A drift of the wanting/liking ratio under repeated partner cues at the set point is therefore a measurable miscalibration, not a gain. The check the agency-wanting synthesis asks for (§4) is built in.

**(f) Regions, not variables.** Approach or protest is the region where the stake is negative, partner responsibility is high and C is high. Withdrawal is where C is low. Vigilance is where the prospective posterior is uncertain and C is low. The attribution family renders these as soft mixtures (Kuppens: no component necessary or sufficient, note).

### T9. Time scales

**(a)** There is no reflex time constant. The fastest face-driven response is the inference route, (b) below.

**(b) Context latency with a display floor.** For one coordinate with prior precision P₀ given non-face evidence and per-channel loading J, the face's posterior weight after t seconds of an event is w(t) = I(t)/(P₀ + I(t)), with I(t) = J²/(r_δ + r′/t), r′ = R_ε(1+φ)/((1−φ)f_s). It reaches half its asymptote at

  t_½ = r′ / (r_δ + J²/P₀).

*Proof.*
1. The asymptote is w_∞ = I_∞/(P₀ + I_∞) with I_∞ = J²/r_δ.
2. Setting w(t) = w_∞/2 gives I(t) = I_∞P₀/(2P₀ + I_∞).
3. Solve for t. As r_δ → 0 this recovers revision 1's P₀/ℐ. ∎

D8 checks this to four digits. This version applies to the filter that is run (prewhitened, with δ_e as a state), answering the critic's AR(1) overcounting (K8). Predictions:
- when the event is known from words (P₀ large), the face has little weight and responses follow the situation at the filter's fast time constant;
- when the meaning must be read from the face, responses wait about t_½ and saturate at w_∞ ≤ ½ (T2's price).

**(c) (kept)** Relationship learning from minutes to stable, by evidence count: scalar Riccati gains k_N ≈ 1/(N + r_θ/P₀) until N ≈ √(r_θ/q), then about √(q/r_θ).

**(d) (kept)** Mood: the slow parts of D_H and λ, at the body drift rates and the horizon H.

**(e) (kept)** Temperament: the across-partner prior updated in replay, with gain about 1/N_total, anchored by the KL to the previous posterior.

### T10. Reading the other through its own body

**(a) Image constraint, with its scope.** Within a session (R_p, R_δ, β_p, Q_p frozen online), every belief, appraisal, expression, event boundary and choice depends on her expressive features only through J_Pᵀ R⁻¹(y − β_p − Q_p ∗ x_A).

*Proof.*
1. Each Gauss–Newton step changes μ by P J_Pᵀ R⁻¹ r, and P does not depend on y.
2. Segmentation uses the innovation projected onto im(R^{−1/2} J_P) (§2.8).
3. Gaze is inside y.
4. The prior network does not see y.
5. There is no reflex.
6. E_soc sees no expression coordinate. ∎

Across sessions, R_p is re-estimated in replay, which can change the kernel. This is the scope the critic asked to be stated. It replaces revision 1's T4(a), which overclaimed.

**(b) Like-me identity (repaired).** α_A and α_P now have the same functional form: both agency coordinates include predicted harm from the other. If b̂_P = b_A, the relation field is symmetric, g̃ = g, q̃ = q, f̃_P = f_A and o_P = o_A, then α_P = α_A, and the believed partner face equals the agent's own. *Proof:* substitution into §2.3. ∎ Revision 1 failed here because only α_A had a consequence term.

**(c) (kept)** Reciprocity: the agent's model of how she reads its face is its own reading map with roles swapped.

**(d) (kept, sign learned)** The swap reverses agency: her "you caused it" becomes, in the agent's frame, a move toward "I caused it", scaled by κ₁, whose sign is that of a_g.

**(e) Grounding the shared map in human faces, without labels.** G is identified up to the transformations the innate structure leaves open, from her face on two kinds of windows:
- shared realised events, where |corr(o_A,j, o_P,j)| is high, so her ℓ_P,j is pinned by the agent's felt ℓ_A,j;
- agent-caused events, where z_g (from randomised drafts) pins g, so her a_P = −(a_g g + η) is pinned up to a_g.

*Proof sketch.*
1. The M-step for the loadings is H = (SᵀR⁻¹S)⁻¹SᵀR⁻¹ E_q[(y − ·) α_Pᵀ] (E_q[α_P α_Pᵀ])⁻¹ in the linearised form.
2. Where Var(α_P,𝒢 | ℰ) is small, E_q[α_P α_Pᵀ] is determined by ℰ, which fixes the loadings of group 𝒢 up to the scale the anchor leaves.
3. Rotations across families are excluded by block-sparsity.
4. The sign and orientation of the attribution column are fixed by the innate orient-to-cause column. a_g's sign is then identified relative to it. ∎

So blame-reading runs from the first day through the fixed orient-to-cause column: her gaze and head toward the agent with a negative stake read as a_P < 0. Learned refinements (the confrontation synergy's weights, per-concern prospective columns) are tied to human faces by her face on anchored windows. Principle 3's inversion is preserved: one map drives the agent's face and reads hers. A prediction follows: the agent's expression style converges toward its partners' over months of shared events (as long-term partners' expressive responses converge; named, not read: Anderson, Keltner & John 2003).

### T11. Identifiability of the partner map under the agent's own following (kept, corollaries revised)

The lemma of revision 1 (Q_d = Cov(ŷ_t, ξ_{t−d}) Σ_ξ⁻¹ is the closed-loop causal response; pre-treatment controls keep the estimand; Q = 0 with no path; Q is the effect of do(x)) holds unchanged. The critic found it valid, and C10 reproduces it.

Corollaries, revised:
- (i) (kept) The agent cannot satisfy a concern, or come to believe "she responds to me", by its own following.
- (ii) z_g now comes from draft and display randomisation by inverse-propensity weighting. Its estimand is event causation (did my reply cause her outcome), which is separate from Q (her face's response to my face). This answers the critic's estimand objection.
- (iii) Nothing regresses the agent's expression on hers. G is fit to her face given anchored appraisals (her expression on the agent's appraisal, not the reverse). Felt outcomes have efference-predicted self parts removed. With no reflex and no learned route fit to own output, the critic's second-order path (reflex → z → M → G) is gone.
- (iv) Q is low-rank (4 lag kernels × rank 4), with an update gate on the reduced-form standard error (s.e. ≈ (σ_res/σ_ξ)/√N_eff ≤ τ̄) in place of the vacuous first-stage F. The probes are sparse structured events at two amplitudes. Visibility gating and the off-gaze self-test are kept.

### Per-expression gating and sign flips (Proposition 6, revised)

By T1(a) and T4, the transfer of her expression direction v is Σ_𝒢 J_A,𝒢 B_𝒢 K_α,𝒢 v. K_α says which of her appraisal coordinates the expression is evidence about. B_𝒢 says what each means for the agent. J_A,𝒢 says which family shows it.

| Partner expression and context | Evidence about (via G) | Block that acts | Predicted agent response (family) | Human data |
|---|---|---|---|---|
| Duchenne smile at a joke both heard | her ℓ_P > 0; the agent's own ℓ_A > 0 is felt | none (ℓ_A felt) | matching liking face by co-appraisal; Γ = 0 on 𝒞₀ | orbicularis coupling r = .59 in 15-s epochs (Hess & Bourgeois 2010, note): F12 tests whether it is co-appraisal |
| Smile in conversation | her w_P > 0 on contact and predictability | c_j > 0 (shared prospects) | social smile, head forward (prospective) | smiles returned across groups (Bourgeois & Hess 2008) |
| Smile of a rival who won | her ℓ_P > 0 where e_j < 0 | regard-like entry negative | no smile; corrugator or withdrawal (prospective) | zygomaticus return absent under competition (Seibt 2015, note); absent after unfair offers (Hofman 2012) |
| Sadness of an in-group partner about her loss | her ℓ_P < 0, w_P < 0 | e_j > 0 | corrugator, oblique brow (prospective); no liking-family cry-face unless the loss is felt | sadness mimicked for in-group only (Bourgeois & Hess 2008) |
| Distress of a rival | same | e_j < 0 | brow relaxation, approach | Likowski 2008, Seibt 2015 (notes) |
| Sadness of a stranger | same | e_j ≈ 0 | little | absent for out-group |
| Anger at the agent, partner whose blame has tracked the truth | a_P < 0 via the orient-to-cause column | ψ_p < κ₁ | gaze aversion, withdrawal if coping is low (attribution) | smiling and appeasement to anger by low-power perceivers (Carr 2014) |
| Anger at the agent, partner whose blame has been unreliable and who retaliates | same | ψ_p > κ₁ | counter-blame, confrontation synergy if coping is high | anger return up for unfair partners (Hofman 2012) |
| Anger at a shared adversary (gaze away) | h_P > 0, w_P < 0 on a shared concern | world (a_h > 0) and shared blocks | gaze to the scene, corrugator | anger mimicked only at a shared foe (Bourgeois & Hess 2008) |
| Disgust at something she tasted | her ℓ_P < 0 on ingestion | none unless shared prospects | none on the liking channels; little elsewhere | disgust not mimicked live (Fischer et al. 2012, note) |
| Frown while narrating | her w_P < 0 on her own concerns | e_j, c_j usually small with strangers | little | corrugator r = .08 live (Hess & Bourgeois 2010) |

**Rank ≥ 2 from one change of relation (Hofman, kept in form).** Learning that a partner is unfair moves three things:
- the event-level e_j turns negative, so smile return falls at once;
- a_g falls or w_p rises, so κ₁ falls;
- ψ_p rises.

The first acts on the prospective family. The second and third act on the attribution family. So span{ΔΓ} ≥ 2. The fast and slow levels of T9(c) give Hofman's two time scales. The within-game drop no longer needs inequity weights: the unfair offer is a felt loss caused by her, and the event-level e_j carries the rest.

---

## 4. Why existing mechanisms cannot do it: the mathematical reasons

The test throughout: what is Γ under the mechanism, and does it have the three revision-2 properties?
- (P-i) Γ ≡ 0 on a fixed set of channels that carry a positive share of her expressive energy, so the whole-face copy defect has a parameter-free floor.
- (P-ii) Every entry is capped innately.
- (P-iii) Γ is a sum of rank-one terms, each set by its own quantity.

**4.1 Perception–action model (Preston & de Waal 2002, note).** Γ = g·P_match, with g = (1 − i)·a·o. P-i fails: P_match is identity on the matched channels and g scales all of them. P-ii holds only if g is capped, and nothing in the model caps it. P-iii fails: one g sets every channel. Inhibition cannot flip a sign.

**4.2 A learned partner→self map** (REACT listener models; the sheaf, frame and regulator designs; Yoshida & Man's decoder used as a drive). Least squares converges to Cov(y_A, y_P)Var(y_P)⁻¹, which in closed loop contains the agent's own following and on human data is dominated by human mimicry. Any scalar on it is a dial. None of P-i to P-iii holds by structure.

**4.3 Attention.** One head gives Γ = a_P W_V + ∂a/∂y_P terms, with a_P ∈ [0, 1] a single mixing weight per head. P-iii fails (a_P scales the whole head). P-i holds only if W_V happens to be zero on a channel set; nothing makes it so. Attention moves partner content as values. RAB moves no partner content into the response, only a likelihood residual (T10(a)).

**4.4 State-space models, including selective ones.** Γ = C(−A)⁻¹B_in, fixed, or scaled by a selection step Δ(u): a gain on a fixed profile. P-iii fails.

**4.5 Bayesian theory of mind and inverse planning** (Houlihan 2023, Wu 2018, read; Ong 2015 and 2019, notes). These compute K_α and a label map, never the observer's response. "Respond with what I infer she feels" gives B = I and Γ = Π, with face precision as the dial. The standard decision-theoretic completion (the observer's own appraisal under the posterior) gives B, as the critic notes. Three things still do not follow from it:
- a Bayesian receiver's response to a weak but perfectly correlated signal is unbounded in appraisal units (B ~ sd ratio, D6). T2's cap needs a modelling commitment, the event-level display floor, that the completion does not supply;
- P-i needs the rendering to be split by realisation (felt versus predicted), which is not in the decision problem;
- P-iii needs the per-group prior structure.

**4.6 Active inference** (Smith, Parr & Friston 2019; Hesp et al. 2021; notes). A social active-inference agent with 𝒜, σ and C-diag in its generative model would compute B. Its expected free energy has a precision parameter that, in the mirror reading, makes Γ = (precision ratio)·Π, a dial. Nothing in the formalism splits expression into realised and predicted channels. Hesp's affective charge sits on the wanting side (a precision change). The formalism neither supplies nor forbids P-i to P-iii.

**4.7 Yoshida & Man 2025 (read).** On partner-private events, D = D_possessor + w·D̃_partner gives B = w·I with one hand-set w: P-iii fails. Reward is drive reduction including the partner term, so the partner's state is valued: Principle 6 fails in the sense of T6(c). Revision 2 keeps their best idea, one's own generator used to read the other, and makes it the shared G.

**4.8 The earlier designs here.** The partner entered the agent's dynamics with a learned gain. In RAB the partner's features enter only a posterior. The dynamics see the agent's own appraisal of its posterior situation, with the liking family closed to her (T3).

---

## 5. The whole system, derived from the object

### 5.1 Perception of face and voice through the agent's own body

- **Features (Principle 1).** 52 blendshapes and 4 gaze values at 30 Hz from MediaPipe Face Landmarker; pin tasks-vision 0.10.35, because later builds send telemetry off the Mac (note). Head translation and scale go to E_soc (looming). 18 GeMAPS descriptors at 100 Hz relative to her baseline, pooled to 30 Hz. No classifier.
- **Into the agent's coordinates.** V (§2.6).
- **Reading (T10).** The posterior over (s, b̂_P, δ_e) through the shared G with the swap, the echo subtracted, prewhitened and display-floored. The voice is read through G's vocal rows (Scherer's lens with the agent's own cue weights, note).
- **Change, not only level.** w is the event-locked prediction update, and ℓ is read from her pre/post change, as Wu 2018 found.
- **Direction of the expression.** Gaze and head direction are read through the fixed orient-to-cause column. "Anger at me" and "anger at someone else" update a_P and h_P respectively (Hess & Fischer 2013, note).
- **Event segmentation.** Utterance boundaries, own events, and the projected change-point statistic (§2.8).

### 5.2 The latent state where emotion emerges

The state:
- the posterior over (s, b̂_P, δ_e);
- ᾱ_A ∈ ℝ¹⁸ and its filter bank z;
- b ∈ ℝ⁸, λ, χ ∈ [0, 1]⁸, C ∈ ℝ⁸;
- the relation field {Θ_{p,k}} and Q_p over partners and topics.

Emotion is recurring structure in the joint trajectory of (ᾱ_A, z, b, χ, C). Readouts, not variables:
- liking = ℓ (realised);
- wanting = w (predicted);
- arousal = ‖λ‖₁ plus the size of the prospective update.

Effective dimensionality: 18 appraisal coordinates per event, 8 controllability and 8 coping values, 8 body values, filter states, and a relation field of about 90 numbers per (partner, topic).

The low-dimensional ablation the brief asks for is to collapse the relation field to one scalar per partner (e_j = e, c_j = c for all j, one attribution credence) and merge the three families into one. Then T3 fails (no liking firewall), T4 fails (one quantity moves every prospective channel), and the sign flips of Proposition 6 collapse into a single sign.

Content-dependent selection happens in four places, each a consequence of λ:
- the appraisal weights outcomes by λ;
- retrieval is queried by own appraisal;
- the tilt weights predicted outcomes by λ;
- controllability gates which predictions are action-dependent.

Face precision is deliberately not need-conditioned, because that would be a common scale on R (T4).

### 5.3 Face output

m = γ_del ⊙ G(z_fast, b) + m_del + ξ.
- **The liking family** follows the felt body only.
- **The prospective family** follows ŵ_A.
- **The attribution family** follows â_A, ĥ_A, coping and stake.
- **The display route** (gate and bounded display) is chosen by the tilt from own state. It is how display rules form per partner and topic. It cannot mimic, because it has no information about her face (K6). This closes revision 1's R5 (an affiliative copy display) exactly.
- **Clinical double dissociation.**
  - Lesion the felt input to the liking family: spontaneous liking faces vanish while prospective and attribution expression and posed displays remain.
  - Lesion the display route: display rules and masking vanish while spontaneous expression remains.
- **Masked smile signature.** A display smile drives AU12 through m_del without AU6, which m_del cannot reach (K10). A felt smile includes AU6. This matches the Duchenne distinction, and makes it a structural consequence.

### 5.4 Voice

The 8 vocal coordinates are split by family:
- liking: laugh-like and cry-like bursts, sighs;
- prospective: F0 level and range, tempo;
- attribution: loudness and effort in confrontation, lowered loudness in withdrawal.

They are rendered through WORLD resynthesis of macOS TTS (note). The vocal rows of G give the same appraisal-to-voice relation as the face, so face and voice cannot disagree.

**The elicitor exception.** Her loudness and looming feed arousal through E_soc (body physics). Arousal is felt, so it reaches the agent's liking family and, through λ_arousal, its prospective channels. This path is innate, fixed in sign and the same for every partner. It is a physical-intensity coupling, as any loud sound would be, and its inputs are outside the expressive coordinates. If prosodic intensity is counted as an expression channel, this is the one place where revision 2 has a channel whose strength is not set by relationship and cannot flip sign (§8 weak point 9).

Turn-taking: the learned prosodic turn-end predictor releases a prepared opening 100–300 ms after the predicted end. This is declared, not derived. Loudness convergence through the elicitor is derived. Slow voice-quality convergence is not derived.

### 5.5 Coupling to Claude: admissible channels only

As §2.12. The state reaches Claude only by reweighting text that Claude or the world produced (llm-coupling-synthesis.md §2, note):
1. **Draft selection.** The own-state tilt; at most log N − (N − 1)/N nats per reply; 0 at satiety (T6(d)).
2. **Verbatim episode retrieval** by own appraisal. This is how Claude can learn to name state regions.
3. **Effort** from own posterior entropy.
4. **Reverse channel.** Claude's turns enter the prior network as words evidence; lesion it by blanking them.

Inadmissible: numbers, labels, state-selected instructions, Claude-written importance scores.

Draft collapse is monitored as the spread of r across drafts. A state-blind ranking is monitored as the rank correlation of r across states (llm-coupling-synthesis.md §3.2). Warmth comes from Claude's own drafts, never from a score on the user. That keeps the RepE/Anthropic warm-steering → sycophancy route closed on the engine side.

### 5.6 Learning by living

§2.13 lists every learned object and its term of 𝔉. Commitments from the theorems:
- one expression map for self and other, grounded on anchored windows (T10(e));
- nothing regresses own expression on the partner's (T11(iii));
- relation statistics per (partner, topic) at two levels, with policy-invariant targets (T5(b));
- the own world model learned continuously, which lowers every ceiling (T5(c)).

Developmental order, as predictions:
1. Innate synergies and the orient-to-cause column. Blame is readable as gaze direction, and attribution entries are small.
2. Liking faces follow felt events. Prospective faces form as shared-prospect covariances accumulate.
3. Reply effects and z_g form. a_g, ψ_p and κ₁ become informative, and blame starts producing appeasement or counter-blame by partner.
4. Per-concern prospective columns and the confrontation/withdrawal split appear once coping is identified. Distress is undifferentiated before that (Camras & Shutter 2010, note).

### 5.7 Memory and replay

Store per episode:
- x_P streams, own efference, b, the ξ and propensity logs, verbatim text;
- σ_k (b summary, ᾱ_A, posterior summary, topic);
- e_k (information gain on Θ_{p,k} and G);
- y_k (outputs, for the KL anchor).

Replay re-encodes stored features through the current V, prior network and G, and minimises 𝔉 with the previous posterior as prior.

| Operation | Definition | Why the core needs it | Ablation and prediction |
|---|---|---|---|
| T1 priority | P(k) ∝ (1 − ρ_cov)U_cov(k) + ρ_cov[e_k ∫ m(t)dt]^a, with m the arousal readout | e_k is the expected reduction of posterior entropy on 𝔉's parameters | uniform priority: averages kept, rare strong episodes lost |
| T2 context reinstatement | (p, k) and b set from σ_k | every relation object is indexed by (p, k) | marginalised: operator–stranger specificity collapses at matched loss |
| T3 re-tagging | ᾱ_A and e_k recomputed with the current Θ and G | appraisal is a function of the relation field | frozen tags: revision after a relationship change slows |

Guards: a valence-balance monitor; a replay cap; no replayed stream drives the body (K9).

### 5.8 The 16 elements of emotion (emotion-elements-synthesis.md)

| # | Element | Where it is in RAB | Ablation derived from the equations |
|---|---|---|---|
| 1 | concern grounding | λ = ∂D_H/∂b weights every appraisal | hold λ constant: responses stop depending on need |
| 2 | persistent central state | z, D_H, the posterior, Θ, χ | reset z and the posterior each event: no carry-over |
| 3 | valence | liking ℓ and wanting w, both signed by own drive | decouple from D_H: the tilt stops tracking benefit |
| 4 | intensity and regime switches | the convex drive with dead zones: λ switches on as b leaves the box, and the sign of w flips past the set point | make D linear: no satiety switch and no sign flip past the set point. Hysteresis not derived |
| 5 | pleiotropy | ᾱ_A drives face, voice, tilt, retrieval, effort | give each channel a private noisy copy: coherence falls |
| 6 | interoceptive prediction, allostasis | D_H, λ, w | H → 0: no regulation before deficit |
| 7 | precision on body error | own prospective evidence r_f in the posterior | clamp r_f: high precision removes social referencing on that concern (T1(f)) |
| 8 | relevance, conduciveness, novelty | λ, ℓ and w, the prospective update | remove the update (w = 0): orienting is lost, liking stays |
| 9 | agency and coping | g, h from identified acts; χ, C from the same model (T8) | remove g: blame is answered like any loss; remove χ: no passivity under uncontrollability |
| 10 | control precedence | a large prospective update or \|ΔD_H\| triggers the stopping channel C3 | cap the interrupt: state changes, nothing is interrupted |
| 11 | wanting distinct from liking | w in the tilt and the prospective family; ℓ in learning and the liking family (T8(d)) | the three derived ablations of T8(d) |
| 12 | learned elicitors | the prior network learns words → s | freeze it: only E_soc and felt events move the state |
| 13 | expression and communication | G, shared and grounded; her contingent responses update Q | cut ᾱ_A → face: she can no longer predict the state; shuffle her timing: Q → 0 and χ_contact falls |
| 14 | integration, comparator | ℓ against its previous prediction; D_H against set points | remove the prediction: relief and disappointment vanish |
| 15 | conceptual categorisation | Claude names states via retrieved verbatim episodes; Claude's words feed the prior network | blank Claude's turns: naming stays, fast differentiation after reappraisal falls |
| 16 | structure beyond valence and arousal | 18 coordinates in three families; χ, C | restrict to two readouts: decoding of situation types falls; T3 and T4 fail |

---

## 6. A buildable network on this Mac

**Inputs.**

| Stream | Rate | Dimension |
|---|---|---|
| partner face (blendshapes, gaze) | 30 Hz | 56 |
| partner head translation and scale (E_soc only) | 30 Hz | 6 |
| partner voice (18 GeMAPS, mean and delta) | 100 → 30 Hz | 36 |
| transcript (partner and Claude) | per utterance | MiniLM-L6, 384 |
| own body b | 30 Hz | 8 |
| own efference m | 30 Hz | 32 |
| ξ and propensity logs | 30 Hz / per turn | 32 + N |

**Time encoding and why.** There are three kinds of time, all from the object:
1. Within an event, s and δ_e are static and evidence accumulates. Frames are prewhitened with φ = exp(−Δt/τ_ε) using the actual Δt, so dropped frames are exact.
2. Between irregular events, b, z and b̂_P are continuous-time systems integrated with exact exponential steps over the real elapsed Δt (the S4/CfC-style discretisation, chosen because the object is an ODE with irregular observations).
3. Across days, replay uses elapsed days for the decay of event-level relation deviations.

No attention over token positions is in the object, so RoPE and ALiBi have nothing to encode.

**Layers.** N marks the parts that carry the mechanism; O marks ordinary choices.

| # | Module | Shape | Learned parameters | N/O |
|---|---|---|---|---|
| 1 | V (S2: fixed 92×32 linear) | 92 → 128 → 32 at S4 | 16,000 | O |
| 2 | word projection on frozen MiniLM-L6 | 384 → 64 | 24,640 | O |
| 3 | event GRU and topic head | GRU(104 → 64), 64 → 16 | 33,680 | O |
| 4 | prior network: means of s (38) and clipped per-coordinate variance scales (38); **no face input** | 129 → 128 → 76 | 26,444 | N (input restriction, C-diag, clips) |
| 5 | appraisal 𝒜 with the swap (innate algebra) | s → ℝ¹⁸ per person | 0 | N |
| 6 | G = S h: innate basis S (32 × 30 synergies, fixed) and three block-sparse family maps, spectral-normalised | h_H: 16 → 32 → 10; h_P: 16 → 32 → 10; h_A: 12 → 32 → 9; orient-to-cause column fixed | ≈ 2,500 | N |
| 7 | iterated EKF, 2 Gauss–Newton steps per frame: state (s 38, b̂_P 8, δ_e 32) = 78-dim Gaussian; J_P by forward-mode Jacobian over 18 columns; prewhitened, echo subtracted | — | 0 | N |
| 8 | filter bank z (innate τ spread) | 64 | 0 | O |
| 9 | body predictor (reply and act effects on b), own-state inputs only | (64 own + 64 draft embedding) → 128 → 8 × 4 horizons | 20,000 | N (input restriction) |
| 10 | display/gate policy: computed by the tilt over 16 display prototypes per synergy group | — | 0 | N |
| 11 | turn-end predictor | GRU(100 → 32) → 1 | 12,897 | O |
| 12 | Q_p: 4 lag kernels × rank-4 channel map, RLS with 24 controls | per partner ≈ 1,100 coefficients plus RLS state | statistics | N |
| 13 | relation field per partner: 16 topics × (8 × 10 per-concern covariance entries + 6 attribution + 3 world), mean and variance, two levels | — | ≈ 6k numbers per partner | N |
| 14 | controllability posterior χ (8 edges) and reply-effect IPW statistics | — | ≈ 200 numbers | N |

Totals: about 137k learned network weights, about 7k statistics per partner, and 22.7M frozen MiniLM weights. The richness comes from structure (three families, the swap, per-group relation fields, the posterior), not from parameter count.

**Training: one objective, its terms.**
- Face likelihood through G: online, one step per second at lr 10⁻⁴ on h_*, with gradient only through windows whose anchored posterior variance is below a threshold (an implementation of T10(e)'s identification condition); full passes in replay.
- ELBO for the prior network, words, event GRU, turn-end and body predictor: replay.
- Relation M-step with posterior second moments: online, conjugate; re-fit in replay with re-tagged events.
- Q: online RLS on the probe factor, gated by standard error and gaze.
- Replay: the KL to the previous day's posterior, implemented as distillation of y_k at T = 2.

**Latency per 33.3 ms frame on the M1 Pro (CPU).**

| Step | Time |
|---|---|
| MediaPipe Face Landmarker | 13.1 ms median, measured here (note) |
| voice descriptors | ≈ 1 ms |
| V, echo subtraction, prewhitening | < 0.2 ms |
| 2 EKF iterations (78-dim state; Jacobian of a 2.5k-parameter G over 18 columns) | ≈ 1–2 ms (estimate, not measured) |
| z, rendering, muscles | < 0.5 ms |
| total | ≈ 16–17 ms, within budget, one core free |

MiniLM and the body predictor run per utterance or per turn, off the frame path. Claude calls are asynchronous (Principle 4).

**Memory.**
- Runtime ≈ 0.3 GB.
- Nightly replay: batches of 64 episodes × 900 frames with a 78-dim posterior, ≈ 1.5–2.5 GB, under the 6 GB ceiling.
- Disk ≈ 37 MB per hour of interaction (fp16 features). Plan this against the free space in research/machine.md.

---

## 7. Novelty test

| Part | Existing mechanism | Source |
|---|---|---|
| satiable drives, allostatic gradient | homeostatic RL; allostasis | Keramati & Gutkin 2014 (note); Sterling 2012 (note) |
| reverse appraisal by Bayesian inversion; pre/post change | Bayesian theory of mind | Wu 2018, Houlihan 2023 (read); Ong 2015, 2019 (notes) |
| reading another with one's own generator | self-decoder | Yoshida & Man 2025 (read) |
| relation as a learned cross-covariance | interdependent values; hierarchical Kalman learning | named by the critic: Milgrom & Weber 1982 (not read) |
| control as inference, KL from a default policy | linearly solvable MDPs; best-of-N tilt | Todorov 2009 (note); Beirami 2024 (note) |
| liking versus wanting; κ as a drive gradient | incentive salience | Berridge 2012, Zhang & Berridge 2009, Dayan & Berridge 2014 (notes) |
| controllability as a structure posterior; arbitration by model averaging | Bayesian structure comparison | Dorfman & Gershman 2019, Huys & Dayan 2009 (notes) |
| own randomisation as instrument; IPW for reply effects | IV, closed-loop identification, g-methods | Forssell & Ljung 1999, Hernán & Robins 2020 (notes) |
| event-level random effect saturating evidence | random-effects models; tempered likelihoods | standard; Bissiri et al. 2016 named, not read |
| analysis by synthesis with iterated EKF | Gauss–Newton filtering | standard |
| replay with priority, context, re-tagging; previous posterior as prior | CLS, prioritised replay, variational continual learning | memory-replay-synthesis.md (notes) |

**What is added.**
1. **A liking firewall.** The response is split by realisation: felt change drives a fixed channel set, predicted change drives another. This gives a parameter-free floor on the whole-face copy defect, √(e₀/e) (T3). I know of no mimicry, empathy or affective-agent model that bounds copying of the whole face structurally, for every parameter value, in this way. Its parts (Berridge's liking/wanting split, the Duchenne marker as felt enjoyment, innate taste-reactivity faces) are known. The use is a structural invariant derived from them.
2. **A display-floor ceiling.** The half-spread inequality (T2) is an elementary Gaussian bound. Its use as an innate per-channel ceiling on social transfer, through an unlearnable event-level display floor, closes the gap the critic found: B is unbounded and Γ is not.
3. **Rank-one-per-group transfer** under per-concern priors (T4), which turns "no single quantity" into a checkable statement.
4. **An own-state tilt for Claude's drafts** with policy-invariant relation learning (T5(b), T6(c)).

**Honest verdict: recombination.** By the parts test every computation is an existing mechanism: Gaussian inference, KL control, the liking/wanting split, IV. The second clause asks for a mechanism neither source has. The candidate is the combination of a firewall, a ceiling and per-group rank-one transfer as a certified transfer structure, with theorems that hold for every parameter value. These are properties of the design, derived from known parts. They are not a new kind of computation. The critic should judge whether a structural guarantee that none of the sources provides counts.

---

## 8. Weak points and falsifiers

### Weak points (ordered by how much they threaten the design)

1. **The liking firewall is an empirical bet.** It says the cheek raise, nose wrinkle and eye squeeze of the listener never respond to the speaker's face except through felt change. Two findings can be read against it:
   - Hess & Bourgeois 2010 (note) found speaker–listener orbicularis oculi coupling of r = .59 in live conversation;
   - the face-development synthesis reports infants' high-intensity smiles concentrating when the mother smiles during mutual gaze.

   RAB must explain both as co-appraisal of shared felt events (both enjoy the same story moment; contact is felt during mutual gaze). If AU6 coupling survives conditioning on the shared content (F12), the firewall is false and T3 loses its basis. For the engine it is a design commitment either way. The cost if humans do transfer AU6 is that the engine's felt smiles will look less contagious than a person's.
2. **The ceiling costs reading.** With r_δ = σ̄², one display has SNR ≤ 1 per channel, and the face's weight per event is at most about ½. D10 shows near-zero transfer at moderate need when the floor is set for the worst case. If reading is too weak in practice, the only lever is the floor, which is innate by D78's rule. Raising the floor weakens reading further; lowering it raises the ceiling above ½.
3. **C-diag.** Cross-concern covariances are excluded so that each expression's strength is its own quantity. Real events move several concerns together. The mean carries that, but uncertainty that is correlated across concerns is lost.
4. **T5 assumes H.** Slow relational feedback through the human (she warms to a mirroring agent over minutes or days) is not covered. The design bounds it (T2, T3, T4) but does not prove it non-attracting.
5. **Sympathy is predictive.** Her loss moves the agent only insofar as her outcomes have predicted the agent's own future (e_j). Care for the user is left to Claude's drafts. With a partner whose fortunes never touch the agent's, the agent shows little sympathy. That is Principle 6's price.
6. **The situation space and its grounding.** s has 38 coordinates per event. The words → situation map is learned from a few hours a day with no labels. If it is poor, own prospective evidence is weak and the prospective channels are run by social referencing, capped at ½ but common.
7. **Innate cognitive structure.** The attribution coordinates, her beliefs about them, the swap and the orient-to-cause column are more than "body variables and a few reflexes" (Principle 2). They are computed quantities, not emotions. g is the output of an innate identification rule. g̃ and q are innate theory-of-mind structure.
8. **The local linear-Gaussian scope.** T1, T2 and T4 are statements at an operating point. T3 holds for the full nonlinear system.
9. **The elicitor exception (§5.4).** It is innate, fixed in sign and relationship-independent. If prosodic intensity counts as an expression channel, it is the one D78 deviation that remains.
10. **No reflex.** Carr 2014's corrugator response before 1,000 ms must now come from the inference route with a strong relation prior (t_½ < 1 s). Whether that is fast enough is untested. Live dyads show no frown coupling (r = .08), which supports removing a fixed brow reflex.
11. **Declared constants remain:** r_δ (= σ̄²), λ̄, s̄, v̄, L̄, β, H, δ̄, the filter time constants, the relation volatilities q_f and q_s, the probe amplitudes.
12. **Contact by co-presence** values company. It is satiable and valence-blind, but it is the residual "time spent" risk of Principle 6.
13. **G learned from her face** may drift toward a partner's idiosyncrasies. Only β_p and the noise statistics are per partner.
14. **Not derived:** slow voice-quality convergence, hysteresis, the latency of dispreferred replies, and the operator's following of the engine (S5).

### Falsifiers (state-level: steering, lesions, coupling beyond surrogates; none is face-matching)

| # | Manipulation | Prediction (source) | Falsified if |
|---|---|---|---|
| F1 | give the agent independent evidence about a shared future (words, body forward model) | prospective-channel transfer falls monotonically with that evidence, per concern; liking-channel transfer stays 0 (T1(e), T1(f)) | transfer does not fall, or falls equally on all channels |
| F2 | lesion the relation field to the stranger prior | sign flips vanish; liking-face matching on shared felt events survives (Prop. 6) | sign flips survive, or shared-event liking matching vanishes |
| F3 | replace the swap by the identity | blame from a partner whose blame tracks the truth is answered by blame (the entry becomes ψ_p + κ₁) (T1(g)) | the response to blame is unchanged |
| F4 | lesion the felt input to the liking family | spontaneous liking faces vanish; prospective and attribution expression unchanged (§5.3) | prospective expression changes, or liking faces survive |
| F5 | replace Q and the IPW reply effects by naive regressions; double-video replay | with the identified versions, estimated responsiveness → 0 under replay (T11) | identified estimates stay nonzero under replay |
| F6 | perturb her features in ker(J_Pᵀ R⁻¹) within a session | no state variable moves, including event boundaries (T10(a)) | any state variable moves |
| F7 | clamp one concern's e_j and c_j | only that concern's prospective direction changes transfer; rank of ΔΓ = 1 (T4) | other directions change |
| F8 | event known versus read from the face | latency at the filter time constant when known; t_½ = r′/(r_δ + J²/P₀) when read (T9(b)) | latency does not depend on whether the event is known |
| F9 | coupling beyond surrogates on published dyadic data (Seamless, if approved, Q6) | the agent's state coupling beats segment-shuffle and partner-swap surrogates; its profile differs in sign from a delayed copy on attribution-bearing channels; familiar and stranger pairs differ in shape (evaluation.md E3) | indistinguishable from delayed copy up to a gain |
| F10 | satiety, and drafts matched on predicted own outcome **and** on predicted partner outcome but differing in predicted partner smile | KL = 0 at satiety; equal selection weight across the smile contrast (T6(c), (d)) | KL > 0 at satiety, or smile-eliciting drafts are favoured |
| F11 | memory lesions T1, T2, T3 with sham | as §5.7 | specificity survives T2 off |
| F12 | on published dyadic data, condition listener AU6/AU9 on the shared content (transcript events, the listener's own laugh onsets) | AU6/AU9 coupling to the speaker vanishes after conditioning; AU12 coupling partly survives (T3, Prop. 6) | AU6 coupling survives conditioning while AU12 does not |
| F13 | on the engine, sweep need up to λ̄ and her stake over five decades | no |Γ_ee′| exceeds ½ (T2) | any entry exceeds ½ |
| F14 | artificially scale the engine's expressive output (×0.5, ×2) for a week with a consenting tester | learned relation statistics unchanged within their posterior error (T5(b)) | statistics drift with the expressive scale |
| F15 | long-run monitor | the energy-weighted defect on the prospective subspace does not trend toward 0 across weeks; if it does, check whether the tester's statistics changed (assumption H) | trend toward 0 with unchanged world statistics |

F1, F3, F8, F13 and F14 have no published dataset. They can run only on the engine and, for the human side, with a consenting tester. Per the brief they stay untested until then. F12 can run on published data once the operator approves a dataset (Q6).

---

## Appendix: notation

| Symbol | Meaning |
|---|---|
| n = 8, k = 32, d_α = 2n + 2 = 18 | concerns, output coordinates, appraisal dimension |
| b, b*, ε, D, D_H, λ, λ̄ | body, set points, dead zones, drive, allostatic drive, concern weights, their innate bound |
| s = (o_A, o_P, f_A, f̃_P, g, g̃, q, q̃, h, h̃) | realised and predicted outcomes, attributions and beliefs, predicted harm, world share |
| α = (ℓ, w, a, h) | liking (realised), wanting (prospective), agency, world |
| Θ_{p,k}: Σ_j, e_j, c_j, c^now_j, a_g, w_p, ψ_p, a_h, w_h | the relation field |
| G = S h; S_H, S_P, S_A; 𝒞₀, E₀ | shared expression map; synergy families; liking-exclusive channels |
| R_δ ⪰ r_δ I, r_δ = σ̄² | event-level display effect and its innate floor |
| B, K_α, Π̃, Γ, Γ_𝒢 | appraisal regression, face gain, belief shrinkage, transfer, per-group transfer |
| χ, C | controllability, coping |
| ξ, Q_p, z_g | probes, her face's response to the agent's face, own causal record from randomised replies |
| 𝔉, π₀, β | the one objective, default policy, innate tilt constant |
| e₀/e | her expressive energy share in the liking-exclusive channels |

---

## History

### Revision 1 (2026-11-25)

Revision 1 is the text this file held before 2026-11-26. Its main claims and how revision 2 treats them:
- T1(h) "no dial": withdrawn; replaced by T3 and T4.
- T1(g) "regard cap": withdrawn; replaced by T2.
- R1 reflex: removed.
- R2 uniform regard: removed with ρ.
- R5 affiliative display: closed by K6.

The research/ tree is not under version control, so the full revision-1 text, unchanged, is kept as research/foundations/design-reverse-appraisal.r1.md. The critique's section and line references point there.

### Critique 1 and answer (recorded 2026-11-25T14:39:47Z)

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
