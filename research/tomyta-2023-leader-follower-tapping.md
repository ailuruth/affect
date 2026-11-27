# The physiological basis of leader-follower roles in the dyadic alternating tapping task (Tomyta, Saito & Ohira)

Citation: K. Tomyta, N. Saito, H. Ohira. "The physiological basis of leader-follower roles in the dyadic alternating tapping task." *Frontiers in Psychology* 14:1232016, 2023. doi:10.3389/fpsyg.2023.1232016.

Source read: the Frontiers PDF, text-extracted. Read in full: abstract, Introduction, Methods, Results, Discussion. **Not read:** the Supplementary material, which holds the state-space model itself.

## The study
- **Task.** 41 pairs (one excluded), side by side across a partition, tapping a key alternately (anti-phase). Block 1: one partner is told to lead (may change tempo), the other to follow; Block 2: roles swapped; 5 min each. ECG (BIOPAC), 14-channel consumer EEG (Emotiv EPOC).
- **Role estimate.** A state-space model fitted to each person's inter-tap intervals with two parameters: α_Self ("degree one's tap(n) was explained by one's tap(n−1)") and α_Pair ("explained by one's tap(n−1) and pair's tap(n−1)"). Leader-like = high α_Self; follower-like = high α_Pair. The model's equations are only in the supplement.
- **Results as reported.**
  - Block 1: pairs in which both had α_Pair above the median had higher R–R interval correlation than pairs with one or none (t₃₅ = −3.54, P < 0.01; t₃₅ = −3.49, P < 0.01). Block 2: no differences (F₂,₃₅ = 0.37, P = 0.70); the authors suspect an order effect.
  - HF-HRV correlated with α_Pair in Block 1 (r = 0.23, P < 0.05), not in Block 2.
  - Phi1 (10–12 Hz) larger in high-α_Self participants; Phi2 (12–13 Hz) larger in high-α_Pair participants (the Discussion states the opposite direction for Phi2 from the Results).
- **Reporting problems.** Several statistics are impossible as printed (e.g. "r = 1.4", "r = 1.82"); the Methods say the R–R intervals for synchrony came from the 10-min resting ECG, which would precede the task; a non-significant contrast is printed with t = −3.54. The findings cannot be relied on as stated.

## The mathematical object
Each person's timing as a bivariate autoregression with a self term and a pair term, so "leading" and "following" are two separate per-person coefficients, not one asymmetry score. Heart-rate synchrony appeared, if at all, when **both** partners were following (mutual adaptation), not in a leader–follower pair.

## What it means for the design
- Weak support, consistent with boukarras-2025: physiological synchrony goes with mutual adaptation, not with one partner driving the other.
- The two-coefficient description (own persistence and responsiveness to the other, estimated separately) is the standard bivariate AR/TIES form already in the index (butler-2011-temporal-interpersonal-emotion-systems.md).

## Verdict
- **reject as evidence (reporting errors; model unread); watch only as a pointer** to mutual-adaptation accounts of heart-rate synchrony.
