# Searching for a new core mechanism, fourth pass: the body as the clock of perception, synchrony without following, induction heads, slots, inverse planning (synthesis, 2026-11-27)

Sources read in full for this pass (notes in research/):
- al-2020-heart-brain-somatosensory.md (cardiac phase changes sensitivity; heartbeat-evoked potential changes criterion; both additive to alpha; SI not read);
- allen-2022-cardiac-active-inference.md (a POMDP whose visual likelihood precision is set by the inferred cardiac state; simulations only);
- boukarras-2025-physiological-synchrony-joint-action.md (heart-rate synchrony under imposed leader–follower roles is symmetric and at zero lag; raised by novelty, lowered by social anxiety; SI not read);
- tomyta-2023-leader-follower-tapping.md (self vs pair autoregressive coefficients; heart-rate synchrony when both adapt; reporting errors, model in an unread supplement);
- olsson-2022-induction-heads.md (transition-keyed lookup; phase change; smeared key; ablations; Model Analysis Table and appendices only skimmed);
- locatello-2020-slot-attention.md (competition over slots, shared update, permutation equivariance; supplement not read);
- zhixuan-2020-sips-inverse-planning.md (the other as a bounded partial plan, revised at divergence; supplement not read).

**Not reachable from here** (proxy refusal, rate limit or no resolution): transformer-circuits.pub (the HTML version of Olsson et al. and the "Mathematical Framework" paper), jneurosci.org (Garfinkel et al. 2014), nature.com (Baker et al. 2017, BToM), pnas.org directly (Al et al. was read through PMC), elifesciences.org, biorxiv.org (HTTP 429), pure.mpg.de, api.plos.org. arxiv.org, PLOS article pages, Frontiers and PMC pages worked. No claim below rests on an unread source. Standard results used without a source read here are marked **(standard)**.

Checks: `foundations/sims/new-core-search-4/checks.py` (`python3 -I checks.py`, numpy only, about 1 min; output in `out.txt`). It verifies only the mechanism of Direction 1 on hand-made streams. It is not evidence about behaviour or about people (brief: no toy worlds).

No emotion labels or named emotion variables appear below the Claude layer. "Channel" means a face or voice feature in the agent's own coordinates. "Partner movement" means the partner's face or voice features read into those coordinates by the agent's own inverse body model.

## What this pass adds

- **The body acts on perception through two separable operators** (Al et al.). The phase of one's own cycle changes discriminability: d′ is lower in systole, only late evoked activity is reduced, and the effect is stronger when one's own rhythm is more regular (r = −0.36 with HRV). The size of the body-evoked response shifts the decision criterion and early gain. Any route described as "attention" has to say which of the two it moves.
- **A model in which the body clocks perception** (Allen et al.). The likelihood precision of the world is a function of the agent's own body state, and the agent's own arousal policy changes how much time it spends in imprecise phases. Affect-like expectations arise from that coupling. It is active inference with a state-dependent precision, and its states and preferences are hand-named.
- **Synchrony without following** (Boukarras et al.; weakly Tomyta et al.). With leader and follower roles imposed by information asymmetry, heart-rate synchrony was still at zero lag and symmetric. It rose with shared novelty, fell with self-focus, and was unrelated to behavioural synchrony. What fits is a common cause (both bodies responding within about a second to shared uncertainty about the joint task), not a driven follower. Physiological synchrony is therefore no evidence of a self ← partner coupling, and a core can produce it with none.
- **A discovery story with an architectural intervention** (Olsson et al.). The pattern was: an abrupt measured change (a phase change), an intervention that moves it (a one-parameter smeared key that lets a one-layer model do it), ablation, then mechanism. The object is a lookup keyed on what preceded each stored item and returning what followed it.
- **Two ways of making "through my own body" exact.**
  - Weight sharing across exchangeable entities (slot attention: one update rule for every slot, with binding by competition).
  - Running one's own planner in inverse (SIPS: the other is a bounded partial plan in the same world model, revised only when it fails to predict).

---

## Direction 1: a transition-keyed contingency head. "What you did the last times I did this", typed as a model of the partner

### (1) The object
- **Memory per partner.** M_t = {(k_s, v_s) : s < t}. Each key is the agent's own preceding act, read through an innate shift:

  k_s = φ(σ(α)·a_{s−δ} + (1 − σ(α))·a_{s−δ−1}),

  the smeared key of Olsson et al. Here a is the agent's own motor command (efference) in its channel coordinates, and δ is a body-given latency. The value v_s = p_s is the partner's movement in the agent's own body coordinates, per channel.
- **Read-out at time t.** Weights w_s = softmax_s(⟨φ(a_{t−δ}), k_s⟩/τ). It produces three things:
  - the predicted partner response p̂_t = Σ w_s v_s;
  - the per-channel residual r_t = p_t − p̂_t: what the partner did beyond its usual answer to the agent's act;
  - the contingency mass c_t, the peakedness of w, together with the index of the retrieved moment.
- **Typing rule.** p̂_t is written only into the agent's model of the partner. The agent's rich latent state z receives r_t, c_t and an embedding of the retrieved moment. No path takes p̂_t, or the values v, to the agent's own expression. The agent's own face and voice are moved by partner input only through:
  - its own appraisal of (r, c, words) (D83);
  - the capped fast-mimicry reflex (D81), each channel with its innate ceiling and learned sign (D83).
- **Two time scales from the mechanism, not from time constants.** In context: M is the current exchange or day, read by attention. In weights: nightly replay consolidates φ, and the retrieval embedding, into slow parameters. A third structural time scale is the abrupt onset of contingency use (the phase change). With the shift given innately, the prediction is that it is available from the first exchanges.

### (2) What it gives (derived; C1 checks the mechanism)
- **D1-a: a partner whose movement answers the agent's act is predicted, so it leaves little residual.** With an exact lagged mirror (p_t = a_{t−δ}), the residual keeps 9–45 % of the partner's variance depending on τ and on how slow the agent's acts are. With a non-linear answer plus independent noise it keeps 33–64 %, against a noise share of about 25 %, so part of a non-linear answer also leaks (C1). A mirroring partner therefore feeds the agent's appraisal mostly as c (high and steady contingency), not as content.
- **D1-b: contingency is kept as content, not erased.** The property of derivation-self-invariant-maps.md Theorem 6 (invariance erases "you responded to me") is not imposed on c_t. c_t is high exactly when the partner's response matches its earlier responses to the same act. The infant probe of an abrupt stop and restart (kristen-antonow-2015) gives a sharp, measurable change in c.
- **D1-c: per expression, sign-flippable, capped.** Residuals are per channel. Their effect on the agent's own channel k goes through the agent's appraisal and then a cap c_k with a learned sign. The cap stays innate, which D88 allows.
- **D1-d: an ablation derived from the mechanism.** Remove the innate shift (set σ(α) so the key is the current act): contingency use should then need composition across layers and appear late and abruptly, as in Olsson et al.'s one-layer models. Remove M: r becomes raw partner movement and c disappears.

### (3) How it meets the needs
- **Emotion as structure in a rich latent.** What enters z is a content-addressed pattern: which earlier moments of this relationship are re-entered, how sharply, and on which channels the partner departs from them. That is structure over people, episodes and time without a fixed list of gauges. It is a substrate for the structure, not a theory of it.
- **The other through the agent's own body.** Keys are the agent's own acts. Values are the partner's movements in the agent's own body coordinates. The agent never copies, because the values have no route to its motor output.
- **Copying is not an attractor through this loop.** In the loop agent → partner mirrors → agent, the mirror is predicted, so its residual and with it the loop gain shrink by the residual fraction (0.09–0.45 in C1), times the per-channel cap. It does not become zero, so ceilings stay.
- **Contingency kept.** See D1-b.
- **Time scales.** Reflex comes from the capped reflex route. Exchange-scale memory is in context. Relationship-scale memory is in weights. Temperament is not produced by this mechanism.

### (4) Novelty verdict (honest)
- **Recombination.**
  - The lookup is an induction head (Olsson et al.).
  - Its prediction is in-context nearest-neighbour regression: a kernel smoother **(standard)**.
  - Its residual is the partialling-out residual of derivation-self-invariant-maps.md Theorem 5, with τ as the regulariser.
- **What is new, as far as this pass found:**
  - the typing rule, which sends a transition-keyed lookup into the partner model only;
  - the use of its match mass as the contingency signal that invariance-based designs erased.

  Neither is a new computation on the level of attention.

### (5) Against the lessons of reports 8, 9 and 12
- **Report 8: ignoring simultaneous movement is not new.** This does not ignore simultaneous movement. It predicts the partner from the agent's own act. It is the "what would you have done" comparison that report 8 found useful, with "your usual answer to me" as the counterfactual.
- **Report 8: limits against raw movement and across minutes.** The residual can exceed the raw movement (C1: up to 1.37 of the partner's variance with a recency exclusion). So any cap must be stated against raw p, not against r.
- **Report 8: routes that do not depend on the face now** (tempo, turn events) can be keys or values. Using them in appraisal is still a route to count.
- **Report 9.** The residual is the known partialling residual and inherits Theorem 5's dial: blindness versus leak, set here by τ and by the recency exclusion. The G-mirror test applies unchanged.
- **Report 12.** The quantity at issue is a slope (partner → own channel), and the bound is a per-channel cap on the appraisal route, not a level budget. It does not claim to close Q35.

### (6) Most likely concrete failure
- **Temporal-proximity aliasing erases the partner's own slow expressions** (C1).
  - When the agent's own acts are slow (AR(1) ρ = 0.98), the most similar key is usually the most recent one. The head then becomes a "partner's last value" predictor.
  - It cancels 53 % of an *independent* slow partner (residual 0.47 at τ = 0.05, no exclusion).
  - So a partner's sustained expression, unrelated to anything the agent did, mostly disappears from the residual the agent appraises. This is the held-level information the brief wants the agent to know.
- **Fixing it opens the other side.** Excluding the most recent 60 steps restores the independent partner (1.37, now inflated above raw). But the mirror's residual rises to 0.24–0.44.
- **τ and the exclusion window are two dials between blindness and leak**, as Theorem 5 predicted for any estimated partialling. A design would have to fix them innately, and they would be the next critique's target.

---

## Direction 2: exchangeable body slots. Self and partner are two slots of one set, updated by one learned body model

### (1) The object
- **A set of slots** S_t = {z_0, z_1, …, z_K}, each updated by the same learned body dynamics F_θ (a GRU or RSSM cell: the agent's own body model).
- **What breaks the symmetry.** z_0 is the only slot whose input includes efference and interoception.
- **Binding.** Each sensory feature x_i (the agent's proprioception, its interoception, the partner's face and voice in the agent's coordinates) is assigned by softmax over slots of predictive log-likelihood, A_ij = softmax_j(log p(x_i | z_j)), as in slot attention's normalisation over slots. Each slot is then updated with the weighted mean of its assigned features.
- **Output and reading.** The agent's expression is read from z_0 only. The partner's state is z_j, already in the agent's body coordinates, because F_θ is the agent's own model: weight sharing makes "through my own body" exact (Proposition 1).
- **Coupling.** The partner reaches z_0 through a slot-interaction term I(z_0, z_j). Its per-channel effect on the expression read-out has a cap c_k and a learned sign.
- **Relationships, groups and episodes** are persistent slots; new people need no new parameters.

### (2) What it gives
- **Structure over people.** The state is a set whose size varies. The assignment matrix A (who explains which feature) is itself a rich, label-free state. Self/other individuation is "explaining away" by competition, not a gate.
- **Divergence-driven updating** (SIPS). A partner slot's predicted plan is revised mainly where its prediction fails, so the partner model moves at event rate.

### (3) How it meets the needs
- Rich latent, structured over persons: yes.
- The other through the own body: yes, exactly, by weight sharing.
- Per-expression, sign-flippable, capped coupling: only through I, with innate caps, so the caps are carried over rather than derived.
- Time scales: none beyond F's own.
- Contingency: none beyond what F learns.

### (4) Novelty verdict (honest)
- **Recombination:** slot attention (soft k-means with a learned shared update) plus the simulation-theory idea of modelling the other with one's own model (Yoshida–Man; SIPS in inverse planning).

### (5) Against the lessons of reports 8, 9 and 12
- It does not rest on copy-blindness, so report 8's first lesson does not bite.
- But the binding A is partner-dependent and changes what z_0 is updated with. That is a new, uncounted route of exactly the kind Q35 and report 12 are about. A bound on I alone does not bound it.

### (6) Most likely concrete failure
- **Competition gives a synchronous partner to the self.**
  - A partner who moves with the agent (lag under the self slot's prediction horizon) is predicted best by z_0, so A routes the partner's features into the self slot.
  - The self model then absorbs the partner: the enfacement failure recorded in the project's note maister-2013-mirror-touch-enfacement.md (seen touch shifting synaesthetes' self-face judgement as felt + seen synchrony does in everyone; source not re-read in this pass).
  - Copying then becomes an attractor of *binding*: the more the agent and partner agree, the more partner input is taken as self, and the closer z_0 is pulled to the partner.
- **Tagging features by source** (camera versus efference) removes the competition. The mechanism then reduces to two separate models plus a capped interaction, which is the existing build's class.
- **The symmetric configuration is distinguished.** With shared F and a symmetric I, z_0 = z_j is a fixed point. This is the equivariance lesson of new-core-search-3, met again.

---

## Direction 3 (closed): body-clocked sampling of the partner

### (1) The object
- The partner's movement enters only as an observation whose precision Π_k(φ(t), u(t)) is set by the agent's own state:
  - φ(t) is the phase of the agent's own body cycles (breath, its own expression cycle);
  - u(t) is its own uncertainty about the joint exchange.
- Π ≥ 0, and nothing partner-derived sets it.
- Al et al.'s dissociation would be two operators: phase on discriminability (a multiplicative noise term) and allocation on the criterion (an additive offset).
- Boukarras et al.'s zero-lag synchrony would arise without coupling. Two agents whose bodies respond to their own uncertainty about a shared task co-vary at zero lag.

### (2) Why it is closed
- **Known.**
  - It is predictive coding or Kalman filtering with state-dependent observation noise **(standard)**: active inference (Allen et al.), an excluded framework.
  - As a coupling route it is the "modulates, never authors" pattern already in the index (phillips-2016 apical amplification; hasani-2021 reversal-bounded conductances).
- **Concrete failure.**
  - Precision is a gain on the partner channel. If the agent's policy may shape its own body timing to sample better, as Allen et al.'s arousal policy does, then precision-seeking pulls the agent's own cycle into phase with the partner's informative moments.
  - The rhythm of the agent's body then entrains to the partner. Rhythm copying becomes an attractor of the epistemic drive, through a route that touches no expression channel and is counted by no ceiling.

### (3) Kept
- **The rule.** Any "attention" route must state whether it moves sensitivity or criterion. The two have different ablation signatures (late versus early evoked responses).
- **The evaluation constraint.** Zero-lag physiological synchrony cannot credit a design with coupling.

---

## Overall verdict

- **No direction clears the bar** of a genuinely new core mechanism on the level of attention.
  - Direction 1 is the strongest and the most concrete. It keeps contingency as content, types the copying operation (an induction head) away from the agent's own output, and gives a derived ablation (the innate shift). But it reduces to a kernel-smoother residual with two dials, and its first concrete failure (C1: 53 % of an independent slow partner cancelled) is measured.
  - Direction 2 makes "through my own body" exact by weight sharing. But its binding competition makes a synchronous partner part of the self, so copying becomes an attractor of binding.
  - Direction 3 is a known pattern, and its epistemic version entrains the agent's own rhythm.
- **Most useful products.**
  1. A per-partner, in-context contingency memory with typed output (Direction 1), as a component the build candidate could use for its appraisal input. It needs an independent critique before any use.
  2. The constraint from Boukarras et al. that physiological synchrony arises co-driven at zero lag even under imposed roles. Evaluation should not read synchrony as following, and a core need not couple bodies to reproduce it.
  3. Al et al.'s sensitivity/criterion dissociation as a required statement for any precision- or attention-type route.

## Next steps
1. If Direction 1 is pursued: an independent critique aimed at (a) the τ/exclusion dials on recorded dyads, by measuring, on Seamless Interaction movement features under D70/D85, how much of each listener's slow, independent movement the head cancels; (b) the G-mirror test; (c) whether the appraisal route from r and c can be bounded per channel against raw movement at lags of minutes.
2. Read, if the hosts open: the "Mathematical Framework for Transformer Circuits" (transformer-circuits.pub), Garfinkel et al. 2014 (J Neurosci), Baker et al. 2017 (BToM, Nature Human Behaviour), Thorson, West & Mendes 2018 (dyadic physiological influence), and the Tomyta et al. supplement (its state-space model).
