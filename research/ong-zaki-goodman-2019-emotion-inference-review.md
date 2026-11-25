# Ong, Zaki & Goodman 2019, "Computational Models of Emotion Inference in Theory of Mind: A Review and Roadmap" (Topics in Cognitive Science 11(2):338-357, doi 10.1111/tops.12371)

Source read: full text (Europe PMC open-access XML of PMC7077035), all sections including Table 1 and the Fig. 1 caption. Appendix S1 (the derivation of the taxonomy) was not read. This is a review; the studies it summarises are reported here as the authors describe them.

## Claims
- People reason about others' emotions with an "intuitive theory of emotion": a causal model in which an outcome o and the agent's beliefs b and desires d cause an emotion e ("third-person appraisal"), and the emotion causes expressions x and actions a, which cause new outcomes (Fig. 1).
- Treating Fig. 1 as a Bayesian network gives 47 inferences involving e; 26 reduce by conditional independence; the remaining 21 fall into six categories, plus a seventh (counterfactuals) added by hand (Table 1): emotion recognition P(e|x), P(e|a); third-person appraisal P(e|o,b,d); inferring causes P(o|e); cue integration P(e|o,x); reverse appraisal P(b,d|x,o); prediction P(a|e), P(x|e); counterfactuals P(e|not o).
- Third-person appraisal reduces the situation to a few features relevant to the agent's well-being (goal conduciveness, prediction error, "closeness" to a better outcome). The observer's appraisal on the agent's behalf can differ from the agent's own, both because the observer's feature set differs and because the observer's estimate of b, d may be wrong.
- Emotion recognition is context-dependent: intense positive and negative events can give perceptually similar faces (Aviezer et al. 2012, as cited), so P(e|x) alone is weak.
- The authors' own view of the largest open problem: representation. Labels ("angry" vs not) are insufficient; even a vector is insufficient because "angry at X" and "sad because Y" are relational. They suggest probabilistic programs.
- Interpersonal consequence: a partner's smile vs frown after mutual cooperation changes inferred intent and the observer's next move (de Melo et al. 2014, as summarised): reverse appraisal mediates behaviour.

## Formal model
- Causes of emotion: P(o|e) ∝ P(e|o) P(o) (Eq. 1).
- Cue integration: P(e|o,x) ∝ P(e|o) P(e|x) P(e) (Eq. 2 as printed). Under the conditional independence of o and x given e, the correct form is P(e|o) P(e|x) / P(e); the printed "× P(e)" is a typo: Ong, Zaki & Goodman 2015 (Eq. 5, derived in its Appendix B) has P(e|f)P(e|o)/P(e).
- Reverse appraisal, marginalising the latent emotion: P(b,d|x,o) ∝ P(b,d) Σ_e P(x|e) P(e|b,d,o) (Eq. 3).
- The model is computational-level (Marr); the authors say nothing about algorithm or implementation, and allow that P(x|e) may be best learned by a neural network.

## Evidence
No new data. It summarises Ong, Zaki & Goodman 2015 (gamble scenarios; see that note for numbers), Wu et al. 2018 (poison/sugar vignettes; see that note), Saxe & Houlihan 2017, and de Melo et al. 2014 (reverse appraisal in a social dilemma; not read). No effect sizes are given in the review.

## What it implies for the design
- Eq. 3 is the cleanest statement of the hypothesis under examination: the partner's face x is evidence, through a likelihood P(x|e), about latent b, d (what the partner wanted and expected) given a shared outcome o. The face never maps to the agent's face; it changes a posterior over the partner's concerns and over the situation, and the agent's response is a separate decision computed from that posterior and the agent's own concerns.
- Sign flips fall out of this structure for free in one case: if the agent's concern is anti-aligned with the partner's (competition), the same inferred "partner's goal met" is a loss for the agent. If aligned (cooperation), it is a gain. The relation enters as the sign and shape of the agent's utility over the partner's outcome, not as a gain on the partner's face. This is a per-concern, not per-channel, structure.
- Per-expression gating also arises: different facial features carry different evidence (a smile is evidence about goal conduciveness, a raised brow about expectation violation), so each feature updates a different latent and has different consequences for the agent.
- **Hidden scalar check.** Eq. 2 contains one: the reliability of P(e|x) relative to P(e|o). As the face's likelihood sharpens, the posterior over the partner's state follows the face; as it flattens, it follows the situation. That is a flat-to-face dial on the *belief*, not on the agent's *expression*. It becomes a flat-to-copy dial on the agent's face only if the agent's response is a monotone function of the inferred partner state (e.g. "express what the partner feels"). If the response is a decision over the agent's own concerns, the precision moves how confident the agent is about the partner, not which way the agent's face goes. A design must show the response function is not the identity on the inferred partner state.
- Principles 1-2 conflict: e is a labelled emotion variable in every model reviewed. The structure that does not need labels is the reverse-appraisal one (Eq. 3 with e marginalised): x is evidence about b, d and o directly, via P(x|b,d,o). The latent can be the partner's goal-relative state in the agent's own coordinates (e.g. "the change in my own needs that would make me make that face").
- The relational point (anger *at X*) matters for the agent: what the expression is about must be a variable, matching the mimicry data (anger at a shared foe vs at me).

## Verdict: adopt (as the formal frame)
The taxonomy and Eq. 3 are the reference statement of "expression as evidence about appraisal". The models reviewed all use emotion labels and hand-built outcome spaces, so the structure is adopted, not the variables.
