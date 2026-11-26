# Check of the Cayley–ledger revision 9 (build core): the audit of situation-specific rules

Independent checker, 2026-11-26T21:21:23Z

**Standard:**
- questions.md Q29 (no situation-specific rules), and the operator's answers under Q24, Q26, Q27 and Q28.
- DECISIONS.md D70, D78 (condition 4), D81, D83, D85, D88, D89 and D90.
- Innate parts are allowed only for the body, reflexes, newborn muscle patterns and per-expression copy ceilings. Situational appropriateness may come only from Claude's regulation path, from learning on recorded human dyads (movement features only, no labels), and from general innate learning biases.

**Read:**
- design-cayley-ledger.md, revision 9 (all of it: the audit, the mechanism text, §3.11, the Build core summary);
- design-cayley-ledger.r8.3.md §2 and the parts it inherits by reference: .r7.md §2.1–§2.15, .r6.md §2.1–§2.13 and §3.11, .r5.md §2.1–§2.9, .r4.md §2.1 and §2.9;
- sims/design-g9/ (both scripts and outputs), sims/design-g7/checks.py `ledger7`;
- research/seamless-interaction.md (what the corpus holds, and the loader allowlist).

**My checks:** `sims/check-cayley9/ledger_margin.py`, with outputs `ledger_margin.out.txt` (κ 0.80, 166 s) and `ledger_margin070.out.txt` (κ 0.70, delay 240 s, 66 s).
- The script reuses `ledger_lag120.py`'s definitions and partners verbatim, as `ledger_lag300.py` does, with revision 9's 61 constraints per channel.
- It changes one thing: the ledger enforces κ·c instead of c, the same on every channel and every constraint.
- Constructed partners: these runs test the mechanism, not people. Nothing is left running.

## Verdict: FAIL

There are three concrete failures, each with a fix that adds no situation-specific rule:

1. **The audit missed a situation-specific rule that is still in force: the softened follow-up.** It speaks 1.5 s after an unanswered question from the agent, once per silence, detected by a punctuation rule.
   - It is defined in r4 §2.1 and §2.9, kept by r5 §2.9 and r6 (§5: "follow-up"), and inherited by r7, r8.3 and revision 9 through "as revision 5/6/7".
   - Revision 9 says that "constants of revisions 5–7 stand unless removed in the audit" (§2.1), and nothing removes it. So it stands.
2. **Under D70, several "learned from recorded dyads" replacements cannot be fitted.** Seamless `FAUValue` holds 24 facial action units only: no head pose, no gaze, no audio. The loader allowlist is `FAUValue`, `is_valid`, transcript and VAD.
   - Among the behaviours revision 9 sends to source 2 are the turn-end nod (S33), the concern face's head tilt (L_d's TILT, HP and VG), the attentive head (S29), and head and voice accommodation (S30). Revision 9 also sends the gaze and head cues of turn-taking (S36) and the cross-entry sign prior on head, gaze, voice and audio-laugh channels (S32).
   - None of these has a corpus target. Those channels fall back to the hand-written signed synergies, and that fallback still contains rule J ("−1 across joy and sadness").
   - So item 5 of "No allowed source" is understated, and S32 is only partly removed.
3. **The safety net does not hold the per-expression ceiling.**
   - The author's own runs leave an unlisted copy delayed 10–120 s at 1.03–1.20 c, and one delayed 150–240 s at 1.17–1.34 c. F22 is written to accept up to 1.25 c.
   - A uniform margin closes this. With the ledger target at 0.80 c, delays of 10–120 s come out at 0.94–0.99 c; with it at 0.70 c, a 240-s delay comes out at 0.94–1.02 c. In both runs the counted routes change on 0 frames, so D81's fast mimicry is untouched.

The rest holds:
- Every REMOVE item is gone from the mechanism text.
- No counted route is opened.
- D78-4 holds: every new learned part is frozen and trained on strangers.
- D81's fast partial mimicry is kept, at 0.45 s on every channel.

## 1. Completeness of the audit: rules the audit missed

The audit's 50 rows are accurate as far as they go, and its counts are right (32 removed, 18 kept). The rules below are in r8.3 or are inherited by it, and are missing from the table.

| # | Rule (where) | What it is | Should be |
|---|---|---|---|
| M1 | **Softened follow-up** (r4 §2.1 "softened follow-up: 1.5 s of no partner voice after the agent's own question (punctuation rule on its own text); one per silence"; r4 §2.9 item 2; r5 §2.9 "as revision 4 (… softened follow-up …)"; r6 §5) | a timer for one event type, an unanswered question; it calls Claude and speaks | **REMOVE.** The dyad-learned silence hazard can take "the speaker's last turn ended in a question" as a transcript feature (S2), and the follow-up becomes part of the one speak-or-wait choice. Revision 9 §2.9 should say so explicitly, and the punctuation rule should be deleted from the assembly list as well. **Concrete failure (Q29).** |
| M2 | **Gaze following in the reflected frame** (r5 θ₀; r6 §2.1 "(r5)") | the agent's gaze follows his | KEEP as a **reflex**, and list it. Its gain is inside the head and gaze group's two-sided fast budget (0.80 c). |
| M3 | **Own head micro-motion gated down by his 2.6–6.5 Hz head envelope** (r5 θ₀, chosen to produce signature C1; r6 §2.1) | the agent keeps still while his head moves | KEEP as a **reflex** (attenuate-only), but list it. It is a hand-set innate coupling, introduced to reproduce one human signature. |
| M4 | **Audio onset → blink** (r6 R5 and R8) | startle blink | KEEP as a **reflex**, and list it. S44's startle-orient is a different reflex. |
| M5 | **Relief–distress opponent masking R′ = max(0, R − 3 S)** (r4/r5 "masking") | relief is not shown while a distress event co-occurs | S22 removed only the second factor, × max(0, 1 − 𝒟_p/0.05). This first factor is general (no situation named), so KEEP it as a **body** rule, but list it. |
| M6 | **Driver of the activation row: A_L ← max(A_L, 0.5 s_lex²), τ 3 min** (r5) | his surprising words raise the agent's lids and outer brow | S45 keeps the row; its driver should be listed as well, as **body** (the agent's own surprise at content). |
| M7 | **Rule 7 (phrase targets read h, C_L, E, f_id, A_L, envelopes)** (r5 §2.2) | voice targets | Not updated. C_L and f_id lost their display rows (S27, S28), but rule 7 still names them, and it does not name L_d, whose RT output therefore has no stated path to the voice. Fix the text. |
| M8 | **The signed-synergy fallback of the sign mask** (r5 §2.5: "−1 across joy and sadness"), kept in revision 9's assembly list | rule J, written by hand | On every channel the corpus cannot supply (head, gaze, voice, BU_L, RHY, BRE), the fallback is S32's hand rule unchanged. List it as "S32, partly kept", or ask the operator (§5). |

Borderline items, not failures:
- **S41's loud-voice branch, f_loud(1 − 2 f_pos)₊.** The exception for laughter and Duchenne smiles was added to fix critics' "loud praiser" and "loud teaser" cases. The glare branch is a clean reflex; this branch is a hand-made discrimination. It can stay as part of "what a threat display is", but the audit should say why it was added.
- **The hand-set values in kept or new parts:** S38's thresholds (word care 0.05, V̂ 0.20), K_id's e(t) (spoken in the last 60 s), β = 4, the trace τs and |L_d,k| ≤ 0.45. None names a situation. They are acceptable as body constants or general biases.

## 2. Every REMOVE item is gone from the mechanism text

I searched lines 98–540 (§0–§9) for every removed symbol:
- δ_g, λ_w, π, m_s, d_b, θ_C, θ_I, P_c, T_max, V_v, H^p, R_p, ω_sym, p_end;
- the play-structured rule, familiarity, the flash, the nod, the halving, rule J, sensitization, the squint drop, D_s, c_L.

Every hit is a statement that the item is removed or replaced (§0 move 1, §2.1 "Removed constants", §2.2, §2.4.2, §2.10, §3.11 R40′/R27′/R1w, §3.15). §2.10 and §2.4.2 are struck through, and their text is only in `.r8.3.md`. **This item passes.** The exceptions are things the audit never listed (M1, M7, M8).

## 3. The KEEP items: do they belong to an allowed category?

Most are correctly placed:
- the reflexes: S41, S42, S43, S44;
- the body items: S21, S26, S47, S50;
- the general biases: S13 (fitted directions), S15 (multi-scale traces), S38, S39, S40, S48;
- the learned or Claude parts: S16, S49.

Three need a plain judgement.

**S46: the ban on learning anger, disgust and contempt displays.** This is not a per-expression *copy* ceiling. It forbids the agent's own expression in every situation, whatever the partner does.
- It names no situation, so it is not a Q29 violation of the "timer or gate" kind. But it fits none of the four allowed innate categories.
- "Newborn" does not justify it either: newborns show a disgust face to bitter taste, and an anger-like cry face.
- Copy safety does not need it. The zero toward ceilings on BL, LT, NW, LPR and DIM already block copying those channels.
- Its purpose is to stop the agent learning a scowl through its own legibility pressure (r5 H4: weight 0.22 drifted onto the masked synergies without it). That is a design choice about the agent's character.
- **Verdict:** it belongs to the operator. The author did put it under "Choices left to the operator", which is the right handling. The audit row should read "operator's call", not "KEEP: ceiling". I agree with the author's recommendation to keep it.

**S45's own-distress row (BI +0.45, LD +0.35, lower voice), driven by S_n, the rises of his word need 𝒟_p(N_L).** This is the largest built-in face response to his words of trouble that remains. Its brow is larger than the removed word-concern row's BI +0.25.
- It is T-only, so it is not a copy route.
- Its trigger is a general drive change (any rise of the agent's own care load), not a named situation.
- It is the agent's own reactive distress, shown as a brief envelope: rise 0.4 s, apex to 1.5 s, decay τ 3 s. Newborn reactive crying to another's cry is a known innate response.
- **Verdict:** allowed. But the summary should tell the operator plainly that a built-in brief distress brow at his words of need remains, since D89 removed a built-in concern face.

**S43, the fast gains and the pooled shares.** These are per-expression settings inside the ceilings, and they are allowed. The inner brow's special trace share (0.5, 0.5, 0, 0) is justified by "sadness is held". It is a per-expression choice, not a per-situation one, so it is acceptable.

## 4. Copy routes, D78-4, D81 and the ledger residual

**No copy route is opened.** Each change in §3.11 is a deletion, an attenuate-only learned part, or a T-only learned part. I checked every one:
- g ≤ 1 under the pointwise bound g G_k u_k(t − 0.45 s), including fitted positive cross terms.
- g_o never reads his face. His face reaches it only through the agent's own face, which the shadow sees.
- L_d and q̂ read T only.
- The counted routes change on 0 frames under the extended ledger (N2, N2b, and my K2).
- D78-4 holds: every dyad part is frozen and trained on strangers, and ω is covered by Lemma S\*.
- D81 holds: the echo is at 0.45 s on every channel.

**The residual above c is a concrete failure of the per-expression ceiling as the safety net states it.**
- §3.3 says "held … to about c_k", and the summary table says "≤ about 1.2 c_k". The ceiling is innate and is not "about".
- The residual arises because the 2-s window scans lags only to 3 s, while the critics' block metric is evaluated at the copy's lag.
- §0 move 4 says the residual is "the same as its zero-lag case". It is not. The zero-lag residual is 0.36–0.37, that is 1.03–1.06 c. The lagged residual is up to 0.42, that is 1.20 c, and up to 1.34 c at 150–240 s.
- F22's threshold of 1.25 c writes the overshoot into the acceptance test.
- It concerns only routes nobody has listed, which is exactly what the net is for, so it cannot be waived.

**The fix: one uniform margin.** The ledger enforces κ c_k on every channel and every constraint. This is part of the ceiling structure and names no situation.

| Uncounted gain-1 copy, delay L | Ledger at c (author) | κ 0.80 | κ 0.70 |
|---|---|---|---|
| 5-min mood blocks, L 10 / 90 / 120 s | 1.20 / 1.20 / 1.17 c | 0.99 / 0.99 / 0.99 c | — |
| 30-s blocks, L 10 / 90 / 120 s | 1.17 / 1.17 / 1.14 c | 0.95 / 0.96 / 0.94 c | — |
| L 240 s (5-min; 30-s blocks) | 1.34; 1.23 c | 1.12; 1.05 c | 1.02; 0.94 c |
| counted routes (fast gear + held route), frames changed | 0 | 0 | 0 |

Grow and flip are 0.000 in every row.

Two costs, which the author should state:
- Below the counted routes' sup-gain total of 0.974 c_k, the ledger *can* bind on counted routes for an extreme partner. It is attenuate-only, so the ceiling still holds; what would shrink is mimicry. On the natural partners it changed 0 frames.
- Alternatives are to scan the 2-s window at lags (more constraints), or to use κ 0.8 together with a wider 60-s scan.

F22 should then read "> c_k". A route delayed beyond 300 s remains outside the scan, and that should stay listed.

**A related point, not a failure: L_d can carry the speaker's expected face through his words.**
- Recorded listeners partly mimic speakers. A map from words to listener faces therefore learns the part of the speaker's face that the words predict.
- |L_d,k| ≤ 0.45 is above c_k on BI, LP and RT, and only the falsifier F23 measures this.
- Suggested fixes, neither situation-specific: make F23 a gate before day 1 on held-out Seamless people, or fit L_d's target with the speaker's concurrent same-channel movement regressed out.

## 5. The six "no allowed source" behaviours

| Item | Stated accurately? | Must it go to the operator? |
|---|---|---|
| 1. A concern look before words | Yes. The inner brow is ≤ c_BI × his deviation (≈ 0.10), about 0.05 in practice. A dyad-learned face → face map would be a copy route and stay under the ceiling anyway. | No: D89 is his answer. |
| 2. Gladness in the first 2–3 s of a mourner's arrival | Yes, given that g_o must not read his face. One option is worth checking before calling it "no source": a per-session latched T value from his earlier sessions' words (allowed by T1(c)) as a g_o input. Its weight cannot be fitted on Seamless (no prior sessions), so this may indeed fail. | It belongs in the risks, as stated. Not a question. |
| 3. The recognition brow flash | Yes. BO is in FAUValue, so it can be learned if openings exist. | No. |
| 4. A 0.2–0.5-s chuckle at a bad-news sentence-final laugh | Yes (word delivery 0.6–0.75 s against an echo at 0.45 s). | No: Q29 named the word-wait gate for removal. |
| 5. Anything from voice sound | **Understated.** FAUValue has no head pose and no gaze either. Also lost, or left on hand fallbacks: the turn-end **nod** (S33 claims "none once fitted"), the concern face's **head tilt**, the **attentive head** (S29), head and voice **accommodation** (S30), **gaze and head** cues in turn-taking (S36, §6.7 item 6), and the sign prior on head, gaze, voice and the audio laugh channels (S32). | **Yes, as a real question.** Widening D70 is the operator's alone. Nods and turn-taking are core to a conversational agent. Ask whether Seamless's head and gaze movement and audio prosody may be read, under D70's other restrictions. The "Choices left" bullet on audio should become a question in questions.md and include head and gaze. |
| 6. Relationship strengths that differ by group | Yes. | No. |

## 6. The Build core summary

Mostly accurate. These need correcting:
- **Day 1, "nods":** they cannot be learned from FAUValue, so remove them or make them conditional on the operator's answer (§5).
- **"Innate, and nothing else":** omits the softened follow-up (M1, to be removed), gaze following, the head micro-motion gating and the startle blink (M2–M4).
- **The ledger risk:** "a residual of about 1.2 c" is a failure of the ceiling, not just a risk. Replace it with the κ margin (§4).
- **§0 move 4:** "the same residual as its zero-lag case" is wrong (1.20 c against 1.06 c).
- **"Choices left to the operator":** S46 correctly. Audio should be widened to head and gaze, and asked as a question.
- **Day 1 sympathy:** say plainly that "its own brief distress at his need" is an innate brow of up to +0.45, so that it is not read as the learned concern face.
- Day 1 and after learning are otherwise stated fairly. The "weakest point" (everything situational rests on unfitted Seamless parts) is honest.

## Corrections required for a pass

1. Add M1 (the softened follow-up) to the audit and remove it. Add M2–M8 as KEEP rows or text fixes.
2. Re-state which S2 replacements are fittable from 24 facial AUs plus transcripts. Move the head, gaze and voice items to "No allowed source" and mark S32's fallback as rule J kept. Put the D70 widening to the operator as a question.
3. Hold the ledger at κ c_k (κ 0.80; 0.70 if 150–240-s delays must also be ≤ c), and set F22's threshold at c_k. State the cost: possible binding on counted routes at the extreme.
4. S46: change the audit row to "operator's call". Keep it in "Choices left".
5. Make F23 a gate before day 1, or residualise L_d's target on the speaker's same channel.
