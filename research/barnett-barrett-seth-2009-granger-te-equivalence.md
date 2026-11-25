# Barnett, Barrett & Seth 2009, "Granger causality and transfer entropy are equivalent for Gaussian variables" (Phys Rev Lett 103:238701; arXiv:0910.4514)

Source read: arXiv v2 (10 Nov 2009), 10 pages, in full, including footnotes [28]-[34]. The published PRL version was not compared against it.

## Claims
- Central result (Eq. 13): "if all processes are jointly Gaussian, then F_{Y→X|Z} = 2 T_{Y→X|Z} so that Granger causality and transfer entropy are equivalent up to a factor of 2. This result holds, in particular, for a univariate predictee X with the standard definition (8) of G-causality."
- Granger causality (Eq. 8): "the natural logarithm of the ratio of the residual variance in the restricted regression (6) to that of the unrestricted regression (7)". For a multivariate predictee they use Geweke's generalised variance (Eq. 9): F = ln(|Σ(X | X⁻⊕Z⁻)| / |Σ(X | X⁻⊕Y⁻⊕Z⁻)|).
- Transfer entropy (Eq. 10): T_{Y→X|Z} ≡ H(X | X⁻⊕Z⁻) − H(X | X⁻⊕Y⁻⊕Z⁻), "the degree of uncertainty of X resolved by the past of Y over and above the degree of uncertainty of X resolved by its own past."
- Mechanism: for jointly Gaussian variables, H(X | Y) = ½ ln|Σ(X | Y)| + ½ n ln(2πe) (Eq. 11), where Σ(X | Y) is the partial covariance, which equals the residual covariance of the OLS regression (Eq. 3).
- Caution on causality: "identification of a G-causality interaction is not identical to identifying a physically instantiated causal interaction in a system", and causal structure "can only be unambiguously identified by perturbing a system and observing the consequences".

## Evidence
Analytic proof; no data. The conditions and limits, verbatim:
- Joint Gaussianity: the processes must be "jointly multivariate Gaussian (i.e. any finite subset of the component variables ... has a joint Gaussian distribution)".
- Stationarity is assumed "for simplicity", but "The analysis carries through for the non-stationary case" (fn 30). Discrete time (fn 29).
- The regressions are "predictive models", and the variables "may depend on latent (unknown) or exogenous (unmeasured) variables not included in the regressions" (fn 31).
- Estimation: numerical equivalence "will depend on the method used to estimate the transfer entropy in sample". "naive estimation of transfer entropy by partitioning of the state space is problematic". For TE, unlike G-causality whose estimator is asymptotically χ², "we are not aware of any such general result ... significance testing for transfer entropy estimates is likely to be hard."
- Non-Gaussian case: "Further research is thus required to characterize ... the manner in which the equivalence (13) breaks down when Gaussian assumptions fail", although "in the generic (non-Gaussian) case, nonzero G-causality implies nonzero transfer entropy".
- Their preliminary claim: "under Gaussian assumptions there is nothing extra to account for by nonlinear extensions to G-causality, since a stationary Gaussian AR process is necessarily linear".

## License
arXiv non-exclusive distribution license 1.0. No code with the paper.

## Runs on this Mac without a GPU?
Yes. Gaussian TE is half the log ratio of two OLS residual variances. A standard-library Python check on a 200,000-step bivariate VAR(1) gave F = 0.3626 nats and TE = 0.1813 nats. This only checks the algebra (both are computed from the same residual variances), not an independent estimator.

## Verdict: adopt (as the default estimator of the contingency measure, under stated assumptions)
For the "contingently answered" signal this gives a cheap, closed-form estimator with known sampling theory: fit restricted and unrestricted linear autoregressions on the agent's and partner's sign streams, and take ½ ln of the residual variance ratio as TE, in nats. It also gives an asymptotic χ² null for free, which the authors say TE lacks. Conditions to log with every estimate:
- The equivalence holds only for jointly Gaussian processes. Discrete signs such as facial blendshapes, prosody events and turn onsets are not Gaussian. Either transform them, or report the result as "linear (Gaussian) TE" and check against a nonparametric estimator.
- Lag orders p, q, r and the conditioning set Z must be fixed in advance. Latent common drivers are not removed.
- It is a predictive, not causal, quantity. The paper itself says causation needs perturbation. Contingency perturbations such as a still-face or a delayed replay, where the partner's input is replaced, are the intervention that turns the measure into a causal test.
