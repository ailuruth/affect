# Cohen & Welling 2016: Group Equivariant Convolutional Networks

## Citation

T. S. Cohen, M. Welling. "Group Equivariant Convolutional Networks." Proceedings of the 33rd International Conference on Machine Learning (ICML), PMLR 48, 2016. arXiv 1602.07576. Version read: v3 (3 Jun 2016), the latest.

## What was read

PDF from arXiv (v3), text extracted with pdftotext. The -layout extraction interleaves the two columns, so I also extracted in reading order.

- Read in full: abstract; sections 1 (introduction), 2 (structured and equivariant representations), 4 (mathematical framework: symmetry groups, p4, p4m, functions on groups), 5 (equivariance properties of CNNs), 6 (G-correlation, pointwise nonlinearities, subgroup and coset pooling), 7 (efficient implementation), 9 (discussion), 10 (conclusion); Appendix A (the derivation that planar correlation is not rotation-equivariant, and that pooling commutes with the group action); Appendix C (G-conv calculus: gradients as G-correlations).
- Read, results only: section 8 (rotated MNIST, CIFAR-10).
- Skimmed: section 3 (related work); Appendix B (GPU gradient of the indexing operation).
- Not read: references.

## The object, exactly

**Groups.**
- G is a discrete group acting on a set X. In the first layer X = Z^2, the pixel grid. In later layers X = G itself.
- Z^2 is the translation group (integer pairs under addition).
- p4 = all compositions of translations and rotations by 90 degrees, parameterised by g(r, u, v) = [[cos(r pi/2), -sin(r pi/2), u], [sin(r pi/2), cos(r pi/2), v], [0, 0, 1]], with 0 <= r < 4 and (u, v) in Z^2. Composition is matrix multiplication. g acts on a pixel (u', v') by multiplying its homogeneous vector (u', v', 1).
- p4m adds mirror reflections: g(m, r, u, v) has (-1)^m on the first row's rotation entries, m in {0, 1}, and m = (1 - det g)/2.
- "Split" groups decompose as g = t s, with t a translation and s in the stabiliser of the origin (4 rotations for p4, 8 rotation-flips for p4m).

**Feature maps.**
- A stack of K feature maps is a function f: X -> R^K with finite support. The value f(x) is a K-vector, and f_k is channel k.
- Group action on feature maps (Eq. 4): [L_g f](x) = f(g^{-1} x). This is a homomorphism: L_g L_h = L_{gh} (Eq. 5).
- For f: G -> R^K the same formula holds, with g^{-1} h read as group composition.
- Involution (Eq. 6): f^*(g) = f(g^{-1}).

**Layers.**
- First-layer G-correlation (Eq. 10), with filter psi: Z^2 -> R^K:
  [f star psi](g) = sum_{y in Z^2} sum_k f_k(y) psi_k(g^{-1} y), for g in G.
- Full G-correlation (Eq. 11), with f, psi: G -> R^K:
  [f star psi](g) = sum_{h in G} sum_k f_k(h) psi_k(g^{-1} h).
  The output is a function on G. One output map per filter, so K_out filters give f: G -> R^{K_out}.
- Pointwise nonlinearity (Eq. 14): C_nu f(g) = nu(f(g)), with nu: R -> R.
- Pooling without stride (Eq. 16): P f(g) = max_{k in gU} f(k), where U is a subset of G (a neighbourhood of the identity) and gU = {gu : u in U}.
- Subsampling on a subgroup H of G. Coset pooling is pooling with U = H, which gives a function on the quotient G/H.
- Biases and batch-norm parameters: one per G-feature map, not one per plane.

## The key property and its proof, step by step

### Theorem 1 (G-correlation is equivariant), Eq. 12

**Statement.** For all u in G, all finitely supported f, and all filters psi:
[L_u f] star psi = L_u [f star psi].

**Hypotheses** (stated or implied):
- G is a group.
- The sum over X is unchanged by the substitution h -> u h. For X = G with counting measure this holds because left multiplication by u is a bijection of G. For the first layer it needs G to map the grid Z^2 onto itself, which is why only 90-degree rotations and the flips are used.
- f has finite support, so the sums are finite.
- The filter psi is the same on both sides. It is not transformed.

**Proof** (the paper's Eq. 12, with each step checked):
1. By the definition of L_u: [[L_u f] star psi](g) = sum_h sum_k f_k(u^{-1} h) psi_k(g^{-1} h).
2. Substitute h -> u h. This is a bijection of G, so the sum's range is unchanged: = sum_h sum_k f_k(h) psi_k(g^{-1} u h).
3. Use g^{-1} u = (u^{-1} g)^{-1}: = sum_h sum_k f_k(h) psi_k((u^{-1} g)^{-1} h).
4. By the definition of star: = [f star psi](u^{-1} g).
5. By the definition of L_u: = [L_u [f star psi]](g). QED.

The first-layer version is the same computation with y in Z^2. Contrast it with Appendix A (Eq. 9 and 19), where the substitution y -> r y is valid because rotation preserves Z^2. Ordinary planar correlation satisfies only [L_r f] star psi = L_r [f star [L_{r^{-1}} psi]]. It is equivariant to rotation only if the filter bank contains every rotated copy of each filter, and even then the individual maps are permuted.

Not in the paper, but follows in a few lines (my derivation). For a finite G, every linear map Phi on functions G -> R^K that commutes with all L_u is a G-correlation:
1. Write Phi f(g) = sum_h kappa(g, h) f(h).
2. Commuting with every L_u forces kappa(u g, u h) = kappa(g, h).
3. Hence kappa(g, h) = kappa(e, g^{-1} h) =: psi(g^{-1} h).

So G-correlation is not just one equivariant layer. On the regular representation it is all of them.

### Theorem 2 (pointwise nonlinearities preserve equivariance), Eq. 15

**Statement.** C_nu L_h = L_h C_nu.

**Proof.** C_nu L_h f = nu o (f o h^{-1}) = (nu o f) o h^{-1} = L_h C_nu f. This is associativity of composition: L acts by precomposition and C by postcomposition. QED.

**A hypothesis the paper does not stress.** The proof works because the group acts on feature maps only by moving points of the domain (a permutation of coordinates); it never acts on the values. If a group element acted on the values, say by x -> -x on a channel, then nu commutes with it only if nu itself is equivariant (here: odd). ReLU is not. The standard fix is to make every action a permutation, as the regular representation does.

### Theorem 3 (pooling preserves equivariance), Eq. 17 and Appendix Eq. 20

**Statement.** P L_h = L_h P.

**Proof.**
1. P L_h f(g) = max_{k in gU} f(h^{-1} k).
2. Substitute k' = h^{-1} k: = max_{k' in h^{-1} g U} f(k') = P f(h^{-1} g) = L_h P f(g). QED.

The proof needs the pooling domains to be left translates gU, so that the left action commutes with them.

**Consequences.**
- Subsampling on a subgroup H leaves equivariance to H only.
- With U = H, the result is constant on cosets g H, because g h' H = g H. It is then a function on G/H that is still G-equivariant.
- Pooling over the 4 rotations at each pixel gives a rotation-invariant feature map on Z^2 = p4/R.

### Empirical results (read, not checked)

- **Rotated MNIST, test error.** P4CNN 2.28% vs a planar Z2CNN 5.03% with about the same parameter count. The previous best was 3.98%.
- **Pooling over rotations after every layer** (P4CNNRotationPooling) gives 3.21%, worse than keeping the rotation axis until the end. The authors read this as "premature invariance is undesirable".
- **CIFAR-10, test error.** p4m All-CNN 7.59% vs 9.44%. p4m ResNet44 6.46% vs 9.45%, and 4.94% vs 5.61% with augmentation.
- The authors note that CIFAR is not rotation-symmetric, yet the group layers still help.

## What it would mean for a dyadic affective core

All of this section is my inference.

**The space.** Represent the dyad at one instant as a feature map on the swap group Z2 = {e, s}, s^2 = e:

    f: Z2 -> R^K,   f(e) = x_self,   f(s) = x_other.

Here K indexes expression and body channels, and both values live in the agent's own body coordinates. The action is L_s f(g) = f(s g): it exchanges the two slots. "Whose" is the group coordinate; "what" is the channel index k. This is exactly the G-CNN split between pose and feature. A layer that keeps the group axis keeps (b) by construction.

**The general equivariant layer** (Theorem 1 plus the finite-group converse above). With matrix-valued filters psi: Z2 -> R^{K' x K}:

    [f star psi](e) = A x_self + B x_other,   [f star psi](s) = B x_self + A x_other,   A = psi(e), B = psi(s).

Equivalently, the joint map is Phi = [[A, B], [B, A]], which is all matrices commuting with the swap P = [[0, I], [I, 0]].

Proof: write Phi = [[A, B], [C, D]]. Then P Phi = [[C, D], [A, B]] and Phi P = [[B, A], [D, C]], so P Phi = Phi P forces C = B and D = A.

**What swap-equivariance forces.**
1. **Reciprocity of the coupling.** The rule by which self is moved by other (B) is the rule by which other is moved by self. For a nonlinear core F = (F_self, F_other) with a relation state h that the swap maps to sigma(h) (my history with you, exchanged with your history with me), equivariance reads F_other(a, b, h) = F_self(b, a, sigma h). Differentiating:

       d F_other / d x_self (x, h) = d F_self / d x_other (P x, sigma h).

   The other's coupling to me is my coupling to them, evaluated on the swapped state.
2. **Mirror states cannot be broken.** If x_self = x_other and h = sigma h, then the output is also swap-symmetric. Proof: P f = f implies P Phi(f) = Phi(P f) = Phi(f). An equivariant core can never break a tie that the state does not already break.
3. **Weight sharing across "whose", which is a precise form of (d).** The same filter A reads my state in my slot and the partner's state in theirs. So the agent's model of the partner's response is its own response function applied to the swapped dyad: F_other(x, h) = F_self(P x, sigma h). "Reading the other through one's own body" becomes this identity. It is valid only after both streams are encoded into one common space; the raw inputs (camera action units vs proprioception) are different spaces on which Z2 does not act. The first layer must be an encoder pair (E_self, E_other) into the common space. Equivariance can start only after it, and the design question for (d) is that encoder pair.

**What swap-equivariance does not force, and where it reduces to excluded mechanisms.**
- B is an arbitrary K' x K matrix. It can differ per expression, have off-diagonal entries (smile in response to anger), and have negative entries. Equivariance does not imply a scalar gain.
- The scalar gain is the sub-case B = g I. Copying is A = 0, B = I.
- **Consensus.** In the coordinates u = x_self + x_other and w = x_self - x_other, Phi acts as A + B on u and A - B on w; these are the eigenspaces of P, so they decouple. Under dx/dt = Phi x, w -> 0 from every start if and only if A - B is Hurwitz. The two-node diffusion (A = -kappa I, B = kappa I) is swap-equivariant. So diffusion to consensus is inside the equivariant class: equivariance neither causes nor forbids it.
- **Invariance (pooling over Z2) is the collapse of (b).** If y_self is required to be swap-invariant, y_self(x_self, x_other) = y_self(x_other, x_self), then in the linear case A = B: the agent cannot tell whose expression it is. This is the dyad analogue of the paper's premature-invariance result (3.21% vs 2.28%).

**What (a)-(b) need: a broken symmetry, located precisely.** The mimicry data are not reciprocal. In Carr 2014 (as summarised in mimicry-context-synthesis.md) high-power perceivers smile at high-power targets' anger, so the response depends on the asymmetric relation. There are two ways to get this:
- (i) **Explicit breaking.** Drop equivariance and use B_self<-other != B_other<-self. This loses weight sharing and the partner model in point 3.
- (ii) **Breaking by state.** Keep F equivariant and put all asymmetry into h, with h != sigma h. Then, by point 1, the couplings differ exactly when h differs from its swap. When the relation is mutual (h = sigma h), the couplings are forced to be reciprocal. Option (ii) is the sharper design: every asymmetry is in a learned, inspectable state.

**Sign and reflection groups on expression channels.**
- Let Z2 act on a bipolar channel by x_c -> -x_c. On every channel at once, any linear map commutes with it, so the constraint is vacuous. On a subset of channels, a linear map must be block-diagonal between flipped and unflipped channels.
- For nonlinear maps it forces an odd response, F(-x) = -F(x): if the agent answers a smile with X, it must answer the opposite expression with -X.
- Action-unit intensities are non-negative, so the natural version is a permutation of antagonist pairs, for example AU12 (lip corner puller) with AU15 (lip corner depressor), and AU1+2 (brow raisers) with AU4 (brow lowerer). As a permutation it is compatible with ReLU (Theorem 2's hypothesis).
- Equivariance to it would force the response to a partner's frown to be the mirror of the response to their smile. The synthesis data reject this: smile return is robust across relations, while the returns of sadness and anger switch on, off or change sign with the relation.
- So a sign or reflection symmetry on expression channels should **not** be imposed. It is broken in the data, and imposing it would itself be a falsifiable mistake.

**(c) Time scales.** G-CNNs supply none. Equivariance to time translation (G = Z) is ordinary temporal convolution, which says nothing about which time constants exist.

**The theorem the design would need.** Let F = (F_self, F_other) be swap-equivariant with state h -> sigma h, and let J(x, h) = d F_self / d x_other. Show:
1. There exist reachable histories h, h' such that J(x, h) and J(x, h') are not related by a positive scalar on the expression block. Some expression keeps its sign while another flips. So {J(x, h)} is not contained in {g J_0 : g in R}: not a gain.
2. J(x, h) != g I for generic h: not a copy.
3. A - B, or its nonlinear analogue d(F_self - F_other)/d w, is not Hurwitz uniformly in h: no forced consensus.
4. J_other(x, h) := d F_other / d x_self (x, h) = J(P x, sigma h). The partner model's coupling is the agent's own coupling on the swapped state, which is the formal (d).

Items 1-3 are properties the learned h must reach. Equivariance alone guarantees only item 4 and the reciprocity of point 1.

## Verdict

**adopt** as the formal frame for (b) and (d); it is a constraint, not a mechanism.

- Swap-equivariance with all asymmetry carried by a relation state h gives an exact identity: the other's coupling is my coupling on the swapped state. That makes "whose" a group coordinate distinct from "what", and makes reading the other through one's own response function a theorem.
- It does not supply (a) or (c).
- It does not exclude consensus, which is an equivariant special case.
- Sign or reflection symmetry on expression channels should not be imposed, because the data break it.
