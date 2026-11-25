# Coupling a continuous affective state to Claude without numbers or words: synthesis

S0, 2026-11-25. Answers the brief's open problem "how a frozen language model is coupled to a continuous affective dynamical system without text (an interface theory)", under Principle 4 and the constraint that Claude is reached only through the operator's subscription (`claude -p` or the Python Agent SDK; no weights, activations, logits, log-probabilities or API key).

Sources (all in research/): [Claude Code / Agent SDK controls](claude-code-agent-sdk-controls.md), [ActAdd](turner-2023-activation-addition.md), [RepE](zou-2023-representation-engineering.md), [soft prompts](li-2021-lester-2021-soft-prompts.md), [PPLM](dathathri-2020-pplm.md), [FUDGE](yang-klein-2021-fudge.md), [GeDi](krause-2021-gedi.md), [persona vectors](chen-2025-persona-vectors.md), [WebGPT best-of-n](nakano-2021-webgpt-best-of-n.md), [reward-model overoptimization](gao-2023-reward-overoptimization.md), [best-of-n KL](beirami-2024-best-of-n-kl.md), [generative-agents retrieval](park-2023-generative-agents-retrieval.md); earlier: [Anthropic emotion concepts](anthropic-emotion-concepts.md), predictions.md (P1), foundations/efference-memory.md §2.5, foundations/sketches/v2-llm-interface-linguist.md.

## 1. What the internal-access literature shows, though none of it is available

1. **A continuous vector can change a frozen LM's processing in a graded way.**
   - ActAdd adds one activation difference with |c| < 15. It shifts topic and sentiment, with off-target perplexity changing by 0.6%.
   - RepE's per-input contrast vector adds +16.9 and +18.1 points on TruthfulQA (7B and 13B).
   - Soft prompts match full fine-tuning at 11B parameters (SuperGLUE average 90.5 over 5 prompts). One soft token is enough at that scale.
   - PPLM nudges the key-value history with step size 0.01–0.03. At 0.05 or more the output degenerates.

   Every one of these needs embeddings, activations, gradients or logits. `claude -p` and the SDK expose none of them (claude-code-agent-sdk-controls.md).
2. **Prompting is a worse version of the same move.**
   - ActAdd's prompt baseline costs 13% perplexity on unrelated text, against 0.6% for the vector.
   - Prompting made OPT more toxic than doing nothing (.200 vs .134 unsteered).
   - RepE: "directly prompting the model to be more truthful has proven ineffective". The same prompt pair works when used as an internal contrast.
   - Persona vectors: system-prompt mitigation is weaker than steering.

   This is consistent with P1, where body numbers in the prompt changed nothing (0/5 vs 0/5). Words and numbers are a different channel from modulation, not a weaker form of it.
3. **Warm steering has a known side effect.**
   - RepE: +happiness steering took compliance with 500 harmful requests from 0% to 100%.
   - Anthropic 2026: steering Claude Sonnet 4.5 toward positive emotions raises sycophancy.
   - Persona vectors: sycophancy is the trait most consistently set by in-context text, and its features are "mostly stylistic".

   Any channel that makes Claude warmer has to be tested against flattery (Principle 6).
4. **Context sets the internal state before generation.**
   - Persona vectors, on Qwen and Llama (not Claude): the projection of the last prompt token onto a trait vector predicts the trait in the reply at r = 0.63–0.83, when system prompts or prepended examples vary.
   - Examples that *demonstrate* a trait move the direction at least as consistently as prompts that *describe* it. For sycophancy, the within-condition r is 0.81 vs 0.67.
   - Anthropic 2026: Claude's emotion vectors are token-local and recomputed from context by attention. Claude carries no persistent emotional state between positions.

   Together, these make the composition of the context the black-box handle on Claude's internal emotion representations.
5. **Token-level control and draft-level selection have the same target.** FUDGE's per-token rule P(x_i | x_<i, a) ∝ P(a | x_1:i) P(x_i | x_<i), with an exact prefix classifier, telescopes to P(x | a). Resampling whole drafts with weight P(a | draft) aims at the same distribution. The token-level method is cheaper, but it does not reach a different target. What the subscription takes away is efficiency, not the target.

## 2. The admissible channels

**Admissibility criterion.** The state may *reweight* text that Claude or the world produced. It may never *write* text. Formally, a channel is admissible if, for every state s, the support of the text it places before Claude is contained in a support that does not depend on s: Claude's own sampled drafts, verbatim records from the episode store, or Claude-independent settings. This splits the cases:
- Selection among Claude's drafts is admissible, because support(π_N) ⊆ support(π) (beirami-2024).
- Verbatim retrieval is admissible.
- Numbers, labels and descriptions are not: those tokens exist only because of the state.
- State-chosen instructions with no state words, such as "be brief" when the state is depleted, are also not admissible. Each is a code word for a state region, i.e. a label.

| # | Channel | Mechanism in `claude -p` / SDK | Changes Claude's processing in this turn? | Bound on state information per reply | Mathematically characterized? |
|---|---|---|---|---|---|
| C1 | **Draft selection** (argmax best-of-N, softmax choice, threshold-and-redraw) | N parallel calls; engine scores r_s(y); keep one | No. It changes which output is used. Processing changes only in later turns, through history | KL(π_N‖π) ≤ log N − (N−1)/N for argmax; ≤ log N for any rule that picks one of N; ≤ log E[M] with redraws | Yes: an exact exponential tilt (§3.1) |
| C2 | **Chunk selection** | N streams, `include_partial_messages`, `interrupt()` the losers at sentence boundaries, restart from the kept prefix | Same as C1, at finer grain | ≤ K · (log N − (N−1)/N) over K chunks (Beirami App. B) | Yes, blockwise. The seam is unsolved: no assistant prefill is documented, so the prefix returns as context text |
| C3 | **Stopping time** | `interrupt()` or an output-token cap | No. It truncates | ≤ log₂(number of admissible stop points) | Yes: a stopping rule |
| C4 | **Context selection**: verbatim episodes retrieved by a state query; branch point (`resume_session_at`); an image of the agent's own face | Prompt, streaming input with images, session fork | **Yes.** Context sets the internal trait and emotion coordinates (persona vectors; Anthropic 2026) | ≤ H(choice) ≤ log₂ C(M, k) for k of M records (e.g. 14.3 bits for 3 of 50); the effective amount is far lower | Only through the data-processing bound. The effect is whatever Claude does with the content, with no closed form |
| C5 | **Processing settings**: effort (5 levels), model (3–4), whether and when to call | `--effort` / `effort`, `--model` / `set_model()`, call timing | **Yes, without any text.** Effort changes deliberation depth; the model changes the whole policy | ≤ log₂(5 · 4) ≈ 4.3 bits per call | Only as a discrete control u(s). Its effect on social replies is unmeasured |
| C6 | **Affordances**: which tools exist, which calls are denied | `tools`, `disallowed_tools`, `toggle_mcp_server()`, `can_use_tool` | Yes, it changes the action space. Tool names and denial messages are text, but not state descriptions | ≤ log₂(number of tool subsets) | Discrete |
| C7 | **Reverse channel** (Claude → engine) | `duration_ms`, `thinkingTokens`, refusals, draft content read by the engine | — | — | Closes the loop with no text in either direction |

**Not admissible:**
- numbers (P1);
- labels or descriptions in the system prompt, the user turn or a hook's `additionalContext`;
- state-selected instructions;
- importance or affect scores written by Claude and then used for retrieval (park-2023), because Claude's own labels would steer what Claude later sees.

## 3. What can be stated mathematically

### 3.1 Draft selection is an exponential tilt with a hard cap

Draw y_1..y_N i.i.d. from Claude's draft distribution π (conditioned on the context) and return the draft with the highest r_s(y). With F_s the CDF of r_s under π and no ties (Beirami Lemma 2.3, continuous case):

    π_N^s(y) = N · F_s(r_s(y))^(N−1) · π(y) = π(y) · exp[(N−1) · log F_s(r_s(y)) + log N]

So best-of-N is exactly the KL-regularized optimum (the exponential tilt) for the reward log F_s(r_s(y)), the log-quantile of the score, with strength N−1 (derivation in beirami-2024-best-of-n-kl.md). Three consequences follow.
- Only ranks matter, so rescaling r_s does nothing.
- KL(π_N^s ‖ π) ≤ log N − (N−1)/N for any π and any score without ties (Theorem 3.1). That is 0.64, 1.20, 1.84 and 3.17 nats for N = 4, 8, 16, 64. The bound is nearly tight for long free-text drafts (Theorem 3.4, n²δ ≪ 1).
- Mutual information: I(S; Y | context) = min_q E_s KL(P_{Y|s} ‖ q) ≤ E_s KL(π_N^s ‖ π) ≤ log N − (N−1)/N. At N = 8 this is **at most 1.74 bits of state per reply**.

Softmax selection (P(pick i) ∝ exp(β r_s(y_i))) is self-normalized importance sampling. It tends to π_β ∝ π e^{β r_s} as N → ∞, with KL(π_β‖π) = β E_β[r_s] − log E_π[e^{β r_s}], and is still capped at log N for finite N. Threshold-and-redraw (efference-memory.md §2.5) is capped at log E[M], where M is the number of draws. Each extra nat of steering multiplies the expected number of calls by e.

### 3.2 Gain is set by the spread of the score across drafts

For small β, E_β[r] − E_π[r] ≈ β Var_π(r) (linear response). For argmax with a Gaussian score, the expected gain is σ_r · e_N, with e_N = 1.03, 1.42 and 1.77 for N = 4, 8 and 16. Write r_s(y) = g(y) + h(s, y). Only the interaction term h carries state. Two failures follow.
1. **Draft collapse.** Var_π(r_s) ≈ 0, so selection is a uniform pick and the KL is about 0.
2. **State-blind ranking.** g dominates, so the argmax is the same for every s. The KL can be near the bound while I(S; Y) ≈ 0.

Neither failure is visible in the text of the drafts. Both are measurable without log-probabilities:
- the standard deviation of r_s across the N drafts;
- for one fixed draft set, the rank correlation of r_s across different states. If it is near 1, the ranking ignores the state.

No temperature knob exists in either interface, so draft diversity can come only from Claude's default sampling and from varying the context per draft. Varying the context per draft turns C1 into a joint C1 × C4 channel.

### 3.3 The whole coupling per turn is a few bits to a few tens of bits

By the chain rule, if a turn uses context choice C(s), settings U(s) and selection among N drafts:

    I(S; Y_t | H_t) ≤ H(C) + H(U) + (log N − (N−1)/N)

With 3 of 50 episodes, effort plus model, and N = 8, the upper bound is about 14.3 + 4.3 + 1.7 ≈ 20 bits. The effective amount is much smaller, because C(s) is a deterministic and highly correlated function of s. Context selection is by far the widest channel. It is also the only one besides C5 that changes Claude's processing within the turn.

Over T turns, the chosen drafts and episodes stay in the history. Claude's later context can therefore carry up to T times the per-turn amount of state-correlated text.

### 3.4 Homeostatic scoring makes the coupling vanish at satiety

Principle 6 maps onto the tilt if the selection strength depends on need. Let β(s) ∝ D(s), where D(s) = Σ_j relu(|b_j − b*_j| − ε_j) is the total drive. Equivalently, let r_s(y) score the predicted reduction in drive after reply y, with a dead zone around the set point. At the set point β = 0, so π_N = π and the KL is 0: a satiated agent lets Claude speak as Claude would. Two things follow by construction:
- the coupling is strongest when the need is largest;
- user approval can enter only through a satiable body variable, so flattery has a ceiling.

Gao et al. give the alternative, which is a monotone proxy pushed toward an overoptimization peak: R_bon(d) = d(α − βd) with d = sqrt(log N − (N−1)/N). With the read-off coefficients of their weakest scorer, that peak lies at about 4.2 nats (N ≈ 180). Realistic N (4–16) stays below it. That protects against extremal Goodhart. It does not protect against a scorer that is biased toward approval.

## 4. Is selection by state itself a text channel?

Yes. It should be described honestly as one: **the state reaches Claude only as which of its own possible words, and which verbatim past words, are present.** Three distinctions keep this inside Principle 4.

1. **Reweighting vs writing** (the criterion in §2). Selection never adds a token that would not exist without the state. "Sad" episodes retrieved when the state is low are mood-congruent recall, which is the brief's need-conditioned attention applied to memory. A summary that says "a sad day" is a label. Store verbatim spans and feature-stream pointers, never summaries. Retrieval importance must come from the engine (for example an arousal-like signal at encoding), not from Claude.
2. **Processing vs choice of output.**
   - C4 and C5 change Claude's processing within the turn.
   - C1–C3 change only what is kept.

   A P1-style test of C1 is trivially "positive", because the engine picks the output. Credit for "the state changed how Claude processes" requires an effect on the *next* turn's drafts, or on C4/C5 alone, with selection held fixed.
3. **Decodability is needed, within bounds.** The grounding problem needs Claude to name states, so some state information must reach it. The admissible route is: the state selects episodes, and Claude notices what they share and names it. That is Barrett-style categorization by the language layer. The capacity bounds in §3 make this a measured, low-rate channel rather than a disguised label. Two tests of whether the channel has become a label:
   - **Label equivalence.** Replace the selected context with the state's best one-word description. If the behavior is unchanged, the channel was working as that label.
   - **Leakage.** Have a blind judge decode the state from the selected context alone. Report the bits recovered against the §3.3 bound.

## 5. What each channel can and cannot change

- **Draft selection.** It can choose among things Claude would say. It cannot make Claude say anything new: the support is fixed, the cap is log N per reply, and nothing happens if the drafts collapse.
- **Chunk selection and stopping.** They can shape the course and length of a reply. They cannot continue Claude's own generation seamlessly, because no prefill is documented and every restart reads the prefix as context.
- **Context selection.** It can move Claude's internal emotion and persona coordinates before generation; this is the persona-vector and Anthropic evidence, measured on other models or with internal access. It cannot be predicted in closed form, and it carries the warmth → sycophancy risk.
- **Effort and model.** They can change the depth of deliberation and the whole policy with no text. They cannot vary smoothly: effort has 5 levels, the scale is calibrated per model, and a change applies only at turn boundaries. A token count for thinking is ignored on Opus, Sonnet and Haiku 5.5. Their effect on affective content is unknown.
- **Timing.** It can set when Claude is called and when it is stopped. It is the only truly continuous lever, and it affects Claude only through truncation or through timestamps, which are text.
- **None of them** can do what ActAdd, RepE or soft prompts do: add a graded vector to Claude's internal state. The interface theory must be built on discrete, low-rate channels, and the richness required by the brief's "expressive structure" must live in the engine.

**An advantage the black-box channels have.** Selection, retrieval and settings do not depend on a particular model's internals. They survive a model upgrade (S6), where a steering vector would not.

## 6. Open problems

1. **Does effort change affective content?** Run P1's reunion protocol at effort `low` vs `max`, with the same context and no state words. Score both content (blind rater) and length and latency. This is the only fully text-free processing lever, and it is untested.
2. **Draft spread on Claude.** Measure Var(r_s) and the rank correlation across states (§3.2) for N = 8 drafts from `claude -p` on reunion contexts, before building any scorer. If the spread is near zero, draft selection is dead (the linguist sketch's "draft collapse"), and the coupling reduces to C4 and C5.
3. **The seam.** Can a resumed transcript containing a partial assistant message be continued as the same message? It is undocumented. If not, chunk selection (C2) always reintroduces the prefix as text.
4. **Training the scorer without labels or approval.** r_s must be learned from the engine's own body and episodes (Principles 1, 2 and 6). It also needs an independent "gold" to detect overoptimization (Gao; WebGPT's validation reward model). Candidates are homeostatic outcomes after the reply and held-out raters.
5. **History drift.** Selected drafts become Claude's precedent. Persona-vector many-shot results show monotone drift with more same-trait examples. A model of the compounding is needed: an in-context analogue of iterated RLHF (Gao §4.3). Possible bounds: a per-session limit on cumulative tilt, or resetting the context from the episode store each turn.
6. **How much information must reach Claude for grounding?** Naming states needs decodable structure in the context. Principle 4 forbids labels. The minimum rate at which Claude can learn to name the engine's state regions from selected episodes alone is unknown.
7. **Ablation predictions owed (Principle 5).** For each channel:
   - a sham lesion that uses the state from another time, with the same channel active;
   - a random scorer, or random retrieval at equal entropy;
   - N = 1 for selection;
   - fixed effort for C5.

   Prediction: the sham removes the state-specific effect but not the generic one. The full experiment is the efference-memory §2.5 interface run under these lesions.
8. **Images.** Is a rendered image of the agent's own face (C4) admissible? It carries state without numbers or words, but it asks Claude to read the state. The operator should decide this, because the brief makes naming Claude's job.

## 7. Summary

Under the subscription, nothing can add a continuous vector to Claude. The admissible coupling is a set of discrete, bounded channels:
- selection among Claude's own drafts: an exact exponential tilt, at most log N − (N−1)/N nats per reply;
- selection of verbatim context: the widest channel, and the only text-bearing one that moves Claude's internal affect coordinates before generation;
- effort, model and timing: the only text-free changes to processing.

All of these reweight text Claude or the world produced; none writes state words. Satiable scoring makes the tilt vanish at the set point. The first experiments to run are the draft-spread measurement and the effort test.
