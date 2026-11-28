# Searching for a new core mechanism, tenth pass: can the per-expression ceilings be built into the learned routes, so that they hold by design rather than by monitoring? (synthesis, 2026-11-28)

**Scope of this pass.** D93 left open the gap between the necessary per-channel bound (research/foundations/conjecture-five-passes.md, Theorem 1) and a sufficient one for nonlinear cores with memory (its O1). The scaled safety net (research/foundations/design-scaled-safety-net.md, revision 2; Q35, D99) measures and attenuates; its proved bound is loose (about 1–2 c plus a detection term), and slow (2–5 min), switched (6 min on, 24 off) and growing copies get through during its 70–220 s detection span. This pass reads the mathematics of incremental gain, contraction and Lipschitz-bounded recurrent maps and asks one question: can a **per-channel** incremental gain bound, from the partner-input path to each output channel k, at most a stated fraction of c_k, be **enforced by construction** on the build core's learned routes (design-cayley-ledger.md, revision 9.2)?

## Sources read (notes in research/)
| Note | Area | How fully |
|---|---|---|
| revay-manchester-2020-contracting-implicit-rnn.md | contracting RNNs with a free metric (convex set; penalty-enforced) | full text |
| boczar-lessard-recht-2015-exponential-iqc.md | exponentially weighted (ρ-) IQCs; discrete Megretski–Rantzer restated | §1–6 in full; appendix proofs not read |
| revay-wang-manchester-2020-lipschitz-bounded-equilibrium-networks.md | direct parameterisation of Lipschitz-bounded static equilibrium layers | §1–6 in full; appendix tables as extracted |
| wang-manchester-2023-sandwich-lipschitz-networks.md | complete, direct parameterisation of Lipschitz-bounded deep nets (sandwich layer) | §1–5 in full; appendices not read |
| pauli-2021-training-robust-nn-lipschitz.md | LipSDP counterexample; ADMM enforcement of a bound | full text |
| kozachkov-ennis-slotine-2022-rnns-of-rnns.md | contracting assemblies: hierarchy and skew feedback | main text and appendices A–B; proofs not read |
| martinelli-2023-noderen-dissipative-neural-odes.md | continuous-time RENs; discretisation caution | main text in full; appendix not read |

**Already in the index and used without re-reading as notes:** Lohmiller & Slotine 1998 (contraction), Revay, Wang & Manchester 2023 (RENs), Fazlyab et al. 2019 (LipSDP), Scherer 2022 (dissipativity and IQCs, standing in for Megretski & Rantzer 1997), Hughes 2021 (Willems), Sontag (ISS), whole-loop-bounds-synthesis.md, and the fibred attribution core with its critique. For one point (whether a robust REN can carry a contraction rate ᾱ < 1 together with its IQC) I re-opened the REN paper's Theorem 1 (LMI (16), whose top-left block is ᾱ²P), its appendix A and §V-B; nothing else of it was re-read.

**Not reachable from here** (nothing below rests on them):
- Angeli 2002, "A Lyapunov approach to incremental stability properties" (*IEEE TAC* 47(3)): not on arXiv; no open copy found. Cited only as Revay & Manchester 2020 cite it.
- Megretski & Rantzer 1997 (*IEEE TAC* 42(6)): lup.lub.lu.se refused by this session's network (403), as in the earlier pass; not on arXiv. Used only through Boczar et al.'s Theorem 2 and Scherer's Theorem 28.
- Pauli et al. on Lipschitz-bounded 1-D convolutional networks (2022, 2023) were not fetched; the 2021 paper was read instead.

**Checks.** `research/foundations/sims/new-core-search-10/check.py` (numpy only; `python3 -I check.py > out.txt`, a few minutes), output in `out.txt` there. **It checks algebra on synthetic signals. It is not evidence about people, behaviour or the engine.** Settings: 1 Hz, 1-h session, neutral input u⁰ = 0.30 while his mean is 0.44, block means of 10 s, final 20-min window (and every 20-min window in steps of 5 min), lags 0–300 s, floor σ₀ = 0.03, c = 0.05.

**Vocabulary.** No emotion labels or named emotion variables appear below the Claude layer. Channels are the build core's codes (LD lid droop, LP lip pull, CR cheek raise, BI inner brow, BO outer brow). "His counterpart" p_k is his same channel in the agent's coordinates. "T inputs" are his words, turn events and the agent's own words, held equal in the factual and shadow runs (rule 10). "Partner deviation" d = p − u⁰ is the difference between the factual and the shadow (neutral) input.

## What this pass adds (in short)
1. **Yes, a per-channel incremental gain bound can be built in**, for every parameter value learning can reach, and its incremental pair is exactly the shadow ledger's pair (factual run against neutral-face run with his words kept). Object and proof below (Proposition 1, 2).
2. **But an incremental gain bound is not the ledger's slope bound**, and the translation costs a factor Φ that depends on the metric and on an innate prefilter, not on learning (Proposition 3). Two nonlinear attack families make Φ large without a prefilter, and a band-pass prefilter removes both in the checks: a context sign aligned with his blocks multiplying his held offset from u⁰ (4.4–4.5 c → 0.00 c), and demodulation of fast movement that leaves his block means flat (1.33 c → 0.01 c).
3. **The pathwise reading of the metric (every window, every lag, floor σ₀) is not met by any gain bound, linear routes included.** A lag-aimed, non-stationary partner drives a plain linear copy of gain 0.5 c to 1.11–1.12 c at lag 300 s in a 20-min window (Observation 4). The D93 gap for the pathwise reading is therefore not about nonlinearity or memory; only output-side attenuation reaches that reading. In the long-window (stationary) reading of Theorem 2 the construction closes the gap up to the prefilter.

---

## 1. The object: a certified per-channel partner path

**Signals per frame (at the rate the block runs; Martinelli et al.'s caution: certify the discrete map actually executed).**
- e_t = F(d)_t ∈ ℝ^m: the partner deviation (all his face and voice channels, in the agent's coordinates) through an **innate linear prefilter** F, per input channel. Default here: F = LP(10 s) − LP(120 s), a band-pass that removes his held offset from u⁰ and movement within a 10-s block.
- z_t: context identical in both runs: T inputs, and own variables that do not depend on his face (or are computed inside the block, see §3).
- y_k: the partner-dependent part of output channel k from the learned routes.

**Construction (per channel k).**
- **Trunk.** A robust REN 𝓡^{(k)}_θ (Revay et al. 2023, direct parameterisation, θ ∈ ℝ^N) with input (W_k e, z), contraction rate ᾱ < 1, and the incremental IQC with Q = −I, S = 0, R = diag(I, ρ²I): the partner part of the input is weighted by W_k and the context part by an arbitrary ρ.
- **Input weighting.** W_k = diag(1 on his counterpart p_k, w_× on his other channels), w_× ≤ 1 innate (Theorem 2 of the conjecture prices cross inputs at a_i/(√2 σ₀) ≈ 7, so w_× ≈ 1/7).
- **Readout.** y_k = γ_k φ_k(h^{(k)}, z), with φ_k(·, z) 1-Lipschitz in h for every z: a sandwich network (Wang & Manchester 2023) or a norm-bounded row r_k(z)ᵀh with ‖r_k(z)‖ ≤ 1. The sign, shape and gating of r_k are free functions of z.
- **Sharing.** Several channels may share one trunk only at the most restrictive input weighting of the channels it feeds (§2 of the critique below). With per-channel trunks the bound is exactly per channel, with no joint budget across the face; Kozachkov et al.'s hierarchy rule keeps the assembly contracting.
- **Innate constants:** γ_k, W_k, ρ, ᾱ, F. Compiled into the map; not parameters.

### Proposition 1 (per-channel incremental bound, for every θ)
For every θ ∈ ℝ^N, every context history z, every pair of partner histories with deviations d and d′ = 0 (the shadow) and the same z, and every T:

  ‖Δy_k‖_{[0,T]} ≤ γ_k ‖W_k Δe‖_{[0,T]},  Δe = F d.

*Argument.* REN Theorem 3: every θ in the image of the direct parameterisation satisfies the IQC, so Σ_{t≤T} (γ̃²|W_kΔe_t|² + ρ²|Δz_t|² − |Δh_t|²) ≥ 0 with zero initial difference (both runs start the session from the same state). Δz = 0 because z is equal in both runs. φ_k is 1-Lipschitz in h for each fixed z_t, so |Δy_{k,t}| ≤ γ_k|Δh_t| pointwise. ∎ (The pairing of factual and shadow runs as the incremental pair, and the free weight ρ on T inputs, are my reading; they need nothing beyond REN Theorem 3.)

### Proposition 2 (window form, fading memory)
If the REN carries rate ᾱ < 1 (LMI (16) with ᾱ²P in the top-left block), then for every window [s, T]:

  ‖Δy_k‖²_{[s,T]} ≤ γ_k² ( ‖W_kΔe‖²_{[s,T]} + Σ_{t<s} ᾱ^{2(s−1−t)} |W_kΔe_t|² ).

*Argument (my derivation).* Pre- and post-multiplying (16) by the incremental vector gives V(Δx_{t+1}) ≤ ᾱ²V(Δx_t) + γ|Δe_t|² − γ⁻¹|Δy_t|² (absorbing γ_k into the IQC scaling). Drop the output term up to s to get V(Δx_s) ≤ γ Σ_{t<s} ᾱ^{2(s−1−t)}|Δe_t|²; telescope over [s, T] with ᾱ² ≤ 1 and V ≥ 0. This is the windowed reading of a ρ-IQC (Boczar et al., Definition 6 and Remark 10). ∎

### Proposition 3 (from energy to the ledger's slope: the factor Φ)
For the ledger's metric (block means of length b over a window of N blocks, lag L, floor σ₀), with D̃, P̃ the centred block means of Δy_k and of his counterpart at lag L:

  β_k(L) = ⟨D̃, P̃⟩ / max(‖P̃‖², N σ₀²) ≤ ‖Δy_k‖_{[s,T]} / ( √b · max(‖P̃‖, √N σ₀) ).

So CG(c_k) holds for this route whenever **γ_k Φ_k ≤ s_k c_k**, where s_k is the share of c_k left by the counted routes and

  Φ_k = sup over admissible paths of √(numerator of Prop. 2) / (√b · max(‖P̃‖, √N σ₀)).

Φ_k depends on F, W_k, ᾱ and the metric, **not on θ**: it is innate and computable once. Slopes add over routes (the metric is linear in Δy), so shares add.

*Argument.* Cauchy–Schwarz on the centred block means; ‖D̃‖ ≤ ‖D̄‖ ≤ ‖Δy‖_{[s,T]}/√b (block averaging); then Proposition 2. ∎

**What the check says about Φ** (Part A; upper bound by a generalised eigenvalue with the box relaxed to a ball, and a feasible path from the top eigenvector):

| prefilter F | memory 60 s, L = 0 | L = 120 s | L = 300 s |
|---|---|---|---|
| identity | ≤ 57.2, attained ≥ 22.5 | ≤ 57.2, ≥ 0.75 | ≤ 57.2, ≥ 1.11 |
| LP 10 s | ≤ 56.9, ≥ 18.7 | ≤ 55.7, ≥ 5.9 | ≤ 56.9, ≥ 8.4 |
| BP 10–120 s | ≤ 37.5, ≥ 1.97 | ≤ 45.6, ≥ 4.0 | ≤ 47.6, ≥ 5.1 |
| cross-channel input (his counterpart held at the floor) | ≤ 34–40 | | |

Read plainly: the Cauchy–Schwarz route gives a sufficient condition that is useless pathwise (γ_k ≤ c_k/40). Its size comes from the floor σ₀: a partner can hold his counterpart's block means at the floor while putting large energy where the regressor does not look (inside blocks, in his offset from u⁰, at other lags, on other channels). Without a prefilter at least 22.5 is attained at L = 0, which is the a/σ₀ scale (0.70/0.03 ≈ 23).

**What the check says about routes** (Part B; toy routes certified by construction at gain γ = c: one-pole stages with ℓ₂ gain ≤ 1, a 1-Lipschitz rectifier, own-context multipliers bounded by 1; worst slope / c over lags 0–300 s and every 20-min window):

| route | identity F (natural / floor-aimed / wiggle partner) | BP 10–120 s |
|---|---|---|
| copy, 5 s | 0.97 / 0.84 / 0.91 | 0.76 / 0.65 / 0.66 |
| slow copy, ≈ 120 s late | 0.70 / 0.18 / 0.19 | 0.44 / 0.15 / 0.15 |
| switched copy, 6 min on / 24 off | 0.92 / 0.44 / 0.46 | 0.32 / 0.20 / 0.20 |
| growing copy (own context ramp 0 → 1) | 0.87 / 0.67 / 0.72 | 0.57 / 0.55 / 0.55 |
| demodulator (envelope of |e|) | 0.83 / 0.56 / **1.33** | 0.19 / 0.00 / 0.01 |
| own-context sign aligned with his blocks | 0.78 / **4.39** / **4.52** | 0.23 / 0.00 / 0.00 |

The two bold failures are the nonlinear-with-memory mechanisms behind O1: the context sign multiplies his held offset (u⁰ ≠ his mean; factor ≈ 0.14/0.03), and the rectifier turns block-invisible movement into a block-level output. The band-pass removes both in these runs. Slow, switched and growing copies inside the block stay below c at all times: there is no detection span, because nothing is detected.

### Observation 4 (the pathwise reading is out of reach of any gain bound)
Let him be flat except for a ±σ₀ block pattern during [T − 2L, T − L] and the same pattern at amplitude A during [T − L, T]. Then a route that follows him at lag about 0 with gain g reads, at lag L in a window of length W,

  β(L) ≈ g · (L/W) · (A/σ₀),

because the regressor (his face L seconds earlier) sits at the floor while the route answers his present movement. Part C, a plain linear copy with g = 0.5 c, W = 20 min: 1.11–1.12 c at L = 300 s, A = 0.30 (predicted 1.25 c); 0.44–0.46 c at L = 120 s; with the band-pass 0.19 c (10-s pattern) and 0.69 c (60-s pattern) at L = 300 s. Shorter windows make it worse (with W ≤ L, β ≈ g·A/σ₀ ≈ 10 g).

So under "every window, every lag, every partner path", no gain bound short of g ≈ c σ₀W/(A L) suffices even for a linear time-invariant route. This bears on two existing statements:
- conjecture-five-passes.md O1: for the pathwise reading the gap between necessary and sufficient is not specific to nonlinear cores with memory; Theorem 2's exact equivalence uses long windows and stationary inputs, and it does not extend to finite windows with a lag scan.
- design-cayley-ledger.md §2.13 says "a sup-gain bound holds at every lag". That holds in the stationary long-window reading; pathwise it does not (Part C). The build core already states that for an extreme partner the ledger may trim the counted routes; Observation 4 is one such partner, and the ledger's attenuation, not the routes' gains, is what holds the ceiling there.

---

## 2. Answer to (1): can a per-channel bound be built into a recurrent parameterisation?

**Yes, in the incremental-energy sense, exactly and for every θ** (Propositions 1–2), by per-channel robust RENs (or a shared trunk at the cross weight) with 1-Lipschitz readouts and the shadow pair as the incremental pair. A block-structured supply rate on one shared REN (m simultaneous IQCs, one per channel, each with its own input weighting) is not available as a direct parameterisation (the direct parameterisation takes one (Q, S, R); whole-loop-bounds-synthesis.md, open problem 3). The structural route (per-channel trunks, or trunk plus norm-bounded rows) gives the same per-channel bound without it.

**As the ledger's slope ceiling:**
- **Long-window, stationary reading (Theorem 2's):** yes, with γ_k ≈ s_k c_k for his counterpart through the band-pass and γ_k w_× priced at the Theorem 2 weight for his other channels. Checkable: Proposition 3 with Φ computed in that reading (Theorem 2's spectral argument applies to the band-passed input of a contracting map whose memory is shorter than the window).
- **Pathwise reading (every 20-min window, every lag to 300 s):** no; not for any gain-bounded route (Observation 4). The honest sufficient condition is γ_k ≤ s_k c_k/Φ_k with Φ_k ≈ 20–50 from Part A, which would make the learned routes nearly mute.

**Checkable proof sketch** for a given build: (i) the code graph shows every value derived from his face reaching channel k only through 𝓡^{(k)} (a type or taint check; the build core already type-checks routes); (ii) each 𝓡^{(k)} is constructed by the direct parameterisation with the innate (γ_k, W_k, ρ, ᾱ), at the rate it runs; (iii) the readouts are sandwich layers or norm-bounded rows; (iv) the counted routes' shares plus s_k sum to at most 1; (v) Φ_k is computed once for the metric reading adopted; (vi) an adversarial-pair lower bound is reported at fit time (LBEN and sandwich report 40–99.9 % tightness).

## 3. Answer to (2): what it costs

- **Gain budget.** The learned routes get only the share s_k that the counted routes leave (they already take up to 0.974 c_k). On small-ceiling channels (LD c = 0.05) a 0.2 share is a certified gain of 0.01 per unit of his band-passed movement.
- **What the learned routes may see of him.** Only band-passed deviations (between about 10 s and 2 min) of his face and voice, and T inputs. His held level reaches the face only through the counted linear held cone (≤ 0.22 c). Context-dependent responses to his held face (a response that deepens because he has held a face for ten minutes) can then come only from his words, from the cone, or from cross-session learning.
- **No partner-writable persistence inside the block.** Contraction gives one driven trajectory per input history (so copy never attracts and the copy defect is ≥ 1 − γ_k), but it excludes partner-switchable multistable states. Persistent affect written by his face has infinite incremental gain (whole-loop-bounds-synthesis.md, open problem 1; the fibred core's critique, K3). Persistence must be written only by own variables or T inputs.
- **Q18.** Per expression: yes (one certified block per channel). Set by context and the learned relationship: the readout r_k(z) and the trunk's context input are free functions of z, and ω (fixed within a session) is a parameter. Flip sign: yes, r_k(z) may take either sign; the bound is on magnitude. Under an innate ceiling: γ_k is compiled in. Copy never a settled state: contraction. **The catch:** context that itself depends on his face (the agent's own body state while he is present, the gate g's traces of his masked face) differs between the two runs, so it must be computed inside the certified interconnection, and its effect is charged by the product rule |Δ(r(z)h)| ≤ |r||Δh| + Lip(r)·|h|_max·|Δz|.
- **Learning.** Every θ ∈ ℝ^N is certified, so nightly replay can never raise a gain above γ_k, on any night. Within a session the build core learns states only, which is the case the certificate covers exactly. **Online learning of parameters from his face within a session breaks it:** if the shadow runs its own learner, Δy contains R_θ(u) − R_θ′(u⁰), a difference of two maps that no incremental bound controls; if the shadow uses the factual θ (as rule 10 does for the gates), the learning route is invisible to the ledger. The fix is to freeze within sessions or to put the learner inside the certified state as a contracting (forgetting) update. Switching between certified θs with different metrics is not covered (Kozachkov et al.'s constant-metric limitation).
- **Accuracy.** REN Table I: NRMSE 16 % → 30 % at a tight bound on F16; LBEN and Pauli et al.: an order-of-magnitude lower bound for ≤ 0.2 points of accuracy on images; sandwich layers use 94–99.9 % of the certified bound. None of this is about expression routes.
- **Engineering.** Diagonal multipliers only (Pauli et al.; Wang & Manchester, Remark 2.2); the repo's LipSDP note needs that correction. Certify the discrete map at the rate it runs (Martinelli et al.). About 33 small RENs, cheap on the Mac.

## 4. Answer to (3): does it close the D93 gap and the Q35 edge cases?

- **D93 / O1.** For cores whose partner dependence passes through an innate band-pass and certified per-channel blocks, the gap closes in the long-window reading: necessity (Theorem 1) and sufficiency (Proposition 3) meet up to a computable factor. For the pathwise reading the gap is reframed rather than closed: Observation 4 shows that no gain bound meets it for any core, linear or not, so in that reading only output-side attenuation works. The conjecture's O1 should say so.
- **Q35's edge cases, for learned routes inside the block: closed.** Slow, switched and growing copies are failures of detection, and a certified block detects nothing; its bound holds from the first frame (Part B: switched ≤ 0.32 c, slow ≤ 0.44 c, growing ≤ 0.57 c at γ = c with the band-pass). Growth across nights is impossible above γ_k.
- **Q35 proper (routes nobody listed): not closed by the construction itself.** A route outside the block is outside the proof. The construction helps when combined with Q35's first option, a type rule making it impossible for any value derived from his face to reach the face except through certified blocks; then an unlisted route is an implementation error, and the ledger or governor becomes a monitor for errors and for the pathwise reading.
- **What remains outside:**
  - Claude's word route (his words are kept in the neutral run; outside the ledger by design, D93);
  - the T-only learned displays L_d and q̂ (frozen, causal slope 0 on his face; their correlation with his face through his words is F23);
  - cross-session level shifts through nightly learning (R_θ(u⁰) changes; outside the within-session metric, audit S23);
  - partner-writable events or persistent states (counted in bits, not gain);
  - the echo gate g, whose traces read his masked face: it is a partner-dependent multiplier and must move inside the block or be charged by the product rule (today it is declared at ≤ 0.31–0.53 c and policed);
  - the pathwise reading of the metric (Observation 4), for which the ledger's attenuation stays necessary.

## 5. Answer to (4): novelty
**Recombination.** RENs, LBEN and sandwich direct parameterisations, ρ-IQCs and Willems/Scherer composition are existing machinery. whole-loop-bounds-synthesis.md (2026-11-26) already proposed a robust REN with diagonal output weights, and the fibred attribution core built one; its critique found the REN part sound and the failures elsewhere (base, events, held levels). What this pass adds is three applications:
- the shadow pair used as the incremental pair, with T inputs at a free weight;
- the band-pass prefilter as the general fix for the two nonlinear attack families;
- Observation 4 about the metric.
None of these is a new core.

## Products
1. **A Q35 note (recommended)**: for the learned, nonlinear routes, per-channel certified blocks would make the ceilings hold by construction in the long-window reading and remove the slow, switched and growing edge cases for those routes; together with a type rule this narrows "unlisted routes" to implementation errors. The ledger stays, for the pathwise reading and as a monitor.
2. **A note for conjecture-five-passes.md O1 and for design-cayley-ledger.md §2.13**: Observation 4 (the pathwise metric is beaten by a lag-aimed partner even for linear routes; "a sup-gain bound holds at every lag" holds only in the stationary reading).
3. **A correction for fazlyab-2019-lipsdp.md**: the coupled-multiplier variant is invalid (Pauli et al.).
4. **No designs.md line**: this is a constraint layer for the build core's learned routes, not a design. It earns a line only if the parent turns it into a revision of the build core and it survives a critique.

## Next steps
1. Decide which reading of CG the ceilings promise: long-window (by construction) or pathwise (needs attenuation). Observation 4 means the answer changes what "by design" can mean. The decision is the operator's (Q35).
2. If the construction is adopted, list the build core's partner-dependent learned and nonlinear routes (gate g with its traces, appraisal bases, the per-person readers on the path to the face) and check, route by route, whether each can be moved inside a certified block with the band-pass prefilter. That is a design task, followed by a critique.
3. Compute Φ_k exactly in the long-window reading (a spectral argument as in Theorem 2) for the band-pass and the build core's windows, and check Part B's attack families against a REN built by the direct parameterisation rather than the toy chain.
