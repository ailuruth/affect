# REACT 2025: the Third Multiple Appropriate Facial Reaction Generation Challenge (Song et al., arXiv 2505.17223, 2025)

Song, Spitale, Kong, Zhu, Luo, Palmero, Barquero, Escalera, Valstar, Daoudi, Baur, Ringeval, Howes, André, Gunes. "REACT 2025: the Third Multiple Appropriate Facial Reaction Generation Challenge." arXiv 2505.17223v1, 22 May 2025 (ACM MM 2025 challenge paper).

## What was read
- Full text of arXiv 2505.17223v1 (6 pages plus references), extracted with pdftotext.
- Table 3 (baseline results) came out of the extraction as a flat list of numbers. I rebuilt the rows by column order (FRCorr, FRDist, FRDiv, FRVar, FRRea, FRSyn) and checked them against every number quoted in the prose (PerFRDiff FRCorr 0.58, REGNN 0.54 and FRDist 155.49, online FRDist 222.69 vs 212.22, online FRCorr 0.55 vs 0.25). All prose numbers match the rebuilt rows. The FRRea column is empty ("–") for every row in the extracted text.

## Claims
- Earlier facial reaction generation treated the task as "one-to-one mapping" that tries "to accurately replicate the ground truth (GT) listener facial reactions". The authors argue it is "fundamentally a 'one-to-many mapping' task" because the same speaker behaviour elicits different reactions "depending on external and their internal contexts".
- REACT 2023 and 2024 used clips cut from NoXi, UDIVA and RECOLA, "all of which were recorded for the purposes other than the MAFRG task. Consequently, their data and labels limit the development of more advanced MAFRG systems."
- New dataset MARS: 137 dyads (23 speakers, 137 listeners), video-conference on Microsoft Teams, 23 scripted sessions per clip over five topics in a fixed order, 2856 session pairs. Audio, video, transcripts, EEG (MUSE-2), Big-Five (10-item).
- Ground truth for appropriateness: "for each speaker behaviour expressed in a specific session, we define all facial reactions expressed by different listeners under the same session to be appropriate facial reactions (i.e., ground-truth)."
- Output representation: 25 frame-level attributes (15 AUs, 8 expression probabilities, valence and arousal from EmoNet) plus rendered video. Ranking uses only FRCorr and FRRea.

## Evidence (Table 3, MARS test set; FRCorr summed over 10 samples, so GT = 10)
| Row | FRCorr ↑ | FRDist ↓ | FRDiv ↑ | FRVar ↑ | FRSyn ↓ |
|---|---|---|---|---|---|
| GT | 10 | 0.00 | 0.1876 | 0.0669 | 48.66 |
| B_Random | 0.03 | 474.68 | 0.3342 | 0.1671 | 46.64 |
| B_Mime (copy speaker) | 0.52 | 206.02 | 0.0000 | 0.0766 | 43.70 |
| B_MeanFr (training mean frame) | 0.00 | 205.65 | 0.0000 | 0.0000 | 49.00 |
| Offline Trans-VAE | 0.30 | 181.72 | 0.0076 | 0.0083 | 49.00 |
| Offline PerFRDiff | 0.58 | 217.32 | 0.1596 | 0.0862 | 48.66 |
| Offline REGNN | 0.54 | 155.49 | 0.0012 | 0.0048 | 44.81 |
| Online Trans-VAE | 0.25 | 212.22 | 0.1082 | 0.0564 | 48.20 |
| Online PerFRDiff | 0.55 | 222.69 | 0.1506 | 0.0841 | 46.56 |

- The authors' own reading: "the B_Mime setting achieved surprising FRCorr performance by simply generating the corresponding speaker facial behaviours, which can be explained by the fact that human listeners often exhibit facial behaviours that mirror those of the corresponding speakers, i.e., facial mimicry."

## Failures documented
- **Copying the speaker is a near-ceiling baseline.** B_Mime (FRCorr 0.52) beats Trans-VAE offline (0.30) and online (0.25), and is within 0.06 of the best model (PerFRDiff, 0.58). B_Mime has the best synchrony score of every row (FRSyn 43.70).
- **A frozen average face beats several models on distance.** B_MeanFr (FRDist 205.65), which never moves, is closer to real reactions than offline PerFRDiff (217.32) and both online models (212.22, 222.69).
- **Mode collapse in distribution-learning baselines.** REGNN's diversity across its 10 samples is FRDiv 0.0012 against a human spread of 0.1876 (about 1/150), and its within-clip variance is FRVar 0.0048 against 0.0669. Offline Trans-VAE: 0.0076 and 0.0083. The model with the best distance (REGNN) is the one that barely varies.
- **The appropriateness label is defined by session, not by the partner.** Any listener's reaction in the same scripted session counts as appropriate for any speaker in it. The metric then takes the best-matching one, so it cannot reward reactions specific to this partner or this relationship.
- **Emotion is an external classifier output, not a state.** Valence, arousal and the eight expression probabilities in the target vector are EmoNet predictions on the listener's face.
- **Short, scripted, one-off context.** Sessions average 305-339 s, topics follow a fixed order, and each listener meets one speaker once. Nothing in the task asks a model to carry state across sessions.
