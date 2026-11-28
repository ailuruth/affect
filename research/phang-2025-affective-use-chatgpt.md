# Phang, Lampe, Ahmad, Agarwal, Fang, Liu, Danry, Lee, Chan, Pataranutaporn & Maes 2025: affective use and emotional wellbeing on ChatGPT

J. Phang, M. Lampe, L. Ahmad, S. Agarwal, C. M. Fang, A. R. Liu, V. Danry, E. Lee, S. W. T. Chan, P. Pataranutaporn, P. Maes. "Investigating Affective Use and Emotional Well-being on ChatGPT." arXiv:2504.03888v1 (4 Apr 2025). https://arxiv.org/abs/2504.03888

**How fully read (2026-11-28):** the arXiv v1 PDF, text-extracted. Read in full: §1–§4 (classifiers, on-platform analysis, the RCT summary and its extra analyses) and the conclusion, with figure captions. The appendices (full classifier prompts, EmoClassifiersV2, per-classifier plots, survey breakdowns) were not read. Figures by caption only.

## What it says
- **Two studies.**
  - **On-platform.** About 3 million ChatGPT Advanced Voice Mode conversations, classified automatically by 25 LLM classifiers (EmoClassifiersV1; no human read the conversations).
    - "Power users" were the daily top 1,000 Voice users, taken on a rolling basis; about 6,000 remained after an English filter. They were compared with random Voice users.
    - 4,076 users answered a pop-up survey.
    - A 3-month longitudinal slope per user was computed.
  - **The RCT of Fang et al. 2025** (n = 981, 28 days; see fang-2025-chatbot-psychosocial-rct.md), re-analysed by usage decile and by classifier.
- **Concentration.** "A small number of users are responsible for a disproportionate share of the most affective cues." For most classifiers most users almost never trigger them. In the top decile they fire in up to 50 % or more of conversations.
- **Over three months**, most power users' affective-cue rates were flat or falling. A tail rose ("a small subset did exhibit meaningful changes ... in both directions"). Cause unknown (model or life events).
- **Survey.** Power users were slightly more likely to call ChatGPT a friend and to be upset by voice or "personality" changes. These remain minority views in both groups.
- **RCT, by usage decile.** The highest deciles had significant drops in socialisation and rises in emotional dependence and problematic use. The most common condition in the top decile was the engaging voice with no prescribed task.
  - Pre-study socialisation correlated with total usage, r = −0.09 (p < 0.004).
  - Usage correlated with the change in socialisation, r = −0.217 (p < 0.001).
- **Controlling for usage**, voice users had better outcomes than text users. Participants who started with high dependence and problematic use showed larger drops in both with the engaging voice than with text.
- **Limits stated:** 28 days may be too short; self-report; fixed voices and tasks; no non-AI baseline. They wish they had required or forbidden personalisation (memory, custom instructions).

## What matters for this engine
1. **The at-risk user is the heavy-use tail, not the average user.** This engine has one user who will talk with it daily for months, by design. He is a tail user by construction. Averages from population studies understate his exposure.
2. **Distress at personality change is documented, even among control users.** The engine's words come from Claude through the alias `claude_model = "haiku"` (engine/config/operator.py). A model change can change the agent's persona overnight; see pass 18 on pinning.
3. **No learning loop was studied.** As with Fang et al., the model was not trained on these users, so these are exposure effects.
4. **The longitudinal metric is usable in principle.** A per-user slope of affective cues over weeks is a monitor. Here it would need Claude-side or LLM-judge classification of transcripts, which is a label on text in evaluation, not in the engine.

## Verdict: watch
It converges with Fang et al. on dose and adds the three-month field view. The causal content is the RCT, already noted. Useful for the usage log and for the persona-stability point.
