# Self–other control of automatic imitation: the computation that stops "reading through my body" from becoming copying (synthesis)

Cycle question: every design lets the partner's face come back into the agent's face through indirect routes. The brain has the same problem: seeing an action activates one's own motor code (automatic imitation), yet people do not copy. What computation prevents it, stated so a design can formalise it?

**Evidence status.**
- **Read in full:** sowden-2015 (rTMS), hogeveen-2015 (tDCS), wang-hamilton-2012 (STORM review), darda-ramsey-2019 (fMRI meta-analysis, bioRxiv v3) and lanillos-2020 (robot model).
- **Abstract-level only:** brass-2009 and santiesteban-2012. Their primary texts were unreachable; their claims enter through how the papers above paraphrase them.
- **Older full-text notes used:** cook-2014-mirror-neurons-origin, blakemore-wolpert-frith-2002, synofzik-2008-2013 and mimicry-context-synthesis.
- The structure below is my inference across all of these.

## What the evidence says
1. **One code, two sources.** A seen action activates the observer's own motor representation through a learned map (Cook 2014: 50–90 min of crossed training abolishes or reverses it). Sowden & Catmur define control as "exciting the self-representation and inhibiting the other-representation, *or vice versa*". It is one operator whose direction depends on the task: "vice versa" is perspective-taking.
2. **Removing the attribution step increases copying, and only copying.** rTMS over rTPJ took the imitative effect from ~7 to ~20 ms. The spatial effect (~63 ms) and baseline RT were unchanged (F(1,15) = 5.10, P = .039, n = 16). The authors' alternative reading: rTPJ is needed when the two representations **overlap one-to-one** (index↔index), not when the overlap is diffuse (left↔any left).
3. **Selection is generic.** Across 12 fMRI studies (300 participants), conflict between a seen action and one's own intention reliably engages the multiple-demand network, never mPFC. rTPJ appears for spatial but not imitative compatibility (only 3 imitative contrasts). Darda & Ramsey's model: social *input*, domain-general *selection*.
4. **Partition and router are different operators.** In Hogeveen (n = 48), TPJ tDCS improved inhibition (d = .58) but left delayed social mimicry alone. IFC tDCS improved inhibition (d = .54) *and* raised social mimicry (d = .62): "control of the mirror system's impact on overt behavior" in whichever direction the context needs. Self–other control is needed when representations are "easy to confuse ... synchronous"; appropriate mimicry runs at a lag of seconds.
5. **The router is social policy and acts at the input.** STORM: mimicry is raised or lowered for social advantage. It is non-additive: a nasty high-status partner is mimicked most. Direct gaze adds 13 ms, through congruent trials (facilitation, not inhibition). In the DCM, the gaze × mimicry interaction sat on mPFC→STS, the sensory input to the mirror system.
6. **Active inference copies unless attribution gates action.** In Lanillos's robot, perception and action both descend one prediction error. The other's hand "acted sometimes as an attractor for the body inference, generating mirroring actions similar to imitation". Self-attribution is accumulated log-evidence under the robot's own forward model plus a contingency term (100/100 mirror trials correct). A perfectly synchronous copier is classed as self, and the robot's own actions had to be aperiodic.

## The computation, stated for formalisation
Notation:
- $o_t$: the partner's face observation.
- $u_t$: the agent's own motor intention (the output of its core).
- $P$: the learned partner-to-own correspondence (ASL; it can be non-identity or crossed).

1. **Two registers in one coordinate frame.** The other-register is $x^{o}_t = G(c_t)\,P(o_t)$. It uses the same action-unit coordinates as the self-register $x^{s}_t$, which $u_t$ drives. $G(c)$ is the input-side social gain (STORM's mPFC→STS). Reading the partner (Principle 3, inversion of one's own generative map) runs on $x^{o}$. **Same coordinates, not same slot.**
2. **Attribution as model evidence.** For each component $k$:

   $$\lambda_{t,k} = \lambda_{t-1,k} + \log p\big(o_{t,k} \mid \text{own forward model},\,u_{1:t}\big) - \log p\big(o_{t,k} \mid \text{partner model}\big),$$

   with $a_{t,k} = \sigma(\lambda_{t,k})$, smoothed as in Lanillos ($p_{\text{self}} \leftarrow p_{\text{self}} + K(p_{\text{norm}} - p_{\text{self}})$). Slower context priors (Synofzik) enter the prior on $\lambda$. The tag is needed most where $P$ is one-to-one and timing is synchronous. Identifiability needs aperiodic own output (Lanillos; contingency-causal-synthesis).
3. **Only self-attributed error drives action.** Action descends $a \odot e$ (equivalently, error in $x^{s}$ only). Other-attributed error updates beliefs about the partner and is never descended by action. This is the line that removes the active-inference copy route in (6).
4. **Generic selection.** Output $y_t = \mathrm{select}(x^{s}_t)$ by the same competitive dynamics as any action choice (Darda & Ramsey). Other-register content reaches $x^{s}$ only through a router:

   $$x^{s}_{t+1} = f(x^{s}_t,u_t) + W(c_t)\,x^{o}_{t-\tau},\qquad \|W(c)\| \le w_{\max} < 1,$$

   with $W$ signed, set per expression and learned per partner (STORM; IFC in Hogeveen). Its lag $\tau$ should be of order seconds, not zero: appropriate mimicry is delayed, and zero lag is where attribution fails. Copying is $W = I$, $\tau = 0$ with $u$ silent. The bound, the lag and (5) exclude it.
5. **Always an own intention.** Generic selection resists mirrored input only when an own intention competes. The core must always supply $u$: a set-point face, rhythms, homeostatic tone. Otherwise the idle agent copies. This is an inference from Darda & Ramsey; no source tests it.
6. **Carry the tag through the core (design obligation; no source tests this).** The brain data cover the motor route only. To close indirect routes (partner face → agent affect → agent face), affect evidence from $x^{o}$ updates beliefs about the partner and the shared event (social appraisal). It reaches the agent's own affect only through its own concerns, never by an identity map. The invariant to prove: along every path, $\|\partial y/\partial o\|$ in the copy direction is at most $w_{\max}$ times the appraisal gain, so no composition of paths gives $\approx I$.

**What this is not.**
- Not attenuation of the partner. That is self-attenuation in Blakemore, in the opposite direction.
- Not a global inhibitor.
- Not one gain: a stronger partition removes only wrong leaks; a stronger router makes influence *more conditional both ways*.

## Time scales
- **Attribution and selection:** within a response (<0.5 s). Imitative interference is ~7–20 ms on RTs of ~430–500 ms; gaze modulation is 13 ms.
- **Attribution evidence in the robot model:** accumulates over seconds.
- **Router context:** seconds (gaze) to the session (status, liking, belief).
- **Map and partition learning:** about an hour (Cook: 50–90 min of crossed training), with effects 24 h later (Santiesteban, abstract-level).

## Open questions
1. **Per component or per episode?** Is attribution per expression component (so a smile can be shared while a frown is countered)? Per-expression gating suggests so; no source here tests faces.
2. **Indirect routes.** Does the brain stop emotional contagion by the same partition? No source read here addresses affect. Next reading: self–other distinction in empathy (e.g. Steinbeis et al. 2015 on right supramarginal gyrus; Lamm, Bird & Silani 2016).
3. **The idle case.** Is spontaneous facial mimicry larger when the observer has no competing intention? This is a prediction of point 5 and checkable in published EMG data.
4. **Synchrony.** How much lag and own aperiodicity keep attribution calibrated against a partner who mirrors the agent at near-zero lag?
5. **Localisation conflict.** Stimulation (Sowden; Hogeveen) implicates rTPJ; fMRI (Darda & Ramsey) does not. The computational split (input-side attribution, generic selection, signed router) survives either result.
6. **Unread primaries.** Brass 2009 and Santiesteban 2012 (Cognition), and also Santiesteban et al. 2012 (Current Biology, tDCS) and Wang, Ramsey & Hamilton 2011 (J Neurosci), whose numbers STORM reports second-hand.
