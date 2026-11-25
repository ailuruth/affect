# Ong, Zaki & Goodman 2015, "Affective cognition: Exploring lay theories of emotion" (Cognition 143:141-162, doi 10.1016/j.cognition.2015.06.010)

Source read: accepted manuscript (revision of 12 June 2015, cocolab.stanford.edu PDF): introduction, Experiments 1-4 (methods, model details, results) and the opening of the general discussion in full; Appendices A-B (model selection, derivation of the cue-integration equation) and the later discussion were skimmed only. Numbers below are from the manuscript and should match the journal version, which I did not see.

## Claims
- People reason about others' emotions with a structured lay theory, modelled as a causal network: outcome o → emotion e → expressions (face f, utterance u). Forward, backward and multi-cue inferences all follow from one model by Bayes' rule.
- The forward model P(e|o) is low-dimensional and economic: observers' attributions depend on amount won, prediction error PE (won minus the wheel's expected value) and |PE| (loss aversion). Regret, relief, win probability and a near-miss term did not survive stepwise selection for most emotions (they did for surprise).
- Attributed emotions collapse to two principal components: PC1 (59% of variance) tracks valence and correlates with PE, r = .737 [.707, .764]; PC2 (16%) tracks intensity of positive and negative emotions ("arousal") and correlates with |PE|, r = .280.
- Cue conflicts are resolved by reliability, not by a fixed dominance rule ("face dominance" vs "context dominance"): each cue is weighted by how peaked P(e|cue) is.
- In their gambling task, positive cues were more reliable than negative ones, which looks like "positive-valence dominance" but is a reliability effect; the authors warn it should not be generalised.

## Formal model
- Forward (Exp. 1): e_k = c0_k + c1_k·win + c2_k·PE + c3_k·|PE| + ε_k, one linear mixed model per emotion k of 8; ε_k ~ N(0, σ_k²).
- Backward (Exp. 2): P(o|e) ∝ P(e|o) P(o), with P(o) = sector size, P(e|o) = Π_k N(e_k − ê_k(o); 0, (ζσ_k)²). **One free parameter ζ**, a likelihood-smoothing (precision) factor, fitted: ζ = 3.2 [2.9, 3.6].
- Cue integration (Exp. 3-4): P(e|o,f) ∝ P(e|f) P(e|o) / P(e), with P(e|f), P(e|o) estimated as smoothed empirical distributions from single-cue trials. Reliability = low Shannon entropy of P(e|cue).
- Faces were FaceGen avatars: 12 varying in valence and in arousal (lip gap), 6 "ambiguous" blends.

## Evidence
- Exp. 1: N = 100 (MTurk), 18 wheels × 3 outcomes → 50 scenarios, 10 trials each, 8 emotion scales.
- Exp. 2 (outcome from emotion profile, N = 122): model r = .806 [.792, .819], RMSE .116; split-half ceiling r = .895.
- Exp. 3 (faces + outcomes, N = 465): Bayesian r = .812 [.790, .833] vs face-only .733 and outcome-only .692 (both p < .001); RMSE 1.218 vs 1.386 and 1.524. Incongruent trials: negative face + best outcome, Bayesian r = .571, face-only .343, outcome-only .465; positive face + worst outcome, Bayesian .667, face-only .678, outcome-only .297. Entropy of P(e|f): negative faces 2.66 bits vs positive 1.60 bits (t(7) = 2.70, p = .03); negative wheels 2.39 vs positive 1.99 bits.
- Exp. 4 (utterances + outcomes, N = 150): Bayesian r = .733 vs utterance-only .570, outcome-only .668. Utterance-only correlated *negatively* (r = −.147) with judgments for negative utterance + positive outcome.

## What it implies for the design
- **This is where the hidden scalar lives, named.** ζ is exactly a likelihood precision on the expressive cue, and in the cue-integration model the face's influence on the inferred partner state is set by its entropy. If the agent's response were "adopt the inferred partner emotion", ζ (or a global precision on the partner's face) would run the agent from flat (face ignored, outcome only) to copy (face dominant). The paper is the precise statement of the risk the critique round found, displaced from the face channel to the belief channel.
- **But reliability is per cue and per value, not global.** Negative faces were less reliable (higher entropy) than positive ones in the same task; a single learned precision would not reproduce this. In a design where precisions are per-feature and per-context (computed from the agent's own predictive record of the partner), there is no single knob; the weighting is a by-product of how diagnostic each feature has been. This is the same shape as the per-expression gating in the mimicry data (smile return robust, brow and sadness responses context-dependent), and it suggests a mechanism: robust responses are those to reliable cues.
- **Valence relative to a reference** (PE, not amount) is the core of the observer's forward model. For the agent, the partner's outcome should be scored against the partner's expectation, and the agent's response to it against the agent's own concerns. Both are differences, computable in body coordinates without labels.
- **Context selects, face adjusts.** When the face conflicts with the outcome, the less reliable cue loses. With the mimicry data in mind: a rival's sad face in a context where the rival lost to me is integrated with the outcome, and what the agent does with that loss is determined by the agent's own stake, giving the brow relaxation (positive response) the data show.
- **Labels.** All variables are 8 Ekman-plus adjectives rated by humans (against Principles 1-2). The parts that transfer are the low-dimensional reference-dependent forward model and reliability-weighted fusion; the latent e must be replaced by a state in the agent's own coordinates.

## Verdict: adopt (the cue-integration result and ζ as the named risk)
A clean, quantitative demonstration that people fuse face and situation by reliability, with one fitted precision parameter. It confirms the hypothesis's structure and names the scalar a design must not expose globally.
