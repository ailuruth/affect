# Ending a mutual concern display (synthesis)

Sources read in full for this note: rogers-2018-dual-eye-tracking-mutual-gaze.md, binetti-2016-preferred-mutual-gaze-duration.md, ho-2015-gaze-signaling-dyadic.md, hu-2025-interactive-repair-stress-recovery.md, austry-2026-toddler-responses-to-distress.md; with beebe-2016-self-interactive-contingency.md, hess-bourgeois-2010-you-smile-i-smile.md and the still-face notes (mesman-2009, ekas-2012) already in the index. Written for the concern look's open failure (questions.md, Q24/Q27; design-cayley-ledger.md, the mirroring partner who holds the look on).

**Not reached** (hosts blocked in this environment; nothing below cites them): Bavelas, Coates & Johnson 2002 (listener responses inside a "gaze window"); Bavelas et al. 1986 ("I show how you feel", motor mimicry ending with eye contact); Peräkylä et al. 2015 (recipient affiliation lowers the teller's arousal); Kaukomaa, Peräkylä & Ruusuvuori 2013/2015 (turn-opening smiles; listeners' faces shifting the stance of a telling); Voutilainen et al. 2018; Gianino & Tronick 1988. These are the papers that would time adult listeners' faces during trouble-telling. **No source read here measures how long an adult listener holds a concern face in a recorded conversation.** That number is still missing.

## 1. What a human listener does instead of holding the look

**Gaze never holds.** In live conversation between strangers, mutual eye contact lasts about 0.36 s per episode and mutual face gaze about 2.2 s (per-conversation means 0.7–4.7 s; Rogers et al.). Each fixation lasts under a second and moves among eyes, mouth and other face. A stranger's direct look becomes uncomfortable after about 3.3 s ± 0.7 s, sooner for a face judged threatening (Binetti et al.). People still feel they had eye contact ~70% of the time, because what they track is face gaze, not eye fixation.

**Gaze breaks are driven by turn-taking, not by the other's face.** A speaker looks at the listener to give up the turn; the listener starts talking about 400 ms later. The new speaker begins with gaze averted and looks back about 700 ms in (Ho et al.). In fast exchange the two people's gaze is anti-correlated (r ≈ −.18). So each turn, including a two-word comfort, breaks mutual gaze at least once.

**The display is a short mismatch, and it is the caregiver who leaves it.** In infant–caregiver coding a caregiver's sad, worried or concerned face counts as a mismatch. The state the dyad returns to is the caregiver gazing at the infant with an attentive, interested face and voice, or a smile (Hu et al.). Mismatches last about 5 s on average in play and 11–17 s after a stressor. Faster return predicts better recovery. Caregivers follow infants several times more than infants follow them, and each person's face is mostly driven by its own recent past: self-effects 4–52× partner effects, partner β ≈ .02–.14 (Beebe et al.). When the infant turns away, the mother sits back (Beebe et al.), which is a negative-sign response on orientation. In adult strangers' live talk, frowns are barely coupled at all (r = .08, Hess & Bourgeois).

**Inner change outlasts the face.** Toddlers watching distress showed a facial-temperature change that lasted to 200 s, with no measurable increase in concern faces (Austry et al.). Weak evidence (video, posed), but in the same direction: the visible display is not a readout of the slow inner state.

## 2. Timing, channels, replacement

| | Human evidence | Source |
|---|---|---|
| Eye-to-eye contact | ~0.36 s per episode | Rogers |
| Mutual face gaze | ~2.2 s per episode (means up to 4.7 s) | Rogers |
| Comfort limit for a direct look | 3.3 ± 0.7 s, shorter if threatening | Binetti |
| Gaze at own turn onset | averted, back ~0.7 s in | Ho |
| Partner speaks after a yielding look | ~0.4 s | Ho |
| Mismatch (display) episode | ~5 s in play, ~11–17 s after stress | Hu |
| Partner influence on own face | β .02–.14 against self .5–.6 | Beebe |

Channels that change first: **gaze** (seconds, tied to turns), then **orientation** (stepping back when the other turns away), then the **face**, which returns to an attentive, interested neutral or a smile. What replaces the look is not a blank face and not a copy of the partner. It is attention carried by face-scanning gaze and voice.

## 3. What it implies for the design (no labels below Claude)

1. **Separate the gaze channel from the brow display.** The look as specified holds gaze and brow together for minutes. Human gaze in a dyad never holds: give the agent's gaze its own cycle. Use about 1-s fixations moving among the partner's eyes, mouth and face, with eye-to-eye episodes under a second and face-directed episodes of ~2–3 s, jittered (s.d. ~0.7 s). Add short off-face breaks. None of this is gated by the partner's face. This alone removes the eye-to-eye hold that a mirroring partner can lock onto.
2. **Tie gaze to the agent's own turns.** At every agent utterance onset gaze leaves the face and returns ~0.7 s in. At the end of an agent turn, a look at the partner yields the floor. A mirroring partner then meets a gaze break every turn, set by the agent's speech timing.
3. **Make the brow display an episode with its own decay, not a state.** On the infant evidence, the display is a mismatch the carer ends within seconds to tens of seconds by returning to attentive engagement. The display's offset should come from the agent's own dynamics, and the partner's matching face should never extend it. This agrees with revision 8.3's rule that only distress words or sobs renew it. A new distress event may start a new episode, but the face itself is not evidence.
4. **Replacement state: attentive neutral plus voice.** After the episode the face goes to rest with brows level and gaze cycling on the face. The voice stays available for a back-channel or a short exploration question. A slow body variable may stay perturbed for minutes, but it does not drive the face back into the display. The face is driven by the episode, the body sets only the readiness to start one.
5. **Keep partner→face gains small and gaze coupling non-positive.** Measured partner effects are an order of magnitude below self-effects, brow coupling between strangers is near zero, and gaze in fast talk is anti-phase. A positive gaze gain (look back whenever looked at) is the loop.
6. **Orientation step-back.** If the partner looks or turns away during the display, the agent eases posture back and does not lean in or chase (the mother's sit-back in Beebe et al.).

**Tests.**
- With the author's mirroring partner (J33 P4b–d), no mutual face-gaze episode lasts more than ~5 s and no eye-to-eye episode more than ~1 s.
- The brow display ends within the episode limit, whatever the partner's face does.
- Repair latency, computed Hu-style from agent and partner per-frame states, stays near the human ranges (median mismatch seconds, not minutes).
- Lagged cross-correlation of the agent's gaze with its own speech reproduces Ho's ~0.7-s return; with the partner's gaze it is ≤ 0.

**Open.** Adult evidence on how long a listener's concern face lasts during trouble-telling, and on what face follows it (smile, neutral, nod), is in the unreached conversation-analysis and Bavelas papers. Item 4's "attentive neutral" rests on infant coding and adult gaze data, not on a measured adult face sequence.
