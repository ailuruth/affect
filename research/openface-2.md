# OpenFace 2.0 (Baltrušaitis, Zadeh, Lim & Morency, IEEE FG 2018, "OpenFace 2.0: Facial Behavior Analysis Toolkit")

Source read: full paper (NSF PAR author copy, par.nsf.gov/servlets/purl/10099458); github.com/TadasBaltrusaitis/OpenFace OpenFace-license.txt, wiki pages "Action-Units" and "Mac-installation". I did not build or run it.

## Claims
- Open toolkit for landmarks, head pose, gaze and facial action units; "capable of real-time performance and is able to run from a simple webcam without any specialist hardware".
- Simple SVM/SVR on HOG features is "competitive even when compared to recent deep learning methods".

## Evidence
- AUs (Table II): 1, 2, 4, 5, 6, 7, 9, 10, 12, 14, 15, 17, 20, 23, 25, 26, 28, 45. "We predict intensity and presence of all AUs, except for AU28, for which only presence predictions are made."
- Outputs (wiki): `AU01_r` intensity on a "5 point scale" (0 absent, 1-5 min-max, continuous); `AU01_c` presence 0/1. Presence and intensity models were "trained separately", so they can disagree.
- Method: dimensionality-reduced HOG from a 112 x 112 aligned face plus shape features; "the median value of the features is subtracted from the current frame" for person normalization; for intensity, "we take the lowest nth percentile ... of the predictions on a specific person and subtract it". Wiki: dynamic models are the default for video and calibrate per person; the wiki recommends `-au_static` for low-dynamic-range sequences; multi-face videos are less reliable.
- Training data: DISFA, SEMAINE, BP4D, UNBC-McMaster, Bosphorus, FERA 2011.
- Validation (Table VI, DISFA intensity, Pearson r, 5-fold person-independent): AU1 .64, AU2 .50, AU4 .70, AU5 .67, AU6 .59, AU9 .54, AU12 .85, AU15 .39, AU17 .49, AU20 .22, AU25 .85, AU26 .67, mean .59. "The average concordance correlation coefficient (CCC) on DISFA validation set across 12 AUs of OpenFace is 0.70, while using OpenFace 2.0 it is 0.73."
- Speed: landmark detection at "30-40Hz frame rates on a quad core 3.5GHz Intel i7-2700K processor, and 20Hz ... on a Surface Pro 3 ... without any GPU support".

## License
OpenFace-license.txt: "ACADEMIC OR NON-PROFIT ORGANIZATION NONCOMMERCIAL RESEARCH USE ONLY"; derivatives "will be owned by Licensor" (CMU) and may only be used for "noncommercial internal research purposes". Confirmed noncommercial.

## Runs on this Mac without a GPU?
Probably, as offline CPU processing: the paper reports CPU-only real time on 2012-era Intel, and the command-line tools are listed for "Mac OS X". The Mac wiki is a Homebrew/CMake build that the author says he cannot test ("I don't have a Mac"), and it never mentions Apple silicon or arm64. Unverified on this machine.

## Verdict: adopt (human side only, offline, for continuous AU intensity)
- Use `AU12_r` (lip corner puller) and `AU04_r` (brow lowerer) as the camera analogues of zygomaticus and corrugator, plus `AU06_r`. AU12 (r = .85) is reliable; AU4 (.70) adequate; AU15 (.39) and AU20 (.22) too weak to carry a claim.
- Per-person normalization subtracts a running baseline, which helps windowed correlation but changes absolute levels; record which model (dynamic or static) was used.
- Never fed to the agent. Noncommercial license is acceptable for an internal research evaluation only.
- It is not a substitute for EMG on sub-visible rapid mimicry; validation was on visible, FACS-coded spontaneous expressions.
