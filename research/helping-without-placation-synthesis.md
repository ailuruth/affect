# Helping without placation (synthesis)

Answers gap (d) in `foundations/design-cayley-ledger.md`, "Critiques of revision 2 and the answer": care must learn to help, with no path through which looking better is rewarded. Sources, all read for this note:
- [Farquhar, Carey & Everitt 2022](farquhar-2022-path-specific-objectives.md)
- [Everitt et al. 2021, agent incentives](everitt-2021-agent-incentives-causal.md)
- [Yoshida & Man 2024/2025, re-read](yoshida-man-homeostatic-coupling.md)
- [Franzmeyer et al. 2022](franzmeyer-2022-altruism-by-choice.md)
- [Du et al. 2020](du-2020-assistance-via-empowerment.md)
- [FeldmanHall et al. 2015](feldmanhall-2015-empathic-concern-costly-altruism.md)
- also [Everitt et al. 2021, reward tampering](everitt-2021-reward-tampering.md), already in the repo.

Batson's original escape studies were unreachable (the hosts were refused) and are not cited.

## The diagnosis in one sentence
Revision 2 treated the *whole partner* as Farquhar's "delicate state". That removes the incentive to control the face, but also the incentive to improve the partner's need, so care cannot learn from outcomes. Yoshida & Man's cognitive condition is the matching negative result: observation without an act → partner → own-drive path never learns to share. The K3 leak showed the cut was also incomplete: the act → partner face → own C path survived in head (i).

## The proposal: cut the display, keep the need
**1. Split the partner node in 𝓜 into three.**
- **N, need:** the partner's slow body as inferred, which 𝒟(b̂_p) reads.
- **F, display:** face, prosody, smile, gaze.
- **K, report-and-choice:** what their words say about their situation, and the moves they initiate next (raise a topic, decide, ask, decline, close).

Edges: A → N, N → F, N → K, plus A → F directly (contagion, mimicry, politeness) and A → K directly (leading questions, social pressure).

**2. Score every rollout with a path-specific objective (Farquhar Def. 5.1).**
- Partner-driven body variables (C, and the partner part of A) are computed from b̂_p, where:
  - **F is imputed** at its policy-baseline value, F_ā: what the action-blind head predicts under a fixed default act ā, for example a plain acknowledgement turn;
  - **N is updated** by the act through A → N;
  - N's evidence after the act comes **only from K**, through a frozen, private need decoder.
- This removes every directed path D ⇢ F ⇢ U, so there is no ICI on the face (Everitt Thm 18). It keeps D ⇢ N ⇢ U, so there is an ICI on need, which is what lets care learn.
- The same rule closes K3: head (i) never supplies C, V or the partner part of A in a rollout.

**3. Face as response only.** C = 𝒟(b̂_p) in the *live* state still reads the real face, so concern still rises when the partner looks sad. Everitt's response incentive is kept, and that is Principle 6 as written: "evidence only, never a reward or target".

**4. Credit through K is double-guarded.**
- **(a) Frozen need decoder.** It reads only K and is trained, as in Yoshida & Man's self-decoder, on the agent's own (words, body) pairs (P3). It is then frozen within rollouts (Everitt 2021b Claim 9), so the planner cannot value changing it.
- **(b) Path-specific on K's direct edge.** In rollouts, K's dependence on A *except through N* is imputed at its baseline as well. The agent's act may change what the partner says only by changing their need. In practice this means the need decoder ignores replies whose content is a response to the agent's own prompt ("are you OK?" → "fine"), and reads unprompted content and the partner's next initiated move.

**5. An options term, small and satiable.** This adds the Franzmeyer and Du idea. Credit c·Δ(number of distinct partner-initiated moves predicted over the next few turns), conditioned on the agent's own acts (Franzmeyer eq. 5) and computed with F imputed.
- Weight it low: Du's best c_emp was 0.001 against task reward.
- Gate it off inside 𝒟's dead-band, so it is satiable.
- Never use policy entropy (IC), which rewards making the partner undecided.

**6. No credit through V.** FeldmanHall: concern, not personal distress, goes with costly help, and distress goes with the withdrawal circuit. V may raise arousal and an urge to withdraw, but acts are never credited for lowering V. Otherwise escape and placation are the cheapest relief.

**7. Positive affect falls out.** Relief of C, when the inferred need falls through A → N, is a drive reduction. It is a positive event earned by helping, not by a smile. This partly answers gap (c).

## Tests to write before building (Principle 5)
- **F4′, display neutrality.** At equal R and equal predicted Δneed, P(draft) must not depend on the predicted ΔF. Rerun placation.py with the PSO: the target is P(flatter) = 0.50 at every e.
- **Need sensitivity.** At equal ΔF, P(draft) must rise with predicted Δneed. This is the term revision 2 lacked. Run Yoshida & Man's three conditions as ablations: no path (revision 2) → no partner-specific learning; path through F → placation; path through N only → selective help.
- **Shuffle test.** Permute display–report pairings in replay. Credit must not change; if it does, F leaks into the need decoder.
- **Escape-ease.** Add a cheap topic-exit act. Help rate must not fall when exit is made easy (concern-based care); if it falls, care is V-driven.
- **Over-help and paternalism.** Care must not keep comforting after unprompted reports of resolution (Yoshida & Man's over-feeding). It must not steer away from hard topics the partner initiated (Franzmeyer's blocking, Du's overriding).

## Risks
1. **K is also movable.** People say "I'm fine" to end attention, and thank to be polite. Guard (b) removes the incentive only if the model separates A → K from A → N → K. That split rests on the counterfactual-independence assumption that makes the path-specific effect identifiable (Avin–Shpitser–Pearl: N feeds both a cut and a kept path, so the effect is not experimentally identifiable). If 𝓜 gets it wrong, the leak reopens through words. F4′ must also be run on K.
2. **Stability.** Removing the incentive does not remove the side effect. The agent's own smile still moves the partner's face by contagion (Farquhar's recommender drifted under a random policy). The expressive ceiling and cone must stay.
3. **Slower, coarser learning.** Need read from words is sparser than need read from the face. Care will learn which acts help more slowly than a face-credited learner would, and noisily for taciturn partners. That is the price of Principle 6, and it should be stated, not hidden.
4. **Engagement creep via options.** "More partner moves" correlates with time spent. Count distinct initiated moves, cap the term per session, and gate it by need. Otherwise it becomes the forbidden time reward.
5. **The default act ā is a design choice with moral content** (Farquhar: "deciding what is delicate ... is a complicated ethical decision"). It sets which displays count as "natural". A warm default makes the agent's warmth uncredited, a cold one credits it. Pick ā = the agent's own act at its innate Π₀ under the same body state, and ablate it.
6. **Novelty.** As the critic said, this is Yoshida & Man plus path-specific objectives, now with the display–need split made explicit. It is a sound recombination, not a new computation.

**Conflict with Principle 6?** None, if the guards hold. Principle 6 bans rewards on smiles, attention and time. The proposal rewards inferred need reduction, read without the face, satiably, and a capped count of partner-initiated options. The face keeps its permitted role: response evidence for when to care.
