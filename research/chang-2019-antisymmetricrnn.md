# AntisymmetricRNN, and stable architectures for deep networks (Chang et al.; Haber & Ruthotto)

Bo Chang, Minmin Chen, Eldad Haber & Ed H. Chi, "AntisymmetricRNN: A dynamical system view on recurrent neural networks", *ICLR* 2019, arXiv:1902.09689. Companion: Eldad Haber & Lars Ruthotto, "Stable architectures for deep neural networks", *Inverse Problems* 34(1):014004, 2018 (arXiv:1705.03341, 2017).

## What was read

**Not read in this session.** arxiv.org is outside this session's network allowlist. A search confirmed:
- the paper treats RNNs as discretised ODEs;
- it uses an antisymmetric weight matrix so that the Jacobian's eigenvalues are purely imaginary;
- it adds a diffusion term $-\gamma I$ because forward Euler is unstable on the imaginary axis;
- it reports better long-term memory than LSTMs on some tasks.

The equations below are the standard form as I know it, consistent with that summary. The claims about the dyad are mine, checked in `foundations/sims/symmetry-no-copy/checks.py` (C1–C3).

## The computation, precisely

**AntisymmetricRNN.**
$$h_t = h_{t-1} + \epsilon\,\tanh\!\big((W-W^\top-\gamma I)h_{t-1} + Vx_t + b\big).$$
- **Why it holds memory.** The underlying ODE $\dot h=\tanh((W-W^\top)h+\dots)$ has a Jacobian $\mathrm{diag}(\tanh')\,(W-W^\top)$. The eigenvalues of $W-W^\top$ are purely imaginary, so the linearised flow neither explodes nor contracts: gradients and memories are preserved.
- **Why $\gamma$.** Forward Euler on the imaginary axis is unstable, so $\gamma>0$ shifts the spectrum slightly left. $\gamma$ trades memory against numerical stability.

**Haber & Ruthotto.** They give two "stable" designs.
1. **Antisymmetric layers**, with $Y_{j+1}=Y_j+h\,\sigma(K_jY_j+b_j)$ and $K_j=-K_j^\top$.
2. **Hamiltonian layers**, with $\dot Y=\sigma(KZ)$, $\dot Z=-\sigma(K^\top Y)$, integrated with leapfrog or Verlet. These are volume-preserving and time-reversible.

By Liouville's theorem a volume-preserving flow has no asymptotically stable sets.

## What it means for the designs

The operator's suggestion was that coupling which conserves rather than contracts leaves no attracting copy. **That holds for a closed system and fails for the dyad, which is open.** There are three failures, all checked.

1. **Error-driven skew coupling copies (C1).** $\dot x=-dx+gK(u-x)$ with $K$ skew. The transverse spectrum is $-d\pm ig\theta$, stable for every $g$. The DC transfer $(dI+gK)^{-1}gK$ approaches $I$ as $g$ grows (distance to $I$: 0.98, 0.45, 0.05, 0.005 at $g$ = 0.1, 1, 10, 100). Skew coupling acting on an *error* is high-gain tracking.
2. **Skew forcing copies rotating signals (C2).** $\dot x=-dx+gJu$, with $J$ a 90° rotation in a channel plane. Then $\langle u,Ju\rangle=0$ pointwise, and for a time-reversible partner (independent OU channels) the zero-lag copy correlation is about 0, as expected. But for a partner whose two channels are in quadrature (a circular signal), the rotation is a time shift. The 90° rotation and the filter's −63° lag partly cancel, giving a **zero-lag copy correlation of 0.895 and a lagged correlation of 0.999**. Face channels with lead–lag structure (for example smile onset leading cheek raise) are exactly such signals.
3. **Two skew stages in series compose to the identity (C3).** $J\cdot J^\top=I$. Skew maps are closed under addition (a Lie algebra) but not under composition. A two-stage indirect route, percept → state → face, each stage skew, reproduces copy. $J\cdot J=-I$ gives anti-copy. This is the recurring failure (copy returning through indirect routes) in its simplest algebraic form.

**The positive residue.**
- *Inside* the agent, a Hamiltonian or skew core keeps state without contraction, which suits persistent affect.
- A pure group action of the partner on the self, $x\mapsto R(u)x$ with $R(u)$ orthogonal, conserves the self's norm, a Casimir the partner cannot change. That gives "the partner owns direction, the self owns magnitude". But scaled copy remains whenever the rotation aligns $x$ with $u$, and parallel routes do not compose within a group.

The class that survives sum, product and feedback is the equivariant class, not the skew class (see `golubitsky-2002-symmetry-perspective.md`).

**Is it an excluded framework?** It is an RNN cell, a linear operator plus a nonlinearity: excluded as a core. Usable as a numerical constraint (non-contracting internal memory).

## Verdict
**reject (as a no-copy mechanism; primary not read).** Conserving or skew coupling does not prevent copy in an open dyad: error-driven skew coupling tracks, rotation equals delay for circular signals, and two skew stages compose to the identity. Keep only the idea of a non-contracting internal memory.
