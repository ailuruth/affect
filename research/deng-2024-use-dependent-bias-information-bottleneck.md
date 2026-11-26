# Use-dependent biases as optimal action under information bottleneck (Deng & Haith)

Hokin X. Deng & Adrian M. Haith, arXiv:2407.17793v4 [q-bio.NC], 15 Aug 2024 (author's manuscript).

**Why this source.** The brief listed Zénon, Solopchuk & Pezzulo 2019 (*Neuropsychologia* 123:5–18) and Sims 2003 (*J Monetary Econ* 50:665–690). Neither could be read:
- Zénon's bioRxiv preprint (10.1101/208280) returned 429, and biorxiv.org is then not resolvable from this session;
- the typeset.io copy returned 403;
- Sims' Princeton page did not resolve;
- the journal versions are paywalled.

Neither is cited below. This paper was read instead. It is the closest readable case of a capacity limit on a **continuous** sensorimotor channel producing a measured behaviour in humans. It cites Zénon et al. 2019 and Tishby & Polani for its framing.

## What was read
The arXiv PDF from export.arxiv.org, in full (about 7,700 words): introduction, theory (§2.1–2.3), both experiments, results, discussion and Appendix A (the derivation of the optimal policy). Figures were seen as captions.

## The computation, precisely

**Objective (Eq. 1).** $\min \mathbb E[J(s,a)]$ s.t. $I(S;A)\le C$. The optimum (Eq. 2) is $p(a\mid s)\propto p(a)e^{-\beta J(s,a)}$, with β monotone in C.

**Continuous closed form (Eq. 3).** Take a quadratic cost $J = \frac12(s-a)^2$ and a Gaussian action marginal $p(a) = \mathcal N(s_0, 1/\epsilon)$, where $s_0$ is the repeated (habitual) direction and ε its precision. Then
$$p(a\mid s)\propto \exp\Big[-\tfrac{\beta+\epsilon}{2}\Big(a - \frac{\beta s + \epsilon s_0}{\epsilon+\beta}\Big)^2\Big].$$
The mean response to target s is a **shrinkage toward the agent's own habitual action** with gain $\beta/(\beta+\epsilon) < 1$ on the target. The variance is $1/(\beta+\epsilon)$. Lower capacity means lower β, which means a smaller gain, a larger bias toward $s_0$, and more variability.

**Speed (§2.3).** An optimal-feedback-control model (Liu & Todorov 2007) gives a cost-to-go on initial direction about 6.73× (≈7×) larger for 250 ms than for 500 ms movements. Substituting this into Eq. 2 predicts that the bias nearly vanishes for fast movements.

**Data.**
- **Handedness experiment** (N = 28): 7 targets; in repetition blocks the central target appears 70 times per 100 trials.
  - Repetition reduced the slope of initial direction against target by −0.072 ± 0.040 in the non-dominant hand and −0.039 ± 0.049 in the dominant hand.
  - The hand × condition interaction was F = 7.92, p = .009. The bootstrap 99% CI of the difference was [0.0037, 0.0639].
- **Speed, a re-analysis** of Wong & Haith 2017 (N = 16): there was a bias toward the array centre at slow speed (p < .001) and none at fast speed (interaction p = .04). The model was fitted to a ~3° bias at 30° eccentricity for slow movements.

Discussion points:
- the equations are "directly analogous to Bayesian inference", but of the motor command, not of the target;
- "even the degree of action variability is a consequence of the information bottleneck";
- in motor control the cost may reflect neural resource and precision, not policy storage as in Lai & Gershman.

## What it means for the designs

Map s = the partner's current expression level on one channel, a = the agent's level on that channel, and J = whatever the agent's core says the response should be (for a copier, J = ½(s − a)²).

- **The one clean result for "per-channel copy gain".** If the core's target *were* copying, a capacity-limited channel produces a copy gain $\beta/(\beta+\epsilon)$ strictly below 1, a pull toward the agent's own habitual level $s_0$, and variability $1/(\beta+\epsilon)$. Per channel, a lower innate capacity gives a lower ceiling on copy gain. This is the information-cap analogue of the REN per-channel ceiling.

  Two limits stop it being a learning-proof ceiling:
  1. β/(β + ε) depends on ε, the *precision of the agent's own habit*. A broad, uncertain habit (small ε) lets the gain approach 1 at fixed β. So the ceiling is set by C *and* by how stereotyped the agent's own repertoire is.
  2. The gain is per sample. For a slowly varying held level, the bits per second needed are small (see the Tanaka note), so a held level is still followed almost fully.
- **Stakes reduce bias.** When an error is costly (fast movements, high J curvature), the bias vanishes. For a dyad: on channels where the agent's own concerns make the partner's state matter sharply, the agent tracks the partner closely; on low-stakes channels it reverts to its own habit. Applied to copy that is a dial again, but applied to *the agent's own response target* (not copy) it is per-expression gating by the agent's concerns.
- **Variability as a signature of the cap.** Lower-capacity channels (the non-dominant hand) are both more variable and more biased. A capacity-limited agent should show more variable *and* more self-biased expression on channels with less capacity. That is a testable prediction, without labels, for a learned agent.
- **Sign.** The sign of the mapping belongs to J, not to the cap.
- **Copy non-attracting.** The habit marginal $s_0$ is itself learned from the agent's own past output (use-dependence). If the agent has been copying, $s_0$ drifts toward the partner's typical level. That gives slow convergence in level and parameters (C9 in non-copying-dynamics-synthesis.md), not instantaneous matching. Whether that drift is bounded depends on how fast the marginal is updated, which is a learned or innate time constant that must be named.
- **Framework.** This is rate–distortion / policy compression in a continuous action space (existing). Here it reduces exactly to Bayesian shrinkage, so it is not a new computation.

## Verdict
**adopt (evidence).** In human reaching, a capacity limit on the state→action channel yields a gain below 1 toward the target, a pull toward one's own habitual action, and more variability where capacity is lower. All of it is reduced when errors are costly. The gain ceiling depends on the agent's own habit precision as well as C, and it does not cap held-level tracking. Zénon et al. 2019 and Sims 2003 remain unread.
