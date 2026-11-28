# Direct parameterization of Lipschitz-bounded deep networks: the sandwich layer (Wang & Manchester)

Ruigang Wang & Ian R. Manchester, *Proceedings of the 40th International Conference on Machine Learning (ICML)*, PMLR 202, 2023; arXiv:2301.11526v3 (6 Jun 2023). Code cited (github, LBDN; partly in RobustNeuralNetworks.jl); not inspected.

## What was read
arXiv v3, extracted text: §1–5 **in full** (problem set-up, the LipSDP-Neuron LMI (4)–(5), the direct parameterisation (6)–(8), Theorems 3.1–3.2, Proposition 3.3, the convolution algorithm, the comparison with prior 1-Lipschitz layers, the toy example with Table 1 and Figs. 3–4, the image-classification results including Table 2). **Not read:** the appendices (proofs, the Fourier-domain details, training settings).

## The computation, precisely
**Target.** A feedforward network z₀ = x, z_{k+1} = σ(W_kz_k + b_k), y = W_Lz_L + b_L (σ slope-restricted in [0, 1]) with Lip(f) ≤ γ, certified by the LipSDP-Neuron LMI with **diagonal** Λ (Remark 2.2 repeats that the coupled-multiplier version of Fazlyab et al. is false).

**Direct parameterisation.** Write the LMI matrix as H = PPᵀ with a block-bidiagonal P whose diagonal blocks give positive diagonal H_kk. This is achieved with the Cayley transform: [A_kᵀ; B_kᵀ] = Cayley([X_k; Y_k]) (orthogonal columns), Ψ_k = diag(e^{d_k}), then

  W_k = 2Ψ_k⁻¹B_kA_{k−1}ᵀΨ_{k−1},  with A₋₁ = I, Ψ₋₁ = √(γ/2) I, Ψ_L = √(2/γ) I.

Free parameters θ = {X_k, Y_k, b_k, d_k} ∈ ℝ^N; parameters are shared between neighbouring layers.

**Theorem 3.1 (complete).** The network satisfies the LMI (5) if and only if its weights can be written as (8). **Theorem 3.2.** The *sandwich layer* h_out = √2 AᵀΨ σ(√2 Ψ⁻¹B h_in + b) is 1-Lipschitz; a γ-Lipschitz network is h₀ = √γ x, a stack of sandwich layers, y = √γ B_L h_L + b_L. **Proposition 3.3.** A linear layer is 1-Lipschitz iff W = 2AᵀB with A, B from (7) (so the class contains every 1-Lipschitz linear map).

**Why it is tighter than products.** Individual layers may have spectral norm > 1 while the network is 1-Lipschitz; in the toy example the product of layer spectral norms is 65.9 for a network certified at 10.

## Evidence with numbers
- **Tightness (Table 1; square-wave fit, γ̲/γ̄ in %):** at γ = 1 / 5 / 10: AOL 77.2 / 45.2 / 47.9; orthogonal 74.1 / 72.8 / 64.5; SLL 99.9 / 90.5 / 67.9; sandwich 99.9 / 99.3 / 94.0. Fitted slopes at the discontinuity with γ = 10: AOL 4.8, orthogonal 6.5, SLL 6.8, sandwich 9.4 (best possible 10).
- **CIFAR-100 (Table 2, certified bound 2):** clean / AutoAttack ε = 36/255 accuracy for sandwich small 54.2 / 44.3 % (3 M parameters, 19 s per epoch) against SLL small 52.9 / 41.9 % (41 M, 29 s); sandwich large 57.5 / 48.5 % (48 M).
- Per-layer bounds are tight for AOL, orthogonal and sandwich layers (≥ 99.1 %); the whole-network gap is what differs.

## What it means for the designs
1. **Per-channel nonlinear readouts with a ceiling, learned freely.** A sandwich network φ_k scaled to γ_k is any learned, nonlinear map whose sensitivity to its input never exceeds γ_k, for every value of the free parameters. Placed after a certified recurrent trunk, it lets a channel's response to the trunk change shape, sign and context while its gain stays under the share of c_k assigned to it (my use; the composition rule is Lip(φ ∘ h) ≤ Lip(φ)·Lip(h)).
2. **Little budget is wasted.** At small γ the certified bound is attained to 94–99.9 % on the toy task, so a ceiling share given to a learned readout is close to the gain it can actually use. This matters for small-ceiling channels.
3. **Static only.** Memory must come from the trunk (a REN); this paper bounds memoryless maps.

## Verdict
**adopt (the direct parameterisation for the static, per-channel parts of a certified route: complete, tight, cheap).**
