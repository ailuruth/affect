# Korb, Goldman, Davidson & Niedenthal 2019, "Increased Medial Prefrontal Cortex and Decreased Zygomaticus Activation in Response to Disliked Smiles Suggest Top-Down Inhibition of Facial Mimicry" (Frontiers in Psychology 10:1715, doi 10.3389/fpsyg.2019.01715)

Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC6677088/ (open access).

## What was read
The full PMC text: introduction, methods (participants, stimuli, conditioning, rating, oddball task, EMG, fMRI, ROI and PPI), results, discussion, table 1. Supplementary whole-brain tables were not opened. Sims et al. 2012 (*Psychophysiology*, the paradigm this replicates) was not reachable; it is used only as this paper reports it.

## What it says
- **Conditioning (within one session).** 35 women analysed. A card-guessing game of 120 trials with a task-irrelevant neutral face beside the cards: one identity came with a win (+50 cents) on 27 of 30 trials, one with a loss (−40 cents) on 27 of 30, two with equal wins, losses and draws (30 each). Outcomes were pre-programmed whatever the participant chose. By the stated timings a trial is about 6–7 s plus the response, so the conditioning took on the order of 15 min (my estimate).
- **Liking.** Loss-associated faces were liked less than win and no-change faces (F(2,80) = 28.5, η²p = .45); win and no-change did not differ. Rated intensity did not change.
- **Test (in the scanner, after conditioning).** 3 runs × 10.4 min; 4-s dynamic happy and angry clips of the win and loss faces (about 34 usable trials per participant and cell). EMG over the zygomaticus; the corrugator was too noisy to analyse.
  - Emotion × Reward × Time F(3,114) = 3.2, p = .036.
  - Happy clips: more zygomaticus to the win face than the loss face (113.2 vs 108.1 % of baseline; F(1,38) = 7.8, η²p = .17), significant in seconds 1, 2 and 3 (t = 3.3, 2.8, 2.2) and not in second 4.
  - Angry clips: no reliable win/loss difference on the zygomaticus.
  - The authors note their η²p (.16) exceeds Sims et al. 2012's (.09) on the same paradigm.
- **Interpretation.** The authors read the effect as inhibition of mimicry when the expression's valence is incongruent with the face's learned association (happy + loss), not as reward boosting mimicry; the paradigm has no neutral-association test face to decide between the two. mPFC ROI: Emotion × Reward interaction F(1,34) = 4.7, p = .036 (incongruent > congruent); PPI connectivity of mPFC with insula, premotor cortex and IFG on incongruent trials, at uncorrected thresholds only.

## What matters for this engine
- **Partner-specific smile gating learned within one session, from about 30 pairings per partner.** The learned association (this face goes with my losses) reduces smile return to that face from the first second of its smile, and lasts through 30 min of test without reinforcement. The effect is per expression: it is shown on the smile, not on the zygomaticus response to anger (the corrugator could not be read).
- **The learning signal is approval-closed in this experiment.** The money never depended on the observer's face, or even on the observer's choice; the face predicted the observer's own outcomes. In pass 7's terms, no path runs from the observer's expression to the outcome, so the learning cannot steer which expressions the observer makes. What is learned is a value of the partner (a relation), not a value of the partner's expression.
- **Mapped to the build core.** The nearest part is ω's person-valence rule: relief events attributed to him (ρ_rel) and the session's hurt (h̄) set a signed relation per group, which scales the held cone's diagonal. Its direction matches (fewer good outcomes with him → less smile copy). Two gaps:
  - **speed:** ω moves 1/60 of the way per session; humans move in about 30 pairings within one session;
  - **place:** the cone's input carries DC within a session, so its gain is latched per session (Lemma S). A within-session relation can act only on zero-DC paths: the echo gate g (on a 4-s high-passed input) or the appraisal display (band-passed).
- **In conversation the path exists.** Unlike the card game, the operator's words and presence can depend on the agent's display, so a relation learned from relief attributed to him is open to his words (Proposition 1(b)), though closed to his face as long as ρ_rel and h̄ read only T events.

## Limits
Women only; one win and one loss identity per participant; corrugator lost; EMG inside the MR scanner; no learning curve (conditioning effects measured only after the block, pooled over runs); fMRI at uncorrected thresholds.

## Verdict: adopt (as the clearest open within-session evidence that a partner's predicted outcome for the self gates smile return, and that the signal is approval-closed)
