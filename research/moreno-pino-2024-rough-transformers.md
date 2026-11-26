# Rough Transformers: lightweight continuous-time sequence modelling with multi-view signatures (Moreno-Pino, Arroyo, Waldon, Dong & Cartea)

Citation: F. Moreno-Pino, Á. Arroyo, H. Waldon, X. Dong, Á. Cartea. "Rough Transformers: Lightweight and Continuous Time Series Modelling through Signature Patching." NeurIPS 2024. arXiv:2405.20799 (v3, 11 Jan 2025).

Source read: arXiv v3 PDF, text-extracted. Read in full: sections 1–5 (problem, Transformers and signatures, multi-view signature transform and attention, efficiency, irregular sampling, spatial processing, experiments: frequency classification, BIDMC heart rate, five long UEA datasets, timing, irregular sampling). Appendices read only where cited by the main text.

## What it does
- **Multi-view signature.** For each of L̄ ≪ L time points t_k: M(X)_k = (S(X̃)_{0,t_k}, S(X̃)_{t_{k−1},t_k}), a global and a local truncated signature of the piecewise-linear interpolation. Attention runs over these L̄ tokens instead of L raw samples; queries, keys and values are linear maps of the signatures.
- **Claims.** Reparametrisation invariance gives robustness to irregular sampling (Proposition 3.1); cross-channel signature terms give "spatial processing" without a predefined channel graph; for many channels, use log-signatures, univariate time-augmented signatures, or randomised signatures.
- **Evidence.** BIDMC heart rate: RFormer improves the vanilla Transformer by 67 % in RMSE. Long UEA classification: matches or slightly beats NCDE/NRDE/log-CDE and SSM baselines. Speed-ups of 1.4× to 26.11× over standard attention, more over ODE-solver models; scales to L = 250k; small drop under random point removal.

## What it means for the design
1. **Signature features at several window scales combined with attention-style selection already exist.** The design's need-conditioned top-8 selection over (channel, scale) cells is attention over signature patches with a sparse top-k, as here plus Shazeer's fixed k.
2. Nothing here restricts which signature terms of which party may drive a state; that restriction is the design's only distinctive element, and it is a design rule (see the critique).

## Verdict
- [Rough Transformers (Moreno-Pino et al.)](moreno-pino-2024-rough-transformers.md) — 2024 — watch (prior art: multiscale signatures under attention) — attention over global and local signature patches cuts sequence length, is robust to irregular sampling, improves BIDMC heart-rate RMSE by 67 % over a Transformer and trains 1.4–26× faster; the commutator design's selection over (channel, scale) signature cells is the same pattern with a sparse top-k.
