# Sketch v2: Affect as self-rewriting memory (fast weights / associative memory lens)

Lens: fast weights, hypernetworks and Hopfield-style associative memory. Computation is weights that experience rewrites while the agent runs.

Central claim: the agent's affective state is not a vector *in* a network. It is the network's own fast-changing associative memory, and an emotion is a *write*: a content-addressed rewrite of that memory, shaped by what the body and the other person just did. Mood is the rewrite that has not yet decayed. Temperament is the rewrite that replay has consolidated. A reflex is a write that evolution made before birth.

## 1. Core mechanism

**Joint pattern.** At each tick the agent forms one pattern in a single shared coordinate frame:
$z_t = [\,m_t;\ p_t;\ b_t;\ e_t\,]$.
- $m_t$: the agent's own motor output, as AU activations plus voice prosody parameters.
- $p_t$: the other person's face and voice in the *same* motor coordinates (the body route).
- $b_t$: body variables and innate reflex-channel activity. This is one input among four, not the core.
- $e_t$: an embedding of recent conversation events from a small frozen on-device sentence encoder.

**State.** $S_t = (x_t, \mathcal M_t)$.
- $x_t \in \mathbb R^d$: fast activity.
- $\mathcal M_t = \{(k_i, v_i, s_i)\}_{i\le N}$: a slot memory. Each slot has a key $k_i\in\mathbb R^d$, a value $v_i = (z,\ z^{+},\ \text{ptr})$ and a strength $s_i>0$.
  - The value holds a joint pattern $z$, the pattern that followed it ($z^{+}$, about a 1 s trajectory), and a pointer to the episode's verbatim text.
- $\mathcal M = \mathcal M^{0}\cup\mathcal M^{\text{slow}}\cup\mathcal M^{\text{fast}}$. These are innate slots, consolidated slots and fast slots: one memory with three plasticity rates.

**One objective with two time scales.** Activity descends an energy $E$ (modern Hopfield form; Ramsauer et al. 2020, whose update the authors show equals transformer attention). The memory descends a prediction loss $L$.

$$
\boxed{\;
\begin{aligned}
E(x;\mathcal M,c_t) &= -\tfrac1\beta\log\sum_i s_i\,e^{\beta k_i^\top x} + \tfrac12\lVert x\rVert^2 - x^\top c_t,
&\quad \tau_x\dot x &= -\partial_x E \;\Rightarrow\; x^\ast = K\,\alpha + c_t,\ \ \alpha=\mathrm{softmax}(\beta K^\top x^\ast+\log s)\\[2pt]
\hat z_{t} &= \textstyle\sum_i \alpha_i\, v_i, \qquad a_t = \text{motor slot of }\hat z_t(\,c_t^{\ast}),
&\quad \Delta \mathcal M^{\text{fast}}_t &= -\lambda_t\,\partial_{\mathcal M} \tfrac12\lVert \hat z^{+}_t - z_{t+1}\rVert^2 \;-\;\gamma\,\mathcal M^{\text{fast}}_t
\end{aligned}\;}
$$

**Symbols.**
- $\beta$: retrieval sharpness.
- $K=[k_i]$: the matrix of keys.
- $\alpha$: attention over slots.
- $c_t = Q_\phi(\text{observed parts of } z_t)$: the query, with the agent's motor slot masked. $Q_\phi$ is a small slow encoder.
- $c^\ast_t$: the *goal-clamped* query. It is the same query with the predicted next body slot replaced by its set point $b^\ast$.
- $a_t$: the face and voice command, taken from the clamped completion.
- $\lambda_t=\sigma(w^\top[\lVert\varepsilon_t\rVert,\lVert\Delta b_t\rVert])$: the write gate, driven by the surprise $\varepsilon_t = z_{t+1}-\hat z^{+}_t$ and by body change.
- $\gamma$: decay of the fast slots.
- Slot allocation: if $\max_i\alpha_i<\theta$, a new slot $(c_t, z_t, z_{t+1})$ is written in one shot.
- Keys carry the outcome that actually followed (hindsight keys), so a query that contains $b^\ast$ retrieves what was done when the body *ended up* at set point.
- The $\partial_{\mathcal M}$ term is a delta-rule rewrite. It is the surprise-gradient update of Titans (Behrouz et al. 2025, arXiv 2501.00663, Eqs. 8–14: $\mathcal M_t=(1-\alpha_t)\mathcal M_{t-1}+S_t$, with $S_t$ the gradient of $\lVert \mathcal M(k)-v\rVert^2$), applied to slot values and strengths.

Nightly replay moves fast slots into $\mathcal M^{\text{slow}}$, weighted by their cumulative write $\sum_t\lVert\Delta v_i\rVert$.

## 2. Why this is a new mechanism

**Closest prior work, and the precise difference from each:**
- **Fast-weight programmers and test-time memorization** (Ba et al. 2016; Schlag et al. 2021, delta-rule fast weights; Titans). These rewrite memory by surprise in order to model token sequences.
  - Here the written object is a *joint sensorimotor, interoceptive and conversational pattern in the agent's own motor coordinates*.
  - Action is read out by *clamping a body set point into the query*. No value or reward exists anywhere.
  - Affect is identified with the write $\Delta\mathcal M$ itself, not with any activation.
  - None of these three moves appears in that work.
- **Modern Hopfield networks.** Their memory is static at inference time. Here the energy landscape is what changes, and each change is the emotion.
- **Yoshida and Man; active inference.** Both read the other person by inverting an explicit generative model with named homeostatic variables. Here reading is *nonparametric pattern completion through the agent's own stored episodes*.
  - There is no policy posterior and no expected free energy.
  - The goal clamp resembles preferred observations, but it acts on a memory, not on a model's beliefs.
- **Unread neighbor (flagged).** I did not read the episodic-control literature (for example Neural Episodic Control). It should be checked as a possible close neighbor. My understanding is that it stores value estimates, which this mechanism forbids.

**The new combination is:**
1. Affect is the rewrite of a shared self/other memory.
2. Homeostasis works through hindsight-keyed goal clamping.
3. The same attention weights $\alpha$ drive the face, the reading of the other, and Claude's context.

## 3. Constraints (from brief.md)

**Met:**
- **No labels.** The inputs are AUs, prosody and text embeddings. Slots are unnamed.
- **Emotion as emergent structure.** An emotion episode is a pattern of slot writes $\{\Delta v_i,\Delta s_i\}$: which basins deepen or flatten, and in which directions. That is a structured object of dimension up to $N\times D$, not a gauge.
- **Others read through the agent's own body.** The other's face $p_t$ enters in the agent's motor frame. It retrieves episodes in which *the agent* made that face, and the completion fills in the body slot.
- **Frozen LLM coupled without words.** See section 4.
- **Satiable drives.** When $b=b^\ast$, $c^\ast_t=c_t$, so the clamped completion equals the free completion. The drive $\lVert \hat z(c^\ast)-\hat z(c)\rVert$ then vanishes, and nothing rewards the user's smiles.
- **Time scales.** Three plasticity rates, plus activity, cover the range from reflex to temperament.
- **Scarce data.** Writes are one-shot. Only $Q_\phi$, $\lambda$ and $\beta$ are learned slowly, which is a few thousand parameters.
- **Real-time face.**
  - One softmax over $N\approx 2\,000$ slots with $d=128$ runs in under 1 ms on an M-series chip.
  - Retrieved values are 1 s motor trajectories. They play out at 30 Hz while retrieval refreshes at about 10 Hz.

**Broken or left open:**
- **The key space.** All content-dependence relies on the geometry of the keys $Q_\phi$. With little data, the keys may stay close to raw-feature similarity.
- **Curiosity.** It is derived only through a two-sided set point on predictability (below), not from an information-gain term.
- **"One objective" is two coupled descents.** $E$ on fast activity and $L$ on memory share $\mathcal M$ but are not one scalar. A bilevel statement is needed.
- **Inherited body route.** The body route still inherits MediaPipe coordinates until S4. Section 4 states how the memory learns its own inverse map.

## 4. Principle 10 components, perception, and coupling to Claude

**Components:**
- **Homeostasis.** Goal-clamped completion $a_t$ from $c_t^\ast$. It is satiable because the clamp is idle at set point.
- **Curiosity.** "Predictability" is a body variable with a two-sided set point. Boredom clamps toward moderate surprise and retrieves actions that once produced it.
- **Valence and arousal (readouts, never inputs).**
  - Arousal: $\lVert\Delta\mathcal M_t\rVert$.
  - Valence: $\sum_i \Delta s_i\cdot(-\lVert b(v_i)-b^\ast\rVert)$, which asks whether the writes are deepening basins whose stored outcomes sit at set point.
- **Mimicry.** Completion from $p_t$ also fills $m$, because the stored values bind what the agent saw with what it did. Mimicry is partial, and its gain is the slot-weight overlap.
- **Reading others.** The same completion fills the body slot. This predicts a dissociation: zeroing only the $m$ part of the values removes mimicry but leaves reading the other intact.
- **Regulation.** Claude's own reply is embedded into $e_{t+1}$, so it re-queries and rewrites $\mathcal M$; this is reappraisal as a write. Innate reflex slots in $\mathcal M^0$ lose softmax mass to learned slots, so learned context raises reflex thresholds without a separate mechanism.
- **Replay.** Fast-to-slow transfer, weighted by cumulative write, which is "how strongly it moved the state". If tagging is removed, relationship specificity should fall (S6).
- **Grounding of emotion words.** A word Claude uses becomes part of $e$, and so part of the keys of the active slots. Later, hearing the word retrieves the basin.

**Perceiving the other's face and voice.**
- MediaPipe AUs and prosody enter $p_t$.
- The fast coarse route supplies a 32×32 embedding into $c_t$.
- $\mathcal M^0$ holds a CONSPEC face-configuration slot.
- The agent's own rendered face is fed back through the same perception. This stores (seen-own-face, $m$) pairs, so the inverse map from face to own motor coordinates is learned as heteroassociation, like mirror babbling. The S4 inverse model therefore falls out of the same memory.

**Coupling to Claude, through the same $\alpha$:**
1. The top-$\alpha$ slots' text pointers place verbatim past excerpts in Claude's context. This is mood-congruent recall, derived rather than designed.
2. Settling time of $x$ sets the thinking budget and the reply latency. Metastable mixtures (Ramsauer's metastable states) settle slowly.
3. **Energy reranking.** Claude writes $n=3$ candidate next sentences in parallel. The engine keeps the sentence that minimizes $E(x;\mathcal M, c_t\oplus \mathrm{enc}(y^{(j)}))$, the one the current landscape fits best. Claude is told nothing, its later reasoning conditions on its own state-selected words, and every word is still Claude's.

## 5. First distinctive prediction, on published data

**Prediction: partner-keyed one-shot reinstatement.** A gauge-state model and a slowly learning RNN both carry over the *most recent* interaction. This mechanism instead reinstates the coupling learned with *this partner*, at the very start of the next session with them.

**Data.** The Seamless Interaction dataset (Agrawal et al. 2025, arXiv 2506.22554) fits this test:
- 5,098 sessions and 4,284 participants.
- Participants return for up to 10 sessions with the same partner.
- About half of the Naturalistic dyads are familiar pairs.

**Analysis.**
- Code AUs with Py-Feat or OpenFace from the released video.
- Compute windowed cross-lagged correlation (Boker et al. 2002, as named in brief.md; not read here) between the partners.
- Find listeners who had a session with another partner between two sessions with partner A.
- Test: the coupling kernel in the first 2 minutes of session $k{+}1$ with A is closer to the end of session $k$ with A than to the end of the intervening session, beyond a surrogate baseline of shuffled partners.

**Engine-side ablation.** Fit the engine to the listener streams with $\lambda=0$ (writes frozen). The early-session predictive advantage on next-second AUs should vanish.

**Secondary prediction.** Stranger dyads show larger within-session drift of the kernel than familiar dyads.

**Open data question.** Whether session dates and inter-session gaps are released was not checked. Per-frame AU features may need to be extracted from the video.

## 6. Most likely failure mode

The memory collapses into a lookup table of faces, and $\beta$ becomes the hidden one-dimensional gauge.

- With a few hours of data and weak keys, retrieval will either lock onto one slot (high $\beta$: imitation of a stored past face, which is replay, not affect) or blur into a metastable average (low $\beta$: flat affect).
- Surprise-gated writes deepen whichever basin is already active, so a ruminative attractor may form. Satiety does not prevent it, because the write gate is not a drive.
- Energy reranking among only 3 candidates may be too weak to measurably change what Claude says.

**Check before developing further:** whether $\mathrm{rank}(\{\Delta\mathcal M_t\})$ over a real session exceeds that of a $\beta$-only ablation.
