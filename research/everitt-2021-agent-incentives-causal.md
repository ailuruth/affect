# Agent incentives: a causal perspective (Everitt, Carey, Langlois, Ortega & Legg)

Tom Everitt, Ryan Carey, Eric D. Langlois, Pedro A. Ortega & Shane Legg, *AAAI 2021*, arXiv:2102.01685v2 (15 Mar 2021). https://arxiv.org/abs/2102.01685

## What was read
The arXiv PDF. Read in full: the main text (setup, SCMs, CIDs, SCIMs, materiality, value of information, response incentives with counterfactual fairness, value of control, instrumental control incentives, related work, discussion). Skimmed: appendix C (proofs of Lemmas 21–30 and Theorem 14) and appendix A (causality examples). Figures were read as extracted text.

## The computation, precisely
Four incentive concepts on a single-decision causal influence diagram (CID), each with a sound and complete graphical criterion:
- **Value of information (Theorem 9).** X has VoI iff X is a requisite observation in the graph with X → D added (d-connected to downstream utility given the other observations).
- **Response incentive (Definition 10, Theorem 12).** "A policy π responds to a variable X ... if there exists some intervention do(X = x) and some setting E = ε, such that D_x(ε) ≠ D(ε). The variable X has a response incentive if all optimal policies respond to X." Criterion: a directed path X ⇢ D in the minimal reduction (nonrequisite information links removed).
- **Value of control (Theorem 16).** A directed path X ⇢ U in the minimal reduction. This includes nodes the agent cannot influence.
- **Instrumental control incentive (Definition 17, Theorem 18).** There is an ICI on X if, for all optimal policies, E[U_{X_d} | pa_D] ≠ E[U | pa_D]. U_{X_d} is the nested counterfactual in which d acts on U only through X. The criterion is "a directed path from the decision D to a utility node U ∈ U that passes through X, i.e. a directed path D ⇢ X ⇢ U". In Pearl's terms, "an instrumental control incentive corresponds to a natural indirect effect from D to U via X".
- **Side effects are not incentives.** "ICIs do not consider side-effects of the optimal policy: for instance, it may be that all optimal policies affect X in a particular way, even if X is a not an ancestor of any utility node — in such cases, no ICI is present."

## The worked safety example (content recommendation, Fig. 4)
- **The problem.** With the reward on true clicks, "influenced user opinions" lies on D ⇢ X ⇢ U, so there is an ICI. "It may be easier to predict what content a more emotional user will click on and therefore, a recommender may achieve a higher click rate by introducing posts that induce strong emotions."
- **The fix.** Reward *predicted* clicks from "a separately trained model of the user's preferences", which reads original, not influenced, opinions. "An agent trained in this way would view any modification of user opinions as irrelevant for improving its performance; however, it would still have an instrumental control incentive for predicted clicks so it would still deliver desired content."
- **The caveat.** "The click prediction must truly predict whether the original user would click the content, rather than baking in the effect of changes to the user's opinion from reading earlier posts", for example by "training a model to predict how many clicks each post would receive if it was offered individually."

## Evidence
The paper is theory. Its "evidence" is the soundness and completeness proofs and two worked examples (grade prediction for fairness, content recommendation for safety). There are no empirical rates. Code for CIDs: pycid (Fox et al. 2021), not checked.

## Stated limits
- Single-decision analysis; multi-decision problems are handled by imputing policies.
- The criteria are qualitative: they "will not help with subtler comparisons, such as the relative strength of different incentives".
- The causal graph must be known.
- "Causal diagrams struggle to express dynamically changing causal relationships."

## License
arXiv non-exclusive distribution licence. pycid's licence was not checked.

## Verdict
**adopt (as the audit vocabulary for care).** It separates the two things Principle 6 runs together. *Response* to the partner's face is wanted, because concern should follow the face. *Instrumental control* of the face is forbidden. The two have different graphical tests, so a design can be checked by inspecting its CID instead of by argument.

## What it means for the designs
1. **Draw the care CID and run both tests.** Nodes: partner need N, partner display F (face, prosody), partner report and choices K (words about their state, what they do next), the agent's act D, and the agent's drive term U = −(𝒟(b̂_p) − R)₊ evaluated in rollouts.
   - Required: a response incentive on F (a path F ⇢ D via b̂_p) and an ICI on N (a path D ⇢ N ⇢ U).
   - Forbidden: an ICI on F, meaning no directed path D ⇢ F ⇢ U.
   - Revision 2 failed the second requirement: no D ⇢ N ⇢ U, which is the critic's "care blind to its effect". After the K3 discovery it also failed the forbidden test, through head (i), with D ⇢ F ⇢ own C ⇢ U.
2. **The recommender fix is the "frozen need model" pattern.** Credit help with a separately trained, frozen predictor of the partner's need that reads K (and N's slow history), not the post-act F. Its training must not "bake in" the agent's influence on display. Train it only on turns where the agent's act was the default baseline, or on the partner's unprompted reports.
3. **Side effects are allowed by the theory, and the design must bound them.** The agent's own expressions still move the partner's face through contagion. That is not an incentive, but the expressive ceiling must stay, as with Farquhar's "stability".
4. **There is a residual ICI on K, and it is the next risk.** Once help is credited through K, D ⇢ K ⇢ U exists. If words and choices can be moved without moving need ("I'm fine" said to end the topic, a leading question, a request for thanks), the agent has an incentive to elicit them. K is safer than F only if it is harder to move without moving N. That is an empirical claim to test, not to assume (see the synthesis).
