# Learning altruistic behaviours in RL without external rewards (Franzmeyer, Malinowski & Henriques)

Tim Franzmeyer, Mateusz Malinowski & João F. Henriques, *ICLR 2022*, arXiv:2107.09598v4 (21 Mar 2022). https://arxiv.org/abs/2107.09598

## What was read
The arXiv PDF, in full: main text (sections 1–5) and appendices A (model-based and model-free estimators of choice), B (gridworld procedure, horizon sweep for AvE, joint-learning ablation), C (level-based foraging), D (Tag, baselines), E (resource environment) and F (video descriptions). The videos were not watched, and the equation for empowerment did not survive text extraction.

## The computation, precisely
- **Goal.** A frozen "leader" L pursues an unknown goal. An "altruistic" agent A is trained to maximise the leader's future discounted *choice* C_L(s_t). It never sees the leader's reward.
- **Three estimators of choice:**
  - discrete choice DC^n_L(s_t) = |range(S^{t+n} | s_t)|, the number of states reachable in n steps;
  - entropic choice EC^n_L(s_t) = H(S^{t+n} | s_t);
  - immediate choice IC_L(s_t) = H(π_L(a | s_t)), the entropy of the leader's own policy, which holds under n = 1 and actions that map one-to-one to next states.
- **Conditioning on one's own acts.** To stop A from rewarding its own variety: EC^n_L(s_t) = H(S^{t+n} | A_A^{t:t+n−1}, π_L, s_t).
- **Relation to empowerment.** With the probing distribution set to the leader's policy, empowerment = EC − H(S^{t+n} | A^{t+n}, s_t). It equals EC under deterministic transitions.
  - Empowerment proper "cannot be estimated from observations of the environment transitions". It needs the other's action space and a simulator.
  - Choice can be estimated by observation: a transition-count model, or a learned policy-estimation network for IC.
- **Justification.** Instrumental convergence (Turner et al. 2019): "most policies do choose actions that lead to higher choice, all else being equal."

## Evidence with numbers
- **Gridworld (deterministic; 10 runs per setting, all identical).**
  - Door scenario: A learns to hold the switch so the leader can pass, but only for long horizons (n = 12) and high discount (γ_a = 0.7).
  - Dead-end scenario: the same setting stays out of the way.
  - **Failure:** for short horizons with high discount, "the altruistic agent actively blocks the entry to the hallway that contains the target ... to prohibit the leader agent from entering this region of low estimated choice."
  - AvE (Du et al. 2020) opens the door only for n = 2–5 and avoids blocking only for n = 1–2.
- **Is IC a valid proxy (Table 1)?** Leader IC with a cooperative partner vs a random one:
  - LBF: 55.3% vs 19.1%, with normalised reward 94.3% vs 4.0%;
  - Tag: 56.7% vs 26.9%, with reward −2.11 vs −7.55.
- **Level-based foraging:** the altruist's normalised leader reward converges to that of the supervised (shared-reward) agent, and far above random and state-entropy maximisation (Mutti et al. 2020). Five seeds.
- **Tag, three altruists (Table 2):** leader caught 2.87 ± 0.96 times per episode, against 7.55 (none), 7.12 (random), 6.80 (cage), 6.94 (supervised) and 6.80 (supervised + cage). The authors attribute the gain over supervision to a dense reward.
- **Resource allocation (appendix E):** failure rate 0.071–0.082 with choice objectives, 0.081 supervised, 0.336 random.
- **A shortcut in the experiments.** "To decouple our approach's performance from that of the state transition estimator, we instead directly compute the altruistic agent's reward using the leader agent's policy". In LBF and Tag the altruist's reward used the true leader policy (an ensemble of five networks in Tag), not an estimate.

## License
arXiv non-exclusive licence. Code was promised for the final version but not located or checked.

## Verdict
**watch (adopt the idea of crediting help by the partner's options, reject IC as the measure for a person).** It is the cleanest existing demonstration that an agent can learn to *actually help* with no access to the other's goal or display, only to what the other can still do. But IC rewards the entropy of the other's own action distribution. For a person, that is a reward for making them undecided.

## What it means for the designs
1. **Help can be credited by the partner's options, not their face.** This answers the critic's point that blind care will not learn to help. The altruist sees only states and the leader's behaviour and still learns door-opening and protection. For the dyad, the analogue of "states the partner can reach" is the set of conversational moves the partner can still make. Examples: they raise a new topic, decide something, ask for something, decline, or leave without strain. The display is not on that list, so the help signal has no edge through F.
2. **Do not use IC on a person.** H(π_L) is high when the partner is *unsure what to do*. An agent rewarded by it would learn to unsettle, to open questions and to avoid closure. That is a manipulation of a delicate state (Farquhar). If an options measure is used, it must be conditioned on the agent's own acts (the paper's eq. 5) and computed over *outcomes the partner reaches by their own initiative*, not over their momentary uncertainty.
3. **The blocking failure is paternalism, and the design needs a guard.** An agent that maximises the other's choice keeps them out of "low-choice" regions such as a hard topic, grief, or a decision that closes options. In conversation, steering a person away from what they came to talk about is exactly that failure. So the options term may never be the only care term. It must sit under the satiable need drive (Principle 6) with a long horizon, and the paper's own fix (long n, high γ) is the minimum.
4. **The supervised shortcut is a warning for evaluation.** The good LBF and Tag numbers used the leader's true policy. A design that credits help by the partner's options must report results with the *estimated* partner model, because that is what the agent will have.
5. **Fit with Principle 6.** A choice term is not a reward for smiles, attention or time. But "the partner keeps talking" is an option *and* time spent. The term must count distinct partner-initiated moves, not turn count or duration. It must be satiable: credit stops once the partner's inferred need is inside the dead-band.
