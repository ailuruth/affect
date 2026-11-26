# Learning stochastic differential equations using RNN with log signature features (Liao, Lyons, Yang, Ni)

Citation: S. Liao, T. Lyons, W. Yang, H. Ni. "Learning stochastic differential equations using RNN with log signature features." arXiv:1908.08286 (v2, 22 Sep 2019).

Source read: arXiv v2 PDF, text-extracted. Read in full: sections 1–6 and Appendix A (signature, log-signature, Chen's identity). Read in part: the remaining appendices (network configurations). Table entries were partly garbled; numbers quoted are from the text.

## What it does
- **Model.** A log-signature layer computes the depth-M log-signature of the input stream over each interval of a coarse partition (u_k); an RNN (or LSTM) runs on that sequence. Motivated by the log-ODE method for SDEs: the solution over an interval is approximated from the interval's log-signature. A universality theorem (4.1): Logsig-RNN approximates solutions of SDEs/CDEs under regularity conditions. PT-Logsig-RNN adds learnable linear path-transformation layers before the log-signature for high-dimensional inputs.
- **Evidence.** Synthetic SDE: best MSE among four methods on high-frequency, downsampled and 5 %-missing inputs; RNN length cut from 50k/1k to 4 steps, training time 50,930 s → 343 s. NTU RGB+D 120 (skeleton, 150 channels; includes two-person interaction classes): the log-signature layer adds 3.7 points over the LSTM baseline (cross-subject). ChaLearn 2013 gestures: 93.27 % with augmentation (state of the art at the time). More robust than an RNN when frames are zeroed.

## What it means for the design
1. **Interval log-signatures feeding a recurrent state are prior art (2019)**, as is their two-person use on skeleton streams. Morrill et al. 2021 cite this as the pairing the NRDE turns into a true log-ODE solve. The commutator core's "log-signature terms per node into a recurrent block" is a Logsig-RNN with the partner's level-1 terms deleted, at 24 partitions at once.

## Verdict
- [Logsig-RNN (Liao, Lyons, Yang & Ni)](liao-2019-logsig-rnn.md) — 2019 — watch (prior art for interval log-signatures into a recurrent state) — depth-M log-signatures over a coarse partition fed to an RNN, with a universality theorem from the log-ODE method; SDE training 50,930 s → 343 s, +3.7 points on NTU RGB+D 120 (two-person classes included), 93.27 % on ChaLearn 2013.
