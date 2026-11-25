# Stoytchev 2011, "Self-detection in robots: a method based on detecting temporal contingencies"

Robotica 29(1):1-21, doi:10.1017/S0263574710000755. Based on chapter V of the author's Georgia Tech PhD thesis.

Source read: the published PDF hosted by the author's lab (home.engineering.iastate.edu/alexs/papers/Robotica_2011/Self-Detection_In_Robots.pdf), read in full as extracted text (all sections, algorithms, figure captions, tables, references). Numeric cell values in Tables I-III did not survive extraction; only the classifications did.

## Claims
- A robot can learn its own efferent-afferent delay (motor command to the onset of seen motion) from motor babbling. It "imprints" on that delay, then classifies visual features as "self" or "other" using Watson's two contingency indexes computed inside a delay window.
- The window's width need not be estimated: by Weber's law for timing (scalar timing), σ = βμ, so the tolerance scales with the mean delay.
- Watson's necessity index must be conditioned on the type of motor command. A shoulder marker moves for only 4 of 7 command types, so an unconditioned index stays below threshold for real body parts. Indexes must also be corrected for visibility: a TV image shows the arm only in some poses.
- Self-detection in a live TV image works with these corrections: 5 of 6 TV markers were classified "self".
- A mimicking second robot corrupts delay learning (bimodal histogram), but once the delay is imprinted the mimic is easily classified "other", because its motion onsets fall outside the window.

## Mechanism (as given)
- Motion detection: a marker is moving if its centroid moved more than 1.5 px in the preceding 0.1 s (640×480, 30 fps), then a box filter of width 5 (at least 3 of 5 frames).
- Delay learning (Algorithm 3): for each frame with a movement onset (0→1), add (frame time − time of the last motor command) to a histogram over [0, 6) s with 1/30-s bins. Only one update per frame, so a large many-part object cannot dominate. Threshold at 50% of the peak and take the mean: μ.
- Window: a movement onset at delay d is contingent if |μ − d|/μ < β, with β = 0.25 (pigeon estimates are about 0.3; other animals 0.10-0.25).
- Counters per feature i: C_i (motor commands), M_i (observed movement onsets of i), T_i (onsets that are contingent).
  - As defined in §7: "necessity index" N_i = T_i / C_i ("whether the feature moves consistently after every motor command"), and "sufficiency index" S_i = T_i / M_i ("whether for every movement of the feature there is a corresponding motor command that precedes it").
  - Per command type m: N_i^m = T_i^m / C_i^m.
  - Rule: f_i ∈ self iff ∃m: N_i^m(t) > α and S_i(t) > α, with α = 0.75.
- Naming caution: the §7 definitions are reversed relative to Watson's usage as reported in gergely-watson-1996-social-biofeedback.md, where sufficiency = P(stimulus | response) and necessity = P(response preceded | stimulus). The paper's own Summary states them the Watson way round, so the paper contradicts itself. The quantities are the same two conditional probabilities whichever name is used. A project note should use the explicit forms P(effect in window | own act) and P(own act in window before | effect).
- Visibility correction: with T̂_k = T_k + μ + βμ, if marker i is visible in fewer than 80% of the frames in [T_k, T̂_k), no counter for i is updated until the next command.

## Evidence with numbers
- CRS Plus arm, 3 joints in the vertical plane, 6 body markers. Babbling: 500 random target joint vectors (each joint moves or not at random), 2° tolerance, 8-s timeout; about 45 min per data set.
- Learned delay μ = 1.02945 s and 1.04474 s on two solo data sets (less than half a frame apart). Delays were similar across all six markers.
- Two robots with uncorrelated babbling (a video composite): the other robot's onsets spread almost uniformly over 0-5 s; μ = 1.02941 s, unchanged. Self markers had sufficiency near 1; other-robot markers had sufficiency and necessity near 0; all 12 markers were correct (Table I).
- Static background markers that are sometimes occluded: μ = 1.03559 s; all 12 correct (Table II).
- Mimicking robot (fixed 20-frame = 0.66 s lag): the delay histogram was bimodal (peaks near 1.0 s and 1.7 s) and Algorithm 3 returned μ = 1.36363 s (SD 0.334); the raw mean was 1.44883 s. The author left the algorithm unmodified, citing animal timing data, where animals learn the mean of a mixture, not its lower limit. With μ imprinted at 1.035 s from the solo data, the mimic's markers had near-zero indexes and all 12 were correct (Table III): "the mimicking test condition turned out to be the easiest one to classify."
- TV monitor (live feed from a second camera): before the visibility correction, half the TV markers had sufficiency below 0.75 (visibility 99.9, 99.9, 86.6, 72.1, 68.5, 61.7%). After the correction, 5 of 6 were "self". TV4 stayed at sufficiency 0.64 because of colour distortion.
- The author dismisses sustained mimicry as "a degenerate case that is highly unlikely to occur in any real situation". That is false for social partners: adults imitate infants often (jones-2009-development-of-imitation.md), and the engine's partner may mirror it.

## What it implies for an engine learning a partner model and its self–other face map from live contingency
- Separate the two estimation problems in time, as here. First learn the agent's own efference-to-visible-effect delay (render latency, its own following latency) and imprint it. Then use it as a fixed window when scoring others. Learning the window during interaction with a follower gives a mixture and a wrong window (1.36 s here). The engine can measure its own render/feedback delay exactly, so it never has to learn it from interaction.
- The confound in critique-design-dyadic-sheaf.md has a timing signature. When the agent follows the partner, the partner's events precede the agent's acts by the agent's own following latency. When the partner responds to the agent, the agent's acts precede the partner's events by the partner's response latency. A lag-resolved contingency (onsets inside a window after the agent's own act, compared with the base rate) separates the two cases where a same-time or exponential-trace regression cannot. This works only if the agent's acts that were themselves responses to the partner are excluded or labelled. Stoytchev's robot babbled with no partner influence, so every motor command was exogenous. That is exactly the instrument condition.
- Condition the indexes on act type (per-channel, per-action-unit command). A partner may respond to the agent's smile but not its brow raise, and a pooled index would hide it. Correct the denominators for what the agent could see: the partner's face is not always visible or tracked.
- Two indexes, not one correlation. P(partner event in window | my act) high but P(my act before | partner event) low means a partner who answers me and also does much on its own: the high-but-imperfect contingency Watson calls social. Both near 1 means the partner is effectively part of me (a mirror, or my own render) or a perfect follower. That is the "self" signature, and the engine should treat it as such, not as a very responsive partner.
- Binary onsets plus a timing window are cheap, interpretable and CPU-trivial, and they suit the 52-blendshape face if onsets are defined per channel.

## License
Cambridge University Press journal article, all rights reserved; author-hosted copy. No code released (pseudocode in the paper).

## Runs on this Mac without a GPU?
Yes; three counters per feature and a 180-bin histogram.

## Verdict: adopt (lag-windowed two-index contingency with a self-delay learned from exogenous babbling and then frozen; per-act-type and visibility-corrected indexes)
One arm, colour markers, offline processing of recorded data; the "second robot" conditions are video composites, not a second physical agent. Mind the index-name reversal.
