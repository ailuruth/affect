# Asada 2015, "Towards Artificial Empathy: How Can Artificial Empathy Follow the Developmental Pathway of Natural Empathy?"

International Journal of Social Robotics 7(1):19-33, doi:10.1007/s12369-014-0253-z. Open access (Creative Commons Attribution License).

Source read: the published PDF from SpringerLink, 15 journal pages, read in full apart from the reference list. Figures were read from their captions and the text that describes them; the diagrams themselves (Figs. 2-9) were not visible in the extracted text. The companion paper, Asada 2015, "Development of artificial empathy", Neuroscience Research 90:41-50, was not read; it is not in PMC, and only the DOI landing page was located.

## Claims
- It proposes "affective developmental robotics" (ADR) as the affective branch of cognitive developmental robotics (CDR). Empathic behaviour should be learned through social interaction, not specified by a designer. The paper's criticism of existing emotional robots (WAMOEBA, WE-4RII) is that "almost all of robot behaviors are explicitly specified by the designer, little space is left for robots to learn or develop the capacity to share their emotional states with humans".
- Empathy develops in parallel with imitation (de Waal's Russian doll) and with self-other cognition. The proposed order is: emotional contagion (with motor mimicry), then emotional empathy (EE) and cognitive empathy (CE), then sympathy and compassion, then envy and schadenfreude.
- One mechanism underlies the sequence: **synchronization (entrainment)**. Contagion, EE and CE are synchronization of one's emotional state with another's. Sympathy and compassion are "inhibition of synchronization", a de-synchronization that needs self-other discrimination and emotion regulation. Envy and schadenfreude need in-group/out-group cognition and metacognition.
- Self-development has three stages, said to be "seamlessly connected", following Neisser:
  1. Ecological self: synchronization with objects (rhythmic hitting, reaching) until phase-locked.
  2. Interpersonal self: the caregiver initiates synchronization. Infants first treat caregiver actions as their own ("like me"), then as other ("different from me"). Turn-taking is described as a 180° phase difference, and the agent learns "when to inhibit his/her behavior by detecting the phase difference".
  3. Social self: switching synchronization between partners, then make-believe with virtual objects.
- "These substructures are not added but expected to emerge from previous stages." This is asserted, not shown.
- "Designing a computational model that can explain the developmental process shown in Fig. 6 is very challenging, and such a model does not yet exist."
- Language is excluded from the model, on the grounds that severe aphasics retain theory of mind.
- Two admitted gaps: "we have not considered emotional states coming from visceral organs... a homeostasis-like structure is needed", and the relation of intrinsic motivation to empathy is open ("Explicit or implicit? That's an issue to be addressed further").

## Architecture (as given)
This is a conceptual model, with no equations.
- Fig. 2 places empathy terms on two axes: unconscious → conscious with self-other distinction, and physical/motor → emotional/mental. The whole story runs along "a gentle slope from the bottom-left to the top-right".
- Fig. 4: one entrainment mechanism with substructures added in stages: synchronization, then inhibition (for turn-taking), then switching.
- Fig. 6 shows seven points from "no self-other discrimination" (1) to "completely separated agent representations with different emotional states" (7). Its parts are:
  - a synchronization base under contagion, EE and CE;
  - inhibition of harmonization, built on agency, for sympathy and compassion;
  - a split into a subjective and an objective (virtualised) self for metacognition, such as enjoying sad music;
  - group-level synchronization for envy and schadenfreude.
- Fig. 9 gives a neuroanatomical draft for Watanabe et al. 2007. The caregiver's face is processed in IFG and/or insula and mapped onto dACC, which "maintain[s] the learner's emotional space that drives facial muscles". The learner's own state is in the amygdala and its reflection of the caregiver's state in dACC. The author says the neural substrates are not consistent across the studies cited.
- Table 1 (from Shamay-Tsoory) separates EE (simulation, IFG BA44, infants, rodents and birds) from CE (mentalizing, VM BA10/11, children and adolescents, chimpanzees). It lists Smith's seven EE-CE relationship models and four empathy disorders (CEDD, EEDD, GEDD, GESD) as targets for "a control module of EE sensitivity and CE ability".
- Oxytocin and opioids are proposed as modulators of emotional empathy and dopamine of cognitive empathy, "to characterize empathic disorders... with our computational model".

Studies the paper reviews as implementations of points on Fig. 6:
- Mori & Kuniyoshi fetal and neonatal simulation: 198 neural oscillators and 198 muscles, with self-organised movement. It is the base for motor resonance.
- Nagai et al. 2011: early mirror-system development from immature vision. Low visual resolution at first makes self- and other-actions look equivalent, so both get bound to the same motor commands. As vision sharpens, the self/other distinction appears, but the early association is kept, giving motor ↔ self-observation and motor ↔ other-observation links that enable imitation. Asada places it between points 1 and 2-3. Summarised secondhand here; the primary was not read.
- Kuriyama et al.: interaction-rule learning from contingency and intrinsic motivation for play.
- Watanabe, Ogino & Asada 2007: intuitive parenting (see watanabe-ogino-asada-2007-intuitive-parenting.md). It is presented as the move from contagion to emotional empathy.
- Takahashi et al.: recognising others' behaviour by the transition of one's own learned state values, as a route to perspective-taking.
- Affetto, a realistic child-like android face, as a platform.

## Evidence
None. It is a position and review paper. No implementation, experiment, number or ablation is reported. The studies it reviews are cited for their own (small, mostly qualitative) results.

## Failure modes
- **Stages and modules are added by hand.** The text hopes later structure emerges from earlier stages, but the conceptual architecture is a ladder of added substructures, inhibition and switching. Neither a single objective nor a derivation is offered (against Principle 10).
- **Hand-named emotion axes.** The reviewed implementation, Watanabe, uses Russell's pleasure and arousal as state variables. Asada treats them as "the most fundamental emotional axes" that infants are born with (against Principle 2, which makes them readouts).
- **Wired vs learned.** Motor resonance is said to be "fairly hardwired or at least functional very early", citing Sommerville. That contradicts the associative account the project holds (ray-heyes-2011-wealth-of-the-stimulus.md, cook-2014-mirror-neurons-origin.md). The Nagai model it reviews instead *learns* the self-other correspondence.
- **No body.** Visceral and homeostatic sources of emotion are admitted to be missing.
- **No persistence, no evaluation, no ablation.** There is nothing to evaluate.
- **Neuroanatomy as decoration.** The region mapping (IFG/insula → dACC, amygdala) is a draft the author himself calls inconsistent.

## License
CC BY (Springer open access). No code.

## Runs on this Mac without a GPU?
n.a. (conceptual).

## Verdict: watch (framing only)
It gives no mechanism to adopt. It is useful as a map of which empathy phenomena a developmental system should eventually produce, and as a statement, from the leading lab in the area, that no computational model of the whole pathway existed in 2015. Its proposed unifier, synchronization, is close to this project's coupled-dynamics directions, but it is stated without equations.

## What it implies for this engine
- **Sympathy as regulated decoupling.** This idea survives Principles 1-10 if it is derived and not added. If perceived faces drive an inferred-other state that couples into one's own state (Principle 3), then contagion is high coupling and sympathy is the same coupling with regulated gain, or with a sign or offset, so that one represents the other's distress without matching it. The engine's core should make that coupling gain a state-dependent quantity. Its ablations: fix the gain high, and the agent can only mirror; remove the coupling, and the agent reads the operator without being moved.
- **Phase relations as a test.** The stage claims translate into measurable dyadic signatures: near-zero-lag entrainment of the face (contagion, mimicry), and anti-phase alternation in voice and turn-taking (the interpersonal stage). These can be scored with the project's existing coupling analyses (coordination-synthesis.md), not taken from Asada.
- **The self-other map should be learned, not assumed.** Asada's own review contains both views: hardwired resonance in the text, learned correspondence in Nagai's model. The project's position (face-development-synthesis.md) sides with learning. Nagai's immature-vision idea adds a concrete curriculum: start with coarse perception, in which self and other are not yet separated, and let the distinction appear as resolution increases. In the engine this could be a coarse-to-fine schedule on the perceptual precision of the operator's face. It needs its own primary read before use.
- **The prior-work gap holds here too.** No affective developmental robot in this review has a homeostatic body, long-term living, or ablations. Asada names the first as missing.
