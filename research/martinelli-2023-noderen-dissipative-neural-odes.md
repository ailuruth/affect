# Unconstrained parametrization of dissipative and contracting neural ordinary differential equations (Martinelli, Galimberti, Manchester, Furieri & Ferrari-Trecate)

Daniele Martinelli, Clara Lucía Galimberti, Ian R. Manchester, Luca Furieri & Giancarlo Ferrari-Trecate, *Proc. IEEE Conference on Decision and Control (CDC)* 2023; arXiv:2304.02976v2 (15 Sep 2023), 6 pp. plus appendix. Code cited (github, NodeREN); not inspected.

## What was read
arXiv v2, extracted text: §I–V **in full** (problem, Definitions 1–2, Table I of supply rates, the NodeREN model (8)–(9), Lemma 1, Theorems 1–4, Remarks 1–3, the pendulum identification and irregular-sampling results, conclusions). **Not read in detail:** the appendix proofs (A–E).

## The computation, precisely
**Model.** A continuous-time REN: ẋ = Ax + B₁w + B₂u + b_x, v = C₁x + D₁₁w + D₁₂u + b_v, y = C₂x + D₂₁w + D₂₂u + b_y, w = σ(v), σ slope-restricted.

**Properties.**
- Contracting (Definition 1): |x_a(t) − x_b(t)| ≤ κe^{−ct}|a − b| under the same input.
- Incremental IQC (Definition 2): a storage S ≥ 0 with S(Δx(t₁)) ≤ S(Δx(t₀)) + ∫ s_Δ(Δu, Δy) dt, s_Δ = [Δy; Δu]ᵀ[[Q, Sᵀ], [S, R]][Δy; Δu], Q ⪯ 0. Table I: ℓ₂ gain γ is Q = −I/γ, R = γI, S = 0; passivity, input and output passivity are other choices.

**Results.** Theorem 1: an LMI in (P, Λ) gives contraction; Remark 2: adding −2ω̃P gives the rate c = ω̃. Theorem 2: an LMI gives the incremental IQC. Theorems 3–4: direct (unconstrained) parameterisations onto rich subsets of contracting and IQC NodeRENs, via a Cayley-type construction. Remark 3: every IQC-NodeREN is also contracting.

**The caution (Introduction, Remark 1).** The guarantees of discrete-time RENs "are only compatible with discrete-time or sampled-data systems", and those discrete conditions "fail to ensure these properties for the continuous-time solutions". Conversely, a continuous-time certificate holds for the exact ODE; a numerical integrator with too few steps can break it (fixed-step methods "may be insufficient … which can result in numerical instability").

## Evidence with numbers
- Pendulum identification, C-NodeREN with n = 4, q = 5, about 150 parameters: test losses for euler, rk4 and dopri5 in a range plotted against function evaluations (Fig. 1); a general, unconstrained NodeREN can be unstable on longer horizons where the C-NodeREN is not (Fig. 2).
- Ten C-NodeRENs on ten irregularly sampled data sets: test losses 3.7 × 10⁻⁴ to 9.1 × 10⁻³.

## What it means for the designs
1. **Certify in the time base the engine runs in.** The engine's routes are discrete at 30 Hz, 10 Hz and 2 Hz. A ceiling certificate must be stated for the discrete map that is actually executed (a discrete REN at that rate), or the integrator must be shown to preserve it. A continuous-time certificate on a module that is then Euler-stepped is not a ceiling.
2. **Multi-rate composition.** Routes at 2 Hz feeding the 30-Hz output are sampled-data interconnections; the certificate of each discrete block holds at its own rate, and the hold/upsample maps between rates have gain ≤ 1 per sample energy only if they are zero-order holds normalised by the rate ratio (my note; to be checked when built).
3. Otherwise this is the same object as the REN; it adds no per-channel structure.

## Verdict
**background (continuous-time RENs; its value here is the warning that a certificate holds only for the time discretisation it was proved for).**
