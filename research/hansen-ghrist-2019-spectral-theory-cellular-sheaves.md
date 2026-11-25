# Hansen & Ghrist 2019: Toward a Spectral Theory of Cellular Sheaves

## Citation

J. Hansen, R. Ghrist. "Toward a Spectral Theory of Cellular Sheaves." *Journal of Applied and Computational Topology* 3 (2019). arXiv 1808.01513. (I took the venue from memory and did not check it; the arXiv text is the source read.)

## What was read

arXiv PDF, text extraction.
- Read in full: §1 Introduction; §2.2 Cellular sheaves (definitions, global sections, cosheaves, cohomology, morphisms, operations); §3.1 Weighted sheaves; §3.2 The sheaf Laplacian, including Theorem 3.1 (discrete Hodge) and its proof; §3.4 Normalisation; §3.5 Discrete vector bundles; §3.6 Comparison with earlier constructions; §4.1 Harmonic extension (Proposition 4.1 and proof); §4.3 Maximum modulus (Lemma 4.4, Theorem 4.5); §5 opening (Propositions 5.1, 5.2, 5.5, Theorem 5.7); §5.4 Product complexes (Proposition 5.15, Corollary 5.16, Proposition 5.17); §7 Cheeger; §8.1 Consensus (Proposition 8.1 and proof); §8.2 Flocking; §8.3 Opinion dynamics; §8.7 Synchronisation.
- Not read: §2.1 cell-complex details; §3.3 infinite-dimensional case; §4.2 Kron reduction; §5.1 beyond Theorem 5.7; §5.2-5.3 morphisms and covers; §6 effective resistance and sparsification; §8.4-8.6 and §8.8; §9.

## The object, exactly

**Cellular sheaf (Definition 2.4).** X is a regular cell complex with face poset P_X. A cellular sheaf F is a functor P_X → Vect:
- a stalk F(σ) for every cell σ;
- a restriction map F_{σ⊴τ}: F(σ) → F(τ) for every incidence σ ⊴ τ;
- identity: F_{σ⊴σ} = id; composition: ρ ⊴ σ ⊴ τ ⇒ F_{ρ⊴τ} = F_{σ⊴τ} ∘ F_{ρ⊴σ}.

Related definitions:
- Global section (Definition 2.5): x_τ = F_{σ⊴τ} x_σ for all σ ⊴ τ.
- Constant sheaf V: every stalk V, every map the identity.

**Cochains and coboundary.** C^k = ⊕_{dim σ = k} F(σ). With a signed incidence [σ : τ] ∈ {0, ±1}, the coboundary is (δ^k x)_τ = Σ [σ : τ] F_{σ⊴τ} x_σ, and δ^{k+1}δ^k = 0. Then H⁰(X; F) ≅ Γ(X; F), the global sections. On a graph, (δx)_e = F_{v⊴e} x_v − F_{u⊴e} x_u.

**Weighted sheaf (§3.1).** The stalks are inner-product (Hilbert) spaces, so every restriction map has an adjoint F*.

**Hodge Laplacians (§3.2).**
- Δ^k = (δ^k)*δ^k + δ^{k−1}(δ^{k−1})*, with up-Laplacian L^k = (δ^k)*δ^k.
- On a graph the degree-0 Laplacian L = δ*δ has blocks L_vv = Σ_e F_{v⊴e}*F_{v⊴e} and L_uv = −F_{u⊴e}*F_{v⊴e}.
- Normalised version (Definition 3.5, Lemma 3.6): reweight the stalk inner products, not the matrix. On a graph this gives D^{†/2} L D^{†/2}.

**Discrete O(n)-bundle (§3.5).** Every restriction map on a cell is a positive scalar times an orthonormal map. Such bundles correspond to flat vector bundles, local systems, and representations of the fundamental groupoid (Riemann-Hilbert, cited by the paper). The graph connection Laplacian of Singer & Wu is the sheaf Laplacian of an O(n)-bundle (§3.6).

## Key properties and their proofs

### Theorem 3.1 (discrete Hodge): ker Δ^k ≅ H^k

1. H^k = ker δ^k / im δ^{k−1}. In finite dimensions this is isomorphic to (ker δ^k) ∩ (im δ^{k−1})^⊥ = ker δ^k ∩ ker (δ^{k−1})*.
2. ker δ^k = ker (δ^k)*δ^k = ker Δ^k₊, and likewise ker (δ^{k−1})* = ker Δ^k₋.
3. ker(Δ₊ + Δ₋) = ker Δ₊ ∩ ker Δ₋, because im Δ₊ = (ker δ^k)^⊥ and im Δ₋ ⊆ ker δ^k, so the two images meet only at 0.
4. Corollary: C^k = H^k ⊕ im δ^{k−1} ⊕ im (δ^k)*, an orthogonal decomposition.

For k = 0 on a graph: ker L = H⁰ = global sections. The paper's own warning: "one cannot hear the shape of a sheaf". Two non-isomorphic sheaves can share a Laplacian (Fig. 3.1), because restriction maps can be rank-deficient.

### Proposition 8.1 (consensus on a sheaf)

ẋ = −Δ^k_F x converges exponentially to the orthogonal projection of x₀ onto H^k.
1. x(t) = e^{−tΔ} x₀.
2. Δ is self-adjoint, so x(t) = Σ_i e^{−tλ_i} ⟨v_i, x₀⟩ v_i.
3. Terms with λ_i > 0 decay at rate λ_i. Terms with λ_i = 0 stay.

"A distributed system can reach consensus on the nearest global section to an initial condition."

### Proposition 4.1 (harmonic extension)

Partition the cells into a boundary subcomplex B and the rest S. Given x|_B, there is a unique x harmonic on S with that boundary value if H^k(X, B; F) = 0. Proof:
1. Write the block equation Δ(S,S) x_S + Δ(S,B) x_B = 0.
2. Show ker Δ(S,S) ⊆ ker of the Hodge Laplacian of the relative complex. So Δ(S,S) is invertible when the relative cohomology vanishes.

For 0-cochains an extension always exists. It is unique iff H⁰(X, B; F) = 0.

### Theorem 4.5 / Corollary 4.6 (maximum modulus, O(n)-bundles)

A 0-cochain harmonic off a thin boundary set B attains its maximum stalk norm on B.
1. Lemma 4.4: at a harmonic vertex, x_v = (1/d_v) Σ F_{v⊴e}*F_{w⊴e} x_w. Each F*F is α_e² times an orthogonal map.
2. Take norms and apply the triangle inequality: ‖x_v‖ ≤ (1/d_v) Σ α_e² ‖x_w‖ ≤ ‖x_v‖ at an interior maximum. So equality holds throughout.
3. Propagate the equality through the connected interior.

### Theorem 5.7 / Proposition 5.8 (interlacing)

A rank-t PSD perturbation shifts eigenvalues by at most t places (Courant-Fischer). Deleting cells from a sheaf therefore interlaces its spectrum, with t the codimension of H^k of the deleted part.

### Proposition 5.15 / Corollary 5.16 (product sheaves)

For F on X and G on Y, the product sheaf F ⊠ G = π_X*F ⊗ π_Y*G on X × Y has the degree-0 Laplacian

  L_{F⊠G} = id ⊗ L_G + L_F ⊗ id,

and its spectrum is {μ_i + λ_j}. Proof: C¹(X×Y) splits into (C⁰_F ⊗ C¹_G) ⊕ (C¹_F ⊗ C⁰_G). The coboundary is the stacked block [id ⊗ δ_G; δ_F ⊗ id]. Then δ*δ gives the sum. For graphs, Proposition 5.17 gives the eigenvectors of L¹ from those of L⁰.

### §7 (Cheeger)

For O(n)-bundles the authors restate the Bandeira-Singer-Spielman bound λ₁ ≤ min η(x) ≤ 10√λ₁ as reported, not proved here. For sheaves whose maps are partial isometries they give a two-vertex counterexample to the rounding lemma: F(v₁) = F(v₂) = R², F(e) = R, maps [1 0] and [½ √3/2]. So the Cheeger route fails beyond bundles. §7.2 proposes a "structural" Cheeger constant instead: the smallest perturbation of the restriction maps that creates a new global section. It is bounded below by λ₁(L_F) in a Frobenius relaxation (stated, not proved in detail).

### §8.2-8.3 (applications, sketched, no theorems)

- Flocking: each agent has stalk R³ in its own frame. An edge stalk R compares bearings. The restriction maps are ⟨b(v,w), ·⟩ and −⟨b(w,v), ·⟩. A common heading is a global section.
- Opinion dynamics: private opinion stalks and edge "discourse spaces". Topics outside an edge's discussion lie in the kernel of its restriction maps. Agents "lie … only to certain individuals on certain topics". This is developed in the discourse-sheaf paper (separate note).

**Where the paper is loose.** Its title says "toward". Much of §8 is sketched applications with no results. The Cheeger section for general sheaves is open. Venue and later versions not checked.

## What it would mean for a dyadic affective core (my inference)

Three results from this paper do real work for the dyad. The worked sheaf, its no-flat invariant and the time-scale reading are in the discourse-sheaf note.

1. **Each agent's own frame is built in, which serves (d).** The flocking construction is "reading the other through my own body" in exact form. Each agent's stalk is in its own coordinates. Comparison happens only in an edge space, through the agent's own restriction map. The agent never touches the partner's stalk directly. The adjoint F_{s⊴e}* is the only route from expression space into the agent's own state. So the partner's expression can affect only im F_{s⊴e}*. That subspace is the orthogonal complement of the agent's private kernel, and it is set by the agent's own expression map. The precise statement is: (im A)^⊥ = ker Aᵀ is invisible to the agent. If my body cannot produce an expression component, I cannot register it in another, under this dynamics.

2. **Time scales are spectral, from the product sheaf (c).** Put the dyad sheaf F (on the two-node graph) in a product with a sheaf G on a time or scale graph Y. For example, Y is a path of "fast", "middle" and "slow" copies of each stalk, with restriction maps that scale or project. The Laplacian is L_F ⊗ I + I ⊗ L_G, and its decay rates are sums μ_i + λ_j. A mode's relaxation time is 1/(μ_i + λ_j). A design can therefore read off which expression channel relaxes at which rate from two spectra, instead of setting time constants by hand. Per-expression restriction maps give per-expression rates without any time-constant parameter. The cost is that rate and coupling strength are tied, since μ_i grows with ‖F‖². That is a testable prediction: the most strongly coupled channel should be the fastest. It may conflict with the Carr 2014 observation that context-carrying smile responses are the slow ones (mimicry synthesis, section 3).

3. **Copy is one global section, and collapse is a spectral fact.** By Theorem 3.1 and Proposition 8.1, where a coupled dyad ends up is decided by H⁰ alone. With the constant sheaf, H⁰ is the diagonal {x_s = x_o}, which is copying. With non-identity maps, H⁰ = {A x_s = B x_o} contains copying only if A = B on the relevant subspace. So "how close is this design to copying" has an exact answer: the principal angles between H⁰ and the diagonal. The interlacing result (Theorem 5.7) bounds how much that can change when one coupling edge is added or removed.

**Reductions.**
- Constant sheaf: graph-Laplacian consensus = copying.
- O(n)-bundle on the single-edge dyad: path-independent transport, so the sheaf is isomorphic to a constant sheaf after a change of frame. That is copying in a rotated frame, and the maximum-modulus principle gives ‖x_s‖ = ‖x_o‖ at the harmonic extension.
- Only rank-deficient maps or loops with holonomy escape.

**Theorems a design would need.**
- (i) H⁰ ∩ diagonal = a declared subspace (the robust smile-to-smile core in the mimicry synthesis), with a lower bound on λ₁ elsewhere.
- (ii) A product-sheaf spectrum statement that puts the context-dependent channels' relaxation times in the 2-4 s band and the matching channels' below 1 s.

## Verdict

adopt (as the mathematical base for any sheaf design). It supplies the definitions and the Hodge, consensus, harmonic-extension, maximum-modulus and product-spectrum theorems with checkable proofs. The opinion-dynamics material is sketched and is developed in the discourse-sheaf paper.
