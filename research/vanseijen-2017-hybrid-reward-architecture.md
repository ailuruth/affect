# van Seijen et al. 2017: Hybrid Reward Architecture for Reinforcement Learning (HRA)

Citation: H. van Seijen, M. Fatemi, J. Romoff, R. Laroche, T. Barnes, J. Tsang. NIPS 2017. arXiv 1706.04208v2.

Source read: the arXiv v2 main text in full (sections 1-4). The supplementary material (Ms. Pac-Man details and exploration heads) was not read. Fruit-task results are given only as curves (Fig. 3). No numbers are quoted for that task.

## Claims
- Decompose the environment reward into components `R_env = Σ_k R_k`. Train one value head per component, off-policy, all from the same experience. Act on `Q_HRA(s, a) = Σ_k Q_k(s, a)`.
- The decomposition pays when components are local: "the decomposition should be such that each reward function is mainly affected by only a small number of state variables." In that case "the corresponding value function can be approximated more easily by a low-dimensional representation".
- The sum of separately optimal component values is not the optimal joint value: "Q*_HRA is different from Q*_env and generally not consistent." The authors accept a "semi-consistent" target in exchange for learnability.

## Evidence
- Fruit collection: a 10×10 grid with 10 possible fruit locations and 5 fruits per episode. HRA uses 10 heads, one per location, on the same network as DQN. "HRA shows a clear performance boost over DQN, even though the network is identical."
  - Giving each head only its relevant features (HRA+1) helps HRA.
  - "Using that same network for DQN results in a decrease in performance."
- Ms. Pac-Man: there is "a separate RL agent associated with each object in the game". Heads are created online: "Whenever the agent finds a pellet at a new location it creates a new head corresponding to the pellet."
  - Final scores, fixed start / random start: HRA 25,304 / 23,770; human 15,693 / 15,375; best previously reported 6,673 / 2,251; A3C (pixels) 2,168 / 626.
  - HRA trained for about 150 million frames; A3C for 800 million.
- The gains rest on heavy domain knowledge:
  - hand-built object channels;
  - pseudo-reward GVFs per map location;
  - per-object weights "set equal to the reward received when the object is eaten";
  - extra exploration heads.
  "All combinations achieved over 10,000 points in training, except the combination with no exploration at all, which … performed very poorly."

## License
- Paper: arXiv (no CC licence stated on the version read).
- Code (fruit task only): github.com/Maluuba/hra. Archived, last pushed 2018. The GitHub licence field reads NOASSERTION. It requires Keras 1.2 with Theano. The README says "the deep RL methods of this code run faster on CPU."

## Runs on this Mac without a GPU?
The fruit task would be cheap on CPU, but the Keras 1.2/Theano stack is obsolete. Re-implementing it in PyTorch is easier than installing it. Not run.

## Verdict: watch (the mechanism is a precedent; the evidence leans on hand-engineering)
- HRA is the strongest precedent for values that range over a growing set of entities. Heads are spawned when a new object is met and summed with weights. That is a "set of needs over entities" in its plainest form.
- The Ms. Pac-Man margin cannot be credited to decomposition alone, because so much domain knowledge was added.

## What it implies for the open question
- Per-entity structure pays when the total objective is approximately a sum of per-entity terms and each term depends on a few features, such as the agent's position relative to that entity.
- It costs optimality wherever entities interact, because the summed heads ignore interactions. Example: eating one pellet changes the route to another. This is the same trade-off Dulberg et al. found with needs.
- For the Bot: per-person or per-topic value heads, created when a new person or topic first appears, are a natural fit to "needs as a set over a learned space."
- Two things must be checked:
  - that the coupled terms (one relationship affecting another) are small;
  - that the summed heads do not learn to chase several people at once. That would be the engagement failure Principle 6 forbids.
