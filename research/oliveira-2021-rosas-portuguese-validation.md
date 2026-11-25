# Oliveira, Arriaga, Stroessner & Paiva 2021, "Preliminary validation of the European Portuguese version of the Robotic Social Attributes Scale (RoSAS)" (Human Behavior and Emerging Technologies 3:750-758, doi 10.1002/hbe2.311). Secondary source for Carpinella, Wyman, Perez & Stroessner 2017, "The Robotic Social Attributes Scale (RoSAS): Development and Validation" (HRI '17, pp. 254-262, doi 10.1145/2909824.3020208)

Source read: the full Oliveira et al. 2021 PDF from the ISCTE repository (introduction, method, results, discussion; supplementary tables not read). NOT READ: the primary Carpinella et al. 2017 paper. ACM DL and ResearchGate both returned 403, and Semantic Scholar and OpenAlex list it as closed access. Everything below about the original RoSAS is as Oliveira et al. report it, and Stroessner, one of the original authors, is a co-author. The original paper's own alphas, exact instructions and scoring rule are unverified.

## Claims
- Items as reported for the original English RoSAS, three factors of six: "The dimension of warmth is measured by collecting judgments of a robot on the terms (in the original version) happy, feeling, social, organic, compassionate, and emotional. The competence dimension includes capable, responsive, interactive, reliable, competent, and knowledgeable. Finally, perceptions of discomfort are captured by the items scary, strange, awkward, dangerous, awful, and aggressive."
- Response format of the original, as reported: "participants were asked to evaluate how closely various terms (e.g., social, strange, reliable) were associated with their perception of robots, using a Likert-type format scale ranging from 1 (definitely not associated) to 9 (definitely associated; see Study 2 in Carpinella et al., 2017)."
- The RoSAS was built from Godspeed plus the stereotype content model. Its three dimensions "parallel the dimensions of likeability, perceived intelligence, and security concerns (respectively)" in Godspeed, and the authors claim it has "stronger psychometric qualities (i.e., higher eigenvalues and higher levels of reliability)".
- Intended uses as reported: "(1) as a tool to evaluate preexisting robots; (2) as a way to inform the development of new robots ... and (3) to serve as a standardized metric".

## Evidence
- Portuguese sample N = 185 young adults, 9-point association format, 18 translated items, with a 2-week retest.
- "the original scale structure did not present a good fit to our data, with several items not loading onto the expected dimensions". The authors kept 11 items (warmth: emotional, feeling, happy, compassionate; discomfort: dangerous, scary, strange, aggressive; plus competence items; the full competence list was not extracted).
- Abstract: "The scale presented poor to acceptable levels of temporal reliability. We found a positive correlation between the warmth and competence dimensions."
- Warmth did not correlate with Godspeed Likeability in either model, contrary to the claimed parallel.
- Scoring: Oliveira et al. analyse factor scores. Their paper does not state the original's scoring rule (presumably the mean of the six items per factor; unverified).

## License
The RoSAS items are a list of 18 English words, as printed in the secondary source. The license of the original HRI paper is unknown (ACM, closed). Oliveira et al. is a Wiley article and was read from the institutional repository copy.

## Runs on this Mac without a GPU?
n.a.

## Verdict: watch
RoSAS is accepted in HRI and its Discomfort factor (scary, strange, awkward, dangerous, awful, aggressive) is the most direct published read on "the face/voice is unsettling". That makes it a natural companion to Godspeed for an uncanny-valley failure check. Before adoption, read the primary paper for the exact instruction wording, the alphas and the scoring rule. Do not run it from the secondary description alone. The one independent validation we read did not reproduce the factor structure and found poor-to-acceptable test-retest reliability. That argues against any n=1 or repeated-measures use on the same rater. A within-subject ablation failure would be the full-affect agent scoring higher on Discomfort, or no higher on Warmth, than the ablated agent across a powered sample.
