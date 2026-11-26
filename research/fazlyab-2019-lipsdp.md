# Efficient and accurate estimation of Lipschitz constants for deep neural networks (Fazlyab et al.)

Mahyar Fazlyab, Alexander Robey, Hamed Hassani, Manfred Morari & George J. Pappas, *NeurIPS 2019*; arXiv:1906.04893v2 (14 Jan 2023), 17 pp.

## What was read
arXiv v2, extracted text:
- **Read in full:** the abstract, §1 (contributions, related work, motivating applications), §2 (problem statement, Definitions 1–2, Lemma 1, Theorems 1–2, Remark 1, §2.5 variants and splitting), §3 (experiments, Tables 1–2, figure captions) and §4 (conclusions).
- **Not read:** the appendix (proofs, the repeated-nonlinearity constraints of A.8, Proposition 1).
- v2 lists two variants (LipSDP-Neuron, LipSDP-Layer). I did not read v1 and do not know what else it contained.

## The computation, precisely

**Activation as a quadratic constraint.**
- **Definition 1:** φ is slope-restricted on [α, β] if α ≤ (φ(y) − φ(x))/(y − x) ≤ β. ReLU, tanh and sigmoid are slope-restricted on [0, 1].
- **Lemma 1:** for any diagonal T = Σ_i λ_ii e_ie_iᵀ with λ_ii ≥ 0,

  [x−y; φ(x)−φ(y)]ᵀ [[−2αβT, (α+β)T],[(α+β)T, −2T]] [x−y; φ(x)−φ(y)] ≥ 0 for all x, y.

  This is an *incremental* quadratic constraint (Definition 2) on the whole layer.

**Theorem 1 (one hidden layer).** For f(x) = W¹φ(W⁰x + b⁰) + b¹, if for some ρ > 0 and T ∈ 𝒯_n

  M(ρ,T) = [[−2αβW⁰ᵀTW⁰ − ρI, (α+β)W⁰ᵀT],[(α+β)TW⁰, −2T + W¹ᵀW¹]] ⪯ 0,

then ‖f(x) − f(y)‖₂ ≤ √ρ‖x − y‖₂. Minimising ρ over (ρ, T) is an SDP.

**Theorem 2 (ℓ layers).** Stack all layers as Bx = φ(Ax + b), f = Cx + b_ℓ (eq. 12–13) and impose one LMI (14) of the same form. **One** certificate covers the whole network jointly. It is not the product of per-layer norms.

**Variants.**
- LipSDP-Neuron: one multiplier per neuron, n + 1 variables.
- LipSDP-Layer: one per layer, ℓ + 1 variables.
- Splitting into sub-networks and multiplying their bounds is allowed for scale, and returns to product-type looseness at the split points.

## Evidence with numbers
- **The naive bounds:**
  - upper: Π‖W^i‖₂ (product of per-layer spectral norms);
  - lower: ‖W^ℓ⋯W⁰‖₂.
  - On five-hidden-layer MNIST nets (test accuracy > 97%), LipSDP-Neuron is tighter than CPLip and SeqLip, and "the true Lipschitz constants … are very close to the naive lower bound". The per-layer product overestimates heavily (Fig. 2a; values not tabulated in the text).
- **Run time** (MATLAB/CVX/MOSEK, 9-core CPU, 16 GB RAM):
  - one hidden layer, n = 500 → 3000 neurons: Neuron 5.2 s → 735 s; Layer 2.9 s → 473 s (Table 1);
  - 5 → 500 layers of 100 units, split into 5-layer pieces: Neuron 20 s → 708 s; Layer 3.4 s → 216 s (Table 2);
  - 50,000 neurons: about 12 min (Neuron), 4 min (Layer).
- **Robust training** (LP-Train, PGD-Train) gives markedly lower certified Lipschitz bounds than Adam. Accuracy drops coincide with drops in the Lipschitz constant (Fig. 4). Leaky ReLU nets had larger constants than ReLU nets of the same topology (Fig. 5).

## What it means for the designs
1. **Per-route caps compose as a product; a joint certificate does not.** This is the paper's headline in network form. Bounding each layer (each route) separately and multiplying gives a bound far above the truth, because it ignores how the routes interact. That is the mirror image of the designs' failure: they bounded routes separately, and the *sum* of routes (critique 3's relief smile, own-part path and nightly residual) went over the claimed ceiling because the routes were not counted together. A joint LMI over the stacked system counts every route and its interactions once. **The lesson: state the ceiling on the stacked map (all routes as one implicit layer), never as a product or sum of per-route caps.**
2. **Learned modules need slope descriptions, not value clips.** Lemma 1 abstracts each nonlinearity by its slope sector. Critique 3's T8 error was a clip on *value* treated as a bound on *slope*. Any gate, clip or saturation in a design should be written in this incremental-quadratic form before a ceiling is claimed.
3. **A checker the critic can run.** For a feedforward partner→face read-out (no recurrence), LipSDP gives a certified upper bound on the whole read-out's gain in minutes on a CPU. Per-channel ceilings follow by computing it for each output row (f_i = e_iᵀf), which is just a choice of C. It could be added to sims/ checks for any design with a learned read-out.
4. **Where it falls short.**
   - *Analysis after training*, not a guarantee during learning. The certificate holds for the weights it was computed on; after the next learning step it must be recomputed. That is a per-version check, not an innate ceiling. revay-2023-recurrent-equilibrium-networks.md turns the same LMI into a parameterization that cannot be violated.
   - Feedforward only: no recurrence, so no loops. Loops need the dynamic version (REN, or the IQC theorems in scherer-2022-dissipativity-iqc.md).
   - It is an existing analysis tool and does not touch copy-attractiveness (no dynamics).

## Verdict
**watch (as the static special case and a practical checker).** The method and its lesson matter: per-route products are loose and route sums leak, so certify the stacked map jointly. Use the dynamic, learning-proof version (REN) for the core.
