# Bounded rationality, abstraction, and hierarchical decision-making: an information-theoretic optimality principle (Genewein, Leibfried, Grau-Moya & Braun)

Tim Genewein, Felix Leibfried, Jordi Grau-Moya & Daniel A. Braun, *Frontiers in Robotics and AI* 2:27, 2015, doi:10.3389/frobt.2015.00027.

## What was read
The full open-access HTML text from frontiersin.org: abstract, §1–6, all figure captions, and Tables 1–2. **The display equations are images and were not in the extracted text.** The forms written below are given where the prose states them (Eqs. 4, 9–10, 13, the serial and parallel objectives). Elsewhere they are labelled as the standard form the text describes. The Supplementary Methods and notebooks were not read.

## The computation, precisely

**One-step bounded rationality (§2.1).** Start from a prior policy $p_0(a)$. Maximise $\sum_a p(a\mid w)U(w,a) - \frac1\beta \mathrm{KL}(p(a\mid w)\|p_0(a))$. The solution is
$$p^\star(a\mid w) = \frac{p_0(a)e^{\beta U(w,a)}}{Z(w)}.$$
Its value is a free-energy difference ΔF(w). The limits:
- β → ∞ gives the maximum-expected-utility (MEU) choice;
- β → 0 leaves the agent on its prior.

β is also a sampling cost: the expected number of rejection samples needed is at least exp(KL). Fig. 1's numbers: about 95% of maximum utility costs about 1 bit, and the last 5% costs a further 2 bits.

**Optimal prior → rate–distortion (§2.2).** Optimising $p_0$ as well, averaged over $p(w)$, gives $p_0 = p(a) = \sum_w p(w)p^\star(a\mid w)$. The objective becomes
$$\max_{p(a\mid w)} \ \mathbb E[U] - \tfrac1\beta I(W;A),$$
which is "equivalent to the problem formulation in rate-distortion theory". The solution is given by self-consistent equations solved by Blahut–Arimoto iteration, with a convergence guarantee only in this one-step case: $p^\star(a\mid w)\propto p(a)e^{\beta U(w,a)}$, with $p(a)$ the marginal. In the authors' words: "the decision-maker is a channel that transmits information from w to a … limited channel capacity could also arise from noise … an agent with noisy sensors or actuators."

**Emergence of abstraction (§2.4, Figs. 2–3).** A recommender task: specific items have utility 3, category best-sellers 2.2, super-category 1.6.
- At β = 1.3 the agent mostly recommends the category item: "identical policies (i.e., columns in the plot) for sets of world-states".
- Sweeping β gives **plateaus** in H(A), separated by sharp kinks. Each plateau is one level of abstraction. Along a plateau, H(A|W) falls: the same actions are used, but less stochastically.
- "the abstractions are not induced because some stimuli are more similar than others under some utility-free measure … Rather, the abstractions are shaped by the utility function."

**Serial perception → action (§3).** The chain is W → X → A, with separate prices β₁ on I(W;X) and β₂ on I(X;A). The optimal percept is $p^\star(x\mid w) \propto p(x)\exp(\beta_1 \Delta F_{ser}(w,x))$: perception is chosen to maximise the *downstream action stage's* free energy. In the predator–prey example (three size groups):
- with the same 2 bits, the optimal percept discriminates small animals individually and merges the medium and large groups;
- when the action channel is cheapened to β₂ = 1, perception drops to "predator vs prey" only;
- "the percept in the bounded-optimal case no longer corresponds to some observed animal size but rather to a more abstract concept".

**Parallel hierarchy (§4).** A model selector p(x|w), models p(a|x) used as priors, and a low-level p(a|w,x). The objective is $\mathbb E[U] - \frac1{\beta_1}I(W;X) - \frac1{\beta_3}I(W;A\mid X)$. The optimal model is a Bayesian mixture of the low-level solutions. A hierarchy is optimal only if β₁ > β₃ *and* the selector's cardinality |X| is limited. Otherwise all processing shifts to the cheaper pathway. Fig. 11: each element stays ≤ 1.58 bits while the system's I(W;A) is ≈ 2.6 bits.

**General case (§5).** The objective is a total correlation with three prices. No convergence proof is given outside the one-step case, and the solutions are initialisation-sensitive (§6).

## What it means for the designs

Take W = the partner's perceived expression history, A = the agent's output, and a capacity on the W→A channel.

- **Categorisation of the partner is the central prediction, and it is shaped by the agent's own utility, not by similarity of faces.** Under a tight cap, partner states that call for the same *agent* response are merged. The agent's percept of the partner becomes "states that matter to me" (predator/prey), not "what the partner's face looks like". This is a precise information-theoretic statement of Principle 3: the other is read through what it means for the agent's own concerns. It also predicts **discrete regime switches** as capacity or price changes (the plateau kinks), not graded weakening.
- **Copying is expensive unless the utility rewards it.** Copy needs the action to be a one-to-one function of the partner's expression, which is the maximum-rate policy. With any finite price and a utility that does not specifically reward matching, the optimum merges partner states and does not copy. With a utility that rewards matching (prediction error on the partner, social reward for mirroring), copy is the β → ∞ limit. **The capacity is then a flat-to-copy dial** (β ↔ C is monotone): it fails D78 as a lone primitive, exactly as the Gershman/Lai "β indexes state-dependence" reading says.
- **Perseveration and default behaviour.** The marginal p(a) is the prior. A capacity-limited agent drifts toward its *own* habitual output whenever the partner's information is not worth its price. This is a self-restoring pull that coupling cannot switch off while C is finite (see C10 in non-copying-dynamics-synthesis.md).
- **Per-expression and sign.** Separate channels (expression families) can each carry their own C_i (the parallel architecture with several limited elements). Sign is set by U, not by the cap: if U says "comfort when the partner frowns", the bits are spent on a sign-flipped response at the same cost as a copy.
- **Held levels.** Not addressed: the framework is one-shot, with no dynamics. See the Tanaka note for why a rate cap leaks slow levels.
- **Framework.** This is rate–distortion / free-energy bounded rationality (Ortega & Braun), an existing framework, and an optimisation, so it is excluded as a core. It contributes two usable *constraint-level* ideas:
  1. the cardinality cap |X| as a hard, innate bound distinct from the price β (§4.3: "changing the cardinality of X … governs the channel capacity … but has no influence on the price"); a hard innate |X| is a capacity no learning can raise;
  2. the result that perception optimised under the cap is shaped by the action stage.

## Verdict
**adopt (two constraint-level ideas).**
1. A hard cardinality cap on the partner representation, as distinct from a price, is the innate form of a capacity.
2. Capacity-limited perception of the partner merges partner states by the agent's own utility, with stepwise regime changes.

The optimisation itself is existing machinery, and the capacity becomes a flat-to-copy dial whenever the utility rewards matching.
