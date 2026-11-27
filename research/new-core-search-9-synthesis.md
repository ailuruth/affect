# Searching for a new core mechanism, ninth pass: which learning signal shapes the infant's own output under contingent feedback, and can any form of it be approval-closed (synthesis, 2026-11-27)

**Scope of this pass.** Pass 7 derived (Proposition 1) that an objective keeps the partner's reaction out of the agent's expression learning only if it scores nothing the partner can move. Pass 8 found that infant expression is shaped by own-state regulation through the partner (open), and that the copy limit lives in the caregiver's policy. This pass reads the most direct evidence on contingent learning of the infant's **own output** (vocal, because that is where the experiments are), asks which signal shapes the output in each study, whether it is approval-closed by pass 7's rule, and what follows for the engine with the per-expression ceilings taken as given (D93; research/foundations/conjecture-five-passes.md).

## Sources read (notes in research/)
| Note | Area | How fully |
|---|---|---|
| goldstein-schwade-bornstein-2009-vocal-extinction-burst.md | infant output learned from partner response; still-face extinction burst | full text (PMC author manuscript); figures by caption |
| warlaumont-2014-social-feedback-loop.md | naturalistic partner contingency on content and the child's dependence on it | full main text (PMC); supplement (model, statistics) not read |
| kuhl-tsao-liu-2003-social-gating-phonetic-learning.md | social gating of learning (perception) | full text (PMC) |
| takahashi-fenley-ghazanfar-2016-marmoset-turn-taking.md | partner timing on the infant's own fluctuation; self-monitoring onset | full text (PMC) |
| ghazanfar-liao-2018-marmoset-constraints-flexibility.md | contingent vs total feedback; the closed-loop twin experiment as reported | full text (PMC author manuscript; short review) |
| teramoto-2017-vocal-development-waddington-landscape.md | formal model: feedback as a rate on an own-body cost | introduction, results, discussion in full; methods skimmed; appendix not read |
| warlaumont-finnegan-2016-reward-modulated-babbling.md | self-scored output reward vs partner-scored, yoked control | full article (PLOS); algorithm and table images through the text |

Already in the index and used without re-reading: Goldstein & Schwade 2008 (contingent vs yoked maternal responses reshape babbling within 10 min; infants take up the pattern, not the phonemes), Gergely & Watson 1996, Bornstein & Manian 2013, Tronick & Beeghly 2011, Rayson et al. 2017, Heyes 2016, Maister et al. 2020, pass 7 and pass 8 syntheses.

**Not reachable from here** (nothing below rests on them):
- Goldstein, King & West 2003 (*PNAS*, contingent vs yoked maternal responses and babbling): PMC (PMC164707) served a reCAPTCHA bot check (not bypassed); pnas.org returns 403; babylab.cornell.edu does not connect. Its result is used only as cited by Goldstein et al. 2009 and Warlaumont et al. 2014, and marked so.
- Takahashi, Liao & Ghazanfar 2017 (*Curr. Biol.*, closed-loop twin experiment): no open copy found; cell.com and oar.princeton.edu do not connect. Used only as reported by Ghazanfar & Liao.
- Carouso-Peck & Goldstein 2019 (*Curr. Biol.*, contingent female visual feedback shapes zebra finch song non-imitatively): the only copy found is on babylab.cornell.edu, which does not connect.
- Albert, Schwade & Goldstein 2018 (*Dev. Sci.*, review of the social feedback loop): PMC6004332 served a bot check.
- Gergely & Watson 1999, Fonagy & Gergely 2007, Bigelow & Rochat 2006: still no reachable copy (psychology.emory.edu and discovery.ucl.ac.uk do not connect; no PMC copy).
- europepmc.org returns 403; the NCBI E-utilities and api.semanticscholar.org (429) were not usable, so searches went through a web search and direct PMC pages; PMC answered some pages and served a bot check on others (PMC8204797, a marmoset paper, among them).

The contingency-detection side (Gergely & Watson's model, Bigelow) is therefore again not read in the original; this pass rests on the vocal-learning literature, which is where the contingent-vs-yoked experiments are.

**Checks.** One tiny numpy illustration of Proposition 3 was run (scratchpad, not kept in the repository). **It is not evidence.** A scalar own-body optimum at 1.0, noisy gradient steps, 20,000 steps, mean of 5 runs: no gate 0.98; predictable gate (partner engagement varying slowly, set before each sample) 1.02; adapted gate (partner answers when the step moves toward its preferred side) −0.08. It only illustrates the algebra below.

**Vocabulary.** No emotion labels or named emotion variables appear below the Claude layer in the directions. "Channel" is a face or voice feature in the agent's own coordinates; "body variable" is an innate regulated variable; "partner features" are the partner's face, voice and words read into the agent's own coordinates; "innovation" ξ_t is the agent's own logged motor noise (pass 8). Call-type names in the marmoset notes are the sources' acoustic categories.

## What this pass adds
- **Every study that shapes the infant's output does it through a signal that covaries with the infant's own output.**
  - Goldstein & Schwade 2008 (index) and Goldstein, King & West 2003 (as cited): contingent maternal responses reshape the form of babbling; yoked responses with the same amount, form, touch and smiling do not (they only raise how much the infants vocalize).
  - Ghazanfar & Liao (reporting Takahashi et al. 2015, 2017): the number of **contingent**, not total, parental calls predicts when marmoset calls mature (≈10-40 days); in randomised twins, high-contingency playback speeds maturation.
  - Takahashi et al. 2016: parents time their calls on a preferred phase of the infant's own ≈0.1 Hz acoustic fluctuation (≈230°, the noisier-to-more-tonal transition); infant calls within 5 s after a parental call are more tonal and longer. The partner's content is constant; its **timing** carries the selection.
  - Warlaumont et al. 2014 (13,836 h): adults answer speech-related vocalizations more (+0.065), and the next vocalization is more speech-related after an answered one (+0.036), compounding over more than 2,000 vocalizations a day.
  - Warlaumont & Finnegan 2016: a spiking model learns syllabic output from a reward on its own sound's salience; a yoked reward schedule teaches nothing.
- **The learned output converges on what the partner answers** (receiver predisposition: parents answer more-adult-like calls; Ghazanfar & Liao). In pass 7's terms every one of these signals is Proposition 1(a): open. Human and marmoset output learning use the approval route; pass 8 found the same for expression.
- **The signature of that route is a channel-specific extinction burst** (Goldstein, Schwade & Bornstein): when an unfamiliar partner goes still, 5-month-olds' vocalizing rises to a peak at a median 75 s and falls (F(2,74) = 10.88, ηp² = .23; 37 of 38 infants peak), while smiling only falls and is uncorrelated with vocalizing (ps > .42). Natural schedules are partial (30-50 % answered), which makes the learned elicitation resistant to extinction.
- **A social gate on learning need not be a reward on output** (Kuhl, Tsao & Liu): live Mandarin sessions reverse the decline in a non-native contrast (65.7 % vs 56.7 %, F(1,19) = 7.34), the same speakers on DVD give nothing, and more attention (AV 2.79 vs audio 1.48) does not help. This is a gate on perception learning, and it is not attention.
- **One formal model puts the partner only in the rate** (Teramoto et al.): C_t(θ) = −log g_t(θ) + λ₀θ − (δ + κF)tθ; the direction of learning is the infant's own vocal gain, the partner's contingency F only sets the speed, and F = 0 still converges. The model is direction-free only because F is averaged per infant; the phase result above says the biological F is not.

## Proposition 3 (gated learning of own output: predictable gates rescale time, adapted gates steer)

**Setting.** As in pass 7 and 8. An output-side learner updates parameters θ by Δθ = η Σ_t w_t h_t over credit events t. Here h_t is any statistic of the agent's own output in the credit window starting at s_t: a score ∇_θ log π_θ(y_t | s_t), a sample of the gradient of an own-body objective, or a correspondence pair. w_t ≥ 0 is any weight the step receives: a reward, a learning-rate gate, a replay priority or a sampling probability. Write ḡ(θ) = E[h_t | 𝒢_t] for the own-objective gradient, where 𝒢_t is the information before s_t (agent history before the window, partner randomness), and assume the own objective has no partner path (Proposition 1(b)).

**Claim.**
- (a) **Predictable gate.** If w_t is 𝒢_t-measurable (fixed before the credited innovations are drawn), then E[w_t h_t] = E[w_t ḡ(θ_t)]. The mean dynamics are dθ/dt = w(t) ḡ(θ), a time change of the own-objective gradient flow: for a scalar gate the orbit and the fixed points are those of ḡ, whatever the partner does. A per-block (per-channel) gate changes the path but not the set of fixed points.
- (b) **Adapted gate.** If w_t depends on partner features after s_t (a response, a phase-locked call, a reaction-tagged replay priority), then E[w_t h_t] = E[w_t]ḡ + Cov(w_t, h_t − ḡ), and the partner policy controls the covariance term. With w_t = 1 + c·1[⟨h_t − ḡ, a⟩ > 0] the mean drift gains a component along a for any chosen direction a, and the fixed point solves E[w h] = 0, which is not the own optimum. No valenced content is needed: timing alone suffices (Takahashi et al. 2016).
- (c) **The closed arm is the yoked arm.** A predictable gate is what a yoked control delivers: the same amount and timing of partner input with no covariance with the learner's own output. In every experiment read or cited here, the yoked arm learns no partner-shaped form (Goldstein & Schwade 2008; Warlaumont & Finnegan 2016; Takahashi et al. 2017 as reported). So the approval-closed version of social output learning is, empirically, the version that teaches no partner-specific form.

*Argument.* (a): w_t is 𝒢_t-measurable, so E[w_t h_t] = E[w_t E[h_t | 𝒢_t]]. A positive scalar time change of an autonomous flow preserves its orbits and zeros. (b): direct expansion; the construction picks the sign of the noise projection. (c): definition of the yoked design. ∎ (This is pass 8's instrumental argument read from the gate's side: pass 8 asked what the partner's response is correlated with; this asks what a step weight is correlated with.)

**Caveat.** With stochastic steps, a predictable scalar gate still sets the effective step size ηw, which can change which basin of a multi-optimum own objective is reached (noise temperature). Every reachable end point is still an own-objective optimum; the partner can choose among them only through speed.

---

## Direction 1: predictably gated own-body output learning (the Teramoto form, typed)

### (1) The object
- **Own-output objective.** J_own(θ) on the agent's own production only: for the voice, a fixed innate auditory model's measure of the agent's own sound (the gain g of Teramoto et al., or a salience measure as in Warlaumont & Finnegan, scored by the agent's own model on its own efference copy, not on the microphone mix); for the face, the S4 self-reproduction loss of the agent's own decoder. No partner features in J_own (pass 7, Direction 1 typing).
- **Gate.** A per-night scalar w_n ≥ 0 per channel block, computed in replay from the **previous** day's statistics (for example the partner's liveness rate or the day's own-body prediction-error level), frozen before the night's update.
- **Update.** θ_{n+1} = θ_n + η w_n Σ_{t ∈ B_n} h_t, with B_n a replay batch disjoint from, and sampled independently of, the events that set w_n; h_t the gradient of J_own on that batch. Output stays behind the per-channel ceilings.

### (2) What it gives (derived)
- Learning of the agent's own production toward innate body optima, faster on days of social engagement and still converging with none (Teramoto's δ path).
- Proposition 3(a): end points independent of the partner policy; a partner cannot create a fixed point, so no learned copy attractor.
- A Kuhl-style social gate on learning that is neither reward nor attention, if the gate is liveness and not "the partner answered me".

### (3) Q18 check, with the ceilings given
- Output ≤ c_j on every channel (the conjecture's bound is on the output). Per channel the learned strength is set by the own objective, so it is per expression and bounded; sign flips and context-setting must come from elsewhere (context keys, Claude); copying is never a fixed point of the learning (Proposition 3(a)). Remaining routes: selection and Claude, as in passes 5 and 7.

### (4) Approval route
- **Closed, by structural fact:** the gate is 𝒢-measurable with respect to the innovations it credits (computed the night before, applied to a disjoint batch), and J_own has no partner path. Both are auditable: the first by data lineage (which events set w and which events are in B), the second by pass 7's typing.
- **Opens** as soon as the gate is computed from the same events it weights, or event-level (a response within 5 s of the credited act), or as soon as J_own is scored on the microphone mix that contains the partner.

### (5) Reduction check (honest)
- A learning-rate schedule on an own-objective gradient; three-factor (neuromodulated) plasticity with a social third factor; a time change of gradient flow. Teramoto et al. is the model, Kuhl et al. the gating evidence.
- **And by Proposition 3(c) it gives no partner-shaped form:** it is the yoked arm. The brief's "manner of speaking learned by living with people" does not come out of it beyond speed.
- **Verdict: recombination.** Useful product: the predictability condition, which turns "social gating of learning" into an auditable lineage check.

---

## Direction 2: contingent response credit (the signal infants and marmosets actually use)

### (1) The object
- Output policy π_θ over own channels (behind the ceilings). Credit r_t = 1[partner response in (s_t, s_t + Δ)], Δ = 1-5 s (Warlaumont 1 s; Takahashi 5 s; Goldstein 2 s), on a natural partial schedule.
- Update: ∇_θ J = E[(r_t − b) ∇_θ log π_θ(y_t | s_t)], nightly in replay.

### (2) What it gives (derived)
- Fast, relationship-specific shaping of the agent's own output toward what this partner answers (Goldstein & Schwade: within 10 minutes; Warlaumont: compounding small contingencies); an instrumental "my act brings an answer" expectation; and, on withdrawal, a channel-specific extinction burst.

### (3) Q18 check, with the ceilings given
- The output bound holds. **Inside the band it fails D78 condition 4:** the learned direction is the partner's selectivity (receiver predisposition), so a partner who answers only when the agent's channel matches theirs makes matching the learned optimum on every such channel, held at c_j. It also fails Principle 6: the credit is the partner's attention to the agent.

### (4) Approval route
- **Open, by structural fact:** the credit reads u directly (Proposition 1(a)); equivalently the gate is adapted (Proposition 3(b)).

### (5) Reduction check (honest)
- Operant conditioning with a social reinforcer; REINFORCE with a partner-response reward; Warlaumont & Finnegan's DA-modulated STDP is a spiking implementation.
- **Verdict: reduces, rejected.** Product: the **extinction-burst probe** for the battery. Run two copies of the agent through the same partner input stream, one with the partner contingent on the agent's output and one yoked (Ghazanfar & Liao's twin design), then a still face. Any channel whose still-face rate rises and falls in the contingent copy but not in the yoked copy was trained by an approval route. Rate and timing references: a peak about 75 s into a 2-min still face in 5-month-olds; vocal channel only; not in smiling.

---

## Direction 3: lineage typing of every step weight (replay priority, sampling, gates)

### (1) The object
- For every learner L in the engine whose output reaches expression through any path, and every weight w on its training steps (reward, gate, replay priority, sampling probability, tag), a lineage record: the set E(w) of events that w was computed from, and the set C(w) of credited events it weights.
- **Typing rule:** w is admissible for L only if every partner-feature event in E(w) precedes the start of every credited window in C(w) and is independent of them (𝒢-measurable). Otherwise L must be a past-term (representation) learner with no gradient path to expression (pass 7, consequence 1; pass 8, product 3).

### (2) What it gives (derived)
- Closes the route Proposition 3(b) identifies for weights that are not rewards. The case that matters in the build is S6's state-tagged replay: a replay priority raised by the partner's reaction after the agent's act is an adapted gate, so whatever it trains toward expression is trained by approval even though no reward exists.
- It keeps relationship-specific replay (S6) possible: tags from the agent's own state and own prediction errors before the credited window, or tags on representation learners only.

### (3) Q18 check, with the ceilings given
- No new expression parameter; it removes one way learning could make copying attracting inside the band.

### (4) Approval route
- **Closed for every typed weight, by structural fact:** the lineage condition (partner events in E(w) precede and are independent of C(w)). Like pass 8's r = B * ξ, it reduces the audit to a check on named objects.

### (5) Reduction check (honest)
- Prioritised experience replay with a causal-masking constraint; the predictable-integrand condition of stochastic calculus; selection-bias control in off-policy learning. Prioritised replay and path-specific objectives were **not read** this pass, so the reduction is flagged, not asserted.
- **Verdict: recombination (an audit rule).**

---

## Overall verdict

- **No direction clears the novelty bar.**
  - Direction 1 (predictably gated own-body output learning) is a learning-rate schedule on an own objective. Closed by gate predictability; by Proposition 3(c) it is the yoked arm and teaches no partner-shaped form.
  - Direction 2 (contingent response credit) is the infant's and the marmoset's actual signal: operant learning from partner responses. Open; inside the band it makes the partner's selectivity, including matching, the learned optimum.
  - Direction 3 (lineage typing of step weights) is an audit rule that extends pass 8's approval tensor from rewards to every gate and replay priority.
- **Why everything reduces here.**
  1. **The direct evidence agrees with pass 8 and makes it sharper.** The signal that shapes infant (and marmoset) output is the covariance between the partner's response and the infant's own output. It is open in every study, and in Takahashi et al. 2016 it works through timing alone.
  2. **The closed version is the yoked control, and the yoked control teaches nothing about form** (Proposition 3(c)). An approval-closed output learner can only speed up learning toward targets fixed inside the agent (Direction 1); it cannot learn what this partner prefers. That is a property of the closure, not a gap in the reading.
  3. **So with D93 given, partner-shaped output form has to come from routes that are not contingency on the agent's own output.** In the engine those are: Claude's word and regulation path; learning from recorded human dyads (Q26 source 2); and the reading map trained by being mirrored (pass 8, Direction 1). The long-term goal's phrase "acquires its manner of speaking by living with people" can be met, under Principles 3 and 6 and D93, only through those routes. Infants meet it through the open route, with the caregiver's policy as the limit.
- **Most useful products for the build core** (none needs a new design):
  1. **Predictability condition for any social gate on learning:** the gate is computed from events that precede and are independent of the events it weights (nightly statistic, disjoint replay batch). Social engagement may set how fast, never which way (Direction 1).
  2. **Lineage typing of replay priorities and tags** (Direction 3), with S6's state-tagged replay as the first object to check.
  3. **Own-output objectives are scored on the agent's own efference and its own innate auditory or visual model, never on the microphone or camera mix that contains the partner** (Direction 1(4)).
  4. **Battery additions:**
     - the contingent-vs-yoked twin copy plus still face: a channel-specific extinction burst in the contingent copy only is the behavioural sign of an approval route (Direction 2);
     - a phase-locked partner, who answers at a fixed phase of the agent's own fluctuation on one channel with constant content: a closed learner's output must not drift on that channel (Proposition 3(b));
     - Kuhl's live-vs-recorded contrast for any perception-side gate: a gate driven by the user's attention score should be absent (Principle 6).

**designs.md:** no candidate deserves a line as a new design. Products 1-3 refine the Cayley-ledger build core's learning specification and audit, if adopted.

## Next steps
1. Read, if the hosts open: Goldstein, King & West 2003 (PMC164707 when PMC serves it without a bot check), Takahashi, Liao & Ghazanfar 2017, Carouso-Peck & Goldstein 2019 (a non-vocal, visual partner signal shaping song: the closest animal analogue of a face channel shaping output), Albert, Schwade & Goldstein 2018.
2. Read the prioritised-replay and path-specific-objective literature (for example Schaul et al. 2016; Farquhar, Carey & Everitt 2022) to check whether Proposition 3 and the lineage rule are already stated there; cite if so.
3. Check the build core's replay and nightly-update code paths against products 1-3; that is a build task, not a search task.
