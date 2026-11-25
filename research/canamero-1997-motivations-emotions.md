# Cañamero 1997, "Modeling motivations and emotions as a basis for intelligent behavior"

Dolores Cañamero, in W. L. Johnson (ed.), *Proceedings of the First International Conference on Autonomous Agents (Agents '97)*, ACM Press, pp. 148–155, doi:10.1145/267658.267688.

**Source read: the full text was NOT read.** Attempts:
- dl.acm.org returned HTTP 403.
- Semantic Scholar marks the paper CLOSED.
- OpenAlex reports no open-access copy and "any_repository_has_fulltext: false".
- Web searches found no author-hosted, CiteSeerX or archive.org copy.

What I did read:
1. The abstract, from the Sciweavers record. It is truncated at the end.
2. How the group's later papers, read in the original, describe and build on the architecture: Lewis & Cañamero 2016, *Adaptive Behavior* (read in full; see lewis-canamero-2016-hedonic-pleasure.md), and Avila-García & Cañamero 2005, "Using hormonal feedback to modulate action selection in a competitive scenario", AISB'05 symposium proceedings (architecture section read, uhra.herts.ac.uk/id/eprint/12751).

Anything below that is not in the abstract is the lineage as these later papers describe it. It is **not** a verified account of the 1997 mechanism. I deliberately do not repeat details remembered from secondary literature (creature and world names, the exact list of hormones), because I could not check them.

## Claims (from the abstract)
- An autonomous creature in a two-dimensional world, built in the Society of Mind framework from a developmental perspective. "Phases in the experiment correspond broadly to cognitive stages in the development of an infant". This paper covers the first stage, a "newborn".
- The newborn's behavior is "strongly driven by motivational states (impulses to action based on bodily needs) and basic emotions (peripheral and cognitive responses triggered by the recognition of a significant event)".
- "Physiological parameters are used to model both concepts, which are seen by analogy with control systems."
- "Motivations drive behavior selection and organization based on the notions of arousal and satiation, and the exploitation principle."
- "Emotions exert further control by sending 'hormones' that may affect the intensity of the selected behavior, enable it, or ..." The abstract is cut off here.

## Architecture (lineage, as later papers state it)
- **A synthetic physiology** of homeostatically controlled essential variables, each with a setpoint. Leaving the viable range means "death" (Ashby's viability).
- **Motivations** are tendencies to keep homeostasis given internal deficits and external cues. Each motivation controls one physiological variable. The later formalization (Avila-García et al. 2003; Avila-García & Cañamero 2005; Lewis & Cañamero 2016) is $m_i = d_i + d_i\,\alpha\,c_i$, where $d_i$ is the deficit, $c_i$ the incentive cue and $\alpha$ a cue weight. Whether the 1997 paper used this form was not verified.
- **Behaviors** are coarse-grained subsystems ("similarly to those proposed in (Maes, 1991; Cañamero, 1997)"). They are consummatory or appetitive, and executing them changes physiological variables.
- **Emotions** are a second layer. They are triggered by recognizing significant events, and they release "hormones" that modulate the intensity of the selected behavior or enable it. Later papers turn this into hormonal modulation of *perception*: of external cues (Avila-García & Cañamero 2005, in a competitive scenario) and of internal variables (prey and predator). It becomes the pleasure hormone that scales α in Lewis & Cañamero 2016.
- The group itself calls this its "longstanding approach (Cañamero, 1997, 2001) to ground embodied cognition and interaction in 'core' affect modeled around a 'physiology' of homeostatically-controlled essential variables" (Lewis & Cañamero 2016, §2).

## Evidence with numbers
Not read. The abstract reports no numbers. It describes a first-stage simulation of a "newborn" and gives no evaluation design.

## Failure modes (judged from the abstract and the lineage; to be confirmed on reading)
- **Hand-named basic emotions as separate modules.** The abstract describes "basic emotions" triggered by recognizing significant events. This is a discrete-emotion layer on top of motivations: two mechanisms (motivations; emotion-released hormones), not one principle.
- **Hand-set physiology and triggers.** The variables, setpoints, emotion triggers and hormone effects are designed. In this first stage nothing indicates that emotion or its triggers are learned. The developmental program (later stages with learning) is promised, and its follow-through was not checked here.
- **Persistence and ablations:** unknown from the material read.
- **Its descendants inherit the pattern.** In Lewis & Cañamero 2016, the clearest descendant read in full, all parameters are still empirical and the run-level evidence has no statistics.

## License
ACM copyright. No public full text found. No code.

## Runs on this Mac without a GPU?
n.a.

## Verdict: watch (unread; cite only as the origin of the homeostatic-motivation lineage)
It is the root of a line the project already draws on (canamero-attachment-robotics.md, lewis-canamero-2016-hedonic-pleasure.md, ho-avilagarcia-nehaniv-2005-wta-voting.md). From the abstract it conflicts with Principle 2 (named basic emotions sending hormones) and Principle 10 (motivations and emotions are separate mechanisms). Its lasting contribution is to treat motivation as homeostatic control of physiological variables, with satiation built in. That idea survives Principle 6.

## What it implies for this engine
- **Survives: the innate body as essential variables with viability bounds, and motivation as a deficit gated by cues.** This is what Principle 2 means by "a set of body variables to regulate and a few reflexes". Cañamero 1997 is the standard precedent for it in robotics.
- **Survives: the developmental framing.** A newborn driven by bodily needs is "stage 1", and later stages are learned. That is the brief's long-term goal (an innate body first, emotions acquired by living). Whether the program ever got past stage 1 should be checked before the project claims novelty on this point. On the evidence read, the group's later robots (Robin, ALIZ-E) kept a hand-designed physiology plus modulators, and did not learn emotion structure.
- **Does not survive: basic emotions as a separate, event-triggered layer that releases hormones.** In the engine, what the 1997 design calls emotion must come out of the same core that does homeostasis (Principle 10), and it must not be a set of named triggers.
- **Action:** if the full text becomes available (ACM access, or an interlibrary request), redo this note. The questions are which "basic emotions" were used and how they were triggered, whether any learning occurred, and whether any evaluation was reported.
