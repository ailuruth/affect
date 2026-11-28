# Kory-Westlund & Breazeal 2019: a robot whose voice converges on a child's pitch and rate

Kory-Westlund, J. M. & Breazeal, C. (2019). "Exploring the effects of a social robot's speech entrainment and backstory on young children's emotion, rapport, relationship, and learning." *Frontiers in Robotics and AI* 6:54. doi:10.3389/frobt.2019.00054. Open: https://pmc.ncbi.nlm.nih.gov/articles/PMC7806080/ (CC BY). Entrainment code: github.com/mitmedialab/rr_audio_entrainer (GPL-3, not opened).

**How fully read:** the full text from PMC, from the abstract through the conclusion: background, design, entrainment method, all results sections and the discussion, including limitations. Table 2 (affect means by condition) lost its numbers in extraction. Figures were read by their captions. The reference list and supplement were not read.

Read for item 7 (how listeners respond to a converging synthetic voice). Levitan et al. 2016 (ISCA archive) and Lubold et al. 2016 (closed; HRI) were not reachable. Lubold's results are known here only from this paper's one-paragraph summary.

## What it says
- **Participants and design.** 86 children aged 3–8, one session each, in a 2 × 2 between-subjects design: Entrainment vs none × Backstory (the robot is said to hear poorly) vs none. The robot (Tega) was teleoperated. Its speech was a recorded human female voice, pitch-shifted up.
- **What the entrainment did.** This is held-level convergence on absolute values:
  - *speaking rate:* time-stretched to match the child's rate, between a floor and a ceiling;
  - *mean pitch:* first shifted to the mean F0 of children of that age, from a table, then shifted up or down per utterance according to whether the child's last utterance was higher or lower;
  - *volume and animation "exuberance":* set by the teleoperator at two fixed points, after judging the child as quiet or loud;
  - *pitch contour:* not adapted, because pilot tests sounded unnatural;
  - *latency:* the control condition went through the same processing, so the delay was matched.
- **Results.**
  - *Facial expressions (Affectiva Affdex, a classifier that outputs affect labels):* with entrainment, children showed more "joy", smiles, laughter and positive "valence", and fewer "fear" and "disappointment" outputs. Significant at p ≤ .004: disappointment F(1,70) = 14.7, laughter 8.94, valence 14.6. Joy, smiles, fear and attention were trends.
  - *Laughter over time:* more laughter in the first half of the session, which then decreased.
  - *Learning:* children in the no-entrainment condition identified *more* target words (F(1,77) = 5.47, ηp² = .07, near ceiling). Entrainment with backstory gave more use of target words in retelling (interaction F(1,59) = 9.45).
  - *Closeness:* no main effect of entrainment on closeness ratings. Children who rated the robot closer used more target words (rs = .36) and more of the robot's phrases (rs = .27).
- **Lubold et al. 2015–2018, as reported here:** pitch-adaptive robot voices raised learning in undergraduates and middle-school students but did not raise self-reported rapport. They compared an adapted voice with a flat TTS voice, confounding adaptation with expressiveness. This study controlled expressiveness.

## What matters for this engine
- **A converging synthetic voice draws more of the listener's smiles and laughter.** This is the one controlled result read on the question. With absolute pitch and rate matched to the listener, the listener's face shows more of the expressions an approval-seeking system would maximise.
  - It is a reason why the agent's voice coupling must never be *learned from* his reactions. A learner rewarded by his smiles or laughter would find convergence, and then more of it: Principle 6's flattery path, on the voice.
  - The build core's voice coupling is not learned from his face. The cone's diagonal is innate in form and scaled by ω, and ω follows word- and presence-based relief, not his expressions (new-core-search-15-synthesis.md §5).
- **Convergence did not buy closeness and cost recall.** No main effect on closeness was found, and word identification was worse. So listeners do not uniformly prefer it, and its benefits are not established.
- **Its method is the forbidden kind.** Matching absolute pitch through an age table plus the child's last utterance is a copy of the partner's habitual level and of his last value. Under the build core that is a held copy (rule 6, Lemma S\*) and a sampled-at-onset route (revision 3's K1/K2). The study shows what such copying does to a listener. It is not a design to adopt.
- **Labels.** The affect outcomes are classifier labels (Affdex). They are reported here as the paper uses them. Nothing in the engine would use such a classifier (Principle 1).

## Verdict: adopt (as evidence that convergence is a reward route if learned from his reactions); reject (as a mechanism)
Children, one session, a teleoperated robot, an affect classifier as the main social measure, unequal cells (16–28 per condition), many tests. Volume matching was manual and coarse.
