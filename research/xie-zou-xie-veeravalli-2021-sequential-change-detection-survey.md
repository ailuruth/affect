# Sequential (quickest) change detection: classical results and new directions (Xie, Zou, Xie & Veeravalli)

Liyan Xie, Shaofeng Zou, Yao Xie and Venugopal V. Veeravalli, *IEEE Journal on Selected Areas in Information Theory* 2(2), 2021; arXiv:2104.04186v1 (9 Apr 2021), 22 pp. https://arxiv.org/abs/2104.04186

## What was read
arXiv v1, extracted text: §I–IV **in full** (problem, CUSUM, SR, Shewhart, minimax and Bayesian optimality, GLR/mixture, EWMA; non-i.i.d. asymptotics; change-of-measure ARL approximations; non-stationary and multiple changes, transient dynamics, moving anomalies; robust and adversarial detection; data-efficient detection; high-dimensional streams; detection–isolation; alternative metrics; machine-learning, distribution-free, bandit and optimisation directions). §V (applications) and §VI skimmed. References used only for pointers.

## What it says, precisely
- **Lower bound (their Theorem 1, from Lai 1998):** inf_{FAR ≤ α} CADD ≥ |log α|/D(f₁‖f₀)(1 + o(1)); CUSUM with b = |log α| attains it for Lorden's and Pollak's criteria; "the FAR decays to zero exponentially with exponent D(f₁‖f₀)" against delay (Fig. 2, slope 1/D).
- **Shewhart's chart is optimal for a different criterion:** maximising the probability of detecting the change at the moment it occurs subject to FAR (Pollak & Krieger). Without memory it loses information on small changes.
- **Non-i.i.d. data (§III-A):** the generalised CUSUM on conditional log-likelihood ratios is first-order optimal when (1/t)ΣY_i → I completely; I replaces the KL. Linear regression, GARCH and hidden-Markov cases are cited.
- **GLR (§II-E):** sup over the post-change parameter; not recursive in general; window-limited GLR (Willsky & Jones; Lai 1995, 1998) is asymptotically optimal "if the window size is carefully chosen as a function of FAR".
- **Transient changes and nuisance changes (§III-C):** dynamic CUSUM and weighted dynamic CUSUM are recursive, first-order optimal and adaptive to unknown transient durations. A **nuisance change** (one that must not raise an alarm) can be modelled as a transient phase.
- **Robustness (§III-D):** minimax-robust CUSUM uses the least favourable pair of distributions in the uncertainty classes (Huber; exact optimality under a generalised Lorden criterion when the classes are jointly stochastically bounded). **Adversarial attacks** are treated only in the sensor-network sense: compromised sensors, handled by waiting for L local CUSUMs.
- **Distribution-free (§IV-B):** kernel MMD, nearest-neighbour statistics, and martingale tests with thresholds from a non-asymptotic law of the iterated logarithm, for data whose law is not modelled.

## What matters for this engine
1. **Nuisance change.** The start-of-session step from b_id to today's level, and ordinary slow drifts of his face, are nuisance changes that must not engage the governor; the survey's framing (treat them as transient phases, or remove them by invariance) matches revision 2's start rule and the batch centring in the pass-12 check.
2. **Window-limited GLR with the window set by the FAR** is the textbook form of "keys with several memories": revision 2's 1/5/30-min memories are a coarse grid of such windows.
3. **No source treats a change chosen by an adversary to evade the detector** beyond the change-time adversary of Lorden/Moustakides; the evasion floor in the synthesis is derived there, not taken from the literature.
4. **Heavy tails and an unmodelled pre-change law** point to empirical calibration (or a distribution-free martingale threshold), not to the Gaussian formula.

## Verdict
**adopt (as the second survey and for the nuisance-change and window-limited GLR framings).**
