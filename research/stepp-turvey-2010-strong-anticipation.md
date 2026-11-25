# Stepp & Turvey 2010, "On strong anticipation" (Cognitive Systems Research 11(2):148-164, doi 10.1016/j.cogsys.2009.03.003); with Stepp 2009, "Anticipation in feedback-delayed manual tracking of a chaotic oscillator" (Experimental Brain Research 198(4):521-525)

Source read, 2026-11-25:
- **Stepp & Turvey 2010.** Author's offprint (Elsevier "author's personal copy", from the first author's site), text extracted with pdftotext. Read:
  - §§1-7 in full: the outfielder problem, Dubois's definitions, anticipating synchronization, the mechanism of delay coupling, and the hallmarks;
  - §8.1 (an array of anticipating times);
  - §10.3;
  - §11 (Conclusions).
  - Skimmed only: §8.2-8.4 and §9 (circadian rhythms, Pavlovian learning) and §10.1-10.2 (forward models).
- **Stepp 2009.** Full text on PMC (PMC3724402), through a fetch tool. This is the human data. The 2010 paper itself has none.

## Claims
- **Dubois's distinction,** quoted by the authors: in "strong anticipation" the current states are "computed from past and/or present states but also from potential future states, anticipated from these systems themselves and not from models of these systems". "Weak anticipation" uses models.
  - In their words: "prediction of the future given a model is labeled weak anticipation and prediction of the future not given a model—and relying instead on systemic lawfulness—is labeled strong anticipation".
  - The Kalman filter is their "classic exemplar of weak anticipation".
- **Delay in the slave's own feedback is the sine qua non.** "Delayed feedback in the slaved systems is the sine qua non of the strong anticipation." "The positive, productive status of delayed feedback cannot be overemphasized." This is against the internal-model view, in which delays are threats to be compensated.
- **Five hallmarks of strong anticipation.** It is:
  1. "an achievement by the system as a whole": "Any effort to separate the equations will destroy the slave's anticipatory ability";
  2. "owed to proper organization": "The coupling term must take a particular form ... k(x − y_τ). For example, k(y_τ − x) will not suffice";
  3. "uses the natural unfolding of events". The coupling term "is not a model of either system, nor contains the dynamics of either system";
  4. "is purely reactive at some level of analysis";
  5. "relates implicitly to future states". The solution y(t) = x(t + τ) refers to the future although no equation does.
- **The slave can differ from the master** (eq. 4): a harmonic oscillator anticipates a Rössler master and vice versa. "Only a small subspace, or even a single state variable, need participate."
- **Many slaves on one master give many anticipation times** (§8.1). The authors propose this for nested organism, organ and cell time scales (§10.3).
- **Errors look like prediction errors.** When the chaotic master turns abruptly, the slave makes a large error, "Analogues of ... incorrect prediction and manifest surprise", without any model.

## Evidence
- **The 2010 paper is theoretical.** Its figures are simulations:
  - Ikeda lasers;
  - Rössler master and slave;
  - excitable Adler and FitzHugh-Nagumo systems;
  - a Rössler and harmonic-oscillator mismatch with τ = 0.6, k = 1.
- **Fig. 9** maps anticipation (maximum shifted correlation) over coupling k ∈ [0, 1.4] and delay τ ∈ [0, 2.5]:
  - for matched parameters (a = b = 0.1, c = 14);
  - for mismatched ones (slave a = b = 0.2, c = 5.7).
  - It is "greater for the matched than the unmatched", but "either case provides a large area of anticipation".
  - "Increasing delay eventually leads to the destruction of anticipating synchronization."
- **Stepp 2009 (human, n = 10)** tracked a "chaotic spring" target on a tablet with delayed visual feedback of their own stylus.
  - Delays τ: 20, 200, 400, 600, 800 and 1000 ms. Trials of 80 s; 18 trials, of which the first block of 6 was practice.
  - Synchrony fell from ρ = 0.98 (SD 0.016) at 20 ms to 0.65 (SD 0.070) at 1000 ms. All pairwise paired tests were significant at α = .02; there was a cubic trend, F(1,9) = 5.40, p = .045.
  - At 20 ms the hand lagged, t(9) = −2.48, p = .035.
  - The hand led (anticipated) at 200 ms, t(9) = 4.74, p = .0011, and at 400 ms, t(9) = 4.88, p < .001.
  - For τ ≤ 400 ms the lead grew roughly linearly with τ: R² = .54, F(2,27) = 32.42, p < .001, slope b = 0.44.
  - From 600 ms on there was no reliable lead or lag. The SD of the lead was 0.058 below and 2.2 above the critical delay, which lies between 400 and 600 ms.
  - Participants reported trailing the target even when measurably ahead of it.

## Formal models
- **Ikeda master with delay, slave without** (eqs. 1-2):
  ∂x/∂t = −a x(t) − b sin x(t − τ)
  ∂y/∂t = −a y(t) − b sin x(t)
- **Voss delay coupling, delay in the slave** (eq. 3):
  ẋ = f(x)
  ẏ = f(y) + k(x − y_τ), with y_τ = y(t − τ)
  The manifold y(t) = x(t + τ) is the anticipating solution.
- **General form** (eq. 4): ẏ = g(y) + k(x − y_τ), with g ≠ f allowed.
- **Rössler master and slave** (eqs. 5-6):
  ẋ₁ = −x₂ − x₃; ẋ₂ = x₁ + a x₂; ẋ₃ = b + x₃(x₁ − c)
  ẏ₁ = −y₂ − y₃ + k(x₁ − y₁,τ); ẏ₂ = y₁ + a y₂; ẏ₃ = b + y₃(y₁ − c)
- **Many slaves** (eq. 10): ẏᵢ = f(yᵢ) + k(x − yᵢ,τᵢ). Each slave anticipates by its own τᵢ.
- **Stepp 2009 target** (chaotic spring):
  ẋ₁ = x₂; ẋ₂ = −(2π(x₃α + β))² x₁, with a Rössler (x₃, x₄, x₅) driving the stiffness;
  a = b = 0.1, c = 14, α = 100, β = 0.3.

## What it implies for a dyadic affective core
- **The partner-to-self coupling has a second parameter besides its gain: the delay in the self-term.**
  - k(x − y_τ) compares the partner now with oneself τ ago. The same k gives lagging, synchronous or leading behaviour depending on τ.
  - Stepp 2009 shows humans move from lag (20 ms) to lead (200-400 ms) as the delay grows, and lose it past about 500 ms.
  - A one-gain model k(x − y) cannot produce a lead without an explicit predictor.
- **Multi-scale coupling comes for free.** A bank of slaves with different τᵢ on one partner signal (eq. 10) anticipates at several horizons at once. This suggests the agent's response to a partner should be a family of delay-coupled channels, not one filter.
- **It names the failure the project fears.** On the synchronization manifold y(t) = x(t + τ), the agent becomes a *leading copy* of the partner. Anticipating synchronization is still copying, only shifted forward in time.
  - Strong anticipation therefore solves the lag problem, not the imitation problem.
  - It must be combined with a non-identity relation (complementarity, a task manifold) to avoid the flat-to-copy dial.
- **Prediction-error-like signals without a model.** Abrupt partner changes produce large transient slave errors. That is a model-free surprise signal that could feed affect, testable by lesioning the delay term.
- **Not shown:**
  - Nothing interpersonal: the 2010 paper is about physical, circadian, Pavlovian and motor systems.
  - Stepp 2009 is a human tracking a computer signal, unidirectional, with n = 10.
  - No bidirectional (mutual) anticipating synchronization between two people is reported here.
  - The link from the human data to the delay-coupled equations is qualitative by the author's own account.

## Verdict: adopt (mechanism option), with a bound
- Adopt delay-coupled channels k(x − y_τ) as the model-free alternative to an explicit predictor of the partner. Each τ is an ablatable component with a clear prediction: remove the delay and the lead vanishes.
- On its own it is another route to a (leading) copy, so it does not answer the single-dial target.
- The human numbers are from a single n = 10 tracking study.
