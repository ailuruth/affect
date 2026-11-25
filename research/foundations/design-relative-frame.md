# Design: Relative-frame transport (RFT)

Written 2026-11-25 for operator notes Q16 and Q17, by an isolated design author. No other design-*.md written this cycle was read.

**Sources read for this design, in the original:**
- Su et al. 2021, RoFormer, arXiv 2104.09864 v5: §2-3.4 (re-read for this design; the project's note su-2021-roformer-rope.md was checked against it).
- Löwe et al. 2022, Complex AutoEncoder, arXiv 2204.02075: §2-3.5 and Table 1.
- Löwe et al. 2023, Rotating Features, arXiv 2306.00600: §3, §4.4, §5-6.
- Merrill, Petty & Sabharwal 2024, "The Illusion of State in State-Space Models", arXiv 2404.08819 v3: §2.1, §4-5.2 (Definition 2.1, Lemma 4.1, Theorems 4.2, 4.4, 4.6, Corollary 4.7, Theorems 5.1-5.2).
- Grazzi et al. 2025, "Unlocking State-Tracking in Linear RNNs Through Negative Eigenvalues", arXiv 2411.12537 v5: abstract, §4.1-4.3 (Theorems 1-4, Proposition 1).

**Project notes relied on:** su-2021-roformer-rope.md, lowe-2022-2023-complex-autoencoder-rotating-features.md, sun-2024-test-time-training-layers.md, the three sheaf notes, altafini-2013-signed-consensus.md, math-objects-synthesis.md, mimicry-context-synthesis.md, coordination-synthesis.md, face-development-synthesis.md, emotion-elements-synthesis.md, new-mechanisms-synthesis.md and known-failures.md.

**Not read, and possibly closest on the position-encoding side:**
- Learned-generator rotary encodings: LieRE (Ostmeier et al. 2024), ComRoPE, STRING.
- Rotating values as well as queries and keys ("VO-RoPE").
- Unitary RNNs (Arjovsky et al. 2016).

They must be read before the novelty verdict in §7 is final. Nothing below rests on them.

**Numerical checks.** Small numeric checks of my own equations were run in a scratch directory (numpy, this Mac). They test algebra only and are not results.

---

## 1. Plain-language intuition

When you see someone frown, three different things can happen in your face. You can frown back (matching). You can see the frown clearly and do nothing with your face (holding it). Or you can answer it with the opposite, a soothing smile or a satisfied look at a rival's distress (countering). The literature in mimicry-context-synthesis.md says people do all three, separately for each expression and each partner, and a single "how much do I copy" knob cannot produce that. Every one of the project's twelve earlier sketches had such a knob, and its two ends were a flat face and a copy.

RFT replaces "how much" with "which way".
- **Reading.** Every expression of the partner is first read through the agent's own body, as the muscle command the agent would need to make that face itself.
- **Turning.** That command is then *turned*, not scaled, before it reaches the agent's own face. Each perceived expression is a vector in a doubled space with two halves:
  - an **enacted** half, which drives the agent's muscles;
  - a **held** half, which the agent registers and keeps but does not show.
- **Stance.** The turn is a rotation, so it never changes the length of the vector. Matching is no turn. Holding is a quarter turn. Countering is a half turn.
- **What a relationship is.** The relationship with a partner is the particular rotation the agent applies, with a different turn for each pattern of expression. The rotations form a group, the unitary group U(K). Copying is one point of it: the identity. It is not the end of a dial.

Three consequences matter.
1. **Stance never costs perception.** However the agent stands toward a partner, the partner's expression is registered in full; only its split between enacted and held changes (Theorem 1a). Tracking the partner and aligning with the partner are therefore separate (Hoehl et al. 2021, coordination-synthesis §1e). Going from matching to countering passes through holding, never through not seeing.
2. **Every response starts at matching and turns.** When something surprising happens on the partner's face, the agent's applied rotation is pulled back toward the identity (reflex matching). It then turns again toward the learned relation over about a second. Fast matching followed by slower context, as Carr et al. 2014 and Weyers et al. 2009 report, is a path on the group. A predictable expression causes no pull back, so context shows from the start, as Mauersberger et al. 2022 found for laughter.
3. **The relation is learned from the agent's own body, not from the partner's approval.** The rotation for a partner is learned so that the partner's turned expression predicts what the agent's own body is about to express. The agent "feels" this through innate synergies of its body variables. Consequences:
   - A partner whose smiles precede the agent's own relief gets their smiles matched.
   - A partner whose expressions say nothing about the agent's body gets them held.
   - Copying is learned on a channel only if the partner's expression predicts the agent's own reaction at least one to one (Theorem 1d).

   Nothing here rewards the partner's smiles.

A frame objection, raised in math-objects-synthesis.md, applies to any design of this kind: on a single dyadic edge, a fixed rotation is only a change of coordinates, so "copy in a rotated frame". RFT escapes it three ways, each proved in §3:
- what reaches the muscles is the real part of a rotation, which is generally not itself a rotation;
- the applied rotation moves along a path that passes through the identity, and that pins the coordinates;
- the rotation is a function of the partner, the gaze target, the episode and the agent's history, not a constant.

What is not new: rotating vectors by learned group elements, complex activations with phase as a second message, and online learning of a weight by gradient on a self-supervised loss all exist (§7). The design's claim is narrower: a derived invariant (Theorem 1a) removes the gain, and with it the flat end, as a free quantity. The theorems in §3 say exactly where copying and flatness can still occur.

---

## 2. The precise object

### 2.1 Spaces

| Symbol | Space | Meaning |
|---|---|---|
| t | ℝ (seconds) | continuous time; frames arrive at about 30 Hz with real timestamps |
| K | integer, K = 32 | number of the agent's own motor channels: 28 face (action-unit-like muscle groups of its own face) + 4 voice (speech rate, pitch shift, gain, pause length) |
| 𝕄 = ℝ^K | motor space | the agent's own muscle and voice commands |
| 𝕍 = ℂ^K = 𝔼 ⊕ iℍ | complexified motor space | 𝔼 = ℝ^K (real part: **enacted**), ℍ = ℝ^K (imaginary part: **held**) |
| 𝕆 = ℝ^66 | observation space | partner features per frame: 52 blendshapes, 6 head-pose values, 8 prosody features |
| G = U(K) | unitary group | relations; dim_ℝ G = K² = 1024 |
| 𝔤 = 𝔲(K) | Lie algebra | skew-Hermitian K×K matrices X* = −X; write X = B + iA with B real skew, A real symmetric |
| b ∈ ℝ^4 | body variables | energy budget b_E, integrity load b_I (sensory intensity: loudness, looming), expressive effort b_F (muscle and voice fatigue), learning progress b_P (curiosity as a satiable variable, the project's D62 definition) |
| s = (s_f, s_m, s_s) ∈ ℝ^128 × ℝ^64 × ℝ^32 | latent state | fast, middle and slow recurrent state; no unit is named |
| P | finite set, growing | partners met so far, indexed by an identity embedding (§5.1) |

Inner product on 𝔤: ⟨X, Y⟩ = Re tr(X*Y). Operator norm ‖·‖. Real part acts entrywise: for r = M + iN with M, N real, Re r = M and Im r = N.

### 2.2 Maps

**(M1) Own forward model.** F_ω: 𝕄 → 𝕆 is a small network that predicts what the agent's own face and voice look and sound like for a motor command. It is learned from self-observation: the agent's rendered face is passed through the same face tracker, and its own voice through the same prosody front end.

**(M2) Own inverse model (correspondence).** C_ω: 𝕆 → 𝕄 is an amortized inverse of F_ω, trained so that C_ω(F_ω(m)) ≈ m and F_ω(C_ω(o)) ≈ o. **Partner motor image:**

  m̂(t) = π(t) · C_ω(o(t)) ∈ 𝕄,

where π(t) ∈ [0, 1] is the perceptual precision: face-detection confidence times visibility. It is not learned and not a relation.

**(M3) Innate body-driven expression.** Y: ℝ^4 × ℝ^4 → 𝕄, with y(t) = Y(b(t), ḃ(t)), is a fixed innate synergy map (face-development-synthesis §4, items 1-2):
- smile synergy (lip-corner pull recruiting cheek raise) driven by drive reduction, −dΦ/dt > 0;
- cry/distress synergy (brow lowering, eye constriction, mouth opening scaled by rising drive);
- an orienting brow raise driven by learning-progress spikes;
- lid droop driven by low energy.

There are no emotion templates. Y is the "what my body does by itself" signal.

**(M4) Drive.** Φ(b) = Σ_i w_i ψ_i(b_i − b_i*), with ψ_i(x) = (|x| − δ_i)_+² and fixed set points b_i*, dead bands δ_i > 0 and weights w_i > 0.

### 2.3 The relation and its levels

The relation the agent currently holds toward partner p, given gaze directedness γ ∈ [0, 1] (is the partner's expression aimed at the agent?), is

  r(t) = R_T · Δ_p(γ(t)) · R_ep(t) ∈ U(K),   (R)

with three factors:
- **R_T ∈ U(K): temperament.** It changes only in replay (§2.6).
- **Δ_p(γ) = Δ_p^away · Exp(γ · Log((Δ_p^away)* Δ_p^at)): partner deviation.** Two learned elements per partner (aimed at me, aimed elsewhere), joined by the geodesic. A new partner starts with Δ_p^at = Δ_p^away = I.
- **R_ep(t) ∈ U(K): episode relation.** It decays toward I, which means toward the partner level, never toward copy or flat.

Log is the principal logarithm on U(K): for unitary U = V diag(e^{iθ_k}) V* with θ_k ∈ (−π, π], Log U = V diag(iθ_k) V*. It is defined everywhere and is continuous except where some θ_k = π (see weak point W5). Write L(t) = Log r(t).

### 2.4 The applied frame and the transport (the core dynamics)

The agent does not apply r directly. It applies a frame g(t) ∈ U(K) that relaxes along the group toward r and is pulled back toward the identity by surprise:

  ġ = g · X,  X = (1/τ₀) Log(g* r) − ν(t) Log g,   (F)

where:
- τ₀ = 1.2 s is innate, chosen in the 1-4 s band of Carr 2014 and Weyers 2009;
- ν(t) ≥ 0 is the **surprise rate**: ν(t) = ν₀ · ‖m̂(t) − m̂_pred(t)‖² / (σ̄² + ‖m̂(t) − m̂_pred(t)‖²), where m̂_pred is a two-lag linear predictor of the partner motor image and σ̄² a running scale.

The update is integrated with the exponential map g ← g · exp(dt · X), which stays exactly on U(K) for any dt, so dropped frames do not break it.

**Transport.** The partner's motor image is moved into the agent's frame:

  z(t) = g(t) m̂(t) ∈ 𝕍,  e(t) = Re z(t) (enacted),  η(t) = Im z(t) (held).   (T)

**Own expression and display.**
- The agent's own anticipatory expression is a(t) = A_ω(s(t)) ∈ 𝕄.
- Its display frame is Γ(t) = exp(L_Γ(t)) ∈ U(K), with L_Γ produced by the deliberate system (§5.4). Display rules rotate expression into the held half; they do not subtract it.
- The emotional-route drive and the held content are

  u_emo(t) = Re(Γ(t)(a(t) + z(t))),  h(t) = Im(Γ(t)(a(t) + z(t))).   (E)

**Agreement** between the agent's own affect and the transported partner, used by memory and by the Claude interface:

  κ(t) = Re⟨Γa, Γz⟩ = Re(a* z).

### 2.5 Body, muscles and latent

- **Muscles.** μ ∈ [0, 1]^K with τ_m μ̇ = −μ + sat(W_syn u_emo + u_del + c_ref), where:
  - τ_m = 60 ms;
  - W_syn is a fixed innate synergy coupling;
  - u_del is the deliberate route (§5.4);
  - c_ref is the output of the innate reflex pattern generators (startle, blink, laugh burst).
- **Body.** ḃ = f_b(b, μ, o, events). This is innate:
  - energy falls with activity and recovers at rest;
  - integrity load rises with the loudness and looming of the input and decays;
  - effort rises with muscle and voice use;
  - b_P is learning progress, the smoothed decrease of the latent's own prediction error.
- **Latent.** s_f, s_m and s_s are gated recurrent units (§6) fed by [b, b − b*, dΦ/dt, e, η, μ, h, prosody, text-event projection]. The slow unit runs at 1 Hz.

### 2.6 Learning (what changes and on what signal)

**(L1) Relation loss.** The partner's transported expression should predict the part of the agent's own coming body-driven expression that the agent's own state does not already anticipate:

  ℓ(r) = ‖Re(r m̂(t)) − ỹ(t)‖²,  ỹ(t) = y(t + Δ) − sg[a(t)],  Δ = 1 s,

where sg is stop-gradient and ỹ is the residual target. The Riemannian gradient on U(K), right-trivialised, is

  Ξ(r) = ½ (r* ε m̂ᵀ − m̂ εᵀ r) ∈ 𝔲(K),  ε = Re(r m̂) − ỹ.   (G)

Derivation:
1. For X ∈ 𝔤, (d/dλ) Re(r e^{λX} m̂)|₀ = Re(r X m̂).
2. So dℓ = 2 εᵀ Re(r X m̂) = 2 Re tr(m̂ εᵀ r X) = 2⟨W, X⟩ with W = (m̂ εᵀ r)* = r* ε m̂ᵀ.
3. Projecting W onto 𝔤 gives (W − W*)/2 = Ξ.

The numeric check against central finite differences agreed to 10 digits.

**Updates of each level:**
- **Episode level, online:** R_ep ← R_ep exp(−η_ep dt Ξ_ep − λ_ep dt Log R_ep). Ξ_ep is (G) taken at the episode factor; leak rate λ_ep ≈ 1/(2 min).
- **Partner level, online with a small rate and in replay with a larger one:** Δ_p^c ← Δ_p^c exp(−η_p Ξ_p). The gaze-selected factor c ∈ {at, away} receives the gradient split by γ. There is no leak.
- **Temperament, replay only:** the log-Euclidean barycenter of the total relations,

  R_T ← Exp(Σ_p w_p Log(R_T Δ_p)),

  with w_p proportional to experience with p. After each move every Δ_p is re-centred, Δ_p ← R_T,new* R_T,old Δ_p, so each partner's total relation is unchanged and the shared part moves into R_T. A new partner starts at the temperament, the "stranger relation".
- **Text events.** Each transcript segment (the partner's words, or Claude's own spoken words) with sentence embedding x applies R_ep ← R_ep exp(G_ψ(x)). G_ψ: ℝ^384 → 𝔤 is low rank: G_ψ(x) = U_ψ(x) diag(iλ_ψ(x)) U_ψ(x)*, with U_ψ ∈ ℂ^{K×4}. It is trained in replay to predict the episode update that the following 30 s of living actually produced, Log(R_ep(t + 30 s) R_ep(t)*). This is the switchable route for reappraisal by the conceptual layer (§5.5).
- **Ordinary parts** (F_ω, C_ω, A_ω, latent, body predictor, policy): §6.

---

## 3. Theorems and proofs

Throughout, m ∈ ℝ^K is a partner motor image (π included), r ∈ U(K), M = Re r and N = Im r.

### Lemma 0 (unitary structure)

r ∈ U(K) iff MᵀM + NᵀN = I and MᵀN is symmetric. Also MMᵀ + NNᵀ = I.

*Proof.*
1. r*r = (Mᵀ − iNᵀ)(M + iN) = (MᵀM + NᵀN) + i(MᵀN − NᵀM).
2. r*r = I iff the real part is I and the imaginary part vanishes, i.e. MᵀN = (MᵀN)ᵀ.
3. rr* = I gives the last identity the same way. ∎

### Theorem 1 (T1): what RFT has instead of a flat-to-copy dial

**(a) Conservation (the dilation identity).** For every r ∈ U(K) and every m ∈ ℝ^K,

  ‖Re(r m)‖² + ‖Im(r m)‖² = ‖m‖².

The set of enacted transfers {Re r : r ∈ U(K)} is exactly the closed operator-norm unit ball 𝔅 = {M ∈ ℝ^{K×K} : ‖M‖ ≤ 1}.

*Proof.*
1. r is an isometry of ℂ^K, so ‖rm‖ = ‖m‖. Since m is real, Re(rm) = Mm and Im(rm) = Nm, and ‖w‖² = ‖Re w‖² + ‖Im w‖². This gives the identity.
2. Hence ‖Mm‖ ≤ ‖m‖, so M ∈ 𝔅.
3. Conversely, take M ∈ 𝔅 with singular value decomposition M = U diag(c_k) Vᵀ, c_k ∈ [0, 1]. Set φ_k = arccos c_k and r = U diag(e^{iφ_k}) Vᵀ. Then r is unitary and Re r = U diag(cos φ_k) Vᵀ = M. ∎ (Checked numerically on random contractions to 4·10⁻¹⁶.)

*Reading.*
- The partner's total registered magnitude is π‖C_ω(o)‖, whatever the relation. The relation decides only the split.
- No setting of the relation makes the partner disappear from the agent. "Flat" in the face (Re r m = 0) always comes with ‖η‖ = ‖m‖ in the held channel.

**(b) Where a single gain still lives.** For unit u ∈ ℝ^K, the enacted share of a partner expression in direction u is c_r(u) = ‖(Re r)u‖² ∈ [0, 1], and the held share is 1 − c_r(u).
- c_r is independent of u (one scalar "amount of the partner" for every expression) iff Re r = cos θ · O for some O ∈ O(K) and θ ∈ [0, π/2].
- The set 𝒵 of such r is r = O exp(iθJ), with O ∈ O(K), θ ∈ [0, π] and J a symmetric involution (Jᵀ = J, J² = I).
- dim 𝒵 ≤ K(K−1)/2 + 1 + ⌊K²/4⌋ < K² for K ≥ 2. For K = 32 that is 753 against 1024. So 𝒵 is a closed set of measure zero in U(K).

*Proof.*
1. c_r(u) = uᵀMᵀMu. It is constant on the unit sphere iff MᵀM = c I, i.e. M = √c O with O orthogonal. Write √c = |cos θ|.
2. By Lemma 0, NᵀN = I − MᵀM = sin²θ I. If sin θ ≠ 0, N = sin θ · O′ with O′ orthogonal. MᵀN = cos θ sin θ · OᵀO′ must be symmetric. If cos θ ≠ 0, then J := OᵀO′ is symmetric and orthogonal, so J² = JᵀJ = I.
3. Then r = O(cos θ I + i sin θ J) = O exp(iθJ), using J² = I in the exponential series. The edge cases θ = 0 and θ = π/2 are included with J arbitrary.
4. Dimension count:
   - O(K) has dimension K(K−1)/2;
   - θ adds 1;
   - symmetric involutions with a k-dimensional −1 eigenspace form the Grassmannian Gr(k, K), of dimension k(K−k) ≤ ⌊K²/4⌋;
   - the map (O, θ, J) ↦ r is smooth, so its image has dimension at most the sum.
5. The sum is 3K²/4 − K/2 + 1 < K² iff K²/4 + K/2 − 1 > 0, which holds for K ≥ 2. A finite union of images of lower-dimensional manifolds under smooth maps has measure zero. ∎

**(c) The copy-in-a-frame objection, answered (gauge pinning).** The objection (math-objects-synthesis §1): on a single edge, an invertible group-element coupling is a change of frame, hence copying in disguise, by Bodnar Lemma 6, the Altafini gauge and Schur. RFT's enacted coupling escapes it three ways.

1. **The enacted coupling is a compression, not a group element.** The map from partner image to muscles is Re r = P_𝔼 r ι, with ι: ℝ^K → ℂ^K the inclusion and P_𝔼 the real-part projection. By (a) it is an orthogonal matrix, a frame change, iff N = 0, i.e. r ∈ O(K). O(K) has dimension K(K−1)/2 < K², so measure zero in U(K). Otherwise Re r has singular values cos φ_k that differ from one another and from 1. It is rank-reducing in the sense of the math synthesis's escape route 1: the complement is sent to ℍ, which the muscles never see.

2. **The applied frame moves through a one-parameter subgroup, which pins the gauge.**
   - *Setting.* After a surprise the frame g(t) is pulled toward I, and between surprises it relaxes toward r. When r is constant and g starts at I (or anywhere on {exp(sL)}), (F) keeps g on the geodesic g(t) = exp(s(t)L), with s(t) ∈ [s_min, 1] (Proposition 3b).
   - *Claim.* There is a fixed matrix D and a scalar function c(s) with Re exp(sL) = c(s)D for all s in some open interval iff either L = 0, or L = iaJ with a ∈ ℝ and J a symmetric involution. In both cases D ∝ I and Re exp(sL) = cos(sa) I.
   - *Proof.*
     1. s ↦ Re exp(sL) is real-analytic on ℝ.
     2. If Re exp(sL) = c(s)D on an interval with D ≠ 0, then c(s) = ⟨D, Re exp(sL)⟩/‖D‖² is analytic. So Re exp(sL) − c(s)D vanishes on all of ℝ by the identity theorem.
     3. At s = 0: I = c(0)D, so D = I/c(0).
     4. Hence Re(Lⁿ) ∝ I for all n ≥ 1: these are the derivatives at 0.
     5. With L = B + iA: n = 1 gives B = βI, and B is skew, so B = 0.
     6. Then Lⁿ = iⁿAⁿ. For n = 2, −A² ∝ I, so A² = a²I and A = aJ with J² = I.
     7. Conversely, for L = iaJ, exp(sL) = cos(sa)I + i sin(sa)J, so Re exp(sL) = cos(sa)I. ∎
   - *Reading.* Over the course of every response, the family of enacted transfers is equivalent to copying in some fixed frame only if the relation lies in the dial set 𝒟 = {iaJ} ⊂ 𝔤, of dimension at most 1 + ⌊K²/4⌋. In that case it is exactly the scalar dial cos(sa).
     - The frame objection assumes a free choice of coordinates at the partner node. The passage through the identity removes that freedom.
     - This holds even for relations that are real rotations, r ∈ SO(K), which are frame changes at each instant. Over a response they move from matching (s = 0) to the rotated map, and no single frame makes both copies. It is the holonomy argument of Bodnar Propositions 3-5 applied to the multigraph of lags: the loop "partner at lag s₁ → self → partner at lag s₂" has transport exp((s₁ − s₂)L) ≠ I.

3. **The relation is content-, partner- and history-dependent.** By (R), r is a function of partner identity, gaze directedness, the episode and the text events. Within one episode it changes by (G). Across histories, the reachable transfers fill 𝔅: for any M₀ ∈ 𝔅, a history whose residual target satisfies ỹ = M₀m has, by (d) below, a global minimiser with Re r = M₀. So the dial rank of the math synthesis (dim span{T(h)}) is K², and the Altafini test across h fails for generic pairs of histories: there is no common signature D with D T(h) D ≥ 0 for all h.

**(d) Copy is earned, per subspace.** Let Σ_mm = E[m mᵀ] ≻ 0, Σ_mỹ = E[m ỹᵀ], S = sym(Σ_mỹ) and Λ = Σ_mm − S. Consider ℓ̄(r) = E‖Re(r m) − ỹ‖² on U(K).

(i) The global minimum value of ℓ̄ equals min over M ∈ 𝔅 of E‖Mm − ỹ‖². This is a convex problem with a unique minimiser M*, and every r with Re r = M* is a global minimiser of ℓ̄.

(ii) The identity (copy) is a critical point of ℓ̄ iff Σ_mỹ is symmetric.

(iii) If Σ_mỹ is symmetric, the Riemannian Hessian of ℓ̄ at I is block-diagonal over 𝔤 = so(K) ⊕ i·Sym(K). For X = B + iA:

  ℓ̄(I · e^{εX}) = ℓ̄(I) + ε² [tr(BᵀB S) − tr(A Λ A)] + O(ε³).

So I is a strict local minimum if S ≻ 0 and Λ ≺ 0, i.e. S ≻ Σ_mm. If Λ has a positive eigenvalue with eigenvector v, then I is not a local minimum: moving along X = i vvᵀ rotates direction v into the held channel and lowers ℓ̄.

*Proof.*
1. (i): ℓ̄(r) depends on r only through Re r, which ranges over exactly 𝔅 by (a). E‖Mm − ỹ‖² is a strictly convex quadratic in M (Σ_mm ≻ 0), and 𝔅 is convex and compact, so the minimiser is unique.
2. (ii): At r = I, ε = m − ỹ. By (G), E[Ξ(I)] = ½E[εmᵀ − mεᵀ] = ½(Σ_mỹ − Σ_mỹᵀ) after the mmᵀ terms cancel. This is zero iff Σ_mỹ is symmetric.
3. (iii): Re e^{εX} = I + εB + (ε²/2) Re(X²) + O(ε³), and Re(X²) = B² − A², since (B + iA)² = B² − A² + i(AB + BA).
4. Write ε₀ = m − ỹ. Then ℓ̄ = E‖ε₀ + εBm + (ε²/2)(B² − A²)m‖² + O(ε³).
5. The first-order term 2εE[ε₀ᵀBm] = 2ε tr(B Σ_m ε₀) vanishes under (ii).
6. The second-order coefficient is E‖Bm‖² + E[ε₀ᵀ(B² − A²)m] = tr(BᵀBΣ_mm) + tr((B² − A²)Λ), using E[mε₀ᵀ] = Σ_mm − Σ_mỹ and the symmetry of B² − A².
7. With B² = −BᵀB, this is tr(BᵀB(Σ_mm − Λ)) − tr(A²Λ) = tr(BᵀBS) − tr(AΛA). There is no B-A cross term.
8. tr(AΛA) > 0 for all nonzero symmetric A iff Λ ≻ 0; for A = vvᵀ it equals (vᵀΛv)‖v‖².
9. If S ≻ 0, tr(BᵀBS) > 0 for B ≠ 0. ∎

(Checked numerically. With ỹ = 0.5m + noise, Λ ≻ 0 and a held step from I lowered the loss as the formula predicts, 1.6822 against a predicted 1.6819. With ỹ = 1.5m + noise, Λ ≺ 0 and it rose, 1.7253 against a predicted 1.7251.)

*Reading.* Under the relation loss, copying a direction v is stable only if the partner's expression along v predicts the agent's own coming body-driven expression at least one to one (vᵀSv > vᵀΣ_mm v). Where the partner's face is larger than what it predicts for the agent's own body, the relation turns it into the held channel. Where it predicts nothing (Σ_mỹ = 0), the minimiser is M* = 0: hold everything, see everything. For most partners and channels copying is generically unstable, and the stable copy directions are a learned, partner-specific subspace (the "robust smile core" if the data make it so).

**(e) The scalars that remain, with their exact endpoints.** RFT has four scalar quantities that modulate partner influence. None is a single setting that runs the face from flat to copy for all relations.

| Scalar | What it does | Endpoints | Flat-to-copy dial? |
|---|---|---|---|
| π(t), perceptual precision | multiplies m̂, so it scales e and η together | π = 0: blind (e = η = 0); π = 1: the relation acts | No. It cannot change any share c_r(u). Flat-by-blindness has η = 0, distinguishable in the state from flat-by-relation (‖η‖ = ‖m̂‖). |
| ν(t), surprise rate | moves g along the geodesic from r toward I; for constant ν the steady state is s* = 1/(1 + ντ₀) (Proposition 3b) | ν = 0: g = r; ν → ∞: g = I (copy) | **Yes, for one class of relations and only transiently.** If r ∈ i·O(K) (hold everything), ν runs from flat-enacted to copy. ν is computed from the partner's predictability, not set, and it decays after each onset. This is the design's remaining dial, stated as such. |
| η_p, η_ep, learning rates | scale (G) | η → 0: the relation stays at its start | No. The relation flow has no leak at the partner level, so its fixed points (d)(i) do not depend on η. The episode leak λ_ep pulls toward the partner relation, not toward copy or flat. |
| τ₀ | speed of relaxation toward r | — | No. It changes timing, not fixed points. |

The one honest caveat in (e) is ν: an agent that holds a partner's expression transiently copies that partner's surprising expressions. This matches Weyers 2009, where early seconds were similar across conditions and context appeared from the 4th second. It is a prediction (falsifier F3), not a hidden constant.

### Theorem 2 (T2): the drives are satiable, and nothing rewards the partner's approval

(a) Φ ≥ 0, and Φ = 0 exactly on the box 𝔅* = Π_i [b_i* − δ_i, b_i* + δ_i], which has nonempty interior.

(b) Every motivational quantity in RFT is one of:
- the policy objective ∫Φ(b)dt over a horizon;
- the valence readout v = −dΦ̂/dt;
- the need vector ∇Φ(b);
- the innate target y = Y(b, ḃ), which depends on b only through the same synergies.

On the interior of 𝔅*, ∇Φ = 0 and Φ = 0. So no learning or selection signal derived from Φ is nonzero there.

(c) The partner's observable o enters f_b only through:
- integrity load, a cost increasing in sensory intensity whose minimum is reached at low intensity;
- learning progress b_P, which depends on |prediction-error decrease| and is therefore unchanged by flipping the sign of any expression channel.

So ∂Φ/∂(any partner smile or affiliative feature) is zero except through b_P, and b_P's contribution vanishes inside its band. No term in Φ is monotone increasing in the partner's smiles, attention or time spent.

(d) The relation loss ℓ is a prediction error of the agent's own future body-driven expression. Its gradient (G) contains the partner only as the input m̂. No term has the partner's future expression as a target. Changing r changes the agent's face and hence possibly the partner's future m̂, but (G) is myopic: it does not differentiate through the partner. So no gradient pushes the relation toward eliciting any particular partner expression.

(e) **Corollary (bounded dependence; the hidden-regulator hazard of coordination-synthesis §1g).**
- No body variable is fed only by the partner's presence.
- The interior of 𝔅* is reachable with the partner absent: energy recovers at rest; integrity load decays without input; effort decays; b_P can be raised by any learnable input, including the world and the conversation content.
- So removing a partner cannot by itself hold Φ above zero indefinitely. The partner-specific relation Δ_p persists as memory, but the drive carries no deficit for that partner.

*Proof.*
1. (a): ψ_i ≥ 0, with ψ_i(x) = 0 iff |x| ≤ δ_i.
2. (b): the gradient of (|x| − δ)_+² is 2(|x| − δ)_+ sign x, which is zero on the band.
3. (c): by construction of f_b in §2.5. The sign-flip invariance of b_P holds because it is a function of ‖m̂ − m̂_pred‖, which is invariant under m̂ ↦ Dm̂, m̂_pred ↦ Dm̂_pred for any diagonal sign matrix D when the predictor is linear: the error vector is mapped by D, which preserves its norm.
4. (d): read off (G).
5. (e): the reachability claims are properties of f_b as specified. ∎

*Caveat.* Satiable learning progress can be sought by provoking surprising behaviour in the partner rather than by flattering. It is satiable, so the provocation is bounded, but it is the Principle 6 risk this design carries (weak point W9).

### Theorem 3 (T3): time scales from the structure

**(a) Reflex level.** Muscles relax with τ_m = 60 ms. The innate reflex generators fire on fixed triggers.

**(b) Stance level: matching first, context after, with latency set by the relation's angle.**
- *Setting.* Let r = e^L be constant, with L principal and eigenvalues iθ_k, |θ_k| ≤ π. Let a surprise reset the frame to g(t₀) = I, and let ν = 0 afterwards.
- *Claim.* Then g(t) = exp(s(t)L) with s(t) = 1 − e^{−(t − t₀)/τ₀}. Along the k-th eigen-axis u_k of L the enacted share is Re(e^{iθ_k s(t)}) = cos(θ_k s(t)).
  - If |θ_k| > π/2 (a counter-response), the enacted share crosses zero at t₀ + τ₀ ln[1/(1 − π/(2|θ_k|))]. For a full counter (θ = π) that is τ₀ ln 2 ≈ 0.83 s. For θ = 2π/3 it is τ₀ ln 4 ≈ 1.66 s.
  - If |θ_k| ≤ π/2, it never crosses zero.
  - With constant ν > 0 the steady progress is s* = 1/(1 + ντ₀).
- *Proof.*
  1. On the curve g = exp(sL): g*r = exp((1 − s)L). Log of this is (1 − s)L, because (1 − s)θ_k stays in the principal branch for s ∈ [0, 1].
  2. Log g = sL.
  3. So X = [(1 − s)/τ₀ − νs]L, and ġ = g ṡ L (L commutes with exp(sL)).
  4. Matching gives ṡ = (1 − s)/τ₀ − νs, whose solution from s(t₀) = 0 with ν = 0 is as stated. Its fixed point for constant ν is 1/(1 + ντ₀).
  5. The direction u_k is an eigenvector of exp(sL) with eigenvalue e^{iθ_k s}. For real u_k (L real-diagonalisable on that axis) the enacted part is cos(θ_k s)u_k. In general the share is the real part along the axis.
  6. Solve cos(θs) = 0 for the first s = π/(2|θ|). ∎ (A numeric run of (F) with a decaying surprise at onset gave enacted share 0.92 at 0.2 s, 0.19 at 1 s, −0.69 at 2 s and −0.99 at 4 s for θ = π.)
- *Reading.*
  - The time at which context shows is not a separate constant per expression. It is a function of the relation's angle: strong counters show earlier than weak ones.
  - Predicted expressions (ν ≈ 0) get no reset, so context shows from onset. This covers both the Carr/Weyers pattern and the Mauersberger exception.

**(c) Episode, partner and temperament levels are nested by where their leaks point.**
- R_ep leaks toward I, which in (R) means toward R_T Δ_p.
- Δ_p has no leak.
- R_T has no leak and moves only by barycentre.

So each level forgets toward the next slower one, never toward copy or flat. Consolidation moves the shared part of the partner relations into R_T and leaves every total relation unchanged (§2.6). In the log-Euclidean form,

  ‖Log R_T,new − Log R_T,old‖ ≤ Σ_p w_p ‖Log(R_T Δ_p)_new − Log(R_T Δ_p)_old‖,

by the triangle inequality on a weighted average of algebra elements, provided all Logs stay in the principal branch. The temperament moves at most as fast as the experience-weighted average movement of the relationships. With N partners of equal weight, its rate is at most 1/N of a typical relationship's. This rate is structural, not a time constant.

**(d) Body and latent.** The body variables have the innate dynamics of f_b (seconds to hours). The latent runs at 30 Hz, 30 Hz and 1 Hz. These are ordinary choices and are not claimed as structure.

**(e) What is not from structure.** τ_m, τ₀, λ_ep and the learning rates are set by hand. The structure fixes only:
- the order of the levels and where each one forgets toward;
- the angle dependence of context latency;
- the barycentre bound on temperament.

### Theorem 4 (T4): "reads the other through its own body", as mathematics

**(a) Factorisation.** Every state variable depends on the partner observation o(t) only through m̂(t) = πC_ω(o(t)). If C_ω(o) = C_ω(o′), the agent's whole trajectory is identical under o and o′.
- If F_ω is linear with full column rank and C_ω = F_ω⁺, then every component of o in (im F_ω)^⊥ has no effect at any time: an expression the agent's body cannot make is invisible to it.
- *Proof.* o enters (T) only through m̂, and (F), (E), (G) and the latent take m̂, e, η and μ as inputs. F_ω⁺ annihilates (im F_ω)^⊥. ∎ This is the sheaf statement D2 of the discourse-sheaf note, carried over to a learned inverse model.

**(b) One space, one operation.** The partner's transported expression z and the agent's own anticipatory expression a enter the same space, through the same display frame Γ, into the same muscle layer (E).
- Holding the partner's expression (r rotates it into ℍ) and masking one's own (Γ rotates it into ℍ) are the same operation, multiplication by a unitary followed by Re.
- So the agent regulates what it shows of the partner with the same machinery it uses to regulate what it shows of itself.

**(c) Relative-frame invariance of agreement (the RoPE-type property).**
- *Claim.* For any display frame Γ ∈ U(K),

  Re⟨Γ(a), Γ(gm)⟩ = Re⟨a, gm⟩,

  and more generally Re⟨Γ_s a, Γ_o m⟩ = Re⟨a, Γ_s*Γ_o m⟩ depends on the two frames only through the relative frame Γ_s*Γ_o.
- *Proof.* ⟨Γ_s a, Γ_o m⟩ = a*Γ_s*Γ_o m, and Γ*Γ = I. This is RoPE's Eq. 16 identity, R_m^T R_n = R_{n−m}, for the group U(K) instead of positions. ∎
- *Reading.* Display regulation (suppression or masking) changes what reaches the muscles. It cannot change the agent's agreement with the partner. Suppressing a smile does not reduce resonance; it moves the smile into ℍ.

**(d) Decodability of the partner does not depend on stance.** From (e, η) the agent can recover m̂ exactly, m̂ = Re(g*(e + iη)), for every g. So the information about the partner in the pair (e, η) is the same for every relation.
- If the held channel is removed from the latent's input (lesion), the information left is that of e = (Re g)m̂. Its linear decodability is set by the singular values cos φ_k of Re g and falls as the relation moves toward holding.
- *Proof.* g*z = g*gm̂ = m̂, which is real. ∎

**(e) Inferring the other's state by inverting one's own expression map** (Yoshida & Man's form, as in yoshida-man-homeostatic-coupling.md):

  ŝ_o(t) = argmin_s ‖A_ω(s) − m̂(t)‖² + β‖s − s(t)‖².

This is the latent state that would make the agent itself produce the partner's motor image, regularised toward its own current state. It uses only A_ω, the agent's own expression readout.
- *Corollary.* Any change in A_ω, such as a learned display habit or a lesion of a channel's readout, changes ŝ_o for every partner in the same way.

### Proposition 5: the properties the human data require

**(H1) Gating per expression, in independent directions.**
- *Claim.* The relation's enacted transfer has singular axes (patterns of the partner's expression) and per-axis angles. Across histories, the reachable transfers fill 𝔅 (Theorem 1c.3). So two histories can move one expression toward countering and another toward matching. This is the Hofman 2012 pattern: anger return up and smile return flat after an unfair reputation.
- *Proof.* Choose histories whose residual targets realise M₁, M₂ ∈ 𝔅 with the required sign pattern, and apply Theorem 1d(i). ∎
- *Caveat.* What histories the agent's actual body produces is limited by the rank of Σ_mỹ (weak point W3).

**(H2) Sign flips pass through holding, never through not seeing.** Along the geodesic from match (θ = 0) to counter (θ = π) on an axis, the enacted share is cos θ and the held share sin θ, with total 1 by Theorem 1a. A gain model g·I, g ∈ [−1, 1], must pass through g = 0, where the partner's expression is absent from the output, and has no held component.

**(H3) Fast matching, then slower context.** Theorem 3b.

**(H4) Partner-specific history at two time scales, and reinterpretation of the past.**
- *Fast.* A partner's unfair act enters as a text event (G_ψ) and as a burst of relation-loss gradient, changing R_ep within seconds. This is Hofman's immediate loss of smile return.
- *Slow.* Δ_p accumulates over sessions and is consolidated in replay. This is reputation.
- *Read-time transport.* Episodic memory stores raw, frame-free motor images m̂ and applies the current relation at recall. A past smile of a partner now held as a rival is recalled through the rival relation.

**(H5) Tracking is separate from aligning.** Theorem 4d.

**(H6) Order effects (non-commutativity).**
- *Claim.* Two relation updates e^{−ηΞ_A} and e^{−ηΞ_B}, from events A and B, give, in the two orders,

  e^{−ηΞ_A}e^{−ηΞ_B} = e^{−ηΞ_B}e^{−ηΞ_A} · e^{η²[Ξ_A, Ξ_B] + O(η³)}.

  So the relation after "A then B" differs from "B then A" by the commutator.
- *Proof.* Baker-Campbell-Hausdorff to second order. ∎
- This is a prediction. No human data on order effects in relationship updating were read (weak point W7).

---

## 4. Why the closest existing mechanisms cannot do this

In each case the question is whether the mechanism produces, from its own structure, the three properties of Theorem 1:
- (i) conservation: the partner is registered in full whatever the stance;
- (ii) a per-expression signed transfer that is not frame-equivalent to copying over a response;
- (iii) copy as a learned outcome under a stated condition, not an endpoint of a parameter.

**Attention, including RoPE attention.** From the RoPE note (derivation checked against the paper's Eqs. 2 and 16), for one attention layer over self and partner frames, the partner's contribution to the output is

  Σ_h α_h M_h x̄_h,  α_h ∈ [0, 1],  M_h = W_O^h W_V^h fixed,  x̄_h a convex combination of partner frames.

- (i) fails: α_h → 0 removes the partner from the layer's output altogether. There is no complementary held output, because softmax weights over tokens trade the partner against the self.
- (ii) fails: the Jacobian ∂y/∂x_j = Σ_h a_{tj}^h M_h with a ≥ 0 lies in the cone of H fixed matrices. A sign flip of one expression that depends on history is available only if some fixed M_h already carries it. RoPE rotates queries and keys only ("the position information in the value term is removed", RoFormer §2.3), so the rotation never reaches the content.
- Getting RFT from attention needs (1) values multiplied by a state-dependent learned unitary, (2) a fixed real-part readout and (3) a held output. That is the RFT object, not attention.

**Hopfield retrieval.** The update ξ ← X softmax(βXᵀξ) outputs a convex combination of stored patterns. The partner enters through which patterns are retrieved. β runs from averaging, which is flat, to nearest-pattern, which copies when the partner's own pattern is stored (critique-fast-weights.md). No conservation; no held output.

**Fast weights and test-time training.** The relation level *is* a TTT layer in the sense of Sun et al. 2024 (the TTT note): the hidden state is a weight (r) updated by a gradient step on a self-supervised loss. The input view is the partner image and the label is the agent's own body-driven residual, as that note proposed. What RFT adds, and an unconstrained TTT weight W ∈ ℝ^{K×K} does not have:
- (i) conservation: W has no held complement;
- the fixed point without a leak: an unconstrained delta rule needs weight decay to stay bounded, and its fixed point is then ridge regression with penalty set by the leak-to-rate ratio, the dial found in critique-developmental-dyad (v2-README). RFT is bounded by compactness of U(K), so (G) needs no leak, and its fixed points (Theorem 1d(i)) do not depend on the learning rate;
- the gauge pinning of Theorem 1c.2.

So: TTT with the weight constrained to a compact group and a real-part readout. This is recorded as recombination in §7.

**State-space models.**
- **S4 and other non-gated, linear time-invariant SSMs.** The partner-to-output map is a fixed convolution kernel. It cannot depend on the partner's identity or the history, so (ii) fails across partners.
- **Mamba and other diagonal SSMs.** Transitions are diagonal and input-dependent, hence mutually commuting. Merrill et al. (Theorems 4.4 and 4.6) prove that such SSMs, and those simultaneously diagonalisable in a fixed basis, are in L-uniform TC⁰. Under TC⁰ ≠ NC¹, no fixed-depth such model solves the S₅ word problem (Corollary 4.7).
  - RFT's relation state is a product of input-dependent, non-commuting unitaries, r_t = r_{t−1} e^{−ηΞ_t}. U(K) contains the permutation matrices for K ≥ 5, so this recurrence can in principle represent permutation composition, as IDS4 can (Merrill Theorem 5.2) and as products of generalised Householder matrices can (Grazzi et al. Theorem 3).
  - Precisely: a diagonal-SSM relation gives the same final relation for any order of the same events, because diagonal transitions commute. RFT's differs by the commutator (H6).
  - This separates RFT from S4 and Mamba, not from IDS4 or DeltaProduct-type recurrences, which share the non-commuting product. Grazzi et al.'s Proposition 1.2 shows that products of generalised Householder matrices with eigenvalues in [−1, 1] reach every matrix with norm at most 1. That is the same contraction ball 𝔅 as Theorem 1a, reached by a different route.
- **Nonlinear dynamics.** Neither the frame dynamics (F), with Log and exp, nor the read-time transport of stored memories is a linear recurrence.

**Diffusion.** A conditional generator p(face | partner) can represent any response distribution, including countering, but nothing in its structure gives (i)-(iii). Any such property must be in the conditioning signal. The REACT tables (known-failures rows 1-2) show such models landing at copy or at the mean.

**Oscillators and Kuramoto.** In the Kuramoto-Sakaguchi form θ̇_i = ω_i + K sin(θ_j − θ_i − α), the lag α is a relation angle, and RFT's per-axis angle resembles it. Two differences can be stated exactly:
- In Kuramoto the angle is the phase of an oscillating variable, and the coupling strength K is a gain: K → 0 gives independence, large K gives locking at α. That is the excitability dial of the v2 coupled-dynamics critique.
- In RFT the angle acts on expression amplitudes and is not a phase of oscillation. The strength of partner influence is not a parameter (Theorem 1a), and the structure is U(K), non-commutative, rather than the torus U(1)^K of independent phases.

AKOrN's vector Kuramoto oscillators (miyato-2025-akorn.md) also act by rotation, but their coupling strength is a gain.

**Linear operators (sheaves, Friedkin-Johnsen, port-Hamiltonian coupling).** For a fixed r and g = r, RFT's enacted path is the linear operator Re r: a contraction. This sits inside the discourse-sheaf family as a restriction-map product A⁺B with ‖A⁺B‖ ≤ 1. So at an instant with a fixed relation, RFT *is* a constrained linear operator. What a fixed operator cannot do:
- the time-varying transfer Re g(t) along the geodesic (Theorem 1c.2), which no fixed matrix reproduces and which pins the gauge;
- the held output with conservation. A linear pair (M, N) with MᵀM + NᵀN = I is an isometric embedding ℝ^K → ℝ^{2K}, a point of the Stiefel manifold V_K(ℝ^{2K}), of dimension (3K² − K)/2. RFT restricts to U(K) ⊂ V_K(ℝ^{2K}), the isometries that also commute with the complex structure (MᵀN symmetric), because only these compose as a group. Composition is what (R), (F) and the display frame need: held content can later be rotated back into enactment, as in a delayed or released expression.

**Complex-valued networks (Complex AutoEncoder, Rotating Features).** In the CAE, phase is a binding label and the read-out is the magnitude |ẑ| (CAE §3.1). The CAE is equivariant to global phase: CAE(x e^{iα}) = CAE(x) e^{iα} (Proposition 3.1), so its output magnitudes are invariant to any global rotation. A stance encoded as a global phase in a CAE would therefore have no effect on its output.
- RFT's read-out Re(·) depends on absolute phase by design: angle 0 means "enact". So RFT deliberately breaks that equivariance.
- Two pieces are shared:
  - the CAE's per-feature phase bias b_φ (Eq. 3) is a diagonal relation, a fixed learned constant;
  - Rotating Features' per-dimension biases are a fixed orientation offset.
- In RFT the same kind of rotation is a state: per partner, non-diagonal, learned online, and moved by surprise.

---

## 5. The whole system derived from the object

```
 webcam 30 Hz ─► face tracker ─► 52 blendshapes + 6 pose ┐
 mic ─► prosody front end (100 Hz ─► 30 Hz, 8 features) ──┼─► o(t) ─► C_ω (own inverse) ─► m̂ = π·C_ω(o)
                                                          │                                   │
 transcript events ─► sentence encoder x ─► G_ψ(x) ───────┼──────► R_ep ─┐                    │
                                                          │              ▼                    ▼
 partner identity ─► Δ_p(γ) ◄── gaze directedness γ       │   r = R_T Δ_p(γ) R_ep ─► frame g (F) ◄── surprise ν
                                                          │                                   │
                                                          │                     z = g m̂ ─► e = Re z, η = Im z
 latent s (GRU f/m/s) ◄── [b, b−b*, dΦ/dt, e, η, μ, h, prosody, text] ◄───────────────────────┘
      │  a = A_ω(s)                         display frame Γ (deliberate system)
      └──────────────► u_emo = Re Γ(a + z)  ──► muscle layer μ ◄── u_del (deliberate route) ◄── policy / speech plan
                        h = Im Γ(a + z) ──► latent              │
                                                                ├─► face renderer (AU face, neutral placeholder)
                                                                └─► voice: TTS with rate, pitch, gain, pause
 body b (innate f_b) ◄── μ, o, rest ;  y = Y(b, ḃ) ──► relation loss (G), A_ω loss
 episodic memory (raw m̂, a, b, s summary, tags) ◄──► need-conditioned attention ──► recall to Claude; replay
```

### 5.1 Perception of face and voice, through the agent's own body

- **Face.** The face tracker gives 52 blendshapes and a head transform at about 13 ms per frame (mediapipe-face-landmarker.md, measured on this Mac in a browser). No label is computed (Principle 1).
- **Voice.** The prosody front end gives F0 level, F0 slope, RMS energy, spectral tilt, voicing probability, speech-rate proxy (syllable-nucleus rate), pause indicator and jitter, at 100 Hz, averaged to 30 Hz.
- **Through the own body.**
  - Both streams go through C_ω into the agent's own 32 motor channels. The partner's prosody becomes the agent's own speech-rate, pitch, gain and pause commands that would reproduce it.
  - The off-diagonal blocks of r can couple partner voice to own face and partner face to own voice (cross-modal relations).
  - Theorem 4a states what this excludes.
  - C_ω starts weak and non-selective (small random output), and is trained from the agent's own mirror (perfect-contingency self-observation) and from shared events. This follows the associative account in face-development-synthesis §3: the visual-to-motor map is learned. At the start, m̂ ≈ 0 and nothing is mimicked.
- **Gaze directedness.** γ ∈ [0, 1] is computed geometrically from the partner's head pose and the camera, with no parameters.
- **Partner identity.** An embedding from landmark-geometry and voice statistics, clustered online. This is an ordinary choice, not a label of emotion.

### 5.2 The latent state where emotion emerges

**What it holds.** No unit of s is named. Emotion, in the functional sense of the brief, is the joint configuration of:
- (a) the latent s;
- (b) the relation field {R_T Δ_p : p ∈ P}, a point of U(K)^|P|: how each partner's expressions are turned;
- (c) the applied frame g and the held content (η, h), what the agent registers but does not show.

**Readouts.**
- **Valence:** v = −dΦ̂/dt, the predicted drive change from the body predictor head.
- **Arousal:** ‖ds_f/dt‖.

Neither is set; both are read out, as Principle 2 requires.

**Structure over people, episodes and time (brief, expressive structure).**
- Relationships are points on U(K), compared by geodesic distance. Temperament is their barycentre (§2.6).
- Episodes are stored with the relation snapshot and the raw partner content.
- The effective dimensionality of the relational part is up to K² = 1024 per partner. The low-dimensional ablation is to restrict r to the dial set 𝒟 (one angle per partner), or to diagonal relations (U(1)^K, one angle per channel in a fixed basis).
- Behaviours the restricted versions provably cannot produce:
  - with 𝒟, any two expressions moving in different directions (Theorem 1b);
  - with diagonal relations, off-diagonal responses (a smile answered on the brow) and order effects (H6), because diagonal relations commute.

**Content-dependent selection (brief, attention-level richness).** Need-conditioned attention over episodic memory (§5.6) uses as query the need vector b − b* together with s_m. What the agent needs selects which past episodes return. The partner content of a returned episode is re-transported by the current relation (H4).

### 5.3 Face output: two routes into one muscle layer, separately ablatable

- **Emotional route:** u_emo = Re Γ(a + z). It carries the agent's own anticipatory expression and the transported partner, through innate synergies W_syn (AU12 recruits AU6 with intensity; mouth opening scales with arousal). It is bilateral and reaches the upper face.
- **Deliberate route:** u_del. It is produced by the policy and the speech plan (visemes, posed expressions), addresses single channels, and is weighted toward the lower face (face-development-synthesis §1).
- **Reflex generators:** c_ref.

**Ablations.** These follow from the equations and match the clinical double dissociation:

| Cut | Predicted effect | Clinical analogue |
|---|---|---|
| u_del | posed expressions fail; spontaneous expressions and mimicry survive | volitional palsy |
| u_emo | spontaneous expression and transported mimicry vanish; posing survives; held content (h) still reaches the latent | emotional palsy, amimia |

**Masking.** Display rules act through Γ. A masked smile (mouth enacted through u_del, cheek raise rotated into ℍ by Γ) gives the zygomaticus-without-orbicularis signature as an output of the equations.

### 5.4 Voice

The 4 voice channels of μ set speech rate, pitch shift, gain and pause length for the TTS engine. The Kokoro note measured a real-time factor of 0.55-0.65 on this Mac; its built-in control is speed, and pitch and gain are applied after synthesis by signal processing. Voice and face come from one u_emo + u_del, so they cannot disagree, as known-failures row 11 requires. The deliberate system also sets L_Γ (display) and turn timing.

### 5.5 Coupling to Claude without text (Principle 4)

Claude never sees a number, a label or a description of the state. The interface is the shared plumbing (v2-README, "Coupling to Claude by choosing among Claude's own drafts"), with three parts specific to RFT.

1. **Draft selection by enacted agreement.**
   - Claude writes N drafts.
   - Each draft is passed through the TTS front end to its prosody trajectory, and through C_ω to the agent's own voice-motor trajectory a_d(τ). The agent hears its own draft through its own body.
   - The agent speaks the draft maximising Σ_τ Re⟨Re Γ(a + z)(t + τ), a_d(τ)⟩: the draft whose voice the agent would enact.
   - Held content does not count toward selection. What the agent holds, it does not voice. This is display regulation applied to speech.
2. **Timing derived from the frame.**
   - A reply starts when the applied frame has settled, ‖Log(g*r)‖ < ϵ_settle.
   - After a surprising partner utterance (a reset toward I), the agent waits until its stance has re-formed, about τ₀ ln(θ_max/ϵ_settle).
   - Reply latency is a function of how far the partner's last expression moved the agent's frame.
3. **Recall.**
   - The episodes returned by need-conditioned attention (§5.6) supply verbatim transcript snippets to Claude's context.
   - The state chooses what Claude remembers, never what Claude is told about the state.

**Feedback from Claude (the D1 switch of emotion-elements-synthesis).**
- Claude's spoken words re-enter as transcript events and act on R_ep through G_ψ. A reappraisal ("they were teasing") rotates the episode relation, and through it what the partner's faces now mean to the face.
- G_ψ is a switch. Turning it off keeps Claude naming but cuts its concepts from the fast core: that is the constructionist lesion (a).
- Claude never drives frames. It moves a relation, which moves faces only through (F) and (E).

### 5.6 Learning by living, and memory and replay with state tagging

**Online, on every frame or event:**
- the frame g, by (F);
- R_ep, by (G) with its leak;
- Δ_p, with a small rate;
- the latent state;
- small steps on F_ω and C_ω from self-observation;
- the episodic write.

**Episodic memory.**
- Every 2 s segment stores raw m̂ at 10 Hz, a, b, the summary s_m, the partner id, γ, and a pointer to the transcript. Feature streams only, no raw video or audio (Principle 7).
- **State tag:** w = |ΔΦ| + ‖Ξ‖. That is how much the segment changed the drive, plus how much it pushed the relation.
- **Read-time transport:** stored partner content is frame-free. Whenever it is replayed or recalled, the current relation is applied.

**Need-conditioned attention for recall.**
- 4 heads with query W_q[b − b*; s_m] and stored keys W_k[b − b*; s_m].
- An ALiBi-style recency bias −λ_h log(1 + Δt/1 s) per head, with λ_h spanning seconds to months. RoPE was rejected for this, because its decay over 10⁷-fold time ranges is not guaranteed (RoPE note, Property 3).

**Replay, offline.** Segments are sampled with probability ∝ w^α, α = 1. Replay runs:
- TTT steps of (G) on Δ_p, with a larger rate;
- temperament consolidation;
- training of G_ψ;
- training of the latent, A_ω and the body predictor on stored sequences;
- refresh of F_ω and C_ω.

**Tagging lesion (the S6 claim).**
- With uniform replay, the relation-informative segments (large ‖Ξ‖) are under-sampled. The replayed fixed point of Δ_p is then the regression over all segments rather than over the segments that carried the relationship, so partner specificity falls.
- This is a prediction, not a theorem. It rests on the informative segments being rare.

### 5.7 The 16 elements of emotion-elements-synthesis.md

| # | Element | In RFT | Status |
|---|---|---|---|
| 1 | concern grounding | body variables b and drive Φ | constraint (innate) |
| 2 | central persistent state | latent s plus the relation field and the held content | derived structure |
| 3 | valence | v = −dΦ̂/dt; also the sign of y's synergy | readout |
| 4 | intensity and regime switch | muscle saturation; the principal-log branch at θ = π gives a discontinuity in the transient path (W5) | partial; hysteresis not derived |
| 5 | pleiotropy | one u_emo drives face and voice; s drives the policy, recall and draft choice | derived |
| 6 | interoceptive prediction | body predictor head; A_ω anticipates y(t + Δ) | derived from the losses |
| 7 | precision on body error | not in the core; π is perceptual precision on the partner only | missing |
| 8 | relevance and novelty checks | ν (surprise) resets the frame toward reflex matching, so orienting precedes stance | partly derived |
| 9 | agency and coping potential | "whose" is carried by frames (self content in Γ, partner content in Γg), but controllability is not represented | partial |
| 10 | action readiness and interrupt | reply timing waits on frame settling (§5.5) | partial |
| 11 | wanting distinct from liking | not derived | missing |
| 12 | learned elicitors and generalisation | the relation learns what partner expressions mean for the agent's body (Theorem 1d) | derived |
| 13 | expression and social communication | the core object | derived |
| 14 | comparator and self-model | the agreement κ compares own affect with the partner; relief and disappointment are not derived | partial |
| 15 | conceptual categorisation | Claude, with the G_ψ feedback switch | constraint (Principle 4) |
| 16 | structure beyond valence and arousal | the relation has K² dimensions per partner; the latent has 224 | derived capacity; to be shown |

---

## 6. A buildable network

**Inputs.**
- 30 Hz face (52 blendshapes, 6 pose).
- Prosody at 100 Hz, averaged to 30 Hz (8 features).
- Transcript segments, embedded by a frozen sentence encoder (384-d).
- The agent's own body b (4), muscles μ (32) and self-observation of its rendered face and voice.

**Time encoding, and why.** The object fixes the fast-loop encoding:
- The stance "position" of a partner expression is its progress s ∈ [0, 1] along the geodesic from I to r, advanced in real time by (F) and pulled back by surprise.
- This is a rotary encoding of content by state-dependent progress, not of tokens by index. It is exact for any frame interval, because exp(dt·X) is exact.
- The recurrent units use dt-aware updates.
- Memory uses log-time ALiBi-style biases (§5.6), because recalls span seconds to months.

**Layers in order.** Column "New?" marks the parts that carry the RFT mechanism. Parameter counts include biases.

| # | Layer | Shape | Params | New? |
|---|---|---|---|---|
| 0 | face tracker (frozen, external) | frame → 58 | (3.8 MB model) | no |
| 0′ | prosody front end (signal processing) | audio → 8 | 0 | no |
| 1 | C_ω own inverse model, MLP 66→256→256→32, GELU | 66 → 32 | 90,912 | no (analysis by synthesis) |
| 2 | F_ω own forward model, MLP 32→256→256→66 | 32 → 66 | 91,202 | no |
| 3 | surprise: two-lag linear predictor of m̂ | 64 → 32 | 2,080 | no |
| 4 | **relation store**: L_T (1,024), Δ_p^at and Δ_p^away (2,048 per partner), R_ep state (1,024) | 𝔲(32) elements | 3,072 + 2,048·|P| | **yes** |
| 5 | **G_ψ text-to-generator**: linear 384 → (U ∈ ℂ^{32×4}, λ ∈ ℝ⁴) | 384 → 260 | 100,100 | **yes** (ordinary layer, RFT target) |
| 6 | **frame dynamics (F) and transport (T)**: eigendecomposition of a 32×32 Hermitian, exp, multiply | — | 0 | **yes** |
| 7 | display generator L_Γ: linear 64 → rank-4 𝔲(32) | 64 → 260 | 16,900 | **yes** (same object) |
| 8 | text projection 384 → 64 | | 24,640 | no |
| 9 | GRU_f, input 209 (b 4, b − b* 4, dΦ/dt 1, e 32, η 32, μ 32, h 32, prosody 8, text 64), hidden 128 | | 130,176 | no |
| 10 | GRU_m, input 128, hidden 64 | | 37,248 | no |
| 11 | GRU_s, input 64, hidden 32, at 1 Hz | | 9,408 | no |
| 12 | A_ω own expression readout, 224→128→32 | | 32,928 | no |
| 13 | body predictor, 224→64→12 (4 variables × 3 horizons) | | 15,180 | no |
| 14 | latent self-prediction head, 224→128→64 (compressed m̂, e, η, μ at +1 frame and +1 s) | | 37,056 | no |
| 15 | policy: deliberate route, voice and turn timing, 224→128→38 | | 33,702 | no |
| 16 | need-conditioned attention: W_q, W_k (228→64 each), W_o (64→64) | | 33,472 | no |
| 17 | muscle layer: 32 first-order units, innate W_syn (32×32) and reflex generators | | 0 learned (1,024 fixed) | no |
| 18 | renderer (AU-driven neutral placeholder face, Principle 8) and TTS (Kokoro 82M, frozen) | | external | no |

Total learned parameters: about 0.66 M, plus 2,048 per partner. The new mechanism (rows 4-7) has about 0.12 M parameters and no free gain.

**Training objectives.**

| Objective | Formula | Trains |
|---|---|---|
| J1, own body | ‖F_ω(m) − o_self‖² on the agent's own rendered face and voice; ‖C_ω(o_self) − m‖²; cycle term ‖F_ω(C_ω(o)) − o‖² on partner frames | F_ω, C_ω |
| J2, relation | ℓ of §2.6, by the group updates | R_ep, Δ_p, R_T |
| J3, latent | multi-horizon prediction of b, own μ, m̂, e and η (self-supervised on own and perceived signals) | GRUs, heads 13-14 |
| J4, expression | ‖A_ω(s(t)) − (y(t + Δ) − sg[Re(r m̂(t))])‖² | A_ω |
| J5, policy | minimise predicted ∫Φ over 3 s, by gradient through the learned body predictor plus an actor-critic baseline (homeostatic, satiable) | policy, L_Γ |
| J6, text events | ‖G_ψ(x) − Log(R_ep(t + 30 s)R_ep(t)*)‖² | G_ψ (replay only) |

J2 and J4 together are backfitting on one additive model. Each route fits the residual of the other. Weak point W2 states what that leaves unconstrained.

**Online versus replay.**
- Online: g, R_ep, Δ_p (rate η_p,online), latent state, small F_ω/C_ω steps.
- Replay (nightly, prioritised by w): J2 on Δ_p (rate 10 × η_p,online), R_T consolidation, J3-J6, F_ω/C_ω refresh.

**Latency per 33 ms frame on this Mac.**

| Step | Time | Source |
|---|---|---|
| face tracker | about 13 ms | measured in browser WASM (note); not measured in the Python process |
| prosody | under 1 ms | estimate |
| C_ω | about 0.05 ms | estimate |
| frame dynamics and transport | 0.12 ms | measured here: numpy, 32×32 Hermitian eigendecomposition + exp + apply, 2,000 repetitions |
| GRUs and heads | about 0.5 ms | estimate |
| attention over 100k keys every 10th frame | about 1 ms | estimate: 6.4 MFLOP |
| **total** | **about 15-17 ms** | |

Claude and TTS run asynchronously and never block the loop (Principle 4).

**Memory (estimates, not measured).**

| Item | Size |
|---|---|
| parameters | under 3 MB |
| episodic store, 100k segments × about 1.5 KB at fp16 | about 150 MB |
| tracker | under 0.1 GB |
| Kokoro (weights about 97 MB per the note) with runtime | about 0.5 GB |
| sentence encoder | about 0.2 GB |
| Python and PyTorch | about 1 GB |
| replay training on MPS | under 1 GB extra |
| **peak** | **about 2-3 GB**, within the 6 GB budget of machine.md |

---

## 7. Novelty test

| Part | Existing mechanism it is | Source read |
|---|---|---|
| own forward and inverse model; perception as inversion | analysis by synthesis; inverting one's own generative mapping | yoshida-man-homeostatic-coupling.md; face-development-synthesis |
| complexified activations with phase as a second message | CAE / Rotating Features; Reichert & Serre 2014 (via Löwe) | Löwe 2022 §2-3, Löwe 2023 §3 |
| rotations acting on content, relative-frame identity | RoPE (q/k only there) | RoFormer §3 |
| enacted = Re of a unitary; held complement | unitary dilation of a contraction (classical operator theory; proved in Theorem 1a, no source cited) | — |
| relation learned by a gradient step on a self-supervised loss, as a state | TTT layers / fast weights / delta rule | Sun 2024 (note) |
| products of input-dependent non-commuting orthogonal or unitary transitions | IDS4; products of generalised Householder matrices (DeltaNet with negative eigenvalues) | Merrill 2024 §5.2; Grazzi 2025 §4.3 |
| first-order relaxation on a Lie group, with resets gated by surprise | geodesic attraction (standard); surprise-gated writes (Titans, via critique-fast-weights) | critique notes |
| levels of relations, barycentre as temperament | log-Euclidean mean (standard) | — |
| need-conditioned attention with recency bias | attention; ALiBi | Bahdanau/Vaswani notes; ALiBi note |
| satiable drive with dead bands | homeostatic RL | keramati-gutkin-2014 note |
| two-route muscle layer | clinical neuroanatomy | gothard, matsumoto-lee, topper notes |
| draft selection, recall, timing | the shared Claude interface | v2-README |

**Verdict: a recombination by the parts test.** Every part has a precedent.

**The candidate second-clause claim** (new-mechanisms-synthesis §3): the design changes the defining invariant of partner coupling from "a map with a free magnitude" to "an isometry into enacted ⊕ held, with stance as a group element" (Theorem 1a). It derives the update from that invariant (the Riemannian gradient (G) on U(K)). It deletes the free scalar that carried the measured failure (the gain, and the leak that set the ridge fixed point; Theorem 1e). Two derived theorems no part has on its own:
- gauge pinning by the passage through the identity (Theorem 1c.2);
- the copy-stability condition (Theorem 1d).

**My honest judgment.**
- This is a constrained TTT layer on U(K) with a dilation readout and a geodesic transient. The constraint is principled, and it removes the dial everywhere except the transient ν-route for held partners (Theorem 1e).
- That is less than attention or the LSTM changed. It is a mechanism-level recombination with one derived invariant.
- The closest unread prior work (learned-generator rotary encodings, rotating values, unitary RNNs) may contain the value-path rotation already. If it does, the claim shrinks to the dilation readout, the anchor and the learning target.

---

## 8. Weak points and falsifiers

### Weak points

- **W1: per axis it is still a signed number.** Along each singular axis of Re r the enacted share is cos φ_k, a signed gain in [−1, 1]. Theorem 1 is about the family (dimension, gauge pinning, conservation), not about any single axis. A critic can call the instantaneous enacted map "a contraction matrix", correctly (§4, linear operators).
- **W2: a second route around the constraint.**
  - The latent receives (e, η), from which m̂ is recoverable (Theorem 4d). A_ω can therefore learn any function of the partner, so partner influence on the face through the agent's own state is not constrained to the unit ball.
  - The defence: this route is trained toward the agent's own body target. A linearisation of Theorem 1d to any predictor trained on that target says it converges to copy only under the same one-to-one condition.
  - But no conservation or gauge pinning holds for it. The lesion F2 is what separates the routes.
- **W3: few body variables limit the relation.**
  - With 4 body variables, y = Y(b, ḃ) lies in a subspace of dimension at most 8, so Σ_mỹ has rank at most 8 (plus whatever A_ω's residual adds).
  - The learned M* is then nonzero only on that subspace. Every other direction of the partner's expression is held, apart from the reflex transients.
  - The agent overtly responds only along what its body cares about. That is principled, but it may be far poorer than human mimicry. Learned (non-innate) targets would raise the rank and re-open the copy risk.
- **W4: copy before learning.** A newborn agent's relation is I (R_T = I). It copies whatever C_ω delivers until relations are learned. This is safe early on only because C_ω starts weak. If C_ω matures faster than the relation, the agent passes through a copying phase. That is a developmental prediction, and a risk.
- **W5: the branch cut at θ = π.**
  - The principal Log is discontinuous where an eigenvalue of g*r sits at −1.
  - When the relation is a full counter, the transient path from I goes through +held or −held depending on the sign of a tiny perturbation, so the transient's held component can jump.
  - Same-channel counter responses near π are therefore numerically fragile.
- **W6: not derived.** Escape from lock and metastability (coordination-synthesis §1f); wanting against liking; coping potential; relief and disappointment; precision on body error.
- **W7: is non-commutativity needed?** No human data on order effects in relationship updating were read. If a diagonal relation, U(1)^K in a learned fixed basis, fits all data, the U(K) structure is unnecessary. The design then reduces to per-channel phases: the CAE phase bias made per-partner and learned.
- **W8: the ν route.** For partners the agent holds, surprise is a transient flat-to-copy dial (Theorem 1e). An unpredictable partner gets more copying. This may be wrong for strangers or rivals with erratic faces.
- **W9: Principle 6 via curiosity.** Satiable learning progress can motivate provoking surprise in the partner. It is bounded, but present.
- **W10: the Claude interface is shared plumbing.** Only the timing rule (§5.5.2) and the G_ψ route are derived from the object.
- **W11: conservation may be too strong for humans.** RFT says that holding a partner's expression costs no reading of it. Human studies report that blocking one's own facial mimicry impairs emotion recognition. I have not read them (for example Oberman et al. 2007; Wood et al. 2016). If the effect is robust, the human system does not conserve, and RFT is a worse model of humans than of its own design goals.

### Falsifiers (state-level, in the sense of evaluation.md E1-E3)

**F1, steering.**
- Intervene on r: rotate one singular axis by φ.
- Predicted, exactly:
  - the overt share along that axis is cos φ (after muscle saturation);
  - the linear decodability of m̂ from (e, η) is unchanged at every φ (Theorem 4d);
  - the agreement κ is unchanged by any intervention on Γ (Theorem 4c).
- A change in decodability, or a κ that moves with Γ, falsifies the implementation of the object.

**F2, lesion of the held channel.**
- Remove η and h from the latent input.
- Predicted:
  - decodability of the partner from s falls in proportion to Σ_k sin²φ_k of the current relation;
  - the overt mimicry pattern is unchanged at first.
- Sham lesion: an equal number of random latent inputs.
- If decodability does not depend on the relation after the lesion, the latent was reading the partner by another route (W2).

**F3, lesion of the surprise reset (ν ≡ 0).**
- Predicted: the early matching transient disappears; counter responses show their sign from onset.
- With ν intact, a counter's zero-crossing latency follows τ₀ ln[1/(1 − π/(2|θ|))]: earlier for stronger counters (Theorem 3b).
- Testable in human data (published dyadic AU data, for example Seamless Interaction):
  - are listener counter-responses to more surprising partner onsets preceded by a matching transient?
  - does the zero-crossing latency shorten with the size of the eventual counter?
- A latency independent of response magnitude falsifies the angle dependence.

**F4, partner swap and the gain-model test (E3).**
- Fit per pair:
  - (a) a gain model r = e^{iθ}I;
  - (b) the dial set 𝒟;
  - (c) diagonal relations;
  - (d) full RFT;
  - (e) an unconstrained linear map with the same lag structure.
- Score each on held-out prediction of the listener's own-motor-coordinate responses, with partner-swap and segment-shuffle surrogates.
- RFT predicts:
  - (d) beats (a)-(c);
  - (d) ties (e) in fit, and (e)'s fitted maps have singular values ≤ 1 (after the own-body normalisation of C_ω).
- Robust singular values > 1 (the listener systematically responds larger than the partner's expression, in their own coordinates) falsify the group constraint.

**F5, order effects.**
- Present the same two partner events in both orders, in replay or in living.
- RFT predicts a difference in the subsequent relation proportional to the commutator [Ξ_A, Ξ_B].
- A diagonal-relation lesion must remove it. If the full model shows no order effect, W7 holds.

**F6, copy-stability.**
- In logged living, compute Λ = Σ_mm − sym Σ_mỹ per partner and channel subspace.
- RFT predicts that the relation converges to copy only on directions with Λ ≺ 0, and rotates out of copy on directions with a positive eigenvalue (Theorem 1d).
- Divergence, on enough data, falsifies the implementation or the loss.

**F7, the replay-tagging lesion (S6).**
- With uniform replay, partner specificity of Δ_p falls: the distance between partners' relations, relative to within-partner session variability.
- Sham: replay reweighted by a random tag of equal entropy.

None of these is a face-matching score. Simulated worlds are not evidence, and the numeric checks in this file test algebra only.

---

## Critique 1 and answer (recorded 2026-11-25T13:13:04Z)

**The critique** (independent; full text in critique-design-relative-frame.md; the algebra checks in sims/critique_relative_frame_checks.py are not evidence):
- **Proofs:** 27 items checked: 13 valid, 4 gaps, 8 errors.
  - **The worst error.** The relation is initialised at r = I. From there the learning rule never leaves real rotations, so the "held" channel never appears, and every partner expression is passed through at full strength by a rotation of channels. For an uninformative partner, that rotation drifts at random. This is the copy-in-a-frame the design claimed to escape.
  - **Other errors:** H2 has a counterexample, and T4a's claim that the partner enters only through m̂ is false.
- **The dial: yes.**
  - Per direction, the learned gain is min(κ, 1), where κ is the slope of the agent's own coming body expression on the partner's image. It runs from flat to copy (checked for κ = 0 to 2).
  - A second dial: the constant ν₀τ₀ pulls every relation toward copying at all times.
- **Novelty: recombination,** confirming the author. LieRE, STRING and ComRoPE do not contain the mechanism: they rotate queries and keys by position, with generators fixed after training. In substance, the design is an online-learned linear map capped at norm 1, plus a surprise-driven blend toward copying.

**The design's answer:**
- **Accepted:** the gain theorem, and the copy-in-a-frame failure.
- **The claim "no free gain" is withdrawn.** The design has two gains, κ (learned) and ν₀τ₀ (fixed).
- **Revision owed (next cycle):**
  1. start the relation at "hold everything" (r₀ = iI) and add the real-rotation lemma;
  2. state the exact gain theorem;
  3. decide whether an online-learned, norm-capped map can be made to produce per-expression sign flips without a gain, or whether the design is stood down.
- **Status:** critiqued. The core claim failed; held for revision.
