# Sketch v2: Shared-Charge Routing (lens: mixture-of-experts, slots, modular and continual learning)

**Core idea in one sentence.** The affective state is not a vector. It is a **sparse routing graph** between *slots* (self, the person in front of me, remembered people and topics) and a growing library of tiny *sensorimotor modules* written in the agent's own body coordinates. Its one non-standard ingredient is a **charge** on each module, shared by every slot that routes through it. Because the charge is shared, reading the other person through a module primes my own use of that module. Contagion, mood, mood-congruent recall and temperament all come out of this one quantity.

## 1. Core mechanism

Per-slot routing (a top-$S$ sparse softmax over modules):

$$
R_{jk,t}=\operatorname{top}_S\,\operatorname{softmax}_k\Big[\underbrace{\tfrac{(W_q[z_{j,t};e_t])^{\top}\kappa_k}{\sqrt d}}_{\text{content}}\;+\;\underbrace{\alpha\log(\epsilon+c_{k,t})}_{\text{shared charge}}\;-\;\underbrace{\lambda\,\ell_k(x_{j,t-w:t})}_{\text{fit}}\;+\;\underbrace{\gamma\,\langle -n_t,\widehat{\Delta n}_k\rangle}_{\text{need}}\Big]
$$

The charge is the only state that crosses slots:

$$
\tau_k\,\dot c_k=-c_k+\textstyle\sum_{j}\omega_j R_{jk,t}
$$

Output and prediction:

$$
a_t=\textstyle\sum_k R_{\text{self},k,t}\,u_k(z_{\text{self},t})\;(+\text{voluntary path}),\qquad p(x_{j,t+1})=\textstyle\sum_k R_{jk,t}\,p_k(x_{j,t+1}\mid x_{j,t-w:t})
$$

There is one objective. Minimise the mixture negative log-likelihood of every slot's next observation, $\mathcal L=-\sum_{t,j}\log\sum_k R_{jk,t}\,p_k(x_{j,t+1})$, with a description-length penalty $\beta K$ on the size of the library. Modules learn from responsibility-weighted error, as in EM. A new module is spawned when no existing module fits a slot's stream better than a fixed novelty threshold.

Read the charge as the time-decaying **global weight of a hierarchical mixture**. The slots are the groups and the modules are shared atoms (structurally like a hierarchical Dirichlet process, which I have not checked against its primary source for this sketch). Contagion is then what happens when groups share statistical strength.

Symbols:
- $j$: slot. The slots are *self*, *other* (the current partner), and episodic slots instantiated by retrieval (a remembered person, a topic).
- $z_{j,t}\in\mathbb R^{d}$: slot state, a small GRU with weights shared across slots ($d\approx32$).
- $x_{j,t}$: the slot's stream in **own-body coordinates**. For self, this is efference (own AUs and prosody) plus body variables. For other, it is the perceived face mapped to own-AU space (body route) plus the partner's prosody.
- $e_t$: embedding of conversation events, including Claude's own words.
- $k$: module, $1\le k\le K(t)$, with $K$ growing from $K_0$ innate modules to a few hundred. Each module $m_k=(\kappa_k,\,p_k,\,u_k,\,\widehat{\Delta n}_k,\,\tau_k)$:
  - $\kappa_k\in\mathbb R^d$: key.
  - $p_k$: forward model of a short window of the stream.
  - $u_k$: motor primitive (an AU and prosody trajectory).
  - $\widehat{\Delta n}_k$: the module's predicted change in needs when it drives self.
  - $\tau_k$: time constant, learned, initialised log-uniform between 0.1 s and 6 h.
- $c_{k,t}\ge0$: charge.
- $\omega_j$: slot weight on charge ($\omega_{\text{self}}=1$, $\omega_{\text{other}}<1$).
- $\ell_k$: module $k$'s recent prediction error on slot $j$.
- $n_t=b_t-b^*$: need vector. This is the only homeostatic input.
- $\operatorname{top}_S$: keep the $S\approx4$ largest entries and renormalise.

## 2. Why it is new, and the closest prior work

- **MOSAIC (Wolpert, Doya and Kawato, Phil. Trans. R. Soc. B 2003; read pp. 593–598).** Multiple paired predictor–controller modules. Responsibilities come from prediction error, and the *observer's own* modules are run on another's movement to encode it as a symbolic module sequence. This is the closest ancestor of my fit term and of "read others through my own body". Three differences:
  1. In MOSAIC, the responsibilities for the observed actor are computed and then used for imitation. Nothing persists across self and other. Here, a **charge with a module-specific time constant, shared across slots**, is the substrate of affect, and it makes contagion, mood and carry-over follow from the same variable.
  2. MOSAIC's priors come from context. Here, the routing prior is conditioned on content and on needs.
  3. MOSAIC has a fixed module set. Here, the library grows continually.
- **Neural Production Systems (Goyal et al. 2021) and Recurrent Independent Mechanisms (Goyal et al. 2019).** I read the abstracts only. They provide the slots × rules and competing-module machinery. Their rules are stateless templates (NPS), or their modules hold private state with sparse communication (RIMs). Neither has a *usage trace shared across entities* that biases future routing for other entities, and neither is tied to a body, a motor output or needs.
- **Switch-style mixture-of-experts.** Same routing arithmetic. There, routing is a compute device and carries no meaning. Here, the routing graph *is* the state.

What is new is a **cross-slot charge field over a shared expert library**: a mixture-of-experts whose expert-usage history is the mood, and whose sharing across self and other is the contagion. This is not active inference, homeostatic RL or a value readout. The need term is one additive bias on routing, and it vanishes at the set point.

## 3. Constraints

| Constraint | Status |
|---|---|
| No labels | **Met.** Inputs are AUs, prosody and body variables. Modules are unnamed. |
| Emotion as emergent structure | **Met.** An "emotion episode" is a recurring *coalition*: a sparse set of modules co-charged across slots. Emotion concepts are communities in the long-run co-charge graph. Valence and arousal are readouts: arousal $=\sum_k c_k/\tau_k$ (fast charge); valence $=\sum_k c_k\langle -n,\widehat{\Delta n}_k\rangle$. |
| Others read through own body | **Met by construction.** The other's slot can only be explained by my own modules. |
| Frozen LLM coupled without words | **Met.** Every memory item is stored with the charge vector $c$ at the time it was encoded. Claude's context is assembled by $\operatorname{sim}(c_t,c_{\text{item}})$, restricted to the active slots, so recall is coalition-congruent and specific to the person. Routing load sets the thinking budget, reply length and delay. Which of the user's cues reach Claude as observations is decided by the other slot's top modules. Claude's own text enters $e_t$, so a reappraisal reroutes the slots. No numbers or labels reach Claude. |
| Satiable drives | **Met.** The need term is proportional to $n$ and is zero at $b^*$. There is no reward for smiles. |
| Time scales from reflex to temperament | **Met.** Reflex: innate modules with fixed keys and $\tau\approx0.1$ s. Episode: seconds. Mood: the charge of long-$\tau$ modules (minutes to hours). Consolidation: nightly replay. Temperament: the library itself plus the stationary charge distribution (weeks). |
| Scarce real data | **Partly met.** Modules are tiny (about 10k parameters, linear-Gaussian or 2-layer). Sparse routing protects rarely used modules from being overwritten, which works as continual learning without replay of everything. The weak point is that a router can collapse when data are scarce. |
| Real-time face | **Met.** Routing $K\le256$, $d=32$ at 30 Hz is negligible on Apple silicon, and the fast loop never waits for Claude. |
| Principle 10 (one core) | **Open risk.** One likelihood objective is stated, but $\alpha,\gamma,\omega$ are hyperparameters whose values the core does not fix. |
| Brief's "need-conditioned attention" | **Met.** The need term enters the *query* for every slot, including the other's, so needs bias what I perceive in them. |

## 4. Principle 10 components, one line each

- **Homeostasis:** the need term selects self modules whose predicted effect reduces $\lVert n\rVert$. The term is satiable.
- **Curiosity:** spawning, plus gaze and orienting toward the slot with the largest residual mixture NLL. The description-length objective rewards attending where the library is worst.
- **Valence and arousal:** the readouts above. Neither feeds back.
- **Mimicry:** the other's slot charges module $k$, and the charge raises $k$'s logit for self, which emits $u_k$. *Ablation:* give each slot a private charge. Mimicry and contagion vanish, while reading accuracy ($\ell$ on the other's slot) is unchanged.
- **Reading others:** $R_{\text{other},\cdot}$ says which of my own ways of moving explains them. Their likely need change is $\sum_k R_{\text{other},k}\widehat{\Delta n}_k$, an inversion through my own modules.
- **Regulation:** Claude's words in $e_t$ change the queries (reappraisal), and the voluntary motor path mixes with $a_t$. *Ablation:* drop $e_t$ from the queries.
- **Replay:** offline, stored feature streams are rerouted. Episodes are prioritised by the change in charge they caused. Modules are updated, merged when they are always co-routed, split when bimodal, and frozen when rarely routed. Claude may watch the replay of a coalition and name it, which grounds the concept as a community name kept on the text side only.

**Perceiving face and voice.** A fast coarse route (a CONSPEC-like innate module) instantiates the *other* slot when a face is present. The body route maps the face to own-AU coordinates, using MediaPipe for now and the agent's own inverse model in S4. Together with prosody, this forms $x_{\text{other}}$. The dynamic route (MARLIN-type features) enters only the query, as context. Perception *is* routing: the other's face is understood as the set of my modules that best predict it.

## 5. First distinctive prediction, and published data to test it

**Prediction: coalition-specific carry-over.** A partner's expression primes the listener's *own* module coalition with the decay of that coalition. Some coalitions should outlast the partner's expression by tens of seconds. Per-AU instantaneous coupling cannot do this, and neither can a 1-D or 2-D (valence/arousal) charge.

**Test** on **Meta Seamless Interaction** (arXiv 2506.22554), with AUs extracted by OpenFace or Py-Feat as a human-side measurement:
1. Fit the library on participants' **own** streams only (self slot, no partner).
2. Freeze the library, then route each partner's stream and integrate their charge.
3. Predict the listener's routing at $t+\Delta$ from the partner's charge, beyond (a) the partner's raw AUs in a ±5 s window, analysed with windowed cross-lagged correlation (Boker et al. 2002), and (b) a pseudo-dyad surrogate baseline.

The prediction is a gain for $\Delta=10$–$30$ s that is concentrated in modules with large fitted $\tau_k$. The same pipeline with $K=1$ or a 2-D charge should show no such gain. **Falsified** if the partner's charge adds nothing beyond the 5 s window, or if the low-dimensional version matches it.

## 6. Most likely failure mode

**The modules carve the stream along articulation and pose, not affect.** Speaking versus listening, visemes and head pose dominate AU variance, so with scarce data the router learns "talking" coalitions or collapses onto a few modules. Charge carry-over would then reflect turn-taking or a shared topic (a common cause), not contagion. Mitigations: route articulation through a separate speech pathway before modules see the stream, use load-balancing penalties, and control for topic and turn in the test. If carry-over survives none of these, the mechanism is wrong.
