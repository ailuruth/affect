# Shumailov, Shumaylov, Zhao, Gal, Papernot & Anderson 2023/2024: training on generated data makes models forget (model collapse)

Shumailov, I., Shumaylov, Z., Zhao, Y., Papernot, N., Anderson, R. & Gal, Y. "The Curse of Recursion: Training on Generated Data Makes Models Forget." arXiv:2305.17493, v3 (14 April 2024). https://arxiv.org/abs/2305.17493. The peer-reviewed version is "AI models collapse when trained on recursively generated data", *Nature* 631:755–759 (2024), doi:10.1038/s41586-024-07566-y. nature.com is outside this session's network, so **the Nature text was not read**. Everything below is from arXiv v3, the preprint of that paper, and the Nature version's experiments and wording may differ.

**How fully read:** arXiv v3 main text read in full on 2026-11-28 (§1–6: definitions, the discrete and Gaussian derivations, the noisy-approximation bound, GMM, VAE and OPT-125m experiments, Discussion). The appendices (proofs A.1–A.2, extra figures) and the reference list were not read.

## What it says
- **Definition.** Model collapse is "a degenerative process affecting generations of learned generative models, where generated data end up polluting the training set of the next generation". *Early* collapse: the tails of the distribution disappear. *Late* collapse: modes merge and the model converges to something with "very small variance".
- **Two causes.**
  - Statistical approximation error from finite samples, the primary one. Without it there is no collapse beyond the first generation.
  - Functional approximation error: the model class is wrong, or puts mass outside the support.
- **The process studied.** Generation i+1 is fitted to data from p_{i+1} = α_i p_θ,i+1 + β_i p_i + γ_i p_0: new model samples, previous data, and original data. The theory uses α = γ = 0 (each generation trained only on the previous generation's samples).
  - **Discrete distribution, exact fitting.** The fit–resample loop is a Markov chain whose only absorbing states are delta functions, so it collapses to one state with probability 1. A state of probability below 1/M is lost first.
  - **1-D Gaussian, unbiased estimates.** Var(X^n) = σ²(1 + n/M) for constant sample size M. The parameters follow a random walk. E[W₂²] to the truth grows like (3/2)σ² Σ 1/M_i, so it diverges unless M_i grows superlinearly.
  - **Noisy approximation (Gelbrich bound).** The same lower bound plus Σ E‖ε_i‖² from approximation noise.
- **Experiments.**
  - GMM, two Gaussians, 1,000 samples per generation: misperceived by generation 50, nearly a point by 2,000.
  - VAE on MNIST-like data: modes entangle by generation 20. The *original* encoder places descendants' samples ever closer to the mean.
  - OPT-125m fine-tuned on WikiText-2, then each generation on the previous one's outputs (5-way beam search). Generation 0 reaches a mean perplexity of 34 on real test data (zero-shot 115). With no original data and 5 epochs per generation, later generations still learn the task but lose "some performance – from 20 to 28 perplexity points" (the authors' wording; I read it as the increase over generation 0). With 10 % of the original data kept each generation: "only minor degradation". Later generations produce both more high-likelihood sequences and a long tail of sequences the original model would never produce. A repetition penalty makes it worse.
- **Their conclusion.** Access to the original data source is needed to sustain learning; tails, the improbable events, are lost first.

## What matters for this engine
- **The engine's nightly replay is not generative replay in this sense.** The store replays recorded moments: his real face, voice and words, and the agent's real rendered outputs and own-face observations. No step samples from a learned generator to make its own training data, so the finite-resampling random walk that drives Shumailov's collapse is not present as such. van de Ven's generative replay, which the repo considered (van-de-ven-2020-brain-inspired-replay.md), would bring it in; the spec does not use it.
- **But three loops in the spec do train on data the engine itself produced** (new-core-search-16-synthesis.md §3):
  1. Π̃ is trained on the agent's own (state, face) pairs, and Δ is trained so that Π̃ reads the agent's own face correctly (𝓛_display). Writer and reader are both learned from the writer's own output: a co-adaptation loop, the "co-training drift" that F8″ already names.
  2. 𝒜's bases and the draft scorer are trained on moments produced by yesterday's Γ and yesterday's draft choices (performative data).
  3. After the 30-day retention window, real data older than 30 days are deleted. What remains is only the consolidated weights. That is Shumailov's "replace" regime for anything older than the window, with the pull to θ₀ standing in for γ p_0.
- **Tails first.** The paper's main empirical lesson: rare events are what a self-trained model loses first. In the engine the rare events are the hard moments. That is a point *for* some priority on rare moments, and against letting retention deletion plus a fixed-point pull wash them out. It is not a point for weighting them by distress level for as long as they are stored. Rarity and distress are different quantities.

## Verdict: adopt (as the risk statement for self-trained loops); its mechanism applies only to the loops listed above
Adopt the definition and the "keep real data in the mix" lesson. Cite arXiv v3, not the Nature paper, until the Nature text is read.
