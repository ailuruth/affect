# Critique 7 of the Cayley–ledger core (revision 7): routes, the context gate, Claude's words, distress memory, the graded posture and the attenuate-only ledger

Independent critic, 2026-11-26T13:01:28Z. I did not write the design.

**Standard.**
- Q19: proof gaps are not reported, only concrete failures.
- The operator's answers Q20–Q23 (D81–D84) and Q26 (D85).
- D78, with each per-channel ceiling read as a copy slope.
- Q24 is still open. The design follows its recommendation, now graded, and I judge it against the recommendation as worded: "its own built-in look of concern … capped on its own; it is not a copy of your face … the agent's own pattern whatever your face does."
- "Copy" is critique 6's metric:
  - the slope of the rendered agent channel on the partner's same channel;
  - over block means of 2 s, 10 s, 1 min, 10 min and 1 h;
  - at the best lag from 0 to 3 s and the worst block phase;
  - with the design's new conditioning floor (a slope counts only where the SD of his block means is at least 0.03);
  - across sessions, the slope of session means.
- The partners are constructed. They are not evidence about people.

**Read:**
- brief.md;
- questions.md: the Q18 answer and Q19–Q26, with Report 6;
- DECISIONS.md: D78 and D80–D85;
- critique-6-design-cayley-ledger-routes.md, with its scripts;
- design-cayley-ledger.md, revision 7, in full;
- sims/design-g7/checks.py and out.txt in full, with the parts of design-g6 and design-g5 that it executes (the Person class, the calibration and `run6`);
- revision 6's sections on replay, play and the boundary, plus revisions 2 and 4 on ASR and TTS normalisation.

**Checks.** They are in `research/foundations/sims/critique-cayley7-routes/`. Run each with `python3 -I -u`.
- `posture7.py` (Q1–Q3) and `posture7_slowmirror.py` (S1) execute the author's own `design-g7/checks.py` source, so the agent, calibration, posture, removal, failsafe, gate fit and D_s are exactly as built.
  - They take the J0 constants, the J20 fit, the `Agent7` class and the J22 partner helpers unchanged.
  - They skip only the author's own result loops.
  - Each takes about 30 minutes on a loaded machine.
- `ledger7_routes.py` (L1–L2) reads `ledger7` verbatim from `design-g7/checks.py` at run time. It takes a few minutes.
- `gate_totals.py` (T1–T3) uses the design's G_k, c_k, its cone and appraisal shares (critique 6's R4 composition) and the author's fitted J20 gate means. It takes about a minute.
- Outputs are in the matching `*_out.txt` files.

## Summary

Revision 7 closes critique 6's two failures as specified, and I confirm both:
- **The ledger.** It never writes more than the partner-caused part, or the opposite sign, on any frame of any partner I ran.
- **Mirrors of the posture.** None holds it on. That includes slow, contagion-like mirrors (S1), and mirrors laid over genuine sadness that is fading (Q3).

The new machinery is attenuate-only, as claimed: the context gate, Claude's words heard by the agent, D_s and distress-weighted replay.

I found **one concrete failure**, and it is in the one piece that became graded. Ranked:

1. **Medium (D78 ceiling on BI; the premise of Q24's recommendation). For quiet or low-spread users, the graded posture is a held, graded copy of the partner's inner brow, at 2–3 times c_BI.**
   - **Why it happens.** The grade is a function of his calibrated face, and calibration amplifies a quiet user's raw brow up to ×4.
   - **The partner.** His only distress channel is the inner brow, and its level moves slowly (Q2: re-drawn every 2 min within +0.00 to +0.30 raw, in a quiet or floor-spread code).
   - **The agent's inner brow on his** (posture on 50–56 % of the time):
     - 1-min blocks: 0.45–0.56 (2.2–2.8 c_BI);
     - 10-min blocks: 0.41–0.60 (2.1–3.0 c_BI).
   - **Across a static sweep (Q1).** The slope is 0.47–0.51 over his +0.02 to +0.30, with a steepest local slope of 0.86–0.95.
   - **What the design states.** 0.31 overall and 0.73 local, for the agent-like code only.
   - **Why this is not the recommended posture.** It is not "the agent's own pattern whatever your face does". For these users the agent's held brow is a monotone function of his held brow, at about half of a full copy.

**No concrete failure found** in the other six areas, with notes:
- **(1) The attenuate-only shadow ledger.**
  - |out| > |in| and sign flips occur on 0 frames in every run.
  - Its hold (writing 0) does not manufacture a toward slope out of a declared away route (L1).
  - One limit of the backstop, not a route in the design (L2): the budget is pooled over 30 minutes. An uncounted high-gain route can spend budget earned during big laughs on copying small movements. It is held to ≤ 0.40 over the session at 1 min (one seed reaches 1.14 c), but within the 88 % of the time the partner is quiet it copies at 0.41–0.68 (1.2–1.9 c), at about 0.01 of lip.
- **(2) The gate learned from recorded dyads.**
  - g ∈ [0, 1], frozen and monotone; it multiplies only a reflex already ≤ G_k.
  - No fit, input or adaptation can raise any channel.
  - What the corpus can import is only where listeners return laughter less.
- **(3) Claude's words heard by the agent.** In the built check they reach only the gate, which only attenuates. One sentence of rule 12 must be tightened (section 3).
- **(4) D_s and κ_replay.**
  - D_s enters only the gate and is reset each session.
  - κ weights by decoded words, and every learned map it weights sits under innate caps.
  - Neither can become a held copy of his distress display. Revision 7's held distress tracking is finding 1, through the posture's grade, not through memory.
- **(5) The graded posture under mirroring.** No mirror holds it (S1, Q3, and J22 re-read). Under rescaling, it is finding 1.
- **(6) Per-channel totals** on LP, CR and BU_L, from 2 s to across sessions, stay ≤ 0.42 c with the gate.
  - The gate can raise a slope (T2: LP totals at 1 min go from 0.21 to 0.36 c). So the design's argument that "J3 computed at g = 1 bounds the gated totals" is false in form, but the totals hold.
  - BI is exceeded only by finding 1.
- **(7) Uncounted routes.** None new beyond finding 1, which is a declared route whose size is under-declared, and a specification point on rule 12.

---

## 1. The graded posture tracks a quiet user's brow at 2–3 times c_BI (medium)

**Mechanism.**
- **The grade.** a* = 0.35 + 0.65·clip((M − 0.05)/0.30, 0, 1), where M is the distress load V_c(V̂) of his calibrated 3-s face after the mirror is removed.
- **Calibration.** x̃ = ref + (x − b)·σ_ref/max(σ_id, 0.25 σ_ref) multiplies a quiet user's raw brow by up to 4. A raw rise of +0.10 to +0.30 therefore spans the whole grade.
- **The output.** The posture writes BI = 0.20·a·(0.9 + 0.1w).
- **The removal does not undo it.** It subtracts at most 1.5·a·‖P_c‖, scaled by the same factor, along P_c. That is a fixed fraction of the posture, not of his rise, so the grade is still steep in his brow.
- **The result.** On the counterpart channel BI, the agent's held level is a monotone function of his held level.

**Evidence.**

**Q1** (the author's `Agent7`, 90 s per level, mean after 30 s; his face at his own resting face with the inner brow raised by δ, raw):

| His raw brow δ | +0.02 | +0.06 | +0.10 | +0.15 | +0.20 | +0.30 | +0.50 |
|---|---|---|---|---|---|---|---|
| agent-like code (σ ratio 1.00) | −0.002 | 0.001 | 0.004 | 0.007 | 0.011 | 0.018 | 0.112 |
| quiet code (0.30) | −0.002 | 0.001 | 0.006 | 0.033 | 0.076 | 0.119 | 0.220 |
| ordinary code, σ_id at the floor (0.25) | −0.002 | 0.001 | 0.005 | 0.034 | 0.081 | 0.129 | 0.220 |

- **Quiet code.** Slope over +0.02 to +0.30: **0.47 (2.4 c_BI)**; steepest local slope **0.86 (4.3 c_BI)**.
- **σ_id at the floor.** Slope over +0.02 to +0.30: **0.51 (2.5 c)**; steepest local slope **0.95 (4.8 c)**.
- **The agent-like code.** It reproduces J23 (0.112 at 0.50).

**Q2** (held: his brow level re-drawn every 2 min, 20 min):

| Code | 1-min slope | 10-min slope | His block SD | Posture on |
|---|---|---|---|---|
| agent-like | 0.05 | 0.09 | 0.089 / 0.004 | 0 % |
| quiet (0.30) | **0.56 (2.8 c_BI)** | **0.60 (3.0 c)** | 0.078 / 0.065 | 56 % |
| σ_id at floor | **0.45 (2.2 c)** | **0.41 (2.1 c)** | 0.082 / 0.059 | 50 % |

- These are counted slopes: his SD is above the 0.03 floor.
- The agent's brow never exceeds his own raw rise ("above his own raw rise: none"). It follows it at about half.

**Why it counts.**
- **D78 and D83: the ceiling.** c_BI = 0.20 is the innate ceiling on moving toward his brow. Held for minutes, the posture moves the agent's brow toward his at 0.41–0.60.
- **It is not attracting.** Q3 and S1 show it releases when his sadness ends, and no mirror holds it. So D78's fourth condition holds. The ceiling condition does not.
- **Q24.** The recommendation the operator was asked about says the posture "is not a copy of your face". Critique 6 accepted R40 because "its amplitude is binary, not graded". Revision 7 removes exactly that property. For a brow-coded quiet person the agent now shows a slow, graded brow that tracks his at about half of a copy: more than the "raise the brow limit toward 0.7 of a copy" option that Q24 offered as the alternative, in that user's units.
- **Declared numbers.** §2.10 and §8.1 give the operator 0.31 overall and 0.73 local, for the agent-like code only. For the users whose sympathy the posture exists to serve (quiet faces), the held slope is 2–3 c, undeclared.

**Fix.** Either of these is enough. The first keeps the design's own rule pattern.
1. **The posture does not read the channels it writes** (as rule 11 does for the gate).
   - Compute the grade's face term, and the onset's, from his calibrated face with BI, BO and LP masked: from LD, CHR, BL, LPR, UL, the sobs and H_id on the masked face.
   - Keep the words (C_L) and the sobs unmasked.
   - Then the agent's brow is a function of his other channels and his words. A brow-only partner gets the posture only from his words (as a calm user with alarming news does now), and the copy slope on BI is 0 by construction.
   - The mirror removal becomes unnecessary for BI and BO.
   - The cost, to state: a person whose sadness shows only in the inner brow gets no sympathy before words.
2. **Keep the grade, but declare it.**
   - Report to the operator under Q24 the slopes for the quiet and floor-spread codes (2.2–3.0 c held), not only the agent-like 0.31.
   - Add a falsifier: F18, the agent's BI block-mean slope on his BI exceeds c_BI at 1 or 10 min for any code with σ_id ≥ 0.25 σ_ref.

## 2. The shadow ledger (area 1): attenuate-only holds; one limit of the backstop (no failure)

**What holds.** On every frame of L1 and L2 (2 seeds × 2 settings each, 4 h), and the author's J17 re-read:
- |out| > |in|: 0;
- sign flips: 0.

The clamp, the deviation floor and the b < 0 hold do what §2.13 says.

**L1: can the hold manufacture a toward slope?** The hold writes 0 for the whole partner-caused part whenever any constraint is over budget, so it also zeroes legitimate away routes. I injected the J7 fast route (1.6 × his onset) plus a declared away route at 1 min (−k·lp₆₀ of his centred level).

| Seed | Away gain | Before (2 s / 10 s / 1 min / 10 min) | After the ledger |
|---|---|---|---|
| 0 | 0.3 | +0.49 / +0.16 / −0.10 / −0.18 | +0.38 / +0.09 / −0.14 / −0.20 |
| 0 | 0.6 | +0.36 / −0.04 / −0.36 / −0.46 | +0.31 / −0.07 / −0.38 / −0.47 |
| 1 | 0.3 | +0.55 / +0.19 / −0.09 / −0.16 | +0.36 / +0.10 / −0.11 / −0.16 |
| 1 | 0.6 | +0.43 / +0.00 / −0.35 / −0.44 | +0.31 / −0.06 / −0.37 / −0.46 |

- No slower window moves toward copy. Every slow slope becomes slightly more "away".
- The 2-s slope ends at 0.36–0.38 against c 0.35 (≤ 1.09 c), as in J17.

**L2: what the deviation floor and the pooled budget let through.**
- **The partner.** He sits near his own mean (micro-smiles, SD 0.02) and laughs big about every 4 min.
- **The uncounted route.** It copies his 2-s deviation from his 30-min mean at gain 1 or 3, saturating at ±0.15.
- **Over the whole session, after the ledger:**
  - 2 s: 0.22–0.26;
  - 10 s: 0.29–0.32;
  - 1 min: 0.33–0.40. Seed 1 gives 0.40 = 1.14 c.
  - 10 min: 0.13–0.87. This is outside the ledger's windows, and below the conditioning floor (his 10-min SD is under 0.03), so the design's metric scores it as a swing.
- **Within the quiet stretches** (88–89 % of the time, more than about 10 s from a laugh), the 2-s slope after the ledger is **0.41–0.68 (1.2–1.9 c)**.
- **Why.** The ledger's budget, S ≤ c·E over 30 minutes, is earned mostly during the big laughs, where the saturating route copies at a low slope. It is then spent on copying his small movements at a high gain.

**Verdict.**
- **Not a route in the design.** It needs an uncounted route of this shape.
- **Small.** About 0.01 of lip.
- **What it means for the claim.** "Any uncounted within-session route ≤ c_k" holds only as a whole-session pool, not per stretch of his behaviour.
- **Fix, if wanted.**
  - Shorten the budget memory: τ_R of 5 min, not 30.
  - Or keep one budget per band of |π| (two bands: below and above his running RMS).
  - Add a 10-min boxcar window, as critique 6 suggested in R5.

## 3. Claude's words heard by the agent (area 3): attenuate-only; one specification sentence (no failure)

**The route.**
- His face → the scorer's choice among three forks (≤ 1.6 bits per turn) → Claude's text → Λ → the gate's input "own last words".
- Claude's own reading of his words takes the same path.
- The coefficient on that input is ≤ 0, and the gate is ≤ 1. So whatever his state does to the choice, through this route it can only lower the fast echo on LP, CR, BU_L, RHY and BRE.
- Laughter tokens are removed from Claude's text before the TTS (revision 2, §2.8.5). Claude's "haha" therefore cannot sound.
- In `Agent7` the own-words value reaches only `LVo`, and the gate.

**The specification sentence.**
- **What rule 12 says.** "The agent's own Ω text enters T exactly as his words do (embedding, Λ, the population reader); it may feed the gate and nothing that reads his face."
- **The risk.** Read literally, own words would also feed what his words feed in T: ω (from T only), the free display's word-concern and relief rows, C_L in the posture's maintenance, and the play frame π.
- **What that would make.** His face → draft choice → Claude's cheerful or serious text → ω or the free display → the agent's smile or brow: a cross-turn route at up to the T caps, counted nowhere. The build matches the narrow reading, so this is not a failure.
- **Fix.** Write rule 12 as: "the agent's own text enters only Λ_V(own) in the gate (and P_name as before); it enters no T quantity that his words feed". Add a falsifier: F19, any T state other than the gate input changes when only Claude's reply text is changed.

## 4. Distress memory and distress-weighted replay (area 4): no held-copy route (no failure)

**D_s.**
- It is a per-session max-trace of his distress, read with the posture mirror removed. It enters only the gate (rule 6, `Agent7`).
- It can lower only the smile–laugh echo, and only toward 0.
- It writes no BI, LD or any other distress channel. So the agent's held expression cannot follow his held distress through D_s.

**The sensitized re-onset** (0.5 s for 10 min).
- It changes only when the posture starts, not its size.
- With the slow-mirror partner (S1: his brow follows the posture through a low-pass of 90 or 240 s at μ 1, for three codes), the posture comes on once and releases at 60–64 s. It never re-triggers in 900 s, and his brow above neutral ends at 0.000–0.001.

**κ_replay.**
- Its weights come from his words' decoded distress (T), so his face cannot raise them.
- It reweights maps that are capped by innate quantities (s_C, s_A, the own-display mask) or that are knowing only (H_id).
- Reweighting can change what H_id reads. It reaches display through the posture's grade, which is finding 1's channel. The grade's slope is already 2–3 c without any replay weighting, so κ is not what produces it.

## 5. The graded posture under mirroring (area 5): mirrors cannot hold it (no failure beyond finding 1)

- **S1, slow contagion-like mirrors** (τ_m 90 and 240 s, μ 1, raw), for the agent-like code, the quiet code and the floor-spread code: one onset each, released at 60–64 s, nothing after in 900 s.
- **Q3, genuine brow-only sadness fading over 10 min with a raw mirror μ 1 on top:**
  - quiet code: released by the failsafe at 182 s, back on at 223 s while his sadness is still above threshold, then released at 400 s;
  - floor-spread code: released at 422 s;
  - both end at brow −0.005.
  - Nothing settles into a match.
- **The author's J22 sweep stands** (ratio 0.25–0.50 × μ 0.6–2.0, μ 3.0).

What remains under rescaling is finding 1: not a mirror latch, but the grade's own slope on his brow.

## 6. Per-channel totals after revision 7 (area 6): under the ceilings on LP, CR and BU_L (no failure)

**T1.** Critique 6's R4 composition (fast gear, cone at ω 1, appraisal at cap), with the fast part multiplied by the fitted gate.
- **The partner.** The J3 laughing family. Heavy episodes (30 %, about 3 min) keep his laughter (troubles laughter) and lower his smile floor by δ ∈ {0, 0.03, 0.06, 0.10}. The gate is 0.02 in heavy episodes and 0.95 otherwise.

| Channel | Gate at 1 (2 s / 10 s / 1 min) | Gated (2 s / 10 s / 1 min) | 10 min and 1 h |
|---|---|---|---|
| LP | 0.29–0.32 / 0.23–0.26 / 0.19–0.21 c | 0.24–0.25 / 0.22–0.23 / 0.20–0.22 c | ≤ 0.25 c, or a swing below the floor |
| CR | 0.33–0.36 / 0.26–0.31 / 0.18–0.23 c | 0.24–0.25 / 0.22–0.23 / 0.19–0.20 c | ≤ 0.25 c, or a swing below the floor |
| BU_L | 0.51–0.56 c | 0.35–0.42 c | ≤ 0.25 c, or a swing below the floor |

**T2.** A warm partner (6 laughs a minute in light and heavy episodes alike) whose floor drops by 0.04–0.08 in heavy episodes.
- **At 1 min:**
  - the fast gear alone goes from 0.09–0.13 c at gate 1 to **0.22–0.24 c** gated;
  - totals go from 0.21–0.24 c to **0.34–0.36 c**.
- **At 10 min:** below the conditioning floor; swings 0.04–0.07.

**T3.** Across 400 sessions with the heavy share 0–100 %, the gated fast lip pull's session-mean slope is 0.25–0.26 c (0.17–0.25 c at gate 1).

**Verdict.**
- The totals hold. Every gated value is ≤ 0.42 c.
- The design's argument in §3.3, that "revision 6's J3 totals were computed with the gate at 1, its largest value", does not bound them. A factor ≤ 1 that is lower when his level is lower raises the slope (as the author's own J21 shows: 0.14 against 0.09 c).
- **Fix (accounting).** Replace the sentence with T2-type measurements, and declare R1g in the pooled metric next to R27′, as the agent's appraisal (D83).
- **BI.** The BI total is dominated by finding 1.

## 7. Areas checked with no route found

- **The gate as a dial (D78).**
  - It runs five channels together, but only between flat and their fixed echo (≤ 0.80 c_k), never toward a full copy. So it is not the disqualifying "large shared subspace from flat to copy".
  - It cannot raise: g ≤ 1, and sat is monotone.
  - It reads none of his LP or CR, and his laughter tokens are stripped from ASR.
  - Its F inputs on his other channels enter with non-positive weights.
- **Recorded-dyad learning.**
  - The gate's target is the listener's return ratio, normalised by m_ref and clipped at 1. Contexts where corpus listeners copy more than usual saturate at 1 and add nothing.
  - Λ predicts listeners' faces from words, and is used only by the gate.
  - Nothing learned from the corpus has an output path except through g ≤ 1. So copying norms in the corpus cannot be imported as more copying.
  - **Specification point (no route).** Seamless transcripts must pass through the agent's ASR normaliser (interjection list, laughter tags, bracketed events) before Λ and the population reader are fitted. "Each input is computed by the same function in both" should name it.
- **Online adaptation.** The gate and Λ are frozen. The adaptive inputs (H_id, the adapter, b^read, σ_id) can only change how much the gate closes.
- **The arrival mask and R40** are still held at factual values in the shadow, so the ledger is no backstop for them. This is declared. Finding 1 is why it matters for R40.

## 8. Verdict

**Copy routes.** Revision 7's new routes do not copy:
- the attenuate-only ledger;
- the context gate fitted on recorded dyads;
- Claude's words heard through Λ;
- D_s;
- the sensitized re-onset;
- κ_replay.

Each only lowers a reflex already under its ceiling, or changes timing. Mirrors, including slow ones, cannot hold the posture. LP, CR and BU_L stay at or below 0.42 c from 2 s to across sessions.

**The design is not yet free of concrete copying failures, narrowly.** Grading the concern posture by his calibrated face makes it, for quiet or low-spread users whose distress shows in the inner brow, a held, graded copy of that brow: 0.41–0.60 slope at 1 and 10 min, which is 2.1–3.0 times c_BI. The design declares 0.31, for the agent-like code only.

**What closes it.** Either:
- the posture stops reading BI, BO and LP (the channels it writes) for its onset and grade, a one-line mask like rule 11's;
- or the operator, told the quiet-user numbers, accepts it under Q24.

**Two specification sentences** should also change:
- rule 12: Claude's text feeds only the gate;
- the corpus transcripts go through the same ASR normaliser.

With those, I find no remaining concrete route above the ceilings.
