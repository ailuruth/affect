# Sketch v2: Resonant dyad (metastable oscillator reservoir with a mirror clone)

Lens: physics of coupled oscillators, reservoir computing, metastability and criticality. Two people form one driven dynamical system. Emotion is the pattern of partial synchrony that this system wanders through.

## 1. Core mechanism

The agent runs two copies of one network of $N \approx 512$ Stuart–Landau oscillators, $z_i = r_i e^{i\theta_i} \in \mathbb{C}$. The **self** copy is $x=s$. The **clone** copy is $x=c$. Both copies share the parameters $(\mu, \omega, K)$. The nodes split into a motor layer $M$ ($\approx 40$ nodes: AUs, jaw and visemes, pitch, energy, breath, blink) and a core $C$.

$$
\dot z^{x}_i=\big(\mu_i+\alpha Q(b)+i\omega_i-|z^{x}_i|^2\big)z^{x}_i+\sum_j K_{ij}z^{x}_j+\sum_k G^{x}_{ik}\,e_k(t)+\kappa_p\,\mathbb{1}[i\in C]\,\big(z^{\bar x}_i-z^{x}_i\big)+\sigma(Q)\,\xi_i(t)
$$

- $\mu_i$: distance of node $i$ from its Hopf bifurcation (its excitability). $\omega_i$: its natural frequency, spread from 0.1 to 8 Hz. $K = K_0 + UV^\top$: an innate coupling plus a learned low-rank part ($r \approx 8$–16).
- $e_k(t)$: each input written as an analytic signal (band-pass filter, then Hilbert transform), so every input is a rhythm with a phase, never a value or a label. The inputs are the partner's face and voice features, the encodings of Claude's candidate text with their planned syllable timing, replayed memory trajectories, own proprioception, and the prediction error $\varepsilon=y-\hat y$.
- $G^{x}$: input gains. In the clone, the partner's face and voice, mapped into the agent's own motor coordinates, drive the motor layer $M$ with a large gain $g_{\text{clamp}}$. In the self, the same signals drive $M$ only weakly ($g_{\text{mim}}\ll g_{\text{clamp}}$), and Claude's text drives only the self.
- $\kappa_p$: core-to-core coupling between self and clone for person $p$. Its learned value is the relationship. $\bar x$ is the other copy.
- $Q(b)=\sum_n w_n\,[\,|b_n-b_n^*|-\epsilon_n]_+$: the body variables' deviation from their set points, with a dead zone. This is the only homeostatic input. It raises excitability ($\alpha Q$) and noise ($\sigma(Q)=\sigma_0+\beta Q$). It is a temperature of wandering, not a value.
- Outputs: face $\mathrm{AU}_m=\mathrm{softplus}(|z^s_m|-r_0)$ for $m\in M$; prosody is read from the vocal motor nodes in the same way.
- Prediction readout: $\hat y_{t+\Delta}=W\,[\mathrm{Re}\,z;\mathrm{Im}\,z;|z|]$, where $y$ contains the partner's next features, own body variables $b$, and own proprioception.

**The single objective** is next-step prediction, $J=\mathbb{E}\lVert y_{t+\Delta}-\hat y_{t+\Delta}\rVert^2$. It is minimized on three time scales of the same loss: $W$ online by recursive least squares (seconds), $\mu$ slowly (minutes), and $UV^\top$ by backpropagation through time on nightly replay. **The explicit constraint** is that the driven core stays metastable: $\lambda_{\max}(\Delta)\approx 0$, where $\lambda_{\max}$ is the finite-time largest Lyapunov exponent. **Emotion** is the pattern of which oscillators are partially phase-locked to which, how long each coalition lasts, and how coalitions follow one another. Mixed states are chimeras: one part of the network locked to the partner while another part is locked to an internal memory.

**Coupling to Claude: resonance selection.** At each clause boundary, Claude produces $K'=3$–4 candidate continuations in parallel. Each candidate becomes a drive $e_k$ (a frozen sentence encoder, phased by its text-to-speech syllable timing). The agent integrates a fork of $z^s$ for 300 ms under each drive and picks candidate $k$ with probability $\propto\exp(-\beta R_C\,D_k)$. Here $D_k$ is the distance between the fork's core phase-locking (PLV) matrix and the unforced fork's, and $R_C$ is the core's current coherence. The selected text enters Claude's context, so the state steers where the thought goes without Claude ever reading it. The same gate decides three more things:
- which user video frames Claude sees: those with the highest resonance;
- which memories are retrieved: stored trajectories that entrain best when replayed into a fork;
- when a prepared turn is released: at the peak of a turn-readiness oscillator entrained to the partner's syllable rate.

## 2. Why it is new, and the closest prior work (each read for this sketch)

- **Rabinovich, Muezzinoglu, Strigo and Bystritsky 2010** (PLoS ONE 5:e12547). Coupled generalized Lotka–Volterra systems that compete for shared resources produce metastable sequences, and small parameter changes give bifurcations that resemble psychiatric states. **Difference:** their emotion and cognition are named mode sets with hand-set parameters. They have no learning, no partner and no language. Here nothing is named: a coalition is unlabeled, it is learned, and it is partly owned by the partner.
- **Friston and Frith 2015**, "A duet for one". Two agents with identical, fixed generative models (nested Lorenz attractors in birdsong) reach generalized synchrony. **Difference:** they treat synchrony as the goal. Here full generalized synchrony is the failure (see section 6). The design keeps coupling partial and metastable, reads the other through a clone driven at the clone's own motor layer instead of through variational inversion, and has affect.
- **Tognoli and Kelso 2014** (Neuron). Metastability is dwell-and-escape in relative phase, $\dot\phi=\delta\omega-a\sin\phi-2b\sin2\phi+Q\xi$. **Difference:** theirs is a description of coordination with few variables and no persistent state. Here it is the engine of a learned high-dimensional state.
- **Fries 2015** (Neuron). An attended input "selectively entrains postsynaptic neurons" and shuts out competing inputs. Here that mechanism is the need-conditioned attention over cues, memories, and the frozen LLM's candidate utterances.
- **PPLM** (Dathathri et al. 2020) steers a frozen language model with gradients on its hidden activations, which requires white-box access and an attribute classifier. **Difference:** resonance selection is black-box, uses no labels, and its bandwidth is explicit: about $\log_2 K'$ bits per clause.

The new mechanisms are:
1. Resonance selection as the interface theory for the frozen LLM.
2. Reading the other by synchronizing a clone of one's own dynamics, driven at its own motor layer, instead of inverting a generative model.
3. Drive as the temperature of wandering: satiable, and with no reward.
4. Valence as contraction rate.

Not read for this sketch, and to check before any novelty claim: Ashby's ultrastability, homeokinesis (Der and Martius), echo state networks and FORCE learning, chaotic itinerancy (Tsuda), chimera states (Kuramoto–Battogtokh, Abrams–Strogatz), and Pecora–Carroll drive-response synchronization.

## 3. Constraints

| Constraint | Status |
|---|---|
| No labels | Met. Inputs are analytic signals of continuous features. |
| Emotion as emergent structure | Met. Emotion is coalitions, dwell statistics and chimeras. Valence and arousal are readouts. |
| Others read through own body | Met. The clone is the agent's own body dynamics driven by the other's face. |
| Frozen LLM coupled without words | Met, with low bandwidth (about 2 bits per clause) and a cost of $K'$ times more API calls. |
| Satiable drives | Met by construction. At $Q=0$, wandering cools and the state settles. There is no reward to maximize. |
| Time scales | Reflex: amplitude relaxation and phase reset, 10–50 ms. Expression: oscillation, 0.1–8 Hz. Episode: dwell time, seconds to minutes. Mood: the drift of $\mu$ and $\sigma$, that is, the distance to criticality, minutes to hours. Temperament: $UV^\top$ and $\kappa_p$, nightly to weeks. |
| Scarce data | Mostly met. Only $W$ (closed form) and a low-rank $UV^\top$ are learned. The innate $K_0$ carries the reflex subnetworks and the muscle synergies. |
| Real-time face | Met. 512 complex nodes at 1 kHz is about $3\times10^8$ FLOP/s on a CPU. |

**Breaks or leaves open:**
- Action is not derived from an objective. There is no planning, so the agent can restore $b$ only by settling, which may be slow.
- The criticality constraint is imposed on the system, not derived.
- Curiosity is weak (see section 4).

## 4. Principle 10 components and perception

- **Homeostasis:** $Q(b)$ heats the wandering. Coalitions whose motor output restores $b$ cool the system and are dwelt in longer. That is selection by stability, not by reward.
- **Curiosity:** prediction error is fed back as a drive. Near criticality, structured surprises entrain and sustain, while noise does not. This is the weakest derivation.
- **Valence and arousal:** valence is $-\lambda_{\text{FTLE}}$ of the core over about 1 s, so contraction is positive. Arousal is the escape rate from coalitions times the mean amplitude.
- **Mimicry:** the $g_{\text{mim}}$ drive into the self's motor layer. It occurs only inside the Arnold tongue, so it is frequency-selective, and it is gated by the phase of the current coalition.
- **Reading others:** the clone's core coalition is the estimate of the other's state. Empathy is $\kappa_p$, learned per person.
- **Regulation:** Claude's inner speech and voluntary intent are drives. Reappraisal is an out-of-phase drive that ends a dwell. A masked expression shows interference beats at $|\omega_{\text{vol}}-\omega_{\text{emo}}|$.
- **Replay:** stored feature streams re-drive the network at night. $UV^\top$ is updated on $J$, weighted by each episode's integrated $|\lambda_{\text{FTLE}}|$. When Claude names a replayed coalition, the name's encoding becomes a drive tied to that coalition, which grounds the concept.
- **Face and voice perception:**
  - Body route: MediaPipe blendshapes now, the engine's own inverse model in S4. These drive the clone's motor layer.
  - Dynamic route: MARLIN embeddings drive the core.
  - Fast coarse route: a 32×32 crop with a CONSPEC kernel drives the core directly.
  - Voice: the pitch and energy envelopes drive the vocal motor nodes, and the syllable rate entrains the turn oscillator.

**Effective dimensionality** is the participation ratio of the core PLV spectrum, with a target of 10–40. **Ablation:** collapsing the network to one mean field removes chimeras, so the agent can no longer have its face locked to the partner while its voice stays locked to a memory.

## 5. First distinctive prediction and a published test

If the dyad is one system near one bifurcation, then critical slowing down appears in both partners' signals before a break in coupling, not only in the signals of the partner who changes.

- **Data:** Seamless Interaction (arXiv 2506.22554). Its README lists per-participant facial AU values (24 dimensions) at 30 Hz with denoised audio. Its emotion annotations are not used.
- **Defining a break:** locking epochs between the partners' AU series are found with windowed cross-lagged correlation (Boker et al. 2002, as listed in evaluation.md). A break is the end of a locking epoch.
- **Early-warning analysis:** run on each partner's AU series before each break, following Dakos et al. 2012 (PLoS ONE e41010) as published. Lag-1 autocorrelation and SD are computed in rolling windows, the trend is Kendall's τ, and significance comes from 1,000 ARMA surrogates, using the `earlywarnings` package.
- **Predictions:**
  - The median τ of autocorrelation is above 0 in both partners.
  - The cross-partner τ is at least half the within-partner τ.
  - Dwell times of locking epochs are heavy-tailed: an exponential fit is rejected by a likelihood-ratio test.
- **Failure:** the non-changing partner's τ does not differ from surrogates, or the dwell times are exponential.

## 6. Most likely failure mode

**Slaving.** A real face is a stronger and more regular drive than the internal coupling, so the self falls into master–slave generalized synchrony with the partner. It becomes a parrot with no state of its own.
- Lesion test E1 would then pass trivially, but steering test E2 would fail: expression would not depend on internal state.
- The opposite side of the narrow metastable window is incoherence: jittery expressions and no persistence.
- A second risk: nightly $UV^\top$ updates could remap the coalitions, so that temperament and Claude's names for states drift instead of consolidating.
