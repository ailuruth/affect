# Banse & Scherer 1996, "Acoustic profiles in vocal emotion expression"

Journal of Personality and Social Psychology 70(3):614-636. doi:10.1037/0022-3514.70.3.614.

Source read: the published PDF (University of Bonn course copy). Read in full: abstract, introduction including the review of prior acoustic findings and the component-process prediction method, Method, Recognition study, Acoustic analysis (regressions, residual scores, F0, energy, spectral energy distribution, speech rate), relation between judges' inferences and acoustic parameters, jackknifing and discriminant analysis, confusion-matrix discussion, and the General Discussion up to the treatment of confusions as similarity. Tables 6-9 were extracted as text and are partly garbled; numbers below are taken from the prose, not from the tables. The closing section on future research was skimmed.

## Claims
- Design: 12 professional German stage actors, 14 emotions chosen to include intensity pairs within a family (hot vs cold anger, panic fear vs anxiety, despair vs sadness, elation vs happiness) plus interest, boredom, shame, pride, disgust, contempt; 2 scenarios x 2 nonsense-like standard sentences. Actors imagined a scenario and spoke "when they actually felt the intended emotion". From 1,344 recordings, 224 were selected for acoustic analysis (2 per cell, most recognizable, preferring two different actors). Three actors furnished 88% of the selected male portrayals: actor and emotion are partly confounded, and the authors analyse z-residuals with sex and actor identity partialled out.
- 29 acoustic parameters, all continuous: F0 mean, SD, 25th and 75th percentiles; mean log energy; duration of articulation and of voiced periods (inverse tempo); voiced long-term average spectrum in 9 bands (125 Hz to 8 kHz); Hammarberg index; spectral slope above 1 kHz (DO1000); proportion of voiced energy below 500 Hz and below 1 kHz; unvoiced spectrum in 9 bands.
- Variance: speaker identity accounted for more variance than speaker sex in every domain except F0. After sentence, sex and speaker were removed, emotion still explained 55% of the variance in mean energy and 50% in mean F0; lowest for the 300-800 Hz and 5-8 kHz voiced bands.
- F0 is highest for the "intense" emotions (despair, hot anger, panic fear, elation), lowest for contempt and boredom. Energy correlates r = .62 with F0 and follows the same order, except shame and sadness, which are mid-range in F0 but lowest in energy. Contempt has very low F0 and low energy, read as a dominance display with controlled arousal (Morton 1977).
- Spectral balance follows the predictions in pattern though smaller in size (about 0.5 SD less than predicted). Sadness has a high share of low-frequency energy: low coping potential (a lax voice) outweighs unpleasantness (a narrow, tense voice) when the two mechanisms conflict.
- Tempo: sadness slowest; hot anger and panic fast; happiness, predicted slower, came out faster (actors portrayed an active form).
- Theory route: predictions are derived per appraisal check (component process model, Scherer 1986), each check mapped to a physiological change in respiration, phonation and articulation, and the per-emotion profile is the sum of check outcomes. Example: appraising an object as intrinsically unpleasant gives faucal and pharyngeal constriction and tensed tract walls, hence more high-frequency energy, rising F1, falling F2 and F3, narrower F1 bandwidth. Most predictions held; failures (contempt, anxiety, shame, disgust, hot anger, elation for F0) are used to revise the theory.
- Judges and acoustics: judges reached 48% over 14 categories (chance 7%), 55% when within-family confusions count as correct. Hot anger 78%, boredom 76%, interest 75%; shame 22%, disgust 15%. Disgust and shame are argued to be expressed by affect bursts ("yuck") or by not speaking, not by a sentence-length voice.
- Beyond arousal: judges differentiate valence or "quality" from the voice, not only arousal.
- Statistical classification of the 16 best parameters: jackknifing to mean profiles 40%; discriminant analysis 53% fitted on all cases, 25% under rotating 7/8 cross-validation. Confusion patterns of judges and statistics resemble each other, but per stimulus the two are unrelated (correlation between judge recognition and jackknife hit r = .04): the same aggregate accuracy from different cues or prototypes.

## Evidence with numbers
- n = 224 portrayals (223 after removing one), 12 actors, 12 judges.
- Emotion R^2 (after removing speaker): mean energy .55, mean F0 .50.
- Judges 48% (55% families collapsed); jackknife 40%; DA 25-53%.
- Multiple R between the 7 forced acoustic predictors and judges' use of each category: hot anger .63, sadness .49, happiness .27; non-significant for cold anger .16, interest .18, disgust .17.

## What it implies for an engine whose voice is driven from an internal state through an innate vocal body
- The mechanism, not the labels, is what carries over. Scherer's route is state -> physiological settings of breathing, larynx and tract -> acoustics. In the engine that becomes: latent state -> innate vocal-body parameters (subglottal pressure / loudness, vocal-fold tension / F0 level, F0 variability, glottal adduction / spectral tilt, tract constriction / formant shifts, articulation rate) -> sound. No emotion category sits in the path (Principles 1-2). The 14 labels in this study are the experimenters' stimuli, not engine variables.
- Two separable axes of the voice body, supported here: an activation axis (F0 level, F0 spread, energy, tempo move together; r = .62 between F0 and energy) and a quality axis carried by spectral balance and voice quality (low-frequency share, Hammarberg index, slope above 1 kHz) that can move against activation (sadness: mid F0, lowest energy, most low-frequency energy). A voice body with only pitch and rate controls (macOS `say`, Kokoro) cannot express the second axis.
- Conflicting mechanisms combine additively in the theory, and the data say which wins (coping potential beat unpleasantness for sadness). In the engine, two body drives acting on one actuator (tension vs laxness) should sum on the actuator, not be arbitrated by a label.
- Speaker identity explains more variance than sex: a person's own baseline dominates. Perceiving the operator's voice must be relative to the operator's running baseline (z-scores per speaker), exactly as the paper's residual analysis does. Same for the engine's own voice: its affective range is a deviation from its innate baseline.
- Some states do not live in sentence prosody at all (disgust, shame). The innate vocal body should include non-speech bursts and the option of silence, not only a modulated TTS sentence.
- The per-stimulus dissociation between judges and classifier (r = .04) is a caution for evaluation: matching an aggregate confusion pattern does not show the same mechanism.

## License
APA, all rights reserved; copy from a university course page. No code or data released.

## Verdict: adopt (as the mapping from appraisal-driven physiology to acoustic parameters, and the parameter list)
Actor portrayals selected for recognizability exaggerate differences; treat the effect sizes as upper bounds for spontaneous speech.
