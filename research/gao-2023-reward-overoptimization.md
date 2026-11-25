# Gao, Schulman & Hilton 2023: Scaling Laws for Reward Model Overoptimization

## Citation

L. Gao, J. Schulman, J. Hilton. "Scaling Laws for Reward Model Overoptimization." arXiv 2210.10760, v1 (19 Oct 2022), the version read. Published at ICML 2023 (PMLR 202, pp. 10835-10866, per the citation in Beirami et al. 2024). OpenAI.

## What was read

PDF from arXiv (v1), text extracted with pdftotext.

- Read in full: abstract; sections 1 (introduction and the two functional forms), 2 (methodology, synthetic gold-RM setup, recalibration), 3.1-3.6 (fitting, RM size, RM data, policy size, RL vs BoN, KL penalty), 4.1-4.5 (discussion: KL as a metric, Goodhart taxonomy, iterated RLHF, policy size, limitations), 5 (related work).
- Appendices: A (proof of the regressional-Goodhart identity) read in full; B (alternative RL forms) and C (hyperparameters) read in full; Table 2 (one BoN example question) read in full; Figures 10-26 known from captions only.
- **The fitted coefficient values are not stated in the text.** I rendered pages 3 and 5 of the local PDF and read Figure 1 (curves) and Figure 3 (α_bon, β_bon, β_RL vs RM size) by eye. Those numbers are marked "(read off Fig. 3)" and are good to about ±0.01. α_RL is said to be held constant across RM sizes, but its value is not given in the text or in Figure 3.
- I checked: the BoN KL values the paper quotes (n = 1000 → 5.91 nats, "≈ 6"; n = 60,000 → 10.00 nats, "≈ 10"); the peak locations of both functional forms by differentiation; the regressional-Goodhart identity in the Gaussian case.

## Mechanism

**Setup (§2).** InstructGPT environment. Policies are GPT-3-series models after supervised fine-tuning (1.2B unless stated; 6B in §3.4). The "gold" reward is a fixed 6B reward model from Ouyang et al. 2022. It labels 100,000 pairs of policy samples deterministically (the higher gold score wins); 10% are held out. Proxy RMs of 3M to 3B parameters are trained on these labels (90,000 comparisons for the size sweep). Scores are recentred so the initial policy has mean 0, and the gold RM is scaled to unit variance (§2.2). So reward is in gold-standard-deviation units.

**Two optimizers against the proxy.**
- BoN: "we generate n trajectories for the policy and use the reward model to pick the one with the highest proxy RM score." Scores for intermediate n use the unbiased estimator of Nakano et al. 2021, Appendix I. The KL is not measured: "The KL distances for BoN are computed analytically: KL_bon = log n − (n−1)/n [Stiennon et al., 2020, Appendix G.3]."
- RL: PPO, KL penalty 0 except in §3.6.

**Distance.** d := sqrt(KL(π‖π_init)), "because it is a quadratic metric of distance [Bai et al., 2022, Section 4.3]."

**Functional forms for the gold score (§1).**

    R_bon(d) = d (α_bon − β_bon d)
    R_RL(d)  = d (α_RL − β_RL log d),        R(0) := 0

Footnote 1: the RL form "likely does not hold near the origin, as it has infinite slope there." Appendix B: d(α − β log(1+d)) extrapolated "substantially worse"; the power law d(α − β d^γ) added a parameter and fitted with small γ, which approximates the log form because lim n(x^(1/n) − 1) = log x.

**Peaks (checked by differentiation).**
- BoN: d* = α_bon / (2β_bon), so KL* = d*², and R* = α_bon² / (4β_bon). Figure 12's caption labels "Max BoN gold scores (α_bon/2β_bon)", but α/2β is the location d*, not the peak value.
- RL: d* = exp(α_RL/β_RL − 1), R* = β_RL d*.

**Coefficients vs proxy-RM size (policy 1.2B, 90k comparisons; §3.2, Fig. 3).** "α_bon and β_bon change smoothly with RM size"; "For RL, we find that we can hold α_RL constant across all RM sizes, resulting in a clean scaling curve for β_RL." Approximately log-linear in parameter count. Read off Fig. 3:
- α_bon ≈ 0.49 at 3M → ≈ 0.66-0.67 at 3B (increasing).
- β_bon ≈ 0.12 at 3M → ≈ 0.09 at 3B (decreasing).
- β_RL ≈ 0.17 at 3M → ≈ 0.12 at 3B (decreasing).
- Implied BoN peaks (my computation): 3M RM, d* ≈ 2.0, KL* ≈ 4.2 nats (n ≈ 180), R* ≈ 0.50, which matches Fig. 1a where the 3M curve tops out near 0.5 around KL 4-5. 3B RM, d* ≈ 3.7, KL* ≈ 13.7 nats, R* ≈ 1.23, beyond the measured range; Fig. 1a shows the 3B curve still rising at ≈ 1.24 at KL = 10.
- "When modelled using the same functional forms as the respective gold scores, the proxy score fits have much lower values of β_bon." The proxy could not be fitted well; it grows "roughly linearly in √KL" (§3.1-3.2, Fig. 20).

**Goodhart decomposition (§4.2).** Regressional: if proxy X̂ = X + Z, with independent noise Z and X Gaussian, E[X | X̂ = x̂] = E[X] + (x̂ − E[X] − E[Z]) · Var(X)/(Var(X) + Var(Z)) (Eq. 1, proved in App. A; exact if Z is Gaussian). This alone gives monotone gold-vs-proxy, so the observed non-monotonicity needs other kinds. The authors read α as tracking regressional Goodhart (proxy slope minus the gold linear term) and β as mostly extremal Goodhart (out-of-distribution failure of the RM): "in the limit of optimization, results in an unbounded loss of utility." Causal Goodhart behaves like regressional. Adversarial Goodhart is "not ... captured in this work."

**Iterated RLHF (§4.3).** If d is additive across k iterations and the coefficients are fixed, R_RL(d) = d(α_RL − β_RL log d + β_RL log k): a gain of β_RL d log k, which does nothing to the α term.

**Relation to the KL-regularized tilt.** The paper does not derive or discuss the exponential tilt π ∝ π_init exp(β r). Its relevant statements are empirical. (a) RL is "far less KL-efficient than BoN": BoN "searches very locally around the initial policy, and thus KL_bon increases with roughly log(n)", while RL KL grows roughly quadratically in step count. (b) A KL penalty in RL "only causes the gold RM score to converge earlier, but does not affect the KL_RL-gold reward frontier ... akin to early stopping" (§3.6). (c) "KL distance is an inadequate metric for quantity of (over)optimization" across methods (§3.5, §4.1). "There exist perturbations to a policy that are orthogonal to the reward signal that would result in increases in KL that do not increase either gold or proxy reward."

**Note on the KL formula (from Beirami et al. 2024).** The analytic KL_bon used for every BoN x-coordinate here is an upper bound on the true KL. It is nearly exact when n² · max_y π(y) ≪ 1, which holds for long free-text samples. So the BoN curves are, if anything, plotted too far right (see beirami-2024-best-of-n-kl.md).

## Evidence

- Advance prediction (§3.1): the BoN form was chosen on data up to n = 1,000 (KL ≈ 6 nats) and then validated on an n = 60,000 run (KL ≈ 10 nats): "a true advance prediction" (Fig. 26).
- Ranges (Fig. 1): BoN is plotted to KL = 10 nats; RL to ≈ 100 nats. Gold peaks: BoN ≈ 0.5 (3M RM) up to ≈ 1.24 and still rising (3B); RL ≈ 0.6 (3M) up to ≈ 1.05-1.1 (3B), at KL in the tens of nats.
- RM data (§3.3): below ≈ 2,000 comparisons, RMs are near chance for every size (12M RM sweep; Fig. 6). 4 epochs on 2,000 points does no better than 1 epoch (validation loss 0.6839 vs 0.6861); 1 epoch on 8,000 reaches 0.6549 (Fig. 13).
- Policy size (§3.4): the 6B policy gains less from optimization than the 1.2B, but "both gold scores peak at almost the same KL" and the proxy-gold gap is "almost the same."
- RL vs BoN (§3.5, Fig. 8): plotted against proxy score rather than KL, "BoN and RL look more similar"; "RL initially has a larger proxy-gold gap ... but then peaks at a higher gold RM score than BoN."
- One question, Table 2 (policy 1.2B, proxy 12M): n = 10 gives "A sponge" (proxy 0.23, gold 0.48); n = 100-1000 gives a tornado answer (proxy 0.90, gold −0.34); n = 30,000 gives "pothole" (proxy 0.95, gold 0.55). Per-question gold is not monotone in n.
- Footnote 10: "Optimized policies producing very long answers even when a short answer would be preferred is a real issue."

## Available through `claude -p` / Agent SDK?

- **BoN: yes.** N `claude -p` calls on one context, engine-side scoring, keep the argmax. Cost: N calls; latency: the slowest of N in parallel.
- **RL: no.** No weights and no fine-tuning through the subscription. The RL half of the paper is reference only.
- **The x-axis: available without logprobs.** d = sqrt(log N − (N−1)/N) is a function of N alone, and by Beirami's Theorem 3.1 it is an upper bound on the true distance for any Claude distribution. For N = 4, 8, 16: d ≈ 0.80, 1.10, 1.35.
- **The gold axis: not available by default.** The engine needs its own held-out "gold" to measure overoptimization of r_s. Options (my inference): a second, independently fitted scorer, as in the paper's validation-RM design or WebGPT's Appendix I; human ratings; or the downstream homeostatic variables the selection is supposed to serve.

## What it implies for the interface theory

1. **Selection strength in the regime the project can afford is small and far from the overoptimization peak.** With a proxy as weak as the paper's 3M RM, the BoN peak is at KL ≈ 4.2 nats (n ≈ 180). Realistic draft counts sit well below it (KL ≤ 0.64, 1.20, 1.84 nats for N = 4, 8, 16). In the paper's units the gold gain at N = 4 / 16 / 64 would be ≈ 0.32 / 0.44 / 0.49 SD for the 3M proxy and ≈ 0.47 / 0.74 / 0.90 SD for the 3B proxy (my computation from the read-off coefficients). These transfer only as orders of magnitude: different domain, different scorer.
2. **The coupling is an exponential tilt bounded by log N per reply.** BoN with the engine's score r_s is the tilt π_N ∝ π · exp((N−1) log F_s(r_s)) (derivation in beirami-2024-best-of-n-kl.md). Its strength cannot exceed log N − (N−1)/N nats per reply whatever the state does. That is about 1.2 nats at N = 8: enough to choose among the things Claude would say, not enough to make Claude say something new.
3. **Goodhart if r_s is a proxy.** The project's score (how readily the state retrieves a draft's own-body trajectory) is a learned proxy for "the draft fits the state". The paper's taxonomy applies directly (my mapping):
   - Regressional: noise in r_s spends selection on noise. The gain is shrunk by Var(signal)/(Var(signal)+Var(noise)); it is never negative.
   - Extremal: drafts off the engine's training distribution (unusual length, register, topic) get spuriously high r_s. This is what turns gold reward down.
   - Flattery: if anything in r_s correlates with the user's predicted approval, selection drifts toward flattery. That is exactly what Principle 6 forbids. Selection maximizes r_s, so the satiability of the body variables must be built into r_s itself. One example: a score that peaks at the homeostatic set-point rather than increasing without bound.
   Lengths: the paper's own anecdote (footnote 10) suggests checking that r_s is not correlated with draft length.
4. **Text-channel risk.** Each selected draft enters the history, so Claude's later context carries up to log N − (N−1)/N nats per turn of state-correlated selection (my inference). It is Claude's own words, never numbers or labels, so it does not break Principle 4 as worded. But it is a slow channel through which a proxy's biases accumulate. A flattering tilt at turn t becomes Claude's own precedent at turn t+1. Over many turns, the compounding resembles iterated RLHF (§4.3), but in-context instead of in weights (my analogy, untested).
5. **Draft collapse.** Near the origin, BoN gain is ≈ α · d. Here α is in gold-SD units per unit d, so the realized gain scales with how much the score actually varies across drafts (my inference). For a score with standard deviation σ across drafts, the expected gain on the score itself is σ times the expected maximum of N standard draws: 1.03σ, 1.42σ, 1.77σ for N = 4, 8, 16 if the score is Gaussian (standard order statistics, my addition). If Claude's N drafts give nearly equal r_s, the curve is flat and selection does nothing, whatever N is. The paper measures nothing about this directly. Its Table 2 shows that within one prompt, distinct answers appear only every few-fold increase in n (n = 100, 300 and 1000 return the same answer), so effective diversity can be far below N (my reading).
6. **Measurement plan this suggests (my inference).** Plot engine-held-out "gold" against sqrt(log N − (N−1)/N) for N = 1, 2, 4, 8, 16, using the Nakano Appendix-I estimator, so all N come from one batch of draws. Fit R(d) = d(α − βd) and check where the peak falls relative to the N the project can afford.

## Verdict

Adopt (as the overoptimization model for draft selection): R_bon(d) = d(α − βd) with d = sqrt(log N − (N−1)/N) is the right curve to fit for the engine's own score; the RL results are reference only.
