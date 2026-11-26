# Critique of the commutator-coupling design: novelty, fitness as an emotional agent, buildability

Independent critic, 2026-11-26T18:59:31Z

Critic of research/foundations/design-commutator-coupling.md. I did not write it. Standard: brief.md (Principles, and the operator's demand for a genuinely new core mechanism at the level of attention or Transformers, not an existing framework with structure bolted on), questions.md Q17 as relaxed by Q19 (concrete failures, not rigor), Q21 and D82 (a recombination with no known concrete failure goes to the operator, its novelty stated plainly). A separate critic hunts copy routes through the limiter; I size none, and hand on the one I met (§2.2, item 3).

Read for this critique, notes in research/: Nolte et al. 2008 (phase slope index; restates the 2004 imaginary-coherency paper, which was unreachable), Gyurkó et al. 2013 (signature lead–lag in finance), Bennett, Cucuringu & Reinert 2022 (Lévy-area lead–lag metric), Kaushik 2024 (Baryshnikov's cyclicity analysis and lead matrix; the 2016 CDC paper was unreachable), Liao et al. 2019 (Logsig-RNN), Koutník et al. 2014 (Clockwork RNN), Moreno-Pino et al. 2024 (Rough Transformers), Salvi et al. 2021 (signature kernel), Alkhodari et al. 2026 (signed phase coupling in dyadic debate), Kauttonen et al. 2023 (in part; dyadic facial recurrence). Also re-read: the design's nearest-neighbour notes (Morrill 2021, Kidger 2020) and new-core-search-synthesis.md. Unreachable: Delaherche et al. 2012 (synchrony methods survey; HAL blocked), Baryshnikov & Schlafly 2016 (Illinois repository blocked), Nolte et al. 2004 and 2005 (no open copy; NeurIPS proceedings blocked).

Checks of the mathematics only, on constructed signals (not evidence): research/foundations/sims/critique-cc-novelty/checks.py, output in out.txt, 1.5 s.

---

## Summary verdict

- **Novelty: recombination, and less new than the design says.** I agree with the author's verdict and go further. Even the two elements the design lists as "genuinely different" are established:
  - The copy-blind, hold-blind, swap-antisymmetric, sign-says-direction input is the **imaginary part of coherency / quadrature spectrum** (Nolte 2004; phase slope index, Nolte 2008), introduced for the same reason: zero-lag mixtures must not count as interaction. The expected node commutator at each scale depends only on the quadrature cross-spectrum (K1, derived and checked). The Lévy area as a lead–lag reading is standard in finance (Gyurkó 2013; Bennett 2022) and fMRI (Baryshnikov's lead matrix).
  - "One 2×2 matrix for knowing and bounding" is **coherency's imaginary part versus its modulus**: the split Alkhodari et al. 2026 use on dyadic heart rhythm.
  - Interval log-signatures into a recurrent state (Liao 2019, Morrill 2021), exponential clocks (Koutník 2014), and attention over multiscale signature patches (Moreno-Pino 2024) cover the rest of the core.
  - **What remains is a design rule, not a mechanism:** the partner is admitted into the agent's state only as a same-channel quadrature statistic against the agent's own efference path. That is an input restriction on an existing class, justified by an existing invariance.
- **The design's interpretation of its input is wrong in three concrete ways** (all from the algebra, checked):
  1. The sign of ρ is (lead direction) × (sign of association), not "who led". A partner who counters the agent reads exactly as the agent following him (K2: +0.221 vs −0.222). The design expects countering (m_k down to −γ_k).
  2. One relationship gives opposite signs at adjacent scales: a follower at 0.6 s gives −0.07 at 0.53-s nodes and +0.14 at 1.07-s nodes (K5); on rhythmic channels a 3/4-period lag reads as the reverse lead (K3). The phase slope index exists precisely to avoid this.
  3. The divisive pool makes ρ independent of how much the agent moves. Whenever the agent's own channel drifts monotonically (a mood display), ρ becomes a readout of the partner's own Haar curvature: correlation 0.65–0.86 at a drift of 0.02–0.2 per minute (K6). "It feels him only where it is moving" holds only in the sense "where it moves above a tiny floor, at full strength whatever the size."
- **As an emotional agent: mostly the Cayley ledger's agent, with a relational feature extractor added.** Emotion still lives in six innate body gauges; valence and arousal are read from them, not from the new 384-d latent; relational facts (being followed, being ignored, a still face) can change the face and echo strengths but no feeling; the commutator route goes dark when the agent itself is still, which is most of listening; the temperament blocks cannot be trained (below).
- **Buildability on an M1 Pro, 16 GB: inference yes, training of the slow half no.** Online cost is a few ms per frame and tens of MB. But scales 16–24 (9 of 24 blocks) never complete a node in recorded-dyad sessions, and in a first year at 1–2 h a day scale 24 completes 2–5 times (K4). Time scales "from the structure" exist as clocks, not as learned dynamics.
- **Fit to go to the operator under D82: not yet.** It has known concrete failures (items above, §2), and its own novelty verdict needs correcting before the operator sees it. If revised, it should go with the verdict "recombination; one design rule".

---

## 1. Novelty

### 1.1 What the core reduces to

| Element of the design | Existing mechanism | Read here |
|---|---|---|
| Node commutator c = ½(Δa^L Δx^R − Δx^L Δa^R) | Level-2 log-signature (Lévy area) at one dyadic split; Chen/BCH | Morrill 2021; Gyurkó 2013 |
| "Area > 0 means a leads x" | Lead–lag reading of the oriented area; lead matrix | Gyurkó 2013; Bennett 2022; Kaushik 2024 |
| Zero on zero-lag affine copy, signed by direction, antisymmetric (P1, P3) | Imaginary coherency / phase slope index: insensitive to instantaneous mixtures | Nolte 2008 (restating 2004) |
| Expected c per scale | Haar-band quadrature cross-spectrum (K1) | derived here |
| Divisive pool ρ = c / (ε + ½‖v_a‖₁‖v_x‖₁) | Divisive normalisation; coherency normalisation | Carandini & Heeger; Nolte |
| Limiter statistic hypot(trace, antisymmetric part) | Coherency modulus |Re + i Im|, lag-scanned | Nolte; Alkhodari 2026 |
| Multiscale neural CDE driven by interval log-signatures | NRDE; Logsig-RNN | Morrill 2021; Liao 2019 |
| Blocks updating on node completion, holding between | Clockwork RNN with exponential periods | Koutník 2014 |
| Need-conditioned top-8 selection over (channel, scale) cells | Attention over signature patches + fixed-k sparse gating | Moreno-Pino 2024; Shazeer 2017 |
| Own side = efference (S⁰) path | Reafference / efference copy; counterfactual self-model | Bahrick & Watson 1985 (project note); the own-body critic's secure multi-execution |

**K1, the core input is a quadrature spectrum.** For jointly stationary (a, x) with cross-spectrum S_ax and half-node length h frames, G_h(f) = e^{i2πfh} − 1:

  E[c_j] = −∫ |G_h(f)|² sin(2πfh) Im S_ax(f) df.

The real (co-)spectrum drops out exactly. Checked on a constructed follower: data mean vs quad-only prediction −0.00451 vs −0.00440 (j = 4), +0.00818 vs +0.00836 (j = 6); the co-spectrum alone would have given the opposite sign at both. At j ≥ 8 both are within sampling noise of zero. So the mean ρ array is, up to the normalisation, a Haar-band imaginary coherency. Its copy-blindness is Nolte's insensitivity to volume conduction under another name.

### 1.2 Is anything genuinely new?

- **Mechanisms: none.** Every operator in the core and the limiter is an existing one (table above). The design's own §7 says so for the core; it is also true of the two elements §7 calls "genuinely different".
- **One design rule is distinctive: the efference-anchored quadrature restriction.** The partner enters the agent's state only as a same-channel, zero-lag-blind, antisymmetric statistic computed against the agent's counterfactual own path (what it would have done had he held still), never as his increments, levels or cross-channel brackets. I found no prior work that uses imaginary-coherency-type statistics as the *only* gate from another agent into an agent's state, or that anchors them to an efference counterfactual. That is a design rule (an input restriction on the NRDE class, motivated by an existing invariance), not a mechanism: it adds no computation that the excluded frameworks cannot express, and §3.3 of the design shows the restriction does not even bound what the core can know (C4) or copy (P6–P7). By the brief's own test ("a synthesis counts as new only if it adds a mechanism neither source has"), it does not clear the second novelty clause.
- **Is it on the level of attention or Transformers?** No. Attention introduced a new computation (content-addressed soft selection) that changed what a network can do per parameter. This design introduces a choice of which existing features to feed an existing network.

### 1.3 Corrections owed to the design's novelty section

- §7's "What is genuinely different" should cite imaginary coherency and the phase slope index for the invariance, and coherency (modulus vs imaginary part) for the shared 2×2 statistic.
- §2.3's heading "⟵ new mechanism" and §2.7's "new form" should be removed. "New" applies only to the design rule in §1.2.

---

## 2. The agent

### 2.1 Concrete failures of the new parts

1. **The sign of ρ is not "who led" (P3 is false as stated).** Bennett et al. state it for the same metric: it cannot tell "i leads j, negatively" from "j leads i, positively". K2, same channel, 0.6-s lag: partner follows +gain +0.221; agent follows +gain −0.221; partner follows −gain (countering) −0.222; agent follows −gain +0.221. The design wants countering (rival brow relaxation, smile suppression; m_k to −γ_k) and has the slow blocks learn the relationship from the ρ array. A rival who suppresses his smile when the agent smiles is then encoded as "the agent follows him". A learned H can only separate the two cases with information the mask removed (his increments or levels on that channel).
2. **Lead direction aliases across scales and on rhythms.** One follower at 0.6 s, own motion smoothed 0.3 s: mean ρ −0.05 at 0.53-s nodes, +0.22 at 1.07 s, +0.06 at 2.13 s, about 0 elsewhere (K5). A 2-s rhythm followed at 1/4, 1/2 and 3/4 period gives +0.635, 0.000 and −0.635 (K3). So the design's table in §3.2 ("depths 1–3: who flashes first; 4–6: returned smiles") is wrong cell by cell: a returned smile at 0.6 s is invisible at depths 1–3 and *negative* at depth 4. Individual cells sample the odd part of the increment cross-correlation near lag 2^{j−1} frames, with side lobes. A phase-slope estimate (Nolte 2008) reads a pure delay's direction without this aliasing.
3. **When the agent's own channel drifts, ρ is the partner's own curvature.** With own increments equal in both halves (a ramp), c = ½δ(Δx^R − Δx^L) and the pool divides out δ: ρ = (Δx^R − Δx^L) / (2(|Δx^L| + |Δx^R|)), a function of the partner alone, signed by the agent's drift. K6, partner smile bursts 4/min, own drift 0.002 / 0.02 / 0.2 per minute: correlation of ρ with his normalised Haar curvature up to 0.53 / 0.68 / 0.86 at 17–137-s nodes. The agent's slow mood displays are exactly such drifts. So at episode and session scales the "relational" input is largely "his smile onsets, times the sign of my mood trend". More generally, per node c = ½ v_a^⊥ · v_x is his increment pair projected on a direction set by the agent's own pair, so any fixed own shape turns ρ into a normalised linear readout of his motion; only the average over many nodes is lead–lag. This is knowing, which D81 allows, but it is not lead–lag, and it is a partner-only signal at full strength however little the agent moves, which §3.7's R1 says cannot happen. The routes critic should check whether H can integrate this into a slow, partner-shaped display (it passes the hold-blind test because his onsets, not his holds, drive it).
4. **The route goes dark when the agent is still, which is most of listening.** The own side is S⁰, which excludes everything his face does to the agent. While he speaks and the agent listens, the agent's autonomous channels are mostly at rest (no visemes, no own appraisal beyond his words). Below the floor ρ → 0 on every such channel. The design gives no number for how often a_k exceeds the floor during the partner's turns. People are most attentive to the other's face when they are still and listening.

### 2.2 Against the brief's agent criteria

| Criterion | What the design gives | Verdict |
|---|---|---|
| Rich learned latent in which emotion can emerge | z ∈ [−1, 1]^384, trained only by self-prediction (own face, own b, next ρ, his word-decoded need). Valence and arousal "read out as in Cayley: from the drive's change and from b" (§9). z never drives b. | **Hollow at the centre.** The affect itself is the six innate gauges of the Cayley ledger; z is a predictive model of the dyad attached to them. Nothing argues or shows that z carries emotion-like structure, and the emotion readouts bypass it. The brief's warning about cores that "reduce to a few scalar gauges" applies to b, unchanged. |
| Own-body reading of the other | R2: his levels through Π̃ (Cayley's inverse expression map) → own appraisal → b, rank ≤ 6. R1: the commutator. | **Inherited, plus a contingency statistic.** An earlier Cayley critic found that what is inverted is an own display map, not a generative body model (critique-design-cayley-ledger-novelty §1.2, on revision 1); whether that still holds of Π̃ in revision 8.3 is the Cayley design's matter, and it carries over unchanged. R1 is a Bahrick–Watson contingency measure, not a simulation through one's own body; with item 3 above it is partly not even relational. Fine distinctions of a still face never reach the slow state (the design's own risk 9). |
| Time scales from reflex to temperament from the structure | 24 clocked blocks, leak tied to node length. | **As clocks, yes (Koutník); as learned dynamics, no** (§3). Contact time only: between sessions nothing changes. The core cannot represent how long he has been away, so separation and reunion (Ainsworth; project note ainsworth-1978-strange-situation.md) have no place in z. Whether b handles absence is the Cayley ledger's matter. |
| Satiable drives | Cayley 𝒟(b), unchanged; ρ drives no body variable and no objective. | **Satiable, and deliberately inert to contingency.** The design rejects linking "being followed" to any drive, to avoid attention-seeking. The cost: the best-replicated affective effects of contingency do not happen. A still face (Mesman 2009 meta-analysis: positive affect down, negative up) and a non-contingent replay (Murray & Trevarthen 1985; Nadel 1999: fewer smiles and less gaze under replay) change the infant's *feeling*. Here a yoked or frozen partner changes ρ (C9) and, through learning, displays and echo strengths, but never the agent's body state or valence. A satiable "contact" variable credited by contingency rather than by his smiles would not be flattery: the design should argue why it cannot have one, not just reject it. |
| State-to-expression path | g(z, b) → display; m_k(z) echo strengths; posture; all through the limiter. | **Present, limited by the limiter's own cost** (29 % loss on legitimate partner-caused content, the design's risk 2), and m_k is read from blocks that will not be trained (§3). |
| Coupling to Claude without text | Cayley's forked drafts, scored by predicted own-body change over a 30-s rollout with z as rollout state (D84). | **Inherited, unchanged.** The rollout requires z's slow blocks to predict something; at deploy they are constant. |

**What it fails to explain from emotion science** (beyond the above): emotions as responses to events with an object (appraisal of his words is Cayley's, not derived from the core); action readiness (the only choices are which draft and when; nothing in the core produces approach or withdrawal); emotion concepts and their naming (no categories form in z; nothing for Claude to name). Kauttonen et al. 2023 show that a stranger's mere presence changes a listener's own facial recurrence structure and *lowers* synchrony; the core, driven only by same-channel lead–lag and a 6-d body route, has no channel for "being watched" other than b.

---

## 3. Buildability on an M1 Pro-class Mac, 16 GB

**Inference: yes, with margin.**
- Parameters: about 300k in the core (modules 3–10) plus the Cayley ledger's about 522k perception/readers/scorer. Under 1M in total, a few MB in float32.
- Tree: 33 channels × 24 scales × 4 open half-increments: about 3k floats. The design's < 0.05 ms per frame is plausible.
- Core: about 30 block updates per second per run (Σ_j 30/2^j), 35 runs, ≈ 0.1 MFLOP each: about 0.1 GFLOP/s. The design omits the cost of re-running the appraisal and body route in each of the 34 counterfactual runs (S^k holds one of his channels and re-runs Π̃ and the readers). At the Cayley ledger's sizes that is of order 1 GFLOP/s, still well within an M1 Pro's CPU, but it should be counted.
- Limiter: about 2.4M multiply-adds per frame, 72 MFLOP/s; EW state about 10 MB, lag buffers about 3 MB. Fine.
- Persistence of z, the open tree nodes and the limiter state: tens of MB. Fine.

**Training of the slow half: no, as specified (K4).**
- **Recorded dyads cannot train scales above about 15.** A 10-, 20- or 60-min session completes its deepest node at scale 14, 15 or 16. Blocks 16–24 (144 of 384 dimensions) receive no completed node in the about 400 dyad-hours of pretraining, so the shared MLPs F, H and G are never trained at their scale codes e_16…e_24. At deploy those blocks run on scale codes the network has never seen.
- **Living gives almost no samples.** Completed nodes in a first year at 1 h / 2 h of contact a day: scale 16, 602 / 1,203; scale 18, 150 / 301; scale 20, 38 / 75; scale 22, 9 / 19; scale 24, 2 / 5. The self-prediction targets for the slow blocks (next ρ array at that scale, own face at that scale) are as few. Temperament "from the tree" is a block that updates twice in the first year, trained on two targets.
- **Backpropagation through those spans is not possible nightly.** One scale-20 node is 1M frames; the design does not say how gradients reach blocks whose state was set days or months earlier. Truncation treats them as inputs, so their dynamics are not learned at all.
- **Downstream effects.** m_k (echo strengths) reads z_10…24 and the selection query reads z_18…24 and b; both are fitted on dyads in which z_16…24 never moved. When those blocks start moving months into living, both meet inputs they were not fitted on. The echo stays under G_k, so this is not a safety failure, but per-relationship echo strengths will move for reasons unrelated to the relationship.

---

## 4. What a revision would need

1. **Correct the novelty section** (§1.3): cite imaginary coherency / the phase slope index for the invariance and coherency for the shared statistic; remove "new mechanism" and "new form"; state the one distinctive element as a design rule. Put it to the operator, if at all, as "recombination; one design rule".
2. **Fix what the input means.**
   - Either give the core the information to separate direction from association (for example the same-channel co-spectrum sign alongside the quadrature, which is zero-lag-sensitive, so its route must be audited), or stop claiming that the sign is "who led" and let H learn the joint pattern, with an ablation that tests it on recorded dyads containing countering.
   - Replace per-cell sign readings with a phase-slope-type direction estimate across adjacent scales, or show on recorded dyads that the learned core decodes the side-lobed pattern.
   - Address the per-node partner readout (item 3 of §2.1). Per node, c = ½ v_a^⊥ · v_x: his two half-increments projected on the perpendicular of the agent's own pair. Detrending the own path does not help (it leaves −¼ d_a s_x, his node increment signed by the agent's own curvature). Only the *expectation* over many nodes is relational (K1). Two options: feed the core a running mean of c per (channel, scale) instead of per-node ρ; or drop the own-amplitude factor from the pool so the input really is in proportion to the agent's own motion. Re-run C2, C6 and C8 with the change.
   - Report how often a_k exceeds the floor during the partner's turns on recorded dyads (with each person's own path standing in for S⁰, with the Bahrick–Watson caveat).
3. **Make the latent carry affect, or say it does not.** Either derive valence and arousal, or the body variables' set points, from z (so that emotion emerges in the learned state, Principle 2), with an ablation that removes the relational blocks and shows a change in affect, not only in display; or state plainly that the design's affect is the Cayley ledger's six gauges and that z is a dyad model.
4. **Decide on contingency and affect.** Argue from the still-face and double-video findings either for a satiable variable credited by contingency itself (not by his smiles, attention or time), with a proof that it cannot reward seeking, or for leaving it out, with the predicted failure on those paradigms written as an ablation prediction.
5. **Make the slow scales trainable or drop them.** Options: cap the tree at the deepest scale that recorded data and the first months can train (about 14–16), and put temperament in nightly parameters and slow statistics of the expected ρ array per identity (a running mean is learnable from few nodes); or tie the slow blocks to wall-clock time and train them on summary statistics rather than by backpropagation. State the training procedure for any block whose node outlasts a night.
6. **Count the counterfactual perception cost** in §8.5.
7. **Absence.** If the core keeps contact time, say where time apart is represented (b, or a wall-clock input to the slow blocks), so the agent can register a long absence.

None of these touches the limiter's per-expression bound; the routes critic should re-check it after change 2.
