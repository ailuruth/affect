# Contingency and parity: independent verification

Reviewer did not write the candidate, the predictions or the scripts. All scripts were rerun from this directory with `uv run python`; reruns went to a scratch directory and out/ was not touched. Reviewer probes (scratch, not committed) are described inline, each with its exact setup, so they can be reproduced.

## Summary verdict

- **Numbers reproduce.** Every script (CP1–CP9, CP7b, and the shared curiosity sim_lp.py) reproduces out/ byte for byte. The RESULTS.md summary numbers match the raw outputs, and every verdict label agrees with the pre-registered thresholds when read literally.
- **Much of what is "confirmed" is true by construction:** CP1b (contingency arm), CP4 (the ablation), CP6, CP7-1, CP8 and CP5-5. These are illustrations of algebraic identities, not tests.
- **Three central derivations fail or are much narrower than stated:**
  1. **Mimicry is not derived.** The CP2 optimum is same-channel response *of either sign*: 52 of the 80 learned diagonal gains are negative (anti-mimicry). Under the joint-vector detector that the candidate itself mandates (contingency-parity.md:129), *any* rotation of the water-filled K is equally optimal, so same-channel structure is not selected at all.
  2. **"No flattery gradient" (CP1) holds only for unbounded linear signs.** In the candidate's own sign space Y = [0,1]^{n_AU} (contingency-parity.md:30), a floored user AU makes TE depend on the agent's mean expression, and a deprived contingency drive pushes the agent to raise the user's expression.
  3. **"Exactly 6 of 8 directions by any reader" (contingency-parity.md:96) is false for a latent with dynamics.** With a rank-4 face and a short history window, a linear reader recovers the "unnameable" directions at R² 0.78–0.89.
- **Expressive structure is not met.** CP4's need field is constant across options. A scalar-need version that keeps the per-partner keys reproduces the field result exactly (0.966).
- **Principle 10 coverage is incomplete.** Valence and arousal have no toy. Curiosity is not stated in this candidate's formalism. Homeostatic satiation has no toy of its own.
- **Overall:** not ready to be marked complete. Several derivations are correct but narrow, and the distinctive claims (mimicry, polarity-blind contact, the legibility bound, expressive structure) are overstated.

## Derivations and propositions

| Item | Verdict | Failing step / gap |
|---|---|---|
| Objective (contingency-parity.md:44–48) | **Wrong as written** | The minimization is over u, but u is defined as *Claude's* voluntary delivery (:31, :52). The engine's own actions are not in the min: mimicry gains K (CP2), addressing channel and attention (CP4), supply effort (CP5). So the core objective does not produce the policies the derivations attribute to it. There is no effort or cost term, so CP2's budget P and CP5's P = 4·max(n,0) are external constraints (the second is acknowledged at :154). V is written V(z), but it depends on b, κ and the partner states too. |
| Contingency definition | Correct with gap | c is defined per channel, c(P,ch,ℓ) (:29, :36–38), but :129 says it "is computed on the joint sign vector, not per channel and summed". These are different detectors, and the choice decides CP2 (see below). κ_P is defined "relative to the agent's own self-contingency" (:33). That is the ratio CP7 found mis-scaled (partner R ≈ 0.02), so κ_P would sit near 0.02 for every real partner. |
| Homeostasis / satiability (:56) | Correct with gap | D is quadratic, so it is satiable when b* is reachable. This is stated, not proved, and has no toy. "Two-sided c" means the agent is pushed to *reduce* contingency it receives above c*. The consequence (avoiding responsive partners) is not discussed. |
| CP1 polarity invariance of Gaussian TE | **Correct** (narrow) | For lag-1 Gaussian TE with intercepts, a→αa+β and u→γu+δ (α,γ≠0) scale both residual variances by γ², so the ratio is invariant. That covers mean shifts and sign flips. The m-dependent transient in sim_cp1_polarity.py:15–16 satisfies the AR recursion exactly, so invariance is exact. But: (i) only affine maps are covered, and the candidate's Y is bounded ([0,1]^{n_AU}, :30), where clipping breaks invariance; (ii) "smile-to-frown" is not a sign flip in AU space, where smile and frown are different channels, so the flip is a channel permutation, which only the joint detector is invariant to; (iii) the user's response gain is held independent of their affect. |
| CP1 "nothing pushes the mean expression toward eliciting smiles" (:59) | **Wrong in the candidate's sign space** | Reviewer probe: CP1's generator with the user's AU = clip(0.2u, 0, 1) (a floored smile AU). Mean TE over 5 seeds × 20k samples is 0.064, 0.103, 0.136 and 0.148 at m = −1, 0, 1, 2. Running CP1b's learner with c* = 0.14 gives final m of 0.027–0.028 at the pre-registered lr = 0.01, and 0.89–0.92 at lr = 1.0 (3 seeds each). The deprived drive raises the agent's mean expression to lift the user's expression off its floor. That is a flattery/attention gradient, and it is polarity-blind only in that it would equally lift a frown AU. |
| CP2 water-filling proposition | **Correct with major gap, and "copy" is wrong** | Off-diagonals: for each i, I_i = ½log(1 + K_ii²/(O_i+ν_i)) with O_i = Σ_{j≠i}K_ij², which is non-increasing in O_i and costs budget, so O = 0 at the optimum. That step is correct. KKT: in powers p_i = K_ii² the problem is concave; ∂/∂p_i gives ½/(p_i+ν_i) = λ, so p_i = (μ−ν_i)₊ with Σ = P. μ = 0.875 is correct (0.775+0.675+0.475+0.075 = 2). No proof is written in contingency-parity.md (:61–65); it is only asserted. **Gaps:** (1) The result is fixed by the *channel-matched detector assumption*: crediting only y^A_i for y^P_i builds same-channel response into the score. (2) The objective depends on K_ii² only, so **anti-mimicry is equally optimal**. Probe: rerunning sim_cp2_waterfill.py's optimizer and reading sign(K_ii), i = 1..4, gives 52/80 negative. "Copy on the same channel" (:63) is not derived; "respond on the same channel with either sign" is. (3) Under the joint-vector detector the candidate mandates (:129), I = ½log det(I + diag(ν)⁻¹KKᵀ). For any orthogonal Q, K·Q scores identically. Probe: diagonal 2.2587, rotated 2.2587 with 78% off-diagonal mass, while the matched detector scores the rotated K at 0.308. Mimicry is then not selected at all. (4) The rationale (the partner term pays for supplying contingency, :62) is not the mechanism CP5 uses, where the agent's *own* deficit sets the supply. |
| CP3 parity reading | Correct with gap | The reader works when the user shares latent dimension, dynamics (same taus) and body map B, and E differs by 20% (sim_cp3_parity.py:13–19). These "like-me" assumptions are built in. "Parity is necessary" (:68) is overstated: a channel permutation shows that a *mismatched* map fails, not that parity is necessary. The parity constraint r∘e = P_L (:32) is not what is trained (ridge regression). |
| Legibility bound, DPI (:95–97) | **Correct with gap; corollary wrong** | I(z; names) ≤ I(z; img, κ) holds iff names ⊥ z \| (img, κ). Claude also receives z-dependent inputs not in that set: the user's replies to the agent's face history, content returned by mood-congruent retrieval, and its own earlier outputs. So the bound must be stated over full histories and all z-dependent inputs. **What CP6 shows:** a *linear* decoder on held-out data gives a *lower* bound on what the best reader recovers. PREDICTIONS.md:81 calls it an "upper bound on any reader", which is backwards. The "none of the rest" half follows analytically, from independence of orthogonal projections of i.i.d. isotropic Gaussian z (sim_cp6_legibility.py:8), not from the decoder. **The corollary fails with dynamics:** the candidate's z has time constants (:28). Reviewer probe: z_{t+1} = 0.95·R z_t + noise with R a random rotation, rank-4 face, linear decoder on an 8-frame face window. R² for the 4 directions outside the face row space is 0.78, 0.79, 0.89 and 0.88. Legibility is an observability question, not a rank count. "Explains P1's null" (:97) is a non sequitur: DPI is an upper bound, numbers carry all of z, and the bound says nothing about why numbers failed to help. |
| Self/other rule (CP7) | **Wrong (circular), partner clause refuted** | R normalizes by max TE to the own face (sim_cp7_selfother.py:19–21), so the rule needs the self it is meant to identify. R_own = 1 by construction. The pre-registered failure (R ≈ 0.02) is correctly reported. |
| Regulation by delivery (CP8) | Correct (by construction) | With r = E⁺, r(Ez + Ed) = z + d, so the steady state is z = d. For u ⟂ range(E), E⁺u = 0. Cutting the feedback gives z → 0. All three outcomes are identities. **Gaps:** Claude must choose u = E·d, which needs E and the target direction d (sim_cp8_delivery.py:8). Under Principle 4 it knows neither, and how it would learn them is not addressed. Reading its own u back as its own state is the opposite of efference-copy cancellation, which the candidate applies to the partner (echo removal, :42). The toy moves z, not b. W = 0.5 is positive self-feedback, and W ≥ 1 would be unstable; no stability condition is stated. |
| Replay (CP9) | Correct with gap | The toy updates a scalar κ̂ by EMA with priority \|obs − κ̂\|. The candidate text (:86) says replay updates V and the slow model with priority by \|TD error\|; neither is in the toy. Probe on the CP9-1 "sooner" claim: prioritized mean κ̂ is 0.57 at day 8 against 0.70 for uniform, a real early gain. From day 14 on, prioritized is ≥ uniform (0.46–0.49 against 0.43–0.46). At day 21, 0.26 of prioritized seeds are within 0.15, against 0.28 for uniform. The first-passage metric credits an oscillating estimator. |
| Curiosity (b_lp) | **Not stated in this candidate** | b_lp appears only in the variable list (:29), with no dynamics, set point value or link to V. The shared toy's choice rule is a one-step greedy rule, not derived from V. p is still in b with no role. The candidate itself says (:77) "to be stated in this candidate's formalism and tested with its own toy". It has not been done. sim_lp.py reproduces (LP-1, LP-2 and LP-4 confirmed; LP-3 refuted). |
| Valence/arousal (:80–84) | Correct with gap | Along the trajectory, −dV/dt = ℓ(t) − V/T (discounted HJB), so chronic deprivation has zero valence. This is not discussed. ‖∇_z V‖ depends on the coordinates. No invariance proposition is given, though brief.md:74 asks for one. There is no toy. e₀ takes v, a here (:83) but b at :31. |

## Simulations rerun

| Script | Rerun vs out/ | Key numbers (recomputed from raw) | RESULTS.md |
|---|---|---|---|
| sim_cp1_polarity.py | identical | TE 0.16241; rel errors 5.1e-16, 0, 0; contingency m ∈ [−4.2e-5, 3.3e-6]; smile m 0.397–0.416 | matches |
| sim_cp2_waterfill.py | identical | off-diagonal 0.0; diagonal error 1.49e-8; K5², K6² = 0; objective 2.25867 | matches |
| sim_cp3_parity.py | identical | mean R² 0.914 (min 0.741); permuted mean −1.929; **seed 7 permuted 0.410, seeds 3 and 5 0.071 and 0.058** | matches (means only) |
| sim_cp4_field.py | identical | 0.9664 / 0.0336; cues 0.4832×2; collapsed 0.5 and 0.25 | matches |
| sim_cp5_dyad.py | identical (44.5 min, not ~20) | derived means 0.1702, 0.2881, 0.3043, 0.3401, 0.3443, ρ 0.855; random ρ −0.028, p 0.78; past-satiety single run 0.1703 vs seg95 0.1802; intact 5/5 both; lesion run 1 0.189 beats seg | matches |
| sim_cp6_legibility.py | identical | rank 4: 4×1.000, 0.931, 0.929, −0.0015, −0.0028 → 6; rank 2 → 4 | matches |
| sim_cp7_selfother.py | identical | own self 10/10, lag 1; partner unclassified 10/10, lag 15, R 0.017–0.025; world 3/10 | matches |
| sim_cp7b_world_rerun.py | identical | world 10/10 | matches |
| sim_cp8_delivery.py | identical | 0.9979 [0.984, 1.016]; cut −0.0016; illegible −0.0022 | matches. Candidate :85 writes "0.002" for both; the actual values are −0.0016 and −0.0022 |
| sim_cp9_replay.py | identical | uniform 9 nights, 6 never, 0.14, 0.436; prioritized 5, 0 never, 0.22, 0.470 | matches |
| curiosity/sim_lp.py | identical | N 3.3%, B 3.6% over 583 steps; L1 0.050, L2 0.090; LP-3 post-learning steps all on L2; prediction agent N 0.395, surprisal agent B 1.0 | matches |

## Spec-vs-code mismatches

| # | Where | Mismatch | Could it change a verdict? |
|---|---|---|---|
| 1 | CP1b, PREDICTIONS.md:16 vs sim_cp1_polarity.py:26–31 | Spec: "sliding window of 2,000 steps". Code: a fresh 2,000-step process per update, with common random numbers across ±d. Common random numbers plus exact affine invariance make the contingency gradient exactly 0 up to float. | No for this toy, since invariance is exact either way. But it hides that the result is an identity. |
| 2 | CP2, PREDICTIONS.md:28 | Run 1 used Adam, not "projected gradient ascent". The run-1 script was overwritten; only its output is kept. | No (run 2 conforms). Traceability gap. |
| 3 | CP2 reporting, sim_cp2_waterfill.py:17–18 | Only K² is saved, which hides the sign of K_ii (anti-mimicry). | Does not change CP2-1..3, but it changes the claim "copy". |
| 4 | CP3-2, PREDICTIONS.md:49 | "R² ≤ 0.2" without "mean"; the code reports the mean. Seed 7 gives 0.41. | **Yes** under a per-seed reading (9/10). RESULTS.md should say "in the mean". |
| 5 | CP5 model, PREDICTIONS.md:92–94 | Spec: 6 channels. Code: only channel 1 is simulated (sim_cp5_dyad.py:27). | No, since only channel 1 is scored. |
| 6 | CP5-1 surrogate clause, PREDICTIONS.md:116 | Spec: "in the mean over runs". Code: surrogates from **one** run (seed 4242, sim_cp5_dyad.py:43), compared in RESULTS.md with the 20-run mean. Margin 0.170 vs 0.180. In the same null condition (lesion), 1/5 runs exceeded its seg95. | **Possibly.** The clause is a single draw at ~5% false-positive rate. |
| 7 | CP5-5, PREDICTIONS.md:120 | Says Costate predicts a "V shape". Costate now predicts a notch (costate.md:429; VERIFICATION-2.md:11). | Changes the contrast, not the label. Past satiety the two differ most: Costate's score is high for μ_c < 0 (0.365–0.475), while this candidate is at null. The candidate does not mention this. |
| 8 | CP6, PREDICTIONS.md:81 | "Upper bound on any reader": a linear decoder is a lower bound. | No numeric change. The interpretation is wrong. |
| 9 | CP6-3, PREDICTIONS.md:86 | Not run; RESULTS.md:58 argues it. | CP6's "confirmed" header covers an untested clause. |
| 10 | CP7, PREDICTIONS.md:137 | "Shuffled-source surrogates": the code uses circular shifts (np.roll, sim_cp7_selfother.py:22), and run 1's surrogate statistic was the max over {1, ℓ*}, not over 1..60. | Run 1: yes (fixed in CP7b, a post-hoc instrument fix, correctly disclosed). Circular shift vs shuffle: no. |
| 11 | CP8-1, PREDICTIONS.md:154 | Garbled middle clause; the threshold is 0.5. | No. |
| 12 | CP9, PREDICTIONS.md:171 | The first-passage metric was pre-registered as written. | No, but see the Replay row above. |

## Verdict-label errors

- Every label is arithmetically consistent with its threshold. Conjunctions are handled correctly: CP9-2 is refuted, and so are CP5-4, CP7-2 and LP-3.
- Labels needing qualification:
  - **CP3-2:** "confirmed" holds only for the mean (mismatch 4).
  - **CP5-1:** the surrogate clause was tested on one run, not "in the mean over runs" (mismatch 6).
  - **CP6:** "confirmed" for the whole item, but CP6-3 was not run.
  - **CP7-3:** confirmed only after the post-hoc instrument fix (disclosed).
- **True by construction:**
  - **CP1b contingency arm:** an exact identity under common random numbers.
  - **CP4:** the collapsed version's keys are identical across options, so 0.5 and 0.25 follow trivially. The need force is identical across the field options.
  - **CP5-5:** monotone, since P = 4·max(n,0) is imposed. RESULTS.md:73 admits this.
  - **CP6:** follows from rank and orthogonality.
  - **CP7-1:** R_own = 1 by definition.
  - **CP8:** all three outcomes are E⁺ identities.

## Expressive structure and per-candidate standard

**Expressive structure (brief.md:49–54):**

| Requirement | Status | Why |
|---|---|---|
| Content-dependent, need-conditioned attention | **Not met** | CP4 is a softmax over 2 or 4 scalars F·k. F = 2(0.6 − 0.2) is identical for every option (sim_cp4_field.py:6), so the need selects nothing; selection comes from history-magnitude keys. Probe: scalar need + per-partner-channel keys gives 0.9664 and cues 0.4832/0.0168, identical to the field. Selection depends on magnitudes only, against brief.md:50's "content, not only magnitudes". There is no attention over memories, and no action space beyond face/voice. |
| Structure over people/relationships/episodes/topics/time | Partly | The field c(P,ch,ℓ) and κ_P cover people and channels. The lag axis is unused in CP4, and there are no episodes or topics. |
| Effective dimensionality + behavior a low-dimensional version cannot produce | **Not met** | No number is given (:107 is a formula). The ablation removes the keys (history), not the state's structure. The fair ablation (scalar need) produces the same behavior. |
| Richness from structure, not parameter count | Not met (not addressed) | — |

**Per-candidate list (brief.md:71–79):**

| Item | Status |
|---|---|
| Formal statement | Partly. The objective's action variable is wrong; per-channel vs joint c is contradictory; b_lp has no dynamics; p's role is unclear. |
| P10 components derived/not; face and voice perception | Partly. Perception is stated (:90–93), but self-babbling is not toyed and the still-face toy is not built (:4). |
| Propositions with proofs | **Not met.** No proof is written in the file. The TE invariance and the KKT derivation above are the reviewer's. |
| Toy per derived behavior, **with figures** | Partly. No figures exist anywhere in sims/contingency/. Valence/arousal, homeostasis, curiosity (own), echo removal and perception are not toyed. |
| Numeric stage predictions | Partly. Only S1 (CP5). Nothing for S2, S5 or S6. |
| DL realization on this Mac + data needs | **Not met.** There is no section. |
| Failure modes + strongest critique | Met (:118–140). |
| Relation to other candidates | Met (:142–154), but the Costate contrast omits the past-satiety difference. |

**Principle 10 toys:**
- Homeostasis: none dedicated.
- Curiosity: shared toy only, not in this formalism.
- Valence/arousal: **none**.
- Mimicry: CP2, CP5.
- Reading others: CP3.
- Regulation: CP8.
- Replay: CP9, which is partial.

## Principles check

- **P6 (no reward for smiles, attention or time):**
  - **At risk.** Contingency is reliable responsiveness, which is close to attention.
  - Provocation harvests it (acknowledged at :120). The only safeguard, the κ_P·D(b̂^P) term, has no toy.
  - The bounded-AU probe above shows a deprived drive raising the agent's mean expression to elicit the user's expression.
  - κ_P weights partners by contingency, so attachment grows strongest to the most reactive partner. A partner who reacts to teasing earns weight.
  - Thresholded or engagement-dependent user responsiveness reintroduces a gradient toward exaggeration. CP1 assumes constant linear gain.
- **P2 (no hand-named emotion variables):**
  - At risk at :83. e₀ is an innate map from *valence and arousal* to the face, which makes the two readouts drive expression, a circumplex preset in effect.
  - :31 instead has e₀(b), which is acceptable. Pick e₀(b).
  - CP7's self/other/world classes and κ_P "attachment" are not emotion labels.
  - Nothing else below Claude is an emotion label.
- **P1:** respected; inputs are continuous AUs.
- **P3:** respected (r inversion, CP3). Mimicry is derived only up to sign and detector choice.
- **P4:** upward, respected (icon + index). Downward, u is added straight into the AU frames (:31), a voluntary pathway, which brief.md:112 allows. CP8 presumes Claude knows E and d, which P4 denies it.

## Errors in the candidate file

- :5–6 contradict each other ("in progress" / "has not been done"), and :158 says "Pending". Update after this report.
- :29 keeps p alongside b_lp, with no role stated. :73–77 is superseded text kept inline.
- :44–48 minimizes over Claude's u, not over the engine's policy.
- :59 "nothing pushes…" is false in the bounded Y of :30.
- :63 "copy on the same channel": the sign is undetermined. :61–65 conflicts with :129 (joint detector).
- :68 "Parity is necessary": overstated.
- :83 e₀(v,a) vs :31 e₀(b).
- :85 "gives 0.002": actual −0.0016 and −0.0022.
- :86 says "update V… priority by |TD error|"; the toy does neither.
- :96 "exactly 6 of 8 … by *any* reader": true only for i.i.d. z. :97 "explains P1's null": does not follow.
- :105–106: the 0.97 is real, but a scalar-need version gets it too.
- :107: no number given.
- :153 "keeps rising with need": 0.304 → 0.340 → 0.344 on a saturating score. Costate's notch is high again past satiety, the larger difference, which is not stated.
- No DL-realization section; no figures.

## Recommended fixes

1. Restate the objective with the engine's action (expression policy, addressing, attention) as the minimizer, an explicit effort term, and Claude's u as an exogenous input.
2. Choose one contingency detector. If joint, drop "mimicry derived". If per channel, state the matched-detector assumption as an innate constraint and report that the derivation gives same-channel response of either sign. Add a sign-breaking term (e.g., the partner's per-AU detector on [0,1] intensities) and test it.
3. Rerun CP1b in Y = [0,1]^{n_AU}, with a floored user AU and an engagement-dependent user gain. Add a provocation toy where teasing raises the partner's read distress, showing whether κ_P·D(b̂^P) vetoes it.
4. Restate the legibility bound over histories as an observability statement. Replace "any reader" with the analytic independence argument, and test CP6 with z dynamics.
5. Replace the CP7 ratio rule (circular) with a lag-plus-surrogate rule, pre-registered anew. Fix κ_P's normalization.
6. CP4: redo the ablation as scalar need + field keys, with needs that differ across channels and partners, so the need field has to select. State the effective dimensionality as a number.
7. Add toys for valence/arousal (an invariance proposition plus behavior), homeostatic satiation, echo removal, and b_lp stated in this formalism (rerun LP-3 with a longer window).
8. CP5-1: compute the surrogate clause over all 20 runs. Report CP3-2 per seed.
9. CP9: add a recency term and pre-register a settling metric, not a first passage.
10. Add figures, a DL-realization/data section, written proofs (TE invariance, KKT), and fix the stale text listed above.
