# RNNs of RNNs: recursive construction of stable assemblies of recurrent neural networks (Kozachkov, Ennis & Slotine)

Leo Kozachkov, Michaela Ennis & Jean-Jacques Slotine, *NeurIPS 2022*; arXiv:2106.08928v6 (29 Jan 2023), main text 10 pp. plus long appendix.

## What was read
arXiv v6, extracted text: §1–5 **in full** (the network-of-networks model, the negative-feedback parameterisation (3), Theorems 1–7, §3.1 on Jacobian eigenvalues, §4 experiments with Table 1 and the controls, discussion); appendix A (the combination primitives) and B (limitations) read; appendix C proofs and D (extra experiments) not read.

## The computation, precisely
**Model.** Wilson–Cowan rate RNNs τẋ_i = −x_i + W_iφ(x_i) + Σ_j L_ij x_j + u_i(t), φ monotone with 0 ≤ φ′ ≤ g. Each module i contracts in a constant metric M_i.

**Two combination primitives.**
- **Negative feedback** (eq. 3): L_ij = B_ij − M_i⁻¹B_jiᵀM_j for free B_ij. Then M_iL_ij = −L_jiᵀM_j (skew-symmetric in the joint metric), the coupling cancels in the symmetric part of the Jacobian, and the assembly contracts for every B. B is trained freely by backpropagation.
- **Hierarchy** (appendix A): ẋ = f(x, t), ẏ = g(y, t) + h(x, t) with h of bounded Jacobian is contracting (Lohmiller & Slotine 1998), recursively to any depth; hierarchical connections may be nonlinear.

**Module conditions (Theorems 1–5).** |W|-restricted (P(g|W| − I) + (·)ᵀP ≺ 0), symmetric (W = Wᵀ, gW ≺ I), W = −P₁QP₂ with Q ≻ 0 (easy to parameterise), triangular gW − I Hurwitz, and singular-value restricted g²WᵀPW − P ≺ 0 (the discrete-time echo-state condition, generalised). Theorem 7: diagonal stability of the symmetric part does not imply contraction in any constant metric (2 × 2 counterexample with strong antisymmetry). §3.1: negative real parts of the Jacobian's eigenvalues do not imply stability.

## Evidence with numbers
- Sparse Combo Net (16 × 32 modules, 3.3 % sparse fixed modules, trained feedback only): best permuted sequential MNIST 96.94 % (4 trials 96.65–96.94 %), sequential CIFAR-10 65.72 % (10 trials 63.73–65.72 %), with 130 K parameters; previously reported best stable RNN 64.2 % (Lipschitz RNN). Unstable baselines reach more (S4 91.13 % on sequential CIFAR-10).
- Removing the stability constraint on the inter-module matrix (L = B free) dropped permuted sequential MNIST from 96.7 % to 47.0 %.
- One module → two modules: 37.1 % → 89.1 % (Sparse Combo), 61.8 % → 92.9 % (SVD Combo).

## What it means for the designs
1. **A certified route can be built from per-channel modules.** Hierarchy preserves contraction: a contracting trunk feeding per-channel contracting modules is contracting, and the per-module gains multiply along the hierarchy (my reading, by the same argument). That is the structural way to give each expression channel its own certified module under a shared one.
2. **Feedback between modules is safe only in the skew form** for contraction; for gain bounds the corresponding tool is the neutral interconnection of dissipative blocks (scherer-2022-dissipativity-iqc.md). The paper does not bound input–output gain.
3. **Constant metrics.** The authors list as a limitation that only constant metrics are used; state- or time-dependent metrics are left open. That matters for learning that changes weights during a session: a switch between two contracting weight settings with different metrics is not covered.
4. **Stability and accuracy are not opposed here**: on these benchmarks the constraint helped (96.7 % vs 47.0 %).

## Verdict
**adopt (as the modular construction rule: certified trunk plus per-channel modules by hierarchy; skew-form feedback).** No input–output bound; contraction only.
