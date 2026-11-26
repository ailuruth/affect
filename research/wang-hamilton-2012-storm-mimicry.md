# Social top-down response modulation (STORM): a model of the control of mimicry in social interaction (Wang & Hamilton)

Yin Wang & Antonia F. de C. Hamilton, *Frontiers in Human Neuroscience* 6:153, 2012, doi:10.3389/fnhum.2012.00153 (PMC3366585, CC BY-NC).

## What was read
The full PMC open-access text (JATS XML from the PMC OAI service): all sections and figure captions. It is a review/hypothesis paper. Its primary data are summarised from Wang, Newport & Hamilton 2011 (behaviour), Wang, Ramsey & Hamilton 2011 (*J Neurosci*, fMRI/DCM) and two studies "in preparation". I did not read those primary papers. Numbers below are as reported in this review.

## The computation, precisely
**Claim.** Mimicry is "a strategic intervention to change the social world for self-advancement". "If mimicry in the current situation can benefit one's social standing, individuals will increase mimicry; on the contrary, if mimicry becomes inappropriate at the present time, individuals will inhibit mimicry." Mimicry itself is built by associative sequence learning (Heyes); STORM is control on top of it.

**Evidence and numbers (as reported here):**
- **Eye contact:** "direct gaze facilitates mimicry of hand action by 13 ms, compared to averted gaze". The effect is carried by **congruent** trials, "which suggests that eye gaze directly influences the mimicry process per se, but not the process of the inhibition of mimicry". A follow-up found that only "direct-gaze-during-action" enhanced mimicry; joint attention to the hand did not.
- **Not additive in social features:** participants mimicked a **nasty high-status** actress most, more than a nice high-status one. So mimicry is not a sum of positive stimulus features.
- **Belief, not appearance:** identical gloved-hand animations gave stronger mimicry when participants believed the hand was human (Liepelt & Brass 2010).
- **Per-expression, signed:** more mimicry of sad and less of anger toward in-group members (Bourgeois & Hess 2008). Less mimicry of dominant behaviour by high-status targets (Mastrop et al., in prep.). Romantically involved people mimic attractive opposite-sex targets less.
- **Neural (DCM, Wang et al. 2011):** strong intrinsic mPFC→IFG and mPFC→STS connectivity ("mPFC constantly exerts top-down control on the MNS"). The task increased STS→IFG coupling (the visuomotor map). **The gaze × mimicry interaction modulated mPFC→STS**: "mPFC ... modulates sensory input (i.e., STS) to the MNS."
- **Self-focus raises inhibition** (Spengler et al. 2010b, as reported): seeing oneself in mirrors beside the screen strengthened inhibition of mimicry.

**Two separate controls, distinguished by the authors themselves:** inhibition of mimicry is "linked to ... the self-other distinction. However, this does not explain the information processing behind the decision of when to mimic and when to inhibit mimicry." STORM is the second: a decision about *whether copying pays*.

## What it means for the designs
- **The control acts on the input to the motor map, not on the output.** In the DCM, social context gates STS (visual action representation) → IFG. Formally: $x^{o} = G(c)\,P(o)$ with $G$ set by social context, before the motor map. This is the gain on the *perceived* face, and it is where a flat-to-copy scalar can hide (designs.md gap 1). STORM is **not** a guard against copying. It is the thing that *sets* copying.
- **Two operators are needed, and they are separable.** (1) Attribution: whose activation is this (Brass/Sowden). (2) Policy: should the other's activation reach output, with what sign (STORM). Without (1), (2) is the one-scalar dial. With (1), (2) acts only on other-tagged content and can be bounded and signed per expression and per partner.
- **The objective is social consequence, not matching.** "Mimic the nasty high-status person most" is the value of an action under the agent's own concerns (affiliation need × difficulty). That is what the social-appraisal route (designs.md gap 8) would compute. STORM gives a measured target: the policy is non-monotone in the partner's niceness.
- **Time scales:** gaze acts within a trial (13 ms on hand-action RTs); belief and status act over the session; the authors contrast this with naturalistic modulation "over a couple of minutes".

## Verdict
**adopt as the policy layer, behind an attribution layer.** STORM alone restates the dial. Its usable content is: control enters at the sensory input (mPFC→STS), it is signed and non-additive, and its objective is social consequence. Primary numbers come from cited studies that were not read.
