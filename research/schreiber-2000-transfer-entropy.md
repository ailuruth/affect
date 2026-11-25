# Schreiber 2000, "Measuring Information Transfer" (Phys Rev Lett 85(2):461-464; arXiv:nlin/0001042)

Source read: arXiv v1 (19 Jan 2000), 4 pages, in full: abstract, information-theory background, the definition (Eq. 4), the estimator, the three examples (tent-map lattice, Ulam lattice, heart/breath series), the conclusion and the references. The published PRL version was not compared against it.

## Claims
- Problem: time-delayed mutual information "does not explicitly distinguish information that is actually exchanged from that due to the response to a common input signal or history."
- Null hypothesis: the generalised Markov property p(i_{n+1} | i_n^(k)) = p(i_{n+1} | i_n^(k), j_n^(l)). "In the absence of information flow from J to I, the state of J has no influence on the transition probabilities on system I."
- Definition (Eq. 4), the Kullback entropy of that assumption: T_{J→I} = Σ p(i_{n+1}, i_n^(k), j_n^(l)) log [ p(i_{n+1} | i_n^(k), j_n^(l)) / p(i_{n+1} | i_n^(k)) ]. Here i_n^(k) = (i_n, ..., i_{n-k+1}) is a length-k history. "The most natural choices for l are l = k or l = 1. Usually, the latter is preferable for computational reasons."
- Direction: "T_{J→I} is now explicitly non-symmetric since it measures the degree of dependence of I on J and not vice versa."
- Common drivers: "the influence of a known common driving force Z may be excluded by conditioning the probabilities under the logarithm to z_n as well." Only a known Z can be excluded this way.
- Conclusion: transfer entropy "is able to detect the directed exchange of information between two systems. Unlike mutual information, it is designed to ignore static correlations due to the common history or common input signals."

## Evidence
- Conditions: I is assumed "a stationary Markov process of order k". For continuous systems coarse-grained at resolution ε, "the limit lim_{ε→0} T_{Y→X}(ε) is finite and independent of the partition, except for the case of deterministic coupling, when T_{Y→X}(ε) diverges as ε → 0." In practice "Either one can study transfer entropy as a function of the resolution, or one can fix a resolution".
- Estimator: kernel estimation with a step kernel Θ at radius r; "Dynamically correlated pairs should be excluded as usual". With correlation integrals at q = 2, "we would have to give up positivity".
- Tent-map lattice (binary partition, k = l = 1): T_{I^{m-1}→I^m} = α²ε²/ln(2) + O(ε⁴), with fitted "α = 0.77", while the reverse direction and the time-delayed MI are "consistent with zero". 100 maps, "10 runs of 10^5 iterates after 10^5 transients".
- Ulam lattice: near ε = 0.18 (a period-two state) "the mutual information is found to be 1 bit ... although information is neither produced nor exchanged", while "The transfer entropy finds a zero rate of information transport, as desired."
- Heart rate vs breath rate (sleep apnea, Santa Fe 1991 data set B, 2 Hz): TE indicates "a stronger flow of information from the heart rate to the breath rate than vice versa". The author adds: "Certainly, both signals could instead be responding to a common external trigger." For small r "the curves deflect down to zero due to the finite sample size."

## License
arXiv "assumed" license for 1991-2003 submissions (arxiv.org/licenses/assumed-1991-2003). The definition is mathematics and free to use. No code.

## Runs on this Mac without a GPU?
Yes. A plug-in estimator for discrete, history-length-1 TE is a few lines of standard-library Python. A check on 200,000 samples ran in 0.6 s on this Mac and reproduced James et al.'s XOR values (see james-barnett-crutchfield-2016-information-flows-critique.md). Continuous signals need binning or a kernel or nearest-neighbour estimator. Those are also CPU-cheap at conversational data rates, but the result depends on resolution, as the paper says.

## Verdict: adopt (as the formal definition), with the interpretation bounded
Adopt Eq. 4 as the measure "the partner's state reduces uncertainty about my next state beyond my own history", in both directions (partner→agent and agent→partner). It is directional, it conditions out self-history, it is model-free, and it is cheap. Constraints taken from the paper itself:
- It assumes stationarity and a Markov order k. Conversation is neither, so windowed estimates with stated k, l and resolution are needed.
- Results depend on the coarse-graining resolution. Report the binning and r, or a TE(r) curve.
- It removes only known common drivers. A shared external rhythm (a beat, turn-taking prompts) inflates TE unless it is conditioned out.
- The paper calls TE "information transfer". James et al. 2016 show this word is too strong. Name the quantity "predictive dependence of the agent's next state on the partner's past", not "flow".
