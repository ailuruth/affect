# In the Body's Eye: the computational anatomy of interoceptive inference (Allen, Levy, Parr & Friston)

Citation: M. Allen, A. Levy, T. Parr, K. J. Friston. "In the Body's Eye: The computational anatomy of interoceptive inference." *PLoS Computational Biology* 18(9):e1010490, 2022. doi:10.1371/journal.pcbi.1010490.

Source read: the PLOS printable PDF, text-extracted. Read in full: abstract, author summary, Introduction, Methods, Results, Discussion, Limitations, figure captions. **Not read:** the code (SPM12 DEM demo; GitHub repository).

## The model
- **A two-modality POMDP (Markov decision process).** Hidden states: an interoceptive factor (cardiac phase: two diastolic states and one systolic state) and an exteroceptive factor (arousing vs non-arousing picture). Two policies: relaxed and aroused. Precisions: visual likelihood α, cardiac likelihood β, transition precision ("inverse volatility") z = 0.9.
- **The single coupling.** "The two domains of perception are coupled by – and only by – sensory attenuation: i.e., attenuation of sensory precision in the visual domain during (inferred) systole." In systole the visual likelihood is made uninformative ("all outcomes were equally plausible"); in diastole it is precise.
- **Policies act on the body clock.** Relaxed: two diastolic phases and one systolic. Aroused: the first diastolic state jumps straight to systole, so arousal means more time in systole, hence less precise vision.
- **Preferences (C).** The agent expects systole together with an arousing picture and diastole with a non-arousing one. This creates the trade-off the authors stress: stay relaxed to keep sampling precisely, or accelerate the heart and lose precision once something arousing is inferred.
- **Generative model = generative process** ("in the spirit of the good regulator theorem").

## Results (simulations only)
- **Startle-like response.** 60 simulated subjects; 14 baseline "flower" trials, a "spider" on trial 15: immediate cardio-acceleration that habituates, and the posterior of a spider on the next trial jumps from ~25 % to ~65 %.
- **Threat expectation oscillates with the beat.** During baseline the expected spider probability rises ~5 % on each systole: attenuated precision raises uncertainty, and with a prior over two states, uncertainty moves mass toward the less expected state. The authors offer this as a mechanism for fear stimuli being potentiated in systole.
- **Interoceptive lesion (β = 0.5).** Blunted cardiac acceleration and blunted belief update after the spider; baseline threat expectation 5–10 % higher ("psychosomatic hallucination").
- **Uncertainty maps** over α, β ∈ [0.5, 1]: exteroceptive entropy is set mostly by α, modulated by β; it oscillates by cardiac phase. (The text says precision "drops effectively to null" "on each diastole", which contradicts the model description and figure; it reads as a slip for systole.)
- **Synthetic HRV "phenotypes"** (1000 trials; 350 ms per state): healthy 63.5 BPM, LF/HF 0.52; precise viscera 59.5 BPM, peak 0.25 Hz; precise arousal priors 84 BPM, peaks at 0.04 and 0.34 Hz.
- **Limits stated by the authors.** Proof of principle; no fit to data; "substantive further work will be needed to develop an observation model of empirical heart-brain interactions".

## The mathematical object
A **likelihood whose precision is a function of the agent's own (inferred) body state**: A_ext(s_intero), with the body state's dynamics selected by the agent's own policy. Perception of the world is thus clocked by the body, and the agent's own arousal is paid for in sampling precision. Affect-like expectations arise from that coupling, not from a named variable.

## What it means for the design
1. **The body as the sampling clock of the other.** Read with Al et al. 2020: the other is perceived only through windows the agent's own body opens. In a dyad, the partner's face would be sampled with a precision set by the agent's own phase and policy, so the partner can never set when the agent looks closely. This is an architectural fact, not a gain.
2. **But a precision gate is still a gain on the input**, and in this model it is binary and hand-set. As a coupling route it is the apical-amplification / liquid-time-constant pattern already in the index (phillips-2016-apical-amplification-arousal.md; hasani-2021-liquid-time-constant.md): modulation without authorship.
3. **Hand-named states.** "Aroused/relaxed", "spider/flower" and the preference table are labels and hand-set structure, against Principles 1–2. Only the structural idea transfers.

## Verdict
- **watch (structural idea only).** It is active inference with a state-dependent likelihood precision; the brief excludes adopting it as is, and no data are fitted.
