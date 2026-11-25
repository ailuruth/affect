# Windowed cross-correlation and peak picking: Boker, Xu, Rotondo & King 2002 (Psychological Methods 7:338-355, doi 10.1037/1082-989X.7.3.338) and the `wcc` R package

Source read: the 2002 abstract (Europe PMC record, PMID 12243305); the `wcc` 0.4.2 reference manual on CRAN (maintainer Steven Boker), all functions; and the WCC and peak-picking description in Moulder, Boker et al. 2018 (see moulder-2018-synchrony-surrogates.md). I could NOT read the 2002 article itself (APA paywall; Semantic Scholar lists it as closed access). Author order per PubMed is Boker, Xu, Rotondo, King.

## Claims
- Abstract: "Cross-correlation and most other longitudinal analyses assume that the association between 2 variables is stationary." WCC estimates the peak association and the lag at which it occurs, over successive windows of elapsed time.

## Evidence
- Four parameters (Moulder 2018: "Researchers need to choose four parameters in order to fully specify a WCC analysis"): window size, maximum lag, window increment, lag increment. "a pair of time series are first broken into a number of short paired windows"; "Windows are cross-correlated at differing lags by lagging one window positively or negatively in time."
- `wcc` defaults, in samples: `wMax` = 50 (window; must be at least 5, "It is recommended that wMax be greater than 15"), `tMax` = 50 (max lag), `wInc` = 1, `tInc` = 1. Increment 1 gives the greatest sensitivity to non-stationary change and to lag changes.
- Peak picking: "The peak picking algorithm starts at the center column (lag 0) of the first row of a WCC matrix" and searches both directions for the peak closest to lag 0 (Moulder 2018). In `wcc::wccPeakPick`, a peak must exceed the values within `Lsize` (default 8) samples on both sides, rows are loess-smoothed with `pspan` = 0.25, and rows with no peak return NA.
- Summaries: mean and SD of peak correlation and mean and SD of peak lag; `wccAggregate` also reports Fisher-z means and variances.
- Significance: no parametric test. `wccSurrogateDyads` builds a null by re-pairing series across dyads (at most N(N-1)/2 unique surrogates; 45 for N = 10); `wccTestSurrogateDyads` reports the proportion of real dyads outside the surrogate 5th-95th range, a two-sided Kolmogorov-Smirnov p-value and decile differences. `wccFindDyadParam` tunes parameters on a hold-out set "between 10 and 20 dyadic timeseries".

## License
`wcc`: Apache License 2.0. Article: APA copyright.

## Runs on this Mac without a GPU?
Yes. R package with compiled C and a cumulative-sum method; CPU only.

## Verdict: adopt (analysis method)
- The standard way to ask whether the operator's AU series follows the agent's, and at what lag, without assuming the coupling is constant. Report all four parameters in seconds and samples, fixed before looking at outcome data.
- Direction: a peak at positive lag with the human trailing the agent supports "the operator follows"; but Moulder 2018 found mean peak lag rarely beats any null, so lag alone cannot carry the claim.
- Significance must come from surrogates (Moulder 2018), not from testing r against zero.
- The parameter choices in the original 2002 paper are unverified because I did not read it.
