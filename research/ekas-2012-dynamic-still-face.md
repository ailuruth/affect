# Ekas, Haltigan & Messinger 2012, "The Dynamic Still-Face Effect: Do Infants Decrease Bidding Over Time When Parents Are Not Responsive?" (Developmental Psychology, doi:10.1037/a0029330)

Source read: the advance-online PDF from the Messinger lab (local.psy.miami.edu/.../Dynamic_SF_2012.pdf). Read: abstract, introduction on Tronick et al. 1978, the Procedure and Behavior Coding sections, the Analytic Plan opening, and the discussion passages on Tronick 1978. Results tables and the full coding definitions for smiles and cry-faces were NOT read.

## Claims
- The still-face episode is not static. Within it, "infant gazing at the parent, smiling, and social bidding (smiling while gazing at the parent) decreased with time in the SF episode, while infant cry-face expressions increased."
- On the original: "Tronick and colleagues (1978) relied on the observation of only seven infants and did not indicate whether all infants displayed the same pattern," and "increases in frank expressions of negative affect were not a feature of Tronick and colleagues' (1978) original description."

## Evidence
- Procedure, verbatim: "Parents were asked to play with their infant without toys for 3 min (FF episode), stop playing and maintain a still face with a neutral expression for 2 min (SF episode), and then resume play for another 3 min (RE episode)." "Episodes were curtailed if infants cried steadily for 30 seconds." Infants were 6 months old.
- Gaze coding: "either at the parent's face or away", with frame-level reliability κ = .90 on 25% of videos. Smiles and cry-faces were coded with FACS.
- Episode means were compared by repeated-measures ANOVA, "typically referred to as the SF effect (Mesman et al., 2009)". Within-episode change was fitted with hierarchical linear models (logarithmic decline expected).
- Variability: "a majority, but not all, of the infants ... showed a decline in gazes at the parent, smiles, and positive social bids", and "slightly less than half" showed rising cry-faces. "Elapsed time ... only accounted for a small proportion of variance."

## License
APA journal article. Lab copy for teaching. No code.

## Runs on this Mac without a GPU?
n.a. (protocol).

## Verdict: adopt (as the operational parameters and the within-episode measure)
It supplies concrete, published settings for the still-face run in mesman-2009-still-face-meta-analysis.md:
- 3-2-3 min episodes.
- A curtailment rule (30 s of steady distress).
- Gaze coded as at or away from the partner's face.

It also adds a second published outcome: bidding should decline over the still-face, not just differ in mean.

For the Bot, the published within-episode signature is a falling rate of partner-directed positive bids (smile while gazing) across the 2 min. A human coder can score it from the Bot's rendered face. A flat or rising bid rate under a non-responsive partner fails this signature.

The finding that many infants do not show every component also sets a fair bar: the Bot should match the group pattern across sessions, not every session.
