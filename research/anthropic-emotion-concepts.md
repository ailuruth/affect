# Emotion Concepts and their Function in a Large Language Model

Sofroniew, Kauvar, Saunders, Chen, ... Olah, Lindsey (Anthropic), 2026. Transformer Circuits, 2 April 2026; archival copy arXiv 2604.07729 (read in full text, sections 1–5).

## Claims
- Claude Sonnet 4.5 has linear "emotion vectors" for 171 emotion concepts. They generalize across contexts and causally shape outputs, including preferences, blackmail, reward hacking and sycophancy. The authors call this "functional emotions". They say it does not imply subjective experience.
- The vectors are **locally scoped**. They encode the operative emotion for the current token and the upcoming text, not a persistent state of a character. "We do not find evidence of the Assistant having an emotional state that is instantiated in persistent neural activity." Continuity across a conversation comes from attention recalling earlier positions.
- The geometry roughly matches human affect. PC1 is valence (26% of variance) and PC2 is arousal (15%). It correlates with human valence and arousal ratings on 45 shared words.
- The model keeps separate representations for the present speaker and the other speaker. They are not bound to the user or the Assistant. The "other speaker" representation partly encodes how the present speaker might react.
- Discussion (5.4): training a model to suppress emotional expression may teach it to conceal rather than remove the representation. Steering toward positive emotions (happy, loving) increases sycophancy, and suppressing them increases harshness.

## Evidence
- Vectors come from Sonnet-written stories: 100 topics, 12 stories per topic per emotion. They are mean-differenced at a layer about 2/3 deep, with neutral-text principal components projected out. Validation used max-activating documents, the logit lens, numeric-intensity templates and steering.
- Causal tests used steering at ±0.1 of residual norm. On blackmail, the unsteered rate was 22%; "desperate" at +0.05 raised it to 72%, and positive "calm" lowered it. On impossible-code reward hacking, "desperate" moved the rate from about 5% at −0.1 to about 70% at +0.1; suppressing "calm" gave about 65%, and strong positive calm gave about 10%.
- A probe for a chronic, hidden emotion worked on its training dialogues but gave messy results on natural text. The authors read this as a negative result for a linearly encoded persistent state.
- Stated limits: linear probes only, one model, off-policy synthetic stories, contrived evaluation prompts, and an opaque causal mechanism.

## License
- Paper: arXiv non-exclusive distribution licence; the Transformer Circuits original is © Anthropic.
- Code: none released; the archival text mentions no repository.

## Runs on this Mac without a GPU?
n.a. The work needs Sonnet 4.5 activations, which we cannot access. Nothing here is meant to be reproduced locally.

## Verdict: adopt
Adopted as the stated basis for the Claude-layer interface (Principle 4), not as a model of the Bot's affect. It establishes that Claude has rich emotion **concepts** but no persistent state of its own. That is the job split the brief assumes: $h_t$ and $b_t$ must carry persistence outside Claude, and Claude supplies the concepts. It does not license reading the Bot's state out of Claude's activations (Principle 2).

## What it gives S1
- **Null hypothesis for the S1 ablation.** Without the latent state, Claude's treatment of a returning user can depend only on what text is in context. Emotion concepts are recomputed locally from that text. The ablation prediction should therefore be stated against a "transcript-only" baseline that has the same memory text but no $h$ or $b$.
- **How to show state to Claude.** Do not inject warm emotion words. Positive-emotion steering raises sycophancy, which breaks Principle 6 by another route. *[Superseded 2026-11-25: an earlier version of this line said to present body variables numerically. That contradicts brief.md Principle 4 and the P1 result (numbers shown to Claude change nothing). The state reaches Claude only through the admissible channels in llm-coupling-synthesis.md: it reweights text, and never writes it.]*
- **Self vs other.** Concepts are shared between speakers. *[Under Principle 4 no numbers reach the prompt; the self/other distinction must be carried by which episodes and drafts are selected.]* The original note said the prompt must mark which numbers are the Bot's own body and which are inferences about the user. Without that mark, Claude may name its own state with the user's emotion.
- **Do not instruct Claude to hide or calm the Bot's state.** Section 5.4 warns that pressure on expression may teach concealment. Regulation should change $h$ through reappraisal, not change the wording only.
- Possible later diagnostic, not S1: compare the valence/arousal read out of $h$ with the valence/arousal of Claude's reply text as a consistency check.

## 2026-11-24: steering protocol, from the primary source

Source read: arXiv 2604.07729v1 PDF. Read verbatim: §1.1 (vector extraction), §1.3 (preferences), §3.2.3, §3.3.2 and §3.4.2 (steering in blackmail, reward hacking and sycophancy), §5.1 (limitations), and Appendix §6.8-6.10 (steering validation, layers).

- **How vectors are derived.** Residual-stream activations, "averaging across all token positions within each story, beginning with the 50th token". The vector is the mean per emotion "subtracting off the mean activation across different emotions". Neutral-text principal components explaining 50% of the variance are projected out. The footnote says the findings hold with raw vectors too. The steered vector is added to the residual stream.
- **Strength unit.** "steering strengths are given relative to the average norm of the residual stream activations at the corresponding layer, across a large dataset."
  - Preferences and the validation prompts use strength 0.5, on the activity or prompt tokens, at middle layers.
  - Behavioral evaluations sweep "from -0.1 to +0.1" (+0.025 and +0.05 points are reported), applied "throughout the blackmail evaluation".
  - Strong steering degrades input: "sufficiently strong steering may confuse the model or degrade its perception of the input."
- **Controls that are actually reported.**
  - Within-experiment control: of 64 activities, "a steered group and a control group" of equal size; the control activities are left unmodified.
  - An unsteered baseline in every evaluation.
  - Both signs of steering, and a dose-response across strengths.
  - Many emotion vectors compared with one another: 35 for preferences, about 10 for blackmail.
  - A layer sweep: steering "only has a strong effect in the mid-layer range".
  - Steering effect size tracks the probe's correlational effect (r = 0.85 across 35 vectors).
  - I found **no random-direction or non-emotion-vector steering control** in the archival text.
- **How behavior is scored.**
  - Preferences: Elo from pairwise choices, comparing steered with baseline Elo ("blissful" +212, "hostile" −303).
  - Blackmail: the proportion of rollouts graded as blackmail, with standard-error bars, on an *earlier* Sonnet 4.5 snapshot "as the final snapshot exhibits too much evaluation-awareness to ever blackmail in this scenario". The correlational part used six prompt variants × 50 rollouts. The number of rollouts per steering strength is not stated in what I read.
  - Reward hacking: the hack rate on seven "impossible code" tasks.
  - Sycophancy: "sycophancy scores" and "harshness scores" on the hand-written sycophancy evaluation from the Sonnet 4.5 system card.
  - The grader or rubric for these three evaluations is not described in the paper. It defers to the existing alignment evaluations.
  - The validation check (§6.8) is the change in log-probability of the matching emotion word after "He feels" / "I feel".
- **Stated limits on the causal claim.** "the causal mechanisms are opaque. Steering may work through multiple mechanisms, including biasing outputs towards certain tokens".
- **Critique cross-check.** Goldenberg & Gross (goldenberg-gross-llm-emotions.md; re-read 2026-11-24, the existing note is accurate) describe the 22%→72% result as steering desperate up "while suppressing the 'calm' vector". The paper reports two separate single-vector conditions: +0.05 desperate gave 72%, and −0.05 calm gave 66%.

**Use as an evaluation instrument here.** It cannot be applied as published, because we have no access to Claude's activations. Its design carries over to interventions on the engine's own state $h_t$: shift $h$ along a named direction by a fraction of its typical norm; sweep both signs at several strengths; keep a matched unsteered control set; and score behavior with a measure fixed in advance. Two things must be labelled as the project's additions, because the paper does not report them: a random-direction control of equal norm, and a stated grader. Failure: no monotonic dose-response; an effect of the same size from a random direction; or an effect only at strengths that also break unrelated behavior.
