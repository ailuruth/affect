# Moerland, Broekens & Jonker 2018, "Emotion in reinforcement learning agents and robots: a survey"

Machine Learning 107(2):443-480, 2018, doi:10.1007/s10994-017-5666-0. Preprint arXiv:1705.05172.

Source read: the arXiv v1 preprint (15 May 2017, 36 pages of text plus references), read in full, including Tables 1-10 and the discussion. The published journal version was not read; numbering and some wording may differ from it.

## Claims
- First survey of emotion models inside RL agents (agent emotion, not recognition of human emotion). A Google Scholar search plus citation chasing gave 52 papers, tabulated in Tables 9 and 10 (43 rows, because some rows merge a group's papers).
- Emotion in this literature is "hooked on characteristics of the MDP" (value, transition, reward), not learned. The authors say so in the introduction: the topic "does not imply the agent should 'learn its emotions'".
- Three elicitation routes are useful and cover different aspects: homeostasis covers resource status, appraisal covers model status, value/reward covers the learning process. Hard-wired elicitation is "least useful ... by definition hand-crafted to the task".
- Emotion has been made to act on every node of the RL loop: reward, state, learning parameters, action selection, or nothing (epiphenomenon).
- The field's evaluation is weak: every paper builds its own scenario, no scenario was ever reproduced by another group, implementations are often under-specified, and questionnaire results are sometimes reported for a subset of items.
- Future direction named by the authors: integrate all aspects into one system, "potentially taking a fully learned approach", where emotion-like nodes are trained for function and characterized afterwards (Williams et al. 2015 is the model).

## Mechanism (the taxonomy, equations as given)
Framework: motivated RL with an internal Critic (Chentanez, Barto & Singh 2004). MDP {S, A, T, r, γ}; extrinsic reward depends on state content, intrinsic reward depends only on history g and learned model M.

Elicitation (Section 4):
- Homeostasis / extrinsic. Variables h_i,t with set points h*_i; simple dynamics h_i,t+1 = h_i,t + ψ(s,a) on consumption, h_i,t − ε otherwise (eq. 5). Drive D_t = Σ θ_i |h*_i − h_i,t| (eq. 6; any metric allowed); weights θ_i may depend on level and an online-estimated priority (Konidaris & Barto 2006). Well-being W_t = K − D_t (eq. 7). Emotions are either read from subsets of variables (Gadanho & Hallam: happiness from decreasing hunger, fear from collisions) or from W and its change (Salichs & Malfaz; Cos et al. "hedonic value"). Table 2 lists the usual variables: energy, water, body integrity, activity, sleep, and once (Salichs & Malfaz 2012) social interaction / loneliness. This is the same drive-reduction scheme as keramati-gutkin-2014-homeostatic-rl.md; see that note rather than repeating it.
- Appraisal / intrinsic. ζ_j = f_j(g, M) (eq. 8): relevance 1/(1+d̂(s, goal)) (eq. 9), recency 1 − 1/c(s) (eq. 10), model uncertainty as summed KL between ensemble transition models (eq. 11), novelty as nearest L1 distance to history (eq. 12), curiosity as KL between transition-model posteriors before and after an update (eq. 13, Houthooft et al. VIME). Table 4 shows the same appraisal name implemented in incompatible ways across six papers (e.g. "control" from transition entropy, visit counts, planning distance or success ratio). The authors call this the field's "fundamental challenge": no accepted translation of appraisal concepts into maths.
- Value / reward. Emotion as Q-value (Bozinovski), worst historical Q as fear (Salichs & Malfaz), positive/negative TD as joy/distress (eq. 14; Jacobs et al., Moerland et al. 2016), hope/fear as anticipated TD from forward simulation, valence as short- vs long-term average reward (Broekens; Schweighofer & Doya).
- Hard-wired. Direct rules from sensors, fuzzy maps, or a recognized human emotion (Hasson et al. 2011 face recognition; Kubota speech; Ficocelli; Hoey) copied into the agent's state.

Type (Section 5): mostly categorical (joy in 18 papers, sadness 13, fear 14, anger 11 in Table 6); dimensional much rarer (valence in 10 papers, arousal 6, control 1 in Table 8).

Function (Section 6):
- Reward modification, always additive: r_t = r̃_t + r^Δ_t (eq. 15). Homeostatic version r^Δ = W_t − W_{t−1} = D_{t−1} − D_t (eq. 16), which gives no reward for food when sated. Appraisal version r^Δ = Σ φ_j ζ_j(g) (eq. 17), usually without a difference term, so it never satiates.
- State modification: Q(s, a, e), emotion-specific value functions (Maggie robot: fear replaces the dominant drive).
- Meta-learning: Doya's mapping (dopamine-TD, serotonin-γ, noradrenaline-β, acetylcholine-α) used by Shi et al. (joy→δ, anger→β, fear→α, relief→γ) and von Haugwitz et al.
- Action selection: valence tunes Boltzmann temperature or simulation depth (Broekens), frustration switches value functions.
- Epiphenomenon: emotion computed and displayed, no effect on learning (10 of 43 rows in Table 9).

Evaluation (Section 7): embodiments are single agent, multiple agents, screen agent, simulated robot, real robot; scenarios are mostly self-built gridworld navigation and multi-resource tasks; criteria are learning efficiency, emotion dynamics (match to psychology qualitatively) and HRI questionnaires.

## Evidence with numbers (my counts from Tables 9-10, 43 rows)
- Embodiment: 13 of 43 rows used a real robot (one of these also simulated). The rest are gridworlds, abstract agents, multi-agent simulations, simulated robots, one screen agent, one purely theoretical model.
- Criterion: learning efficiency 26 rows, emotion dynamics 15, HRI questionnaire 4 (Kim & Kwon 2010, El-Nasr 2000, Ficocelli 2015, Shibata 1997), none 3. Several rows have two criteria.
- Human interaction of any kind: 9 rows (counting Blanchard & Cañamero 2005, whose physical human interaction is named in the text, not the table). Long-term or multi-session interaction: none reported in the table.
- Learned (not hand-specified) emotion connections: 2 rows (Williams et al. 2015; Sequeira et al. 2014 via genetic programming). Everything else hand-wires elicitation.
- "Ablation": the only form present is a comparison against a non-emotional baseline, and only in learning-efficiency papers ("many authors ... do compare"). No row reports removing one emotion component at a time and predicting the specific behavioural change, except Williams et al. (fear, surprise and happiness enabled separately on a real robot). Hogewoning et al. 2007, the one attempt to combine two earlier mechanisms, could not improve on either.
- Reproduction: "We have not encountered any (emotional) scenario being reproduced by other researchers."

## Failure modes
- Assembled, not derived. The survey's own framing is a menu: pick a function, then work backwards to a type and an elicitation (its "advice for implementation"). Single emotions get different elicitation routes in different papers (Table 7: anger from hunger, from non-progress, from falling reward). There is no single objective from which several functions follow; the authors list integration as the open problem.
- Hand-named emotions. Almost every system names its emotion variables (joy, fear, hope) and wires them; Principle 2 forbids exactly this. Even the one "fully learned" system (Williams) labels its two nodes "happy" and "fear" after the fact, which is acceptable only as a read-out.
- Classifier input. The hard-wired route that copies a recognized human emotion (Hasson et al. via facial expression recognition, Ficocelli, Hoey) is the Principle 1 violation; the authors themselves rate hard-wired elicitation least useful.
- Non-satiating appraisal reward. Eq. 17 adds novelty or relevance bonuses with no homeostatic difference term, so they never satiate. This is the curiosity-as-unbounded-reward pattern Principle 6 rules out; the homeostatic eq. 16 is the satiable one.
- Persistence. Internal state rarely outlives an episode; emotion is mostly a function of the current TD, value or homeostatic level. The exceptions are slow traces such as average-reward valence. No system in the tables persists state across sessions.
- Evaluation. Toy worlds built by each author, no shared benchmark, qualitative "plausible dynamics" claims, questionnaires as the only social evidence.

## License
Springer journal article; arXiv preprint under the arXiv non-exclusive licence. No code.

## Runs on this Mac without a GPU?
Not applicable (survey).

## Verdict: adopt (as the map of the prior design space and as the documented baseline of evaluation practice to exceed); reject every surveyed mechanism as a component unless it falls out of the core.

## What it implies for this engine
- The brief's Principle 10 claim ("assemblies without one principle") is confirmed for the whole emotion-RL literature to 2017 by the field's own survey: the taxonomy is a list of places to bolt an emotion onto an RL loop, and the authors name integration under one learned system as the unsolved future.
- Of the four elicitation routes, only two survive Principles 1, 2 and 6 as derivations rather than parts: homeostatic drive reduction (eq. 16, satiable, see yoshida-sprekeler-gutkin-2025-hrrl.md) and model-based quantities such as expected TD or model uncertainty, if they come out of the core's objective (cf. hesp-2021-deeply-felt-affect.md, where valence is a change in policy confidence, not set). Hard-wired and recognized-human-emotion routes are excluded by Principle 1.
- The four functions (reward, state, learning parameters, action selection) should not be four mechanisms. A single core should make one latent state do all four, and the ablation predictions should say which behaviour each function's removal changes. This is a concrete checklist for the candidate foundations: does the candidate's state change reward (through drive), representation, learning rate or precision, and policy temperature, all from one equation?
- The "control" appraisal is implemented five incompatible ways (Table 4). Any controllability quantity in the engine must be defined by the core (for example as policy-to-outcome information) and not borrowed by name.
- Evaluation bar to beat, stated in the survey's own numbers: 4 of 43 rows used human-rated interaction, none long-term, none reproduced, and almost none ran component ablations. S5 and S6 (two-way contagion measured on the human; months of living with restarts) would be outside everything the survey covers.
- Williams et al. 2015 (learned nodes with post-hoc labels) is the nearest precedent to Principle 2 in this literature and worth a separate read if the engine needs a precedent for post-hoc naming.
