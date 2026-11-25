# Li & Liang 2021; Lester, Al-Rfou & Constant 2021: Prefix-Tuning and Prompt Tuning (soft prompts)

## Citation

- X. L. Li, P. Liang. "Prefix-Tuning: Optimizing Continuous Prompts for Generation." arXiv 2101.00190. Version read: v1 (1 Jan 2021). Published at ACL-IJCNLP 2021. The ACL version may differ from v1 in details and numbers; everything below is from v1.
- B. Lester, R. Al-Rfou, N. Constant. "The Power of Scale for Parameter-Efficient Prompt Tuning." arXiv 2104.08691. Version read: v2 (2 Sep 2021). Published at EMNLP 2021. LM-adapted T5.1.1 checkpoints released by the authors (github.com/google-research/text-to-text-transfer-transformer, released_checkpoints.md).

## What was read

PDFs from arXiv, text extracted with pdftotext.

- **Li & Liang.** Read in full: abstract, §1–9 (related work, problem statement, method §4.1–4.3, setup §5, results §6.1–6.4, intrinsic evaluation §7.1–7.4, discussion §8), Tables 1–4, and appendix A.1–A.4 (Table 5 hyperparameters, Table 6 qualitative examples). Figures 3–7 are plots. Their values do not survive text extraction, so I report only what the captions and text state. References: only identified.
- **Lester et al.** Read in full: abstract, §1–8, Tables 1–3, appendix A.1–A.3 (parameter counts Table 4, runtimes Table 5, search space Table 6, dataset sizes and label distributions Tables 7–16). Figures 1, 3 and 4 are plots. I could not read per-model-size SuperGLUE scores from them. Only the numbers stated in the text and tables are reported. References: only identified.
- Neither paper was checked by rerunning anything.

## Mechanism

### Prefix-tuning (Li & Liang, §4)

- Frozen autoregressive LM with parameters phi. The activation at step i is h_i = [h_i^(1); …; h_i^(n)], all layers stacked. Each layer's entry is a key-value pair; in GPT-2 each key and value has dimension 1024 (footnote 1).
- Normal recurrence (Eq. 1): h_i = LM_phi(z_i, h_<i).
- Prefix-tuning prepends a prefix: z = [PREFIX; x; y]. For an encoder-decoder (BART): z = [PREFIX; x; PREFIX′; y].
- Eq. 3: h_i = P_theta[i, :] if i ∈ P_idx, otherwise LM_phi(z_i, h_<i). P_theta has shape |P_idx| × dim(h_i). So **the prefix sets the key-value activations at every layer** for the prefix positions. It is not just an input embedding.
- Objective (Eq. 2): max over theta of sum over i ∈ Y_idx of log p_phi(z_i | h_<i), with phi frozen.
- Reparametrization (§4.3): P_theta[i, :] = MLP_theta(P′_theta[i, :]), with P′ of shape |P_idx| × k (k = 512 for table-to-text, 800 for summarization). "directly updating the P_theta parameters leads to unstable optimization and a slight drop in performance". After training, the MLP is dropped and only P_theta is stored.
- Initialization (§7.4): the prefix is initialized with the LM's activations of real words.
- Defaults: 10 epochs, batch 5, learning rate 5e-5, prefix length 10, AdamW. Task-specific parameters: 250K (E2E, WebNLG), 500K (DART), against 345M in GPT-2 medium, i.e. 0.1%.

### Prompt tuning (Lester et al., §2)

- T5 encoder-decoder. Input tokens are embedded as X_e ∈ R^{n×e}. A soft prompt P_e ∈ R^{p×e} is concatenated: [P_e; X_e] ∈ R^{(p+n)×e}. This passes through the frozen encoder-decoder as usual.
- Only P_e is trained, by maximizing Pr_{theta;theta_P}(Y | [P; X]). **The prompt lives only at the input-embedding layer.** Deeper layers are computed by the frozen network.
- Parameter cost: E·P (embedding dimension × prompt length). For T5-XXL with 5 tokens, that is 20,480 parameters (Fig. 2). With 100 tokens it is 409,600, i.e. 0.0037% (Table 4).
- Initialization options: random uniform in [−0.5, 0.5]; sampled from the 5,000 most common vocabulary tokens; or "class label" embeddings (multi-token labels averaged), with sampled vocabulary filling the rest.
- "LM adaptation": T5.1.1 is pre-trained on span corruption, so the authors continue training up to 100K steps with an LM objective. This is done once and produces one frozen model.
- Default: LM-adapted 100K steps, class-label init, prompt length 100. Training is 30,000 steps, learning rate 0.3, batch 32, Adafactor.

### Difference between the two

Prefix-tuning writes activations at every layer. Prompt tuning writes only the input embeddings. Lester: "Our new conditional generation is now Pr_{θ;θP}(Y|[P;X])". In their words, prompt tuning "can be thought of as using a fixed prompt of special tokens, where only the embeddings of these prompt tokens can be updated" (§2). Li & Liang's "embedding-only" ablation (§7.2) is the same object as Lester's prompt tuning.

## Evidence

### Prefix-tuning (GPT-2 medium/large, BART-large)

- **Table-to-text** (Table 1, GPT-2 medium, BLEU):
  - E2E: prefix 0.1% 69.7; fine-tune 68.2; adapter 3% 68.9; adapter 0.1% 66.3; FT-top2 68.1.
  - WebNLG (seen / unseen / all): prefix 62.9 / 45.6 / 55.1; fine-tune 64.2 / 27.7 / 46.5.
  - DART: prefix 46.4; fine-tune 46.2.
  - The paper says prefix-tuning is on average 4.1 BLEU better than adapter 0.1% per dataset.
- **Summarization** (XSUM, Table 2, ROUGE-L): fine-tune 37.25; prefix 2% 36.05; prefix 0.1% 35.05. Here the prefix underperforms.
- **Low data** (§6.3): training sizes {50, 100, 200, 500}, 5 datasets × 2 seeds each. The prefix outperforms fine-tuning "by 2.9 BLEU on average", and "the gap narrows as the dataset size increases".
- **Extrapolation** (§6.4): XSUM news-to-sports ROUGE-L 31.51 (prefix) vs 30.26 (fine-tune). WebNLG unseen categories BLEU 45.6 vs 27.7. Adapters extrapolate about as well, so the authors attribute the gain to keeping LM parameters frozen.
- **Prefix length** (§7.1, Fig. 4): performance rises up to a threshold, 200 for summarization and 10 for table-to-text, then drops slightly. Longer prefixes give lower training loss but worse test scores (overfitting, footnote 14).
- **Continuous all-layer vs input-embedding-only** (§7.2, Table 4, E2E BLEU): full prefix 69.7. Embedding-only EMB-1 48.1, EMB-10 62.2, EMB-20 61.9. Infix (between x and y) INFIX-1/10/20: 67.9 / 67.2 / 66.7.
  - Claim, §7.2: "The embedding-only ablation upper bounds the performance of discrete prompt optimization … because discrete prompt restricts the embedding layer to exactly match the embedding of a real word. Consequently, we have this chain of increasing expressive power: discrete prompting < embedding-only ablation < prefix-tuning."
  - **This is a set-inclusion argument, not a measurement.** No discrete-prompt baseline (manual or searched, e.g. AutoPrompt) is run in the paper. The only discrete evidence is footnote 2: "In our preliminary experiments, GPT-2 and BART fail in this setting; the only exception is GPT-3." No numbers are given.
- **Initialization** (§7.4, Fig. 5/7, low data, 100 examples): "Random initialization leads to low performance with high variance." Initializing with real-word activations "significantly improves generation". Task-relevant words ("summarization", "table-to-text") are slightly better than irrelevant ones ("elephant", "divide"). Plot values are not readable from the text.
- **Personalization** (§8.1–8.2): one prefix per user, with a shared frozen LM; requests from different users can be batched in one forward pass. Stated as a property, not tested.

### Prompt tuning (T5.1.1 Small to XXL, SuperGLUE dev)

- **Scale closes the gap** (§3.1, Fig. 1): "At the XXL size (11 billion parameters), prompt tuning matches even the stronger multi-task model tuning baseline, despite having over 20,000 times fewer task-specific parameters." The per-size curve is only in the figure. Mean of five XXL prompts: SuperGLUE 90.5 (Table 3).
- **Prompt design comparison** (§1, §3.1):
  - GPT-3 175B few-shot SuperGLUE is 71.8, against fine-tuned T5-XXL at 89.3 (quoted from prior work).
  - "prompt-tuned T5-Small matching GPT-3 XL (over 16 times larger), and prompt-tuned T5-Large beating GPT-3 175B (over 220 times larger)".
  - **This is a cross-model comparison.** Footnote 5: "We also experimented with using GPT-3's manual text prompts directly with our LM-adapted T5 checkpoints. However performance was far below GPT-3 for comparable model sizes." So there is no same-model test of discrete vs continuous prompts. The reported gap mixes the conditioning channel with model, pre-training data and the number of labeled examples (prompt tuning uses the full training set; few-shot uses a few in context).
- **Ablations** (§3.2, Fig. 3; mean ± sd over 3 runs):
  - Length {1, 5, 20, 100, 150}: "increasing prompt length beyond a single token is critical" for most sizes, but "the XXL model still gives strong results with a single-token prompt". Beyond 20 tokens gains are marginal; beyond 100 tokens there is a mild drop for larger models (footnote 6).
  - Init: class-label init is best. "At smaller model sizes, there are large gaps between the different initializations, but once the model is scaled to XXL size, those differences disappear."
  - Pre-training objective: with off-the-shelf span corruption, "only 2 out of 5 models working well". Mid-sized models "never learn to output a legal class label and thus score 0%" on many tasks. LM adaptation fixes this. XXL works with any objective.
- **Domain shift** (§5, Tables 1–2):
  - Train on SQuAD, test zero-shot (F1, model tuning → prompt tuning): TextbookQA 54.3 → 66.8 (+12.5), BioASQ +1.2, RACE +0.9, RE +0.4, DuoRC −1.2, DROP −1.8, SQuAD in-domain −0.1.
  - QQP → MRPC: accuracy 73.1 → 76.3, F1 81.2 → 84.3. MRPC → QQP: accuracy 74.9 → 75.4, F1 70.9 → 69.7.
- **Prompt ensembling** (§6, Table 3, XXL, 5 prompts, majority vote): SuperGLUE average 90.5, best single 91.0, ensemble 91.3. The ensemble runs as one batch of N copies of the input with different prompts.
- **Interpretability by nearest tokens** (§7; cosine distance to vocabulary embeddings):
  - "the top-5 nearest neighbors form tight semantic clusters", e.g. {Technology / technology / Technologies / technological / technologies} and {entirely / completely / totally / altogether / 100%}. "random vectors drawn from the embedding space do not show this sort of semantic clustering."
  - Class labels persist as nearest neighbors after class-label init. With other inits they appear as neighbors of several prompt tokens.
  - Long prompts (100) have "several prompt tokens with the same nearest neighbors", which suggests excess capacity.
  - BoolQ prompts have neighbors such as science, technology and engineering; about 20% of BoolQ questions are "Nature/Science". The authors suggest the prompt may "prime the model to interpret inputs in a specific domain or context".
  - Overall: "Beyond this, we did not find our learned prompts to be interpretable" (§3.2). No test decodes a prompt to its nearest tokens and measures the score of that discrete version.
- **Cost**: XXL prompts took 21 min (length 1) to about 3 h 51 min (length 100) to converge on BoolQ, on 16 TPU v3 (Table 5). In total, 195 runs plus 18 domain-shift runs and 24 ensemble runs.

### Prefix vs prompt across the two papers

- At GPT-2 medium (345M), Li & Liang find input-only clearly worse than all-layer: E2E BLEU 62.2 vs 69.7.
- At T5-XXL (11B), Lester find input-only enough to match full fine-tuning.
- (my inference) The two results are consistent if input-only conditioning becomes sufficient with scale. Lester's own curves show the small models need longer prompts and better inits. Neither paper runs both methods on the same model, so this is not established.

## Available through `claude -p` / Agent SDK?

**No.**
- Prefix-tuning needs write access to per-layer key-value activations.
- Prompt tuning needs to place arbitrary vectors in the input-embedding sequence.
- Both need gradients of the output log-likelihood with respect to those vectors, i.e. backpropagation through the frozen model.

The CLI and SDK accept only token text (and images) and return text. They expose no embeddings, activations, logits or gradients. No released Claude soft-prompt interface exists that I know of.

Black-box analogues, none tested in these papers:
- **Discrete prompt search.** Choose words for the system prompt by black-box search scored on outputs. This is "prompt design". By Li & Liang's inclusion argument it is the weakest level, and here it fails Principle 4 by construction, because the state would then reach Claude as words.
- **Nearest-token projection.** Lester's nearest neighbors are word-like, but there is no Claude soft prompt to project.
- **Prompt ensembling ≈ N-draft selection.** Table 3 is an ensemble of five prompts with majority voting, +0.8 SuperGLUE over the mean prompt. Its structure (one input, N conditionings, an aggregation outside the model) matches running N drafts and choosing outside Claude. But the N conditionings are learned vectors, and the vote is over class labels, not free text.

## What it implies for the interface theory

1. **Soft prompts are the formal model of Principle 4.** A vector that is not a word, prepended to a frozen model, reliably changes how the model processes all later tokens (Li & Liang §4.2: non-prefix activations "still depend on P_theta, because the prefix activations are always in the left context"). That is exactly "the state reaches Claude only by changing how it processes". It is the ideal the project cannot implement.
2. **Conditional prefixes are a small step that neither paper takes.**
   - Both papers learn one prefix per task (or per user, §8.1) and never as a function of a continuous variable.
   - Li & Liang already generate P_theta = MLP_theta(P′) from a smaller matrix. Replacing the fixed P′ with an encoding of the engine state, P = MLP(s_t), gives a state-conditional prefix trained end to end (my inference). It would need targets: training data that says what text a state should produce. That supervision is the hard part for an affective engine, and neither paper addresses it.
   - Neither paper interpolates between prefixes, so continuity of behavior in the prefix is not evidenced.
3. **What continuity buys over words is weakly evidenced, and it shrinks with scale.**
   - The "continuous > discrete" claim in Li & Liang is an inclusion argument with no discrete baseline run.
   - Lester's "beats prompt design" compares different models trained on different data.
   - At 11B, a single soft token suffices, and the gap between word-initialized and random prompts disappears.
   - Learned soft tokens sit near tight clusters of real words.
   - (my inference) At Claude's scale, much of what a soft prompt does is probably close to what some well-chosen words do. That makes "prompt design" a weaker substitute than these papers suggest only at small scale. But it is still the wrong channel for Principle 4: P1 already showed that putting state as numbers into the prompt changed nothing (0/5 vs 0/5). Words also make the state legible to Claude as labels, which Principle 4 forbids.
4. **Domain robustness comes from freezing.** Frozen-model conditioning generalizes better out of domain (TextbookQA +12.5 F1). That supports the design choice to leave Claude unmodified and put adaptation outside it. It does not tell us how.
5. **No black-box analogue preserves the soft-prompt property.**
   - Every channel through `claude -p` is text, images, tool results or configuration.
   - Configuration knobs (thinking budget, max turns, model choice, interrupt timing) change how Claude processes without words in context. They are the only black-box analogues of "conditioning without words". But they are a handful of coarse scalars, not a vector over the key-value cache (my inference).
   - The richest such channel is selection among drafts (see the PPLM note). It acts on Claude's output, not its input, and its effect returns to Claude as text in later turns.

## Verdict

**Watch (as the formal ideal; reject as an implementation).** Soft prompts are the cleanest existing demonstration of Principle 4 — a non-word vector that changes how a frozen LM processes. They need embedding-level input and gradients, which `claude -p` and the Agent SDK do not expose. The evidence that continuous conditioning expresses more than words is indirect, and it narrows at ≥10B scale.
