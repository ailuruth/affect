# Scellier & Bengio 2017: Equilibrium Propagation: Bridging the Gap Between Energy-Based Models and Backpropagation

Citation: B. Scellier, Y. Bengio. "Equilibrium Propagation: Bridging the Gap Between Energy-Based Models and Backpropagation." *Frontiers in Computational Neuroscience* 11:24, 2017. arXiv:1602.05179 (v5, 28 Mar 2017).

Source read: arXiv v5 via text extraction. Read in full: abstract and sections 1-6 (continuous Hopfield model, neuronal dynamics, free and weakly clamped phases, STDP link, general framework with Theorem 1 and Proposition 2, related work with CHL, Boltzmann machines, recurrent backprop and Xie & Seung, MNIST experiments, discussion). Not read: Appendix A (proof of Theorem 1), Appendix B (Lagrangian proof), Appendix C (stochastic version). The theorem is quoted from the main text.

## The failure or bottleneck it answered
- **Backprop needs a second kind of computation.** Backpropagation "requires a special computational circuit and a special kind of computation in the second phase of training." Recurrent backprop (Almeida 1987; Pineda 1987) "involves a different kind of neural computation in the second phase", a linearised network.
- **Contrastive Hebbian learning is inconsistent.** Its objective "may take negative values if the clamped phase and free phase stabilize in different modes of the energy function, in which case the weight update is inconsistent and learning usually deteriorates, as pointed out by Movellan (1990)."
- **Contrastive divergence can cycle.** "The CD1 update rule is provably not the gradient of any objective function and may cycle indefinitely in some pathological cases".
- **The earlier fix needs extra assumptions.** Xie & Seung (2003) needed "infinitesimal feedback weights and exponentially growing learning rates for remote layers."
- These are theoretical failures, not a measured curve. The experiments only show trainability: MNIST with 1-3 hidden layers of 500 units, "0.00% training error", generalisation error "between 2% and 3%".

## The new computation, in one equation

  ∂J/∂θ = lim_{β→0} (1/β) [ ∂F/∂θ (θ, v, β, s^β) − ∂F/∂θ (θ, v, 0, s^0) ],  F = E + βC,  ds/dt = −∂F/∂s

The network relaxes to a free equilibrium s^0. The outside world (the target) is then added as a *weak* external potential βC, and the network relaxes to a nearby nudged equilibrium s^β. The gradient of the objective is the difference between the two equilibria's local energy derivatives, divided by β. The same relaxation dynamics compute both the prediction and the credit assignment. For the Hopfield energy this gives a local rule, ΔW_ij ∝ (1/β)[ρ(u_i^β)ρ(u_j^β) − ρ(u_i^0)ρ(u_j^0)].

What is computed is the *linear response of an equilibrium to a vanishing external influence*. In the limit, the magnitude of β cancels.

## New computation or recombination?
Parts:
1. A continuous Hopfield energy (Hopfield 1984; Bengio & Fischer 2015).
2. Gradient-flow relaxation.
3. A contrastive two-phase Hebbian update (Movellan 1990; Boltzmann machines).
4. The fixed-point objective shared with recurrent backprop (Almeida/Pineda).
5. The implicit function theorem.

The paper notes that "algorithms related to ours based on infinitesimal perturbations at the outputs were also proposed by O'Reilly (1996); Hertz et al. (1997)." So it is a recombination by the parts test.

The contribution that changes what is computed is a reinterpretation of *strength of clamping* as a continuous variable, and the use of only its derivative at zero. The paper states this directly: "the cost C represents the marginal variation of the total energy F due to a change of β." CHL is the β = ∞ end ("We choose the notation u^∞ for the fully clamped fixed point because it corresponds to β → +∞"). The free phase is β = 0. EqProp is the tangent at β = 0. The local-perturbation definition fixes CHL's mode-switching problem, because "the implicit function theorem guarantees that the weakly clamped fixed point will be close to the free fixed point (thus in the same mode of the energy function)."

## What it suggests for an affective core
This paper contains the project's dial in plain sight, under its own name.
- **The dial is named.** β is called the "influence parameter": it "controls whether the output y is pushed towards the target y or not, and by how much". β = 0 is the free agent. β → ∞ is full clamping, where the output *is* the target: a copy. CHL works at the copy end and fails when the copied state sits in a different basin from the agent's own.
- **EqProp's move is to stop using β as a gain.** It uses an infinitesimal β, only to *measure*. The computed quantity is the derivative ds^β/dβ at 0, which by the implicit function theorem is −(∂²F/∂s²)⁻¹ ∂C/∂s: the outside's pull filtered through the inverse of the agent's own Hessian. That is a state-dependent *matrix*, shaped by the agent's whole current energy landscape. The scalar's size divides out.
- **Two time scales, two roles.** Under EqProp, the outside world never sets the fast state; the nudged state stays in the agent's own basin by construction. The outside changes only the slow parameters θ (the landscape) through the contrast between the free and nudged equilibria.
- **Translated:** the partner's expression would act as a weak potential on the agent. The agent would settle where its own landscape puts it. Partner influence would be read as the agent's *susceptibility* (how its own equilibrium yields) and written into the slow landscape, not into the face.
  - Partner influence is then a response operator that differs by state and by direction. The prediction that would set this apart: the agent yields to the partner along its soft (low-curvature) directions and not along its stiff ones, and which directions are soft changes with need.
  - Implementation detail: "it helps regularize the network if we choose the sign of β at random".
- **Where it collapses back.** At any finite β, the nudged state is a biased estimate, and β is again a knob. Used as an online coupling rather than a learning probe, a large β is CHL, which is copying. The structure also needs symmetric weights (an energy), a static input, and long relaxations (500 iterations for three layers, Table 2).
- **Is it new for this project?** Linear response and fluctuation-dissipation ideas are already near the project (research/seifert-2012-stochastic-thermodynamics.md). The Lagrangian proof in Appendix B uses a costate, as does research/foundations/costate.md. The new part would be the assignment of roles: the partner as an infinitesimal probe of the agent's own landscape, never as a clamp.

## Verdict
- [Equilibrium propagation (Scellier & Bengio)](scellier-bengio-2017-equilibrium-propagation.md) — 2017 — adopt (as a direction) — the influence parameter β runs from free (0) to clamped copy (∞), and EqProp uses only dβ at 0: the outside acts through the agent's own inverse Hessian and writes to slow parameters, not to the state; recombination by parts (Hopfield, CHL, Almeida-Pineda).
