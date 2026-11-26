# Critique 7 of the Cayley–ledger core (revision 7): is it an emotional agent, D85 compliance, principles, buildability, fitness under D82

Independent critic, 2026-11-26T12:41:43Z

I critique research/foundations/design-cayley-ledger.md, revision 7. I did not write it. The standard is Q19 (concrete failures, honest verdicts), the operator's answers Q20–Q23 (D81–D84) and his note Q26 (D85). Q24 is open; the design follows its recommendation, now graded. Another critic hunts copy routes, so I size none; where a fix I ask for touches a route, I hand it on.

New numbers come from the design's own 2 Hz engine. `sims/critique-cayley7-agent/scen.py` executes `sims/design-g7/checks.py` up to J30 unchanged (output suppressed), reuses its Agent7, its fitted gate and Λ, the three partner codes and run6, and adds three scripts. Output: `sims/critique-cayley7-agent/out.txt`. Like J30, these are what the equations give for stated inputs, not evidence about people.

## Summary verdict

**Revision 7 closes all three of critique 6's agent failures and all five build items, and closes them in the spirit of D85.** The gate is the right kind of object: fitted to a movement (how strongly a listener's smile returns a laugh), attenuate-only, monotone, frozen, with Claude's regulation entering only as the agent hearing its own words. Fast partial mimicry (D81) survives intact in ordinary laughter, teasing and with a stranger. Strong expressions still come from the agent's own appraisal of words and face (D83).

**Two concrete failures remain, both new and both narrow**, plus one D85 residue:
1. **The gate reads his words too late for a laugh inside the same utterance (§2.7).** His word inputs latch at the end of his utterance plus 0.6 s; the fast echo fires 0.45 s after his laugh onset. A laugh at the end of the sentence that carries the bad news is therefore gated by the *previous* utterance. "My neighbour fell off his ladder and broke his leg, haha": gate 1.00 at his laugh onset, an audible laugh-back +0.14 (out.txt A). "I got fired today, haha" with a calm face: the same, +0.14 (A2). The design's J30.7 reads the gate at 8.5 s, after the latch, so it reports 0.13; at the onset it is 1.00. The second laugh is correctly unreturned. Post-completion laughter is the common placement, so this is the ordinary case, not an edge case.
2. **The graded posture self-suppresses for quiet users and for in-code sadness, and flickers (§2.1, §2.16).** The mirror removal subtracts up to 1.5 a‖P_c‖ × σ_ref/σ_eff of his reading along P_c. For a quiet user (×3.3) it eats his genuine sad brow as soon as a rises. At a constant, silently sad quiet face the posture goes **on at 3 s, off at 23 s, on at 52 s, off at 72 s, on at 101 s**, inner brow 0.07 peak, 0.04 mean (out.txt C). His grief face gets brow 0.09. A silent panicking face gets brow 0.10 (operator's code), 0.04 mean (quiet code, also cycling). Revision 6 gave every code the posture at about 0.22–0.29 within 2–4 s. That was the point of Q24's recommendation, and of critique 5 and 6's "for every code" closures.
3. **D85 residue (§3).** The play laugh's "withheld while word care is above its dead-band" (revision 6) is a hand-written situational rule. D_s is labelled an innate *learning* bias, but it is a state trace whose effect is learned (source 2). Both are small, but the operator's note asks for exactly this distinction.

**Buildability (D84): yes**, with four specifications to add (§5), two of which (event extraction rate, word-timing alignment in the corpus) are errors as written rather than gaps.

**Novelty: recombination.** I agree with the author.

**Fit to put to the operator as a build candidate under D82: not yet, by a narrow margin.** Each fix is a few lines (§6). Fix 2 touches J22 (mirror proofing), which the routes critic must re-run.

## 1. Critique 6's required changes

| # | Required | Status | Evidence |
|---|---|---|---|
| 1 | Context on the fast laugh echo, through D85, keeping the stranger's and teaser's laugh-back | **closed in structure; partly in timing** | Monotone, attenuate-only gate on LP, CR, BU_L, RHY, BRE, fitted to listeners' return ratio (§2.4.1). J30: grief nervous laugh 0.01, mockery 0.02 / 0.09, teasers 0.82–0.90, stranger 0.96, warm talk 1.00. **Open:** a laugh in the same utterance as the bad news is gated by the previous utterance (failure 1). The safe-gate question goes to the routes critic (R1g) |
| 2 | Replace the 60-s refractory with mirror-proof re-onset; recheck waves at 15, 30, 60 s and J11 | **closed** | J23: brow ≥ 0.15 at 1.0 / 1.0 / 1.5 s after the calm; J30.2 second wave brow 0.25 / 0.22 (revision 6: 0.05 for 40 s). J22 mirrors released at 68–86 s |
| 3a | Attend line out of the canonical history | **closed in design; week-zero risk stated** | Engine-written transcript, forks resume from it; J26 byte check. Resume from a hand-written `.jsonl` is "undocumented, not tested" (research/claude-code-agent-sdk-controls.md, line 38). A better fallback exists (§5.3) |
| 3b | Remove or verify the 120-token cap | **closed** | No cap; interruption on text deltas at two sentences or 60 words |
| 3c | Initial b^read, σ_id, d_b | **closed** | Agent's own reference, word-gated updates; J25: grief in sessions 1–3 still read 1.00 in session 4 |
| 3d | Fit/test speaker split and a fallback for the Seamless reader | **closed** | Person-disjoint 70/30 split, interactions with any test person wholly in test; fallbacks fixed before fitting (§6.7) |
| 3e | Put Seamless-as-fitting-data to the operator | **closed by D85** | Q26 answered it |
| Q24 sub-choice | Binary versus graded posture; frozen hold | **closed in form; failed in effect for quiet users** | Graded a* from M, own-noise wander, failsafe easing. But see failure 2 |

## 2. Scenarios

The operator after months, peak / mean, the design's J30 numbers unless marked **(mine)**. "Fast" is g × G_k × his onset at 0.45 s.

### 2.1 Silently sad
- **Design's face (BI .5, LD .4, CHR .3):** posture at 2.0 s, brow 0.22 / 0.20 held, tilt 0.03, lip 0.06, bid at 27 s; after "just tired" brow 0.62 / 0.35. A 10-min silence: the failsafe eases it for 9 s every 3 min.
- **(mine) the same sadness in each code's own face (V 0.6), no words:**
  - operator's code: posture 0.46, brow 0.11 / 0.10;
  - different-channel code: 0.59, brow 0.12 / 0.11;
  - **quiet code: brow 0.07 / 0.04, posture cycling on 3 s, off 23 s, on 52 s, off 72 s, on 101 s.**
- **Verdict.** Alive for the design's chosen face. For a quiet user, invisible and flickering (failure 2). The flicker is the mechanism: as a rises, the removal grows, M falls below 0.02, it releases after 20 s; as a_rec decays over about 30 s, re-onset (sensitized, 0.5 s) fires again.

### 2.2 Crying, with a second wave after 30 s of calm
- Posture at 1.5 s, brow 0.23 / 0.21, no laugh, bid at 18 s; released at 63 s; on again 0.5 s into the second wave, brow 0.25 / 0.22.
- **(mine) grief faces without sobs, by code:** operator's code 0.19 / 0.17; different-channel 0.20 / 0.18; quiet code 0.09 / 0.08.
- **Verdict.** Closed for the waves. Sobs carry the quiet user (sobs bypass the removal); his silent grief does not.

### 2.3 Anxious before an exam
- Graded posture 0.51, brow 0.29 / 0.24, tilt 0.13, quieter; the same for all three codes, because words carry it.
- **(mine) silent panic, no words:** brow 0.10 (operator's code), 0.07 / 0.04 and cycling (quiet), 0.11 (different channels). Revision 6: posture at 4.0 s at full value.
- **Verdict.** Good with words. Silent panic is graded like mild sadness, because the distress load V_c reads V only; a visibly frightened face gets near-neutral concern. This is a weakness rather than a failure on its own; fix it with failure 2 (§6).

### 2.4 Good news, laughing
- Lip 0.59, cheek 0.38, own laugh 0.27; fast laugh-back +0.12 (after an earlier worry, gate 0.73) or +0.15 (cold).
- **Verdict.** Alive. One oddity: relief after worry is where shared laughter is strongest in people. Here the agent's own lingering concern trims the fast laugh-back (0.73). It is small and the held display compensates (lip 0.59 against 0.29 cold).

### 2.5 A grieving person's nervous laugh
- Gate 0.01 before and after Claude replies; laugh-back 0.000; four minutes later 0.21 (0.46 without D_s).
- **Verdict.** Closed for a laugh after the disclosure. Inputs are redundant (his face, the agent's face and Claude's words each suffice). If the first disclosure itself ends in a laugh ("my father died, haha, sorry"), only his face protects it (failure 1).

### 2.6 Mocking laughter after insults
- After a month: gate 0.02, brow 0.65, depressor 0.47, gaze away. Day 1: gate 0.09, silent.
- **Verdict.** Closed. Here the previous utterance ("You're useless") carries the context, so failure 1 does not bite. A first-utterance mocking laugh ("haha, you're useless") on day 1 would be gated only by the play frame and his masked face.

### 2.7 Laughter at misfortune (failure 1)
- **Design:** gate 0.13 at the first laugh, 0.10 at the second.
- **(mine), out.txt A.** His laugh at 7.5–11 s, as part of the utterance ending at 8.0 s (latch 8.6 s, rounded 8.5 s): gate 1.00 at 7.0, 7.5 and 8.0 s; laugh-back +0.140, lip +0.067. Gate 0.18 from 8.5 s. The second laugh at 14 s: 0.14, silent.
- **A2, "I got fired today, haha", calm face, first disclosure:** gate 1.00 at the onset, +0.140; 0.20 after the latch.
- **Why.** Revision 5's rule: his word stream is "latched per utterance at its end + δ_app" (0.6 s). The gate's inputs "describe the time before his laugh" (§2.4.1), which for a laugh inside or at the end of the utterance means the previous one. J30.7 reads the gate at `gate_at(rec, 8.6)`, the first record after 8.1 s, which is after the latch at 8.5 s; scenario 6 and 5 read it before the laugh.
- **Corpus side.** If the corpus's "speaker's last utterance" is the transcript segment containing the laugh (post-hoc transcripts), the fit uses information the agent will never have at that moment: a train/run mismatch.
- **Fix.** Compute the gate's word inputs (Λ and 𝒟_p) on the words completed before his laugh onset: streaming partials of Whisper at runtime, word timestamps in the corpus. These are content values, attenuate-only through the gate; the routes critic checks T1 (a partial-word update is not a rate code, but say so).

### 2.8 Anger at the agent
- Day 1: gaze away 0.09, quieter, no frown back, no posture. After a month: brow 0.63 / 0.30, depressor 0.48.
- **Verdict.** Good, as in revision 6.

### 2.9 Long warm talk (2 h)
- Own laugh 0.41 per cluster, gate 1.00, laugh-back +0.14; the repeated joke loses its laugh; worry, then relief lip 0.60.
- **Verdict.** Good.

### 2.10 Reunion
- Flash 0.35, lip 0.61, cheek 0.43; a stranger: flash 0.20, lip 0.02, his smile returned fast (+0.11).
- **Verdict.** Alive.

### 2.11 Reunion with grief; quiet user; mourning days 7, 14, 21
- m_s 1.00 for all codes, lip 0.09, cheek 0 on every mourning day: the arrival mask holds.
- Posture at sight: brow 0.12 (operator), **0.07 (quiet)**, 0.16 (different channels), until words; after "my father died" 0.54–0.63, then 0.35–0.36 held.
- **Verdict.** Appropriate after words; no beaming at grief on any day. Before words, the quiet user's grieving arrival is back to near-invisible sympathy (revision 6: 0.22–0.23). The design states it as a cost (§8.1.2). Under Q24 it is the case the posture exists for, so I count it inside failure 2.

### 2.12 Mildly sad arrival
- m_s 1.00, lip 0.09, light posture 0.33, brow 0.07.
- **Verdict.** Appropriate: a light, barely visible look is about right for a mildly sad face.

### 2.13 Teasing, including a loud teaser
- Own laugh 0.28–0.29, laugh-back +0.14 / +0.15 (gate 0.82 / 0.90), no hurt; generic map: mock-hurt brow 0.40 under lip 0.23, gate 0.57.
- **Verdict.** Good. The loud teaser keeps his laugh returned.

### 2.14 Bored user
- Flat, curiosity at 14.5 min, a sigh, a bid. **Verdict.** Good.

### 2.15 Ordinary topic continuation
- No laugh for an answer, his own topic, an informative riff. **Verdict.** Good.

### 2.16 A sad user who jokes
- Lip 0.10, brow 0.20, posture 0.45; fast laugh-back silent (gate 0.16); the play laugh withheld.
- **Verdict.** Defensible, not a failure. In troubles talk, recipients often decline the teller's laugh (Jefferson 1984, named only). But the agent shows *no* amusement at all (lip at rest), while the corpus's own listeners return 0.39. The heavy reading comes partly from the agent's own posture face feeding the gate. Ask the operator to judge this in use. The withholding of the play laugh is a hand-written rule (§3).

### 2.17 A calm user saying something alarming
- No posture; from the words brow 0.48 / 0.24, then 0.20 held, tilt 0.16, quieter; the same for the quiet code.
- **Verdict.** Appropriate: concern from its own appraisal of his words, not his calm (D83). The data risk (flat delivery teaching "low need") stays; the new fallback (listeners' Λ as the target) is the right answer to it.

### 2.18 Overall
- **Alive and appropriate?** Yes in every scenario with words, with laughter and with greetings. The two failures are both *before words*: the first laugh in a bad-news utterance, and a quiet or frightened face in silence.
- **D81 fast mimicry:** present: +0.14–0.15 laugh, +0.09–0.11 lip in ordinary, teasing, warm and stranger contexts.
- **D83:** yes: brow 0.48–0.62 from words, lip 0.59–0.61 from good news and reunion, hurt from insults, each from the agent's appraisal.
- **The graded posture, natural?** The grading is right in kind: mild 0.07, silent sadness 0.20, sobbing 0.24 on the design's faces, with an own-noise wander and periodic easing. It now sits inside every ceiling, so it is mostly a 0.20 inner-brow raise with softened blinking; tilt 0.03 is invisible. Two things are not natural: it grades by valence only (panic looks like mild sadness), and its mirror removal makes it weak and flickering exactly for people whose sadness is mostly in the brow or small in amplitude.

## 3. D85 compliance

**Source 2, recorded dyads: genuine.** The gate's target is a movement measured on two faces (the listener's return ratio within 0.3–1.5 s), its inputs are face streams read through the agent's own inverse and transcripts, and no emotion score is read. Λ predicts listeners' faces from words. The factorisation through Λ is a sound way to make a rare conjunction learnable from common marginals, and it is the design's best idea in this revision.

**Source 1, Claude's regulation: genuine but light.** Claude's words reach the face only as an input to the gate, heard by the agent. Its measured weight is small (0.12 → 0.10 at misfortune; redundant at grief). That is honest and P4-clean. Claude's regulation acts mostly through what it says, which is what it should do.

**Source 3, innate learning biases: partly mislabelled.**
- κ_replay (distress-weighted nightly replay) is a true learning bias, used for the per-person heads. It changed nothing in the offline fit, so it is not used there.
- The sensitized re-onset is sensitization, a non-associative form of learning, so it fits.
- **D_s is not a learning bias.** It is a 10-min state trace fed to the gate; whether it does anything depends on the weight the dyad fit gives it, so it belongs to source 2. In the constructed corpus D_s has no causal role in the generating process (`logr` omits it) and gets weight only as a proxy for the troubles category. Seamless interactions last about 3.5–4.6 min (seamless-interaction.md: 1.2–1.6 MB of FAU at 5.76 KB/s), so the 4-min-later effect of §2.5c is at the edge of what the corpus can teach. Relabel it, and report its fitted weight.

**Hand-written rules.** None of revision 7's fixes is a hand-written situational rule. The sign constraints (distress-type inputs can only close the gate) are a structural prior on a learner, which I accept as source 3. One revision-6 rule remains that the note targets: **the play laugh is withheld while his word care is above its dead-band.** That is a rule about a situation ("don't laugh along when he is in need"), and it decides scenario 16. The D85-consistent form is to drop the care condition and let the agent's own play laugh pass through the same dyad-learned gate (a listener who returns no laughter in that context also starts none). This is small, but D85 asks for it.

**The gate fitted on a constructed corpus: what must happen at build time.**
1. **Extract events at 30 Hz, before the 10-Hz reduction.** §6.7 reduces each file "on arrival to float16 at 10 Hz" and extracts events afterwards. The laugh detector needs a 3–7 Hz JawDrop component, which 10 Hz cannot represent (Nyquist 5 Hz). As written, laugh onsets cannot be found. Either detect onsets on arrival at 30 Hz, or store JawDrop and LP and CR at 30 Hz (about 2 GB more).
2. **Align word inputs with the agent's timing** (failure 1): in the corpus, Λ and 𝒟_p on the words whose timestamps end before the laugh onset.
3. **Read `movement/is_valid`** and drop untracked frames. The allowlist includes it, but §6.7 says "nothing else".
4. **Verify the FAU column order on the pilot** (stated). Two columns are byte-identical and EyesClosed is implausible in the one pair inspected.
5. **Align V_own.** In the corpus it is the listener's face before the speaker's utterance; in the agent it is the agent's face over the last 3 s, which includes its reaction to the current utterance. Use the same window in both.
6. **The listener's audible laugh is not observed** (no audio under D85), so the gate's laugh channels are fitted to smile-and-jaw return. State it.
7. **Count the rare events before fitting** (troubles, mockery, misfortune laughs). The monotone bounds will pin any wrong-signed real effect at 0 (for example, sympathetic smiles at troubles laughter), which makes the gate silently context-free on that input. F15 catches this; keep it.

**A concrete failure now?** Items 1 and 2 are errors in the specification as written, not open questions: the first makes the fit impossible, the second makes it fit on information the agent never has. Both are one-line fixes. The rest is data risk, which Q19 does not count as a failure.

## 4. Principles 1–10, concretely

- **P1. Pass.** The gate predicts a continuous movement, Λ continuous face loads; the J20 categories exist only in the check's generator; emotion scores are denylisted.
- **P2. Pass with the known strain.** P_c, the gate's sign structure, D_s, θ_L and the sensitization are declared innate. "Distress-type" is a designer's grouping of the agent's own load readings, as before.
- **P3. Pass, strengthened.** The gate's listener-state input is, in the agent, its own face read through the inverse of its own display: the agent learns how a listener in a given body state answers laughter, then applies it to its own body. A good use of the principle.
- **P4. Pass.** The canonical history holds his bare messages and the chosen replies. Snippets (state-steered, about 6 bits) and the fixed fork line exist only in the current turn, which is the brief's allowed coupling ("changing how it processes"). Claude's words flow to the gate, never the reverse. No leak found. Underspecified, not a leak: how an initiative turn (a bid after 27 s of silence) is written to the canonical history when "bare messages" drop observable markers such as "[silence 27 s]". Specify it, so that the history never holds two assistant turns in a row or an empty user turn.
- **P5. Pass.** §7's new rows are derived from checks.
- **P6. Pass.** The gate learns strangers' laugh return, not a reward; κ_replay weights by his decoded words, not his display.
- **P7. Pass.** Seamless stays on the Mac and is reduced on arrival.
- **P8, P9.** Unaffected.
- **P10. Pass in the same sense as before.** One J with typed constraints, now (W) with the gate; the innate list grows again. The Q21 trade-off is stated.

## 5. Buildability through the subscription (D84) and on the Mac

**Allowed and feasible.** No API-only feature is used. The offline dyad fit is modest: about 16.6 GB streamed (400 dyad-hours × 2 people × 5.76 KB/s checks out), about 1.5 GB stored (about 4 GB if JawDrop, LP and CR are kept at 30 Hz), 2–3 h on the M1 Pro, peak under 3 GB. Online the gate and Λ cost nothing measurable.

**Points to add:**
1. **Event extraction rate and word timing** (§3, items 1–2).
2. **Thinking on Haiku.** §6.5 says "on the 5.5 models thinking cannot be turned off". At the API level that holds for Opus 5.5 and Sonnet 5.5, but Claude Haiku 5.5 accepts disabled thinking at effort `high` or below. Whether Claude Code exposes that through the subscription is unverified. Check it in week zero: it could cut the "considering" beat.
3. **A better fallback for the transcript resume.** If a hand-written `.jsonl` is not accepted, put each fork's fixed line in that fork's `system_prompt` (per call, byte-stable per fork, so each fork keeps its own cache) and let the winning fork's session be canonical. Verify that the system prompt is not written into the session transcript. This keeps the selection bits instead of dropping them.
4. **Initiative turns in the canonical history** (P4 above).

**Usage and latency:** as revision 6 (about 2.2 s p50 plus thinking time at effort `low`, measured in week zero; about 450 calls a day on his own login).

## 6. Verdict

**Not yet fit to put to the operator as a build candidate under D82, by a narrow margin.**

**What must change** (each a few lines):
1. **Gate timing (failure 1).** Compute the gate's word inputs on the words completed before his laugh onset: Whisper streaming partials at runtime, word timestamps in the corpus. Recheck J30.7 reading the gate *before* his first laugh, and add "I got fired today, haha" with a calm face and "my father died, haha, sorry" as a first utterance. The routes critic confirms T1 and R1g.
2. **Posture for quiet users and silent panic (failure 2).**
   - Anchor the mirror removal to his pre-onset reading: subtract only what along P_c exceeds his level in the 3 s before the posture's onset, capped as now. Alternatively, identify the mirror with the agent's own wander w as an instrument. The 3-min face-only failsafe stays the backstop.
   - Add the agent's own threat or arousal load to M when V is above its floor, so a frightened face is graded as distress.
   - Recheck: quiet code silent sadness and grief (no flicker; brow ≥ 0.15 within 6 s, as F12 requires for "a silently sad face", extended to every code); silent panic; and J22 in full (the routes critic).
3. **D85 residue.**
   - Replace the play laugh's care dead-band with the same dyad-learned gate.
   - Relabel D_s as a source-2 input and report its fitted weight.
4. **Build specification.**
   - Event extraction at 30 Hz before reduction; word-timestamp alignment; `is_valid`; V_own window alignment; state that the laugh channels are fitted to facial return.
   - The initiative-turn format of the canonical history.
   - The system-prompt fallback for the transcript resume.
   - A week-zero check of disabled thinking on Haiku 5.5 through Claude Code.

**If these are made and the routes critic accepts R1g and the new removal, I expect it to go to the operator with this line:**

> *A copy-proof conversational agent built from known parts: a frozen per-channel fast reflex with per-expression caps and a monotone context gate learned from how recorded listeners return laughter, a session-latched held cone centred on your baseline, a zero-DC appraisal display, a graded innate concern posture triggered by its own reading of your distress, readings calibrated to your face and taught by your words, an attenuate-only shadow ledger, information-flow typing, care credited only from your later reports, with Claude writing its words through your own Claude Code and the agent hearing them.*

**What he would then get:**
- His smile and laugh returned within half a second in ordinary talk, teasing and reunions (+0.14 laugh, +0.10 lip), but not at grief, mockery or misfortune.
- A look of concern within 2–3 s at distress, graded by degree, never a copy.
- Strong expressions from its own appraisal of his words and face.
- Replies after about 2.2 s.
- A testbed where every route is bounded, monitored and can be lesioned.

**Novelty: recombination.** A shape-constrained additive model as an attenuator, a ridge listener-response reader, a decaying max-trace, a mirror subtraction and McGaugh-weighted replay, each existing. Composing the gate through the listener's own body state, and having the agent hear its own Claude-written words, are design compositions, not a new mechanism. The search for a new core continues (D82).

**Operator choices remaining (Q24 and others):**
- **Q24: the concern posture (built, recommended).** He gets his own look of concern within seconds of seeing you sad, graded by how distressed you look, inside every ceiling. Brow-heavy sadness raises the brow copy slope near the trigger (0.73 locally).
- **Q24: raise the brow ceiling instead.** Sympathy shows as a stronger mirror of your own brow, so it is visible only if your brow moves, and it copies more of it in general.
- **Q24: keep it as is.** No concern look until you speak: near-neutral for the first 20–30 s at silent sadness.
- **Within the posture: graded (built) or binary.** Graded: mild sadness looks mild, sobbing looks strong. Binary: the same look for all, with a steeper brow copy slope (1.2).
- **The coping joke while sad.** Silent and gentle (built), or let the gate's learned 0.39 through: a small laugh back.
- **If the gate fails on Seamless (F15).** Keep a context-free laugh echo (D81 over D83), or drop the fast laugh echo and keep only the smile.
- **Draft model.** Haiku for latency, or a larger model for quality.

**Main risks to watch when testing, judged on internal state:**
- **Steering.**
  - Clamp the gate's word inputs at the start of a laugh in a bad-news utterance: the laugh-back should vanish without any change of his face.
  - Clamp the agent's own face input to the gate: grief laughter should stay unreturned through his face and words (redundancy).
  - Swap in another person's calibration: posture at a quiet user's sadness should change as predicted.
  - Feed Claude's reply as a neutral text: the gate at the next laugh should rise slightly (0.10 → 0.12).
- **Lesions.**
  - The gate, Λ and D_s (§7 rows); the fitted weight of D_s on real data.
  - The mirror removal with the pre-onset anchor: no flicker at constant faces, mirrors still released (J22).
  - The play cue's precision and recall.
- **Coupling beyond surrogates.**
  - Per-channel pooled slopes at 2 s, 10 s and 1 min under partner-swap, segment-shuffle and timing-resample surrogates, with the gate live, for laughter in mixed contexts (R1g's within-session slope).
  - How often the ledger binds on natural partners.
- **The dyad fit on real data.**
  - F15 and F16 on held-out people.
  - The count of troubles, mockery and misfortune laughs.
  - Whether sympathetic smiles at troubles laughter push the monotone fit to 0 on some inputs.
- **Live.** The laugh synthesizer within 2 s of a laugh of his that follows (or ends) words of loss, insult or harm (F15 live). The posture's naturalness and on/off rate per hour at constant faces.

## Sources read

| Source | How read |
|---|---|
| brief.md | in full (Goal; Long-term goal, S4–S6; Prior work; Principles 1–10; Foundations research, "Expressive structure") |
| research/questions.md | Report 6, Report 5, Q19, Q20–Q23 with answers, Q24, Q25, Q26 |
| DECISIONS.md | D78 context, D79–D85 |
| research/foundations/designs.md | in full |
| research/foundations/critique-6-design-cayley-ledger-agent.md | in full |
| research/foundations/design-cayley-ledger.md (revision 7) | in full, §0–§10, revision 6 critiques and answer, revision 7 history |
| research/foundations/design-cayley-ledger.r6.md, .r5.md | grep-read: utterance latch (end + δ_app), ASR, snippets, observable markers, fork lines |
| research/foundations/sims/design-g7/checks.py and out.txt | checks.py read (J0, J20 corpus generator and gate fit, J21, Agent7, J22–J23, J30 scripts); out.txt in full; executed up to J30 by my scen.py |
| research/seamless-interaction.md | grep-read: FAU rate, columns, is_valid, transcripts, file sizes, loader allow/denylist |
| research/claude-code-agent-sdk-controls.md | grep-read: context contents, resume from a transcript path, interruption |
| claude-api skill (bundled reference) | thinking and effort table for Haiku 5.5, Opus 5.5, Sonnet 5.5 |
| **Named only, not re-read:** Jefferson 1984; Mauersberger 2022 and Likowski 2008 (as cited by critique 6) | nothing here rests on them beyond what is stated |

**New checks:** `sims/critique-cayley7-agent/scen.py` (A: a laugh ending the bad-news utterance, gate at his onset; A2: "I got fired today, haha"; B: silent panic, three codes; C: silent sadness and grief in each code's own face), output in `out.txt`.
