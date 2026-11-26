# Dissipativity and integral quadratic constraints: tailored computational robustness tests for complex interconnections (Scherer)

Carsten W. Scherer, *IEEE Control Systems Magazine* 42(3), 2022, doi:10.1109/MCS.2022.3157117; author version arXiv:2105.07401v3 (19 Sep 2023), 47 pp. This note stands in for **Megretski & Rantzer 1997, "System analysis via integral quadratic constraints", IEEE TAC 42(6):819–830**. The 1997 paper could not be reached: the Lund repository copy (lup.lub.lu.se) and the core.ac.uk copy were refused by this session's network. Scherer restates the Megretski–Rantzer theorem exactly as his Theorem 28 and proves that his dissipativity framework contains it. Statements about the 1997 paper below rest only on that restatement.

## What was read
The arXiv author version, as extracted text:
- **Read in full:** the introduction; "Motivation: the Lur'e problem" (Theorem 1, the circle criterion); "Dissipativity" up to Theorem 5; "Robustness analysis with dynamic IQCs" (Corollary 11, Definition 12, Theorems 13–15, Remark 16); "Structured uncertainties" (Lemma 20 and the worked example, eq. 54–55); "Nonlinear uncertainties"; Example 23 with Figures 4–5; the conclusion; the sidebars "The circle criterion: dissipativity proof" (the neutral-interconnection argument, S5–S6) and "Link to classical IQC theorem" (Theorem 28 and the comparison with Definition 12).
- **Skimmed:** the KYP-lemma section (Theorems 4–9, Lemma 8) and the appendix lemmas 31–35.

## The computation, precisely

**Dissipativity (Willems), as used here (Definition 2).** A system ẋ = f(x,u), y = g(x,u) is dissipative with respect to a supply rate s(u,y) if some storage V satisfies

  V(x(t₂)) ≤ V(x(t₁)) + ∫_{t₁}^{t₂} s(u,y) dt  (DI)

for all trajectories. It is *strictly* dissipative if the right-hand side also carries "− ε∫(‖x‖² + ‖u‖²)". "Both dissipation inequalities impose convex constraints on the pair (V, s)."

**The whole-loop argument is one line (sidebar, S5).** Subsystem 1 is dissipative with supply s₁(z,w). Subsystem 2 is strictly dissipative with s₂(u,y). If the interconnection is *neutral*, meaning s₁ + s₂ = 0 on every signal the loop allows, then adding the two inequalities gives

  x(T)ᵀXx(T) + ε∫₀ᵀ(‖x‖² + ‖u‖²) ≤ x(0)ᵀXx(0).

Scherer calls this "a simple version of one of the key results in [Willems 1972], which roughly states that the neutral interconnection of dissipative systems stays dissipative". No route-by-route accounting appears: the inequality holds for every signal path in the loop at once.

**IQCs describe a block by what it cannot do, not by what it is.** The uncertainty Δ may be any set-valued map w ∈ Δ(z) satisfying a *hard IQC*:
- static: ∫₀ᵀ s_P(w,z) dt ≥ 0 for all T ≥ 0;
- dynamic, with a filter Ψ (state ξ) and a terminal cost Z (Definition 12): ∫₀ᵀ vᵀPv dt − ξ(T)ᵀZξ(T) ≥ 0 for all T, where v = Ψ₁z + Ψ₂w.

The set of valid (P, Z) is convex.

**Robust stability (Theorem 13).** If Δ satisfies such an IQC and there are P ∈ 𝒫 and X satisfying the dissipation LMI (36) for the filtered linear part, together with the coupling

  [[X₁ + Z, X₁₂],[X₁₂ᵀ, X₂]] ≻ 0,

then the loop is stable for every Δ in the class. The proof again adds two inequalities.

**Robust performance (Theorem 15).** With exogenous d and error e, the LMI (41) certifies

  x(T)ᵀE(X,Z)x(T) + ∫₀ᵀ s_{P_p}(d,e) dt ≤ x(0)ᵀX₂x(0)

for *all* loop trajectories and *all* Δ in the class. With Q_p = I, S_p = 0, R_p = −γ²I this is "the energy gain of the channel d ↦ e … robustly bounded by γ". This is the form a whole-system partner-to-face ceiling would take: d is the partner channel, e is the agent's face channel, and every internal route is inside the loop.

**Structure (Lemma 20).** If Δ_a and Δ_b satisfy IQCs with (Ψ_a, P_a, Z_a) and (Ψ_b, P_b, Z_b), the block-diagonal Δ = diag(Δ_a, Δ_b) satisfies the IQC with Ψ = diag(Ψ_a, Ψ_b), P = diag(λ_aP_a, λ_bP_b), Z = diag(λ_aZ_a, λ_bZ_b), λ ≥ 0. This is how a network of heterogeneous parts (parameters, saturations, dynamic blocks, a learned module) is certified at once. "This strategy is modular." An incrementally dissipative nonlinear subsystem (eq. 56) satisfies a hard IQC with P = {λP}, so any learned module that carries its own certificate can be dropped in as one block.

**The classical theorem (Theorem 28, Megretski–Rantzer as restated).** Take the loop ẋ = Ax + Bw, z = Cx + Dw, w = Δ(z) + d, with A Hurwitz and Δ causal and bounded. Suppose:
- the loop is well-posed for τΔ, for every τ ∈ [0,1];
- Δ satisfies the frequency-domain IQC ∫[ẑ; τΔ(z)^]^* Ψ^*PΨ [ẑ; τΔ(z)^] dω ≥ 0 for all z ∈ L₂ and all τ;
- the FDI [Ψ₁G + Ψ₂]^* P [Ψ₁G + Ψ₂] ≺ 0 holds on the imaginary axis.

Then the loop is stable. Scherer notes that Theorem 13 needs none of the causality, stability-of-Δ or homotopy (τ) assumptions, and that with a terminal cost it "encompasses the general IQC theorem".

## Evidence with numbers
- **Fig. 4 (saturation in a loop, α ∈ [5, 50]):**
  - Static multipliers give a guaranteed amplitude bound that diverges at a small α.
  - Zames–Falb (dynamic) multipliers with pole a = 10 push the margin much further.
  - With a = 100, the computed bound meets the exact nominal bound: "Zames-Falb multipliers involve no conservatism" there.
- **Fig. 5 (dynamic uncertainty, α ∈ [0.9, 1]):** static multipliers give a looser bound than the new dynamic multipliers with ψ(s) = col(1, (s+0.9)²/(s+1)²). The earlier method of [26] (M ≻ 0, K = 0) is visibly conservative.
- No exact numbers are tabulated; the figures were not seen, only their captions and the text.
- **Tightness claim:** "these robust dissipativity tests are lossless for the so-called small block structures in µ-theory … if only the basis transfer function ψ is chosen sufficiently rich". This covers the structured-singular-value D and D/G scalings as special cases.

## What it means for the designs
1. **This is the missing object: one inequality over all routes.** Every critique found a route that the design's per-route caps missed:
   - the comfort loop whose slope was not bounded (critique 3, T8);
   - the shared variance scale (critique 2, X3);
   - content-layer events (manifolds critique).

   A performance IQC from d = partner face to e = own face, certified by Theorem 15 for the *whole interconnection*, cannot miss a route. Any path from d to e passes through the loop the LMI describes, or it is not in the model, and that is then a modelling error, not a proof error. The critic's question changes from "did you enumerate the routes?" to "is the block diagram complete?". The second question can be checked mechanically against the code graph.
2. **A per-channel ceiling is a choice of performance supply rate.** Take e = W_out·y with W_out = diag(1/c₁, …, 1/c_m), the c_i innate per-expression ceilings, and Q_p = I, R_p = −I. Then ∫‖W_out y‖² ≤ ∫‖d‖², and so ‖y_i‖₂ ≤ c_i‖d‖₂ for each channel i over the whole partner face. Copy on channel i needs ‖y_i‖ ≈ ‖d_i‖, so the copy defect is ≥ 1 − c_i. (My derivation, from Theorem 15 with this supply rate.) Frequency-dependent weights (dynamic Ψ) let the ceiling differ by time scale: a fast onset echo allowed at a higher ceiling than sustained matching. That fits "fast match before context".
3. **It bounds slopes, not values: the critique-3 T8 error.** The norm clip bounded ‖C‖, not its Jacobian, and a pitchfork appeared. A sector/IQC description of the care operator constrains (Δz, Δw) pairs, i.e. slopes. The design's "(SG)" condition would be replaced by an LMI that already accounts for the operator's worst slope.
4. **Copy non-attracting.** A strictly dissipative closed loop with positive-definite storage has a unique globally attracting equilibrium for each constant input (S5–S6). Bistability and pitchforks are excluded *by certificate*. Copying can then attract only if the unique input-driven response is itself a copy, which item 2 forbids.
5. **Where it falls short.**
   - IQC analysis is a *verification* framework for a given model; it is not a core. It also belongs to "robust/optimal control, linear operators", which the operator excludes as cores. It can only be a **constraint on a new core**: a theorem the core must satisfy.
   - The analysis is for one fixed system. A learning system changes its parameters, and Theorem 15 must hold for every parameter value reachable by learning. Without a parameterization that guarantees it (see revay-2023-recurrent-equilibrium-networks.md), learning can leave the certified set.
   - Strict dissipativity of the whole loop excludes multistability. That is incompatible with persistent, hysteretic affective states (jung-2020-pcd-persistence-network.md; Lee et al. 2014 hysteresis) unless those states are outside the certified partner→face channel.
   - The partner is a human. To close the dyadic loop, the partner must be given an IQC (for example "human mimicry gain ≤ g_p"), which is an empirical assumption, not a theorem.
   - The LMI's size grows with state dimension. LMIs are not trainable constraints at scale (Revay et al. make the same point).

## Verdict
**adopt (as the proof form of the dial rule, not as a core).** State the D78 rule as a robust performance IQC (Theorem 15) on the whole interconnection, with a diagonal output weight of innate per-channel ceilings. Certify modules separately and combine them with Lemma 20. The Megretski–Rantzer 1997 original was not reached; cite it only through Theorem 28 here.
