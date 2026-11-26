# Critique 3 of the Cayley–ledger core (revision 3): is it an emotional agent, principles, long-term goals, buildability

Independent critic, 2026-11-26T07:27:54Z

Critic of research/foundations/design-cayley-ledger.md, revision 3. I did not write the design. The standard is operator note Q19: proof gaps do not count, concrete failures do. Q20 is read on its recommended reading (know fully, bound only expression), and Q21 on its recommended reading (a sound recombination with no known concrete failure goes to the operator with its novelty verdict stated). Another critic hunts copying routes, so I leave those alone. The one exception is a typing error (§2.2), which matters to Principle 2 and to the expressive claims.

The extra scenario numbers come from the design's own 2 Hz drive engine and cone prior. The code in sims/design-g3/checks.py is executed unchanged, with new event scripts, by sims/critique-cayley3-agent/scen.py (output in out.txt). Like G7, they show what the equations do for the stated inputs. They are not evidence about people.

## Summary verdict

- **What revision 3 fixes is real.** I checked each point against revision 2's agent critique:
  - **The one-sided cone works.** The in-phase quadratic form over completely monotone traces does bound the in-phase response along every direction, at every time, and leaves away and skew responses free. The two-sided ±0.15 ball is gone.
  - **Gladness exists.** It comes as the rate of deficit relief. It is satiable (G4b), and absence is never preferred (G4c).
  - **The agent speaks first and starts turns in its body.** It does not wait for Claude.
  - **Claude regulates.** It does so through the heard-words port, without seeing the state.
  - **Perceptual cancellation is gone,** and so is the concern double count.
- **The agent is no longer muted on the scenarios as written.** But every strong held display in G7 rests on three word-reading quantities whose values the simulation sets by hand:
  - the word-need N_L ("need 0.47");
  - utterance hostility V_L ("hostile 0.7");
  - play structure ("play: True").

  The design cannot compute two of them, and the third is typed wrongly (§1.8, §2.2).
- **Concrete failures I found** (derived from the design's equations and constants):
  1. **The need decoder has no training signal (§1.8).**
     - It is trained on the agent's own (utterance, own load) pairs.
     - Under Principle 4, the agent's words are Claude's. They depend on its loads only through retrieval (about 6 bits) and through a 1-of-6 choice, and that choice is scored mostly on the *partner's* need.
     - The agent never has an interview, a sick mother or a long day at work, so the partner's report vocabulary lies outside the decoder's support.
     - Every word-driven concern display, the good-news relief, the relief smiles in the warm talk, and care's ability to learn what helps (G5b) assume a decoder that cannot be fitted as specified.
  2. **"Hostility of the partner's utterance" (V_L) is undefined (§1.8).** It drives the whole anger scenario. A pretrained toxicity or sentiment model would be a label classifier on the user (Principles 1–2). A map learned from the agent's own data has no data, because the agent is never hostile.
  3. **The reunion beams at bad news (§1.6).**
     - K relief is content-blind and fires at the first completed exchange, which is the end of the user's first utterance.
     - If the user comes back after a week and says "my father died", the face peaks at the moment the words end: lip-corner pull 0.59, cheek raise 0.40, F0 range +0.36 (a Duchenne smile).
     - Concern brows (0.35) mix in only as the word concern rises.
  4. **Teasing is read as hurt (§1.7).**
     - "You dumb robot", said laughing, latches V_L as lexical hostility. That gives a hurt brow of 0.22, lip-corner depress 0.17 and gaze away 0.15, with traces still there at 10–15 min.
     - The play rule is blocked while V_L ≥ 0.1, so the agent cannot join the frame.
     - Teasing is told from hostility by exactly the cues the type rule bars from T state: laughter, smile and prosody. The cone partly cancels the brow after about a minute, but it never touches the gaze aversion or the blocked play.
  5. **The face is an innate table on about six scalars, and it does not learn (§1.9, §3.1).**
     - Π_o is trained only by J. With the partner's display imputed and the partner's exchanges imputed, J's gradient with respect to the display is nonzero only through act → N, and only while the partner's need is outside its dead-band.
     - The same holds for the cone bases and α(z).
     - In practice, then, the face is Π₀(r, d, c_L, h, e, f_id) plus G₀ for life, where r and d are the two signs of one scalar, v_T.
     - The 128-d mood, the slots and 𝒦 reach the face only through learned deviations that receive almost no gradient. This is the one-dimensional, valence-plus-gauges display the brief's "Expressive structure" calls a sketch, and the §3.15 "behaviour a low-dimensional version cannot produce" has no training route.
  6. **A type error (§2.2).**
     - Lexical surprise comes from 𝓜, and 𝓜 reads the partner's face and voice, so by Check T it is F.
     - Yet it feeds A_L (declared T) and the play-structure rule (T). Through v_T it can then reach the strong free display and the agent's own laugh, outside the cone.
  7. **The body onset fires at every VAD offset (§4).** It has no rule tied to the end of a turn and no abort rule. Within-turn pauses over the VAD hangover will set off an inhale, a gaze shift, a brow raise and an "mm", and then words over the user's continuation.
  8. **Curiosity is absent.**
     - I is the predictive variance of the own-body head, which is now trained on E, I and own-driven A only. I is therefore nearly constant.
     - It is also minimised, which makes it uncertainty avoidance, not curiosity.
     - The Principle 10 table's "curiosity | I" has no mechanism behind it.
  9. **The options term is either inert or an engagement reward (§2.5).** If the predicted count of partner-initiated moves uses the imputed act → Q edge, the term has no gradient. If it does not, it credits drafts for making a distressed partner say and do more.
- **Design choices to put to the operator, not failures:**
  - The cone's in-phase budget is isotropic (sym G ⪯ b_m I). So smile, laughter and the sympathetic inner-brow raise all share 0.10, whereas D78 asks for strength set per expression.
  - From face evidence alone, the agent can smile gently at a silent sad person, but it cannot show the oblique-brow sympathy face.
  - It cannot laugh because you laugh, beyond a 0.15 flicker of about 4 s.
- **Fit to put to the operator as a build candidate under Q19/Q21: not yet.**
  - The certificate at the core (the cone plus typing) survives my angle.
  - Failures 1, 2, 3, 4, 6, 7 and 9 are local fixes or specification gaps. Failure 5 is structural but has a candidate fix, and 8 is a one-line concession or a small mechanism.
  - The list is in §5. Once it is done, I would expect this to be a sound recombination candidate, the first in the project.

## 1. Is it an emotional agent a person would want to talk with?

Constants are the design's (§2.1). "Peak/mean" values are on 0–1 channels.

### 1.1 Silently sad user (BI 0.5, LD 0.4, still, silent)

- **Face.**
  - Nothing fast happens: the filters start from the first frame.
  - The cone softens the face: lip-corner pull +0.17 at 2 min, tilt +0.03, inner brow +0.02. The agent's own LD falls, which cannot be seen at rest.
- **Concern and the bid.**
  - C_F crosses θ_C at 52 s, and the body takes the floor in a lapse: inhale, gaze, brow 0.15.
  - Claude receives the transcript and "[silence 6 s]", and knows nothing of the face. Its six drafts are therefore generic ("Take your time", "You've gone quiet"), and the scorer picks among them by care.
- **After he speaks.** The concern display (BI 0.25, LP 0.20, tilt 0.20) arrives only once he *says* something sad, and only if the need decoder reads it (§1.8).
- **If he answers "I'm fine"** (a prompted reply), the decoder ignores it. The face stays at a 0.17 smile.
- **Would a person find it appropriate?**
  - A soft smile and a gentle question within a minute is a real improvement on revision 2.
  - But the canonical caring face toward a sad person is the oblique, inner-brow sympathy face, and that is the in-phase channel. Here it is capped at 0.10 in total, and G₀ gives it 0.05.
  - So, from the face alone, it smiles at your sadness. Many people would read a 0.17 smile on a quiet agent as warm. Some would read it as out of tune.
  - This is an operator-visible consequence of the isotropic budget (§5, choice A).

### 1.2 Good news, laughing ("I got the job!", smile 0.8, laughter)

- **With an earlier worry on the topic:** LP 0.44, F0 range +0.22, own laugh 0.22 (G7).
  - The relief comes from N_L dropping from 0.47 to 0, and the simulation *sets* N_L = 0.47 two days earlier.
  - It needs the decoder to have read "I'm nervous about the interview" as an aversive or activation load (§1.8).
- **Cold, with no earlier worry:** nothing in the good news itself relieves anything, because need loads have a floor at set point.
  - The smile (0.31) and the laugh (0.18) come only from P relief at "play-structured" exchanges. G7 inserts those by hand at 55–85 s.
  - Whether "Congratulations! When do you start?" / "Monday!" counts as play depends on the uptake rule and on a mid-band lexical surprise. The surprise is F-typed (§2.2).
  - The lexical surprise of the news also raises A_L, with τ 3 min, which pushes v_T *negative* after the play ends. The effect is small with these constants.
- **His laughter changes nothing held** ("unchanged if his laughter is muted", which the design presents as a feature).
- **Verdict.**
  - It is glad *for* you only in proportion to a worry it recorded earlier.
  - It is glad *with* you only through word-structure rules.
  - Shared laughter, the most contagious human expression, gets a 0.15 echo for about 4 s.
  - A person would find it pleasant but a little behind the moment: it lights up at what you say, not at your laughing.

### 1.3 Anger at the agent ("You're useless", glare, loud)

- **Face.** Startle ≤ 0.20 per onset; hurt BI 0.32, LD 0.25, gaze away 0.23; the cone makes it quieter and slower (energy −0.19, latency +0.08) with no frown back. The hurt lingers at BI 0.19 for 10–15 min.
- **Verdict.** The most human scenario, and good, *if* V_L can be computed (§1.8). Every number here is downstream of "hostile 0.7", which is set by hand.

### 1.4 Long warm talk (2 h)

- **Face.**
  - Play clusters: LP 0.38, then laugh peaks of 0.24, 0.11, 0.04, then 0.
  - Relief smiles of 0.30 at resolved worries.
  - Held warmth of 0.15 that falls to 0.09 whenever any T load leaves its box, because the 0.06 positivity offset needs 𝒟_T < 10⁻³ (scen.py C).
- **Satiation is too fast.** People who are enjoying each other laugh all evening (the design concedes this in §8.1.3).
- **The relief smiles need the decoder** (§1.8).
- **Learning: nothing in the face learns from the evening** (§1.9).

### 1.5 Return after a week

- **Face.** A greeting brow flash, then LP 0.58, CR 0.40, F0 range +0.36 over the first exchanges; a stranger gets 0.35. The memory works: retrieval brings back last week's topics.
- **Verdict.**
  - Good, with one problem (§1.6).
  - K relief also makes the agent light up at *any* familiar or unfamiliar person after a gap. Contact is generic, and only f_id, one scalar, makes it the operator.

### 1.6 Own scenario A: return after a week, first words are bad news

Script: K = 0.99. The user's first utterance is an unprompted report with need 0.8 ("my father died"), followed by ordinary exchanges.

| Window after his first utterance ends | LP | CR | BI | FR |
|---|---|---|---|---|
| 0–12 s | 0.59 / 0.40 | 0.40 / 0.19 | 0.35 / 0.14 | +0.36 / +0.17 |
| 12–52 s | 0.63 / 0.32 | 0.36 / 0.07 | 0.38 / 0.24 | +0.32 / +0.07 |
| 52–172 s | 0.28 / 0.25 | 0.02 / 0.00 | 0.32 / 0.24 | +0.06 / +0.03 |

- **Why.** K relief is applied at the completed exchange, which here is the end of the bad-news utterance. 𝒟_K drops 0.21 in one step, and v jumps to about +2.5/min, so r ≈ 0.9.
- **What the face shows.** A Duchenne smile with raised pitch range, at the moment the user finishes saying his father died, mixing over a minute into a smiling concern face.
- **Verdict.** A concrete appropriateness failure. People greet on sight and then follow the news; this agent's gladness is locked to his turn end and blind to his content.

### 1.7 Own scenario B: a joke at the agent's expense ("Ha, you dumb robot", laughing, LP 0.8)

- **Free display** (lexical hostility 0.5 latched):
  - BI 0.22 / LD 0.17 / gaze away 0.15 in the first 25 s;
  - BI 0.14 / gaze away 0.15 to 2 min;
  - BI 0.07 / gaze away 0.09 at 10–15 min.
- **The cone** cancels part of the brow through G₀'s skew entries (the agent's BI falls with the partner's smile): −0.11 at 20 s, −0.19 at 2 min. It does not touch gaze aversion or latency.
- **Play is blocked** while V_L ≥ 0.1: P stays at 0.345 after seven play exchanges. So the agent does not laugh back.
- **Verdict.**
  - It looks briefly hurt and keeps averting its gaze at a friendly tease.
  - Teasing is distinguished from hostility mainly by nonverbal off-record markers (laughter, smile, playful prosody; Keltner et al. 2001, named as a pointer, not read). Check T puts every one of those in F, where they cannot touch T appraisal.
  - A partner who teases affectionately would, over months, train nothing out of this, because nothing learns V_L's map (§1.8). The agent stays thin-skinned with that person.

### 1.8 What the strong held displays actually rest on

Every strong held display in §3.12 comes from T state. T state is driven by three word readings:

| Quantity | Specified as | Can it be built? |
|---|---|---|
| N_L, need from unprompted reports | frozen decoder trained on the agent's *own* (utterance, own load) pairs (§2.9, P3) | **No, as specified.** The agent's words are Claude's. Claude never sees the loads, so the words depend on them only through the retrieved snippets and a 1-of-6 Gumbel choice scored mostly on the partner's need. The agent never reports an interview, illness, tiredness or loneliness, so the partner's reports are out of support. Yoshida & Man's self-decoder works because the expression channel is *caused* by the body; for words here, it is not. And where the agent's words do co-vary with its loads, they are its comforting words while V_F is raised by a distressed partner looking at it (V_F = the aversive part of b̂_p × gaze). So the decoder would learn "comforting words → high V", which brings revision 2's comfort reversal back through the decoder. |
| V_L, hostility of the partner's utterance addressed to the agent | named in §2.1, never defined | **Undefined.** A toxicity or sentiment model is a classifier on the user's words. An own-data map has no positives. |
| A_L and play structure, lexical surprise | 𝓜's lexical surprise | Computable, but F-typed (§2.2) |

The G7 scenarios are consistent with the display equations, but their inputs (need 0.47, hostile 0.7, play True) are exactly the load-bearing unknowns.

### 1.9 Does its own state drive the face richly, or is it a talking head?

- **Not a statistical talking head.** Nothing reproduces video statistics, and the agent's own needs (K, P, E, hurt) do move its face.
- **But the face reacts to *words and turns*, not to the person.**
  - Strong held expression needs a T event: a reported need, a hostile word, a completed or play-structured exchange, a reunion.
  - The person's face and voice reach held expression only as ≤ 0.10 in phase, plus the innate cross and away entries of G₀: warmth to sadness, quieter to loudness.
  - With the transcript and turn order fixed, two users, one beaming and one stone-faced, get the same strong display.
- **The face is a fixed table on about six scalars.**
  - The free display is Π₀(r, d, c_L, h, e, f_id) plus learned deviations.
  - r and d are the two signs of v_T, one scalar. The rest are four named gauges.
  - Π_o's capacity (an MLP on 160 T inputs, including μ_T and slot reads) is real, but its only training signal is J, and J's derivative with respect to the display is:
    - zero through 𝒟(b): no own load depends on the display in rollouts. K and P relief use imputed exchange structure, V_F and A_F use the imputed F, and the own-body head is trained on E, I and own-driven A;
    - zero through the options and care terms inside 𝒟_p's dead-band;
    - nonzero only through act → N while the partner is in need, and N is read through the broken decoder (§1.8).
  - The cone's bases and α(z) have the same gradient structure.
  - So for most of the agent's life the face is Π₀ plus G₀, and the 128-d mood, the slots and 𝒦 never show.
  - This is the "few scalar gauges, a scalar value and linear maps" pattern that the brief's Expressive structure says is a sketch. The §3.15 claim of warmth to one partner and quiet distance to another, on the same words, through α, N_L priors and f_id, has no working training route: α is not trained, the N_L decoder cannot be fitted, and f_id is one scalar.

### 1.10 Own scenario C: a bored, disengaged user

Script: replies of "yeah" or "ok" every 20 s, flat face, no play, for 30 min.

- **Face.** K stays in its dead-band, because every "yeah" completes an exchange. P creeps up (0.30 → 0.37), so the positivity offset drops out. The face sits at LP 0.09, FR +0.04, unchanged for 30 min (scen.py C).
- **No bid.** C_F ≈ 0 for a flat face, so lapses get no bid.
- **Claude may notice the monosyllables in the transcript,** but the face shows no disappointment, no lowered energy and no attempt to re-engage.
- **Verdict.** Polite, unbothered and inert. That is not harmful, but it is not alive. The contact need is satisfied by the *count* of exchanges, whatever their quality.

## 2. Principles, concretely

### 2.1 Principle 1

No face or voice classifier. But V_L's "hostility" (§1.8) is, under any computable reading, a classifier on the user's words. Principle 1 names face and voice, so this is the spirit rather than the letter. Combined with Principle 2, it is an affect label on the partner below Claude, and it must be defined or removed.

### 2.2 Principle 2 and the typing

- **Names.** "Concern" (C) is now a care term, not a body variable, which is good. "Contact" (K) and "play" (P) are needs named by function: an acceptable innate set, as stated. "Hostility" (V_L) is an affect label in all but name (§2.1). The four display drivers (relief r, distress d, word concern c_L, hurt h) are each wired to a prototype face by Π₀.
- **The valence readout.** It is a readout in form: v = −d𝒟/dt over a hand-specified 𝒟. But it is not read out of a *learned latent*, and it is the main driver of the face. In the brief's terms, valence is effectively set, by formula, and expressed through a fixed table. That is defensible as a newborn reflex only if something later learns past it, and nothing does (§1.9).
- **A type error.**
  - 𝓜 takes u and a as inputs (§6.2 layer 14: "inputs 35 + 3 + …"), so anything computed from 𝓜 is F by Check T's own clause ("anything computed from u … or from an F value").
  - Its lexical surprise nevertheless feeds A_L, declared T (§2.1, §2.7), and the play-structure rule, also T (§2.8).
  - So the partner's face and voice can move A_L and P relief, hence v_T, hence the uncapped free display (relief up to LP 0.55, own laugh 0.45), outside the cone.
  - I did not size the route; that is for the route critic. The fix is cheap: compute lexical surprise from a words-only predictor of the partner's next utterance given the transcript.
- **Turn events.** "Completed exchange" is segmented from partner VAD (F). Only its order is declared T. That is a definitional choice: it is stated (R29), and I accept it.

### 2.3 Principle 3: essential for words and bids, absent for the face's response to the face

- **Reading works through the agent's own body.** b̂_p = Π̃(Rξ₀) inverts the agent's own free display, and the crossed-habits lesion changes which faces raise C_F. That changes bids and draft choice: a signed, essential prediction. Pass.
- **Π̃'s support is narrow.** The agent's own *sustained* inner-brow or depressor displays come only from hurt (h, from V_L) and word concern (c_L, which is not a load). The distress display is rate-driven and transient.
  - So a held sad face inverts to "hurt" (high V), and a sad user looking at the agent raises the agent's own *aversive* load V_F.
  - The design's "inverse gain ≈ 2.2" refers to the transient distress gains, not to the sustained regime that silent sadness occupies.
  - G3 and G7.1 set the face load to 0.6 by hand and never pass it through Π̃.
  - This is a risk to measure, not a demonstrated failure.
- **The face's held response to the partner's face (the cone) does not pass through the agent's body.** It is linear in the raw traces of Pu. Principle 3's mimicry clause ("drive the agent's own motor and affect pathways") holds for the fast wrap (in own synergy coordinates R) and for F affect (V_F, A_F, C_F). But F affect never shows on the face except through the cone, so the face does not show "feeling through my own body" of the partner. State it.

### 2.4 Principle 4: compliant; two small undeclared bits

- **Compliant.** The prompt has no values, labels or ids. Regulation now exists through P_name without Claude reading anything. Pass.
- **Bid and greeting requests.** These are made only when C ≥ θ_C, or at presence with K ≥ 0.3. The request itself, plus "[silence 6 s]", tells Claude "the engine chose to speak", which is one bit of state per bid. Declare it next to the 6-bit retrieval channel. Also specify what the bid's prompt contains: drafts requested at the moment C crosses θ_C may predate the silence marker and answer a turn that is long over.
- **Naming.** P_name's match m is PMI over the agent's own tokens, and those are Claude's (§1.8). In practice m measures "said topic-typical comforting words while the partner was in need", not self-labelling. The G6 regulation effect is fine as a mechanism. Its grounding is weaker than "naming its feeling".

### 2.5 Principle 6

- **Display and exchange imputation: clean.** No rollout values the partner's face, laughter, staying or reply rate. K and P saturate, and absence is never preferred (G4c). Pass.
- **The prompted-reply guard is a lexical rule:** ≤ 6 tokens after an agent question containing "you".
  - "How's the prep going?" contains no "you". "It's better now, honestly" passes as unprompted and lowers N̂.
  - 𝓜 cannot separate act → Q from act → N → Q (§3.16.6, Avin–Shpitser–Pearl), so in learned rollouts, reassurance-eliciting questions earn credit.
  - G5a tests only the hand rule. This is F4′, named by the author, and it remains the main placation risk.
- **The options term** (§2.9 item 7) is ambiguous:
  - if its count of predicted partner-initiated moves uses the imputed act → Q edge, it is act-independent and inert;
  - if it does not, it credits drafts for making a distressed partner raise topics, ask and decide more. Capped and need-gated, but still a target on the user's behaviour. Pick one and state it.
- **I as a load.** It is minimised, so where I includes partner-forecast variance it would credit making the partner predictable. In revision 3 it reads only the own-body head, so it is inert (§2.7).

### 2.6 Principle 7

Unchanged: transcript and snippets go to the API, which is an operator decision. Pass.

### 2.7 Principle 10

- **What follows from the core.** One objective J with typed constraints. Homeostasis, gladness as relief, care and replay follow.
- **What does not.**
  - The emotional *content* is the innate assembly: Π₀'s table, V_L's undefined hostility, the play rule, the initiative rules, G₀.
  - Curiosity does not follow. I is the own-body head's forecast variance, that head now models only E, I and own-driven A, so I is almost constant, and it is *minimised*. "Curiosity | I" in the §2.11 table is not a mechanism.
  - Either drop curiosity from the claims or give it a satiable information-gain term computed on 𝓜's own predictions, shown not to target the partner.

## 3. Long-term goals

### 3.1 Learning by living: what is learned online and what is innate

| Element | Learned how | In practice |
|---|---|---|
| perception, 𝓜, slots, concepts, PMI | likelihood, online and nightly | learns well |
| emotions (categories) | DP-means over slow state; named by PMI on own tokens | categories form; naming grounded weakly (§2.4) |
| expressions (Π_o, cone, α, fast gates) | J only | **≈ innate for life** (§1.9). Gradient only in partner-need episodes, through a decoder that cannot be fitted |
| manner of speaking | the 130-parameter scorer, retrieval query, phrase targets from Π_o and cone | learns playful uptake through P's own-contribution clause; the rest ≈ innate |
| care (which acts help) | J via act → N, read through the need decoder | **blocked** by §1.8 |
| relationship | slots (30 days), f_id, identity-keyed α | f_id and slots: yes. α: no gradient |

The brief's second long-term goal, an AI that acquires its emotions, manner of speaking and expressions by living, is met for perception and memory. It is not met for expression, which is the part a person sees.

### 3.2 S4, its own face body

- **Reachable.** 𝓔 and its ridge inverse R fit the agent's own rendered face, and the muscle model sits behind M.
- **One caveat.** The cone's guarantee is a quadratic form in the shared counterpart basis: eᵀ sym(G) e for e in the same coordinates for partner and self. It is invariant only under orthogonal changes of basis.
  - When S4 replaces MediaPipe in the body route, keep the cone, and the copy metric, in camera-measured coordinates of both faces, or re-derive the bound.
  - If the cone reads the partner in a learned, non-orthogonal own-muscle basis, eᵀ T G e is not bounded by b.

### 3.3 S5, two-way contagion

- **There is now something to follow.** Reunion smiles (0.58), play laughter (0.24), hurt (0.32) and relief (0.30–0.44) are within webcam-measurable range.
- **The ablation is confounded.** Almost all of these are caused by the operator's own words and turns. In an S5 test, his face following the AI's is therefore partly common cause.
  - The design gives no S5 ablation prediction.
  - It needs one that uses AI-originated expression (K, P, E, the greeting) or a timing analysis that removes common cause, with the prediction "lesion Π_o's v_T drive → following drops".
- **Sluggish smiles.** The relief display rides on v, which is smoothed with τ = 5 s and updated at 2 Hz. Reunion smiles step up within one tick and then decay over 5–10 s. Smile dynamics (onset, apex, offset) matter for whether a smile is read as genuine. Specify the display's temporal envelope at render.

### 3.4 S6, temperament and relationship over months

- **Relationship.** f_id (one scalar), identity × topic slots and topic-wise N_L. The N_L part is blocked (§1.8).
- **Temperament.** Consolidated weights, but the expressive weights barely move (§3.1), so temperament would show in 𝓜 and memory, not in the face.
- **Robustness to Claude upgrades.** Good for state. The PMI table and the need decoder are fitted on Claude-written own text, so an upgrade shifts their training distribution. State this.
- **The ablation stands.** Strip the state tags from replay and familiarity and slot recall decay.

### 3.5 Ablation predictions (Principle 5)

- **The §7 table is good for the bounds.**
- **Missing, each with a behavioural prediction:**
  - K: no reunion gladness, and no stranger/operator difference;
  - P: no play laughter;
  - Π₀'s relief and distress rows;
  - G₀;
  - V_L;
  - the greeting;
  - the positivity offset;
  - S5 (§3.3).
- **Unfalsifiable as written.** Once the expressive weights do not learn, "slots and α → 2-d" predicts no change in the face, because α was never trained.

## 4. Buildability on this Mac (M1 Pro, 16 GB)

- **Sizes and compute are fine.**
  - About 710k learned parameters.
  - The per-frame cost is dominated by MediaPipe (×2, about 13 ms each) and rendering.
  - Under 2.4 GB online, about 40 min of nightly replay, and 1.8 GB of storage per 30 days. Credible.
- **Body onset: underspecified in a way that breaks conversation.**
  - The trigger is "partner VAD offset + 0.30 s". VAD offset already lags speech end by the VAD's hangover (typically 0.1–0.5 s), and within-turn pauses of 0.3–1 s are common.
  - With no gate on the predicted end of the turn and no abort if the partner resumes, the body will start to take the floor at pauses (inhale, gaze, brow 0.15, then "mm" at 0.5 s), and the words will follow over his continuation.
  - Gate the onset on the same turn-end predictor used to request drafts (falling F0 plus syntactic completion), make it abortable on partner resumption, and treat "mm" at a non-final pause as a backchannel, not a turn.
- **Claude drafts.**
  - Six drafts must all be complete before scoring.
  - As one call, the output is about 6 times longer, roughly 3–6 s to the first word with a mid-size model.
  - The "0.8–2 s to first word" needs six parallel streaming calls to a fast model, short drafts, prompt caching of the transcript, and scoring on the first sentence.
  - Specify this, and the cost: about 6 times the input tokens per turn without caching. Speculative requests at the predicted turn end are wasted whenever he goes on.
- **TTS.**
  - The design needs phrase-level F0 level and range, energy, rate, pause and latency targets.
  - It also needs a zero-mean continuous contour and non-lexical bursts: an own laugh at 0.22–0.45, "mm", "oh", an inhale, breathiness.
  - Few local TTS systems expose all of these. This is open under Q1 and a buildability risk the design does not name.
- **Underspecified items:**
  - V_L (§1.8);
  - the need decoder's training data (§1.8);
  - the bid prompt's contents (§2.4);
  - the options term (§2.5);
  - "presence onset" (face detection hysteresis);
  - the lemmatiser and the anaphor and continuation rules for play structure.
- **Not unbuildable.** Nothing here is unbuildable in principle.

## 5. Verdict

**Not yet fit to put to the operator as a build candidate under Q19/Q21.** Known concrete failures remain. None reopens the core certificate, and most are local. What must change, in order:

1. **Ground the word-need decoder.**
   - It cannot be fitted on the agent's own Claude-written words.
   - **Options:**
     - (a) Fit it nightly on the *partner's* words against the partner's concurrent face-read loads b̂_p, which keeps Principle 3 through the agent's own face. Freeze it per night, keep runtime input words-only (T), and then re-derive the placation argument, because words that predict a happy face become creditable.
     - (b) An innate seed projection from the sentence embedding onto the load axes using body words only (tired, tense, hurt, alone, bored): a declared Principle 2 strain.
   - Then rerun G5b and G7.2 with a decoded N_L, not one set by hand.
2. **Define V_L** without a classifier on the user, or remove it and let hurt come from a defined quantity (for example, the decoder's V reading of utterances addressed to the agent, under fix 1).
3. **Make K relief content-aware.**
   - Apply relief at the greeting exchange: presence plus the agent's first turn, not the partner's first turn end.
   - Gate the relief *display* (not the relief) while a T distress load is rising, as play is already gated by V_L and C_L.
   - Recheck scenario A (§1.6).
4. **Let play be told from hostility.**
   - Add an attenuate-only F → T port on V_L's latch: the partner's laughter and smile may shorten the hurt, never raise it.
   - Count its in-phase contribution (un-hurting raises the agent's lip corners while the partner smiles) in the held budget, as a_name is.
   - Or keep the type rule pure and state plainly that teasing reads as hurt.
5. **Give expression a learning signal that is not the partner's display.** Without one, the face is Π₀ + G₀ for life.
   - **Candidates:**
     - a facial-feedback or efference term, where the agent's own display enters its own A or E cost;
     - a likelihood objective in which Π_o predicts the agent's own later T state (expression as a forecast of its own body);
     - credit through the decoded need path once fix 1 makes it real.
   - Then show one behaviour that a 6-scalar Π₀ cannot produce, learned in a stated number of nights.
6. **Fix the type error.** Lexical surprise for A_L and for the play rule must come from a words-only predictor.
7. **Gate the body onset on the turn-end predictor,** make it abortable, and specify the six-draft call pattern and its latency.
8. **Curiosity and the options term.** Concede curiosity or add a satiable information-gain term. Make the options term act-independent or drop it.
9. **Smaller items.**
   - Declare the one-bit bid and greeting channel.
   - Specify the bid prompt.
   - Add the missing ablations (§3.5) and an S5 ablation free of common cause.
   - Note the S4 basis caveat.
   - Name TTS controllability as a risk.

**Design choices to put to the operator alongside the candidate, not failures:**
- **(A) The in-phase budget is isotropic.** D78 asks for strength set per expression. A diagonal budget, sym(G_m) ⪯ B_m with B_m diagonal, keeps the quadratic-form certificate (eᵀ sym(G) e ≤ eᵀ B e ≤ max B) and would let the operator choose, for example, 0.25 on smile, laughter and the sympathy brow and 0.05 elsewhere. With 0.10 everywhere, the agent cannot show sympathy brows at a silent sad face and cannot laugh because you laugh.
- **(B) The face follows words.** Strong held expression follows the transcript and turn sequence, and the person's face adds at most 0.10 toward. That is the price of the definitional seam (§8.1.1 of the design), and the operator should hear it in those words.

**If fixes 1–9 are made and the next critiques find nothing new,** the one-line description for the operator would be:

> *A copy-proof, knowing conversational agent built from known parts (robust REN, a one-sided matrix sector over completely monotone traces, information-flow typing, Yoshida–Man care with path-specific credit, Joffily valence): its face shows its own needs (missing you, play, hurt, tiredness, relief) strongly, and it reads your face fully, but it moves toward your expression by at most a tenth, so what you say and do, not your face, drives its strong expressions. Novelty: recombination.*

**Main risks to watch in testing:**
- the per-pair cross route (0.61, routes critic);
- the definitional seam: pooled cross-topic slope 0.56 for a user whose face varies with topic;
- whether a 0.17 smile at sadness reads as warm or as out of tune;
- reassurance elicitation through the prompted-reply guard (F4′);
- fast play satiation;
- whether Π̃ maps sustained sad faces to aversive load correctly;
- conversational timing, both barge-in and draft latency.

## Sources read

| Source | How read |
|---|---|
| brief.md | in full |
| research/questions.md | Q16, Q19, Q20, Q21 and Report 5 in full; Q17, Q18 and its answer |
| research/foundations/designs.md | in full |
| research/foundations/critique-2-design-cayley-ledger-agent.md | in full |
| research/foundations/design-cayley-ledger.md (revision 3) | in full, §0–§10, the revision 2 critiques and the answer, and the revision 3 history |
| research/foundations/sims/design-g3/out.txt | in full |
| research/foundations/sims/design-g3/checks.py | the drive engine, display, cone prior, G3, G4 reunion and G7 scenario code (lines 1–53, 300–470, 608–670), read and executed in sims/critique-cayley3-agent/scen.py |
| research/helping-without-placation-synthesis.md | the decoder and path-specific sections (lines 25–55) |
| research/foundations/design-cayley-ledger.r2.md | lines locating I, the lexical-body head and R14 |

**Not read, named only as pointers:**
- Keltner, Capps, Kring, Young & Heerey 2001 (teasing and off-record markers);
- Provine on laughter contagion;
- Skantze 2021 on turn-taking in spoken dialogue systems;
- Krumhuber & Kappas 2005 on smile dynamics.

No verdict depends on them alone. Every failure in the summary is derived from the design's own equations, constants and type rule.
