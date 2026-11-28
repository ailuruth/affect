# Detecting an intermittent change of unknown duration (Sokolov, Spivak & Tartakovsky)

Grigory Sokolov, Valentin S. Spivak and Alexander G. Tartakovsky, "Detecting an intermittent change of unknown duration", arXiv:2210.17342v2 (10 Apr 2023), 34 pp. https://arxiv.org/abs/2210.17342

## What was read
arXiv v2, extracted text: §1–3 **in full** (motivation; ARL vs local unconditional and conditional false-alarm probabilities, Propositions 1–3 with proofs; Lorden's and Pollak's criteria restated; the reliable-detection criterion; maximum-likelihood derivations of CUSUM, window-limited CUSUM and FMA). §4 read for the window-limited CUSUM and FMA bounds (Lemmas 1–2 with proofs); the CUSUM integral-equation design in §4.1 skimmed. §5 (numerical study, Tables 1–6, QQ plots) read; §6 skimmed.

## What it says, precisely
- **Model.** i.i.d. g before ν, f during ν+1 … ν+N, g again after: the change lasts N samples and ends.
- **False alarms locally.** LPFA_m(T) = sup_ℓ P_∞(T ≤ ℓ + m | T > ℓ). Proposition 2: a bound α on LPFA_m implies ARL ≥ 1 + m(1 − α)/α, but **a large ARL does not bound LPFA_m** (counterexample: a deterministic wait followed by a geometric tail). For stopping times close to geometric (CUSUM, SR, WL CUSUM and FMA in their QQ plots at ARL ≈ 200), LPFA_m ≈ 1 − (1 − 1/ARL)^m (eq. 40), accurate to 0.1–12 % in Table 5.
- **Detection of a change that ends.** The criterion is the probability of detecting **while the change lasts**, LPD_π(T) = inf_ν Σ_k π_k P_ν(T ≤ ν + k | T > ν, N = k), maximised subject to LPFA_m ≤ α.
- **ML derivations.** With no information on the duration, maximising the likelihood over start and end gives exactly Page's CUSUM (eqs. 15–18: the running maximum of the CUSUM process). With an upper bound M on the duration, window-limited CUSUM; with known duration, the finite moving average (FMA).
- **Numbers (Gaussian mean shift of one SD, D = {5, …, 10} samples, m = 10; Table 1).** The probability of detecting within the change at LPFA 10⁻¹: WL CUSUM 0.744, CUSUM 0.742, FMA 0.729, mFMA 0.767; at LPFA 10⁻²: 0.395, 0.366, 0.384, 0.418; at LPFA 10⁻⁴: 0.064, 0.031, 0.051, 0.056. With D = {7, …, 15} (Table 2) at 10⁻⁴: 0.163, 0.137, 0.121, 0.126. The total KL of a 5–10-sample change is 2.5–5 nats; at small false-alarm probability such changes are mostly missed whatever the rule.

## What matters for this engine
1. **A switched copy is an intermittent change.** Each on-period of a 6-min/24-min copy is a transient change of known kind and unknown duration. The paper shows that whether a transient is caught depends on its **total information** against the threshold, and that at low false-alarm levels a transient whose accumulated KL is a few nats is missed by every rule (Table 1–2). This is the basis of the evasion floor in the synthesis: a route whose on-periods each carry less than about log(1/α) nats is not reliably caught by any detector at false-alarm level α.
2. **Measure false engagement locally**, not by mean time to false engagement: "at most once per N hours" should be stated as a local probability per window, which matches the operator's reading of "false engagement on ordinary partners".
3. **The ratchet turns detection of a transient into protection from all later ones**: once any on-period is caught, the copy stays held. The paper's criterion therefore applies to the first on-period only.

## Verdict
**adopt (the transient-change framing and its floor; watch for the reliable-detection criterion as a way to state F1).**
