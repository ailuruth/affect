# A Clockwork RNN (Koutník, Greff, Gomez & Schmidhuber)

Citation: J. Koutník, K. Greff, F. Gomez, J. Schmidhuber. "A Clockwork RNN." ICML 2014. arXiv:1402.3511.

Source read: arXiv v1 PDF, text-extracted, in full (sections 1–5; tables were partly garbled by extraction, so per-size numbers are not quoted).

## What it does
- **Architecture.** A simple RNN whose hidden layer is split into g modules, module i with clock period T_i (here exponential, T_i = 2^{i−1}). At step t only modules with t mod T_i = 0 update; the others hold their values. Recurrent weights are block-upper-triangular: slower modules feed faster ones, not the reverse. Backpropagation copies the error of inactive modules back in time.
- **Claim.** Slow modules "process, retain and output the long-term information … not being distracted by the high speed modules," fast modules handle local detail; fewer parameters and at least g/4 speed-up over an RNN of equal width.
- **Evidence.** Audio generation with no input (five 320-step music snippets; 100–1000 weights; 100 runs each): CW-RNN mean error 5.7× lower than the best LSTM, which "resembles a sliding average." TIMIT spoken-word classification (25 words, 175 sequences, periods 1…64): CW-RNN beats RNN and LSTM by 8–20 % on average at every parameter budget; more than 2× better than LSTM for the largest nets.
- **Stated options.** Other period series, learned periods, slowest period > 1 as a low-pass; the Sequence Chunker (Schmidhuber 1991–92) is the event-clocked predecessor.

## What it means for the design
1. **The design's "time scales from the tree" is a clockwork schedule.** Block j updates when a node of 2^j frames completes and holds between updates: Koutník's exponential clock, with a leak tied to the period. Coupling to both neighbours (z_{j−1}, z_{j+1}) differs from the paper's one-way slow-to-fast wiring, which is a design choice, not a mechanism.
2. **"The time constants are not tuned: they are the tree" is the clockwork property.** It gives scales by construction, but nothing about what a slow module learns: the paper's longest sequence is 320 steps; the design's slowest clock is 2^24 frames.

## Verdict
- [A Clockwork RNN (Koutník et al.)](koutnik-2014-clockwork-rnn.md) — 2014 — watch (prior art for the multiscale schedule) — hidden modules updating on exponential clocks (1, 2, 4, …) and holding between ticks gave 5.7× lower generation error than LSTM and 8–20 % better TIMIT word classification at equal parameters; the commutator design's dyadic block schedule is this clock driven by tree-node completions.
