# Rolnick, Ahuja, Schwarz, Lillicrap & Wayne 2019, "Experience Replay for Continual Learning" (CLEAR; NeurIPS 2019; arXiv 1811.11682)

Source read: the arXiv v2 PDF (26 Nov 2019, the NeurIPS camera-ready), read in full on 2026-11-25. That covers sections 1-5, Appendix A (distributed setup, network, buffers, training weights, evaluation) and Appendix B (cumulative replots; captions only, since the plots are images). The tables in Figures 3 and 7 were read with a layout-preserving text extraction. Not read: the cited IMPALA/V-trace paper (Espeholt et al. 2018), Progress & Compress (Schwarz et al. 2018) or Isele & Cosgun 2018 on reservoir buffers. No official code was checked.

## Claims
- Replay, "largely overlooked as a solution to forgetting in deep reinforcement learning", is enough to almost eliminate catastrophic forgetting in multi-task RL. It does so "despite being significantly less complicated and not requiring any knowledge of the individual tasks being learned".
- The split is: "on-policy learning from novel experiences (for plasticity) and off-policy learning from replay experiences (for stability)", plus "behavioral cloning between the current policy and its past self".
- "Interference" and "catastrophic forgetting" are separate phenomena. In their DMLab set interference is negligible, so the damage comes from sequential overwriting: "while interference may happen, forgetting is ubiquitous".
- A small buffer suffices. Reservoir-sampled buffers far smaller than total experience work almost as well.
- Pure replay keeps old tasks but slows the learning of new ones. Fresh on-policy data is needed for plasticity.
- Limits named by the authors:
  - Methods may "live on a Pareto frontier": when storage is prohibitive, parameter-protection methods may suit better.
  - When "the action space of a task changed during training, fitting to the old policy's action distribution ... could have a deleterious effect". They write that "we may need to develop algorithms that selectively forget skills as well as protecting them".

## Evidence (numbers)
- DMLab, three tasks (explore_object_locations_small, rooms_collect_good_objects, rooms_keys_doors_puzzle), trained cyclically. The metric is final cumulative reward (1/t)Σ_{s<t} r_s, an area under the curve. Three runs each, mean ± SD (Fig. 3):

| Condition | explore | collect | keys |
|---|---|---|---|
| Separate | 29.24 | 8.79 | 19.91 |
| Simultaneous | 32.35 | 8.81 | 20.56 |
| Sequential, no CLEAR | 17.99 | 5.01 | 10.87 |
| CLEAR 50-50 | 31.40 | 8.00 | 18.13 |
| CLEAR without behavioural cloning | 28.66 | 7.79 | 16.63 |
| CLEAR 75-25 new-replay | 30.28 | 7.83 | 17.86 |
| CLEAR 100% replay | 31.09 | 7.48 | 13.39 |
| Buffer 5M | 30.33 | 8.00 | 18.07 |
| Buffer 50M | 30.82 | 7.99 | 18.21 |

  Separate ≈ simultaneous, so interference is minimal. Sequential training roughly halves cumulative reward. CLEAR recovers most of the loss.
- Buffer size. 900M total frames, compared at buffer capacities of 450M, 50M and 5M. The 5M buffer stores about 1 in 200 experiences and shows "some catastrophic forgetting", attributed to overfitting the few stored samples. The default cap is half the frames trained on.
- Probe task (natlab_varying_map_randomized). It is inserted at different points in the cycle. Under normal CLEAR its final performance is independent of when it appears. Under 100% replay it "deteriorates markedly as it appears later", because it makes up a shrinking share of the buffer.
- Atari, the same 6-game sequence and network as Progress & Compress, with CLEAR at 75-25 new-replay. Final cumulative reward (Fig. 7):

| Method | space_invaders | krull | beam_rider | hero | star_gunner | ms_pacman |
|---|---|---|---|---|---|---|
| Baseline | 346.47 | 5512.36 | 952.72 | 2737.32 | 1065.20 | 753.83 |
| CLEAR | 426.72 | 8845.12 | 585.05 | 8106.22 | 991.74 | 1222.82 |
| EWC | 549.22 | 5352.92 | 432.78 | 4499.35 | 704.20 | 639.75 |
| P&C | 455.34 | 7025.40 | 743.38 | 3433.10 | 1261.86 | 924.52 |

  CLEAR is best on 3 of 6 games (krull, hero, ms_pacman). EWC is best on space_invaders, P&C on star_gunner, and the no-protection baseline on beam_rider. The baseline "rapidly re-acquires" games after forgetting. The authors' summary, "comparable to or better than P&C, and significantly better than EWC", is an aggregate, and no statistical test is reported. CLEAR needs no task boundaries. EWC and P&C were given them.

## Mechanism
- Actor-critic (IMPALA) with V-trace off-policy correction, used for both actor lag and replay staleness. Notation: π_θ is the current policy, μ the behaviour policy that generated the stored data, and h_s the network's hidden state.
  - V-trace target: v_s = V(h_s) + Σ_{t=s}^{s+n−1} γ^{t−s} (Π_{i=s}^{t−1} c_i) δ_t V, with δ_t V = ρ_t (r_t + γV(h_{t+1}) − V(h_t)).
  - Truncated importance weights: c_i = min(c̄, π_θ(a_i|h_i)/μ(a_i|h_i)) and ρ_t = min(ρ̄, π_θ(a_t|h_t)/μ(a_t|h_t)).
  - Losses on both new and replayed data:
    - L_pg = −ρ_s log π_θ(a_s|h_s)(r_s + γv_{s+1} − V_θ(h_s)), weight 1.
    - L_value = (V_θ(h_s) − v_s)², weight 0.5.
    - L_entropy = Σ_a π_θ(a|h_s) log π_θ(a|h_s), weight ≈ 0.005.
  - Extra losses on replayed data only, the cloning to the past self:
    - L_policy-cloning = Σ_a μ(a|h_s) log(μ(a|h_s)/π_θ(a|h_s)) = KL[μ‖π_θ], weight 0.01. The forward KL keeps π_θ nonzero wherever the past policy was.
    - L_value-cloning = ‖V_θ(h_s) − V_replay(h_s)‖², weight 0.005.
- What the buffer stores: the observation, the network's output logits, the value output, the action and the reward. These are the agent's own past outputs, saved alongside the experience. The hidden state is not listed as stored. Unrolls are stored whole or not at all.
- Mix. Each learner batch element is a pair (new unroll, replay unroll), and the new/replay ratio picks one of the pair. The default is 50-50. Atari used 75-25. Performance "does not appear to be very sensitive to this ratio".
- Reservoir sampling. Each unroll gets u ∼ U(0,1). A rising threshold keeps exactly the capacity's worth of unrolls above it, so the buffer is always a uniform random sample of all past unrolls. No task identity or priority is used anywhere.
- The authors' intuition, not proven: cloning keeps π_θ near μ, which lowers the variance of the importance weights. As the buffer fills with better policies, cloning "increasingly acts to regularize the network towards improved policies".

## License
arXiv non-exclusive distribution licence (arxiv.org/licenses/nonexclusive-distrib/1.0). No code was released that we know of. The losses and buffer are specified exactly enough to reimplement.

## Runs on this Mac without a GPU?
The paper's distributed IMPALA set-up, with many CPU actors and one learner on DMLab or Atari at 10⁸-10⁹ frames, does not. The mechanism does, and this is our judgment. A single learner with V-trace, a reservoir buffer and two extra loss terms is trivial at our scale. Our storage estimate: 3 h/day at 30 Hz is about 3.2×10⁵ frames/day; at ~100 float16 features per frame (blendshapes, prosody, body variables, logits, value), six months is roughly 10-15 GB. All of it could be kept on disk, so reservoir subsampling is optional. The design question is weighting, not capacity.

## Implications for the engine (our inferences)
- **Replay is the main defence against forgetting, and it needs no task boundaries.** That fits a life with no labelled tasks better than EWC or SI. It also matches Principle 7: the buffer holds feature streams. A buffer of ~10⁷ feature frames is cheap.
- **The stored outputs are already a state tag, but of the wrong kind for S6.** CLEAR's buffer keeps the agent's past logits and value alongside each experience, and cloning pulls the present self toward them. For the engine, the natural tag is the agent's internal state at encoding time: body variables, need levels, arousal, the latent, and the inferred partner context. CLEAR shows what such a tag can do mechanically. Stored past outputs give "be who you were then in that situation", which is how a temperament would resist drift. Two cautions follow:
  - (a) Learned outputs and latents drift across model upgrades, which S6 must survive. A tag that has to survive upgrades should be written in innate, fixed coordinates: the body variables (Principle 2). A tag written in the conceptual layer's latent would not survive.
  - (b) The authors warn that cloning is harmful when the action space changes. S4 changes the action space on purpose, replacing the action-unit face with a muscle model. Cloning stored action logits across that swap is wrong. Cloning would have to target outcomes in body or feature space (what the face looked like, how the body variables moved), not the old action distribution.
- **Uniform reservoir replay is the right null model for the S6 ablation, and it is strong.** Uniform replay alone recovered most of the lost cumulative reward here. If the engine's claim is "removing state tagging removes operator-specificity", the ablation must swap tag-weighted sampling for uniform reservoir sampling at equal buffer size, equal new/replay ratio and equal replay compute. The expected effect is not on retention, which uniform replay already handles. It is on specificity: which context-conditioned mapping each replayed sample trains, and how much salient states weigh. If tags only re-weight sampling, uniform replay may match them on everything except rare high-salience episodes. Design the S6 metric around those episodes.
- **Age bias from cloning to every past self.** A uniform reservoir keeps early, immature experiences in proportion forever, and cloning anchors to the policies stored with them. That is Huszár's double-counting bias in replay form: it favours the early self. For a developing infant-like agent, either (i) recompute or relabel μ and V_replay with a recent network during sleep, or (ii) down-weight cloning by age while keeping the off-policy RL term, which corrects with current π_θ. That choice should follow from the objective, not be tuned. The paper does not test either.
- **What, when, and with what weight.**
  - *What*: whole unrolls, so temporal context and the timing of exchanges are preserved, plus the stored past outputs and the internal-state tag.
  - *When*: CLEAR mixes within each batch, online. For us, the day can keep a 50-50 mix of today's on-policy data with replay to stay plastic. The night can run 100% replay, which CLEAR shows still maintains and even slightly improves old tasks (performance "increases throughout ... from replay alone").
  - *Weighting*: the probe result is a warning. If the relationship forms only from replay, it forms more slowly as the buffer grows and the operator's newest patterns become a vanishing share. Fresh data must keep a fixed share regardless of buffer age.
- **Fast/slow.** CLEAR has one network and one buffer: the buffer is the fast episodic store and the network the slow store, with nothing like a hippocampal index or generative replay. Combining it with a slow-parameter anchor (P&C or online EWC) is "quite orthogonal" per the authors. That gives a two-mechanism design: replay for content, plus a precision anchor between replays for slow temperament parameters.
- **Interference vs. forgetting, applied to partners.** The finding that separate ≈ simultaneous training (no interference) while sequential training collapses means that if a second person appears weeks later, the risk to the operator relationship is forgetting through disuse, not incompatibility. Interleaved replay of operator episodes during that period is the direct antidote, and a partner-context tag decides which mapping each replayed episode trains.

## Verdict: adopt the mechanism; watch the uniform reservoir and the cloning targets
- Adopt: the replay buffer of feature-stream unrolls, the fixed new/replay mix during waking with replay-only offline phases, off-policy correction (V-trace or an equivalent) when the stored behaviour differs from the current policy, and cloning to stored past outputs as the drift-resisting term. Each is a constraint on the objective's data distribution, not a module. Under Principle 10, the core's objective must say what distribution the replay approximates; CLEAR implicitly picks "all past experience, uniformly".
- Watch: uniform reservoir sampling is the ablation baseline for state tagging, not the design. Behavioural cloning targets must be stated in coordinates that survive S4 and S6 upgrades. CLEAR gives no account of what the tag should be or of selective forgetting, which the authors themselves flag as needed.
