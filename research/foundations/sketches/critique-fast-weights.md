# Critique: v2-fast-weights (affect as self-rewriting memory)

Critic: an independent subagent that did not write any sketch. Written 2026-11-25 under questions.md Q8 (critique round) and Q9 (novelty test). Nothing here is measured. The verdicts are arguments, not results.

**Sources read for this critique**, in primary form. The extracted PDF text was read with grep and by section; the read scope is given for each.
- Behrouz, Zhong & Mirrokni 2025, Titans, arXiv 2501.00663. **Read §2–3.1** (background, the memory update, surprise, forgetting, the persistent-memory definition).
- Ramsauer et al. 2020/21, "Hopfield Networks is All You Need", arXiv 2008.02217. **Read §1–2 in full** (energy, update rule, Theorems 1–5, metastable states) and **appendix A.1.8** (forgetting).
- Ba, Hinton et al. 2016, "Using fast weights to attend to the recent past", arXiv 1610.06258. **Read §1–2** (the fast associative memory and its settling).
- Schlag, Irie & Schmidhuber 2021, "Linear Transformers are secretly fast weight programmers", arXiv 2102.11174. **Read the delta-rule section and the conclusion.**
- Pritzel et al. 2017, Neural Episodic Control, arXiv 1703.01988. **Read §3** (DND lookup, writes, algorithm).
- Srivastava et al. 2019, "Training agents using Upside-Down Reinforcement Learning", arXiv 1912.02877. **Read §2–2.1** (behavior function, commands).
- Wolpert, Doya & Kawato 2003, MOSAIC, Phil. Trans. R. Soc. B 358:593–602. **Read in full.**
- Gerstner et al. 2018, "Eligibility traces and plasticity on behavioral time scales: experimental support of neoHebbian three-factor learning rules", arXiv 1801.05219. **Read the abstract and introduction only.**
- Ng et al. 2022, Learning to Listen, arXiv 2204.08451. **Read §1–6**, plus the Appendix D passage on person-agnostic models.

Named in the sketch or below but **not read here**, so no claim from them is relied on: complementary learning systems (McClelland et al.), Decision Transformer beyond its title page, Hindsight Experience Replay, Boker et al. 2002, Seamless Interaction's session-date metadata.

---

## 1. Parts list (novelty test)

| # | Part of the core mechanism | Existing mechanism | Evidence (quoted from the primary source) |
|---|---|---|---|
| 1 | Joint pattern $z_t=[m;p;b;e]$, with the partner in the agent's own motor coordinates | Feature concatenation; "partner in own coordinates" is the MOSAIC observation route | MOSAIC: "the visual information of the actor's movement must be converted into a format that can be used as inputs to the system such as the motor system." |
| 2 | Energy $E=-\tfrac1\beta\log\sum_i s_i e^{\beta k_i^\top x}+\tfrac12\lVert x\rVert^2-x^\top c_t$ | Modern Hopfield energy (Ramsauer Eq. 2), with **per-pattern log-weights** (Ramsauer A.1.8.2) and an **external input field** (Ba et al.'s "sustained boundary condition") | Ramsauer: $E=-\mathrm{lse}(\beta,X^\top\xi)+\tfrac12\xi^\top\xi+\dots$. A.1.8.2: "We introduce forgetting to the new Hopfield networks by adding a negative value in the softmax which increases with patterns that are more in the past." Ba et al.: the slow inputs are "maintained as a sustained boundary condition for a brief iterative settling process which allows the fast weights to influence the new hidden state." |
| 3 | Settling $\tau_x\dot x=-\partial_xE$, giving $x^*=K\alpha+c_t$ and $\alpha=\mathrm{softmax}(\beta K^\top x^*+\log s)$ | The Hopfield update, which is attention | Ramsauer: "Surprisingly, our new update rule is also the key-value attention as used in transformer and BERT models." Their update converges by CCCP (Theorem 1). |
| 4 | Read-out $\hat z=\sum_i\alpha_i v_i$, with values $(z,z^+,\text{ptr})$ | Heteroassociative key–value lookup: the NEC differentiable neural dictionary | NEC: "the output of a lookup in a DND is a weighted sum of the values in the memory, whose weights are given by normalised kernels between the lookup key and the corresponding key in memory." |
| 5 | Delta-rule write $\Delta\mathcal M=-\lambda_t\partial_{\mathcal M}\tfrac12\lVert\hat z^+-z_{t+1}\rVert^2-\gamma\mathcal M$ | Titans' surprise-gradient update with forgetting; Schlag's delta rule; Ba et al.'s decaying fast weights | Titans Eqs. 13–14: $\mathcal M_t=(1-\alpha_t)\mathcal M_{t-1}+S_t$, $S_t=\eta_tS_{t-1}-\theta_t\nabla\ell(\mathcal M_{t-1};x_t)$. Ba et al.: $A(t)=\lambda A(t-1)+\eta h(t)h(t)^\top$. |
| 6 | Write gate $\lambda_t=\sigma(w^\top[\lVert\varepsilon\rVert,\lVert\Delta b\rVert])$ | Titans' data-dependent step size $\theta_t$; a neoHebbian three-factor rule with surprise or body change as the third factor | Titans: "$\theta_t$ is controlling how much of momentary surprise should be incorporated … in a data-dependent manner." Gerstner et al.: "This third factor, signaling reward, punishment, surprise, or novelty." |
| 7 | Since $\hat z=\sum\alpha_iv_i$, the delta-rule gradient on $v_i$ is $\alpha_i\varepsilon$: writes are weighted by retrieval responsibility | MOSAIC's responsibility-gated learning | MOSAIC: "the responsibilities are used to gate the learning of the predictors and controllers." |
| 8 | Slot allocation when $\max\alpha<\theta$: a one-shot write | Append-only episodic writes (NEC); novelty-triggered allocation | NEC: "Writes to a DND are append-only: keys and values are written to the memory by appending them onto the end of the arrays." |
| 9 | Three plasticity classes (innate/frozen, slow/consolidated, fast/decaying) plus nightly replay | Titans' three memories (persistent, long-term test-time, short-term attention); complementary learning systems (not read here) | Titans: "Persistent Memory: this is a set of learnable but date-independent parameters that encodes the knowledge about a task." |
| 10 | Goal clamp: replace the body slot of the query with $b^*$ and use hindsight keys, so action is "what was done when the body ended up at set point" | Command-conditioned behavior from hindsight: the Upside-Down RL behavior function, estimated non-parametrically | UDRL: "a basic agent neither predicts values nor explicitly maximizes them, but instead only learns to interpret commands … Commands can specify requirements for desired behavior such as total return, desired goals to reach." UDRL Eq. 3 estimates $B_T$ by counting stored segments that achieved the command. The sketch's clamped retrieval is the kernel-smoothed version of that count, with command = desired body state. |
| 11 | Drive $=\lVert\hat z(c^*)-\hat z(c)\rVert$ | A readout: the difference of two conditional completions | — |
| 12 | Emotion = the write $\Delta\mathcal M$; arousal $=\lVert\Delta\mathcal M\rVert$; valence $=\sum\Delta s_i\cdot(-\lVert b(v_i)-b^*\rVert)$ | Readouts of the update. $\lVert\Delta\mathcal M\rVert$ is Titans' "surprise" (a gradient norm) times the gate. | Titans: "a simple definition of surprise for a model can be its gradient." |
| 13 | Energy reranking of $n=3$ Claude drafts | Best-of-n reranking by an energy score | Not part of the core. |
| 14 | An inverse map from face to own motor, learned by heteroassociating seen-own-face with $m$ | Associative learning of the inverse model ("motor babbling"), as in HAMMER's follow-ups (not read here) | — |

**Every part maps to an existing mechanism.** The sketch itself says "The new combination is: …" (§2) and lists three items:
- "Affect is the rewrite" is a readout (#12).
- "Homeostasis through hindsight-keyed goal clamping" is UDRL-style command conditioning (#10).
- "The same $\alpha$ drive face, reading and Claude" is a wiring choice.

### Two factual corrections to the sketch's §2

1. **"Modern Hopfield networks. Their memory is static at inference time."** This is not true of the family.
   - Ba et al. 2016 is a Hopfield-style fast associative memory that "is updated all the time and the writes are all superimposed on the same fast changing component of the strength of each synapse". It also uses settling under a sustained input, which is the sketch's $-x^\top c_t$ term.
   - Ramsauer A.1.8.2 already adds time-dependent log-weights to the patterns.

   So "a Hopfield landscape rewritten online with decaying weighted patterns" is prior work.
2. **"Titans … Eqs. 8–14: $\mathcal M_t=(1-\alpha_t)\mathcal M_{t-1}+S_t$, with $S_t$ the gradient".** This drops Titans' momentum term. In Titans, $S_t=\eta_tS_{t-1}-\theta_t\nabla\ell$ ("past surprise" plus "momentary surprise"). The omission does not change the verdict.

### An internal inconsistency that matters

§1 says "Keys carry the outcome that actually followed (hindsight keys)". The allocation rule writes the slot $(c_t,z_t,z_{t+1})$ with key $c_t=Q_\phi(\text{observed parts of }z_t)$. That key holds the *current* body, not the outcome. The delta rule is "applied to slot values and strengths", not keys, so keys never acquire the outcome.

As written, clamping $b^*$ into the query therefore retrieves **what the agent did while it was already at set point**, not **what it did that brought it to set point**. The homeostatic action path (#10) does not work as stated. A fix is to key slots by $Q_\phi(z_t)\oplus b_{t+H}$, written $H$ steps late, which is exactly hindsight relabeling. That still leaves the part existing (UDRL/hindsight relabeling).

## 2. Closest prior work, read in full

### 2.1 Titans (Behrouz et al. 2025), §2–3.1 read

Titans has a memory rewritten at test time by a gated gradient of an associative loss $\lVert\mathcal M(k)-v\rVert^2$, with data-dependent forgetting, and a persistent, data-independent memory. The fast-weights sketch adds three things:
1. **What is stored:** joint self/other/body/text patterns in motor coordinates, instead of token projections. This is a content choice.
2. **A slot-structured memory** (keys, values and strengths, softmax read) instead of an MLP memory. This is closer to Ramsauer or NEC than to Titans.
3. **A gate driven by body change** as well as prediction error. This is a different input to Titans' $\theta_t$; the operation is unchanged.

None of these is a new operation.

### 2.2 Modern Hopfield networks (Ramsauer et al.), §1–2 and A.1.8 read

The sketch's energy and settling are Ramsauer's, with the A.1.8 weighting and an input field. Ramsauer also supplies the theory of the sketch's main failure mode (§4b): "three types of energy minima (fixed points of the update): (1) global fixed point averaging over all patterns, (2) metastable states averaging over a subset of patterns, and (3) fixed points which store a single pattern."

The sketch adds online writes, already present in Ba et al., and goal clamping of part of the query. Clamping part of the state is classical pattern completion with a partial cue, which is what Hopfield networks are for. Here the cue is a desired body state.

### 2.3 Neural Episodic Control (Pritzel et al. 2017) and Upside-Down RL (Srivastava et al. 2019), method sections read

The sketch flagged NEC as unread and guessed that "it stores value estimates, which this mechanism forbids". **That is correct.** In NEC, "The values in the DND … are the Q values corresponding to the state that originally resulted in the corresponding key-value pair." The sketch stores next patterns instead of Q values. NEC's lookup and append-only writes are otherwise the sketch's read and allocation rule.

The "no value" property, together with action from a desired outcome, is exactly UDRL's behavior function, which "neither predicts values nor explicitly maximizes them". UDRL Eq. 3 is even non-parametric: "$N_\kappa(s,d_r,d_h)$ is the number of trajectory segments in $T$ that start in state $s$, have length $d_h$ and total reward $d_r$." The sketch's goal-clamped completion is UDRL with command = body set point and counting replaced by softmax retrieval.

### 2.4 MOSAIC (Wolpert, Doya & Kawato 2003), read in full

MOSAIC already has:
- reading others through one's own modules;
- responsibility-gated learning (#7);
- partner identity as context ("whether it is the identity of a tool or the identity of another person");
- the proposal to "learn a new HMOSAIC for other people".

The sketch's partner-keyed reinstatement is the non-parametric, episodic version of MOSAIC's per-person context selection: retrieval of stored episodes rather than selection of a learned module. That is a real difference in implementation, parametric against episodic, but not a new computation. Episodic kernel retrieval exists (NEC).

**Net: what the sketch does that none of these does.** It is the one system that uses a single episodic Hopfield memory, in own-motor coordinates, both as a listener's face controller and as its partner-reading mechanism, with body set points as completion cues. That is a scope and wiring claim. Every operation exists.

## 3. Reduction attempt

**Rewrite.** The sketch is a Ramsauer modern-Hopfield memory with per-pattern log-strengths and decay (A.1.8.2), settled under an input field (Ba et al.). It is written by a Titans/Schlag delta rule with a three-factor gate on surprise and body change, plus NEC-style append-only allocation. It holds Titans-style persistent, slow and fast partitions with nightly consolidation. Its read-out is UDRL-style command-conditioned retrieval with command = $b^*$. Valence and arousal are read out of the write.

**What is left after the rewrite.** The identification "emotion = the write $\Delta\mathcal M$". That is a definition of which quantity to call affect, a readout, and not a computation the system performs.

**Verdict: recombination.** No new computation. The sketch's own §2 already calls its novelty "the new combination".

## 4. Break attempts on the shared risks

### (a) Collapse into a delayed copy of the partner. Strong break, not answered by the sketch.

The scenario follows the sketch's own rules.
1. **At satiety the face is pure completion from the partner.** When $b=b^*$, $c^*_t=c_t$, so the face is the free completion of $m$ from the observed $p_t$. Over a conversation the body variables are mostly at set point, which is the satiety claim, so most of the time the face is this completion.
2. **The memory then learns its own copying.** The innate memory $\mathcal M^0$ is to hold reflexes, including mimicry ("Mimicry. Completion from $p_t$ also fills $m$"). Every early episode is therefore stored as $(p, m\approx \text{lagged } p)$.
3. **Writes stop where copying works.** Writes are gated by surprise. Human partners also mirror, and L2L measured that the listener's TLCC peak is "≈ 17 frames … ≈ 0.5s". A copying agent's next pattern is therefore *more* predictable, surprise falls, and $\lambda_t$ falls. The copy basin is where writes stop, so it is the absorbing state. The sketch half-states this ("Surprise-gated writes deepen whichever basin is already active … a ruminative attractor").
4. **The lag is fixed by the playback design.** Retrieval refreshes at 10 Hz and plays 1-s trajectories, so the lag is about 0.1–1 s.

The result is the "Delayed Mirror" baseline. A published model has done exactly this: LFI "defaulted to mirroring the speaker, resulting in excessively high synchrony", with expression PCC 0.89 against GT 0.09 (L2L Table 1, their numbers on their data).

**Does the sketch answer it?** No. §6 discusses collapse to *one stored past face* (high $\beta$) or a blur (low $\beta$), not collapse to the *partner*. Its claimed dissociation, "zeroing only the $m$ part of the values removes mimicry but leaves reading the other intact", is an ablation that detects mimicry, not a mechanism that prevents copying.

**Suggested guard.**
- Gate writes on surprise **relative to a copy predictor**: the residual after the delayed-mirror prediction, not the raw $\varepsilon$.
- Report held-out PCC and TLCC against the human range.

### (b) A single hidden dial from flat affect to rigid imitation. Strong break, admitted, with a partial test.

Ramsauer gives the dial its theory. Retrieval error is bounded by $2(N-1)\exp(-\beta(\Delta_i-\dots))M$ (Theorem 5), where $\Delta_i$ is pattern separation. "If no pattern $x_i$ is well separated from the others, then the iteration converges to a global fixed point close to the arithmetic mean of the vectors."

With weak keys (the sketch's admitted risk: keys "may stay close to raw-feature similarity") the separations are small and similar, so the regime is governed by roughly one scalar, $\beta\bar\Delta$:
- low: the global average, which is flat affect;
- high: a single stored pattern, which is rigid replay;
- in between: metastable mixtures.

$\lambda$ and $\gamma$ only move patterns along this axis. **The sketch's answer**, "whether $\mathrm{rank}(\{\Delta\mathcal M_t\})$ over a real session exceeds that of a $\beta$-only ablation", is the right type of test, with two weaknesses:
1. The rank of writes measures what changes in memory, not what changes in behavior. A memory can be rewritten in many directions while the face still moves along one axis.
2. The rank needs a noise floor.

A better test: fit the $\beta$-only model (keys frozen to raw features, only $\beta$ learned) and the full model to listener AUs, then compare held-out log-likelihood and the number of significant canonical components between state and face. The answer is **partial**.

### (c) A lookup table of past faces under scarce data. Strong break, admitted, not answered.

By construction the face is $\sum\alpha_iv_i$, a convex combination of stored trajectories. Learned parameters are "a few thousand" ($Q_\phi,\lambda,\beta$). With few hours of data it is a kernel smoother over the past, which is L2L's "NN motion" baseline with soft weights: "Given an input speaker motion, we find its nearest neighbor from the training set and use its corresponding listener segment as the prediction."

L2L reports that baseline as weak on realism (expression FD 20.66 against 3.55 for L2L) and on synchrony (PCC 0.02 against GT 0.09). L2L also states the motivation against lookup directly: rich listener dynamics are "hard to achieve and generalize using conventional database methods that generate motion via a lookup into a database of ground truth motion".

The sketch names this as its most likely failure. It offers no mechanism against it, only the rank check from (b). **Not answered.**

### A further problem: the first prediction does not isolate the mechanism

Partner-keyed reinstatement (carry-over to the next session with the same partner, beyond an intervening session with someone else) is a claim about **humans**, testable on Seamless if session order is released (the sketch rightly flags this as unchecked). Even if it holds, it does not favor fast weights. Any model given partner identity reproduces it, including MOSAIC's "learn a new HMOSAIC for other people" and a partner-ID-conditioned L2L.

To isolate the mechanism, the engine-side test must give **no partner identity**: reinstatement must come only from content-addressed retrieval keyed by the partner's face and voice. It must be compared against a partner-ID-conditioned baseline of matched size. The sketch's $\lambda=0$ ablation removes all within-deployment learning, which is a weaker contrast.

## 5. Which measured failure of published listener models this might fix (hypothesis only)

Nothing has been measured in this project. These are failures stated in the published papers themselves:
- **No lasting, partner-specific state.** L2L predicts $\hat f^L_t=P(F^S_{1:t},A^S_{1:t},\hat F^L_{1:t-1})$ (its Eq. 1): the speaker's motion and audio plus its own past predicted motion within the sequence. Nothing is carried across sessions, and models are trained per *listener*, not per *dyad*. Its discussion says "modeling the full dyadic cycle of back-and-forth effect remains for future work." Hypothesis: a test-time-written episodic memory gives better next-second listener AU prediction in the first minutes of a session with a **returning** partner than with a new one. A partner-ID-free L2L shows no such difference. This is the one failure this sketch is designed for, and it can be scored on Seamless Interaction's returning dyads if session order is available.
- **Not a plausible fix: delayed-copy collapse or lookup-like output.** These are the sketch's own failure modes (§4a, §4c) and match the LFI and NN-motion failures L2L reports.

Q9 requires a measured failure before development, so this stays a hypothesis until L2L is run as published on Seamless Interaction and the carry-over gap is measured with numbers.
