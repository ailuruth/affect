# Critique: v3-enactive-robotics (dyadic loop regulation)

Critic: an independent subagent that did not write the sketch. Written 2026-11-25T09:42:58Z under operator notes Q8 (critique round) and Q9 (novelty test). Nothing here was run on Seamless Interaction. Section 4 uses two kinds of check:
- the sketch's own scalar dyad (P-a), solved exactly with a discrete Lyapunov equation;
- a synthetic null for P1.

Both check algebra and statistics, not people. One descriptive number comes from the single Seamless pair already on disk; nothing was downloaded.

**Verdict: recombination, as the sketch itself says.** Named exactly: **certainty-equivalence indirect adaptive control of the joint dyadic loop toward marginal stability.** It is DEP- and homeokinesis-style criticality plasticity whose target is the leading eigenvalues of an estimated joint Jacobian. The partner's leg is identified with a dither, which is the interventional contingency detection of Watson and Movellan. Movellan 2005 is uncited and is closer than anything the sketch cites for this part.

**Central claim (no scalar sweep passes through imitation; rank K\* ≤ 2r excludes the mirror; inverted-U compensation): does not survive as stated.**
- The leak λ is a single dial. As λ → 0, the joint loop goes critical, and the agent's and partner's signals become locked: their correlation goes to 1, and the partner-driven share of the agent's variance goes to 1.
- "Critical reciprocity" is a scaled, possibly lagged, copy on every copy index.
- The rank bound holds only at a stationary fixed point with λ > 0. Even then, rank 6 covers 93–95% of AU variance in the one local pair.
- The inverted U is correct algebra. In P1 it is confounded with the stability envelope of any stationary dyad.

## Sources read for this critique

| Source | What I read, and how |
|---|---|
| Der & Martius 2016, ICDL-EpiRob, "Dynamical self-consistency ..." (Leipzig PDF) | PDF text extracted. Read: the controller and normalization section and §IV-A "Including vision" in full. Not read: the rest. |
| Der & Martius 2015, PNAS, "Novel plasticity rule ..." (PMC4653169) | Through a fetch tool that returned the κ sentences and the DEP rule from the first 100,000 of 110,950 characters. |
| Movellan 2005, "An Infomax Controller for Real Time Detection of Social Contingency", ICDL (UCSD PDF) | PDF text extracted. Read: abstract and §I–III.B. |
| Di Paolo, Rohde & Iizuka 2008 (CSRP 589 preprint) | PDF text extracted. The sketch's quotations were checked. Not read in full. |
| Project notes: research/react-challenge-baselines.md, research/seamless-interaction.md, research/harness/HARNESS.md, critique-developmental-dyad.md | Read where relevant. |
| research/data/seamless/…/V00_S0080_I00000377 (2 people, 2,640 frames each, v1 FAUValue) | Already on disk. Used for PCA only. |

I did not read Der 2008, De Jaegher & Di Paolo 2008, Aguilera & Bedia 2018 or Åström & Wittenmark 1973, and I make no claim about them.

## 1. Parts list (novelty test)

| # | Part | Existing mechanism | Source (read) |
|---|---|---|---|
| 1 | First-order AU plant, A = diag(α_i) | Linear filter | — |
| 2 | CTRNN self-model with log-spaced τ | CTRNN / multi-time-scale RNN | Di Paolo et al.: CTRNNs "allow the specification of multiple timescales" |
| 3 | Fast plastic partner operator K_t | Fast weights | — |
| 4 | B̂ from the agent's own innate micro-motion ξ | Dither or persistent-excitation system identification. Socially, it is **active contingency detection**: an agent uses its own actuator to test whether a partner responds. Movellan: "in order to gain information about H the robot must use its actuator at least once and not use it at least once"; a control robot "was not responsive to the infant's behavior" | Movellan 2005 |
| 5 | "Like me" prior for Λ̂_p | Inverting one's own model; the DEP robots' hypothesis | Der & Martius 2016: "Each robot hypothesizes (correctly) that the other one is of the same construction as itself" |
| 6 | (★) eigenvalue-gradient drive of the leading |μ_j| to 1, with leak | Criticality-seeking plasticity. DEP: "With κ sufficiently large, this global attractor is destabilized so that modes start to self-amplify" … "ending up in full chaos for large κ" | Der & Martius 2015 |
| 7 | k ∝ 1/b at high b | Indirect adaptive pole placement (the sketch's own reading) | — |
| 8 | K̄_p, per-partner EMA | Slow weights | — |
| 9 | Mode readouts (|μ|, arg μ, loadings, participation) | Eigendecomposition / DMD | — |

Every part is an existing mechanism, so it is a recombination under Q9.

## 2. Closest prior work and the sketch's reading of it

**Der & Martius 2016.** Quotes checked and accurate:
- "x = (xown, xoth)";
- the learning signal "is replaced with the sum x′own + x′oth";
- "a rapid convergence (in seconds) toward a synchronized motion";
- "the sighted robot learns to imitate the motions of the blinded robots, which acts as a sender".

The sketch reads it fairly: the closest work shows synchrony, imitation and a κ dial openly. Its claim that DEP "has no estimate of the partner's responsiveness" is right for this paper.

**Der & Martius 2015 (PNAS).** Quotes checked and accurate:
- "With κ small (compared with 1), activity breaks down ...";
- "With κ sufficiently large, this global attractor is destabilized ...";
- "full chaos for large κ".

**Di Paolo, Rohde & Iizuka 2008.** Quotes checked and accurate:
- "sensitivity to contingency arises from processes of circular causality that characterise the collective dynamics";
- "the feedback is broken in the one-way interaction";
- "Two–way mutual scanning is the only globally stable condition." This sentence appears in the preprint itself, so the sketch's attribution to Auvray et al. "through this paper's account" holds.

**Movellan 2005 (missed; the closest prior work for the part the sketch calls new).** A robot detects a responsive social agent by scheduling its own actions, and its causal model separates self-feedback, agent-response and background periods: "The role of the robot is to discover as soon as possible and as accurately as possible the presence of responsive social agents." The original infant study had a yoked control in which the robot "was not responsive to the infant's behavior or to any other events in the room". That is the sketch's live-versus-recording test.
- The sketch's B̂ is a continuous, multichannel, linear version of this.
- What the sketch adds is **using** the estimated responsiveness to set its own coupling toward joint marginal stability.
- Movellan has a background process. The sketch replaces it with the independence of ξ, which is valid only in the live case (see section 5).

**Misquotes found:** none in the sources I checked.

## 3. Reduction

With B̂ := b fixed and known, (★) is gradient descent on Σ_j(1 − |μ_j|)²/2 + λ‖K‖²/2 over the agent's block of a known joint matrix, a regularized pole-placement objective. With B̂ estimated online and used as if true, it is certainty-equivalence indirect adaptive control. Remove the partition into legs (regulate the whole loop) and it is homeokinesis or DEP aimed at criticality. Remove the regulation and keep the probe, and it is Movellan's contingency detector without the infomax scheduling. Nothing is left over.

## 4. Break attempts

### Algebra checks

**P-a is correct.** det(J − I) = (1−a)(1−p) − kb, so μ₊ = 1 if and only if kb = (1−a)(1−p). I solved the scalar fixed point λk = (1 − |μ₊|)·∂μ₊/∂k (with ∂μ₊/∂k = b/2D) numerically for a = p = 0.8 and λ = 0.01. k\* across b = 0.001, 0.005, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2:

0.43, 0.64, **0.70**, 0.54, 0.35, 0.19, 0.08, 0.04, 0.02

This is an inverted U, and at large b it follows k\* ≈ (1−a)(1−p)/b.

**Slip in the sketch.** (★) is written τ_K K̇ = (gradient) − λK. Its fixed point is K\* = (gradient)/λ, which **does not depend on η = 1/τ_K**. P-a's "k\* ≈ (η/λ)…" and §3's "sweeping η/λ" should read 1/λ. η sets only the speed of approach.

### (b) A single dial: the central claim

**Effective gain.** Hold the partner (a, p, b) fixed and treat 1/λ as the dial. I computed the stationary covariance of the joint AR(1) [y; x] with unit noise on both sides by solving the discrete Lyapunov equation. Columns: corr0 = corr(y_t, x_t); max lag corr = max over δ in 0..30 of corr(y_{t+δ}, x_t); partner share = 1 − Var(y | uncoupled)/Var(y).

| b | λ | k\* | abs(μ₊) | corr0 | max lag corr | partner share |
|---|---|---|---|---|---|---|
| 0.15 | 10 | 0.020 | 0.855 | 0.35 | 0.35 | 0.04 |
| 0.15 | 1 | 0.071 | 0.903 | 0.49 | 0.49 | 0.19 |
| 0.15 | 0.1 | 0.175 | 0.962 | 0.78 | 0.79 | 0.65 |
| 0.15 | 0.01 | 0.250 | 0.994 | 0.96 | 0.97 | 0.95 |
| 0.15 | 0.001 | 0.265 | 0.999 | 1.00 | 1.00 | 0.99 |
| 0.02 | 10 | 0.012 | 0.816 | 0.07 | 0.07 | 0.00 |
| 0.02 | 0.01 | 0.696 | 0.918 | 0.69 | 0.84 | 0.90 |
| 0.02 | 0.0001 | 1.925 | 0.996 | 0.98 | 0.99 | 1.00 |

- The **coefficient** k\* is bounded, as the sketch says.
- The **share** is not bounded. Near criticality, the loop amplifies the partner-driven part of the agent's variance without limit, and agent and partner move together along the critical eigenvector, in the ratio v_a/v_p = k/(1−a).
- This holds whether b is small or large, so a mirroring partner (large b) does **not** make the agent less correlated with it. The "compensation" applies to the coefficient, not to the behaviour.
- One scalar, λ, takes the agent from near-uncoupled (corr ≈ 0.07–0.35) to lockstep (corr ≈ 1).
- This is DEP's κ again. The sketch moved the dial from κ to λ and the endpoint from chaos to criticality, and in a linear loop criticality is synchrony.
- With complex μ (a rhythmic mode, which the sketch wants for nods and laughter), the locked mode is a phase-shifted oscillation in both partners. The maximum lagged correlation then goes to 1 at the phase lag: a delayed copy whose lag is set by arg μ.

**"σ_ξ changes only the variance of B̂."** It also sets the uncoupled variance of y, so it rescales the share. This is minor.

**"The partner share is a function of (B̂, Λ̂_p, Λ_a), varies by channel."** True for the profile across channels. The **level** is set by λ, through the closeness to criticality of every regulated mode. "One gain sets the level, structure sets the profile" is the structure the eight v2 sketches had.

### P-b: the rank bound

The algebra is correct where it applies: each ∂μ_j/∂K is a complex rank-1 matrix, its real part has rank ≤ 2, and at a stationary fixed point λK\* is a sum of r of them. It applies narrowly, for three reasons:
1. **No stationarity in conversation.** K(t) = e^{−λt/τ}K(0) + (1/τ)∫e^{−λ(t−s)/τ}G(s)ds, where each G(s) has rank ≤ 2r but its eigenvectors move as B̂ (τ_B ≈ 20 s) and h change. The integral accumulates new directions over the memory τ_K/λ. The smaller λ is (the dial again), the higher the realized rank.
2. **K_t starts at K̄_p**, an EMA of K_t over hours to days, which is generally full rank. A returning partner starts the agent from a high-rank operator.
3. **At λ → 0** the fixed-point condition becomes |μ_j| = 1 for every regulated mode, which is a manifold of K's. Nothing on it forces low rank.

**Even where the bound holds, it does not exclude a practical mirror.** In the one local pair, the top 6 principal components hold 94.7% (P0115) and 93.4% (P0116) of the 23-AU variance (valid frames, the duplicate column dropped; one pair, column order unverified). A rank-6 delayed mirror in the dominant subspace reproduces nearly all of what Mirror does. The critical modes load on high-variance directions, so that is where a rank-6 K would go.

### (a) Collapse into a delayed copy

- **Reached at small λ** (table above): lockstep in ≤ 2r channels, which carry about 93–95% of the variance, with lag arg μ.
- The defence "a recording gives B̂ → 0, so K decays" is correct for a live agent facing a recording. It does not protect against the live case, where the human responds.

### (c) A lookup table of past faces

- **Not a lookup table.** No face is stored, and the memory is low-dimensional operators.
- The scarce-data risk is different: **B̂ estimation power.** B̂ is a rank-4 regression of 24 partner channels on a 240-dimensional lagged dither, from about 200 samples per τ_B (20 s at 10 Hz).
  - If σ_ξ is small enough to be invisible, the partner cannot respond to it, so B̂ is noise, and (★) drives K with noise.
  - If σ_ξ is visible, the agent twitches.
- The sketch gives no power calculation. It should give one before any live claim.

## 5. The Seamless test: feasibility and whether it discriminates

**Feasible as data, blocked by disk.** V00 FAUValue, is_valid, VAD and transcripts are available. Familiar and stranger pairs are naturalistic only. The repeat actor pairs (195) are V00 improvised only, with no session order; P4 already says so.

**The mechanism cannot run on a recording, and the sketch says so (Part B).** Part A substitutes something else:
- ξ := X's self-model residuals;
- B̂ = a Granger cross-lag estimate;
- X re-anchored to its real state every second.

That removes the part the sketch calls new (interventional identification). It brings back the common-driver bias the sketch says ξ avoids: topic, turn and laughter drive both X's residuals and Y. Movellan's model handles this with an explicit background process; Part A has none. **What Part A tests is a Granger-coupled forecaster regulated toward criticality, not the proposed agent.**

**P2 against the simple baselines.**
- **Criterion 1 is unfair in the mechanism's favour.** Part A re-anchors to X's true state every second; Median, Random, NN, Mirror and Delayed Mirror get no re-anchoring. Any re-anchored forecaster beats Mirror on CCC against the real X. The sketch includes Persistence, which is the right floor, and criterion 1 should be "beats Persistence and a re-anchored ridge forecaster", not "beats Mirror".
- **Criterion 2 is not diagnostic.** With re-anchoring, the copy index of ŷ inherits X's real correlation with Y.
- **Criterion 3 tests the wrong rival.** The dial family is a full-rank ridge. The obvious one-dial rival to a rank-≤6 operator is a **reduced-rank ridge (rank 6) with one λ**. If it matches the per-AU partner-share profile, the mechanism's advantage is just low rank. It must be added before criterion 3 can falsify anything.

**P1 (human data; the "primary falsifier") is confounded on its inverted-U part.**
- Every 20-s window of a real, bounded recording is fitted by a stable operator, so the windowed gains satisfy roughly g_{X←Y}·g_{Y←X} < (1−a)(1−p). That is a hyperbolic ceiling, and it exists without any regulation.
- I simulated the sketch's own falsifying alternative: mutual contagion, with both gains rising with a shared engagement factor (corr 0.60 before filtering), plus only the stability condition, a = p = 0.8, 1,705 stable windows.
  - On the true gains, the quadratic fit gave a negative curvature (−0.68), a positive slope at the low end (+0.08) and an interior peak: **the predicted inverted U, from contagion alone.**
  - Segment-shuffle and data-sliding surrogates break cross-coupling, but they do not remove a stability envelope that every real window has. The E3 surrogates therefore do not control this.
- The **product-stability criterion does discriminate.** Under the null, var log(kb) = 9.6 > var log k = 4.4. It should become the primary falsifier, with the inverted U demoted to secondary.
- **Power.** With OLS estimates from 200-sample windows, the null's low-end slope flipped sign (−0.04). Estimation noise in 20-s windows is of the same order as the effect. A power analysis is needed before P1 is run.

**P3 is not discriminating.** "Human cross-person operator rank ≤ 6" is expected of almost any model if, as in the one pair, 6 components carry about 94% of AU variance.

**P4 is not specific.** Per-pair carry-over of an EMA operator is predicted equally by the fast-weights and developmental-dyad recombinations. It tests "per-pair memory", not loop regulation.

**Named channels.** The amusement-mode readouts (CheekRaiser, LipCornerPuller) need the AU column order, which the harness treats as unverified and unlabelled.

## 6. Summary for the record

| Item | Finding |
|---|---|
| Verdict | Recombination: certainty-equivalence indirect adaptive control of the joint loop toward marginal stability (DEP/homeokinesis-style criticality plasticity) + dither-based interventional contingency identification (Movellan 2005, uncited) |
| Algebra | P-a correct (inverted U confirmed). The fixed point depends on 1/λ, not η/λ. P-b correct only at a stationary λ > 0 fixed point |
| Strongest break | 1/λ is a single dial: as λ → 0 the joint mode goes critical and corr(agent, partner) → 1 (0.35 → 1.00 at b = 0.15), partner share → 1, delayed at arg μ for rhythmic modes. "Critical reciprocity" is the copy |
| Rank defence | K̄_p initialization and non-stationary eigenvectors give a high realized rank; rank 6 covers about 94% of AU variance in the one local pair |
| Central claim | Fails as stated. What survives: zero coupling to a non-responsive recording (live case only), and a bounded coupling coefficient (not a bounded share) |
| Test | Part A tests a different (Granger) mechanism; re-anchoring makes Mirror an unfair floor; add a reduced-rank one-λ ridge; P1's inverted U is produced by contagion + stability; the product-variance part of P1 is the usable falsifier |

## Appendix: the checks (run in research/foundations/sims' uv environment; scripts not kept in the repo)

- **Scalar dyad.** J = [[a, k], [b, p]], a = p = 0.8, unit noise on both. k\* comes from brentq on λk − (1−|μ₊|)·Re[(μ̄/|μ|)·b/(2D)] over (0, (1−a)(1−p)/b). The covariance comes from scipy's solve_discrete_lyapunov(J, I), with lagged covariances J^δ Σ.
- **P1 null.** e ~ U(0,1) for N = 4,000 windows; k, b = clip(0.5e + 0.12·N(0,1), 0). Windows were kept if kb < 0.98(1−a)(1−p). A quadratic fit of k on b used the true gains, and separately the OLS gains from 200-step simulations of each window.
- **PCA.** v1 FAUValue of P0115 and P0116; is_valid frames only; column 19 dropped; centred SVD.
