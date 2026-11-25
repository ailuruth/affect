# Dayan & Berridge 2014: Model-based and model-free Pavlovian reward learning

Citation: P. Dayan and K. C. Berridge, "Model-based and model-free Pavlovian reward learning: revaluation, revision, and revelation". *Cognitive, Affective & Behavioral Neuroscience* 14(2):473–492, 2014. doi:10.3758/s13415-014-0277-8. NIH author manuscript, PMC4074442.

Source read: the full author manuscript, from the PMC XML via NCBI efetch, read on 2026-11-25. Covered: the abstract, sections 1–5, the Appendix with all equations, and the captions of Figures 1–2. The figures themselves were not seen. Not read: the reference list. The equations below are quoted from the Appendix. The words "revision" and "revelation" in the title are not defined anywhere in the body text that was read. The paper's own terms are revaluation, stimulus substitution and UCS "defocusing". The data it discusses (Robinson & Berridge 2013; Tindell et al. 2009) were not read in the original.

Overlap: the κ equation itself, and the salt-appetite result in ventral pallidum, are in zhang-berridge-2009-incentive-salience-model.md. The wanting/liking substrates are in berridge-kringelbach-2015-pleasure-systems.md. This note adds the model-based reading, the claim that κ needs the outcome's identity, and the link between Pavlovian control and action–outcome uncertainty.

## Claims
- Pavlovian prediction is not only model-free. "Pavlovian predictions can involve their own form of model-based evaluation. In model-based Pavlovian evaluation, prevailing states of the body and brain influence value computations, and thereby produce powerful incentive motivations that can sometimes be quite new."
- What makes a response Pavlovian is that "the conditioned response is directly elicited by a CS that is predictive of a UCS, without regard to the effect of the response on the provision or omission of that UCS". The responses in the salt experiment "achieved no instrumental benefit".
- Instant revaluation requires the outcome's identity, not just its value. "the computation must possess information about the sensory/perceptual identity of Pavlovian outcomes, distinct from mere previous values". The identity must also be "connected to the modulation of value by the current physiological state".
- The Zhang κ model does "violence … to any pre-existing model-free cache". "In order for the κ transformation to operate correctly, it is essential that the identity of the reward that is immediately expected be known, so that its appropriate κ can be applied." Also, "κ(m, m̃) [must] be a function of both the original m and current m̃ motivational states". Splitting off r_t and knowing s_{t+1} "exactly constitute a model of the domain". The κ model is therefore read as "an heuristic method for calculating an approximate model-based prediction".
- Defocusing. With extended training the predicted UCS representation may become "generalized, blurred or otherwise partially merged" into a category ("tasty food"). A defocused prediction escapes identity-specific devaluation but still motivates. This is offered as an alternative to "habit" for devaluation insensitivity and for general PIT. The authors grant that it blurs the model-based/model-free line, because a model-based system with a defocused outcome behaves like a model-free one.
- Pavlovian and instrumental model-based values may differ in uncertainty. "Pavlovian model-based predictions might be less uncertain than instrumental ones, since they do not have to incorporate an assessment of the contingency between action and outcome". So "there might still only be one model-based knowledge system, but two control systems". Instrumental incentive learning needs retasting and is independent of dopamine; Pavlovian revaluation needs no retasting and is dopamine-modulated.
- Dopamine release "can actually reflect model-based evaluations rather than (at least only) model-free predictions".
- Aversive Pavlovian predictions can prune the model-based search tree (citing Dayan & Huys 2008; Huys et al. 2012). This is "an influence over internal, cognitive, actions".

## Evidence (all secondary, from the authors' summaries)
- Dead Sea salt experiment (Robinson & Berridge 2013). The CS predicted an intra-oral squirt of NaCl at Dead Sea concentration, "triple that of ordinary seawater". Rats turned away from the lever, "pressing themselves against the opposite wall". After first-ever deoxycorticosterone + furosemide, tested in extinction with no retasting: "appetitive engagement with salt-associated CS increased by a factor of more than 10 compared with the pre-deprivation training days". This happened on the very first presentations. The sucrose lever and the control lever were unchanged. The salt CS sometimes elicited orofacial "liking" reactions (lip and paw licking): CS alliesthesia.
- Fos. The CS plus appetite together raised Fos in the NAc core and rostral shell, VTA, rostral VP, infralimbic and orbitofrontal cortex. "No significant Fos elevation at all" occurred in VTA with appetite alone, and "only one-third as high or less" in NAc. The cue and the state interact; neither alone suffices.
- Decorticate rats still revalue salt cues under new salt appetite (Wirsig & Grill 1982), so cortex is "not necessary".
- First-order CSs are revalued immediately and second-order CSs less so (Holland & Rescorla 1975). Holland 2004: after overtraining, devaluation fails to reduce specific PIT even though head entries to the dish fall.
- Sign-trackers show CS-evoked dopamine and are dopamine-antagonist sensitive; goal-trackers are not (Flagel et al. 2011). No numbers given here.

## Formal model (Appendix, quoted)
- Value of circumstance s under motivational state m: `V(s_t, m) = E[Σ_τ γ^τ r(s_{t+τ}, m)]`.
- Model-free TD: `δ_t = r_t + γV(s_{t+1}, m) − V(s_t, m)`, `V ← V + εδ_t`. "If the state changes from m to m̃, the model-free learning mechanism provides no hint as to how to change V(s_t, m) to V(s_t, m̃)."
- Zhang κ (A3): `Ṽ(s_t, m̃) = r_t·κ + γV(s_{t+1}, m)`.
- Model-based (A4): `V(s_t, m̃) = r(s_t, m̃) + Σ T_{s_t s_{t+1}} r(s_{t+1}, m̃) + Σ T²_{s_t s_{t+2}} r(s_{t+2}, m̃) + …`. Here `T_xy = P(s_{t+1}=y | s_t=x)`, and r(s, m̃) is the utility of the outcome *identity* at s under the current state.
- Their point: (A3) is (A4) truncated after one step, with the model-free cache standing in for the tail. Revaluation works only for the immediate term, which is why first-order cues revalue and second-order cues lag.

No algorithm is fitted. "A comprehensive algorithmic version of the model-based Pavlovian computation has yet to be proposed."

## License
NIH author manuscript in PMC: "available for text mining … consistent with the principles of fair use". No code.

## Runs on this Mac without a GPU?
n.a.

## Verdict: adopt (as the formal form of the wanting term)
It turns κ from a free gain into a consequence of evaluating a predicted outcome identity under the current body state. That is what a single core with satiable drives can produce without adding a variable.

## What it implies for one formal core
- **Wanting can be derived without a named variable.** Let the core predict, for a cue c, a distribution over outcome identities o, each with a body effect Δ_o. Let the core's homeostatic objective be a drive D(b) (e.g. Keramati & Gutkin's distance to setpoint). Then the model-based Pavlovian value is (A4) with `r(o, b) = D(b) − D(b + Δ_o)`. The "κ" of Zhang et al. is not a parameter here. It is the local slope of D along Δ_o, which is need-specific automatically: salt depletion changes only the salt coordinate of ∇D.
- **The sign flip comes free, but the ranking claim becomes testable.** My derivation, not the paper's: with a quadratic drive, `r(Δ) = 2g·Δ − Δ²` for deficit g. At g ≈ 0 every salt concentration is aversive, with the strongest worst. Under a large deficit (g greater than every concentration) the strongest becomes best, which inverts the rank order. Berridge (2012) states instead that "the least disliked … becomes the most liked", which preserves it. A quadratic-drive core and Zhang's additive `r + log κ` therefore make different predictions about rank order under depletion. Which drive shape fits is an empirical question the core must answer, not assume.
- **Liking** is the same r evaluated on the *sensed* body change at consumption, not the predicted one. Wanting and liking share D, which is why natural appetite moves both together (Berridge 2012, Fig. 1). They come apart only where the predicted path has a gain that the sensed path lacks (see berridge-2012-prediction-error-to-incentive-salience.md).
- **Controllability enters through the arbitration.** The paper's claim that Pavlovian prediction beats instrumental prediction because it need not estimate action–outcome contingency gives a formal hook for coping potential. When the core's estimate of action→outcome contingency is uncertain or low, Pavlovian (outcome-predicted, action-blind) control should dominate. When it is high, instrumental control should. This is the same arbitration Dorfman & Gershman 2019 fit with an explicit controllability belief. The two papers together put coping potential and incentive salience on the same arbitration weight.
- **Defocusing is a representational claim the core can host.** A hierarchical outcome code (specific identity → category → valence only) gives specific PIT, general PIT and valence-only blocking as three levels of one predictor, with no separate model-free system needed.

## Ablations this separates
- **Identity ablation.** Replace the outcome-identity prediction with a scalar cached value (model-free only). Prediction: in a never-experienced need state, the cue tied to that need's outcome is not revalued on first encounter, and its approach stays at the learned (possibly negative) value until re-experienced. With identity intact, approach shifts on the first trial and only for that cue (>10× in the rat data).
- **State-input ablation.** Keep identity, hold the body state entering r(o, b) fixed at its training value. Prediction: the same failure, plus no selectivity across needs.
- **Contingency arbitration ablation.** Fix the arbitration weight between Pavlovian and instrumental values. Prediction: no shift towards cue-driven responding when action–outcome contingency is degraded. This is the bridge test to the controllability notes.
