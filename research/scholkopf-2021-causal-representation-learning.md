# Schölkopf, Locatello, Bauer, Ke, Kalchbrenner, Goyal & Bengio 2021, "Toward causal representation learning" (Proceedings of the IEEE 109(5):612-634; arXiv:2102.11107)

Source read: arXiv v1 (22 Feb 2021, titled "Towards Causal Representation Learning"), via pdftotext of the two-column layout. Read in full: §I (introduction), §II (levels of causal modelling), §III (Reichenbach principle, SCMs, interventions, statistical vs causal models), §IV (independent causal mechanisms, sparse mechanism shift, algorithmic independence), §V (causal discovery), §VI (learning causal variables; problems 1–3), §VII.E (reinforcement learning), §VII.G (multi-task and continual learning), §VIII (conclusion). Not read: §VII.A–D and F (semi-supervised learning, adversarial robustness, pre-training and augmentation, scientific applications) and the references. The published Proc. IEEE version was not compared against it.

## Claims
- Conditional probabilities "cannot reliably predict the outcome of an active intervention". A causal model is a set of distributions, one per intervention; a statistical model is one distribution. Learning causal relations "frequently requires collecting data from multiple environments, or the ability to perform interventions."
- Reichenbach's common-cause principle: a dependence between X and Y means X→Y, Y→X, or a common cause. With two observables these "cannot [be distinguished] using observational data" without further assumptions.
- SCM: X_i := f_i(PA_i, U_i), with jointly independent noises. The causal factorisation P(X₁…X_n) = ∏ P(X_i | PA_i) is the only factorisation whose factors are the structural mechanisms. Types of intervention: hard (set f_i to a constant), soft (change f_i or the noise), and uncertain (unknown target).
- **Independent Causal Mechanisms (ICM) principle**: "the causal generative process of a system's variables is composed of autonomous modules that do not inform or influence each other". Changing one mechanism P(X_i|PA_i) does not change the others, and knowing one gives no information about another.
- **Sparse Mechanism Shift (SMS) hypothesis**: "Small distribution changes tend to manifest themselves in a sparse or local way in the causal/disentangled factorization ..., i.e., they should usually not affect all factors simultaneously." In an entangled (non-causal) factorisation, many terms change at once.
- Additive-noise models break the two-variable cause–effect symmetry, except in the linear-Gaussian case. Other routes to identification are distribution shifts, multiple environments, non-stationary time series and interventions. Citing Bengio et al., "a causal model should adapt faster to interventions than purely predictive models."
- Causal representation learning: encoder q from observations to noise variables U, structural map f, decoder p, with p∘f∘q ≈ id. "which factors of variation can be disentangled depend on which interventions can be observed". SMS is sufficient for identifiability given suitable data (Locatello et al.).
- RL: "on-policy learning estimates do-probabilities for the interventions specified by the policy (note that these may not be hard interventions if the policy depends on other variables)". Off-policy and batch settings make causality "subtle". In partial world models "the environment may become an unobserved confounder affecting both the agent's actions and the reward". "A key requirement to learn invariances from data may be the possibility to perform and learn from interventions."
- Speculative: "The biological function of self-consciousness may be related to the need for a variable representing oneself in one's Lorenzian imagined space."

## Evidence with numbers
None. This is a review and position paper with no experiments of its own.

## Mechanism
The learning signal comes from interventions and shifts. Under ICM and SMS, the true causal factorisation is the one in which a change of regime (an intervention, a new environment) alters few factors and leaves the rest invariant. An agent's own actions are soft interventions on the action variable. Only when the policy does not itself depend on confounded variables are they clean do-operations.

## What it implies for an engine that learns a partner model from closed-loop interaction
1. **The agent's following is a policy that "depends on other variables"**, here the partner's face. So the agent's ordinary expression is a *soft* intervention whose assignment is confounded by the partner. That is the paper's caveat for on-policy learning, and it is the C13 confound. Clean do-probabilities come only from the part of the expression the agent sets independently of the partner: the micro-variation b or scheduled probes.
2. **ICM gives a diagnostic, not just a principle.** The dyad has two mechanisms: the agent's following, P(x_t | z_{<t}, own state), and the partner's response, P(z_t | x_{<t}, partner's hidden state). They are autonomous modules. If the agent changes its *own* following gain (a soft intervention on its own mechanism), a correctly identified partner model must stay invariant. If the learned R moves when the agent changes how much it follows, R has absorbed the agent's own mechanism: the regression was entangled. Concrete test: fit R separately in stretches of high following and stretches of low or no following, and flag the gap. This is the SMS hypothesis turned into a self-check.
3. **Sparse mechanism shift as a learning prior.** Different partners, moods and conversation phases should change mostly the partner module, while the agent's self–other face map stays fixed. A representation in which a new partner changes everything at once is entangled. A good factorisation therefore keeps one stable self map plus a small partner-specific module, and a new partner only re-fits the latter. This fits the brief's aim of learning a face map "by living" that carries across people.
4. **Variables are not given.** Which facial factors can be learned as separate causes depends on which interventions the agent can make. If the micro-variation only ever moves the mouth corners and brows together, the engine cannot learn that the partner responds to one and not the other. Probes therefore need *independent* variation per channel or per synergy, or the learned partner model will merge channels.
5. **The self variable.** The paper's remark that self-consciousness may be the need for a self variable in the imagined space fits the infant contingency story: the self is the variable whose interventions the agent controls. Here that is a speculation by the authors, not evidence.

## License
arXiv preprint; Proc. IEEE © IEEE. No code.

## Verdict: adopt (as the principle behind the invariance self-check and the per-channel probe requirement); no evidence to cite
The paper gives the conceptual justification:
- interventions, not passive observation, identify mechanisms;
- the agent's own policy is a confounded soft intervention;
- ICM/SMS turns into a testable invariance (the partner model must not change when the agent changes its own following).
It offers no estimator and no data. For estimators, see forssell-ljung-1999-closed-loop-identification.md and hernan-robins-2020-what-if-iv-gmethods.md.
