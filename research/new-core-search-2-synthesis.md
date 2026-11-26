# Searching for a new core mechanism, second pass: self/other in shared body maps, population geometry, and structure-first ML (synthesis, 2026-11-26)

Sources read in full for this pass (notes in research/):
- kennedy-sawtell-2014-temporal-basis-negative-images.md (corollary discharge; learned negative images on a random-mixture temporal basis);
- banissy-ward-2013-mirror-touch-self-other.md (vicarious touch is kept implicit by a gate graded by context and self–other similarity; opinion piece);
- maister-2013-mirror-touch-enfacement.md (seeing touch rewrites the self-face model in mirror-touch synaesthesia, as felt+seen synchrony does in everyone);
- mante-2013-selection-vector.md (represent vs integrate: right vs left eigenvector of a line attractor; Supplementary Information not read);
- mastrogiuseppe-ostojic-2018-low-rank-rnn.md (random + low-rank connectivity; overlaps set time scales and input selection; Methods read in part);
- vandenoord-2018-contrastive-predictive-coding.md (model a density ratio; the negatives decide what is learned);
- zaheer-2017-deep-sets.md (property first, characterisation theorem, architecture read off it).

Not reachable (proxy refused the host): Ward & Banissy 2015 and Heyes & Catmur 2015 on mirror-touch theories; the Bangor copy of Maister et al. (read from PMC instead). The first pass (new-core-search-synthesis.md) is not repeated here.

No emotion labels or named emotion variables appear below the Claude layer. All channels are face, voice and timing features in the agent's own coordinates. Derivations marked "derived" are mine. Numbers marked "checked" come from a throwaway script (an OU own-command signal, τ = 2 s, 30 Hz, 33 min; an LMS negative image on 52 basis functions: 40 log-spaced delays from 33 ms to 120 s and 12 exponential filters from 0.1 s to 60 s).

## What this pass adds to the search

- **Self and other share one map; what keeps them apart is a subtraction or a gate, and both are learned.** In the fish, the self-caused part of the input is cancelled by a learned negative image of one's own command history; what is left is, by construction, the other. In people, vicarious touch activates the same somatosensory map and stays implicit through a gate graded by context and similarity; when the gate fails (mirror-touch synaesthesia) the result is not a stronger coupling everywhere but felt copying plus a self-model that absorbs the other.
- **The copy attractor has a learning form as well as a dynamical form.** Maister et al.: seen–felt coincidence rewrites the self-face model, and in synaesthetes vicarious activation is enough to supply the "felt" side. For the engine this means the own-body model (used to read the partner "through the agent's own body") must never be trained on a signal the partner's face can drive. A synchronous mirroring partner is the enfacement condition.
- **Population geometry gives "know fully, move within a limit" a precise object.** Mante et al.: an input can deflect the population strongly and still not be integrated, because persistence is set by its projection on the left eigenvector (selection vector) of the slow mode, not on the mode itself. Mastrogiuseppe & Ostojic: in random + low-rank networks, the left connectivity vectors select inputs, the right ones set the output pattern, and time constants are set by their overlaps relative to the bifurcation value. Temperament as one structural number (Nair et al.'s leading time constant) fits this object.
- **Method.** CPC and Deep Sets were found by choosing what to compare (negatives) and by stating the required property first and proving the form that has it. Neither added a module.

---

## Direction 1: the social negative image. The partner's response to the agent is the agent's reafference

### (1) The object
- **Own history basis.** The agent's own expression and timing commands u(t) ∈ R^m (face channels, voice prosody channels, its own turn and tempo events). A fixed, innate expansion Φ(t) = Ψ(u_[t−D, t]) ∈ R^M, M ≫ m: sparse random mixtures (≤ 3 inputs each, as in Kennedy et al.) of per-channel delayed and filtered copies of u. Delays run from one frame to D ≈ 10 min; the long-delay elements act on low-passed u.
- **Negative image.** For each partner channel j (partner face and voice in the agent's own coordinates), p̂_j(t) = w_jᵀ Φ(t), learned by the normalised LMS form of the anti-Hebbian rule: e_j = p_j − w_jᵀ Φ, Δw_j = η e_j Φ / (1 + |Φ|²).
- **Drive.** The core latent z ∈ R^N receives the partner only through the residual: τ ż = −z + J φ(z) + B_own x_own + Σ_j b_j g_j(z) e_j, with |g_j| ≤ c_j (innate per-channel ceiling) and the sign of g_j set by state and context (for example g_j = c_j tanh(θ_jᵀ z)).
- **Relationship.** W = [w_j] is a learned map from the agent's own expressions to this partner's responses, per channel and per delay. It is kept as the relationship memory. The contingency signal p̂ is kept as its own input, not discarded.

### (2) Novelty verdict (plain)
- **Recombination.** The negative image is an adaptive filter (LMS on a fixed basis) and a forward-model comparator: the prediction-error family close to predictive coding and active inference. The coupling g_j is a capped gain.
- **The only new element is the transposition:** treating the partner's mirroring of the agent as reafference, cancelled on the same principle as the fish's own discharge. This does not clear the bar.

### (3) Emotion in a rich latent; the other through the own body; no copy attractor
- **Latent.** z is any rich recurrent state; Direction 2 is the natural choice. The partner reaches it only as news: what the partner did that the agent's own expressive history does not predict.
- **Through the own body.** The partner is compared against a prediction built only from the agent's own commands, in the agent's own coordinates.
- **Copy loop opened (derived).** At LMS convergence E[e Φᵀ] = 0, so the residual is uncorrelated with every function in span(Φ). The loop agent expresses → partner mirrors → agent integrates then has zero gain for every partner response that is a linear filter of the agent's history within D, whatever g_j is (Deep Sets method: a linear functional vanishes on all such responses if and only if it depends on the partner only through such a residual).
- **Checked.** A partner copying the agent at 0.5 s lag, plus 20% independent content, is left at 6.1% of its variance (ideal 5.9%).
- **Per-channel, sign-flippable, capped:** g_j as above.

### (4) The four lessons of report 8
- **L1 (ignoring simultaneous movement is not enough).** Cancellation covers every lag in the basis, not lag 0.
- **L2 (compare with the face the agent would have made had the partner held still).** This is the mirror image: the residual is the partner minus "what the partner does when only answering me". The counterfactual own face is still needed for the agent-follows-partner direction.
- **L3 (limits against raw movement, across minutes).** The residual is in raw partner units, and the basis reaches 10 min. The numbers below show this is the weak point.
- **L4 (routes that don't depend on the face now).** Own tempo and turn events are in Φ, so the partner's tempo-following of the agent is cancelled. The agent following the partner's tempo is not touched and needs its own count.

### (5) Most likely concrete failure
- **(a) Slow copying is cancelled only partly, and slowly.** Checked:
  - a fast signal copied at 40 s lag is left at 79% (the sparse long delays miss it);
  - a 60-s low-passed component copied at 40 s or 90 s is left at 46% and 65% of its slow-band variance after 33 minutes.

  The fish needed ~1,000 command periods. By that ratio a minutes-scale copy needs on the order of 1,000 minutes of conversation before it is cancelled.
- **(b) It cancels "you responded to me".** The contingency the project values (partner responsiveness) is exactly what is subtracted from the drive. It survives only as p̂ and W, which then need their own ceiling, or they become the route back.
- **(c) The agent copying the partner is not addressed.** The residual is the partner's innovation (checked: 64% of variance for a 1-s-lag self-copy of a 2-s OU signal). A core can integrate innovations back into a copy, so the ceiling c_j carries that direction alone.

---

## Direction 2: a selection-geometry latent. Represent the partner fully, integrate only through capped left-vector overlaps

### (1) The object
- **State.** x ∈ R^N (N in the hundreds), with τ ẋ = −x + J(c) φ(x) + Σ_j b_j (v_j − v̂_j) + Σ_j b_j p_j + B_i i + B_c c.
- **Connectivity.** J(c) = g χ + Σ_{k=1}^r m_k n_k(c)ᵀ / N: random bulk plus low rank (Mastrogiuseppe & Ostojic).
- **Shared body map.** The agent's own channel-j proprioception v_j and the partner's channel-j feature p_j enter along the same innate pattern b_j. Own movement is cancelled by its efference prediction v̂_j (Direction 1 applied to the agent's own body), so the net drive in the shared map is the other. i is interoception; c is context (relationship, Claude's regulation path).
- **Time scales from overlaps.** λ_k = n_kᵀ m_k / N with τ_k = τ/(1 − λ_k) in the linear regime. A ladder λ_k = 1 − 2^(−k) gives τ_k = 2^k τ: reflex in the random bulk (τ ≈ 30 ms), and 6 days at k = 24. Temperament is the top of the ladder, one structural number.
- **Ceiling by construction (derived).** Write n_k(c) = n_k⁰ + Σ_j β_kj tanh(θ_kj(c)) b̃_j, with:
  - n_k⁰ orthogonal to every b_j;
  - b̃_j the dual basis (b̃_iᵀ b_j = N δ_ij).

  Then the overlap κ_kj(c) = n_k(c)ᵀ b_j / N = β_kj tanh(θ_kj(c)) for every context and every learned θ.
  - In the linear regime the long-time partner-to-face gain on channel j is G_jj = Σ_k (C m_k)_j κ_kj / (1 − λ_k).
  - Choosing β_kj = c_j (1 − λ_k) / (r |(C m_k)_j|) gives |G_jj| ≤ c_j.
  - So the partner's overlap with a mode must shrink as 1/τ_k: the slowest modes are the hardest to move.

### (2) Novelty verdict (plain)
- **Recombination; it reduces to excluded frameworks.** A low-rank RNN (whose special cases are Hopfield and FORCE) linearised around line and ring attractors. In left-eigenvector coordinates it is a diagonal state-space model whose input matrix depends on context: a selective SSM with bounded B.
- **What it adds:**
  - the represent/integrate split through non-normality;
  - the 1/τ_k scaling of the per-channel ceiling;
  - the shared body map with efference cancellation.

  None of these is a new computation.

### (3) Emotion in a rich latent; the other through the own body; no copy attractor
- **Latent.** x is high-dimensional with mixed selectivity; persistent states live on span(m_k) (line and ring attractors, as in Nair, Vinograd and Mante). Position on the slow manifold selects the expressive repertoire, not only its amplitude.
- **The partner is known fully.** B_p p deflects x and is decodable at all times, but persists only through κ_kj.
- **Coupling.** Per channel, capped (β_kj) and sign-flippable by context (tanh θ_kj(c)), with the cap holding for every reachable context. That closes Mante's second-order route, where a partner-driven context rotates the selection vector.
- **No copy attractor (linear regime).** Because |G_jj| ≤ c_j < 1, the partner's channel cannot be reproduced on the agent's channel. The copy set is not invariant.

### (4) The four lessons
- **L1.** Nothing here depends on simultaneity: any time course of p_j reaches the slow modes only through κ.
- **L2.** Efference cancellation in the shared map is the "own face had the partner held still" comparison, built into the input.
- **L3.** The ceiling is stated on the long-time (DC) gain through the slowest mode, so it is measured against raw partner movement over minutes to days, in the linear regime.
- **L4.** Context c may depend on partner tempo, and its effect is bounded by β. A tempo feature entering as an input needs its own b and its own β: one more count, stated.

### (5) Most likely concrete failure
- **Bistable modes break the ceiling.** Where λ_k > 1 (needed for persistent discrete states), a sustained input along n switches the mode from one stable state to the other (Mastrogiuseppe & Ostojic, Fig. 2D right). A bounded overlap times a long enough partner hold produces a full jump. The DC-gain ceiling says nothing about it: the gain at a saddle-node is unbounded.
- **The random bulk moves the effective left eigenvector.** By an amount growing with g, so the β bound holds on n_k but only approximately on the true selection vector.
- **Cross-channel copying through the partner's own correlations.** G_ij with i ≠ j can rebuild channel i from correlated partner channels j. This is the face-and-voice-together leak found in earlier designs.

---

## Direction 3: contrastive individuation. The latent is what tells the agent's own future from the partner's

### (1) The object
- **Shared encoder.** A shared per-channel encoder φ_j (the agent's own body coordinates, used for both its own and the partner's features).
- **Context state.** c_t = g(φ(y)_{≤t}, φ(p)_{≤t}, i_{≤t}) of any recurrent form, for example Direction 2's x.
- **Objective.** For each channel j and horizon k ∈ K (one frame to minutes), with score f_jk(a, c) = exp(φ_j(a)ᵀ W_jk c):

  L = Σ_j Σ_{k∈K} E[ −log f_jk(y_{j,t+k}, c_t) / ( f_jk(y_{j,t+k}, c_t) + Σ_{d∈Δ} f_jk(p_{j,t+k−d}, c_t) + Σ_{t'∈T} f_jk(y_{j,t'+k}, c_t) ) ]

  where:
  - y is the agent's own future face and voice;
  - Δ is a set of lags from 0 to minutes (the partner's lagged futures as negatives);
  - T is a set of other times (the agent's own other futures).
- **One objective.** The face generator is trained by the same L. It must produce a future that its own state predicts and that is not the partner's at any listed lag.

### (2) Novelty verdict (plain)
- **Not an excluded framework.** It is contrastive learning, which is not on the list.
- **Prior art not established.** One web search found no use of a partner's futures as negatives for self–other individuation; that is not proof of absence.
- **But it is an objective with a chosen negative set, not a core computation.** Measured against attention it is thin: the dynamics substrate is still an RNN. It is the most novel of the three, and it does not clear the bar alone.

### (3) Emotion in a rich latent; the other through the own body; no copy attractor
- **Latent.** c_t is whatever makes the agent's next moments its own. It is learned, rich, and its time scales are set by the horizon set K: CPC's step ablation went from 28.5% to 64.6% phone accuracy as the horizon grew from 2 to 12 steps.
- **Through the own body.** The same φ_j encodes both faces.
- **Copy is the worst case of the objective, for every parameter value (derived).** If y_j(t + k) = p_j(t + k − d) for some d ∈ Δ, the positive and one negative have the same score for any critic, so that term is at least log 2 above its floor. Exact copying at any listed lag is repelled by the objective itself, not by a ceiling.
- **Doing the opposite is discriminable and free.** This is the property report 4 found that no symmetric information measure has.
- **Per-channel, sign-flippable, capped coupling: only partly.** The objective gives a floor on discriminability, not a ceiling on coupling. Ceilings must come from Direction 2.

### (4) The four lessons
- **L1.** Copies are repelled at every lag in Δ, not only at lag 0.
- **L2.** The counterfactual own face (the partner held still) can be added as a positive-side view; not needed for the copy property.
- **L3.** Discrimination is on raw partner features at lags up to minutes.
- **L4.** Tempo and turn timing are channels with their own term. The count is one term per channel, so a route without a term is visible by its absence.

### (5) Most likely concrete failure
- **What counts as a copy is set by the invariance of φ_j, and that choice is a dial.**
  - With raw levels, an offset copy y = p + b, or a scaled copy y = 0.9 p, is discriminable and passes.
  - With scale-normalised increments, every positive affine copy is repelled, but then no channel may follow at all, which violates D83's non-zero ceilings for smile and laughter.
  - Choosing the invariance per channel brings back a per-expression knob from flat to copy-repelled: exactly the dial the refined rule forbids, moved into the encoder.
- **Full-gain opposite responding passes.** It sits at ceiling magnitude, so a contrarian lock-on is not prevented.

---

## Overall verdict

- **None of the three clears the bar** of a genuinely new core mechanism on the level of attention.
  - Direction 1 is an adaptive filter turned on the social loop.
  - Direction 2 reduces to a low-rank RNN, that is, a selective state-space model with bounded input overlaps.
  - Direction 3 is a new use of a contrastive objective, not a computation.
- **Each contributes one property that holds by construction, and the three fit together:**
  - Direction 1: the agent → partner → agent loop has zero gain on the span of the agent's own history;
  - Direction 2: a per-channel long-time ceiling that shrinks as 1/τ_k, holding for every context;
  - Direction 3: copying at any listed lag is the maximum of the objective.

  Direction 2 would be the substrate, Direction 1 the self/other gate in the shared body map, and Direction 3 the single training objective. The composite is a recombination, and should be put that way.
- **The most useful single idea for a later new mechanism** is the one Deep Sets' method points to and this pass did not finish: characterise *all nonlinear* causal functionals of (own history, partner path) that vanish on every partner path that is a (possibly nonlinear) function of the agent's own history within D. The linear answer is "depends only on the residual" (Direction 1). If the nonlinear answer has a usable form, that form would be an architecture derived from the property, which is how attention-level mechanisms have been found.

## Next steps
1. **Independent critique of Direction 3's copy property and of its invariance dial**, since it is the least reducible.
2. **Measure, on the Seamless Interaction features** (Mac only, D70/D85 restrictions), how much of each listener's face is linearly predictable from the speaker's own history at lags up to 10 min. That number bounds what Direction 1 would cancel, and with it failure (b).
3. **Attempt the nonlinear characterisation** (Volterra or kernel form, with the residual as a conditional expectation) before writing any design.
