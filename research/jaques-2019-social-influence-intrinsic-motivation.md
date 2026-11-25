# Jaques, Lazaridou, Hughes, Gulcehre, Ortega, Strouse, Leibo & de Freitas 2019, "Social influence as intrinsic motivation for multi-agent deep reinforcement learning" (ICML 2019, PMLR 97; arXiv:1810.08647)

Source read: arXiv v4 (18 Jun 2019), via pdftotext. Read in full: main text §1–§9 (sequential social dilemmas, MARL setup, basic influence and Experiment I, influential communication and Experiment II, Model of Other Agents and Experiment III, related work, causal-inference details with Fig. 8, conclusions), plus supplementary Table 4 (final collective rewards). Not read: the rest of the supplement, including the MI proof (§10.1), hyperparameter tables and the speaker-consistency formula. The arXiv v4 header carries the ICML 2018 template line; the paper appeared at ICML 2019.

## Claims
- Agents get an intrinsic reward for causally influencing other agents' actions. Influence is assessed counterfactually: "How would j's action change if I had acted differently in this situation?"
- In expectation, the reward is the mutual information between the agents' actions, I(a^k; a^j | s), a "social form of empowerment".
- Influence was sparse in time: "An agent's influence is only greater than its mean influence in less than 10% of timesteps". Listeners are not compelled to listen, so influence through cheap-talk messages must carry useful information.
- Decentralised version: each agent learns a Model of Other Agents (MOA) that predicts the others' next actions, p(a_{t+1} | a_t, s_t^k). It then computes influence by imagining counterfactual actions through the MOA. No access to others' rewards or policies is needed.
- Caveat stated by the authors: "it may be possible to influence another agent in a non-cooperative way". With communication, they argue, influence must be informative because the listener is trained only on environment reward.

## Evidence with numbers
- Environments: Cleanup (public goods) and Harvest (common-pool resource) sequential social dilemmas (agent count not checked in the text read), learned from pixels with A3C plus an LSTM. Results are from the best hyperparameter setting, 5 seeds; error bars are 99.5% CI.
- Final collective reward over the last 50 agent steps (Supplement Table 4):

  | model | Cleanup | Harvest |
  |---|---|---|
  | A3C baseline | 89 | 485 |
  | Inequity aversion (Hughes et al. 2018; sees others' rewards) | 275 | 750 |
  | Influence, basic (centralised) | 190 | 1073 |
  | Influence, communication | 166 | 951 |
  | Influence, MOA (decentralised) | 392 | 588 |

- Across 100 sampled conditions, being influenced through communication correlated with the listener's own task reward: Cleanup ρ = .67, Harvest ρ = .34, both p < .001.
- Influence agents learned to use their own movement as a binary signal (moving only when apples were present). In Cleanup, the best communication-head setting used α = 0: influence reward alone, with no extrinsic reward.

## Mechanism
Reward r_t^k = α e_t^k + β c_t^k, where c is the causal-influence term:

c_t^k = Σ_{j≠k} D_KL[ p(a_t^j | a_t^k, s_t^j) ‖ Σ_{ã} p(a_t^j | ã_t^k, s_t^j) p(ã_t^k | s_t^j) ] = Σ_{j≠k} D_KL[ p(a_t^j | a_t^k, s_t^j) ‖ p(a_t^j | s_t^j) ].

- The marginal is formed by sampling counterfactual actions ã from the agent's own policy.
- For a correct counterfactual, the conditioning set must include the influencee's internal LSTM state u_t^j (eq. 3).
- The basic version requires that k acts before j within a step, so that "k can influence j but j cannot influence k". In other words, feedback is removed by ordering.
- Communication version: c uses m_{t−1}^k in place of a_t^k.
- MOA version: the MOA is trained by cross-entropy on observed trajectories to predict a_{t+1}^j from (a_t, s_t^k). The authors argue that the backdoor path through s_t is blocked by colliders at s_{t+1}, u_{t+1}^j, and that "it would be sufficient to condition only on s_t^k". The influence reward is given only while j is in k's field of view, where the MOA is more accurate.

## What it implies for an engine that learns a partner model from closed-loop interaction
1. **Counterfactual influence is the right *quantity* for "does the partner respond to me".** The agent asks what the partner's next face would be had it expressed differently, and averages the divergence over its own counterfactual expressions:
   C(s) = E_{x̃∼π}[ D( p(z_{t+τ} | x, s) ‖ E_{x̃} p(z_{t+τ} | x̃, s) ) ].
   With a linear-Gaussian partner model z = Rx + noise, this reduces to a function of R and the agent's own expression variance, which a person can inspect.
2. **It is only as causal as the partner model it runs through.** In the decentralised MOA case, the MOA is fitted by supervised learning on closed-loop trajectories, and the influencer's actions there depend on its view of the influencee's past behaviour. Their no-confounding argument assumes k's observation s_t^k blocks every backdoor. It does not block a path through j's *memory* u^j, which shapes j's earlier actions, which shape k's action through k's own memory. For a partner with persistent hidden state (a person), and an agent that follows, a supervised MOA learns exactly the C13 association. Their counterfactual is then a counterfactual of the agent's own following. The fix is to train the partner model on the exogenous part of the agent's expression (IV, or IP weights from the agent's known propensities), not on all trajectories. See forssell-ljung-1999-closed-loop-identification.md and hernan-robins-2020-what-if-iv-gmethods.md.
3. **The basic version avoids confounding by turn order.** This is the multi-agent version of the "delay in the loop" condition: identification needs the agent's act to precede the partner's response, with no within-step loop back. In a live face-to-face dyad there is no enforced order, so lag 0 is unidentifiable and influence must be measured at τ ≥ one frame.
4. **Use as a measurement, not as a reward.** Rewarding influence over the partner is close to what the project's Principle 6 forbids: learning to move the partner, the flattery and provocation path. The authors note that non-cooperative influence is possible, and their safeguard (a listener who may ignore cheap talk) does not apply to a human partner's facial reflexes. For example, the agent could learn to provoke reflex smiles. Keep C as an *estimate of partner responsiveness* that feeds the agent's model, and never as a quantity the agent's policy is trained to maximise.
5. **Sparsity is informative.** The partner responds in under 10% of moments, the ones that matter. So the estimate should be situation-dependent (when does the partner respond?) rather than a global gain. This matches Seitzer et al.'s local causal influence; see seitzer-2021-causal-influence-detection.md.

## License
ICML proceedings, © the authors. Environment code is open source (github.com/eugenevinitsky/sequential_social_dilemma_games); the agent code was not checked.

## Verdict: watch (adopt the counterfactual-influence measure; reject influence as a reward)
It gives a clean, inspectable definition of counterfactual influence on another agent, and shows that a learned model of the other suffices to compute it. But the decentralised estimator is trained on closed-loop observational data, which is the confound at issue. Its no-confounding argument holds for its grid-world setup, not for a partner with hidden persistent state. Its use as an intrinsic reward runs against Principle 6. Evidence is 5 seeds per condition in two games.
