# Whole-loop bounds: one certificate over all routes from partner to face (synthesis)

Written 2026-11-26 from six notes:
- scherer-2022-dissipativity-iqc.md (IQC and dissipativity; carries the Megretski–Rantzer theorem);
- hughes-2021-willems-dissipativity-retrospective.md (Willems 1972);
- revay-2023-recurrent-equilibrium-networks.md;
- fazlyab-2019-lipsdp.md;
- tatikonda-2009-feedback-capacity-directed-information.md (carries Massey 1990);
- wan-2025-information-limits-feedback.md (carries Martins & Dahleh 2008).

The primary texts of Megretski–Rantzer, Willems, Massey and Martins–Dahleh were not reachable from this session. Each is cited only through the restatement named.

## The problem in one sentence
Every design so far blocks the direct partner-face → agent-face route and caps other routes one at a time. Each critique then found an uncounted route that brought copying back:
- critique 3 (partner regulator): the care loop's slope; the clip bounded a value, not a Jacobian (X2: loop gain 0.88 → 120);
- critique 2 (reverse appraisal): a shared variance scale (X3: defect 0.000);
- manifolds critique: content-layer events, and event-rate integration (C3).

D78 asks for a ceiling per channel that no single quantity, and no learning, can push to copy.

## Which result best gives a per-channel, innate, learning-proof ceiling over all routes

**The robust recurrent equilibrium network (Revay, Wang & Manchester 2023), with a diagonally weighted incremental IQC, framed and composed by Willems/Scherer dissipativity.**

Reasons, in order:
1. **All routes at once.** An incremental IQC bounds the response of the *whole map* to differences in partner input, through every internal path, loop and shared estimate. Scherer's Theorem 15 and Willems' Theorem 5 are the same statement for interconnections: sum the dissipation inequalities, and internal supplies cancel. No enumeration of routes is needed. The burden moves to one checkable question: is every partner-dependent signal inside the certified block?
2. **Per channel.** Use the weighted Lipschitz form (REN Remark 1) with output weight W₁ = diag(1/c₁, …, 1/c_m). Then ‖Δy_i‖ ≤ c_i‖W₂Δu‖ holds for each expression channel i, against the *whole* partner input. It also gives a joint budget Σ_i‖Δy_i‖²/c_i² ≤ ‖W₂Δu‖², which is stronger than separate caps. Dynamic weights allow time-scale-dependent ceilings: fast onset echo above sustained matching.
3. **Innate and learning-proof.** The direct parameterization maps all of R^N onto models that satisfy the IQC. The constants (c_i, W₂) are compiled into the map and are not parameters, so no gradient step, replay or consolidation can exceed them. LipSDP (Fazlyab) shows why per-route products and sums are the wrong accounting, but it only certifies after the fact. RENs certify by construction.
4. **Copy non-attracting.** A contracting map has one driven trajectory per input history, so there are no pitchforks and no bistable copy state. With c_i < 1 that trajectory is never a copy: copy defect ≥ 1 − c_i on channel i. Copy lies outside the image of the parameterization, so learning cannot be attracted to it. (The *ceiling corner* can still attract learning. D78 accepts that only because the ceiling is real, and here it is.)
5. **Sign flips and context are untouched.** The IQC bounds magnitude of incremental response only. Sign, gating by the agent's own drives and per-relationship shape are free inside the ceiling.

**The information-theoretic results (directed information, feedback capacity) are a second, complementary ceiling, not the main one.**
- They bound the bits about the partner that any route can carry: an innate noisy perceptual channel of capacity C_i, then by rate–distortion a copy-defect floor 2^{−2C_i}.
- They are sign-blind and loose for slow expressions.
- Their unique value is for the routes a gain bound cannot certify: discrete content events, Claude's text, and partner influence on persistent multistable states.

The Martins–Dahleh floor adds a diagnosis: a loop that *regulates* the agent through the partner must carry partner information at the rate of the instability it regulates. That is why regulator designs leak.

## Sketch of the theorem a design would state

Notation:
- u = the partner's perceived expression channels, normalised by an innate W₂;
- z = the agent's own variables (drives, persistent affective states, relationship code), declared as non-partner inputs;
- y = the agent's expression channels (face synergies, voice prosody);
- e = discrete content events from Claude or appraisal heads that read the partner.

**Architecture constraint (A).** Every map from u to y is a single robust REN 𝓡_θ(u, z, e) with the incremental IQC Q = −W₁ᵀW₁ (W₁ = diag(1/c_i)), R = W₂ᵀW₂, S = 0, compiled with the direct parameterization. θ ranges over all of R^N.

**Port constraints (P).**
- (P1) z is not written by u: any z-update that reads u is inside 𝓡. Persistent multistable states read only the agent's own variables, or else (P3) applies.
- (P2) e reaches 𝓡 through a discrete channel of innate capacity C_e bits/s.
- (P3) Any partner-driven update of a persistent state passes through a channel of innate capacity C_z.

**Theorem (claim to prove for a given design).** For all θ ∈ R^N, all agent histories z, and all pairs of partner histories u, v with the same e:
1. ‖y_i(u) − y_i(v)‖₂ ≤ c_i‖W₂(u − v)‖₂ for each channel i; and Σ_i c_i⁻²‖y_i(u) − y_i(v)‖² ≤ ‖W₂(u − v)‖².
2. Hence the copy defect on any channel is ≥ 1 − c_i, and on the whole face ≥ 1 − max_i c_i.
3. 𝓡_θ is contracting, so the dyad closed through any partner whose incremental mimicry gain g_p satisfies max_i c_i·g_p < 1 is contracting. No self-sustaining matched state exists. (With g_p ≤ 1 this needs only c_i < 1. But the gain from the partner's *own exogenous* expression to the agent's face, around the loop, is c_i/(1 − c_i g_p). Keeping that below 1 needs c_i ≤ 1/(1 + g_p), which is ½ for a partner who mimics fully. This is the same ½ the reverse-appraisal design chose by hand; my derivation, small gain.)
4. Through e and z, the directed information from u to y over the routes outside 𝓡 is ≤ (C_e + C_z)·T, and the copy-defect floor on those routes follows by rate–distortion.

Items 1–3 follow from REN Theorem 3, Remark 1 and small gain. Item 4 follows from the data-processing and converse results of Tatikonda & Mitter. The design-specific work is to prove (A) and (P): that the code graph puts every partner-dependent signal inside 𝓡 or behind a counted channel.

## Open problems
1. **Persistence against contraction.** Contraction excludes the multistable, hysteretic states the cycle wants (staircase manifolds; Jung 2020; Lee 2014). A partner-switchable bistable state has *infinite* incremental ℓ₂ gain: a finite kick makes a permanent difference. So persistence must either have no partner write port (the Jung "loop property, no write port" reading) or be bounded in bits, not gain. Composing a gain certificate with a bit budget into one copy-defect bound is not standard. I found no source that does it.
2. **Amplitude, not energy.** Face ceilings are naturally peak amplitudes, not ℓ₂ energies. Energy-to-peak and peak-to-peak incremental bounds exist in Scherer's framework (amplitude bounds, Figs. 4–5), but not as a direct REN parameterization.
3. **Several IQCs at once.** A design may want a per-channel ceiling *and* incremental passivity on some channels. Direct parameterization handles one (Q, S, R). Intersections need the convex LMI form, which cannot be enforced at scale during learning.
4. **The partner's IQC is empirical.** Item 3 of the theorem needs a bound g_p on human incremental mimicry gain. The mimicry syntheses suggest it is small and context-gated, but no number is established here.
5. **Expressivity cost.** REN Table I: a tight γ costs accuracy (NRMSE 16% → 30% at γ = 10 on F16). Whether c_i < 1 leaves enough room for rich responsive expression must be measured, not assumed.
6. **Novelty.** Everything here is existing robust-control and information-theoretic machinery, excluded as a core. The proposal is to use it only as the **constraint layer** a new core is built inside: "the core's partner path is a certified REN with innate weights". Whether a new core can live inside that layer and still produce the shape-changing, sign-flipping mimicry of gap 6 is the real open question.
