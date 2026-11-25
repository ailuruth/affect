# Critique: v2-attention-architect (efference-keyed attention, EKA)

Critic: an independent subagent that did not write any sketch. Written 2026-11-25 under questions.md Q8 (critique round) and Q9 (novelty test). Nothing here is measured. The verdicts are arguments, not results.

**Sources read for this critique**, in primary form. The extracted PDF text was read with grep and by section; the read scope is given for each.
- Wolpert, Doya & Kawato 2003, "A unifying computational framework for motor control and social interaction", Phil. Trans. R. Soc. B 358:593–602. **Read in full** (author copy, bicr.atr.jp/~kawato/Ppdf/ROY03.pdf).
- Demiris & Khadhouri 2006, "Hierarchical attentive multiple models for execution and recognition of actions" (HAMMER), Robotics and Autonomous Systems 54:361–369. **Read sections 1–4.2** (background, architecture, top-down attention, implementation). The results tables were not read.
- Locatello et al. 2020, Slot Attention, arXiv 2006.15055. **Read §1–2** (method, Algorithm 1).
- Jaegle et al. 2021, Perceiver, arXiv 2103.03206. **Read §3.1** (architecture).
- Goyal et al. 2019, Recurrent Independent Mechanisms, arXiv 1909.10893. **Read §2** (method).
- Yamashita & Tani 2008, MTRNN, PLoS Comput Biol 4:e1000220. **Read only the model passages and figure captions**, not the full results.
- Kilner, Friston & Frith 2007, "Predictive coding: an account of the mirror neuron system", Cogn Process 8:159–166. **Read the abstract and the passages on generative-model inversion.** The two-column extraction was garbled, so only short quoted sentences are used.
- Ng et al. 2022, Learning to Listen, arXiv 2204.08451. **Read §1–6**, plus the Appendix D passage on person-agnostic models.

Named in the sketch or below but **not read here**, so no claim from them is relied on: JEPA, CONSPEC (Morton & Johnson), Boker et al. 2002, Ramseyer & Tschacher, Aviezer, Damasio, Joffily & Coricelli, Schaul et al. 2016.

---

## 1. Parts list (novelty test)

| # | Part of the core mechanism | Existing mechanism | Evidence (quoted from the primary source) |
|---|---|---|---|
| 1 | Slots $s_i$, each a leaky integrator $\tau_i\dot s_i=-s_i+\dots$ with log-spaced $\tau_i$ | Continuous-time RNN with multiple time scales (MTRNN); latent arrays (Perceiver) | MTRNN: "Context units were divided into two groups based on the value of time constant τ: a group of fast context units (τ = 5) and a group of slow context units (τ = 70)." EKA uses more than two time constants. That is a hyperparameter choice, not a new computation. |
| 2 | Cross-attention from slot queries $W_q s_i$ to a token pool, softmax over **tokens** | QKV cross-attention from a latent array (Perceiver), and per-module input attention (RIMs) | Perceiver: "a cross-attention module that maps a byte array … and a latent array to a latent array." RIMs: "the queries come from the RIMs, while the keys and values come from the current input." |
| 3 | Key $=\mu(x_j)$, a fixed map from a token to the own-motor trajectory that would reproduce it | An inverse model (MOSAIC, HAMMER) used as a **frozen key encoder** for standard attention | MOSAIC: "each controller in the observer generates the motor command which it would produce given the observed trajectory and current state of the actor." HAMMER: "the motor control systems of a robot … can be used in the dual role of (a) competitively selecting and executing an action, and (b) perceiving it." |
| 4 | Value $v_j=[\mu(x_j);F(\mu(x_j),S_t)]$: the motor program plus the forward model's predicted consequence | A MOSAIC/HAMMER predictor–controller pair | HAMMER: "The building block of HAMMER is an inverse model paired with a forward model." MOSAIC: "the output of each controller forms the input to its paired predictor, thereby generating a prediction of the next likely state." |
| 5 | Log-mass $m_j$, an additive logit bias that goes to $-\infty$ at the set point so the token leaves the pool | An additive attention bias, or a mask (causal masking; the RIMs null token; the Hopfield forgetting bias) | RIMs: "We first concatenate a row full of zeros" and select the RIMs "which have the least attention on the null input." Need-weighted salience is the *use* of the bias, not a new operation. |
| 6 | Slot-to-slot attention $\beta_{il}$, with slow slots biasing fast slots' queries | RIMs communication; HMOSAIC top-down priors | RIMs: "we allow the activated RIMs to read from all other RIMs (activated or not)." HMOSAIC: "The output of higher-level modules is a set of (top-down) prior probabilities of the subordinate modules, which act to prioritize lower-level module selection." |
| 7 | Innate heads: fixed, untrained query rows | Frozen parameters inside an attention layer | No new computation. CONSPEC as a content prior was not read here. |
| 8 | Action readout $a_t=\sum_c \mathrm{softmax}_c(\langle W_a\bar s,\mu(c)\rangle)\,c$ over the own repertoire | Soft selection over a motion codebook (Learning to Listen's VQ codebook); MOSAIC's responsibility-weighted controller mixture | L2L: "Our autoregressive Predictor outputs a distribution over the K discrete codebook indices." MOSAIC: "The outputs of the controllers are weighted by the likelihood that each is appropriate, to determine the final motor command." |
| 9 | Loss: latent prediction of $\mu(X_{t+\Delta})$ with stop-gradient, plus cycle consistency $M(\mu(x))\approx x$ | JEPA-style latent prediction (not read here); autoencoder/cycle consistency; MTRNN's next-step prediction of own proprioception | MTRNN: "the system generated predictions of proprioception $m_{t+1}$ and the vision sense $s_{t+1}$ for the next time step." |
| 10 | Arousal $=\lVert\dot\alpha\rVert$; valence = predicted change in body-token mass | Readouts (the class Q9 names: "value or price readouts") | They are read out of the state and do not drive it. |
| 11 | Replay weighted by the KL between routing maps | Prioritized replay (Schaul et al. 2016, not re-read here) with a different priority score | — |
| 12 | Somatic reranking of K Claude drafts | Best-of-K reranking by a scoring model | Not part of the core. |

**Every part maps to an existing mechanism.** The sketch's own novelty claim, "attention whose metric is the agent's own body", is a choice of **key space** for ordinary attention. Q9 rules this out explicitly: "If every part is an existing mechanism … the candidate is a recombination: record it as one, whatever the key space."

The point is sharper for the stage the sketch would actually run at. Until S4, $\mu$ for the other's face is "MediaPipe blendshapes" (sketch §1). The "inverse model" is then the identity on borrowed blendshape coordinates, so EKA is a Perceiver/RIMs-style cross-attention whose key projection is frozen to the identity on AU features. The model comparison the sketch proposes, "EKA … should predict listener AUs better than a parameter-matched Perceiver with learned keys", therefore compares frozen against learned keys. That is a test of key learning under scarce data, not of embodiment.

## 2. Closest prior work, read in full

### 2.1 MOSAIC / HMOSAIC (Wolpert, Doya & Kawato 2003), read in full

MOSAIC already contains EKA's three social claims.
- **Others read through own controllers:** "the observer uses his own multiple modules to try to simulate the observed percept."
- **Others represented in one's own repertoire:** "the movement is represented in the observer's private lexicon … The more different the MOSAICs the harder it may be for the observer to represent the actor's behaviour."
- **Imitation biased by one's own repertoire:** "This information can either replace the observer's usual sequence of module activation or be used to bias it."
- **Slow levels prioritizing fast selection:** HMOSAIC's top-down priors.
- **Partner identity as context:** "different people will react in different ways to the same input. Therefore both control and social interaction have to take into account the context, whether it is the identity of a tool or the identity of another person."

What EKA does that MOSAIC does not:
1. **How selection works.** MOSAIC selects modules by **prediction error**: "the sensory prediction error from a given forward model is represented as a probability; if the error is small then the probability that the forward model is appropriate is high." EKA selects tokens by a **query from the agent's own slow state** dotted with motor keys. In EKA, selection can therefore precede evidence, being driven by need and mood. In MOSAIC it follows evidence. This is a real difference in the selection rule, but the EKA rule is standard attention.
2. **What is selected among.** EKA attends over an open pool that includes memories, body tokens and text, all mapped into motor space. MOSAIC attends over a fixed module set.
3. **Explicit time constants.** EKA has a $\tau$ spectrum. MOSAIC has hierarchy but no stated time constants.

MOSAIC states its own limits: "We have yet to simulate the hierarchical action understanding." It has never been tested on facial dyads. EKA would be a first test of a MOSAIC-like idea on face data, not a new idea.

### 2.2 HAMMER (Demiris & Khadhouri 2006), §1–4.2 read

HAMMER is the closest prior work for the *attention* part, and the sketch does not cite it. HAMMER already derives top-down attention from inverse models: "for a given action, the information that the attention system will try to extract during the action's demonstration is the state of the variables the corresponding inverse model would have control if it was executing this action." It also weights by confidence: "the saliency of each request can be made a function of the confidence that each inverse model possesses."

The difference is that HAMMER's inverse models sit on the **query/request** side and allocate a scarce sensor through round-robin or confidence-based arbitration. EKA puts the motor program on the **key** side and uses soft dot-product attention. HAMMER is also tiny ("In total, eight inverse models were used"; "Forward models were handcoded"). EKA's addition is "HAMMER with soft QKV attention, learned queries, multiple time scales and an open token pool". That is a recombination.

### 2.3 Perceiver, Slot Attention and RIMs (§2–3.1 read)

EKA's state update is Perceiver cross-attention (latents query inputs, softmax over inputs) plus RIMs communication (modules read other modules), run as leaky ODEs.

**One detail matters for break (a).** Slot Attention's defining choice is to normalize "over the slots, i.e., the queries … This choice of normalization introduces competition between the slots for explaining parts of the input." EKA normalizes over **tokens**: $\operatorname{softmax}_j$ in the sketch's equation. EKA therefore lacks the one mechanism in this family that prevents every slot from binding to the same input. The sketch cites Slot Attention as a neighbor without adopting its anti-collapse normalization.

### 2.4 MTRNN (Yamashita & Tani 2008), model passages only

MTRNN is a dynamical-systems precedent for two EKA ideas: multiple time constants in one recurrent net, and training by predicting one's own next proprioception and vision. Functional hierarchy emerged from the time-constant difference alone. Like MOSAIC, MTRNN predicts in its own body coordinates. EKA adds attention over a token pool, which MTRNN lacks. Only the model description and figure captions were read here.

**Net: what EKA does that none of the four does.** It is the one network that applies a single motor-space key to faces, voice, episodes, body deficits and the language model's drafts at once. That is a scope claim, not a computation. The selection, value and update rules all exist in the works above.

## 3. Reduction attempt

**Rewrite.** EKA is a Perceiver-style latent array with RIMs-style inter-latent attention, integrated as leaky ODEs with MTRNN-style multiple time constants. Its keys come from a frozen encoder: a MOSAIC/HAMMER inverse model, or MediaPipe AUs before S4. Its values are MOSAIC predictor–controller outputs. It has additive logit masks for satiated needs and a soft codebook action head as in Learning to Listen. It is trained by JEPA-style latent prediction.

**What is left after the rewrite.** Nothing computational. The remainder is (i) the choice to put text, body deficits and episodes into the same motor key space, and (ii) the interpretation that emotion is a recurring routing motif. Choice (i) is a key-space choice, and Q9 counts it as recombination. Item (ii) is a readout/interpretation.

**Verdict: recombination.** No new computation. If one candidate for a new computation had to be named, it would be "a single frozen embodiment-derived key space shared across perception, memory, interoception and language". That is a representational commitment inside standard attention, not a new operation.

## 4. Break attempts on the shared risks

### (a) Collapse into a delayed copy of the partner. Strong break, partly admitted.

The scenario has five steps.
1. Take the pre-S4 system, where $\mu$ of the other's face is their MediaPipe blendshapes and $\mu$ of one's own face is one's own blendshapes. The partner token and an own-expression token showing the same face then have **identical keys**. The sketch gives no source tag that separates "they smiled" from "I smiled".
2. The loss predicts $\mu(X_{t+\Delta})$ of the joint stream. In conversation, the listener's next face is far more predictable from its own last face and from a lagged copy of the partner than from anything slow.
3. The values *are* motor programs, and the action head re-emits them: "Its value *is* an own-motor program, so the action readout re-emits it". Every slot that binds to the partner token therefore outputs a scaled copy of the partner, lagged by $\tau_i$.
4. Because softmax runs over tokens (§2.3), nothing stops all slots from binding to the partner token.
5. Nothing in $\mathcal L$ penalizes excess synchrony.

The predicted collapse is $a_t\approx g\cdot\mu(\text{partner}_{t-\delta})$ with $\delta$ set by the dominant $\tau_i$. That is the "Delayed Mirror" baseline of Learning to Listen.

**This has happened to a published listener model.** Learning to Listen reports that the earlier LFI model, retrained on in-the-wild data, "defaulted to mirroring the speaker, resulting in excessively high synchrony (PCC)". In L2L's Table 1 (their numbers, on their data, not measured here), expression PCC is GT 0.09, Mirror 1.00, Delayed Mirror 0.98, LFI 0.89 and L2L 0.07. L2L adds that "a mime that mirrors the speaker like Mirror and Mirror Delay looks uncanny due to excessive variation and synchrony."

MOSAIC also names the mechanism: when the observer cannot interpret a movement at higher levels, imitation ends up "slavishly replicating kinematics."

**Does the sketch answer it?** It names the risk in §6: "Routing collapse into an echo … the system becomes a delayed copier." The only mitigation is "diversity pressure across slots and the innate heads", marked untested. **The answer is weak.**

Cheap fixes the sketch could adopt:
- slot-axis normalization, as in Slot Attention;
- a self/other source embedding added to keys;
- a falsifiable guard: the model's expression PCC and its TLCC peak must stay within the human range on held-out dyads, not drift toward 1.

### (b) A single hidden dial from flat affect to rigid imitation. Moderate break, partly answered.

- **Where the dial is.** The temperature is fixed at $1/\sqrt d$, but the query norm $\lVert W_q s_i\rVert$ acts as an inverse temperature. The output is a convex combination of motor programs in a space of about 50 dimensions. How much the face follows the partner is the attention mass on the partner token, a monotone function of the query's projection on the partner-key direction.
- **How the dial forms.** Suppose the slots do not differentiate (see (a)) and the slow slots learn only an overall gain. A low gain gives a mean face (flat affect), and a high gain gives a delayed copy. The $\tau$ spectrum adds smoothing, not a second dimension.
- **The sketch's answer.** The structure ablation predicts "partner- and topic-specific mimicry gain matrices whose rank exceeds 1". That is a falsifiable answer and the right kind. Two gaps remain:
  1. Rank must be estimated with cross-validation, because a few hours of data will give rank > 1 from noise.
  2. A one-dial comparator should be fitted explicitly: the same model with all slots tied and one learned gain. Then report the held-out likelihood difference.

The answer is **partial**.

### (c) A lookup table of past faces under scarce data. Moderate-to-strong break, not answered.

The action is by construction a convex combination over the own repertoire $\mathcal C$, and reading others "retrieves own episodes keyed by similar programs". The key geometry is fixed, so retrieval similarity is raw motor-feature similarity, and the sketch presents that as a data-efficiency strength. With little data, $\mathcal C$ and the episode store are small, and the model reduces to kernel regression from the current partner face to stored own faces. That is a smoothed version of L2L's "NN motion" baseline: "Given an input speaker motion, we find its nearest neighbor from the training set and use its corresponding listener segment as the prediction."

In L2L's Table 1 that baseline was strongest among the non-learned ones on L2 but poor on realism (expression FD 20.66 against L2L's 3.55) and on synchrony (PCC 0.02 against GT 0.09). The sketch does not address (c) directly. Its scarce-data row says the key geometry "is given innately", which makes the risk worse, not better.

### A further problem: the first prediction does not discriminate

Prediction 5(b) says the residual (echo − partner) correlates with (nearest own prototype − partner). That holds for a listener who **ignores the partner entirely**: if the "echo" is just the listener's habitual face, the residual points at the listener's own prototype by definition. The sketch applies its surrogate control (segment-shuffled pseudo-dyads) only to the cross-lagged correlation step. It must also be applied to 5(b), and the effect must exceed the pseudo-dyad value.

Even then, any person-specific listener model predicts repertoire-biased echo, including L2L's per-listener models ("person-specific modeling better captures individualistic listening styles and mannerisms") and MOSAIC ("private lexicon"). A prediction that EKA, MOSAIC and the published baseline all make cannot select EKA.

## 5. Which measured failure of published listener models this might fix (hypothesis only)

Nothing has been measured in this project. These are failures **reported by the published papers themselves** that EKA could plausibly address:
- **Generalization to a new listener from little data.** L2L trains person-specific models on hours of one host and reports that person-agnostic models lose individual style. Hypothesis: EKA's frozen motor keys plus a repertoire built from the first minutes of a new listener predict that listener's AUs better than a person-agnostic L2L in the first 5 minutes. This is the sketch's own model comparison, and the weakest-assumption target it has.
- **Context dependence (misreading under context).** L2L conditions only on speaker motion and audio, with no state beyond its context window. EKA lets conversation tokens compete with face tokens in one softmax. That is a plausible fix for "the same smile, different response by topic", but it needs a published task scoring context-dependent listener response. None is named.
- **Not a plausible fix: collapse into a delayed copy** (the LFI failure). It is EKA's own most likely failure (§4a).

Q9 requires a measured failure before development, so all of these stay hypotheses until the L2L baseline is run on Seamless Interaction as published.
