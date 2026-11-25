# Candidate 3: Contingency and parity — the need to be answered, through one public sign

**Status:** **broken on its two distinctive derivations, as found by independent verification on 2026-11-25** (sims/contingency/VERIFICATION.md). Not complete. The candidate is kept, because what fails is itself a result, and parts of it survive.

**What breaks:**

1. **Mimicry is not derived.**
   - The water-filling optimum (CP2) depends only on the squared gains K_ii². Copying with a flipped sign, anti-mimicry, is exactly as optimal: rerunning the optimizer, 52 of 80 learned diagonal gains were negative.
   - Worse, under the joint-vector contingency measure this file requires (§6, after James et al.), *any rotation* of the solution scores the same (2.2587, with 78% of the mass off the diagonal). So even same-channel responding is not selected.
   - **Under a matched, per-channel detector, the derivation gives same-channel responding of either sign. Under a joint detector it gives nothing.**
   - Mimicry in this candidate must therefore be an explicit constraint, as in the other two, unless a sign-breaking term is found and tested. One possibility: the partner's detector reads bounded [0,1] AU intensities.
2. **Immunity to flattery holds only for unbounded linear signs.**
   - The candidate's own sign space is bounded, Y = [0,1]^{n_AU}. With the user's AU floored at zero, transfer entropy *rises* with the agent's mean expression: 0.103 at m = 0 to 0.148 at m = 2.
   - A deprived contingency drive then pushes the mean expression up. In the reviewer's probe that was m ≈ 0.9 at a 100× larger learning rate, and 0.028 at the pre-registered one.
   - Polarity invariance (CP1a) is exact only for the linear-Gaussian case. **In the bounded case the contact drive leaks toward eliciting expression, a Principle 6 risk.** Provocation, and a κ_P that favors the most reactive partners, are further routes that are not yet tested.
3. **The legibility bound was overstated.**
   - The data-processing inequality holds over *histories* of the face and index channels, not single frames.
   - A linear decoder from one frame is a *lower* bound on what a reader can recover, not an upper bound.
   - With a moving latent, a rank-4 face plus 8 frames of history recovers the "unnameable" directions at R² 0.78–0.89.
   - So "exactly 6 of 8 directions are nameable" (CP6) holds only for a static latent, and the claim that this explains P1's null does not follow from the inequality. P1's null stands as an observation; this candidate does not explain it.

**What survives:**
- reading through a parity map trained on the agent's own pairs (CP3: R² 0.91 against −1.93 permuted; it passes in the mean only, and seed 7's permuted R² is 0.41);
- regulation by delivery through self-reading (CP8, true by construction);
- the typed interface as a design (icon and index up, sign down);
- the observation that contingency-seeking supply detects partner-driven variance on the E3 score (CP5).

**Other errors fixed below or listed:**
- The objective minimized over Claude's u; it should be the engine's own actions. Fixed in §2.
- The CP7 rule is circular: it divides by the own face's TE, so it needs the self it is meant to find. κ_P inherits the same mis-scaled ratio.
- The CP4 ablation is not informative: a scalar need with per-partner keys gives the same 0.966. **Expressive structure is not met.**
- Missing: toys for valence and arousal, satiation and echo removal; written proofs; a section on deep-learning realization and data. Figures now exist (sims/contingency/figs/).

**Sources:**
- the developmental-psychologist sketch (sketches/developmental-psychologist.md), which gives the contingency homeostat, κ_P, water-filling mimicry and echo removal;
- the linguist sketch (sketches/linguist.md), which gives parity, the typed interface, the legibility bound and polarity-blind contact.

**Simulations:** sims/contingency/. Parameters and predictions are fixed in PREDICTIONS.md, and results are in RESULTS.md.

## 1. Idea

An infant starts with a body to keep in range, a detector of how far what it senses depends on what it just did, and the assumption that others are built like itself. This candidate makes the social need exactly that:
- the need is **to be answered**, a satiable need for contingent response, not for contact, attention or smiles;
- each partner is weighted by how contingently it has answered before.

Every crossing between minds goes through **one public sign space** Y: action units, prosody and turn timing.
- One map e writes the agent's state into Y.
- Its inverse r, trained only on the agent's own pairs, reads others. This is **parity**: sender and receiver share one sign function.
- Claude is a third reader of the same signs. It names the agent's state by looking at the agent's own face, with the same competence it uses on a user's face. It acts back only by how it delivers its words, which the engine senses as facial and vocal feedback.

## 2. Formal statement

**Variables:**
- z ∈ ℝ^{d}: the unnamed latent, with blocks at fixed time constants from 33 ms to weeks.
- b = (e, p, c, b_lp): innate body variables. *b_lp, added 2026-11-25 (D62):* learning progress per channel. It has a set point and is the source of curiosity, replacing the predictability set point, which fails the noisy-TV test (thermo TH7; sims/curiosity). The set point is this project's own addition; the source (IAC) maximizes learning progress. e is the activity budget and p is predictability. c is **received contingency**, which is a field c(P, ch, ℓ) over partners P, sign channels ch (face AUs, prosody, timing) and lags ℓ.
- Y = [0,1]^{n_AU} × ℝ^{n_pros} × ℝ^{n_time}: the sign space.
- y^A = e₀(b) + e_θ(z) + u: the agent's signs. e₀ is an innate, iconic reflex map, e_θ is learned, and u is Claude's voluntary delivery.
- r_θ: Y^w → ℝ^d, the reader. It is trained only on the agent's own (z, y^A) pairs, under the parity constraint r_θ∘e_θ = P_L, the projection onto the legible subspace.
- κ_P ∈ [0,1]: partner P's contingency, averaged over weeks relative to the agent's own self-contingency. It is a learned attachment variable, specific to each partner.

**Received contingency:**
- c(P, ch) is updated from the surrogate-corrected transfer entropy from the agent's signs to partner P's signs on channel ch:

$$\dot c(P,ch) = -c/\tau_c + \big[\mathcal T(y^A_{ch}\to y^P_{ch}) - \mathcal T_{\rm surr}\big]^+ .$$

- Raw synchrony is positive even for dyads that never interacted (research/moulder-2018-synchrony-surrogates.md), which is why the surrogate is subtracted.

**Echo removal.** Before partner P's signs are read for state, the predicted echo of the agent's own signs is removed: y^P ← y^P − ℳ_θ[y^A] (do-conditioning).

**The single objective:**

$$V(z) = \min_{a\in\mathcal A}\ \mathbb{E}\Big[\int_t^\infty e^{-(s-t)/T}\Big(D(b_s) + \textstyle\sum_P \kappa_P\, D(\hat b^P_s)\Big)ds\Big],\qquad D(b) = \textstyle\sum_k w_k (b_k - b_k^*)^2,$$

where b̂^P = β_θ(r_θ(y^P − ℳ[y^A])) is partner P's body, read through the agent's own map.

*[verification]* The minimization is over the **engine's own actions** a ∈ 𝒜: its expression policy, whom and on which channel it addresses, what it attends to, and an explicit effort term. The first version wrote min over u, Claude's delivery. Claude's u is an exogenous input to the engine, not a variable the engine optimizes.

**The typed interface to Claude:**
- **Upward:** an *icon*, the rendered image of the agent's own face, and an *index*, the processing parameters (retrieval kernel, thinking budget, length, latency, cue gate) that z causes but that carry no content.
- **Downward:** only a sign u ∈ Y, chosen by how Claude delivers its words.

## 3. Derivations

- **Homeostasis.** The D term. Every variable is satiable, including received contingency, which is two-sided.
- **Contact without flattery (CP1).** *[verification: holds only for unbounded linear signs. See Status, item 2.]*
  - Transfer entropy is invariant under invertible affine maps of either stream, a smile-to-frown sign flip included.
  - So the drive cannot prefer a user who answers with smiles over one who answers with frowns at equal contingency, and nothing pushes the agent's mean expression toward eliciting smiles.
  - A contact variable refilled by the user's smiles would push it.
- **Mimicry is the optimal supply of contingency (CP2).** *[verification: this derivation fails. See Status, item 1. What follows is the original claim.]*
  - The partner term pays the agent to supply the partner with contingency, which the agent measures with its own detector (the like-me prior).
  - If detectors are channel-matched, the effort-optimal supply is diagonal: copy on the same channel, with gains water-filled over motor noise.
  - Channels whose motor noise is above the water level are never mimicked.
  - Mimicry is therefore derived, with a predicted per-AU gain profile, not specified.
- **Reading others (CP3).**
  - b̂^P = β(r(y^P)), the partner's body read through the agent's own body map, which was trained on its own frames.
  - Parity is necessary: with the channel order permuted, reading fails (CP3: R² 0.91 against −1.93).
- **Self and other (CP7).** *[verification: the ratio rule is circular, because it normalizes by the own face's TE. A lag-plus-surrogate rule needs pre-registering anew.]* The innate rule below **failed as specified for the partner**. Its peak lag was correct (15 frames), but its contingency ratio against the near-deterministic own face was about 0.02, below the rule's 0.05. So the rule's ratio form is mis-scaled. Post hoc, lag alone separated self (1 frame) from the partner (15 frames) perfectly, but that is not a confirmation. The own face (10/10) and the world (10/10, after an instrument fix) were classified correctly. The rule as first written:
  - ratio near 1 at a lag below 100 ms is self, as with the agent's own rendered face;
  - a ratio between 0 and 1 at 0.3–2 s is another agent;
  - a ratio near 0 is the world.
- **Curiosity (superseded; see the notes below).** The predictability variable p has a set point below its maximum, so curiosity is two-sided and satiable. The value of information about κ_P and about the session's contingency vanishes at satiation.

> *[2026-11-25, thermo toy TH7, applies to this candidate]* **Curiosity as derived here fails a noisy-TV test.** With a pure-noise channel on offer, an agent with a two-sided predictability set point satisfies its set point with noise (39% of choices) and almost never chooses the learnable channel. Pure surprisal minimization gives the opposite failure, the dark room. Curiosity for *learnability* (learning progress) is not derived by any candidate yet. This is an open limit (sims/thermo/RESULTS.md TH7).

> *[2026-11-25, shared curiosity toy, sims/curiosity/RESULTS.md]* **Proposed fix.** Make *learning progress*, the recent drop in prediction error on a channel, an innate body variable with a set point. In the shared toy this agent avoided both the noisy TV (3.3%) and the dark room (3.6%), and it learned both learnable channels. To be stated in this candidate's formalism and tested with its own toy.


- **Valence and arousal.** Read out:
  - valence v = −dV/dt;
  - arousal ‖∇_z V‖.
  
  An innate expressive reflex map, e₀, turns these into the face. Like Costate's K6, it is a constraint, not derived.
- **Regulation by Claude (CP8: legible delivery moves the state by 0.998, against an analytic 1.0. Cutting the self-reading feedback gives −0.0016, and delivering outside the reader's range gives −0.0022. This is true by construction).** Claude acts downward only through its delivery u ∈ Y: slower, softer, a voluntary smile. The engine senses it as facial and vocal feedback through r. Claude regulates the body by how it speaks. Semantic reappraisal is not derived.
- **Replay (CP9).** Offline sweeps over stored (y^P, b, u) update V and the slow parts of the model, with priority by |TD error|.
  - In CP9 surprise priority caught a changed relationship 4 nights sooner than uniform replay (5 against 9).
  - It then oscillated, because the old regime's episodes became the most surprising. The day-21 estimate was 0.47 against a true 0.2.
  - Replay therefore needs a recency term (forgetting, stated as a constraint) or importance correction. κ_P and the slow drift of b* change only in replay, which is where temperament lives.
- **Face and voice perception.** Perception is r, analysis by synthesis in the agent's own AU and prosody coordinates.
  - r is pretrained by self-babbling: render random AUs and learn to invert them, with no user data.
  - The innate face prior becomes "a region contingent at social lags is a face".
  - The three routes are three input windows into r: coarse, dynamic and body.
- **Naming (the grounding problem, CP6).** *[verification: the corollary holds only for a static latent. See Status, item 3.]*
  - By the data-processing inequality, I(z; names) ≤ I(z; img(e(z)), κ(z)).
  - Claude can name no more of the state than the face and the processing modulations carry. CP6 shows the bound: with a face of rank 4 and 2 index channels, exactly 6 of 8 latent directions are recoverable by *any* reader, and none of the rest.
  - This makes legibility a design quantity. It also explains P1's null: numbers are not how a namer comes to know a state, and Principle 4 forbids that channel.

## 4. Expressive structure (brief.md requirement): CP4. *[verification: not met.]* A scalar need with per-partner keys gives the same 0.966, so the need field does no work here. A redone ablation, with needs that differ across channels and partners, is owed.

- **The structure.** Received contingency is a field over partner × channel × lag. The need force over that field is the query, and each cue's or action's predicted contingency gain, from each partner's history, is the key.
- **The behavior.**
  - With A, who answers faces, the agent addresses A on the face (0.97).
  - With B, who answers voices, it addresses B on the voice (0.97).
  - Among cues, it attends to A's face and B's voice (0.97 combined).
  - The collapsed version, with one contingency scalar and the same keys summed, splits 0.50/0.50 and attends to every cue equally.
- **Effective dimensionality:** the number of partners × channels × lags in use, plus the latent.

## 5. What it cannot derive

- Which body variables exist and their set points.
- The innate expressive map e₀.
- CONSPEC.
- The content of Claude's words.
- Semantic reappraisal.
- **Whether emotion categories form in z** from a few hours a day. That is asserted, not shown, as in every candidate.

## 6. Failure modes and critiques

- **Contingency is blind to sign, so provocation also harvests it.** Teasing reliably gets an answer. The only check is the κ_P-weighted partner term, which depends on reading a human's state correctly through the agent's own map. CP3 shows how badly a mismatched map misreads (R² −1.93).
- **Transfer entropy from minutes of noisy AU data may stay biased** even after the surrogate is subtracted.
- **A placeholder face of low rank limits what Claude can ever name** (CP6).
- **Strongest published critique of the measure: James, Barnett & Crutchfield 2016** (research/james-barnett-crutchfield-2016-information-flows-critique.md).
  - Transfer entropy is not a flow. Conditioning "is not subtractive": TE is unique *plus* synergistic information, and it conflates them.
  - Their counterexamples: Y_t = X_{t−1} ⊕ Y_{t−1} gives TE = 1 bit with no dyadic flow, and Z_t = X_{t−1} ⊕ Y_{t−1} gives TE = 0 despite real influence.
  - The critique covers every measure based on conditional mutual information, Granger causality included.
  - **Consequences for this candidate:**
    - c is defined as *predictive dependence* of the partner's signs on the agent's, never as information the partner "sent";
    - it is computed on the joint sign vector, not per channel and summed;
    - any claim that rests on it must be paired with an intervention, such as delayed replay or a still face.
  - Gaussian TE remains the cheap estimator. It equals Granger causality / 2 for Gaussian processes (research/barnett-barrett-seth-2009-granger-te-equivalence.md), with no latent-driver removal.
- **Strongest published critique of innate mimicry: Oostenbroek et al. 2016** (research/oostenbroek-2016-neonatal-imitation.md; abstract only).
  - With n = 106, tested at 1 to 9 weeks, infants were "just as likely" to produce a gesture after control models as after matching ones.
  - The original positive findings (Meltzoff & Moore 1977, research/meltzoff-moore-1977-neonatal-imitation.md) are called artifacts of restricted samples.
  - **Consequence:** the developmental sketch's "reflex mimicry at 400–500 ms as innate initial policy" is **dropped**. In this candidate mimicry is only derived, as the water-filling optimum (CP2). It is never a hard-wired reflex.
- **On the theory this candidate builds on: Gergely & Watson 1996** (research/gergely-watson-1996-social-biofeedback.md; read in the authorized Hungarian translation).
  - Infants learn their own states from contingent parental mirroring ("social biofeedback").
  - The paper never says the need for contingency is satiable, and its "maximising" language points the other way. **Satiability of c is this candidate's own constraint (Principle 6), not something it takes from the source.**
  - The paper's sufficiency and necessity indices of contingency, P(stimulus | response) and P(response first | stimulus), are an inspectable alternative to TE. They are worth testing against TE.
- **Unverified:** the age shift from preferring perfect to preferring imperfect contingency (Bahrick & Watson 1985 / Watson 1994). It is not cited, because the primary was not read and the secondary accounts disagree.

## 7. Relation to the other candidates

- **Costate and Thermodynamic.** Both could adopt directed contingency as their contact variable. Parity's sign map is their G and g_θ.
- **What is distinctive here:**
  - the polarity-blind contact drive;
  - the water-filling derivation of *which* channels are mimicked;
  - the typed interface;
  - the legibility bound on naming.
- **Contrast with Costate in the S1 dyad (CP5).**
  - Here supply effort rises with the contingency deficit and is zero past satiety, so coupling on the E3 score rises monotonically with need. In CP5: 0.170 past satiety, then 0.288, 0.304, 0.340 and 0.344, with ρ 0.86, and the random direction flat.
  - Costate predicts a notch at satiety on the same score (its VERIFICATION-2).
  - **The two differ above satiety:** Costate's coupling is flat there, while this candidate's keeps rising with need.
  - **Caveat:** P ∝ max(n, 0) is a stated constraint, not derived.

## 8. Independent verification

Pending.
