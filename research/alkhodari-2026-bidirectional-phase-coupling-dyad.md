# Continuous bidirectional coupling of heart rate variability and emotions in dyadic speaker–listener dynamics (Alkhodari et al.)

Citation: M. Alkhodari, I. Ziogas, J. Singh, P. Grigolini, G. W. Muschert, F. Kusmartsev, H. F. Jelinek. "Continuous bidirectional coupling of heart rate variability and emotions in dyad speaker-listener dynamics reveals unique interpersonal synchronization." Frontiers in Systems Neuroscience, 2026. doi:10.3389/fnsys.2026.1802891.

Source read: publisher PDF, text-extracted. Read in full: abstract, introduction, methods (K-EmoCon data, audio and PPG preprocessing, HRV and entropy features, the coupling index, statistics), the coupling results, discussion and limitations. Figures and per-feature heatmaps not checked one by one.

## What it does
- **Data.** K-EmoCon: 32 people in 16 dyads, about 10-min structured debates on a contested topic; Empatica E4 PPG at 64 Hz → RR intervals; speech timing; self, partner and external valence/arousal ratings.
- **The coupling index (after Jelinek & Khandoker 2020; Jelinek et al. 2025).** Instantaneous phases of the two band-limited RR series by the Hilbert transform; a phase-locking degree λ from the circular mean of the phase difference; Bi λ = λ × (an arctangent of the mean phase difference's imaginary over real parts), in [−1, 1]. Magnitude = locking strength; sign = who leads (positive: participant 1, speaker-leading in that ordering). The authors keep the complex vector because taking only the cosine "can spuriously inflate synchrony estimates and remove directional information," and cite the imaginary part of coherency and the phase-lag index as measures that discount zero-lag coupling.
- **Results.** Speaker-leading segments: partner-related emotion ratings correlate with parasympathetic HRV (RMSSD, SD1) up to 0.63; listener-leading segments: sample entropy, Rényi entropy and LF power up to 0.71; diffusion entropy flips the sign of its correlation with polarity. Correlations are across aggregated segments; no surrogates, no causal test.
- **Limitations stated:** small sample, structured debate, polarity only analysed, no causal inference, faces and voice not analysed.

## What it means for the design
1. **Signed, zero-lag-discounting lead–lag of two people's continuous signals is an active, current measurement practice in dyadic affect research** (here on heart rhythm). Magnitude-plus-polarity of a complex coupling vector is the same split as the design's coherence-for-the-limiter, quadrature-for-the-core.
2. **Polarity mapped to different self/partner emotion associations** is the kind of state-level claim the design's ρ array would need to show on recorded dyads; this study shows it only correlationally, with ratings the project may not read (Principle 1, D70).

## Verdict
- [Bidirectional phase coupling in dyadic debate (Alkhodari et al.)](alkhodari-2026-bidirectional-phase-coupling-dyad.md) — 2026 — watch (prior art: signed dyadic lead–lag of continuous signals) — a complex phase-coupling index on 16 debating dyads' heart rhythms gives strength and lead polarity; speaker-leading vs listener-leading segments associate with different HRV features (r up to 0.63 and 0.71); correlational, no surrogates.
