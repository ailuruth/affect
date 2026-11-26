# Check of the Cayley–ledger revision 9.1 (build core): the narrow fixes of check 9

Independent checker, 2026-11-26T21:35:12Z

**Standard:**
- questions.md Q29 (no situation-specific rules); the operator's answers under Q24, Q26, Q27 and Q28; the open questions Q30–Q32.
- DECISIONS.md D70, D78 (condition 4), D81, D83, D85, D88, D89 and D90.
- Innate parts are allowed only for the body, reflexes, newborn muscle patterns and per-expression copy ceilings. Situational appropriateness may come only from Claude's regulation path, from recorded human dyads (movement features only, no labels; under D70, 24 facial action units and transcripts), and from general learning biases.

**Read:**
- check-cayley-ledger-9.md;
- design-cayley-ledger.md: the audit table (rows S1–S50, M1–M8, Counts, "No allowed source"), §0, §2.9, §2.13, §3.3, §8.1, F22, "Check of revision 9 and the answer", "Revision 9.1 history", and the Build core summary;
- sims/design-g91/ (the author's script and output), sims/design-g9/ledger_lag120.py and ledger_lag300.py.

**My checks:** `sims/check-cayley91/ledger_close.py`, with outputs `*.out.txt` in that folder.
- The script reuses `ledger_lag120.py`'s definitions and partners verbatim, as the author's `ledger_margin.py` does.
- It takes the margin κ, the scan, the delays and the partners as arguments.
- Scan `base` is revision 9.1's 61 constraints. Scan `w10` adds the 10-s window at lags 125–300 s in 5-s steps, which gives 97 constraints.
- Each run took 18–143 s. Nothing is left running.
- Constructed partners: these runs test the mechanism, not people.

## Verdict: FAIL

There is one concrete failure, and it has a uniform fix:

1. **The 0.70 c ledger does not hold the per-expression ceiling across the delays it scans.**
   - The author measured only 10, 90, 120 and 240 s, and reports a single 2 % excess, at 240 s.
   - At κ 0.70, on the same 5-min mood-block partner, an unlisted gain-1 copy delayed by these amounts is left at:

     | Delay | 150 s | 180 s | 210 s | 240 s | 300 s |
     |---|---|---|---|---|---|
     | Residual | 1.043 c | **1.072 c** | 1.010 c | 1.02 c | 1.046 c |

     Only 270 s stays below c, at 0.986 c.
   - All of these delays are inside the 300-s scan that the design says it covers. The Build core summary says the 60-s window to 300 s "holds 150–240-s delays too". That is false.
   - The ceiling is innate and exact (D83), and check 9 already ruled that a residual above c on an unlisted route is a failure of the safety net, not a risk. So a 2–7 % excess is a concrete failure, though a small one.
   - A lower margin does not close it. At κ 0.68 the 240-s case is 1.025 c; at κ 0.65 it is still 1.006 c.
   - The cause is structural. The 2-s window is constrained only at lags 0–3 s, and the 10-s window only to 120 s. Beyond 120 s, only the 60-s window acts, while the ceiling is read by the 2-s block metric at the copy's lag.
   - **The fix:** scan the 10-s window to 300 s, in 5-s steps. The rule is the same attenuate-only rule on every channel and every lag, and it names no situation (see Evidence).

Everything else holds:
- **The softened follow-up is gone.** Rule J is gone. Head, gaze and voice sound are nowhere claimed as dyad-learned.
- **No copy route is opened.**
- **D78-4 holds.**
- **D81 holds:** the fast echo stays at 0.45 s, and 0 frames of the counted routes are changed.
- **The cost to counted routes is stated:** the ledger may trim them for an extreme partner, attenuate-only.

## 1. The three failures of check 9

**(a) The softened follow-up is closed.**
- It is removed in audit row M1, §2.9 ("the only follow-up … is removed in 9.1") and §2.14's assembly list. The punctuation rule and the 1.5-s timer are deleted.
- What replaces it is a transcript feature of the dyad-learned silence hazard: whether the last turn ended in a question, and whose turn it was (§2.1 table, §6.7 item 6). Its weight is fitted. It is one input to the general speak-or-wait choice, not an event timer, so it is allowed (S2).
- I found no other text that still defines a follow-up.

**(b) Head, gaze and voice under D70 are closed.**
- I searched §0–§9 for nod, tilt, gaze, accommodation, pitch, prosody, audio and head pose.
- Every hit either says "no dyad source under D70", or describes a reflex (gaze following M2, head-motion gating M3, the threat glare-away, startle-orient).
- L_d now fits BI, BO, LD, LP and CR from facial action units, and RT from transcript word timing. TILT, HP, VG, FR and EN are held at 0. The turn-end predictor and the hazard read word timing, syntax and the 24 facial action units only (§6.7 items 4, 6 and 7).
- Rule J is removed from the fallback (S32, M8): the fallback keeps within-synergy signs only, and cross-synergy pairs are unsigned and charged to the cross budget.
- The loss is stated: nothing innate stops a learned joy-sign cross entry from his sadness on the head, gaze, voice and laugh-sound channels, and it stays under the cross budget.
- Q30 is with the operator.

**(c) The ledger margin: closed for 10–120 s, not for 150–300 s.**
- At κ 0.70 the author's figures reproduce: 0.85–0.88 c at 10–120 s, and 1.02 c and 0.94 c at 240 s.
- Within the scanned range, the 5-min partner exceeds c at 150, 180, 210, 240 and 300 s (Verdict, item 1).
- The 30-s partner stays below c at 150, 180, 240 and 300 s (0.86, 0.945, 0.94 and 0.90 c).
- F22 as written covers only 10–120 s, so F22 itself passes. But the summary, §0 move 4, the §3.3 totals table and §8.1 item 7 all imply ≤ c, or ≤ 1.02 c, out to 240–300 s, and that is not what the runs show.

## 2. Situation-specific rules in disguise

**The built-in brow of up to +0.45 at his words of need (S45) is not situation-specific. It is allowed.**
- Its driver is S_n, the rises of the agent's own care load 𝒟_p(N_L) and its hurt. N_L comes from the learned population reader, and its input is T-only (E1, r5 §2.13). It never reads his face, so it is neither a copy route nor a face-triggered posture.
- The chain "the partner's need raises my care load, and my own distress shows the newborn cry-face row" is the same in every situation. No word class, scene or timer is named in it.
- It is the agent's own brief distress (rise 0.4 s, τ 3 s). Newborn reactive crying makes it a defensible newborn-pattern item.
- **Advisory, not a failure.** In practice it puts a built-in inner brow larger than the removed concern row (+0.45 against +0.25) on the agent's face exactly when he speaks of trouble. That is close to what D89 took out.
  - The summary now says this plainly, as check 9 asked.
  - I recommend that it also be put to the operator explicitly, for example as a line in Q32 or beside Q31: "keep the agent's own brief distress brow at his words of need, or scale it down". If he reads D89 broadly, he may not want it.

**Relief masking by the agent's own distress (M5, R′ = max(0, R − 3S)) is acceptable as body.**
- It is an opponent interaction between the agent's own appetitive and aversive events. It reads no channel of his and no word class, and it acts the same at any co-occurrence.
- The author admits that in practice it partly reproduces S22, the removed "no relief shown over his distress". That is because S includes rises of 𝒟_p(N_L).
- That reproduction is a consequence of a general body rule, not a rule written for that scene. Opponent motivational interactions, with aversive events dominating, are a standard body-level assumption.
- The factor 3 is a hand-set body constant. It should be listed with the other body constants. That is not a failure.

**Nothing else kept in 9.1 is situation-specific.**
- M2–M4 and M6 are general reflexes or body items.
- The question feature in the hazard is a fitted input.
- S46 is correctly labelled the operator's call (Q31).

## 3. Copy routes, D78-4, D81 and the stated cost

- **No copy route is opened.** 9.1's changes are four:
  - deletions: the follow-up, rule J, and the L_d head and voice targets;
  - a fitted transcript feature, which feeds timing only;
  - unsigned cross-synergy fallback entries, which are cross-channel, inside the existing cross budget ≤ s_X c_k, and not same-channel toward entries;
  - a lower ledger target, which is attenuate-only.

  Grow and flip are 0.000 in every one of my runs.
- **D78-4 holds.** Every learned part is still frozen and fitted on strangers. Nothing in 9.1 adds an online learner on a path to the face.
- **D81 holds.** The fast gear stays at 0.45 s. Counted routes (the fast gear plus a held 2-min route at 0.22 c) have 0.000 frames changed on both partners at κ 0.70 and 0.65, and at κ 0.70 and 0.80 with the w10 scan.
- **The cost is stated in four places:** §2.13 "The cost (9.1)", §8.1 item 7, the Risks of the Build core summary, and 9.1 history row 3. It reads: for an extreme partner the ledger may trim counted routes, fast mimicry included, attenuate-only, because their sup total is 0.974 c, above 0.70 c.

## 4. The Build core summary

It is accurate except on these points:
- **"Choices left: … holds 150–240-s delays too"** is false at κ 0.70. The figures are 1.04–1.07 c at 150–180 s, 1.01–1.02 c at 210–240 s, and 1.05 c at 300 s.
- **Risks, "The ledger … 0.94–1.02 c at 240 s"** is incomplete. It should read "up to 1.07 c at 150–300 s". The same applies to §0 move 4, the §3.3 totals row ("≤ 1.02 c_k at 240 s"), §2.13 ("every other measured case is ≤ 0.94 c"), §3.3 Claim O‴ and §8.1 item 7.
- **"Innate, and nothing else"** omits the own-display mask (S46). It is still in force pending Q31 and is listed under "Choices left", so this is minor, but the innate list should name it as "kept pending the operator".
- The rest is fair:
  - day 1: no nods, no head tilt, the built-in +0.45 distress brow stated plainly, and the follow-up at the corpus's timing;
  - the learned-parts table: correct D70 inputs;
  - "What it no longer does";
  - Q30 and Q31;
  - F23 left open as a risk.

## Evidence (sims/check-cayley91/, partners as revision 9: 2 h, lip pull, c 0.35, seed 910)

Worst block-mean slope over lags 0–300 s at the 2, 10 and 60-s windows, as a ratio to c. Grow and flip are 0.000 everywhere.

| Unlisted gain-1 copy, delay L | Partner | 61 keys, κ 0.70 (9.1) | κ 0.68 | κ 0.65 | **97 keys (10-s window to 300 s), κ 0.70** | 97 keys, κ 0.80 |
|---|---|---|---|---|---|---|
| 10 / 90 s | 5-min | 0.88 / 0.87 (author) | | | **0.883 / 0.870** | |
| 120 s | 5-min | 0.87 (author) | | | | 0.995 |
| 150 s | 5-min | **1.043** | | | **0.870** | |
| 180 s | 5-min | **1.072** | | | **0.869** | 0.978 |
| 210 s | 5-min | **1.010** | | | **0.850** | |
| 240 s | 5-min | **1.02** (author) | 1.025 | 1.006 | **0.848** | 0.944 |
| 270 s | 5-min | 0.986 | | | **0.847** | |
| 300 s | 5-min | **1.046** | | | **0.836** | 0.946 |
| 150 / 180 / 240 / 300 s | 30-s | 0.860 / 0.945 / 0.94 / 0.897 | | 0.867 (240 s) | **0.845 / 0.863 / 0.846 / 0.833** | |
| counted routes, frames changed | both | 0.000 | | 0.000 | **0.000** | 0.000 (5-min) |

Files:
- `k070_scanlags.out.txt` and `k070_scanlags30.out.txt`: 61 keys at κ 0.70, other delays.
- `k068_240.out.txt` and `k065_240.out.txt`: lower margins.
- `k070_w10_*.out.txt`: the w10 scan at κ 0.70.
- `k080_w10.out.txt`: the w10 scan at κ 0.80.

## Corrections required for a pass

1. **Ledger.** Add the 10-s window at lags 125–300 s in 5-s steps, the same attenuate-only rule on every channel. Keep κ 0.70.
   - **Measured:** every delay from 10 s to 300 s is held at 0.83–0.88 c on both partners, with 0 frames of the counted routes changed.
   - **Cost:**
     - 97 constraints per channel instead of 61, about 1.6× the ledger's compute.
     - No new memory: the 10-s window means are already kept for 300 s (§2.13's 0.8 MB).
     - On mimicry, the same stated cost as now: possible trimming for an extreme partner.
   - **A gentler alternative:** κ 0.80 with the same scan holds 0.94–0.995 c at 120–300 s, with almost no slack. It trims counted routes less often at the extreme, because 0.974 c is closer to 0.80 c, but the case for κ 0.70 is the margin it leaves.
   - **Not a fix:** lowering κ alone (0.65 still gives 1.006 c).
2. **Text.** Restate the ledger residual in §0 move 4, §2.13, the §3.3 table and Claim O‴, §8.1 item 7, F22 (extend it to 10–300 s at 1.0 c) and the Build core summary, using the new figures. Delete "holds 150–240-s delays too" unless correction 1 is adopted. Routes delayed beyond 300 s stay listed as unscanned.
3. **Summary.** Add S46 to "Innate, and nothing else" as "kept pending Q31".
4. **Advisory, not required.** Put the built-in +0.45 own-distress brow at his words of need to the operator explicitly, in Q32 or beside Q31, given D89. List M5's factor 3 among the body constants.
