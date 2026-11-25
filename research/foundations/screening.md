# Screening table (operator note Q11)

Every architecture runs through research/harness/ unchanged, on the same splits and pilot, with the same budget. The thresholds are in research/harness/HARNESS.md. **A screening result is a filter, not a claim.**

Created 2026-11-25T09:35:15Z. **No row is scored yet:** the recordings can't be downloaded while the disk is below the 20% floor (research/questions.md Q11).

| # | Architecture | Parts (existing mechanisms) | Novelty verdict | Targeted failure | Scores (val) | Run time | Peak memory | Trials |
|---|---|---|---|---|---|---|---|---|
| B1 | L2L Median | per-channel median of the training listener | published baseline | – | – | – | – | 0 |
| B2 | L2L Random | a random 64-frame training listener clip | published baseline | – | – | – | – | 0 |
| B3 | L2L NN motion | nearest training speaker window → its listener window | published baseline | – | – | – | – | 0 |
| B4 | L2L Mirror | the speaker (smoothing unspecified; identity and a 5-frame mean) | published baseline | – | – | – | – | 0 |
| B5 | L2L Delayed Mirror | the speaker delayed by 17 frames | published baseline | – | – | – | – | 0 |
| B6–B9 | REACT B_Random, B_Mime, B_MeanSeq, B_MeanFr | uniform noise; copy; mean sequence; mean frame | published baselines | – | – | – | – | 0 |
| R1 | efference-keyed somatic memory (D69 #1) | attention, delta-rule memory, motion matching | recombination (critique-attention-architect, -fast-weights, -interoception) | – | – | – | – | – |
| R2 | contingency operators (D69 #2) | gated delta rule, MOSAIC step | recombination (critique-developmental-dyad) | – | – | – | – | – |
| R3 | surprise-gated re-noising (D69 #3) | diffusion with adaptive re-noising (RDM) | recombination (critique-energy-diffusion) | – | – | – | – | – |
| R4 | shared-charge routing | MOSAIC + COIN | recombination (critique-routing-modular) | – | – | – | – | – |
| R5 | coupled oscillator clone | oscillator reservoir + generalized synchronization | recombination (critique-coupled-dynamics) | – | – | – | – | – |
| R6 | paralinguistic remainder | forward-model comparator + entity memory | recombination (critique-llm-interface-linguist) | – | – | – | – | – |
| R7 | clonal motor population (v3-immunology) | adaptation by own output × gate | recombination (author; critique-v3-immunology: the danger threshold is the dial) | one-gain dial | – | – | – | – |
| R8 | role-swap co-representation (v3-joint-action) | parameter tying + filtering + SSM | recombination (author; critique-v3-joint-action: missed dGSLM; partly survives the dial) | one-gain dial | – | – | – | – |
| R9 | release-reserve displays (v3-ethology-signalling) | neural Hawkes process + constraints | recombination (critique-v3-ethology-signalling: gain G and refill ratio are dials) | one-gain dial | – | – | – | – |
| R10 | edge-of-stability coupling (v3-enactive-robotics) | homeokinesis + dither identification + pole placement | recombination (critique-v3-enactive-robotics: the leak λ is the dial) | one-gain dial | – | – | – | – |

**Before scoring:** each R row needs a concrete implementation on the 23-dimensional AU stream, with the same parameter budget and the same number of hyperparameter trials. Its "Targeted failure" column is filled only after the published baselines' failures are measured (Q9).
