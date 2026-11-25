# Neurons that function within an integrator to promote a persistent behavioral state in Drosophila (Jung et al.)

Yonil Jung, Ann Kennedy, Hui Chiu, Farhan Mohammad, Adam Claridge-Chang & David J. Anderson, *Neuron* 105(2):322–333.e5, 2020, doi:10.1016/j.neuron.2019.10.028 (PMC6981076).

## What was read
The full PMC author text (JATS XML, ~9,000 words): summary, introduction, all Results sections, the Discussion in full, and the Methods section "Curve Fitting for Leaky bucket model" (which gives the model equation). Figure captions were read; figures not seen. This note also draws on `lee-2014` material I read in the same session (Lee et al. 2014, *Nature* 509:627–632, PMC4098836, read in full) for the scalable-intensity side of the same programme, cited where used.

## The computation, precisely

**The architecture claim: command and state are different pathways from the same trigger.**

> "In Drosophila, male-specific P1 interneurons promote courtship song, as well as a persistent internal state that prolongs courtship and enhances aggressiveness. However, P1 neurons themselves are not persistently active. Here we identify pCd neurons as persistently active, indirect P1 targets that are required for P1-evoked persistent courtship and aggression ... P1 neurons coordinate both command-like control of courtship song, and a persistent internal state of social arousal mediated by pCd neurons."
> "P1 neurons activate this circuit in parallel with a 'command' network, including pIP10 descending interneurons, that triggers rapid-onset courtship behavior. These results illustrate how acute and enduring responses to sensory cues may be segregated into parallel neural pathways, allowing behavioral control on different time scales".

So one sensory trigger fans out to (a) a fast reflex path and (b) a slow integrator path, and the two are separately manipulable: silencing pCd left the time-locked behaviour during stimulation untouched and removed only what outlasted it — "silencing pCd neurons dramatically reduced persistent wing extension evoked by Chrimson activation of P1 cells ... Importantly, time-locked wing-extension during photostimulation was unaffected."

**The state is necessary but not sufficient, and this is proved three ways.**
- Activating pCd alone does nothing: "optogenetic activation of pCd neurons in solitary flies had no visible effect, in contrast to optogenetic activation of P1 neurons".
- Activating pCd *in the presence of a social stimulus* changes the response to it: with a dead female present, "Activation of pCd neurons ... dramatically elevated courtship behavior during photostimulation, and this effect persisted for several minutes after stimulus offset"; with a dead female present it also "significantly enhanced fly aggressiveness after photostimulation". "pCd activation alone cannot do so ... However pCd neuron activation can enhance and extend the effect of a dead female to promote these social behaviors."
- Physiologically the same asymmetry: direct stimulation of pCd gave fast-decaying responses (median $\tau \approx 13.4$ s) while *indirect* P1-driven activation gave $\tau \approx 83$ s, "indicating that persistent activity cannot be triggered cell autonomously", and transient inhibition during the decay phase **did not recover**: GtACR1 caused "a rapid, ~68% decrease in ΔF/F signal, which did not recover to control levels following the offset of inhibition, but rather remained flat". A nearby population (PPF2) *did* recover, so pCd is inside the loop, not downstream of it: "persistence in pCd neurons requires their continuous activity. However the fact that persistent activity cannot be evoked by direct stimulation of pCd neurons alone suggests that persistence likely requires co-activation of a network".

**The model, with its equation.** Both behavioural phenotypes are fit by one leaky integrator in which **only the leak differs by genotype**:

> "$\dot r(t) = -r(t)/\tau + I$, which has analytical solution $r(t) = (r_0 - \tau I)e^{-t/\tau} + \tau I$, where r is the behavior rate as a function of time t (in minutes), I is a constant sensory input, τ is the time constant of integration, and r0 is the initial behavior rate ... the sensory input I was constrained to take the same value for all groups and conditions, while r0 was fit separately for courtship and for aggression; only τ was fit independently for each group and each behavior."

And the interpretation of the two opposite-looking phenotypes:

> "For UWEs, in control flies the relatively flat line reflects the fact that the initial rate of behavior is high, and already close to the steady-state ... In contrast, the faster decline of UWEs in pCd>Kir2.1 flies was best fit by an increase in T. During aggression, control flies exhibit escalation because the initial rate of aggression is low, and the sensory input rate constant R is greater than T for this behavior. Increasing T in pCd>Kir2.1 flies therefore converts aggression to a relatively flat line ... the superficially different courtship vs. aggression phenotypes caused by silencing pCd neurons can be explained by a common mechanism, whereby inhibition of pCd neurons increases the leak rate constant of a neural integrator".

**The social memory result, which is the most relevant finding for a dyad.** Five minutes with a female, then removal, leaves a male more aggressive toward another male, and that carry-over requires continuous pCd activity:

> "Male flies pre-incubated with a female showed significantly higher levels of lunging than controls, indicating a persistent influence of female exposure to enhance aggressiveness."
> "Transient inhibition of pCd neurons abrogated the effect of female pre-exposure to enhance aggression, mirroring the effect of such transient inhibition to disrupt persistent physiological activity in these cells."
> "pCd neurons participate in a network that may encode a persistent memory of a female, which can be combined with the detection of an opponent male at a later time to elicit aggression."

And the state **changes what a later cue computes**: "Among pCd neurons persistently activated by P1 stimulation, only half responded to cVA alone ... However, delivery of cVA 30 s after P1 stimulation ... yielded cVA responses in 90% of the pCd cells ... peak cVA responses were significantly greater following P1 activation, than in flies exposed to the pheromone on its own (median increase 1.8-fold)."

## Evidence with numbers
- $\tau \approx 83$ s (indirect P1-driven persistence) vs $\approx 13.4$ s (direct pCd stimulation).
- GtACR1 inhibition: ~68% ΔF/F drop, no recovery; PPF2 control recovered.
- cVA responsiveness 50% → 90% of cells after P1 activation; peak response ×1.8 (median).
- Behaviour: silencing pCd increased latency to copulation; abolished escalation of lunging over the 15 min assay without changing initial lunging; made courtship decline instead of holding steady.
- Leaky-integrator fit: one free parameter per group/behaviour ($\tau$), with $I$ shared across all groups and conditions — an unusually constrained fit, and the reason the result is interesting.
- Female pre-exposure: 5 min, effect measured in a separate arena afterwards.

**Limits:** flies; pCd identity via several drivers (results replicated with a specific split-GAL4); the integrator's other members are unidentified ("It is likely that this integrator circuit comprises additional neurons"); a conflicting report (Zhang et al. 2019) on timescales of pCd involvement is discussed by the authors.

## Is this a new computation relative to the excluded frameworks?

Parts: (i) a leaky integrator $\dot r = -r/\tau + I$ — **excluded** (a one-pole SSM; homeostatic-RL drive models use the same); (ii) a multiplicative interaction between state and stimulus (the state gates the response to a cue) — **excluded** (gain modulation); (iii) parallel fast/slow pathways — **excluded** (residual plus slow branch).

**No new computation.** The findings that are not recombinations, and that the seventeen designs did not use:

1. **Necessary-but-not-sufficient persistence as a *structural* fact.** Direct drive gives $\tau \approx 13$ s; being inside the loop gives $\tau \approx 83$ s; interrupting the node kills the state permanently rather than transiently. So the persistent variable **does not exist in any single unit**: it is a property of a loop, and no unit can be driven to create it. For a core: an affective state that cannot be set by writing to any one variable — including by the partner — because the state is only ever the loop's. That is a sharp form of "the partner cannot author the state".
2. **One leak parameter explains two opposite-looking behavioural signatures** (a decline where the control is flat; a flat line where the control escalates), with the input $I$ held equal across all conditions. This is the reading cycle's "derived invariant deletes a free scalar" pattern in a behavioural fit: the authors did not fit per-condition sensitivities, they fit one leak. Any design claiming "context changes the shape of the response" should be held to this standard — fit the shapes with one structural parameter, not with per-condition gains.
3. **A persistent state that changes which later cue is effective** (cVA: 50% → 90% of cells responsive, ×1.8 peak). The state does not add to output; it **changes the agent's own receptive field for the next event**. That is partner influence as a change of the *input* map, not the output map.

## What it suggests for an affective core where the partner is structured, not a gain

1. **Split the Bot's response to the partner at the source: a fast command path and a slow integrator path, from the same perception.** The brief already wants an innate fast onset match; this gives the architecture for it, with the measured property that lesioning the slow path leaves the fast match intact. Two separately-testable components, and the partner's lasting influence lives only in the slow one.
2. **Make the slow state unable to be written by any single input.** The invariant to prove: the persistent variable has no representation as a function of any single unit's activity (it is the loop's), so there is no injection point for the partner — the partner can only perturb the loop's input. Vinograd's holographic result is the mammalian analogue: stimulating five $x_1$ cells moved the state *along the manifold* but the manifold's existence was the network's.
3. **State changes the agent's own receptive field.** Let the affective state multiply the agent's *perceptual* sensitivities rather than its expressive amplitudes: after a warm exchange, a brief ambiguous cue from the partner becomes legible (50% → 90%); the output map is untouched. This is a precise, non-gain reading of "the partner's influence is structured": it changes *what the agent can notice next*, which then changes expression only through the agent's own appraisal.
4. **Carry-over as a measurable target.** The five-minute-female experiment is the exact shape of the carry-over failure Q9 names: a prior social episode changes behaviour in a later, different interaction, and interrupting the state abolishes it. The equivalent test for the Bot: a prior episode with partner A changes the Bot's behaviour with partner B; resetting the slow loop abolishes it; nothing else changes.
5. **Escalation and decline are one parameter.** With $I$ fixed, whether a behaviour escalates or decays depends only on whether $I\tau$ exceeds $r_0$. For the core this means engagement and withdrawal need not be two mechanisms with two learned gains — they are two sides of one structural constant, which answers the brief's "time scales from structure" item without new parameters.
6. **Scalability from the companion paper** (Lee et al. 2014, read in full): in mouse VMHvl$^{Esr1}$, graded activation produced *different behaviours*, not more of one — "mounting (either alone or mixed with attack) evoked up to 0.1 mW/mm² and attack (only) evoked by intensities >3 mW/mm²" on a log-intensity scale, with hysteresis ("once attack was elicited, reducing the photostimulation intensity did not evoke mounting, but simply failed to elicit attack"), and with intensity corresponding to both more active neurons and more activity per neuron (roughly linear overall, "with a slope of ∼30"). Hysteresis is worth stealing: a state variable whose *downward* path is not the inverse of its upward path cannot be run smoothly from flat to copy and back by a single quantity.

## Verdict
**adopt (three mechanisms: fast command path separate from slow integrator path; persistence that exists only as a loop property and so has no write port; state that changes the agent's own input sensitivity rather than its output amplitude — plus hysteresis from Lee et al. 2014).** The mathematics is a one-pole leaky integrator, which is excluded; the constrained single-parameter fit and the necessary-not-sufficient structure are the contributions.
