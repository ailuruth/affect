# Harms & Biocca 2004, "Internal Consistency and Reliability of the Networked Minds Social Presence Measure" (PRESENCE 2004, 7th International Workshop on Presence, Valencia, pp. 246-251)

Source read: the full 6-page proceedings PDF from the ISPR proceedings archive (matthewlombard.com/ISPR/Proceedings/2004), including Table 3 with all retained items. Tables 1 and 2 (the ANOVA results) were referenced but not printed in the text I extracted. The Harms 2004 dissertation cited for later results was not read.

## Claims
- Six subscales, 36 items. Each item comes as a matched pair: self-to-other and other-to-self ("each of the 50 items were reflected to measure the observer's perception of the other's response").
- Format: "a Likert scale format would be used to measure each item" and "All scale means are on a scale from one to seven." The paper does not give the anchor labels or a reverse-scoring rule, though several items are negatively keyed (e.g. 7, 8, 11, 12, 17, 18, 21, 22).
- Items (verbatim from Table 3; "(my partner)" is the slot for the other's name):
  - Co-presence (α = .84): 1 I noticed (my partner). 2 (My partner) noticed me. 3 (My partner's) presence was obvious to me. 4 My presence was obvious to (my partner). 5 (My partner) caught my attention. 6 I caught (my partner's) attention.
  - Attentional Allocation (α = .81): 7 I was easily distracted from (my partner) when other things were going on. 8 (My partner) was easily distracted from me when other things were going on. 9 I remained focused on (my partner) throughout our interaction. 10 (My partner) remained focused on me throughout our interaction. 11 (My partner) did not receive my full attention. 12 I did not receive (my partner's) full attention.
  - Perceived Message Understanding (α = .87): 13 My thoughts were clear to (my partner). 14 (My partner's) thoughts were clear to me. 15 It was easy to understand (my partner). 16 (My partner) found it easy to understand me. 17 Understanding (my partner) was difficult. 18 (My partner) had difficulty understanding me.
  - Perceived Affective Understanding (α = .86): 19 I could tell how (my partner) felt. 20 (My partner) could tell how I felt. 21 (My partner's) emotions were not clear to me. 22 My emotions were not clear to (my partner). 23 I could describe (my partner's) feelings accurately. 24 (My partner) could describe my feelings accurately.
  - Perceived Emotional Interdependence (α = .85): 25 I was sometimes influenced by (my partner's) moods. 26 (My partner) was sometimes influenced by my moods. 27 (My partner's) feelings influenced the mood of our interaction. 28 My feelings influenced the mood of our interaction. 29 (My partner's) attitudes influenced how I felt. 30 My attitudes influenced how (my partner) felt.
  - Perceived Behavioral Interdependence (α = .82): 31 My behavior was often in direct response to (my partner's) behavior. 32 The behavior of (my partner) was often in direct response to my behavior. 33 I reciprocated (my partner's) actions. 34 (My partner) reciprocated my actions. 35 (My partner's) behavior was closely tied to my behavior. 36 My behavior was closely tied to (my partner's) behavior.

## Evidence
- N = 240 students, between-subjects: face-to-face, text (AOL IM), video (NetMeeting); a 5-minute get-to-know chat with a confederate.
- CFA on a 100-item pool; "64 items were deleted in total"; "Alpha reliability for all scales ranged at satisfactory levels between .81 and .87."
- Criterion validity was only partly met. Face-to-face beat mediated on four of six subscales; "perceived message understanding and perceived emotional interdependence yield null results".
- Failure: "the measure failed in the criterion-related validity test involving the ability of the measure to distinguish between two levels of mediated interaction". Text scored higher than video on message and affective understanding, "contrary to what would be predicted from theory ... This suggests that the measure may not be sensitive enough to detect differences in social presence across different media".
- Stated limitations: the media/sensory confound, and that "the experiment only tested a narrow range of relationships and tasks".
- No test-retest reliability is reported, despite the title.

## License
Workshop proceedings, posted openly by ISPR; no license stated. Items may be reproduced for research with citation (no stated restriction).

## Runs on this Mac without a GPU?
n.a.

## Verdict: adopt (Perceived Affective Understanding and Perceived Emotional Interdependence as the primary subscales), with the sensitivity caveat
These are the only accepted self-report items here that ask the user directly whether they could read the other's feelings ("I could tell how (my partner) felt") and whether moods passed between them. That is exactly what an affect-bearing face and voice claims to change. Use the 36-item 2004 version as printed, 7-point, subscale means, negatively keyed items reversed, alpha reported. Treat the missing anchors and reversal rule as a documented gap, not something to invent quietly. The scale was validated on human partners. Using it with an artificial agent is an adaptation the authors anticipate in their definition ("human, animate, or artificial being", Biocca et al. 2001) but never validated. Our ablation is a richer-versus-poorer mediated contrast, which is exactly the contrast this paper says the measure failed to detect. A null result is therefore weak evidence, and a pre-registered power analysis is mandatory. Not usable at n=1: the reliability is between-subjects internal consistency only.
