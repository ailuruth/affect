# Recurrent equilibrium networks: flexible dynamic models with guaranteed stability and robustness (Revay, Wang & Manchester)

Max Revay, Ruigang Wang & Ian R. Manchester, *IEEE Transactions on Automatic Control* (2023/2024), arXiv:2104.05942v3 (12 Jul 2023), 16 pp. Code: RobustNeuralNetworks.jl (Julia), cited in the paper; not inspected.

## What was read
Full text (arXiv v3, extracted):
- **Read in full:** §I–VI (problem, model class, Theorem 1, Theorem 2 statement, the convex parameterizations and Theorem 3, the direct parameterizations for contracting and robust RENs including the D₂₂ construction and special cases, random sampling and echo-state networks, expressivity); §VII (system identification benchmarks, Figs. 2–5 captions and Table I); §VIII (observer design, the reaction–diffusion example); §IX up to the example setup (Youla/Q-parameterization with a contracting Q).
- **Not read:** the appendix proofs.

## The computation, precisely

**Model (eq. 6–8).** A discrete-time state-space model whose nonlinearity is an implicit (equilibrium) layer:

  x_{t+1} = Ax_t + B₁w_t + B₂u_t + b_x,  y_t = C₂x_t + D₂₁w_t + D₂₂u_t + b_y,
  w_t = σ(D₁₁w_t + C₁x_t + D₁₂u_t + b_v),

with σ elementwise and **slope-restricted in [0, 1]** (Assumption 1). The equilibrium layer contains all feedforward deep nets as a special case (D₁₁ strictly block lower-triangular).

**Contraction (Definition 2).** |x_t^a − x_t^b| ≤ Kα^t|a − b| for the same input: initial conditions are forgotten exponentially.

**Incremental IQC (Definition 3).** For all pairs of solutions with inputs u, v and initial states a, b:

  Σ_{t=0}^T [y^a−y^b; u−v]ᵀ [[Q, Sᵀ],[S, R]] [y^a−y^b; u−v] ≥ −d(a,b), for all T,

with Q ⪯ 0. The special cases:
- Q = −(1/γ)I, R = γI, S = 0 gives an ℓ₂ **Lipschitz bound γ**: ‖R_a(u) − R_a(v)‖_T ≤ γ‖u − v‖_T.
- Q = 0, S = I, R = −2νI gives incremental passivity.
- Q = −2ρI, S = I, R = 0 gives incremental strict output passivity.

**Frequency-weighted bounds (Remark 1).** If R is contracting with Lipschitz bound γ and W₁, W₂ are stable filters with W₁ stably invertible, then W(u) = W₁⁻¹R(W₂u) is contracting and satisfies ‖W₁(W(u) − W(v))‖ ≤ γ‖W₂(u − v)‖.

**Theorem 1 (certificates).**
- A REN is well-posed and contracting with rate α < ᾱ if there are P ≻ 0 and diagonal Λ ≻ 0 with the LMI (15).
- It additionally satisfies the incremental IQC (Q, S, R) if (16) holds.
- The proof uses the incremental Lyapunov function V(Δx) = |Δx|²_P with V(Δx_{t+1}) ≤ α²V(Δx_t) − Γ(Δv, Δw), where Γ ≥ 0 is the incremental quadratic constraint of the slope-restricted σ.

**Theorem 2.** Every contracting REN has *some* finite ℓ₂ Lipschitz bound.

**The key step: direct parameterization (§V).** The LMI (19)/(20) is turned into a smooth surjective map from free parameters to models that satisfy it:
- For contracting RENs: H = XᵀX + εI ≻ 0, partitioned to give F, B₁, P, C₁; then E = ½(H₁₁ + P/ᾱ² + Y₁ − Y₁ᵀ), and Λ, D₁₁ from the diagonal/strictly-lower split of H₂₂.
- For robust RENs: H is shifted by the known (Q, S, R) terms (eq. 29). D₂₂ = −Q⁻¹Sᵀ + L_Q⁻¹NL_R, with N a Cayley-type transform of free matrices (eq. 31–33). For the Lipschitz case, L_Q = I and L_R = γI.

> "we construct a smooth mapping from R^N to the model weights such that every model in the image of this mapping satisfies the desired behavioural constraints."

So **Θ = R^N**: no projection, no barrier, no LMI at training time. Any SGD/Adam step, any random sample, any value of the free vector gives a model that satisfies the prescribed IQC.

**Expressivity (§VI).** The class contains:
- all stable LTI systems, all previously known contracting RNNs (ciRNN, s-RNN) and echo-state networks with the echo-state property;
- deep feedforward nets, NFIR models, and Wiener/Hammerstein models.

It also universally approximates fading-memory and contracting systems with finite Lipschitz bound (citing [69]).

**Use in feedback (§IX).** If the controller augmentation is ũ = Q(ỹ) with Q a contracting REN, the closed loop ζ = T₀w + T₁Q(T₂w) is "nonlinear but contracting" for *every* Q in the class. The Youla trick turns a learned policy into a loop that is stable by construction.

## Evidence with numbers
- **F16 ground-vibration benchmark** (~118,000 parameters per model; RNN 340 neurons, LSTM 170, REN n = 75, q = 150):
  - The REN is "about 10% of the sensitivity" of the RNN (Wiener–Hammerstein: about 1%).
  - Contracting REN NRMSE 0.16 versus 0.24 for the earlier Robust RNN γ = ∞.
  - For small γ, the observed lower bound on the Lipschitz constant is "very close to the guaranteed upper bound".
- **Table I (F16), guaranteed γ against measured γ and NRMSE:**

  | guaranteed γ | acyclic: measured γ | acyclic: NRMSE | cyclic: measured γ | cyclic: NRMSE |
  |---|---|---|---|---|
  | 10 | 8.8 | 30.0% | 9.1 | 30.3% |
  | 20 | 17.5 | 25.7% | 17.1 | 26.8% |
  | 40 | 36.7 | 20.1% | 36.0 | 21.8% |
  | ∞ (contracting only) | 91.0 | 16.2% | 85.26 | 16.8% |

  The ceiling binds, and it costs accuracy: about +14 points NRMSE at γ = 10 against unconstrained contraction.
- **Adversarial perturbation ‖Δu‖ < 0.05 (Fig. 4):** incremental gains of 980 (RNN), 290 (LSTM), 37 / 8.6 (R-aREN, γ = 40 / 10), 38.9 / 9.1 (Robust RNN).
- **Observer (§VIII):** a contracting REN (n = 51, q = 200) trained on one-step prediction tracks a 51-state reaction–diffusion PDE from a wrong initial state. A free-run copy of the PDE does not converge (the plant itself is not contracting).

## What it means for the designs
1. **This is the "innate ceiling that learning cannot exceed".** Make the *entire* partner→face path a single robust REN: every internal recurrence, every shared learned estimate, every gate that is a function of state. Give it the weighted Lipschitz IQC of Remark 1 with W₁ = diag(1/c_i) (innate per-expression ceilings c_i < 1) and W₂ an innate normalisation of partner channels. Then:
   - ‖y_i^a − y_i^b‖ ≤ c_i‖W₂(u − v)‖ for every channel i, every pair of partner histories, **every parameter vector the learner can ever reach** (Θ = R^N). Learning, replay and consolidation move only the free vector.
   - The ceiling constants (Q, S, R) are not parameters. They are compiled into the map, so no quantity the agent learns can turn them.

   (Per-channel corollary: the derivation is mine, from the weighted bound.)
2. **It bounds slopes over all routes jointly.** The certificate is incremental: it bounds the response to *differences* in partner input, i.e. the Jacobian along every path at once, including loops through the agent's own state. The comfort-loop slope that critique 3 found unbounded (X2: 0.88 → 120) is impossible inside a certified REN.
3. **Copy is non-attracting, structurally.**
   - Contraction means two runs with the same partner input converge to the same trajectory. There is no bistable "copy state" for the agent to fall into, and no pitchfork (the K6 bistability of critique 3 cannot occur).
   - With per-channel c_i < 1, the unique driven response is never a copy: the copy defect on channel i is ≥ 1 − c_i.
   - Learning cannot attract to copy, because copy is outside the image of R^N. Learning can still drift to the ceiling corner (critique 3, X3), which D78 tolerates only if the ceilings are real. Here they are real.
4. **Sign flips and context gating are free.** The IQC bounds the magnitude of incremental response, not its sign or its dependence on context. Context can enter as an extra input that is *not* counted in W₂ (the agent's own drives, the relationship code). Note: if context inputs are themselves functions of the partner, they must be routed inside the REN or counted in W₂. Otherwise they are an uncertified route (content events).
5. **Where it falls short.**
   - **Contraction forbids persistence.** A contracting system has one attractor per input. The designs need hysteretic, persistent, multistable affective states (staircase manifolds; Jung 2020 "persistence only as a loop property"; Lee 2014 hysteresis). Such states cannot live inside a contracting partner→face map.
     - They can live outside it, as an agent-owned state z that enters the REN as a non-partner input. But then any partner→z route must be bounded too.
     - A partner-*switchable* bistable z has unbounded incremental ℓ₂ gain: a finite kick gives a permanent difference. So either z has no partner write port at all, or partner→z must be bounded in another currency (bits; see tatikonda-2009-feedback-capacity-directed-information.md).
   - **Accuracy cost** at tight γ (Table I). With c_i < 1 on bounded face units, expressivity is genuinely limited.
   - **Discrete time, one IQC at a time.** The direct parameterization handles one (Q, S, R). Several simultaneous IQCs (say a Lipschitz ceiling *and* incremental passivity) are only available through the convex (LMI) form.
   - **Existing framework.** It is a robust-control/learned-model class. As a core it would be a contracting RNN, which is excluded. Its proper role is the **constraint layer** that any new core's partner path must be built from or embedded in.

## Verdict
**adopt (as the implementation of the whole-path, learning-proof ceiling: the agent's partner→face path is a robust REN with an innate diagonal output weight; the ceilings are compiled into the parameterization, so no reachable parameter exceeds them).** Open: how to coexist with persistent multistable states that the partner can influence.
