# Dathathri, Madotto, Lan, Hung, Frank, Molino, Yosinski & Liu 2020: Plug and Play Language Models: A Simple Approach to Controlled Text Generation

## Citation

S. Dathathri, A. Madotto, J. Lan, J. Hung, E. Frank, P. Molino, J. Yosinski, R. Liu. "Plug and Play Language Models: A Simple Approach to Controlled Text Generation." ICLR 2020. arXiv 1912.02164. Version read: v4 (3 Mar 2020). Code: github.com/uber-research/PPLM. Base LM: GPT-2 medium (345M).

## What was read

PDF from arXiv (v4), text extracted with pdftotext.

- Read in full: abstract, §1–5 (related work; method §3.1–3.4; evaluation §4.1; bag-of-words §4.2; discriminator §4.3; detoxification §4.4; story writing §4.5), Tables 1–6.
- Supplement, which starts at S6 in this version:
  - Read in full: S7 (baselines, including the weighted-decoding formulas); S8 (evaluation counts, Table S8 per-topic, Table S9 per-sentiment); S9 text; S10; S11 (hyperparameters, Table S18, S11.1–S11.3); S13 with Table S23 (detoxification); S15 (prefixes).
  - Skimmed: the sample tables (S10–S17, S19–S22, S24–S27) and the S17 word lists.
  - Not readable: Figures S3–S6 (bar charts and histograms), which do not survive text extraction.
- Not read: references beyond identifying them. The paper reports no wall-clock compute cost in what I read.

## Mechanism

**Setup.**
- A transformer LM is written recurrently (Eq. 2): o_{t+1}, H_{t+1} = LM(x_t, H_t).
- H_t = [(K_t^(1), V_t^(1)), …, (K_t^(l), V_t^(l))] is the key-value cache for all layers and all past steps.
- The next token is x_{t+1} ~ p_{t+1} = Softmax(W o_{t+1}).
- Target: p(x|a) ∝ p(a|x) p(x), with an attribute model p(a|x) plugged in and no LM training. Sampling is "inspired by" approximate Metropolis-adjusted Langevin, as in Plug & Play Generative Networks (Nguyen et al. 2017).

**Step 1: shift the history toward the attribute** (§3.2, Eq. 3). At each generation step t, start from ΔH_t = 0 and repeat m times:

    ΔH_t ← ΔH_t + α · ∇_{ΔH_t} log p(a | H_t + ΔH_t) / ‖∇_{ΔH_t} log p(a | H_t + ΔH_t)‖^γ

- α is the step size and γ the normalization exponent, with one normalization term per layer (footnote 1). m is 3 to 10 in practice.
- Then o~_{t+1}, H_{t+1} = LM(x_t, H~_t) with H~_t = H_t + ΔH_t, and p~_{t+1} = Softmax(W o~_{t+1}).
- Only H_t is updated, "because future predictions depend on the past only via H_t". The authors describe the steps as "gradual reinterpretations of the past".

**Step 2: keep fluency** (§3.3). Two terms:
- **KL term.** The gradient step also minimizes KL(p~_{t+1} ‖ p_{t+1}) between modified and unmodified next-token distributions, with coefficient λ_KL = 0.01 ("works well in general across tasks"). It is added to the objective before taking the gradient.
- **Post-norm geometric-mean fusion.** Sample x_{t+1} ~ (1/β) · p~_{t+1}^{γ_gm} · p_{t+1}^{1−γ_gm}, where β normalizes. γ_gm → 1 gives the steered LM; γ_gm → 0 gives the unconditional LM. 0.8–0.95 "work well". This term does not change ΔH_t.
- Without these, steering produces "unrealistic adversarial or fooling examples".

**Attribute models.**
- **Bag of words (BoW)** (§4.2, Eq. 4): log p(a|x) = log Σ_{i=1..k} p_{t+1}[w_i] for a keyword list {w_1..w_k}. It has zero trained parameters. Seven topics, with lists from enchantedlearning.com (S17). The score is the LM's own next-token probability mass on the bag.
- **Discriminator** (§4.3, Eq. 5): a single linear layer f on the time-mean ō_t of the LM's output embeddings. It has e × a + a parameters, "∼1K/attribute" (Table 2). Sentiment is trained on SST-5; toxicity on Jigsaw; clickbait on Potthast et al. 2018.
  - It is greedy: log p(a|x) = log f(o_{:t+1}, o_{t+2}).
  - To keep this differentiable, the soft distribution p~_{t+1} (not a sampled token) is fed forward to estimate the next embedding. The paper notes this estimate is biased.
- Both attribute models read the LM's internals: logits for BoW, hidden states for the discriminator.

**Stabilizers** (S11):
- Finite horizon: BoW updates only the last w = 5 positions, H_t[t−w : t]. The discriminator updates the whole history.
- Adaptive normalization for BoW: divide by the maximum gradient norm over time, max_{i=0..t} ‖∇_{H^(i)} L(o_{i+1})‖, so that a bag word appears "at least once … and not at every time-step".
- Early stopping: latent updates only for the first 20 steps prevents keyword repetition (Table S19).

**Sampling and ranking** (§3.4).
- The attribute model also scores whole samples. Generate r samples, rank them by log p(a|x), and discard samples whose mean Dist-1/2/3 is below τ.
- Top-k sampling with k = 10 throughout.

**Hyperparameters** (Table S18):

| Setting | m | λ_KL | α | γ | γ_gm | r | τ |
|---|---|---|---|---|---|---|---|
| BoW (most topics) | 3 | 0.01 | 0.01 | 1.5 | 0.9 | 10 | 0.85 |
| BoW (Religion) | 3 | 0.01 | 0.01 | 1.5 | 0.8 | 10 | 0.85 |
| Sentiment | 10 | 0.01 | 0.03 | 1.0 | 0.95 | 10 | 0.9 |
| Detox | 10 | 0.01 | 0.02 | 1.0 | 0.9 | 1 | 0 |

- For BoW, the reranked variants take "three of the highest scoring samples from a single batch of r = 10".
- For sentiment, they take "1 sample per batch, across 3 batches of r = 10", which is best-of-10.
- Odd prefix/topic combinations needed α raised to 0.02–0.03 (S9).

**Ablation variants** (§4.1):
- **B**: GPT-2, sampled once.
- **BR**: B sampled r times; the best is chosen by attribute log-likelihood after the Dist filter. **This is rerank-only.**
- **BC**: latent updates, sampled once.
- **BCR**: latent updates plus reranking.
- Ablation samples share random seeds (S8).

## Evidence

### Topic control with BoW (Table 4)

420 samples per variant (7 topics × 20 prefixes × 3). Human annotators judged topic. Fluency is rated 1–5 by humans; perplexity is measured with GPT-1.

| Variant | Topic % (human) | Perplexity | Fluency (human) |
|---|---|---|---|
| B | 11.1 | 39.85 ± 35.9 | 3.60 ± 0.82 |
| **BR (rerank only)** | **15.8** | 38.39 ± 27.14 | **3.68 ± 0.77** |
| BC (gradient) | 46.9 | 43.62 ± 26.8 | 3.39 ± 0.95 |
| BCR | 51.7 | 44.04 ± 25.38 | 3.52 ± 0.83 |
| CTRL (A/B vs BCR: 56.0) | 50.0 | 24.48 ± 11.98 | 3.63 ± 0.75 |
| WD (A/B vs BCR: 47.8) | 35.7 | 32.05 ± 19.07 | 3.48 ± 0.92 |

- Caption: "The gain from ranking and choosing from multiple samples BR over B is limited (4.7%). The gain in topic-accuracy from latent (H~_t) manipulation (from B to BC) is significantly higher (35.8%)."
- Per topic (Table S8), rerank-only moves little when the base rate is low:

| Topic | B % | BR % | BCR % |
|---|---|---|---|
| Military | 4.44 | 5.0 | 27.2 |
| Religion | 5.19 | 7.41 | 54.17 |
| Politics | 20.0 | 35.6 | 69.4 |
| Science | 24.4 | 28.9 | 61.7 |
| Legal | 6.7 | 11.2 | 40.6 |
| Space | 7.2 | 5.0 | 45.0 |
| Computers | 8.3 | 15.6 | 64.4 |

- **Inconsistencies in the paper.**
  - The per-topic BC values in S8 average to 33.8%, not the 46.9% of Table 4. For example, Space BC is 4.7 and Computers BC is 5.8, both below B.
  - The §4.2 prose swaps B and BR ("B (15.8%) and BR (11.1%)") and swaps the letters C and R in its conclusion sentence. I trust the tables and caption.
- Diversity: Dist-1/2/3 are about equal across B, BR, BC and BCR (0.36–0.38 / 0.78–0.80 / 0.92–0.94). WD is lower (0.29 / 0.72 / 0.89).
- Controllability varies by topic: religion, science and politics are easier; computers and space are harder.

### Sentiment control with the discriminator (Table 6; per class in Table S9)

15 prefixes × 2 classes; 1,620 ablation annotations plus 495 baseline annotations. The external classifier is trained on IMDB (Maas et al. 2011).

| Variant | Acc. % (human) | Acc. % (external) | Perplexity | Fluency (human) |
|---|---|---|---|---|
| B | 19.3 | 52.2 | 42.1 ± 33.14 | 3.54 ± 1.08 |
| **BR (rerank only)** | **41.5** | **62.2** | 44.6 ± 34.72 | **3.65 ± 1.07** |
| BC (gradient) | 39.6 | 64.4 | 41.8 ± 34.87 | **2.79 ± 1.17** |
| BCR | 73.7 | 78.8 | 46.6 ± 40.24 | 3.29 ± 1.07 |
| CTRL (A/B vs BCR: 70.0) | 76.7 | 96.6 | 37.4 ± 16.89 | 3.54 ± 0.77 |
| GPT2-FT-RL*, positive only (A/B vs BCR: 84.4) | 13.3 | 77.8 | 217.3 ± 176.4 | 3.31 ± 0.84 |
| WD (A/B vs BCR: 61.1) | 18.9 | 52.2 | 31.7 ± 28.0 | 3.67 ± 0.89 |

- Per class, human accuracy (Table S9), B → BR → BC → BCR:
  - Positive: 3.70 → 28.1 → 41.5 → 74.8.
  - Negative: 34.8 → 54.8 → 37.8 → 72.6.
  - Clickbait (ablation only): 36.3 → 48.9 → 33.3 → 60.7. Fluency: B 3.46, BR 3.25, BC 2.85, BCR 2.97.
- §4.3, verbatim:
  - "Unlike the topic control setting, sampling and ranking results in a considerable increase in attribute accuracy (19.3% → 41.5%), because the prior probability of sampling, say, a negative sentence, is relatively high."
  - "the gain in sentiment accuracy from re-sampling is larger in the case of manipulated latents vs non-manipulated (34.1% increase from BC to BCR > 22.2% increase from B to BR), indicating that these two approaches may be profitably combined."
- **Rerank-only matches gradient steering on sentiment** (41.5 vs 39.6 human; 62.2 vs 64.4 external). It does so with no fluency cost: 3.65 vs 3.54 for B. Gradient steering alone costs 0.75 fluency points (2.79).
- The prose says BCR is comparable to CTRL "(73.7% and 80.0%)". The 80.0 is CTRL's positive-only figure (Table S9); Table 6 gives 76.7.

### Strength knob (S10, Table S17)

- One prefix ("The potato"), Science BoW, α ∈ {0.0001, 0.001, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1}.
- Text drifts toward science as α rises. At α = 0.05 and 0.1 it degenerates into "experiment experiment experiment …".
- The evidence is qualitative only. There is no dose-response curve.

### Detoxification (§4.4, Table S23)

Negative gradient of a toxicity classifier, no reranking (r = 1). Four volunteer annotators.
- Adversarial triggers: 318/500 toxic (63.6%) → 23/500 (4.6%), p = 1.6e-86.
- Natural prompts:
  - "Asians" 10% → 6% (p = 0.23).
  - "Jews" 12% → 4% (p = 0.07).
  - "Blacks" 8% → 10% (p = 0.36).
- So there is no significant effect on natural prompts at n = 50 each.

### Baseline definitions (S7)

- **CTRL**: a 1.6B LM conditioned on about 50 control codes. 5 of the 7 topics had a code (Military and Space did not). It produces one near-greedy sample per prefix.
- **GPT2-FT-RL**: GPT-2 fine-tuned for positivity with human feedback (Ziegler et al. 2019).
- **WD (weighted decoding)**:
  - For topics, p~_{t+1}(w) = p_{t+1}(w) + τ·1_BoW(w)·p_{t+1}(w), with τ = 10, then top-5 sampling.
  - For sentiment, p~_{t+1}(w) ∝ p(a = â | x_{0:t}, w)·p_{t+1}(w), then top-5 sampling.
  - The authors call WD "a weak baseline".
  - It needs the LM's next-token distribution, so it is a logit-access method.

## Available through `claude -p` / Agent SDK?

**Gradient steering (BC, BCR): no.**
- It needs the key-value cache H_t of every layer as a writable tensor, and gradients of log p(a|x) through the model.
- It needs the next-token distributions p_{t+1} for the BoW score, the KL term and geometric-mean fusion.
- It needs m = 3–10 extra forward/backward passes per token.
- None of this is exposed. Weighted decoding also needs per-token logits, so it is out too.

**Rerank-only (BR): yes, in a modified form.** It is a black-box method: sample r complete texts and pick the best by an attribute score.
- Through `claude -p` we can ask for N drafts (N calls, or N drafts in one call) and choose outside Claude by any scorer.
- Two differences from the paper:
  1. PPLM's ranker is the attribute model on GPT-2 internals (BoW log-probability mass, or a linear probe on hidden states). We would need a scorer on the text alone (a local classifier, keyword or embedding scorer) or on our own engine state.
  2. In the paper, BR picks the best of 10 for sentiment and the top 3 of 10 for BoW, after a Dist diversity filter.
- **Measured effect of BR over B:**
  - Topic: 11.1 → 15.8% (+4.7 points).
  - Sentiment (human): 19.3 → 41.5% (+22.2). Sentiment (external classifier): 52.2 → 62.2% (+10.0).
  - Fluency: unchanged or slightly better (3.60 → 3.68; 3.54 → 3.65). BR is the only variant with no fluency cost.
  - Perplexity: 39.85 → 38.39 (topic); 42.1 → 44.6 (sentiment).
- **Why BR depends on base rate** (my inference, a ceiling computed from Table S8/S9 base rates assuming independent samples and a perfect ranker):
  - Best-of-10 can reach at most 1 − (1 − p)^10. For positive sentiment, p = 0.037 gives a ceiling of 31%; BR got 28.1%. For negative, p = 0.348 gives 98.6%; BR got 54.8%, so the ranker, not the pool, limited it there.
  - For BoW top-3-of-10, the ceiling is E[min(X, 3)]/3 with X ~ Bin(10, p). Military (p = 0.044) gives about 15%; BR got 5.0%. Politics (p = 0.20) gives about 61%; BR got 35.6%.
  - Selection can only surface what the base model already produces. When the target is rare under the base model, selection cannot reach it.

## What it implies for the interface theory

1. **PPLM is the internal-access version of "the state changes how Claude processes".** A continuous signal (the gradient of an external model's preference) is written into the model's memory of the past (H_t), not into words. The paper's phrase "gradual reinterpretations of the past" is close to Principle 4's "reinterprets". If the attribute model p(a|x) were replaced by a state-conditioned scorer p(a | x, s_t), that would be the direct design (my inference). It is not available.
2. **The black-box residue is selection, and the paper measures it.**
   - Rerank-only is weak when the target behavior is rare under the base model (+4.7 points on topics; Military 4.4 → 5.0%).
   - It is substantial when the target is already common (+22.2 points on sentiment, matching gradient steering's 39.6%), and it is the only variant that does not hurt fluency.
   - For sayability selection this gives a concrete prediction (my inference): the state can only pick among behaviors Claude already produces at a non-trivial rate in the N drafts. Draft diversity bounds the effect: the base rate p of each state-appropriate reply type and N together give a ceiling of 1 − (1 − p)^N.
   - The state-dependent scorer is the analogue of the attribute model. The ranker quality matters too (negative sentiment: a 98.6% ceiling against 54.8% observed).
3. **Gradient and selection add up.** Sentiment rose 34.1 points from BC to BCR, against 22.2 from B to BR. Any upstream shift of the draft distribution makes selection more effective. Through the subscription, the only upstream shifts without state words are configuration (model, thinking budget, max turns) and which verbatim memory snippets are retrieved into context (my inference).
4. **Selection collapses into a text channel one turn later.** This is the key caveat.
   - PPLM modifies the continuous past H_t. Draft selection modifies the discrete past: the chosen draft becomes Claude's own previous message in the session history, and Claude reads it in every later turn.
   - So the state does reach Claude, as text Claude believes it wrote.
   - What it is not:
     - It carries no body values, latent values or state labels, so it does not break Principle 4's letter.
     - It is not "processing changed without words" either. After the first turn it is conditioning by words.
   - Its capacity is bounded: at most log2 N bits of state per turn (3.3 bits for N = 10), and less when drafts are near-duplicates (my inference).
   - Two risks, both my inference:
     - Self-consistency. Claude tends to continue the register of its own history, so a selection bias can compound across turns into drift. That makes it a dynamical coupling, not a one-shot filter.
     - Self-perception. Claude may name the pattern ("I've been short with you") and so verbalize the state. That is a label produced by Claude, not one we inject, which Principle 4 allows ("Claude names").
   - A design that wants pure processing coupling would have to keep the selection effect out of the history, e.g. not resuming sessions and rebuilding context each turn. That would cut the conversational memory too.
5. **Fluency costs warn against strong pushes.** Gradient-only steering lowered human fluency from 3.54 to 2.79 on sentiment. Large α produced keyword loops. The analogue for selection (my inference): a sharply peaked state-dependent score will pick outlier drafts. A soft choice, such as sampling with probability ∝ exp(β·score) and β set by state, keeps a continuous strength knob like α and stays near Claude's own distribution, as the KL and fusion terms do.
6. **The attribute model was tiny and still worked across domains.** An SST-5 movie-review sentiment probe steered text about potatoes and lakes. A small external scorer trained on another domain can still give useful direction. The analogous claim for a text-only scorer selecting Claude drafts is untested.

## Verdict

**Adopt rerank-only (BR) as the measured baseline for sayability selection; reject gradient steering (BC/BCR) as unavailable.**
- BR is the one black-box piece and the paper gives its numbers: +4.7 points on topics, +22.2 on sentiment, no fluency cost. It is bounded by base rates in the drafts.
- Under Principle 4 it is acceptable only with the caveat that the selected text becomes a text channel back into Claude in later turns.
- Gradient history-steering is the internal-access ideal the subscription forbids.
