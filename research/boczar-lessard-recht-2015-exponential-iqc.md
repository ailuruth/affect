# Exponential convergence bounds using integral quadratic constraints (Boczar, Lessard & Recht)

Ross Boczar, Laurent Lessard & Benjamin Recht, *Proc. IEEE Conference on Decision and Control (CDC)* 2015; arXiv:1503.07222v4 (19 Oct 2015), 10 pp. plus appendix.

Read in place of a source on exponentially weighted ("ρ-hard") IQCs. It also restates, in discrete time, the main IQC theorem of Megretski & Rantzer 1997 (its Theorem 2), which this session could not reach in the original (see also scherer-2022-dissipativity-iqc.md).

## What was read
arXiv v4, extracted text: §1–6 **in full** (introduction and the special case, notation and the classical IQC theorem, the ρ-IQC definition, Propositions 5 and 7, Theorem 8, the KYP computation (Lemma 11, Corollary 12), the examples (pointwise, Zames–Falb, Theorem 16, multiple IQCs) and the conclusion). **Not read:** the appendix proofs of Proposition 5 and Theorem 16.

## The computation, precisely
**Classical IQC (Definition 1, Theorem 2; discrete-time Megretski–Rantzer).** Signals y, u satisfy the IQC Π if ∫_𝕋 [ŷ; û]* Π [ŷ; û] dz ≥ 0. For G ∈ RH∞ and a bounded causal Δ: if the loop is well posed for τΔ, τ ∈ [0, 1], τΔ ∈ IQC(Π), and [G; I]*Π[G; I] ⪯ −εI on the unit circle, the loop is (ℓ₂, BIBO) stable.

**Why gain bounds give poor rates.** For a passive Δ and P ≻ 0 the LMI gives V(x_{k+1}) ≤ V(x_k), and one can tighten to (1 − ε)V. In the general IQC setting "P is not positive definite in general and V may not decrease along trajectories", so this trick fails.

**ρ-IQC (Definition 6).** Fix ρ ∈ (0, 1). Signals in ℓ₂^ρ (ρ^{−k}u_k ∈ ℓ₂) satisfy the ρ-IQC Π if ∫ [ŷ(ρz); û(ρz)]* Π(ρz) [ŷ(ρz); û(ρz)] dz ≥ 0. Proposition 7: Δ satisfies the ρ-IQC Π iff Δ′ = ρ₋ ∘ Δ ∘ ρ₊ satisfies the ordinary IQC Π(ρz), where ρ₊, ρ₋ multiply the k-th sample by ρ^k and ρ^{−k}. With a factorisation Π = Ψ*MΨ (Remark 10) the ρ-IQC is the time-domain inequality Σ_k ρ^{−2k} z_kᵀMz_k ≥ 0.

**Theorem 8 (exponential stability).** If G(ρz) is stable, τΔ ∈ IQC(Π, ρ) for all τ ∈ [0, 1], and [G(ρz); I]*Π(ρz)[G(ρz); I] ⪯ −εI on the circle, the loop is exponentially stable with rate ρ. Corollary 12: the frequency condition is the LMI [ÂᵀPÂ − ρ²P, ÂᵀPB̂; B̂ᵀPÂ, B̂ᵀPB̂] + λ[Ĉ D̂]ᵀM[Ĉ D̂] ≺ 0; minimising ρ is a generalised eigenvalue problem (bisection on ρ²).

**Which IQCs survive the weighting.**
- Pointwise IQCs (norm bound, sector [α, β]) hold for every ρ ≤ 1, "even if Δ is time-varying".
- Zames–Falb IQCs (slope-restricted static Δ) are ρ-IQCs only for multipliers H with Σ_k ρ^{−2k}h_k ≤ 1 (Theorem 16), a strict subset.

## Evidence with numbers
- G₁(z) = −(z + 1)(10z + 9)/((2z − 1)(5z − 1)(10z − 1)) with Δ(x) = b·arctan x: the sector IQC plus the off-by-1 Zames–Falb ρ-IQC give a rate bound that meets the true rate (from linearisation, ρ = 0.7058 at b = 1; Figs. 6–7).
- G₂(z) = (2z − 1)/(10(2z² − z + 1)): more ρ-IQCs give better bounds, but the bound is not tight even with six.

## What it means for the designs
1. **This gives the windowed form of an incremental gain bound.** The ledger judges slopes on finite windows, not on ℓ₂ from time 0. A certificate with storage decay V(Δx_{t+1}) ≤ ρ²V(Δx_t) + supply (my reading of the robust-REN LMI (16) of Revay et al. 2023, whose top-left block is ᾱ²P) gives, by telescoping (my derivation):
   - from time 0: Σ_{k≤T} ρ^{2(T−k)}(γ|Δe_k|² − γ⁻¹|Δy_k|²) ≥ 0, an exponentially discounted gain bound;
   - on any window [s, T]: ‖Δy‖²_{[s,T]} ≤ γ²(‖Δe‖²_{[s,T]} + Σ_{k<s} ρ^{2(s−1−k)}|Δe_k|²).
   So what happened before the window counts only through a fading term with memory 1/(1 − ρ). This is the object used in research/new-core-search-10-synthesis.md.
2. **Time variation.** Pointwise IQCs survive time variation; dynamic multipliers need more. A route whose gain is modulated by the agent's own context (a time-varying multiplier bounded by 1) stays inside a pointwise certificate.
3. **Rates are cheap to certify; tightness is not guaranteed.** The G₂ example shows the certified rate can stay loose, so the memory constant used in a ceiling proof should be the one the parameterisation imposes (ᾱ), not a fitted one.

## Verdict
**adopt (the exponentially weighted IQC as the windowed, fading-memory form of the per-expression gain bound).** It is an analysis result for a given system; the by-construction part comes from the REN parameterisation with ᾱ < 1.
