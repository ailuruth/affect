# Blakemore, Wolpert & Frith 2002: Abnormalities in the awareness of action

Citation: S.-J. Blakemore, D. M. Wolpert, C. D. Frith. "Abnormalities in the awareness of action." *Trends in Cognitive Sciences* 6(6): 237–242, 2002. doi:10.1016/S1364-6613(02)01907-1. It is the short form of Frith, Blakemore & Wolpert 2000, "Abnormalities in the awareness and control of action", *Phil. Trans. R. Soc. B* 355: 1771–1788.

Source read: the whole 2002 TICS paper, from the author PDF on the Wolpert lab site, including Box 1 and Figs 1–3. The 2000 paper was **not read**. PMC holds it only as a scanned PDF behind a bot check, and the API returns only its abstract. This note therefore stands in for "Frith/Blakemore forward-model agency". The cited experiments (Blakemore 1998/1999 tickle, Frith & Done 1989, Blakemore 2000 patients) were not read.

## Claims
- The motor system holds a goal or desired state, an inverse model ("controllers") that maps the desired state to motor commands, and a forward model ("predictors") that maps the efference copy to a predicted state and predicted sensory feedback.
- The forward model makes two comparisons:
  - Predicted against desired, before movement. This drives fine correction.
  - Predicted against actual feedback, after movement. This "can be used to anticipate and compensate for the sensory effects of movement, attenuating the component that is due to self-movement from that due to changes in the outside world".
- What reaches awareness: the goal or desired state and the predicted state. Motor commands, fine adjustments, the actual state and the comparator outputs do not, "as long as the desired state is successfully achieved."
- Delusions of control: "the prediction mechanism is faulty, and as a consequence self-generated movements are not attenuated and are wrongly classified as externally generated." The patient is aware of the goal and of the movement, but "not aware of having initiated the movement."
- Each syndrome is a lesion of one arrow in a single diagram:

  | Syndrome | Lesioned arrow |
  |---|---|
  | Optic ataxia | Affordances no longer tune the inverse model |
  | Anarchic hand | Affordances no longer inhibited by the current goal; the discrepancy is noticed |
  | Utilization behaviour | No goal formed; the discrepancy is not noticed |
  | Phantom limb, and its loss over time | The forward model keeps predicting movement, then adapts to the absent feedback |
  | Delusions of control | The predicted state is unavailable |

## Evidence (as reported here, numbers from the cited studies)
- Self-tickle. A robot interposed between the hands added delays of 0, 100, 200 and 300 ms. There was "a striking correlation between delay and the perceived 'tickliness'", yet "none of the subjects had noticed the delays."
- Awareness of initiating a movement comes about 80 ms before the movement (Libet). Awareness of a target jump lags the motor correction by more than 200 ms (Castiello).
- Fourneret & Jeannerod: participants made large hidden deviations to draw a straight line and did not report them.
- Patients with passivity symptoms or auditory hallucinations show no attenuation of self-produced touch. Psychotic patients without these symptoms, and controls, do show it (Blakemore et al. 2000).

## Formal model (the paper's Fig. 1, written as equations; my notation, not the paper's)
- Motor command: u_t = π(s*, ŝ_t, affordances).
- Forward model: ŝ_{t+1} = f(ŝ_t, u_t) and ŷ_{t+1} = h(ŝ_{t+1}).
- Self-attribution signal: e_t = y_t − ŷ_t. The percept is y_t − α·ŷ_t (attenuation). The event is classed as self-caused when |e_t| is small.
- The paper gives no likelihood, no threshold and no learning rule. "The exact threshold above which the discrepancy becomes available to awareness is currently unknown."

## License
Journal article, © Elsevier. Author copy on the lab site; not redistributable. No code.

## Verdict: adopt (as the ablation map for self/other attribution), with its own limits noted
- It gives the canonical decomposition of self/other attribution in motor control, and a lesion table that already reads as ablation predictions.
- It is verbal. The comparator is a difference, not an inference.
- Haggard 2017 and Synofzik 2013 (separate notes) point out that a comparator registers only non-agency. It produces no positive signal for successful agency.

## What it implies for the single core
- **Agency attribution comes from the forward model the core already needs.** Any core that predicts its own sensory input from its own actions (active inference, an RSSM world model with an action input) has ŷ(u). Self-attribution of a change is then the part of the change that ŷ(u) explains. Partner attribution is the residual that a model of the partner explains better than the world prior does.
- So agency is not a new variable. It is a decomposition of prediction error by source: e = e_self + e_partner + e_world. The decomposition requires the generative model to carry separate causal channels: own action, partner action, exogenous.
- **Attenuation is the readout.** The percept is y − α·ŷ_self, so self-caused input is weaker. For the face, the agent's own expressions seen in a mirror or in the partner's mimicry should be attenuated relative to the partner's spontaneous expressions. That gives a measurable internal signature without a label.
- **Ablations derived from the lesion table:**
  - Ablate the efference-copy path (ŷ computed without u). Self-caused partner responses, such as the partner mirroring the agent, are classed as partner-initiated and are not attenuated. The analogue of passivity: the partner's mimicry of the agent's own smile would drive the agent's state as strongly as a spontaneous partner smile.
  - Ablate goal inhibition of affordance-driven responses (the anarchic-hand arrow). Reflex mimicry escapes the current policy.
  - Freeze forward-model learning. The phantom-limb analogue: predictions of the partner's response to the agent's acts do not adapt when the partner stops responding.
- **The project's own problem.** contingency-causal-synthesis.md shows that in a closed loop with a following partner, a naive comparator misattributes. Here the comparator sees y − ŷ(u). If the partner is reflexively mimicking, the error is small and the event reads as self-caused. That is not wrong (the agent did cause it), but it cannot separate "the partner copies me" from "the partner responds to me". The instrument fix in that synthesis (the agent's own exogenous variation) is what makes the decomposition identifiable.
