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

Written 2026-11-27 by an independent checker who did not write the design. Extra checks in `sims/scaled-safety-net/critique_check.py` (numpy only; it executes check.py's definitions verbatim, so the Governor, Ledger, partner recipe and metric are the design's own; `python3 -I critique_check.py`, about 5 min). Output in `critique_check.out.txt`. **Synthetic signals: a check of the mathematics, not evidence about people.** Pure routes are run at c = 0.05 only, which by Lemma 0 (exact) loses nothing; each cell is the worst of 2 synthetic partners, so cells are noisy.

**Verdict: holds with stated limits, and the limits are wider than §2.6 states.** For the class it was built for (a constant-gain, linear, delayed copy, in ≥ 1-h sessions) it holds: I reproduce 0.62–0.66 c at g/c 3–33, against 0.99–2.96 c for the current ledger. It is a real improvement on F22's mechanism test. It is **not** a catch-all net bounded uniformly in g/c: Theorem 1 is conditional on an assumption (A1) that holds only for that class, and outside it routes reach 1.03–1.24 c in 1-h sessions. It also does not make the net pass F1 or F22's counted-routes clause. Fit to implement as an attenuate-only stage in front of the ledger. It should not close Q35/D98 as "the net holds every limit".

### 6.1 The proof, step by step

- **A1 is the conclusion in disguise.** R is defined as (the metric's worst slope) / (the governor's largest key slope). Assuming R ≤ R̄ amounts to assuming that the governor's keys see what the metric sees, and that is the whole question for an unlisted route. Lemma 1 bounds R only for a pure delayed copy. R̄ = 1.05 is then "measured" on the same runs the theorem is meant to bound. For every other shape R is unbounded a priori; §6.2 measures R ≈ 2 for slow routes. The theorem is correct as a conditional, but it is not a guarantee about unlisted routes in general. The design says this for nonlinear routes with memory. It applies just as much to **linear** routes whose gain sits outside the 10-s/60-s step keys.
- **"Uniform in g/c" is not what the bound says.** Its last term, (g/c) q_tr, is linear in g/c at fixed T. In 20-min sessions it is the design's own 1.3–1.8 c. So the residual is bounded uniformly in g/c only in the limit of long sessions.
- **Step 2 (fine as algebra).** It needs every unlatched key to have passed n_min. Keys still short of evidence are unbounded, which is part of the detection span. The numbers in §2.6 then take η ≤ 0.05, while §3.3 measures se up to 0.065 c (VG) and 0.054 c (YAW). With η = 0.065 the first term is 1.05 (0.60 + 0.195)(1.07) = 0.89 c before any detection term, so the stated ≤ 0.9 c is not implied on the G/c = 0.8 channels.
- **Step 3.** The block mean of δ·r is not δ times the block mean of r, so Cauchy–Schwarz needs the rms of block means of |r|, not of r_b. Both include r's DC part. When the neutral input u⁰ is not his session mean (in the engine u⁰ is b_id, a 6-session baseline, not today's mean), r carries g(ū − u⁰), and Λ is no longer ≈ R. This is a gap in the proof only: numerically the offset costs little (§6.2 K1).
- **Step 4: q_cl, not √q_cl, needs an unstated assumption.** Cauchy–Schwarz restricted to the ledger-changed blocks Q gives sqrt(Σ_Q x_b²) · sqrt(Σ_Q u_b²) / S. That equals a q_cl factor only if the output's energy in Q is proportional to his energy in Q at the same lag. Without that assumption the factor is √q_cl: at q_cl = 0.05 that is 0.22, and the first term becomes 1.05 · 0.75 · 1.24 ≈ 0.98 c. The value "q_cl ≤ 0.05 (measured)" is also not what check.out.txt shows. In the causal construction the ledger stage changes up to 9.1 % of frames (F0); as written, 60 % (RT) and 36 % (BRE).
- **Step 5.** It uses his block variance in the span. The output in the span is g(u − u⁰), so with u⁰ ≠ ū the term carries the offset as well (the same correction as step 3).
- **Lemma 0 and step 1** are correct; I confirmed Lemma 0's exactness from the check's own section I.
- **The figures 0.44–0.84 c** are correctly reported for the design's runs. They are measured, not implied by the theorem: with the corrections above the theorem's own bound sits at about 0.9–1.0 c for 1-h sessions.

### 6.2 Counterexamples (critique_check.py K1–K5; residual / c, current ledger → new net)

| Route (1 h, c = 0.05) | g/c 3 | g/c 10 | g/c 33 |
|---|---|---|---|
| copy, u⁰ = session mean (the design's case) | 1.49 → 0.65 | 1.35 → 0.63 | 2.07 → 0.66 |
| copy, u⁰ = mean − 0.10 / + 0.05 (b_id ≠ today's mean) | 1.15 → 0.65 / 1.34 → 0.62 | 0.99 → 0.65 / 1.46 → 0.62 | 1.37 → 0.63 / 2.96 → 0.75 |
| **copy low-passed τ 120 s** | 1.35 → **1.24** | 0.87 → 0.84 | 2.82 → **1.04** |
| **copy low-passed τ 300 s** | 0.78 → 0.78 | 1.28 → **1.20** | 0.74 → 0.70 |
| **copy on 6 min / off 24 min** | 0.70 → 0.70 | 0.86 → 0.86 | 1.69 → **1.14** |
| **copy on 10 s / off 50 s** | 0.47 → 0.47 | 1.20 → **1.03** | 1.14 → 0.68 |
| copy, gain ramps linearly 0 → g over the hour | 0.74 → 0.71 | 1.03 → 0.88 | 1.93 → 0.83 |
| copy, gain grows exponentially (θ 300 / 600 s) | ≤ 0.53 | ≤ 0.69 | ≤ 0.79 |
| fast echo: 2-s high-passed copy, delay 30 s | 0.88 → 0.88 | 2.39 → 0.79 | 3.04 → 0.68 |

- **Slow routes fail F22's 1.0 c** (1.04–1.24 c). The 10-s steps are dominated by his fast movement and the 60-s steps see little of a 2–5-min route, so R ≈ 2 and the governor barely engages. The net reverts to the current ledger's behaviour. The design names "periods ≳ 2 min, seen only by the ledger" but measured only τ = 30 s. *General fix:* add longer windows (e.g. 120 s and 300 s steps) to the same c-scaled test, or regress centred window means started at u⁰. This needs its own false-positive check.
- **Switched routes.** With long off-periods, β̂ (30-min memory) decays below κ_g c and the key releases. On the next on-period, β̂ climbs back slowly because the off-period's evidence dilutes it, so the route runs at full gain for minutes (1.14 c). A 10-s/50-s duty cycle gives 1.03 c. *General fix:* a ratchet (a_k non-increasing within a session once latched), or a short-memory estimate (e.g. τ = 120 s) whose latches combine with the 30-min ones by max. Both are c-scaled general settings. A ratchet makes false positives last for the rest of the session.
- **Growing gain: invisible to the session metric, not contained.** At the end of the session the effective gain a(t)g(t) is 0.85–1.21 c for a linear ramp, and 2–10 c for exponential growth (θ 300 s at g/c 10: a is still 1 at 60 min, so the copy renders at full gain 10 c). The session-wide metric reads ≤ 0.79 c only because it averages over an hour in which the route was mostly small. The online monitor (F1 live) on shorter windows would flag it. This is the realistic shape of an unlisted route in a learning engine (a plastic weight that grows). The 30-min memory always lags a gain that grows faster than τ. *General fix:* the multi-memory estimate above. No causal estimator can bound arbitrarily fast growth, and that limit should be stated.
- **Short sessions:** the design's own 1.3–1.8 c at 20 min stands. There is no general fix within a causal net other than faster detection (the 2-s window, rejected for false positives). The guarantee should be stated as "per ≥ 1-h window", and the F1 live monitor's window chosen to match.
- **Held:** off-grid delays, u⁰ offsets (≤ 0.75 c), a fast echo at a 30-s lag (0.68–0.88 c; the 10-s keys catch enough), and copies split across lags (both the governor and the metric are marginal per-lag regressions, so they see the same sum).
- **Not covered, consistent with the metric:** copies split across channels (cross routes). The governor regresses on the same channel, as the metric does (D93's weighted term).
- **Mirror partner / feedback loop: not simulated.** Argument only: the governor regresses the raw r, so it has no loop through its own output. Once latched, the loop gain is about h · 0.6 c / ψ ≤ 0.25, which is stable. Before detection, a route with g · h > 1 can run unstably (clipped to [0, 1]) for the ~15-s detection span.

### 6.3 Situation-specific rule? Q18? The listed routes?

The governor is a general setting: one rule on every channel, output-side thresholds ∝ c_k, absolute quantities only on his signal or on time, and nothing names a partner, event, channel or time of day. It is categorised "ceiling" like the ledger's own constants in engine/config/innate.py. It names no emotion and rewards nothing; it can only lower output. Q18:
- **Per channel, sign-preserving (a ≥ 0), under the ceiling:** yes.
- **Never a settling state:** there is tension. Once a route is caught, the governor holds it at a steady ≈ 0.6 c copy for the rest of the session rather than pushing away from copying. *General fix:* a slope confidently above the listed routes' provable pooled sup (0.974 c_k) can only come from an unlisted route, so a may then be pushed lower than κ_g c / β̂ (to 0 if one accepts losing that channel's fast mimicry).
- **Listed routes:** a legal but lively partner who drives the counted routes to 0.70–0.974 c (all within their by-construction bound) has that channel's fast mimicry cut by 14–38 % for ~30 min (§4 G: a < 1 on 97–99.6 % of frames). That changes the listed routes' intended behaviour more than the ledger's 0.70 did. *General fix, if assembly is additive per route:* the engine knows each listed route's contribution r_L, so the governor could scale only r − r_L, the unlisted remainder. If assembly is not additive, the trade-off between κ_g and the bound is real.

### 6.4 False-positive cost (F1: ≤ 1 % of frames)

- **The governor's "0 frames" depends on u⁰ = his session mean.** That is non-causal, and check.py, §3.1 and the proposed test fixture all use it. With u⁰ = mean − 0.10 (b_id below today's level), seed 10 latches on LP for **4.3 % of frames with a down to 0.30**, and with + 0.10 on RT for 0.3 % (a down to 0.45). The start-of-session step from u⁰ to his level, with only n_min = 0.25 windows (5 s) of evidence, is enough to pass the 3-σ test. Hysteresis and the 30-min memory then hold the latch. *General fix:* require more evidence (n_min ≥ 1–2 windows), or start the sums with a prior of zero slope worth one window. The cost is slower detection, roughly +10–20 s.
- **The ledger stage's finding is worse than §3.1 says.** I rebuilt `test_counted_routes_untouched`'s exact recipe over seeds 7–14 (K7; the engine's own Ledger gave the same figures in a separate run). The worst capped channel's frames changed:
  - 30-min sessions: 0.07, 0.07, **16.6, 10.8, 6.9, 1.4, 2.6**, 0.09 %. Five of 8 partners are above 1 %.
  - 1-h sessions: 0.00, **3.2**, 0.09, **5.8**, 0.17, 0.04, **1.06**, 0.21 %. Three of 8 are above 1 %.
  
  The test passes only on seed 7. Since the proposed net is governor + unchanged ledger, **the net as proposed fails F1's ≤ 1 % and F22's second clause on most synthetic partners**. Raising the ledger's κ to 1.0 (§3.1: 3.3 % and 1.8 %) does not fix it. This is open and must be solved before F22 is claimed. The governor does not cause it, but §5's plan to assert "a_k = 1 on ≥ 99 %" in the seed-7 test would hide it.

### 6.5 F22

- **Would the test pass?** With the governor before the ledger and u_neutral = U.mean(0), yes. check.py reproduces the fixture's partner draws (same RNG call order) and reads 0.76 c with a stricter metric (a 30-s block added), so the test's metric gives at most that.
- **Is it the right test? Not on its own.**
  1. It exercises exactly the model class the governor estimates: constant gain, pure delay, linear. Passing it is weak evidence of a catch-all.
  2. The fixture's u⁰ = session mean is non-causal (the engine uses b_id).
  3. One seed hides the counted-routes failure in §6.4.

  It should add, as general mechanism cases:
  - the spec's onset-lobe + 60-s low-pass shape (the design's 0.61–0.96 c);
  - a 120-s low-passed copy;
  - a 6-min/24-min switched copy;
  - u⁰ ≠ session mean;
  - the counted routes on ≥ 8 seeds.

  With these it would currently fail on the slow and switched copies (1.04–1.24 c) and on the counted routes.

### 6.6 Concrete failures, and whether a general fix exists

| # | Failure | Numbers | General (non-situation-specific) fix? |
|---|---|---|---|
| 1 | A1 assumes R ≤ R̄; this holds only for flat-gain delayed copies | R ≈ 2 on slow routes | partly: longer windows in the same c-scaled test |
| 2 | Slow routes (τ 120–300 s) | 1.04–1.24 c | yes, longer windows (needs a false-positive check) |
| 3 | Switched routes: release, then slow re-detection | 1.03–1.14 c | yes: a ratchet or a short-memory estimate (c-scaled) |
| 4 | Growing gain beats the 30-min memory | time-local 2–10 c; session metric ≤ 0.79 c | partly: multiple memories; no causal net bounds arbitrarily fast growth |
| 5 | Detection term linear in g/c | 1.3–1.8 c in 20-min sessions | no, beyond faster detection; state the bound per ≥ 1-h window |
| 6 | Proof constants: η up to 0.065; √q_cl; q_cl up to 9 % | stated bound ≈ 0.9–1.0 c, not ≤ 0.85 c | restate the bound |
| 7 | Governor false positive when u⁰ ≠ his session mean | 4.3 % of frames, a = 0.30 | yes: larger n_min or a zero-slope prior |
| 8 | Ledger stage binds on counted routes | up to 16.6 % (30 min), 5.8 % (1 h); 5/8 and 3/8 seeds over 1 % | open; not fixed by κ = 1.0 |
| 9 | Listed routes trimmed above 0.6 c; a caught copy is held at a steady 0.6 c | a 0.62–0.86 for ~30 min | yes, if r_L is separable: govern r − r_L only |

**Fit to implement:** yes, as an attenuate-only stage. It makes nothing worse, and F22's injected-copy test would lose its xfail. But Q35 should stay open on failures 2–4, 7 and 8, with fixes 2, 3 and 7 checked before day 1. §2.6's claims should be restated as "≤ about 0.9–1.0 c for flat-gain delayed copies in ≥ 1-h sessions", not as uniform in g/c.

---

## 7. Revision 2 (after the critique)

Written 2026-11-27, once, in answer to §6. The original design (§0–§5) and the critique (§6) stand as written above; this section replaces §1.3–§1.5, §2.3–§2.6 and §5 where it says so. Same rules: one rule for every channel, every output-side threshold a multiple of c_k, absolute quantities only on his signal or on time, attenuate-only, no situation named, nothing rewarded.

**Check:** `sims/scaled-safety-net/rev2_check.py` with the reference implementation `sims/scaled-safety-net/rev2_lib.py` (numpy only, plus the standard library's process pool; `python3 -I -B rev2_check.py > rev2_check.out.txt`, 12.0 min on 4 cores). Output in `sims/scaled-safety-net/rev2_check.out.txt`. It reuses check.py's partner recipe, metric and Ledger verbatim. **A check of the mathematics on synthetic signals, not evidence about people.** Every run uses an **engine-like neutral input** u⁰ = b_id: the 6-session exponential average of the same synthetic partner's earlier session means (as engine/config/innate.py's `cone_baseline_tau_sessions` = 6 makes it). This is not his session mean (|ū − b_id| up to 0.14 on these partners). Every route is causal (0 until it acts). The one exception, labelled where it appears, is F22's fixture as tests/test_ledger_injected.py builds it.

### 7.0 Result in one paragraph

Revision 2 keeps the multiplicative governor in front of the unchanged ledger and changes how it estimates and when it acts:
- **step and level keys:** the level keys are window means regressed with an intercept, as the metric's own block means are;
- **three memories** (30 min, 5 min, 1 min);
- **a ratchet:** a_k never rises within a session;
- **an evidence rule:** no pre-session history in the sums, a batch sandwich, an effective count of independent batches, and a Student-t test.

On the 8 synthetic partners of `test_counted_routes_untouched` (30 min and 1 h), on 8 held-out partners and on the critique's four K6 stress cases, all with b_id ≠ his mean, the governor engaged on **0.00 % of frames** (rev 1: up to 4.3 %).

Across 13 route shapes (the original scenarios and the critique's K1–K5), 4 ceilings (0.03–0.35) and g/c 1.5–33, the session residual is **0.28–0.95 c in 206 of 208 cells**. The exceptions are 1.06 c (off-grid copy, c 0.03, g/c 33) and 1.26 c (6 min on / 24 min off, c 0.35, g/c 10). The current ledger reaches 0.80–3.58 c on the same cells.

On F22's scenario, as the test builds it, the worst channel is 0.72 c (current 2.01 c). Built causally with b_id it is 1.26 c on one channel (BO, c 0.10, g/c 10), and 0.91 c or less elsewhere (current 3.62 c).

Every case above 1.0 c is the **detection span**: the governor now needs 70–220 s of his movement after a route starts, against 5–21 s in rev 1. That is the price of the evidence rule that removed the false engagement. A faster provisional rule was tried and brought the false engagement back (§7.6).

**Plainly:** revision 2 does not hold ≤ 1.0 c on every scenario. The best general bound is the steady part, measured at 0.45–0.95 c, plus a detection term (g/c)·Q_tr that no causal net with a non-zero false-engagement margin removes. Restated with honest constants, the proved bound is weak (§7.3).

The unchanged ledger's own F1 problem is **not** changed by the revision. A general fix exists for it: an evidence floor E0 on the ledger's E. It takes `test_counted_routes_untouched`'s recipe from 5/8 and 3/8 partners above 1 % to 0/8 at both durations. It changes the bit-identical ledger, so it is listed separately (§7.5).

### 7.1 What changed, and why (critique item → change)

| Critique (§6.6) | Change in revision 2 | General? |
|---|---|---|
| 1, 2: slow routes (τ 120–300 s), R ≈ 2 | **Level keys** beside the step keys: ū_W(t−L) and r̄_W(t), regressed **with an intercept** by West's exact incremental weighted covariance. There is no lagging centre, so the drift that made rev 1 drop centred means does not arise. Level keys see his slow movement as the metric's block means do. Measured R on the long-memory keys: 0.97–0.99 for the 120-s and 300-s low-passed copies (rev 1: ≈ 2). | one rule, every channel |
| 3: switched routes release and re-detect slowly | **Ratchet**: a_k(t) = min(a_k(t−1), target), so a caught route stays held for the session. **Short memories** (300 s, 60 s), whose latches combine with the 30-min one by max slope, so a re-start mid-session is seen within about a minute of evidence. | yes |
| 4: gain that grows during the session | The short memories plus the ratchet; a **running metric** (20-min windows from 10 min on) and the **effective gain a(t)g(t) at the end** are now reported (§7.4). | partly (§7.6) |
| 7: false engagement when u⁰ ≠ his mean | (a) A key counts frames only from t ≥ L + 2W, so the session-start step from u⁰ to his level never enters its sums. (b) The standard error is a **batch sandwich** over batches of 2W. The evidence is the **effective number of independent batches** n = (Σw_b E_b)² / Σw_b² E_b², so one large start step counts as one batch however large it is. (c) Engagement needs n ≥ 2 and β̂ − t_{n−1}·se > κ_g c_k, with t_{n−1} Student's multiplier at z = 3's level (one-sided p = 0.00135). Few batches therefore need a much larger margin (t ≈ 9 at n = 4, 4.3 at n = 11). | yes: statistical settings on his signal and on time |
| 6: proof constants | Theorem 1′ (§7.3): √q_cl; Λ on block means of \|r\| including the offset g(ū − u⁰); η = a_T t_n se/(z c), which can exceed 0.065; a transient term in place of g q_tr. | – |
| 8: the ledger's F1 | Unchanged by the revision; diagnosis and a general fix in §7.5. | yes (E0), separately |
| 9: listed routes trimmed above 0.6 c | Kept (κ_g c is the one target for all of r). With the ratchet the trim is deeper (§7.4 R4). Governing only r − r_L is not adopted: it would bound the remainder, not the total, so the total could reach the listed routes' 0.974 c plus 0.6 c. | – |

Kept from rev 1: κ_g = 0.60, z = 3 (now as a level), σ₀ = 0.01, lags 0–300 s, the 10-Hz rate, the ledger after the governor (unchanged, κ 0.70, 97 keys), and attenuate-only (|x₂| ≤ |r|, x₂ r ≥ 0).

### 7.2 The governor, revision 2 (replaces §1.3–§1.5)

Per channel k, at f_g = 10 Hz, with exponential window means ū_W of his counterpart (started at u⁰ = b_id) and r̄_W of the raw partner-caused part (started at 0):

- **Keys** (153 per channel × 3 memories = 459):

  | W | kind | lag grid | keys |
  |---|---|---|---|
  | 10 s | step: π = ū(t−L) − ū(t−L−W), ρ = r̄(t) − r̄(t−W) | 0–300 s by 5 s | 61 |
  | 10 s | level: π = ū(t−L), ρ = r̄(t) | 0–300 s by 5 s | 61 |
  | 60 s | level | 0–300 s by 10 s | 31 |

- **Memories** τ ∈ {1800, 300, 60} s, d = exp(−1/(τ f_g)). Per key and memory, on frames with t ≥ L + 2W only (weight v = 1, else 0):
  - W_t ← d W_t + v;
  - running means μ_π, μ_ρ updated by v/W_t;
  - C ← dC + v(π − μ_π^old)(ρ − μ_ρ^new), and E the same with π;
  - batch increments P_b, E_b summed over batches of B = 2W frames, then A₁₁ ← d^{2B}A₁₁ + P_b², A₁₂ ← d^{2B}A₁₂ + P_bE_b, A₂₂ ← d^{2B}A₂₂ + E_b², Ē ← d^B Ē + E_b.
- **Estimate:** β̂ = C / max(E, σ₀² W_t).
- **Evidence:** n = Ē² / A₂₂.
- **Standard error:** se² = (A₁₁ − 2β̂A₁₂ + β̂²A₂₂)/Ē² · n/(n−1).
- **Latch:** [n ≥ 2 and β̂ − t_{n−1}(z)·se > κ_g c_k] or [latched and β̂ > κ_g c_k]. t_{n−1}(z) is the Cornish–Fisher expansion of Student's quantile (Abramowitz–Stegun 26.7.5).
- **Gain:** target = κ_g c_k / max over latched keys and memories of β̂ (1 if none); **a_k(t) = min(a_k(t−1), target)**; x_k = a_k r_k. Everything resets at session start.

**Constants** (one rule for every channel; output-side thresholds ∝ c_k; the rest on his signal or on time):

| Name | Value | Unit | Scales with c_k | Category |
|---|---|---|---|---|
| `governor_kappa` | 0.60 | fraction of c_k | target = 0.60 c_k | ceiling |
| `governor_z` | 3.0 (one-sided p 0.00135) | – | no | ceiling (general statistical setting) |
| `governor_t_test` | on (Student multiplier at z's level, n − 1 df) | – | no | ceiling (general statistical setting) |
| `governor_n_req` | 2 | independent batches | no | ceiling (general statistical setting) |
| `governor_batch_W` | 2 | windows per batch | no | ceiling (general statistical setting) |
| `governor_start_W` | 2 | windows after the lag before a key counts | no | ceiling (general statistical setting) |
| `governor_sigma0` | 0.01 | his units | no (on the regressor) | ceiling |
| `governor_taus_s` | 1800, 300, 60 | s | no | ceiling |
| `governor_keys` | (10 s step, 5 s), (10 s level, 5 s), (60 s level, 10 s); lags 0–300 s | s | no | ceiling |
| `governor_ratchet` | on | – | no | ceiling |
| `governor_rate_hz` | 10 | Hz | no | generic (engineering) |
| `governor_frame_budget_ms` | 0.5 | ms | no | generic (engineering) |
| `ledger_evidence_floor` (§7.5, separate change) | 0.54 = 600 frames × 0.03² | his π² units | no (on his signal) | ceiling |

Lemma 0 (exact homogeneity in (c_k, r_k)) still holds. The new quantities (n, t, batches, start rule) depend on his signal and time only, and C, A₁₁, A₁₂ scale as before. Checked exactly at λ = 8: output and a differences 0 (R7).

Compute: 459 key-memories × 33 channels × about 40 flops × 10 Hz ≈ 6 Mflop/s; running sums ≈ 15 × 33 × 459 floats ≈ 1.8 MB; ring buffers as rev 1.

### 7.3 Theorem 1′ (replaces §2.3 and §2.6; honest constants)

**Setting.** Take a channel with c > 0 and the long-memory key family 𝒦_L (τ = 1800 s). Let B* be the largest β̂ over 𝒦_L at T.
- R := ρ*[r]/B* (the metric's worst slope on the raw part, against the governor's largest slope).
- Λ := max_b rms((|r|)_b)/(sd(u_b)·B*): block means of |r|, so the offset g(ū − u⁰) is included (critique, steps 3 and 5).
- a_T is the final gain.
- η := a_T · max t_{n−1} se/(z c) over keys of 𝒦_L with n ≥ 2 and β̂ ∈ (κ_g c, κ_g c + t_{n−1}se]. These are the keys the test may leave unlatched; the factor a_T was missing in rev 1's step 2.
- τ_s is the settle time, the first time a ≤ (1 + ε_a)a_T. a is non-increasing, so it stays within (1 + ε_a)a_T after τ_s.
- q_cl is the share of his block variance in blocks where the ledger stage changes frames after τ_s.
- The transient term is Q := Σ_i a_i √(Σ_{b∈S_i} r_b²) √(Σ_{b∈S_i} (u_b − ū)²) / S, over the spans S_i from the route's onset to τ_s in which a stays above half its value a_i at the span's start. For a copy, r_b = g(u_b − u⁰), so Q = g·Q_tr.

Then

  **ρ*[x₂] ≤ c (κ_g + zη) [ R + Λ (ε_a + √q_cl (1 + ε_a)) ] + Q.**

*Proof sketch, with the critique's corrections.*
1. The metric is linear: ρ*[a_T r] = a_T R B*.
2. A latched key of 𝒦_L gives a_T β̂ ≤ κ_g c (ratchet: a_T ≤ every past target). An unlatched key with evidence has β̂ ≤ κ_g c + t se, so a_T B* ≤ c(κ_g + zη). Keys of 𝒦_L without evidence at T are excluded: in 1-h sessions every long-memory key has n ≥ 2 well before T. This is an assumption to check, not a theorem.
3. After τ_s, a = a_T + δ with 0 ≤ δ ≤ ε_a a_T. Cauchy–Schwarz on the block means of δ|r| (not δ r_b) gives ≤ ε_a a_T Λ B*.
4. The ledger stage removes v with |v| ≤ |x| on the blocks counted in q_cl. Cauchy–Schwarz restricted to them gives the factor **√q_cl**, not q_cl.
5. Before τ_s, each span contributes at most a_i √(Σr_b²) √(Σ(u_b − ū)²)/S by Cauchy–Schwarz restricted to the span.
6. Sum the parts. ∎

**Measured constants** (R2, max over engaged cells per shape; full table in rev2_check.out.txt):
- R = 0.73–1.23. A1, R ≤ R̄, is still an assumption, but the level keys bring R to ≈ 1 on the slow shapes too: 0.97 and 0.99 on the 120-s and 300-s low-passed copies.
- Λ = 1.3–3.5.
- η = 0.04–0.43, and 3.3 on the θ = 300 s growth route.
- q_cl ≤ 0.083; ε_a = 0.10 by the choice of τ_s.

The steady-state term evaluates to **0.89–2.02 c** (8.6 c on the θ = 300 s growth route), and the transient term g·Q_tr to 1.3–28 c. The whole bound held in every engaged cell (bound ≥ measured in 194/194), but it is **loose by a factor 2–30 against the measured 0.45–1.26 c**. Rev 1's "≤ 0.85 c independent of c and g/c" is withdrawn. With honest constants the theorem gives an O(1)·c steady bound uniform in g/c for long sessions, about 1–2 c with the measured Λ and η, plus a transient term linear in g/c. That term shrinks with the session length and with faster detection. The ≤ 1.0 c figures are measured, not proved.

**Where the theorem stops:**
- **Nonlinear routes with memory** (D93, O1): nothing bounds R a priori. A route whose slope depends on his history in a way no fixed per-key regression tracks can have R ≫ 1. This is not closed.
- **A partner who mirrors the agent:** the theorem and the metric treat his signal as exogenous. If he copies the agent's rendered face, his u contains a delayed, scaled copy of the agent's own output. The governor then regresses r on a signal that partly contains r: a closed loop. Its estimate mixes the route's gain with the loop's. Because a ≤ 1, the governor can only lower the loop gain, and once latched the loop gain is at most about h·0.6 c/ψ. Whether it latches on the counted routes alone against a strong mirror, and so cuts permitted fast mimicry for the rest of the session under the ratchet, is **not simulated**. It is the first thing to check with recorded dyads (M4).
- **Cross-channel routes** (D93 Theorem 2's weighted term), **delays > 300 s**, and **sessions < ~15 min** (the long-memory keys may still lack evidence there) are outside it, as in rev 1.

### 7.4 Results (rev2_check.out.txt; residual / c_k; engine-like u⁰ = b_id unless stated)

**Worst session residual per ceiling per scenario** (worst over g/c 1.5, 3, 10, 33; one partner per cell, so cells are noisy). "Running" is the worst 20-min window from 10 min on. "Eff. gain" is the largest a(t)g(t) over the last 30 min.

| Scenario | Current ledger, worst | **Rev 2, c = 0.03** | **0.05** | **0.10** | **0.35** | Running 20-min, worst | Eff. gain at end |
|---|---|---|---|---|---|---|---|
| copy, delay 90 s (on grid) | 2.77 | 0.61 | 0.65 | 0.65 | 0.68 | 0.75 | |
| copy, 47.35 s (off grid) | 2.16 | **1.06** | 0.57 | 0.75 | 0.64 | 0.66 | |
| copy, 213.7 s (off grid) | 2.01 | 0.65 | 0.87 | 0.64 | 0.55 | 0.64 | |
| copy low-passed 30 s, 120 s | 1.64 | 0.67 | 0.67 | 0.62 | 0.84 | 0.74 | |
| spec F22 shape (onset lobe + 60-s lp), 120 s | 1.38 | 0.81 | 0.63 | 0.71 | 0.68 | 0.79 | |
| K3: copy low-passed 120 s | 1.88 | 0.78 | 0.95 | 0.72 | 0.71 | **1.12** | |
| K3: copy low-passed 300 s | 2.21 | 0.90 | 0.65 | 0.78 | 0.89 | **1.70** | |
| K4: fast echo (2-s high-pass), 30 s | 3.58 | 0.67 | 0.80 | 0.70 | 0.71 | 0.84 | |
| K5: on 10 s / off 50 s | 1.85 | 0.94 | 0.57 | 0.58 | 0.87 | **1.15** | |
| K5: on 6 min / off 24 min | 1.90 | 0.54 | 0.54 | 0.45 | **1.26** | **3.69** | |
| K2: gain ramps 0 → g over the hour | 2.04 | 0.61 | 0.65 | 0.67 | 0.66 | 0.96 | 0.70 c |
| K2: gain grows exp., θ 600 s | 1.32 | 0.64 | 0.55 | 0.50 | 0.56 | 0.89 | **1.04 c** |
| K2: gain grows exp., θ 300 s | 0.80 | 0.28 | 0.45 | 0.35 | 0.33 | **1.08** | **1.50 c** |

In rev 1 (critique K1–K5, c = 0.05) these were 1.24, 1.20, 1.03 and 1.14 c on the slow and switched routes, with effective gains of 2–10 c at the end on the growth routes. In rev 2, 206 of 208 session cells are ≤ 0.95 c. The detection-time column per cell is in the output: 70–220 s after onset for most routes, longer for weak or slow routes, which leave less to catch.

**F22's scenario** (gain-1 copy on all 33 channels, delays 10–300 s by channel; worst per ceiling):

| Construction | c 0.03 | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.35 | Worst (current ledger) |
|---|---|---|---|---|---|---|---|---|---|
| as tests/ builds it (padded, minus session mean; u⁰ = session mean) | 0.56 | 0.70 | 0.72 | 0.27 | 0.51 | 0.52 | 0.60 | 0.50 | **0.72** (2.01) |
| causal, u⁰ = b_id (engine-like) | 0.51 | 0.91 | **1.26** (BO) | 0.54 | 0.52 | 0.52 | 0.58 | 0.50 | **1.26** (3.62) |

- In the causal row, BO's 1.26 c comes from its first 4 minutes. The route starts at 150 s and is detected 89 s later, while he moves a lot (300-s mood blocks). From 10 min on, the worst channel reads 0.67 c.
- Zero-ceiling channels: ≤ 0.017. Attenuate-only on every frame.

**Copies near the target on top of the counted routes** (R3, seed 8, b_id), worst over all 20 capped channels: copy g/c 0.8 → 0.72 c, 1.2 → 0.73 c, 2 → 0.67 c, 5 → 0.90 c (JO, c 0.10).

**Counted routes running high** (R4, an extreme but legal partner): counted slope 0.70–0.99 c is trimmed to 0.52–0.61 c on every ceiling, with a < 1 on 89–98 % of frames and final a 0.46–0.85. Because of the ratchet the trim is deeper than rev 1's (0.62–0.86). At 0.50 c nothing is touched.

**False engagement** (counted routes only: fast gear 0.45 s and the held 2-min route at 0.22 c_k, both relative to b_id; governor a < 1, worst channel):

| Partners | Governor a < 1 | Ledger stage changed (unchanged ledger) | With ledger floor E0 |
|---|---|---|---|
| seeds 7–14, 1 h | **0.00 %** on all 8 | 0.00–8.39 %; 5 of 8 above 1 % | 0.00 % on all 8 |
| seeds 7–14, 30 min | **0.00 %** on all 8 | 0.09–16.91 %; 6 of 8 above 1 % | 0.00 % on 6; 0.97 % (seed 10); **4.61 %** (seed 13) |
| held-out seeds 15–22, 1 h | **0.00 %** on all 8 | 0.00–8.75 %; 6 of 8 above 1 % | 0.00 % on all 8 |
| critique K6 (seed 8, livelier seed 10; u⁰ = mean ∓ 0.10) | **0.00 %** on all 4 (rev 1: 4.3 %, a 0.30) | 2.23–8.35 % | – |

Counted-route slopes on these partners are 0.33–0.51 c, below the 0.60 c target. The engagement test now needs both that margin and enough independent evidence.

**Ledger floor E0 on the residuals:** governor plus ledger with E0 changes the R2 worst values by at most 0.01 c (the "with E0" column of R2). On F22 as built the worst is 0.73 c, causal with b_id 1.26 c. The ledger stage matters only in the detection span, and there E0 costs no measurable residual.

### 7.5 The unchanged ledger's F1 problem

Rebuilt exactly as `test_counted_routes_untouched` builds it (u⁰ = session mean, onset filter from 0), seeds 7–14, the worst capped channel's frames changed by the 97-key ledger at κ 0.70 alone (R6):
- 30 min: 0.07, 0.07, **16.57, 10.76, 6.87, 1.40, 2.56**, 0.09 %. Five of 8 are above 1 %.
- 1 h: 0.00, **3.21**, 0.09, **5.75**, 0.17, 0.04, **1.06**, 0.21 %. Three of 8 are above 1 %.

These reproduce the critique's K7 exactly. With b_id they are similar or worse (table above).

**The revision does not change it.** On these partners the governor never engages (a ≡ 1), so the ledger sees exactly the raw r it sees today.

**Diagnosis.** A development run with the same recipe (not in rev2_check.py) split the changed frames by time. Almost all of them fall in the **first 5 minutes**: seed 9 at 30 min, 16.04 of 16.57 %; seed 10 at 1 h, 5.67 of 5.75 %; seeds 11–13 at 30 min and seeds 8 and 13 at 1 h, all of it. The one partial exception is seed 10 at 30 min, 5.32 of 10.76 %. Early in a session the ledger's E is near zero (it starts at 10⁻⁹). Its bound κc_k E − S is then a ratio of tiny sums, and an ordinary burst on a channel with fast gain 0.8 c_k (HP, F0, LAT, PAU, TILT, YAW, VG, RT) breaks it. Raising κ to 1.0 does not fix this (§3.1, §6.4), because the trouble is the missing evidence, not the target.

**General fix: an evidence floor on the ledger,** b = κ c_k (E + E₀) − S, with E₀ = 0.54. That is one minute (600 frames) of his window-mean movement at the metric's own floor of 0.03, the same for every channel.
- It is on his signal (the regressor), so Lemma 0 still holds. It lets the ledger allow at most κ c_k E₀ of extra early covariance, which is proportional to c_k.
- Measured on the test's recipe, 30 min and 1 h: **0.00 % on all 8 partners** (0/8 above 1 %, against 5/8 and 3/8).
- With b_id it is 0.00 % on 22 of 24 partner-sessions. The exceptions are 0.97 % (seed 10) and **4.61 %** (seed 13, both 30 min). Seed 13 has the largest |ū − b_id| of all, 0.14. So in short sessions with a baseline far from today's level, the ledger can still exceed F1. The governor does not.
- It costs at most 0.01 c of residual when the governor is in front (§7.4).

It **changes the bit-identical ledger**: the regression test must allow E₀ as a parameter, with E₀ = 0 reproducing today's output bit for bit. For that reason it is listed as a separate build item. Without it, the net as built fails F1 and F22's counted-routes clause on most synthetic partners, as the critique said.

### 7.6 What remains, stated plainly

- **Detection span (critique items 5 and 7; the reason for every residual above 1.0 c).**
  - What it costs: requiring independent evidence before acting moved detection from 5–21 s (rev 1) to 70–220 s after a route starts. Until then the route runs at the ledger's leaky level. Hence F22-causal BO 1.26 c, the off-grid cell at g/c 33 (1.06 c), the 6/24 switched route at g/c 10 (1.26 c in the session, 3.69 c in the 20-min window that holds its first on-period), and the running-window excesses on the slow routes (1.12, 1.70 c).
  - What was tried: a **provisional, non-ratcheted gain** from keys with ≥ 1–1.5 batches whose plain z lower bound exceeds the target. In development runs (not in rev2_check.py) it cut detection to 6–85 s. It also engaged on natural partners on 0.1–0.7 % of frames in 1-h sessions and up to 3.7–5.7 % in 30-min ones, so it is not adopted.
  - **There is no general fix inside a causal net that keeps the false-engagement margin.** The best general bound is the steady term plus (g/c)·Q_tr, where Q_tr is his movement share in the 70–220 s detection span (§7.3). The guarantee should be read per ≥ 1-h session, and the F1 live monitor's window chosen to match.
- **Growth during the session (critique item 4).** The effective gain at the end is 0.70 c for a linear ramp, **1.04 c for exponential growth with e-folding 600 s and 1.50 c with 300 s** (rev 1: 2–10 c). The session metric reads ≤ 0.64 c and the 20-min running metric ≤ 1.08 c. The shortest memory that clears the t test (60 s, about 6 batches, t ≈ 5.6) sets the lag. A gain growing faster than that is followed at about κ_g c·(1 + lag/θ) or worse. **No causal estimator bounds arbitrarily fast growth.** A step increase in gain is the detection-span case above.
- **Nonlinear routes with memory** (D93) and a **partner mirroring the agent**: not covered and not simulated (§7.3).
- **Listed routes above 0.6 c** are trimmed for the rest of the session (ratchet) on an extreme partner. That is the price of one target for all of r.

### 7.7 What the build would implement (replaces §5)

**`engine/shadow/governor.py` (new).**
- `class Governor(ceilings, fs, u_neutral, cfg=GOVERNOR)`, vectorised over (channels, keys) per key set and memory, matching `Governor2` in `sims/scaled-safety-net/rev2_lib.py`:
  - `reset(u_neutral)`: ring buffers of ū_W at b_id, of r̄_W at 0, all sums 0, a = 1;
  - `step(u, r) -> x`, returning a ⊙ r;
  - exposed `a`, `latched_key()`, `beta`, `se`, `neff` for logging and asserts.
- Helpers: `t_multiplier(z, df)` (the Cornish–Fisher expansion) and `_update_set(...)` (West's incremental covariance, batch sums, evidence, latch).
- At 30 Hz: window means at 30 Hz; sums, batches and gain at 10 Hz (every third frame); a held between updates. Lags, batches and the start rule are in seconds, so they are rate-independent.

**`engine/shadow/shadow.py`** (frame step, beside `self.ledger`): r = y − ȳ; `x = self.governor.step(fr.u, r)`; `x2 = self.ledger.step(fr.u, x)`; rendered ȳ + x2. Construct with `u_neutral = self.b_id[:N]`, the shadow's own input, never the session mean. Per-minute logging adds min a_k, the binding key and memory, β̂, se and n.

**`engine/shadow/ledger.py`:** the algorithm is unchanged. **Separate item:** add the `evidence_floor` parameter E₀ (default 0.54 once accepted; E₀ = 0 is bit-identical to today). Its docstring's input becomes "the governor's output".

**`engine/config/innate.py`:** the constants of §7.2's table: `governor_kappa`, `governor_z`, `governor_t_test`, `governor_n_req`, `governor_batch_W`, `governor_start_W`, `governor_sigma0`, `governor_taus_s`, `governor_keys`, `governor_ratchet` (category **ceiling**), `governor_rate_hz` and `governor_frame_budget_ms` (category **generic**), and `ledger_evidence_floor` (category **ceiling**, separate item). Regenerate `INNATE.lock` and `innate_names.txt` by the usual procedure. None names a situation, partner, channel, event or time of day.

**`engine/invariants/asserts.py`:** **A4g** per frame:
- 0 ≤ a_k ≤ 1;
- a_k(t) ≤ a_k(t−1) within a session (ratchet);
- x_k = a_k r_k exactly;
- a_k = 1 until some key has latched;
- on zero-ceiling channels a_k ∈ {0, 1}.

Failure handling is as A4: the channel renders ȳ_k. A3 and A4 apply to the ledger stage with its input x.

**Tests.**
- **`tests/test_ledger_injected.py` (F22's mechanism test):**
  - The fixture runs `Governor` → `Ledger`.
  - `test_copy_held_below_ceiling_on_capped_channels` **loses its xfail**: 0.72 c on its own seed and construction (current 2.01 c).
  - New `test_copy_causal_engine_baseline`: the same copies built causally with u_neutral = an engine-like b_id. It asserts ≤ 1.0 c read from 10 min on (measured 0.67 c). The whole-session ≤ 1.0 c is an **expected failure** (BO 1.26 c, the detection span, §7.6), so the limit stays visible.
  - New `test_mechanism_shapes`: at c = 0.05 and g/c 3 and 33, the spec's onset-lobe shape, a 120-s low-passed copy, a 10-s/50-s switched copy and the fast echo, each ≤ 1.0 c (measured ≤ 0.95 c). The 6/24 switched copy at g/c 10 is an expected failure (1.26 c).
  - `test_counted_routes_untouched`: seeds 7–14, 30 min, with b_id. It asserts a_k ≡ 1. It asserts ledger frames changed ≤ 1 % only with E₀ (otherwise it stays as today, seed 7 only, with a comment pointing to §7.5).
- **New `tests/test_governor.py`:**
  - Lemma 0: scale c and r by 8, a identical, output × 8, exactly.
  - Attenuate-only, x = a r, and the ratchet monotone, on every frame.
  - No sums before t = L + 2W.
  - One start step counts as one batch.
  - The t multiplier against tabulated quantiles (df 3, 10, 30).
  - Zero-ceiling behaviour.
  - Natural partners: a ≡ 1 on seeds 7–14 and on u⁰ = mean ∓ 0.10.
  - Counted routes at s = 0.85 c trimmed to ≤ 0.65 c.
  - Bit-for-bit regression against `rev2_lib.Governor2` at 10 Hz.
- **`tests/test_ledger_regression.py`:** unchanged (E₀ = 0 path), plus one case with E₀ = 0.54 if the separate item is accepted.

**Elsewhere, not edited here:**
- research/build/spec.md §1.6 (the governor before the ledger; A4g) and §5.1's F22 row and synthetic-construction note (causal, b_id).
- `eval/f22_delayed_copy.py`: governor before ledger in the ledger-only re-run; F22 judged on ≥ 1-h sessions.
- design-cayley-ledger.md's Build core summary.
- DECISIONS.md (a D-entry) and questions.md Q35.

### 7.8 Status and readiness

**Ready to implement as an attenuate-only stage in front of the ledger**, with the separate ledger evidence floor recommended:
- It makes nothing worse on any case checked.
- It holds 206 of 208 scenario cells and every F22 channel as tests/ builds it at ≤ 0.95 c.
- It removes the false engagement on all 20 partner-sessions and stress cases checked.

**Not a closed guarantee:**
- detection-span excesses up to 1.26 c in 1-h sessions with b_id, and more in 20-min windows;
- growth faster than about 10 min of e-folding reaches 1.0–1.5 c by the end;
- the theorem's honest constants give about 1–2 c plus a transient term, not ≤ 1.0 c;
- nonlinear routes with memory and a mirroring partner remain open.

**Q35/D98 should stay open on these points.** If the operator wants every scenario at ≤ 1.0 c, the remaining lever is faster detection. The check shows that buys false engagement on ordinary partners (§7.6), so it is the operator's trade-off, not a free setting.
