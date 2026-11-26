# LQG control with minimum directed information: semidefinite programming approach (Tanaka, Esfahani & Mitter)

Takashi Tanaka, Peyman Mohajerin Esfahani & Sanjoy K. Mitter, *IEEE Transactions on Automatic Control* 63(1):37–52, 2018; arXiv:1510.04214v3 (10 Jun 2017).

## What was read
The arXiv v3 PDF from export.arxiv.org, 18 pages: introduction, problem formulation (§II), operational meaning (§III), main results for time-varying and time-invariant plants and the data-rate corollary (§IV), the numerical example (§V), the proof outline (§VI), the partially observed extension (§VII), the conclusion and Appendix A (data-processing inequality for directed information). Appendix proofs B–F were skimmed only. Figures were seen as extracted text.

## The computation, precisely

**Problem.** Plant $x_{t+1} = A_t x_t + B_t u_t + w_t$, $w_t \sim \mathcal N(0, W_t)$. The policy is any causal stochastic kernel $\mathbb P(u_t \mid x^t, u^{t-1})$. Minimise Massey's directed information from state to control,
$$I(x^T \to u^T) = \sum_{t=1}^T I(x^t; u_t \mid u^{t-1}),$$
subject to the LQG cost $J = \sum_t \mathbb E(\|x_{t+1}\|^2_{Q_t} + \|u_t\|^2_{R_t}) \le D$. (Eq. 4; stationary version Eq. 6, per-step limits.)

The authors note the conservation law $I(x^T;u^T) = I(x^T \to u^T) + I(u^{T-1}_+ \to x^T)$: (4) counts only the feedback flow through the policy, not what the plant passes back.

**Operational meaning (§III, Lemma 1, Eq. 8).** Over a noiseless binary channel with prefix-free codewords, the minimum average codeword length $R(D)$ satisfies
$$DI(D) \le R(D) < DI(D) + \tfrac r2 \log\tfrac{4\pi e}{12} + 1,$$
where $r$ is at most the state dimension. Directed information is therefore the real bit rate, to within a constant. The lower half follows from a directed data-processing inequality: an encoder between state and control can only lose directed information.

**Structure of the optimum (Theorem 1, Fig. 3).** An optimal policy is a three-stage pipeline:
1. a *virtual sensor* $y_t = C_t x_t + v_t$, $v_t \sim \mathcal N(0, V_t)$. This is linear plus additive Gaussian noise, and it is optimal among all Borel-measurable sensors;
2. a Kalman filter $\hat x_t = \mathbb E(x_t \mid y^t, u^{t-1})$;
3. a certainty-equivalence controller $u_t = K_t \hat x_t$, with $K_t$ from the ordinary Riccati recursion.

The optimal policy is a **linear Gaussian randomized policy**. Stochasticity is part of the optimum, not a defect of it. Two separation principles hold at once: filter–controller (LQG) and sensor–filter (zero-delay Gaussian rate–distortion).

**Synthesis (Eq. 12 / stationary Eq. 18).** The covariance schedule comes from a max-det SDP:
$$\min_{P,\Pi}\ \tfrac12\log\det\Pi^{-1} + \tfrac12\log\det W \quad\text{s.t.}\quad \mathrm{Tr}(\Theta P) + \mathrm{Tr}(WS) \le D,\ \ P \preceq APA^\top + W,\ \ \begin{bmatrix}P-\Pi & PA^\top\\ AP & APA^\top + W\end{bmatrix}\succeq 0,$$
with $\Theta = K^\top(B^\top S B + R)K$. Then $\mathrm{SNR} = P^{-1} - (APA^\top + W)^{-1}$, factored as $C^\top V^{-1} C = \mathrm{SNR}$. The sensor's dimension is $r = \mathrm{rank}(\mathrm{SNR})$.

**Data-rate theorem (Corollary 1).** $\lim_{D\to\infty} DI(D) = \sum_{|\lambda_i|\ge 1}\log|\lambda_i|$. Only the unstable modes need bits for mere stability, independent of $W$.

**Example (§V, Fig. 5).** A random 4-state plant: 6.133 bits/step at $D = 33$ (3-dimensional sensor), 3.266 at $D = 40$ (2-dimensional), 1.602 at $D = 80$ (1-dimensional). The horizontal asymptote is 1.169 bits/step. As the budget falls, the sensor's rank drops in discrete steps (a "phase transition"): the controller attends to fewer and fewer *directions* of the state.

## What it means for the designs

Read the plant state $x$ as the partner's face stream (as the agent perceives it) and $u$ as the agent's entire output. Put an innate cap on $I(\text{partner}^T \to \text{agent output}^T) \le C\cdot T$. Tanaka's structure then says what the *best possible* use of the cap looks like, and therefore bounds what any core can do through it.

- **Sluggishness (derived here, scalar case of Eq. 18; my computation, checked numerically).** Take a partner channel that is a stationary Gauss–Markov level with time constant τ, sampled at dt, with rate C·dt per step. The minimum tracking error is
  $$\frac{P}{\sigma^2} = \frac{1-a^2}{2^{2C\,dt} - a^2} \;\xrightarrow{dt\to 0}\; \frac{1}{1 + C\tau\ln 2},$$
  and the Kalman estimator's pole is $a\,2^{-2C\,dt}$. That gives an effective following time constant
  $$\tau_{\rm est} = \left(\tfrac1\tau + 2C\ln 2\right)^{-1}.$$
  At C = 1 bit/s, a fast partner change is followed with τ_est ≈ 0.72 s at best. At 0.2 bit/s it is ≈ 3.6 s. The lag is forced, not chosen.
- **Held-level tracking is *not* capped.** The best copy fidelity (the regression gain of the MMSE estimate) is $g = C\tau\ln2/(1 + C\tau\ln2)$. Numbers:
  - τ = 0.5 s, C = 1 bit/s: g = 0.26;
  - τ = 5 s: 0.78;
  - τ = 300 s: 0.995;
  - τ = 300 s at C = 0.2 bit/s: still 0.98.

  A held partner level (pitch, posture, mood display) costs almost no bits to follow, so **a rate cap leaks held-level copy almost completely.** This is the quantitative form of the earlier note that the information ceiling is "loose for slow expressions" (tatikonda-2009 note; whole-loop synthesis).
- **Per-channel copy gain is not bounded either.** Mutual information is invariant to scaling and sign. An output $k\hat x$ with k > 1, or −k, costs the same bits as $\hat x$. A rate cap bounds *fidelity* (correlation, coherence, distortion), not gain. In the Gaussian case it is equivalent to a budget on coherence across frequencies, $\int -\tfrac12\log_2(1-|\gamma(f)|^2)\,df \le C$ (standard Gaussian rate formula; not in this paper). Bits can be spent in one band and withheld from another. That is per-band and per-expression allocation, but it is sign-blind.
- **Categorisation into few states.** The rank drop in Fig. 5 is the continuous analogue: under a tight budget the agent "sees" the partner along only one or two learned directions. This is a few-dimensional reading of the partner, not discrete categories.
- **Stochasticity.** The optimum injects Gaussian noise ($v_t$). Lemma 1 shows that a deterministic quantiser does almost as well (within a constant number of bits). So noisy behaviour emerges only if the cap is *implemented* as a noisy channel.
- **Copy non-attracting?** Nothing here. The optimum is determined by D, so copy is attracting exactly when the cost rewards tracking the partner. The cap only says that perfect copying of fast channels is infeasible.
- **Framework.** This is optimal control with an information constraint, so it is excluded as a core. Usable pieces: (i) the directed-information quantity and its data-processing inequality (Lemma 1) as a *constraint* any core can be certified against; (ii) the tracking-error floor above, which holds for every causal policy under the cap, not only the optimal one, because Theorem 1 shows the Gaussian linear policy is optimal among all of them. The lag figure is the lag of the *optimal* follower. A worse policy can lag more, but the result gives no reason to think any policy at this rate can lag less while keeping the same error.

## Verdict
**adopt as a bound, not a mechanism.** It gives the exact rate cost of following a partner, and it shows that the cost vanishes for slow held levels, so a single partner→agent capacity cannot by itself stop held-level copying or cap gain or sign. The lag floor τ_est ≥ (1/τ + 2C ln 2)⁻¹ is the most usable number.
