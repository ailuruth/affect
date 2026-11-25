# Forssell & Ljung 1999, "Closed-loop identification revisited" (Automatica 35(7):1215-1241, doi:10.1016/S0005-1098(99)00022-9)

Source read: the submitted version, "Closed-loop Identification Revisited – Updated Version", Linköping technical report LiTH-ISY-R-2021 (1 April 1998, "Submitted to Automatica"), 55 pages, from the Linköping automatic-control report archive. Read in full: abstract, §1–§5 (approaches, assumptions, prediction-error review, direct/indirect/joint input–output and projection methods), §6 (Corollary 4, its remarks, Example 5), §7 (asymptotic variance), §9 (summary). Skimmed only: §8 (parameter-vector variance, Corollaries 7–11) and Appendix A.1. Not read: the remaining appendix proofs. The published Automatica text was not compared against this version.

## Claims
- "The fundamental problem with closed-loop data is the correlation between the unmeasurable noise and the input. ... whenever the feedback controller is not identically zero, the input and the noise will be correlated." Methods that work in open loop (subspace, non-parametric correlation and spectral analysis) fail on closed-loop data "unless special measures are taken."
- "There is only one method": direct, indirect and joint input–output approaches are all the prediction-error method with different parameterisations of the dynamics model G and the noise model H.
  - Direct: ignore the feedback; fit y = G(q,θ)u + H(q,θ)e to measured u, y.
  - Indirect: fit the closed-loop map from the external reference r to y, then solve for G using a known regulator K. The indirect method is a direct method whose noise model contains the regulator, H = (I + GK)⁻¹H₁ (Lemma 3).
  - Joint input–output: treat (y, u) as outputs of a system driven by r and noise; G = G_yr G_ur⁻¹. Variants: coprime-factor, two-stage, projection.
- Informativeness: data are informative if the spectral matrix [[Φ_u, Φ_ue],[Φ_eu, Λ₀]] is positive definite at all frequencies. Under linear feedback u = r − Ky this holds if and only if the reference spectrum Φ_r is positive definite at all frequencies, i.e. "for linear feedback we should use a persistently exciting, external reference signal, otherwise the experiment may not be informative." General condition: "there should not be a linear, time-invariant, and noise-free relationship between u and y." Switching between linear regulators, or a non-linear regulator, also makes the data informative.
- A delay is required somewhere in the loop: "either G₀(q) or k contains a delay" (Assumption 2).
- The direct method is consistent and statistically optimal *if* both G and H can be modelled correctly. It "requires a correct noise model (possibly estimated) to avoid bias in the dynamics transfer function for closed-loop data." The authors call it "the first choice": "When this method fails no other method will succeed."
- The indirect method needs exact knowledge of the regulator. Real regulators have limiters, anti-windup and other non-linearities, which "strongly disfavors" it.
- The projection method (an instrumental-variable idea going back to Akaike) is consistent "regardless of the feedback", even non-linear feedback, with a fixed noise model, at some cost in variance.

## Evidence with numbers
- Example 5 (noise-free, so only bias):
  - True system: G₀ = q⁻¹ ± 0.8q⁻², a two-parameter FIR. Minus signs were lost in our text extraction, so all coefficients below are magnitudes; true b = (1.0000, 0.8000).
  - Feedback: φ(x) = 0.25x + 4 for x > 0 and 0.25x − 4 for x < 0, a scaled Coulomb-friction element.
  - Data: white-noise reference, 5000 samples.
  - Estimates:
  - direct (1.0000, 0.8000);
  - indirect, ignoring the non-linearity (1.8060, 4.8793), "completely useless";
  - two-stage, 11th-order FIR first step (0.9595, 0.8258); ARX first step (0.8857, 0.6906);
  - projection, 11-tap non-causal FIR first step (0.9985, 0.7965).
  The non-causal taps matter: the two-stage method, which uses only causal taps, is biased under non-linear feedback.
- No real-data examples.

## Mechanism
Setup (Assumption 1): y(t) = G₀(q)u(t) + v(t), v(t) = H₀(q)e(t), e white. Feedback (linear case): u(t) = r(t) − K(q)y(t), with r independent of v. Then
- y = S₀G₀r + S₀v, u = S₀ⁱr − KS₀v, where S₀ = (I + G₀K)⁻¹ and S₀ⁱ = (I + KG₀)⁻¹.
- Input spectrum splits into a reference part and a feedback-noise part: Φ_u = Φ_uʳ + Φ_uᵉ, Φ_uʳ = S₀ⁱΦ_r S₀ⁱ*, Φ_uᵉ = KS₀Φ_vS₀*K*.

Direct method limit (Corollary 4, eq. 96–97). The estimate converges to
θ* = argmin ∫ tr Λ⁻¹H_θ⁻¹ [ (G₀ + B_θ − G_θ) Φ_u (G₀ + B_θ − G_θ)* + (H₀ − H_θ)(Λ₀ − Φ_eu Φ_u⁻¹ Φ_ue)(H₀ − H_θ)* ] H_θ⁻* dω,
with the **bias pull**
B_θ = (H₀ − H_θ) Φ_eu Φ_u⁻¹.
- In open loop Φ_ue = 0, so B = 0 for any noise model.
- In closed loop, B = 0 only if the noise model is right (H_θ = H₀).
- Bound (106): σ̄(B) ≤ σ̄(H₀ − H_θ) · √(σ̄(Λ₀)/σ̲(Φ_u)) · √(σ̄(Φ_uᵉ)/σ̲(Φ_u)). The bias is small where the noise model is good, where the feedback-generated share of the input power is small, or where the signal-to-noise ratio is high.

Variance (eq. 117, high model order, all methods): Cov vec Ĝ_N(e^{iω}) ≈ (n/N) (Φ_uʳ(ω))^{-T} ⊗ Φ_v(ω). Only the part of the input that comes from the reference counts: "that part of the input that originates from the feedback noise has no information value when estimating G." (At fixed model order, the direct method with a correct noise model can extract a little information from the noise part; §8, skimmed.)

Akaike / projection (eq. 71–72, 76–79): with an instrument x correlated with u and y but uncorrelated with e (standard choice x = r),
Ĝ_yu = Φ̂_yx / Φ̂_ux.
The projection method first fits u on r with a two-sided (non-causal) FIR filter, û(t) = Σ_{k=−M}^{M} s_k r(t−k). It then fits y = G(q,θ)û + H*e by output error. û is asymptotically uncorrelated with the noise, so the second step is an open-loop problem.

## What it implies for an engine that learns a partner model from closed-loop interaction
Map the paper's quantities onto the dyad:
- plant G₀: the partner's response map R, from the agent's expression x to the partner's face z;
- input u: x;
- output y: z;
- noise v = H₀e: everything the partner does on their own (their talk-driven expressions, mood drift, reactions to the room), usually strongly coloured;
- regulator K: the agent's own following (mimicry reflex, ρ/κ edges, facial feedback);
- reference r: whatever moves x that the partner did not cause, such as the agent's innate micro-variations b, spontaneous acts, or scheduled probes.

1. **C13 is exactly the direct-method bias.** The critique's rule (L_R) regresses z on the agent's trace with an implicit white, fixed noise model, while H₀ is strongly coloured. B = (H₀ − H)Φ_eu Φ_u⁻¹ is then non-zero, and it points along the agent's own following: Φ_eu ≠ 0 *because* x follows z. A strictly lagged regressor does not remove it, because lag only enforces the delay condition; it does not make H right. This explains why the critique still found R = 2.1 with a 1.2-s lagged trace.
2. **Two consistent routes, with different fragilities.**
   - (a) **Direct with a correct partner noise model.** Regress z(t) on the partner's own past *and* the agent's lagged x, ARX/Granger-style, which estimates H. This is consistent only if the partner's autonomous dynamics are inside the model class.
   - (b) **IV / projection with the agent's own exogenous variation as r.** R_IV = Cov(z(t), b(t−τ)) Cov(x(t−τ), b(t−τ))⁻¹, or in the frequency domain R̂ = Φ̂_zb / Φ̂_xb. This is consistent whatever the agent's following does, linear or not, and needs no model of the partner's own dynamics.
3. **A two-line simulation of ours** (not from the paper; numpy, 2×10⁵ steps):
   - Model: partner z_t = 0.7z_{t−1} + R·x_{t−1} + e_t; agent x_t = 0.8z_{t−1} + b_t with σ_b = 0.3.
   - True R = 0: strictly lagged OLS 0.57; ARX with the partner's own lag −0.00; IV on b −0.01.
   - True R = 0.2: OLS 0.90, ARX 0.198, IV 0.192.
   - Adding a hidden slow partner drive (an AR(1) at 0.99, standing for mood or topic): OLS ≈ 1.22 for both R = 0 and R = 0.2; ARX biased (0.04 and 0.03, so it misses a true 0.2); IV unbiased on average (5 seeds at R = 0.2: 0.13, 0.17, 0.23, 0.35, 0.02) but noisy.
   - So route (a) breaks as soon as the partner has unmodelled slow dynamics, which real partners always have. Route (b) survives, but pays in variance.
4. **The instrument must be truly exogenous.** b must be drawn by the agent's own generator, and logged, *before* and independently of the partner's current state. A residual of the measured expression is not acceptable: it contains the feedback. Anything that routes the partner into b breaks r ⊥ v. Examples: facial feedback carrying the partner's reflex copy (critique §2, item 4), or arousal driven by the partner's loudness. b's micro-variations must therefore be generated upstream of every partner-driven loop.
5. **Excitation budget.** The variance law Cov ≈ (n/N)Φ_v/Φ_xʳ says precision grows only with the power of the b-driven part of x, and only at frequencies where b has power. So b must be broadband over the partner's response timescales (about 0.2–3 s). Its amplitude sets a trade-off: more micro-variation means faster, surer learning of R, but a less faithful expression of the agent's state. In the simulation, σ_b = 0.05 gave a useless IV (first-stage F ≈ 1.5, estimate 0.16 for a true 0); σ_b = 0.3 gave F ≈ 47–500.
6. **Switching regulators are a second identification tool.** The paper notes that switching between regulators makes closed-loop data informative. For the agent this means alternating its own following gain: stretches of low or zero following interleaved with normal stretches. This is the agent-side analogue of double-video "breaks". Over those stretches the feedback-noise term Φ_uᵉ shrinks and B shrinks with it (bound 106).
7. **Delay.** Identification needs at least one sample of delay in the loop. The agent's following must not be instantaneous within a frame, or R and the following map become confounded at lag 0. Evaluate lag 0 separately or exclude it.
8. **No knowledge of the agent's own regulator is needed for IV**, which is lucky: the agent's following is non-linear and learned. The indirect method, which needs it, is the wrong choice; Example 5 shows how badly it fails.

## License
Elsevier journal article, all rights reserved; the technical report is freely downloadable from Linköping University. No code.

## Verdict: adopt (the formal frame for the closed-loop confound and its fixes)
It states the confound exactly (the bias term B), gives the condition that removes it (external excitation, or a correct noise model), and shows that only the externally excited share of the input carries information. The projection/IV route is the one robust to the agent's non-linear, learned following and to the partner's unmodelled dynamics. Caveats: everything is asymptotic and linear-in-G. The dyad is non-stationary (partners change mood and topic), so windows must be long enough for the variance law, and short enough for R to be roughly constant. We have not seen the paper's treatment of time-varying systems, and it may not have one.
