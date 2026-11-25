# Yang & Klein 2021: FUDGE: Controlled Text Generation With Future Discriminators

## Citation

K. Yang, D. Klein. "FUDGE: Controlled Text Generation With Future Discriminators." Proceedings of NAACL-HLT 2021. arXiv 2104.05218, version read: v2 (15 Aug 2021). Code: github.com/yangkevin2/naacl-2021-fudge-controlled-generation.

## What was read

PDF from arXiv (v2), text extracted with pdftotext.

- Read in full: abstract; sections 1 (introduction), 2 (related work), 3 and 3.1 (method, advantages and limitations), 4.1-4.3 (couplet, topic and formality experiments, with Tables 2-9), 5 (discussion), 6 (ethics).
- Read in full in the appendix: A (the rule-based checker F), B (PPLM on translation, Table 11), C (hyperparameters, Tables 12-13), D (predictor ablations, Tables 14-15), E (other perplexity models, Tables 16-17), F (significance tests), G (strength λ, Table 19), H (candidate pruning, Table 20), M (software).
- Skimmed: the example generations (Tables 18, 21-30; appendices I, J, L) and the word lists and prefixes (K). I looked at them for degeneration patterns only.
- Not read: the reference list beyond identifying cited works.
- Figure 1 is a diagram. Only its caption survived extraction.

## Mechanism

Base model G gives P(x_i | x_{1:i-1}). The goal is to sample from P(X | a) for an attribute a that G was not trained on.

The Bayesian factorization (section 3):

    P(x_i | x_{1:i-1}, a)  ∝  P(a | x_{1:i}) · P(x_i | x_{1:i-1})

- The second factor is G's next-token distribution. It needs G's output logits, nothing else. No gradients and no weights.
- The first factor comes from a small binary classifier B(x_{1:i}). B predicts whether the **completed** sequence x_{1:n} will have attribute a, given only the prefix. This is the "future discriminator".
- Training data for B: each labelled example (x_{1:n}, a') gives one training pair (x_{1:i}, a') per prefix length i. Every prefix gets the label of the finished text.
- Decoding step: take the top 200 tokens of G. Run B on each candidate prefix x_{1:i-1} + x_i. Add log B to G's log-probabilities. Renormalize over the 200 candidates. Sample (top-k, k = 10, for couplets and topics) or decode greedily (translation).
- B is an LSTM: 3 layers, 300 dimensions, output dimension 1 (appendix C). For the rhyme and future-word predictors it is bidirectional (150 per direction) and trained with noise-contrastive estimation, so its outputs are unnormalized.
- Composition: for conditionally independent attributes, add their log-probabilities (couplets: meter B1 + rhyme B2 + sentence end B3).

Strength knob. There is no exponent in the main method. The paper says (4.1.2): "it is possible (and trivial) to adjust the conditioning strength in FUDGE by multiplying the binary predictors' output logits by a constant. However, this deviates from our Bayesian factorization of P(X|a), and we do not do so." The one exception is topic control. There, with a bag of N topic words w_j, the term added to G's logits is

    (λ / N) · Σ_{j=1..N} log P(w_j | x_{1:i})

λ is read as "how many bag words must appear", and is chosen on a validation bag (λ = 4). This is in effect an exponent λ/N on a product of per-word predictors.

Why a future discriminator gives the exact posterior. This is my own check; the paper states the factorization but does not show the telescoping. Suppose B is exact: B(x_{1:i}) = P_G(a | x_{1:i}), the probability under G's own continuations that the finished text has a. Then the normalizer of the step above is

    Σ_{x_i} P(a | x_{1:i}) P(x_i | x_{<i})  =  P(a | x_{<i})

So each step is P(x_i | x_{<i}, a) = P(a | x_{1:i}) P(x_i | x_{<i}) / P(a | x_{<i}). The product over i = 1..n telescopes to

    P(x_{1:n}) · P(a | x_{1:n}) / P(a)  =  P(x_{1:n} | a)

So with an exact B and no exponent, token-level FUDGE samples **exactly the same distribution** as sequence-level conditioning, that is, rejection sampling or sampling-importance-resampling over whole drafts with weight P(a | x). The token-level method buys efficiency, not a different target. Exactness breaks in practice through (1) B's approximation error, (2) the top-200 truncation, (3) unnormalized NCE outputs, (4) the λ/N reweighting in topic control. The formality B is also not trained on G's own continuations but on human GYAFC text, so it is not P_G(a | prefix).

The paper contrasts FUDGE with "weighted decoding" (WDEC) and with PPLM. Both "greedily optimize for a on the immediate extension x_{1:i+1}" (section 3). FUDGE scores where the text is going, not what it already contains.

## Evidence

All with G = GPT2-Medium for couplets and topics, and a Marian es-en model for translation. Perplexity is measured with GPT, as in PPLM.

**Couplet completion** (Table 2; 154 Shakespeare prefix lines; success = meter + rhyme + sentence end, by the rule checker F):

| Method | Success | Grammar | Perplexity | Dist-1/2/3 |
|---|---|---|---|---|
| G | 0 | 0.52 | 44.3 ± 42.2 | .35/.74/.77 |
| FINETUNE | 0.21 | 0.44 | 55.8 ± 98.3 | .35/.74/.78 |
| PPLM | 0 | 0.54 | 60.8 ± 66.1 | .40/.78/.78 |
| FUDGE | 0.44 | 0.44 | 70.9 ± 89.4 | .40/.79/.78 |
| Shakespeare | 0.45 | 0.29 | 333.8 ± 418.9 | .44/.81/.79 |

- The fluency cost is large here: perplexity 44.3 → 70.9 (+60%) and grammar 0.52 → 0.44. With Transformer-XL perplexity: 84.8 → 137.5 (Table 16).
- FUDGE beats FINETUNE on success with p < 0.0001, McNemar test (appendix F).

**Topic control** (Table 4; 7 topics × 20 prefixes × 3 samples = 420 generations of 80 tokens; success = distinct words from a held-out bag W' that appear):

| Method | Success | Grammar | Perplexity | Dist-1/2/3 |
|---|---|---|---|---|
| G | 0.22 | 0.81 | 37.1 ± 26.9 | .35/.78/.92 |
| FINETUNE | 0.28 | 0.74 | 24.9 ± 13.7 | .29/.70/.88 |
| WDEC | 0.14 | 0.59 | 33.8 ± 33.7 | .16/.42/.55 |
| PPLM | 0.48 | 0.78 | 43.1 ± 23.7 | .35/.78/.92 |
| FUDGE (λ = 4) | 0.59 | 0.79 | 40.7 ± 26.3 | .34/.75/.91 |

- FUDGE vs PPLM on success: p = 0.04, Wilcoxon matched pairs (appendix F). The margin over PPLM is modest.
- PPLM was run "without reranking for fair comparison" (4.2.1).
- Low perplexity is not fluency here: FINETUNE and WDEC repeat the bag words. With Transformer-XL, WDEC's perplexity is 7802.4 (Table 17).

**Human evaluation, topic** (Table 5; Mechanical Turk, 3 workers per pair, 420 pairs per comparison; on-topic fraction, fluency 1-5):

| Pair | On-topic | Fluency |
|---|---|---|
| G vs FUDGE | 0.16 vs 0.78 | 4.11 vs 4.30 |
| FINETUNE vs FUDGE | 0.24 vs 0.76 | 3.95 vs 4.22 |
| WDEC vs FUDGE | 0.49 vs 0.75 | 2.50 vs 4.21 |
| PPLM vs FUDGE | 0.45 vs 0.74 | 4.05 vs 4.16 |

**Strength λ vs fluency** (Table 19, main topic set):

| λ | Success | Grammar | Perplexity |
|---|---|---|---|
| 2 | 0.49 | 0.79 | 38.6 |
| 4 | 0.59 | 0.79 | 40.7 |
| 8 | 0.76 | 0.74 | 56.5 |

Doubling λ from 4 to 8 buys +0.17 success at +39% perplexity. "Success and perplexity both increase as the conditioning strength λ increases."

**The greedy present-tense baseline collapses** (Table 13, WDEC adds a constant λ_WDEC to the logit of each bag word; validation fantasy bag, 60 samples):
- λ_WDEC = 4: success 0.57, Dist-1 0.33.
- λ_WDEC = 8: success 1.90, Dist-1 0.04, grammar 0.47.
- λ_WDEC = 16 and 32: Dist-1 0.01.
- "WDEC frequently degenerates into repeating the given words in the bag W, despite tuning λ_WDEC" (4.2.2). Table 29 shows "law law law law ..." and "yin yin yin ...".

**Candidate set size** (Table 20): top-100 / 200 / 400 give success 0.54 / 0.59 / 0.61 and perplexity 48.9 / 40.7 / 49.4. 200 is the main setting.

**Predictor architecture barely matters** (Tables 14-15): a homogenized predictor gives couplet success 0.39 vs 0.44, and topic 0.62 vs 0.59.

**Formality in translation** (Table 8; BLEU against two fluent references; formality from a GYAFC classifier trained on a different domain):

| Method | BLEU (no fine-tune) | Formality | BLEU (fine-tuned) | Formality |
|---|---|---|---|---|
| G | 16.98 | 0.45 | 22.03 | 0.41 |
| G + ST | 7.87 | 0.96 | 9.63 | 0.97 |
| FUDGE | 17.96 | 0.51 | 22.18 | 0.48 |

- PPLM on the fine-tuned G: BLEU 21.94, formality 0.40 (Table 11).
- The effect is small: formality +0.06 to +0.07. The paper's examples show that it "often simply corrects punctuation or capitalization" (Table 9). Formality vs G: p < 0.0001, paired t-test.
- G + ST is the only post-hoc, black-box baseline in the paper: it rewrites G's finished output with a T5 style-transfer model. It reaches near-perfect formality and less than half the BLEU, because the rewriter does not keep the meaning.

**Speed.** The full test set of each task takes "no more than 15 minutes on a single Quadro RTX 6000 GPU" (section 3). PPLM "takes a few hours compared to FUDGE's 15 minutes for the full set of 420 generations" (4.2.2).

**Rerank or sample-then-filter baseline: none.** The paper only says (section 3): "it is likely that augmenting FUDGE with reranking approaches such as rejection sampling could improve output quality at the cost of compute time, although we do not comprehensively evaluate such extensions in this work." The introduction dismisses rejection sampling from P(X) as "highly inefficient in practice", with no number. So the paper gives **no evidence** on how best-of-N compares with token-level tilting.

## Available through `claude -p` / Agent SDK?

No, not as published. FUDGE needs G's full next-token distribution (at least the top 200 log-probabilities) at every step, and it needs to choose the next token itself. `claude -p` and the Agent SDK expose neither logits nor log-probabilities nor per-token sampling. The paper's claim of "access only to G's output logits" is still more access than we have.

What is available:
- The **sequence-level equivalent of the same target**: sample N whole drafts and select or resample with weight B(x)^λ. By the telescoping above, this targets the same P(x | a) with no logits, because Claude's own sampling supplies the P(x) factor.
- The **future-discriminator idea**: a small model, trained on prefixes labelled with the final text's attribute, that scores partial drafts. It runs entirely outside Claude, on streamed text.

## What it implies for the interface theory

All of this section is my inference unless it cites a table.

**1. Token-level and draft-level tilts have the same target. They differ in cost and reach.** With an exact future discriminator and λ = 1, FUDGE samples P(x)P(a|x)/P(a). Best-of-N with resampling weights P(a|x)^λ (sampling-importance-resampling) targets P(x)P(a|x)^λ / Z, and it needs no logits. The difference is how far N samples can move the distribution.
- Selection over N drafts carries at most log2 N bits per reply. That is about 3 bits for N = 8.
- A known result outside this paper: the KL divergence of best-of-N from the base distribution is at most log N − (N−1)/N. That is about 1.2 nats for N = 8.
- Token-level tilting has no such cap. That is why FUDGE reaches 0.59 topic success, and a property absent from almost all of Claude's drafts cannot be reached by selection.
- Consequence: draft selection can only pick among what Claude already tends to write. It cannot make Claude write something it rarely writes. For our use this is acceptable, even desirable: the state should modulate Claude, not author for it.

**2. Chunk-level tilt via streaming, interruption and continuation.** This is the closest available analogue of a per-token tilt. It is a particle filter over sentences. Algorithm:
- Start N parallel calls on the same context.
- Read the streams. At a chunk boundary (end of a sentence or a clause), score each partial draft with a future discriminator V_s(prefix) ≈ P(state-fit of the final reply | prefix). FUDGE is the reason the scorer must be a future predictor.
- Keep one prefix, by argmax or by resampling with weight V^λ. Interrupt the others.
- Launch N new calls that continue from the accepted prefix.
- With K boundaries per reply, the cap rises to K · log2 N bits.

Costs, per reply of length L with K chunks:
- Output tokens: about N · L, the same as best-of-N, if the losing streams are killed at each boundary.
- Input tokens: about K · N re-reads of the whole context plus prefix.
- Latency: K sequential rounds. Each round costs a call start-up plus the time to generate one chunk. Best-of-N is one round. The start-up time of `claude -p` must be measured locally before choosing K. For a spoken reply, K = 1-3 is the realistic range.
- Rate limits: N parallel calls per round count against the subscription.
- A cheaper variant is "monitor and veto": run one stream, score each finished sentence, and only interrupt and restart (with M candidates) when V falls below a threshold. Cost then scales with the rejection rate, and latency is paid only on rejection. This is a threshold filter, like GeDi's τ, not a smooth tilt.
- In a voice pipeline, accepted sentences can be spoken while the next chunk is being chosen. That hides part of the latency.

**3. The continuation seam is the weak point. It is untested.**
- The CLI and the Agent SDK do not, to my knowledge, expose an assistant-prefill parameter. I have not verified this.
- It is also unknown whether an interrupted partial assistant message persists in a resumable session. This must be tested.
- If it does not persist, the accepted prefix has to be passed back as user-turn text ("continue this reply: ..."). Then Claude reads its own words as quoted material from someone else. That changes the conditioning, invites rephrasing or commentary at the seam, and is a different thing from Claude continuing its own turn.
- If session resume does keep the partial turn, the seam is cleaner. This one test decides whether chunk-level tilting is usable.

**4. What FUDGE says about the scorer.**
- Score the future, not the present. The WDEC rows show what a present-tense, keyword-like score does under strength: λ_WDEC = 8 gives Dist-1 0.04 and "law law law" (Tables 13, 29). A sayability score that rewards affect-laden wording in each chunk will do the same at chunk level: it will select chunks that say the state.
- Train the scorer FUDGE's way: generate many full Claude drafts offline, label each finished draft with the state-dependent score, and train a small prefix model on every (prefix, final label) pair. That is cheap and stays outside Claude.
- Keep λ low. Table 19 shows the trade: going from λ = 4 to 8 buys +0.17 success for +39% perplexity. We cannot even measure Claude's perplexity (no log-probabilities), so a fluency guard has to be external, for example a local LM or a Claude-as-judge call.

**5. The text-channel question.** Choosing outputs by a state-dependent score puts state-shaped text into the history that Claude reads later.
- This is **not** "the state in words" in the sense of Principle 4. No label, value or state name is written by the engine. Every selected token is one Claude itself produced. Selection moves probability mass among Claude's own candidates.
- It **is** a text channel. The history carries up to log2 N bits per reply (K · log2 N with chunking) of information about the state. Claude can in principle read the state back from the tone of its own past turns. The emotion-concepts note (anthropic-emotion-concepts.md) says Claude's emotion representations are local and continuity comes from attention to earlier text. If so, the selected history is exactly how the state would persist in Claude's processing. That is arguably the intended route ("the state reaches Claude only by changing how it processes"), but it is mediated by text, and the P1 null (numbers in the prompt changed nothing) does not tell us whether this route works.
- Three risks follow:
  - (a) **Lexical leakage.** A scorer that is sensitive to affect words will pick drafts in which Claude names the state ("I'm a bit on edge"). The state then enters the history in words, chosen by the engine through Claude's mouth. This is the WDEC failure in a different form. Mitigation: penalize explicit affect labels in the score, or score only non-lexical features (length, hedging, pace, topic distance).
  - (b) **Compounding.** State-tinted history makes Claude's next drafts more state-tinted. Selection then pushes further. This is a feedback loop that can drift.
  - (c) **Seam text.** Chunk continuation passed as user text is engine-written context. It must be verbatim Claude output and nothing else, with no framing beyond "continue".
- Measure: an ablation with the same history text but a shuffled state, as in the S1 transcript-only baseline.

## Verdict

**watch**: not usable as published (it needs per-token logits). Adopt its design rule for our scorer: score partial drafts by a prefix-to-final-attribute "future discriminator", at a low strength, over Claude's own sampled drafts or chunks.
