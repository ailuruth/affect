# Saxe & Houlihan 2017, "Formalizing emotion concepts within a Bayesian model of theory of mind" (Current Opinion in Psychology 17:15-21, doi 10.1016/j.copsyc.2017.04.019)

Source read: full text (author-hosted PDF, saxelab.mit.edu), all sections, Figures 1-2 and the annotated references. A 7-page opinion piece; the studies it cites are reported as Saxe & Houlihan describe them.

## Claims
- Emotions belong in the intuitive theory of mind as effects of *inferred appraisals*: interpreting events "through the lens of their relevance for one's goals, beliefs, costs" (Fig. 1). Goals/values (including long-term ones such as relationships and status) and constraints (costs, controllability, what is possible) feed the appraisal; appraisals cause emotions; emotions cause expressions. Goals and values can also act directly on expressions (display rules).
- **Faces are weak evidence.** Attribution from isolated faces is "uncertain, noisy, and low-dimensional": many emotions are attributed to one configuration; the perceived space has "a handful of dimensions"; at high intensity even valence is not readable from the face (Aviezer et al. 2012: the same configuration reads as joy, distress, pleasure or pain).
- **Forward vs inverse inference are different operations.** Expressions (face, body, voice) are effects of a common cause, so combining them sharpens the *inverse* inference continuously among nearby emotions. Event information bears on the *cause*, so it can select among separated alternatives (forward inference). Prior work confused the two (the nipple-piercing photo is event information, not posture).
- **Asymmetry.** Forward inference from inferred appraisals is granular but biased (we assume others share our desires and norms; we underestimate coping). Inverse inference from expressions is coarse but "relatively accurate and unbiased". Combined: the forward model proposes specific states, the face confirms or corrects "within a reduced possibility space".
- **Timing as evidence.** A change of expression coincident with an event outcome lets observers infer the outcome was unexpected (Wu et al.); observers otherwise miss surprise in mixed expressions. The order of expressions can tell which hidden variable went with which emotion.
- Neural: fine-grained (20-way) emotion distinctions are decodable in theory-of-mind regions (TPJ, MPFC) and generalise across stories, events and faces; expression perception and cross-modal integration depend on STS; the two dissociate in individual differences and neurodegeneration (Skerry & Saxe 2015, as cited).

## Evidence (as cited)
- With human-rated appraisals: 25 appraisal features → correct label (of 14) for 51% of 6,000 real events, only 10% of choices judged wrong (Scherer & Meuleman 2013); 38 appraisal features → correct label (of 20) for 57% of 200 stories, humans 63% (Skerry & Saxe 2015).
- 10-month-olds are surprised when an agent whose goal was fulfilled then cries (Skerry & Spelke 2014).
- Wu et al. (CogSci 2014; see the Wu 2018 note): from Grace's smile after the poisoning, observers infer she knew it was poison and wanted the death.

## Formal model
Box-and-arrow only (Fig. 1); the formal content is deferred to Ong et al. 2015 and Wu et al. 2018/Baker et al. 2009 (inverse planning). Implicitly: P(emotion | appraisal(event; goals, beliefs, costs)) forward, P(expression | emotion) inverse.

## What it implies for the design
- Supports the hypothesis directly: the partner's face should be the weak, low-dimensional, *confirming* channel, and the shared event (what just happened, what was said, what each wanted) the strong, *selecting* channel. A design that drives the agent's face from the partner's face inverts this weighting.
- The asymmetry is a concrete answer to the mimicry data. The forward route explains why identical faces get different responses (anger at a shared foe vs at me; laughter at a funny vs a disgusting scene): the event changes which appraisal is inferred, and the face only adjusts within it.
- Timing coincidence (face change locked to an event) is itself evidence; an agent can use contingency between the partner's expression changes and shared events, which it can compute without labels.
- **Hidden scalar check.** The relative weight of face vs event evidence is a reliability ratio, one scalar per cue pair. It moves the agent's *belief* about the partner between "what the face says" and "what the situation implies". It is a flat-to-copy dial on the agent's own face only if the response is "express the inferred partner state". The paper's frame places the response downstream of a model of the partner's goals, so the dial is confined to the belief. A design still has to show that.
- Principles 1-2: the paper works with emotion labels and human-rated appraisal features. The label-free part that survives is the structure: goals/costs/constraints → appraisal → expression, inverted. For the agent, the "goals" can be its own body variables used as a template for the partner's (Principle 3), so the inferred partner appraisal lives in the agent's own need coordinates.
- Display rules: goals and values act directly on expression, so a smile is not always an appraisal readout; social goals (politeness, status) are a separate cause the inverse model must include, matching Heerey & Crossley's genuine vs polite smiles in the mimicry synthesis.

## Verdict: adopt (the forward/inverse asymmetry)
Short and verbal, but its forward-vs-inverse distinction and its demotion of the face to a coarse confirming cue are the most useful framing for breaking the copy channel.
