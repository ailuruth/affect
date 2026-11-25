# v3 sketch: Role-Swap Co-Representation with Reciprocal Offers (RSCR)

Lens: joint action and improvisation (co-representation, the mirror game, complementary vs imitative coordination, turn-yielding, "yes-and" offers). Written in isolation from the other sketches, 2026-11-25.

Target: in every earlier design the partner's share of the agent's expression is set by one scalar gain, and copying the partner (B_Mime) beats the learned REACT models on FRCorr (0.38 vs 0.03 to 0.19; research/react-challenge-baselines.md). RSCR's aim is to take that share out of the agent's free parameters and tie it to quantities the partner itself shows.

## 1. Mechanism

**Idea in one line.** The agent does not keep "my state" and "an input from you". It keeps one model of the *pair*: two role slots run by one shared function, with argument order "self first, other second". The partner's slot is corrected by the partner's real face. The agent's own slot is driven by the same function plus the agent's own offers. Those offers are drawn from the same distribution the model fits to the *partner's* offers. As in improvisation, you accept the other's offer as part of the shared scene ("yes") and add your own at the rate offers are being made ("and").

**Observations, 30 Hz.** For person $P \in \{A, B\}$: $y^P_t \in \mathbb{R}^{p}$ is 24 FAU intensities (23 after dropping the duplicate column 12/19; the column order is unverified), plus prosody (f0, energy) at deployment. $c^P_t$ is context: own VAD bit, word-onset events, and turn-final word events from transcripts. A is the agent at deployment; on Seamless, A and B are the two humans.

**Own body.** One encoder and decoder pair, $E: \mathbb{R}^p \to \mathbb{R}^m$ and $D: \mathbb{R}^m \to \mathbb{R}^p$, with $D \circ E \approx \mathrm{id}$. Both people are coded by the same pair. At deployment $D$ is the agent's face/voice plant map, and the user is read only as $u^B_t = E(y^B_t)$: the motor command that would make *my* face look like yours (Principle 3).

**Scene state.** $S_t = (s^A_t, s^B_t)$, with $s^P \in \mathbb{R}^n$ a multi-timescale state (diagonal SSM blocks with time constants from 100 ms to minutes). Each slot also carries a static person code $\pi^P \in \mathbb{R}^q$ for individual style. The swap is $R(s^A, s^B) = (s^B, s^A)$, and it also swaps $u$, $c$ and $\pi$.

**Dynamics (one shared function, swap-equivariant).**
$$\bar s^A_{t+1} = f_\theta(s^A_t, s^B_t, c^A_t, c^B_t, \pi^A, \pi^B), \qquad \bar s^B_{t+1} = f_\theta(s^B_t, s^A_t, c^B_t, c^A_t, \pi^B, \pi^A)$$
so $F(RS) = R\,F(S)$ exactly.

**Offers (innovations) in motor coordinates.**
$$\nu^P_{t+1} = u^P_{t+1} - W\bar s^P_{t+1}, \qquad \nu^P \sim \mathcal{N}\big(0,\ \Sigma_\theta(s^P, s^{\bar P}, \pi^P, \pi^{\bar P})\big)$$
$\Sigma_\theta$ is one shared, state-conditional covariance network, also with "self first" argument order. $\bar P$ is the other person.

**Update: asymmetric only in what is observed.**
- Partner slot (yes, the uptake): $s^B_{t+1} = \bar s^B_{t+1} + K_\theta(S_t)\,\nu^B_{t+1}$, where $\nu^B$ is computed from the observed $E(y^B)$. This is filtering: the partner's offer is written into the shared scene.
- Own slot (and, the extension): $s^A_{t+1} = \bar s^A_{t+1} + K_\theta(RS_t)\,\nu^A_{t+1}$, with $\nu^A \sim \mathcal{N}(0, \Sigma_\theta(s^A, s^B, \pi^A, \pi^B))$ *sampled*. The agent's own offer comes from the same state-conditional offer law that fits human offers in its role.

**Readouts.** Own face: $y^A_{t+1} = D(W s^A_{t+1})$. Predicted partner: $\hat y^B_{t+1} = D(W \bar s^B_{t+1})$, i.e. "what my body would show in your place".

**Training on human dyads.** Both slots are observed. Maximize $\sum_t \log p(u^A_{t+1}, u^B_{t+1} \mid S_t)$ under the Gaussian offer law, plus a reconstruction loss on $E, D$. By the swap tie, every frame is two training examples of the same $f$, $\Sigma$ and $K$: once with A as self, once with B as self.

**What it computes.** A role-symmetric generative model of the pair, used in an asymmetric way: it filters the partner's slot and samples its own. In the isotypic coordinates $z_\pm = (s^A \pm s^B)/\sqrt2$:
- The **in-phase** (imitative) part is $z_+$, which the swap leaves unchanged.
- The **anti-phase** (complementary, role) part is $z_-$, which the swap negates.

Linear equivariant maps are block-diagonal in $(z_+, z_-)$. The two blocks are coupled only through nonlinear terms of $f$: products $z_- \odot z_-$ feed $z_+$, and $z_+ \odot z_-$ feeds $z_-$. Turn-holding enters $z_-$ through $c^A - c^B$. A turn exchange is approximately the map $z_- \to -z_-$ on the turn-locked part, with $z_+$ carried through.

## 2. Novelty test (honest)

| Part | Existing mechanism it is |
|---|---|
| Shared $E/D$, reading the other via own inverse | Autoencoder / inverse model; analysis by synthesis; Yoshida-Man inversion; MOSAIC paired forward-inverse models |
| Multi-timescale slot state | SSM / RNN |
| One $f$ with swapped argument order | Parameter sharing across agents. Same as SOM (below); also Z2-equivariant networks and a 2-node graph network |
| $z_\pm$ decomposition, in-phase/anti-phase | Isotypic decomposition (representation theory). Normal modes of symmetric coupled oscillators; the HKB in-phase/anti-phase structure |
| Partner-slot correction by innovation | Kalman / amortized filtering, predictive coding (RSSM posterior) |
| Own-slot sampled innovations | Stochastic generative rollout (RSSM prior sampling) |
| Offer law tied across roles | A consequence of the parameter sharing above |
| Claude couplings (sec. 4) | Retrieval (attention over episodes), scalar budget readouts |

**Closest prior work, read in full here.**
- **Friston & Frith 2015, "A duet for one"** (Consciousness and Cognition 36; read in full from the author's PDF, the appendix skimmed).
  - Two agents share one generative model: "this infinite regress dissolves if the two brains are formally similar".
  - Agency is not in the state. The paper says "the expectations are without agency" and assigns agency to "fluctuations in sensory attenuation (and proprioceptive precision)".
  - Turn-taking is scheduled by hand: "Each bird listened for two seconds (with a low proprioceptive precision…" and then sang.
  - The result is "identical synchrony at both the first and second hierarchical levels".
  - The paper leaves out learned turn-taking: "We have not dealt with this aspect of communication here."
  - RSCR's difference: Duet's shared state is RSCR's $z_+$ alone, and Duet's endpoint (identical synchrony) is failure (a) at the latent level. Duet's agency is a per-channel precision dial switched on a schedule, which is failure (b). RSCR puts agency in the state as the swap-odd component $z_-$, inferred from VAD and faces. It also ties the size of own offers to the partner's offers instead of to a precision value.
- **Raileanu, Denton, Szlam & Fergus 2018, "Modeling Others using Oneself" (SOM; arXiv 1802.09640; method and experiments read).**
  - The agent "uses its own policy to predict the other agent's actions".
  - The parameter tie is the same as RSCR's swap: "the parameters of fother are the same as the parameters of fself", and "the two networks differ in their relative placement of the inputs".
  - SOM infers a discrete goal by gradient steps and uses it as input to a reward-maximizing policy.
  - SOM does not have: continuous co-filtering of a shared state, a sampled own-innovation law tied to the other's observed innovations, or any account of expression.
- **Mirror-game line.**
  - Noy, Dekel & Alon 2011 (PNAS 108:20947). **Not read in full:** PMC blocks automated access and the PNAS full text was not retrievable, so its predictor-corrector model is not quoted or relied on here.
  - Hart, Noy, Feniger-Schaal, Mayo & Alon 2014 (PLoS ONE e87213; results read via the journal page). Co-confident (CC) segments converge to a shared shape. Quote: "in the mirror game players do not meet at an intermediate segment shape", which matches a joint mode ($z_+$ dynamics) rather than a weighted blend of the two players.
  - Leader-follower rounds show follower "jitter" at 2-3 Hz.
- **Not read here:** Sebanz, Knoblich & Prinz 2003 (social Simon co-representation) and Haken, Kelso & Bunz 1985. They are cited as background only.

**Verdict: recombination.** Every computational part is listed above as existing. Nearest whole: SOM's self-other parameter tying, applied to Duet-style co-filtering of a continuous shared state, with the swap-odd component carrying agency. What I could not find in the works read: using the tie to pin the agent's *own* sampled innovation law to the partner's observed one, so that expressiveness and partner share are identified by the partner's behaviour. I believe that is a new *use*, not a new computation; it is still parameter sharing. Record RSCR as a recombination baseline that targets the measured dial failure.

## 3. Answers to the shared risks

Define the partner's share as the response operator $\Gamma_{A\leftarrow B}(\tau; S) = \partial y^A_{t+\tau}/\partial y^B_t$. It is a 24x24 matrix for each lag and state. One-gain designs have $\Gamma = g\,M(\tau)$: a ray, so $g$ sweeps flat to copy.

**(b) No single dial.** Expand the response through the model:
$$\Gamma_{A\leftarrow B}(\tau;S) = J_D W\,\Big[\textstyle\prod \partial_{1} f\Big]\,\partial_{2} f\,K(S)\,J_E$$
- $\partial_1 f$ and $\partial_2 f$ are the Jacobians of $f$ in its self and other arguments.
- By equivariance, $\Gamma_{A\leftarrow B}(\tau;S) = \Gamma_{B\leftarrow A}(\tau;RS)$. The cross Jacobian is therefore fitted, from the same frames, to how B responds to A. In human dyads that response is neither zero nor a copy (Mirror P-FD 75.3 vs GT in L2L; ng-2022-learning-to-listen.md).

Proposition (informal; proof sketch only):
- **Copy needs two things.** It needs $\Sigma(s^A,\cdot) \to 0$ in the copied directions, so A adds nothing unpredictable from B's past. It also needs $\partial_2 f$ restricted to those directions to equal the identity map onto the readout. Under the tie, $\Sigma(s^A, s^B) = \Sigma$ evaluated as for a human in A's role. That is the fitted law of human offers, bounded below by the observed innovation variance of the partner's role. So copy is reachable only if the training humans themselves copied.
- **Flat needs both $\Sigma \to 0$ and $\partial_2 f \to 0$.** The second contradicts the fitted response of B to A.
- **The free scalars left do not move along the flat-to-copy axis.**
  - Filter gain: $K \to 0$ means responding to an imagined partner; large $K$ means responding to the observed one.
  - A post-hoc scale $c$ on $\Sigma$ moves from "deterministic self-dynamics responding to the partner" to "noisy". Neither end is a copy.
- **The share is content-, lag- and state-dependent.** Smile-to-smile in-phase lives in $z_+$; jaw is turn-locked in $z_-$, so the listener does not open their jaw when the speaker does; brow responses can be complementary. These are separate blocks of a nonlinear Jacobian, not one gain.

**(a) No delayed copy.** The agent's output contains $\nu^A$, which by construction is independent of B's past given $S$. Its variance is that of human offers. So the residual of the best predictor of $y^A$ from $y^B_{\le t}$ stays at the human level. This is falsifiable (P1, P5).

**(c) No lookup table.**
- There is no episodic store of faces: output is a parametric rollout, about $2\times10^5$ parameters.
- The swap tie halves the parameters and doubles the examples.
- An untied twin (two separate $f$) is the ablation predicted to overfit at about 60 min per person.
- Memorization is measured directly (P5).

## 4. Emotion as structure, reading through the body, and driving face, voice and Claude

**Structure, not labels.**
- $f$ is Z2-equivariant, so its attractor landscape is too. Every attractor is either swap-invariant (in $z_+$: shared states, for example shared amusement or mutual calm) or one of a swap-related pair. A pair $(a, Ra)$ is two complementary role configurations, for example one person distressed and the other soothing.
- Transitions are symmetry-breaking or symmetry-restoring bifurcations. A shared state splitting into two roles is a disagreement; two roles relaxing into $z_+$ is repair after comfort.
- Slow SSM blocks give mood (minutes) and, through $\pi$ and a slow pair state, relationship carry-over.
- Nothing is named. Valence or arousal, if wanted, are fitted *post hoc* as readouts for analysis only.
- Body variables (homeostasis) enter as part of $c^A$ (own) and as inferred components of $s^B$. They are one input to the state, not the core.

**Reading the other.** The user exists for the agent only as $E(y^B)$, in its own motor coordinates. Their inferred state is $s^B$, which is the agent's own dynamics run on the swapped scene. Inferring "what you feel" is literally "what I would be in your role" (simulation via the swap $R$).

**Face and voice.** $D(W s^A)$ gives AU targets and prosody (f0 contour offset, energy, rate) from the same slot, so face and voice share one source. Speaking is the turn state $c^A = 1$ inside $f$: jaw and lips get speech-locked input while the rest of the face keeps reading the scene.

**Claude (never sees numbers or words for the state).**
1. *Turn-yield timing.* The reply delay is the time until the model's predicted partner turn-end, from rolling $\bar s^B$ forward. Reply length comes from the swap image of the partner's recent turn lengths in the current state.
2. *Uptake cue selection.* Of the user's recent utterances, the ones whose offers moved $z_+$ most get carried into Claude's context window. The others age out. This is "what it took up".
3. *State-congruent recall.* Past episodes are retrieved by similarity of their stored slow-scene state to the current one, and their transcripts are offered as memories.
4. Claude sees a rendered image of its own face.

Word choice changes only through what is in context (2, 3, 4) and when Claude speaks (1).

## 5. Falsifiable test on Seamless Interaction (features only)

**Data.**
- V00 `movement/FAUValue` v1, `is_valid`, VAD and transcripts; no v4 mixing.
- Naturalistic: familiar and stranger pairs. Improvised: the 195 repeat actor pairs.
- Person-disjoint train/dev/test splits from the shared harness (Q11).
- Drop invalid frames. Keep one of columns 12/19. Report results with and without column 23.

**Task.** Generate A's 23 AU over 30 s windows (after a 4 s warm-up with A observed) given B's full streams, B's VAD and transcript events, and A's own VAD (speech timing given, as in L2L). 10 samples per window.

**Baselines, as published.** Median, Random (another person's clip), Nearest Neighbour (partner-feature match, retrieve that listener), Mirror, and Delayed Mirror (15 frames).

**Scores (representation-agnostic).**
- L2, FD and P-FD (L2L definitions) on AU sequences.
- Variation, and SI (k-means, k = 15).
- Per-AU PCC with the partner, against the human-human PCC.
- TLCC peak lag.
- FRDiv, FRVar, FRDvs.
- E3 windowed synchrony against segment-shuffle and data-sliding surrogates.
- FRCorr and FRDist are not computable (no appropriate-neighbour matrix). Do not report them.

**Pre-stated predictions; any one failing falsifies RSCR as targeted.**
- **P1 (no dial).** Estimate $\Gamma(\tau)$ (lagged 23x23 cross-regression, lags 0-2 s) for humans, for RSCR samples, and for the one-dial family $y = \alpha\,x^B_{t-\tau} + (1-\alpha)\,\mathrm{median}$, $\alpha \in [0,1]$.
  - RSCR's distance to human $\Gamma$ must be below $\min_\alpha$ of the family's, with a 95% bootstrap CI over test dyads.
  - Then sweep every scalar exposed post hoc (a scale on $K$ and a scale on $\Sigma$, each over 0.1 to 10). Mirror-PCC must stay inside the human 95% range, and the off-diagonal structure of $\Gamma$ must keep a rank correlation above 0.5 with human $\Gamma$.
  - Fails if any single sweep takes mirror-PCC from below the human range to above 0.5.
- **P2 (tie earns its keep).** Tied vs untied $f, \Sigma, K$ at equal parameters and budget. Tied has lower held-out NLL and FD at ≤60 min of training per person. Fails if untied is equal or better.
- **P3 (turn swap).** In the 3 s after VAD-derived turn exchanges:
  - RSCR's FD must beat all five baselines and the untied ablation.
  - In human data and in RSCR samples, the sum signal $y^A + y^B$ of the cheek/lip-corner AUs is continuous across the exchange (no change-point at p < .05 more often than in matched non-exchange windows), while the difference signal of jaw/lips-part flips sign.
- **P4 (carry-over).**
  - For repeat actor pairs, start interaction $k+1$ from the slow scene state at the end of interaction $k$ of the *same* pair. Prediction: lower NLL in its first 30 s than starting from another pair's final state, or from the population state.
  - Familiar vs stranger (naturalistic): the ratio of energy in $z_+$ to $z_-$ is higher in familiar sessions, with a person-level mixed model across the 160 V00 people who have both.
- **P5 (beats baselines, no copy, no lookup).**
  - RSCR beats Median, Random, NN, Mirror and Delayed Mirror on FD and P-FD (CIs over person-disjoint test dyads).
  - Variation and SI are within 20% of human.
  - The residual variance of RSCR's $y^A$ given B's past is at least 80% of the human value.
  - The distance from each generated 2 s segment to its nearest training segment is no smaller than for held-out human segments (NN baseline as the positive control for lookup).

**Budget (research/machine.md applies).** Pilot of about 300 V00 interactions, under 1 GB of features. Model about $2\times10^5$ parameters; training under 1 h on MPS/CPU; peak memory under 2 GB. All 5 baselines run in minutes. Blocked on the disk-floor question (Q11) like every download.

**Failure modes to report.**
- $\Sigma$ fitted on one partner's offers can make the agent mirror a flat user's flatness. That is reciprocal, possibly human-like, and also a harm channel: record it.
- If humans in a role do copy (for example during laughter), RSCR copies there too. That is intended, and it is local.
- The swap tie assumes the same plant for both. At deployment the agent's face rig differs, so only $E/D$ differ and $f$ stays tied.
