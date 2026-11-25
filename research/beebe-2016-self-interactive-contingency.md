# Beebe, Messinger, Bahrick, Margolis, Buck & Chen 2016, "A systems view of mother–infant face-to-face communication" (Developmental Psychology 52(4):556-571, doi:10.1037/a0040085); stand-in for Tarabulsy, Tessier & Kappas 1996

Source read: Beebe et al. 2016, full text (34-page accepted-manuscript layout from a University of Miami course host): introduction, method, results (Tables 1-3) and the first part of the discussion. The online supplement (model tables) was not read.

Tarabulsy, Tessier & Kappas 1996, "Contingency detection and the contingent organization of behavior in interactions: implications for socioemotional development in infancy" (Psychological Bulletin 120(1):25-41, doi:10.1037/0033-2909.120.1.25), was NOT read. No open copy exists (Semantic Scholar: closed; Crossref: no abstract; APA PsycNET needs a login). Only its PubMed abstract was read. It reviews four groups of studies: infants detect contingencies unrelated to their behaviour; infants detect contingencies involving their behaviour; contingency as a way to describe behavioural organisation in parent-infant interaction; and links between early contingency and later socioemotional outcomes. Beebe et al. use its definition of contingency ("a temporal relation between the occurrence of two events ... that involves sequential coordination"), and they also cite it for the event-based distinction between "responsiveness" (given A, B follows) and "dependency" (B occurs only after A), which is Watson's sufficiency vs necessity. Beebe et al. is used here because it states the time-series method in full, and the method is what matters for the engine.

## Claims
- Two kinds of contingency are estimated together, each controlling for the other: self-contingency, a person's current behaviour predicted from their own prior seconds (autoregression); and interactive contingency, a person's current behaviour predicted from the partner's prior seconds (lagged cross-regression).
- In 4-month mother-infant face-to-face play:
  1. Both kinds are significant in 7 of 8 modality pairings.
  2. Interactive contingency is bidirectional but asymmetric: mothers coordinate with infants more than infants with mothers.
  3. Self-contingency is far larger than interactive contingency.
  4. Across dyads, self- and interactive contingency are negatively correlated in some modalities: less self-stable individuals coordinate more with the partner. The authors read this as a homeostatic balance.
- Most earlier work controlled autocorrelation as a nuisance. Here it is treated as a variable: "it is not appropriate to conceptualize interactive processes without simultaneously accounting for dynamically interrelated self-organizing processes."

## Evidence with numbers
- 132 low-risk dyads (152 recruited at birth), first 2.5 min of uninterrupted play, coded per second on ordinal scales: gaze on/off, facial affect (infant 5 levels, mother 9), infant vocal affect, orientation, touch, and an algorithmic facial-visual engagement composite. Kappas .68-.90. 19,800 s per partner per modality.
- Model (Chen & Cohen 2006; SAS PROC MIXED, GLIMMIX for gaze): for each person and modality, y_i(t) = a + b_self·ȳ_i(t−1..t−3) + b_int·ȳ_j(t−1..t−3) + controls. Here ȳ is a weighted mean of the prior 2-3 s, weighted by each lag's significant beta. Both coefficients enter the same model, and random effects allow per-dyad mean, slope and autoregression.
- Lag lengths found: mothers 2-3 s for both kinds. Infant self-contingency 1-4 s by modality. Infant interactive contingency up to 6 s for gaze and 5 s for face, but 0 s for mother orientation → infant head (a same-second effect).
- Standardized effects (Table 2; 95% CIs exclude zero unless noted):
  - Infant coordination with mother: gaze .025, face .038, face→vocal .030, engagement .024, orientation .050; touch pairings n.s.
  - Mother coordination with infant: gaze .061, face .139, vocal→face .073, engagement .136.
- Self vs interactive (standardized): mother face self .529 vs interactive .139, about 4:1. Mother gaze 5:1, touch 24:1, orientation 52:1. Infant head 12:1, face 16:1, gaze 25:1.
- Signs: all positive (mutual mirroring of direction of change), except orientation, where mother looming in → infant turns away ("chase-dodge"), and infant turning away → mother sits back.
- Negative self-vs-interactive covariance across dyads, significant in 4 of 8 pairings for mothers (e.g. facial affect r = −.431) and 3 of 8 for infants; none for gaze or touch.

## Mechanism
A bivariate lagged autoregression, a vector-autoregressive (Granger-style) decomposition estimated across dyads. "Interactive contingency" is the partner's lagged effect after the person's own lags are partialled out. It is not an intervention-based estimate: it cannot separate a true partner-to-self influence from a common driver of both partners, and same-second effects (lag 0) carry no direction.

## What it implies for an engine that learns a partner model and its own self–other face map from contingencies in live interaction
- This is the minimum correction for the critique's confound (C13). The design learned R by regressing the partner on the agent's own trace, without the partner's own past in the model. If the partner is autocorrelated and the agent follows the partner, the agent's recent state carries the partner's recent state, which predicts the partner's next state; the regression credits that to the agent. Putting the partner's own lags in the same regression (b_self for the partner) removes the route that runs through the partner's autocorrelation. Putting the agent's own lags in its own self-model does the same in the other direction. Strictly lagged regressors, both histories, one model.
- It is not sufficient. Partialling out both histories still leaves common drivers (the conversation topic, the room, a third person) and same-second coupling, and closed-loop estimates remain biased when the agent's following is fast. The engine should add an exogenous instrument, such as its own spontaneous micro-variations, which are not caused by the partner (see watson-1997-contingency-two-indices.md and rochat-morgan-1995-spatial-self-perception.md).
- Realistic sizes. In natural face-to-face play the partner's effect on the other is small: β of about .02-.14 per SD, against self-effects of .5-.6. A learned partner gain of order 1 or above (critique C13: R = 9.5) is far outside anything measured in human dyads. Use these figures as a prior and a sanity bound on the learned partner map, per channel.
- Asymmetry. Even at 4 months, the caregiver follows the infant about 2.4 (gaze), 3.7 (face) and 5.7 (engagement) times more than the reverse. If the engine is in the infant's position (a learner with a responsive operator), most of the cross-correlation it sees is the operator following it. That is the true partner→agent contingency it should learn, but the same data also contain the agent's own following, so the direction has to be estimated, not read from the correlation.
- Lag windows differ by channel: gaze and face responses run 3-6 s for infants, 2-3 s for mothers, and orientation is same-second. The engine's partner model should estimate the lag window per channel, not assume one.
- The negative self-vs-interactive covariance suggests a design check: an engine whose own expressive dynamics are very stable should coordinate less, and one with labile dynamics more. If the partner gain and the self-stability of the engine's face are set by independent knobs, this human pattern will not emerge.

## License
APA journal article, all rights reserved; author-distributed manuscript.

## Runs on this Mac without a GPU?
Yes. A per-channel lagged regression with both histories is a few hundred multiply-adds per second.

## Verdict: adopt (estimate self- and interactive contingency in one lagged model as the minimum partner-model estimator; use the measured effect sizes as a prior), with the caveat that it is observational and not robust to common drivers
Tarabulsy et al. 1996 stays unread (abstract only); look for it through a library if the event-based statistics (conditional probabilities, base rates, Yule's Q, lag-sequential analysis) are needed.
