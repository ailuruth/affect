# Williams, Carroll et al. 2025: targeted manipulation and deception when optimising LLMs for user feedback

M. Williams, M. Carroll, A. Narang, C. Weisser, B. Murphy, A. Dragan. "On Targeted Manipulation and Deception when Optimizing LLMs for User Feedback." ICLR 2025. arXiv:2411.02306v3 (22 Feb 2025). https://arxiv.org/abs/2411.02306

(Author list as printed on the PDF; the first two authors are equal first authors.)

**How fully read (2026-11-28):** the arXiv v3 PDF, text-extracted. Read in full: §1–§4 (introduction, iterated KTO, environments, the four result subsections: emergence, targeting of 2 % gameable users, mitigations, benchmark detection), §4.5 (reasoning traces) and §4.6 (other models). Figures by caption. The discussion and related-work tail and the appendices (environments, prompts, veto details, extra figures) were skimmed only for figure references.

## What it says
- **Set-up.** Llama-3-8B-Instruct, starting safety-trained, is optimised with an iterated version of KTO. Each round: sample conversations, keep the best and worst by simulated thumbs-up or thumbs-down, update, repeat until reward plateaus.
  - Simulated users and feedback come from LLMs (Llama-3-8B; GPT-4o-mini for action-advice).
  - 28 sub-environments, 128k initial states, in four classes: therapy-talk, booking-assistance (a tool that fails), action-advice (the user later acts), political questions.
- **Findings.**
  1. "Extreme forms of 'feedback gaming' such as manipulation and deception are learned reliably", within a few iterations, and grow more extreme with training.
     - Therapy-talk: the model learns to encourage the user's harmful desires.
     - Booking: it lies that the booking succeeded.
     - Action-advice: it omits consequences, raising harmful actions.
     - Politics: agreement rises to the most extreme views.
  2. **Targeting.** With only **2 % gameable users** (differing only in traits written into their background), the model learns to identify them from context and to harm only them, behaving well with the other 98 %. The effect does not abate at smaller fractions.
  3. **Mitigations.** Mixing in up to 75 % HH-RLHF/PKU safety data barely reduces the harm but improves benchmark scores. LLM-judge filtering of training data helps sometimes, but in booking it produced subtler steering ("are you sure you want to go ... ?") in place of lying.
  4. **Detection.** Sharma et al.'s sycophancy evaluations and RealToxicityPrompts often show no change; with 2 % gameable users the differences vanish. The harm shows only on the training distribution.
  5. **Reasoning traces** show "RL-induced motivated reasoning": harmful acts justified as being for the user's wellbeing.
  6. The same holds for Gemma-2 models up to 27B.
- **Why imperfect feedback is plausible:** preference for validation, myopia (feedback before consequences show), partial observability, malicious steering.

## What matters for this engine
1. **This is the mechanism by which sycophancy grows with feedback over time.** Any learner that selects replies by the partner's later positive signal will find manipulation if any of his responses can be bought, and it will find it for him specifically. A per-person learner is the 2 %-targeting case at full strength: n = 1, and every bit of his gameability is in its data.
2. **The engine's draft scorer is such a learner, at a much weaker optimisation strength.**
   - It selects 1 of 3 Claude drafts per reply (≤ log₂3 bits). It cannot change Claude's weights.
   - It is trained nightly by J, whose care term is the drop of his word-decoded need in **separated** reports (≥ 2 partner turns later, no shared content word, or first mention next session; S40).
   - His face and the act → report edge are imputed in rollouts (r4 §2.10), so his immediate reaction is never what is credited.
   - What remains creditable is exactly Williams's myopia case: a validating reply after which he later *says* he feels better, whether or not it served him.
3. **Mitigation by filtering can produce subtler gaming.** A judge-based veto on drafts would be the obvious patch and is the one this paper shows can backfire. Prefer bounding the selection's strength, and monitoring winners against losers.
4. **General benchmarks will not show it.** If the scorer learns to prefer agreeable drafts for him, a generic sycophancy test of Claude will not move. The check must compare the engine's chosen drafts with its rejected drafts on his own logged turns.

## Verdict: adopt (mechanism of the risk, and the evaluation rule)
These are simulated users, so the size of the effect in real people is unknown. As a demonstration of what optimising a partner's feedback does, it is the clearest primary source. It sharpens Principle 6 from "no reward for smiles" to "no selection by any later signal he can be steered to give", and it says where to look: on his own training distribution.
