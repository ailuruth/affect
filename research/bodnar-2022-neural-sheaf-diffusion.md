# Bodnar, Di Giovanni, Chamberlain, Liò & Bronstein 2022: Neural Sheaf Diffusion

## Citation

C. Bodnar, F. Di Giovanni, B. P. Chamberlain, P. Liò, M. M. Bronstein. "Neural Sheaf Diffusion: A Topological Perspective on Heterophily and Oversmoothing in GNNs." *NeurIPS* 2022. arXiv 2202.04579 (v4, 6 Jan 2023). Code: github.com/twitter-research/neural-sheaf-diffusion.

## What was read

arXiv PDF, text extraction.
- Read in full: abstract, sections 1-5 and 7, Appendix A (harmonic-space proofs: Propositions 3, 4, 5, Lemma 6), Appendix B up to Proposition 12 (Proposition 20, Lemma 21 as stated, Propositions 8, 9, 10, 23, 11, 12), Appendix C (Propositions 29, 17, 30; Lemmas 31, 32, 33; Corollaries 36-37), Appendix D (Proposition 18).
- Skimmed: section 6 and Table 1 (results), the end of the Lemma 33 proof.
- Not read: Appendix B from Lemma 25 on (the O(d) constructions behind Proposition 13), the main proof of Theorem 15 (only its lemmas), Appendices E and F.

## The object, exactly

**Cellular sheaf on a graph (Definition 1).** G = (V, E) undirected. For each v ∈ V a vector space F(v) (vertex stalk); for each e ∈ E a vector space F(e) (edge stalk); for each incident pair v ⊴ e a linear map F_{v⊴e}: F(v) → F(e) (restriction map). In the paper all stalks are R^d.
- 0-cochains: C⁰(G; F) = ⊕_v F(v), a block vector x ∈ R^{nd}.
- Global sections: H⁰(G; F) = { x ∈ C⁰ : F_{v⊴e} x_v = F_{u⊴e} x_u for every edge e = (v, u) }.
- Sheaf Laplacian (Definition 2): L_F(x)_v = Σ_{v,u⊴e} F_{v⊴e}ᵀ (F_{v⊴e} x_v − F_{u⊴e} x_u). Diagonal blocks L_vv = Σ_e F_{v⊴e}ᵀF_{v⊴e}, off-diagonal blocks L_vu = −F_{v⊴e}ᵀF_{u⊴e}. Positive semidefinite. Normalised Δ_F = D^{-1/2} L_F D^{-1/2}, D its block diagonal.
- ker L_F ≅ H⁰(G; F) (harmonic cochains = global sections).
- Trivial sheaf: d = 1, all restriction maps the identity on R. Then L_F is the ordinary graph Laplacian, Δ_F the normalised graph Laplacian Δ₀.
- Discrete O(d) bundle: all F_{v⊴e} ∈ O(d). Transport along a path γ = (v, v₁, …, u): P_γ = (F_{u⊴e}ᵀ F_{vℓ⊴e}) ⋯ (F_{v₁⊴e}ᵀ F_{v⊴e}): F(v) → F(u). It may depend on the path (holonomy).

**Sheaf diffusion (Eq. 3).** Ẋ(t) = −Δ_F X(t), X ∈ R^{nd×f}. Euler step: X(t+1) = (I − Δ_F) X(t).

**Sheaf convolution (Eq. 4, after Hansen & Gebhart).** Y = σ((I_nd − Δ_F)(I_n ⊗ W₁) X W₂), with W₁ ∈ R^{d×d} acting inside each stalk and W₂ ∈ R^{f₁×f₂} across channels. With the trivial sheaf, W₁ is a scalar and this is a GCN.

**Neural Sheaf Diffusion (Eqs. 5-6).** X_{t+1} = X_t − σ(Δ_{F(t)} (I ⊗ W₁ᵗ) X_t W₂ᵗ). The restriction maps are produced by a learned function of the two endpoint features: F_{v⊴e=(v,u)} = Φ(x_v, x_u) = σ(V[x_v ‖ x_u]), reshaped to d×d. Φ must be non-symmetric in its arguments to produce asymmetric maps. Three families: diagonal, orthogonal (Householder products), general.

## The key properties and their proofs

### 1. Diffusion ends in the projection onto the global sections (Lemma 21, stated without proof; proved in Hansen & Ghrist, see the discourse-sheaf note)

X(t) → orthogonal projection of X(0) onto ker Δ_F. Everything about the infinite-time limit therefore depends only on ker Δ_F. Oversmoothing is the case where ker Δ_F is too small to separate classes.

### 2. The trivial or symmetric sheaf is ordinary graph diffusion (Proposition 20, Proposition 29)

- **Proposition 20.** The set {Δ_F : F ∈ H¹_sym} (d = 1, F_{v⊴e} = F_{u⊴e}, nonzero) equals the set of weighted graph Laplacians. Proof (one direction given): for weights w_vu, set F_{v⊴e} = F_{u⊴e} = ±√w_vu. Then L_vu = −w_vu and L_vv = Σ_u w_vu.
- **Proposition 29.** If F is an O(d) bundle with symmetric maps (F_{v⊴e} = F_{u⊴e}), then x ∈ ker Δ_F iff every coordinate x^k ∈ ker Δ₀. Proof: in the Dirichlet energy, ‖F_e D_v^{-1/2} x_v − F_e D_u^{-1/2} x_u‖ = ‖d_v^{-1/2} x_v − d_u^{-1/2} x_u‖ because F_e is orthogonal; the energy is then the graph Dirichlet energy applied channel by channel.

So identity restrictions, positive scalar restrictions and symmetric orthogonal restrictions all give exactly graph-Laplacian diffusion on each channel: the limit is (degree-weighted) agreement.

### 3. Two nodes with same-signed one-dimensional maps cannot stay apart (Proposition 23)

For G = one edge {v, u} with d = 1 and F_{v⊴e} = α, F_{u⊴e} = β, αβ > 0, the only harmonic vector is constant up to normalisation, so the two nodes become identical in the diffusion limit for every initial condition. This is the dyad case.

### 4. A negative transport separates (Proposition 10)

With d = 1, F_{v⊴e} = −α_e for v ∈ A and F_{u⊴e} = α_e for u ∈ B, the single harmonic vector has y_v > 0 on A and y_u < 0 on B. Diffusion polarises the classes to opposite signs. The transport F_vᵀF_u = −α_e² on cross edges is path-independent. The paper reads this as the sheaf-theoretic reason that negative edge weights help in heterophilic graphs.

### 5. The size of the harmonic space is a holonomy question (Proposition 4, Lemma 6, Propositions 3 and 5)

For an O(d) bundle on a connected graph:
1. If x ∈ H⁰, then on every edge x_{v_{i+1}} = F_{v_{i+1}}ᵀ F_{v_i} x_{v_i}, because F_{v_{i+1}} x_{v_{i+1}} = F_{v_i} x_{v_i} and F is orthogonal.
2. Composing around a cycle γ based at v gives x_v = P_γ x_v, so x_v ∈ ker(P_γ − I) (Proposition 4).
3. A global section is fixed by its value at one vertex, x_u = P_γ x_v. So dim H⁰ ≤ d, with equality iff transport is path-independent (Lemma 6).
4. Upper bound (Proposition 3): build a test signal by transporting one vector along minimal paths. Its Rayleigh quotient is bounded by r²/2, where r is the largest difference between two transports. So λ₀ ≤ r²/2: nearly path-independent transport gives a nearly harmonic signal.
5. Lower bound (Proposition 5): if every cycle moves every vector by at least ε‖x_v‖, then λ₀ ≥ ε²/(2·diam(G)·n·d_max). Proof: take the eigenvector, the vertex of largest norm and a cycle that moves it; telescope the cycle into edge discrepancies; use Cauchy-Schwarz and the Dirichlet energy.

On a tree, including a single edge, every transport is path-independent. So dim H⁰ = d always.

### 6. Oversmoothing is a contraction of the Dirichlet energy (Theorem 15/16, Lemmas 31-33)

E_F(x) = xᵀΔ_F x = ½ Σ_e ‖F_{v⊴e} D_v^{-1/2} x_v − F_{u⊴e} D_u^{-1/2} x_u‖².

**Theorem.** For F ∈ H¹₊ (one-dimensional maps of the same sign), or F an O(d) bundle with symmetric maps, and σ = (Leaky)ReLU:

  E_F(Y) ≤ λ* ‖W₁‖² ‖W₂ᵀ‖² E_F(X),  with λ* = max over nonzero eigenvalues of (λ − 1)².

Proof steps:
1. Lemma 31: expand x in eigenvectors of Δ_F. Then E_F((I − Δ_F)x) = Σ c_i² λ_i (1 − λ_i)² ≤ λ* Σ c_i² λ_i, since eigenvalues lie in [0, 2].
2. Lemma 32: E_F(XW) ≤ ‖Wᵀ‖² E_F(X), by trace cyclicity.
3. Lemma 33: E_F((I ⊗ W)x) ≤ ‖W‖² E_F(x). This needs the maps to be orthogonal and symmetric, so that W commutes past F_e.
4. The (Leaky)ReLU step does not increase the energy. Its proof was not read.

Consequence: if λ*‖W₁‖²‖W₂‖² < 1, the representation converges exponentially to ker Δ_F. If E_F(X) = 0, the output stays in the kernel whatever the weights.

**Escape (Proposition 17).** Outside H_sym, for any ε there is a sheaf, a W₁ with ‖W₁‖ < ε, and an x with E_F((I ⊗ W₁)x) > E_F(x). Construction: an O(d) bundle that is symmetric except on one edge, where B = F_{v₀}ᵀF_{u₀} − I ≠ 0 has a nontrivial kernel. Take x_v = √d_v · g with g ∈ ker B, a global section. Then W₁ = ε × the projection onto (ker B)^⊥ pushes x out of the kernel.

### 7. Any sheaf is learnable (Proposition 18)

If all ordered endpoint-feature pairs (x_v, x_u) are distinct, a smooth function equal to the target maps on that finite set exists (bump functions). By universal approximation an MLP Φ can approximate it. This is an existence result only.

**Where the theory is loose.**
- All separation results are about the t → ∞ limit and "almost all initial conditions".
- The Proposition 5 bound is, in the authors' words, "of little use in practice".
- Lemma 21 is imported without proof.
- The paper notes that Cai & Wang's original contraction bound "appears to be an error" and corrects it.
- Results on 9 node-classification datasets are empirical (Table 1): first on 5 of 6 heterophilic sets. No generalisation theory.

## What it would mean for a dyadic affective core (my inference)

The analogy the operator flagged is exact for a two-node graph, and the theorems say precisely when a dyad collapses.

**The dyad as a sheaf.**
- G = {s, o} with one edge e (or several edges, see below).
- F(s) = the agent's own affective-body stalk. F(o) = the agent's stalk for the partner. F(e) = an expression space where the two meet, for example face action units.
- A = F_{s⊴e} is the agent's map from its own state to expression. B = F_{o⊴e} maps the partner's state to expression.
- Diffusion drives the dyad to H⁰ = {A x_s = B x_o}: agreement in expression space, not in state space.

**Exact reductions to the excluded mechanisms.**
- **Copying.** A = B = I (constant sheaf), or any symmetric orthogonal pair (Proposition 29), gives L_F = L_graph ⊗ I_d with L_graph = [[1, −1], [−1, 1]]. The limit is x_s = x_o = the average. Each layer of a stacked version contracts E_F by λ*‖W₁‖²‖W₂‖² (Theorem 16). Collapse onto copying is then a theorem about depth and weight norms, not a training accident. This is the formal shape of the REACT failure, where copying the speaker nearly ties the best model.
- **Copy in a frame.** One edge is a tree, so any invertible orthogonal pair (A, B) has path-independent transport and dim H⁰ = d (Lemma 6). Changing basis at o by P = BᵀA turns it into the constant sheaf. So orthogonal per-expression maps, signed diagonals included, are copying after a fixed relabelling. A "−1" on the brow channel is anti-mimicry that is still a copy (Proposition 10 is this case).
- **A gain.** d = 1 with same signs (Proposition 23) collapses to agreement. With scalar maps A = aI, B = bI and the partner held fixed as data, the agent settles at x_s = (b/a) x_o: the flat-to-copy dial, with b/a as the dial.

**What escapes, with a provable property.**
1. *Non-invertible, per-expression maps.* If A has a kernel, the agent's state splits into ker A (private: no expression consequence and no partner influence) and its complement. Diagonal maps (Proposition 12) give d independent one-dimensional sheaves, so each expression channel can have its own sign and strength. That is requirement (a) at the level of structure: per-channel, signed, and not one scalar.
2. *Holonomy.* With several edges between s and o (for example one per context or per time lag, a multigraph), the transport around the s-o-s loop is P_γ = (F_{s⊴e₂}ᵀF_{o⊴e₂})(F_{o⊴e₁}ᵀF_{s⊴e₁}). By Proposition 4 and Lemma 6, if P_γ ≠ I then dim H⁰ < d: some expression directions cannot reach agreement at all. The spectral gap λ₀ > 0 on those directions (Proposition 5) is then a quantitative "no-copy margin". Copying is one global section among others, available only in the directions fixed by the holonomy.
3. *Learned, state-dependent maps.* NSD's Φ(x_v, x_u) is exactly "restriction maps that depend on both partners' current features". For the dyad it is the natural slot for partner history: Φ(x_s, x_o, h), with h a slow relation state.

**Theorems the design would need.**
- (i) A no-copy theorem: for the learned family of (A, B), copying is not in H⁰ except on a declared subspace. Equivalently, BᵀA ≠ I outside that subspace, with a lower bound on λ₀ there.
- (ii) A no-contraction theorem for the stacked network, from Proposition 17: the learned sheaf stays outside H_sym, or the energy ratio is bounded below.

The risk: NSD's sheaf is trained only for node classification. Nothing in the method stops a training loss that rewards matching the partner from learning A = B, the trivial sheaf.

## Verdict

adopt (as the formal frame for copy-collapse). It turns "oversmoothing" into theorems about ker L_F and energy contraction, and they apply to the two-node graph verbatim: identity, symmetric or same-signed maps provably collapse a dyad, while non-symmetric, signed, rank-deficient or holonomic maps provably do not. The learned-sheaf model itself is a GNN for node classification, not a dynamics design.
