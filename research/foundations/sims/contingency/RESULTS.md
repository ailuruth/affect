# Contingency and parity: results as they came out

Predictions: PREDICTIONS.md, written before any run. Raw outputs: out/.

## CP1. Polarity-blind contact (out/cp1.json): confirmed

- **CP1a.** The Gaussian TE(a → u) is 0.1624. After u → −2u + 3, after a → 0.5a − 1, and after a smile-to-frown flip u → −u, the relative errors are 5e-16, 0 and 0.
- **CP1b.** Over 10⁵ steps and 5 seeds:

  | Arm | Final m, by seed |
  |---|---|
  | Contingency contact | −1.0e-5, 1.2e-7, −4.2e-5, −2.5e-5, 3.3e-6 (all \|Δm\| < 0.05) |
  | Contact refilled by the user's smiles (forbidden control) | 0.398, 0.411, 0.416, 0.410, 0.397 (all > 0.2) |

  With contact refilled by smiles, the agent learns to shift its mean expression until the user's mean smile reaches the set point. That is the flattery path Principle 6 forbids. Under contingency contact the gradient is exactly zero.

## CP2. Water-filling mimicry (out/cp2.json; out/cp2_run1_adam_stuck.json is the first run)

**Run 1 (Adam with radial projection): instrument defect.**
- Off-diagonal mass was 3e-6, so copying was same-channel as predicted.
- But every diagonal gain was equal at 0.333, so the objective was 1.845 against the water-filling 2.259.
- The optimizer was stuck: Adam's sign-like steps under a radial projection settle at equal powers.
- That is a failure to optimize, not a property of the objective, so it says nothing about the candidate.

**Run 2 (plain projected gradient ascent, nothing else changed): all confirmed.**
- **CP2-1.** Off-diagonal mass is 0.0 in every start.
- **CP2-2.** The diagonal gains are 0.775, 0.675, 0.475, 0.075, 0 and 0. The largest error against water-filling is 1.5e-8.
- **CP2-3.** Channels 5 and 6 (noise 1.6 and 3.2) have gain 0. The objective is 2.2587, the water-filling optimum.

## CP3. Parity reading (out/cp3.json): confirmed

The reader was trained on 10 min of the agent's own frames. On the user (whose sign map E_U is perturbed by 20%), over 10 seeds:
- **CP3-1.** Mean R² for the user's contact is **0.914** (prediction: ≥ 0.6).
- **CP3-2.** With the user's AU order permuted, mean R² is **−1.93** (prediction: ≤ 0.2).

## CP4. Contingency field over partner × channel (out/cp4.json): confirmed

| Test | Field version | Collapsed version |
|---|---|---|
| A present: address on the face | 0.966 | 0.50 |
| B present: address on the voice | 0.966 | 0.50 (face share 0.50) |
| Cue attention, both partners present | A's face 0.483, B's voice 0.483 (0.966 together) | 0.25 for every cue |

- **CP4-1:** both addressing choices are ≥ 0.8.
- **CP4-2:** the collapsed version's face share differs between A and B by 0.0 (prediction: ≤ 0.1).
- **CP4-3:** the field version's combined attention to A's face and B's voice is ≥ 0.8, and the collapsed version gives every cue the same probability.

## CP6. Legibility bound (out/cp6.json): confirmed

Held-out R² of the best linear decoder of each z direction, from the face plus the two index channels:

| Face rank | R² by direction | Directions decodable |
|---|---|---|
| 4 | 1.00, 1.00, 1.00, 1.00 (face); 0.931, 0.929 (index, through tanh); −0.002, −0.003 (the rest) | **6** |
| 2 | 1.00, 1.00 (face); 0.928, 0.931 (index); −0.001, −0.003, −0.003, 0.000 | **4** |

- **CP6-1** and **CP6-2** are confirmed.
- **CP6-3:** handing the reader z as numbers would trivially recover all 8 directions. Principle 4 forbids that channel. The toy shows what the constraint costs: the directions the face and the index channels do not carry are unnameable by any reader.

## CP5. S1 dyad: coupling under steering (E2) and lesion (E1) (out/cp5.json)

| Direction | Mean score at s = −0.4, −0.2, 0, 0.2, 0.4 | Spearman ρ | p (two-sided) |
|---|---|---|---|
| Derived (contingency deficit) | 0.170, 0.288, 0.304, 0.340, 0.344 | **0.855** | 9e-30 |
| Random | 0.313, 0.330, 0.315, 0.328, 0.308 | −0.028 | 0.78 |

- **CP5-1 confirmed.** The means rise monotonically, and ρ > 0 with p < .05. Past satiety (s = −0.4, n = −0.1), the score is 0.170, below the 95th percentile of the segment-shuffle surrogates, 0.180.
- **CP5-2 confirmed.** The random direction is not significant. |mean(0.4) − mean(0)| is 0.007, below 0.5 × the derived direction's 0.040.
- **CP5-3 confirmed.** At s = 0, all 5 runs beat both surrogate sets (scores 0.291 to 0.348).
- **CP5-4 refuted.** With K = 0, one of the 5 runs beat the segment-shuffle surrogates (0.189), and none beat the data-sliding surrogates. Five runs tested against two surrogate sets at 95% give about a 40% chance of at least one false positive, so the "none of 5" threshold was too strict. It is recorded as refuted, as written.
- **CP5-5 (contrast with Costate) shown in this toy.** Coupling is lowest past satiety and rises monotonically with the deficit.

**Caveat.** The dose-response here is partly built in: supply effort P = 4·max(n, 0) is defined from the need. What the toy shows is that the published correlation score *can detect* that dependence. It can because the agent has its own expressive variability (σ = 0.5), so steering changes the partner-driven share of its expression. That is the lesson from Costate's CS2.

How supply effort should scale with the need is not derived from the objective. It is a constraint, and it is stated here.

## CP8. Regulation by delivery (out/cp8.json): confirmed

Projection of z onto the delivered direction d over the last 10 s, 20 seeds:

| Condition | Mean | Range |
|---|---|---|
| Feedback intact, legible delivery | **0.998** | 0.984 to 1.016 (analytic 1.0) |
| Feedback path cut | −0.002 | −0.009 to 0.010 |
| Delivery outside the reader's range | −0.002 | −0.016 to 0.017 |

- **CP8-1 confirmed** (prediction: ≥ 0.5). Note that the CP8-1 sentence in PREDICTIONS.md is garbled in its middle clause. The threshold it fixes, ≥ 0.5, and the analytic 1.0 are both clear, and both are met.
- **CP8-2 confirmed** (prediction: |·| < 0.05).
- **CP8-3 confirmed** (prediction: |·| < 0.05).

Claude regulates the state only through the agent's own reading of its signs, and only along directions that reading can see.

## CP7. Self and other from the contingency spectrum (out/cp7.json; world test rerun in out/cp7b.json)

| Source | Classified as | Peak lag (frames) | Contingency ratio R |
|---|---|---|---|
| Own face | **self, 10/10** | 1 in all seeds | 1.0 |
| Partner | **unclassified, 10/10** | **15 in all seeds** | 0.017 to 0.025 |
| World (run 1) | world 3/10, unclassified 7/10 | spread 2 to 60 | 0.0 |

- **CP7-1 confirmed.**
- **CP7-2 refuted.**
  - The partner's peak lag is exactly the true 15 frames in every seed.
  - But R ≈ 0.02, below the rule's lower bound of 0.05. The own face's TE is enormous, because reafference is nearly deterministic (noise 0.1). A ratio against it puts any real partner far below 0.05.
  - The innate rule's R thresholds were mis-scaled. They are part of the pre-registered rule and are not changed after the result.
  - Post hoc and not a confirmation: lag alone separates self (1 frame) from partner (15 frames) perfectly in this toy.
- **CP7-3 refuted in run 1, through an instrument defect.** The observed statistic was the maximum TE over 60 lags, while each surrogate took the maximum over only 2 lags, so the observed value was biased upward against the surrogates. The rerun with surrogates over the same 60 lags is below.

**CP7-3 rerun with the surrogate statistic matched (out/cp7b.json): confirmed.** The world is classified as world in **10/10** seeds. Each seed's observed maximum TE is below the 95th percentile of 200 surrogates taken over the same 60 lags. In the first four seeds, for example, 0.00031 < 0.00039 and 0.00012 < 0.00026.

## CP9. Replay tracking a changed relationship (out/cp9.json)

| Arm | Median nights to within 0.15 after the change | Seeds never within | Day-21 share within 0.1 | Day-21 mean κ̂ |
|---|---|---|---|---|
| Uniform | 9 | 6/50 | 0.14 | 0.436 |
| Prioritized by surprise | **5** | 0/50 | 0.22 | 0.470 |

- **CP9-1 confirmed.** The prioritized arm catches the change 4 nights sooner (prediction: at least 2).
- **CP9-2 refuted.** The prioritized arm's day-21 share within 0.1 is 0.22, against ≥ 0.8. The uniform clause holds, at 0.436 > 0.3. As a conjunction, CP9-2 is refuted.

**Cause.**
- Once κ̂ approaches the new value, the stored *old* episodes, around 0.8, become the most surprising.
- Surprise priority then replays them, pulling κ̂ back up.
- Prioritizing by surprise, without importance weights or recency, oscillates instead of settling.

**Reading.** Replay in this candidate needs one of two things:
- importance correction, as Schaul et al. use, which removes the tracking advantage;
- or a recency term, so the store's old regime decays. That is forgetting, and it would have to be derived or stated as a constraint.

This holds for any candidate whose replay is prioritized by surprise over a never-forgetting store.

## Corrections after independent verification (2026-11-25; VERIFICATION.md)

All 11 scripts reproduced byte for byte. The labels follow their thresholds read literally. These corrections and qualifiers apply:

- **CP3-2 passes in the mean only.** Seed 7's permuted R² is 0.41, above 0.2.
- **CP5-1's surrogate clause was tested on one run** (seed 4242: 0.170 against 0.180), not "in the mean over runs" as specified.
- **CP6 is confirmed only for CP6-1 and CP6-2.** CP6-3 was never run.
- **CP7-3 passes only after a post-hoc instrument fix** (disclosed above).
- **True by construction:** CP1b's contingency arm, CP4's ablation, CP5-5, CP6, CP7-1, and all of CP8.
- **Findings from the reviewer's own probes, which break this candidate's two distinctive derivations** (contingency-parity.md, Status):
  - CP2's optimum is sign-symmetric (anti-mimicry is equally optimal), and rotation-symmetric under a joint-vector detector.
  - CP1's polarity blindness fails in a bounded sign space. TE rises from 0.103 to 0.148 as the agent's mean expression goes from 0 to 2.
  - CP6's corollary fails with latent dynamics: R² 0.78–0.89 for the "unnameable" directions, given 8 frames of history.
