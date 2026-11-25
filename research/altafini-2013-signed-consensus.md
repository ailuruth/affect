# Altafini 2013: Consensus Problems on Networks with Antagonistic Interactions

## Citation

- C. Altafini. "Consensus problems on networks with antagonistic interactions." *IEEE Transactions on Automatic Control* 58(4):935-946, 2013. No arXiv version exists (checked the arXiv author listing for Altafini; the closest arXiv items are later papers). An author copy is listed at users.isy.liu.se (Linköping), but that host did not resolve from this machine, so the original was **not read**.
- Read instead, and cited below "as reported by":
  - A. V. Proskurnikov, R. Tempo. "A Tutorial on Modeling and Analysis of Dynamic Social Networks. Part II." *Annual Reviews in Control* 2018. arXiv 1801.06719 (v2). Section 6 covers the Altafini model. Below: "P&T-II".
  - G. Shi, C. Altafini, J. S. Baras. "Dynamics over Signed Networks." *SIAM Review* 2019. arXiv 1706.03362 (v3). Altafini is a co-author. It gives a discrete-time version of the theorem with a full proof. Below: "SAB".

## What was read

- **Altafini 2013 itself: not read.** Every statement about it below is "as reported by" P&T-II or SAB.
- P&T-II, read in full: section 6 (6.1 balance theory, Definitions 2-6, Lemmas 25-26; 6.2 Altafini's model, Propositions 27-28, Theorem 29, Remark 30, the Fig. 7 counterexample, Lemmas 31-32), and the opening of 6.3 (extensions, discrete-time Altafini model). The rest of Part II was not read.
- SAB, read in full: section 1 (signed graphs, the two signed Laplacians, structural balance, the opposing and repelling rules) and section 2.1.1 (Theorem 1 with its proof, Theorem 3 statement for digraphs). Skimmed: 2.1.2 (repelling rule) and the random-network results in section 3. Not read: the appendix proofs of the digraph and random cases.
- P&T-II states the key lemma (Lemma 26) without proof and cites Altafini. The proof given for it below is my reconstruction and is marked as such.

## The object, exactly

**Signed graph.** n agents, V = {1..n}. A = (a_ij) in R^{n×n}, with a_ij != 0 iff agent j influences agent i, and the entries may be negative. Following P&T-II, A is assumed sign-symmetric: a_ij a_ji >= 0 (friendship and enmity are mutual).

**Signed Laplacian** (P&T-II eq. 53, as reported from Altafini):

    L[A] = Δ − A,   Δ = diag(Σ_m |a_1m|, ..., Σ_m |a_nm|)

So l_jk = −a_jk for j != k and l_jj = Σ_m |a_jm|. When A >= 0 this is the usual weighted Laplacian.

**Dynamics** (continuous time, P&T-II eq. 54):

    dx_i/dt = Σ_j |a_ij| (sgn(a_ij) x_j − x_i) = Σ_j (a_ij x_j − |a_ij| x_i),   that is   dx/dt = −L[A] x,   x(t) in R^n

Each agent moves toward the partner's opinion when the tie is positive, and toward the *negated* partner opinion when it is negative. SAB call this the "opposing rule". They contrast it with the "repelling rule", which pushes the two states apart and is a different model.

**Discrete time** (SAB eq. 8-9, undirected, unweighted, step sizes α for positive edges and β for negative edges):

    x(t+1) = W_G x(t),   W_G = I − α L_{G+} − β L^o_{G−}

Here L^o_{G−} = D_{G−} − A_{G−}, where A_{G−} has −1 on negative edges. Each row of W_G has absolute values summing to 1 (SAB eq. 10).

**Structural balance** (P&T-II Def. 4). V splits into disjoint V1 and V2 (one may be empty) such that a_ij >= 0 within V1 and within V2, and a_ij <= 0 across them. Harary's theorem (as reported by SAB): an undirected signed graph is balanced iff no cycle has an odd number of negative edges. P&T-II Lemma 25: balanced implies all cycles positive. The converse holds for strongly connected graphs; in general all semicycles must be positive.

**Gauge transformation** (P&T-II eq. 55). Let δ_i = +1 for i in V1 and −1 for i in V2, and let D = diag(δ_1..δ_n), so that D = D^{-1}. Then:

    y = D x,   δ_i δ_j a_ij = |a_ij|,   D A D = |A| >= 0,   L[A] = D L[|A|] D

where |A| = (|a_ij|). In y-coordinates the dynamics are ordinary unsigned consensus (P&T-II eq. 56):

    dy_i/dt = Σ_j |a_ij| (y_j − y_i)

**Lemma G (balance ⇔ gauge).** G[A] is structurally balanced iff some D = diag(±1) gives D A D >= 0 off the diagonal.

Proof (one line, mine): given the partition, take δ as above. Then δ_i δ_j = +1 within a camp and −1 across, which flips exactly the negative entries. Conversely, given D, set V1 = {i : δ_i = +1}.

The gauge leaves diagonal entries unchanged (δ_i² = 1), so a negative self-loop can never be gauged away.

## The key property and its proof, step by step

### Continuous-time result (P&T-II, as reported from Altafini)

**Lemma 26.** If G[A] is strongly connected, then 0 is an eigenvalue of L[A] iff G[A] is structurally balanced.

**Theorem 29 (static A).**
- (a) If G has a directed spanning tree and is structurally balanced, the opinions polarize (P&T-II eq. 57):

      x_i(t) → w^T x(0) for i in V1,   x_i(t) → −w^T x(0) for i in V2,   w = D p

  Here p >= 0 is the left null vector of L[|A|], normalized so that p^T 1 = 1. This is "bipartite consensus".
- (b) If G is strongly connected and structurally imbalanced, then −L[A] is Hurwitz and x(t) → 0 for every x(0).
- (c) In general the opinions converge and may split into clusters.

Proposition 27 adds that the system is always Lyapunov stable (M(t) = max_i |x_i(t)| is non-increasing). Proposition 28 adds that limits always exist.

**Proof, as numbered checkable steps.** Steps 2-4 are my reconstruction of Lemma 26, which P&T-II only state.

1. **Gershgorin.** Row i of L[A] has centre l_ii = Σ_m |a_im| and radius Σ_{m≠i} |a_im| <= l_ii. So every eigenvalue of −L[A] lies in Re ≤ 0, and the only possible eigenvalue on the imaginary axis is 0 (P&T-II, text before Lemma 26).
2. **Balanced ⇒ 0 is an eigenvalue.** L[A] = D L[|A|] D, and L[|A|] 1 = 0, so L[A] (D 1) = 0. Strong connectivity is not needed for this direction.
3. **0 is an eigenvalue ⇒ balanced, under strong connectivity** (reconstruction):
   - Let L[A] v = 0 with v ≠ 0, and pick i with |v_i| = max_k |v_k|.
   - Row i reads l_ii v_i = Σ_{j≠i} a_ij v_j. So |v_i| Σ_j |a_ij| ≤ Σ_{j≠i} |a_ij| |v_j| ≤ |v_i| Σ_{j≠i} |a_ij|. (Any self-loop |a_ii| enters the left side only, and only strengthens the inequality.)
   - Equality must hold throughout. So every in-neighbour j of i has |v_j| = |v_i| and sgn(a_ij v_j) = sgn(v_i).
   - The set of maximizers is therefore closed under taking in-neighbours. Strong connectivity makes it all of V.
   - Set V1 = {v_i > 0} and V2 = {v_i < 0}. The sign condition says a_ij > 0 inside a camp and a_ij < 0 across camps, which is balance.
4. **Imbalanced and strongly connected ⇒ Hurwitz.** By step 3, 0 is not an eigenvalue. By step 1, no other eigenvalue lies on the imaginary axis. So −L[A] is Hurwitz, giving (b).
5. **Balanced ⇒ polarization.**
   - Under the gauge, y = D x obeys unsigned consensus.
   - With a directed spanning tree, 0 is a simple eigenvalue of L[|A|] (P&T-II Part I, Lemma 8), so y(t) → 1 p^T y(0).
   - Undo the gauge: x(t) → D 1 p^T D x(0). This gives (a) with w = D p.
   - The limit is nonzero for almost every x(0), namely whenever w^T x(0) ≠ 0.

**Hypotheses matter.** P&T-II (Fig. 7) give a 3-agent graph that has a spanning tree but is not strongly connected and is imbalanced: a12 = a21 = −1, a31, a32 > 0. It has a line of equilibria (ξ, −ξ, ρξ) with ρ = (a31 − a32)/(a31 + a32). So it shows neither polarization nor decay to zero, and "imbalanced ⇒ 0" needs strong connectivity.

### Discrete-time result with a complete proof (SAB Theorem 1, undirected)

Assume 0 < α + β < 1/max_i deg_i. Then:
- (i) If G is balanced with partition V1, V2, then x_i(t) → ±(Σ_{V1} x_j(0) − Σ_{V2} x_j(0))/n, with sign + on V1 and − on V2.
- (ii) If G is not balanced, then x_i(t) → 0 for all i.

Their proof:

1. (i) The gauge z_i = ±x_i turns (8) into a standard consensus iteration, so (i) follows from known consensus results.
2. (ii) By Gershgorin, every eigenvalue of W_G lies in (−1, 1]. W_G is symmetric, so x(t) → y with W_G y = y.
3. Claim: |y_1| = ... = |y_n|. SAB's text says only "impossible for a connected graph". The fill-in:
   - Take i maximizing |y_i|. Then |y_i| ≤ Σ_j |[W_G]_ij| |y_j| ≤ |y_i|, using absolute row sums equal to 1.
   - So every neighbour j of i has |y_j| = |y_i|, with [W_G]_ij y_j of the same sign as y_i.
   - Connectivity spreads this to every node.
4. If y ≠ 0, the sign pattern of y is a balancing partition (step 3's sign condition), which contradicts imbalance. So y = 0.

**Where the sources are loose.**
- SAB step 3 is stated without the maximizer argument, filled in above.
- SAB Theorem 3(i) for digraphs carries a stray "/n" next to weights that already sum to 1.
- P&T-II state Lemma 26 without proof.
- I could not check Altafini's own Lyapunov proof or his nonlinear variants. P&T-II say the nonlinear variants behave "very similar[ly]", but that claim is unchecked here.

## What it would mean for a dyadic affective core (my inference)

**Mapping.**
- Two agents, A (the engine) and B (the partner), each with m expression channels (action-unit groups).
- Lift to a signed graph on 2m nodes (agent, expression), with state x = (x_A, x_B) in R^{2m}.
- The coupling matrix has four m×m blocks:
  - K_AA: within-agent, cross-expression coupling;
  - K_AB: partner expression → engine expression; for example a negative (A, anger) ← (B, smile) entry;
  - K_BA and K_BB: the partner's side.
- Per-expression, possibly signed coupling (requirement (a)) is the sign pattern of K_AB.

**Precise reductions** (these follow from Lemma G and Theorem 29).

1. **Per-channel counter-mimicry is copying in a flipped frame.** Suppose K_AA and K_BB are diagonal (no cross-expression coupling inside an agent). Then the lifted graph splits into m separate dyads, one per expression p: (A,p)–(B,p). A sign-symmetric 2-node graph has no cycle that can be negative, so each dyad is balanced. In the gauge y_{A,p} = x_{A,p}, y_{B,p} = sgn(k_p) x_{B,p}, the dynamics are plain consensus. Counter-mimicry on expression p is exactly copying the negated partner channel, and the limit is x_{A,p} = sgn(k_p) x_{B,p}.
2. **Cross-expression coupling with a balanced sign pattern changes nothing in kind.** If some D = diag(±1) on the 2m nodes makes D K D ≥ 0, the whole system is unsigned consensus in the frame D. If the lifted graph is also connected, all 2m node values converge to one common modulus, so every expression of both agents ends at ±c. That is worse than copying: it is a mean face up to signs.
3. **Imbalance gives a flat face.** A negative cycle can arise only through cross-expression links. An example: (A,smile) ← (B,smile) positive, (B,smile) ← (B,anger) positive, (B,anger) ← (A,smile) negative. With such a cycle, a strongly connected lifted graph has −L Hurwitz and every channel decays to 0. Sign-asymmetric coupling falls in the same case: the engine mimics while the partner counter-mimics, a12 = 1, a21 = −1, which is not sign-symmetric and so not balanced. Its −L = [[−1, 1], [−1, −1]] has eigenvalues −1 ± i, so it is a damped oscillation to 0 (checked numerically).
4. **No-anchor exclusion.** With dx/dt = −L[K] x and a strongly connected lifted graph, the limit is either D 1 c (copying in a frame) or 0 (flat). The limit map x(0) ↦ x(∞) has rank ≤ 1. Pure Altafini dynamics therefore produce exactly the two excluded outcomes, copying (after a sign flip) or a flat face, and nothing between.

**On (b) "whose" vs "what".** The gauge is a relabelling of node signs and carries no notion of whose. The lifted index (agent, expression) keeps whose and what apart only as bookkeeping.

**On (c) time scales.** In the balanced case the spectrum of L[K] equals that of the unsigned L[|K|]. There is one zero mode, which is a conserved memory w^T x(0) and so an integrator. The rest are decaying modes with rates from the graph. That gives no anchor and no temperament, only a slow consensus mode plus faster disagreement modes.

**On (d) reading the other through one's own body.** Altafini's model has nothing for this.

**What the design would need.** Requirement (a) forbids "copy after a sign flip". So the design's partner-coupling block must be shown **not gauge-equivalent to a nonnegative matrix**: its lifted sign pattern must contain a negative cycle, or a negative self-loop, which no gauge can remove. The design must also escape the "imbalanced ⇒ 0" collapse. That requires an input or anchor term (Friedkin-Johnsen style; see parsegov-2017-multidimensional-friedkin-johnsen.md) or a nonlinearity.

The theorem to prove would be roughly:

> For the design's coupling K and anchor, the steady-state map u_B ↦ x_A* is (i) not of the form D_A |T| D_B, i.e. not a nonnegative map conjugated by diagonal sign matrices, and (ii) not identically zero.

Lemma G turns (i) into a checkable cycle-sign test on the lifted graph.

## Verdict

Adopt, as a lemma and a test rather than as the mechanism. The gauge lemma (D K D ≥ 0 ⇔ balanced) is the exact tool for proving that a signed per-expression coupling is, or is not, merely copying in a flipped frame. The model alone yields only "copy in a frame" or "flat", which are the excluded outcomes.
