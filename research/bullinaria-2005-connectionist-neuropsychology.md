# Bullinaria 2005, "Connectionist Neuropsychology" (in G. Houghton (Ed.), Connectionist Models in Cognitive Psychology, pp. 83-111, Psychology Press), reviewing Bullinaria & Chater 1995 (Language and Cognitive Processes 10:227-264)

Source read: the author's pre-print of the 2005 chapter (johnbullinaria.github.io/PUBS/CN.pdf), read in full. Bullinaria & Chater 1995 itself was NOT read: I found no free copy. Everything below about B&C 1995 is as Bullinaria reports it. Shallice 1988 (From Neuropsychology to Mental Structure, ch. 10) was NOT read; its quotes below are as cited by Bullinaria.

## Claims
- B&C 1995: "assuming one successfully avoids small scale artefacts, only single dissociations are possible without modularity". The single dissociations come from regularity and frequency: items learned faster and better are more resistant to damage.
- Four damage types, "removing random hidden units, removing random connections, globally scaling the weights, or adding random noise to the weights", gave "very similar patterns of results."
- Small-scale artefacts: in small networks "the effect of individual damage contributions can be large enough to produce wildly fluctuating performance on individual items, which in turn can result in dissociations in arbitrary directions. Often these small scale artefacts are sufficient to produce convincing looking double dissociations." "As soon as we scale up to larger networks ... We always find that the apparent double dissociations dissolve into single dissociations".
- A check is proposed: individual contributions to each output, C = c_ij / Σ_k c_ik, should be "much less than one". Otherwise single units act as "modules" in their own right.
- Resource artefacts: a crossover double dissociation in patients can come from one shared resource "such that which task is performed better depends on the amount of resource that has been spared". It "should NOT be taken to imply modularity" (citing Shallice).
- Shallice 1988 is cited for a list of non-modular systems that can produce double dissociations, and for "as yet there is no suggestion that a strong double dissociation can take place from two lesions within a properly distributed network" (p. 257).
- Plaut (1995) and Marchman (1993) are reconciled as differences in terminology, or as a frequency-regularity confound.

## Evidence
Simulations of fully connected feed-forward networks with one hidden layer trained on regular and irregular mappings, comparing 30 and 100 hidden units. The other evidence is the review itself.

## License
Book chapter © Psychology Press; author pre-print. No code.

## Runs on this Mac without a GPU?
n.a. The contribution-ratio check is cheap on any small model.

## Verdict: adopt (as a validity check on lesion results)
Rules for the engine's ablations:
- Report the contribution-ratio distribution, or the equivalent redundancy, before trusting a lesion. If one unit or parameter carries most of an output, a lesion effect may be an artefact.
- Check that a result is stable across network sizes.
- Control for how strongly an item or behavior was trained (frequency) before attributing a selective loss to a component.

Failure here: a claimed effect of removing component X that disappears when the latent state is made larger or more redundant. Another failure is an effect that is explained by X's behaviors simply having been trained less.
