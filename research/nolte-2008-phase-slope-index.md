# Robustly estimating the flow direction of information in complex physical systems: the phase slope index (Nolte et al.)

Citation: G. Nolte, A. Ziehe, V. V. Nikulin, A. Schlögl, N. Krämer, T. Brismar, K.-R. Müller. "Robustly estimating the flow direction of information in complex physical systems." Physical Review Letters 100, 234101 (2008). arXiv:0712.2352.

Source read: arXiv v1 PDF, text-extracted, in full (the letter is four pages). It builds on Nolte et al. 2004, "Identifying true brain interaction from EEG data using the imaginary part of coherency" (Clin. Neurophysiol. 115:2292), which was not reachable (no open copy found); its idea is used here only as this letter restates it.

## What it does
- **Problem.** Granger causality reports significant but false directions when independent sources with non-trivial spectra are mixed into the channels (instantaneous, zero-lag mixing, e.g. EEG volume conduction).
- **The measure.** With complex coherency C_ij(f) = S_ij(f)/√(S_ii S_jj), the phase slope index is Ψ̃_ij = ℑ(Σ_{f∈F} C*_ij(f) C_ij(f + δf)) = Σ α(f)α(f+δf) sin(Φ(f+δf) − Φ(f)), a coherence-weighted average slope of the phase spectrum, normalised by a jackknife standard deviation. A pure delay τ has linear phase 2πfτ, so the slope's sign gives direction.
- **Properties claimed and shown.** Antisymmetric; zero whenever the imaginary part of coherency vanishes, hence "strictly insensitive to mixtures of arbitrary independent sources"; meaningful for non-linear phase spectra; frequency contributions weighted by coherence.
- **Evidence.** Random AR(5) systems with unidirectional flow plus randomly mixed independent noise (1,000 systems per noise level γ = 0…1): Granger's significant false detections approach 50 % as γ grows; PSI's worst case is 6 % (wide band, γ = 0.8), 3.5 % at finer frequency resolution. Resting EEG, 88 subjects: a front-to-back flow at the alpha peak in about 60 % of subjects; band-edge artefacts appear when the band covers only half the alpha peak.

## What it means for the design
1. **"Blind to zero-lag affine mixing, signed by direction, antisymmetric" is the defining property of imaginary coherency and PSI**, introduced (2004, 2008) for exactly the reason the design gives for its mask: a zero-lag copy (volume conduction there, mimicry here) must not count as interaction. The design's P1/P3 are this classical invariance on a Haar tree. The expected node commutator at each scale depends only on the quadrature (imaginary) cross-spectrum (derived and checked in research/foundations/sims/critique-cc-novelty, K1).
2. **PSI fixes what the per-scale commutator gets wrong.** Reading direction from the imaginary part at one band aliases once the delay exceeds half the band's period; reading it from the phase *slope* across frequencies does not, for a pure delay. The commutator array reads each scale's sign separately, so one follower at 0.6 s gives opposite signs at adjacent scales (K5).
3. **The coherence modulus |C| and its imaginary part are the "one 2×2 matrix serves knowing and bounding" pair.** The design's limiter (hypotenuse of trace and antisymmetric part) is a lag-scanned Haar coherence; its core input is a Haar imaginary coherency.

## Verdict
- [Phase slope index (Nolte et al.)](nolte-2008-phase-slope-index.md) — 2008 — adopt as prior art (and as a better direction estimator) — a coherence-weighted phase-slope measure that is antisymmetric and exactly insensitive to zero-lag mixtures of independent sources; 6 % worst-case false directions vs near 50 % for Granger under mixing; front-to-back alpha flow in 88 resting subjects; it shows the commutator's copy-blindness is imaginary-coherency invariance and that phase slope, not per-band sign, avoids lag aliasing.
