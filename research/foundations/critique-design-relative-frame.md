# Critique: Relative-frame transport (design-relative-frame.md)

Independent critic, 2026-11-25, written under questions.md Q16 and Q17. I did not write the design and did not see its author's reasoning. Nothing was downloaded except paper text. No data and no weights.

**Summary verdict.**
- **Proofs.** 27 items checked: 13 valid, 4 with a gap, 8 with an error.
- **The worst error.** The design's own learning rule, started where the design starts it (r = I), never leaves the real orthogonal group O(K). So the held channel, the conservation story and the "compression, not a group element" escape never come into play. The agent enacts every partner expression at full magnitude in an orthogonal frame. For a partner who predicts nothing, that frame drifts at random. This is copy-in-a-frame, the very object the design claims to escape (§1, C1–C3).
- **The dial.** There is one, and its effective gain can be derived exactly. With the relation off O(K), the learned enacted gain along each direction is min(κ_v, 1). Here κ_v is the regression slope of the agent's own coming body-driven expression on the partner's motor image. One scalar κ (innate synergy amplitude relative to partner-image amplitude, or 1/π at learning time) runs the agent from flat (κ = 0) to copy (κ ≥ 1); C4 checks this. A second dial is the unspecified constant ν₀τ₀. With a self-normalised surprise it acts tonically and blends every relation toward copy (C7).
- **Novelty.** The author's verdict, recombination, is confirmed. LieRE, STRING and ComRoPE do **not** contain the mechanism. They are position-only, real SO(d), query/key-only encodings with fixed (trained, not online) generators. What they share with RFT is only the relative-frame identity of Theorem 4c, which is RoPE's identity. Functionally, RFT reduces to a TTT fast-weight linear map projected onto the spectral-norm unit ball, a passthrough of the partner image to the latent, and a surprise-gated blend toward an identity skip (§3).

## Sources read for this critique

| Source | How read |
|---|---|
| Ostmeier et al. 2024, LieRE, arXiv 2406.10322 (HTML) | Full text via a fetch tool, two passes: method, theory (relative-position approximation, App. A 1-D equivalence), App. C implementation, experiments list |
| Schenck et al. 2025, STRING, arXiv 2502.02562 (HTML) | Characters 0–100k of 128k via a fetch tool: Def. 3.1, Thms 3.2–3.5, Cayley/circulant variants, App. A.1 opening. The last 28k (experiment appendices) were not read |
| Yu et al. 2025, ComRoPE, arXiv 2506.03737 (HTML) | 100k of 101k characters via a fetch tool: Thm 1 (relative property iff the angle matrices commute), Prop. 1, Algorithm 1 |
| Su 2025, VO-RoPE (kexue.fm, Transformer-upgrade series part 19) | **Secondary only**, through search summaries and a translation index. The original post was not reached |
| Unitary RNNs (Arjovsky et al. 2016; Wisdom et al. 2016, full-capacity uRNN) | **Not re-read**; cited from memory and marked as such |
| Project files | questions.md Q16–Q17, brief.md Principles, designs.md, math-objects-synthesis.md, mimicry-context-, coordination-, face-development-, emotion-elements- and memory-replay-synthesis.md, and the design in full |

**Numerical checks.** They are in `research/foundations/sims/critique_relative_frame_checks.py`; run them with `uv run python critique_relative_frame_checks.py` from sims/. They check the design's own equations and are algebra checks, not evidence. They are labelled C1–C9 below.

---

## 1. Proof check, theorem by theorem

Notation follows the design: m is the partner motor image, r ∈ U(K), M = Re r, N = Im r.

### Lemma 0 (unitary structure): **valid**
r*r = (MᵀM + NᵀN) + i(MᵀN − NᵀM). The claim follows.

### T1(a) Conservation, and {Re r} = closed unit ball 𝔅: **valid**
- The identity holds because r is an isometry and m is real.
- Surjectivity onto 𝔅 holds through r = U diag(e^{iφ_k}) Vᵀ.
- This is the classical unitary dilation of a contraction (Halmos 1950). The design notes there is "no source cited". It is textbook operator theory, not a new result.

### T1(b) The isotropic set 𝒵 has dimension ≤ 753 < 1024, so measure zero: **valid as mathematics; the reading is wrong**
- Each step checks:
  - MᵀM = cI ⇒ M = |cos θ|O;
  - NᵀN = sin²θ·I;
  - MᵀN symmetric ⇒ J symmetric orthogonal ⇒ J² = I;
  - the dimension count 3K²/4 − K/2 + 1.
- **But measure zero is not unreachability.** The learning flow is attracted *onto* this set whenever the data are isotropic on a subspace. C4 shows this: with target ỹ = κPm, the flow converges to Re r = min(κ, 1)·P, an isotropic gain on the span of P.
- A measure-zero set can be an attractor. The reading ("one scalar amount for every expression" is non-generic) therefore says nothing about what the agent learns.

### T1(c).1 "The enacted coupling is a compression, not a group element": **error**
- The steps are true: Re r is orthogonal iff N = 0.
- The conclusion does not follow, for three reasons.
  - **The escape uses the wrong group.** A generic Re r is an *invertible* contraction (C9: singular values 0.23 to 1.0, all nonzero). That is an element of GL(K). The math synthesis's table lists GL(d) explicitly among the gauge groups. On a single edge, any invertible map is a change of frame. The argument excludes only O(K)-frames.
  - **"Rank-reducing" is false.** Singular values cos φ_k ∈ (0, 1) give a full-rank map. The synthesis's escape route 1 is a *kernel* (some cos φ_k = 0 exactly), and that set has measure zero.
  - **"Singular values differ from one another" is false** in general. The set 𝒵 is the counterexample.
- So the instantaneous enacted map is a frame change in GL(K) whenever it is invertible, which is generic.
- The real escape is the third route, (c).3: dependence on relation state. **Any** per-partner learned linear map has that escape. It is not specific to U(K).

### T1(c).2 Gauge pinning through the identity: **valid lemma; its relevance is a gap**
- The analyticity steps check:
  - c(s) is analytic;
  - the identity theorem extends the relation to all of ℝ;
  - Re Lⁿ ∝ I;
  - B = 0;
  - A² = a²I.
- Relevance gap 1. The frame objection allows time-dependent gauges. Over a response, the partner coordinate m′(t) = exp(s(t)L)m(t) makes the agent an exact copier of m′.
- Relevance gap 2. The "holonomy on the multigraph of lags" sentence is not proved. A loop needs a partner(t₁)–partner(t₂) edge with identity transport. No such edge exists in (F) or (T).
- At steady state (g = r) the transfer is one fixed matrix. The pinning concerns only the ~1 s transient.

### T1(c).3 Reachable transfers fill 𝔅, so the dial rank is K²: **error**
- Reachability assumes a history with ỹ = M₀m for any M₀. But ỹ = Y(b, ḃ)(t + Δ) − sg[a], where Y is a fixed innate map of 8 numbers built from four synergies (smile, cry, orienting brow, lid droop).
- At the backfitting fixed point of J2 and J4, both routes target y. So the column space of every learned M* lies in the image V_Y of Y, which has dimension about 4 to 8.
- Hence dial rank ≤ dim V_Y · K, which is about 128–256 for K = 32, not 1024.
- More importantly, the partner's influence on the face lies in a 4–8-dimensional synergy subspace. W3 admits this; the theorem still asserts K².

### T1(d)(i) The global minimiser is the convex projection M*: **valid open-loop; gap closed-loop**
- Open loop, the steps check: ℓ̄ depends on r only through Re r, the problem is strictly convex when Σ_mm ≻ 0, and 𝔅 is compact.
- Closed loop, the joint law of (m, ỹ) depends on r through three routes:
  1. r → u_emo → μ → effort b_F → y;
  2. J4: a is fitted to y − Re(rm), so ỹ moves with r;
  3. the partner reacts to the agent's face, so m̂ moves with r. T2(d) concedes this.
- This is a performative prediction problem. Repeated minimisation converges, if at all, to a performatively stable point, which is not the minimiser of ℓ̄. Theorem 1(d) is stated as if (m, ỹ) were exogenous.

### T1(d)(ii) I is critical iff Σ_mỹ is symmetric: **valid**
E[Ξ(I)] = ½(Σ_mỹ − Σ_mỹᵀ). Checked by hand.

### T1(d)(iii) Hessian at I: tr(BᵀBS) − tr(AΛA): **valid**
- C8 checks it: numeric −0.8419 against predicted −0.8421.
- The expansion Re e^{εX} = I + εB + ε²/2·(B² − A²) and the absence of a B–A cross term both check.

### T1(d) reading together with the initialisation of §2.6: **error (the worst in the design)**
- §2.6 and W4 start every relation at the identity: R_T = I and Δ_p^at = Δ_p^away = I. The reading says copying is "generically unstable" and that uninformative partners get "held".
- **But on real r the Riemannian gradient (G) is real.** For r ∈ O(K), ε = Mm − ỹ is real, so Ξ = ½(rᵀεmᵀ − mεᵀr) is real skew. Then exp(−ηΞ) ∈ SO(K). The episode leak Log R_ep is real for real R_ep away from −1, and so are (F) and the barycentre.
- So **O(K) is an invariant manifold of the whole relation dynamics.** The instability of Theorem 1(d)(iii) lies in the i·Sym directions, which the gradient never excites from a real start.
- Consequences:
  - **C1.** For ỹ = 0.5m + noise and 20,000 steps from I: max|Im r| = 0.0 exactly. All singular values of Re r are 1. The loss is about 2.0, against the minimum attainable on 𝔅 of 0 (noise-free part).
  - **C2.** If the partner predicts nothing, r performs a random walk in SO(K): ‖Re r − I‖_F = 3.8, all singular values 1, Im r = 0. The design says such a partner's expressions are held. In fact they are enacted at full magnitude, cross-mapped by a drifting rotation.
  - **C3.** Escape needs a perturbation. From 10⁻¹² it takes about 5,000 steps at η = 0.01. After that the flow does reach the predicted held minimiser (singular values ≈ 0.5). In float64 the only perturbation is rounding, or the text route G_ψ.
  - G_ψ does not supply a systematic perturbation. It is trained in replay to imitate the episode updates, which are real.
- Conservation (T1a), the held channel, the "flat face with ‖η‖ = ‖m‖" reading, and H2 are therefore vacuous for the system as specified.

### T1(e) The remaining scalars: **error**
- **ν is not limited to held relations.** For any r, ν → ∞ gives s* → 0 and g → I. Every relation is pulled to copy, not only r ∈ i·O(K). The table states only the flat-to-copy case.
- **ν is tonic, not transient, as specified.** ν = ν₀·e²/(σ̄² + e²), with σ̄² a running scale of the same error. That ratio is self-normalising: for K = 32 and Gaussian errors its mean is 0.49 with s.d. 0.06 (C7); with t(2.5) errors it is 0.40.
  - So ν ≈ ν₀/2 for *every* partner with stationary errors, predictable or not. The steady progress is s* ≈ 1/(1 + ν₀τ₀/2) < 1.
  - ν₀ is not given a value anywhere in the design.
  - C7 shows the effect. With ν₀ = 1 s⁻¹, a hold relation enacts cos(π/2·0.62) = 0.56 of the partner and a full counter enacts −0.38 instead of −1. With ν₀ = 2, the counter becomes +0.14, a mimic.
  - **ν₀τ₀ is a global, hand-set copy-blend dial** (§2 below).
- **The leak is not "never toward copy".** R_ep leaks toward R_TΔ_p, which is I at birth and for every partner met before R_T moves. So λ_ep/η_ep is a ridge toward copy for a new agent. This also contradicts T3(c).
- **The table omits the scalars that set the learned relation.** These are κ (§2), the precision π during learning, and the motor-unit scale of C_ω relative to Y.

### T2(a), (b) Satiability: **valid**
- The dead-band box argument is correct.
- (b) is narrower than its wording, because the relation loss, J3 and J6 are learning signals not derived from Φ. None of them rewards the partner's approval, though, so the conclusion stands.

### T2(c) No term increasing in partner smiles; sign-flip invariance of b_P: **error**
- b_P is defined in §2.5 as "the smoothed decrease of the latent's own prediction error".
- The proof instead proves sign-flip invariance of ‖m̂ − m̂_pred‖, the *surprise* quantity of ν, under a linear predictor.
- The latent is a GRU, which is not equivariant to channel sign flips. Its prediction-error decrease can perfectly well be larger for smiles, for example if smiles are more predictable.
- The claim is unproved for the quantity that matters. W9 (curiosity-driven provocation) is a symptom of this.

### T2(d) The relation gradient is myopic: **valid**
It is read off (G).

There is a related route, not covered: the policy J5 differentiates through the body predictor and chooses the display frame Γ. Since u_emo = Re(Γ(a + z)), Γ multiplies the relation. The effective enacted map is Re(Γg), not Re g.
- An effort cost in Φ (b_F) gives J5 a gradient toward rotating everything into ℍ: a policy-driven route to a flat face.
- J5 can also choose Γ = g*, which is copy.
- Nothing in T1 constrains Γ.

### T2(e) Bounded dependence: **gap**
"The reachability claims are properties of f_b as specified", but f_b is not specified by equations (§2.5 gives prose). The corollary cannot be checked.

### T3(a): not a theorem (design constants)

### T3(b) Matching first, context after, with angle-dependent latency: **valid for L ∈ i·Sym; gap otherwise**
- Staying on the curve g = exp(sL) and the ODE ṡ = (1 − s)/τ₀ − νs both check.
- The crossing times check (C6): 0.83 s for θ = π and 1.66 s for θ = 2π/3.
- **The per-axis formula cos(θ_k s) needs real eigenvectors, i.e. L = iA.** The design hedges with "in general the share is the real part along the axis".
- For L with a real-skew part (the only kind the flow produces from I, per the error above) the transient does not hold; it cross-maps. See H2.
- The angle-dependence prediction (F3) does not separate RFT from a plain linear blend M(s) = (1 − s)I + sM*.
  - The blend crosses zero at s = 1/(1 − cos θ), which also decreases in θ.
  - For θ = π the two crossings coincide (s = ½).

### T3(c) Nested leaks; barycentre bound on temperament: **bound valid; reading an error**
- The bound is valid under three conditions: principal branches; the old R_T being the barycentre of the old relations; and the re-centring identity R_T,new Δ_p,new = R_T,old Δ_p,old, which checks.
- "Never toward copy" is false at birth (see T1e).
- **With one dominant partner the levels collapse.** This is the S6 case: w_op ≈ 1.
  - R_T → R_TΔ_op, so Δ_op → I. Temperament *becomes* the operator relationship.
  - A stranger "starts at the temperament", so a stranger inherits the operator relationship.
  - The operator-versus-stranger specificity that E1/S6 measures is driven toward zero by the consolidation rule itself. The 1/N rate bound gives no protection when N ≈ 1.

### T3(d), (e): statements, not theorems
They are honest about which constants are set by hand.

### T4(a) The partner enters only through m̂: **error**
Counterexample from the design itself. Three paths take the partner observation o into the state without passing through C_ω:
- gaze directedness γ, computed from the partner's head pose in o, enters r through Δ_p(γ);
- the partner-identity embedding uses landmark geometry and voice statistics;
- raw prosody (8 features) is a direct input to GRU_f (§6, row 9).

Two observations with equal C_ω(o) but different head pose give different trajectories. The linear-pseudoinverse corollary holds only for the m̂ path.

### T4(b): definitional, **valid**

### T4(c) Relative-frame invariance: **valid but trivial**
- It is unitary invariance of the inner product, RoPE's identity in another group.
- Note also that a is real, so κ = Re(a*z) = aᵀ Re z. Agreement sees only the *enacted* part of the partner, and a hold relation makes κ = 0. "Suppressing does not reduce resonance" holds for Γ but not for the relation r.

### T4(d) Decodability is stance-independent: **valid**
g*z = m̂.

### T4(e): a definition, not a theorem

### H1 Per-expression gating in independent directions: **gap**
It inherits the T1(c).3 error. The histories it needs are not realisable by a body whose target lives in a ≤8-dimensional synergy image, and the caveat in the design does not repair the proof.

### H2 "Sign flips pass through holding, never through not seeing": **error**
- This is true only for L ∈ i·Sym.
- **Counterexample (C5).** Take a real relation L = π(e₂e₁ᵀ − e₁e₂ᵀ) and partner m = e₁ (say, the smile channel). Along the geodesic from match to counter:
  - the enacted output goes (1, 0) → (0.71, 0.71) → (0, 1) → (−1, 0);
  - the held output is zero throughout.
- So the sign flip passes through *full enactment of a different expression* (channel 2), not through holding.
- Because the learning flow from I stays real, every counter the design will actually learn is of this kind.

### H4: not proved
The fast route via G_ψ is learned only to predict relation drift, see §4.

### H6 Order effects by BCH: **valid but not distinctive**
e^X e^Y = e^Y e^X e^{[X,Y] + O(3)}, with [X, Y] = η²[Ξ_A, Ξ_B]. Any non-commuting update has order effects, including an unconstrained matrix delta rule. F5's diagonal lesion therefore separates RFT only from diagonal models.

### Tally

| Verdict | Items |
|---|---|
| valid (13) | Lemma 0; T1a; T1b (math only); T1c.2 (lemma only); T1d(ii); T1d(iii); T2(a,b); T2d; T3c (bound only); T4b; T4c; T4d; H6 |
| gap (4) | T1d(i) closed loop; T2e; T3b beyond L ∈ i·Sym; H1 |
| error (8) | T1c.1 (GL frame); T1c.3 (dial rank K²); T1d reading plus initialisation (O(K) invariance); T1e (ν universal and tonic, leak toward copy at birth, omitted scalars); T2c (wrong quantity); T3c reading (never toward copy; collapse with one partner); T4a (bypass paths); H2 (counterexample) |

---

## 2. Dial hunt

**A learned relative group element per expression is copy-in-a-frame, as specified.**
- From r = I the relation stays in SO(K) (C1, C2). On a single edge with a fixed partner, the enacted map is then an orthogonal frame change, with no held part and no magnitude change. This is exactly the math synthesis's reduction.
- Across partners and episodes the frames differ, so the dial rank exceeds 1. But that is the escape any per-partner learned linear map has (synthesis route 3), not one that U(K) provides.
- If the relation is started off O(K) (C3, C4), the design does escape the O(K)-frame. It lands in a GL(K)-frame (T1c.1) whose per-axis gains are set as follows.

**Derived effective gain (dial 1: contingency strength κ).** Assume Σ_mm = σ²I (whitened partner image) and target ỹ = κ·Pm + noise. P is the projector onto the partner directions that predict the agent's own body-driven expression, and its range lies inside the synergy image V_Y. T1(d)(i) then gives

  M* = argmin_{‖M‖≤1} E‖Mm − ỹ‖² = min(κ, 1)·P,

that is, singular-value clipping of the least-squares slope. C4 confirms it: κ = 0, 0.3, 0.7, 1, 2 give diagonal gains 0, 0.30, 0.70, 1.00, 1.00.
- One scalar runs the face from flat to copy on V_Y.
- The scalar is not one number in the code. It is set by three things:
  - **the amplitude of the innate synergy map Y** relative to the motor-unit scale of C_ω;
  - **the perceptual precision π during learning**: m̂ = πm, so the slope is κ/π, and partners seen poorly while learning end up closer to copy;
  - **the dead bands δ_i**: inside the box Φ = 0 and the smile synergy (−dΦ/dt) is silent, so wide bands drive κ → 0 and the relation toward hold.
- At the saturated end (κ ≥ 1) M* is the polar factor on V_Y: an orthogonal map, i.e. copy-in-an-O-frame again.

**Dial 2: ν₀τ₀, a tonic blend toward copy.**
- Through the self-normalised surprise, g settles at exp(s*L) with s* ≈ 1/(1 + ν₀τ₀·E[ratio]), where E[ratio] ≈ 0.4–0.5 (C7). For a hold relation the enacted gain is cos(π/2·s*). That function runs from 0 (ν₀ = 0) to 1 (ν₀ → ∞) for every relation.
- ν₀ has no stated value. The design must specify an absolute surprise scale, for example σ̄² as a slow, fixed prior, or admit ν₀ as a global dial.

**Dial 3: λ_ep/η_ep at birth.** It is a ridge toward R_TΔ_p = I, that is, toward copy, until the slower levels move.

**Dial 4: the display frame Γ chosen by the policy.** It multiplies the relation, so the policy can rotate toward copy (Γ = g*) or toward flat. The design does not bound it.

**Verdict.** RFT has no single *parameter* labelled gain. It does have an exact effective gain per direction, min(κ_v, 1)·cos-blend(ν₀τ₀), which one scalar family runs from flat to copy. The design converts the gain into a regression slope (a fitted dial, like the v3 role-swap sketch) plus a hand constant ν₀.

---

## 3. Reduction attempt

**What T1(d)(i) actually says.** The objective depends on r only through M = Re r ∈ 𝔅. So the face path is a **linear fast weight constrained to the spectral-norm unit ball**, a 1-Lipschitz linear layer, trained by test-time training on the target y(t + Δ) − a(t).
- The held output η = Nm is, by T4(d), information-equivalent to m̂.
- Functionally, then, the latent simply receives the partner image. The particular unitary completion N of M is not unique and changes nothing decodable.

**Reduced form.**

  face_partner(t) = M(t)·m̂(t),  M(t) ≈ blend(I, M_p; s(t)),  latent ← m̂,

where:
- M_p is a per-partner TTT weight projected to ‖M_p‖ ≤ 1;
- s(t) is a surprise-gated first-order blend from an identity skip to M_p.

The geodesic on U(K) differs from the linear blend only in the shape of the transient. The two have the same endpoints and the same angle ordering of zero crossings (§1, T3b).

**Against the families the brief names:**

| Family | Contains RFT's mechanism? | Exact difference |
|---|---|---|
| RoPE (Su 2021) | Only Theorem 4c (relative-frame identity) | Fixed commuting 2×2 rotations of q/k by position; no value path |
| **LieRE** (read) | **No** | Learned dense skew generators per layer and head, R(p) = exp(Σ p_i A_i) ∈ SO(d), applied to **queries and keys only**, position-only, fixed after training. Relative property only approximate (non-commuting). No complex group, no Re readout, no online or state-dependent rotation, no value rotation |
| **STRING** (read) | **No** | Commuting learned generators; Thm 3.2: every translation-invariant, continuously differentiable R with R(0) = I is STRING; Thm 3.4: STRING = P·RoPE·Pᵀ (RoPE in a learned basis). Real SO(d), q/k only, position-only |
| **ComRoPE** (read) | **No** | Thm 1: the relative-position property holds iff the trainable angle matrices commute. Real SO(d), q/k only |
| VO-RoPE (secondary) | Partly | Rotates values by position and inverse-rotates the output, so a *relative* rotation does reach content. This refutes §4's general claim that in the rotary family "the rotation never reaches the content". It is still fixed, position-indexed and real |
| uRNN / full-capacity uRNN (not re-read) | Closest on the group side | Learned unitary transitions on U(N), trained by Riemannian gradient on the manifold. They are trained offline, not as an online per-partner state, and their readout uses Re and Im together |
| TTT / delta rule | Yes, with a constraint | §4 already concedes this |
| DeltaProduct / negative-eigenvalue linear RNNs (Grazzi 2025) | The non-commuting product and the contraction ball | §4 already concedes this |
| Rotating Features / CAE | Phase as a second message | Per-feature fixed phase biases versus RFT's state rotation |

**Verdict.** The author's "recombination" verdict is **confirmed**. The candidate "second-clause" contribution, deleting the gain as a free quantity, **does not survive**: the gain reappears as κ and ν₀τ₀ (§2). The surviving original content is two items:
1. the specific copy-stability condition (copy is stable iff the regression slope is ≥ 1; T1d(iii)), which is the clipped-regression fact written as a Hessian;
2. the idea of a held channel that keeps the partner image in the latent while gating it out of the face. That idea needs no U(K): a 1-Lipschitz map plus a passthrough does the same.

**Correction to the design's §7.** LieRE, STRING and ComRoPE do not shrink the claim. They are further from it than the design feared, and nothing in them rotates values or holds state. The claim shrinks for the different reasons above.

---

## 4. What it fails to explain

| Requirement (source synthesis) | RFT | Status |
|---|---|---|
| Per-expression sign flips: smiling at a rival's pain, brow relaxation at a rival's distress, smiling at anger under power (mimicry-context §2) | Representable as a counter axis. **Learnable only if the partner's expression predicts the agent's own synergy target y.** The body has energy, integrity, effort and learning progress, with no concern shared with or opposed to the partner's outcomes. "The rival's loss is my gain" and "soothe the partner" therefore have no route into Σ_mỹ. From I, learned counters are real rotations that cross-map rather than hold (H2) | **fails** |
| Fast matching, then later context (Carr; Weyers; the Mauersberger exception) | T3(b) gives it for L ∈ i·Sym. Carr found *different muscles* for early matching (corrugator) and late context (zygomaticus), whereas RFT predicts the same channel crossing over. With self-normalised ν the "early matching" is tonic, not onset-locked | partial |
| Partner history at two time scales (Hofman: immediate loss of smile return after an unfair offer; reputation) | Δ_p per partner. The fast route G_ψ learns only to predict the 30-s relation drift that the body-target statistics produce. An unfair offer does not move any body variable, so G_ψ has nothing to learn from it. With one dominant partner, consolidation copies the operator relation into the stranger's start (T3c) | **fails for the S6 claim** |
| Tracking separate from aligning (coordination §1e) | T4(d): this is a real strength | meets |
| Roles, direction and lag asymmetry (coordination §1c) | No role state; the relation is the agent's alone | missing |
| Regulation of a joint deviation; coregulation after a disturbance (§1b) | Nothing targets a joint variable | missing |
| Metastable dwell and escape (§1f) | Absent (W6) | missing |
| Hidden-regulator bound (§1g) | T2(e) is asserted but f_b is unspecified | gap |
| Wanting vs liking (emotion-elements row 11) | Not derived (author agrees) | missing |
| Agency and coping potential (row 9) | Not represented | missing |
| Precision on body error (row 7) | Missing | missing |
| Two face routes (face-development §1) | u_emo, u_del and c_ref converge on one muscle layer with clinical lesion predictions; the masking signature follows | **meets** (the design's strongest part) |
| Contingency-learned visual-to-motor map that reverses under crossed training (face-development §4.7) | C_ω is trained by self-observation and cycle consistency, not by a contingency (Rescorla-Wagner) rule, so crossed training would not reverse it | partial |
| Memory and replay (memory-replay §1.9, §2–3) | Three problems. (1) It stores m̂ = C_ω(o), a learned-coordinate code. Refreshing C_ω in replay invalidates stored episodes: lesion L9, specificity lost across an upgrade. It should store o. (2) The tag w = \|ΔΦ\| + ‖Ξ‖ is a single salience score, not eligibility × global modulator with a coverage term. (3) F7 lesions *priority*. The synthesis predicts that this lesion leaves specificity largely intact (Rolnick; L2) and that context reinstatement (T2/L1) is the one that removes it, so F7 can fail for the wrong reason | **gap** |

---

## 5. Buildability on an M1 Pro, 16 GB

- **Parameters and per-frame compute are fine.** About 0.66 M parameters, and the 0.12 ms eigendecomposition is plausible for K = 32. PyTorch MPS lacks complex linalg such as eigh, so the relation core should run in numpy or on the CPU, as the author measured.
- **Self-observation doubles the tracker.** Training F_ω/C_ω online from the agent's own rendered face means running the face tracker twice per frame: about 26 ms of the 33 ms budget, before the GRUs, if the browser figure of 13 ms transfers to Python. Run self-tracking at ≤ 10 Hz or in replay.
- **Draft selection is not real-time as specified.** Scoring N drafts needs N TTS syntheses to get each draft's prosody. At a real-time factor of 0.55–0.65, three drafts of a 5-s reply take about 9 s serially before speech starts. Use a learned text-to-prosody predictor, or score only the first chunk.
- **C_ω takes 66-dimensional input (face plus prosody), but a draft has no face.** The design does not say how a draft's voice-only trajectory is passed through it.
- **Memory** (2–3 GB) is plausible.

---

## 6. The most important fixes, in order

1. **Start the relation off O(K) and say why. Then restate T1 honestly.**
   - The natural start is r₀ = iI, "hold everything". It matches the design's own developmental story (C_ω weak, nothing mimicked) and makes copy earned. At r₀ = iI the gradient has an imaginary-symmetric component, so the held directions are live.
   - Add the invariance lemma (O(K) is invariant under (G)) as a theorem with this consequence.
   - Replace the "no free gain" claim with the exact gain theorem: per-direction enacted gain = min(slope, 1), modulated by the ν-blend. Name κ, π-at-learning and ν₀τ₀ as the design's dials.
2. **Fix ν.** Make surprise absolute: a fixed or slowly learned prior scale, not the running scale of the same error. Specify ν₀, and prove that ν's time-average is zero for a predictable partner. Otherwise the copy blend is tonic.
3. **Give the body a concern that the partner's outcomes can enter.** Examples are a shared-goal or competition variable, or controllability. Without one, the human sign flips (rival, cooperation, power) cannot be learned through Σ_mỹ. Prove the rank of V_Y needed for H1, or drop the K² claim.
4. **Separate temperament from a single dominant relationship.** For example, barycentre over episodes or contexts rather than partners, or a stranger prior that is not R_T. Otherwise S6's operator specificity is removed by construction.
5. **Correct T1(c).1, T4(a), T2(c) and H2 as listed.** Also bound or constrain the policy's display frame Γ, which multiplies the relation unconstrained.
6. **Memory: store o, not m̂, and use the synthesis's T2 context-reinstatement lesion for F7.**
