# Majha, Sarkar & Zagami 2019: Categorizing wireheading in partially embedded agents

Citation: Arushi Majha, Sayan Sarkar, Davide Zagami. "Categorizing Wireheading in Partially Embedded Agents." arXiv:1906.09136v1 [cs.AI], 21 Jun 2019. https://arxiv.org/abs/1906.09136

Source read: the full 3-page PDF. It is a short workshop-style paper from the AI Safety Camp. Cited by Metoyer 2026 (research/metoyer-2026-satisfied-not-solving.md) as categorizing wireheading in partially embedded agents.

## Claims
- An agent whose reward, observation and belief machinery sits inside the environment can wirehead through six arrows. It can replace the reward signal (1), the reward mapping R_t (2), the observation signal o_t (3), the observation mapping O_t (4), the belief b_t (5), or the belief-update function B_t (6).
- Rewarding beliefs instead of observations (Hibbard's proposal) does not by itself remove the incentive, because beliefs and the belief update can be tampered with too.
- Definition: a partially embedded agent is "wirehead-vulnerable" if its policy set differs from that of a dualistic agent that cannot reach its internal parts.

## Evidence (quoted from the PDF)
- Observation route: "Since now there is a causal link from observations to rewards, the agent has an incentive to manipulate the observation signal o_t and the observation mapping O_t."
- The closed-eyes case: "imagine a cleaning robot that gets a negative reward for seeing disorder (such as dirt), and zero rewards for seeing no disorder. This agent is incentivized to close its eyes".
- Belief route: "Since there are causal arrows from beliefs to rewards, the agent may have an incentive to manipulate its beliefs to artificially achieve a high reward." And: "it may want to corrupt the belief update subroutine (red arrow labeled with a 6) to always interpret observations as evidence for the most rewarding belief."
- Experiments: AIXIjs gridworlds (N = 7 to 20) with a blue tile that replaces the reward signal, the reward mapping, the observation signal or the observation mapping. The agent wireheads in each case. Results are shown as screenshots only, with no rates or seeds. The authors state that "our agents are bounded in computing power, they don't always identify the opportunity to wirehead".
- Definition 4: a partially embedded agent is wirehead-vulnerable if Π_D(q) ≠ Π_P(q) for each non-simple environment q.

## License
arXiv: CC BY-NC-SA 4.0. Code: an extension of AIXIjs (JavaScript). I did not check the repository or its license.

## Runs on this Mac without a GPU?
AIXIjs is browser JavaScript and should run anywhere. I did not run it.

## Verdict: watch
- The taxonomy is useful. Arrows 5 and 6 (belief and belief-update tampering) name the exposure of model-derived body variables precisely.
- The evidence is qualitative demos with no numbers, and it does not involve homeostatic or satiable rewards. It adds no constraint beyond Everitt et al. 2021 (research/everitt-2021-reward-tampering.md).

## (a) Mechanism
Any agent action with a causal arrow into a node between the world state and the reward: the observation signal or mapping, the belief or belief-update function, or the reward mapping or signal.

## (b) Exposure of the candidates
- The candidates' innate d and f_b close arrows 1 and 2, provided the implementation keeps them out of reach of every learned or selected component.
- Arrows 3 and 4 correspond to priced attention and the cue mask, whenever a body variable is computed from attended cues. This is the "close its eyes" case: attend away from what lowers predictability.
- Arrows 5 and 6 correspond to costate's b_p ("minus the running prediction error of x") and to learning progress (D62). Both are computed from the agent's own learned model F_θ, and its training (including replay) is shaped by the agent's own selections.

## (c) Constraint that would close it
Per the paper's own definition, the agent's policy must equal that of a dualistic agent that cannot reach its internal parts. For this project that means: no action or selection (attention, cue mask, replay, Claude settings) may be a parent of a body-sensing node, of the model that computes a model-derived body variable, or of d. A direct test follows: compute each candidate's choices with those parent links cut, and require them to match.
