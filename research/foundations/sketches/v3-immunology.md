# Sketch v3: the self-tolerizing repertoire (immunology lens)

Status: sketch, 2026-11-25. Written in isolation from the other sketches. Novelty verdict (section 2): **recombination**. One coupling, tolerance of partner detectors induced by the agent's own expressed output and licensed by an endogenous signal, was not stated in any prior work I read. It still reduces to known parts.

## 0. The idea in immunology terms

An immune system does not have one gain for "how much of the outside gets in". Its response to an antigen is set by a population of clones. Each clone binds some content. Clones expand when they bind and receive a second, endogenous signal (danger: Matzinger). They are silenced (anergy) when they bind self without that signal. They persist as memory. And they stimulate and suppress one another (Jerne's idiotypic network). Mapped onto a face:
- the partner's face and voice are the **antigen**;
- the agent's own expressed face and voice, encoded by the same body code, are **self**;
- signals from the agent's own body and its own failed predictions are **danger**.

Partner content that the agent is already expressing becomes "self" and is tolerized unless the body is in danger. So imitation is not a regime a dial selects. It is a fixed point the mechanism dismantles.

## 1. Mechanism

**Streams** (30 Hz, $\Delta t = 1/30$ s):
- $o_t \in \mathbb{R}^{28}$: partner features (24 FAU intensities, VAD, and 3 prosody channels when audio features exist; in Seamless, VAD only).
- $y_t \in \mathbb{R}^{28}$: the agent's own expressed output (24 AU, 4 voice parameters: pitch, pitch range, rate, volume).
- $d_t \in \mathbb{R}^m_{\ge 0}$, $m \approx 4$: the agent's own body deviations $|b_t - b^*|$. In Seamless these are the agent's own speaking load (from its own VAD), time since its own last turn, and own-expression effort $\|y\|$. No partner feature enters $d_t$.

**Own-body code.** $\phi: \mathbb{R}^{W\times 28}\to\mathbb{R}^{d}$ ($W = 15$ frames = 0.5 s, $d = 18$) is a small temporal convolution trained only on the agent's own output stream, as the encoder of its own motor trajectories. The partner is encoded with the same map:
$$u_t = \phi(o_{t-W+1:t})\ \ (\text{antigen}),\qquad s_t = \phi(y_{t-W+1:t})\ \ (\text{self}).$$

**Repertoire.** Clones $i = (v,\delta,j)$, $K = n_V n_D n_J$ (for example $16\cdot 8\cdot 8 = 1024$). Each clone has:
- a receptor built combinatorially from germline segments, $r_i = [V_v; D_\delta; J_j] + \Delta r_i$, where $\Delta r_i$ is a small somatic offset;
- class weights $\pi_i \in \Delta^{C}$ over $C = 4$ effector classes, with class maps $A_c: \mathbb{R}^d \to \mathbb{R}^{28}$;
- a costimulation profile $\zeta_v \in \mathbb{R}^m$, set by its V segment.

Its state is $(x_i = \ln n_i,\ a_i \in [0,1],\ m_i \ge 0,\ \pi_i)$: population, anergy, memory, class. The **latent state is $\{x, a, m, \pi\}$, $\approx 7K$ numbers**; the learned parameters are about $10^4$.

**Affinity and fields.** $\beta(z;r) = \exp(-\|r - z\|^2/2\sigma^2)$. The binding of clone $i$ to the antigen is $b_i = \beta(u_t; r_i)$; its binding to self is $\beta_i^{s} = \beta(s_t; r_i)$. The idiotypic coupling is complementarity in shape space, $J_{ij} = \gamma\,\beta(-r_j; r_i)$. Then:
$$h_i^{\rm net} = \sum_j J_{ij} n_j / N_t,\qquad h_i = b_i + h_i^{\rm net}.$$
The **internal image** (Jerne) of what the repertoire expects to meet, and the partner content it failed to expect:
$$\hat u_t = \sum_i \omega_i r_i,\quad \omega_i \propto n_i\,w(h_i^{\rm net}),\qquad \varepsilon_t = u_t - \hat u_t .$$

**Signal 2 (danger), local and endogenous.** Costimulation for clone $i$ comes only from the agent's own failed prediction near that clone's content, and from its own body:
$$g_i = \operatorname{sig}\!\big(\chi\,\beta(\varepsilon_t; r_i)\,\|\varepsilon_t\| + \zeta_{v(i)}^{\top} d_t - \theta_g\big).$$

**Dynamics.** Window activation $w(h) = \frac{h}{\theta_1+h}\cdot\frac{\theta_2}{\theta_2+h}$ (bell-shaped: low-dose and high-dose unresponsiveness). Noise $\xi_i$ is Poisson-like birth noise, which is what makes the model's samples differ.
$$x_i \leftarrow x_i + \Delta t\big[\rho\,(1-a_i)\,g_i\,w(h_i) - \delta - \lambda\,(x_i - \ln(n_0 + m_i))\big] + \sqrt{\Delta t}\,\xi_i \quad\text{(clonal selection)}$$
$$a_i \leftarrow a_i + \Delta t\big[\kappa\,\beta_i^{s}\,(1-g_i)(1-a_i) - \nu\,g_i a_i - \mu a_i\big] \quad\text{(self-tolerance: binds own output, no danger)}$$
$$m_i \leftarrow m_i + \Delta t\,\epsilon_m\big[(n_i - n_0)_+ - \eta\, m_i\big] \quad\text{(memory, hours to days)}$$
$$\pi_i \leftarrow \operatorname{softmax}\big(\ln \pi_i + \Delta t\,\Gamma^{\top} d_t\big) \quad\text{(class switching by body context)}$$
Affinity maturation runs only while costimulated: $\Delta r_i \leftarrow (1-\eta_r)\Delta r_i + \eta_r\, g_i\, b_i\,(u_t - r_i) + $ noise, with $\|\Delta r_i\| \le r_{\max}$.

**Readout (secretion).**
$$\alpha_i = \frac{n_i(1-a_i)\,g_i\,w(h_i)}{Z_0 + \sum_j n_j},\qquad y_t = y_0 + \sum_i \alpha_i \sum_c \pi_{ic} A_c r_i + \text{autonomic}(t).$$
$y_t$ drives the face (AUs) and the voice parameters, and returns through $s_t$ into the anergy equation. That loop is the core of the mechanism.

**What it computes.** A population code over the agent's own motor shape space. In it:
- partner content excites clones only where the agent's own body or its own failed predictions license a response;
- content the agent already expresses is progressively ignored;
- complementary clones hold an internal image of the partner after the partner stops;
- repeated content leaves memory that speeds the next response.

**Learning.**
- Germline (offline, across many people; "evolution"): the segments $V, D, J$, the maps $A_c$, $\phi$, $\Gamma$, $\zeta$ and the scalars. Trained by truncated BPTT to predict the next frame of the real listener's AUs from the partner stream on training dyads, with the population dynamics run forward.
- Online, per person: only state ($x, a, m, \pi$) and the bounded somatic offsets $\Delta r$. Nothing per frame is stored.

## 2. Novelty test

| Part | Existing mechanism it is |
|---|---|
| Shared own-body encoder $\phi$ for partner and self | Common coding / efference copy; MOSAIC observation mode (Wolpert, Doya & Kawato 2003) |
| Affinity $\beta(u; r_i)$ over a repertoire | RBF units / attention scores / mixture responsibilities |
| $r_i$ built from V, D, J segments | Product-key memory (Lample et al. 2019); factorized embeddings |
| Log-population growth driven by stimulation | Replicator / multiplicative-weights dynamics; Farmer–Packard–Perelson (FPP) 1986 immune network equation |
| Bell-shaped $w(h)$ | "Window automata" / log-bell proliferation of theoretical immunology |
| Idiotypic $J_{ij}$ with complementary shapes | Jerne network; shape-space models; computationally a recurrent net on populations |
| Internal image $\hat u$ and innovation $\varepsilon$ | Jerne's internal image; predictive coding / prediction error |
| Two-signal gate $g_i$ | Dendritic Cell Algorithm (DCA; Greensmith et al. 2005); multiplicative gating (LSTM) |
| Anergy from self-binding without signal 2 | Negative selection (Forrest et al. 1994); stimulus-specific adaptation |
| Memory compartment $m$ | Two-time-scale / slow weights |
| Effector classes $A_c$, $\pi_i$ | Mixture of experts; MOSAIC paired controllers |
| Affinity maturation | CLONALG (de Castro & Von Zuben 2002); competitive learning with noise |
| Readouts (section 4) | Rate-of-change readouts (Joffily & Coricelli 2013) |

**Closest prior work, read in primary source:**

1. **Immune-network behavior arbitration** (Watanabe, Ishiguro, Shirai & Uchikawa, ICEC 1998, read in full; their eq. 1 is the FPP 1986 equation they cite. I could not obtain FPP 1986 itself, so it is not read.)
   - The mapping: "current situations detected by installed sensors work as multiple antigens (or epitope), and a prepared competence module (i.e. simple behavior) can be regarded as an antibody (or B-lymphocyte), while the interaction between modules is represented by stimulation and suppression between antibodies."
   - Dynamics: $\frac{dA_i}{dt} = (\alpha\sum_j m_{ji}a_j - \alpha\sum_k m_{ik}a_k + \beta m_i - k_i)\,a_i$, squashed by $a_i = 1/(1+\exp(0.5 - A_i))$. "The first and second terms … denote the stimulation and the suppression from other antibodies … The third term represents the stimulation from the antigen, and the fourth term the dissipation factor (i.e. natural death)."
   - Selection: "selection of antibodies is simply carried out on a roulette-wheel manner basis according to the magnitude of concentrations … only one antibody is allowed to be selected … (i.e. winner-take-all manner)."
   - Antigens are binary sensor categories, antibodies are fixed if-then behaviors, and the repertoire comes from an offline GA.
   - Absent there: a continuous output mixture, any self term built from the agent's own output, any danger gate, and memory.
2. **Dendritic Cell Algorithm** (Greensmith, Aickelin & Cayzer, ICARIS 2005, sections 1–5 read).
   - "the Danger Theory rests on the detection of endogenous signals. Endogenous danger signals arise as a result of damage or stress to the tissue cells themselves."
   - "the absence of danger signals and the presence of cytokines released as a result of apoptosis can lead to antigen presentation in a different context, deleting or anergising a matching T-cell."
   - The algorithm itself is a fixed weighted sum of four "pre-classified" signal types (their eq. 1, Table 1). It labels data items mature or semi-mature, with "Antigen … represented in its simplest form, as the identification number of a data item."
   - Absent there: effectors, a repertoire, and any self that is the system's own output.
3. **MOSAIC for social interaction** (Wolpert, Doya & Kawato, Phil Trans B 2003, MOSAIC and imitation sections read).
   - "the sensory prediction error from a given forward model is represented as a probability; if the error is small then the probability that the forward model is appropriate is high."
   - "A natural extension of the model is to compare the predictions, not with one's own state, but with the state of a system that is being observed."
   - "Rather than these commands acting on the observer's own musculoskeletal system, the output of each controller forms the input to its paired predictor."
   - Responsibilities are an instantaneous normalized posterior, with no population memory, no anergy and no gate. Observation reuses one's own modules, so imitation is the natural output.
4. **Window activation.** Chowdhury (arXiv cond-mat/9803033, sections 2–4 read): "$S_i = 1$ only if $h_i$ falls within a certain window between two thresholds."
5. **Danger model** (Matzinger, Science 2002): abstract only; the full text was not accessible. Its claim that the immune system responds to damage rather than to foreignness is the premise of $g_i$.

**What is not in the prior work read.** The tolerance term is
$$\kappa\,\beta(\phi(y_{\rm own}); r_i)\,(1-g_i)$$
It is a cross-stream coupling: the detectors of the *partner's* content are silenced by the *agent's own expressed* output, which is encoded in the same body code, unless the agent's own body or prediction failure licenses them. FPP and the immunoid have no self term. The DCA tolerizes data items, not its own outputs. MOSAIC has no suppression of modules the agent's own output already covers.

**Plainly:** this term is stimulus-specific adaptation whose input is the efference copy, multiplied by a gate. Candidate precedents I have not read in full:
- vocalization-induced suppression of auditory cortex (Eliades & Wang 2003);
- "self–other control" in imitation inhibition (Brass et al. 2009);
- copy-suppression attention heads (McDougall et al. 2023).

The sketch is therefore a **recombination** (FPP/Jerne dynamics + DCA gating + MOSAIC-style self-coded repertoire + product keys + efference-driven adaptation). Under Q9 it is a baseline, not the core. What it contributes is a structural answer to the one-dial failure, which the critique round should try to break.

## 3. The three shared risks

**(a) Delayed copy.**
- Let partner content be held near $u^*$ for longer than $1/\kappa$, and suppose the agent copies it with lag $\tau$, so $s_t \approx u_{t-\tau} \approx u^*$.
- Then $\beta_i^s \approx b_i$ for exactly the clones driving the copy. The internal image converges, $\hat u \to u^*$, so $\varepsilon \to 0$, and the costimulation falls to its body-only value $g_0 = \operatorname{sig}(\zeta^\top d - \theta_g)$.
- Steady-state anergy: $a^* = \kappa b(1-g_0)/(\kappa b(1-g_0) + \nu g_0 + \mu)$. The copy clones' secretion scales with $(1-a^*)g_0 \approx g_0(\nu g_0 + \mu)/(\kappa b)$, which is second order in $g_0$.
- So **sustained copy is self-extinguishing unless the agent's own body is in danger**. Fast copying of *changes* survives: new content raises $\|\varepsilon\|$, the clones it binds are not yet tolerized, and they respond within $\approx W$ = 0.5 s. That matches rapid facial reactions at 300–400 ms (Dimberg & Thunberg 2012), not delayed mirroring.
- Content the partner shows that the agent is *not* expressing ($\beta^s \approx 0$) is never tolerized. So the drift is toward expressions complementary to the agent's own, not toward the partner's.
- Contagion that holds (shared laughter) is predicted only under high $\zeta^\top d$: a body state, not a setting.
- The lesion $\kappa = 0$ is predicted to move the output toward Delayed Mirror (section 5, P2).

**(b) One hidden dial.**
- The partner Jacobian is
$$\partial y/\partial u = \sum_i c_i\, e_i\, \nabla_u b_i^{\top},\qquad c_i = \frac{n_i(1-a_i)}{Z}\big[g_i w'(h_i) + w(h_i)\,\partial g_i/\partial b\cdots\big],$$
  with $e_i = \sum_c\pi_{ic}A_c r_i$. It is a sum of rank-one terms with state-dependent, *signed* coefficients ($w' < 0$ past the bell's peak).
- Define the content gain $G_t(k) = \|(\partial y/\partial u)\,k\|$ for a direction of partner content $k$ (for example a lip-corner pull against a brow raise). In any model where one scalar sets the partner's share, $y = F(\text{state}, g\cdot L[o])$ with $L$ fixed, the ratio $G(k_1)/G(k_2)$ is the same in every state.
- Here the ratio moves with the history of each content separately:
  - anergy is high where the agent's own output has covered $k_1$;
  - local danger is high where $k_2$ was unpredicted;
  - memory is high where $k_2$ recurred with this partner;
  - high dose pushes $h$ past the peak.
- No scalar parameter reproduces these changes, because they are indexed by content.
- Honest caveats. The model has about 15 global scalars ($\rho, \kappa, \sigma, \theta_{1,2}, \ldots$). Scaling $\rho$ or $Z_0$ changes overall expressivity. But no single one of them runs flat → imitation:
  - imitation needs $A_c \approx \phi^{-1}$, $a \approx 0$ and $g \approx 1$ together, and two of these are state driven by the agent's own output and body;
  - the bell bounds the high end;
  - flat affect arises from $g \to 0$ (a body at rest, a predicted partner) or from global anergy, both of which are states.
  - A critic may call $d_t$ the dial. It is a vector of the agent's own body signals, read per clone through $\zeta_v$, not a single gain on the partner path.

**(c) Lookup table under scarce data.**
- Nothing per frame is stored. Outputs are population mixtures of smooth maps $A_c r_i$ over about $10^4$ parameters, so the model cannot replay a past listener trajectory, as Nearest Neighbour does.
- Receptors are combinations of 32 segment vectors. Somatic offsets are bounded by $r_{\max}$.
- Per-person adaptation is state, not stored exemplars: about $7K$ numbers of population, anergy and memory.
- Diagnostic (section 5): an NN-copy index, the maximum correlation of each generated 2 s window with any training listener window. It must sit below Nearest Neighbour's index and near the human-to-human level.

## 4. Emotion as structure, reading through the body, driving face, voice and words

**Structure, not labels.**
- The idiotypic network with bell activation has multiple self-sustaining configurations: localized expansions ("patches") in shape space that persist after the antigen is gone (the immune, tolerant and suppressed states of shape-space models).
- The candidate emotion-like structure is these configurations: recurrent, partly self-sustaining clone families. Each has:
  - a characteristic effector profile across face and voice;
  - a costimulation signature, meaning which body signals license it;
  - many partner contents that can reach it (degenerate, as constructed emotion requires);
  - a tolerance history that makes it person-specific.
- Time scales: populations over seconds, memory over hours to days, germline segments over weeks (temperament).
- Two readouts, never set:
  - arousal: proliferation flux $\sum_i n_i|\dot x_i|$;
  - valence: the rate of danger resolution $-\tfrac{d}{dt}\overline{\textstyle\sum_i g_i}$.
- Nothing below Claude is named. Clustering repertoire states is for analysis only.

**Reading the other through its own body.**
- The partner exists for the agent only as which of its own clones bind them in its own motor code $\phi$, and as the internal image $\hat u$ decoded as "what my face would be doing".
- The agent infers the partner's state by its own generative mapping: $\hat u$ and the class maps $A_c$ are the agent's motor programs.

**Face and voice.** Both come from the same $y_t$: 24 AU channels to the face, and pitch, range, rate and volume per word to speech synthesis.

**Claude (never sees numbers or state words).**
1. Retrieval: episodes are stored with their memory signature $m$. Episodes whose signature overlaps the current one are placed in Claude's context as text: immunological memory as mood-congruent recall.
2. Cue selection: a fixed describer turns partner features into plain observations ("she looked away"). Only cues bound by non-anergic, costimulated clones are passed on, so what the agent has become tolerant to, Claude does not notice.
3. Proliferation flux sets the thinking budget, reply length and latency.
- Word choice changes only through items 1 to 3.

## 5. Falsifiable test on Seamless Interaction features only

**Data.**
- V00 `FAUValue` (v1 only, not mixed with v4), `is_valid` mask, duplicate column 12/19 dropped, VAD, and transcripts (used only for turns).
- Splits: the shared harness's person-disjoint train/validation/test.
- Familiar and stranger sessions come from naturalistic V00 (between pairs).
- The V00 improvised repeat actor pairs (195 pairs) are held out whole in validation and test, and run in session order.
- Pilot: a few hundred interactions, under 1.5 GB, after Q11 allows a download. Compute is CPU-trivial ($K = 1024$, $d = 18$): under 2 GB peak, and well under an hour for the screening budget.

**Baselines (REACT, as published):**
- Median (training median listener face), Random (a listener clip from another interaction), Nearest Neighbour (nearest speaker window to its listener window), Mirror, and Delayed Mirror (15 frames).
- The explicit one-dial families: $y = (1-g)\,\text{median} + g\,\text{Mirror}_{\tau}$ over $g, \tau$, and a ridge VAR with its penalty swept.
- All get the same tuning trials on validation.

**Metrics.**
- REACT's representation-agnostic metrics on AU series: FRVar, FRDiv (10 samples), FRDvs, FRSyn (TLCC).
- CCC and DTW against the *actual* listener. This is a stated deviation: Seamless has no appropriate-neighbour matrix.
- E3 coupling (windowed cross-correlation against surrogates, evaluation.md).

**Predictions.** Thresholds are fixed before scoring, and confidence intervals come from a person-level bootstrap.

- **P1, no single dial (the core claim).**
  - Method: estimate local partner→listener linear maps (lags 0–1 s) separately for these conditions:
    - familiar vs stranger;
    - session 1 vs sessions ≥ 3 of repeat pairs;
    - partner-content onset frames vs sustained frames;
    - listener already expressing that content vs not.
  - Do it on real listeners and on each model's output. Gain-ratio variation is the across-condition spread of $\log G(k_1)/G(k_2)$ for the top partner-AU directions.
  - Predictions:
    - (i) Humans show a spread greater than 0 (CI excludes 0). If not, the one-dial target does not describe people, and this sketch's motive is falsified.
    - (ii) The model's spread falls within the human CI, and the cosine between model and human condition-difference maps is ≥ 0.3.
    - (iii) Every one-dial baseline shows a spread of ≈ 0 by construction, so it fails (ii).
- **P2, anti-copy.**
  - The model's copy index (peak lagged partner→listener correlation, 0–0.7 s) does not exceed the human 95% upper bound.
  - Onset gain over sustained gain is ≥ 1.5 in both humans and the model.
  - The $\kappa = 0$ lesion moves the copy index at least halfway toward Delayed Mirror.
  - Falsified if the intact model already sits at the Delayed Mirror level, or if the lesion changes nothing.
- **P3, secondary response with a returning partner.**
  - Run over repeat pairs in session order. A model whose memory $m$ carries across sessions beats the same model reset each session, on CCC with the real listener and on response latency to partner onsets. Human latency should shorten across sessions with the same partner but not with a new one.
  - Falsified if carried state ≤ reset state (paired, by pair).
- **P4, the REACT failure.**
  - CCC (model) > CCC (Delayed Mirror) and > CCC (Mirror), with a CI excluding 0.
  - Beats Median, Random and Nearest Neighbour on CCC.
  - FRVar within 20% of human; FRDiv > 0.
  - NN-copy index below Nearest Neighbour's.
  - If Delayed Mirror still wins CCC, the mechanism fails the test that motivated it.
- **Ablations** (E1, each with a written prediction): no anergy ($\kappa = 0$) → copy (P2); no idiotypic coupling ($\gamma = 0$) → no persistence after partner offsets; no memory ($\epsilon_m = 0$) → P3 lost; clamp $g \equiv 1$ → imitation; clamp $g \equiv 0$ → flat.

Caveat: Seamless gives the listener no interoception. $d_t$ is built from the listener's own VAD and expression load, which is a thin stand-in for a body. P1–P4 test the partner pathway, not the body.
