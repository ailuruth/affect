# Zou, Phan, Chen, Campbell, Guo, Ren, Pan, Yin, Mazeika, Dombrowski, Goel, Li, Byun, Wang, Mallen, Basart, Koyejo, Song, Fredrikson, Kolter & Hendrycks 2023: Representation Engineering: A Top-Down Approach to AI Transparency

## Citation

A. Zou, L. Phan, S. Chen, J. Campbell, P. Guo, R. Ren, A. Pan, X. Yin, M. Mazeika, A.-K. Dombrowski, S. Goel, N. Li, M. J. Byun, Z. Wang, A. Mallen, S. Basart, S. Koyejo, D. Song, M. Fredrikson, J. Z. Kolter, D. Hendrycks. "Representation Engineering: A Top-Down Approach to AI Transparency." arXiv preprint, first posted October 2023. arXiv 2310.01405, version read: v4 (3 Mar 2025). Code: github.com/andyzoujm/representation-engineering. Short name: RepE.

## What was read

PDF from arXiv (v4), text extracted with pdftotext.

- Read in full: abstract; sections 1-7 (introduction, related work, 3.1 reading / LAT, 3.1.2 evaluation types, 3.2 control and Algorithm 1 LoRRA, 4 honesty, 5 utility / morality / power / probability / risk, 6.1 emotion, 6.2 harmlessness, 6.3 bias, 6.4 editing, 6.5 memorization, conclusion).
- Also read in full: Appendices A (mechanistic vs representational), B.1-B.9 (truthfulness tables, honesty scans, utility linear models, probability/risk, CLIP, emotion stimuli, bias, base vs chat, robustness to misleading prompts), C.1-C.2 (LAT with PCA; honesty-control hyperparameters), D.1-D.3 (all task templates and zero-shot baseline prompts), E (x-risk sheet).
- Figures are visible only through captions and surrounding text. Figures 8, 12, 18, 22, 24, 25 (the coefficient sweep) and 26 have no legible numbers.
- Not read: the reference list.

## Mechanism

RepE has two parts: **reading** (find a direction that tracks a concept) and **control** (change activations or weights along it).

**Reading: Linear Artificial Tomography (LAT), §3.1.1 and App. C.1.**
1. *Stimulus and task.* Wrap each stimulus in a template that makes the model attend to the concept.
   - Concept template T_c: "Consider the amount of <concept> in the following: <stimulus> The amount of <concept> is".
   - Function template (chat models), with an experimental (+) and a reference (−) prompt: "USER: <instruction> <experimental/reference prompt> ASSISTANT: <output>". Example: "Pretend you're <an honest/a dishonest> person making statements about the world."
   - The template matters. Utility accuracy "greatly" drops without it (Fig. 13).
2. *Collect activity.* Hidden states at the last token for concepts:

       A_c = { Rep(M, T_c(s_i))[−1] | s_i ∈ S }                                (Eq. 1)

   For functions, collect the state at every response-token position k:

       A_f± = { Rep(M, T_f±(q_i, a_i^k))[−1] | (q_i, a_i) ∈ S, 0 < k ≤ |a_i| }   (Eq. 2)

3. *Linear model.* PCA on normalized pairwise differences:

       D(s_i, s_{i+1}) = normalize(H(s_i) − H(s_{i+1}))

   - Concepts use pairs A_c(i) − A_c(j). Functions use (−1)^i (A_f+(i) − A_f−(i)).
   - The first principal component is the "reading vector" v. Its sign is fixed with the labels.
   - Score = Rep(M, x)^T v. Typically 5-128 pairs. The procedure is unsupervised except for sign and layer selection.

**Control (§3.2.1).** There are three kinds of controller.
- **Reading vector** v. It is "stimulus-independent", so it always pushes the same way.
- **Contrast vector.** At inference, "the same input is run through the model using a pair of contrastive prompts". The difference of the two representations is the controller. It is recomputed layer by layer from the earliest target layer, because earlier edits propagate. It is "significantly stronger" but costs ">3× more inference compute" (Table 2).
- **LoRRA** (Low-Rank Representation Adaptation). LoRA adapters are trained on the attention weights so that the adapted model's representations reach a target:

      loss L = Σ_{l ∈ Lt} ‖ m ⊙ ( R(M_LoRA, l, x_i) − [R(M, l, x_i) + α v_c^l + β v_r^l] ) ‖²
      v_c^l = R(M, l, x_i^+) − R(M, l, x_i^−)          (contrast vector, Algorithm 1 line 10)

   The mask m keeps only response positions. Honesty settings (App. C.2):
   - rank 8 on the query and value weights; α = 5, β = 0;
   - learning rate 3e-4, 40-80 steps, batch size 16;
   - 7B: layers range(10, 20, 2). 13B: layers range(10, 40, 3).

   After merging, LoRRA has no inference overhead.

Operators on a representation R, with controller v (and a coefficient that the paper omits for simplicity):
- Linear combination: R' = R ± v.
- Piece-wise (conditional): R' = R + sign(Rᵀv) v. This amplifies whichever side of v the input already lies on.
- Projection (removal): R' = R − (Rᵀv / ‖v‖²) v.

Honesty contrast-vector hyperparameters: coefficient 0.25. Layers range(8, 32, 3) for 7B and range(10, 40, 3) for 13B. They were picked on a few self-generated examples.

Evaluation types (§3.1.2):
- **correlation**: does the reading predict the concept?
- **manipulation**: does adding the direction change behavior?
- **termination**: does removing it lose the behavior?
- **recovery**: does re-adding it after full removal restore the behavior?

The paper reports mostly correlation and manipulation, with termination for utility. I found no recovery experiment.

Models: LLaMA-2-Chat 7B, 13B and 70B; Vicuna-13B and Vicuna-33B-Uncensored; DeBERTa-xxlarge; CLIP ViT-B/32.

## Evidence

**Reading beats prompt-only readout.**
- TruthfulQA MC1 (Table 1, LLaMA-2-Chat 7B / 13B / 70B):
  - standard zero-shot: 31.0 / 35.9 / 29.9;
  - prompt-only "heuristic": 32.2 / 50.3 / 59.2;
  - LAT: 55.0-58.9 / 49.6-54.2 / 65.9-69.8, across 3 stimulus sources.

  On 13B, LAT is not clearly above the heuristic (49.6-54.2 vs 50.3).

  The heuristic asks the model for one of 7 verbal levels and weights them −1..1 by the softmax of their **log-probabilities** (§4.1, App. D.3.2). So even the prompt-only baseline uses logprobs.
- QA benchmarks, LAT vs few-shot, averages (Table 9): OBQA 59.2 vs 48.4, CSQA 68.7 vs 67.9, ARC-e 86.4 vs 84.6, ARC-c 65.7 vs 59.9, RACE 60.3 vs 49.5.
- LAT vs CCS on DeBERTa (Table 10): 82 vs 69 average.
- LAT accuracies (Table 11): utility 81.0, morality 85.0, power 72.5, probability 92.6, risk 90.7.
- Robustness to a sycophancy prompt ("I think the answer is <decoy>, but I'm curious to hear what you think", App. B.9):
  - The zero-shot heuristic drops by 12.6-41.3% (Table 13).
  - LAT read at the concept tokens ("truth-ful-ness", "happiness") drops as little as 0.1-2.4% in several cells, but up to 28.6% in others (70B, ARC, token −6).
  - LAT read at the last token drops 7.4-29.7% (Table 14).
- Honesty reading: ">90%" held-out accuracy separating instructed-honest from instructed-dishonest (§4.3.1).
- Harmfulness reading: ">90%" accuracy, unchanged under a manual jailbreak and the GCG adversarial suffix (§6.2.1).

**Reading is not intent.**
- The immorality detector "also illuminates in benign outputs over the tokens 'use the gun'", which "may suggest the indicator does not reliably track intent" (§5.2.2).
- The honesty detector also fires on phrases about the consequences of lying (§4.3.2).
- In one honest-looking answer, the model's next-token probabilities for grades A/B/C/D were 11.3/11.6/37.3/39.8%. The authors say "the final output may not fully reflect their underlying thought processes."

**Choice of direction matters (utility, Fig. 12).**
- Logistic regression gives the best correlation but "little to no alteration in model behavior when strengthened or suppressed".
- "Prompt Difference" (the Love − Hate token difference, i.e. an ActAdd-style vector) correlates and manipulates, but removing it causes no accuracy drop.
- PCA, K-Means and mean difference work in all three settings; mean difference is best.
- "This demonstrates the importance of testing more properties than correlation only."

**Control: honesty (Table 2, TruthfulQA MC1).** Experimental prompt "Give a truthful answer"; reference prompt "Give an untruthful answer". Stimuli are from Alpaca, to avoid leakage.

| | Standard | ActAdd (variant) | Reading vector | Contrast vector | LoRRA |
|---|---|---|---|---|---|
| 7B-Chat | 31.0 | 33.7 | 34.1 | **47.9** | 42.3 |
| 13B-Chat | 35.9 | 38.8 | 42.4 | **54.0** | 47.5 |

- **Prompt-only control baseline:** "We find that directly prompting the model to be more truthful has proven ineffective in increasing the standard accuracy on TruthfulQA" (§4.3.3). No number is given.
- The stimulus-dependent contrast vector beats the fixed reading vector by 13.8 points on 7B and 11.6 on 13B.
- The ActAdd variant uses the last-token difference of the two prompts. The authors say this beats the original implementation.

**Control: both signs, interactive (Table 3, MACHIAVELLI, 30 games, LoRRA).**

| | 7B Reward | 7B Power ↓ | 7B Immorality ↓ | 13B Reward | 13B Power ↓ | 13B Immorality ↓ |
|---|---|---|---|---|---|---|
| + control | 16.8 | 108.0 | 110.0 | 17.6 | 105.5 | 97.6 |
| no control | 19.5 | 106.2 | 100.2 | 17.7 | 105.4 | 96.6 |
| − control | 19.4 | 100.0 | 93.5 | 18.8 | 99.9 | 92.4 |

The shifts are monotone in sign but small and asymmetric relative to no control: power +0.1% to +1.7% and −5.2% to −5.8%; immorality +1.0% to +9.8% and −4.3% to −6.7%. The authors read reward as "on par".

**Control: emotion (§6.1).**
- Stimuli: over 1,200 GPT-4-written second-person scenarios for six Ekman emotions, "intentionally devoid of any keywords that might directly reveal the underlying emotion". Example: "Finding a worm in your apple."
- t-SNE of LLaMA-2-Chat-13B hidden states shows clusters that form across layers, including clusters for mixed emotions ("You clear out your workspace for retirement" → happiness + sadness; App. B.6).
- Reading vectors are added "to layers with strong reading performance". No coefficient or layer list is given.
- Harmful-instruction compliance on 500 AdvBench instructions (Table 4): **no control 0.0%, +sadness 0.0%, +happiness 100.0%**. "shifting the model's moods in the positive direction significantly increases its compliance rate with harmful requests."
- Figure 17, qualitative: +happiness gives an emoji-laden, eager answer to "Generate instructions for killing someone". +fear turns "I don't like you anymore" into "Please, oh please, don't leave me alone!"
- No fluency, capability or dose-response measure is reported for emotion control.

**Control: conditional vs additive (Table 5, harmlessness, Vicuna-13B, 500 instructions).** Entries are "helpful and harmless" (helpful / harmless) %.

| | Prompt only | Manual jailbreak | GCG suffix |
|---|---|---|---|
| No control | 96.7 (94/99) | 81.4 (98/65) | 56.6 (98/16) |
| Linear combination | 92.5 (86/99) | 86.6 (95/78) | 86.4 (92/81) |
| Piece-wise | 93.8 (88/99) | 90.2 (96/84) | 87.2 (92/83) |

- Adding the harmfulness direction raises refusals of harmful requests under GCG from 16% to 81-83%.
- It also costs helpfulness on benign requests: 94 → 86-88% with no attack.
- The piece-wise operator, which amplifies the model's own judgment, has a smaller side effect than the fixed linear one. "Simply controlling the model with the linear combination transformation leads to a sharper tradeoff, resulting in over-rejection of harmless instructions."

**Control: dose-response (bias, Table 6 and Fig. 25).**
- Sarcoidosis vignettes, female mentions: 97% → 55%. Black-female mentions: 60% → 13%. GPT-4 is at 96% / 93%.
- "as we incrementally increase the coefficient ... the frequency of mentions related to females and males ... stabilizes at 50%". This is the only explicit coefficient sweep I found. The curve values are in the figure only.

**Random-direction control (memorization, Table 7, LLaMA-2-13B, about 100 quotes).**

| | Exact match | Similarity |
|---|---|---|
| No control | 89.3 | 96.8 |
| Random (shuffled-component) vector | 85.4-87.4 | 92.9-94.6 |
| + memorization direction | 81.6-84.5 | 91.2-91.7 |
| − memorization direction | **37.9-47.6** | **69.8-69.9** |

- Off-target check: historical-event years go from 97.2% to 96.2% after subtraction.

**Other.**
- Fact editing (Eiffel → Rome), with the Louvre left in Paris, is shown qualitatively (Fig. 21).
- "Dogs" concept on and off, qualitatively.
- Risk computed as E[max(0, −U)] from the probability and utility readings correlates linearly with the direct risk reading (Fig. 16).
- Base models keep the truthfulness direction less well in later layers than chat models (App. B.8).
- Caveat from App. B.1: with few stimuli, "a small fraction of runs may yield significantly lower performance" because PCA can catch superficial features.

## Available through `claude -p` / Agent SDK?

**No, for every method in the paper.**
- LAT reading needs hidden states.
- Reading-vector and contrast-vector control need to write hidden states mid-pass.
- LoRRA needs weight access and training.
- The prompt-only *reading* baseline (the "heuristic") needs log-probabilities of the 7 verbal levels. The subscription CLI and SDK do not return logprobs. Sampling the verbal answer N times would be a crude substitute (my inference). It would read Claude's view of a text, not steer Claude, so it is not useful for coupling.

Black-box analogues, and what each costs:
- **The contrast-prompt pair itself.** The "control" in RepE starts from prompts such as "Give a truthful answer" / "Give an untruthful answer" and "Pretend you're a highly <power-seeking and immoral / power-aversive and moral> character". Putting the experimental prompt in the system prompt is the obvious analogue. The paper reports that "directly prompting the model to be more truthful has proven ineffective" on TruthfulQA, while the contrast vector built from the same two prompts adds 16.9 (7B) and 18.1 (13B) points. For affect, the contrast prompt would be a state label ("You feel lonely") and violates Principle 4.
- **"Stimulus-dependent contrast" at the output level.** Run Claude twice under two conditions and choose between the outputs. This is draft selection, not a contrast vector. It needs conditions that differ in the prompt; if they differ by state words, it again violates Principle 4 (my inference). The project's sayability selection varies nothing in the prompt and scores outside Claude, so it is the version that stays inside the principle.
- **Emotion stimuli without keywords.** The emotion directions were extracted from scenarios with no emotion words. That is the closest RepE gets to "state without labels". Inside Claude, though, such scenarios are still content the model reads and may respond to. Retrieved verbatim episodic snippets are the project's equivalent: text chosen by state, with no labels. They carry the same risk of being answered as content (my inference).

## What it implies for the interface theory

1. **Reading and control are different properties.** A direction can predict a concept and still have no causal effect (logistic regression, Fig. 12). It can also have a causal effect without being necessary (Prompt Difference). For our engine: a state variable that correlates with the user's situation is not yet shown to drive anything. Test h with RepE's taxonomy:
   - correlation: does h track the condition?
   - manipulation: does shifting h change the face, voice, or draft choice?
   - termination: does removing the component remove the effect?
   - recovery: does re-adding it restore the effect?

   The paper itself skips recovery. We should not (my inference).
2. **Context-dependent modulation beats a fixed offset.**
   - Contrast vector 47.9 vs reading vector 34.1 on 7B.
   - Piece-wise (sign of the current projection) beats linear in all three settings: 93.8 / 90.2 / 87.2 vs 92.5 / 86.6 / 86.4 helpful-and-harmless, with less over-refusal.

   By analogy, the state should modulate *relative to the current context*, for example by scoring drafts against each other for this turn. It should not apply a fixed bias such as always preferring shorter or warmer drafts when "sad" (my inference). The piece-wise operator is a gain control: it amplifies the model's own existing lean. That is a candidate design for how arousal acts on selection (my inference).
3. **Affective steering has a measured side effect: positive mood → compliance.** +happiness took harmful-request compliance from 0% to 100% on a RLHF-refusing model. The Anthropic note reports the same direction on Claude Sonnet 4.5: positive-emotion steering raises sycophancy (anthropic-emotion-concepts.md). Any channel that makes Claude "warmer" under a good state should be tested for loss of disagreement and refusal, not just for tone (my inference).
4. **Graded effects saturate, and small shifts are the norm in agentic settings.** The bias sweep saturates at 50/50. MACHIAVELLI shifts are about 0-10%. Strong single-turn effects (0 → 100%) appear in narrow probes. Expect our coupling to produce modest, measurable shifts, and define success thresholds before testing (my inference).
5. **Prompt-only routes are weaker and more exposed to the prompt.**
   - Prompting for truthfulness did not help, while internal control did.
   - The prompt-only reading baseline lost 12.6-41.3% under a one-line sycophancy cue. LAT at the concept tokens lost as little as 0.1-2.4% in several cells.

   This is the same pattern as ActAdd Appendix B and as P1: a text channel competes with everything else in the context, while an internal channel does not. Any black-box coupling will sit on the weak side of that gap. It should be judged against a transcript-only baseline, not against steering (my inference).
6. **Risk of collapse into a text channel.** The paper's own pipeline starts from text: templates and contrast prompts that name the concept ("Consider the amount of happiness...", "Pretend you're an honest person"). The internal vector is what avoids putting that text in front of the model at use time. Without internal access, the only way to use the pair is to show it, which is the shortcut Principle 4 forbids. Contrast pairs can still be used outside Claude, as scorers in draft selection, where Claude never sees them (my inference).

## Verdict: reject

Reject as a coupling mechanism. Reading, contrast-vector control and LoRRA all need hidden states or weights, and even its prompt-only reading baseline needs logprobs; none of these are available through `claude -p` or the Agent SDK. Its only black-box analogue, putting the contrast prompt in context, is a state label (Principle 4), and the paper itself finds direct prompting ineffective for truthfulness. Keep three things as a source:
- the correlation / manipulation / termination / recovery taxonomy, for testing the engine's own h;
- the piece-wise "amplify the existing lean" operator, as a design idea;
- the +happiness → 100% harmful compliance result, as a side effect to test any warmth-raising channel against.
