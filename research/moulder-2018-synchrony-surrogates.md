# Moulder, Boker, Ramseyer & Tschacher 2018, "Determining synchrony between behavioral time series: An application of surrogate data generation for establishing falsifiable null-hypotheses" (Psychological Methods 23(4):757-773, doi 10.1037/met0000172)

Source read: full author manuscript (PMC6163103, via the NCBI BioC full-text service), all sections and table footnotes.

## Claims
- "All measures of synchrony show significant synchrony even when participants have not interacted with one another." The null "no synchrony exists between two individuals" is "theoretically impossible and can easily be falsely rejected by standard null-hypothesis testing methods."
- Surrogate data give falsifiable nulls; which surrogate you use decides which null you reject.

## Evidence
- Four surrogates:
  - Data shuffling: "each data point, Xi, is randomly shuffled"; keeps "the same mean, variance, and distribution as X, but all time dependent properties of this series are now destroyed."
  - Segment shuffling: "cut a time series X into shorter sections of size m which are randomly appended to one another"; m = 2 s and 30 s here; "conserves more time dependent structure".
  - Data sliding: cut at a point in the middle 60% of the series, move the tail to the front; "conserves most time dependent structure".
  - Participant shuffling: pair X with a partner's series from another dyad; tests "the amount of synchrony between participants engaged in conversation with one another is no different than participants not in conversation"; inflated if all dyads "share a similar prompt, talking point, or behavior".
- WCC settings tested: "window size and maximum lag parameters of either 2-seconds and 2-seconds or 30-seconds and 5-seconds". Data: sine waves and MEA at 10 Hz, motion capture at 83 Hz, 5 minutes each, plus random noise. Window and lag increments are not stated for the study (Figure 1 example uses 1 and 1).
- Synchrony scores: "the mean absolute value of all elements in the matrix z yields a single measure of global synchrony" (Fisher z), plus four peak-picking measures (mean and SD of peak r, mean and SD of peak lag).
- Test: 1000 surrogates per series for shuffling, segment shuffling and sliding; all possible pairs for participant shuffling. "Observed synchrony scores were then compared to the 95th percentile of these distributions" (one-tailed, α = .05).
- Results: data shuffling was easiest to reject; under data sliding only some measures survived, e.g. MEA rejected it for mean peak r and mean absolute Fisher z at 30-s windows / 5-s lag, and "This null-hypothesis was not rejected for any synchrony statistic for random noise." Mean peak lag rarely rejected any null.
- Recommendations: "start with the proposed data shuffling" method; participant shuffling only "when researchers have data from at least 50 additional participants' data"; "These methods require many data points (we suggest at least 500)".

## License
Author manuscript in PMC: "available for text mining" and fair use; APA copyright. No code released with the paper (`wcc` and `rMEA` implement parts).

## Runs on this Mac without a GPU?
Yes. 1000 WCC surrogates on a 5-minute 30 Hz series is CPU work in seconds to minutes.

## Verdict: adopt (significance procedure)
- For both claims, compute synchrony as mean absolute Fisher-z WCC and mean peak r, and require the observed value to exceed the 95th percentile of surrogates.
- Data shuffling is too easy: any two autocorrelated series beat it. A pass should be claimed only against segment shuffling and data sliding, with the surrogate type named.
- For "operator follows agent", participant shuffling is weak in our design because every session sees the same agent behaviour repertoire; the paper's own warning about shared prompts applies.
- At least 500 samples per series per test.
