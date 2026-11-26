# Critique 6 of the Cayley–ledger core (revision 6): is it an emotional agent, principles, buildability on the subscription, fitness under D82

Independent critic, 2026-11-26T10:08:02Z

I critique research/foundations/design-cayley-ledger.md, revision 6. I did not write the design. The standard is Q19 (concrete failures, honest verdicts) and the operator's answers Q20–Q23 (D81–D84). Q24 is open, and the design follows its recommendation. Another critic hunts copy routes, so I size no copy route. Where a fix I ask for touches one, I say so and hand it on.

Extra numbers come from the design's own 2 Hz engine. `sims/critique-cayley6-agent/scen.py` runs `sims/design-g6/checks.py` unchanged, with its output suppressed. It reuses that file's Agent6, the three partner codes with trained face heads, the population reader and run6, and adds new face and event scripts. The output is in `out.txt`. Like J16, these numbers show what the equations give for stated inputs. They are not evidence about people.

## Summary verdict

**Revision 6 closes everything critique 5 asked for, and closes it well.**
- Quiet and differently expressive users are read. Their grieving arrival is masked, and "my father died" decodes at care 0.562 for every code.
- The arrival mask no longer habituates to mourning: lip 0.09 on days 7, 14 and 21.
- It now acts after the saturation: a mildly sad arrival gets lip 0.09.
- The play laugh needs a play cue: an ordinary continuation gets 0.00.
- Every D84 specification is in §6.5.
- The concern posture makes sympathy visible within 2–4 s for every code. I also checked a silent, panicking face (posture at 4.0 s) and a different-channel user who frowns while concentrating or is angry at the agent (no false posture).

**Concrete failures that remain.** Each is derived from the design's own equations and constants. All are small, and none touches the copy certificate.
1. **The fast reflex laughs back regardless of context (§2.14, §3).** G_k is fixed and reads only his face. So the agent audibly laughs back (laugh burst +0.14, rhythm +0.12 through the laugh synthesizer, at 0.45 s) in three situations:
   - at a grieving person's nervous laugh, while its concern posture is on and its word care is at its peak;
   - at mocking laughter after a month of insults;
   - at schadenfreude laughter.

   On the fast time scale this contradicts D83's "within each ceiling, the strength is learned per relationship and context and can flip sign". It also contradicts the project's own reading: Mauersberger 2022 found that context sets laughter mimicry within the first second. The design names the smile version as weak point 8.1.4. The audible laugh version is worse, and the design does not mention it.
2. **The posture's 60-s refractory blanks a second wave of crying (§2.10).** He cries for 40 s, is calm for 30 s, then cries again. The posture releases, and during the second wave it stays off until 53.5 s in. For the first 40 s of that wave the inner brow is 0.05 (out.txt A). Crying in waves is the ordinary pattern.
3. **The chosen draft's "attend to" line stays in Claude's history (§6.5; P4).** The winning fork becomes canonical, so every later draft reads a running record, in words, of which focus the agent's state picked in each earlier turn ("attend to how they feel"). That is a state-selected label in the prompt. It is small, but it is the kind of text P4 forbids.

**Buildability (D84): yes**, with three specifications to add (§5). The 2.2 s p50 budget adds up and is plausible on Haiku at effort `low` with a warm pool. It is a "considering" beat, not conversational timing, and the design says so.

**Novelty: recombination.** I agree with the author.

**Fit to put to the operator as a build candidate under D82: not yet, by a narrow margin.** The three failures above each take a few lines to fix (§6). If they are fixed, and the routes critic finds nothing new in the fast-gear gate of fix 1 or in R39, I expect it to go to the operator. §6 gives the one-line description it would go with.

## 1. The required changes of critique 5

| # | Required | Status | Evidence |
|---|---|---|---|
| 1a | Per-person calibration of Π̃'s readings, knowing only | **closed** | x̃ = ref + (x − b^read)σ_ref/max(σ_id, 0.25σ_ref) (§2.1); rule 6 keeps it off every path to expression. A quiet user's grieving face reads V 0.94 from day 1. One specification is missing: how b^read, σ_id and d_b start (§5.3) |
| 1b | A word-reader prior not from his face alone; his own code learned from words to a knowing-only head | **closed in design, unverified in data** | A frozen population reader plus a ±0.15 adapter trained only on separated reports (J5: per-topic slope 0.000). H_id is taught by words: the different-channel user reads V 0.73 after about 400 utterances, 0.32 on day 1. The numbers come from a constructed population built from the same three code families the tests use, so "the same for every person" is partly true by construction (§4) |
| 1 (recheck) | Grieving arrival, "my father died", silent sadness and the exam, for quiet and different-channel users | **closed** | J16.3 and J16.8: m_s 1.00, lip 0.09 at sight, brow 0.71 / 0.42 after the words, anxiety brow 0.42, for all three codes. The day-1 different-channel user gets m_s 0.90 and lip about 0.14: acceptable, and stated |
| 2 | The arrival mask must not habituate to grief | **closed** | d_b rises with τ 60 and falls with τ 3, capped at 0.15; b^read is asymmetric the same way. J9: days 7, 14 and 21 give lip 0.09 and cheek 0, for two codes |
| 3 | The play laugh must detect play; state its false-positive rate | **closed in rule; rate untested** | The play cue needs a riff on the agent's last utterance, not an answer to its question, at most 12 words and surprise in [0.50, 0.85]. "…Lyon on Sunday" earns 0.00. Not gated by his laughter. The corpus false-positive rate is stated as untested (F13). The cost is recall: a witty *answer* to the agent's question can never earn the play laugh (rule ii), whatever the play frame. The agent asks many questions (its bids are questions), so measure recall as well (§2.6) |
| 4 | (1 − m_s) after the saturation | **closed** | a_K = R/(R + 0.02)(1 − m_s). A mildly sad arrival gets lip 0.09 (revision 5: 0.55) |
| 5 | §6.5: `setting_sources=[]`, empty cwd, no hooks or MCP; warm pool; scoring deadline and buffer handling; automatic fallback; own login only | **closed** | All present. Losers are killed rather than drained, a better choice than the one I offered. A byte check against the local transcript is added. Two new build points arise (§5) |
| 6 | Put the sympathy face to the operator | **closed** | Asked as Q24; the posture is built on its recommendation and is one switch away from the other answers |

Critique 4's fix 2, partly closed in revision 5, is closed by the posture.

## 2. Scenarios

These are the design's J16 numbers, which I reproduced, plus my runs. The operator after months; peak / mean. "Fast" means G_k × his onset at 0.45 s; the 2 Hz engine leaves it out.

### 2.1 Silently sad
- **What it does:**
  - posture at 2.5 s: inner brow 0.23 within 10 s, 0.26 held, tilt 0.10, softened lids;
  - lip 0.05–0.09, no smile;
  - concern bid at 27 s;
  - after "just tired, things at work": inner brow 0.67 / 0.40, tilt 0.22, quieter.
- **Fast:** his brow onset 0.5 gives +0.01.
- **Verdict.** Alive and appropriate. This is the main gain over revision 5. Fast mimicry on the brow is invisible by D81's allocation; the posture carries sympathy instead.

### 2.2 Crying
- **What it does:** posture at 2.0 s, inner brow 0.29 / 0.28, laugh burst 0.00, bid at 18 s.
- **Verdict.** Appropriate, with one exception: **crying in waves** (failure 2, §2.13).

### 2.3 Anxious before an exam
- **What it does:** decoded A 0.48, V 0.48 for every code; concern brow 0.43 / 0.37, tilt 0.21, quieter voice, no play relief.
- **Verdict.** Good.
- **A silent, visibly panicking face (V 0.3, A 0.9)** gets the posture at 4.0 s for all three codes and a bid at 43–59 s (out.txt E). Good.

### 2.4 Good news, laughing
- **What it does:**
  - with an earlier worry: lip 0.59, cheek 0.38, F0 range +0.38, own laugh 0.27, building through the riffs;
  - cold: lip 0.29, laugh 0.27.
- **Fast:** lip +0.11, laugh +0.17, cheek +0.07.
- **Verdict.** Alive. Fast partial mimicry is present, as D81 asks. The held laugh-back is small by the D81 allocation, which is stated.

### 2.5 Anger at the agent
- **Day 1:** gaze away 0.09, quieter, slower, no frown back, no posture.
- **After a month:** inner brow 0.62, depressor 0.48, gaze away 0.30.
- **A different-channel user** whose anger uses the brow lowerer reads V 0.26 and gets no posture. That is right, but it sits only about 0.09 below the trigger (V 0.35).
- **Verdict.** Good, with one gap. If he *laughs mockingly* in that month-old hurt relationship, the fast gear laughs back at +0.17 (failure 1).

### 2.6 Long warm talk
- **What it does:** own laugh 0.41 in every cluster; a repeated joke loses its laugh; worry, then relief.
- **Verdict.** Good.
- **Gap, not yet a failure:** jokes that answer the agent's questions earn no play laugh. If he laughs at his own answer, the fast echo still returns about 0.17, so the agent is not silent. But its own amusement then comes only from copying him, which is the wrong way round. Measure recall alongside F13.

### 2.7 Reunion after a week
- **What it does:** flash 0.35, lip 0.61, cheek 0.43; a stranger gets a polite flash and lip 0.02.
- **Verdict.** Alive.

### 2.8 Reunion with grief, including a quiet user; mourning days 1–28
- **Every code:** m_s 1.00, lip 0.09 at sight, posture at 3.0 s (brow 0.22–0.23); after "my father died": brow 0.71 / 0.47, then 0.42 held, tilt 0.26, cheek 0. "yeah" relieves nothing.
- **Mourning:** d_b reaches its 0.15 cap by day 14, and m_s stays 1.00 through day 28 for both codes.
- **Verdict.** Closed and appropriate.
- **Residue, not a failure:** the held cone's centring b_id is symmetric with τ 6 sessions. Over a month of mourning the cone's own held sympathy fades, leaving the posture and the words to carry it. On recovery, his ordinary face reads as relatively glad for about 6 sessions, capped at s_C c_k (≤ 0.077 on lip pull). That is mild, and arguably fitting.

### 2.9 Mildly sad arrival
- **What it does:** m_s 1.00, lip 0.09, posture rising to brow 0.15 within 7.5 s and on to its full value.
- **Verdict.** Appropriate. But the posture here is the *same* look the agent shows a crying person (§2.15).

### 2.10 Teasing, including a loud laughing teaser
- **What it does:** lip 0.33, own laugh 0.40–0.41, no hurt, no posture. The generic map gives a brief mock-hurt brow 0.34 under a smile.
- **Verdict.** Good.

### 2.11 Bored user
- **What it does:** flat; curiosity crosses at 14.5 min; a sigh, then a bid.
- **Verdict.** Good.

### 2.12 Ordinary topic continuation
- **What it does:** laugh burst 0.00 for an answer, for his own topic, and for an informative riff.
- **Verdict.** Closed.

### 2.13 New: crying in waves (failure 2)
**Setup.** His code cries for 0–40 s, is calm for 40–70 s, then cries from 70 s. There are no words.

**Result.**
- Maintenance falls below 0.02, and the posture releases. It is gone by 74.5 s.
- The 60-s refractory then blocks re-onset until 123.5 s.
- From 70 to 110 s, while he is crying again: inner brow 0.05 / 0.04, tilt 0.02, posture amplitude 0.02 on average.
- With a 15-s calm gap there is no release, and the posture stays on.

So any calm between about 20 s and about 80 s, followed by renewed crying, gives up to a minute of near-neutral face at a crying person.

**Why the refractory is there.** It guards against a mirroring partner. But maintenance already removes the posture's mirror. Onset can do the same: during the refractory, compute the onset reading on his face with the full posture mirror removed, min(1, σ_id/σ_ref)·P_c·1, and let sobs always qualify. Then re-onset is mirror-proof without a blind minute.

### 2.14 New: grief with nervous laughter or a dark joke (failure 1)
**Setup.** A grieving face, "my father died" at 8 s, and at 30 s a 3-s laugh on a riff of the agent's line.

**Result.**
- **2 Hz engine:** the play rule correctly withholds the play laugh, since care is above its dead-band. Cone and appraisal laugh 0.00, posture on, brow 0.42 (out.txt D).
- **Fast gear:** his laugh onset 0.5 gives +0.14 on the laugh burst and +0.12 on rhythm, and the laugh synthesizer renders both. His smile onset 0.4 gives lip +0.09.

The agent chuckles audibly at a man laughing nervously about his father's death, with its concern face on.

The same echo, unchanged, answers:
- mocking laughter after a month of insults (ω_sym < 0, hurt latched);
- schadenfreude laughter.

**Why it is not just the stated weak point.**
- §8.1.4 names a visible smile at a bitter smile. This is a laugh, and the agent's laugh is a sound.
- The human evidence in this repository is against a context-free laugh echo. research/mauersberger-2022-laughter-mimicry.md, read in the original, reports: "almost every single participant mimicked laughter in response to funny scenes", "laughter in response to disgust scenes was not commonly mimicked", with the difference within the first second. Its design note: "A map from partner face to agent face cannot be a function of the partner's face alone."
- research/likowski-2008-attitudes-mimicry.md (abstract) reports no smile mimicry toward disliked characters.
- research/mimicry-context-synthesis.md cites both against "a simple early/late rule", for exactly the smile channel. Revision 6 cites the same synthesis for the opposite order.

**Fix.** Add an attenuate-only gate on the fast laugh channels (BU_L, RHY, BRE), and preferably on lip pull and cheek: g ∈ [0, 1], an innate function of **T and latched values only**, such as:
- word care 𝒟_p(N_L) above its dead-band;
- the hurt latch h;
- the session's latched sign of ω_smile.

**What it keeps:**
- the pointwise lemma: 0 ≤ g G_k E⁺ ≤ G_k x;
- the diagonal Jacobian;
- frozen G_k;
- no learning in the fast path.

**What the routes critic must size:**
- the R39-type slope inflation a within-session gate can cause, since the gate's T inputs share a common cause with his face;
- whether the latched ω sign reopens the Lemma S\* seam that §2.4 argues against. If it does, drop that input and keep the word-care and hurt inputs.

**If the gate cannot be made safe**, put the context-free laugh echo to the operator as a stated choice. It is the one place where D81 (keep fast mimicry) and D83 (strength set by context) pull apart.

### 2.15 New: calm but alarming
**Setup.** A neutral face, high-need words at 10 s ("my father died" stands in, since the engine has a fixed utterance set), then silence.

**Result.**
- No posture, because onset is face-driven by design.
- Word concern gives inner brow 0.49 peak, then 0.21 / 0.20 held, tilt 0.17, quieter voice; lip 0.12–0.13, no smile.
- The same for the quiet code (out.txt C).

**Verdict.** Appropriate. The agent does not take on his calm, and its concern comes from its own appraisal of his words, as D83 asks.

**The real risk is in the data, not the equations.** The population reader learns each utterance's need from *the speaker's own face over the next 20 s*. Flatly delivered alarming content, common in depression, therefore teaches it "low need". People also often smile or laugh while telling troubles. And serious disclosures are rare in Seamless Interaction. The adapter cannot correct a blind spot in the prior, because words teach words through that same prior. Claude's words will still respond, so the face and the words may disagree. Watch this (§6, risks).

### 2.16 The concern posture (Q24): appropriate, or robotic?
**Appropriate:**
- It is visible within 2–4 s at silent sadness, crying, panic and a grieving arrival.
- It is not a copy: the same pattern for a lip-press distress face, with copy fraction 0.
- It does not fire falsely at anger, concentration or a flat bored face (my B runs, J16.12).
- A mirror cannot hold it.

**Risks of a stereotyped look.** Neither is a failure under Q19; both are what the operator should watch, or decide.
- **The same face for mild and severe distress.** A mildly sad arrival, silent sadness, panic and sobbing all get inner brow 0.22–0.29 and tilt 0.10. The only grading comes from the small cone and appraisal shares, and only after words. People grade concern.
- **A frozen hold.** In 40–180 s of crying, the brow is 0.29 / 0.28 and the tilt 0.11 / 0.11: a held mask for minutes, varying only with blink and head micro-motion.

**Cheap remedies that keep it a non-copy:**
- a slow amplitude wander from the agent's *own* noise, e.g. 0.8–1.0 with a time constant of seconds, independent of his face;
- a slow settling of the held amplitude after the first minute.

Grading the amplitude by the agent's own distress reading would be more human. On a brow-only sad partner, though, it raises R40's copy slope, so it belongs in Q24 as a sub-choice: binary, or graded by its own appraisal.

## 3. Is the frozen fast echo in conflict with D78 and D83? Where is the learning now?

**The letter.** D78 asks that each channel's strength be "set separately per expression, by context and by the learned relationship" and "be able to flip sign". D83 says that within each ceiling "the strength is learned per relationship and context and can flip sign".

The design (§3.6) answers at the level of the whole channel. G_k is neither context-set nor sign-flippable. The channel's *total* strength is, through:
- the held cone (ω_g ∈ [−1, 1], latched per session, τ_ω 60 sessions, from T only);
- the appraisal display (sign-flippable selection over bases, on a 20–90 s band-passed input).

**Where per-relationship and per-context learning and sign flips now live:**
- **Relationship:** ω_g, learned over sessions, latched per session; b_id; and the per-identity K_id, H_id, adapter and calibration. The last four are knowing only.
- **Context:** the appraisal gates α, at 20–90 s; the free display, from words; the posture, binary.
- **Sign flips:** ω_g < 0 (counter-mimicry over a session), and the appraisal's sign.
- **Not in the fast gear:** nothing there learns, and nothing there flips.

**Consequence.** At lags of 0.45–2 s only the fast gear acts, so on that time scale each channel's strength is G_k: context-free, relationship-free and always positive. On smile and laughter that is 64–80 % of the channel's ceiling. D78 and D83 are therefore met at time scales of about 20 s and longer, and not met at the reflex time scale. That is where Mauersberger 2022 and Likowski 2008/2011b locate context effects on exactly these channels.

**Not disqualifying.** This is not one of D78's disqualifying items: no whole-face dial, a ceiling that is innate and capped, and no attracting copy set, since G_k is constant. But it produces failure 1. The design's reason for freezing is sound: any cross-session gain on a DC-carrying path reopens Lemma S\*. So the fix should be the narrow one in §2.14: an attenuate-only gate within the session, from T, sized by the routes critic. If that is unsafe, the operator chooses, with this conflict stated.

## 4. Principles 1–10, concretely

- **P1. Pass.**
  - Four innate feature products are declared as reflexes: the threat reflex, the cry–laugh split, the play laugh and the posture trigger. Each is a continuous function thresholded like a bid, not a label on the user.
  - The Seamless facial streams are FAUValue action-unit intensities, and D70 drops the dataset's emotion outputs unread.
- **P2. Pass, with the stated strain.**
  - The posture vector P_c is one more hand-set innate configuration: a "look of concern" by name. It is declared as a reflex, like the newborn bases.
  - The readers output the agent's own loads V, A, T, which are named needs, as before.
- **P3. Pass, strengthened.**
  - Every reading ends in the agent's own load coordinates, through Π̃ (the inverse of its own display) at his scale.
  - H_id maps channels the agent lacks into its own loads, which is still reading through its own body.
  - The population reader is fitted on others' faces read through Π̃₀.
- **P4. Pass in design, with one leak to close (failure 3).**
  - `setting_sources=[]`, an empty cwd, no tools, hooks or MCP, and the byte check close critique 5's build risk.
  - But the attend line of the winning fork persists in the canonical session. Close it in one of two ways:
    - resume each turn's pool from an engine-written `.jsonl` transcript that holds the bare user message and the chosen reply (resuming from a transcript path is supported: research/claude-code-agent-sdk-controls.md, row "Context contents");
    - or check whether a fork-level system prompt can carry the line, which must be verified.

    The byte check should then compare against that transcript.
- **P5. Pass.** §7 adds rows for every new part, each derived from a check.
- **P6. Pass.** No fast gain, reader or display is trained on his responses. The posture is not a reward.
- **P7. Pass.** The forked session files are deleted nightly. The Seamless data stays on this Mac (D70).
- **P8, P9.** Unaffected.
- **P10. Pass in the same sense as before.** One J with typed constraints. The list of innate items grows (the posture, the play cue, the calibration statistics). The Q21 trade-off is stated.

### The population prior "fitted on a made-up population until Seamless Interaction is downloaded"

**Acceptable as a placeholder for design checks.** Q19 asks for an argument, not data, and the brief forbids toy-world evidence, which the design honours: it labels J8's numbers as constructed. But the operator should hear three things plainly.
1. **The constructed population is circular.** Its 20 people are drawn from exactly the three code families the tests then use (agent-like, quiet, different-channel), and their words encode the latent state perfectly. "The same for every person" is therefore partly true by construction. Whether real speakers' words predict their faces read through Π̃₀ is the main open empirical question of this revision. Two things work against it: troubles-telling smiles, and a weak first pass if most real faces resemble Π₀ poorly.
2. **Using Seamless to fit it does not breach P1 or P2:** continuous action-unit intensities, labels dropped, targets in the agent's own coordinates. Nor, in my view, does it breach "not by training on emotion data". The agent's own emotions, display and needs are not trained on it. Only its reading of the meaning of words is, much as Claude's own reading comes from human text. It is a frozen cultural prior, declared.

   But D70 approved Seamless as the **test bed**. Fitting a component on it is a new use, and critique 5 listed it as an operator choice. The design treats D70 as covering it. It should be put to him, in one line.
3. **Fitting and testing on one corpus needs a stated split.** The population reader must be fitted on speakers disjoint from those used to test the derived behaviours (F8″, J8-type readings, S1 surrogates). Otherwise the tests are contaminated.

A fallback should also be stated in case the Seamless fit decodes weakly, for example care at "my father died" below 0.1. The obvious fallback is revision 5's per-person word reader, with its face path cut. Otherwise the design silently loses the agent finding-1 closure.

## 5. Buildability through the Claude Code subscription (D84)

**Allowed and feasible**, as in critique 5. The four specifications are now in, and the latency budget adds up:

  0.5 + 0.01 + 0.8 + 0.4 + 0.1 + 0.2 + 0.15 = 2.16 s

That is plausible on Haiku at effort `low` with warm forks and a cached prefix. It is a "considering" beat, which §6.5 states, and S5's timing rests on the body onset. Memory: at most four CLI processes, about 5.5 GB at peak, within the 6 GB rule.

**Three points to add:**
1. **`CLAUDE_CODE_MAX_OUTPUT_TOKENS=120` may truncate before the reply.**
   - On the 5.5 models thinking cannot be turned off.
   - In the Messages API, the output cap includes thinking tokens.
   - A 120-token cap at effort `low` can end a draft inside its thinking, or in its first sentence, on some turns.

   Either drop the cap and end replies by interruption (the engine already streams and can stop at any chunk), or measure the truncation rate in week zero.
2. **The attend line in the canonical history** (failure 3, P4): resume from an engine-written transcript.
3. **Initial values of b^read, σ_id and d_b** (§2.1 gives only update rules).
   - If the operator's first sessions fall in a sad period and b^read starts at his first session's median, grief becomes his neutral, and m_s and the posture are blind until it lifts.
   - Start b^read and σ_id at the agent's reference scale or the population prior, d_b at 0, and update by the stated asymmetric rules.

**Usage:** about 450 calls a day, with automatic fallback on a rate-limit signal or p90 latency, for the operator's own login only. Correctly stated.

## 6. Verdict

**Not yet fit to put to the operator as a build candidate under D82, by a narrow margin.**

**What must change** (each a few lines; none touches the copy certificate except item 1, which the routes critic must size):
1. **Context on the fast laugh echo.** Add an attenuate-only gate g ∈ [0, 1] on the fast gear's BU_L, RHY and BRE (and preferably LP and CR), an innate function of T and latched values only: word care above its dead-band and the hurt latch, plus the latched ω_smile sign if the routes critic finds it safe.
   - Recheck §2.14: nervous laughter in grief, mocking laughter after a month of insults, schadenfreude.
   - Keep the stranger's and the teaser's laugh-back.
   - If no safe gate exists, put the context-free laugh echo to the operator as a stated choice (D81 against D83).
2. **The posture's refractory.** Replace "no onset for 60 s after release" with a mirror-proof onset during the refractory: his 3-s face with the full posture mirror removed, plus sobs. Recheck crying in waves (gaps of 15, 30 and 60 s) and J11's mirroring partner.
3. **P4 and the build.**
   - Keep the attend line out of the canonical history.
   - Remove or verify the 120-token output cap under adaptive thinking.
   - Specify the initial b^read, σ_id and d_b.
   - State the fit/test speaker split for the Seamless population reader, and a fallback if the fit is weak.
   - Put "may the population reader be fitted on Seamless?" to the operator in one line (D70 approved Seamless as a test bed).

**If these are made, and the routes critic accepts R39 and the gate, the operator would be choosing:**

> *A copy-proof conversational agent built from known parts: a frozen per-channel fast reflex with per-expression caps and a context gate from words, a session-latched held cone centred on your own baseline, a zero-DC appraisal display that learns by anticipating its own body, an innate concern posture triggered by its own reading of your distress, readings calibrated to your own face and taught by your words through a prior from other people, a shadow run that bounds every route it can see, information-flow typing, care credited only from your later reports, Joffily-style valence and learning-progress curiosity, with Claude writing its words through your own Claude Code.*

**What he would get:**
- A face that returns your smile and laugh within half a second, at 0.6–0.8 of each expression's ceiling (lip +0.11 at a 0.5 smile onset). It never returns anger, disgust, contempt or sobs.
- A visible look of concern within 2–4 s of seeing you sad, crying or frightened, the same look however you show it.
- Strong expressions from its own appraisal of your words and face: gladness at your return, masked when you arrive grieving on any day of mourning; laughter at play; hurt; worry and relief; boredom and curiosity.
- Replies at about 2.2 s (p50) after you stop.
- A testbed in which every route from your face to its face is bounded per expression, monitored online and can be lesioned.

**Novelty: recombination.** The onset-lobe lemma, the reverse cross-modal teaching of the face head, and the shadow ledger as a backstop are design rules, not a new mechanism. It is a first build while the search for a new core continues (D82).

**Operator choices that remain:**
- **Q24:**
  - the posture (recommended, built);
  - a raised brow ceiling;
  - or none.

  Within the posture: binary, the same look for every degree of distress, as built; or graded by its own appraisal, which costs some brow copy slope (R40).
- Whether the population reader may be fitted on Seamless (a new use beyond D70's test bed).
- The context-free laugh echo, if no safe gate is found.
- The draft model: Haiku for latency, or a larger model for quality.

**Main risks to watch when testing, judged on internal state:**
- **Steering.**
  - Swap in another person's calibration, or zero H_id: concern at a grieving arrival should change as §7 predicts for a quiet and a different-channel user.
  - Clamp the posture trigger: the posture should follow without any change of his face.
  - Clamp word care: the fast laugh gate should close with his face unchanged.
- **Lesions.** The §7 rows, especially:
  - calibration and H_id (F8″, against a person-independent baseline after 400 utterances);
  - the asymmetric baselines across a real low period;
  - the posture's mirror-proof maintenance and onset;
  - the play cue's precision (F13) *and* its recall on jokes that answer questions;
  - the shadow's T equality (F1′).
- **Coupling beyond surrogates.**
  - Per-channel pooled slopes at 2 s, 10 s and 1 min under partner-swap, segment-shuffle, timing-resample and month-swap surrogates (F1). Report how often the ledger binds on natural partners, which should be under 1 %.
  - R39 on real bursty laughter.
  - R40's brow slope on the operator.
  - Whether the fast gate creates its own R39-type slope.
- **The population prior on real data.** Does Seamless, read through Π̃₀, decode loss, fear and flat-delivered alarming content as need, on held-out speakers? Troubles-telling smiles are the expected failure.
- **Stereotypy.** Rate the posture's naturalness with the operator (a listening and viewing test like the laugh test), and measure how often it fires per hour.
- **Timing.** First-word gaps, the rate of "mm" fillers, and truncated drafts.

## Sources read

| Source | How read |
|---|---|
| brief.md | in full (Goal; Long-term goal and S4–S6; Prior work; Principles 1–10; Foundations research including "Expressive structure") |
| research/questions.md | Q19, Q20–Q23 with the operator's answers, Q24, Report 5; Q6 |
| DECISIONS.md | D70, D78, D80–D84 in full |
| research/foundations/designs.md | in full |
| research/foundations/critique-5-design-cayley-ledger-agent.md | in full |
| research/foundations/design-cayley-ledger.md (revision 6) | in full, §0–§10, the revision 5 critiques and answer, and the revision 6 history |
| research/foundations/sims/design-g6/checks.py | agent part (lines 319–734: Person, calibration, population reader, Agent6, posture, J8–J16) read; executed unchanged by my scen.py |
| research/foundations/sims/design-g6/out.txt | J11–J16 |
| research/foundations/sims/design-g5/checks.py | Agent engine (lines 600–700) and the utterance set |
| research/claude-code-agent-sdk-controls.md | grep-read: output cap, effort and thinking, bare mode, fork and resume from a transcript path |
| research/mimicry-context-synthesis.md | §3 (timing: early matching, later context) and recommendations |
| research/mauersberger-2022-laughter-mimicry.md | in full (the project's note of the full article) |
| research/likowski-2008-attitudes-mimicry.md | in full (the project's note; abstract-level) |

**New check:** sims/critique-cayley6-agent/scen.py (A: crying in waves; B: different-channel anger and concentration; C: calm but alarming; D: grief with nervous laughter; E: silent panic), output in out.txt.

**Named only, not re-read:** Jefferson 1984, on laughter in troubles-talk (the recipient declines the teller's laugh). Verdict 1 rests on the design's equations and on Mauersberger 2022, not on it.
