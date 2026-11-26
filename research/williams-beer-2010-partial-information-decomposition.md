# Nonnegative decomposition of multivariate information (Williams & Beer)

Paul L. Williams & Randall D. Beer, arXiv:1004.2515v1 [cs.IT], 14 Apr 2010. Unpublished preprint; the founding paper of partial information decomposition (PID).

## What was read
The full arXiv v1 (about 8,400 words): every section, Appendices A–E (specific-information measures, lattice definitions, the redundancy lattice, all proofs of Theorems 1–5) and the figure captions. Figures were not seen as images; the worked examples were read from the text.

## The computation, precisely

**Setting.** A target S and sources R = {R1, …, R_{n−1}}. The aim is to split I(S; R) into parts contributed "individually or jointly by various subsets of R".

**Three kinds of information** in the two-source case:
- unique: "R1 may provide information that R2 does not";
- redundant: R1 and R2 "provide the same or overlapping information";
- synergistic: "the combination of R1 and R2 may provide information that is not available from either alone". Canonical example: S = R1 ⊕ R2, where each source alone gives 0 bits and together they give 1.

**Redundancy measure.** The specific information about one outcome is

  I(S = s; A) = Σ_a p(a|s) [log 1/p(s) − log 1/p(s|a)],

that is, "the average reduction in surprise of s given knowledge of A". It equals D(p(a|s) ‖ p(a)) ≥ 0 (Theorem 1). Redundancy is the expected minimum over sources:

  I_min(S; {A1, …, Ak}) = Σ_s p(s) min_i I(S = s; A_i).

The point of the minimum per outcome is that two sources "might provide the same average amount of information, while also providing information about different outcomes of S".

**Lattice and atoms.** The collections of sources in which no source contains another (the antichains, counted by Dedekind numbers: 1, 4, 18, 166, 7579, …) are ordered by α ≼ β ⇔ every B ∈ β contains some A ∈ α. The partial-information atoms Π_R are the Möbius inverse of I_min on this lattice. In closed form:

  Π_R(S; α) = I_min(S; α) − Σ_s p(s) max_{β∈α⁻} min_{B∈β} I(S = s; B).

Theorem 5: every atom is ≥ 0. For two sources:

  I(S; R1, R2) = Π{1} + Π{2} + Π{1}{2} + Π{12}

(unique 1, unique 2, redundancy, synergy).

**Why interaction information goes negative.** I(S; R1; R2) = Π{12} − Π{1}{2}, synergy minus redundancy. A system with both can score zero (Fig. 4B: ½ bit of each). For four variables, 3-parity (pure synergy) and three copies of S (pure redundancy) both give +1 bit: the measure "fails to distinguish between the polar opposites of purely synergistic and purely redundant information".

**Asymmetry.** "Unlike mutual information or interaction information, partial information is not symmetric": the synergy that R1 and R2 give about S differs in general from the synergy that S and R2 give about R1. The decomposition is always about a chosen target.

## What it means for the designs

1. **PID is as sign-blind as mutual information, and this is structural.** Every quantity in the paper is built from specific informations, which are KL divergences between conditional and marginal laws. KL is unchanged by any relabelling (bijection) of an alphabet. So "agent copies partner" (A = P) and "agent does the opposite" (A = ¬P, or A = −P on a continuous channel) give identical atoms. I checked this (`foundations/sims/directional-influence/checks.py`, D1): with target a_t and sources (p_{t−1}, a_{t−1}), copy and anti-copy both give unique_partner = 1.000 bit and every other atom 0, while Spearman's ρ is +1.000 and −1.000. **No PID atom can be the per-expression copy constraint.** Copying is not a region of the PI diagram.
2. **What PID does separate is how the partner's information is used.** A copy and an anti-copy are both pure *unique* information from the partner. A response that depends on the partner only jointly with the agent's own state (XOR-like: "do whatever does not repeat what we just did") is pure *synergy*. In D1, a_t = p_{t−1} ⊕ a_{t−1} gives synergy 1.000, unique 0, TE 1.000 and ρ ≈ 0. This is the information-theoretic form of contingent-but-not-copying. It is also exactly the case where per-channel transfer entropy cannot attribute the bit (james-barnett-crutchfield-2016).
3. **A constraint of the type "partner-unique information about my face ≤ ε, synergy free"** would forbid copy and anti-copy equally. It would allow only responses that need the agent's own state to decode. That is too strong for Principle 3 (the fast matching route is unique information) and for the human sign flips (a plain inversion is also unique). It is a candidate only for the slow, pattern-avoiding component (C7 in non-copying-dynamics-synthesis), not for the per-expression rule.
4. **I_min itself is not usable.** Bertschinger et al. 2014 (bertschinger-2014-unique-information.md) and Harder et al. (cited there) show I_min is "unreasonably large" in some cases. It also cannot be computed in closed form for continuous channels. Any design that uses PID should use a bivariate measure with an operational meaning, and only with two or three sources (the lattice has 18 atoms at three sources and 166 at four).

## Verdict
**Adopt the vocabulary, reject as a constraint.** Unique, redundant and synergistic information is the right language for *how* the partner's signal is used. It cannot say *which way* the agent moves, so it cannot carry the copy-direction prohibition. Its value for the designs is the evaluation split: a human-like agent should show partner information that is largely synergistic with its own state at slow time scales. The per-expression sign constraint has to come from an order-sensitive object (see puccetti-wang-2015-extremal-dependence.md).
