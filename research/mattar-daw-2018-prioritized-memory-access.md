# Mattar & Daw 2018: prioritized memory access explains planning and hippocampal replay (priority = gain × need)

Mattar, M. G. & Daw, N. D. (2018). "Prioritized memory access explains planning and hippocampal replay." *Nature Neuroscience* 21:1609–1617. doi:10.1038/s41593-018-0232-z. Read as the bioRxiv preprint 10.1101/225664 v4 (posted 20 May 2018, CC-BY-NC-ND): https://www.biorxiv.org/content/10.1101/225664v4. The typeset Nature Neuroscience text (nature.com) and the PMC author manuscript (bot check) were not reachable; the published wording and figures may differ.

**How fully read:** the bioRxiv v4 PDF, read in full on 2026-11-28: abstract, Introduction, Results 2.1–2.6, Discussion, Methods 4.1–4.3 (model, gain and need terms, simulation details, the formal derivation of EVB), with all figure captions. Figures themselves were read by caption only. Reference list and supplementary figures not read.

## What it says
- **Question.** Out of everything stored, which experience should an agent access at each moment, and in what order, to make the best future decisions? Hippocampal replay (forward, reverse, offline during rest or sleep) is the empirical window.
- **Model.** Dyna-style Q-learning. Accessing a memory e_k = (s_k, a_k, r_k, s′_k) performs a Bellman backup of Q(s_k, a_k). Its utility is the expected value of backup, EVB = E_π_new[return] − E_π_old[return].
  - Because a backup changes the policy only at s_k, EVB factors exactly (eq. 13): **EVB(s_k, a_k) = Need(s_k) × Gain(s_k, a_k)**.
  - **Gain** = Σ_a [π_new(a|s_k) − π_old(a|s_k)] q_π_new(s_k, a): how much better the agent will act at s_k because of the update.
  - **Need** = μ_π(s_k) = Σ_i γ^i Pr(S_{t+i} = s_k): the discounted expected number of future visits. It is computed from the successor representation (I − γT)⁻¹ when the agent is in the environment, and from the stationary distribution μT = μ in the sleep simulation, where the agent is elsewhere.
  - A backup with no effect on behaviour has zero utility however often the state will be visited, and a backup at a state never to be visited again has zero utility however large its effect.
  - Simulation settings: softmax β = 5, α = 1, γ = 0.9, reward noise σ = 0.1, 20 planning steps before and after each episode, minimum gain 10⁻¹⁰, all re-computed after every backup.
- **What it reproduces, with no parameter fitting.**
  - Forward replay before a run (need-driven) and reverse replay after reward (gain-driven), as in Diba & Buzsáki 2007.
  - Initiation bias at the agent's location, and over-representation of goals and of the turning points before them.
  - Offline (sleep) replay biased toward the cued, rewarded arm (Ólafsdóttir 2015).
  - **Asymmetric effects of reward change.** More reverse replay after a 4× reward and less after a 0× reward, while forward replay is unchanged (Ambrose 2016).
  - **Aversive outcomes are replayed when they change behaviour.** After a shock at the end of a track, the probability of a backup at the shock zone is 1, against near 0 before. Replay "extending from the animal's position toward" the shock zone, without the animal entering it, was observed by Wu et al. 2017. Learning that a still-best action is slightly worse, or that a bad action is even worse, has zero (or negative) gain and is not replayed.
  - **Familiarity.** Replay events fall from about 2 to 0.8 per trial with experience (gain falls as the task is learned), while the probability that a frequently visited state is included rises (need concentrates).
- **A key distinction they draw.** "Only gain is affected by replay": learning from replayed experience lowers later gain, whereas need changes only with real experience.
- **Against pure prediction-error priority.** Prioritized sweeping (and Schaul-type |TD| priority) backs up any large surprise. Gain × need differs in two ways: it ignores surprises that would not change behaviour, and it adds forward search from the current state.
- **Pathology.** Dysfunction of this selection "may underlie pathologies like rumination and craving".
- **Limitations they state.** Deterministic, stationary grid worlds; gain as defined requires knowing a backup's policy effect *before* doing it, which is unrealistic, so a process model needs approximations (they suggest the myopic value of perfect information). Single scale; episodic and semantic memory not separated.

## What matters for this engine
- **It is the normative account the repo lacked for "what should replay prioritise".** Priority is the product of how much a memory can still improve behaviour (gain) and how likely the situation is to recur (need). Neither factor is valence. Distress enters only through gain: a bad outcome is replayed when, and as long as, replaying it changes what the agent will do.
- **κ_replay = 4 is not gain × need.** It is a fixed function of the stored moment's need load, and it does not fall as the moment is learned. In Mattar & Daw's terms it is a salience heuristic: like prioritized sweeping, but on stakes rather than surprise, and without either a gain or a need factor. The paper's simulations predict exactly what such a weight misses. Once a hard moment has taught what it can, further replay of it has no value, and continued replay is their candidate model of rumination.
- **What carries over to the engine, as constraints on a replacement (new-core-search-16-synthesis.md §1.4).**
  - *Need* should come from how often the context recurs, learned from real experience: in the engine, the same person and topic slot coming back across sessions, which is T-typed.
  - *Gain* should fall with replay itself. The paper's own note that only gain is reduced by replay is what licenses a replay-count decay as the cheapest gain proxy.
  - The exact gain needs a policy-effect estimate that the engine does not have until its world model 𝓜 and draft scorer exist. Even then it must be computed from T-typed targets to keep fix A-iii.
- **Valence asymmetry is allowed, but only through behaviour change.** Bad news that changes nothing is not replayed; bad news that changes what to do is replayed at once and strongly. This is the principled version of "rare distressing moments learned faster" (S48's stated purpose), without the standing 4× weight.
- **The engine's "policy" is mostly not Q-values.** Nightly learners are readers, an expression basis, a display network, a scorer and ω. Gain × need applies most directly to the scorer and initiative (J's choices). For the readers, the analogue of gain is the expected reduction of their own loss, which is closer to Schaul-type priority. That needs the coverage floor (Hayes 2021, Isele & Cosgun).

## Verdict: adopt (as the normative frame for replay priority); watch (the exact gain term, which the engine cannot compute yet)
