# Precise mathematical objects for the dyadic core: synthesis

Written 2026-11-25 for Q17. It covers 12 notes on 15 primary sources. Each note says what was read and what was skipped. This is an argument from reading plus a few derivations, each marked as mine and checked numerically where stated. Nothing here is a design. The point is to say which existing objects could carry requirements (a)-(d) with a property that can be proved, and which provably reduce to the excluded mechanisms.

The requirements, from the brief and [mimicry-context-synthesis](mimicry-context-synthesis.md):
- (a) partner influence is per expression, can flip sign, and depends on learned partner history; it is not one gain from flat to copy;
- (b) "whose" is kept separate from "what";
- (c) time scales from reflex to temperament come from structure;
- (d) the other is read through the agent's own body.

Notes:
- **Position and time:**
  - [RoPE](su-2021-roformer-rope.md)
  - [ALiBi](press-2021-alibi.md)
- **Symmetry:**
  - [G-CNN](cohen-welling-2016-group-equivariant-cnn.md)
  - [Geometric Deep Learning](bronstein-2021-geometric-deep-learning.md)
  - [Clifford group networks and GATr](ruhe-2023-clifford-group-equivariant.md)
- **Sheaves:**
  - [Neural Sheaf Diffusion](bodnar-2022-neural-sheaf-diffusion.md)
  - [spectral theory of cellular sheaves](hansen-ghrist-2019-spectral-theory-cellular-sheaves.md)
  - [discourse sheaves](hansen-ghrist-2021-discourse-sheaves.md)
- **Energy:**
  - [Hamiltonian NNs](greydanus-2019-hamiltonian-nn.md)
  - [port-Hamiltonian NNs](desai-2021-neary-2023-port-hamiltonian-nn.md)
- **Opinion dynamics:**
  - [multidimensional Friedkin-Johnsen](parsegov-2017-multidimensional-friedkin-johnsen.md)
  - [Altafini signed consensus](altafini-2013-signed-consensus.md), from tutorials only; the 2013 original was not reachable.

## 1. The excluded mechanisms, stated as exact reductions

Every family read contains the excluded behaviour as a special case. The table gives the exact condition under which each one becomes copying, a scalar gain, or a mean face. Throughout, x_s is the agent's state, u the partner's observed state, and the dyad is two nodes joined by one edge unless stated otherwise.

| Object | Condition | Reduces to | Source of the statement |
|---|---|---|---|
| Sheaf diffusion ẋ = −L_F x | identity restriction maps (constant sheaf) | L_F = L_graph ⊗ I; consensus x_s = x_o = mean | Bodnar Prop. 20/29; Hansen-Ghrist Prop. 8.1 |
| Same, partner held fixed (stubborn) | A = B = I | x_s → u: exact copy | Hansen-Ghrist 2021 Thm 5.1; Prop. D1 in that note (mine) |
| Same | scalar maps A = aI, B = bI | x_s → (b/a)u: the flat-to-copy dial | Prop. D1 (mine) |
| Same | one-dimensional maps with the same sign on two nodes | harmonic vector constant: collapse | Bodnar Prop. 23 |
| Same | invertible orthogonal maps on a single edge (a tree) | path-independent transport, dim H⁰ = d; isomorphic to the constant sheaf after a change of frame: **copy in a frame** | Bodnar Lemma 6; Hansen-Ghrist 2019 §3.5 |
| Stacked sheaf convolutions | symmetric or same-signed maps, λ*‖W₁‖²‖W₂‖² < 1 | Dirichlet energy contracts exponentially to ker L_F (oversmoothing as a theorem) | Bodnar Thm 15/16 |
| Signed consensus (Altafini) | structurally balanced signs (some D = diag(±1) with DAD ≥ 0) | L[A] = D L[\|A\|] D: consensus in a sign-flipped frame, so counter-mimicry is copying −u | Altafini as reported by Proskurnikov-Tempo II and Shi-Altafini-Baras |
| Signed consensus | not balanced, strongly connected | x → 0: flat face | same |
| Signed edge potential (repulsion) | a negative edge that is a cutset (the dyad's only edge always is) | indefinite Laplacian: divergence | Hansen-Ghrist 2021 Prop. 12.1 |
| Friedkin-Johnsen W ⊗ C | C = cI, Λ = λI | T = t(c)I: one scalar gain | Parsegov note (dyad closed form, mine, checked) |
| Friedkin-Johnsen | Λ = I, C = I | DeGroot averaging: mean face | Parsegov et al. |
| Friedkin-Johnsen | C with D_C C D_C ≥ 0 | copy in a flipped frame | Parsegov note; their Example 5 is Example 4 conjugated by diag(1, −1) |
| Port-Hamiltonian interconnection | resistive coupling u_A = −k(y_A − y_B) | diffusion; outputs synchronise (LaSalle) | port-Hamiltonian note (mine) |
| Port-Hamiltonian, first-order case | J = 0, R = rI, G = I, u = kŷ_B | ė = −re + kŷ_B: a gain k/r | same |
| Attention over two tokens, any score-side position code | one head | αψ(x_B) + (1−α)ψ(x_A), α ∈ [0, 1]: a scalar gain on a fixed value map; the code changes only the non-negative weights | RoPE note; GDL note; Clifford note (GATr) |
| ALiBi, content-blind | one head, M = I | exponential moving average of the partner times a gain: a smoothed copy | ALiBi note (mine) |
| Swap-invariant (pooled over self ↔ other) | invariance instead of equivariance | A = B in [[A, B], [B, A]]: "whose" erased | G-CNN note (mine) |
| O(d)-equivariant algebra over expression space (Clifford) | expressions as vectors of V | every grade-1 output lies in span{x_A, x_B}: y = φ_A x_A + φ_B x_B, an invariant scalar gain on a copy of the whole face | Clifford note (mine) |
| Gauge coupling on one edge | irreducible structure group (O(d), SO(d) with d ≥ 3, GL(d), signed permutations) | Schur's lemma gives Θ = cI: a scalar gain | GDL note (mine) |
| Hamiltonian NN, closed dyad | J skew, no dissipation | no attracting equilibrium (Liouville): cannot copy, rest, or settle a mood | HNN note |

The table points to one structural fact. It is mine, assembled from the rows above. **On a single edge, any invertible coupling that is a group element is a change of frame. So it is copying in disguise, or it decays to flat.** Three separate results say the same thing:
- Lemma 6 of Bodnar: a tree has no holonomy.
- The Altafini gauge: on a dyad, balance is automatic. The signed graph's only cycle is the dyad's two-node loop, whose sign is a_12·a_21. That is positive whenever the coupling signs are symmetric, which the model requires.
- Schur's lemma in the gauge setting.

So a fixed sign or rotation per expression is not enough for (a). Something must break the frame equivalence. The candidates:
1. **Rank deficiency.** A private kernel that the partner cannot reach.
2. **Holonomy.** Several edges between self and other (per context, per lag, or through time), whose loop transport is not the identity.
3. **A sign or map that is a function of a slow relation state h.** Then no single frame change works across relation states.

## 2. Which objects can carry (a)-(d), and the theorem each would need

### (a) Per-expression, signed, history-dependent influence

**Carrier: the dyad discourse sheaf.** The construction is in the [discourse-sheaf note](hansen-ghrist-2021-discourse-sheaves.md):
- F(s) = the agent's private state, R^n.
- F(e) = the expression space, R^k.
- A = F_{s⊴e} is the agent's own state-to-face map. B = F_{o⊴e} maps the partner's observed state u into the same space.
- With the partner stubborn, the agent's dynamics are ẋ_s = −αAᵀ(A x_s − B u).
- The steady response is x_s* = A⁺B u + Π_{ker A} x_s(0). This is Hansen-Ghrist Theorem 5.1; the dyad form is mine and was checked numerically.
- A⁺B is any linear map of rank ≤ k. Off-diagonal and signed entries are allowed.
- The structural content beyond "a learned matrix" is the factorisation through the agent's own map A and the private kernel ker A.

The multidimensional Friedkin-Johnsen model (W ⊗ C plus an anchor) is the same in discrete time. Its closed form for the dyad shows the limits:
- the gain on each eigenmode μ of C has the sign of μ;
- a negative μ also makes the agent's own face alternate sign on that mode.

So "counter the partner" and "flip my own expression" cannot be separated while one C acts on both. The fix is separate self and partner maps, x_A(k+1) = λ_A(w_AA P_A x_A + w_AB Q_A x_B) + (1−λ_A)u_A, as the Parsegov note derives.

**Where the sign must live.** The port-Hamiltonian note proves a static-gain lemma (mine). For a passive agent with R ≻ 0, the steady input-output map S = Gᵀ(R − J)⁻¹G has a positive-semidefinite symmetric part, so S_ii ≥ 0. **A passive body cannot counter-mimic on the same channel through its own dynamics.** A same-channel sign flip, such as smiling at anger under power or brow relaxation at a rival's distress, must come from the coupling: the restriction map B(h), or the port matrix K(h). It cannot come from the agent's internal dynamics.

**Definition: dial rank (mine).** Let T(h) be the steady partner-to-self transfer under relation state h; in the sheaf, T(h) = A(h)⁺B(h). The dial rank is the dimension of span{T(h) : h ∈ H}.
- A "single gain from flat to copy" is exactly dial rank 1 with T(h) = c(h)·I.
- "Copy in a frame" is T(h) = c(h)·D, with D fixed.
- The mimicry data need dial rank ≥ 2, because rows move in different directions:
  - Bourgeois & Hess: smile return flat while sadness return switches.
  - Hofman: anger return up while smile return stays.
- They also need some T(h) whose lifted sign pattern is not balanced by any fixed D. That is the Altafini test, applied across h.

**Theorem the design would need (a).** For the learned family {A(h), B(h)}:
- (i) dial rank ≥ 2, and T(h) is not of the form c(h)·D|T₀|D′;
- (ii) the copy map I lies in the closure of {T(h)} only on a declared subspace: the robust smile-to-smile core;
- (iii) the agent stays stable while h switches. Because the sheaf term is −∇ of ½‖A(h)x − B(h)u‖², a common Lyapunov function is available when A(h) changes slowly. With the port-Hamiltonian body added, H + ½‖A x − B u‖² is the candidate. This is not proved; it needs a dwell-time or slow-variation argument;
- (iv) the learning rule for h is not ‖δx‖² descent. Hansen-Ghrist Theorem 8.1 proves that such descent converges to the Frobenius-nearest map under which the pair looks like agreement. They call it "learning to lie"; for a face it is a sycophantic display.

### (b) "Whose" separate from "what"

**Carriers:**
- **The sheaf's vertex/edge split.** "Whose" is the vertex (separate stalks F(s) and F(o), possibly of different dimension). "What" is the edge stalk, the expression space where the two meet. Agreement A x_s = B x_o is agreement of display, not identity of state.
- **Friedkin-Johnsen's Kronecker form W ⊗ C.** This is the same split in its simplest form: W over agents, C over expressions. Its weakness is that it is a tensor product: the same C for both agents and for self and other. That is why it collapses to a scalar when C = cI.
- **Swap-equivariance (G-CNN note).** The general swap-equivariant linear core is [[A, B], [B, A]]. B is unrestricted: per expression, off-diagonal, signed. "Whose" is a coordinate the group permutes, and "what" is a channel it never mixes. Every asymmetry is moved into a relation state h with h ≠ σh. Invariance (pooling over the swap) gives A = B and destroys (b); the paper's "premature invariance" result is the empirical analogue.

**Rejected carrier.** Clifford O(2) over directions e_s and e_o makes self and other interchangeable by a group element. Once a fixed reference e_s is fed in to break this, linear partner-to-self terms are forbidden. "Whose" as a geometric direction is the wrong encoding. The Löwe complex-autoencoder note's "orientation = whose" has the same weakness if made rotation-equivariant.

**Theorem the design would need (b).**
- Swap-equivariance of the core with an explicitly asymmetric h.
- A proof that, for h ≠ σh, the agent's state and the partner model do not converge to the diagonal. Equivalently, H⁰ meets the diagonal only on the declared subspace from (a)(ii).

### (c) Time scales from structure

Four structural sources of rate appear in the reading. Each covers part of the range.

1. **Fixed frequency or recency banks.**
   - RoPE's θ_i = 10000^(−2(i−1)/d) and ALiBi's slopes 2^(−8h/n) are fixed geometric banks.
   - At 30 Hz, eight ALiBi heads span about 0.067-8.5 s (ALiBi note).
   - RoPE's relative-position property is exact: the score depends only on n − m because m ↦ R_m is a homomorphism Z → SO(d).
   - The RoPE note proves (mine) that, if position acts linearly on content and queries and keys share the operator, RoPE is unique up to the choice of frequencies.
   - These banks reach seconds, not days. The paper's long-term-decay claim rests on a plotted bound that is non-monotone: it rises at 988 of 2000 steps (RoPE note).
2. **Laplacian spectra.**
   - Sheaf diffusion relaxes mode i at rate αλ_i(L_F) (Hansen-Ghrist Prop. 8.1).
   - A product sheaf over (dyad) × (scale graph) has spectrum {μ_i + λ_j} (their Prop. 5.15).
   - Per-expression restriction maps therefore give per-expression rates with no time-constant parameter.
   - The cost is that rate is tied to coupling strength (λ grows with ‖A‖²). That makes a testable prediction, possibly contradicted by Carr 2014's slow context-carrying smile.
3. **Dissipation structure.**
   - In a port-Hamiltonian body every decay rate lies in [λ_min(R′), λ_max(R′)], with R′ = Q^{1/2}RQ^{1/2}. J cannot create rates outside R's spectrum.
   - But J can create a slow mode: J = [[0, ω], [−ω, 0]] with R = diag(r, 0) gives τ_slow ≈ r/ω². For r = 30 s⁻¹ and ω = 0.03 s⁻¹ this is about 9 h.
   - A fast reflex channel gyrator-coupled to an undamped store thus yields a temperament-scale mode by structure (port-Hamiltonian note, mine).
4. **Invariants: zero rate, set by structure.**
   - The private kernel ker A is exactly invariant under all partner input (Prop. D1).
   - The discourse-sheaf joint flow (state ẋ_s = −αAᵀr and learned map Ȧ = −βr x_sᵀ, with r = A x_s − B u) conserves Q = αAᵀA − βx_s x_sᵀ **for any partner signal u(t)**. Derivation mine; it is the self-vertex block of Hansen-Ghrist's Theorem 9.3. Numerical check: drift 3.4×10⁻⁶ against entries of order 1.7.
   - A negative eigenvalue −q of Q, with eigenvector w, gives a floor |wᵀx_s(t)| ≥ √(q/β) for all t. The agent cannot be flattened in that direction by anything the partner does.
   - Two limits: the floor is at most one-dimensional, and AᵀA is slaved to x_s. So this flow cannot also store a slow relation memory.

Block-diagonal dissipation with eigenvalues across decades is itself a scalar-per-mode design (time constants by hand). So I read option 4 as the only "temperament from structure" in the strict sense: a quantity the partner provably cannot change. Options 2 and 3 give the middle range from the coupling structure itself.

**Theorem the design would need (c).**
- A statement that the linearised core's spectrum has (i) modes below 1 s on the matching channels, (ii) modes at 2-4 s on the context channels (the Carr and Weyers timing), and (iii) a partner-unreachable invariant or near-invariant subspace, by construction rather than by fitted constants.
- The invariant Q must be rechecked once the body dynamics (J − R)∇H are added. Q is not conserved in general then. A design must say which conserved quantity survives.

### (d) Reading the other through one's own body

Three objects give the same precise statement. **The partner can enter only through the adjoint of the agent's own output map.**
- **Sheaf** (discourse-sheaf note, Prop. D2, mine): ẋ_s depends on u only through AᵀBu. Any component of the partner's expression in ker Aᵀ = (im A)^⊥ has no effect at any time. An expression my body cannot produce is invisible to me.
- **Port-Hamiltonian:** collocated ports, input through G and output y = Gᵀ∇H, are what make power balance dH/dt ≤ yᵀu hold. The partner's power enters on the same channels through which the agent expresses.
- **Swap-equivariance** (G-CNN note): ∂F_other/∂x_self(x, h) = ∂F_self/∂x_other(Px, σh). The agent's model of how it moves the partner is its own response function with roles swapped. Simulation-by-self is an identity, not a learned option.

The port-Hamiltonian note also gives a bounded-influence theorem (mine). With H_A ≥ 0, R_A ⪰ δGGᵀ and ‖K‖ ≤ κ:
- ∫|y_A|² ≤ (κ/δ)²∫|ŷ_B|² + (2/δ)H_A(0);
- H_A(t) ≤ H_A(0) + (κ²/4δ)∫|ŷ_B|².

The partner can move the agent's body energy only by the power its port supplies. This bounds how much, not in which direction. It does not exclude copying.

The Clifford versor transport is a literal (d) for head pose and gaze: transport the partner's pose into the agent's body frame. It is silent on how expressions couple.

**Theorem the design would need (d):**
- im(partner influence) ⊆ im Aᵀ (structural);
- a bounded-influence inequality (energy);
- the swap identity (symmetry).

The first two are proved above for the linear sheaf term and the passive body. Whether they survive a learned nonlinear A(h) is open.

## 3. Which objects to carry forward

| Object | Carries | Proved property worth keeping | Reduces to the excluded mechanism when | Verdict in note |
|---|---|---|---|---|
| Discourse sheaf on the dyad | (a), (b), (d) | harmonic extension A⁺Bu; private kernel invariant; im Aᵀ bound; conserved Q (no-flat floor) | A = B = I (copy); scalar maps (gain); orthogonal single edge (copy in frame); learning by discord descent (display agreement) | adopt |
| Sheaf spectral theory | (c) and analysis | Hodge, consensus, harmonic extension, product spectra, interlacing | constant sheaf | adopt |
| Neural sheaf diffusion | collapse as a theorem | energy contraction for symmetric maps; escape outside H_sym; holonomy bounds on dim H⁰ | symmetric or same-signed maps | adopt (frame) |
| Port-Hamiltonian body | (d), (c), stability | power balance; interconnection passivity; static gain S_ii ≥ 0; bounded influence; gyrator slow mode | resistive coupling (diffusion); first-order scalar case | adopt (scaffold) |
| Swap-equivariance (G-CNN) | (b), (d) | [[A, B], [B, A]]; reciprocity identity | invariance (A = B); h = σh admits consensus | adopt (constraint) |
| Multidimensional FJ | (a) baseline, reduction test | Kronecker stability ρ(ΛW)ρ(C) < 1; closed form | C = cI; Λ = I, C = I; balanced C | adopt (baseline) |
| Altafini gauge | test for (a) | balanced iff gauge to non-negative | balanced = copy in frame; unbalanced = flat | adopt (lemma) |
| RoPE | time encoding | exact relative position; uniqueness under the linear-shared assumption (mine) | as a source of (a): score side only | adopt for time |
| ALiBi | fast end of (c) | bounded horizon per head (mine) | content-blind = EMA copy | watch |
| GDL blueprint | language; time warping | equivariance composes; gauge convolution | swap symmetry gives consensus; irreducible gauge gives cI | watch |
| Clifford / GATr | pose and gaze only | grade-preserving equivariant polynomials | O(d) over expressions gives a scalar gain on a copy | reject as core |
| Hamiltonian NN | none alone | dH/dt = 0 | closed: no attractors at all | reject as core |

The objects that survive in combination: a **port-Hamiltonian body whose coupling to the partner is a sheaf term with relation-dependent restriction maps**,

  ẋ_s = (J − R)∇H(x_s) − Aᵀ(h)(A(h)x_s − B(h)u),  with h a slow relation state.

Within it:
- the swap-equivariant form constrains how h enters;
- dial rank ≥ 2 is the formal "not a dial" requirement;
- the Altafini test across h is the formal "not copy in a frame" requirement;
- ker A and the Q-type invariant are the candidates for temperament.

This is a direction, not a design: requirements (a)(iii), (a)(iv) and the survival of Q are unproved. By the parts test of [new-mechanisms-synthesis](new-mechanisms-synthesis.md) it is also a recombination. Its candidate second-clause novelty is a derived invariant that removes the free scalar: dial rank ≥ 2 replaces the gain, and Q replaces a hand-set temperament constant.

## 4. What remains open or unread

- Altafini 2013 and the original Friedkin-Johnsen papers were not read; their claims come via tutorials.
- The NSD proofs for O(d) separation (Lemma 25 onward) were not read.
- The appendices of Bronstein's chapters 4.2-4.4, 4.6, 6 and 7 were not read.
- The GATr appendices were not read.
- No source read handles **switched or slowly varying restriction maps with a stability proof**. That is the missing theorem for history-dependent sign changes. Dwell-time and common-Lyapunov results from switched-systems theory are the next reading.
- Sheaves with **cycles through time**: a dyad sheaf on (two agents) × (lag graph), whose holonomy could give provable no-copy margins (Bodnar Prop. 5). This is untested here.
- Everything above is linear or near-linear in the coupling. Whether dial rank and the private-kernel invariant survive a learned nonlinear A(h, x) is the first question for a design.
