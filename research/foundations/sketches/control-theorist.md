# Affect as the forced structure of a robust homeostatic regulator

**Idea.** Pose one problem, not a model: keep the body variables at their set points, robustly, while another person keeps disturbing them. The internal model principle says any controller that solves this robustly *must* contain a dynamical copy of whatever generates the disturbance, so a social regulator is forced to carry a model of the other. The engine is that regulator. Mood is its integral state, reading others its internal model, mimicry that model's steady-state output, temperament the shape of its sensitivity function. Claude is an unmodeled slow outer loop, coupled by gain scheduling and kept safe by a small-gain bound. Each component is a necessary condition of the problem or an explicit constraint on it.

## Core object

The regulator problem, and the structure it forces:

$$
\begin{aligned}
&\textbf{Problem: } \text{find } (\xi, m, \theta)\text{-dynamics such that } \forall\, x_o \in \mathcal X_\theta:\quad \dot V \le -\alpha(\|z\|) + \gamma(\|\nu\|),\qquad e(t)\to 0 .\\[2pt]
&\dot b = \phi(b) + u + w(x_o) \qquad\qquad\qquad\qquad\ \ \text{(body)}\\
&\dot m = \nabla d(e) - \varepsilon_m m \qquad\qquad\qquad\qquad\ \text{(mood: leaky integral)}\\
&\dot \xi = F_\theta(\xi, a) + \hat c\, L\,(y - G(\xi)) - \Gamma_\theta^{\top}\nabla d(e) \quad \text{(internal model of the other)}\\
&u = -K\nabla d(e) - K_I m - H_\theta \xi, \qquad a = G\big(R_\theta[e;m] + \kappa\,\xi\big)\\
&\dot\theta = -\eta\,\Phi^{\top}\!\nabla d(e) - \eta\,\sigma_\theta(\theta - \theta_0), \qquad s = S(m, \xi, \|\partial u/\partial z\|) \to \text{Claude}
\end{aligned}
$$

Symbols:
- $b\in\mathbb R^{n_b}$ are the innate body variables (contact, predictability, activity budget). $b^*$ is the innate set point and $e=b-b^*$.
- $d(e)=(\sum_i|e_i|^n)^{1/m'}$ with $m'>n>1$ is the satiable drive (research/yoshida-sprekeler-gutkin-2025-hrrl.md).
- $\phi$ is body drift; $u$ is internal regulatory action.
- $x_o$ is the other's unobserved state, in the class $\mathcal X_\theta$ of systems built from the agent's *own* generator $(F_\theta, G)$; $w(x_o)$ is its effect on the agent's body.
- $y\in\mathbb R^{n_y}$ are the perceived features: AUs or blendshapes, prosody, conversation events (Claude's own utterances included).
- $\xi\in\mathbb R^{n_\xi}$ (a few hundred dimensions) is the internal model of the other: a learned state-space model in the coordinates of the agent's own face and voice generator $G:\mathbb R^{n_\xi}\to\mathbb R^{n_a}$.
- $\hat c\in[0,1]$ estimates how strongly the other moves this body, identified by recursive least squares from $(e,y)$ from an innate start $\hat c_0$, with no leakage. $L$ is the innate observer gain.
- $m\in\mathbb R^{n_b}$ is mood, with leak $\varepsilon_m$ of order $10^{-3}$ to $10^{-4}\,\mathrm s^{-1}$.
- $a\in\mathbb R^{n_a}$ is the own action-unit and voice output. $R_\theta$ is the expressive map, and $\kappa\in[0,1)$ is the motor leak of the internal model.
- $\theta$ are slow parameters (temperament), with innate prior $\theta_0$ and leakage $\sigma_\theta$. $\Phi$ is the regressor.
- $z=(e,m,\xi-\xi^\star,\theta-\theta^\star)$ is the closed-loop error state. $V$ is its ISS-Lyapunov function, and $\nu$ collects unmodeled inputs: Claude's events and out-of-class behavior of the other.
- $s$ is Claude's processing schedule: retrieval bias, thinking budget, reply length, latency, cue mask, and the rendered self-face.

## Derivations

- **Homeostasis.** The objective $e\to0$. Satiable: at $e=0$ with no disturbance, $u=0$, and overshoot raises $d$.
- **Mood.** The internal model principle for step-like disturbances forces an integrator, $m$: unresolved error accumulated over minutes to hours.
- **Reading others.** The internal model principle applied to structured disturbances forces a generator of $w$, which is $\xi$. Building it from the agent's own $(F_\theta,G)$ makes perception an observer that inverts the agent's own generative map. The other's body error is read as $\hat e_o=R_\theta^{+}\xi$: "what state of mine would make me look like that."
- **Mimicry.** At steady state the regulator's output must cancel $w$. The generator that produces it lives in motor coordinates, so $\kappa G(\xi)$ is a copy of the other's expression whose amplitude scales with $\hat c$ (Proposition). This fits the finding that rapid facial mimicry appears only in high-empathy viewers (research/dimberg-thunberg-2012-rapid-facial-reactions.md).
- **Valence.** $v=-\dot V$, read out. The dissipation inequality gives $v\ge\alpha(\|z\|)-\gamma(\|\nu\|)$: negative valence requires something pushing on the agent.
- **Arousal.** $\rho=\|\partial u/\partial z\|$ is the instantaneous loop gain, read out. Because $\nabla^2 d$ grows with deficit, arousal rises with need. Through $s$, arousal sets face time constants and reply latency.
- **Curiosity.** Partly derived, from dual control: under parameter covariance $P_\theta$ the cost-to-go contains $\mathrm{tr}(Q P_\theta)$, so the optimal action probes, and probing stops (satiates) once $P_\theta$ no longer raises expected $d$. The tractable one-step approximation is a design choice.
- **Regulation by Claude.** An output-feedback outer loop measuring the conversation and its rendered face, never $z$. Its utterances enter $y$ as context, changing the observer innovation, hence $\xi$ and the predicted disturbance. That is reappraisal: Claude changes the estimate of the other, not the body. Time-scale separation keeps the cascade stable.
- **Replay.** The adaptive law run offline on stored feature streams, choosing segments that maximize the minimum eigenvalue of $\sum\Phi^\top\Phi$ (E-optimal excitation): in practice, where the state moved most.
- **Face and voice perception.** The observer term itself: the fast coarse route is a high-gain, low-dimensional observer (fast, noise-amplifying), the dynamic route a low-gain, high-dimensional one, the body route $G$.
- **Time scales.** Reflex at 30 Hz, observer about 1 s, mood minutes to hours, $\theta$ weeks; singular perturbation needs each layer ISS and bandwidth ratios of at least 10.
- **Temperament.** Bode's sensitivity integral, $\int_0^\infty \ln|S(j\omega)|\,d\omega \ge 0$ for loops of relative degree two or more, says reactivity cannot be suppressed at every frequency. Temperament is where $\theta$ puts the bulge: calm toward slow events and jumpy toward fast ones, or the reverse.

## Constraints

1. No labels below the language layer: **met**.
2. Emergent emotion: **partly met**. Valence and arousal are read out and regimes are unnamed, but body variables are named (permitted as innate).
3. Others read through one's own body: **met**. $\xi$ lives in the coordinates of the agent's own $G$, and $\hat e_o=R_\theta^+\xi$.
4. Frozen Claude without the state in words: **met**. The state reaches Claude only through $s$.
5. Satiable drives: **met, provably**. $u\to0$ at the set point, and nothing rewards the user's smiles.
6. Time scales: **met**, by the stated separation ratios.
7. Little data: **partly met**. Structure is innate and leakage bounds $\theta$ without persistent excitation; whether $\xi$ can be learned in hours is open.
8. Real-time face on CPU: **met**. A small SSM plus an observer is cheap at 30 Hz.

## Open problems

**(a) Interface theory.** Treat Claude as an unmodeled operator $\Delta_C$ from schedule $s$ to events $\nu$. The interface must satisfy two bounds, an *interface sector*:
- *Safety.* Small gain, $\|\Delta_C\|\cdot\|T_{s\leftarrow\nu}\|<1$, so no utterance can destabilize mood.
- *Influence.* The map from slow state $(m,\hat e_o)$ to Claude's behavior features must be observable (rank $\ge \dim m$), so the state demonstrably moves how Claude acts.

Both gains are measurable by perturbing $s$.

**(b) Dyad.** Each agent's face is the other's exosystem. For linearized copies, mutual mimicry stays bounded if $\kappa_A\kappa_B\hat c_A\hat c_B\|G\|^2<1$ (small gain). Near and above that bound, a self-sustained shared rhythm can appear: synchrony as a small-gain crossing.

**(c) Little data.** Innate structure carries almost everything (internal-model form, set points, own $G$, reflexes). Only $\theta$ is learned, with leakage that keeps it bounded even without excitation, so stability never depends on learning succeeding.

**(d) Grounding.** Candidate concepts are the closed loop's recurrent regimes: which body directions are in error, which modes of $\xi$ are active, the sign of $v$. Claude names a regime by watching a replay of its own rendered face and the conversation; the name stays in the language-layer memory index, never fed down. The clustering rule itself is **not derived**.

## Proposition and toy

**Proposition (mimicry is forced, and proportional to coupling).** Take the linearized loop with $\dot b=-\lambda b+u+c\,y_u$, where $y_u$ is generated by a neutrally stable finite-mode system. Every controller that achieves robust asymptotic regulation contains a generator whose output converges to $-c\,y_u$. If that generator is realized in motor coordinates, the expressed copy has amplitude linear in $c$ and vanishes at $c=0$.

*Proof idea.* The regulator (Sylvester) equations have a unique solution under non-resonance, which gives $u_{ss}=\lambda b^*-c\,y_u$ exactly. The internal model principle says this signal must be generated inside the controller.

**Toy simulation.**
- Scalar body with $\lambda=0.1$. User rhythm $y_u=\sin(1.57t)$, $c\in\{0,0.25,0.5,1\}$.
- Proportional-integral controller ($k_p=1$, $k_I=0.1$) with and without an adaptive-frequency internal model. The internal model starts at $\hat\omega_0=1.0$ and $\hat c_0=0.5$, with $\kappa=0.3$.

Predictions, fixed now:
1. Proportional-integral only: steady RMS error $=0.379\,c$ (±5%), computed analytically from $|s/(s^2+1.1s+0.1)|=0.536$ at $\omega=1.57$.
2. Intact: RMS error at most 5% of (1) after 120 s.
3. Mimicry: the face channel's peak $|r|$ with $y_u$ is at least 0.9 at $|\text{lag}|\le0.25$ s. Its amplitude is linear in $c$ ($R^2\ge0.98$).
4. At $c=0$, mimicry decays to within the noise floor within 10 min as $\hat c\to0$: innate indiscriminate mimicry pruned to those who matter.

## What is new

- **Active inference.** There the agent predicts everything it observes; here it models the other only in the subspace that disturbs its body, so mimicry and empathic reading scale with body coupling, a dissociation active inference does not predict. Added guarantees: an ISS bound on valence, a small-gain safety bound on the language model.
- **Homeostatic RL (Yoshida and Man).** There, coupling to the partner is a hand-set weight $w$ added to the drive, and behavior is learned by deep RL over $10^4$ to $10^7$ steps (research/yoshida-man-homeostatic-coupling.md). Here, coupling is forced by the internal model principle, the regulation law is innate, and only $\theta$ is learned.
- **BabyX and data-driven avatars.** BabyX is an assembly with no theorem linking its parts; avatars mimic because people mimic in the data. Here mood, the model of the other, mimicry and temperament follow from one regulation problem, and mimicry amplitude is a lesionable consequence of internal coupling.

## Biggest risk

The internal model principle is exact only for disturbances from a finite-dimensional, neutrally stable class, and people are neither; outside it the copy is approximate and "forced" weakens to "favored." Second, a perfect regulator would be affectless: affect lives in transients and the Bode bulge, so gains too high yield a flat agent. Third, $c$ (how the other moves "contact" or "predictability") is partly a design decision. If it is set by hand, mimicry ∝ $c$ is engineered, not emergent.
