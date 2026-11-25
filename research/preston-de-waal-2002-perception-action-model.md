# Preston & de Waal 2002, "Empathy: Its ultimate and proximate bases" (Behavioral and Brain Sciences 25(1):1-20, with commentary to p. 72; doi 10.1017/S0140525X02000018)

Source read: the publisher PDF (Cambridge Core). Read in full: §1, which covers the introduction, terminology, Tables 1-3 and the overview of the model. The representation section was read through extracted passages: familiarity, similarity, past experience, salience, and the account of inhibition and prefrontal control. Not read: the ultimate-bases section beyond its opening and competitor passages, most of the proximate neuroscience review, and the Open Peer Commentary. The reply to commentators was not read. Read here as the contrast case to social appraisal.

## Claims
- **The Perception-Action Model (PAM).** In the authors' words: "attended perception of the object's state automatically activates the subject's representations of the state, situation, and object, and that activation of these representations automatically primes or generates the associated autonomic and somatic responses, unless inhibited."
  - "Object" is the one who has the emotion; "subject" is the one who empathizes.
  - "Automatically" means "as a matter of course, unless controlled or inhibited", and does not require conscious processing.
- **Empathy is defined by process, not by result.** It covers any process in which the attended perception of the object's state produces a state in the subject "more applicable to the object's state or situation than to the subject's own prior state". Emotional contagion, sympathy, cognitive empathy and helping are subclasses (Fig. 1). The model also extends to imitation, yawning and priming.
- **Five robust effects across species (Table 1).** Empathy increases with:
  - familiarity (prior experience with the object);
  - similarity (species, personality, age, gender);
  - learning;
  - past experience with the distress situation;
  - salience (louder, closer, more realistic).
- **The authors reduce four of the five to one mechanism:** "the greater the familiarity or similarity, the richer the subject's representation of the object". Following McClelland & Rumelhart, "the strength of the activation of a representation is proportional to the degree of overlap between the input and the representation". Salience raises the probability and extent of activation through attention. More similarity means more state-matching, better accuracy and less "projection".
- **Two kinds of response.**
  - Response *with* the object: matching, distress to distress, joy to joy.
  - Response *to* the object: instrumental, such as consolation to distress or fear to anger.
  - Matching emerges earlier and with less learning. Instrumental responses need experience.
- **Interdependence drives attention, and through it the response.** Interdependence can be temporary ("the object's distress blocks the goal of the subject") or lasting (kin, spouses). The PAM "extend[s] to the prediction and response to allies as well as competitors" and "can produce appropriate helping behaviors, as well as effective punishments".
- **Overt matching declines with age and experience.** The reasons are prefrontal inhibition, a growing separation of self and other representations, and display rules. Covert responses (the "distress keeper") can persist after attention is moved. Cognitive empathy is the PAM plus prefrontal working memory and inhibition.

## Evidence (as the authors report it)
- **Masserman et al. 1964, rhesus monkeys.**
  - After seeing a conspecific shocked when they pulled the larger-reward chain, two-thirds switched to the non-shock chain at half the food.
  - One monkey stopped pulling for 5 days and another for 12.
  - The effect was stronger for visual than auditory cues, in animals that had themselves been shocked, and with familiar conspecifics.
- **Church 1959, rats.** Bar pressing dropped on seeing a conspecific shocked:
  - most when the subject's own prior shock had been paired with the other's;
  - less after unpaired shock;
  - least, and habituating quickly, with no prior shock.
- **Similarity manipulations in humans.**
  - Similarity raised offers to take the target's shocks: similar observers offered even when they could leave, dissimilar ones only when they had to keep watching.
  - Krebs 1975: made-similar men showed more physiological response, identified more, and helped more.
  - Rosekrans 1967: boys imitated a model more when made to feel similar.
- **Physiological linkage.** Subjects who identify an object's emotion correctly show physiology correlated with the object's (Levenson & Ruef 1992). Empathically concerned subjects show heart-rate *deceleration* to a target's distress, a response *to* the object (Eisenberg et al. 1990-1994).
- These are all summaries. Most of Table 1 is from 1959-1997, much of it on distress only, and no effect sizes are pooled.

## Formal model
There are no equations. The model is verbal, but its quantitative core is explicit enough to write down. The subject's activated state is a match between the perceived object state and the subject's own stored representations. The size of that match grows with overlap, and the result is gated by attention (salience, interdependence) and by inhibition. Read literally:

response ≈ (1 − inhibition) · attention · overlap(similarity, familiarity, past experience) · [the subject's own representation of the object's state]

Every moderator in Table 1 enters as a multiplier on one matched representation.

## What it implies for the design
- **The PAM is the flat-to-copy dial in its original form.** Familiarity, similarity, past experience and salience all scale how strongly the *same* (matched) representation is activated, and inhibition scales it down. Any agent built on it has a single gain from flat (no overlap, or full inhibition) to copy (high overlap, no inhibition). This is the pattern found in every sketch and every design so far (v2-README.md, "all eight break on the same point"; critique-design-dyadic-sheaf.md: "a single scalar gain on a copy").
- **The model cannot produce the shape changes in mimicry-context-synthesis.md.**
  - A familiarity gain moves every expression the same way. Yet smiles are returned across groups while sadness switches on and off (Bourgeois & Hess 2008), and anger return rises while smile return stays flat after unfairness (Hofman 2012).
  - Inhibition can remove a response but cannot invert it. It cannot give a smile at anger (Carr 2014) or brow relaxation at a rival's distress (Seibt 2015).
- **The PAM names the missing part but does not supply it.**
  - Its "response *to* the object" (consolation to distress, fear to anger) and its "effective punishments" toward competitors are exactly the off-diagonal and sign-flipped entries the data require.
  - But the mechanism for them is only that the subject "accesses the object's state and generates an appropriate response". What makes a response appropriate (the subject's goals and its relation to the object) lies outside the perception-action core.
  - That missing step is what social appraisal and the Bayesian theory-of-mind models supply: the partner's state, once estimated, is evaluated against the subject's own concerns.
- **Principle 3 in brief.md is close to the PAM's text.**
  - "Perceived features drive the agent's own motor and affect pathways (mimicry)" is the PAM's automatic activation clause.
  - "Infers another's state by inverting its own generative mapping" is the PAM's own-representation idea used for inference rather than for driving.
  - The appraisal hypothesis keeps the second clause and makes the first one conditional. Otherwise the PAM's gain structure returns in whatever form the coupling takes. This is a note for the operator, not a reopening of the Principle.
- **One part is worth keeping: overlap of representations as a precondition for reading.** Understanding is easier for an object whose states map onto the subject's own representations (the PAM's "projection" versus "accuracy"). This is a case for reading the partner in the agent's own body coordinates (inference by an own-model). It is not a case for enacting what is read.
- **One scalar can be removed by derivation.**
  - The PAM's own reasoning for familiarity, a richer representation of the object, is a *precision* claim: better models give sharper estimates of the object's state.
  - In an inference design, familiarity should sharpen the *estimate* of the partner's state. It should not raise how much of that state the agent adopts.
  - If the design ties adoption to estimate precision, the PAM dial is back.

## Verdict: reject as the mechanism; keep as the named contrast and as support for own-model reading
It is the canonical contagion route. Its moderators are gains on a matched representation, and so it predicts uniform scaling across expressions, which the human mimicry data contradict. Its distinction between "response with" and "response to" the object, and its use of interdependence, point to the appraisal route without modelling it.
