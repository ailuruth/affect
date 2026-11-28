# Contracting implicit recurrent neural networks: stable models with improved trainability (Revay & Manchester)

Max Revay & Ian R. Manchester, *Proceedings of the 2nd Conference on Learning for Dynamics and Control (L4DC)*, PMLR 120, 2020; arXiv:1912.10402v1 (22 Dec 2019), 11 pp. Code cited (github, ci-rnn); not inspected.

## What was read
arXiv v1, extracted text, **in full**: abstract, §1 (contraction, convex parameterizations, contributions), §2 (model set, implicit RNNs, Theorem 1 with proof), §3 (identification problem, initialisation, training), §4 (simulated system, gait prediction, figure captions). The figures were seen only through their captions and the text.

## The computation, precisely
**Model (eq. 5–8).** x_{k+1} = f_θ(x_k, u_k), y_k = g_θ(x_k, u_k), with f_θ an L-layer network written implicitly: E₀h⁰ = x, E_{ℓ+1}h^{ℓ+1} = φ(W_ℓh^ℓ + B_ℓu + b_ℓ), f_θ = E_L h^L, E_ℓ invertible. The activation φ is any piecewise-differentiable scalar nonlinearity with slope in [−1, 1] (γ = 1 "for simplicity"). The implicit and explicit forms are input–output equivalent (z_ℓ = E_ℓh^ℓ, A_ℓ = W_ℓE_ℓ⁻¹).

**Contraction (§1.1).** A differential Lyapunov function V(x, δx) > 0 with V(x_{k+1}, δx_{k+1}) ≤ λV(x_k, δx_k), 0 < λ < 1 (λ = 1 allowed: non-expansive). With a constant metric M ≻ 0, the condition is (∂f/∂x)ᵀM(∂f/∂x) − λM ≺ 0 (eq. 3). Spectral-norm methods are the special case M = I, λ = 1. Example 1: a ReLU RNN with A = [[0.8, 1], [0, 0.8]] has ‖A‖ = 1.44, so it fails the spectral test, but contracts in P = diag(1, 10).

**The convex set (eq. 10, Theorem 1).**

  [[E_ℓ + E_ℓᵀ − P_ℓ, W_ℓᵀ], [W_ℓ, P_{ℓ+1}]] ≻ 0, ℓ = 0, …, L − 1, with P₀ = λP_L and P_ℓ positive diagonal.

This is jointly convex in (E, W, P). Theorem 1: every θ in the set gives a model contracting with rate λ in the metric V = δxᵀE₀ᵀP₀⁻¹E₀δx. The proof uses δᵀP⁻¹δ ≥ Λ(h, δ)ᵀP⁻¹Λ(h, δ) for diagonal P and slope-restricted φ, plus EᵀP⁻¹E ⪰ E + Eᵀ − P.

**What is not there.** Only contraction (forgetting of initial state under the same input) is certified. There is no input–output (incremental gain) bound, and the output map g_θ "can be any function". The LMIs are enforced during training by a Burer–Monteiro penalty (M = LLᵀ with a penalty raised ×10 when violated by more than 10⁻³), so membership in the set is approximate during learning, not by construction. Initialisation: sample A with entries N(0, α²/n) (eigenvalues on a circle of radius α), then project onto the set by a cvxpy problem.

## Evidence with numbers
- Simulated system (Chen et al. 1990, modified to run near instability; 20 batches of 500 samples; 2 layers × 60 ReLU units): the contraction constraint "did not hinder training" compared to the same implicit structure unconstrained (A vs B), whereas the spectral-norm constraint "dramatically hinders training" (D vs E). Numbers only in figures.
- Gait prediction (9 participants, 11 trials each, last 2 held out; 64 units, 1–3 layers): almost all ci-RNNs beat the matching s-RNN on test NSE, in every case for 3 layers; several unconstrained RNNs were unstable with unbounded NSE.

## What it means for the designs
1. **Contraction alone is not a ceiling.** A ci-RNN forgets initial conditions, so it has no bistable state and no copy attractor of its own, but it says nothing about how strongly partner input reaches the output. For the per-expression ceilings, a contraction certificate is necessary (it rules out partner-switchable persistent states inside the block) but not sufficient; an incremental gain certificate is needed on top (the robust REN, revay-2023-recurrent-equilibrium-networks.md).
2. **A non-identity metric matters for expressivity.** Example 1 and the A-vs-E comparison show that the price of stability is mostly the price of a fixed metric. Any ceiling construction for the engine should use the REN-type free metric, not per-layer spectral norms.
3. **Penalty enforcement is not by construction.** This paper's training enforces the LMI only approximately. For the D93 question ("can the ceiling hold by design?") only direct parameterisations count (Revay et al. 2023; Wang & Manchester 2023).

## Verdict
**background (the contraction layer only; superseded by the direct parameterisation of RENs).** It shows that contraction by itself costs little accuracy on identification tasks; it certifies no input–output bound and enforces its set only by penalty.
