# Critique: v3-ethology-signalling (release-reserve display process, RRDP)

Critic: an independent subagent that did not write the sketch. Written 2026-11-25T09:42:58Z under operator notes Q8 (critique round) and Q9 (novelty test). Nothing here was run on Seamless Interaction. The numbers in section 4 come from short simulations of the sketch's own equations (3)–(4) for one unit (code in the appendix). They check the algebra and are not evidence about people.

**Verdict: recombination, as the sketch itself says.** Named exactly: a **multivariate nonlinear Hawkes process / point-process GLM** (Pillow-style self-history and coupling filters, and Mei and Eisner's self-modulating intensities) with a **divisive resource gate on each unit's hazard**. The gate is Tsodyks–Markram depression; its mean field is the saturating "dead-time" law ν = g/(1 + g·κ̃/ρ). Its marks are a **frozen template codebook** (shot-noise output; a VQ-style motion dictionary as in Learning to Listen). The partner enters through a **matched-filter prefix parse** and a **state-switched release map**; the closest computational-ethology instance of that map is the GLM-HMM of Calhoun, Pillow and Murthy (2019), which the sketch does not cite.

**Central claim (the partner's share is not a function of one scalar; flat and copy are unreachable): does not survive as stated.** The share is a monotone function of the gain G. G runs the agent from vacuum activity (a Random-like listener) to a template-quantized delayed mirror, at a nearly fixed lag of about 200 ms, whenever the partner displays more slowly than the reserve ceiling. The refill-to-quantum ratio ρ/κ is a second dial. The tonic path A·m_t carries the partner into the face with no cap at all. A weaker claim survives (section 4b).

## Sources read for this critique

| Source | What I read, and how |
|---|---|
| Mei & Eisner 2017, "The Neural Hawkes Process", arXiv 1612.09328 | PDF text extracted locally. Read: abstract, the §1 paragraph on superadditive effects, §3.1–3.2.1 (Hawkes, D-SM-MPP with inhibition, softplus) and §7 conclusion. The rest was keyword-searched only, not read in full. |
| Mancini, Ferrari & Palagi 2013, Sci Rep 3:1527 (PMC3610402) | Full-text XML from Europe PMC, keyword-searched. Every quotation the sketch uses was checked; the paper was not read cover to cover. |
| Pillow et al. 2008, Nature 454:995 (PMC2684455) | Through a fetch tool that returned quoted passages from the model description. Not read in full. |
| Calhoun, Pillow & Murthy 2019, Nat Neurosci (PMC7819718) | Through a fetch tool that returned quoted passages from the first 100,000 of 137,081 characters (abstract, Results model sections). Not read in full. |
| Gratch et al. 2006, "Virtual Rapport" (IVA) | **Abstract line only**, from a search result. The DTIC PDF returned 403. |
| Project notes: research/ng-2022-learning-to-listen.md, research/react-challenge-baselines.md, research/seamless-interaction.md, research/harness/HARNESS.md | Read in full where relevant. |
| One local Seamless pair already on disk (V00_S0080_I00000377) | Used only to check effective dimensionality (in the enactive critique); nothing was downloaded. |

## 1. Parts list (novelty test)

| # | Part | Existing mechanism | Source (read) |
|---|---|---|---|
| 1 | Unit dictionary φ_k (seqNMF/CSC, frozen) | Convolutional dictionary; a motion codebook | The sketch's own table; L2L uses a learned motion codebook (project note) |
| 2 | Output a_t = A m_t + Σ γ_k(1+ξ) φ_k[t−s] | Shot noise / marked point process with stereotyped kernels, plus a linear readout of an SSM | — |
| 3 | Prefix parse e_j = σ(β[cos(Π^p φ_j[0:P], o) − θ_j]) | Matched filtering; attention with template-prefix keys; MOSAIC-style recognition through one's own repertoire | — |
| 4 | Hazard with partner cross-terms R(f) z | Coupled point-process GLM | Pillow 2008: "a set of coupling filters, which capture dependencies on the recent spiking of other cells" |
| 5 | Reserve gate (r−κ)_+/(1−κ) with consumption κ and refill ρ | Tsodyks–Markram depression. Functionally, a **self-history filter**: Pillow's "post-spike filter, which captures dependencies on spike-train history (for example, refractoriness, burstiness and adaptation)". Mei & Eisner's D-SM-MPP already allows "inhibition (α_{j,k} < 0)", including α_{k,k} < 0 | Pillow 2008; Mei & Eisner §3.2.1 |
| 6 | Mutual inhibition over antagonistic AU pairs | Lateral inhibition / WTA (the sketch cites Redgrave et al.) | — |
| 7 | Conflict term χ = Σ min(σ(u_k), σ(u_l)) r_k r_l → displacement units | A conjunctive feature routed to extra outputs (a gated product) | — |
| 8 | Frames f switching R(f) | **State-dependent sensorimotor mapping from partner cues to discrete display modes**: the GLM-HMM. "The GLM–HMM allows each state to have an associated multinomial GLM to describe the mapping from feedback cues"; states are "characterized by different mappings from feedback cues to song modes"; "transition probabilities are also parameterized by GLMs" | Calhoun et al. 2019 |
| 9 | ψ^p (rank-2 per-partner deformation) | Speaker adaptation (MLLR-like) | — |
| 10 | η^p habituation | Multi-time-scale habituation | — |
| 11 | Slow state m | Diagonal SSM | — |

Every part is an existing mechanism, so it is a recombination under Q9.

## 2. Closest prior work and the sketch's reading of it

**Mei & Eisner 2017.** Quotes checked against the PDF text and accurate: "conditioning future event intensities on the hidden state of a recurrent neural network that has consumed the stream of past events"; "Past events may now either excite or inhibit future events"; "superadditive, subadditive, or even subtractive". The sketch is right that every RRDP intensity lies inside the neural Hawkes family. It missed a closer point in the same paper: the simpler **D-SM-MPP** (§3.2.1) already relaxes the positivity constraint so that "αj,k ... range over R, which allows inhibition". A negative self-kernel is action-specific refractoriness. The only thing RRDP adds over it is that the gate is divisive (a ceiling on rate), not subtractive.

**Pillow et al. 2008.** The sketch cites it only for partner cross-terms. Its post-spike filter is the standard computational form of the RRDP's "action-specific exhaustion" ("refractoriness, burstiness and adaptation"). With the exponential nonlinearity ("the summed filter responses are exponentiated"), a negative post-spike filter is a multiplicative gate on the rate, which is what the reserve is.

**Calhoun, Pillow & Murthy 2019 (missed, and closer than anything the sketch cites for frames).** In fly courtship, a male produces discrete song modes ("sine, fast pulses (Pfast), slow pulses (Pslow) and no song"). The inputs are "male and female movements in addition to his changing distance and orientation to the female". Hidden states switch the cue-to-mode map and are themselves driven by cues, and "Using GLM filters from the wrong state worsened predictive performance." That is RRDP's partner-parse → frame → release map → discrete display, already fitted on real dyadic animal data. It has no reserves and no motor templates.

**Mancini et al. 2013.** Quotes checked and accurate: "both immature and adult subjects mimicked play faces (PF/PF; FPF/FPF) ... but not lip-smacking (LS)"; "the mother-infant dyads showed the highest level of RFM and the fastest responses"; "within 1 sec from the emission of the facial stimulus"; "did not show any facial expression in the 1 s prior to the trigger's stimulus". The sketch's reading is right: the design excludes the own-history test that H1 proposes.

**Human-agent listener systems (missed).** Rule-based virtual listeners that fire stereotyped backchannels from speaker cues predate this sketch. The abstract of Gratch et al. 2006 describes "a system, based on psycholinguistic theory, designed to create a sense of rapport between a human speaker and virtual human listener". I could not read its rules (403), so I claim nothing about them. It belongs in the prior-work search for "releasers set when and which, not how".

**Misquotes found:** none in the sources I could check. Lorenz, Tinbergen, Morris, van Iersel and Bol, Krebs and Dawkins, and Tsodyks and Markram are cited by the sketch from secondary knowledge, which it states honestly.

## 3. Reduction

Set the frame count F = 1, drop χ (v ≡ 0), and replace the divisive reserve by a negative self-kernel. What remains is a point-process GLM with coupling filters, which Pillow 2008 describes, with template marks. Restoring frames gives a GLM-HMM over display units, which Calhoun 2019 describes. Restoring the divisive reserve changes only the high-drive limit: a ceiling instead of sublinear growth. With an exponential link and a negative post-spike kernel of integral H < 0, the mean-field rate solves ν = e^{u+Hν}, which grows like u/|H|. With the reserve it saturates. **The one property the sketch claims as its own (section 2, "a property, not a computation") is this ceiling.** It is not new as mathematics: it is the mean field of synaptic depression and of a dead-time counter.

## 4. Break attempts

### (b) A single dial: the central claim

**The sketch's own algebra is right in mean field, but it does not show what the sketch claims.**
- I re-derived ν(G) = ρg/(ρ + κ̃g) with g = g0 + G·g_p.
- Simulating one unit at constant drive matches this law at low and middle drive: κ = 0.3, ρ = 0.214, g = 0.5 gives 0.250/s simulated against 0.250/s predicted.
- At high drive the simulation exceeds the stated ceiling ρ/κ̃ = 0.499/s, reaching 0.561/s at g = 50. The reason: fluctuations let r fall to about 0. The exact mass-balance bound is ρ/κ (0.714/s here), which the sketch states under eq. (4) but not in §3. S_max is therefore a mean-field quantity, and H2's "within 10%" test of it can fail at high drive for this reason alone.

**The partner's share is a function of one scalar.**
- S_k(G) = 1 − ν_k(0)/ν_k(G) is strictly increasing in G. That is the definition of a dial.
- The sketch shows only that the dial's endpoints move. The low end becomes vacuum activity, not flatness, which is a Random-like listener. The high end becomes S_max < 1 in long-run rate.

**The rate ceiling binds only if the partner displays faster than the ceiling.** One unit was simulated with the sketch's own equations: κ = 0.3, a ceiling of about 0.5/s (the sketch's figure), a vacuum rate of 0.05/s and a 200 ms prefix parse. The partner showed the matching display as a Poisson stream at 0.1/s.

| G | Partner displays answered within 1 s | Median lag (frames) | Lag SD (frames) |
|---|---|---|---|
| 0 | 0.04 (chance) | 16 | 8.6 |
| 16 | 0.69 | 10 | 3.7 |
| 64 | 0.93 | 8 | 2.7 |
| 256 | 0.93 | 6 | 2.8 |

At a 5/s ceiling, the share answered reaches 1.00 with lag SD 1.2 frames. So G runs from chance to "answer nearly every display, about 6 frames after its onset". That is a **delayed mirror at template resolution**, and the lag collapses to the parse's prefix length P.
- The sketch's claim (a)(iii), "lags ... can be zero or negative", cannot hold relative to the partner's onset through the parse. The earliest detection is P = 6 frames after onset. A lag of zero or less can come only from q_t or m.
- Whether real partners display more slowly than the ceiling is unmeasured on Seamless. Smiles and nods in conversation are plausibly sparse, but that is a guess, and the claim rests on it.

**Refill rate ρ and quantum κ are a second dial.**
- S_max = ρ/(ρ + κ̃·g0) → 1 as ρ/κ̃ → ∞, and the model then becomes an ordinary Hawkes process with G as its dial. The sketch concedes this case (κ → 0).
- ρ_k = ρ_k(m_t) is learned, and m receives the partner parse e_t (eq. 7). The ceiling itself can therefore be raised by the partner. Whether "scale every partner term by G" includes B's e_t column is not specified.

**Unit thresholds θ_j and the parse sharpness β act along the same dial.**
- A common downward shift of θ raises e_j for every partner window, matched or not. That is G plus a nonspecific baseline.
- Raising θ silences the parse, which is G → 0.
- They move the agent along the same S(G) curve. They add no new endpoint.
- The event-extraction threshold used to define training onsets is a further hidden choice; the sketch flags it in §6.

**The tonic path is an uncapped partner channel, so the "form" bound and the "information bound" fail as written.**
- §1(5) says A·m_t "does not depend on the partner". But eq. (7) feeds m with e_t (the partner parse), q_t (both partners' VAD) and the text embedding.
- The learning objective includes the AU residual term log N(a_t − â_t), so A is trained to explain whatever part of the listener's face the templates miss, including partner-predictable mimicry.
- e_j is a cosine, so it loses the partner's amplitude but keeps the direction of the partner's 200 ms window, through 48 soft detectors over a 144-dimensional window.
- A·B·e_t is therefore a learned, continuous, rate-unlimited filter from the partner's face to the agent's face, and its gain ‖A·B_e‖ is exactly the scalar dial §0 set out to remove.
- The 40 bit/s bound counts only the onset stream. With m carrying e_t at 30 Hz into a_t, the bound does not hold.
- **Fix (the sketch's to make):** remove e_t and q_t from m's input, or detach A from the residual loss, or bound ‖A B_e‖ and report it.

**What survives.** Suppose κ > 0 and ρ are fixed, the tonic path is cut, and the partner displays faster than the ceiling. Then the long-run fraction of partner displays the agent can answer is below 1, and the answer's form is the agent's own template. That is a real property of divisive gating, which a plain Hawkes process lacks. It is narrower than "not a function of one scalar".

### (a) Collapse into a delayed copy
- **Mostly reachable** (table above).
- With a release map that is mostly diagonal, which is what fitting to people who return smiles with smiles would give, the RRDP becomes "detect the prefix of my unit j in the partner, then play my unit j". This is motion matching: retrieve the stored continuation of the best-matching prefix.
- The "form is own" defence holds only to the extent that the templates differ from the partner's displays. The templates are fitted on the same population's AU streams, so they are built to reconstruct those displays.
- Through the tonic path (above), a continuous delayed filter is available as well.

### (c) A lookup table of past faces under scarce data
- **Partly.** Nothing stores the user's past faces, and the living stage adapts only about 200 numbers per partner. That defence holds.
- But the output is a concatenation of population segments of 0.3–2 s chosen by prefix similarity, which is a codebook decoder.
- The sketch's distinction (it looks up motor primitives, not reactions) is real but thin: a diagonal R with a prefix parse is a nearest-prefix retrieval.
- H3's scaling test, which asks whether NN's FD worsens faster than RRDP's as data shrink, is a reasonable way to check this.

## 5. The Seamless test: feasibility and whether it discriminates

**Feasible in principle, blocked in practice.** V00 has FAUValue (24 AUs at 30 Hz), is_valid, VAD and transcripts. Familiar and stranger pairs exist only in naturalistic sessions. The 195 repeat actor pairs are V00 improvised only, with no session order (research/seamless-interaction.md). The pilot download waits on Q11.

**Named-AU dependence.** H1 uses LipCornerPuller and CheekRaiser, and H3 uses PCC of LipCornerPuller. The harness treats the AU vector as **unlabelled**: the column order is unverified, columns 12 and 19 are byte-identical in the one inspected pair, and EyesClosed has a mean of 1.28. The harness has already recorded L2L's lip-curvature PCC as "Not computable as published on Seamless". H1 and the PCC parts of H3 cannot run until the column order is verified.

**H1 does not single out the mechanism.** OR ≤ 0.7 for a congruent response after one's own recent congruent onset is predicted equally by a point-process GLM with a negative post-spike filter (Pillow) and by Mei and Eisner's D-SM-MPP with α_kk < 0. H1 tests self-inhibition, not reserves.
- What would separate a divisive reserve from a subtractive self-kernel: the listener's response rate saturates as the partner's display rate rises (reserve) instead of growing sublinearly without bound (GLM). That needs high-rate partner stretches, which may be rare.
- **Add as a baseline:** a GLM with a post-spike filter and one partner gain G, swept exactly as in H2. If it matches RRDP on H1–H3, the reserve adds nothing.

**Open loop.**
- H1 and H4 (human side) are analyses of human data and are unaffected.
- H2 and H3 generate an agent's face against a recording. The recorded partner responded to the true listener, not to the agent, and the generated agent's reserves follow its own onsets, not the true listener's.
- Held-out log-likelihood with the true listener's onsets fed in (teacher forcing) is the clean comparison. Free-running L2 against ground truth mixes the mechanism with divergence of its own history.

**Against Median, Random, NN, Mirror and Delayed Mirror.** H3's FD, P-FD, variation and SI are distribution metrics, and any template sampler with a reasonable rate can beat Median and Random on them. The prediction that bears on the claim is H2's sweep against Mirror-blend (a good explicit one-dial baseline), but its prediction "at G = 64, CCC(agent, partner) ≤ 0.5" is at risk:
- by the simulation above, which answers about 93% of sparse partner displays at a near-fixed lag;
- by the tonic path.

H2 should report the answered fraction and the lag SD per unit as functions of G, together with the partner's display rate relative to ρ/κ.

**TLCC "lags ≤ 0".** These are not available through the parse (minimum 6 frames). If they appear, they come from q_t or m, which would itself show that the partner is entering through the tonic path.

## 6. Summary for the record

| Item | Finding |
|---|---|
| Verdict | Recombination: nonlinear Hawkes / point-process GLM + divisive (Tsodyks–Markram) hazard gate + template codebook marks + prefix matched filter + GLM-HMM-style state-switched release map |
| Missed prior work | Calhoun, Pillow & Murthy 2019 (state-switched cue-to-display maps in a courting dyad); Pillow 2008's post-spike filter as refractoriness; Mei & Eisner's own D-SM-MPP self-inhibition |
| Strongest break | G is a dial from vacuum activity to a ~6-frame delayed template mirror whenever partner displays are sparser than ρ/κ; the tonic path A·m_t ← e_t is an uncapped continuous partner filter |
| Second dial | ρ/κ (and ρ(m) is partner-driven) |
| Central claim | Fails as stated; survives only as "with the tonic path cut and the partner faster than the ceiling, the long-run answered fraction is < 1" |
| Test | Data exist; blocked by disk; H1 needs verified AU column order and does not separate reserves from a GLM post-spike filter; add a GLM-with-gain baseline |

## Appendix: the simulations (run in research/foundations/sims' uv environment; scripts not kept in the repo)

One unit, Δ = 1/30 s, eqs. (3)–(4) verbatim. Partner onsets are Poisson at ν_p; e = 1 for frames onset+6 … onset+11; z ← z + Δ/0.2 (e − z); u = −3 + G·z; λ = (r−κ)_+/(1−κ) · softplus(u); fire with probability 1 − e^{−λΔ}; r ← r + Δρ(1−r) − κ·fire. One simulated hour per cell. "Answered" means the agent's first onset falls within 30 frames after a partner onset. Mean-field check: constant g, 20,000 s per cell.
