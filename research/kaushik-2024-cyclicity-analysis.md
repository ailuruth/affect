# Cyclicity analysis of the Ornstein–Uhlenbeck process (Kaushik; Baryshnikov's cyclicity analysis)

Citation: V. Kaushik. "Cyclicity Analysis of the Ornstein-Uhlenbeck Process." PhD dissertation, University of Illinois Urbana-Champaign, 2024 (director Y. Baryshnikov). arXiv:2409.12102. It restates cyclicity analysis as introduced by Baryshnikov & Schlafly, "Cyclicity in multivariate time series and applications to functional MRI data," IEEE CDC 2016, pp. 1625–1630 (not reachable: the Illinois repository and IEEE were blocked; used here only through the dissertation's restatement).

Source read: arXiv PDF, text-extracted. Read in full: chapter 1 (leader–follower questions, periodic signals and cross-correlation, the chain-of-offsets model, the reparametrisation failure of cross-correlation, cyclic signals, cyclicity analysis and the lead matrix, its spectral properties). Chapters 3–5 (OU process, explicit lead matrices, simulations) read only for their statements.

## What it does
- **Problem.** Which component leads which, and in what cyclic order, when components trace a common signal up to scale and time shift (chain-of-offsets model, COOM), or a time-warped ("cyclic") version of it.
- **Why not cross-correlation.** Its arg-max lag is not invariant to time reparametrisation; a worked example flips the inferred leader under a monotone warp.
- **The lead matrix.** A_mn = ½∫(x_m dx_n − x_n dx_m): the oriented (Lévy) area of each pair, closed by the chord. "We heuristically interpret the oriented area as an indicator of the lead-lag relationship … x_m leads x_n if A_mn > 0." A is skew-symmetric, so its eigenvalues are 0 or ± iλ; under COOM the phases of the leading eigenvector's components recover the cyclic order of the offsets. Applied to fMRI (Baryshnikov & Schlafly 2016) and studied here for a cyclic OU network, where the leading eigenvector reflects the sensor ring's structure in some regimes and not others.

## What it means for the design
1. **The antisymmetric matrix of pairwise Lévy areas, read as "who leads whom", reparametrisation-invariant and zero for synchronous pairs, is an established analysis tool** (fMRI, sensor networks). The design's same-channel areas between agent and partner are entries of such a matrix restricted to (own_k, partner_k) pairs.
2. **COOM's own premise shows the aliasing.** Order is recovered only as a cyclic order modulo the period: a lag past half a period reads as the opposite lead. This is the design's quarter-lag maximum (C3) seen from the analysis side, and it applies to every rhythmic channel the design names (nods, laugh rhythm, voice rate).

## Verdict
- [Cyclicity analysis (Kaushik 2024, restating Baryshnikov & Schlafly 2016)](kaushik-2024-cyclicity-analysis.md) — 2024 — watch (prior art for the lead matrix) — the skew-symmetric matrix of pairwise oriented areas is a reparametrisation-invariant lead–lag analysis already applied to fMRI; its spectrum recovers cyclic order only modulo the period, so lead direction aliases past a half-period lag; the commutator array is a per-channel, per-scale block of such a matrix.
