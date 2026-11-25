# Greydanus, Dzamba & Yosinski 2019: Hamiltonian Neural Networks

## Citation

S. Greydanus, M. Dzamba, J. Yosinski. "Hamiltonian Neural Networks." arXiv 1906.01563, version v3 (5 Sep 2019), cs.NE. The arXiv PDF header says "Preprint. Under review."; the paper appeared at NeurIPS 2019 (Advances in Neural Information Processing Systems 32, pp. 15379-15389, as reported by the reference lists of Desai et al. 2021 and Zhong et al. 2020). Code: github.com/greydanus/hamiltonian-nn.

## What was read

arXiv PDF v3, via `pdftotext -layout`.
- Read in full: abstract; section 1 (introduction); section 2 (theory: Hamiltonian mechanics, symplectic gradient, the HNN loss, Eq. 1-3); section 3 (tasks 1-3, methods, results, the friction limitation); section 6 (useful properties: adding and removing energy, "perfect reversibility"); section 8 (discussion); Appendix A (training details, the Task 3 train/test split).
- Read, but only for setup and headline numbers: section 4 (two-body), section 5 (pixel pendulum, the auxiliary latent loss Eq. 7), Table 1, Appendix B (three-body, Table 2), Appendix C (pixel pendulum details).
- Skimmed: section 7 (related work). Figures were not inspected (text extraction only).

The paper has no theorem or proof section. The conservation property is asserted in one sentence; the proof below is the standard one, and the one-line form appears in Zhong, Dey & Chakraborty 2020 (Eq. 2, read).

## The object, exactly

- State space: canonical coordinates x = (q, p) ∈ R^N × R^N = R^{2N}. q = positions, p = momenta.
- The learned object: a scalar function H_θ : R^{2N} → R, a fully connected network (three layers, 200 hidden units, tanh) with parameters θ. It outputs one "energy-like" number.
- The dynamics: the symplectic gradient of H_θ,
  dq/dt = ∂H_θ/∂p,  dp/dt = −∂H_θ/∂q   (paper's Eq. 2),
  i.e. dx/dt = S_H(x) := J_can ∇H_θ(x) with J_can = [[0, I_N], [−I_N, 0]] (skew-symmetric, J_can^T = −J_can). The matrix notation J_can is mine; the paper writes S_H = (∂H/∂p, −∂H/∂q).
- The forward pass: evaluate H_θ, then take the "in-graph" gradient ∇_x H_θ by automatic differentiation (Fig. A.1).
- Training: regress the symplectic gradient on observed time derivatives,
  L_HNN = ‖∂H_θ/∂p − ∂q/∂t‖² + ‖∂H_θ/∂q + ∂p/∂t‖²   (Eq. 3).
  The targets ∂q/∂t, ∂p/∂t are analytic where possible and finite differences otherwise. Adam, learning rate 10^-3, full batch, 2000 steps (10,000 for two-body).
- Prediction: integrate dx/dt = S_H(x) from x_0 with "the fourth-order Runge-Kutta integrator in scipy.integrate.solve_ivp", error tolerance 10^-9.
- Pixel variant (section 5): an autoencoder maps two stacked 28×28 frames to a 2-unit latent z = (z_q, z_p). The HNN acts on z. An auxiliary loss L_CC = ‖z_p^t − (z_q^t − z_q^{t+1})‖² (Eq. 7) pushes z_p toward a finite difference of z_q, "to have roughly same properties as canonical coordinates".
- Two further operations (section 6): integrating the ordinary gradient R_H = (∂H/∂q, ∂H/∂p) changes the conserved quantity ("bump" the pendulum to a higher energy level); integrating S_H conserves it.

What is learned: only the scalar landscape H_θ. The structure J_can is fixed by hand and assumes the coordinates are canonical.

## The key property and its proof, step by step

**Proposition (conservation).** Let H_θ be C¹ and let x(t) solve dx/dt = J_can ∇H_θ(x) with J_can skew-symmetric. Then dH_θ(x(t))/dt = 0 for all t.

Paper's wording: "moving in the direction of the symplectic gradient keeps the output exactly constant." No proof is given.

Proof:
1. Chain rule: dH_θ/dt = ∇H_θ(x)^T dx/dt.
2. Substitute the dynamics: dH_θ/dt = ∇H_θ^T J_can ∇H_θ.
3. For any vector a and skew J: a^T J a is a scalar, so a^T J a = (a^T J a)^T = a^T J^T a = −a^T J a. Hence a^T J a = 0.
4. With a = ∇H_θ(x), dH_θ/dt = 0. In coordinates: (∂H/∂q)^T (∂H/∂p) + (∂H/∂p)^T (−∂H/∂q) = 0, which is Zhong et al.'s one line.

The property holds for every θ and does not depend on training. It follows from the skew structure alone.

**Second claimed property (reversibility).** The paper says trajectories are "perfectly reversible", citing Liouville's theorem ("the density of particles in phase space is constant"), and concludes that "any mapping (q0, p0) → (q1, p1) is bijective/invertible."

**Where the paper is loose or only empirical:**
- **The conserved quantity is H_θ, not the true energy.** The paper shows the two are close only in figures, and Table 1 shows the HNN energy error is small but not zero.
- **Identifiability of H_θ.** The loss sees only ∇H_θ, so H_θ is fixed only up to an additive constant. Section 3.2 says the conserved quantity "differs by a constant factor" from the true energy; its own footnote example (a height offset) describes an additive constant. A multiplicative factor would change the vector field.
- **Exact conservation holds for the continuous flow only.** RK4/RK45 is not a symplectic integrator, so the integrated H_θ can drift. Desai et al. 2021 mention that Zhu et al. show symplectic integrators matter for Hamiltonian NNs (as reported by Desai; not read).
- **The reversibility argument names the wrong theorem.** Any ODE with a locally Lipschitz vector field has a bijective time-t flow map, by uniqueness forward and backward. Liouville gives something stronger: volume preservation (Jacobian determinant 1). Bijectivity does not need Liouville.
- **Friction cannot be represented.** The paper states this itself: on the real pendulum "the HNN roughly conserves this quantity... a fundamental limitation of HNNs: they assume a conserved quantity exists and thus are unable to account for things that violate this assumption, such as friction."
- **Canonical coordinates are assumed.** From pixels, the auxiliary loss only "encourages" canonical form. Nothing checks the Poisson bracket relations.
- **Derivative targets are needed** (finite differences on noisy data).
- **Three-body results are weak.** Appendix B, Table 2: test loss 49 ± 48 (HNN) vs 38 ± 40 (baseline); the authors: "both models struggled".

**Measured (Table 1, energy MSE ×10³, baseline vs HNN):**

| Task | Baseline | HNN |
|---|---|---|
| Mass-spring | 170 ± 20 | 0.38 ± 0.1 |
| Ideal pendulum | 42 ± 10 | 25 ± 5 |
| Real pendulum | 390 ± 7 | 14 ± 5 |
| Two-body (×10^6) | 6.3e4 | 39 |
| Pixel pendulum | 9.3 | 0.15 |

Train/test losses are about equal. The exception is the real pendulum, where HNN train loss is worse (9.2 vs 2.7).

## What it would mean for a dyadic affective core

My inference, not the paper's.

**A concrete mapping.**
- Agent state x_A = (q_A, p_A): q_A = expression and posture coordinates (e.g. AU activations, body set-points), p_A = their conjugate "momenta" (rates or drive variables).
- Partner state x_B the same.
- A joint Hamiltonian H(x_A, x_B) = H_A(x_A) + H_B(x_B) + H_int(x_A, x_B), with dynamics dx/dt = J_can ∇H.

**What the HNN would deliver on (a)-(d):**
- (b) Self vs other: block structure of x and additive H_A + H_B, so "whose" is the block index.
- (d) Reading the other through one's own body: use the agent's own learned H_A as H_B, i.e. evaluate the partner's inferred state x̂_B on the agent's own energy landscape. "How much would this face cost my body" is H_A(x̂_B).
- (a) Coupling through H_int, e.g. H_int = q_A^T W q_B with W ∈ R^{m×m}. Then dp_A/dt gets −W q_B and dp_B/dt gets −W^T q_A. W can be signed and off-diagonal per expression, so (a) is representable in form. But the coupling is reciprocal: the same W acts in both directions, transposed (action equals reaction).

**Why it fails as a core: it excludes settling as well as copying.**

*Claim (standard fact, my statement):* a Hamiltonian flow has no asymptotically stable equilibrium.

*Proof sketch:*
1. Liouville: the flow preserves phase-space volume.
2. If an equilibrium x* were asymptotically stable, a small ball around it would be mapped, for large t, into a strictly smaller neighbourhood of x*. Its volume would then shrink, which contradicts step 1.

*Consequences:*
- A closed HNN dyad can never converge to consensus, so it cannot collapse to copying. That is good for (a).
- It can never relax to a mood baseline either. A partner's smile injects energy that sloshes between the agents forever, and the flow is time-reversible.
- (c) has no structure in this object. With quadratic H the linearized modes are undamped oscillations with frequencies set by H. No decay rates exist, so there are no reflex-to-temperament time constants.

**When it reduces to an excluded mechanism.** It does not reduce to copying or to diffusion to consensus, because both need dissipation, which the object forbids. A scalar gain appears if W = w·I: one number scales every expression's coupling, and it is the excluded "flat to copy" knob in conservative form.

**The theorem a design would need.** One cannot be stated inside this object: the property the core needs (bounded, decaying influence) contradicts conservation. The useful piece is the idea of a learned scalar energy whose gradient, contracted with a fixed structure matrix, gives the dynamics, with the property following from the structure for every θ. The port-Hamiltonian extension (see desai-2021-neary-2023-port-hamiltonian-nn.md) keeps that idea and adds dissipation and ports.

## Verdict

**Reject as the core, keep the construction.** A closed conservative flow has no damping, no inputs and no attractors, so it can model neither mood relaxation nor a partner's input. The construction of a learned scalar energy plus a fixed skew structure, giving a property for every θ, is the right template and carries over to port-Hamiltonian form.
