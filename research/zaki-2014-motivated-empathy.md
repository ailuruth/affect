# Zaki 2014, "Empathy: A motivated account" (Psychological Bulletin 140(6):1608-1647, doi 10.1037/a0037679)

Source read: full article PDF (author-lab copy, ssnl.stanford.edu). Read in full: the abstract, the sections on automaticity and context dependency, the model (ultimate sources, proximate mechanisms, the three regulatory strategies), and the evidence sections on avoiding pain, avoiding costs, avoiding interference with competition, approaching capitalization and approaching affiliation. Approaching desirability, the Implications section and the clinical part were skimmed. Tables 1-2 (the 6 × 3 grid and about 100 study summaries) were read only as flattened text, so the mapping of some rows to studies is uncertain. This is a narrative review. Every study below is cited as Zaki describes it; I did not read the primary papers.

## Claims
- Empathy has three dissociable parts. **Experience sharing** means taking on the target's sensory, motor, visceral and affective states. **Mentalizing** means explicit inference about the target's intentions, beliefs and emotions, drawing on "lay theories" and citing Baker, Saxe & Tenenbaum 2009 and Ong, Zaki & Goodman. **Mind perception** means detecting that the target has internal states at all. Experience sharing and mentalizing often compete ("a hydraulic relationship").
- Empathy is both automatic and context dependent. Zaki reconciles the two with **motives**:
  - three avoidance motives: suffering (it hurts), material costs (it obliges helping), and interference with competition;
  - three approach motives: positive affect ("capitalization" on others' good states), affiliation, and social desirability.
- Motives act through three **regulatory strategies**, which operate before, during and after the empathic response:
  - **situation selection**: whether one is exposed to the target's cues at all;
  - **attention modulation**: attending toward or away from the target's affective cues;
  - **appraisal**: re-interpreting what the cue means. Zaki names four forms:
    - (a) believing the display is exaggerated or understated;
    - (b) whether the target is responsible for the state;
    - (c) whether the target deserves it;
    - (d) whether the target's state is, on balance, good for the observer. "Under zero-sum competition ... observers often appraise targets' affect incongruently (seeing target suffering as a positive cue, and vice versa)": schadenfreude and gluckschmerz.
- Goals and strategies can be implicit. Regulation can stop empathy from arising at all, not only damp it afterwards.
- Zaki frames the motives as costs and benefits that "together provide a net signal as to whether an individual should engage". Social distance (Preston & de Waal's familiarity and similarity) acts first on motives, and motives then set how richly the target is represented.
- A developmental conjecture: experience sharing may start as "a ballistic, undifferentiated response to the emotions of all targets". Learned social rules (group membership) then "tune" it.

## Evidence
- **Speed of the context effects.**
  - Reduced neural resonance to outgroup pain appears by about 200 ms (Sheng & Han 2012, ERP).
  - Physicians show blunted ERP to needle-pricks by 110 ms (Decety et al. 2010).
  - Context therefore acts on the earliest measurable response, not only through later deliberation.
- **Competition produces counter-responses, not only reductions.** Opposite reactions are reported in:
  - self-report (Cikara et al. 2014; Yamada & Decety 2009);
  - facial expression (Cikara & Fiske 2012: subthreshold smiles while reading about outgroup targets' suffering; van der Schalk et al. 2011: outgroup anger answered with fear and outgroup fear with aversion, i.e. countermimicry; Weisbuch & Ambady 2008: outgroup negative affect primed positive emotion);
  - autonomic arousal (Lanzetta & Englis 1989: counterempathic responses to competitive but not cooperative targets);
  - reward-related brain activity (a competitive target's misfortune; an unfair target receiving shocks, T. Singer et al. 2006, in male observers only).
  - Counterempathy is reported in negotiations, minimal groups, zero-sum games and sports fandom. The grid cell "competition × attention/appraisal" has 30 or more studies.
- **Affiliation raises mimicry, which is evidence that mimicry can be a signal.**
  - Observers mimicked a target's pained grimace more when they believed the target could see them (Bavelas et al. 1986).
  - Outcome dependency, i.e. expecting to share a task or outcome, increased looking at and mimicking the target (Gump & Kulik 1997) and taking on the target's expected mood (Huntsinger et al. 2009).
  - Rejection increased mimicry (Lakin, Chartrand & Arkin 2008), empathic accuracy (Pickett et al. 2004) and attention specifically to smiles (DeWall, Maner & Rouby 2009).
  - Self-monitoring predicted mimicry of high-power but not low-power targets (Cheng & Chartrand 2003).
- **Social need behaves like a satiable drive.** Satiating it (thinking about close ties) increased later dehumanization of outgroups (Waytz & Epley 2012). Loneliness increased anthropomorphism (Epley et al. 2008).
- **Pain avoidance.**
  - Passers-by kept a wider berth from a charity table showing a suffering rather than a healthy child (Pancer 1988).
  - Observers prefer to avoid future interactions with depressed people (Coyne 1976).
  - Expecting empathy to be exhausting predicted dehumanizing the target (Cameron, Harris & Payne 2014).
- **Valence-specific capitalization.** High trait positive affect and mania risk predicted inaccuracy for targets' negative but not positive affect (Devlin et al.; Dutra et al. 2014). Older adults attend preferentially to positive faces (Isaacowitz et al. 2006).
- **The grid is uneven.** Zaki says the evidence is "highly imbalanced": some cells have 30 or more studies and others almost none, e.g. selecting oneself into others' positive affect.

## Formal model
None. The model is verbal: a 6 (motive) × 3 (strategy) grid, a schematic in Figure 1, and a "net signal" of approach against avoidance. No equations, no fitted parameters and no quantitative predictions.

## What it implies for the design
- **The three strategies sit at three different places in an inference architecture.**
  - Situation selection is *policy over what to observe*: an action choice, including gaze.
  - Attention modulation is *precision on the partner channel*.
  - Appraisal is *the likelihood model itself*: how the partner's expression maps onto the shared situation and the agent's own concerns.
- **Only the third gives sign flips.** Zaki's mechanism for counterempathy is appraisal form (d): the target's state is evaluated *relative to the observer's outcome*, so under a zero-sum structure the observer's valence is the negative of the target's. This is exactly the hypothesis that "the expression is evidence about the shared situation, interpreted against the agent's own concerns". It is support, at the level of a verbal account, for putting the sign in the concern map rather than in a coupling gain.
- **Attention modulation is the hidden dial again.** If motive acts only by turning the precision on the partner's expression up or down, one scalar runs the agent from flat (precision 0: the partner is ignored) to full contagion (precision high: the partner's state dominates the agent's posterior). This is the same failure the critiques found in every sketch (critique-design-*.md; v2-README.md, "all eight break on the same point").
  - An appraisal design must therefore show that high precision on the partner's expression produces *a confident estimate of the partner's state*, not *adoption of it*.
  - That holds only if the agent's own affect is computed from its own concerns given that estimate, with no direct term that pulls the agent's state toward the partner's.
- **Zaki's own frame contains a scalar.** "A net signal as to whether to engage" is a one-dimensional approach-avoid summary per episode, which is the dial at the level of theory. The evidence he reviews is not one-dimensional, however:
  - capitalization targets positive states and pain avoidance targets negative states, which is gating per valence;
  - competition flips sign, and does not merely subtract;
  - affiliation raises mimicry of a grimace only when the agent is visible, so it is communicative and depends on whether the expression is addressed to the agent.
  - A faithful design would carry motive × partner-state valence × strategy, not one engagement level.
- **This matches the mimicry-context table.** Seibt 2015's brow relaxation at a rival's distress, Carr 2014's smile at anger, and van der Schalk 2011's fear at outgroup anger are all appraisal-form (d) responses: what the partner's state means for me.
- **Smile return is robust and close to context-free** (mimicry-context-synthesis.md, row 1). This fits Zaki's capitalization motive, since a partner's positive state is good for the observer under almost any relation except zero-sum.
- **Tension with Principle 3.** Zaki treats experience sharing (driving the agent's own states from the partner's) and mentalizing (inferring them) as separate systems that compete. Principle 3's second clause ("infers another's state by inverting its own generative mapping") is mentalizing done in body coordinates. Its first clause ("perceived features drive the agent's own motor and affect pathways") is experience sharing.
  - The evidence here says experience sharing is the component that motives turn down to zero or invert.
  - If an agent keeps the first clause as a direct path, that path needs its own sign source. Otherwise it is the scalar.
- **Social need as a drive.** The satiation result (Waytz & Epley 2012: satiating social need increases dehumanization) is the one place where the motive behaves like a homeostatic variable. It suggests deriving "engagement" from a satiable affiliation need rather than setting it. It would still be a scalar unless its effect is routed through appraisal.

## Verdict: adopt (as the framework for where motive acts), with a warning
This is the clearest statement in the literature that context acts in three places, and that the sign flip lives in appraisal (the partner's state evaluated against the observer's own outcome) rather than in the strength of sharing. Do not adopt its "net approach/avoid signal" as a mechanism: that is the flat-to-copy dial stated as theory. Every cited effect is second-hand from a narrative review.
