# Heerey, Clerke, Johnson & Patenaude 2024, "The subjective value of genuine smiles guides real-world social behaviour" (PLoS ONE 19(6):e0304726, doi 10.1371/journal.pone.0304726)

Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC11166336/ (open access). Data and code: OSF 3m95e (not opened).

## What was read
The full PMC text: introduction, hypotheses, methods, results, discussion, table 1. The supplementary text (stimuli, reliability details, descriptive tables) was not opened.

## What it says
- **Sample and order.** 361 undergraduates online (Zoom, early 2021); 309 with usable task data, 263 with usable video, 131 dyads for the dyad-level model. Order: a 5-min unscripted Zoom conversation with a stranger first, then the smile-valuation task (as Heerey & Gilder 2019: six faces, 80 % vs 60 % wins, genuine / polite / neutral feedback on wins; 30 exposures per face; 120 test choices), then a visual search task with the same faces as neutral distractors.
- **Smiles have value.** Median utilities > 0 for money, genuine and polite smiles; genuine-smile utility (1.04) exceeded money's (0.67), so on average a low-paying genuinely smiling face was preferred to a high-paying neutral one. Split-half reliabilities .74–.79. Genuine-smile utility was uncorrelated with money utility (r = .02).
- **Attention capture.** Neutral faces previously associated with smiles slowed search for a novel target more than familiar neutral faces (F(2,616) = 213.3, ω² = .40; genuine > polite > neutral). The genuine-smile capture effect correlated with genuine-smile utility (ρ = .47).
- **Reciprocity in the conversation** (FaceReader 8 at 15 fps; genuine = AU12 with AU6, polite = AU12 without AU6; a return = the same type within 4 s of the partner's smile onset):
  - proportion returned: genuine .72 (SD .15) vs polite .57 (SD .20), d = .66;
  - onset-to-onset latency: genuine **939 ms (SD 358)** vs polite **1413 ms (SD 297)**, d = −.99.
- **Value predicts speed of genuine return.** Genuine-smile utility correlated with genuine return latency (r = −.27, 95 % CI −.38 to −.16), as did attention capture (ρ = −.18). Neither predicted polite return speed, and polite utility did not predict polite speed (ps > .65).
- **Partner effect.** In an actor–partner model, a person's genuine-return latency predicted the *partner's* rating of interaction quality (−.20, p = .0006), not their own (−.08, n.s.). Proportion returned and polite latency predicted nothing.

## What matters for this engine
- **A human norm for return latency by smile type.** Natural strangers return genuine smiles in about 0.94 s and polite ones in about 1.41 s, onset to onset, with 72 % and 57 % returned within 4 s. The build core's fast echo starts at 0.45 s on every smile channel, with one latency for both types. That is about 1.4 SD faster than the genuine-return mean, plausible for the fastest returns but not for the distribution, and it has no type difference. This is an evaluation marker (the echo's onset distribution against these numbers on recorded dyads), not a parameter to copy.
- **The learning signal is approval-open.** The individual difference that predicts faster return is how much the person values seeing a smile, measured as willingness to give up money for it. That is the partner's expression as a reward. The study is correlational, the valuation task came after the conversation, and attention capture covaries with value, so an approval-closed alternative (earlier detection of a predictive cue) is not excluded for the speed result. But the predictor itself is a reward value of the smile, and no prediction of anything else is measured. The engine may not use it (Principle 6); the build core has no route by which his smile relieves a drive, and must not get one.
- **Within-session learning is not shown.** The smile-value contingencies are learned within the task (30 exposures per face), but the link to conversation is between people, not across trials. Nothing here shows a partner-specific change inside one conversation.

## Limits
Online video interaction; automated AU coding at 15 fps (each frame 67 ms); one 5-min conversation per person; correlational; order fixed (conversation before tasks).

## Verdict: adopt (as the evaluation norm for return latency and rate by smile type); reject the value mechanism for the engine
