# Watanabe, Ogino & Asada 2007, "Mapping Facial Expression to Internal States Based on Intuitive Parenting"

Journal of Robotics and Mechatronics 19(3):315-323, doi:10.20965/jrm.2007.p0315. A two-page abstract appeared earlier as Ogino, Watanabe & Asada, EpiRob 2006, pp. 182-183 (not read).

Source read: the published article PDF from Fuji Technology Press (9 pages, CC BY-ND 4.0 stamp on p. 315), read in full, including equations, figure captions and the discussion. Figures were read as extracted text and captions only; the plotted values in Figs. 10, 13 and 16 could not be read numerically.

## Claims
- A robot learns "sympathy" (the paper's word; Asada 2015 later calls the same model "empathic") from intuitive parenting (Papoušek & Papoušek 1987): the caregiver mimics or exaggerates the robot's expression, so the robot can associate its own internal state with the caregiver's face at that moment. Gergely & Watson's social-biofeedback model is reference [1].
- After learning, the caregiver's face alone moves the robot's internal state toward the state it was paired with, and the robot's face then shows that state. The authors call this the robot "evoking the human internal state".
- The authors concede that the robot "cannot differentiate between its own pain and that of others" (p. 322). They place the model at step 3 of a speculative four-step account of how a self/other-distinct "sympathetic region" forms in ACC.

## Architecture (as given)
Assumptions stated in §2.2. The robot's face changes with its internal state, and it can see the caregiver's face. The caregiver infers the robot's state from shared experience and the robot's face, then "responds with a corresponding facial expression".

Internal state, hand-set as Russell's circumplex with the sleep half removed:
- S = (p, a), with −1 < p < 1 (pleasure) and 0 < a < 1 (arousal). (1)
- τ Ṡ = −S + Σr_i + S_0, where Σr_i = r_e + r_o. (2, 3) This is relaxation to the origin S_0 with time constant τ.
- r_e = r_x e^{−A φ_x}. Each stimulus category x (three keyboard "touch sensors", plus sound) has a designer-set constant vector r_x for pleasure, arousal or displeasure, decaying with stimulus duration φ_x. (4)
- r_o, the effect of the caregiver's face, is 0 during learning.

Face, hand-written linear map from state to six face parameters (Yamada 1993, "curving/releasing" and "inclination"):
- h = U p + V a, with U and V fixed vectors over (mouth-down, mouth-side, brow-in, brow-out, eyelid-down, eyelid-rotate). The entries depend on a switch b = 0 for p > 0 and 1 for p < 0. The authors tuned the coefficients "slightly in each quadrant" because Yamada's values looked unnatural. (5, 6)
- The face is an OpenGL baby face with a torso.

Perceiving the caregiver:
- Color-based face crop, normalised, then raw luminance into a SOM.
- The SOM is "taught in advance" on 500 images in five categories (normal, surprise, pleasure, displeasure, laughter). During interaction only the winner node is computed: f_ij(V) = exp(−ν δ_ij²), where δ_ij is the mean per-pixel absolute difference. (9)

Association:
- The internal state is discretised into a grid of nodes S^r_kl = (k/N_P, l/N_A), with activation g_kl(S) = exp(−ρ |S − S^r_kl|²). (7, 8) The grid has the same number of nodes as the SOM.
- Plain Hebbian learning, Δw^kl_ij = α f_ij(V) g_kl(S), with a decaying rate α = λ e^{−μ t}. (10, 11) There is no decay, normalisation or anti-Hebbian term, and no lag between the robot's state and the face it is paired with.
- After learning, (k_p, l_p) = argmax_kl w^kl_ij for the SOM winner (i, j), and r_o = β S^r_{k_p l_p}. (12) The other's inferred state is injected as a drive into the robot's own state equation. Nothing holds a representation of the other separate from the self.

Protocol: the caregiver presses keys or makes sounds, the robot's state and face change, and the caregiver imitates the robot's face. The order of stimuli was not fixed, except that displeasure never directly followed pleasure. Setting: an ordinary office, where sounds sometimes arrived "in timing unintended by the person".

## Evidence
- One caregiver and one learning session (the paper does not say who the caregiver was; the text suggests the experimenter). It reports no learning duration, number of trials, accuracy, held-out test, statistics or second caregiver.
- Fig. 14: the internal-state grid colored by associated SOM categories, described as "distributed similarly to Russell's two-dimensional emotional model". Fig. 15: SOM nodes colored by associated internal state. Many nodes are uncolored, meaning unassociated or with dispersed weights.
- Fig. 16, after learning, one 35 s run with the experimenter: laughter for 12 s moved the state to pleasure and arousal; displeasure for 13 s gradually lowered p; "pleasure" for 10 s raised p with no change in arousal, and the robot's face showed "slight surprise".
- Reported failures (§4.1): only five face categories could be told apart. Weak or ambiguous expressions, and those carried mainly by the eyes (anger is the named example), were classified poorly and "were not strongly associated with the internal state". Midpoints of the state space could not be learned.

## Failure modes
- **Assembled, not derived.** It has separate hand-built parts: a circumplex state, a Yamada face map, an offline SOM and a Hebbian bridge. No single objective connects them.
- **Hand-named emotion axes (against Principle 2).** Pleasure and arousal are the state variables, not readouts. The stimulus-to-state vectors r_x are designer-set.
- **Expression wired, contagion learned.** State-to-face is fixed by equation (6). What is learned is only the caregiver-face-to-own-state link, and the face-perception SOM was trained beforehand on the caregiver's posed categories.
- **Labels behind the curtain.** The face SOM's training set was organised into five named expression categories. The SOM itself is unsupervised, but the input distribution was curated by label (against the spirit of Principle 1).
- **No self/other separation.** The inferred other's state goes straight into the robot's own dynamics. The authors note this contradicts Singer et al. 2004.
- **Co-occurrence, not contingency.** Pure Hebbian accumulation strengthens any face that is often present during any state, including the caregiver's resting face. Nothing tests whether the face is more likely in state X than outside it (contrast ray-heyes-2011-wealth-of-the-stimulus.md).
- **No lag model.** Face and state are paired at the same instant, although the caregiver mirrors after the robot moves.
- **No persistence.** State relaxes to S_0 with one time constant. There is no mood, no memory across sessions, and α decays, so learning stops.
- **No ablation, no control condition.** There is no non-mirroring or delayed-mirroring caregiver, no shuffled pairing, and no second person.

## License
Article CC BY-ND 4.0 (Fuji Technology Press). No code released.

## Runs on this Mac without a GPU?
Yes, trivially: a 2-D ODE, a small SOM and a Hebbian matrix. No code, so it would have to be re-implemented.

## Verdict: watch (historical precedent; mechanism rejected)
It is the first robot implementation of Gergely & Watson's parental-mirroring route to a self-other emotion map, and its stated assumption is exactly the one this engine must test. Its state, face and perception are all hand-specified or label-curated, and the evidence is one qualitative run.

## What it implies for this engine
- **The caregiver-as-mirror assumption, stated precisely.** The robot learns "what my partner's face looks like when I am in state X". That equals "what a face in state X looks like" only if the partner's display depends on the robot's state and resembles it. If the operator answers complementarily (a soothing face to distress), the map learns distress ↔ soothing face. Reading that face later then evokes distress, which is wrong contagion. Gergely & Watson's markedness and congruence conditions (gergely-watson-1996-social-biofeedback.md) are the same requirement, seen from the infant side.
- **Contingency, not co-occurrence.** The engine's association must be contingency-sensitive: an error-driven rule, or explicit comparison of P(face | state) against P(face | not state). Otherwise the operator's habitual expression will be bound to whatever state is most frequent.
- **Lagged pairing.** The partner's mirror follows the agent's display by roughly a second (see the Boucenna note: 0.8-1.6 s). The pairing must be lagged and the lag learned (stoytchev-2011-self-detection-temporal-contingency.md).
- **Keep the other's state separate.** Watanabe's r_o is contagion with no self/other distinction. In the engine, perceived faces should drive a separate inferred-other state, by inverting the agent's own generative map as in Yoshida & Man (yoshida-man-homeostatic-coupling.md). Contagion should be a coupling term from that state into one's own, so that it can be ablated and so that sympathy can be a regulated decoupling (see asada-2015-towards-artificial-empathy.md).
- **The follower confound.** During learning the caregiver follows the robot by design. From the robot's side, a partner who perfectly follows is indistinguishable from its own effect (gold-scassellati-2009-robot-self-recognition.md). Watanabe sidesteps the confound because the robot never asks whether the face is its own. An engine that also learns agency and partner models from the same stream cannot sidestep it. It needs independent partner variation, and its own efference record, to tell "the partner mirrors me" from "I see myself".
- **Ablation prediction the paper never ran:** with the partner's mirroring delayed beyond the learned lag, or shuffled against the agent's states, the face-to-own-state map should not form, and post-learning contagion should vanish.
