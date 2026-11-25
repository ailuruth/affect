# Critique: v3-immunology ("the self-tolerizing repertoire")

Independent critic, 2026-11-25T09:42Z, written under questions.md Q8 (critique round) and Q9 (novelty test). I did not write the sketch. No datasets or weights were downloaded. Counts in §5 were computed from metadata CSVs and research/harness/splits_v2.json that were already in the repository.

**Verdict: recombination** (I agree with the sketch's own verdict). It is **efference-driven stimulus-specific adaptation with a gate**, the tunable-activation-threshold / discontinuity computation of theoretical immunology, inside a Farmer–Packard–Perelson population network. The sketch missed this closest prior work. The output is decoded linearly.

**Its central claim fails.** The claim is that the partner's share of the agent's expression is not set by one scalar. The danger threshold θ_g (equivalently, the common-mode part of ζᵀd) is a single scalar. It runs the model from flat to un-tolerized, and the sketch's own ablation list names the two ends "flat" and "imitation". The same scalar also switches off the content-specific modulation that the sketch offers as its proof (§4b, derived).

## Sources and how they were read

| Source | How read |
|---|---|
| Sontag 2017, "A dynamical model of immune responses to antigen presentation predicts different regions of tumor or pathogen elimination", *Cell Systems* 4:231 (PMC5323365) | Full text of the author manuscript via a fetch tool: Introduction, Results, Biology Box, Discussion. Supplement not read. |
| Grossman & Paul 1992, "Adaptive cellular interactions in the immune system: the tunable activation threshold and the significance of subthreshold responses", *PNAS* 89:10365 | **Abstract only.** The PMC full text is scanned page images, so no text could be extracted. |
| Pradeu, Jaeger & Vivier 2013, *Nat Rev Immunol* 13:764 | **Not read.** The preprint servers refused automated access. It is cited below only as Sontag cites it. |
| Blyuss & Nicholson 2012, arXiv 1209.4487 | Introduction read (PDF text). Used only for its quotation of the TAT definition. |
| Ng et al. 2022, Learning to Listen, arXiv 2204.08451 (HTML v1) | §5–5.2 via a fetch tool: baseline definitions and the TLCC result |
| research/dimberg-thunberg-2012-rapid-facial-reactions.md, research/react-challenge-baselines.md, research/seamless-interaction.md, research/harness/HARNESS.md | Project notes, read in full. Claims from them are marked as secondary. |

## 1. Parts list

I accept the sketch's table (§2 of the sketch) with these corrections and additions:

| Part | Existing mechanism | Note |
|---|---|---|
| Anergy driven by self-binding without signal 2, plus the danger gate g_i | **Tunable activation threshold** (Grossman & Paul 1992) and the **discontinuity theory** it feeds (Pradeu et al. 2013, via Sontag 2017). Formalized as an incoherent feed-forward loop (Sontag 2017). | Missed by the sketch. See §2. |
| Readout α_i ∝ n_i(1−a_i)g_i w(h_i)/(Z₀+Σn_j) | Divisive normalization over a population code. With RBF affinities it is a normalized kernel (Nadaraya–Watson-type) weighting. | |
| e_i = Σ_c π_ic A_c r_i | **Linear in the receptor.** So y − y₀ = Σ_c A_c (Σ_i α_i π_ic r_i): a gated linear decode of a population-weighted average of receptors. | Matters for §4a and §4c. |
| r_i = [V; D; J] + Δr | Product quantization / product keys. The sketch says so. | |
| Internal image û and innovation ε | Predictive coding prediction error, and Jerne's internal image. The sketch says so. | |

**No part is new.** What the sketch claims as unprecedented is the *input* to the anergy term: the agent's own output encoded by φ, rather than the antigen. Q9 rules that a choice of input is not a new computation.

## 2. Closest prior work, read in primary source

**Tunable activation threshold and discontinuity (missed).**
- Grossman & Paul 1992, abstract: lymphocytes "achieve this by tuning and updating their responsiveness to recurrent signals". "Cellular anergy in vivo is a dynamic state in which the threshold for a stereotypic mode of activation has been elevated."
- Blyuss & Nicholson quote the definition: "activation is a threshold phenomenon and the threshold is tuned by the stimulatory experience of the cell".
- Sontag 2017 states the computation:
  - "lymphocytes mount a sustained response only when faced with a sufficiently steep increase in their level of stimulation";
  - under Grossman and Paul's model, effector cells "should become tolerant to continuously expressed motifs, or even gradually increasing ones";
  - Sontag names the "discontinuity theory" of Pradeu, Jaeger and Vivier as a variant of the same idea.
- Sontag's model is ẋ = −δₓx + βu, ẏ = h(u/x) + f(y), "a type of incoherent feedforward loop (IFFL)". It shows "the return to a basal value independent of the excitation magnitude", and it estimates the growth rate of an exponentially rising input.

**Comparison with the sketch.** The sketch's own answer to the delayed-copy risk (its §3a) is this computation, stated in other words. "Sustained copy is self-extinguishing … Fast copying of *changes* survives" is the discontinuity principle applied per content channel.
- **What the sketch adds:** the adapting variable is driven by φ(own output) instead of by the stimulus.
- **In the copy regime**, own output ≈ partner content (s_t ≈ u_{t−τ}). The anergy input then equals the partner stream delayed by the loop lag, and the sketch's term reduces to TAT/discontinuity adaptation on the partner stream.
- **Outside the copy regime**, the efference input changes behavior only for content the agent is already expressing for other reasons. The effect there is "do not echo what I already show". That is the reafference idea (efference copy cancelling self-matching input; von Holst & Mittelstaedt 1950, *not read*), here applied to the partner channel.
- **So the anti-copy work is done by a known computation.** The new input changes behavior only off the copy manifold.

**Did the sketch misquote, or misread its prior work?**
1. **Baselines attributed to the wrong paper.** The sketch lists "Baselines (REACT, as published): Median, Random, Nearest Neighbour, Mirror, and Delayed Mirror (15 frames)".
   - These are Learning to Listen's baselines, not REACT's.
   - L2L §5.1: "Here we mirror the speaker's smoothed motion delayed by 17 frames (≈0.5 s)", the lag chosen "according to time lagged cross correlation". **17 frames, not 15.**
   - The REACT 2023 code's baselines are different. B_Random is uniform noise, and there are B_Mime, B_MeanSeq and B_MeanFr (react-challenge-baselines.md, secondary).
2. **Dimberg & Thunberg 2012 is read selectively.** The sketch says rapid facial reactions occur "at 300–400 ms".
   - The project note on the paper (secondary) gives 300–400 ms only for the corrugator in the *high-empathy* group, and 400–500 ms for the zygomatic.
   - The paper also says "the most clear-cut difference between the stimuli appears after 500 ms".
   - These were reactions to photographs in the lab, not dyadic conversation.
   - The sketch's surviving response latency, ≈ W = 0.5 s, is the Delayed Mirror lag itself.
3. **An algebra slip in §3a.** The copy clones' secretion is (1−a*)g₀ = g₀(νg₀+μ)/(κb(1−g₀)+νg₀+μ). For μ > 0 this is **first order** in g₀ (≈ g₀μ/κb), not second order as the sketch says. The extinction is weaker than claimed.
4. The sketch's reading of Watanabe et al. 1998 and Greensmith et al. 2005 was not re-checked here.

## 3. Reduction

The whole mechanism can be written as:

> A divisively normalized RBF population code over the agent's own motor code (FPP/Jerne dynamics, product-quantized receptors), decoded linearly by A_c,
> + per-content adaptation of the TAT/discontinuity kind, whose adapting input is the efference copy,
> + a sigmoid gate on (local prediction error + a weighted body vector − θ_g),
> + a slow memory compartment,
> + mixture-of-experts class weights.

**Verdict: recombination. The computation is gated efference-driven stimulus-specific adaptation.** It is not a new mechanism.

## 4. Break attempts

### (a) Collapse into a delayed copy

1. **What survives is a high-passed Delayed Mirror.**
   - Linearize around a fixed gate g. The anergy of a clone that the agent's own output covers relaxes at rate 1/τ_a = κβ^s(1−g) + νg + μ.
   - Clonal growth lags by about 1/ρ, and φ adds a W = 15-frame window.
   - So for partner content the agent copies, the output is approximately G·HP_{τ_a}[u](t − ≈0.5 s): the partner, delayed by about the L2L Delayed Mirror lag (17 frames), passed through a first-order high-pass filter.
   - The sketch itself says "Fast copying of changes survives". On partner AU series dominated by onsets (smiles and nods are short), a high-passed delayed mirror is close to a delayed mirror.
   - Nothing in the sketch fixes τ_a relative to the length of typical partner AU events. If τ_a is longer than an event, the mechanism never acts.
2. **The extinction argument assumes something it does not derive.** It needs the internal image û → u*, so that ε → 0 and the local danger on the copy clones falls.
   - But û = Σ ω_i r_i with ω_i ∝ n_i w(h_i^net), and h^net comes from *complementary* clones (J_ij = γβ(−r_j; r_i)).
   - During a sustained copy, the anti-clones (r ≈ −u*) do not bind the antigen, and receive no local danger (β(ε; −u*) is small). So they do not expand, and the copy clones get little idiotypic weight in û.
   - Then ε ≈ u* − û stays large. The local danger term χβ(ε; r_i)‖ε‖ stays high on exactly the copy clones (r_i ≈ u*). The factor (1−g_i) ≈ 0 blocks their anergy, and **the sustained copy persists**.
   - Whether û tracks u* is an empirical property of the trained J and γ. It must be shown, not assumed.
3. **Positive point.** Content the agent never expresses is never tolerized, so the drift is away from echo. But this drift is toward the *un-adapted* response, which is whatever A_c learned. If A_c learned listener ≈ mirror (the training target is the real listener, and REACT shows mirror is a strong predictor), the un-adapted response is a mirror.

### (b) A single hidden dial: the central claim

**The sketch's argument.** The ratio G(k₁)/G(k₂) varies with content history. One-gain models y = F(state, g·L[o]) keep that ratio fixed. Therefore there is no single dial.

**Problem 1: the criterion is wrong.** A varying gain ratio does not show that there is no dial.
- Take the one-dial saturating mirror y = σ(g·L u). Its Jacobian is g·diag(σ′(gLu))·L.
- The ratio G(k₁)/G(k₂) moves with the operating point: onset against sustained, or the listener already expressing a content against not.
- Yet one scalar g runs it from flat (g = 0) to copy (L ≈ I, g large).
- So P1(iii), "every one-dial baseline shows a spread of ≈ 0 by construction", is true only for *linear* one-dial baselines. A nonlinear one-dial model passes P1. P1 cannot detect the failure it was built to rule out.

**Problem 2: the dial exists, and the sketch names its two ends.**
- Use the sketch's own sustained regime (ε → 0). There g_i = sig(ζ_vᵀd − θ_g) for every clone with V segment v.
- Shifting θ_g moves every g_i in the same direction, monotonically.
- At the steady state of the sketch's equations:

  a_i* = κβ_i^s(1−g) / (κβ_i^s(1−g) + νg + μ),  1 − a_i* = (νg+μ) / (κβ_i^s(1−g) + νg + μ)

  n_i* = (n₀+m_i)·exp{[ρ(1−a_i*)g·w(h_i) − δ]/λ}

  partner gain of clone i: c_i ∝ n_i*(1−a_i*)·g·w′(h_i)

- **As θ_g → +∞ (g → 0):** c_i → 0 for all i, and y → y₀ + autonomic. The sketch's own ablation: "clamp g ≡ 0 → flat".
- **As θ_g → −∞ (g → 1):** a_i* → 0 for every clone, so tolerance is off. c_i → (n₀+m_i)e^{(ρw−δ)/λ}w′(h_i), the un-tolerized population filter. The sketch's own ablation: "clamp g ≡ 1 → imitation".
- **The content-specific spread is a function of the same scalar.** The tolerance-induced log gain ratio between a covered content (β^s = 1) and an uncovered one (β^s = 0) is

  Δ(g) = log[(κ(1−g) + νg + μ) / (νg + μ)]

  It falls monotonically from log((κ+μ)/μ) at g = 0 to **0 at g = 1**.
- So θ_g sets both how much of the partner enters (0 → full) and how content-specific that entry is (maximal → none). The sketch's caveat says imitation needs "a ≈ 0 and g ≈ 1 together, and two of these are state". That is answered by the derivation: the a ≈ 0 condition is a function of g, and g is a function of the one scalar θ_g.
- What remains content- and history-dependent at g = 1 is memory m_i and the bell w(h_i). Neither is tolerance.

**Problem 3: a conditional tipping point (it depends on a sign the training will choose).**
- In the Seamless version, d_t contains the agent's own expression effort ‖y‖. Write ‖y − y₀‖ ≈ g·S, where S is the un-gated secretion norm.
- If the learned weight on that channel ζ_y > 0, the gate obeys g = sig(ζ_y·g·S + r − θ_g).
- The slope of the right side in g is at most ζ_y S/4. So for **ζ_y S > 4** the gate is bistable: one stable state near g = 0 (flat) and one near g = 1 (the un-tolerized, "imitation" state).
- This is a fold in one scalar, ζ_y S, the same shape as the α = 1 + 2ε tipping point found in the routing-modular critique.
- For ζ_y ≤ 0 it does not arise. The sketch should constrain the sign or report the learned value.

**Answer to (b): the "no single dial" claim does not survive.** The effective gain is the common-mode gate offset θ_g − ζᵀd. Its two ends are the sketch's own two ablations.

### (c) A lookup table under scarce data

**This largely survives.**
- No frames are stored. Receptors are product-quantized and bounded by r_max. Per-person adaptation is state.
- But affinity maturation pulls r_i toward observed u_t, and e_i is linear in r_i. So the repertoire becomes a per-partner codebook of the *partner's* code, decoded by A_c.
- The risk is therefore not replaying listener faces, as Nearest Neighbour does. It is **a mirror through a learned linear map**, which is risk (a) again.
- The proposed NN-copy index is adequate for (c).

## 5. The Seamless test: feasibility and discrimination

**Feasibility** (counts computed here from repository metadata, harness split v2):

| Item in the sketch | Status |
|---|---|
| Inputs: FAUValue v1, is_valid, VAD, transcripts; d_t from own VAD and own ‖y‖ | Feasible. o_t is 23 AU after the harness drops column 19, not 24. |
| "The V00 improvised repeat actor pairs (195 pairs) are held out whole in validation and test" | **Conflicts with the harness**, which assigns *persons* by hash. Under splits_v2 only **6 repeat pairs fall in val (254 interactions) and 5 in test (194)**. 86 are in train, 96 straddle splits and are dropped, and 2 are absent. Holding 195 out would need a different split, and the harness forbids changing splits after fixing them. A person-level bootstrap over 5 test pairs gives very wide CIs. |
| P1 condition "session 1 vs sessions ≥ 3"; P3 "run over repeat pairs in session order", latency shortening across sessions | **Not computable as stated.** research/seamless-interaction.md: "Session order and dates: not released … interaction order within a session is not given". Only same-pair against other-pair contrasts are possible, without order. |
| P1 condition "familiar vs stranger" (naturalistic V00) | **Between-person and thin.** In val and test, **0 persons have both familiar and stranger naturalistic sessions**. Stranger naturalistic interactions number 15 (val) and 21 (test), against 203 and 149 familiar. Any gain-ratio difference is confounded with person. |
| P1 "top partner-AU directions" | Feasible via PCA. The column order is unverified, so named directions (lip corner, brow) are not. |
| Metrics: FRVar, FRDiv, FRDvs, FRSyn; CCC and DTW against the actual listener; E3 | Computable. CCC/DTW against the actual listener is a labelled deviation. The harness's screening tests for the shared risks are L2L's L2, FD and P-FD (P-FD below Delayed Mirror's is *the* delayed-copy test), and the sketch does not report them. Add them. |
| Compute | CPU-trivial, as claimed. Blocked on Q11 (disk) like every download. |

**Would it discriminate the mechanism from the published baselines?**
- **P4** (CCC above Mirror and Delayed Mirror, FRVar within 20%, FRDiv > 0) separates the model from Median, Random, NN and Mirror. Median and the mirrors are deterministic, so FRDiv = 0 for them. But P4 does not separate *this mechanism* from any adapting or stochastic model.
- **P1 does not test the claim** (Problem 1 above). A one-dial *nonlinear* model passes it. Its null must be simulated through the same estimator, with at least σ(g·Delayed-Mirror) and σ(g·ridge-VAR) + noise, not asserted to be ≈ 0.
- **P2's κ = 0 lesion is confounded with overall gain.**
  - Removing anergy raises every clone's gain (1 − a), so the copy index rises for any model that loses a damping term.
  - It needs a **gain-matched control**: replace a_i by its population mean (content-blind, same total gain), or re-tune θ_g to match FRVar.
  - It also needs the **decisive ablation for the claimed novelty**: drive anergy by the delayed *partner* stream β(φ(o_{t−τ}); r_i) instead of φ(own output). That is TAT/discontinuity without efference. If P1, P2 and P4 do not change, the efference input adds nothing.
- **Add two cheap baselines** that a "copy changes, not states" model must beat:
  - **gain × high-passed Delayed Mirror**, with gain, lag and τ_a tuned on val with the same trial budget;
  - **scaled Delayed Mirror + spectrum-matched noise**.

  Both are one- or two-dial models and would pass P2's "onset gain / sustained gain ≥ 1.5" criterion. So that criterion is not specific to the mechanism.

**Bottom line.** The sketch is a recombination, as it says. Its "no single dial" claim fails: θ_g is the dial, its two ends are the sketch's own ablations, and the same scalar removes the content specificity. Its test P1 would not detect the failure. The test plan is partly infeasible on released Seamless metadata: there is no session order, only 11 repeat pairs fall in val/test, and there is no within-person familiar/stranger contrast in val/test.
