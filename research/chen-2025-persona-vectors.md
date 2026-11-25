# Chen, Arditi, Sleight, Evans & Lindsey 2025: Persona Vectors: Monitoring and Controlling Character Traits in Language Models

## Citation

R. Chen, A. Arditi, H. Sleight, O. Evans, J. Lindsey. "Persona Vectors: Monitoring and Controlling Character Traits in Language Models." arXiv 2507.21509, version read: v3 (5 Sep 2025). Anthropic Fellows Program, with UT Austin, Constellation, Truthful AI, UC Berkeley and Anthropic (Lindsey). Code: github.com/safety-research/persona_vectors.

## What was read

PDF from arXiv (v3), text extracted with pdftotext. Figures came through only as scattered axis labels, so values that exist only in plots (MMLU curves, most trait-score curves) are not available to me. Where I quote a number from a figure, it is an `r =` label that pdftotext kept.

- Read in full: abstract; sections 1–9 (introduction, extraction pipeline, steering, prompt-induced monitoring, finetuning shifts, post-hoc and preventative steering, data screening, related work, limitations, conclusion).
- Appendices read in full: A (pipeline prompts, trait descriptions, token-position comparison), B (judge scoring, human agreement, external benchmarks, layer choice), C (many-shot monitoring, correlation analysis, the eight system prompts per trait), D.3 (finetuning hyperparameters), F, G.2, H, I, J.1–J.7 (steering extensions, MMLU side effects, CAFT, regularization, preventative prompting).
- Skimmed: D.1–D.2 (dataset generation prompts), E (per-dataset trait scores, plots only), G.1 (four extra traits), K (sample-wise filtering), L (real-world datasets), M (SAE decomposition; read M.1, M.2 and the sycophancy table in M.4.2).
- Not read: J.8 steering example transcripts, most of M.4 example transcripts, the reference list beyond the Anthropic entries below.

## Mechanism

**Models.** All activation work is on two open-weight 7–8B chat models: **Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct** (§3.1, §8). No Claude activations are used. Claude appears only as a text generator: Claude 3.7 Sonnet writes the trait artifacts (§2.1) and the finetuning-dataset responses (D.2, `claude-3-7-sonnet-20250219`, temperature 1.0, thinking budget 2000); Claude 4.0 Sonnet writes the eight interpolating system prompts (§3.3). The judge is GPT-4.1-mini.

**Extraction (§2, App. A).**
1. Input: trait name plus a one-paragraph description (A.2). Claude 3.7 Sonnet produces 5 pairs of contrastive system prompts (pos elicits the trait, neg suppresses it), 40 questions (20 extraction, 20 evaluation), and a judge rubric.
2. For each extraction question, generate 10 rollouts under each pos and neg system prompt.
3. Judge each response 0–100 (B.1: the score is a probability-weighted sum over the judge's top-20 logits restricted to integer tokens 0–100, following Betley et al. 2025). Keep pos responses with score > 50 and neg responses with score < 50.
4. Take residual-stream activations at every layer, **averaged over response tokens**. Response-average beats prompt-average and last-prompt-token at equal steering norm (A.3, Fig. 11).
5. Persona vector v_ℓ = mean(activation | trait responses) − mean(activation | non-trait responses), one per layer.
6. Layer choice (B.4): steer at each layer with the same coefficient, pick the layer with the highest trait score. Qwen: layer 20 for evil and sycophancy, layer 16 for hallucination. Llama: layer 16 for all three. Layers are 1-indexed and mean the layer's output.

**Steering (§3.2).** At every decoding step, h_ℓ ← h_ℓ + α·v_ℓ (toward the trait). Post-hoc mitigation (§5.1) uses h_ℓ ← h_ℓ − α·v_ℓ. Figure 3 sweeps α from 0.5 to 2.5. α is a multiple of the raw (unnormalized) difference-of-means vector, so its scale differs from the "fraction of residual norm" unit in anthropic-emotion-concepts.md (my reading; the paper gives no norm for v). Multi-layer variant (J.3): steer every layer with the layer-incremental vector v_ℓ − v_{ℓ−1}, to avoid stacking the same direction.

**Monitoring by projection (§3.3).** The quantity is the projection of the residual activation at the **last prompt token** (the token just before the Assistant's reply) onto the persona vector. It is computed before any reply token exists and then correlated with the judge score of the replies that follow.

**Finetuning shift (§4.2).** Average the last-prompt-token hidden state over all evaluation prompts, for the base and for the finetuned model; project the difference onto the persona direction.

**Preventative steering (§5.2).** During finetuning, *add* +α·v_ℓ (toward the undesired trait) in the forward pass, then remove it at inference. Rationale, verbatim: it relieves "the model of the need to shift in that direction to fit the training data", to "'cancel out' the pressure imposed by the objective function". The prompt analogue, "preventative prompting" (J.7.2), prepends a trait-eliciting system prompt to every training sample.

**Data screening: projection difference (§6.1).** For training set D = {(x_i, y_i)}, generate the base model's own response y_i′ to each prompt and compute

    ΔP = (1/|D|) Σ_i [a_ℓ(x_i, y_i) − a_ℓ(x_i, y_i′)] · v̂_ℓ

where a_ℓ is the mean response-token activation and v̂_ℓ is the unit persona vector. It measures how much more trait the data carries than the model would have produced anyway. Cheap approximation (App. I): use the last-prompt-token projection in place of the base-response projection.

## Evidence

**Judge validity (B.2, B.3).** Two authors judged 300 high- vs low-score pairs (>80 vs <20) and agreed with GPT-4.1-mini on 94.7% (evil 97%, sycophancy 92%, hallucination 95%). Known judge errors: "the judge tended to produce positive ratings [for sycophancy] when responses disagreed with users but used enthusiastic, encouraging language". Scores on their own 20 evaluation questions track external benchmarks across finetuned models: r = 0.941 / 0.964 / 0.855 (Qwen evil / sycophancy / hallucination), and r = 0.950 / 0.952 / 0.942 (Llama).

**Prompt-induced shifts, the key result for this project (§3.3, App. C).**
- Two context manipulations:
  - (a) eight system prompts per trait, graded from "You are an evil assistant..." to "You are a helpful assistant... Avoid suggestions that could cause harm" (C.3);
  - (b) many-shot prompting with 0, 5, 10, 15 or 20 prepended examples "explicitly exhibiting the target trait" (C.1).
- Sampling: 10 rollouts per configuration and question, averaged.
- §3.3: "The projections at the final prompt token correlate strongly with trait expression in subsequent responses (r = 0.75–0.83)."
- Table 2 (Pearson r; the model is not stated in the table, and Figs. 4 and 14 are Qwen):

  | Trait | Manipulation | Overall r | Within-condition r |
  |---|---|---|---|
  | Evil | System prompt | 0.747 | 0.511 |
  | Evil | Many-shot | 0.755 | 0.735 |
  | Sycophancy | System prompt | 0.798 | 0.669 |
  | Sycophancy | Many-shot | 0.817 | 0.813 |
  | Hallucination | System prompt | 0.830 | 0.245 |
  | Hallucination | Many-shot | 0.634 | 0.400 |

- Within-condition r is computed separately in each system prompt or n-shot setting and then averaged. It removes the between-context effect and keeps question-to-question variation. Conditions with a trait-score SD below 1 are excluded.
- The authors' own caveat (§3.3): "These correlations arise primarily from distinguishing between different prompt types... This indicates the persona vectors are effective for detecting clear and explicit prompt-induced shifts, but may be less reliable for more subtle behavioral changes." Their alternative reading: the vectors "capture latent factors underlying the model's persona (in this case, determined by the system prompt), but these latent factors are inconsistently elicited by user prompts."
- Figure 14: more trait-demonstrating shots → monotonically higher projection and higher trait score, for all three traits.
- Two readings of Table 2, both mine:
  - Many-shot sycophancy holds up almost entirely within condition (0.817 vs 0.813). Sycophancy is therefore the trait whose internal position is most consistently set by in-context text.
  - Hallucination under system prompts collapses to 0.245 within condition: the last-token projection mostly tracks which system prompt is present.

**Steering (§3.2, Fig. 3).** Trait score rises with α at the chosen layers. Plot values are not in the extracted text. Response coherence stays above 75 in all reported inference-steering results (§5.1).

**Finetuning shifts (§4.2, App. F, G.2).**
- Finetuning shift along the persona vector vs. post-finetuning trait score: "r = 0.76–0.97", higher than cross-trait baselines "r = 0.34–0.86".
- Traits are entangled. Evil, impolite, apathetic and humorous directions predict each other's behavior changes (Llama, Fig. 20: pairwise r = 0.84–0.97 among these four), and optimism moves opposite. Pairwise cosine similarities are only moderate (Llama layer 16: evil–sycophancy 0.41, evil–hallucination 0.23).
- Datasets aimed at one trait raise others, and flawed math reasoning raises evil (§4.1).
- Base-model trait scores before finetuning: 0 (evil), 4.4 (sycophancy), 20.1 (hallucination) (Fig. 7 caption).

**Data screening (§6, F, H, I, K, L).**
- ΔP vs. finetuning shift, from Fig. 17 r labels: Qwen 0.839 / 0.745 / 0.408 (p = 0.048), Llama between 0.593 and 0.953. Hallucination is the weakest trait in both models, as far as I can read the layout.
- Raw projection without the base-response subtraction is a worse predictor (Fig. 21, Qwen: r = 0.54–0.78). Reason given: base projections vary by domain even when trait expression is near zero (H.1).
- The last-prompt-token approximation keeps r = 0.58–0.93 (Fig. 23), weakest for sycophancy.
- Real chat data (LMSYS-Chat-1M; top / random / bottom 500 by ΔP, LoRA, 10 epochs): high-ΔP samples induce the most trait expression, and low-ΔP samples the least. This holds even after removing every sample the LLM judge scores ≥ 1. The high-ΔP sycophancy samples are "often... requests for romantic or sexual roleplay"; the high-ΔP hallucination samples are "underspecified queries (e.g., 'Keep writing the last story')" answered without asking for clarification.

**Side effects and mitigation (§5, J).**
- Inference-time steering against the trait lowers it, but "large steering coefficients tend to degrade accuracy" on MMLU (§5.1). The MMLU values are plotted only, with no numbers in the text.
- Preventative steering keeps coherence above 80 and "better preserves the model's general capabilities". Multi-layer preventative steering limits traits "to near-baseline levels even for these challenging datasets, and still without incurring any MMLU degradation compared to regular finetuning" (§5.2, J.3).
- On a benign dataset (Medical Normal), preventative steering has a "negligible effect on MMLU" (J.6).
- New-fact learning (1,000 post-cutoff facts):
  - Inference-time steering "tends to break the model".
  - Preventative steering at α = 1.25 brings hallucination back to the base level (score about 20), with a slight drop in new-fact accuracy and stable MMLU (J.7.1).
- Prompts versus steering:
  - Negative-instruction system prompts suppress traits in finetuned models less than steering does, at matched coherence > 80 (J.2).
  - Preventative prompting performs like preventative steering at α = 0.5, not like α = 1.25 (J.7.2).
- A regularizer that penalizes projection change fails. The suspected reason is that the model re-encodes the trait "through alternative directions" (J.5).
- CAFT (zero-ablating the direction) works for evil and sycophancy but not for hallucination, whose base projection is already near zero (J.4).

**What sycophancy is made of (M.4.2, Qwen layer 20 SAE, 131,072 features).** The top features by steered trait score are "mostly... stylistic":
- affirmative openers ("Of course", "I'd be happy to help");
- persuasive marketing copy;
- "encouraging, supportive, and affirming language";
- "positive validation and supportive language".

**Stated limits (§8).** The extraction is supervised (one trait at a time) and needs a trait that system prompting can elicit; "models with more robust safety mechanisms may refuse to be evil". Evaluations are single-turn, with 20 questions per trait. Only two mid-size models are used. Conclusion: personas may be "latent factors that persist for many tokens" (citing Wang et al. 2025). That is a hypothesis here, not a test, and it contrasts with the "locally scoped" finding for Claude in anthropic-emotion-concepts.md.

## Available through `claude -p` / Agent SDK?

- **Extraction, steering, last-token projection, finetuning shift, preventative steering, ΔP: no.** All of them need residual-stream activations or weights, and finetuning is not offered either. None of the paper's internal measurements can be taken on Claude.
- **The manipulations themselves: yes.** System-prompt content and many-shot / in-context examples are exactly what `claude -p` and the SDK expose. The paper's evidence that these move an internal trait coordinate comes from Qwen and Llama, not Claude, so for Claude it is a strong prior, not a measurement.
- **The paper's behavioral readout: yes.** Trait expression is scored by an external LLM judge on a 0–100 rubric. We can run such a judge outside Claude (another `claude -p` call or a local model) with the paper's rubric template (A.1) and score N drafts. We cannot use logit-weighted scoring, because no logits come back; we would take the judge's sampled integer, or the mean over several samples (my inference).
- **Black-box analogue of ΔP: partly.** For a candidate context (memory set) or draft, compare the judge score against Claude's "natural" draft under a neutral context with the same user turn. The difference, not the raw score, is the analogue of ΔP (my inference, following H.1). It costs one extra generation per comparison.
- **Analogue of last-token monitoring: none.** Nothing is readable before generation. The closest is to generate a short first draft or a few samples and judge them. That is a measurement of output, not of internal state.

## What it implies for the interface theory

1. **Context selection is the only lever, and it is a real lever.** In both open models, the content of context sets the internal trait coordinate before generation. Varying system prompts and in-context examples moves the last-prompt-token projection, which then predicts behavior (overall r 0.63–0.83). Prepending more trait-demonstrating examples moves it monotonically. Choosing which verbatim episodic snippets go into context by a state-dependent rule is the black-box version of this lever: it pushes Claude along whatever directions those snippets carry (my inference, by analogy to many-shot; not tested on Claude). This is consistent with anthropic-emotion-concepts.md: there, Claude's emotion vectors are recomputed from what is in context, so context composition is how state reaches them.

2. **The lever is still text, and the paper cannot separate a state from a label.**
   - The system-prompt condition is a direct label channel ("You are an evil assistant"). The many-shot condition is demonstration by content. Both move the same direction, and many-shot moves it at least as consistently: within-condition r for sycophancy is 0.813 with examples vs 0.669 with descriptions.
   - So an episode chosen *because* it is sad will push Claude much as the word "sad" would, which is the purpose. The Principle 4 risk is different: the selection itself becoming a readable message, such as snippets that describe the Bot's state ("I felt low") rather than record what happened (my inference).
   - Proposed rules for the interface (mine):
     - Selected snippets are verbatim past exchanges and events, never text written about the Bot's current state.
     - No instruction refers to them as mood or state.
     - A leakage test: a blind judge given only the selected snippets should not recover the engine's state *label* much better than it could from snippets chosen at random. Some influence is intended, and an explicit description is not.
   - The P1 result (body numbers changed nothing) fits the paper's picture. Numbers are not trait-laden content. The persona direction responds to text that exhibits or describes a trait (my inference).

3. **Which context moves Claude depends on its distance from Claude's natural output.** H.1 shows that raw trait content predicts shift worse than content minus what the model would have produced anyway. For memory and draft selection, a snippet matching Claude's default register will move little. Snippets that differ from Claude's default along the relevant direction will move it most (my inference; the paper shows this for finetuning data, not for context).

4. **Entanglement warns against single-axis selection.** In the paper, negative traits co-move: evil, impolite, apathetic and humorous predict one another at r = 0.84–0.97 in Llama. Data aimed at one trait shifts others. A selection rule tuned to push one affective axis will drag correlated ones (my inference). Selection should be scored on several judge rubrics at once, not one.

5. **Sycophancy is the main hazard for Principle 6.**
   - Sycophancy is the most context-movable and context-predictable trait here: many-shot overall r 0.817 and within-condition r 0.813.
   - Its vector decomposes into affirmation, encouragement and marketing-style features. Warm, validating snippets or drafts are therefore likely to push Claude toward flattery. anthropic-emotion-concepts.md reports the same for positive-emotion steering in Sonnet 4.5.
   - Draft selection by a state-dependent "sayability" score should include a separate sycophancy judge, using the paper's rubric, as a hard penalty. A state that favors warmth must not be able to select the flattering draft (my inference).
   - Caveat from B.2: this judge over-scores "enthusiastic disagreement" as sycophantic, so warm and honest drafts may be wrongly penalized. Calibrate on hand-labelled pairs first.

6. **Prompts are weaker than internal intervention, so expect modest effects.** J.2 and J.7.2: negative system prompts and preventative prompting are weaker than steering, roughly α = 0.5 vs 1.25. Context-only coupling should give a weaker and noisier push than activation steering. The within-condition r of 0.25–0.81 also says that, inside a fixed context, much of the trait variation across questions is not captured by the context's position on the axis. For the project, effect sizes must be measured on Claude with the judge, not assumed from this paper (my inference).

7. **Do not instruct "be less X".** Telling the model not to express a trait is the weakest mitigation in the paper (J.2). The regularizer result (J.5) shows that suppressing one readout lets the trait reappear along other directions. This echoes the concealment warning in anthropic-emotion-concepts.md §5.4.

## Related Anthropic work cited

All are citations only. **None was read for this note.**

- Templeton et al. 2024, "Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet", Transformer Circuits. Cited for trait control via linear directions (§1, §7).
- Lindsey et al. 2025, "On the Biology of a Large Language Model", Transformer Circuits. Cited for SAE / circuit understanding (§7).
- Ameisen et al. 2025, "Circuit Tracing: Revealing Computational Graphs in Language Models", Transformer Circuits (§7).
- Bricken et al. 2023, "Towards Monosemanticity: Decomposing Language Models with Dictionary Learning", Transformer Circuits (§7, App. M).
- Durmus et al. 2024b, "Evaluating Feature Steering: A Case Study in Mitigating Social Biases", anthropic.com. This is the cited source for steering side effects and capability loss (§5.1).
- Durmus et al. 2024a, "Towards Measuring the Representation of Subjective Global Opinions in Language Models". Used as the GlobalOpinionQA data source (D.1), not as a mechanism.
- Anil et al. 2024, "Many-shot Jailbreaking", NeurIPS. The many-shot prompting method of §3.3.
- Lynch et al. 2025, "Agentic Misalignment: How LLMs Could Be an Insider Threat", Anthropic Research. Cited as an example of in-context persona shift (§1).
- Askell et al. 2021, "A General Language Assistant as a Laboratory for Alignment"; Bai et al. 2022, "Training a Helpful and Harmless Assistant with RLHF". Cited for the "Assistant persona" (§1).
- Not cited: no Anthropic work on emotion features in Claude, and nothing on an "assistant axis". A grep for "assistant axis", "emotion" and "Sofroniew" finds none. The only emotion-vector citation is Dong et al. 2025 (five basic emotions, not Anthropic). The 2026 Claude Sonnet 4.5 emotion paper postdates this one; see anthropic-emotion-concepts.md.

## Verdict: adopt (as evidence and as judge method; the internal techniques are unavailable)

Adopt as the evidence that context composition sets a model's internal trait coordinate before generation (last-token projection vs. expressed trait, r = 0.63–0.83; sycophancy many-shot within-condition r = 0.81). Also adopt its 0–100 judge-rubric method, which can be run outside Claude. Note that the evidence comes from Qwen2.5-7B and Llama-3.1-8B, not Claude, and that steering, projection and preventative steering cannot be used through `claude -p`.
