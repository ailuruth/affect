# Influence budgets: one privacy-style guarantee in place of per-route caps (synthesis)

Written 2026-11-26 from six notes:
- kairouz-2015-composition-theorem-dp.md (carries DRV10 advanced composition and the standard definitions as restated);
- mironov-2017-renyi-differential-privacy.md;
- rogers-2016-privacy-odometers-filters.md;
- jain-2021-dp-continual-observation.md (carries DNPR10 as restated);
- alvim-2011-dp-utility-information-leakage.md (carries Smith 2009 as restated);
- andres-2013-geo-indistinguishability.md (carries Chatzikokolakis et al. 2013 d-privacy as restated).

Dwork & Roth 2014, Dwork–Rothblum–Vadhan 2010, Dwork–Naor–Pitassi–Rothblum 2010, Smith 2009 and Chatzikokolakis et al. 2013 were **not reachable** from this session. Each is cited only through the restatement named. This synthesis complements whole-loop-bounds-synthesis.md: that one bounds *gain* over all routes, this one bounds *distinguishability*.

## The question
Five designs capped partner→face routes one at a time, and copying returned through a route nobody counted:
- the base tilt (K1);
- event proposals that read ℓ − b̃ (K3);
- Claude's selection reading ŝ, and from there voice (K9);
- a slow state tracking the partner's held level.

Can a single guarantee on *everything the partner can influence*, closed under composition, post-processing and adaptive interaction, replace the caps?

## Answer in one paragraph
**Partly yes.** Rényi DP gives exactly the missing accounting:
- one ledger, a vector of ε(α) values;
- every route adds into it (Mironov, Proposition 1), whatever the interleaving and however the partner adapts (the composition game of Kairouz et al.; the adaptive continual-release game of Jain et al.);
- anything computed only from released outputs is free (post-processing);
- every downstream use of the outputs, including an observer's test, a slow integrator or a learner, is bounded by the same number (Kairouz, Theorem 2.1 and the Blackwell converse).

The route-completeness lemma that every critique broke becomes one structural check: **only the sanitizer touches partner data**. But it is **sign-blind**. It bounds how much the agent's whole output can depend on the partner, never in which direction. And with standard granularities (event-level or user-level) it is either vacuous over hours or forbids contingent care. It works only with a **neighbouring relation designed on held level** and with **noise designed on traces**. That makes it the *magnitude* primitive. A structural constraint (the REN's sign-free incremental ceilings, the router's role code) must still supply the *shape*.

## Sketch of the theorem
**Setting.**
- P = (p₁, …, p_T) is the partner's whole input to the agent: face features, voice prosody and words. It must be the whole input, for the reason given under "What breaks", item 2.
- Z is the agent's own exogenous variables (drives, noise seeds).
- The agent is a randomized map 𝒜 producing Y = (face_t, voice_t, draft choices, memory writes, weight updates)_{t ≤ T}.
- The partner is an adaptive adversary: p_{t+1} may depend on Y_{≤t}.

**Neighbouring relations (innate).**
- *Onset neighbours* ~_e: P and P′ differ by one expression event, an onset of size ≤ Δ_e on one synergy.
- *Level neighbours* ~_L: P′ = P + Δ_L u·1_W, a sustained offset of size Δ_L along unit direction u, over any window W of any length.

**Architecture (A).**
- Every component that reads P is inside a sanitizer 𝒮.
- 𝒮 releases X_t = (h ∗ p)_t + n_t, with Gaussian n_t ∼ N(0, σ²I) and an innate linear prefilter h of zero DC gain (H(0) = 0).
- It also releases discrete partner-dependent events and choices only through mechanisms of stated RDP curve ε_k(α), for example a softmax over scores of bounded sensitivity.
- Everything else in 𝒜 (the core, Claude, memory, learning) reads only X, the released events and Z.

**Filter (F).**
- A basic-sum privacy filter with innate budgets (ε_e, ε_L) per refresh horizon H halts all partner-dependent releases when either budget is spent (Rogers, Theorem 3.4).

**Claim** (my statement; the parts are standard).
1. **Whole-output budget.** For all adaptive partners and all parameter values of the core, including values reached by learning (learning reads only X, so it is post-processing), 𝒜 is (α, ε_e)-RDP with respect to ~_e and (α, ε_L)-RDP with respect to ~_L, over each horizon H. *Proof:* composition (Mironov, Proposition 1) of the Gaussian costs α‖h ∗ δ‖²Δ²/(2σ²), plus the discrete curves, all capped by the filter. Then post-processing. The level cost is finite for every W because H(0) = 0. With a single onset of size Δ_e, the Gaussian part costs α‖h‖²Δ_e²/(2σ²).
2. **Copy ceiling for held level.** Convert to (ε, δ) by Proposition 3. For any statistic of Y, including the agent's own window-mean face on any channel, the probability q that it lands within Δ_L/2 of the partner's held level under both P and P′ obeys

   q ≤ (e^ε + δ)/(1 + e^ε)  (Kairouz, Theorem 2.1).

   At ε = 0.1 this is chance (0.525). It holds over every route at once: tilt, events, Claude, voice, memory.
3. **Per-channel legibility.** On any channel whose partner-dependent part is linear with gain g, g ≤ (σ/Δ)√(2ε/α).
4. **Contingent responding is allowed, at a price in resolution.** A categorical decision with r outcomes that depends on the held level can achieve utility up to the ε-DP ceiling (Alvim, Theorem 3). For r = 2 at ε_L = 1 it can be about 73% right on a level difference of Δ_L, and more on larger differences by group privacy or d-privacy scaling. Continuous tracking cannot.

The design-specific proof burden is only (A): a taint check that no partner-reading code sits outside 𝒮. That is the analogue of proving the REN contains every partner-dependent signal, and it is easier, because 𝒮 is an input gate rather than a whole map.

## What breaks
1. **Sign and form are invisible.** Divergences are invariant to bijections of the output (Kairouz, Theorem 2.5). Mirroring and countering an onset cost the same. Inside the budget, the agent may copy as well as it can respond. Concretely, a fast onset mirror is allowed at ε_e. That is acceptable only because Principle 3 wants the fast match anyway. Anything about direction (no positive linear coupling in 2.6–6.5 Hz, the C1 constraint) must come from structure, not from the budget.
2. **The secret must be the partner's whole input.** DP says nothing about correlated side information (the Terry Gross point; Kairouz: DP "implicitly imposes independence"). If words are outside the protected input, mood leaks through Claude's reading of the words, and the face-only guarantee is about a channel, not about the partner. Putting words inside 𝒮 means Claude reads partner text only through a priced mechanism. Today that is the costliest part of the proposal: private text generation at useful budgets is not something these sources address.
3. **Real noise.** No deterministic non-constant map is DP. The noise sits either on perception, in which case the agent sees the partner blurred and only through changes, or on output, in which case the face jitters by σ on every partner-sensitive channel. Spending budget on events, by putting the noise on high-passed onsets, keeps the face smooth. It still means the agent perceives held levels only to resolution ~1/ε_L.
4. **The agent cannot know sustained partner states well.** With level-privacy, comforting a persistently sad partner is possible only as a coarse decision, a few bits per horizon (Alvim, Proposition 2). Is that enough for the care behaviour the brief wants? It is an empirical question, not answered here.
5. **Horizons are a value choice.** A per-hour budget still lets the partner shift the agent ε_L per hour. Over days, temperament can be set anyway. The horizon must be stated, and cannot be derived (Rogers).
6. **Implementation hazards.** Rounding after noise can break the guarantee (Andrés, Theorem 4.1). Running meters (odometers) are provably weaker than filters (Rogers, Theorem 6.1). Data-dependent stopping is itself a channel unless it is behind a filter.

## Recommendation
Use RDP as the **magnitude ledger** and the REN as the **shape**: an incremental-gain certificate supplies each route's sensitivity, and calibrated noise turns sensitivity into indistinguishability (andres-2013, point 4). Together:
- the REN's per-channel ceilings c_i bound gain;
- a level-neighbour RDP budget ε_L bounds held-level tracking over *all* routes, including the discrete ones a gain bound cannot certify (events, Claude's choices, memory writes);
- the filter makes the budget an innate constant with a halt.

The test that would retire the idea is a measurement, not a proof. Build the sanitizer, run the fibred critique's K1, K3 and K9 attacks against it, and report the ε each one spends. Then ask whether the care behaviour of item 4 survives at the ε_L that makes q ≈ chance.
