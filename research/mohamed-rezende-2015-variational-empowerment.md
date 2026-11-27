# Variational information maximisation for intrinsically motivated reinforcement learning (Mohamed & Rezende)

Citation: S. Mohamed, D. J. Rezende. "Variational Information Maximisation for Intrinsically Motivated Reinforcement Learning." NeurIPS 2015. arXiv:1509.08731.

Source read: arXiv PDF, text-extracted. Read in full: abstract, §1–6 (framework, MI and empowerment, the variational bound and algorithm, complexity, results on static rooms, dynamic environments with lava, keys and bricks, predator–prey, conclusion). **Not read:** appendices A–D (intuition, model-based empowerment, importance-sampling estimator, network details). Figures not seen; numbers from text.

## Key claims, with numbers
- **Empowerment from pixels.** E(s) = max_ω I^ω(a, s′ | s) over K-step action sequences (Eq. 2). Bound (Barber & Agakov): I ≥ H(a | s) + E[log q_ξ(a | s′, s)] (Eq. 4); the transition model appears only linearly, so the bound is estimated from interaction samples without a world model.
- **Algorithm.** Alternate (i) a maximum-likelihood **decoder** q_ξ(a | s, s′) (an inverse model over action sequences, autoregressive) and (ii) a **source** ω*(a | s) ∝ exp(β E[ln q_ξ(a | s, s′)]), approximated by a normalised h_θ plus a scalar ψ_θ(s) with E(s) ≈ ψ_θ(s)/β, trained by squared error (Eq. 8). An entropy constraint on H(a | s) avoids divergence (Eq. 5). Behaviour: greedy one-step maximisation of expected empowerment (K = 5).
- **Agreement with exact values:** on environments with ≤ 400 states, heat maps match Blahut–Arimoto; for two rooms, correlation 1.00, R² = 0.90.
- **Emergent behaviour without reward:** maximum empowerment at room centres and doors; near movable boxes (tools); before a key is taken the maximum is near the key, after it near the door; the agent builds a brick wall to stem lava; in a 3-D predator–prey simulation "the maximum empowerment lies in regions away from the predator, which results in the agent learning to escape".
- **Complexity:** O(D²P + LP²) for representations plus O(H²KN) for the autoregressive models, against O(N^K D⁴) for Blahut–Arimoto on grids.

## What it means for the engine
1. **An inverse model is the estimator.** The bound is tight when q(a | s′, s) recovers which actions produced the outcome. That is the same object as the agent's own inverse body model (brief S4): own-body empowerment can be estimated by how well the agent can tell, from its own body's later state, what it did.
2. **Another agent as an option-restricter emerges as aversive without labels.** The predator result is the clearest case read so far of an avoidance tendency toward another agent arising from an objective about one's own options, not from a label. In a dyad the same objective would push away from a partner who restricts the agent's own action → own-sensor channel, and toward one who widens it.
3. **Approval route.** Which sensors define s′ decides it (see salge-glackin-polani-2014). With the partner's face in s′, the decoder learns to read the agent's actions off the partner's face, and the source learns to act so the partner's face reveals its actions: a contingency-maximising, attention-seeking drive. With own body only in s′, the route is closed except through contexts.
4. **Not satiable.** As in all empowerment work, the value is climbed, not satiated.

## Verdict
- **background (scalable estimator; option-restriction as emergent aversion).** Method material for Candidate 2 of the pass-7 synthesis, not a core.
