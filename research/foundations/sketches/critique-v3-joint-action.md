# Critique: v3-joint-action ("Role-Swap Co-Representation with Reciprocal Offers", RSCR)

Independent critic, 2026-11-25T09:42Z, written under questions.md Q8 (critique round) and Q9 (novelty test). I did not write the sketch. No datasets or weights were downloaded. Counts in §5 were computed from metadata CSVs and research/harness/splits_v2.json that were already in the repository.

**Verdict: recombination** (I agree with the sketch's own verdict). RSCR is a **weight-tied two-channel generative model of the dyad**: one network cloned into two towers with argument order swapped, coupled across channels. Used asymmetrically, it filters the partner's channel and samples its own.

**The closest prior work was missed.** It is Nguyen et al.'s dialogue GSLM (dGSLM): "a two-tower transformer network with Cross-Attention and shared weights", made "speaker-independent", which learns turn-taking from two-channel conversation.

**On the dial.** RSCR has no *exposed* scalar that runs flat → copy. But that property comes from fitting by maximum likelihood, not from the swap tie. The sketch's own post-hoc noise scale c still sets the partner's share as an explicit function of one scalar (derived in §4b). So the README's literal target ("not a single scalar gain, or a function of one") is not met by the mechanism. It is only pinned, at c = 1, by the data.

## Sources and how they were read

| Source | How read |
|---|---|
| Nguyen, Kharitonov, Copet et al. 2022, "Generative Spoken Dialogue Language Modeling", arXiv 2203.16502v2 (TACL 2023) | PDF text extracted locally (pdftotext); §3.3 (DLM architecture and objectives) and §4.3 generation settings read. §5.2–5.3 results via a fetch tool. |
| Friston & Frith 2015, "A duet for one", *Consciousness and Cognition* 36:390 | Author PDF (fil.ion.ucl.ac.uk), text extracted. §3 and §4 read, and every quote the sketch uses was checked against the text. |
| Raileanu, Denton, Szlam & Fergus 2018, "Modeling Others using Oneself in Multi-Agent RL", arXiv 1802.09640 | PDF text extracted. The method section around the parameter tie, and the abstract. |
| Ng et al. 2022, Learning to Listen, arXiv 2204.08451 (HTML v1) | §5–5.2 via a fetch tool: baselines and the TLCC result |
| research/seamless-interaction.md, research/react-challenge-baselines.md, research/ng-2022-learning-to-listen.md, research/tran-2024-dim.md, research/harness/HARNESS.md | Project notes (secondary) |
| Hart et al. 2014; Noy et al. 2011; Kenny's Actor–Partner Interdependence Model (APIM) for indistinguishable dyads | **Not read by me.** Not relied on. The APIM with equal actor and partner effects for exchangeable dyads is the statistical form of the same tie, and it is worth checking in the primary source. |

## 1. Parts list

I accept the sketch's table with these additions:

| Part | Existing mechanism | Evidence |
|---|---|---|
| One f with swapped argument order, plus cross-coupling between slots, trained on both channels | **dGSLM's Dialogue Transformer LM** | "We train a single Transformer model which we clone into the two towers with shared weights, which allows the model to be speaker-independent without having to do permutation invariant training." The cross-attention block is added "to share information between different channels" (§3.3). |
| The same tie, for modelling an other | SOM | Verified: "the parameters of fother are the same as the parameters of fself … the two networks differ in their relative placement of the inputs". |
| Partner slot filtered, own slot sampled | Conditional generation with one channel teacher-forced: a Kalman-type or amortized posterior on one channel, prior sampling on the other | Standard. dGSLM generates "in both channels" from prompts (§3.3, §4.3), at "the default generation temperature of 1.0". I did not find a mode in dGSLM that clamps one channel, so this asymmetric *use* is RSCR's own. It is not a new computation. |
| State-conditional Σ_θ | A heteroscedastic Gaussian likelihood (deep state-space models) | |
| z± decomposition | Isotypic / normal-mode decomposition | The sketch's algebra is correct. A linear swap-equivariant map (F₁s^A + F₂s^B, F₂s^A + F₁s^B) acts as M₊ = F₁ + F₂ on z₊ and as M₋ = F₁ − F₂ on z₋. |

**No part is new.**

## 2. Closest prior work, and the author's reading of it

**dGSLM (missed, and closer than SOM).** It is a dialogue model, not RL goal inference. It has the identical weight tie with cross-channel coupling, and it is trained on two-channel conversation (Fisher, about 2,000 h). It is judged on turn-taking events.
- Its §5.2 shows that the cross-channel coupling is what produces realistic timing: "The lack of communication between the two channels during generation creates huge gaps and overlaps".
- **What RSCR adds over dGSLM:**
  - continuous AU and SSM state instead of discrete units;
  - explicit filtering of the observed partner channel;
  - the z± reading;
  - application to faces.
- None of these is a new computation.

**Friston & Frith 2015.** All five of the sketch's quotes are verbatim. Examples: "the expectations are without agency"; "Each bird listened for two seconds (with a low proprioceptive precision and a high exteroceptive precision)"; "We have not dealt with this aspect of communication here". **But the sketch misreads what the synchrony is.**
- The paper's "identical synchrony" is of the two birds' **posterior expectations**: "the posterior expectations show identical synchrony at both the first and second hierarchical levels".
- Their **outputs** alternate: "the sonogram is continuous over successive one second epochs – being generated alternately by the first and second bird". The listening bird "take[s] up the song, following on from where the other bird left off".
- So Duet's endpoint is shared *belief* with complementary *output* (turn-taking). It is not "failure (a) at the latent level" as the sketch puts it.
- In RSCR's terms, Duet's synchrony corresponds to RSCR's own partner-slot filtering succeeding (s^B tracking B). It does not correspond to s^A = s^B.

**SOM.** Quoted accurately. The sketch's description of how SOM differs is fair.

**Mirror-game work.** The sketch says it did not read Noy et al. 2011 in full and that it read Hart et al. 2014 "via the journal page". I did not re-check the Hart quote.

## 3. Reduction

> RSCR = the dGSLM/SOM weight-tied two-tower dyad model, in continuous multi-timescale SSM form with a heteroscedastic Gaussian innovation law, conditioned on the observed partner channel (filtering) while the own channel is sampled from the prior.

**Verdict: recombination.** The sketch's candidate novelty, "using the tie to pin the agent's own sampled innovation law to the partner's observed one", is a use of parameter sharing, as the sketch itself says. It is also weaker than stated (§4b, point 3).

## 4. Break attempts

### (a) Collapse into a delayed copy

1. **Copy is built into the attractor set.**
   - The sketch says every attractor is either swap-invariant ("shared amusement or mutual calm") or a swap pair. A swap-invariant state satisfies RS* = S*, that is **s^A = s^B**. With the shared readout D∘W, that gives **y^A = y^B**: the agent shows the partner's face.
   - This is exactly the "identical synchrony" the sketch calls failure (a) in Duet, now in the agent's own state, where Duet never put it.
   - In the linear approximation, the synchronization manifold z₋ = 0 is attracting iff ρ(F₁ − F₂) < 1. Its residual size is set by how strongly the z₋ noise (ν^A − Kν^B) is damped.
   - The sketch's P4 predicts *more* z₊ energy in familiar sessions, which means more copy with familiar partners.
   - Whether that is a failure depends on human data. But the mechanism contains no defence against copy in z₊. It only says "copy is reachable only if the training humans themselves copied."
2. **"Fitted conditional mean + human-level noise" is the whole anti-copy argument.**
   - P5's criterion is that the residual of y^A given B's past stays ≥ 80% of the human value.
   - The two-parameter baseline **g·Delayed-Mirror + spectrum-matched noise** also meets it, by construction.
   - So the criterion does not distinguish RSCR from a noisy delayed copy. REACT's finding (B_Mime FRCorr 0.38 against 0.03–0.19 for learned models; react-challenge-baselines.md, secondary) suggests the human conditional mean is close to a lagged mirror. RSCR's predictable part would then be that mirror.

### (b) A single hidden dial: the central claim

**What survives.**
- Γ_{A←B}(τ; S) is a state-dependent matrix Jacobian, so the partner's share is not a ray g·M(τ).
- With c = 1 and no rescaling of K, no free parameter of the model selects the share; the data do.
- Every likelihood-fitted conditional generator has that property: the untied ablation, dGSLM at temperature 1.0, a fitted L2L. So **the property is not evidence for the swap tie.**

**The derived dial: the sketch's own scale c on Σ.**
- In the linear-Gaussian approximation, the agent's output splits into a part driven by B's observed stream (variance V_m) and a part driven by its own sampled offers. The sampled offers enter linearly through f, so their variance scales with c: Var = c·V_n. The two parts are independent, because ν^A ⊥ y^B.
- Let R² = V_m/(V_m + V_n), the model's partner share at c = 1. Then

  **partner share(c) = R² / (R² + c(1 − R²))**

  **mirror-PCC(c) = r_h / √(R² + c(1 − R²))**,

  where r_h is the model's mirror-PCC at c = 1 (≈ human, if the fit is good).
- **As c → 0** the agent becomes **flat** (its variance falls to R²V) **and fully partner-determined** (share → 1, mirror-PCC → r_h/R). If the partner-predictable part is mostly same-AU lagged information (R ≈ r_h), mirror-PCC → 1: a low-amplitude copy.
- **As c → ∞** the agent becomes expressive and uncoupled (share → 0).
- So one scalar sets the partner's share monotonically. The README's target ("must not be a single scalar gain, or a function of one") is therefore met only in the sense that maximum likelihood fixes c = 1.
- **P1's sweep bounds decide the outcome.**
  - Take per-AU r_h = 0.09 (L2L's ground-truth smile PCC; ng-2022 note, secondary) and R² = 0.01. Then mirror-PCC is about 0.27 at c = 0.1 and about 0.03 at c = 10.
  - So the sweep moves mirror-PCC monotonically from below the human range to about 3× the human value, but stays under the 0.5 fail threshold.
  - With R² ≈ r_h², c = 0.1 gives r_h/√(0.1 + 0.9r_h²) ≈ 0.28, also under 0.5.
  - So P1 is calibrated to pass even though the dial exists. **The fail threshold should be "leaves the human 95% range", not "exceeds 0.5".**

**A second, empirical dial: the agent's person code π^A.** At deployment, π^A is a free q-dimensional vector. If the first principal component of the learned person codes tracks expressivity × mimicry (a common outcome for style embeddings, not shown here), moving π^A along it is a one-dimensional flat → mimic dial. P1 should sweep π^A along the top PCs of the training codes, not only K and Σ.

**A misstatement inside the proposition.**
- The sketch says the tied Σ is "bounded below by the observed innovation variance of the partner's role", and that the tie "ties the size of own offers to the partner's offers".
- Equivariance gives only Σ_A(s^A, s^B) = Σ_B(s^B, s^A): A's offer variance is what B's *would be in A's position*. It is not bounded by B's *current* observed offers.
- The two coincide only on the diagonal s^A = s^B, which is the copy manifold of (a).
- So the claimed coupling of expressiveness to the partner holds exactly where the agent is copying.

**Answer to (b): partly survives.** There is no exposed flat → copy dial and the share is a matrix, but this is a property of maximum-likelihood fitting, not of the mechanism. The share is an explicit monotone function of the one scalar c. The flat end of that sweep is also the partner-locked end.

### (c) A lookup table under scarce data

**This survives.** RSCR is a parametric rollout (about 2·10⁵ parameters) with no store of episodes, and the tie doubles the examples. The P5 nearest-segment test with Nearest Neighbour as positive control is adequate.

The residual risk is person codes π^B fitted on few minutes of data. That is overfitting, not lookup.

## 5. The Seamless test: feasibility and discrimination

**Feasibility** (counts computed here from repository metadata, harness split v2):

| Item in the sketch | Status |
|---|---|
| Inputs: V00 FAUValue v1 (23 AU), is_valid, VAD, transcripts; person-disjoint harness splits | Feasible, and consistent with the harness. |
| Baselines "as published … Delayed Mirror (15 frames)" | **Misquoted.** L2L §5.1: "delayed by 17 frames (≈0.5 s)". The harness uses 17. |
| Metrics: L2, FD, P-FD, Variation, SI (k = 15), TLCC, FRDiv/FRVar/FRDvs, E3; FRCorr/FRDist excluded | Matches the harness. Per-AU PCC against the human–human PCC is a labelled deviation (L2L's PCC uses lip curvature). |
| P3: named AUs (cheek/lip-corner, jaw/lips-part) across VAD turn exchanges | **Blocked until the AU column order is verified** (seamless-interaction.md: "Treat the order as unverified"). The turn exchanges themselves are derivable from VAD. |
| P4: "start interaction k+1 from the slow scene state at the end of interaction k of the same pair" | **Order is not released**, neither sessions nor interactions within a session. A same-pair against other-pair seeding contrast is feasible without order, if "k+1 after k" becomes "another interaction of the same pair". Under the harness split, only **6 repeat pairs fall in val (254 interactions) and 5 in test (194 interactions)**; 96 of the 195 straddle splits and are dropped. |
| P4: familiar vs stranger "person-level mixed model across the 160 V00 people who have both" | **None of those people are in val or test.** There, 0 persons have both kinds of naturalistic session, and stranger naturalistic interactions number 15 (val) and 21 (test). The within-person test can only be run on train people, which is not a held-out test. On test it is between-person, with a small stranger cell. |
| Budget | Plausible (about 2·10⁵ parameters, CPU/MPS). Blocked on Q11 (disk) like every download. |

**Would it discriminate the mechanism from the published baselines?**
- **P5 separates RSCR from Median, Random, NN, Mirror and Delayed Mirror** on FD and P-FD. Learned listener models do this routinely; DIM's Mirror P-FD is 87.11 against DIM-Listener's 12.95 (tran-2024-dim.md, secondary). So passing P5 says little about the mechanism.
- **P1's comparison family y = αx^B_{t−τ} + (1−α)·median is a deterministic straw man.** Any fitted matrix Γ beats a scalar × identity family on distance to the human Γ.
  - The informative null is a **fitted VAR (or the untied RNN) with one scalar on its cross-block, plus noise**.
  - The fail threshold should be "mirror-PCC leaves the human CI under any single-scalar sweep (c, K-scale, π^A along PC1)", not "> 0.5" (see §4b).
- **P2, tied against untied at equal budget**, is the only prediction that tests the sketch's mechanism. Keep it as the primary test.
- **Add two baselines:**
  - **g·Delayed-Mirror + spectrum-matched noise**, to defend P5's residual criterion;
  - **dGSLM-style symmetric joint generation**: both channels sampled, then scored only on A. This isolates the asymmetric filter/sample use from the tie itself.

**Bottom line.** RSCR is a recombination whose closest prior work is dGSLM (missed). Its quotes are accurate, but it misreads Duet's "identical synchrony", which is shared belief with alternating output. On the dial, RSCR is better than the eight v2 sketches, since no exposed scalar runs flat → copy. Even so, the absence of a dial comes from maximum-likelihood fitting, which the untied ablation shares. Its own Σ-scale c sets the partner's share as share(c) = R²/(R² + c(1−R²)). Its swap-invariant attractors are copy states. The tests are mostly feasible, but there is no session order, there are only 11 repeat pairs in val/test, and there is no within-person familiar/stranger contrast outside train. Only P2 discriminates the mechanism.
