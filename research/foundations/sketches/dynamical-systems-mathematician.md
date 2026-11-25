# The mirrored slow-fast flow

Lens: a mathematician of dynamical systems.

The agent is one stochastic slow-fast flow on its own body, face and latent state, plus a second copy of that flow driven by the other person's face seen in the agent's own motor coordinates. Affect is the flow's geometry, never a variable in it: arousal is dissipated power, valence the drift of the forecast body drive, emotions the metastable sets of the transfer operator, mood the position along the slowest Koopman coordinates. Reading another person is the copy synchronizing to them; mimicry is the copy leaking into the self. Claude sits outside the flow: it receives only the slow coordinates, recast as processing settings, and acts back only as impulses its own perceived words cause.

## Core object

$$
\begin{aligned}
T\dot x &= -(K_\theta + J_\theta)\,\nabla_x V_\theta(x;m) + \phi(x,o) + \kappa P(\hat x - x) + \textstyle\sum_k B\,e_k\,\delta(t - t_k) + \Sigma\dot W \\
T\dot{\hat x} &= -(K_\theta + J_\theta)\,\nabla_x V_\theta(\hat x;m) + \phi(\hat x,\hat o) + L\,(y - C\hat x) \\
\tau_m \dot m &= \psi_\theta(x) - m, \qquad u_k = \Gamma\big(m(t_k)\big), \qquad V_\theta(x;m) = D\big(\beta_\theta(x)\big) + U_\theta(x;m)
\end{aligned}
$$

**State.**
- $x = (a, b, h)$ is the agent's own state.
  - $a \in [0,1]^{n_a}$: own action units plus voice parameters, $n_a \approx 20$.
  - $b \in \mathbb{R}^{n_b}$: innate body variables (contact, predictability, energy), $n_b \approx 3$.
  - $h \in \mathbb{R}^{d}$: unnamed latent state, $d \approx 64$ to $256$.
- $\hat x = (\hat a, \hat b, \hat h)$: the mirror copy, the other person as one's own body would be if producing what is seen.
- $m \in \mathbb{R}^{k}$, $k \approx 4$: mood, the running average of the slow coordinates $\psi_\theta$.

**Dynamics.**
- $T = \mathrm{diag}(\tau_a, \tau_b, \tau_h)$: $\tau_a \approx 50$ ms, $\tau_h \approx 0.3$ to $3$ s, $\tau_b$ minutes; $\tau_m$ 10 minutes to 3 hours; $\theta$ changes over days to weeks.
- $K_\theta \succeq 0$: symmetric dissipation metric; $J_\theta = -J_\theta^\top$: circulation (non-dissipating rhythms and cycles). Both have zero $b$-rows, so the agent cannot set its own body.

**Objective terms.**
- $D(b) = \tfrac12 (b - b^*)^\top W (b - b^*)$: the innate satiable drive, $W \succ 0$, set point $b^*$.
- $\beta_\theta(x)$: learned forecast of the body a horizon $H$ ahead; since $\nabla_{a,h} D(\beta_\theta) \neq 0$, the drive moves face and latent state.
- $U_\theta$: learned landscape; its basins' depth and number are temperament.

**Inputs and coupling.**
- $\phi$: fixed body physics and exteroceptive input: $\phi_b = -\Lambda(b - b_0) + G(a,o)$ (decay plus satiation by contact); for $h$, conversation events and context $o$; $\hat o$ is the other's context as inferred.
- $y \in \mathbb{R}^{n_a}$: the other's face and prosody in the agent's own motor coordinates (body route). $C$: projection onto $a$. $L$: observer gain.
- $\kappa \ge 0$, $P$: leak from copy to self; $P$ projects onto $a$ (optionally $h$), never onto $b$.

**Claude coupling.**
- $t_k$: turn times. $e_k$: Claude's reply as the engine perceives it (prosody, reply embedding as a conversation event, rendered image of its own face); $B$ its input map.
- $u_k$: Claude's processing settings (retrieval bias, thinking budget, reply length, latency, cue gating); $\Gamma$ a fixed map from $m$. $\Sigma\dot W$: noise.

**Learning.** A single functional on the agent's own stream:
$$\mathcal{E}(\theta) = \mathbb{E}_{\text{self}}\big[\lVert y^{\text{self}}_{t+\Delta} - C\hat x_{t+\Delta}\rVert^2 + \lVert b_{t+H} - \beta_\theta(x_t)\rVert^2\big].$$
The copy is trained by synchronizing it to the agent's own face, the same operation it later performs on the other's face.

## Derivations

- **Homeostasis.** Without input, $\dot V = -\nabla V^\top K \nabla V \le 0$ (the skew part contributes nothing). The drive pulls only while the forecast body is off $b^*$; at the set point the gradient vanishes, so satiation holds by construction.
- **Arousal.** $\alpha = \nabla V^\top K \nabla V$, dissipated power: high far up a steep slope (after a startle), zero at rest.
- **Valence.** $v = -\tfrac{d}{dt} D(\beta_\theta(x))$, the Lie derivative of the forecast drive along the flow: signed, graded, anchored only to innate body variables.
- **Emotions, moods, temperament.** Singular perturbation theory gives a normally hyperbolic slow manifold $M_\varepsilon$ along which mood $m$ moves. An emotion episode is a fast excursion off $M_\varepsilon$ and back; emotion types are the almost-invariant sets of the transfer operator at a lag of seconds, their number fixed by the spectral gap. Temperament is the barrier heights of $U_\theta$.
- **Curiosity.** Partly. On the satiated set $\nabla D = 0$, so noise and $J$ make the state wander and cycle along neutral directions: exploration and play-like rhythms, not directed information-seeking.
- **Mimicry.** $\kappa P(\hat x - x)$ pulls the own face toward the copy's, with latency about $1/L + 1/\kappa$. The term is a stated constraint (self and copy share one substrate); its properties are derived.
- **Reading others.** The copy is a synchronization observer built from one's own dynamics; $\hat b, \hat h$ are the other's body and latent state, inferred by inverting one's own generative flow through time (proposition below).
- **Face and voice perception.** Analysis by synthesis in dynamical form: synchronize a copy of one's own face-generating flow to what is seen. Each route is a measurement channel $C_i y_i$ into the one observer: fast coarse (large $L_i$, low resolution), dynamic (the copy's $\hat h$), body (into $a$-coordinates). Context enters through $\hat o$.
- **Regulation by Claude.** A reply's jump $Be_k$ changes the emotion only if it crosses a separatrix: shallow basins yield to one reappraisal, deep ones need repeated jumps plus the drift of $m$. The mechanism is derived; what Claude says is not.
- **Replay.** Offline, stored $y$ and own streams drive both equations while $\theta$ descends $\mathcal{E}$, each episode weighted by $\int \alpha\,dt$. Derived: barrier heights are set by rare transitions between metastable sets, so an unbiased gradient under the invariant measure must importance-weight them.

## Constraints

1. **Met.** Inputs are action-unit and prosody coordinates; emergent sets have no names until Claude gives one.
2. **Met.** Valence and arousal are functionals of the flow, emotions are spectral sets; only body variables are named.
3. **Met.** The copy is the agent's own flow; mimicry is its leak into the self.
4. **Met.** Claude receives $u_k = \Gamma(m)$ only; its effect returns only as perceived impulses.
5. **Partly.** $D$ is satiable and nothing rewards smiles, but if $P$ touched $b$ the drive would depend on the other's face, a route to flattery. Excluding $b$ from $P$ is a stated restriction, not derived.
6. **Met.** A singular-perturbation hierarchy with gaps of 10 or more between levels.
7. **Partly.** Self-data is unlimited (motor babbling through the agent's own renderer trains the copy); the operator's hours fit only the mismatch residual. Whether that transfers to a human face is the main risk.
8. **Met.** Two ODEs with $d \le 256$ at 30 Hz cost microseconds per step on a CPU.

## Open problems

- **(a) Interface.** A turn lasts much longer than $\tau_h$, so by averaging only coordinates with $-1/\ln|\lambda_j| > T_{\text{turn}}$ ($\lambda_j$ a Koopman eigenvalue) have a well-defined value over a turn; faster ones alias. Hence $\Gamma$ must factor through the slow Koopman coordinates $\psi_\theta$, and the interface's rank is the number of eigenvalues past the cutoff. The loop $m \to u \to$ reply $\to e_k \to x$ is sampled-data feedback; a small-gain condition separates converging regulation from runaway (terse replies that provoke the user and agitate the agent further).
- **(b) Dyad.** Person, self and copy form one coupled system. Below a critical coupling $\kappa^*$, set by the conditional Lyapunov exponent on the face-synchrony manifold, the dyad shows only generalized synchronization; above it, it locks (echopraxia). Near $\kappa^*$ synchrony is on-off intermittent, predicting synchronized-episode durations in windowed cross-correlation with a power-law exponent of $-3/2$. Design places $\kappa$ just below $\kappa^*$.
- **(c) Scarce data.** Innate structure carries the load: $D$, $\phi_b$, the gradient-plus-skew form, $C$, an echo-state-like contracting core. The self-stream trains the observer; human data estimates only the mismatch $w$.
- **(d) Grounding.** A concept is an almost-invariant set, named by Claude from replays drawn from it. Grounding is testable as agreement (adjusted Rand index) between the partition of episodes by Claude's names and the spectral partition.

## Proposition (reading by synchronization)

Assume the other evolves as $\dot x_H = F_\theta(x_H; m_H) + w(t)$ with $|w| \le \bar w$ ($F_\theta$ the flow above); the virtual system $\dot z = F_\theta(z;m) - LCz + LCx_H(t)$ contracts at rate $c_L$ in a metric $M$; and the two moods tilt the flow by at most $\mu$. Then
$$|\hat x(t) - x_H(t)|_M \le e^{-c_L t}\,|\hat x(0) - x_H(0)|_M + \frac{\bar w + \mu}{c_L},$$
independent of $\kappa$.

Proof idea: $x_H$ solves the virtual system up to a bounded perturbation; Gronwall on the differential length in $M$ gives the bound, and $\kappa$ appears only in the self equation.

Corollaries. $\kappa = 0$ abolishes mimicry and spares reading; $L = 0$ abolishes both. In directions undetectable through $C$, contraction fails and $\hat x$ relaxes to the agent's own attractor under its own $m$: mood-congruent projection, derived rather than added. $F$ itself may be multistable (the agent has emotions); only $F - LC$ must contract.

**Toy simulation.** A and B share one random gradient-plus-skew flow ($d = 16$, $n_a = 4$, $n_b = 2$, 3 attractors in $h$). B sees only A's $a$ plus noise ($\sigma = 0.05$), with $L = 10\,\text{s}^{-1}$, $\kappa = 3\,\text{s}^{-1}$, over 10 simulated minutes. Predictions fixed now:
- Same $\theta$: $R^2(\hat b, b_A) \ge 0.8$. A's $U_\theta$ redrawn: $R^2 \le 0.3$.
- $\kappa = 0$: reading $R^2$ changes by less than 0.02; the correlation of B's $a$ with A's $a$ falls from at least 0.5 to at most 0.1.
- B's face lags A's at the cross-correlation peak by 0.25 to 0.45 s, inside the 0 to 1,000 ms windows Dimberg and Thunberg 2012 used to score rapid facial reactions.

## What is new

- **Active inference** sets valence from free energy or policy precision. Here valence and arousal are geometric functionals (dissipated power, Lie derivative of the forecast drive), emotion types are transfer-operator sets, and the Claude interface is constrained by the Koopman spectrum.
- **Homeostatic RL (Yoshida and Man)** reads others with a static decoder trained by MSE on own (expression, state) pairs, and makes empathy the reward term $w D_{\text{partner}}$. Here reading is a dynamical observer with a contraction error bound that recovers latents no single frame contains; empathy is a state leak; there is no RL.
- **BabyX** is a module assembly with no Lyapunov function; here mimicry latency and the ablation dissociations come from one flow.
- **Data-driven avatars** model $p(\text{face} \mid \text{context})$ from human video; here there is no human video, and the face is the projection $Ca$ of a regulated state.
- **The dyad.** No prior work in the brief predicts a critical coupling, echopraxia as the locked regime, or the $-3/2$ intermittency law.

## Biggest risk

The "like me" assumption may fail at scale. A human is not $F_\theta$, the MediaPipe coordinates are borrowed, and display rules differ, so $\bar w / c_L$ may be vacuous and the copy may track the face but not the person. Making $F - LC$ contract may need gains so high that the copy just echoes $y$ and recovers nothing hidden. And a few hours of data may never give $U_\theta$ metastable sets sharp enough to name.
