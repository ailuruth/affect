# The signature kernel is the solution of a Goursat PDE (Salvi, Cass, Foster, Lyons & Yang)

Citation: C. Salvi, T. Cass, J. Foster, T. Lyons, W. Yang. "The Signature Kernel is the solution of a Goursat PDE." SIAM J. Mathematics of Data Science 3(3), 2021. arXiv:2006.14794 (v9, 20 Mar 2021).

Source read: arXiv v9 PDF, text-extracted. Read in full: sections 1–3 and 5 (tensor algebra, signature, factorial decay, Definition 2.4, Theorem 2.5 and its proof, the Goursat problem and the finite-difference scheme with its complexity, GPU implementation, UEA classification, Bitcoin regression). Section 4 (rough-path extension) and Appendix B read for statements only.

## What it does
- **Object.** k_{x,y}(s, t) = ⟨S(x)_{[u,s]}, S(y)_{[v,t]}⟩, the inner product of the untruncated signatures of two paths.
- **Theorem 2.5.** For C¹ paths, k solves the linear hyperbolic (Goursat) PDE ∂²k/∂s∂t = ⟨ẋ_s, ẏ_t⟩ k with k(u, ·) = k(·, v) = 1. So the kernel needs only the increments' inner products, no signature computation. An explicit finite-difference scheme costs O(d ℓ²) per pair (ℓ path length, d channels), and parallelises on GPU along anti-diagonals to near-linear time in ℓ. A rough-path version is an analogous rough integral equation.
- **Evidence.** SVC on UEA multivariate datasets: the PDE kernel is among the top two in most datasets and always beats the truncated signature kernel, which often overfits; SVR on daily Bitcoin prices (36-day window, next 2-day mean): best test MAPE among linear, RBF, GAK and truncated-signature kernels.

## What it means for the design
1. **A kernel between the agent's path and the partner's path would compare shapes, not lead–lag.** k(a, x) is symmetric in its two arguments and is maximal for a copy, the opposite of what the design wants; it is not a candidate for the core's partner input.
2. It is the standard nonparametric tool for learning from very few paths (the brief's data scarcity), e.g. for testing on recorded dyads whether expected commutator arrays separate partners, without training the core.

## Verdict
- [Signature kernel as a Goursat PDE (Salvi et al.)](salvi-2021-signature-kernel-goursat.md) — 2021 — watch (tool for small-data comparison of paths) — the untruncated signature kernel solves ∂²k/∂s∂t = ⟨ẋ, ẏ⟩k, computable in O(dℓ²) (near-linear on GPU) and better than the truncated kernel on UEA and Bitcoin; it is symmetric and largest for a copy, so it is no substitute for an antisymmetric lead–lag input.
