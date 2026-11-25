# Sketch v2: Efference-keyed attention (lens: sequence-model architect)

The proposal is a new primitive, not a new loss. In standard attention, keys are learned projections of whatever the token happens to be. Here every token is keyed by **the motor program the agent itself would issue to produce it**: a face it sees, a voice it hears, a memory, a body need, even a sentence Claude proposes. The agent's body supplies the attention metric. Emotion is not a vector inside this machine. It is a recurring **routing regime**: which slots bind to which tokens, at which time constants.

## 1. Core mechanism

The state is a set of $N$ slots $S_t=\{s_i\}_{i=1}^N$, $s_i\in\mathbb{R}^d$, each with its own time constant $\tau_i$, log-spaced from ~50 ms to weeks. A token pool $X_t$ holds whatever is present: the other's face and voice windows, the agent's own proprioceptive and expressive windows, retrieved episodes, conversation events, body-variable tokens, and candidate utterances.

$$
\tau_i\,\dot s_i=-s_i+\sum_{j\in X_t}\alpha_{ij}\,v_j+\sum_{l\in S}\beta_{il}\,U s_l,
\qquad
\alpha_{ij}=\operatorname{softmax}_j\!\Big(\tfrac{\langle W_q s_i,\;\mu(x_j)\rangle}{\sqrt{d}}+m_j\Big)
$$

The symbols:

- $\mu$ is the **efference key**, the agent's own inverse model. It maps any token's features to the own-motor trajectory (AU or muscle activations plus vocal-source parameters over a ~1 s window) that would reproduce them. For own expression, $\mu$ is the efference copy. For the other's face and voice, it is the inverse model (MediaPipe blendshapes stand in until S4). For text, it is the prosody and face trajectory the agent would produce while saying the text, taken from its own speech model. For an episode, it is the stored motor trajectory.
- $v_j=[\mu(x_j);\,F(\mu(x_j),S_t)]$ is the value: the motor program plus the forward model's predicted consequence of that program.
- $m_j$ is the token's log-mass. It is $0$ for ordinary tokens. A body token has $m_j=\log\,\mathrm{relu}(\lvert b_k-b_k^*\rvert-\epsilon_k)$, so its mass goes to $-\infty$ at the set point and the token leaves the pool.
- $\beta_{il}$ is slot-to-slot attention with the same form, which lets slow slots bias the queries of fast slots. $W_q$ and $U$ are learned.
- Some query rows are **innate heads**: fixed and never trained. Examples are CONSPEC (a face-configuration query on the coarse route), startle (a query on onset and residual), separation (a query on the "absent partner" sink token), contact, and play.

Action reads out over the agent's own motor repertoire $\mathcal{C}$:

$$a_t=\sum_{c\in\mathcal{C}}\operatorname{softmax}_c\big(\langle W_a\bar s_t,\mu(c)\rangle\big)\,c$$

One objective trains everything: predict the dyad in one's own motor coordinates.

$$\mathcal{L}=\sum_t\big\|\,\mathrm{sg}[\mu(X_{t+\Delta})]-P(S_t)\big\|^2+\lambda\sum_{\text{own}}\|M(\mu(x))-x\|^2$$

The first term is JEPA-style latent prediction of the joint self, other and body stream. The second is cycle consistency, learned by the agent reproducing faces with its own face.

## 2. Why it is new, and the closest prior work

These descriptions are from memory and were not re-read for this sketch, so check each one in the original.

- **Slot Attention** (Locatello et al. 2020) and **Perceiver** (Jaegle et al. 2021) are latent slots that cross-attend to inputs. Their keys are learned, input-specific projections. In EKA the key space is fixed by embodiment and is shared by self, other, memory and language.
- **RIMs** (Goyal et al. 2019) are modules with attention-gated updates. They have no shared motor metric, no time-constant spectrum, and no mass-gated drive tokens.
- **MOSAIC / HMOSAIC** (Wolpert, Doya and Kawato 2003) is the nearest relative. Paired forward and inverse models compete through a softmax responsibility over prediction errors, and the same machinery is reused to understand others. The differences:
  - MOSAIC selects among a few modules. EKA lets multi-time-scale slots query an open token pool by content.
  - EKA also keys episodes, needs and Claude's candidate sentences into the same motor space.
- **Somatic markers** (Damasio) appear here as an operation, not a metaphor: candidate utterances are scored by the bodily trajectory they would produce.

**The new mechanism is attention whose metric is the agent's own body.** Neither sequence models nor mirror-system models have it.

## 3. Constraints met, broken and open

| Constraint | Status |
|---|---|
| No labels | **Met.** Inputs are motor-space features. No emotion variable exists anywhere. |
| Emotion as emergent structure | **Met.** An emotion is a routing motif: a recurring pattern in $\{\alpha,\beta\}$ across slots and time scales. Valence and arousal are read out (see §4). |
| Others read through own body | **Met by construction.** It is the key space itself. |
| Frozen LLM coupled without words | **Met.** See §4, Regulation and coupling. Claude sees no numbers or labels. |
| Satiable drives | **Met.** A satisfied variable's token is deleted from the pool. |
| Time scales from reflex to temperament | **Met.** Comes from the $\tau_i$ spectrum. |
| Scarce real data | **Partly met.** The hardest part of attention, the key geometry, is given innately by the body. Only queries, values and $\tau$ are learned. |
| Real-time face | **Met.** About 16 slots × 64 tokens at 30 Hz is trivial on Apple silicon. |

What stays open or breaks:

1. **The drive-to-action path is weak.** Without reward, actions that relieve a need come only from episodic association: a body token's value comes to carry the motor programs that preceded its last mass drop. This is the least novel part and leans on episodic control.
2. **The text-to-motor key may carry little affect.** It depends on how much the speech model's prosody predictor carries beyond syntax.
3. **Reranking costs latency and API calls,** because it needs K candidates per turn.

## 4. Principle 10 components, and perceiving the other

**Drives and needs:**

- **Homeostasis.** A body token's mass is the deficit. Need-conditioned salience is that mass biasing every slot's softmax. Satiety removes the token, so the bias vanishes.
- **Curiosity.** $\mu(x_j)$ includes the token's current prediction residual. The innate orienting head queries it, and learned slots inherit it because residual tokens predict future change, which reduces $\mathcal{L}$.

**Affect readouts:**

- **Arousal** is the rate of routing change, $\lVert\dot\alpha\rVert$ (entropy collapse).
- **Valence** is the predicted change in total pool mass under the current routing, $-\tfrac{d}{dt}\sum_{\text{body}}e^{m_j}$ through $F$.

**Social:**

- **Mimicry.** A slot binds to the other's face token. Its value *is* an own-motor program, so the action readout re-emits it, with lag set by $\tau_i$.
- **Reading others.** A query built from the other's motor key retrieves own episodes keyed by similar programs. Their stored slot states are the inferred state of the other: inversion of one's own generative mapping by retrieval.

**Regulation and coupling (Claude):**

- **Regulation.** Claude's voluntary intent and any reappraisal text enter as tokens through the text-to-motor key, so they re-route the slots instead of setting values.
- **Context composition.** Slot queries over the episode store choose which past transcripts enter Claude's context. Mood-congruent recall follows.
- **Somatic reranking.** Claude's K candidate openings are keyed by their own-voice and own-face trajectories, and the slots' attention picks one.
- **Budget and timing.** The thinking budget and reply latency follow routing entropy.
- **Own face as input.** Claude is shown its rendered face as an image.

**Memory and time:**

- **Replay.** Stored feature streams are re-run offline. Each episode is weighted by the KL between routing maps before and after it, and the weighted replay consolidates the queries of slow slots.
- **Temperament.** It lives in the slowest slots and in $W_q$.
- **Grounding.** Claude names replayed routing motifs, and the names are stored with the episodes, so a name attaches to a motif.

**Perceiving face and voice.** The coarse, dynamic and body routes are three tokenizers that feed one pool. The body route is $\mu$ itself. The coarse route enters through the innate CONSPEC head. Voice is inverted into the agent's own vocal-source parameters (F0, energy, timing, spectral tilt). Context dependence (Aviezer) comes for free, because conversation tokens compete in the same softmax.

**Structure ablation.** Collapse to one slot with uniform attention. The model can then no longer give the same smile different responses by partner or topic. EKA predicts partner- and topic-specific mimicry gain matrices whose rank exceeds 1.

## 5. First distinctive prediction, on published data

**Prediction: repertoire-biased mimicry.** Others are read and echoed through one's own repertoire. A listener's echo of a partner's AU configuration should therefore be:

- (a) larger and faster for configurations near the listener's own frequent configurations, beyond base rates, and
- (b) **shifted toward the listener's nearest own prototype.** The residual (echo − partner configuration) should correlate positively with (nearest own prototype − partner configuration).

**Data:** Meta Seamless Interaction, with the CANDOR corpus (Reece et al. 2023) as a second set. I am fairly sure both exist; check the access terms and whether there are enough minutes per participant.

**Analysis:**

1. Estimate each person's own prototypes by k-means on their AU vectors from the first half of the session.
2. Test the second half with windowed cross-lagged correlation (Boker et al. 2002).
3. Compare against segment-shuffled pseudo-dyad surrogates (Ramseyer and Tschacher).

**Model comparison:** an EKA model whose keys are the listener's own trajectories should predict listener AUs better than a parameter-matched Perceiver with learned keys, and most of all in the low-data regime (the first 5 minutes).

## 6. Most likely failure mode

**Routing collapse into an echo.** The motor key space is only about 50 dimensions. If slots do not differentiate, every slot binds to the partner's face token and the system becomes a delayed copier: high E3 coupling, but no dependence on state under steering (E2 fails). In effect it would be a GRU on blendshapes, the one-dimensional failure again.

**Mitigation, untested:** diversity pressure across slots and the innate heads. If these do not hold, the richness claim fails.
