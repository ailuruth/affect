# Differential privacy: on the trade-off between utility and information leakage (Alvim, Andrés, Chatzikokolakis, Degano & Palamidessi)

Mário S. Alvim, Miguel E. Andrés, Konstantinos Chatzikokolakis, Pierpaolo Degano & Catuscia Palamidessi, *Formal Aspects in Security and Trust (FAST 2011)*, LNCS 7140, pp. 39–54, 2012; arXiv:1103.5188v3 (25 Aug 2011), 30 pp. with appendix.

This note stands in for **Smith 2009, "On the foundations of quantitative information flow" (FoSSaCS)** and the later g-leakage papers of Alvim et al. None of them was reachable: the FIU and HAL hosts were blocked from this session. Smith 2009 is cited here only through this paper's background (§2.2, ref. [12]). Nothing here about g-leakage in general, or about its data-processing behaviour, goes beyond what this paper states.

## What was read
arXiv v3: §1–7 in full (background; channel model; Theorems 1–2 and Propositions 1–2 on leakage; Definitions 2–3 and Theorems 3–4 on utility and the optimal mechanism; Examples 1–3; related work). The appendix proofs were not read.

## The computation, precisely

**Channel view.** A randomized query K is a channel matrix p(z | x) from databases x ∈ 𝒳 = Val^u (u individuals, v values each) to reports z. ε-DP ⇔ p(z | x) ≤ e^ε p(z | x′) for all z and all adjacent x ~ x′.

**Min-entropy leakage (after Smith 2009).** H_∞(X) = −log₂ max_x p(x). H_∞(X | Z) = −log₂ Σ_z p(z) max_x p(x | z). I_∞(X; Z) = H_∞(X) − H_∞(X | Z). This is the log of the ratio of a one-guess adversary's success after and before observing Z. Capacity C_∞ = max_{p_X} I_∞ is attained at the uniform prior and equals log₂ Σ_z max_x p(z | x).

**Theorem 1.** If K is ε-DP, then for every prior,

  I_∞(X; Z) ≤ u log₂( v e^ε / (v − 1 + e^ε) ).

This is tight (Proposition 1). It is 0 at ε = 0 and tends to u log₂ v as ε → ∞. The tight matrix has entries a/e^{εd}, where d is the graph distance in the adjacency graph.

**Proposition 2 (small range).** If |Range(K)| = r, then I_∞ ≤ log₂[ r e^{εu} / ((v − 1 + e^ε)^ℓ − e^{εℓ} + e^{εu}) ] with ℓ = ⌊log_v r⌋. For r = v this is log₂[v e^{εu}/(v − 1 + e^{εu})] < log₂ v: **a mechanism with few possible outputs leaks at most about log₂ r bits, however many inputs it reads.**

**The converse fails.** Small min-entropy leakage does not imply DP, because a rare observation with zero probability under one input breaks DP but hardly moves an average.

**Theorem 2 (one individual).** Fix the other u − 1 values. Then I_∞(X_{D−}; Z) ≤ log₂ e^ε, for every prior.

**Utility as a gain function.** The user sees z and remaps it to a guess y′ = ρ(z) of the true answer y = f(x). The utility is U(Y, Z) = Σ_y p(y) Σ_{y′} p(y′ | y) g(y, y′). With the binary gain, U = Σ_z max_y p(y, z): the converse of the Bayes risk, and H_∞(Y | Z) = −log₂ U.

**Theorem 3 (utility ceiling).** Assume the answer graph (𝒴, ~) is vertex-transitive and every distance shell has size 0 or ≥ c. Then an ε-DP K has

  U ≤ (e^ε)^n(1 − e^ε) / ( (e^ε)^n(1 − e^ε) + c(1 − (e^ε)^n) ),

where n is the graph diameter. Theorem 4 constructs the optimal mechanism p(z | y) = α/e^{ε·dist(y, z)}, which attains this bound under a uniform prior. Rings (counting modulo |𝒴|) and cliques satisfy the condition. Example 2 (clique of 6 cities, ε = log 2): the optimal mechanism has U = 0.2857, against 0.2243 for the truncated geometric mechanism. Example 3 (a line, 5 voters): the truncated geometric mechanism (4/9) beats the ring construction (4/11). Optimality depends on the answer graph.

## Evidence with numbers
Worked examples only (Tables 1–2, Figure 3: B(u, v, ε) for u = 100 and v = 2, 10, 100).

## What it means for the designs
1. **The agent is the "user" whose gain is copying.** Read the agent's own output as the remapped guess y′ about the partner's state y. Its copy score is a utility U(Y, Z) with gain g(y, y′) = "the agent's expression matches the partner's". Theorem 3 then **caps the agent's copy success** under ε-DP, for any remapping, so for every downstream route. With binary gain on a clique of c + 1 = 6 partner-expression categories at ε = log 2, the agent can match the partner's category at most 0.2857 of the time, against a chance level of 1/6.
2. **But the same ceiling caps every contingent response.** A gain g(y, y′) = "the agent's expression is the appraisal-appropriate response to y" is equally a utility over a remapping. The theorem bounds it identically. **No leakage or utility bound distinguishes copying from contingent responding when the contingent map is a bijection of the partner's state.** This is the formal form of the sign-blindness noted in kairouz-2015.
3. **Where they do differ: range.** Proposition 2 says a mechanism with r possible outputs leaks at most about log₂ r bits. Contingent responding is typically *categorical*: comfort or not, approach or not, a few appraisal outcomes. Copying a held level is *continuous*: it needs fine resolution in the partner's own coordinates. So a small budget admits a few-category contingent decision almost at full utility, and rules out tracking. **Copying is information-expensive and categorical contingency is information-cheap.** That asymmetry, not sign, is what a budget can exploit.
4. **Theorem 2's per-individual form is the dyad.** Hold "everything else" fixed: the agent's own drives, the context, the words. The leakage about the partner's face alone is ≤ ε·log₂ e bits per guess, for every prior. This is the right reading of a budget "with respect to the partner's face stream": it is conditional on all the agent's own variables.
5. **The independence caveat bites.** DP's guarantee is relative to neighbouring inputs. If the partner's words carry their mood and the words are not in the protected input, DP with respect to the face says nothing about mood leaking through words. The protected secret must be the partner's whole input to the agent, or the guarantee is about a channel, not about the partner.

## Verdict
**adopt (the agent-as-guesser reading: copy score is a utility capped by ε-DP over every remapping; small-range outputs leak ≤ log₂ r).** It confirms that DP cannot separate copy from contingent response by sign or direction. It shows that it *can* separate them by resolution: categorical contingency is cheap, continuous tracking is expensive.
