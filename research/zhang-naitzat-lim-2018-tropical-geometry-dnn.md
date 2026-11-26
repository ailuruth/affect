# Tropical Geometry of Deep Neural Networks (Zhang, Naitzat & Lim)

Citation: L. Zhang, G. Naitzat, L.-H. Lim. "Tropical Geometry of Deep Neural Networks." ICML 2018 (PMLR 80). arXiv:1805.07091.

Source read: arXiv PDF, text-extracted. Read in full: sections 1–7 (tropical semiring, tropical polynomials and rational functions, tropical hypersurfaces, Newton polygons and dual subdivisions, Minkowski sums and zonotopes, the neural-network assumptions, Proposition 5.1 recursion, Theorems 5.2 and 5.4, Proposition 5.5, decision boundaries, Lemma 6.2, Theorem 6.3 and the conclusion). Not read: the supplement (proofs in section D, worked examples in section C).

## What it shows
- Tropical semiring: x ⊕ y = max{x, y}, x ⊙ y = x + y; no additive inverse. Tropical polynomials are convex piecewise-linear; tropical rational functions f ⊘ g = f − g are difference-of-convex.
- **Theorem 5.4:** a function is a tropical rational function if and only if it is a feedforward ReLU network with integer weights (real weights by approximation and rescaling). Proposition 5.5: equivalently, continuous piecewise-linear with integer coefficients. The authors credit Arora et al. 2018 for the real-weight version.
- One layer: max{Ax + b, t} = max{A⁺x + b, A⁻x + t} − A⁻x — every layer splits into a positive and negative tropical polynomial. The geometry: one-hidden-layer networks are built from zonotopes; linear regions correspond to vertices of upper faces; Theorem 6.3 bounds the number of regions by O(n^{d(L−1)}), which "does not improve on" Raghu et al.

## What it means for the design
1. **A max-plus core is not new as a function class.** Whatever is written in max/plus/minus with integer exponents is a ReLU network. "Tropical dynamics" therefore reduces to a piecewise-linear recurrent network; it cannot by itself clear the novelty test.
2. **What max-plus does give is a language for ceilings and races, not a mechanism.** A ceiling is min(c_k, ·) and "whichever comes first" is max of event times. Per-channel caps written this way are the same clipped units the critiques already found leaking through learned slopes (design-partner-regulator.md, X1).
3. **Max-plus linear algebra of event timing** (eigenvalues as maximum cycle means, which would make rhythms a property of the coupling graph's cycles) is the part that could matter for turn-taking and echo latency. The paper only names it (Butkovič 2010) and I have not read that source, so it stays a lead, not a finding.

## Verdict
- [Tropical geometry of deep neural networks (Zhang, Naitzat & Lim)](zhang-naitzat-lim-2018-tropical-geometry-dnn.md) — 2018 — reject as core — tropical rational maps are exactly integer-weight ReLU networks (Theorem 5.4), so a max-plus core is a ReLU network in other notation; max-plus event-timing algebra (cycle-mean rhythms) is an unread lead.
