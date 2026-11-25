# Memory, sleep replay and continual learning: synthesis for S6

Written 2026-11-25 from the twelve notes listed at the end. Everything here is our inference unless it is attributed to a note. Read status matters: Teyler & Rudy 2007, Tse et al. 2007 and McGaugh 2004 were **not** read in full (abstracts plus secondary or later sources by the same authors), and Payne & Kensinger 2010 was replaced by their 2018 review. Claims resting on those are marked.

The question is S6 (brief.md): over months of a few hours a day with one operator, a stable temperament and an operator-specific relationship should form, survive restarts and upgrades of the conceptual layer, and lose their specificity when state tagging is removed from replay (evaluation.md, E1). This note is candidate-neutral: since D68 (research/foundations/STATUS.md) no core is chosen. Under Principle 10, every rule below must come out of the chosen core's equations or be declared as a constraint on them. The last column of the ablation table says which.

## 1. Mechanisms that let temperament and relationship form from a few hours a day

**1.1 Two stores and interleaved replay (McClelland 1995; Kumaran 2016).** Each day's episodes go into a fast store that learns in one shot. A slow parametric model learns only from replay drawn from it, interleaved with older material. Interleaving is what prevents catastrophic interference: in the paper's demonstration, focused learning of "penguin" corrupts every other animal and interleaved learning does not. McClelland's two-compartment equations give a quantitative baseline that can be fitted from the engine's own logs:

- S_h(t) = S_h(0)·e^(−D_h t) (fast trace decay);
- dS_c/dt = C·S_h·(1 − S_c) − D_c·S_c, with C = ε·r_h (consolidation is driven by replay rate times trace strength);
- fitted rodent rates (D_h, C, D_c) per day run from .25/.40/.075 down to .035/.02/.003, and humans are about .001.

An engine that must show a relationship within months needs rodent-like rates (a handover over days to weeks), not human ones. Kumaran reports replay compressed about 20× in time. A few hours of contact can therefore yield many offline passes, which is how scarce data is multiplied.

**1.2 Learning in the slow store depends on prior knowledge (Tse 2007, via McClelland 2013 and Kumaran 2016; primary paper unread).** Once a schema exists, new consistent associations are learned in one trial and survive a hippocampal lesion 48 h later. Material that is inconsistent with the schema still needs slow interleaving. McClelland 2013 reproduces this with one network at one learning rate. The efficiency index (net weight change over the sum of individual changes) is .93 for consistent items and .27 for inconsistent ones. For S6 this is the route to fast relationship learning: after weeks, a new fact about the operator that fits the operator model should consolidate almost directly. **Testable:** the number of exposures needed to learn a new operator contingency that fits the existing model falls over the months.

**1.3 A separate code per context or partner protects the others.** Three forms converge:
- pattern separation: sparse, non-overlapping traces per context (Kumaran: about 2.5% active in CA3);
- per-context gains and biases with an inferred context, as in the EWC Atari agent (ewc-si note);
- context gating on the decoder only, as in van de Ven 2020.

A partner-specific mapping then forms in the partner's own parameters, initialised from a shared prior. The robust-regulator's ĉ_p already has this shape. Updates to that mapping do not overwrite the shared slow store or other partners' codes. With one operator, the "others" are the innate baseline and the simulated stranger of E1.

**1.4 Replay preserves function, not weights (Rolnick 2019; van de Ven 2020).** Two results bear on this:
- CLEAR mixes new and replayed data 50-50 and clones to stored past outputs. That nearly removes forgetting without task boundaries, and a reservoir of 5M of 900M frames is enough.
- In van de Ven, one replayed sample per 128 new ones, or a VAE with 10 hidden units, still beats every replay-free method in class-incremental learning.

The replay target should be the engine's own past outputs and predictions (distillation, T = 2). This fits Principles 1-2: no labels exist, but the engine's own past responses do. Temperament can be defined operationally as what this function-space preservation holds fixed across days.

Two limits:
- With 100% replay, a newly arriving task is learned worse the later it arrives (Rolnick), so fresh data must keep a fixed share of the waking learning signal.
- Replay protects but does not teach: in van de Ven's words, "having to learn something new is substantially harder than not forgetting it".

**1.5 Weight-importance penalties as the hardening of temperament (EWC, SI, Huszár).** The consistent form is a single penalty anchored at the latest weights, with accumulated precision Σ_t λ_t F_t, where λ_t stands for the amount of data N_t (Huszár). Read with day as task and night as boundary, the slow parameters become stiffer as evidence accumulates. That is a formal version of "temperament stabilises over months", and of McClelland's optimal learning rate falling as 1/n. Two weaknesses:
- Anchors in weight space do not survive an upgrade that changes the parameterisation, which is what S4 and the conceptual-layer upgrades in S6 do.
- Precision only grows, so unless the core derives a decay, temperament becomes unable to change.

Keep it as a candidate only if the core is Bayesian. Replay of stored features is the upgrade-proof mechanism.

**1.6 Arousal at and after encoding decides what lasts (McGaugh; Redondo & Morris; Payne & Kensinger).**
- **McGaugh** (2004 abstract plus his 2005 and 2013 papers): one valence-free modulator, noradrenergic activity in the basolateral amygdala, scales consolidation in whichever store holds the content. It acts for minutes to hours after the event: amygdala noradrenaline peaks 15-30 min after training, and an arousing video within 30 min after learning enhances memory at 1 week.
- **Synaptic tagging and capture** makes this precise. Encoding sets only a local eligibility tag, which lasts about 90 min. A later, non-specific plasticity signal captured within that window decides persistence, and novelty before or after weak learning rescues it symmetrically.
- **Payne 2008:** sleep kept negative objects but let their neutral backgrounds fade (F(1,46) = 4.7, ηp² = .10). Payne & Kensinger 2018 split the tag into a fast term (skin conductance on each trial) and a slow term (cortisol). Each predicts later memory only if sleep follows.

Together these turn "what gets replayed" into a product of a local tag and a global signal, not a single salience score (§2).

**1.7 Retrieval reopens a memory (Nader 2000; Nader & Hardt 2009).** A reactivated memory becomes labile for a window of hours. It can be updated or lost during that window, while memories that were not reactivated are untouched. In Nader 2000, anisomycin given after reactivation caused amnesia even at 14 days, and given without reactivation it did nothing. For the engine this gives two things:
- a natural limit on interference: only replayed or retrieved items update;
- a rule for re-tagging stored episodes with the current state, which Costate already proposed.

The boundary conditions are real: with strong training, 10 min of reactivation destabilised the memory and 3-5 min did not.

**1.8 Sleep may strip the affect but keep the content (Walker & van der Helm 2009; contested).** The proposed mechanism is REM-like replay with low noradrenergic gain. It keeps the episode's content and weakens its autonomic response. If it fails, the memory returns night after night. Their own cited evidence is mixed (Sterpenich 2007 for, Wagner 2002 partly against), and Payne's data show emotional content kept, without addressing affect. Treat this as an optional second pass with its own ablation, not a foundation.

**1.9 Store pointers to features, not old latents (Teyler & Rudy, abstract only; McClelland's infantile-amnesia argument; Kumaran's open problem on maintaining the index).** A trace stored in an old encoder's code becomes unreadable once the encoder changes. To survive upgrades, the episodic store keeps raw feature streams and the innate body-variable trajectories (Principle 7 already requires features, not raw media). Replay re-encodes them through the current encoder. Waking cue-driven retrieval (partial cue → whole episode) is a second replay channel that can be ablated separately from offline replay.

## 2. What "state-tagged replay" should mean, precisely

"Removing state tagging" currently names at least three different lesions, and they predict different outcomes. E1 should fix which one carries the S6 claim before data are collected.

For each stored episode k (a segment of a session, not a whole session; Payne's object-versus-background split argues for segments), store:

- **x_k**: the feature streams (operator face and voice features, the engine's own commanded outputs, and its body-variable trajectory b(t));
- **σ_k, the state tag**: the internal state at encoding, expressed in **innate coordinates** (body variables and the core's valence and arousal readouts, never a hand-named emotion) plus the partner, inferred from features, never a given label. Innate coordinates matter because a tag in an old latent space does not survive an upgrade;
- **e_k, the eligibility tag**: how much the episode could teach the model, ideally the gradient-norm-squared priority that Costate derived (∝ δ² under squared error, not |δ|);
- **y_k**: the engine's own outputs and predictions at the time, the distillation targets.

Three operations then use the tags.

**T1, priority (what gets replayed, and how often).**

p_k = e_k · ∫_{t_k−W}^{t_k+W} m(t) dt

Here m(t) is the global modulator. It is arousal derived from homeostatic deviation and does not depend on valence. W is about an hour (STC's roughly 90 min tag), and the window is symmetric, per the bidirectional novelty rescue.

Replay draws from a mixture:

P(k) = (1 − ρ)·U_cov(k) + ρ·p_k^α / Σ_j p_j^α

U_cov is a coverage-matching term. Hayes 2021 reports Isele & Cosgun's finding that replay chosen by TD error or reward alone did not stop forgetting, while coverage matching did as well as an unlimited buffer. Importance weights at β = 1 apply wherever a gradient is read as affect (Schaul note; Costate).

**T2, context reinstatement (what the replayed episode carries).** During replay, σ_k is reinstated as the conditioning context. It is fed to the per-partner code or gate (§1.3) and to the slow model's state input. The slow model therefore learns p(x | σ, partner) and not p(x).

McClelland 1995 derives what happens without this: context reaches the slow store only if reinstatements include it, and replay across contexts without the context yields "schematic", context-free memory. In van de Ven, removing conditional replay or context gating drops permuted MNIST from about 0.81 to plain generative replay's 0.40. **This is the lesion that should remove specificity.**

**T3, re-tagging (reconsolidation).** When episode k is replayed or retrieved, it becomes labile for a window. Its tags σ_k and e_k are re-evaluated under the current model and state. If the reactivation produces a prediction error, the episode's contribution to the slow store is updated.

Two guards are needed:
- a cap or extinction criterion: priority decays once replay no longer moves arousal, which is Walker's failure mode inverted;
- a valence-balance monitor, because replay under a persistent negative state rewrites neutral episodes toward negative ones (reconsolidation note).

**When.** Offline, after each daily session. Graves 2003 (cited in the sleep note) found that sleep deprivation in the first 0-5 h after training impaired memory and deprivation at 5-10 h did not. The order is:
1. a content pass (T1 sampling with T2 reinstatement, trained to distillation targets plus the self-supervised prediction loss);
2. optionally, the affect pass (Walker), with the arousal gain clamped low;
3. at the end of the night, the anchor and precision update if a §1.5 penalty is used.

During the day there is no offline replay. Waking retrieval refreshes S_h. In McClelland's argument, waking reinstatement refreshes a trace and offline replay does not, so traces that keep being relevant persist. Replayed streams never pass through the innate event detectors (D67, second amendment). The partner identity in replay comes from σ_k, not from re-detection.

**Derivation status under Principle 10.**
- Derivable from a gradient-based core: e_k ∝ ‖∇ℓ_k‖², the importance weights, and the distillation target, which is the core's own loss on its past outputs.
- Derivable if arousal is a readout of the core: m(t).
- Constraints to declare: W, ρ, α, the fast-trace decay D_h, the lability window, the affect-pass gain, and segment length.

## 3. What is ablatable

All lesions are offline on stored feature streams (E1 conditions: ≥ 20 seeds, sham lesion, operator versus simulated stranger). The predictions are ours.

| # | Lesion | Matched control | Predicted effect | Source of the prediction | Derived or constraint |
|---|---|---|---|---|---|
| L1 | **T2 off**: replay without σ_k reinstatement | same replay count, timing and samples | Operator–stranger specificity collapses toward a context-free average. Overall prediction loss barely changes. | McClelland 1995; van de Ven (0.81 → 0.40) | derived, if the core is conditional |
| L2 | **T1 off**: uniform reservoir | same replay count | Average operator statistics kept (CLEAR). Salient asymmetries lost (rupture versus repair, the operator's rare strong reactions). Specificity largely kept. Slower detection of a changed relationship (CP9: 4 nights sooner with priority) but no oscillation. | Rolnick; McGaugh; Payne; CP9 | weight derived, mixture ρ a constraint |
| L3 | T1 salience only (ρ = 1, no coverage) | same count | Everyday low-arousal interaction fades. Old-regime episodes dominate after change (CP9's oscillation). Possible negative drift. | Hayes / Isele & Cosgun; CP9 | constraint |
| L4 | **T3 off**: frozen tags | same | After the relationship changes, stale tags keep old episodes prioritised. Slower revision. | Nader; Costate's re-tagging | constraint (window) |
| L5 | No interleaving (replay only the latest days) | same count | Forgetting of the innate baseline and of stranger responses. The stranger is treated like the operator, so specificity *falls* by over-generalisation, not by loss of the operator model. | McClelland; Kumaran | derived from CLS |
| L6 | Per-partner code removed (one shared map) | same parameter count | Interference: operator learning shifts stranger responses. | EWC Atari context gains; Tse / McClelland 2013; van de Ven gating | architecture choice |
| L7 | Post-event modulator off, or one-sided window | same | Episodes whose significance became clear only after the event (a repair minutes later) are lost. | Redondo & Morris; McGaugh | constraint |
| L8 | Affect pass off (if adopted) | same compute | Reactivity to replayed rupture episodes does not decline over nights. Content is unaffected. | Walker & van der Helm (contested) | constraint |
| L9 | Replay stored latents instead of re-encoded features across an encoder upgrade | same | Specificity is lost after the upgrade (the "survive upgrades" test). | McClelland (infantile amnesia); Kumaran (index) | derived |
| L10 | Distillation targets off (prediction loss only) | same | Drift of the engine's own response style across days: temperament measured as response stability falls. van de Ven: −0.13 on permuted MNIST. | van de Ven; CLEAR without cloning | derived |
| S | Sham: random σ_k with matched marginals | – | Should behave like L1 if T2 carries the specificity. Should behave like the intact engine if specificity comes from elsewhere, for example the partner code learned online. | – | – |

L1 against L2 is the key contrast. If E1 lesions only T1, these sources predict that specificity *survives*: uniform reservoir replay is a strong null (Rolnick), and E1 could fail for the wrong reason. evaluation.md's S6 wording should name T2.

## 4. Open problems

1. **Which tag is "the" state tag in E1.** See §2. Until one is named, a failed E1 is uninterpretable.
2. **The partner tag without a label.** Partner identity must be inferred from features (EWC's inferred-context model creates a new context when none fits). With one operator and a simulated stranger, the stranger model can confound the specificity measure. A specificity score computed against a stranger the engine has never met can be inflated by novelty alone.
3. **Rates come from rodents.** McClelland's fitted rates, STC's about 90 min tag, McGaugh's 15-30 min noradrenaline peak and Graves's 0-5 h window are all biological. The engine's constants must be chosen as declared constraints, and swept.
4. **Temperament stiffening versus revisability.** Accumulated precision (§1.5) and the 1/n learning rate make temperament ever harder to change. The reconsolidation window (§1.7) is the only reopening mechanism here, and its boundary conditions (reactivation strength and duration) have no engine analogue yet.
5. **Runaway and negative drift.** Kumaran names PTSD-like runaway replay. Payne and Walker predict negative content is kept preferentially. Re-tagging under a negative state can spread negativity. The guards are an importance correction, a cap, and a valence-balance monitor. None is derived.
6. **Unlearnable transitions** (Schaul): a noisy sensor or an unpredictable channel keeps e_k high. The coverage term limits this but does not remove it.
7. **No temperament instrument** (evaluation.md, S6). Operationally, this synthesis offers response stability under distillation across days, plus the slow parameters' drift rate. Neither is a validated measure.
8. **Sleep-to-forget is contested.** The affect pass (L8) should be adopted only if a core derives it. Otherwise it is an assembled module, which Principle 10 forbids.
9. **Stored versus generative replay.** Principle 7 allows stored feature streams, so the storage and privacy argument for generative replay (van de Ven) does not apply. Generative or internal replay is worth having only if the core needs "dreamed" trajectories, for example for planning. Internal replay also requires frozen lower layers, which conflicts with re-encoding after upgrades.
10. **Unread primaries.** Teyler & Rudy 2007, Tse et al. 2007 and McGaugh 2004 full texts, and Payne & Kensinger 2010. The Clopath 2008 and Barrett 2009 STC models would give real equations for T1 and are unread.

## Notes this rests on
- mcclelland-1995-complementary-learning-systems.md
- kumaran-2016-cls-updated.md
- teyler-rudy-2007-hippocampal-indexing.md (abstract only)
- mcgaugh-2004-amygdala-modulates-consolidation.md (abstract plus later McGaugh papers)
- redondo-morris-2011-synaptic-tagging-capture.md
- nader-2000-hardt-2009-reconsolidation.md
- sleep-emotional-memory-walker-payne-kensinger.md
- tse-2007-schemas-rapid-consolidation.md (primary unread; McClelland 2013 read)
- van-de-ven-2020-brain-inspired-replay.md
- ewc-si-2017-weight-importance.md
- rolnick-2019-experience-replay-continual.md
- hayes-2021-replay-missing-biology.md
- Earlier: schaul-2016-prioritized-experience-replay.md; foundations/costate.md (Replay); foundations/contingency-parity.md (CP9); foundations/robust-regulator.md (CT8, ĉ_p); foundations/efference-memory.md (nightly slow writes).
