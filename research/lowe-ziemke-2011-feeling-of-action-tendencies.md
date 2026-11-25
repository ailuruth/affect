# Lowe & Ziemke 2011, "The feeling of action tendencies: on the emotional regulation of goal-directed behavior"

*Frontiers in Psychology* 2:346, 27 December 2011, doi:10.3389/fpsyg.2011.00346. Article type: **Review Article**.

Source read: the publisher PDF (20 pages) from frontiersin.org, read in full from the abstract to the conclusion; the reference list was skimmed. Figures were seen only as captions. There is **no model, no equation, no robot and no experiment** in this paper. It is a theoretical position paper. The computational work it points to (a dynamic-field-theory model of the Iowa gambling task, Lowe & Ziemke 2010 and Lowe et al. 2010b; energy-constrained robots, Lowe et al. 2010a and Montebelli et al. 2010) was **not read**.

## Claims
- Emotion theories either treat emotions as discrete action programs with specific autonomic profiles (Ekman, Levenson, Panksepp, Damasio), or ground them in motivation: broad appetitive and defensive systems whose tendencies are shaped by context (Frijda, Lang & Bradley, Cacioppo). The authors side with the second camp, citing weak evidence for autonomic specificity (Mauss & Robinson 2009).
- **Feelings are predictions of action tendency.** An emotional feeling is a neural-dynamic, stable, above-threshold activation pattern that predicts "what the agent is physiologically and cognitively primed to do". It is a minimal, low-dimensional prediction, updated by bodily and cognitive feedback.
- **ATPFL (action tendency prediction–feedback loops).** A primary response, the prediction (Koole's "sensitivity"), is followed by a secondary response, regulation, which is driven by the mismatch with feedback:
  - Prediction too high (the body cannot supply the predicted tendency, e.g. fatigue) leads to down-regulation, or a switch to a cheaper emotion.
  - Prediction too low (an unlearned stimulus, where the body responds more strongly than predicted) means the body leads. Volitional control is lost and later reasserted.
- **ATPFL is allostatic.** The authors redraw Sterling's (2004) allostasis loop with an added "update prediction" arrow. The prediction (feeling) desensitizes homeostatic setpoints so that resources can be mobilized; feedback then up- or down-regulates and updates the prediction (their Figure 6).
- Feeling has two tiers, an adaptation of Damasio's body loop and as-if body loop (their Figure 4):
  - (1) a coarse brainstem prediction–feedback loop;
  - (2) a contextual cortical loop (somatosensory cortex and insula) that the stimulus-evaluating areas (vmPFC, amygdala) drive *before* bodily feedback arrives.
  The as-if loop works when the agent is certain; under uncertainty, bodily feedback is needed.
- **Regulating goal-directed behavior.** Predicted action tendencies are judged for availability (energy and resources across the *whole* set of goals and needs) and acceptability (social context, actual or relative reward). Pursuing a goal that costs too much relative to the full set is down-regulated.
- The feeling substrate is proposed to be low-dimensional: pleasantness, arousal and dominance (approach–withdrawal), or PAD. These would be built speculatively from dopamine and serotonin signals:
  - P is a negation of the dopamine and serotonin signals;
  - A is their conjunction (combined magnitude);
  - D is a negation of their magnitudes.
  An attractor landscape over these fields, shaped by personality and experience, would give moods and a mapping from dimensions to discrete emotions.

## Mechanism (as stated; no equations)
- **Stabilization by dynamic neural fields (Amari 1977; Schöner 2008).**
  - A field site becomes a "unit of representation" only when it is above threshold.
  - Self-stable states need ongoing input, and the authors judge them right for emotional feelings, which end when the trigger ends.
  - Self-sustained states persist after the input is removed, and are offered as pathology (for example "sham rage").
  - Subthreshold activity is priming.
  - With an above-threshold prediction, error acts like an OR gate: it amplifies or destabilizes the state. With a subthreshold prediction it acts like an AND gate: only bodily feedback that matches the primed site raises it above threshold.
- **The emotion episode, in sequence (their Figure 7):**
  1. A trigger: a stimulus at a reinforcement contingency or goal juncture.
  2. A primary response: the PAD feeling field shifts, and the autonomic system is driven through amygdala, hypothalamus and brainstem.
  3. A secondary response: availability and acceptability feedback.
  4. Strategic or tactical selection: PAD biases appetitive and defensive subtrees, toward persisting with a goal or abandoning it.
  5. Overt coping (BAS) or inhibition (BIS).
  6. Behavioral feedback modulates all of the above.
- Goal junctures are mapped onto Rolls's reinforcement-contingency space and Boureau & Dayan's dopamine/serotonin × active/inhibitory quadrants. The emotion episode becomes BIS inhibition under uncertainty (step 1), then deliberation, then active coping (step 2).

## Evidence with numbers
None. No data, simulation or robot is reported. Support is by citation of human and animal literature (Damasio/Bechara, Koole 2009, Frijda 2004 and 2010, Lang & Bradley 2010, Sterling 2004, Boureau & Dayan 2010).

## Failure modes
- **No implementation, so no failures can be measured.** The ATPFL is a verbal box-and-arrow model. The DFT mechanism is cited, not instantiated. Thresholds, kernels and the update rule for the prediction are unspecified.
- **Assembled by reconciliation.** Damasio's loops, Koole's primary and secondary responses, Sterling's allostasis, Frijda's availability and acceptability, PAD, and Boureau & Dayan are stitched together by analogy. There is no single objective.
- **Hand-named feeling dimensions.** PAD is chosen in advance as the feeling space, with speculative neuromodulator formulas. That is the opposite of Principle 2, where valence and arousal are read out of a learned state.
- **Learning is asserted, not specified.** "Update prediction" appears in Figure 6, but the paper gives no rule for how the trigger-to-feeling association changes.
- **No ablations.** There is no system to lesion.
- **Persistence.** Feelings are self-stable (they decay with their trigger). Mood is attributed to a slowly shaped attractor landscape, again unspecified.

## License
CC BY (Frontiers open access; the 2011 standard license is CC BY 3.0, not checked on the PDF). No code.

## Runs on this Mac without a GPU?
n.a. There is nothing to run.

## Verdict: watch (as theory source for the regulation loop; not a precedent of a built system)
It clashes with Principle 2 (PAD fixed in advance) and does not meet Principle 10 (no formal core). But its central idea agrees with the engine's direction: feeling as a *prediction* of the body's readiness to act, corrected by bodily feedback, inside an allostatic loop. It is a verbal predecessor of the interoceptive-inference accounts already in the index (Seth 2013; Barrett & Simmons 2015; Sterling 2012).

## What it implies for this engine
- **Survives: affect as the predicted action readiness, compared against the body.** In a formal core, the "feeling" can be defined as the model's prediction of its own coming motor and interoceptive trajectory (expression, voice energy, approach or withdrawal), with regulation as the error between that prediction and what the body then does. That yields a testable ablation: cut the feedback path from the produced face and voice back to the state, and over- and under-estimates of readiness stop being corrected, so expressions should overshoot or fail to recover after a perturbation.
- **Survives: availability across the whole need set.** Whether to keep pursuing one need is judged against the cost to *all* needs. In the engine this is the need-conditioned attention over the full structured need set (brief, "Expressive structure"), not one goal's value. It is the same idea as Lewis & Cañamero's persistence/opportunism trade-off, stated at the level of resource budgets.
- **Survives: the two-tier timing.** A coarse, fast, body-near prediction is followed by a slow, contextual one that can run ahead of the body when it is certain. This maps onto the brief's fast loop and conceptual layer only partly. In the engine the contextual tier must remain sub-linguistic: Claude is not this tier, because Claude never reads the state (Principle 4).
- **Does not survive:** PAD as the feeling space, neuromodulator formulas set by hand, or field thresholds chosen by the designer. If the engine uses attractor dynamics, the attractors must be learned in the latent state, and any PAD-like axes must be found afterwards by probing, not built in.
- **For the synthesis table:** this is the clearest example in robot-affect research of a framework that names the right loop (prediction, bodily feedback, allostatic regulation) but never builds it. It counts as theory, not as a prior system.
