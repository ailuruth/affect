# Desai et al. 2021, Zhong et al. 2020, and Neary & Topcu 2023: Port-Hamiltonian Neural Networks

## Citation

Three papers were read, because the preferred one is thin on theory.
- **Desai 2021.** S. A. Desai, M. Mattheakis, D. Sondak, P. Protopapas, S. J. Roberts. "Port-Hamiltonian neural networks for learning explicit time-dependent dynamical systems." arXiv 2107.08024, version v1 (16 Jul 2021), cs.LG. Preprint dated July 19, 2021.
- **Zhong 2020.** Y. D. Zhong, B. Dey, A. Chakraborty. "Dissipative SymODEN: Encoding Hamiltonian Dynamics with Dissipation and Control into Deep Learning." ICLR 2020 Workshop on Integration of Deep Neural Models and Differential Equations (DeepDiffEq). arXiv 2002.08860, version v3 (30 Apr 2020).
- **Neary & Topcu 2023.** C. Neary, U. Topcu. "Compositional Learning of Dynamical System Models Using Port-Hamiltonian Neural Networks." Proceedings of Machine Learning Research vol. 211 (5th Annual Conference on Learning for Dynamics and Control, L4DC 2023). arXiv 2212.00893, version v2 (13 May 2023). Code: github.com/cyrusneary/compositional_port_hamiltonian_NNs.

Neary & Topcu is the paper that states the power-balance inequality and composes port-Hamiltonian systems, so the theory below rests on it. Desai is the assigned paper and is described for what it does.

## What was read

All three via arXiv PDF and `pdftotext -layout`.

**Desai 2021.**
- Read in full: abstract; sections I-III (background on HNN and the port-Hamiltonian framework, Eq. 3; the method, Eq. 4-5; testing metrics, Eq. 6-7); section V (discussion, including the identifiability remark); section VI (conclusion); Appendix A (λ grid search); Appendix B (pipeline); Appendix C (why damping cannot go into a Hamiltonian).
- Skimmed: section IV results (mass-spring, damped, forced, Duffing, relativistic Duffing), for setup and headline claims.
- Not read: Appendices D-F beyond their first figure; the noise study and the coupled-spring appendix experiment.

**Zhong 2020.** The whole paper (5 pages): section 2 (port-Hamiltonian dynamics, including the one-line conservation proof), section 3 (architecture, PSD parametrization), section 4 (tasks, Table 1).

**Neary & Topcu 2023.**
- Read in full: sections 1-5 (PH systems, Eq. 1; the running example, Eq. 2; PHNN construction, including the cyclo-passivity statement; composition, sections 5.1-5.2, Eq. 4; Theorem 1); Appendix A (proof of Theorem 1, step by step); Appendix B (composite matrices, Eq. 21; network details).
- Skimmed: section 6 experiments (6.1-6.3, Fig. 4-7).
- Also read: section 7 (conclusions; no limitation section beyond it).

**Not read in the original and cited only as these papers report them:** van der Schaft 2000 (*L2-gain and passivity techniques in nonlinear control*); van der Schaft et al. 2014; Duindam et al. 2009; Ortega et al. 2002. The interconnection theorem below is my derivation, marked as such. None of the three papers states it in input-output form.

## The object, exactly

### General form (Neary & Topcu Eq. 1)

ẋ = [J(x) − R(x)] ∇_x H(x) + G(x) u,   y = G(x)^T ∇_x H(x)

The symbols:
- x ∈ R^n: state.
- H : R^n → R: the Hamiltonian (energy). It is learned, as an MLP H_θ.
- J(x) ∈ R^{n×n}: skew-symmetric for every x (J = −J^T), the "interconnection matrix". It encodes energy-conserving internal exchange. Neary assumes J is known a priori, as do all prior PHNN papers by their account.
- R(x) ∈ R^{n×n}: symmetric positive semidefinite, the "dissipation matrix". It is learned as R_θ(x) = L_θ(x) L_θ(x)^T with L_θ lower-triangular with non-negative diagonal. Zhong does the same and adds ε to the diagonal of M^{-1}.
- G(x) ∈ R^{n×m}: input (port) matrix, learned (constant or an MLP).
- u ∈ R^m: input.
- y ∈ R^m: the collocated output (power-conjugate to u, so y^T u is power).

Training (Neary Eq. 3): integrate with fixed-step RK4 over [t_i, t_{i+1}] and minimize Σ ‖PHNN_Θ(x_i, u_i, t_i, t_{i+1}) − x_{i+1}‖² over trajectories. Neary uses no derivative targets; Desai uses derivative targets.

### Composition (Neary section 5.1)

For subsystems i = 1..k with states x_i ∈ R^{n_i}:
- composite state x_c = (x_1, ..., x_k);
- composite Hamiltonian H_c(x_c) = Σ_i H_i(x_i), with each H_i depending only on x_i (stated assumption);
- R_c = Diag(R_i), G_c = Diag(G_i);
- J_c = Diag(J_i) + C(x_c), where C is skew-symmetric with zero diagonal blocks (the "composition matrix").

C is either known, learned by least squares from a few composite transitions (Eq. 4, when C is constant), or given by a network C_φ(x_c).

Running example (Appendix B, Eq. 21): two spring-mass-dampers, x_i = (Δq_i, p_i), H_i = p_i²/(2m_i) + k_i Δq_i²/2, nonlinear damping R_i = diag(0, b_i p_i²/m_i²), G_i = (0, 1)^T. The coupling block of J_c is C_12 = [[0, 0], [1, 0]], C_21 = −C_12^T.

### Desai's special case (Eq. 4)

x = (q, p):

(q̇, ṗ) = ([[0, I], [−I, 0]] + [[0, 0], [0, N]]) (∂H/∂q, ∂H/∂p) + (0, F(t))

- H_θ1(q, p): an MLP for the stationary Hamiltonian.
- N_θ3: a single learned scalar weight.
- F_θ2(t): an MLP of time only.
- Loss (Eq. 5): ‖q̇̂ − q̇‖² + ‖ṗ̂ − ṗ‖² + λ_F ‖F̂‖_1 + λ_N ‖N̂‖_1, with targets the true derivatives.

Desai's "port" is a learned time signal F(t). No output y is defined and nothing is interconnected.

### Zhong's case (Eq. 3, 5-6)

- J canonical, damping term −D(q) with D ⪰ 0, input g(q) u, u held constant per trajectory.
- H = ½ p^T M^{-1}(q) p + V(q), with four networks for M^{-1}, V, g and D.

## The key property and its proof, step by step

### Theorem A: power balance and cyclo-passivity

Neary states this in one line, citing van der Schaft 2000:

> "dH/dt = h^T J(x) h − h^T R_θ(x) h + h^T G_θ(x) u ≤ y^T u",

with h = ∇H_θ. Neary also says "the rate of change of the system's energy cannot exceed the externally-provided power", and that this holds "regardless of the output of the parametrized Hamiltonian" because J is skew and R_θ is PSD by construction.

Hypotheses: H ∈ C¹; J(x) skew and R(x) symmetric PSD for every x; x(t) a solution for a given input u(t).

Proof (mine; each step checkable):
1. Chain rule: dH/dt = h^T ẋ with h = ∇H(x).
2. Substitute: dH/dt = h^T J h − h^T R h + h^T G u.
3. h^T J h = 0, because J is skew: a scalar equals its transpose, so h^T J h = h^T J^T h = −h^T J h.
4. h^T G u = (G^T h)^T u = y^T u.
5. **Power-balance identity:** dH/dt = −h^T R h + y^T u.
6. R ⪰ 0 gives h^T R h ≥ 0, so dH/dt ≤ y^T u.
7. Integrate over [0, t]: H(x(t)) − H(x(0)) ≤ ∫_0^t y^T u ds. This is cyclo-passivity.
8. If H is also bounded below (H ≥ 0 after a shift), H is a storage function and the system is passive.

Neary says "cyclo-passivity" because an MLP H_θ need not be bounded below.

**Conservative case (Zhong section 2).** "Ḣ = (∂H/∂q)^T q̇ + (∂H/∂p)^T ṗ = 0" when R = 0 and u = 0.

### Theorem B: composition preserves the structure

Neary: "the interconnection and dissipation terms of the composite model retain their properties of skew-symmetry and positive semidefiniteness, respectively."

Proof:
1. A block-diagonal matrix of skew blocks is skew; a skew C added to it keeps it skew.
2. A block-diagonal matrix of PSD blocks is PSD.
3. Apply Theorem A to (H_c, J_c, R_c, G_c): dH_c/dt ≤ y_c^T u_c, with H_c = Σ H_i.

Neary shows this empirically too: Fig. 6 plots dH_c,θ/dt ≤ 0 along a learned composite trajectory with no input. It already follows from the construction.

### Theorem C (Neary Theorem 1): error bound for a composite model

Hypotheses:
- the true subsystems are port-Hamiltonian;
- ‖P_i − P_i,Θ‖ ≤ ε_i on Ω_xi × Ω_ui;
- ‖∇H_i − ∇H_i,θ‖ ≤ η_i;
- ‖(C − C_φ)_{ij} ∇H_j‖ ≤ γ_ij (the extraction shows the hypothesis without a norm, apparently a typo);
- σ_ij = max ‖C_φ,ij‖.

Claim: ‖P_c − P_c,Θ‖ ≤ Σ_i ε_i + 2 Σ_{j>i} (γ_ij + σ_ij η_j).

Proof steps (Appendix A):
1. Triangle inequality, splitting off the C term.
2. The block-diagonal structure separates the subsystems.
3. (∇H_c)_{I_i} = ∇H_i because H_c is separable (Eq. 11).
4. Add and subtract C_φ ∇H_c (Eq. 15).
5. Bound by blocks (Eq. 16-19).

**Where the paper is loose:**
- **Step 16 to 18 is not valid as written.** It replaces the sum over ordered pairs i ≠ j by 2 Σ_{j>i}. That is valid only if γ_ij = γ_ji and σ_ij η_j = σ_ji η_i. Skewness of C_φ gives σ_ij = σ_ji, but η_j ≠ η_i in general. The bound that follows from their steps is Σ_i ε_i + Σ_{i≠j} (γ_ij + σ_ij η_j).
- **Sign typo in Eq. 8:** "+ R_c,θ" should be "− R_c,θ".
- **The theorem bounds the vector-field error pointwise, not the trajectory error.** There is no Grönwall step, so rollout error can still grow exponentially in time.
- **Cyclo-passivity is stated, not proved.** The proof is the five lines above.

**Desai's looseness:**
- **The dissipation sign is inconsistent.** Eq. 3 adds "+ D(q)" with D called "semi-positive definite". Under Theorem A this would give dH/dt = +h^T D h ≥ 0, an energy source. In Eq. 4 the damping is a free scalar N, not constrained in sign, so dissipativity is not enforced.
- **F(t) is not a port.** It has no conjugate output, so no passivity statement can be made.
- **H and F are not identifiable.** The authors: "it is possible to learn a shifted force i.e. F = F0 + ε... resulting in a leak of information between H and F". In the damped mass-spring case the pHNN "learns a non-zero oscillating force".
- **Appendix C's argument is informal.** It shows one attempt to put damping into H failing, not that it is impossible.

**Zhong's looseness.**
- The learned D does not match the true D in Task 1 ("does not match the ground truth"); it matches better with angle-aware inputs (Task 2).
- Results are a single table with large standard deviations, e.g. Task 1 prediction error 34.03 ± 47.83.

### Theorem D (my derivation): power-conserving interconnection of two passive PH systems

Neary's composition with a skew C is the state-space form of this. Neither paper writes it in port form.

Setup:
- Σ_A = (H_A, J_A, R_A, G_A) and Σ_B = (H_B, J_B, R_B, G_B), each with m-dimensional ports.
- Interconnect with a matrix K ∈ R^{m×m} and external inputs v_A, v_B:
  u_A = −K y_B + v_A,   u_B = K^T y_A + v_B.

Claim: the closed loop is port-Hamiltonian with
- H_c = H_A + H_B;
- R_c = diag(R_A, R_B) ⪰ 0;
- J_c = diag(J_A, J_B) + C, where C_AB = −G_A K G_B^T, C_BA = G_B K^T G_A^T and C_AA = C_BB = 0;
- G_c = diag(G_A, G_B), with input v and output y_c = (y_A, y_B).

So dH_c/dt = −h_A^T R_A h_A − h_B^T R_B h_B + y_A^T v_A + y_B^T v_B ≤ y_c^T v.

Proof:
1. G_A u_A = −G_A K G_B^T h_B + G_A v_A and G_B u_B = G_B K^T G_A^T h_A + G_B v_B, using y = G^T h.
2. Collect terms: ẋ_c = (diag(J_A, J_B) + C − R_c) h_c + G_c v, with h_c = ∇H_c = (h_A, h_B) because H_c is separable.
3. C is skew: C_BA = G_B K^T G_A^T = −(−G_A K G_B^T)^T = −C_AB^T, and the diagonal blocks are 0.
4. The interconnection supplies zero power: y_A^T(−K y_B) + y_B^T(K^T y_A) = −y_A^T K y_B + y_A^T K y_B = 0.
5. Apply Theorem A to the closed loop.

If H_A, H_B ≥ 0, the interconnection is passive with storage H_A + H_B. With v = 0, H_A + H_B is non-increasing, so it is a Lyapunov function.

**General linear interconnection (my derivation).** Stack y = (y_A, y_B) and set u = −K_full y + v. Split K_full = K_s + K_k (symmetric and skew parts).
- The power absorbed by the interconnection is y^T K_full y = y^T K_s y; the skew part contributes nothing.
- So dH_c/dt = −diss − y^T K_s y + y^T v.
- The interconnection is lossless iff K_s = 0, and passive (non-generating) iff K_s ⪰ 0.
- **Lossless requires reciprocity.** With u_A = −K_AB y_B and u_B = −K_BA y_A, losslessness for all y requires K_BA = −K_AB^T. Whatever A does with B's output, B must do the negative transpose with A's.

## What it would mean for a dyadic affective core

My inference throughout, with derivations marked.

### Mapping onto (a)-(d)

**The agent.** Σ_A with state x_A = (e_A, b_A, z_A):
- e_A: expression coordinates (AU channels, m of them);
- b_A: body/interoceptive coordinates;
- z_A: slow relational state per partner.

H_A(x_A) is the agent's own body energy, which is (d). J_A is a skew coupling inside the agent between expression, body and relation. R_A ⪰ 0 is dissipation.

**The partner's expression enters through a port.** u_A = K(z_A) ŷ_B, where:
- ŷ_B ∈ R^m is the partner's expression mapped into the agent's port coordinates;
- K(z_A) ∈ R^{m×m} is a per-expression port matrix that depends on the learned partner history z_A.

**(b) Whose vs what.** The state is block-separated and H_c = H_A + H_B is additive. The agent's energy changes only through its own dissipation and the port power:

dH_A/dt = −h_A^T R_A h_A + y_A^T u_A   (Theorem A).

"Whose" is the block index. "What" is the channel index inside the port. The partner can affect the agent only through the scalar power y_A^T u_A.

**(d) Reading the other through one's own body.** The agent models the partner as a PH system with the agent's own H_A, J_A, R_A, G_A (B := a copy of A). It infers x̂_B by matching G_A^T ∇H_A(x̂_B) to the observed partner face. H_A(x̂_B) is then "what that face would cost my body". Theorem D gives the joint energy accounting H_A(x_A) + H_A(x̂_B).

**(c) Time scales.** Linearize around a rest state with H = ½ x^T Q x, Q ≻ 0. Then A_lin = (J − R) Q, which is similar to J' − R' with J' = Q^{1/2} J Q^{1/2} (skew) and R' = Q^{1/2} R Q^{1/2} (PSD).

*Bound (my derivation).* Every eigenvalue λ of A_lin satisfies −λ_max(R') ≤ Re λ ≤ −λ_min(R').
1. Take a unit eigenvector v of J' − R': λ = v*J'v − v*R'v.
2. v*J'v is purely imaginary, because J' is skew.
3. v*R'v is real and lies in [λ_min(R'), λ_max(R')].

Consequence: J cannot create decay rates outside the spectrum of R'. A spread from reflex (about 30 s^-1) to temperament (about 10^-5 s^-1) must be present in R' as a whole.

*How a slow scale arises from structure (my derivation).* Take
- J = [[0, ω], [−ω, 0]], R = diag(r, 0), Q = I.
- The characteristic polynomial is λ² + rλ + ω² = 0.
- For r ≫ ω the roots are λ_fast ≈ −r and λ_slow ≈ −ω²/r.

A fast-dissipating coordinate (an expression channel, r = 30 s^-1) coupled losslessly with weak ω to an undissipated coordinate (a temperament variable) gives a slow time constant τ = r/ω². For ω = 0.03 s^-1, τ ≈ 3.3·10^4 s ≈ 9 h. So the slow scale comes from the lossless coupling, not from a hand-set slow rate. R still has eigenvalues spread from 0 to r, as the bound requires.

**(a) Per-expression, signed, history-dependent influence.**

*Static gain lemma (my derivation).* Take the LTI system with R ≻ 0 and a constant input u. The equilibrium satisfies Q x* = (R − J)^{-1} G u, and R − J is invertible because z^T(R − J)z = z^T R z > 0. The steady output is y* = S u with S = G^T (R − J)^{-1} G.

With w = (R − J)^{-1} G u:

u^T S u = (G u)^T w = ((R − J) w)^T w = w^T R w ≥ 0.

So S has a positive-semidefinite symmetric part, and every diagonal entry S_ii ≥ 0. The skew part of S is nonzero only if J ≠ 0.

Consequences for the agent's steady response y* = S K(z) ŷ_B:
- A passive agent cannot counter-mimic on the same channel through its dynamics. The same-channel sign flip, such as brow relaxation to a rival's frown, must be carried by a negative entry of the port matrix K(z).
- Cross-channel signed responses, such as a smile to anger, can come either from J (the skew part of S) or from off-diagonal entries of K(z).

### When it reduces to an excluded mechanism (precise)

1. **Scalar gain from flat to copy.** Take expression coordinates only, H = ½|e|², J = 0, R = rI, G = I, u = k ŷ_B. Then ė_A = −r e_A + k ŷ_B, a first-order low-pass of the partner's face with steady state e_A = (k/r) ŷ_B. One scalar k/r runs from flat (0) to copy (1). This is the excluded mechanism exactly. More generally, it reduces to a scalar gain whenever K(z) = k(z) M for a fixed M and S M is proportional to I.

2. **Diffusion to consensus.** Take the resistive interconnection u_A = −k(y_A − y_B) and u_B = −k(y_B − y_A), i.e. K_s = k [[I, −I], [−I, I]] = k (Laplacian ⊗ I_m) and K_k = 0. It absorbs power k|y_A − y_B|², so dH_c/dt = −diss − k|y_A − y_B|² ≤ 0. If the sublevel sets of H_c are compact, LaSalle's invariance principle puts every limit point in the largest invariant set inside {R^{1/2} h = 0 and y_A = y_B}. The outputs synchronize, which is copying/consensus. (Standard argument; my sketch, not in the papers.)

   **Mutual copying can be passive only as diffusion.** u_A = c y_B, u_B = c y_A supplies 2c y_A^T y_B, which is sign-indefinite, so it is not passive. Adding self-damping, K_full = [[kI, −cI], [−cI, kI]], is ⪰ 0 iff k ≥ |c|, and at k = c it is exactly diffusion.

3. **The gyrator (lossless, skew) interconnection is not copying.** For identical scalar agents ė = −r e + u with u_A = −κ y_B and u_B = κ y_A, the eigenvalues are −r ± iκ. The two agents settle in quadrature, a rotation and not synchronization. Losslessness forces K_BA = −K_AB^T: if B's smile pushes A toward smiling, A's smile must push B away from smiling. That is a signed, asymmetric relation, which (a) wants. But it holds only inside the agent's internal model of the dyad, since the real partner is not bound by it.

### What passivity proves: a bounded-influence theorem (my derivation)

Hypotheses:
- H_A ≥ 0;
- strict output passivity: R_A ⪰ δ G_A G_A^T for some δ > 0, so h^T R h ≥ δ|y|²;
- ‖K(z)‖ ≤ κ for all z (enforce by spectral normalization).

Then:
- (i) H_A(x(t)) ≤ H_A(x(0)) + (κ²/(4δ)) ∫_0^t |ŷ_B|² ds. Proof: dH/dt ≤ −δ|y|² + |y||u| ≤ |u|²/(4δ).
- (ii) ∫_0^T |y_A|² dt ≤ (κ/δ)² ∫_0^T |ŷ_B|² dt + (2/δ) H_A(x(0)). This is a finite L2 gain κ/δ from the partner's face to the agent's port output. Proof: dH/dt ≤ −(δ/2)|y|² + |u|²/(2δ); integrate and use H(T) ≥ 0.
- (iii) If H_A = ½ x^T Q x and R_A ⪰ ρI ≻ 0, then H_A(t) ≤ e^{−ct} H_A(0) + ‖G‖² κ² sup|ŷ_B|² / (2ρc), with c = ρ λ_min(Q). This is a uniform input-to-state bound. Proof: dH/dt ≤ −(ρ/2)|h|² + |G u|²/(2ρ), |h|² ≥ 2λ_min(Q) H, then Grönwall.

So the partner can move the agent's body energy only by the power the port supplies, and with δ > 0 only by a bounded factor. Note what this does not say: passivity bounds how much, not which direction. It does not exclude copying. It only bounds its amplitude.

### The theorem the design would need, beyond passivity

- **Non-reduction.** The learned map z ↦ K(z) has an image not contained in any line {k M}. In particular, it contains matrices whose diagonals differ in sign pattern, such as K_smile,smile > 0 with K_sad,sad switching sign. The (a) data require this: smile return flat while sadness switches (Bourgeois & Hess 2008), and opposite changes in two channels (Hofman 2012), as summarized in mimicry-context-synthesis.md.
- **Modulation keeps passivity.** If z evolves with its own passive dynamics, the agent-side inequality holds pointwise for any u_A, because it is stated for an arbitrary input. So history dependence costs nothing in the energy bound, provided ‖K(z)‖ ≤ κ.
- **Exclusion.** Exclude the reductions in items 1-2 above by construction: K_k ≠ 0, or a sign-varying K(z), or J_A coupling expression and body. Show that the REACT copy baseline, which corresponds to e_A tracking ŷ_B, is reached only on a measure-zero set of parameters, or is penalized.

## Verdict

**Adopt as the energy-accounting scaffold, not as the source of (a).**

What it gives, proved from the structure for every θ:
- a power-balance identity;
- a bounded-influence theorem (finite L2 gain, ISS bound);
- additive self/other separation;
- a precise test for when coupling is diffusion (a Laplacian K_s) and for when it is lossless (a skew K_k, forced reciprocity).

What it does not give: the per-expression, sign-flipping, history-dependent response. That must be carried by a learned, bounded port matrix K(z) and by J. Passivity makes same-channel counter-mimicry impossible through the dynamics alone.

Desai 2021 itself adds only a learned forcing F(t) and an unconstrained damping scalar. Its theory is thin, and the useful statements come from Neary & Topcu 2023 and the classical theory.
