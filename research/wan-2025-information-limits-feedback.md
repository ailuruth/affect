# An information-theoretic analysis of discrete-time control and filtering limitations by the I-MMSE relationships (Wan, Li, Hovakimyan & Voulgaris)

Neng Wan, Dapeng Li, Naira Hovakimyan & Petros G. Voulgaris, arXiv:2304.09274v2 (17 Mar 2025), 19 pp., "the extended version of the paper with the same title accepted by IEEE Transactions on Automatic Control". This note stands in for **Martins & Dahleh 2008, "Feedback control in the presence of noisy channels: 'Bode-like' fundamental limitations of performance", IEEE TAC 53(7):1604–1615**. That paper and Martins, Dahleh & Doyle 2007 were not reachable: the hosts dahleh.lids.mit.edu and doyle.caltech.edu are outside this session's network. Wan et al. restate the Martins–Dahleh entropy inequality and generalise it. Nothing below is attributed to Martins & Dahleh beyond what Wan et al. say of it.

## What was read
- **Read in full:** §I (introduction and literature, including the Martins–Dahleh paragraph), §II (definitions, Lemma 2.3 Duncan's theorem, Theorem 2.4 the discrete I-MMSE sandwich) and §III.A–B (the general nonlinear control channel (9)–(11), Theorem 3.2, Proposition 3.3, Theorem 3.4 with its proof, Proposition 3.6 and Corollary 3.7 for LTI plants).
- **Skimmed:** §III.C–D and §IV (LTV and nonlinear cases, filtering). Appendices not read.

## The computation, precisely

**Setting (eq. 9–11).** A plant X_{i+1} = f_i(X_i) + b_i(X_i)E_i, Y_i = h_i(X_i), with controller U_i = g_i(Y_0^i, C_0^i). The loop is seen as a channel with feedback,

  E_i = U_i(E_0^{i−1}, C_0^i, X_0) + W_i,  W_i ~ N(0, I) white,

where the "message" is (C, X₀): the command signal and the initial state.
- (A1): mean-square internal stability and finite input power E[UᵀU] < ∞.

**Proposition 3.3 (conservation identities).**
- I(E_0^n; C_0^n, X_0) = I(E_0^n; X_0) + I(E_0^n; C_0^n | X_0).
- I(E_0^n; C_0^n, X_0) = h(E_0^n) − h(W_0^n).

Wan et al.: "the important entropy inequality in [Martins & Dahleh, Theorem 4.2], i.e., h(E_0^n) ≥ I(E_0^n; X_0) + h(W_0^n), can be restored from (14) and (15)." That is, the loop must carry at least the information needed to cancel the plant's instability.

**Theorem 2.4 / 3.2 (I-MMSE sandwich, with or without feedback).**

  ½Σ cmmse(U_i) ≤ I(E_0^n; C_0^n, X_0) ≤ ½Σ pmmse(U_i),

where pmmse and cmmse are the one-step prediction and causal filtering MMSEs of the channel input. This holds "regardless of the distribution and stationarity of the signals".

**Theorem 3.4 (the ceiling).** C_LB ≤ Ī(E; C, X₀) ≤ C_f. Under the power constraint E[U_iᵀU_i] ≤ ρ_i, the feedback capacity equals the no-feedback capacity:

  C_f = C = lim (1/2(n+1)) Σ_i log|Σ_{U_i} + I|  (scalar: (1/2(n+1)) Σ log(1 + ρ_i)).

**Feedback does not raise the ceiling** of this power-limited Gaussian channel, whatever the controller does.

**Proposition 3.6 (LTI, the floor).** For a mean-square-stable LTI loop, Ī(E; X₀) = Σ_j log|λ_j⁺(A)| (the open-loop unstable poles). This is the information-theoretic form of Bode's sensitivity integral. Corollary 3.7: with a *nonlinear* controller the rate is still ≥ Σ log|λ_j⁺(A)|.

## Evidence with numbers
Theorems; a numerical check of the sandwich (22) is in an appendix that was not read. The reusable fact: for a scalar Gaussian channel with power ρ and unit noise, the information through the loop is at most ½log₂(1 + ρ) bits per step, with or without feedback.

## What it means for the designs
1. **A floor and a ceiling on what any loop carries.**
   - The *ceiling* (Theorem 3.4): if the partner's face enters the agent only through a power-limited channel with innate noise, the total information per step through the whole loop, all routes included, is at most ½log(1 + SNR). Feedback (the partner reacting to the agent's face) cannot raise it.
   - The *floor* (Prop. 3.6, Martins–Dahleh): a loop that stabilises something unstable must carry at least Σ log|λ⁺|.

   For the designs the floor is a warning. If any design makes the agent's affect *depend on the partner for its own stability* (a comfort loop the agent needs to stay regulated), that loop is forced to carry information about the partner at a rate fixed by the instability. That is a structural reason why "partner as regulator" designs leak partner content into the face.
2. **Per-channel innate ceilings** follow by giving each expression channel its own noisy perceptual channel with innate (ρ_i, noise). The design-level statement is: "the agent's perception of partner channel i is a Gaussian channel of innate SNR_i; hence I(P_i → anything in the agent) ≤ ½log(1 + SNR_i) per sample, for all architectures, learning states and loops." Learning cannot raise SNR_i if the noise is injected before any learned stage.
3. **The care loop, diagnosed.** Critique 3 found the care route to be a model-free proportional regulator of the user's read state toward their baseline. By Prop. 3.6's logic, a regulator that holds an unstable or slowly drifting quantity must transmit at the instability rate. The leak is not a bug in the bound; it is required by what the loop is for.
4. **Where it falls short.**
   - Same as directed information: sign-blind, and loose for slow, low-entropy expressions.
   - The power-limited AWGN form needs an explicit innate noise stage in the perception path, which the designs do not currently have. Their perception is deterministic analysis-by-synthesis, which has unbounded capacity in principle.
   - Existing framework (information-theoretic control limits). Usable only as a **constraint on the partner port** and as a diagnostic for regulator-type designs, not as a core.

## Verdict
**watch (ceiling: feedback capacity = no-feedback capacity under an innate power/noise limit; floor: a loop that regulates must carry the instability rate).** The floor explains why regulator designs leak. Martins & Dahleh 2008 itself not reached.
