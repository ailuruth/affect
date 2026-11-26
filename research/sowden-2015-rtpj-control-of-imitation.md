# The role of the right temporoparietal junction in the control of imitation (Sowden & Catmur)

Sophie Sowden & Caroline Catmur, *Cerebral Cortex* 25(4):1107–1113, 2015 (online 31 Oct 2013), doi:10.1093/cercor/bht306 (PMC4380005, CC BY-NC).

## What was read
The full PMC open-access text (JATS XML from the PMC OAI service): abstract, Introduction, Methods, Results with Table 1, Discussion and the figure captions. The figures themselves were not seen; the effect sizes below are computed from Table 1.

## The computation, precisely
**What "control of imitation" is taken to be.** The authors define it as switching between two co-active representations in one motor code:
> "I intend to lift my index finger, and activate the motor representation for index finger lifting; but the sight of someone else lifting their middle finger activates the motor representation for middle finger lifting. I need to inhibit the motor representation of the other person's action and to excite my self-generated motor representation in order to perform the task successfully."

They use "switching between" to mean "this process of exciting the self-representation and inhibiting the other-representation, or vice versa". Note **"or vice versa"**: perspective-taking and ToM use the same operation with the sign reversed (excite other, inhibit self).

**Design.** n = 16 (3 more excluded for >15% errors). Within subjects: neuronavigated rTMS over rTPJ (MNI 54, −47, 26, the mean peak of Brass 2005/2009 and Spengler 2009) vs a mid-occipital control (0, −95, 26). 6 pulses at 10 Hz, 110% of resting motor threshold, **delivered online at stimulus onset** on every trial. Imitative and spatial compatibility were crossed (left- vs right-hand stimuli, after Catmur & Heyes 2011), plus pixelated-hand baseline trials. Stimulus shown 480 ms. 18 trials per cell per site.

**Table 1 (mean RT, ms; SC/SI = spatially compatible/incompatible, IC/II = imitatively compatible/incompatible):**

| | rTPJ | MO control |
|---|---|---|
| SCIC | 425.9 | 431.2 |
| SCII | 447.2 | 444.5 |
| SIIC | 488.7 | 500.8 |
| SIII | 506.6 | 502.1 |
| baseline L / R | 469.9 / 469.9 | 467.8 / 474.1 |

My arithmetic from the table: **imitative compatibility effect ≈ 19.6 ms under rTPJ TMS vs ≈ 7.3 ms under control**; spatial effect ≈ 61 ms vs ≈ 64 ms (unchanged). Statistics: main effect of spatial compatibility (437 vs 500 ms), F(1,15) = 65.53, η² = .81; main effect of imitative compatibility (462 vs 470 ms), F(1,15) = 11.44, P = .004, η² = .43. **Site × imitative compatibility F(1,15) = 5.10, P = .039, η² = .25; site × spatial F < 1, P = .647.** Baseline RTs did not differ by site. Errors (<7% overall) showed no site interactions.

**The authors' own caveat, which matters for the design:** the effect may reflect *selectivity of the mapping*, not "social" per se:
> "the TPJ may be involved in controlling competing representations (regardless of modality) when there is a high degree of overlap between these representations, and thus, greater selectivity is required to inhibit one representation and to excite another."

An imitative match (index↔index) is a one-to-one map; a spatial match (left↔any left response) is diffuse.

## What it means for the designs
- **The guard acts on the high-overlap, one-to-one component of the body map.** Under the authors' alternative reading, rTPJ is needed exactly when the other's representation is nearly identical to a self representation. For a face, the partner-to-own action-unit map is the most one-to-one map the agent has. It is the component that needs a self/other partition. Diffuse cues (the partner moved, the partner is on the left) do not.
- **Removing the operator increases copying ~2.7× (7 → 20 ms) without changing baseline speed or the spatial effect.** That is the ablation a design should reproduce: delete the partition and the copy component of the response grows, while perception and other stimulus–response mappings stay the same.
- **The operation is two-sided and signable.** "Excite self, inhibit other, *or vice versa*" is one operator with a direction set by the task. That is the same object needed for reading the other (Principle 3) and for not copying.
- **Time scale:** acts within the 480 ms trial (online TMS at stimulus onset).

## Verdict
**adopt (as the ablation target and the "one-to-one overlap" criterion).** Small n (16), a single site comparison and P = .039 on the key interaction: treat it as suggestive, and note that Darda & Ramsey 2019 find no consistent rTPJ activation for imitative compatibility in fMRI.
