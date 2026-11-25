# Bronstein, Bruna, Cohen & Veličković 2021: Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges

## Citation

M. M. Bronstein, J. Bruna, T. Cohen, P. Veličković. "Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges." arXiv preprint (proto-book), 2021. arXiv 2104.13478, version v2 (2 May 2021).

## What was read

Read from the arXiv PDF, via `pdftotext -layout`. The margin notes are interleaved with the body text in the extraction; I read them where they carried definitions.

- **Read in full:** Preface; Notation; 1 Introduction; 2 Learning in High Dimensions (2.1, 2.2); all of 3 Geometric Priors (3.1 symmetries, representations, invariance; 3.2 isomorphisms and automorphisms; 3.3 deformation stability; 3.4 scale separation; 3.5 the blueprint); 4.1 Graphs and Sets; 4.5 Gauges and Bundles; 5.3 Graph Neural Networks; 5.4 Deep Sets, Transformers, and Latent Graph Inference; 5.7 Recurrent Neural Networks; and the time-warping part of 5.8 (LSTMs), up to the gate-bias remark.
- **Skimmed (first page only):** 5.2 Group-equivariant CNNs and 5.5 Equivariant Message Passing.
- **Not read:** 4.2 Grids, 4.3 Groups and homogeneous spaces, 4.4 Geodesics and manifolds, 4.6 Meshes, 5.1 CNNs, 5.6 Intrinsic mesh CNNs, the LSTM equations in 5.8, 6 Problems and Applications, and 7 Historic Perspective.
- This text has no proof appendix. Several stability results are cited, not proved: the wavelet stability bound (Mallat 2012), the universality of Deep Sets (Zaheer et al. 2017) and the 15 linear graph equivariants (Maron et al. 2018). I report them as cited.

## The object, exactly

**Domain and signals (3, eq. 1-3).**
- Ω is a set, the domain, with points u ∈ Ω. C is a vector space of channels.
- The signal space X(Ω, C) = {x : Ω → C} is a vector space under pointwise addition. With an inner product on C and a measure μ on Ω, it is a Hilbert space with ⟨x, y⟩ = ∫_Ω ⟨x(u), y(u)⟩_C dμ(u).
- A group G acts on Ω by (g, u) ↦ g.u, with g.(h.u) = (gh).u.
- This induces a linear action on signals, (g.x)(u) = x(g⁻¹u).
- A representation is a map ρ : G → R^{n×n} with ρ(gh) = ρ(g)ρ(h).

**Invariance and equivariance (3.1).**
- f : X(Ω) → Y is G-invariant if f(ρ(g)x) = f(x) for all g, x.
- F : X(Ω) → X(Ω') is G-equivariant if F(ρ(g)x) = ρ'(g)F(x).

**Deformation stability (3.3, eq. 4).**
- Let c(τ) be a cost on τ ∈ Diff(Ω) with c(τ) = 0 for τ ∈ G.
- f is geometrically stable if ‖f(ρ(τ)x) − f(x)‖ ≤ C c(τ) ‖x‖ for all x.
- Domain version (eq. 5): ‖f(x, Ω) − f(x̃, Ω̃)‖ ≤ C ‖x‖ d_D(Ω, Ω̃).

**Scale separation (3.4).**
- A coarsening hierarchy Ω_1, ..., Ω_J has signal spaces X_j(Ω_j, C_j).
- f is "locally stable at scale j" if f ≈ f_j ∘ P_j, where P_j : X(Ω) → X_j(Ω_j) is a nonlinear coarse-graining and f_j : X_j(Ω_j) → Y.
- The paper says "we informally say"; this is not a theorem.

**Blueprint (3.5).** The building blocks are:
- a linear G-equivariant B : X(Ω, C) → X(Ω', C');
- a pointwise nonlinearity σ, with (σ(x))(u) = σ(x(u));
- a local pooling P : X(Ω, C) → X(Ω', C) with Ω' ⊆ Ω (a coarsening);
- a G-invariant global pooling A : X(Ω, C) → Y.

The model is f = A ∘ σ_J ∘ B_J ∘ P_{J−1} ∘ ... ∘ P_1 ∘ σ_1 ∘ B_1. Different blocks may use different groups. B is "localised" if (Bx)(u) depends only on x(v) for v ∈ N_u = {v : d(u, v) ≤ r}.

**Sets and graphs (4.1, eq. 6-13).**
- X ∈ R^{n×d} holds the node features as rows. A ∈ {0,1}^{n×n} is the adjacency matrix. G = Σ_n acts by X ↦ PX and A ↦ PAPᵀ.
- f is invariant if f(PX, PAPᵀ) = f(X, A). F is equivariant if F(PX, PAPᵀ) = PF(X, A).
- **Linear equivariants on a set** are spanned by two generators: the identity F_1 X = X and the mean F_2 X = (1/n) 11ᵀ X. With channels this becomes F(X) = XΘ_1 + (1/n)11ᵀXΘ_2 (the multichannel form is my extension of the paper's sentence).
- Graph layers are F(X, A)_u = φ(x_u, X_{N_u}), where X_{N_u} = {{x_v : v ∈ N_u}} is a multiset and φ is permutation-invariant in its second argument.

**Three GNN flavours (5.3, eq. 33-35).** In each, ⊕ is a permutation-invariant aggregator (sum, mean or max):
- convolutional: h_u = φ(x_u, ⊕_v c_uv ψ(x_v));
- attentional: h_u = φ(x_u, ⊕_v a(x_u, x_v) ψ(x_v));
- message passing: h_u = φ(x_u, ⊕_v ψ(x_u, x_v)).

Containment: convolution ⊆ attention ⊆ message passing. A Transformer is the attentional flavour on the complete graph A = 11ᵀ, with positional encodings breaking Σ_n (5.4).

**Gauges (4.5).**
- A vector bundle has base Ω and fibre V at each u. A gauge is a frame ω_u : R^s → T_uΩ (or onto the fibre).
- A gauge transformation is a map g : Ω → G, with G the structure group (for example GL(s), O(s), SO(s), or Σ_3 on RGB channels). It acts by ω'_u = ω_u ∘ g_u, and the coordinates change as x'(u) = g_u⁻¹ x(u). The geometric object ω_u(x(u)) is unchanged.
- A pointwise map f : R^{d_in} → R^{d_out} is gauge-equivariant if f ∘ ρ_in(g) = ρ_out(g) ∘ f for all g ∈ G.
- Gauge-equivariant convolution (eq. 23): (x ⋆ Θ)(u) = ∫ Θ(u, v) ρ(g_{v→u}) x(v) dv. Here g_{v→u} ∈ G is parallel transport along the (locally unique) geodesic from v to u. The condition is Θ(u, v)ρ(g) = ρ(g)Θ(u, v) for g ∈ G.

**Time (5.7-5.8).**
- Input frames z^(t) feed a recurrence h^(t) = R(z^(t), h^(t−1)).
- A time warp is τ : R+ → R+, monotone increasing and differentiable, "an automorphism of time".
- A model class is "invariant to time warping" if for every model and every τ some model in the class processes the warped input as the original model processed the unwarped input. This is invariance of the class, not of one function.

## The key property and its proof, step by step

The paper does not state numbered theorems. I extract four results that are proved, or argued, in the text read.

**P1. Linear invariants collapse to the group average (3.5).**
- Hypotheses: f is linear and G-invariant, and G is compact with Haar measure μ.
- Claim: f(x) = f(A x), where A x = (1/μ(G)) ∫_G g.x dμ(g).

Steps:
1. Invariance gives f(x) = f(g.x) for every g. Average over G: f(x) = (1/μ(G)) ∫ f(g.x) dμ(g).
2. Linearity moves f outside the integral: f(x) = f((1/μ(G)) ∫ g.x dμ(g)).
3. So f depends on x only through its orbit average. For images under translation, this is the mean colour.

This is complete and checkable. It is the paper's argument for nonlinearity.

**P2. Equivariant layers compose, and invariant pooling makes the result invariant (3.5, "blueprint").**
- Hypotheses: B satisfies B(g.x) = g.B(x); σ acts pointwise; P commutes with the group action on the coarser domain; A satisfies A(g.x) = A(x).
- Claims: U = σ ∘ B is G-equivariant, and A ∘ U_J ∘ ... ∘ U_1 is G-invariant.

Steps:
1. (σ(g.y))(u) = σ(y(g⁻¹u)) = (g.σ(y))(u). The action only moves points of Ω and σ acts on values, so pointwise σ commutes with the action.
2. U(g.x) = σ(B(g.x)) = σ(g.B(x)) = g.σ(B(x)).
3. A composition of equivariant maps is equivariant, by induction on depth.
4. A(g.U(x)) = A(U(x)), so the whole pipeline is invariant.

Where it is loose:
- Step 1 holds only when σ acts on channels that the group does not mix. For a gauge group acting on the fibre, a pointwise ReLU is not equivariant. The paper does not flag this in 3.5.
- For a pooling P onto a coarser Ω', equivariance needs G to act compatibly on Ω' (for example, translations by multiples of the stride). The blueprint lets "different blocks exploit different choices of symmetry groups" but does not state the compatibility condition.
- Universality: "It is not hard to adapt the standard Universal Approximation Theorems ... to show that shallow 'geometric' networks are also universal". This is asserted, with Zaheer et al. 2017 cited for Deep Sets. It is not proved here.

**P3. Permutation equivariance of local message passing (4.1, eq. 13; 5.3).**
- Hypothesis: φ(x_u, X_{N_u}) is invariant to the order of the multiset X_{N_u}.
- Claim: F(PX, PAPᵀ) = PF(X, A).

Steps:
1. Under P, node u becomes node π(u). Its neighbourhood becomes π(N_u), and the multiset of neighbour features is the same.
2. φ gives the same output at π(u) as it gave at u.
3. Stacking the rows gives the output permuted by P.

Sketched in the text, and correct.

**P4. Time-warp invariance of the class forces gating (5.8, following Tallec & Ollivier 2018, as the paper states).** This is a derivation, not a proof.
1. Read the recurrence as an Euler step of the ODE dh/dt = R(z(t+1), h(t)) − h(t) (eq. 50).
2. Under a warp τ, the chain rule gives dh(τ(t))/dt = τ'(t) [R(z(τ(t+1)), h(τ(t))) − h(τ(t))] (eq. 52).
3. Discretise with step 1 and replace τ'(t) by a learned Γ(z^(t+1), h^(t)). This gives h^(t+1) = Γ R(z^(t+1), h^(t)) + (1 − Γ) h^(t) (eq. 53).
4. τ' > 0, and the Taylor step needs τ' ≲ 1, which gives 0 < Γ < 1: a logistic gate.
5. A SimpleRNN is the special case Γ ≡ 1, so its class is not warp-invariant.
6. Vector gates fit "a different warping derivative in every dimension ... reasoning over multiple time horizons simultaneously".
7. The characteristic forgetting time is ∝ 1/Γ ("it can be shown", not shown).
8. E[Γ] ≈ logistic(b_Γ) for zero-centred inputs, so the gate bias sets the time scale.

Where it is loose:
- Steps 1-3 are first-order Taylor heuristics.
- "Class invariance" does not give zero-shot transfer. The paper says a model trained on τ_1 "cannot zero-shot transfer" to τ_2, except when τ_2 = ατ_1 (rescale Γ by α).

**P5. Gauge-equivariant convolution (4.5, eq. 23).**
- Hypotheses: there is a transport g_{v→u} that transforms under a gauge change as g_u⁻¹ g_{v→u} g_v (the text writes it as g_u⁻¹ g_{u→v} g_v), and the filter commutes with ρ(G).
- Claim: (x' ⋆ Θ)(u) = ρ⁻¹(g_u)(x ⋆ Θ)(u).

Steps (with the consistent convention x'(v) = ρ(g_v)⁻¹ x(v)):
1. Θ ρ(g_u⁻¹ g_{v→u} g_v) ρ(g_v)⁻¹ x(v) = Θ ρ(g_u)⁻¹ ρ(g_{v→u}) x(v).
2. Commutation moves ρ(g_u)⁻¹ to the left of Θ.
3. Integrate over v.

Where it is loose:
- The text says the field transforms as "x(v) ↦ ρ(g_v)x(v)". That is inconsistent with its earlier x' = g⁻¹x and with its stated result; the inverse is needed.
- The paper shows why a filter without transport is impossible. The condition Θ(u, v) = ρ⁻¹(g(u)) Θ(u, v) ρ(g(v)) for independent g(u), g(v) forces Θ = 0 ("Indeed Θ would have to be zero in this case").

## What it would mean for a dyadic affective core (my inference)

**The domain.**
- The natural domain is Ω = {A, B} × T: agent and partner, crossed with time frames at 30 Hz.
- The channel space C = R^{d_AU} (face) holds per-expression channels, plus voice and body channels.

Three candidate symmetry groups behave very differently.

1. **Agent swap Σ_2 on {A, B} must be excluded, and the blueprint shows why.** By 4.1, a Σ_2-equivariant linear layer is h_u = Θ_1ᵀ x_u + Θ_2ᵀ (x_A + x_B)/2.
   - Θ_2 can be a full signed d×d matrix. So per-expression, off-diagonal, sign-flipping coupling is allowed, but only symmetrically: A reads B by the same matrix that B reads A.
   - Iterate this layer linearly:
     - the difference d = x_A − x_B evolves by Θ_1ᵀ alone;
     - the mean evolves by (Θ_1 + Θ_2)ᵀ.
   - If the spectral radius of Θ_1 is below 1, d → 0. That is **diffusion to consensus**, the excluded mechanism.
   - The invariant readout A (sum or mean over agents) is literally the dyad average.
   - Σ_2 equivariance is also exactly the statement that "whose" carries no information, which contradicts (b).
   - Conclusion: the agent index must not be a symmetry. Self and other are distinct nodes of a 2-node graph with no permutation symmetry, so the GDL machinery for graphs gives nothing on this axis.
2. **Time translation on T is a legitimate symmetry** (stationarity). It gives convolution or recurrence over time. The time-warp argument (P4) is the most useful thing in the text for (c), but it delivers time scales as learned gate values (1/Γ, set by b_Γ). It does not derive them from structure.
3. **Bilateral facial mirror Z_2 on channels.** This swaps left and right action units and is the one real symmetry of the expression space. It is also a natural gauge for (d): when two people face each other, B's left appears on A's right. The transport across the A-B edge is then an element of Z_2 (anatomical versus specular reading). The commutant of the L/R swap on a (left, right) pair is {[[a, b], [b, a]]}, so symmetric and antisymmetric parts couple separately. The constraint is mild.

**(c) Scale separation as structure.**
- Coarsen T dyadically: level j pools 2^j frames, about 2^j/30 s:
  - j = 0 is 33 ms;
  - j = 5 is about 1 s;
  - j = 11 is about 68 s;
  - j = 17 is about 73 min;
  - j = 22 is about 39 h;
  - j = 26 is about 26 days.
- Twenty-six levels span reflex to temperament, with the time scales fixed by the hierarchy rather than learned.
- What GDL actually supplies here is only the factorisation f ≈ f_j ∘ P_j, stated informally, with no theorem on why the coarse levels should hold dispositions.
- Two cautions:
  - **Pooling is averaging.** It must act on T only. Pooling across the agent index is the consensus operator again.
  - **The blueprint's pooling is non-causal and stateless.** An online agent needs a causal multi-rate state (level j updates every 2^j frames). That is a design addition, not something in the paper.

**(d) Gauge reading of "the other through my body".**
- Model each agent's latent body space as a fibre with structure group G. Partner influence is then h_A = Θ_AA x_A + Θ_AB ρ(g_{B→A}) x_B, which is eq. 23 on a 2-node graph.
- The gauge condition says Θ_AB must commute with ρ(G). This produces a precise trilemma.
  - **G irreducible: the coupling is one scalar.** If G acts absolutely irreducibly on the fibre (G = O(d), SO(d) for d ≥ 3, GL(d), or signed permutations), Schur's lemma forces Θ_AB = c·I. The partner term becomes c · ρ(g_{B→A}) x_B: one scalar gain on a transported copy.
  - **On one edge, the transport can be absorbed.** The 2-node graph has a single edge and no cycle, so the transport is pure gauge: choose g_B = g_{B→A}⁻¹ g_A to make it the identity. The only gauge-invariant coupling parameter is then c. **This is exactly the excluded scalar gain from flat (c = 0) to copy (c = 1)**, with countering (c < 0) as anti-copy.
  - **Group-valued transport is invertible.** Even when the transport is meaningful (fixed frames, learned g), any group element is invertible. It can flip signs and map smile to anger (a signed permutation or rotation), but it cannot switch off one expression while passing another. Per-expression gating, which the mimicry data require, needs singular maps.
  - **G diagonal: per-expression gains, no cross-talk.** If G = (Z_2)^d (independent sign per channel), the commutant is all diagonal matrices. Θ_AB = diag(c_i) gives per-expression gains with signs but no off-diagonal coupling (no smile to anger).
  - **G trivial: no constraint at all.** Θ_AB is any matrix, and gauge language adds nothing beyond the "learned partner-conditioned linear map" already in mimicry-context-synthesis.md.
- Holonomy offers a way out. Gauge-invariant content on a graph lives in cycles. In a dyad over time, the loop A_t → B_t → B_{t+1} → A_{t+1} → A_t has a holonomy, the product of transports around it. That is a frame-independent quantity, and it could measure whether the partner's response to me matches my reading of them (contingency). This is speculative; the paper says nothing about time-indexed loops.

**Reductions, stated precisely.**
- Σ_2 on agents with linear layers: consensus when ρ(Θ_1) < 1, and the invariant readout is the mean.
- Gauge coupling with an irreducible structure group on a single edge: a scalar gain c on a transported copy.
- Attentional GNN layers (5.3) with softmax weights on two nodes: h_A is a convex mix α ψ(x_B) + (1 − α) ψ(x_A), with α ∈ [0, 1] the scalar "flat to copy" gain.

**Theorem the design would need.** Write the partner term as M(m) x_B, where m is the partner-history state. Then:
- (i) the set {M(m)} spans a space of dimension > 1 that includes matrices with off-diagonal and negative entries and singular matrices (so no single scalar c reproduces it);
- (ii) the difference x_A − x_B is not contracted to 0 by the closed-loop dyad dynamics for generic histories (no consensus);
- (iii) the time constants of m are fixed by a causal multiscale hierarchy (2^j frames) rather than by free gate biases.

GDL supplies the vocabulary to state (i)-(iii). It supplies no mechanism that satisfies them. Its symmetry constraints, applied to the agent axis or to a full fibre group, push toward the excluded mechanisms.

## Verdict

watch. GDL gives exact language (domain, group, equivariant layer, coarsening, gauge with transport) and two useful negative results for the dyad: agent-swap symmetry yields consensus, and gauge coupling with an irreducible structure group on one edge yields a scalar gain. Its scale-separation prior and time-warp gating give a structural route to reflex-to-temperament time scales only if built as an explicit causal multi-rate hierarchy, which the text does not do.
