# Liking as a balance between synchronization, complexity and novelty (Ravreby, Shilat & Yeshurun)

Inbal Ravreby, Yoel Shilat & Yaara Yeshurun, *Scientific Reports* 12:3181, 2022, doi:10.1038/s41598-022-06610-z (PMC8873358). Preprint title: "Reducing synchronization to increase interest improves interpersonal liking". Data: OSF 6pbgf.

## What was read
The full PMC open-access text: introduction, results (Granger causality, novelty, the sync–complexity–novelty correlations, regression models, time-course analysis), discussion, and the full methods (participants, motion-energy analysis, segmentation algorithm, novelty, synchrony, entropy, liking, permutation tests, Bayes factors). Figures and the supplementary material (permutation distributions, max-cross-correlation re-analyses) were not seen.

## Findings, precisely

**Design.** 26 Israeli women, unacquainted, in three round-robin sessions (6, 10, 10 people) → 105 dyads, 104 analysed, 100 after outlier removal. Full-body **Mirror Game**, hands only, standing 50 cm apart, no talking, ~2 min (mean 119.8 s). Only instruction: move your hands "with as much coordination as possible"; no leader assigned. After each game, liking of the partner on a 0–100 scale. Motion energy (frame differencing, 29.97 fps), z-scored.

**Measures.** Synchronisation = Pearson correlation of the two motion-energy series at lag 0 (max cross-correlation as a check). Complexity = Shannon entropy of each person's motion-energy value distribution, averaged across the dyad. Novelty = mean Kolmogorov–Smirnov distance between each movement segment and all previous segments (segments cut at shared stopping points; mean segment ≈ 4 s).

**Results.**
- **Mutual influence, not leader–follower:** in 95 of 100 dyads each person's movement Granger-caused the other's; 5 were one-directional.
- **People chose novelty although told only to coordinate:** 99% of dyads more novel than a repetitive up-down reference (mean novelty 0.40, SD 0.04; low-novelty reference 0.32, d = 2.18; deliberately varied reference 0.46).
- **Trade-off:** synchronisation correlates **negatively** with complexity (r = −0.27, permuted p = .003) and with novelty (r = −0.32, p < .001); complexity and novelty correlate +0.39.
- **Liking:** synchronisation alone R² = **0.078** (F(1,98) = 8.28, p = .005); adding complexity R² = **0.149** (β_sync = 0.35, β_complexity = 0.28); adding novelty adds 0.5% (n.s., BF10 = 0.37). Fitted: Liking = −59.33 + 64.73 × Sync + 8.38 × Complexity. Complexity acts partly as a suppressor: it raises the sync weight.
- **Over time (median split, 50 v 50 dyads):** high-liking dyads were more synchronised for 55.9% of the game (significant at any time point only 1.2%), more complex for 79.6% (significant 15.7%), more novel for 90.2% (significant 10.7%).
- **Novelty rises within 2 min** in both groups (low-liking r = 0.82; high-liking r = 0.67); slope steeper in the low-liking group (6.34 × 10⁻⁴ vs 3.29 × 10⁻⁴ per s; z = 1.69, p = .045) but high-liking dyads start higher (intercepts 0.39 vs 0.35).

**What it does not show.** The title's "balance" is not an inverted U: synchronisation stays a **positive** linear predictor of liking. The claim is that sync and complexity trade off in behaviour and both add to liking. Entropy of a motion-energy value distribution is a coarse complexity measure (it is insensitive to temporal order). Women only; each person in many dyads (handled by permutation).

## What it means for the designs
1. **Even under an instruction to copy, people inject novelty into the joint trajectory, and pay for it in synchrony.** The mirror game is the most copy-favouring task possible, yet 99% of dyads avoided repetition. A design must contain a pressure **against repeating the joint trajectory** that persists while coupling is high — a drive on the dyad's history, not on the partner's current state. That is a concrete form of the "satiable drive" in open gap 7: repetition of a recent joint pattern should reduce its own future probability.
2. **The non-copying pressure grows within minutes.** Novelty rose over the 2-min game, faster in pairs that liked each other less. Required property: the anti-repetition term accumulates on a timescale of tens of seconds to minutes; its starting level and growth rate can differ by partner.
3. **Coupling and variety must both be present; neither alone suffices.** The measurable target: joint-motion correlation above surrogate **and** per-person movement entropy/novelty high, with the empirical trade-off (r ≈ −0.3) between them. A design that maximises correlation (copying) fails the second; one that maximises variety fails the first.
4. **Bidirectional influence.** 95% of dyads had mutual Granger causality: neither partner is purely a follower. An agent that only follows (copies with a lag) is the 5% case.
5. **Do not overclaim.** No evidence here that *more* synchrony reduces liking; the evidence is that people trade synchrony for variety and that variety adds independently to liking.

## Verdict
**adopt (constraint: anti-repetition of the joint trajectory, rising over minutes)** — 100 dyads show people sacrifice synchrony for novelty even when told only to coordinate, and that complexity adds to synchrony in predicting liking; synchrony itself is still positively related to liking, so the "too much synchrony" reading is not supported.
