# Hansen & Ghrist 2020/2021: Opinion Dynamics on Discourse Sheaves

## Citation

J. Hansen, R. Ghrist. "Opinion Dynamics on Discourse Sheaves." arXiv 2005.12798 (v1, 26 May 2020). Published in *SIAM Journal on Applied Mathematics*, 2021. (I took the venue from memory and did not check it; the arXiv v1 text is the source read.)

## What was read

arXiv v1 PDF, text extraction.
- Read in full: §1-§12, every theorem and proof (Theorems 2.2, 4.1, 5.1, 6.1, 8.1, 9.2, 9.3, 9.4, 11.1, 11.2; Lemma 9.1; Propositions 10.1, 12.1), and Examples 4.2, 6.3, 8.2, 9.5.
- Skimmed: §13 Conclusions.
- Not read: the references. Theorem 6.2 is stated in the paper without proof.

## The object, exactly

**Discourse sheaf (§3).** G = (V, E) is a social network. Each agent v has an opinion stalk F(v), a real inner-product space whose basis is "private" topics. Each edge e = u ∼ v has a discourse stalk F(e), whose basis is topics up for discussion. The expression maps F_{v⊴e}: F(v) → F(e) are linear.
- A 0-cochain x ∈ C⁰ = ⊕F(v) is a private opinion distribution.
- A 1-cochain is a distribution of expressed opinions.
- Coboundary: (δx)_e = F_{v⊴e}x_v − F_{u⊴e}x_u, "difference of expression".
- Laplacian: L_F = δᵀδ, with (L_F x)_v = Σ_e F_{v⊴e}ᵀ(F_{v⊴e}x_v − F_{u⊴e}x_u).
- Hodge (Theorem 2.2): H⁰(G; F) = ker L_F.

The paper's reading:
- Agreement F_{u⊴e}x_u = F_{v⊴e}x_v "does not imply that u and v have the same opinions: it means that their expressions of personally held opinions have the appearance of agreement."
- Negative scalars in a restriction map "permit falsehoods", and this can be selective by edge.
- The constant sheaf Rⁿ "is the implicit structure in most of the literature on opinion dynamics."

**Dynamics studied.**
1. Opinion diffusion: ẋ = −αL_F x (Eq. 4.1).
2. Stubborn agents U: ẋ_v = −α(L_F x)_v for v ∉ U, and ẋ_v = 0 for v ∈ U (Eq. 5.1).
3. Control: ẋ = −αL_F x + Bu (Eq. 6.1).
4. Weighted reluctance: ẋ_v = −α(L_F x)_v + αγ_v((x₀)_v − x_v) (Eq. 7.1). This is realised as a sheaf on an augmented graph. Each agent gets a stubborn "parent" vertex v′ joined by restriction maps √γ_v·I.
5. Expression learning ("learning to lie"): dF_{v⊴e}/dt = −β(F_{v⊴e}x_v − F_{u⊴e}x_u)x_vᵀ, or dδ/dt = −βP_δ(δxxᵀ) (Eqs. 8.1-8.3).
6. Joint opinion-expression diffusion: ẋ = −αδᵀδx together with δ̇_e = −βδ_e x_e x_eᵀ (Eq. 9.1).
7. Nonlinear Laplacians L^Φ_F = δᵀ∘Φ∘δ from edge potentials U_e: bounded confidence (§11) and antagonism (§12).

## Key properties and their proofs

**Theorem 4.1.** x(t) → the orthogonal projection of x(0) onto H⁰.
- Proof: L_F is symmetric PSD, so exp(−tαL_F) tends to the projector onto ker L_F.
- "If this sheaf has no nontrivial global sections, the only stable opinions will be everywhere zero."

**Example 4.2.** Four agents with one-dimensional stalks. Two agents "tell a polite lie" (a negative restriction map) to the other two. Every initial condition converges to a polarised global section: public agreement with opposite private opinions.

**Theorem 5.1 (stubbornness = harmonic extension).** With x|_U = u held fixed, write y = x|_Y for Y = V∖U.
1. The dynamics are ẏ = −α(L[Y,Y]y + L[Y,U]u).
2. L[Y,Y] is a principal submatrix of a PSD matrix, so it is PSD, and im L[Y,U] ⊆ im L[Y,Y].
3. Split y = y^⊥ + y^∥ with y^⊥ ∈ ker L[Y,Y]. The y^⊥ part never moves.
4. Solve the inhomogeneous linear ODE on im L[Y,Y]. The limit is y^∥_∞ = −L[Y,Y]^† L[Y,U]u.
5. So y_∞ = y₀^⊥ − L[Y,Y]^† L[Y,U]u: the minimum-norm harmonic extension plus the untouched kernel part. It minimises ‖δx‖² subject to x|_U = u.

**Theorem 6.1 (controllability).** If H⁰(G, U; F) = 0 (no nonzero global section vanishes on U), the system is stabilisable with inputs at U. Proof: the PBH rank test; only λ = 0 matters because the spectrum of −αL is real and non-positive.

**Theorem 8.1 (learning to lie).** With x fixed, each edge block δ_e follows a linear flow δ̇_e = −βδ_e(x_e x_eᵀ). That flow is PSD in the trace inner product, with kernel {δ_e : δ_e x_e = 0}. So δ converges to the Frobenius-nearest coboundary δ′ with δ′x = 0. The sheaf learns the smallest change of expression that makes the current opinions look like agreement. Example 8.2: two agents with opinions −4 and +1 on the constant sheaf. One restriction map changes sign and shrinks: that agent "learns to lie".

**Lemma 9.1 and Theorems 9.2-9.4 (joint dynamics).**
- Ψ(x, δ) = ½xᵀδᵀδx is non-increasing. Its derivative is −α xᵀ(δᵀδ)²x − β Σ_e ‖δ_e x_e‖²‖x_e‖².
- The flow is gradient descent on Ψ in the metric (1/α)xᵀx′ + (1/β)Σ tr(δ_eᵀδ′_e). So the limit points satisfy δx = 0.
- Smooth equilibria are Lyapunov stable (Theorem 9.2, by the centre-manifold argument).
- Theorem 9.3: the diagonal blocks of M = αδᵀδ − βxxᵀ are conserved. Hence if some diagonal block of M(0) is indefinite, x(∞) ≠ 0. For any (δ₀, x₀) some rescaling κx₀ converges to a nontrivial global section.
- Theorem 9.4: ‖δ‖_F², ‖x‖² and ‖δx‖² are non-increasing, and so is the Rayleigh quotient ‖δx‖²/‖x‖² (by Jensen's inequality).

**Proposition 10.1.** For edge potentials U_e that are radially unbounded with a unique local minimum at 0, the nonlinear heat equation has the same limit as the linear one. The Lyapunov argument runs on im δᵀ.

**Theorems 11.1-11.2 (bounded confidence).**
- The potential is U_e(y) = ψ_e(‖y‖²) with ψ′_e > 0 below a threshold D_e and ψ′_e = 0 above it.
- x is an equilibrium iff every edge either agrees or disagrees by at least D_e.
- Near an equilibrium in the interior of its region K_x, trajectories converge to the nearest global section of the sub-sheaf F_x, which keeps only the edges still "in confidence".

**Proposition 12.1 (antagonism).**
- Negative edges carry the potential −‖y‖², which gives the linear signed Laplacian L^S_F = δᵀSδ, with S = ±I by edge sign.
- If the negative edges form a cutset and some local section on one side does not extend by zero, then L^S is indefinite and the dynamics are unstable.
- "For the case of the constant sheaf on G, … a graph with a cutset of negative edges always has an indefinite signed Laplacian, and hence unstable opinion dynamics."
- The paper also names the alternative: flip the sign of a restriction map, "an agreement to disagree". That alternative is stable.

## What it would mean for a dyadic affective core (my inference; derivations mine, numerically checked)

**The dyad sheaf.**
- Vertices: s (the agent) and o (the partner as observed). One edge e for now.
- F(s) = Rⁿ is the agent's private affect and body state. F(e) = R^k is the expression space (for example action units). A = F_{s⊴e} (k×n) is the agent's own state-to-face map.
- The partner's observed state u(t) sits at o with map B (for example B = I if o holds the observed AUs).
- The partner is stubborn from the agent's point of view: the agent cannot move it. Theorem 5.1 then gives the agent's dynamics:

  ẋ_s = −α Aᵀ(A x_s − B u).

**Proposition D1 (what the dyad sheaf computes).** For fixed A and B, and a constant u, x_s(t) → A⁺B u + Π_{ker A} x_s(0).
- Proof: Theorem 5.1 with L[Y,Y] = AᵀA and L[Y,U] = −AᵀB. Then (AᵀA)^†AᵀB = A⁺B. I checked this numerically with random A (2×4) and B (2×5): prediction and simulation agree to 4 decimals.
- Reductions:
  - A = B = I: x_s → u, exact copying.
  - A = aI, B = bI: x_s → (b/a)u, the flat-to-copy dial.
  - Diagonal A and B: x_s,i → (b_i/a_i)u_i, a signed gain per expression channel with no cross-talk.
  - General A and B: any linear map of rank ≤ k, factored as "read the partner's face (B), then invert my own face (A⁺)". Smile-to-anger and other off-diagonal responses are allowed.
- The kernel part Π_{ker A}x_s is untouched by any partner. It is the private part of the state: provably invariant under all partner input.

**Proposition D2 (only what I can express can move me: requirement (d)).** The partner enters only through Aᵀ. Any component of the partner's expression B u in (im A)^⊥ = ker Aᵀ has no effect on x_s, at any time and for any input. Proof: ẋ_s depends on u only through AᵀBu. This is "reading the other through one's own body" as an exact statement: perception of the other is the adjoint of one's own expression map.

**Proposition D3 (no flat affect, whatever the partner does).** Let the agent learn its own expression map by the paper's rule, Ȧ = −β(A x_s − B u)x_sᵀ, while ẋ_s = −αAᵀ(A x_s − B u) and u(t) is any partner signal. Then

  Q := α AᵀA − β x_s x_sᵀ is constant in time.

Proof, with r = A x_s − B u:
1. d(AᵀA)/dt = ȦᵀA + AᵀȦ = −β(x_s rᵀA + Aᵀr x_sᵀ).
2. d(x_s x_sᵀ)/dt = ẋ_s x_sᵀ + x_s ẋ_sᵀ = −α(Aᵀr x_sᵀ + x_s rᵀA).
3. So α·(step 1) − β·(step 2) = 0. u never enters.

This is Hansen & Ghrist's Theorem 9.3 invariant, extended to an exogenous partner. Their partner vertex also evolves; here it need not. Numerical check: n = 4, k = 3, partner input a sum of sinusoids, 20 time units of RK2 integration. The largest entry of |Q(t) − Q(0)| was 3.4×10⁻⁶, against entries of Q of order 1.7.

Consequence: suppose Q has a negative eigenvalue −q with unit eigenvector w. Then for all t,

  β (wᵀx_s(t))² = α‖A(t)w‖² + q ≥ q.

So the agent's state keeps |wᵀx_s| ≥ √(q/β) whatever the partner does. A provable floor against flat affect.

Two limits of D3:
- AᵀA is PSD and βx_sx_sᵀ has rank 1, so Q has at most one negative eigenvalue. The floor holds in one direction only.
- AᵀA(t) = (Q + βx_s x_sᵀ)/α is fixed by the current state. The relation learned into A is slaved to x_s up to a rotation within expression space. So this flow cannot hold a slow partner-history memory separate from the current state (requirement (a), the history part). A separate slow variable, such as a restriction map driven by a different time scale and signal, would have to be added. Once it is, the invariant must be rechecked.

**Proposition D4 (learned relation = minimal lie).** By Theorem 8.1, if only A learns and x_s and u are held fixed, A converges to the Frobenius-nearest map under which the current pair looks like agreement. For an affective agent this is the warning: an expression map learned only to reduce discord learns to display agreement. It is the sheaf form of a sycophantic face. A learning rule for the relation must therefore have a target other than ‖δx‖².

**Signs, exactly.** Two ways to get a negative response, with opposite properties:
- (i) A sign in a restriction map, such as A_ii < 0 ("lying"). This is stable, but on a tree it is gauge-equivalent to copying: change basis by −1 on that channel. Anti-mimicry by a fixed sign is copy in a flipped frame.
- (ii) A negative edge potential (repulsion). On the dyad the single edge is a cutset, so by Proposition 12.1 the signed Laplacian is indefinite and the dynamics diverge.

Neither gives the human pattern of a sign that depends on the relation (Carr 2014: smiling at anger under power). That needs a restriction map whose sign is a function of a slow relation state, together with a theorem that the sign switch keeps the system stable. A switched linear system with a common Lyapunov function would be one route; it is not in this paper.

**Time scales (c).** Per channel, the relaxation rate is α times the eigenvalues of AᵀA restricted to im Aᵀ (Proposition D1 dynamics). The private kernel has rate 0, which makes it temperament-like. Reluctance γ_v (§7) adds a rate αγ_v toward a stored baseline x₀. That gives three structural time scales: expression-coupled modes at rate αλ(AᵀA), reluctance at αγ, and the invariant kernel. The learning rate β adds a fourth, for the relation.

## Verdict

adopt. It is the closest existing precise object to (a), (b) and (d): private state separate from public expression, per-edge and per-topic signed maps, stubbornness as harmonic extension, and learned expression maps with proved convergence. It also shows the traps exactly:
- the constant sheaf is copying;
- scalar maps are a gain;
- a sign is copy in a flipped frame;
- repulsion is unstable;
- learning to reduce discord learns to lie.

The derived no-flat invariant (D3) is the one new property worth carrying into a design.
