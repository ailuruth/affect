# Striano, Henning & Stahl 2005, "Sensitivity to social contingencies between 1 and 3 months of age"

Developmental Science 8(6):509-518.

Source read: the published PDF (Wayback Machine copy of the Max Planck EVA author repository file Striano_Sensitivity_DevScience_2005_1555283.pdf), read in full except the last paragraph of the general discussion and the references.

## Claims
- At about 6 weeks, infants did not discriminate between three kinds of imperfect maternal contingency: Normal, Non-Contingent (the mother re-performs her own recorded speech from a week earlier) and Imitation (the mother copies the infant's facial expressions, gestures and vocalizations).
- At about 3.5 months the same infants did discriminate. They gazed most when the mother imitated them but smiled most in normal reciprocal interaction, and smiled least when imitated.
- Interpretation: attention and affect are separate systems. Imitation "captured infants' visual attention and may have modulated arousal by providing a higher degree of contingency compared to the more reciprocal Normal or Non-Contingent interaction", but did not raise affect. Infants smile most at a familiar, intermediate level of contingency: Normal is familiar, Imitation is "likely higher than the familiar level", Non-Contingent lower. This is framed as support for Watson's shift from preferring perfect to preferring high-but-imperfect contingency around 3 months.

## Evidence with numbers
- Study 1: n = 68 (M = 45.2 days, range 36-58); 11 excluded. Face to face, not video. Visit 1: 3 min of normal play, with 60 s of the mother's speech recorded. Visit 2 (about 6.9 days later): 60 s in each condition, counterbalanced in six orders. In Non-Contingent, the mother heard her visit-1 recording through headphones and repeated it (about 25 utterances, one every 2.4 s).
- Study 2: n = 66 of the same infants at M = 109.8 days (88-128); 13 excluded; 90 s per condition.
- Manipulation check: a blind observer identified the condition with κ = .85 (Study 1) and .95 (Study 2). Coder κ = .71-.83 for infant gaze and smile. A coder blind to the mother's image agreed with the original gaze coding at κ = .73/.76.
- Study 1, % of time, Normal / Imitation / Non-Contingent: infant gaze 68.7 / 63.2 / 64.9; infant smile 6.4 / 4.2 / 6.6; no condition effects (ps > .22 and > .56). Mothers smiled less in Imitation than in Non-Contingent (p = .004). Independent of condition, infants gazed more when mothers smiled more (GLMM F(1,174.9) = 7.12, p = .008, β = .3).
- Study 2, % of time: infant gaze 75.9 / 83.0 / 70.4, F(2,120) = 8.44, p < .001; Imitation > Normal (p = .018) and > Non-Contingent (p = .001); Normal > Non-Contingent at trend (p = .055). Infant smile 12.4 / 5.9 / 9.3, F(2,120) = 8.79, p < .001; Normal > Imitation (p < .001) and > Non-Contingent (p = .052); Non-Contingent > Imitation (p = .015). Controlling for maternal smiling, Normal still exceeded both (p < .001, p = .043). Mothers smiled least in Imitation (p = .022, p = .001).
- A Condition × Order interaction on smiling (p = .048) was explained by carry-over from Non-Contingent.
- Limits: the main coder was not blind to condition (a quad-split image was used). Mothers did not fully comply in Imitation: they smiled more than their infants. Periods were short (60-90 s). The authors say the design cannot assess directionality.

## Mechanism
Not modelled. The working account is Watson's and Gergely's contingency-detection module: an early bias toward perfect contingency is re-set around 3 months toward high but imperfect contingency, the level typical of social partners. Being imitated delivers above-familiar contingency. That raises orienting (gaze) but not positive affect. Reciprocal, partly independent responding (Normal) is what raises smiling.

## What it implies for an engine learning a partner model and its self–other face map from live contingency
- This is the reverse of the critique's confound, measured in infants. Here the partner follows the agent (the mother imitates the infant), and 3-month-olds respond to it differently from reciprocal interaction. Maximal partner-follows-me contingency is not treated as the best social contingency: attention goes up and affect goes down. An engine should likewise not read "the partner copies me closely" as "the partner is highly responsive to me" in its affect. A near-perfect follower sits close to the self signature (see stoytchev-2011-self-detection-temporal-contingency.md: both indexes near 1). The engine's partner model needs a contingency level, not just a direction, and the social optimum is intermediate.
- Watson's two indexes give the signature. In Imitation, P(partner act | my act) is high and P(my act before | partner act) is also high, because the mother acts mostly when the infant does. In Normal, the first is high and the second lower, because the mother also initiates. The engine can compute both per channel and treat "both high" as copying or self, "first high, second moderate" as a reciprocal partner, and "both low" as an independent other.
- Being imitated is still informative for the face map. Associative sequence learning (ray-heyes-2011-wealth-of-the-stimulus.md) needs exactly the contingent pairing of the agent's own act with the partner's matching act. The attention increase is consistent with imitation being a privileged learning signal for the self–other map, separate from what drives affect. This fits Principle 6 in brief.md: the engine should learn the mapping from being imitated without being rewarded by it.
- The 1-month null shows these discriminations need development. An engine should not expect its contingency estimates to separate partners until it has accumulated enough of its own act history.
- Use controlled partner conditions as an evaluation battery: a human tester who (a) interacts normally, (b) re-performs an earlier recording, or (c) imitates the engine. The engine's learned partner-responsiveness and its affect readouts should order these conditions the way 3-month-olds do. If the engine's affect peaks under imitation, it is being rewarded by being copied.

## License
Blackwell/Wiley journal article, all rights reserved; author-repository copy.

## Runs on this Mac without a GPU?
n.a. (empirical study).

## Verdict: adopt (as evidence that being followed is distinguished from reciprocal response by 3 months, with attention and affect dissociating; and as a three-condition test battery)
One lab, face-to-face rather than video, non-blind main coder, short periods; the Non-Contingent condition is a re-performance, not a true replay.
