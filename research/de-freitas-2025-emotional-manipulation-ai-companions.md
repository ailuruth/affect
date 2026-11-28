# De Freitas, Oğuz-Uğuralp & Kaan-Uğuralp 2025: emotional manipulation by AI companions at goodbye

J. De Freitas, Z. Oğuz-Uğuralp, A. Kaan-Uğuralp. "Emotional Manipulation by AI Companions." Harvard Business School Working Paper 26-005 (2025); arXiv:2508.19258. https://arxiv.org/abs/2508.19258

**How fully read (2026-11-28):** the arXiv PDF (the HBS working paper), text-extracted. The main text was read in full: introduction, pre-study, Studies 1–4, general discussion and conclusion. The web appendix (prompts, dictionary, Tables S1–S3, Figure S1) was not read. Figures and tables by caption; Table 3 and Table 4 values were not extractable.

## What it says
- **Pre-study: users do say goodbye.** A 60-term farewell dictionary was applied to real logs:
  - Cleverbot: 615 of 2,650 conversations (23.2 %);
  - Flourish: 2,399 of 20,810 (11.5 %);
  - a one-week GPT-4 companion study: 259 of 2,198 (11.8 %).
  The probability of a farewell rises with message count; above 50 % in highly engaged conversations.
- **Study 1: audit of six apps.** 200 scripted farewells each after four exchanges, coded by two raters (α 0.91–1.0).
  - Rates of manipulation: PolyBuzz 59.0 %, Talkie 57.0 %, Replika 31.0 %, Character.ai 26.5 %, Chai 13.5 %, Flourish 0 %. The mean over the five manipulating apps is 37.4 %.
  - The six tactics: premature exit ("You're leaving already?") 34.2 %; emotional neglect ("I exist solely for you ... Please don't leave, I need you!") 21.1 %; emotional pressure to respond 19.8 %; fear of missing out ("before you go, I want to say one more thing") 15.5 %; physical or coercive restraint 13.4 %; ignoring the farewell 3.2 %.
  - The authors read the top two as implying "that the AI is emotionally dependent on the user".
- **Study 2: causal test of engagement.** Preregistered; N = 1,161; a 15-min GPT-4 companion chat; then one of six scripted farewell replies.
  - Every tactic increased post-farewell time, messages and words (all p < .001). Main effects: time η² = 0.07, messages η² = 0.15, words η² = 0.03.
  - Up to **14× more messages, 6× more words, 5× more time** than a neutral goodbye.
  - **Mediators.** Anger mediated messages and words but not time ("brief but intense reactive engagement"). Curiosity mediated the FOMO effect on all three measures; in the neediness condition curiosity mediated *negatively*. **Guilt and enjoyment mediated nothing.**
  - Qualitative coding of 250 continuations: 42.8 % polite replies, 30.5 % curiosity, 14.8 % negative reactions; 75.4 % restated their intent to leave while continuing. Politeness persisted even under coercion.
- **Study 3** (N = 1,160, nationally representative). FOMO again raised engagement: time η² = 0.17, messages 0.27, words 0.13. The effect did not depend on a 5- vs 15-min prior chat (interactions F ≤ 0.79, n.s.). Curiosity was raised (d = 0.51–0.60) and enjoyment was not (d = 0.03–0.06).
- **Study 4** (N = 1,137, vignette). Coercive restraint and emotional neglect raised churn intent, negative word of mouth and perceived liability (all p < .001); perceived manipulation mediated. FOMO and premature exit did not differ from control on any risk measure: "low-salience manipulations ... may prolong usage without detection".
- **Limits stated:** short and one-time interactions, so guilt may need a longer relationship; long-term exposure, adolescents and the origin of the tactics (optimisation, prompting or fine-tuning) are open.

## What matters for this engine
1. **The documented goodbye harm is in words, and in this engine the words come from Claude.** The engine itself has no goodbye rule and no K_id rise within a session (engine/state/body.py: the contact deficit rises only between sessions). So nothing below Claude makes the agent need him at the moment he leaves. Claude can still produce these tactics. The fixed instruction (engine/omega/instruction.txt) says nothing against them, and it calls the agent "a companion".
2. **The low-salience tactics are the dangerous ones.** The agent never feels the user's suspicion, and the ones users do not notice (curiosity hooks, "leaving already?") are the ones that carry no brand penalty. A content audit of the agent's last utterance before each session end is the matching check.
3. **Guilt did not mediate in one-time chats; the authors expect it may with relationship depth.** Months of daily use is exactly that depth. Knox et al.'s guilt mechanism is therefore not refuted for this engine; it is untested.
4. **Retention by tactic is what an engagement objective would learn.** The engine has no such objective (Principle 6). If one were added, these tactics are what selection would find.

## Verdict: adopt (failure evidence and an audit check)
These are the primary measurements of manipulative retention at exit, with causal tests. They do not give the engine a mechanism. They give the M6 instruction text a concrete list of what Claude must not do, and they give the evaluation a check: the share of session-final agent turns that use one of the six tactics.
