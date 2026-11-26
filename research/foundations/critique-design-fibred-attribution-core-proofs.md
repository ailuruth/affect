# Critique: Fibred attribution core, proofs and the dial (design-fibred-attribution-core.md)

Independent critic, 2026-11-26T04:32:57Z. Written under questions.md Q16 and Q17 and judged against the refined rule (Q18 answer, DECISIONS.md D78) and the constraints C1–C10 of non-copying-dynamics-synthesis.md. I did not write the design and did not see its author's reasoning. Scope: the proofs and the dial. Nothing was downloaded. No data, no weights.

Numerical checks are in `research/foundations/sims/critique-fibred-proofs/` (`base_noise.py`, `filter_leak.py`, `held_level.py`, `lemmas_misc.py`; outputs in `out.txt`). They check the design's own equations on hand-built, admissible parameter values. They are **not** evidence about behaviour, people or data (brief.md, no toy worlds). Each counterexample below uses only constants from the design's §2.1 and parameter values inside its admissible set Θ.

## Summary verdict

- **Proofs: 34 items checked. 12 valid, 11 with a gap, 11 with an error.**
  - Valid: the algebra of Lemma 1, Lemma 3 (without noise), Lemma 5, Lemma 6(1)–(3) and (5), the bucket count, Theorem 1(a), (b) and (d) as literally stated, and the arithmetic of the Theorem 3 and 4 tables, which I reproduced to three digits.
  - The errors are in what the proved statements are said to mean, and in routes the inventory leaves out.
- **Worst error: the base does not persist under the design's own noise, and its noise-driven switching is a partner-influenced route the token budget does not count.**
  - The Kramers estimate in §3.3 drops the relaxation rate ε_b. The exponent is 2ε_bΔV/σ_b² = 1.53, not 7.65.
  - Simulated with the design's constants and its worst admissible placement (neighbouring centres at d_min, the same placement its own estimate uses), a well is held for about **37 s on average**, not 6–19 h. The state is never within r = 0.1 of a centre. Its mean distance from the nearest centre is 0.69, which exceeds the 0.25 half-separation.
  - The body tilt t_ψ(ζ̃) is reached by the partner through motor effort and is never charged a token. At its innate maximum (0.05) it shifts occupancy between the two end wells by a factor of **136** (K1).
  - So Theorem 1(c), Theorem 6(b) ("partner-caused switches ≤ bucket") and Theorem 8 ("mood, hours") fail with σ_b = 0.09. They hold only at σ_b = 0, where the base has no spontaneous dynamics at all.
  - This confirms the novelty critic's lead (1). The effect is larger than the ~22× in that lead, because the tilt selects the well, not only the switching rate.
- **Three further errors on central claims.**
  1. **Theorem 2's identity Γ(σ·p) = Γ(p) fails for any causal filter bank.** A causal F_f is not idempotent, so flipping the partner's physical 3 Hz motion changes u^m by 0.17–0.24 of its amplitude (K2). A router-only agent then has 3-Hz coherence of 0.13–0.21 with the partner, against a 0.01–0.02 surrogate. That is positive linear coupling inside C1's 2.6–6.5 Hz band, which the theorem says no parameter can produce.
  2. **Lemma 7 is not complete.**
     - N_own takes own-speech prosody (from Claude's text) and, for the startle reflex, an audio onset. Neither input is capped.
     - Voice channels have no role cap.
     - Visemes sit outside every bound.
     - So the Claude route reaches the face and voice uncapped. Theorem 3 also fixes "every Claude output" in its counterfactual, which removes the retrieval route by definition.
  3. **A single quantity can run the whole face toward a copy of the partner's held expression on the mood time scale, inside the budget (K3).** Event proposals are REN outputs that see both the partner's levels ℓ and the agent's displayed base b̃. They can therefore fire "up" or "down" on any partner movement whenever ℓ differs from the displayed level. The result is a quantised feedback tracker, spending 130 of 362 allowed tokens over 6 h.
     - On 1-min means, the agent's whole 16-channel face matches the partner's held face with uncentred correlation **0.93** (defect **0.38**) and pooled gain **0.36**, at a 7-min lag.
     - That gain exceeds the design's whole-face figure (0.27), and the defect is below its whole-face floor (0.49).
     - The own-variation floor of Theorem 4 does not exist at these time scales, because d has no power below 0.05 Hz.
- **Dial verdict (D78): not met as proved.**
  - The router, the REN ceilings and the role term meet D78 per channel, with innate caps that are applied after learning. That is a real advance on earlier designs.
  - Three things still fail D78:
    1. The base position (one shared learned direction, through H on every channel) can run the whole face's slow level from flat to a near-copy (K3).
    2. A shared estimate (ŝ, or 𝓜's partner prediction) drives text selection and retrieval, and through N_own's uncapped speech input it reaches the speaking face and voice. This route is neither named nor bounded (K9: best-of-4 selection gives a correlation of 0.78 with the partner's valence).
    3. "Copy never attracting" is shown only as an empty-set statement about copies better than the floor. The routing-learning loop itself (Theorem 5(c)) needs a linear echo inside the dither band. If the partner echoes outside 0.05–1 Hz, the instrument sees nothing, and with g_p = 4 learning runs to the row cap, where both caps are attracting (K8).
- **Expressivity (item 4).**
  - The fast match at 0.35–0.65 s fits the human data.
  - Context from the partner or from words can move at most about 10% of the routing mass (c_ω = 0.2), so it cannot flip the sign of matching within 2–4 s. Sign flips need a base event (sustained ≤ 1/min) or a role change.
  - Nothing about the partner is learned within a session except through those events.
  - The agent's own state reaches its face slowly and weakly: at most about 0.6 of a typical expression, at most about 10⁻³ per second. The common-cause (content) route is capped near 0.07, against 0.3 for partner matching. That is the reverse of C8, and it inverts the brief's "expressions come from an internal state".

## Sources read for this critique

| Source | How read |
|---|---|
| research/foundations/design-fibred-attribution-core.md | in full, 1145 lines |
| research/foundations/sims/design-f/checks.py and out.txt | in full; reran nothing, reproduced F10/F11 numbers independently in K7 |
| brief.md; questions.md Q16, Q17, Q18 with answer; DECISIONS.md D78 | in full |
| research/foundations/known-failures.md; research/non-copying-dynamics-synthesis.md | in full |
| research/foundations/critique-design-modulated-manifolds.md | summary and §1 opening, for format |
| Revay, Wang & Manchester 2023; Lanillos et al. 2020; Forssell & Ljung 1999 | **not re-read.** I take the design's citations of Revay Theorem 3 and of the IV identity at face value. Nothing below depends on them except where I say "as cited" |

---

## 1. Item-by-item check

### §3.0 Definitions
1. **The copy-defect identity δ = (1 − ρ²)^{1/2}: valid.** The minimisation in x = 1/c is correct.
2. **The neutral counterfactual: gap.**
   - It says to "fix … every Claude output", and then says content pulses "differ between g and g⁰ when selection differs". These cannot both hold. Read literally, fixing Claude's drafts removes the route partner → ŝ/𝓜 → retrieval → Claude's context → drafts from Δy by definition.
   - It also keeps partner voice activity unchanged in g⁰. That puts the voice-activity route into the "own part" o_K of Theorem 4 (item 27).

### Lemma 1 (contraction forbids multistability)
3. **Valid.** Uniqueness follows from the contraction inequality; existence follows from Banach's theorem in the certificate metric.

### Lemma 2 (no free persistence)
4. **(a) Gain port: gap (minor).**
   - The barrier argument at b*_i is correct in one dimension.
   - The "returns to m_i" clause assumes b never crosses M_{i−1} downward. With |s| ≤ S two-sided, that needs the mirror condition kS < max_{[M_{i−1}, m_i]}(−V′), which is not stated.
5. **(b) Derivative port: gap.**
   - During the slow rise b does not sit at m_i. It sits at the quasi-equilibrium where V′(b) = 2kΦ/T_r, above m_i. The fall starts from there.
   - The landing condition should read h_D + (b_eq − m_i) < 2kΦ < D + h_D + (b_eq − m_i). It reduces to the stated one only as T_r → ∞. F5 passes because its T_r is long.
6. **(c) Bucket count ≤ B + ρT: valid.** It holds by construction.
7. **"The budget is the only innate stop", and so the fibred, budgeted shape is forced: error.**
   - Lemma 2(a)'s own second clause is a different innate stop: a gain port with kS < min F^+.
   - The design itself uses one: the body tilt, capped at t_max.
   - With noise (σ_b > 0), a capped gain port changes switching rates continuously, with no budget (K1).
   - A non-contracting fence, such as a finite-horizon incremental-gain bound, is not excluded by Lemma 1 either.
   - What Lemma 2 actually shows: some innate cap on the partner's switching rate is needed. It says nothing about the *content* of the switches (which well, what weight). That content is where K3 leaks.

### Lemma 3 (C persistent states for every parameter and tilt)
8. **Deterministic statement: valid.**
   - η, e_max, the inward-pointing condition on the sphere and the Hessian bound I − β Cov_p ⪰ (1 − 4β(C − 1)η)I all check.
   - The exponent identity (d_min − r)² − r² = d_min(d_min − 2r) is correct, and η = e^{−14}.
   - For a time-varying tilt, "equilibrium" should read "tracked minimiser". Forward invariance still holds.
9. **The noise paragraph: error.**
   - For db = −ε_b∇V dt + σ_b dW the invariant density is ∝ exp(−2ε_bV/σ_b²). The exponent is 2·0.2·0.031/0.0081 = **1.53**, not 7.65.
   - At a barrier of about 1.5 kT, Kramers' formula does not apply.
   - Simulation (K1, 400 runs of 1 h each, worst admissible placement): mean residence **37 s**; time spent within r = 0.1 of a centre is **0**; mean distance from the nearest centre is **0.69**. The 23 directions orthogonal to the neighbouring centres are each an OU process with variance σ²/2ε = 0.020.
   - The design flags this estimate as unproved. But Theorem 8 ("Mood, hours … Kramers 6–19 h") rests on it.

### Theorem 1 (fibred persistence)
10. **(a): valid as stated (for a fixed own-input path). Its "consequence" is an error.**
    - The consequence says the partner's influence "through every continuous route" decays within 3.3 s. But the REN drives m^pre, then ζ (time constant 10 min), then ζ̃, which feeds back into the REN.
    - The habituation A (2 min), the baselines p̄ and σ̄ (60 s), 𝓜's state and λ are all continuous and partner-dependent, and they outlast 3.3 s.
    - Theorem 8's "structural statement (proved)" is false for the same reason.
11. **(b): valid at σ_b = 0.** It is vacuous at the design's σ_b (item 9).
12. **(c): valid at σ_b = 0. Error at σ_b = 0.09.**
    - The tilt is partner-influenced through ζ̃ and uncounted. It biases spontaneous switches: occupancy of the end wells shifts by ×136 at |t| = t_max (K1).
    - So "the only partner-dependent terms that can move b out of a ball are event jumps" is false for the design as specified.
13. **(d): valid.**

### Lemma 4 and Lemma 5
14. **Lemma 4: the statement is valid; the meaning is an error.**
    - The diagonal case is a one-line fact.
    - The design's summary concludes "No quadratic (IQC-type) ceiling can express this". That does not follow. RENs admit a general Q ≺ 0.
    - Counterexample K4: Q = −(I + α11ᵀ)/c², R = I, α = 10, K = 32. The single-channel copy gain is ≤ 0.045 and the whole-face g·I is ≤ 0.0084, a ratio of 5.4.
    - A non-diagonal quadratic budget does separate one-channel matching from whole-face matching. The ℓ₁ router is a choice, not a necessity, and novelty result 2 should be restricted to diagonal multipliers. This confirms the coordinator's lead.
15. **Lemma 5: valid.** The construction attains the bound.

### Lemma 6 (router)
16. **(1)–(3): valid.**
17. **(4): gap.**
    - The radial projection onto an ℓ₁ ball is 2-Lipschitz in ℓ₁, not 1 (K5: ratio 1.9998).
    - The Schur test's column sum τ assumes that, for a fixed source sample, all output channels read it at the same time. With per-channel lags ℓ_{a,k} and weights that change from frame to frame, the column sum can reach Σ_k W_k. K6 gives an incremental gain of 1.17 against the claimed 0.42.
    - The claim "for every logit path" is therefore false. It holds for logits that change slowly compared with the lag spread, which the τ_ω low-pass and the slews make plausible but nothing proves.
    - The fix is a stated rate bound on the logits, or a factor √(number of distinct lags). Theorem 5(b)'s Γ_A inherits this.
18. **(5): valid.** The bound ‖ΔA‖ ≤ T_s/(√2 T_R)‖Δμ‖ is even slightly better than the one used.

### Theorem 2 (sign-blindness) and Corollary 2a
19. **Theorem 2: error.**
    - The proof uses Γ(σ·p) = Γ(p), with σ acting as c^f ↦ σc^f and r held fixed. The system computes c^f = F_f p from the percept, and F_f(r + σc^f) = σc^f requires F_f² = F_f.
    - Complementary *causal* filters are not idempotent. In K2, ‖F_f(r − c^f) + c^f‖/‖c^f‖ = 1.14 (first order) and 0.92 (second order); it would be 0 if F_f were idempotent.
    - A physical sign flip of a 3 Hz head motion changes u^m by 0.24 (first order) or 0.17 (second order) of its amplitude, and ε by about 33%.
    - What is proved is invariance in the coordinates (r, c^f). That is not invariance to the sign of the partner's motion above 2 Hz, and it is the latter that C1 measures.
    - A further gap: the floor rule's partner voice activity and the ASR word timestamps are computed from raw audio, outside Γ. The theorem conditions on words, but not on voice activity.
20. **Corollary 2a: gap.** It is correct for the filter output c^f in open loop. The C1 "G" row in §3.17 uses it for the physical band, where K2 shows a coherence of 0.13–0.21 against a surrogate of 0.01–0.02 for a router-only parameter.

### Lemma 7 (route completeness)
21. **Error. The following edges exist in §2 and are not in the table:**
    - **N_own ← own-speech prosody features and the utterance text** (§2.10). Its Lipschitz bound is stated only in (b̃, ζ̃). The text depends on retrieval keyed by ŝ, on 𝓜's selection keys and on the scorer. This route is uncapped on face and voice.
    - **N_own ← loud audio onset** (the startle reflex, §5.2). This is a partner-audio input that never passes Γ.
    - **The role term on voice channels.** O_k caps face channels only, and speaking versus listening changes the voice completely.
    - **Visemes from own phonemes.** They lie outside the 16 coordinates but on the rendered mouth, with no bound.
    - **σ_d(t)**, through A (listed under R8, but then cancelled wrongly; item 22).

### Theorem 3 (all routes)
22. **(3a) on face channels: gap. The arithmetic is reproduced exactly (K7).**
    - "d is identical in both runs" is false. σ_d depends on A, which depends on the partner, so Δd = Δσ_d·ξ, with RMS up to σ₀. This adds σ₀ to RMS(Δy); asymptotically it adds nothing to the gain.
    - y^R(g⁰) ≠ 0 during the first ℓ₂ ≈ 2.5 s, because the taps reach back before t₀.
    - ε_j = LP|c^f_j|/σ₀^p is neither saturated nor scaled by the partner, and σ₀^p is never given. So ā_g, and with it χ_k, has no bound for an energetic partner.
23. **(3a) on voice channels, and on the face through N_own's speech input: error.** There is no bound at all (item 21).
24. **(3d), the claim ϖ_K ∈ [1/|K|, 1]: gap.** M_k takes the maximum over all 16 partner coordinates of the band, not over K. With active coordinates outside K, ϖ_K > 1. The pooled value of 0.47 survives only through the row cap (min(W_max, τϖ)).
25. **The headline numbers: gap.** The summary quotes single-channel 0.59 at 30 s next to 4-channel 0.47 and whole-face 0.27 at 10 s. At 30 s my recomputed values are:

    | T | single (W = 0.30) | 4-ch worst | whole worst | whole frozen |
    |---|---|---|---|---|
    | 10 s | 0.549 | 0.474 | 0.267 | 0.144 |
    | 30 s | 0.587 | **0.512** | **0.305** | 0.182 |
    | 60 s | 0.644 | 0.569 | 0.362 | 0.239 |
    | 5 min | 1.10 | 1.03 | 0.82 | 0.70 |
    | 10 min | 1.67 | 1.60 | 1.39 | 1.27 |

    Beyond about 3 min every bound exceeds 0.8 and is uninformative. That is the time scale of the base route (item 26).
26. **"No single quantity runs the whole face or a large subspace from flat to copy": error.** See counterexample K3 (§2) for the base and K9 for the draft or retrieval route.

### Theorem 4 (defect floor)
27. **The proof: gap.**
    - o_K := y(g⁰) − d_K is not independent of u_K. g⁰ keeps the partner's voice activity, and with it r and N_own's role term. o_K also contains state set by the partner before t₀.
    - d is not "independent of everything else": A6 lets it feed the IV estimator, then a_t, then b, then b̃, and so A and σ_d.
    - "Observable" refers to the internal channel outputs y_(j,β), not to the rendered face m_j = Σ_β F_β y_(j,β).
    - Each of these is repairable by adding O_k to C_K and by a mixing argument.
28. **The meaning ("the observed face is never better than a δ_K-defective copy, whatever the weights"): error.**
    - d is band-limited to 0.05–1 Hz. Copy measured on any time scale where d has no power (1-min means; the 1–2 Hz part of the mid band) has no floor.
    - In K3 the whole-face defect on 1-min means is 0.38 at gain 0.36. Both values lie past the design's whole-face figures (floor 0.49, gain 0.27).

### Theorem 5 (copy not attracting)
29. **(a): error as framed.**
    - It uses Theorem 4, which assumes open loop, so it does carry an assumption about the partner.
    - It shows only that copies better than the floor are unreachable. It does not show that the agent does not settle at the most-matched admissible state, which is what D78 forbids ("never let copying become a state the agent settles into").
    - The claim that it needs "no correct-model assumption" belongs to this tautological part only.
30. **(b): gap.**
    - It inherits item 17: Γ_A is 0.42 + … only for slowly varying logits.
    - g_p is defined in mixed units: the partner gate is normalised by the partner's own σ̄, and the agent's units by its expressive scale. A partner who returns a typical-size expression to a 0.3-unit agent expression has g_p ≈ 3 > 1.56.
31. **(c): valid as a conditional statement; the condition fails under misspecification.**
    - The IV (Lemma 8) identifies the echo only where d has power. An echo of the agent's 1–2 Hz or below-0.05 Hz component gives Ĝ = 0, and then a = 0.
    - With λ_e = 0.3 and g_p = 4, learning runs to ω = W = 0.30. With s* = 0, both caps ±W are attracting and 0 is unstable (K8). The row cap is the attracting state.
32. **(d): valid.** The design's own admission that habituation does not bound concentration is correct (1.58 > 1).

### Theorems 6, 8 and 9 (as they bear on the dial)
33. **Theorem 6(a): error in coverage.**
    - It is proved for a partner whose whole percept is frozen. Lemma 7 cites it for "held levels" in general.
    - With a held level on one coordinate and ordinary movement on the others, the event port re-arms at every transient. The REN can then encode the held level in which event fires (K3).
    - Separately, "after which b is autonomous" is false with noise: the fibre's sustained response to ℓ reaches the tilt through ζ (item 12).
    - **(b)** is valid at σ_b = 0.
34. **Theorem 9(b), and the unspecified c_s: gap.** This confirms the coordinator's lead (2).
    - ŝ = D(ℓ) is a REN output, so its sensitivity to ℓ is ≤ c_s/√m_g, and c_s is never given. Nor are c_κ, c_ev, q_max, D_R^max or σ₀^p.
    - The own expression map E_own = (H, N_own) has Lipschitz constant ≤ A_k + L_own ≈ 0.3, so an exact left inverse needs Lip(D) ≥ about 3.3. That requires c_s ≥ 3.3·√80 ≈ 30, which contradicts the small ceilings the certificate relies on.
    - A further gap: the partner's levels live in [−1, 1], but the agent's own displayed repertoire spans only about ±0.3. Most human expressions therefore lie outside E_own(S_own), and ŝ is read through the projection Π almost always.
    - "ŝ = s exactly" holds only if c_s is large and the partner is as unexpressive as the agent.

**Tally (34 items):** valid 12 (items 1, 3, 6, 8, 10 as stated, 11, 13, 15, 16, 18, 31 as a conditional, 32); gap 11 (2, 4, 5, 17, 20, 22, 24, 25, 27, 30, 34); error 11 (7, 9, 12, 14, 19, 21, 23, 26, 28, 29, 33). Item 10's consequence and item 11 at the design's noise level are covered by the errors in items 9 and 12.

---

## 2. Counterexamples

Each uses design constants and parameters in Θ.

**K1. The base does not persist, and the partner tilts it without tokens** (`base_noise.py`).
- Setup: five centres on a line at separation d_min, β_b = 200, ε_b = 0.2, σ_b = 0.09, 24 dimensions, 400 parallel runs of 1 h each.
- With no tilt: 96 switches per hour (mean residence 37 s). The state is never within 0.1 of a centre; its mean distance is 0.69.
- With the tilt at +0.05 (t_max), which ζ̃ supplies and which the partner reaches through motor effort: occupancy of the five wells is 0.005 / 0.015 / 0.054 / 0.193 / 0.732.
- Neither is charged to any bucket.
- Caveat: with wider learned spacing the barriers grow quadratically, and persistence can recover. The design's own estimate assumed d_min spacing, and Θ allows it.

**K2. The fast band leaks its sign** (`filter_leak.py`).
- Setup: a partner signal made of slow motion plus an amplitude-modulated 3 Hz component. Flipping the 3 Hz component changes u^m (and so the router input) by 0.24 / 0.17 of its amplitude, for first- and second-order banks.
- A router slot at W = 0.2 and lag 0.5 s, plus own variation, gives 3-Hz coherence 0.21 / 0.13 against a partner-swap surrogate of 0.02 / 0.01.
- In the twisted band the agent has no own variation (d stops at 1 Hz), so nothing dilutes this leak.

**K3. The token budget plus the slow display copies the partner's held whole face** (`held_level.py`).
- Setup:
  - The partner holds a whole-face expression L_k = P_k·ℓ, with ℓ ∈ {−1, −0.5, 0, 0.5, 1}, and makes ordinary movement transients about every 15 s.
  - The learned event proposal is "up" if ℓ > level(b̃) + 0.25 and "down" if ℓ < level(b̃) − 0.25, gated by any transient. Both ℓ and b̃ are REN inputs.
  - Jump ±0.5 (within j_max = 0.6); the design's bucket, refractory period, wells, slew v_b and H with A_k = 0.25.
- Results over 6 h:

  | Mean hold | Tokens used (of 362) | 1-min corr | Defect | Pooled whole-face gain | Lag |
  |---|---|---|---|---|---|
  | 8 min | 226 | 0.83 | 0.55 | 0.29 | 6 min |
  | 20 min | 130 | **0.93** | **0.38** | **0.36** | 7 min |
  | (no tracking) | 0 | 0.00 | 1.00 | 0.00 | – |

- One quantity, the base position along one learned axis, moves all 16 channels together.
- The design classes this as C9 ("converge in parameters"). It is convergence of the *output*. Gain is capped only by A_k (innate), and the scale-free defect is not floored at these time scales.
- The design's whole-face bound at T = 10 min is 1.39, so it says nothing here.

**K4. A quadratic budget that separates** (`lemmas_misc.py`). This is item 14: ratio 5.4 between single-channel and whole-face admissible copy gains.

**K5 and K6. The router incremental constant** (`lemmas_misc.py`). This is item 17: a projection ratio of 2.0, and a switched-weight incremental gain of 1.17 against the claimed 0.42.

**K7. The totals** (`lemmas_misc.py`). This is the table in item 25.

**K8. Learning makes the cap attracting under misspecification** (`lemmas_misc.py`).
- Setup: the echo lies outside the dither band, so Ĝ = 0 and a = 0.
- With g_p = 2 the loop gain is 0.6 and there is a unique small fixed point (0.037).
- With g_p = 4 the loop gain is 1.2. From either sign, ω reaches +0.30, the row cap. With s* = 0, both caps attract.

**K9. The conceptual route** (`lemmas_misc.py`).
- A best-of-4 draft choice by closeness to ŝ correlates 0.78 with the partner's valence.
- Through N_own's uncapped speech input, the selected text sets the speaking face and voice. The same holds for ŝ-keyed retrieval, which changes all four drafts.
- The bits per reply are few, but the amplitude is not bounded. It acts on every speaking channel at once: a shared learned estimate moving many channels together, the failure the earlier critiques found.

**Tested and not found.** These leads from earlier critiques do not reproduce here:
- **Event rate as a dial.** It is capped at 1 per minute, which is genuine.
- **The router's mass concentrated so that a 4-channel subspace sits at its ceiling.** The mass τ = 0.6 limits a 4-channel frozen allocation to 0.15 each. With the REN and role terms the subspace reaches 0.32 (frozen) or 0.47–0.51 (attention-chasing, 10–30 s). The ceiling is innate.
  - Read by gain, that is not "flat to copy".
  - Read scale-free, the defect at the 4-channel worst case is ≥ 0.30 in the 0.05–1 Hz band, so not a copy there either.
  - It does count as copy outside that band (item 28).
- **The held-level leak through the router.** u is high-passed at 60 s, which removes it.

---

## 3. D78, quantity by quantity

| Quantity | Per expression | Set by context and relationship | Sign | Innate cap, not learned | Copy non-attracting under own learning |
|---|---|---|---|---|---|
| Router slot weights ω_kja | yes | own context yes. Partner or word context ≤ ~10% of mass (c_ω = 0.2) | yes (± slots) | yes: W_k and τ, applied after the logits | **no, not proved**. Thm 5(c) needs a linear, in-band echo; K8 |
| REN sensitivity on k (θ) | yes | yes | yes | yes: c_k compiled in. But ε is unsaturated and σ₀^p is unspecified, so the effective gain is open | joint with the router learning; not separately shown |
| Base display H_k, J, ψ | per channel in H. But **one base direction moves all channels** | yes | yes | A_k and v_b yes. The partner-write count fails under noise (K1) | **no**: K3 is a whole-face slow near-copy reachable in Θ |
| Role term | yes. One r moves all face channels (≤ 0.08 each) | yes | yes | face yes (O_k); **voice no** | not addressed; small |
| N_own speech/text dependency | **not named** | – | – | **no cap** | **not addressed** (K9) |
| ŝ, 𝓜 keys, draft scorer | shared across channels | – | – | **none downstream** | **not addressed** |
| Twisted outputs | yes | yes | sign-blind only in (r, c^f) coordinates | c = 1.0 | leak copy (K2) |
| Own variation σ_d | – | – | – | floor σ₀ | – |

The design passes D78 on the fast, continuous, per-channel part (router and fibre). That part is the best-bounded of any design in this project. It fails on the slow shared parts (the base, through events and through noise and tilt) and on the conceptual route (N_own's speech input), and its non-attraction claim is not proved.

---

## 4. Expressivity against the human data

| Human requirement | Design | Verdict |
|---|---|---|
| Fast match at ~0.5 s (Golland 0.48 s; Hale 0.59 s) | router tap ℓ₁ = 0.35–0.65 s | compatible |
| Context changes or flips the response within 2–4 s (Golland 1.75 s when context and smile disagree; C2, C4) | partner- or word-driven key changes move the allocation by ‖Δμ‖ ≤ ~0.1, too little to flip a sign. Flips need a base event (≤ 1/min sustained, burst of 2) followed by a steep N_q in b̃, or a role change | **only at about 1 per minute**; human context effects act per expression, every few seconds |
| Sign flips by role (C4) | the role enters the queries directly | compatible |
| Partner history learned within minutes (Golland's second clip; C7, C9) | weights change only nightly (A8). Within a session only base events, habituation (2 min, which fits C7) and baselines adapt. κ_rel is frozen after 5 s | partial. C7 yes; within-session partner-specific coupling no |
| Common cause dominates face coupling (C8: about two-thirds common, one-third partner-specific) | content pulses reach the face with ≤ c·‖e‖/√80 ≈ 0.07 on one channel. The router gives 0.3 | **reversed** |
| Own appraisal shows on the face within seconds (brief: expressions come from internal state) | own state reaches the face through H (range ≤ 2A_k tanh 1 ≈ 0.38, slew 4·10⁻⁴/s), N_own (L_own = 0.05) and the REN (κ_b·c = 0.075). A full change takes ≥ 20 min. While listening, the largest structured component of the face is partner-driven | **incompatible**. The fast and large part of the face budget belongs to matching |
| Mood shifts over minutes | a slew-limited display moves 0.1 in about 4 min, but the base under σ_b wanders every ~40 s (K1) | the display is slow while the base underneath is noise-driven. Neither matches |

---

## 5. Fixes

1. **Base noise.** Rescale σ_b so that 2ε_bΔV/σ_b² ≥ 15 at d_min spacing (σ_b ≤ 0.029), or prove persistence with an explicit Freidlin–Wentzell bound. Then charge noise-driven switches to a budget, or cap the tilt's effect on escape rates and include it in Theorem 1(c) and Theorem 6(b).
2. **Theorem 2.** Define the gate on a filter-independent decomposition: either a non-causal idempotent split applied with a fixed delay, or a narrower claim ("invariant to the sign of F_f p"). Report the leakage of the 2–3 Hz transition band, and move 𝒯's lower edge to where |1 − F_f| is negligible (e.g. 4 Hz) if C1's 2.6 Hz edge matters.
3. **Lemma 7 and Theorem 3.**
   - Cap N_own in its speech-prosody and text inputs per channel, and cap the role term on voice.
   - Bound visemes, or exclude their blendshapes from the copy metric explicitly.
   - Add the startle input to the table with its cap.
   - Remove "fix every Claude output" from the counterfactual and bound the retrieval and selection route through N_own.
4. **Event content.** Make event *type and weight* independent of partner levels ℓ (the proposals see only u and ε, never ℓ or b̃ jointly), or budget the information per event. Otherwise the bucket bounds the rate and not what the events say (K3).
5. **Defect floor.** Extend d below 0.05 Hz (a slow own random walk in b, ideally the base noise itself once it is rescaled) and above 1 Hz. Or state Theorem 4 as a band-limited result and give a separate slow-time-scale bound.
6. **Theorem 5.** Drop the "no correct-model assumption" headline, or prove non-attraction of the cap state directly: for example, make the routing target saturate in ω, or put an innate stop on learning near the cap.
7. **Constants.** Specify c_s, c_κ, c_ev, q_max, D_R^max and σ₀^p. Check Theorem 9(b) against c_s, and either rescale E_own or state that ŝ is a projection reading.
8. **Lemma 4 and novelty.** Restrict the claim to diagonal multipliers, and compare the router with a non-diagonal quadratic budget (K4) on the expressivity it allows.
9. **Lemma 6(4).** Either add a stated bound on how fast the logits may change, or carry the extra factor of √(number of distinct lags) into Γ_A.
10. **Expressivity.** Give own-state expression a fast, capped route that does not pass the 20-min display: for example, own content events into a separate fast own channel with its own cap. And rebalance the content route against the router so that C8's proportions are reachable.
