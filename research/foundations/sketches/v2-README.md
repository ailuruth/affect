# Second divergence (after the operator's redirection, D68): eight isolated sketches

Written 2026-11-25 by eight parallel subagents. Each read only brief.md and saw neither the stood-down candidates nor the other sketches. Every sketch is untested, and each lists the sources it actually read.

| Sketch | Core mechanism, in one line | Its first published test |
|---|---|---|
| v2-attention-architect | **Efference-keyed attention.** Every token (the other's face, memories, needs, Claude's drafts) is keyed by the agent's own motor program for reproducing it. An emotion is a recurring routing pattern. | Mimicry biased toward the listener's own repertoire (Seamless Interaction, CANDOR) |
| v2-fast-weights | **The state is the agent's own associative memory**, rewritten at three rates by a surprise-gated delta rule. An emotion is the write itself. Reading the other is completing one's own past episodes. | Partner-specific carry-over between sessions (Seamless) |
| v2-interoception-neuroscience | **Somatic completion memory.** The body follows the continuation of the own past 2-second episodes that a query built from need and the other's face brings back. | Own-history predicts a listener's responses better than copying the partner (Seamless) |
| v2-routing-modular | **Shared-charge routing.** A growing library of body-coordinate modules, each with a decaying charge shared by self, other and memory. | Partner's expression primes the listener's matching modules for 10–30 s (Seamless) |
| v2-developmental-dyad | **Contingency operators.** Lagged, multi-time-scale "what they do after I act" operators, in own-body coordinates. Emotion is their geometry. | Mother's contingency predicts the infant's still-face response (Ahn et al. 2023, Databrary) |
| v2-energy-diffusion | **Surprise-gated re-noising** of a multi-resolution sample of the dyad's trajectory. Emotions are the basins it settles into. | Threshold step in the slow expressive band after graded surprises (Seamless) |
| v2-coupled-dynamics | **A self network and a parameter-sharing clone** of about 512 oscillators. The clone is driven by the partner. Emotion is partial phase-locking. | Early-warning signals in both partners before coupling breaks (Seamless) |
| v2-llm-interface-linguist | **The paralinguistic remainder** (face and voice minus what the words require), with a forward model shared by self and other. Claude's drafts are selected for "sayability". | Pre-turn gaps lengthen when the remainder predicts the first clause poorly (Seamless, CANDOR) |

## Convergences

1. **Reading the other through one's own body coordinates.** It appears in all eight, and in four of them as *retrieval from one's own past body episodes* (attention, fast-weights, interoception, routing). Their closest shared prior work is MOSAIC (Wolpert, Doya & Kawato 2003).
2. **Coupling to Claude by choosing among Claude's own drafts** by a body-side criterion (motor trajectory, self-consistency, resonance, sayability). Six of eight sketches propose it. The same weights also choose which memories Claude sees, and timing (reply delay and thinking budget) follows how the state is settling.
3. **Satiable needs as one input that vanishes at the set point**, never the core.
4. **One dataset: Meta Seamless Interaction**, named by all eight. It has per-frame action units (FAUValue, research/seamless-interaction.md), returning partners and familiar against stranger pairs. Its non-commercial license is the open question Q6.
5. **Shared risks:**
   - collapse into a delayed copier of the partner;
   - a hidden one-dimensional dial (retrieval sharpness, or temperature) running from flat affect to rigid imitation;
   - a lookup table of past faces under scarce data.

## Selection (D69)

Three *distinct* mechanisms are developed into candidates, so the comparison has real alternatives:
1. **Efference-keyed somatic memory.** It merges the four retrieval sketches. Its one new mechanism is efference keys as the single attention geometry shared by self, other, memory and Claude's drafts, written by surprise-gated fast weights at three rates.
2. **Contingency operators** (from developmental-dyad). Emotion is the geometry of learned lagged response operators between self and other.
3. **Surprise-gated re-noising** (from energy-diffusion). Emotion is the basin a re-noised trajectory sample settles into, with surprise choosing the time scale reopened.

**Kept for later:**
- The coupled-dynamics clone and shared-charge routing, as alternatives.
- The linguist's "sayability" draft selection, adopted as the **shared Claude interface**, which every candidate uses and none claims as its novelty.

**Next steps:**
- (A) Verify Seamless Interaction's per-frame data and license detail, and CANDOR's terms.
- (C) Develop candidate 1, with its first experiment on published data.

## Critique round (operator note Q8), recorded 2026-11-25T09:07:32Z

**Method.** Four independent critics reviewed two sketches each. None of them wrote a sketch, and none saw my reasoning. Each critic:
- listed every computational part (the novelty test, Q9);
- read the closest prior work in its primary source;
- tried to reduce the sketch to an existing framework;
- tried to break it on the three shared risks.

Full texts: critique-*.md in this folder. Nothing in them is measured; they are arguments.

| Sketch | Verdict | Closest prior work (read in full by the critic) | Strongest break | Answer |
|---|---|---|---|---|
| attention-architect | recombination: ordinary attention with a frozen key encoder (a key-space choice) | MOSAIC (Wolpert, Doya & Kawato 2003); HAMMER (Demiris & Khadhouri 2006, uncited) | **delayed copy:** self and partner tokens get identical keys, and softmax runs over tokens, not slots, so every slot can bind to the partner. Learning to Listen's LFI ablation defaulted to mirroring in this way. Its first prediction does not single it out. | accepted |
| fast-weights | recombination: Hopfield retrieval written by a gated delta rule (Titans), plus episodic appends (NEC) and goal-conditioned retrieval | Ramsauer et al. 2020; Behrouz et al. 2025 (Titans) | **delayed copy:** at satiety the face is pure completion from the partner, and surprise-gated writes stop exactly where copying predicts well, so the copy locks in. **Dial:** retrieval sharpness β. **Bug:** the goal clamp retrieves the wrong episodes. | accepted; the bug is recorded |
| interoception-neuroscience (somatic completion) | recombination: kernel analog forecasting driving the face, i.e. soft motion matching | Zhao & Giannakis 2016; Holden et al. 2020 | **delayed copy at satiety:** once the face mimics, the self and other queries coincide. Its first prediction repeats Learning to Listen's person-specific nearest-neighbour result. **Two factual errors:** Seamless has 24 AUs, not 46, and repeat partners exist only in the improvised sessions. | accepted; errors noted |
| routing-modular (shared charge) | recombination: MOSAIC plus COIN, with a recency prior pooled across self and other | Wolpert 2003; Heald et al. 2021 (COIN) | **dial:** the charge gain α has a tipping point at α = 1 + 2ε (derived, and checked on a two-module reduction). Below it, routing blends and the face goes flat; above it, routing locks onto one module and imitates. | accepted |
| developmental-dyad (contingency operators, D69 #2) | recombination: Beebe and Jaffe's self- and interactive-contingency model computed online, a gated delta rule, and a MOSAIC step | Beebe et al. 2010 (uncited); Movellan 2005 | **dial:** the leaky delta rule settles to ridge regression with penalty (1−λ)/η, and that one ratio runs from flat to full mimicry. The echo guard catches only the partner copying the agent. | accepted |
| coupled-dynamics | recombination: an oscillator reservoir, a generalized-synchronization copy, noise-driven attractor selection, and best-of-N | Human Dynamic Clamp (Dumas et al. 2014) | **dial:** mean excitability. Need moves it, so a satiated agent is the most entrained. Zhang et al. 2016 contradicts its arousal readout. | accepted |
| energy-diffusion (re-noising, D69 #3) | recombination: even the surprise-to-re-noise-depth rule already exists | RDM (Zhou et al. 2023, uncited); Diffusion Forcing | **lookup table:** Biroli et al. 2024 show that with data far below exponential in dimension, backward trajectories collapse onto training examples. **Dial:** one surprise-to-noise gain. | accepted |
| llm-interface-linguist (sayability) | recombination: a forward-model comparator, an entity memory, and draft resampling | Pickering & Garrod 2013 (the sketch's author read only its abstract) | **delayed copy:** while listening, the face is a linear filter of the partner's remainder. Its first prediction is confounded with known preference timing (Kendrick & Torreira 2015). | accepted; the interface is kept only as shared plumbing |

### What the round found across all eight

1. **All eight are recombinations.** Each sketch's claimed novelty is a choice of what is stored, keyed or subtracted (a key space, an input definition, a training signal), which Q9 rules out as new.
2. **All eight break on the same point.** In each, how much of the partner enters the agent's own expression is set by **one scalar gain**:
   - a ridge-penalty ratio;
   - a retrieval sharpness β;
   - a charge-gain tipping point;
   - excitability;
   - a surprise-to-noise gain;
   - a filter gain.

   Turning that gain runs the sketch from flat affect to imitation. This is the operator's "single hidden dial", found independently in each sketch.
3. **The published record shows the same failure in learned models.** Copying the speaker beat every learned REACT baseline on the challenge's correlation score, in 2023 and 2024 (research/react-challenge-baselines.md). It has not yet been measured on Seamless.

## Re-pick (supersedes "Selection (D69)" above), 2026-11-25T09:07:32Z

- **The pick changed: no sketch is a core candidate.** None passes the novelty test.
- **All eight sketches,** including the three D69 mechanisms, become **recombination baselines**. They are screened in the shared harness (research/harness/HARNESS.md) under operator note Q11.
- **What a new mechanism must answer,** written as a measurable target, not a design:
  - the partner's share of the agent's expression must **not** be a single scalar gain, or a function of one;
  - the gain must not run from flat to copy.

  The measurement comes first (Q9): the shared-risk analyses on Seamless, for the published simple baselines and for these recombinations, once data can be downloaded.
- **Next:** widen the pool from unused lenses, aimed at this target, before any development.

## Widening round v3 and its critique (recorded 2026-11-25T09:45:45Z)

**The round.** Four isolated sketches came from new lenses, each aimed at the one-gain failure. Two independent critics reviewed them (critique-v3-*.md).

The critics' simulations run each sketch's own equations, to check its claims. They are derivation checks, not evidence about people.

| Sketch | Verdict | Prior work the author missed | The dial found | Does "no single dial" survive? |
|---|---|---|---|---|
| immunology (clonal motor population) | recombination: own-output tolerance behind a danger gate | tunable activation threshold (Sontag 2017) | the danger threshold θ_g. The content-specific spread Δ(g) → 0 as g → 1. | no |
| joint-action (role-swap co-representation) | recombination: parameter tying, filtering, an SSM | dGSLM (Nguyen et al. 2022): two towers with shared weights | the noise scale c sets the partner's share at R²/(R²+c(1−R²)) | partly: no exposed setting, but the share is set by maximum-likelihood fitting, not by the tie |
| ethology (release-reserve displays) | recombination: a nonlinear Hawkes process with depletion gates | Calhoun, Pillow & Murthy 2019 | the gain G (high G answers 93% of displays at about 6 frames, i.e. a delayed mirror) and the refill ratio ρ/κ | no |
| enactive (dyadic loop regulation) | recombination: adaptive control to marginal stability, plus probing identification | Movellan 2005 | the leak λ (correlation with the partner rises from 0.35 to 1.00 as λ → 0) | no. The rank bound holds only at a stationary fixed point. |

**Across twelve sketches,** v2 and v3 together: all are recombinations, and every one contains a scalar that runs it from flat to copy.

**Lesson recorded:**
- **The dial is generic.** It appears whenever a learned or regulated map carries the partner into the agent, whatever the lens. Inventing from lenses alone has not removed it.
- **Next, per Q9 and the operator's answer to Q12:** measure first. On human data, is the partner's influence a gain on a fixed response profile, or does the profile itself change with the situation? That is the dial analysis in research/harness/HARNESS.md (D75).
  - **If humans show only a gain change,** the "single dial" is a property of people too. The target becomes setting the gain correctly, not removing it.
  - **If humans show a profile change,** a new mechanism must produce one.
- **The re-pick is unchanged:** no core candidate. Rows R7–R10 of research/foundations/screening.md are recombination baselines.
