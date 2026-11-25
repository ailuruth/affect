# Sketch v2: Surprise re-noising in a rolling dyadic diffusion (energy-based / diffusion lens)

Lens: an energy-based and diffusion modeler. States are samples from a learned landscape, and behavior is what the sampler emits while it denoises.

## 1. Core mechanism

The agent does not hold a state vector. It holds one partly denoised sample of **the dyad's trajectory**: a rolling, multi-resolution window over its own expression, the other's expression, bodies and conversation. A prediction error does not nudge this sample. It **re-noises** it, and the size of the error sets how deep the noise goes. A deeper re-noising erases slower structure. Denoising then settles the sample again, possibly into a different basin. Emotion is the geometry of that re-settling.

**State.** $W_t=\{w^{\ell}_t\}_{\ell=0}^{L}$ is a temporal pyramid. Level $\ell$ is a trajectory sampled every $\tau_\ell=\tau_0 2^{\ell}$ ($\tau_0=33$ ms; $L\approx 14$, about 9 min per step at the top level). It spans a clamped past and an imagined future. Each token is $w=(s,\,u,\,b,\,\tilde b,\,c)$:
- $s$: the agent's own expression, as action units (AUs) and voice parameters.
- $u$: the other's face and voice in the agent's **own** motor coordinates, $u=\phi(o)$.
- $b$: the agent's body variables.
- $\tilde b$: the other's body variables. These are never observed, only inpainted.
- $c$: an embedding of the conversation, made by a small frozen local text encoder.

**Landscape.** $E_\theta(W;\sigma)=E^{\text{learn}}_\theta(W;\sigma)+E^{\text{innate}}(W)$.
- $E^{\text{learn}}$ is a small transformer over tokens indexed by time, level and channel, trained by denoising score matching.
- $E^{\text{innate}}=\sum_i \psi(b_i)+\sum_k R_k(W)$. Here $\psi$ is zero inside the set range and quadratic outside it, and the $R_k$ are fixed reflex wells (startle, orienting, separation call, CONSPEC face prior on $u$).
- Self–other swap symmetry: $E^{\text{learn}}(s,u,b,\tilde b,c)=E^{\text{learn}}(u,s,\tilde b,b,c)$.

**Update at each tick (30 Hz):**

$$
\underbrace{\Delta_t = E_\theta\big(W_t\!\mid\! u_t{=}\phi(o_t)\big)-E_\theta\big(W_t\big)}_{\text{surprise as an energy jump}}
\;\Rightarrow\;
\sigma_t = R(\Delta_t),\qquad
W \leftarrow W_t + \sigma_t\,\epsilon\;\;\text{on levels }\{\ell:\sigma^*_\ell<\sigma_t\},
$$
$$
\frac{dW}{d\sigma} \;=\; \sigma\,\nabla_W E_\theta(W;\sigma)\quad\text{integrated from }\sigma_t\text{ down to }\sigma_{\min},\ \text{with the past and } u_t \text{ clamped (inpainting)},
\qquad a_t = s\text{-channel of } W \text{ at } t{+}\delta .
$$

**Symbols.**
- $\phi$ is the agent's own inverse face and voice model. MediaPipe blendshapes stand in for it until S4.
- $R$ is a monotone map from surprise to noise level, and $\epsilon\sim\mathcal N(0,I)$.
- $\sigma^*_\ell$ is the **speciation noise level** of level $\ell$: the noise at which that level's gross structure is decided during backward diffusion. Biroli, Bonnaire, de Bortoli and Mézard (Nat. Commun. 2024) show it is computable from the spectrum of the data's correlation matrix. Coarser levels have larger $\sigma^*_\ell$.
- The flow is the probability-flow ODE, and $a_t$ is the emitted face and voice frame. Most ticks re-noise only levels 0–1, which takes one or two steps after consistency distillation.

**Time scales.**

| Time scale | Where it lives in the model |
|---|---|
| Reflex | The $R_k$ wells at level 0 |
| Expression | Levels 0–3 |
| Mood | Levels 8 and up, reopened only by a large $\Delta$ or by their own slow roll |
| Temperament | $\theta$, consolidated nightly |

The key identification is **time scale = noise scale**. How surprised the agent is decides how slow a part of itself it reopens.

## 2. Why it is new, and the closest prior work

| Closest prior work | What it does | The difference here |
|---|---|---|
| Rolling diffusion (Ruhe et al. 2024) and Diffusion Forcing (Chen et al. 2024) | Give tokens independent noise levels; later frames get more noise. | The noise level is fixed by position or schedule there. Here it is a **state variable set online by surprise**, and through $\sigma^*_\ell$ it selects which time scale is reopened. |
| SDEdit-style editing | Re-noises an input, then denoises it. | That method sets edit strength by hand. |
| Residual EBMs for text (Deng et al., ICLR 2020) | Put an energy on top of a frozen LM and sample by importance sampling. | There the energy is trained to score text quality. Here it is the agent's own embodied dyadic density, so the LM is reweighted by what the body–dyad landscape finds probable (§4). |
| Active inference and precision or volatility models | Expected-free-energy policy selection; surprise scales learning rates in a fixed unimodal hierarchy. | Here there is no expected-free-energy policy selection and no preference distribution beyond the flat-bottomed $\psi$. Surprise instead **erases and re-samples** structure in a multimodal landscape, so a mood shift is a discrete jump between basins, not a gain change. |
| Yoshida and Man | Infer the other's state by inverting the agent's own model. | Here the inversion is conditional sampling through a swap-symmetric score. |

## 3. Constraints

- **Meets: no labels.** Inputs are continuous AUs, prosody and text embeddings. Training is score matching with no targets.
- **Meets: emotion as emergent structure.** Emotions are the basins of $E^{\text{learn}}$ at coarse levels. They are modes of joint self–other–body–conversation trajectories ("what is about to happen between us"), not points or variables.
- **Meets: others read through the agent's own body.** The other enters only through $\phi$, into the agent's motor coordinates. Swap symmetry means the same score that generates the agent's own face also infers $\tilde b$ from $u$.
- **Meets: frozen LLM coupled without words.** See §4. No number or label reaches Claude.
- **Meets: satiable drives.** $\psi$ is flat inside the range, so $\nabla\psi=0$ when sated. Body variables are one channel, not the core.
- **Meets: reflex to temperament.** The pyramid levels and $\theta$, as in the table in §1.
- **Partly meets: real-time face.** It is real time only if re-noising stays shallow on most ticks and the fine levels are distilled to one or two steps. A deep re-noise costs a burst of computation, which plausibly shows up as a "freeze".
- **Breaks or leaves open: scarce real data.** Diffusion models are data-hungry. The proposed split is principled but unproven:
  - Pretrain only levels $\ell\le2$ (sub-second motor coarticulation, below every affective $\sigma^*_\ell$) on Seamless Interaction, as a motor-babbling prior.
  - Learn the coarse levels only from living. Swap symmetry doubles every episode.

  If the coarse levels never develop more than one basin, the claim fails (§6).
- **Open: need-conditioned attention.** It is present in the architecture: $b$ tokens act as queries over $u$, $c$ and memory tokens inside the score network, so needs select cues. It is not yet derived from the objective.
- **Open: structure over people.** A relationship is a low-rank tilt of $E^{\text{learn}}$, one per person. It is not yet derived either.

## 4. Principle 10 components, the coupling to Claude, and perception

Each Principle 10 component in one line:
- **Homeostasis:** the flat-bottomed $\psi$ in $E^{\text{innate}}$. Imagined futures that bring $b$ into range have lower energy, so emitted actions drift toward them, and the pull stops once the variable is sated.
- **Curiosity:** only partly derived. Novel input keeps re-noising until replay learns it, so novelty holds the state open and makes behavior variable. Directed information seeking is not derived.
- **Arousal:** a readout of re-noise depth, $\sigma_t$, and how fast it decays.
- **Valence:** a readout of $-(E_{\text{after}}-E_{\text{before}})$ across one re-settling, whether the state lands in a deeper or a shallower basin. This is close to Joffily and Coricelli's $-dF/dt$, but measured across a discrete re-settling.
- **Mimicry:** $\phi$ is learned by reproducing faces with the agent's own face, so the earliest learned basin is the diagonal $s\approx u$. With $u$ clamped at level 0, denoising pulls $s$ along it. Mimicry is predicted to weaken as living adds other structure.
- **Reading others:** $\tilde b$ and the other's coarse levels are inpainted by the same swap-symmetric score. The other is modeled as a re-noised copy of the agent.
- **Regulation:** Claude's reappraisal is embedded and clamped into $c$ at coarse levels. That conditioning change is itself an energy jump, so it re-noises and re-settles the window. Reappraisal is an inpainting edit to the slow part of the state.
- **Replay:** score matching on stored feature windows. Each episode is trained up to the noise depth $\sigma$ it actually reached, so an episode's state tag is its re-noise profile. Episodes that reopened mood train mood.

**Coupling to Claude (interface theory).** Claude is one expert in a product of experts and never sees the state:
1. **Choosing among drafts.** Claude writes $K$ drafts. Each is embedded and clamped into $c$, and draft $k$ is chosen with probability proportional to $\exp(-[E_\theta(W\mid c{=}e_k)-E_\theta(W)]/T)$: say what the body is already about to do. $K$ grows with the entropy of the $c$-channel, so a multimodal landscape gets more drafts.
2. **Memory.** Memories are retrieved with weights $\exp(-E_\theta(W\oplus m))$. Mood congruence follows because the coarse levels decide compatibility.
3. **Turn timing.** The agent starts speaking when its own denoised future says it speaks now. If Claude's text is not ready, the face and voice emit the turn-holding behavior that the window predicts, so the fast loop never waits.
4. **Its own face.** The rendered face can be shown to Claude as an image.

**Perception.**
- **Face:** $o_t$ is blendshapes, later the S4 inverse model, plus a 32×32 fast-route crop through a small encoder. It enters as $u$ at level 0, in the agent's own AU coordinates.
- **Dynamic route:** enters as conditioning tokens.
- **Voice:** prosody enters in the same parameter space the agent uses for its own voice output, so heard voice is in the agent's own vocal-motor coordinates.
- **Context:** $c$ is always present, so a face is never read without context.

## 5. First distinctive prediction and a published test

**Prediction (surprise depth selects the time scale reopened, with a threshold).**
- After partner events of graded surprise, a listener's band-limited expressive dynamics change only down to a frequency band that depends on surprise.
- The slow (tens-of-seconds) band shifts in a **step** at a surprise level set by that band's speciation threshold. It does not shift linearly.
- Right after the event, short-lag coupling gain to the partner rises transiently, because the clamp dominates the reopened prior.

A bank of linear leaky integrators or an SSM predicts a linear dose–response with no step. Fixed-gain mimicry or Kuramoto coupling predicts no dependence on surprise.

**Test on published data.**
- **Data:** the Seamless Interaction dataset (Meta, arXiv 2506.22554), naturalistic split: 30 fps video and audio of in-person dyads.
- **Features:** extract AUs with a published coder (OpenFace or Py-Feat, used to measure people) and prosody.
- **Surprise:** score it per window with a predictive model of the partner trained on other dyads.
- **Analysis:** windowed cross-lagged correlation (Boker et al. 2002, as listed in the brief) and band-limited baseline shift, per surprise quantile. Match on partner motion energy.
- **Model comparison:** compare a step model against a linear model. Pre-register the step location, estimated from the covariance spectrum of slow-band trajectories in the training split.

## 6. Most likely failure mode

**Coarse unimodality.** With one person's few hours a day, the coarse levels' covariance spectrum may show no gap. There would then be no speciation and only one mood basin, and surprise re-noising would collapse into an adaptive-gain filter: an HGF-like model with extra steps, emitting a face that is only a smoothed mirror. This can be checked early, before any engine work, by computing $\sigma^*_\ell$ from the spectrum on the published dyadic data and on the operator's first weeks.

A secondary risk: choosing among drafts by energy is mode-seeking, so it may favor bland, typical replies.
