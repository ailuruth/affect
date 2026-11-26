# Human decision making balances reward maximization and policy compression (Lai & Gershman)

Lucy Lai & Samuel J. Gershman, *PLOS Computational Biology* 20(4):e1012057, 2024, doi:10.1371/journal.pcbi.1012057.

**Substitution note.** The brief asked for Lai & Gershman 2021, "Policy compression: an information bottleneck in action selection" (*Psychology of Learning and Motivation* 74). That chapter, and the 2024 *Psychological Review* version, could not be reached from this session: gershmanlab.com returned 403, and dash.harvard.edu and bioRxiv were blocked or rate-limited. This 2024 PLOS paper by the same authors, which tests the 2021 theory experimentally, was read instead. Nothing below cites the 2021 chapter beyond what this paper restates.

## What was read
The full JATS XML from journals.plos.org: abstract, author summary, introduction, all Results, the Discussion, the full Methods (theory, process model, β-update rules, comparison models, fitting, recovery), and the supplementary figure captions. Figures were not seen.

## The computation, precisely

**Objective (Eqs. 9–13).** Policy complexity is
$$I^\pi(S;A) = \sum_s P(s)\sum_a \pi(a\mid s)\log\frac{\pi(a\mid s)}{P(a)},$$
the number of bits about the state used to choose actions. A capacity-limited agent solves
$$\arg\max_\pi V^\pi \ \text{s.t.}\ I^\pi(S;A) = C \qquad(\text{dual: } \min I \text{ s.t. } V = R).$$
The optimum is
$$\pi^*(a\mid s)\propto \exp[\beta Q(s,a) + \log P^*(a)],\qquad P^*(a)=\sum_s P(s)\pi^*(a\mid s),$$
with $\beta^{-1} = dV/dI$ at the capacity. β is monotone in C, but there is "no analytical form for the mapping from C to β".

**Process model (Eqs. 15–25).** An actor-critic on $\mathbb E[\beta r - \log\frac{\pi(a\mid s)}{P(a)}]$:
- the marginal is tracked as $\Delta P(a) = \alpha_P[\pi(a\mid s) - P(a)]$;
- the complexity estimate $\xi$ is a moving average of the per-trial *policy cost* $\log\frac{\pi(a\mid s)}{P(a)}$;
- β adapts in one of three ways: toward capacity, $\Delta\beta = \alpha_\beta(C-\xi)$; toward an aspiration, $\Delta\beta = \alpha_\beta(R - \rho)$; or both (the winning "Capacity–Value" rule), $\Delta\beta = \alpha_\beta(\frac{C-\xi}{R-\rho} - \beta)$.

**Response time (Eq. 6).** $\log RT = \log[t_0 + b_1\log\frac{\pi(a\mid s)}{P(a)} + b_2 H(\pi(\cdot\mid s))] + \epsilon$. The rationale: decoding a compressed (Huffman-like) code takes time proportional to the bits inspected.

**Experiments.** 200 MTurk subjects; 3 states × 3 actions; three tasks with a control (Q1) and a test (Q2) condition each.
- **Task 1 (state frequency).** One stimulus appears with P = 0.6. Reward was higher in Q2 at equal complexity (d = 0.34). Subjects preferred the suboptimal action that is *frequent overall* in the other states (d = 0.25 and 0.15).
- **Task 2 (shared optimal action).** Complexity was lower in Q2 (d = 0.20) and reward higher (d = 0.89). Of two equally rewarded optimal actions, subjects chose the one with the higher marginal (d = 0.31, 0.34). Action bias correlated with complexity at r = −0.82.
- **Task 3 (time pressure, 1 s vs 2 s).** Complexity fell (d = 0.50), reward fell, stochasticity rose (d = 0.39), and the shift toward the high-marginal suboptimal action rose (d = 0.32). Only the action favoured by the marginal changed: the other suboptimal choices did not move (d ≈ 0.08).
- **Re-analysis of Collins' set-size data (N = 40).** The bias toward high-marginal actions is present at every set size and increases only weakly with it.
- **Trait-like capacity.** Complexity in the control condition was flat across tasks (F = 1.03, p = .36) and correlated across tasks (r = 0.43–0.57).
- **RT.** Policy complexity correlated positively with RT in all tasks (r = 0.51–0.67). The non-compression models predict the opposite sign.

Limits, as stated by the authors:
- the model variants within the compression class are not identifiable (BIC gap 71.7; PXP fails);
- most subjects lie off the optimal reward–complexity curve;
- other perseverations (sequential effects, motor habits) are not explained;
- the theory "assumes people always prefer simpler policies", whereas empowerment-seeking can reverse this.

## What it means for the designs

If the agent's dependence on the partner were a capacity-limited policy, with state = partner expression and action = agent expression, this paper gives the measured human signatures of the cap:

- **Perseveration toward the agent's own marginal, not toward the partner.** Under compression the agent's response to any partner state is pulled toward *its own* most frequent responses. That is a pull toward the agent's self, not the partner. It is anti-copy in a precise sense: as C falls, the partner-specific part of the output shrinks toward a partner-independent default. Time pressure and load (more partners, more expression families) strengthen it. This is the human evidence for the "default pull" predicted by Genewein's optimal prior.
- **Sluggishness and stochasticity under pressure.** When the decision window shortens (fast face dynamics), complexity drops and stochasticity rises. A fast partner channel should get *fewer* bits per event than a slow one, which works against fast echo copying. But it does not stop slow matching (see the Tanaka note).
- **Capacity looks innate and trait-like.** It is roughly constant within a person across tasks, which supports making C an innate constant of the agent rather than a learned scalar. But the *β* that implements it adapts trial by trial (Eqs. 21–25), so in the model the moment-to-moment state-dependence is a learned dial bounded by C. For D78 the bound is C, and C is one scalar over everything the policy reads, unless it is split per channel.
- **Sign and gain.** The framework says nothing about sign: Q(s,a) decides what the bits buy. A copy policy and a complementary policy of the same state-dependence have the same complexity.
- **Copy non-attracting?** Only if Q does not reward matching. Here the information term's attractor is the marginal (the self). That is useful: in Lagrangian form the *cost* side always pulls away from partner-dependence, including copy. But whether copy is attracting overall depends on the value side.
- **Framework.** Policy compression is rate–distortion applied to RL (Tishby lineage; existing), and it is optimisation-based, so it is excluded as a core. As a constraint it supplies a measurable human quantity (policy complexity, via the Hutter estimator) that could be estimated for real partner→face coupling in the Seamless data, without labels.

## Verdict
**adopt (evidence, not mechanism).** It is the strongest human evidence read here that a capacity limit produces:
- perseveration toward one's own frequent actions;
- more of that bias under time pressure and load;
- a trait-like, cross-task capacity.

It also supplies the estimator to measure partner→agent policy complexity. The model itself is rate–distortion RL. Its capacity is a single scalar, and it is sign-blind.
