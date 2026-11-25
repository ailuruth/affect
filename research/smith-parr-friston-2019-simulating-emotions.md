# Smith, Parr & Friston 2019: Simulating Emotions (active inference model of emotion concept learning)

Source read: full text, Front. Psychol. 10:2844, doi:10.3389/fpsyg.2019.02844 (PDF from frontiersin.org). Supplementary `Emotion_learning_model.m` not opened.

## Claims
- Emotion conceptualization can be cast as inference over a hidden-state factor ("emotion concepts") that generates five lower-level outcome modalities: valence, arousal, approach/avoid, situation (social rejection / crowded event), blame (self/other).
- Attention is a mental action: a second state factor picks which modality gives a precise observation. Policies are one-step, chosen by expected free energy, so the agent forages for evidence (epistemic value), then reports (pragmatic value, prior preference for "correct" feedback).
- Concepts can be learned from "blank" states (flat A matrix) by Dirichlet count accumulation on A and D.
- Learning fails when outcome precision or transition (stability) precision is low; early one-emotion "childhoods" and habitual attention biases (E matrix, 50x prior on some policies) yield coarse or wrong concepts.

## Evidence
- Toy POMDP: 4 emotion states (SAD, AFRAID, ANGRY, HAPPY) x 6 attention states, 6 time steps per trial. Hand-written A mapping (e.g. ANGRY -> unpleasant, high arousal, approach, social rejection, other-blame).
- Precision set by softmax temperature on A and B. Temp 2 for both: learning reaches ~100% report accuracy over 200 trials (50 per emotion, interleaved). Tipping points: A precision 1.5, B precision 0.5.
- "Adulthood": after 150 trials on 3 emotions, a 4th is added over 200 trials. ANGRY, SAD, HAPPY learned (HAPPY interfered with SAD); AFRAID not learned. 100 AFRAID-only trials ("flooding") fixed it; 600 interleaved trials reached 40-80%.
- Attention-bias runs (40 trials, no learning): e.g. somatic bias gives SAD 10%, HAPPY 0%.
- Single simulated agent, no statistics across seeds reported; authors call it "deliberately simple", "a proof of principle".

## License
- Paper: CC BY (stated on the article).
- Code: supplementary MATLAB script; belief updates call `spm_MDP_VB_X.m` from SPM12 (github spm/spm is GPL-2.0). No separate license seen for the supplement.

## Runs on this Mac without a GPU?
Yes in principle: small discrete POMDP, CPU only. Needs MATLAB plus SPM12. Not tried; Octave compatibility not checked.

## Verdict: watch
The model's hidden states are hand-named emotions supervised by "correct/incorrect" report feedback. Copying it would put named emotion variables and a label target into the system, against Principles 1 and 2. The findings about learning dynamics are still useful for S1, so keep it as a reference rather than a component.

## What it gives S1
- A precedent for Claude's job. In this model a concept is learned by pairing a pattern of lower-level outcomes with a label from outside (in their reading, "linguistic feedback from others in one's culture"). In S1 the latent `h` stays unnamed and Claude supplies the label afterwards, so the labelling step sits outside the dynamics, as Principle 4 requires.
- Stability prior matters. Concept learning collapsed when B (state persistence) precision fell to 0.5. Prediction for S1: if `h` mixes too fast between turns, Claude's names for a state will not stay consistent across a silence. Give `h` a slow component, on the "mood over minutes to hours" timescale in the brief.
- Failure modes to watch in S3 replay: (a) strong D priors make the agent "jump to conclusions" from 2 observations; (b) a history dominated by one pattern stops later concepts from forming; (c) a new concept needs persistent unexplained evidence before it splits off. Replay weighting by state change should be checked for (b).
- Attention as a mental action (choosing which channel to sample) is a candidate innate subsystem ("orienting"), but here it is fitted to a report task. Do not copy the reward-for-correct-report preference: that would be a social-approval target (Principle 6).
- Not useful for the S1 silence claim directly: there is no body variable or time-in-absence in the model.
