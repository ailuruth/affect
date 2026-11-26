# Critique: Fibred attribution core (design-fibred-attribution-core.md): reduction, novelty, principles, and what it fails to explain

Independent critic, 2026-11-26T04:21:07Z. I did not write the design and did not see its author's reasoning. This critique covers reduction to existing mechanisms, novelty against the brief's two clauses, the Principles, the expressive-structure items, and what the design fails to explain. A separate critic checks the proofs and the dial; I flag only the problems that bear on novelty or that are glaring (§1.8). Nothing was downloaded except papers, and no data or weights were used. Papers were read from export.arxiv.org. arxiv.org and ar5iv were blocked in this session; export.arxiv.org served the same PDFs.

## Summary verdict

- **Reduction: complete.** Every part reduces to an existing mechanism, and so do the three "composition results" that the author offered as new. The author did not survey robust control or hybrid systems. Those fields contain the following.
  - **Theorem 1(c), the token-bucket count B + ρT,** is the average-dwell-time switching class of Hespanha and Morse, with the bucket capacity as the chattering bound N₀ and 1/ρ as τ_a. It is the token-bucket traffic specification already used in networked control (Linsenmayer & Allgöwer 2018; Wildhagen et al. 2019; Jaumann, Wildhagen & Allgöwer 2020, read). Stability of switched systems with *multiple* equilibria under a dwell time is also studied (Alpcan & Başar; Makarenkov & Phung 2017, read).
  - **Lemma 2** is bifurcation tipping (its part a) plus rate-induced tipping (its part b), in the taxonomy of Ashwin, Wieczorek, Vitolo & Cox 2012 (read). That taxonomy names a third route, noise-induced tipping. The design leaves it uncounted, and it leaks (§1.8).
  - **"Contraction and persistence coexist only in fibred form" (Lemma 1 → Theorem 1) is false as a general claim.**
    - Forni & Sepulchre's p-dominance (read) gives multistability (p = 1) with contraction in the other n − p directions, and comes with an LMI dissipativity interconnection theory.
    - k-contraction (Wu, Kanevskiy & Margaliot, read) gives 2-contracting systems with several equilibria, in which every bounded solution converges.
    - A fast contracting fibre over a slow multistable base is the standard slow–fast (Tikhonov–Fenichel) picture.
  - **Lemma 4's conclusion is false.** The lemma shows that no *diagonal* IQC separates one-channel matching from whole-face matching, and that is trivially true. Its stated meaning, that a non-quadratic ℓ₁ constraint is needed, does not follow. Revay et al. allow any Q ⪯ 0. A non-diagonal Q = −(I + α𝟙𝟙ᵀ) admits a single channel at gain √(r/(1+α)) but whole-face matching only at √(r/(1+αn)), whatever the per-channel signs. This is a quadratic joint budget Σt_k² ≤ r/α on the diagonal gains. In the worst case it separates *better* than the router's ℓ₁ mass does: 0.053 per channel on 32 channels, against the router's 0.144 (§1.3).
  - **Theorem 4** (a gain ceiling plus an independent innovation gives an observable fidelity floor) is the coherence/SNR identity ρ² ≤ SNR/(1+SNR). In privacy terms it is the sensitivity-plus-noise mechanism; differential privacy bounds leakage (Alvim et al., read), and Revay et al. themselves cite privacy as an ℓ₂ Lipschitz bound.
  - **The router with row caps, total mass and habituation** is constrained softmax/sparsemax with fertility upper bounds that shrink with accumulated attention. Malaviya, Ferreira & Martins 2018, read, eq. 5: α_t = csoftmax(z_t, f − β_{t−1}). Coverage (Tu et al. 2016, read) is the habituation vector.
  - **The typing rules A1–A8 and the route inventory (Lemma 7)** are an information-flow type system. Theorem 2 is a noninterference statement with |c^f| declassified.
- **Novelty.** The author's verdict, recombination, is confirmed, and on a weaker basis than the author claimed. Neither clause of the novelty test is met. No part is a new primitive. The design moves in the opposite direction to the historical pattern (new-mechanisms-synthesis §2.4): it *adds* about 45 innate constants and 8 typing rules to cap dials, instead of deleting a scalar by changing what is computed. §2 names what would have to change.
- **Principles.**
  - Principle 1 holds.
  - Principle 2 is strained. The repetition drive is an installed motivational variable over a cognitive quantity (attention allocation). It is not a body variable and not a reflex. The base is one categorical state, so "emotion as emergent structure" is thin.
  - Principle 3 is real in perception: P_φ is learned from babbling. It is **not essential in state inference.** D's output ŝ reaches behaviour only through a fence budget shared with 80 inputs, plus a retrieval key. The decoder may be unable to invert at all under the certificate, because the constant c_s is unspecified (§3.3).
  - Principle 4 holds for the channel, but Claude cannot name, reinterpret or regulate anything, which is the role the brief gives it.
  - Principle 6 holds for the face. The information drive is lowered by surprise in the *partner's words*, so draft selection carries an engagement incentive.
  - Principle 10 fails: this is an assembly. The author says so.
- **Expressive structure.** The router is selection among 2048 fixed scalar gains, not content-addressed attention. The persistent affect is one well among 64 (about 6 bits), plus 5 body gauges, plus a 3.3-s fibre. Between 3.3 s and the base, nothing persists. At conversational time scales, what the face can show from the agent's own state is throttled to about 0.025 per channel per minute. This is a categorical-gauge design, closer to the "few gauges" sketch than its parameter count suggests.
- **What it fails to explain.** Five things.
  - **Vocal convergence on held levels** is excluded by construction, by the very "level-blindness" the design proves.
  - **Partner history within minutes** has no carrier: weights change only at night, κ_rel is frozen, and the base is shown through a 20-min slew.
  - **Fast emotional reactions to what is said** (appraisal within 1–2 s) have no route larger than about 0.15 shared.
  - **Interoception** is decorative: nothing goes from the base to the body.
  - **Grounding of concepts named by Claude** is absent: no selection pressure ties Claude's emotion words to the agent's state.

---

## 1. Reduction

I tried to reduce each part and each claimed composition result, reading the closest prior work.

### 1.1 The fibre is a robust REN, as the author says

This is Revay, Wang & Manchester (read: §I–IV, Theorems 2–3, §VI on expressivity). Revay states that the IQC triple (Q, S, R) is user-chosen with any Q ⪯ 0 (Definition 3), and that RENs "can be used to learn subsystems that specify prescribed or parameterized IQCs, and which therefore cannot destabilize the system when interconnected". So the "fence" (§2.4) is the paper's stated purpose, applied as intended. Nothing is added to the REN.

### 1.2 The base, the port and the display reduce to known hybrid-systems objects

| Design element | Existing object | Source read |
|---|---|---|
| Log-sum-exp landscape with C wells (§2.8), and Lemma 3 (every well keeps a forward-invariant ball with a unique stable point when separation is large against 1/β) | Continuous modern Hopfield energy. Lemma 3 is the gradient-flow version of Ramsauer et al.'s Definition 1 ("stored": a sphere around each pattern with a single fixed point to which all its points converge) and their Theorem 4: a Jacobian bound 2βN M(N−1)exp(−β(Δ−…)), the same structure as the design's 4β_b(C−1)η. Biases h_c and the tilt are routine additions | Ramsauer et al. 2020, §2 and Theorems 3–5 |
| Partner writes as counted jumps through a token bucket (Theorem 1c, Lemma 2c) | Token-bucket traffic specification in networked control: β(k+1) = min{β(k) + g − γ(k)c, b}, which guarantees an average transmission rate ≤ g/c. The count bound B + ρT is the **average-dwell-time class** S_adw(τ_a, N₀) = {σ : N_σ(s,t) ≤ N₀ + (t−s)/τ_a} of Hespanha & Morse 1999. N₀ is called the "chattering bound" | Jaumann, Wildhagen & Allgöwer 2020 (§1–2); a 2024 converse-Lyapunov paper restating Hespanha–Morse's definition (arXiv 2405.03560, §2) |
| Multistable base switched by events, with a dwell time between switches | Switched systems with multiple equilibria and dwell time; trapping regions around an "ideal attractor"; whether "adding more discrete events is alone capable of making the dynamics faster" (the rate-dial question) | Makarenkov & Phung 2017 (Theorems 2.1, 3.1; Alpcan–Başar as Corollary 3.1) |
| Lemma 2(a): a held level crosses the barrier iff kS > F⁺ | Bifurcation tipping (B-tipping) / hysteresis of a forced bistable system | Ashwin et al. 2012, §1 |
| Lemma 2(b): a sawtooth walks the staircase | Rate-induced tipping (R-tipping): "a sufficiently rapid change to an input … may cause the system to tip", with no bifurcation needed | Ashwin et al. 2012, §2 |
| Contracting fibre over a slow multistable base (Theorem 1) | Slow–fast (singularly perturbed) system: normally attracting fast fibres over a slow manifold, on which the slow flow may be multistable (Tikhonov; Fenichel). The design's base-to-fibre coupling is continuous; its fibre-to-base coupling is impulsive. That makes it an impulsive slow–fast hybrid system | Fenichel 1979 *not read in the original* (paywalled); a discrete GSPT paper (arXiv 2201.06996) skimmed for the standard statement. **Not load-bearing:** the dwell-time and tipping reductions above stand alone |
| Contraction and multistability at once | p-dominance: "stability is the particular situation where the dominant behavior is 0-dimensional … multistability through 1-dominance"; Corollary 1: every bounded solution converges to a fixed point when p = 1. k-contraction: 2-contracting systems may have several equilibria | Forni & Sepulchre 2019 (§I–IV); Wu, Kanevskiy & Margaliot 2021 (§1) |
| Contraction of hybrid systems without dwell-time restrictions (the author's weak point 6) | Infinitesimal contraction for hybrid systems with guards and resets, "without restrictions on mode sequence or dwell time" | Burden, Libby & Coogan (arXiv 1811.03956, abstract and §I) |
| Slew-limited display | Actuator rate saturation | standard |
| Persistent slow memory written only by gated, budgeted events; fast state alongside | LSTM cell state (slow) versus hidden state (fast); Skip RNN's explicit budget on the number of state updates (L_budget = λΣu_t); option switching with a deliberation (switching) cost, which is the soft version of a bucket | Skip RNN (Campos et al. 2018, §3); Harb et al. 2018 (switching cost as margin) |

**Verdict on composition result 1** (Lemma 2 with Theorem 1, "necessity and sufficiency of a fibred, budgeted port"):
- **Sufficiency** is a known construction: an average-dwell-time switched multistable system with a contracting fast subsystem.
- **Necessity is not established, for three reasons.**
  1. *Lemma 2(a), second case, is itself a non-budget innate stop.* A continuous port with gain kS below the smallest barrier force never causes a switch, yet still gives graded within-well influence. The design uses exactly this for the body tilt t_max. So "the budget is the only innate stop" (Lemma 2c) contradicts Lemma 2(a). It holds only under the unstated premise that the partner *must* be able to cause switches.
  2. *Contraction and multistability coexist without a product structure* (p-dominance, k-contraction), with LMI-checkable port bounds. "Only in fibred form" is false. What survives is narrower: any partner port into the dominant (multistable) directions is either sub-barrier or a tipping route. That narrower statement is Ashwin's B/R taxonomy.
  3. Lemma 2 is proved for a scalar staircase. In n_b = 24 dimensions a held level can also steer *which* basin a noise-driven escape enters. That is the N-tipping route of §1.8.

### 1.3 The router is constrained attention with coverage

- The softmax with a null slot and per-row caps, bounded total mass, and "habituation" A_i accumulating μ and lowering logits are each published:
  - constrained softmax: "upper bound the amount of attention a word can receive" (Martins & Kreutzer 2017);
  - constrained sparsemax with fertility bounds updated by cumulative attention, α_t = csoftmax(z_t, f − β_{t−1}) (Malaviya et al. 2018, eq. 5);
  - the coverage vector "summing previous alignment probabilities" fed back into attention (Tu et al. 2016).
- The design's twist is that slots index (own channel, partner coordinate, lag, sign) and values are scalar partner coordinates. That is a new key space, which Q9 counts as a recombination.

**Verdict on composition result 2** (Lemma 4 with Lemma 6: the ℓ₁ mass reaches beyond any diagonal IQC):
- Lemma 4 is correct but trivial (a diagonal matrix inequality is a box).
- Its stated meaning is wrong: "That needs an ℓ₁-type (non-quadratic) constraint" (§3.5), and "No quadratic (IQC-type) ceiling can express this" (§1).
- **Counterexample.** Take R = rI, S = 0, Q = −(I + α𝟙𝟙ᵀ) ⪯ 0, which is admissible in Revay's Definition 3. For any diagonal transfer T = diag(t):
  - TᵀQT = −(diag(t²) + α ttᵀ);
  - its largest eigenvalue is at least α‖t‖²;
  - so admissibility requires α Σ_k t_k² ≤ r.
- That is a **quadratic joint budget on the per-channel gains, sign-independent**:
  - one channel can reach √(r/(1+α));
  - matching on all n channels, with any signs, is held to √(r/(1+αn)).
- **Numbers.** With the single-channel cap at 0.30 and α large, whole-face uniform matching on 32 channels is ≤ 0.30/√32 = 0.053 per channel. The router's worst case is τϖ₃₂ = 0.6 × 0.24 = 0.144 (§3.9).
- So a quadratic certificate inside the REN, with no router, would separate one-channel from whole-face matching *more strongly* than the ℓ₁ mass does in the worst case. The ℓ₁ mass wins only with frozen allocation (τ/|K|).
- The router's real advantage is that its weights are input-selected, which is attention. It is not that ℓ₁ is beyond IQCs.

### 1.4 The sign-blind gate is invariant features

- Rectifying a band (|c^f|) before every consumer is the motion-energy / invariant-feature construction. The author says so ("as an object this is invariant features, which is standard").
- Theorem 2's proof is an induction over the code graph, showing that no module sees the sign. That is a **noninterference** proof with |c^f| declassified: a typed information-flow argument in the sense of the secure-information-flow literature (Denning; Goguen–Meseguer: *not read in the original*; the quantitative version through Alvim et al., read).
- A1–A8 as a whole are an information-flow type system on a dataflow graph. Lemma 7 (route completeness by inspection) is its typing judgement.

### 1.5 Theorem 4 is the coherence bound / sensitivity-plus-noise mechanism

- **The bound.** δ_K ≥ σ₀/(C_K²ā² + σ₀²)^{1/2} is 1 − ρ² ≥ N/(S + N): the magnitude-squared coherence between output and partner, bounded by the signal-to-noise ratio of the partner-dependent part against an independent additive innovation.
- **The DP reading.** The same pattern defines the Gaussian and Laplace mechanisms of differential privacy: bounded sensitivity plus independent noise bounds what an observer can recover. Alvim et al. show that differential privacy bounds mutual information. Revay et al. note that privacy in dynamic policies "can be represented as an ℓ₂ Lipschitz bound".
- **Verdict on composition result 3:** a known composition in a new application.

### 1.6 Attribution is Lanillos with an instrument, as the author says

- Lanillos, Pages & Cheng 2020 (read: §1–4): accumulated log-evidence for "self" against "other", and the observation that the other "acted sometimes as an attractor … generating mirroring actions similar to imitation".
- The design takes the evidence step and does not let action descend other-slot error, as the self–other synthesis recommends.
- Ĝ from the agent's own dither is Forssell & Ljung's closed-loop instrumental variable. Nothing is added.

### 1.7 Hierarchical RL options and gated RNNs

- Each base well conditions N_own, H and the router queries: one "mode" that sets a policy over the fast layer, terminated by events. That is an option with external termination; the bucket is a hard switching budget, where Harb et al. use a soft deliberation cost.
- The fast/slow split with a gated write is the LSTM cell/hidden split; the budget is Skip RNN's.
- These are analogies of structure, not identities, but they leave no new computation.

### 1.8 Glaring items for the proof critic (not checked in depth here)

1. **Noise-induced tipping leaks the held level into the base without spending tokens.**
   - Theorem 1(c), Theorem 6(a) ("b is autonomous … no force pulls the base toward any function of the held level") and Lemma 2(c) count only event jumps. But the base has noise σ_b and a tilt t_ψ(ζ̃).
   - ζ is partner-dependent: motor effort comes from m^pre, which contains the router output y^R driven by the partner; the information deficit comes from the partner's words.
   - A tilt of up to t_max = 0.05 changes each barrier by up to about t_max·d_min/2 = 0.0125. That changes the Kramers rate by a factor of about exp(2·0.0125/0.0081) ≈ 22, using the design's own estimate ΔV ≈ 0.031 and σ_b² = 0.0081.
   - So a sustained partner behaviour can move the mean escape time from 6–19 h to about 16–50 min, and *bias which well is entered*, with no token spent.
   - The window bounds of Theorem 3 survive, because the display slew still bounds the face. The claims "no force toward the held level" and "event rate is not a dial" (in law) fail. This is the N-tipping member of Ashwin's taxonomy, missing from Lemma 2.
2. **c_s is unspecified, and the decoder's invertibility depends on it.**
   - ŝ = D(ℓ) is an output of the REN, bounded by (R) with W₂ = I/√80 on ℓ, so Lip(D) ≤ c_s/√80.
   - Inverting E_own, whose own display part has Lipschitz ≤ A_k = 0.25 per channel, needs Lip(D) of order 1 or more.
   - Either c_s is of order 9 or more, which must be stated and checked against the claim that ŝ "shares" y^F's budget, or Theorem 9(b)'s "ŝ = s exactly" is unreachable.
3. **Theorem 4's floor falls with partner expressiveness.** At ā = 2 the single-channel floor is 0.12. A more expressive partner observably gets a closer copy. Defensible, but it should be stated as a property, not hidden in F10.
4. **Partner speech articulation enters P_φ's expressive coordinates.** The agent's own visemes are a separate subspace, but the partner's jaw and lip motion while talking is projected onto the 9 synergies, so every gate quantity carries the partner's articulation. Nothing in Γ separates it.

---

## 2. Novelty against the brief's two clauses

**Clause 1 (parts list, Q9).** Every part is an existing mechanism:
- REN;
- constrained softmax attention with coverage;
- modern-Hopfield energy;
- invariant features;
- Lanillos evidence plus an instrumental variable;
- homeostatic drive;
- token bucket / average dwell time;
- rate limiter;
- LRU world model.

**Fails.**

**Clause 2** ("a mechanism counts as new if it changes the signature or the defining invariant of the computation, derives the update from that invariant, and thereby removes a named, measured failure, ideally by deleting a free scalar"):
- No computation's signature changes. Every module computes what its source computes.
- The design states invariants (the per-channel ceilings, the mass τ, the slews, the bucket, sign-blindness), but they are *imposed by clipping and typing*. They are not the defining property from which an update is derived, the way softmax attention follows from soft alignment, or LegS from the projection measure.
- No measured failure is targeted: the failures are the critiques' counterexamples, not data.
- **The scalar count goes up.** §2.1 lists about 45 innate constants, and the D78 guarantee depends on all of them.

**Fails.**

**Is anything at the level of a primitive?** No. The design's real contribution is methodological. It is the first design in the project to make route completeness a typing judgement and to state every bound uniformly over the parameter set. That is valuable as an audit standard for all designs, and it is how robust control and information-flow security already work.

**What would have to change for it to become one.** Precisely:
1. **One defining invariant must replace A1–A8 plus the caps.** The most promising one, consistent with Report 3's direction, is an *information* invariant on the typed partner channel instead of a gain:
   - the mutual information between the partner's percept history and everything self-typed (state, outputs, stored records) is at most C bits per second, set innately;
   - by the data-processing inequality this covers every downstream route at once, so no route inventory is needed;
   - by rate–distortion it implies a copy-defect floor that tightens with the number of copied channels: a K-channel copy of bandwidth W with defect δ needs about K·W·log₂(1/δ) bit/s, so δ_K ≥ 2^{−C/(KW)};
   - the floor comes from capacity, not from injected noise, and it would remove τ, W_k, c_k, c_ω, the buckets and σ₀ as independent scalars.
2. **The layer must be derived from that invariant**, not attached to it. For example, routing by need-conditioned allocation of the capacity across partner coordinates, lags and signs (water-filling under the agent's needs), with base writes coded in bits charged against the same budget, so the bucket becomes a consequence.
3. **A measured failure it removes by construction.** The candidates are the D75 dial curve, or delayed-copy collapse of listener models on Seamless data, once the operator permits.
4. **Honest caveat.** Capacity-limited, need-weighted attention is *rational inattention* (Sims 2003; not read here), and channel-capacity limits in control are the data-rate theorem (Tatikonda & Mitter; not read here). The move may also be judged a recombination. What could make it new is the typed, all-routes, learned version whose update rule is derived from the capacity constraint. That should be tested before anyone builds it.

---

## 3. Principles

### 3.1 Principle 1
Holds. MediaPipe blendshapes, prosody features and ASR text enter as continuous features or words; there is no classifier.

### 3.2 Principle 2 (no hand-named emotion variables; emergence versus installed structure)

**Not hand-named emotions:**
- The 64 base states are unnamed, with learned centres.
- The slew display is a rate limit.
- Valence := −d𝒟/dt and arousal := ‖Δx‖ + Ψ are readouts, not fed back. The arousal readout adds the repetition load, a boredom-like quantity, to arousal, which is odd but harmless.

**Strained:**
- **The repetition drive D_R = (Ψ − Ψ*)₊.** The brief allows "a set of body variables to regulate and a few reflexes". Ψ is neither. It is a drive over the agent's *attention allocation*, installed for an anti-copy purpose, and it functions as boredom or satiation of matching. It is not named as an emotion, but it is a hand-designed motivational variable whose meaning is given. Information deficit is in the same position as a non-body "body variable". Both should either be derived (for example, Ψ as the prediction error of the agent's own allocation under 𝓜, so that repetition is the agent's own predictability) or declared as an explicit exception the operator approves.
- **Installed structure.** The ± sign slots, the per-band split, the 0.5 s and 2 s taps, the onset prior (+3 on smile and brow) and the startle reflex are declared reflexes and substrate. That is acceptable. But emotion "emerging" in the base is thin:
  - b moves only by learned jumps J from 40 event types, a tilt of at most 0.05, and noise;
  - centres are placed "from visited b weighted by drive change", and b is visited only where J sent it;
  - the landscape therefore learns where its own jumps land.
- **No emergence of affect from body regulation.** Nothing couples b back into ζ (§2.7 has no b term), so wells are not interoceptive states (§5.4).

### 3.3 Principle 3 (the other read through the agent's own body)

- **Perception: real.** P_φ is fitted on the agent's own babbling renders, and the partner is perceived as the agent's motor command that would look most like them. This is the design's strongest Principle 3 element. Note that the router, the main partner pathway, uses these motor coordinates u directly.
- **Inverting the agent's own generative map: present but not essential.**
  1. ŝ = D(ℓ) reaches behaviour only as one of the inputs to 𝓡, whose whole partner sensitivity is c = 0.15 against the 80-coordinate gate, about 0.05 per channel by the author's own account (§8.1). It also reaches behaviour as a retrieval key.
  2. Ablation 8 ("remove D: ŝ-dependent things lose ŝ-dependence") is circular. No behavioural prediction follows from the inversion.
  3. The agent's own expressive repertoire E_own is throttled: display amplitude A_k = 0.25, slew-limited. So most real partner expressions fall outside E_own's range and are read only through a projection (Theorem 9b). The agent can "read" in others only the small, slow expressions it allows itself.
  4. The c_s issue (§1.8.2) may make the inversion impossible inside the certificate.
- **What would make it essential:** a derived behaviour that depends on ŝ and fails when D is replaced by any other regressor of ℓ. For example, misreading predicted from the agent's own history: an agent that never frowned reads frowns as its nearest own state. That is testable as a state-level falsifier.

### 3.4 Principle 4 (Claude never reads state; only chooses drafts and snippets)

- **Holds for the channel.** Draft selection by predicted own drive change, verbatim retrieval by a need key, an effort level, and no numbers or labels.
- **Missing roles.** The brief also says Claude "names, reinterprets and regulates states". Here Claude's outputs reach the core only as content pulses (inside the 0.15 fence) and content events (bucket, 1 per minute, 20-min display). Claude cannot reappraise in any way the core feels within a conversation. Nothing grounds Claude's emotion words in the state (§5.6).
- Retrieval chooses past text by state. That is admissible under the llm-coupling synthesis, but it is the one place where state shapes Claude's context, and it should be audited for state-revealing regularities (for example, always retrieving sad spans when one well is occupied).

### 3.5 Principle 6 (the partner's face only as evidence; satiable drives; no reward for smiles, attention or time)

- **The face: holds.** It is never a target, reward or regulated variable (A7, Theorem 7b). The routing target is the agent's own display change; the partner appears only as a regressor.
- **Satiability:** 𝒟 is satiable, and β_sel = 0 at satiety.
- **A residual engagement incentive.**
  - The information deficit "falls with the agent's own prediction error on content", and content includes the *partner's words*.
  - Draft scores are predicted drive change.
  - So drafts that elicit surprising partner speech are selected whenever 𝒟 > 0.
  - That is a satiable curiosity reward on the user's talk: a mild version of "reward for attention". Excluding the partner's face does not exclude this.
  - **Fix:** the information term should count only prediction error the agent's own actions did not cause (attribution-weighted), or exclude partner speech from the draft-score's information component.

### 3.6 Principle 10 (one formal core or an assembly?)

**An assembly.** The author's own honest note concedes it: "one objective plus a predictive constraint plus typing rules, the same shape as the earlier designs".
- None of the nine replay losses (§6.3) is a gradient of the stated objective 𝔼Σγ𝒟. The router regresses on a shared-fate coefficient, H on decodability, ψ on visited states, the events on drive change.
- 𝒟 itself affects behaviour only through draft-selection strength, σ_d and replay priorities.
- The face's behaviour is not derived from the drive.
- About 45 innate constants carry the guarantees.
- By the brief's standard ("a component the core does not produce is not added") the router, the base, the attribution, the gate and the own variation are all added.

---

## 4. The expressive-structure items

| Item | Assessment |
|---|---|
| **Content-dependent selection at the level of attention** | **Partly.** The router is attention in form, but it selects among a fixed index set (32 own channels × 16 partner coordinates × 2 lags × 2 signs). Its values are scalar partner coordinates, so its output is a need-selected signed gain matrix: a mixture of 2048 fixed linear maps. What is selected is *which channel copies or counters which*, not perceived content, memories or actions in a learned space. Need-conditioned retrieval of past episodes for Claude is genuine content-dependent attention, but it sits outside the affective core and the face. Nothing in the core is "hunger makes food cues salient": percepts are 16 motor coordinates, with no cue space for needs to select over |
| **Structure over people, episodes, topics and time** | **Thin.** People: an 8-dimensional key frozen per session, acting through biases \|h_c\| ≤ 0.5 and the jumps J. Episodes: tags on stored records. Topics: 32-dimensional content heads into a capped fibre. There are no sets, graphs or fields over people or episodes in the core state itself. Time scales are well structured (Theorem 8), but most of them are innate constants, not learned structure |
| **Effective dimensionality** | Claimed: 24 + 96 + the simplex. In fact:<br>• the fibre's 96 dimensions forget in 3.3 s and respond to the partner within c = 0.15;<br>• the base sits in one well at a time, so the persistent affective state is a single categorical variable with ≤ 64 values (6 bits). Its position inside a well (radius 0.1, tilt ≤ 0.05) is negligible;<br>• the expressed persistent state moves at most 0.0017 per second.<br>The **ablation claim (i)** (a 1-D base cannot hold a relationship mood and an episode feeling independently) applies to the full design too: two persistent factors must be product-coded into separate wells (for example 8 × 8). The landscape has no factorised structure that makes them independent. A low-dimensional version "cannot produce" only what the full version also cannot |
| **Richness from structure, not parameter count** | 730k parameters, about 280k of them in the REN, whose partner influence is capped at 0.15. The design spends its structure on *limiting* richness (fences, caps, slews) and does not show richness that comes from composition. The author's own biggest risk is unmeasured expressivity (§8.1). |

**Answer to "64 base states + a REN: few gauges or rich?"** Not scalar gauges: the router's signed per-channel selection is genuinely richer than one gain, and it meets the per-expression, sign-flipping part of D78. But the *affective state* is one 6-bit categorical gauge plus 5 body gauges, shown through a 20-minute slew. By the brief's test (behaviour that a low-dimensional version cannot produce, demonstrated by ablating structure), the design has one valid example: ablation (ii), the box against the mass. It has none for the affective state. Minimum fix: a factorised base, a product of several small landscapes, or a field over κ_rel, with an ablation showing two independent persistent factors.

---

## 5. What it fails to explain

### 5.1 Vocal convergence on held levels (pitch, intensity, rate, voice quality)

- **The human data.** Speakers converge in mean F0, intensity and speaking rate across a conversation, and turn by turn, and the convergence outlasts the conversation (Levitan et al. 2011/2012; Pardo 2006, project notes; non-copying synthesis C9 for rate; Duran & Fusaroli on speech rate).
- **What the design does.** It makes held levels *invisible* by construction:
  - u is the deviation from a 60-s partner baseline, so the router's response to a held level decays to 0 (Theorem 6a);
  - the floor rule (speak ≥ 0.2 s after the partner stops) means the partner's voice is silent when the agent's own speech is generated;
  - N_own sets the agent's speaking prosody "from its own text and own state only"; own-speech prosody has no gate input;
  - the only remaining routes are the fibre's level input ℓ, capped inside the shared 0.15 budget, and the base display (events, 20-min slew).
- **So** turn-by-turn F0 and intensity entrainment, and slow convergence of speaking rate and voice quality to the partner's levels, cannot be produced at human magnitude. "Loudness convergence … is a positive slot on the loudness coordinate" (§5.4) applies only to backchannels and deviations, not to held levels.
- This is the held-level gap that designs.md lists for the next reading round, and here the design's proved level-blindness turns it into an impossibility.
- **Fix:** a separate *parameter-convergence* route, the one C9 explicitly permits. A slow, bounded adaptation of N_own's prosodic set points toward the partner's turn-level statistics, typed as parameter learning within the session, with its own innate ceiling. It converges statistics and is barred from frame-level matching by construction.

### 5.2 Fast match, then context at 2–4 s

- **Mostly produced.** The router tap at 0.35–0.65 s with an onset prior gives the fast match. The key low-pass τ_ω = 2 s and tap ℓ₂ at 1.5–2.5 s give a context sign change at about 2 s (Carr 2014; Weyers 2009). Known context acts at once through z^own, which fits Mauersberger 2022's early context effects for laughter.
- **Two gaps.**
  1. The mimicry synthesis says the response depends on *where the expression is aimed* (gaze, head) and *what it is about*. Partner **eye gaze is not among the 16 coordinates** (only head pose), and "what it is about" reaches the router only through REN keys, capped and with 3.3-s memory.
  2. The "anger at a shared foe versus anger at me" distinction needs appraisal of the referent, which the design routes into a capped fibre.

### 5.3 Partner history within minutes

**Not representable.** The human data:
- an unfair offer removes smile return *immediately* and reputation changes anger return later (Hofman 2012);
- one pairing changes later responses (Likowski 2008);
- crossed sensorimotor training acts within 50–90 min (Cook 2014, via the self–other synthesis).

In the design:
- weights change only in nightly replay (A8);
- κ_rel is frozen after the first 5 s;
- the router queries and the fibre see the base only through b̃, slewed at 1/600 s⁻¹, so moving the routing context by one well separation (0.5) takes at least 5 min;
- the fibre forgets in 3.3 s.

There is no carrier for "this partner just did X, so for the next ten minutes I respond to their smile differently". **Fix:** an own-typed, within-session relational state, fast-written and slowly decaying, that conditions the router queries only (outside the face path, so Theorem 3's pointwise router bound is unaffected because that bound holds for every logit). It could be fed by attributed partner events and content.

### 5.4 Temperament over months

- **Partly addressed.** Nightly replay with an EWC-type anchor moves centres and biases over weeks, and the base is saved across restarts.
- **Not explained.**
  - In the affective-science sense (Rothbart; Kagan), temperament is stable differences in *reactivity and regulation*: thresholds, intensities, recovery times. Here every reactivity constant (caps, slews, σ₀, buckets, ε_b) is innate and fixed for life. Only *where* the wells are can change, not how reactive the agent is.
  - The anchoring precision is assumed, not derived.
  - S6's "relationship specific to the operator" rests on biases of at most 0.5 and the jumps J. Whether that is enough to measure is unknown.

### 5.5 Interoception

**Decorative.**
- The five body variables are bookkeeping for a disembodied agent (energy, motor effort, information deficit, sleep pressure, voice effort).
- The base affects the body only through display effort.
- The body affects the base only through a tilt of at most 0.05 and threshold events.
- Interoceptive prediction (allostasis, in which emotion regulates and predicts the body: Sterling; Barrett; Seth) has no counterpart.
- So the brief's testbed aim cannot be expressed: concepts built over interoceptive plus exteroceptive states, and the subcortical-versus-conceptual contrast.
- **Fix:** give wells *bodily consequences* (b sets ζ* set points or time constants), and give body predictions as the content wells are learned from.

### 5.6 Grounding of concepts named by Claude

**Absent.**
- Draft selection scores drafts by predicted *drive change*, not by fit to the current state. Claude can say "I'm delighted" from any well, and nothing selects against it.
- There is no learned association between the agent's own words and its wells, so naming is ungrounded.
- **Fix, without labels or state text:**
  1. Train in replay a content head that predicts the agent's own (b, ζ) at utterance time from the embedding of its own past utterances.
  2. Add to the draft score the log-likelihood of the current own state under that head.
  3. Drafts whose affective content fits the state are then preferred, and Claude's emotion words become grounded by selection.
- This also gives Claude a regulating role: reappraising drafts that the state does not predict move the base only through content events, which can be measured.

### 5.7 Further gaps

- **Fast emotional reaction to content.** People show appraisal-driven facial responses within about 1–2 s of hearing news. Here content reaches the face only through content pulses (inside c = 0.15 shared by 80 inputs, about 0.05 per channel) or through a content event plus the base display (about 0.025 per channel after 1 min). The agent's *own* emotional reactions to what is said are nearly invisible on its face at conversational time scales. Only the partner-face-driven router is fast. That inverts the brief's goal that expressions come from an internal state.
- **Own intention, not noise.** The self–other synthesis (point 5) asks for a competing *own intention* (a set-point face, rhythms, tone), so that generic selection resists the mirrored input. The design's defect floor comes mainly from injected band-limited noise d. That defeats a copy metric without being an intention. Human "own variation" is state-driven and structured.

---

## 6. Concrete changes

In priority order.

1. **Correct the novelty claims (§10, §4, §1).**
   - Composition result 1 is average-dwell-time switching (Hespanha & Morse) plus B/R-tipping (Ashwin et al.).
   - "Only fibred" is false (p-dominance, k-contraction).
   - Result 2's "no quadratic ceiling" is false: Q = −(I + α𝟙𝟙ᵀ) gives a joint ℓ₂ budget, and it separates more strongly than the worst-case ℓ₁ mass.
   - Result 3 is the coherence / sensitivity-plus-noise bound.
   - The router is constrained softmax with coverage (Martins & Kreutzer 2017; Malaviya et al. 2018; Tu et al. 2016).
   - A1–A8 are an information-flow type system.
   - Cite these sources and reword §10.
2. **Count noise-induced tipping.** Either make the tilt t_ψ independent of partner-influenced ζ components, or bound the escape-rate modulation and count noise-driven partner-influenced switches against the bucket. Restate Theorem 6(a) in law, not only deterministically.
3. **Fix Lemma 2(c).** State the premise that partner-caused switches are required, and list a sub-barrier continuous port as the alternative innate stop.
4. **Specify c_s** and check that D can invert E_own under (R). Otherwise restate Theorem 9(b).
5. **Consider replacing the router's ℓ₁ mass by a non-diagonal IQC inside the REN, or justify the mass by input-selectivity rather than by Lemma 4.** This removes τ, W_k and the clip/projection, which is a scalar deletion in the spirit of clause 2.
6. **Add a bounded within-session relational state** that conditions router queries (§5.3), and **a bounded prosodic parameter-convergence route** for held vocal levels (§5.1). Both are typed as own-state changes whose effect on the face is bounded by existing theorems.
7. **Ground Claude's words** by an own-state likelihood term in draft scoring (§5.6). Remove partner speech from the information term of the draft score, or weight it by attribution (§3.5).
8. **Derive or declare the repetition drive** (§3.2). Make wells interoceptive by giving them body consequences (§5.5).
9. **Factorise the base** so that two persistent factors are independent, and write the ablation that shows it (§4). Replace or supplement the noise floor with a structured own intention (§5.7).
10. **For a new primitive (§2):** test whether an all-routes information-capacity invariant on the typed partner channel can replace the caps, buckets and noise floor, with the router derived as need-conditioned capacity allocation. Read rational inattention (Sims) and the data-rate theorem (Tatikonda & Mitter) in full first, because they may already contain it.

---

## Sources read

Project files, in full:
- brief.md;
- research/questions.md (Reports 1–3, Q9, Q16–Q18);
- research/foundations/designs.md;
- research/new-mechanisms-synthesis.md;
- research/foundations/design-fibred-attribution-core.md (all 1,145 lines);
- research/mimicry-context-synthesis.md, non-copying-dynamics-synthesis.md, self-other-control-synthesis.md;
- the opening of critique-design-modulated-manifolds.md (for format).

Primary sources, from export.arxiv.org PDFs, with the extent read:

| Source | Extent |
|---|---|
| Revay, Wang & Manchester, Recurrent Equilibrium Networks (arXiv 2104.05942) | §I–IV, Definition 3 and the IQC special cases, Theorems 2–3, §VI expressivity |
| Forni & Sepulchre, Differential dissipativity theory for dominance analysis (1710.01721) | abstract, §I–IV (Definition 2, Theorems 1–3, Corollary 1, the monotonicity link) |
| Wu, Kanevskiy & Margaliot, k-Contraction: Theory and Applications (2008.10321) | abstract, §1 |
| Ashwin, Wieczorek, Vitolo & Cox, Tipping points in open systems (1103.0169) | abstract, §1–2 (B-, N-, R-tipping; R-tipping criterion) |
| Makarenkov & Phung, Dwell time for switched systems with multiple equilibria (1703.06205) | §1–3 |
| arXiv 2405.03560 (converse Lyapunov results for average dwell time) | §1–2, for the Hespanha–Morse definition and the chattering bound |
| Burden, Libby & Coogan, Infinitesimal contraction analysis for hybrid systems (1811.03956) | abstract, §I |
| Jaumann, Wildhagen & Allgöwer, Token bucket specification in rollout control (1911.10847) | §1–2 (the token-bucket specification and its control lineage) |
| Malaviya, Ferreira & Martins, Sparse and constrained attention for NMT (1805.08241) | §1–4 (csoftmax, csparsemax, fertility bounds, eq. 5) |
| Tu et al., Modeling coverage for NMT (1601.04811) | §1–3 (coverage vector, fertility) |
| Ramsauer et al., Hopfield Networks is All You Need (2008.02217) | §1–2 (energy, Definition 1, Theorems 3–5, metastable states) |
| Campos et al., Skip RNN (1708.06834) | §3 (update gate, budget loss) |
| Harb et al., Options with a deliberation cost (1709.04571) | §3–4 (switching cost) |
| Lanillos, Pages & Cheng 2020 (2004.05473) | §2–4 (checking the attractor/imitation passage) |
| Alvim et al., Differential privacy versus quantitative information flow (1012.4250) | §1 (the differential-privacy definition and its bound on mutual information) |

**Named but not read in the original:**
- Hespanha & Morse 1999 (definition taken from 2405.03560);
- Fenichel 1979 and Tikhonov (standard statement only; not load-bearing);
- Martins & Kreutzer 2017 (through Malaviya);
- Denning 1976 and Goguen–Meseguer 1982;
- Sims 2003 (rational inattention);
- Tatikonda & Mitter 2004;
- Levitan et al., Pardo 2006 and Hofman 2012 (project notes, through the syntheses);
- Sutton, Precup & Singh 1999 (options).

The reductions in §1.2–1.5 rest on the sources read. Where a reduction cites only an unread source, it is marked.
