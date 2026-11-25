# Bahrick & Watson 1985, "Detection of intermodal proprioceptive-visual contingency as a potential basis of self-perception in infancy" (Developmental Psychology 21(6):963-973, doi:10.1037/0012-1649.21.6.963)

Source read: the primary text, all 11 pages (abstract, introduction, Experiments 1-4, Table 1, Figure 2, general discussion), from the author copy formerly hosted by the FIU Infant Development Lab, retrieved from its Wayback Machine snapshot of 2025-01-01. The PDF is a scan with an embedded text layer; two-column text is interleaved in places, but every number below was checked against its sentence. The earlier version of this note (2026-11-25) was written from secondary accounts only (Gergely & Watson 1996; Rochat 1998) and was marked "watch"; this version replaces it.

## Claims
- Hypothesis (p. 964): "perfect contingency may serve to specify stimulation arising from the self, whereas imperfect contingency may specify stimulation arising from sources other than the self." A mirror or live video gives "essentially perfect contingent stimulation"; a mobile tied to the leg gives conjugate but not isomorphic stimulation; a mother's response is contingent but "not invariant with the infant's behavior. They are imperfect" (p. 972).
- Five-month-olds discriminate a live (perfectly contingent) video of their own legs from a noncontingent video, and they show it by looking MORE at the noncontingent display.
- The discrimination survives occlusion of the infant's direct view of its body (a bib and tray), so it rests on an intermodal proprioceptive-visual relation, not a visual-visual comparison of seen leg and screen.
- It survives removing all featural differences (live self vs a recording of self made minutes earlier in the same clothes), so it is contingency, not recognition of one's own legs.
- Three-month-olds show no group preference but significantly more extreme individual preferences than 5-month-olds: a bimodal split. The authors read this as a possible transition "from perfect contingency specifying self to imperfect contingency specifying other" (p. 973), and say the preference "may be reversed prior to the age of 3 months" (p. 972). They did not find 3-month-olds preferring the contingent display.
- Two interpretations are left open (p. 972): infants may detect the proprioceptive-visual invariant without perceiving it as "self", or detection may entail self-perception from the start (Gibson).

## Evidence with numbers
- Design common to all experiments: two TV screens side by side, 76 cm away, 46 cm apart; camera between them, inverted, so the legs appear feet-up as in the infant's own view, with right leg on the right (mirror-like). Yellow booties. 4-min test. Measure: proportion of total looking time to the noncontingent display; observer blind to sides; interobserver r = .99 on 34 of 89 infants.
- Yoked control: each infant's live image was recorded and became the noncontingent "peer" film for the next infant, so the amount of leg motion was matched across displays. Every peer film was itself recorded while that peer watched a live view of itself.
- Experiment 1 (n = 20, mean age 148 days; legs visible directly; live self vs peer): .65 to the noncontingent peer (SD .207), t(19) = 3.30, p < .005; 16 of 20 infants above .5. First minute .66, last minute .68; no trend, F(3,57) = 1.4.
- Experiment 2 (n = 20, mean 150 days; direct view occluded): .66 (SD .163), t(19) = 4.39, p < .001; 17 of 20. No trend, F(3,57) = 2.38.
- Experiment 3 (n = 20, mean 143 days; occluded; live self vs recording of self made just before, same clothes, after a 4-min recording session and ~5-min break): .69 (SD .196), t(19) = 4.34, p < .001; 18 of 20. No trend, F(3,57) = 0.09.
- Experiment 4 (n = 29, mean 99 days; occluded; live self vs peer): mean .47 (n.s.), SD .281 vs .163 for 5-month-olds in Exp. 2. Only 3 of 29 infants fell between .4 and .6; 14 were below .4 (preferring the contingent self) and 12 above .6. Moses test of extreme reactions: 3-month-olds more extreme than 5-month-olds, p < .005. Non-significant drift toward the noncontingent film within the session (.46 in min 1, .54 in min 4).
- No side or sex effects in any experiment.

## Resolution of the secondary-source disagreement
Rochat 1998 and Rochat & Morgan 1995 ("3-month-olds showed split preferences") report the paper correctly. Gergely & Watson 1996 ("the three-month-olds preferred to look at the perfectly contingent image") overstate it: about half of the 3-month-olds preferred the contingent view, the group did not, and the age reversal is the authors' conjecture. Do not cite this paper for "3-month-olds prefer perfect contingency".

## Mechanism
No equations. The detector is described as finding an amodal invariant shared by proprioception and vision of one's own motion: common timing, trajectory or direction, and intensity (p. 972). Self is the source of a perfect (invariant) relation; other people and objects produce imperfect relations. Contingency here is perfect in both of Watson's senses (every movement is shown, and every shown movement was made), at zero delay.

## What it implies for an engine that learns a partner model and its own self–other face map from contingencies in live interaction
- A self/other classifier by contingency level is supported, with one caveat: the evidence is a looking preference, not a classification. The engine can label a channel "self" when its relation to the engine's own motor output is near-perfect in both directions at a fixed short delay (its rendered face, its own voice in the microphone, its own avatar seen by the camera) and "other" when the relation is partial. This matters for the face map: the engine's own rendered face reaching its perception must be routed to the self-mirror, never learned as partner behaviour, and the partner's face must never be expected to hit perfect contingency.
- The yoked-control design is a ready-made test for the engine. Show the engine a replay of a partner recorded in another session (matched in motion amount) beside or instead of the live partner. A partner model that is truly learned from contingency must assign the yoked replay a contingency near zero. The critique's counterexample (C13: R = 9.5 learned from a partner who never responds) would fail this test; that is the point of running it.
- Intermodal, not intramodal: the infants matched felt motion to seen motion. The engine's analogue is efference copy (what it commanded) against perception (what it sees), not perception against perception. Contingency should be computed from the engine's motor commands, which it knows exactly, not from its own perceived output.
- The 5-month preference for the noncontingent display is a preference for the partner-like, imperfectly contingent source over the perfectly predictable self. An engine whose curiosity or attention is driven by learnable contingency should likewise lose interest in its own perfect echo once it is learned; looking time to the self-view did not decline over 4 min, so the preference was present from the first minute at 5 months.
- What this paper does not address: the infant was never the follower here. The displays did not respond to anything except the infant's own legs, so the confound in the critique (the agent's following of the partner learned as the partner's responsiveness) cannot arise in this paradigm. Identification in live dyads needs the lag and self-control methods of Watson 1997 and Beebe et al. 2016 (see those notes).

## License
APA journal article, all rights reserved. Author-hosted copy (now offline; archived).

## Runs on this Mac without a GPU?
n.a. (empirical study). The yoked-replay test runs on the engine with a recorded session and a webcam, CPU only.

## Verdict: adopt (perfect vs imperfect contingency as the self/other signature; yoked replay as the engine's partner-model test)
Primary read. Three experiments, n = 20 each, consistent effects (.65-.69) at 5 months. The 3-month result is a bimodal split, not a preference for self; the developmental "self first, then other" story is a conjecture.
