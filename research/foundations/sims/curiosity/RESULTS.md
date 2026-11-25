# Shared curiosity toy: results (out/lp.json)

| Agent | L1 | L2 | Noise N | Boring B |
|---|---|---|---|---|
| Learning-progress (LP) body variable: visits | 307 | 253 | 19 | 21 |
| Predictability set point: share of steps | — | — | **0.395** | — |
| Surprisal minimizer: share of steps | — | — | — | **1.00** |

- **LP-1 confirmed.** In the 583 steps before both learnable channels were learned, the LP agent chose N in 3.3% and B in 3.6% of steps. It escapes both the noisy TV and the dark room.
- **LP-2 confirmed.** Final errors were L1 0.050 and L2 0.090, both under 0.1. L1 first held a majority at step 0, and L2 at step 371.
- **LP-3 refuted as written.** Both channels were learned only at step 583, which left 17 steps, all on L2, whose error was still falling slightly. "Neither N nor B > 80%" holds, but L2 took 100% of those steps. The prediction was meant to show no persistent preference after learning ends. The window was too short to test that. It needs a longer run, pre-registered anew.
- **LP-4 confirmed.** The predictability set-point agent chose N in 39.5% of steps, and the surprisal minimizer chose B in 100%.

**Not predicted.** The LP agent kept returning to the already-learned L1: 307 visits, about 200 of them after L1 was learned. That follows from the two-sided set point. When recent learning progress is *above* its set point, the agent prefers a channel with *low* progress, the "rest" side of the drive. A learned channel serves as rest. Whether a two-sided learning-progress drive (with rest) is wanted, rather than a one-sided one, is a design question this toy raises.

**Reading.** Learning progress as an innate body variable with a set point gives curiosity that:
- is satiable (Principle 6);
- avoids the dark room;
- avoids the noisy TV.

It is proposed as a shared innate body variable for all three candidates, replacing the predictability set point as the source of curiosity. Each candidate must still state it in its own formalism, and the sources it borrows from (IAC; Schmidhuber) are being read in their primaries.

## Sources, read 2026-11-25 (research/oudeyer-kaplan-hafner-2007-iac.md and related notes)

- **The measure is Oudeyer, Kaplan & Hafner's IAC.** Learning progress is a windowed comparison of errors: "D(t+1) = ⟨e_n(t+1)⟩ − ⟨e_n(t+1−τ)⟩", "L(t+1) = −D(t+1)". It **must be computed per region**: over time alone, it rewards switching from a hard activity to an easy one. This toy computes it per channel, as required.
- **Learning progress is the standard answer to both traps:**
  - prediction-error curiosity is "stuck by white noise" (IAC). In Burda et al. 2019, a TV in the maze took performance from about 0.8–0.95 to about 0–0.05, read off their Fig. 6;
  - surprise minimization avoids the dark room only through priors evolution built in (Friston, Thornton & Clark 2012).
- **No source treats learning progress as satiable or as having a set point.**
  - IAC says learning progress "must be kept maximal".
  - Schmidhuber 2010 says the reward "eventually vanishes" where nothing new can be learnt, citing Berlyne-era "nonhomeostatic drives".
  - **The set point, and with it the "rest" behavior on an already-learned channel, is this project's own construction, imposed by Principle 6.** It has no source.
- **No animal or human evidence for preferring learnable over unlearnable stimuli** was found in what could be read. Gottlieb & Oudeyer 2018 was read in abstract only. The leads not yet read are Baranes, Oudeyer & Gottlieb 2014, and the 2013 Trends in Cognitive Sciences review.

**Correction (2026-11-25, thermo VERIFICATION.md).** LP-3 is **inconclusive**, not refuted: with only 17 post-learning steps, the test could not discriminate. This label does not favor the candidate. It records that the toy did not test the claim.
