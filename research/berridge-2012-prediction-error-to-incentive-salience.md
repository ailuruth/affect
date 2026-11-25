# Berridge 2012: From prediction error to incentive salience

Citation: K. C. Berridge, "From prediction error to incentive salience: mesolimbic computation of reward motivation". *European Journal of Neuroscience* 35(7):1124–1143, 2012. doi:10.1111/j.1460-9568.2012.07990.x. NIH author manuscript, PMC3325516.

Source read: the full author manuscript, from the PMC XML via NCBI efetch, read on 2026-11-25. Covered: the abstract, every section through the Conclusion, and the captions of Figures 1–5. Not read: the figures themselves and the reference list. Equations are quoted from the text. The primary studies (Tindell et al. 2005, 2009; Smith et al. 2011; Wyvell & Berridge 2000, 2001; Flagel et al. 2011; Berridge & Robinson 1998) were not read in the original.

Overlap: the multiplicative and additive κ forms and the rank-order argument are already in zhang-berridge-2009-incentive-salience-model.md. The dopamine-is-not-liking evidence (1% dopamine, hotspots) is in berridge-kringelbach-2015-pleasure-systems.md. This note covers what is new here: the confound argument against dopamine = TD error, the four utilities, the serial-CS dissociation of prediction from wanting, focus width, reboosting, and the dopamine-free learning results.

## Claims
- Knowledge is not motivation. "learned associations contain only information … But knowledge by itself, no matter what kind, is never motivation." Wanting is "generated anew in each moment of encounter with a previously learned cue".
- **Four utilities.** Following Kahneman et al. 1997: predicted utility (expected value), decision utility (the motivating value revealed in choice and pursuit), remembered utility and experienced utility. "for cognitive desires, decision utility = predicted utility, and predicted utility = remembered utility". Under dopamine-related stimulation, "cue-triggered decision utility > remembered utility … and similarly decision utility > predicted utility". "it is possible to 'want' what is not expected to be liked, nor remembered to be liked, as well as what is not actually liked when obtained."
- **Two signatures of wanting:** "UCS-directed 'wanting'" (PIT pulses) and "CS-directed 'wanting'" (the cue as a "motivational magnet": sign-tracking).
- **The κ = 1 confound.** "when κ=1 in the Zhang equation the incentive salience output mimics a temporal difference model". Schultz's monkeys were kept at a constant thirst ("removing water for about 20 hours before each training and test session"). So dopamine "that codes Pavlovian incentive salience might often masquerade as coding learned prediction errors". "Only when state is changed can an experimenter tell whether a neural activation encodes stable associative memory (learning) or transformed incentive salience."
- Familiar states are not a clean test, because a learning theorist can posit a separate cache per state (occasion setting). "For proof of principle, the emphasis must be on new κ states."
- **High κ alone is not wanting.** In Parkinson's patients, L-DOPA alone "failed to elicit the high surges of endogenous dopamine release in the absence of cues", and cues alone were weak. "high kappa by itself is not incentive salience. Cues are also needed."
- **Limits of the Zhang model, as the author lists them.**
  - (1) Directedness: wanting points at a particular CS/UCS, and the model "considers just one CS-UCS association at a time".
  - (2) No parameter for "width of focus". Opioid stimulation of central amygdala narrows wanting "in winner-take-all fashion"; DBS and dopamine agonists can broaden it to many targets.
  - (3) Reboosting: CS wanting is maintained trial by trial when the UCS arrives, and low-dose neuroleptic blocks reboosting, so CS value decays gradually ("extinction mimicry").
  - (4) "Miswanting": after associative devaluation (taste aversion) or overtraining, CS wanting persists although the UCS is no longer liked.
  - (5) It omits cognitive model-based desire and S–R habits.
- **Dopamine is not needed for reward learning.** "Without dopamine, the 6-OHDA rats had normal 'liking' and learning, but no 'wanting'."

## Evidence with numbers
- **Serial CS.** CS1→CS2→sucrose (Smith et al. 2011; Tindell et al. 2005).
  - Before CS1 the chance of predicting reward is "roughly 1 out of 14", given as "log2 h=3.88". Note: log₂14 ≈ 3.81, so the reported figure does not match its own probability.
  - CS1 takes surprisal to about 0. CS2 "adds almost no new predictive information" yet carries maximal approach.
  - NAc amphetamine amplified VP firing to CS2 "to levels 1.5 X normal" (">50%" in the Fig. 3 caption), while firing to CS1 "remained unchanged". DAMGO in the hotspot did the same.
  - Sensitization (amphetamine binges weeks earlier) amplified CS2 but not CS1, with no drug on board. Sensitization plus amphetamine on test day "added cumulatively".
  - When the sucrose UCS was finally delivered, neither amphetamine nor sensitization amplified UCS-evoked firing. Only opioid stimulation of the hotspot did.
- **PIT** (Wyvell & Berridge 2000, 2001). NAc amphetamine raised the peak of cue-triggered pressing surges, each lasting "about a minute", but not the baseline plateau. Sensitization weeks before did the same with no drug on board. The CS had never been paired with pressing, which rules out S–R habit.
- **Salt.** Body ≈ 0.9% NaCl; seawater ≈ 3%; UCS 10% NaCl ("roughly equivalent to … the Dead Sea"). Appetite was induced within 24 h. On the first CS in the new state, VP neurons fired "as robustly to the salt-associated CS … as to the sweet-associated CS".
- **Dopamine-free learning.** 6-OHDA "destroyed 98% of dopamine neurons in nucleus accumbens and neostriatum". The lesioned rats learned a LiCl taste aversion after 3 pairings as fully as controls (liking reactions reversed to gapes), but would have starved without intragastric feeding. Dopamine-deficient mice learn sucrose-spout and place preferences.
- **Humans.** Leptin-deficient adults: leptin plus a meal dampened mesolimbic food-cue activation (Farooqi et al. 2007). DDS patients: L-DOPA raised cue-evoked ventral striatal dopamine (O'Sullivan et al. 2011), and dopamine release correlated with wanting-more ratings, not liking (Evans et al. 2006).
- **Sign- vs goal-trackers** (Flagel et al. 2011). Learning was equal; only sign-trackers showed large phasic NAc dopamine to the lever, and only sign-tracking was impaired by dopamine blockade. This paper gives no effect sizes.

## Formal model (quoted)
- Generic: `Ṽ(s_t) = r̃(r_t, κ) + γV(s_{t+1})`, with κ = 1 during training. Multiplicative: `r̃ = κ·r_t` (drugs, sensitization, most hunger). Additive: `r̃ = r_t + log κ` (valence reversals: salt appetite, desire↔dread).
- Extension proposed in the text: for a UCS itself, put an innate attractiveness `U_t` in place of r_t, "modulated by kappa in … exactly the same way".
- The learned input r_t may come from any Pavlovian learner, not only TD: "What is important … is the interaction of κ with r_t".

## License
NIH author manuscript in PMC (open manuscript). No code.

## Runs on this Mac without a GPU?
n.a.

## Verdict: adopt (as the test design and the target signatures)
Two pieces are directly usable. (1) The κ = 1 confound is a rule for our ablation design: a wanting/learning dissociation can be shown only across a change of body state never seen in training. (2) The serial-CS result is a ready-made signature: a gain that raises the response to the proximal cue (CS2) but leaves the predictive cue (CS1) unchanged.

## What it implies for one formal core
- **Formal split.** Experienced utility (liking) = the realized change in the core's objective at consumption, e.g. drive reduction `ℓ_t = D(b_t) − D(b_{t+1})`. Predicted utility = the learned or model-based expectation of ℓ. Decision utility (wanting) = the predicted utility after a cue-gated gain, which enters the policy and attention but not the learning target. In symbols: `w(c) = g(b, h)·Ê[ℓ | c, b]`, where g depends on body state b and a slow history h. Learning updates `Ê[ℓ]` from the realized ℓ only, not from w.
- **Satiable natural appetite is safe; sensitization is not.** Natural appetite enters through b in both ℓ and Ê[ℓ], so wanting and liking move together and both fall to zero at the setpoint. That is Principle 6. The dopamine-like factor g is the only place the two can dissociate. A g that rises with exposure (sensitization) is a non-satiable term: it raises wanting without any deficit and lasts "for years" (see robinson-berridge-2008-incentive-sensitization.md). The core may hold g as a precision or gain on cue-predicted value, but g must not learn upward from repeated exposure to one partner.
- **Cue AND state, not either.** The interaction finding ("high kappa by itself is not incentive salience") requires the gain to be multiplicative with a cue-evoked prediction, not an additive arousal term. An additive tonic arousal channel would fail this test.
- **Focus width is the structure the brief asks for.** Winner-take-all versus broad attribution of salience is exactly need-conditioned attention over cues with a temperature. A per-need κ alone has no width parameter; a softmax over cue-attached predicted values, with a temperature, does.
- **Agency and controllability.** The paper adds little directly. One point: the PIT effect works on an action never paired with the cue, so wanting energizes whatever instrumental means the agent believes it controls. Coping potential (my action can reach the outcome) and wanting (the outcome is worth reaching now) should therefore multiply in the policy, not compete as alternatives.

## Ablations this separates
- **Gain ablation (6-OHDA analogue).** Set g = 0. Prediction: no approach to cues and no PIT; the liking readout on contact is intact; a new value is still learned at a normal rate (the Berridge & Robinson 1998 pattern). If learning also fails, the core has wrongly routed its learning signal through wanting.
- **Gain elevation.** Raise g on test day only. Prediction: the response to the proximal cue (CS2-like) rises about 1.5× while the predictive cue (CS1-like) and the consummatory readout do not change.
- **Liking ablation.** Remove ℓ from the readout while keeping the cached Ê[ℓ]. Prediction: approach to cues continues at first (decision utility intact) but decays with no reboosting, since nothing refreshes the cache. This is the double dissociation, and both halves must be run in a never-trained body state, or the κ = 1 confound hides it.
