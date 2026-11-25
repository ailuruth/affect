# Plaut & Shallice 1993, "Deep dyslexia: A case study of connectionist neuropsychology" (Cognitive Neuropsychology 10(5):377-500, doi 10.1080/02643299308253469)

Source read: the full PDF on Plaut's CMU page (journal scan, 125 pp.). Read verbatim: the review of Hinton & Shallice (H&S 1991), the lesion procedure, the architecture comparisons, "Effects of Lesion Severity", "Error Patterns for Individual Lesions", the concrete/abstract double dissociation, and the general discussion on syndromes and dissociations. The output-network and Boltzmann-machine sections were skimmed.

## Claims
- A single lesion anywhere along a network that maps orthography to semantics, and on to phonology, produces the deep-dyslexia error pattern: visual, semantic and mixed errors above chance. "the observed distribution of error types is insufficient to determine a patient's lesion location". The result depends on distributed representations, gradient learning, semantic attractors, and richer semantics for concrete words.
- Lesions to the direct pathway give a concrete-word advantage. "severe lesions to the clean-up pathway produce the reverse advantage for abstract words, similar to the concrete word dyslexic patient, CAV". So a double dissociation appears without separate stores for concrete and abstract words: "the specialisation is not in terms of the surface distinction".
- Negative finding: H&S's striking category-specific sparing of foods "did not occur" in "a second network that was essentially the same except for the use of a different random starting point". "the strong dissociations obtained may reflect idiosyncrasies in the learning experience of particular networks."

## Evidence (lesion method as used)
- Lesion types: "removing either a random subset of the units in a layer or the connections between two layers, or by adding random noise to the weights."
- Instances and severities. H&S used "10 instances of each lesion type". Plaut & Shallice used "Twenty instances of lesions" at severities "0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, and 0.7" (the proportion of connections removed), across several architectures. "for a given simulation experiment with 4 locations of 9 severities of lesion, we are creating 720 simulated patients".
- Response read-out is fixed before testing. A response counts if its cosine to some word's semantics is "greater than 0.8" and beats the next word by "at least 0.05"; otherwise it is an omission.
- Comparison to patients:
  - Error categories follow the clinical scheme (Morton & Patterson 1980).
  - Rates are compared with a chance distribution "if responses were chosen randomly from the word set". Only relative rates are compared, because "a random pattern of responding would match the chance distribution of errors and not simply the chance rate for a particular error type."
  - Results are averaged over severities giving "correct performance between 15-85%", because the most severe lesions dominate otherwise and "the correct performance of most of the patients we are considering falls within this range."
  - Individual lesions are checked against single-patient phenomena, such as response reversals.
- Several architectures are compared to see which results generalize. Some H&S findings "do not generalise to all lesion sites of all connectionist networks."

## License
Journal article © Taylor & Francis; the author copy is free to read. No code.

## Runs on this Mac without a GPU?
n.a. as a paper. The method is cheap: re-running random lesions over seeds and severities on a small engine model is CPU work.

## Verdict: adopt (as the ablation protocol for Principle 5)
What makes a lesion result count, taken from this paper and its critics (bullinaria-2005-connectionist-neuropsychology.md, plaut-2003-double-dissociations.md):
1. Many random instances per lesion type: 10 in H&S, 20 here. Report the mean.
2. A sweep of severities, with the analysis restricted to a stated performance band chosen in advance.
3. Compare against a chance or sham baseline, using the distribution of outcomes and not one rate.
4. Replicate across independently trained networks (different seeds) and across nearby architectures. A dissociation that vanishes with a new seed does not count.
5. Fix the read-out criteria before lesioning.

Failure when applied here: the predicted behavior change appears in some lesion instances or seeds but not in the mean; or it appears only at one severity; or it is not distinguishable from a sham lesion of equal size elsewhere. Any of these means the component has not been shown to matter. A "double dissociation" between two of the engine's components is not evidence that they are separate modules (see the critiques).
