# Task-dependent and distinct roles of the temporoparietal junction and inferior frontal cortex in the control of imitation (Hogeveen et al.)

Jeremy Hogeveen, Sukhvinder S. Obhi, Michael J. Banissy, Idalmis Santiesteban, Clare Press, Caroline Catmur & Geoffrey Bird, *Social Cognitive and Affective Neuroscience* 10(7):1003–1009, 2015 (online Dec 2014), doi:10.1093/scan/nsu148 (PMC4483570, CC BY 4.0).

## What was read
The full PMC open-access text (JATS XML from the PMC OAI service): abstract, Introduction, Methods, Results, Discussion and footnotes. The figures were not seen; their captions were read.

## The computation, precisely
**Model under test (the authors'):** TPJ and mPFC "control self-other representations with an indirect impact upon imitation, while IFC has a direct impact on the degree of imitation". IFC is cast as a "**gain control** on imitation, increasing or decreasing the influence of the mirror system upon behavior". Self–other control "would impact upon ... the degree of imitation — by either boosting the representation of another's action (increasing imitation) or one's own motor plan (decreasing imitation)."

**When self–other control is needed:** "when there is a task-relevant conflict between the motor plans ... of the self and the other, or when it is easy to confuse representations of the self and other (for example, when two people perform a synchronous action)". In the naturalistic task, the participant's copies lag by "a few seconds", so "there is little opportunity to confuse agency".

**Design.** n = 48 analysed (16 per group; one TPJ outlier removed). Between subjects: anodal tDCS 1 mA for 20 min, offline, at CP6 (rTPJ), at FC6 (rIFC), or sham; cathode at vertex. Then ~40 min of tasks:
1. **Imitation inhibition**: finger lift to a number cue while watching a congruent or incongruent finger lift (hand shown orthogonal to reduce spatial compatibility).
2. **Non-imitative inhibitory control**: same responses, but a congruent or incongruent *finger is highlighted*, with no observed action.
3. **Social interaction**: describe photographs with a confederate who touched her face throughout (M = 12.9 min). Face-touch rate relative to a 1–2 min alone baseline; hand touches as a control behaviour. Two coders, α = .72.

Measures: inverse efficiency (RT/(1 − error rate)), incongruent − congruent, residualised on pixelated baseline.

**Results.** Task × stimulation F(4,90) = 2.95, P < .05, ηp² = .12. Imitation inhibition: stimulation effect F(2,45) = 3.35, ηp² = .13; **TPJ improved inhibition (P = .04, d = 0.58), IFC improved it (P = .03, d = 0.54)**. Non-imitative inhibitory control: no effect (F < 1). Social interaction: stimulation effect F(2,45) = 3.2, ηp² = .12; **IFC increased face-touch mimicry (P = .02, d = 0.62); TPJ did not (P = .43, d = 0.20)**. Hand touching (non-mimicked control behaviour) was unchanged. Confederate behaviour did not differ between groups (face touches M = 80, hand touches M = 28).

The authors' conclusion: "IFC modulates imitation directly according to task demands, whereas TPJ controls task-appropriate shifts in attention toward representation of the self or the other, indirectly impacting upon imitation."

## What it means for the designs
- **Two operators, causally dissociated.**
  1. **Self–other partition (TPJ-like).** Strengthening it reduces copying *only where self and other compete* (synchronous, conflicting). It leaves delayed, appropriate social mimicry alone. It separates; it does not set a level.
  2. **Context-signed router (IFC-like).** Strengthening it moves imitation *in the direction the context wants*: down in the inhibition task, up in the rapport task. "Not simply enhanced mirroring or enhanced inhibition, but enhanced control of the mirror system's impact on overt behavior."
- **Formally:** with other-register $x^{o}$ and self-register $x^{s}$, the partition shrinks the unintended leak $x^{o}\to x^{s}$ (an off-diagonal term), while the router scales $|W(c)|$ around a context-set sign. More control does **not** mean less mimicry; it means **more conditional** mimicry. That is the shape-not-size result (mimicry-context-synthesis.md) at the level of mechanism.
- **The partition matters most when timing is synchronous.** The authors tie the need for self–other control to synchrony ("easy to confuse"). Appropriate mimicry runs at a lag of seconds. For the agent: a mirrored response at near-zero lag is where the attribution is ambiguous and copying risk is highest. That fits Hale & Hamilton (1 s mimicry detected far more than 3 s).
- **Time scale:** within trial for the inhibition task; minutes for the social task; tDCS effects persist ~90 min.

## Verdict
**adopt.** It is the clearest causal evidence that partition and context routing are distinct operators, and that strengthening control makes imitation more conditional rather than smaller. Moderate n (16/group), between subjects, effects at P ≈ .02–.04.
