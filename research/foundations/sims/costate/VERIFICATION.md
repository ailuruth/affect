# Costate: independent verification

Reviewer: independent subagent that did not write costate.md or the sims. Date 2026-11-25.
Scope: research/foundations/costate.md, sims/costate/{PREDICTIONS,RESULTS}.md, all scripts, out/.
Scratch checks (not part of the project) were run against env_t1.py and sim_t1b_modelbased.py; their numbers are quoted below.

## Summary verdict

- **Reproducibility: good.** Every script rerun gives bit-identical output to out/ (light sims fully; T1, T1b, F, H on seeds 0 and 7, max abs diff 0). The RESULTS.md summary statistics recompute correctly from out/ except where noted below.
- **Mathematics: mostly sound, with one sign error and several insufficient hypotheses.**
  - The costate equation (costate.md:122) has the wrong signs.
  - Prop 1's hypotheses do not cover the candidate's own setting: the latent x depends on b, and the user responds to u.
  - The consummatory/anticipatory split and Prop 2's invariance of μ·ḃ fail under Itô for nonlinear φ.
  - Prop 6 conflicts with K2.
  - Props 3 and 4 and the T*/L* algebra are correct, with stated gaps.
- **Two reported interpretations are wrong.**
  1. **T1b C3.** RESULTS says the prediction was mis-derived and that the exact share is 0.889. The exact share is actually 17/18 = 0.944, which passes. The 0.886 failure comes from a one-step offset in the rollout: the same code with a perfect forecast gives 0.889.
  2. **T1b C1 ratio.** The ratio "26.3 (analytic 22)" is an artifact of the max(μ_brb, 0.01) floor. The learned μ_brb is negative (−0.006).
- **F3 call timing.** "20 vs 85 min in all 20 seeds" holds only for S ≥ 180. The call search is not confined to the separation.
- **Verdicts.** No confirmed/refuted label flips at the headline level. However:
  - G2 passes vacuously, and G4 is refuted rather than "not interpretable".
  - F2 is refuted, not "half confirmed".
  - F3 depends on an unregistered choice of S.

## Propositions

**Prop 1 (convexity / satiation). Correct for a narrower setting; the hypotheses as stated are insufficient.**
- Steps 1–5 are the standard partial-minimization argument and are valid if:
  - the controls are adapted processes under full state information;
  - the exogenous path is independent of **both b and u**.
- The min over u needs no separate step, because a mixture of feasible controls bounds V from above. Optimal u¹ and u² need not exist; ε-optimal controls suffice.
- Failures:
  - (a) Step 3, "same exogenous path", needs independence from u. The assumption list (costate.md:225) states only independence from b. In sims G and D, and in the engine, the partner responds to the agent's bids and displays.
  - (b) V is V(b, x), and the policy acts on x. But x_{t+1} = F_θ(x, o, y, **b**, …) (costate.md:53), so the information state depends on b. The mixture θu¹+(1−θ)u² is not implementable by a policy on the mixed trajectory's x. Convexity needs x (and b̂^o) independent of b, or full information.
  - (c) The λ term: convexity needs λd(b̂^o) jointly convex in (b, u). It suffices that b̂^o is independent of b and u, or affine in u. Line 240 states only the b condition.
  - (d) Step 5 assumes V is differentiable. For convex V, μ is a subgradient selection.
- Corollary (line 229) on the bang-bang rule and "never once μ_i ≤ 0":
  - Singular arcs (μ·B = 0) are not excluded.
  - H is affine in u only if ẋ(u) is affine.
  - "Lower set of b_i" does not follow when an action moves several needs: monotonicity gives μ·B_j nonincreasing along B_j, not along e_i. "Never when μ_i ≤ 0" needs the action's other effects to be weakly costly, i.e. μ_e ≥ 0 (true in sim A only because e ≤ e*).
- Line 239 says "T1 uses saturating dynamics". In fact T1 is affine in b (switched affine with exogenous switching), so Prop 1 applies to T1/T1b/F.

**Prop 2 (invariance). Correct for V, v and α as scalar processes, and for the covector law. Wrong for the consummatory term under Itô.**
- V′∘(φ,ψ) = V: correct. μ′ = (Dφ)^{−T}μ: correct.
- With Itô noise and nonlinear φ, db′ = Dφ db + ½∇²φ[Σ_b]dt. So μ′·db′ = μ·db + μᵀDφ^{−1}·½∇²φ[Σ_b]dt, and μ·ḃ is **not** invariant. Step 5 is valid only for deterministic dynamics, affine φ, or a Stratonovich reading.
- For the same reason, the decomposition v = μ·ḃ − ∇_xV·ẋ (costate.md:94) omits the Itô term −½tr(∇²V Σ) (and the b–x cross term) once noise is present. Total v stays invariant; only the split is coordinate-dependent.
- Arousal: the quadratic variation of the scalar V_t is invariant, and Σ′ = DφΣDφᵀ (the Itô correction is drift-only), so μᵀΣμ is invariant. Correct.
- The arousal formula (costate.md:106) **omits the cross term 2μᵀΣ_{bx}∇_xV**. This term is nonzero here because F_θ takes b_t as input, so the latent innovations are correlated with the body noise.
- The A5 test only checks a linear diagonal φ. Re-solving the VI on the scaled grid reproduces V elementwise, so the 1e-13 agreement is close to tautological and does not test the nonlinear case.

**Valence decomposition / HJB (costate.md:94–98). Correct (deterministic); see the Itô gap above.** −dV/dt = μ·ḃ − ∇_xV·ẋ has the right signs. 𝔼[dV] = (ρV − d − λd^o)dt is correct from the HJB, and so is the reading "positive when d exceeds the annuity ρV".

**Costate equation for mood (costate.md:122). Wrong.**
- From the HJB with the envelope theorem: μ̇ = ρμ **+ ∇d − (∂_b f_b)ᵀμ**. The file has −∇d + (∂_b f_b)ᵀμ, with both signs flipped.
- Check on T1, 120 min after "bye":
  - numerical μ̇ = 0.091;
  - correct formula gives 0.105;
  - file's formula gives 1.334.
- The scalar steady state shows it too. Under the file's formula, b < b* gives μ < 0 when ρ > a.
- Also missing are the x-coupling term (∂_b ẋ)ᵀ∇_xV and the λ term. The qualitative claim that mood inherits the body time constants survives only along the closed-loop optimal path, on which μ = μ(b(t)).

**Prop 3 (mimicry shrinkage). Correct.**
- The SVD algebra checks: x* = V(cI+wS²)^{−1}wSUᵀõ and Gx* = U diag(ws²/(c+ws²))Uᵀõ.
- This requires c > 0 for "always partial" and for invertibility when G is rank-deficient.
- Step 3 (line 282) calls the eigenvalues of (cI+wGᵀG)/τ "time constants". They are rates; the time constants are their inverses (the claim line itself is right).
- Gap: the attention rule gives per-channel gains w_i (line 145). With W = diag(w_i), x* = (cI+GᵀWG)^{−1}GᵀWõ, which G's SVD does not diagonalize, so the closed form needs W ∝ I.

**Mimicry gain argument (costate.md:145). Correct with a gap.**
- ∂V/∂õ ≈ −μ_c ∂𝔼[Δb_c]/∂õ, so w ∝ |μ_c|, not μ_c.
- An over-satiated agent (μ_c ≪ 0, the regime sim G actually reached) also mimics more. "A deprived agent mimics more" holds only for μ_c > 0.
- w_i ∝ |∂V/∂o_i|σ_i is a first-order sensitivity heuristic, not a derived value of information. "Derived, not set" is overstated.

**Prop 4 (do-conditioning). Correct, with a gap.**
- With κ̂ = κ, the reader's input L x^o + ε is independent of y given x^o.
- "Marginal value ∝ (κ − κ̂)" holds only to first order. The factor multiplying (κ − κ̂) itself depends on (κ − κ̂)y; sim D's own optimum λk/(η+λk²) is not linear in k.
- It needs ε independent of y and L injective.

**Prop 5 (T*, L*). Algebra correct; the domain conditions are missing.**
- T*: FOC −β e^{−T/T₀}/T₀ + κ_w = 0 gives T₀ln(β/(κ_wT₀)). This needs κ_w > 0. If waiting is neutral or beneficial (κ_w ≤ 0), there is no interior optimum (T* = ∞).
- L*: this needs μ_e c_L > 0.
- Both forms are first-order: μ is held constant over T, and discounting within the reply is ignored.
- The Principle 6 caveat (line 311) says "μ_c ≤ 0 at or above the threshold of Prop 1, bounded by construction". Prop 1 gives monotonicity, not a reachable threshold. In T1, at b ≈ 1 one minute before "bye", the exact μ is +0.109, so μ_c > 0 over the whole reachable range [0, 1]. Boundedness is not by construction.

**Replay priority (costate.md:183). Partly wrong.**
- One SGD step on ½δ² reduces that sample's loss by ≈ ηδ²‖∇_θV‖². So the priority is δ² only if feature-gradient norms are equal, and that would argue for p = δ², not |δ|.
- With β = 1 importance weights, the expected update equals the uniform one, so the claimed benefit is variance only.
- "|δ| = valence surprise" holds only on-policy with exact V.
- It also conflicts with K5: V is a rollout, not TD-trained. Sim H prioritizes the presence-model BCE, so it does not test this rule.

**Prop 6 (dyadic loop). Correct only under extra assumptions, and inconsistent with K2.**
- The small-gain bound ‖MH‖ < 1 holds for any ‖H‖ ≤ 1.
- The per-mode ℓ_i = m_i g_H and the amplification 1/(1−ℓ_i) need the human's mimicry to be diagonal in the agent's U basis.
- It also needs first-order lags, so that the H∞ gain equals the DC gain.
- Under K2, õ ← õ − κ̂y removes the echo before the same õ enters Gᵀ(õ − Gx). The effective loop gain is then m_i(g_H − κ̂_i) ≈ 0, so the predicted S5 amplification contradicts K2 unless K2 is applied only to the b̂^o readout. This needs to be stated.

## Simulations rerun

| Sim | Reproduced | Notes |
|---|---|---|
| A | yes, identical | All A1–A5 values identical to out/a.json. |
| C | yes, identical | All values identical to out/c.json, including the C-M5 score and surrogate percentiles. C-M1 to C-M4 were also checked by hand: 4s²/(4+4s²) and the 3.4 ratio are correct. |
| D | yes, identical | All values within ±0.05 of prediction. |
| E | yes, identical | |
| G | yes, identical | The out/g.json file has a RuntimeWarning line prepended, so it is not valid JSON. |
| analytic_t1 | yes | bye 0.2663, brb 0.0120, ratio 22.21. |
| analytic_t1_belief | yes | Drops at positions 0/30/59 are 0.794/0.721/0.245. No script computes the quoted "65%". The reviewer's mean over all 61 per-minute positions is 0.664; on the env's actual 5-min jitter grid it is 0.714. |
| analytic_f | yes | S = 10 intact prints `L* = nan`: max(nan, 0.0) returns nan at analytic_f.py:28. PREDICTIONS reports 0, which is right in intent. |
| T1 seeds 0, 7 | yes, bit-identical | 20-seed stats recomputed: diff 0.0080 [−0.0024, 0.0173]; ratio 1.27 [0.87, 1.66]; drop 0.64 [0.13, 1.24], 13/20 seeds ≥ 0.4; sat 0.18 [0, 1]; MSE 3.4e-4 [1.9e-4, 4.7e-4]. Matches RESULTS. |
| T1b seeds 0, 7 | yes, bit-identical | diff 0.2685 [0.2669, 0.2701]; ratio 26.26; drop 0.832 [0.738, 0.926], min 0.574; sat 0.886 [0.869, 0.889], 0/20; BCE 0.064. Matches. **μ_brb mean −0.0058 (all 20 negative).** |
| F seeds 0, 7 | yes, bit-identical | Table means, F1 (69.7, 164.3), F2 (183.6, 213.9, 144.2), lesion-B range (9.53 max per seed) and F5 sequence all match. F5 holds per seed in only 2/20. Call times by S: intact 230/20/20/20; lesion A 295/345/85/85. |
| H seeds 0, 7 | yes, bit-identical | All 10 seeds reach ≥ 0.10 on night 2 in both arms. Night-14 values are 0.2667–0.2682. The night-2 values are **identical between arms** (see mismatches). |

## Spec-vs-code mismatches

1. **T1b/F/H rollout offset (sim_t1b_modelbased.py:12–17, 26–32).**
   - F[t, k−1] = present[t+k], so the first transition b_0 → b_1 uses p_{t+1}, not the current presence p_t. The environment (env_t1.py:41) uses p_t.
   - PREDICTIONS:100 is itself ambiguous (p_k for k = 1..72 drives b_{k+1}).
   - **Verdict-changing for C3.** With a perfect forecast, code alignment gives C3 = 0.889 (fail) and correct alignment gives 0.944 (pass).
   - With correct alignment μ_brb = +0.016 and the ratio is 16.5. C1 still passes.
2. **5-min explicit Euler in the rollout (K_P·Δ = 0.5).**
   - The analytic references use exact 1-min dynamics.
   - With true presence, the rollout's μ at a long-absence arrival is 0.021, against the exact 0.106. The horizon is not the cause: the exact value with a 6-h horizon is also 0.106.
   - So the F "analytic L*" column (0/156/194/198) is not what the implemented V gives even with a perfect forecast. The perfect-forecast values under the implemented V are 0/24/112.5/118.5.
   - Under that reference F1 and F2 would pass, so the F failures are attributable to the learned forecast. That supports RESULTS' reading.
   - But the "144 ≥ 40" margin at S = 1240 and the 85 vs 65 min lesion-A call are inflated by discretization.
3. **F call search (sim_f_s1_lesion.py:61–64)** runs 300 steps past "bye" without stopping at the reunion.
   - For S = 10 (both arms) and S = 60 (lesion A), the recorded "call" follows the *second* "bye", at 200 min plus the latency.
   - PREDICTIONS:167 does not say which S is used for F3. RESULTS:137 silently uses S ≥ 180.
   - Averaged over all S, intact = 72.5 min > 40, so F3 would fail. **Could change the F3 verdict.**
4. **F lesion B (sim_f_s1_lesion.py:66–68)** averages over day 3, which contains the manipulated separation. This matches PREDICTIONS:150's wording ("the test day"), so it is a spec defect more than a code defect. F4 fails either way.
5. **G world-model supply (PREDICTIONS:185; sim_g_stillface.py:10).** Predicted supply is q̂·0.8/s·0.01, but the actual contact opportunities are about 0.3/s plus bids. The model over-predicts supply by roughly 2.7× and the predicted equilibrium is about 0.95. Not verdict-changing: the actual play equilibrium is 0.0024(1−b) = b/3600, giving b ≈ 0.90 > b*, so over-satiation is real regardless.
6. **G responses** are decided at emission time (sim_g:28), so a response can land up to 1 s into the still-face. Negligible.
7. **A action set** is discrete {0, .25, …, 1} (sim_a:6), while Prop 1 and PREDICTIONS:36 say convex. The spec contradicts itself (line 41), and the code follows the grid. A therefore does not test Prop 1 under its own hypotheses, though it passes anyway.
8. **E1 bored condition (sim_e:17)** uses ε_N after the step's update, not at decision time. Not verdict-changing (100%).
9. **H night 2** has exactly one candidate window (sim_h:28: arange(0, 1, 6) = [0]), so the arms are identical on the night the criterion is met. H1 could not have been confirmed. This is consistent with RESULTS' "uninformative" but was not stated.
10. **T1 deficit ablations** (C1/C2 "exactly 0", PREDICTIONS:27–28) are asserted, not computed. Trivially true.

## Errors in RESULTS.md or costate.md

1. RESULTS.md:72–82 and costate.md:331: "C3 refuted because the prediction was mis-derived; exact share 0.889; learned matches."
   - **Wrong.** The exact μ at the 5-min second-half steps exceeds 0.02 only at bye−5 (+0.044); bye−10 is −0.002. That is 1/18, so the exact share is 0.944 ≥ 0.90.
   - The table values in RESULTS:76–80 are correct; the count "2 of 18" is not.
   - The failure is the rollout offset (mismatch 1).
2. RESULTS.md:67 and costate.md:331: "ratio 26 (analytic 22)". The value is μ_bye/0.01 floor, because μ_brb < 0 in all seeds (true learned ratio < 0). The pre-registered metric passes, but the comparison to the analytic 22 is spurious.
3. RESULTS.md:137 and costate.md:336, 353: call times "20 vs 85 min in all 20 seeds". This holds only for S ∈ {180, 1240}; see mismatch 3.
4. RESULTS.md:134: "F2 half confirmed". F2 is a conjunction (PREDICTIONS:166) and the intact ≤ 20 clause fails (213.9), so F2 is refuted.
5. RESULTS.md:107–110 (G):
   - G2's threshold (last30 ≤ 0.5 × first30) is satisfied vacuously (0 ≤ 0), so "fails" misstates it.
   - G3 fails on its smile clause (0.016/0.044 = 37% < 50%), not for the reason given. The distress clause passes vacuously.
   - G4 is refuted, not "not interpretable": the lesion smile rises from 0.0036 to 0.0079, failing its "smile falls ≥ 50%" clause.
   - The overall "refuted" stands.
6. RESULTS.md:84 and 141: C2 0.83 vs 0.65, and F μ "against analytic −0.03 to 0.10". These attribute the gaps to the predictor or to out-of-distribution data, without noting the Euler bias (mismatch 2). The 65% is the per-minute belief average; the 5-min-grid value is 0.71.
7. costate.md:239: "T1 uses saturating dynamics". T1 is affine in b; Prop 1 applies.
8. costate.md:122: costate equation sign error (see Propositions).
9. costate.md:350: "falls by 65% (analytic expectation)". No script produces it; it reproduces as 0.664 only with per-minute positions.

## Recommended fixes

1. Fix costate.md:122 to μ̇ = ρμ + ∇d − (∂_b f_b)ᵀμ (plus the x-coupling term), and restate the mood claim along the closed-loop path.
2. Prop 1:
   - Add the assumptions that the exogenous process is independent of u, and that x and b̂^o are independent of b (or full information).
   - Weaken the bang-bang corollary: allow singular arcs and multi-need actions.
   - Delete "T1 uses saturating dynamics".
3. Prop 2 and the valence/arousal formulas:
   - Restrict μ·ḃ invariance to deterministic or affine φ (or use Stratonovich).
   - Add the Itô term to the valence split and the Σ_bx cross term to α².
4. Prop 6: reconcile with K2, by stating whether the echo is removed before the mimicry path. Add the mode-alignment assumption.
5. Prop 5: add κ_w > 0 and μ_e c_L > 0. Drop "bounded by construction", or require μ_c ≤ 0 to be reachable.
6. Mimicry: write w ∝ |μ_c| and note the over-satiated case. Note the SVD form needs W ∝ I.
7. Replay: reconcile with K5, and correct the |δ| vs δ² claim.
8. RESULTS.md:
   - Correct the C3 explanation and the ratio remark.
   - Relabel F2 (refuted) and G2/G3/G4 per the thresholds.
   - State the S used for F3.
   - Add the perfect-forecast reference for F (0/24/112.5/118.5).
   - Keep the original verdicts, since T1b C3 stays refuted as run.
9. Code, as post-hoc exploratory runs:
   - Align the rollout to use p_t for the first transition.
   - Use exact exponential integration per step.
   - Confine the F call search to [bye, arrival).
   - Write stdout only to out/g.json.
   - Fix max(nan, 0) in analytic_f.py:28.
