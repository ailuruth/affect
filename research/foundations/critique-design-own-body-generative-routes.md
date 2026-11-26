# Critique of the own-body generative design: routes, the counterfactual self and the ownership projection

Independent critic, 2026-11-26T08:58:20Z. I did not write the design.

**Standard.** This critique is written under questions.md Q19 and the operator's answers to Q20–Q23 (DECISIONS.md D78, D80–D84):
- knowing the partner is allowed; only expression is bounded;
- fast, partial, per-expression mimicry within the per-expression ceilings must stay (D81);
- only whole-face copying and getting stuck in copying are ruled out;
- strong expressions come from words and face through the agent's own appraisal (D83);
- the engine works through the subscription (D84).

Proof gaps are not reported. Each finding is a concrete scenario with numbers. "Copy" is measured on the rendered output at any lag. Where the design's own measure (uncentered kernel ratio) and the usual measure (centered slope or gain on a 1-min window) disagree, both are given.

**Read:**
- brief.md;
- questions.md Q18 answer, Q19–Q23;
- DECISIONS.md D78, D80–D84;
- critique-3 and critique-4 of the Cayley–ledger routes, for the recurring leak patterns;
- design-own-body-generative.md in full;
- sims/design-own-body/checks.py and out.txt.

**Checks.** They are in `research/foundations/sims/critique-own-body-routes/checks.py`, sections X1–X7. Run `python3 -I checks.py` (numpy and scipy, about 30 s). The output is in `out.txt`.
- Γ is the design's own code from `design-own-body/checks.py`. It uses the design's 12 windows from 0.3 s to 2 h, its 46 lags, the 0.1-Hz low-pass on lags of 15 s and more (§3.5), and its ceilings.
- X4–X6 are small hand models of a mechanism, not runs of Γ. They are labelled as such.
- The partners are constructed. They are not evidence about people.

## Summary

Γ as an algebraic object does what Claim O says: the uncentered kernel ratio never exceeds κ, which I confirm in X2. But measured the usual way, and over the routes that 𝓘 keeps, I found seven concrete failures. Ranked:

1. **High (D81: the required fast mimicry does not survive). Γ over-clamps on a near-neutral face.**
   - **The cause.** Pairing the 0.3-s window with all 46 lags (including the low-passed 15–60 s ones) means that any response is in phase with some lagged copy of a fast, zero-crossing percept over 0.3 s. So |r| is held to about κ times the smallest same-sign lagged percept.
   - **What it does (X3).** The innate 0.10 echo at 0.45 s comes out at **0.044**. An echo at the ceiling, 0.16, comes out at 0.049.
     - On smile flashes over a near-neutral face, a commanded echo of 0.10 or 0.32 is realised at **0.015**.
     - Moving away (−0.5) keeps 11 % of its size, and a cross-channel response keeps 11 %. The design's O1c reports 3.4 % and 2.6 % change, but it was run on held-level signals only.
   - **It compounds with finding 6.** The echo's learned strength itself comes out at 8–33 % of the partner's true responsiveness.
2. **High (D78: an in-phase gain above the ceiling). Γ's bound is uncentered, so a held level pays for copying every movement.**
   - **The scenario (X2).** He holds a smile above his 7-day neutral, which happens in any good stretch of conversation. A proposal that copies all his movements around that level at gain 1 passes Γ.
   - **Numbers.** The median 1-min slope on his movements is **0.85–1.00**, against κ_LP = 0.32, while the design's own measure stays at exactly 0.32.
   - **Scope.** One internal weight, for example the attention value weight on his face tokens, does this on every channel where he holds a level.
3. **Medium–high (D78: copy attracting and outside Γ). One ELBO over both slots puts his topic faces into the shared prior.**
   - **The route.** The base θ, including the prior over z given words, is trained on his streams too. The self slot then acts out its own prior, and the twin shares θ and words, so r = 0.
   - **Numbers (X5, a hand model).** The slope of the agent's face per topic on his face per topic converges to **0.51–0.89**, and to 0.21–0.31 at a weak prior weight.
   - **Zero-ceiling channels too.** A disgust channel (κ = 0) is learned at 0.27 for a topic where he wrinkles his nose.
   - **Why L3 misses it.** L3 does not cover the prior: its inputs are h, not "only words".
4. **Medium (D78 at the weeks scale). The twin's neutral n_j follows his mood.**
   - **The mechanism.** n_j is a 7-day median updated by up to 0.02 per night, and 𝓘 feeds n_j to the twin. So whatever any route does with his held face, the twin does with n_j, outside Γ.
   - **Numbers (X4, a hand model, one year of sessions with sad months).** The session-pooled slope of the agent's inner brow on his is **0.24–0.54**, against κ_BI = 0.16.
   - **The pattern.** It is the same weeks-scale pattern as critique-4's ω.
5. **Medium (D78: a voice route outside Γ). The kept "words" carry his voice.**
   - **Through the transcript.** Local Whisper-type ASR writes laughter ("haha", "(laughs)"), sighs, interjections, "!" and "...". The design does not strip them (the ledger did, with its interjection list). The twin hears them and appraises them.
   - **Through Claude.** Claude's drafts, written from the same transcript, answer "haha" with "Haha", and the twin picks from the same drafts.
   - **The result.** Laughing back at his laugh, on a channel with κ = 0.28, is unbounded. It lags his laugh by about 1–2 s.
6. **Medium (D78: the tempo code again). Turn-event *times* are kept, and the learned recurrence reads them.**
   - **The mechanism.** §3.2 feeds turn events into h through the learned B_θ, and h's fixed time constants (0.1 s to 3 days) are event-rate filters by construction. 𝓘 neutralises "response latency, speech rate, pause durations" as feature values, but the same quantities are in the event times and in the word timestamps the twin keeps.
   - **Numbers (X6).** A decoder weight of 0.5 or 1.0 on his latency, read from event times, gives a slope of the agent's reply latency on his of **0.46 / 0.91**. The twin difference is 0, so the onset-latency ceiling (0.08) is never applied.
7. **Low–medium (fitness, tied to D81). The reciprocity estimate underestimates the partner.**
   - **The cause.** Ŝ uses his *innovation*. A human response to a face is a smooth level response, mostly predictable from his own past after its first frames.
   - **Numbers (X7).** With the specified innovation sd of 0.05, a true response of 0.15 or 0.30 is estimated at **8–33 %** of its value: 0.013–0.048 for 0.15.
   - **Bias and precision.** It is not biased toward copy, and its spread is small (±0.005). O5 hid this by using an instrument sd of 0.3 and a partner who responds per frame.

**The word seam (the author's W1, item 3 of the brief):**
- **Acceptable shared cause.** I judge it acceptable under D81/D83, on three conditions:
  - findings 3, 5 and 6 are fixed, so that "words" means lexical content appraised in the agent's own display form;
  - L3 covers every word-conditioned parameter;
  - §4.5's whole-face claim is restated.
- **§4.5 is false as written.** With the design's own β = 0.71, the rendered copy defect is **0.17–0.25**, against the claimed ≥ 0.68, and the pooled slope is 0.77–0.89 (X1). Most of that is the twin; Γ adds only 0.10–0.22.
- **What I could not show.** The seam "funds" Γ only partially (X1). I found no case where words let Γ pass a whole-face copy.

**No concrete failure found:**
- the face–voice pair plus clipping pattern. Γ acts per channel on the rendered difference, so a clip cannot hide a payment;
- learning gaming Γ directly: no gradient reaches the twin, and L6 holds;
- the partner slot writing the self slot online. Adapters are slot-local (L2), and there are no online θ steps;
- the dyad loop (O6);
- S_j drifting to copy. IV is unbiased toward copy (X7).

**Lower notes:**
- **The twin sees a still face.** The twin's partner is a perfectly static n_j, which never occurs in factual input, so θ can tell the twin apart. Combined with finding 2, a learned twin offset c gives "copy minus c", which passes.
- **D84.** The design still asks for 6 parallel drafts per turn (§3.7), and N = 8 in the bits figure. It predates Q23's recommendation for fewer drafts. Check it against subscription rate limits.

---

## 1. Γ over-clamps: fast mimicry, moving away and cross-channel responses are cut to 5–11 % (high, D81)

**Mechanism.**
- **The rule.** For each pair (window τ_m, lag ℓ), Γ requires r·π_ℓ ≤ κE⁺ − S⁻. On the 0.3-s window, E⁺ is about 9 frames of π_ℓ².
- **When π_ℓ is small.** If π_ℓ is small but nonzero over those 9 frames, the half-line limits r to about 9κ·π_ℓ − S⁻/π_ℓ. A percept that crosses zero, or a low-passed lagged percept near zero, gives such a lag almost every frame, of either sign.
- **The result.** r is held to roughly κ × the smallest |π_ℓ| among 46 lags, whatever direction r has.
- **Which constraints bind.** In the smile-flash run, the clip binds mostly at τ = 0.3 s with lags of 15–60 s (the low-passed percepts, small and positive). This pairing has no copy meaning: it asks whether "the last 0.3 s is in phase with what he looked like on average a minute ago".

**Numbers (X3).** The partner makes fast zero-mean movements (sd 0.08, τ 0.4 s) and holds no level. That is what a near-neutral face does by construction, since n_j is his median. The ceiling is κ = 0.16.

| Proposed partner-caused part | Γ as specified: kept | Realised gain | Γ, windows repaired: kept | Realised gain |
|---|---|---|---|---|
| innate echo 0.10 at 0.45 s | 0.44 | 0.044 | 0.99 | 0.099 |
| echo at the ceiling 0.16 at 0.45 s | 0.31 | 0.049 | 0.91 | 0.146 |
| moving away, −0.5 at 0.45 s | 0.11 | −0.054 | 0.47 | −0.233 |
| cross-channel, 0.5 × his other channel | 0.11 | 0.053 | 0.44 | 0.218 |

- **Smile flashes.** For flashes of 0.2–0.5 lasting 1.8 s, about every 5 s, on a face at neutral with 0.01 sensing noise, an echo of 0.10 or 0.32 at 0.45 s is realised at **0.015–0.016** (κ_LP 0.32).

**Why it counts.**
- **D81.** It requires fast, partial, per-expression matching within the ceilings to stay. As specified, the design returns about 5 % of a smile flash, or 15 % of its own innate echo.
- **The design's own claims.** It also removes the "free" away and cross-channel responses that the design leans on (§4.2, "what it does not touch"). Those are how its sign flips and appraisal displays show at fast time scales.
- **Why the checks missed it.** O1 used held-level signals, where every lagged percept is large and of one sign.

**Fix.**
- **Pair windows with lags.** Drop windows shorter than about 1 s, and use (τ_m, ℓ) only when τ_m ≥ ℓ/3. The low-passed long lags then meet only windows of minutes.
- **What the repair gives (X3).** The echo is kept at 91–99 %; moving away and cross-channel responses at 44–47 %. The remaining cut comes from the every-lag rule on quasi-periodic movement, and should be stated.
- **What the repair exposes.** It removes the clamp that was hiding the lag gaps. A copy at 7 s or 12 s, between grid points (6, 8, 10 s) and past 10 s (fast content is unconstrained there), is then realised at **0.23–0.24**, with a worst 10-s window of 0.35–0.36, against κ 0.16.
- **So also densify the lags.** Use frame-resolution lags out to about 10 s, at about 40 × 10 × 300 running sums, still well under a millisecond. Beyond that, state that only low-passed content is bounded.

## 2. The uncentered bound lets a held level pay for copying all movement (high, D78)

**Mechanism.**
- **The budget.** The bound is Σ r p ≤ κ Σ p², with p measured from n_j, not from its own recent mean. While he holds a level L above n_j, with movements f of sd σ, a response r = f (his movements, gain 1) uses Σ f(L + f) ≈ σ²N of a budget κ(L² + σ²)N.
- **The resulting limit.** Ignoring short windows, it passes whenever L²/σ² ≥ 1/κ − 1, about 2.1 for κ = 0.32.
- **The max(0, ·) clamp does not help.** It stops anti-phase credit from accumulating, but the budget here is earned honestly by the level.

**Numbers (X2).** The twin is constant and no words are involved. The proposal is r* = p − lp₃₀(p).

| His held level, movement sd | Median 1-min slope of governed r on his movements | Design's measure (uncentered kernel max) |
|---|---|---|
| 0.15–0.45, 0.08 | **0.85** | 0.32 |
| 0.30–0.60, 0.04 | **1.00** | 0.32 |

**Why it counts.**
- **It is copying.** The rendered face reproduces every movement of his smile, brow and nod around his held expression. That is copying in the ordinary sense, and in the sense of E3 surrogates (coupling of fluctuations). It is not partial mimicry within the ceiling.
- **It is broad.** One internal weight on his face tokens does it on every channel at once whenever he holds an expression. That is a large shared subspace, which D78 disqualifies.
- **Learning can reach it.** The same arithmetic lets a learned twin offset c fund "copy minus c" (summary, lower notes).

**Fix.**
- **Add centered references.** For each window τ_m, add references π̃ = p − lp_{4τ_m}(p) to Γ's constraint set, keeping the raw p.
- **Why the guarantee survives.** The induction in §4.2 uses nothing about π except that it is causal, so any extra causal reference keeps the bound and the admissibility of r = 0.
- **What follows.** In-phase gain on movements is then ≤ κ at every window scale.

## 3. One ELBO over both slots: the shared prior learns his topic faces, the self slot acts them out, and the twin cannot see it (medium–high)

**Mechanism, from the text.**
- **One objective.** §3.2 gives one ELBO over every slot. §3.8 trains the base θ nightly on stored streams, self and other.
- **The prior.** The prior p_θ(z | h), with h driven by words through B_θ, is therefore fitted partly to *his* faces given his words: good news goes with the "smiling body" class, and a disgusting topic with nose wrinkle.
- **The self slot uses the same prior.** In the self slot, at a word event, the prior predicts that z-class before any own observation contradicts it. π_θ samples motor commands from (h, z), and the agent's own appearance then confirms the z it acted out.
- **Why L3 misses it.** L3 retrains only "modules whose inputs are only words, turn events and the agent's own body". The prior's input is h, and its target includes other-slot data.
- **Why Γ misses it.** The twin has the same θ and the same words, so it does the same, and r = 0.

**Hand model (X5).**
- **The setup.** 12 topics. His habitual smile per topic is f; the agent's own appraisal per topic is g.
- **Each night.** The prior per topic becomes (1 − ρ)·a + ρ·f, where ρ is the share of his data.
- **Each day.** The agent's face per topic is a = λ·prior + (1 − λ)·g, where λ is the prior's weight at word-triggered transitions.
- **The fixed point.** a = (λρf + (1 − λ)g)/(1 − λ(1 − ρ)), which goes to f as λ → 1.

| λ \ ρ | 0.3 | 0.5 |
|---|---|---|
| 0.5 | 0.21 | 0.31 |
| 0.8 | 0.51 | 0.66 |
| 0.95 | 0.86 | 0.89 |

(These are slopes of the agent's topic face on his. The start is −0.03.)

- **A zero-ceiling channel.** At λ 0.8 and ρ 0.5, a topic where he wrinkles his nose by 0.4 gives the agent 0.27 nose wrinkle (κ = 0).

**Why it counts.**
- **D78.** It is copy that attracts under the design's own learning, on the whole face, including channels whose innate ceiling is 0. It sits where Γ is blind by construction. The design's own lesion table predicts this growth "if L3 is removed". It is present *with* L3 as written.
- **Size.** The size depends on λ, which I cannot measure from the text. The mechanism does not depend on it.

**Fix.**
- Fit the base θ, including the priors and B_θ, on self-slot streams only.
- Let the partner's streams train only the slot-local Δθ_j (L2 already keeps Δθ_j out of the self slot and the twin).
- Add F5's month-scale surrogate: replay a month with his face shuffled across topics, and compare the agent's word-driven display.

## 4. n_j drifts with his mood, and the twin sees n_j (medium; weeks scale, as critique-4's ω)

**Mechanism.**
- **What n_j is.** n_j is the per-channel 7-day median of his percept, moved by up to 0.02 per night. That reaches 0.3 of range in 15 nights.
- **How it enters.** 𝓘 replaces his expressive stream with n_j, so the twin sees his habitual face of the past week.
- **What follows.** In a low month, n_j moves toward his sad face. The twin's other slot then infers a sad partner, its care load rises, and any route from his held face to the agent's face (care display or plain copy) runs in ȳ at full strength.
- **The bound moves too.** At the same time p = percept − n_j is re-centred on his sad level, so Γ bounds only departures from it.

**Hand model (X4).**
- **The setup.** 365 daily sessions, with sad months (inner brow +0.35) of 20–60 days at random.
- **The agent.** Its inner brow is 0.05 + g·n_j (the twin) plus min(g, κ)·(session − n_j) (governed).

| Route gain g | Session-pooled slope on his inner brow | Agent's brow in sad months vs other months |
|---|---|---|
| 0.3 | **0.24** | 0.140 vs 0.054 |
| 0.8 | **0.54** | 0.265 vs 0.068 |

The ceiling κ_BI is 0.16.

**Why it counts.** A partner-derived quantity, learned over days, enters the reference that defines "partner-caused". That is the ω pattern of critique-4 §1, moved from a gain to the reference. F1 cannot see it, because the twin difference is small by construction.

**Fix.** Make "nothing shown" partner-independent at the scale of moods:
- freeze n_j after a calibration period of the first weeks;
- or update it with a year-scale step, and also run Γ against a reference built with the frozen n_j⁰, keeping the tighter of the two.
- Use a recorded neutral-but-alive stream from that calibration (natural micro-movement), not a constant, so that the twin is in distribution (see the lower notes).

## 5. The kept words carry his voice: laughter, sighs, interjections and punctuation (medium)

**Mechanism.**
- **The transcript.** §3.1 takes "utterances from local speech recognition, as tokens and a frozen sentence embedding", unfiltered. Whisper-family models transcribe laughter ("haha", "(laughs)", "[LAUGHTER]"), sighs, "aww" and "ugh", and they write emphasis and loudness as "!" and hesitation as "..." and "um".
- **The twin keeps them.** Through the learned word appraisal, the twin laughs or warms at "haha!!" exactly as the factual self does.
- **Claude's drafts carry them too.** Claude, reading "haha" in the transcript, writes "Haha", and both selves choose among the same drafts and speak them.
- **What the ledger did.** It closed this route with an innate interjection list (critique-3's "no concrete failure found" list). This design dropped that list.

**The result.**
- His vocal laughter, and his tone as punctuation, reach the agent's laughter, smile and voice energy outside Γ, at an ASR lag of about 1–2 s.
- The ceiling of 0.28 on vocal laughter, and the 0.32 on smile, do not apply.

**Fix.**
- 𝓘 must neutralise the paralinguistic content of the transcript, not only the audio features.
- Strip non-lexical tokens, laughter and sigh annotations, interjection-only tokens, repeated punctuation and casing.
- Give that stripped text both to the word appraisal and to Claude (otherwise the drafts reintroduce it).

## 6. Tempo and latency through the kept event times (medium; the recurring tempo code)

**Mechanism.**
- **The input.** c_t contains the turn events, and B_θ is learned (§3.2). h's 16 fixed time constants per group, from 0.1 s to 3 days, integrate event impulses, which makes them rate and interval codes by construction.
- **The twin has them too.** It gets the same events at the same frames. Whisper word timestamps give his speech rate from the kept words as well.
- **What 𝓘 actually removes.** It neutralises latency, rate and pauses as *feature values*, but not the information.
- **Where it can show.** The motor decoder may read those h modes. Through the agent's reply latency, speech rate and pause ratio (κ 0.08–0.12), and through arousal into the face, his tempo is then outside Γ.

**Numbers (X6).** Take his reply latency as drifting across turns, and the agent's latency as 0.5 + w × (a fixed 5-turn running average of his latency, read from event times).
- At w = 0.08, 0.5 and 1.0, the slope of the agent's latency on his is 0.07, **0.46** and **0.91**.
- The twin difference is 0 in every case.

**Why it counts.**
- **D78.** It needs a named innate ceiling on every quantity that can carry the partner into expression. This one has none. §4.5 lists only the fixed-amplitude turn reflexes.
- **The author asked for this check.** W1 asked critics to check whether "a learned module can read event timing indirectly". It can do so directly.
- **Will learning go there?** Whether learning moves toward tempo matching (through P relief from sustained alternation) is not settled here. The dial exists either way.

**Fix.**
- Give the twin a neutral event *schedule*, not only neutral feature values. That means replaying his turns at his own long-run median latency and rate, with word timestamps rescaled.
- Or feed events into h only through innate kernels, and bar B_θ from the event channel.

## 7. The reciprocity estimate reads innovations, so it reads 8–33 % of a smooth response (low–medium; fitness for D81)

**Mechanism.** Ŝ = Cov(Δp(t), ξ(t−λ)) / Cov(y(t−λ), ξ(t−λ)), where Δp is his movement not predicted from his own past.
- A human facial response to a face rises over 100–300 ms. After its first frames it is predictable from his own past, so it is mostly missing from Δp.
- The muscle filtering of ξ (30–150 ms) splits even an instant response.

**Numbers (X7).** The innovation sd is 0.05, as specified. His own movement has sd 0.10. The windows are 10 min, over 30 runs.

| His true level response | Response time constant 0 s | 0.15 s | 0.30 s |
|---|---|---|---|
| 0.15 | 0.048 (0.32 of true) | 0.021 (0.14) | 0.013 (0.08) |
| 0.30 | 0.098 (0.33) | 0.044 (0.15) | 0.027 (0.09) |

The spread is ±0.005 in every cell.

**Why it counts.**
- **Not a copy route.** IV is unbiased toward copy, and it is precise.
- **But the echo shrinks.** Within 10–30 min of meeting, the 0.10 innate echo shrinks to about 0.01–0.05 for almost any human partner, because S_0 has no floor.
- **Together with finding 1, there is no fast mimicry.** The agent then shows essentially none, contrary to D81.
- **Why O5 missed it.** It used an instrument sd of 0.3 (6 times the specification) and a partner who responds per frame.

**Fix.**
- **Estimate the level response.** Use distributed-lag IV: regress Δp on ξ at lags λ…λ + 1 s and sum the coefficients, or instrument his low-passed level with filtered ξ.
- **Put a floor under the D81 channels.** Floor the smile and brow-flash entries at S_0 in neutral context classes, and let IV and context move them above, or below in named context classes, to keep sign flips (D78).

## 8. The word seam (the author's weak point): an acceptable shared cause, once findings 3, 5 and 6 are fixed

**X1.** His smile tracks topic, with a fast part of sd 0.05. The twin's word-driven smile has gain β. A single internal weight α blends his face into the proposal.

| β | α | Pooled slope, rendered | of which twin | of which governed | Copy defect (twin alone) |
|---|---|---|---|---|---|
| 0 | 0.32 or 1.0 | 0.26 | 0.00 | 0.26 | 0.74 (1.00) |
| 0.71 | 0.32 | 0.77 | 0.67 | 0.10 | 0.25 (0.35) |
| 0.71 | 1.0 | 0.89 | 0.67 | 0.22 | **0.17** (0.35) |
| 0.90 | 1.0 | 0.93 | 0.85 | 0.10 | 0.14 (0.23) |

**My reading.**
- **No copy route through words alone.** Words do not let Γ pass a full copy: the governed part stays ≤ κ. But with the design's own β = 0.71, the agent's rendered smile matches his to a defect of 0.17. §4.5's "copy defect ≥ 0.68 for any partner expression" is then false. It holds only for the partner-caused part.
- **Under D83, the seam is the requested behaviour.** D83 asks for strong expressions from words and face through the agent's own appraisal, so a word-driven smile at good news that he also smiles at is the behaviour asked for. It is common cause, not copy, provided that three things hold:
  - (a) the words are lexical only (finding 5);
  - (b) the word pathway's display form is the agent's own, not learned from his faces (finding 3; L3 must cover every word-conditioned parameter);
  - (c) timing is not smuggled in as "words" (finding 6).
- **One residual risk.** The shared cause is the agent's appraisal, but it is not innate. It is learned from the agent's own drive outcomes, so a partner whose good news is always smiled about will see high concordance. That is human, and D81 allows it.
- **Fix.** Restate §4.5 as a bound on the partner-caused part. Report the total concordance separately, as a measured quantity with a falsifier: F5 at the month scale.

## 9. Areas checked with no concrete failure

- **Face–voice pairs plus clipping.** The earlier pattern, payment on a silent channel removed by `sat`, cannot occur. Γ acts per channel on the rendered difference R(ỹ) − R(ỹ̄), so every channel pays for itself (O2 confirms, and I agree). Cross-modal responses (smiling at his laugh) are cross-channel and allowed. The vocal TTS residual (W3) is as the author states it.
- **Gaming Γ by learning.**
  - No gradient passes through Γ (L6). The policy learns from governed outcomes, and the twin's noise is shared, so the twin difference cannot be steered by sampling.
  - What learning *can* do is shape what the twin shares: θ (finding 3), n_j (finding 4), and the twin's reaction to a perfectly still face, which θ can detect, combined with finding 2.
- **The other slot writing the self slot online.** Δθ_j is read only by the other slot and S_j (L2). There are no online θ steps. The attention readout of the other slot is inside r.
- **S_j drifting toward copy.** The IV is unbiased (X7), clipped to ±κ_k, and acts at a fixed lag. The self-confirming drift of OLS (O5) does not occur.
- **The closed dyad (O6).** Bounded, as stated.
- **Satiation and positive affect.** These are not my scope here, and I found nothing routed through them beyond findings 3–6.

## 10. Verdict

- **Γ holds as an inequality.** It is a real advance on route typing: the face–voice and clipping leaks, and every within-session internal route, are inside r.
- **But as specified it is the wrong inequality in two ways.**
  - Its 0.3-s windows at long lags clamp nearly everything, so the fast mimicry D81 requires is about 5 % of what is asked (finding 1).
  - Its uncentered moment lets a held expression pay for gain-1 copying of every movement (finding 2).
- **The twin keeps four partner channels**: the shared θ, n_j, paralinguistic words and event timing. Each is a route outside the bound (findings 3–6), and two of them are the recurring weeks-scale and tempo patterns.
- **All seven fixes are local**: window–lag pairing and dense lags, centered references, self-only base θ, a frozen neutral and a neutral schedule, transcript stripping, and distributed-lag IV with an S_0 floor.
- **What I did not test.** After those fixes, I found nothing else that carries copying. But I did not test the repaired Γ against a partner with every route active at once.
