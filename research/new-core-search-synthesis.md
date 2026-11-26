# Searching for a new core mechanism: synthesis of the 2026-11-26 reading pass

Sources read in full for this pass (notes in research/):
- chevyrev-kormilitzin-2016-signature-primer.md (signatures, Lévy area, Chen's identity);
- kidger-2020-neural-cde.md (how the neural CDE was derived; Theorem C.1);
- zhang-naitzat-lim-2018-tropical-geometry-dnn.md (max-plus = ReLU networks);
- shazeer-2017-sparsely-gated-moe.md (routing collapse and its balancing losses);
- ba-kiros-hinton-2016-layer-normalization.md (pool transposition and its invariances);
- carandini-heeger-2012-normalization-canonical.md (divisive normalisation across species and areas).

Unreachable or not attempted: Pouget & Snyder 2000 on gain fields (publisher blocked); Butkovič on max-plus algebra and Morrill et al. on neural rough differential equations (not read; named below only as leads).

No emotion labels or named emotion variables are used below the Claude layer. All channels are face and voice features in the agent's own coordinates. All derivations marked "derived" are mine; they were checked numerically in a throwaway script (sinusoid area −π r_s r_p sin φ to 7 digits; affine copy and anti-copy areas 10⁻¹³; the dyadic decomposition equal to the direct area on a 4096-step random path; the normalisation ceiling and its sign flip).

## What the derivation stories add

- **Neural CDE.** The failure: an ODE cannot hear data that arrives after t₀. The fix, taken from rough analysis rather than invented: integrate against the data path, dz = f(z) dX. Its own theorem (C.1) is the warning for this project. The CDE strictly contains input-driven ODEs *because* a constant field copies the driver. So whatever drives a dyadic core must exclude the partner's raw increments.
- **Layer norm.** The same computation pooled over a different set (units instead of batch), justified by a proved invariance: the scale of all summed inputs is erased. As with attention and ResNet, the new thing is a transposition or a subtraction, not an addition.
- **MoE.** A self-reinforcing selection collapse (the twin of a copy attractor) was tamed by a hand-weighted penalty: perplexity 39.8 → 35.6 once a balancing loss is on. A counter-example: the instability was not removed by structure.
- **Tropical geometry.** Max-plus with integer exponents *is* the ReLU network class (Theorem 5.4). A tropical core is notation, not a mechanism.

The pattern the project already recorded (new-mechanisms-synthesis.md) holds. The candidate below follows it: one **subtraction** (remove the partner's level-1 terms from the driver) justified by an **algebraic invariant** (antisymmetry of the Lie bracket).

---

## Direction 1: commutator coupling. The partner reaches the agent's state only through Lie brackets with the agent's own motion

### (1) The object
- **Channels.** For each expression channel k = 1…m:
  - the agent's own rendered channel s_k(t);
  - the partner's channel p_k(t), read into the agent's own coordinates (by the agent's inverse model; perception is not specified here).
- **Commutators, on a fixed dyadic tree of windows over time.** Leaf length h₀ is one frame; a node at scale j spans 2^j h₀. When a node with left half L and right half R completes, it emits one commutator per channel:

  ΔA_k^{(j)} = ½ (Δs_k^L Δp_k^R − Δp_k^L Δs_k^R) / (σ_k + TV_node(p_k)).

  Δ is the increment over the half-window and TV the partner's total variation over the node. The numerator is the level-2 Lie-bracket coefficient [e_s, e_p] of the 2-D path (s_k, p_k) added at that split, by the step-2 BCH product (x₁, a₁)·(x₂, a₂) = (x₁+x₂, a₁+a₂+½[x₁,x₂]).
  - **Derived:** the sum over all nodes of the numerators equals the Lévy area of the whole window exactly (for piecewise-linear paths).
  - So the commutators are an exact decomposition of the lead–lag area by time scale.
- **Core.** The latent state z ∈ R^n evolves as a controlled differential equation:

  dz = F(z, b) dt + Σ_{k,j} f_{kj}(z) dA_k^{(j)} + G(z) dB.

  Here:
  - B is the agent's own interoceptive and own-body path;
  - F is the agent's own dynamics;
  - s = g(z) is the agent's face;
  - |f_{kj}| ≤ c_k, an innate bound per channel, enforced by construction (for example c_k·tanh).
- **Allowed partner terms.** Same-channel brackets only. Cross-channel brackets [s_j, p_k] with j ≠ k are excluded, because on a copy they equal the partner's own internal brackets [p_j, p_k] and would let the partner drive the agent during copying (derived).
- **Excluded partner terms.** The partner's level-1 increments dp_k and level p_k never enter.
- **Words.** The partner's words reach the agent through Claude and the agent's own appraisal, which is outside this object.

### (2) Why it is not an excluded framework with structure bolted on (honest)
- **What it is not:**
  - not attention or Hopfield (no similarity score, no softmax over stored items);
  - not an SSM or linear operator (the driver is an antisymmetric bilinear functional of two paths, and F may be nonlinear);
  - not oscillator coupling (no phase variable);
  - not active inference or optimal control (no objective is optimised by the coupling itself).
- **What it is:** a **neural CDE (or rough differential equation) with a restricted driver.** Neural RDEs driven by log-signature features already exist (Morrill et al., not read). By the brief's parts test this is a **recombination**. Its single new element is the restriction: the other is admitted only as a commutator with one's own motion, channel by channel and scale by scale.
- **Why that may still matter.** The restriction yields properties that hold for every parameter value, by algebra rather than by a learned ceiling. That is the form the second novelty clause asks for. Whether it clears that clause is for the independent critic.
- **Reduction risk.** For oscillatory own dynamics, a commutator is a phase detector. With F oscillatory and f tuned, the system becomes phase-locked coupling: Kuramoto-like, which is excluded.

### (3) Per-channel capped coupling, no copy attractor, multiple time scales

**Properties that hold for every parameter value (derived):**
- **P1 Copy-blind.** If s_k = a·p_k + b on a node (any a, b: copy, scaled copy, anti-copy), every commutator of channel k on that node is 0.
- **P2 Hold-blind.** If either party holds still on a node, the commutator is 0.
  - Held partner levels have no route.
  - The partner registers only in commutation with the agent's own movement: reading the other *through* the own body, as a bilinear fact.
- **P3 Copy is not sustainable.** Suppose the agent copies, s ≡ p.
  - Then all allowed partner terms vanish (P1), and ds = Dg(z)[F dt + G dB] no longer depends on the partner.
  - Sustained copying therefore requires the partner's path to be a trajectory of the agent's own dynamics under its own body input.
  - For a generic partner, the copy set is not invariant. Nothing partner-dependent acts on it, so it cannot attract.
  - (This is level copying at zero lag; see failure (b) for lagged copying.)
- **P4 Ceiling set by the agent's own body.** |numerator| ≤ TV(s_k) TV(p_k), so |ΔA_k^{(j)}| ≤ TV_node(s_k) ≤ v_k^max·2^j h₀.
  - v_k^max is the agent's innate movement-speed limit for channel k.
  - So the partner's per-node influence on channel k is bounded by how much the agent itself moved on k, times the innate c_k.
  - Partner intensity saturates through the normalising denominator: Carandini & Heeger's eq. 9 form, see Direction 2.
- **P5 Sign.** The sign of A says who led (swap-antisymmetric and reversal-antisymmetric). f_{kj}(z) maps either sign either way and depends on the state, so its sign can flip with the relationship and context. It is per channel and per scale.
- **Time scales from the tree, not from time constants.** Nodes at scale j complete every 2^j h₀. With h₀ = 33 ms:
  - depth 20 reaches about 9.6 h;
  - depth 24 reaches about 6.4 days.

  Reflex-scale lead–lag (fine nodes) and day-scale lead–lag (coarse nodes) are the same quantity at different depths of one exact decomposition. Temperament would be how f_{kj} and F weight the coarse scales.

### (4) Most likely concrete failure
- **(a) Fast matching cannot come from this route.** D81's fast echo (about 0.8–1.0 s) is near-zero-lag matching, which P1 makes invisible.
  - The echo must be a separate innate route, and that route is where a dial can return.
  - (A lagged echo does create area, so the echo also feeds the core. That needs checking for runaway.)
- **(b) Lagged copying.** For sinusoids the area per period is −π r_s r_p sin φ (derived). It is zero at copy and maximal at a quarter-period lag.
  - A learned f that grows with area can build a phase-locked loop that follows the partner with a lag: copying shifted in time, possibly attracting.
  - Test: the copy defect at the best lag, not at lag 0, measured on recorded dyads.
- **(c) Blind to speed.** Signatures are reparametrisation-invariant, so time or intensity channels must be added (as Kidger et al. do). Each added channel is a new partner route to audit.
- **(d) Rate dial up to the cap.** A partner who moves more does push the drive toward the cap.
- **(e) Richness is not shown.** The partner contributes an m × J array of signed commutators. Whether rich structure emerges in z depends entirely on F, G and f; the object guarantees the coupling's form, not the latent's richness.

---

## Direction 2: a self–other divisive pool, with the time constant set by the pool

### (1) The object
- **Rate form (Carandini & Heeger, eq. 9 generalised):**

  R_k = (w_k^s d_k^s + w_k^p d_k^p + β_k) / (σ_k + Σ_j α_kj (d_j^s + d_j^p))

  - d^s is the agent's own drive;
  - d^p is the partner's mapped drive;
  - w_k^p, α and σ are innate per channel.
- **Conductance form:**

  C dV_k/dt = −g_L V_k + Σ_i g_i(·)(E_i − V_k)

  The steady state is a convex combination of fixed reversal levels E_i, and τ_k = C/(g_L + Σ g).

### (2) Not excluded? Honestly, no
- This is divisive normalisation, layer norm in ML, and the liquid-time-constant neuron's steady state (hasani-2021, already "reject as core").
- It is an existing mechanism, a constraint layer, not a core.

### (3) What it gives (derived; checked numerically)
- **Ceiling.** The partner's effect on R_k never exceeds w_k^p, however strong the partner. With w^p = 0.3 and partner drive 1000, R = 0.302.
- **Sign flip by context, with no learned sign.** The same partner input:
  - raises R from 0 toward 0.3 when the agent is quiet;
  - *lowers* R from 0.75 toward 0.3 when the agent's own drive is high.
- **Time scale from the pool.** τ_k = C/(g_L + Σ g) shortens with total activity: fast when lively, slow when quiet. No time constant needs tuning.
- **Copy.** With an innate saturating shape, whole-range copying is impossible, because R is concave and bounded in the partner's level.
- **Use in Direction 1.** It supplies the normalising denominator that caps the commutators.

### (4) Most likely concrete failure
- If the partner's pre-map d^p = h(p) or the conductance g^p(p) is learned, copying *below* the ceiling is reachable.
  - Derived: g^p(p) = p(g_L + g_s)/(E^p − p) gives V = p on [0, E^p), taking the agent's own reversal at rest as 0.
  - The scale of that learned map is a flat-to-copy dial inside the ceiling.
- It meets D78 only if the partner's pre-map shape is innate. That leaves learning only to the own-side weights, and probably starves the per-relationship learning D83 asks for.

---

## Direction 3: a graded-group state. Memory lives in the step-2 nilpotent group, forgotten by dilation

### (1) The object
- **State.** The truncated signature of the joint path (own and partner channels), G_t = (x_t, a_t) in the free step-2 nilpotent group. It is the universal linear CDE solution dG = G ⊗ dX (primer, Picard section).
- **Forgetting.** Forgetting by the group's dilation δ_λ(x, a) = (λx, λ²a) at each step:

  G_{t+h} = δ_λ(G_t) · exp(ΔX_t)

- **The relationship.** The expected log-signature of the dyadic path under this partner. On compact sets, the expected signature determines the law of the path (Cor. 1.36), so the relationship would be a characteristic of the joint distribution, not a gain.

### (2) Not excluded? It reduces
- It is the signature itself plus exponential decay (fading-memory signatures likely exist in the literature; not read).
- With the partner's level-1 coordinates removed, it collapses into Direction 1's commutator store.

### (3) What it would give
- A relationship descriptor with no scalar in it: per-channel and cross-channel lead–lag moments at every order.
- Time scales tied by grade: level-1 memory decays as λⁿ and level-2 as λ²ⁿ (derived), so τ₂ = τ₁/2.

### (4) Most likely concrete failure
- **Grading gives fixed ratios (a factor of the grade), not orders of magnitude.** Reflex to temperament spans about 10⁶, which needs Direction 1's tree, not dilation.
- **Level 1 leaks held levels.** The level-1 part, if kept, is an exponential average of the partner's level: the held-level leak the critiques already found.
- **Verdict.** Reject as a time-scale source. Keep the expected log-signature as the form of the relationship, and pass it to Direction 1's f_{kj} as context.

---

## Overall verdict and next steps

- **Direction 1 (commutator coupling) is the most promising this pass found.**
  - Its copy-blindness, hold-blindness, self/other antisymmetry and exact scale decomposition hold for every parameter, by the algebra of the Lie bracket.
  - Honest verdict: a recombination (a restricted neural CDE/RDE) whose one new element is a subtraction.
  - Its predictable failures are lagged copying and the separate echo route.
- **Direction 2** is an existing constraint layer that Direction 1 needs.
- **Direction 3** reduces to Direction 1.

Before any design is written:
1. Read Morrill et al. on neural RDEs and log-ODE methods (the nearest neighbour), and a primary rough-paths text (Lyons) for the BCH step used here.
2. Read Butkovič on max-plus event timing (cycle-mean rhythms) for turn-taking.
3. On the Seamless Interaction features (Mac only, D70/D85 restrictions), measure per-channel commutator spectra across scales for real dyads. Check whether lagged following at the best lag is common: that is failure (b), measured before it is designed around.
