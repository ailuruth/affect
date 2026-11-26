# Lead-lag detection and network clustering for multivariate time series (Bennett, Cucuringu & Reinert)

Citation: S. Bennett, M. Cucuringu, G. Reinert. "Lead-lag detection and network clustering for multivariate time series with an application to the US equity market." arXiv:2201.08283 (v1, 20 Jan 2022).

Source read: arXiv v1 PDF, text-extracted. Read in full: sections 1–4 (problem, related work, pairwise lead–lag metrics, directed-network clustering, ranking, complexity, synthetic experiments). Sections 5–6 (US equities, trading signal) and the appendix read only for their claims, not their tables.

## What it does
- **Pairwise lead–lag metrics.** (i) Functionals of a sample cross-correlation function (Pearson, Kendall, distance correlation, mutual information): ccf-lag1 = ccf(1) − ccf(−1), and ccf-auc, a signed normalised area over lags 1…L. (ii) **The signature metric** (after Levin et al. 2016): over a window, the difference of the two level-2 cross terms of the log-price path, i.e. twice the Lévy area. All metrics are antisymmetric, S_ij = −S_ji.
- **Stated limitation of the signature metric (section 3.1.2):** "it is not able to tell the difference between 1. i → j with negative association, 2. i ← j with positive association." Also: its magnitude grows with volatility, so prices should be normalised first.
- **Network step.** A = max(S, 0) as a directed weighted graph; Hermitian random-walk spectral clustering finds cluster pairs with high cut imbalance (leaders vs laggers).
- **Synthetic results** (p = 100 series, T = 250, lagged-factor models with 10 or 20 lag clusters, 48 repeats). Linear factor: ccf-auc and signature metrics best; accuracy falls to chance around σ = 4. Cosine (non-monotone) factor: all methods reach chance near σ = 0.5, and "the ccf-lag1 and signature methods perform poorly; this is not a surprise since this method cannot deal with negative associations." Hermitian RW and DI-SIM clustering recover the true clusters (ARI ≈ 1) at low noise.

## What it means for the design
1. **The commutator ρ is this signature metric, windowed and normalised.** Its "sign says who led" claim inherits the confound stated here: a partner who counters the agent (opposite direction) reads as the agent following him. The design allows and expects countering (m_k down to −γ_k; rivals), so the confound is not hypothetical. Checked numerically in research/foundations/sims/critique-cc-novelty (K2: +0.22 vs −0.22 swap exactly with the sign of gain).
2. **A lead matrix over channels is an established object** (here over stocks); the design's 33 × 24 array is a per-channel, per-scale version of it.

## Verdict
- [Lead-lag detection and network clustering (Bennett, Cucuringu & Reinert)](bennett-2022-lead-lag-network-clustering.md) — 2022 — watch (prior art; names the commutator's sign confound) — the Lévy-area lead–lag metric is used alongside cross-correlation functionals to build directed lead–lag networks; it cannot tell "i leads j, negatively" from "j leads i, positively" and fails on non-monotone dependence (chance at σ ≈ 0.5 in the cosine model); Hermitian clustering recovers leader/lagger clusters (ARI ≈ 1 at low noise).
