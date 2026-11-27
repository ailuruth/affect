# A scaled safety net: a gain governor in front of the ledger (the Q35 answer, D98)

Written 2026-11-27 for the operator's answer to Q35 (2026-11-28, D98): "design a different safety net whose limits scale with each expression's own limit; building continues alongside." Read under Q29 (D88: no situation-specific rules; innate only for the body, reflexes, newborn muscle patterns and the per-expression copy ceilings), D92 (the margin tuning stood down after three failures), D93 (a per-channel gain bound is necessary: conjecture-five-passes.md, Theorems 1 and 2), the build core (design-cayley-ledger.md, revision 9.2, §2.13, "Check of revision 9.1 and the answer", "Build finding at M0", "Build core summary"), critique-isospectral-q35.md, and the code read-only: engine/shadow/ledger.py, engine/shadow/shadow.py, engine/config/channels.py, engine/config/innate.py, tests/test_ledger_injected.py (F22's expected-to-fail test).

**Check:** `sims/scaled-safety-net/check.py` (numpy only; `python3 -I check.py > check.out.txt`, about 9 min; `quick` for 20-min sessions in about 1.5 min). Output in `sims/scaled-safety-net/check.out.txt`. **It checks the mathematics on synthetic signals. It is not evidence about people or behaviour.**

**Status:** design, checked numerically; independent critique pending (§6). Nothing in engine/, tests/, eval/, tools/ or research/build/ is changed by this note; §5 lists what would change.

---

## 0. Result in one paragraph

The current ledger's limits are already proportional to c_k in form: scaling a channel's ceiling and its partner-caused part together scales its output exactly (Lemma 0). What is not proportional is the leak. The ledger enforces its bound by clipping each frame into an interval, and the part it fails to remove grows with the unlisted route's own gain **relative to the ceiling**, g/c: on the same partners, the mean residual is 0.96 c at g/c = 1.2 and 1.59 c at g/c = 33, with no trend in c itself (row means 1.04–1.21 c). F22's injected copy has a fixed gain of 1, which is 2.9 c on the lip pull but 20–33 c on the lid, gaze, head and voice channels; that is why "small ceilings" fail. The new net puts a **multiplicative gain governor** in front of the unchanged ledger. Per channel it estimates, from the raw partner-caused part, the slope on his movement at every window and lag, and when one is confidently above κ_g c_k it multiplies the whole partner-caused part by a_k = κ_g c_k / (that slope). A multiplication commutes with every window and lag of the copy metric, so the residual becomes κ_g c_k times a fidelity ratio R that depends on his signal and the route's shape but **not on g/c and not on c** (Theorem 1). At κ_g = 0.60 the check gives, on every ceiling from 0.03 to 0.35 and every gain from 1.2 c to 33 c: **0.51–0.84 c** for pure delayed copies (on and off the lag grid, 1-h sessions), **0.44–0.76 c** on F22's own scenario as the test builds it and 0.51–0.74 c with the route built causally (current ledger 0.84–2.01 c and 0.72–3.06 c), 0.58–0.74 c for copies near the target on top of the counted routes, and **0 frames** of governor action on four natural partners with the counted routes only. F22's 1.0 c criterion would pass. Where it stops: a short detection span after an unlisted route switches on (5–21 s measured), which weighs more in short sessions (20-min sessions: up to 1.3–1.8 c on the most extreme gain); filtered routes, whose slow part the 10-s steps see weakly (the spec's F22 shape, onset lobe + 60-s low-pass: 0.61–0.96 c; a 30-s low-passed copy: 0.57–1.28 c, one cell above 1.0 c); and nonlinear routes with memory (D93's open gap).

---

## 1. The object

### 1.1 Intuition

Think of each expression channel as having a volume knob for "everything the partner causes on this channel", sitting just before the face. The old net was a hand on the output that pushes back frame by frame whenever the following looks too strong. If the thing pushing is far stronger than the limit (an unlisted copy at 20–33 times a small ceiling), the hand cannot push back cleanly, and what slips through is a fixed fraction of the push, not of the limit. The new net first turns the knob: it measures how strongly the partner-caused part follows his movement (at each delay up to 5 minutes), and if that is clearly more than 0.6 of the channel's own limit, it turns the whole partner-caused part down by exactly the factor that brings it to 0.6 of the limit. Because the knob scales everything on that channel by the same number, whatever follows him follows him in the same proportion at every timescale and every delay, so the limit holds wherever the metric looks. The old hand stays behind the knob for the first seconds, before the knob has evidence.

Everything is one rule for every channel: every threshold is a fraction of that channel's c_k, and no rule names a situation, a partner, a channel or a time of day.

### 1.2 Signals (per channel k, at the governor rate f_g = 10 Hz)

| Symbol | Domain | Meaning |
|---|---|---|
| u_k(t) | [0, 1] (one-sided), [−1, 1] (signed) | his counterpart on channel k, as the ledger reads it now |
| u⁰_k | same | the neutral partner's value: the input the shadow run is fed (rule 10). Before the session, his history is u⁰_k |
| r_k(t) | ℝ | the **raw** partner-caused part: assembled factual output minus assembled shadow output, before any net. Before the session, r_k = 0 |
| a_k(t) | [0, 1] | the governor's gain |
| x_k(t) = a_k(t) r_k(t) | ℝ | the governor's output, the ledger's input |
| y_k(t) = ȳ_k(t) + Ledger(u, x)_k(t) | | the rendered channel (the ledger of revision 9.2, unchanged) |

### 1.3 What is measured: window steps at every lag

For each window W ∈ 𝒲 = {10 s, 60 s}, exponential window means with α_W = 1 − exp(−1/(W f_g)):

- ū_{k,W}(t) = ū_{k,W}(t−1) + α_W (u_k(t) − ū_{k,W}(t−1)), started at u⁰_k;
- r̄_{k,W}(t) the same for r_k, started at 0.

His **step** at key (W, L) and the output's step at window W:

- π_{k,W,L}(t) = ū_{k,W}(t − L) − ū_{k,W}(t − L − W)
- ρ_{k,W}(t) = r̄_{k,W}(t) − r̄_{k,W}(t − W)

Steps (a change over one window) are used instead of deviations from a 30-min centre, because a slow centre that starts at the first frame drifts for half an hour, and that drift enters both his and the output's deviations in proportion to the route's own gain. That is the same kind of g-proportional error this design removes (the check's first version, with a centre, read 1.2–7.5 c on causal routes for this reason; differences read 0.5–0.7 c).

**Keys.** 𝒦 = {(10 s, L): L = 0, 2, …, 300 s} ∪ {(60 s, L): L = 0, 10, …, 300 s}: 151 + 31 = **182 keys per channel**, each lag step at most a fifth of its window. No 2-s window: it was tried at lags ≥ 10 s and engaged on 6–21 % of frames of natural partners (keys with a few seconds of evidence; §3.2).

### 1.4 The estimate, its noise floor and the engagement rule

With d = exp(−1/(τ f_g)), τ = 1800 s (the ledger's budget time), at each frame:

- C ← d C + ρ π, E ← d E + π², N ← d N + 1[t ≥ L + W] (frames on which the key is defined);
- A₂ ← d² A₂ + π² ρ², A₃ ← d² A₃ + π³ ρ, A₄ ← d² A₄ + π⁴ (for the weighted sandwich variance);
- **slope** β̂ = C / max(E, σ₀² N);
- **standard error** se = sqrt(m_W (A₂ − 2β̂A₃ + β̂²A₄)) / max(E, σ₀² N), with m_W = 2 W f_g (the serial correlation of window means: one independent window per 2W of frames);
- **engagement latch** ℓ ← [N ≥ n_min m_W and β̂ − z·se > κ_g c_k] or [ℓ and β̂ > κ_g c_k];
- **gain** a_k = min(1, κ_g c_k / max over latched keys of β̂), and a_k = 1 if no key is latched.

All sums reset at session start (as the ledger's budgets). On a zero-ceiling channel κ_g c_k = 0: a key whose slope is confidently above 0 latches and sets a_k = 0 until its slope falls to 0; the ledger's A3 rule stays behind it.

### 1.5 Every constant, its domain, value and how it scales with c_k

| Constant | Value | Domain / unit | Scales with c_k? | Kind |
|---|---|---|---|---|
| κ_g, the governor's target | **0.60** | fraction of c_k | **target = 0.60 c_k** | ceiling (part of the per-expression ceiling structure, like the ledger's κ) |
| engagement threshold | κ_g c_k + z·se | slope units | yes: κ_g c_k, and se is in the units of r_k, whose non-copy content is proportional to c_k (§3.3) | follows from the above |
| release threshold | κ_g c_k | slope units | yes | follows |
| attenuation step | a_k = κ_g c_k / β̂ | [0, 1] | yes: after the step the binding key's slope is exactly κ_g c_k, whatever c_k and the route's gain | follows |
| z, confidence multiplier | **3.0** | – | no (a probability level) | general statistical setting |
| n_min, evidence before a key may engage | **0.25** independent windows (5 s at 10 s, 30 s at 60 s) | windows | no (time) | general statistical setting |
| σ₀, floor on his step | **0.01** | his counterpart's units | no: it is on **his** movement (the regressor), not on the output; the same for every channel's counterpart | general statistical setting (the metric's own floor, conjecture-five-passes.md §1.3, is 0.03 on block SDs) |
| m_W, serial-correlation factor | 2 W f_g | frames per independent window | no | follows from W |
| τ, memory of the estimate | **1800 s** | s | no | as the ledger's budget time |
| windows 𝒲 | **10 s, 60 s** | s | no | as two of the ledger's windows |
| lag grid | **0–300 s**, step 2 s (10-s window), 10 s (60-s window) | s | no | as the ledger's scan (D90, 9.2) |
| f_g, governor rate | **10 Hz** | Hz | no | engineering (the ledger's reference rate) |
| **ledger (unchanged)** κ = 0.70, 97 keys, floor 0.10, τ 1800 s | as revision 9.2 | | target 0.70 c_k | ceiling |

Nothing in the table names a situation, a partner type or a channel; every output-side threshold is a multiple of c_k; the absolute quantities are all on his signal or on time.

### 1.6 The whole net, per frame

r = y_factual − y_shadow (assembled) → **x = a(u, r) · r** (governor) → x₂ = Ledger(u, x) (revision 9.2, unchanged) → rendered ȳ + x₂.

Both stages are attenuate-only and sign-preserving (0 ≤ a ≤ 1; the ledger clips between 0 and its input), so the net as a whole is: |x₂| ≤ |r|, x₂ r ≥ 0 on every frame.

---

## 2. The guarantee

### 2.1 Lemma 0 (both nets are exactly homogeneous)

For λ > 0, replacing (c_k, r_k) by (λ c_k, λ r_k) multiplies the output of the ledger and of the governor by λ and leaves a_k unchanged.

*Proof.* Ledger: S is a sum of products of output means and π, so S ∝ λ; the bound κ c E ∝ λ; b, the interval ends and the clip of x ∝ λ; the deviation floor and PI_EPS act on π only. Governor: C, A₃ ∝ λ; A₂ ∝ λ²; E, A₄, N do not depend on r; so β̂ ∝ λ, se ∝ λ, the latch predicate compares λ-scaled quantities with λ κ_g c_k, and a_k = λκ_g c_k / (λβ̂) is unchanged. ∎

Checked exactly in floating point (check section I: λ = 8 on four ceilings, governor and ledger together: output difference 0, gain difference 0).

**Consequence.** For either net, residual / c_k is a function of the route's **relative** gain g/c_k and of his signal only. "The small-ceiling gap" is therefore not about c_k: it is that the old net's residual grows with g/c_k, and a route of fixed gain is a large multiple of a small ceiling. The check confirms this (§4, section B): residual of the current ledger by g/c (column means over c = 0.03, 0.05, 0.10, 0.35) 0.96, 0.86, 1.00, 1.04, 1.23, 1.35, 1.59 c for g/c = 1.2, 1.5, 2, 3, 5, 10, 33; by c (row means over g/c) 1.12, 1.21, 1.04, 1.21 c. Read with Lemma 0, the operator's request "limits that scale with each expression's own limit" has one exact meaning: **the residual must be bounded uniformly in g/c_k**. That is what Theorem 1 gives.

### 2.2 Setting and assumptions

- **S1 (channel).** Channel k with c := c_k > 0 (zero ceilings: §2.5).
- **S2 (route class).** r(t) = r_L(t) + g · v(t − D), with v(s) = u_k(s) − u⁰_k for s ≥ 0 and v(s) = 0 for s < 0 (the route starts with the session, as the shadow convention makes it), gain g ≥ 0, delay D ∈ [0, 300 s]. r_L is the listed routes' part (fast gear, cone, appraisal, free display), bounded by construction (pooled sup total ≤ 0.974 c; revision 6, J3).
- **S3 (metric).** For a block length b ∈ ℬ = {2, 10, 30, 60} s, lag L ∈ [0, 300 s] and block phase, β_b(L)[y] is the slope of the block means of y (shifted by L) on his block means over the session [0, T]; ρ*[y] is the maximum over b, L and phase (tests/synth.py's `worst_block_slope`, with a 30-s block added).
- **A1 (fidelity).** Define the **fidelity ratio** of the raw partner-caused part, R := ρ*[r] / max_{κ∈𝒦} β̂_κ(T), the ratio of the metric's worst slope to the governor's largest key slope, both computed on r, and the **amplitude ratio** Λ := max_b rms(r_b) / (sd(u_b) · max_κ β̂_κ) (block-mean size of r per unit of his block movement, against the same key slope). Both are homogeneous of degree 0 in r (unchanged when r is scaled) and do not depend on c. Assume R, Λ ≤ R̄. (For a delayed copy, Λ ≈ R ≈ 1/ψ, Lemma 1.)
- **A2 (estimation).** On [τ_d, T] (τ_d defined below), the latched keys' slopes vary by at most a relative ε_a: a(t) ∈ [ā(1 − ε_a), ā(1 + ε_a)].
- **A3 (noise relative to the ceiling).** η := max se / c over keys whose slope lies in (κ_g c, κ_g c + z·se] (keys the latch may leave unlatched). Because se is computed from r, whose non-copy content is in the units of c (§3.3), η does not depend on c.
- **A4 (his signal and the detection span).** τ_d is the first time a key within one lag step of D latches. q_tr is the largest share of his session block variance that falls in any span of length τ_d − D. Assume his step variance at the 10-s window exceeds σ₀² somewhere in that span (he moves).
- **A5 (ledger stage).** q_cl is the share of his block variance in blocks where the unchanged ledger stage changes frames after τ_d.

### 2.3 Theorem 1 (the residual is bounded uniformly in g/c)

Under S1–S3 and A1–A5, the rendered partner-caused part satisfies

  ρ*[x₂] ≤ c · [ R̄ (κ_g + z η)(1 + ε_a + q_cl) + (g / c) q_tr ].

The first term does not depend on g/c or on c. The last is the detection span, which no causal net can avoid (a route cannot be measured before it has acted); it shrinks with the session length T for a fixed detection time.

*Proof.*
1. **Steady state, constant gain.** Suppose a(t) = ā on [τ_d, T]. The metric is linear in the output, so β_b(L)[ā r] = ā β_b(L)[r] for every b, L and phase, hence ρ*[ā r] = ā ρ*[r] = ā R B*, with B* = max_κ β̂_κ.
2. **The gain.** Let B_ℓ be the largest latched slope, ā = κ_g c / B_ℓ. Every unlatched key has β̂ ≤ κ_g c + z se ≤ c(κ_g + zη) (it failed the lower-bound test, or it was released at β̂ ≤ κ_g c). So B* ≤ max(B_ℓ, c(κ_g + zη)), and ā B* ≤ max(κ_g c, κ_g c (κ_g + zη) c / B_ℓ) ≤ c(κ_g + zη), because B_ℓ > κ_g c. If nothing is latched, ā = 1 and B* ≤ c(κ_g + zη) directly. Either way ρ*[ā r] ≤ R̄ c (κ_g + zη).
3. **Varying gain.** Write a = ā + δ with |δ| ≤ ε_a ā. For each b, L, phase, Cauchy–Schwarz gives |β[δ r]| = |Cov((δr)_b, u_b)| / Var(u_b) ≤ ε_a ā rms(r_b) / sd(u_b) ≤ ε_a ā Λ B* ≤ ε_a R̄ c (κ_g + zη), using step 2's bound on ā B*.
4. **Ledger stage.** It removes v = x − x₂ with |v| ≤ |x| and sign(v) = sign(x), only on the blocks counted in q_cl. Cauchy–Schwarz restricted to those blocks gives |β[v]| ≤ (ā rms(r_b)/sd(u_b)) q_cl ≤ q_cl R̄ c (κ_g + zη), by the same chain as step 3.
5. **Detection span.** On [D, τ_d] the output is at most g|v| in absolute value (the ledger only attenuates). Its covariance with his block means, divided by his total block variance, is at most g · sqrt(A_tr B_tr) / S ≤ g q_tr by Cauchy–Schwarz restricted to those blocks (A_tr, B_tr: his block variance in the span at the two lags; S: his total). The slope over [0, T] is at most the steady-state slope plus this term, since the steady-state blocks' variance is part of S.
6. Sum 1–5. ∎

### 2.4 Lemma 1 (the fidelity ratio of a delayed copy)

For r = g·v(t − D) alone, in the limit of a long stationary session: (i) the metric's worst slope is g (at L = D the block means of r are exactly g times his; at other lags the slope is g times an autocorrelation, at most 1); (ii) the governor's key at the lag nearest D estimates g ψ, where ψ is the autocorrelation of his 10-s step series at the lag offset |L − D| ≤ 1 s, which for a window mean of W = 10 s is about exp(−|L − D|/W) ≥ 0.90 when his movement has little power above 1/W (an assumption on his signal: fast movement lowers ψ); so R ≈ Λ ≤ 1/ψ ≤ 1.11. With listed routes added (r_L), R is a ratio of their sum and stays in the same range as long as the copy dominates; near the threshold the listed routes' own slope enters both numerator and denominator.

Finite sessions add a sampling term: the metric picks the worst of about 300 lags × 6 phases × 4 block lengths. **Measured** (§4, sections D and H): the steady-state residual is 0.60–0.63 c for pure copies of any g/c, i.e. R = 1.00–1.05, and 0.51–0.74 c with the counted routes underneath.

### 2.5 Zero-ceiling channels

κ_g c = 0, so any confidently positive slope sets a_k = 0 (the whole partner-caused part removed while latched), and the ledger's A3 holds behind it. Measured: the block-metric slope on the 13 zero-ceiling channels of F22's scenario is 0.003–0.007 (current ledger 0.004–0.017). Theorem 1 with c = 0 reads ρ* ≤ g q_tr + (whatever the ledger's A3 leaves): the detection span only.

### 2.6 The numbers, and the target ≤ 0.9 c

With κ_g = 0.60, z = 3, R̄ = 1.05 (measured), ε_a ≤ 0.02 and q_cl ≤ 0.05 (measured: the ledger stage changed 0–9 % of frames after detection in F22's scenario, mostly within the first minutes), the first term is 1.05 (0.60 + 3η)(1.07). **For η ≤ 0.05** (measured se at the end of natural sessions: 0.008–0.065 c by channel; 0.01–0.03 c on most) this is ≤ 0.85 c, **independent of c and of g/c**. The detection term (g/c) q_tr adds, for a 1-h session with detection 15 s after onset and his movement spread evenly (q_tr ≈ 0.004): 0.01 c at g/c = 3, 0.08 c at g/c = 20, 0.14 c at g/c = 33. So the stated bound reaches 0.9 c for g/c ≤ about 10 in 1-h sessions and needs his movement in the ~15-s detection span to be at most about half his session average for g/c = 33. The measured residuals sit well inside it (0.44–0.84 c across all ceilings and gains, F22's gain-1 copies included), because the unchanged ledger stage attenuates the detection span too, which the bound does not credit.

**What the theorem does not cover (where the guarantee stops).**
- **Nonlinear routes with memory** (D93, conjecture-five-passes.md O1): a route whose slope depends on his history in a way that a fixed per-key regression does not track (for example one that follows only after he has been still for a minute) can have R far above 1. Theorem 1 still holds with that R, but nothing bounds R. This is the open gap noted in D93; it is not closed here.
- **Routes whose gain sits at long periods.** A copy low-passed with time constant τ_f has a smaller slope on the 10-s steps (which weight his faster movement) than on 60-s block means, and the 60-s keys carry more noise, so R grows with τ_f. Measured: τ_f = 30 s gives 0.57–1.28 c (one cell above 1.0 c, at c = 0.05, g/c = 33); the spec's F22 shape (onset lobe + 60-s low-pass) gives 0.61–0.96 c, inside F22's 1.0 c but above 0.9 c in 3 of 28 cells (0.92–0.96 c). For these shapes the target ≤ 0.9 c is not met; 1.0 c is, except the one τ_f = 30 s cell. Periods beyond the 60-s window's reach (≳ 2 min) are seen only by the unchanged ledger.
- **Fast routes at lags 0–3 s** whose gain is only at the 2-s scale (an unlisted fast echo): the governor has no 2-s window; the ledger's 2-s keys remain the only net there, as now.
- **Delays beyond 300 s** are unscanned, as now.
- **Cross routes** from his other channels (conjecture Theorem 2's weighted term): the governor regresses on his same-channel counterpart only, as the ledger does.
- **Short sessions.** The detection term grows as 1/T: in 20-min sessions the check reads up to 1.3–1.8 c for g/c = 20–33 on two channels of F22's scenario (`quick` run). F22 is judged on ≥ 1-h sessions (≥ 2 h per person in the spec), and the online monitor (F1 live) should use windows of at least that length for this guarantee to apply.
- **A2 and A3 are statistical.** β̂ − z se > κ_g c is a 3-σ test with a sandwich variance; with 182 keys × 20 channels and correlated estimates, a spurious latch is possible. Its cost is attenuation (never growth), and the check saw none on four natural partners.

---

## 3. The cost

### 3.1 False-positive attenuation on natural partners (F1: the net binds on ≤ 1 % of frames)

| Natural partner, counted routes only (fast gear 0.45 s + held 2-min route 0.22 c_k), 1 h, all 33 channels | Governor a < 1 (worst channel) | Ledger stage frames changed (worst channel), unchanged from now |
|---|---|---|
| seed 7 | **0.000** | 0.000 |
| seed 8 | **0.000** | 0.046 (HP, F0) |
| seed 9 | **0.000** | 0.001 |
| seed 10, livelier (30-s mood blocks on every channel) | **0.000** | 0.083 (PAU, LAT) |

The governor adds no false-positive attenuation on these partners: the counted routes' worst block-metric slope is 0.36–0.42 c, under 0.60 c, and no key passed the engagement test. **A finding about the existing ledger, independent of this design:** on two of the four synthetic partners the unchanged 97-key ledger changes 4.6 % and 8.3 % of frames on signed channels whose fast gain is 0.8 c_k (HP, F0; PAU, LAT), above F1's 1 %. tests/test_ledger_injected.py's `test_counted_routes_untouched` uses one 30-min partner (seed 7), where it is within 1 %. Raising the ledger stage's κ to 1.0 roughly halves this (3.3 % and 1.8 %), and is possible once the governor carries the guarantee (the ledger stage then only covers the detection span and fast lags 0–3 s); it is not proposed here, because it changes the bit-identical ledger and would need its own check.

**On an extreme partner** (counted routes running high): the governor trims them to 0.60 c (§4 G: counted slope 0.70 c → 0.59–0.62 c, 0.85 c → 0.56–0.61 c, 0.974 c → 0.60–0.61 c, on every ceiling; at 0.50 c it does nothing). The current ledger trims at 0.70 c; the new net trims at 0.60 c. So for a partner who drives the counted routes above 0.60 c at some delay, fast mimicry is scaled down on that channel for the rest of the session (the estimate's memory is 30 min). On the natural partners this never happened.

**When an unlisted route is caught**, a_k scales down everything the partner causes on that channel, fast mimicry included (to about 0.6 c / g of its size). That is the price of an attenuation that commutes with the metric, and it is paid only when a route nobody listed is copying.

### 3.2 Why no 2-s window, and the detection time

A 2-s window (lags 10–300 s, 1-s steps) detected gain-1 copies in 2–6 s instead of about 15 s, but on natural partners it latched on 6–21 % of frames (keys holding 1–8 s of evidence, slopes 1.6–6.8 c from the fast gear's bursts), even with 8 s of evidence required. It is left out. **Detection time** after an unlisted route starts: one window plus n_min (10 + 5 s at the 10-s window) once he moves; measured 5.5–21 s on F22's scenario, independent of c (Lemma 0) and nearly independent of g/c once g/c is above about 1.5. Copies near the target are detected later (more evidence is needed to separate 0.7 c from 0.6 c), but they then leave little excess (§4 H: 0.58–0.74 c).

### 3.3 Small ceilings and estimation noise

Small ceilings are **not** noisier for this estimator. se is computed from r, and every listed route's gain is a fraction of c_k (fast gains G_k/c_k = 0.10–0.80; cone, cross and appraisal shares are fractions of c_k), so the part of r that is not the copy is proportional to c_k, and se/c_k depends on G_k/c_k and his signal, not on c_k. Measured se at the end of natural sessions: LD (c 0.05) 0.011 c, BU_L (c 0.35) 0.024 c, YAW (c 0.03, G/c 0.8) 0.054 c, VG (c 0.05, G/c 0.8) 0.065 c. What would break this is noise in r that is **not** proportional to c_k: the shadow run sharing the agent's randomness exactly (rule 10) makes r exactly 0 wherever no partner route acts, so such noise can come only from rounding or from a component that differs between the runs for another reason (an A5 failure). Section F of the check adds white noise of σ 0.005 and 0.02 (0.17 c and 0.67 c on a 0.03 channel) to r: the residual changes by at most 0.11 c (0.63 → 0.74 c at c = 0.03, g/c = 1.5), because the 10-s window averages it out. Slow non-proportional noise would not average out; its effect is to raise η, and the requirement is plain: such noise at periods ≥ 10 s must stay below about 0.05 c_k × (his 10-s step SD) × √(independent windows), about 0.05 × 0.03 × 0.1 × √90 ≈ 1.4 × 10⁻³ on a 0.03 channel. A5 (shadow equality) already enforces far less than that.

**Best achievable bound, stated plainly.** For flat-gain delayed copies in sessions of ≥ 1 h, the governor holds every ceiling at about 0.6 R c ≈ 0.60–0.63 c after detection, and the session residual at 0.51–0.84 c measured for g/c up to 33, on c = 0.03 as on c = 0.35. Nothing about small ceilings forces a worse bound; what forces one is the detection span against the session length, and the route's shape.

### 3.4 Compute and memory

182 keys × 33 channels × about 25 flops at 10 Hz: about 1.5 Mflop/s, well under the ledger's 1 ms frame budget (spec §1.6). Memory: ring buffers of his and the output's window means for 360 s at 10 Hz, 2 windows × 2 signals × 33 channels: about 3.8 MB in float64; the running sums 6 × 33 × 182 floats ≈ 0.3 MB.

---

## 4. Numerical check (a check of the mathematics, not evidence about people)

`sims/scaled-safety-net/check.py`, numpy only, synthetic partners by tests/synth.py's recipe (rewritten in numpy), the current ledger re-implemented from engine/shadow/ledger.py's algorithm, 1-h sessions at 10 Hz. Metric: worst block-mean slope over 2-, 10-, 30- and 60-s blocks, lags 0–300 s, 6 phases, as a multiple of c_k. Output: `check.out.txt`. Two constructions of F22's injected copy: **as written** in tests/test_ledger_injected.py (first D seconds padded with his first frame, minus his session mean) and **causal** (0 until D has elapsed, then g(u(t − D) − u⁰), as the engine would produce it).

**A/C. F22's scenario (gain-1 copy on every channel; delay 10–300 s by channel).**

| | Current ledger (κ 0.70), small-ceiling channels | Current, all 20 capped | **New net**, all 20 capped |
|---|---|---|---|
| as written | LD 2.01, VG 1.25, F0 1.21, RT 1.22, PAU 1.55, LAT 1.21, TILT 1.48, HG 1.23, YAW 1.06, EN 0.84 c | 0.84–2.01 c | **0.44–0.76 c** |
| causal | LD 3.06, F0 1.89, RT 1.70, PAU 1.60, LAT 1.41, TILT 1.41, BO 2.12, FR 2.37 c | 0.72–3.06 c | **0.51–0.74 c**; 0.63 c worst read from 600 s on |

The current ledger reproduces the M0 gap (1.1–2.0 c and beyond on small ceilings; LP at c 0.35, g/c 2.9: 1.07 c). Final a_k equals κ_g c_k / g on every channel to three decimals. Detection 5.5–21 s after the delay (causal construction; in the as-written construction the copy's constant first D seconds delay one channel's detection to 103 s without harm). Zero-ceiling channels 0.003–0.007. Attenuate-only on every frame.

**B. Diagnosis: the current ledger by ceiling and relative gain** (causal copy, delay 90 s; residual / c). Rows c, columns g/c:

| c \ g/c | 1.2 | 1.5 | 2 | 3 | 5 | 10 | 33 |
|---|---|---|---|---|---|---|---|
| 0.03 | 0.89 | 0.85 | 1.04 | 1.25 | 0.97 | 1.92 | 0.94 |
| 0.05 | 1.08 | 1.00 | 1.17 | 0.76 | 1.53 | 1.08 | 1.85 |
| 0.10 | 0.80 | 0.79 | 0.94 | 1.28 | 1.02 | 1.38 | 1.10 |
| 0.35 | 1.07 | 0.79 | 0.87 | 0.85 | 1.40 | 1.02 | 2.45 |

Each cell is one partner, so cells are noisy; the column means rise with g/c (0.96 → 1.59 c) and the row means do not move with c (1.04–1.21 c), as Lemma 0 requires.

**D. New net over the same grid** (residual / c; ranges over all 28 cells):

| Route | Range | Notes |
|---|---|---|
| delay 90 s (on the lag grid) | **0.51–0.84 c** | 0.60–0.63 c in 24 of 28 cells |
| delay 47.35 s (off every grid) | **0.52–0.83 c** | |
| delay 213.7 s (off every grid) | **0.52–0.83 c** | |
| delay 120 s, copy low-passed τ 30 s | 0.57–1.28 c | outside Lemma 1's class; one cell (c 0.05, g/c 33) above 1.0 c |
| delay 120 s, spec F22 shape (onset lobe + 60-s low-pass) | **0.61–0.96 c** | filtered shape (§2.6): under F22's 1.0 c in every cell, above the 0.9 c target in 3 of 28 (0.92–0.96 c) |

**E. Cost on natural partners:** §3.1 table.

**F. Absolute noise in r** (σ 0, 0.005, 0.02; grid at delay 90 s): 0.51–0.84, 0.51–0.84, 0.50–0.84 c; largest change 0.11 c (c 0.03, g/c 1.5).

**G. Counted routes above the target** (slope s c at 0.45 s): s = 0.50 → 0.50–0.51 c, untouched; s = 0.70, 0.85, 0.974 → 0.56–0.62 c, a ≈ 0.86, 0.71, 0.62. Same on c = 0.03, 0.05, 0.10, 0.35.

**H. Copies near the target, on top of the counted routes** (natural partner, delay 60 s, all 20 capped channels):

| g/c of the copy | 0.5 | 0.8 | 1.0 | 1.2 | 2.0 | 5.0 |
|---|---|---|---|---|---|---|
| raw (copy + counted), worst channel | 0.71 | 1.01 | 1.21 | 1.41 | 2.22 | 5.28 |
| **new net, worst channel** | **0.71** | **0.74** | **0.71** | **0.68** | **0.68** | **0.73** |

**I. Lemma 0:** exact (differences 0 at λ = 8).

**Not checked:** a mirror-only partner (report 12 noted the current net intervenes often against one; the governor regresses the output on his past, and a partner who copies the agent makes his past correlate with the agent's own partner-caused part, so it may latch; its cost is attenuation, not growth); recorded partners (M4, on the operator's Mac); the 30-Hz engine rate (the governor runs at 10 Hz on decimated window means, §5).

---

## 5. What would change in the code

**New file `engine/shadow/governor.py`.**
- `class Governor(ceilings, fs, u_neutral, kappa_g=GOV_KAPPA, keys=GOV_KEYS, z=GOV_Z, n_min=GOV_N_MIN, sigma0=GOV_SIGMA0, tau=GOV_TAU_S)`, vectorised over (channels, 182 keys) like `Ledger`.
- `reset(u_neutral)`: at session start; window means of u start at u⁰ (the shadow's neutral input vector), of r at 0; every sum, N, the latch and a = 1 reset.
- `step(u, r) -> x`: the update of §1.3–1.4; returns a ⊙ r; exposes `a`, `latch`, `beta`, `se` for logging and asserts.
- **Rate.** The engine runs at 30 Hz (`Shadow(fs=30)`). The governor updates its window means at 30 Hz and its sums and gain at 10 Hz (every third frame), holding a for the frames between. Its key lags are in seconds, so the key set is rate-independent.
- The reference implementation to match is `Governor` in `sims/scaled-safety-net/check.py`; a regression test should compare the engine's governor with it at 10 Hz bit for bit, as the ledger's test does.

**`engine/shadow/shadow.py`** (around line 270, the frame step): r = y − ȳ; **x = self.governor.step(fr.u, r)**; x₂ = self.ledger.step(fr.u, x); rendered ȳ + x₂. Construct `self.governor = Governor(TABLE.c, self.fs, u_neutral)` beside `self.ledger` (line 163); reset both at session start. Per-minute logging (spec §1.6) adds per channel: min a_k, the latched key with the largest slope, its β̂ and se.

**`engine/shadow/ledger.py`:** unchanged (the regression test stays bit-identical). Its docstring's "the partner-caused part" becomes "the governor's output".

**`engine/config/innate.py`: new constants**, one rule for every channel:

| Name | Value | Unit | Category | Why |
|---|---|---|---|---|
| `governor_kappa` | 0.60 | fraction of c_k | **ceiling** | target of the multiplicative governor, part of the per-expression ceiling structure (Q29: allowed innate item) |
| `governor_keys` | 151 keys (10 s; 0–300 s by 2 s) + 31 keys (60 s; 0–300 s by 10 s) | s | ceiling | the scan, as the ledger's |
| `governor_z` | 3.0 | – | ceiling | confidence multiplier of the engagement test |
| `governor_n_min` | 0.25 | independent windows | ceiling | evidence before a key may engage |
| `governor_sigma0` | 0.01 | his counterpart's units | ceiling | floor on his step variance (the regressor) |
| `governor_tau_s` | 1800.0 | s | ceiling | memory of the estimate (= the ledger's budget time) |
| `governor_rate_hz` | 10.0 | Hz | generic (engineering) | update rate of the sums and gain |
| `governor_frame_budget_ms` | 0.5 | ms | generic (engineering) | cost per update on one performance core |

`INNATE.lock` and `innate_names.txt` are regenerated with them (the lock's usual procedure). No constant is a situation-specific rule: each applies to every channel and names no partner, event or time of day.

**`engine/invariants/asserts.py`:** a new check, **A4g**, per frame: 0 ≤ a_k ≤ 1; x_k = a_k r_k exactly; a_k = 1 when no key is latched; on zero-ceiling channels a_k ∈ {0, 1}. Failure handling as A4 (the channel renders ȳ_k). A3 and A4 apply to the ledger stage with its input x in place of r; A4's |x₂| ≤ |r|, x₂ r ≥ 0 then also holds against the raw r.

**Tests that would change.**
- `tests/test_ledger_injected.py`: the fixture runs governor then ledger (`Governor(TABLE.c, FS, u_neutral=U.mean(0))`); `test_copy_held_below_ceiling_on_capped_channels` **loses its xfail** (expected worst ≈ 0.76 c on its own seed and construction; it could be tightened to ≤ 0.9 c); the A3/A4 checks compare the ledger stage with its input x; `test_counted_routes_untouched` also asserts a_k = 1 on ≥ 99 % of frames.
- **New `tests/test_governor.py`:** Lemma 0 (scale c and r by λ: a identical, output × λ, exactly); attenuate-only and x = a r on every frame; the latch's hysteresis; zero-ceiling behaviour; the (c, g/c) grid of §4 D at ≤ 0.9 c on 1-h synthetic partners (on- and off-grid delays); counted routes at s = 0.85 c trimmed to ≤ 0.65 c; natural partners a ≡ 1; regression against the reference `Governor` at 10 Hz.
- `tests/test_ledger_regression.py`: unchanged.
- **Elsewhere, not edited here:** research/build/spec.md §1.6 (the governor before the ledger; A4g in the assertion table), §5.1's F22 row ("so only the ledger sees it" becomes "so only the net, governor and ledger, sees it"; the injection point after assembly is unchanged) and the F22 synthetic-construction note (use the causal construction, which is what the engine produces); `eval/f22_delayed_copy.py` (run the governor before the ledger in the ledger-only re-run of §5.5; its per-person cost rises by about half the ledger's); design-cayley-ledger.md §2.13 and the Build core summary (the ledger's figures replaced by Theorem 1's); DECISIONS.md (a D-entry recording the governor); questions.md Q35 (closed by D98 if the critique holds).

---

## 6. Independent critique

pending
