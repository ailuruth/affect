# Boucenna, Gaussier, Andry & Hafemeister: a robot head learns facial expressions because the human imitates it (2008-2014)

Target paper: Boucenna, Gaussier, Andry & Hafemeister, "A Robot Learns the Facial Expressions Recognition and Face/Non-face Discrimination Through an Imitation Game", International Journal of Social Robotics 6(4):633-652, 2014, doi:10.1007/s12369-014-0245-z.

Source read, honestly:
- The IJSR 2014 journal paper was **not read**. It is paywalled, and HAL holds only a record with no file (hal-01738583).
- Read in full instead, the two conference papers whose content the journal paper consolidates:
  - Boucenna, Gaussier & Andry, "What should be taught first: the emotional expression or the face?", EpiRob 2008 (HAL hal-00522705, 9 pages). It has the formal two-agent argument, the ε table and the face/non-face results.
  - Boucenna, Gaussier, Andry & Hafemeister, "Imitation as a Communication Tool for Online Facial Expression Learning and Recognition", IROS 2010 (HAL hal-00522773, 7 pages). It has the multi-person study.
- The figure-only numbers in IROS 2010 (Figs. 6 and 7) could not be read from the extracted text.
- A related paper, Boucenna, Anzalone, Tilmont, Cohen & Chetouani, "Learning of Social Signatures Through Imitation Game Between a Robot and a Human Partner", IEEE TAMD 6(3):213-225, 2014, was **not read**. It is closed access (HAL hal-02423049, no file). From its record it is about learning *postures* from adults, typically developing children and children with autism, not facial expressions, and it has different co-authors.

## Claims
- A baby or robot can learn to recognise others' facial expressions with no teaching signal and no face detector, provided that (a) it displays expressions driven by its own internal state and (b) the partner imitates those expressions. "The learner must produce facial expressions first and be mimicked by his/her caregiver" (2008, 2010).
- From the formal model (Gaussier 2004, cognitive system algebra, not read): "If both agents display their internal emotional state S1 and S2, the learning is impossible if we suppose both agents have independent emotional states... the only solution is to suppose that the second agent mimics or resonate[s] to the facial expressions of the baby... (the parent is no more than a mirror)" (2008, §2).
- Imitation is "a communication tool instead of [a] learning tool": the caregiver communicates with the robot by imitating it.
- Recognising faces is harder to learn autonomously than recognising expressions, and expression recognition can bootstrap face/non-face discrimination. The robot uses the predictability of the interaction rhythm as a reward that says a partner is present.

## Architecture (as given)
Formal agent (2008, Fig. 3):
- R_i = c(A_i1 · V_i). Visual recognition by a competitive mechanism c (WTA, ART or Kohonen).
- E_i = c(I · S_i + A_13 · R_i). The emotional state is driven one-to-one by internal signals S_i ("fear, hunger...") through an unconditional link, plus a learned visual input.
- F_i = c(I · E_i + A_12 · R_i). The facial expression is driven one-to-one by the emotional state, plus a learned visual input.
- Only the A matrices are learned. The identity links S → E → F are innate reflexes.

Robot implementation (2008, 2010):
- Head: 13 servos (4 eyebrow, 1 forehead, 5 mouth, 3 camera). There are five prototypical expressions (sadness, happiness, anger, surprise, neutral; the text also lists "hunger" once), each calibrated by FACS experts (Nadel's group). An expression change takes 200-400 ms.
- Internal state IS: 5 neurons, one per expression. During learning, a **random generator** picks an expression, the robot holds it for 2 s and then returns to neutral for 2 s. No body, drive or stimulus sets the state.
- Vision, with no face framing: gradient, then a DoG filter giving focus points. About 10 most-active focus points per image (about 7 of 10 land on the face). At each, a log-polar patch (radius 20 px), plus Gabor mean and standard deviation in 2010.
- VF (local-view prototypes) is online k-means with recruitment. VF_j = net_j · H_{max(γ, mean(net)+σ_net)}(net_j), with net_j = 1 − (1/N) Σ_i |W_ij − I_i|. A new neuron is recruited when the best match falls below the vigilance γ. The update is ΔW_ij = δ_jk (a_j(t) I_i + ε (I_i − W_ij)(1 − VF_j)): one-shot copy on recruitment, slow averaging otherwise.
- ISP (internal-state prediction) uses the LMS rule: Δw_ij = ε · VF_i · (IS_j − ISP_j). This is error-driven, so local views present during every expression (background, hair) converge to zero weight.
- STM sums ISP over the views of one image: STM_i(t+1) = (1/N) ISP_i(t+1) + ((N−1)/N) STM_i(t). Output: F_i(t+1) = β STM_i(t+1) + α F_i(t), with β = 1 and α ≈ 0.8, then WTA to one expression. After learning, the visual route is "strong enough to bypass the low level reflex activity coming from the internal state", so the robot imitates the human.
- Face/non-face (2008): a rhythm predictor (derivation group, a 15-neuron temporal battery, and a prediction group; Andry et al. 2001). It predicts either the interval between the partner's motion peaks or the delay from the robot's own expression to motion seen in the camera. Low prediction error gives a "rhythm OK" neuron, high error a "rupture" neuron. The tensor product of this 2-neuron reward with E (5 neurons) gives X (10 neurons); Y learns R → X by LMS; STM3 accumulates; an LMS group FD (2 neurons) learns face versus non-face from STM3 against the rhythm signal.

Protocol: a learning phase of 2-3 min (2010) or 5-10 min (2008), "according to the subject's patience", with the human **asked** to mimic the robot. Then the random generator is stopped and the robot imitates the human.

## Evidence with numbers
- 2008, single subject, effect of the averaging constant ε (γ = 0.92), accuracy over the five classes (chance 20%):

  | ε | sadness | neutral | happy | anger | surprise | total |
  |---|---|---|---|---|---|---|
  | 1 | 49% | 6% | 92% | 64% | 42% | 51% |
  | 0.1 | 51% | 4% | 92% | 66% | 49% | 52% |
  | 0.01 | 51% | 34% | 94% | 67% | 49% | 59% |
  | 0.001 | 49% | 51% | 79% | 70% | 57% | 61% |
  | 0.0001 | 49% | 51% | 78% | 69% | 56% | 60% |

- 2008, face/non-face: trained and tested on the same subject, near 100%. Trained 10 min on one subject and tested on 4 others: 29% (bearded) to 90%. Trained on 3 subjects (1500 images) and tested on 5 others (5000 images): about 70%.
- 2010: 10 people, 2 min of learning each, 32 test images per expression per person. Generalisation to unseen people after 20 people had trained. Per-expression rates are only in Figs. 6 and 7 (not read numerically). Sadness was worst; the authors suggest people "have difficulties to display sadness without a context". The neutral face was misrecognised in the dynamic test (Fig. 8b, 2008 Fig. 9b).
- Loop timing: the period from robot expression to human recognition to human mimicry was about 800 ms for expert subjects and 1.6 s for novices. If the robot learns from the first frames after its change, it pairs its new state with the human's *previous* expression and "the previous expression is unlearned". The fix was to hold each expression long enough to "neglect the first images". The lag was not modelled.
- Ablations: none, beyond the ε sweep. Faster whole-image architectures from earlier work are mentioned but not compared here. There is no non-imitating-partner control, although the formal argument predicts that learning should fail without one.

## Failure modes
- **The "internal emotional state" is the robot's displayed-expression label.** Five hand-named categories are set at random during learning. They regulate nothing and come from no body variable (against Principle 2). In effect it is supervised learning in which the robot's own display supplies the label and the human supplies the matching image.
- **Wired:** the expression set (FACS-calibrated prototypes), the one-to-one state → face reflex, the emotion categories, the competitive read-out, and the learning/test phase switch. **Learned:** visual prototypes and the view → state association. Mimicry *by* the robot is learned (it emerges once the visual route overrides the reflex). Mimicry *by* the human is instructed.
- **No persistence.** There is no state beyond a short-term filter, and no development once the generator is switched off. The learning phase was "completely predefined" (the authors' own criticism, which motivated the rhythm reward).
- **Assembled.** The pieces are separate modules (focus-point vision, k-means, LMS, STM, WTA, rhythm predictor, tensor-product gating). The formal model unifies only the conditioning step.
- **The human requirement is heavy:** an instructed, attentive mimic for minutes, at about 1 s latency. The authors note that "some human partners are not expressive".

## License
HAL deposits (author versions); the IJSR paper is © Springer. No code found (the group's neural simulator was not checked).

## Runs on this Mac without a GPU?
Yes. Small online k-means and LMS layers at 3-5 images/s in 2010 hardware terms. No code released.

## Verdict: adopt (the formal identifiability condition and the lag finding), reject (the emotion model)
The cleanest prior statement of the condition this engine's learned self-other face map depends on, and the only one with a multi-person test and a measured interaction lag. The emotion side is five labels on a random generator.

## What it implies for this engine
- **The identifiability condition, as a derivable proposition.** Gaussier's argument says the association between own state and partner face converges only if the partner's display is statistically dependent on the agent's state. If the two states are independent, the map does not form. The engine's formal core should state this as a proposition (the self-other map is identified only under partner dependence on the agent's display) and derive the ablation from it: replace the operator's responses with a time-shuffled copy, and the map does not form.
- **What "caregiver as mirror" asks of the operator.** It needs (a) responses congruent with the agent's display, (b) at a stable lag (here 0.8-1.6 s), (c) often enough, over minutes. Boucenna got this by instruction and Watanabe by an intuitive-parenting caregiver. An adult operator will not do it unprompted at that rate (face-development-synthesis.md, risk noted there). The engine must measure how much partner dependence a session actually holds, and must not assume it.
- **Error-driven, not Hebbian.** The LMS rule is why background features drop out: they predict no particular state. This is the contingency property Watanabe's pure Hebbian rule lacks (watanabe-ogino-asada-2007-intuitive-parenting.md). Keep it.
- **The lag is the main practical failure.** A mirror arriving 1 s late, paired at zero lag, teaches the wrong map. Model the response lag explicitly and learn it (stoytchev-2011-self-detection-temporal-contingency.md).
- **The follower confound has two sides here.** During learning the human follows the robot. From inside, that partner looks like the robot's own effect (gold-scassellati-2009-robot-self-recognition.md). The design works only because the robot never asks whose face it is. After learning, the robot follows the human, and if the human keeps mirroring, the loop is an echo with no new information. In the engine, learning must be weighted toward moments when the agent's display was spontaneous, meaning driven by its own state and not by the partner. Partner-independent variation is what identifies "the partner answers me".
- **Rhythm as evidence of a partner.** The predictability of the partner's motion relative to one's own expression changes signals that someone is engaged. This is a cheap, label-free "a partner is answering" signal. In this engine's terms it is a contingency estimate, not a reward to maximise: Principle 6 forbids rewarding partner attention.
- **The robot's states must come from a body, not a dice roll.** Boucenna's random state generator gives clean, balanced, independent labels. An engine whose states come from its body and from the operator will have states correlated with the operator's behaviour, which is the confound above, so that correlation has to be handled explicitly.
