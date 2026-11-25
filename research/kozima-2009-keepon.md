# Kozima, Michalowski & Nakagawa 2009, "Keepon: a playful robot for research, therapy, and entertainment"

Hideki Kozima, Marek P. Michalowski and Cocoro Nakagawa, *International Journal of Social Robotics* 1(1):3–18, 2009, doi:10.1007/s12369-008-0009-8. Companion: Michalowski, Sabanovic and Kozima, "A dancing robot for rhythmic social interaction", HRI 2007, pp. 89–96.

Source read:
- The IJSR paper: the full published PDF from the CMU Robotics Institute publications server (publications.ri.cmu.edu, pub_files/2009/1/fulltext.pdf). Sections 1–6 were read in full; the reference list was skimmed.
- The HRI 2007 dance paper (same server): sections 1–4.3 read, covering system, setup, initial chi-square analysis and the start of the Noldus coding. The remainder of its results and discussion was skimmed only through figure values.
- Not read: the separate controlled rhythm study [35] cited in the IJSR paper, and Michalowski's 2010 thesis.

## Claims
- A minimal robot that shows only attention (where it looks) and emotion (rocking, bobbing, vibrating), with a soft deformable body, lets infants, toddlers and autistic children perceive a "mind" without being overwhelmed. Their earlier 29-DoF humanoid Infanoid caused anxiety in children under three. The authors attribute this to the difficulty of integrating many separately moving parts into one gestalt.
- Typically developing children's play with Keepon changes with age. Children under 1 treat it as a "moving thing" (touch and mouth). Children aged 1–2 treat it as an "autonomous system" with attention and emotion, and some mimic its rocking and bobbing. Children over 2 treat it as a "social agent" whose responses are contingent on their own acts.
- Autistic children formed dyadic, then triadic and empathetic relations with Keepon. The authors propose that the "missing motivation" to share mental states is present in autism and that Keepon offers a "bypass channel" past a failed "social filter".
- Rhythm matters for engagement. A robot moving in synchrony with music made children more likely to start dancing.

## Architecture (as given)
- **Body**: 120 mm silicone "snowman". The eyes are two 120° wide-angle CCD cameras and the nose is a microphone. Four DoF, driven like a marionette by gimbal and wires: nod ±40°, pan ±180°, rock ±25°, bob with a 15 mm stroke.
- **Two action types**:
  - attentive: orient head and gaze, giving eye contact and joint attention;
  - emotive: rock and/or bob, or vibrate, while attention stays fixed, plus "pop" sounds. Pleasure means side-to-side rocking, excitement means bobbing, fear means vibrating. This mapping was fixed by design.
- **Automatic mode** (described, rarely used): face, toy and motion detectors feed an "attention map" of salience. Habituation shifts attention away from a stimulus held too long. The robot orients to the most salient target, and its "emotional expressions are determined by the type of object and its relative salience".
- **Manual (wizard) mode**, used for nearly all studies: an operator watching the onboard cameras clicks gaze targets and presses keys for emotive actions.
- **Dance system** (HRI 2007): implemented in Max/MSP.
  - A master metronome gets its BPM from the last three roughly evenly spaced "taps". Taps come from audio amplitude peaks, beat detection, hand-labeled beats, optical-flow direction reversals with hysteresis, or zero-crossings of a low-pass-filtered accelerometer magnitude in a toy.
  - Each DoF has random binary switches (active, limit or full cycle per beat, phase) and a random range, re-drawn at random intervals "to keep the dance interesting".
  - The operator sets the direction of attention; the rhythmic movement around it is autonomous.

## Evidence with numbers
- **Scale**: about 400 hours of recorded interaction with "hundreds of children" over four years.
- **Lab**: 25 typically developing children in three age groups:
  - under 1 year: n = 8, mean 9.0 months;
  - 1–2 years: n = 8, mean 16.5 months;
  - over 2 years: n = 9, mean 37.3 months.

  Sessions lasted 10–15 minutes until boredom. Results are qualitative descriptions of interaction styles; no statistics.
- **Preschool**: 27 children aged 3–4 over about 25 sessions in the playroom. Results are qualitative vignettes (caregiving, protecting, teaching, seeking praise). The authors note the children "never lost interest even after 20 sessions", against boredom after 15 minutes in the lab.
- **Autism day-care**: over 30 children, over 100 sessions (700 child-sessions) across three years. The paper gives three case narratives:
  - M: 15 sessions; gaze aversion, then touch, then a kiss.
  - N: 39 sessions over 17 months. In S33 she began an "imitation game" in which Keepon, teleoperated, copied her bobbing, rocking or bowing, while she looked referentially at her mother.
  - S: 15 sessions; from kicking to protective behavior.

  One figure tracks eye-contact distance over five months for two children. The authors state the cases are "not to be considered generalizable".
- **Dance open house** (HRI 2007):
  - 116 children were coded in the first pass, and 35 danced. Significantly more began dancing when Keepon was already moving in synchrony with the music: χ²(1, N = 116) = 9.321, p = 0.0023.
  - In the second pass (Noldus coding, 113 girls and 96 boys), Keepon was in synchrony with the music for 37.9% of the time, out of synchrony for 52.6%, and still otherwise.
  - The authors caution that the codes "were the result of rather subjective impressions on the part of the coder".
- **Controlled rhythm study** (summarized in IJSR §5.3): a scripted teleoperator switched Keepon between synchronizing to a toy accelerometer and to song tempo. The authors report that novelty, age and individual variance made it "difficult to consistently elicit the desired rhythmic behaviors". No effect size is given in this paper.

## Failure modes (reported or evident)
- **Mostly teleoperated.** The "attention" and the contingent "emotional responses" that children reacted to were chosen by a human operator in almost all studies. The case reports are evidence about children's responses to a well-timed human-in-the-loop puppet, not about a robot's internal state.
- **No internal state.** In automatic mode, expression is a fixed function of object type and salience, with habituation as the only dynamics. There are no drives, no persistence across sessions and no learning.
- **Mimicry was wired or wizarded, not learned.** The "imitation game" with N was performed by the operator. The dance system copies tempo by peak-interval arithmetic and adds random variation.
- **Synchrony was not manipulated.** In the dance study, the robot responded to visual motion, not to the music. Whether it was "in synchrony with the music" depended on whether people in view were already moving to the music. The predictor is therefore confounded with the outcome (children dancing). The authors' controlled follow-up failed to elicit the behavior reliably.
- **Assembled, but small.** A salience map, habituation and a metronome; no unifying principle is claimed.
- **No ablations.** The Infanoid comparison is anecdotal. The dance study's comparison is observational.

## License
Springer journal article; the author copy is on the CMU RI server. The HRI 2007 paper is ACM/IEEE, with an author copy on the same server. No code released (Max/MSP patches not public).

## Runs on this Mac without a GPU?
n.a. There is no code. The rhythm extraction (interval of the last three peaks) is trivial to re-implement.

## Verdict: watch (design and evaluation lessons; no architecture to adopt)
Keepon shows what a minimal expressive channel achieves when a human supplies the contingency. It also shows how hard it is to get a controlled effect out of child–robot rhythm play.

## What it implies for this engine
- **Contingent timing carried most of the effect.** Children moved from "thing" to "system" to "social agent" as they discovered that the robot's attention and emotion were contingent on their own acts. Keepon had four degrees of freedom and a human operator supplying the timing. Expressive richness was not what produced the effect. This supports the brief's emphasis on timing and on S5's coupling measures over face realism. It also warns that an engine judged on engagement alone could be matched by a well-timed puppet. The evaluation must lesion the internal state (Principle 5), not just show engagement.
- **The authors' phase argument.** "A purely reactive system cannot, theoretically, be synchronous", meaning in phase rather than merely at matching frequency, because of sensing and acting delays. In-phase coupling needs anticipation. This matches hoffman-breazeal-2007-anticipatory-action.md. For the engine, the self–other face map must be predictive (lead or zero-lag), not a lagged copy.
- **The mirroring direction in the "imitation game" was the parent's direction.** The robot (operator) copied the child, the child led and checked the adults, and triadic sharing followed. This is the contingent-mirroring arrangement the engine relies on for learning, with the roles reversed: in the engine the user mirrors the Bot. Two lessons for learning the self–other map from it:
  1. The mirrored partner here was the leader and stayed engaged. Being copied can sustain interaction. It does not show that copying is the best partner behavior; see striano-2005-social-contingency-1-3-months.md.
  2. Because copying was operator-timed, there is no data on what lag or fidelity made it work. The engine must measure those itself.
- **Too many moving parts hurt readability.** Infanoid's many independently moving parts were hard for young children to integrate. This argues for a face whose parts are driven from one shared internal state, so that they move as a gestalt (Principle 10), rather than per-feature controllers.
- **Methodological caution for S5 and S6.** Synchrony that is observed rather than manipulated is confounded with the partner's own state. The engine's contagion claims need a manipulated lesion (emotional pathway off) and surrogate controls, as evaluation.md already requires.
