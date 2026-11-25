# Kelso, de Guzman, Reveley & Tognoli 2009, "Virtual Partner Interaction (VPI): Exploring novel behaviors via coordination dynamics" (PLoS ONE 4(6):e5749, doi 10.1371/journal.pone.0005749); with Tognoli & Kelso 2014, "The metastable brain" (Neuron 81(1):35-48, doi 10.1016/j.neuron.2013.12.022)

Source read, 2026-11-25:
- **VPI.**
  - Full text on journals.plos.org and PMC2685001, through a fetch tool (methods, results, discussion).
  - The equations are images in both copies. The two model equations (e003, e004) were read from the PLoS equation images. Table 1 is partly unreadable: only A = 0.12 and B = 0.025 were extracted.
  - The last ~4k characters of the PMC page (end of the references) were not read.
- **Tognoli & Kelso 2014.**
  - NIH author manuscript, PMC3997258, characters 0-100k of 160k (Introduction, Parts I and II, part of the Conclusions).
- **Already in this project, not re-read.** Dumas et al. 2014 (human dynamic clamp) and Zhang et al. 2016 (emotional responses to a virtual partner) were read by the critic in research/foundations/sketches/critique-coupled-dynamics.md. Their facts are cited from there.
- **Not read.** Schöner & Kelso 1988, on intention as a term in the relative-phase equation, is not read here.

## Claims
- VPI: "Inspired by the dynamic clamp of cellular neuroscience, this paper introduces VPI". A human moves with an animated hand driven in real time by an HKB oscillator, which is in turn driven by the human's finger.
- The partner's coordination preference is set by the sign of a coupling parameter μ, not its size. μ is used "to control for the virtual partner's preference for in-phase or anti-phase coordination with the subject".
- The experiment pitted intentions: humans were told to stay in-phase, and the VP used "reversed coupling (μ<0) so that the virtual partner was parameterized to couple most stably anti-phase with the human subject creating, as it were, a 'conflict of intentions'". The outcome is predicted to depend "on neither the virtual partner nor the human subject alone".
- The VP "can induce the human toward its preferred coordination behavior as well as being influenced by him/her". The switch to anti-phase was "more likely" "induced on the human subject by the virtual partner".
- Humans found unplanned strategies: "There is no indication that these behaviors were planned or decided in advance."
- Some subjects said in exit interviews that the machine was "messing" with them, read by the authors as attribution of agency. These were informal interviews.
- Tognoli & Kelso 2014:
  - "metastability corresponds to a régime devoid of stable coordination states".
  - Dwell length grows with symmetry and coupling strength.
  - Metastable dynamics can reorganize "even in the absence of inputs or noise".
  - A "locked" brain "is maladaptive".
  - They cite VPI as an interpersonal case showing locked, transient and unlocked behaviour, "depending on coupling reciprocity and movement frequency".

## Evidence
- **Participants and design.** n = 10 right-handed participants (6 female, 4 male), aged 18-35.
  - Two 200-s scaling trials, 1.5 to 3.3 Hz in 0.2 Hz steps every 20 s, set each subject's low and high frequency.
  - 32 trials of 100 s: 16 bidirectional, 8 human-to-VP (display off), 8 VP-to-human (coupling term zero, so the VP acts as a metronome).
  - Finger angle sampled at 1 kHz, downsampled to 100 Hz, low-passed at 10 Hz.
  - Relative phase by Hilbert transform.
- **Trial classes,** by synchronization index (SI) and dwell time τ, with a dwell defined as more than 2 cycles within 0.17 rad:
  - stable: SI > 0.8 and τ ≥ 90%;
  - switching: 0.3 ≤ SI ≤ 0.8 and τ ≥ 25%;
  - unstable: SI < 0.3.
- **Relative-phase distributions:**
  - Human-to-VP: peaks near anti-phase (~2.5 rad at low frequency, near π at high frequency).
  - VP-to-human: peaks at in-phase.
  - Bidirectional: bimodal, more in-phase than anti-phase, with anti-phase growing at high frequency.
- **Bidirectional trials (Table 2):**
  | frequency | stable | switching | unstable |
  |---|---|---|---|
  | low | 42.5% | 37.5% | 20% |
  | high | 2.5% | 32.5% | 65% |
- **No inferential statistics** are reported. It is a proof of concept.
- **Simulations:**
  - A reverse-coupled HKB pair settled at ±π/2.
  - The VP's amplitude decayed under sustained in-phase coordination.
  - Human strategies kept the VP oscillating: brief switches to anti-phase, keeping their own amplitude in a range, and shifting the center of oscillation toward flexion.
  - Sine-input simulations with an origin shift P (0, −0.7, −1.0) and an amplitude Q (4, 2, 1) delayed the VP's amplitude decline. At P = −1.0, Q = 1 the amplitude was kept for the whole run.
- **From the critic's reading of the follow-ups:**
  - Dumas et al. 2014 show "phase wrapping and metastability (intermittent dwells near stable in- and antiphase states)". VP coupling and intention are fixed by the experimenter; only frequency adapts.
  - Zhang et al. 2016 found human "Arousal was higher when coordination was stable" (skin potential).

## Formal models
- **VP oscillator** (VPI eq. e003, HKB component):
  ẍ + (αx² + βẋ² − γ)ẋ + ω²x = (A + B(x − y)²)(ẋ − ẏ)
  - x is the VP's position and y the partner's.
  - The second component is obtained by swapping x↔y.
- **Modified coupling used for the VP** (e004):
  K = (A + B(x − μy)²)(ẋ − μẏ)
  - A = 0.12, B = 0.025.
  - μ scales the human input and sets the preferred mode; μ < 0 makes anti-phase the VP's stable mode.
- **Relative-phase reduction** (Tognoli & Kelso 2014, eq. 1):
  φ̇ = δω − a sin φ − 2b sin 2φ + Qξ
  - φ = φ₁ − φ₂;
  - δω = ω₁ − ω₂, the intrinsic-frequency difference (symmetry breaking);
  - a, b are coupling parameters;
  - Qξ is noise, "not essential for metastable behavior".
  - With δω ≠ 0 and weak coupling, fixed points vanish and φ dwells near the ghosts of 0 and π, then escapes.
- **Spatially extended ring** (Tognoli & Kelso 2014, eq. 2):
  ∂φ(x,t)/∂t = ω − ∫ G(x − x′) sin[φ(x,t) − φ(x′,t) + α] dx′

## What it implies for a dyadic affective core
- **Coupling has a sign and a target mode, not just a size.** In HKB the partner's influence is (A + B(x − μy)²)(ẋ − μẏ).
  - The sign of μ chooses which pattern (in-phase, imitation-like, or anti-phase, complementary) is the attractor.
  - The ratio b/a sets whether both patterns exist.
  - δω sets whether any pattern is locked at all.
  - One gain on (partner − self) has only the in-phase attractor. It cannot express "my preferred relation to you is opposition", and it cannot hold two coexisting patterns with switching between them.
- **Intentions on both sides shape the joint outcome.** In VPI the observed pattern (bimodal, switching, ±π/2 in simulation) belonged to neither party alone. Instruction (human) and parameterization (VP) acted as separate terms.
  - A dyadic affective core needs a term for its own preferred relation to the partner, separate from the coupling strength.
- **Metastability, not locking, is the target regime.**
  - Tognoli & Kelso argue that being locked is maladaptive, and the useful regime is dwell-and-escape set by symmetry breaking (δω) against coupling.
  - In the project's terms, the flat-to-copy dial is the a-axis of this model. An agent tuned to metastability needs intrinsic detuning of its own dynamics as a second, independent axis.
- **Partner influence also shows in the human's choice of strategy.** People found amplitude and offset changes that kept the VP alive. This is coordination through manipulating the partner's coupling, which a fixed gain cannot represent.
- **Arousal reading.** Per Zhang 2016 (via the critic), human arousal was higher in stable coordination. That matters for any readout tying arousal to instability.
- **Not shown:**
  - Nothing about faces, voices or affect, beyond Zhang 2016.
  - The VP's μ was fixed by the experimenter, so the work shows that sign-structured coupling matters, not how it would be learned or chosen.
  - n = 10, no statistics.
  - Tognoli & Kelso give no interpersonal numbers.

## Verdict: adopt (formal vocabulary), watch (as precedent)
- Adopt HKB's decomposition of coupling (sign or preferred mode μ, harmonic ratio b/a, detuning δω, noise Q) as the minimum vocabulary against which a "single gain" claim is tested. Each of the four, ablated, changes a different behaviour (Principle 5).
- VPI itself is a one-dimensional finger task with hand-set intentions and no learning. It shows that role and intention enter the coupling. It does not show how an affective agent should get them.
