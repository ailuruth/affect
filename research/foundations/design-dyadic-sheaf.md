# Design: the dyadic contingency sheaf

Written 2026-11-25 for the Q16 cycle under the Q17 standard. Isolated design; it does not draw on other designs written this cycle.

Read for this design:
- In full: brief.md; research/questions.md Q16-Q17; foundations/designs.md; foundations/known-failures.md; the syntheses on mimicry in context, coordination, face development, emotion elements, new mechanisms, mathematical objects and memory/replay; the notes on Hansen & Ghrist 2019 and 2021, Bodnar et al. 2022, Altafini 2013, Parsegov et al. 2017, Butler & Randall 2013, Ray & Heyes 2011 and Cook et al. 2014.
- Primary sources I read myself for the results this design relies on:
  - Hansen & Ghrist, "Opinion dynamics on discourse sheaves", arXiv 2005.12798 v1: §3-§5 (Theorem 5.1 and its proof), §8 (equations 8.1-8.3, Theorem 8.1 and its proof, Example 8.2), §9 (Theorem 9.3 and its proof), §12 (Proposition 12.1 and the "agreement to disagree" passage).
  - Bodnar et al., "Neural sheaf diffusion", arXiv 2202.04579 v4: Propositions 3-5 and Lemma 6, with the proofs in the appendix.
- Psychological claims are cited through the project's notes, which record what each author read. Where a note read only a secondary source, I say so.

Small numeric checks of my own equations are in §3.9. They check algebra only. They are not results.

---

## 1. Intuition (one page)

The agent holds two things in its own body's coordinates:
- its own state x (body variables plus a learned latent);
- a reading z of the partner, also in the agent's own coordinates. It is the state the agent's own body would need in order to make the face and voice it is seeing and hearing.

The agent makes faces and voices through a map A from state to expression. It reads the partner through the same A, run backwards (the adjoint). This is the "reads the other through its own body" principle, and §3.4 states it as an equation.

Between "me" and "the partner as I read them" there are **two different links**, learned from two different contingencies:
- **Contingency link R** ("what they do after I act"). It is learned from pairs of the form "I was in state x, and about τ seconds later they looked like z". Its learning rule is that of associative sequence learning: being imitated teaches R ≈ identity, and crossed experience teaches a crossed R. Because a sheaf link pulls both ways, R also pulls the agent's state toward the state whose expected response is what it now sees. That pull is fast mimicry. It is learned, so it can be matching, crossed or absent channel by channel.
- **Consequence link W** ("what their state does to my body"). It is learned from pairs of the form "they looked like z, and then my own body variables changed by Δb". Its target is the agent's own innate body sensors, which no display can fake. Through W a rival's smile can come to mean a loss to me, and a partner's distress can come to mean that my body mobilises.

Because there are two links between the same two vertices, the pair forms a **loop**: from me to them through R, and back to me through W. The loop's round-trip operator, the monodromy M = W R, is a property of the relationship that no change of coordinates removes. A single link, the case the earlier sketches and the sheaf literature analyse, has no loop. That is why every single-link design turned out to be "a gain on a copy" or "a copy in a flipped frame".

Four consequences, each proved in §3:
1. **No dial, and what replaces it.** How much of the partner reaches the agent has a structural ceiling ϑ < 1, and a temperament anchor always remains. Copying the partner is therefore impossible for every learned map, with an error at least (1−ϑ) times the distance between the partner and the agent's temperament. Which way the agent responds (matching, countering, ignoring), channel by channel, is set by the learned maps. No coordinate change can turn a counter-response into a copy, because the agent's face and the partner's face share the same physical channels, which pins the frame.
2. **Mimicry and coregulation are different loops.** The R loop alone is always self-reinforcing (contagion; Butler & Randall's "morphogenic" class) for every possible R. Damped oscillation back to a set point (their "morphostatic" coregulation) requires the W loop with a negative round trip. So lesioning one link and then the other should dissociate fast mimicry from coregulation.
3. **Time scales come from the shape of the graph.**
   - A reflex arrives in order t¹.
   - An emotional response, which passes through the partner reading and the agent's own state, arrives in order t³.
   - A newly inferred context arrives in order t⁴.
   - A shared mood persists for a time that grows as (1 − μ)⁻², where μ is the loop's round trip. The closer the relationship's loop is to closing on itself, the longer a shared state outlasts the partner.
   - Temperament lives in a private subspace that the partner cannot reach.
4. **Emotion is structure, not a variable.** The agent has no emotion variable. What exists is:
   - the state x (64 dimensions);
   - the obstruction: the part of the current dyadic disagreement that no change of the agent's own state can resolve, split by which link carries it;
   - the relationship's loop spectrum (eight complex numbers per partner).

   Valence and arousal are read out of the body potential and the obstruction. They are never set.

What this design is not: a new computational primitive. The fast core at a fixed relation is a quadratic energy on a cellular sheaf, which is a Gaussian Markov random field, and its learning rules are delta rules. §7 gives the verdict.

---

## 2. The precise mathematical object

### 2.1 Spaces

| Symbol | Space | Meaning | Size in the build |
|---|---|---|---|
| S = B ⊕ L | ℝⁿ, inner product ⟨·,·⟩ | the agent's stalk: innate body coordinates B ≅ ℝ^{n_b} and learned latent L ≅ ℝ^{n_ℓ} | n_b = 8, n_ℓ = 56, n = 64 |
| C_B : S → B | coordinate projection | selects the body block (fixed, innate) | 8 × 64 |
| O = S | ℝⁿ | the partner stalk: the partner's state *in the agent's own coordinates* (Principle 3) | 64 |
| E = ⊕_{c=1}^{C} E_c | ℝ^k | expression space: face blendshapes, head pose and gaze, voice prosody, split into C channel groups | k = 66, C = 10 |
| y(t) ∈ E | boundary data | the partner's observed face and voice features at 30 Hz | |
| f(t) ∈ E | boundary data | the agent's own expression as sensed back (rendered face, synthesized voice) | |
| b(t) ∈ B | boundary data | the agent's sensed innate body variables | |
| b* ∈ B | constant | innate set points | |
| H ⊆ ℝ^m | relation states | slow relation state h; a prior h̄_p for each partner p | m = 16 |

The innate body variables are regulated quantities, not emotions (Principle 2). In the build they are:
- energy (compute and fatigue budget);
- activation;
- contact (time since being addressed and answered);
- predictability (running own-prediction error);
- integrity (abrupt or loud input);
- vocal load;
- novelty intake;
- rest.

Each has a set point and innate afferents (§5.2).

### 2.2 The base graph and the sheaf

Each agent holds a cellular sheaf F_h on a fixed multigraph Γ. The restriction maps depend on h.

**Vertices.**
- Interior: s (stalk S) and o (stalk O).
- Boundary, with values fixed by data: ŷ (stalk E, value y), f̂ (stalk E, value f), b̂ (stalk B, value b), ā (stalk S, value x̄_p, the temperament anchor for partner p) and ⋆ (stalk B, value b*).

**Edges and restriction maps.** Each edge e = u ∼ v has stalk F(e), maps F_{u⊴e} and F_{v⊴e}, and a weight Λ_e ≻ 0 (a precision).

| Edge | Joins | Edge stalk | Map from u | Map from v | Weight | Meaning |
|---|---|---|---|---|---|---|
| obs | o ∼ ŷ | E | A | I_E | Π | the partner, read through my own expression map |
| disp | s ∼ f̂ | E | A | I_E | Π_f | my own face and voice, sensed back (facial feedback) |
| ρ (contingency) | s ∼ o | O | R(h) | I_O | P | "they respond to my state x as R x" |
| κ (consequence) | o ∼ s | B | W(h) | C_B | Λ | "their state z means W z for my body" |
| sens | s ∼ b̂ | B | C_B | I_B | K_s | my body, sensed |
| anc | s ∼ ā | S | I_S | I_S | Γ_h | temperament anchor (stubborn parent, as in Hansen & Ghrist §7) |

**The display map A : S → E is the same on obs and disp.** This tie is Principle 3 made structural. A is the agent's own state-to-expression map, learned from its own mirror (§2.5). It is used both to express and to read.

The coboundary is (δξ)_e = F_{v⊴e} ξ_v − F_{u⊴e} ξ_u. The cochain is ξ = (x, z) on the interior, with the boundary values held fixed.

**The cycle.** ρ and κ are two distinct edges between s and o, so Γ has a cycle s →ρ→ o →κ→ s. Since the stalks differ (κ lands in B), its round trip is defined on the body:

  M_B(h) := W(h) R(h) C_Bᵀ : B → B,  the *body monodromy*;

and on the whole stalk:

  M(h) := C_Bᵀ W(h) R(h) : S → S.

A global section on the cycle (both edges exact) requires z = R x and C_B x = W z, i.e. (C_B − W R) x = 0. So the cycle admits a nonzero consistent state only where the loop closes.

### 2.3 Energy

For fixed boundary data and relation h, the sheaf Dirichlet energy plus the homeostatic potential is

(E) ℰ_h(x, z) = ½‖A z − y‖²_Π + ½‖A x − f‖²_{Π_f} + ½‖z − R(h) x‖²_P + ½‖C_B x − W(h) z‖²_Λ + ½‖C_B x − b‖²_{K_s} + ½‖x − x̄_p‖²_{Γ_h} + U(C_B x) + V_θ(x).

Here ‖v‖²_Q := vᵀQv.
- U : B → [0, ∞) is the innate homeostatic potential: U(β) = Σ_i φ_i(β_i − b*_i), with each φ_i convex, φ_i(0) = 0 and φ_i ≥ 0. Satiable: it has its minimum at the set point.
- V_θ : S → ℝ is a learned potential on the latent (a small MLP). It is the only nonlinearity in the fast core, and its Hessian is constrained to satisfy ∇²V_θ ⪰ −σI with σ declared (§6).

The quadratic part is the weighted sheaf Laplacian energy of F_h with boundary (Hansen & Ghrist 2021, §5).

**Ceiling normalisation (a declared structural constant ϑ ∈ (0, 1)).** The anchor weight is not a free parameter. It is set from the partner-edge weights:

(N) Γ_h := γ₀ I + ((1−ϑ)/ϑ) · (‖Rᵀ P R‖ + ‖Λ‖) I,  with γ₀ > 0 and ϑ = 0.5 in the build.

This is the sheaf form of Friedkin-Johnsen's "coupling condition" (Parsegov note: stubbornness tied to the influence weights). Its role is fixed by Theorem 1(b).

### 2.4 Fast dynamics

The fast dynamics are a gradient flow on ℰ_h with the boundary data as stubborn vertices (Hansen & Ghrist Theorem 5.1), plus a reflex path, a delay through the real partner, and the muscle layer:

(F1) ż = −α_z ∂ℰ_h/∂z    (perception; α_z ≈ 10 α, settles in about 100 ms)
(F2) ẋ = −α ∂ℰ_h/∂x     (state; 1/α ≈ 0.3 s)
(F3) ṁ = −β_m (m − σ_m( A_F x + Θ_r y + D u_del ) ⊙ (1 − g_inh)) ... see §5.4 for the two routes

Here:
- A_F is the face block of A.
- Θ_r is the innate reflex matrix. It is sparse and fixed, and its nonzero entries form a declared core: lip-corner pull to lip-corner pull, and brow-lowerer relaxation to lip-corner pull.
- m holds the muscle activations.

Written out:

  ∂ℰ/∂z = AᵀΠ(Az − y) + P(z − R x) − Wᵀ Λ (C_B x − W z)
  ∂ℰ/∂x = AᵀΠ_f(Ax − f) − RᵀP(z − Rx) + C_BᵀΛ(C_B x − W z) + C_BᵀK_s(C_B x − b) + Γ_h(x − x̄_p) + C_Bᵀ∇U(C_B x) + ∇V_θ(x).

The partner is real. Its face y(t) responds to the agent's expression with its own dynamics and latency, so the closed dyad is a delay system (§3.3c).

### 2.5 Learning (medium time scale: seconds to minutes, online)

Three delta rules (Rescorla-Wagner / least mean squares). Each target is a quantity that the agent's display cannot fake.

(L_A) Ȧ = η_A (f_sensed − A x) xᵀ
- A self-mirror pair: the commanded state and the sensed own expression. This is perfect contingency, which is how the self is singled out (Bahrick & Watson, via face-development synthesis).

(L_R) Ṙ_j-coefficients and h: d/dt R = η_R P (z_y(t) − R x̃_τ(t)) x̃_τ(t)ᵀ, projected onto the span of the basis {R_j} (§2.6)
- z_y := (AᵀΠA + Σ₀)⁻¹AᵀΠ y is the partner reading from the face alone, with no prior from R and no pull from x. This matters for Theorem 5.
- x̃_τ is a bank of exponential traces of the agent's past state, x̃_τ(t) = τ⁻¹∫_{−∞}^{t} e^{−(t−s)/τ} x(s) ds, with τ ∈ {0.3, 0.6, 1.2, 2.4, 4.8} s. R is fitted at the lag with the lowest residual.

(L_W) d/dt W = η_W Λ (Δb(t+τ_κ) − W z_y(t)) z_y(t)ᵀ,  with Δb(t+τ_κ) := b(t+τ_κ) − b(t)
- The target is the change in the agent's *sensed* body. W is updated τ_κ late, from a stored z_y(t).

Precisions (Π, P, Λ, K_s, Π_f) are running inverse residual variances of their edges. Each is diagonal and per channel. Each is floored and capped by declared constants.

### 2.6 Relation state (medium-slow) and partner priors (slow)

(H) R(h) = R₀ + Σ_{j=1}^{m} h_j R_j,  W(h) = W₀ + Σ_{j=1}^{m} h_j W_j,
  ḣ = −η_h [ ∇_h ( ½‖z_y − R(h) x̃_τ‖²_P + ½‖Δb − W(h) z_y‖²_Λ ) + Ω (h − h̄_p) ].

h is inferred online (context inference: which relation explains the current contingencies). The basis maps {R_j, W_j}, the partner priors h̄_p and x̄_p, A's slow component, and V_θ are learned only in replay (§5.7).

**The relation never descends display agreement.** No edge in (H) is an equal-time agreement edge between my display and theirs. This is what keeps the design out of Hansen & Ghrist's "learning to lie" (Theorem 5).

### 2.7 The gauge group

Changes of frame act on interior stalks: (g_s, g_o) ∈ GL(S) × GL(O). They act on maps by A ↦ A g_s⁻¹ on disp, A ↦ A g_o⁻¹ on obs, R ↦ g_o R g_s⁻¹, W ↦ W g_o⁻¹, C_B ↦ C_B g_s⁻¹, and Γ, V_θ transported accordingly. Boundary stalks (E, B) are physical: face channels and body sensors. The admissible gauge group is therefore the stabiliser of the boundary maps:

  𝒢 := { (g_s, g_o) : A g_s⁻¹ = A, C_B g_s⁻¹ = C_B, A g_o⁻¹ = A }.

### 2.8 Readouts (not state variables; Principle 2)

- **Valence** v(t) := −(d/dt) U(C_B x(t)), the rate of drive reduction.
- **Obstruction.** Let r* be the residual cochain at the fast equilibrium (x*, z*), weighted per edge. The obstruction is ε_obs := ½‖r*‖², which equals ℰ_h(x*, z*) minus the U and V terms. Its split by edge is the attribution vector a_e := ½‖r*_e‖², for e ∈ {obs, ρ, κ, sens, anc}.
- **Arousal** a(t) := ‖∇U(C_B x)‖ + ε_obs.
- **Relationship spectrum** spec M_B(h̄_p) for each partner p (eight complex numbers).

---

## 3. Theorems and proofs

Standing conventions:
- Q ≻ 0 means positive definite and Q ⪰ 0 means positive semidefinite.
- All precisions are symmetric positive definite.
- "Linear core" means V_θ ≡ 0 and U quadratic, U(β) = ½‖β − b*‖²_{K_b}. Where a statement holds beyond the linear core, it says so.
- For the linear core, write the Hessian blocks of ℰ_h as follows.
  - K := AᵀΠA ⪰ 0 (the observation Gram).
  - S := RᵀP + C_BᵀΛW (n × n), the total s-o coupling.
  - H_zz := K + P + WᵀΛW ≻ 0.
  - H_xx := RᵀPR + C_BᵀΛC_B + L_a, with the partner-independent anchor block L_a := AᵀΠ_fA + C_Bᵀ(K_s + K_b)C_B + Γ_h ≻ 0.
  - H_xz := −S.
  - The full Hessian H = [[H_xx, −S], [−Sᵀ, H_zz]] is ≻ 0. It is a sheaf Laplacian block, which is ⪰ 0, plus anchor terms that make it ≻ 0 (§3.1, Lemma 1).

### 3.0 Lemma 0 (why a single shared edge collapses to a projection copy)

**Statement.** Take the one-edge sheaf s ∼ o with the same map A on both ends, energy ½‖A x − A z‖², and the partner read from the face, z = A⁺y. Then the stubborn-boundary flow gives x(∞) = A⁺A z + Π_{ker A} x(0), and the agent's expression is A x(∞) = A A⁺ y = Π_{im A} y. That is an exact copy of every partner component the agent can express.

**Proof.**
1. By Hansen & Ghrist Theorem 5.1 (read), the U-restricted flow converges to −L[Y,Y]^†L[Y,U]u + y₀^⊥. Here L[Y,Y] = AᵀA, L[Y,U] = −AᵀA and u = z.
2. So x(∞) = (AᵀA)^†AᵀA z + Π_{ker AᵀA} x(0) = A⁺A z + Π_{ker A} x(0), since (AᵀA)^†Aᵀ = A⁺.
3. Then A x(∞) = A A⁺ A z = A z = A A⁺ y (the kernel term vanishes under A).

**Reading.** Principle 3 plus a display-agreement edge is copying, by construction. This is the formal shape of known-failures row 1. Any design that ties perception and production through one map needs something between them that is not an agreement edge. Here that is the pair of predictive edges ρ and κ, plus the anchor.

### 3.1 Lemma 1 (well-posedness)

**Statement.** For the linear core, H ≻ 0. ℰ_h is strictly convex, the fast flow (F1-F2) with fixed boundary converges exponentially to the unique minimiser (x*, z*), and (x*, z*) depends linearly on (y, f, b, x̄_p, b*).

**Proof.**
1. ℰ_h is a sum of squared norms of affine functions of (x, z), so H ⪰ 0.
2. Suppose (x, z)ᵀH(x, z) = 0. Then every term vanishes. The anchor term gives ‖x‖²_{Γ_h} = 0, so x = 0 because Γ_h ⪰ γ₀I ≻ 0. The ρ term then gives ‖z − 0‖²_P = 0, so z = 0. Hence H ≻ 0.
3. The flow is ξ̇ = −D_α(Hξ − c) with D_α = diag(α_z I, α I) ≻ 0. Then D_α H is similar to D_α^{1/2} H D_α^{1/2} ≻ 0, so its eigenvalues are real and positive, and convergence is exponential to ξ* = H⁻¹c, which is linear in the data.

Beyond the linear core: if ∇²(U + V_θ) ⪰ −σI and λ_min(H) > σ, the same argument gives a unique strictly stable equilibrium (strong convexity).

### 3.2 Theorem 1 (T1: no single setting runs the design from flat to copying; what it has instead)

The design has five structural facts in place of a gain.

**(a) The frame is pinned, so a counter-response is not a copy in disguise.** Every (g_s, g_o) ∈ 𝒢 satisfies im(g_s⁻¹ − I) ⊆ ker A ∩ ker C_B and im(g_o⁻¹ − I) ⊆ ker A. The steady transfer from partner expression to own expression,

  T_h := ∂(A x*)/∂y : E → E,

is invariant under 𝒢. In particular, no admissible change of frame maps a sign-flipped transfer (T_h = D T₀ with D = diag(±1) ≠ I) to an unflipped one. The reductions "counter-mimicry is copying −u" (Altafini gauge; Parsegov Example 5) and "an orthogonal single edge is copying in a frame" (Bodnar Lemma 6) do not apply. Those reductions need a frame change at one vertex that is not the identity on the expressible subspace, and 𝒢 contains none.

*Proof.*
1. A g_s⁻¹ = A ⇔ A(g_s⁻¹ − I) = 0 ⇔ im(g_s⁻¹ − I) ⊆ ker A. The same holds for C_B and for g_o.
2. Gauge acts trivially on the boundary stalks E and B, by definition of 𝒢. The energy is gauge-invariant: each edge term transforms covariantly, and the boundary values are untouched.
3. So the minimiser transforms as (x*, z*) ↦ (g_s x*, g_o z*). Then A x* ↦ A g_s⁻¹ g_s x* = A x*. The physical output is unchanged, and T_h, a derivative of it with respect to physical input, is unchanged.
4. A flipped transfer and an unflipped one are different maps E → E. An invariant cannot take both values on one gauge orbit.

**Schur's lemma** (the math-objects synthesis) gives a scalar gain only when the coupling must commute with an irreducible group acting on expression space. The design imposes no such equivariance: brow and mouth are physically distinct channels, so no symmetry group acts on E.

**(b) Ceiling and copy margin.** For the linear core, write the x-stationarity equation as a matrix-weighted average:

  (L_a + L_ρ + L_κ) x* = L_a t_a + Rᵀ P z* + C_BᵀΛ W z*,  with L_ρ := RᵀPR, L_κ := C_BᵀΛC_B,

where t_a := L_a⁻¹(Γ_h x̄_p + C_Bᵀ(K_s b + K_b b*) + AᵀΠ_f f) is the partner-independent target. Let M_p := (L_a + L_ρ + L_κ)⁻¹(L_ρ + L_κ) (the partner share).
- (i) Under (N), every eigenvalue of M_p is real and lies in [0, ϑ].
- (ii) Suppose the learned maps were exactly the copy maps on the relevant subspace, R = I and C_BᵀW = C_BᵀC_B, so both partner targets equal z*. Then

  ‖x* − z*‖_L ≥ (1 − ϑ) ‖t_a − z*‖_L,  with L := L_a + L_ρ + L_κ.

  So the agent never copies the partner unless the partner already sits at the agent's own temperament target.

*Proof.*
1. Write L_p := L_ρ + L_κ ⪰ 0. From (N), Γ_h ⪰ ((1−ϑ)/ϑ)(‖L_ρ‖ + ‖Λ‖)I ⪰ ((1−ϑ)/ϑ) L_p, because ‖C_BᵀΛC_B‖ ≤ ‖Λ‖ (C_B is a coordinate projection). So L_a ⪰ Γ_h ⪰ ((1−ϑ)/ϑ)L_p.
2. M_p = L⁻¹L_p is similar to L^{−1/2} L_p L^{−1/2}, which is symmetric ⪰ 0, so its eigenvalues are real and ≥ 0.
3. Its largest eigenvalue is max_v vᵀL_pv / vᵀ(L_a + L_p)v ≤ max_v vᵀL_pv / (((1−ϑ)/ϑ) + 1) vᵀL_pv = ϑ. This gives (i).
4. Under the copy maps, Rᵀ P z* + C_BᵀΛW z* = L_ρ z* + L_κ z* = L_p z*. So L x* = L_a t_a + L_p z*, which gives x* − z* = L⁻¹L_a (t_a − z*).
5. L⁻¹L_a = I − M_p, whose symmetrised form L^{−1/2}L_aL^{−1/2} has eigenvalues in [1−ϑ, 1] by step 3.
6. Therefore ‖x* − z*‖_L = ‖L^{1/2}L⁻¹L_a(t_a − z*)‖ = ‖(L^{−1/2}L_aL^{−1/2}) L^{1/2}(t_a − z*)‖ ≥ (1−ϑ)‖t_a − z*‖_L. This gives (ii).

**(c) No flat affect.** Suppose the sensed body b(t) carries innate fluctuation with spectral density Σ_b(ω) ≻ 0 on a frequency band, independent of the partner. Then for any partner behaviour, including a closed loop through the partner with the agent's loop stable (Theorem 7), the spectral density of the agent's expression satisfies

  S_f(ω) ⪰ A G_b(iω) K_s Σ_b(ω) K_s G_b(iω)^* Aᵀ  (as Hermitian matrices, for the open-loop part),

and it is nonzero wherever A C_Bᵀ ≠ 0 on the reachable subspace. So the agent's face is never flat while its body moves and its innate synergies A_B := A C_Bᵀ are nonzero.

*Proof (open loop: partner input independent of the body noise).*
1. The linear core is an LTI system with inputs (y, b, …).
2. The output spectral density is the sum of the contributions of independent inputs, each ⪰ 0.
3. The body contribution is A G_b(iω) C_BᵀK_s Σ_b K_s C_B G_b(iω)^* Aᵀ, where G_b(s) = (s/α I + H_s)⁻¹ is invertible for every s on the imaginary axis (H_s ≻ 0).
4. A G_b C_Bᵀ K_s^{1/2} ≠ 0 whenever A C_Bᵀ ≠ 0 on the range of G_b, which is all of S.
5. Closed loop: the transfer from b to f is A(s/α I + H_s − N e^{−sτ})⁻¹C_BᵀK_s. It is nonsingular on the imaginary axis when the loop is stable (no characteristic roots there), so the same nonvanishing holds.

This replaces Hansen & Ghrist's conserved Q = αAᵀA − βxxᵀ as the floor. Q is not conserved here, because the design's learning rule is not joint discord descent (Theorem 5). Its floor came from one direction only, whereas this floor holds on all of A·im(G_b C_Bᵀ).

**(d) Dial rank ≥ 2, and no single fixed frame balances the family.** Fix any two body channels c₁ (smile, a lip-corner pull group) and c₂ (a second group: sadness, a brow and lip-depressor group, or anger, a brow-lowerer group). The design can realise two relation states h₁, h₂ such that:
- (i) the c₁ → c₁ entry of T is the same at h₁ and h₂, while the c₂ → c₂ entry differs. This is the Bourgeois & Hess pattern.
- (ii) the c₂ → c₂ entry has opposite signs at h₁ and h₂, while c₁ → c₁ stays positive. This is the Hofman / Carr pattern.

In case (i), span{T_{h₁}, T_{h₂}} is two-dimensional. In case (ii), there are no fixed diagonal sign matrices D, D′ with D T_{h} D′ ≥ 0 entrywise for both h. Moreover, the set of basis maps {R_j, W_j} for which dim span{T_h : h ∈ H} ≤ 1 is a proper real-algebraic subset, so it has measure zero.

*Proof.*
1. Construction for (i). Put the c₁ → c₁ entry on the reflex core, Θ_r[c₁, c₁] > 0, which does not depend on h. Let W(h) differ between h₁ and h₂ only on the column read from partner channel c₂: W(h₂) = W(h₁) + w e_bᵀ A_{c₂}^+ for a body coordinate b whose innate synergy A_B[c₂, b] ≠ 0, with every other block equal.
2. By Lemma 1 the map from W to T is rational, and its derivative in the direction w e_bᵀA_{c₂}^+ is nonzero on the (c₂, c₂) entry when A_B[c₂, b] ≠ 0. That derivative is A H_s⁻¹(C_BᵀΛ w e_bᵀ A_{c₂}^+)H_zz⁻¹KΠ-terms, nonzero generically.
3. So T_{h₂} − T_{h₁} is supported on rows reached from b and columns from c₂. T_{h₁} has a nonzero (c₁, c₁) entry from the reflex, which T_{h₂} − T_{h₁} does not change. Hence T_{h₁} and T_{h₂} are not proportional unless T_{h₂} = T_{h₁}.
4. For (ii), choose w large enough with sign opposite to the h₁ value, so the (c₂, c₂) entry changes sign. This is possible because the entry is continuous in w and, in the diagonal scalar reduction of §3.9, equals a positive multiple of (p r + λ w).
5. Suppose fixed D, D′ made both nonnegative. Then d_{c₂} d′_{c₂} T_{h₁}[c₂, c₂] ≥ 0 and d_{c₂} d′_{c₂} T_{h₂}[c₂, c₂] ≥ 0 with entries of opposite sign. This forces a contradiction, since d d′ = ±1.
6. Genericity: dim span ≤ 1 means every pair of 2×2 minors of the stacked vectors [vec T_{h₁}, vec T_{h₂}] vanishes for all pairs (h₁, h₂). These are polynomial equations in the entries of the basis maps, after clearing the denominators det H, which are nonzero. The construction in steps 1-3 shows they are not all identically zero. The zero set of a nonzero polynomial has measure zero.

**(e) What a single scalar can and cannot do.** Let κ > 0 multiply any one declared constant or precision of the design. Then:
- (i) κ cannot produce copying, by (b) for every κ;
- (ii) κ cannot produce a flat face, by (c) for every κ, as long as A_B ≠ 0 and Σ_b ≻ 0;
- (iii) if κ multiplies *all* precisions together (a global "temperature"), it leaves x*, z*, T_h and the class of every dyadic loop mode unchanged (Theorem 6(c)).

What a single scalar *can* do is move the magnitude of the partner share inside [0, ϑ]. The ratio of two learned precisions (P against Λ) can also change the class of a loop mode (Theorem 6(b)), but that ratio is a measured reliability of two contingencies, not a setting.

*Proof of (e)(iii).* Each precision multiplies one quadratic term. Scaling every term of ℰ_h by κ, including Γ_h (which by (N) scales with the precisions; γ₀ is scaled too), gives κℰ_h, with the same minimiser. The loop matrices of Theorem 6 then both scale by κ, so H_s⁻¹N is unchanged.

**What the design has instead of a dial, stated exactly:**
1. a structural ceiling ϑ on the partner share, with a temperament remainder of at least 1 − ϑ;
2. a direction for each channel (match, counter, cross, none), set by the learned R(h) and W(h) and pinned to physical channels;
3. a loop class for each relationship mode (contagion, coregulation or chase), set by the gauge-invariant spectrum of the learned loop (Theorem 6);
4. a body-driven floor on expressive variance.

### 3.3 Theorem 2 (T2: drives are satiable; nothing rewards the partner's smiles, attention or time)

**(a) Zero drive at the set point.** ∇U(b*) = 0. At C_B x = b* the body potential exerts no force on x, and the readout v(t) = −∇U·(d/dt)C_B x is 0 there.

**(b) Bounded total drive reduction.** For any trajectory and any T > 0,

  ∫₀ᵀ v(t) dt = U(C_B x(0)) − U(C_B x(T)) ≤ U(C_B x(0)).

The drive reduction obtainable in an interaction is bounded by the deficit at its start, whatever the partner does and however long the interaction lasts. More contact, attention or time beyond satiety yields zero further drive reduction.

**(c) No partner-outcome term.** Neither ℰ_h nor any learning loss (L_A, L_R, L_W, (H), and the replay losses in §6.4) contains a term that increases with the partner's expression of any kind (smile, gaze, speech duration). Every partner-dependent term is a squared prediction error, minimised by accurate prediction, not by any particular partner behaviour. The fast dynamics descend ℰ_h with respect to x and z only, never with respect to the partner's future y. So no expression is ever selected for its predicted effect on the partner.

**(d) Afferents are clipped at satiety.** The innate afferents that move b (§5.2) push each b_i toward b*_i and stop there: b_i ← b_i + min(input, b*_i − b_i) for deficit variables. Being addressed therefore cannot push the contact variable past its set point.

*Proofs.*
- (a) φ_i is convex with its minimum 0 at 0, so φ_i′(0) = 0 whenever φ_i is differentiable there (the build uses φ_i(u) = k_i u²/2 on each side, with possibly different k_i). Hence ∇U(b*) = 0.
- (b) Write v = −(d/dt)U(C_Bx) and apply the fundamental theorem of calculus. U ≥ 0 gives the bound.
- (c) By inspection of (E), (L_A), (L_R), (L_W), (H) and the replay losses: every term involving y, z_y or Δb is of the form ‖target − prediction‖². Its gradient with respect to the agent's maps vanishes at the regression fixed point (Theorem 5), independent of the target's sign or valence.
- (c), continued. Equations (F1-F2) are gradients of ℰ_h with respect to (x, z) at the current boundary data, and y(t + s) for s > 0 does not appear. There is no model-predictive action selection anywhere in the fast core.
- (d) By construction of the afferent.

*Cost, recorded.* (c) means the fast core never acts *in order to* soothe or engage the partner. Coregulation is a property of the learned loop (Theorem 6), not an intention. Intentional regulation, if any, is Claude's, in words (Principle 4). The face-development synthesis (item 10) records the predicted developmental cost of refusing reinforcement by the partner's smile: less social expressiveness.

### 3.4 Theorem 3 (T3: time scales from reflex to temperament come from the structure)

**(a) Onset order equals graph distance.** Linearise the full system, (F1)-(F3) together with (H), around a rest point with the partner input y ≡ 0. Apply a small step in y on channel c at t = 0. The contribution to the muscle output m(t) of each route in the dependency graph y → z, z → x, z → h, x → h, h → x, x → m, y → m is of exact order t^ℓ/ℓ! times the product of the couplings along the route, plus O(t^{ℓ+1}), where ℓ is the route's length. The orders are:
- the reflex route y → m: ℓ = 1;
- the emotional route y → z → x → m: ℓ = 3. Its coefficient depends on the current relation h(0), so a context known before the stimulus acts at order 3;
- the newly inferred context route y → z → h → x → m: ℓ = 4.

*Proof.*
1. The linearised system is ẇ = 𝒜w + ℬy. Here w stacks (z, x, h, m), the zero blocks of 𝒜 follow the dependency graph, and ℬ has nonzero blocks only into z (perception) and m (reflex).
2. For a step input, w(t) = Σ_{k≥0} t^{k+1}/(k+1)! 𝒜^k ℬ y.
3. The m-component of 𝒜^kℬ is a sum over walks of length k from an input-receiving block to m, with each walk contributing the product of its blocks.
4. The shortest walk to m from the m-input (the reflex) has k = 0, giving order t¹. From the z-input, the shortest walk is z → x → m, with k = 2 and order t³. The shortest walk through h is z → h → x → m, with k = 3 and order t⁴.
5. The coefficient of the k = 2 walk is the product of the m←x block (β_m A_F), the x←z block (α S(h(0)), evaluated at the rest point) and the perception input. So h(0) enters at order 3.
6. The h-route needs the h←z block, ∂ḣ/∂z = −η_h ∂²(·)/∂h∂z ≠ 0 generically, and the x←h block, α ∂S/∂h · z₀ plus the anchor terms, evaluated at the rest point.

Compare with the human data (mimicry-context synthesis, section 3):
- Carr 2014 (read): matching corrugator responses before 1 s, context-carrying zygomaticus responses at 2-4 s.
- Weyers 2009 (read): the competition effect appears from the 4th second.
- Mauersberger 2022 (read): context effects within the first second when the context is already known.

The design predicts all three: the h-route is late (order 4) for newly inferred context, and a known context acts already at order 3. This is a prediction, not evidence.

**(b) Persistence of a shared state is controlled by the loop.** Consider the free s-o block, the energy restricted to the ρ and κ edges, ℰ_so(x, z) = ½‖z − Rx‖²_P + ½‖C_Bx − Wz‖²_Λ, with Hessian L_so.
- (i) Scalar stalks (n = n_b = 1, R = r, W = w, P = p, Λ = λ): det L_so = pλ(1 − μ)², with μ = rw the monodromy. The smallest eigenvalue satisfies det/tr ≤ λ_min(L_so) ≤ 2 det/tr. The irreducible tension for a given partner reading z is min_x ℰ_so = ½ · pλ(1 − μ)² z² / (p r² + λ).
- (ii) General stalks: for every x ∈ S,

  λ_min(H) ≤ [ ‖(C_B − W R)x‖²_Λ + xᵀL_a x + (Rx)ᵀK(Rx) + ‖WRx‖²... ] / (‖x‖² + ‖Rx‖²),

  stated exactly as: λ_min(H) ≤ ξᵀHξ/ξᵀξ with the test cochain ξ = (x, Rx), whose sheaf part equals ‖(C_B − W R)x‖²_Λ.

So the state has a slow mode wherever the relationship loop nearly closes, (C_B − WR)x ≈ 0, and the anchor and observation are weak in that direction. Its relaxation rate is at most α times that quotient.

After the partner leaves (Π → 0, so the observation term vanishes), a shared state along a near-closing loop direction decays at a rate bounded by α(‖(C_B − WR)x‖²_Λ + xᵀL_a x)/(‖x‖² + ‖Rx‖²). Persistence is a property of the learned relationship loop, not a time constant.

*Proof.*
1. (i) L_so = [[p r² + λ, −(p r + λ w)], [−(p r + λ w), p + λ w²]].
2. Its determinant is (p r² + λ)(p + λw²) − (p r + λ w)² = p²r² + p r²λw² + λp + λ²w² − p²r² − 2pλrw − λ²w² = pλ(r²w² − 2rw + 1) = pλ(1 − rw)².
3. For a 2×2 matrix ⪰ 0 with eigenvalues λ_min ≤ λ_max, we have λ_max ∈ [tr/2, tr] and λ_min = det/λ_max. This gives the bounds.
4. The minimum of a sum of two quadratics in x, with targets z/r (weight p r²) and w z (weight λ), is ½ (p r² λ/(p r² + λ)) (z/r − w z)² = ½ pλ(1 − rw)² z²/(p r² + λ).
5. (ii) Courant-Fischer with the test vector ξ. Its ρ-term vanishes because z = Rx. Its κ-term is ‖C_Bx − WRx‖²_Λ. The remaining terms of H are the anchor, the observation and the rest of the Hessian, as written.

**(c) The dyadic loop through the real partner: monotone persistence or damped oscillation.** Model the partner, over the relevant band, as responding in the agent's coordinates with lag τ: z_y(t) ≈ R_true x(t − τ). Take the adiabatic limit for z (α_z ≫ α). Then the linear core obeys

  ẋ = −α H_s x + α N x(t − τ) + (partner-independent inputs),

with H_s := H_xx − S H_zz⁻¹Sᵀ ≻ 0 (the Schur complement) and N := S H_zz⁻¹ K R_true. For one mode in the commuting scalar reduction (H_s → f > 0, N → g, after absorbing α):
- (i) If 0 ≤ g < f, the rightmost characteristic root is real and lies in (−f, 0). The return is monotone, with no oscillation. For small |λ|τ that root is ≈ −(f − g)/(1 + gτ). The mode slows as g → f: a shared mood that lingers.
- (ii) If g < 0 and |g| τ e^{1 + fτ} > 1, there is no real root. Every mode is oscillatory, and it is damped when |g| < f. This is damped oscillation back to the set point, Butler & Randall's coregulation signature.
- (iii) If |g| < f, the mode is stable for every delay τ ≥ 0.

*Proof.*
1. The characteristic function is h(λ) = λ + f − g e^{−λτ}.
2. Proof of (i).
   - For real λ, h′(λ) = 1 + gτe^{−λτ} > 0. Also h(−f) = −g e^{fτ} ≤ 0 and h(0) = f − g > 0, so there is a unique real root λ_r ∈ (−f, 0].
   - Let λ = a + ib with b ≠ 0 be a root. Its real part gives a + f = g e^{−aτ} cos(bτ). Its imaginary part gives b = −g e^{−aτ} sin(bτ).
   - If cos(bτ) = 1, then sin(bτ) = 0, so b = 0, a contradiction. So cos(bτ) < 1, giving a + f < g e^{−aτ} (for g > 0), i.e. h(a) < 0, so a < λ_r. Every complex root lies left of the real root. (For g = 0 the only root is −f.)
   - First order: λ + f = g(1 − λτ + O(λ²τ²)) gives λ(1 + gτ) = g − f.
3. Proof of (ii).
   - For g < 0, h(λ) = λ + f + |g|e^{−λτ}. Then h′ = 1 − |g|τe^{−λτ}, which vanishes at λ* = ln(|g|τ)/τ.
   - The minimum value is h(λ*) = λ* + f + 1/τ. It is positive, so h has no real root, iff ln(|g|τ) + fτ + 1 > 0, i.e. |g|τ e^{1+fτ} > 1.
4. Proof of (iii): Theorem 7 with ν = |g|.

### 3.5 Theorem 4 (T4: "reads the other through its own body" as an equation)

**(a) Perception is the adjoint of production.** With x held fixed, the partner reading's Jacobian J := ∂z*/∂y = H_zz⁻¹AᵀΠ satisfies

  ⟨J e, v⟩_{H_zz} = ⟨e, A v⟩_Π  for all e ∈ E, v ∈ O.

So J is the adjoint of the agent's own production map A, with the observation precision on E and the posterior precision H_zz on O.

**(b) Invisibility.** If AᵀΠ e = 0, then J e = 0, and e has no effect on z*, x* or the agent's expression, at any time. In particular, if the agent loses the ability to produce channel c (A_c := 0, a "paralysis" lesion) and Π is block-diagonal by channel, then the partner's channel c has no effect on the agent's state.

**(c) Egocentric bias, bounded.** With y fixed, ∂z*/∂x = H_zz⁻¹Sᵀ. The agent's own state biases its reading of the partner toward the partner state that would explain its own state through R and W, with gain at most ‖PR + WᵀΛC_B‖ / λ_min(K + P + WᵀΛW).

**(d) Self is the closed loop.** For the self-mirror pair (the agent watching its own rendered face, with no delay beyond rendering), the trained A makes the self-loop's contingency perfect (ΔP = 1 in the sense of Theorem 5(a)). A partner is any source whose contingency is high but imperfect. This is the Bahrick & Watson distinction (via face-development synthesis), as a statement about the residual of (L_A) against the residual of (L_R).

*Proofs.*
- (a) From ∂ℰ/∂z = 0: H_zz z* = AᵀΠ y + Sᵀ x, so J = H_zz⁻¹AᵀΠ. Then ⟨Je, v⟩_{H_zz} = (H_zz⁻¹AᵀΠe)ᵀH_zz v = eᵀΠA v (H_zz and Π are symmetric).
- (b) Immediate from (a). x* depends on y only through z* (Lemma 1's linear solve: x* = H_s⁻¹(S H_zz⁻¹AᵀΠ y + …)). With Π block-diagonal, AᵀΠ e_c = A_cᵀΠ_c e_c = 0 when A_c = 0.
- (c) From the same stationarity, ∂z*/∂x = H_zz⁻¹Sᵀ with Sᵀ = PR + WᵀΛC_B, and ‖H_zz⁻¹‖ = 1/λ_min(H_zz).
- (d) In the self-mirror pair, f_sensed is a deterministic function of the commanded state up to rendering noise. The LMS fixed point of (L_A) has residual variance equal to the rendering noise only, whereas the residual of R against a partner includes the partner's own state. (Definition plus Theorem 5(a).)

The swap identity of the math-objects synthesis (∂F_other/∂x_self equal to ∂F_self/∂x_other with roles swapped) is not imposed. Here the agent's model of how it moves the partner is R, learned from what the partner actually did. Simulation-by-self enters only through A.

### 3.6 Theorem 5 (contingency, not contiguity; no learning to lie; crossed experience builds counter-maps)

**(a) The learned maps measure contingency.** At the stationary point of (L_R), when the input is stationary, R* = C_{z_y(t), x̃_τ(t)} C_{x̃_τ}⁻¹, the regression of the partner reading on the agent's lagged state. For a binary act a ∈ {0, 1} and a binary seen event o ∈ {0, 1}, the least-squares weight with an intercept is ΔP = P(o = 1 | a = 1) − P(o = 1 | a = 0). That weight is zero whenever seeing o is as likely without the act as with it, however often the two co-occur.

**(b) No learning to lie.** Hansen & Ghrist's Theorem 8.1 (read) proves that the discord descent dF/dt = −β(F_v x_v − F_u x_u)x_vᵀ drives a restriction map to the Frobenius-nearest map under which the current pair of states looks like agreement. In this design, the fixed points of (L_R), (L_W) and (H) are functionals of the joint distribution of (x̃_τ, z_y) and (z_y, Δb). They do not depend on the agent's current agreement energy, and they cannot be reached by making the agent's display agree with the partner's.
- z_y is computed from y alone, with no prior from R and no pull from x.
- Δb is the sensed body change.
- Neither is a function of the agent's display map, except through the partner's real response.

**(c) Crossed experience reverses mimicry channel by channel.** Suppose that over a training period the partner's readings follow z_y(t) = D x(t − τ) + noise, with D = diag(±1) on some channels, independent noise and x persistently exciting. Then R → D. The ASL pull on the agent's state, the −∂ℰ/∂x term RᵀP(z − Rx), pulls it toward the counter-matched state on exactly the flipped channels.

*Proofs.*
- (a) The update's expectation is zero iff E[(z_y − R x̃)x̃ᵀ] = 0, the normal equations, whose solution is the regression. In the binary case with intercept (o ≈ w₀ + w₁ a), least squares gives w₁ = Cov(o, a)/Var(a). With p₁ := P(o | a=1), p₀ := P(o | a=0) and q := P(a=1): Cov(o, a) = q(p₁ − E o) = q(1−q)(p₁ − p₀), and Var(a) = q(1−q), so w₁ = p₁ − p₀ = ΔP.
- (b) The stationarity conditions of (L_R) and (L_W) are the normal equations of (a), involving only second moments of (x̃_τ, z_y, Δb). The agreement energy ½‖δξ‖² does not appear in any of the three updates. In (H) the gradient is of the two prediction losses only. The disp edge, the only edge comparing the agent's display with anything, compares it with the agent's own sensed expression, not the partner's.
- (c) From (a), R* = C_{z,x̃}C_{x̃}⁻¹ = D C_x̃ C_x̃⁻¹ = D. Then −∂ℰ/∂x ∋ RᵀP(z − Rx) = DP(z − Dx), whose zero for the ρ term alone is x = D z, sign-flipped on D's negative channels.

This is the falsifiable ASL prediction of Ray & Heyes and Cook et al. (via notes): if the agent's displays are systematically crossed with the partner's, its fast "mimicry" reverses on those channels. If it does not, the map was not learned.

### 3.7 Theorem 6 (mimicry is contagion; coregulation needs the consequence loop)

Use the notation of Theorem 3(c), and assume the agent's contingency model is correct on the band, R = R_true. By Theorem 5(a) this holds at the LMS fixed point when the partner is a linear responder.

**(a) The ASL loop alone is always morphogenic.** With the consequence edge lesioned (Λ = 0):
- H_s = L_a′ + Rᵀ(P : K)R and N = Rᵀ(P : K)R, where P : K := P(P + K)⁻¹K is the parallel sum (symmetric ⪰ 0) and L_a′ := L_a (the partner-independent block);
- every eigenvalue ν of the steady loop gain H_s⁻¹N is real with 0 ≤ ν < 1;
- the delayed loop is stable for every τ;
- when L_a′ commutes with Rᵀ(P : K)R, every mode's rightmost root is real, so the return is monotone, never oscillatory (Theorem 3(c)(i)).

This holds for every R, P, Π and A: mimicry learned by contingency produces contagion (a lingering shared state) and never coregulation.

**(b) Coregulation requires the consequence edge with a negative round trip.** In the commuting scalar reduction (one mode, observation Gram k = πa² > 0), the delayed loop gain is

  g = (p r + λ w) k r / (k + p + λ w²),  so sign g = sign(p r² + λ μ),  μ = w r.

A negative loop mode, and hence by Theorem 3(c)(ii) damped oscillation once |g|τe^{1+fτ} > 1, exists iff λ(−μ) > p r²: the consequence loop has a negative monodromy that outweighs the always-positive ASL term.

**(c) Invariance.** Scaling every precision by κ > 0 leaves H_s⁻¹N unchanged, so no global gain changes any loop class. The class is a function of (R, W) through μ and of the ratio p : λ of two learned reliabilities.

*Proofs.*
- (a), the formulas.
  - With Λ = 0: S = RᵀP, H_zz = K + P, and H_xx = RᵀPR + L_a.
  - H_s = RᵀPR + L_a − RᵀP(K+P)⁻¹PR = L_a + Rᵀ[P − P(K+P)⁻¹P]R.
  - P − P(K+P)⁻¹P = P(K+P)⁻¹[(K+P) − P] = P(K+P)⁻¹K = P : K.
  - N = S H_zz⁻¹K R = RᵀP(K+P)⁻¹K R = Rᵀ(P : K)R.
- (a), symmetry of the parallel sum. For K ≻ 0 and P ≻ 0, P(K+P)⁻¹K = (K⁻¹ + P⁻¹)⁻¹, which is symmetric ≻ 0. For K ⪰ 0 take limits, so it is ⪰ 0.
- (a), eigenvalues. ν solves N v = ν H_s v, the generalised symmetric definite problem, so ν is real and ν = vᵀNv/(vᵀL_a v + vᵀNv) ∈ [0, 1), since L_a ≻ 0.
- (a), stability for every delay. V = xᵀx + α∫_{t−τ}^{t} x(s)ᵀN x(s) ds gives V̇ = −2αxᵀH_s x + 2αxᵀN x_τ + αxᵀNx − αx_τᵀN x_τ ≤ −2αxᵀ(H_s − N)x = −2αxᵀL_a x < 0, using 2xᵀNx_τ ≤ xᵀNx + x_τᵀNx_τ for N ⪰ 0.
- (a), monotone return: the commuting case reduces to scalar modes with 0 ≤ g < f, and Theorem 3(c)(i) applies.
- (b) Scalar: S = p r + λ w, H_zz = k + p + λ w², N = S k r/H_zz. Since k, H_zz > 0, sign N = sign((p r + λ w) r) = sign(p r² + λ w r).
- (c) Every block scales by κ, so H_s and N scale by κ and H_s⁻¹N is unchanged.

**Reading.** This is the design's main structural claim. Fast mimicry and coregulation come from different links with different learning signals. ASL (being imitated) can only ever build contagion. Damped return to a set point needs the partner's state to *mean* the opposite for the agent's body around the loop. That fits Butler & Randall's classing of contagion as morphogenic, not regulation (read via note), and it yields a double-dissociation lesion test (§8).

### 3.8 Theorem 7 (stability while the relation switches)

**Statement.** Let h(t) be any piecewise-continuous signal in H, switching arbitrarily, and consider ẋ = −αH_s(h(t))x + αN(h(t))x(t − τ) + αu(t). Suppose λ_min(H_s(h)) ≥ f₀ and ‖N(h)‖ ≤ ν < f₀ for all h. Then for u ≡ 0, ∫₀^∞‖x‖² ≤ V(0)/(2α(f₀ − ν)) and x(t) → 0. For general u, ∫₀ᵀ‖x‖² ≤ (V(0) + (α/(f₀−ν))∫₀ᵀ‖u‖²)/(α(f₀ − ν)), an L² gain bound uniform over all switching signals.

The hypothesis is enforced by construction. (N) and the caps on the precisions bound ‖N(h)‖ relative to λ_min(H_s(h)) over the compact set of admissible h (the h-prior Ω keeps h bounded). The partner's R_true, which the agent does not control, enters ‖N‖. The bound is stated for the agent's model of the partner.

*Proof.*
1. Let V = ‖x‖² + αν∫_{t−τ}^{t}‖x(s)‖²ds. H_s(h) is symmetric, being the Schur complement of a symmetric matrix.
2. Then V̇ = 2xᵀ(−αH_s x + αN x_τ + αu) + αν‖x‖² − αν‖x_τ‖² ≤ −2αf₀‖x‖² + 2αν‖x‖‖x_τ‖ + αν‖x‖² − αν‖x_τ‖² + 2α‖x‖‖u‖.
3. Using 2ν‖x‖‖x_τ‖ ≤ ν‖x‖² + ν‖x_τ‖²: V̇ ≤ −2α(f₀ − ν)‖x‖² + 2α‖x‖‖u‖ ≤ −α(f₀ − ν)‖x‖² + (α/(f₀ − ν))‖u‖².
4. Integrate. For u = 0, x is bounded (V non-increasing), ẋ is bounded, and ∫‖x‖² < ∞, so x → 0 by Barbalat's lemma.

Nothing in the proof uses the switching law. Sign changes of restriction maps, the "agreement to disagree" of Hansen & Ghrist §12, are therefore safe. In contrast, a negative edge *potential* on the dyad's cut edge is unstable (their Proposition 12.1, read).

### 3.9 Numeric checks of the algebra (not results)

Script: /tmp/dcs_checks/check.py, run in research/foundations/sims's uv environment.
- det L_so = pλ(1 − rw)² for five random (p, λ, r, w): agreement to 10⁻¹².
- Scalar transfer ∂x*/∂y equals π a (p r + λ w)/D from the full 2×2 solve: 0.010938157341 both.
- Delay threshold for f = 1, τ = 1.5: |g| = 0.0547. Just below it a real root exists; just above it none. The simulated g = −0.5 mode changed sign 15 times in 40 s and decayed to 10⁻¹¹. The g = +0.5 mode never changed sign.
- λ_min of L_so (with an anchor of 10⁻³) for μ = 0, 0.5, 0.9 lies between det/tr and 2det/tr. At μ = 0.99 the anchor dominates, as expected.

### 3.10 Properties the human data require

| Requirement (gap 6; mimicry-context synthesis) | Where it comes from in the object | Proved in |
|---|---|---|
| Per-expression gating | Π, P, Λ are per channel; W(h) acts column by column on A_c-read channels; R(h) per channel group | Theorem 1(d), 4(b) |
| Sign flips that depend on the relation | the sign of each transfer entry follows (p r + λ w) per channel, with w = W(h) entries changed by h | Theorem 1(d)(ii), 6(b) |
| Off-diagonal responses (smile to anger) | W(h) maps partner channel c into a body coordinate whose innate synergy expresses another channel | Theorem 1(d) construction |
| Fast matching, then slower context | onset order 1 (reflex), 3 (emotional route with pre-set context), 4 (new context) | Theorem 3(a) |
| Partner history within minutes | h inferred online (H); R and W by LMS at rates η_R, η_W | §2.5-2.6 |
| Partner history across days | h̄_p, x̄_p, {R_j, W_j} in replay with reinstated partner tags | §5.7 |
| Tracking separate from alignment (Hoehl) | z (the o vertex) tracks the partner fully; only the ρ and κ edges move x; a stranger (R ≈ 0, W ≈ 0) is tracked but not aligned with, beyond the reflex core | Theorem 4, 1(b) |
| Disgust not mimicked in live dyads | partners rarely imitate the agent's disgust and their disgust rarely predicts the agent's body change, so R and W are ≈ 0 on that channel, and no reflex is declared for it | Theorem 5(a) |
| Coregulation vs contagion are distinct | different links, different loop classes | Theorem 6 |
| Intermittent, mid-range coupling, not maximal lock | the ceiling ϑ; the anchor; the loop gain < 1 in the ASL loop | Theorems 1(b), 6(a) |
| Hidden-regulator hazard bounded | partner share ≤ ϑ; the anchor x̄_p remains when the partner leaves; persistence bounded by Theorem 3(b) | Theorems 1(b), 3(b) |

---

## 4. Why existing mechanisms cannot do this, mathematically

The properties tested:
- **P1:** the frame is pinned and perception is the adjoint of production (Theorems 1(a), 4).
- **P2:** a copy margin ≥ (1 − ϑ)·dist(temperament, partner) for every learned parameter (Theorem 1(b)).
- **P3:** two separately learned links whose loop spectrum classifies the dyad, with ASL alone provably morphogenic (Theorem 6).
- **P4:** shared-state persistence controlled by loop closure (Theorem 3(b)).
- **P5:** learning targets that a display cannot fake, with a ΔP fixed point (Theorem 5).

| Mechanism | Which property fails, and why (exact) |
|---|---|
| **Attention**, one head over self and partner tokens | The output is α V x_partner + (1 − α) V x_self with α = softmax weight ∈ (0, 1). α → 1 as the score gap grows, through query/key norms or temperature, so copying through V is reachable: P2 fails unless a residual floor is imposed, and then the floor is this design's anchor. The value map V is independent of the query and key maps, so P1 does not follow. With two tokens there is one cycle-free relation: no loop, so P3 and P4 do not arise. Multiple heads give a sum of such terms, each a gain on a fixed value map (math-objects synthesis, row "Attention over two tokens"). |
| **Hopfield retrieval** (modern, softmax energy) | Fixed points approach stored patterns as β → ∞. The partner input acts as a query, and the output is a convex combination of stored patterns, discontinuous in the partner as β grows. If partner faces are stored, retrieval at high β is a delayed copy (the fast-weights critique). P2 fails at the β end; P1 has no counterpart; there is no loop (P3, P4). |
| **Fast weights / delta-rule memory** | The update W ← W + η(v − Wk)kᵀ is exactly the LMS rule used here (L_R, L_W). This part is shared, not new. What fails is the use: a fast-weight memory is read forward only, v̂ = Wk. The ASL pull needs the adjoint Rᵀ acting on the agent's state, and the loop needs two such maps learned from different targets and composed. Without the adjoint read, Theorem 6(a) has no object. With it, the memory is a sheaf edge. If the key is the partner's face and the value is the agent's next state (self-prediction), the copy lock-in of the v2 fast-weights critique follows. P5 requires the target to be the agent's body, which the mechanism does not fix. |
| **State-space models** (LTI or selective) | At fixed h the linear core *is* an LTI system with a structured (A, B, C). So it is a constrained SSM, and the constraints are the content. A generic SSM has independent input and output matrices, so P1 (input map = adjoint of output map, in the stated metrics) does not follow. It can realise the pure copy kernel K(τ) = δ(τ − d) I, so P2 fails. The loop and the two learning targets are absent (P3, P5). Selective SSMs make B and C input-dependent, but not tied, so the same holds. |
| **Diffusion (denoising) generators** | A sampler of p(face | partner context) has no persistent state, so P2-P4 are undefined. The documented outcomes are copy or mean (known-failures rows 1-2). |
| **Oscillators** (Kuramoto, HKB) | Kuramoto coupling K sin(θ_j − θ_i) has one gain per pair, and K large gives phase locking, a copy of phase (P2 fails). HKB's virtual-partner coupling has a sign parameter μ that selects in-phase or anti-phase (coordination synthesis 1a). That is the closest prior object to P3, but μ is set by the experimenter, is a scalar, and is not a composition of two learned maps. With one μ per pair, "contagion vs coregulation" is a parameter, not a derived class. |
| **Linear operators** (Friedkin-Johnsen, Parsegov W ⊗ C, per-pair blocks) | At fixed h the linear core is a matrix-weighted Friedkin-Johnsen model with two partner edges. The ceiling (N) is FJ's stubbornness, so P2 is shared with FJ. What FJ lacks: two distinct edges between the same pair with different learned meanings, so no monodromy (P3, P4); the tie of the partner reading to the agent's own production map (P1); and learning (P5). In the Kronecker form, a negative eigenvalue of C also flips the agent's own retention (Parsegov note), which this design avoids because the anchor and the partner maps are separate edges. |
| **Graph-Laplacian diffusion / consensus**, including Altafini signed consensus | The constant sheaf gives x → z, an exact copy, with a stubborn partner (Hansen & Ghrist Theorem 5.1; Lemma 0 here). Balanced signs give copy in a flipped frame, imbalanced signs give a flat face (Altafini via tutorials). P2 fails, and P1 is absent (no expression map). The frame-pinning of Theorem 1(a) is what removes the "flipped frame" reduction, and consensus has no boundary maps to pin with. |
| **Single-edge sheaves** (discourse sheaf as used for a dyad; NSD on two nodes) | A tree has path-independent transport (Bodnar Lemma 6, read), so no holonomy. P3 and P4 have no object. With the partner stubborn the response is A⁺B u (Hansen & Ghrist Thm 5.1). Learning by discord descent learns to lie (their Theorem 8.1, read), so P5 fails. |

**The honest summary of this section.** None of these mechanisms *implies* P1-P5. Several can be *constrained* to satisfy some of them, and doing so would reproduce this design. The properties come from constraints placed on standard parts, not from a new operation.

---

## 5. The whole system, derived from the object

### 5.1 Perception of face and voice through the agent's own body

- **Face** at 30 Hz: 52 blendshapes plus head pose and gaze (6), from MediaPipe at S2, as a borrowed coordinate system (brief S4 replaces it). **Voice:** 8 prosody features at 30 Hz (f0, f0 slope, energy, voicing probability, spectral tilt, speech rate proxy, pause flag, jitter proxy). Together they make y ∈ E, k = 66.
- They enter only as the boundary value of the obs edge. The partner reading z solves (F1). By Theorem 4 it is the adjoint of the agent's own A, so the agent perceives the partner's face and voice as "the state of my body that would make this". Components the agent cannot produce are invisible. There is no classifier and no label (Principle 1).
- Transcript events (turn onsets and offsets, being addressed, word onsets) enter as point events. They feed body afferents (contact, vocal load) and the timing of the deliberate route (§5.4). The words go to Claude only.

### 5.2 Innate body and reflexes

- U: per-variable convex potentials, with set points b* (Theorem 2).
- Innate afferents. Each is a fixed, clipped function from features to a body coordinate's change:
  - being addressed (speech directed at the agent) reduces the contact deficit;
  - abrupt loud onsets raise integrity load;
  - own prediction error ‖z_y − R x̃‖ raises the predictability deficit;
  - own speaking raises vocal load;
  - time drifts energy and rest.

  None reads the partner's smile (Theorem 2(c)).
- The reflex core Θ_r: lip-corner pull to lip-corner pull, and brow-lowerer relaxation to lip-corner pull. This is the robust, context-poor core of the mimicry synthesis, declared as an innate constraint. A surprise reflex raises the brows in proportion to the obstruction's obs-edge component (the orienting response, emotion element 8).
- The innate synergies A_B := A C_Bᵀ start from the face-development synthesis: lip-corner pull recruits cheek raise with intensity; mouth opening tracks activation; a distress pattern (eye constriction with intensity, mouth opening with activation) tracks integrity and contact deficits. There are no anger, fear or surprise templates.

### 5.3 The latent state where emotion emerges (no labels)

- The state is x = (x_B, x_ℓ) ∈ S. x_B is the agent's *predicted* body: the sens edge ties it to the sensed b, and the κ edge pulls it toward what the partner's state predicts. U acts on x_B, so regulation acts on the prediction before the deficit arrives (allostasis, emotion element 6).
- x_ℓ ∈ ℝ⁵⁶ is shaped by:
  - V_θ, trained in replay to make the flow predict future sensed body values at three horizons (§6.4);
  - the anchor x̄_p;
  - facial feedback through the disp edge;
  - the ASL pull through R (which acts on all of S).
- Emotion is structure, not a variable. The candidates for what a theory would call emotion are:
  - (i) regions of S that the flow visits and dwells in (basins of U + V_θ + sheaf energy);
  - (ii) the obstruction and its attribution vector a_e over the edges;
  - (iii) the per-partner loop spectrum spec M_B(h̄_p).

  Valence and arousal are the readouts of §2.8.

### 5.4 Face output through two routes into one muscle layer

The muscle layer has 52 first-order units, one per blendshape, with time constant 1/β_m ≈ 60 ms and saturation σ_m:

  ṁ = −β_m m + β_m σ_m( (A_F x + Θ_r y) ⊙ (1 − g_inh) + D_del u_del ).

- **Emotional route:** A_F x + Θ_r y, the state through the agent's own display map plus the innate reflex. It is bilateral and covers the upper face.
- **Deliberate route:** D_del u_del. u_del carries viseme targets from the TTS phoneme timing, plus discrete gestures that Claude may request (nod, raised brows), addressing individual muscles, mainly the lower face. D_del is a fixed viseme-to-blendshape matrix (15 × 52).
- **Inhibition** g_inh ∈ [0, 1]^52 is the deliberate route's learned, initially near-zero suppression of the emotional route (display rules, masking). It is set by Claude-requested masking and by replay-learned display regularities.
- **Lesions** (face-development synthesis): cut the emotional route (A_F x + Θ_r y := 0) and spontaneous expression goes flat while posing survives. Cut the deliberate route and posing fails while spontaneous expression survives or grows (inhibition released).
- **Two routes, one muscle layer.** The sensed result f feeds back through the disp edge (facial feedback).

### 5.5 Voice

- The voice rows A_V of A map the state to prosody offsets (pitch level and range, energy, rate, pause tendency). They drive a local TTS (Kokoro-82M or Piper are in the notes; ordinary choice) through its prosody controls. The words are Claude's.
- The partner's voice is read through the same A_V rows (Theorem 4), so the agent hears prosody through its own voice.

### 5.6 Coupling to Claude without text (Principle 4)

Claude never sees x, z, h, b or any readout as numbers or words. The state reaches Claude in three ways. The first two are the shared interface already recorded in sketches/v2-README.md and claim no novelty.

1. **Draft selection by sheaf energy.** Claude produces N = 3 drafts. A frozen sentence encoder (an existing small model, ordinary choice) plus a learned head g maps each draft to its predicted prosody and expression summary ĝ(d) ∈ E. The agent selects the draft that adds the least energy on the disp edge: ½‖A x − ĝ(d)‖²_{Π_f}, i.e. the draft its body would say most naturally.
2. **Processing changes.** The obstruction sets Claude's thinking budget and reply latency: high irreducible tension means more deliberation and a later reply. Its attribution vector selects which stored episodes' *transcripts* (never their state) are retrieved into Claude's context. Episodes whose innate-coordinate tags are nearest the current x_B are retrieved first. This changes how Claude processes without telling it anything.
3. **Reappraisal acts on the relation, not the face.** Claude's own reply text is encoded by the same frozen encoder and mapped by a learned head E_h to a proposal Δh, added to (H) with gain η_C. Concepts change what the partner's expression *means* (W(h), R(h)). This is the constructionist path, and it is a switch that can be turned off (emotion-elements synthesis, D1). E_h is trained in replay to predict the h that best explained the partner afterwards.

### 5.7 Learning by living, memory and replay

- **Waking, online:**
  - A from the self-mirror (L_A);
  - R and W by LMS (L_R, L_W);
  - h inferred (H);
  - precisions as running residual variances.
- **Stored per episode** (segments of 30-120 s; Principle 7: features only):
  - the boundary streams y, f, b, u_del and transcript events;
  - the agent's own outputs (distillation targets);
  - the state tag σ_k in **innate coordinates**: x_B trajectory, v, a, ε_obs and its attribution a_e, and the inferred partner p, never a latent vector, so the tag survives encoder changes (memory-replay synthesis §1.9);
  - the eligibility e_k := ‖∇_θ(prediction losses)‖² at encoding.
- **Nightly replay** (memory-replay synthesis §2):
  - Priority is p_k = e_k · ∫_{t_k−W}^{t_k+W} a(t)dt, with W ≈ 1 h. Sampling mixes a coverage term and the priority term, with ratio ρ declared.
  - Context reinstatement (T2 in that synthesis) means h ← h̄_{p_k} and x̄ ← x̄_{p_k} while the fast core is re-run on the stored boundary streams.
  - Learned in replay: the basis maps {R_j, W_j}, h̄_p, x̄_p, V_θ, A's slow part, g and E_h. Distillation of the agent's own past outputs preserves temperament.
- **Derived here, not added:** replay is re-running the same energy ℰ_h on stored boundary data, and the reinstated tag is the partner's anchor and relation prior. So "state tagging" has a precise lesion: replay with h̄_p and x̄_p not reinstated. The predicted effect is partner specificity collapsing to a context-free average (memory-replay synthesis L1).
- **Declared constraints:** W, ρ, segment length, the lability window for re-tagging, and the replay budget.

### 5.8 The 16 elements of emotion (emotion-elements synthesis)

| # | Element | How it arises here | Derived or constraint |
|---|---|---|---|
| 1 | Concern grounding | U on the body coordinates; the same partner input moves x differently at different deficits because U's gradient enters the same stationarity equation | derived (U is innate) |
| 2 | Central persistent state | x, with slow modes from the anchor, the loop (Theorem 3(b)) and V_θ basins | derived |
| 3 | Valence | readout v = −dU/dt | derived readout |
| 4 | Intensity with regime switches | V_θ's nonconvex basins give hysteresis; the linear core alone cannot | constraint (V_θ class) |
| 5 | Pleiotropy | one x drives face (A_F), voice (A_V), draft selection, Claude's budget and replay tags | derived |
| 6 | Interoceptive prediction, allostasis | x_B is a predicted body; κ anticipates the body change from the partner's state; U acts on the prediction | derived |
| 7 | Precision | Π, P, Λ, K_s are learned inverse residual variances in the same energy | derived |
| 8 | Novelty and relevance checks | novelty is the obs and ρ components of the obstruction (contingency surprise), with the innate brow-raise reflex; conduciveness is the sign of W's prediction for U | partly derived; the reflex is a constraint |
| 9 | Agency and coping | who caused it is which edge carries the residual (ρ: "they did not answer my act as expected"; κ: "their state is not what my body predicts"); controllability is ‖R‖ (how much my acts move them) | derived readouts |
| 10 | Action readiness, interrupt | an obstruction threshold interrupts the current reply and recruits Claude (§5.6, item 2) | constraint (threshold) |
| 11 | Wanting vs liking | wanting is the need-weighted cue value ⟨∇U(x_B), W(h)z⟩ (does this partner cue predict relief of my current need), used as a precision boost on the obs edge for that channel; liking is the realised v on consumption. Lesions: drop the ∇U weighting, so approach is no longer need-gated while v remains; drop U's realised term, so v is lost while cue precision remains | the wanting gate on Π is a constraint; both quantities are derived |
| 12 | Learned elicitors | R and W by contingency (Theorem 5) | derived |
| 13 | Expression and social communication | A is the display; the partner's contingent response feeds the agent through z_y and the ρ residual | derived |
| 14 | Integration and comparator | the self-mirror loop (Theorem 4(d)); relief and disappointment as the sign of dε_obs/dt at the moment the predicted partner response arrives | partly derived |
| 15 | Conceptual categorisation | Claude names; reappraisal enters as Δh (§5.6, item 3), with a switch for the D1 test | constraint (interface) |
| 16 | Structure beyond valence and arousal | x is 64-dimensional; obstruction attribution is 5-dimensional; the loop spectrum is 8 complex numbers per partner; dial rank ≥ 2 | claim to test (D3 in that synthesis) |

### 5.9 The brief's expressive-structure items

- **Content-dependent selection.** Which partner directions reach the agent depends on content through im Aᵀ (what my body can produce), through W(h) and R(h) (what has mattered), and through need (the element 11 precision boost). Selection is of subspaces (a point on a Grassmannian, varying with h and need), not of softmax weights over tokens.
- **Structure over people, episodes and time.**
  - People: h̄_p and x̄_p per partner, and the shared basis {R_j, W_j}.
  - Episodes: tags in innate coordinates.
  - Time: lag traces, the loop delay, replay.
- **Effective dimensionality.** At an instant the partner influence has rank ≤ rank(S) ≤ rank R + n_b. Across relation states it has dial rank dim span{T_h} (generic upper bound k², reached only with enough basis maps). The ablation is to restrict h to one dimension (m = 1): dial rank ≤ 2 with one direction fixed, so Theorem 1(d)(i) and (ii) cannot both hold for two different channel pairs.
- **Richness from structure, not size.** About 105k learned parameters (§6.5).

---

## 6. A buildable network

### 6.1 Inputs and time encoding

| Stream | Rate | Dimension | Enters as |
|---|---|---|---|
| Partner face (MediaPipe blendshapes + pose and gaze) | 30 Hz | 58 | boundary of obs |
| Partner voice prosody | 100 Hz, pooled to 30 Hz | 8 | boundary of obs |
| Own sensed face and voice | 30 Hz | 66 | boundary of disp |
| Own body sensors | 30 Hz | 8 | boundary of sens |
| Transcript events | events | — | afferents; deliberate-route timing; words to Claude |

**Time encoding.**
- The object is a continuous-time energy flow, so time is not a position. Each 30 Hz frame is integrated in 4 semi-implicit Euler substeps (120 Hz): implicit in the linear sheaf part, explicit in ∇U and ∇V_θ.
- Lags for contingency learning use a bank of five exponential traces x̃_τ, τ ∈ {0.3, 0.6, 1.2, 2.4, 4.8} s. Each costs O(n) memory and is shift-equivariant (a causal convolution), so "what I did about τ ago" is available without storing a window.
- The delayed z_y(t) for (L_W) is kept in a ring buffer of τ_κ_max = 5 s (150 frames × 64).
- RoPE and ALiBi are not used because nothing here is an attention score. If attention were added for retrieval over episodes, ALiBi's recency bias would be the ordinary choice.

### 6.2 Layers in order (per frame)

| # | Operation | Size | Params | Carries the new structure? |
|---|---|---|---|---|
| 1 | Feature normalisation (running mean and variance) | 66 + 8 | 0 learned (stats) | no |
| 2 | Innate afferents → b update (clipped) | 8 | ~160 fixed | no (constraint) |
| 3 | Lag traces x̃_τ update | 5 × 64 | 0 | no |
| 4 | Relation maps R(h) = R₀ + Σ h_j R_j (rank-16 factors), W(h) = W₀ + Σ h_j W_j | R: 17 × (64×16 + 16×64); W: 17 × (8×64) | 34,816 + 8,704 | **yes** (two-edge loop) |
| 5 | Ceiling: Γ_h from (N) | scalar norms | 0 | **yes** (ceiling) |
| 6 | Fast sheaf solve: 4 substeps of (F1-F2), implicit in the quadratic part (one 128×128 Cholesky solve per substep, refactored only when h moves by more than a threshold), explicit ∇U, ∇V_θ | x, z ∈ ℝ⁶⁴ | A: 66×64 = 4,224; precisions 210 | **yes** (A shared on obs and disp; ρ and κ edges) |
| 7 | V_θ: MLP 64 → 128 → 128 → 1, SiLU, gradient by autograd or analytic | — | 24,961 | no (ordinary) |
| 8 | Readouts: v, ε_obs, a_e, a | — | 0 | **yes** (obstruction attribution) |
| 9 | Relation inference: one gradient step of (H) | 16 | priors 16 + 64 per partner | partly |
| 10 | Online learning: LMS on A, R, W coefficients, precisions | — | (same as above) | the targets are the structure (Theorem 5) |
| 11 | Muscle layer: two routes (emotional A_F x + Θ_r y; deliberate D_del u_del), inhibition g_inh, first-order units | 52 | Θ_r: 6 fixed; D_del: 780; g_inh: 52 | no (structure from neurology, ordinary math) |
| 12 | Voice prosody controls from A_V x → TTS | 8 | (in A) | no |
| 13 | Claude interface: frozen sentence encoder (existing, ~22M, not counted); g: 384 → 66; E_h: 384 → 16 | — | 25,410 + 6,160 | no (shared interface) |

**Learned total:** about 4.2k (A) + 0.2k (precisions) + 34.8k (R basis) + 8.7k (W basis) + 25.0k (V_θ) + 0.8k (D_del) + 0.05k (g_inh) + 31.6k (Claude heads) ≈ **105k**, plus 80 per partner.

### 6.3 What is learned where

| Part | Online (waking) | Replay (nightly) |
|---|---|---|
| A | fast component, self-mirror LMS | slow component, distillation |
| R₀, W₀ coefficients in the current h direction | LMS (L_R, L_W) | — |
| Basis {R_j, W_j} | frozen | learned on reinstated episodes |
| h | inferred (H) | reset to h̄_p at the start of each session |
| h̄_p, x̄_p | frozen | learned (average inferred h; anchor as the long-run mean of x with the partner) |
| V_θ | frozen | learned (§6.4) |
| Precisions | running variances | consolidated |
| g, E_h | frozen | learned |

### 6.4 Training objectives (none targets the partner's face with the agent's face; none rewards the partner)

- 𝓛_A = Σ_t ‖f(t) − A x(t)‖²: the self-mirror.
- 𝓛_R = Σ_t min_τ ‖z_y(t) − R(h_t) x̃_τ(t)‖²_P: contingency.
- 𝓛_W = Σ_t ‖Δb(t+τ_κ) − W(h_t) z_y(t)‖²_Λ: consequence for the body.
- 𝓛_V (replay only): backpropagation through 10-s windows of the flow (F2) with the stored boundary streams. The loss is Σ_{Δ∈{1,10,60 s}} ‖b(t+Δ) − φ_Δ(C_B x(t))‖² + ζ‖∇²V_θ + σI‖_−, i.e. body prediction at three horizons plus a penalty keeping the Hessian bound of Lemma 1 (φ_Δ are fixed linear decays toward set points).
- 𝓛_dist (replay): ‖A x_replay − A x_stored‖² on old episodes, so the agent's own past responses are preserved (temperament across days; memory-replay §1.4).
- 𝓛_g (replay): ‖ĝ(d_spoken) − f(t over the utterance)‖², learned from the agent's own speech.
- 𝓛_Eh (replay): ‖E_h(text) − h*_{after}‖², where h*_{after} is the relation inferred in the following minute.

### 6.5 Latency and memory on this Mac (M1 Pro, 16 GB; ≤ 6 GB peak)

- **Per frame, fast core** (operation counts, not measured): one 128×128 triangular solve (~16k multiply-adds) × 4 substeps, the V_θ forward and backward (~2 × 25k), and R(h), W(h) products (~2 × 64 × 64 × 2). That is under 0.5 M FLOPs per frame, well under 1 ms on one CPU core in PyTorch eager.
- The Cholesky refactor (128³/3 ≈ 0.7 M FLOPs) runs only on h changes.
- Face tracking and TTS dominate the loop's latency. They are measured separately (machine.md budget); the core adds less than 1 ms. The fast loop never waits for Claude (Principle 4).
- **Memory, waking:**
  - the model: under 1 MB of parameters;
  - the ring buffers: 150 × 64 floats;
  - MediaPipe and TTS processes: their own footprint, to be measured.
  - Under 1 GB in total is expected.
- **Replay:** 256 windows × 300 frames × ~210 feature dims × 4 B ≈ 65 MB of data per batch; autograd through 300 steps × 256 × 128 states ≈ 40 MB. Peak under 0.5 GB.
- **Disk:** about 210 float16 features at 30 Hz is ~12.6 KB/s, about 136 MB per 3-hour day. machine.md reports 55 GiB free against a lowered 10% floor, so the episode store is capped (proposed: 15 GB, pruned by lowest priority p_k after consolidation).

### 6.6 Ablation switches (each is one line in the build)

| Switch | Removes | Predicted effect (from the theorems) |
|---|---|---|
| κ off (Λ = 0) | consequence link | coregulation (damped oscillation after a perturbation) disappears; fast mimicry intact (Theorem 6(a)) |
| ρ off (P = 0) | contingency link | the early learned mimicry beyond the reflex core disappears; coregulation can remain (Theorem 6(b)) |
| A_c := 0 | the agent's production of channel c | the partner's channel c no longer affects state (Theorem 4(b)) |
| h frozen | relation inference | context effects only from pre-set relations (order 3); no new-context effects (Theorem 3(a)) |
| m = 1 | relation basis to one dimension | cannot produce both the Bourgeois-Hess and the Hofman pattern (§5.9) |
| reinstatement off in replay | state tagging | partner specificity collapses (memory-replay L1) |
| emotional route off / deliberate route off | face routes | emotional / volitional palsy pattern |
| Claude → h off | reappraisal path | D1 test in the emotion-elements synthesis |

---

## 7. Novelty test

### 7.1 Every computational part and the existing mechanism it is

| Part | Existing mechanism | Read? |
|---|---|---|
| Cellular sheaf, coboundary, Laplacian, harmonic extension, stubborn vertices | Hansen & Ghrist 2019, 2021 | yes (2021 §3-5, 8, 9, 12 in the original; 2019 via note) |
| Quadratic sheaf energy with linear maps = MAP in a Gaussian Markov random field | standard (any Gaussian factor graph) | — |
| Holonomy and its effect on dim H⁰ | Bodnar et al. 2022, Prop. 4-5, Lemma 6 (for O(d) bundles) | yes |
| Stubborn anchor tied to the influence weights | Friedkin-Johnsen with the coupling condition (Parsegov 2017) | note; the FJ originals unread |
| LMS / Rescorla-Wagner updates | delta rule; ASL (Ray & Heyes; Cook et al.) | notes |
| Context inference over a basis of maps | COIN-like context inference; FiLM-style conditioning | not read for this design; named only |
| Perception by inverting one's own generative map | predictive coding; Yoshida & Man (via brief) | not reread here |
| Delay-differential loop analysis | standard DDE theory (characteristic equation, Lyapunov-Krasovskii) | textbook facts, proofs given |
| Two face routes into one muscle layer | the neurology in the face-development synthesis | notes |
| Draft selection, thinking budget, retrieval as the Claude interface | shared interface (sketches/v2-README.md) | — |
| CLS replay with tag reinstatement and distillation | McClelland 1995; van de Ven 2020; Rolnick 2019 (memory-replay synthesis) | notes |

### 7.2 Against Hansen & Ghrist's discourse sheaves, exactly

Their paper already has, in the original:
- private stalks and edge expression stalks;
- signed restriction maps ("lying", "agreement to disagree");
- stubborn agents as harmonic extension (Theorem 5.1);
- restriction-map learning by discord descent (Theorem 8.1);
- joint opinion and expression diffusion with the conserved diagonal blocks (Theorem 9.3);
- bounded-confidence and antagonistic nonlinear Laplacians.

What this design adds, each with its proof here:
1. **Two edges with different meanings and different learning targets between the same pair**, forming a loop whose monodromy is gauge-invariant. Their graphs are simple, and all their edges are equal-time agreement edges.
2. **Frame pinning by a shared production map** on the self and partner-reading vertices (Theorem 1(a)). In their model each agent's maps are its own, and nothing ties my reading of you to my own expression map.
3. **Learning targets that a display cannot fake** (Theorem 5), replacing their discord descent, which their own Theorem 8.1 shows learns to lie.
4. **The loop-class theorem** (Theorem 6), the persistence bound (Theorem 3(b)), the onset-order theorem (Theorem 3(a)) and the copy margin (Theorem 1(b)).

None of these is a new operation on vectors. Items 1-3 are structural choices, and item 4 is analysis.

### 7.3 Verdict

**Recombination, not a new computation.** The fast core at a fixed relation is a Gaussian MRF on a cellular sheaf, solved by gradient flow. The learning rules are delta rules. The relation is context-weighted basis maps. Replay is complementary learning systems.

Under the second clause of the new-mechanisms synthesis (what changed what is computed: an invariant or a removed knob), the design has three candidate contributions:
- **(i)** the gain knob is removed in favour of a ceiling plus learned directions, with a proved copy margin (Theorem 1(b)), where FJ already has the ceiling;
- **(ii)** frame pinning, which closes the "copy in a frame" loophole by a structural tie (Theorem 1(a));
- **(iii)** a derived classification of dyadic regimes by the spectrum of a composition of two separately learned maps, with "learned mimicry is always contagion" as a theorem (Theorem 6).

(iii) is the closest to new. The nearest prior is HKB's sign parameter μ, which is a scalar set by hand.

These are derived invariants on a recombined core, not a new primitive like attention or RoPE.

---

## 8. Weak points and what would falsify it

### 8.1 Weak points

1. **The core is linear where the theorems hold.** V_θ is the only nonlinearity, and every theorem is for the linear core or holds locally under a Hessian bound. Emotional regime switches (element 4) live entirely in V_θ, where nothing is proved.
2. **The ratio of two learned precisions can flip a loop class** (Theorem 6(b)). If P or Λ is misestimated, for example because the operator's contingencies are sparse, the agent is in the wrong class. This is where a "dial" survives: a measured ratio rather than a setting, but a single number per mode.
3. **The consequence link is narrow.** W maps into 8 body coordinates, so contagion through κ has rank ≤ 8. Rich *own* expression comes from x_ℓ, but rich *partner-driven* change of state is bottlenecked by design. That may be too thin for the variety of reactive emotion in the mimicry data.
4. **ASL needs being imitated.** An adult operator will not imitate the agent once a minute (Ray & Heyes, via note). If R stays near 0, the only fast mimicry is the reflex core. The design states this, and it does not hide it behind an innate copy map.
5. **The partner is read in the agent's coordinates.** By Theorem 4(b), partner states the agent's body cannot express are invisible. That is the principle, but it also means the agent cannot represent, for example, a partner's expressive style that differs from its own.
6. **No intentional regulation** (Theorem 2(c)). Coregulation is a property of the loop, never an act. Whether a loop learned from a few hours a day becomes negative (coregulatory) at all is unknown. Butler & Randall themselves say adult coregulation is not established.
7. **The ceiling ϑ is a declared constant.** It does not run flat to copy (Theorem 1(e)), but a critic can still call it a gain on the partner share. The defence is that the endpoint at any ϑ is the learned profile, never the copy.
8. **Theorem 7's bound uses the agent's model of the partner.** A real partner who amplifies strongly can still destabilise the closed loop. The guarantee is only as good as ‖R_true‖ ≤ ‖R‖ + error.
9. **The Claude interface is the shared, recombined one** and may be inert (the draft-collapse risk in the v2 linguist critique). The reappraisal-into-h path is new plumbing with no evidence.
10. **The egocentric bias** (Theorem 4(c)) is proved, but its size in practice is unknown. If Λ is large relative to Π, the agent reads its own state into the partner.
11. **The onset-order claim assumes a rest point.** Live conversation is never at rest. Order-of-onset predictions then hold only for perturbations small relative to the ongoing signal.

### 8.2 What would falsify it (state-level tests, after a build is chosen; no simulated world counts)

- **F1, double dissociation (Theorem 6).** Perturb the dyad (a still-face episode, or a scripted partner laughter onset) and score Butler & Randall's four criteria on the agent's state x_B.
  - With κ off: damped oscillation after the perturbation should vanish, while the early lip-corner and brow coupling beyond surrogates (E3) remains.
  - With ρ off: the reverse.
  - Falsified if both lesions remove both effects, or neither does.
- **F2, crossed contingency (Theorem 5(c)).** Over sessions, a partner (recorded and replayed contingently on the agent's acts, or a confederate) systematically crosses the agent's displays on two channels. R on those channels should flip sign, the agent's early response should counter-mimic on exactly those channels and not others, and spec M_B should move accordingly. Falsified if mimicry does not reverse, or reverses on all channels together (that would be a hidden scalar).
- **F3, steering dial rank (Theorem 1(d)).** Inject Δh along each basis direction and a random-direction control. Measure the state Jacobian T_h per channel. The prediction is non-proportional changes across channels (dial rank ≥ 2) and a sign change in at least one entry with others fixed. Falsified if every injected direction scales T_h by a common factor.
- **F4, persistence vs loop closure (Theorem 3(b)).** After the partner leaves, the decay rate of the agent's shared-state component should be predicted by ‖(C_B − WR)x‖²_Λ from the learned maps, better than by a fixed time constant, across sessions and partners.
- **F5, adjoint lesion (Theorem 4(b)).** Set A_c = 0 for one channel. The partner's channel c should lose all coupling to the agent's z and x beyond surrogates, while other channels keep theirs. Falsified if coupling to c survives.
- **F6, onset order (Theorem 3(a)).** For known versus newly inferred relations, measure the first lag at which the agent's response differs between relation conditions. Known context should differ by the emotional-route latency; new context only later. Falsified if new-context effects arrive as early as known-context ones.
- **F7, coupling beyond surrogates (evaluation E3).** Real pairing against partner-swap and segment-shuffle surrogates, scored on x and z as well as the face. This is the general check that the partner enters the state, not just the output.
- **F8, replay specificity (memory-replay L1 vs sham).** Replay without reinstating h̄_p and x̄_p should collapse operator-versus-stranger specificity, and a sham with random tags should match it.

What would *not* count: face matching to human video, rater preference, or any simulated partner written for this project.

---

## Critique 1 and answer (recorded 2026-11-25T13:14:59Z)

**The critique** (independent; full text in critique-design-dyadic-sheaf.md; the algebra checks in sims/critique-dyadic-sheaf/check.py are not evidence):
- **Proofs:** 28 items checked: 12 valid, 7 gaps, 9 errors.
- **The worst error.** The copy margin holds only when the learned maps are the copy maps. The ceiling caps the weight of the partner edges, not the size of what they pull toward. With a learned R = r·I, the transfer from the partner's face to the agent's own face is a single scalar gain on a copy: it runs from 0 through exact copy (at r ≈ 0.02 and 0.31) to a peak of 2.04.
- **Other errors:**
  - The contingency rule learns R ≈ 9.5 from a partner who never responds: it learns the agent's own following as the partner's contingency.
  - The onset-order theorem fails: the new-context route is also t³, not t⁴.
  - The ceiling cancels the claimed (1−μ)⁻² persistence.
  - The loop spectrum changes under the design's own gauge group.
- **The dial: yes.** The ceiling ϑ is the dial, with gain T = ϑk/(k+(1−ϑ)q) on the copy maps. Further dials: the anchor floor γ₀, the learned scale of R or W, and the facial-feedback precision acting on the innate reflex.
- **Novelty: recombination,** confirming the author.
  - The ceiling is Friedkin–Johnsen susceptibility.
  - Frame pinning is a vacuous invariance.
  - The loop-class result is a correct but conditional linear lemma.

**The design's answer:**
- **Accepted:** the dial (ϑ and the learned scale of R), and the confound in the contingency rule.
- **Withdrawn:** the copy-margin theorem as stated, the frame-pinning claim, and the t⁴ onset order.
- **Revision owed:**
  1. bound and prove the face-to-face transfer itself, not the edge weight;
  2. learn R from lagged, exogenous variation (instrumental variables), so the agent's own following is not read as the partner's contingency;
  3. re-derive persistence with the ceiling in place.
- **Kept as a useful lemma:** the classification of dyadic regimes by the spectrum of the loop between the two learned maps (correct but conditional). The contingency confound found here applies to any design that learns from contingency.
- **Status:** critiqued. The core claim failed; held for revision.
