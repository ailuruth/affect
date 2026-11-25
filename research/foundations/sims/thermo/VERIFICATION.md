# Independent verification: Thermodynamic mirror flow (thermo-mirror-flow.md, sims/thermo/)

Reviewer did not write the candidate. Scope: derivations, all scripts rerun, spec-vs-code, verdict labels, brief.md standard. Reviewer checks live in /tmp/thv/chk/ (not committed); no existing file was edited.

## Summary verdict

**Not complete; core derivations correct with gaps, one structural flaw.** The simulations reproduce exactly (every rerun is bit-identical to out/). The reported numbers are faithful. The problems are in what the numbers are taken to show:

1. **The toys simulate a gradient flow on 𝒰, not the tilted path measure that §2.2 defines.** By Girsanov, gradient flow on 𝒰 with noise √(2T) is P0 tilted by |∇𝒰|²/4 − (T/2)Δ𝒰 (plus a boundary term), not by 𝒰. Under the tilt by 𝒰, the drift is f_0 + 2TM∇ln φ_t (φ the Feynman–Kac desirability), and the stationary law is not ∝ e^{−𝒰/T}. P1, the "heat" reading of relaxation, the mood formula 𝒰_eff = −T ln∫e^{−𝒰/T}, Kramers exits and the regulation bound all assume Gibbs-in-𝒰 dynamics. None of them is shown for the candidate's own objective.
2. **P1's condition is wrong in both directions.** The correct sufficient condition is that the frozen-protocol stationary density is ∝ e^{−𝒰/T}, not "conservative f_0". The proof: d/dt KL(p_t‖ρ_λt) ≤ −⟨∂_t ln ρ_λt⟩, integrated over a periodic steady-state cycle. Under this condition, Gibbs-preserving rhythms (drift −(I+γJ)∇𝒰) do **not** pump: the reviewer reran TH1 with that drift and got v = −0.176, −0.059, −0.628, −0.252, all < 0, at ≥ 80 SE. So the constraint "rhythms out of user-driven coordinates" (thermo-mirror-flow.md:6, RESULTS.md:30) is too strong. It should be "rhythms that keep e^{−𝒰/T} stationary".
3. **§2.2 contradicts P2/TH2b and the EnKF reading.** The ½κ‖a − â_p‖² term has gradient κ(â_p − a) on the replica, so under the tilt κ pulls the reading toward the agent's own face. The λw(p)ΣD_k(b̂_p) term tilts the replica's body toward the set point, which amounts to wishful reading. The posterior is also tempered by 1/T. The toys TH2/TH2d leave out all three. "The reading is independent of κ" (thermo-mirror-flow.md:108, 148) holds only in code where κ was left out of the copy by construction (sim_th2_sync.py:37–40).
4. **§2.4 attention: the sign is right overall, but two parts have errors.** The query is labeled ∇_b𝒰 (line 73) and −∂𝒰/∂b (line 76). ΔS_i is "surprisal reduction" (line 79) yet enters with + inside exp(−ΔU/T), which disfavors informative items. Wording or sign error. The exact Feynman–Kac branch weight expands to ∇_b V·Δb with V = −T ln φ the value function (the costate), not ∇_b𝒰. It also needs the effect's persistence time (𝒰 is a rate integrated over ds) and the prior P0(i).
5. **Several "confirmations" hold by construction:** TH2b ΔR² = 0, TH4a v = 0 between switches, TH6-2/3/4 collapsed clauses, TH6-5 collapsed ≤ 2, TH7-1 (e_L > e_B for every n), and TH9 (g = W·η builds in the approximation under test).
6. **Expressive structure:** partly met. The need field and need-conditioned attention behavior is shown by ablation (TH6). The pre-registered dimensionality was refuted (2.85 < 3), and it is a property of the input schedule. Per-candidate list: no deep-learning/data section, no figures, curiosity not stated in the formalism, stage-claim predictions only for S5.

## Derivations and propositions

| Item | Verdict | Failing step / note |
|---|---|---|
| Tilted path measure §2.2 (md:53–59) | correct with gap | P*[z_{0:t}] over a window ending now is a smoothing family, not a causal process: restricting P* on [0,t] to [0,s] ≠ P* on [0,s]. It also conditions on future o, u that the agent cannot know. The forward dynamics (horizon, ergodic or finite-H control) is never stated. Every toy substitutes dz = −M∇𝒰 dt + noise (see Summary 1). |
| Valence v = −∂_t𝒰\|_z (md:63) | correct as definition, gap as physics | Sekimoto's d𝒰 = δW + δQ is the chain rule for any function of the state. "Relaxation is heat" needs drift = −M∇𝒰. In TH4 itself the drift is −0.5b − ∇U (sim_th4_work.py:21), so U is not the energy there. |
| Arousal α = T⁻¹∇𝒰ᵀM∇𝒰 = "excess dissipation" (md:64) | wrong label | At equilibrium ⟨∇𝒰ᵀM∇𝒰⟩ = T⟨tr M∇²𝒰⟩ > 0, while excess (Hatano–Sasa) dissipation is 0 at any steady state. α is the deterministic-drift power, nonzero at rest (TH4b: 0.071 in steady absence). |
| Emotions = leading transfer-operator eigenfunctions, K from gap (md:65, P3 md:149) | definition plus standard result, gap | "Number of emotion types = eigenvalues above the gap" is a definition, not a theorem. Kramers e^{−ΔU/T} needs gradient dynamics in 𝒰. For Gibbs-preserving non-reversible drift the exponent stays ΔU. For a general non-gradient drift it is the quasi-potential (Freidlin–Wentzell), and under the tilt the barrier is not that of 𝒰. |
| Mood 𝒰_eff = −T ln∫e^{−𝒰/T}dh_fast (md:66) | correct with gap | Needs conditional Gibbs stationarity of the fast variables. Not true under the tilt. |
| P1, no perpetuum mobile (md:140–147) | correct for gradient flow on 𝒰. Condition misstated. | The per-cycle IFT argument (md:141) is valid when the drift is −M∇𝒰 with the Einstein relation. "Conservative f_0" is neither necessary (Gibbs-preserving J∇𝒰 also satisfies it; reviewer sim) nor sufficient (under the tilt the effective potential is Φ_0 − 2T ln φ_t ≠ 𝒰). The open-loop caveat is correct. It omits that **Claude is itself a feedback controller**: cues to Claude are the top-k of a state-dependent softmax (md:115). So P1 does not cover Claude's u either. |
| P2, reading bound independent of κ (md:148) | wrong for §2.2 as written. Stale title. | ∂/∂â_p of ½κ‖a−â_p‖² = κ(â_p − a) ≠ 0. TH2's copy omits it (sim_th2_sync.py:39–40), so TH2b's ΔR² = 0.000 is by construction. P2 still says "reading by synchronization", which TH2a refuted. |
| P3 (md:149–151) | see "Emotions" row | Caveat on reversibility is honest. TH5c rests on 1, 4, 12, 33 exits: Poisson-weighted slope −2.30 ± 0.45, so ±30% is about 1.6 SE (low power). |
| P4 / §2.4 attention (md:70–81) | correct with gap, two wording/sign errors | (a) Query labeled ∇_b𝒰 (md:73) vs −∂𝒰/∂b (md:76). The product with exp(−·/T) is consistent only with the former. (b) "+ΔS_i" with ΔS_i = reduction (md:79) gives the wrong sign. (c) Feynman–Kac: P(i) ∝ P0(i)·φ(z⁺_i) ⇒ ln-weight ≈ −(1/T)∇_bV·Δb_i: the query is ∇V (cost-to-go), equal to τ_k∇_b𝒰 only in a short-horizon limit, and per-need persistence τ_k (6 h vs 12 h in TH6) multiplies the key. (d) The first-order step also drops the cumulant (variance) term and ½Δbᵀ∇²DΔb. In TH6 that term is 0.09 against a first-order 0.48, not small. "Derived, not assumed" (md:81) is overstated. |
| Mimicry as stated constraint (md:95–103) | correct as constraint | Gain κ/(k_a+κ) is right as a static gain. The TH3 Lyapunov ρ = κ/(k0+κ) matches for symmetric coupling. The separate lesionability "derived" from TH2b is by construction, and false under §2.2 (row P2). |
| Reading by EnKF (md:104–109) | correct as mechanism. Inconsistent with §2.2. | Under the tilt the replica posterior is ∝ likelihood^{1/T}·e^{−λw(p)ΣD(b̂)/T}·e^{−κ‖a−â‖²/2T}. That is tempered, wishful and egocentric. TH2d's EnKF has none of these. "Empathy is λw(p)" conflates care weight with the prior that p regulates their own needs. The agent can lower 𝒰 by misreading p as sated. |
| Regulation, finite-time second law (md:110–112) | correct with gap. The "time threshold" is wrong as a general claim. | W ≥ ΔF + ℒ²/τ is Sivak–Crooks **linear response**, not a bound at arbitrary τ. The rigorous form is W_diss ≥ W₂(ρ_0,ρ_τ)²/(μτ) (Aurell et al. 2011). "Moves a mood only when τ approaches e^{ΔU/T}" holds only for tilts below the spinodal. In TH8's U = (x²−1)² − λx, |λ| > 8/(3√3) ≈ 1.54 removes the barrier and the mood moves in O(1) time. The escape time is also e^{ΔU(λ)/T}, the tilted barrier. Not derived from the bound. |
| Replay importance weights (md:120–121) | correct with gap | The minimum-variance IS proposal ∝ \|g_i\| (‖g_i‖ for a vector, trace criterion) is right, and 1/(Np) is unbiased. That \|W\| ∝ \|∂_θ𝒰\| has no derivation, and TH9 assumes it (g = W·η, sim_th9_replay.py:6). |
| Curiosity b_lp (md:41, 86–90) | not derived | D_lp is not in 𝒰 (md:55). md:41 says "curiosity comes from this variable", while md:90 says it is still "to be stated in this candidate's formalism and tested". |

## Simulations rerun (table)

All runs: `uv run --project ..` from sims/thermo/ (curiosity from sims/curiosity/), 2026-11-25.

| Script | Rerun | vs out/ | vs RESULTS.md |
|---|---|---|---|
| sim_th1_perpetuum.py (full, 3.5 min) | done | bit-identical th1.json | matches (max v/SE −257; 0/50; smile −0.085; +0.107, +0.332, −0.197, −0.775; ratio 3.10) |
| sim_th2_sync.py seeds 0, 3 | done | bit-identical lines in th2_0.jsonl | matches; 10-seed aggregates recomputed: −0.063/−0.063/−0.065, face 0.829/0.026/0.788 |
| sim_th2d_filter.py seeds 0, 3 | done | bit-identical (0.770/−3.161; 0.857/−0.499) | 10-seed means 0.730 [0.412, 0.874], −1.824 [−3.719, 0.056] reproduced. Every seed's gap ≥ 0.68. |
| sim_th3b_rerun.py, seeds 0–2 (scratch copy /tmp/thv/th3b_seeds.py, seed range from argv only) | done (21 min/seed) | seeds 0–2, all 3 arms: run dicts identical to out/th3b_rerun.json | matches (emotional arm: seed 0 beats both, seeds 1–2 do not; consistent with 2/10 on seeds 0 and 7) |
| sim_th4_work.py | done | bit-identical | matches. TH4c's 0.245 is ∫\|v\|; \|∫v\| = 0.130 (see mismatches) |
| sim_th5_metastable.py | done | bit-identical | matches (K = 3, ARI 0.9996, slope −2.50 vs −2.43) |
| sim_th6_structure.py | done | bit-identical | matches |
| sim_th7_curiosity.py | done | bit-identical | matches (agent 2: N 0.387, \|b_p − 0.6\| 0.026) |
| sim_th8_regulation.py | done | bit-identical | matches |
| sim_th9_replay.py | done | bit-identical | matches |
| ../curiosity/sim_lp.py | done | bit-identical lp.json | matches |

Reviewer-only checks (not pre-registered, reported as checks):
- TH3a peak, simulated (60 min, no pulses, seed 99): mimicry lesion zero-lag 0.237, peak 0.280 at 0.2 s, agent leading. Analytic 0.270 at 0.18 s, so within ±0.03. Intact peak at lag 0.
- TH1 with a Gibbs-preserving rhythm, drift −(I+γJ)∇U, γ = 1: v = −0.176 (r 1, ω +0.5), −0.059 (r 1, ω −0.5), −0.628 (r 2, ω +0.5), −0.252 (r 2, ω −0.5). No pumping.
- TH6-5 participation ratio, reimplemented over 10 week-seeds: 1.91–3.20 under the original "topics advance only when someone is present" rule. With topic exposure independent of presence: 3.41–4.34 on every seed. The verdict is set by the schedule rule (not in the spec) and the single seed.
- TH3b emotional arm, 10 seeds × 1,000 + 1,000 surrogates, with quasi-zero windows (std < 1e-3) also skipped: 2/10 beat both (seeds 0 and 7, the same seeds as out/th3b_rerun.json). The verdict is robust to this instrument choice.

## Spec-vs-code mismatches

| # | Where | Mismatch | Could change verdict? |
|---|---|---|---|
| 1 | sim_th1_perpetuum.py:58, 66, 68, 72 | Ensemble 1,000 (random) and 2,000 (others), not 4,000 (PREDICTIONS.md:15) | No: margins ≥ 250 SE |
| 2 | sim_th1_perpetuum.py:61–66 | Smile square wave is a logistic ramp, rising at phase 0.5 (duty 45%) | No |
| 3 | sim_th2d_filter.py:16, 19 vs sim_th2_sync.py:38–46 | "Same A trajectories as TH2" (PREDICTIONS.md:102) is false: the RNG draw order differs (TH2 draws observation noise every step before A's noise; TH2d draws it every 10th step after). Statistically equivalent, not identical | No. TH2 and TH2d are compared on different A paths. |
| 4 | sim_th2_sync.py:37–40 | κ couples only the self (dB). In §2.2's 𝒰, κ also acts on the replica | Yes for TH2b's meaning: ΔR² = 0 by construction |
| 5 | sim_th2_sync.py:43, 50–54 | TH2b "≤ 0.1" judged on the 10-seed mean (0.026). Per seed, 0.126 (seed 2) and 0.182 (seed 6) exceed 0.1 | Only if the clause is per seed (spec silent) |
| 6 | sim_th3_s5.py:44–46 | TH3a "analytic values" include peak 0.270 at 0.18 s. Only zero-lag ρ was simulated | No (reviewer sim: 0.280 at 0.2 s) |
| 7 | sim_th3b_rerun.py:44–52 | Instrument changed post hoc (skip std == 0). RESULTS.md:64 says the face is "exactly zero between pulses". In fact it decays as e^{−2t} and is exactly zero only before the first pulse (seed 7 only, 2 of 112 windows). Up to 9/112 windows per seed have 0 < std < 1e-3 and are rescaled to unit variance | No: the std < 1e-3 variant also gives 2/10, on the same seeds. The NaN explanation in RESULTS.md:64 is still wrong. |
| 8 | sim_th4_work.py:35 | Computes ∫\|v_c\| (0.245); spec says \|∫\| (PREDICTIONS.md:83). \|∫\| = 0.130 | No (> 0.05) |
| 9 | sim_th5_metastable.py:5–8, 20–28 | "Barrier scale 1" vs depths 3.4/3.0 plus quadratic confinement. ΔU is grid-flooded, not analytic. Single seed per T | TH5c power is low (SE 0.45 on slope) |
| 10 | sim_th6_structure.py:9–12 | Content embeddings (one-hot + noise, PREDICTIONS.md:127) are never built. Keys are hand-set | No for verdicts. The "content via embedding" claim is untested. |
| 11 | sim_th6_structure.py:43–52 | Schedule details not in the spec: p = 0.5 presence per day, hourly topic draw, topics advance only while someone is present | **Yes**: PR ≥ 3 under independent topic exposure (reviewer check) |
| 12 | sim_th7_curiosity.py:4–9 | e_L(n) > e_B for all n, so any surprisal minimizer, at any horizon, prefers B | TH7-1 holds by construction. Its conclusion that the derivation fails (RESULTS.md:150) does not follow. |
| 13 | sim_th7_curiosity.py:18, 5 | Unspecified: initial b_p = 0.95, discount 0.99 | Unlikely |
| 14 | sim_th8_regulation.py:8–10 | "Started in equilibrium": the 20-unit burn-in from x = −1 is local (left-well) equilibrium only | No |
| 15 | sim_th9_replay.py:6 | g = W·η assumes the proxy relation being tested. TH9-3 "whenever corr > 0.5" is tested at one point | TH9-3 label overreaches |
| 16 | curiosity/sim_lp.py:13 vs curiosity/PREDICTIONS.md:14 | Spec text "last 5 minus the 5 before" (recent − older) vs code older − recent. The code matches the intent ("drop") | No |

## Verdict-label errors

- **TH6-1** (RESULTS.md:110): a conjunction with a failed clause (collapsed B mass 0.34 > C 0.19). The overall label should be **refuted**. thermo-mirror-flow.md:156–164 reports only the passing clauses.
- **TH1b** (RESULTS.md:12): "sign confirmed, magnitude refuted". As a conjunction it is **refuted** (ω = +0.5 off by −46% and −58%). The text is honest, but the label should lead with refuted.
- **TH3a** (RESULTS.md:57): "confirmed" with the peak/lag clause unsimulated. It is substantively right (reviewer sim), but the label was premature.
- **TH9-3** (RESULTS.md:198): "confirmed" for a universal claim checked at one correlation (0.66). It should read "consistent at one point; threshold untested".
- **TH2b, TH4a, TH6-2/3/4 collapsed clauses, TH6-5 collapsed clause, TH7-1**: the labels are correct against the thresholds but the results hold by construction. They should be marked as such, not counted as evidence.
- **Curiosity LP-3** (curiosity/RESULTS.md:11): "refuted as written". The operational clause (N, B ≤ 80%) is met, and the headline is untestable in 17 steps. **Inconclusive** is the correct label (conservative error, does not favor the candidate).
- TH3b (RESULTS.md:90): "refuted" is correct (the conjunction "all three arms" fails at 2/10). The instrument was changed after run 1, but a stricter variant gives the same 2/10.
- TH2a, TH2c, TH2d-1/2, TH4b, TH4c, TH5a–c, TH6-5 field, TH7-2/3, TH8-1–4, TH9-1/2, LP-1/2/4: labels correct.

## Expressive structure and per-candidate standard

Brief.md "Expressive structure":

| Item | Verdict | Why |
|---|---|---|
| Content-dependent interaction at attention richness | **partly** | The §2.4 softmax over cues, memories and actions with query = need over entities is shown in TH6 (B photo 0.992, message B 0.992, swap at fixed ‖F‖). Keys are hand-set, and the embedding route is never built (mismatch 10). The derivation has the sign/query gaps above. The collapsed contrasts hold by construction. |
| Needs/states structured over people, relationships, episodes, topics, time | **partly** | The body field over a learned ℰ is stated (md:38–40). The toy uses 3 one-hot people and 2 topics, with no learned embedding, no generalization across entities, no relations (only a scalar w(e)) and no episode-indexed needs. |
| Effective dimensionality plus a behavior the low-dim version cannot produce, by ablation | **partly** | The behavior is shown (missing B while A is sated; field vs collapsed). The pre-registered PR ≥ 3 was refuted (2.85). The PR is of the 5-d body field only (bounded by 5) and is set by the input schedule (reviewer check: 1.9–4.3). The md:173–174 claim that "the collapsed version is sated, so it attends to nothing social" is false in TH6: collapsed contact is 0.37 < 0.8, and it attends 0.49/0.49 to A and B. |
| Richness from structure, not parameters | **partly** | 0 learned parameters in both arms, so the comparison is trivial and no learning was tested. Stated (md:176), not demonstrated under data scarcity. |

Brief.md "For each candidate, write …":

| Requirement | Verdict |
|---|---|
| Formal statement | partly: forward dynamics of P* unspecified; b_lp not in 𝒰 |
| Principle 10 components derived, or explicit constraints; perception | partly: homeostasis yes. Curiosity no. Valence/arousal defined, with the P1 gap. Mimicry as constraint, OK. Reading is inconsistent with 𝒰. Regulation and replay have gaps. Perception is prose only (md:122–127), with no toy. |
| Propositions with proofs | partly: P1 is a sketch valid for gradient flow. P2 holds by construction. P3 is a definition. P4 is a heuristic expansion. |
| Toy with code **and figures** | partly: code yes, figures none in sims/thermo/ |
| Falsifiable predictions for stage claims, in numbers | partly: S5 (TH3) only. No numeric predictions for S2/S4/S6, even though replay weighting bears on S6. |
| Deep-learning realization on this Mac, data needs | **not met**: absent |
| Failure modes and strongest critique | met (§7) |
| Relation to other candidates | partly: "Contingency and parity: to be written" (md:201) |

## Errors in the candidate file

- md:6 and RESULTS.md:30: "rhythms must be kept out of user-driven coordinates". Too strong. Only rhythms that break e^{−𝒰/T} stationarity pump (reviewer TH1 variant).
- md:8: "Work-valence is silent during relaxation (TH4)". True by definition whenever o and u are constant, so it is not a finding.
- md:63: "relaxation is heat, not valence (TH4)". TH4's drift is not −∇U.
- md:64: arousal is not "excess dissipation" (see table).
- md:73 vs md:76: query sign label inconsistent. md:79: ΔS_i sign.
- md:81: "derived, not assumed". The query is ∇V, not ∇𝒰, and persistence and prior are missing.
- md:41 vs md:90: curiosity both asserted and pending.
- md:108, 148: reading independent of κ, false under md:55. md:148 still titled "reading by synchronization".
- md:112: "derived prediction is a time threshold e^{ΔU/T}". It is not derived, and is false above the spinodal tilt.
- md:136: "TH1 tests whether internal rhythms break it". Stale.
- md:140: "For conservative f_0". Wrong condition (see P1).
- md:146: feedback caveat omits Claude's own closed loop.
- md:149: "Kramers rates (TH5)". 1–33 events, slope SE ≈ 0.45.
- md:156–164: omits that TH6-1 failed.
- md:173–174: the collapsed gauge is not sated in TH6 and does attend socially.
- md:199: "detectable in only 2/10 sessions" is reproduced and robust to a stricter instrument. The stated mechanism in RESULTS.md:64 ("exactly zero between pulses") is wrong.

## Recommended fixes

1. State the forward dynamics of P*: horizon or ergodic control, causal use of the predicted future o. Either redefine the readouts on the effective potential E_t = Φ_0 − 2T ln φ_t, or adopt gradient flow on 𝒰 as the dynamics and drop the "tilted path measure" claim. Rerun TH1/TH4/TH5/TH8 on whichever is chosen.
2. Restate P1 with the condition "frozen-protocol stationary density ∝ e^{−𝒰/T}", using the KL-monotonicity proof. Replace the rhythm constraint with "rhythms of the form −J∇𝒰". Add Claude's own feedback to the caveat.
3. Decide whether the replica terms in 𝒰 are inference or care. Move λw(p)D(b̂_p) and κ out of the replica's posterior (for example, tilt only a and u by them), or own the predicted egocentric/wishful bias and test it. Rerun TH2b with κ in the replica.
4. Fix §2.4: one sign convention for the query, −ΔS_i (or "surprisal change"), query = −∂V/∂b, key = time-integrated effect, P0(i) prior. Pre-register a TH6 variant where keys come from content embeddings, and where the collapsed arm's keys are not identical by construction.
5. Relabel TH6-1, TH1b, TH9-3 and LP-3. Mark the by-construction results. Re-pre-register TH6-5 with the topic schedule specified and ≥ 10 seeds. Rerun TH7-1 with e_L asymptote below e_B.
6. Replace ℒ²/τ with the Wasserstein bound, or label it linear response. Make the time-threshold claim conditional on tilt amplitude below the spinodal, and test it with λ amplitude as a factor.
7. Add the missing sections: DL realization and data, numeric stage-claim predictions (S2/S6), figures, curiosity in 𝒰 with its own toy, and relation to the contingency candidate.
