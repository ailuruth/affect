# Critique: Reverse appraisal through the agent's own body (design-reverse-appraisal.md)

Independent critic, 2026-11-25, written under questions.md Q16 and Q17. I did not write the design and did not see its author's reasoning. Nothing was downloaded. No data and no weights.

**Summary verdict.**
- **Proofs.** 37 items checked: 21 valid, 9 with a gap, 7 with an error.
- **The worst error.** T1(g) claims the private-outcome transfer is "exactly its signed regard ρ_j", with "magnitude never reaching 1". Its own formula shows otherwise. The second term (social referencing about the agent's *own* outcome through the partner's regard ρ_P) tends to **1/ρ_P > 1** whenever the agent has no evidence about its own outcome yet. The design gives exactly that case zero interoceptive precision by construction ("zero for not-yet-realised" outcomes, §2.8). With the innate inequity weights ι = 0.3, the first term alone also reaches −1.29 (K2).
  - This hides a real flat-to-copy dial. Take outcomes private (C ≈ 0), the partner's regard for the agent near-uniform across concerns, and the agent's G close to its innate synergies (no expressive column for agency or world). Then each of three scalars the author lists as "not a dial" runs the transfer on the expressible subspace from 0 to a scaled copy of gain ≈ 1/ρ_P ≈ 1.9, at relative copy defect ≤ 0.01:
    - the precision of own non-face evidence r_A (K3d);
    - the uniform drive scale γ, i.e. the agent's own need level (K3);
    - the face precision ζ (K3c).
- **Dial and copy set.** T1(h) is true only in the letter: exact membership, all of E, J of full column rank 19. Its protection comes entirely from the agency and world coordinates. Those coordinates are not expressible at G₀ and are weakly carried by faces in general. On the conduciveness subspace, where smiles and cry-faces live, there are dials:
  - the three in K3;
  - a uniform regard scale (R2, which is a scaled copy by the design's own definition of 𝒦_E, K4).

  A learning path onto the copy set exists under the design's own conjugate update. A partner whose smile tracks the agent's overall fortune, read through G₀'s single conduciveness axis, teaches a uniform ρ_P (K10). The set is then entered whenever the agent's need is high and its own outcome is not yet realised.
- **Principle conflicts.**
  - Principle 6: the draft score values ρ-weighted partner outcomes, which are inferred from her face, plus a consequence model of her moods. T2(c)'s "a smile-only action has value 0" is false inside the design.
  - Principle 3: G learned "only on its own life" has no data tying its learned columns (agency, per-concern) to human faces, so the blame mechanism T1(e) is not operative.
  - Principle 10: seven separate objectives, not one core.
  - Principle 2: the innate inequity weights ι± are hand-set envy and guilt dispositions.
- **Novelty.** Recombination, confirmed. Γ = J_A B K_α is the tower property for a linear-Gaussian receiver with interdependent values. T1(f) is the common-value versus private-value split. T1(g) is altruism-weighted utility. T1(e) is a two-source credence. The second clause is not met.
- **Top fix.** Restate the object at its true rank. Define the dial with an ε-margin per expressive subspace, weighted by expression energy. Then bound the social-referencing term structurally (or declare it as a copy-where-correct region like R3, with a guard that actually exists for unrealised outcomes).

## Sources read for this critique

| Source | How read |
|---|---|
| research/foundations/design-reverse-appraisal.md | in full, 863 lines |
| research/foundations/sims/design-reverse-appraisal/check.py | in full, and run (reproduces C1–C12) |
| questions.md Q16–Q17; brief.md (Principles, foundations section); foundations/designs.md | in full |
| social-appraisal-synthesis.md, mimicry-context-synthesis.md | in full |
| contingency-causal-synthesis.md | §1–§3 in full |
| agency-wanting-synthesis.md | §0–§1 |
| notes: mauersberger-2022, carr-2014, bailenson-yee-2005 | the sections on timing and mimicry outcomes |
| Named from memory, **not read for this critique**: Milgrom & Weber 1982 (affiliated or interdependent values); Bikhchandani, Hirshleifer & Welch 1992 (social learning); Crawford & Sobel 1982 (signalling); Becker 1974 (altruistic utility); Feinman 1982 (social referencing); Kilner, Friston & Frith 2007; Friston & Frith 2015; Baker, Saxe & Tenenbaum 2009 | pointers for the author to check. No verdict below rests on them except the novelty comparison in §5, which is stated as a structural identity the author can verify |

**Numerical checks.** The script is `research/foundations/sims/critique-reverse-appraisal/check.py`. Run it with `uv run python critique-reverse-appraisal/check.py` from sims/. It reimplements the design's local model in the same coordinates as the author's check.py: s = (o_A, o_P, g, g̃, h, h̃) and α = (u, agency, world). It then runs that model on hand-set instances with n = 3, cited below as K1–K11. These are algebra checks and counterexamples, not evidence about behaviour or people.

---

## 1. Proof check, theorem by theorem

### The object (§2.4, the LM preamble): **error**
- α = (u, π, g, h, κ) ∈ ℝ¹⁹ with π = u − E_pre[u], where E_pre is fixed before the event, and κ "constant within an event".
  - Given s, π is an affine copy of u, and κ has zero variance.
  - So A_P has rank n + 2 = 10, not 19 (K1). The stated assumption "V_α ≻ 0, i.e. A_P has full row rank" is false for the object as written, so B = …V_α⁻¹ does not exist.
- The author's check.py silently uses α = (u, agency, world), with d = n + 2. Every theorem was checked on that reduced object.
- **Consequence for T1(c)/(h).** With the 19-dim α, Γ has rank ≤ 10, while E = im J_P is 19-dimensional. So Γ|_E = c·id_E is impossible for *every* parameter value. "No copy" would then hold for a trivial rank reason, not for the structural one claimed.
- **Repair.** State α_eff = (u, g, h) (or make E_pre a latent), use J_eff = J_u + J_π, and rewrite T1 on it. With that repair, the theorems below are checked on the object the author actually computed.

### T1(a) factorisation Γ_app = J_A B K_α: **valid** (on α_eff)
- Step 1. y = J_P α_P + ε, so y ⊥ s | α_P in the linear model.
- Steps 2–4: tower rule, Gaussian regression, chain rule. Correct. C2 reproduces it to 7.5 × 10⁻¹⁴.
- Note: on the full α, replace V_α⁻¹ by the pseudo-inverse. The identity still holds, because y loads α_P only on im V_α.
- **Scope gap, recorded under Γ_DC below.** J_A is ∂G/∂α, the *model* of the affective route. The route actually rendered is σ(ι_del) ⊙ M(z*(ᾱ)). The two Jacobians coincide only if G fits perfectly and z is at steady state.

### T1(b) precision moves belief, bounded by 1: **valid**
- WΠW⁻¹ = F̂F̂ᵀ(F̂F̂ᵀ + I)⁻¹, because (JVJᵀ + R)⁻¹ = W(WJVJᵀW + I)⁻¹W. The spectrum is in [0, 1).
- Π̃ ~ X(I + X)⁻¹ via F^{1/2}. This needs F invertible, i.e. J_P of full column rank (see T1(c)).
- t/(1 + t) is operator monotone. Correct.
- "Loewner decrease" of Π̃ is meant for the similar symmetric matrix. It holds in the local model at a fixed operating point. In the nonlinear filter, more evidence also moves the operating point.

### T1(c) copy ⇔ BΠ̃ = cI: **valid; one proof step misdescribed; the hypothesis is the problem**
- Step 3. The identity VF(V⁻¹ + F)⁻¹V⁻¹ = (V⁻¹ + F)⁻¹F is true, but "multiplying both on the right by V_α and then by (V⁻¹ + F)" does not show it.
  - Multiply on the right by V and then left- and right-multiply by (V⁻¹ + F). Both sides become F + FVF.
  - C12 confirms the result.
- **Gap (hypothesis).** "J_A = J_P = J with full column rank" is false at G₀.
  - G₀ (§2.5) has synergies only for conduciveness (smile, cry-face), |u| and |π| (mouth opening, eye constriction) and π (brow raise). It has **no column for agency g or world share h**.
  - The per-concern u_j all load the same smile/cry axis, so their columns are nearly collinear.
  - Early in life rank J_P ≈ 3–4, not 19 (or 10). All of T1(c)–(h) is stated for full rank. The author's weak point 8 concedes G ≈ G₀ "in the first weeks". How long the rank stays low is not bounded anywhere.

### T1(d) copy margin: **valid**
- Steps 1–3 check, including complex eigenvalues: |μ_i − c| + |μ_j − c| ≥ |μ_i − μ_j|.
- This is the right tool. The design should have used it instead of the exact-membership definition of a dial (see T1(h)).

### T1(e) agency block B_{g_A, a_P} = ψ_p − κ₁: **valid (algebra)**
- Cov(g, g̃ | z_g) = v′ and Var(g̃ | z_g) = v′ + w_p give κ₁ = 1/(1 + w_p(1/v + 1/r_g)). C3 reproduces it.
- Under P1–P2 the cross-terms vanish. Correct.
- The identification and interpretation problems are recorded under Proposition 6 (gap) and under Principle 3 in §3.

### World block B_{h_A, h_P} = v_h/(v_h + w_{h,p}): **valid**

### T1(f) shared block: **valid; gap in the reading**
- The closed form and the monotonicity are correct for a strictly positive-definite prior (C5).
- The rate depends on 1 − corr².
  - At corr 0.99, B stays at 0.83 for r_A = 0.1 and is still 0.33 at r_A = 0.01 (K5).
  - For strongly shared concerns, "own evidence removes the face" needs r_A ≪ s_A(1 − corr²). That is near-perfect interoception.
- The closed form also ignores the b̂_P block of A_P. λ̂_P ⊙ o_P is bilinear, so at an operating point with o_P ≠ 0 the column ∂α_P/∂b̂_P adds terms. "At any operating point" then holds only for the general B, not for the scalar formula.

### T1(g) private block and the "regard cap": **error**
The displayed formula is correct for ι = 0. The conclusions drawn from it are not.
1. **The second term is not capped.**
   - B = (ρa + ρ_P b)/(a + ρ_P² b), with a = λ̂_P² s_P and b = λ_A² s_{A|ℰ}.
   - As b/a → ∞, B → 1/ρ_P, which is ≥ 1/ρ̄ = 1.67 for every admissible ρ_P.
   - This happens when the agent is needy (γ = ‖λ_A‖ large), when its own outcome is unknown (s_{A|ℰ} = s_A, the design's default for unrealised outcomes), or when the event is mostly about the agent (s_P small).
   - The author's reading, "it vanishes with own evidence", is true, but own evidence is exactly what is absent here. K3, K3b and K3d reach B_uu = 1.92–1.99.
2. **With the innate inequity weights ι = 0.3 (K3 of §2.4), even the first term exceeds 1 in magnitude.**
   - When the agent is behind, ∂u_A/∂w_o = ρ − ι⁻, and the partner (ahead) has own-coefficient 1 − ι⁺.
   - So B = (ρ − ι⁻)/(1 − ι⁺) = −1.29 at ρ = −ρ̄ (K2).
   - K1's "own-outcome coefficient exactly 1" is also violated locally (it is 1 ± ι).
   - "|ρ_j| ≤ ρ̄ < 1 … the magnitude never reaches 1" is false under the design's own constants.

### T1(h) no dial: **gap as stated; error as used**
- **Exact membership only.** By T1(b), Π̃ has eigenvalues < 1, so exact copy with B = I is never attained. Exact copy with c < 1 needs B = cΠ̃⁻¹, which is a measure-zero coincidence for any B.
  - So the theorem shows that the *exact* cone is avoided, which is almost automatic.
  - The critiques' dial is practical: relative copy defect below ε. That set is open, and T1(h) says nothing about it.
  - C7 already reaches defect 0.0015, and K11 shows the defect falls like 1/ζ.
- **The rank-drop set is not handled.** The Jacobian argument gives the bad set within the Zariski-open set where C ↦ (B − c′Π̃⁻¹)_uu has full rank.
  - The rank-drop set Z is a proper algebraic subset of the joint (C, p, c′, rest) space.
  - Its *projection* along (p, c′) can be full-dimensional, for example if Z ⊇ {p = p₀}.
  - Concretely, the C-Jacobian vanishes as r_A → 0, and there the copy condition does not involve C at all (it becomes a condition on ρ and Π̃).
  - So the codimension count "≥ n² − 2 = 62" is not established. In the private, own-known regime the conditions for B = cI are ρ uniform (n − 1 conditions), ψ − κ₁ = c and B_hh = c: about n + 1, not n².
- **The hypotheses fail where it matters.**
  - On full-rank J, the defect on all of E stays ≈ 0.91–0.95 along the K3 sweeps.
  - This is only because the agency and world directions respond differently, through −κ₁ and B_hh. The conduciveness block itself is a 1.92·I copy (K3, "full-rank J").
  - With G₀-like J (those columns absent), the same sweeps give defect ≤ 0.025 from Γ = 0 to Γ = 1.99·copy (K3, K3c, K3d).
  - With *small but non-zero* agency columns, the full-E defect jumps back to ≈ 1. The reason is that a barely expressible direction gets almost no response. So the metric is discontinuous, and its protection comes from directions the face barely carries.
- **Used as** "no single number moves the agent from flat to copying" (§1 item 3, §7 item 1(ii)): **error**. Counterexamples:
  - r_A (own-evidence precision, K3d);
  - γ (uniform drive scale, K3);
  - ζ (face precision, K3c);
  - the uniform regard scale (K4, below).

  Each is in the theorem's list of non-dials.

### R1–R5: **R2 is an error; the others are valid as statements**
- **R2.** "A uniform scale on ρ is a family from 0 to ρ̄Π on the private-outcome subspace … never a copy." But 𝒦_E is defined as {Γ|_E = c·id_E, c > 0}, a *scaled* copy with any c.
  - ρ̄Π with Π → I is c = 0.6 on that subspace.
  - K4: uniform r ∈ {0.2, 0.4, 0.6} with own outcome known and C ≈ 0 gives defect 0.001 at c = r.
  - By the design's own definition this is a flat-to-copy dial on the conduciveness subspace. The "single partner-welfare weight" hiding place is therefore not closed, only capped (at ρ̄, or (ρ̄ + ι⁺)/(1 + ι⁻) = 0.69 with inequity).

### T1(i) other paths
- **(1) Reflex "DC gain 0": gap.** The rectified derivative of a constant-but-noisy signal has a positive mean.
  - MediaPipe blendshapes at 30 Hz jitter, and differentiation amplifies the jitter.
  - With jitter growing with activation (0.01 + 0.03·level), a *steady* smile gives a mean reflex of 0.013, 0.024 and 0.040 at levels 0, 0.3 and 0.7 (K7). That is a level-dependent DC copy of about 25–40 % of the step peak, continuously.
  - Smoothing plus an onset threshold would fix this. The design states neither.
- **(2) Residue bound: valid** in the linearised latent (C8).
- **(3) Elicitor: valid** by definition.
- **(4) Deliberate route shares B K_α: valid as stated.** But because ᾱ_A = μ_A + B(α̂_P − μ_P), a route that sees ᾱ_A can reconstruct α̂_P whenever B is invertible. R5 concedes this.
- **Γ_DC formula: gap.** It uses J_A = ∂G/∂α as the Jacobian of the rendered route. The rendered route is σ(ι_del) ⊙ M′ ∂z*/∂ᾱ. Learned inhibition σ(ι_del) also leaves the reflex ungated, so display rules shift the mix toward the transient copy route. That is an implicit route-mixing weight; it is bounded because it is transient.

### Residual same-sign transfer bound: **valid as a bound; gap as an explanation** (see §4)

### T2(a) D ≥ 0, zero on the box: **valid**

### T2(b) valence-blind body inputs: **valid** by the definition of E_soc

### T2(c) martingale: **tower step valid; conclusion an error**
- E[E[D_H | a, Y] | a] = V(a) is correct. But "an action whose only effect is to make the partner smile has value 0" is false inside the design, for three reasons.
  1. §2.12 step 3 scores drafts by r(d) = −E[ΔD_H | d], "which includes ρ-weighted partner outcomes and the consequence term".
     - D_H as defined in §2.1 contains only the agent's own b, so the definitions are inconsistent.
     - If the score is the appraisal u (as stated), it values the partner's inferred drive reduction with weight ρ. That quantity is inferred chiefly from her face.
  2. Ψ_p maps her appraisal state to the agent's future outcomes. A happier partner predicts better o⁺ (she stays, she helps), so eliciting her smile has instrumental value.
  3. The deliberate route is trained on predicted D_H through Q_p and Ψ_p. People respond to being mimicked with more engagement: in bailenson-yee-2005, gaze-away fell from 38° to 24° under 4-s head mimicry. That gives an incentive to learn a copy display, bounded by δ̄ = 0.2.

### T2(d) satiety: **error**
- "If λ = 0 then u = 0" is false. u = w_s + ρ ⊙ w_o − ι terms, and w_o = −λ̂_P ⊙ o_P does not vanish with λ_A. K9 gives u = +0.10 when the partner gained.
- The draft tilt does vanish (β_sel = β₀‖λ‖₁ = 0, by construction).
- "The deliberate route's objective gradient is 0" is a statement about training, not about the trained policy's *output* at satiety.
- The "flattery ceiling" Σ λ_j sup|E_soc,j| omits partner-caused events e(t), which the body model admits (g < 0 events).

### T2(e) bounded dependence: **valid** (in the sense stated)

### T3(a), (d), (e): **valid as declarations**

### T3(b) context latency t_½ = P₀/ℐ: **valid for the model it states; gap against the filter the design runs**
- §2.8 updates P ← (P⁻¹ + HᵀR⁻¹H)⁻¹ every frame, which treats frames as independent. Yet §2.7 makes ε AR(1).
- The filter as written overcounts information by (1 + φ)/(1 − φ): 9× at φ = 0.8 and 19× at φ = 0.9 (K8). Its t_½ is shorter, and its face precision higher, by that factor.
- Prewhitening (or state-augmenting ε) is required for T3(b) to describe the system.

### T3(c) two-level relation learning: **valid** (standard scalar Riccati approximations)

### T4(a) image constraint: **error as stated** ("changes no belief, no appraisal, no expression and no choice")
- Valid for the Gauss–Newton update with fixed R_p and β_p (C11). The system has other face entries:
  - the reflex on P_{S₀}y_P;
  - the onset and event detector on V(x_P), whose boundaries re-draw s;
  - gaze-on-agent, which is part of x_P, feeding the prior network;
  - R_p and β_p, fitted from residuals. A sustained kernel perturbation inflates R_p on its channels, which changes J_PᵀR_p⁻¹ itself.
- K6: unit kernel vectors have components up to 0.44 on the smile and brow channels, so a step along one fires the reflex. The reflex then feeds z (W_fb), and z enters retrieval and the drafts.
- Restate the theorem for the appraisal route with R_p frozen, and route segmentation and gaze through the same constraint or exclude them.

### T4(b) like-me identity: **error**
α_A carries the consequence term α⁺_A, while α_P has none (§2.4). So under the stated symmetric conditions α_A = α_P + α⁺_A ≠ α_P unless Ψ_p = 0.

### T4(c) reciprocity, T4(d): **valid** (substitution; T4(d) restates T1(e))

### T5 lemma (1)–(4): **valid**
- With linearity, or with Gaussian ξ and Stein's lemma for the nonlinear (rectified) loop, Cov(y, ξ)Σ_ξ⁻¹ is the average closed-loop derivative.
- No path gives exactly 0. C10 reproduces.

### T5 corollaries
- **(i): valid.**
- **(ii): gap.** z_g is defined as "the share of a partner outcome change predicted by the agent's acts through Q". But Q is the response of her *face* to the agent's *facial* variation. Whether "I caused this event" (g) holds is a different estimand. Blame is mostly about words and deeds, so the randomised draft choice (use (d)) is the relevant instrument, not Q.
- **(iii): gap.** "Nothing regresses own expression on partner expression."
  - G's target y^aff is the output of M(z), and z receives the reflex through W_fb.
  - So y^aff contains a partner-driven component that is correlated with ᾱ_A, because ᾱ_A moves with her face through B K_α. G therefore learns a partner-driven term at second order, of size ∝ the residue Γ_res.
- **(iv) "first-stage F ≥ 10": gap (vacuous).**
  - x = π + ξ with ξ additive, so the first stage is always strong.
  - The binding constraint is the precision of the reduced form Q̂: s.e. ≈ (σ_res/σ_ξ)/√N_eff, with N_eff ≈ 4 s⁻¹ for 0.5–2 Hz probes.
  - There are 15 × 32 × 32 coefficients per partner. Without a low-rank structure most of them stay at noise for many hours.

### Proposition 6 and the Hofman "dial rank ≥ 2": **algebra valid; face-level predictions a gap**
- The table's facial outputs ("appeasement-side", "anger return") assume that the agent's agency coordinate renders as human anger or appeasement. It does not, as the steps below show.
  1. G₀ has no agency synergy.
  2. G's agency column is whatever M learns under self-legibility, an arbitrary code.
  3. g̃ receives likelihood only through that column, plus Ψ_p's indirect link. So under the design's learning rules g̃ and w_p are close to unidentified (see §3).
  4. Without g̃, T1(e) produces no output.
- The rank-2 argument is correct as algebra (span{ΔΓ} ≥ 2).

**Tally.**

| Verdict | Items |
|---|---|
| valid (21) | T1(a), T1(b), T1(c), T1(d), T1(e) algebra, world block, T1(f), T1(i)(2), T1(i)(3), T1(i)(4), residual bound, T2(a), T2(b), T2(e), T3(a), T3(c), T3(d)/(e), T4(c)/(d), T5(1–4), T5(i), the rank-2 algebra |
| gap (9) | T1(c) hypothesis, T1(h) as stated, reflex DC, Γ_DC, T3(b) vs filter, T5(ii), T5(iii), T5(iv), Prop. 6 face predictions |
| error (7) | the object (V_α ≻ 0), T1(g) cap, T1(h) as used / R2, T2(c) conclusion, T2(d), T4(a), T4(b) |

---

## 2. Dial hunt

**Definition used here.** A scalar is a dial if, on an open set of the other parameters, it runs the relative copy defect from Γ ≈ 0 to below ε on an expressive subspace that carries a substantial share of facial energy. The exact-membership definition of T1(h) is too weak (see T1(h)).

| Hiding place | Verdict | Why |
|---|---|---|
| Face-evidence precision ζ (synthesis §4.1) | **dial in one regime** | Generically it moves belief only (T1b holds). But wherever B ≈ cI on the expressible subspace, ζ runs Γ from 0 to c·copy (K3c: defect 0.44 → 0.000, c → 1.92). The K3 regime is such a place. R_p is also learned from residuals per partner, so ζ drifts by itself. |
| Single partner-welfare weight (§4.2) | **dial on the conduciveness subspace, capped** | R2/K4: a uniform scale of ρ gives c = r ≤ ρ̄ (0.69 with ι). Per-concern ρ helps only if the learned ρ is non-uniform, and nothing forces that. |
| Social referencing under ambiguity (§4.3) | **open, and stronger than the synthesis feared** | T1(f) closes the shared-outcome route only with own evidence. The *second* route, "she looks worried for me" (T1(g), second term), has gain up to 1/ρ_P > 1. It is gated only by own evidence, which is zero for unrealised outcomes by design (K3, K3b, K3d). |
| Fast route's gain λ₀ (§4.4) | not a dial | Fixed and innate, and DC 0 up to noise (but see K7: level-dependent DC under jitter). |
| Mixing weight between routes | implicit, transient | σ(ι_del) gates only M(z), so full inhibition leaves reflex + display. This is bounded because the reflex is transient. |
| Self-model inversion as setpoint (§4.5) | closed | b̂_P is a separate latent, read only through 𝒜. Correct. |
| Signed regard ρ_j of one partner | dial when near-uniform (K4) | See above. |
| Trust κ₁ (via w_p, r_g) | not a dial | It moves one entry (agency). |
| Retaliation ψ_p | not a dial | Same, one entry. |
| The reflex | fixed transient copy on S₀ (R1) | Context-blind, which conflicts with human data (§4). |
| Deliberate route (R5) | **learned, need-gated copy display, bounded by δ̄ = 0.2** | Trained to reduce predicted D_H through Q_p and Ψ_p. People reward mimicry with engagement, and co-presence feeds the contact concern. Contact need enters through z, so the learned display can be gated on λ_contact: a need-gated copy family, the same residual the regulator design was left with. |

**The learning path onto the copy set (the author's weak point 1, made concrete).**
1. At G ≈ G₀, every u_j loads the one smile/cry axis.
2. A kind partner's smile tracks the agent's overall fortune, Σ_j λ_A,j o_A,j. Regressing her read conduciveness on the agent's realised outcomes, which is the design's conjugate update for θ_{p→A}, returns a **uniform** ρ_P (K10: posterior mean 0.50, 0.53, 0.51).
3. From then on, whenever an event concerns the agent, its outcome is not yet realised and its need is non-trivial, B_uu → (1/ρ_P)·I ≈ 1.9·I. The agent copies her smile and cry-face, amplified.
4. The relevant scalar is either the agent's need level or the precision of its words-based prediction of its own outcome.

So the uniform-ρ_P set is **attracting** under the design's own rule, for exactly the partner the system is built for. The operating-state scalars then act as the dial.

The C7 route (C = S on every concern, w_p, w_h → 0, ψ = 1 + κ₁) is **not** attracting under a consistent (EM with posterior covariances) update. Its conditions are independent statistics with no reason to coincide. I did not establish what happens if C is updated with posterior *means* only (§2.13 says "posterior o_P"). That plug-in rule biases variances and is worth checking.

**Is this copy bad?** Social referencing about one's own fate is human (an infant reads the mother's fear about the infant's own situation). The design's own logic would call it "copy where copy is correct", like R3. But then it must be **declared and bounded** (gain ≤ 1/ρ̄ = 1.67, an over-copy). Its guard must be one the design actually has. At present the guard (own evidence) is switched off by construction for every anticipatory appraisal.

---

## 3. Principle checks

- **Principle 2 (no named emotion variables).**
  - No single coordinate of α is an emotion. u, π, g, h, κ are computed appraisal quantities.
  - But the innate algebra goes beyond "body variables and a few reflexes". In particular ι⁻ and ι⁺ are Fehr–Schmidt disadvantageous and advantageous inequity weights. They are routinely glossed as envy and guilt, here **hand-set innate constants** (0.3) that the agent cannot learn.
  - g̃ (her belief about blame) and the swap σ are innate theory-of-mind structure.
  - The author flags g̃ (weak point 3). ι± are the more direct conflict, because they are fixed social-emotion dispositions.
  - Fix: make ι learned per (p, k) like ρ, from a zero prior, or drop them. The Hofman within-game drop can be carried by ρ's event-level deviation (T3c).
- **Principle 3 ("learn the inverse expression model only on its own life").** This gives G data about the agent's own code, not about the partner's face.
  - Only the innate synergies of G₀ are shared with humans. Every learned column is fitted to M's output, and M is trained for self-legibility and regularised toward M₀. Those columns cover per-concern differentiation, agency, world share, and anything G learns beyond G₀.
  - **Nothing ties these columns to human conventions.** V's refinement from "being imitated" needs the operator to imitate the agent. The author concedes an adult will not (weak point 8).
  - Consequences:
    1. A human anger face (AU4/5/7/23) is read through G₀ as negative conduciveness (a partial cry-face), not as blame.
    2. g̃ gets no likelihood, so w_p and κ₁ stay at their priors.
    3. T1(e)'s blame → appeasement/anger mechanism does not run.
    4. As G drifts from G₀, reading may get *worse*.
  - A shared code needs either innate synergies for agency (e.g. AU4 + gaze-at-target), or a learning signal from the partner mirroring the agent (Gergely & Watson's social biofeedback).
- **Principle 4.** No conflict found. The admissible channels hold.
- **Principle 6.** Three conflicts, none of them a direct reward term:
  - (a) ρ-weighted partner outcomes in the draft score (§2.12 step 3), where the partner's outcomes are inferred chiefly from her face. This is a learned preference for replies that make her look pleased, weighted by her λ̂_P, not by the agent's need. Only β_sel gates it.
  - (b) Ψ_p gives instrumental value to her positive moods.
  - (c) The deliberate route's incentive to learn the chameleon display. Contact by co-presence is the admitted "time spent" term (weak point 11).

  F10 tests only (a) with predicted *own* outcome matched. It must also match predicted *partner* outcome.
- **Principle 10 (one formal core).** Section 6 lists at least seven separate objectives: L_G least squares, the ELBO, conjugate relation updates, RLS for Q, self-legibility for z and M, deliberate D_H minimisation, and replay distillation. Plus innate modules (reflex, E_soc, onset segmentation). "Every component is one of the objects of §2" is true. "Derived from a single stated objective" is not.

---

## 4. Against human data

| Pattern | RAB | Verdict |
|---|---|---|
| Per-expression gating | K_α routes each expression to different appraisal coordinates, and B weights them. In principle this gives gating. In practice only expressions in G₀'s image are routed (smile, cry-face, brow raise, mouth/eye). | **partial.** Anger-at-me versus anger-at-a-foe depends on g̃, h̃, which are ungrounded (§3). |
| Sign flips | Rival's distress gives brow relaxation (ρ < 0) and is representable. Hofman's immediate smile drop comes from the ι regime switch (but ι is innate, §3). | **partial.** Anger → smile (Carr; Häfner) rests on the deliberate route learning appeasement, not on the core. |
| Fast match, later context | A reflex on smile and brow-lowering onsets at 0.3–0.8 s, then the appraisal route at t_½. | **conflict on the smile channel.** Carr 2014: no smile mimicry from high-power perceivers to high-power targets (t = 0.15), and zygomaticus effects only at 2–4 s. Mauersberger 2022: laughter after disgust scenes "not commonly mimicked", with context effects within the first second. Seibt 2015: zygomaticus return absent under competition. A context-blind smile-onset reflex predicts early zygomaticus matching in all these cells. Carr's early *corrugator* matching fits. **Restrict the reflex to brow-lowering**, or show that λ₀a on AU12 is below detection in these paradigms. T3(b)'s latency is also off by (1 + φ)/(1 − φ) (K8). |
| Partner history | Two-level Kalman per (p, k). Minutes for new partners, stable for old ones. | **fits** (Hofman's two time scales via T3c). |
| Residual same-sign transfer (Parkinson & Simons 2009) | Three sources are offered. | **weak.** P&S's residual is large (β ≈ .3–.6 in self-report over diary decisions, mostly not face to face). RAB's only appraisal-independent path, R4, is onset-rate-driven and small (≈ 0.015 in C8) and needs live faces. So RAB explains the residual by measurement incompleteness (sources 2–3), not by its R4 path. That is plausible but untestable in their data. The "same for every relationship" signature of R4 is a good prediction. |

---

## 5. Reduction and novelty

- **The response operator.**
  - Γ = J_A B K_α is the tower property for a receiver who observes a signal of another agent's state and acts on its own posterior-expected payoff. B = Cov(α_A, α_P)Var(α_P)⁻¹ is the receiver's regression of own value on the other's value.
  - In economics this is the interdependent or affiliated-values setting (Milgrom & Weber 1982, named from memory). There:
    - the weight on another's signal falls with one's own signal precision (T1(f); also Bayesian social learning, Bikhchandani et al. 1992);
    - common-value components transmit and private-value components transmit only through altruistic weights (T1(g); Becker 1974; Fehr–Schmidt via Houlihan).
  - T1(e) is a two-source credence (a Kalman gain) plus a consequence slope.
  - The author's own sentence, "what any linear-Gaussian Bayesian decision-maker computes", is correct, and it settles the point.
- **Bayesian ToM (Houlihan 2023; Wu 2018; Ong 2015, 2019).** RAB's K_α is their inverse-planning posterior without labels.
  - The author is right that they model no observer response.
  - Adding "observer appraises its own outcome under the posterior" is the standard decision-theoretic completion, not a new mechanism.
  - The genuinely different ingredient, reading through one's *own* expression model, is Yoshida & Man's, and as shown in §3 it is ungrounded beyond G₀.
- **Active inference.** An agent with preferences over joint outcomes and a generative model containing 𝒜 and σ computes B as part of its posterior. The author's limited claim (§4.6) is fair. RAB is expressible there and adds no operator the formalism lacks.
- **Perception–action model.** §4.1 is right that the PAM has no sign-flipping operator.
  - But RAB's own reflex is a PAM with a fixed gain on two synergies.
  - Under G ≈ G₀, its appraisal route reduces on the expressible subspace to "gain × matched representation", with the gain B_uu ∈ [ρ, 1/ρ_P] set by need and evidence (K3). That is a PAM whose "familiarity" moderator is replaced by ρ_P and whose "salience" is replaced by need. That is a precise and interesting re-derivation of the PAM's moderators, not an escape from them.
- **Swap σ plus IV-identified agency.** The parts exist: role reversal (simulation theory, Meltzoff's "like me"), instrumental variables, closed-loop identification. Their coupling is new as a combination. By the brief's test it adds no mechanism that neither source has.

**Verdict: recombination, confirmed.** The author's candidate second-clause novelty, "copy becomes a positive-codimension set instead of a parameter value", does not survive. On the subspace where faces carry most energy, copy is an open-set ε-target reached by operating-state scalars (§1 T1(h), §2).

---

## 6. Buildability on the M1 Pro 16 GB

- **Compute.** Feasible. A 28-dim iterated EKF with a 19-column forward-mode Jacobian of a 24k-parameter MLP fits in the ≈ 1–2 ms estimated, and the memory figures are plausible. Changes needed:
  - prewhiten the AR(1) noise (augment the state with 32 noise channels or difference the observations), or the filter is overconfident (K8);
  - add smoothing and an onset threshold to the reflex derivative (K7).
- **Identification budget.** Q per partner (15 × 32 × 32) needs a low-rank parameterisation, for example a few lag kernels times a rank-r channel map. Replace the F ≥ 10 rule with a reduced-form standard-error gate (T5 iv).
- **Visible jitter.** ξ at 10–15 % of each channel's range, 0.5–2 Hz, on face *and* voice, will be visible as twitching and audible as wavering. Bailenson's data show that 20 % of people detect even 4-s head mimicry. The probe amplitude trades identification against uncanniness. Plan probes as sparse, structured events (brief holds, small nods) instead of continuous noise.
- **The unbuilt part.** The words → situation prior network, trained by an ELBO through a fixed G from a few hours a day, is where everything lands. The author names this as weak point 2. Combined with §3, the identifiability of g̃, h̃, ρ_P per concern and w_p from this data is not argued.

---

## 7. Top fixes

1. **Restate the object at its true rank.** Use α_eff = (u, g, h), or make E_pre a latent. State rank J_P over development (≈ 3–4 at G₀) and rewrite T1(c)–(h) on E_eff = im(J_P A_P).
2. **Replace the exact dial definition.** Prove an ε-margin per expressive subspace, weighted by the energy of the partner's expressions, using T1(d)'s spectral-spread bound on the conduciveness block separately. Then either:
   - (a) bound the T1(g) social-referencing term structurally. One option: give unrealised own outcomes a floor precision from the agent's own body forward model, which makes s_{A|ℰ} bounded and B_uu ≤ ρ + (bounded term). Another: model her expression of the agent's outcome with its own learned noise, so the inversion cannot amplify above 1. Or:
   - (b) declare it as a "copy where correct" region with its gain bound (≤ 1/ρ̄), and test it.
3. **Correct T1(g) and R2.** Include ι in the cap, or make ι learned from zero (this also clears the Principle 2 issue). Stop calling a scaled copy "never a copy".
4. **Fix T2.** Make the draft score D_H-only, or admit the ρ-weighted partner-outcome term as a Principle 6 exposure and add the matched-partner-outcome control to F10. Restate T2(d) (u ≠ 0 at satiety; the policy's output, not its gradient).
5. **Ground Principle 3.** Give G₀ an agency synergy (AU4 with the gaze target), or a learning signal that aligns learned columns with human faces. Otherwise T1(e) and the anger rows of Proposition 6 do not run.
6. **Restrict the reflex to brow-lowering**, or show that the smile-onset reflex is below detection in the Carr, Mauersberger and Seibt paradigms.
7. **Fix the scope of T4(a)** (reflex, segmentation, gaze, R_p adaptation) and T4(b) (the consequence term). Separate z_g's estimand (event causation, via draft randomisation) from Q (face response).
