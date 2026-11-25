# Parsegov, Proskurnikov, Tempo & Friedkin 2017: Novel Multidimensional Models of Opinion Dynamics in Social Networks

## Citation

- S. E. Parsegov, A. V. Proskurnikov, R. Tempo, N. E. Friedkin. "Novel Multidimensional Models of Opinion Dynamics in Social Networks." *IEEE Transactions on Automatic Control* 62(5), 2017. arXiv 1505.04920 (v5, 9 Sep 2016).
- Folded in for the scalar Friedkin-Johnsen (FJ) model and the DeGroot consensus background: A. V. Proskurnikov, R. Tempo. "A Tutorial on Modeling and Analysis of Dynamic Social Networks. Part I." *Annual Reviews in Control* 2017. arXiv 1701.06307 (v2). The v2 PDF header misprints "Part II", but the abstract says "first part". Below: "P&T-I".
- The original FJ papers (Friedkin & Johnsen 1990, 1999, and the 2011 book) were **not read**. I did not look for open copies, so every FJ claim below is "as reported by" Parsegov et al. or P&T-I.

## What was read

**Parsegov et al., read in full:**
- sections I-V: the scalar FJ model, Theorem 1, Corollaries 1-2, the multidimensional model, Theorems 2-3, Remarks 1-3, Examples 1-5;
- section IX, all proofs: Lemmas 2-4 and the proofs of Theorems 1-4.

**Parsegov et al., partly read:**
- section VI (gossip version): the Theorem 4 statement was read, but its proof leans on their ref. [22], which was not read;
- section VII (numerics): skimmed, including the footnote on DeGroot with C ≠ I;
- section VIII (estimating C by convex QP): skimmed.

**Not available:** the Appendix that proves eq. (12), lim A^k = lim_{α→1} (1−α)(I − αA)^{-1}, is referred to in the text but is not in the arXiv v5 text I extracted.

**P&T-I:** read in full:
- section 3.1 and 3.3-3.4: the DeGroot model, Lemma 9, Lemma 10, Corollary 13 and Theorem 12, i.e. the consensus criteria;
- section 6 and 6.1: the FJ model, Theorem 21 with its proof sketch, and Corollaries 22-23.

Other sections of P&T-I were not read.

**Checked numerically.** I reproduced the paper's Examples 3-5 and the DeGroot limits in Fig. 6 with numpy: final opinions (16), (19), the x'_{C2} vector of Example 5, and [25,...] and [65,−65,...] for Λ = I.

## The object, exactly

**Scalar FJ model** (Parsegov eq. 1):

    x(k+1) = Λ W x(k) + (I − Λ) u,   x(0) = u,   k = 0, 1, ...

The symbols:
- x(k) in R^n: the agents' opinions.
- W in R^{n×n}: row-stochastic (w_ij ≥ 0, Σ_j w_ij = 1), the interpersonal influence weights. G[W] has an arc (i,j) iff w_ij > 0.
- Λ = diag(λ_11..λ_nn): susceptibilities, 0 ≤ λ_ii ≤ 1.
- u in R^n: prejudices, by convention equal to the initial opinions.

The agent types:
- Agent i is **stubborn** if λ_ii < 1, and **totally stubborn** if λ_ii = 0.
- Agent i is **oblivious** if it is neither stubborn nor reachable by a walk in G[W] from a stubborn agent. P&T-I call these agents "P-independent".
- The common special case is the "coupling condition" Λ = I − diag W.
- Λ = I is DeGroot's iterative pooling, x(k+1) = W x(k). P&T-I write "Λ = 0" at one point, a typo; their later text says Λ = I_n.

**Multidimensional FJ with issue interdependence** (Parsegov eq. 17):
- Each agent holds x_i(k) in R^m, its opinions on m issues.
- C in R^{m×m} is the "matrix of multi-issues dependence structure" (MiDS). It may be signed, and it is the same for all agents.

The per-agent update:

    x_i(k+1) = λ_ii C Σ_j w_ij x_j(k) + (1 − λ_ii) u_i

Stacked over agents (Parsegov eq. 22, where the printed equation drops the final u):

    x(k+1) = [(Λ W) ⊗ C] x(k) + [(I_n − Λ) ⊗ I_m] u

C acts *after* the social averaging, so it also acts on the agent's own self-weighted term w_ii x_i. The paper's reading: c_pq is "a contribution of the qth issue of the leader's opinion to the pth issue of the follower's one". On C itself: "the MiDS matrix should be independent of the social network itself, depending on introspective processes, forming an individual's belief system". C = I_m gives m independent copies of scalar FJ (eq. 14).

**Gossip version** (eq. 28). At each step one sampled arc (i,j) gives:

    x_i ← (1 − γ1_ij − γ2_ij) x_i + γ1_ij C x_j + γ2_ij u_i

## The key property and its proof, step by step

**Theorem 1 (scalar FJ).** Number the agents so that the oblivious ones are n'+1..n. This gives the block forms W = [[W11, W12], [0, W22]] and Λ = diag(Λ11, I).
- (i) Λ11 W11 is Schur stable.
- (ii) The model is stable (ρ(ΛW) < 1) iff there are no oblivious agents.
- (iii) With oblivious agents, it converges iff W22 is regular, i.e. lim (W22)^k exists.

In the stable case:

    x' = (I − ΛW)^{-1} (I − Λ) u

**Corollary 1.** If G[W] is strongly connected and Λ ≠ I, the model is stable.

**P&T-I Theorem 21 adds:** V = (I − Λ11 W11)^{-1} [I − Λ11, Λ11 W12] is row-stochastic. So every final opinion is a **convex combination** of prejudices and the final opinions of oblivious agents.

**Proof of Theorem 1** (Parsegov section IX, checked):

1. **Substochastic, Lemma 2 part 1.** A = ΛW is nonnegative with row sums ≤ 1, so ρ(A) ≤ 1 by Gershgorin. If ρ(A) = 1:
   - Perron-Frobenius gives v ≥ 0 with A v = v; scale it so that max v_i = 1.
   - Let J = {i : v_i = 1}. For i in J: 1 = Σ_{j in J} a_ij + Σ_{j not in J} a_ij v_j ≤ Σ_j a_ij ≤ 1.
   - Since v_j < 1 off J, equality forces a_ij = 0 for j not in J and Σ_{j in J} a_ij = 1. So J is a "stochastic subset".
2. **Lemma 2 part 2.** A union of stochastic subsets is stochastic, so a maximal one J* exists. Permuting J* to the end gives A = [[A11, A12], [0, A22]] with A22 stochastic. If ρ(A11) were 1, step 1 applied to A11 would give a further stochastic subset, contradicting maximality. So ρ(A11) < 1.
3. **Lemma 3.** For A = ΛW, J* is exactly the set of oblivious agents:
   - For i in J*: 1 = Σ_{J*} λ_ii w_ij ≤ λ_ii, so λ_ii = 1, and no arc leaves J*. So agents in J* are oblivious.
   - Conversely, the oblivious agents have λ = 1 and receive no arcs from the rest, so they form a stochastic set. Hence they lie in J*.
4. **Theorem 1.** Steps 2-3 give (i).
   - The oblivious block obeys DeGroot dynamics x2(k+1) = W22 x2(k), so convergence needs W22 regular.
   - Given that, x1(k+1) = Λ11 W11 x1(k) + Λ11 W12 x2(k) + (I − Λ11) u1 converges because Λ11 W11 is Schur stable.
   - With no oblivious agents, A = A11 is Schur stable, which is (ii).
5. **P&T-I's proof that V is stochastic.**
   - V 1 = 1 follows by direct computation.
   - V ≥ 0 because I − Λ11 W11 is a nonsingular M-matrix, whose inverse is nonnegative (P&T-I Lemma 7).

**Theorem 2 (multidimensional stability).** ΛW ⊗ C is Schur stable iff ρ(ΛW) ρ(C) < 1. Then:

    x'_C = (I_mn − ΛW ⊗ C)^{-1} [(I_n − Λ) ⊗ I_m] u

If ρ(C) = 1, stability is equivalent to stability of the scalar FJ model.

The proof is one step: spec(A ⊗ B) = {λ_i μ_j} (Lemma 4, a standard Kronecker fact), so ρ(ΛW ⊗ C) = ρ(ΛW) ρ(C). Remark 2 adds that C may have eigenvalues outside the unit circle, as long as ρ(C) < 1/ρ(ΛW).

**Theorem 3 (convergence with oblivious agents, n' < n).** The model converges iff C is regular (C* = lim C^k exists) and either C* = 0 or W22 is regular. The limit is given by the block formula (24), with blocks (Λ11 W12 W22*) ⊗ C C* and W22* ⊗ C*.

The proof uses the block form ΛW ⊗ C = [[Λ11 W11 ⊗ C, Λ11 W12 ⊗ C], [0, W22 ⊗ C]]:
- **Necessity, C regular.** Take z with z W22 = z. Then (z ⊗ I)(W22 ⊗ C)^k = z ⊗ C^k must converge, so C is regular.
- **Necessity, W22 regular.** If ρ(C) = 1, take C z = z; then (W22 ⊗ C)^k (I ⊗ z) must converge, so W22 is regular. The printed expression "(W22)^k ⊗ v" is a typo for (W22)^k ⊗ z.
- **Sufficiency** follows as in Theorem 1.

**Theorem 4 (gossip ergodicity).** Assume ρ(ΛW) < 1 and C row-stochastic, and set Γ1 = ΛW, Γ2 = (I − Λ)W. Then E x(k) → x'_C, and the time average converges to x'_C almost surely and in L^p. The proof reduces to Theorem 1 of their ref. [22], which I did not read. Remark 8 says that allowing negative entries in C "is beyond the scope of this paper", so the gossip result is **not proved for signed C**.

**Where the paper is loose or open.**
- Eq. (22) as printed drops the final u.
- The proof of eq. (12) is said to be in the Appendix, which is absent from the arXiv text.
- The paper names stability under **heterogeneous** per-agent MiDS matrices C_i as an open problem in section X. It reports only numerics on that case.
- The signed-C examples are not new behaviour. Example 5's C2 = [[0.8, −0.2], [−0.3, 0.7]] equals D C1 D, with D = diag(1, −1) and C1 the stochastic matrix of Example 4. I checked numerically that x'_{C2}(u) = (I ⊗ D) x'_{C1}((I ⊗ D) u) holds to the printed precision. The DeGroot limits in Fig. 6 are related the same way: 25 for C1, ±65 for C2, where 65 = 0.6·75 + 0.4·50 uses C1's stationary row (0.6, 0.4) applied to the gauged prejudice of agent 3.

## What it would mean for a dyadic affective core (my inference)

**Mapping.**
- n = 2 agents: A (the engine) and B (the partner).
- x_i in R^m: expression intensities per channel, i.e. action-unit groups.
- W = [[1−w, w], [w, 1−w]] (symmetric case): w is the attention paid to the partner's face.
- Λ = λ I: openness to influence. 1 − λ is the pull of the private anchor u_i, the temperament or baseline face.
- C in R^{m×m}: the per-expression, possibly signed, cross-channel coupling. For example, c_{anger,smile} < 0 is partner smile pushing the engine's anger down.

This meets requirement (a) only as far as the paper's structure allows. The reductions below set the limits.

**Closed form for the symmetric dyad** (my derivation, checked numerically).

1. Change to sum and difference coordinates, s = x_A + x_B and d = x_A − x_B. Since W has eigenvalue 1 on (1, 1) and 1 − 2w on (1, −1):

       s(k+1) = λ C s(k) + (1−λ) s_u
       d(k+1) = λ(1−2w) C d(k) + (1−λ) d_u

2. With ρ(C) < 1/λ, the steady state is:

       x_A* = S u_A + T u_B
       S = ((1−λ)/2) [ (I − λC)^{-1} + (I − λ(1−2w)C)^{-1} ]
       T = ((1−λ)/2) [ (I − λC)^{-1} − (I − λ(1−2w)C)^{-1} ]

3. T is a rational function of C. It therefore commutes with C and acts on each eigenvector of C with gain:

       t(μ) = (1−λ) w λ μ / [ (1 − λμ)(1 − λ(1−2w)μ) ]

   For real μ with |λμ| < 1 both factors in the denominator are positive. So **sign t(μ) = sign μ**.

**Exact reductions to excluded mechanisms.**

1. **Single scalar gain.** If C = c I_m and Λ = λ I, then T = t(c) I and S = s(c) I. The partner influence on every expression is one number t(c), set jointly by (λ, w, c): exactly the excluded "gain from flat to copy". Example: λ = 0.6, c = 0.9, w = 0.3 gives T = 0.18 I and S = 0.69 I.
2. **Copying.** Take λ_A = 1, w_AA = 0, B totally stubborn (λ_B = 0) and C = I. Then x_A(k+1) = u_B: a pure copy. With general C, x_A = C u_B, i.e. copy through C.
3. **Mean face.** If Λ = I (DeGroot) and C = I, then for any primitive W both faces converge to one common face, the left-Perron-weighted mean of the initial faces (P&T-I Lemma 10, Corollary 13). If C is stochastic and regular, Fig. 6b shows that even all channels collapse to a single number.

   Both REACT failure modes are therefore corners of this model: copy is (λ_A = 1, w_AA = 0, C = I), and mean face is (Λ = I, C = I).
4. **Sign flips that are only copying in a frame.** If some D_C = diag(±1) gives D_C C D_C ≥ 0, then (I ⊗ D_C)(ΛW ⊗ C)(I ⊗ D_C) = ΛW ⊗ |C|. So the whole trajectory is the nonnegative model's trajectory in a flipped frame (see altafini-2013-signed-consensus.md, Lemma G). That covers any counter-mimicry pattern whose signs are balanced across channels; the paper's own Example 5 is one.
5. **Genuine sign flip only with a side effect.** A negative eigenvalue μ of C does give t(μ) < 0 on that mode. But C also multiplies the self-retention term w_AA x_A, so the same mode's own dynamics have a negative eigenvalue λμ, and the engine's own face alternates sign step to step on that mode. In this model, "counter-mimic the partner" cannot be separated from "flip my own expression".

**On (b) "whose" vs "what".** The Kronecker factorization ΛW ⊗ C keeps who-influences-whom (W) separate from what-maps-to-what (C). That is a clean formal version of (b). But the factorization forces the same C on one's own face and the partner's, and that is exactly why reduction 5 bites.

The fix is a per-pair block model:

    x_A(k+1) = λ_A (w_AA P_A x_A(k) + w_AB Q_A x_B(k)) + (1 − λ_A) u_A

Here P_A is self-retention and Q_A is the partner map, and both may be learned per partner. This is no longer a Kronecker product, so Theorem 2 does not apply. It contains the paper's open heterogeneous-C problem as a special case.

A sufficient stability condition (mine, by contraction in an induced norm):

    max_i λ_i (w_ii ||P_i|| + w_ij ||Q_i||) < 1

**On (c) time scales.** The spectrum is {λ_k(ΛW) μ_l(C)}, giving time constants τ = −1/ln|λ_k μ_l|. For the dyad that is 2m modes:
- the shared (sum) modes λ μ_l, which are slow;
- the difference modes λ(1−2w) μ_l, which are faster.

The anchor u is an infinite-time-scale term (temperament), but it is fixed: FJ has no learning, and no reflex scale below one step. The time scales do come from structure, but only as two families.

**On (d) reading the other through one's own body.** C is "introspective": the partner's face enters only as C x_B, passed through the agent's own cross-channel structure. This is a weak, linear form of (d), with no body state.

**On learned partner history.** C is fixed in the dynamics. Section VIII estimates C from observed trajectories by a convex QP, and this could be run per partner as the learned part. That use is my inference.

**What the design would need.** For the per-pair block model with (P_A, Q_A, Λ, W, u), prove all of the following:
- (i) stability, by the condition above or a sharper one;
- (ii) the steady-state partner transfer T_A = ∂x_A*/∂u_B is not t·I (no scalar gain);
- (iii) T_A is not D |T| D' for diagonal sign matrices D, D' (no copying in a frame), i.e. its lifted sign pattern has a negative cycle;
- (iv) the engine's own retention P_A stays sign-preserving, so counter-mimicry is not bought with self-oscillation.

In the Kronecker model with C diagonalizable, (ii) holds iff t is not constant on spec(C). That generically holds when C ≠ cI, but there are non-generic exceptions. (iii) fails whenever C's sign pattern is balanced.

## Verdict

Adopt, as the linear baseline and the reduction test. Two parts carry over: (W ⊗ C) with an anchor is the right shape for "whose ⊗ what", and its closed form shows exactly when the model collapses to a scalar gain, a copy, or a mean face. Its single shared C cannot give counter-mimicry without self-flipping, so the core needs separate self and partner maps.
