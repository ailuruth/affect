# Commutator coupling: the partner reaches the agent's state only through same-channel Lévy-area commutators with the agent's own autonomous motion, on a dyadic tree of time windows

Written 2026-11-26 by a design-author subagent, from research/new-core-search-synthesis.md Direction 1 (with Direction 2 as its normaliser), after reading Morrill et al. 2021 in full (research/morrill-2021-neural-rde.md). Standard: Q17 as relaxed by Q19/D80 (a precise object and a convincing argument per key property; concrete failures matter, not rigor). Rules in force: D78 (refined copy rule), D81 (know fully, bound only expression), D83 (innate per-expression ceilings; strong expressions through the agent's own appraisal), D84 (subscription), D85 (three sources of situational appropriateness). **Not yet critiqued.**

Numerical checks of the mathematics only (not evidence): research/foundations/sims/design-cc/checks.py, output in out.txt (C1–C9, 2.2 min on one CPU).

---

## 0. Summary

- **The object.** For each expression channel k, pair the agent's own *autonomous* channel a_k (its face as it would be had the partner's face and voice held still) with the partner's channel x_k, read into the agent's own coordinates. On a dyadic tree of time windows, every completed node emits one commutator, ½(Δa^L Δx^R − Δx^L Δa^R): the Lie-bracket coefficient that the node's split adds to the Lévy area. Divide it by the product of the two parties' motion over the node (a divisive pool) to get ρ_kj ∈ (−1, 1). A multiscale neural CDE z is driven by the agent's own path and by these ρ's, and by nothing else of the partner's face or voice except through the agent's own body (his face → the agent's own appraisal → its six body variables).
- **What the algebra gives, for every parameter value.** ρ is zero on any zero-lag affine copy (gain, offset or sign), on a lagged *ramp*, and when either party holds still; it is swap- and time-reversal-antisymmetric; it is bounded and scale-free; the tree's commutators sum exactly to the window's Lévy area, so lead–lag is decomposed by time scale. Scales 1–24 run from 67 ms to 155 h of contact.
- **What the algebra does not give, stated.** (a) The commutators are not information-poor: with the own path known, the tree determines the partner's motion up to adding a multiple of the agent's own motion (C4). Copy is removed from the *cheap* functions of the core (Kidger Thm C.1's constant field), not from its class. (b) Copying is not made "unattractive" by the input being zero on the copy set: a commutator is a phase detector, and a loop that feeds the agent's *rendered* face back into ρ locks onto the partner like a phase-locked loop (C7: lagged correlation 0.999). Hence the own side is the autonomous (efference) path, and the hard ceiling comes from a second element.
- **The ceiling.** Per-channel counterfactual runs (his channel k held at his baseline, everything else live) give the exact causal part of the agent's channel k that his channel k caused; an all-held run gives the part his whole face and voice caused. Each part passes an attenuate-only limiter whose statistic is the node's 2×2 cross-matrix of (first-half, second-half) increments. Its trace is the in-phase co-variation, its antisymmetric part is the commutator. Their hypotenuse is a phase-invariant coherent gain, scanned over lags 0–60 s and octaves 1–11 plus a broadband stage, and capped at the innate per-channel ceiling (smile 0.35; all routes 0.55; zero on 13 channels).
- **Failure (1), a quarter-period lag.** The area is maximal there (−π r_s r_p sin φ, C3), and the design uses it: it is knowing (who leads at which scale). It cannot become a copy route through any of the three mechanisms found: closed-loop lock (removed by the efference own side), heterodyne mixing (C7: 0.50 before the limiter, 0.25–0.27 after) or reconstruction (C4), because the limiter counts the quadrature part exactly as the in-phase part. Constructed lagged copies at 0.9 s, 2.5 s and 20 s at gain 1 come out at 0.27, 0.27 and 0.26 (C6). A phase-only limiter leaks 0.58, 0.79 and 0.94, so lag-completeness is what does it.
- **Failure (2), the fast partial echo.** It is the Cayley-ledger fast gear, reused: frozen innate gains G_k (lip pull 0.224, laugh burst 0.280), the onset lobe, the word-waiting gate (0.8–1.0 s on smile and laugh), times a per-channel, sign-flippable strength m_k(z) ∈ [−γ_k, 1] set by the core's relationship state. It runs channel k from flat to at most G_k ≤ c_k, never to copy. It does not feed the core's own side, so it cannot lock. The limiter does not bind on it alone (C6: 0.154 → 0.152, rms 0.99).
- **Novelty verdict, plainly: recombination.** The core is a depth-2 neural RDE (Morrill et al. 2021) on (own path, partner path) with the partner's level-1 and cross-channel bracket columns masked, a normalised same-channel bracket, all dyadic step sizes at once, and an efference own side. A neural CDE/RDE with structure bolted on. The ceiling is the Cayley-ledger shadow ledger made causal per channel, phase-complete and lag-complete. No new core mechanism.

---

## 1. Plain-language intuition

When two people talk, their faces move. Some of the agent's movements come first and his follow; sometimes the reverse. "Who moved first, on which expression, over which stretch of time" is a rich description of a relationship. It holds no copy of either face.

Take one expression, say the lip-corner pull. Draw a curve with the agent's own lip pull on one axis and his on the other, as the conversation runs.
- If the agent copies him exactly, the curve is a straight line, and it encloses no area.
- If either of them holds still, the curve is a line again: no area.
- If the agent's smile tends to come first and his follows, the curve loops one way and the signed area is positive. If his comes first, the area is negative.

The signed area is the Lévy area. It is the one quantity of two paths that is zero for every copy and every hold, and whose sign says who led.

Cut time into halves, quarters, eighths and so on down to single frames. The area over a long stretch is exactly the sum of one small "commutator" per cut. Each commutator says who led in that piece at that size. So one exact bookkeeping gives who-leads-whom at 0.1 s (a brow flash), 1 s (a returned smile), 10 s (a turn), 5 minutes (a topic), and weeks (the relationship).

The agent's inner state is a learned continuous-time network fed by:
- its own face, voice, body and words;
- these commutators, one per expression and per time scale;
- what its own body felt on seeing his face (its own appraisal of him, through its own inverted expression model).

It never sees his raw face movement as an input it could simply pass through.

Two honest limits shape the rest of the design.
- **The commutators know a lot.** Given its own movements, the agent can reconstruct his from them, apart from the part that moves like its own. Knowing is allowed (D81).
- **A commutator is a phase detector.** If the agent fed its own *rendered* face into the commutator, a learned loop could lock onto him like a phase-locked loop and copy him. So:
  - the "own" side of every commutator is the face the agent would have made had he held still: its efference, not its perceived output (Bahrick & Watson);
  - every path from the state to the face passes a limiter. The limiter measures how coherently the agent's partner-caused movement follows his, at every lag and time scale, and caps it per expression.

The same little 2×2 matrix per time window gives both: its antisymmetric part is "who led" (fed to the state), and its full size is "how much did I follow" (capped).

---

## 2. The object

### 2.1 Spaces, channels and constants

- **Time.** Discrete at the camera rate f_s = 30 Hz, h₀ = 1/30 s, counted in **contact time**: frames advance the tree only while the partner is present (face tracked or voice active). Partial nodes stay open across sessions.
- **Channels.** The m = 33 counterpart channels of the Cayley-ledger design (revision 6 §2.1): smile (LP, CR), laughter (BU_L, RHY, BRE), sympathy group (BI, BO, LD, JO), head and gaze (HP, VG, yaw, tilt, horizontal gaze), phrase-level voice (F0 level, F0 range, energy, rate, pause, latency), and the 13 zero-ceiling channels (BL, UL, LT, NW, LS, CHR, LPR, DIM, funnel, pucker, mouth close, lip roll, sob burst BU_S). Every channel is normalised to its innate range [0, 1] (signed channels [−1, 1]).
- **The partner's channel** x_k(t): his face and voice in the agent's own coordinates. MediaPipe → P₀ → reflection, then the per-identity calibration x̃ = ref + (x − b^read_id)·σ_ref/max(σ_id, 0.25 σ_ref) (Cayley revision 6 §2.1, reused unchanged).
- **The agent's own autonomous channel** a_k(t): channel k of the all-held counterfactual run S⁰ (§2.2).
- **Own body** b ∈ R⁶: the Cayley-ledger body variables (E, A, V, K_id, P, I) with their set points, dead-bands and satiable drive 𝒟(b) = Σ_i w_i ψ(|b_i − b_i*| − δ_i)₊, ψ(x) = x² (Cayley revision 5 §2.1, unchanged).

**Innate constants (compiled in; not parameters).**

| Symbol | Value | Meaning |
|---|---|---|
| J | 24 | tree depth; node at scale j spans 2^j frames (j = 1: 67 ms … j = 24: 155 h of contact) |
| ν_k^a, ν_k^x | per-frame increment noise SD of the agent's renderer at rest and of the tracker on a still face (week 0, own data and a still mannequin) | noise floors |
| ε_kj | ν_k^a ν_k^x 2^j | semi-saturation of the divisive pool (diffusive scaling of increment noise) |
| κ_τ | 4 | leak of block j: Λ_j = 1/(κ_τ 2^j h₀) |
| η | 0.25 | elementwise bound of each commutator vector field column (tanh) |
| k_sel | 8 | number of (channel, scale) cells the need-conditioned selection may read at once |
| c_k (same-channel ceiling, D83) | the Cayley table: LP 0.35, CR 0.25, BU_L 0.35, RHY 0.30, BRE 0.15, BI 0.20, BO 0.10, LD 0.05, JO 0.10, HP 0.10, VG 0.05, lateral 0.03, voice 0.05–0.10; 0 on the 13 zero channels | ceiling on his channel k → the agent's channel k, all routes |
| a_k (appraisal allowance) | LP 0.20, CR 0.15, BU_L 0.15, RHY 0.10, BRE 0.05, BI 0.25, BO 0.15, LD 0.15, JO 0.05, head, gaze and voice 0.05; 0 on the 13 zero channels | extra room for his *other* channels moving the agent's channel k through its own appraisal |
| c_k^tot | c_k + a_k (max 0.55, LP) | ceiling on everything his face and voice cause on the agent's channel k, toward his channel k |
| margin | 0.85 | the limiter targets c·0.85 |
| L_max | 60 s | longest lag scanned |
| G_k, δ_g, the gate, P_c and the posture rules | Cayley revision 8.3 (§2.1, §2.4, §2.10 there) | reused verbatim |
| γ_k (echo sign range) | 0.25 on smile and laughter, 1.0 on BI, BO, LD (brow relaxation and countering), 0.5 elsewhere | how far the echo strength may go negative |

### 2.2 The counterfactual runs and the own side

The engine runs one factual copy and 34 counterfactual copies of the core with the same parameters and the same own inputs.
- **S⁰ (all-held).** His face and voice channels are replaced by his reading baseline b^read_id (his usual face, latched per session; Cayley). His words, turn events, the agent's own words and body inputs, the concern posture and the word gate are kept at their factual values (Cayley rule 10, shadow equality). In S⁰ his channels are constant, so **every commutator is exactly 0** by property P2 below: no special case is needed for "neutral".
- **S^k (one per channel, k = 1…33).** Only his channel k is held at b^read_id,k; everything else is live. In S^k, ρ_kj ≡ 0 for all j, and the appraisal sees his channel k at baseline.
- **The own side.** a_k := s_k^{S⁰}, the agent's channel k in S⁰. It contains everything the agent does on its own account (body, its own and his words, its Claude-written replies, visemes, the posture), and nothing that his face or voice did to it through the echo, the core or the body route.
  - Why: Bahrick & Watson 1985 (research/bahrick-watson-1985-proprioceptive-visual-contingency.md): contingency is detected between felt motor output and seen motion, and "contingency should be computed from the engine's motor commands … not from its own perceived output".
  - C7 shows what happens otherwise: a loop on the rendered face locks onto the partner.
- **Partner-caused parts.**
  - δ_k := s_k − s_k^{S⁰}: everything his face and voice did to channel k.
  - δ_k^{(k)} := s_k − s_k^{S^k}: what his channel k did to the agent's channel k, by any route (exact, not estimated, because the core is the agent's own program).
  - δ_k − δ_k^{(k)} = s_k^{S^k} − s_k^{S⁰}: what his *other* channels did to the agent's channel k (the appraisal and proxies).

### 2.3 The dyadic tree and the commutators  ⟵ new mechanism (with 2.4–2.5)

For each channel k and scale j ∈ {1…24}, node i spans frames [i·2^j, (i+1)·2^j) with halves L and R of 2^{j−1} frames. When the node completes, it emits:

  Δa^L, Δa^R, Δx^L, Δx^R (half-window increments),
  c_kj^{(i)} = ½ (Δa^L Δx^R − Δx^L Δa^R).

- **Exact decomposition (Chen's identity at step 2, derived in the synthesis).** For the piecewise-linear path through the frames, the Lévy area of (a_k, x_k) over any root window equals the sum of c over all its descendant nodes (leaves add nothing). C1: 4,096-step random path, direct area and tree sum agree to 0.
- **Haar form.** With s = Δ^L + Δ^R (node increment) and d = Δ^R − Δ^L (Haar detail), c = ¼(s_a d_x − d_a s_x): one party's trend against the other's curvature.
- **The node matrix.** v_a = (Δa^L, Δa^R), v_x = (Δx^L, Δx^R), M = v_a v_xᵀ.
  - Its antisymmetric part is c (C12 − C21 = 2c).
  - Its trace is the in-phase co-variation Δa^L Δx^L + Δa^R Δx^R.
  - For a sinusoid with period 2·(node length), v is an exact quadrature pair, so a lag φ rotates v_a against v_x by φ. The averaged M then has trace ∝ cos φ and antisymmetric part ∝ sin φ (derived in §3.5). That is why one matrix serves both the core (antisymmetric part) and the limiter (its size).

### 2.4 Divisive normalisation

  ρ_kj^{(i)} = c_kj^{(i)} / ( ε_kj + ½ ‖v_a‖₁ ‖v_x‖₁ ).

This is Carandini & Heeger's eq. 9 form, with a pool equal to the product of the two parties' motion over the node.
- |c| ≤ ½(|Δa^L||Δx^R| + |Δx^L||Δa^R|) ≤ ½‖v_a‖₁‖v_x‖₁, so |ρ| < 1 always (C2: max 0.958 on random paths).
- Well above the floor, ρ is invariant to rescaling either party separately (C2: median change 1.8·10⁻³ when the agent's motion is ×5 and his ×2). Near the floor, ρ shrinks to 0: tracker jitter on a still face gives nothing.
- **Held drive.** Between completions, scale j holds its last value: ρ̄_kj(t) = ρ_kj^{(last completed)}. So the drive per unit time from one (k, j) cell is at most 1, whatever his burst rate or amplitude (C8: mean |ρ| at j = 9 is 0.16, 0.26 and 0.18 at burst rates 4, 16 and 64/min; 0.05 at a tenth of the amplitude).

### 2.5 The core: a multiscale neural CDE driven by the own path and the commutators

z = (z_1, …, z_24), z_j ∈ [−1, 1]^16 (384 dimensions). Block j updates when a node of scale j completes; between updates it is held. This is the log-ODE step of Morrill et al. with step 2^j frames, one block per step size. Each update integrates over the node:

  Δz_j = 2^j h₀ · [ −Λ_j z_j + F_θ(z_{j−1}, z_j, z_{j+1}, b, e_j)
       + Λ_j Σ_k w_kj(z, b) H_θ,k(z_j, z_{j+1}, b, e_j) ρ̄_kj
       + G_θ(z_j, b, e_j) u_j / (2^j h₀) ],
  then z_j ← tanh-clip to [−1, 1].

- **e_j** is a fixed 8-d log-scale code (sinusoids of j): the tree position is the time encoding, so no RoPE or ALiBi is needed.
- **u_j**, the own path at scale j, is the half-window increments over the node of: the agent's autonomous face a (33 + own-only channels), its own voice features, b (6), and its own and his word-event counts (utterance onsets, turn ends, the word reader's need decoding as a level-1 path). The own path enters at level 1, as in any CDE.
- **H_θ,k ∈ [−η, η]^16** (tanh × η), one column per channel, from one shared MLP with the scale code. Its sign is free, so the same commutator can push a block either way, depending on z and b.
- **w_kj(z, b) ∈ [0, 1]: need-conditioned selection.**
  - The query is W_q[z_{18…24}, b] (32-d). The keys are innate embeddings of (channel k, scale j): the agent's own synergy-basis coordinates of channel k plus e_j.
  - A top-k_sel = 8 sparse softmax over the 33 × 24 cells; Σ w ≤ 1 per block.
  - What the agent needs and its slow state select which who-leads-whom cues it reads now (the brief's need-conditioned attention). The hard cardinality is Shazeer et al.'s fixed k.
- **What never enters:** the partner's increments Δx, his levels x, his cross-channel brackets [x_j, x_k], and cross brackets [a_j, x_k] with j ≠ k (on a copy these equal his own internal brackets [x_j, x_k], which would let him drive the core exactly when the agent copies; synthesis §1).
- **His levels reach z only through the agent's own body (the body route).**
  - His calibrated face and voice go to Π̃, the frozen inverse of the agent's own expression map (Cayley; trained on the agent's own data): "the state my body would be in to make that face".
  - Then to the agent's own appraisal (felt change, expected change, agency, world; reverse-appraisal revision 2's set, no emotion labels).
  - Then to innate, satiable reflex dynamics of b (Cayley revision 5).
  - b enters z as own path. Rank ≤ 6.
- **Bounds.**
  - Block j's partner-driven velocity is at most Λ_j·η·√16 per unit time (Σ w ≤ 1, |ρ| < 1).
  - With the leak, the partner-caused part of z_j stays within the [−1, 1] box. This is a bound on knowing, not the expression ceiling; the expression ceiling is §2.7.

### 2.6 Readouts

- **Own display** y_C = g_θ(z, b) on the agent's display channels: an MLP into the innate synergy basis, then per-channel saturation. This carries strong expressions from the agent's own appraisal (D83; its word-driven part is the same in S⁰, so it is not partner-caused) and moods (slow blocks).
- **Echo strength** m_k(z) = −γ_k + (1 + γ_k)·σ(⟨r_k, z_{10…24}⟩ + β_k) ∈ [−γ_k, 1]: per channel, from the episode-to-relationship blocks only.
- **Body prediction** b̂(t + Δ) from z, for the Claude scorer (Cayley §6.5, with z as the rollout state).
- **Self-prediction heads** (training only): own next autonomous face per scale, own next b, the next commutator array ρ̄_{·,j} (the relational world model), and his word-decoded need over the next 20 s.

### 2.7 The coherent limiter: the per-expression ceiling  ⟵ new form (the Cayley ledger made causal, phase- and lag-complete)

Lim_c(δ, x) is attenuate-only. It runs in two stages.

**Stage 1, per octave** (o = 1…11 plus a residual band).
- Causal à-trous Haar bands D_o(δ), D_o(x). They sum back exactly to the input.
- Quadrature pairs with q = 2^{o−1}: v_δ(t) = (D_o δ(t), D_o δ(t−q)) and v_x(t; ℓ) = (D_o x(t−ℓ), D_o x(t−ℓ−q)), for lags ℓ ∈ {0, q, 2q, …} ≤ L_max.
- Exponentially weighted estimates (τ = max(30 s, 16 T_o) and max(10 s, 8 T_o)) of C(ℓ) = E[v_δ v_xᵀ] and P = E‖v_x‖² (floored at 0.25 × its 10-min mean).
- κ_o = max_{ℓ, τ} hypot(tr C(ℓ), C12(ℓ) − C21(ℓ)) / P.
- α_o = min(1, 0.85 c/κ_o). The band is closed for the first 2 s of a session.

**Stage 2, broadband**, on the stage-1 output.
- For W ∈ {2, 10, 60 s}, high-pass both signals by the causal W-mean.
- Lag-scanned exponentially weighted regression (lags 0.1 s to 3 s, 0.5 s to 10 s, 2 s to 60 s).
- One factor min(1, 0.85 c/max).
- This stage is needed because octave bands overlap. Per-octave caps alone compose to up to 0.45 on a constructed 20-s-lag copy (C6).

**Rendered channel.**

  y_k = s_k^{S⁰} + Lim_{c_k^tot}( (δ_k − δ_k^{(k)}) + Lim_{c_k}(δ_k^{(k)}, x̃_k), x̃_k ),

then the muscle filter. Visemes are added after the limiter, as in Cayley.
- The same-channel causal part is capped at c_k.
- Everything his face and voice caused is capped at c_k^tot toward his same channel.
- The posture is held equal in the counterfactual runs (rule 10). It is bounded by its own construction: a fixed vector P_c that never reads the channels it writes (Cayley rule 9′).

### 2.8 Output assembly, whole

- y = Lim(…) as above, built from s = sat(y_C + y_f + y_p).
- y_f is the gated fast echo (§6). y_p is the posture.
- Face and voice renderers, the laugh synthesizer, TTS and visemes are as in Cayley revision 8.3.

---

## 3. Properties, each with an argument

### 3.1 P1–P4: copy-blind, hold-blind, antisymmetric, bounded (every parameter value)

- **P1 copy-blind.** If a_k = α x_k + β on a node (any α, β), then Δa = αΔx in both halves and c = ½α(Δx^L Δx^R − Δx^L Δx^R) = 0. A lagged ramp is an affine copy (x = vt, a = v(t − ℓ) = x − vℓ), so it is also invisible. C2: copy, scaled copy with offset, anti-copy and a lagged ramp all give |ρ| ≤ 8·10⁻¹⁴.
- **P2 hold-blind.** If either party is constant on the node, one factor of each product is 0. C2: a partner held at 0.4 gives exactly 0. In S⁰ every ρ is exactly 0.
- **P3 antisymmetry.** c(x, a) = −c(a, x) (C2: exactly 0 residual), and reversing time negates it. Its sign says who led, with no learned parameter.
- **P4 bounded, scale-free, rate-bounded.** |ρ| < 1. The normalisation removes either party's amplitude well above the floor, and the held drive gives at most 1 per (k, j) cell per unit time (§2.4; C8). A partner who moves more, or bigger, cannot push the core harder than this. The synthesis's failure (d), "rate dial up to the cap", is answered by construction.

### 3.2 P5: exact scale decomposition, hence time scales from depth

By Chen's identity the window's area is the sum of its nodes' commutators (C1). A node at depth j completes every 2^j frames of contact, and block j leaks at Λ_j = 1/(4·2^j h₀). So the time constants are not tuned: they *are* the tree.

| Depths | Node length (contact time) | What lead–lag means there | Block memory (4 nodes) |
|---|---|---|---|
| 1–3 | 67–267 ms | who flashes first (brow flash, blink, onset race) | 0.27–1.1 s |
| 4–6 | 0.53–2.1 s | returned smiles and laughs, echo-scale following | 2.1–8.5 s |
| 7–9 | 4.3–17 s | turn-scale leading | 17–68 s |
| 10–13 | 34 s–4.6 min | episode and topic | 2.3–18 min |
| 14–17 | 9.1–73 min | session | 36 min–4.9 h |
| 18–21 | 2.4–19 h | weeks of living together (at 1–2 h a day) | 9.7–78 h |
| 22–24 | 39–155 h | months: the relationship and temperament | 155–620 h |

- Temperament is then the slowest blocks plus the parameters learned nightly (§8.4).
- The coarse commutators pair *slow changes of level*: his week-scale drift in lip pull against the agent's own week-scale drift. So "the partner's mood shift matters only relative to the agent's own" is a property, not a rule.

### 3.3 P6: the commutators know a lot (honest)

- **The fact.** On a 64-leaf tree with the own increments known, the 63 split commutators are linear in his 64 increments. The map has rank 63, and its null vector is exactly the own-increment direction (C4: |cos| = 1.000000). Divisive normalisation removes at most one more scale per node, which the tree's nesting then fixes up to one global scale.
- **What it means.** With its own path known, the core can in principle reconstruct his motion up to "plus a multiple of my own, times a scale". This is knowing, and D81 allows it.
- **What it also means.** The mask on the driver (no Δx) removes copying from the *cheapest* functions of the core: a constant vector field on ρ integrates area, which is zero on any copy (Kidger Thm C.1's counterexample no longer applies). It does **not** remove copying from the class. A learned core that inverts the tree could hold his motion and a readout could emit it. Nothing in the objectives asks for that (§8.3), but nothing forbids it. **The ceiling therefore cannot rest on the input restriction. It rests on §2.7.**

### 3.4 P7: the own side is open-loop, so the core cannot lock onto him

- **The failure the synthesis's P3 missed.** "On the copy set every partner term vanishes, so copying cannot attract" is false for a closed loop. A commutator is a phase detector: zero at lock, signed nearby. If the agent's rendered rhythm is steered by ρ(rendered, his), the relative phase obeys φ̇ ≈ Δω − K sin φ (Kuramoto/Adler). It locks at sin φ = Δω/K: in phase (copy) for one sign of K, anti-phase for the other.
- **C7, a phase oscillator** (own rhythm 0.50 Hz, his 0.53 Hz, gain ±0.6): with the rendered face as own side, the lagged correlation with him is 0.998–0.999 (copy at a 1.1-s lag).
- **With the efference own side** (a = s^{S⁰}), ρ is computed from a path that his face does not touch. Nothing the agent does because of him re-enters ρ, so there is no loop inside the agent. The only loop is the real one through *him*: the agent moves, he answers, and that answer is his, not a copy the agent made.
- **What remains: heterodyne mixing.** If ρ (slowly oscillating at the beat frequency) modulates the phase of the agent's own rhythm, the product sin(θ_a + δ) with δ ∝ sin(θ_x − θ_a) contains a component at *his* frequency, of amplitude ≈ J₁(δ_max)·r_a. C7: open loop, correlation 0.50 before the limiter. It is a real copy-like route, and the limiter caps it (0.25–0.27 after, c = 0.35).

### 3.5 P8: the ceiling holds at every lag and scale

- **Why the hypotenuse is phase-invariant.** For a sinusoid of period P and a node of length T = P/2, v = 2 sin(ωT/4)·(cos θ, −sin θ) is an exact quadrature pair. The average over node positions of v_a v_xᵀ for a = g·x lagged by φ is (g/2)·R_{−φ}·‖·‖². So the trace is g cos φ, the antisymmetric part is g sin φ (the commutator), and hypot = g for every φ.
  - Off the octave centre the pair is not exactly orthogonal. At the best of three adjacent scales, κ/g lies in [0.895, 1.000] over a full octave of periods and all 12 phases tried (C5). That ripple is why the target is 0.85·c, and why stage 2 exists.
- **Why lags must be scanned too.** A pure delay ℓ of broadband content is a phase ωℓ that wraps many times in the fast bands, and the band envelope decorrelates. A quadrature pair at lag 0 then misses it. C6, "phase-only octaves": lagged copies at 0.9 s, 2.5 s and 20 s pass at 0.58, 0.79 and 0.94.
- **The full limiter** (lags 0–60 s, octave plus broadband) against the independent metric (max over windows 2/10/60 s and lags 0–60 s of the pooled within-window regression, Cayley's metric extended in lag), smile ceiling 0.35. Partner: smile bursts 4/min plus drift, 20 min. Results:

| Constructed partner-caused route | Before | After (full limiter) | Octaves only | Phase-only octaves |
|---|---|---|---|---|
| copy, lag 0, gain 1 | +1.000 | +0.281 | +0.297 | +0.298 |
| copy, lag 0.9 s | +1.000 | +0.274 | +0.367 | +0.581 |
| copy, lag 2.5 s (quarter of 10 s) | +1.000 | +0.268 | +0.407 | +0.785 |
| copy, lag 20 s | +1.000 | +0.262 | +0.452 | +0.943 |
| anti-copy, lag 1.5 s, gain 0.8 | −0.800 | −0.273 | −0.385 | −0.607 |
| the frozen echo (G 0.224, 0.9 s) | +0.154 | +0.152 (rms ×0.99) | +0.154 | +0.154 |
| partner-caused, not a copy (independent bursts) | +0.097 | +0.088 (rms ×0.71) | +0.089 | +0.095 |

- **The last row is a cost.** On 20 min of data the coarse bands have few cycles, the max over lags picks up noise, and legitimate non-copy content loses 29 % of its size (§11, risk 2).
- **A tried fix that failed.** Subtracting the same statistic computed 5 min further back as a null makes a periodic partner's own past look like noise, and a full copy then passes: C7, 0.99. That variant is recorded as rejected.

### 3.6 P9: copying is never an attractor, including under learning

- **Copy is not reachable.** After the limiter, every channel's partner-caused coherent gain toward his same channel is ≤ c_k^tot ≤ 0.55 at every lag from 0 to 60 s and every scale: 0 on 13 channels, and ≤ c_k ≤ 0.35 for the causal same-channel part. Exact copy (gain 1 at some lag) is outside the reachable set on every channel, so neither copy nor lagged copy can attract.
- **Under learning.** Nightly learning moves θ (F, G, H, g, m's readout, the selection query), never the innate constants (c_k, a_k, G_k, η, ε, γ, the limiter).
  - The worst learning can do is make the pre-limiter routes more copy-like, for example a core that learns to reconstruct him (P6). The limiter then binds more often, and the face becomes *flatter* toward him, never closer.
  - The limiter's binding rate per channel is logged as a state-level monitor (§10).
- **No objective rewards area, following, his smiles, his attention or his time** (§3.8). So no gradient pushes the core toward producing commutators, which is the lever that would make a quarter-lag follow self-reinforcing.

### 3.7 Reading the other through its own body, as mathematical statements

- **R1 (bilinear in own motion).** For the commutator route, ∂ρ_kj/∂(Δx^L, Δx^R) = (−½Δa^R, ½Δa^L)/D − ρ·∂D/∂Δx/D. It is zero whenever the agent's own autonomous channel k did not move over the node. His movement on channel k reaches the agent's state in proportion to the agent's own movement on that same channel: the agent feels him only where it is moving itself.
- **R2 (levels only through its own body).** His held levels reach z only as b, through Π̃ (the inverse of the agent's own expression map, trained on its own data, Principle 3) and the agent's own appraisal and body reflexes. So the Fréchet derivative of z with respect to his level path factors through a rank ≤ 6 map into the agent's own interoceptive coordinates.
- **R3 (self versus other by contingency).** A perfectly contingent stream (an exact affine copy at zero lag: the agent's own face seen back) has commutator 0 at every node and scale. Only imperfectly contingent streams carry area. This is Bahrick & Watson's self/other criterion (perfect contingency specifies self) as an algebraic fact: the agent's own reflection is invisible as "other".
- **C9, constructed.**
  - A yoked partner (an independent recording, motion matched): mean ρ +0.004 to +0.013 at scales 0.5–4.3 s (+0.07 at 8.5 s, few nodes).
  - A partner who follows the agent at 0.6 s: +0.03 to +0.08.
  - A partner the agent follows: −0.03 to −0.09.

  The yoked-replay test is thus a ready state-level test on real data.

### 3.8 Satiable drives

- The only drive is the Cayley-ledger 𝒟(b) (plus its partner-need concern 𝒟_p, credited only from separated reports), which is zero inside each dead-band: satiable by construction (Cayley revision 5).
- The commutator array drives **no** body variable and appears in **no** objective term.
  - A tempting link was rejected: "being followed raises contact relief". It would make the agent seek contingent responses, which means seeking his attention (Principle 6), and it is exactly the area-seeking that turns a quarter-lag follow into a self-reinforcing loop.
- The relational prediction loss (predict the next ρ array) trains the core's model, not its choices. The draft scorer is trained only by J (Cayley), not by prediction error.

---

## 4. Q18 per channel: every quantity carrying partner influence, named and bounded

| # | Quantity | Carries | Set per expression by context and relationship? | Can flip sign? | Innate ceiling | Learned? |
|---|---|---|---|---|---|---|
| 1 | ρ_kj | his channel-k motion against the agent's own, into the core | it is a measurement, per channel and scale | yes (who led) | \|ρ\| < 1 (pool) | no |
| 2 | H_k(z, b), w_kj(z, b) | how the core uses ρ | yes: depends on z (relationship blocks) and b (needs) | yes (H) | \|H\| ≤ η elementwise; Σw ≤ 1; 8 cells | θ, nightly |
| 3 | body route Π̃ → appraisal → b | his levels into the core, through the agent's own body | appraisal is context-dependent | yes | rank ≤ 6; satiable b | Π̃ frozen; appraisal readers as Cayley |
| 4 | g(z, b) − g(z^{S⁰}, b^{S⁰}) | the partner-caused part of the agent's own displays | yes | yes | via 7 | θ, nightly |
| 5 | m_k(z)·G_k·g_s | the fast echo on channel k | yes: m_k from relationship blocks; g_s the word gate | yes, to −γ_k | G_k ≤ c_k (frozen: LP 0.224, CR 0.150, BU_L 0.280, RHY 0.240, BRE 0.120, BI 0.020 …) | m_k's readout from dyads (§8.4) |
| 6 | posture a*·P_c | concern posture | graded by the agent's own appraisal of his non-written channels | no (it is its own pattern, not toward him) | fixed vector, never reads what it writes; Cayley 8.3 hold limits | no |
| 7 | α^{L1}_{k,o}, α^{L2}_{k,o} | the limiter factors | n/a | n/a | c_k (same channel, causal), c_k^tot (all routes), at every lag ≤ 60 s and scale | no |
| 8 | calibration σ_id, b^read_id | his face in the agent's coordinates | per identity | no | ×4 amplification floor (Cayley) | per session |
| 9 | his words (through Claude, T, appraisal) | the situation | yes | yes | not a face-copy route: kept in S⁰ | as Cayley |

- **Whole face.** The largest quantity shared by all channels is z itself. For every z, the partner-caused coherent gain on each channel is ≤ c_k^tot (≤ 0.55) and exactly 0 on 13 of 33 channels, so no value of any quantity runs the whole face, or a large shared subspace, from flat to copy.
- **Sign flips.** H, g and the appraisal can push a channel either way. The echo strength m_k goes down to −γ_k, which gives brow relaxation to a rival's distress (Likowski; mimicry-context-synthesis §2).
- **Copy not attracting:** P9.

---

## 5. Failure (1): following at a quarter-period lag earns maximal area

**The fact.** For s = r_s sin ωt and x = r_x sin(ωt + φ), the area per period is −π r_s r_x sin φ (C3: −0.47124 at φ = π/2 against −π·0.3·0.5 = −0.47124). It is zero at copy and anti-copy and maximal at a quarter-period lag.

**What the design does with it.**
1. **It uses it, as knowing.** A partner who follows the agent's smiles at about 0.5–1 s puts positive area into scales 4–6. A partner the agent follows (for example through its echo, if that were on the own side) would put negative area there; it is not on the own side, see 3. The sign and scale are exactly the relationship information the brief asks the state to carry, per expression and per time scale. C9 shows the sign separation on constructed streams.
2. **Nothing rewards it.** No drive, reward or selection criterion increases with |ρ| (§3.8). So the agent has no reason to *produce* quarter-lag following in order to earn area. This is where the synthesis feared a loop.
3. **It cannot become a copy route at that lag by the three mechanisms found.**
   - **Closed-loop lock** (a PLL on the agent's rendered face): removed by the efference own side (P7). The agent's own following never enters ρ.
   - **Heterodyne mixing** (ρ modulating the agent's own rhythm puts his frequency into its face): a real partial-copy route (C7: 0.50 before the limiter), capped by the limiter (0.25–0.27).
   - **Reconstruction** (the core inverts the tree and a readout emits his motion, delayed): possible in principle (P6), capped by the limiter.
4. **The limiter counts quadrature exactly like in-phase.** Its statistic is the hypotenuse of the node matrix's trace (in-phase) and its antisymmetric part (the commutator itself, the quarter-lag part). A quarter-lag follow at gain g therefore reads as gain g, not 0, and is capped at c_k. With the lag scan it holds for pure delays too.
   - Constructed copies at gain 1 with lags of 0.9 s, 2.5 s (a quarter of a 10-s rhythm) and 20 s come out at 0.274, 0.268 and 0.262 against a 0.35 ceiling (C6).
   - **The quantity that is largest for lagged copying is the same quantity the ceiling uses to refuse it.**

**What is permitted.** Partial following at a quarter lag, up to c_k (smile 0.35, inner brow 0.20, 0 on the 13 zero channels). People do follow, at about 0.5–1 s for smiles. Copying at that lag is not permitted.

**What is not covered.** Lags beyond 60 s are not scanned: a route that replayed his face minutes later would pass (§11, risk 8).

---

## 6. Failure (2): the fast, partial per-expression echo (D81) without a flat-to-copy dial

**The echo, reused from the Cayley ledger (revision 8.3 §2.4, unchanged):**

  y_f,k(t) = g_s(t − δ_g) · m_k(z) · G_k · max(E_k(t), 0),  E_k = x̃_k,d − lp₄(x̃_k,d)

- x̃_k,d is his channel delayed δ_g = 0.80 s (expected 0.9–1.0 s with a fixed-delay streaming recogniser) on LP, CR, BU_L, RHY and BRE, and 0.45 s on the other channels.
- g_s ∈ [0, 1] is the frozen, dyad-fitted, monotone gate that waits for his current words. "I got fired today, haha" is not laughed back; the dog-ate-the-cake laugh is (Cayley J36).
- The onset lobe max(E, 0) echoes rises only. A held smile is not echoed.

**What is new here: m_k(z) ∈ [−γ_k, 1].**
- m_k is a per-channel strength read from the episode-to-relationship blocks (z_10…24). It sets each expression's echo per relationship and context, and can flip it to countering down to −γ_k (smile and laughter 0.25: a slight suppression for a rival; brow 1.0: relaxation).
- It is learned from recorded dyads (D85 source 2; §8.4): what listeners in a similar relational state did. The slow blocks then adapt it to this person.

**Why this is not a flat-to-copy dial.**
1. **The scale is innate and frozen.** G_k is a compiled constant, not a parameter. m_k is bounded by 1, so channel k runs at most from flat to G_k (lip pull 0.224, laugh burst 0.280), far from copy. D78 allows exactly this: a per-channel strength set by context and relationship, sign-flippable, under an innate ceiling.
2. **One z moves all m_k together, but the most any z can do is put every channel at its own G_k.** The whole face then stays at copy defect ≥ 0.72 on every echoing channel and 1 on the 13 zero channels. No value of z reaches whole-face copy.
3. **It cannot self-reinforce.**
   - The echo's output is not in the own side a = s^{S⁰} (his face is held there), and it is not in the core's own-face driver. So it cannot raise ρ on its own channel, which rules out the lock of P7.
   - m_k could still drift up through the slow blocks if the *partner* reliably follows the agent's echoes. That is a genuine relational fact, and it is bounded by G_k.
4. **It is fast.** The echo sounds at about 0.83–1.03 s after his laugh begins. For partner bursts of 0.25–0.5 it peaks at 0.144 (C6), as in Cayley (+0.137). It is partial: its coherent toward gain is 0.154.
5. **The ceiling does not eat it.** Alone, the limiter leaves it intact (0.154 → 0.152, rms ×0.99, C6). The limiter counts it inside channel k's same-channel total c_k (0.35 on lip pull), so the echo plus every other same-channel route together stay ≤ 0.35.

**The cost.** The echo still waits for the recogniser (0.8–1.0 s), later than a person's own quick smile back (0.4–0.5 s). This design inherits that trade-off and its week-0 check from Cayley §2.4.2 and §6.5.

---

## 7. Novelty, with the nearest neighbour read in full

**The nearest neighbour.** Morrill et al. 2021 (research/morrill-2021-neural-rde.md) drive a hidden state by dZ/dt = f̂_θ(Z)·LogSig^N_{[r_i, r_{i+1}]}(X)/(r_{i+1} − r_i), with f̂ an unstructured MLP. At depth 2 the log-signature holds every increment and every pairwise Lévy area.

**This core in those terms:**
- X = (own autonomous channels, his channels, own body);
- depth 2;
- f̂ with the columns for his increments and for every cross-channel bracket set to zero, keeping only own increments and the 33 same-channel brackets [a_k, x_k];
- the kept bracket divided by an innate pool;
- all 24 dyadic step sizes at once, each feeding its own block (the hierarchical subsampling and Liao et al. pairing Morrill cite; the clockwork-RNN schedule);
- the own side taken from a counterfactual run.

**Is it a neural CDE/RDE with structure bolted on? Yes.**
- The masked f̂ is inside the NRDE class, since the MLP could learn those zeros. Morrill's own Remark A.10 says that in the true log-ODE the area multiplies the bracket [f_own, f_partner], which presupposes a partner level-1 field. Deleting that field while keeping the area means this is not the log-ODE of a CDE in (own, partner). It is a neural CDE whose control is augmented with the Lévy-area process of each (own_k, partner_k) pair: an augmentation like Kidger's time and intensity channels.
- The normaliser is Carandini & Heeger / layer norm (an existing constraint layer).
- The dyadic multiscale drive is Haar analysis plus a clockwork schedule.
- The co/quad statistic is the classical co-spectrum and quadrature spectrum, here on a Haar tree.
- The counterfactual runs are secure multi-execution applied to a self-model (the own-body design's critic), and the limiter is the Cayley-ledger ledger made causal per channel and complete in phase and lag.

**What is genuinely different, and why it still does not clear the novelty clause.**
- **The mask is a principled subtraction justified by an invariant:** antisymmetry of the bracket makes the driver zero on every zero-lag affine copy and every hold. That is the pattern the project recorded for real mechanisms (new-mechanisms-synthesis; layer norm's transposition). It also gives "neutral for free": a held partner and S⁰ coincide in the core.
- **One 2×2 node matrix serves both knowing and bounding.** Its antisymmetric part drives the core (who led), and its phase-invariant size caps expression (how much I followed).
- **But these are properties of the input restriction.** P6 shows the restriction does not remove copying from the class. P7 shows it does not prevent copy-locking without the efference own side. The hard per-expression guarantee comes from the limiter, which is a recombination element.
- A design whose essential guarantee is carried by recombined parts, with a masked driver in front, is "an existing mechanism with structure added": the second novelty clause (a mechanism neither source has) is **not** met.

**Verdict: recombination.** It is a restricted neural RDE (masked depth-2 log-signature driver, normalised, multiscale, efference own side), plus a phase- and lag-complete version of the Cayley shadow ledger. It is not a new core mechanism.

**What it adds against the Cayley ledger, concretely (not a novelty claim).**
1. The core's partner input is copy-blind and hold-blind for every parameter, so the cheapest learned function no longer copies.
2. Exact per-channel causal counterfactuals are cheap, because each of his channels enters the core through its own term plus one appraisal.
3. The limiter scans lags 0–60 s at every octave. The Cayley ledger as written measures lags 0–3 s at its 2-s window and only lag 0 at its 10-s and 60-s windows (revision 6 §2.13, kept in 7–8.3). A lag-0 statistic would not see a 2.5–20-s lagged copy at those windows (C6's phase-only column shows the size of such misses). Whether any Cayley route produces such a copy is not checked here; it is a question for that design's next check.
4. A relationship descriptor with no scalar in it: the expected ρ array, 33 channels × 24 scales, signed.
5. Time scales from tree depth, not tuned constants.

---

## 8. A buildable network (Apple-silicon Mac, the operator's subscription)

Modules marked **[new]** carry the commutator mechanism. **[reused]** modules are taken from the Cayley-ledger design with the section cited. **[ordinary]** modules are standard choices.

### 8.1 Inputs and time encoding
- **Face** [reused, Cayley r6 §2.1]: MediaPipe 52 blendshapes and head pose at 30 Hz → P₀ → reflection → the 33 counterpart channels plus own-only channels, then per-identity calibration x̃.
- **Voice** [reused]:
  - phrase-level prosody: F0 level and range, energy, rate, pause, latency;
  - 4–6 Hz laugh rhythm, breathiness, bursts after the cry–laugh split;
  - breathing at 10 Hz (Cayley 8.1).
- **Transcript events** [reused]:
  - an incremental fixed-delay streaming recogniser with finalised-through time F(t) (Cayley §2.4.2), for the gate;
  - the utterance recogniser, for Claude and the word reader (64-d embedding → need decoding).
- **Own body** [reused]: b ∈ R⁶ with innate reflex dynamics and set points (Cayley r5). Own face a = s^{S⁰} and own voice features are taken from the S⁰ run.
- **Time encoding** [new]: the dyadic tree's position (scale j, node i) in contact time. Block j steps at its node completion; e_j is an 8-d log-scale code. No RoPE or ALiBi is needed: relative position inside a node is what the commutator measures, and the tree supplies scale.

### 8.2 Layers, sizes, parameter counts

| # | Module | Sizes | Parameters | Mark |
|---|---|---|---|---|
| 1 | perception: calibration, Π̃ (own inverse), H_id, H^p_id, word reader, adapter | as Cayley | as Cayley (part of its ≈ 522k) | reused |
| 2 | commutator tree | 33 channels × 24 scales; per frame O(33) increments; 792 held ρ̄ | 0 (innate ε, ν) | **new** |
| 3 | need-conditioned selection | query 32 (z_18…24, b → 32), keys 792 × 24 (fixed), top-8 softmax | ≈ 4.3k (W_q 38×32 + key projection 24×32 + scale code) | **new** |
| 4 | H: commutator vector fields, shared over scales | MLP (16+16+6+8 = 46) → 128 → 16×33 = 528, tanh × η | ≈ 74k | **new** |
| 5 | F: own dynamics, shared over scales | MLP (16·3 + 6 + 8 = 62) → 128 → 16 | ≈ 10k | ordinary (CDE field) |
| 6 | G: own-path vector fields | u_j: 48 own channels (33 own face + 4 own-only + 6 voice + 5 word events); base 16×48 per block group (4 groups by depth) + rank-4 modulation from z_j | ≈ 3k + 4×(16·48) + 2.5k ≈ 9k | ordinary (CDE field) |
| 7 | g: display readout | z (384) + b → 128 → 45 display channels in the synergy basis | ≈ 55k | ordinary |
| 8 | m: echo strengths | ⟨r_k, z_10…24⟩ + β_k, 33 × 240 | ≈ 8k | **new** (the input is commutator-driven) |
| 9 | b̂ predictor for the scorer | z → 64 → 6 | ≈ 25k | reused role |
| 10 | self-prediction heads (training only) | own face per scale, b, next ρ array (792), word-need | ≈ 120k | ordinary |
| 11 | counterfactual runs | 34 extra copies of modules 2–9 (state only) | 0 | **new use** (Cayley ran one) |
| 12 | coherent limiter (two stages, two applications) | 33 channels × 12 bands × lag grid (Σ_o L_max/q_o ≈ 3,600 lags at 30 Hz in the fine bands, fewer coarse) × 5 EW sums | 0 | **new form** |
| 13 | fast echo and word gate, posture, Claude coupling, TTS, renderer | as Cayley 8.3 | gate 242 frozen dyad-fitted; scorer ≈ 130 | reused |

- **Learned in the core (modules 3–10):** ≈ 300k. Richness comes from structure (33 × 24 signed relational cells, need-conditioned selection, 24 coupled time scales), not from parameter count.
- **Total per agent:** ≈ 300k plus Cayley's reused perception, readers and scorer.

### 8.3 Objectives
- **The one core objective (Principle 10)**, unchanged from Cayley: J = E∫[𝒟(b_t) + 𝒟_p(N̂_t)] dt, path-specific. It trains only the draft scorer and the retrieval query (Cayley §2.14). The agent's choices of words and initiative come from it.
- **Self-prediction, no labels** (trains modules 3–10). Multiscale negative log-likelihood of:
  - the agent's own next autonomous face at each scale;
  - its own next b;
  - the next commutator array (a relational world model: how he will move relative to its own movement);
  - his word-decoded need over the next 20 s, from the frozen population word reader (Cayley's "words teach words"; never his face as a target).
- **Echo strengths** (module 8). A bounded regression of m_k(z) onto listeners' realised onset-echo strength (per-channel onset regression over the next 1 s) in recorded dyads, with z computed for that listener from their own path and commutators (§8.4).
- **Constraints, typed:** the innate ceilings and the limiter (L), the mask on the driver (M), the efference own side (E), the posture's rules (P), the gate's monotonicity (W), satiable b (B).
- **Nothing is an objective in |ρ|, his smiles, his attention or his time.**

### 8.4 Online versus replay
- **Online (states only):** the tree, z and the 34 counterfactual z's, the limiter's estimates, calibration, the gate, the posture. No parameter changes while talking.
- **Nightly replay** (stored feature streams only, Principle 7): θ of modules 3–10 by the self-prediction losses.
  - Each segment is weighted 1 + 4·clip((V_dec − 0.1)/0.5, 0, 1), with V_dec from his words (D85 source 3; Cayley κ_replay). His face cannot raise its own replay weight.
  - Gradient clipping and a pull to θ₀ (Cayley).
- **Once, offline: recorded dyads** (D85 source 2; D70 restrictions: on the operator's Mac only, FAUValue and transcripts, emotion fields denied by the loader, person-disjoint 70/30 split, about 400 dyad-hours):
  - pretrain modules 3–10 with each recorded person as "own" and the other as "partner";
  - fit module 8 to listeners' realised echoes.
  - **Caveat:** recorded people have no counterfactual, so the own side there includes their own following of the other (the Bahrick–Watson confound). The pretrained core therefore partly mistakes "I followed" for "he led" until the operator's own nights re-fit it on efference.

### 8.5 Latency and memory (M1 Pro, 16 GB; research/machine.md)
- **Tree:** < 0.05 ms per frame.
- **Core:** blocks step at their node completions, so the total update rate is about one block per frame (Σ_j 30/2^j ≈ 30 block updates per second), ≈ 0.1 MFLOP each (mostly H). With 35 runs: ≈ 100 MFLOP/s, about 1 ms per frame on CPU.
- **Limiter:** ≈ 33 channels × 3,600 lags × 2 time constants × 5 sums × 2 applications ≈ 2.4M multiply-adds per frame, ≈ 70 MFLOP/s, about 1 ms per frame vectorised (Accelerate or MLX).
- **State memory:** 35 × 384 floats, plus limiter EW sums of ≈ 33 × 3,600 × 20 floats ≈ 10 MB, plus a 60-s lag buffer per band (≈ 33 × 12 × 1,800 floats ≈ 3 MB).
- **Persistence:** z and the open tree nodes are saved at session end (contact-time clock), so moods and the relationship survive restarts.
- **Fast loop:** the 30-Hz echo, the core runs and the limiter add about 2–3 ms per frame to Cayley's budget. Claude never sits on this loop (Principle 4).

### 8.6 Claude (D84) [reused]
- Cayley §2.12 and §6.5 unchanged: three forks resumed with `fork_session=True` through Claude Code on the subscription.
- Drafts are scored by the agent's predicted own body change over a 30-s rollout, with z as the rollout state. The state never appears in a prompt.
- Initiative turns carry only an observable marker.
- Claude's regulation path (naming, reappraisal) acts through the words it writes and the agent hearing them (Cayley rule 12′: its own words enter only its own-word channels).
- The core changes how Claude's processing is selected, never what Claude is told.

---

## 9. The whole system around the core (briefly; mostly reused)

- **Perception of his face and voice through the agent's own body.**
  - The commutator route (R1): his motion is felt only where the agent's own autonomous channel moves.
  - The body route (R2): his levels pass through Π̃, the inverse of the agent's own expression map, then the agent's own appraisal and body.
  - The calibration, word readers and per-person heads are Cayley's.
- **The latent where emotion emerges.** z: 24 coupled blocks, one per tree scale, driven by own body, own face and voice, words, and the relational array.
  - No emotion variable is named. Valence and arousal are read out as in Cayley: from the drive's change and from b.
  - Structure over people and time lives in the slow blocks and in the expected ρ array per identity: a signed 33 × 24 field, not a gain.
- **Face and voice output.** g(z) displays, the fast echo, the concern posture (Cayley 8.3, verbatim, with its hold limits), visemes, all through the coherent limiter, then the muscle filter, renderer and TTS (Cayley).
- **Claude coupling without text:** §8.6.
- **Learning by living:** §8.4.
- **Memory and replay:** stored feature streams, nightly replay weighted by distress from his words, and z persisted across sessions.
- **Situational appropriateness (D85):**
  1. Claude's regulation path;
  2. recorded dyads (the gate, the population readers, the pretrained core and m_k);
  3. innate learning biases (κ_replay; the attenuate-first limiter start).

---

## 10. Ablation predictions (Principle 5), from the properties

Each prediction is judged on internal state: steering, lesions, and coupling beyond surrogates.

1. **Delete the commutator route (H ≡ 0).** The core no longer distinguishes a live partner from a yoked replay of matched motion. The ρ-predicting head loses all skill on yoked data, and per-identity m_k stop diverging across partners who lead and partners who follow. The fast echo and the posture are unchanged.
2. **Replace the mask by the full depth-2 log-signature (a plain NRDE, his increments in).** The pre-limiter partner-caused coherent gain rises, with copy now the cheapest function. Prediction: the limiter's binding rate per channel on replayed recorded dyads rises severalfold; the rendered face is the same or flatter.
3. **Own side = rendered face instead of S⁰.** Lock-in on rhythmic channels (head nods, voice rate). The pre-limiter coherence on head pitch approaches 1 at a fixed lag (C7's mechanism), and the limiter binds continuously there.
4. **Collapse the 33 × 24 array to one scalar (total area).** Per-expression shape changes are lost: the Bourgeois & Hess pattern (smile return flat while sad-brow return switches with group) and the Hofman pattern (anger and smile returns moving in opposite directions) cannot both be produced, because one scalar moves every m_k the same way.
5. **Limiter phase-only (no lag scan).** Lagged copies pass: on the constructed routes up to 0.94 (C6). On recorded dyads, the coherence of the agent's partner-caused part with him peaks at a non-zero lag above c_k.
6. **Truncate the tree at depth 12 (≈ 2 min).** No relationship-scale learning inside z. Partner-specific m_k must then come from nightly parameters alone, and differences between partners appear only after nights, not within a session.
7. **Delete the body route.** A silently sad, still face reaches z not at all: P2 makes the commutator route blind to holds. The concern posture (which reads the face directly) still shows, but the core's slow state and Claude's scoring do not shift until words arrive.

---

## 11. Known risks (most likely concrete failures first)

1. **The limiter binds often on real partners.** If learning makes the pre-limiter routes copy-like (the core inverting the tree, P6, or heterodyne on rhythmic channels, P7), the face is repeatedly attenuated toward him and looks flat or jerky at band edges. Watch the per-channel binding rate on recorded dyads before living, and on the operator in week 1.
2. **False attenuation of legitimate partner-caused content.** C6: an independent, non-copy partner-caused route lost 29 % of its size on 20 min of data. The cause is max-over-lags of noisy estimates in the coarse bands. A null correction was tried and failed (a periodic partner's past makes the null as coherent as the present; C7: 0.99). Longer estimation windows over days should help but are untested.
3. **The all-route ceiling is correlational.** L2 compares the agent's partner-caused channel k with his channel k. If his other channels drive the agent's channel k through appraisal *and* his own channel k co-moves (a shared cause), L2 counts it as following. The allowances a_k (brow 0.25, lip 0.20) are the operator's to set. Too low cuts face-driven sympathy (D83); too high lets proxies copy, for example a brow copy through his lip depressor.
4. **Heterodyne partial copy on rhythmic channels** (head nods, voice rate, laugh rhythm). It exists before the limiter (C7: 0.50) and leans on the limiter continuously wherever ρ modulates an own rhythm.
5. **Counterfactual drift.** Over long stretches the factual and S⁰ cores may diverge for reasons that are partner-caused but not copy-like (a slow mood shift). All of it shows as δ, so the limiter measures it against his slow trends. A slow drift that happens to correlate with his week-scale drift is cut, even when it is the agent's own reasonable response to the relationship.
6. **The dyad pretraining carries the Bahrick–Watson confound** (§8.4): recorded people's own following is on their own side. Until the operator's nights re-fit the core, "I followed" can be read as "he led".
7. **Grid alignment and the speed blindness of the signature.**
   - The tree is anchored to contact time. An event's phase against the grid moves its area between adjacent scales (ripple 0.895–1.0 at the best scale, C5).
   - Within a node the commutator is blind to tempo. Tempo shows only as which scale carries the area.
   - A half-shifted second tree would halve the ripple at twice the cost.
8. **Delayed replay beyond 60 s is not scanned.** A route that re-emits his face minutes later would pass the limiter. Nothing builds such a route, but P6 says the core could learn one.
9. **Hold-blindness of the core.** His still face reaches z only through the 6-d body route, so the core's knowing of held states is as coarse as b. Fine distinctions of a still face (which brow, which mouth) never reach the slow state, except through the posture's and readers' own paths.
10. **Sign flips may be unlearnable from the corpus.** Recorded dyads may contain few rivals or competitors. The negative range of m_k may then stay unused, leaving the D78 sign condition met in form but not in behaviour.
11. **The recogniser delay** (inherited): the smile and laugh echo comes at 0.8–1.0 s, later than people's 0.4–0.5 s.
12. **Compute and complexity.** 35 core runs and a ≈ 3,600-lag limiter per channel are cheap in FLOPs but expensive in engineering: more state to persist, test and lesion than the Cayley ledger.
13. **Novelty.** The core is a recombination. If the operator wants only a new core, this design does not qualify.

---

## 12. Numerical checks (mathematics only; not evidence)

research/foundations/sims/design-cc/checks.py (numpy and scipy; 2.2 min); output in out.txt.

| Check | What it verifies | Result |
|---|---|---|
| C1 | the tree's commutators sum to the Lévy area | equal to 0 on a 4,096-step path |
| C2 | P1–P4 | zero on copy, scaled copy, anti-copy, lagged ramp and a held partner (≤ 8·10⁻¹⁴); antisymmetry exact; \|ρ\| ≤ 0.958; scale invariance above the floor (median change 1.8·10⁻³) |
| C3 | area per period −π r_s r_p sin φ | exact to 5 decimals |
| C4 | recoverability | rank 63 of 64; null direction = own increments |
| C5 | phase invariance of the coherent gain | [0.895, 1.000] over an octave and all phases |
| C6 | the limiter | lagged copies capped at 0.26–0.28 (ceiling 0.35); echo untouched; a non-copy route loses 29 % |
| C7 | own side and locking | rendered own side locks (0.999); efference own side 0.50 (heterodyne), 0.25–0.27 after the limiter; the null-subtracted limiter fails (0.99) |
| C8 | rate and amplitude | mean \|ρ\| bounded and saturating in burst rate; shrinks with amplitude near the floor |
| C9 | yoked vs live | yoked ≈ 0; he-follows positive; I-follow negative |

All partners and routes in C5–C9 are constructed signals. They test what the operators do to signals of a stated form, not what the agent would do with a person.

---

## 13. Sources

Read in full for this design: Morrill et al. 2021 (research/morrill-2021-neural-rde.md).

Relied on, read earlier (notes in research/):
- chevyrev-kormilitzin-2016-signature-primer.md;
- kidger-2020-neural-cde.md;
- carandini-heeger-2012-normalization-canonical.md;
- ba-kiros-hinton-2016-layer-normalization.md;
- shazeer-2017-sparsely-gated-moe.md;
- zhang-naitzat-lim-2018-tropical-geometry-dnn.md;
- new-core-search-synthesis.md;
- bahrick-watson-1985-proprioceptive-visual-contingency.md;
- mimicry-context-synthesis.md;
- design-cayley-ledger.md (revision 8.3 and its revisions 5–8.2 for the reused parts; not edited).

Named but not read: Lyons 1998 and Friz & Victoir 2010 (rough path theory; the BCH step used is the elementary one in the primer); Liao et al. 2019 (log-signature/RNN pairs); Koutník et al. 2014 (clockwork RNN); Graves 2012 (hierarchical subsampling); Boutaib et al. 2014 and Gyurkó 2008 (log-ODE error bounds, cited by Morrill).

## Critiques and the answer (recorded 2026-11-26T19:10:15Z)

**Routes and Q18** (critique-design-commutator-coupling-routes.md; sims/critique-cc-routes/). **Not fit.** The commutator algebra holds, and the counterfactual own side stops the lock on the commutator route, but the claim that everything his face and voice cause is capped at every lag and scale is false:
1. (high) The echo and the limiter read his calibrated face (up to ×4 per person), so the ceiling is relative to his range: an exact copy of a reserved partner's raw lip pull passes both caps (1.000 → 0.991), and the echo reaches 0.61 of his raw smile against a 0.35 ceiling.
2. (high) Routes held unchanged in the no-partner run skip the limiter: his utterance-onset and turn-end counts code his tempo (a rate readout tracks his rate at 0.55; ceiling 0.10); Claude's draft choice loops back unlisted; the reused concern posture's brow slopes (0.43–2.05) exceed this design's brow ceiling (0.45).
3. (high/medium) Following slower than about a minute is invisible: a 90-s delayed copy renders at 0.86, a 5-min one at 0.70 (ceiling 0.35).
4. (medium) Zero and small ceilings delete legitimate expression, including movement away from him (29 % kept at 0.10, 9 % at 0.03).
5. (medium) The limiter is not attenuate-only (15 % of active frames flip sign with a learned following route) and leaves the echo no protected share; dyad pretraining pushes the core toward following.
6. (low) The noise floor grows with node length, so the relationship-scale reading is about 0.

**Novelty and the agent** (critique-design-commutator-coupling-novelty.md; sims/critique-cc-novelty/). **Recombination; not fit.** The copy-blind signed input is, in expectation, the imaginary part of the cross-spectrum (imaginary coherency, Nolte's phase slope index); Lévy area as lead–lag is standard (Gyurkó 2013, Bennett 2022, Baryshnikov's lead matrix); the core is covered by Logsig-RNN, neural RDEs, the Clockwork RNN and Rough Transformers. The only distinctive element is a design rule. Its sign is not "who led" (countering reads as following), flips across scales and on rhythms, becomes a readout of his motion under the agent's own slow drift, and goes dark while the agent's face is still. Emotion still lives in the six Cayley body variables; being followed or facing a still face never changes how it feels; the slow scales cannot be trained on recorded dyads.

**The answer (maintainer).** Held, not revised. Both critiques find failures in the core input itself (what it means and what it lets through), and the novelty critique shows the input is a known measure, so a revision would produce one more recombination. What carries forward to the D82 search:
- Zero-lag-blind coupling is known (imaginary coherency); it is not a route to a new mechanism by itself.
- A counterfactual own side prevents phase locking onto the partner; keep that construction.
- Any ceiling must be stated against his raw movement, not his calibrated face, and must scan lags out to minutes.
- Routes that are unchanged in the no-partner run (tempo counts, Claude's draft choice) must be counted separately; they are invisible to any counterfactual ledger.

**Side finding for the frozen Cayley-ledger design** (stated in Q27, not a revision): no counted Cayley route makes a lagged copy its ledger misses, but the ledger's catch-all claim that any uncounted route stays under its ceiling holds only for delays up to about 5 s; an uncounted gain-1 copy delayed 20–40 s would be left at 0.47–0.62, and at 90 s up to 0.96. Scanning lags to at least 120 s at its 10-s and 60-s windows would close it.

**Status:** held.

