# Emotions are emergent processes: they require a dynamic computational architecture

Klaus R. Scherer, *Philosophical Transactions of the Royal Society B* 364(1535):3459–3474, 2009, doi:10.1098/rstb.2009.0141 (PMC2781886). This is the computational statement of the component process model (CPM). Its companion is Scherer 2009, *Cognition & Emotion* 23(7), which I did not read.

## What was read
The PMC full text (the first 100k of 113k characters), read through a fetch tool that returned summaries and the verbatim quotes I asked for. Figures and Table 1 were seen only as captions or summarized. The tail of the reference list was not read.

## Claims
- **Definition.** Emotion is "a bounded episode in the life of a system", an emergent pattern of component synchronization that prepares adaptive action tendencies.
- **Four central features** (after Frijda & Scherer 2009):
  1. **relevance**: "Emotions are elicited when something relevant happens to the organism";
  2. **action readiness**;
  3. **whole-person engagement and synchronization**;
  4. **control precedence**: "Emotions bestow control precedence" on states of action readiness.
- **Five components:** appraisal, autonomic physiology, motor expression (somatic nervous system), motivation (action tendencies) and feeling. Feeling "monitors and regulates the component process".
- **Stimulus evaluation checks (SECs):** relevance, implications, coping potential and normative significance.
  - All checks run "simultaneously, starting with relevance detection", but each reaches preliminary closure in a fixed order.
  - Appraisal is **recursive**: it repeats until monitoring signals termination.
- **Three levels of appraisal:**
  - sensory-motor, "mostly genetically determined";
  - schematic, "based on social learning";
  - conceptual, "requiring consciousness".
- **Component patterning.** Each SEC result has **direct efferent effects** on face, voice, autonomic physiology and posture (Table 1). Emotion-specific expressions are therefore compositions of check-by-check effects, not fixed programmes.
- **Emergence.**
  - "Basic emotion theories postulate neuromotor affect programmes"; under them "there is no emergent pattern but the relatively rigid execution of a programme."
  - Appraisal theorists "espouse emergentism". Frequent combinations make up "modal emotion families", not categories that are built in.
- **Feeling and consciousness.** "It is hypothesized that it is the degree of synchronization of the components ... that will generate conscious experience." A Venn model sets out three nested sets:
  - **A**, the unconscious monitoring of all components;
  - **B**, the conscious part (qualia);
  - **C**, the verbalized part, which depends on the language's categories.
- **Architecture.**
  - Neural networks are "much better suited to model emergent emotion processes" than rule systems.
  - Adaptive thresholds, nonlinear dynamics, attractors and **hysteresis**. One example is a cusp catastrophe for anger as a function of goal obstruction and coping power.
  - Scherer recommends starting with "a very simple creature, an organismus simplicissimus".

## Evidence
The paper says a review would "largely exceed the available space". Table 1 gives the predicted efferent patterns for each SEC, citing for example the P3a and alpha changes for novelty. It mentions GENESE, an expert system at 78% accuracy, and an interactive activation and competition (IAC) network prototype. No new data.

## Mechanistic commitments
1. **Several coupled subsystems** whose coherence *is* the emotion episode. The episode is a pattern across subsystems, not a separate node.
2. **Graded, recursive evaluation** of events against concerns, with an order of completion.
3. **Direct efference.** Each appraisal dimension drives expression and physiology on its own, with no emotion label in between. (This lines up with Principle 1.)
4. **Nonlinear dynamics with hysteresis.**
5. **Feeling as an integrating monitor** over the components, with conscious access scaled by synchronization.

## What it implies for a single formal core
Of the theories read, Scherer's is the most compatible with "elements emerge, not named". He explicitly rejects programme nodes, and his checks are continuous evaluations rather than labels. In a single core the SECs need not be modules:
- **relevance** is the magnitude of predicted change in the core's objective;
- **implications** (conduciveness) is its sign;
- **coping potential** is how far the agent's available actions can change that outcome, which is the controllability of the value;
- **novelty** is prediction error.

If these four quantities come out of the core's equations and each drives the face directly, then expressions are composed in the Scherer sense, which is a derivation target for Principle 10.

His **synchronization hypothesis** gives a measurable quantity: coherence across the engine's output channels (face, voice, policy, body variables) over an episode. It can be compared with Russell's claim that coherence is low (russell-2003-core-affect.md).

## What an ablation could separate
- **Check order.** Perturb an input so that relevance is detected early and conduciveness late. Scherer predicts **sequential efferent onsets**: novelty or orienting effects on the face (brow, gaze) before conduciveness effects (smile or frown). With a parallel all-at-once core, onsets would coincide. This is testable on the engine's face timing.
- **Coping-potential ablation.** Remove the agent's model of its own action efficacy. Obstruction should then give a single undifferentiated negative response, with no split between a high-power state (anger-like, approach) and a low-power state (withdrawal). See also Moors et al. on developmental differentiation (moors-2013-appraisal-theories.md).
- **Hysteresis.** Sweep obstruction up and then down. A nonlinear core shows different switching points on the way up and on the way down; a linear readout does not. This is a direct test of the cusp claim.
- **Synchronization.** Decouple the output channels from the shared latent. Coherence across channels should fall.

## Verdict: adopt (emergent component patterning; the check quantities as derivation targets; sequence and hysteresis tests)
It gives a blueprint and not a model, so the computational claims are proposals.
