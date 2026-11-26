# Self-invariant maps: deriving the architecture from "the partner's answers to me do not move me"

A derivation pass in the Deep Sets order (zaheer-2017-deep-sets.md): state the property first, characterise every causal map that has it, then read the architecture off the characterisation. Written 2026-11-26. It carries out the next step that new-core-search-2-synthesis.md suggests: characterise all causal maps of (own history, partner path) that ignore every partner path that is a (possibly nonlinear) function of the agent's own history.

Standards: Q17 as relaxed by Q19/D80 (a precise object and a convincing argument; failures stated concretely). Q18/D78 (the refined copy rule), D81 (know fully, bound expression), D83 (per-expression innate ceilings), D85 (situational sources). There is no emotion label and no named emotion variable anywhere below the language layer.

Algebra checks: `foundations/sims/derivation-si/checks.py` (`python3 -I checks.py`, numpy only, about 3 s; output in `out.txt`). The checks run on hand-made instances and verify only the mathematics stated here (S1–S6). They are not evidence about behaviour or about people (brief: no toy worlds).

**Prior work.** The closest sources are Widrow et al. 1975 (adaptive noise cancelling), Brown, Durbin & Evans 1975 (recursive residuals), Kailath 1968/1970 (innovations), Robinson 1988 and Chernozhukov et al. 2018 (partialling out; double ML), and Frisch–Waugh–Lovell. **None of them could be fetched in this session**: arxiv.org, isl.stanford.edu and en.wikipedia.org do not resolve here. They are cited from standard knowledge, and that is marked wherever a claim depends on them. Read in full, through the project's notes on originals: Kennedy et al. 2014, Forssell & Ljung 1999, Barnett, Barrett & Seth 2009, Beebe et al. 2016, Zaheer et al. 2017.

---

## 0. Summary

- **The property.** The agent's latent state is unchanged when any partner behaviour of the form g(own history) is added to the partner's path, where g ranges over a class G: invariance under p ↦ p + g(a).
- **Characterisation, in general (Theorems 0–1).** Invariance under a set G is the same as invariance under the additive group it generates. It holds exactly when the state depends on the partner only through the partner path modulo the subspace V_t(a) = {g(a) up to t}. This subspace is evaluated on the realised own path.
- **No-go (Theorem 2).** For every nonlinear class worth naming, the state cannot depend on the partner at all. This covers Lipschitz (any constant), polynomial of unbounded degree, and measurable classes, at any horizon including zero lag. It also covers linear filters with horizon at least the elapsed time, and time-varying linear filters. The reason is that such a class interpolates any values on a realised own path whose windows never repeat. Real face and voice streams are such paths. **Pathwise nonlinear self-invariance is vacuous.** It is consistent with keeping the partner only when the class is a finite-dimensional, time-invariant space that is small relative to the data. The partner information kept is the codimension of V_t(a).
- **Finite-dimensional classes (Theorems 3–4).** This covers linear lagged on a basis Φ, and Volterra of fixed degree and horizon. The state must read the partner through a residual (I − P)p, where P is any projection onto span Φ(a).
  - With P orthogonal, the residual is the least-squares residual (Frisch–Waugh–Lovell). Its causal coordinates are the recursive residuals of Brown–Durbin–Evans, the normalised a-priori errors of exact recursive least squares. They are exactly invariant after a burn-in of M samples, and are an isometry onto the quotient, so they never amplify raw movement (S1).
  - With P oblique, along instruments (the agent's own logged exogenous variation), the residual is the instrumental-variable residual. It attributes correctly when the agent itself echoes the partner, but amplifies raw movement by 1/cos θ (1.2 in S5; 9.1 with a weak instrument).
  - Both carry the same information. They differ only in which element of the coset is called "the partner's news", a prior that invariance cannot supply.
- **Statistical version (Theorem 5).** Invariance in L² under adding any function of the own window forces dependence on p − E[p | own window]. That is the partialling-out residual of double ML. Pathwise it must be estimated, and the estimator's regularisation becomes a dial between blindness and leak (S2: kernel ridge keeps 75–96% of the partner while letting 0–16% of a smooth g through).
- **Closed loop (Theorem 6).** Under invariance, the agent's entire closed-loop trajectory is identical for every partner policy ε + g(a), g ∈ ⟨G⟩. The loop agent → partner follows → agent has gain exactly zero, so copying cannot become an attractor through it. The same theorem is the cost: **no invariant state can tell a responsive partner from an unresponsive one with the same news.** "You responded to me" is erased by construction.
- **The forced architecture is known.** It is an adaptive echo canceller (adaptive noise cancelling; acoustic echo cancellation; the mormyrid negative image) in front of an unconstrained recurrent core. In its statistical form it is partialling-out (Robinson/double ML); with instruments, the projection method of closed-loop identification.
- **Novelty verdict: not new.** The only result I have not seen stated for this setting is the no-go theorem, which is elementary and negative.
- **Recommendation: do not design a core from it.** Keep three products:
  1. the no-go theorem, which closes the "nonlinear self-invariance" direction;
  2. Theorem 6 as an evaluation probe, the **G-mirror test**;
  3. an optional fast-lag OLS echo-cancelling pre-stage for the build candidate's partner input. It lowers loop gain but replaces no ceiling, and it must have no slow filters and no constant feature (S4: slow filters remove 59% of a partner's independent slow drift).

---

## 1. Intuition

When you talk with someone, much of what their face does is an answer to yours: they smile because you smiled, slow down because you slowed down. If the agent let those answers drive its own state, a loop would close: it smiles, you smile back, its state takes in your smile, it smiles more. That loop is the copy attractor that has failed earlier designs. The fish in Kennedy et al. solves the same problem for its own electric discharge: it learns to predict what its own command will do to its senses and subtracts that, so what remains is "the world, not me".

The property asked for here is the strongest form of that idea: **nothing the partner does that is a function of what I did may move me.** The Deep Sets method asks what every map with this property looks like. The answers:
- if "function of what I did" means "any function", the only maps with the property ignore the partner entirely;
- if it means "a fixed linear filter of my recent history on a fixed basis", the maps are exactly those that read the partner through an echo canceller's output;
- in every case the property also deletes the thing the operator most wants from the loop: knowing that the partner answered.

---

## 2. Setting and definitions

**Time and paths.** Discrete time t ∈ {0, 1, …} at 30 Hz (continuous time changes nothing below).
- Own path a = (a_t), a_t ∈ ℝ^m: the agent's own face, voice and timing commands or features, including its own turn and tempo event trains.
- Partner path p = (p_t), p_t ∈ ℝ^n: the partner's face, voice and timing features in the agent's own coordinates.
- Write a_{≤t} for the restriction to {0,…,t}, and 𝒫_t = ℝ^{n(t+1)} for partner paths up to t.

**Causal map.** F = (F_t), with F_t : (a_{≤t}, p_{≤t}) ↦ z_t ∈ 𝒵. 𝒵 is any set: a rich latent state, a vector of recurrent activations, or a distribution.

**Partner-response classes.** A class G is a set of causal maps g : own paths → partner paths, with g(a)_t depending only on a_{≤t}. Horizon H means g(a)_t depends only on the window w_t(a) = a_{[t−H, t]}. Time-invariant means g(a)_t = h(w_t(a)) for one fixed h. The classes studied are:

| Class | Definition |
|---|---|
| G_Φ (linear on a basis) | g(a)_t = K Φ_t(a); Φ_t(a) ∈ ℝ^M is a fixed causal feature vector of the own path (lagged copies, exponential filters, sparse mixtures), K ∈ ℝ^{n×M} |
| G_lin,H (all LTI filters of horizon H) | G_Φ with Φ_t = (a_{t}, a_{t−1}, …, a_{t−H}), M = m(H+1) |
| G_Volt,D,H (Volterra) | G_Φ with Φ = all monomials of degree ≤ D in the window entries |
| G_lin,∞ | causal LTI filters of unbounded horizon |
| G_tv | causal linear filters with time-varying coefficients |
| G_Lip,H(L) | g(a)_t = h(w_t(a)), h L-Lipschitz |
| G_poly,H | h a polynomial of any degree |
| G_meas,H | h any measurable function |

**The property (self-invariance).** F is G-invariant if, for every t, every a, every p and every g ∈ G:

  F_t(a_{≤t}, p_{≤t} + g(a)_{≤t}) = F_t(a_{≤t}, p_{≤t}).  (SI)

**Orbit subspace.** Write ⟨G⟩ for the additive group generated by G. The orbit subspace at a is V_t(a) = {g(a)_{≤t} : g ∈ ⟨G⟩} ⊆ 𝒫_t. It depends only on a_{≤t}, because every g is causal.

**Closed loop.** The agent's expression is a_t = A_t(z_{≤t−1}, ξ_{≤t}), where ξ is the agent's own noise, body and other inputs. The partner is p = ε + g(a) for some partner policy, where ε is "the partner's own news". At least one of A or g is strictly causal, so the loop is well-posed.

---

## 3. Results

### Theorem 0 (only the generated group matters)
F is G-invariant if and only if it is ⟨G⟩-invariant.

*Argument.* If SI holds for g₁ and g₂, then F(a, p + g₁(a) + g₂(a)) = F(a, (p + g₁(a)) + g₂(a)) = F(a, p + g₁(a)) = F(a, p). For −g: F(a, p − g(a)) = F(a, (p − g(a)) + g(a)) = F(a, p). ∎

*Consequence.* A "small" class is as strong as its span. Invariance to all 1-Lipschitz responses equals invariance to all Lipschitz responses of any constant, because every L-Lipschitz map is a sum of ⌈L⌉ 1-Lipschitz maps. A bound on the class is never a dial on the property.

### Theorem 1 (quotient characterisation)
F is G-invariant if and only if, for every t, there is a map F̃_t with

  F_t(a_{≤t}, p_{≤t}) = F̃_t(a_{≤t}, [p_{≤t}]_{V_t(a)}),

where [·]_{V} is the coset in 𝒫_t / V_t(a).

*Argument.* For fixed a_{≤t}, SI under ⟨G⟩ says F_t(a, ·) is constant on every coset p + V_t(a). A function constant on cosets factors through the quotient. The converse is immediate. Causality is preserved because V_t(a) depends only on a_{≤t}. ∎

This is Deep Sets' Theorem 2 for an additive, own-path-dependent symmetry. F̃ is otherwise unconstrained, as ρ is in ρ(Σφ). **All of the architecture lies in how the coset is represented.**

### Theorem 2 (no-go: interpolating classes leave nothing)
The partner information an invariant F_t can carry is the quotient, of dimension n(t+1) − dim V_t(a). In particular, if the evaluation map g ↦ g(a)_{≤t} from ⟨G⟩ onto 𝒫_t is surjective (G **shatters** the realised path), then every G-invariant F_t is independent of p_{≤t}.

The evaluation map is surjective in each of these cases:
1. **G_meas,H, G_poly,H, G_Lip,H(L) for any L > 0 and any H ≥ 0, whenever the realised windows w_0(a), …, w_t(a) are pairwise distinct.**
   - Measurable: assign values point by point.
   - Polynomial: Lagrange-type interpolation at finitely many distinct points of ℝ^{m(H+1)}.
   - Lipschitz: the McShane extension h(x) = min_s (v_s + L′|x − w_s|), with L′ = max |v_s − v_r| / |w_s − w_r|, interpolates any values v_s. By Theorem 0 the constant L′ needed does not matter.

   Distinct windows hold with probability one for any continuous-valued noisy stream, even at H = 0. S2: 1,200 samples of a 2-channel path, minimum separation 2.7 × 10⁻³; a Lipschitz h with h(a_t) = −p_t exactly, so (a, p) and (a, 0) lie on one orbit.
2. **G_lin,∞ (unbounded horizon) for a single own channel with a₀ ≠ 0, when t ≥ the horizon.** The causal convolution matrix of a is lower triangular with determinant a₀^{t+1} ≠ 0, so every p_{≤t} is h ∗ a for some h. S3: the inverse exists, but its condition number is 10¹⁸, so the "response" that does this is an absurd filter. Invariance does not care.
3. **G_tv (time-varying linear) whenever a_s ≠ 0 for each s ≤ t:** take K_s = p_s a_sᵀ / |a_s|².

*Argument.* If V_t(a) = 𝒫_t, the quotient is a point and Theorem 1 gives F_t = F̃_t(a). ∎

**What the theorem says.** A pathwise self-invariance can coexist with any partner information only if G is a **finite-dimensional, time-invariant** class whose dimension is small against the number of samples the state has seen. "Nonlinear", "lagged to minutes" and "any function" each push dim V_t(a) toward n(t+1). This answers the synthesis' open question, and the answer is negative: **there is no usable pathwise nonlinear characterisation, because the nonlinear property is empty.**

### Theorem 3 (finite-dimensional classes: the residual and its causal coordinates)
Let G = G_Φ, with Φ_{≤t} the (t+1) × M matrix of features up to t. Then V_t(a) = {Φ_{≤t} Kᵀ}: per partner channel, the column span of Φ_{≤t}, of dimension rank Φ_{≤t} ≤ M.

(i) **Characterisation.** F is G_Φ-invariant iff F_t = F̃_t(a, (I − P_t) p_{≤t}), with P_t any projection (P² = P) whose range is col Φ_{≤t}, applied to each partner channel. The orthogonal choice P_t = Φ(ΦᵀΦ)⁺Φᵀ gives the least-squares residual of p on the own features: the Frisch–Waugh–Lovell partialling-out.

(ii) **Causal coordinates.** Let w_s = e_s / √(1 + h_s) for s > t₀, where:
- e_s = p_s − ŵ_{s−1}ᵀ Φ_s is the a-priori error of exact (unregularised) recursive least squares;
- h_s = Φ_sᵀ (Σ_{r<s} Φ_r Φ_rᵀ)⁻¹ Φ_s is the leverage;
- t₀ ≥ M is the first time the Gram matrix is invertible.

Then:
- (a) each w_s is exactly invariant: least squares is equivariant, ŵ(p + Φ K) = ŵ(p) + K, so e_s is unchanged;
- (b) RSS_t = RSS_{t₀} + Σ_{t₀<s≤t} w_s² (the recursive-residual identity);
- (c) (w_s) together with the burn-in residual is an isometric coordinate system on the quotient, so ‖(w_s)‖ ≤ ‖(I − P_t) p‖ ≤ ‖p_{≤t}‖.

The forced recursive form is a **Kalman filter on a constant parameter state** (RLS), whose standardised innovations are the state's only partner input. An exponential forgetting factor keeps (a) exact, since weighted least squares is also equivariant, and keeps (b) in the weighted norm.

(iii) **What is only asymptotic.**
- Ridge-regularised RLS: ŵ shifts by (G + λI)⁻¹ G K, error O(λ/t).
- (N)LMS, the anti-Hebbian negative image: ŵ_t(p + ΦK) − ŵ_t(p) = K − Π_s (I − η Φ_s Φ_sᵀ/(1 + |Φ_s|²)) K, which decays at the rate of the smallest eigenvalue, that is, at the rate of the slowest own feature.

S1, with M = 22 (2 own channels, 8 lags, 3 slow filters each):
- OLS residual change under a random K: 1.9 × 10⁻¹⁴;
- recursive residuals defined from t = 34 (burn-in ≥ M; the long lags start at zero), change 3.5 × 10⁻¹⁰;
- RSS(burn-in) + Σ w² = 743.530113 against RSS = 743.530110, with |p|² = 1067;
- NLMS innovations under the same g still differ by rms 0.68 → 0.26 → 0.15 → 0.17 across the four quarters of the run: not invariant.

*Argument.* (i) is Theorem 1 with V = col Φ: (I − P) kills V, and two partner paths with the same (I − P)p differ by an element of V. (ii)(a) is the equivariance above. (b) is the standard RLS update of the residual sum of squares (Brown, Durbin & Evans 1975, cited from knowledge; verified to 3 × 10⁻⁶ in S1). (c) follows from (b) and the fact that the w_s are linear in p and vanish on V. ∎

**The same holds for G_Volt,D,H** with Φ = monomials, M = C(m(H+1)+D, D). At m = 50 channels, D = 2 and H = 1 s at 30 Hz, M ≈ 1.2 × 10⁶, so the burn-in alone is about 11 hours of conversation per partner channel. Volterra invariance is formally available and practically the no-go case.

### Theorem 4 (the section is a prior, not a property)
Any two projections P and P′ onto V_t(a) give representatives (I − P)p and (I − P′)p that determine each other: (I − P′)(I − P)p = (I − P′)p, because P′P = P. So the partner information is identical. The choices still differ in two ways that matter downstream, because ceilings and simple readouts are stated in coordinates.

- **Gain from raw movement.**
  - The orthogonal residual is nonexpansive: ‖I − P‖ = 1.
  - An oblique projection along the instrument span, P_IV = Φ(ZᵀΦ)⁻¹Zᵀ with Z = the same features of the agent's own logged exogenous variation b, has ‖I − P_IV‖ = 1/cos θ_max, where θ_max is the largest principal angle between col Φ and col Z.
  - S5: 1.20 with a strong instrument; 9.1 when b is about 4% of own variance.
- **Which element of the coset is called "news".**
  - If the agent itself echoes the partner (D81 fast mimicry), part of the partner's own content ε lies close to span Φ(a). The orthogonal residual then removes it. The IV residual keeps it, because b is exogenous to ε (Forssell & Ljung's projection method).
  - S5: the agent echoes the partner's 20-s news at gain 0.25 and 1 s lag, and the partner follows the agent at gain 0.5. The OLS representative has corr 0.93 with ε and keeps 87% of its variance. The IV representative has corr 1.000 and keeps 101%. Both are exactly invariant (IV: 1.1 × 10⁻¹³).

*Argument.* The algebra is in the statement. The principal-angle norm of an oblique projector's complement is standard. ∎

**The point.** Self-invariance fixes the quotient. It cannot decide which element of the coset is the partner's own news, because that is a causal question (who moved whom) that a pathwise symmetry cannot see: "a function of my own history" is not "caused by me". Answering it needs an assumption, either exogeneity of the agent's own variation (IV) or a model of the partner's own dynamics (ARX). This is the closed-loop identification problem of forssell-ljung-1999-closed-loop-identification.md, reached from the other side.

### Theorem 5 (statistical invariance: the partialling-out residual)
Let (a, p) be jointly stationary with finite second moments. Let 𝒮 = L²(σ(w_t(a)))^n, the square-integrable functions of the own window. If F_t is required to be invariant under p_t ↦ p_t + g(w_t(a)) for all g ∈ 𝒮, as an identity between random variables, then F_t depends on p only through

  r_t = p_t − E[p_t | w_t(a)]

(per time step; the same holds for the whole window).

*Argument.* E[· | w_t(a)] is the orthogonal projection of L² onto the closed subspace 𝒮, so Theorem 1 applies in L². ∎

This is the population counterpart of Theorem 3, and it is exactly Robinson's partialling-out, the "Neyman-orthogonal" residualisation of double ML (Chernozhukov et al. 2018, cited from knowledge).
- **It has to be estimated.** Pathwise, E[p | a] is a learned regression m̂. Fitted on the same path with enough capacity, m̂ interpolates and r̂ → 0, which is Theorem 2 again. DML avoids this by **cross-fitting**: m̂ is trained on other data. The invariance error is then exactly the estimation error of m̂ on g, with none of the orthogonality bonus DML enjoys for a scalar target parameter, because here the target is the residual path itself.
- **The capacity knob is a dial.** S2, kernel ridge on 1,200 own samples, varying the ridge parameter λ:

  | λ | Partner energy kept | Smooth g let through |
  |---|---|---|
  | 10⁻⁶ | 0.75 | 0.0000 |
  | 0.1 | 0.89 | 0.0009 |
  | 10 | 0.96 | 0.158 |

  The bandwidth acts the same way.

### Theorem 6 (the loop is cut, and contingency goes with it)
Let F be ⟨G⟩-invariant and the loop well-posed (§2). For a fixed own noise ξ and partner news ε, let (a⁰, z⁰) be the closed-loop trajectory with p = ε, and (a^g, z^g) the trajectory with p = ε + g(a) for any g ∈ ⟨G⟩. Then (a^g, z^g) = (a⁰, z⁰).

*Argument.* Induction on t. If the trajectories agree up to t − 1, then a_t agrees, since A_t reads only z_{≤t−1} and ξ. Then z^g_t = F_t(a_{≤t}, ε_{≤t} + g(a)_{≤t}) = F_t(a_{≤t}, ε_{≤t}) = z⁰_t by SI. ∎

**Corollaries.**
- **(6a) No copy attractor through the partner's following.** For every partner policy in ⟨G⟩ and every parameter of F̃, the loop agent → partner → agent has gain exactly zero. A copy state cannot be stabilised through that loop. If the partner follows the agent partly outside G, only the leak g_out enters the loop. With an innate per-channel ceiling c_j on the open-loop gain from the representative to the agent's channel j, the loop gain is at most c_j · ‖g_out‖ (small-gain theorem).
- **(6b) Counterfactual identity.** Suppose the "no-partner run" is the run with the partner held at their neutral p₀, and p₀ ∉ V (that is, Φ has no constant feature; §6, F8). Then a partner who only mirrors (p = p₀ + g(a)) leaves **every** route that reads the partner through F exactly at its no-partner value. This includes tempo routes, if the partner's tempo is a coordinate of p and the agent's own turn events are in Φ.
- **(6c) Contingency blindness (the cost).** Two partners with the same news ε, one who answers the agent (g ≠ 0) and one who does not (g = 0), produce identical agent trajectories. **No G-invariant state contains any information about whether, how much, or how the partner responds to the agent.** Watson's contingency, Beebe's interactive contingency and the brief's S5 success criterion (the operator's face following the agent's) all lie in V by definition.

---

## 4. Forced architectures and what they are

| Class G | Forced form of F (Theorems 1–5) | Known mechanism (plain) |
|---|---|---|
| G_Φ, G_lin,H | F̃(a, w) with w the recursive residuals of exact RLS of each partner channel on Φ(a); F̃ any recurrent core | **Adaptive noise cancelling** (Widrow et al. 1975: primary input = partner, reference = own history, output = error); **acoustic echo cancellation** (far end = own expression, echo path = partner's mirroring, near-end talker = partner's news); the **negative image** of Kennedy et al. 2014 in its LMS form, which is invariant only asymptotically (Thm 3 iii); **innovations representation** (Kailath); **Frisch–Waugh–Lovell** in batch |
| G_Volt,D,H | same, with monomial features | Volterra (nonlinear) echo cancellers; practical only at tiny D·H |
| G_Φ with instrument section | F̃(a, p − K̂_IV Φ(a)) | the projection / IV method of closed-loop identification (Akaike; Forssell & Ljung 1999 §5) |
| L² version (all functions of the window) | F̃(a, p − m̂(a)) with m̂ cross-fitted | **partialling-out / double ML** (Robinson 1988; Chernozhukov et al. 2018); adversarial "nuisance-invariant" representations approximate it in distribution only |
| G_Lip, G_poly, G_meas, G_lin,∞, G_tv | F̃(a): no partner input | none: the property is empty |

**What the derivation does and does not force.**
- It forces the front end, an echo canceller, and nothing else. F̃ is unconstrained, exactly as ρ is in Deep Sets.
- Unlike Deep Sets, the forced front end is a classical signal-processing block, and the symmetry is a nuisance to remove, not a structure to exploit.
- Invariant risk minimisation is a different property (one predictor that is optimal across environments) and is not forced here.
- Granger causality and transfer entropy (barnett-barrett-seth-2009-granger-te-equivalence.md) measure the size of V's projection. They are the contingency that Theorem 6c says the state must discard.

---

## 5. Against Q18/D78 and the four lessons of report 8

### Q18 per channel
1. **Set per expression by context and relationship; sign-flippable.** Invariance says nothing here, since F̃ is free. It is compatible: a per-channel readout c_j tanh(θ_jᵀ z) of the representative, as in new-core-search-2 Direction 1, is still invariant.
2. **Innate ceiling.** Not provided. The representative can be passed to channel j with any gain, so the agent copying the partner's news ε is untouched by invariance. That is new-core-search-2 failure (c), and it is now a theorem: the invariance group acts on p by adding functions of a, never on a. Ceilings must be added as before.
3. **Copy not attracting.** Provided on the partner-follows-agent loop for every parameter (6a). The open-loop copy of news needs no attractor argument: it is a forced response bounded by c_j < 1. A residual loop exists only through out-of-class following, at gain ≤ c_j · ‖g_out‖.
4. **Whole-face dial?**
   - The quotient acts per partner channel (V = col Φ ⊗ ℝ^n), but Φ, the forgetting factor and any regularisation are shared across the face.
   - The regulariser (Thm 5) or the basis size moves the whole face between "partner invisible" and "loop open". That is a whole-face scalar on **knowing**, not on flat-to-copy expression.
   - Under D81 it is not a D78 violation, provided innate c_j < 1 cap every expression path, since the loop gain is then < max c_j at any setting.
   - **It must be fixed innately and named.** If it were learned, it would be the dial in disguise.

### The four lessons of report 8
- **L1, "not merely zero-lag blindness".** Met. The residual removes every lag in Φ, and zero lag if Φ includes a_t. It is not merely the zero-lag rule.
- **L2, "ceiling on raw movement".**
  - Met with the orthogonal section: the recursive residuals are an isometry onto the quotient and never exceed the raw partner path in energy over the whole window (Thm 3c). A ceiling on them is a ceiling on raw movement in ℓ² over all lags.
  - This is energy over the window, not per time step: a single w_s can be larger than |p_s|.
  - The IV section breaks it by 1/cos θ (1.2–9.1, S5). Ceilings there must be divided by that factor, and the factor must be monitored.
- **L3, "lags to minutes".** Met only on paper. Covering minutes needs slow features in Φ, and slow features absorb the partner's own slow content, because over a 10-min window the slow subspace has few degrees of freedom. S4, with an own path of 4 channels mixing 2-s and 60-s components:

  | Φ | M | Partner's independent 60-s drift removed (20 seeds) |
  |---|---|---|
  | lags to 3 s plus 5/20/60-s filters | 44 | 59% (sd 15) |
  | same lags, no slow filters | 32 | 5% |

  This is Granger–Newbold spurious regression, built into the state. **Covering minutes and seeing the partner's slow mood conflict directly**, and invariance offers no way to have both. Slow copies are left at 46–65% when the basis is sparse (new-core-search-2).
- **L4, "routes unchanged in the no-partner run counted".**
  - Met exactly for every route that reads the partner through F (6b), including tempo, if tempo is a coordinate of p and the agent's own turn events are in Φ.
  - **Not met for the partner's words.** Claude reads them, and words that answer the agent ("you look cheerful") are a function of the agent's history that no feature basis on face and voice can quotient out. The words route stays outside the invariance and needs its own count, as in every earlier design.

---

## 6. What it destroys, and whether a second channel can restore it

### What is lost
1. **"You responded to me"** (6c). Exactly and for all parameters.
2. **D81 fast partial mimicry, in part.**
   - Spontaneous partner expressions are news, so they survive and can be echoed within c_j.
   - A partner smile that **answers** the agent's smile lies in V and is invisible. The returned smile, shared laughter building up, and mutual escalation of warmth are removed. Human data say these exist (mimicry-context synthesis; Beebe's all-positive interactive contingencies).
   - With the orthogonal section, part of what the agent itself echoed also disappears (S5: 13% of the partner's own news variance).
3. **Reading the other through the agent's own body (Principle 3).** A partner who smiles because the agent smiled is still smiling, and plausibly glad. Inverting the agent's own expression model on the residual reads "nothing happened". The own-body reading must act on the full p. That is a second route from the partner into the state, outside the invariance.

### A second channel: the orbit coordinate
The information removed is the coordinate **along** the orbit. For G_Φ that is ŵ_t (the RLS coefficients) and p̂_t = ŵ_{t−1}ᵀ Φ_t. Both are equivariant: ŵ(a, p + ΦK) = ŵ(a, p) + K. Note that ŵ's increments are G⁻¹Φ_s e_s, so ŵ also carries the partner's news, low-passed at the forgetting rate. Two bounded uses:

- **(R1) Relationship and contingency as a slow parameter.** ŵ per partner is "how this person answers me, per channel and lag". It is a matrix field with n × M entries per person. Feed it to the core only through a saturating map with an innate per-channel gain κ_j. Its bandwidth is the forgetting rate, so it cannot carry a fast copy. Its amplitude bound is κ_j in raw units. That is an amplitude cap, not a gain cap, so the D78 accounting must list it as one more per-channel route.
- **(R2) A bounded echo of returned expressions, normalised by its own estimate.**
  - Let the agent's channel j receive κ_j · p̂_{j,t} / (|K̂_j| + s), where K̂_j is the estimated same-channel response gain (its H∞ norm for lagged responses) and s > 0 is an innate floor.
  - Against a partner who answers with gain K, the loop gain is κ_j K / (K + s) < κ_j **for every partner**. The partner's own gain is divided out, so an exaggerating partner cannot push the loop past 1.
  - With κ_j < 1, the small-gain theorem bounds the agent's departure from its own trajectory by g/(1 − g) of it, and copying cannot become an attractor. S6, with κ = 0.3 and s = 0.2, for K = 0.2 / 1 / 3 / 10:

    | K | Loop gain | Agent's departure from own | Small-gain bound |
    |---|---|---|---|
    | 0.2 | 0.150 | 0.171 | 0.176 |
    | 1 | 0.250 | 0.309 | 0.333 |
    | 3 | 0.281 | 0.359 | 0.391 |
    | 10 | 0.294 | 0.380 | 0.417 |

  - Per channel, innate cap κ_j, sign settable by context. **No dial**: nothing scales the whole face, and the partner's gain cancels.
  - Failure points:
    - K̂ near zero with the wrong sign (s handles that);
    - a lag in K̂ when the partner changes how they answer;
    - lagged responses need the normalisation by the estimated response filter's H∞ norm, not by one coefficient.

### The honest accounting
With R1, R2 and the own-body route on full p restored, the system's no-copy guarantee is no longer the invariance. It is the per-channel small-gain ceilings on every route, exactly the guarantee the build candidate (design-cayley-ledger.md) already has. Invariance then becomes one route among capped routes, the one whose loop gain is zero rather than merely below c_j. That is a real but modest improvement: it removes the partner's following from the main, uncapped knowing channel, so that channel can be as sensitive as perception allows (D81) without feeding the loop. It is not a new core.

---

## 7. Where emotion structure could live

Invariance constrains only the front end. The latent of F̃ is free, so it gives no help with the brief's expressive-structure items, and no obstruction. It does hand the core a **typed decomposition of every partner observation, without labels**:
- own body and expression a;
- other-caused news w (recursive residuals): what the partner did that the agent's own history does not account for;
- other's answer to me, p̂ and ŵ: how the partner responds to the agent.

The split self-caused / other-caused / other's-response-to-self is the agency or causal-attribution dimension that appraisal theories treat as constitutive of social emotions. Here it is computed by the quotient and its orbit coordinate, not learned and not named. Structure follows from it:
- **Relationship as an object.** One ŵ per person (n × M) is a structured, per-channel, per-lag description of the relationship. A state over several people takes the Deep Sets form ρ(Σ_person φ(ŵ_person, history)).
- **Content-dependent selection.** A need-conditioned query could attend over the entries of ŵ (which of my expressions this person answers, and how fast) and over episodes indexed by large w bursts. This is a direction, not derived here.
- **Time scales.** Set by the forgetting factor of the canceller (relationship memory) and by F̃ (moods, temperament), not by the invariance.

---

## 8. Novelty verdict (plain)

**Not new.**
- The characterisation for linear classes is the projection theorem and Frisch–Waugh–Lovell.
- Its causal coordinates are recursive residuals and innovations.
- The forced block is adaptive noise or echo cancellation, already in the project as Kennedy et al.'s negative image.
- The statistical version is partialling-out and double ML.
- The section choice is closed-loop identification's IV or projection method.

The only result I have not seen stated in this setting is Theorem 2 (self-invariance under any interpolating class is empty, with the generated-group remark that makes Lipschitz bounds irrelevant). It is elementary, and it is negative: it removes a direction rather than supplying a mechanism. I could not check the primary literature online (hosts blocked), so "not seen stated" is weaker than usual. The derived architecture is, in one line, **an echo canceller in front of an arbitrary recurrent core**. Measured against attention it is not a candidate core.

---

## 9. Concrete failure modes of the forced form

- **F1. Slow-drift absorption.** Slow own features make the canceller explain away the partner's independent slow mood: 59% at a 10-min window (S4). The agent becomes blind to sustained sadness that happens to drift with its own slow state.
- **F2. Closed-loop misattribution.** With the orthogonal section, partner content that the agent echoed is partly removed (S5, 13%). The fix (IV on the agent's own logged exogenous variation) amplifies raw movement by 1/cos θ, which reaches 9 with a weak instrument.
- **F3. Burn-in blindness and inflated news.** During the first M samples per partner, the quotient is degenerate and exact invariance leaves no partner input. Afterwards, a-priori errors are inflated by leverage, and only the normalised form is safe.
- **F4. Non-uniqueness when own channels are correlated** (the stereo echo-cancellation problem, cited from knowledge). The residual is unique while Φ is collinear, but the coefficients are not. When the agent's own correlation structure changes (a new posture or mood), forgetting-factor RLS predicts with stale coefficients, and a burst of spurious "news" enters the core at exactly the moment the agent changes. Derived, not checked.
- **F5. Out-of-class following passes.** Nonlinear, beyond-basis or slow-lag following leaks: a fast signal copied at 40 s is left at 79% (new-core-search-2). Only the ceilings stop it.
- **F6. The words route.** Words that answer the agent are not quotiented (§5, L4).
- **F7. Contingency blindness and no returned-smile echo** (6c). This is a loss of required behaviour, not a safety failure. R1/R2 restore it only as capped routes.
- **F8. A constant feature absorbs held levels.** If Φ contains a bias term, every held partner expression is in V and invisible. Φ must have no constant, and its slow filters must be few (F1).
- **F9. Learning-rule invariance is only asymptotic.** The anti-Hebbian negative image (NLMS) still passes a mirrored g in S1: innovations differ by rms 0.15–0.17 in the second minute, about 17% of the partner's rms. Only exact least squares is invariant at every step, at O(M²) per step and channel. At M = 52 and n = 50 that is about 1.4 × 10⁵ multiply-adds per frame, trivial on the Mac.

---

## 10. Recommendation

**Do not design a new core from self-invariance.** The derivation worked as a derivation: the property has an exact characterisation. The characterisation, however, either empties the property (every nonlinear class) or reduces it to an echo canceller in front of an unconstrained core (finite linear classes). It erases contingency by theorem (6c), and once contingency, returned-expression echo and the own-body reading are restored, the no-copy guarantee is back to per-channel ceilings.

Keep three products:
1. **Close the nonlinear direction.** Record Theorem 2 in the synthesis: pathwise nonlinear self-invariance is empty. The statistical form is double ML and needs a learned, cross-fitted nuisance model whose capacity is a dial.
2. **The G-mirror test (Theorem 6b) as an evaluation probe for any design, including the build candidate.**
   - Fit g ∈ G_Φ per channel on recorded dyads (Seamless Interaction, D70/D85 restrictions).
   - Replay the design with the partner replaced by p₀ + ĝ(a), generated online from the agent's own output.
   - Compare its state and output with the no-partner run.
   - A design that claims "the partner's answers do not move it" must show zero difference on its invariant routes. Every other route's difference is its loop contribution, measured against its ceiling.

   This is a counterfactual check on internal state, as Q19 asks, and it covers the 20–90 s gap noted in Q27 if Φ reaches 2 minutes.
3. **Optional pre-stage for the build candidate.** An exact-RLS echo canceller on the partner's face channels feeding only the knowing path. Configuration: orthogonal section, fast lags ≤ ~5 s, no slow filters, no constant feature (F1, F8); coefficients ŵ kept as relationship memory (R1). Its value is a zero loop gain on the knowing path. It replaces no ceiling, and it would need its own critique before entering the design.
