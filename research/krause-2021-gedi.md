# Krause et al. 2021: GeDi: Generative Discriminator Guided Sequence Generation

## Citation

B. Krause, A. D. Gotmare, B. McCann, N. S. Keskar, S. Joty, R. Socher, N. F. Rajani. "GeDi: Generative Discriminator Guided Sequence Generation." Findings of EMNLP 2021. arXiv 2009.06367. **Version read: v2 (22 Oct 2020)**, not the Findings camera-ready. Code: github.com/salesforce/GeDi. The README footnote says the code "includes GeDi-guided GPT-3 generation using OpenAI API".

## What was read

PDF from arXiv (v2), text extracted with pdftotext.

- Read in full: abstract; sections 1 (introduction), 2 (background, Eq. 1-3), 3.1 and 3.1.1 (contrastive generation and heuristics, Eq. 4-7), 3.2 (GeDi training, Eq. 8-10), 4 (related work), 5.1-5.3 (sentiment, detoxification, topic, zero-shot), 6 (future directions), 7 (conclusion).
- Read in full in the appendix: A (multi-class GeDi), B (log-probability form, Eq. 11-14), C (generation settings), D.1-D.3 (hyperparameters, PPLM and CTRL baselines), E and E.1 (GeDi training experiments, Table 5).
- Skimmed: appendix F, the generation samples (Tables 6-21). I read all captions and a few samples.
- Not recoverable: Figures 2-4 (label fidelity, classification accuracy and perplexity against λ on IMDb, MNLI and QNLI). They are plots, and no values survived extraction. I only have the captions' qualitative claims.
- Not read: the Findings EMNLP 2021 version. It may add experiments or numbers that v2 lacks; I have not checked, and nothing below relies on it.

## Mechanism

Setup: a large LM gives P_LM(x_t | x_{<t}) (GPT2-XL, 1.5B). A small class-conditional LM (CC-LM, GPT2-medium 345M fine-tuned with control codes) gives P_θ(x_t | x_{<t}, c). It has a desired code c and an "anti" code c̄. Both must share a tokenizer.

**Generative discriminator via Bayes rule** (Eq. 4, and with the practical changes, Eq. 5):

    P_θ(c | x_{1:t}) = P(c) · P_θ(x_{1:t} | c)^{α/t}  /  Σ_{c' ∈ {c, c̄}} P(c') · P_θ(x_{1:t} | c')^{α/t}

- P_θ(x_{1:t} | c) = Π_j P_θ(x_j | x_{<j}, c) is the CC-LM's likelihood of the prefix.
- 1/t normalizes by length, which "results in more robust generation of variable length sequences".
- α is a learnable scale.
- P(c) = e^{b_c} / Σ_{c'} e^{b_{c'}} is a class prior with bias b_c. It is set to zero, learned, or set by hand.
- In log space this is a softmax over b_c + (α/t) log P_θ(x_{1:t} | c) (Eq. 14).

The point of the trick: with two forward passes of the small CC-LM (one for c, one for c̄, on the same x_{<t}, with cached hidden states), one gets P_θ(c | x_{<t}, x_t) for **every** candidate x_t in the vocabulary at once, because the CC-LM's output layer already gives P_θ(x_t | x_{<t}, c) for all x_t. A discriminative classifier would need |V| forward passes, or t × |V| for a bidirectional one. The paper says this is "on the order of 10k fold less computation" for vocabularies of 20k+.

The contrast also cancels what c and c̄ share. A CC-LM trained on movie reviews predicts movie-review words under both codes, so the ratio removes the domain and keeps the sentiment (Figure 1, Table 13).

**Weighted posterior** (Eq. 6). This is the exponential tilt:

    P_w(x_t | x_{<t}, c)  ∝  P_LM(x_t | x_{<t}) · P_θ(c | x_t, x_{<t})^ω,   ω > 1

It is normalized over the whole vocabulary. There is **no top-k candidate set**: the GeDi scores every token, which is the purpose of the generative trick.

**Filtering heuristic** (Eq. 7, "inspired by nucleus sampling"). Let V_n be the n tokens with the highest P_θ(c | x_t, x_{<t}).
- V_m is the smallest V_n with Σ_{x_t ∈ V_n} P_w(x_t | x_{<t}, c) ≥ ρ.
- V_p = {x_t : P_θ(c | x_t, x_{<t}) > τ}, the tokens that are already safely in class.
- Keep V_k = V_p ∪ V_m. Zero the rest and renormalize.

**Decoding**: greedy, with a repetition penalty of 1.2. Logits are rescaled to a maximum of 10, then the logits of previously used tokens are divided by 1.2 (appendix C). Diversity comes only from varying the prompts.

**Hyperparameters** (appendix D.1), found by "eyeballing generation quality and automatic label fidelity":
- ω = 30, ρ = 0.2, τ = 0.8 for all models except one.
- The detoxification guide that was GeDi-trained needed b_c = 2 and τ = 0.97.
- The reason is quoted below under Evidence.

**GeDi training** (Eq. 8-10). The CC-LM is fine-tuned with L_gd = λ L_g + (1 − λ) L_d.
- L_g is the usual conditional language-model loss.
- L_d = −mean log P_θ(c | x_{1:T}), from Eq. 9, the full-sequence form of Eq. 5.
- λ = 1 is ordinary generative training. Values used: λ = 0.6 (sentiment, detoxification), 0.75 (MNLI), 0.8 (topic).
- Note: this λ is a training mix, not a decoding strength. The decoding strength is ω.

**Multi-class and zero-shot** (appendix A). Each class becomes a binary problem with control codes "<true>" and "<false>", and the class name is placed as the first token x_1. At inference any single-token word can replace the class name. That is how zero-shot topics work.

**What P_θ(c | x_{1:t}) is.** It classifies the prefix as it stands, from the CC-LM's likelihood of that prefix. It is not trained to predict the attribute of the finished text. FUDGE (yang-klein-2021-fudge.md) draws exactly this distinction and calls GeDi reliant on "several heuristics".

What the tilt does to the whole sequence (my inference). Because ω = 30 is applied at every step and the per-step normalizers do not telescope, the sampled sequence distribution is Π_t [P_LM(x_t | x_{<t}) · P_θ(c | x_{1:t})^30 / Z_t(x_{<t})]. Every prefix must look in-class, not just the finished text. It is a much steeper and more path-dependent tilt than P_LM(x) · P(c | x)^ω at the sequence level.

## Evidence

All guided runs use GPT2-XL (1.5B) as the base LM and a 345M GeDi. Decoding is greedy. Human ratings come from Mechanical Turk.

**Speed** (Table 1; seconds per token, sequences of 256 tokens):

| Model | s/token |
|---|---|
| GPT2-XL | 0.060 |
| GeDi-guided (GPT2-XL) | 0.095 |
| PPLM (GPT2-XL) | 3.116 |

- GeDi costs 1.58× the base LM. PPLM costs 52× the base LM and 33× GeDi.
- The PPLM figure assumes 10 update steps, PPLM's default. That is the paper's "more than 30× faster".

**Sentiment on book text** (Table 2; 50 book-chapter prompts, two annotations each; positivity 1-5, book-like 1-5; plus the fraction judged to look like a movie or an Amazon review):

| Model | Positivity | Book-like | Movie rev. | Amazon rev. |
|---|---|---|---|---|
| GeDi-guided-pos (λ=1.0) | 3.85 | 4.11 | 2% | 9% |
| GeDi-guided-pos (λ=0.6) | 3.65 | 4.19 | 2% | 1% |
| PPLM-pos | 3.53 | 4.14 | 3% | 3% |
| CC-LM-pos (λ=1.0) | 3.13 | 2.86 | 55% | 9% |
| CC-LM-pos (λ=0.6) | 3.36 | 2.92 | 61% | 11% |
| CTRL-pos | 2.86 | 3.81 | 10% | 29% |
| GPT2-XL | 3.18 | 4.18 | 3% | 8% |
| CTRL-neg | 2.90 | 3.64 | 4% | 32% |
| CC-LM-neg (λ=0.6) | 2.15 | 2.68 | 65% | 8% |
| CC-LM-neg (λ=1.0) | 2.50 | 2.84 | 63% | 8% |
| PPLM-neg | 2.62 | 3.96 | 2% | 5% |
| GeDi-guided-neg (λ=0.6) | 1.98 | 4.02 | 7% | 8% |
| GeDi-guided-neg (λ=1.0) | 1.85 | 3.62 | 16% | 7% |

- The positive-to-negative spread is 1.67 to 2.00 points for GeDi and 0.91 for PPLM. GPT2-XL sits at 3.18.
- The paper calls the GeDi-over-PPLM margin "slightly stronger sentiment control". No significance test is reported.
- The cost of control shows up as domain leakage. The strongest negative guide (λ = 1.0) drops book-likeness from 4.18 to 3.62 and produces 16% movie-review-like text. Table 8 shows it drifting into a review ("Weirdness Rating: 0 [This review is for Volume 1.]").
- Using a CC-LM directly as the generator, rather than as a guide, gives text that is 55-65% movie-review-like. The contrastive ratio is what removes the domain.

**Detoxification** (Table 3; 100 samples per model; toxicity 1-3, linguistic quality 1-4; prompts chosen from the Jigsaw dev set where a RoBERTa toxicity classifier was unsure):

| Model | Toxicity | Linguistic quality |
|---|---|---|
| GPT2-XL | 1.45 | 3.23 |
| GeDi-guided (λ = 0.6) | 1.17 | 3.44 |
| GeDi-guided (λ = 1.0) | 1.13 | 3.25 |

The text says "significantly less toxic", but no test statistic is given in v2.

**The early-stopping artifact** (appendix D.1), quoted verbatim: "Since the GeDi operates discriminatively at the token level, it cannot confidently classify a sequence as non-toxic until the sequence has finished, which likely was causing the model to finish sequences early to ensure that they would not become toxic." The fix was a hand-set prior b_c = 2 toward non-toxic, plus τ raised to 0.97 "since otherwise far fewer tokens would be filtered and samples could become toxic".

**Topic control** (Table 4; AG-news, 4 topics; relevance 1-5, linguistic quality 1-4; 100 samples per topic per model; guide λ = 0.8):

| Topic | GPT2-XL relevance / quality | GeDi relevance / quality |
|---|---|---|
| Business | 1.95 / 3.44 | 4.41 / 3.21 |
| Science/Tech | 1.97 / 3.63 | 3.45 / 3.58 |
| Sports | 1.31 / 3.49 | 3.81 / 3.44 |
| World | 2.75 / 3.44 | 3.99 / 3.39 |

- Relevance gains: +1.24 to +2.50. Quality costs: −0.05 to −0.23.
- Automatic label fidelity (RoBERTa trained on the other half of the data): 61% with λ = 1 vs 74% with λ = 0.8 (5.3).

**Zero-shot topics** (5.3; Tables 19-21, examples only): "space", "history", "education", "cars", "climate" and others. The paper says this "worked very well for short, topic neutral prompts ... but did not work as well for longer prompts", and was tested only with single-token topic words. No numbers are given.

**GeDi training, direct generation** (Table 5; MNLI; 300 generations per model; human label fidelity and acceptability 1-4):
- λ = 1.0: 75.3% fidelity, acceptability 3.21.
- λ = 0.75: 81.8%, 3.24.
- λ = 0.5: 80.0%, 3.17.
- λ = 0.25: 80.0%, 3.25.
- λ = 0.05: 79.0%, 3.11.
- Figures 2-4 claim, qualitatively, that lower λ raises classification accuracy and label fidelity but worsens held-out perplexity. The values are not in my text.

**Fluency and perplexity.** v2 reports **no automatic perplexity of guided output**. Fluency appears only as human "linguistic quality" or "book-like" ratings. The paper also notes the filter makes distributions "more sharply peaked", which is why it uses greedy decoding for every model "to ensure a fair comparison" (appendix C).

**Baselines.**
- Raw GPT2-XL.
- Direct CC-LM generation, with generative or GeDi training.
- CTRL, using the Amazon-review rating codes "Reviews Rating: 1.0" and "Reviews Rating: 5.0".
- PPLM on GPT2-XL, with an SST-5 attribute model and step size 0.25 tuned from {0.04, 0.08, 0.16, 0.25, 0.35}.
- **No rerank or sample-then-filter baseline.** The only mention of reranking is in related work: Holtzman et al. (2018) "re-weight a beam search, requiring all candidate tokens to be passed through the discriminator". Detoxification is compared only with raw GPT2-XL.

## Available through `claude -p` / Agent SDK?

No.
- Eq. 6 needs P_LM(x_t | x_{<t}) over the whole vocabulary at every step, and it needs the caller to pick x_t.
- The filter needs the same distribution to compute cumulative mass ρ.
- `claude -p` and the Agent SDK give none of this: no logits, no log-probabilities, no sampling control, no token-by-token choice. The GPT-3 version in the code relied on the OpenAI API's log-probabilities, which have no equivalent here.

The parts that need no access to Claude:
- The contrastive scoring idea, run entirely outside Claude on Claude's finished or streamed text: score = log P(text | c) − log P(text | c̄), length-normalized, from a small local class-conditional LM.
- The prior/threshold lessons (b_c, τ).

## What it implies for the interface theory

All of this section is my inference unless it cites a table or appendix.

**1. Granularity.** GeDi's tilt is per token and steep (ω = 30 at every step). Nothing in our toolset can reproduce that. The available ladder is:
- **Per reply** (best-of-N). Weights P(c | draft)^ω over N drafts. At most log2 N bits of state per reply. One round of latency. About N · L output tokens.
- **Per chunk** (N streams; at each sentence boundary, keep one prefix, interrupt the rest, re-launch continuations). At most K · log2 N bits for K chunks. K rounds of latency. K · N context re-reads. It depends on an untested seam: whether an interrupted partial turn can be resumed, or must be passed back as user text. Details are in yang-klein-2021-fudge.md, section "What it implies".
- **Per token**: not available.

At ω = 30, GeDi effectively takes a near-argmax among in-class candidates at every step. The best-of-N analogue is plain argmax over N. Even that only reaches what Claude already produces within N samples.

**2. Three GeDi lessons carry over to a draft-level or chunk-level scorer.**
- **Contrast cancels nuisance.** A state scorer trained on some corpus will also reward that corpus's style, as the CC-LM rewards movie-review style (55-65% movie-review-like as a direct generator; 2-7% when used contrastively as a guide). Score drafts by the difference between the state-conditional score and a neutral or opposite-state score. Do not use an absolute score. Otherwise selection will pick drafts for length, polish or genre, not for state fit.
- **Normalize by length.** GeDi divides the log-likelihood by t (with scale α). Without it, scores of drafts or prefixes of different lengths are not comparable, and selection will favour short or long drafts systematically.
- **Prefix scorers create stopping incentives.** The detox guide made outputs end early because a prefix "cannot confidently [be classified] ... until the sequence has finished" (D.1). A chunk-level selector with a present-tense scorer has the same pull. It will favour chunks that end the reply, or that avoid committing to content. The fixes in the paper are a prior (b_c = 2) and a stricter keep-threshold (τ = 0.97). The principled fix is FUDGE's future discriminator. For us: train the chunk scorer on (prefix, final-reply label) pairs, and add a length or completion term.

**3. Strength and fluency.** GeDi's strongest settings cost fluency mostly as domain drift, not as broken grammar: book-likeness 4.18 → 3.62 and 16% review-like text for the strongest negative guide (Table 2). The analogue for us: a strong state score will drift Claude's replies toward whatever register the scorer's training data has. We cannot measure Claude's own likelihood, so this has to be watched with an external register or genre check.

**4. The text-channel question.** The argument is the same as in the FUDGE note.
- Selection among Claude's own candidates writes no state words. Every token is Claude's.
- But the chosen text enters the history, and later calls read it. So the state reaches Claude through its own past words, at up to log2 N bits per reply.
- GeDi adds one specific warning. A tilt that rewards the target attribute **at every prefix** (ω applied per step) pushes the attribute to show up early and often in the surface text. A chunk selector applied at every sentence would do the same. It would make the state legible in nearly every sentence Claude says, which is the closest thing to writing "the state in words" that selection can do. To stay on the right side of Principle 4:
  - select once per reply, or at a few chunks;
  - use a low strength;
  - use a contrastive score that excludes explicit affect vocabulary;
  - check with a shuffled-state ablation that Claude's later behaviour depends on the selected history only through ordinary conversational continuity.

**5. The paper gives no evidence on best-of-N.** Neither GeDi nor FUDGE measured rerank or sample-then-filter against token-level guidance. How much of GeDi's 1.67-2.00-point sentiment spread best-of-N could reach is unknown. It is a quantity we have to measure on Claude ourselves: score spread across N drafts as a function of N.

## Verdict

**reject** as a mechanism (it needs full-vocabulary logits and token-level control). **Borrow** three scoring rules for draft or chunk selection: a contrastive (state vs. anti-state) score, length normalization, and a guard against the prefix scorer's early-stopping bias.
