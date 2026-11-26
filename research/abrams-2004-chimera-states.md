# Chimera states for coupled oscillators (Abrams & Strogatz)

Daniel M. Abrams & Steven H. Strogatz, "Chimera states for coupled oscillators", *Physical Review Letters* 93(17):174102, 2004; arXiv:nlin/0407045.

## What was read
The arXiv text in full: four pages, every equation, and the figure captions (the figures themselves were not seen).

## The computation, precisely
**The model.**
$$\frac{\partial\phi}{\partial t}=\omega-\int_{-\pi}^{\pi}G(x-x')\sin[\phi(x,t)-\phi(x',t)+\alpha]\,dx',\qquad G(x)=\tfrac{1}{2\pi}(1+A\cos x)\quad(1),(2)$$
with $0\le\alpha\le\pi/2$ "a tunable parameter".

**The chimera.**
> "an array of identical oscillators splits into two domains: one coherent and phase-locked, the other incoherent and desynchronized ... It cannot be ascribed to a supercritical instability of the spatially uniform oscillation, because it occurs even if the uniform state is stable."

The paper also separates it from the splitting seen with non-identical oscillators:
> "Here, all the oscillators are the same."

**The exact solution.** Introduce the local order parameter $R e^{i\Theta}=\int G(x-x')e^{i\theta(x')}dx'$ (3). The Kuramoto–Battogtokh self-consistency equation (5), with $\beta=\pi/2-\alpha$ and $\Delta=\omega-\Omega$, is solved in closed form for the cosine kernel: $Re^{i\Theta}=c+a\cos x$. The authors assume the evenness $R(x)=R(-x)$, $\Theta(x)=\Theta(-x)$ "as suggested by the simulations" and show it is self-consistent.

**Bifurcations.**
- The stable chimera "bifurcates from a spatially modulated drift state, and dies in a saddle-node bifurcation with an unstable chimera".
- The unstable branch "emerges from a homoclinic locked state at β₁ = 0, where the in-phase oscillation of Eq. (1) is linearly neutrally stable".
- The minimum drifting fraction on the stable branch is "about 44%", at $(\beta_1)_{\max}\approx0.2205$.

## What it means for the designs
- **There is no structural non-copy result, by the paper's own statement.** The chimera "occurs even if the uniform state is stable". Full synchrony (copy) and the chimera coexist, so which one appears is a matter of initial conditions. Copying is avoided by history, not forbidden by structure: the opposite of the needed guarantee.
- **The phase lag is a dial.** The chimera exists only in a band of $(\beta, A)$ (their Fig. 2) and vanishes at a saddle-node. $\alpha$ near $\pi/2$ makes the coupling nearly a pure rotation, which repeats the skew-coupling lesson in `chang-2019-antisymmetricrnn.md`.
- **Excluded framework.** These are coupled phase oscillators, and they were already a failed v2 sketch.
- **One idea to note.** Identical units with identical coupling can split into matched and unmatched parts, which is the observed shape of human mimicry. But here the split is spontaneous and position-based, not tied to content or the relationship.

## Verdict
**reject.** The chimera is bistable with full synchrony ("occurs even if the uniform state is stable"). It is an excluded oscillator framework, and its partial matching is spontaneous, not selected by content.
