# Free Energy in a Circumplex Model of Emotion (Pattisapu, Verbelen, Pitliya, Kiefer & Albarracin)

Citation: C. Pattisapu, T. Verbelen, R. J. Pitliya, A. B. Kiefer, M. Albarracin. "Free Energy in a Circumplex Model of Emotion." arXiv:2407.02474 (2024); IWAI 2024 workshop paper.

Source read: arXiv PDF, text-extracted, read in full (introduction and prior active-inference accounts, the valence and arousal definitions, polar transform, the search-agent generative model, the five scenarios, results and discussion). Figures not seen; trajectories quoted from Table 2 and the text.

Read in place of the unreachable sources on affect as error dynamics: Kiverstein, Miller & Rietveld 2019 (*Synthese*, "The feeling of grip"; Springer, the UvA repository and CORE are refused or unresolvable from this session) and Van de Cruys 2017 ("Affective value in the predictive mind", open-mind.net refused). Nothing below rests on them.

## Key claims
- **Two read-outs from one active-inference agent, no labels inside the agent:**
  - valence V = U − EU, with utility U = log P(o_t | C) (log prior preference of the observed outcome) and expected utility EU = E_{Q(o_t | s_{t−1}, π)}[log P(o_t | C)]: "better than expected" outcomes are positive (compared to reward prediction error);
  - arousal A = H[Q(s | o)], the entropy of the posterior over states: uncertainty, explicitly not valenced.
  - Polar transform: radius √(V² + A²) as intensity, angle tan⁻¹(A/V) mapped to circumplex labels **by the authors, after the fact**.
- **Simulation:** a pymdp-style agent on a 13-node graph searching for an object (visibility likelihood 0.95), preference for "object visible", five scenarios varying presence and prior (uniform, correct, incorrect, "maybe here" with an absent state, "definitely here" without one).
  - Correct precise prior: "calm" throughout; uniform prior: high-uncertainty start, then low;
  - incorrect precise prior: strongly negative and high-uncertainty on violation, then a near-180° swing to positive/low-uncertainty when found;
  - object absent with an "absent" state available: ends low-uncertainty, neutral; without it: cycles between negative high- and negative low-uncertainty regions, with peaks late (steps 26/43 and 20/40), ending more uncertain.
- **Admitted limits:** simple scenarios, narrow range, "our findings are not benchmarked against human data … we rely on face validity".

## What it means for the engine
1. **Affect-like coordinates read from objective terms, not set.** Both read-outs are quantities the objective already computes (a preference-prediction error and a posterior entropy). This fits Principle 2's "read out, not set" and complements Joffily & Coricelli (−dF/dt) and Hesp et al. (affective charge), both already adopted.
2. **The structural result worth keeping: model structure, not the read-out, decides whether the agent can settle.** The agent without an "absent" state cannot reduce its uncertainty and cycles in negative regions. In the engine this says that a latent unable to represent "this need cannot be met here" gives persistent negative read-outs, the same fixed point pass 6 found in the efficacy level.
3. **Hazard for the dyad.** U is a log preference over outcomes. If outcomes include the partner's face, V is the partner's reaction against the agent's expectation of it: the partner's approval as a learning signal, in exactly the form Sharma et al. measured. U must be defined only over the agent's own body outcomes.
4. **Labels.** The circumplex names are attached by the observer; the agent holds none. The engine would keep the two read-outs as numbers for evaluation only.

## Verdict
- **background (read-out definitions; one structural observation).** Toy, face-valid only, no data; the read-outs are standard active-inference quantities renamed.
