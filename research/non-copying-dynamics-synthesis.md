# How people avoid falling into copying: measurable signatures per channel and time scale

Question (from designs.md open gaps 1, 6 and 7): every design so far lets copying return by some indirect route. What do people actually do, over an extended exchange, that keeps them from settling into copying — at which time scales, and on which channels — stated as constraints a design can be tested against?

Sources read in full for this synthesis (one note each): Hale, Ward et al. 2020 (head pitch, wavelet coherence); Healey, Purver & Howes 2014 (syntax in two corpora); Paxton & Dale 2017 (head motion, argument vs friendly talk); Duran & Fusaroli 2017 (head motion and speech rate under disagreement and deception); Ravreby, Shilat & Yeshurun 2022 (mirror game, synchrony vs novelty); Galbusera et al. 2019 (whole-body synchrony and self-modulation); Golland et al. 2019 (zygomatic EMG synchrony, used as a calibration of copying). Related notes already in the index and used here: Fusaroli & Tylén 2016, Fusaroli et al. 2014, Riley et al. 2011, Richardson et al. 2015, Hasson & Frith 2016, Levitan et al. 2011/2012, Pardo 2006, Timmons et al. 2015, Hale & Hamilton 2016.

Tried but not readable from this session: Tiedens & Fragale 2003 (not open access), Wohltjen & Wheatley 2021 (PNAS; blocked), Riehle et al. 2017 (facial EMG synchrony; blocked). Nothing below cites them.

## The short answer

People do not avoid copying by coupling less. They couple at specific lags and bands, and in the same channel at other lags and bands they are **less similar than chance**. Which band is positive, which is negative, and how strong each is, depends on role (speaker or listener), on the episode (friendly, opposed, monitoring), and on the dyad's recent history. And there is a pressure against **repeating the joint pattern**, which grows within minutes even when the task asks for copying.

## Signatures, by time scale

| Time scale | Channel | Human signature | Source |
|---|---|---|---|
| 0.15–0.4 s movements (2.6–6.5 Hz) | head pitch, roll, yaw | coherence **below** a strict same-dyad, same-role surrogate; driven by the listener's fast nods while the partner speaks (94% precision) | Hale 2020 |
| ~0.5–0.6 s lag on 1–5 s movements | head pitch; zygomatic | positive coupling; head: constant delay 0.59 s, not constant phase; face: 0.48 s lag when context and smile agree | Hale 2020; Golland 2019 |
| ~1.75 s lag | zygomatic | slower coupling when the shared context runs against the smile | Golland 2019 |
| within ±5 s | head motion | turn-taking (recurrence higher off lag 0 than at it); at chance in friendly talk, **below** chance in argument | Paxton & Dale 2017 |
| within 1 s, one direction | head motion | the partner with the monitoring demand follows more; the other direction unchanged | Duran & Fusaroli 2017 |
| one turn (seconds) | syntax | other-repetition **below** chance at the next turn (−0.024, −0.011), at chance by 2–3 turns; words reused above chance meanwhile | Healey 2014 |
| ~4-s segments over 2 min | hand motion | novelty of the joint movement rises across the game; synchrony trades off against complexity (r = −0.27) and novelty (r = −0.32) | Ravreby 2022 |
| whole 5–8 min episode | speech rate; posture; own movement style | speech-rate recurrence lower in disagreement; lower-body coupling ~0.24 in every condition; partners converge in their **own** speed (r = 0.63) and internal coordination (r = 0.71) | Duran & Fusaroli 2017; Galbusera 2019 |
| episode, ~10 min | zygomatic | coupling in the second clip, not the first, predicts later affiliation (ρ = 0.74 vs −0.04) | Golland 2019 |

Not covered by anything read: hours, days, a long relationship. That gap remains (as in the mimicry synthesis).

## Constraints a design must satisfy

Each is stated as a measurable property of the agent–partner pair, with the surrogate that makes it testable. None uses emotion labels.

**C1. Band-signed coupling within one channel.** For head motion, the agent's coherence with the partner must be above a matched surrogate at 0.2–1.1 Hz and **below** it at 2.6–6.5 Hz in the listening role. Surrogate: the same agent and partner, same roles, different exchange (Hale's within-dyad pseudo-trials). A model that ignores the partner at high frequency scores at chance and fails.

**C2. Short-lag divergence that relaxes to independence.** On form-level features of each exchange (the configuration of the agent's facial or vocal response, not its referent), similarity to the partner's preceding exchange must be below a random-partner surrogate at lag 1 and at chance by lag 3. A stable negative correlation fails (it is copying with a minus sign and is predictable). Self-repetition of form must also not exceed chance.

**C3. Shared referent, different form.** Content uptake (what the response is about, where it is aimed) must be above chance while form, net of content, is below chance (Healey's lexical-covariate logic). This needs at least two coupled components with opposite signs; one partner→self map on the whole expression vector cannot do it.

**C4. Role sets the sign.** The same partner signal (e.g. voice activity) must drive a non-matching output in the listening role (fast, small head motion in a band the partner is not using) and not in the speaking role. Leading and following must be asymmetric and set by the agent's role in the episode (Duran: only one lag direction moved).

**C5. Episode sets the net level, including below chance.** Over an episode, net coupling against a phase-randomised surrogate must be able to sit at chance (friendly) and **below** chance (opposed), and the dominant shape must be alternation (U-shaped recurrence profile), not lag-0 synchrony. Reducing a gain toward zero cannot reach below chance.

**C6. No single quantity runs coupling.** Disagreement lowers coupling; disagreement plus a monitoring demand raises it above everything else (Duran). Relational stance and attentional demand must act on coupling separately and be able to push in opposite directions. Any design in which both are read off one scalar fails this test — this is the human evidence behind open gap 1.

**C7. Anti-repetition of the joint trajectory, growing over minutes.** The pair's joint movement must show rising novelty across a 2-min exchange even under maximal pressure to copy, and the agent's contribution must trade synchrony for variety (r ≈ −0.3 between them across partners) while keeping both above surrogate. Mechanically this is a drive whose argument is the **dyad's recent joint history**, satiable by variation — a candidate concrete answer to "satiable drives" in open gap 7, and one that stops copying from being an attracting state because a copying regime is exactly the one that repeats the joint pattern.

**C8. Face coupling is mostly common cause.** When agent and partner share an event, most face synchrony must come from both responding to the event; the partner-specific excess should be about a third of the total (0.44 vs 0.30), absent with no shared driver, and slower (~1.75 s vs ~0.5 s) when the event and the partner's expression disagree. Test: the agent's coupling to a live partner vs to a recording of another partner exposed to the same events.

**C9. Converge in parameters, not in output.** Slow convergence of the agent's own movement statistics (speed, variability, how its channels co-vary) toward the partner's over an episode is human (r = 0.63–0.71) and permitted; it must not translate into moment-to-moment matching of the output. Some slow postural coupling may be context-invariant (Duran's lower body), which is harmless.

**C10. Coupling must not disable self-restoration.** High coupling over minutes went with weaker self-reported modulation (Galbusera; weak evidence, p = .03). The agent's return toward its own set point must be a separate force that coupling cannot switch off, or coupling must itself be pulled down when self-restoration has been weak for a while. Evidence level: watch.

## What this means for the five designs (inference, not a claim of the sources)

- The copy routes the critiques keep finding are routes by which a **positive** partner→self term wins at all lags and bands. The human data have **negative** terms at specific lags (C1, C2, C5) that a design must generate, not merely permit. A cheap audit for any design: compute its coupling spectrum and lagged form-similarity against the surrogates above; if no band or lag is below chance in any episode, copying is not excluded, only weakened.
- C7 is the most design-relevant new item. It places the anti-copy pressure on the **history of the pair**, not on the partner or the self alone, which no current design has. It is compatible with the relationship-as-learned-structure in the mimicry and social-appraisal syntheses: the partner-specific part sets the initial novelty level and its growth rate.
- C3 and C8 together suggest the matching that does occur should run through a shared referent (the event, the topic), which is where the social-appraisal route already puts it.

## What remains open

- **Long time scales.** Nothing here beyond ~10 min; no study of how a couple's divergence signatures evolve over months. Pardo 2006 (convergence that outlasts the conversation) and Timmons 2015 (partner effect flipping from anti-phase to in-phase with influence) are the closest notes in the index.
- **Faces in conversation.** No face study read here measured below-chance coupling; the face evidence (Golland) is co-viewing, side by side. Whether facial actions show Hale's band split in face-to-face talk is untested by anything read. Riehle et al. 2017 (facial EMG, windowed cross-lagged correlation) is the next source to get.
- **Dominance complementarity** (Tiedens & Fragale 2003) could not be read; the complementarity-by-role evidence here is listener/speaker and follower/leader, not dominance.
- **Measurement disagreement.** Head-synchrony findings depend on sensor, signal (velocity vs acceleration vs motion energy), linear vs recurrence analysis and baseline (Paxton & Dale list five differences). Every constraint above should be tested with the source study's own measure and surrogate.
- Samples are small (21–46 dyads for the live-conversation studies; 26 for the face study), mostly students and strangers.
