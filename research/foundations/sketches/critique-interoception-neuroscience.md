# Critique: v2-interoception-neuroscience (Somatic Completion Memory, SCM)

Critic: an independent subagent that did not write the sketch. Written 2026-11-25 under Q8 (critique round) and Q9 (novelty test). Nothing here was run on Seamless Interaction. The two numerical checks below are arithmetic or a few lines of code, not experiments.

**Verdict: recombination.** Every part of the core is an existing mechanism. The closest single framework is **kernel analog forecasting** (Lorenz's method of analogues with a kernel-weighted ensemble), run in closed loop as a soft **motion-matching** controller. Its keys are learned as in **modern Hopfield / attention** retrieval, and its writes are gated by surprise and need change as in **episodic control**. The one detail I could not match to a source is minor and is named in section 3: per-trace playback pointers whose clocks are gated by attention.

## Sources read (primary, by me, for this critique)

| Source | What I read |
|---|---|
| Ramsauer et al., "Hopfield Networks is All You Need", arXiv 2008.02217v3 | Abstract and sections 1–3 in full (energy, update rule, theorems 1–5, metastable states, the equivalence with attention, Hopfield layers). Not the appendix proofs. |
| Zhao & Giannakis, "Analog Forecasting with Dynamics-Adapted Kernels", arXiv 1412.3831v3 | Abstract, section 1, and sections 2.1–2.3 (conventional analog forecasting and basic kernel analog forecasting). Not sections 3–7. |
| Holden et al., "Learned Motion Matching", ACM TOG 2020 (PDF from the author's site) | Abstract, introduction and section 3, "Basic Motion Matching", in full. Not the learned components. |
| Lengyel & Dayan, "Hippocampal Contributions to Control: The Third Way", NIPS 2007 | Main text in full, through section 4 and the start of the discussion. |
| Khandelwal et al., "Generalization through Memorization: Nearest Neighbor Language Models" (kNN-LM), arXiv 1911.00172 | Abstract and section 2 (datastore, retrieval, interpolation). |
| Tu et al., "Modeling Coverage for Neural Machine Translation", arXiv 1601.04811 | Abstract, introduction, section 3.1 (the coverage vector and linguistic coverage). |
| Ng et al., "Learning to Listen", arXiv 2204.08451 (L2L) | Main text in full, plus appendices C and D (person-specific and listener-agnostic results). |
| Anderson et al., "An Integrated Theory of the Mind", Psych. Rev. 2004 | The declarative memory section only (activation, base-level learning, retrieval latency). |
| research/seamless-interaction.md (this project's own data note) | Its "file layout" section. I used it for dataset facts, not the paper itself. |

The sketch itself read Pritzel et al. (neural episodic control) from the abstract only. I did not read it either, so I make no claim about it.

## 1. Parts list (novelty test)

| # | Part of SCM | Existing mechanism | Source and key sentence |
|---|---|---|---|
| 1 | Body $x_t$ updated by Euler steps of fixed reflexes $R$ plus noise $\sigma\xi$ | A stochastic state-space model with a hand-built controller | A standard SDE/ODE; nothing new is claimed for it |
| 2 | $E_\psi$: the other's face mapped into one's own muscle coordinates, later trained so that $E_\psi(\text{render}(x))\approx x$ | Analysis by synthesis (an inverse model trained by self-reconstruction). MOSAIC's first stage of imitation | Wolpert, Doya & Kawato 2003, p. 597: "the visual information of the actor's movement must be converted into a format that can be used as inputs to the system such as the motor system" (read for the companion critique) |
| 3 | Query $q_t=Q_\theta(x,\hat s,c,b-b^*)$ and logits $\beta q^\top k_i$ | Scaled dot-product attention, which is one modern Hopfield update | Ramsauer Eq. (10): "The left part of Eq. (10) is the transformer attention." Their abstract: "The new update rule is equivalent to the attention mechanism used in transformers." |
| 4 | Additive bias $\log w_i$ on the logits | A log prior weight per stored item, as in a weighted mixture or kernel density | A routine softmax bias |
| 5 | $+\gamma u_{t,i}$, with $u$ a low-pass filter of past attention | A coverage vector: the attention history is fed back into attention. Also ACT-R base-level activation (the log of decayed past use) | Tu et al.: "We maintain a coverage vector to keep track of the attention history. The coverage vector is fed to the attention model to help adjust future attention." Anderson et al. 2004: "$B_i=\ln(\sum_j t_j^{-d})$ … reflecting its general usefulness in the past" |
| 6 | $-\rho_{t,i}$, refractory while trace $i$ is consumed | The same coverage mechanism with the opposite sign (penalize what has been attended, to prevent "over-translation"). Habituation | Tu et al.: coverage exists because "some words are unnecessarily translated for multiple times" |
| 7 | Values = continuation velocities $\tau_i[\phi_i{+}1]-\tau_i[\phi_i]$ of the retrieved trajectories | Analog forecasting: find the analog, then follow its recorded future. kNN-LM: retrieve contexts and use what came next | Zhao & Giannakis Eq. (2.5–2.6): "one first identifies the analog … and then evaluates the forecast at lead time $t=k\tau$ via $\hat F_t(y):=f_{i+k}$". kNN-LM: "the key $k_i$ is the vector representation of the context $f(c_i)$ and the value $v_i$ is the target word $w_i$" |
| 8 | A soft mixture over many traces rather than a single nearest one | Kernel analog forecasting | Zhao & Giannakis, abstract: "replace single-analog forecasting with weighted ensembles of analogs constructed using local similarity kernels" |
| 9 | Phase $\phi_i$ advancing one frame per step while trace $i$ is attended | The motion-matching playback pointer; the episodic controller's "follow the stored sequence" | Holden et al. §3: "Each frame we increment the frame variable $i := i+1$ and the pose $y_i$ is looked up in the Animation Database." Lengyel & Dayan: "tries to follow such a sequence whenever it stumbles upon a state included in it" |
| 10 | Pull $\lambda(\tau_i[\phi_i]-x_t)$ toward the attended positions | Relaxation toward the attention readout. If keys equal values, $x \mathrel{+}= \lambda(Xp-x)$ is gradient descent on Ramsauer's energy, because $\nabla_\xi E=\xi-X\,\mathrm{softmax}(\beta X^\top\xi)$ by their Eq. (2)–(3) | Ramsauer Eq. (2): $E=-\mathrm{lse}(\beta,X^\top\xi)+\tfrac12\xi^\top\xi+\dots$ |
| 11 | Objective $J$: mixture-of-Gaussians likelihood of the next $H$ frames under the trace continuations; learn $Q,K,\beta,\dots$ | A kernel/analog forecaster whose similarity metric is learned by maximum likelihood (metric learning for nonparametric regression) | Zhao & Giannakis adapt the kernel to the dynamics by hand (delay coordinates, cone kernels). Learning it by gradient is a routine step. |
| 12 | Write a trace when $-\log p>\eta$; strength $w=|\Delta\lVert b-b^*\rVert|+$ surprise | Salience-gated episodic storage | Lengyel & Dayan: "each time the subject experiences a reward that is considered large enough (larger than expected a priori) it stores the specific sequence of state-action pairs leading up to this reward". SCM replaces signed reward with unsigned need change. |
| 13 | Nightly merge of traces that retrieve each other into prototypes | Clustering; in Hopfield terms, collapsing a metastable set into one stored pattern | Ramsauer: "If some vectors are similar to each other and well separated from all other vectors, then a metastable state near the similar vectors exists." |
| 14 | Valence $=-\sum_i\alpha_i\,\Delta\lVert b-b^*\rVert$ along the retrieved continuations; arousal $=\sum\alpha_i\lVert\dot\tau_i\rVert$ | An episodic Monte Carlo value estimate, with drive reduction as the reward, read out through attention. This is a value readout in Q9's sense | The sketch says "SCM stores no value anywhere". That is true of storage, but valence *computes* an attention-weighted return over stored episodes on the fly. |
| 15 | Reading others: the same keys queried with $Q(\hat s,\hat s,c,0)$ | MOSAIC action observation: run one's own modules on the other's data | Wolpert et al. 2003, p. 597: "the observer uses his own multiple modules to try to simulate the observed percept" |
| 16 | Reply delay = settling time of iterated retrieval | Retrieval latency as a function of activation or separation | Anderson et al.: "$T_i=Fe^{-A_i}$ (latency of retrieval equation)". Ramsauer Thm. 4: well-separated patterns are retrieved "with one update", while metastable mixtures are not |
| 17 | "Articulatory try-on": pick the Claude draft with the highest $\mathrm{lse}_i(\beta Q(y)^\top k_i+\log w_i)$ | Rerank candidates by a density or energy score. This is minus the first term of Ramsauer's energy (Eq. 2) | — |
| 18 | Recall = transcripts of the top-$\alpha$ episodes | Retrieval-augmented prompting with a state-conditioned query | kNN-LM section 2 is the language-model analogue |

## 2. Closest prior work, read in primary sources

**(a) Kernel analog forecasting (dynamical systems). Zhao & Giannakis 2016, building on Lorenz 1969; sections 1–2.3 read.**
- **What it does.** It stores a historical record. It weights past states by a kernel similarity to the current initial data, normalized so the weights sum to one (their Eq. 2.10). It then forecasts by averaging the *time-shifted* observable over those analogs: "$\hat F(y)=\frac1N\sum_i\hat\rho(y,x_i)f_i$", with $f_i$ advanced by the Koopman shift "$U_tf(a_i)=f_{i+k}$".
- **This is SCM's dynamical equation.** In SCM, $\alpha_{t,i}$ is the normalized kernel. "Continuation velocity" is the time-shifted observable. "Trace phase" is the shift index.
- **What SCM adds.**
  1. The forecast is fed back as the system's own next state, so the forecaster becomes a generator.
  2. The kernel is a learned dot product, not a hand-built one.
  3. The record is written online, gated by surprise.
- **What it does not add.** The authors already warn about SCM's main risk: "nonparametric models must compensate for their flexible structure through plentiful samples in phase space", and single analogs suffer "high risk of overfitting the training data."

**(b) Motion matching (graphics). Holden et al. 2020, section 3 read.**
- **What it does.** It stores feature and pose databases, searches them for the nearest feature vector every N frames, and plays the found clip forward frame by frame, with inertialization blending at transitions.
- **SCM is a soft, multi-pointer motion matching.** Many clips play at once, weighted by $\alpha$, instead of one clip chosen by argmin.
- **The sketch's claimed differences are about the data and the key.** The data are "the agent's own life", and the key is need plus the other's face. Q9 excludes both: "whatever the key space, the time scales or the naming". Soft blending of analogs is already the move from Lorenz analogs to kernel analogs in (a).

**(c) Modern Hopfield networks / attention (ML). Ramsauer et al. 2020, sections 1–3 read.**
- **The sketch's stated difference does not hold.** It says Hopfield networks "retrieve static patterns", while SCM retrieves "trajectories whose velocities drive a continuous body." But Ramsauer's Eq. (10) separates keys from values, $V=Y W_K W_V$, so the retrieved value can be any vector, including a continuation segment.
- **kNN-LM shows the same idea in language.** Its keys are past contexts and its values are what followed them.
- **What SCM adds.** Only the choice of values (one's own body continuations) and of keys (need and the other's face in self coordinates). Both are key-space choices.
- **The fixed-point analysis applies to SCM unchanged.** It is the basis of the break in section 4b.

**(d) Episodic control (neuroscience). Lengyel & Dayan 2007, main text read.**
- **What it does.** It stores whole sequences when reward exceeds expectation, then replays a stored sequence when a state recurs. Episodic control "outperforms noisy model-based control in the low data limit". The authors also show "the asymptotic performance of the episodic controller is rather poor, and is barely improved by extra learning."
- **What SCM adds.**
  1. Storage is triggered by unsigned need change and surprise, not signed reward.
  2. Recall is a soft mixture, not a single sequence.
  3. The stored and replayed object is the body trajectory itself rather than an action sequence leading to reward.
- **That last difference is SCM's real conceptual move:** expression is replay of one's own lived bodies. It is a change in *what is stored*, not a new computation.

## 3. Reduction attempt

**SCM, written as existing frameworks plus additions:**
> Closed-loop kernel analog forecasting (Lorenz/Zhao–Giannakis) over a library of one's own 2-second body windows. The kernel is a learned dot-product attention (Ramsauer Eq. 10) with a log-prior per trace and a positive-and-negative coverage term (Tu et al.; ACT-R base level). Writes are gated by surprise and unsigned need change (Lengyel & Dayan's episodic controller). Prototypes are made by nightly clustering. Valence is an attention-weighted episodic return. Reading others queries the same memory with the other's face mapped into one's own body (MOSAIC observation). Claude's drafts are reranked by the Hopfield energy.

Nothing is left over except one scheduling detail. **Each trace has its own playback pointer, which advances only while the trace's attention weight exceeds $\epsilon$ and resets otherwise.**
- Kernel analog forecasting advances all analogs together from the query time.
- Motion matching advances a single pointer.
- I found no source in my reading with attention-gated pointers per item.
- This is a rule about when indices increment, not a new computation. It is also fragile: see the phase-reset break in 4b.

**Verdict: recombination.** The sketch's novelty sentence ("mimicry, mood, recall and empathy are all reactivation of the agent's own lived body trajectories, keyed by need and by the other's body") names what is stored and how it is keyed. Under Q9, that does not count.

## 4. Break attempts on the shared risks

### (a) Collapse into a delayed (or anticipatory) copy of the partner

**Scenario 1: satiation removes the only term that separates self from other.**
- Self-retrieval uses $Q(x,\hat s,c,b-b^*)$ and other-retrieval uses $Q(\hat s,\hat s,c,0)$.
- At satiation, $b=b^*$, which Principle 6 makes the normal resting condition, so the need slot is zero in both queries.
- Once the body has mimicked for a moment, $x\approx\hat s$ (the reflex in $R$ does this even with an empty memory). Then the two queries are identical and $\alpha=\alpha^{\text{other}}$.
- The body then completes exactly the traces it uses to *forecast the partner*. The agent's face plays out its prediction of the partner's next face.
- That is a copy, shifted forward by the forecast. The sketch calls it "anticipating the partner", but it is still mirroring. L2L measured where pure mirroring lands: Mirror and Delayed Mirror have PCC 1.00 and 0.98 against a human ground truth of 0.09, and the authors describe them as looking "uncanny due to excessive variation and synchrony" (L2L Table 1 and section 5.2).
- Nothing in SCM restores the difference between $x$ and $\hat s$ once they meet. Only $c_t$ (the shared conversation context) and noise remain, and the shared context enters both queries the same way.

**Scenario 2: the objective rewards discovering the copy.**
- $J$ maximizes prediction of the agent's own future.
- Early in life, the agent's own future is driven by $R$, which includes a mimicry gain (the sketch says: "With an empty memory, only the small reflex gain in R remains").
- So the most predictive feature of $x_{t+1:t+H}$ is $\hat s_{t-d}$, and gradient ascent on $J$ teaches $Q$ to weight $\hat s$.
- Traces written in this period contain "partner did X, I did X about 0.5 s later". Retrieving them adds that copy to the body, and the cycle continues.
- The surprise gate slows this, because well-predicted copying stops triggering writes. It does not remove the copy basin, and nothing in $J$ penalizes it.

**Does the sketch answer this?** No.
- Section 4 asserts that mimicry is "idiosyncratic and can anticipate the partner".
- Section 5 tests "completion beats lagged copy" on *human* listeners. Humans are not copiers (L2L's ground-truth PCC is 0.09), so the test cannot detect the agent's own collapse.

### (b) A single hidden dial from flat affect to rigid imitation

**The dial is the entropy of $\alpha$.** It is set jointly by $\beta$, by the separation of the keys, and by the self-reinforcing occupancy gain $\gamma$.

- **Flat end.** Ramsauer: "If no pattern $x_i$ is well separated from the others, then the iteration converges to a global fixed point close to the arithmetic mean of the vectors. In this case the softmax vector $p$ is close to uniform."
  - The face then follows the mean continuation velocity of many traces at unrelated phases, which is near zero. The pull term drags the face to the mean posture.
  - L2L measured this end as the Median baseline: variation 0.00, FD 64.48 against 3.55 for their model.
- **Rigid end.** A few traces dominate, and the face replays them. L2L measured this end as the NN-motion baseline: FD 20.66, and 75.3% of raters preferred the learned model over it.

**The occupancy term makes the dial bistable, and its threshold moves with memory size.**
- Take $N$ equally matching traces, and the map from $u$ to $\mathrm{softmax}(\gamma u+\dots)$ at the uniform point.
- Its Jacobian is $\gamma(\mathrm{diag}\,\alpha-\alpha\alpha^\top)$, with eigenvalue $\gamma/N$ on directions that sum to zero.
- So lock-in (perseveration) begins when $\gamma>N_{\text{eff}}$, the number of effectively competing traces.
- With scarce memory ($N_{\text{eff}}$ small), a small $\gamma$ already locks onto one trace, which is rigid. As memory grows, the same $\gamma$ falls below threshold, and the mixture flattens.
- **The regime therefore drifts from rigid to flat as the agent lives, with no parameter changed.**
- Ramsauer's Theorems 4 and 5 add that the separation enters only as the product $\beta\Delta_i$ (error "exponentially small in the separation $\Delta_i$"). So $\beta$ and the data density act on a single axis.

**The phase-reset rule breaks the "completion" at the flat end.**
- A phase advances only while $\alpha_i>\epsilon$. With $10^4$–$10^5$ traces (the sketch's own figure) and near-uniform attention, $\alpha_i\approx10^{-4}$–$10^{-5}$.
- If $\epsilon$ is above that, every phase resets every frame, and the body only ever sees *onset* velocities. Nothing is completed.
- If $\epsilon$ is set below that, every trace advances together, and the per-trace phase means nothing.

**Does the sketch answer this?** Partly. Section 6 names the $\beta$ trade-off honestly ("bland mean … perseverative attractor … jukebox"). It offers $\rho$ and $u$ as possible remedies and admits they may not work.
- My analysis says $u$ makes the problem *worse* (positive feedback with a threshold that depends on $N$).
- $\rho$ turns lock-in into slow switching between tracks rather than removing it.

### (c) A lookup table of past faces under scarce data

**SCM is a lookup table by construction.** The question is only whether soft blending makes it generalize. Four points say it does not.

1. **Its proposed first test is L2L's lookup baseline.**
   - Section 5 proposes "the listener's own earlier responses, retrieved by matching the partner's onset".
   - L2L's NN-motion baseline is exactly this: "Given an input speaker motion, we find its nearest neighbor from the training set and use its corresponding listener segment as the prediction". It is trained per listener.
   - The listener-agnostic NN is the "population retrieval" control.
   - L2L Appendix D already reports the ordering on their data: person-specific NN FD 20.66 against listener-agnostic NN FD 57.29.
   - So "own beats population" is predicted by *any* person-specific model and has already been observed. It is not a distinctive prediction of SCM.
2. **L2L found short-window soft lookup worse.** "We found NN on the full 64-frame sequence to work better than NN on smaller subsequences that are then interpolated together." SCM re-queries every frame with 2-second traces and soft blending, which is the variant L2L found worse.
3. **Nightly merging turns the memory into a codebook.** After prototypes replace traces, SCM's memory is a set of motion-segment prototypes selected by attention from partner features. That is L2L's VQ codebook ($K=200$ segment codes) without L2L's transformer predictor.
4. **Data scale.**
   - This project's data note (research/seamless-interaction.md) estimates a median of 56 AU-minutes per V00 participant, which is about 100,000 frames.
   - That is at most about 1,700 non-overlapping 2-second windows before the surprise gate thins them, in 24 dimensions.
   - Kernel analog forecasting needs "plentiful samples in phase space". At this density, nearest-neighbour distances in 24 dimensions are poorly separated. That pushes SCM to one of the two measured ends: NN-like or Median-like.

**Does the sketch answer this?** It acknowledges a weak cold start (sections 3 and 6). It does not answer the lookup-table objection: merging is its only generalization step, and merging lands on a codebook.

### Factual problems in the sketch's test (section 5)

- **"46 FACS action units".** Seamless's `FAUValue` has 24 AU columns, per the project's data note (README plus one inspected file). The column order is unverified.
- **"Naturalistic participants in up to 10 sessions", and the same-partner contrast.**
  - The data note says naturalistic participants meet up to 10 *different* partners, and "V00 naturalistic pairs never repeat".
  - Repeat pairs exist as 195 improvised *actor* pairs in V00, and 7 pairs in V02.
  - So the "same partner, grows with sessions" sub-prediction is testable only on scripted actor pairs.
  - Session order is not released, so "grows with the number of sessions" cannot be ordered either.
- **Familiar and stranger counts.** The sketch gives 1,752 familiar and 1,611 stranger. The data note counts 1,751 familiar and 3,347 stranger sessions in `relationships.csv`. The sketch's figures may come from the paper. The analysis should use the CSV.

## 5. Which measured failure of published listener models SCM might fix (hypothesis only)

The measured failures I read are all in L2L (Table 1 and Appendix D).

- **The data cost of person-specific listeners.** This is the most plausible fit.
  - L2L trains one model per listener. It excluded two listeners because "we did not have enough data to learn a person-specific model". That failure is qualitative, with no number.
  - Their own model degrades from FD 3.55 (person-specific) to 30.01 (listener-agnostic). The two setups differ, so this is not a clean contrast.
  - SCM's single-exposure, per-person memory is a plausible way to personalize from little data. But point 4c shows a per-person lookup is also what fails, so the hypothesis must be tested against L2L's person-specific NN baseline, not only against copying.
- **Lookup asynchrony.**
  - NN motion has PCC 0.02 against a ground truth of 0.09. Re-querying every frame with completion could plausibly improve synchrony over a lookup of whole 64-frame segments.
  - Evidence against: L2L's own note that sub-sequence NN did worse.
  - Caution: L2L's Figure 4 caption says "NN produces sequences that are too synchronous with the speaker", which conflicts with its Table 1 PCC of 0.02. Recompute before relying on either.
- **Not a measured failure: carry-over across turns or sessions.** L2L conditions on a 64-frame window (about 2.1 s at 30 fps) and feeds "zeros for timesteps without prior listener predictions". It reports nothing about carry-over. SCM's slow occupancy $u$ would target that gap, but Q9 requires the gap to be measured first, by running L2L on Seamless.
