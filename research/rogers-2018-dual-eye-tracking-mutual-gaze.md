# Rogers, Speelman, Guidetti & Longmuir 2018, "Using dual eye tracking to uncover personal gaze patterns during social interaction" (Scientific Reports 8:4271, doi:10.1038/s41598-018-22726-7)

Source read: full text from PubMed Central (PMC5844880, via the PMC OAI full-text record): abstract, introduction, results, discussion, method. The online supplement (per-participant gaze plots, ICC tables, data sheets) was not read.

## Claims
- In live, face-to-face getting-acquainted conversation, mutual face gaze (both looking somewhere on the other's face) is common and comes in short episodes; mutual eye contact (both looking at the eyes) is rare and fleeting.
- People nonetheless judge that eye contact happened most of the time. The authors argue that perceived "eye contact" is really mutual face gaze, and that people are largely blind to where on their face the partner is looking.
- Gaze is an "active eye": any location is fixated for under about a second before moving on, outside both partners' awareness.
- Each person has a stable personal eye-to-mouth gaze preference, the same when speaking and listening.

## Evidence with numbers
- 76 students, 176 four-minute unstructured getting-acquainted conversations, seated 1 m apart, both wearing Tobii Pro Glasses 2 (50 Hz). Only accurately tracked data kept: 107 gaze sets from 49 participants; 51 conversations with both partners tracked for the mutual-gaze measures. Frame-by-frame manual coding in Mangold INTERACT of on-face regions (eyes, nose, mouth, forehead, other face) and off-face directions. Kappa .68/.70 for gaze, .78/.92 for speaking/listening (one dyad double-coded).
- **Mutual face gaze: 63% of the conversation (SD 16, range 27–88%), in episodes averaging 2.2 s (SD 1.0, range of per-conversation means 0.7–4.7 s).**
- **Mutual eye contact: 12% of the conversation (SD 12, range 0–46%), in episodes averaging 0.36 s (SD 0.2, range 0.1–0.9 s).**
- Perceived eye contact: 5.5 of 6 ("often"/"very often") in the lab; in a classroom replication (n = 171) people estimated 72% of the conversation (SD 16).
- Off-face gaze: 29% of the time while speaking, 10% while listening (t(48) = 13.79, d = 1.82). Average fixation on any region just under 1 s (nose, forehead, other face ≤ 0.5 s).
- When on the face: eyes 48% and mouth 29% while speaking; eyes 43% and mouth 34% while listening (small effects, d ≈ .17).
- Within-person consistency across conversations: ICC .88 for proportion of eye gaze, .80 for mouth; mean fixation length ICC .73 (eyes), .69 (mouth).
- The authors compare the 2.2-s mutual face gaze with a ~3.3-s preferred duration found with video stimuli (Binetti et al. 2016, see binetti-2016-preferred-mutual-gaze-duration.md): live mutual gaze is about a second shorter.
- Limits stated: small, unbalanced sample (some people in up to seven conversations); first-time use of the glasses; only getting-acquainted talk between strangers, no emotional content; the perception question asked only about eyes.

## What it implies for the design
- A held mutual look is outside the measured human range. In ordinary talk the two faces are mutually oriented for a couple of seconds at a time (per-conversation means up to 4.7 s), and eye-to-eye contact lasts about a third of a second. The agent's look should never hold eye-to-eye contact as a steady state, whatever its brow is doing.
- Human listeners keep "being with" the speaker by scanning the face (eyes, mouth, other face), not by fixing on the eyes. That is a channel the agent can vary freely: the partner experiences attention as face gaze, not as eye fixation, so moving the agent's gaze among face regions every ~1 s costs no perceived contact.
- Listening involves less off-face gaze (10%) than speaking (29%). A listening agent can stay mostly on the face; its looks away should be mostly brief.
- What this paper does not give: anything about distress, concern displays or facial expression. It is a gaze baseline for neutral talk between strangers.

## License
CC BY 4.0.

## Runs on this Mac without a GPU?
n.a. (empirical study).

## Verdict: adopt (as the live-dyad gaze baseline: mutual face gaze ~2.2 s per episode, mutual eye contact ~0.36 s; attention is carried by face gaze and active scanning, not by a fixed look)
One lab, strangers, neutral topics, n = 51 conversations for mutual gaze; durations are per-conversation means, not maxima.
