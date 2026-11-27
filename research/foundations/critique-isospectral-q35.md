# Critique: the isospectral core as an answer to Q35

Independent critic, 2026-11-27T02:15:49Z

**Under review.** Direction 1 of `research/new-core-search-3-synthesis.md`: the state is a symmetric matrix M. The partner may act only through a rotation X, the agent's own processes only through rotations Ω, and the body only through a spectral source S. The synthesis offers it as a possible safety net for Q35 that counts no routes.

**Question.** Can this guarantee every per-expression ceiling c_k, on every channel including the smallest, for unlisted routes at any delay, with no situation-specific rule (D88), while keeping D81's fast partial mimicry and the contingency gating?

**Read.** The synthesis and its checks (`sims/new-core-search-3/`); Q18, Q19, Q20, Q29 and Q35; D78, D81, D83, D88, D90 and D92; `design-cayley-ledger.md` §2.1, §2.13 and "Build finding at M0"; `engine/shadow/ledger.py`; the ceilings in `engine/config/channels.py`. On the channels the ceilings matter for, c_LD is 0.05, and 0.03–0.05 on the head, gaze and voice channels.

**Checks.** `sims/critique-isospectral/checks.py` (numpy, about 7 s, output in `out.txt`). The setup:
- one 2 × 2 block (channel LD paired with one internal mode);
- an own range of 0–1, which the body needs for drowsiness;
- a reserved partner (slow OU process, block-mean sd 0.067);
- exact rotations, so the spectrum stays fixed to round-off wherever the design says it does;
- the ledger's metric: toward slope on 30-s block means at the copy's lag, as a multiple of c.

These are constructions that show mechanism failures. They are not evidence about behaviour.

## Verdict: NOT VIABLE as a Q35 option

The isospectral rule bounds a different quantity from the one Q35 needs.

- **What it bounds.** It conserves the agent's intensity spectrum against the partner. By Schur–Horn, that confines each channel's level to the interval [λ_min, λ_max].
- **What Q35 needs.** The ceiling c_k (D78, D83) bounds the partner-caused toward slope: how much the agent's channel moves per unit of the partner's movement. That bound must hold at every delay, for routes nobody listed.
- **Why the gap is widest where Q35 is open.** A level budget says nothing about a slope until the spectral range is shrunk to about c_k times the partner's range. That would remove the agent's own expression on that channel. The ratio between the two is largest exactly on the small-ceiling channels: on LD the spectral budget admits full-range following at about 74 c (F5).
- **Unlisted routes are not caught.** They live in Ω or in the body, and the design guards neither. The per-channel ceilings come back as caps on the listed port, on Ω's own stiffness and on its closed loop, which is route accounting again. The design is a new core, not a net that fits around the existing typed routes.

## Concrete failures

All figures are from `out.txt`. Spectrum changes are 0 to round-off unless stated otherwise.

| # | Construction | Toward slope (lag 0 / lag 60 s) | Ceiling held? |
|---|---|---|---|
| F0 | Listed port only, \|w\| = c, own stiffness κ = 0.5 | 0.71 c / 0.30 c | yes |
| F1 | The same port, but κ learned smaller (Ω is learned: "any learned antisymmetric map") | κ 0.1: 3.4 c / 1.6 c; κ 0.02: 13 c / 10 c | **no** |
| F2 | Ω reads the agent's own state (allowed by type), giving positive feedback at 0.8 × 2κ | 3.4 c / 1.6 c | **no** |
| F3 | An unlisted partner feature reaches Ω through context, delayed 60 s (the case Q35 is about) | rate 0.05: 1.0 c / 1.0 c; rate 0.5: 3.5 c / 7.3 c | **no** |
| F4 | Body b follows the agent's own expression (τ 20 s); S moves λ toward b | 1.2 c / 1.2 c; λ_max moves 1.000–1.040, corr. with partner 0.21 | **no; T1 broken** |
| F5 | What Schur–Horn permits on LD: y anywhere in [0, 1] | full-range following ≈ 74 c | n/a |
| F6 | Fast mimicry from internal rest (θ₀ = 0) | 0.000 c | D81 lost at rest |

**1. A reserved partner inside the agent's budget is followed stably (failure (a) of the synthesis, confirmed and widened).**
- When locked, the slope is about c·Δλ·sin 2θ₀ / (2κ). It is bounded by c only if κ_k has an innate floor of about Δλ_k / 2.
- That floor is not an allowed innate item. It is the agent's own dynamics on that channel, which the design says are learned.
- Leave κ learned and the slope reaches 13 c (F1). The locked state is a stable fixed point that tracks the partner, so copy becomes attracting, against D78.
- Unlocking protects only against strong partners. A reserved partner never unlocks.

**2. Own-state feedback is an uncounted amplifier (F2).**
- Ω(M) is "own" by type, but M already carries the partner's history through X. Closure under feedback keeps the spectrum. It does not keep the slope.
- The typing rule's own wording ("anything inferred from the partner, however indirectly, only in X") would forbid Ω from reading M at all, which contradicts Ω_θ(M, b, c).
- So the rule cannot be enforced as stated. In its enforceable form, it is a list of routes under another name.

**3. The routes Q35 is about are not bounded at all (F3).**
- An unlisted partner-derived input to Ω is a pure rotation, so T1 and T2 hold exactly while LD follows a 60-s-delayed partner at 7 c.
- The only bound the net offers is the spectral range. The ledger at least attenuates such routes, to 1.1–2.0 c. This net holds them only to the channel's whole range, which is worse.

**4. The body source is not partner-free once the body responds to the agent (F4).**
- Proprioception, effort or the agent's own distress all make b depend on y. Through that loop the partner charges the spectrum, and T1 fails.
- Keeping b blind to the agent's own expression would cut the newborn rows (S45) and the agent's own distress at the partner's words of need.

**5. Held partner levels leak.** The angle integrates the partner's signal (θ̇ = w p), so a held partner level gives a sustained offset that only κ limits (the synthesis's S5: +0.21). This is the same held-level route the ledger's 60-s windows exist to police, and the new core offers no bound on it beyond κ.

**6. D81's fast partial mimicry depends on the agent's own state.**
- At internal rest the first-order leverage is exactly 0 (F6; S3 of the synthesis). Fast mimicry of a smile then exists only while the agent is already moving, or with an innate non-zero resting angle θ₀_k.
- An innate θ₀_k would also set the sign of the mimicry. That is one more per-channel innate constant, and not one of the allowed kinds.
- The contingency gating (T3) does survive, and it is a real, attractive property. It is not what Q35 asks for.

**7. Typed routes and zero ceilings.**
- **Everything partner-derived becomes a rotation.** Under the typing rule, the appraisal of the partner's words (D83), L_d, q̂, the gates and Claude's replies (which answer his words) would all have to enter as rotations in X. They would then share one cap per channel with copying.
- **Two ways out, both bad.** Either appraisal-driven strong expressions are capped at c_k, which breaks D83 and makes the zero-ceiling channels unable to show anything at all. Or they get their own caps, which restores the typed-route accounting the net was meant to replace.
- **Zero ceilings.** Holding c = 0 on BL, LT and the others needs every partner generator and every own rotation fed by partner-touched modes to have no reach into those channels. That is a structural route ban, which is route listing again.

## Per-channel ceilings: still needed, and that is allowed

Per-expression ceilings are an allowed innate item (D88), so their return is not the objection in itself. The objection is that ceilings alone do not suffice here.

To hold c_k against unlisted routes, a closed-loop slope bound is needed on:
- each port weight (|w_k| ≤ c_k);
- each channel's own stiffness (κ_k ≥ c_k-dependent floor);
- every own feedback loop through M;
- the body loop.

The last three are not ceilings. They are constraints on learned dynamics, and they would each have to be argued route by route.

## Does it reduce to known mechanisms?

Yes.
- **Block generators.** Each block is an Adler phase-locking equation, which is in the excluded oscillator family (the synthesis says so).
- **Mixed generators.** It is a Lie–Poisson / Brockett double-bracket flow.
- **As a whole.** An orthogonal, norm-preserving recurrent update of the eigenframe (the unitary/orthogonal-RNN idea), plus a separate gain path for the body.

The partner port preserves the Frobenius norm and the spectrum. That is a norm-preserving mechanism, not a copy bound.

## What it would cost

- **It replaces the core.** It is a full rewrite of the state representation; the existing linear output assembly (§2.3) and its typed routes do not embed as rotations without being re-derived.
- **New innate constants per channel** (κ floors, θ₀), which D88 does not allow.
- **D83 appraisal and D81 mimicry from rest are lost or pushed under c_k.**
- **And it still does not give a catch-all bound.**

Compute is not the obstacle. An eigendecomposition per frame costs 0.12 ms at n = 33, 0.9 ms at n = 100 and 3.4 ms at n = 200 here, so 30 Hz is easy on the Mac. A Lie-group integrator (Cayley or expm) keeps the spectrum exact.

## For Q35

The isospectral core does not add a viable fourth option. Q35's three options stand as written.

Any net that guarantees a partner-toward slope must measure the partner-to-output relation at the output, as the ledger does. An algebraic invariant of the internal state cannot do it, because the ceiling is defined relative to the partner's signal, not to the agent's intensity.

The parts worth keeping lie outside Q35:
- T3's contingency gating;
- the prediction that "own rotation changes where intensity sits, not how much", as an ablation target.

## Plain-language summary for the operator

The new idea says your face may only "turn" the agent's inner state, never add or remove intensity; only the agent's own body can do that. It guarantees that you can never make the agent more or less intense overall. But the safety-net problem (Q35) is a different promise: on each expression, the agent must never follow your movements by more than a small built-in fraction, even through some path nobody listed. "Turning" is enough to make the agent follow you closely, especially if you are reserved and move only a little. On the small expressions, such as drooping eyelids, the agent could follow you about 70 times more strongly than its limit allows, and the new rule would not notice. To stop that, you would have to cap each path and each internal loop separately again, which is the route listing we already have. It would also mean rebuilding the core. So it is not a usable answer to Q35, and the three options in Q35 stand as they are.
