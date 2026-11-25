# Carr, Winkielman & Oveis 2014, "Transforming the mirror: Power fundamentally changes facial responding to emotional expressions" (Journal of Experimental Psychology: General 143(3):997-1003, doi 10.1037/a0034972)

Source read: full accepted manuscript PDF (author-hosted, pages.ucsd.edu/~pwinkielman), all sections; supplemental materials not read.

## Claims
- Social power "fundamentally changes spontaneous facial mimicry ... thereby challenging the direct-matching principle".
- Low-power perceivers smiled to all targets, including to angry faces. High-power perceivers mimicked smiles of low-power targets but not of high-power targets, and smiled to high-power targets' anger.
- Corrugator responses were earlier (before 1,000 ms) and more stimulus-matching; zygomaticus responses were later (2,000-4,000 ms) and carried the context effects. The authors suggest "early responses follow more direct-matching principles ... and later (while still spontaneous) responses reflect influences of the interaction context."

## Evidence
- N = 55 UCSD undergraduates (82% women), 10-min writing prime: high power (19), low power (18), neutral (18). Manipulation check F(2,52) = 48.2, p < .001; no mood or attention (RT) differences.
- Stimuli: 8 MMI database videos (4 people, happy or angry), validated frame by frame with CERT on AU4 and AU12. Target power by subtitle (physician / executive vs fast food worker / stocker). 80 trials of 5 s.
- fEMG zygomaticus and corrugator, left side; z-scored; 500-ms windows; linear mixed models (lme4).
- Corrugator: to anger vs baseline t(54) = 3.75, p < .001, d = 0.51; valence F(1,52) = 11.96, p = .001; valence × target power F(1,52) = 6.87, p = .01 (more differentiated to high-power targets, angry vs happy b = .11, t = 4.30, d = 0.54). No effect of perceiver power.
- Zygomaticus: perceiver power × target power × valence F(2,104) = 3.21, p = .04. Low-power perceivers smiled to anger: vs baseline t(17) = 2.93, p = .01, d = 0.69; vs controls b = .14, d = 0.80. High-power perceivers: smile mimicry to low-power targets t(18) = 2.96, p < .01, d = 0.68; none to high-power targets t(18) = 0.15; smiling to high-power targets' anger t(18) = 3.42, p < .01, d = 0.78.
- Zero-lag corrugator-zygomaticus correlations were not significant in any cell; the two muscles responded with different latencies, not as a blend.
- A follow-up rating study (N = 69) found no power effects on how smiles were classified or rated, so the shift is not explained by explicit reinterpretation.

## What it implies for the design
- The cleanest single paper for "changes shape": the relation between the two agents (here relative status) changes whether a smile is returned and whether anger is answered with a smile. The response depends jointly on the agent's own state and its model of the partner, not on either alone.
- Two time scales inside one response: a fast, more matching brow channel and a slower, context-shaped smile channel. An agent design should allow per-channel latency, with context entering mainly in the slower component. This gives a testable ablation: removing the context input should leave the sub-second corrugator response nearly unchanged and remove the 2-4 s zygomaticus differences.
- Small cells (18-19), one study, priming manipulation; treat as a pattern to test, not a parameter.

## Verdict: adopt (as primary evidence for sign changes and for the early/late split)
