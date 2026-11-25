# Mongile, Tanevska, Rea & Sciutti 2022, "Validating a Cortisol-Inspired Framework for Human-Robot Interaction with a Replication of the Still Face Paradigm" (arXiv 2204.03518v1, cs.RO; submitted to ICDL 2022)

Source read: arXiv PDF v1, full text (4 pp. plus references).

## Claims
- The iCub robot gets an internal "R-cortisol" variable, updated from "stress and comfort levels" computed from human face (OpenFace action units, mutual gaze) and touch (skin taxels).
- Two hand-designed "robot profiles", "Anxious" and "Avoidant", have different sensitivities. For the anxious profile, absence of touch and smiles is a stressor. The avoidant profile has "a higher R-cortisol threshold and faster recovery".
- The study is "a loose replication of the Still Face [18] and Still Face+Touch paradigms", with the robot "in the role of a toddler".

## Evidence
What was adapted:
- Episode durations shrunk to "20” free play, 20” paradigm (SF or SF+T), 20” reunion, 60” free play" (2 min total).
- The roles are kept (robot as infant, human as caregiver who goes still), but the robot never acted. It "was in an active position ... with a smiling face and straight posture, but not moving or reactive". The robot "recorded visual and tactile stimuli" while "the experimenter narrated how the robot would have behaved".
- 6 participants, all female, 3 per profile. Recorded stimuli were replayed offline through both profiles.

How it was scored:
- Not with any published still-face coding. The outcome is the robot's own internal variable: "the average of R-cortisol during the different phases".
- Results come from a mixed model, for example "a significant effect for the robot profile during the paradigm phase ... Still Face Paradigm (β = −0.35, z = −3.18, p − value = 0.001)", plus a Wilcoxon test on match versus mismatch (z = 2.2014, p = 0.0277).
- Parameters were tuned on prerecorded stimuli "with the goal of obtaining the same results present in HHI literature".

## License
arXiv non-exclusive license. No code released that I saw.

## Runs on this Mac without a GPU?
n.a. as an instrument. The model is small, but no code is released.

## Verdict: reject (as an evaluation precedent); useful as a warning
This is the only direct "still-face on an artificial agent in the infant role" precedent I found. It does not use the instrument as published:
- The episodes are 20 s, not 2 min.
- No behavior of the agent was observed or coded. The agent did not move, and its behavior was narrated.
- The outcome is an internal variable that the authors tuned to produce the expected result. That is circular: it shows the equations do what they were set to do.

It also uses an expression classifier route (OpenFace action units to "stress/comfort"), which this project forbids for the agent's own inputs if it maps to labels.

Lesson for our use: score the agent's observable expressive behavior with Mesman's published categories, coded by blind humans (mesman-2009-still-face-meta-analysis.md), never an internal variable. Fix parameters before the run.
