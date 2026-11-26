# Ho, Foulsham & Kingstone 2015, "Speaking and listening with the eyes: gaze signaling during dyadic interactions" (PLOS ONE 10(8):e0136905, doi:10.1371/journal.pone.0136905)

Source read: full text on journals.plos.org: abstract, introduction, method, results, discussion, limitations. The S1 dataset (start/stop times) was not opened.

## Claims
- With both partners eye-tracked face to face, the classic Kendon / Duncan & Fiske turn pattern holds when timed precisely: a speaker ends a turn by looking at the partner, the partner starts speaking about 400 ms after that look begins, and the new speaker starts with gaze averted, looking back at the partner about 700 ms into the turn.
- Gaze and speech are inversely related within a person: talking goes with looking away, listening with looking at.
- In a fast, back-and-forth exchange the two partners' gaze is anti-correlated: when one looks, the other tends to look away.

## Evidence with numbers
- 40 students in 20 dyads (19 analysed; 37–38 participants per analysis), Dikablis mobile eye trackers at 25 fps, manual coding of every gaze on/off the partner's face and every speech on/off. Two structured games: 20 Questions (slow, long pauses) and a Heads Up / Taboo variant (fast, 3-minute rounds).
- Gaps: between speakers 2208 ms (20 Questions) vs 1430 ms (Heads Up), t(18) = 3.94; between one person's gaze ending and the other's starting 1574 vs 2272 ms.
- Partner-to-partner gaze correlation (zero lag): r = −.05 (20 Questions, n.s.) and **r = −.18 (Heads Up, p < .0001)**. Talking: r = .08 n.s. and r = −.26.
- Own gaze vs partner's talking (max cross-correlation within ±2 s): r = .47 and .53; **partner speech lags the gaze onset by 423 ms (SD 388) and 432 ms (SD 557)**, no difference between games.
- Own gaze vs own talking: r = .37 and .40; **gaze at the partner follows the start of one's own talk by 780 ms (SD 923) and 736 ms (SD 724)**.
- Background they cite: listeners look at speakers more and longer, speakers look more often but briefly; reported ranges 20–65% (speaker looking) and 30–80% (listener looking), with large individual variation.
- Stated limits: structured games with high cognitive load (initial aversion may partly be load), 25-fps tracking, eye trackers worn on the face; no emotional content.

## What it implies for the design
- In human conversation a direct look is a turn signal with a short life: it hands the floor over and is answered within about half a second. A look that is held without a turn change is not a stable human state; the human pattern dissolves it either by the partner taking the turn or by one partner looking away.
- When the agent takes a turn (any utterance, including a short comfort), its gaze should leave the partner's face at onset and return roughly 0.7 s in. That alone breaks a mutual hold at every agent turn, independently of what the face is doing, and it is driven by the agent's own speech timing, not by the partner's face.
- In lively exchange the partners' gaze runs in anti-phase (r ≈ −.18). An agent whose gaze follows the partner's gaze in phase (looking whenever looked at) builds exactly the mutual hold the design fails on. The coupling sign for gaze should be weakly negative or zero, not positive.
- Not covered: listener facial displays, distress or disclosure. These are timing and gaze rules for neutral task talk between students.

## License
CC BY 4.0.

## Runs on this Mac without a GPU?
n.a. (empirical study). The lagged cross-correlation on binary gaze/speech series is cheap and could be the test metric for the agent's own gaze.

## Verdict: adopt (gaze timing at turns: look to yield, partner speaks ~400 ms later; avert at own turn onset, return ~700 ms in; partners' gaze anti-correlated in fast exchange)
Structured games, students, no emotional talk; 19 dyads.
