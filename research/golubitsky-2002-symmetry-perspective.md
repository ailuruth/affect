# The Symmetry Perspective: equivariance, Schur's lemma and fixed-point subspaces (Golubitsky & Stewart)

Martin Golubitsky & Ian Stewart, *The Symmetry Perspective: From Equilibrium to Chaos in Phase Space and Physical Space*, Progress in Mathematics 200, Birkhäuser, 2002. The spatio-temporal H/K theorem is from P.-L. Buono & M. Golubitsky, "Models of central pattern generators for quadruped locomotion I", *J. Math. Biol.* 42:291–326, 2001 (with the general statement in the book, ch. 3).

## What was read

**Not read in this session.** It is a book, with no open copy reachable, and the network allowlist blocks arxiv.org and ams.org. The note states standard results of equivariant dynamics: equivariance, Schur's lemma, fixed-point subspaces and the H/K theorem, as I know them. The new claims in "What it means" are my own, proved in the note and checked numerically (C6 in `foundations/sims/symmetry-no-copy/checks.py`). Cite the book only for the standard definitions.

## The computation, precisely

**Equivariance.** A compact group $G$ acts orthogonally on $X$ by $\rho$. The vector field $f$ is $G$-equivariant if $f(\rho(g)x)=\rho(g)f(x)$ for all $g$. More generally, a map $\Phi: U\to X$ between two representations $(U,\pi)$ and $(X,\rho)$ is equivariant (an intertwiner, when linear) if $\Phi(\pi(g)u)=\rho(g)\Phi(u)$.

**Fixed-point subspaces.** For a subgroup $\Sigma\subseteq G$, $\mathrm{Fix}(\Sigma)=\{x:\rho(\sigma)x=x\ \forall\sigma\in\Sigma\}$ is flow-invariant for every equivariant $f$. Synchrony patterns forced by symmetry are fixed-point subspaces.

**Schur's lemma (real form).** Decompose $\pi$ and $\rho$ into isotypic components. A linear intertwiner $T\in\mathrm{Hom}_G(\pi,\rho)$ maps each isotypic component of $\pi$ to the component of $\rho$ of the *same* irreducible type, and is zero between inequivalent types. On a component with multiplicity $m$, $T$ is an element of $M_m(\mathbb D)$, where $\mathbb D\in\{\mathbb R,\mathbb C,\mathbb H\}$ is the irreducible's endomorphism ring.

**Reynolds projection.** The orthogonal projection of a linear map onto $\mathrm{Hom}_G$ is $\mathcal R(T)=\int_G \rho(g)^{-1}\,T\,\pi(g)\,dg$.

**H/K theorem (spatio-temporal symmetry).** A periodic solution can have spatio-temporal symmetries $(\gamma,\theta)$: $\gamma x(t)=x(t+\theta)$. For example, in a $\mathbb Z_2$-symmetric pair of identical cells there are periodic solutions with $x_2(t)=x_1(t+T/2)$, anti-phase. The H/K theorem says which pairs of subgroups $K\subseteq H$ (spatial and spatio-temporal symmetries) occur. The point here: **a swap symmetry permits "copy with a half-period lag"** as a robust solution type.

## What it means for the designs

**A twisted intertwiner cannot copy, for every parameter, every strength and every route.** Let $G$ act on the partner's face by $\pi$ and on the agent's face by $\rho=\chi\otimes\pi$, where $\chi$ is a one-dimensional character with $\chi(g)=-1$ for some $g$. Copy is the identity map, and the identity is not an intertwiner from $\pi$ to $\chi\pi$. Two statements follow.

- **Global, nonlinear.** Take any equivariant $\Phi$ and any $c>0$. Let $e(u)=\Phi(u)-cu$. Then $\Phi(gu)=\chi(g)\pi(g)\Phi(u) = -c\,\pi(g)u-\pi(g)e(u)$, so $e(gu)=-2c\,\pi(g)u-\pi(g)e(u)$. Since $\pi$ is orthogonal,
  $$\|e(u)\|+\|e(gu)\|\;\ge\;2c\,\|u\| .$$
  On every orbit $\{u, gu\}$ the worst copy defect is at least the copy scale itself. If $u$ is $g$-fixed, then $\|e(u)\|\ge c\|u\|$ directly. Check C6: 2,000 random equivariant two-layer maps with weight scales from 0.1 to 100 gave a minimum normalised defect of 1.0009, against the theorem's bound of 1.
- **Linear.** $\mathcal R(cI)=0$ on the twisted component, so $\|T-cI\|_F\ge c\sqrt{\dim}$ for every $T\in\mathrm{Hom}_G(\pi,\chi\pi)$. Twisted intertwiners are traceless: $\mathrm{tr}\,T=\mathrm{tr}(\rho(g)^{-1}T\pi(g))=-\mathrm{tr}\,T$.

**Why this is closed under every route.** Equivariant maps are closed under composition, sums and feedback: $(I-A)^{-1}$ is equivariant if $A$ is, and limits stay in the class. They are also closed under any learning rule that keeps weight-tying, because the class is a linear subspace of parameters, like a G-CNN (see `cohen-welling-2016-group-equivariant-cnn.md`). The proof needs no cap, and indirect routes do not reopen copy. This is the property every earlier design lacked. **The guarantee holds only if every path from the partner's percept is equivariant.** In practice that means a single input gate: the percept enters once, through an equivariant encoder, and the agent's internal state carries the trivial representation or a declared one.

**What the theorem costs: Schur is a no-go for mimicry.** On any isotypic component where $\pi\cong\rho$, the commutant contains $I$, so $cI$ is an allowed map for every $c$. Symmetry can therefore **only partition the face** into components where copy is impossible (the twisted ones) and components where copy is a free scalar per irreducible (a dial, back to caps). It cannot forbid copy on a component while allowing same-feature positive drive there, because that drive is a non-zero multiple of the identity. This is the precise form of the conflict with Principle 3.

**Lag.** If $G$ includes time shifts, the spatio-temporal theory says a twist can be absorbed by a time shift: anti-phase solutions are "copy at a half-period lag". The rotation counterexample C2 (in `chang-2019-antisymmetricrnn.md`) is the same phenomenon. A twisted design must state its copy test at all lags, and either exclude time shifts from $G$ or show that the partner's signals have no orbit that a shift can map to a twist.

**Is it an excluded framework?** No. It is a constraint class: equivariance under a declared group, with a declared character twist. It is the RoPE-like ingredient: a precise algebraic object with a proved property.

## Verdict
**adopt (as the core constraint; standard theory, primary not re-read).** A twisted-character equivariance makes copy impossible for every parameter, gain and route, with defect at least $c\|u\|$ on every orbit. Schur's lemma shows exactly where this conflicts with Principle 3.
