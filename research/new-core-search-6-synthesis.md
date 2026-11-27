# Searching for a new core mechanism, sixth pass: how a rich latent is structured and learns so that affect emerges in it (synthesis, 2026-11-27)

**Scope of this pass (D93).** The per-expression copy ceilings are taken as given (research/foundations/conjecture-five-passes.md: no core avoids them). This pass looks for novelty in how a rich learned latent state is structured and learns so that emotion emerges as structure in it, in three areas: affect geometry in learned representations and brains; temporal hierarchy in recurrent world models; grounding of interoceptive latents.

## Sources read (notes in research/)
| Note | Area | How fully |
|---|---|---|
| yamashita-tani-2008-mtrnn.md | temporal hierarchy | full text (PLOS HTML); Table 1 numbers and equation images not read |
| saxena-ba-hafner-2021-clockwork-vae.md | temporal hierarchy | full main text and appendices A–D (arXiv); sample galleries not inspected; Table 1 cells not quoted |
| stephan-2016-allostatic-self-efficacy.md | interoception, allostasis | theory and derivation sections in full (Frontiers HTML); equations reconstructed from text; anatomy-of-metacognition, DCM and diagnosis sections skimmed |
| liu-2024-emotion-selectivity-object-cnn.md | affect geometry, learned models | full text (PLOS HTML); S1 supplement not read |
| bush-2017-distributed-affect-mvpc.md | affect geometry, brains | full text (Frontiers HTML); supplement not read |
| sarkar-etemad-2020-self-supervised-ecg.md | label-free body latents | full text (arXiv, journal version) |
| ross-2020-unsupervised-wearable-autoencoders.md | label-free body latents | full text (arXiv); some table cells did not extract and are not quoted |

**Not reachable from here** (nothing below rests on them):
- Gumbsch, Sajid, Martius & Butz 2024, THICK (ICLR): proceedings.iclr.cc does not resolve; openreview.net returned 403 for the PDF; no arXiv version found.
- Petzschner, Garfinkel, Paulus, Koch & Khalsa 2021 (*Trends Neurosci.*, computational models of interoception): the PMC page returned a CAPTCHA, and pmc.ncbi.nlm.nih.gov does not resolve for the fetch tool.
- Horikawa, Cowen, Keltner & Kamitani 2020 (*iScience*, high-dimensional categorical emotion representation): bioRxiv returned a rate-limit error; cell.com refused by the proxy.
- Abdel-Ghaffar et al. 2024 (*Nature Communications*, occipital-temporal tuning to affective features): nature.com refused by the proxy.

The brain side of area 1 is therefore thin: one decoding study (Bush et al.), not an RSA study. arxiv.org, journals.plos.org and frontiersin.org worked.

No checks were run in this pass. No emotion labels or named emotion variables appear below the Claude layer in the directions below. "Channel" is a face or voice feature in the agent's own coordinates; "body variable" is one of the innate regulated variables; "need" is a body variable's deficit.

## What this pass adds
- **Why slow variables form, stated as mechanism** (Yamashita & Tani). Three conditions together: separated leak rates; the slow block reaches the world only through the fast block; a prediction loss whose information the fast block cannot hold across its horizon. The fast block mispredicts at branch points, and that error is what trains the slow block. With equal time constants (ratio 1) and everything else the same, the hierarchy fails (p < 0.01). Retraining only slow↔fast weights recombines existing fast primitives into new sequences.
- **Why slow levels hold slow content, stated variationally** (Saxena et al.). A level that ticks every k^{l−1} steps pays its KL once per tick, so persistent information is cheapest high up. The information per level is measurable (KL per level: 397 / 41 / 2.7 / 0.0001 nats in the 4-level model) and moves down when objects speed up. **The slowest level stored per-episode textures:** global nuisance, not anything semantic.
- **A slow coordinate defined by self-reference** (Stephan et al.). Reflex as a clamped prior descending interoceptive surprise; allostasis as a higher level setting the prior's mean (known-sign threat) or precision (unknown-sign threat); a metacognitive "allostatic self-efficacy" belief fed by whether the agent's own regulation is reducing surprise. Failure of that belief is proposed to give fatigue, then generalised helplessness.
- **Affect-like structure emerges from non-affective training, but is found only with external labels** (Liu et al.). Object-trained VGG-16 units become valence-bin selective, more in deep layers, not in an untrained network; gain-up and lesion of those units moves a separately trained read-out (lesion up to about 80 % loss in deep layers).
- **In brains, valence and arousal are weak, distributed, partly non-linear read-outs** (Bush et al.). Across 32 people, whole-brain linear read-out: valence 59 %, arousal 56 %. Whole brain beats every ROI set; the amygdala alone predicts neither. Within one person, read-out is at chance (arousal below chance). It fails for clearly valenced images of moderate arousal.
- **Label-free body latents learn the person first** (Sarkar & Etemad; Ross et al.). Self-supervised ECG and ECG+EDA autoencoder latents carry arousal-related information, but both evaluations shuffle 10-s windows across folds (same person and same clip in train and test), and Sarkar & Etemad report that subject-independent performance is poor. Window encoders have no time scale above 10 s.

---

## Direction 1: the efficacy-indexed slow level. Slow affective coordinates fed only by the agent's own regulation trend

### (1) The object
- **Per body variable i** (innate set, Principle 2):
  - a **reflex** on x_i: action a_i = −λ_i π_i ∂S_i/∂x_i, where S_i = ½ π_i (y_i − g(μ_i))² is the precision-weighted surprise of the agent's own interoceptive signal y_i under the reflex prior (μ_i, π_i) (Stephan et al.'s Bayesian reflex);
  - an **allostatic level** that sets μ_i(t) and π_i(t) from the fast latent's predictions.
- **A slow efficacy field** E ∈ ℝ^{n×K}: one entry per body variable i and per learned context key κ ∈ {1…K} (person, episode type, place; keys learned by clustering the slow latent, not named). Its only input is the trend of the agent's own surprise during the agent's own regulating action:

  E_{i,κ} ← E_{i,κ} + η_E · w_κ(t) · [ −Ṡ_i(t) · 𝟙{‖a_i(t)‖ > 0} − E_{i,κ} ],

  with w_κ the soft assignment of the current moment to key κ.
- **Typing rule (from MTRNN's connectivity constraint).** E reads no partner features, no face channels and no words directly. It reads only (S_i, Ṡ_i, a_i) of the agent's own body.
- **What E does.** It sets the allostatic level's precision policy (low efficacy in a domain → lower π_i and less vigorous regulation there, Stephan et al.'s "fatigue" as energy saving), and it enters the rich latent as one more slow input.

### (2) What it gives (derived)
- **Affective coordinates about the self.** Fast valence-like read-out −Ṡ (Joffily & Coricelli's −dF/dt, already adopted); slow read-out E, the integral of the same signal under action. Arousal-like read-out: the precisions π_i the allostatic level sets. None is a named variable; all are read-outs of body-regulation statistics (Principle 2).
- **Structure over needs and people** (brief: sets, graphs or fields, not gauges). E is a field over (need, context). "Regulation works with this person, fails at this hour" is a property of the field. Generalisation of failure across domains is a learned coupling between rows of E.
- **Satiable and bounded.** Over an interval, ∫ −Ṡ_i dt = S_i(t₀) − S_i(t₁) ≤ S_i(t₀), so the input to E is bounded by the deficit that existed (the Joffily–Coricelli argument).
- **Ablation predictions.** Clamp E: the agent's regulation vigour stops differing across contexts; per-person differences in how fast it calms with that person vanish. Cut the typing rule (let E read partner features): E becomes a partner-content variable and its per-person rows track the partner's displayed state rather than the agent's regulation.

### (3) Q18 check, with the ceilings given
- **No new expression route outside the ledger.** E reaches expression only through the rich latent and the existing per-channel caps. Anything a partner can change in E is a partner behaviour, so its expressed effect is already bounded by Theorem 1 (contingency included, Corollary 1b).
- **But E is a contingency route by construction.** A partner who comforts the agent makes Ṡ fall, so efficacy-with-this-person rises. That is the intended "you responded to me", kept in the state (D81).
- **Selection hazard (pass 5, C1).** If E biases what the agent does (which needs to attend, which contexts to seek), the agent drifts toward behaviours a regulating partner answers. With no reward and no learning on the partner's smile, this is still occupation shift by selection. It must be audited as a route class: occupation of the agent's own modes conditioned on the partner's reaction.
- **Flattery hazard.** If any body variable is relieved by the partner's smile (a contact need relieved by display rather than exchange), E learns "this person's smiles regulate me". The positive-drives synthesis already forbids that relief source. This direction depends on it holding.
- **A built-in attractor.** Persistent surprise drives E down, which lowers regulation vigour, which keeps surprise up: the helplessness fixed point Stephan et al. propose for depression. It is a property of the object, not a side effect. The exit has to come from outside E (Claude's regulation path, Q26 source 1).

### (4) Reduction check (honest)
- **Hierarchical Gaussian filter / hierarchical active inference.** A higher level updated only by the precision-weighted prediction errors of the level below is exactly the HGF's message passing (Stephan et al. use it for layer 1). E is a level of that hierarchy.
- **Hesp et al.'s affective charge** (index: adopted) is the change in confidence of the agent's own policies; E is its slow average per context.
- **Learning progress** (Oudeyer et al.'s IAC, index) is −d(error)/dt per region; E is learning progress on regulation error, per need and context.
- **Keyed memory.** The context index is a soft key-value store (attention over learned keys).
- **Verdict: recombination** (HGF + affective charge + learning progress + keyed memory). The typing rule (slow level reads only own-regulation statistics) is a design rule, not a new computation.

---

## Direction 2: the rate-priced clock hierarchy with a separate nuisance slot

### (1) The object
- **A hierarchical recurrent state-space model** (CW-VAE form) over the agent's streams: own body variables b, own motor efference, the partner's face and voice in the agent's own coordinates p, word and turn events w.
  - Levels l = 1…L tick on the clock k^{l−1} (frame 33 ms; k = 6, L = 6 gives ticks of about 33 ms, 0.2 s, 1.2 s, 7 s, 43 s and 4.3 min at levels 1–6; anything slower is learned in nightly replay).
  - ELBO with **KL charged per tick**: Σ_l Σ_{t ∈ T_l} KL[q(s^l_t | s^l_{t−1}, s^{l+1}_t, e^l_t) ‖ p(s^l_t | s^l_{t−1}, s^{l+1}_t)].
  - **MTRNN constraint:** levels l ≥ 3 receive no encoder embedding e^l of partner features or words, only the level below. The slow levels are learned from what the fast levels fail to predict.
- **A nuisance slot** n (one latent per session, fixed within a session; lighting, camera pose, microphone gain, sensor placement), with its own prior and KL, conditioning only the observation decoders. Persistent per-session factors are routed there instead of into the slowest affective levels.

### (2) What it gives (derived)
- **Time scales from reflex to temperament as levels,** with a variational reason for what each level holds: a factor lands at the level whose tick matches its persistence, because that is where it costs least KL (Saxena et al.'s argument).
- **A built-in internal measurement.** The KL per level is how many nats each time scale holds. "A temperament level exists and holds about the operator" becomes a measured, label-free quantity; removing a level should move its information to the level below (a lesion with a numerical prediction).
- **Information content adapts to the person's tempo** (Saxena et al., Fig. 8): a slow-moving partner pushes more information up.
- **Recombination by slow-only relearning** (Yamashita & Tani): nightly replay that updates only the upper levels' connections changes how existing fast patterns are sequenced without touching them, which is a precise meaning for "temperament changes slowly, reflexes stay".

### (3) Q18 check, with the ceilings given
- **No route outside the ceilings** on expression: the decoders are output-side, and the caps sit on every channel.
- **The slow levels will know the partner's persistent state.** Earlier designs' slow states tracked the partner's held face at r ≈ 0.9 on one-minute means (report 4; the fibred core's base at r 0.93). Under D81 this is allowed knowing, and the ceilings bound its expression.
- **Uncapped exit through Claude.** The slow state reaches Claude by changing how it processes. If the slowest levels hold the partner's mood, Claude's words drift toward it: content-level conformity, which the face ceilings do not see and which the shadow run counts only if it neutralises words (conjecture §4, point 3). It must be tested with pass 5's three content probes (challenge, stated preference, framing).
- **No dial is created.** k and L set time scales for all channels together; they are not partner-steerable.

### (4) Reduction check (honest)
- The hierarchy is CW-VAE (RSSM plus fixed clocks), whose parts are the Clockwork RNN (index), VTA and Ladder VAEs. The input constraint is MTRNN's. The nuisance slot is a standard group-level (per-session) latent in a hierarchical VAE.
- **Concrete failure without the slot:** the slowest level stores per-session appearance, as CW-VAE's top level stored textures and as the label-free physiological latents encode the person and the session (Sarkar & Etemad; Ross et al.). **Concrete failure with it:** the slot is fixed per session, so anything that persists for a whole session (a low day, a cold room) has two equally cheap homes, and the split between "mood" and "nuisance" is not identified. A day-long mood can be absorbed as nuisance.
- **Verdict: recombination** of known world-model parts. Useful as the build core's slow-state design, not as a new core.

---

## Direction 3: affect as a found direction, not a block. Own-drive selectivity with gain and lesion tests

### (1) The object
- **No affect block anywhere.** After any period of learning, compute in the trained latent z (all levels) the directions v that best predict the agent's own drive change −Ḋ(t+τ) over horizons τ ∈ {1 s, 30 s, 10 min} (D = Σ_i S_i, or per need), by a linear read-out fitted on the agent's own logs. Also find the units with the largest selectivity d′ for high vs low −Ḋ.
- **Never used for control.** v is a measuring instrument and a target for lesions: scale the gain of the most selective units up or down, or zero them, and compare with random units of equal number (Liu et al.'s protocol, with the agent's own drive change in place of human ratings).
- **Distribution test** (Bush et al.): compare a read-out from the whole latent with read-outs restricted to each block or level. "Affect lives in one block" is a failure flag.

### (2) What it gives (derived)
- An operational, label-free meaning for Principle 2's "valence and arousal are read out of the latent, not set": valence-like = the direction predicting the agent's own −Ḋ; arousal-like = the direction predicting the allostatic precisions.
- Lesion predictions written in advance: gaining up the −Ḋ-selective units should change regulation vigour and expression in the direction of drive relief, more for deep (slow) units than shallow ones (by analogy with Liu et al.'s depth trend, not derived).
- A geometry check: if the read-out is strong only at moderate drive change and fails at the extremes, or the other way round, that is the same shape of non-linearity Bush et al. found, and it argues against a linear two-axis affect model inside the engine.

### (3) Q18 check, with the ceilings given
- No route: read-outs drive nothing. Lesion experiments run offline or in the battery.
- **Content confound.** A latent trained on the partner's face and words will contain partner-content directions that predict the agent's −Ḋ simply because partner content and the agent's relief co-occur (Liu et al.'s units responded to what pleasant scenes contain). The read-out must be checked against the neutral-partner shadow run: the part of v·z that survives with the partner's expressive stream set to neutral is the agent's own.

### (4) Reduction check (honest)
- Linear probing plus causal ablation (standard interpretability), with the agent's own drive change as the target. **An evaluation method, not a mechanism.** It belongs in evaluation.md's battery, not in the core.

---

## Overall verdict

- **No direction clears the novelty bar.**
  - Direction 1 is HGF / hierarchical active inference with affective charge and learning progress, keyed by context. Its one design rule (slow level reads only own-regulation statistics) is valuable but is a typing rule. It has a helplessness attractor and a selection route to audit.
  - Direction 2 is CW-VAE with MTRNN's input constraint and a per-session nuisance latent. It gives the clearest account read so far of why slow levels hold slow content and how to measure it. It fails by storing session nuisance at the top, or, with a nuisance slot, by leaving the mood/nuisance split unidentified for day-long states.
  - Direction 3 is an evaluation protocol.
- **Why everything reduces, in this area too.**
  1. **Emergence is a property of the objective, the data and the time-scale structure, not of a new operator.** Every source that shows structure emerging (MTRNN primitives, CW-VAE levels, Liu et al.'s selectivity, the physiological latents) does it with standard parts: leaky or clocked recurrence, a prediction or reconstruction loss, a connectivity constraint. What emerges is decided by what persists and what is predictable in the stream. A "new core" in this area would have to be a new objective or a new data regime, and the objectives found (surprise descent, ELBO with per-tick KL, learning progress) are known.
  2. **Self-reference is the only structural lever found that is specific to affect**, and it is already the active-inference line: the slow affective coordinate should be a statistic of the agent's own regulation (Stephan et al.; Hesp et al.; Joffily & Coricelli). Applying it is a design decision for the build core, not a new mechanism.
  3. **Time scales: order from structure, magnitude from rates,** as in all five earlier passes (τ = 5/70 in MTRNN; k in CW-VAE).
  4. **The data say a two-axis latent is wrong, but do not say what is right.** Bush et al. (59 % / 56 %, distributed, failing at moderate arousal) and the earlier Kragel & LaBar and Russell notes agree that valence and arousal are partial read-outs of a richer state. None of the sources read gives the structure of that richer state; the two unreachable sources (Horikawa et al.; Abdel-Ghaffar et al.) are the ones that would.
- **Most useful products for the build core** (none needs a new design):
  1. **Typing rule for slow affective levels:** they read only the level below and the agent's own regulation statistics, never partner features or words directly (MTRNN constraint plus Stephan et al.'s self-efficacy input). Expected effect: the slow state is about the agent; partner knowledge stays in fast and partner-model levels (D81).
  2. **A nuisance check for every slow latent:** measure how much of each slow level is explained by session identity (lighting, pose, gain, time of day). If session identity explains it, the level is storing nuisance, not mood.
  3. **KL per level as a label-free internal measurement** of how much each time scale holds, with level lesions predicting where the information goes.
  4. **Own-drive selectivity with gain and lesion** (Direction 3) added to the evaluation battery, with the neutral-partner shadow run as the content-confound control.
  5. **Two new hazards to audit:** the efficacy (helplessness) attractor if a self-efficacy level is adopted; Claude-route conformity if slow levels hold the partner's mood (use pass 5's content probes).

**designs.md:** no candidate deserves a line as a new design. Items 1–3 above are refinements of the Cayley-ledger build core's slow state and belong in its specification if adopted, not in the designs table.

## Next steps
1. Read, if the hosts open: Horikawa et al. 2020 and Abdel-Ghaffar et al. 2024 (affect geometry in brains), Petzschner et al. 2021 (interoception models), Gumbsch et al. 2024 (THICK: adaptive, event-triggered slow levels, which would directly address Direction 2's fixed clocks).
2. If the search continues, look for **objectives** rather than operators: what a latent must predict, over which horizons and with which counterfactuals, so that slow levels hold the agent's own regulation history rather than session nuisance or the partner's mood. That is the one place in this area where something new could still be found.
