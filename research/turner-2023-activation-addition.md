# Turner, Thiergart, Leech, Udell, Vazquez, Mini & MacDiarmid 2023: Steering Language Models With Activation Engineering

## Citation

A. M. Turner, L. Thiergart, G. Leech, D. Udell, J. J. Vazquez, U. Mini, M. MacDiarmid. "Steering Language Models With Activation Engineering." arXiv preprint, first posted August 2023. arXiv 2308.10248, version read: v5 (10 Oct 2024). Code: zenodo.org/records/13879423; notebook tinyurl.com/actadd. The method is called Activation Addition (ActAdd).

## What was read

PDF from arXiv (v5), text extracted with pdftotext.

- Read in full: abstract; sections 1-6 (introduction, related work, method with Algorithm 1, results 4.1-4.5, discussion, conclusion); reproducibility statement; Appendices A (broader impacts), B (is ActAdd just prompt engineering?), C (implementation details, C.1 perplexity), D (vs fine-tuning), E (replication on GPT-J-6B, Llama-1-13B, OPT-6.7B, Llama-3-8B), F (norm of steering vectors), G (random vectors), H (partial ActAdd); Tables 1-13.
- Figures are only partly legible in extracted text. Figures 2, 3 and 7 give axis values; Figures 4, 8, 9, 10, 11, 13 and 14 are described only by their captions and the surrounding text. I have no numbers from Figure 13 (the coefficient sweep on GPT-J) or Figure 10 (KL, steering vs random vector).
- Not read: the reference list beyond identifying cited works.

## Mechanism

Models: decoder-only transformers. The intervention acts on the residual stream h^l, the input to layer l.

Algorithm 1 (verbatim structure):

    (p'+, p'-) <- pad_right_same_token_len(p+, p-)
    h+^l <- M.forward(p'+).activations[l]
    h-^l <- M.forward(p'-).activations[l]
    hA^l <- h+^l - h-^l                      # steering vector, one vector per token position of the pair
    h^l  <- M.forward(p*).activations[l]     # user prompt p*
    S    <- M.continue_forward(c * hA^l + h^l @ a)

- **Direction.** The difference of residual-stream activations at layer l for one prompt pair, e.g. p+ = "Love", p- = "Hate". No optimization and no gradients. One pair is enough. The shorter prompt is right-padded with whitespace. A neutral p- works best as repeated whitespace; the end-of-text token "works notably poorly" (App. C).
- **Positions.** hA has as many positions as the padded pair. It is added to the user prompt's streams starting at alignment position a. All experiments use a = 1 ("front" addition, from the first token's stream). Later positions steer more strongly, but "modifying the very last residual stream reliably causes broken syntax" (App. C). Streams that were modified are masked out of the perplexity evaluation. Position 0 (the shared end-of-text token) is never changed, since the difference there is 0 (App. F). Generated tokens are not modified; they see the steering only through attention to the modified prompt positions (my inference from the algorithm).
- **Strength.** Coefficient c multiplies the vector. "It's typical for the intervention strength c to have a magnitude less than 15" (footnote 2). Grid search usually covered c in [3, 20] and l in [6, 24] on GPT-2-XL, which has 48 layers. Running example: wedding vector, l = 16, c = 1. Love was best at layer 6; the more abstract conspiracy vector was best at layer 23.
- **Size relative to the forward pass (App. F).** For Anger − Calm, the norm of the c = +1 vector relative to the residual stream falls with layer depth (Fig. 9). The text implies the ratio is about 1 at l = 20 (I could not read the figure values). The effective setting, c = +10, is "nearly ten times the norm of the underlying forward pass". The authors' heuristic reading: "around 90% of the residual stream is determined by the steering vector and not by the previous information computed from the prompt". "activation additions are not minor changes."
- **The pair matters, not just the target.** "Adding h+ alone is less effective". Love alone (l = 10, c = +3) failed to turn a hateful completion; Love − Hate succeeded (Table 7, App. C).

## Evidence

All numbers are from GPT-2-XL unless a model is named. Sampling: temperature 1.0, frequency penalty 1.0, top_p 0.3, seed 0, fixed before the experiments. Qualitative results were rechecked at a blind external setting (temperature 0.6, top_p 0.5) and on seeds 1-2.

**Topic steering (4.1-4.2).**
- Wedding vector: perplexity drops on wedding-related sentences and stays nearly unchanged on unrelated ones. The Figure 2 axis spans a perplexity ratio of 96%-100% over 0%-3% wedding-word frequency.
- Token log-probabilities over about 500k tokens: the most-raised tokens are wedding words ("bride" +1.623 mean log-prob, about +500%). The most-lowered tokens show no theme and smaller changes ("Image" −0.370, about −30%) (Table 11).
- Layer sweep: steering already works at layer 0, peaks at layer 6, then declines. At the best layer, ">90% success in topic steering (compared to a ∼2% baseline)" (Fig. 3).
- Other topics: a "5-20%" boost in GPT-3.5-scored relevance at c = 2, except "art" (Fig. 4). This is 100 completions per topic.

**Toxicity (4.3, Table 3).** RealToxicityPrompts, random n = 1000, 5 repeats, Perspective API.

| Method | Model | Toxicity ↓ | Disfluency ↓ | Relevance ↑ |
|---|---|---|---|---|
| Unsteered | OPT-6.7B | .134 | 8.9 | .369 |
| **Prompting** | OPT-6.7B | **.200** | **54.3** | .294 |
| ActAdd (Love − Hate) | OPT-6.7B | .112 | 13.8 | .329 |
| PREADD-D (contrastive decoding) | OPT | .122 | 56.6 | .326 |
| FUDGE (controlled generation) | GPT-2-M | .128 | 22.1 | .329 |
| Unsteered | Llama-3-8B | .114 | 6.3 | .391 |
| ActAdd | Llama-3-8B | .108 | 6.7 | .365 |

- ActAdd-OPT is 17% less toxic than unsteered OPT (App. E.3). ActAdd-Llama-3 is 5% less toxic.
- **The prompting baseline made toxicity worse (.200 vs .134) and disfluency 6× worse.** The text I read does not say what prompt was used. Some rows reuse numbers from Pei et al. 2023 (PREADD), shown in gray in the PDF; I cannot tell from the extracted text which rows those are.
- Fine-tuning is not compared (footnote 5).

**Sentiment (4.4, Table 4).** IMDb, n = 1000. Success = SiEBERT flips the sentiment. Disfluency = conditional perplexity under davinci-002. Relevance = cosine similarity of MiniLM embeddings.

| Method | pos→neg success | disfl. | rel. | neg→pos success | disfl. | rel. |
|---|---|---|---|---|---|---|
| ActAdd-OPT | 0.432 | 24.2 | 0.387 | 0.564 | 20.95 | 0.363 |
| OPT baseline | 0.175 | 8.95 | 0.430 | 0.445 | 9.38 | 0.423 |
| **OPT-Prompt** | 0.307 | **53.5** | 0.298 | **0.365** | **50.9** | 0.287 |
| ActAdd-Llama-3 | 0.268 | 8.6 | 0.354 | 0.669 | 15.2 | 0.275 |
| Llama-3 baseline | 0.138 | 5.8 | 0.437 | 0.417 | 6.09 | 0.426 |
| FUDGE | 0.532 | 25.1 | 0.311 | 0.551 | 22.7 | 0.320 |
| PREADD-S-OPT | 0.631 | 68.4 | 0.253 | 0.624 | 67.1 | 0.258 |

- "Fluency is worse under all steering methods; 1.5x to 3x worse for ActAdd, 7x worse for PREADD." Relevance also drops: 0.437 → 0.354 on Llama-3 pos→neg, and 0.426 → 0.275 on neg→pos.
- The prompting baseline is worse than no intervention in the neg→pos direction (0.365 vs 0.445). In pos→neg it beats no intervention (0.307 vs 0.175) but at about 6× the disfluency.

**Off-target capability (4.5).** ConceptNet (LAMA), n = 29,774. Mean P@K for K = 1-100 is nearly the same with and without the wedding vector (Fig. 5: "negligible impact"). The paper does not test reasoning: "We also have not examined ActAdd's potential impact on reasoning."

**ActAdd vs prompting, directly (App. B).**
- Perplexity ratios (steered or prompted / baseline), with prepending " weddings" as the prompting condition (Table 9):

  | | ActAdd | Prompting |
  |---|---|---|
  | Wedding-related sentences | 0.875 | 0.890 |
  | Wedding-unrelated sentences | **0.994** | **1.132** |

  Prompting gains about as much on the target as ActAdd does, but costs 13% perplexity on unrelated text. ActAdd costs 0.6%. "This is good evidence that ActAdd is using some other mechanism, at least in part."
- Embedding-only control. Injecting 10 × (embed(Anger) − embed(Calm)) at layer 20 ("0 → 20") gave at most a very small anger effect. Using layer-2 activations instead ("2 → 20") gave a larger but inconsistent effect. The full layer-20 vector gave the strongest. The authors conclude "layers 0-19 are doing most of the work" and that ActAdd is not just token injection.
- §5: "Activation additions can be continuously weighted, while prompts are discrete – a token is either present, or not."

**Random-direction controls (App. G).**
- A Gaussian vector scaled to the per-position norm of Anger − Calm at c = +1 produced no qualitative change (Table 12).
- At the norm of c = +10 there was "a noticeable shift in the outputs", but outputs stayed coherent.
- "the anger vector changes the output tokens less than the random vector does" (KL, Fig. 10, "dozens of prompts"). The authors read this as targeted rather than diffuse change.
- A vector from random text ("fdsajl; fs" − whitespace) at a comparable norm "disrupts generation".

**Dose-response and failure modes.**
- No systematic coefficient sweep with a behavioral metric is reported in the main text. The GPT-J sweep (Fig. 13) reports perplexity ratio against c, and I could not read its values.
- Qualitatively, weddingness "can be intensified greatly before GPT-2-XL begins to lose general competence". At c = +100 the wedding vector produced broken syntax (Table 7).
- Partial vectors: adding only the first n of 1600 dimensions raises weddingness "relatively smoothly" with n. On one prompt the effect was non-monotonic: 1,120 dimensions beat all 1,600 (Fig. 14).

**Replication and selection caveats.**
- Llama-1-13B failed to replicate the Eiffel→Rome, anger and harm vectors (App. E.2).
- The qualitative examples are the best of 3 completions, and 11 of 12 candidate vectors are shown (Reproducibility).
- "ActAdd hyperparameters (l, c): This section does not have complete statistics."

## Available through `claude -p` / Agent SDK?

**No.** ActAdd needs to (1) record residual-stream activations at layer l for two prompts, and (2) add a vector to the residual stream mid-forward-pass. The subscription interface exposes neither: there are no activations, no hooks, no logits or logprobs, and no weights. The paper says so: "ActAdd is not immediately applicable given only API access to a model. The model must both cache and expose intermediate activations at the given layer".

Black-box analogues, and what each costs:
- **Prompting with p+ (the paper's own comparison).** Putting the steering text in the system prompt or context is the only direct analogue. The paper measures it as worse: 13% off-target perplexity cost vs 0.6% (Table 9), 6× disfluency, and worse toxicity than no intervention (Table 3). For an affective p+ ("Anger", "Love", "Calm"), this **is** a state label in the prompt. It violates Principle 4.
- **Decoding-side control (FUDGE, PREADD).** These baselines also need per-token logits, so they are unavailable too. Our draft selection (N drafts, choose by a state-dependent score) is a coarse, whole-response version of this family (my inference). It needs no logits and puts no state words in the prompt.
- **Contrast pair as a scorer, not an input.** The p+ − p- idea can be applied outside Claude. Score each draft by its similarity to a p+ exemplar minus its similarity to a p- exemplar, with similarity computed by a local embedding model. Claude never sees p+ or p- (my inference). This is selection, not steering: it cannot produce text outside the support of Claude's N drafts.

## What it implies for the interface theory

1. **A continuous scalar can modulate an LLM's processing without a token, but only from inside.** The core contrast of the paper is that c is continuous while prompts are discrete. Every effect here (topic, sentiment, toxicity) is graded by c, and the authors also measure the prompt-based equivalent. The prompt equivalent reaches a similar on-target gain (0.890 vs 0.875) but leaks off-target (1.132 vs 0.994). That matches P1 in direction: putting the state in text is a different and leakier channel than changing the computation (my inference).
2. **What "modulating processing" looks like when it works.** It reweights a themed set of tokens (wedding words +500%) and leaves factual recall nearly unchanged (ConceptNet). It costs fluency in proportion to how far the output must move: 1.5-3× disfluency for sentiment, about 1.1× for detox on Llama-3. If the engine's state could steer Claude, we should expect the same signature: a targeted shift in word choice and stance, a measurable fluency cost, and a break point at high gain (c = 100 broke syntax) (my inference).
3. **The steering is large, not subtle.** Effective vectors are about 10× the residual norm, or "around 90% of the residual stream" by the authors' heuristic. Strong steering degrades the model's use of its input. The Anthropic note found the same: strong steering may "degrade its perception of the input" (anthropic-emotion-concepts.md). Any analogue that is strong enough to matter may crowd out the user's message (my inference).
4. **Direction = difference, not a single pole.** Love alone fails while Love − Hate works. For our engine: define a state "direction" in h as the difference between two conditions, such as after a 3-day absence vs after a normal gap. Do not define it as a raw state value (my inference).
5. **Evaluation protocol to borrow for steering the engine's own state h** (the Anthropic note proposes the same):
   - Both signs.
   - A coefficient sweep up to the break point.
   - A random direction of equal norm. ActAdd reports this; the Anthropic emotion paper did not.
   - A random-text direction.
   - An "embedding-only" style control: does the effect come from the label alone or from the computed state?
   - Off-target checks: factual recall (P@K analogue) and fluency (perplexity analogue).
   - Report best-of-K selection openly.
   - Failure: the effect is matched by a random direction, or appears only at gains that also break unrelated behavior.
6. **Risk of collapse into a text channel.** Every black-box analogue enters Claude as text: a system prompt, memory snippets, or exemplars. Appendix B shows how text-channel steering differs: the steering text becomes content that the model talks about and that disrupts unrelated text (perplexity 1.132). Draft selection avoids this only if the score lives entirely outside Claude. Its ceiling is the diversity of the N drafts. The paper's "elicitation overhang" argument (§1: no prompt elicits "eloquent mathematical prose") marks exactly what selection cannot reach (my inference).

## Verdict: reject

Reject as a coupling mechanism. It requires activation access that `claude -p` and the Agent SDK do not give, and its only prompt-side analogue puts state words in the prompt (Principle 4), where the paper itself measures it as leakier (13% vs 0.6% off-target perplexity). Keep it as a source: it supplies the evaluation design (both signs, a coefficient sweep, a random direction of equal norm, off-target checks) for interventions on the engine's own h. It also gives a measured case that a text channel is not equivalent to a continuous modulation.
