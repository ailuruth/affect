# Heart–brain interactions shape somatosensory perception and evoked potentials (Al, Iliopoulos, Forschack, Nierhaus, Grund, Motyka, Gaebler, Nikulin & Villringer)

Citation: E. Al, F. Iliopoulos, N. Forschack, T. Nierhaus, M. Grund, P. Motyka, M. Gaebler, V. V. Nikulin, A. Villringer. "Heart–brain interactions shape somatosensory perception and evoked potentials." *PNAS* 117(19):10575–10584, 2020. doi:10.1073/pnas.1915629117. PMC7229654.

Source read: the PMC full text, HTML text-extracted. Read in full: abstract, Results, Discussion, Materials and Methods, figure captions. **Not read:** the SI Appendix (GLMM tables, source reconstruction details, Figs. S1–S8).

## The finding
- **Task.** 37 participants, weak electrical pulses to the left index or middle finger at ~50 % detection threshold; yes/no detection then two-choice localisation on every trial; 960 trials each (160 catch). EEG (62 channels) and ECG. Overall d′ 1.57 ± 0.57, criterion c 0.76 ± 0.32.
- **Two heartbeat effects, dissociated by signal detection theory.**
  - **Cardiac phase changes sensitivity, not bias.** Detection was higher in diastole than systole (52.41 % vs 49.53 %, t₃₆ = −3.95, P = 3·10⁻⁴; 27 of 37 participants). d′ was higher in diastole (1.59 vs 1.48, P = 0.008); criterion did not differ (0.75 vs 0.73, P = 0.48); false alarms did not differ. Detection and localisation were lowest 200–400 ms after the R-peak, when the pulse wave reaches the finger. Only the late SEP (P300, 268–468 ms) was reduced in systole; early components were not.
  - **The effect scales with predictability of one's own heart.** Participants with lower heart-rate variability had a larger systole–diastole detection difference (r = −0.36, P = 0.03). The authors cannot say whether this is better temporal prediction of the next beat or vagal tone.
  - **HEP amplitude changes bias, not sensitivity.** Pre-stimulus heartbeat-evoked potential (296–400 ms after the R-peak, centro-parietal) was more positive before misses than hits (Monte Carlo P = 0.004). Across HEP tertiles, criterion rose with HEP (F₂,₃₆ = 10.30, P = 1·10⁻⁴) while d′ did not change (P = 0.84). High HEP was followed by smaller SEPs from 32 ms on, including P50 in primary somatosensory cortex, and P50 differences also in right anterior insula, PCC and LPFC.
  - **Both are additive to sensorimotor alpha.** Alpha also shifted criterion; neither heart effect interacted with alpha (cardiac phase × alpha F = 0.34, P = 0.85; HEP × alpha F = 0.75, P = 0.56).
- **Interpretation offered (not tested).** Phase: the brain predicts and attenuates pulse-synchronous afferent activity, and a weak external stimulus in the same window is treated as "internal noise", lowering d′. HEP: spontaneous shifts of attention between interoception and exteroception, lowering baseline excitability and so raising the criterion. The authors say this second reading "is not definitely proven".
- **Caveat on generality.** Park et al. (visual, MEG) found the opposite sign for HEP and detection; the authors attribute it to modality differences.

## The mathematical object
Two dissociable operators of the body on the perception of the world, in signal-detection terms:
- a **body-phase-indexed noise model**: the observer's own predicted self-generated input sets a time-varying noise floor, so the effective discrimination d′(φ) depends on the phase φ of its own cycle. It acts multiplicatively on discriminability, is strongest when one's own rhythm is most regular, and leaves early processing intact;
- a **slow allocation variable** (intero- vs exteroceptive) that shifts the decision threshold additively, reaches early sensory gain, and is independent of alpha.

So "how well I can tell your signal from my own noise" and "how ready I am to report anything outside me" are separate quantities with separate physiological markers.

## What it means for the design
1. **The other's signal is read against the agent's own predicted body noise.** A copy-blind input that ignores simultaneous movement was the failed lesson of report 8. This is different: what is discounted is the part of the input the agent's own body cycle predicts, by phase, and the discount is on discriminability, not on magnitude. That is the negative-image object (kennedy-sawtell-2014) on a periodic basis, which the index already has.
2. **Two channels, not one gain.** Any design that lets the partner act through "attention" should say whether it moves d′ or the criterion. They have different ablation signatures (late vs early evoked response; sensitivity vs bias).
3. **Predictability of one's own rhythm sets how strongly self-noise is discounted.** A temperament-like trait (heart-rate variability) would set how much partner input falls in "my own noise" windows. That is a slow variable selecting a fast gate, derived from data rather than set.

## Verdict
- **adopt (as a measured dissociation: phase → sensitivity, body-evoked response → criterion).** Not a mechanism; small effects (≈3 percentage points). The predictive-coding account is the authors' interpretation, not demonstrated.
