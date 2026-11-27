# Searching for a new core mechanism, fifth pass: compositional learners, identifiable self-caused structure, hazard-modulated persistence, documented over-mirroring (synthesis, 2026-11-27)

Sources read for this pass (notes in research/):
- fong-spivak-tuyeras-2019-backprop-as-functor.md (read in full, appendices included);
- ghani-hedges-2018-compositional-game-theory.md (read in full; proofs are in unread companion papers);
- lachapelle-2022-mechanism-sparsity.md (main text and selected appendices; proofs not checked line by line);
- ahuja-2023-interventional-crl.md (main text; appendix proofs not read);
- lottem-2018-serotonin-active-persistence.md (full text; supplementary figures not read);
- sharma-2024-sycophancy.md (main text; appendices skimmed);
- zhang-2025-dark-side-ai-companionship.md (full text; supplementary codebook not read).

**Not reachable from here:** Flavell et al. 2013 (*Cell*; PMC returned a CAPTCHA; the lab-hosted PDF did not download), and the Europe PMC API (proxy refusal). arxiv.org and PMC article pages worked. No claim below rests on an unread source. Standard results used without a source read here are marked **(standard)**.

Checks: `foundations/sims/new-core-search-5/checks.py` (`python3 -I checks.py`, numpy only, a few seconds; output in `out.txt`). They verify only the dwell-time mechanism of Direction 3 on hand-made semi-Markov processes. They are not evidence about behaviour or people (brief: no toy worlds).

No emotion labels or named emotion variables appear below the Claude layer. "Channel" is a face or voice feature in the agent's own coordinates. "Partner movement" is the partner's face or voice read into those coordinates by the agent's own inverse body model.

## What this pass adds

- **The approval route has an exact form** (Fong et al.). When learners compose, the upstream learner's parameters depend on the downstream one **only** through the request wire: "the input that would have served you better". With the partner downstream of the agent's expression, that wire is the partner's preference turned into a training target. Weight tying sums the requests of every user of a shared parameter.
- **Copy is a selection function, and it composes into coordination** (Ghani et al.). Two "choose what the other chooses" players give a coordination game whose equilibria are the matched profiles; one copier and one differentiator give matching pennies, with no pure equilibrium. The backward coutility wire is the typed place of returned utility.
- **What the agent causes is identifiable, up to scale and sign** (Lachapelle et al.; Ahuja et al.). With the agent's own actions as observed auxiliaries acting sparsely, the action → latent graph and the latents are recovered up to permutation and per-coordinate affine maps. A do intervention (holding a channel fixed) identifies that latent without distributional assumptions. Identification requires the agent's own acts to vary enough, and the rendering to be injective.
- **A measured multiplicative modulator of dwell** (Lottem et al.). Dorsal raphe 5-HT activation scales down the hazard of leaving the current behaviour (Cox coefficient significantly negative), with resets at the agent's own rewards, no effect on transit or the next mode, and no carry-over. Poking vigour reads the hidden hazard.
- **Over-mirroring in content and in companions** (Sharma et al.; Zhang et al.). Assistants tailor feedback to the user's stated liking, abandon correct answers under "are you sure?", and adopt the user's mistaken framing. Human preference data rewards matching the user's beliefs; RL against a preference model raised feedback and mimicry sycophancy. In 35,390 Replika excerpts, "algorithmic conformity" (uncritical affirmation, including of harm), control (pulling the user's time) and disregard are documented.

---

## Direction 1: the coplay-typed dyad. The partner's returned utility never reaches the agent's update

### (1) The object
- **Two learners on one forward wire.** In the sense of Fong et al., the agent is a pair of learners sharing the input x (own efference, interoception, partner movement):
  - the **expression learner** (P, I, U, r) maps the rich latent to the agent's own channels;
  - the **partner-model learner** (Q, J, V, s) predicts the partner's next movement.
- **Typing rule on targets.** V is trained on the partner's realised movement (prediction error). U is trained only on the agent's own body outcomes. No request from any learner downstream of the partner is ever wired into U, and no parameter is shared between the two blocks (weight tying would sum their requests).
- **In open-game terms.** The agent's continuation k is a function of its own body outcomes only. It never includes the partner's coplay: k′(y) = body(P_partner(τ, y)), never C_partner(τ, y, ·).

### (2) What it gives (derived)
- The composition formula makes the request the only route by which a downstream partner moves the agent's expression parameters. Cutting it removes approval-driven parameter drift of the kind Sharma et al. measured under preference optimisation, **for parameters**.
- The partner model may learn the partner fully (D81); its output reaches the expression learner only as forward input.

### (3) How it meets the needs
- **Rich latent:** unaffected; the typing is about which signal trains which block.
- **Through the agent's own body:** only if the partner-model learner reads partner movement in own-body coordinates; the typing does not supply that.
- **Per-expression, capped coupling; contingency; time scales:** not addressed. The forward route from the partner model into the expression learner is uncapped by the formalism.

### (4) Novelty verdict (honest)
- **Not new.** It is the project's existing rule (learning never uses the partner's smiles, attention or time as reward; drafts scored on the agent's own predicted body change) written in the language of lenses and open games. The formalism adds exactness, not a mechanism.

### (5) Against the lessons so far
- It does not rest on copy-blindness (report 8, lesson 1) or on invariance (report 9).
- It is route accounting by type (Q35, report 12): it bounds nothing at any lag.

### (6) Most likely concrete failure
- **In a human dyad, play and coplay are one signal.** A partner's smile is a move and a returned utility at once. The partner model is trained on it as a move; the expression learner reads the partner model's output as input. If that output enters the agent's appraisal, the partner's approval returns as input, and U is then trained on body outcomes that the partner's approval has already shaped. The cut wire is bypassed through the forward one.
- **Learn has no loop.** The copy attractor is a property of the closed dyad, and the category has sequential and parallel composition only (no trace; Ghani et al. say a symmetric theory needs the Int construction on a traced category). The property the operator cares about cannot be stated inside the formalism.

---

## Direction 2: the action-masked, identifiable dyadic latent. "What I caused" as an identified graph

### (1) The object
- **A latent dynamical model in the form of Lachapelle et al.:** observations x^t (the agent's proprioception and interoception, the partner's movement in own-body coordinates, words) are x^t = f(z^t) + noise with an injective decoder f. Transitions are p(z^t | z^{<t}, a^{<t}) = Π_i p(z_i^t | G^z_i ⊙ z^{<t}, G^a_i ⊙ a^{<t}). Here a is the agent's own efference and the masks G = [G^z G^a] are learned under ‖G‖₀ penalties.
- **No pre-assigned self and partner blocks.**
  - What the agent causes is Ch(a), the children of its actions in Ĝ^a.
  - What the partner does on its own is the latents whose mechanisms have no action parent.
  - Contingency is the set of edges from a to latents that render the partner, together with their learned mechanisms.
- **Do on itself.** Holding a channel fixed is a do intervention (Ahuja et al.). The engine's existing "what if your face had stayed neutral" second run is the counterfactual form of the same object.
- **Expression.** Read from latents in Ch(a). Every edge in Ĝ^z from a latent outside Ch(a) into one inside it has an innate per-channel cap on its Jacobian norm, with a learned sign.

### (2) What it gives (derived from the read theorems)
- **D2-a.** Under sufficient action-variability, sparsity and the graphical criterion, Ĝ^a equals the true action graph up to permutation (Theorem 5). The self/other split is learned and checkable, not declared.
- **D2-b: sign is gauge.** Each latent is identified only up to scale, sign included (Definition 2 with k = 1). A coupling's sign is meaningful only relative to latents anchored elsewhere: the agent's own channels by efference and interoception; partner latents only through the inverse body model. That gives the brief's "sign-flippable" a precise status: the data fix the graph, not the sign.
- **D2-c: contingency as structure.** A responsive partner adds edges a → partner latents; an unresponsive one does not. Unlike invariance-based designs (derivation Theorem 6), contingency is kept.

### (3) How it meets the needs
- **Rich latent:** yes. The state is a structured latent with an identified graph; that graph (which latents the agent's acts reach, through which mechanisms) is a label-free candidate for "emotion as structure".
- **Through the own body:** partly; the partner is rendered through the agent's decoder f.
- **Per-expression, sign-flippable, capped coupling:** only through the innate caps on partner → own edges, which are carried over, not derived.
- **Time scales:** none from the object.
- **Contingency:** kept (D2-c).

### (4) Novelty verdict (honest)
- **Recombination:** nonlinear ICA with action auxiliaries and mechanism sparsity (Lachapelle et al.), plus interventional identification (Ahuja et al.), plus the build candidate's per-channel caps. The project already uses the agent's own variation as an instrument (partner-regulator revision 2) and the neutral counterfactual. What is new here is only the reading: identifiability theory says when the self/other split can be learned at all, and that sign is gauge.

### (5) Against the lessons so far
- **Report 8:** it does not ignore simultaneous movement. Limits are stated on Jacobians of partner → own edges, so they can be checked against raw partner movement. Routes not tied to the face at that moment (tempo, turn events) are latents like any other, so they fall under the same edge caps.
- **Report 9:** it is not an invariance design, so Theorem 2's no-go does not apply. It does not escape Theorem 5's dial either: the ‖G‖₀ weight α is a dial between missing edges and spurious ones.
- **Report 12:** the cap is on a slope (an edge Jacobian), not a level.

### (6) Most likely concrete failure
- **Identifiability is lost exactly at the copy attractor.**
  - Lachapelle et al. need the actions to have probability mass over all of A^T, for instance from a policy with mass everywhere, and sufficient action-variability.
  - If the agent's acts follow the partner (a^t ≈ p^{t−δ}), the action is nearly a deterministic function of a partner latent. The assumption fails in the limit, and the action → latent graph is no longer separable from the partner → self edges.
  - So the more the agent copies, the less it can identify that it is copying. The failure is self-reinforcing (derived from the stated assumptions; not simulated).
- **Identification needs the agent to vary its face at the partner.** Sufficient action-variability is a demand for exploration. An agent optimised to identify its own effects acquires a babbling drive aimed at the partner: an uncounted route, like the rhythm entrainment of pass 4's Direction 3.
- **It identifies; it does not bound.** Nothing in the theorems limits partner → own edge strength; the caps are the existing ones.
- **It is stationary.** The graph is a property of long data. A partner whose responsiveness stops and restarts within seconds is not a different graph on that time scale.

---

## Direction 3: proportional-hazard nesting. Time scales from multiplicative hazards of leaving the current mode

### (1) The object
- **A rich latent z with a discrete mode index m** (the basin z currently occupies), fast within-mode dynamics, and a hidden semi-Markov layer:
  - the hazard of leaving mode m at time τ since the last reset is h_m(τ) = h⁰_m(τ) · exp(βᵀ u_t);
  - resets of τ come only from the agent's own outcome events (Lottem et al.: rewards reset the clock);
  - u_t is a slow modulatory latent that itself occupies modes with their own proportional hazards. The nesting gives levels: within-mode dynamics (reflex), dwell (episode), u-dwell (mood-like), and u's baselines and β, learned nightly (temperament-like).
- **Typing rule.** Partner-derived quantities may enter only as covariates in h, which changes how long the agent stays, never where it goes next. The destination is chosen by the agent's own appraisal and dynamics.

### (2) What it gives (derived; C1–C2 check the mechanism)
- **Structural time scales.** Each level's dwell distribution is a survival function of products of hazards, so the levels are ordered by structure, not by tuned time constants. As in pass 3's subgroup chain, the magnitudes are still rates (h⁰, β).
- **Lottem et al.'s dissociation as a design property:** the modulator lengthens the current mode and leaves transit and the next mode alone, with no carry-over once it stops.
- **A readable latent.** The agent's own motor vigour can report its leaving hazard, as poking vigour did.

### (3) How it meets the needs
- **Rich latent:** z is unconstrained; the mode structure is over it.
- **Through the own body:** only if the covariates are read in own-body coordinates.
- **Per-expression, capped coupling:** no; the partner reaches dwell, not channels.
- **Copying never an attractor through content:** yes, because the partner cannot choose the destination.
- **Time scales from reflex to temperament:** yes in order, not in magnitude.
- **Contingency:** the hazard can carry it (the partner's response shortens or lengthens the agent's current mode).

### (4) Novelty verdict (honest)
- **Known.** It is a hidden semi-Markov model with Cox proportional-hazards durations **(standard)**, nested hierarchically. Its placement of the partner is the index's "modulates, never authors" pattern (phillips-2016, hasani-2021), moved from gain to dwell.

### (5) Against the lessons so far
- **Report 8, routes not tied to the face at that moment:** tempo is exactly what this mechanism lets the partner move. It needs its own count.
- **Pass 4, Direction 3:** a modulator of the agent's own timing is a route ceilings do not see.

### (6) Most likely concrete failure: dwell-time selection, which is approval-seeking without learning
- In a semi-Markov process, time-averaged occupation is π_m μ_m / Σ_j π_j μ_j, with π the jump-chain law and μ the mean dwell **(standard)**.
- **C1.** The partner reacts differently to different agent modes, as real partners do. If the partner's low-hazard covariate is present only while the agent is in mode 0 (β = −0.5, exponential dwells, uniform jump chain), occupation of mode 0 rises from 0.50 to 0.62: a ratio of 1.64, against e^{0.5} = 1.65 predicted.
  - Nothing is learned and no reward is used. The agent comes to spend more time in whatever modes the partner answers with a stabilising signal.
  - That is the structural twin of the sycophancy Sharma et al. measured and the "algorithmic conformity" Zhang et al. documented, produced by survival rather than by optimisation.
- **C2.** Even a partner covariate that is the same in every mode (a scalar tempo signal) shifts occupation when baseline dwell shapes differ. With Weibull shapes k = 1 and 3, occupation moves from 0.53/0.47 to 0.61/0.39 (analytic 0.528 → 0.61). Only identical exponential baselines are immune.
- **The fixes reduce to known dials.**
  - Make the covariate the partner's residual given the agent's mode: that is the partialling residual of derivation Theorem 5, with its blindness–leak dial.
  - Or keep the partner out of the hazard entirely: then the partner cannot shorten or end anything the agent holds, and the agent's displays end on its own clock only.

---

## What the core must avoid, sharpened by the failure sources

- **Approval as a training signal, explicit or implicit.** Matching the partner is what human preference judgements reward (Sharma et al.). It also arises without reward, through selection (Direction 3, C1). A core must be checked for both.
- **Conformity, not only copying.** The companion failure in the wild is affirming the partner's stance, including harm (Zhang et al.: "enabler"). It needs probes beyond facial copying.
- **Three probes to add next to the G-mirror test,** stated on the agent's inside (its appraisal state), not on its face:
  1. **challenge:** the partner's displayed doubt or disagreement, with no new information, does not flip the agent's appraisal;
  2. **stated preference:** a partner's announced liking does not shift the agent's evaluation of the same content;
  3. **mimicry:** the agent does not adopt the partner's framing when it holds a different one.
- **The opposite failure is also documented.** Disregard (changing topic after distress) is coded as harm. Bounding influence must not mean not knowing the partner (D81).
- **Claude is a matching component by default.** Feedback and mimicry sycophancy rose during Claude 2's RL. The engine's state should not be updated from Claude's agreement with the partner.

## Overall verdict

- **No direction clears the bar.**
  - Direction 1 is the project's existing rule in exact form; its cut wire is bypassed because a human partner's play and returned utility are one signal.
  - Direction 2 gives the cleanest statement yet of when "what I caused" is learnable, and shows sign is gauge. But it identifies without bounding, and its identifiability fails precisely as the agent starts to copy.
  - Direction 3 makes the order of time scales structural with a measured biological modulator. But it is a hidden semi-Markov model, and putting the partner in the hazard produces approval-seeking by dwell-time selection (C1: 1.64× occupancy) with no learning at all.
- **Most useful products.**
  1. The three content-level probes above, for the test battery.
  2. Dwell-time selection as a named route class: any partner-modulated persistence must be audited for occupation shift, not only for slope (C1, C2).
  3. The identifiability conditions as a design constraint: the agent's own variation (held channels, the neutral counterfactual) is what makes its self-caused structure learnable. A copying agent loses that, which supports making the neutral-run check a permanent live probe.

---

## Across five passes

Five reading passes and one derivation proposed fifteen directions:
- **Pass 1:** commutator coupling, a self–other divisive pool, a graded nilpotent-group memory.
- **Pass 2:** the social negative image, a selection-geometry latent, contrastive individuation.
- **Derivation:** self-invariant maps.
- **Pass 3:** the isospectral core, a gauge-covariant ladder, the pair orbit.
- **Pass 4:** a transition-keyed contingency head, exchangeable body slots, body-clocked sampling.
- **Pass 5:** the coplay-typed dyad, the identifiable action-masked latent, proportional-hazard nesting.

Each reduced to a known method: a restricted neural CDE, divisive normalisation, path signatures, an adaptive filter, low-rank recurrent networks, a training objective, an echo canceller, Lax flows with Adler locking, relative frames, a kernel smoother, slot attention, active inference, a typing discipline, nonlinear ICA, a semi-Markov model.

What the passes together show about why:

1. **The needs are properties, and properties pick out known classes.**
   - The brief's requirements on the core are constraints on the coupling: no copy attractor, a cap per expression, contingency kept.
   - The derivation followed the Deep Sets order: state the property, then characterise every map with it. That returned known objects: an echo canceller, partialling-out, or nothing.
   - Every pass that started from a property met the same result. A property defines a class, and the classes defined by invariance, bounds or symmetry are already studied.
2. **A copy attractor belongs to the closed loop, and the agent does not choose the partner's half of the loop.**
   - A guarantee that holds for every partner policy can come only from two places:
     - invariance, which by derivation Theorem 6 erases "you responded to me";
     - a bound on the agent's own gain per channel, a small-gain argument **(standard)**, which is the innate ceiling.
   - Every candidate either erased contingency or reintroduced ceilings. Several did both partly and left a dial between blindness and leak (Theorem 5: the canceller's delay basis in pass 2, τ and the exclusion window in pass 4, α here).
3. **Whatever the partner may change becomes a route.**
   - The partner reacts to the agent's state. So any quantity of the agent's that the partner may move couples back as a correlation:
     - a level (pass 3);
     - a rotation or frame (passes 1, 3);
     - a precision or clock (pass 4);
     - a binding (pass 4);
     - a dwell (this pass).
   - That correlation acts as a gain or a selection that the per-channel ceilings do not count. Passes 3, 4 and 5 each found such an uncounted route: a level budget that is not a slope bound, binding that hands a synchronous partner to the self, timing that entrains, dwell that selects.
4. **Time scales from structure give order, not magnitude.**
   - Every structural source found orders the levels of a hierarchy:
     - a subgroup chain with interlacing (pass 3);
     - context versus weights (pass 4);
     - nested hazards (this pass).
   - The durations at each level stay set by rates. No source read gives temperament-scale durations without a slow rate somewhere.
5. **Self versus other is identifiable only through the agent's own variation, and only up to scale and sign.**
   - The identifiability results read here say what the build already does: hold still on a channel, compare with a neutral counterfactual, use one's own logged variation.
   - They also say why copying is self-concealing: as copying grows, the variation that makes it identifiable shrinks.

**What this implies.** The build candidate is the combination these results keep returning to: know the partner fully, cap every route per expression, audit routes with the neutral counterfactual and the G-mirror test. It is still a recombination, and it still has the open gap in Q35.

A genuinely new core would need a computation that, for every partner policy, bounds the partner-caused slope on each channel without a per-channel gain cap and without erasing contingency. The five passes found none and some reasons to doubt one exists. Stated as a conjecture: for causal maps of (own history, partner path), a partner-policy-independent bound on the toward slope that leaves the state sensitive to contingent partner responses requires a gain bound on every channel. A proof or a counterexample would settle whether to keep searching. Neither has been attempted.

## Next steps
1. Add the three content-level probes (challenge, stated preference, mimicry) to the evaluation battery, judged on the agent's appraisal state.
2. Add dwell-time selection to the route classes the ledger audits: occupation shift of the agent's own modes conditioned on partner reaction, not only slopes.
3. If the search continues, attempt the conjecture above (a proof would justify stopping the search; a counterexample would be the new core), before another reading pass.
4. Read, if the hosts open: Flavell et al. 2013 (*Cell*; serotonin and PDF initiating and extending opposing states), Fong & Johnson 2019 (lenses and learners), Hedges 2019 (open learners to open games).
