# Critique 8 of the Cayley–ledger core (revision 8): is it an emotional agent, D85 compliance, principles, buildability, and is it fit to put to the operator under D82

Independent critic, 2026-11-26T14:47:59Z

I critique research/foundations/design-cayley-ledger.md, revision 8. I did not write it. The standard is Q19 (concrete failures, honest verdicts), the operator's answers Q20–Q23 (D81–D84) and his note Q26 (D85). Q24 is open, and the design follows its recommendation. Another critic hunts copy routes, so I size none. Where a fix I ask for touches a route, I hand it on.

New numbers come from the design's own engine. `sims/critique-cayley8-agent/scen.py` loads `sims/design-g8/checks.py` exactly as that file does: the revision-7 parts and the class `Agent8`, without its J31–J39 result loops. It then runs three new partners (B1–B3). The output is in `sims/critique-cayley8-agent/out.txt`. The scenarios take 12 s. Loading the engine took 29 min here, and that load is the design's own cost (revisions 5–7 are executed unchanged), so I could not keep the whole script under 5 min. Like J39, these numbers are what the equations give for stated inputs. They are not evidence about people.

## Summary verdict

**Revision 8 closes every required change from critique 7.** Several closures are better than what I asked for.
- **The posture.** It now reads none of the channels it writes, so a quiet user's sadness and a silent panic get a steady, visible look (J34). No mirror can hold it (J33). The structural fix is better than my proposed pre-onset anchor.
- **The laugh.** "I got fired today, haha" is no longer laughed back.
- **D85 residue.** The play laugh now goes through the learned gate, and D_s is honestly relabelled.
- **Build items.** All of them are specified.

D81 fast partial mimicry survives at 0.80 s (laugh back sounding at 0.83 s). D83 holds. I re-checked the eighteen scenarios against the design's J39 and found them alive and appropriate, with the exceptions below.

**One new concrete failure, narrow, from a part revision 8 added (§2.20, out.txt B2).** The threat silencing switches the posture fully off whenever brow lowerer × lid tightener × gaze-at-the-agent exceeds 0.15 over 3 s. That is also the signature of a tearful squint or a pain grimace directed at the agent. Two cases:
- A grieving face with BL 0.4 and LT 0.4 that looks at the agent gets **posture 0.00** (agent brow 0.03). The same face looking away gets posture 0.99 and brow 0.23.
- A different-channel user's grief face plus LT 0.4 at the agent also gets posture 0.00.

Sobs rescue it. Silence does not. The design declares "a person who glares while distressed … gets no posture" (§8.1.3), but that wording hides how ordinary the trigger is. Unlike the brow-only cost, this is not forced: the anger case it protects (J35) can be kept with a narrower silencing.

**One declared, forced trade-off that the operator must see (§2.19, B1).** Brow-only distress gets no look before words. Inner brow 0.5 alone gives posture 0.00 and agent brow 0.04. For the operator's code the agent's spoken bid comes at 47–57 s; for a quiet user at 106–111 s; for inner brow 0.3, no bid within 2 min. This follows from making the posture copy-proof by construction, and I accept it as a design choice. It is a Q24 matter, and the Build-candidate summary does not yet tell the operator about it.

**Buildability (D84, the Mac): yes.** The recogniser condition is the weakest assumption. A stable-word p90 of 0.55 s or less is unlikely with today's on-device streaming recognisers. About 0.6–0.75 s is realistic with a fixed-delay streaming model, so δ_g will land at about 0.85–1.0 s. The design's own fallback covers that. One specification is missing: the "unknown words → 0" rule needs a finalization watermark from the recogniser (§4).

**Novelty: recombination.** I agree with the author.

**Fit to put to the operator as a build candidate under D82: not as written, by one narrow, avoidable failure.** Three things are needed:
1. Narrow the threat silencing so that a tearful or pained face looking at the agent keeps its posture, while J35 (anger, anger with heavy breathing, concentration) still starts nothing.
2. Add the recogniser watermark to the specification.
3. Correct the Build-candidate summary (§6.2 gives the corrected text).

None of these touches the core bound. Once they are made and the routes critic accepts R40′, R47–R50 and R1g with the new timing, I expect it to go to the operator with the summary in §6.2.

## 1. Critique 7's required changes

| # | Required | Status | Evidence |
|---|---|---|---|
| 1 | Gate timing: word inputs on the words completed before his laugh; recheck J30.7 at his onset; add "I got fired today, haha" and "my father died, haha, sorry" | **closed** (one specification gap, §4) | Incremental recogniser; gated echo at 0.80 s; each frame gated by words ending ≤ frame + 0.25 s; instant closing. J36 at ASR latency 0.30 / 0.55 s: misfortune gate 0.09 / 0.08, fired 0.05 / 0.08, father died 0.01, laugh into the word 0.06, all silent; ordinary +0.136 sounding at +0.83 s. J39.7 re-read at onset: 0.10 / 0.03. The routes critic still has to confirm T1 and R1g with the new timing |
| 2a | Posture for quiet users: no self-suppression, no flicker | **closed, better than asked** | The read set is disjoint from the write set; the mirror removal is deleted. J34: one onset, no release, brow ≥ 0.15 in 2–7 s, mean 0.18–0.22 for silent sadness and grief in every code (revision 7 quiet: on/off every 20–30 s, brow 0.07). The cost is brow-only distress (§2.19) |
| 2b | Silent panic graded as distress | **closed in the constructed codes** | Breathing enters the load only with non-brow distress. J34 silent panic 0.18–0.22 held (revision 7: 0.04–0.11). It depends on an untested breathing sensor (§4) |
| 2c | Recheck J22 in full | **closed for the agent side** | J33: every mirror releases at 62.5–66 s; answering concern released by the probe at 190.5 s. The routes critic confirms |
| 3a | Play laugh through the dyad-learned gate, not the care dead-band | **closed** | Rule 13. J39.9: gate ≥ 0.98 on all 28 play laughs. J39.16: 0.14 × 0.11 = 0.015, below the synthesizer floor |
| 3b | Relabel D_s as source 2; report its fitted weight | **closed** | §2.15, §6.7.7; J37: 1.00 → 0.59 / 0.27 / 0.12 at D_s 0.3 / 0.6 / 0.9; the generating process gave it no causal role, and this is stated |
| 4a | Events at 30 Hz before reduction | **closed** | §6.7.1, with stored snippets (≈ 0.1 GB) |
| 4b | Word-timestamp alignment in the corpus | **closed** | §6.7.2 (words ending ≤ onset + 0.25 s; the segment cut at the onset), plus the same ASR normaliser (§6.7.3) |
| 4c | `is_valid`, V_own window, laugh channels fitted to facial return | **closed** | §6.7.4–6 |
| 4d | Initiative turns in the canonical history | **closed** | Observable-marker user turn, 5-s bins; J38: 0 same-role pairs, 0 empty turns |
| 4e | System-prompt fallback for the transcript resume | **closed** | §6.5, with two sensible week-0 checks (no system prompt or winner's thinking resumed) |
| 4f | Week-0 check of disabled thinking on Haiku 5.5 | **closed** | §6.5, with a check that reads `thinkingTokens` |

## 2. Scenarios

The operator after months, peak / mean. Numbers are the design's J39 unless marked **(mine)**. "Echo" is the 30-Hz gated fast echo at ASR latency 0.40 s.

### 2.1 Silently sad, including a quiet user
- Design face: posture at 2.0 s, brow 0.15 at 3.0 s, then 0.23 / 0.22 held, lip 0.05, bid at 27 s. After "just tired, things at work": brow 0.64 / 0.36, tilt 0.15.
- Each code's own silent sadness over 10 min: 0.23 / 0.21 (operator), 0.20 / 0.19 (quiet), 0.19 / 0.18 (different channels). One onset, no release, bids at 49–60 s.
- **(mine) B3, natural fluctuation** (AR(1) on V, SD 0.10 and 0.20, τ 5 s, 3 seeds × 2 codes). In 4 of 12 runs the first probe at about 190 s reads his random dip as "following" and releases. The posture comes back 2–4.5 s later. Brow mean is 0.17–0.21 throughout; the posture is below 0.05 for under 1 % of the time.
- **Verdict.** Alive and appropriate. The probe's false release is a single short dip, a weak point rather than a failure. Report its rate live (§6.3).

### 2.2 Crying, with a second wave
- Posture at 1.5 s, brow 0.23 / 0.21, no laugh, bid at 18 s, released at 66.5 s. On again 0.5 s into the second wave, brow 0.25 / 0.23. Quiet code 0.20 / 0.18 and 0.20 / 0.19.
- **Verdict.** Good. Sobs also bypass the threat silencing (B2: grief + squint + sobs at the agent, posture 0.99).

### 2.3 Anxious before an exam; silent panic
- With words: brow 0.33–0.38 / 0.27–0.32, tilt 0.13–0.14, quieter, all codes.
- Silent panic: on at 3.0–4.5 s, brow about 0.20 held for 10 min.
- **Verdict.** Good. Silent panic now rests on breathing, which is an assumption about the sensor (§4), not a demonstrated input.

### 2.4 Good news, laughing
- Lip 0.59, own laugh 0.35. Echo +0.135 (after a worry, gate 0.82) or +0.157 (cold), sounding at +0.83 s.
- **Verdict.** Alive. The "relief trims the laugh" oddity of revision 7 is smaller (gate 0.82, was 0.73).

### 2.5 A grieving person's nervous laugh
- Gate 0.00 before and after Claude's reply; brow 0.40–0.69, posture on.
- Four minutes later, composed: 0.06 with D_s, 0.25 without it. Silent either way.
- "My father died, haha, sorry" as a first disclosure: 0.01.
- **Verdict.** Closed, and now also for the first-utterance case I raised.

### 2.6 "I got fired today, haha"; a laugh ending a bad-news sentence
- Gate at his onset 0.05–0.09, no laugh back, lip ≤ +0.006.
- Limit stated by the design: a laugh beginning more than 0.25 s before the bad word ends is echoed (+0.138) until the word arrives (J36 h).
- **Verdict.** Closed. I do not count the limit as a failure. A listener who smiles back at a smiling teller before the bad word is spoken does what any person would do, because no one can know the next word. People also rarely laugh in the middle of a phrase; laughter clusters at phrase ends (Provine 1993, named only).

### 2.7 Mocking laughter
- After a month: gate 0.01, brow 0.54, depressor 0.41, gaze away. Day 1: gate 0.05, silent.
- With incremental words, a first-utterance "haha, you're useless" is now gated by "useless" once it lands, provided the laugh does not start more than 0.25 s before that word.
- **Verdict.** Good.

### 2.8 Laughter at misfortune
- Gate 0.10 / 0.03 at his onsets, silent; brow 0.37 from the words.
- **Verdict.** Closed.

### 2.9 Anger at the agent
- Day 1: gaze away, quieter, no frown back, no posture. After a month: brow 0.62 / 0.25, depressor 0.48.
- **Verdict.** Good. J35 holds, but the mechanism that keeps the posture off here is the one that fails in §2.20.

### 2.10 Long warm talk (2 h)
- Own laugh 0.41 per cluster; all 28 play laughs pass (gate ≥ 0.98); echo +0.138; the repeated joke loses its laugh; relief lip 0.60.
- **Verdict.** Good.

### 2.11 Reunion; a stranger
- Flash 0.35, lip 0.61, cheek 0.43. Stranger: echo lip +0.044 at gate 1.00.
- **Verdict.** Alive.

### 2.12 Reunion with grief; repeated mourning (days 7, 14, 21)
- m_s 1.00, lip 0.09 and cheek 0 every day, brow at sight 0.19–0.20 for every code (revision 7 quiet: 0.07).
- After "my father died": 0.68–0.69 / 0.44–0.45.
- **Verdict.** Good. The quiet user's grieving arrival is fixed.

### 2.13 Mildly sad arrival
- Design's mild face: light posture 0.41, brow 0.09. Each code's own V 0.3: no posture.
- **Verdict.** Appropriate: little or nothing at mild sadness.

### 2.14 Teasing, including a loud teaser
- Echo +0.138 / +0.193 (gate 1.00), own laugh 0.38–0.40, no posture; generic map mock-hurt brow 0.39 under lip 0.27.
- **Verdict.** Good.

### 2.15 Bored user; ordinary topic continuation
- Flat, curiosity at 14.5 min, a sigh, a bid; no laugh for an answer.
- **Verdict.** Good.

### 2.16 A sad user who jokes
- Brow 0.30, posture 0.97; echo silent (gate 0.07); own play laugh 0.015, silent.
- **Verdict.** Defensible, and now decided by the learned gate, not by a rule. The corpus's listeners return 0.39 here. This stays an operator choice (§6.2).

### 2.17 A calm user saying something alarming
- No posture; from the words, brow 0.50 / 0.26, then 0.21 held, tilt 0.17, quieter; the same for the quiet code.
- **Verdict.** Appropriate (D83: own appraisal of his words).

### 2.18 D81 and D83
- **D81: satisfied.** Fast partial matching is present: laugh +0.136–0.193 sounding at 0.83 s; lip +0.044–0.110 peaking at about 0.9 s; ordinary, teasing, warm and stranger contexts.
  - 0.80 s is inside the first second, where antiphonal laughter ("during or immediately after" the partner's laugh, Smoski and Bachorowski 2003; I could not confirm their exact window) and context-modulated mimicry (Mauersberger 2022, named only) both sit.
  - Two costs. First, the smile echo on LP and CR also moved from 0.45 s to 0.80 s, including silent smiles where no words are pending. That is unnecessary but harmless. A constant delay is what keeps T1 clean, so I do not ask for it to change. Second, if week 0 forces δ_g to 1.0 s, the laugh sounds at about 1.03 s, which is still "fast" by any reading of D81, but at its edge.
- **D83: satisfied.** Strong expressions come from the agent's own appraisal of words and face: brow 0.50–0.69 at bad news, lip 0.59–0.61 at good news and reunion, hurt after insults, concern at a silently sad face (non-brow evidence).

### 2.19 Distress that shows only in the brow (the author's declared weak point; out.txt B1)

| His face (silent, 120 s) | Operator's code | Quiet code |
|---|---|---|
| inner brow 0.5 | posture 0.00; agent brow 0.038 / 0.029; bid at 57 s | posture 0.00; brow 0.008; bid at 112 s |
| inner 0.5 + outer 0.15 | posture 0.00; brow 0.038; bid at 47 s | posture 0.00; brow 0.008; bid at 107 s |
| inner 0.3 | posture 0.00; brow 0.021; no bid within 120 s | posture 0.00; brow 0.003; no bid |

- **What it means.** The agent's face stays near neutral. The fast gear's brow echo (≤ 0.04) is invisible. Its first sign of concern is the spoken bid, about a minute in for the operator and nearly two minutes for a quiet person.
- **How common it is.** In real faces the inner brow raise is the sadness signal that is hardest to suppress (Ekman's "reliable" grief muscles, named only). So a person who keeps a brave mouth while sad shows mostly this. Two things limit the cost:
  - In the AU1+4 form, the brow lowerer (BL) is in the posture's read set, and the per-person head H^p_id can learn it from his words.
  - The words carry it as soon as he speaks.
- **Verdict: a forced trade-off, not a failure.** Reading the inner brow is exactly the copy route the routes critic found in revision 7 (2–3 × c_BI). Every variant that reads it either copies or subtracts, and subtracting is what flickered. The design chose "copy-proof by construction" and stated the cost. That is a legitimate choice, but it belongs to the operator under Q24, and the summary must say it.

### 2.20 A tearful or pained face that looks at the agent (new failure; out.txt B2)

| Silent, no sobs, 120 s | Posture | Agent brow peak / mean |
|---|---|---|
| operator's grief face | 0.99 (on at 2.5 s) | 0.23 / 0.20 |
| the same + BL 0.4, LT 0.4, **looking at the agent** | **0.00** | 0.03 / 0.02 |
| the same, looking away | 0.99 | 0.23 / 0.20 |
| the same + BL 0.3, LT 0.3 at the agent (glare 0.09, partial silencing) | 0.99 | 0.23 / 0.20 |
| different-channel grief + LT 0.4 at the agent | **0.00** | 0.00 |
| operator grief + squint + sobs, at the agent | 0.99 | 0.23 / 0.21 |

- **Why it happens.** The silencing multiplies the posture's whole face load by 1 − clip(glare₃ / 0.15, 0, 1), where glare = BL · LT · gaze-at. Brow lowering and lid tightening (AU4, AU7) are part of crying faces and are the core of the pain face (Prkachin's pain action units, named only). A person in pain or crying with a squint who looks at the screen, which is where the agent is, crosses 0.15 at moderate intensities.
- **It is avoidable.** The silencing exists only so that a different-channel user's angry face, whose BL reads as distress once the inner brow is not read, does not start the posture (J35: load 0.052, just over onset). Possible fixes:
  1. **Channel-specific silencing.** While glare is up, drop BL (and LPR, which anger also uses) from the posture's read set, rather than zeroing the whole load. Cheek, depressor, chin, breathing, voice, sobs and words still count, so a crying or pained face keeps its posture, and the J35 anger face (BL, LT, gaze, no other distress sign) reads near 0. The arousal term needs V_p ≥ 0.15, so anger with heavy breathing stays off as well.
  2. **A D85-consistent alternative.** Learn the silencing as a frozen monotone attenuator from recorded listeners' inner-brow response to speakers' faces, the same way the laugh gate was learned. This is more work.

  Either way, recheck J35 and B2, and hand R48 to the routes critic.

## 3. D85 compliance; Principles 1–10

**No hand-written situational rules: true for everything revision 7 critics flagged.**
- The play laugh's care condition is gone, replaced by the learned gate.
- D_s is a dyad-learned input whose weight is reported.
- δ_g, λ_w and "unknown words close" are timing constants and an attenuate-on-missing-information rule. They are not situations.
- The posture's read set is structural.
- The probe is a perturbation test with no situation named.

**The threat silencing is the one part closest to a situational rule.** As an interaction of two innate reflexes, where a threat state inhibits an affiliative display, it is admissible as innate structure (P2 allows reflexes). But it was added to fix one situation (the angry face), and its misfire (§2.20) is what a rule-shaped patch looks like. Fix 1 keeps it innate and narrower. Fix 2 moves it to source 2. Either is acceptable.

**Source mapping (§2.15) is honest.** Source 1 (Claude's words, heard by the agent, gate only, rule 12′) is small and P4-clean. Source 2 carries the gate, Λ and D_s. Source 3 is sensitization and κ_replay.

**Principles:**
- **P1. Pass.** No classifier. Breathing is a continuous feature; the gate predicts a continuous return.
- **P2. Pass with the known strain.** The new innate parts are declared: the read set, the breathing condition, the threat silencing, the probe. "Distress-type" groupings are the designer's, as before.
- **P3. Pass.** The posture reads him through the agent's own inverse with the written rows removed.
- **P4. Pass.** Initiative turns are observable markers in 5-s bins. The system-prompt fallback has a sound check against a fixed line being resumed through the winner's thinking. Rule 12′ keeps Claude's text out of every T quantity except Λ_V(own).
- **P5. Pass.** The §7 rows come with checks (posture read set, breathing, silencing, probe, word timing, instant closing, play gate, D_s).
- **P6. Pass.** The probe reads his response and learns nothing from it. No reward for his face.
- **P7. Pass.** Seamless stays on the Mac and is reduced on arrival. The incremental recogniser runs on-device.
- **P8, P9.** Unaffected.
- **P10. Pass in the same sense as before.** One J with typed constraints; the assembly list grows (read set, breathing, silencing, probe, δ_g, λ_w) and is stated.

## 4. Buildability through the subscription (D84) and on the Mac

**Subscription: feasible as specified.** Nothing new needs the API. The three week-0 checks are well posed: transcript resume, system prompt and thinking not resumed, and thinking on Haiku 5.5.

**The recogniser (< 0.55 s stable latency): is it realistic?** Partly.
- **The condition is about stable words, not partials.** "Stable" means a word never revised afterwards, and that is what makes "unknown words → 0" safe. The candidates differ:
  - **Apple's recognisers.** SFSpeechRecognizer partials are revised freely and carry no stability flag. The newer SpeechAnalyzer and SpeechTranscriber separate volatile from finalized results. Developers report finalization delays of about 1.5–2.2 s in live use (Apple developer forum thread 794720, anecdotal), far above 0.55 s. Using volatile results "once they stabilise" means adding a local-agreement wait, which costs a further update interval.
  - **Whisper-based streaming** (local agreement) typically runs at seconds of latency. Not suitable.
  - **Fixed-delay streaming models** are the realistic route. Kyutai's stt-1b-en_fr emits words 0.5 s after they are spoken, never revises them, and returns word timestamps (Kyutai's delayed-streams-modeling repository). With its 80-ms frames and compute, word end to delivery is about 0.6–0.7 s, so ℓ_p90 ≤ 0.55 s is unlikely and ℓ_p90 ≈ 0.65–0.75 s is likely.
  - **Expected result:** δ_g = min(1.0, ℓ_p90 + 0.25) ≈ 0.9–1.0 s, inside the design's fallback, with the laugh sounding at about 0.93–1.03 s. Above 0.75 s the choice goes to the operator, as specified.
- **Conditions to state:**
  1. **Language.** That model covers English and French only, so the operator's language decides the candidate.
  2. **The MLX build.** The repository's MLX example is the 2.6B model, which has a 2.5-s delay. The 1B model is documented on iPhone 16 Pro (Swift) and in Rust. Which runtime runs it on the M1 Pro, alongside the utterance recogniser (Whisper), face tracking, TTS and the engine within the 16 GB budget, is a week-0 measurement.
  3. **A finalization watermark.** "If the words through s + λ_w are not delivered by s + δ_g, the gate target is 0" is not implementable unless the recogniser says how far its stable output reaches. Otherwise a late word is simply absent, and the gate sees the previous sentence and opens. The simulation models only the global condition ℓ + λ_w ≤ δ_g. Specify: the gate for frame s uses words only if the recogniser's finalized-through time is ≥ s + λ_w; otherwise 0. A fixed-delay model gives this watermark directly (now − delay − frame). VAD gives it in silence.
- **Breathing.** "Microphone breath band and upper-body motion at 10 Hz" is plausible from webcam chest and shoulder motion, but untested here. Silent breathing is near the noise floor of a laptop microphone at conversation distance. Silent panic depends on it, so the week-0 list should include a breathing-sensor check at the operator's desk. This is a risk, not a blocker: without it, silent panic falls back to revision-7-level concern and words.

**Nothing else blocks building.** Parameter counts, the dyad fit (2–3 h, about 1.6 GB stored) and the online cost (< 0.1 ms per frame for the echo) are as before.

## 5. Weak points that are not failures

1. **Probe false releases** (B3): in 4 of 12 runs, one 2–4.5 s dip at the first probe. Harmless; measure live.
2. **The smile echo is also delayed to 0.80 s** when no words are pending. Harmless, and it keeps T1 simple.
3. **A laugh starting more than 0.25 s before the bad word** is echoed for under 0.4 s. Human-like.
4. **Coping joke while sad**: silent; the corpus's listeners return 0.39. Left to the operator.
5. **The dyad-learned parts are still fitted on a constructed corpus.** This is the design's own "weakest point", and it stays one. F15, F16 and F21 decide it.

## 6. Verdict

### 6.1 Fit under D82?

**Not as written, by one narrow, avoidable failure. Yes once these are made:**
1. **Threat silencing (§2.20).** It must not remove the posture from a tearful or pained face looking at the agent. Use channel-specific silencing (drop BL and LPR from the read set while glare is up) or a dyad-learned attenuator. Recheck J35 (anger, anger with heavy breathing, concentration: no posture), B2 (grief plus squint at the agent: posture on within 4 s), and J34. The routes critic checks R48.
2. **Recogniser watermark (§4).** Gate frame s only on words whose finalized-through time is ≥ s + λ_w, else 0. Name the recogniser candidates honestly: expected δ_g is about 0.9–1.0 s, not 0.80. Add the language and runtime conditions, and a breathing-sensor check, to week 0.
3. **The Build-candidate summary**, corrected as below.

Everything else holds. I would not ask for another critique round of the agent side after these three, beyond a recheck of the B2 and J35 numbers. The routes critic's verdict on R40′, R47–R50 and R1g is still needed.

### 6.2 The Build-candidate summary, corrected

**One line.** A conversational agent whose face and voice come from an inner state that knows the operator closely but can move toward him only through innately capped, per-expression, context-gated paths. Claude writes its words through his Claude Code subscription and is never told the state.

**What the operator would get.**
- **Laughter and smiles.** His smile and laugh are returned within about a second in ordinary talk, teasing, reunions and warm evenings: laugh back +0.14–0.19 sounding 0.8–1.0 s after his (the exact delay is set by the on-device recogniser in week 0), lip +0.04–0.11. They are not returned at grief, mockery, misfortune, or a laugh that ends a bad-news sentence.
- **A look of concern.** It appears within 2–7 s of silent sadness, grief, crying or silent panic, for quiet and differently expressive faces too, graded by how distressed he looks. It is never a copy of his brow, and it is released when his distress ends. **Exception:** it reads only what it does not show, so distress that shows only in his inner and outer brows gets no look until he speaks or the agent asks after him (about 50 s; up to 2 min for a very quiet face).
- **Strong expressions from its own appraisal** of his words and face: brow 0.5–0.7 at "my father died", hurt after insults, lip 0.6 at good news.
- **Replies after about 2.2 s** through his subscription. The agent speaks first after 18–60 s of silent sadness or crying.
- **A testbed.** Every route from his face to its face is named, bounded, monitored by a shadow ledger, and can be lesioned.

**Novelty verdict: recombination, stated plainly.** Every part exists: per-channel capped reflexes, a monotone additive gate, ridge readers, a decaying trace, McGaugh-weighted replay, a perturbation probe, an incremental recogniser. What is new is the composition:
- knowing separated from moving, with a per-channel cap on every path;
- situational competence learned by watching recorded strangers and composed through the listener's own body state;
- the agent hearing its own Claude-written words;
- a concern reflex whose sensors are disjoint from its effectors.

No new core mechanism. The search continues in parallel (D82).

**Remaining operator choices, and what happens with each.**
- **Q24, the concern look before words** (open):
  - **Own concern posture (built, recommended):** a steady look within seconds at visible distress, never a copy of his brow; but brow-only sadness gets nothing until words.
  - **Raise the brow ceiling toward 0.7 instead:** sympathy shows only as a stronger mirror of his own brow, so brow-only sadness is answered, but his brow is copied far more in general.
  - **No look until he speaks:** a near-neutral face for the first 20–60 s of silent sadness.
- **Within the posture:**
  - **Graded (built):** a mild face gets a light look, sobbing a strong one.
  - **Binary:** the same look whenever it is on. With the new read set this costs no copying, only nuance.
- **If the recogniser is too slow (stable latency above 0.75 s):**
  - **Keep a laugh echo judged by the previous sentence:** fast laughter stays, but "I got fired today, haha" is laughed back.
  - **Keep only the smile echo:** no fast laugh back, never a wrong one.
- **If the gate fails on Seamless (F15):**
  - **A context-free laugh echo:** D81's fast mimicry is kept, but grief and mockery laughs are sometimes returned.
  - **No fast laugh echo:** always appropriate, less alive.
- **The coping joke while sad:**
  - **Silent and gentle (built):** no laugh at a joke made while sad.
  - **Let the corpus's 0.39 through:** a small laugh back, as recorded listeners do.
- **Draft model:**
  - **Haiku:** shorter "considering" beat.
  - **A larger model:** better words, slower replies.

**Main risks to watch in testing** (judged on internal state).
- **Steering.**
  - Hold his words fixed and move only the laugh's timing relative to the bad-news word: the laugh back should switch off within 0.25 s of the word's end.
  - Clamp his brow, outer brow and lip to rest while he is sad: the posture's amplitude must not change (F18).
  - Swap Claude's reply for a neutral text: only Λ_V(own) may change (F19).
  - Clamp the agent's own face input to the gate: grief laughter should stay unreturned through his face and words.
  - **New:** hold a crying face fixed and add only lid tightening while he looks at the agent: the posture must stay on.
- **Lesions.**
  - The posture's read set (restore BI: the brow-copy slope returns).
  - Breathing (silent panic loses the posture).
  - The probe (answering concern latches).
  - The word timing (bad-news laughs are returned).
  - The gate on the play laugh, D_s, and the gate and Λ themselves.
  - The threat silencing (an angry face of a different-channel user starts the posture).
- **Coupling beyond surrogates.**
  - Per-channel pooled slopes at 2 s, 10 s and 1 min under partner-swap, segment-shuffle and timing-resample surrogates, with the gate and the posture live.
  - The posture's causal slope on his BI should be indistinguishable from 0. Its pooled slope over his sadness should survive shuffles that keep his sadness and break his brow.
  - How often the ledger binds on natural partners.
- **The dyad fit on real data.**
  - F15, F16 and F21 on held-out people.
  - The counts of rare laughs.
  - Whether sympathetic smiles pin monotone inputs at 0.
  - D_s's real weight.
- **Live.**
  - The recogniser's stable latency and finalization watermark (week 0); the breathing sensor at his desk.
  - F20: the laugh synthesizer within 2 s of his laugh ending a sentence of loss, insult or harm.
  - The posture's on/off rate per hour at constant faces, and how often the probe releases genuine sadness.
  - How often his distress shows only in the brow, and how often in a squint at the screen.

## Sources read

| Source | How read |
|---|---|
| brief.md | in full |
| research/questions.md | Reports 5–6, Q19, Q20–Q23 with answers, Q24, Q25, Q26 |
| DECISIONS.md | D78, D80–D85 |
| research/foundations/designs.md | in full |
| research/foundations/critique-7-design-cayley-ledger-agent.md | in full |
| research/foundations/design-cayley-ledger.md (revision 8) | in full, §0–§10, revision 7 critiques and answer, revision 8 history, Build-candidate summary |
| sims/design-g8/checks.py and out.txt | Agent8, J34–J39 code read; out.txt J31–J39 read; engine loaded and reused by my scen.py |
| sims/design-g5/checks.py, design-g6/checks.py, design-g7/checks.py | grep-read: Π₀ and its inverse, his codes, Person, run6, glare, MASK |
| sims/critique-cayley7-agent/scen.py | read (method reused) |
| Kyutai delayed-streams-modeling repository (github.com/kyutai-labs/delayed-streams-modeling) and its search summaries | 0.5-s delay of stt-1b-en_fr, word timestamps, MLX example for the 2.6B model, 1B model on iPhone |
| Apple developer forum thread 794720; WWDC25 session 277 (search summaries) | volatile and finalized results; reported finalization delays 1.45–2.2 s (anecdotal) |
| Smoski and Bachorowski 2003 (abstract via search) | definition of antiphonal laughter; exact window not confirmed |
| **Named only, not re-read:** Provine 1993 (laughter at phrase ends); Ekman's "reliable" grief muscles; Prkachin's pain action units; Mauersberger 2022 | nothing here rests on them beyond what is stated |

**New checks:** `sims/critique-cayley8-agent/scen.py` (B1 brow-only sadness, two codes; B2 tearful or pained squint looking at the agent; B3 naturally fluctuating silent sadness and the probe), output in `out.txt` (engine load 29 min, which is the design's own cost; scenarios 12 s).
