# What Works Clearinghouse Procedures and Standards Handbook, Version 5.0 (IES/NCEE, August 2022, revised December 2022; WWC 2022008REV)

Source read: full PDF from ies.ed.gov. Read verbatim: the summary of changes, Chapter VI (single-case designs), the design-comparable effect size section, and the passage on nonoverlap of all pairs (NAP). Also read the summary of changes and SCD standards in the Standards Handbook Version 4.1 (2020) for comparison.

## Claims
Changes since 2010:
- 4.1 (2020): the "pilot" label was removed. The procedures for synthesizing single-case findings now use "design-comparable effect sizes". The 2010 Strong/Moderate/No Evidence visual-analysis rating does not appear in the 4.1 SCD standards or in v5.0 Chapter VI. In 5.0, visual analysis is mentioned only for data availability, and NAP is described as "analogous to some of the visual-analytic judgments". This is my reading of what is absent; I found no statement that the rating was formally withdrawn.
- 5.0 reversal design. Without Reservations: "the first baseline phase must have at least six data points, and at least two phases per condition must have five or more data points per phase." With Reservations: "two phases per condition must have three or more data points per phase." A case needs at least four phases.
- 5.0 multiple baseline. At least six phases, with "at least three unique timings". Without Reservations: "the first baseline phase within each tier must have at least six data points", and later phases need at least 5. With Reservations: "three phases per condition must have three or more data points per phase". Tiers must be concurrent. Tiers can be "outcomes or contexts within a single" case.
- 5.0 alternating treatments. Without Reservations: "at least five data points per condition"; With Reservations: four. "a maximum of two sequential data points of the same intervention condition", unless the order is fully randomized.
- New exception: "Any phases with three or more data points and zero within-phase variance" count as long enough.
- New "limit risk of bias" step, which uses NAP (Parker & Vannest 2009). Baseline trend: compare "the last three data points with all other data points within the initial baseline phase. A nonoverlap of all pairs of .85 or smaller will be considered evidence of minimal baseline trends." Reversibility: compare the return-to-baseline phase with the initial baseline; "A nonoverlap of all pairs of .85 or less will be taken as evidence of achieving at least minimal reversibility." A failure on either drops the rating to With Reservations. The footnote calls .85 "relatively arbitrary and novel".
- Interassessor agreement: at least .80 percentage agreement or .60 kappa. It is collected in each phase on at least 20% of data points, now pooled across all data rather than per condition. Interassessor agreement is the required form of reliability "For these direct observation outcomes". Other outcomes must give other evidence of "acceptably low levels of measurement error", such as internal consistency or test-retest reliability. For automated AU coding, the project must cite that tool's published reliability.
- Manipulation: "Randomization designs or masked visual analysis designs are considered to have satisfied this requirement."
- Residual (carryover) effects: if a content expert and a reviewer agree they are likely, the finding "is rated Does Not Meet WWC Standards".
- Design-comparable effect size (Pustejovsky et al. 2014, a multilevel REML model) "only can be estimated from treatment reversal/withdrawal designs and multiple baseline/multiple probe designs with three or more individuals."

## Evidence
A procedures document. It states that the thresholds come from expert consensus: "A small working group of methodologists and applied single-case design researchers arrived at this critical threshold".

## License
"This report is in the public domain."

## Runs on this Mac without a GPU?
Yes. NAP is a pairwise count. The design-comparable effect size needs at least 3 individuals, so it is not applicable here.

## Verdict: adopt (as the current design standard)
Rate S5 and S6 designs against the v5.0 numbers, which are stricter than 2010: the first baseline needs 6 points. Use NAP ≤ .85 for baseline trend and for reversibility. With one operator there is no design-comparable effect size and nothing to synthesize: WWC intervention reports need "at least 20 cases across studies". So the project can claim at most a single study that meets standards, not an effective intervention in WWC terms. Use the 2010 visual-analysis rule to say whether an effect was shown, and state that this rule comes from the 2010 pilot. Failure means:
- the rating is Does Not Meet;
- NAP > .85 on the initial baseline's trend or on reversal, which caps the rating at With Reservations;
- likely carryover between AI-on and AI-off blocks, such as the operator's learned expectations, which gives Does Not Meet for alternating or third-condition designs.
