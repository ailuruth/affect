# Ainsworth, Blehar, Waters & Wall 1978, *Patterns of Attachment: A Psychological Study of the Strange Situation* (Erlbaum): procedure and scoring

Source read. The book itself was NOT read: the Internet Archive copies are lending-only and the publisher text is not open. What I read instead:
- Everett Waters (2002), "The Ainsworth Strange Situation", 18 pp. (psychology.psy.sunysb.edu/attachment/measures/content/ss_scoring.pdf), read in full. Waters is a co-author of the book. The PDF states: "The scoring material here is abstracted from Ainsworth, Blehar, Waters & Wall (1978)... The commentary and the similarity matrix are my own." It reproduces four of the six interactive scales with all anchors, the A/B/C group and subgroup criteria, and the book's Table 33 (subgroup means).
- A one-page episode table, "The Episode of the Strange Situation", attributed to "Campos et al., 1983", from a University of Utah course handout (content.csbs.utah.edu/~isabella/1500 online/strangesituation.table.pdf). This is a secondary reproduction of the episode list, not the book's own table.
- Ainsworth 1979, "Infant–mother attachment", American Psychologist 34:932-937, first page only.
- The Protocol and Expert-ratings sections of Prince et al. 2021, Infant Behavior and Development 63:101565.

Not read: the book's text on the **search** and **distance-interaction** scales. Waters does not reproduce them, so their anchors are unverified here.

## Claims
Episodes, from the Campos et al. 1983 table, verbatim:

| # | Present | Duration | Action |
|---|---|---|---|
| 1 | Mother, baby, and observer | 30 seconds | "Observer introduces mother and baby to experimental room, then leaves." |
| 2 | Mother and baby | 3 minutes | "Mother is non-participant while baby explores; if necessary, play is stimulated after 2 minutes." |
| 3 | Stranger, mother, and baby | 3 minutes | "Minute 1: stranger silent. Minute 2: stranger converses with mother. Minute 3: stranger approaches baby. After 3 minutes mother leaves unobtrusively." |
| 4 | Stranger and baby | 3 minutes or less (a) | "First separation episode." |
| 5 | Mother and baby | 3 minutes or more (b) | "First reunion episode." |
| 6 | Baby alone | 3 minutes or less (a) | "Second separation episode." |
| 7 | Stranger and baby | 3 minutes or less (a) | "Continuation of second separation." |
| 8 | Mother and baby | 3 minutes | "Second reunion episode." |

(a) "Episode is curtailed if the baby is unduly distressed." (b) "Episode is prolonged if more time is required for the baby to become involved in play."

Running rules (Waters):
- "the length of separations and reunions MUST be adjusted adaptively. If after a full minute of crying it is obvious that he will not calm down on his own, you should move on."
- "scoring absolutely should not include behavior beyond the end of Episode 8."
- Prince et al. 2021 apply the same curtailment: "e.g., 60 s of crying; Waters, 2002".

## Evidence
Scoring basis, verbatim from Waters:
- "Strange Situation classifications are based primarily on 'interactive behaviors' toward the mother in the two reunion episodes (Ep. 5 & Ep. 8)."
- "four 7-point scales: Proximity seeking, Contact maintaining, Avoidance of proximity and contact, and Resistance to contact and comforting."
- Crying in each episode is timed. Scoring must use video: "It is not possible to reliably score the procedure by observing it as it occurs."

Scale anchors (top and bottom, verbatim):
- **Proximity and contact seeking**:
  - 7: "Very Active Effort and Initiative in Achieving Physical Contact... Contact is more than momentary; the baby does not turn away to other things within 15 seconds." In Episodes 5, 7 and 8 a 7 is barred "if the initial approach ... is delayed substantially (i.e., more than 30 seconds)".
  - 1: "No Effort to Achieve Physical Contact or Proximity", including "The baby merely looks, or smiles, or interacts across a distance".
- **Contact maintaining**:
  - 7: in "contact lasting over 2 minutes, shows at least two instances of active resistance to release".
  - 1: "Either No Physical Contact or No Effort to Maintain It."
- **Resistance**:
  - Mood "angry-pouting, petulance, cranky fussing".
  - Behaviors "pushing away, throwing away, dropping, batting away, hitting, kicking, squirming to be put down".
  - 7 needs "two or more" of repeated hitting, strong resistance to being held, a full temper tantrum, and similar.
- **Avoidance**, relevant behaviors: "increasing distance ... turning the back on the person; turning the head away; averting the gaze; avoidance of meeting the person's eyes; hiding the face; or simply ignoring the person."
  - Of mother, 7: "The baby does not greet the mother upon her return in a reunion episode (episode 5 or 8)-neither with a smile nor with a protest. He pays little or no attention to her for an extended period despite the mother's efforts".
  - Scores 5 and 4 are keyed to ignoring her "for about 30 seconds" and "for a time (15 to 30 seconds)".

Classification, verbatim:
- **Secure (B)**: "The baby wants either proximity and contact with his mother or interaction with her, and he actively seeks it, especially in the reunion episodes"; "Little or no tendency to resist ... Little or no tendency to avoid his mother in the reunion episodes"; distress, if present, "is clearly related to his mother's absence and not merely to being alone."
- **Avoidant (A)**: "Conspicuous avoidance of proximity to or interaction with the mother in the reunion episodes"; "Either the baby is not distressed during separation, or the distress seems to be due to being left alone rather than to his mother's absence."
- **Resistant (C)**: "conspicuous contact- and interaction-resisting behavior, perhaps especially in Episode 8"; "also shows moderate-to-strong seeking of proximity and contact ... so that he gives the impression of being ambivalent".
- Subgroups A1, A2, B1-B4, C1 and C2 are defined. Classification is a holistic judgment, with no numeric cut-offs: "develop a hypothesis during the first reunion and look for converging evidence within and across episodes", and keep "can't classify" open.
- **Disorganized (D)**: "not included in Ainsworth's original scoring system"; "usually < 5%" in normal samples; see Main & Solomon 1990 (duschinsky-2015-disorganized-attachment-history.md).
- Table 33 (book, reproduced) gives subgroup means on each scale per episode. For example, Episode 8 proximity seeking is B3 4.98, A1 1.42 and C1 4.00; Episode 8 avoidance is A1 5.92 and B3 1.28.

## License
The book is © Erlbaum (now Psychology Press). Waters' abstraction is posted for research use. Scoring reliability in practice requires a trained, certified coder (Waters: "2-3 day training clinics"; Prince et al. used a coder who "passed the Minnesota attachment reliability test").

## Runs on this Mac without a GPU?
n.a. (protocol).

## Verdict: reject as an instrument for this Bot (used as published); watch the avoidance scale and the B/A/C logic as design references
The scales are defined on a crawling or walking 12-18-month-old in a room with a stranger:
- Proximity seeking scores "creeping, crawling, or walking" and "clambering up".
- Contact maintaining scores clinging while held.
- Resistance scores "squirming to be put down" and hitting.

A screen-bound face-and-voice Bot can do none of these, so the Bot would score 1 on three of four scales by construction. Rewriting the anchors for a screen ("proximity = sends a message") changes the items and the scoring, which breaks the rule of using instruments as published. The classification also has no algorithmic cut-offs: it is a trained coder's holistic judgment, normed on human infants.

What survives without modification:
- The episode logic: a familiar partner present, absent and back, with a stranger condition. Reunion behavior, not separation distress, carries the diagnosis.
- The avoidance scale's observable items ("does not greet", "turning the head away", "averting the gaze", ignoring for 15-30 s) can be coded on a rendered face. Using one scale out of a classification system is still an adaptation and must be reported as one.

Failure, if a future embodied version were scored as published: reunion behavior indistinguishable from separation-episode behavior, or from behavior toward a stranger. The B criterion requires the partner to be "clearly" preferred over the stranger.

Precedents with artificial agents (htet-2024-coupled-oscillator-attachment-robots.md, gagliardi-2022-attachment-control-system.md, mongile-2022-icub-still-face.md) did not apply these scales or classification rules; see those notes.
