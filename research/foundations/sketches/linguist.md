# Parity: affect as the private side of a public sign

*Lens: linguistics (grounding, prosody, conversation timing, emotion-word acquisition, iconicity).*

Emotion words never refer to private states directly. A child learns "tired" because someone names what is visible (face, voice, pace, situation), and the word sticks to the felt state because that sign was caused by it. The engine copies this. There is one public sign space $Y$: action units, prosody and turn timing. Every crossing between minds (engine and user, engine and Claude, both directions) goes through $Y$ or through how processing is modulated, never through symbols. One map $e$ writes the engine's state into $Y$. Inverted, the same map reads the user. Claude names the engine's state the way it names the user's: by looking at a face. Grounding is a commuting square, not a lookup table: a word means a state only through its public sign. The requirement that sender and receiver share one sign function is **parity**.

## Core object: the parity system

```
              Claude (frozen): words, names
         icon ▲ img(y^A)          │ u  (chosen delivery: pace, softness, voluntary AUs)
  index κ(z)  │                   ▼
   z^A ──e──▶ y^A ∈ Y ──────────────────▶ user
    ▲ ◀──r── (own feedback: facial/vocal)
    └───r─── y^U ∈ Y ◀────────────────── user (z^U hidden)
```

$$
\begin{aligned}
y^A_t &= e_0(b_t) + e_\theta(z_t) + u_t\\
\tau \odot \dot z_t &= -z_t + F_\theta\big(z_t,\, b_t,\, r_\theta(y^A_{t-w:t}),\, g_t \odot r_\theta(y^U_{t-w:t})\big) + \sigma\xi_t\\
\dot b_t &= \beta(b_t)\odot\big(c_t,\; -\epsilon_t,\; -\lVert y^A_t - y_{\mathrm{rest}}\rVert\big) - \delta\\
\theta^\star &= \arg\min_\theta\; \mathbb{E}\,\lVert s_{t+\Delta} - \hat s_\theta(z_t)\rVert^2 + \lambda\,\mathbb{E}\textstyle\sum_{h\le H}\lVert b_{t+h}-b^\star\rVert^2_\Lambda \quad \text{s.t. } r_\theta\!\circ e_\theta = P_L \text{ on self pairs}\\
\text{reply}_t &\sim \mathrm{Claude}\big(\text{text}_t,\ \mathrm{img}(y^A_t);\ \kappa_\theta(z_t)\big)
\end{aligned}
$$

Symbols. $z_t\in\mathbb{R}^d$ ($d\approx128$) is the unnamed latent. Its units differ only by time constant $\tau\in\mathbb{R}^d_+$, log-spaced from 33 ms to three weeks (a prosodic hierarchy: syllable, phrase, register, voice quality). $b_t\in[0,1]^3$ are the innate body variables (contact, predictability, activity budget) with set points $b^\star$ and precision $\Lambda$. $Y=[0,1]^{52}\times\mathbb{R}^6\times\mathbb{R}_+^2$ is the sign space: AU/blendshape intensities, prosody, and timing (gap, overlap). $y^A, y^U\in Y$ are the agent's and the user's signs. $e_0$ is an innate, iconic body-to-sign reflex map; $e_\theta$ its learned residual. $u_t\in Y$ is Claude's voluntary delivery. $r_\theta: Y^w\to\mathbb{R}^d$ is the reader, an inverse of $e$ trained only on own $(z, y^A)$ pairs. $P_L$ projects onto the legible subspace $Z_L=\mathrm{range}(r\circ e)$. $g_t\in[0,1]^d$ is a provenance gate. $c_t=\tfrac12\ln\det\Sigma_{U\mid U^-}-\tfrac12\ln\det\Sigma_{U\mid U^-,A^-}$ is contact supply: Gaussian transfer entropy from the agent's signs to the user's next signs. $\epsilon_t$ is the sign-stream prediction error. $s=(y^A,y^U,b)$. $\beta$ saturates at the bounds and $\delta$ is drift. $\kappa_\theta(z)\in K$ are Claude's processing parameters: retrieval kernel over state-tagged episodes, thinking budget, reply length, latency, and the user-cue gate. $\mathrm{img}$ renders the agent's face.

## Derivations

- **Homeostasis.** The $\lambda$ term; zero at $b^\star$, so a satisfied body exerts no gradient.
- **Curiosity.** Predictability has a set point below its maximum. When the sign stream is too predictable the $\lambda$ term favours actions that raise $\epsilon$; when too unpredictable, actions that lower it. Curiosity is derived, satiable, inverted-U.
- **Valence.** Read out as $v=w_v^\top z$, where $w_v$ is the least-squares direction predicting $-\Delta_H\lVert b-b^\star\rVert^2_\Lambda$. Never set, never an input.
- **Arousal.** Read out as $a=w_a^\top z$, where $w_a$ predicts upcoming sign energy $\lVert\dot y^A\rVert+\epsilon$. It is iconic: arousal is how much the public channel is about to move.
- **Mimicry.** Parity prior: at birth, $F$'s weights on $r(y^A)$ and $r(y^U)$ are tied. A perceived face drives $z$ as one's own face would, and $e$ writes it back; learning unties them only as far as prediction needs.
- **Reading others.** $\hat z^U=r_\theta(y^U)$ and $\hat b^U=$ the body readout of $\hat z^U$. This is Yoshida and Man's self-trained decoder (research/yoshida-man-homeostatic-coupling.md), generalized to the whole latent. Separate slots give mineness (research/williams-functional-valence.md).
- **Regulation by Claude.** Claude's only downward channel is $u$, the delivery it chooses: slower, softer, a voluntary smile. The engine senses $y^A$ through $r$ (facial and vocal feedback), so Claude regulates the body by how it speaks. No label or number crosses downward.
- **Replay.** The first term is an expectation over the agent's life. Nightly replay estimates it from stored $(y,b)$ streams, without language. Weighting episodes by $\lvert\Delta\lVert b-b^\star\rVert\rvert$ is a constraint borrowed from Barrett's body-gated learning (research/barrett-constructed-emotion.md), not derived.
- **Face and voice perception.** Perception is $r$: features in $Y$ become coordinates of the agent's own body. A fast coarse route is a second encoder from a 32×32 crop into $Y$, distilled from the agent's own renders. Partly derived, because $Y$'s face coordinates are MediaPipe's until S4.
- **Naming.** Claude sees $\mathrm{img}(y^A)$ and the cues that $\kappa$ passes on. It names both faces with one competence. Names are stored at the language layer as (word, $z$-region) episodes and come back through $\kappa$'s retrieval kernel. They never enter $F$.

## Constraints

1. Met. Words live only in Claude's episodic store, and only signs and modulations cross downward.
2. Met. Concepts are clusters in $Z_L$, and $v$ and $a$ are regressions.
3. Partly. Parity holds, but the coordinates are borrowed until S4.
4. Met. Upward the channels are icon and index only; downward only $u\in Y$.
5. Met, and stronger than required: see the Proposition.
6. Partly. The $\tau$ spectrum spans the range; that weeks-scale units learn temperament is unshown.
7. Partly. Self-data is unlimited; the user-specific residual still needs real hours.
8. Met. $F$, $e$, $r$ are small MLPs or an SSM; 30 Hz on CPU.

## Open problems

**(a) Interface.** An admissible interface types its channels. Engine to Claude may be *icon* (images of signs) or *index* (processing parameters caused by $z$ that carry no content). Claude to engine may only be a *sign* in $Y$. By the data-processing inequality, $I(z;\text{names})\le I\big(z;\ \mathrm{img}(e(z)),\kappa(z)\big)$. Claude can name no more of the state than the face and the modulations carry, which is the limit humans live with too. Legibility becomes a measurable design target, and P1's null (research/predictions.md) is expected: symbols are not how a namer comes to know a state.

**(b) Dyad.** $(z^A,z^U)$ are coupled only through $Y$, which is the formal common ground. Linearized, the joint system has a shared mode, and the agent's mimicry gain times the user's sets its stability margin and lag. S5 says the user's gain is non-zero. Reply latency set by $\kappa$ is itself a sign in $Y$ that the user reads, as a pause is read in conversation. Coupling is scored by windowed cross-correlation (research/wcc-windowed-cross-correlation.md).

**(c) Little data.** Parity converts unlimited self-data into the ability to read others. Self-data is $(z,y^A)$ at 30 Hz, including babbling while the user is away. The innate parts are $e_0$, the tied weights, $b^\star$ and $\tau$. From the user, only the residual between their sign map and the agent's has to be learned.

**(d) Grounding.** A concept is a sign: the signified is a region of $Z_L$, and the signifier is the words Claude used when the state was there. Its instances are a population of episodes. A user's correction ("tired, not sad") adds a word to that region and never moves $b^\star$, a deliberate departure from Nomura et al. (research/nomura-2026-social-reality-of-emotion.md).

## Proposition: the contact drive is blind to polarity

For any invertible affine maps $M_A$ and $M_U$ on the sign streams, $c_t$ is unchanged. These maps include mean shifts and sign flips, such as relabelling the user's smile response as a frown response. So contact cannot prefer a user who answers with smiles over one who answers with frowns at equal contingency, and no gradient pushes the agent's mean expression toward eliciting smiles.

*Proof idea.* Conditional covariances of $M_U y^U$ scale by $M_U(\cdot)M_U^\top$ in both determinants, so $\det M_U^2$ cancels. Conditioning on $M_A y^A$ generates the same σ-algebra as conditioning on $y^A$. Mean shifts do not enter covariances. Caveat: a user whose responsiveness depends nonlinearly on the agent's mean expression breaks the corollary, though not the invariance.

## Toy simulation (predictions fixed now)

Setup: linear-Gaussian, $d=8$, three body variables, 12 AUs. The simulated user has the agent's $e$ plus a perturbation of relative Frobenius norm 0.2, and the user's own smile responds linearly to the agent's smile. $r$ is fitted on 18,000 own frames (10 min at 30 Hz).
- Reading others: $R^2$ for the user's contact variable is at least 0.6. With a reader whose AU order is permuted (same training, parity broken), it is at most 0.2.
- Flattery: after $10^5$ steps of learning $e_\theta$ under the $\lambda$ term, the agent's mean smile AU moves by less than 0.05 (on a 0–1 scale) with contingency contact. It moves by more than 0.2 in the forbidden control, where contact is replenished by the user's smile intensity.

## What is new

- One sign function, three readers. The user reads the agent with $e$, the engine reads the user with $e^{-1}$, and the frozen LLM names the engine through $\mathrm{img}\circ e$, the same competence it uses on the user. Yoshida and Man have two readers. In Smith, Parr and Friston (research/smith-parr-friston-2019-simulating-emotions.md), concepts are latent states inside the model, whereas here no concept exists below Claude.
- Contact as directed contingency, provably blind to whether responses are pleasant. Homeostatic RL couples energy drives and has no answer to flattery at the level of the drive.
- Regulation by delivery. The LLM changes the body only by how it speaks, through feedback, which closes the loop from LLM to affect with no text or labels injected. Data-driven avatars have no state to close it on. BabyX, as the brief describes it, has no conceptual layer.
- A bound on what the LLM can name, which makes grounding measurable.

## Biggest risk

Legibility may be too small. A placeholder AU face shows few dimensions, so much of $z$ stays unnameable. Claude's reading of a stylized face may also pull in its own cartoon categories of basic emotion, letting an essentialist label scheme in through the icon channel. And the index channels (budget, latency, retrieval) may be as inert as P1's numbers. The first test is whether Claude's names for recurring regions of $Z_L$ are consistent across days at all. If they are not, the square does not commute and parity buys perception but not grounding.
