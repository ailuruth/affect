# Initiative and conceptual regulation (synthesis)

Sources: bogels-2015-pregnant-pause.md, templeton-2022-fast-response-times-connection.md, liu-2021-emotional-support-conversation.md, deng-2023-proactive-dialogue-survey.md, ochsner-2012-reappraisal-imaging-review.md, lieberman-2011-affect-labeling-subjective.md, fan-2018-affect-labeling-minute-dynamics.md; with levinson-torreira-2015, stivers-2009 and knox-2025 already in the index. Written for two gaps in foundations/design-cayley-ledger.md ("Critiques of revision 2 and the answer"): (1) the agent never speaks first; (2) Claude's words reach only the face.

**Not reached** (blocked hosts; nothing here is cited beyond what the papers read say about them): Roberts, Francis & Morgan 2006; Burleson's person-centred comforting papers; Lieberman et al. 2007; Torre & Lieberman 2018. Lieberman et al. 2011 and Fan et al. 2018 stand in for the affect-labeling pair; Liu et al. 2021 for comforting; Bögels et al. 2015 for silence perception.

## 1. Initiative: what triggers it and when

**There are two silences, and the literature times only one.** After a turn that makes a reply relevant (a question, an offer), silence is read quickly: an answer at ~300 ms is unmarked, by ~700 ms a refusal or trouble is more likely than not, and at 1.7 s the questioner re-speaks with an easier version of the question (Bögels et al.). A *lapse*, where nobody owes a turn, is what a silently sad user produces, and none of these sources gives a human timing for initiative in a lapse. No proactive-dialogue method starts a turn in silence or from the system's own state either (Deng et al.); everything surveyed leads the content of a turn already owed, toward a system goal.

So the design has to compose initiative from parts, all in the body, with Claude asked only for words:

- **I1, pursuit after an unanswered agent turn.** No partner voice for about 1.5 s after an agent question → one softened re-offer that makes the hard answer easier ("Or just a long one?"). At most one per silence. To meet the timing, the six drafts made at the agent's turn include a pursuit variant, prepared before it is needed.
- **I2, a bid in a lapse, from the agent's own concern.** No turn owed, mutual silence, and the agent's concern C above an innate threshold θ_C → the body takes the floor: inhale, gaze to the user, a slight brow raise, then the words. One bid per silence episode, never learned from whether the user answered (Knox et al.), never scored on steering the user (the goal-driven objectives Deng et al. survey are the ones to avoid). The minimum lapse length is a design parameter; no source read fixes it.
- **Concern must reach θ_C in minutes, not at the end of the episode.** People build a negative state for about an hour before naming it (Fan et al.); a user who never names it is never addressed by an agent that waits for words. The critique measured a 10-min build in revision 2. A faster rise for C (a separate rise time of about 1 min, keeping the 10-min decay) is the obvious repair; it is my proposal, not a measured value.
- **Content of the bid: exploration first.** An open question or an observation about *this moment* ("You've gone quiet"), not advice and not a reinterpretation of the user's feelings, which Liu et al. removed even from trained human supporters. Naming longer-range inferences ("you've seemed sad since ten") is the privacy risk proactivity creates (Deng et al.).
- **Responsiveness decides whether initiative helps.** Users feel connected when their *partner* answers fast; slowing gaps 2× lowered judged connection causally (Templeton et al.), and a delayed answer is heard as trouble (Bögels et al.). R15 (onset waits 1–3 s for Claude) must go: the fast loop starts every agent turn within about 250–300 ms with a breath, particle or gaze, and words follow. Longer latencies come only from the agent's state, within a small range.

## 2. A route from Claude's words to the agent's state that never reads the state

**Revision 2 gives Claude only response modulation.** In Gross's process model, as Ochsner et al. set it out, an expression-only strategy leaves experience nearly unchanged and raises arousal; reappraisal and attention act on the appraisal itself and last. The face-only port P_Ω (zero DC, 15 s) is the expression-only class.

**The brain's proposed route keeps Claude blind.** Reappraisal is thought to change the representation that the appraisal system then "sees" (Ochsner et al.): no wire into the affect system, only a new input. For the agent: **its own realised utterance re-enters the slow block as a heard event, and the body appraises it.** Claude chooses words; it never sees a value, a label or an instruction to regulate. Affect labeling is the safest form of this, because it is:

- **an attenuator, not a valence push:** naming lowered distress for negative pictures and pleasure for positive ones (Lieberman et al. 2011);
- **small:** about 4–6% of the rating within a 5-s trial, against roughly twice that for instructed reappraisal;
- **larger for stronger states,** in three of four studies;
- **incidental:** it works while people talk for other reasons, and people predict it will hurt.

**Proposed rule (port P_name into the slow block's body inputs, beside P_Ω).** When an agent utterance ends, its innate lexical sign (the valence and arousal of its own words, computed inside S, so Check B2 needs only a line for this port) is compared with the sign of each body variable's deviation. On a match, Δb = −κ(b − b*), κ ≈ 0.05, at most once per agent utterance, applied to C and V.

- Bounded by construction: it never crosses the agent's own set point b*. The change per utterance is at most κ|b − b*|.
- Partner-dependence enters only through what Claude chose to say, and at most κ per utterance.
- Attenuate-only. The self-heard words do *not* also pass through the ordinary partner-word appraisal (R14). Elaborating on the sad topic is how people up-regulate (rumination), and increasing is the easier direction (Ochsner et al.).

**Time course.** At about two agent utterances per minute, κ = 0.05 adds a decay rate of ~0.1/min to C's own 0.1/min (τ = 10 min). That roughly halves concern's half-life while the agent names it, from about 7 to about 3.5 min. This is in line with the ~5-min half-life after people name a negative state (Fan et al., observational and confounded by naming at the peak). Reappraisal effects outlasting the episode by up to 30–40 min (Ochsner et al.) are carried by the body's own memory, not by the port.

**Three consequences for open findings.**
- *Comforting no longer reads as sender distress.* Comforting words are labeling words ("I understand how anxious you are"; Liu et al.), and on this route they lower the agent's concern. Appraising them as one's own distress is the lay error Lieberman et al.'s predictors made.
- *Naming the agent's pleasure would shorten it.* So the satiable positive drive the critique asks for must not depend on this route; its natural input is fast, contingent exchange (Templeton et al.).
- *Larger regulation is still open.* A reinterpretation or distancing draft that should regulate more than a label needs an appraisal of meaning inside S, which S lacks. Until then, larger effects can come only through draft selection (f_recv already simulates relief) plus the same contraction.

**Tests.**
- Align on the agent's naming utterances and compare concern trajectories with matched non-naming turns (Fan et al.'s method). Lesion P_name, and the difference must vanish.
- A mislabel ("I'm fine" while concerned) gives no contraction.
- A silently sad user gets exactly one exploration-type bid per lapse, after C crosses θ_C, and the agent answers the reply within 300 ms.
