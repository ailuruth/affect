# Interpersonal physiological synchrony during dyadic joint action is increased by task novelty and reduced by social anxiety (Boukarras, Placidi, Rossano, Era, Aglioti & Candidi)

Citation: S. Boukarras, V. Placidi, F. Rossano, V. Era, S. M. Aglioti, M. Candidi. "Interpersonal Physiological Synchrony During Dyadic Joint Action Is Increased by Task Novelty and Reduced by Social Anxiety." *Psychophysiology* 62(3):e70031, 2025. doi:10.1111/psyp.70031. PMC11913774.

Source read: the PMC full text, HTML text-extracted. Read in full: abstract, Introduction, Methods, Results, Discussion, Limitations, Conclusion. **Not read:** the Supporting Information (lag-group figures S1–S5, full model tables, behavioural models S1–S2).

## The study
- **Design.** 40 same-sex unacquainted dyads (80 participants; masks worn, COVID period). 4-min baseline with a panel between them, then 16 blocks (20 trials, ~5 min) of a joint grasping task: grasp bottle-shaped objects as synchronously as possible, imitatively ("same") or complementarily ("opposite").
  - **Free blocks:** both hear the same instruction and must coordinate without talking.
  - **Leader–follower blocks:** only the leader hears where to grasp; the follower must watch and imitate or complement. Roles swap after four blocks.
- **Synchrony measure.** Inter-beat intervals at 4 Hz; each series pre-whitened by auto-ARIMA (d = 1, seasonal D = 1, Box–Cox); cross-correlation of residuals at lags ±3 s (±12 samples). Control: 13,260 pseudo-dyads (participant shuffling).

## Results
- **Synchrony is above chance only in interaction.** Real > pseudo dyads during the task; no difference at baseline. (The reported means for REAL and PSEUDO appear swapped in the text; the t-test and the figure support real > pseudo.)
- **No lagged leader → follower synchrony.** The authors expected the leader's physiology to predict the follower's at positive or negative lags. Instead, in both Leader 1 and Leader 2 blocks, cross-correlation peaked at zero lag (−4…+4 samples, i.e. ±1 s) with no difference between positive and negative lags (P = 0.327, P = 0.622) — the same pattern as free blocks.
- **Novelty raises synchrony.** Blocks that switched to a new task version had higher synchrony than repetitions (b = −0.187 for old vs new, P = 0.005). Pseudo-dyads showed no novelty effect, so it is not shared task context.
- **Dyad-level social anxiety lowers synchrony** (β = −0.20, P = 0.005); the absolute-difference terms were not significant, so it is both members' sum.
- **No link to behavioural synchrony** (grasp-time difference P = 0.23; start-time difference P = 0.80), and none to any subjective rating. HRV (rMSSD change) rose in new blocks and with perspective taking.
- **Interpretation offered.** Synchrony reflects reciprocal attention and performance monitoring, not behavioural alignment; socially anxious people's self-focused attention removes the conditions for it.
- **Limits stated.** Exploratory; masks hid faces; one synchrony method; small sample.

## The mathematical object
Read for dynamics:
- **Not a leader–follower coupling.** A one-way driven system (follower = filter of leader) predicts lagged cross-correlation. With an imposed information asymmetry, the observed synchrony was still at zero lag and symmetric. What fits is a **common-cause structure**: both bodies respond, within about a second, to a shared state of the interaction (uncertainty about the joint task), not to each other's physiology.
- **The gate is attention to the other**, raised by shared uncertainty (novelty) and removed by self-focus (anxiety). Synchrony is a consequence of both agents allocating precision to the joint task at the same time.

## What it means for the design
1. **Synchrony is not evidence of following.** A design need not, and should not, produce physiological synchrony through a self ← partner coupling. Coincident body responses to shared uncertainty already produce it at zero lag. That supports keeping copying out of the core while still predicting synchrony on recorded dyads.
2. **Shared uncertainty, not the partner's state, is the common driver.** An engine whose own body responds to its own uncertainty about the joint exchange would synchronise with a partner who does the same, with no partner-to-body route.
3. **Evaluation consequence.** Zero-lag synchrony cannot separate "coupled" from "co-driven"; lag asymmetry did not appear even with imposed roles. This matches the index's cautions (butler-randall-2013, timmons-2015).

## Verdict
- **adopt (as evidence and as a constraint on dynamics).** Heart-rate synchrony under imposed leader–follower roles is symmetric and at zero lag, modulated by shared novelty and self-focus. Small exploratory study; masks; supplementary tables not read.
