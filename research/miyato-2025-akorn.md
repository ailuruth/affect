# Miyato, Löwe, Geiger & Welling 2025: Artificial Kuramoto Oscillatory Neurons (AKOrN)

Citation: T. Miyato, S. Löwe, A. Geiger, M. Welling. "Artificial Kuramoto Oscillatory Neurons." ICLR 2025. arXiv:2410.13821v3 (16 May 2025). Code: github.com/autonomousvision/akorn.

Source read: the arXiv v3 PDF via text extraction. Main text read in full (sections 1-7, Eqs. 1-9, Tables 1-4). Appendix read: A.1-A.5 (projection operator, the ablation replacing the Kuramoto update with a residual update, number of rotating dimensions N, the C and m ablation, run time), B.1 (relation to physics), and D.4 (symmetric constraint). Not read: C (experimental settings beyond the first table), D.1-D.3, D.5, E, and the Lyapunov proofs F-G. The cited non-reciprocal phase-transition paper (Fruchart et al. 2021) was not read.

## The failure or bottleneck it answered
- The motivation is binding: "neurons representing features such as square, blue, and toy are bound by synchronization to represent a square blue toy". Earlier synchrony models (complex-valued autoencoders, Rotating Features) "are shown to work well on relatively synthetic data but have been struggling to scale to natural images", and slot-based models "struggle on natural images and are therefore often combined with powerful, pre-trained SSL models such as DINO".
- The paper does not start from one measured bottleneck; it argues from neuroscience and then measures gains on four task families.
- Measured results:
  - Object discovery, CLEVRTex FG-ARI 88.5 ± 0.9 (from scratch; ISA-TS 92.9 is higher); on the OOD variant 87.7 ± 0.3, the best in Table 1. "Among the distributed representation models, AKOrN is the first method that is shown to be competitive with slot-based models on the complex CLEVRTex dataset."
  - Sudoku OOD board accuracy 89.5 ± 2.5, against 5.2 ± 0.2 for a Transformer and 34.4 ± 5.4 for the weight-tied iterative self-attention baseline (ItrSA), with 128 test-time steps and energy-based voting over 4,096 random initial states.
- Ablations that bear on "what is the new part": removing projection and normalization, which turns the update into an ordinary residual update, drops Sudoku ID from 100.0 ± 0.0 to 59.8 ± 54.6 and OOD from 51.7 ± 3.3 to 17.1 ± 16.6 (Table 6). Using N = 2 (the classical phase oscillator) instead of N = 4 drops Sudoku ID to 0.3 ± 0.4 and CLEVRTex FG-ARI to 44.6 ± 2.5 (Table 7). Symmetrized J "underfit[s] the data" (D.4).

## The new computation, in one equation
Each unit is a unit vector x_i ∈ S^{N−1}, updated by a generalized Kuramoto flow with a stimulus field (Eq. 2):

  ẋ_i = Ω_i x_i + Proj_{x_i}( c_i + Σ_j J_ij x_j ),  Proj_x(y) = y − ⟨y, x⟩ x,

discretized as x_i ← (x_i + γ Δx_i)/‖x_i + γ Δx_i‖, with the next layer reading C' = g(‖Σ_i U_ki x_i‖).

What is computed is a **relational code**: the information that the next layer reads is which units have come to point the same way, because the readout takes a norm and is invariant to a global rotation ("patterns after certain Kuramoto steps only differ in global phase shifts"). A unit's magnitude carries nothing (it is fixed at 1); binding is the computation. With symmetric J and Ω the flow descends the energy E = −½ Σ x_iᵀ J_ij x_j − Σ c_iᵀ x_i (Eq. 3), and the paper uses that energy at test time to select among random restarts.

## New computation or recombination?
Parts, each with its prior:
1. Kuramoto phase oscillators (Kuramoto 1984), Eq. 1.
2. The vector (N-dimensional) Kuramoto model on the sphere: Olfati-Saber 2006, Chandra, Girvan & Ott 2019 and others, all cited; A.1 says its reduction to Eq. 1 "is just a rephrased version of Chandra et al. (2019)".
3. The stimulus field c_i: the external field of a Heisenberg (classical spin) model, "akin to a magnetic field interaction" (B.1).
4. The energy, Eq. 3: the Heisenberg / Hopfield-type quadratic energy; the paper says the symmetric model "can also be studied by viewing it as ... the Heisenberg model".
5. Tangent projection plus renormalization: Riemannian gradient steps on the sphere.
6. Connectivity: convolution or QKV attention (Bahdanau 2014; Vaswani 2017), Eqs. 7-9.
7. Readout by norms of linear combinations: the magnitude readout used in complex-valued and Rotating-Features models (Löwe et al. 2022, 2023), on which the second author worked.
8. Weight-tied iterative blocks (Bansal et al. 2022, cited).
9. Asymmetric J and heterogeneous Ω_i: non-reciprocal coupling, studied in active matter (Fruchart et al. 2021, cited, not read).

By the project's test this is a **recombination**: every term exists in physics or in prior binding models, and the paper presents itself as "firmly grounded in well-understood physics models". The operator's excluded list already names oscillators. What is new is empirical: the N ≥ 4 sphere with a field and non-reciprocal learned coupling, placed as the unit of a deep network, scales to natural images and gives an energy usable for test-time search. The Table 6 and 7 ablations show that the change of state space (unit vectors, N ≥ 4) is what matters, not the label "oscillator".

## What it suggests for an affective core
- **Does AKOrN have the single dial?** In the classical model with all-to-all J_ij = K/N there is one gain, K, with a critical value that runs from incoherence to full synchrony. AKOrN has no exposed scalar of this kind: J is a full learned matrix, Ω_i per unit, c_i per unit, and only the step size γ is a learned scalar. But two dials remain implicit:
  - **The overall scale of J against Ω and c.** Multiplying J by λ takes any positively coupled connected group from free rotation to alignment. This is the v2-coupled-dynamics critique's excitability dial in another form.
  - **The field c against J.** Fig. 10: "The oscillators on the white region of C are aligned with the conditional stimuli and almost stay constant across time. The oscillators on the black region are largely influenced by the neighboring oscillators". If the partner's features enter as c, the ratio ‖c‖/‖J‖ runs the agent from internally organized waves (partner ignored) to pinned to the partner (copy). That is the flat-to-copy dial again. So the partner must not enter as the field.
- **A structural route the paper opens: non-reciprocal coupling.** The authors found asymmetric J better than symmetric J and point to non-reciprocal phase transitions. In two non-reciprocally coupled populations (self and partner representation), the coupling has a symmetric part (align or anti-align) and an antisymmetric part (one chases the other). The phase diagram then has more than two regimes: incoherent, aligned, anti-aligned, and a "chasing" regime with a persistent rotating phase lag (this last claim is from the cited physics, not verified here). In such a regime the agent neither copies nor ignores the partner; the dyadic state is a *relation* (a lag and direction of rotation). Partner influence is then at least two-dimensional (symmetric and antisymmetric parts of a block of J), and the relation, not the agent's content, is what changes with the situation. This is a direction to test, not a result.
- **The relational readout** is the most transferable idea: what the core expresses could be a function of which of its own units have bound together, invariant to a common rotation. If the partner can only rotate everything together, a phase-invariant readout makes that rotation invisible in expression. The partner then influences expression only by changing *which units cohere*, which is a change of profile, not of gain.
- **Limits the authors state.** "each single oscillator cannot represent the 'presence' of the features ... AKOrN would not perform well on memory tasks, where the model needs to remember the presence of events." A mood that persists across minutes needs exactly what the unit-norm constraint removes; any use here would have to relax the norm (as Rotating Features do with a magnitude).

## Verdict: watch (recombination of Kuramoto, Heisenberg and attention parts; the non-reciprocal coupling and phase-invariant readout are worth a test)
Not a new computation by the project's test, and oscillators are on the excluded list. Two ideas survive: partner influence carried by the antisymmetric (non-reciprocal) part of a coupling, giving a dyadic phase relation that is neither copy nor indifference; and expression read out invariantly to a common rotation, so that the partner can only act by changing which of the agent's units bind. Feeding the partner as the field c recreates the dial and must be avoided.
