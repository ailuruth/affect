# Quantifying causal influences (Janzing, Balduzzi, Grosse-Wentrup & Schölkopf)

Dominik Janzing, David Balduzzi, Moritz Grosse-Wentrup & Bernhard Schölkopf, *Annals of Statistics* 41(5):2324–2358, 2013, doi:10.1214/13-AOS1145 (arXiv:1203.6502v2).

## What was read
The full arXiv v2 (the AoS reprint, about 14,300 words). Read: §§1–8 and Appendices A.1–A.4, including the proofs of Theorems 2, 4 and 5 and the controllability appendix. The online supplement (permutation copies, an alternative measure, total influence) was not read. Ay & Polani 2008, which the paper discusses at length, could not be fetched from this session (santafe.edu blocked, other mirrors unreachable). It is cited here only as Janzing et al. describe it.

## The computation, precisely

**Postulates for the strength C_S of a set of arrows S in a causal DAG:**
- P0 (C_S = 0 ⇒ Markov w.r.t. the graph without S);
- P1 (for X → Y alone, C = I(X; Y));
- P2 locality (only P(Y|PA_Y) and P(PA_Y) matter);
- P3 (C_{X→Y} ≥ I(X; Y | PA_Y∖X));
- P4 heredity.

**Definition: cut the wire and feed it noise of the right marginal.** Delete X → Y by feeding Y's mechanism an independent copy X′ ~ P(X):

  P_S(x_j | pa_j^S̄) = Σ_{pa_j^S} P(x_j | pa_j^S̄, pa_j^S) Π P(pa_j^S),  and  C_S = D(P ‖ P_S).

For a set of arrows, each open end gets an *independent* marginal, not the joint ("each channel is cut by an independent attacker"). Keeping the dependence between open ends breaks Markovianity (Remark 1).

**Key results.**
- Theorem 2: C_S = O_S + (nonnegative term). Causal influence majorises the observed influence D(P ‖ P̃_S).
- Theorem 4: C_{X→Y} = I(X; Y | Z) + D[P(Y|Z) ‖ P_{X→Y}(Y|Z)]; the second term vanishes when X ⊥ Z. "Conditional mutual information underestimates causal strength."
- Theorem 5: additivity over targets, locality, monotonicity for independent sources, heredity. General additivity fails:
  - error-correcting repetition code: cutting ≤ k of the 2k+1 arrows has zero effect, so the measure is not subadditive;
  - XOR with X = Z: each single arrow and the pair each carry 1 bit, so it is not superadditive;
  - broadcasting to n copies: n bits.
- **Gaussian case (Example 8):** with only one parent, C_{X1→X2} = −½ log(1 − r²), where r² = α²Var(X1)/Var(X2).
- **Time series:** TE fails on Ay & Polani's mutual copy loop (0 bits where 1 is right). Under noise ε, TE → 0 while C → 1 bit.
- The authors note the noiseless copy loop "is impossible to distinguish ... from a model without interaction ... where X_{t+1} is obtained from X_t by inversion", whatever is observed.
- Appendix A.4: C equals the controllability repertoire minus the uncontrollable variability, H(Y|Z) − H(Y|X, Z).

## What it means for the designs

1. **The best-axiomatised strength measure is sign-blind by construction.** In the Gaussian case C depends on α² only, so a gain of +α (copy) and −α (anti-copy) have equal causal strength. Every postulate is stated in terms of KL divergence or mutual information, so no measure satisfying P1 can be signed. "How much influence" in the strict causal sense has no direction. Direction must be a second, separate quantity.
2. **Wire-cutting is the right intervention for our audits.** The P_S construction (feed the partner→face route an independent sample of the partner's own marginal) is exactly a replay or shuffled-partner surrogate. It is the operational version of the "same agent, different exchange" surrogate in non-copying-dynamics-synthesis C1. It also gives a principled way to measure *each route's* contribution to copying, provided the copy *direction* is scored by a signed statistic on P versus P_S. For example, ΔSpearman(partner_k, agent_k) between the intact and cut systems is a direct "how much of the copy direction does this route cause" number.
3. **Non-additivity is the formal reason indirect routes keep winning.** The repetition-code example shows that k parallel routes can each have zero individual effect while the set carries the full bit. A per-route cap, which is what most designs impose, cannot bound the set. The bound must be on all arrows into the face at once. That is the whole-loop certificate argument of whole-loop-bounds-synthesis, now with an information-theoretic counterexample.
4. **Copy loops can be unidentifiable from inside.** With noiseless mutual copying, partner-driven and self-driven dynamics produce the same joint law. An agent cannot tell, from statistics alone, whether its face is copying the partner or the pair is following a shared inertial pattern. This supports the self-other synthesis requirement that the agent's own output be aperiodic or perturbed (Lanillos), so that attribution stays identifiable.

## Verdict
**Adopt the intervention, not the scalar.** "Cut each arrow and feed it its own marginal" is the right surrogate for measuring how much copying each route causes. Theorem 5's counterexamples are the cleanest proof that per-route caps cannot bound the whole. The strength C itself is symmetric in sign and cannot carry the copy-direction constraint.
