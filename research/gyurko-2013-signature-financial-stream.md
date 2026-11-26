# Extracting information from the signature of a financial data stream (Gyurkó, Lyons, Kontkowski & Field)

Citation: L. G. Gyurkó, T. Lyons, M. Kontkowski, J. Field. "Extracting information from the signature of a financial data stream." arXiv:1307.7244 (v2, 15 Jul 2014).

Source read: arXiv v2 PDF, text-extracted, in full (sections 1–5 and figures/tables as extractable; the coefficient tables were partly garbled by extraction).

## What it does
- **Signature of a data stream.** Piecewise-linear interpolation of the samples, then iterated integrals to depth 4 (sigtools/CoRoPa). Properties used: reparametrisation invariance, linearity (shuffle product), signature of linear paths, Chen's multiplicative identity, uniqueness up to tree-like equivalence.
- **The area as lead–lag (section 2.3).** For i < j, A^{i,j} = ½(X^{(i,j)} − X^{(j,i)}) is the signed area between the curve and its chord. "If an increase (respectively decrease) of the component X¹ is typically followed by an increase (decrease) in the component X², then the area A^{1,2} is positive. If a move in X¹ is followed by a move in X² to the opposite direction, the area is negative." Second-order areas (depth 3) separate profiles with equal increments and equal area.
- **Lead–lag transform (section 2.5).** Pair a stream with its one-step-lagged copy; the area between the lead and lag components equals the quadratic (cross-)variation, which the signature of the raw path does not contain.
- **Experiments.** LASSO-regularised linear regression on truncated signatures of normalised order-book streams (time, log mid-price, spread, imbalance, cumulative volume, plus the lag of price). WTI crude 30-min buckets: 14:00–14:30 vs 9:30–10:00, out-of-sample correct classification 95 %, AUC 0.984; 12:00–12:30 vs 12:30–13:00 indistinguishable (AUC 0.49). Two FTSE execution algorithms: out-of-sample correct classification median about 0.58 (buy) against a 95 % shuffled-label reference of about 0.53; the most relevant terms were depth-4 iterated integrals; performance degrades below about 200 training streams.

## What it means for the design
1. **"Area = who led, by sign" is in the literature since at least 2013**, with the same caveat the design omits: the sign mixes direction of lead with sign of association (a follower in the opposite direction gives the opposite sign).
2. **The lead–lag transform is the design's quarter-lag hazard read the other way.** Pairing a path with its own one-step-lagged copy produces area equal to quadratic variation: a lagged copy is exactly what generates area. The design's own C3 (maximal area at a quarter-period lag) is this fact.
3. Signature features of short windows fed to a learned readout are standard practice; nothing here is online, two-party in the sense of interacting agents, or coupled.

## Verdict
- [Extracting information from the signature of a financial data stream (Gyurkó et al.)](gyurko-2013-signature-financial-stream.md) — 2013 — watch (prior art for the commutator's lead–lag reading) — the Lévy area of two components read as lead–lag by sign, explicitly confounded with the sign of association; the lead–lag transform shows a lagged self-copy is what creates area; LASSO on depth-4 signatures separates trading-time buckets (AUC 0.98) and two execution algorithms (correct 0.58 vs 0.53 shuffled).
