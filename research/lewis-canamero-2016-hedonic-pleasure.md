# Lewis & Cañamero 2016, "Hedonic quality or reward? A study of basic pleasure in homeostasis and decision making of a motivated autonomous robot"

*Adaptive Behavior* 24(5):267–291, special issue "Grounding Emotions in Robots", doi:10.1177/1059712316666331. (The repository cover sheet misprints the DOI as a *Neural Computation* one.)

Source read: the published version (25 pages) from the University of Hertfordshire Research Archive (uhra.herts.ac.uk/id/eprint/5545/1/Published_Version.pdf), read in full through the conclusion and notes. The reference list was skimmed. Figures were seen only as captions, because the text extraction has no images. Table 2 was reconstructed from the extracted numbers. It is internally consistent: geometric discomfort is at least the arithmetic one in every cell.

Related note: research/canamero-attachment-robotics.md covers Hiolle, Lewis & Cañamero 2014 from the same group (comfort traces, responsiveness). This paper is the group's non-social counterpart. It looks at pleasure acting on perception within a two-resource survival task.

## Claims
- Pleasure need not be reward. Here it is a simulated hormone that acts on the *perceptual* term of each motivation, the incentive salience of the cues, and not on learning.
- Pleasure released by need satisfaction ("Modulated α", Moα) produces a behavior pattern that no fixed α can produce. Its opportunism matches low α and its persistence matches medium α. With any fixed α the two rise together.
- Pleasure unrelated to need satisfaction (a "hedonic quality" released on the act of consuming) can improve viability when it is attached to the scarce resource.
- Whether each form of pleasure is adaptive depends on the environment. In the easy arena the highest fixed α was best. In the hard arena, medium fixed α had the fewest deaths and Moα did worse.

## Architecture (equations as given)
- **Robot and body.** Nao humanoid in a 2 m × 2 m walled arena. Red balls are "food" and green balls are "drink". Detection is by colour and size from the camera. The robot also has sonar, foot contacts and gyroscopes.
- **Physiology.** Two essential variables, energy and hydration, range 0–100, with the setpoint at the upper limit. Deficits $d_i$ grow by 0.1 every 250 ms. Each "bite" of a resource reduces its deficit by 10 (7 in Experiment 3). Starting from deficits of 20, death comes at 3 min 20 s without consumption.
- **Motivation intensity (Eq. 1):** $m_i = d_i + d_i \cdot \alpha \cdot cue_i$. Here $cue_i$ is the apparent radius of the largest visible matching resource (0 if none), and $\alpha$ is one scalar shared by all motivations. The cue term is gated by the deficit, so a satiated need ignores its cue. Same form as Avila-García & Cañamero 2005: $m_i = d_i + d_i\,\alpha c_i$.
- **Behaviors.** A tree of hand-written behaviors:
  - fall recovery (a reflex);
  - return-to-neutral posture;
  - two composite motivated subsystems (hunger, thirst), each with a consummatory act (eat or drink) and an appetitive search (wander, visual search, gaze, approach).
  Each node has an activation threshold. Selection runs every 125 ms: sort the children by activation and run each one that is above threshold and has free actuators. Compatible behaviors run in parallel.
- **Pleasure hormone (Moα).** Every 500 ms the model takes finite differences of each deficit: $d'_t = (d_t - d_{t-0.5})/0.5$ and $d''_t = (d'_t - d'_{t-0.5})/0.5$.
  - Release (Eq. 2): if $d''_t < 0$, then $\Delta^+ h = -d''_t \cdot s$. A bite gives $d'' \approx -40$; with $s = 0.4$ that releases 16 units.
  - Decay (Eq. 3), once per second: $\Delta h = -(h - b)\,k$, with background $b = 10$ and $k = 0.19$ (half-life about 3.3 s above background).
  - Coupling (Eq. 4): $\alpha = 0.01\,h$. At background, $\alpha = 0.1$, which equals the low fixed condition.
  - Only improvements release hormone. Displeasure (a positive $d''$) is mentioned but not modeled.
- **Hedonic pleasure (Experiment 3).** A further 40 units are released on each successful consummatory act for one resource type, independent of nutritional effect. In this experiment $s = 0.8$ and a bite gives $d'' \approx 28$, so the need-linked release is 21.6 units.
- **Metrics:**
  - arithmetic discomfort $D_A = \frac{1}{n}\sum_i d_i$;
  - geometric discomfort $D_G = 100 - \sqrt[n]{\prod_i(100-d_i)}$, which is 100 only at death;
  - variance of the deficits;
  - rates of *attempted* persistence and *attempted* opportunism, defined by which deficit is larger when a resource-directed behavior starts or continues.

## Evidence with numbers
All runs used the real robot, with up to 6 min per run and 10 runs per condition in a randomized order. No inferential statistics are reported anywhere: only means, box plots and example plots.
- **Experiment 1, easy symmetric arena (4 food, 4 drink), 40 runs.** No deaths in any condition.
  - Mean geometric discomfort: low/medium/high fixed α (0.1/0.35/0.6) gave 49.8/33.3/27.1; Moα gave 39.7.
  - Mean deficit variance: 28.0/59.3/71.2 for the fixed conditions; Moα gave 47.0.
  - For fixed α, attempted persistence and opportunism both rise with α. Moα showed low-α opportunism together with medium-α persistence.
- **Experiment 2, a central box and food and drink on opposite sides, 40 runs.**
  - Deaths: low α 9/10, medium α 2/10, high α 4/10, Moα 5/10.
  - Geometric discomfort: 65.7/52.8/50.6 for low/medium/high, and 61.9 for Moα.
  - Variance: 44.9/146.9/192.4, and 89.1 for Moα.
  - The authors stress that Moα was "not optimized in any way". Its parameters were set empirically for interaction dynamics and never tuned for performance.
- **Experiment 3, five conditions, 50 runs.**

| Condition | Arithmetic discomfort | Geometric discomfort | Variance | Deaths |
|---|---|---|---|---|
| 1: symmetric arena, symmetric pleasure | 46.7 | 47.4 | 61.8 | 0 |
| 2: symmetric arena, extra pleasure from drink | 42.5 | 43.4 | 81.5 | 0 |
| 3: asymmetric arena (6 food, 2 drink), symmetric pleasure | 56.6 | 57.6 | 76.2 | 4 |
| 4: asymmetric arena, extra pleasure from the scarce drink | 48.8 | 50.1 | 98.0 | 1 |
| 5: asymmetric arena, extra pleasure from the abundant food | 50.9 | 52.2 | 105.5 | 3 |

  Extra pleasure lowered discomfort but raised variance in every case, including the "wrong" (abundant) resource. That was unexpected. The share of the robot's lifetime spent with each deficit larger shifted toward balance under condition 4 and away from balance under condition 5.

## Failure modes
- **Assembled, not derived.** The motivation formula, behavior tree, thresholds, actuator arbitration, hormone release rule and the hormone-to-α map are separate hand-designed pieces. The authors frame it as "a first step" toward a "systematic study". Nothing ties the hormone to an objective. The second-derivative trigger is a design choice and is not derived.
- **Hand-named variables.** "Hunger", "thirst" and "pleasure hormone" are named and hand-wired. Pleasure is a scalar with one target (α).
- **Nothing is learned.** Every parameter ($s$, $b$, $k$, the 0.01 gain, the thresholds) was "established empirically" by the designers. The authors list "designer (e.g. a human or an evolutionary algorithm)" as who would set them. The robot does not adapt α itself.
- **No persistence.** The hormone half-life is 3.3 s, and each run starts fresh. No state survives across runs.
- **The ablation is real but narrow.** Fixed α is in effect a lesion of the hormone dynamics, and Experiment 3 compares with and without the hedonic release. That is better than most robot-affect work. But there are 10 runs per cell, no significance tests, and outcomes that depend on the arena: the modulated variant was the *worst survivor* except for low α in Experiment 2. The design claim, that pleasure decouples persistence from opportunism, rests on box plots of attempted-behavior rates.
- **The hedonic channel can be gamed.** The authors note it themselves: separating "liking" from nutrition means "the robot could find a resource that is very pleasurable to eat but has little benefit". Condition 5 shows the cost.

## License
CC BY 3.0 (published version). No code released (UrbiScript framework, not public).

## Runs on this Mac without a GPU?
n.a. as code. The model is a few scalar equations and could be re-implemented in an afternoon. The evidence depends on the physical Nao arena.

## Verdict: watch (mechanism adopted in spirit; the model itself rejected)
- Against Principle 2: the named hormone and named drives.
- Against Principle 10: assembled.
- Against Principle 5: no ablation prediction written in advance, and results not tested statistically.
- Consistent with Principle 6: the drives are satiable; pleasure never becomes a quantity the robot maximizes; and it changes salience, not value. That is the right direction.

## What it implies for this engine
- **Pleasure as gain on need-conditioned salience survives.** Eq. 1, $m_i = d_i(1 + \alpha\,cue_i)$, is the scalar ancestor of the brief's need-conditioned attention: the deficit gates the cue, so a satiated need ignores food. The engine should get the same structure from its core, with attention whose query is the current need state, and not from a shared scalar. What the engine adds is content dependence. Here α is shared by every motivation, which is exactly the low-dimensional sketch the brief warns about.
- **A derivative-based hedonic signal is consistent with Hesp et al. and the drive-reduction literature.** Release on $-\ddot d$ (an improvement in the rate of need reduction) is close to "valence as rate of change of expected free energy or deficit". The engine should *read out* such a quantity from its core and not release a named hormone (Principle 2). The paper's own finding is a useful prediction for the engine's ablations: modulation that depends on the *rate* of need reduction separates persistence from opportunism, and a constant gain cannot.
- **Ablation template.** "Freeze the modulator at its own background value" (fixed α = 0.1 equals Moα at rest) is a clean lesion. The engine should copy it: clamp the learned affective modulation at its resting value, and predict persistence falling while opportunism stays unchanged.
- **Warning for the social case.** Hedonic pleasure decoupled from need satisfaction helped when tied to the scarce resource and hurt when tied to the abundant one. In a social engine, a "liking" signal tied to the user's smiles is condition 5 with the user as the abundant, pleasurable resource. That is the flattery path Principle 6 forbids. Any hedonic channel must stay tied to need reduction, or be explicitly satiable.
- **Metric.** Geometric discomfort (100 only at death, weighted toward the largest deficit) is a better summary of multi-need viability than the mean. It is worth reusing for any homeostatic evaluation of the engine's body variables.
