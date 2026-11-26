# Social top-down response modulation (STORM): a model of the control of mimicry in social interaction (Wang & Hamilton)

Yin Wang & Antonia F. de C. Hamilton, *Frontiers in Human Neuroscience* 6:153, 2012, doi:10.3389/fnhum.2012.00153 (PMC3366585).

## What was read
**Not the paper.** Frontiers and PMC were blocked by this session's network policy. What I had: the abstract and search-engine excerpts of the article body, plus excerpts describing Wang, Ramsey & Hamilton 2011 (*J Neurosci* 31:12001–12010) and Wang & Hamilton 2015 (*SCAN* 10:486, "anterior medial prefrontal cortex implements social priming of mimicry"). Only the 13 ms gaze figure was seen as a number.

## The computation, precisely
- **Claim (abstract):** "the subtlety and sophistication of mimicry in social contexts reflect a social top-down response modulation (STORM) which increases one's social advantage and this mechanism is most likely implemented by medial prefrontal cortex (mPFC)." Mimicry is **strategic**. When it is inappropriate, it is inhibited; when it serves the actor's social goal, it is enhanced.
- **Bidirectional:** unlike the Brass account (inhibition only), STORM modulates mimicry up *and* down. Direct gaze, prosocial primes and the in-group raise it; the opposite contexts lower it.
- **Number (excerpt):** in a social stimulus–response compatibility task, "direct gaze facilitates mimicry of hand action by 13 ms, compared to averted gaze". The authors read this as eye contact itself, not spatial or joint attention, driving mimicry.
- **Neural (excerpt):** in Wang et al. 2011, mPFC and two other regions showed a gaze × mimicry-congruency interaction. The account has mPFC modulating the input to the mirror system (STS/IFG). Wang & Hamilton 2015: anterior mPFC implements social priming of mimicry.
- **What the control signal depends on:** the actor's **social goal** given the current cues (eye contact, primes, the partner's group, liking). It does not depend on whether an activation is self- or other-generated.

## What it means for the designs
- **Two different controllers.** Brass and Sowden: *attribution* (whose is this?). STORM: *policy* (does copying serve me here?). STORM is the context-dependent, signed, per-partner gain that mimicry-context-synthesis.md already requires (sign flips, per-expression gating). It is **not** a guard against copying. It is the thing that sets how much copying, and so it is exactly where the flat-to-copy scalar can hide (designs.md gap 1).
- **The combination a design needs:** attribution first, then policy. The policy may only act on other-tagged content, and only through a bounded, sign-capable operator: $m_{\text{out}} = u_{\text{self}} + W(\text{context})\,\Pi_{\text{other}} m$, with $\|W\| \le w_{\max} < 1$ and $W$ learned per partner. Without the attribution step, STORM's gain multiplies everything, and that is the one-scalar dial.
- **Time scale:** the gaze effect acts within a trial (13 ms on a sub-second RT). Goals and primes act over minutes.

## Verdict
**adopt as the policy layer, with the attribution layer from Brass/Sowden in front of it (abstract-level; re-read).** On its own, STORM restates the dial. It is useful as the definition of what the bounded, signed $W$ is for: social advantage, not matching.
