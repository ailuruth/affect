# Deep Sets (Zaheer, Kottur, Ravanbakhsh, Póczos, Salakhutdinov & Smola)

Citation: M. Zaheer, S. Kottur, S. Ravanbakhsh, B. Póczos, R. Salakhutdinov, A. J. Smola. "Deep Sets." NeurIPS 2017. arXiv:1703.06114 (v3, read).

Source read: arXiv PDF, text-extracted. Read in full: abstract, sections 1–4 (problem, structure theorem, permutation-equivariant layer, relations to de Finetti, kernels and spectral methods; experiments on population statistics, digit sums, point clouds, red-shift, set expansion, image tagging, outlier detection), Appendix A (proofs for the countable case, the fixed-size uncountable case via Newton–Girard and the root–coefficient homeomorphism, Theorem 9 via Stone–Weierstrass and symmetric polynomials, worked examples) and Appendix B (proof of Lemma 3). Appendices on experimental details were skimmed.

## The derivation story (method of discovery)
- **Start from the invariance, characterise every function that has it.** Theorem 2: on a countable universe, f(X) is permutation invariant iff f(X) = ρ(Σ_{x∈X} φ(x)). Proof idea: φ(x) = 4^{−c(x)} makes the sum a unique code of the set. For fixed-size subsets of [0,1] the sum-of-powers map is injective (Newton–Girard), giving the same form; for general set sizes on uncountable domains it is only conjectured.
- **Then the layer.** Lemma 3: σ(Θx) is permutation equivariant iff Θ = λI + γ11ᵀ — a necessary and sufficient parameter-sharing pattern, proved by commuting Θ with transpositions.
- **The architecture is read off the theorem**: embed each element, sum, transform. The max-pool variant σ(λx + γ maxpool(x)1) is used in practice.
- Evidence the structure matters: trained on sums of ≤ 10 digits, DeepSets generalise to 100 where LSTM/GRU do not; ModelNet40 90 ± 0.3% from 5,000-point clouds without voxels.
- **Limits stated in the paper:** for uncountable domains the sum form is proved only for fixed set size; DeepSets need more data than kernel methods on small problems (Fig. 1).

## What it means for the design
1. **The method to copy.** State the property the core must have for *every* parameter value, then prove what form a function must take to have it. The form is then the architecture, and no ceiling, penalty or training trick is needed to keep the property. Lemma 3 is the template: a symmetry forces tied weights λI + γ11ᵀ, and that is all a linear layer can be.
2. **Applied to the dyad (open problem, stated not solved).** "The drive on the agent's state is zero for every partner response that is a causal linear filter of the agent's own expression history within delay D." By the projection theorem, a linear functional of the partner path has this property for all such filters iff it depends on the partner path only through its residual after projection onto the span of the agent's own delayed history. This is the negative image of kennedy-sawtell-2014-temporal-basis-negative-images.md, arrived at as a characterisation rather than as a mechanism. The nonlinear case is not characterised.
3. **Sum-decomposition over people.** A state over a set of partners and episodes that must not depend on their order has the ρ(Σφ) form; the brief's "needs over people as a set" is already pinned to this form.

## Verdict
- **adopt (as method).** The architecture itself (permutation invariance) is mostly already in the project's equivariance notes (cohen-welling-2016-group-equivariant-cnn.md); the value is the order of work — property first, characterisation theorem second, architecture last — which is what this search lacks.
