# Elements of emotion across theories: what a single core must produce, and how to show each matters

This synthesis draws on the notes written in this tick and on notes already in the index. It serves the long-term goal in brief.md: "one system that holds every element of emotion that cognitive science and affective neuroscience consider necessary, each shown by ablation to matter". The claim stays functional throughout. Nothing here is a claim that the system feels.

## Sources and abbreviations
| Key | Note |
|---|---|
| AA14 | anderson-adolphs-2014-emotion-primitives.md |
| A17 | adolphs-2017-emotion-states-concepts-experiences.md |
| LD12 | ledoux-survival-circuits.md (existing) |
| LB17 | ledoux-brown-2017-higher-order-emotion.md |
| B17 | barrett-constructed-emotion.md (existing) |
| BS15 | barrett-simmons-2015-epic-interoceptive-predictions.md |
| S13 | seth-2013-interoceptive-inference.md |
| DC13 | damasio-carvalho-2013-nature-of-feelings.md |
| C09 | craig-2009-anterior-insula-awareness.md |
| P11 | panksepp-primary-affective-systems.md (existing) |
| Sch09 | scherer-2009-component-process-emergence.md |
| M13 | moors-2013-appraisal-theories.md |
| R03 | russell-2003-core-affect.md |
| BK15 | berridge-kringelbach-2015-pleasure-systems.md (with berridge-2004-motivation-concepts.md) |
| KL16 | kragel-labar-2016-decoding-emotion.md |

Each "ablation" below is an operation on the engine. Each is stated so that it can be derived from the core's equations, as Principle 10 requires, rather than added as a module. "Signature" is the behaviour a reviewer would measure.

## Elements table

| # | Element | Required by | Functional signature | Ablation that would show it matters | Where theories disagree (testable) |
|---|---|---|---|---|---|
| 1 | **Concern grounding**: something the agent needs, which events are evaluated against | DC13, BS15, B17, C09, M13 ("concerns"), LD12 (survival circuits), P11 | The same stimulus gets different responses under different need states (alliesthesia); responses stop once the need is met | Hold the need input constant or remove it. Responses become tied to the stimulus and the same at any need level | Drive reduction (DC13 stop condition) against incentive motivation without deficit (BK15, Berridge 2004). Prediction of need (BS15) against present error |
| 2 | **Central persistent state**: an integrator between stimulus and response | AA14, A17 ("decoupling"), LD12 ("global organismic state"), Sch09 (bounded episode), BS15 (slow priors); R03 (core affect, always present) | Effects outlast the trigger; carry-over into the next exchange; recovery has a time constant | Reset the latent every step, or shorten its time constant. Outputs follow the current input with no aftereffect | R03: core affect persists, but there is **no** persistent emotion-episode node. AA14: there is a central emotion state. See D2 |
| 3 | **Valence**: a sign, antithesis | All | Opposite output patterns (approach against withdrawal; Darwin's antithesis); learning from good or bad outcomes | Decouple the readout's sign from change in the core's objective. Approach and withdrawal stop tracking benefit | Where the sign comes from: homeostatic value (DC13), interoceptive prediction (BS15, S13), hedonic hotspots apart from wanting (BK15), a readout of a learned latent (R03, B17) |
| 4 | **Intensity and scalability**, with regime switches | AA14, R03 (arousal), Sch09 (hysteresis, cusp), C09 (energy expenditure axis) | Graded responses that change in kind at high intensity (freeze, then flee); different switching points rising and falling | Make the policy readout of the state linear. No change in kind and no hysteresis | Sch09 predicts hysteresis; none of the other sources commits either way |
| 5 | **Pleiotropy and coordination**: one state, many outputs | AA14 (the "acid test"), A17, LD12, Sch09 (synchronization) | Perturbing the state moves face, voice, policy, attention and memory together | Give each output channel a private latent. Coherence across channels collapses | R03: components are weakly coupled, sharing 10–15% of variance. See D2 |
| 6 | **Interoceptive prediction and allostasis** | BS15, S13, B17, C09 (anticipatory moments), DC13 (feelings enable anticipation) | Regulation before the deficit; the affect readout follows the predicted body more closely than the sensed body | Set the prior's learning rate high, so the model is purely reactive. No anticipation, a volatile readout, less persistence | Prediction-led (BS15, S13) against bottom-up re-representation (C09, DC13). See D4 |
| 7 | **Precision on body error** | BS15, S13 | Autonomic or face action engages only when error precision drops; the state is stable against noisy afferents | Clamp precision. High gives a flat, belief-revising, low-action state; low gives a state cut off from the body (S13's analogue of depersonalization) | Only the predictive theories need it, which makes it a test of those theories against non-predictive cores (Gershman's challenge) |
| 8 | **Relevance, conduciveness and novelty checks** | Sch09, M13, R03 (perception of affective quality), LD12 (detecting challenges), AA14 (generalization) | Each check has its own efferent signature on face and voice, and the signatures add | Remove the novelty (prediction-error) term. The orienting part of the face response (brow, gaze) is lost while the valenced part stays | Order of checks: Sch09 says they run in parallel but close in a fixed order; M13 says this is unresolved. See D6 |
| 9 | **Agency and coping potential** (who caused it; can I change it) | M13, Sch09 | Distress splits into approach or protest (high control, or the partner as cause) against withdrawal (low control); developmentally this comes after attribution of agency | Remove partner/world attribution or controllability from the world model. Responses to partner-caused and world-caused losses become the same | Appraisal theory says differentiation comes from these dimensions; constructionism (B17, R03) says from concepts. See D1 |
| 10 | **Action readiness and control precedence**: interrupt | Sch09, A17 ("pre-potent ... interrupt"), LD12 ("monopolized"), DC13 (action programmes), P11 | The state preempts ongoing behaviour, such as a reply or gaze pattern in progress | Cap the state's influence on policy switching. The state still changes, but nothing is interrupted | Programmes (P11, DC13) against emergent readiness (Sch09). See D7 |
| 11 | **Wanting distinct from liking** | BK15, Berridge 2004 | Pursuit triggered by cues that is separable from the consummatory readout; context can flip a cue's sign | A double dissociation. (a) Remove the need gain on cue value: approach drops, the readout on contact stays. (b) Remove the consummatory term: approach stays, the readout is lost | A single scalar value gradient cannot show this. That is a test that rules out some cores |
| 12 | **Learned elicitors and generalization** | AA14 (Box 3), A17, DC13 (money, drugs), B17 (learning gated by allostatic relevance), M13 (schematic level) | New cues come to evoke the state; different inputs reach the same state region | Freeze learning. Only the innate triggers move the state; the partner's cues never acquire value | B17: learning is gated by body relevance; others leave the gate unspecified. Test whether gating changes what is learned |
| 13 | **Expression and social communication** | AA14, Sch09 (efferent patterning), C09 (communication as the evolutionary driver), S13 (others' responses confirm one's own interoceptive inference), P11 | Face and voice depend on the state and are readable by the partner; the partner's contingent response changes the agent's state | (a) Cut the path from state to face: the partner can no longer predict the agent's state. (b) Shuffle the partner's timing: the agent's state estimates lose confidence (S13) | Whether expression is a readout only (R03: "no separate class of emotional behavior") or part of inference about oneself (S13) |
| 14 | **Integration, self-model and comparator buffer** | C09 ("global emotional moment" plus buffer), LB17 (self-HOROR), S13 (body ownership), DC13 (insula brings feeling into cognition) | Comparisons of now against predicted give relief and disappointment; states are referenced to the self | Remove the agent's own state history and prediction of its own next state. Present valence stays; relief and disappointment vanish | A single bottleneck (C09) against degenerate paths (DC13, BS15). See D5 |
| 15 | **Conceptual categorization**: meta-experience, labels, reappraisal | R03, B17, LB17, LD12, A17 (concepts as a separate stratum) | Episodes named and narrated; reappraisal changes later regulation | Remove Claude, or remove Claude's feedback into the fast core | The central disagreement over where feeling lives. See D1 |
| 16 | **Structure beyond valence and arousal** | KL16; against a purely dimensional core (R03, B17 hold 2-D core affect but construct categories) | Situation types are decodable from the latent above the valence/arousal ceiling | Restrict the affective subspace to 2-D. Decoding falls to the 2-D ceiling; check whether behaviour loses differentiation too | KL16 says discrete; R03 and B17 say a dimensional core plus concepts. See D3 |

Elements the brief already covers through existing notes: 1 (Keramati & Gutkin, Yoshida et al.), 3 (Hesp's affective charge as a readout), 11 (Zhang & Berridge, Berridge 2004), 13 (Yoshida & Man, Gergely & Watson), and Goldenberg & Gross's reorganization criterion, which is row 5 seen from the side of processing.

## Disagreements the engine could test

The engine tests functional predictions only. Where a theory's claim is about experience (LB17: emotions cannot be unconscious; DC13: feelings exist in other species), the engine can test only what that claim implies for behaviour and report.

**D1. Where feeling lives: fast subcortical core, higher-order self-model, or conceptual construction.**
- *Subcortical* (DC13, P11, BK15): the valenced core, its learning and its hedonic reactions are generated without cortex.
- *Higher-order* (LB17): survival circuits give nonconscious input, and experience needs a self-referential re-representation.
- *Constructionist* (B17, R03): core affect is ever-present, and specific emotions are categorizations made with concepts.

Engine test: two lesions.

**(a) Remove the conceptual layer's feedback into the fast core.** This keeps Claude naming but stops its concepts and reappraisals from entering the predictive model (the path B17's note proposes).
- Constructionism predicts that differentiation among situation types *in the fast loop* (face, policy, regulation) falls and recovery after reappraisal slows.
- The subcortical and higher-order views both predict little change in the fast loop.

**(b) Remove the coupling from body to latent but keep Claude.**
- LB17 predicts that reports go on, from schemas, with weaker intensity.
- DC13 predicts that valence and reports lose grounding: flat or confabulated.

Note: **the brief's architecture already decides part of this dispute.** Under Principle 4, Claude never drives frames, so with no feedback path the constructionist prediction for the face is false by design. For the engine to serve as a testbed, the feedback path in (a) must exist as a switch that can be turned off.

**D2. A single central state or dissociated components.**
- AA14 and Sch09 predict that a perturbation moves all channels together, with high shared variance.
- R03 predicts low coherence: Bradley & Lang's 10–15% shared variance, and Reisenzein's r from .19 to .46 except appraisal with feeling at .78.

Engine test: compute the variance across face, voice, policy and body variables that a shared factor explains, under matched perturbations. Compare it with those human figures, and with an ablation that gives each channel a private latent. A single core that produces Russell-level coherence would show the two views are compatible: one central state, read out noisily.

**D3. Discrete or dimensional structure.**
- KL16 says classification beats valence and arousal.
- R03 and B17 say a 2-D core with constructed categories.

Engine test: decode situation types (not emotion labels) from the latent. Compare with its 2-D projection. Track decoding accuracy over development: if structure grows with lived interaction from a category-free start, that is an existence proof of learned categories.

**D4. Is interoception prediction-led or sensation-led?**
- BS15 and S13 say what is experienced follows the prior: "perceptions follow actions".
- C09 and DC13 say a bottom-up re-representation of afferent signals.

Engine test: perturb a body variable in a way the agent's model does not expect. A prediction-led core's readout lags and holds its prior; a sensation-led core's readout follows the sensor at once. Measure the readout's lag and its dependence on the prior's learning rate.

**D5. A single integration bottleneck or degenerate paths.**
- C09 says the AIC is necessary for awareness.
- DC13 (Patient B) and BS15 (Roger and Boswell) say several paths can each support the integrated readouts.

Engine test: lesion the single integrating layer, if the core has one. See whether every downstream readout fails, or whether each survives through other paths.

**D6. Sequential or parallel appraisal.**
- Sch09 says checks run in parallel but close in a fixed order: novelty, then intrinsic pleasantness, then goal conduciveness, then coping, then norms.
- Other appraisal theorists, per M13, call the order assumption overly restrictive.

Engine test: time the onset of each component's efferent effect on the face (orienting against valenced action units) after a matched event.

**D7. Fixed programmes or emergent patterning.**
- P11 and the action programmes in DC13 say coordinated, stereotyped patterns.
- Sch09 says expressions are compositions of check-by-check efferents.

Engine test: give a mixed appraisal input, for example novel plus conducive plus low control. Is the face response the sum of the single-check responses (composition), or does it snap to the nearest frequent pattern (a learned programme)? Either can emerge in a learned core. Which one does is informative.

**D8. Drive reduction or incentive** (covered in berridge-2004-motivation-concepts.md). Rows 1 and 11 above give the double-dissociation test.

## What this means for the candidates
- Rows 2–5 and 12 come almost for free in any recurrent learned core with a homeostatic objective. They still need ablations to show that they matter.
- Rows 6–7 need a predictive or filtering core, with learned precision.
- Rows 9 and 11 are the **hard derivation obligations**:
  - agency and coping potential need a model-based core that attributes causes and estimates how controllable value is;
  - wanting against liking needs need-scaled cue gain to enter separately from the realized reduction.
- Row 13's half about confirming the partner (S13, Gergely & Watson) is the only theoretical route found here by which the partner's contingent response feeds the agent's own state estimate. It does not reward the agent for the partner's reply, so it respects Principle 6.
- Row 15 lives in Claude by design (Principle 4). Row 15's ablation and D1 can be run only if Claude's feedback into the fast core exists as a switch that can be turned off.
