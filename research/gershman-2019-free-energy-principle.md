# Gershman 2019, "What does the free energy principle tell us about the brain?" (Neurons, Behavior, Data analysis, and Theory; arXiv 1901.07945v5)

Source read: arXiv PDF v5 (2 Oct 2019) in full via text extraction, sections 1-8 and footnote 1. Reference list skimmed for [42] only. The NBDT journal typeset version was not compared.

## Claims
- Method: "This article systematically deconstructs the assumptions underlying FEP, with the goal of identifying what its distinctive theoretical claims are. ... FEP does not have a fixed set of distinctive claims. Rather, it makes different claims under different sets of assumptions."
- Principle vs theory: as a principle, "its mathematical soundness is sufficient demonstration of its credentials"; as a theory it must be judged by "specific implementations (process models)".
- Unrestricted FEP equals Bayes: "minimizing free energy when the variational family is unrestricted is equivalent to exact Bayesian inference", so its predictions cannot be distinguished "from other asymptotically correct inference algorithms".
- Predictive coding "is not a generic consequence of FEP"; it needs a hierarchical model, a factorized Gaussian family, a quadratic approximation of the free energy around the mode, and gradient descent.
- Active inference equals an information-gain policy only "when the approximate posterior is exact and the observations are deterministic functions of actions. When observations are stochastic, active inference induces a form of risk-aversion".
- The argument most relevant to KL control and valence: the "postulate that the utility of an outcome is equal to its log prior probability" makes planning as inference "a notational variant of Bayesian decision theory, provided the utilities and probabilities coincide (free energy theorists typically stipulate that they coincide)". "why should utility be proportional to probability? Undoubtedly there are high probability events that have low utility (e.g., if you are born into poverty then lacking access to basic goods may be highly probable)." The justification offered by proponents, that "evolution has equipped us with the belief that low utility states are low probability", is reported, not endorsed. Footnote 1: "Technically, utilities can always be formulated as log probabilities. But it is an empirical question whether subjective beliefs and preferences disclosed by behavior coincide".

## Evidence
Conceptual analysis with equations; no data.

## License
arXiv page lists CC BY 4.0. No code.

## Runs on this Mac without a GPU?
n.a.

## Verdict: adopt (as a critique the core must answer)
The argument applies directly to KL and path-integral control. In Todorov's and Kappen's formulations the cost-to-go is a negative log probability (v = −log z; J = −λ log ψ), and the control cost is a KL divergence from passive dynamics. Gershman's point, stated as strongly as he states it: rewriting utility as log probability adds no content. The rewrite is always possible ("Technically, utilities can always be formulated as log probabilities"), so the framework makes distinctive predictions only where the stipulated probabilities and the agent's actual preferences come apart, or where the approximations lead to different algorithms.
- For an affect engine this means "valence is work" or "valence is change in −log z" cannot be the claim. The claim must be a prediction that a plain utility-maximising agent with the same preferences would not make. For example: arousal that scales with noise because of the λ = νR coupling, or the periodic no-gain theorem's consequence for repeated play. Each such prediction should be written before building (Principle 5).
