# Quantifying unique information (Bertschinger, Rauh, Olbrich, Jost & Ay)

Nils Bertschinger, Johannes Rauh, Eckehard Olbrich, Jürgen Jost & Nihat Ay, arXiv:1311.2852v2 [cs.IT] (16 Jan 2014). Published as *Entropy* 16(4):2161–2183, 2014. Its measure is the "BROJA" PID.

## What was read
The full arXiv v2 (about 10,700 words): the introduction, §2 (operational interpretation), §3 (all properties and proofs), §4 (comparison with I_min and I_red), §5 (examples, the dice system), §6 (outlook) and Appendices A.1–A.3 (the polytope Δ_P, critical equations, the AND example, Example 31 and its figure caption, technical proofs). The published *Entropy* version was not compared.

## The computation, precisely

**The invariance assumption (∗).** Unique and shared information about X should "depend only on the pair marginal distributions of (X, Y) and (X, Z)". The operational reason: Y has unique information about X relative to Z iff there is a decision problem (p, A, u) where an agent observing Y earns a strictly higher expected reward than one observing Z (Definition 1). By Blackwell's theorem this holds unless the channel to Y can be degraded into the channel to Z.

**The definition.** Let Δ_P be the set of joint distributions Q with the same (X, Y) and (X, Z) marginals as P. Then

  ŨI(X : Y∖Z) = min_{Q∈Δ_P} MI_Q(X : Y | Z),
  S̃I(X : Y; Z) = max_{Q∈Δ_P} CoI_Q(X; Y; Z),
  C̃I(X : Y; Z) = MI(X : (Y, Z)) − min_{Q∈Δ_P} MI_Q(X : (Y, Z)).

- Lemma 3: under (∗), these are bounds for *any* nonnegative decomposition (UI ≤ ŨI, SI ≥ S̃I, CI ≥ C̃I). Equality holds iff some Q in Δ_P has zero synergy. This is property (∗∗): "It is not possible to decide whether or not there is synergistic information, when only the marginal distributions of (X, Y) and (X, Z) are known."
- Lemma 4: the problems are convex on a convex set.
- Lemma 6: ŨI(X : Y∖Z) = 0 iff P(x, y) = Σ_z P(x, z) λ(z; y) for some stochastic λ, i.e. Z's channel can be garbled into Y's.

**The polytope.** Δ_P = (P + ker A) ∩ Δ, where A is the linear map to the two pair marginals. ker A is spanned by the moves γ_{x;y,y′;z,z′} = δ_{xyz} + δ_{xy′z′} − δ_{xy′z} − δ_{xyz′}, and has dimension |X|(|Y|−1)(|Z|−1) (Lemma 26). Δ_P is a product over x of fibre polytopes of couplings of P(Y|x) with P(Z|x) (Lemma 27). In words, **the decomposition is an optimisation over couplings with fixed marginals.**

**The sign-blindness in the paper's own figure.** Example 31 takes three i.i.d. fair bits, so Δ_P is a square. The caption of Fig. 2: "In the two dark corners, X is independent of Y and Z, and either Y = Z or Y = ¬Z. In the two light corners, Y and Z are independent, and either X = Y XOR Z or X = ¬(Y XOR Z)." Copy and negated copy are distinct vertices with identical information values.

**Examples (Table 1).** Rdn (X = Y = Z): SI = 1, CI = 0. Unq (X = (Y, Z)): SI = 0, CI = 0. Xor: CI = 1. And: SI = 0.311, CI = ½. Here I_min wrongly gives 1 bit of shared information for Unq. The measure does not extend to three sources on the Williams–Beer lattice, because the identity axiom is incompatible with it (§6). Lemma 25: unique information cannot grow when more variables are conditioned on.

## What it means for the designs

1. **Copying is a vertex of a coupling polytope, and information cannot tell which vertex.** For a binary partner feature P and agent feature A with fixed marginals, the couplings form a segment whose ends are A = P (the comonotone coupling) and A = ¬P (the countermonotone one). MI is the same, maximal, at both ends and zero in the middle. Every information quantity treats the two ends as one point. The direction needs an order on the alphabet, which copula theory supplies (puccetti-wang-2015-extremal-dependence.md): there the ends are the Fréchet–Hoeffding upper and lower bounds.
2. **The operational definition is the useful part for us.** "Unique information" is defined by reward in decision problems. For the agent, "the partner's face gives me information my own state does not" means "some decision goes better if I see the partner's face". It does not mean "my face should look like theirs". This is the right reading of Principle 3 (reading the partner through one's own body). It keeps the *value* of the partner's signal separate from any *resemblance* of the output.
3. **A constraint written as a set of couplings is convex and cheap to state.** Because Δ_P is a polytope, any linear inequality on the joint law (for example, a cap on the probability mass on the diagonal "same expression at the same time", or a copula ceiling) is an intersection with a half-space. It cuts off the copy vertex while keeping the opposite vertex and the interior. The information quantities then become optimisations over the cut polytope, which stay convex. This makes "bound information AND exclude the copy vertex" a well-posed convex object. It is not yet a property the agent's map has *for every partner*. That transfer is the open problem (see the synthesis).
4. **Engineering cost.** The optimum is "very ill-conditioned" even for three bits (Example 31). Mathematica's FindMinimum "does not always find the true optimum out of the box". As a runtime quantity in the agent's loop it is unsuitable; it is an offline evaluation tool.

## Verdict
**Adopt for evaluation, and as the bridge to couplings.** It is the best-motivated bivariate PID, with an operational meaning that matches Principle 3. Its formulation over couplings with fixed marginals is what links information decomposition to the comonotone/countermonotone geometry. It confirms, in the authors' own example, that information measures put copy and anti-copy at the same value.
