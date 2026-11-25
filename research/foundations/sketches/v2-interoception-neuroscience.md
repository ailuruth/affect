# Sketch v2: Somatic Completion Memory (lens: interoception, embodied simulation, face perception, mimicry)

**Idea in one line.** The agent's state is its own lived body: a running body vector plus an associative memory of short trajectories that this body actually went through. At every frame, need, the other person's face mapped into the agent's own muscles, and context form a query. The query reactivates past bodily episodes, and the present body moves along their continuation. What a neuroscientist would call feeling is, functionally, which of its own past bodies the agent is currently completing. Face, voice, the language model's recollections and its choice among replies are all read from the same attention weights.

## 1. Core mechanism

State $S_t = (x_t, \mathcal{M}_t, u_t)$.

- $x_t \in \mathbb{R}^{d_x}$, with $d_x \approx 50$, is the body now, in the agent's own coordinates. It has four parts: $m_t$ (facial muscle or AU activations), $v_t$ (vocal and prosody parameters), $r_t$ (phase and amplitude of the innate rhythms: breath, blink, pulse) and $b_t$ (body variables with set point $b^*$).
- $\mathcal{M}_t = \{(k_i, \tau_i, w_i, e_i)\}_{i=1}^{N}$ holds the lived somatic traces. Each $\tau_i \in \mathbb{R}^{L\times d_x}$ is a window of the agent's own past body, with $L \approx 60$ frames (2 s). $k_i$ is the trace's key, written at its onset. $w_i \ge 0$ is its strength. $e_i$ points to the stored episode: feature streams and a transcript snippet, never raw video.
- $u_t \in \mathbb{R}^N$ is slow occupancy, a low-pass filter of retrieval: $u_{t+1} = (1-\tfrac{1}{T_u})u_t + \tfrac{1}{T_u}\alpha_t$.
- $\hat s_t = E_\psi(o^{\text{face}}_t, o^{\text{voice}}_t) \in \mathbb{R}^{\dim m + \dim v}$ is the other's face and voice expressed in the agent's own muscle and vocal coordinates. It is a fixed map from blendshapes until S4. After S4, $\psi$ is trained by self-reproduction, so that $E_\psi(\text{render}(x)) \approx x$.
- $c_t$ is the context: an embedding of the conversation event, the partner's identity embedding (learned from face and voice) and the time of day.

**Query and attention (need-conditioned):**
$$q_t = Q_\theta\big(x_t,\ \hat s_t,\ c_t,\ b_t - b^*\big), \qquad \alpha_{t,i} = \operatorname{softmax}_i\big(\beta\, q_t^\top k_i + \log w_i + \gamma\, u_{t,i} - \rho_{t,i}\big)$$

Here $\rho_{t,i}$ is a refractory term (habituation) that grows while trace $i$ is being consumed.

**The one dynamical equation (somatic completion):**
$$x_{t+1} = x_t + \Delta t\Big[\underbrace{R(x_t, o_t)}_{\text{innate reflexes}} + \kappa \sum_i \alpha_{t,i}\big(\underbrace{\tau_i[\phi_i{+}1]-\tau_i[\phi_i]}_{\text{continuation velocity}} + \lambda\,(\tau_i[\phi_i]-x_t)\big)\Big] + \sigma\xi_t$$

$\phi_i$ is trace $i$'s phase. It advances one frame while $\alpha_i > \epsilon$ and resets otherwise. $R$ is fixed: startle, orienting, blink, breath, separation call, contact seeking. The face is $m_t$ plus the voluntary command from Claude. The voice is $v_t$.

**Single objective.** The parameters $\theta = (Q, K, \beta, \kappa, \lambda, \gamma)$ maximize the agent's prediction of its own embodied future under the trace mixture:
$$J(\theta) = \sum_t \log \sum_i \alpha_{t,i}\, \mathcal{N}\big(x_{t+1:t+H};\ \tau_i[\phi_i{+}1{:}\phi_i{+}H] + (x_t-\tau_i[\phi_i]),\ \Sigma\big).$$

**Write and merge rules.** These are constraints on the core, not derived from it. A trace is written when surprise $-\log p > \eta$. Its strength is $w = |\Delta\lVert b-b^*\rVert|$ over the window plus surprise. The strength is symmetric in gain and loss, so nothing rewards the user's smiles. Strength decays slowly.

## 2. Why this is new, and the closest prior work

- **Modern Hopfield networks and attention** (Ramsauer et al., arXiv 2008.02217, which I read): one retrieval step equals attention, and the fixed points are a global average, metastable subset averages or single patterns. Difference: they retrieve static patterns. Here the retrieved objects are trajectories whose *velocities* drive a continuous body. The keys are written by the agent's own surprise and need change. The query mixes need with the other's face in self coordinates.
- **Motion matching** (Learned Motion Matching, Holden et al., SIGGRAPH 2020; I read the author's page): the controller picks the next clip from a mocap database by matching features. Difference: that database is actors' motion, curated offline and selected by a game controller. Here the database is the agent's own interoceptive and expressive life, written online. Blending is soft and need-keyed. The same weights $\alpha$ also drive language-model recall and reply selection.
- **Neural episodic control** (Pritzel et al., arXiv 1703.01988, abstract read): memory stores *value estimates* for action choice. SCM stores no value anywhere. Action is completion of the agent's own past body.
- **Active inference** (brief's Candidate A): a parametric generative model, posterior inference over hidden states, and preferences as priors in expected free energy. SCM has none of these. The generative model is nonparametric and made of the agent's own episodes. Drives act only by *selecting which past bodies come back*, not through a preference prior. Mimicry is retrieval and completion, not the fulfilment of proprioceptive predictions about the other.

The new mechanism is that mimicry, mood, recall and empathy are all **reactivation of the agent's own lived body trajectories, keyed by need and by the other's body.** None of the sources has that.

## 3. Constraints (from brief.md)

| Constraint | Status |
|---|---|
| No labels below the language model | Met. Inputs are AU, blendshape and prosody streams. Traces are body windows. |
| Emotion as emergent structure | Met. Emotion appears as recurring clusters of mutually retrieving traces and as metastable states of $\alpha$. Nothing is named. |
| Others read through the agent's own body | Met, strongly. $\hat s$ is in own coordinates, and the other is interpreted by the agent's *own* past continuations. |
| Frozen language model coupled without words | Met, see section 4. |
| Satiable drives | Met. The need slice of $q$ vanishes at $b = b^*$, so need stops biasing retrieval. Trace strength is need *change*, not gain. |
| Time scales from reflex to temperament | Met. $R$ acts within frames, traces last seconds, $u$ moves over minutes to hours, merging runs nightly, and the distribution of $w$ and prototypes sets temperament over weeks. |
| Scarce real data | Mostly met. Memory learns from single exposures, and only small maps are trained. Cold start is weak, see section 6. |
| Real-time face | Met. Attention over $10^4$–$10^5$ keys of 64 dimensions at 30 Hz is cheap on Apple silicon. |

What it breaks or leaves open:
- The write and merge rules are constraints, not consequences of $J$. This is the main tension with Principle 10.
- Directed curiosity is not derived.
- The text-to-prosody planner used in section 4 is a borrowed human-trained mapping.
- Semantic content reaches the body only through the embedding $c_t$.

## 4. Principle 10 components, and perception

- **Homeostasis.** $b$ is part of $x$, and the term $b - b^*$ in the query reactivates episodes during which need changed. Satiation follows because that term is zero at the set point.
- **Curiosity.** Novelty means that no trace matches, so the log-sum-exp energy is low. The innate orienting reflex in $R$ fires and writing increases. Seeking novelty on purpose is **not** derived.
- **Valence and arousal** are readouts. Valence is $v_t = -\sum_i \alpha_i\,(\lVert b(\tau_i[\phi_i{+}H])-b^*\rVert - \lVert b(\tau_i[\phi_i])-b^*\rVert)$, the expected need change along the bodies being completed. Arousal is $\sum_i\alpha_i\lVert\dot\tau_i\rVert$.
- **Mimicry.** $\hat s$ retrieves the agent's own traces whose onset looked like the partner, and the body completes them. Mimicry is therefore idiosyncratic and can anticipate the partner. With an empty memory, only the small reflex gain in $R$ remains.
- **Reading others.** $\alpha^{\text{other}}$ uses the same keys with query $Q(\hat s, \hat s, c, 0)$. The inferred state of the other is $\sum\alpha^{\text{other}}_i\tau_i$: what the agent's own body did next when it was in that state. Empathic overlap is $\langle\alpha,\alpha^{\text{other}}\rangle$.
- **Regulation.** Reappraisal is Claude's words changing $c_t$, which re-keys retrieval, so the face, the valence readout and recall all change. Suppression is a voluntary motor override, so the face changes but $\alpha$ and recall do not. That dissociation is an ablation prediction.
- **Replay.** Each night, every trace is used as a query. Traces that retrieve each other are merged into strength-weighted prototypes, and $Q$ and $K$ are retrained on $J$ over the stored feature streams. The prototypes are the emerging emotion concepts. Claude may name them by watching rendered replays, as an optional step.
- **Coupling to Claude, with no state in words or numbers:**
  - **Recall.** Transcript snippets from the episodes with the highest $\alpha$ enter the prompt as what comes to mind, so recall is mood-congruent by construction.
  - **Timing.** The reply delay and the thinking budget equal the settling time of the iterated retrieval when the user's utterance arrives. Metastable mixtures settle slowly, which looks like hesitation.
  - **Articulatory try-on.** Claude writes 3 or 4 candidate opening sentences. Each is mapped into a somatic trajectory $y^{(j)}$ by a frozen prosody and viseme planner, and the agent speaks the candidate with the highest memory energy $\operatorname{lse}_i(\beta Q(y^{(j)})^\top k_i + \log w_i)$: the sentence its body can say right now. The chosen text then conditions Claude's later thinking.
  - **Self-view.** Claude sees a rendered image of its own face.
- **Perceiving the other's face and voice.** The two are perceived jointly by one inverse model into the agent's own muscle and vocal coordinates. Meaning comes from the agent's own memory, not from a separate perception pipeline. The fast coarse and dynamic routes in brief.md would feed $c_t$ and $\hat s$. The body route *is* $E_\psi$.

## 5. First distinctive prediction, and a published test

**Prediction: completion, not copying.** A listener's facial response after the partner's expression onset is better predicted by **the listener's own earlier responses**, retrieved by matching the partner's onset, than by (a) a lagged copy of the partner's trajectory or (b) other people's responses retrieved with the same key. The advantage is larger when the past responses were to the *same partner* (relationship specificity), and grows with the number of sessions.

**Data.** The Seamless Interaction dataset (arXiv 2506.22554, read).
- Per-frame values for 46 FACS action units plus head pose and gaze, from Meta's tool. This tool measures the humans, which brief.md allows.
- Participant IDs, with Naturalistic participants in up to 10 sessions.
- 1,752 sessions between familiar pairs and 1,611 between strangers.

**Analysis.**
1. Take participants with at least 3 sessions.
2. Define events as onsets in the partner's AU stream.
3. Set the target to the listener's 46-AU trajectory over the next 2 s.
4. Fit the models with leave-one-session-out. Compare held-out error and Boker-style windowed cross-lagged correlation against surrogates built from shuffled events.

**Falsified if** own-history retrieval does not beat both population retrieval and the lagged copy. The paper notes that some participant IDs are wrong, so check robustness by restricting to sessions with consistent IDs.

## 6. Most likely failure mode

The trade-off in $\beta$ on scarce data. With one person's few hours, the keys are crowded. At low $\beta$, retrieval falls into Ramsauer's global-average fixed point and the face is a bland mean. At high $\beta$, a few strong traces capture the dynamics and the face becomes a perseverative attractor: stereotyped, rumination-like faces. The refractory term $\rho$ and the slow occupancy $u$ may not open a usable window between the two. In that case SCM reduces either to the reflexes or to a jukebox.
