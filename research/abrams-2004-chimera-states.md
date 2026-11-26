# Chimera states for coupled oscillators (Abrams & Strogatz)

Daniel M. Abrams & Steven H. Strogatz, "Chimera states for coupled oscillators", *Physical Review Letters* 93(17):174102, 2004; arXiv:nlin/0407045. Original observation: Y. Kuramoto & D. Battogtokh, *Nonlinear Phenom. Complex Syst.* 5:380–385, 2002.

## What was read

**Not read in this session** (arxiv.org is outside the network allowlist). The model and results below are as I know them from the paper and the later literature. Treat this note as a pointer, not a source.

## The computation, precisely

**Model.** Identical phase oscillators on a ring, with non-local coupling and a phase lag:
$$\dot\phi(x,t)=\omega-\int_{-\pi}^{\pi}G(x-x')\,\sin\!\big(\phi(x,t)-\phi(x',t)+\alpha\big)\,dx',\qquad G(x)=\tfrac{1}{2\pi}(1+A\cos x).$$

**Chimera.** For $\alpha$ slightly below $\pi/2$ there is a stable state in which part of the ring is phase-locked and the rest drifts incoherently. The symmetry is broken even though all oscillators are identical and identically coupled.

**Analysis.** Abrams & Strogatz solved the state exactly in the continuum limit through a self-consistency equation for the local order parameter $R(x)e^{i\Theta(x)}$. They showed that the chimera coexists with the fully synchronous state, which is also stable: the system is **bistable** between sync and chimera.

## What it means for the designs

- **No structural non-copy result.** Full synchrony remains a stable attractor alongside the chimera. Whether a unit ends up copying depends on initial conditions, so copy is avoided by history, not forbidden by structure. This is the opposite of what the operator wants.
- **The phase lag $\alpha$ is the dial.** Near $\alpha=\pi/2$ the coupling is almost purely "rotational", the skew part of the interaction. This repeats the skew-coupling lesson (`chang-2019-antisymmetricrnn.md`): rotation-dominated coupling does not remove the synchronous attractor.
- **Excluded framework.** Coupled phase oscillators are on the excluded list and were already a failed v2 sketch.
- **One idea worth keeping.** Identical units under identical coupling can split into a matched part and an unmatched part. That is the observed shape of human mimicry, which matches some channels and not others. But here the split is spontaneous, not tied to content or the relationship, so it does not give per-expression selection.

## Verdict
**reject (excluded framework; bistable with full sync, so no structural no-copy; primary not read).** It shows that spontaneous partial matching can coexist with full synchrony, which is the wrong guarantee for this project.
