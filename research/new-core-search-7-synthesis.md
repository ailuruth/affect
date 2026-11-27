# Searching for a new core mechanism, seventh pass: training objectives under which affect-like structure could emerge, and whether each closes the approval route (synthesis, 2026-11-27)

**Scope of this pass.** Pass 6 concluded that what emerges in a learned latent is set by the training objective, the data and the time-scale layout, so a new core would have to be a new **objective**, not a new operator. The per-expression copy ceilings are taken as given (D93; research/foundations/conjecture-five-passes.md). This pass reads objectives in three families (self-supervised predictive and world-model objectives; intrinsic objectives: learning progress, empowerment, curiosity; affect-like read-outs of such objectives) and asks of each whether it avoids the **approval route**: the partner's reaction or preference becoming a training signal for the agent's own expression (pass 5: Fong et al.'s request wire; Sharma et al.'s preference-driven sycophancy; dwell-time selection as its no-learning twin).

## Sources read (notes in research/)
| Note | Area | How fully |
|---|---|---|
| bardes-2024-v-jepa.md | predictive objective (JEPA) | full main text (arXiv); appendices not read |
| hafner-2023-dreamerv3.md | world-model objective | full main text (arXiv); methods appendix and supplementary curves not read |
| hafner-2020-action-perception-divergence.md | unifying objective lattice | §1–5 in full (arXiv v3); appendices A–C not read |
| salge-glackin-polani-2014-empowerment-introduction.md | empowerment | §4.1–4.5, QLG (§4.6.8–4.6.11), §4.7.1–4.7.2 and conclusion in full; §4.6.1–4.6.7 skimmed |
| mohamed-rezende-2015-variational-empowerment.md | empowerment (scalable) | main text in full (arXiv); appendices not read |
| oudeyer-kaplan-2007-intrinsic-motivation-typology.md | learning progress and the typology of intrinsic objectives | full text (Frontiers HTML); equations are images and were read only through their text descriptions |
| pathak-2017-intrinsic-curiosity-module.md | curiosity and the noisy-TV problem | §1–4.2 and §6 in full; §4.3 and §5 skimmed |
| pattisapu-2024-free-energy-circumplex.md | affect-like read-outs of an objective | full text (arXiv) |

Already in the index and used here without re-reading: van den Oord et al. 2018 (CPC), Oudeyer, Kaplan & Hafner 2007 (IAC), Schmidhuber 2010 (compression progress), Burda et al. 2019 (noisy TV), Joffily & Coricelli 2013 (valence = −dF/dt), Hesp et al. 2021, Stephan et al. 2016, Saxena et al. 2021 (CW-VAE), Lachapelle et al. 2022, Sharma et al. 2024.

**Not reachable from here** (nothing below rests on them):
- LeCun 2022, "A Path Towards Autonomous Machine Intelligence" (JEPA position paper): openreview.net does not resolve for this session and returns a script page to curl; no arXiv version.
- Klyubin, Polani & Nehaniv 2005 (both empowerment papers): no arXiv copy; the University of Hertfordshire repository is refused by the proxy. Their results are used only as reported by Salge et al., and marked so in that note.
- Kiverstein, Miller & Rietveld 2019 (*Synthese*, "The feeling of grip", error dynamics): Springer and core.ac.uk are refused by the proxy; pure.uva.nl does not resolve.
- Van de Cruys 2017 ("Affective value in the predictive mind", Open MIND): open-mind.net refused by the proxy.
- Eldar, Rutledge, Dolan & Niv 2016 (mood as momentum, *Trends Cogn. Sci.*): the PMC page returns a CAPTCHA.
- Gottlieb, Oudeyer, Lopes & Baranes 2013 (*Trends Cogn. Sci.*): the HAL copy is refused by the proxy.

Area 3 (affect-like dimensions emerging from such objectives) is therefore thin: one toy active-inference paper (Pattisapu et al.), plus the already adopted Joffily & Coricelli and Hesp et al. arxiv.org and frontiersin.org worked.

**Checks.** None were run in this pass. The two derived statements below (Proposition 1 and the mirror property of Direction 1) are short arguments, not simulations.

**Vocabulary.** No emotion labels or named emotion variables appear below the Claude layer in the directions. "Channel" is a face or voice feature in the agent's own coordinates; "body variable" is one of the innate regulated variables; "need" is a body variable's deficit; "partner features" are the partner's face, voice and words read into the agent's own coordinates.

## What this pass adds
- **A lattice that every candidate objective falls into** (Hafner et al., APD). Any objective of the form "choose latents z and a target τ(x, z), minimise KL[p_φ ‖ τ]" splits into **past terms** (ELBO or contrastive bounds: representation learning) and **future terms** (preferred future inputs, information gain, empowerment, skills). Past terms shape the latent and never select actions; only future terms train behaviour. Active inference, KL control, MaxEnt RL, empowerment, curiosity and skill discovery are all members.
- **Representation is set by the prediction objective, not the reward** (DreamerV3: performance "predominantly rests on the unsupervised reconstruction loss"; V-JEPA: the masking scheme, i.e. what is predicted from what, moves frozen K400 accuracy from 51.5 to 72.9, more than any other choice).
- **Every intrinsic objective read has a dyadic failure of the same kind:**
  - empowerment with the partner's face among the sensors rewards making the partner maximally responsive to the agent (Salge et al.: "empowerment is about influencing the world one can perceive");
  - learning progress over a pool that includes the partner rewards learnable partner responses; the Playground robot's turn to vocalising at an "adult" robot is the developmental form (Oudeyer & Kaplan);
  - synchronicity motivation over mixed self/partner channels is a copy drive by construction (Oudeyer & Kaplan's typology);
  - prediction-error curiosity on inverse-model features keeps exactly the parts of the partner that reveal the agent's own action, i.e. the contingent and mirrored parts, and rewards their unpredictability (Pathak et al., derived here);
  - a valence read-out defined as log preference of outcomes, U − EU (Pattisapu et al.), becomes the partner's reaction against expectation as soon as outcomes include the partner's face.
- **Option restriction gives avoidance without labels** (Mohamed & Rezende: an empowerment agent moves away from a predator). It is the cleanest case read so far of an agent-directed avoidance tendency arising from an objective about the agent's own options.
- **Model structure decides whether a read-out can settle** (Pattisapu et al.: an agent with no "absent" state cycles in negative regions to the end of the run).

## A derived criterion: when an objective opens the approval route

**Setting.** θ are the parameters that generate the agent's expression (the policy over its own channels and any decoder trained by return). J(θ) = E[f(τ)], where τ is a trajectory containing the agent's own body outcomes o, its own channels y, and the partner's features u, with the partner's response policy P mapping the agent's past expression to u. The score-function gradient is ∇_θ J = E[(f(τ) − b(s)) Σ_t ∇_θ log π_θ(y_t | s_t)] for any baseline b that does not depend on y.

**Proposition 1 (approval route of an objective).** Call J approval-closed if ∇_θ J does not depend on P (for fixed environment and body dynamics).
- (a) If f reads u directly (the partner's face or words in the reward, the preferred inputs, the sensors of empowerment, the pool of a curiosity or progress measure), J is not approval-closed: choose P that produces high-f partner features only after expressions in a set A; ∇_θ J then points toward A.
- (b) If f reads only the agent's own body outcomes o, J is approval-closed **if and only if** no path u → o exists in the body dynamics. If such a path exists (a body variable whose deficit the partner's behaviour reduces or raises), the same construction applies through it: a partner who reduces the deficit only after A makes ∇_θ J point toward A. "Own-body only" closes the route only for an asocial body.
- (c) The route can be closed while the path exists only by evaluating f under the intervention do(u = u⁰) in credit assignment (the neutral-partner counterfactual), which removes every partner-mediated consequence of the agent's expression from the objective. Contingency then stays in the state (D81) but not in what the agent learns to do.

*Argument.* (a) and the "if" of (b) are the definition plus the score-function identity: if f's conditional law given (y, s) does not depend on P, neither does the gradient. The "only if" of (b) is the construction. (c): under do(u = u⁰), f's law no longer depends on P. ∎

**Consequences.**
1. **Past-term objectives are approval-closed** as long as no reward or value gradient flows into the encoder that the expression reads. DreamerV3 lets reward and value gradients reach the representation (its ablation stops them); the engine must not.
2. **Future-term objectives (every intrinsic objective read here) face a dichotomy:** either they score something the partner can move (open), or they are closed by the neutral counterfactual and become blind to how the agent's own expression changes the partner's effect on it. Pass 5's coplay typing, the build core's "drafts scored on the agent's own predicted body change" and its shadow run are instances of (b) and (c).
3. **The cut in (c) needs the partner as an explicit node.** A world model that absorbs partner-mediated effects into a learned map from the agent's own action to its own body (which a predictor conditioned on own action will do whenever the partner is contingent) cannot be evaluated under do(u = u⁰): there is no u to hold. Approval closure therefore constrains the world model's factorisation, not only the loss.
4. **The selection route survives all of this.** Proposition 1 is about learning. Pass 5's dwell-time selection (occupancy shift with no learning) is untouched by any choice of objective and must still be audited.

This is the objective-level counterpart of the conjecture's Corollary 1c (self-invariance removes the partner's answers) and of derivation Theorem 6 (invariance erases contingency). Path-specific objectives in the agent-incentives literature (for example Farquhar, Carey & Everitt 2022) are the likely prior art for (c); they were **not read** in this pass, so the reduction is flagged, not asserted.

---

## Direction 1: the own-body predictive objective. Targets are only the agent's own body and channels; the partner is context only

### (1) The object
- **Streams** (30 Hz frames, event-time words): own body variables b_t ∈ ℝ^{n_b} (innate set), own channels m_t ∈ [0, 1]^m (efference, in the agent's own coordinates), partner features u_t (face and voice through the agent's inverse body model; word and turn events).
- **Encoder.** A hierarchical state-space encoder E_θ (the build core's slow-state layout; CW-VAE clocks or an RSSM) maps (b, m, u)_{≤t} to z_t = (z_t^1, …, z_t^L).
- **Target typing (the one new choice).** Prediction targets are only g_t = (b_t, m_t). Partner features are inputs, never targets, and are never masked targets in replay.
- **Loss** (JEPA form, V-JEPA Eq. 1, with action conditioning):

  L_own(θ, ϕ) = Σ_{k ∈ K} Σ_t ‖ P_ϕ^k(z_t, m_{t+1:t+k}) − sg(Ē(g_{t+k})) ‖₁ + free-bits KL per level (Saxena et al.; DreamerV3),

  with horizons K = {0.2 s, 2 s, 30 s, 10 min} (CPC: the horizon set fixes the time scale the latent must hold) and Ē an EMA of a small own-body target encoder.
- **Online vs replay.**
  - Online: inference only (encoder forward pass, levels ticking on their clocks); no weight updates; no planner.
  - Nightly replay: L_own with forward (causal) targets, plus masked bidirectional prediction over own-body tokens with partner tokens always visible as context (V-JEPA's causal[12] vs multi-block gap, 71.9 vs 72.9 on K400 and 63.6 vs 67.4 on SSv2, says replay should use both).
- **Expression** is not trained by this objective. It is the build core's innate display prior plus the decoder learned by self-reproduction (S4), behind the per-channel ceilings; words come from Claude.

### (2) What it gives (derived)
- **Affect-like coordinates by construction.** Every latent direction survives only by predicting the agent's own future body and channels. The read-out pass 6 proposed as an evaluation (directions predicting the agent's own drive change, Direction 3) becomes what the latent is made of. The sign of change of the predicted need (Joffily & Coricelli's −dF/dt, already adopted) and the predictor's own uncertainty per level (Pattisapu et al.'s posterior entropy) are read-outs, not variables.
- **A mirror partner is invisible to the latent.** If u_t = h(m_{≤t−δ}) + ε with ε independent of the agent's future, then I(g_{t+k}; u_{≤t} | b_{≤t}, m_{≤t+k}) = 0: u adds nothing the agent's own past does not already give, so the loss gives no incentive to encode it, and the free-bits floor makes encoding it a cost above the floor. A contingent partner who adds information about the agent's own body future (deficit reduction or load) is encoded, but only through that part.
- **"You responded to me" is kept as a prediction, and its absence as an error.** With a contingent partner, the effect of the partner's answer is absorbed into the map from the agent's own channels to its own body. If the partner stops answering (still-face), that map mispredicts: a prediction error on the agent's own body, at the horizon where the answer was expected.
- **Partner knowledge is restricted to what bears on the agent.** Partner states that never affect the agent's body or channels are dropped (ICM's type-3 sources). D81's fuller knowing would need a separate partner-model learner (pass 5, Direction 1), typed so that its targets are the partner's features and its output reaches the expression learner only as forward input.

### (3) Q18 check, with the ceilings given
- No route outside the ledger: L_own trains no expression parameter; every route from z to expression passes the per-channel caps.
- **Claude route.** Slow levels will hold the partner's persistent state whenever it predicts the agent's own body (a person's steady manner predicts reduction of a need). They reach Claude by changing how it processes, which the face ceilings do not see. Pass 5's three content probes (challenge, stated preference, framing) apply.
- **Selection.** Without a planner there is no learned selection, but anything that biases what the agent attends to from z can shift occupancy (pass 5, C1). Audit as before.

### (4) Approval route
- **Closed for learning, by structural fact:** L_own is a past-term objective (APD Eq. 6), its targets contain no partner features, and no reward or value gradient enters E_θ (Proposition 1, consequence 1).
- **Opens the moment a planner uses P_ϕ to choose expressions.** P_ϕ predicts the agent's own body from its own planned channels, with partner effects folded in; planning on it is Proposition 1(b) with the path u → o present. Because the partner is not an explicit node in P_ϕ, the do(u = u⁰) cut of 1(c) cannot be applied to it (consequence 3). So the object must stay planner-free, or carry an explicit partner node used only for the cut.

### (5) Reduction check (honest)
- JEPA / CPC with a typed target set; the CW-VAE level layout and free bits for time scales; predicting one's own sensor signals over several horizons is the general-value-function programme in RL **(standard; not read here)**.
- In the linear-Gaussian case the mirror property is partialling out: the partner enters through its innovation relative to the agent's own past, which is the echo-canceller result of the self-invariant-maps derivation reached through the loss instead of the architecture; the information measure involved is transfer entropy from partner to own body (index: Barnett et al.).
- **Verdict: recombination.** Target typing is a design choice inside APD (a choice of x and τ), not a new objective. It is the most useful product of this pass for the build core.

---

## Direction 2: floored own-body empowerment. A satiable capacity drive over the agent's own action → own body channel

### (1) The object
- **Capacity.** For model state s and horizon n (0.5–5 s of motor sequence), own-body empowerment

  E_b(s) = max_{ω} I(A_{t:t+n}; B_{t+n} | s),

  estimated by the variational bound E ≥ H(A | s) + E[log q(A | B_{t+n}, s)] (Mohamed & Rezende), whose decoder q is the agent's own inverse body model, or by the quasi-linear Gaussian form ½ Σ_i log(1 + σ_i P_i) over the singular values of the local Jacobian ∂b_{t+n}/∂a (Salge et al., Eq. 4.31). Sensors: own body variables only.
- **Two variants for the partner:**
  - *E_b^cut*: evaluated under do(u = u⁰);
  - *E_b^full*: partner-mediated paths a → u → b counted.
- **Satiable drive** (Principle 6): D_E(s) = max(0, E* − E_b(s)) with an innate floor E* per need family, entering the homeostatic objective with the body deficits; its read-out is −dD_E/dt.
- **Contexts.** Context-dependent capacity E_b(k) over learned contexts k, with Klyubin et al.'s minimal optimal context K_opt = argmin H(K) s.t. E(K) = E(R) (as reported by Salge et al., Eqs. 4.10–4.12): contexts are split only where they change how the agent's actions affect its own body.
- **Online vs replay.** q and the Jacobian model are refit nightly; E_b is evaluated online from the current model (QLG cost is one SVD per step).

### (2) What it gives (derived)
- **A capacity form of the efficacy coordinate** of pass 6 (Stephan et al.): not "is my surprise falling" but "how much can my actions still do to my body here", per context.
- **Avoidance of option-restricting contexts without labels** (the predator result), and context keys that come from the agent's own control channel, not from content.
- **Bounded:** E_b ≤ log of the distinguishable body states, and D_E = 0 above the floor.

### (3) Q18 check, with the ceilings given
- Expression is bounded by the caps whatever D_E does. The hazards are selection and Claude, as in Direction 1, plus one specific to this object: the Greek-gods flattening. Measured through a high-capacity latent, E_b goes flat and D_E carries nothing (Salge et al., §4.5.4).

### (4) Approval route
- **E_b^full is open, and it is an attention drive.** The capacity counts the agent's ability to make the partner regulate its body, so raising it means making the partner reliably responsive to the agent (Proposition 1(b)). That is Principle 6's "attention" by another name.
- **E_b^cut is closed but asocial.** In a screen dyad the partner has no physical path into the agent's body except through u. Under do(u = u⁰), E_b is then independent of the partner altogether (Proposition 1(c)), and the contexts K_opt never split by person.
- **The dichotomy is exact here:** social and open, or closed and about the body alone.

### (5) Reduction check (honest)
- Empowerment (Klyubin et al. via Salge et al.; Mohamed & Rezende) with own-body sensors, plus a homeostatic floor (homeostatic RL; Keramati & Gutkin in the index), plus the efficacy level of Stephan et al. In APD it is the "actions with expressive target" row restricted to body inputs.
- **Verdict: recombination, and rejected as a core:** its social form violates Principle 6 and its closed form carries nothing about the partner.

---

## Direction 3: typed learning progress. Progress of the own-body predictor, regions split on own state only

### (1) The object
- The Direction 1 predictor P_ϕ supplies errors ε_t on the agent's own body targets. Regions R are split adaptively (IAC) on **own-state features only** (b, m and the slow latent levels), never on partner features.
- Reward r_t = −(ε̄_R(t) − ε̄_R(t − θ)) for the region containing s_t (Oudeyer & Kaplan's LPM), used to bias which own-body regulation strategies the agent practises.
- Online: errors and region statistics; nightly: predictor refit and region splits.

### (2) What it gives (derived)
- **Self-limiting:** progress vanishes once a region is learned; noise gives no progress (Schmidhuber's argument; the noisy-TV failure of plain prediction error, Burda et al., does not arise).
- **A mirror partner gives only transient progress:** learning that the partner mirrors the agent is quick, after which there is nothing left to learn and the reward falls to zero. The copy attractor earns nothing in the long run.
- The read-out −dε̄/dt per region is Joffily & Coricelli's −dF/dt averaged over a region; per region and over the slow levels it is the pass 6 efficacy field.

### (3) Q18 check, with the ceilings given
- Expression bounded by the caps. Practice selection is a selection route and must be audited for occupancy shift.

### (4) Approval route
- **Open.** Regions are keyed on own state, but the predictor's errors depend on the partner whenever the partner moves the agent's body. A partner who answers in ways that are new but learnable produces progress in the regions where the agent's expressions elicited them, so those expressions are practised more. That is engagement-seeking (the Playground robot vocalising at the "adult"), a partner's responsiveness turned into reward without naming it. Closing it with do(u = u⁰) leaves progress on body physics alone (Proposition 1(c)).

### (5) Reduction check (honest)
- IAC / compression progress applied to an own-body predictor; identical in substance to pass 6's Direction 1 (efficacy as learning progress on regulation error). **Verdict: recombination.**

---

## Overall verdict

- **No direction clears the novelty bar.**
  - Direction 1 (own-body predictive objective) is JEPA/CPC with a typed target set, inside the APD lattice. It is approval-closed for learning by a structural fact (past-term objective, no partner targets, no reward gradient into the encoder). It makes a mirror partner invisible to the latent by an information argument, and keeps "you responded to me" as a prediction and its withdrawal as an error. It reopens the route the moment a planner uses it.
  - Direction 2 (floored own-body empowerment) is empowerment plus a homeostatic floor. It is exactly dichotomous: with partner-mediated paths it is an attention drive (Principle 6); without them it is asocial.
  - Direction 3 (typed learning progress) is IAC on the own-body predictor and pass 6's Direction 1 again. It is open: it rewards eliciting learnable partner responses.
- **Why everything reduces, in this area.**
  1. **APD absorbs every objective of the kind asked for.** Choosing which variables are latents, which are targets and what the target distribution prefers is APD's recipe. A "new objective" is a new choice inside the lattice unless it leaves the KL family, and none read or derived here does.
  2. **Approval closure is decided by which terms train behaviour, not by how clever the objective is** (Proposition 1). Past terms are closed; future terms are open whenever the partner can move what they score; closing them by the neutral counterfactual makes them blind to the partner-mediated consequences of the agent's own expression. That is the shadow run applied to the objective, which the build core already does.
  3. **Affect-like structure emerges where the targets are.** Directions predicting the agent's own body change are what an own-body predictive objective is made of, so the read-outs Principle 2 asks for come out of Direction 1 without labels. That is a consequence of target typing, which is a design choice, not a mechanism.
  4. **Every intrinsic drive read here becomes an attention or engagement drive in a dyad** unless it is typed to the agent's own body and cut from partner-mediated paths. Synchronicity motivation over mixed channels is a copy drive outright.
- **Most useful products for the build core** (none needs a new design):
  1. **Target typing for the slow state's training objective:** prediction targets are only the agent's own body variables and channels; partner features are context only. It strengthens pass 6's typing rule from "slow levels read only the level below and own regulation statistics" to an objective-level statement with the mirror-invisibility property.
  2. **No reward or value gradient into the encoder the expression reads** (Proposition 1, consequence 1; DreamerV3 shows the default lets them in).
  3. **If any planner ever chooses expressions, the partner must be an explicit node of the model it plans with**, so the neutral-partner cut can be applied to its value (consequence 3).
  4. **Audit list additions:** synchronicity-type rewards over mixed self/partner channels (copy drive); inverse-model features over the dyad (concentrate on mirrored channels); empowerment or progress measures with partner-mediated paths (attention drive); any valence-like read-out defined on outcomes that include partner features.
  5. **Evaluation:** the still-face withdrawal should appear as an own-body prediction error at the horizon of the expected answer (Direction 1); this is a lesion prediction for the battery.

**designs.md:** no candidate deserves a line as a new design. Products 1–3 are refinements of the Cayley-ledger build core's training objective and belong in its specification if adopted.

## Next steps
1. Read, if the hosts open: LeCun 2022 (openreview.net), Klyubin et al. 2005 (both papers), Kiverstein et al. 2019 and Van de Cruys 2017 (error dynamics as affect; the area this pass could not reach), Eldar et al. 2016.
2. Read the agent-incentives literature on path-specific objectives and instrumental control incentives (for example Farquhar, Carey & Everitt 2022; Everitt et al. on causal influence diagrams) to check whether Proposition 1 and its consequence 3 are already stated there. If so, cite them; if not, Proposition 1 is still a standard argument and not a core.
3. If the search continues, the one direction this pass leaves open is an objective outside the KL family (APD's own suggestion: other divergences give other families). Nothing read says such an objective would change Proposition 1, whose argument uses only the score-function identity.
