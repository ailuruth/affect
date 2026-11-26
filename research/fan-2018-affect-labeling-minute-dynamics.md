# Does putting your emotions into words make you feel better? Measuring the minute-scale dynamics of emotions from online data (Fan et al.)

Rui Fan, Ali Varamesh, Onur Varol, Alexander Barron, Ingrid van de Leemput, Marten Scheffer & Johan Bollen, arXiv:1807.09725v1, 2018 (preprint; I did not check for a later journal version).

## What was read
The full arXiv text (26 pp.): data, detection of "I feel" statements, VADER scoring, the time series, curve fits, null-model confidence intervals, duration estimates, peak z-score mixture, gender split, discussion, methods. Figures read from captions and extracted numbers.

## Claims and evidence
- **Data.** 665,081 Twitter timelines (2006–2012). An affect label = "I feel / I'm feeling / I am feeling" + one of 10 unambiguous adjectives (positive: good, happy, great, awesome; negative: bad, unhappy, sad, terrible, horrible, awful), optionally boosted. 109,943 such statements; after filters (no retweets, no heavy oversharers, at most one label per 48 h, timezone known) 27,865 positive and 46,622 negative timelines. Every other tweet in ±6 h scored by VADER (−1 to +1), the label tweet itself excluded. 1-min bins, 10-min rolling mean; a CUSUM change-point test and a bootstrap against a null drawn from the same users at matched time of day and weekday.
- **Negative: slow build, fast drop after naming.** Valence departs from baseline about 63 min before "I feel bad" and returns within about 9–10 min after (CUSUM span −63 to +9 min; CI non-overlap −40 to 0). Post-label decay half-life about **5 min**.
- **Positive: fast rise, slower decay.** Span −38 to +53 min (CI non-overlap −10 to +20); half-life about **11 min**.
- Both ramps fit best by separate exponentials before and after t0 (better than Gaussian, Lorentzian or quadratic), which the authors read as feedback loops "affected or interrupted by the subjects' explicit expression".
- **Generalises across users:** per-user peak z-scores form a main component at −1.42 (68% weight) for negative and +1.32 (78%) for positive; about 17% of peaks run against the label's sign (VADER failures, irony, or real exceptions).
- Gender split: negative recovery looks faster for women, positive decay faster for men; the authors call this inconclusive.

**Limits, which matter here.** Observational. People may post "I feel bad" at the peak of an episode, so a drop afterwards is partly regression to the mean and the natural end of an episode; the design has no non-labeling control at matched intensity. Text valence is not felt emotion. Public posting is also a social act, so replies may do some of the work. The paper is suggestive about the time course, not proof of a causal labeling effect; Lieberman et al. 2011 supplies the causal evidence at the 5-s scale.

## What it means for the designs
1. **A naming route should act on the minute scale.** After a person names a negative state, text valence returns to baseline with a half-life of about 5 min (11 min for positive). For the agent's naming contraction (lieberman-2011), the matching implementation is: the contraction acts on the slow body variables (C, V), whose own τ is 10 min, so its effect is carried and dissipated by the body's dynamics, not by a 15-s face port. Expected effect: one naming utterance shortens an episode of concern by some minutes, not seconds and not hours.
2. **Negative and positive behave differently after naming,** with the negative recovery about twice as fast. A single symmetric κ is the simplest rule that fits the lab result; the observational asymmetry is a reason to give the contraction its own gain per valence only if a later test shows the same asymmetry in the agent's users.
3. **Negative states build for about an hour before people name them.** That is useful for initiative: in people, the naming comes late, after a long rise. An agent that waits for the user to name sadness will wait through most of the episode. The agent's own concern must be able to reach its bid threshold well before the user says anything, which the 10-min build in revision 2 does not deliver (the critique measured it).
4. **Evaluation target.** The paper's method (align on a naming event, compare to a matched null, fit exponentials before and after) can be applied to the agent's own logs: align on the agent's own naming utterances, compare concern trajectories against matched non-naming turns. A naming route that is working shows a post-utterance decay faster than the matched null, and a lesioned route shows none.

## Verdict
**adopt (time course, with the confound stated):** naming is followed by a return to baseline in minutes (half-life about 5 min negative, 11 min positive) after an hour-long negative build; observational and confounded by naming at the peak, so it sets the time scale of a naming route, not its existence.
