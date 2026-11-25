# Seitzer, Schölkopf & Martius 2021, "Causal influence detection for improving efficiency in reinforcement learning" (NeurIPS 2021; arXiv:2106.03443)

Source read: arXiv v2 (2 Dec 2021), via pdftotext. Read in full: main text §1–§7 (introduction, related work, background on local causal graphs and the but-for test, CAI definition and estimator with Propositions 1–2, detection experiments, three RL uses, discussion and limitations). Not read: the supplement (proofs A.1–A.3, the Gaussian-mixture KL formula A.4, environment details, extra results including the combined 95% run).

## Claims
- Causal influence of actions is *situation-dependent*: a robot arm can move an object only in contact with it. The agent is "in control" of entity S_j in state s if the local causal graph G_{S=s} keeps the edge A → S_j′ under every full-support policy.
- Proposition 1: the edge A → S_j′ exists in G_{S=s} under do(A := π(a|s)) iff S_j′ is not independent of A given S = s.
- Proposition 2: dependence under one intervention implies dependence under all full-support interventions. Independence under one full-support intervention implies independence under all of them. So a single full-support policy, such as uniform, is enough to detect control.
- Causal action influence (CAI) is a pointwise conditional mutual information, C^j(s) = I(S_j′; A | S = s).
  - It is a one-step local transfer entropy that conditions on the full state.
  - For state-independent policies it is a pointwise version of Janzing et al.'s causal strength.
  - It is a lower bound on one-step empowerment, which is max_π C(s).
- Related to "contingency awareness" in psychology (the paper's ref. 38; the authors cite it as knowing that one's actions can affect the environment).
- Limitations stated:
  - full observability is assumed, "which simplifies the causal inference problem as there is no confounding between an agent's action and its effect";
  - the state factorisation into entities is given;
  - estimation needs a correct model, and "deep networks can struggle at times to pick up the causal relationship between actions and entities."
- On data: "if the data policy is different from the sampling policy π, the model is biased to some degree." Training only on samples drawn from π reduces the bias, but the authors "find to obtain better performing models by training on all data despite potentially being biased."

## Evidence with numbers
- Detection (5 seeds, K = 64 sampled actions):

  | method | 1D-Slide AUC / AP / F1 | FetchPickAndPlace AUC / AP / F1 |
  |---|---|---|
  | CAI | 1.00 / 0.98 / 0.95 | 0.97 / 0.96 / 0.89 |
  | entropy H(S_j′\|s) | 0.96 / 0.47 / 0.50 | 0.84 / 0.73 / 0.78 |
  | attention (Pitis et al.) | 0.42 / 0.13 / 0.18 | 0.46 / 0.44 / 0.62 |
  | simulator contacts | 0.89 / 0.78 / 0.88 | 0.79 / 0.77 / 0.73 |

  Performance degrades gracefully as observation noise rises to 20% of one standard deviation.
- RL with DDPG+HER, 10 seeds, sparse-reward Fetch tasks:
  - CAI alone as reward: the agent learned to grasp, lift and hold the object after about 2000 episodes.
  - As an exploration bonus (λ = 0.2): 60% success about 4× faster than no bonus.
  - Choosing the most influential of K sampled actions during exploration: about 2× faster.
  - Influence-prioritised replay (CAI-P): 1.5–2.5× faster than prioritised experience replay at 60% success, on par with or better than an energy-based oracle.
  - All combined: FetchPickAndPlace to 95% success in 3000 episodes (supplement, not read).
- FetchRotTable: the object also moves with a periodically rotating table, without the agent's control. CAI-P still helped there.

## Mechanism
C^j(s) = I(S_j′; A | S=s) = E_{a∼π} D_KL[ P(S_j′ | s, a) ‖ P(S_j′ | s) ].

Estimator (eq. 4): Ĉ^j(s) = (1/K) Σ_i D_KL[ p(s_j′ | s, a^(i)) ‖ (1/K) Σ_k p(s_j′ | s, a^(k)) ], with a^(i) drawn iid from a uniform π.
- The transition model is p(s_j′ | s, a) = N(μ_θ(s,a), σ²_θ(s,a)), fitted by Gaussian negative log-likelihood (eq. 5).
- The KL to the Gaussian mixture uses the Durrieu et al. approximation.
- The finite-mixture estimator is a lower bound that converges as K grows (Poole et al.).

Uses:
- bonus r = r_task + λ C^j(s);
- active exploration, choosing argmax_{a∈{a^(1..K)}} D_KL[p(s_j′|s,a) ‖ (1/K)Σ_k p(s_j′|s,a^(k))];
- episode-level replay priority by rank of total influence.

## What it implies for an engine that learns a partner model from closed-loop interaction
1. **A situational contingency map, not one gain.** The partner responds to the agent's face when looking at it, during listening turns, or after the agent's bids, and much less otherwise. CAI's question, "in this situation, does my action change the partner's next state?", is the right shape: C(s) = I(z_{t+τ}; x_t | s_t). The context s must include the partner's own recent face and gaze, and the turn state. This replaces a global R with an R(s) that is near zero in many states. It is also the developmental reading: an infant learns *when* the mother is contingent, not only *whether* she is (see the infant-side notes on Watson's contingency indices).
2. **Their central limitation is our central problem.** CAI is causal only because the state is fully observed: the action's assignment depends only on s, so conditioning on s closes every backdoor. A human partner has hidden state (mood, topic, what they are hearing), and the agent's following makes x depend on that partner's recent behaviour. Fitting p(z′ | s, x) on all closed-loop data then reproduces C13. The authors' own remedy is to train only on samples whose action came from the full-support sampling policy. Applied here, that remedy is the instrument idea:
   - designate probe steps, or the exogenous micro-variation component b, as the "sampling-policy" part of the agent's expression;
   - fit the partner response model on that component only (as a regressor, or by IV);
   - evaluate CAI under the same probe distribution.
   Their pragmatic choice of training on all data "despite potentially being biased" is exactly what an engine that must not mistake following for responsiveness cannot afford.
3. **Proposition 2 lets the probe be small and fixed.** Any full-support probe distribution detects the presence or absence of influence. The agent therefore does not need large or partner-tailored probes to decide *whether* a channel is contingent. It needs only that every expression channel sometimes varies independently of the partner. *How much* influence there is still depends on probe amplitude (see the weak-instrument caveat in hernan-robins-2020-what-if-iv-gmethods.md).
4. **Active probing must be bounded.** Choosing the action with the largest expected effect on the partner is efficient for learning, but used as policy it turns into seeking influence over the partner. Under the project's Principle 6, active probing may at most select *which channel or moment to probe* for information about R. It must have a fixed budget and no reward for the partner's response itself.
5. **The rotating table is the autonomous partner.** FetchRotTable is the closest analogue to a partner who moves by themselves. A good contingency detector must report low influence while the object moves a lot. The entropy baseline confuses movement with control (AP 0.47 vs CAI 0.98 on 1D-Slide), just as a co-occurrence learner confuses a lively partner with a responsive one.

## License
NeurIPS proceedings / arXiv, © the authors. Code exists on the authors' GitHub (not checked).

## Verdict: adopt (CAI as the situational responsiveness measure, estimated only on the exogenous component of the agent's expression)
It gives a principled, situation-dependent contingency measure with a usable estimator, and shows that a full-support probe distribution suffices to detect influence. It states plainly that its causal validity rests on full observability. A human partner violates that, so CAI must be paired with IV or probe-only fitting before it can separate the partner's responsiveness from the agent's own following. Evidence is simulated robotics only.
