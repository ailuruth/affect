# Interoceptive inference, emotion, and the embodied self

Anil K. Seth, *Trends in Cognitive Sciences* 17(11):565–573, 2013, doi:10.1016/j.tics.2013.09.007. Read from a PDF copy hosted on Karl Friston's UCL site (the Sussex repository lists it as open access). © Elsevier.

## What was read
The full main text from the PDF, extracted with pdftotext: the glossary, Boxes 1–3, Figures 1–3 with their captions, and the concluding remarks. I did not read the reference list or the "Outstanding questions" box in full.

## Claims
- "'Interoceptive inference' conceives of subjective feeling states (emotions) as arising from actively-inferred generative (predictive) models of the causes of interoceptive afferents." The paper says this "generalizes 'appraisal' theories": Schachter–Singer's arousal-plus-interpretation becomes inference about the causes of bodily change.
- Top-down interoceptive predictions run against bottom-up prediction errors. "Subjective feeling states ... are hypothesized to depend on the integrated content of these predictive representations across multiple levels." The emotion is the **best explanation** of the body signal.
- **Active inference reaches the viscera.**
  - Interoceptive predictions become set points for autonomic reflexes, just as proprioceptive predictions drive motor reflexes.
  - This works only if the precision of interoceptive error is lowered for a moment: "active interoceptive inference depends on the selective attenuation of attention to interoceptive prediction errors."
  - Otherwise, precise errors revise the prediction instead of driving action.
- **Multimodal predictions.** At higher levels, interoceptive and exteroceptive models merge into one multimodal model. Emotional responses to external cues come from these merged predictions. "Perceptual scenes that evoke interoceptive predictions will always be affectively coloured."
- **Social link.** The paper suggests that "the expression of an emotional state (e.g., anger) elicits behavioural responses from others, the detection of which could serve to confirm predictions of interoceptive condition." It points to predictive models of social interaction.
- **Self.** Body ownership is predictive multisensory integration across interoceptive and exteroceptive signals.
- **Psychopathology (Box 3).** Depersonalization ("loss of 'emotional colour'") may come from **imprecise** rather than inaccurate interoceptive predictions. Anxiety may come from mismatches between predicted and actual interoceptive states in AIC.
- The AIC is proposed as the comparator. Other frameworks (Damasio, Craig, Critchley) are described as "largely bottom-up".

## Evidence
- **Seth's own disclaimer:** "there is not yet any direct confirmatory evidence for interoceptive inference."
- Supporting evidence:
  - AIC encodes predicted pain and pain prediction error in one task, and risk and risk prediction error.
  - False cardiac feedback raises the rated emotional salience of stimuli and right-AIC activity.
  - Suzuki et al. 2013: a virtual hand pulsing in time with the participant's heartbeat increases ownership, measured by proprioceptive drift and questionnaire. Synchronous finger movement overrides the cardiac effect.
  - People with lower interoceptive sensitivity are more susceptible to the rubber-hand illusion.

## Mechanistic commitments
1. A **hierarchical generative model** whose lowest level predicts interoceptive signals and whose higher levels are multimodal.
2. **Emotion content is the inferred cause** of interoceptive change, given exteroceptive context.
3. **Precision control** decides between updating the model (perception) and acting on the body (autonomic action). Attention is precision.
4. The **self-model** is the set of signals inferred "most likely to be me", built from the same kind of inference.

## What it implies for a single formal core
Seth puts the whole affect story in one objective: prediction-error minimization over interoceptive and exteroceptive channels with learned precisions. That fits Principle 10 if the core is an active-inference or filtering scheme. Three consequences for the engine:
- **(a)** Affect content is not a variable. It is the posterior over latent causes of body change, so valence and arousal are read out of it (Principle 2).
- **(b)** A precision schedule is needed for autonomic action. The derivation must show where the transient drop in precision comes from; otherwise the core acts by hand-written reflexes instead.
- **(c)** The social sentence is the seed of Principle 3. The other's reaction is evidence about one's own state. That makes contingent responsiveness informative to the agent, which links to Gergely & Watson (gergely-watson-1996-social-biofeedback.md).

Gershman's critique (gershman-2019-free-energy-principle.md) applies. The account must predict something a decision-theoretic core would not. The candidate difference is (b): reflexes engage only when error precision drops.

## What an ablation could separate
- **Precision ablation.** Hold interoceptive precision high. Seth's account predicts fewer autonomic actions (errors revise beliefs instead), so the face and body-regulation output should be flatter. Hold it low. Beliefs then stop tracking the body, the **depersonalization analogue**: readouts become flat and decoupled from the body.
- **Exteroceptive context ablation.** Remove the exteroceptive input to the higher multimodal level. The same body perturbation should then give a less differentiated posterior. This is the functional version of Schachter–Singer. Partner context should change how the agent interprets the same body change.
- **Social-confirmation ablation.** Shuffle the timing of partner responses relative to the agent's expressions. If the other's response confirms the agent's interoceptive inference, the agent's state estimates should become less confident (higher entropy) under shuffling.

## Verdict: adopt (precision-gated active interoceptive inference; the social-confirmation idea)
A theory without simulation. Its distinctive, testable claim is the precision gate on autonomic action.
