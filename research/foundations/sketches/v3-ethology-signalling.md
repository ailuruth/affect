# v3 sketch, ethology and signalling lens: the release-reserve display process (RRDP)

Author lens: ethology and animal signalling (ritualization, typical intensity, releasers and action-specific exhaustion, conflict and displacement, play meta-signals, rapid facial mimicry in primates). Written in isolation from the other sketches, 2026-11-25. No data or weights downloaded.

## 0. The ethological diagnosis of the "one dial" failure

Every earlier design passes the partner's face into the agent's face through a continuous map, then scales it with one gain. Animals do not couple displays that way. Four classic observations point to a different structure:
- **Releasers set *when* and *which*, not *how*.** A sign stimulus triggers a stereotyped motor pattern; the stimulus does not shape it.
- **Typical intensity.** Morris (1957) proposed that ritualized displays keep about the same form and amplitude over a wide range of motivation. Motivation shows in how often a display occurs, not in its size.
- **Action-specific exhaustion versus stimulus-specific habituation.** Ethologists separate two things. A motor pattern that has just been performed is harder to release again, whatever releases it. A stimulus that keeps repeating loses its effect, whatever response it drew. Lorenz's "action-specific energy" and the later habituation literature (Hinde) correspond to these two.
- **Conflict produces a third behaviour, not a blend.** When two incompatible tendencies are both strong, an apparently irrelevant act appears: Tinbergen's displacement activities, explained either by "spark-over" or by van Iersel and Bol's disinhibition.

Primate rapid facial mimicry (RFM) fits this pattern. It is specific to some displays, depends on the relationship, and is fast. Mancini, Ferrari and Palagi (2013, read in full) found that geladas "mimicked play faces (PF/PF; FPF/FPF) ... but not lip-smacking (LS)", and that "the mother-infant dyads showed the highest level of RFM and the fastest responses".

Krebs and Dawkins (1984) cast the receiver as a *mind-reader*: it predicts what the actor will do next from intention movements, the first parts of motor patterns. On that view, reacting to a partner means reacting to the partner's *predicted next act*. It does not mean replaying the partner's current form.

The mechanism below makes these four observations into constraints on one generative process.

## 1. Mechanism

**Time and spaces.** Frames run at 30 Hz with step Δ = 1/30 s. The agent's body output is $a_t\in\mathbb R^{D}$, where D = 24 AU intensities plus V vocal channels: speech on, short backchannel token, laugh token if transcribed. The partner's perceived features are $o_t\in\mathbb R^{D}$, built the same way from their AUs, VAD and word timestamps. $q_t$ holds turn features derived from both VAD streams.

**Repertoire (the innate, "phylogenetically ritualized" body).** The repertoire is K stereotyped display units $\phi_k\in\mathbb R^{L_k\times D}$, with K ≈ 48 and $L_k$ from 0.3 to 2 s. They are learned once by convolutional factorization (seqNMF or convolutional sparse coding) on the AU and vocal streams of the training people, then frozen. A unit is a motor pattern, not a past response.

**State** $h_t=(r_t, z_t, f_t, m_t;\ \psi^p,\eta^p)$:
- reserves $r_t\in[0,1]^K$ (action-specific);
- partner-parse traces $z_t\in\mathbb R^{K\times 3}$ at time constants 0.2, 1 and 5 s;
- frame $f_t\in\Delta^{F}$, with F ≈ 4 (meta-communicative context);
- slow state $m_t\in\mathbb R^{64}$, a diagonal state-space model with time constants from 1 s to hours;
- per partner p, stored across sessions: a perceptual deformation $\psi^p$ and stimulus habituation $\eta^p\in(0,1]^K$.

**(1) Reading the partner through the agent's own body (intention-movement parse).** The parse compares the partner's last P = 6 frames (200 ms) with the *onset prefix* of each of the agent's own units, deformed by $\Pi^p=I+U_pV_p^\top$ (rank 2):
$$e_{j,t}=\sigma\!\Big(\beta\big[\cos(\Pi^p\phi_j[0{:}P],\ o_{t-P+1:t})-\theta_j\big]\Big),\qquad z^{(\tau)}_{j,t+1}=z^{(\tau)}_{j,t}+\tfrac{\Delta}{\tau}\big(\eta^p_{j,t}\,e_{j,t}-z^{(\tau)}_{j,t}\big).$$
The agent therefore perceives the partner only as "the beginning of something *I* can do". The vocabulary is its own, and the parse is predictive, because a prefix comes before the display completes.

**(2) Drive.**
$$u_{k,t}=b_k+w_k^\top m_t+\sum_{j,\tau}R^{(\tau)}_{kj}(f_t)\,z^{(\tau)}_{j,t}+c_k^\top q_t-\sum_{l\in\mathrm{Inc}(k)}I_{kl}\,n_{l,t}+v_k\,\chi_t ,$$
where:
- $R(f)=\sum_\varphi f_\varphi R^{\varphi}$ is the release map (low rank, one per frame);
- $n_{l,t}$ is how much of own unit l is currently playing;
- $\mathrm{Inc}$ pairs units with antagonistic AUs (for example LipCornerPuller and LipCornerDepressor, or Inner/OuterBrowRaiser and BrowLowerer) and is fixed from anatomy;
- $\chi_t$ is the **conflict term** (Tinbergen/van Iersel–Bol):
$$\chi_t=\sum_{(k,l)\in\mathrm{Inc}}\min\big(\sigma(u^{0}_{k,t}),\sigma(u^{0}_{l,t})\big)\,r_{k,t}\,r_{l,t}\qquad(u^0=u\text{ without the }\chi\text{ and } I \text{ terms}),$$
which is large only when two incompatible units are *both* driven and *both* charged.

The loadings $v_k\ge 0$ are learned. Which units become displacement units is therefore emergent, not named.

**(3) Hazard, gated by the reserve.**
$$\lambda_{k,t}=\frac{(r_{k,t}-\kappa_k)_+}{1-\kappa_k}\cdot\mathrm{softplus}(u_{k,t}),\qquad \Pr[\text{unit }k\text{ starts at }t]=1-e^{-\lambda_{k,t}\Delta}.$$

**(4) Consumption and refill.** This is Lorenz's reservoir: each act uses a fixed quantum, and the reserve refills toward full. Tsodyks–Markram depletion is the neural analogue.
$$r_{k,t+\Delta}=r_{k,t}+\Delta\,\rho_k(m_t)\,(1-r_{k,t})-\kappa_k\,\mathbb 1[k\text{ starts at }t],\qquad 0<\kappa_k<1,\ \rho_k(m)>0 .$$
By mass balance, a unit's mean rate can never exceed $\rho_k/\kappa_k$, whatever drives it.

**(5) Expression with typical intensity.**
$$a_t=A\,m_t+\sum_{(k,s):\,0\le t-s<L_k}\gamma_k\,(1+\xi_s)\,\phi_k[t-s],\qquad |\xi_s|\le\varepsilon\ (\varepsilon\approx0.15).$$
Drive changes rate and selection. It barely changes amplitude, and it never changes form. The tonic term $A m_t$ is a slow posture, for example brow tone, and does not depend on the partner.

**(6) Frames (play meta-communication, Bateson 1955; Bekoff).** Specific *partner* units switch frames, and frames decay:
$$f_{t+\Delta}=\mathrm{softmax}\big((1-\Delta/\tau_f)\log f_t+\Delta\,G\,e_t\big).$$
A frame does not change what is recognized ($e$). It changes what a recognized unit *releases* ($R^\varphi$). This is the computational form of "the nip denotes the bite, but not what the bite denotes". Which units act as meta-signals is learned (sparse $G$).

**(7) Slow state.**
$$m_{t+\Delta}=\Lambda m_t+B\,[\text{own onsets},\ e_t,\ \chi_t,\ r_t,\ q_t,\ \text{word-end text embedding},\ \text{body variables}]$$
with a pointwise nonlinearity. Homeostatic body variables are at most one input here.

**Learning.**
- *Population stage* (the stand-in for evolution, where ritualization happens). One objective: the log-likelihood of each training person's unit onsets and AU residual, given their own history and the partner's observed stream, $\mathcal L=\sum_{t,k}\log\Pr(y_{k,t}\mid h_t)+\log\mathcal N(a_t-\hat a_t;0,\sigma^2)$. Parameters: $b,w,R^\varphi,c,I,v,\kappa,\rho(\cdot),G,\Lambda,B,A,\gamma$.
- *Living stage* (one user). Only two things adapt. $\psi^p$ is fitted so that one's own templates reconstruct *the partner's* displays (it uses only the partner's face). $\eta^p$ follows a fixed two-time-scale habituation rule, $\eta_j\leftarrow\eta_j+\Delta[(1-\eta_j)/\tau_{\rm rec}-\alpha\,\eta_j e_j]$, driven only by partner stimuli.
- Nothing learned in living takes the agent's own expression as input, and nothing has the partner's response as a target. There is no reward term anywhere. This meets Principle 6 and D66 by construction.

**What it computes.** A marked multivariate point process over the agent's own stereotyped displays. The partner can change *which* display starts and *when*, through a parse in the agent's own motor vocabulary. The agent's state decides *whether it has anything left to give* (reserves), and *what shape and size* the display takes (own templates at typical intensity).

## 2. Novelty test, honestly

| Part | Existing mechanism it is |
|---|---|
| Unit dictionary $\phi_k$ | Convolutional sparse coding / seqNMF (Mackevicius et al. 2019); close to the VQ motion codebook of Learning to Listen (Ng et al. 2022) |
| Expression as a sum of templates at fixed gain | Shot-noise / marked point process with a stereotyped kernel |
| Prefix parse by own templates | Matched filtering; attention with keys = template prefixes; mirror/simulation models (Wolpert, Doya and Kawato 2003, MOSAIC) |
| Hazards with partner cross-terms | Multivariate (nonlinear) Hawkes process; coupled point-process GLM (Pillow et al. 2008); dyadic Hawkes (Halpin and De Boeck 2013) |
| Multiplicative reserve with consumption and refill | Tsodyks–Markram short-term depression; spike-frequency adaptation; Lorenz's 1950 psychohydraulic model as concept |
| Mutual inhibition among incompatible units | Lateral inhibition / winner-take-all action selection (Redgrave, Prescott and Gurney 1999) |
| Conflict term $\min(\cdot,\cdot)$ routed to a third output | Conjunctive feature plus gating; ethology's disinhibition hypothesis (van Iersel and Bol 1958) as concept |
| Frames switching the release map | Regime-switching / Markov-modulated point process; mixture-of-experts gating |
| Per-partner $\psi^p$ | Speaker adaptation (low-rank, MLLR-like); fast-weight adaptation |
| $\eta^p$ | Multi-time-scale habituation (Staddon and Higa 1996) |
| $m$ | Diagonal SSM / RNN |

**Closest prior work.**
- *ML, read in full (Sec. 1–5 and 6.1–6.2; appendices not read): Mei and Eisner 2017, "The Neural Hawkes Process" (arXiv 1612.09328).*
  - The model "allows past events to influence the future in complex and realistic ways, by conditioning future event intensities on the hidden state of a recurrent neural network that has consumed the stream of past events".
  - It targets exactly the effects used here: "Past events may now either excite or inhibit future events". Also: "The combined effect of past events on future events can now be superadditive, subadditive, or even subtractive."
  - A continuous-time LSTM can represent reserve depletion, partner cross-excitation, conflict conjunctions and frame switching. **Every intensity function the RRDP defines is inside the neural Hawkes family.** No *computation* here is missing from it.
  - What Mei and Eisner do not have is a set of *constraints*:
    - (i) a separate multiplicative reserve whose refill flux caps each unit's rate;
    - (ii) marks with fixed own-template form and near-constant gain (their events carry no motor form at all);
    - (iii) the partner entering only through a parse in the agent's own template prefixes.
- *Dyadic event modelling:* Halpin and De Boeck 2013, "Modelling dyadic interaction with Hawkes processes" (Psychometrika 78:793–814). **Only the abstract and index records were available; not read in full.** Per those records, its worked example is workplace email.
- *Ethology, read in full:* Mancini, Ferrari and Palagi 2013 (Sci Rep 3:1527).
  - RFM is defined as a congruent response "within 1 sec from the emission of the facial stimulus".
  - Note the design: "we considered only those interactions in which the observer ... did not show any facial expression in the 1 s prior to the trigger's stimulus". So the paper excludes, by design, the own-history dependence that the reserve predicts. Prediction H1 below is the test it did not run.
- *Human dyads, methods read:* El Haddad, Nallan Chakravarthula and Kennedy (ICMI 2019). Mimicry is counted when B starts after A starts and before $\min\{T_{stop}(A_i)+\Delta T,\ T_{start}(A_{i+1})\}$. They report that "laughs are mostly mimicked by laughs and not by smiles". This is a descriptive probability, not a generative mechanism.
- *Not read in primary source (paywalled or book chapters; known only from secondary summaries):*
  - Lorenz 1950; Tinbergen 1952 ("Derived activities"); Morris 1957 ("Typical intensity", Behaviour 11:1–12); van Iersel and Bol 1958;
  - Krebs and Dawkins 1984 (in Krebs and Davies, *Behavioural Ecology*, 380–402); Bateson 1955;
  - Tsodyks and Markram 1997 (PNAS returned 403). The reserve equation is written from the standard form, not checked against the paper.

These sources are conceptual inputs, and none of them is a computational model of a face. Before any claim, they must be read.

**Verdict: recombination.** The RRDP is a constrained neural/nonlinear Hawkes process: a coupled point-process GLM with depressing self-gates, a template dictionary, gated release maps and habituation. Its components are existing mechanisms, and so is the whole. The only thing that might be its own is a *property, not a computation*: the constraints give a parameter-independent bound that rules out both copy and flatness (Sec. 3). The unconstrained neural Hawkes process does not have that bound. Under Q9's rule it is a recombination baseline, not a core.

## 3. The three shared risks

**(b) Is the partner's share a single dial? It is not. Here is why, in algebra.** Take one unit k with partner-independent drive $g_0=\mathrm{softplus}(b_k+w_k^\top m)$ and partner drive $g_p\ge0$. Scale every partner term by a gain G, which is the dial a critic would look for. Under (3)–(4), at mean-field steady state with constant drive $g=g_0+Gg_p$, refill balances use: $\rho(1-r^*)=\kappa\nu$ and $\nu=g\,(r^*-\kappa)/(1-\kappa)$. Writing $\tilde\kappa=\kappa/(1-\kappa)$, the unit's rate is
$$\nu_k(G)=\frac{\rho_k\,g}{\rho_k+\tilde\kappa_k\,g}\ \xrightarrow[G\to\infty]{}\ \frac{\rho_k}{\tilde\kappa_k},\qquad \nu_k(0)=\frac{\rho_k g_0}{\rho_k+\tilde\kappa_k g_0}>0 .$$

*The flat end cannot be reached.* At G = 0 every unit still fires at $\nu_k(0)>0$: vacuum activity, set by own state through $g_0(m)$ and $\rho(m)$.

*The rigid-imitation end cannot be reached, in three ways.*
- *Rate.* The share of unit k's events caused by the partner is $S_k(G)=1-\nu_k(0)/\nu_k(G)$. Its supremum is $S_k^{\max}=\rho_k/(\rho_k+\tilde\kappa_k g_0)<1$. If the partner shows unit j at rate $\nu_p>\rho_k/\tilde\kappa_k$, at most $\rho_k/(\tilde\kappa_k\nu_p)$ of those displays can be answered.
- *Form.* Whatever G is, the output lies in the span of own templates at gain $\gamma_k(1\pm\varepsilon)$. The partner's amplitude and idiosyncratic shape never reach $a_t$, so the concordance with the partner is bounded by template match quality. It does not tend to 1.
- *Content.* G scales every entry of $R$. Turning it up makes the agent more *responsive*, which includes complementary releases (a nod or backchannel when the partner speaks, a displacement unit under conflict). Only the diagonal entries amount to *copying*.

So the copy fraction is a property of the learned structure of $R(f)$, the frame $f$, the reserves $r_t$, the habituation $\eta^p$ and the familiarity $\psi^p$. It is not a property of G. The bounds $[\nu(0), \rho/\tilde\kappa]$ differ per unit and move with $m$.

*Where the argument fails.* If the fit gives $\kappa_k\to0$ (no consumption) and $b_k\to-\infty$ (no vacuum activity), the RRDP collapses into an ordinary Hawkes process, and the single dial is back. The answer to (b) is therefore an *empirical* claim about human listeners: that consumption and vacuum activity exist. H1 tests it.

**(a) Can it collapse into a delayed copy? Copying needs the agent to answer every partner event, with the partner's form and a fixed lag. The RRDP breaks all three.**
- (i) It answers at most a fraction set by the reserve, and a second display soon after the first goes unanswered (refractoriness).
- (ii) The form is its own.
- (iii) The parse fires on a 200 ms *prefix*, so the agent can start before the partner's display peaks. Its lags are spread out and can be zero or negative, not fixed at about 17 frames.

There is also an information bound. The partner reaches the output only through the onset stream, with at most $\sum_k\rho_k/\kappa_k$ events per second, each carrying $\le\log_2K$ bits for identity plus a few bits of timing. With K = 48 and a rate ceiling of about 0.5/s per unit, that is about 40 bit/s. A 24-AU copy at 30 Hz needs an order of magnitude more.

**(c) Is it a lookup table of past faces? No.**
- The templates are 0.3–2 s motor patterns shared across the population, comparable to a phoneme inventory. They are not stored responses to contexts.
- Per partner, the learned part is about 200 numbers: $\psi^p$ at rank 2, plus $\eta^p$.
- A new situation produces a new *composition* of timings and selections. Nothing retrieves a past segment by similarity, which is what Nearest Neighbour does.

A critic can fairly call $\phi$ a codebook (as in L2L). The distinction claimed here concerns only what is looked up: motor primitives, not reactions. The scaling test in H3 checks it.

## 4. Emotion as structure, reading the other, readouts

**No emotion variable.** Nothing below Claude is named.
- What an observer would call a mood is the pattern of refill rates $\rho(m)$: which displays come back quickly.
- What would be called anxiety-like is a regime where $\chi_t$ is high: two incompatible reserves are full and both driven, and the units with learned $v_k>0$ fire. Maestripieri et al. (1992, not read here) proposed displacement activities as indicators of emotion in primates. The prediction is that these units turn out to be self-directed mouth and eye units (LipPressor, LipSuck, EyesClosed bursts), named only after fitting.
- What would be called playfulness is a frame $f$ in which threat-like partner units release affiliative units.
- Valence and arousal may be read out afterwards as principal axes of the $(r,f,\chi,m)$ trajectory; they are never set.

**Reading the other through one's own body.** Perception *is* the agent's own motor vocabulary, applied to the partner's face: a prefix parse with $\psi^p$, the "how this person does my displays" deformation. Running the agent's own reserve dynamics (4) on the parsed partner events gives $\hat r^p$, an estimate of what the partner has "used up". This is simulation through one's own body, as in Yoshida and Man. Familiarity sharpens $\psi^p$, so intention movements are detected earlier. That *derives* Mancini et al.'s faster RFM with close partners, instead of assuming it.

**Face.** $a_t$ in AU space, directly.

**Voice.** Vocal units (backchannel onset, laugh onset, prosodic accents on TTS words) are units of the same process, at typical intensity.

**Claude, which never sees numbers or labels.**
- (i) Claude's spoken reply is itself a unit, "take the turn". Its onset waits for that unit's hazard, so reply latency emerges from the state.
- (ii) Each episode stores its state snapshot $(r,f,\chi)$ as a retrieval key. Past *text* exchanges from similar snapshots are offered to Claude as memories. This is mood-congruent recall, with frame-congruent examples in a play frame.
- (iii) The thinking budget and reply length follow $\sum_k\lambda_k$ and $\chi$.

**No engagement objective.** Nothing anywhere is rewarded. In the living stage, learning uses only the partner's face ($\psi$) and stimulus counts ($\eta$).

## 5. Falsifiable test on Seamless Interaction features

**Data and harness.**
- V00 `FAUValue` (24 AUs at 30 Hz), masked by `is_valid`; VAD and transcript word times for the vocal and turn channels.
- Contrasts: naturalistic familiar versus stranger pairs, and V00 improvised repeat actor pairs (195 pairs).
- The shared harness's person-level splits; the dictionary and all population parameters are fitted on train people only.
- The AU column order must be verified by the harness first, because it is unverified in seamless-interaction.md.

**Baselines, exactly as in Learning to Listen:** Median, Random (another training clip), Nearest Neighbour (motion), Mirror, and Delayed Mirror (lag chosen by TLCC on train). Added: a *Mirror-blend* $a=(1-G')\,\text{median}+G'\,o$, the explicit single-dial family.

**Metrics, as published:**
- L2L: L2, FD, variation, SI, P-FD, PCC of LipCornerPuller between partners, compared with ground truth, and TLCC lag.
- REACT: FRVar, FRDiv, FRSyn.
- evaluation.md E3: windowed cross-correlation against segment-shuffle, data-sliding and participant-shuffle surrogates.
- Held-out log-likelihood of onsets, labelled *provisional*.

**Predictions, fixed before any data:**
- **H1, the core, on human data alone.** Take LipCornerPuller+CheekRaiser onsets of the partner while the listener's AU is below threshold (Mancini's no-prior-expression control).
  - The listener's congruent onset within 1 s is *less* likely when the listener's own congruent onset occurred 1–3 s earlier than when none occurred in the last 10 s, controlling for the partner's recent rate: OR ≤ 0.7.
  - The effect is unit-specific: the listener's own recent brow-raise onsets leave the smile response unchanged, OR in [0.85, 1.15].
  - **If the OR is ≥ 0.9 with a CI covering 1, the reserves are unsupported. The RRDP then reduces to a Hawkes process with a dial and is dropped.**
- **H2, the gain sweep, fitted model.** Scale every partner term by G ∈ {0, 0.25, 0.5, 1, 2, 4, 16, 64}.
  - At G = 0, variation is at least 0.5 × the ground-truth value.
  - At G = 64, CCC(agent, partner) is ≤ 0.5. Mirror-blend reaches 1.0 and its variation tends to 0 at G' = 0.
  - The empirical per-unit $S_k^{\max}$ matches $\rho_k/(\rho_k+\tilde\kappa_k g_0)$ within 10% (mean-field).
- **H3, against the baselines.**
  - The RRDP beats Median, Random and NN on FD and P-FD, and has L2 ≤ Median.
  - Its variation and SI are within 25% of ground truth.
  - |PCC − PCC_GT| is smaller than for Mirror and for Delayed Mirror.
  - Its TLCC lag distribution overlaps ground truth's (including lags ≤ 0), where Delayed Mirror's is a spike.
  - Fitting with 5, 15 and 60 min per listener, NN's FD worsens by more than the RRDP's as data shrink.
  - Mirror may well still win on frame-wise concordance with the true listener (the REACT finding). That is reported, not hidden.
- **H4, familiarity.**
  - In human data, congruent smile latency is shorter (by ≥ 50 ms) and the rate higher (ratio ≥ 1.15) in familiar than in stranger naturalistic pairs.
  - In the model, carrying $\psi^p,\eta^p$ across sessions of the *same* improvised actor pair improves held-out onset log-likelihood and latency error compared with resetting them. Carrying *another* actor's $\psi$ (a participant-shuffle control) does not.
- **H5, conflict.** Fitting $v\ge0$ improves held-out log-likelihood over $v\equiv0$ by a pre-registered margin, and the units with the largest $v_k$ are self-directed lip and eye units. **If not, the conflict pathway is removed.**

**Ablations predicted from the equations (Principle 5):**

| Ablation | Predicted change |
|---|---|
| κ = 0 | The H1 signature vanishes in generated data, and the G sweep reaches copying |
| ε → amplitude ∝ drive | Partner amplitude leaks into the agent's output; CCC with the partner rises |
| ψ off | No familiarity effect (H4) |
| f off | Release no longer depends on context after meta-signal units |

**Budget.** All of this is small point-process fitting on the CPU: under 1 GB of pilot features and under 2 GB of RAM. It waits on the disk question (Q11).

## 6. Known weaknesses

- Very little is learned by living: the repertoire and release maps are population-fixed, and only reading and habituation adapt. That may fall short of the operator's "acquired by living".
- Unit discovery from noisy 24-AU streams may yield poor templates, and the column-order question is unresolved.
- Hawkes-type fitting at 30 Hz with K = 48 needs care, because event extraction thresholds are a hidden choice.
- Voice prosody cannot be tested on these features, which have no audio; only VAD and token timing can.
- The strongest critique: this is a neural Hawkes process with priors. Its value is H1. If human listeners show no action-specific refractoriness, nothing distinctive remains.
