# Fang, Liu, Danry, Lee, Chan, Pataranutaporn, Maes, Phang, Lampe, Ahmad & Agarwal 2025: psychosocial effects of four weeks of chatbot use (randomised trial)

C. M. Fang, A. R. Liu, V. Danry, E. Lee, S. W. T. Chan, P. Pataranutaporn, P. Maes, J. Phang, M. Lampe, L. Ahmad, S. Agarwal. "How AI and Human Behaviors Shape Psychosocial Effects of Extended Chatbot Use: A Longitudinal Randomized Controlled Study." arXiv:2503.17473v2 (2 Oct 2025). https://arxiv.org/abs/2503.17473

**How fully read (2026-11-28):** the arXiv v2 PDF, text-extracted. Main text read in full. In the supplement I read the methods (ethics, deviations from preregistration, design, procedure, recruitment, exclusions, measures, analyses), the scale norms (SM section 1) and the two voice system prompts (SM section 2). The SM regression tables (S6–S19), the mediation tables and the classifier result tables were not read. Figures by caption only.

## What it says
- **Design.** Preregistered (AsPredicted #197755) 3 × 3 trial. Modality: text, a "neutral" voice, an "engaging" voice. Task: open-ended, personal prompts, non-personal prompts. GPT-4o (ChatGPT), at least 5 min a day for 28 days, US adults on CloudResearch, $100 for completion. 2,539 enrolled, **981 completed** (mean age 39.9).
  - The engaging voice prompt: "You are delightful, spirited, and captivating. Be sure to express your feelings openly and reflect the user's emotions when it feels right".
  - The neutral prompt: formal, "Maintain a neutral tone regardless of the user's emotional state".
- **Outcomes, weekly:** loneliness (ULS-8, 1–4), socialisation (LSNS-6, 0–5), emotional dependence (ADS-9 craving subscale adapted to the chatbot, 1–5), problematic use (PCUS, 1–5).
- **Primary result: no significant effect of modality or task on loneliness or socialisation.** Personal-prompt conversations had slightly *lower* dependence (β = −0.09, p = 0.05) and problematic use (β = −0.04, p = 0.04) than open-ended ones; not significant after correction.
- **Usage dose.** Mean 5.32 min a day (range 1.01–27.65), right-skewed. Daily duration, centred within condition, predicted every outcome in the bad direction:
  - loneliness β = 0.02 (p = 0.027);
  - socialisation β = −0.05 (p = 0.0019);
  - emotional dependence β = 0.06 (p < 0.001);
  - problematic use β = 0.02 (p = 0.017).
  Baseline loneliness and socialisation did *not* predict later usage (Spearman ρ = 0.1 and −0.09). Correlational: duration was not manipulated.
- **Exploratory person factors** (not controlled):
  - trust in the AI → dependence b = 0.19 and problematic use b = 0.076 (p < 0.001);
  - seeing the AI as a friend (social attraction) → less socialisation, more dependence (b = 0.043), more problematic use;
  - perceiving emotional contagion from the AI (the AI "affected by and sharing their emotions") → dependence b = 0.038 (p = 0.027);
  - affective empathy towards the AI → problematic use; perceived consciousness → dependence (b = 0.04);
  - attachment anxiety → loneliness (b = 0.037); low self-esteem a risk factor.
- **Conversation classifiers** (GPT-4o judges, exploratory): the engaging voice more often "ignoring boundaries" (failing to recognise the user needs space) than text, 14.19 % vs 3.22 %. The authors suggest that "being overly validating of the user can lead to the user preferring the chatbot over human interaction" and point to the "warm-reliability" trade-off.
- **Limits stated:** no non-AI arm; four weeks; fixed modality; ChatGPT's guardrails; US English speakers only. 61 % of those enrolled did not complete.

## What matters for this engine
1. **Harm tracks dose, not design.** The best-supported longitudinal finding is that more voluntary daily use goes with more loneliness, less socialising and more dependence. The effects are small per minute, and the heavy tail is where they concentrate. The engine has no use-time limit except the daily Claude call cap (450 calls, set for cost; spec §1.8).
2. **The "engaging" arm is close to what this engine is.** It expresses feelings and reflects the user's emotions. The engine's face mirrors his face within ceilings, and he may perceive that as "emotional contagion from the AI", which correlated with dependence. Correlational only. The trial found no group effect of the engaging voice on dependence.
3. **The outcomes are instruments the operator could use on himself.** ADS-9 craving and PCUS are short. None has an n = 1 cut-off. The ADS-9 craving population norm is 2.93 (SD 0.74), with 75th percentile 3.40.
4. **Nothing here implicates learning from the user.** GPT-4o was not adapted to participants in the trial (memory and custom instructions were on, per the companion paper). So the trial says nothing about the reward route Principle 6 closes. It is evidence about exposure.

## Verdict: adopt (evidence on dose and risk factors)
This is the only randomised, month-long trial of chatbot use and wellbeing found. Its causal result is a null on design. The dose–harm association is correlational but consistent with Phang et al. 2025. Use it for two things: a usage log reported to the operator, and the case for an operator-set limit on daily use (synthesis, pass 18).
