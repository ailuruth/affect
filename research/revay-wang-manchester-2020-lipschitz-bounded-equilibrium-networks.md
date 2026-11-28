# Lipschitz-bounded equilibrium networks (Revay, Wang & Manchester)

Max Revay, Ruigang Wang & Ian R. Manchester, arXiv:2010.01732v1 (5 Oct 2020), 8 pp. plus appendices.

## What was read
arXiv v1, extracted text: §1–6 **in full** (introduction, related work, problem statement, preliminaries, Conditions 1–2, Theorems 1–2 with the proof sketch, Remark 3, Example 1, the direct parameterisations (10)–(11), the convex-optimisation and neural-ODE views, Propositions 1–4, experiments and conclusions); appendix A's tables as extracted (their layout was partly garbled; only clearly legible figures are quoted); appendix B skimmed; the other appendices not read.

## The computation, precisely
**Model (eq. 1).** A static (weight-tied) equilibrium network z = σ(Wz + Ux + b_z), y = W_o z + b_y, with σ monotone and slope-restricted in [0, 1] (Assumption 1).

**Conditions.**
- Condition 1 (well-posedness): ∃Λ positive diagonal with 2Λ − ΛW − WᵀΛ ≻ 0.
- Condition 2 (Lipschitz γ): 2Λ − ΛW − WᵀΛ − (1/γ)W_oᵀW_o − (1/γ)ΛUUᵀΛ ≻ 0.

Theorem 2: under Assumption 1 and Condition 2 the network is well posed and ‖y₁ − y₂‖ ≤ γ‖x₁ − x₂‖. Proof sketch: the incremental sector condition ⟨Δv − Δz, Δz⟩_Λ ≥ 0, a Schur complement and left/right multiplication give γ‖Δx‖² − γ⁻¹‖Δy‖² ≥ 2⟨Δv − Δz, Δz⟩_Λ ≥ 0.

**Direct parameterisation (eq. 11).** With free V, d, skew S = −Sᵀ, free U, W_o and Ψ = diag(e^d):

  W = I − Ψ( (1/2γ)W_oᵀW_o + (1/2γ)Ψ⁻¹UUᵀΨ⁻¹ + VᵀV + εI + S ),

which satisfies Condition 2 automatically; the authors state the construction is necessary and sufficient (every W satisfying (4) arises this way). Training is plain unconstrained gradient descent; no projection, no barrier.

**Remark 3 (a correction).** The richer "repeated nonlinearity" multipliers claimed in Fazlyab et al. 2019 are not valid for incremental constraints: increments σ(v_i + Δv_i) − σ(v_i) are not repeated functions of Δv_i, because the base points v_i differ between units. Counterexample in Pauli et al. 2020 (pauli-2021-training-robust-nn-lipschitz.md). Only diagonal Λ is valid.

**Neural-ODE view (Prop. 4).** Under Condition 1 the ODE v̇ = −v + Wσ(v) + Ux + b_z is contracting in a constant metric, "independent of the input x … so extends directly to the case when these are time-varying".

## Evidence with numbers
- MNIST (fully connected): certified upper and adversarial lower Lipschitz bounds are close, "in many cases around 90 %"; the unconstrained equilibrium model's observed Lipschitz constant is "more than an order of magnitude higher" with no gain in test error; LBEN γ = 5 shows a slight regularising effect (higher training error, lower test error).
- Time per epoch: MON 14.4 s, unconstrained 16.1 s, LBEN γ < ∞ 14.9 s, LBEN γ = 5 14.8 s, against a 50-fold increase reported for ADMM-based Lipschitz training (Pauli et al.).
- SVHN (convolutional): a slight drop in clean accuracy for more than a 10-fold reduction of the sensitivity to adversarial attack; one legible row: LBEN γ < 2, certified 2, observed lower bound 0.8 (40 %), looser than MNIST, attributed to a more restrictive multiplier set.

## What it means for the designs
1. **A per-channel readout bound costs nothing at training time.** The construction puts the bound into W through W_o and U. For an engine readout of channel k from a shared trunk, the same form with γ = c_k (or a share of it) bounds that channel's sensitivity to the trunk by construction, whatever the learner does (my use).
2. **Only diagonal multipliers.** Any certificate written for the engine must use diagonal Λ (Remark 3). The repo's LipSDP note (fazlyab-2019-lipsdp.md) should be read with this correction: the coupled-multiplier variant does not give a valid bound.
3. **The bound is close to attained on dense data and loose on convolutional structure**: the share of the ceiling that is wasted depends on the architecture, so the engine should measure the lower bound (adversarial pairs) as a fit-time report, as the paper does.

## Verdict
**adopt (as the static building block: a direct, complete parameterisation of Lipschitz-bounded equilibrium layers, for per-channel readouts).** Static only; the dynamic version is the REN.
