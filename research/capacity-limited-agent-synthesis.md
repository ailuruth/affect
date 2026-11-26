# A capacity-limited partner channel: what it predicts, and whether it can be a core primitive (synthesis)

Written 2026-11-26 from six notes:
- tanaka-2018-lqg-minimum-directed-information.md;
- alemi-2017-deep-variational-information-bottleneck.md;
- genewein-2015-bounded-rationality-abstraction-hierarchy.md;
- lai-2024-policy-compression-human-decisions.md;
- tiomkin-2017-unified-bellman-information-value.md;
- deng-2024-use-dependent-bias-information-bottleneck.md.

It also uses tatikonda-2009 and whole-loop-bounds-synthesis.md.

**Not read** (all blocked or paywalled from this session, so nothing here cites them):
- Sims 2003, "Implications of rational inattention";
- Tishby & Polani 2011;
- Zénon, Solopchuk & Pezzulo 2019;
- Lai & Gershman 2021 (the chapter).

Each was replaced by the readable source named in its slot's note.

## The lead
Replace many per-route caps with one innate capacity: the directed information from the partner's face stream to the agent's entire output is at most C bits/s, $I(u^T\to y^T)\le CT$. By data processing (Tatikonda; Tanaka Lemma 1), this covers every route at once, including learning, persistent states and Claude's text, provided that every partner-dependent signal passes through the channel.

## What the cap forces, for any core
These hold for every causal policy under the cap, not only an optimal one.
1. **Lag.** Following a step in the partner takes at least (bits needed)/C. For a partner level with time constant τ, the best follower has time constant (1/τ + 2C ln 2)⁻¹. That is ≈0.72 s at 1 bit/s and ≈3.6 s at 0.2 bit/s (scalar case of Tanaka Eq. 18; my derivation, checked numerically).
2. **A fidelity budget, spent by band.** In the Gaussian case the cap is a budget on coherence across frequencies, ∫ −½log₂(1 − |γ(f)|²) df ≤ C. Bits can be withheld from one band and spent in another.
3. **Few distinguishable partner states.** In a window of w seconds, at most 2^{Cw} partner histories can be told apart. The rank drop in Tanaka Fig. 5 and the collapse in Alemi Fig. 2 are the continuous and network versions.
4. **Fast channels cannot be copied; slow ones can.** The best copy fidelity on a Gauss–Markov partner level is g = Cτ ln2/(1 + Cτ ln2). At C = 1 bit/s that is 0.26 for τ = 0.5 s, 0.78 for 5 s and 0.995 for 300 s. Even at 0.2 bit/s it is 0.98 for τ = 300 s. **A rate cap does not stop held-level copying.**
5. **Gain and sign are free.** Information is invariant to scaling and sign. An amplified copy, an anti-copy and a copy all cost the same bits.

## What emerges only if the core optimises under the cap
Rate–distortion, the information bottleneck, policy compression and rational inattention all add the following when the core optimises. These are the excluded optimal-control cores.
- **A pull toward the agent's own habit.** Responses shrink toward the agent's own marginal action: π* ∝ P(a)e^{βQ} (Lai); mean = (βs + εs₀)/(β + ε) (Deng). This is perseveration toward the self, not the partner. In people it grows under time pressure (d = 0.32) and load. It is larger on a lower-capacity effector (the non-dominant hand). Capacity is trait-like across tasks (r = 0.43–0.57).
- **Inertia.** The cost is surprise relative to the agent's own predicted next action (Tiomkin Eq. 18). Holding course is cheap.
- **Partner bits in bursts.** Bits are drawn at critical moments (the "narrow door").
- **Categories set by the agent's own utility.** Partner states that call for the same response are merged, with stepwise regime changes as capacity changes (Genewein plateaus).
- **Stochasticity,** but only if the cap is built as a noisy channel. A quantiser does almost as well (Tanaka Eq. 8).

## Against the refined rule (D78)

| Requirement | Rate cap alone |
|---|---|
| Per expression | Yes, if C is split into innate C_i per channel (and per band). One global C is a single scalar over the whole face: Genewein and Lai show β (monotone in C) runs state-dependence from none to full |
| Sign-flippable | Neutral: sign is set by the core's objective, never by the cap |
| Innate ceiling | On fidelity in fast bands, yes. On gain, no (scale invariance). On held levels, effectively no (g → 1 as τ grows) |
| Copy non-attracting | Not by itself. In Lagrangian form the cost side pulls toward the agent's own marginal, but copy is attracting whenever the value side rewards predicting or matching the partner (Alemi: the relevance variable decides what is kept) |
| Existing framework? | Yes: rate–distortion / information bottleneck / directed-information control. A new core can use it only as a constraint |

So the cap **cannot replace** the per-channel gain ceiling. It covers what a gain bound cannot: fast bands, discrete content events and persistent-state writes. The gain ceiling covers what the cap leaks: amplitude and held levels. This matches the whole-loop synthesis, and adds numbers.

## Against the human non-copying signatures (C1–C10, non-copying-dynamics-synthesis.md)
- **Matches.**
  - **C9** (converge in parameters, not output): slow levels and the agent's own marginal are cheap to shift; fast moment-to-moment matching is expensive.
  - **C10** (self-restoration that coupling cannot switch off): the pull toward one's own marginal persists for any finite C. If C is a *shared* budget for partner and own body, it also predicts Galbusera's trade (high coupling, weak self-modulation).
  - **C8** (face coupling mostly common cause, slower when event and face disagree): an agent whose relevance variable is its own concerns spends its bits on the shared event. The partner-specific excess is small. Conflicting cues need more bits, so they arrive later (lag ∝ bits/C). Order-of-magnitude calibration: a ~0.5 s following lag implies C ≈ 1.4 bits/s per channel (speculative).
- **Partial.**
  - **C1:** the cap predicts *chance* coherence in fast bands, not *below-chance* coherence.
  - **C3:** it predicts content above chance and form at chance, not below chance.
  - **C4:** turn and role can gate *when* bits are spent (bursts), but not the sign.
  - **C6:** the attention or monitoring demand maps cleanly onto "how many bits the partner is worth", separately from stance, which sets sign through the objective. That gives two quantities, which C6 requires, but only if sign lives outside the cap.
- **Contradicts.**
  - **C2** requires form self-repetition not to exceed chance; compression *predicts* above-chance self-repetition.
  - **C7** requires novelty of the joint trajectory that grows over minutes; compression and inertia predict growing repetition.
  - **C5** (below-chance coupling in argument) costs bits, exactly like copying. A cap makes *ignoring* cheap, not *diverging*.

## What is missing to make it a new primitive
1. **A source of sign and divergence.** Below-chance coupling (C1, C2, C5) and growing novelty (C7) need a drive, not a limit. One candidate from Tiomkin's dual channel: cap *inbound* directed information (partner → agent). Let a satiable drive pursue *outbound* directed information over the joint state, meaning variety the agent itself causes. Copying is high-inbound and low-outbound, so it is poor on both counts. This pairing is my inference. No source combines the two, and it must not become an optimised objective, or it is excluded.
2. **A held-level leak fix.** Either keep the gain ceiling for low bands, or find a structural bound on low-frequency coherence: for example an innate noise floor N(f) injected on the partner path before any learned processing, bounding |γ(f)|² ≤ S/(S + N) per channel. This holds for mutual information by data processing. For coherence after nonlinear processing it is unproved.
3. **Innate, not priced.** VIB's β and Lai's adaptive β are learnable dials. A true cap needs a fixed noise floor with a bounded-range encoder, or a fixed cardinality (Genewein §4.3). Its value C_i must be compiled in.
4. **Accounting through persistence and learning.** Directed information has a Bellman recursion (Tiomkin), so it can be *metered* online. Composing that meter with the REN gain certificate into one copy-defect bound remains open problem 1 of the whole-loop synthesis.
5. **A human number.** No source gives C for face or voice coupling. Lai's estimator (Hutter mutual information) can measure partner → agent policy complexity per channel and band on the Seamless features without labels. That is the first measurement to make.
6. **Novelty.** As read, everything is existing machinery. The cap is a usable **constraint layer** for a new core. It is not itself the new computation.
