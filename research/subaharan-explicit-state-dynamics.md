# Controlling Long-Horizon Behavior in Language Model Agents with Explicit State Dynamics

Sukesh Subaharan (independent researcher), arXiv 2601.16087, January 2026. Read in full (about 4.5k words).

## Claims
- An LLM agent keeps a continuous **Valence-Arousal-Dominance (VAD)** state outside the model. A natural-language control prompt injects it each turn.
- Three update rules are compared:
  - stateless (the per-turn estimate only);
  - first-order (exponential smoothing; α=1 in the experiments);
  - second-order with momentum μ (0.8 or 0.95).
- Results:
  - The stateless agent never "recovers" after a hostile phase.
  - The first-order and μ=0.8 agents recover at about turn 14, when the scripted reconciliation starts.
  - μ=0.95 never recovers within 25 turns.
  - Hysteresis area grows with inertia: 4.36, then 6.85, then 21.19.
- "Affective state dynamics do not anticipate recovery but instead mediate the system's response to changes in interaction tone."

## Evidence
- The per-turn affect is **VADER lexicon sentiment**. The compound score stands in for valence, magnitude for arousal, and positive minus negative for dominance. It is computed over user input and model output.
- One fixed 25-turn scripted "philosophical" dialogue was used, with 5 seeds per condition. The LLM is not named in the text.
- Whether the injection works was checked only qualitatively, with one prompt under static VAD settings.
- Limitations the author states: a coarse lexicon estimator, one protocol and a short horizon.
- A limitation I noticed: the stateless condition is scored on the same smoothed metric, so "no recovery" and "zero hysteresis" partly hold by construction.

## License
- Paper: CC BY 4.0.
- Code: none linked.

## Runs on this Mac without a GPU?
Yes. VADER plus an API LLM is trivial, but there is nothing to run because no code is published.

## Verdict: reject
As a design it breaks three Principles:
- It uses a sentiment classifier on text (the text analogue of the emotion classifier Principle 1 forbids).
- VAD is **hand-named and set**, not read out of a learned state (Principle 2).
- The "state" is only prompt text, which is exactly the "modulates output like any contextual feature" pattern Goldenberg and Gross reject.

There are no body variables, no satiation and no wall-clock time.

## What it gives S1
- **A ready-made baseline to beat.** Our S1 ablation should include a "smoothed sentiment state" arm (VAD from text, injected as a prompt) beside "no state" and "full $h$ plus $b$". If the reunion behavior of full S1 cannot be distinguished from this arm, the latent state and body add nothing. That is a sharper falsifier than "no state" alone.
- **Two metrics to borrow, with fixes.** Recovery turn and hysteresis area are useful. Measure them in **wall-clock time across sessions**, not only in turns, and on behavior (bids, retrieval, length), not on the Bot's own sentiment.
- **Inertia warning for reunion.** Too much persistence blocks recovery: μ=0.95 never recovered. On reunion after silence, the decay of the distress component must be fast once contact resumes; Panksepp's offset on reunion is the basis. Otherwise the Bot stays "hurt" and sulks. Pre-register an upper bound, such as N turns, for return to baseline after a warm reunion.
