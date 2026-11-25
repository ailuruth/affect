# Schaul, Quan, Antonoglou & Silver 2016, "Prioritized Experience Replay" (ICLR 2016; arXiv 1511.05952v4)

Source read: the arXiv PDF v4 (25 Feb 2016), main text sections 1-7 in full, plus Appendix A (prioritization variants). Read on 2026-11-24. Not read: Appendix B (experimental details, hyperparameter tables, per-game score Tables 6-7, Figures 7-12) beyond the cross-references in the main text, and the reference list.

## Claims
- The priority is the magnitude of the TD error, used as a proxy for "expected learning progress": "a reasonable proxy is the magnitude of a transition's TD error δ, which indicates how 'surprising' or unexpected the transition is". New transitions get maximal priority "to guarantee that all experience is seen at least once".
- Greedy prioritization is replaced by stochastic sampling: "P(i) = p_i^α / Σ_k p_k^α", "with α = 0 corresponding to the uniform case". There are two variants. Proportional: "p_i = |δ_i| + ε". Rank-based: "p_i = 1/rank(i)", which is "likely to be more robust, as it is insensitive to outliers".
- Importance-sampling correction: "w_i = (1/N · 1/P(i))^β", which "fully compensates for the non-uniform probabilities P(i) if β = 1". The weights are normalized "by 1/max_i w_i so that they only scale the update downwards". β is annealed linearly "from its initial value β0 to 1", because "the unbiased nature of the updates is most important near convergence at the end of training".
- Reported gains: DQN with prioritized replay outperforms uniform DQN "on 41 out of 49 games". Against Double DQN, "the median performance across 57 games increased from 111% to 128%, and the mean performance from 418% to 551%". "on aggregate, learning is twice as fast".

## Evidence
- Atari 2600, human-start evaluation, with "a single hyperparameter setting across all games". Hyperparameters: "α = 0.7, β0 = 0.5 for the rank-based variant and α = 0.6, β0 = 0.4 for the proportional variant", from "a coarse grid search (evaluated on a subset of 8 games)". The step size was "reduced ... by a factor 4". The baseline replay memory retains "the last 10^6 transitions"; minibatches are "32 transitions"; "all experience is replayed 8 times on average".
- Table 1: DQN median normalized score "48%" → "106%" (rank-based). Double DQN median "111%" → "113%" (rank-based) and "128%" (proportional); mean "418%" → "454%" and "551%". Games above human: "30" → "33". The mean is flagged as "not a very reliable metric because a single game (Video Pinball) has a dominant contribution".
- Learning speed: the baseline's median is matched at "47% and 38% of total training time" (rank-based and proportional respectively).
- Blind Cliffwalk toy: a random policy reaches the reward with probability "2^−n"; an oracle ordering gives "exponential speed-ups over uniform choice".
- The two variants perform similarly, which the authors suspect is "due to the heavy use of clipping (of rewards and TD-errors)".
- Stated weaknesses of |δ|: "it ignores inherent stochasticity in rewards or transitions ... it is problematic when there are unlearnable transitions". Asymmetric (sign-dependent) priorities "were inconclusive" in preliminary experiments. The authors note rodent replay favours reward and "high magnitude TD error".
- Class-imbalanced MNIST, "removed 99% of the samples for digits 0, 1, 2, 3, 4": prioritized sampling "outperforms the uninformed uniform baseline". Reported as a "preliminary experiment".

## License
arXiv non-exclusive distribution license (arxiv.org/licenses/nonexclusive-distrib/1.0). The paper publishes no code; Algorithm 1 is given in full, along with the sum-tree and rank-segment sampling schemes.

## Runs on this Mac without a GPU?
Yes, for our scale. This is our judgment, not the paper's. The mechanism is a sum-tree over a buffer: O(log N) updates, "O(1)" maximum lookup for the greedy heap version. That is trivial on a CPU for a small agent. The paper's Atari-scale DQN experiments are a different matter.

## Verdict: adopt (the mechanism), watch (the |TD| priority for an affect agent)
- For (d), prioritized replay: adopt proportional prioritization with ε, a max-priority insert for new transitions, and IS weights annealed to β = 1. It is simple, documented and cheap.
- Caution for our use. Replaying by |δ| changes the data distribution the value function sees. Without β → 1, it "changes the solution that the estimates will converge to". If ∂V/∂H is broadcast as affect, a biased V gives a biased costate. So keep the IS correction fully on whenever the broadcast signal is read.
- For a homeostatic agent, |δ| peaks at surprising need changes: the unexpected arrival of food, or the omission of food after a cue (Chen 2015's relapse case). That makes prioritized replay a plausible way to learn the anticipatory drop quickly. This is our inference, not the paper's.
- Watch the authors' own warning about "unlearnable transitions". A noisy body sensor would keep |δ| high and hog replay. The variants they suggest (the change in |δ|, or a staleness bonus) are untested beyond "preliminary experiments".
