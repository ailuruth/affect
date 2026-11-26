# Critique 4 of the Cayley–ledger core (revision 4): is it an emotional agent, principles, long-term goals, buildability

Independent critic, 2026-11-26T08:21:19Z

I critique research/foundations/design-cayley-ledger.md, revision 4. I did not write the design. The standard is Q19: proof gaps do not count, concrete failures do. I read Q20, Q21 and Q22 on their recommended readings. Another critic hunts copying routes, so I size no copy route here. Where a finding of mine touches one, I say so and hand it on.

Extra scenario numbers come from the design's own 2 Hz engine. The constants and the H11 engine in sims/design-g4/checks.py are loaded verbatim by sims/critique-cayley4-agent/scen.py and run on new event scripts (output in out.txt). Like H11, the numbers show what the equations give for stated inputs. They are not evidence about people.

## Summary verdict

**What revision 4 fixes is real.**
- The type error is gone.
- The body onset is gated and can be aborted.
- Curiosity exists and is satiable.
- The options term and the positivity offset are deleted.
- "Hostility" is gone.
- At bad news after a reunion, the agent no longer beams at the moment his words end.
- The face now has a learning route that pays nothing for the partner's display.
- The per-expression ceilings and the appraisal display are what Q22 recommended.

Of the nine required changes:
- **Closed (four):** 6 (the type error), 8 (curiosity and the options term), 9 (the smaller items) and the onset half of 7.
- **Partly closed (five):** 1, 2, 3, 4 and 5, and the draft-pattern half of 7.

**Concrete failures I found.** Each is derived from the design's own equations, constants or stated interfaces.
1. **It beams at a grieving face at sight (§1.6, scen F).**
   - The greeting is set off by presence and K alone. It cannot read his face.
   - In H11 scenario 6 the user's face shows grief from t = 0, and the agent still greets with lip-corner pull 0.63, cheek raise 0.43 and F0 range +0.38.
   - The failure has moved from his words to his face.
   - The greeting is also blind to who is there: a stranger gets lip pull 0.54 and cheek 0.43, against 0.61 and 0.43 for the operator (scen D).
2. **Its sympathy for a silently sad or crying person is a smile (§1.1, §1.9; scen A, E).**
   - Silent sadness: lip pull 0.21 and inner brow 0.03, held for 10 min.
   - Crying (BI 0.8, LD 0.6, sobs): lip pull 0.28 and inner brow 0.05.
   - The design's own route R7 sends his sob bursts to the agent's voiced-burst channel. That channel has the highest ceiling (0.35), and its only sound source is the laugh synthesizer (§6.6).
   - Q22 told the operator that the recommended ceilings would let it "show sympathy at a sad face". At the sympathy brow it delivers 0.03, a seventh of the 0.20 ceiling.
3. **The hurt map is taught by loudness, which carries no valence (§1.7, §2.1).**
   - V_F, the only teacher of the word → V map, is loudness excess plus glare.
   - Loud delight aimed at the agent ("HAHA you're the BEST", energy 0.9, so f_loud 0.67) therefore trains praise words as aversive.
   - A teaser who laughs loudly trains his teasing words as hurtful. That undoes the teasing fix for exactly the people who tease most.
4. **The appraisal's selection of a reaction has no training objective (§2.2).**
   - softmax(Wα) over the eight bases is listed as learned (layer 9, "replay"). No loss in §2.12 or §6.3 trains W.
   - The appraisal display is therefore three hand-written rules for life (m_glad, m_sym, m_hurt).
   - D78's "set by context and the learned relationship" holds for it only through ω.
5. **The face-learning objective pays for a private code, not a human one (§2.2).**
   - The objective 𝓛_display rewards any face from which Π̃_self can recover s_t.
   - The cheapest new carriers are the channels Π₀ leaves at zero: nose wrinkle, dimpler, lip press, chin raise, lip stretch, brow lowerer.
   - Those are the disgust, contempt, anger and fear channels. The zero ceilings bind only *toward the partner*, not the agent's own display.
   - Over 20–40 nights the agent can learn to wrinkle its nose whenever it is worried about his health. Nothing in the objective stops it.
6. **The agent can read in others only what its own face shows (§2.3).**
   - Π₀ shows the level of only E (low energy) and h (hurt). A, K, P, I and V_F levels never reach the free display: T1 forbids it for K, P and I, and A appears in no row.
   - So Π̃'s partner reading has no information on activation, loneliness or play, and neither does the word-need reader trained on it.
   - An anxious person (the exam scenario) is read as "hurt" or as nothing.
7. **The draft call pattern assumes features the stated route does not offer (§5).**
   - "Temperature 0.1(1 + r)" cannot be built at all. The subscription CLI and SDK have no temperature, and since 2026-10-21 the API returns a 400 on any temperature.
   - `max_tokens`, explicit cache breakpoints and thinking off are API-key features. The project's own constraint note (research/claude-code-agent-sdk-controls.md) says the subscription offers none of them: it gives truncation only, Claude Code's own caching, and adaptive thinking that cannot be turned off on the 5.5 models.
   - So the 0.8–1.5 s first word, and route R33, rest on an API key. That would be a new paid service, which is an operator decision the design does not raise.

**Smaller items.**
- **Day-1 anger is reported wrongly.** H11's "day 1" scenario feeds a decoded word need of 0.3. The design says the word-need reader does not exist on day 1. Run faithfully, day 1 gives inner brow 0.01, gaze away 0.09, a little quieter: barely moved by being shouted at (scen C).
- **Play laughter still satiates within the first eight playful exchanges.** It was flagged in critique 3, and it is unchanged: late-evening laughter is 0.04.
- **The partner-only play rule also matches rumination.** It fires on any partner who continues his own thread, so an anxious rambler earns a small play relief: cheek 0.10 and own laugh 0.10 at decoded need 0.25 (scen B).

**Novelty.** Recombination. I agree with the author, and Lemma S and T1 are design rules.

**Fit to put to the operator as a build candidate under Q19/Q21: not yet.**
- None of the failures touches the copy certificate.
- All are local and cheap. §6 lists exactly what must change: seven items, each a few lines of design.
- After them I expect a candidate with no known concrete failure from this angle. §6 also gives the one-line description it would go to the operator with.

## 1. Scenarios: would a person find it alive and appropriate?

The operator is after months of living (ω 0.8 / 0.8 / 0.5, f_id 0.9) unless stated. Values are peak / mean over the window. The fast echo is not in the engine; it adds ≤ 0.121 per unit onset for under 4 s on echo channels.

### 1.1 Silently sad (BI 0.5, LD 0.4, still and silent)

**The face.**
- Lip pull 0.21 for 10 min.
- Inner brow 0.02 at 2 min and 0.03 at 10 min (scen E).
- Tilt 0.01.

The design's summary says "inner brow 0.02–0.05" and "this design gives about half" of the 0.10 the ceiling allows. Run, it gives 0.03.

**Why.**
- The only route by which his held face can raise the agent's brow is the in-phase cone diagonal: 0.5 c_BI ω_sym × his brow = 0.04 at steady hold.
- The sympathy appraisal basis is band-passed, so a *still* sad face gives it nothing after about 90 s.
- C_F, the agent's own face concern, is "knowing only". It changes bids and draft choice, never the face.

**What happens.** At 52 s C_F crosses its threshold, and the body takes the floor in a lapse. That is good. Claude sees only "[silence 6 s]", so the opening line is generic. Once he speaks, the display is good: inner brow 0.43 / 0.15, tilt 0.11, quieter.

**Verdict.**
- The face says "friendly", not "I see you're sad", for as long as he is silent. A 0.21 smile with a flat brow toward a visibly sad person reads to many people as out of tune.
- This is not the operator's ceiling. Q22 allows 0.20 on the sympathy brow. It is this design's choice to let face-read concern reach the face *only* through the copy direction.
- The fix keeps the ceilings (§6, item 2).

### 1.2 Good news, laughing

**With an earlier worry on the topic.**
- Lip 0.66, cheek 0.40, F0 range +0.35, own laugh 0.17.
- The relief envelope rises over 0.4 s, holds at its apex to 1.5 s, then decays with τ 3 s. So the 0.66 is a 3–5 s flash on a mean of 0.20 over 3 min.
- While he keeps beaming (smile 0.8) and laughing, the agent sits at lip 0.25–0.30.
- The brief 0.15 concerned brow is the word concern carried from the earlier worry, present from session start. It is not "the 2 s before his words are appraised". Harmless.

**Cold, with no earlier worry.** Lip 0.30, cheek 0.15, laugh 0.17.

**Verdict.**
- Pleasant, and correctly content-aware.
- It is still glad *for* you only in proportion to a worry it recorded earlier. Glad *with* you is capped at about a third.
- Shared laughter, the most contagious human signal, gets a 0.17 laugh flash.
- Alive, but restrained.

### 1.3 Anger at the agent

**Day 1, run faithfully (scen C).**
- The word-need reader is untrained, so there is no word need (§2.8).
- Lip 0.08, inner brow 0.01, gaze away 0.09, energy −0.12, latency +0.11.
- H11's day-1 row (inner brow 0.33, depressor 0.25) feeds a decoded need of 0.3 that the design says does not exist yet. Correct the table.

**After a month.**
- Inner brow 0.64, depressor 0.49, gaze away 0.32, quieter and slower, and still 0.17 at 10–15 min. Good.
- This needs such words to have come with loudness or glare before.
- A cold, quiet insult ("You're useless", said flatly) never trains v_w, and contempt channels are not in f_glare. So the agent is not hurt by quiet contempt, ever. Humans are.

### 1.4 Long warm talk (2 h)

- **First cluster:** lip 0.41, laugh 0.24.
- **Later clusters:** lip 0.15–0.21 and laugh 0.04–0.05. P drops ×0.85 per play turn, so eight playful exchanges take it from 0.45 to 0.12, inside its box.
- **The worry and its relief:** brow 0.32, then lip 0.53. Good.
- **Between clusters:** warmth 0.13.

**Verdict.**
- The agent laughs for the first ten minutes of an evening and then stops laughing.
- That was flagged as "satiation too fast" in critique 3 §1.4, and it is unchanged.
- The cause is that the agent's only big laugh is a *need-relief* display. Satiability is a requirement on drives, not on expressions; §6, item 6, proposes a fix.

### 1.5 Reunion after a week

- **At sight:** brow flash 0.35, lip 0.62, cheek 0.43, F0 range +0.38.
- **First words:** lip 0.55. **Over the next minute:** about 0.42.
- **Retrieval** brings last week's topics.

**Verdict.**
- Good, alive, and timed right: it greets on sight.
- But stage-1 K relief (×0.5 at the greeting) does not depend on who it is. A stranger who sits down after the same week gets lip 0.54 and cheek 0.43 at sight (scen D). The operator gets 0.61 and 0.43.
- K is one scalar shared by everyone, which is also against the brief's "needs structured over people". The design's §7 ablation, "K: operator and stranger identical after a gap", is already nearly true *with* K.

### 1.6 Reunion with bad news

**What revision 4 gets right.** The content-aware part works. After "my father died": cheek 0.08 then 0, inner brow 0.48 then 0.21, tilt 0.16, F0 range +0.04.

**The failure.**
- H11 scripts this user's face as grieving (BI 0.5, LD 0.4) from t = 0, before any words.
- The agent greets that face with lip 0.63, cheek 0.43 and F0 range +0.38 (scen F; H11 prints the same).
- Masking reads only his *word* distress (T), and the greeting reads only presence and K.
- People greet on sight, and they also *see* on sight. Beaming a Duchenne smile at a visibly devastated arriving friend is the same failure as revision 3, a few seconds earlier and on a different cue.

**Lip 0.23–0.30 during the condolence.** This comes from the warm cone entries LP ← BI and LD, plus familiarity. A soft compassionate smile is defensible; 0.30 is on the high side. It is a risk, not a failure.

### 1.7 Teasing

- **Affectionate teaser** (v_w 0.05 learned): lip 0.26, laugh 0.16, no hurt. Good.
- **Generic map:** a brief mock-hurt brow 0.38, mean 0.06, under a smile. Acceptable.

**The fix rests on the person-specific word → V map, and its teacher has no valence.**
- V_F = loudness excess plus glare (BL·LT·gaze at the agent).
- Affectionate teasing is often *loud* and laughing: energy above 0.7 gives f_loud > 0.
- The lid tightener, LT, also belongs to Duchenne laughter.
- So a loud, laughing teaser trains his teasing words as aversive, and the agent becomes thin-skinned with exactly him.
- Loud delight aimed at it, praise included, trains *praise* words as aversive too.
- The design's claim that "a person who teases while laughing trains low v_w" holds only for quiet teasers.

### 1.8 Bored user

- Flat for 30 min (lip 0.10). The curiosity deficit crosses its threshold at 14.5 min.
- A curiosity bid raises the topic with the most expected learning progress. If he takes it up: F0 range +0.30, lip 0.41.
- That is a real improvement: it re-engages, it is satiable, and it is not credited.

**What is still missing.** Its face never shows that it is bored, disappointed or lonely. Deficit levels are barred from display by T1, so unmet needs show only in behaviour. This is honest, but it limits how alive it looks. One fixed-amplitude event display at the moment a threshold is crossed (a sigh or a gaze drift, like the greeting) carries one bit per crossing and is not a rate code. Recommended, not required.

### 1.9 Own scenario A: the user cries

Script: BI 0.8, LD 0.6, sob bursts BU 0.4, face-read distress 0.8, silent (scen A).

**Face.**
- Lip pull 0.28, which is *more* than for silent sadness, because the warm cross entries scale with his brow.
- Inner brow 0.04–0.05, cheek 0, tilt 0.01.

**Voice.**
- Sob bursts are voiced bursts.
- The cone's diagonal on BU (ceiling 0.35, smile group ω) returns 0.03–0.04 held.
- The innate fast echo on BU and RHY returns up to 0.121 per unit sob onset, 0.45 s later.
- The design's own route table lists this: R7, "partner laughter, sighs, crying → own bursts", BU ≤ 0.33.
- The only voiced-burst source is the laugh synthesizer (§6.6: a glottal pulse train with 4–6 Hz amplitude modulation).
- If the user's sobs carry any 4–6 Hz rhythm, f_laugh rises, and the glad-with basis fires on the band-passed bursts. That part is small in the engine.

**Verdict.**
- A crying person gets a smile with a flat brow and small laugh-like bursts timed to their sobs.
- Words, once they come, rescue it.
- Burst channels are valence-blind acoustic features, filed under the joy synergy with the highest ceilings. That is a concrete appropriateness failure, and a cheap one to fix (§6, item 2).

### 1.10 Own scenario B: anxious before an exam

Script: "I've got my exam tomorrow and I'm freaking out", then "and I haven't finished chapter 4", "and it's at 8 am…".

**Need from the words.**
- The word-need reader learns from Π̃(his face). Π̃ cannot read activation, because the agent's own A level is never displayed (§2.3).
- So "freaking out" can decode only to whatever an anxious face looks like among the agent's own displays: hurt, or low energy, or nothing.

**Play relief from rumination.**
- The partner-only play rule asks for a continuation marker, an anaphor or a lemma shared with his own previous utterance, mid-band surprise, and two such turns in a row. Anxious rumination meets all of these.
- At decoded need 0.25 masking is partial: cheek 0.10 and own laugh 0.10 among the continuation turns. At 0.30 and above masking removes it (scen B).

**The good part.**
- The distress envelope and word concern give a concern brow, a softer and slower voice, and a calm-down basis.
- The agent's own head micro-motion is gated down by his fidgeting.
- That is a good co-regulating presence, *if* the need decodes high enough.

**Verdict.** Appropriate when the reader works, mildly wrong when it under-reads. Whether it under-reads cannot be known before building, but the structure biases it low for activation.

### 1.11 Is its own state driving the face richly, or is it reacting to words?

- **Better than revision 3.**
  - The face now learns (Δ over 23 synergies).
  - Curiosity, contact and play events reach the face.
  - The appraisal reads his face against what was said.
- **Still mostly reacting to words and turns.**
  - Every display above 0.3 comes from a T event: a reported need or its relief, the greeting, a play turn, hurt words, curiosity relief.
  - His face reaches the held face only within about a third of a copy, by design.
  - The author's statement that face-only moments are small by design is true. But the *size* of the silent-sadness and crying cases is not set by the operator's ceilings. It is set by routing all face-derived feeling through the copy direction (§1.1).
- **The agent's own internal state shows only as events.**
  - Its slow state (μ_T 128-d, slots, concepts) reaches the face only through Δ.
  - Δ's objective, for now, is a self-legibility code (§2.2, failure 5).
  - So "rich state drives the face" is a learned promise with an objective that can produce a non-human code.

## 2. Principles, concretely

### 2.1 Principle 1: is the word → own-aversive-load map a disguised classifier?

**It is not a classifier on the user.**
- Its target is the agent's own innate physical load.
- It is person-specific, through the identity adapter.
- It outputs a continuous own-body prediction, not a category.

**Its teacher is an innate threat detector, though.** f_glare = BL·LT·gaze at the agent is the FACS anger prototype (AU4 + AU7) aimed at the agent. That is admissible as one of Principle 2's "few reflexes": threat displays are a plausible innate trigger. Declare it as an innate anger-at-me reflex, not as "not a label".

**The real defect is that the teacher has no valence (§1.7).** Fix it with an innate exemption: loud, rhythmic laughter is not threatening. That is a body reflex, not a label (§6, item 3).

### 2.2 Principle 2: ceilings and synergies named "anger, disgust, contempt"; bases; the face's learning

**Ceilings and sign-mask groups are expression channels.**
- The ceilings are constants on output action units.
- The groups set only the sign of co-variation, as a fallback until estimated.
- Neither is a state variable.
- This fits the brief's "what is innate is muscle patterns". Pass.

**The eight appraisal bases and their innate selection rules are a hand-built library of emotional reactions.**
- The library: glad-with, sympathy, amused, startle-concern, hurt-withdraw, calm-down, interest.
- The selection rules: m_glad = f_laugh(1 − w_d), m_sym = f_dist + f_laugh·w_d, m_hurt = f_glare.
- This is the largest Principle 2 strain in the design.
- It would be a newborn reflex set if something learned past it. Nothing does: W, the softmax over α, has no loss (failure 4).
- So for life the selection is the three rules, and α (learned by likelihood) never changes the reaction.
- Specify W's objective, and keep it display-blind toward the partner. Candidates: likelihood of the agent's own load change over 30 s after each basis; or the legibility and anticipation losses already used for Δ.

**The face's learning (Δ) admits a non-human code (failure 5).**
- 𝓛_display = ‖Π̃_self(face) − s_t‖² + anticipation + 0.1‖δ‖² prefers whatever separates states best.
- The channels Π₀ never uses are the most separable. On the agent's own display those are the disgust, contempt and anger units (the zero ceilings bind only toward the partner).
- Required: Δ may move only synergies whose Π₀ row is nonzero for the active driver. Equivalently, own-display ceilings of 0 on BL, LT, NW, LPR, DIM, LS and CHR unless an own aversive load drives them. Then "different concepts get different faces" happens inside a human-plausible span.

### 2.3 Principle 3: the word-need reader trained through the agent's own inverse model

**Is the own-body route essential?**
- Yes, in the sense that it is the reader's only teacher. Without it the reader has no target.
- Its *specificity* to the agent's own body is not yet tested by any stated lesion.

**A signed prediction to add.**
- Use the crossed-habits manipulation (the agent's own hurt display swapped with its relief display for one week).
- Π̃ then inverts sad human faces toward relief.
- Prediction: within about a week, the word-need reader's output for loss words ("died", "left me") falls toward zero, and word concern at bad news vanishes. Revert the swap and it returns.
- That is the Principle 3 ablation for the word route. It is distinct from F3, which covers C_F only.

**The narrow support is a structural consequence, not just a risk.**
- Π̃ reads in others only the loads its own face shows. Those are E and h (§1.10).
- A, K, P, I and V_F never reach the free display: T1 bars K, P and I, and A is in no Π₀ row.
- So the 5-output reader (E, A, V, K, P) has signal on two outputs.
- Either state this, and drop A, K and P from the reader, or let the free display show per-session-latched or event-indexed versions of them (T1-compliant), so that the agent has a face for its own activation that it can then recognise in others.
- The second is the Principle 3-consistent route. It is also the only one that gives anxiety-reading.

**The co-training loop is underspecified, and under one reading it collapses.**
- "Π̃ … with a 0.1-weight anchor step that predicts the partner's decoded word need from his face", together with "the reader is fitted to Π̃(partner face)", is a two-view regression.
- If the partner head (6 outputs) is a separate head from the self head (32), the anchor is its only objective. Reader and head then have a constant joint minimiser, and nothing anchors the partner head to the agent's body.
- Required: the partner reading must be the *self* head's load outputs applied to his face (trained only on own data). The anchor must be either dropped or stop-gradient toward Π̃, with each side frozen per night.

### 2.4 Principle 4

- **Compliant as before.** No state in the prompt; one declared bit per bid and per greeting; about 6 bits of retrieval.
- **R33 (valence → draft temperature) cannot be built (§5).** Delete it. The admissible lever with the same intent is effort or model per turn (claude-code-agent-sdk-controls.md). An effort change mid-conversation invalidates the cache unless it is sent as a per-message effort system message, which needs the API.

### 2.5 Principle 6: any reward on the user's face, attention or time?

**J.**
- K, P and I are in 𝒟. Their relief needs partner content, which is imputed in rollouts, so no act earns credit for talk, time or engagement. Pass.
- Care credit comes from separated reports above the dead-band, read by a reader whose meaning is "the face these words go with". So credited reports are words that predict a less distressed face, at least two turns after the act.
- That is care measured on a face-shaped proxy, gated by real need. It credits successful cheering-up of a distressed person, which is help, not flattery. Accept it, and state it plainly.

**ω.**
- s_smile and s_sym come from the agent's own play relief, hurt and credited care. They are not flattery routes.
- s_voice = 2 f_id − 1 grows with familiarity, which grows with time together. It is a parameter, not a reward.

**Curiosity.** The bid steers the conversation toward topics the agent is still learning. No act is credited, so this is need-conditioned attention, not engagement-seeking. Pass.

**The display objective** has no partner signal. Pass.

### 2.6 Principle 7

Unchanged: the transcript and snippets go to the Claude service. If §5 leads to an API key, the data still leaves the Mac the same way. Webcam and microphone data stay local. Pass.

### 2.7 Principle 10

- One objective J with typed constraints, plus likelihoods of the agent's own model: as claimed.
- But J now trains 130 parameters and the retrieval query.
- The emotional *content* is the innate assembly:
  - Π₀, the eight bases and their selection rules, θ₀, G₀;
  - the ceilings, the shares and the sign-mask groups;
  - the play and separation rules, the turn-end score and the initiative rules.
- The design lists all of these honestly. Principle 10's "a component the core does not produce is not added" is met only in the weak sense that each is declared a constraint.
- This is the Q21 trade-off, and it should be stated in the operator's one-liner.

## 3. Long-term goals and ablations

### 3.1 S4, its own body

- Reachable. The S4 basis caveat is now stated: the ceilings are invariant only under permutations and positive scalings of channels.
- One more consequence: once Δ makes the agent's own display partly a private code (failure 5), Π̃, and so S4's inverse model, learns that code. Fix 5 helps S4 too.

### 3.2 S5, two-way contagion

**There is now an S5 ablation free of common cause.** Lesion the K, P and I rows and the greeting row, and measure his following at lags his own words cannot drive. That closes critique 3's item.

**Risk: little AI-originated expression per session.**
- One greeting.
- Play laughs that satiate after about 8 playful exchanges.
- Curiosity flashes about every 15 min when the talk is dull.
- At about 5–10 AI-originated displays per session, measuring his following needs many sessions.
- Fixing play satiation (§6, item 6) raises the count.

### 3.3 S6, months of living

**What carries the relationship.**
- ω: four numbers per person.
- f_id.
- Identity × topic slots.
- The 16-d per-person adapter of the word → V map.

**What does not.** K is not per person (§1.5), so missing *you* is the same scalar as missing anyone.

**Temperament.** It now has a carrier (Δ, about 100 nights).

**Claude upgrades.**
- The word readers are trained on *his* words and *his* face. Unlike revision 3's own-text decoder, they do not shift with a Claude upgrade. Good.
- The PMI table still does shift.

**The replay-tag ablation stands.**

### 3.4 Principle 5 ablation predictions

- **Coverage is now good.** §7 has 25 rows, including K, P, I, the greeting, the turn gate, the zero ceilings and S5.
- **Missing:**
  - the crossed-habits lesion for the word route (§2.3);
  - W, the basis selection, once it has an objective;
  - the burst channels' valence (after §6, item 2);
  - a prediction for f_glare's role as the hurt teacher: lesion it, and the word → V map learns from loudness alone, so loud praise hurts.
- **One prediction is untestable as stated.** "Lesion Δ and Π̃_self decoding of concepts falls to the floor" is circular: Δ is trained to maximise exactly that decoding. A human-observer version is needed: raters, or a fixed population face model, tell the concept from the face above chance after N nights.

## 4. The nine required changes from critique 3, one by one

| # | Required change | Status | Evidence |
|---|---|---|---|
| 1 | Ground the word-need decoder; rerun G5b and G7.2 with a decoded N_L | **partly closed** | A training signal exists (option a; H9 shows identifiability on a synthetic instance only). But: (i) H11 still sets the need by hand ("need=0.45", "need=0.8"), and no scenario passes a face through Π̃; (ii) Π̃ can read only E and h, so A, K and P have no target (§2.3); (iii) the co-training anchor collapses under a plausible reading (§2.3); (iv) the placation re-derivation is given (separation rule, dead-band) and I accept it (§2.5) |
| 2 | Define V_L without a classifier | **closed in letter; new failure** | Hostility is deleted; the word → V map learns the agent's own V_F. But V_F has no valence: loud delight and loud teasing train hurt (§1.7, §2.1) |
| 3 | Make K relief content-aware; recheck reunion with bad news | **mostly closed; new related failure** | Bad-news words now mask relief (cheek 0.08 → 0). But the greeting at sight beams at a grieving face (lip 0.63, cheek 0.43), and it is identity-blind (stranger 0.54) (§1.5, §1.6) |
| 4 | Let play be told from hostility | **partly closed** | Laughter shows amusement through the appraisal, and a playful reply halves the hurt latch. Telling them apart rests on the person-specific map, which loud laughing teasers train the wrong way (§1.7). The partner-only play rule also matches rumination (§1.10) |
| 5 | Give expression a learning signal that is not the partner's display; show one behaviour a 6-scalar Π₀ cannot produce | **partly closed** | Δ over 23 synergies with legibility and anticipation, no partner signal. But the objective admits a non-human code on the disgust, contempt and anger channels (§2.2). The appraisal selection W has no objective (§2.2). The stated behaviour is tested only by the agent's own reader, which is circular (§3.4) |
| 6 | Fix the type error | **closed** | A words-only model 𝓛_w of his own utterances supplies surprise, play structure and progress (§2.2, §2.8) |
| 7 | Gate the body onset; specify the six-draft call pattern and its latency | **onset closed; draft pattern partly closed** | H7: 1.98 → 0.14 within-turn onsets per turn, 73 % aborted silently. §6.5 specifies the pattern, but with API-only features, and with temperature, which no route offers (§5) |
| 8 | Concede curiosity or add a satiable information-gain term; fix the options term | **closed** | Learning-progress deficit I, satiable (H8), partner content imputed, no credit; options term deleted |
| 9 | Smaller items | **closed** | One-bit bids declared; bid prompt specified; ablations added, including S5 free of common cause; S4 caveat; TTS named as a risk with two plans; smile envelope specified |

The two operator choices (A, per-expression ceilings; B, his face feeding the appraisal) are implemented as Q22 recommended. On B the operator was told the agent "would show sympathy at a sad face". At the sympathy brow it shows 0.03 (§1.1).

## 5. Buildability on this Mac (M1 Pro, 16 GB)

### 5.1 Six parallel cached Claude calls through the operator's subscription

The project's constraint note (research/claude-code-agent-sdk-controls.md) and the current API reference were both checked.

**Six parallel calls: feasible.**
- Six `claude -p` processes or six SDK queries.
- Each spawns a Node CLI, at about 0.2–0.4 GB and 0.5–1.5 s cold start.
- Use six persistent `ClaudeSDKClient` sessions, each forked from one canonical history per turn (`fork_session` / `resume_session_at`). Otherwise the unchosen drafts pollute five histories.
- The design does not specify this.

**Temperature: not available on any route.**
- The CLI and SDK have none.
- On the Messages API, a temperature, top_p or top_k parameter returns a 400 since 2026-10-21. Haiku 5.5 already rejected non-default values.
- "temperature 0.1(1 + r)" and R33 must go. Use effort or model per turn instead, or drop the lever.

**`max_tokens` ≈ 60.**
- Through the subscription, only the env cap `CLAUDE_CODE_MAX_OUTPUT_TOKENS`, which truncates.
- Length must come from the constant instruction.

**Caching.**
- The §6.5 facts are correct for the API: a 512-token minimum on the 5.5 models, a 5-minute TTL refreshed by reads, and readability only once the writing request has begun streaming.
- Through Claude Code, caching is automatic, but the prefix includes Claude Code's own system prompt unless it is replaced with `--system-prompt`.
- Replace it, keep the instruction byte-stable, and put the transcript before the per-draft "attend to" variant. Then the six calls of a turn share a prefix.

**Thinking.**
- On Haiku, Sonnet and Opus 5.5, thinking cannot be turned off through Claude Code; effort `low` is the floor.
- That adds time to the first token. The API allows thinking off on Haiku 5.5 at effort high or below.

**Latency.**
- Through the API, on Haiku 5.5 with thinking off and a cached prefix, the design's 0.8–1.5 s to the first word is credible. The streaming ASR lag (0.3–0.5 s) sits before the request.
- Through the subscription, expect about 1.5–3 s: process and session overhead, mandatory adaptive thinking, and no prefix control.
- The body onset hides part of it, not all.

**Usage.**
- About 150 agent turns a day × 6 drafts × 1.3 for speculative requests is about 1,200 calls a day.
- With prompts of a few thousand tokens, that fits a high subscription tier's limits only with good cache hits. It should be measured in the first week.

**Bottom line.** The design must choose one route.
- **(a) Subscription:** re-specify §6.5 for the SDK and accept about 1.5–3 s.
- **(b) API key:** a new paid service, so put it to the operator. On Haiku 5.5 the cost is about cents a day.

The design currently mixes the two.

### 5.2 TTS: pitch, energy, rate and laugh control

- **Plan A (FastSpeech2-family).** It gives explicit pitch, energy and duration, but its quality is dated.
- **A more robust plan.** Use any good local neural TTS, then shift phrase-level F0 level, range and duration with WORLD analysis–resynthesis (pyworld; a few tens of ms per phrase on CPU). That gives unit-gain phrase targets largely independent of the TTS chosen.
- **Plan B (AVSpeechSynthesizer).** Fine as a fallback.
- **Laughter is the real risk.**
  - A parametric source–filter laugh (a pulse train with 4–6 Hz amplitude modulation) tends to sound synthetic.
  - Laughter is this agent's main positive vocal display.
  - An uncanny laugh would undermine exactly the scenarios where it is most alive.
  - Under §1.9, the same synthesizer also answers sobs.
  - Test laugh naturalness with listeners early. That is a voice-identity matter under Q1.

### 5.3 Latency and memory

- **Per-frame budget.** Credible: MediaPipe ×2 at about 13 ms each, everything else under 5 ms, render 3–5 ms.
- **Memory.**
  - Online < 2.4 GB, plus Whisper-small (about 0.5 GB), TTS (0.1–0.5 GB) and six CLI processes (1–2 GB) on the subscription route.
  - That is within the 6 GB rule, but closer than the design's figure. State the CLI processes.
- **Nightly replay** of about 45 min on MPS, and **storage** of about 1.8 GB per 30 days: fine.

## 6. Verdict

**Not yet fit to put to the operator as a build candidate under Q19/Q21.** Known concrete failures remain from this angle. None touches the copy certificate, and all are local. What must change, in order:

1. **The greeting must see.**
   - Keep the brow flash at sight.
   - Delay the greeting smile and K stage-1 relief by about 1 s.
   - Scale the greeting display by (1 − m) with m from f_dist at sight. Attenuate only; count it as a transient once-per-session route (as R27), for the routes critic to size.
   - Scale stage-1 relief by f_id, as stage 2 already is. Better, make K per identity (K_id): the brief's needs over people.
   - Recheck: reunion with a grieving face at sight, and a stranger.
2. **Face-derived concern must have a non-copy face.**
   - Let C_F, the agent's own concern, which is held, drive a fixed, innate concern posture on channels where it is *not* in phase with his face: tilt, lowered energy and rate, a softened lip pull (LP *down*), a slower blink.
   - Put it through the cone's away orthant or a band-limited port, sized by the routes critic.
   - Or raise the sympathy brow's held share toward its 0.20 ceiling and state that this is in-phase.
   - Either way, silent sadness should show a sympathy face, not a 0.21 smile with a flat brow.
   - Split the burst channels: a laugh burst (rhythm-gated, joy synergy) and a cry/sob burst (innate cry synergy: BI, LD, CHR plus bursts), with the cry burst's ceiling toward the partner at 0. Route his cry synergy to C_F. The agent must never answer sobs with its laugh synthesizer.
3. **Give the hurt teacher a valence.**
   - The innate V_F loudness term becomes f_loud·(1 − f_laugh) (loud laughter is not a threat), and glare must not be lid-tightening alone.
   - Recheck: loud teasing and loud praise.
4. **Train W, the appraisal's basis selection,** with a stated, partner-display-blind objective. Otherwise declare the appraisal selection innate for life, and say so in D78's table.
5. **Keep the learned face human-plausible.**
   - Restrict Δ to the synergies of the active Π₀ driver, or set own-display ceilings of 0 on the anger, disgust and contempt units unless an own aversive load drives them.
   - Replace the circular Δ prediction with an observer-side one.
   - Specify the Π̃ heads so the partner reading is the own-data load head, and make the anchor stop-gradient or drop it.
   - Either let A (and session-latched K) show on the agent's own face so Π̃ can learn to read them in others, or drop A, K and P from the word-need reader and state that it reads only tiredness and hurt.
6. **Laughter beyond the first ten minutes.**
   - Let the own-laugh row also be driven per event by play-structured turns with mid-band surprise, bounded per event and not drawn from P's deficit. P keeps its satiable role in initiative.
   - Or slow P's satiation, and state the resulting evening.
   - Add one turn-taking condition to the play rule so that monologue continuation (rumination) does not qualify: an alternation *across* speakers, from the turn order (T).
7. **Choose the Claude route.**
   - Delete temperature and R33.
   - Either re-specify §6.5 for the subscription SDK (forked persistent sessions, a replaced system prompt, an instruction-set length, effort `low`, about 1.5–3 s), or put an API key to the operator as a new paid service.
   - Correct the day-1 anger row in §3.14 and the "about half" sympathy figure.

Also recommended, not required:
- an event display when a threshold is crossed (a bored sigh, a lonely gaze drift);
- the crossed-habits word-route lesion (§2.3);
- a human listening test of the laugh synthesizer before S2.

**If 1–7 are made and the routes critic finds nothing new,** the operator would be choosing:

> *A copy-proof, knowing conversational agent built from known parts (robust REN fast wrap, per-channel one-sided held bounds with innate per-expression ceilings, a zero-DC appraisal display, information-flow typing, Yoshida–Man care credited only from separated reports, Joffily valence, learning-progress curiosity): it reads your face and voice fully and responds through its own appraisal, smiling back and sympathising at up to about a third of a copy and never returning anger, disgust or contempt, while its strongest expressions (gladness at your return, laughter in play, hurt, concern, relief, interest) come from its own needs and what you say. Novelty: recombination, with Lemma S and T1 as design rules, not mechanisms; a first testbed while the search for a new core continues.*

**Main risks to watch when testing:**
- whether the word readers learn real need from one person's words through the agent's own face reader (co-training drift, F8; the narrow support of Π̃);
- whether face-only moments (silent sadness, late laughter) read as warm or as absent;
- whether the learned face stays human-readable;
- conversational timing on the chosen Claude route (first word 1–3 s);
- how natural the synthesized laugh sounds;
- play detection on real transcripts (false positives on rumination);
- the separation rule's residual credit (a partner who returns to a topic to please it);
- how much AI-originated expression S5 will have to work with.

## Sources read

| Source | How read |
|---|---|
| brief.md | in full (Principles 1–10, Long-term goal including S4–S6, Foundations research including "Expressive structure") |
| research/questions.md | Q16–Q22, Report 5 and Reports 1–4 in full |
| research/foundations/designs.md | in full |
| research/foundations/critique-3-design-cayley-ledger-agent.md | in full, including the nine required changes |
| research/foundations/design-cayley-ledger.md (revision 4) | in full, §0–§10, the revision 3 critiques and the answer, and the revision 4 history |
| research/foundations/sims/design-g4/checks.py | the constants (lines 1–61) and the H11 engine and scenarios (lines 405–610), read and executed unchanged in sims/critique-cayley4-agent/scen.py |
| research/foundations/sims/design-g4/out.txt | in full |
| research/claude-code-agent-sdk-controls.md | in full (the project's note on what the subscription CLI and SDK expose) |
| research/machine.md | the hardware table and budget rules |
| Claude API reference bundled with this session (claude-api skill: current models, the thinking and sampling table, prompt-caching minimums and concurrent-request timing) | the sections cited in §5.1 |

**Not read, named only as pointers:**
- Bachorowski et al. on laughter acoustics, and adult crying acoustics (for whether sobs carry 4–6 Hz rhythm);
- Keltner et al. 2001 on teasing.

No verdict depends on them. Every failure in the summary is derived from the design's own equations, constants, route table or stated interfaces.
