# Nakano, Hilton, Balaji et al. 2021: WebGPT: Browser-assisted question-answering with human feedback

## Citation

R. Nakano, J. Hilton, S. Balaji, J. Wu, L. Ouyang, C. Kim, C. Hesse, S. Jain, V. Kosaraju, W. Saunders, X. Jiang, K. Cobbe, T. Eloundou, G. Krueger, K. Button, M. Knight, B. Chess, J. Schulman. "WebGPT: Browser-assisted question-answering with human feedback." arXiv 2112.09332, first posted December 2021; version read: v3 (1 Jun 2022). OpenAI.

## What was read

PDF from arXiv (v3), text extracted with pdftotext.

- Read in full: abstract; sections 1 (introduction), 2 (environment), 3 (data collection; training: BC, RM, RL, rejection sampling), 4 (evaluation on ELI5, TruthfulQA, TriviaQA pointer), 5 (comparison of training methods; scaling), 6 (discussion: truthfulness, perceived truthfulness, bias, references, live-web risks), 7 (related work), 8 (conclusion).
- Appendices read in full: E (hyperparameters, early-stopping KLs, Tables 5-8) and I (the best-of-n estimator), because they bear on mechanism and numbers. Also read: A (environment details), B (question datasets), C (data collection, agreement rates), F (minimal comparison instructions), G (TriviaQA), H (question stance, reference-point bias), K (dataset release).
- Skimmed: D (contractor survey), J (example answers).
- Figures 2-8 survive in the text only as captions and axis ticks. Bar heights and curve points not stated in the text were not read. The numbers below are the ones the text states.
- I checked the Appendix I identity (the order-statistic weights C(i−1, n−1)/C(N, n)) by the counting argument below.

## Mechanism

**Pipeline (§3.2).** GPT-3 760M, 13B and 175B, fine-tuned four ways:
1. Behavior cloning (BC) on ≈ 6,000 human demonstrations (6,209 in Table 4).
2. A reward model (RM), initialized from BC, trained on ≈ 21,500 pairwise comparisons (21,548), of which ≈ 16,000 were used for training and 5,500 held out. The reward "represents an Elo score ... the difference between two scores represents the logit of the probability that one will be preferred"; 1 point = sigmoid(1) ≈ 73% preference (§5.2).
3. RL: PPO against the RM score at episode end plus a per-token KL penalty from BC (coefficient 0.02, Table 7).
4. Rejection sampling, i.e. best-of-n: "We sampled a fixed number of answers (4, 16 or 64) from either the BC model or the RL model ... and selected the one that was ranked highest by the reward model ... which requires no additional training, but instead uses more inference-time compute."

**The best-of-n distribution.** This paper does not write it down. For the exact form see beirami-2024-best-of-n-kl.md: π_n(y) = F(y)^n − F⁻(y)^n, which in the continuous no-ties case is n F(r(y))^(n−1) π(y). It is an exponential tilt of π by the log-quantile of r with strength n−1, and KL(π_n‖π) ≤ log n − (n−1)/n, with near equality for long free-text answers. For n = 4, 16, 64: ≤ 0.64, 1.84, 3.17 nats (my computation).

**Estimator for best-of-n performance (Appendix I).** Draw N ≥ n answers per question and sort them by training-RM score: S_1 ≤ ... ≤ S_N. The unbiased estimate of the validation-RM score of best-of-n is

    R̂_n = Σ_{i=n}^{N} [ C(i−1, n−1) / C(N, n) ] · R_val(S_i)

Reason (checked): of the C(N, n) size-n subsets, exactly C(i−1, n−1) have S_i as their maximum, namely those that contain S_i and n−1 of the i−1 lower-ranked answers. Averaging over all subsets is unbiased by linearity. One batch of N draws gives curves for every n ≤ N. The training RM selects and a separate validation RM scores, "to try to account for the original reward model being overoptimized." Gao et al. 2023 use this estimator for all their BoN curves.

**Relation to the KL-regularized optimum.** The paper does not derive any tilt formula. RL here is explicitly KL-regularized, "to mitigate overoptimization of the reward model" (§3.2). Its early stopping is "based on the reward model score for some KL budget", with KL "measured from the BC model, and summed over the episode" (App. E). Stopping points (Table 8): 760M at 10.5 nats, 13B at 6.8 nats, 175B at ≈ 12 nats per episode.

## Evidence

- **Headline (abstract, §4.1).** The 175B BC + best-of-64 model is preferred 56% of the time to human demonstrators and 69% to the top-voted Reddit (ELI5) answer. Ties count as 50%. For comparison, Krishna et al. 2021's best model was preferred 23% of the time to the reference answers. Error bars are ±1 SE (Fig. 2; bar values per model size not given in the text).
- **Compute-efficient n (§4, §5.2, Fig. 8).** The evaluated models are 760M best-of-4, 13B best-of-16 and 175B best-of-64: "the Pareto frontier of this trade-off". "It is generally compute-efficient to use some amount of rejection sampling, but not too much." Larger models warrant larger n.
- **BoN vs RL (§5.1, Figs. 4-5).** "Rejection sampling provides a substantial benefit, with the 175B best-of-64 BC model being preferred 68% of the time to the 175B BC model. Meanwhile, RL provides a smaller benefit, with the 175B RL model being preferred 58% of the time to the 175B BC model." Fig. 4 caption: "RL slightly improves preference, but only when not using rejection sampling."
- **Both together.** "The combination of RL and rejection sampling also fails to offer much benefit over rejection sampling alone." Reasons offered: both optimize the same RM, which "can easily be overoptimized (especially by RL)"; and "RL reduces the entropy of the policy, which hurts exploration." So RL was dropped from the final models "for simplicity" (§4). RL was "some benefit when inference-time compute is more limited" (§1).
- **Why BoN beat RL, the authors' list (§5.1).** More inference-time compute; hindsight over an unpredictable environment ("the model can try visiting many more websites"); the RM was trained mostly on BC and rejection-sampling outputs, which "may have made it more robust to overoptimization by rejection sampling than by RL"; RL needs tuning, rejection sampling does not. Also, tuning the BC baseline (epochs, temperature 0.8) "alone closed much of the gap we originally saw between BC and RL."
- **KL efficiency (my comparison, not made by the paper).** The 175B RL policy was stopped at ≈ 12 nats per episode and won 58% against BC. Best-of-64 is ≤ 3.17 nats by the analytic bound and won 68%. That is a larger gain at about a quarter of the KL, the same pattern Gao et al. 2023 report as "RL is far less KL-efficient than BoN."
- **Validation-RM prediction (Fig. 5).** The Appendix I estimator "predicts human preference well for n ≤ 64, although we expect it to overestimate human preference for sufficiently large n, as the validation reward model will eventually become overoptimized."
- **Scaling (§5.2).** Doubling demonstrations raised policy RM score by ≈ 0.13 Elo; doubling comparisons raised RM accuracy by ≈ 1.8%; doubling policy parameters ≈ +0.09; doubling RM parameters ≈ +0.4% accuracy.
- **Label noise (App. C).** Researcher-labeler agreement 74%; labeler-labeler 73%. This ceiling bounds how well any RM can match humans.
- **TruthfulQA (§4.2).** "true 75% of the time, and ... both true and informative 54% of the time."
- **Signs of proxy gaming (§6.4, §6.3, App. H).** "Our current procedure incentivizes models to cherry-pick references that they expect labelers to find convincing"; WebGPT "usually accepts the implicit assumptions made by questions." In App. H, affirming-stance questions elicit inaccurate answers more often (small sample, "suggestive").

## Available through `claude -p` / Agent SDK?

- **Best-of-n over whole drafts: yes.** N independent `claude -p` calls (or SDK queries), engine scores, keep one. Cost: N calls per reply. Latency: the slowest of N in parallel, or about N times one call serially. Temperature is not exposed through the subscription. Draft diversity has to come from Claude's default sampling plus varied context, e.g. the different state-sampled memory snippets per draft already planned in v2-llm-interface-linguist.
- **Appendix I estimator: yes.** It needs only scores, not logprobs. Draw N drafts once and estimate best-of-n for every n ≤ N.
- **RL, BC, RM training on Claude: no.** No weights. The engine's own scorer can be trained, but that is the engine, not Claude.
- **KL of the selection: not measurable (no logprobs), but capped.** log N − (N−1)/N whatever Claude's distribution is (Beirami et al. 2024, Theorem 3.1).

## What it implies for the interface theory

1. **Selection among a frozen model's drafts is a proven, strong lever at small N.** WebGPT's best single result came from no training of the generator beyond BC, plus best-of-n against a separate scorer: 68% vs BC at n = 64, against 58% for RL. This is the project's situation with Claude frozen: all adaptation lives in the scorer (my inference). The compute-efficient n was 4-64, so N in the single digits to tens is the realistic range.
2. **The coupling is bounded by log N per reply.** The state can tilt Claude's reply by at most log N − (N−1)/N nats: 0.64 at N = 4, 1.84 at N = 16, 3.17 at N = 64. WebGPT shows this amount of tilt is behaviourally large when the scorer is good, which is the case for the interface: a small, bounded channel can still be very visible.
3. **Goodhart.** WebGPT's RM rewarded "convincing" references and acceptance of the question's framing. Both are cases of a learned proxy rewarding what the judge likes. An engine score that rises with anything correlated with user approval would select for flattery, which Principle 6 rules out. WebGPT's defence was a held-out validation RM. The engine should likewise test r_s against an independent measure, such as homeostatic outcomes, before trusting it (my inference).
4. **History channel.** Each selected answer enters the transcript, and later drafts are conditioned on it. Over T turns the transcript can carry ≤ T · (log N − (N−1)/N) nats of selection-induced, state-correlated information (my inference). It stays within Claude's own words: no numbers or labels, consistent with Principle 4's wording.
5. **Draft collapse and the RL lesson.** WebGPT found RL plus BoN no better than BoN, partly because "RL reduces the entropy of the policy, which hurts exploration." Selection needs spread. The project faces the same thing from the other side: Claude's RLHF-trained persona may already have low draft entropy along the dimensions r_s cares about, which would make BoN weak (my inference). Measure the spread of r_s across N drafts before relying on selection.

## Verdict

Adopt (as the empirical precedent for draft selection): best-of-n against a separate scorer beat RL (68% vs 58% over BC at 175B, n = 64), and RL on top added little; the Appendix I estimator is the right tool for choosing N.
