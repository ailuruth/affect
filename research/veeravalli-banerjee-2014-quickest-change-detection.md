# Quickest change detection (Veeravalli & Banerjee)

Venugopal V. Veeravalli and Taposh Banerjee, "Quickest change detection", chapter in *Academic Press Library in Signal Processing*, vol. 3 (Elsevier, 2014); arXiv:1210.5552v1 (19 Oct 2012), 50 pp. https://arxiv.org/abs/1210.5552

## What was read
arXiv v1, extracted text, **in full**: §I–VIII (introduction; martingales, stopping times and nonlinear renewal theory; Bayesian theory with Theorem 3.2 and Corollary 1; minimax theory with Lorden's and Pollak's criteria, Lemma 2, Theorems 4.1–4.3, Corollaries 2–3; Moustakides's adversary interpretation; unknown pre/post-change distributions, GLR and window-limited GLR; data-efficient detection; distributed sensors; applications; open directions). The reference list was read only for the citations used below.

**Used here as the open restatement of three originals that are not reachable from this environment** (projecteuclid.org, jstor.org, academic.oup.com and ieeexplore.ieee.org are refused by the network proxy): Page 1954 (CUSUM, Biometrika 41), Lorden 1971 (Ann. Math. Statist. 42), Moustakides 1986 (Ann. Statist. 14) and Lai 1998 (IEEE Trans. Inf. Theory 44). Nothing in this repo should be read as a reading of those papers; the statements below are the chapter's.

## What it says, precisely
- **Setting.** Observations X_n; the distribution changes at an unknown time γ from f₀ to f₁. False alarms are measured by the mean time to false alarm E_∞[τ] (ARL) or its reciprocal FAR.
- **CUSUM (Page 1954, Algorithm 2).** W_{n+1} = (W_n + log L(X_{n+1}))⁺, W₀ = 0; alarm at W_n ≥ b. It is the maximum-likelihood test of "change at some k ≤ n" against "no change", maximised over k (eq. 49).
- **Lorden's criterion (eq. 51).** WADD(τ) = sup_n ess sup E_n[(τ − n)⁺ | X₁ … X_{n−1}]: the worst case over the change time **and over the pre-change path**. Lorden (1971) showed CUSUM with b = |log α| has FAR ≤ α and WADD ≤ |log α|/D(f₁‖f₀)(1 + o(1)), and that every procedure with FAR ≤ α has WADD ≥ |log α|/D(f₁‖f₀)(1 + o(1)) (via the optimality of the SPRT). Moustakides (1986) and Ritov (1990) showed CUSUM is **exactly** optimal for Lorden's criterion at every FAR.
- **Pollak's criterion** CADD(τ) = sup_n E_n[τ − n | τ ≥ n] ≤ WADD; Shiryaev–Roberts variants are second- or third-order optimal for it; CUSUM is first-order optimal for both (Corollary 3). Figure 5: CADD against −log FAR is a line of slope 1/D(f₁‖f₀).
- **Non-i.i.d. (Lai 1998; Theorem 4.3).** With Y_i the conditional log-likelihood ratio, if (1/t)Σ_{i=n}^{n+t} Y_i → I (condition 69), then inf_{FAR ≤ α} WADD ≥ inf CADD ≥ |log α|/I (1 + o(1)); the generalised CUSUM max_k Σ_{i=k}^n Y_i ≥ b has E_∞[τ] ≥ e^b and, under condition (71), WADD ≤ b/I (1 + o(1)). The lower bound's proof is a change of measure: any rule that stops within L_α = (1 − δ)|log α|/I of the change, before the log-likelihood has reached (1 − δ²)|log α|, would also stop that early under no change with probability ≥ e^{−V_α} times as often, contradicting the FAR constraint.
- **Unknown post-change parameter (§VI-A).** Lorden's GLR max_k sup_{|θ|≥a} Σ log(f_θ/f₀) with threshold of order |log α| has WADD_θ ∼ |log α|/D(f_θ‖f₀) for **each** θ: no first-order loss from not knowing θ. Lai's **window-limited** GLR and mixture tests (maximise only over change times in a window m_α, chosen as a function of the FAR) keep this optimality, also for non-i.i.d. data. Robust (least-favourable-pair) tests can beat GLR at moderate FAR.
- **Moustakides 2008 (§V).** Lorden's worst case is exactly the delay against an adversary who chooses the change time **with access to the observations**; Pollak's is the delay against an adversary who sees only the test's performance.
- **Open direction 1 (§VIII): transient changes**, which return to the pre-change state; then "detection while the change is still in effect" becomes the metric.

## What matters for this engine
1. **The exact shape of the frontier.** Delay ≈ log(ARL)/I, where I is the information per sample about the change. For the governor, a "sample" is one roughly independent batch of window means and I is the KL of a batch slope shifted from the boundary κ_g c_k to the copy's slope (synthesis, §2). Lorden's lower bound applies to **every** stopping rule, so it is a floor under any revision of the detector, not a tuning result.
2. **Worst case over the pre-change path is the right reading here.** Lorden's ess sup over X₁ … X_{n−1} is the case of a route that switches on when the partner's recent history makes the statistic least favourable; CUSUM is exactly optimal for that criterion, and Moustakides's adversary reading says it is optimal against a change time chosen with knowledge of the data.
3. **Unknown slope and lag cost nothing at first order** (GLR, mixture, window-limited GLR); the price of the lag search is in the threshold (second order).
4. **The theory assumes known pre-change law and light-tailed log-likelihoods.** The governor's statistic is heavy-tailed on ordinary partners (kurtosis ≈ 10 in the pass-12 check), so thresholds from the Gaussian formula are optimistic and must be set empirically.

## Verdict
**adopt (as the reference for the delay–false-alarm frontier and as the restatement of Page, Lorden, Moustakides and Lai).**
