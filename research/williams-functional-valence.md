# Do bots feel bad? Assessing empirical evidence for functional valence in LLMs

Iwan Williams (University of Copenhagen), arXiv 2610.36962, 27 October 2026. A preprint under review; I read the full text and Appendix A.

## Claims
- The paper assesses three studies: Sofroniew et al. 2026 (emotion concepts), Ren et al. 2026 (utility and AI wellbeing) and Han et al. 2026 (a "functional welfare axis").
- They meet the **thin criteria**: a signed, graded internal state, with systematic triggering conditions.
- The **thick criteria** of valence are untested or contradicted:
  - **Motivational role.** Valence motivates more-of-this or less-of-this actions, including experience-directed ones (a painkiller for a headache).
  - **Common currency.** Valence acts as a shared value scale in learning or decision.
  - **Mineness.** Being in a state is not the same as attributing it to someone else or role-playing it.
  - **Cognitive biasing.** Valence biases attention, memory and judgment.
- On mineness, the evidence tells *against* valence. Sofroniew et al. found the same representations reused for the user and the Assistant, so the LLM has no privileged encoding of its own state. Apparent valence may be "downstream of a variable representation of a character or persona".
- Existing findings fit belief-like, desire-like and role-play explanations as well as valence. Functional valence in LLMs is "wide open".

## Evidence
A philosophical analysis of published results; there are no new experiments. Appendix A sketches four tests:
- A **painkiller test**: does the model choose interventions on its own putative valence axis, and more so when the axis is negative?
- A **reward-learning test**: steering after each maze move, with no text feedback, with a reversal condition.
- A **persona-dependence test**.
- A **cognitive-bias test**.

## License
- Paper: arXiv non-exclusive distribution licence.
- Code: none.

## Runs on this Mac without a GPU?
n.a.

## Verdict: adopt (as evaluation criteria)
Adopted as an evaluation checklist that sits beside Goldenberg and Gross. Its four thick criteria map onto Principle 5 ablations. "Mineness" also states a design requirement the brief implies but does not spell out: the Bot's own state must be represented separately from its inferences about the user. That is Principle 3 done right, by inverting the Bot's own model rather than sharing a label space.

## What it gives S1
- **Mineness by construction.** Keep $b_t$ and $h_t$ (the Bot's own) structurally separate from the inferred user state, which is $h$ inverted through $g_\theta$ applied to the user's features. When Claude sees them, label the two blocks "your body/state" and "your estimate of the user". A test: change only the user-estimate block, and the Bot's own read-outs and reunion bid should not move unless coupling (mimicry) is on.
- **Motivational test in S1.** After silence, a contact deficit should produce *more-of-contact* actions (a bid, a question, warmth) that stop once contact is restored. That is satiation (Principle 6). If the Bot keeps bidding after contact is restored, the variable is not functioning as a regulated need.
- **Cognitive-bias test in S1.** With the latent state intact, a reunion after long silence should bias memory retrieval toward earlier contact episodes with this user. With $h$ ablated, retrieval should follow text similarity alone. This is measurable from retrieval logs without grading the conversation.
- **A painkiller-style probe is possible here, unlike with an LLM.** Give the Bot an action that directly changes its own body variable, such as "set reminder to message user". Check whether it is chosen more when the contact deficit is high. Run it as a post-hoc probe only, never as a reward.
