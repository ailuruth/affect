# Extremal dependence concepts (Puccetti & Wang)

Giovanni Puccetti & Ruodu Wang, *Statistical Science* 30(4):485–517, 2015 (arXiv:1512.03232v3, with corrections to March 2025). This is an open review of comonotonicity, countermonotonicity and their higher-dimensional substitutes. It stands in for Nelsen's *An Introduction to Copulas*, ch. 2, which is not openly available; it states and proves the same Fréchet–Hoeffding results.

## What was read
The full arXiv v3 (36 pages, about 22,800 words): §1 (rearrangements, Sklar), §2 (comonotonicity, Theorem 2.1, historical remark), §3 (countermonotonicity, pairwise countermonotonicity, joint mixability, the new Σ-countermonotonicity with all proofs), §4 (optimisation over Fréchet classes, the dependence-measure example) and §5 (open questions). Figures were read from their captions.

## The computation, precisely

**Dependence as rearrangement.** Any random vector equals (F_1⁻¹∘f_1(U), …, F_d⁻¹∘f_d(U)) for one U ~ U[0,1] and measure-preserving rearrangements f_j (Theorem 1.1). The copula is the law of (f_1(U), …, f_d(U)). The Fréchet class F(F_1, …, F_d) is all joint laws with the given marginals.

**The two bivariate extremes.**
- **Comonotonic:** all components are increasing functions of one U. The joint law is the upper Fréchet–Hoeffding bound F^∨ = min{F_1(x_1), …, F_d(x_d)}, with copula M(u, v) = min(u, v) (support on the main diagonal). Theorem 2.1: this is equivalent to F ≥ G for every G in the class, and to maximising E c(X) for every supermodular c. It exists and is unique in law in every Fréchet class, in every dimension.
- **Countermonotonic (d = 2):** X_1 = F_1⁻¹(U), X_2 = F_2⁻¹(1 − U). The joint law is max{F_1 + F_2 − 1, 0}, with copula W (the anti-diagonal). It is the minimiser of every supermodular expectation (Theorem 3.1).

Every bivariate law satisfies W ≤ C ≤ M pointwise (3.5).

**Spearman's ρ_S is a function of the copula only**, and "takes value 1 when X1 and X2 are comonotonic and value −1 when they are countermonotonic". Pearson's ρ depends on the marginals, and its extremes can be strictly inside [−1, 1].

**The asymmetry that matters.**
- **Dall'Aglio (1959), quoted in §3.2:** "if U, V, Z are continuous random variables with (U, V) and (V, Z) countermonotonic random vectors, then (U, Z) has to be comonotonic." Countermonotonicity is not closed under composition; comonotonicity is.
- For d > 2 no negative-dependence concept has existence, uniqueness and supermodular minimality together. The lower bound F^∧ is a distribution only when marginals have atoms at their extremes (Proposition 3.2). The substitutes are:
  - joint mixability (the sum is constant a.s.), which minimises E f(ΣX) for convex f but is not always supported;
  - Σ-countermonotonicity (every partial sum is countermonotonic with the rest), which always exists (Theorem 3.7) but has only a local optimality property (Proposition 3.9).
  - Example 3.5: in a 3-normal model one solution is "X2, X3 move together oppositely to X1", so two of the three are comonotone.

**Information versus concordance.** Shuffles of Min (bijective piecewise-continuous rearrangements) are dense in the copulas, so "any pair of independent random variables can be approximated by a sequence of pairs of mutually completely dependent random variables" (Kimeldorf & Sampson 1978). Full determination and near-zero concordance coexist.

## What it means for the designs

1. **Copying has an exact geometric definition, and it is not about information.** On a single expression channel k at lag τ, "the agent copies the partner" (up to any increasing rescaling of amplitude) is exactly the event that the copula of (partner_k(t−τ), agent_k(t)) is M, the top vertex of the coupling set. The opposite is W, the bottom vertex. Mutual information is maximal (infinite in the continuous case) at both. Spearman's ρ_S, Kendall's τ and the copula order are invariant under strictly increasing transforms of each channel. This matters: the agent cannot evade a copula bound by changing its own gain. But they flip under a decreasing transform. **The relevant symmetry group is Sym (any bijection) for information and Inc (increasing bijections) for concordance.** Copying is a statement only an Inc-invariant, Sym-non-invariant object can make. This matches the symmetry synthesis: the copy direction is visible only to an object that is not invariant under the sign character.
2. **A candidate constraint is a one-sided copula ceiling per channel and lag.** For example C_{k,τ} ≤ κM + (1 − κ)Π pointwise, with 0 < κ < 1, where Π is the independence copula. It is linear in C, so it is convex and cuts the coupling polytope (bertschinger-2014). It excludes M and its neighbourhood, contains W and everything below Π, and says nothing about information. Checks (`foundations/sims/directional-influence/checks.py`, D4, κ = 0.5):
   - copy violates it by +0.124 and anti-copy satisfies it (−0.003);
   - reversed-strip shuffles carry 6 bits (64-bin MI) and satisfy it;
   - random-strip shuffles (6 bits, ρ_S ≈ 0) violate it by 0.064 → 0.025 → 0.016 as the strips shrink (m = 4, 16, 64). Their local increasing pieces are small local copies, and the pointwise ceiling catches them weakly.
   - Independent samples sit at +0.001, which is sampling noise.

   So the pointwise ceiling is strict about local copying and lenient about global anti-copying. The scalar version (ρ_S ≤ κ) is the weak extreme: it lets a coupling copy on half the range and invert on the other half.
3. **Dall'Aglio's theorem is the copula form of the recurring indirect-route failure.** Two strong sign flips in series (partner→appraisal inverted, appraisal→face inverted) compose to copying. Check D3: ρ_S = −0.983 and −0.994 per stage give +0.979 end to end. So a per-stage "may flip, may not copy" rule is not closed under products, any more than skew maps were (symmetry-no-copy-synthesis). **The ceiling must hold on the end-to-end partner→face law**, across all routes, as in the whole-loop certificate.
4. **Several channels: no symmetric "most anti" exists.** For three or more expression channels there is no unique, always-existing extremal negative dependence. A design cannot demand "every channel maximally opposite to the partner" as a universal; Σ-countermonotone solutions include pairs moving together. The per-channel ceiling is well defined in any dimension, because M exists and is unique in every Fréchet class. That is one more reason to state the constraint as "not near M on each channel" rather than "near W".
5. **"Less alike than chance at some lags" is negative concordance, not synergy.** Healey's below-chance other-repetition and Hale's below-surrogate coherence are statements that the copula at that lag lies below the surrogate's. That is a sign property, which this framework sees and PID does not. A stable W at all lags is itself copying with a minus sign (non-copying-dynamics-synthesis C2), and by the delay argument it becomes M in the band ω = π/τ (synthesis, D5). The ceiling must therefore hold at all lags, or equivalently on the real part of the cross-spectrum in every band.

## Verdict
**Adopt as the mathematical home of the copy-direction constraint.** Copying is the comonotone vertex M of the per-channel coupling set. A one-sided, Inc-invariant ceiling below M is the simplest object that bounds the copy *direction* while leaving information, sign flips and contingency free. Dall'Aglio's theorem says why it must be imposed end to end.
