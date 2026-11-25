# Do Large Language Models Have Emotions? (critique of Sofroniew et al.)

Goldenberg (Harvard) and Gross (Stanford), arXiv 2606.14742, June 2026. Read in full (an 8-page commentary).

## Claims
- Emotions have two functions. The first is context-sensitive interpretation of situations (appraisal). The second is **reorganization of processing across systems**: attention narrows or broadens, decisions speed up, motivation and action tendencies shift, and memory encoding is biased.
- On function 1, the support is partial. Anthropic's consistent, discrete emotion vectors conflict with neuroscience showing variable, distributed and context-dependent emotion signatures (Lindquist et al. 2012 meta-analysis; Satpute). "A consistent fear vector looks more like a learned semantic representation than a flexible emotional process."
- On function 2, the evidence is mixed. Each forward pass is fixed in structure: "no narrowing of attention, no acceleration of certain processing pathways, no sustained shift in how incoming information is weighted." The vectors modulate output like any other contextual feature.
- Emotions have a characteristic time course: "more sustained than a reflex, more bounded than a mood". They persist through an episode and fade when the eliciting situation resolves.
- Bodies and faces are not required. Collective emotions show that the substrate can be distributed. What is required is "sustained, multi-system reorganization of processing, not merely a shift in the probability of the next token".

## Evidence
A conceptual argument from appraisal theory and affective neuroscience. It contains no new data, models or experiments. It relies only on the published Anthropic results.

## License
- Paper: CC BY 4.0.
- Code: none.

## Runs on this Mac without a GPU?
n.a.

## Verdict: adopt
Adopted as an **evaluation criterion**, not as an architecture. Its test of "reorganizes processing, with an episode-length time course" fits Principles 2 and 5: the latent state must change behavior and must be ablatable. It also explains why a state that only adds tone words to a prompt (see subaharan-explicit-state-dynamics.md) would not count.

## What it gives S1
- **Make $h_t$ and $b_t$ reorganize processing, not only wording.** In S1, the coupling should reach at least two non-lexical channels per turn. Candidates:
  - retrieval breadth or recency weighting over memory (attention);
  - reply latency and length budget (speed);
  - whether the Bot initiates, asks or withdraws (action tendency).
  An ablation that removes $h$ should then change these measurable quantities, not only sentiment.
- **Time course as a test.** After a reunion, the state should rise, persist for a bounded episode and decay as the situation resolves. A step that never decays is a mood or a bug. A one-turn blip is a reflex. Write the expected half-life into the ablation prediction.
- **Variability as a feature.** The same "silence" event should yield different $h$ trajectories depending on history and body. A fixed per-event signature would reproduce the classical-view error the paper criticises. This matches Barrett (barrett-constructed-emotion.md).
