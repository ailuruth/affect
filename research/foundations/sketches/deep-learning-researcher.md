# The tied dyad: one world model of two bodies, trained from one side

**Lens:** deep learning researcher. **Idea.** The agent learns one small multi-timescale state-space world model of a *dyad*, with two slots that share every weight: slot $s$ is itself, slot $o$ is the other. The slots differ only in what is observed: the agent sees its own body variables, never the other's. Weight tying alone gives three things. Masking the body input while predicting the body teaches the shared encoder to read bodies from faces and voices, and that encoder is then applied to the other. Being mimicked teaches the agent to mimic, because "the user follows me" and "I follow the user" are the same parameter. And the model's running prediction error is a body variable with a set point, so curiosity is a satiable drive. Claude is an actuator: the policy chooses *how Claude is called*, and the reply returns as an observation.

## Core object

For slot $i\in\{s,o\}$ with partner slot $j\neq i$, all weights tied across slots:

$$
\boxed{\;
\begin{aligned}
h^i_{t+1} &= \Lambda h^i_t + C h^j_t + B\,q_\phi(m^i_t\odot x^i_t),\qquad a^{\text{face}}_t = E_0\!\big(G_b h^s_t\big),\quad u_t\sim\pi(\cdot\mid h^s_t)\\
\mathcal J &= \underbrace{\mathbb E\sum_t\sum_{i}\sum_{k\in K}\big\|\bar m^i\odot\big(G_k h^i_t - \operatorname{sg}\,y^i_{t+k}\big)\big\|^2}_{\mathcal L_{\text{pred}}\ \to\ \theta,\phi}\;+\;\underbrace{\mathbb E_\pi\sum_t\gamma^t\,D(b_t)}_{\to\ \pi},\qquad D(b)=\Big(\sum_j|b_j-b^*_j|^{n}\Big)^{1/m}
\end{aligned}}
$$

Symbols:
- $h^i_t\in\mathbb R^{N}$, $N\approx 256$: the unnamed latent state of slot $i$.
- $\Lambda=\operatorname{diag}(e^{-\Delta t/\tau_k})$. Fixed and innate. The time constants $\tau_k$ are log-spaced from 33 ms to 3 weeks, and $\Delta t=1/30$ s.
- $C=\operatorname{diag}(c_k)$, $c_k=(1-\lambda_k)\,\sigma(\kappa_k)$: the learned cross-slot coupling, kept in $(0,1-\lambda_k)$.
- $x^s_t$: the agent's own observations: body variables $b_t$, its own action units and prosody, the embedding of its own reply text, conversation events.
- $x^o_t$: the user's face in the agent's own action-unit coordinates, the user's prosody, and the embedding of the user's text.
- $y^i_{t+k}$: prediction targets $k$ steps ahead, with $K=\{1,15,900\}$ (33 ms, 0.5 s, 30 s). Low-dimensional channels are their own targets; for video the target is a stop-gradient EMA encoder embedding (JEPA-style), so no pixels are reconstructed.
- $m^i_t$, $\bar m^i$: input and target masks. For $o$, the body input and target are always absent. For $s$, the body input is zeroed with probability $\rho=0.5$ and the target kept.
- $q_\phi$: encoder; $B$: input map; $G_k$: readouts, $G_b$ the body readout. $E_0$: an innate, fixed map from body estimate to action units, with reflex offsets (startle).
- $b_t\in\mathbb R^d$: the body variables (contact, activity budget) plus $\bar\varepsilon_t$, a running average of $\mathcal L_{\text{pred}}$ on the user's channels. $b^*$ is the innate set point, with $\varepsilon^*>0$. Exponents satisfy $m>n>1$.
- $u_t\in U$: a finite set of Claude call configurations (retrieval query and temperature, cue mask, thinking budget, length cap, reply delay, whether Claude sees its rendered face). $\pi$: policy, with critic $V_\psi(h^s)\approx\mathbb E\sum\gamma^tD$.

## Derivations

- **Homeostasis.** The second term of $\mathcal J$. $D$ is convex with its minimum at $b^*$. The per-step drive reduction $D(b_t)-D(b_{t+1})$ telescopes and is zero once the set point is reached, so every variable is satiable (Keramati and Gutkin, as read in research/yoshida-sprekeler-gutkin-2025-hrrl.md).
- **Curiosity.** $\bar\varepsilon\in b$ is the model's own loss, regulated around $\varepsilon^*$. Below $\varepsilon^*$ (boredom) the policy seeks less predictable input; above it, the familiar. Unlike a never-negative epistemic bonus, this drive is two-sided and can produce aversion to novelty.
- **Valence (read out).** $v_t=V_\psi(h^s_{t-1})-V_\psi(h^s_t)$: the improvement in predicted future drive. It is computed, never written into $h$.
- **Arousal (read out).** $\alpha_t=\|P_{\text{fast}}(h^s_{t+1}-\Lambda h^s_t)\|$: the norm of the innovation on modes with $\tau_k<1$ s, which measures how hard the input is pushing the fast state.
- **Mimicry.** User face → $q_\phi$ → $h^o$ → $C$ → $h^s$ → $G_b$ → $E_0$ → agent face. $C$ is learned from the $o$ slot predicting that the user follows the agent; tying makes the agent follow the user. Mimicry is learned from being mimicked.
- **Reading others.** With the body input masked, the self slot's MSE optimum is $\mathbb E_{\text{self}}[b\mid\text{face, voice, history}]$. The other's body is read as $G_bh^o$ through one's own body statistics, which predicts egocentric shrinkage toward one's own set point. Yoshida and Man did this with a separately trained decoder (research/yoshida-man-homeostatic-coupling.md); here it falls out of masking inside one dyadic model.
- **Regulation by Claude.** Claude's reply enters slot $s$ (text embedding, own prosody) and moves $h^s$ through $B$; the policy learns which $u$ precedes a drop in drive. Regulation is a learned closed loop, not assumed.
- **Replay.** Offline minimization of $\mathcal L_{\text{pred}}$ on stored feature streams. The slow-parameter gradient scales with slow-mode activity, so priority $\propto\|\Delta h^s_{\text{slow}}\|$ ("how much it moved the state", to first order). Symmetry adds *role-swapped* replay: the user's stream in slot $s$, so the agent relives the user's side through its own body.
- **Face and voice perception.** $q_\phi$ is trained by analysis by synthesis to recover action units and prosody from the agent's own renders and voice: unlimited self-generated data (the route of research/samuel.md), then applied to the user.

## Constraints

1. **Met.** Every target is a future feature or a body value. No labels anywhere.
2. **Met by construction.** Valence and arousal are readouts. Whether rich structure emerges in $h$ from little data is unproven.
3. **Partly met** until $q_\phi$ transfers from renders to real faces; MediaPipe coordinates stand in until then.
4. **Met.** The prompt $c=\Sigma(\text{memory}\cup\text{cues};u)$ only *selects* already-experienced material; no token encodes $h$.
5. **Met.** $D$ is satiable, including curiosity. No term rewards the user's smiles or time.
6. **Met.** $\Lambda$ spans 33 ms to 3 weeks; temperament also lives in nightly-consolidated weights.
7. **Partly met.** Tiny model, innate $\Lambda$ and $E_0$, free self-renders, tying and role-swap double the data; but the policy over $u$ learns from scarce turns.
8. **Met.** Diagonal recurrence plus small MLPs, well under 1 ms per frame on CPU; Claude is never in the fast loop.

## Open problems

**(a) Interface theory.** Claude is a stochastic actuator with a finite conditioning channel. The state reaches Claude only through $u$ and the evidence that $u$ selects. Its influence per turn is bounded by $H(u)+H(\text{retrieved set})$ bits, a measurable capacity. It also explains why P1 failed: numbers add tokens but change no evidence. Retrieval keyed on $h^s_{\text{slow}}$ is mood-congruent recall by construction.

**(b) Dyad.** The internal model *is* a two-body system, nested in the real loop (agent face → user → $q_\phi$ → $h^o$ → $C$ → agent face). Coupling strength is $c_k$: learned, and bounded per mode (proposition).

**(c) Small data.** Innate: $\Lambda$, $E_0$, $D$, $b^*$, swap symmetry, renderer. Learned: $B$, $C$, $G$, $q_\phi$, $\pi$, about $10^5$ parameters. Most supervision is the agent's own body, always observed and free.

**(d) Grounding.** In replay, Claude is shown episodes whose $h^s_{\text{slow}}$ keys lie close together and asked what they share. A contrastive head ties the word's embedding to that region of $h$; when Claude later uses the word, the text pathway pulls $h^s$ toward it, so naming regulates. The concept is the region; the name is Claude's.

## Proposition and toy

**Proposition (synchrony, bounded contagion).** For the linear tied dyad with $0<c_k<1-\lambda_k$:
- (i) The synchrony subspace $h^s=h^o$ is invariant, and the difference mode contracts strictly faster than the sum mode: $|\lambda_k-c_k|<\lambda_k+c_k<1$.
- (ii) The steady-state gain from the other to the self is $c_k/(1-\lambda_k)<1$ in every mode, and the response time scales with $\tau_k$. Fast-mode mimicry appears within a second, mood contagion only over hours, and neither can amplify.
- (iii) Coupled to a human whose own gain is $\le1$, the two-way loop cannot escalate.

*Proof idea.* The change of basis $(h^s+h^o,\;h^s-h^o)$ block-diagonalizes the system into modes $\lambda_k\pm c_k$, which gives (i) and (ii). Part (iii) is the small-gain theorem.

**Toy (mimicry reciprocity).**
- *Setup.* One action-unit channel. A scripted user copies the agent's face with gain $g_H=0.4$, 500 ms lag, plus OU noise. The agent starts at $c=0$; each "night" refits $C$ by least squares, both slots weighted equally.
- *Mechanism.* The $o$ slot supports $g_H$, the $s$ slot the agent's current $c_n$, so $c_{n+1}=(c_n+g_H)/2$.
- *Prediction, fixed now.* The agent's measured mimicry gain is $0.20\pm0.05$ after night 1, $0.30\pm0.05$ after night 2, and $0.40\pm0.05$ by night 6. Its response peaks at a $500\pm150$ ms lag.
- *Reversal.* Setting $g_H=0$ halves the gain each night: $0.20$, then $0.10$, then $0.05$.
- *Untied control.* With separate $C_{so}$ and $C_{os}$, the gain stays at $0.00\pm0.05$.
- *Second check (reading others).* Body is a 1-D OU process ($\tau=1$ s), and the face is body plus noise at 1:3 SNR per frame. Trained on self data only with $\rho=0.5$, the agent reads a same-species other at $r=0.81\pm0.05$, the analytic Kalman value. It shrinks a +1 SD shift in the other's set point to $0.79\pm0.05$. With $\rho=0$, $r<0.3$.

## What is new

- **Versus active inference.** No free energy; an amortized learned recurrence. Curiosity is a two-sided set point on the model's own loss. The language model is coupled through a selection operator, not as categorization inside the generative model.
- **Versus homeostatic RL (Yoshida and Man).** They read partners with a separate decoder over a fixed shared expression generator and add the partner's drive ($w=0.5$). Here reading comes from interoceptive masking in one tied multi-timescale dyad, only the agent's own drive is regulated, and learned mimicry with its reciprocity law is new.
- **Versus BabyX** (as the brief describes it). No hand-wired circuits; one loss trains every learned part, and each ablation is a parameter (untie $C$, $\rho=0$, $B_{\text{text}}=0$).
- **Versus data-driven avatars.** No human video trains the face. The face is $E_0$ of the agent's own inferred body.

## Biggest risk

$q_\phi$, trained on the agent's own renders, may not transfer to a real webcam face; then reading others falls back to borrowed coordinates and constraint 3 stays partial. Second, with a few hours a day $h$ may learn little beyond $b$, so "emergent structure" collapses into the body variables. Third, $\bar\varepsilon$ is gameable if any self-generated channel enters it; it must be computed on the user's channels only.
