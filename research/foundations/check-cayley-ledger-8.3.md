# Check of the Cayley–ledger revision 8.3 face-only reset

Independent checker, 2026-11-26T17:55:47Z

**Standard:**
- questions.md Q19: concrete failures only.
- D78, especially condition 4: copying must never become a state the agent settles into.
- D81–D85.
- Q24: still open; the design follows its recommendation.
- Q27.

**Scope:** the 8.3 rule only. His decoded distress words (C_L) and his sobs reset the face-only clock. His voice (V_v) and breathing only extend the face-only maximum from 180 s to 600 s. The refractory period is 120 s. I also checked the changed concern-posture text (§2.1, §2.10) and the Build-candidate summary.

**Checks:** `sims/check-cayley83/check.py` (X1–X4; output in `out.txt`).
- It loads the engine exactly as `sims/design-g83/checks.py` does and takes `Agent83` and `stretch()` from that file's text, unchanged. Its M1–M5 loops are skipped.
- One engine load (about 4 min); 8 min in all.
- The run printed every result, then stopped on its last line, a timing print (`NameError: time`, in `err.txt`). That line is fixed in the script. No other line changed, so the run was not repeated.
- No processes are left running.
- As before, these are constructed partners and a constructed word decoder. They test the design's rules, not people.

## Verdict: PASS (no concrete failure; one residual made sharper, and summary corrections)

**The bound holds by construction and in every run.** Without distress words or sobs, no partner keeps the look longer than 600 s at a stretch or more than 600/720 of the time. I tried:
- voice and breathing timed to the refractory window;
- soft evidence present only when the clock passes 180 s;
- 20-s release gaming just before 600 s;
- random voice and breathing schedules.

The posture's longest stretch without words or sobs was 600.0 s and its highest duty 81.9 %. The visible look reached 612.0 s and 83.7 %.

**Ordinary words do not reach presence.** Neutral words, hedges and "I'm fine" decode below presence. Interjections such as "hmm" and "yeah" are removed by the ASR normaliser before any reading.

**The residual is stated correctly and is not a D78-4 failure,** though it should be described more precisely. A partner who sobs in answer to the look, or who keeps saying distress words, keeps the look. That is concern at expressed distress in channels the agent never shows. No agent channel is copied.

## Evidence

### 1. Can any partner hold the look past 600 s, or above 600/720 of the time, without words or sobs? No.

**X4.** The partner's face was the C1b answerer, his voice was EN −0.05 and his breathing was at β 0.9. Codes: operator and different channels; 60 min each.

| Strategy | Longest stretch without words or sobs: posture (visible) | Posture on (visible) |
|---|---|---|
| voice only in the refractory window | 180.0 s (191.5 s) | 38.2 % / 16.4 % (as with no voice) |
| breathing only in the refractory window; voice and breathing in it together | 180.0 s (191.5 s) | 43.6 % / 21.8 % |
| voice bursts only while the clock is at 150–180 s | 271.0 s (282.5 s) | 68.1 % / 39.4 % |
| breathing from clock 170 s | 600.0 s (611.5 s) | 81.9 % |
| voice every 60 s, plus breathing in the refractory window | 600.0 s (611.5 s) | 81.9 % |
| release gaming: neutral face for 25, 60 or 115 s when the clock reaches 570 s, voice every 60 s | 593.0 s (visible **612.0 s**) | ≤ 81.9 % (visible **83.7 %**) |
| 8 random voice and breathing schedules per code | 600.0 s | ≤ 78.2 % |

**Why the timing strategies do nothing:**
- In the refractory window, `Agent83` sets the whole face load to 0 unless words or sobs are present. Onset reads only that load and sobs, so voice or breathing in that window can neither restart nor grade the look.
- A 20-s release does not reset the clock, so a look that comes back is still withdrawn at 600 s.
- The visible margin is 0.5 s wider than the author's 611.5 s. That is the same bridge across a release and its sensitized re-onset that the check of 8.2 measured for the 180-s limit. The summary's "about 612 s, 84 %" covers it.

**X1: can ordinary words reach C_L presence?** C_L is the 40-s low-pass of 𝒟_p(N_L), the decoded need of his words, and N_L decays with τ 1800 s. Presence needs 𝒟_p ≥ 0.02. Without noise, that is decoded V ≥ 0.21 alone, A ≥ 0.34 alone or T ≥ 0.42 alone. The decoder was run 200 times per latent, with 0.15 embedding noise:

| His words (constructed latent) | P(𝒟_p ≥ 0.02) | How long C_L stays present (median) |
|---|---|---|
| neutral ("yeah", "ok"); "I'm fine" | 0.00; 0.01 | 0 s |
| hedge ("I don't know, I guess") | 0.07 | 0 s |
| small talk ("anyway, how was your day?") | 0.12 | 0 s (max 158 s) |
| "meh, so-so"; "a bit tired" | 0.26; 0.36 | 0 s (max 750–800 s) |
| "I'm okay, just a bit tired"; "long day"; "busy, a bit stressed"; "not great" | 0.81–0.97 | 340–630 s |
| the author's "just tired, things at work" | 1.00 | 1158 s (max 1488 s) |

So neutral and hedging words do not reach presence. Mildly negative remarks usually do, for about 2.5–10 min, and the author's explicit reply for about 20 min. In the real build, which words count is set by the population reader on real text, so this mapping belongs on the week-0 risk list (see section 4).

### 2. The residual: answering with sobs or words

**Sobs (the author's M4, re-read).** The partner sobs in answer to the look: v_sob = 0.20 × a 30-s low-pass of the look. He keeps the look 100 % of the time, agent brow +0.235. Sobs count as present only from v_sob ≥ 0.103, sustained.
- **This is acceptable.** Sustained sobbing is crying, whatever started it, and a concerned look at a crying person is what the look is for.
- **No agent channel is copied.** The agent has no sob output, and the posture never reads its own effectors.
- **D78-4 is not met.** It concerns copying becoming a settled state. Here the partner's channel is not a copy of anything the agent shows.
- **Build risk:** whether the live tracker confuses laughter bursts with sobs (BU_L against BU_S). That belongs in the week-0 checks.

**Words that answer the look (X2).** The face is the C1b answerer again, 60 min, in two codes.

| His words | Posture on (operator / different channels) | Agent BI mean |
|---|---|---|
| none (control: the face-only cycle) | 38.2 % / 16.4 % | +0.080 / +0.020 |
| "just tired, things at work", 10 s after each return of the look | 92.7 % / 92.7 % | +0.302 / +0.259 |
| the same, every 20 min | **100 %** / **100 %** | **+0.332 / +0.286** |
| "I'm okay, just a bit tired" or "long day", after each return | 74.5–75.8 % | +0.18 to +0.22 |
| the same, every 20 min | 67.3 % / 35.3 % | +0.18 / +0.07 |
| control: sad until 40 s, then a neutral face; "just tired" every 20 min | **0 %** | +0.091 |

**So C_L can be an answering route.** A partner who answers the look's return by naming his distress, or names it every 20 min, holds the look at the highest agent brow of any partner checked in 8.2 or 8.3 (+0.29 to +0.33).

**The words alone do not hold it.** With a neutral face, the same words start no look at all, because onset reads only his face load and sobs. The look and its full amplitude come from his face answering it. The words only stop the clock that would otherwise cut that loop.

**Why I do not count this as a concrete D78-4 failure:**
- The words that do this are explicit distress content. "Just tired, things at work" is the author's own genuine-distress case. Mild remarks give only 67–76 %. Neutral words and hedges give nothing.
- No agent channel is copied: the look carries no words.
- The agent's own words cannot feed C_L (rule 12′).
- The design states this residual and lists it among the risks.

**But the summary should state it as it is,** not only as "one who sobs or names distress in answer keeps it" (correction 4 below): a sad-looking partner who keeps saying he is tired keeps the full look indefinitely, at a higher brow than any other case.

### 3. Anything else broken by 8.3? No.

- **Face-only bounds are unchanged.** The X4 refractory-only strategies and the X2 face-only controls fall at or under 180 s and 60 %, and the author's M2 agrees (≤ 180.0 s, ≤ 60.0 %).
- **Genuine distress with words or sobs keeps the look.** The author's M3 is consistent, and X3 reproduces it: words present until 1348 s, first withdrawal at 1527.5 s.
- **Totals are untouched.** The diff from r8.2 touches no fast or gated route, and R1g (≤ 0.53 c BU_L, ≤ 0.31 c LP, ≤ 0.35 c CR) is unchanged.
- **Spec precision (not a failure) — the clock against the refractory rule.** Two places disagree slightly, and each is safe on its own:
  - The text resets the clock only by words, sobs or T_ref without the look. `Agent83` sets it to 0 at withdrawal.
  - The text says the refractory period blanks "face and breathing". R_p and A_b also include his voice when he speaks, while `Agent83` blanks the whole load.
  - A build that took the code's reset and the text's narrower blanking together could let his voice restart the look during the refractory period with a fresh clock.
  - **Fix:** state that the refractory period blanks the whole of L_p, voice included.
- **Text:** §2.1 and §2.10 say C_L is "appraised through Claude". C_L is 𝒟_p(N_L), the population reader on his recognised words (r5 §2; §2.4.2 here). Claude's text is kept out of it by rule 12′. Say "decoded by the population reader".

### 4. Build-candidate summary: mostly accurate; corrections

**Accurate:**
- the 600/720 (83 %) and 180/300 (60 %) bounds;
- "voice and breathing lengthen, never renew";
- the visible margins (about 612 s, 84 %);
- the voice-only and panic-only cost of 10 min on, 2 min off (when the voice reading stays present);
- the risks that were added (the V_v threshold, accommodation, how often each limit binds, the residual).

**Corrections:**
1. **Q24, built option:** "steady while his words, voice, sobs or breathing also show distress" is 8.2's rule. Change it to "steady while his words or sobs also show distress; his voice or breathing extend it to 10-min pieces".
2. **Voice-only distress:** "10 min on, 2 min off" holds only while he speaks at least about every 90 s. With longer pauses, the look is withdrawn at the first lapse after 180 s. In the author's M1, stretches were 271 s and the look was on 64–66 % of the time (25–29 % for a different-channel user). The 8.3 history says this; the summary does not.
3. **"One reply keeps it for about 21 min"** is the upper end. It holds for the author's explicitly worded reply, and only if he says nothing else with content.
   - Any later neutral sentence replaces the reading. X3: "anyway, what's new?" ends C_L within about 70 s, and the 180-s limit follows.
   - Milder replies ("long day", "not great") keep it about 2.5–10 min.
   - Say "up to about 21 min".
4. **The residual, stated concretely:** "A person whose face answers the look and who names his distress each time it returns, or every 20 minutes, keeps it 93–100 % of the time at the strongest brow seen (+0.29 to +0.33). The words do not start or hold the look on their own (neutral face: no look); they stop the limit from cutting his face's answer."
   - Add to the risks: which everyday remarks reach C_L presence in the real reader, and for how long (constructed: mild remarks such as "long day" or "not great" 0.8–0.97 of the time, for 2.5–10 min).
   - Add to the risks: laughter misread as sobs, a week-0 tracker check.
5. **Optional precision:** the visible extended stretch is up to 612 s and 83.7 %, measured with release gaming.
