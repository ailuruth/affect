# REACT 2026: Personalised MAFRG and Appropriate EEG Reaction Prediction (Song et al., arXiv 2606.07935, 2026)

Song, Spitale, Wu, Kong, Luo, Palmero, Barquero, Escalera, Valstar, Daoudi, Ringeval, Howes, André, Gunes. "REACT 2026: The Fourth Multiple Appropriate Facial Reaction Generation Challenge: Personalised MAFRG and Appropriate EEG Reaction Prediction." arXiv 2606.07935 (ACM MM 2026 challenge paper).

## What was read
- Full text (6 pages plus references), extracted with pdftotext. In Table 2 the offline personalised row (S-PerReactor) has check marks but no numbers in the extracted text, and the generic offline rows have no FRRea value. I report only the numbers that came out. For the three online personalised PerFRDiff rows, the extraction does not show which check marks (listener history, personality, both) go with which row, so I report them as three variants without labels.

## Claims
- Existing MAFRG solutions "generate general AFRs without considering personalised aspect, i.e., human listeners of different internal disposition (e.g., personality) can express varied AFRs in response to the same speaker behaviour", and "they focus on generic FRG modelling but overlook the role of individual differences."
- Previous datasets "rarely integrate neurophysiological signals, limiting the exploration of internal–external alignment between latent user states and observable facial reactions."
- New personalised tasks: generate reactions "similar to real AFRs expressed by the target listener", conditioned on the listener's historical facial behaviour (LHFB) and/or Big-Five traits. Same MARS data as REACT 2025; each speaker is paired with 2 to 8 listeners.
- EEG head: a 2-layer MLP predicting MUSE-2 EEG channels from the speaker's behaviour.

## Evidence (Table 2, MARS test set; FRCorr summed over 10 samples)
| Row | FRCorr ↑ | FRDist ↓ | FRDiv ↑ | FRVar ↑ | FRSyn ↓ |
|---|---|---|---|---|---|
| GT | 10 | 0.00 | 0.1926 | 0.0623 | 48.80 |
| B_Random | 0.0360 | 432.14 | 0.3343 | 0.1671 | 47.62 |
| B_Mime | 0.5454 | 180.68 | 0.0000 | 0.0756 | 45.79 |
| B_MeanFr | 0.0000 | 163.61 | 0.0000 | 0.0000 | 49.00 |
| Offline Trans-VAE | 0.2582 | 157.57 | 0.0078 | 0.0069 | 49.00 |
| Offline REGNN | 0.4770 | 130.30 | 0.0014 | 0.0040 | 46.22 |
| Online Trans-VAE | 0.3483 | 182.46 | 0.0893 | 0.0500 | 49.00 |
| Online PerFRDiff (generic) | 0.5680 | 199.56 | 0.1503 | 0.0867 | 47.65 |
| Online PerFRDiff, personalised variant 1 | 0.5497 | 204.36 | 0.1515 | 0.0872 | 47.88 |
| Online PerFRDiff, personalised variant 2 | 0.5475 | 196.37 | 0.1452 | 0.0832 | 47.40 |
| Online PerFRDiff, personalised variant 3 | 0.5453 | 192.54 | 0.1445 | 0.0828 | 47.69 |

- EEG (Table 3): EEGCorr 0.0671 to 0.1719 across baselines; EEGDiv 0.0000 to 0.0052. The authors call the predictions "weakly associated" with the ground truth.
- The authors on mimicry: "the strong results of B_Mime suggest that human listeners may frequently exhibit facial behaviours that mirror those of the corresponding speakers, i.e., facial mimicry."
- The authors on personalisation: "personalised models do not necessarily achieve better appropriateness performance ... than their generic variants". They explain this by the metric: a personalised output is compared only with the target listener's reaction, a generic one with all listeners'.

## Failures documented
- **Copy-the-speaker still beats or ties learned models.** B_Mime FRCorr 0.5454 beats offline REGNN (0.4770) and both Trans-VAEs, and equals the personalised PerFRDiff variants (0.5453 to 0.5497). B_Mime again has the best synchrony of every row (FRSyn 45.79).
- **A never-moving mean face beats both online models on distance.** B_MeanFr FRDist 163.61 against online Trans-VAE 182.46 and online PerFRDiff 199.56, and against all three personalised variants (192.54 to 204.36).
- **Personalisation adds nothing measurable.** All three personalised variants score below the generic model on FRCorr (0.5453-0.5497 vs 0.5680). Conditioning on the listener's own history or personality did not produce a reaction that matches that listener better than copying the speaker does.
- **Mode collapse persists.** Offline REGNN FRDiv 0.0014 and Trans-VAE 0.0078 against GT 0.1926. The REGNN EEG head has EEGDiv 0.0000.
- **"Internal state" enters as a static trait label.** Personality is a 10-item questionnaire score, and listener history is a 3DMM time series. Neither is a state that changes inside the interaction.
