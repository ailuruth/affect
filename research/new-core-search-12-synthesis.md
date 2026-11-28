# Searching for a new core mechanism, twelfth pass: how fast can the safety net catch a copy without switching on for ordinary partners? (synthesis, 2026-11-28)

## In plain terms

- **The question.** Revision 2 of the scaled safety net (research/foundations/design-scaled-safety-net.md §7) holds copies of the operator's face below each expression's limit in 206 of 208 tested cases and never switches on by mistake, but it needs 70–220 s to catch a copy. In that time a copy that is switched on and off (6 min on, 24 off) reaches 1.26 times the limit, and a fast copy on the smallest limit 1.06 times. The design said the only lever left is faster detection, bought with false alarms on ordinary partners. This pass asks what the mathematics of change detection says that trade-off is at best.
- **The answer has three parts.**
  1. **The limit is not information.** For a copy strong enough to matter, one 20-second batch of the governor's own statistic carries enough evidence. Any detector at a given false-alarm rate needs delay ≥ log(time between false alarms) / (evidence per second) (Lorden 1971; Lai 1998). For a copy at 3 times the limit or more, that is one batch, about 30 s with the window. Revision 2 waits 80–120 s because its test estimates its own noise from the same few batches, and a copy whose delay falls between its lag steps makes that noise estimate grow with the copy. Its delay therefore does not shrink as the copy grows.
  2. **A standard detector on the same statistic is 5–8 times faster at the same zero false engagement.** A CUSUM (Page's cumulative sum, the optimal rule for this criterion) has its noise scale fixed on ordinary partners. On revision 2's own test cells it catches copies in a median 10–20 s instead of 80–120 s, and the switched copy drops from 1.26 to 0.36 of the limit. It is worse on very slow copies, so it must run beside revision 2, not replace it.
  3. **A check with zero false alarms by construction does more than any statistical test.** The listed routes have known maximum gains, so the most the partner can legitimately cause on a channel at any moment is known exactly. When the partner-caused part exceeds that, a route nobody listed must be acting. Cutting the gain at once removes the dependence on the copy's strength. On the checked cells, revision 2 plus this envelope has no cell above the limit (worst 0.95); adding the CUSUM brings the worst 20-minute window on plain copies to 0.76–0.84.
- **What no detector can do.** Three things are out of reach of detection:
  - copies whose effect sits at periods of several minutes, judged over 20-minute windows (still up to 1.3–3.9 times the limit);
  - growth faster than the detector's memory;
  - the windowed metric's own over-reading, which goes beyond a route's gain (pass 10's Observation 4).

  A route that switches itself to evade can do no better on average than about 0.67–0.75 of the limit: it can hide only by staying weak.
- **Not a new core.** These are known statistics (CUSUM, the boundary design, an envelope check) applied as components.
- **For the operator (Q35).** The three existing options stand. The pass adds one possible fourth line: add the envelope (and optionally the CUSUM) to revision 2 before day 1, as a third revision that needs its own independent check.

## Scope of this pass

Q35 (research/questions.md), D98 and D99 leave the scaled safety net at revision 2:
- 206 of 208 cells at ≤ 0.95 c_k, with 0 % false engagement on 20 partner-sessions and stress cases;
- detection 70–220 s after a route starts;
- a proved bound of about 1–2 c plus a transient term (g/c)·Q_tr;
- §7.6 and §7.8: "the remaining lever is faster detection", which buys false engagement on ordinary partners.

Pass 10 (new-core-search-10-synthesis.md) showed that by-construction gain bounds do not reach the pathwise reading of the metric; only output-side attenuation does. This pass reads the mathematics of sequential (quickest) change detection and asks:
- what the best achievable trade-off between detection delay and false engagement is, per channel;
- whether any known procedure beats revision 2's window-mean keys, with their 30/5/1-min memories and ratchet, at equal false engagement;
- what an adaptive, switching route can do against any detector.

Read in the repo: brief.md (Principles), questions.md Q35, design-scaled-safety-net.md in full (§0–§7.8) with its sims (check.py, critique_check.py, rev2_lib.py, rev2_check.py and outputs), new-core-search-10-synthesis.md, conjecture-five-passes.md (§0–§1 and the statement of O1), and design-cayley-ledger.md's shadow-ledger parts (§2.13, the counted routes' sup-gain total 0.974 c_k, rule 10). The partner-caused part r_k is the factual output minus the shadow's, where the shadow is the same agent fed the neutral face u⁰ = b_id with his words kept. The "slope" is the regression of r_k's window means on his same-channel window means at a lag.

**Vocabulary.** No emotion labels or named emotion variables appear below Claude. Channels are the build core's codes (LP lip pull, LD lid droop, BO outer brow, …). c_k is channel k's ceiling, κ_g = 0.60 the governor's target, s a copy's slope in units of c_k (s = g/c for a plain delayed copy of gain g).

## Sources (notes in research/)

| Note | What | How fully read |
|---|---|---|
| veeravalli-banerjee-2014-quickest-change-detection.md | survey chapter: Bayesian and minimax theory, CUSUM optimality, Lai's non-i.i.d. bound, GLR, window-limited GLR | **in full** (arXiv v1) |
| xie-zou-xie-veeravalli-2021-sequential-change-detection-survey.md | survey: classical results, non-i.i.d., transient and nuisance changes, robust and adversarial detection | §I–IV in full; §V–VI skimmed |
| sokolov-spivak-tartakovsky-2023-intermittent-change.md | detecting a change that ends; local false-alarm probability; ML derivation of CUSUM, window-limited CUSUM, FMA | §1–3 in full; §4 Lemmas 1–2; §5 tables; CUSUM integral equations skimmed |
| mei-2006-change-detection-composite-prechange.md | change detection when "in control" means a parameter below a limit | §1–2 to Theorem 2.2; §3–5 not read |

**Not reachable from here, so not read** (projecteuclid.org, jstor.org, academic.oup.com and ieeexplore.ieee.org are refused by this session's network proxy):
- Page 1954, "Continuous inspection schemes" (Biometrika 41);
- Lorden 1971 (Ann. Math. Statist. 42);
- Moustakides 1986 (Ann. Statist. 14);
- Lai 1998 (IEEE Trans. Inf. Theory 44);
- Siegmund & Venkatraman 1995.

Their results are used **only as the two surveys restate them** (Veeravalli & Banerjee, Theorems 4.2–4.3, Corollary 3, §VI-A; Xie et al., Theorem 1 and §III-A), and Mei 2006 restates Lorden's bound (his eq. 1.2) and Lemma 2.1. Moustakides & Veeravalli on transitory changes (2016) has no open copy; Sokolov et al. stand in for transient changes.

**Check.** `research/foundations/sims/new-core-search-12/check.py` (numpy only; `python3 -I -B check.py > out.txt`, about 8 min on 4 cores; output in `out.txt`). It reuses revision 2's reference implementation read-only (rev2_lib.py: partners, b_id, counted routes, Governor2, Ledger, metric) on the same partners and cells as rev2_check.py's R2. **It checks algebra on synthetic signals. It is not evidence about people, behaviour or the engine.**

## What this pass adds (in short)

1. **The frontier in the governor's units** (§2, table): delay ≥ τ_b · log(γ_b K) / I_b(s), with I_b(s) = (s − κ_g)²/(2η_b²) per batch of τ_b = 2W, η_b = 0.16–0.30 on channels with a fast gain of at least 0.4 c_k and 0.03–0.08 on the others (measured), plus a structural floor of about W + τ_b ≈ 30 s for 10-s window means.
2. **Diagnosis of revision 2's delay** (Proposition 2): a self-normalised Student test with few batches has a detection time that does not shrink with the copy's gain. A likelihood (CUSUM) test whose noise scale is fixed on ordinary partners crosses in one batch for large copies.
3. **CUSUM on the same statistic, at equal (zero) false engagement** (check B, D): detection medians drop from 80–120 s to 10–20 s on plain, off-grid and switched copies. Worse on slow copies, so it is a companion to revision 2.
4. **An envelope stage with zero false engagement by construction** (Proposition 3, check C, D): it removes the g/c dependence of the transient term, which becomes Γ_k/c_k · Q_tr with Γ_k ≤ 1.82 c_k. Revision 2 + envelope: 0 of 96 cells above 1.0 c (revision 2 alone: 2 of 96).
5. **The evasion floor** (Proposition 4): no detector at false-alarm level α can be guaranteed to keep a switching route's slope below about κ_g + η_b √(2 τ_b log(1/α) / T_w), which is 0.67–0.75 c for 1-h and 20-min windows. Bursts at gains above the envelope cannot evade it at all.
6. **What stays out of reach** (§5): slow routes and growth judged over 20-min windows, and the windowed metric's own inflation above a route's gain (check F: up to 1.9 g).

---

## 1. The governor as a change detector

Per channel k and key κ = (W, kind, L), revision 2 regresses window means of the raw partner-caused part r_k on his window means at lag L. Cut its frames into batches of τ_b = 2W (20 s at W = 10 s, 120 s at W = 60 s). Per batch, let b_b be the batch slope in units of c_k. Then:
- **pre-change (ordinary partner, listed routes only):** b_b = s_L + noise, with s_L ≤ κ_g (measured 0.33–0.51 on these partners; the listed routes' sup total is ≤ 0.974, so an extreme legal partner can exceed κ_g, and the design already accepts that as a trim);
- **post-change (an unlisted route of slope s starts at an unknown time):** b_b = s_L + ψ s + noise, with ψ ≤ 1 the fidelity of the best key to the route's shape and lag (≈ 1 on the grid; ≈ 0.9 off it).

This is a change in the slope of a regression at an unknown time, with:
- an unknown post-change slope and lag (composite post-change: GLR over keys);
- a composite pre-change (any slope up to κ_g: Mei's formulation);
- dependent, heavy-tailed noise.

**Measured inputs (check A; ordinary partners, counted routes, u⁰ = b_id, 8 partners × 1 h):**
- η_b (SD of the batch slope residual, units of c_k), W = 10 s level keys: median 0.23–0.25 across lags. By channel: LP 0.21, CR 0.16, BU_L 0.26, RHY 0.21, BRE 0.28, HP 0.24, VG 0.28, YAW 0.28, TILT 0.29, HG 0.25, F0 0.29, FR 0.28, EN 0.30, RT 0.25, PAU 0.28, LAT 0.25; the low-fast-gain channels BI 0.03, BO 0.08, LD 0.07, JO 0.08. Step keys: 0.29 median. W = 60 s level keys (τ_b = 120 s): 0.06–0.08 median, up to 0.19.
- **Dependence across batches is small:** the lag-1 correlation of batch residuals has median +0.01 to +0.03 on level keys, +0.08 to +0.15 on step keys and −0.19 to +0.03 at W = 60 s. So batches of 2W are close to independent samples, which supports revision 2's m_W = 2W.
- **Heavy tails:** the median kurtosis is 10–12 at W = 10 s (up to 109) and about 5 at W = 60 s; the Gaussian value is 3. The fast gear's bursts make the statistic far from Gaussian, so Gaussian thresholds are optimistic (§3).

## 2. The frontier (Proposition 1)

**Proposition 1 (lower bound; Lorden 1971, Lai 1998, as restated by Veeravalli & Banerjee Thm 4.3 and Xie et al. Thm 1; the translation is mine).** Let τ be any stopping rule on the governor's data, causal and per channel, whose mean time to false engagement on ordinary partners is at least γ batches. Suppose the per-batch log-likelihood ratio of "slope s" against "slope at the boundary κ_g" has a long-run mean I_b(s) after the change. Then Lorden's worst-case delay satisfies

  WADD(τ) ≥ τ_b · log γ / I_b(s) · (1 + o(1)),

and the CUSUM (Page) attains it: exactly for i.i.d. data (Moustakides 1986), asymptotically for dependent data (Lai 1998). Not knowing s and the lag costs nothing at first order: GLR and window-limited GLR attain the same rate, and the search over K keys enters the threshold as log(γK) at second order.

**In the governor's units (my derivation, Gaussian batch model).**
- I_b(s) = (s − κ_g)²/(2η_b²) nats per batch.
- "False engagement once per N channel-hours" means γ_b = 3600 N / τ_b. For the whole face (20 capped channels), once per M face-hours means N = 20 M.
- The structural floor of window means is one window plus one batch, ≈ W + τ_b = 30 s at W = 10 s.

So d*(s) ≈ max(1, log(γ_b K)/I_b(s)) · τ_b + W, with K = 153 keys.

**What delay would keep the copy at or below 1.0 c?** The steady part is ≈ 0.60–0.65 c. During the span the copy acts at full slope s, and if his movement is spread evenly it adds ≈ s · d/T_w (the transient term of Theorem 1′ with Q_tr ≈ d/T_w). So d_max(s) ≈ 0.35 T_w / s.

**Table 1. The frontier (delay in seconds after a route starts; Gaussian model; W = 10 s keys).**

| copy slope s (× c_k) | 1.0 | 1.5 | 3 | 10 | 33 |
|---|---|---|---|---|---|
| **lower bound, η_b = 0.30** (noisiest channels), false engagement once per 10 / 100 / 1000 channel-h | 292 / 344 / 395 | 66 / 76 / 86 | 30 | 30 | 30 |
| **lower bound, η_b = 0.08** (BI, BO, LD, JO) | 30 / 34 / 37 | 30 | 30 | 30 | 30 |
| delay that keeps the session ≤ 1.0 c, 1-h window | 1260 | 840 | 420 | 126 | 38 |
| same, 20-min window | 420 | 280 | 140 | 42 | 13 |
| **revision 2, measured** (median over cells with g/c ≥ 3) | – | – | 80–120 (plain, off-grid, switched); 425–728 (slow) | | |
| **CUSUM bank, measured** (same cells, same zero false engagement) | – | – | 10–20 (plain, off-grid, switched); 330–1170 (slow) | | |

**How to read it.** "False engagement once per N hours of ordinary partner costs at least D seconds of delay for a copy of slope s":
- **once per 100 channel-hours (once per 5 face-hours) costs at least 76 s for s = 1.5 and 344 s for s = 1.0 on the noisiest channels;** each tenfold reduction in false engagement adds only log 10 / I_b (≈ 10 s at s = 1.5, ≈ 50 s at s = 1.0);
- for every s ≥ 3 the bound sits at the structural floor of about 30 s at any reasonable false-engagement rate. Information is not the limit there; the window length is;
- copies with s ≤ 1.5 are slow to detect but cheap to miss: their transient term is ≤ 1.5 · 86/3600 ≈ 0.04 c per hour.

**Consequences (my derivation).**
- (i) In 1-h windows the frontier is inside d_max for every s up to about 33. Revision 2's 70–220 s is not forced by information: it is 3–7 times the floor for large copies, and the two failing cells (1.06 c, 1.26 c) lie in the region a frontier detector holds.
- (ii) In 20-min windows, **no detector on 10-s window means can hold s ≳ 14** (floor 30 s > 0.35 · 1200/s). Shorter windows lower the floor, but revision 1 found that 2-s windows engage on 6–21 % of ordinary frames. Proposition 3 is the way past this.
- (iii) **Slow routes** (2–5 min low-passed) put their evidence at long periods, where the number of independent samples is T_w/(2τ_f): about 12 per hour for τ_f = 300 s. Their delay is then of order 2τ_f·log(γK)/I, i.e. many minutes, and no detector shortens it, because his slow movement supplies only that many independent looks.
- (iv) **Growth.** For a slope growing as s(t) = s₀e^{t/θ}, the accumulated information reaches log γ when s ≈ κ_g + η_b √(4τ_b log γ / θ); for θ = 300 s, η_b = 0.3 that is ≈ 1.2. After detection a tracking estimator lags by ℓ ≥ τ_b, so the held gain is ≈ κ_g e^{ℓ/θ}: 0.69 c at ℓ = 40 s, θ = 300 s, and 1.17 c at θ = 60 s. That matches the critique's "no causal estimator bounds arbitrarily fast growth" with a number.

## 3. Why revision 2 is slow, and the CUSUM bank (Proposition 2, check B and D)

**Proposition 2 (my derivation).** Revision 2 engages a key when β̂ − t_{n−1}(z)·se > κ_g c.
- Its se is a sandwich estimate from the same n batches.
- t_{n−1}(z = 3) is ≈ 96 at n = 2, 9.0 at n = 4 and 5.6 at n ≈ 6 (Cornish–Fisher, as rev2_lib).

For a route the key fits only partly (lag between grid points, or a shape that differs from the key's window), the batch residual contains (1 − ψ)-type misfit proportional to g. Then β̂ ≈ ψg and se ≈ g√(1 − ψ²)/√n, and the condition becomes n ≳ t²(1 − ψ²)/ψ², which does not depend on g. So detection takes a fixed number of batches, however strong the copy. That is the "nearly independent of g/c" of §3.2 and §7.6, and the 70–220 s.

A likelihood-ratio test with a **fixed** noise scale (the pre-change law treated as known, which is what Lorden and Lai assume) has a per-batch score that grows like ψg. It crosses in one batch once ψs is a few times η_b above the boundary. Mei's remark gives the design: when "in control" means "slope ≤ κ_g", the minimax CUSUM is the one designed **at the boundary** κ_g.

**The bank checked (check.py, CusumBank).**
- Same 153 keys per channel as revision 2.
- Batch-centred P_b, E_b, so the step from b_id to today's level never enters (a nuisance change removed by invariance; Xie et al. §III-C).
- Normalised batch slope b̂ = P_b/(c_k E_b) with weight E_b/(N_b σ_u²).
- Score (s₁ − κ_g)(b̂ − (κ_g + s₁)/2)·w for two design slopes s₁ ∈ {1.2, 3.0}.
- CUSUM S ← max(0, S + score) per key; engage at S > h. On engagement, a_k = min(a_k, κ_g c_k / pooled slope of the current run) (ratchet).

Every output-side quantity is a multiple of c_k (homogeneous of degree 0 in (c_k, r_k) by construction; Lemma 0's numerical check was not repeated).

**False engagement (check B).**
- The largest CUSUM statistic on any capped channel, key and design slope, on the calibration partners (seeds 7–14, 1 h and 30 min, b_id), was 3.82, so the threshold was set at h = 1.5 × 3.82 = 5.73.
- On the held-out partners (seeds 15–22, 1 h) and the four K6 stress cases (u⁰ = mean ∓ 0.10, one livelier), the largest was 4.61: **0 of 12 engaged.**
- Revision 2's own figure is 0 of 20. "Equal false engagement" therefore means zero at the resolution of these runs (about 240 held-out channel-hours: by the rule of three, below about 1 per 80 channel-hours at 95 %). It is not a measured rate.
- The held-out maximum (4.61) is closer to h than the calibration maximum. Because of the heavy tails, h corresponds to about 64 nats at η_b = 0.3, against 12–17 for the Gaussian formula: the empirical threshold is about 4 times the Gaussian one, and Table 1's KL-limited entries should be read as optimistic by that factor.

**Detection and residuals (check D; revision 2's R2 cells: 6 scenarios × 16 cells, c ∈ {0.03, 0.05, 0.10, 0.35} × g/c ∈ {1.5, 3, 10, 33}; residual / c_k; detection = median over cells with g/c ≥ 3):**

| scenario | rev2: session max, cells > 1.0 c, 20-min max, detection | **CUSUM alone** | **envelope + rev2** | **envelope + CUSUM + rev2** |
|---|---|---|---|---|
| copy, 90 s (on grid) | 0.68, 0/16, 1.42, 80 s | 0.76, 0/16, 1.34, 10 s | 0.65, 0/16, 1.00, 0 s | **0.54, 0/16, 0.76, 0 s** |
| copy, 47.35 s (off grid) | **1.06**, 1/16, 1.50, 113 s | 0.50, 0/16, 0.84, 13 s | 0.63, 0/16, 1.50, 0 s | **0.36, 0/16, 0.84, 0 s** |
| low-passed 120 s | 0.95, 0/16, 2.00, 425 s | **1.29, 2/16**, 1.56, 330 s | 0.95, 0/16, 1.40, 275 s | 0.95, 0/16, 1.31, 150 s |
| low-passed 300 s | 0.90, 0/16, 3.92, 728 s | 0.94, 0/16, 3.92, 1170 s | 0.90, 0/16, 3.90, 413 s | 0.90, 0/16, 3.90, 413 s |
| on 6 min / off 24 min | **1.26**, 1/16, 3.69, 120 s | 0.36, 0/16, 1.83, 20 s | 0.53, 0/16, 1.70, 0 s | **0.30, 0/16, 1.70, 0 s** |
| gain grows exp., θ 300 s | 0.45, 0/16, 1.08, 2889 s | 0.54, 0/16, 1.30, 3020 s | 0.45, 0/16, 1.08, 2889 s | 0.42, 0/16, 1.08, 2889 s |
| **all 96 cells above 1.0 c** | **2** | 2 | **0** | **0** |

Plainly:
- **On plain, off-grid and switched copies, CUSUM detects 5–8 times faster** at the same zero false engagement. The off-grid failure (1.06 → 0.50) and the switched failure (1.26 → 0.36) disappear, and the 20-min windows fall (1.50 → 0.84 off grid).
- **On slow routes it is worse** (1.29 c, two cells above 1.0). Batch centring removes the slow level that revision 2's level keys with an intercept see. So CUSUM is a companion: run both and take the smaller gain. Each stage is attenuate-only, so the minimum is too.
- **Does the ratchet already approximate CUSUM?** Partly.
  - The ratchet makes engagement final, which is the stopping-rule half of CUSUM.
  - The 1-min memory is a crude window-limited test: it forgets old evidence, as CUSUM's reset to zero does.
  - What revision 2 lacks is the likelihood with a known noise scale: its t test pays for not assuming the pre-change law by needing several batches whatever the copy's size.
  - The ratchet's real value against switching is different (Sokolov et al.): once **any** on-period is caught, every later one is held, so only the first on-period counts.

## 4. The envelope: zero false engagement by construction (Proposition 3, check C and D)

**Proposition 3 (my derivation; the idea is the standard model-based fault-detection pattern with bounded uncertainty, for which no source was read in this pass).** Suppose every listed route from his face to channel k is a linear filter with impulse-response ℓ₁ norm h_{k,i}, times a gate in [0, 1], driven by v = u − u⁰ (his deviation from b_id). Then for every partner path, open or closed loop, and every t,

  |r_{L,k}(t)| ≤ Γ_k · sup_{s≤t} |v(s)|,  Γ_k = Σ_i h_{k,i} c-scaled gains.

So |r_k(t)| > Γ_k sup|v| proves that an unlisted partner-caused part is present, **with zero false engagement**: it is a certificate, not a test.

The stage a_env(t) = min(a_env(t − 1), Γ_k sup|v| / |r_k(t)|):
- is attenuate-only and ratcheted;
- commutes with the metric, because it is multiplicative;
- never lowers a_env below Γ_k/g for a copy of gain g, because |g v(t − D)| ≤ g sup|v|.

After its first action the route renders at an effective gain ≤ Γ_k, so Theorem 1′'s transient term (g/c)·Q_tr becomes (Γ_k/c_k)·Q_tr, whatever g is.

In this synthetic engine:
- the fast gear runs through the 4-s onset high-pass, whose ℓ₁ norm is 2;
- the held cone is a low-pass with ℓ₁ norm 1, at 0.22 c_k;
- so Γ_k = 2G_k + 0.22 c_k ∝ c_k, at most 1.82 c_k (G_k ≤ 0.8 c_k), and 0.42 c_k on BI.

On channels whose listed routes are weak, the envelope alone holds a copy below κ_g from the first frame.

**Checked:**
- 0 frames over the envelope on all 28 ordinary and stress partner-sessions (by construction).
- In check D, detection at 0 s (median) for g/c ≥ 3 on plain, off-grid and switched copies.
- The switched cell falls from 1.26 to 0.53 c, the off-grid cell from 1.06 to 0.63 c, and no cell exceeds 1.0 c.
- The envelope is blind to routes whose peaks stay under Γ_k: slow (low-passed) copies and gains below Γ_k. There the statistical stages do the work.

**Caveats (each needs work before it could be built).**
1. **The real listed routes need peak-to-peak gains, not the H∞ sup gains** that the ledger design records (design-cayley-ledger.md: the appraisal band-pass's sup 0.636 is a frequency-domain bound; its ℓ₁ norm is larger), and every gate must be in [0, 1]. Nonlinear listed parts need a certified peak bound (pass 10's certified blocks give ℓ₂ incremental bounds; a peak version is a different certificate).
2. **"sup since session start" can be blinded by the partner.** One large early movement raises sup|v| and leaves later copies under the envelope. The fix is a fading sup over the listed routes' memory with an exact exponential tail term (for a low-pass of time constant τ: |lp(v)(t)| ≤ sup_{[t−H,t]}|v| + e^{−H/τ} sup_{all}|v|). That fix is not checked here.
3. **The bound is exact only if the shadow's equality (rule 10) holds.** Anything else that makes the factual and shadow runs differ (an A5 failure) appears as "unlisted" and is attenuated, which errs on the safe side.

**Closed loop.** The envelope is a statement about the listed routes' input–output map. It holds when he mirrors the agent (v then contains the agent's own output), where the regression tests' "exogenous regressor" reading does not. This is the only stage of the net for which the mirroring-partner gap (§7.3) does not arise.

## 5. Evasion and the floor no detector beats (Proposition 4)

The sources treat one adversary: Lorden's ess sup over the pre-change path is the delay against an adversary who **chooses the change time with access to the data** (Moustakides 2008, restated by Veeravalli & Banerjee §V), and CUSUM is exactly optimal against it. A route that **switches on and off to evade** is a sequence of transient changes (Sokolov et al.). For those, the probability of detecting within a change of total information of a few nats is small at low false-alarm levels for every rule. Their Table 1: a 5–10-sample one-SD shift is caught within its duration with probability 0.03–0.06 at LPFA 10⁻⁴.

**Proposition 4 (evasion floor; my derivation in the Gaussian batch model).** Let a detector have false-engagement probability ≤ α within a window of length T_w on ordinary partners. A route active for a total time T_on in that window at slope s carries total information KL = (T_on/τ_b)(s − κ_g)²/(2η_b²). By the data-processing inequality for the binary event "engaged", it is caught with probability at most (KL + log 2)/log(1/α). So:
- (a) **Bursts.** A burst of slope s lasting less than about 2η_b²τ_b log(1/α)/(s − κ_g)² is usually missed by every detector. Its contribution to a T_w-window metric is about s · T_on/T_w. That is largest for s near κ_g and small for large s; for example, at s = 1.5, η_b = 0.3 and T_w = 20 min it is ≤ 0.08 c.
- (b) **Sustained evasion.** Spreading the activity over the whole window, the largest slope that stays undetected with probability ≥ 1/2 is about

  s_floor ≈ κ_g + η_b √(2 τ_b log(1/α) / T_w).

  With η_b = 0.3, τ_b = 20 s and α = T_w/(100 h): 0.67 c for T_w = 1 h and 0.72–0.75 c for T_w = 20 min. **No detector beats this floor, and a detector that scans all window lengths (CUSUM or GLR over change times, or revision 2's three memories as a coarse grid) attains it up to constants.** It lies below 1.0 c, so a switching route can hide only by staying weak.
- (c) **Above the envelope there is no statistical floor.** A frame with |r| > Γ_k sup|v| is caught deterministically, so bursts at gains above Γ_k cannot evade by timing at all. Caveat 2 of §4 (the fading sup) is needed against a partner who inflates sup|v| on purpose.

**Checked (check E; c = 0.05, copy delayed 90 s, four partners, worst):**
- g/c 1.5, on 20 s of every 40 s: revision 2 first engages at 1544 s (session 0.72 c, 20-min 0.87 c); CUSUM at 220 s (0.18 c, 0.49 c).
- g/c 5, on 60 s of every 600 s: revision 2 engages at 2520 s (0.92 c, 20-min 1.56 c); envelope + CUSUM + revision 2 at 600 s (0.09 c, 0.81 c).
- The one pattern nothing caught (g/c 1.5, 60 s of every 600 s) left 0.32 c in the session and 0.43 c in the worst 20-min window. That is Proposition 4: it evades because it is weak.

**Who is the adversary here?** In Q35 the unlisted route is inside the engine. It can learn to evade only if some learner sees the governor's action, so a rule follows: **the governor's and envelope's gains and statistics must be invisible to every learner** (no gradient through a_k, not in replay features, not in any learned route's input). The partner is the other adaptive party. He controls the regressor (his movement), and through it the information rate and the metric's floor (pass 10, Observation 4). No detector controls that.

**What no detector removes (check F).** Divided by the route's own gain, the raw route's worst 20-min window reads up to 1.92 g (switched, c 0.03, g/c 10) and 1.25–1.54 g in other switched cells, and up to 1.06–1.11 g for low-passed copies. The windowed metric reads more than the route's gain: the pathwise inflation of pass 10's Observation 4. The 1.70 c left in the switched copy's worst 20-min window at g/c 1.5, and the 3.90 c of the 300-s low-passed copy at g/c 10, are of this kind together with §2 (iii). Detection speed cannot remove them. Only a lower target in short windows, or the long-window reading of the guarantee, can.

## 6. Q18 and principles check

| Requirement | CUSUM bank | Envelope |
|---|---|---|
| per channel | yes: one bank per channel, same keys as revision 2 | yes: Γ_k per channel |
| thresholds scale with c_k | boundary κ_g and design slopes in units of c_k; b̂ = P/(c_k E); h and σ₀ are on his signal or in units of c_k: homogeneous of degree 0 (Lemma 0 by construction) | Γ_k = 2G_k + 0.22c_k with G_k = PHI_k c_k, so ∝ c_k; a_env is invariant to scaling (c_k, r_k) |
| one general rule, no situation named (D88) | yes; h and the design slopes are general statistical settings, the same for every channel. h was calibrated on synthetic ordinary partners, so its false-engagement rate on real partners is **unknown until recorded dyads (M4)** | yes; Γ_k is derived from the innate route table, as the ceilings are |
| attenuate-only, sign-preserving | a_k ∈ [0, 1], multiplicative, ratchet | same |
| never a settling state | as revision 2 (a caught route is held at κ_g c; §6.3's tension unchanged) | holds a caught route at ≤ Γ_k until the statistical stages finish |
| no partner expressions as reward | nothing learns from it; **its gains and statistics must be hidden from every learner** (§5) | same |
| no emotion labels or named emotion variables | none | none |
| cost on ordinary partners | 0 of 12 held-out/stress sessions engaged; heavy tails make the margin (held-out max 4.61 vs h 5.73) thin | 0 by construction; costs nothing |

## 7. Novelty verdict

**A component, not a new core.**
- CUSUM is Page 1954, and its optimality is Lorden 1971 and Moustakides 1986.
- Designing at the boundary is Mei 2006's remark.
- Window-limited GLR is Lai 1998.
- The envelope is the textbook model-based residual check with a bounded uncertainty set.

What the pass contributes is the translation into this governor's units: the frontier table, the diagnosis of why revision 2's delay does not shrink with a copy's strength, the evasion floor and the closed-loop observation about the envelope. No designs.md line.

## 8. Q35: what the frontier adds to the options

The three existing options under Q35's update stand: build revision 2 with the one-minute fix (recommended), build it without, or keep the current net as a monitor. The frontier adds:
- **Revision 2's two failures are not information-limited.** A frontier detector would hold them. The trade-off "faster detection costs false engagement" is real only for copies at about 1–1.5 times the limit, and those leave ≤ 0.04 c per hour when missed.
- **What no detector can do:** slow copies and growth judged over 20-min windows, copies above about 14 times the limit judged over 20-min windows when the detector uses 10-s means, and the metric's own over-reading. These stay as visible warnings whatever is chosen.

One possible addition, drafted for the parent to put to the operator if it wishes (it would be a third revision of a design whose tuning D99 stood down, so it needs its own independent critique before it is built):
- **Add the envelope stage (and optionally the CUSUM bank) to revision 2 before day 1:** on the checked synthetic cells it removes both edge cases (no cell above the limit; switched 1.26 → 0.30–0.53, off-grid 1.06 → 0.36–0.63) with no false engagement by construction from the envelope. The cost is stating every listed route's peak gain (the appraisal display's still has to be computed), and, for the CUSUM part, a threshold whose false-engagement rate on real partners is known only after recorded dyads.

## 9. What remains open

1. Peak-to-peak gains Γ_k for the real listed routes (appraisal display, gates) and a fading-sup envelope against a partner who inflates sup|v| (§4, caveats 1–2); neither is computed or checked here.
2. The CUSUM threshold on real ordinary partners (M4). The heavy tails (kurtosis ≈ 10) suggest a robust or distribution-free threshold (a martingale law-of-the-iterated-logarithm bound, Xie et al. §IV-B), not read here.
3. A band-wise envelope for slow routes: the fast gear's contribution through a 60-s low-pass has a much smaller ℓ₁ norm than 2G_k, so a slow-band envelope could catch slow copies the peak envelope misses. Not derived or checked.
4. The mirroring partner for the statistical stages (unchanged from §7.3), and nonlinear unlisted routes with memory (D93, O1).
5. Lorden, Moustakides, Lai and Page were read only through the surveys; their exact conditions for dependent data (Lai's condition (69)/(71)) were not checked against the governor's statistic beyond the measured lag-1 correlations.
