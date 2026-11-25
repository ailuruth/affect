# Sketch v2: the dyadic contingency kernel (developmental lens)

Lens: a developmental psychologist of infant–caregiver interaction who also builds learning systems. Working hypothesis: an infant does not first have emotions and then express them. It first detects which of its own acts the caregiver answers, how fast and how much, and learns what its inner states are from the caregiver's contingent, exaggerated ("marked") reflections of them (Gergely and Watson 1996, social biofeedback). The engine's state should therefore be the dyad's contingency structure as seen from inside one party, not a vector describing one body.

## 1. Core mechanism

All signals live in the agent's own body coordinates. $x^s_t \in \mathbb{R}^d$ is the agent's own stream: its motor output $\mu_t$ (AU and vocoder parameters), an interoceptive embedding $e_\theta(\iota_t)$ of the body variables $\iota_t$ (one input among several), and an embedding of its own last utterance while speaking. $x^o_t = G_\theta^{-1}(o_t) \in \mathbb{R}^d$ is the partner's face and voice mapped into the same coordinates by the inverse of the agent's own forward model $G_\theta$ (own motor parameters to own rendered face and voice).

**State.** A bank of directed, lag-resolved, multi-scale associative operators (fast weights):

$$\mathcal{S}_t=\{K^{ab}_{k,t}(\tau)\in\mathbb{R}^{d\times d}\;:\;(a,b)\in\{(s,o),(o,s),(s,s)\},\;\tau\in\Lambda,\;k=1..m\}$$

$K^{so}$ means "what they do $\tau$ after I do something". $K^{os}$ means "what I do after they do something". $K^{ss}$ is perfect self-contingency, the body. $\Lambda$ is a set of lags (e.g. 16 bins, 0.1–3 s). $k$ indexes time scales with decay $\lambda_k$: about 0.5 s (reflex), 10 s, 20 min (mood), and days (temperament, reached through replay).

**Update (delta rule, every frame at 30 Hz):**

$$K^{ab}_{k,t}(\tau)=\lambda_k K^{ab}_{k,t-1}(\tau)+\eta_k\big(x^b_t-K^{ab}_{k,t-1}(\tau)\,x^a_{t-\tau}\big)\,x^{a\top}_{t-\tau}$$

**Prediction** with content-dependent attention over scales and lags:

$$\hat x^b_t=\sum_{k,\tau}\alpha_{k,\tau}(q_t)\,K^{ab}_{k}(\tau)\,x^a_{t-\tau}$$

The query $q_t$ is the current expected-but-missing response $\Delta_t=\hat x^o_t-x^o_t$ together with conversation events. **Contingency profile:** $\Gamma_t\in[0,1]^{C\times m}$ is the per-channel, per-scale fraction of the partner's variance explained by the agent's own past. It is a vector over channels and scales, not one scalar.

**Action** (the same state drives face, voice and Claude's sampling):

$$\mu_{t+1}=\underbrace{\rho(x^s_t)}_{\text{innate reflexes}}+\underbrace{\textstyle\sum_{k,\tau}\alpha\,K^{os}_k(\tau)\,x^o_{t+1-\tau}}_{\text{attunement / mimicry}}+\underbrace{\gamma_t\,\textstyle\sum_\tau K^{so}_{\text{slow}}(\tau)^{\top}\Delta_t}_{\text{bid: replay the own act that used to elicit the missing response}}$$

$$\gamma_t=\operatorname{dist}\big(\Gamma_t,\,[\kappa_{lo},\kappa_{hi}]\big)$$

$\gamma_t$ is zero inside the band, so the drive is satiable. Below the band (partner unresponsive) the agent bids. Above it (a perfect echo, which is self-like) the attunement gain is lowered and the agent turns away.

**Marked-mirror binding** is the slow objective that grounds inner states:

$$\mathcal{L}=\sum_{ab}\lVert x^b-\hat x^b\rVert^2+\;\mathbb{E}\big[\beta(m_t)\,\lVert x^o_t-W e_\theta(\iota_{t-\tau})\rVert^2\big]+\;\beta_{IB}\,I(\iota;e_\theta)$$

$m_t$ is the "markedness" of $K^{so}_{\text{fast}}$: gain $>1$ on the subspace of the agent's own recent expression with a small structured deviation. When the partner answers the agent's own expression in amplified, transformed form, that answer is treated as information about the *self*, and $e_\theta$ is trained so that its own interoceptive state predicts it. Slow parameters $\theta=\{G, e, W, \alpha, \rho\text{-thresholds}\}$ learn only from $\mathcal{L}$ and from replay. The kernels are not trained by gradient descent: they are the state.

**Emotion as structure.** Recurring configurations of $\mathcal{S}$ carry the affective content: the singular modes of $K(\tau)$, their lags and gains, and the gaps between scales. Three examples. "My bids are answered with gain > 1 at 0.5 s." "They lead and I follow at 1 s." "The fast $K^{so}$ has collapsed while the slow $K^{so}$ is intact" (protest, then withdrawal). These are relations, which no single-body vector contains.

**Coupling to Claude, without words:**
1. *Mirror priming.* Memory retrieval is keyed on kernel-configuration similarity, and what it returns is the **partner's own past words** from moments when the dyad had this contingency structure. Claude is primed by how the other reflected it before.
2. *Contingency-selected sampling.* Claude drafts N candidate replies. Each is embedded as $x^s$, the slow $K^{so}$ predicts the partner's response to it, and the engine sends the candidate whose predicted response moves $\Gamma$ toward the band. Claude never sees why.
3. The lag profile of $K^{os}$ sets reply onset and interruption tolerance.
4. Offline, Claude watches replays of kernel-configuration clusters and names them. The names are used only as retrieval keys.

## 2. Why this is a new mechanism

The state is a second-order relational operator: a learned, directed, lagged map between the self's past and the other's future, in the self's motor coordinates. It is updated by a local rule. It is not a posterior over hidden causes, a value, or a body-variable vector. The drive regulates a property of that operator (a contingency band), not an observation or a set point. Inner-state categories are learned by a binding term that treats marked partner responses as labels of one's own interoception, so the dyad builds the categories.

| Closest prior work | Precise difference |
|---|---|
| Friston and Frith 2015, generalized synchrony (from the brief) | There, coupling emerges between two belief states. Here the coupling is the state, and it is regulated into a band. That predicts that too-perfect contingency is aversive; synchrony maximization does not. |
| Boker et al. 2002, windowed cross-lagged correlation (from the brief) | There it is an analysis instrument computed by an observer. Here it is the agent's own state, made directed, multi-dimensional and multi-scale, and it drives action. |
| Schlag, Irie and Schmidhuber 2021 (delta-rule fast weight programmers; read the abstract) | Same algebra. The new parts are what the keys and values are (own past acts, the other's future in own body coordinates), reading the fast weights as affect, and the transpose-retrieval bid. |
| Gergely and Watson 1996 (abstract read) | A verbal theory. This sketch adds the binding loss and the band drive as equations. |
| Yoshida and Man | They invert one's own homeostatic model. Here the motor forward model is inverted, and the quantity shared between agents is contingency, not body state. |

## 3. Brief constraints

- **Met.**
  - *No labels anywhere:* the inputs are AU, prosody and vocoder parameters only.
  - *Emotion as emergent structure:* it is kernel geometry, with valence and arousal read out (section 4).
  - *Others read through own body:* via $G^{-1}$, $K^{os}$ and $K^{ss}$.
  - *Frozen LLM coupled without words:* retrieval of the partner's words, best-of-N selection by predicted contingency, and timing.
  - *Satiable drive:* $\gamma=0$ inside the band.
  - *Reflex to temperament:* $\lambda_k$ plus replay consolidation into the slowest $K$.
  - *Scarce data:* the kernels are learned in-session with no gradients. $G$ is learned from self-view motor babbling, which is self-generated and unlimited. Only $e$, $W$ and $\alpha$ need real dyadic data.
  - *Real-time face:* $3\times16\times4$ matrices of size $32\times32$ is about 200k multiply-adds per frame.
  - *Expressive structure:* need-conditioned attention ($\Delta_t$ as the query). Structure over people: one kernel bank per partner, which gives relationship specificity. Effective dimensionality is the participation ratio of the kernel modes. The low-dimensional ablation is scalar zero-lag synchrony.
- **Breaks or leaves open.**
  - The bid term is a one-step descent on a structural quantity. That is close to control, though not RL.
  - The markedness detector $m_t$ is an innate prior that I chose; it is not derived.
  - Delta-rule kernels confound caused contingency with co-driven covariation.
  - The inverse vocal model $G^{-1}$ for voice is unproven.
  - Best-of-N adds latency at the turn level, though never to the fast loop.
  - Adults rarely mark-mirror, so the binding signal with the operator may be weak.

## 4. Principle 10 components, and perception

- **Homeostasis:** band regulation of $\Gamma$. Body variables $\iota$ are extra channels of $x^s$, so their contingencies are regulated the same way.
- **Curiosity:** bids are biased toward channels where $K^{so}$ has the largest recent delta-rule error. This is contingency testing.
- **Valence and arousal:** read out, not set. Valence is $d\Gamma/dt$ along the attended channels (contingency gained or lost). Arousal is $\lVert\Delta K_{\text{fast}}\rVert$.
- **Mimicry:** the $K^{os}$ readout in shared motor coordinates. It is weak at first and grows wherever the partner leads.
- **Reading others:** their face and voice become $G^{-1}(o)$, and their state is the self-configuration that would have produced that act with that lag structure.
- **Regulation:** co-regulation through binding, since a marked contingent answer reduces interoceptive prediction error. Self- and Claude-regulation work by re-weighting $\alpha$ over scales (reappraisal as choosing which history governs the moment).
- **Replay:** nightly re-running of stored feature streams through the delta rule at slow scales, weighted by $\lVert\Delta K\rVert$. $e_\theta$ is retrained by binding during replay.
- **Perception:** the coarse route feeds $q_t$, so it is fast salience for the query. The dynamic route supplies $x^o$ channels. The body route is $G^{-1}$, which replaces MediaPipe in S4. Voice is analysis-by-synthesis into the agent's own vocoder parameters. Context (conversation events) enters the attention query, never alone.

## 5. First distinctive prediction: published data

**Data.** Ahn, Ertuğrul, Chow, Cohn and Messinger 2023, *Infancy* (doi 10.1111/infa.12556; read in full). Forty 4-month-old infants and their mothers did the Face-to-Face/Still-Face: 2 min face-to-face (FF), 2 min still-face (SF), 2 min reunion (RE). There is frame-level automated AU coding (AU4, AU6, AU12, AU20) for infant and mother. The data are openly available in Databrary volume 1474 to authorized investigators.

**Prediction.**
- **P1.** Compute the infant→mother kernel $K^{so}$ from the infant's FF stream. The mother's AU6 and AU12 at lags 0.3–2 s are predicted from the infant's AUs, and the explained variance gives $\Gamma^{so}$. Each infant's FF→SF decline in Duchenne smiling and its FF→SF increase in Duchenne cry-face should scale with $\Gamma^{so}$. This should hold after controlling for the mother's FF smiling proportion and for undirected zero-lag correlation.
- **P2.** The opposite-direction kernel (the infant following the mother) should predict a smaller effect.
- **P3.** Infant smile bursts during the SF should over-represent whichever smile type (Duchenne or non-Duchenne) the mother answered with the highest gain during FF. This is the transpose-retrieval bid.

The scalar-synchrony ablation predicts neither P2 nor P3. Ahn et al. report that infant and mother smiling *levels* were not associated in the first 30 s (Duchenne r = 0.09), which is consistent with level being the wrong statistic, but it is not evidence. Power: with n = 40, only partial correlations of about |r| ≥ 0.43 are detectable at 80% power. A null on P1 and P2 falsifies the claim that the still-face response is a collapse of the directed kernel. A one-to-one adult analog (who leads, and responses to partner stillness) can be run on Seamless Interaction.

## 6. Most likely failure mode

Spurious contingency. Adult conversation is full of shared drivers: both people laugh at the same content, and turn-taking imposes rhythm. The delta rule cannot tell "they answered me" from "we were both driven by the same thing", so $\mathcal{S}$ comes to encode conversational rhythm rather than affect. The band drive then turns into a metronome that treats every pause for thought, or every glance at a screen, as a still face and starts bidding. It would be needy rather than attuned. Conditioning the kernels on conversation events only partly helps. If, in addition, the operator rarely gives marked mirroring, the binding term never fires, $e_\theta$ stays unstructured, and the emergent "emotion" is only dyadic timing.
