# Check of the Cayley–ledger revision 8.1 fixes

Independent checker, 2026-11-26T16:01:29Z

Standard: questions.md Q19 (concrete failures only), D78, D81–D85, and Q24 (open; the design follows its recommendation). Scope: only the revision 8.1 fixes (the face-only cap, the squint drop, the text corrections, and the Build-candidate summary).

Checks: `sims/check-cayley81/check.py` (C1–C5, output in `out.txt`) and `check_b.py` (C1b, output in `out_b.txt`). Both load `sims/design-g81/checks.py`'s engine and `Agent81` unchanged and skip its K1–K5 loops. The engine takes about 4 min to load; the runs take 1–2 min.

## Verdict: FAIL (one medium failure, the same kind as routes critique 8's finding 1 but narrower)

The squint fix works and opens no copy route. The text corrections hold. The face-only cap releases the critic's partner at every lag from 0 to 90 s, as K1 shows. **But a partner who answers the agent's concern more slowly, with a time constant of about 5 min or more, holds the look indefinitely.** So does a stronger answerer at 2–3 min. Because the cap doubles, the tests come further and further apart while the hold continues. Under D78 condition 4 this is a hold the agent settles into: the mutual concern state that routes critique 8 called attracting. It is still there, only at slower lags. The doubling also makes the failure worse.

## Evidence

### 1. The face-only cap

**The author's partner leaves out the slow answerers.** In K1's `run_answer`, his lagged trace starts at 0 at t = 0. When his genuine sadness ends at 40 s, his face therefore drops straight to μ × (a trace that has barely risen). For τ ≥ about 150 s that drop releases the look through the 20-s rule. This is an artefact of how the partner is built, not the cap working. With τ 300–600 s and the same start, my C1 runs release at 63 s in both codes. A person whose distress continues into his answer has no such drop. C1b starts his trace at his sadness level and otherwise uses K1's partner unchanged. Results over 60 min, operator code and different-channel code (identical outcomes):

| His answer (low-pass of the look) | Tests (start s, ratio, outcome) | Look on, 50–60 min | Agent BI, last 10 min |
|---|---|---|---|
| μ 1.0, τ 150 s | 242.5 held 0.75; 782.5 follows 0.50 → released 902.5 s | 0 % | −0.005 |
| **μ 1.0, τ 300 s** | 242.5 held 0.87; 782.5 held 0.71; 1862.5 held 0.71 | **100 %** | **+0.235** (diff. ch. +0.189) |
| **μ 1.0, τ 600 s** | held 0.93, 0.84, 0.84 | **100 %** | +0.234 |
| **μ 1.2, τ 240 s** | held 0.84, 0.71, 0.74 | **100 %** | +0.238 |
| μ 1.5, τ 120 s | held 0.92; follows 0.60 → released 902.5 s | 0 % | −0.005 |
| **μ 2.0, τ 180 s** (C1, start at 0) | held 1.0, 1.0, 1.0 | **100 %** | +0.238 |
| **μ 3.0, τ 90 s** (C1, start at 0) | held 1.0, 0.90, 0.90 | **100 %** | +0.238 |

- Each test gives the same ratio every time, because the partner's decay over a 120-s lapse is fixed. The next test would come at about 63 min and the one after at about 2 h, so these holds do not end.
- The release threshold of 0.70 at a 120-s lapse catches a low-pass answer only if τ is below about 260–300 s. This matches the author's own late-phase τ 240 s case, ratio 0.65; τ 300 s gives 0.71.
- The design itself treats 90–240 s contagion as a realistic partner time scale (J33's S1). An answering distress that decays over 5 min is one step beyond that, not an exotic partner. The same family at gain 2–3, saturating his face, holds at τ 90–180 s. J33 used mirror gain 3 as a test partner, so gain 2–3 is within the design's own range.

**Pure delay** (C2: his face = μ × the look d seconds earlier). This is less realistic, so it is a note, not the failure.
- d ≤ 30 s: one release.
- d = 90 s and 150 s: an endless on/off cycle. There are 7–10 onsets in 30 min and the look is on 85–91 % of minutes 20–30. The 20-s rule ends each cycle, but the sensitized re-onset (0.5 s) restarts it when his delayed answer arrives.

**A partner who learns the cap's timing, or answers only after a test.** This is not a failure. To keep the look he must keep his read distress up through every lapse. That is steady distress independent of the agent's look, and it is not a mutual loop. A partner who answers only after the look returns drops while it is on, and the 20-s rule releases it.

**Is the doubling a new problem?** Yes. A passed test pushes the next one to 13, 31, 67 … min. Two things follow:
- a slow answerer is effectively never tested again;
- a chance pass becomes a long hold. The author's own noisy 90-s answerer held until 17.4 min.

Revision 8's fixed 3-min probe at least kept testing at the same rate.

**The cost to genuine distress** (C3, 60 min of steady silent sadness, all three codes): tests at 4, 13 and 31 min, no release, look withdrawn 266 s of 3600 (7 %). Over the first 15 min it is 154 s (17 %), as K3 says. As stated, I find this acceptable as a fitness cost, not a concrete failure:
- it applies only to wordless, sob-free distress, since concerned words or sobs reset the count;
- by then the agent has already bid in words.

But the operator is not told about it (see the summary corrections below).

**Possible fixes** (not checked here):
1. Do not double the cap; keep testing every 4–8 min.
2. Make the test cumulative across lapses. For example, release if two consecutive ratios are both below about 0.85. P2's single-test minimum is 0.82, so this needs a specificity check.
3. An absolute face-only limit (for example 20–30 min without words or sobs), after which re-onset needs a rise above his minimum (revision 7's rule). This ends any slow answerer, at the cost of a long wordless grief.
4. Declare the limit to the operator under D78/Q24 and restate F12 beyond 90 s. In any case, §2.10's "Every such hold ends" and the summary's "released … including when he has only been answering the agent's own look" are false as written.

### 2. The squint drop

- **K4 reproduced.**
  - Grief with a squint, looking at the agent: 0.99 in the operator and quiet codes, 0.50 for a different-channel user.
  - Every listed anger and concentration face: 0.00.
- **No copy route reopened.**
  - The squint drop touches only his BL and LPR. The posture writes neither, and both are read only after attenuation toward his rest.
  - The glare's gaze input is the one written channel the posture reads. It can only lower the load toward what he would get looking away, so the agent's gaze-away stays within the declared level row, gaze × (1 − 0.5a). The gaze route is narrower than in revision 8, which removed the whole load.
  - C5: a different-channel user who frowns or squints and follows the agent's gaze (his gaze-at = 1 − look, with a 3-s glance away) never starts the look in 15 min.
- **Narrow side-effect (fitness, not copy):** anger mixed with lip depressor or chin raise. The squint drop keeps LD and CHR, which is why grief with a squint works, so some angry faces now get the full look (C4, 180 s):
  - Anger + LD 0.3 → 0.99 in every code (revision 8: 0.00 / 0.33 / 0.33).
  - Anger + CHR 0.3 + LD 0.2 → 0.99 in every code (revision 8: 0.00).
  - Anger + CHR 0.4 (a canonical anger component) → 0.99 in the quiet code only. It is 0.00 for the operator's and the different-channel codes.

  This is the cost of the squint fix's trade-off: grief with a squint and a sulky, pouting anger share LD and CHR. It should be stated beside the "half look" cost and added to the risks. I do not count it as a concrete failure: no rule is broken, and showing concern at a downturned-mouth frustration face is defensible.

### 3. Nothing else broken

- **Per-channel totals.** The R1g declaration (≤ 0.31 c LP, ≤ 0.35 c CR, ≤ 0.53 c BU_L) agrees across §0.6, the bound table, §3.3 (Correction 8.1) and §3.11. Claim W′ (the level bound) is unchanged. The old figure of 0.42 c survives only in the record of the revision-7 critiques, which is historical.
- **Laugh-gate timing.** δ_g = min(1.0, ℓ_p90 + 0.25) agrees with ℓ + λ_w ≤ δ_g. So do the finalised-through requirement (F(s + δ_g) ≥ s + λ_w, else gate 0), the 0.75-s operator threshold and the summary's "0.8–1.0 s". The only change is the stricter requirement on the recogniser, which only closes the gate.
- **K5:** D_s does not read BRE.
- **Stale mentions of "probe"** for a mechanism 8.1 removed (text only): §0 move 1 (J34 line), rule 9′, §2.14, §2.15, the §3.6 posture row ("probe ends any answering hold"), §3.12 P2/P6, §3.14, §6.1, §10, and the summary's novelty list, lesion list and Live list.

### 4. Build-candidate summary: accurate except for these corrections

- **The one-line description, novelty verdict (recombination), Q24 options, brow-only trade-off (about 50 s; about 110 s for a quiet face), echo timing (0.8–1.0 s, against a person's 0.4–0.5 s) and one line per option** are present and match the body.
- **Correct:** "released when his distress ends, including when he has only been answering the agent's own look". Change it to: "…released when he answers it within about 4 min; a person whose distress is sustained by the look over 5 min or more keeps it (see the risks)". Alternatively, fix the mechanism.
- **Add (the cap's cost):** during wordless, sob-free distress, the look is withdrawn for 60 s after 4 min, then for 120 s at about 13 and 31 min. That is about 155 s of the first 15 min and about 4.5 min per hour. The summary's "a steady look" omits this.
- **Add:** a different-channel user whose grief is mostly brow lowerer gets a half look (0.50) when he squints at the agent. Angry faces with lip depressor or chin raise can get the full look.
- **Replace** "The probe (answering concern latches)" in the lesions with "the face-only cap (answering concern latches)". Replace "how often the probe releases genuine sadness" with "how often the cap's test lapses withdraw the look at genuine distress". In the novelty list, "a perturbation probe" can stand as a generic description, or become "a withdrawal test".
- **Add to the risks:** hold durations against slow answerers (time constant 2–10 min) and the growing gap between tests.
- **Echo timing:** consistent. The sound comes about 0.03 s after δ_g and the lip peaks about 0.1 s later (§2.4.2), so the stated range is fine.
