# Critique 8 of the Cayley–ledger core (revision 8): routes, the read-disjoint posture, the probe, the word-timed laugh echo, the gated play laugh

Independent critic, 2026-11-26T14:49:23Z. I did not write the design.

**Standard.**
- Q19 and D80: no proof gaps reported, only concrete failures with a scenario and numbers.
- D78 (per-channel ceilings read as copy slopes; copy must not be attracting), D81–D85.
- Q24 is still open. The design follows its recommendation, and I judge it against that wording: "the agent's own pattern whatever your face does".
- "Copy" is critique 6's and 7's metric:
  - the slope of the rendered agent channel on the partner's same channel;
  - over block means of 2 s to 1 h, at the best lag (0–3 s) and the worst block phase;
  - counted only where the SD of his block means is at least 0.03.

  This critique also reports the design's own causal (paired-run) slope, and the level bound, wherever they differ.
- The partners are constructed. They are not evidence about people.

**Read:**
- brief.md;
- questions.md: the Q18 answer, Q19–Q26 and Report 6;
- DECISIONS.md: D78 and D80–D85;
- critique-7-design-cayley-ledger-routes.md, with its `gate_totals.py`;
- design-cayley-ledger.md, revision 8, in full, including the Build-candidate summary and the revision-8 history;
- sims/design-g8/checks.py and out.txt in full;
- the parts of design-g7, design-g6 and design-g5 that the checks execute: Agent7, Person, the calibration, read, Π̃₀, his_face, the codes, play6, laugh6 and run6.

**Checks.** They are in `research/foundations/sims/critique-cayley8-routes/`. Run each with `python3 -I -u`.
- `load8.py` executes `design-g8/checks.py` up to the end of its definitions (Agent8 and helpers), changing nothing and skipping only J31–J39.
  - On this shared machine (load average about 9) the load took 20 minutes, which is the author's own cost. The runs themselves took a few minutes.
- `probe_slow_answer.py` (P1 and P2) uses the author's Agent8 unchanged. Output: `probe_slow_answer_out.txt`.
- `sentence_gate.py` (R1s) and `sentence_gate_extreme.py` (R1s-x) take about a minute each. They use critique 7's composition (G_k, c_k, the onset lobe, the cone and appraisal shares), revision 8's 0.80-s delay and the author's J36 gate values. Their output is reproduced in §3.

## Summary

Revision 8 closes both of critique 7's findings as specified, and I confirm them:
- **The posture's read and write sets are disjoint.** Its part of BI, BO and LP does not change when only his same channel changes.
- **It is steady at constant faces for every code.** It is not released by chance at fluctuating genuine sadness (P2: 0 of 24 runs, OU SD 0.05–0.10 in V).
- **No mirror on the written channels can hold it.**

The laugh echo's word timing, the gated play laugh, rule 12′ and the Seamless specification add no copy route.

I found **one concrete failure**. Ranked:

1. **Medium (D78 "copy must not be attracting"; the design's own F12 and J33 claim). The contingency probe releases answering concern only when the answer is instantaneous. With the author's own full-strength answering partner (P4b–d: his own code at V = 1.0 × the posture) and any lag of 5 s or more (τ 5–90 s), the posture is held for the whole 15 minutes in every code, with all four probes "held".**
   - **The effect.** His sad face and the agent's concern look keep each other up after his own sadness ended at 40 s.
   - **The state at 13–15 min:**
     - posture 0.94;
     - agent inner brow +0.234 (operator's code), +0.198 (quiet), +0.188 (different channels);
     - his face held at V ≈ 0.9–1.0 in his own code, which in the operator's code includes his inner brow at ≈ +0.47.
   - **Why the probe misses it.** It sees his evidence fall by only 1–12 % in its 8-s window, where it needs 20 %.
   - **The design's claims.**
     - It states this partner "is released by the probe at 190 s" (J33, measured only at τ = 0).
     - F12 says the posture must not be held more than 4 minutes by concern answered in his own code.

**No concrete failure found** in the other areas, with notes:
- **(1) Correlated non-written channels.** The causal slope of the posture on every written channel is 0. What his realistic co-activations (brow with cheek, depressor, chin) produce is the declared pooled appraisal R40′. Its level is bounded by |P_c,k| ≤ c_k on BI, BO, TILT, HP and LP.
  - The pooled *slope* is not bounded (it grows as his own brow spread shrinks), so it should be declared as a level, not as slopes.
  - Gaze and blink are written multiplicatively and are outside the level row.
  - Three letter-of-the-rule points: the glare reads his gaze; R_p lists BRE while D_s must not; tracker crosstalk is untested. All are attenuate-only or conditional.
- **(1b) The probe as a dial or oscillation.** It can only end the posture. I found no oscillation: after a release the "rise ≥ 0.05 above its minimum" rule prevents re-onset. Its failure is finding 1, a latch, not a dial.
- **(2) The 0.80-s laugh echo.**
  - A constant delay changes no slope at the metric's 0–3 s best lag, and no route copies at 0.80 s.
  - Context now differs sentence by sentence, which raises the gated slopes back toward their ungated values. BU_L reaches 0.46–0.53 c against a declared ≤ 0.42 c; LP is ≤ 0.31 c and CR ≤ 0.35 c. This is an accounting correction; everything is under c.
  - **Timing.** The smile echo now starts 0.80 s after his smile onset. That is inside the first second but at its late end. Human zygomatic reactions separate at 0.4–0.5 s (Dimberg and Thunberg 2012).
- **(3) The learned gate on the play laugh.** It is attenuate-only (g ≤ 1) and reads none of his LP or CR. The play laugh is triggered by his words (T). No copy route and no dial.
- **(4) Per-channel totals, 2 s to across sessions.**
  - LP, CR and BU_L: ≤ 0.53 c on every measured window (§3).
  - BI, BO and LP from the posture: causal ≤ 0.10, 0.03 and 0.05 (author's J32, reproduced by construction). Pooled R40′ is bounded in level by c_k.
  - Across sessions: unchanged from critique 7's T3 (0.25–0.26 c). D_s is reset per session, and H^p_id is knowing only.
- **(5) Uncounted items.** The gaze and blink modulation of the posture (§2.2); BRE in R_p; the glare's gaze term. None carries copying above a ceiling.

---

## 1. The probe does not release answering concern with a lag (medium)

**Mechanism.**
- **What the probe tests.** After 180 s of face-only hold it halves the posture's target for 8 s. It releases if the mean of his V_p over the probe's last 4 s is below 0.8 × its mean over the 3 s before.
- **What a lagged answer does.** If his answering face follows the agent's look through a first-order lag τ, the fall he can show inside that 4-s window is roughly 0.5·(1 − e^{−6/τ}) of the answer, before his own 3-s smoothing.
  - τ = 5 s: about 0.35 at most;
  - τ = 15 s: about 0.16;
  - τ = 30 s: about 0.09.
- **The result.** At τ ≥ 5 s the fall is below the 20 % criterion. Every probe reads "held", and the probe is the only thing that can end a face-only hold that stays above the release floor.

**Evidence (P1, the author's Agent8; his sadness V 0.8 in his own code until 40 s, then his own code at V = μ × lp_τ(posture shown); 15 min):**

| Code | μ 1.0, τ 0 (author's P4b–d) | μ 1.0, τ 5 s | τ 15 s | τ 30 s | τ 60 s | τ 90 s |
|---|---|---|---|---|---|---|
| operator (agent-like) | probe release 190.5 s | held 15 min; probe 0.989 → 0.866 (−12 %) | held; −5 % | held; −3 % | held; −1 % | held; −1 % |
| quiet 0.3 | release 190.5 s | held; −12 % | held | held | held | held |
| different channels | release 190.5 s | held; −12 % | held; −5 % | held; −3 % | held; −1 % | held (posture 0.33) |

- **In every "held" row:**
  - four probes at 182.5, 370.5, 558.5 and 746.5 s, all "held";
  - posture on 100 % of the time after 60 s;
  - last 2 min: posture 0.94 (0.33 for different channels at τ 90), agent BI +0.188 to +0.234.
- **At μ 0.6 the loop is not self-sustaining.** It releases at 66–286 s in every code, sometimes after a held probe (operator and quiet codes at τ 5–15: released at 231 and 285.5 s by the 20-s rule).
- **Genuine steady sadness with natural fluctuation is not released by chance** (P2: 24 runs, OU SD 0.05 and 0.10, τ 10 s, three codes: one onset each, all probes held, on 100 %). So the probe's specificity is fine; its sensitivity covers only τ ≈ 0.

**Why it counts.**
- **D78, condition 4.** After his own distress ended, the pair settles into a held state that both sides sustain: the agent's look of concern and his matching sad face, which in the operator's code includes a raised inner brow (≈ +0.47 raw against the agent's +0.23).
  - Critique 6's P4 was this state with an instantaneous answer. The design counted it as a failure and closed it with the probe.
  - A lag of a few seconds, slower than his own face's 3-s smoothing, is ordinary for a felt response. Critique 7's slow mirrors used τ 90–240 s.
- **The design's own falsifier F12 is met.** F12 says: "concern answered in his own code holds it more than 4 min". J33 and §2.10 say the answering partner "is released by the probe at 190.5 s in all three codes". That is true only at τ = 0.
- **What it is not.** It is not a copy of his written channels: the posture's part is still independent of his BI, BO and LP. It is a held mutual-expression latch, which D78 treats as disqualifying.

**Fixes** (any one; I have not run them, so each needs its check):
1. **A probe matched to slower answers.** Hold the softening longer when the first window is ambiguous: soften to half for up to 30–60 s, ending early if his evidence falls by ≥ 20 % against a lag-matched baseline, and release if it does.
   - The cost to state: a genuinely sad, silent person sees a half-strength look for up to a minute every few minutes, unless an early "held" is allowed once his evidence has clearly not moved after 30 s.
2. **Accumulate the probes.** Release when successive probes show a fall of the same sign above a small threshold (for example ≥ 3 % in each of three probes; P1 shows −12 %, −5 % and −3 % at every probe at τ 5–30 s), and require that genuine fluctuation does not produce it (P2 gives the null).
   - The cost: about 9 min before release, and τ ≥ 60 s still escapes.
3. **Bound the face-only hold in time.** After N minutes of face-only hold (no words, no sobs), cap the grade at its minimum 0.35 until words or sobs renew it. This needs no contingency estimate.
   - The cost: a silent, steadily sad person gets a lighter look after N minutes. The bid for words already comes at 27–60 s.

Whichever is chosen, extend J33 with lagged answers (τ 5, 15, 30, 90 s) at μ 1.0.

## 2. Correlated non-written channels (area 1): declared appraisal, no copy route

**Causal.**
- R_p ∩ W_p = ∅ (J31). The paired runs in J32 change the posture part by 0.000.
- In real faces, co-activation (inner brow with lip depressor, chin raise and cheek in sadness) makes his written channels *correlate* with what the posture reads. Changing his written channel alone still changes nothing. So no realistic correlation can make the posture depend on his brow.

**Pooled (R40′).**
- **The values.** Over his sadness the agent's BI correlates with his BI: declared 0.69 (operator), 2.05 (quiet) and 0.43–0.52 (σ_id at the floor), all far above c_BI 0.20.
- **Why this is not copying under D83.** It is appraisal of his non-brow face, voice, sobs and words, with a fixed vector. The posture part of BI is ≤ 0.20 in *level*, so the agent never moves its brow by more than the ceiling, whatever his brow does.
- **What to declare.** The slope is unbounded: it equals 0.20 Δa divided by his brow change, so a person whose brow barely moves gives any number. Declare R40′ as the level bound (≤ |P_c,k| ≤ c_k per channel) and drop the slope column, which invites the wrong reading.

**Not covered by that level row.**
- **Gaze and blink.** The posture also multiplies the agent's gaze-away by (1 − 0.5a) and its blink rate by (1 − 0.3a). These are not |P_c,k| entries, so "|y_p,k| ≤ |P_c,k| ≤ c_k on every channel" is not shown for gaze.
- **Direction.** In every declared case the change is *away* from his direction: he averts his gaze when sad, and the agent holds its gaze on him. A partner who looks *more* at the agent when distressed would see the agent's gaze-away fall with his, by at most half of the agent's own gaze-away at that moment (≈ 0.05–0.15 in the scenarios; c_HG 0.03 lateral).
- **What it is.** Appraisal with causal slope 0, not copy. It should be in R40′'s declared list and in the level row.

**Letter-of-the-rule points** (no copy route; fix the text):
1. **The threat silencing reads his gaze.** glare₃ = BL · LT · gaze-at, and gaze is in W_p ("nothing in its onset, grade, release or probe reads any channel in W_p").
   - It only attenuates the load. Its effect on the agent's gaze runs opposite to his: his gaze at the agent ↑ → posture ↓ → the agent's gaze-away returns.
   - Fix: state the exception in rule 9′ (the threat reflex's own input, attenuate-only).
2. **BRE in R_p versus rule 11′.**
   - §2.1 lists BRE (the breath sound, a gated-group channel) in R_p. D_s is "V_p … with LP and CR also removed", so by the text D_s reads his BRE, which rule 11′ forbids.
   - The code is clean: the 3-s face `f3` carries no BRE, and Π̃₀ maps BRE only to activation, giving V 0. In the build, though, H^p_id could learn a positive BRE weight from crying, and then his big laughs (BRE 0.3) would raise D_s for 10 minutes and close the echo.
   - That is attenuate-only, but it would mute ordinary laughter after laughter. Fix: remove BRE from R_p, or from D_s's input.
3. **Tracker crosstalk (conditional, untested).**
   - If the face tracker leaks his inner-brow raise into a read channel (lip depressor, brow lowerer, chin raise) with coefficient κ, then a brow-only partner drives the posture again at a gain proportional to κ, times the quiet-user calibration factor (up to ×4).
   - I cannot measure κ here (no data).
   - F18's steering test clamps his *feature* BI, which leaves the leaked component in place, so it would not detect this.
   - Fix: a week-0 check on the operator (pose the inner-brow raise alone and read R_p). Drop a channel from R_p for that user if its leak exceeds the level that would bring the brow-only slope to c_BI.

**Fitness note (for the agent critic, not a copy route).**
- In the code, R_p is always read as an unvoiced face (`posture_read(..., False)`). Speech articulation raises the tracked chin raise, lip press and depressor.
- If the calibration baseline excludes speech frames, a calm talker could start the posture. The design does not say how his visemes are handled in the posture's reading.

## 3. The 0.80-s laugh echo, the sentence-level gate and the totals (areas 2 and 4)

**No route copies at 0.80 s.**
- The delay is a constant on the gated group. The pointwise bound 0 ≤ y ≤ g G_k u(t − 0.80) holds (R1s, W′ check: max block excess +0.0000).
- Unknown words only close the gate. His laughter tokens are removed before the gate. The look-ahead λ_w reads his later words, never his laugh.

**But the gate is now correlated with each laugh, not with minutes.**
- §3.3 says the timing change "keeps the gate's per-episode values". It does not: the gate now reads the sentence that each laugh ends.
- Critique 7's T2 showed that a gate lower where his level is lower raises a slope. A partner whose laughs after troubles sentences are smaller than his ordinary laughs (Jefferson's troubles laughter) now has exactly that, laugh by laugh.

**R1s** (6 h, his sentences 3 s, a laugh after a share of them; the gate 0.99 after an ordinary sentence and 0.05 after a troubles sentence, as J36). Totals are in c_k, shown as ungated / revision 7 (previous sentence) / revision 8 (current sentence):

| His laughs | LP 2 s | CR 2 s | BU_L 2 s | BU_L 10 s | BU_L 1 min |
|---|---|---|---|---|---|
| 30 % troubles, same size | 0.34 / 0.26 / 0.25 | 0.35 / 0.25 / 0.25 | 0.49 / 0.35 / 0.34 | 0.45 / 0.34 / 0.32 | 0.43 / 0.37 / 0.36 |
| 30 % troubles, half size | 0.31 / 0.23 / 0.30 | 0.34 / 0.24 / 0.32 | 0.49 / 0.34 / 0.46 | 0.46 / 0.34 / 0.46 | 0.45 / 0.37 / 0.47 |
| 50 % troubles, half size | 0.31 / 0.19 / 0.27 | 0.34 / 0.18 / 0.29 | 0.50 / 0.26 / 0.43 | 0.47 / 0.26 / 0.45 | 0.46 / 0.32 / **0.49** |
| 30 % troubles, 0.3 size | 0.32 / 0.24 / 0.31 | 0.35 / 0.24 / 0.34 | 0.51 / 0.35 / 0.50 | 0.48 / 0.35 / 0.49 | 0.47 / 0.42 / **0.51** |
| R1s-x: 80 % troubles, 0.2 size | 0.27 / 0.13 / 0.26 | — | 0.51 / 0.12 / 0.49 | 0.49 / 0.15 / **0.53** | below floor |

**Verdict.**
- Every total is ≤ 0.53 c. The sentence-level gate returns the slope to about its ungated value: it never exceeds the ungated value by more than 0.04 c.
- No ceiling is crossed, and Claim W′ (the level bound) holds exactly.
- **Accounting.** The declared R1g row (≤ 0.42 c BU_L, from critique 7's episode-scale gate) is too low. Replace it with ≤ 0.53 c BU_L, ≤ 0.31 c LP and ≤ 0.35 c CR at 2 s to 1 min, or with the ungated values, which bound these to within 0.04 c.

**D81 timing (no failure).**
- D81 asks for fast, partial matching. The design's smile echo (LP, CR), not only the laugh, now starts 0.80 s after his onset, and its lip peaks at +0.90 s.
- **Against human data.**
  - It is inside the first second, where Mauersberger 2022 finds context-set laughter mimicry.
  - It is late against rapid facial reactions: zygomatic responses separate at 400–500 ms (Dimberg and Thunberg 2012). Half of their 500–1,000 ms scoring window would show no agent response.
- **Option (not required).** A silent smile with no pending words could keep 0.45 s.
  - At 0.45 s, an echo of frame s reads words ending ≤ s + 0.25 s only if the recogniser's latency is ≤ 0.20 s. Otherwise it reads the words through s, and those are delivered once the latency has passed. That keeps the gate's information.
  - The delay would then depend on voice activity, a timing input that T1 must count.
- **Timing mismatch inside one laugh.** His laugh's head and voice-contour components still echo at 0.45 s, ungated. So at a grieving person's nervous laugh the agent's head can bob (HP ≤ G_HP = 0.08) with no smile. That is within c_HP; it is a fitness point.

## 4. The learned gate on the play laugh (area 3): no route

- **What triggers it.** The play laugh is triggered by his words: his riff on the agent's line, its surprise. The amplitude is 0.40 · band · (0.35 + 0.65 π) × g.
- **Inputs.** π is the agent's own play history. g ∈ [0, 1] reads his masked 20-s face (no LP or CR; the code's `f20` carries no BRE, BU_L or RHY), his words, the agent's own face and words, and D_s.
- **What it can do.** The gate can only lower the laugh. It cannot make the agent laugh because his face laughs.
- **Pooled correlation.** The agent's laugh at his joke correlates with his own laugh at it. That is a T route (appraisal of words, as in revisions 4–7), and the gate can only lower it.
- **Shadow.** The shadow holds g at factual values, so the ledger does not treat the gate's dependence on his face as partner-caused. Since it is attenuate-only, nothing is missed.

## 5. Across sessions and anything else not counted (areas 4 and 5)

- **Across sessions.**
  - D_s is reset per session. H^p_id is learned nightly on his words, knowing only, and on channels the posture does not write.
  - The gated fast lip pull's session-mean slope is unchanged in form from critique 7's T3 (0.25–0.26 c). The per-sentence gate changes within-session correlation, not session means.
- **Not counted, and should be listed:**
  - the posture's gaze and blink modulation (§2);
  - BRE in R_p (§2.2);
  - the glare's gaze term (§2.1);
  - the speech-viseme question (§2, fitness).
- **Rule 12′ holds in the code.** Own words reach only `LVo`.
- **The Seamless specification items are consistent with the runtime alignment.** Words end ≤ onset + 0.25 s; same normaliser; 30-Hz onsets.

## 6. Verdict

**The design is not yet free of concrete copying failures, narrowly.**
- The contingency probe that replaced the face-only failsafe catches answering concern only when the answer is instantaneous.
- With the author's own full-strength answering partner and a lag of 5–90 s, the agent's concern look and his own sad face hold each other for the whole session in every code: posture 0.94, agent brow ≈ 0.19–0.23, his inner brow ≈ +0.47 in the operator's code. That is an attracting mutual state, and the design's own F12 is met.
- A longer or cumulative probe, or a time cap on face-only hold, closes it, and the check is J33 with lagged answers.

**Everything else holds:**
- The posture is causally independent of every channel it writes.
- No mirror on those channels holds it.
- Genuine fluctuating sadness is not released by chance.
- The 0.80-s echo adds no copy route.
- The gate on the play laugh is attenuate-only.
- Per-channel totals stay ≤ 0.53 c on LP, CR and BU_L, and within the declared causal bounds on BI, BO and LP.

**Text to correct:**
- R1g's declared numbers (≤ 0.53 c BU_L);
- R40′ declared as a level, with gaze and blink included;
- BRE removed from R_p or from D_s;
- the glare's gaze read stated as an exception to rule 9′;
- a week-0 tracker-crosstalk check added to F18.
