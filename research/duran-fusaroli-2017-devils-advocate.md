# Conversing with a devil's advocate: interpersonal coordination in deception and disagreement (Duran & Fusaroli)

Nicholas D. Duran & Riccardo Fusaroli, *PLoS ONE* 12(6):e0178140, 2017, doi:10.1371/journal.pone.0178140 (PMC5456047). Data and code: github.com/nickduran/coordination-deception.

## What was read
The full PMC open-access text: introduction and hypotheses, paradigm, participants, measurement (motion-energy extraction, windowed lagged cross-correlation, speech-rate series, CRQA), virtual-pair baseline, mixed models, cross-validation, all results (Tables 1–2), discussion. Figures not seen; supplementary files (rapport by role, prediction from ratings) not read.

## Findings, precisely

**Design.** 46 dyads of undergraduates (22 disagree, 24 agree; strangers), standing face to face ~6 ft apart, two 8-min conversations on political topics. Between dyads: **agree vs disagree**. Within dyads: **honest vs devil's advocate** (one partner secretly argues the position opposite to their own; the naive partner is never told; none suspected). Order counterbalanced.

**Measures.**
- Head motion energy from side-view video (frame differencing, 6 Hz). Windowed lagged cross-correlation, 10-s windows, lags up to 5 s in 1/6-s steps. Three summaries: **~0 ms** (lag 0 ± one step), **DA-follows** (positive lags to 1 s), **Naive-follows** (negative lags to 1 s).
- Lower-body motion as a control channel.
- Speech rate: syllables/min in 5-s windows with 333-ms slide (3 Hz). CRQA indices: RR (amount), DET, L, LMAX, T2 (stability), ENTR (complexity).
- Baseline: virtual pairs from different conversations of the same condition.

**Head movement.**
- Virtual pairs: no coordination across lags and no condition effects.
- Real pairs, honest conversations: **agree > disagree** at ~0 ms (0.093 vs 0.069, p = .02) and DA-follows (0.060 vs 0.025, p = .003).
- Real pairs, deceptive conversations: **disagree > agree**, and **deceptive disagreement is the peak**: ~0 ms 0.132 (vs honest disagreement 0.069, p = .003); DA-follows 0.088 (vs 0.025, p = .01). Veracity × Conflict interactions p = .021 and .024. Naive-follows showed no effects.
- So the person with the extra monitoring demand (the deceiver, under threat of disbelief) **follows** the partner more within 1 s.

**Lower body.** Tightly coupled (cross-correlation ≈ 0.235) in every condition, **no condition differences** — a context-blind coupled channel alongside a context-sensitive one.

**Speech rate.** Real > virtual on every CRQA index (p < .00001). Disagreement: lower RR (0.041 vs 0.068), lower DET (0.60 vs 0.70), shorter LMAX (22.8 vs 42.4), longer T2 (64.6 vs 47.0). Deception (main effect, no interaction): longer L (4.08 vs 3.41), longer LMAX (35.3 vs 24.9), **higher entropy** (1.46 vs 1.30) — more stable and more varied, which the authors read as "flexible interpersonal adaptation", not "stereotyped" repetition.

**Rapport ratings.** Agreement rated closer and more understood; deception made no difference to ratings — so in deceptive talk coordination and rated rapport came apart.

**Prediction across dyads.** Deception detectable at 66.2% balanced accuracy from one feature (lagged head synchrony at lag −2 s/−3 s, the DA following less at that lag); disagreement at 58.7% from lower speech-rate RR. Weak generalisation; behaviour is dyad-specific.

## What it means for the designs
1. **Coupling strength is not a monotone function of the relationship.** Honest disagreement lowers head coupling; disagreement plus a believability demand raises it above everything. A single relational scalar running from "flat" to "copy" cannot produce both. What drives tight following here is **monitoring demand on one partner** (role-asymmetric: DA-follows changes, Naive-follows does not). A design must let attentional demand and relational stance act on coupling **separately**, possibly in opposite directions.
2. **Following is role-asymmetric.** Only one direction of lag changed. The agent's lead/follow balance must be a property of its role in the episode, not a symmetric dyad-level synchrony.
3. **Some channels are context-blind.** Lower-body coupling held at ~0.24 in every condition. A design should not route all channels through the same context gate; at least one slow postural channel may be coupled invariantly (and such invariance is a weak, safe form of matching, not the face-level copying the brief forbids).
4. **"Stable but varied" is the signature of good coupling on prosody.** Longer shared sequences together with higher entropy of their lengths: coupling that is not periodic repetition. This matches Ravreby 2022's sync-plus-complexity result and gives a measurable target: recurrence structure with high DET *and* high line-length entropy, not high DET alone.
5. **Time scales:** head following within 1 s; speech-rate coupling across the whole 8-min conversation, including re-use of a partner's pattern much later (CRQA, all lags).

## Verdict
**adopt** — demonstrates in 46 live dyads that coupling magnitude depends on a goal/attention variable that can move against the relational one, that following is role-asymmetric, and that one channel stays coupled regardless; motion-energy from side video is coarse.
