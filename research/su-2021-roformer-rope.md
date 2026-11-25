# Su, Lu, Pan, Murtadha, Wen & Liu 2021: RoFormer: Enhanced Transformer with Rotary Position Embedding

## Citation

J. Su, Y. Lu, S. Pan, A. Murtadha, B. Wen, Y. Liu. "RoFormer: Enhanced Transformer with Rotary Position Embedding." arXiv preprint, first posted April 2021. arXiv 2104.09864, version read: v5 (8 Nov 2023), the latest. Code: github.com/ZhuiyiTechnology/roformer.

## What was read

PDF from arXiv (v5), text extracted with pdftotext.

- Read in full: abstract; sections 1, 2 (preliminaries, absolute and relative position embeddings), 3 (formulation 3.1, RoPE in 2D and general form 3.2, properties 3.3, theoretical explanation 3.4.1-3.4.3), 4.5.5 (limitations), 5 (conclusion). The paper has no appendix; section 3.4 is the whole of the derivation and proofs.
- Read but not checked: the experiments in section 4 (WMT14 BLEU 27.5 vs 27.3; BERT MLM loss curves; GLUE, where RoFormer is worse than BERT on SST-2, QNLI and MNLI; Performer on Enwik8; Chinese CAIL2019-SCM).
- Not read: the references beyond identifying them.
- I checked every step of 3.4.1 and 3.4.3 by hand, and computed the decay bound of 3.4.3 numerically (pure Python, d = 64 and 128, relative distance 0-2000).

## The object, exactly

Tokens w_i, i = 1..N, with embeddings x_i in R^d (d even). Query, key and value at positions m, n in {1..N} (integers):

    q_m = f_q(x_m, m),   k_n = f_k(x_n, n),   v_n = f_v(x_n, n)                          (Eq. 1)
    a_{m,n} = exp(q_m^T k_n / sqrt(d)) / sum_j exp(q_m^T k_j / sqrt(d)),  o_m = sum_n a_{m,n} v_n   (Eq. 2)

The requirement (Eq. 11): the score depends on positions only through their difference,

    <f_q(x_m, m), f_k(x_n, n)> = g(x_m, x_n, m - n)

for some function g. (Eq. 21 in 3.4.1 writes n - m; the sign convention flips between the two equations. It does not matter.)

The solution proposed (Eq. 14-15). Frequencies Theta = {theta_i = 10000^(-2(i-1)/d), i = 1..d/2}. For an integer m, R^d_{Theta,m} is the d x d block-diagonal matrix with 2x2 blocks

    R(m theta_i) = [[cos m theta_i, -sin m theta_i], [sin m theta_i, cos m theta_i]],  i = 1..d/2,

and

    f_q(x_m, m) = R^d_{Theta,m} W_q x_m,   f_k(x_n, n) = R^d_{Theta,n} W_k x_n,   f_v(x_n, n) = W_v x_n,

with W_q, W_k, W_v in R^{d x d} learned. Values carry no position. In complex form (2D, Eq. 12): identify the pair (q^(1), q^(2)) with the complex number q^(1) + i q^(2); then f_q = (W_q x_m) e^{i m theta}, f_k = (W_k x_n) e^{i n theta}, and

    g(x_m, x_n, m - n) = Re[(W_q x_m)(W_k x_n)^* e^{i(m-n)theta}].

The map m -> R^d_{Theta,m} is a group homomorphism from (Z, +) into SO(d): R_{Theta,m}^T R_{Theta,n} = R_{Theta,n-m}, and R_{Theta,m+n} = R_{Theta,m} R_{Theta,n}. That is the whole object: a representation of the translation group of positions, acting on queries and keys by rotations, with the d/2 planes rotating at geometrically spaced frequencies.

Linear-attention variant (Eq. 19), with non-negative feature maps phi, varphi:

    Attention_m = sum_n (R_{Theta,m} phi(q_m))^T (R_{Theta,n} varphi(k_n)) v_n  /  sum_n phi(q_m)^T varphi(k_n).

## The key property and its proof, step by step

### Property 1 (relative position). This is a theorem, and it is exact.

Statement. For all x_m, x_n in R^d and integers m, n:
(R_{Theta,m} W_q x_m)^T (R_{Theta,n} W_k x_n) = x_m^T W_q^T R_{Theta,n-m} W_k x_n (Eq. 16; the paper drops the transpose on W_q).

Proof.
1. Each block R(m theta_i) is a rotation, so R(m theta_i)^T = R(-m theta_i).
2. Rotations of one plane commute and add angles: R(a) R(b) = R(a + b).
3. Block-diagonal matrices with the same block structure multiply blockwise, so R_{Theta,m}^T R_{Theta,n} = blockdiag(R((n - m) theta_i)) = R_{Theta,n-m}.
4. Substitute into the inner product. The score therefore depends on (x_m, x_n, n - m) only. QED.

This holds for real-valued positions as well, since step 2 holds for any real angles. That matters for continuous time stamps (my remark; the paper uses integers).

### Property 2 (the derivation in 3.4.1). It exhibits a solution. It does not prove uniqueness.

The paper's claim (3.2.1) is that it will "prove ... that a solution to our formulation Equation (11) is" Eq. 12. The derivation, in the paper's steps, with my check of each:

1. d = 2. Write f_q(x_q, m) = R_q(x_q, m) e^{i Theta_q(x_q, m)}, f_k similarly, and g = R_g e^{i Theta_g} (Eq. 23). Initial condition (Eq. 22): f_q(x_q, 0) = q, f_k(x_k, 0) = k.
2. Eq. 24 equates moduli, R_q(x_q, m) R_k(x_k, n) = R_g(x_q, x_k, n - m), and angles, Theta_k(x_k, n) - Theta_q(x_q, m) = Theta_g(x_q, x_k, n - m).
   **Loose.** The requirement is on the real inner product, which is Re[conj(f_q) f_k]. Equating modulus and angle requires the full complex number conj(f_q) f_k to depend only on n - m, that is, the dot product and the 2D cross product together. The derivation therefore solves a stronger condition than Eq. 11. Under the real-only condition there are solutions outside the paper's family. Example: f_q(x, m) = diag(e^{lambda_1 m}, e^{lambda_2 m}) q and f_k(x, n) = diag(e^{-lambda_1 n}, e^{-lambda_2 n}) k give q^T diag(e^{-lambda_1 (n-m)}, e^{-lambda_2 (n-m)}) k, a function of n - m. This is not a rotation and not a complex scalar.
3. Set m = n (Eq. 26a): R_q(x_q, m) R_k(x_k, m) = ||q|| ||k||. The paper then writes "a straightforward solution of R_f could be formed": R_q(x_q, m) = ||q||, R_k = ||k||.
   **A choice, not a deduction.** The general solution of 26a together with 24 is R_q(x_q, m) = ||q|| c(m), R_k(x_k, n) = ||k|| / c(n), with c(m)/c(n) a function of m - n. On the integers, with c(0) = 1, that forces c(m) = e^{lambda m} for a real lambda. So, even for the stronger complex condition, the solution is f_q = q e^{(lambda + i theta) m}, f_k = k e^{(-lambda + i theta) n}. The modulus is not forced to be position-free. The paper's solution is the case lambda = 0.
4. Eq. 26b gives Theta_q(x_q, m) - theta_q = Theta_k(x_k, m) - theta_k for all x_q, x_k. The left side depends only on x_q and the right side only on x_k, so both equal a function phi(m). **Valid** (mod 2 pi).
5. Set n = m + 1 (Eq. 29): phi(m + 1) - phi(m) = Theta_g(x_q, x_k, 1) + theta_q - theta_k, a constant. Hence phi(m) = m theta + gamma (Eq. 30). **Valid on the integers.** For real positions one needs a regularity assumption, such as continuity, to solve the Cauchy equation. The initial condition actually forces gamma = 0, which the paper instead sets by choice. "theta is non-zero" is also a choice: theta = 0 is a solution with no position information.
6. Eq. 32-33 set q = W_q x_m, k = W_k x_n, giving Eq. 12. For d > 2, 3.2.2 simply stacks d/2 independent 2D copies "in the merit of the linearity of the inner product". This is a construction: no argument is given that the general d-dimensional solution is block-diagonal.

What can be proved (my derivation, not in the paper). Restrict to position maps linear in content: f_q(x, m) = A_m W_q x, f_k(x, n) = B_n W_k x, with A_0 = B_0 = I. Require Eq. 11 for all contents. Then:
- (a) Polarization gives A_m^T B_n = C(n - m) for a matrix function C.
- (b) Setting m = 0 gives B_n = C(n). Setting n = 0 gives A_m^T = C(-m). So C(-m) C(n) = C(n - m) for all m, n.
- (c) Hence C(n) = M^n with M = C(1) any invertible matrix, B_n = M^n and A_m = (M^{-m})^T. The solution set is the whole group GL(d), not a rotation.
- (d) If one also demands the same operator on queries and keys (A_m = B_m, as RoPE has), then m = n gives A_m^T A_m = I. So M is orthogonal, and by the real normal form M = P^T blockdiag(R(theta_1), ..., R(theta_j), +-1, ...) P with P orthogonal.
- (e) P can be absorbed into W_q and W_k. So, within this class, RoPE is unique up to the choice of frequencies, where eigenvalues +-1 are the frequencies 0 and pi.

The two hypotheses that do the work are linearity in content and the shared operator. Drop the shared operator and one gets per-plane decaying rotations M = e^{-lambda} R(theta), or plain exponential scalings.

### Property 3 (long-term decay). Only an upper bound is proved, and the decay of the bound is shown by a plot, not proved.

Steps (3.4.3):
1. Group q = W_q x_m and k = W_k x_n into complex pairs. Then the score equals Re[sum_{i=0}^{d/2-1} h_i e^{i(m-n)theta_i}] with h_i = q_[2i:2i+1] k^*_[2i:2i+1] (Eq. 35). **Correct.**
2. Set S_j = sum_{i<j} e^{i(m-n)theta_i}, S_0 = 0, h_{d/2} = 0. Abel summation gives sum_i h_i (S_{i+1} - S_i) = -sum_i S_{i+1}(h_{i+1} - h_i) (Eq. 36). **I checked it: correct.**
3. Triangle inequality: |score| <= max_i |h_{i+1} - h_i| * sum_i |S_{i+1}| (Eq. 37). **Correct.**
4. "the value of (1/(d/2)) sum |S_i| decay[s] with the relative distance", shown in Figure 2 only. **Not proved.**
   - It is not monotone. In my computation with this Theta, it increases at about half of all unit steps: 974 of 2000 for d = 64, 988 of 2000 for d = 128.
   - It decays on average: for d = 128 it is 32.5 at distance 0, 12.6 at 50, 6.6 at 250, and between 2.8 and 11.2 over distances 200-2000.
   - The factor max |h_{i+1} - h_i| depends on content and is unbounded. So the bound says nothing uniform about the score itself.
   - The score of a fixed q, k pair need not decay at all: with d = 2 it is periodic in m - n.
   - The paper's own limitations paragraph says "we have not come up with a faithful explanation" for the long-text gains.

### Property 4 (linear attention). An algebraic identity, with a caveat.

Since (R_m phi(q))^T (R_n varphi(k)) = phi(q)^T R_{n-m} varphi(k), the numerator of Eq. 19 can be computed as (R_m phi(q_m))^T [sum_n R_n varphi(k_n) v_n^T]. The bracket can be accumulated once, so linear cost is kept. That part is exact.

The caveat is stated by the paper: the denominator is left unrotated "to avoid the risk of dividing zero". The weights are then "not strictly probabilistic normalized" and can be negative. Only the empirical Performer curve supports it.

## What it would mean for a dyadic affective core

All of this section is my inference.

**Mapping.** Tokens are 30 Hz frames, each carrying a source label s in {self, other} and a per-expression vector:
- the agent's own body or expression state, for s = self;
- the partner's action units mapped into the agent's body coordinates, for s = other.

RoPE gives the attention score a property that only relative time matters. That suits (c) and a 30 Hz stream. Positions can be real time stamps (Property 1 holds for real m, n), so dropped frames do not break it.

**Carrying "whose" like position, for (b).** Treat the source as a second coordinate with its own rotation:
- Score blocks i get an extra R(psi_i) when the query is self and the key is other.
- Time rotations and source rotations act in the same planes and commute, so the score depends only on (content, relative time, relative source).
- "Whose" is then relational, as in Lowe et al.: a global relabelling does not matter.
- If psi_i varies across planes and the planes are aligned with expression groups, the partner's frames are scored differently per expression. psi_i = pi flips the sign of that plane's contribution to the score.
- Make psi_i = psi_i(h), a function of the learned partner history h. Time-relativity survives, because R(psi_i(h)) still commutes with R(m theta_i).

**Where it reduces to an excluded mechanism.** The exact statement, for one attention layer: the output at frame t is sum_h W_O^h sum_j a^h_{tj} W_V^h x_j. Split j into self and other frames and write alpha_h = sum_{j in other} a^h_{tj}, which lies in [0, 1]. The partner's contribution is

    sum_h alpha_h M_h xbar^h,   M_h = W_O^h W_V^h (fixed after training),   xbar^h = a convex average of partner frames.

Per frame: holding the attention weights fixed, the derivative of the output with respect to partner frame x_j is sum_h a^h_{tj} M_h, with a^h_{tj} >= 0. The score path adds a further term through d a / d x_j, but that term only redistributes the convex weights over the same vectors M_h x_j'.

So RoPE, and any score-side encoding including a source rotation, can change only which partner frames are averaged and how much mass each head puts on the partner. It cannot change the per-expression map M_h or its sign. The value-path partner-to-self map lies in the cone {sum_h alpha_h M_h, alpha_h >= 0} of H fixed matrices:
- With H = 1 it is exactly a scalar gain on a fixed matrix.
- If M_h = I it is a gain on copying.
- A history-dependent sign flip in one expression is possible only if some fixed M_h already has that sign and the history moves alpha toward that head.

This is the precise sense in which RoPE keeps "whose" out of "what": values carry no position or source. That separation is clean for (b), but it means (a) cannot come from the position code. The per-expression, signed, history-dependent map has to live in the value path, for example as M(h).

The theorem the design would need: for a value path M(h) and a source-rotated score, the partner-to-self Jacobian d y_self / d x_other = alpha(h) M(h) can take, for two histories h, h', opposite signs on one expression and the same sign on another. A one-parameter family of histories must not be able to do this, or else it is a gain.

**For (c).** Geometric frequencies give log-spaced periods 2 pi / theta_i, from 2 pi up to about 2 pi * 10^4 frames (about 35 minutes at 30 Hz, for large d). But these are oscillation periods, not decay times. Decay is not guaranteed (Property 3). RoPE gives "when, relatively" by structure, not "how long it lasts".

**For (d).** Not addressed. The relative-position property needs self and other frames to share W_q and W_k, that is, to be expressed in one common coordinate system. Building that common space (the partner's face mapped into the agent's body coordinates) is the real content of (d), and RoPE assumes it rather than providing it.

## Verdict

**adopt** as the time encoding for attention over the 30 Hz streams; **reject** as a source of (a).

- The relative-position property is a clean, checkable theorem, and it extends to real time stamps.
- The paper's derivation only exhibits a solution. It is unique only under linearity and a shared query/key operator, by the derivation above.
- The decay claim is a plot of an upper bound.
- Any score-side code leaves the partner influence in a cone of fixed value matrices.
