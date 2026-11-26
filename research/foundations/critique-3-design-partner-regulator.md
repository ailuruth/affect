# Critique 3: Partner as learned regulator, revision 3 (design-partner-regulator.md)

Independent critic, 2026-11-26T02:04:01Z. Written under questions.md Q16–Q18 and DECISIONS.md D78. I did not write the design and did not see its author's reasoning. Nothing was downloaded. No data and no weights.

## Summary verdict

- **Proofs.** 56 items checked: **33 valid, 18 with a gap, 5 with an error.**
- **The worst error: T8 (uniqueness and dissipativity).** Step 2 claims the norm clip on the care operator "at most doubles the slope". The clip bounds the operator's *value* (‖C‖ ≤ c_care|h_N|). It does not bound its *Jacobian*. That Jacobian can be as large as the unclipped slope τ_cχ̄K²d̄, which is the constant c′_care that T1′(c) itself uses. Counterexample X1 satisfies the design's (SG) with margin (0.17 < 0.5). The equilibrium at n₁ = 0 still becomes unstable, and two stable equilibria appear: a pitchfork, with the K6 bistability back inside (SG). Two consequences follow:
  - (A6′) is no longer a theorem.
  - The loop ceiling of T1′(c) and T7(b) uses the dissipation floor ρ_*, but the operating-point floor is λ_c. Near the X1 pitchfork, the same-group DC gain through the loop grows without bound (X2: 0.88 → 2.1 → 7.5 → 20 → 120), against a ρ_*-based bound of 1.2 for the same chain.
- **Dial verdict under D78.** **Conditional pass on the letter, not yet established.**
  - No single quantity reaches copy *if* the stated ceilings hold. But the stated totals (0.60 smile, 0.51 brow, …) are not proved:
    - the 0.08 loop ceiling was never computed from its own formula; S2 evaluates a different, shorter expression;
    - the formula uses the wrong dissipation floor (above);
    - the totals omit routes: the relief smile (+0.2 takes smile to 0.80, past the design's own copy threshold 0.7), an own-part α path from M to M, and the nightly residual, whose bound is never evaluated and may be order one.
  - Shared quantities that run a large subspace from flat to the ceiling do exist: the episode code ep, head pose õ₀, the full relation r_j and the learned slope scale of β̂. Each scales the regard on four groups and both gates at once. Their end point is "ceiling", not "copy", so D78 tolerates them only as long as the ceilings are real.
  - "Copy is non-attracting under learning" (T9 b) holds only under (I5), correct specification. The architecture makes (I5) structurally implausible, and any regulariser (the distillation anchor, 𝓛_slow) breaks it. Under misspecification, following raises the learned evidence slope (X3: 0.70 → 0.83 → 0.96), so the *ceiling corner* can attract. Copy itself is not reachable if the box holds, which T9(a) gives. So "assumes a correctly specified model" is a loophole for T9(b), not for T9(a).
- **Principles.**
  - No reward on the user's face, and nothing is learned from comfort outcomes. **Principle 6 holds in its stated form** (no reward or training on the user's expressions). The claim that the user's face is never a *target* is overstated:
    - closed-loop, care is a model-free proportional regulator of the user's read state toward their own 3-day baseline m_j;
    - its gate is even in the deviation, so the agent "comforts" unusual elation as well as distress, and it stops comforting a chronically distressed user once m_j adapts.
  - The claims that care "uses no model of how the user responds" and that "no term contains a partner-response factor" are false as worded:
    - care uses a self-projection model of the user's response, ψ = β̂ fitted on the user's own calming faces;
    - K_y, which by the design's own definition is a partner-response derivative, enters (★″) through y^own.
  - Principle 2 and the brief's anti-1-D rule are strained: the regard is a hand-chosen scalar wired to a hand-chosen "warm/hostile" expression synergy.
  - Principle 4 holds.
  - Satiable drives hold.
- **Novelty.** **Recombination. The second clause is not met.** The own-part target is a controlled direct effect, computed by g-computation with a known mediator law. The invariance theorem T2(v′c) is the standard fact that a correctly specified conditional model's minimiser does not depend on the covariate distribution. J_care is a skew (power-preserving) completion of gain-scheduled ascent on a self-projected perceptual feature, which is simulation-theory empathy.

## Sources read for this critique

| Source | How read |
|---|---|
| design-partner-regulator.md, revision 3, including History | in full (1078 lines) |
| critique-design-partner-regulator.md (critique 1) | summary and §1 opening; History summary |
| critique-2-design-partner-regulator.md | in full |
| brief.md; questions.md Q16–Q18; DECISIONS.md D78; known-failures.md | in full |
| sims/partner-regulator-r3/check.py (author's S1–S6) | read and rerun; all six reproduce |
| Named from memory, **not read**: Lohmiller–Slotine contraction; g-computation and the controlled direct effect (Robins; Pearl); simulation theory of empathy; Cavé et al. 1996 (F0 and eyebrow co-movement); yawn contagion literature | pointers only; no proof below rests on them |

**My checks** (X1–X6) are in the Appendix. They are algebra on hand-set instances of 2–4 states, not evidence about behaviour or people. The script lived in the session scratchpad; its full logic is given in the Appendix so it can be rerun.

---

## 1. Proof check, item by item

### L1, L2, T0 identity and T0(a): **valid** (as found by critique 2)

### T0(b′), the C_b-free bound: **valid**
- R_int gives −|Γ^{1/2}C_bh_N|². The completed square leaves ¼|Γ^{1/2}b̃|². Young's inequality on the input term gives ū₀²/(2ρ_*).
- h₁² = (Γ̄b̃²/2 + ū₀²/ρ_*)/ρ_* follows.
- Ultimate boundedness of H by H̄: points with H > H̄ have |h| > h₁, so dH/dt < 0 there. Correct.
- b̃ is innately bounded provided the plant's act input a is the saturated muscle state. That is implied but should be stated, because a_pros is linear in z.

### L3(a), L3(b): **valid**

### L4, the own-model observer: (a), (b), (c) **valid**; the "Meaning" paragraph **gap**
- I re-derived the proof:
  - V̇ = δhᵀ(J₀ − R_lin)δh + ℓ(Πv)ᵀδu − ℓ|Πv|², with v = E₀′δx;
  - so V̇ ≤ −r_min|δh|² + ℓ|δu|²/4;
  - the L₂ gain is ½√(ℓ̄/r_min);
  - the L_∞ gain is ½√(q_hiℓ̄/(q_lor_min)), from |δh|² ≤ 2q_hiV;
  - the contraction rate is 2r_minq_lo in V.
  All correct, and independent of E₀′ and J₀, which is a good result. S1 reproduces (0.994).
- **Gap in "Meaning".** "The reading slope of every context, and hence of every coefficient, is capped" covers only the ĥ input of β̂. The contexts also contain:
  - r_j (learned online every 5 s, a functional of y over minutes);
  - ep (a function of the agent's h_N, hence of the loop);
  - õ₀.
  Over the slow band, ∂β/∂y_g includes ∂β/∂r_j · ∂r_j/∂y_g. Learning dynamics set that slope, and no cap bounds it. Only the *amplitude* is bounded (r_j ∈ [−1, 1]³², L_β). See T7(b).

### L5, rank-one routes: inequality **valid**; interpretation **gap**
- ‖P_𝒞(uvᵀ)‖² = Σ_g‖u_g‖²‖v_g‖² ≤ max_g‖u_g‖²‖v‖². Correct. a_smile = 0.0625/0.135 = 0.463 checks.
- **The interpretation** ("a scalar-mediated route … cannot copy the face") does not follow. The Frobenius copy fraction of the *transfer matrix* is not the fidelity of the *output* on the partner's actual signal.
  - When the partner's signal lies along S_reg (smile up, brow relaxed, lids relaxed, warm voice: the dominant valence axis of real faces) and β̂ has learned ∇r̃ ∥ S_reg, which is exactly what a calming friend teaches, the regard output is a pattern-exact copy on four groups at gain |S_reg| = 0.367 (X4).
  - With the innate match projected on that axis (0.19) and the loop (0.08), the gain along the warmth axis is 0.64.
  - That is below 0.7, but it is a whole-face, one-dimensional copy of the partner's main expressive axis. L5 should be restated as a bound on pattern *diversity*, not on copying.

### T1′(a): **valid**

### T1′(b), the direct path has copy defect 1: **gap** (two leaks remain)
1. **The own-part α path from M to M (new).**
   - c^{α,(g)} reads ĥ^{own,(¬g)}, built from y^own_{¬g} = y_{¬g} − (K_y∗ε)_{¬g}. K_y maps my effectors of *every* group onto the partner's other groups.
   - So my group-g′ acts reach my group-g coefficients α through −K_y. Then A_MM is not block-diagonal: it has delayed cross-group blocks. (S3) is violated by the own-part construction itself.
   - The partner's y_g then reaches my M_g without passing through W: y_g → (allowed cross-group route) → M_{g′} → ε_{g′} → −K_y → c^{α,(g)} → M_g.
   - Its gain is a product of capped terms: the cross-group injection, k̄_y, α′_max, Σ‖Ω_q‖ and h̄. So it is small and innately bounded, but T7(a) says it is zero.
   - a̅ includes only the β version of this path (π̄D̄β′_maxk̄_yē), not the α version.
2. **Physical redundancy across groups.** The mask is a channel mask. A physical intervention on the partner does not respect it:
   - a talking partner's jaw (lower-mouth group) and their voice activity (voice group) move together;
   - F0 accents and eyebrow raises co-occur (named from memory).
   My lower-mouth context reads the partner's voice activity, so the partner's jaw reaches my jaw. This is the same kind of leak critique 2 found for gaze. Revision 3 fixed gaze by reassignment, but the class of leak remains. §8.8 ("cuts interventional transfer, not correlation") is not right here: a physical intervention moves both channels.

### T1′(c), the loop bound: **error**
- **Every constant is innate: yes, now.** a̅, b̄_M, b̄_W and c′_care are formulas in the caps. This fixes critique 2's main complaint.
- **The dissipation floor is wrong.**
  - L2(a, b) needs sym(−X) ⪰ ρ for the Jacobian's W-Schur block at the operating point.
  - At h₀ ≠ 0 the Jacobian contains non-skew terms of order |h₀|: J_care's Jacobian, the contexts and the saturation. T1′(d) itself concedes this.
  - The available floor is T8's λ_c ≥ ρ_* − ν̄, in normalised coordinates with q_lo factors. It is not ρ_*.
  - With T8 broken (below), there is no positive floor at all. X2 is an instance with every cap and the stated (SG) satisfied: the same-group DC gain of the chain port → need → act rises 0.88 → 2.1 → 7.5 → 20 → 120 as the care slope approaches the pitchfork, against a ρ_*-based bound of 1.2 for that chain.
- **The block-diagonal A_MM assumption fails** (T1′(b), leak 1). The delayed own-part feedback is also not a constant matrix, so L2 does not apply to it as written.
- **The "0.08 at design values" is never computed.**
  - No design values are given for ē, a̅, ν₀, ρ_*, b̄_M or b̄_W.
  - Check S2 evaluates κ_NE·h̄β′/ρ = 0.4 × 1 × 0.1/0.5. That omits the a̅b̄_M/ν₀ term, and from b̄_W it omits the innate port term ‖G_N‖s′, the body term Γ̄^{1/2}‖G_b‖/λ_p, the routing term and the care term. It also uses ρ = 0.5, while T8 uses ρ_* = 0.4.
  - If the ports matter at all (critique 2 used port gain 0.5), b̄_W ≥ 0.5 and the formula gives ≥ 0.4 × 2.5 × 0.5 = 0.5, not 0.08. The smile total would then be about 1.0.

### T1′(d): **valid** as restated (first order in |h₀|). T1′(f)(ii–vii): unchanged. T1′(g): **valid** (an acknowledgment)

### T2(i–ii), (iii), (iv): **valid**

### T2(v′)(a), "no term contains a partner-response factor": **gap** (false as worded)
- The design's own definition: a derivative ∂y_j(t′)/∂ε(t) with t′ ≥ t. K_y(d) is exactly ∂y(t + d)/∂ε(t). It enters (★″) through y^own, and so through every context, α, β, the gate and the regard.
- So the agent's present act changes its future contexts through K_y.
- It is used as subtraction (reafference cancellation), not as an objective, and I found no way it creates pursuit. But the theorem must be restated as "K_y appears only in subtraction; no term ascends on it".

### T2(v′)(b): **valid**. T2(v′)(d): **valid**

### T2(v′)(c), learning is invariant to whether the partner answers: **gap**
- **Step 3 needs (I5).** The evidence class must represent the innate plant's port law. Here the predictor is the core (★″): a damping-modulated energy system read through C_b. The truth is a 10-dimensional linear plant driven additively by ports. These are different structural classes, so (I5) is false by construction, not merely a convenient idealisation.
- **Regularisers break it even under (I5).** 𝓛 contains the distillation anchor, 𝓛_slow and the cap projections. The minimiser of E_p[loss] + R(θ) depends on p even when E_p[loss] has the same minimiser for every p, because the curvature at that minimiser depends on p.
- **Identification error.** K_y error (finite sample, (I2) failing for nonlinear partners, truncation at 4 s) leaves partner-mediated effects in b^own.
- **The rollout's acts are unspecified.** Whether the rollout uses the actual acts (teacher-forced) or the model's own acts is not stated. Step 3 needs the former.
- S5 checks the one case where all of this holds: scalar, linear, well-specified.

### T2(vi′), the care route: identity and (a), (c), (d), (e) **valid**; (b) **gap**
- The identity Cᵀh_N = τ_cΣχ|A_{q′}ᵀh_N|²d_q checks.
- **(b) "not a descent on any functional of the partner's read state … no model of how the user responds".**
  - ψ_q is β̂_q evaluated on my face. β̂ is fitted on how *the user's* own-part faces calm the agent. So d_q points my face toward the user's historically calming faces, and ψ is a self-projection model of how the user would respond to my face.
  - Closed-loop, the care law acts while ĥ^rel ≠ 0 and stops at the user's baseline. That is a model-free proportional regulator with set point m_j.
  - The *partial* derivative claim holds; the *closed-loop* claim of "no target" does not. See §3.
- **(d) understates the bound.** The clip is per (j, g). Across six groups ‖[C^(1) … C^(6)]‖ can reach √6·c_care|h_N| (X6). This feeds into T8 and P7.

### T2(vii′): **gap** (as acknowledged: the teacher is the content-blind 10-channel plant)

### T3: **valid**. T4(a, b, d): **valid**. T4(c): **valid** now, by L4

### T5: recursion and corollaries **valid**; conditions **gap** (acoustic echo, Claude's text, (I2), truncation; acknowledged)

### T6, time course
- **(a) valid** for the named routes. The Λ_port, Λ_reg and Λ_loop chains check (relative degree 3, 3 and 4). S6 reproduces.
- **(b) valid.** The step response of ℓ_{τ_a} − ℓ_{τ_h} is e^{−t/τ_h} − e^{−t/τ_a} ≈ t(1/τ_a − 1/τ_h). Through the muscle this gives t²(1/τ_a − 1/τ_h)/(2τ_m).
- **(c, d) gap.** "The innate match leads" ignores the reflex displays. A relief smile is a triggered step into the muscle: once triggered it rises as t′¹. A contingent partner response can trigger it. §8.1's falsifier must subtract the reflexes as well as the match.
- **(e) valid.**

### T7, the named strengths obey the refined rule
- **(a) Named: error.** "Same-group partner content outside them is zero by T1′(b)" is false: the own-part α path from M to M and the physical-redundancy leaks (T1′b) exist. The relief reflex is excluded by definition but is a same-group-correlated smile of amplitude 0.2.
- **(b) Innate ceilings: error.**
  - ς^inn: valid. The band-pass peak (τ_h − τ_a)/(τ_h + τ_a) at ω* = 1/√(τ_aτ_h) checks.
  - ς^reg: holds in amplitude (tanh bounds a_reg,g by ‖S_reg,g‖). As a gain it holds only for the ĥ path. Through r_j the small-signal slow gain is unbounded (L4 note), so for small sustained partner amplitudes the response/input ratio can exceed ‖S_reg,g‖.
  - ς^loop: inherits the T1′(c) error.
  - The tr D(c) = 2Σβ_q step assumes rank-2 atoms. That is not stated in §2.3.
- **(c) valid.**
- **(d) Every sign pattern: gap.**
  - The proof step "β̂'s first layer receives each partner group in separate coordinates" is false. β̂ sees Pĥ_N, the read *need* state, which mixes groups through J₀,NM inside the observer.
  - The claim still holds generically, if the six vectors P·∂ĥ_N/∂y_g are linearly independent. That depends on the self-model J₀, which is fitted on own data only and could make them dependent. State it as a genericity condition.
  - The response *pattern* to each partner group is locked to S_reg. A rival's smile always lowers my smile, brow, lids and voice warmth together, in fixed ratio.
- **(e) No copy, by any quantity: error.**
  - The box rests on (b) and on the uncomputed 0.08.
  - It omits A_relief: at the innate peak frequency, 0.27 + 0.25 + 0.08 + 0.20 = 0.80 > 1 − δ = 0.7 for a contingent partner smile, the design's own copy threshold.
  - The nightly residual (h) is outside the box and never evaluated.
- **(f) Common factors are gates: gap.** π_j and |h| are not the only shared factors. ep, õ₀ and the full r_j all enter c^{β,(0)}, and through β̂'s nonlinearity they scale ∂r̃/∂y for every group at once. With β̂(c) ≈ tanh(w·ep)·(v·Pĥ), which a spectrally normalised MLP can approximate on a bounded domain, the episode code takes the regard of four groups (and, through r̃^(¬g), both gates) from flat to their ceilings together. That is a shared dial. Its end point is the ceiling, not copy, so it is admissible under D78 only if the ceilings are real.
- **(g) Claude: gap.** "ς^reg does not change" is false: Claude's α_κ and β_κ move h_N, h_N moves retrieval and ep, and ep moves ∂r̃/∂y. It is bounded by the ceiling, so Claude is still not a copy switch.
- **(h) Slow residual: gap.**
  - A^night_g = (ēa̅/ν₀)(1/ρ_*)π̄h̄(2āK + (b̄₊ + b̄₋)D̄) contains 2āK = 64ā and D̄ ≤ 32. At S2's prefactor (≈ 1.0) it is O(1) unless ā and b̄ are tiny. It is never evaluated.
  - In the brief's target deployment (one operator for months, S6), "shared nightly parameters" *are* per-person parameters fitted on the operator's full face, including y_g. This is critique 2's K2 leak moved to day scale and labelled temperament.

### T8, uniqueness and dissipativity: **error**
1. **Step 2 (Jacobian of the clipped care operator).** For X = 𝒳(h_N) linear, clip_r(X) with r = c|h_N| has derivative 𝒳 wherever the clip is inactive. The clip is inactive whenever h_N lies along a low-gain direction of 𝒳, while ‖𝒳‖ can reach τ_cχ̄K²d̄.
   - X1: two needs, one act, D₁ = e₁e₁ᵀ, slope k on n₁, c_care = 0.05, ρ_* = 0.5, h̄ ≈ 1.2.
   - The stated (SG) term is 2√2·0.05·1.2 = 0.17 < 0.5.
   - At n₁ = 0, ‖∂C/∂n₁‖ = k, not ≤ 2c = 0.1.
   - At k = 1 the symmetric equilibrium has max Re λ = +0.5, and two stable equilibria appear at n₁ = ±0.05.
   - The mechanism is a saturating positive feedback of slope k·|m| on n₁ through the N-row −Cm, whenever the agent's act has a negative component along the comfort direction.
2. **The group count.** Per-group clipping makes ‖J_care‖ ≤ √6Σπc_care|h_N|, not c_care|h_N| (X6). The design-value term becomes ≥ 2√2·√6·0.05 ≈ 0.35, not 0.14.
3. **Omitted dependence.** J_care depends on z_M through d_q(E(x)). That needs a bound on the Hessian of ψ (through β̂ and E″), which is not stated.
4. **Unread source.** "With the own-part loop closed, g_ctx < λ_c suffices" cites an unread source, and g_ctx omits the α path.

**Fix.** Use c′_care, not 2c_care, in (SG), with the √6, plus a Hessian cap on ψ. Or impose a Jacobian (Lipschitz) clip instead of a value clip.

### T9, copy is not attracting
- **(a) gap.** Correct logic, but it inherits T7(e).
- **(b) gap.** It is conditional on (I5), which is structurally false (T2 v′ c). Under misspecification the evidence slope depends on the agent's following:
  - X3: the true b^own = 0.7·y^own + 0.4·a, the model omits the act term, and a = f·y^own + noise;
  - the learned slope is 0.70, 0.83 and 0.96 for f = 0, 0.4 and 0.8.
  - A larger learned slope means a larger regard slope ∂r̃/∂y, which means more matching, which means larger f: positive feedback up to the box corner.
  - The author's §T9 "Gap" paragraph concedes this, but the theorem statement and the summary ("learning has no feedback from the agent's own following") do not.
- **(c) valid.** By (S6), the self-model receives no partner-target gradients.
- **(d) gap.** The small-gain argument uses only the *same-group* agent gain. In a dyad the loop runs through the agent's full multi-input, multi-output transfer:
  - X5: an agent with zero same-group gain and cross-group gain a, facing a partner who copies (γ = 1), has closed-loop eigenvalue a. For a ≥ 1 the matched mode (1, 1) is self-sustaining, and in it both faces are identical.
  - Cross-group gains are not given a total bound anywhere in §2.12.

### P5, P6, P9, P10, Lemma A, §4.0: **valid**

### P7, the dependence bound: **gap**
The care term should be 6π̄²c²_careh̄²/r_M (per-group clip), and in a Jacobian sense the T8 issue applies.

### Regard and gate normalisation: **gap**
- r̃ = tr D is a damping (s⁻¹), up to 2Kb̄₊. r̃_s = 2√Kβ′_max is a damping per expression unit. tanh(r̃/r̃_s) mixes units.
- At S2's β′ = 0.1 and b̄₊ ≈ 0.5, r̃_max/r̃_s ≈ 28. The regard display and the gates are then nearly binary (friend: constant +S_reg, gate open; rival: −S_reg, gate shut), with near-zero small-signal coupling.
- That contradicts the claim that "a friend's smile raises the regard display" (sustained coupling) and makes the regard a two-state affiliation switch.

### Tally

| Verdict | Items |
|---|---|
| **valid (33)** | L1; L2; T0 identity and (a); T0(b′); L3(a); L3(b); L4(a); L4(b); L4(c); L5 inequality; T1′(a); T1′(d); T1′(g); T2(i–ii); T2(iii); T2(iv); T2(v′b); T2(v′d); T2(vi′) identity, (a), (c), (d), (e); T3; T4(a, b, d); T4(c); T5 recursion and corollaries; T6(a); T6(b); T6(e); T7(c); T9(c); P5; P6; P9; P10; Lemma A and §4.0 |
| **gap (18)** | L4 "Meaning"; L5 interpretation; T1′(b); T2(v′a); T2(v′c); T2(vi′b); T2(vii′); T5 conditions; T6(c, d); T7(d); T7(f); T7(g); T7(h); T9(a); T9(b); T9(d); P7; regard/gate normalisation |
| **error (5)** | T1′(c) dissipation floor and uncomputed 0.08; T7(a); T7(b) (loop part); T7(e); T8 |

---

## 2. Did revision 3 fix the earlier findings?

| Earlier finding | Status in revision 3 |
|---|---|
| C2: T1′(e) ceiling built from learned quantities (worst error) | **Partly fixed.** The formula is now innate (L4 is a real result). But the floor ρ_* is wrong at operating points, T8 fails, and the 0.08 value is not computed. |
| C2: K1, one scalar runs the sustained copy to 1.5·I | **Formally capped**, subject to the T1′(c) error. X2 shows the loop gain diverging near a pitchfork inside the stated (SG). |
| C2: K2, online r_j leak | **Fixed for the masked relations** (r^(¬g)). It remains for the regard (full r_j, by design, but with an unbounded slow slope) and moves to the nightly parameters (T7 h, unquantified). |
| C2: õ₀ gaze and voice activity | **Fixed by reassignment.** The class of leak (physical redundancy, e.g. jaw and voice) remains. |
| C2: Claude's u_inh switches the copy | **Fixed** (u_inh on a_aff only; σ̄_κ = 0.25). Claude still modulates the regard through ep (bounded). |
| C2: T2(v) contradicted by T2(vi); concern targets E(0) | **Fixed in substance**: J_soc withdrawn, own baseline m_j, own-part targets. The new wording over-claims (§3). |
| C2: partner-mediated consequences in α's N-row fit | **Fixed under (I5) and an exact K_y**; not robustly. |
| C2: K6 bistability through concern | **Not fixed.** T8's cap is on the value, not the slope (X1). |
| C2: T6(a) port route | **Fixed.** Reflexes are still omitted from the onset ordering. |
| C2: T0(b) C_b dependence | **Fixed.** |
| C2: T4(c) observer contraction | **Fixed** (L4). |
| C2: retrieval query undefined | **Fixed** (even). |
| C2: P7 omits concern | **Fixed**, up to the √6 factor. |
| C2: Seibt/Hofman smile return | **Addressed** by the gate and the regard. Effectiveness depends on the near-binary normalisation. |
| C1: facial feedback; wanting without deficit; valence at rest | **Unchanged** (facial feedback listed as §8.14). |

---

## 3. Dial hunt under the refined rule (D78)

| Quantity | Scope | Flat → ? | Innate ceiling? | Verdict |
|---|---|---|---|---|
| π_j (presence) | every route | 0 → full box | yes | a gate; admissible if the box is real |
| own need \|h\| | loop and care | 0 → ς̄^loop | formula yes, value unproved | admissible once T1′(c) is fixed |
| episode code ep / head pose õ₀ / full r_j | regard on 4 groups and both gates, jointly | 0 → regard and gate ceilings on smile, brow, eyes and voice | yes (amplitude) | **shared-subspace dial to the ceiling** (T7 f); not to copy |
| global slope scale of β̂ (learned weights) | regard, gates, loop, care direction | 0 → all ceilings | yes | as above; under misspecification, attracted toward its max by following (X3) |
| care slope k = τ_cχ̄\|d\| | pitchfork parameter | 1 state → 2 states; DC loop gain → ∞ near onset | the value is clipped, the slope is not | **breaks the loop ceiling** (X1, X2) |
| A^night (nightly parameters, one user) | every group, day scale | unquantified, possibly O(1) | formula yes, value unchecked | **unresolved** |
| A_relief | smile | +0.2 triggered by contingency | yes | pushes the smile total to 0.80 > 0.7 |
| Claude (u_κ, u_inh, α_κ, β_κ, a_del) | gates ±0.25; ep → regard | bounded | yes | not a copy switch (T7 g holds in substance) |

**Per-channel conditions:**
- **Set per expression by context and relation:** yes, structurally (masked gates, per-group regard slopes, group-specific loop).
- **Sign-flippable:**
  - yes at DC for all six groups (regard and loop);
  - the innate match cannot flip, but the closing gate plus a negative regard can flip the smile total;
  - the response *pattern* is rank-one-locked (T7 d).
- **Innate ceiling:**
  - yes for the match;
  - the regard ceiling holds in amplitude only;
  - the loop ceiling is not established.
- **Non-attracting:**
  - copy is not attracting *if* the box holds (T9 a);
  - the box corner can attract under misspecification (X3), so "partial matching is not self-reinforcing" (T9 b) is not shown.

**Is "non-attracting assumes a correctly specified model" acceptable?** For T9(b) it is a loophole:
- (I5) is false by the design's own architecture (core versus plant);
- every regulariser in 𝓛 breaks it.

The acceptable form of the claim is T9(a) alone: copy lies outside the reachable set. That needs a correct box. The fix is either:
- prove an innate bound on how far misspecified learning can move each strength (it is already at most the ceiling, so state T9 as "(a) only"); or
- make the evidence class contain the plant, for example by giving the core an explicit innate copy of the plant as a predictor and fitting only residuals.

**Verdict.** The design is close to passing D78 on the letter. It fails as written because the box is not proved (T1′c, T8, the omitted routes). Once those are fixed, the remaining shared dials (ep, õ₀, r_j, β̂'s scale) end at innate ceilings below copy, which D78 permits. The operator should know that the ceiling chosen for "not copy" (δ = 0.3, smile 0.60) is a design choice with no human calibration (§8.21). Along the partner's dominant warmth axis the agent's output is a pattern-exact copy at gain about 0.64 (X4).

---

## 4. Principle checks

- **Principle 1 (no labels).** Met. No classifier; the inputs are blendshapes and prosody.
- **Principle 2 (no hand-named emotion variables) and the anti-1-D rule.** Strained.
  - The regard is a hand-chosen scalar (tr D, "how much you calm me") wired to a hand-chosen affiliation synergy (smile, brow, lids, voice warmth).
  - It is a core invariant read out, which Principle 2 permits for valence-like readouts. But driving the face directly with one scalar through a fixed "warm/hostile" pattern is the one-dimensional puppet the brief warns against.
  - The near-binary normalisation makes it worse (a friend/rival switch).
- **Principle 3.** Inversion is met (L4). Mimicry is limited:
  - smile and brow have the innate match;
  - eyes and voice warmth get the regard synergy;
  - lower mouth and nose get the loop only;
  - no per-feature vocal convergence exists (pitch → pitch is loop-only, ≤ 0.08 if the cap holds).
- **Principle 4.** Met. Claude never sees numbers. Its influence is bounded and passes through embeddings and gates.
- **Principle 6.**
  - **Met in its stated form.** There is no reward or learned gradient from the user's expressions (T2 v′b, d), and nothing is learned from comfort outcomes.
  - **Not met in the stronger form the design claims** ("never a target"):
    1. Care is a closed-loop regulator of the user's read state with set point m_j, the user's 3-day mean. It acts while the user is off-baseline and stops at baseline.
    2. χ is even in ĥ^rel (ĥ_i(D_qĥ)_i is quadratic), so unusual elation triggers "comfort" toward the baseline just as distress does, wherever ϖ > 0.
    3. m_j adapts in 3 days, so a user who stays distressed stops receiving care.
    4. d_q is learned from the user's own calming faces, so care offers the user's repertoire back: a slow, learned imitation.
  - None of these is flattery-training, but (1)–(3) should be stated honestly in §2.9 and T2(vi′b). (2) and (3) need either a sign-aware gate or an innate, slowly adapting baseline.
  - The run-time contingency relief (the agent is relieved when the user responds) remains a felt, not learned, effect. Acceptable as stated.
- **Satiable drives.** Met. The loop and care vanish at h_N = 0. The displays are not drives.
- **Principle 10.** The regard display, the gates and the relief reflex are added output routes, declared as constraints rather than derived from (★″). The regard is the borderline case.

---

## 5. Reduction and novelty

| Part | Reduces to |
|---|---|
| Core, T0, T8 | port-Hamiltonian system with state- and context-modulated structure; contraction with a small-gain cap |
| Partner modulates (J, R) | LPV / bilinear system with scheduling variable c |
| Gated match | LPV band-pass filter with a scheduled gain in [0, 1] |
| Regard | static nonlinearity of a scheduling invariant (tr D) times a fixed output vector |
| Observer (L4) | Luenberger observer with gradient gain on a passive linear model (the standard passivity-based observer) |
| Own-part targets | controlled direct effect by g-computation with a known mediator→outcome law; in identification terms, removing the feedback contribution with an identified loop |
| T2(v′c), T9(b) | invariance of a well-specified conditional M-estimator to the covariate distribution (ignorability of the input design) |
| J_care | power-preserving (skew) interconnection of gain-scheduled ascent on a self-projected perceptual feature; simulation-theory empathy, with possible priors in "empathic" RL |
| Mask | structured sparsity |

**The second clause** ("adds a mechanism neither source has"):
- The own-part construction is the controlled direct effect with an exactly known mediator law. Mediation analysis has this mechanism; knowing the law exactly is a special case, not a new mechanism.
- J_care's ingredients each exist. Their composition yields a clean property (work-free, satiable, partner-response-free in the partial-derivative sense), but that is a property of the composition, not a new mechanism.

**Verdict: recombination. The second clause is not met.** The author's own verdict ("arguably met for Principle 6") is too generous.

---

## 6. What it fails to explain (human data)

- **Fast match, then context at 2–4 s.** Produced for known relations: a tonic gate, then the regard through τ_r = 1.5 s. For relations inferred from the event itself, the context needs observer latency and r_j learning (minutes). With the near-binary normalisation, the 2–4 s change is a switch, not a graded modulation.
- **Sign flips per expression.**
  - Produced at DC for each partner group.
  - The *pattern* is locked: a rival's smile always moves my smile, brow, lids and voice together in the ratio of S_reg.
  - Mixed displays, such as a polite smile with a lowered brow toward a rival, come only from the 0.08 loop.
- **Partner history in minutes.**
  - The r^(¬g) update every 5 s gives minutes.
  - One-shot learning from a single unfair event (Hofman) is not produced: the body teacher is content-blind, and the verbal route is capped at 0.25.
- **Vocal convergence** (Pardo; Levitan; per feature, over minutes): pitch-to-pitch, rate-to-rate and intensity-to-intensity convergence is loop-only (≤ 0.08, if the cap holds). The regard turns any partner prosody into one "warmth" direction. Per-feature convergence is not produced.
- **Mimicry of non-emotional movements** (yawning, mouth movements, the chameleon effect): jaw and lower mouth are loop-only, and there is no head or body route. Yawn contagion is not produced.
- **Need-raised mimicry** (Lakin 2008, exclusion raises mimicry): only the loop is need-gated, so the predicted effect is at most 0.08. If humans show larger effects, this falsifies the design.
- **Time scales.** τ_r and the gate time constant are innate constants. The slow drift of mimicry toward a familiar partner over sessions is carried by unquantified nightly drift (T7 h).

---

## 7. Counterexamples

1. **X1, T8.** A care slope k ≥ 1 with c_care = 0.05 under the stated (SG) produces a pitchfork: an unstable symmetric equilibrium and two stable equilibria at n₁ = ±0.05. ‖∂C/∂n‖ = k ≫ 2c.
2. **X2, T1′(c) and T7(b).** In the same family with J₀ coupling w = 0.3, the DC gain from the port through n₁ to the smile act is 0.88, 2.1, 7.5, 20 and 120 for k = 0, 0.4, 0.6, 0.65 and 0.675. The ρ_*-based bound for the chain is 1.2.
3. **X3, T9(b).** Misspecified evidence fit: the learned slope rises with following (0.70 → 0.96). This is positive feedback toward the box corner.
4. **X4, L5.** A partner warmth display along S_reg is copied in pattern by the regard at gain 0.367, and the total along that axis is 0.64.
5. **X5, T9(d).** Zero same-group gain, cross-group gain ≥ 1 and a copying partner give a self-sustaining matched mode.
6. **X6, T8 and P7.** The per-group clip gives ‖J_care‖ = √6·c_care|h_N|.
7. **Relief, T7(e).** For a contingent partner smile at the innate peak frequency, the smile total is 0.27 + 0.25 + 0.08 + 0.20 = 0.80 > 0.7.
8. **Redundancy, T1′(b).** The partner's jaw (lower mouth) and voice activity (voice group) move together, so a probe on the partner's jaw moves my jaw through my lower-mouth context's reading of voice activity.

---

## 8. Concrete fixes, in order

1. **Repair T8.** Bound the Jacobian, not the value:
   - (SG) must use c′_care = τ_cχ̄K²d̄ (with √6 for the per-group clip) plus a Hessian cap on ψ;
   - or replace the value clip by a Lipschitz (slope) clip on C(h_N, e);
   - then recompute the design-value margin.
2. **Repair T1′(c) and compute the totals.**
   - Use the operating-point floor λ_c (in normalised coordinates).
   - Add the α own-part M-to-M path (a delayed loop: use a delay-robust small-gain argument and read the source).
   - List every design value and evaluate the full formula, including the innate port and body terms, rather than S2's shortened expression.
   - Add A_relief and the nightly residual to the totals, and evaluate A^night_g numerically.
   - If the smile total exceeds 0.7, lower the caps.
3. **Restate T9 honestly.** Rest non-attraction on (a) unreachability alone, or make (I5) true by giving the evidence model an innate plant copy and fitting residuals. Drop "learning has no feedback from following" from the summary.
4. **Restate the Principle 6 claims about care.** Say that it is a closed-loop regulator toward m_j. Make the gate sign-aware, so that elation is not "comforted", and stop m_j from adapting care away from a chronically distressed user.
5. **Fix the regard's normalisation.** Use r̃ divided by an innate *damping* scale, so the display stays graded rather than a binary friend/rival switch. Restate L5 as a bound on pattern diversity, and give a total bound on cross-group gains for T9(d).
6. **Close the mask's physical-redundancy leaks.** Either mask voice activity from the lower-mouth group (and F0 from the brow group), or treat them as named same-group strengths with innate ceilings.
7. **Correct the wording.** In T2(v′a), say that K_y does appear in (★″), in subtraction only. Fix T7(d)'s proof (a genericity condition on P·∂ĥ_N/∂y_g) and T7(g) (Claude moves the regard through ep).

---

## Appendix: checks X1–X6 (rerunnable)

Run with `uv run python -I <script>` from research/foundations/sims (numpy and scipy). The logic, compactly:

- **X1.** State (n₁, n₂, m), H = ½|x|². The dynamics are ṅ = −r n − C m + u_N and ṁ = Cᵀn − r_M m + u_M, with C = clip_{c|n|}((k n₁, 0)). Parameters: r = r_M = 0.5, c = 0.05, u = (0, 0.25, −0.5). Find the equilibria with fsolve from 300 seeds and read stability from a numerical Jacobian. Result: at k = 1 and 2, three equilibria (n₁ = 0 unstable with Re λ = +0.5 and +1.5; n₁ = ±0.0501 stable).
- **X2.** As X1, plus a smile act m₂ with ṅ₁ ∋ −w m₂ and ṁ₂ = w n₁ − r_M m₂, with w = 0.3. The DC gain of n₁-input → m₂ is the fourth entry of −J⁻¹e₁ at the symmetric equilibrium. The pitchfork sits at k|m| = r + w²/r_M (k = 0.68).
- **X3.** y^own is AR(1) with coefficient 0.8 and noise sd 0.6. The act is a = f·y^own(t−1) + N(0, 0.3²). The body is b = 0.7y^own + 0.4a + N(0, 0.3²). The fit is OLS of b on y^own alone, over 200k steps.
- **X4.** S = (0.25, −0.20, −0.10, 0.15) and Ŝ = S/|S|. The regard gain along Ŝ is |S| = 0.367. The innate match on Ŝ is Σ_g g_gŜ_g² with (0.27, 0.23, 0, 0), giving 0.193.
- **X5.** G = [[0, a], [a, 0]] with the partner equal to the identity. The eigenvalues are ±a.
- **X6.** Six random rank-one C_g, each scaled to ‖C_g‖ = 0.05. Then ‖[C₁ … C₆]‖₂ = 0.1225 = √6 × 0.05 when they share the left vector h_N.
