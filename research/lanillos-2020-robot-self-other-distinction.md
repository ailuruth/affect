# Robot self/other distinction: active inference meets neural networks learning in a mirror (Lanillos, Pages & Cheng)

Pablo Lanillos, Jordi Pages & Gordon Cheng, *ECAI 2020*, Frontiers in Artificial Intelligence and Applications 325:2410–2416, doi:10.3233/FAIA200372. Read as arXiv:2004.05473v1.

## What was read
The full arXiv PDF (7 pages, extracted to text): all sections, Algorithm 1, equations (1)–(14) and the figure captions. Figures were not seen.

## The computation, precisely
**Body inference by active inference.** The latent body state $\mu$ (7 arm joint angles) is inferred by gradient descent on Laplace free energy. Proprioceptive error $e_p = s_p - \mu$ and visual error $e_v = s_v - g(\mu)$ are weighted by variances $\Sigma_p, \Sigma_v$, plus a goal-attractor prior $f(\mu,\rho)$. **Action also descends the same errors**: $\dot a = -\partial F/\partial a$. The visual forward model $g(\mu)$ (the 2D image position of the hand) is a mixture density network: 1 hidden layer of 20 units, 4 Gaussians, trained on contingent samples (200 samples or 20 s).

**Self attribution = accumulated model evidence.** Per step,
$$L_i = -\tfrac12\big(e_v^\top\Sigma_v^{-1}e_v + \ln\det\Sigma_v + n\ln 2\pi\big),\quad L \leftarrow L + L_i + \ln p(\text{contingent}),$$
$p_{\text{norm}} = (\exp L - \text{LOGMIN})/(\text{LOGMAX}-\text{LOGMIN})$, and $p_{\text{self}} \leftarrow p_{\text{self}} + K(p_{\text{norm}} - p_{\text{self}})$, with $K$ "a smoothing constant working as a Kalman gain". $p(\text{contingent})$ comes from a binary CNN classifier: joint velocities plus a 10-bin optical-flow direction histogram → was this visual motion caused by my action? "Highly surprising events ... drastically drop the probability of being self."

**Results.** Mirror: 10 positions × 10 runs, "All experiments were successfully classified as itself". Actions used random inter-wave delays (up to 3 s) "so actions were not periodic". Two identical robots doing the same movements asynchronously: classified as other; "the robot could not learn anything as there was no causality". A human imitating the robot: "In all cases, the robot correctly identified the agent in front as not itself. However, as expected, **in the case of perfect synchronization the robot will identify it as itself**."

**The side effect the designs need to know about:**
> "We further observed an interesting side effect of using the action to minimize the prediction error. The human or robot hand in the self/other distinction experiment acted sometimes as an attractor for the body inference, **generating mirroring actions similar to imitation**."

## What it means for the designs
- **Active inference copies by default.** If perception and action both descend one prediction-error term, and the other's body falls under the agent's body likelihood, the agent moves to match it. That is automatic imitation produced by the objective itself. Any design whose core is active inference over a shared face code (Principle 3 read naively) **has a built-in copy route**. The cure is the one the brain uses: only self-attributed error may drive action. Formally, action descends $p_{\text{self}}\cdot e$ (or $e$ restricted to the self-register), and other-attributed error updates beliefs about the partner only.
- **A working attribution recipe.** Evidence = the log-likelihood of the observation under the agent's own forward model, plus a contingency term, smoothed with gain $K$. For faces: per action-unit group, the partner's motion that the agent's own recent commands do not predict accumulates "other" evidence.
- **Two identifiability conditions.** (1) The agent's own output must be **aperiodic** (random delays), or a periodic partner becomes indistinguishable. (2) A **perfectly synchronous** copier is classed as self. This matches blakemore-wolpert-frith-2002 and contingency-causal-synthesis.md: a partner who mirrors with zero lag is read as the agent itself. Hogeveen 2015 locates the human need for self–other control in the same place (synchrony).
- **Time scale:** evidence accumulates over seconds (learning ≤20 s; then waving continues "until it decides").

## Verdict
**adopt (as a mechanism and a warning).** It gives the attribution signal as model evidence under one's own forward model, and it shows empirically that active inference without attribution gating produces imitation. Single robot, one joint chain, single-blob vision, no quantitative accuracy beyond 100/100 mirror trials.
