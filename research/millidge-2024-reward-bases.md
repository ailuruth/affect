# Millidge, Song, Lak, Walton & Bogacz 2024: Reward Bases, a simple mechanism for adaptive acquisition of multiple reward types

Citation: B. Millidge, Y. Song, A. Lak, M. E. Walton, R. Bogacz. *PLOS Computational Biology* 20(11): e1012580, 2024. doi:10.1371/journal.pcbi.1012580. Full text: PMC11614280. Earlier preprint: "Reward Bases: Instantaneous reward revaluation with temporal difference learning", bioRxiv 10.1101/2022.04.14.488361.

Source read: the full text via the Europe PMC XML, covering the main text, the methods for the room and salt tasks, and the discussion. Figure values were not extracted.

## Claims
- Reward is a need-weighted sum of reward bases: `r(x) = Σ_i m_i r_i(x)`. Here `m_i` is "a motivational drive parameter for each reward basis" (for food, it reflects hunger).
- Learn one TD value per basis, `V_i`. The value under any need vector is then `V = Σ_i m_i V_i`. When needs change, value updates with no new experience of reward.
- TD learning on a single value cannot do this: "TD learning … require[s] an experience of reward to update the value function estimate." Homeostatic RL (Keramati & Gutkin) has the same limitation: "in these models, the agent learns a single overall value function … when the motivation changes, these models require experiencing reward to change the overall value function."
- The model predicts that individual dopamine neurons are tuned to reward type.

## Evidence
- Room task: a 6×6 grid with 3 objects. Each object gives reward 5 in one dimension and −1 in the others, and the valued dimension reverses periodically. Results are over 10 runs.
  - Reward Bases and the successor representation "both achieve approximately equal performances", and both beat TD, "which needs to completely re-learn the value function after each reversal."
  - Memory cost: Reward Bases stores X×N values against X×X for the successor representation, "36 × 3 = 108 while the successor matrix required 36 × 36 = 1296".
- Salt task: the simulation reproduces the rat result in which a salt-paired lever is approached immediately under first-ever sodium depletion. The TD agent "simply predicts that the salt lever will remain aversive".
- Dopamine reanalysis, single primate (Lak et al. data): "7 neurons out of 19 possessed a statistically significant interaction coefficient implying that their response depended on reward type". This was tested against a 1,000-shuffle null. The data set is small and comes from one animal.

## Limits the authors state
- "The Reward Bases method requires that the reward function be expressable as a linear combination of reward basis vectors".
- It "assumes that these reward basis vectors can be specified beforehand".
- Homeostatic RL's nonlinear drive can explain "that deprivation of one need reduces the rewarding value of other outcomes". The linear Reward Bases model cannot.

## License
- Paper: PLOS (CC BY).
- Code and data: github.com/YuhangSong/reward-bases, AGPL-3.0, Python. The README says it is tested on Linux and macOS (Darwin).

## Runs on this Mac without a GPU?
Yes for the simulations: tabular 6×6 grids and a small network. Not run. The AGPL licence would matter only if the code were copied into the engine; re-implementing the idea takes a few lines.

## Verdict: adopt (as the zero-shot revaluation mechanism and its ablation)
- It is the minimal model-free way for a need vector to re-weight learned per-need values instantly.
- It also answers Berridge's "wanting without relearning" critique (see berridge-2004-motivation-concepts.md) with arithmetic.
- It does not by itself give satiety or overshoot penalties, and it loses the cross-need inhibition of a nonlinear drive. Pair it with a drive whose gradient supplies `m_i`. In Keramati & Gutkin, the reward is approximately `−K·∇D`, so `m_i ≈ ∂D/∂h_i` is the natural weight.

## What it implies for the open question
- Structured needs give a measurable advantage exactly when the need state changes faster than values can be relearned:
  - reversals;
  - first-ever deprivation states;
  - a new person mattering more after a long silence.
- A scalar learned value must re-experience reward to adapt. Per-need values recombined by the current need vector adapt at once. In the room task the advantage over TD is large, and memory grows linearly in the number of needs.
- An ablation prediction for the Bot: collapse the per-need values into one value and the Bot should no longer change its approach to a person or topic immediately when the corresponding need changes. It should need fresh contact first.
