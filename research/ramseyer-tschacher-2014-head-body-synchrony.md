# Ramseyer & Tschacher 2014, "Nonverbal synchrony of head- and body-movement in psychotherapy: different signals have different associations with outcome" (Frontiers in Psychology 5:979, doi 10.3389/fpsyg.2014.00979)

Source read: Frontiers full-text HTML, first ~100k characters (introduction, method, results, most of the discussion). Read as a stand-in for Ramseyer & Tschacher 2011 (J Consult Clin Psychol 79:284-295, doi 10.1037/a0023419), whose full text I could NOT read (psync.ch copy returned 401; APA paywall). For 2011 I read only the ERIC abstract. This 2014 paper reanalyses a subsample of the 2011 data with the same method.

## Claims
- 2011 (ERIC abstract): in 104 sessions of 70 patients, "nonverbal synchrony is higher in genuine interactions contrasted with pseudointeractions", higher in sessions patients rated high in relationship quality, and associated with greater symptom reduction.
- 2014: head synchrony and body synchrony are measured separately and differ in strength and in their links to outcome (outcome associations not checked verbatim by me).

## Evidence
- Motion Energy Analysis (MEA): motion energy is "defined as differences in gray-scale pixels between consecutive video-frames", per region of interest; "the head region covered the head including the neck"; body region "the upper-body from the chair's seating-base upward and the arms". Raw series "filtered and corrected prior to further analyses" (details deferred to Grammer et al. 1999; frame rate and threshold not given in this paper).
- Synchrony: cross-correlated "in window segments of 1 min duration" with "time-lags up to ±5 s"; "Absolute values of cross-correlation were aggregated over the entire interval of 15 min in each session." Window increment and Fisher z use not stated.
- Pseudosynchrony: per session, N = 100 surrogates made by shuffling the data window-wise (windows paired with windows from other times in the same session); synchrony is "how much the genuine cross-correlation coefficients departed from the mean shuffled coefficients".
- Genuine vs pseudo: head t(69) = 6.03, p < .0001, d = 0.74; body t(69) = 2.17, p < .05, d = 0.20.
- Sample: 70 same-sex dyads, one session each, first 15 min of seated interaction.

## License
Frontiers article (open access; license text not shown in the part I read). MEA software: described as a "fully automated computer program" at psync.ch; I could not read its terms or platform list.

## Runs on this Mac without a GPU?
The method is frame differencing plus windowed correlation; both run on CPU. The original MEA program's platform is unverified.

## Verdict: adopt (analysis method: windowed |r| vs within-session shuffled surrogates)
- Scoring as published: 1-min windows, lags to ±5 s, mean absolute r over the session, minus the mean of 100 within-session window-shuffled surrogates; group test of genuine vs pseudo across dyads.
- MEA itself measures gross head and body motion, not facial expression. For this project it is the template for the statistics, applied to AU series from OpenFace; MEA on the face region could be a secondary, AU-free check of coordination.
- Absolute r means anti-phase coupling also counts as synchrony; for mimicry the sign matters, so report signed peak r as well (my inference).
