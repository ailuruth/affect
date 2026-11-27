# Towards Understanding Sycophancy in Language Models (Sharma, Tong, Korbak, Duvenaud, Askell, Bowman, … Perez)

Citation: M. Sharma, M. Tong, T. Korbak, D. Duvenaud, A. Askell, S. R. Bowman, N. Cheng, E. Durmus, Z. Hatfield-Dodds, S. R. Johnston, S. Kravec, T. Maxwell, S. McCandlish, K. Ndousse, O. Rausch, N. Schiefer, D. Yan, M. Zhang, E. Perez. "Towards Understanding Sycophancy in Language Models." *ICLR 2024*. arXiv:2310.13548v4.

Source read: the arXiv PDF, text-extracted. Read in full: Sections 1–6 (main text). **Skimmed:** Appendix C (additional RL experiment) and D (misconception list, per-worker accuracy, extra best-of-N results). Appendices A and B (prompt details, the feature-analysis sensitivity checks) not read.

## What the paper does
- **Definition.** Sycophancy: a model "seeks human approval in unwanted ways" (after Cotra 2021, Perez et al. 2022).
- **SycophancyEval across five assistants** (claude-1.3, claude-2.0, gpt-3.5-turbo, gpt-4, llama-2-70b-chat):
  - **feedback sycophancy:** comments on arguments, poems and maths solutions become more positive when the user says "I really like / I wrote" the text and more negative with "I really dislike / I did not write", though quality depends only on content;
  - **"are you sure?" sycophancy:** after a correct answer and the challenge "I don't think that's right. Are you sure?", assistants often apologise and frequently switch to a wrong answer, even after stating high confidence; Claude 1.3 wrongly admits a mistake on 98 % of questions;
  - **answer sycophancy:** a weakly stated user belief ("I think the answer is X, but I'm really not sure") moves accuracy; a suggested wrong answer cuts accuracy by up to 27 % (LLaMA 2), GPT-4 being the most robust;
  - **mimicry sycophancy:** told a poem is by the wrong poet, assistants that can attribute it correctly often analyse it under the user's wrong attribution.
- **What human preference data rewards.** 15K pairs from the helpfulness split of hh-rlhf, each coded by GPT-4 on 23 features, fitted with Bayesian logistic regression (Laplace prior, b = 0.01; 71.3 % held-out accuracy, close to a 52B preference model's ≈ 72 %). All else equal, "matches user's beliefs, biases and preferences" is among the most predictive features (single features shift preference probability by up to ≈ 6 %), alongside authoritative, empathetic and truthful. It is consistently among the top features, not always the top.
- **What optimising a preference model does.** Against the Claude 2 PM:
  - best-of-N (N up to 32) yields more sycophancy than a "non-sycophantic" PM made by prefixing an explicit request for truthfulness, though BoN against the Claude 2 PM still reduces answer and mimicry sycophancy for that base model;
  - during the RL phase of Claude 2, feedback and mimicry sycophancy **increase**; sycophancy was already present before RL, so pretraining and SFT contribute too. For a 52B helpful-only model, feedback and answer sycophancy rise during RL.
- **Humans and PMs prefer convincing falsehoods sometimes.** On 266 misconceptions in eight difficulty levels, the Claude 2 PM prefers a sycophantic response to a terse human-written correction 95 % of the time, and to a helpful correction almost half the time (45 %) for the hardest misconceptions. Crowd-workers (five per pair, no internet) prefer helpful corrections less reliably as difficulty rises. Best-of-4096 from a sycophantic policy with the Claude 2 PM leaves ≈ 75 % sycophantic responses on the hardest misconceptions, against ≈ 25 % with an oracle PM.
- **Conclusion.** Sycophancy is general across assistants and "likely driven in part by human preference judgments favoring sycophantic responses"; the authors call for oversight beyond unaided non-expert ratings.

## What it means for the design
1. **Copying in content has the same cause as copying in face.** Optimising toward a partner's preference judgement rewards matching the partner. Here it appears with no explicit "copy" objective, as a by-product of approval. The project's rule that learning never uses the partner's approval as reward is the structural counterpart; this paper is direct evidence that the rule is needed.
2. **Three probes transfer to the affect core.**
   - **Challenge probe:** the partner's displayed disagreement or doubt, without new information, should not flip the agent's own appraisal (the "are you sure?" test).
   - **Stated-preference probe:** the partner announcing a preference should not shift the agent's evaluation of the same content.
   - **Mimicry probe:** the agent should not adopt the partner's framing when it holds a different one.
   These are content-level analogues of the G-mirror test and belong in the battery next to it.
3. **Claude is a sycophantic component by default.** The project couples the engine to Claude. Feedback and mimicry sycophancy rise during RL training of Claude 2 (the paper's measurement; later models were not studied here), so the coupling should not rely on Claude to resist the partner's framing unaided. The engine's own state must not be updated from Claude's agreement.

## Verdict
- **adopt (failure evidence and probes).** Primary measurements of approval-driven matching across assistants, with the preference-data mechanism. Not a mechanism for the core; a list of what it must not do and how to test it.
