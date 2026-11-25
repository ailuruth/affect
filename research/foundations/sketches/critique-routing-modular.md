# Critique: v2-routing-modular (Shared-Charge Routing, SCR)

Critic: an independent subagent that did not write the sketch. Written 2026-11-25 under Q8 (critique round) and Q9 (novelty test). Nothing here was run on Seamless Interaction. The bistability check in section 4b is a 20-line iteration of the sketch's own equations, not an experiment.

**Verdict: recombination.** SCR is **MOSAIC** (own predictor–controller modules, responsibilities from prediction error, run on the observed other, with the observed responsibilities biasing one's own module selection) plus **COIN** (a growing repertoire of modules, a nonparametric prior with a novel-module option, learning gated by responsibility). Its routing prior is a **sequential distance-dependent CRP with exponential decay** (equivalently, ACT-R base-level activation with exponential decay), with one twist: the usage events of the self and other slots are pooled into one shared prior. The selection uses **noisy top-k mixture-of-experts gating**, and the need term is a **value bias**. Two details have no exact match in my reading: a separate decay constant per module, and slot weights $\omega_j$ on the pooled counts. Both are parameterizations of the prior, not new computations.

## Sources read (primary, by me, for this critique)

| Source | What I read |
|---|---|
| Wolpert, Doya & Kawato, "A unifying computational framework for motor control and social interaction", Phil. Trans. R. Soc. B 358 (2003), PDF from the Kawato lab site | Sections 1–6, pp. 593–599, in full (the social loop, MOSAIC, action observation and imitation, start of HMOSAIC). Not pp. 600–602. |
| Heald, Lengyel & Wolpert, "Contextual inference underlies the learning of sensorimotor repertoires", bioRxiv 2020.11.23.394320 (preprint of the 2021 Nature paper) | Abstract, the main-text model description and the spontaneous-recovery section opening, and the Methods "Generative model" (Eqs. 2–9). Not the inference (particle filter) details, the experiments' full methods, or the supplement. |
| Blei & Frazier, "Distance Dependent Chinese Restaurant Processes", arXiv 0910.1022 | Section 1 and the definitions of section 2 (Eq. 2, decay functions, sequential CRPs, marginal invariance). Not the inference or experiments. |
| Anderson et al., "An Integrated Theory of the Mind", Psych. Rev. 2004 | The declarative memory section only. |
| Shazeer et al., "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer", arXiv 1701.06538 | Section 2.1 (gating) and the importance-loss paragraph. |
| Goyal et al., "Neural Production Systems", arXiv 2103.01937 | Section 1 and the rule-selection steps of the method. |
| Goyal et al., "Recurrent Independent Mechanisms", arXiv 1909.10893 | Abstract and the input-attention competition section only. |
| Tu et al., "Modeling Coverage for Neural Machine Translation", arXiv 1601.04811 | Abstract, introduction, section 3.1. |
| Ng et al., "Learning to Listen", arXiv 2204.08451 (L2L) | Main text in full, plus appendices C and D. |
| research/seamless-interaction.md (this project's data note) | Its "file layout" section. |

I could not get the full text of Zhu, Ghahramani & Lafferty 2005 ("Time-sensitive Dirichlet process mixture models"). The DTIC and CMU copies returned 403. I cite it only through Blei & Frazier's statement that it is a special case of the ddCRP. I did not read Teh et al. 2006 (the hierarchical Dirichlet process). The sketch flags the same gap, and I rely on COIN's own HDP statement instead.

## 1. Parts list (novelty test)

| # | Part of SCR | Existing mechanism | Source and key sentence |
|---|---|---|---|
| 1 | Slots (self, other, episodic), each with a GRU state, weights shared across slots | Slot or object-file architectures with interchangeable slots, plus a recurrent network | NPS §1: slots are "also known as object files … Importantly, the slots are interchangeable" |
| 2 | Modules $m_k=(\kappa_k,p_k,u_k,\widehat{\Delta n}_k,\tau_k)$: a forward model paired with a motor primitive | MOSAIC predictor–controller pairs | Wolpert et al., p. 596: "each predictor is paired with a corresponding controller forming a predictor–controller pair" |
| 3 | Content logit $(W_q[z;e])^\top\kappa_k/\sqrt d$ | Softmax gating of experts, and query–key rule selection | Shazeer Eq. (2): "$G_\sigma(x)=\mathrm{Softmax}(x\cdot W_g)$" (after Jordan & Jacobs). NPS: rules are chosen by "$r=\arg\max_i(q_pk_i+\gamma)$" with keys from the rules |
| 4 | Fit term $-\lambda\,\ell_k(x_{j,t-w:t})$ | MOSAIC responsibilities | Wolpert et al., p. 596: "the sensory prediction error from a given forward model is represented as a probability; if the error is small then the probability that the forward model is appropriate is high" |
| 5 | Charge $\tau_k\dot c_k=-c_k+\sum_j\omega_jR_{jk}$ entering the logit as $\alpha\log(\epsilon+c_k)$ | A recency-weighted usage prior. At $\alpha=1$, $\exp(\log(\epsilon+c_k))=\epsilon+c_k$ is the sequential ddCRP prior with exponential decay: the probability of joining module $k$ is proportional to the decayed sum of past assignments to it. It is also ACT-R base-level activation (the log of decayed use), and the coverage vector of NMT | Blei & Frazier: "The exponential decay $f(d)=e^{-d/a}$ decays the probability of linking to an earlier customer exponentially with the distance to the current customer". Anderson et al.: "$B_i=\ln(\sum_j t_j^{-d})$ … reflecting its general usefulness in the past". Tu et al.: "maintain a coverage vector to keep track of the attention history" |
| 6 | The charge is **shared across slots** (self, other, memory) | Pooling all groups' assignments into one prior. In COIN the transition rows share a global weight vector: "contexts that are more common in general will be transitioned to more frequently from all contexts". In MOSAIC, observation biases one's own selection | COIN Methods, after Eq. 7. Wolpert et al., p. 598: the observed module sequence can "either replace the observer's usual sequence of module activation or be used to bias it" |
| 7 | A separate $\tau_k$ per module, initialized log-uniform from 0.1 s to 6 h | **No exact match in my reading.** The ddCRP has one decay function, and ACT-R one $d$. COIN gives each context its own retention $a^{(j)}$, but on that context's *state*, not on its usage prior. A spread of exponential decays approximates ACT-R's power-law decay | A parameterization, not a computation |
| 8 | Slot weights $\omega_j$ ($\omega_\text{self}=1$, $\omega_\text{other}<1$) | Weighted customers or counts | A parameterization |
| 9 | Need term $\gamma\langle -n,\widehat{\Delta n}_k\rangle$ | An expected-drive-reduction value bias on selection. A "value readout" in Q9's sense | — |
| 10 | $\mathrm{top}_S$, then renormalize | Noisy top-k gating | Shazeer Eq. (3)–(5): "keep only the top k values, setting the rest to $-\infty$" |
| 11 | Output $a=\sum_kR_{\text{self},k}u_k$ | A responsibility-weighted mix of controllers | Wolpert et al., Fig. 2 caption: "The outputs of the controllers are weighted by the likelihood that each is appropriate, to determine the final motor command" |
| 12 | Mixture-NLL objective with EM-style, responsibility-weighted learning | MOSAIC and COIN learning gated by responsibility | Wolpert et al.: "the responsibilities are used to gate the learning of the predictors and controllers". COIN: "each memory is updated according to the probability of the corresponding context under the posterior" |
| 13 | Spawn a module when nothing fits better than a threshold; a description-length penalty $\beta K$ | A nonparametric repertoire with a novel-component option | COIN: "A new memory is created whenever the probability of a novel context becomes high." ddCRP/CRP: a new table with weight $\alpha$ |
| 14 | Reading others: route the other's stream through one's own modules | MOSAIC action observation | Wolpert et al., pp. 597–598: "the observer uses his own multiple modules to try to simulate the observed percept … the identities of the modules which best account for the percept form a symbolic code of the hidden state of the actor" |
| 15 | Valence $=\sum_kc_k\langle -n,\widehat{\Delta n}_k\rangle$; arousal $=\sum_kc_k/\tau_k$ | Linear readouts of the usage state; valence is a value readout | — |
| 16 | Memory items stamped with $c$, retrieved by $\mathrm{sim}(c_t,c_\text{item})$ | Attention with the charge vector as key (mood-congruent retrieval) | Ramsauer Eq. (10) (read for the companion critique) |
| 17 | Replay: merge, split and freeze modules | Split–merge of mixture components; freezing for continual learning | — |
| 18 | Routing load sets the thinking budget and delay | Retrieval latency from activation | Anderson et al.: "$T_i=Fe^{-A_i}$" |

## 2. Closest prior work, read in primary sources

**(a) MOSAIC. Wolpert, Doya & Kawato 2003, pp. 593–599 read.** The sketch read the same pages. Its three claimed differences, checked against the text:

1. **"Nothing persists across self and other."** Half right.
   - MOSAIC explicitly lets the observed module sequence act on one's own selection: "This information can either replace the observer's usual sequence of module activation or be used to bias it towards a better action."
   - What MOSAIC does not have is a bias that decays continuously and automatically, with a time constant per module. That is a decay kernel on usage, and the ddCRP and ACT-R already have one (see c).
2. **"MOSAIC's priors come from context; here content and needs."** A gate conditioned on content is ordinary MoE gating (Shazeer Eq. 2). Needs enter as one more additive bias, which is a value term.
3. **"Fixed module set; here the library grows."** COIN, MOSAIC's direct successor, already grows a repertoire (see b).

**(b) COIN. Heald, Lengyel & Wolpert 2020/2021; model description and generative model read.**
- **What it does.** It holds a repertoire of context-specific memories. A sticky HDP prior is placed on context transitions, with global weights shared across rows. Contexts are inferred from feedback and cues. "A new memory is created whenever the probability of a novel context becomes high." The motor output expresses each memory "commensurate with the probability of the corresponding context". Learning is weighted by responsibility.
- **COIN already derives SCR's main behavioural claim, carry-over.** "Spontaneous recovery arises in the COIN model due to the dynamics of contextual inference." Slow drifts of the inferred context probabilities, not the memories themselves, produce lasting after-effects. SCR's "coalition-specific carry-over" is the same idea, with the inference replaced by a leaky usage count.
- **What SCR does that COIN does not.**
  1. COIN models one agent. It has no other slot and no pooling of the other's assignments into one's own prior.
  2. SCR's prior decays per module.
  3. SCR uses a forward-pass gate instead of Bayesian inference.
- **What SCR loses.** COIN's novel-context probability is part of the inference. SCR's spawn rule is a fixed threshold outside the objective, and section 4c shows why that matters.

**(c) Sequential ddCRP with exponential decay. Blei & Frazier, sections 1–2 read.**
- **What it does.** Eq. (2): "$p(c_i=j\mid D,\alpha)\propto f(d_{ij})$ if $j\neq i$; $\alpha$ if $i=j$". With sequential distances and $f(d)=e^{-d/a}$, the probability of joining table $k$ is proportional to $\sum_{j\in k}e^{-(t-t_j)/a}$. That is exactly a leaky integrator of past assignments, which is SCR's $c_k$ with $\tau=a$.
- **SCR's routing is a posterior under this prior.** Its logit adds $\log$ prior ($\log(\epsilon+c_k)$) to a log-likelihood ($-\lambda\ell_k$) and to gate terms. So $R_{jk}$ is a posterior assignment under a ddCRP-style prior, multiplied by a content gate and a need bias.
- **The modelling choice SCR makes.** The "customers" are routing events from every slot, weighted by $\omega_j$, sitting in one restaurant.
- **Blei & Frazier already motivate shared influence with social contagion.** On why one might drop marginal invariance: "consider the goal of modeling preferences of people within a social network … A similar example is modeling the spread of disease." Their intended use is a prior over *data partitions*, not over one's own motor modules. Still, the computation, influence passed through shared, decaying cluster counts, is the same.

**(d) ACT-R declarative memory. Anderson et al. 2004, declarative memory section read.**
- **What it does.** Activation is "a sum of a base-level activation, reflecting its general usefulness in the past, and an associative activation, reflecting its relevance to the current context". The base level is $\ln\sum_jt_j^{-d}$, and retrieval latency is $Fe^{-A_i}$.
- **The mapping to SCR's logit.** $\alpha\log(\epsilon+c_k)$ is a base level with exponential decay. The content term is associative activation. Using load to set the reply delay is ACT-R's latency equation.
- **The pooling.** In ACT-R, every "practice" of a chunk raises its base level, whoever the retrieval was for. Pooling the self and other slots is therefore ACT-R's default, not an extension.

## 3. Reduction attempt

**SCR, written as existing frameworks plus additions:**
> MOSAIC predictor–controller modules, with responsibilities from prediction error, run on both one's own and the other's streams (Wolpert et al. 2003). They are grown and learned as in COIN, with responsibility-gated updates and a novel-module option. Selection is a top-k softmax gate (Shazeer) whose logit is: content (MoE gating) + log-likelihood (MOSAIC) + a log recency-of-use prior (a sequential exponential-decay ddCRP, or ACT-R base level) pooled over the self and other slots + a value bias toward drive reduction. Valence, arousal and mood-congruent recall are readouts of, or attention over, the prior's count vector.

**What is left over:**
1. **A different decay constant for each module's usage count.** I found no source in my reading with per-component decay of a usage prior. It is one parameter per module, not a new computation. A log-uniform spread of exponential decays mostly reproduces ACT-R's power law.
2. **Fractional slot weights on the pooled counts.** These are weighted customers.

**Verdict: recombination.** The sketch's novelty sentence, "a cross-slot charge field over a shared expert library … whose sharing across self and other is the contagion", describes *which data share the prior*. Under Q9, that is a choice of data and key space, not a computation.

## 4. Break attempts on the shared risks

### (b) A single hidden dial from flat affect to rigid imitation

This break is the clearest of the three, so it comes first.

**Setup.** Take two modules, the self slot only, no content term, and the steady state of the charge ($c_k=R_{\text{self},k}$, since $\omega_\text{self}=1$). Write $x=R_{\text{self},1}$. The charge feedback is then the one-dimensional map

$$x\ \mapsto\ \sigma\big(\alpha[\log(\epsilon+x)-\log(\epsilon+1-x)]+h\big),$$

where $h$ is any other input to the logit difference, such as the partner's share of the charge, content or need.

**Threshold.** At $x=\tfrac12$, $h=0$, the slope is $\tfrac14\cdot\alpha\cdot\frac{2}{\epsilon+1/2}=\frac{\alpha}{1+2\epsilon}$. The symmetric state therefore becomes unstable, and two locked states appear (a pitchfork), at
$$\alpha_c=1+2\epsilon.$$

**Numerical check** of the sketch's own equations: 20,000 iterations from five starting points.

| $\epsilon$ | $\alpha$ just below $\alpha_c$ | $\alpha$ just above $\alpha_c$ | $\alpha=3$ |
|---|---|---|---|
| 0.01 | one state, 0.5 | 0.04 / 0.96 | 0.0 / 1.0 |
| 0.1 | one state, 0.5 | 0.22 / 0.78 | 0.001 / 0.999 |
| 0.5 | one state, 0.5 | 0.35 / 0.65 | 0.05 / 0.95 |

**Effect of a partner bias.** Add a bias $h=0.5$ standing for the partner.
- Below $\alpha_c$, the self's routing shifts smoothly toward the partner's module (0.71–0.98, depending on $\epsilon$ and $\alpha$). This is graded contagion.
- At $\epsilon=0.01$ and $\alpha=1.5$, both locked states survive the bias. Whichever module was locked first stays locked against the partner. This is hysteresis: rigid perseveration, and if the partner set the lock, rigid imitation.

**So $\alpha$ (with $\epsilon$) is one dial.**
- **Low $\alpha$:** the charge barely matters, routing is a broad mixture, and $a=\sum R\,u_k$ averages motor primitives. This is the flat end.
- **Above $\alpha_c$:** winner-take-all lock-in that the partner can only flip with a large push. This is the rigid end.
- **Just below $\alpha_c$:** high gain to the partner's charge, which is the delayed-copy regime (4a).

**The time constants do not help.** The steady-state charge $c^*=\sum_j\omega_jR_{jk}$ does not depend on $\tau_k$. The time constants change only *how fast* a module locks or fades, not *whether* it does. Making $\alpha$ per-module or learned does not remove the threshold either: each module then has its own $\alpha_c$.

**Does the sketch answer this?** No. Section 3 lists "$\alpha,\gamma,\omega$ are hyperparameters whose values the core does not fix" as an open risk. It does not notice that $\alpha$ has a bifurcation at $1+2\epsilon$.

### (a) Collapse into a delayed copy of the partner

**The mimicry path is a delayed copy by construction.**
- The other slot routes to module $k$ by fit to the partner's stream, in own-AU coordinates.
- $c_k$ rises with time constant $\tau_k$, which raises $k$'s logit for the self slot, so the self emits $u_k$.
- For the innate fast modules ($\tau\approx0.1$ s), this is a low-passed copy of the partner in module space, delayed by about $\tau_k$.
- The sketch's own ablation (private charge, so that "mimicry and contagion vanish") confirms that this path carries all of the mimicry.

**What stops the copy:** the self slot's content term (its own $z$ and $e$) and the need term. Both fail in common conditions:
1. **At satiation ($n=0$), the need term is zero by design** (Principle 6). Satiation is the normal resting state, so whenever the agent is content, one of its two self-specific inputs disappears.
2. **With scarce data, the content router is the part most likely to collapse.** The sketch admits this: "the weak point is that a router can collapse when data are scarce". A collapsed content term gives the same logit for the self and other slots.
3. **Once the self mimics, the two slots' streams converge**, so $z_\text{self}\approx z_\text{other}$ (the GRU weights are shared). That makes the content terms equal as well.

At that point $R_{\text{self},\cdot}=R_{\text{other},\cdot}$ up to the charge feedback, which is the copier's fixed point. L2L measured where a learned listener model ends up when it falls into this: LFI, re-trained on their data, "defaulted to mirroring the speaker, resulting in excessively high synchrony", with PCC 0.89 against a human ground truth of 0.09 (L2L Table 1).

**Does the sketch answer this?** No. It presents mimicry as a success ("Mimicry: the other's slot charges module k …"). It has no term that penalizes or limits copying. Section 6 names a different failure (modules carving along articulation).

### (c) A lookup table of past faces under scarce data

**The spawn rule turns the library into a lookup table.**
- A module is spawned whenever "no existing module fits a slot's stream better than a fixed novelty threshold".
- Seamless `FAUValue` streams are noisy. The data note found columns 12 and 19 byte-identical and an implausible mean of 1.28 for `EyesClosed`.
- With a threshold set tight enough to separate affective windows, most novel windows spawn a module. Each such module's $u_k$ and $p_k$ are then fitted to essentially one episode. Rarely routed modules are "frozen", which preserves them as exemplars.
- The result is a table of past windows indexed by key, which is L2L's NN-motion baseline: FD 20.66 against 3.55 for the learned model, with 75.3% of raters preferring the learned model.

**The guard is outside the objective.** The description-length penalty $\beta K$ should prevent this, but it sits in the objective while the spawn decision is a separate fixed threshold. So library size is set by a second dial (the threshold, played against $\beta$), not derived from the objective. COIN avoids this by making the novel-module probability part of the inference.

**Does the sketch answer this?** Partly. It claims small modules and sparse routing protect against forgetting (section 3). That protection is the same mechanism that preserves one-episode exemplars. It does not discuss library growth under its fixed threshold.

### Problems in the sketch's test (section 5)

- **"AUs extracted by OpenFace or Py-Feat."** That requires downloading video. Seamless already ships 24-AU `FAUValue` features for V00 and most of V02 (data note), so no video download is needed. With the disk below its floor (Q11), the video route is the wrong one.
- **The discriminating control is a 2-D charge or $K=1$.** That is sound. But the 10–30 s gain can also come from any slow shared latent (topic, turn-taking, a shared arousal level). The sketch names this confound but proposes only to "control for topic and turn", without saying how topic is measured. The transcripts would have to be embedded for that, and an embedding is not a label, so it is allowed.
- **Interaction length.** Naturalistic interactions average about 208 s (data note). Lags of 10–30 s therefore leave few independent windows per interaction. Pool across interactions only with partner-level resampling.

## 5. Which measured failure of published listener models SCR might fix (hypothesis only)

- **No lasting state.** This is SCR's natural target, but it is *not yet measured*.
  - L2L predicts from a 64-frame window (about 2.1 s at 30 fps) and, at test time, feeds "zeros for timesteps without prior listener predictions".
  - It reports nothing about carry-over beyond the window.
  - SCR's long-$\tau$ charge targets this gap. Under Q9, the gap must first be measured by running L2L as published on Seamless with SCR's own lagged analysis (partner state at $t$ against listener at $t+10$–$30$ s, beyond a ±5 s window).
- **Copy collapse.** Measured: LFI's PCC is 0.89 against a ground truth of 0.09. SCR is more likely to *reproduce* this failure than to fix it (see 4a and 4b), unless $\alpha$ is held below $1+2\epsilon$ and the content term is kept separate for the self and other slots.
- **Flat output.** Measured: L2L's Median baseline has variation 0.00 and FD 64.48. SCR below threshold, with a collapsed router, is a mixture of motor primitives and would plausibly land near Median. This is a risk, not a fix.
