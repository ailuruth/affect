# Critique: v2-developmental-dyad ("the dyadic contingency kernel")

Independent critic, 2026-11-25, written under questions.md Q8 (critique round) and Q9 (novelty test). I did not write the sketch. Nothing was downloaded except paper text; no data and no weights.

**Verdict: recombination.** Every computational part is an existing mechanism. The most distinctive element, the markedness-gated binding loss, is a new *training signal* taken from Gergely and Watson's verbal theory. It is not a new computation. The operator already reached the same verdict on the D69 version of this line in Q9 ("Contingency operators ... are existing mathematics"). This critique confirms that verdict at the level of each part.

## Sources and how they were read

| Source | How read |
|---|---|
| Yang, Kautz & Hatamizadeh 2024, "Gated Delta Networks: Improving Mamba2 with Delta Rule", arXiv 2412.06464v3 | HTML full text via a fetch tool, characters 0–100k of 118k (§2.2 and §3.1 covered; the appendix end not covered) |
| Wolpert, Doya & Kawato 2003, "A unifying computational framework for motor control and social interaction", Phil Trans R Soc B 358:593 | Author PDF (bicr.atr.jp), text extracted and read: §§1–4 including the social loop and the MOSAIC observation mode |
| Movellan 2005, "An Infomax Controller for Real Time Detection of Social Contingency", ICDL 2005 | Author PDF (mplab.ucsd.edu), text extracted and read: the introduction, the causal model, inference and control (§§I–III) |
| Beebe, Jaffe, Markese, Buck, Chen, Cohen, Bahrick, Andrews & Feldstein 2010, "The origins of 12-month attachment: A microanalysis of 4-month mother–infant interaction", Attach Hum Dev 12:3–141 (PMC3763737) | Full text via a fetch tool, characters 0–200k of 541k: the abstract, introduction and Method. **Results were not read.** |
| Gergely & Watson 1996 | **Not read by me.** Only through this project's note gergely-watson-1996-social-biofeedback.md, which itself read a Hungarian translation. Claims from it are marked as secondary. |
| Ng et al. 2022, "Learning to Listen", arXiv 2204.08451 | arXiv PDF, text extracted: method, baselines, Table 1, discussion |
| Cobbe et al. 2021, "Training Verifiers to Solve Math Word Problems", arXiv 2110.14168 | **Abstract only** |

## 1. Parts list (novelty test)

| # | Part of the core mechanism | Existing mechanism | Evidence |
|---|---|---|---|
| 1 | $x^o = G_\theta^{-1}(o)$: the partner read into own motor coordinates by inverting the own forward model | Inverse or forward-model inversion; analysis by synthesis; MOSAIC's observation mode | Wolpert et al. 2003: "each controller in the observer generates the motor command that it would produce given the observed trajectory ... the observer uses her own multiple modules to try to simulate the observed percept." |
| 2 | $K^{ab}_{k}(\tau)$ written by $K \leftarrow \lambda_k K + \eta_k (x^b - K x^a_{t-\tau}) x^{a\top}_{t-\tau}$ | The **gated delta rule** with a constant gate. It is also the leaky LMS/Widrow–Hoff adaptive filter, one per lag, which makes it an online multi-lag linear (VAR-type) regression | Yang et al.: $S_t = S_{t-1}(\alpha_t(I-\beta_t k_t k_t^\top)) + \beta_t v_t k_t^\top$, "where the data-dependent gating term αt∈(0,1) controls state decay", with "the delta rule optimizing the online regression objective". They credit the rule to Widrow et al. 1960 (not read by me). The sketch's rule is this with $\alpha=\lambda_k$ fixed, $k = x^a_{t-\tau}$, $v = x^b_t$, and an $\eta$ that is not normalized. |
| 3 | The three directions $K^{ss}$, $K^{os}$, $K^{so}$ | Beebe and Jaffe's **self-contingency** and **interactive contingency**, estimated as lagged time-series regressions in each direction | Beebe et al. 2010: "Self-contingency (auto-correlation) refers to the degree to which a prior state predicts the next observed state within an individual"; interactive contingency is "moment-to-moment adjustments of each individual that are correlated with changes" in the partner; model "M = M_lagged + I_lagged + ...", lagged variables "a weighted average of the recent prior sec", "Typically the prior three sec sufficed". |
| 4 | $\hat x^b = \sum \alpha_{k,\tau}(q_t) K_k(\tau) x^a_{t-\tau}$ | Softmax attention or mixture-of-experts gating over a bank of linear predictors. MOSAIC's responsibility weighting over predictors is the motor-control form of it | Wolpert et al.: "The set of errors are transformed into responsibilities (probabilities)" |
| 5 | $\Gamma_t$: the fraction of the partner's variance explained by the own past, per channel and scale | The $R^2$ of a lagged linear regression, a Granger-type directed statistic. It is computed online instead of offline | As 3. Beebe et al.: "the larger the coefficient, the stronger the contingency." |
| 6 | Band drive $\gamma_t = \mathrm{dist}(\Gamma_t, [\kappa_{lo}, \kappa_{hi}])$ | Dead-zone set-point regulation on a statistic. The band itself is the "optimum midrange model" and Watson's "high-but-imperfect contingency" preference | Beebe et al. 2010 report Jaffe et al. 2001: "midrange degree of 4-month mother-infant and stranger-infant interactive contingency of vocal rhythms" predicted security, "higher and lower degrees predicted disorganized/anxious-resistant and avoidant attachment", and "more contingency is not necessarily better". Watson's preference for high-but-imperfect contingency (secondary, via the project note on Gergely & Watson). |
| 7 | Bid $\gamma_t \sum_\tau K^{so}_{slow}(\tau)^\top \Delta_t$ | One gradient step of **distal supervised learning** through a learned linear forward model of the other: $-\nabla_x \lVert \Delta - Kx\rVert^2 \propto K^\top(\Delta - Kx)$. Socially, MOSAIC's forward social model used to pick one's own act. The behavior "bid when you are unsure whether the partner responds" is Movellan's infomax contingency controller | Wolpert et al.: "by monitoring one's own action and the response of others it is possible to learn a predictive model of the likely behaviour of someone in response to our actions" and "a forward social model could be used to determine the appropriate change in our actions to achieve our desired result." Movellan: the robot schedules its actuator to "maximize the information received about the presence or absence of social agents". |
| 8 | Markedness $m_t$: the gain of $K^{so}_{fast}$ above 1 on the own-expression subspace | A hand-set detector on an operator's singular values. Its content is Gergely and Watson's markedness | Project note, secondary: mothers "mark" mirroring with "an exaggerated, transformed version of their real emotion expression". The sketch says itself: "an innate prior that I chose; it is not derived." |
| 9 | Binding loss $\beta(m_t)\lVert x^o_t - W e_\theta(\iota_{t-\tau})\rVert^2 + \beta_{IB} I(\iota; e_\theta)$ | A gated auxiliary regression (the partner's response predicted from the own interoceptive embedding) plus an information-bottleneck penalty | Gating a supervised loss by a detector is standard. The IB penalty is named here, not read. |
| 10 | Valence $= d\Gamma/dt$; arousal $= \lVert \Delta K_{fast}\rVert$ | A rate-of-change readout (the brief's −dF/dt family) and a learning-step-size or surprise readout | brief.md, Candidate A paragraph |
| 11 | Contingency-selected sampling: N Claude drafts, choose by predicted $\Gamma$ | Best-of-N reranking by a scorer | Cobbe et al. (abstract): "we generate many candidate solutions and select the one ranked highest by the verifier." |
| 12 | Mirror priming: retrieval of the partner's past words keyed by kernel similarity | Content-addressable memory or nearest-neighbor retrieval in a new key space. Q9 already rules a new key space not novel | Q9 |
| 13 | Replay weighted by $\lVert \Delta K\rVert$ | Prioritized replay | Project note schaul-2016-prioritized-experience-replay.md (not re-read here) |

**No part is new.** Parts 2–7 together are, almost term for term, an online, agent-internal version of Beebe and Jaffe's dyadic time-series model (self and interactive contingency, lagged, per modality), plus their midrange hypothesis turned into a set point, plus a MOSAIC forward social model used for control.

## 2. Closest prior work, and what the sketch adds

1. **Beebe et al. 2010 and Jaffe et al. 2001 (developmental).** This is the closest prior work, and the sketch does not cite it. Beebe estimates exactly $K^{ss}$ (self-contingency) and $K^{os}$/$K^{so}$ (interactive contingency for each partner) as lagged regressions over about 3 s, per modality. Beebe also hypothesizes that the healthy region is a band: "insecurity biases the system toward contingency which is both heightened (in some modalities) and lowered (in others)."
   - **What the sketch adds:** (i) the statistic is computed online by one party and used as that party's state, not by an observer after the fact; (ii) multiple decay scales; (iii) the band is a control target that triggers action, not a correlate of later attachment.
   - (i) and (iii) are an architectural use of a known statistic, not a new computation.
   - Beebe et al. also report that "measures of maternal contingent coordination with infant yielded the fewest associations with 12-month attachment". That cautions against treating the mother→infant direction as the carrier of affect.
2. **Wolpert, Doya & Kawato 2003 (computational neuroscience).** Here the "forward social model" (other's response to my act), its use to choose one's own action, and the reading of others through one's own modules are already stated.
   - **What the sketch adds:** linear, multi-lag, multi-scale forward models updated by the delta rule; the target of control being a statistic of the forward model ($\Gamma$) rather than a desired state of the other; and the markedness-gated binding loss.
   - MOSAIC has no notion of regulating *how predictable the other is from me*. That is the sketch's real addition at the level of the objective, and it comes from Watson and Jaffe/Beebe, not from ML.
3. **Movellan 2005 (developmental robotics).** A robot that decides whether a partner is contingent, and schedules its own actions to find out. Its causal model separates "self periods", "agent periods" and "background periods" by response delay $[\tau_{1a}, \tau_{2a}]$, and the robot's background-rate prior lets it reject "two social agents ... talking to each other" as non-contingent.
   - **What the sketch adds:** multi-dimensional, continuous, multi-scale operators instead of one binary channel, and the band instead of pure information gain.
   - **What Movellan has that the sketch lacks:** an explicit background process. It is exactly the defense against the sketch's own §6 failure (co-driven covariation). Movellan's inference "does not depend on o1,t, q1,t, i.e., the self-periods are uninformative", so self-feedback is separated structurally. The sketch's $K^{so}$ has no such separation, so the agent's own echo and the shared drivers both enter $\Gamma$.
4. **Yang et al. 2024 / Schlag et al. 2021 (ML).** The algebra is identical, and the sketch says so ("Same algebra").
   - **What the sketch adds:** a choice of keys and values (own lagged acts and the partner's present) and reading the matrix as affect. Under Q9 a new key space is not a new mechanism.

## 3. Reduction attempt

The whole sketch can be rewritten as:

> **Beebe/Jaffe dyadic contingency model, computed online** (a bank of leaky-LMS lagged linear regressions = gated delta rule with fixed gates, one per direction, lag and decay scale) **+ attention gating over that bank** (mixture of experts) **+ a dead-zone set-point controller on the regression $R^2$** (the optimum-midrange hypothesis as a set point) **+ action by one gradient step of distal supervised learning through the forward social model** (MOSAIC; Movellan for the "bid to test contingency" behavior) **+ a gated auxiliary regression loss** (Gergely & Watson's markedness made into a sample weight) **+ best-of-N reranking** of Claude drafts.

Every term of the sketch's equations is accounted for. **Verdict: recombination.**

If the sketch wants a claim to novelty, the only candidate is the **markedness-gated binding**: partner responses whose fast operator has gain > 1 on the own-expression subspace are used as regression targets for the own interoceptive encoder. That is a new *use* of a detector to select training data. It is not a computation absent from prior work, and its detector is hand-set.

## 4. Break attempts on the shared risks

### (a) Collapse into a delayed copy of the partner

**Argument.** Every term of the action equation is a linear function of lagged partner and own history:
- the attunement term is $\sum \alpha K^{os}(\tau) x^o_{t+1-\tau}$;
- the bid is $K^{so\top}\Delta$, where $\Delta$ is the partner's missing response;
- the reflexes $\rho(x^s_t)$ act on an own state that is itself mostly a function of past actions.

The only variance source independent of the partner is interoception $\iota$, which the sketch calls "one input among several" and which moves slowly. In a listener segment of Seamless Interaction, the speaker supplies most of the AU variance. The agent's output is then a time-varying linear filter of the speaker's last 0.1–3 s, which is a delayed, smoothed copy. This is the *Delayed Mirror* baseline in Learning to Listen, which mirrors "the speaker's smoothed motion delayed by 17 frames (≈ 0.5 s)".

**The sketch's answer, and why it misses.** The sketch defends against echo with the upper band edge ("Above it (a perfect echo, which is self-like) the attunement gain is lowered and the agent turns away"). But $\Gamma$ is defined as "the fraction of the partner's variance explained by the agent's own past". That is the *partner* echoing the *agent*. Nothing in the sketch measures or penalizes the *agent* echoing the *partner*, which is the collapse at issue.

**Worse: a limit cycle between copying and turning away.** If the agent copies the partner with delay $d$, then $x^s_{t-\tau} \approx x^o_{t-\tau-d}$. The partner's autocorrelation then makes the agent's past "predict" the partner's present, so $\Gamma^{so}$ rises spuriously. This is the co-driven covariation the sketch itself names in §6.
1. The band then fires from above, and attunement is lowered.
2. $\Gamma$ falls, and bidding starts.
3. Copying resumes.

**Prediction of this critique:** a relaxation oscillation between mirroring and withdrawal, with period set by the slow kernel scale. That is the opposite of attunement.

**Rating.** Answered for the wrong direction; not answered for the right one. A fix would need a $\Gamma^{os}$ ceiling (the agent's own followership), plus Movellan-style separation of shared drivers.

**A related leak (Principle 6).** The project's own verification of the D69 contingency candidate found that in bounded AU space "transfer entropy rises with the agent's mean expression", so "the contact drive leaks toward eliciting expression" (contingency-parity.md, What breaks 2). The sketch's $\Gamma$ is an explained-variance statistic on bounded AU, and its below-band bid pushes toward acts that raise it. The same leak is expected: large, provocative expressions get answered more reliably. Contingency is also sign-blind, so teasing satisfies the drive. The sketch does not address either.

### (b) A single hidden dial from flat affect to rigid imitation

**Argument (derived).** Take expectations of the leaky delta rule at stationarity:

$K = \lambda K + \eta(C_{ba} - K C_{aa})$, so $K^* = C_{ba}\big(C_{aa} + \tfrac{1-\lambda}{\eta} I\big)^{-1}$.

Each kernel is **ridge regression with penalty $(1-\lambda_k)/\eta_k$**. The mimicry gain $\lVert K^{os}\rVert$ is therefore monotone in the single ratio $\eta_k/(1-\lambda_k)$:
- penalty → ∞ gives $K = 0$: no attunement, only reflexes, so **flat affect**;
- penalty → 0 gives the full Wiener regression of own action on the partner's past, applied with gain α: **maximal mimicry** wherever the partner is predictive.

With $1-\lambda_k \approx \Delta t / T_k$, the slow scales (days) have penalty ≈ 0. They are the unregularized pole, which is exactly where temperament is supposed to live.

So the expressive axis from flat to copy is one scalar per scale, and in practice one global ratio, since the sketch fixes $\lambda_k$ by time scale and $\eta_k$ by hand.

**The sketch's answer.** Partial. It makes $\Gamma$ a vector over channels and scales, and adds the band, which modulates the attunement gain. But the band modulates the *same* scalar gain. A vector-valued *readout* does not stop the *policy* from moving along one axis.

**Rating.** Not answered. A fix would have to show a behavior, on published data, that two settings of $\eta/(1-\lambda)$ cannot reproduce. That is the brief's low-dimensional-ablation requirement, with the right ablation: one ridge ratio, not "scalar zero-lag synchrony".

### (c) A lookup table of past faces under scarce data

**Argument.** The kernels themselves are *not* a lookup table. They are second-order statistics (lagged covariances), with about 200k numbers for 32-d features. They cannot store individual faces. The risk is the opposite: a linear operator cannot express content-dependent responses (a smile after a joke against a smile after an insult), so content dependence has to come from the attention query alone.

Two places do become lookup tables under scarce data:
1. **The fast kernel.** At a 0.5 s decay, $K_{fast}$ is a sum of about 15 recent outer products. That is literally a fast-weight episodic store of the last half second, so the bid $K^{so\top}\Delta$ replays the one or two acts that preceded the last strong response. Under a few hours of data, P3 ("replay the own act that used to elicit the missing response") is a lookup by construction, not a generalization.
2. **Mirror priming.** It retrieves "the partner's own past words from moments when the dyad had this contingency structure". With a few hours of one operator, the key space has few occupied cells, so the same handful of utterances will be returned. It is a lookup table of words keyed by kernel geometry.

**The sketch's answer.** Not addressed. Its "scarce data" line covers only parameter learning ("kernels are learned in-session with no gradients").

**Rating.** Partly safe (the core is low-capacity and linear), but the two retrieval paths that carry content are lookups.

### The sketch's own risk (§6) is real and has a published remedy it does not use

Spurious contingency from shared drivers is exactly what Movellan's background process models. The sketch's "conditioning on conversation events" is weaker than an explicit null model.

### The first prediction does not discriminate the mechanism

P1–P3 on Ahn et al. 2023 test whether infant→mother lagged $R^2$ predicts the still-face response. That is a hypothesis about infants in the Beebe/Jaffe tradition. A result either way says little about whether an *agent* built on online kernels works. The stated ablation, scalar zero-lag synchrony, is a straw man. The informative ablation is a single ridge ratio, or Beebe's own multilevel model.

## 5. Which measured failure of published listener models this might fix (hypothesis only)

No baseline has been run in this project (Q11: disk below the floor; research/runs has only P1 and P2). What exists are the published numbers in Ng et al. 2022, Table 1, on their own 72-hour teleconference data.

**Failure 1: no state beyond a short window.**
- Learning to Listen generates and evaluates 64-frame sequences (≈ 2.1 s at the paper's 17 frames ≈ 0.5 s).
- Its Discussion states: "as we only model listener motion in response to a speaker, modeling the full dyadic cycle of back-and-forth effect remains for future work."
- *Hypothesis:* per-partner kernel banks at the 20-minute and days scales could carry partner-specific state across sessions, which a 2-s window cannot. A returning partner in Seamless Interaction would be the test.
- This is the sketch's best claim to a reason to exist under Q9, and it is the same failure the D69 fast-weights line targets. It is therefore not specific to this sketch.

**Failure 2: one-directional modeling.**
- $K^{so}$ models the effect of the listener's acts on the speaker, which Learning to Listen omits by design.
- *Hypothesis:* the bid term could produce listener behavior that elicits speaker responses.
- No published listener metric scores this. The test would need a new analysis, so it is not "as published".

**What the sketch would not fix, and risks causing:**
- *Mirroring collapse.* Learning to Listen reports the re-trained LFI baseline "defaulted to mirroring the speaker, resulting in excessively high synchrony (PCC)": expression PCC 0.89 against ground truth 0.09. By break (a), this sketch's policy is a lagged linear filter of the partner, which is the Delayed Mirror family (PCC 0.98).
- *Damped variation.* The published model's expression variation is 2.01 against ground truth 2.90. The sketch's ridge-shrunk kernels would, if anything, damp variation further.
