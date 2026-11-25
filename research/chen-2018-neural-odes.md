# Chen, Rubanova, Bettencourt & Duvenaud 2018: Neural Ordinary Differential Equations

Citation: R. T. Q. Chen, Y. Rubanova, J. Bettencourt, D. Duvenaud. "Neural Ordinary Differential Equations." NeurIPS 2018. arXiv:1806.07366v5 (14 Dec 2019).

Source read: sections 1-8 in full: introduction, the adjoint method with Algorithm 1, ODE-Nets for supervised learning, continuous normalizing flows, the latent ODE time-series model, scope and limitations, related work, conclusion. Not read: Appendices A-F, which hold the proof of Theorem 1, the adjoint derivation, the extended algorithm with time derivatives, code, the latent-ODE algorithm and extra spiral figures.

## The failure or bottleneck it answered

This paper did **not** start from a measured failure. It started from an observation about an existing structure, then found bottlenecks the limit removes:

- **The observation.** Residual updates "h_{t+1} = h_t + f(h_t, θ_t) … can be seen as an Euler discretization of a continuous transformation" (citing Lu et al. 2017; Haber & Ruthotto 2017). The authors ask: "What happens as we add more layers and take smaller steps?"
- **The bottlenecks it then answers:**
  - Training memory grows with depth. Backpropagating through a deep stack stores every activation, "a major bottleneck of training deep models". Table 1 on MNIST: ResNet 0.41% error, 0.60 M parameters, O(L) memory; ODE-Net 0.42%, 0.22 M parameters, O(1) memory.
  - Normalizing flows need a Jacobian determinant, "which has a cubic cost in either the dimension of z, or the number of hidden units". In practice, standard flows therefore stack "many layers of only a single hidden unit."
  - Irregularly sampled time series: binning "leads to difficulties with missing data and ill-defined latent variables." Measured on noisy spirals (Table 2, predictive RMSE): RNN 0.3937 against latent ODE 0.1642 at 30 of 100 points; 0.1813 against 0.1346 at 100 of 100.

## The new computation, in one equation

h(T) = h(0) + ∫₀ᵀ f(h(t), t, θ) dt,  da/dt = −a(t)ᵀ ∂f/∂z,  ∂ log p(z(t))/∂t = −tr(∂f/∂z(t))

- **The forward pass** is the solution of an initial-value problem with a learned vector field. "Depth" becomes the number of function evaluations, chosen by an adaptive solver to meet a tolerance.
- **The backward pass** solves a second ODE backwards in time for the adjoint a(t) = ∂L/∂z(t), together with the reconstructed state and dL/dθ = −∫ a(t)ᵀ ∂f/∂θ dt. Memory stays constant.
- **The one new mathematical result** is Theorem 1, the instantaneous change of variables. Along a continuous flow, log-density changes at minus the *trace* of the Jacobian, not by a log-determinant. Because trace is linear, a flow that is a sum of M terms costs O(M), not O(M³), and f need not be bijective.

## New computation or recombination?

Parts:
1. **ResNets as Euler steps.** Lu et al. 2017; Haber & Ruthotto 2017; Chang et al. 2017-2018.
2. **The adjoint sensitivity method.** Pontryagin et al. 1962. It was proposed for neural nets by LeCun et al. 1988 and Pearlmutter 1995: "previously proposed … though was not demonstrated practically." Stapor et al. 2018 gave the results this paper extends.
3. **Black-box adaptive solvers** (Runge-Kutta, implicit Adams via LSODE/VODE).
4. **Reversible residual networks** for constant memory (Gomez et al. 2017), which the paper contrasts as needing partitioned units.
5. **Normalizing flows** (Rezende & Mohamed 2015; NICE).
6. **The latent model:** a VAE with an RNN recognition network, plus an inhomogeneous Poisson-process likelihood on event times.

By the project's test this is mostly a **recombination**. Integrating a learned vector field is what continuous-time recurrent networks already computed. The adjoint is the costate of optimal control, which the project has already used and excluded (research/foundations/costate.md; the computational-neuroscientist sketch's μ = −∇_b V is the same object). The engineering contribution is real: vector-Jacobian products make any black-box solver a differentiable layer. But it changes how gradients are obtained, not what the model computes.

The exception is the **trace formula**. It changes what is computed for a density (a trace in place of a log-determinant), and it is a derived identity, not a design choice.

This paper is the counter-example in this set. Its new model came from **taking a limit of an existing architecture**, not from a measured failure. The failures it fixes (memory, determinant cost, irregular sampling) were found afterwards, as consequences of the limit.

## What it suggests for an affective core

- **The trace as a diagnostic for the dial.** Theorem 1 says what a flow does to a *volume* of possible states: −tr(∂f/∂z) is the rate at which the flow concentrates them. Apply this to the self-minus-partner difference e = x_self − x_partner. A diffusive coupling κ(x_partner − x_self) contributes −κ·I to that difference's Jacobian, so its trace is −κ·n. This is the flat-to-copy dial written as a trace: copying is volume contraction of e, and κ sets its rate. That gives a concrete test for any candidate. Compute the trace of the partner-coupling Jacobian on the difference coordinates. If it is a monotone function of one scalar, the candidate has the dial.
- **A structural alternative (direction, untested).** Let the partner enter only through a **divergence-free** term on the difference coordinates, for example a skew-symmetric or rotational coupling. Such a term adds no volume contraction toward the partner at any coupling strength. It can reshape, rotate or reroute the agent's trajectories, but it cannot by itself pull the agent onto the partner's state. Any convergence would have to come from the agent's own dynamics. This links to the contraction note (lohmiller-slotine-1998-contraction.md): a self-copy observer converges to the other only if the agent's own flow is contracting. Partner influence would then be a vector field with zero trace, not a gain. Two caveats:
  - a traceless field can still contract some directions while expanding others;
  - whether this avoids copying in practice is unproven.
- **Event times carry information.** The latent ODE's Poisson likelihood treats the *fact* that an observation happened as evidence about the latent state ("a patient may be more likely to take a medical test if they are sick"). For a dyad, the timing of a partner's bids and turns is evidence about the agent's latent state, separate from their content.
- **Adaptive depth.** The number of function evaluations "increases throughout training", tracking how hard the input is. An affective core could likewise spend more integration steps (or more of Claude's thinking budget) when its own flow is stiff. That is a settling-time readout, already proposed in the sketch convergences.
- **Where it collapses into the dial.**
  - A free neural vector field f(x_self, x_partner) can learn any coupling, including κ(x_partner − x_self).
  - Unless a structural constraint such as zero trace is imposed on the partner block, training on prediction will find the copy, as the REACT results suggest (research/react-challenge-baselines.md).
  - The tolerance trades accuracy for speed. If that trade is exposed as an affect control, it becomes one more scalar.

## Verdict

watch. The forward computation and the adjoint are recombinations; the adjoint is the costate the project already excludes. The instantaneous change of variables is a genuine new identity. It gives a usable diagnostic (the dial equals the trace of the partner-coupling Jacobian on difference coordinates) and suggests one structural direction: partner coupling restricted to divergence-free fields.
