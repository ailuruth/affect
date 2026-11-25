# Rethinking the emotional brain

Joseph LeDoux, *Neuron* 73(4):653–676, 2012, doi:10.1016/j.neuron.2012.02.004 (PMC3625946, NIH author manuscript; read in full text).

## Claims
- The field should study conserved **survival circuits** instead of searching animals for human feelings. The circuits listed are defense, energy and nutrition, fluid balance, thermoregulation and reproduction ("at a minimum").
- These circuits "are not posited to have any direct relation (causal role) in feelings". They are sensory-motor integrative devices that detect challenges and opportunities and control behavior and physiology "to bring closure to the situation".
- There is deliberately no anger circuit and no joy circuit. Aggression splits by context (defensive, reproductive, predatory), and "joy" behaviors are products of specific circuits.
- Activation produces a **global organismic state**: arousal, innate and autonomic responses, motivation, focused attention, memory retrieval and new learning, all "coordinated and monopolized" for the challenge.
- **Feelings** arise when consciousness "(a) detects that a survival circuit is active or witnesses the existence of a global organismic state ... and (b) appraises and labels this state" in a cognitive workspace (prefrontal and parietal). The state is categorized against long-term memory and can be dimensional (valence/arousal) or specific. Emotion words further partition experience, and specific emotions are "unlikely ... without words".
- He rejects Panksepp's inference from behavior to feeling as unverifiable anthropomorphism.

## Evidence
A conceptual review grounded in defense-circuit work (threat conditioning, amygdala, PAG) and comparative neuroanatomy. There is no new data.

## License
- Paper: © Elsevier. The PMC author manuscript is marked "available for text mining ... consistent with the principles of fair use". Quote sparingly.
- Code: none.

## Runs on this Mac without a GPU?
n.a.

## Verdict: adopt
Adopted as the stated basis for the brief's split: innate subsystems, then a non-emotional global state, then Claude detects and labels it.
- Subsystems are survival functions, not emotions (Principle 2).
- Labelling belongs to a separate conceptual workspace that does not drive the fast loop (Principle 4).

Gap: his list has **no social-attachment circuit**. Separation distress and contact seeking must come from Panksepp's PANIC/GRIEF and CARE (panksepp-primary-affective-systems.md), not from LeDoux.

## What it gives S1
- **A three-layer contract for S1.**
  1. Subsystems (fixed triggers and reflexes).
  2. $h_t$ as the "global organismic state". When a subsystem is active, it should bias what memory is retrieved and what is attended to; that is Goldenberg and Gross's reorganization test.
  3. Claude as the workspace that detects and labels.
- **What Claude is shown.** Which subsystem is active (by function name), how strongly and since when; the low-dimensional read-out of $h$; and the episodic memories that state retrieved. Claude then appraises and labels. A dimensional answer ("unsettled, low") is valid output, and Claude is not forced to choose a specific emotion.
- **Ablation hook.** Removing the subsystem→$h$ coupling should leave reflexes intact (a contact bid still fires after silence) but remove the global effects. On reunion, the Bot would make the bid but retrieve no user-specific memories and change no reply budget. That is a sharper prediction than "behavior changes".
