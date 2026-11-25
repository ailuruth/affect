# Dulberg, Dubey, Berwian & Cohen 2023: Having "multiple selves" helps learning agents explore and adapt in complex changing worlds

Citation: Z. Dulberg, R. Dubey, I. M. Berwian, J. D. Cohen. *PNAS* 120(28): e2221180120, 2023. doi:10.1073/pnas.2221180120. Full text: PMC10334746. Earlier workshop version: "Modularity benefits reinforcement learning agents with competing homeostatic drives", arXiv 2204.06608 (2022).

Source read: the PNAS main text and Materials and Methods in full, via the Europe PMC full-text XML. I also read the 2022 arXiv version in full. The SI Appendix (Figs. S1-S12, Table S1) was not read. The paper gives no effect sizes in its text: every comparison is shown only in figures, and none are quoted here as numbers.

## Claims
- The paper asks whether several needs should be combined at the level of reward (monolithic) or at the level of action value (modular): "Should these objectives be composed together at the level of reward (monolithic) or at the level of action (modular)?"
- Modular agents (one Q-learner per need, with Q-values summed for action selection) beat a monolithic DQN trained on the scalar HRRL drive-reduction reward. They "a) exhibited a form of exploration that was intrinsic and emergent rather than extrinsically imposed; b) were robust to changes in nonstationary environments, and c) scaled gracefully in their ability to maintain homeostasis as the number of conflicting objectives increased."
- Two mechanisms are proposed.
  - Intrinsic exploration: "exploitation from the perspective of one is exploration from the perspective of others."
  - Factored representation: the monolithic agent must build "a form of conjunctive coding that grows exponentially with the number of resources", while the modular agent uses "a form of compositional coding, that grows only linearly with the number of resources."

## Evidence
- Environment: an 8×8 grid holding N overlaid resource maps (2D Gaussians). The agent sees a 3×3 egocentric slice of every map plus its N internal stats. Each stat decays at a constant rate and rises only from its own resource ("h_i is only affected by acquisition of resource i"). Set points are 5 and stats start at 0. Training is one continuing 30,000-step episode with no resets.
- Monolithic agent: `r_t = D(H_t) − D(H_{t+1})` with `D(H) = (Σ_i |h*_i − h_i|^n)^{1/m}` and `(n, m) = (4, 2)`. The paper states "the constraint n > m > 1 was necessary to be consistent with physiology".
- Modular agent: one DQN per stat with `r_{i,t} = D(h_{i,t}) − D(h_{i,t+1})` and `D(h_i) = |h*_i − h_i|^{n/m}`. The action is `a_t = argmax_a Σ_i Q_i(s, a)` (greatest-mass Q-learning). The number of trainable parameters is matched between the two agents.
- Both agents needed a learned sparse input mask in nonstationary worlds: "learning a sparse attentional mask over the input to each network was required for good performance (SI Appendix, Fig. S12)." Each module learned its own mask, with an L1 penalty on the mask.
- Exploration: ε was annealed over 1, 1k, 5k or 10k steps (N = 50 per agent type). "With only 1 step of annealing, modular agents were already at or near maximal performance", while monolithic agents improved with longer annealing.
- Ablation: "each module could only learn from actions that it would have taken if it had full control". This "substantially impaired the performance of modular agents in the absence of extrinsically imposed exploration". A matched random-skip control on the monolithic agent was "relatively unaffected".
- Nonstationarity: resources moved with Poisson rate λ from 0.001 to 0.02 (N = 100 per agent type at λ = 0.02). "Modular agents were largely impervious to the rate of change". Monolithic agents performed worse, and "performance worsened as resource locations changed more slowly", which the authors attribute to local minima.
- Number of needs: 4 to 8 stats at λ = 0.02. The monolithic agent "exhibited strong sensitivity to the number of objectives". Modular agents held homeostasis "regardless of the number of objectives".
- Where the gap narrows: at λ = 0.001 the difference "was greatest with the least amount of extrinsic exploration … and decreased with longer annealing."

## Caveats the paper states
- The design is one module per resource, and all needs are independent. In the authors' words, "policy modularity may vary with drive independence". They suggest that a hybrid, such as one 3-D component for three correlated drives and 1-D components for the rest, might beat both extremes.
- Arbitration is a plain sum of Q-values. The paper says nothing about winner-take-all arbitration.

## Caveats I add
- The two agents optimise different objectives. The modular reward is additively separable: with n/m = 2 it is the sum of squared deviations. The monolithic drive is not separable. The comparison therefore changes both the architecture and the objective. In particular, the modular agent gives up the cross-need inhibition that Keramati & Gutkin derive from a non-separable drive.
- Exponent convention: this paper uses n > m > 1, as does our Keramati & Gutkin note. Our Yoshida, Sprekeler & Gutkin 2025 note records m > n > 1 from a garbled PDF extraction. Recheck that note before choosing exponents.

## License
- Paper: CC BY-NC-ND 4.0.
- Code: github.com/zdulbz/Multiple-Selves, Apache-2.0. It is PyTorch and falls back to CPU (`"cuda" if torch.cuda.is_available() else "cpu"`). The README says the analyses specific to the paper must be requested from the author.

## Runs on this Mac without a GPU?
Probably yes. The networks are small MLPs on 40-dimensional inputs with 30k steps per run, on the CPU path. Not run. A full sweep of 50-100 seeds per cell would take hours on CPU.

## Verdict: adopt (as the reference experiment for the structured-needs ablation)
This is the cleanest published head-to-head of a scalar drive against need-factored values, with matched parameters, lesions and a sweep over the number of needs. It fits the Principle 5 pattern: the ablation is stated, then run. The modular-assembly framing conflicts with Principle 10, but the conflict goes away if per-need value heads are derived from a single objective that decomposes over needs.

## What it implies for the open question
- Structured needs paid off in this setup when three conditions held together:
  - the needs were independent;
  - the environment was nonstationary;
  - the needs were many (the advantage grew from 4 to 8).
- The payoff came from factoring value learning and exploration, not from the drive itself.
- It shrank in a stationary world with a slow rate of change and plenty of imposed exploration.
- A copy of this test for us: per-entity or per-need value heads against one scalar drive, parameters matched, ε near 0, with the number of people or topics swept and the world made to drift. Predicted outcome: the gap grows with the number of entities, and is larger under *slower* change (the paper: the monolithic agent's "performance worsened as resource locations changed more slowly"). *[corrected 2026-11-25 after VERIFICATION-5]*
- The required learned input masks are a small precedent for need-specific attention. Each need learns which inputs to ignore.
