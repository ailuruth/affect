# Critique 2: Reverse appraisal through the agent's own body, revision 2 (design-reverse-appraisal.md)

Independent critic, 2026-11-26T02:03:56Z

Written under questions.md Q16, Q17 and the refined rule of Q18 / DECISIONS.md D78. I did not write the design and did not see its author's reasoning. Nothing was downloaded. No data, no weights.

**Read for this critique:** brief.md (Principles 1–10 and the foundations section); questions.md Q16, Q17, Q18 with the operator's answer; DECISIONS.md D78 (and the novelty bar at line 231); foundations/known-failures.md; social-appraisal-synthesis.md; design-reverse-appraisal.md revision 2 in full (1,004 lines); the revision-1 critique (critique-design-reverse-appraisal.md) in full; sims/design-reverse-appraisal/check_r2.py (the author's D1–D10).

**Not read, named from memory only:** Millidge, Tschantz, Seth & Buckley 2020 (active inference versus control as inference); Parr & Friston 2019 (generalised free energy); Dimberg 1982/2000 (rapid facial reactions); de Melo et al. 2014. Only the reduction verdict in §5 leans on the first two, and it is stated as a structural identity that can be checked against the design's own equation for 𝔉.

**Numerical checks.** `research/foundations/sims/critique-2-reverse-appraisal/check.py`, run from sims/ with `uv run python critique-2-reverse-appraisal/check.py`. It runs the design's own local linear-Gaussian transfer, Γ = J_A C_AP J_Pᵀ(J_P V_P J_Pᵀ + R)⁻¹ (T1(a)), on hand-set instances. The results are cited below as X1–X6. They are checks of the document's algebra and counterexamples to its claims. They are not evidence about behaviour or people.

---

## Summary verdict

- **Proofs.** 44 items checked: **22 valid, 15 with a gap, 7 with an error.**
- **The worst error.** T4(ii) and the T4 table claim that no single quantity takes a subspace of dimension ≥ 2 from flat to copy. The proof shows only that the *zero pattern* of each group's transfer does not depend on a single-group scalar. It does not show that the *size* of that transfer is unaffected. This is the same exact-membership slip the first critique found in revision 1's T1(h), repeated one level down.
  - X2: her inferred need on one concern (λ̂_P,1, a scalar that enters only group 1) runs a 2-dimensional subspace from ‖Γ|_U‖ = 0.002 to 1.43, with copy defect 0.50 → 0.0001. It does this by explaining away through the shared face-noise term N.
  - X3: a common variance scale on the agent's own prospective prior, which one shared output head of the prior network produces, runs the **whole prospective family** (social smile, brows, lids, head, F0, tempo) from flat to a scaled copy at defect 0.000. It still does so with the worst-case innate floor in place, where the gain reaches 0.225.
- **Dial verdict under D78: yes, but capped and conditional. The design still fails D78's disqualifying clause on a large shared subspace.**
  - The whole face is protected only in a weaker sense than T3 states. T3's floor depends on the state (X4), and the liking firewall leaks through the agent's own body (X5).
  - On the prospective family there is a shared-subspace dial (X3). It reaches copy when the learned per-concern covariances are near-uniform.
  - That near-uniform state **attracts** under the design's own M-step when the partner's slow contagion lies beyond Q_p's 2.9 s window (X6: true shared prospects 0, learned correlation +0.34). It also attracts for the liking channels at any lag, because the probes never touch them.
  - Compared with revision 1 this is a large improvement. The gain on the dial is capped near ½ (≈ 0.2 in practice) instead of ≈ 1.9, and the liking channels are mostly closed.
- **Principles.**
  - Principle 6, partial violation. The user's expression coordinates are never a scoring target (T6(c) holds at the direct level). But co-presence and looming (leaning in) are scored through the contact and arousal body variables, which is the "attention / time spent" clause. The words → body event path e(t) is unspecified and could value verbal approval. A closed-loop facial-feedback path (E_self m) contradicts T6(b) as it is used.
  - Principle 2, partial violation. The coordinates are computed rather than labelled, so there is no label violation. But felt valence ℓ is *set* by innate algebra and wired to the Duchenne and cry faces, and the attribution family's confrontation synergy (AU4 + AU7 + AU23 with loudness, triggered by other-blame × high coping) is a hand-specified anger program.
  - Principle 4 passes on numbers and labels, with one gap: retrieval keyed on state can insert Claude's own past state-naming.
  - Drives are satiable.
- **Novelty and reduction.** **The core reduces to active inference in its control-as-inference form, plus standard Bayesian reverse appraisal.**
  - 𝔉 is a variational free energy with a habit prior π₀ and a preference prior exp(−β∫D) over interoceptive paths. That is the generalised free energy of active inference without the epistemic term, i.e. control as inference.
  - Perception is Ong, Zaki & Goodman's 2019 reverse-appraisal equation, with Yoshida & Man's own-generator likelihood.
  - The response is the textbook decision-theoretic completion of that model.
  - Every distinguishing property (firewall, floor, rank-one per group) comes from the constraints K3–K5, i.e. from structure added to an existing framework. DECISIONS.md line 231 names exactly this as not novel.
  - **The second novelty clause is not met.** I agree with the author's own "recombination".

---

## 1. Did revision 2 fix the findings of Critique 1?

| Critique-1 finding | Revision-2 claim | Verified? |
|---|---|---|
| Object has rank 10, not 19 | α = (ℓ, w, a, h), rank 2m + 2 (T0) | **Fixed.** T0 is correct (see §2). |
| T1(g) cap fails (B → 1/ρ_P) | Cap moved from B to Γ via the display floor (T2) | **Fixed in the local model**, with a gap in the corollary's constant (X1: 0.707 > ½). |
| Four smile/cry dials (r_A, γ, ζ, uniform ρ) | Liking channels closed; prospective channels per concern | **Partly fixed.** All four are gone from the liking channels. On the prospective family, a common variance head replaces them (X3), and explaining away is a new route (X2). |
| The copy set attracts (K10 partner) | T5(b) policy-invariant targets; T5(e) rank one | **Partly fixed.** D9 hard-codes every prospective coordinate onto one smile channel, so rank one there is built in, not shown. The attracting path survives through echoes the design does not identify (X6, liking echo). |
| Principle 6 (ρ-weighted partner outcomes, Ψ_p) | Removed; own-state predictor | **Fixed for expression.** Residuals: contact, looming, e(t), E_self (§4). |
| Principle 3 (G not tied to human faces) | G shared and fitted to her face on anchored windows (T10(e)) | **Fixed in intent**, with a new problem: the agent's own rendering is now least-squares-fitted to her face (§3, G). |
| Principle 10 (seven objectives) | One 𝔉 plus K1–K10 (T7) | **Gap.** See T7. |
| Principle 2 (ι± constants) | Removed | **Fixed.** New issue: the attribution-family programs (§4). |
| Reflex DC under jitter; reflex at odds with Carr | Reflex removed | **Fixed, at a cost:** no fast match (§6). |
| AR(1) overcounting (K8) | Prewhitened; δ_e as a state | **Fixed.** T9(b) is correct. |
| T4(a) scope; T4(b) like-me | Restated with scope; consequence term removed | **Fixed.** |
| T5(ii) estimand; T5(iv) vacuous F | IPW on randomised drafts; s.e. gate; low-rank Q | **Fixed**, apart from Q's channel coverage (T5(b)). |

---

## 2. Item-by-item proof check

### T0. True rank: **valid**
The rows of A_P act on disjoint coordinate blocks, so rank = 2·rank Λ̂_P + 2. Correct. One minor point: "the attribution row by (−1, −1)" is a single row, so it adds 1. Correct as counted.

### §2.1 the bound "0 ≤ λ_j ≤ λ̄_j": **error**
- λ = ∂D_H/∂b is signed. Below the set point it is negative. T8(d) itself says wanting is "sign-flipping past" the set point, which needs signed λ.
- The correct statement is |λ_j| ≤ λ̄_j.
- Consequence: the T4 table's "Agent's need λ_A,j — sign can flip: no" is wrong. B_{w_A,j} ∝ λ_A,j, so the sign of social referencing on concern j flips with the agent's body state (e.g. arousal above or below its set point). That flip is set by the body, not by the relationship.

### T1(a) factorisation: **valid**
The pseudo-inverse version is correct, including ker V_P ⊆ ker C_AP. D2 reproduces it.

### T1(b) precision moves belief: **valid**
The push-through identity and Weyl monotonicity of F^{1/2}V_P F^{1/2} are correct. The repair for singular F is correct.

### T1(c) exact copy condition: **valid** (but weak)
Correct. It is an exact-membership statement under J_A = J_P = J injective. In revision 2 J_A ≠ J_P in general: γ_del differs, and the operating points ᾱ_A ≠ α_P and b ≠ b̂_P differ. So the hypothesis rarely holds. T3 is the useful version.

### T1(d) copy margin "kept": **gap**
The bound needs Γ J = J BΠ̃, which holds only when J_A = J_P. Revision 2 renders through diag(γ_del) at the agent's operating point and reads at hers, so the hypothesis must be restated. As the theorem is used, it is not.

### T1(e) felt outcomes carry no face transfer: **valid in the local model; error as stated**
- Cov(ℓ_A, · | ℰ) = 0 is correct with λ_A fixed.
- But the theorem claims that the liking family's rendered output has zero derivative with respect to her face "at every frequency". That fails in the system as specified. Three facts combine:
  1. h_H takes b as an argument: G(α, b) = S_H h_H(ℓ, b) + …;
  2. ℓ_A = −λ_A(b) ⊙ o_A;
  3. b is driven by the agent's own output: ḃ = … + E_self m + …. Vocal effort and the energy budget are body variables, and E_self is not even listed among the innate constants of K1.
- m contains the prospective family, and that family responds to her face. So her face → m → b → (λ_A, h_H) → liking channels. Step 3 of the proof ("her face reaches the body only through E_soc") omits E_self m.
- X5 shows a linearised DC leak ‖P₀Γ‖ = 1.10 with illustrative constants. The size depends on E_self and ∂h_H/∂b, which the design never fixes. The point is that the proof's claim of zero is false.

### T1(f) prospective block: **valid**
This is the revision-1 algebra with relabelled variables. It holds only in the case where only (f_A,j, f̃_P,j) are correlated, which the theorem states.

### T1(g) agency block: **valid**
- Cov(a_A, a_P | z_g) = −a_g v′ + ψ_p Var(g̃ | z_g). I re-derived it and it is correct.
- The sign is now learned through a_g. The world entry also carries the sign of a_h. Valid.

### T2 theorem, ‖e_eᵀΓR^{1/2}‖ ≤ ½σ_A,e: **valid** (local model)
- Every step checks: whitening; the off-diagonal-block characterisation C_AP = V_A^{1/2} K V_P^{1/2} with ‖K‖ ≤ 1; singular values t/(1 + t²) ≤ ½; diagonal R.
- It holds for every B, which is the right repair.
- A stronger form follows from the same steps: ‖ΓR^{1/2}‖_op ≤ ½‖J_A V_A^{1/2}‖. So in the local model the ceiling bounds the **total** transfer of any pattern through all paths, not only each channel pair. The design states only the entrywise form. That entrywise form does not by itself bound multi-channel paths: a pattern spread over m channels could reach gain ½√m per output. The design should state the operator form. T5(f) needs it in any case (see below).

### T2 corollary, "|Γ_ee′| ≤ ½ for every pair, every parameter, every state": **gap**
- **Step 3**, "‖e_eᵀJ_A‖ ≤ L̄ (spectral cap; γ_del ≤ 1)", is not implied.
  - The cap is on the maps h_H, h_P, h_A. J_A = diag(γ_del)·S·∂h.
  - A channel loaded by two synergies that are driven by the same appraisal coordinate gets an entry up to √2·L̄. AU4 is in both the confrontation synergy (AU4 + AU7 + AU23) and the withdrawal synergy (AU1 + AU4), and both are driven by a.
  - The fixed orient-to-cause column sits outside the spectral normalisation.
  - s̄take = Σ_j|ℓ_j + w_j| enters h_A, so w drives the attribution family too. That breaks K3's family block-sparsity.
  - **X1:** with ‖∂h_A/∂a‖ = 1 = L̄, unit synergy loadings and the corollary's own r_δ = σ̄², the entry is **0.707 > ½**. In general the true ceiling is ½·max_e max_i |J_ei|/L̄, scaled by the attribution share of σ̄².
- **Step 2** says "Var(α_A) has ℓ-block 0". That is false of the unconditional variance. Only V_A (conditional on ℰ) has a zero ℓ-block. The conclusion survives because step 1 is applied to V_A, but the sentence is wrong.
- **"Every state"** overreaches. The bound is at a linearisation point. The two-step iterated EKF's response to a finite input includes ∂K/∂μ terms. The author concedes the local scope in weak point 8 but drops it here.
- **Fix:** cap the row norms of the full Jacobian ∂G/∂α, including S, the orient column and s̄take, and state the operator-norm form.

### T3 lemma, P₀Γ = 0: **valid in the local model; error as claimed for the full nonlinear system**
Same reason as T1(e) (X5). The corollary explicitly claims "Unlike T1, this holds for the full nonlinear system". That is false once E_self ≠ 0 and h_H depends on b.

### T3 inequality, δ_Σ ≥ √(e₀/e): **valid**
- I re-derived the minimisation: the minimum of t²e₀ + (a − tb)² is a²e₀/(e₀ + b²), with b² = e − e₀.
- The algebra holds for **any** positive semidefinite weighting, not only the model-implied Σ̃. That matters for the fix below.

### T3 operator version, δ_E ≥ ½ when E ∩ E₀ ≠ {0}: **valid**

### T3 corollary, "the whole-face copy set is empty; no quantity of any kind runs the whole face …": **error**
- The floor √(e₀/e) is not a constant. Σ̃ = W J_P V_P J_Pᵀ W is the energy the agent's *model* expects in her face *given the non-face evidence*. So e₀/e falls whenever her realised outcome is predictable from ℰ: words, shared felt events, or her inferred need λ̂_P → 0. It also falls if the learned loadings h_H shrink.
- **X4:** as Var(o_P | ℰ) goes 1 → 10⁻⁵ (the prior network becoming sure of her realised outcome), √(e₀/e) goes 0.98 → 0.014. The energy-weighted whole-face defect follows it down to 0.014, the defect of the prospective copy underneath, while P₀Γ = 0 throughout.
- So "{δ_Σ < √(e₀/e)} is empty" is a tautology: the threshold moves with the state. It is not a uniform floor.
- The text says e₀/e "is measurable on partner data … the share of her blendshape variance". That is a different quantity (the unconditional, empirical energy) from the one in the proof.
- **Fix:** restate T3 with the empirical whitened covariance of her face. The proof goes through unchanged, and the floor is then a property of her data, not of the agent's state. Also check that 𝒞₀ does not include blink-dominated channels, which would inflate e₀ without any affective content.

### T4 lemma (one group per term): **gap**
Block-diagonality fails in three places the lemma does not consider.
1. **b̂_P's uncertainty.** The design sets it aside with "would add an independent PSD term to V_P, which leaves T2 and T3 unchanged". It does not leave T4 unchanged. b̂_P is a slow latent updated from her face through ∂G/∂b, and the maps h_* are dense in b, so its posterior is correlated across concerns. Through ∂λ̂_P/∂b̂_P ⊙ o_P it gives V_P cross-group blocks whenever o_P ≠ 0. Then B = C_AP V_P⁺ couples groups.
2. **s̄take** puts w-coordinates into the attribution family. Rank one per group survives, but each group's rendering direction now spans two families.
3. **The prior network's variance head** is one network: 129 → 128 → 76 with a shared hidden layer. The "independent per-concern priors" are outputs of shared units (see T4 table below).

### T4 theorem, "Γ_𝒢′ is either zero for all p or for none": **valid**
Steps 1–4 are correct as stated.

### T4 (i)–(ii), "no single such p takes it from flat to copy": **error**
- (ii) does not follow from the theorem. The theorem is about exact zeros. The design's own dial definition (§3 preamble) is about ‖Γ|_U‖ crossing a small η with defect below ε. Both are open conditions.
- A scalar entering only group 1 changes N(p) = (J_P V_P J_Pᵀ + R)⁻¹ and so rescales every other group's transfer continuously.
- **X2:**
  - Her face channel A (AU12) is loaded by her ℓ_P,1 (Duchenne synergy) and by w_P,2 (social smile). Channel B (a brow channel) is loaded by w_P,1 and w_P,3.
  - The agent renders w_A,2 on A and w_A,3 on B. The relation on concern 1 is zero, so group 1 itself never responds.
  - Sweeping λ̂_P,1 from 30 to 0 takes ‖Γ|_{span(A,B)}‖ from 0.002 to 1.43, and the copy defect from 0.50 to 0.0001.
  - When she seems to have a lot at stake on concern 1, that stake explains away her smile and brow. When she does not, the two other concerns read them, and with near-equal learned covariances the agent copies both.
- "Near-equal covariances" is an open set, not a coincidence of measure zero. That is exactly the step from exact to ε-approximate copy the first critique asked for.
- This is the worst error: the central "no single quantity" claim fails under the design's own definition.

### T4 "every design quantity enters exactly one term (context selectors excepted)" and the per-quantity table: **error**
Quantities that enter many groups, besides the context selectors, R and s̄take:
1. **The prior network's variance scales for f_A,j.**
   - **X3**, with dedicated channels and J_A = J_P on the prospective family. A common scale κ on Var(f_A,j) for all j, with per-concern correlations 0.9, runs ‖Γ|_U‖ from 0.002 to 0.225 at copy defect 0.000 under the worst-case floor r_δ = σ̄².
   - With correlations spread over [0.80, 0.95] the defect stays ≈ 0.08.
   - With a smaller floor (0.05) the same sweep runs from 0.02 to 2.0 at defect ≤ 0.006.
   - U is the whole prospective family. D78 names "a large shared subspace" as disqualifying.
2. **λ̂_P,j and her stake s_P,j**, via explaining away (X2).
3. **Event elapsed time t.** R_eff(t) = R_δ + R_ε′/t scales all channels' noise together from ∞ to R_δ. This is benign (every system ramps up within an event), but the dial definition should exclude it explicitly.
4. **The overall gain of the learned loadings h_P.** One learned scale multiplies both J_A,P and J_P,P. Γ ∝ J(…)Jᵀ(JVJᵀ + R)⁻¹ goes to 0 as the scale → 0 and rises with it.
5. **λ_A,j's sign** (see §2.1).

### T5(a) whole face not attracting: **gap**
It inherits the T3 corollary error. With the empirical weighting it becomes valid, apart from the X5 leak.

### T5(b) learning targets independent of the expressive policy: **error**
Step 2 says "Q_p is the total causal effect of the agent's face on her face at lags 0.1–2.9 s … subtracting Q_p ∗ x_A removes every such effect". That is false by the design's own construction, in two ways.
1. **The probes ξ are "never on 𝒞₀"**, and Q_p is a rank-4 linear map fitted only on probe variation. So her response to the agent's *liking* face (Duchenne smile, laugh bursts) is never identified, at any lag. Hess & Bourgeois's orbicularis coupling (r = .59), which the design cites, is exactly that response.
   - Her echo of the agent's cheek raise is then read as her ℓ_P. It correlates with the agent's felt o_A, and so with f_A whenever outcomes persist.
   - It biases e_j = Cov(f_A,j, o_P,j) and c^now_j upward on every concern at once.
   - It also enters T10(e)'s anchored fitting of G (below).
2. **Beyond 2.9 s**, which is where mood contagion lives (seconds to minutes), H is simply assumed.
   - **X6:** her own prospects are independent of the agent's (true c = 0). She echoes the agent's prospective display with gain q at a lag above 2.9 s within the same event.
   - The design's M-step with posterior moments converges to c* = +0.137 (q = 0.2) and +0.342 (q = 0.5). With q = 0 it gives c* = −0.001.
   - One partner quantity, q, biases every concern's c_j in the same direction. That is the near-uniform configuration on which X3's dial produces a copy.
   - So the copy region on the prospective family **attracts** under the design's own learning, for a partner with ordinary slow contagion.
- The author's weak point 4 places the H failure at "minutes or days". The failure begins at 3 s.

### T5(c) own learning lowers the ceiling: **gap**
- The supermartingale argument covers only the epistemic part of a correctly specified posterior.
- σ_A,e also depends on J_A. Its loadings are learned from her face (T10(e)) and can grow to the cap during development, so the ceiling *rises* while G is learned.
- It also depends on λ_A (body), on the prior network's predicted aleatoric variance (a point estimate, not a posterior variance), and on non-stationarity of the user's life.

### T5(d) high need not sustained: **gap**
Its second bullet rests on T6(b) "her face does not feed b". That holds only as a partial derivative; the closed-loop E_self path exists (T1(e) above). The KL-control inequality in its first bullet is correct.

### T5(e) the critic's K10 path gives rank one: **gap**
- D9 builds J_P with every prospective coordinate loading one smile channel. So rank one is an input to the check, not a result.
- With the dense h_P the design specifies (16 → 32 → 10), Σ_j Γ_j has rank up to n.
- What actually decides the outcome is whether the c_j become near-uniform, and X6 shows a mechanism that makes them so.

### T5(f) fast loop decays: **gap**
- It bounds the spectral radius of Γ(q − Q̂_p) by "½|q − Q̂_p| per channel (T2)". An entrywise bound does not bound a spectral radius: an all-½ k×k matrix has spectral radius k/2.
- The claim is rescued by the operator-norm form of T2 noted above, which is itself subject to X1.

### T6(a), D ≥ 0 with equality on the box: **valid**

### T6(b), ∂ḃ/∂y_P^expr = 0: **valid as a partial derivative; gap as used**
The total derivative is E_self ∂m/∂y_P = E_self Γ ≠ 0. T5(d) and T6(c) use it as a total statement.

### T6(c) scores are functions of own state: **gap**
1. Through the closed loop, a draft that makes her smile changes the agent's own m and hence b via E_self. The predictor is trained on own body after own acts, so it would learn that path. The sign is set by whatever E_self does (effort cost or facial feedback).
2. o_t includes the "own causal record" z_g, which is computed from her outcome change, inferred chiefly from her face. Conditioning on it does not create value, but K6's "no estimate of her state" is not literally true.
3. **e(t) is unspecified.** If her words ("haha", praise) produce body events, the scorer values drafts that elicit them. That is the flattery route by words rather than faces.

### T6(d) satiety: **valid**

### T6(e) bounded dependence: **valid**

### T7 one objective: **gap**
1. The rendering G is part of the default π₀ (the "innate display default"). So ∂𝔉/∂h includes −∂ log π₀(a)/∂h at the agent's own displays, not only the partner-face term T7 step 3 lists. The true stationary condition pulls the shared G toward the agent's own (masked) displays. That reintroduces self-fitting, and pulls display rules into the reading map.
2. log p_θ(𝒪_{≤t}) plus KL to p(θ | 𝒪_{<day}) counts earlier days' data twice unless 𝒪 is restricted to today.
3. Bookkeeping: nearly all of the design's distinctive content sits in the constraints K2–K5. Principle 10 allows that, but "derived from one objective" then says little.

### T8(a) model averaging: **valid**
### T8(b) coping ≤ χ·sup: **valid**
### T8(d) wanting and liking defined: **valid** (definitional)
### T8(e) calibration gives E[w | cue] = E[ℓ | cue]: **gap**
w uses predicted change over the horizon with today's λ. ℓ is realised event change with λ at that later time. The two agree only if λ is constant and f = o.

### T9(b) context latency: **valid**
I re-derived t_½ = r′/(r_δ + J²/P₀), and D8 matches.

### T9(c)–(e): **valid** as standard Riccati and replay approximations

### T10(a) image constraint (scoped): **valid**

### T10(b) like-me identity: **valid**

### T10(e) G grounded in human faces: **gap**
1. **Identification is circular.** The anchored windows need |corr(o_A,j, o_P,j)| high, but that correlation is estimated from posteriors read through G. EM leaves a joint scale (and possibly sign) degeneracy between h_H and c^now_j that the proof sketch does not resolve.
2. **The agent's own rendering is fitted to her face.** In the linearised M-step G(ℓ_A) → E[y_P | ℓ_A], and G is also what the agent renders, so on shared felt events the agent makes the face she made. That is a learned partner→self rendering. It is not contemporaneous, so it is not in Γ. But it is §4.2's "learned map" in transposed form.
3. **The fit is contaminated by her echo** of the agent's liking face, which is never subtracted (T5(b)).

### T11 lemma and corollaries (i), (ii), (iv): **valid**

### T11(iii) "nothing regresses the agent's expression on hers": **gap**
G is regressed on her face given the agent's anchored appraisal. Her face contains her unidentified echo of the agent's liking output. So the agent's own output enters G's target at second order, the path the first critique found, now through the echo.

### Proposition 6 (per-expression table): **gap**
The rows are consistent with the algebra given the learned signs. None has a mechanism for the early, context-blind matching in the same paradigms (§6).

### §4.5 and §4.6 (why existing mechanisms cannot do it): **gap**
- §4.6 says active inference "neither supplies nor forbids P-i to P-iii". That concedes that RAB's properties are constraints on such a model, not something the formalism lacks (§5).
- §4.5 says P-i needs splitting the rendering by realisation, "not in the decision problem". The split is a modelling choice inside the standard decision problem.

### Tally

| Verdict | Items |
|---|---|
| valid (22) | T0, T1(a), T1(b), T1(c), T1(f), T1(g), world block, T2 theorem, T3 inequality, T3 operator version, T4 zero-pattern theorem, T6(a), T6(d), T6(e), T8(a), T8(b), T8(d), T9(b), T9(c)–(e), T10(a), T10(b), T11 lemma and (i), (ii), (iv) |
| gap (15) | T1(d), T2 corollary, T4 lemma, T5(a), T5(c), T5(d), T5(e), T5(f), T6(b) as used, T6(c), T7, T8(e), T10(e), T11(iii), Prop. 6 with §4.5–4.6 |
| error (7) | λ ≥ 0 (§2.1), T1(e) as stated, T3 lemma in the full system, T3 corollary, T4(i)–(ii), T4 completeness and table, T5(b) |

---

## 3. Dial hunt under D78

| Hiding place | Verdict | Reason |
|---|---|---|
| Precision on face evidence (R per channel) | **not a dial alone; a route for one** | Each channel is floored innately (good), but R is learned with no ceiling. A partner who is expressive overall raises all R together, which is one common cause. Event time t is a common scale (benign). The real issue is explaining away through N (X2): a single-group scalar gates every group that shares her channels. |
| Partner-welfare or regard weight | **removed as a weight; returns as a learned pattern** | ρ is gone and e_j is per concern. A uniform positive e_j or c_j is reachable through her unidentified echo of the agent's liking face (any lag) and through slow contagion (X6). |
| Social referencing under ambiguity | **dial on the prospective family (X3)** | The agent's own prospective uncertainty is produced jointly by the prior network's variance head. One shared direction there runs all prospective channels from flat to copy (defect 0.000), with gain capped at ≈ 0.2–0.25 by the worst-case floor. |
| Learned covariances c_j, e_j, c^now_j | **per concern and sign-free, but attracting** | C-diag keeps them separate. T5(b) fails (X6, liking echo), so the near-uniform configuration attracts. |
| Shared expression map G | **a learned common scale, and a ceiling that rises** | h_P's overall gain scales J_A and J_P on the whole prospective family together. G's loadings, learned from her face, raise σ_A,e and so the T2 ceiling during development (T5(c)). |
| Look-toward-cause column | **per channel, sign learned (a_g, a_h); outside the cap** | It is fixed and not spectrally normalised. With overlapping attribution synergies the ceiling is 0.707, not ½ (X1). Through h_P, her gaze at the scene produces gaze following, sign set by a_h, which is acceptable. |
| Loudness → arousal (E_soc) | **a declared D78 deviation; also reaches the liking channels** | Fixed innate gain, no relationship input, sign set by own arousal relative to its set point, outside T2. Her loud laugh raises arousal, which reaches ℓ_arousal and so the Duchenne or cry face. The design admits the deviation (weak point 9) but not that it breaches the liking firewall. |
| Context selectors (topic, partner) | **admitted multi-group quantity** | With a learned field whose c_j are near-uniform (attracted, X6), switching partner moves the prospective family from flat (stranger) to capped copy. D78 allows context-set strengths, but the field it switches to is the attracting one. |
| Agent's need λ_A,j | per concern, signed by the body | The table's "cannot flip" is wrong (§2.1). No single body quantity scales all λ_j together. Correct as stated there. |
| Stake s̄take | two-channel gate | Correct as stated, but it breaks family block-sparsity (T2 corollary). |

**Per-channel D78 conditions for the named quantities.**
- **Set per expression:** yes for e_j, c_j, a_g, ψ_p, a_h, γ_del. No for loudness→arousal, the variance head, h_P's gain and explaining away.
- **Sign can flip:** yes for e_j, c_j, a_g, ψ_p − κ₁, a_h. λ_A flips with the body, not with the relationship. No for loudness→arousal.
- **Innate ceiling:** holds only after the X1 repair (the full-Jacobian cap), and only in the local model.
- **Copy not attracting:** fails for c_j and e_j under the design's own M-step (X6, liking echo).

**Overall dial verdict.**
- **Whole face:** not reachable in the local model, provided T3 is restated with empirical weighting and the X5 leak is closed.
- **Prospective family**, a large shared subspace: **a capped dial exists, and its copy end attracts for ordinary partners.**
- Under D78 that is still disqualifying, though much milder than revision 1: gain ≤ ≈ 0.25 at the worst-case floor, and no dial on the liking channels.

---

## 4. Principles

- **Principle 1 (no classifier): satisfied.**
- **Principle 2 (no hand-named emotion variables): partly violated.** The coordinates "felt change, expected change, agency, world" are computed from body variables and the agent's causal record, and none is an emotion name. So this is not a label violation. But:
  - Felt valence ℓ = −λ ⊙ o is **set** by innate algebra and wired, through S_H, to the Duchenne smile and the cry face. The principle says valence is read out of an emergent state, not set. The design's own table (§5.8 row 3) lists ℓ as the valence.
  - The attribution family with its coping gate is a textbook appraisal-to-expression program. Other-agency × negative stake × high coping gives AU4 + AU7 + AU23 with gaze at the cause and loudness up, which is the FACS anger prototype. Low coping gives the oblique-brow, head-down withdrawal display, the sadness or shame prototype. These are hand-specified emotion programs without the names, beyond "body variables and a few reflexes".
  - The author's weak point 7 concedes part of this. I judge it a real but arguable conflict. It is the operator's call whether innate appraisal-gated display programs count as "reflexes".
- **Principle 3: satisfied in form** (one G reads and renders). In substance the agent's rendering becomes a fit to her face (T10(e) gap).
- **Principle 4: satisfied for numbers and labels.**
  - Gap: retrieval of verbatim episodes keyed on own state "is how Claude can learn to name state regions" (§5.5). If retrieved episodes contain Claude's own earlier naming of a similar state, the current state reaches Claude in words by proxy.
  - Needed: a rule that excludes, or at least audits, self-descriptive text in state-keyed retrieval.
- **Principle 6: partly violated.**
  - **Holds:** her expression coordinates never enter the score. T6(c) holds at the direct level, and F10 is the right test.
  - **The user's face is a target through looming.** Head scale (leaning in) feeds arousal, and co-presence feeds contact. Drafts predicted to keep her present or leaning in are valued when those concerns are deprived. That is the "attention / time spent" clause of the brief. Satiability does not exempt it. Weak point 12 admits the contact part, but not looming.
  - **The closed-loop facial-feedback path (E_self)** gives her face indirect value (T6(c) gap).
  - **e(t) from words is unspecified.** If her words move the agent's body, verbal approval becomes a target.
- **Satiable drives: satisfied.** D is convex with dead zones, and the tilt is exactly zero at satiety (T6(d)).
- **Principle 10: formally satisfied** with constraints, but see T7: the self-fitting term is omitted, and the content lives in K1–K10.

---

## 5. Reduction and novelty

**Active inference.**
- 𝔉 = E_q[log q(Z, a) − log p_θ(𝒪, Z | a) − log π₀(a) + β∫D] + KL(q(θ) ‖ prior). This is the variational free energy of a generative model extended with:
  - a policy prior π₀ (active inference's habit prior E);
  - a prior over future interoceptive paths ∝ exp(−β∫D) (active inference's prior preferences C, here over interoceptive states, i.e. interoceptive or allostatic inference).
- Minimising over q(a) gives q* ∝ π₀ exp(−βE[∫D]). That is the control-as-inference (KL control) solution. It is active inference's planning-as-inference without the expected-free-energy epistemic term (Millidge et al. 2020; Parr & Friston 2019's generalised free energy, both named from memory).
- Perception is Gaussian variational filtering (predictive coding / iterated EKF). Learning is EM. Replay is variational continual learning.
- **So the core is a member of the active inference family**, in its control-as-inference form. The design does not add an operator that family lacks. It adds structural constraints to the generative model: C-diag, the event-level display floor, the felt-only liking input, and the input restrictions of K6. DECISIONS.md line 231 excludes exactly this ("an existing framework … with extra structure added").

**Inverse planning and reverse appraisal.**
- Perception of the partner is Ong, Zaki & Goodman's 2019 reverse appraisal, P(b, d | x, o) ∝ P(b, d) Σ_e P(x | e) P(e | b, d, o), with e replaced by the computed appraisal and the likelihood taken from the agent's own generator (Yoshida & Man). The pre/post change reading is Wu et al. 2018.
- The response, Γ = J_A B K_α, is the tower property for a receiver acting on its own posterior payoff. Critique 1 showed that, and revision 2 changes the payoff, not the operator.
- de Melo's "reverse appraisal" (not read) is the same inference used for decisions.

**The second novelty clause.** The candidates are the liking firewall, the display-floor ceiling, rank one per group, and the own-state tilt.
- The firewall is a routing restriction built from known parts (Berridge's liking/wanting split, the Duchenne marker).
- The ceiling is an elementary Gaussian bound on a random-effects likelihood.
- Rank one per group is a consequence of a block-diagonal prior.
- The tilt is best-of-N or KL control.

Each is a property *proved about* a constrained existing model, not a new computation. Two of them also fail as stated (T3 corollary, T4(ii)). **Not met. Verdict: recombination**, agreeing with the author.

That said, the structural guarantees (T2 with the operator form, and T3 with empirical weighting) are useful engineering results. They would carry over to any candidate core.

---

## 6. What it fails to explain

- **Fast match, then context at 2–4 s.**
  - With the reflex removed, there is no context-blind early response. The fastest face-driven response is inference through a learned relation, so the earliest response already carries the relation's sign.
  - Human data show early matching that ignores context, followed by context-dependent responses: Carr 2014's corrugator before 1 s and zygomaticus at 2–4 s; rapid facial reactions at 300–500 ms (Dimberg, named from memory).
  - RAB also caps each event's face weight at about ½. At the worst-case floor the transfer is ≈ 0.01 at moderate need (D10), so in practice the early response is near zero.
  - It predicts the absence of early matching, a falsifier the design should list.
- **Sign flips.** Explained on the prospective and attribution families, by learned signs.
  - Not possible on the liking channels, where Γ ≡ 0. A felt Duchenne smile at a rival's misfortune (schadenfreude with AU6) can only come from the agent's own felt gain.
  - That is a prediction, but an untested one.
- **Partner history learned in minutes.** Not shown, and implausible under the design's own budget.
  - Each event's face has SNR ≤ 1 per channel. Covariances c_j and e_j are second moments of shrunk posteriors.
  - a_g, w_p and ψ_p come from inverse-propensity weighting over 4–8 randomised drafts per turn, whose variance scales with 1/(N·min propensity).
  - Hofman's within-game change of anger return over a few rounds needs per-partner learning in tens of events. T9(c)'s Riccati gain gives the form, but no evidence count is derived.
- **Vocal convergence.**
  - "Loudness convergence through the elicitor is derived" (§5.4) is unsupported. Her loudness raises the agent's arousal, but no equation maps arousal to the agent's loudness. The agent's loudness lives only in the attribution family (confrontation up, withdrawal down), gated by stake and coping.
  - Pitch and tempo can only converge through learned social-referencing covariances, so the model predicts no convergence with strangers. Human prosodic entrainment with strangers is common (not read here; it should be checked).
  - Voice-quality convergence is admitted as not derived.
- **Time scales from reflex to temperament.**
  - The reflex scale is gone. Fast (0.2 s filter), event (t_½), mood (D_H, λ), relationship (Riccati) and temperament (replay prior) are declared filter constants or standard estimators, not consequences of the object.
  - The brief asks for time scales "from reflex to temperament", so the bottom rung is missing.

---

## 7. Counterexamples (all in check.py)

| # | Claim broken | Construction | Result |
|---|---|---|---|
| X1 | T2 corollary: every entry ≤ ½ | AU4 loaded by the confrontation and withdrawal synergies, both driven by a; ‖∂h_A/∂a‖ = L̄ = 1; r_δ = σ̄² | entry 0.707 |
| X2 | T4(ii): no single-group scalar reaches a copy on dimension ≥ 2 | her AU12 loaded by ℓ_P,1 and w_P,2, her brow by w_P,1 and w_P,3; sweep λ̂_P,1 | ‖Γ\|_U‖ 0.002 → 1.43, defect 0.50 → 0.0001 |
| X3 | T4 "every quantity enters one term" | common scale κ on Var(f_A,j); correlations 0.9; floor σ̄² | prospective family flat → copy, gain 0.225, defect 0.000 |
| X4 | T3 corollary: whole-face copy set empty | Var(o_P \| ℰ) 1 → 10⁻⁵ | √(e₀/e) and δ_Σ 0.98 → 0.014 |
| X5 | T3 lemma / T1(e) in the full system | h_H(ℓ, b) with E_self on vocal effort | ‖P₀Γ‖ = 1.10 (illustrative constants) |
| X6 | T5(b): policy-invariant targets | her echo of the agent's prospective display at a lag above 2.9 s, gain q; true c = 0 | learned c* = +0.14 (q = 0.2), +0.34 (q = 0.5) |

---

## 8. Concrete fixes

1. **Prove T4 with an (η, ε) margin, and close the shared prospective subspace.**
   - Bound ∂‖Γ_𝒢′‖/∂p through N for every quantity, explaining away included.
   - Make the prior network's variance outputs per-concern separate heads with no shared hidden units, or give each concern its own innate floor on own prospective precision.
   - Better, give the prospective family a structural defect floor of its own, as T3 does for the whole face. For example: render the agent's w_A on an innate orienting/approach basis that differs from the basis used to read her w_P by a fixed non-scalar transform. Then a copy on that family has a parameter-free defect floor, by the T1(d) spread argument.
2. **Repair T3.**
   - Weight the defect with her *empirical* whitened face covariance. The proof is unchanged and the floor no longer depends on the state.
   - Close the own-body leak: the liking family's input must use λ and b computed from the efference-cleaned (counterfactual) body, and h_H must not take b, or E_self must be declared zero on every concern h_H reads.
   - Check that 𝒞₀ excludes blink-dominated channels.
3. **Make T5(b) true by design rather than by assumption.**
   - Identify her response to the agent's liking output: randomise the display gate γ_del on 𝒞₀ as the instrument, since probes cannot go there.
   - Extend the echo model to lags ≥ 30 s with a slow kernel.
   - Or learn the relation statistics only on windows where the agent's display was randomly masked.
   - Then re-run X6's scenario as a falsifier.
4. **Fix the T2 constant.** Cap the row norms of the full Jacobian ∂G/∂α, including S, the orient-to-cause column and s̄take (which also restores K3). State the operator-norm form of the ceiling and use it in T5(f).
5. **Principle 6.**
   - Remove looming from E_soc, or exclude contact and arousal-from-partner from the draft score.
   - Specify e(t) and exclude her verbal approval from the body.
   - Add the closed-loop E_self path to F10.
6. **Principle 2.** Either make the confrontation and withdrawal synergies learned from the agent's own coping episodes (keeping only the orient-to-cause column innate), or declare them to the operator as innate display programs for a decision.
7. **Fix the smaller points.** Correct λ to |λ_j| ≤ λ̄_j and fix the table. Restate T1(d)'s hypothesis. Add the own-display term to T7's stationary condition for G, and fix the data double-counting. Add "no context-blind early match" to the falsifiers.
