# Critique: Dyadic contingency sheaf (design-dyadic-sheaf.md)

Independent critic, 2026-11-25, written under questions.md Q16 and Q17. I did not write the design and did not see its author's reasoning. Nothing was downloaded. No data and no weights.

**Summary verdict.**
- **Proofs.** 28 items checked: 12 valid, 7 with a gap, 9 with an error.
- **The worst error.** The "copy margin" holds only on the exact copy maps (R = I, W = C_B). The design's ceiling (N) bounds the *weight* given to the partner edges, not the *size of their targets*. The ρ edge pulls the state toward R⁻¹z, and the κ edge pulls the body toward Wz. With a learned R = r·I, the partner-to-face transfer is exactly c(r)·I. That transfer is a single scalar gain on a copy. It rises from 0 through 1 (exact copy) to about 2, then falls again (C3, C4). So "copying the partner is impossible for every learned map" (§1, P2, Theorem 1(e)(i)) is false.
- **The dial.** There is one, and its effective gain can be derived exactly.
  - On the copy maps, the declared ceiling ϑ is itself the dial: T = ϑk/(k + (1−ϑ)q) when the anchor floor is small (C2), where k is the observation precision and q = p + λ is the total partner-edge weight.
  - Off the copy maps, the anchor floor γ₀ is a second dial (C5), and so is the learned scale of R or W (C3, C6).
  - The facial-feedback loop amplifies the innate reflex copy by 1/(1 − g_f), with g_f → 1 as the self-mirror precision Π_f grows (C7).
- **Novelty.** The author's verdict, recombination, is confirmed. Of the three claimed contributions:
  - (i) the ceiling is Friedkin-Johnsen susceptibility, and it is still a dial;
  - (ii) frame pinning is a vacuous invariance, which answers a reduction that never applied to general learned matrices;
  - (iii) the loop-class theorem is a linear instance of the sign rules for feedback circuits, and it holds only at a correct-model fixed point that closed-loop learning does not reach (C13).
- **Top fix.** Bound and prove the partner-to-face transfer T_h itself, not the edge weights, and say plainly that the bound is a gain cap. Learn R from strictly lagged, exogenous variation (instrumental variables), so that the agent's own following is not learned as the partner's contingency.

## Sources read for this critique

| Source | How read |
|---|---|
| The design, research/foundations/design-dyadic-sheaf.md | in full, 817 lines |
| questions.md Q16–Q17; brief.md (Principles and the foundations section); foundations/designs.md | in full |
| math-objects-synthesis.md | in full |
| mimicry-context-, coordination-, emotion-elements-synthesis.md | in full |
| face-development-synthesis.md | §1 and §4 in full; §2–3 skimmed |
| memory-replay-synthesis.md | headings and the ablation table (L1, L10, sham) |
| Prior work named in §3 (Chapman & Robbins 1990; Thomas 1981 and its proofs by Gouzé 1998 and Soulé 2003; Angeli & Sontag 2003; Hayes 1950; Rao & Ballard 1999; Wolpert, Doya & Kawato 2003; Kilner, Friston & Frith 2007; Ljung 1999 and Söderström & Stoica 1989 on closed-loop identification) | **Not read for this critique.** Named from memory, as pointers for the author to check. No claim below rests on them except the novelty comparison |

**Numerical checks.** The script is `research/foundations/sims/critique-dyadic-sheaf/check.py`. Run it with `uv run python critique-dyadic-sheaf/check.py` from sims/. It checks the design's own equations (the linear core, V_θ = 0, quadratic U) and is not evidence about behaviour. The checks are cited below as C1–C13.

---

## 1. Proof check, theorem by theorem

Notation follows the design: k = πa² is the scalar observation Gram, and q = p + λ is the total partner-edge weight.

### Lemma 0 (single shared edge gives a projection copy): **valid**
- With δ = Az − Ax, the cross block is −AᵀA, so x(∞) = (AᵀA)^†AᵀAz + Π_{ker A}x(0) = A⁺Az + Π_{ker A}x(0).
- Then Ax(∞) = AA⁺y.
- Every step checks.

### Lemma 1 (well-posedness)
- **Linear core: valid.** The homogeneous quadratic form vanishes only if the anchor term gives x = 0, and the ρ term (P ≻ 0) then gives z = 0. D_αH is similar to D_α^{1/2}HD_α^{1/2} ≻ 0.
- **Beyond the linear core: gap.** The condition ∇²V_θ ⪰ −σI is enforced only by a penalty in 𝓛_V, evaluated at states visited in replay (§6.4). That is not a global bound, so strong convexity is not guaranteed anywhere else in S.

### Theorem 1(a) (frame pinning)

**Steps 1–4: valid, but the result is trivial.**
- The steps are correct: A g_s⁻¹ = A ⇔ im(g_s⁻¹ − I) ⊆ ker A, and so on.
- Any reparametrisation of interior variables leaves the map from physical input to physical output unchanged. That is true of every model, including Altafini consensus and Friedkin-Johnsen.
- Two small issues:
  - The anchor value x̄_p lives on an S-stalk and must be transported too. (N) defines Γ_h as a scalar times I, which is not covariant under g_s.
  - If A has full column rank (k = 66 > n = 64, so generically yes), 𝒢 is trivial and the theorem says nothing at all.

**The conclusion that "the reductions do not apply": error (non sequitur).**
- The copy-in-a-frame result in the math-objects synthesis is not a claim that −I equals +I as physical maps. It says that a coupling which is a *group element on a single edge* gives a response family that is a copy composed with a fixed relabelling, so the family is still one-dimensional (T(h) = c(h)·D).
- Declaring the relabelling "inadmissible" changes nothing about the dimension of the family.
- That reduction also never applied to a general learned matrix. The synthesis itself says the single-edge discourse sheaf already gives A⁺B, "any linear map of rank ≤ k", with signed and off-diagonal entries.
- What escapes the dial is the *h-dependence of T_h* (the dial rank), not frame pinning.

**The related claim in §1 and §2.2 that the monodromy spectrum "is a property of the relationship that no change of coordinates removes": error.**
- Under the design's own 𝒢 with a nontrivial kernel, M_B = WRC_Bᵀ becomes WRg_s⁻¹C_Bᵀ. This differs from M_B whenever (g_s⁻¹ − I)C_Bᵀ ≠ 0, which is allowed because that image only has to lie in ker A ∩ ker C_B.
- C10 gives a counterexample (n = 8, k = 4). Both pinning conditions hold exactly, and spec M_B moves from {−1.97, 0.56} to {−5.88, 2.87}.
- The root cause is that the "return" along κ needs a right inverse of C_B, and the choice C_Bᵀ depends on the metric.
- The gauge-invariant loop object is the generalised spectrum of (N, H_s) in Theorem 3(c) and Theorem 6, which is physical. M_B is not.

### Theorem 1(b) (ceiling and copy margin)

**(i) Eigenvalues of M_p lie in [0, ϑ]: valid.**
- L_a ⪰ Γ_h ⪰ ((1−ϑ)/ϑ)L_p holds because ‖C_BᵀΛC_B‖ ≤ ‖Λ‖.
- C1 checked 2,000 random draws: the maximum eigenvalue was 0.4995 against the bound 0.5.

**(ii) The copy margin on the copy maps: valid as stated.**
- Steps 4–6 check.
- Note that "copy" here means x* = z* (the agent's state equals its own biased reading of the partner), not Ax* = y.

**The margin as used: error.** The margin is used as "for every learned map" in §1 item 1, as P2 in §4 ("a copy margin … for every learned parameter"), and in Theorem 1(e)(i). It does not extend.
- The x-stationarity equation is a matrix-weighted average with targets t_a, R⁻¹z (weight RᵀPR) and Wz on the body (weight Λ).
- (N) caps the weights, but the targets are unbounded in R⁻¹ and W.
- **Counterexample (C3, C4).** Take the ρ edge only, with k = p = 1, γ₀ = 0.01, ϑ = 0.5 and R = r·I.
  - The transfer is T(r) = kpr / (pr²(2k+p) + γ₀(k+p)), times I. That is exactly a scalar gain on a copy, with zero off-diagonal entries in the 6 × 6 matrix check.
  - T(0) = 0, which is flat.
  - T = 1, an exact copy, at r = 0.021 and again at r = 0.312.
  - The peak is T = 2.04 at r = 0.082, which matches the closed form kp / (2√(p(2k+p)γ₀(k+p))). That is exaggerated mirroring.
- **The κ edge alone (C6).** With r = 0 and w growing, T goes 0 → 1.35 → 3.27 → 0.89.
- Intuition: a weak learned contingency means "to explain what I see, my state must be large", so the ASL pull is strongest at intermediate r.

### Theorem 1(c) (no flat affect): **gap**
- The statement and the proof disagree: the statement omits C_B in A G_b K_s Σ_b K_s G_b^* Aᵀ, while step 3 includes it.
- Step 4's condition "A C_Bᵀ ≠ 0" is neither necessary nor sufficient for A G_b(iω) C_Bᵀ ≠ 0 when A has a kernel. The right condition is im(G_b C_Bᵀ) ⊄ ker A.
- "Independent of the partner" fails for the parts of b driven by afferents (being addressed, loud onsets, own prediction error), which depend on the partner.
- **Interpretation.** The theorem proves a *variance floor driven by the body*. It does not rule out flat affect in the sense of gap 1, where the partner's transfer is near 0. A stranger (R ≈ 0, W ≈ 0, which the design itself predicts in §3.10) gives T_h ≈ 0 on every learned channel.

### Theorem 1(d) (dial rank ≥ 2): **error**
- **Step 1.** The construction puts the c₁→c₁ entry "on the reflex core Θ_r". But T_h is defined as ∂(Ax*)/∂y, and Θ_r acts in the muscle layer, not in x*. The witness is outside the object the theorem is about.
- **Step 1, dimensions.** w e_bᵀA_{c₂}^+ does not conform. It should be an 8 × 64 rank-one matrix e_b uᵀ.
- **Step 3: false.** A rank-one change of W changes S and H_zz = K + P + WᵀΛW, and so H_s, which mixes every column of T.
  - In C9, the change in T outside column c₂ (max 0.062) is larger than inside it (0.021).
  - The state-route (c₁, c₁) entry moves from −0.041 to −0.032.
- **Definition.** Dial rank as dim span{T_h} counts the affine family T_h = T₀ + c(h)Δ as rank 2. That family is still one scalar running one channel from flat to copy. The construction in steps 1–4 is exactly such a family.
  - The relevant quantity is dim span{T_h − T_{h₀}}, and the theorem would also need a proof that the reachable directions are not a single c(h)·D.
- **(ii), the opposite signs of one entry defeating fixed D, D′: valid**, given the sign flip, which step 4 shows in the scalar reduction.
- **Step 6 (genericity): valid in form.** It holds for any generic rational parametrisation, so it is not specific to this design. FJ with a C(h) per relation has the same property.

### Theorem 1(e) (what a single scalar can do)
- **(i): error.** It rests on (b), which covers only the copy maps.
  - **ϑ is a flat-to-copy dial (C2).** With R = I, W = C_B and a small anchor floor, T = ϑk/(k + (1−ϑ)q). It runs 0.026 → 0.33 → 0.82 → 0.998 as ϑ goes 0.05 → 0.5 → 0.9 → 0.999, matching the closed form to four digits.
  - **γ₀ is a dial (C5).** At a fixed learned r = 1/3, T runs 0.016 → 0.14 → 0.63 → 0.94 → 0.9999 as γ₀ goes 10 → 10⁻⁵, approaching k/(r(2k+p)) = 1.
- **(ii): error of meaning.** "Cannot produce a flat face" is about body-driven variance (see (c)), not about the response to the partner.
- **(iii): valid**, provided γ₀ is scaled together with the precisions, as the proof says.

### Theorem 2 (satiable drives)
- **(a), (b), (d): valid.**
  - Convex φ_i with its minimum at 0 gives ∇U(b*) = 0.
  - (b) is the fundamental theorem of calculus with U ≥ 0.
  - (d) holds by construction.
- **(c): gap.**
  - The "being addressed" afferent lowers the contact deficit. So the partner's speech is a (satiable) drive reduction, contrary to the wording "no term increases with … speech duration". This is acceptable under Principle 6 because it is clipped, but the claim should say so.
  - The learning objective of g_inh ("replay-learned display regularities") is not stated, so "by inspection" cannot cover it.
- **Missing.** Theorem 2 proves that U is satiable. It does not show that anything *regulates*.
  - U acts only on the predicted body x_B. Its gradient biases the agent's belief toward the set point and its face toward the corresponding display.
  - No action in the core changes the sensed b, apart from own speaking (vocal load).
  - Homeostasis here is a prior, not a control loop. That matters for wanting, coping and agency (§4 below).

### Theorem 3(a) (onset order equals graph distance): **error**
- The step-response expansion and the walk counting (steps 1–3) are standard and correct. In control terms they are the relative degree of each input-output path.
- **The error is in the dependency graph.**
  - Equation (H) is driven by z_y, the reading "from the face alone", a *static* function of y. It is not driven by z.
  - So ℬ has a block into h, and the new-context route is y → h → x → m, of length 3. That is the same order t³ as the emotional route, not t⁴.
  - At a nonzero rest point, ∂ḣ_j/∂z_y = η_h x̃₀ᵀR_jᵀP ≠ 0 generically. At a zero rest point the h-route vanishes at first order altogether. Neither case gives order 4.
  - C12 makes the t³ coefficient of m acquire an η_h term once y → z_y → h is included.
- **Even if repaired**, an order in the limit t → 0 does not give latencies in seconds. Which route dominates at 1 s or 3 s depends on α, α_z, η_h and β_m, which are declared rates. "Carr's 2–4 s" is set by η_h, not by the structure.

### Theorem 3(b) (persistence and loop closure)
- **(i) Algebra: valid.**
  - (pr² + λ)(p + λw²) − (pr + λw)² = pλ(1 − rw)².
  - The det/tr bounds and the minimum of two quadratics check.
- **(ii) Courant-Fischer: valid**, as an upper bound on the slowest rate.
  - Minor gap: the flow matrix is D_αH with α_z = 10α, so the bound should use the Rayleigh quotient in the D_α⁻¹ metric, not α times the plain quotient.
- **Reading: error.** "A shared mood persists for a time that grows as (1−μ)⁻²" (§1 item 3) holds only for the anchor-free block L_so.
  - Under (N), the anchor is tied to at least the partner-edge weights, so it removes exactly this slow mode.
  - C8 (partner gone, K = 0): as μ goes 0 → 0.9 → 0.99 → 1, λ_min(L_so) falls 0.38 → 0.0026 → 0, while λ_min(H) with (N) stays at 0.70 → 0.71 → 0.76 → 0.77.
  - The author's own check in §3.9 ("at μ = 0.99 the anchor dominates") shows the same thing.
  - The persistence claim and the copy ceiling cannot both hold with the same (N). F4 as written tests a mode that (N) removes.

### Theorem 3(c) (the delay loop through the partner): **valid**
- (i): h is increasing on the reals; complex roots satisfy cos(bτ) < 1 and hence lie to the left of the real root.
- (ii): the minimum of h(λ) is λ* + f + 1/τ.
- (iii): |λ + f| ≥ f > |g| on Re λ ≥ 0.
- The §3.9 threshold e^{−2.5}/1.5 = 0.0547 checks.
- This is the classical analysis of λ + f − ge^{−λτ} (Hayes-type). The modelling assumption, a static delayed linear partner z_y = R_true x(t − τ), is strong but stated.

### Theorem 4 (reading through one's own body)
- **(a): valid.** It is the Gaussian posterior-mean (Kalman-gain) identity. The content is the tie A_obs = A_disp, not the adjoint.
- **(b): error of scope.**
  - For x* and z* of the linear core it is valid.
  - But "no effect … on the agent's expression, at any time" is false for the full design. The obstruction's obs component ½‖Az* − y‖²_Π contains the invisible part of y in full, and it drives:
    - the brow-raise reflex (§5.2);
    - arousal;
    - Claude's thinking budget;
    - replay priority.
  - Π is also a running inverse residual variance, so an invisible component on channel c lowers Π_c and changes how the *visible* components of c are read.
  - The innate afferents and Θ_r read y directly, not through Aᵀ.
- **(c): valid.** ∂z*/∂x = H_zz⁻¹Sᵀ, with the norm bound.
- **(d): gap.**
  - The residual of (L_A) is not "rendering noise only". f = render(m), and m contains Θ_r y (the partner's smile), D_del u_del (visemes) and the inhibition g_inh. None of these is a function of x.
  - So the self-mirror is not perfectly contingent, and (L_A) will fit A to the partner's reflex-driven and speech-driven face.

### Theorem 5 (contingency, no learning to lie)
- **(a): gap.**
  - The ΔP result (Chapman & Robbins's asymptote of Rescorla-Wagner) needs an intercept, which (L_R) lacks. With y normalised and x̃ not centred, the slope is (1−q)ΔP: the sign is right but the size is biased by the agent's own base rate.
  - x̃_τ(t) is a trace that *includes x(t)*, so no lag in the bank excludes the present.
- **(b): error.** "The fixed points … do not depend on the agent's current agreement energy" confuses the update's formula with its fixed point.
  - The moments of (x̃, z_y) are produced by the closed loop, in which x is pulled toward z through ρ, κ and the reflex-plus-feedback route. Regressing the partner on the agent's own trace then learns the agent's *own following*, inverted, as the partner's contingency. This is the textbook bias of direct closed-loop identification.
  - **Counterexample (C13).** The partner is an autonomous process that never responds to the agent, so the true R is 0. Under (L_R) with the design's trace:
    - learned R = 9.5 with W = 0, so R = 0 is an unstable fixed point;
    - learned R = 9.7 with W = 0.5;
    - learned R = 2.1 even with a strictly lagged 1.2-s trace, because the partner is autocorrelated.
  - This is a different route to "learning to lie": the agent learns that the partner follows it because it follows the partner.
- **(c): gap.**
  - With exponential traces, R → D·Cov(x(t−τ), x̃)Var(x̃)⁻¹. That equals cD only when channel autocorrelations are equal.
  - Online R is projected onto span{R_j}, so D is reachable only after a night of replay.
  - The closed-loop bias of (b) applies here too.

### Theorem 6 (mimicry is contagion; coregulation needs κ)
- **(a): valid given R = R_true.**
  - H_s = L_a + Rᵀ(P:K)R, and N = Rᵀ(P:K)R. The parallel sum is symmetric.
  - ν ∈ [0, 1).
  - The Lyapunov-Krasovskii derivative ≤ −2αxᵀL_a x.
  - **Scope.** C11: with the model wrong on two channels (the partner crosses where the model does not), eig(H_s⁻¹N) = {±0.33}, so the ASL loop alone has negative modes and can oscillate.
  - The theorem holds at a correct-model fixed point, and C13 shows closed-loop learning does not reach one.
  - "Contagion" here means positive loop gain in the agent's own state. With R = D crossed, the dyad's *faces* anti-correlate on those channels, which is not contagion in the Butler & Randall sense.
- **(b), (c): valid.** sign g = sign(pr² + λwr).
- **Model error under (b).** (L_W) fits W to the body *change* Δb(t + τ_κ) = b(t + τ_κ) − b(t). But the energy (E) uses Wz as a body *level* target, in ‖C_B x − Wz‖²_Λ. So the κ edge pulls the predicted body toward a predicted increment.
  - The monodromy μ = wr, and therefore the coregulation class, is built from a map learned for a different quantity.
  - The edge should be ‖C_B x − (b + Wz)‖², or W should be learned on levels.

### Theorem 7 (stability under switching)
- **Proof: valid.** V depends on no h, so it is a common Lyapunov-Krasovskii functional. The Young-inequality steps and the Barbalat step check.
- **Hypothesis: gap.**
  - The claim that "(N) and the caps enforce ‖N(h)‖ ≤ ν < λ_min(H_s(h))" is asserted, not proved.
  - With Λ ≠ 0, N is indefinite. N ⪯ H_s in the generalised sense (all that Theorem 6 gives) does not imply the norm condition.
  - The facial-feedback loop (C7) is not in the model at all.

### Count

| Item | Verdict |
|---|---|
| Lemma 0 | valid |
| Lemma 1, linear core | valid |
| Lemma 1, beyond the linear core | gap |
| T1(a), steps | valid (trivial) |
| T1(a), "the reductions do not apply" | error |
| T1(b)(i) | valid |
| T1(b)(ii), as stated | valid |
| T1(b), as used (P2, "every learned map") | error |
| T1(c) | gap |
| T1(d) | error |
| T1(e)(i)–(ii) | error |
| T1(e)(iii) | valid |
| T2(a), (b), (d) | valid |
| T2(c) | gap |
| T3(a) | error |
| T3(b), algebra | valid |
| T3(b), persistence under (N) | error |
| T3(c) | valid |
| T4(a), (c) | valid |
| T4(b) | error (scope) |
| T4(d) | gap |
| T5(a) | gap |
| T5(b) | error |
| T5(c) | gap |
| T6(a) | valid (only at R = R_true) |
| T6(b), (c) | valid |
| T7 | gap (hypothesis) |
| Gauge invariance of spec M_B (§1, §2.2) | error |

**Totals:** 12 valid, 7 gap, 9 error.

---

## 2. Dial hunt

Gap 1 asks for one scalar, or one-parameter family, that runs the system from flat affect to copying the partner. I found four. All are derived from the design's own fast-core equations (scalar channel, linear core).

1. **The ceiling ϑ.** On the copy maps (R = I, W = C_B), with anchor floor γ₀ + (other L_a terms) → 0:

   T(ϑ) = ϑk / (k + (1−ϑ)q),  so T → 0 as ϑ → 0 and T → 1 as ϑ → 1.

   When observation dominates (k ≫ q), T ≈ ϑ: **the ceiling is the gain.** The margin of Theorem 1(b) is (1−ϑ), which → 0. Weak point 7 anticipates this objection and answers that "the endpoint at any ϑ is the learned profile, never the copy". That is false when the learned profile is R = I, as it is for a partner who imitates. (C2)

2. **The anchor floor γ₀.** At fixed learned maps, T(γ₀) = kpr / (pr²(2k+p) + γ₀(k+p)) for the ρ edge.
   - It falls to 0 as γ₀ → ∞.
   - It rises to k/(r(2k+p)) as γ₀ → 0, which equals 1 at r = k/(2k+p). (C5)

3. **The learned contingency scale r** (or the consequence scale w).
   - For a partner who imitates uniformly, R = rI and T = c(r)I: dial rank 1, an exact copy at two values of r, and a peak gain above 1 whenever γ₀(k+p)(2k+p)p < (kp/2)², that is, when the anchor floor is small against the partner precisions. (C3, C4, C6)
   - Because R is learned in a closed loop with a self-reinforcing bias (C13), r drifts through this range on its own, without anyone setting it.

4. **The facial-feedback precision Π_f, acting on the innate reflex.**
   - The reflex Θ_r y enters m. m is rendered as f, f pulls x through the disp edge, and Ax returns into m.
   - The steady loop gain is g_f = Π_f a² / (Π_f a² + c), where c is everything else in L_a. The reflex copy is amplified by 1/(1 − g_f): 0.3 → 0.6 → 3.3 → 30 as Π_f goes 0 → 1 → 10 → 100 (C7, until σ_m saturates).
   - Π_f is a running inverse residual variance, so the *better* the self-mirror, the stronger the hidden copy channel.
   - This route also puts a partner-driven term into t_a ("the partner-independent target", which contains AᵀΠ_f f). So the decomposition used in Theorem 1(b) mislabels it.

**Verdict on the "copy margin".** It is a correct lemma about one point in map space (the copy maps), used as if it held for all maps. The structural fact is that (N) normalises weights, while copying is a statement about the *product of weight and target*.

**Verdict on "frame pinning".** It is not a defence against copy-in-a-frame.
- At a fixed h, T_h is an arbitrary learned matrix, which already escapes the group-element reduction.
- Across h, the real question is whether {T_h} moves along one direction. Frame pinning says nothing about that.
- Item 3 above gives a learned family that is exactly c(r)·I.

**What would remove the dial honestly.**
- State the ceiling on the operator norm of the partner block of T_h, for example by normalising Γ_h with ‖L⁻¹S‖ rather than ‖RᵀPR‖ + ‖Λ‖, and prove sup_h ‖T_h‖ ≤ ϑ < 1. Then say plainly that ϑ is a cap on gain, which is what it is.
- Then prove that {T_h − T_{h₀}} has dimension ≥ 2 for the *learned* family, not for a hand-built witness.

---

## 3. Reduction attempt

**At a fixed h, the fast core is MAP inference in a Gaussian Markov random field.** It is also a matrix-weighted Friedkin-Johnsen model with two partner "edges".
- The ρ edge is a linear-Gaussian observation of z given x.
- The κ edge is a second linear-Gaussian factor on (x_B, z).
- The anchor is the FJ prejudice term.
- The obs edge is the likelihood of y.
- The gradient flow (F1–F2) is predictive coding in the Rao & Ballard form. The update to z through Aᵀ(y − Az) is exactly the "transpose of the generative weights" that Theorem 4(a) calls the adjoint.

**Learning.** (L_A), (L_R) and (L_W) are LMS / Rescorla-Wagner rules. Their asymptote equals ΔP when the regressors are centred and exogenous (Chapman & Robbins 1990).

**Context.** h is context inference over a basis of maps (COIN-like). R(h) and W(h) are mixture-of-experts style linear interpolation of maps.

**Replay** is CLS with context reinstatement and distillation.

**The muscle layer** is a first-order filter with two summed inputs and a multiplicative inhibitory gate.

**I confirm the author's verdict: recombination.** The three claimed second-clause contributions:

| Claim | Assessment |
|---|---|
| (i) The gain knob is removed: a ceiling plus learned directions, with a proved copy margin | **Not achieved.** The ceiling is FJ susceptibility (the stubbornness in Parsegov's coupling condition). It is a flat-to-copy dial on the copy maps (C2), and it does not bound the transfer off them (C3–C6). The author already notes the FJ precedent. |
| (ii) Frame pinning closes the copy-in-a-frame loophole | **Vacuous.** Invariance of the input-output map under interior reparametrisation holds for every model. Boundary conditions fixing a gauge is standard. The loophole concerned the dimension of the response family, which pinning does not touch. The monodromy invariant it was meant to support is not gauge-invariant (C10). |
| (iii) Spectral classification of dyadic regimes; "learned mimicry is always contagion" | **A correct, conditional, linear lemma; not a new mechanism.** The sign of a loop decides between monotone persistence (positive circuit) and oscillation (negative circuit, here helped by delay). That is the linear case of Thomas's feedback-circuit rules and of monotone-systems theory. The clustering of couples' coupled-oscillator profiles by cross-term sign (rties; Butler 2011, in the project's coordination notes) is the empirical analogue. The specific statement, that a *correct* inverse contingency model gives a Gram-form, hence non-negative, round trip, is neat and I have not seen it stated for ASL. But it holds only at R = R_true (C11), which the closed-loop rule does not reach (C13). |

**Other parts of the design that are standard:**
- Theorem 3(a) is relative degree.
- Theorem 3(c) is the classical scalar delay equation.
- Theorem 4(a) is the Kalman gain.
- Theorem 5(a) is Chapman & Robbins.
- Theorem 7 is a delay-independent Lyapunov-Krasovskii bound.
- "Reading others by inverting one's own model" is Wolpert-Doya-Kawato (MOSAIC) and Kilner-Friston-Frith. The tie A_obs = A_disp is the "same generative model for self and other" of Friston & Frith's duet.

None of these is a fault, but none is new.

---

## 4. What it fails to explain (from the project's syntheses)

1. **Sign flips in competition and power** (mimicry synthesis §2: Hofman, Carr, Lanzetta, Likowski). The κ route can flip a sign only if the partner's expression predicts a change in one of the eight body variables.
   - A rival's sadness or a high-power target's anger changes none of energy, activation, contact, predictability, integrity, vocal load, novelty or rest.
   - Payoff, status and winning are not in B.
   - So these flips cannot be *learned* by (L_W). They can come only through Claude's Δh, which is slow and conceptual.
   - The design proves that the flips are realisable (Theorem 1(d)), not that they are learnable from what the agent can sense.
2. **Content and target of the expression** (mimicry synthesis, "What follows": anger at a common foe vs at me; laughter at a funny vs a disgusting scene).
   - T_h is linear in y at fixed h, so there is no fast interaction between gaze direction and expression, or between an episode and expression.
   - h changes only through slow contingency inference.
   - The brief's need-conditioned attention is reduced to a precision boost (element 11), which is a constraint, not a derived mechanism.
3. **Fast matching, then later context.** Theorem 3(a)'s separation fails (order 3 for both routes), and real latencies come from declared rates. So the Carr / Weyers timing is not derived.
4. **Partner history within minutes.** Online learning of R is projected onto the 17-dimensional span of the replay-learned basis. A contingency of a new kind, for example a new crossed channel, cannot be learned until a night of replay. The Hofman "unfair offer removes smile return immediately" needs exactly such a fast change on one channel.
5. **Learning mimicry from real contingency.** C13 shows the learned R reflects the agent's own following, not the partner's response. The face-development synthesis (item 7) asks precisely that crossed experience, not co-occurrence, should shape the map. In closed loop the rule sees co-occurrence.
6. **Wanting vs liking; agency and coping** (emotion elements 9 and 11). The core has no action that changes the sensed body, and no policy.
   - "Wanting" can only alter perception (precision), not pursuit.
   - "Controllability = ‖R‖" is a readout with no behaviour downstream.
   - The protest-vs-withdrawal signature needs a policy that the core does not have.
7. **The two face routes.**
   - D_del is fixed, and the training objective of g_inh is unstated.
   - The emotional route A_F x reaches all 52 blendshapes, not mainly the upper face (gothard, topper).
   - The routes also interact in a way the design does not analyse: the reflex plus facial feedback make a near-integrator (C7). That loop also contaminates (L_A) (Theorem 4(d)).
   - The palsy lesions hold by construction, which is fine.
8. **Metastability and escape from lock** (coordination §1f). A stable linear core with a constant partial coupling has no dwell-and-escape. §3.10 cites the ceiling for "intermittent, mid-range coupling", but a ceiling gives constant partial coupling, not intermittency.
9. **Turn structure** (coordination §1a, Fusaroli): anti-phase on readiness to speak with in-phase speech rate, at the same moment. Nothing in the design addresses this.
10. **Hidden-regulator bound** (coordination §1g). It relies on "partner share ≤ ϑ", which does not bound the transfer (§2 above). The persistence it would bound is removed by (N) anyway (C8).
11. **Grounding of emotion concepts.** The agent exposes the obstruction and the "loop spectrum" as emotion structure. But spec M_B is not gauge-invariant (C10), so it cannot serve as a relation-level invariant that Claude's naming could rest on.

---

## 5. Buildability

- **Derived from the object.**
  - The fast core: one 128 × 128 SPD solve per substep for the gradient flow of ℰ_h.
  - The three LMS rules.
  - The h step.
  - The readouts.
- **Not derived; added beside ℰ.** This bears on Principle 10, "one formal core".
  - The muscle layer, the deliberate route, D_del and g_inh.
  - The innate afferents and the lag selection by min over τ.
  - 𝓛_V, a separate body-prediction objective with fixed decays φ_Δ.
  - 𝓛_dist, 𝓛_g and 𝓛_Eh.
  - The Claude interface.
  - The learning rules are deliberately *not* gradients of ℰ (to avoid learning to lie). So inference and learning have two objectives. That is a defensible choice, but it should be stated as a departure from Principle 10.
- **Parameter counts.** All check: A 4,224; the R basis 34,816; the W basis 8,704; V_θ 24,961; g 25,410; E_h 6,160; total ≈ 105.3k.
- **Latency.** Under 0.5 MFLOP per frame is right. "Refactored only when h moves" ignores that the precisions are updated every frame. A refactor of about 0.7 MFLOP per frame is still trivial. PyTorch eager overhead (about 50 small ops at roughly 10–50 µs each) puts the core at 1–2 ms, not under 1 ms. NumPy or a fused solve would be faster. The core is negligible against MediaPipe, TTS and Claude, so latency is realistic.
- **Replay memory is underestimated.** Backpropagation through 300 frames × 4 substeps × 256 windows, through a flow that contains ∇V_θ, needs double backward. Activations of order 10³ floats per state give about 1,200 × 256 × 2,000 × 4 B ≈ 2.5 GB, not 40 MB. The Hessian penalty in 𝓛_V adds Hessian-vector products per state. This is still within the 6 GB peak, but "under 0.5 GB" is not credible. Use a stochastic minimum-eigenvalue estimate (a few power iterations), or fewer windows.
- **Disk:** 12.6 KB/s, about 136 MB per three-hour day. This checks.
- **Small build issue.** The partner's head pose and gaze are read through the agent's own pose and gaze rows of A. Without a mirror transform, the partner's leftward gaze reads as the agent's leftward gaze, which is rightward from the agent's point of view. A fixed reflection is needed and should be declared.

**Verdict.** The network is small, runs comfortably on an M1 Pro with 16 GB, and is mostly derived from ℰ. The replay budget needs about 5× more memory than stated. The non-derived parts should be listed as constraints.

---

## 6. The most important fixes

1. **Make the no-copy claim true or drop it.**
   - Bound the transfer T_h, not the edge weights. Normalise by the partner block's gain, for example Γ_h ∝ ‖L⁻¹S‖, and prove sup_h ‖T_h‖ ≤ ϑ.
   - State that ϑ is a gain cap.
   - Redefine dial rank as dim span{T_h − T_{h₀}} and prove it ≥ 2 for the learned family.
2. **Fix contingency learning in closed loop.** Use strictly lagged regressors, centre them, and use an exogenous instrument, such as the agent's innate body fluctuation b or its spontaneous acts. Concretely, R_IV = Cov(z_y(t), b̃(t−τ)) Cov(x̃(t−τ), b̃(t−τ))⁻¹. Then prove that the fixed point equals the partner's causal response. Without this fix, Theorems 5 and 6 rest on a fixed point that is never reached (C13).
3. **Close the reflex and facial-feedback loop.** Subtract the reflex and viseme components from f before the disp edge (an efference copy), or bound Π_f against the anchor. Include the loop in Theorems 1, 4(d) and 7.
4. **Repair the κ edge.** Use ‖C_B x − (b + Wz)‖², or learn W on levels. Re-derive Theorem 6(b) for that edge.
5. **Reconcile persistence with the ceiling (Theorem 3(b) vs (N)).** Either decouple the anchor from the loop direction, or withdraw the (1−μ)⁻² persistence claim and F4.
6. **Correct Theorem 3(a).** Drive (H) with z rather than z_y, or accept that both routes have order 3. State the latency predictions in terms of α and η_h.
7. **Replace frame pinning and spec M_B with a gauge-invariant loop object:** the generalised spectrum of (N, H_s). Withdraw contribution (ii).
8. **Give the agent a body variable or route through which competition, power or outcome can change Δb.** Otherwise say that the sign flips of the competition data come only from Claude.
