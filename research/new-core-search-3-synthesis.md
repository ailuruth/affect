# Searching for a new core mechanism, third pass: conserved charges, gauge symmetry, two-agent equivariance, infant self/other (synthesis, 2026-11-27)

Sources read in full for this pass (notes in research/):
- noether-1918-invariant-variation-problems.md (Theorems I and II, the sourced form, proper vs improper conservation laws; Tavel translation);
- favoni-2022-lattice-gauge-equivariant-cnn.md (links, plaquettes, Wilson loops as the gauge-invariant content; L-CNN layers);
- alet-2021-noether-networks.md (learn a conserved quantity instead of a symmetry; conservation as a prediction-time loss);
- vanderpol-2022-multi-agent-mdp-homomorphic.md (between-agent symmetry = agent permutation + transformed edge features; per-agent local transforms are not symmetries);
- satorras-2021-egnn.md (relative-coordinate equivariant interaction; in a dyad its zero is the copy state);
- kristen-antonow-2015-emerging-self.md (Meltzoff's social-mirroring task with timing equated: form match is a separate signal; infants probe with abrupt stop–restart);
- markova-2019-interactional-rhythms.md (perspective: concurrent vs sequential synchrony; rhythm as a carrier).

**Not reachable** (the proxy refused the hosts, or they do not resolve here): Rochat 2003 (Consciousness and Cognition), Koós & Gergely 2001 (the "flickering switch"), Nagy & Molnár 2004 ("homo provocans"), Nagy et al. 2005 (Pediatric Research), Maister et al. 2020 ("Self or (M)other?", PMC blocks automated access), Geangu et al. 2018 (Scientific Reports), Yang & Mills 1954. Gergely & Watson 1996, Bahrick & Watson 1985, Watson 1997, Rochat & Morgan 1995 and Rochat, Neisser & Marian 1998 were already noted and are not repeated. The developmental reading of this pass is therefore thinner than asked. No claim below rests on an unread source. Standard mathematics used without a source read here is marked **(standard)**: Lax-form isospectrality, the Schur–Horn theorem, Cauchy interlacing, Brockett's double-bracket flow, the Adler equation, von Neumann's trace inequality. Each is checked numerically where it is used.

Checks: `foundations/sims/new-core-search-3/checks.py` (`python3 -I checks.py`, numpy only, a few seconds; output in `out.txt`). The checks S1–S7 verify only the algebra stated here, on hand-made instances. They are not evidence about behaviour or about people (brief: no toy worlds).

No emotion labels or named emotion variables appear below the Claude layer. "Channel" means a face or voice feature in the agent's own coordinates.

## What this pass adds

- **Global symmetry gives charges; local symmetry gives only redundancy.** Noether's Theorem I turns a ρ-parameter invariance into ρ conservation laws. Theorem II turns invariance under arbitrary functions (a gauge freedom) into identities among the equations, and §6 shows the resulting conservation laws are "improper". A gauge principle can type an architecture. It cannot make slow variables or time scales.
- **The sourced form says exactly who can change a charge.** With sources (footnote 15), Div B^{(λ)} = Σ T_i δu_i^{(λ)}: an input changes a charge only through its component along that symmetry's direction at the current state. So an input that is itself a symmetry motion (along the orbit) changes no invariant of the orbit, whatever its strength or timing. This is the one new derivation principle of this pass.
- **In a two-agent setting, equivariance points at copy.**
  - Relative-coordinate interactions (EGNN) move the agent along its difference from the partner, so the copy point is the distinguished fixed point, and a learned scalar decides whether it attracts.
  - Between-agent symmetry lives on edges (van der Pol et al.).
  - Per-agent local frames are a gauge freedom, so only holonomy is invariant (Favoni et al.).
- **Infants keep form and timing apart and probe actively.** With temporal contingency equated, 12-month-olds still prefer the imitator. They test the partner with "sudden stop and restart … while eyeing the experimenter" (Kristen-Antonow et al.; small effects, r ≈ 0.3). A core that reads "you responded to me" only from timing misses the form signal. A core that reads only form invites copying.

---

## Direction 1: the isospectral core. The partner can rotate the agent's state; only the agent's body can charge it

### (1) The object
- **State.** A real symmetric matrix M ∈ Sym(n), with n in the tens to hundreds.
  - Its spectrum λ(M) is the agent's intensity profile.
  - Its eigenframe (the point on the isospectral orbit O_λ = {UΛUᵀ}) is the arrangement of that intensity over the agent's own modes.
  - The first m coordinates of a fixed innate basis are the agent's expression channels: the face and voice motor synergies its body can produce. The output is y_k = M_kk, for k ≤ m.
- **Dynamics.**

  Ṁ = [Ω_θ(M, b, c), M] + S_θ(λ(M), b) + [X(p, M, c), M]

  - **Own rotation.** Ω_θ is any learned antisymmetric-valued map: the most general isospectral (Lax-form) flow **(standard)**. It may be an attention-like map over the state, the body b, memory and context c. A double-bracket term Ω = −γ[M, N(b, c)] makes the flow a gradient flow on the orbit toward an own target N **(standard: Brockett)**.
  - **Own-body source.** S_θ = U g_θ(λ, b) Uᵀ, where M = U diag(λ) Uᵀ. It is a spectral function of M and depends otherwise only on interoceptive body variables b. It is the only term that changes the spectrum. Satiable by construction: g drives each λ_i toward a body-set level and is zero there.
  - **Partner port.** X = Σ_j w_j(M, c) p_j A_j. Here p_j is a partner channel read through the agent's own body (perception not specified here). A_j is a fixed innate antisymmetric generator per partner channel. |w_j| ≤ c_j is innate, and the sign of w_j is free, set by state and context.
  - **Typing rule.** Every partner-derived quantity (face, voice, tempo, turn events) enters only inside X. That includes anything inferred from the partner, however indirectly. Nothing partner-derived may enter S.

### (2) Properties for every parameter value (derived; checked)
- **T1 (Noether/Casimir: the partner never charges).**
  - d/dt tr(M^q) = q tr(M^{q−1} S) for every q, every θ, w, p and c. The reason is that tr(M^{q−1}[Z, M]) = 0 for any Z, by cyclicity.
  - So λ(M) evolves by dλ/dt = g_θ(λ, b): a closed, partner-free system. This is Noether's sourced law with the partner as a pure symmetry motion. (S1: eigenvalue change 4·10⁻¹⁴ after 2,000 random, state-dependent, sign-flipping partner steps.)
- **T2 (one budget for all routes).** The diagonal of any matrix on O_λ lies in the permutohedron of λ **(standard: Schur–Horn)**. Hence, along every partner path and every internal route:
  - Σ_{i≤n} M_ii = tr M (zero-sum over all modes);
  - the sum of any r channels is at most the sum of the top r eigenvalues;
  - max_k y_k ≤ λ_max.

  The budget is set by the body, and through T1 the partner cannot move it (S2).
  - **Closure.** The class of flows Ṁ = [Z(t), M], with Z any input- and state-dependent antisymmetric matrix, is closed under sums (parallel routes), composition (series), feedback (Z depending on M), learning (any update of θ or w keeps the form) and time. The symmetry-no-copy synthesis found that skew maps are closed only under sums and orthogonal groups only under products. A Lie algebra acting by commutators is closed under both.
  - What survives closure is a budget, not copy-freedom (see (4)).
- **T3 (coherence-gated leverage: "you responded to me" without a correlation detector).**
  - The partner's first-order effect on channel k is ẏ_k = ([X, M])_kk = 2 Σ_i X_ki M_ik. It is proportional to the agent's own coherences M_ik between channel k and the modes the generator touches.
  - At internal rest (M diagonal in the channel basis), the first-order effect is zero (S3: exactly 0). What remains is second order and even in the partner's sign: it only pulls the agent off its own target (S5: resting at the top of its block, y₁ moves 3.000 → 2.962 for partner +1 and for −1).
  - Coherences arise when the agent's own rotation Ω moves it, that is, when it is acting or changing. So partner input timed during or just after the agent's own change has signed leverage, and partner input while the agent rests has almost none. The window is the decay time of the agent's own coherence.
  - This is a structural form of contingency gating. It is not hold-blindness by a commutator of increments (new-core-search-synthesis.md): it is a product of the partner's input with the agent's *state*.
- **T4 (time scales from a subgroup chain: access is structural).**
  - Choose a chain so(n) ⊃ so(n₁) ⊃ … ⊃ so(n_L) and put the partner generators A_j inside the innermost so(n_L).
  - Then the spectra of every leading k × k block with k ≥ n_L are invariant under the partner (the Gelfand–Tsetlin variables of those levels; S6: change ≤ 2·10⁻¹⁵ for k ≥ j, 0.51 at k < j).
  - By Cauchy interlacing **(standard)**, each inner level's variables are confined between the next outer level's eigenvalues.
  - So, structurally, with no time constant:
    - the partner can reach only the innermost (fastest-moving) level;
    - each level caps the one inside it;
    - the outermost spectrum is reached only by the body.

  Reflex, mood and temperament become *which processes may touch which level*. The durations at each level are still set by rates (γ, g), so time scales are only half from structure: order and access are structural, magnitudes are not.

### (3) How it meets the needs
- **Emotion as structure in a rich latent.**
  - The state has n(n+1)/2 dimensions; the orbit has n(n−1)/2.
  - The double-bracket flow toward N has n! equilibria on a generic orbit (the permutation-sorted diagonals). Which one is stable is decided by the ordering of N **(standard; not checked here)**.
  - Discrete, label-free "which intensity sits on which mode" assignments therefore emerge, and switch when the own target's ordering changes (a bifurcation of the own landscape, not of the partner). Valence- or arousal-like quantities would be read out of λ and the assignment, never set.
- **The other through the own body, per channel, sign-flippable, capped.**
  - **Block generators** (A_k couples expression channel k to an internal mode). Each block reduces to an Adler equation θ̇_k = w_k p_k − κ_k sin 2(θ_k − θ₀_k) **(standard; derived for the 2 × 2 block)**, with y_k = λ_b + Δλ_k cos²θ_k.
  - When locked (|w_k p_k| < κ_k), the response slope at p = 0 is −Δλ_k sin(2θ₀_k) w_k / (2κ_k).
    - Its sign is set by the agent's own resting angle θ₀_k and the sign of w_k, so it flips with the agent's own state and with context. S5: at θ₀ = π/8, partner +1 raises y₁ from 2.561 to 2.770 and −1 lowers it to 2.298.
    - Its magnitude is capped by the innate |w_k| ≤ c_k and by the agent's own spectral gap Δλ_k.
  - **Strong partners unlock** (|w p| > κ): the angle slips and the time-average falls toward the block mean (S5: gain 8 gives 1.824, against a block mean of 1.5). Overwhelming input decouples rather than captures.
- **Copying is not made attractive by the partner's strength.** T1–T2 hold for every coupling; unlocking caps capture.
- **Contingency.** T3 builds the timing gate into the operator. Form match, which infants use separately (Kristen-Antonow et al.), would have to be read in the agent's own appraisal through Ω, a route that stays inside the typing rule.
- **Claude** (a prediction, not a design). If regulation enters only as an own rotation (a term in Ω chosen by the conceptual path), it can change *which* modes carry intensity, including moving it off the expression channels into internal modes. It can never change *how much* the agent holds, which only the body can. That is a precise, ablatable difference between reappraisal-like and body-level change.

### (4) Novelty verdict (honest)
- **Recombination.** The pieces are known:
  - Lax-form and Lie–Poisson isospectral dynamics (Lie–Poisson neural networks exist as physics learners: arXiv search found LPNets, CLPNets and LLPNNs, not read);
  - Brockett's double-bracket gradient flow;
  - per-block Adler phase locking. For block generators the partner coupling *is* phase locking to the partner's integrated signal, which is in the excluded oscillator family.
- **What is new, as far as this pass found:** the design rule that the partner may enter only as an element of the symmetry algebra and the body only as a spectral source. This gives a single all-routes budget (T1–T2, closed under every composition) and coherence-gated leverage (T3). No earlier design in designs.md has a bound that holds for every route at once without counting routes.
- It does not clear the bar of a new computation on the level of attention.

### (5) Against the lessons of reports 8 and 9
- **Not a copy-blind input** (lesson: ignoring simultaneous movement alone is not new). It is a conserved budget.
- **Limits across minutes.** T1–T2 hold at every lag and time scale exactly, since the spectrum is partner-invariant forever. But the limit is relative to the agent's own budget, not to the partner's raw movement (see failure (a)).
- **Routes that do not depend on the face now.** Tempo and turn events are partner-derived, so the typing rule puts them in X, and T1 covers them. A violation is a type error visible in the code (anything partner-derived feeding S or b).
- **Report 9 (contingency erased).** Contingency is kept (T3), not cancelled. The G-mirror test (derivation-self-invariant-maps.md) applies unchanged and is the right first evaluation.

### (6) Most likely concrete failure
- **(a) A partner who fits inside the agent's budget can be followed, and the following attracts.**
  - Within the locking range, the locked state is a stable fixed point that tracks p with slope up to c_k Δλ_k / (2κ_k).
  - A reserved partner whose range is inside [λ_b, λ_a] can therefore be followed closely and stably. This is the same failure report 8 found ("limits set against the calibrated face let a reserved person's copy through"), reached by a different road.
  - The ceilings that prevent it are again innate per-channel c_k, which is the Cayley-ledger content in other clothes.
- **(b) Held levels leak.** The angle integrates the partner's signal (θ̇ = w p), so a held partner expression produces a sustained offset (S5: held +1 moves y₁ by +0.21). Only the locking term stops it; nothing makes the port phasic.
- **(c) Smearing.** Generators that rotate between expression channels move intensity from one channel to another in a sign-blind way. An energetic partner flattens the agent's expressive contrast (S5 mixed generators: (3.0, 2.5) → (2.75, 2.75) for either sign).
- **(d) Per-expression weights open an alignment drive.** In Lie–Poisson form on so(3), uniform port weights conserve the overlap ⟨μ, P⟩ (Larmor precession), but per-channel weights do not (S4: 0 vs 0.72). The drive is Σ_{k<l} (w_k − w_l) p_k p_l ⟨μ, [E_k, E_l]⟩. It vanishes only for commuting generators, which reduce to the blocks of (a). The per-expression freedom the operator requires is exactly what lets the port align.

---

## Direction 2: a gauge-covariant dyadic ladder (closed)

### (1) The object
- **The ladder.** A two-row lattice over time, with sites (self, t) and (partner, t).
- **Local frames.** A local frame group G acts on each site independently: each person's expression coordinates may be re-chosen at every moment.
- **Links.** Own links U_s(t) and partner links U_p(t) run along time. Cross links V(t) are the agent's reading frame for the partner.
- **What the core may see.** By gauge invariance it sees the partner only through traced Wilson loops (Favoni et al.). The basic ones are the plaquettes F_t = U_s(t) V(t+1) U_p(t)⁻¹ V(t)⁻¹ and lag-d rectangles.

### (2) What it gives (derived)
- **Copy-in-a-frame is pure gauge.** If the partner moves as the agent does in any time-varying frame, every plaquette is trivial. So the core is blind to frame-copying for every parameter, and lag-d rectangles detect lag-d frame-copying.
- **Abelian case.** For per-channel scalings the plaquette is a signed area of the two paths: the Lévy-area input of commutator coupling.

### (3) Why it is closed
- **No dynamics from the symmetry.** By Noether's Theorem II and §6, the local symmetry gives identities and improper conservation laws. It adds no state, persistence or time scale.
- **Curvature comes from the cross links, which are a relative frame.**
  - Links built from each person's own data are pure gauge, Ω_x Ω†_{x+1}, so all their loops are trivial.
  - Only the cross links V(t) can carry curvature, and they are a relative self–partner frame. That is the relative-frame-transport design (held; recombination).
  - In the abelian case the plaquette reduces to commutator coupling (held; recombination).
- **Learned links drift to flatness.** Any learning that lowers a Wilson-action-like cost drives the links toward flatness, which is copy-in-a-frame. This matches Hansen & Ghrist's Theorem 8.1 (symmetry-no-copy-synthesis.md).
- **Relational equivariance invites copy.** Two-agent equivariance on the relation (EGNN; van der Pol et al.) makes the relation's zero (copy) the distinguished point.

### (4) Verdict
- Reduces to two held designs.
- Novelty: none beyond L-CNN applied to a two-row lattice.
- Kept: the statement "copy in any time-varying frame ⇔ a flat ladder connection", as a definition for critics.

---

## Direction 3: the relationship as the orbit of a pair. A doubly stochastic overlap between the agent's state and its own-body reading of the partner

### (1) The object
- **Two matrices on one footing.** The agent's own state M = UΛUᵀ (Direction 1), and its reading of the partner P̂ = VΓVᵀ in the same space, inferred by the agent's own inverse body model.
- **The relational state.** Invariants of the pair under simultaneous conjugation. The first of them is Q = (UᵀV) ∘ (UᵀV), an n × n unistochastic matrix (rows and columns sum to 1).
  - tr(M P̂) = λᵀ Q γ.
  - The maximum over the orbit is Σ λ_(i) γ_(i) in sorted order **(standard: von Neumann)**, reached at a sorted permutation.
  - Copy (P̂ = M) gives Q = I.
  - S7 checks double stochasticity, joint-conjugation invariance, the trace identity and the copy case.
- **Relationship memory.** A slow per-partner average of Q (and of the higher mixed traces, which Q does not exhaust).

### (2) What it gives
- **Structure over relationships, frame-free, of size n².**
  - "How the partner's modes sit relative to mine", with no gauge and no scalar.
  - It is invariant to how either person's expressive coordinates are chosen.
  - Its distance from the permutation matrices measures how far the two states are from frame-copy.
- **The two kinds of synchrony split cleanly** (Markova et al.).
  - Concurrent co-rotation (mirroring) leaves Q constant while both frames move.
  - A sequential response changes Q after the agent's own move.
  - This is a structural split, but telling responding from following still needs a lagged statistic: Watson's indices, or the agent's own variation as instrument.

### (3) Verdict and most likely failure
- **Verdict: recombination.** It is matrix analysis plus the relationship-as-invariant idea of math-objects-synthesis.md.
- **Most likely failure.** Any partner-port weight w_j learned from Q has the von Neumann maximiser available. Learning finds that tr(M P̂) rises as Q → sorted permutation, which is copy-in-frame: the Hansen–Ghrist drift again, here as gradient ascent on an overlap that the trace identity makes linear in Q. Using Q only as a sign- and context-key, with |w_j| ≤ c_j, brings back the per-channel ceilings.
- **Also:** Q keeps only squared overlaps, so the relative sign of modes needs the higher invariants.

---

## Overall verdict

- **No direction clears the bar** of a genuinely new core mechanism on the level of attention.
  - Direction 1 is the strongest. It has a precise object, four exact properties for every parameter and route (T1–T4), and a closure property earlier designs lacked. But it reduces per channel to Adler phase locking, and its per-channel protection against stable following is again an innate ceiling.
  - Direction 2 reduces to two held designs.
  - Direction 3 is a useful relational descriptor whose use as coupling reopens alignment.
- **The one idea worth keeping** is the Noether-sourced split: *the partner acts only as a symmetry motion, the body only as a source*. It gives an all-routes intensity budget and structural contingency gating. It could be offered to the build candidate as a structural safety net that counts no routes, in place of the ledger's route accounting, where the ledger's small-ceiling gap is open (Q35, D92). That would need an independent critique first, aimed at failure (a) and at whether a spectral source can be kept free of partner influence once b responds to the agent's own reactions.

## Next steps
1. **Independent critique of Direction 1** on four points:
   - T1–T4 step by step;
   - whether "partner-derived quantities only in X" is enforceable when the body b responds to the agent's own appraisal of the partner (an indirect route into S);
   - failure (a) on recorded dyads: the locked-following slope against the partner's range, measured on Seamless Interaction movement features under D70/D85;
   - the G-mirror test.
2. **Read, if the hosts open:** Brockett 1988 (double bracket), LPNets (Eldred et al.), Yang & Mills 1954, Rochat 2003, Koós & Gergely 2001, Nagy & Molnár 2004, Maister et al. 2020.
