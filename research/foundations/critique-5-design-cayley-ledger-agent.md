# Critique 5 of the Cayley–ledger core (revision 5): is it an emotional agent, principles, buildability on the subscription, fitness under D82

Independent critic, 2026-11-26T09:11:59Z

I critique research/foundations/design-cayley-ledger.md, revision 5. I did not write the design. The standard is Q19 (concrete failures, not rigor) and the operator's answers Q20–Q23 (D81–D84). Another critic hunts copy routes, so I size no copy route. Where a fix I ask for touches one, I say so and hand it on.

Extra numbers come from the design's own 2 Hz engine. `sims/critique-cayley5-agent/scen.py` executes `sims/design-g5/checks.py` unchanged (output suppressed) and reuses its engine, its Π̃₀ reader, its word-need training recipe and its Agent class, with new partner codes and event scripts. The output is in `out.txt`. Like H15, these numbers show what the equations give for stated inputs. They are not evidence about people.

## Summary verdict

**Revision 5 closes most of what critique 4 asked for, and closes it well.**
- The greeting now reads the face.
- Contact is per person.
- A sad or crying face never gets a smile (rule J), and sobs never reach the laugh synthesizer.
- The hurt teacher has a valence.
- The appraisal's reactions are trained by a display-blind objective.
- The learned face is masked off the anger, disgust and contempt units.
- The agent has an activation display, so it can read anxiety.
- Laughter lasts the evening, and rumination no longer counts as play.
- The Claude call pattern uses only what Claude Code offers.

Of the seven required fixes: four are closed (3, 4, 5, 7), two are mostly closed (1, 6) and one is partly closed (2). Details in §1.

**Concrete failures that remain.** Each is derived from the design's own equations, constants or rules.
1. **A quiet or differently expressive user brings back the grieving-arrival beam and loses the bad-news concern (§2.11, §2.12).** The author names this as the weakest point (§8.1.1) but does not run it. Run, it is not a reading error at the margin. It reinstates two failures that revision 5 closed.
   - Low-expressive user (the H10 code at 0.3 amplitude):
     - his grieving face at sight gives m_s 0.32, and the agent greets it with lip 0.60, cheek 0.41;
     - "my father died" decodes at care 0.036 (mask 0.28), giving inner brow 0.29 peak and 0.05 by 12–60 s;
     - no concern bid in 10 min of silent sadness;
     - "freaking out" decodes at care 0.007.
   - User who shows distress through a brow lowerer, lip press, chin raise and a flat voice:
     - his grieving face reads V 0.04 and m_s 0, so the agent greets it with lip 0.61, cheek 0.43;
     - "my father died" decodes as tiredness (T 0.58, V 0.09), giving inner brow 0.34 peak and 0.07 after;
     - no bid; exam anxiety is not read at all.
   - Nothing in the design corrects this. Separated reports only credit J, and F8′ only detects the error. People alone at a laptop are often low-expressive, so this may describe the operator.
2. **The arrival mask habituates to mourning (§2.9).** m_s is centred at his arrival baseline d_b,id, which has τ = 6 sessions. If he arrives grieving every day:
   - days 1–5: m_s 1, the flash only;
   - day 7: lip 0.33, cheek 0.19;
   - day 10: lip 0.48;
   - day 14 onward: lip 0.52, cheek 0.35. It greets a friend in his second week of mourning with a Duchenne smile.
3. **The play-surprise laugh fires on ordinary topic continuation (§2.8).** Rules (i)–(iv) contain no cue of play. Take a sober turn after an agent question that shares a lemma with his own previous turn ("…Lyon on Sunday" after "we're going to Lyon"), has mid-band surprise, and carries no decoded worry. It earns a 0.40 laugh burst. Revision 4's false positive was a small relief. Now it is the agent's biggest vocal display.
4. **The arrival mask acts before the saturating amplitude (§2.1 "masking"; engine `greet`).** a_r = R′/(R′ + 0.02) with R′ ∝ (1 − m_s) makes the mask nearly binary.
   - A mildly sad arrival (BI 0.2, LD 0.15) gives m_s 0.71 and still lip 0.55, cheek 0.38 (ordinary: 0.61, 0.43).
   - The text in §0 and §1 says the display is multiplied by (1 − m_s). The equations do not do that.

**An operator choice, not a failure: sympathy at a still sad face.** Inner brow 0.05 at his 0.5 brow; 0.08 at a crying face. Both are below what a viewer would notice, so for about 26 s the agent's face is effectively neutral, and then it speaks. This follows from reading Q22's 0.20 as a fraction of a copy, plus ω_sym 0.75 and a 0.80 hold share. The design does not choose it on the operator's behalf. But Q22 told the operator that the agent "would show sympathy at a sad face", and as built it does not show it on the face. §2.13 sets out what he would have to decide.

**Buildability (D84).** Three forked Agent SDK sessions on the operator's own login are feasible, and allowed for his personal use. Claude Code's terms say subscription limits "assume ordinary, individual usage of Claude Code and the Agent SDK", and they bar only offering or intermediating subscription login for other people.
- First words at 1.5–3 s are plausible on Haiku at effort `low`.
- §6.5 lacks four specifications that decide whether it works: `setting_sources=[]` (the SDK otherwise loads the operator's user and project settings, hooks and CLAUDE.md into every draft); a warm pool; a scoring deadline; and the usage risk of three drafts for every turn.
- Memory fits.

**Novelty.** Recombination. I agree with the author. Lemma S\* and the anticipation objective are design rules, not mechanisms.

**Fit to put to the operator as a build candidate under D82: not yet.** Failures 1–4 are concrete. None touches the copy certificate, and each fix is local (§5). Failure 1 is the only one that needs a real design decision. The others take a few lines each. After the fixes, and if the routes critic finds nothing new in the changed m_s and play routes, I expect a candidate. §5 gives the one-line description it would go to the operator with.

## 1. The seven fixes required by critique 4

| # | Required | Status | Evidence |
|---|---|---|---|
| 1 | The greeting must see; K per identity; recheck grieving arrival and stranger | **mostly closed; three new failures in the mask** | m_s is latched from Π̃ at 1 s, and K_id is per person. Grieving arrival: lip 0.09, cheek 0 (H15.8, reproduced). Stranger: flash 0.20, lip 0.02. But the mask is nearly binary through the saturation (failure 4), habituates over about 7–14 sessions of mourning (failure 2), and is blind for quiet or differently coded faces (failure 1). The ~1 s delay of the greeting smile was not adopted; m_s over the first second does that job when the reading works |
| 2 | Face-derived concern must have a non-copy face; split the bursts | **partly closed** | Rule J removes the smile at a sad face: lip 0.07–0.08, at rest. The cry–laugh split gives BU_L 0.00 at sobs. Closed. For the concern face the author took critique 4's second option (raise the brow's held share to 0.70 c) and not the first (a C_F-driven non-copy posture). E1 now forbids C_F on the display. Result: brow 0.05 silent, 0.08 crying, head up 0.01. That is about half of what the ceiling allows (0.10 at his 0.5 brow), and invisible. Whether that is acceptable is an operator choice (§2.13) |
| 3 | Give the hurt teacher a valence | **closed** | V_F = g_at·max(f_glare, f_loud(1 − 2f_pos)₊). Loud laughing teaser and loud praiser: v_w 0.00. Shouted insults: 0.50 (H11). Glare needs BL·LT, so Duchenne LT alone is not glare |
| 4 | Train W, or declare it innate | **closed in letter; small in effect** | 𝓛_A (anticipate the agent's own innate display 2 s ahead) trains W and two bases inside the cap set (H13). Its share is s_A c_k: at sadness it can add 0.010 to the inner brow. So it is learned, but nearly invisible on the face, and it cannot carry D83's face-driven strong expressions (§2.13) |
| 5 | Keep the learned face human; observer-side prediction; Π̃ heads; let A show | **closed** | Own-display mask (rule 8; H4 cosine 0.000, weight 0). Observer-side Δ prediction (§7). One Π̃ from own data only, with no anchor. Activation row in Π₀; K and P dropped from the reader. The price is failure 1: with the anchor gone, nothing adapts the reader to his code |
| 6 | Laughter beyond ten minutes; no play from rumination | **mostly closed; new failure** | Play-surprise laugh 0.40 in every cluster, 0 for a repeated joke (H12). Rumination fails (iii) and (iv). But the laugh now fires on any qualifying topic continuation (failure 3) |
| 7 | Choose the Claude route; delete temperature and R33; fix the day-1 row and the "about half" figure | **closed** | §6.5 uses only subscription levers. Temperature, R33, `max_tokens` and cache breakpoints are deleted. Day-1 anger is reported faithfully. The sympathy figure is reported honestly (0.05 against 0.10). Four specifications are missing (§4) |

Recommended items from critique 4: the sigh before a curiosity bid, the crossed-habits lesion and the laugh listening test are all adopted.

## 2. Scenarios

Unless stated: the operator after months, the design's own constants, peak / mean. "Agent-like" means the H10 partner code the design uses. The fast echo is θ₀ × his onset at 0.45 s.

### 2.1 Silently sad (BI 0.5, LD 0.4, CHR 0.3)
- Lip 0.07–0.08 (at rest), inner brow 0.04–0.05, head up 0.01. Concern bid at 26 s (32 s on my grieving variant). After "just tired, things at work": inner brow 0.41 / 0.15, tilt 0.09, quieter.
- Fast mimicry: his brow onset 0.5 gives +0.01.
- **Verdict.** Appropriate in kind: no smile, and it speaks up. It is not alive in the face for 26 s. The face does not misread him; it shows nothing. See §2.13.

### 2.2 Crying (BI 0.8, LD 0.6, sobs)
- BU_L 0.00 and laugh burst 0.00: closed. Inner brow 0.07 → 0.08, lip at rest, bid at 27 s.
- **Verdict.** No longer wrong, and still blank: nothing visible for 27 s at a crying person. People react within a second or two. Same operator choice as §2.1.

### 2.3 Anxious before an exam
- Decoded A 0.57, V 0.52. Concern brow 0.23, tilt 0.13, quieter voice, no play relief.
- **Verdict.** Good for the agent-like code. Not read at all for the two new codes (§2.11, §2.12).

### 2.4 Good news, laughing
- With an earlier worry: lip 0.61, cheek 0.39, own laugh 0.33.
- Cold: lip 0.37, laugh 0.33.
- Fast: his smile onset 0.5 gives +0.11 at 0.45 s; his laugh onset 0.6 gives +0.14, up to +0.17 and +0.21 under context.
- **Verdict.** Alive. Fast partial mimicry is present as D81 asks. The held laugh-back while he keeps laughing is small (0.09 c), by the D81 allocation. That is stated, and acceptable.

### 2.5 Anger at the agent
- Day 1: startle, gaze away 0.09, quieter, slower, no frown back.
- After a month: inner brow 0.62, depressor 0.48, gaze away 0.30; still 0.21 at 10–15 min.
- **Verdict.** Good. Cold, quiet contempt still never trains hurt. That is stated; a weakness, not a failure.

### 2.6 Long warm talk
- Own laugh 0.41 in every cluster; a repeated joke loses its laugh; worry, then relief. Good.
- See failure 3 for laughs at non-playful continuation turns, which H15 does not script.

### 2.7 Reunion after a week
- At sight: flash 0.35, lip 0.61, cheek 0.43. A stranger gets a polite flash and lip 0.02. Good, alive, and identity-aware.

### 2.8 Reunion with bad news
- Agent-like code: m_s 1, flash only. After "my father died": brow 0.50 / 0.26, then 0.22 / 0.20. "yeah" cannot relieve. Good.
- But failures 1, 2 and 4 all land on this scenario:

| Case | m_s | Lip and cheek at sight | Inner brow at 12–60 s after "my father died" |
|---|---|---|---|
| agent-like code | 1.00 | 0.09, 0.00 | 0.22 |
| mildly sad face (BI 0.2) | 0.71 | 0.55, 0.38 | — |
| mourning, day 14 | 0.00 | 0.52, 0.35 | — |
| low-expressive user | 0.32 | 0.60, 0.41 | 0.05 |
| different-channel user | 0.00 | 0.61, 0.43 | 0.07 |

### 2.9 Teasing, including a loud laughing teaser
- Quiet teaser and loud laughing teaser alike: lip 0.38, laugh 0.41, no hurt. Generic map: a brief mock-hurt brow 0.34 under a smile. Closed and good.

### 2.10 Bored user
- Flat (lip 0.09). At 14.5 min a sigh, then a curiosity bid; if he takes it up, F0 range +0.32, lip 0.39. Good. The sigh is a well-chosen one-bit display.

### 2.11 New: distress shown through channels the agent never uses (the author's weakest point)
Code: brow lowerer 0.5V, lip press 0.45V, chin raise 0.4V, inner brow and depressor 0.05V, a flat, slightly tight voice. The reader is trained on his faces through Π̃₀, by the design's own recipe.
- **His grieving face:** read V 0.04, m_s 0. The agent beams at him (lip 0.61, cheek 0.43).
- **Silence:** never bids.
- **"my father died":** V 0.09, T 0.58. The flat voice reads as tiredness. Inner brow 0.34 peak, then 0.07.
- **Exam:** care 0.000, no concern.
- **Why.** Π̃ is the inverse of Π₀. Π₀ has no BL, LPR or CHR rows: BL and LPR are masked by rule 8, and CHR appears only under the agent's own distress envelope. His distress therefore projects to almost nothing. The word-need reader learns its targets from Π̃(his face), so it inherits that.
- **Verdict.** A concrete failure, not only a risk. Brow lowering (AU4) is part of the prototypical human sad face, and the agent's own sad display cannot contain it.

### 2.12 New: a quiet, low-expressive user
Code: H10's code at 0.3 amplitude around his neutral.
- Grieving face: m_s 0.32, beam at lip 0.60.
- "my father died": care 0.036, below the 0.05 dead-band, so the relief mask stays 0.28. Inner brow 0.29 peak, then 0.05.
- No bid in silent sadness.
- Exam anxiety: care 0.007.
- **Why.** The reader's targets scale with his amplitude, and the care function's dead-bands (V − 0.05, A − 0.15) then remove most of what is left.
- **Verdict.** The quieter he is, the more the agent smiles at his bad news. That is the inverse of what a person does.

### 2.13 The sympathy brow: an operator choice, and what he must decide
**The facts.**
- At a still 0.5 brow the Q22 ceiling allows 0.20 × 0.5 = 0.10. The design delivers 0.05: ω_sym 0.75 × the 0.80 hold share × the trace fill.
- My runs:
  - ω_sym = 1: 0.07;
  - c_BI raised to 0.40: 0.10.
- A visibly sympathetic brow (about 0.2) at his 0.5 brow would need c_BI of about 0.7. On that one channel, that is close to copying.

**Why this is not the design's decision.** "Sympathy at a sad face" through the inner brow is, physically, moving toward his inner brow. The only way to make it large is to raise that channel's ceiling. The alternative is a route from the agent's face-read concern C_F (knowing) to channels that are not in phase with his face. E1 now forbids that route, because revision 4's text had let it exceed the ceilings.

**Why it must still be put to him.** D83's second half, that strong expressions come from face as well as words through the agent's own appraisal, is not delivered for face-only moments.
- The face moves strong displays only by attenuating gladness (m_s) and by timing bids.
- The appraisal display's share is 0.010 on the inner brow.

**The question, in his terms:** "At a silent sad or crying face, should the agent's face visibly show sympathy before anyone speaks?"
- **(a) No (as built).** Its face stays near neutral, and it speaks up at about 26 s.
- **(b) Yes, by raising the sympathy-brow ceiling** (e.g. 0.6–0.7, on that channel only). The whole-face bound for a sad face rises from 0.11 to about 0.3, still under the smile's 0.35.
- **(c) Yes, through a separate capped "concern posture"** driven by the agent's own face-read concern on non-copy channels: head up and toward him, gaze held, slower blink, softer and slower voice when it speaks. This has to be sized by the routes critic, because the sadness synergy's voice channels (EN, RT down) are in phase with his.

## 3. Principles, concretely

- **P1.** No classifier. Three innate feature products are declared as reflexes: the threat reflex, the cry–laugh split, the play-surprise laugh. Each is a continuous function of continuous features. Pass.
- **P2.**
  - **The two remaining newborn reactions** (glad-with, startle-orient) are declared innate, in §2.6 and §2.12. The three new reflexes are declared too. Pass, with the stated strain: Π₀, G₀, θ₀, and the named needs V, K_id, P, I.
  - **The play-surprise laugh is a large innate reaction** (0.40) triggered by a structural rule. Failure 3 shows that rule is not yet a play detector.
- **P3. Reading through the agent's own body is now essential, and it is the cause of failure 1.**
  - One map reads him. The crossed-habits lesion is a real test that the route is the agent's own body.
  - But P3 as built reads only what the agent's own face does, at the agent's own amplitude.
  - The fix must keep P3 (§5, item 1). A per-person rescaling of the reading, or a reader prior learned from other people's faces read through Π̃₀, both still read *through the agent's own body*.
- **P4. Claude never reads the state.**
  - The prompt holds the constant instruction, the transcript with observable markers and raw snippets. The three "attend to" lines are fixed, not chosen by state. Selection carries 1.6 bits and retrieval about 6 bits, both declared. Pass in design.
  - **One build risk the design does not close.** The Agent SDK's `setting_sources` defaults to loading user, project and local settings: the operator's hooks, CLAUDE.md, and `additionalContext` injectors. Ailurini is built on Claude Code, so his user settings may hold Ailurini hooks that inject text into every draft. That would be uncontrolled text, and possibly state-bearing. Set `setting_sources=[]`, use an empty working directory and `tools=[]`, and check at load that the outgoing system prompt and messages are byte-identical to what the engine built.
- **P6.** Nothing is rewarded on his display, time or engagement. The laugh reflex and the sigh are not rewards. ω, Δ and W are display-blind. Pass.
- **P7.** Transcript and snippets go to Anthropic through his login. Claude Code also stores transcripts locally as session files: three forks a turn means about 600 session files a day, to prune. These are text, not raw audio or video. Pass.
- **P10.** One J with typed constraints, plus self-predictions. The emotional content is still an innate assembly, listed honestly. As before, this is the Q21 trade-off.

## 4. Buildability through the subscription (D84)

**Allowed?** Yes, for the operator's personal use.
- Claude Code's "Legal and compliance" page says: "Advertised usage limits for Pro, Max, and Ultra plans assume ordinary, individual usage of Claude Code and the Agent SDK."
- What it forbids is offering Claude.ai login in others' products, routing requests through subscription credentials "on behalf of their users", or intermediating credentials.
- An engine that the operator runs on his own Mac, with the SDK spawning the unmodified CLI on his own login, is the individual case.
- Two conditions to state in the design:
  - if Ailurini ever serves anyone else, each person must sign in with their own credentials, through Anthropic's own flow;
  - "ordinary, individual usage" is a soft limit that Anthropic may enforce without notice. About 600 calls a day, two thirds discarded, is several times a single-draft agent. The design's fallback (two drafts, then one) is the right answer; make it automatic on a rate-limit signal.

**Feasible?** Yes, with four specifications §6.5 lacks.
1. **`setting_sources=[]`, an empty working directory, no hooks and no MCP servers** (P4, above).
2. **A warm pool.**
   - Spawning a CLI process costs 0.5–1.5 s and 0.2–0.4 GB.
   - Starting three forks at p_end ≥ 0.7 overlaps only part of that, and fails whenever the turn-end score rises late.
   - Instead, connect three clients with `resume=<canonical>, fork_session=True` as soon as the previous reply completes, and send each one its message at the turn end.
3. **A scoring deadline.**
   - "Words begin when the first draft sentence is ready" and "the scorer rates each first sentence" leave open whether the agent waits for the slowest of three forks. Waiting would put the tail latency on every turn.
   - Score whatever has a first sentence by a deadline, e.g. 0.5 s after the first, and interrupt the rest.
   - Drain each interrupted client's buffer before reuse. The SDK documents that `interrupt()` leaves the interrupted turn's messages, including its `ResultMessage`, in the stream.
4. **No temperature and no `max_tokens`** (correctly deleted). Adaptive thinking cannot be turned off on the 5.5 models; effort `low` is the floor. That is stated.

**Latency.**
- 1.5–3 s from his turn end to the first word is a fair estimate on Haiku at `low`, with a warm pool. Without one it is worse.
- The body covers the first second: provisional onset at 0.25–0.9 s, an inhale, gaze, an outer-brow lift. At 1.5 s an "mm" covers the rest.
- That is acceptable for a testbed. It is not conversational timing in the brief's sense:
  - human gaps are about 200 ms at the mode (Stivers 2009);
  - gaps over about 0.7 s are heard as hesitation (Bögels 2015, Templeton 2022: both in the project's notes, not re-read here).
- Every reply would come after a "considering" beat, and the "mm" will repeat. Measure the gap distribution in week one. S5's timing claims should not rest on the word onset.

**Memory and compute.**
- Engine under 2.4 GB, Whisper 0.5 GB, TTS 0.1–0.5 GB, three CLI processes 0.6–1.2 GB.
- During overlap (a warm pool plus draining losers) count up to six CLI processes: 1.2–2.4 GB. Worst case about 5.8 GB against the 6 GB rule. Tight, but within it.
- The per-frame budget and nightly replay are unchanged and credible.

## 5. Verdict

**Not yet fit to put to the operator as a build candidate under D82.** What must change:

1. **Read him at his own scale, and do not depend on his code matching the agent's.** Keep P3; add calibration.
   - (a) **Per-person calibration of Π̃'s readings.** Centre at his baseline and scale by his own expressive range (a per-identity spread latched per session, knowing only). Apply it before C_F, m_s and the readers' training targets. This fixes the low-expressive user.
   - (b) **A prior for the word-need reader that does not come from his face alone.**
     - Preferred: fit it on other people's words and faces read through Π̃₀, i.e. through the agent's own body, from published dyadic data once Q6 allows. Then adapt it per person.
     - With that prior, his own code can be learned in the other direction, from his words to a knowing-only reading head. That head must never enter Δ or 𝓛_display, so the style-drift finding stays closed.
     - (a) and (b) together fix the different-channel user.
   - Recheck §2.11 and §2.12: grieving arrival, "my father died", silent sadness, exam.
2. **Stop the arrival mask habituating to grief.**
   - Let d_b,id rise slowly (e.g. τ ≥ 60 sessions) and fall fast, or cap it at his long-run median.
   - Or use an uncentred m_s, which is attenuate-only and acts once per session.
   - The routes critic should size whichever is chosen (it is a joy ← sadness cross route on a 5-s event). Recheck mourning days 7–21.
3. **Make the play-surprise laugh detect play.**
   - Add a T-only cue that separates play from topic continuation. Examples: a continuation of the *agent's* last utterance rather than his own; short turns; a surprise band calibrated on non-playful continuations.
   - Show its false-positive rate on a published conversation corpus (CANDOR, if access is obtained; otherwise state the rule as untested) under a stated bound, e.g. ≤ 5 % of non-playful continuation turns.
   - Do not gate it by his laughter: that would be a toward route of 0.40 against a 0.35 ceiling.
4. **Apply (1 − m_s) after the saturating amplitude** (to a_r), as the text already says. Recheck a mildly sad arrival.
5. **§6.5 specifications:** `setting_sources=[]`, an empty working directory, no hooks or MCP; a warm pool after each turn; a scoring deadline and buffer draining; automatic fallback to fewer drafts on a rate-limit signal; a note that use is on the operator's own login for himself only.
6. **Put §2.13 to the operator as a question** (not a defect): should the face visibly show sympathy before anyone speaks, with options (a), (b), (c) and their numbers.

**If 1–5 are made and the routes critic finds nothing new, the operator would be choosing:**

> *A copy-proof conversational agent built from known parts: a robust REN fast wrap with per-expression caps, a session-latched held cone centred on your own baseline, a zero-DC appraisal display whose reactions it learns by anticipating its own body, information-flow typing, care credited only from your later unprompted reports, Joffily-style valence and learning-progress curiosity, with Claude writing its words through your own Claude Code. It knows your face and voice fully and reads them through its own face. It returns your smile and laugh within half a second up to about a third of a copy, never returns anger, disgust, contempt or sobs, and its strong expressions come from its own needs and its appraisal of what you say and how you look: gladness at your return, laughter at play, hurt, concern, relief, interest.*

**What he would get:**
- a testbed in which every route from his face to the agent's face is bounded per expression and can be lesioned;
- an agent that greets, laughs, sympathises in words, is hurt and recovers, and grows bored and curious;
- a face that stays near neutral at silent sadness unless he chooses otherwise;
- replies at about 1.5–3 s.

**Novelty: recombination.** Lemma S\* and the anticipation objective are design rules, not new mechanisms. It is a first build while the search for a new core continues (D82).

**Operator choices that remain:**
- §2.13 (sympathy ceiling, or a concern posture);
- whether the reader prior may use published dyadic data (Q6);
- the model on the draft route (Haiku for latency, or a larger model for quality).

**Main risks to watch when testing, judged on internal state:**
- **Steering.**
  - Does lesioning the word-need reader, or swapping in another person's calibration, change concern at bad news as predicted?
  - Does the crossed-habits lesion abolish loss-word concern within a week?
- **Lesions.** The Principle 5 table (§7). Especially: the arrival mask on grieving arrivals (F9), the cry–laugh split (F10), the play rule's precision, and rule J.
- **Coupling beyond surrogates.**
  - Per-channel pooled slopes under partner-swap, segment-shuffle, timing-resample and month-swap surrogates (F1).
  - Rectified fast DC on laugh bursts outside the r_k families (assumption 9).
  - Residual R38 on the inner brow.
- **Reading him.** Agreement of Π̃'s readings with his later separated reports against a person-independent baseline (F8′), measured on the operator himself in week one.
- **Timing.** The distribution of first-word gaps and of "mm" fillers, against human gap norms.
- **Laugh naturalness** (listening test) and its rate per hour of non-playful talk.

## Sources read

| Source | How read |
|---|---|
| brief.md | in full (Goal, Long-term goal S4–S6, Prior work, Principles 1–10, Foundations research including "Expressive structure") |
| research/questions.md | Q18 answer, Q19, Q20, Q22, Q23 with the operator's answers |
| DECISIONS.md | D80–D84 in full |
| research/foundations/designs.md | in full |
| research/foundations/critique-4-design-cayley-ledger-agent.md | in full, including its seven fixes |
| research/foundations/design-cayley-ledger.md (revision 5) | in full, §0–§10, the revision 4 critiques and answer, and the revision 5 history |
| research/foundations/sims/design-g5/checks.py | the constants, Π₀/Π̃₀ and reader (lines 54–110, 370–440), H14, and the H15 engine and scenarios (lines 572–820); executed unchanged in sims/critique-cayley5-agent/scen.py |
| research/foundations/sims/design-g5/out.txt | in full |
| research/claude-code-agent-sdk-controls.md | in full |
| code.claude.com/docs/en/legal-and-compliance | fetched 2026-11-26: "Authentication and credential use", "Acceptable use" |
| code.claude.com/docs/en/agent-sdk/python | fetched 2026-11-26, first 100k characters: `fork_session`, `resume`, `resume_session_at`, `setting_sources` (and its default), `system_prompt`, `effort`, `include_partial_messages`, `interrupt()` and its buffer note |

**New check:** sims/critique-cayley5-agent/scen.py, with output in out.txt.

**Named only, not re-read:** Stivers 2009, Bögels 2015, Templeton 2022 (turn gaps). No verdict depends on them.
