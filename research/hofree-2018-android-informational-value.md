# Hofree, Ruvolo, Reinert, Bartlett & Winkielman 2018, "Behind the Robot's Smiles and Frowns: In Social Context, People Do Not Mirror Android's Expressions But React to Their Informational Value" (Frontiers in Neurorobotics 12:14, doi 10.3389/fnbot.2018.00014)

Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC5928139/ (open access).

## What was read
The full PMC text: introduction, method, all results sections, discussion, figure captions. Figures were read only through their captions. The prior study with the same android (Hofree et al. 2014, PLoS ONE) was not read; its results are used below only as this paper reports them.

## What it says
- **Design.** N = 27 (20 men). 32 dice games against or with a realistic android (Hanson's Einstein); participants were *told* that the android was a teammate in one block and an opponent in the other, and that its faces were honest. On half the trials the outcome was shown as text, on the other half only by the android's face: it smiled if it won and frowned if it lost. As a teammate, its smile meant the participant won; as an opponent, its smile meant the participant lost. EMG over zygomaticus and corrugator, in 500-ms bins over 6 s after the outcome, z-scored per participant and muscle. The android takes about 1 s to begin an expression; the authors' earlier study found a mean human lag of 1.18 s behind it.
- **The response follows the outcome for the self, not the face.** Zygomaticus rose more to wins than to losses in the later part of the trial (Time × Outcome F(1,10755) = 8.47, p = .004; second-half means F(1,894.7) = 5.09, p = .02). The corrugator relaxed less after losses (F(1,10792) = 5.27, p = .02).
- **No moderation by block.** Block × Outcome was not significant (zygomaticus F(1,71.6) = 0.55; corrugator F(1,49.5) = 1.42), nor was Block × Outcome × Time. So a teammate's smile and an opponent's frown produced about the same smiling, and a teammate's frown and an opponent's smile about the same frowning. The sign of the response to the android's smile flipped with the instructed contingency, from the first block on; no learning curve is reported or needed.
- **Face vs text.** The corrugator outcome effect appeared only when the face carried the outcome (Information Mode × Outcome × Time F(1,20192) = 4.47, p = .03). The zygomaticus was more active overall when the opponent's face gave the outcome (0.27 vs 0.17, F(1,25.8) = 4.75, p = .04).
- **Context-free baseline (as reported from Hofree et al. 2014).** With mere observation, people matched the same android's smiles and frowns.
- 34 % of participants described the android as creepy or scary; these were "relatively less influenced" (analyses on request).

## What matters for this engine
- **The cleanest within-session sign flip read so far, and it is not learned.** The flip is set by an instruction about whose outcome the face reports. It shows that when the face carries information about the observer's own outcome, the observer's face answers the outcome. It says nothing about how fast a relation is learned from experience.
- **Timing.** The outcome effect sits in the second half of a 6-s window, about 1–4 s after the android's expression began. Mere observation gives matching (2014 study, as reported). Fast matching first, context later, fits; the study cannot separate an early mimicry component because the android's own lag smears the onset.
- **Learning signal: approval-closed.** The observer's outcome (a dice roll) never depends on the observer's face, so nothing can train the observer's expression toward what the android prefers. The response is an appraisal of an outcome for the self.
- **For the build core.** In the build core his face can never move the agent's own appraisal or its own displays except through the capped copy routes (rule 10, E1). An outcome conveyed only by his face therefore cannot produce the agent's own smile or own distress face; the same outcome in his words can (drop and rise events, Π₀ rows). This is out of reach by design. Reaching it would mean letting face evidence into the T appraisal, which is the social-referencing dial of social-appraisal-synthesis.md §4, point 3.

## Limits
Small N, mostly men, one android, instructed rather than experienced contingency, 32 trials split over four cells (about 8 face trials per block × outcome), a text control that is a different "speaker". Effects in the mixed models have very large denominator df because 500-ms bins are entered as observations.

## Verdict: adopt (as evidence that a face's sign is read through its outcome for the observer; and as a falsifier marker for the design choice that face-borne outcome information reaches no display)
