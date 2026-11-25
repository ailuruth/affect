# Wu, Baker, Tenenbaum & Schulz 2018, "Rational Inference of Beliefs and Desires From Emotional Expressions" (Cognitive Science 42(3):850-884, doi 10.1111/cogs.12548)

Source read: full text (Europe PMC open-access XML of PMC6033160): introduction, computational model, Experiments 1, 2a, 2b, 3, 4 (methods and results), model comparison, general discussion. The Supporting Information (scenario texts, stimulus morph percentages Table S1, Experiment 3 movie details) was not read. Stimuli in the published figures are pencil sketches; the originals were photographs.

## Claims
- Observers invert an intuitive causal model in which an agent's belief B and desire D (and action A, if she acts) cause her emotional reaction to the anticipated outcome (R0) and to the actual outcome O (R1). People recover hidden B and D from reactions "rationally", i.e. as Bayesian posterior inference.
- **Desires are easy, beliefs are hard.** From one reaction to the outcome, observers recover the desire (from valence relative to outcome) but not the belief.
- **A change of valence over time carries the belief.** Seeing the reaction before and after the outcome (R0 then R1) lets observers recover both: a valence flip means the expectation was false.
- **Surprise in the face was mostly not used.** Observers could detect surprise in the faces out of context (Exp. 2b supplemental) but did not use it to infer false belief; the authors suggest surprise is read as an intensifier of valence, and that some outcomes (a death) are "always shocking", so surprise is uninformative there.
- **Action evidence can override face evidence.** When the agent's action is improbable given the true mental state (e.g. she put poison in the coffee while wanting him to live), observers fail to recover the belief even with R0 and R1; they settle on the belief that makes the action rational.

## Formal model
P(B, D | A, O, R0, R1) ∝ P(R1 | B, D, A, O) × P(R0 | B, D, A) × P(A | B, D) × P(B, D)   (Eq. 1)

Terms drop out when absent (no A in Exp. 1-2; no R0 in Exp. 1, 3). B and D are binary (crash/safe or poison/sugar; live/die), so 4 hypotheses. **No free parameters**: every term on the right is elicited from an independent group of raters (0-100 plausibility, normalised), and the posterior is compared with a separate test group. Emotion is not a latent variable here: the face is conditioned on B, D, O directly (perfect recognition assumed, as Ong et al. 2019 note).

## Evidence
- MTurk, n ≈ 45-60 per group; three groups per experiment (prior, likelihoods, test); ~12% excluded.
- Model-human correlation: Exp. 1 r = .954; Exp. 2a r = .953; Exp. 2b r = .950; Exp. 3 (photos) high, movie replication r = .908; Exp. 4 r = .950. "All r ≥ .95" in the abstract refers to the photo stimuli.
- Exp. 1 (one reaction, agent only observes): target B-D pair rated highest in only 2 of 8 conditions; in the others the right desire, wrong-or-undecided belief.
- Exp. 2a (R0 + R1): target rated highest in all 8 conditions (all z > 3.43).
- Exp. 3-4 (agent acts): congruent conditions recovered (all z > 6.64 in Exp. 3; > 10.54 in Exp. 4); incongruent ones not, as the model also predicts.
- Model comparison: No-Emotion model (prior × action likelihood only) r = .147, .114, .085, .528, .379 for Exp. 1, 2a, 2b, 3, 4. No-Action model r = .843 (Exp. 3), .893 (Exp. 4), significantly worse in Exp. 3. A model-free "event-features" multinomial regression (action, outcome, PCA of rated emotion features of the faces), cross-validated over 44 conditions (33 train / 11 test, 10,000 splits): median r = .583 (95% CI .25-.77) vs Bayesian .957 (.92-.98).

## What it implies for the design
- The cleanest empirical support for the hypothesis that an expression is used as evidence about what the expresser wanted and expected, not as something to share. Observers (strangers, no relation) read the agent's smile at a death as evidence she wanted it; nobody would mimic that smile, and the paper's frame explains why without any gain: the smile updates the posterior over the expresser's desire, and the observer's response follows from what that desire means to the observer.
- **Valence relative to outcome is the informative quantity**, not the face itself. A positive face at a bad-for-the-agent outcome carries the sign-flipped message about the expresser's concern. This is exactly the structure that produces sign flips in the mimicry data: the same face, evaluated relative to the shared outcome and to the perceiver's concerns, has opposite meaning.
- **Temporal structure carries the belief.** The change between the pre-outcome and post-outcome face is what reveals expectation. An agent should compare the partner's expression before and after a shared event, i.e. key on the partner's expression change locked to events, not on its level. This is computable without labels.
- **Model-free regression fails.** A learned map from (outcome, face features) to the partner's state generalised poorly (r = .58) where the structured inverse model did not (.96). This is the same warning as the critique round: a learned regression from partner features to a target collapses to whatever correlation is in the data. It argues for an explicit generative model of the partner (concern → appraisal → face), with the face as a likelihood term.
- **Hidden scalar check.** Eq. 1 has no free gain; the face's weight is set by how diagnostic each face is under each hypothesis (the likelihood ratio). There is still an implicit precision (how peaked P(R|B,D,O) is), which moves the posterior between "prior/action" and "face". That precision is a property of the inference, and it decides how certain the agent is about the partner. It cannot by itself make the agent's face copy the partner's, because nothing in Eq. 1 produces the agent's face. The copy risk moves to the response step: if the agent's response were "express the partner's inferred valence", the precision would be a flat-to-copy dial again.
- **Principles 1-2.** The model uses labelled faces only through raters' likelihood judgments; B, D are discrete scenario variables. A label-free version needs P(partner's face | partner's concern state, shared outcome) learned from the agent's own experience of what its own face does when its own concerns are met or violated (Principle 3), with the shared outcome represented in the agent's own need coordinates.

## Verdict: adopt (the inverse-model result and the temporal-change finding)
Small discrete scenarios with vignettes, but a zero-parameter model at r ≈ .95 and a clean defeat of the model-free alternative. The specific finding that belief is carried by the pre/post change in valence, and not by a surprise template, is directly usable.
