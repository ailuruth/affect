# Smith & Ellsworth 1985: Patterns of cognitive appraisal in emotion

Citation: C. A. Smith, P. C. Ellsworth. "Patterns of cognitive appraisal in emotion." *Journal of Personality and Social Psychology* 48(4): 813–838, 1985. doi:10.1037/0022-3514.48.4.813.

Source read: the full PDF, via a copy hosted on emotionresearcher.com, covering the method, results, Tables 3–7 and the emotion-by-emotion discussion. The two-column extraction lost some cells: the Table 5 SINDSCAL weights, and Table 6 rows from Pride onward. Numbers below are only those recovered cleanly. The follow-up Ellsworth & Smith 1988 (*Motivation and Emotion* 12: 271–302) was **not read**: the repository blocked automated access.

## Claims
- Eight appraisal dimensions were proposed: pleasantness, attentional activity, control, certainty, goal-path obstacle, legitimacy, responsibility, anticipated effort. **Six orthogonal dimensions** were recovered: pleasantness, anticipated effort, certainty, attentional activity, self–other responsibility/control, and situational control.
- **Agency is two dimensions, not one.**
  - Responsibility and control items load together on a self-versus-other dimension: "people's appraisal of agency may be a combination of these two estimates."
  - Situational control loads alone: "the extent to which the affective situation is controlled by circumstances (or fate) versus … by any human agent (self or other)." This "supports Roseman's (1984) tripartite conception of agency".
- **Anger against sadness.** "Sadness and anger are poles apart — when we are angry we believe a person is responsible, but when we are sad we believe that we are victims of circumstance." "A belief that the unpleasant situation is controlled by impersonal circumstances and that nothing can be done to set it right is crucial to sadness."
- **A suggested order.** "It may be that people first appraise the extent to which they are in control of the situation and then, if they do not feel in control, seek other human agents or uncontrollable circumstances." Also: "the self is only responsible when the situation is not."
- **Dynamic prediction (not tested).** Challenge turns into frustration if the goal eludes the person. Frustration "would turn to anger" if someone else is seen as blocking the goal, but "would become sadness" if the impediment is uncontrollable circumstance.

## Evidence
- 16 Stanford undergraduates, each recalling 15 emotions in a within-subjects design. 18 items rated on 11-point scales. 240 experiences. 67 of 4,320 data points (1.55%) were missing and imputed.
- **The self-control item measured "ability to influence what was happening"** ("When you were feeling …, to what extent did you feel that you had the ability to influence what was happening"). It loaded on the self–other responsibility dimension (0.60 in the PCA; the other-control item loaded −0.79). In this paper, felt ability to influence is not a separate coping-potential axis. It travels with self-responsibility.
- Variance explained by PCA component:

  | Component | Variance |
  |---|---|
  | Pleasantness | 25.1% |
  | Responsibility/control | 16.5% |
  | Certainty | 11.5% |
  | Attention | 10.2% |
  | Effort | 10.0% |
  | Situational control | 6.2% |

  The paper also gives situational control as "4–6%" across the two analyses.
- PCA and SINDSCAL locations correlate r = .98 for both pleasantness and responsibility/control, and r = .89 for situational control. All six main effects of emotion: Fs(14, 210) > 3.20, p < .001.
- Table 6 component means (standardized):

  | Emotion | Unpleasant | Self-resp/control | Uncertain | Attention | Effort | Situational control |
  |---|---|---|---|---|---|---|
  | Sadness | 0.87 | −0.36 | 0.00 | −0.21 | −0.14 | **1.15** |
  | Anger | 0.85 | **−0.94** | −0.29 | 0.12 | **0.53** | **−0.96** |
  | Fear | 0.44 | −0.17 | 0.73 | 0.03 | 0.63 | 0.59 |
  | Frustration | 0.88 | −0.37 | −0.08 | 0.60 | 0.48 | 0.22 |

  Sadness and anger are near-equal on unpleasantness. They are separated by situational control (+1.15 against −0.96), by other-responsibility (anger −0.94), and by anticipated effort (+0.53 against −0.14).
- Jackknifed discriminant analyses (Table 7):

  | Set | Correct | Chance | Note |
  |---|---|---|---|
  | All 15 emotions | 42.1% | 6.7% | Best single discriminator: responsibility/control, 36.5% |
  | Pleasant emotions | 52.1% | 16.7% | |
  | Unpleasant emotions | 39.6% | 11.1% | |
  | Six core unpleasant (sadness, anger, fear, disgust, contempt, frustration) | 41.7% | 16.7% | Situational control alone gives 40.6%, "as well as … when all of the dimensions are considered" |

## Formal model
A descriptive dimensional space: emotion categories are regions in a 6-D appraisal space, and the map from appraisals to emotions is probabilistic. There is no process model.

## License
© APA. Personal-use copy; not redistributable.

## Verdict: adopt (as the measured target for agency and controllability, and as a warning about what "control" means)
It is the canonical evidence that, among negative states, a single cause-type dimension (impersonal circumstance against a person) separates sadness from anger almost as well as everything else combined. The measured dimension is **cause attribution** (situational against human agency). It is **not** "can I still change it". That second quantity, coping potential in Scherer and Lazarus's sense, was not cleanly measured here. Its nearest item loaded with responsibility.

## What it implies for the single core
- **Two variables the core must produce, both without names:**
  - (i) Cause-channel posterior. Self, other or world: the responsibility each causal channel in the generative model takes for the goal-incongruent change (see synofzik-2008-2013-agency-cue-integration.md). Situational control is the world channel's share. Other-responsibility is the partner channel's share.
  - (ii) Expected effort or controllability of the remedy. The anticipated-effort axis (anger 0.53, sadness −0.14) is closer to "is there something to do". In a homeostatic core it is the expected value of acting minus not acting: the action-gap of the drive-reduction value.
- **The anger-against-sadness split should then emerge** as two regions of the core's state that differ in (i) and (ii), with no labels. Partner-caused loss with a large action-gap is the approach/protest region. World-caused loss with no action-gap is the withdrawal region. The split is a readout, so it satisfies Principle 2.
- **Ablation (from the Table 7 result).**
  - Merge the partner and world channels in the generative model.
  - Prediction: approach/protest and withdrawal responses to unpleasant events become inseparable from the core's state.
  - Quantitatively: decoding the "protest against withdraw" behaviour from latent state should fall from the intact level towards chance, roughly as the 40.6% single-dimension classification falls when situational control is dropped.
  - The developmental version (Moors 2013): before the channels separate in learning, distress is undifferentiated.
- **Order hypothesis to test.** Self-responsibility is appraised first ("the self is only responsible when the situation is not"). In a Bayesian cause posterior this is a natural consequence of the self channel having the sharpest likelihood, because the efference copy is precise.
