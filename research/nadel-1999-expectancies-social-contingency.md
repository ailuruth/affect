# Nadel, Carchon, Kervella, Marcelli & Réserbat-Plantey 1999, "Expectancies for social contingency in 2-month-olds"

Developmental Science 2(2):164-173, doi:10.1111/1467-7687.00065.

Source read: the abstract only (Crossref and OpenAlex metadata), plus descriptions of the study in three primaries that were read in full or in part: Striano, Henning & Stahl 2005 (Dev Sci 8:509-518, read in full; see striano-2005-social-contingency-1-3-months.md), Henning & Striano 2004 (two-page epigenetic-robotics abstract, read in full), and Soussignan et al. 2006 and Stormark & Braarud 2006 (abstracts only). The full text is listed as free ("bronze") at Wiley, but automated access was refused, so methods, period durations, per-behaviour statistics and the coding scheme were NOT read. The sample size of ten comes from the abstract ("seven of the ten babies").

## Claims (from the abstract)
- Aim: test Murray & Trevarthen's (1985) claim that 6- to 12-week-olds detect contingency, against the objection that infants simply get fussier over time.
- Design: live–replay–live over closed-circuit TV (double video), with "a seamless shift from the initially live interaction period to a replay period of good maternal behavior", then "a seamless shift back to a subsequent live interaction."
- Result: "Two-month-old smiling and gaze decreased while frowning and mouth closures increased during the replay period relative to the initial live interaction period, replicating Murray and Trevarthen's results."
- Against fatigue: "seven of the ten babies increased their positive behaviors and decreased negative behaviors during the second live interaction period, and there was a significant increase in their visual attention to their mothers, thus suggesting a renewed interest in the previously noncontingent partner."

## Evidence with numbers
- n = 10 two-month-olds (Striano et al. 2005 call them 9-week-olds). 7 of 10 recovered in the second live period; gaze to the mother rose significantly from replay to second live. No effect sizes or test statistics were read.
- Context from later primaries:
  - Rochat, Neisser & Marian 1998 failed to replicate the replay effect at 2 months (as reported by Striano et al. 2005; not read).
  - Bigelow & DeCoste 2003 (abstract): contingency and carry-over effects at 4 and 6 months, at 2 months only a hint in effect sizes for attention.
  - Soussignan et al. 2006 (abstract; same Paris group): with three 30-s episodes, the live–replay–live group grimaced more than a live-only control only in the second period. Infants who smiled in the first live episode reacted most negatively to replay. In the control group the third period showed more grimacing and less gaze, which the authors attribute to fatigue.
  - Stormark & Braarud 2006 (abstract): 2- to 4-month-olds looked more at the mother in live than in replay, but only infants low in negative affect.

## Mechanism
None is modelled. The inferred mechanism is that the infant has an expectancy of contingent response, which builds within the first live minutes. When the replay breaks contingency while keeping the form and positive content of maternal behaviour ("good maternal behavior"), the infant's positive acts drop and negative ones rise. The ABA design separates a contingency effect (reversible) from fatigue (monotone).

## What it implies for an engine learning a partner model and its self–other face map from live contingency
- A seamless replay is the cleanest test that the engine's learned partner model encodes responsiveness and not form. Swap the live partner stream for a recorded segment of the same partner, with the same expressions and the same statistics, and switch back (A-B-A). An engine whose "partner responds to me" estimate does not fall during B, and recover in the second A, has learned co-occurrence or its own following, not contingency. This is the infant-validated version of the critic's never-responding-partner counterexample (C13). It needs no new data: replay an earlier stretch of the same session.
- The reversal in the second A is the key control. Without it, any drop is confounded with drift, habituation or the engine's own state trend (the "fussiness" objection). For a learning engine, learned parameters should not be updated during the probe, or the B period will itself retrain the model.
- The effect at 2 months is fragile across labs (one replication with n = 10, one failure, effect-size hints only). By 3-4 months it is robust. Two lessons follow for the engine. First, detecting that a partner is contingent needs enough interaction history to form an expectancy. Second, the response depends on the agent's own state (only positively engaged or low-distress infants show it, per Soussignan and Stormark). An engine's contingency estimate should be gated by its own engagement, or at least read with that caveat.
- Mirror-image probe for the confound: replay the agent's own earlier outputs to the partner while the agent keeps sensing the live partner (Murray & Trevarthen 1986's direction; see murray-trevarthen-1985-double-video.md). If the partner's measured contingency on the agent persists when the agent's output is not reaching the partner, the estimate is an artefact of the agent's following.

## License
Wiley journal article, all rights reserved (listed as free to read at the publisher).

## Runs on this Mac without a GPU?
n.a. (empirical study). The replay probe needs only a buffer of the session's partner stream.

## Verdict: watch (primary text unread; abstract and secondary accounts only)
The design (seamless live–replay–live) is what the engine should copy. The 2-month result itself is small (n = 10) and contested; do not cite it as established without the full text.
