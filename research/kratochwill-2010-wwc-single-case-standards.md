# Kratochwill, Hitchcock, Horner, Levin, Odom, Rindskopf & Shadish 2010, "Single-case designs technical documentation" (What Works Clearinghouse, Version 1.0 (Pilot), June 2010)

Source read: the full PDF from ies.ed.gov (wwc_scd.pdf, 34 pp.). Sections B (design standards), C (evidence criteria), D (visual analysis) and E (combining studies) read verbatim; section F (effect sizes) skimmed. The current WWC rules are in wwc-2022-handbook-v5-scd.md; this 2010 text is the only WWC version that states the Strong/Moderate/No Evidence rule.

## Claims
Two stages. Design Standards rate internal validity ("Meets Evidence Standards", "Meets Evidence Standards with Reservations", "Does Not Meet Evidence Standards"). Then reviewers trained in visual analysis rate each outcome "Strong Evidence, Moderate Evidence, or No Evidence".

Design Standards (all must hold to Meet):
- The researcher manipulates the independent variable: "the researcher determining when and how the independent variable conditions change."
- Interassessor agreement: "measured systematically over time by more than one assessor", collected "in each phase and on at least twenty percent of the data points in each condition", with minimums "0.80 to 0.90 (on average) if measured by percentage agreement and at least 0.60 if measured by Cohen's kappa."
- "at least three attempts to demonstrate an intervention effect at three different points in time or with three different phase repetitions." AB, ABA and BAB designs fail.
- "For a phase to qualify as an attempt to demonstrate an effect, the phase must have a minimum of three data points."
- Reversal (ABAB): Meets = "a minimum of four phases per case with at least 5 data points per phase"; With Reservations = four phases "with at least 3 data points per phase".
- Multiple baseline: Meets = "a minimum of six phases with at least 5 data points per phase"; With Reservations = six phases "with at least 3 data points per phase".
- Alternating treatment: "five repetitions of the alternating sequence to Meet Standards"; four = With Reservations; "fewer than four repetitions Does Not Meet Standards."

Evidence rule: Strong Evidence = "at least three demonstrations of the intervention effect along with no non-effects", verified by "at least two WWC reviewers certified in visual (or graphical) analysis". "If a SCD does not provide three demonstrations of an effect, then the study is rated as No Evidence. If a study provides three demonstrations of an effect and also includes at least one demonstration of a non-effect, the study is rated as Moderate Evidence." Things that make a non-effect: no predictable baseline pattern, high within-phase variability, "long latency" or overlap with the projected pattern, inconsistent patterns across similar phases. For a multiple baseline, if untreated tiers change when one tier is treated, "the highest possible design rating is Moderate Evidence."

Visual analysis has four steps and six features: "(1.) level, (2.) trend, (3.) variability, (4.) immediacy of the effect, (5.) overlap, and (6.) consistency of data patterns across similar phases". Level is the phase mean. Trend is the "slope of the best-fitting straight line". Immediacy compares "the last three data points in one phase and the first three data points of the next". Overlap is "the proportion of data from one phase that overlaps with data from the previous phase".

Combining studies needs at least five papers that meet standards, "at least three different research teams at three different geographical locations", and at least 20 experiments in total.

## Evidence
A methods document written by a panel. The three-demonstrations rule is "based on professional convention (Horner, Swaminathan, Sugai, & Smolkowski, under review)". No validation study is reported here.

## License
US government work (IES/ED). Free to reuse.

## Runs on this Mac without a GPU?
Yes. It is a protocol plus plots. Phase scheduling, plotting and nonoverlap calculations are a few lines of Python.

## Verdict: adopt (design standards via v5.0; evidence rule from this text)
This is the protocol the brief names for S5 and S6. With one operator:
- Use a reversal design (A = component off, B = on) with at least ABAB, or a multiple baseline across outcomes or contexts within the operator (three tiers, staggered). Blocks of days are phases. Each day is one data point, or one session per day.
- Blinding the operator is not a WWC requirement. It is the project's own addition and must be reported as such.
- Outcomes must be measured by more than one assessor, or the claim falls back to a reliability argument (see the v5.0 note). This is open for automated measures such as AU coding.
- Failure here means any of these: fewer than three phase changes; any phase under 3 points (under 5, or under 6 for the first baseline in v5.0, for the top rating); fewer than three demonstrations of an effect, which gives No Evidence; or a reversal phase that does not return toward baseline, which counts as a non-effect and gives at most Moderate Evidence. A component whose effect does not reverse within a block of days, such as learned attachment in S6, cannot be tested with ABAB. It needs a multiple baseline instead.
