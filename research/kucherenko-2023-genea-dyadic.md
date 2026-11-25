# The GENEA Challenge 2023: monadic and dyadic gesture generation (Kucherenko, Nagy, Yoon, Woo, Nikolov, Tsakov, Henter; ICMI 2023)

Kucherenko, T., Nagy, R., Yoon, Y., Woo, J., Nikolov, T., Tsakov, M., Henter, G. E. "The GENEA Challenge 2023: A large-scale evaluation of gesture generation models in monadic and dyadic settings." ICMI '23. doi:10.1145/3577190.3616120; arXiv 2308.12646v1.

## What was read
- Full arXiv text: abstract; Sec. 1-2 (setup, data, baselines); Sec. 3 (human-likeness, results and significance); Sec. 4 (speech appropriateness: mismatching method, MAS, discussion); Sec. 5 (interlocutor appropriateness: stimulus construction, results, discussion); Sec. 6 (conclusion). I did not read the appendix tables of individual team descriptions.

## Claims
- 12 team submissions and 2 baselines (BM monadic, BD dyadic), with held-out motion capture (NA), evaluated in three crowdsourced studies: human-likeness, appropriateness for the agent's own speech, and appropriateness for the interlocutor. Every system received the interlocutor's speech and motion as input. Data: Talking With Hands dyadic mocap.
- Interlocutor study: 29 test segments (5.5-15 s, mean 10.4 s) chosen because "the main agent exhibited dyadic adaptations to the interlocutor, for example head nods", always with the interlocutor speaking. Each segment was paired with a version where only the interlocutor input was swapped for another interaction. Raters chose "In which of the two videos is the Main Agent's motion better suited for the interaction?" The mean appropriateness score (MAS) runs from −2 to 2, with 0 meaning chance.

## Evidence
- Abstract: "Appropriateness seems far from being solved, with most submissions performing in a narrow range slightly above chance, far behind natural motion. The effect of the interlocutor is even more subtle, with submitted systems at best performing barely above chance."
- Speech appropriateness (Table 3): NA 0.81 ± 0.06; best system SG 0.39 ± 0.07 ("a 62% preference for matched motion after splitting ties"); "most submissions are confined to a narrow range of MAS scores between 0.27 and 0.10".
- Interlocutor appropriateness (Table 3): NA 0.63 ± 0.08; BD 0.07 ± 0.06; BM −0.01 ± 0.06; submissions SA 0.09, SB 0.07, SC −0.03, SD 0.02, SE 0.05, SF 0.04, SG −0.09, SH −0.21, SI 0.04, SJ −0.03, SK −0.06, SL 0.07 (CIs ±0.05 to ±0.09). Only NA, BD, SA and SL are significantly above chance. SG and SH are significantly *below* chance.
- "a dyadic system being highly appropriate for agent speech does not necessarily imply high appropriateness for the interlocutor": SG ranks first for speech (0.39) and near last for the interlocutor (−0.09).
- Human raters can tell: NA's mismatch is detected "even for cases where the main agent is listening rather than speaking".
- The speech study "does not reveal to what extent the shortcomings seen are related to mistimed gesturing, or to failures to generate semantically relevant gesticulation." The authors add that "it is not clear if relatively non-specific gesture motion, as generally produced by the systems in the challenge, enhances human-agent communication."

## Failures documented
- **No partner-specificity.** Systems given the partner's speech and motion produce motion that raters cannot tell apart from motion generated for a different partner (MAS within ±0.1 of zero for 13 of 14 systems; humans 0.63).
- **Partner input can make behaviour worse than chance.** SH's motion was judged more appropriate when generated for the wrong interlocutor (−0.21).
- **Non-specific motion.** Even for the agent's own speech, motion is "relatively non-specific": human-like on the surface, weakly tied to what is said.
- The test is a perception study of body gesture, not face. It is the clearest published mismatch test of whether a dyadic generator responds to *this* partner.
