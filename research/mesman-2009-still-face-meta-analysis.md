# Mesman, van IJzendoorn & Bakermans-Kranenburg 2009, "The many faces of the Still-Face Paradigm: A review and meta-analysis" (Developmental Review 29:120-162, doi:10.1016/j.dr.2009.02.001)

Source read: the authors' accepted "article in press" PDF (29 pages), hosted by the Messinger lab, University of Miami (local.psy.miami.edu/.../Mesman_vanIJzendoornetalSFMeta2009.pdf). Read in full: introduction, the procedure description, the meta-analytic method (selection, moderators, Table 2 coding scheme), the results text for all three episode comparisons, Tables 3-5 headline rows, the publication-bias paragraph and the attachment meta-analysis. The narrative-review sections were skimmed. The PDF text lost minus signs, so signs below come from the prose, not the tables.

The original paper, Tronick, Als, Adamson, Wise & Brazelton 1978 (J Am Acad Child Psychiatry 17:1-13), was NOT read: it is paywalled (Elsevier and jaacap.org return 403; Semantic Scholar lists it as closed; PubMed has no abstract). Everything said here about the 1978 paper is Mesman's account of it.

## Claims
- Standard procedure: "a three-step face-to-face interaction with an adult: (1) a baseline normal interaction episode, (2) the 'still-face' episode in which the adult becomes unresponsive and maintains a neutral facial expression, and (3) a reunion in which the adult resumes normal interaction."
- The 1978 original differs: "the still-face procedure consisted of only two episodes: normal interaction and the still-face episode, separated by an interval of 30 s during which mother would turn away from the infant. The two episodes were presented in counterbalanced order."
- Tronick's explanation, as quoted: the adult "looks at the infant, but is completely unresponsive", "communicating Hello and Goodbye simultaneously" (1978, p. 11).
- Hypotheses tested (verbatim): "1. Infant gaze and positive affect decrease from baseline to the still-face episode, while negative affect increases." "2. ... increase from the still-face episode to the reunion, while negative affect decreases." "3. Infant gaze and positive affect are higher and negative affect lower in the baseline episode than during the reunion" (carry-over).

## Evidence
Inclusion rules for the meta-analysis (the closest thing to a published "as used" protocol):
- Baseline then still-face, "either immediately or after a short interval"; no toys; infant not on a lap; "The still-face episode had to be conducted by one adult posing with a neutral expression while looking at the infant and without touching the infant"; lab, not home.
- Outcomes (Table 2): gaze "At mother's face, or face and body (not body only)"; positive affect "Smiling, joy, positive vocalizations"; negative affect "Crying, fussing, anger, sadness, frowning, distress, grimacing, protesting"; neutral "Not positive and not negative".
- Scoring unit: "the average duration or percent of time of the behaviors in each episode (rather than percent of children showing the behavior)". Effect sizes are Cohen's d, random-effects where heterogeneous. 39 studies.

Effects (verbatim from results text):
- Still-face effect (baseline to still-face): "a significant decrease in gaze (d = 0.72, 95% CI = 0.55–0.89) and positive affect (d = 0.93, 95% CI = 0.78–1.08), and significant increases in negative affect (d = 0.52, 95% CI = 0.39–0.65) and neutral affect (d = 0.42, 95% CI = 0.10–0.74)." Table 3: gaze k = 33, n = 1070; positive affect k = 35, n = 1259; negative affect k = 19, n = 1019.
- Recovery (still-face to reunion): "a significant increase in gaze (d = 0.71, 95% CI = 0.51–0.91) and positive affect (d = 0.75, 95% CI = 0.62–0.87)" but "we failed to find a significant decrease in negative affect (d = 0.04 ...), suggesting the absence of 'recovery' regarding this behavior."
- Carry-over (baseline to reunion): "a significant decrease in positive affect (d = 0.20, 95% CI = 0.11–0.29), and a significant increase in negative affect (d = 0.49, 95% CI = 0.42–0.56), but no differences between baseline and reunion for gaze (d = 0.02 ...)".
- Moderators: gaze drop stronger at 6+ months (d = 0.94) than at 0-3 months (d = 0.45); positive-affect drop stronger with a parent (d = 1.01) than a stranger (d = 0.57). Episode length and intervals did not moderate the main effect ("regardless of most procedural variations, such as the length of the SFP episodes").
- Publication bias: trim-and-fill lowers the gaze drop to d = 0.56 and the positive-affect drop to d = 0.82; all stay significant.
- Attachment link: infants later secure showed more positive affect (d = 0.23) and less negative affect (d = 0.24) during the still-face; the positive-affect link loses significance after trim-and-fill (d = 0.19).

## License
Elsevier journal article, all rights reserved; the lab copy is an author preprint. The procedure itself is not licensed; anyone can run it.

## Runs on this Mac without a GPU?
n.a. (protocol).

## Verdict: adopt (as the still-face protocol and its benchmark effects)
This is the accepted statement of what the still-face effect is and how large it is, and its outcome definitions are observable behaviors that a human rater codes. Nothing in it requires the agent to label its own inputs.

How to use it on the Bot without changing the instrument:
- The user (or a trained confederate) plays the adult: 2 min normal face-to-face exchange, 2 min still-face (looking at the camera, neutral face, silent, no reply), 2 min reunion. No toys, no touch, one adult.
- The Bot needs no emotion label to "see" a still face. Its input is blendshapes and prosody, and a still face is just the absence of contingent movement and speech while the face is present.
- Human coders, blind to the hypothesis, code the Bot's rendered face and voice per second with Mesman's four categories (gaze at partner; positive; negative; neutral). Score percent of time per episode, as published.
- Report the same three contrasts as d with 95% CI across sessions.

What counts as failure:
- No drop in positive expression or partner-directed gaze from play to still-face, and no rise in negative expression. Human reference: d = 0.93, 0.72 and 0.52.
- Full, instant recovery in the reunion. Infants recover positive affect and gaze but keep the negative-affect carry-over (baseline to reunion d = 0.49). A Bot that snaps back to baseline behaves unlike the reference.
- The effect survives ablation of the internal state. Then it is a scripted reflex to "partner stopped moving", not state-driven.

Caveats:
- Effect sizes are computed across infants, so for the Bot "n" is sessions or seeds. That changes what d means, and this must be stated.
- The two-episode, counterbalanced 1978 design is not what is in use. The three-step version is the standard.
- The Bot is not an infant. A match shows the Bot reproduces the infant pattern, not that it has infant affect.
