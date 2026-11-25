# Dale, Fusaroli, Duran & Richardson 2013, "The self-organization of human interaction" (Psychology of Learning and Motivation 59:43-95, doi 10.1016/B978-0-12-407187-2.00002-2)

Source read, 2026-11-25: the PDF the Aarhus University repository lists as "Pdf of the draft, Submitted manuscript" (pure.au.dk/ws/files/53762658). It is in fact an Elsevier uncorrected proof, so wording may differ slightly from the print version.
- Read in full: the abstract, §1, §3.2.3, §3.3, §5 (all subsections) and §6 (all subsections).
- Read in part: §4.2–4.3 (the perspective-taking model).
- Skimmed: §2 and §4.1 (eye-tracking under social context).
- Not read: the references.

This is a review chapter. Its evidence is other studies, which were not read here.

## Claims
- **The "centipede's dilemma".** Research studies channels and processes one at a time, but "naturalistic human interaction must integrate all of these factors simultaneously". Dynamical systems theory, with self-organization and synergy, is offered as the integrating frame.
- **Synergy.** "a functionally driven reduction of degrees of freedom, where components do not simply align, but also complement and compensate for each other."
- **Social variables act as control parameters.** "significant reorganization of interactive behaviors should occur under different social contexts", and the change is rapid and nonlinear ("phase transition").
- **Alignment is not enough.**
  - "not all conversations contain the same amount of linguistic alignment".
  - Coordination may run "across many speech turns, thus escaping the tight temporal constraints of automatic priming".
  - "a conversation constituted exclusively of reciprocal repetitions should not strike anybody as a very productive one."
- **Three predictions of the synergy model** (§5.4):
  - "only task-oriented alignment is effective";
  - stable patterns exist "whose role can be indifferently filled in by one or the other of the interlocutors";
  - "the self-organization of the interaction takes time, growing in strength and efficacy as the interlocutors adapt to each other, by both aligning and complementing each other."
- **The authors' own admission.** "dynamical systems accounts are very short on concrete models". The two key features "mostly describe the form of interaction, rather than the underlying mechanisms".

## Evidence (secondary, as reported)
- **Same oddball corpus** (Bahrami et al. 2010). The chapter restates the Fusaroli et al. 2012 lexical result (indiscriminate alignment negative, selective alignment positive) and the Fusaroli & Tylén result (interaction-level recurrence predicts benefit, cross-interlocutor recurrence does not).
- **A third, then-submitted study.**
  - Speech production follows lognormal scaling laws.
  - "Indexes of behavioral alignment (mutual information) were shown to decrease over time, while indexes of more complex multiscale coordination (complexity matching …) were shown to increase over time".
  - "the increase in multiscale coordination—and not its initial value—was shown to significantly correlate with performance."
  - No numbers are given in the chapter.
- **Turn-taking.** More than 50% of gaps are under 300 ms, yet simultaneous starts are rare. Wilson & Wilson's oscillators are "entrained in antiphase".
- **Maze game.** Exchanges shrink from more than 150 turns over 12 games. Mills 2011 found that cross-community pairing disrupts routines.
- **Perspective-taking** (Duran & Dale; Duran et al. 2011). Believing the partner was simulated rather than real raised other-centric responding, sped responses and reduced competition from the egocentric option.

## Formal models
- **Perspective-taking as a bistable potential.**
  - Duran & Dale borrow the Haken–Kelso–Bunz form: "a control parameter in a potential function is set to initiate bistable attractor basins of other-centric or egocentric interpretations."
  - Within a trial, settling comes from competition between landscape shape, initial position and "a subtle noise impulse".
  - Between trials, the control parameter is updated, like a belief about the partner.
  - "setting one set of parameters can simultaneously model all three such timescales" (choice distribution, RT across trials, mouse-trajectory curvature).
  - The potential's equation is not printed in the chapter.
- **"Surface network" proposal** (§6.3, hypothetical, simulated point processes only).
  - Code each person's behaviours (A–D) as event series at 250 ms. Induce a graph with edges from temporal correlation.
  - Count degrees of freedom as unconnected subgraphs:
    - no coupling gives 8;
    - pure cross-person synchrony gives 4;
    - cascading alignment ("saturation") gives 1;
    - a synergy gives mixed clusters spanning both persons and channels that reconfigure over time ("Transition"), with the count possibly unchanged.
- **Estimators named for the coupling:** vector autoregression, Bayes nets, and Shalizi et al.'s causal-state methods. A hidden-Markov layer beneath the surface network is suggested.

## What it implies for a dyadic affective core
- **The surface-network picture shows the one-gain failure as geometry.**
  - A single gain moves the network only along one path: no edges → same-channel cross-person edges (synchrony) → everything coupled (saturation). This is exactly flat → copy.
  - Synergy is a different topology. Cross-channel, cross-person clusters (my smile with your nod; my pause with your brow) reconfigure when the activity changes.
  - So the partner's influence on the Bot should be a structured matrix whose sparsity pattern changes with context, not a scalar times identity.
- **Social beliefs are control parameters that switch attractors.** In the perspective model, one belief about the partner (real vs simulated) changes which basin wins. For the Bot, a slowly updated estimate of the partner (familiar vs stranger, the partner's role) should reshape the landscape. This is the profile change the project's dial analysis asks about, not a gain change.
- **Coupling evolves on a slow time scale.** Alignment falls and multiscale coordination (complexity matching) rises within a session. A fixed gain cannot produce that crossover; a slow variable that restructures the coupling can.
- **Not shown.**
  - No affect measures.
  - No faces.
  - The network method is only a hypothetical sketch.
  - The perspective model's equations are not given.
  - The complexity-matching result has no numbers here.

## Verdict: watch
- It is useful as a map: the surface-network degrees-of-freedom framing is a concrete way to state "not one gain", and it names VAR and causal-state estimators.
- But it is a review with no model of its own, and the read copy is an uncorrected proof.
- The primary sources worth reading next are:
  - Duran & Dale (perspective-taking dynamics);
  - Abney et al. 2014 "Complexity matching in dyadic conversation" (JEP:General 143:2304);
  - Fusaroli et al. 2012 (Psychological Science, indiscriminate vs selective alignment).
