# Rochat, Neisser & Marian 1998, "Are young infants sensitive to interpersonal contingency?"

Infant Behavior and Development 21(2):355-366. doi:10.1016/S0163-6383(98)90012-1.

Source read: the published PDF (12 pages), from the Wayback Machine copy (snapshot 2010-12-05) of the Emory lab site, read in full: abstract, introduction, Experiments 1 and 2, general discussion and references. The scan's text layer garbles some characters; numbers below were checked against the table layout. Murray & Trevarthen 1985 itself was not read; this paper's Table 1 reproduces its means, and that is the only primary-adjacent source we have for them (see murray-trevarthen-1985-double-video.md).

## Claims
- Murray & Trevarthen (M&T) 1985 is weaker than its citations suggest. Only 4 infants (6-12 weeks) were tested, some more than once (18 sessions). The Tape condition always followed a Live one; order was never controlled. M&T let the infant stay in Live "until an active interchange was reached" (Murray, personal communication), so Tape was compared with a peak. A natural decline from that peak would look like a Tape effect.
- Other failures before this paper: Muir & Hains 1993 found no Live-Tape difference with the infant's own mother at 2 or 5 months, but less smiling to Tape with a female stranger at 5 months. Bigelow, MacLean & MacDonald 1995 found attention declined linearly over time.
- Experiment 1 (double closed-circuit TV, built like M&T's, with eye contact through one-way mirrors; three 60-s intervals; first always Live and recorded for Tape; then Tape-Live or Live-Tape counterbalanced):
  - Replication (Live then Tape, N = 5): no coded behaviour differed (all p ≥ .06).
  - Order-controlled (intervals 2 and 3, N = 10, aged 2 m 12 d to 3 m 0 d): the only difference was smiling, and in the opposite direction to M&T: 0.59% Live vs 3.33% Tape (p < .03). Gaze to mother 75.84% vs 75.25% (p = .94).
  - No age trend between 10 and 12 weeks (Table 2, individual infants), against Murray's suggestion that the sensitivity peaks near 10 weeks.
- Experiment 2 (Live 45 s, then mother's still face up to 45 s, then Live or Tape 45 s; 21 infants after 10 exclusions; younger 8-15 weeks, M = 11.3, n = 10; older 17-25 weeks, M = 20.9, n = 11):
  - Gaze: main effect of interval F(2,34) = 9.937, p = .0004; much less gaze during the still face (Tukey p < .001). No effect of age or condition, no interactions: after the still face, Live and Tape did not differ.
  - Smiling: only half the infants smiled at all, so no statistics; same pattern by eye.
  - The still face shows the infants could see their mothers on the screen and were stressed; the stress did not make them more sensitive to Live vs Tape.
- Authors' reading: the null does not show that 2-month-olds lack sensitivity to interpersonal contingency. Video removes touch, distance regulation and gaze tracking, and mothers reported discomfort. "The double-TV method may just not be an effective way to demonstrate it."

## Evidence with numbers
M&T's means as reproduced in Table 1 (Live vs Tape, % of time): gaze to mother 89.3 vs 63.4 (p = .001); frowning 0.5 vs 25.4 (p = .0005); mouth closed 71.3 vs 36.6; eyebrows raised 38.3 vs 15.6; smiling 4.9 vs 1.0 (p = .1). The table header gives N = 8 for M&T while the text and figure legend say 4 infants; we cannot resolve this without the chapter. This paper's replication (N = 5): gaze 73.3 vs 79.8 (p = .28), frowning 0.9 vs 1.8. Coder reliability: Pearson r > .90 on all measures; Cohen's kappa averaged .66 (Exp. 1) and .82 (Exp. 2).

## Mechanism
None proposed; the paper is a replication test. The design point that matters is the confound it names: when the replay always comes second and the live period runs until the infant is engaged, a time-on-task decline is read as detection of non-contingency.

## What it implies for an engine that learns a partner model without confusing its own following with the partner's responsiveness
- The replay (double-video) test cuts exactly the arrow the engine must estimate, partner-depends-on-me, and leaves the partner's content, so the engine can still follow it. That makes it the right acceptance test for the partner model (see contingency-causal-synthesis.md). This paper says how to run it without fooling ourselves:
  - Counterbalance live and replay order, fix each interval's length in advance, and never let "engagement reached" decide when the replay starts.
  - Compare against a time-on-task control (live-live), because the engine's own adaptation and arousal also drift.
  - Use a still-face-like manipulation as a manipulation check: if the engine's estimate does not respond to the partner freezing, it cannot be expected to respond to the subtler replay.
- Infant evidence that a 2-month-old's gaze and affect detect the loss of partner contingency is weak and contested. Do not cite infant replay sensitivity at 2 months as established. The robust developmental evidence is the still face (gross loss of response) and, from about 3-5 months, self-produced contingency (bahrick-watson-1985, rochat-morgan-1995) and imitation vs reciprocity (striano-2005).
- A measured null on behaviour is not a null on detection. The engine can do better than an infant study: it can read its own internal partner-model estimate directly, rather than inferring detection from gaze and smiles.

## License
Ablex/Elsevier journal article, all rights reserved; archived author-site copy. No data released.

## Verdict: adopt (as the methodological caution for any live-vs-replay test; downgrades M&T 1985 as evidence)
Small samples (N = 5, 10, 21); the authors themselves leave open that the video setup, not the infants, failed.
