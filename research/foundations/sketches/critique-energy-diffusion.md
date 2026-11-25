# Critique: v2-energy-diffusion (surprise re-noising in a rolling dyadic diffusion)

Critic: an independent subagent that did not write the sketch. Written 2026-11-25 for the Q8 critique round and the Q9 novelty test. No data or weights were downloaded. Quotes are from primary sources I fetched and read; the extent of each reading is stated in §2.

**Verdict: recombination.** Every computational part is an existing mechanism. The closest single prior work is one the sketch does not cite: **Adaptive Online Replanning with Diffusion Models (RDM; Zhou, Du, Zhang, Xu, Shen, Xiao, Yeung, Gan; arXiv 2310.09629, 2023).** RDM already uses the diffusion model's own likelihood drop on a persistent, partly executed trajectory to choose how deeply to re-noise it, keeps the executed past clamped, and denoises again. The sketch's real additions are:
- a continuous surprise-to-depth map, where RDM uses two thresholds;
- a temporal pyramid, with per-level gates placed at speciation thresholds (Biroli et al. 2024).

These are new settings of existing parts, not a new computation.

---

## 1. Parts list (novelty test)

| # | Part, as written in the sketch | Existing mechanism | Source (read) |
|---|---|---|---|
| 1 | Rolling window over the dyad's trajectory with a clamped past and an imagined future, where each token carries its own noise level | Rolling Diffusion; Diffusion Forcing | Ruhe et al. 2024: "uses a sliding window denoising process … assigning more noise to frames that appear later". Chen et al. 2024: "each token is associated with a random, independent noise level, and … tokens can be denoised according to arbitrary, independent, per-token schedules". |
| 2 | Temporal pyramid, levels subsampled by $2^\ell$ | A standard multi-rate (dyadic) decomposition. Neither the sketch nor I claim it is new. I read no source for pyramids as such. The multi-time-scale *hierarchy of reset* is in Event Segmentation Theory (row 8). | — |
| 3 | $u=\phi(o)$: the other's face in the agent's own motor coordinates | An inverse model used for covert imitation (the "simulation route") | Pickering & Garrod 2013, Fig. 3: A uses "the inverse model and context … to derive the action command … that A would use if A were to perform B's act". |
| 4 | $E^{\text{learn}}$: a transformer trained by denoising score matching | A diffusion or score model, parameterized as an energy (energy-based model) | Ruhe et al. 2024, eq. 5 (the standard diffusion loss). |
| 5 | $E^{\text{innate}}$: a flat-bottomed $\psi$ plus fixed reflex wells, added to the learned energy | A product of experts in energy, i.e. guidance by a hand-specified cost | Chen et al. 2024 (Diffusion Forcing), §3.4: guidance with "any reward … specified over future steps … sparse rewards indicating goal completion $-\lVert o_T-g\rVert^2$". |
| 6 | Self–other swap symmetry of $E^{\text{learn}}$ | A permutation-invariant function (by weight tying or input symmetrization) | Zaheer et al. 2017 (Deep Sets), defining invariance "for any permutation π". |
| 7 | Surprise $\Delta_t=E(W\mid u_t)-E(W)$: the energy jump of the current sample when the new observation is clamped | The generative model's likelihood of the current trajectory sample, used as a trigger to replan | RDM: "we propose to leverage the internal estimated likelihood of the currently executed plan as a gauge on when is a good time to replan." Event Segmentation Theory: "When transient errors in predictions arise, an event boundary is perceived." |
| 8 | $\sigma_t=R(\Delta_t)$, and re-noising only the levels with $\sigma^*_\ell<\sigma_t$, so that a larger surprise reopens slower structure | (i) Likelihood-thresholded re-noise depth: RDM, which uses two thresholds. (ii) Error-thresholded reset at multiple time scales: Event Segmentation Theory. (iii) Per-token noise levels: Diffusion Forcing. (iv) Why distance from the data manifold calls for deeper noise: SDEdit Proposition 1. | RDM Alg. 1: "Threshold $l_s$ of Replanning from scratch, Threshold $l_f$ of Replanning with future and $l_s<l_f$ … Diffusion step $N_f$ … $N_f\ll N_s$". Zacks et al. 2007: "For each timescale, the error signal is integrated to provide a reset signal tuned to the appropriate grain. Fine-grained representations are tuned such that they can be updated in response to small, brief increases in prediction error. For coarse-grained representations … resets happen only in response to larger, more sustained increases in error." SDEdit: "If the guide is far from any realistic images, then we must tolerate at least a certain level of deviation from the guide." |
| 9 | $\sigma^*_\ell$ set at the speciation noise level of each level | Speciation time computed from the top eigenvalue of the covariance. Used here as a fixed gate setting, not a computation. | Biroli et al. 2024: "$\Lambda e^{-2t_S}=1$ … where $\Lambda$ is the eigenvalue of the principal component of the covariance matrix of the data." |
| 10 | Probability-flow ODE from $\sigma_t$ down to $\sigma_{\min}$, with the past and $u_t$ clamped (inpainting) | Diffusion sampling with conditioning by replacement | RDM §3.2: "We will fix the timesteps of $\tau_{\to k}$ that are smaller than $k$ to their observed value." Diffusion Forcing App. B.6 warns that this kind of conditioning, "named 'conditioning by replacement', is both mathematically unprincipled and can lead to inconsistency". |
| 11 | Emit the $s$-channel at $t+\delta$, then roll the window | Receding-horizon execution of a diffusion plan | RDM Alg. 1; Diffusion Forcing §3.4 ("using Diffusion Forcing as a policy"). |
| 12 | Consistency distillation to 1–2 steps | Existing distillation (Song et al. 2023). **Primary source not read by me.** | — |
| 13 | Arousal $=\sigma_t$; valence $=-(E_{\text{after}}-E_{\text{before}})$ | Value or energy-change readouts, which Q9 explicitly lists as existing | Q9 text |
| 14 | Claude: $K$ drafts, each clamped into $c$, draft $k$ chosen with probability $\propto\exp(-\Delta E_k/T)$ | Self-normalized importance resampling of language-model samples under a residual energy | Deng et al. 2020 §3.3: "sampling proceeds simply by: a) sampling from the auto-regressive language model, followed by b) resampling according to the energy function." |
| 15 | Memory retrieval with weights $\exp(-E(W\oplus m))$ | Softmax-weighted retrieval, which Q9 classes as attention or Hopfield retrieval | Q9 text |
| 16 | Replay: score matching on stored windows, trained only up to the noise depth each episode reached | Diffusion training with a chosen weighting over noise levels | Ruhe et al. 2024: "The weighting $a(t)$ can be freely specified." |
| 17 | $\theta$ consolidated nightly | Offline training | — |

**Is any part new?** The only candidate is rows 8 and 9 together: *depth of re-noising, set by surprise and gated per temporal level, as the update rule of a persistent agent state.* Taken apart:
- "A persistent trajectory sample, re-noised by an amount set by its own likelihood, then denoised with the past clamped" is RDM (with the trigger described above).
- "Larger, more sustained error resets coarser time scales" is Event Segmentation Theory.
- "Different tokens at different noise levels within one denoising pass" is Diffusion Forcing.
- "Where to place the thresholds" comes from Biroli et al.

Composing these is a design choice. It is not a computation that is absent from prior work.

A further reduction from optimization: *perturb by a chosen amount, then relax to the local minimum* is Monte Carlo basin-hopping (Wales & Doye 1997). There, "the energy at any point in configuration space is assigned to that of the local minimum obtained by the given geometry optimization", and the perturbation "step size … was adjusted to give an acceptance ratio of 0.5". Re-noise then denoise is a stochastic perturb-and-relax on a learned landscape. The sketch's "mood shift = jump between basins" is basin-hopping driven by surprise.

## 2. Closest prior work, read in primary sources

What I read: RDM §§1–3 in full, including Algorithms 1–3; Diffusion Forcing §§3–3.4 and App. B.4–B.7; Rolling Diffusion §§1–3; SDEdit §3, including Prop. 1 and the choice of $t_0$; Biroli et al. introduction, the speciation and collapse sections, and the general criteria; Zacks et al. 2007, the PMC author manuscript, reading the theory, multiple-time-scales, neural-mechanism and limitations sections (not every empirical review section); Wales & Doye 1997 §2; Learning to Listen §§3–5 and the appendix on per-person models; Avatar Forcing introduction, §3 and App. E (limitations).

1. **RDM, Zhou et al. 2023 (ML). The closest work, and missing from the sketch's table.**
   - **What RDM already does:** a likelihood-based surprise on a persistent trajectory, with the depth of re-noising chosen from it. "When the likelihood assessment of a diffusion model on the plan has a low probability, it is a good indicator of the need for replanning." "We initialize our new plan with the old one and add a small amount of noise to the plan before then denoising the added noise." The likelihood is estimated by re-noising: "we assess the degree to which a diffusion model recovers its original plan after the plan has been corrupted by Gaussian noise."
   - **What the sketch adds:**
     - a continuous $R$ in place of two thresholds;
     - per-level depth over a temporal pyramid, so that the depth selects a *time scale* rather than the whole remaining plan;
     - a dyadic, swap-symmetric energy with innate wells;
     - the reading of re-settling as affect.
   - **What does not differ:** the update rule itself (likelihood drop → re-noise → clamped denoise → execute the first action). The sketch's §2 claim that in prior work "the noise level is fixed by position or schedule" is **false** for RDM.
2. **Diffusion Forcing, Chen et al. 2024 (ML).**
   - **What it already does:** per-token noise levels, a clamped past and noise-stabilized rollouts ("updating the latents using the previous latent associated with slightly 'noisy tokens'"). App. B.7 interprets the noise level as the interpolation between a Bayes filter's prior and posterior: "By varying k between K and 0, the same neural network can parameterize everything between prior and posterior."
   - **What the sketch adds:** a noise level set online by surprise. In Diffusion Forcing the schedule matrix $\mathcal K$ is chosen at design time ("$\mathcal{K}$ can be designed to flexibly achieve different behaviors without re-training").
   - **Why it matters for the reduction:** by B.7, the sketch's surprise-set $\sigma_t$ *is* an adaptive prior-versus-evidence weight. That is the adaptive-gain filter the sketch's own §6 fears.
3. **Event Segmentation Theory, Zacks et al. 2007 (neuroscience and psychology).**
   - **What it already does:** prediction-error-gated reset of working "event models", at several time scales, with coarse scales resetting only on larger and more sustained error. It is attributed to "midbrain neuromodulatory systems" broadcasting error signals.
   - **What the sketch adds:** a concrete generative implementation (diffusion re-noising) and a criterion for where the thresholds sit (speciation).
   - **What EST lacks:** a learned energy over a dyad, emitted action, and any account of affect. Its authors note the reset "needs more development" and is "a purely passive perceiver".
4. **Biroli, Bonnaire, de Bortoli & Mézard 2024 (dynamical systems and statistical physics).** The sketch borrows speciation; I record two things it leaves out:
   - (i) The sharp threshold holds only "in the simultaneous limit of large number and dimension of the data". In finite dimension it is a crossover, and $t_S$ itself is "a convention".
   - (ii) The same paper's *collapse* transition is memorization: "a given trajectory commits to the attraction basin of one of the data points". Avoiding it needs "the number of data [to be] exponential in the dimension". This bears directly on break (c).

Also checked:
- **SDEdit** chooses $t_0$ by hand or by "binary search" with the user, but its Proposition 1 gives the logic that a guide farther from the manifold needs a larger $t_0$.
- **Rolling Diffusion** already ties high noise to low-frequency structure: "the model output tends to contain low-frequency information in high noise regimes". This is the frequency-domain half of the sketch's "time scale = noise scale".

## 3. Reduction attempt

**Rewrite.** RDM (Zhou et al. 2023), with these additions:
- (a) a Diffusion-Forcing per-token noise schedule over a dyadic temporal pyramid, in place of one depth for the whole future;
- (b) an Event-Segmentation-style multi-threshold gate, in place of two thresholds, with the thresholds placed at Biroli speciation levels;
- (c) hand-specified energy guidance (homeostatic $\psi$, reflex wells) added to the learned energy;
- (d) a swap-symmetric (permutation-invariant) energy;
- (e) Deng et al.'s residual-EBM resampling of Claude drafts;
- (f) arousal and valence read out of $\sigma_t$ and $\Delta E$.

Every part maps to an existing mechanism, and nothing in the update rule is left over.

**Verdict: recombination.** Q9 already called this sketch "the closest to a new mechanism, but it still borrows diffusion". Finding RDM strengthens that: the surprise-to-re-noise-depth rule itself is also borrowed.

## 4. Break attempts on the shared risks

### (a) Collapse into a delayed copy of the partner
**Scenario.**
1. Levels $\ell\le2$ are pretrained on Seamless dyads (§3), and at every tick $u$ is clamped at level 0.
2. In human dyads the strongest short-lag cross-channel regularity is the listener following the speaker at about 0.5 s. Learning to Listen reports that "the average TLCC calculated for GT and Ours were both ≈17 frames … ≈0.5 s", and builds a *Delayed Mirror* baseline at that lag.
3. A denoiser that has to inpaint $s$ given clamped $u$ will therefore learn $s_t\approx \text{smooth}(u_{t-15})$ as its cheapest low-loss solution. Learning to Listen's own baseline LFI, retrained on in-the-wild data, "defaulted to mirroring the speaker".
4. The sketch makes this worse in two ways:
   - The mimicry account *wants* the diagonal basin first: "the earliest learned basin is the diagonal $s\approx u$. With $u$ clamped at level 0, denoising pulls $s$ along it."
   - Its prediction 3 says surprise *raises* short-lag coupling to the partner, "because the clamp dominates the reopened prior". So the more surprising the partner, the more the agent copies.
5. Swap symmetry adds a latent version of the same collapse. $\tilde b$ is "never observed, only inpainted" by a score that is symmetric in (self, other). With no data on $\tilde b$, the symmetric fixed point is $\tilde b\approx b$. The agent projects its own body state onto the other.

**Does the sketch answer it?** Weakly. §4 asserts that "Mimicry is predicted to weaken as living adds other structure", with no mechanism. §6 concedes that under coarse unimodality the output is "only a smoothed mirror". No term in $E$ penalizes $s\approx u_{t-\delta}$.

### (b) A single hidden dial from flat affect to rigid imitation
**Argument.** Scale the surprise map, $R\to kR$.
- **$k\to0$:** only the always-open fine levels are ever re-noised. Coarse levels never reopen, mood is frozen, and the emitted face is a fixed conditional of a fixed coarse state. That is flat, stereotyped affect.
- **$k\to\infty$:** every tick re-noises every level. By Diffusion Forcing's B.7 reading, noise erases the prior, so the re-sampled window is dominated by the clamped evidence $u$. That is imitation with no carry-over.

In between, $k$ sets one global prior-versus-evidence weight. The arousal readout *is* that dial, since arousal $=\sigma_t$. The speciation thresholds $\sigma^*_\ell$ fix *where* the steps sit but not $k$, because $R$ is only "a monotone map". Avatar Forcing documents the same one-dimensional tension in a published diffusion-forcing listener:
- the base model gives "less diverse, stiff motions, particularly in response to non-verbal cues";
- the fix is to train *against* samples made "by dropping the user signals", which moves the model along the axis from stiff to user-driven.

**Does the sketch answer it?** Partly. §6 names the risk ("collapse into an adaptive-gain filter: an HGF-like model with extra steps"). It also proposes a check: compute $\sigma^*_\ell$ from published data before any engine work. That check addresses whether coarse levels have more than one basin. It does not address the gain dial $k$, which remains free.

### (c) A lookup table of past faces under scarce data
**Argument.** Coarse levels are learned "only from living".
1. Level 8 has 8.4-s tokens, so about 430 tokens per hour, and a window of tens of tokens. Each token carries AUs, voice, $b$, $\tilde b$ and a text embedding $c$, so a coarse window has dimension $d$ in the thousands.
2. A few hours a day over weeks gives $n$ in the low thousands of windows, so $\alpha=\log n/d\ll1$.
3. Biroli et al. show this is the collapse (memorization) regime: "$t_C$ is of order one only when the number of data is exponential in the dimension". Below $t_C$, a trajectory "falls into the attractor of one given data point".
4. A deep re-noise followed by denoising then returns a stored past episode, which is literally a lookup of a past mood and face trajectory.
5. Swap symmetry only doubles $n$ (×2), which leaves $\log n/d$ unchanged in order.
6. If the network is regularized enough to avoid memorization, the opposite failure follows (the sketch's own §6): one basin and no speciation.

So with the stated data budget the coarse levels sit between two failures: memorization or unimodality. The window in which they are multimodal *and* generalizing is not shown to exist.

**Does the sketch answer it?** No. It addresses unimodality (§6) but never memorization. The swap-symmetry "doubling" does not change the scaling.

### Further problems found while reading
- **The "time scale = noise scale" identification is asserted, not derived.** Biroli's $\sigma^*$ depends on the top covariance eigenvalue $\Lambda$ of whatever is diffused. For each level's standardized tokens, $\Lambda$ reflects how concentrated the correlation is, not how slow the level is. Nothing guarantees $\sigma^*_{\ell+1}>\sigma^*_\ell$. Their criterion also assumes data "organized in distinct classes" with "a single large eigenvalue".
- **The distinctive prediction does not separate the strongest rivals.**
  - "Step, not linear" is also predicted by Event Segmentation Theory (thresholded reset per grain), by RDM-style two-threshold replanning, by Bayesian online changepoint detection (run-length reset; Adams & MacKay 2007), and by any SSM with input-dependent gates (for example the data-dependent forget gate of GLA, Yang et al. 2023).
  - The sketch compares only against *linear* leaky integrators.
  - In addition, a sharp step is a large-$d$ limit result (Biroli). A low-dimensional slow AU band predicts a smooth crossover even if the mechanism is right, so the test can fail for the wrong reason.
- **"Surprise" in the test is not the listener's surprise.** It is scored "with a predictive model of the partner trained on other dyads". That is a population proxy, and it may correlate with partner motion energy in ways a match on motion energy only partly removes.
- **Claude coupling.** The draft selection is Deng et al.'s residual-EBM resampling. It is the same mechanism as the linguist sketch's "sayability" selection, so neither sketch can claim it as novelty. §6 rightly flags that it is mode-seeking.

## 5. Which measured failure of published listener models this might fix (hypothesis only)

None of these baselines has yet been run on Seamless Interaction in this project (Q9, Q11). Avatar Forcing is CUDA-only per research/avatar-forcing.md and is not runnable here. The failures below are those the published papers report themselves.

- **No lasting state.**
  - **Published fact:** Learning to Listen is trained per listener with a past context of $t=32$ frames inside $T=64$-frame sequences ("We use w=8, T=64 … t=32"), at 30 fps.
  - **Hypothesis:** the slow levels of the pyramid (minutes) would carry a post-event shift in the slow expressive band. A window-limited model cannot carry such a shift, so a lasting change after a surprising partner event (measured with the band-limited baseline shift in §5 of the sketch) would separate the two.
- **Stiff, low-variance listening** (Avatar Forcing: "less diverse, stiff motions").
  - **Hypothesis:** surprise-driven re-noising injects variability at the right moments, rather than uniformly.
  - **Risk:** this is the same dial as break (b), so any gain may come from more mirroring.
- **Long-rollout drift and exposure bias** (Avatar Forcing App. E: diffusion forcing "does not fully address exposure bias"). Here the sketch adds nothing beyond Diffusion Forcing's own noise stabilization.

**Bottom line for Q9.** This sketch's reason to exist would have to be the measured *absence of a surprise-dependent, lasting slow-band shift* in published listeners. That absence has not been measured. If it were measured, an RDM- or EST-style gated model would be the fair baseline to beat, not a linear SSM.

## Sources read (primary)
- Zhou, S., Du, Y., Zhang, S., Xu, M., Shen, Y., Xiao, W., Yeung, D.-Y., Gan, C. (2023). Adaptive Online Replanning with Diffusion Models. arXiv 2310.09629.
- Chen, B., Martí Monsó, D., Du, Y., Simchowitz, M., Tedrake, R., Sitzmann, V. (2024). Diffusion Forcing. arXiv 2407.01392.
- Ruhe, D., Heek, J., Salimans, T., Hoogeboom, E. (2024). Rolling Diffusion Models. arXiv 2402.09470 (ICML 2024).
- Meng, C. et al. (2022). SDEdit. arXiv 2108.01073.
- Biroli, G., Bonnaire, T., de Bortoli, V., Mézard, M. (2024). Dynamical regimes of diffusion models. arXiv 2402.18491 (Nat. Commun.).
- Zacks, J. M., Speer, N. K., Swallow, K. M., Braver, T. S., Reynolds, J. R. (2007). Event perception: a mind–brain perspective. Psychol. Bull. 133:273 (PMC2852534).
- Wales, D. J., Doye, J. P. K. (1997). Global optimization by basin-hopping. arXiv cond-mat/9803344.
- Adams, R. P., MacKay, D. J. C. (2007). Bayesian Online Changepoint Detection. arXiv 0710.3742 (model and run-length sections).
- Deng, Y., Bakhtin, A., Ott, M., Szlam, A., Ranzato, M. (2020). Residual Energy-Based Models for Text Generation. arXiv 2004.11714.
- Zaheer, M. et al. (2017). Deep Sets. arXiv 1703.06114 (definition of permutation invariance only).
- Yang, S. et al. (2023). Gated Linear Attention Transformers. arXiv 2312.06635 (§§2–4, gating).
- Pickering, M. J., Garrod, S. (2013). BBS 36:329 (target article §§2–4).
- Ng, E. et al. (2022). Learning to Listen. arXiv 2204.08451.
- Ki, T. et al. (2026). Avatar Forcing. arXiv 2601.00664.
