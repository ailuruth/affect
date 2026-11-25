# Huys & Dayan 2009: A Bayesian formulation of behavioral control

Citation: Q. J. M. Huys, P. Dayan. *Cognition* 113(3): 314–328, 2009. doi:10.1016/j.cognition.2009.01.008. PMID 19285311.

Source read: the accepted "article in press" PDF hosted on Dayan's Gatsby publications page (gatsby.ucl.ac.uk/~dayan/papers/huysdayan09.pdf, 21 pages), extracted with pdftotext. I read the whole main text, Sections 1–6. The text extraction lost the matrix layout of Eq. (2) and some figure panels, so those were rebuilt from the figure captions. Section headers 5.3 and 5.4 are present. The **online supplementary material**, which holds "all the mathematical details" (Supplementary Eqs. 10, 20–23, including the exact prior over χ and the σ parameter), **was not read**. The forms below marked "reconstructed" are rebuilt from the main text.

## Claims
- "There is no fully accepted definition of helplessness or behavioral control", and the engineering notion (a command sequence exists from any state to any other) "has only a loose connection" to it. The proposal: "we formalize controllability in terms of characteristics of prior distributions over affectively charged environments."
- Three nested notions of control, each adding to the last:
  1. **Outcome entropy** of each action, `H = −Σ_o p_o log p_o`. Lower entropy means more control. The number of possible outcomes is used as a proxy.
  2. **Controllably achievable outcomes**: whether *different* actions reliably reach *different* outcomes ("close to the standard engineering notion").
  3. **Controllably achievable reinforcement χ**: "the fraction of reward that can be earned from outcomes that are controlled by any action". The figures label this χ, and the text extraction renders it as "v".
- Controllability lives in the **prior** over action→outcome matrices. It generalizes across environments when they share the hyperparameter. The authors link the sharing to *locus of control*: "The only factor that is really constant across a wide variety of environments is the actor itself."
- Consequences of a high-control prior: larger exploration bonuses, greater "incentive contrast between actions", and higher expected reward. "By making rewards exploitable and punishments avoidable, control renders the world more pleasant, more colorful, and more worth exploring."
- Asymmetry: "only an underestimate of control is problematic; overestimating control, on average, does not hurt performance" (entropy notion). But under notion 2, "an illusion of too much control can be deleterious" (persistent exploration, the optimal action avoided).
- Outcome entropy alone "is not a quantity that is worth inferring and projecting into a new environment"; achievable outcomes and achievable reinforcement are.
- χ is **valence-free** (a normalized fraction of total reinforcement), which explains why helplessness transfers across valence. Inescapable shock impairs appetitive learning, and uncontrollable reward impairs escape (Goodkin 1976; Overmier et al. 1980).
- Tonic dopamine as average-reward opportunity cost (Niv et al.) is linked to χ: "as χ → 1, actions are increasingly worth the effort."

## Evidence
No new data. These are simulations of a single-state "vending machine" with |A| actions, each with L outcomes, and a horizon of D further choices solved by tree search.
- Fig. 3: L = 5, R_o = o. Button k was pressed 3 times (outcome 2 once, outcome 4 twice), and button u was never pressed (Q¹(u) = 3). The exploration bonus Q^D(u) − Q^D(k) is positive only under the high-control prior, for D = 1, 2, 3.
- Eq. (2) example: 5 actions and 5 outcomes. Only outcome 1 (reward 0.3) is controllably achievable, by action 1 with c = 0.8, and outcome 5 carries 0.7. Then χ = 0.24 and Q = [.275 .2 .2 .2 .2] (as extracted). A prior that allows |M| = 5 controllable outcomes ends up *avoiding* the optimal action 1.
- Fig. 8 (learned helplessness): 80 random-action observations in a χ = 0.1 (IS) or χ = 0.9 (ES) environment give posteriors over χ peaked low or high. In a fully controllable test environment (each action a gives outcome o = a, seen 20 times), the IS prior still gives high-entropy predictions, a lower Q for the escape action and smaller Q differences. A larger test shock raises IS escape preference more slowly, which matches the finding that larger shocks lessen helplessness (Jackson, Maier & Rapaport 1978). With prolonged test exposure the groups converge "because there is continued learning about χ".
- Fig. 6 uses σ = 0.05 (defined in the supplementary material). "Smaller σ accentuates the effect."

## Formal model
Quoted or directly given in the main text:
- Posterior over one action's outcome distribution: `p(c^a | n^a) ∝ p(n^a | c^a) p(c^a)` (Eq. 1). n^a holds the outcome counts.
- Value: `Q(a) = Σ_o R_o ∫ dc^a p(c^a | n^a) c^a_o`, plus a decision-tree look-ahead over D choices (which builds in the exploration bonus).
- Notion 2: a binary matrix M with `M_ij = 1` when outcome i is controllably achievable by action j (at most one per column). Then `C_ij = c` and `C_kj = (1−c)/(L−1)` for k ≠ i. A column with no 1 has `C_ij = 1/L`. "|M|/L is the fraction of controllably achievable outcomes."
- Punishment is folded in by `R̃_i = R_i − min_j R_j` (Eq. 3), so avoidance becomes appetitive "safety".
- Helplessness: infer `p(χ | N_env1)`, then predict in env2 with `p(n_{D+1} | N_env2) = ∫ dχ p(n_{D+1} | N_env2, χ) p(χ | N_env1)` (reconstructed from the description of Supplementary Eq. 23).

Reconstructed (exact form in the unread supplementary material):
- `χ = Σ_{o ∈ controllable(M)} R̃_o / Σ_o R̃_o`, with a prior over M and C that favours matrices whose controllable outcomes hold a fraction of reinforcement near χ, at softness σ.

## License
Elsevier copyright. The author-hosted preprint PDF is for reading only. No code.

## Runs on this Mac without a GPU?
Yes for toy sizes. The tree search is exponential in the horizon D, so it does not scale.

## Verdict: adopt (as the formal definition of coping potential as a prior over the agent's action→outcome model)
- It is the only source read so far that turns "coping potential" into a quantity a Bayesian agent infers and generalizes. That quantity is χ, the share of the available value that some action reliably reaches.
- It is valence-free and specific to reinforcement. These are the two properties the engine needs if coping is to be a structural feature of the core and not a named emotion variable.
- Limits the authors state: single state, toy priors, Shannon entropy replaced by set size, no anxiety, no fit to data. They point to correlated Dirichlet processes as the proper generalization.

## What it implies for the engine
- **Coping potential = χ computed over need reduction.** In a satiable core the "reinforcement" is drive reduction, so χ_i = the share of the achievable reduction of need *i* that is reached by outcomes some action reliably produces. This is need-specific without extra machinery, because each need weights outcomes differently (as in Zhang & Berridge's κ_i). An agent can have high χ for warmth and low χ for the partner's attention. That is the structured, need-indexed form the brief asks for, not one gauge.
- **Agency attribution has a place in this prior.** The authors' locus-of-control remark is a statement about *which node of a hierarchical model χ is attached to*: the actor (shared across environments), a particular environment, or (by extension) a particular other agent. Attributing an uncontrollable loss to a partner's policy, and not to the world or to oneself, is a posterior over where χ is low. That is the formal seed of "who caused it". It needs a partner node in the model, which this paper does not have.
- **Passivity, anhedonia and less exploration fall out of one quantity.** Under low χ: (i) expected value falls (the drive looks less reducible), (ii) incentive contrast between actions shrinks (flattened Q), and (iii) exploration bonuses vanish. No "sadness" variable is needed, because these follow from the prior. Adding an action cost (missing here) turns (i)–(iii) into withdrawal, which reconciles this account with Maier & Seligman's default passivity.
- **Wanting vs liking, a caution.** χ reduces how much *instrumental* value is expected. It says nothing about the hedonic readout on contact. Under a low-χ prior a reward that arrives by chance is still consumed and still reduces the drive. It is only "ascribe[d] … to pure chance". The model therefore already separates the expected-and-pursued value from the realized one. This is the instrumental half of the dissociation, not Berridge's cue-triggered half.
- **The illusion-of-control result is a safety constraint.** Overestimating achievable outcomes causes the optimal action to be avoided. The engine's prior over χ should not be wired high "for engagement". Principle 6 already forbids that motive.

## Ablations that separate it
1. **Fix χ at 1** (or remove the hierarchical sharing). Yoked exposure to an uncontrollable loss no longer lowers exploration or incentive contrast in a new context: no transfer.
2. **Untie χ from the actor node, attaching it per environment only.** Helplessness stays local to the context where it was learned (the chronic mild stress versus acute LH contrast the authors draw).
3. **Replace χ by outcome entropy alone (notion 1).** The model then predicts *no* benefit from inferring control (their Fig. 4). Any measured transfer effect would refute this ablated core.
4. **Drop the reinforcement weighting (notion 2 instead of 3).** The agent becomes helpless about outcomes it does not care about as much as about ones it does. Prediction: transfer no longer depends on which need was frustrated.
