# Francis & Wonham 1976, "The internal model principle of control theory" (Automatica 12:457-465)

Source read: the 1976 paper itself was NOT accessible. ScienceDirect and the ResearchGate copy linked from Wikipedia both returned HTTP 403, and Semantic Scholar and Unpaywall gave no open copy. Everything below comes from these primary substitutes, read on 2026-11-25:
1. W. M. Wonham, "The Internal Model Principle of Control Theory", a 3-page note dated 2018.06.17 on the University of Toronto site (control.utoronto.ca/people/profs/wonham/W.M.Wonham_IMP_20180617.pdf). Read in full. It restates the IMP by one of the 1976 authors in a set-and-function setting. It omits the proofs.
2. Bin, Huang, Isidori, Marconi, Mischiati & Sontag 2022, "Internal Models in Control, Bioengineering, and Neuroscience", Annu. Rev. Control Robot. Auton. Syst. 5:55-79 (NSF PAR copy). Read: §1, §2.1-2.3 up to Eq. 16, the end of §2, §3 in full, the end of §4 and §5. Most of §4 (neuroscience) was not read.
3. Sontag, "Adaptation Implies Internal Model", arXiv math/0203228v1 (21 Mar 2002). Read: §1 including the linear case, §2 (definitions, Theorem 1, E. coli example) and the opening of §3. The rest of the proof was not read.
4. Doyle, Francis & Tannenbaum 1990, *Feedback Control Theory* (PDF posted by Francis), §3.3, Theorem 3 and the remark after it.

The 1975 Appl. Math. Optim. wording quoted below is second-hand, as Bin et al. quote it. Francis 1977 (SIAM J. Control) and Isidori & Byrnes 1990 were not accessible and were not read.

## Claims
- Informal statement (Wonham 2018): "a good controller incorporates a model of the dynamics that generate the signals which the control system is intended to track." Classical background: "Error feedback ... by itself can reduce parameter sensitivity, and final tracking error, but only at the expense of high loop gain", while "Error feedback, plus an internal model of the reference signal generator, together reduce final tracking error to exactly zero ... regardless of (reasonable) parameter perturbations, while requiring only moderate average loop gain."
- The two assertions (Wonham 2018): "Assertion 1. Error feedback + Perfect regulation ⇒ Internal Model" and "Assertion 2. Structurally stable (or “robust”) perfect regulation ⇒ Error feedback + Internal Model". Wonham frames these as the "converse questions", that is, necessity: "Is an internal model a necessary condition for “good” regulation?"
- Conditions of Theorem 1 (Wonham 2018): "Assume that S satisfies internal stability, perfect regulation, error feedback, and exosystem detectability."
  - Internal stability: "we assume that X is a finite set" and the exosystem-induced subset is "a global attractor".
  - Error feedback: "the controller C is externally driven only when state of S deviates from the target K, namely the dynamics of C are autonomous as long as x ∈ K".
  - Conclusions: the controller's dynamics form "a copy of the dynamics of E on the global attractor", and "this copy is faithful, namely incorporates fully the exosystem dynamics".
  - Assertion 2 needs a further "final crucial assumption of Rich Parameter Perturbation".
  - On scope: "the IMP crudely represents only a primitive “intelligence”; issues of adaptation, learning, computing power, and “real” problem-solving intelligence are open for investigation."
- 1975 linear statement (Francis & Wonham, as quoted in Bin et al.): asymptotic regulation under plant parameter variations is achieved "only if the controller utilizes feedback of the regulated variable, and incorporates in the feedback path a suitably reduplicated model of the dynamic structure of the exogenous signals which the regulator is required to process".
- Robustness is over the plant, not the controller (Sontag 2002; Bin et al. 2022): the controller "should perform appropriately ... even when the plant subsystem – but most definitely not the controller subsystem – is arbitrarily perturbed. The conclusion is that the controller is driven by y and incorporates a model of the external signals." Some such condition is needed, "since the system Σ which simply outputs y = 0 for every possible input signal u does not contain any subsystem generating the signals u."
- Exosystem class, linear case (Sontag 2002 §1.1): the inputs are solutions of a linear ODE "which has no stable modes. (Stable modes, giving components of u which converge to zero, are less interesting, since they do not represent persistent disturbances.)" The argument: "all the poles of G ... have nonnegative real parts. Therefore, these poles must be canceled in the product GS; in other words, S must have among its zeroes all the poles of G".
- Textbook form (Doyle, Francis & Tannenbaum §3.3): "For perfect asymptotic tracking, the loop transfer function L̂ must contain an internal model of the unstable poles of r̂."
- Nonlinear version with no plant/controller split and no structural stability (Sontag 2002, Theorem 1): "If Assumptions 1-3 hold and the system Σ adapts to inputs in a class U generated by a Poisson-stable exosystem, then S contains an output-driven internal model of U."
  - Assumption 1 is a uniform relative degree, read as "the system is able to detect changes in the input signal". Assumptions 2-3 (completeness and commutation of certain vector fields) are "automatically satisfied for linear systems".
  - Poisson stable means "trajectories keep returning to neighborhoods of the initial state".
- Steady-state content (Bin et al. §2.2): "the controller incorporates an internal model of the feedforward input u(w(t)) needed to secure the desired (zero) steady-state response of the regulated variable."
- "The IMP is not a theorem but rather a “mold” for many possible theorems, each of which will hold under appropriate technical assumptions" (Sontag 2002; repeated in Bin et al.).

### What the IMP does NOT claim (as read)
- No result for exosystems that are not persistent. The linear argument excludes stable modes. Under the nonlinear theorem, "adaptation to ramps is not included in the scope of the theorem to be stated", because ramps "require an unstable second-order system" (Bin et al. §3).
- No robustness to perturbations of the controller itself. Francis–Wonham robustness covers plant perturbations only (quoted above).
- Not a sufficiency result. "The necessary part, in particular, is known as the internal model principle (IMP)". Sontag's conditions "are sufficient but not necessary for the IMP to hold" (Bin et al.).
- Nothing about approximate regulation or unstructured uncertainty. "insisting on the ideal property of zero regulation error in the presence of arbitrary plant uncertainties seems to be unrealistic, to the point that Bin et al. (51) proved that no finite-dimensional robust regulator exists if unstructured perturbations are considered." This points to "approximate but robust designs" or "infinite-dimensional internal models" (Bin et al. §2, end).
- The early regulators cover a known exosystem only: "it cannot deal with uncertainties in the exosystem" (Bin et al. §2.1). Uncertain exosystems need adaptive internal models.
- "Neutrally stable" and "infinite-dimensional disturbance" as named conditions do not appear in the texts I read. The closest statements are "no stable modes" or "nonnegative real parts" (linear), "Poisson-stable" (nonlinear), and the infinite-dimensional-internal-model remark above.

## Evidence
Mathematical theorems. The Wonham 2018 proof is "omitted"; Sontag 2002 gives a proof (only partly read). The worked examples are E. coli chemotaxis (an integrator found by a change of coordinates) and the incoherent feedforward loop (Bin et al. §3). No empirical data.

## License
- Automatica 1976: © Elsevier; not read.
- Wonham 2018 note: author posting with no licence stated.
- Bin et al. 2022: "Copyright © 2022 by Annual Reviews. All rights reserved"; the copy read is the NSF Public Access Repository copy.
- Sontag 2002: arXiv licence.
- Doyle, Francis & Tannenbaum: "© Macmillan Publishing Co., 1990", posted free by Francis.

There is no code in any of them.

## Runs on this Mac without a GPU?
Yes. An internal model is a small linear or nonlinear ODE, such as an integrator or an oscillator bank at the disturbance frequencies, driven by the error. Integrating it costs microseconds per step.

## Verdict: adopt (as the formal basis for "regulation forces an internal replica", with a narrowed claim)
For (a), mimicry forced by robustly regulating a body that another agent disturbs:
- What the theorem forces: if a regulated body variable is to return exactly to its target for every signal in a class generated by an exosystem, robustly to perturbations of the body model, then the regulator must contain an error-driven copy of the exosystem's dynamics.
- In steady state the action it emits is the feedforward u(w) that cancels the disturbance. That makes it the counter-image of the other agent's signal passed through the body, not a copy of the other's behaviour. Outward "mimicry" follows only if cancelling the disturbance requires producing the same signal, which is a property of the plant model and must be argued separately.
- Required assumptions: the other agent's influence must be modelled as an autonomous exosystem in a fixed, persistent class (Poisson stable, or with no stable modes). A person who responds to the agent is not autonomous; the loop then runs through the other person, and the theorems read do not cover that case.
- Exact asymptotic regulation is required. With approximate regulation the necessity is not established in what I read; Andrews, Sontag & Iglesias 2008 ("approximate internal model principle") is cited but was not read.
- Sontag's version needs no plant/controller split. That suits a body that regulates itself, and it replaces robustness with a "signal detection" (relative degree) condition, which is the right condition to state for our agent.
