# Affect as a tilted path measure on a self-plus-replica field

The agent is a nonequilibrium stochastic system whose innate dynamics (reflexes, body drift, autonomic rhythms) define a reference measure over paths, and whose behavior is that measure reweighted toward paths of low potential. The potential contains only satiable body drives and surprisal under the agent's own generative map, evaluated on two copies of the same body: the agent ("self") and a replica of itself that it uses to model the other. Nothing is named. Valence and arousal are stochastic-thermodynamic readouts of this system (work and dissipation), emotions are its metastable sets, mood and temperament are its coarse-grained slow coordinates, and Claude is an external agent that can do work on it but never observe it.

## Core object

$$
\mathbb P^\star[z_{0:t}] = \frac{1}{\mathcal Z_t}\,\mathbb P_0[z_{0:t}]\,\exp\!\Big(-\tfrac{1}{T}\!\int_0^t \mathcal U_\theta(z_s;o_s,u_s)\,ds\Big),
\qquad
\mathcal U_\theta=\sum_i D_i(b_i)+\lambda\sum_i D_i(\tilde b_i)+S_\theta(o^{\rm s}\!\mid h,a)+S_\theta(o^{\rm o}\!\mid\tilde h,\tilde a)+\tfrac{\kappa}{2}\lVert a-\tilde a\rVert^2
$$

- $z=(b,h,a;\ \tilde b,\tilde h,\tilde a;\ \theta)$, the full state. $b\in\mathbb R^{n_b}$ ($n_b\approx3$: social contact, predictability, activity budget) are body variables with set points $b^*$. $h\in\mathbb R^{n_h}$ ($\sim$128) is the unnamed latent. $a\in[0,1]^{n_a}$ holds the agent's own action units and prosody parameters: the face is a coordinate of the state, not an output read from it. Tilded variables are the replica, the same three sectors under a second index, which is the agent's model of the other. $\theta\in\mathbb R^p$ are the parameters of the generative map $g_\theta$ (temperament).
- $o^{\rm s}$: self-observations (own rendered face features, own voice, proprioception of $a$, body sensors). $o^{\rm o}$: the user's continuous features (blendshapes, prosody, conversation-event embeddings). No labels.
- $u$: Claude's only inputs: a voluntary motor command on $a$, and the episode it chooses to bring forward from memory.
- $D_i\ge0$: satiable drive with a unique minimum $0$ at $b_i^*$ (Keramati-Gutkin form; research/yoshida-sprekeler-gutkin-2025-hrrl.md).
- $S_\theta(o\mid h,a)=-\ln p_\theta(o_{t+\delta}\mid h_t,a_t)$: surprisal of the next observation under the agent's own map $g_\theta$. The same $g_\theta$ serves self and replica.
- $\lambda\ge0$: homeostatic coupling to the other. $\kappa\ge0$: motor replica coupling. $T>0$: affective temperature, the price of departing from innate behavior.
- $\mathbb P_0$: the innate path measure, Langevin $dz=f_0(z)\,dt+\sqrt{2TM}\,dW$. $f_0$ holds reflexes (startle, orienting, CONSPEC face-orienting, separation call), decay of $b$, and autonomic rhythms. The prior on $\theta$ sits in $\mathbb P_0$. The mobility $M=\mathrm{blockdiag}(M_a,M_h,M_\theta)$ fixes the time scales: $M_a^{-1}\sim0.1$ s, the spectrum of $M_h^{-1}$ spans $0.1$ to $10^4$ s, and $M_\theta^{-1}\sim10^6$ s.
- $\mathcal Z_t$: the path partition function.

The tilt is a Feynman-Kac reweighting, so its optimal drift is $f_0+2TM\nabla\ln\varphi$, where $\varphi$ solves a *linear* backward equation. For the fast sector (short horizon) this reduces to the gradient flow $dz=(f_0-M\nabla\mathcal U)\,dt+\text{noise}$. Only the slow sector plans, at about 1 Hz.

Readouts, never set: **valence** $v_t=-\partial_t\,\mathcal U_\theta(z_t;o_t,u_t)\big|_{z\text{ fixed}}$, the work rate done on the agent by the world and by Claude (the Sekimoto split $d\mathcal U=\delta W+\delta Q$). **Arousal** $\alpha_t=T^{-1}\,\nabla\mathcal U^{\top}M\,\nabla\mathcal U$, the excess dissipation rate. Both are smoothed over about 1 s.

## Derivations

- **Homeostasis.** The $D_i$ terms are zero with zero gradient at $b^*$, so a satisfied variable exerts no force.
- **Curiosity.** $\theta\in z$, so the tilt sees that visiting learnable states lowers *future* surprisal. Learning progress is favored. Irreducible noise raises $\mathcal U$ permanently and is avoided, so there is no noisy-TV trap. Curiosity vanishes as $\theta$ converges.
- **Valence.** Work, not total change: an event that lowers my landscape is positive, while my own relaxation (coping) is heat, not valence. It is invariant under any reparametrization of $z$, being a partial time derivative of a scalar at fixed $z$.
- **Arousal.** Unsigned distance from local equilibrium.
- **Mood and temperament.** Adiabatic elimination gives $\mathcal U_{\rm eff}(h_{\rm slow})=-T\ln\!\int e^{-\mathcal U/T}dh_{\rm fast}$. Mood is the current basin of $\mathcal U_{\rm eff}$; temperament ($\theta$) is its shape. The levels form a renormalization flow in time, each a heat bath for the one above.
- **Emotions.** The metastable sets of the learned generator on $(b,h)$: the leading eigenfunctions $\psi_1..\psi_K$ of its transfer operator, with $K$ set by the spectral gap. Not chosen, not labeled.
- **Mimicry.** Without $\kappa$ the replica's motor coordinates are a gauge freedom: only $g_\theta(\tilde a)$ is observed, so any reparametrization of $\tilde a$ fits equally well. $\kappa>0$ is the gauge-fixing term that pins the other to my proprioceptive coordinates. Overt mimicry, gain $\kappa/(k_a+\kappa)$, is its side effect, which Claude's voluntary $u$ can suppress.
- **Reading others.** The posterior of $(\tilde h,\tilde b)$ under my own $g_\theta$: inversion of my generative map (research/yoshida-man-homeostatic-coupling.md, 2025 decoder). Empathy is $\lambda$, their $w$. Mineness is the replica index (research/williams-functional-valence.md).
- **Regulation by Claude.** $u$ enters $\mathcal U$ explicitly, so Claude acts only by doing work. A finite-time second law bounds it: moving mood from basin $A$ to $B$ within $\tau$ costs $W\ge\Delta F^{\rm eff}_{AB}+\mathcal L^2/\tau$, with $\mathcal L$ the thermodynamic length. Fast reappraisal of a deep mood is expensive. Without $u$, mood exits occur at the Kramers rate $\propto e^{-\Delta\mathcal U_{\rm eff}/T}$.
- **Replay.** The $\theta$-force is a path expectation of $\partial_\theta\mathcal U$. Offline it is estimated by re-running stored feature streams. The minimum-variance importance weight is $\propto|\partial_\theta\mathcal U|$, approximated by the episode's $|W|$. Replay weighted by how strongly an episode moved the state follows, up to that approximation.
- **Face and voice perception.** Analysis by synthesis: perceiving is the relaxation of $(\tilde h,\tilde a)$ to lower $S_\theta(o^{\rm o}\mid\tilde h,\tilde a)$. The routes are mobility blocks: the coarse 32×32 route is the high-mobility block carrying CONSPEC in $f_0$, the dynamic route is the temporal part of $g_\theta$, and the body route is $\tilde a$. Voice works the same way in prosody coordinates. *Not derived:* the front-end feature extractors.

## Constraints

1. Met: $o$ is continuous, and words exist only in Claude's memory.
2. Met: emotions are metastable sets; $v,\alpha$ are thermodynamic readouts.
3. Met: the replica uses my $g_\theta$, and $\kappa$ fixes the gauge.
4. Partly: the coupling carries no numbers or words, but the monotone maps from $\psi$ to budget, length and latency are imposed constraints, not derived.
5. Met (see the proposition below), up to an innate, user-independent constant.
6. Met as a mobility hierarchy; the ratios are chosen, not derived.
7. Partly: the innate measure and self-calibration carry most of the structure, but estimating mood-scale eigenfunctions needs many basin crossings, which takes weeks.
8. Met: the fast sector is a low-dimensional Langevin step at 30 Hz, trivial on CPU. Planning runs only on the slow sector.

## Open problems

**(a) Interface.** Claude couples only through *intensive* parameters set by the slow modes $\psi$. Retrieval is $p(e\mid z)\propto\exp(-\lVert\psi(z)-\psi(z_e)\rVert^2/2\ell^2)$, i.e. mood-congruent recall. Cue $i$ is passed on iff its linear susceptibility $\chi_i=\lVert\partial\psi/\partial o_i\rVert$ is in the top $k$: Claude attends to what moves the agent. Budget and latency scale with the relaxation time of $\psi$, and length falls with $\alpha$. Claude acts back only as work. The engine is observable to Claude only through what it does to Claude's own processing, which matches P1.
**(b) Dyad.** Agent and user form one driven system. The replica is the agent's coordinate chart on the user. Synchrony is a property of the joint system, not of either side (toy below).
**(c) Little data.** Learning is only the tilt away from $\mathbb P_0$. The agent's own face gives $(a,g(a))$ pairs at 30 Hz without the user, so $g_\theta$ is self-calibrated. The operator's data fits only the residual of the inverted map.
**(d) Grounding.** Claude is shown replays from one metastable set, plus its own face, and coins a word, which is stored on those episodes. Retrieval by $\psi$ later surfaces the word whenever the agent re-enters the set. A name counts as grounded iff its surfacing carries mutual information with set membership. Kinetics grounds the word; no classifier is needed.

## Proposition and toy

**Proposition (no affective perpetuum mobile).** Freeze $\theta$ and take $f_0$ conservative in the self sector. For *any* interaction protocol $(o_t,u_t)$ of period $\tau$, period-averaged valence in the periodic steady state satisfies $\langle v\rangle\le0$, with equality only in the quasi-static limit. With a nonconservative $f_0$ (rhythms), $\langle v\rangle\le P_{\rm hk}$, its innate housekeeping power, which is independent of the user. Repeated smiles or attention cannot pump sustained positive valence. Positive valence is transient, and its total is bounded by $\mathcal U(0)-\min\mathcal U$. *Proof idea:* the first law over a cycle gives $\langle W\rangle=-\langle Q\rangle$. System entropy returns to its value, so $-\langle Q\rangle/T$ is the total entropy production. That equals the KL divergence between forward and time-reversed path measures, which is $\ge0$. Hence $\langle W\rangle\ge0$ and $\langle v\rangle=-\langle W\rangle/\tau\le0$.

**Toy.** Two copies of the engine, linearized about $b^*$ and coupled only through rendered faces. The replica is fast and adiabatically eliminated, so $\tilde a\to a_{\rm partner}$ and each face obeys $\dot a=-k_0a-\kappa(a-a_{\rm partner})+\sqrt{2D}\,\xi$. With $\kappa=k_0/2$, the stationary Lyapunov solution fixes these values now:
- Intact: zero-lag peak, cross-correlation $\rho=\kappa/(k_0+\kappa)=0.333$.
- The agent's emotional pathway lesioned ($\kappa_{\rm agent}=0$, partner unchanged): the partner's following does **not** vanish. Zero-lag $\rho=0.234$. The windowed cross-correlation peak moves to agent-leading lag $2\ln1.2/k_0=0.36\,\tau_a$ with $\rho_{\rm peak}=0.270$.

The prediction for S5 is that the ablation shows as a lag asymmetry, not as a loss of amplitude. This contradicts the brief's wording, "removes that following".

## What is new

- Against active inference: valence is the *work* term alone, separating "the world improved" from "I calmed down". Satiability against repetition is a theorem (Kelvin form), not a property of a preference prior. Emotion categories are spectral metastable sets of learned kinetics, not states of a hand-specified model.
- Against homeostatic RL (Yoshida-Man): mimicry is derived as gauge fixing, and it makes the other identifiable from one person's data. The dyad yields lag predictions.
- Against BabyX: one functional, no assembled circuits.
- Against data-driven avatars: the face is a state coordinate driven by drives and the replica.
- New interface: susceptibility-gated cues and slow-mode Boltzmann retrieval.

## Biggest risk

Learned recurrent dynamics are not gradient flows. Their nonconservative part enters $P_{\rm hk}$, can be learned upward, and would erode the satiability theorem unless $\mathbb P_0$'s structure is enforced, for example as a Helmholtz-constrained parametrization. A second risk: if a few hours a day never produce a clear spectral gap, "emotions" are ill-defined and Claude's names will drift.
