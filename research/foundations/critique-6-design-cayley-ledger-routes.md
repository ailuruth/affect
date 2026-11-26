# Critique 6 of the Cayley–ledger core (revision 6): routes, the onset lobe, the concern posture and the shadow ledger

Independent critic, 2026-11-26T10:17:31Z. I did not write the design.

**Standard.** Q19 and the operator's answers Q20–Q23 (DECISIONS.md D78, D80–D84). Q24 is still open; the design follows its recommendation (a separate concern posture), and I judge the posture against that recommendation.
- Proof gaps are not reported. Each finding is a concrete scenario with numbers.
- "Copy" is the slope of the rendered agent channel on the partner's same channel, over block means of 2 s, 10 s, 1 min and 10 min, at the best lag from 0 to 3 s and the worst block phase. Across sessions it is the slope of session means. This is the metric of critique 5 and of the design's own J3.
- The partners are constructed. They are not evidence about people.

**Read:**
- brief.md;
- questions.md: the Q18 answer and Q19–Q24;
- DECISIONS.md: D78 and D80–D84;
- critique-5-design-cayley-ledger-routes.md;
- design-cayley-ledger.md, revision 6, in full;
- sims/design-g6/checks.py and out.txt in full, and the parts of design-g5/checks.py that it reuses (the reader, `his_face`, H14).

**Checks.** They are in `research/foundations/sims/critique-cayley6-routes/`.
- `posture.py` (P0–P6, A1) executes the author's `design-g6/checks.py` unchanged, so the agent, the reader, the calibration, the posture and the arrival mask are exactly as built. It then runs new partners against them. About 80 s.
- `routes.py` (R1–R5), `ledger_seeds.py` (L1–L2) and `ledger_inject.py` (L3) use the design's constants and a verbatim copy of its `ledger()`. A switch adds the attenuate-only clamp proposed in finding 1. Each runs in under a minute.
- Outputs are in the matching `*_out.txt` files. Run each with `python3 -I`.

## Summary

Revision 6 closes critique 5's findings as specified:
- the fast Jacobian is diagonal;
- no fast gain is learned;
- the word reader is never trained on his face;
- WORLD replaces phrase prosody.

I found **two concrete failures**, both in machinery that is new in this revision and both with local fixes. Three more items are accounting points for the operator rather than copying failures. Ranked:

1. **High (a new route, and a dial the backstop itself creates). The shadow ledger is not attenuate-only, and when it binds it is numerically unstable.**
   - **Mechanism.** The projection bound is (b/π − base)/a. Once the running slope S has climbed above c·E (b < 0) and his centred deviation π crosses zero, that bound diverges. The "clip" then writes outputs of either sign and of any size, including on frames where the partner-caused part was 0.
   - **The design's own J7 injected-route recipe**, seed 0 of three (L3):
     - the ledger's output reaches −7 × 10⁶;
     - the rendered lip sits **at full smile (1.0) on 30 % of frames**, and at 0 on 4 %;
     - the rendered slopes are **−0.9 (2 s), −1.7 (10 s) and −2.4 (1 min)**.

     In this run the backstop turns the lip into a partner-driven full-range channel. With the clamp, the same seed is held at 0.37 / 0.34 / 0.33 against c 0.35.
   - **On the R39 adversary (L1–L2).** The ledger writes more than its input on 5–43 % of frames, and the lip at its floor on up to 4 %. Its "0.78" is a property of these unrenderable outputs. Clipped to what the lip can show, the 1-min slope is **1.2–2.1** over ten seeds and durations, not 0.78.
2. **Medium (D78 condition 4, D81 "stuck in copying"). A faithful mirror holds the concern posture on indefinitely when his spread statistic is low (P5, P5c, P5e).**
   - **Mechanism.** Maintenance subtracts min(1, σ_id/σ_ref)·P_c·a_c from his raw face, then reads it after calibration, which multiplies by σ_ref/σ_id (up to ×4). For σ_id/σ_ref ≤ 0.4 a full raw mirror leaves a residual that reads as distress.
   - **The numbers.** For the design's own quiet code (amplitude 0.3), mirroring the posture at μ = 1 after his sadness ended at 40 s, the posture is **never released** (600 s). The agent's inner brow is held at **0.24** while his is **+0.22**: a mutual brow copy, held.
   - **An ordinary user is exposed too.** An ordinary-expressive user whose σ_id came from six calm sessions locks the same way at ratio 0.4 (μ = 1), 0.3 (μ ≥ 0.8) and 0.25 (μ ≥ 0.6). The 0.25 floor is inside the design's specification.
   - **What does hold.** At ratio ≥ 0.5, or for a mirror at his own scale, it releases at 72–84 s, as J11 says.
3. **Low (accounting, the weakest point the author declared). R39 is an artefact of an ill-conditioned metric with a tiny absolute effect. It is not a copy route.**
   - **Absolute size.** It cannot be made large: pointwise the reflex is ≤ G_k × his level, so the agent's minute-mean swing is ≤ 0.045 (0.012–0.041 over seeds).
   - **Other routes.** Adding the cone and the appraisal at their caps on realistic mixtures adds nothing (R2d).
   - **Realistic held-smile and laughing mixtures** give 2-s slopes of 0.12–0.15 and 1-min slopes of −0.16 to +0.22. The worst is **0.46 (1.3 c) at 10-min blocks**, with an absolute difference of 0.015 lip, when the laughing episodes average 0.014 above the held ones.
   - **Across sessions.** Slopes are −0.24 for style mixtures and +0.13 (0.37 c) for sessions that differ only in laugh rate.
   - **Fix.** Restate the fast bound as a level bound, and give the copy metric a conditioning floor (below).
4. **Low (accounting, for the Q24 decision). R40 is wider than stated.**
   - **The slope.** The posture is a step in his distress reading, so its copy slope depends on where his face sits. For a brow-only sad partner it is ≈ 1.2 between his brow 0.30 and 0.50 (agent 0.018 → 0.252, P6), not 0.49.
   - **Other channels.** It also exceeds c_TILT (head tilt +0.10 against 0.03) and writes a zero-ceiling channel (UL −0.06, "softened eyes").
   - **Verdict.** Under Q24's recommendation this is the agent's own pattern and acceptable. The operator should see these numbers when answering Q24.
5. **Low (accounting). The arrival mask (R27′) is a large pooled route at the arrival window, invisible to the ledger.**
   - **The numbers (A1).** Across arrivals where a sad face also smiles less, the slopes of the at-sight lip and cheek on his are **1.11 (3.2 c) and 1.27 (5.1 c)**. The partial derivative on his lip pull alone is 0.00, and the design quotes that number (≤ 0.040, H14 of revision 5).
   - **Verdict.** It is D83 appraisal (not beaming at a mourner) and not a copy of his smile. It should be declared with R40, in the same metric.
6. **Low (specification). WORLD replacement does not cover pause and latency.** It replaces F0 level, range, energy and rate. Pause (c 0.05) and latency (c 0.05) still follow the chosen draft's punctuation and timing. The question and statement templates must also be normalised to equal phrase-mean level and range.

**No concrete failure found:**
- **(2) Per-channel totals.**
  - With the fixed per-channel echo plus the onset lobe, every channel stays under its ceiling at 2 s, 10 s and 1 min (J3 reproduced in substance), and at 10 min and 1 h: LP 0.23–0.24 c, CR 0.21–0.24 c, BU_L 0.58–0.62 c (R4).
  - Across sessions it stays ≤ 0.37 c on natural laugh-rate variation (R3).
  - The only exceedances are the R39 family (finding 3).
- **(4) Calibration, H_id and the population reader.**
  - None is a gain on a path to expression.
  - H_id reaches the display only through the posture trigger (binary), m_s (attenuate-only), bids and the appraisal selection α, whose display is capped for any α.
  - The word reader is frozen, and the adapter learns from words.
  - I found no way to learn his face through his words into a display. The one place calibration does act on the display is the posture's maintenance, and that is finding 2.
- **Rule J and cross-channel fast paths.** Both are closed by construction.
- **Fast gains under learning.** They are constant.
- **The dyad loop.** It is stable for |μ| < 1.36. The posture lock in finding 2 is a latch, not a dynamic instability.

---

## 1. The shadow ledger writes outputs the partner-caused part did not contain (high)

**Mechanism.**
- **The projection.** In §2.13 (and `ledger()` in J7), for each window and lag, the per-step constraint on the new partner-caused value x is
  - (rW_new − rC)·π ≤ b, with b = c(e^{−1/τ}E + π²) − max(0, e^{−1/τ}S);
  - solved as x ≤ (b/π − base)/a for π > 0, and x ≥ (b/π − base)/a for π < 0.
- **When b < 0.** b becomes negative whenever the running toward sum S exceeds c·E. Exponential decay of E against the clamped S makes this happen after any stretch where the ledger could not keep up. The bound then has the sign of −1/π and diverges as π → 0.
- **What the clip does.** `x2 = clip(x, lo, hi)` (or 0 if lo > hi) moves x to that bound.
- **The result.** The ledger outputs large values of either sign, on frames where his deviation from his 30-min mean is near zero. That is, at every crossing of his own mean.

**Evidence.**
- **L3, the design's J7 recipe** (natural laughing partner plus the injected uncounted route, 4 h), three seeds:

| seed | injected, 2 s / 10 s / 1 min | ledger as specified, rendered (lip clipped to [0, 1]) | frames at full smile 1.0 | ledger with the attenuate-only clamp |
|---|---|---|---|---|
| 0 | 0.82 / 0.69 / 0.61 | **−0.92 / −1.72 / −2.37**; min output −7.2 × 10⁶ | **30.1 %** | 0.37 / 0.34 / 0.33 |
| 1 | 0.87 / 0.75 / 0.65 | 0.40 / 0.36 / 0.36; min −848 | 0.0 % | 0.36 / 0.33 / 0.32 |
| 2 | 0.75 / 0.64 / 0.58 | 0.39 / 0.36 / 0.35; min −14 | 0.0 % | 0.37 / 0.35 / 0.34 |

- **L1–L2, the author's R39 adversary**, seeds 0–4 at 4 h and 6 h:
  - the ledger writes |out| > |in| on 5–43 % of frames;
  - it writes output where the input was 0 on 2–28 %;
  - its minimum output is −1.3 to −470;
  - its 1-min slope is 0.60–2.07 on the unclipped output, and **1.23–2.09 rendered**.

  The author's 0.78 is one draw of the unclipped number.

**Why it counts.**
- **It creates a route the typed analysis never had.** His face (through π) and the ledger's 30-min memory write the agent's channel across its whole range. On seed 0 that is an anti-copy of slope −2.4 on lip pull, with the lip at full smile on 30 % of frames, triggered by a route the ledger was meant to cap.
- **It is a single state that runs a channel from flat to full.** It is the ledger's own state, not the partner's strength, and it is not bounded by any ceiling.
- **The design's claims for it fail.** "Attenuate-only on the partner-caused part" (§3.6 table) is false, and "R42 caps every within-session route at c_k" fails on the rendered face.
- **Where it binds.** It does not bind on a natural partner (J7's 0 % clipped holds). So the failure appears exactly when the backstop is needed: an uncounted route, a bug, or a shape adversary.

**Fix (local).**
- **Clamp.** After the projection, set x2 ← clip(x2, min(0, x), max(0, x)). The ledger may then only shrink the partner-caused part toward 0, never extend or flip it.
- **Guard small deviations.** Skip constraints with |π| below a floor, for example 0.1 × the window's running SD of π.
- **Treat b < 0 as a recovery.** It is a state to recover from by holding x2 = 0, not a bound to chase.
- **With the clamp (L1–L3):**
  - the injected route is held at 0.32–0.37 against 0.35;
  - the natural echo is untouched;
  - R39 is 0.69–2.06. The clamp makes the ledger safe; it does not make it close R39 (finding 3).
- **Falsifier to add.** F1‴: the ledger's output ever has larger magnitude than, or the opposite sign to, the partner-caused part.

## 2. A faithful mirror holds the concern posture on when his spread statistic is low (medium)

**Mechanism.**
- **The maintenance rule (§2.1, §2.10).** M = V_c(V̂ of his 3-s face minus min(1, σ_id/σ_ref)·P_c·a_c), with the subtraction applied to his raw face (as in `Agent6.step`) and V̂ read after calibration, x̃ = ref + (x − b)·σ_ref/max(σ_id, 0.25σ_ref).
- **The residual.** A raw mirror μ·P_c·a_c leaves (μ − σ_id/σ_ref)·P_c raw, which calibration amplifies by σ_ref/σ_id.
- **Where it binds.** For a low ratio the residual reads as distress (V̂ ≥ 0.26 gives M ≥ 0.02), so the release timer never runs.

**Evidence (P0–P5, the author's engine unchanged).** His genuine sadness ends at 40 s. From then on his face is neutral plus his answer to the posture.

| Partner | Posture | Last 2 min: agent BI / his BI above neutral |
|---|---|---|
| P0, the author's J11 (agent-like, μ 1) | released 72 s | −0.01 / 0.00 |
| P1, expressive (amplitude 1.5, 2.0), mirror at his own scale | released 74 s | — |
| P2, agent-like, exaggerated mirror μ 1.6 | released 74 s | — |
| P3, agent-like, a mild sad "aww" in his own code | released 72–73 s | — |
| **P5, the design's quiet code (0.3), raw mirror μ 1** | **never (600 s)** | **+0.24 / +0.22** |
| P5b, quiet code 0.5, raw μ 0.8 | released 74 s | — |
| **P5c, ordinary code, σ_id from calm sessions (× 0.4), μ 1** | **never** | **+0.24 / +0.22** |
| P4, different-channel code, a mild "aww" in his own code | never | +0.22 / +0.02 (not a copy; see below) |

**P5e sweep** (ordinary code; rows are σ_id/σ_ref, columns the raw mirror gain μ):

| σ_id/σ_ref | μ 0.4 | 0.6 | 0.8 | 1.0 |
|---|---|---|---|---|
| 0.25 (the floor) | released | **HELD** | **HELD** | **HELD** |
| 0.30 | released | released | **HELD** | **HELD** |
| 0.40 | released | released | released | **HELD** |
| 0.50 | released | released | released | released |

**Why it counts.**
- **It is a copy state the agent settles into.** In P5 and P5c the agent's inner brow and his match (0.24 and 0.22) and stay matched indefinitely, each holding the other. That is D78's fourth condition ("never let copying become a state the agent settles into") and D81's "getting stuck in copying".
- **The design's own claim.** It says "a partner who mirrors it cannot keep it on".
- **The partner is in specification.** The design itself introduced the quiet code. The calibration floor 0.25 is in specification. A MAD over six sessions of a mostly resting face can land at or near it for an ordinary person.

**P4 is a different thing.** There the posture is held by his answering concern in his own code, which reads as his mild distress. It is not a copy (his brow +0.02). It is a mutual-concern latch, an agent-side issue to note: the agent cannot tell sympathy from distress in a lip-press code.

**Fix (local).**
- **Do the subtraction where the reading happens.** Remove from his *calibrated* 3-s face its positive component along P_c (on BI, BO, UL, LP), up to μ_max·a_c·‖P_c‖·max(1, σ_ref/σ_id) with μ_max = 1.5, before V̂ is read for maintenance. Then no mirror of gain ≤ 1.5 in raw or in his own units can hold it.
- **Add a failsafe.** Release after 3 min of maintenance carried only by the face (no C_L, no sobs), with the 60-s refractory.
- **Add a falsifier.** F12 extended to a quiet code and to σ_id at the floor.

## 3. R39, the shape adversary: an ill-conditioned metric, not a copy route (low)

**What it is.**
- **The pointwise lemma.** It gives 0 ≤ y_f,k(t) ≤ G_k u_k(t − 0.45 s). So over any window the fast mean is ≤ G_k × his mean, and the agent's swing between kinds of minute is ≤ G_k × the bursty minutes' mean.
- **Why the slope runs away.** The slope divides that swing by the change of *his* window means. The adversary drives that change toward 0.

**Can it be made larger?**
- **Absolute size: no.** R1 and L1 give a swing of 0.012–0.045 lip pull. Raising his levels raises the swing only as 0.224 × his bursty mean.
- **Other channels.** On signed channels the fast gear is zero-DC. Laugh burst has no held state. Cheek behaves like lip pull, at G 0.150. Inner brow, outer brow and jaw have G ≤ 0.024.
- **Combined with other routes (R2d).** With the cone at ω = 1 and the appraisal at cap on a realistic mixture, slopes are 0.12 (2 s), 0.07 (10 s) and −0.07 (1 min). The other routes respond to his level, which barely moves.
- **Longer windows.** R2 and R3:
  - polite held smile 0.30 against neutral-with-laughs at nearly equal means, in episodes of about 2 min or 10 min: −0.10 to −0.25 at 1 and 10 min (away);
  - with the laughing episodes 0.014 higher: 0.22 at 1 min and **0.46 (1.3 c) at 10 min**, for an absolute 0.015;
  - across 400 sessions, style mixtures give −0.24, and laugh-rate variation alone gives 0.13 (0.37 c).
- **The ledger.** It centres at 30-min means and has no 10-min window, so these slow cases are outside it.

**Verdict.**
- **In realistic conversation** the exceedance is an edge case with negligible absolute effect: ≤ 0.015 lip at 10 min, ≤ 0.045 in the constructed case. It arises only where his window means hardly change.
- **No D78 condition is broken in substance.** The gain is per channel, innate, constant and partial. The excess is a regression artefact, not a strength.

**Fix.** Either of these is enough. I recommend the first, because the second brings back the rectification problem the author names.
- **Accounting.**
  - State the fast gear's slow-scale bound as a level bound: window mean ≤ G_k × his window mean, and swing ≤ G_k × his within-window peak.
  - Give the copy metric a conditioning floor: count a window-scale slope only where his window means vary by at least 0.03 (SD), and otherwise report the absolute swing against c_k × his within-window range.
- **Design.** Subtract the onset lobe's own 60-s mean and add back G_k·φ·lp₆₀(x_d − b_id)₊, which makes the fast DC follow his level.

## 4. R40 is wider than the design states (low; for the Q24 decision)

**The answers to the critic's questions.**
- **Is it graded by his face?** Its amplitude is not: the posture is binary. P6 confirms it for a brow-only sad partner:

| His brow (brow only) | 0.10 | 0.15 | 0.20 | 0.30 | 0.50 | 0.80 |
|---|---|---|---|---|---|---|
| Agent's brow | 0.004 | 0.007 | 0.011 | 0.018 | 0.252 | 0.273 |

- **What the step does to the copy metric.** Because it is a step, the slope depends on his distribution: ≈ **1.2 (5.9 c_BI)** for a partner moving between 0.30 and 0.50, against the 0.49 quoted.
- **Other channels.** P_c also exceeds c_TILT (+0.10 against 0.03, 3.3×) and writes UL (−0.06), a zero-ceiling channel. Only BI is listed in R40.
- **Can a mirror keep it on?** Not when his spread is ordinary (P0–P3). Yes when σ_id/σ_ref ≤ 0.4 (finding 2).
- **Is +0.49 (or 1.2) on the brow a D78 failure?** Not under D83 with the Q24 recommendation:
  - it is one fixed innate vector, not his face;
  - its amplitude is binary, not graded;
  - it is enabled by the relationship;
  - it is triggered by the agent's own appraisal;
  - the copy slope only measures where the trigger sits.

  It becomes a failure only through the latch of finding 2.

**Fix.** List R40's full footprint (BI, TILT, UL) and its threshold-dependent slope in the Q24 report, so the operator decides on the real numbers.

## 5. The arrival mask's pooled slope (low; accounting)

**Evidence (A1, the author's `m_s6` and `at_sight`).**

| Arrival | m_s | Agent at sight: lip / cheek |
|---|---|---|
| ordinary (LP 0.5, CR 0.3) | 0 | 0.52 / 0.35 |
| neutral (LP 0.3) | 0 | 0.52 / 0.35 |
| mildly sad (BI 0.2, LD 0.15, LP 0.15) | 1 | 0.09 / 0.00 |
| grieving | 1 | 0.09 / 0.00 |

- **Pooled over these arrivals:** lip slope 1.11 (3.2 c) and cheek 1.27 (5.1 c).
- **Partial derivative on his lip pull alone:** 0.00.

**Verdict.**
- **What it is.** It is the agent's own appraisal (D83), it is attenuate-only, and it is once per session. It does not copy his smile: a smiling arrival and a neutral one get the same greeting.
- **What the design gets wrong.** Its metric (J3 pools natural co-movement) would report it as 3–5 c. It is held at the factual value in the shadow, so the ledger cannot see it.
- **What to do.** Declare it next to R40 in that metric, rather than quoting H14's partial-derivative 0.040.

## 6. WORLD: pause and latency (low; specification)

- **What is replaced (§6.6).** Phrase-level F0 level, range, energy and rate.
- **What is not.** The pause channel (c 0.05) still follows the chosen draft's punctuation and sentence count. The latency channel (c 0.05) follows which fork wins, and when.
- **Why that matters.** Draft choice is a function of F through the 𝓜 rollout. Under the author's own J6 assumption (draft liveliness correlated with his laughter), the same construction that gave 0.182 for shift-only F0 range applies to pause rate.
- **Fix.**
  - Set pauses from rule-7 targets: fixed pause durations at phrase boundaries, time-warped with the rest.
  - Start speech at the scoring deadline whichever fork wins.
  - Normalise both F0 templates to equal phrase-mean log-F0 and range.

## 7. Other areas checked

- **Totals (item 2).** Covered in the summary (R4, R3).
- **H_id and calibration (item 4).** Neither is a gain on a partner path.
  - H_id is taught by the frozen population reader's decoding of his words. It reaches the face only through binary or attenuate-only uses, or through α, whose display is capped for every α.
  - σ_ref is computed from the agent's own rendered display, which includes the posture. That couples the posture frequency to the reading gain, but the coupling is bounded (the posture is binary and capped), and I found no copy through it.
  - The new word reader passes critique 5's K5 test (J5): slope 0.000.
- **The shadow run (item 5).**
  - Apart from finding 1, it introduces no route.
  - ȳ depends on b_id only through quantities that vanish at a constant input: the cone centring is zero, and the onset lobe and the band-pass are zero after a 4-s start transient.
  - Rule 10 (T equality) is sound as a check.
  - It holds m_s, the posture and the bids at their factual values, so findings 2, 4 and 5 are invisible to it. The design declares this.
- **WORLD (item 6).** Finding 6.
- **Routes not counted (item 7).**
  - The posture's TILT and UL footprint (finding 4).
  - The arrival mask in the pooled metric (finding 5).
  - Pause and latency (finding 6).
  - Nothing new on the zero-ceiling channels except the posture's UL.

## 8. Verdict

The fast side of revision 6 is the cleanest so far: diagonal, constant and pointwise bounded. R39, its declared weakest point, is a metric artefact of negligible absolute size, and I do not hold the design for it.

**The design is not yet free of concrete copying failures.** Both failures are in the new safety machinery:
- **The shadow ledger.** As specified it is not attenuate-only. On the design's own J7 recipe it can drive the lip across its full range (full smile on 30 % of frames in one seed).
- **The posture's mirror-proof maintenance.** It subtracts in the wrong space, so a quiet user, or one with a low spread statistic, who mirrors the posture holds a matched brow (0.24 against his 0.22) indefinitely.

Both fixes are a few lines:
- clamp the ledger to [min(0, x), max(0, x)] and guard small π;
- remove the P_c component in calibrated space, with a 3-min face-only failsafe.

With them, and with R40's full footprint and the arrival mask declared to the operator under Q24, I would find no remaining concrete route above the ceilings.
