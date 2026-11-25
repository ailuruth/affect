# Bartneck, Kulić, Croft & Zoghbi 2009, "Measurement Instruments for the Anthropomorphism, Animacy, Likeability, Perceived Intelligence, and Perceived Safety of Robots" (Int J Social Robotics 1:71-81, doi 10.1007/s12369-008-0001-3)

Source read: the full 13-page author PDF from bartneck.de (identical text to the Springer version, open access), all sections, plus the Appendix page as an image (the item table is an image, not text). Nothing skipped.

## Claims
- Five stand-alone questionnaires, "distilled into five consistent questionnaires using semantic differential scales". The series is named "Godspeed".
- Format: Appendix "shows the application of the five Godspeed questionnaires using 5-point scales". Each scale is headed "Please rate your impression of the robot on these scales:" except Perceived Safety, headed "Please rate your emotional state on these scales:". Anchors 1 to 5, left anchor = 1.
- Items, verbatim from the Appendix (left anchor / right anchor):
  - I Anthropomorphism (5): Fake/Natural, Machinelike/Humanlike, Unconscious/Conscious, Artificial/Lifelike, Moving rigidly/Moving elegantly.
  - II Animacy (6): Dead/Alive, Stagnant/Lively, Mechanical/Organic, Artificial/Lifelike, Inert/Interactive, Apathetic/Responsive.
  - III Likeability (5): Dislike/Like, Unfriendly/Friendly, Unkind/Kind, Unpleasant/Pleasant, Awful/Nice.
  - IV Perceived Intelligence (5): Incompetent/Competent, Ignorant/Knowledgeable, Irresponsible/Responsible, Unintelligent/Intelligent, Foolish/Sensible.
  - V Perceived Safety (3): Anxious/Relaxed, Agitated/Calm, Quiescent/Surprised.
  - 24 item rows in total; Artificial/Lifelike appears in both I and II.
- Scoring: "Before calculating the mean scores for anthropomorphism, animacy, likeability, or perceived intelligence it is good practice to perform a reliability test and report the resulting Cronbach's Alpha." Scale score = mean of items. The paper does not say how to score Quiescent/Surprised, whose positive pole is on the left, unlike the other two safety items (in Table 1 it correlates −0.530 with Anxious/Relaxed).
- Administration: "When one of these questionnaires is used by itself in a study it would be useful to mask the questionnaire's intention by adding dummy items, such as optimistic/pessimistic. If multiple questionnaires are used then the items should be mixed so as to mask the intention."
- Japanese translation made "using the back translation method" is printed alongside the English.

## Evidence
Reliabilities (Cronbach's alpha), all from small earlier studies; Nunnally's 0.7 is the stated threshold:
- Anthropomorphism: 0.878 [ref 21]; 0.929 human, 0.923 android, 0.856 masked android [ref 22].
- Animacy: "One study used this new questionnaire [36] and reported a Cronbach's Alpha of 0.702".
- Likeability: 0.865 [21]; 0.923 / 0.878 / 0.842 [22].
- Perceived Intelligence: 0.75 [22], 0.769 [51], 0.763 [36] (plus 0.92 for the four-item Likert original by Parise et al.).
- Perceived Safety: no alpha for the semantic-differential version. Reported 0.91 is for the earlier "5 point Likert" affective-state questionnaire. The new version was run on "16 subjects" against robot speed (correlations and a 3-factor ANOVA), and validity "may be assumed".
- No test-retest reliability: "none of the studies that we have access to have had enough participants to allow for a meaningful test-retest analysis."
- Validity: only content validity is argued; construct and criterion validity are said to be not yet achievable.

Cautions stated by the authors:
- "the sensitivity of the Godspeed questionnaire series is not completely known. There may very well be a small difference in perception between two almost identical robots, but this difference might be too small to be picked up by the questionnaire with a small number of participants. ... we recommend increasing the number of participants, based on a power analysis."
- "The resulting values of the measurements should therefore be interpreted not as absolute values, but rather as a tool for comparison. Robot developers can, for example, use the questionnaires to compare different configurations of a robot."
- Overlap: "An additional correlation analysis is therefore recommended when both questionnaires are being administered in the same study."
- Perception drifts over time: "if the experiment would be repeated in twenty years, it would yield different results."
- Translations: "Only native speakers can understand the true meanings of the adjectives in their language."

## License
Article: Creative Commons Attribution Noncommercial License ("permits any noncommercial use, distribution, and reproduction in any medium, provided the original author(s) and source are credited"). The items are free to use.

## Runs on this Mac without a GPU?
n.a. (questionnaire).

## Verdict: adopt (Likeability, Perceived Intelligence, and Anthropomorphism or Animacy, but not both; Perceived Safety only with caveats)
This is the field's default instrument for "how does the agent come across". It is built for the comparison we need ("compare different configurations of a robot"): affect on versus affect ablated, with the agent unchanged otherwise. Use it as published: 5-point semantic differentials, published anchors, mean per scale, alpha reported per condition, items mixed with dummy items. For a within-subject ablation, a failure is the full-affect agent scoring no higher than the ablated one on the target scale at a pre-registered, power-analysed sample size. The scales are not designed for n=1. Alpha needs several respondents. Test-retest reliability was never established. The authors themselves warn that small differences need more participants. One person's ratings are an anecdote, not a Godspeed result. Perceived Safety rates the participant's own emotional state and has the weakest reliability evidence (see bartneck-2023-godspeed-translations-usage.md). It is still the only Godspeed scale that speaks to the human-side harm question.
