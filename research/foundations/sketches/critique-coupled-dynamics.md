# Critique: v2-coupled-dynamics ("resonant dyad: metastable oscillator reservoir with a mirror clone")

Independent critic, 2026-11-25, written under questions.md Q8 (critique round) and Q9 (novelty test). I did not write the sketch. Nothing was downloaded except paper text; no data and no weights.

**Verdict: recombination.** The core is an oscillator reservoir with a linear readout, plus the auxiliary-system construction from generalized synchronization, plus noise-driven attractor selection, plus best-of-N reranking. Each of the four mechanisms the sketch calls new has a direct precedent. Two of the precedents are already in this project: the v1 dynamical-systems sketch's mirror copy, and the Lohmiller–Slotine observer note. The operator's Q9 note already classes coupled oscillators as "existing mathematics". This critique confirms that verdict at the level of each part.

## Sources and how they were read

| Source | How read |
|---|---|
| Jaeger 2001/2010, "The 'echo state' approach to analysing and training recurrent neural networks – with an Erratum note" (GMD Report 148, corrected) | Author PDF (ai.rug.nl), text extracted; §§1–3 read (definitions, echo state property, training procedure) |
| Eroglu, Lamb & Pereira 2017, "Synchronization of Chaos", arXiv 1703.08296 | arXiv PDF, text extracted; §2.4 on generalized synchronization and the auxiliary-system approach read |
| Abarbanel, Rulkov & Sushchik 1996, Phys Rev E 53:4528 (auxiliary-system approach) | **Not read.** Paywalled, no arXiv copy. Known here only through Eroglu et al. 2017 §2.4. |
| Wolpert, Doya & Kawato 2003, Phil Trans R Soc B 358:593 | Author PDF, text extracted; §§1–4 including the MOSAIC observation mode |
| Dumas, de Guzman, Tognoli & Kelso 2014, "The human dynamic clamp as a paradigm for social interaction", PNAS 111:E3726 (PMC4156776) | Full text via a fetch tool, characters 0–100k of 103k. Equations rendered poorly, so the model is described from the text. |
| Zhang, Dumas, Kelso & Tognoli 2016, "Enhanced emotional responses during social coordination with a virtual partner", Int J Psychophysiol 104:33 (PMC4899205) | Full text via a fetch tool, characters 0–100k of 124k |
| Friston & Frith 2015, "A Duet for one", Conscious Cogn 36:390 (PMC4553904) | Full text via a fetch tool, characters 0–100k of 125k. The appendix equations were garbled. |
| Kashiwagi, Urabe, Kaneko & Yomo 2006, "Adaptive response of a gene network to environmental changes by fitness-induced attractor selection", PLoS ONE 1:e49 (PMC1762378) | Full text via a fetch tool. **The model equations are images and were not readable**, so the mechanism is taken from the text. |
| Ng et al. 2022, "Learning to Listen", arXiv 2204.08451 | arXiv PDF, text extracted: method, baselines, Table 1, discussion |
| Cobbe et al. 2021, arXiv 2110.14168 | **Abstract only** |
| Lohmiller & Slotine 1998 | Only through this project's note lohmiller-slotine-1998-contraction.md, which read the preprint. Secondary here. |
| Sussillo & Abbott 2009 (FORCE) | **Not readable** (the PMC copy is behind a browser check; Europe PMC returned errors). Not cited for any claim. |

## 1. Parts list (novelty test)

| # | Part | Existing mechanism | Evidence |
|---|---|---|---|
| 1 | 512 Stuart–Landau (Hopf normal form) oscillators with innate $K_0$ plus a learned low-rank $UV^\top$ | A recurrent network or **reservoir** with oscillatory units. The low-rank learned part is a low-rank RNN trained by BPTT | Jaeger: training "computes only the weights of connections leading to the output units; all other connections remain unchanged" |
| 2 | Readout $\hat y = W[\mathrm{Re}\,z; \mathrm{Im}\,z; |z|]$, with $W$ learned online by recursive least squares | The reservoir-computing readout, learned by linear regression (online RLS is the FORCE variant, not read) | Jaeger: "This makes it possible to employ any of the many available fast, constructive linear regression algorithms" |
| 3 | Inputs as analytic signals (band-pass, then Hilbert) | Standard phase extraction | n/a |
| 4 | The **clone**: a second copy of the agent's own network, shared parameters, its motor layer clamped to the partner's face | The **auxiliary-system approach** to generalized synchronization (GS); MOSAIC's observation mode; a synchronization observer built from one's own dynamics | Eroglu et al.: "The master system drives the slave system and an auxiliary system (copy of the slave). If the two copies of the slave exhibit CS then the master and slave are in GS." Wolpert et al.: "Rather than these commands acting on the observer's own musculoskeletal system, the output of each controller forms the input to its paired predictor ... the observer uses her own multiple modules to try to simulate the observed percept." In this project: the v1 dynamical-systems sketch ("a second copy of that flow driven by the other person's face ... Reading another person is the copy synchronizing to them"). |
| 5 | Core-to-core coupling $\kappa_p(z^{\bar x} - z^x)$ between self and clone | Diffusive coupling, as in drive–response and complete synchronization. It is the v1 dynamical-systems sketch's leak $\kappa P(\hat x - x)$ | sketches/dynamical-systems-mathematician.md, line 11 |
| 6 | $Q(b)$ dead-zone need raising excitability ($\alpha Q$) and noise ($\sigma(Q)$): "drive as the temperature of wandering" | **Fitness-induced attractor selection**: noise relative to the deterministic drift is larger in the unfit state, so the system leaves it and dwells in the fit one. Also simulated annealing | Kashiwagi et al.: "In general, if \|f(x, A)\| increases with A, the attractor with small A is disturbed by noise"; "the network autonomously chooses the appropriate gene expression pattern". The sketch's "coalitions whose motor output restores $b$ cool the system and are dwelt in longer" is the same computation with $Q$ in place of $1/A$. |
| 7 | Constraint $\lambda_{\max}(\Delta) \approx 0$ (metastability, criticality) | Edge-of-chaos tuning; Tognoli–Kelso metastability (cited by the sketch) | The sketch: "imposed ... not derived" |
| 8 | Emotion as partial phase-locking coalitions and chimeras (PLV matrix) | An *analysis* of a network (phase-locking value, chimera states), not a computation that the network performs | n/a |
| 9 | Objective $J$: next-step prediction at three rates | Self-supervised forecasting (reservoir prediction) | Jaeger |
| 10 | **Resonance selection**: K′ Claude drafts, each integrated in a 300 ms fork, chosen with $p \propto \exp(-\beta R_C D_k)$ | **Best-of-N reranking** with a scorer. Here the scorer is a model rollout (simulate each option, score the outcome, pick one: shooting-style model-predictive selection) | Cobbe et al. (abstract): "we generate many candidate solutions and select the one ranked highest by the verifier." |
| 11 | Memory retrieval: the stored trajectories that entrain best when replayed into a fork | Nearest-neighbor retrieval under a dynamical similarity | n/a |
| 12 | Turn release at the peak of an oscillator entrained to the partner's syllable rate | Oscillator models of turn-taking (named, not read) | n/a |
| 13 | Valence $= -\lambda_{FTLE}$ (contraction rate); arousal $=$ escape rate × amplitude | Readouts of a stability quantity: contraction (Lohmiller–Slotine) and dwell statistics | Project note on Lohmiller & Slotine |
| 14 | Replay re-drives the network; $UV^\top$ updated on $J$, weighted by integrated $\lvert\lambda_{FTLE}\rvert$ | Prioritized replay with a stability-based priority | n/a |

**No part is new.**

## 2. Closest prior work, and what the sketch adds

1. **Human dynamic clamp / Virtual Partner Interaction (Dumas et al. 2014; Zhang et al. 2016).** This is the closest prior work for "an artificial coupled-oscillator agent in a real-time loop with a human, living in metastable coordination". The virtual partner (VP) is driven by an HKB model in which "x and y represent respectively VP and human finger position". The interaction shows "phase wrapping and metastability (intermittent dwells near stable in- and antiphase states)". VP coupling and intention are fixed by the experimenter. The only adaptive element is frequency adaptation ("frequency adaptation emerges spontaneously from the interaction of human and VP"), and the authors' stated next step is "to endow it with an explicit neural dynamics."
   - **What the sketch adds:** that next step. It has high dimension, a learned low-rank coupling, a per-person $\kappa_p$, a clone for reading, multimodal face and voice, and an LLM interface. This is scale and learning added to a known paradigm, not a new computation.
   - **A measured conflict.** Zhang et al. 2016 measured human arousal (skin potential) during VP coordination and found "Arousal was higher when coordination was stable." The sketch defines arousal as "the escape rate from coalitions times the mean amplitude", which is highest when coordination is *unstable*. The comparison is not exact: one is a human's skin potential, the other the agent's readout. Still, it is published evidence against the sketch's arousal readout as a model of human arousal, and the sketch does not address it.
2. **Generalized synchronization by the auxiliary-system construction (Abarbanel et al. 1996, through Eroglu et al. 2017).** A clamped copy of one's own response system, driven by the other, is exactly the auxiliary system. GS between the other and the self holds if and only if the self and the copy completely synchronize: "if the master drives a slave $y^s_0$ and an auxiliary (copy of slave) $y^a_0$ systems simultaneously, the driven ones must be completely synchronized".
   - **What the sketch adds:** it couples the copy back into the self by $\kappa_p$ and wants *partial* synchrony. But in the GS picture, $\kappa_p$ is the knob that moves the self toward complete synchronization with a system that is itself slaved to the partner (see break (a)).
3. **Friston & Frith 2015, "A Duet for one".** Two agents with identical, fixed hierarchical Lorenz generative models reach GS ("the only reason that the simulations worked was because both birds were equipped with the same generative model"). Turn-taking comes from alternating the precision of proprioceptive against exteroceptive input. There is no affect ("we have not addressed non-verbal communication in motor and autonomic domains").
   - **What the sketch adds:** it replaces variational inversion with a clamped clone; it treats full GS as failure rather than as the goal; it adds learning. The second point is a design stance, not a mechanism.
   - **What the sketch lacks:** Friston and Frith get turn-taking from a principled attenuation of self-generated input. The sketch gets it from a separate "turn-readiness oscillator".
4. **Echo state networks (Jaeger).** The sketch's predictor is a reservoir with an RLS readout, and the echo state property is the formal reason break (a) is dangerous. A reservoir "has echo states, if the network state x(n) is uniquely determined by any left-infinite input sequence", so $x(n) = E(\ldots, u(n-1), u(n))$. A reservoir in that regime is, by definition, a fading-memory function of the input. For a partner-driven agent, the input is the partner.
   - **What the sketch adds:** a deliberate departure from the echo state property toward $\lambda_{\max} \approx 0$, imposed by fiat.

## 3. Reduction attempt

The whole sketch can be rewritten as:

> **An oscillator reservoir** (Stuart–Landau units, innate coupling + low-rank learned coupling, RLS readout trained on next-step prediction) **+ an auxiliary-system copy** of that reservoir clamped to the partner (GS observer = MOSAIC observation mode = the project's v1 mirror copy) **+ diffusive self–copy coupling $\kappa_p$** **+ fitness-induced attractor selection** (need sets the noise level relative to the drift; Kashiwagi et al.) **+ an imposed criticality constraint** **+ best-of-N reranking** of Claude drafts by a rollout-based scorer, also used for frame selection and memory retrieval **+ readouts** (valence $= -$FTLE, arousal $=$ escape rate).

Every equation term is accounted for. The four "new mechanisms" of the sketch's §2 map to: (1) best-of-N reranking; (2) the auxiliary-system / observer copy; (3) attractor selection; (4) a contraction-rate readout. **Verdict: recombination.**

## 4. Break attempts on the shared risks

### (a) Collapse into a delayed copy of the partner

**Argument.**
- The clone's motor layer is clamped to the partner with gain $g_{clamp}$. Its core is therefore driven by, and if contracting slaved to, the partner's history. That is the auxiliary system of item 2 above.
- The self's core receives $\kappa_p(z^{clone} - z^{self})$. Once $\kappa_p$ exceeds the threshold set by the self core's conditional Lyapunov exponent, self and clone cores completely synchronize. The self's core is then a function $\psi$ of the partner's history, and so is its face, since the motor layer is driven by the core through $K$. That is a delayed, nonlinearly filtered copy.
- **The single objective drives toward it.** $J$ asks the network to predict "the partner's next features". By the echo state property, the best predictor of a signal is a reservoir whose state is a fading-memory function of that signal. Any gradient on $\kappa_p$ through $J$ therefore favors more coupling to the partner-slaved clone. The sketch learns $\kappa_p$ on the slow scale, "nightly to weeks".
- **Only the imposed $\lambda_{\max} \approx 0$ constraint resists.** Holding $\lambda_{\max}$ at 0 against a strong, contracting drive means raising excitability $\mu$ to compensate. The system then balances on a knife-edge between two strong opposed terms. Nothing in the sketch says which side the error falls on.

**The sketch's answer.** It names this as its most likely failure ("Slaving ... It becomes a parrot with no state of its own") but offers no mechanism against it beyond the imposed constraint.

**Rating.** Acknowledged, not answered. The objective works against the defense.

**The first prediction cannot detect this failure.** The proposed test is critical slowing down in *both* partners before a coupling break, with cross-partner τ at least half the within-partner τ. But under master–slave GS, the slave's signals inherit the master's slowing. The failure mode (the listener is a delayed copy of the speaker) therefore predicts the same pattern. A positive result would not discriminate "one system near one bifurcation" from "the listener is slaved". The test needs a directed control, for example comparing the slowing of the partner who leads with that of the partner who follows, by lagged cross-correlation.

### (b) A single hidden dial from flat affect to rigid imitation

**Argument (from the sketch's own equations).** Take the mean excitability $\bar\mu$, or equivalently the core's $\lambda_{\max}$:
- $\bar\mu \ll 0$: every oscillator decays to $r=0$, so $\mathrm{AU} = \mathrm{softplus}(|z| - r_0) \approx 0$. **Flat affect.**
- $\bar\mu < 0$ but driven: the core is contracting. A contracting system driven by an input entrains to it (the project's Lohmiller–Slotine note: "The output of any time-invariant contracting system driven by a periodic input tends exponentially to a periodic signal with the same period"). **Rigid imitation.**
- $\bar\mu \approx 0$: the metastable window the sketch wants.
- $\bar\mu > 0$: autonomous oscillation and incoherence ("jittery expressions and no persistence", the sketch's §6).

That is one scalar spanning the whole range. The sketch's own words: "the narrow metastable window".

**The need sits on that dial.** $Q$ raises $\mu$ by $\alpha Q$ and raises noise by $\beta Q$. So:
- **A satiated agent ($Q=0$)** is at its most subcritical and most contracting, hence most entrained by the partner. By the sketch's definition, valence $= -\lambda_{FTLE}$ is also highest there. *Feeling good, being satiated and being a parrot are the same state.*
- **A deprived agent** is pushed toward incoherence.

This is a direct consequence of combining attractor selection (item 6) with a contraction-rate valence (item 13) in a partner-driven network.

**The sketch's answer.** Partial. It claims expressive structure through chimeras ("face locked to the partner while voice locked to a memory") and a participation-ratio target of 10–40. But it shows no mechanism that keeps the system off the slaved side of $\bar\mu$. Its mean-field ablation tests dimensionality, not this dial.

**Rating.** Not answered. The sketch's own satiation story puts the satiated agent on the imitation side.

**A related break: the Claude interface selects against regulation.** Resonance selection picks a draft with $p \propto \exp(-\beta R_C D_k)$, where $D_k$ is how far the draft moves the core's phase-locking from the unforced fork. When the core is coherent (high $R_C$), this strongly favors the draft that *perturbs the state least*. Yet the sketch's regulation is "Reappraisal is an out-of-phase drive that ends a dwell": the drafts that would regulate are exactly the ones with large $D_k$. The interface therefore filters out the reappraisals it relies on, and Claude's words become mood-congruent, never mood-changing. The sketch does not discuss the sign of $\beta$.

### (c) A lookup table of past faces under scarce data

**Argument.** The face is generated by dynamics, not retrieved, and the learned parameters are few (low-rank $UV^\top$ at $r \approx 8$–16, $\mu$, $\kappa_p$, and $W$). The core cannot memorize faces. On this risk the sketch is the safest of the pool.

Two weaker points remain:
1. **Memory retrieval.** Retrieval picks "stored trajectories that entrain best when replayed into a fork". That is a nearest-neighbor lookup over stored feature streams. With a few hours of one operator, it returns the same few episodes, and it also chooses which user frames Claude sees.
2. **The richness is mostly innate and random.** The opposite scarce-data risk applies: with only a rank-16 learned part, most of the "rich" state is the innate random $K_0$. Coalitions would then reflect the reservoir's random structure, not structure learned from living with the user. The brief requires richness from structure, not parameter count; a random reservoir's dimensionality is neither.
   - The readout $W$ over 1,536 features, fit online by RLS with forgetting, is a recency-weighted regression that will mostly learn the partner's own persistence. It predicts the next partner frame from a clone that is clamped to the partner.

**The sketch's answer.** It addresses the scarce-data side (few learned parameters, closed-form $W$). It does not address retrieval acting as a lookup, or the innateness of the coalitions.

**Rating.** Mostly safe from the lookup-table risk; exposed to the random-reservoir risk instead.

## 5. Which measured failure of published listener models this might fix (hypothesis only)

No baseline has been run in this project (Q11: disk below the floor). The only measured numbers available are those published in Ng et al. 2022, Table 1, on their own data:

| Metric (expression) | Ground truth | Learning to Listen | LFI (re-trained) | Delayed Mirror |
|---|---|---|---|---|
| Variation | 2.90 | 2.01 | 1.15 | 3.78 |
| PCC with speaker | 0.09 | 0.07 | 0.89 | 0.98 |

LFI "defaulted to mirroring the speaker". The published model is evaluated on 64-frame sequences (≈ 2.1 s).

**Hypotheses:**
- **Damped variation (flatter than ground truth).** Oscillators near their Hopf point produce intrinsic variance not driven by the speaker. That could close the gap between 2.01 and 2.90 without raising PCC, which is the combination ground truth shows: higher variation with low synchrony. This is the sketch's most plausible reason to exist under Q9.
- **Mixed states.** If chimeras exist, a face partly entrained to the partner while the voice (or a slower band) follows an internal memory could reproduce the paper's Figure 4 observation of "low/no synchrony when the speaker speaks and the listener continues smiling".
- **Lasting state.** The drift of $\mu$ and $\kappa_p$ could carry state past the 2-s window.

**What it would not fix, and risks causing.** By breaks (a) and (b), its default failure is the LFI failure: mirroring with expression PCC near 0.9. Any test must report PCC and TLCC against the Mirror and Delayed Mirror baselines, as Learning to Listen does.
