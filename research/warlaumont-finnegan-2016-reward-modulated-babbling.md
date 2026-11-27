# Warlaumont & Finnegan 2016, "Learning to produce syllabic speech sounds via reward-modulated neural plasticity" (PLOS ONE 11(1):e0145096, doi:10.1371/journal.pone.0145096, PMC4726623)

Source read: the full article on journals.plos.org (introduction, methods, results, discussion including predictions and limitations); Algorithms 1-2 and Table 1 are images and were read only through the text; supplementary sounds not used; code not run.

Read for search pass 9 (a computational model of output learning where the reward is a property of the learner's own sound, with a yoked control).

## Key claims
- **Model.** 1,000 Izhikevich spiking neurons (800 excitatory, 200 inhibitory) as a fixed random reservoir driven only by random input current (±6.5 pA); 200 reservoir output neurons project to 200 motor neurons (agonist and antagonist halves) whose smoothed difference drives jaw and lip (masseter, orbicularis oris) in Boersma's articulatory synthesizer (Praat), 900 ms per vocalization, 7,200 trials (2 h simulated).
- **Reward.** Auditory salience of the model's own sound (Coath and Denham's transient-detection model, summed |salience| after the first 150 ms); reward if salience exceeds an adaptive threshold (start 4.5, +0.1 whenever ≥ 30 % of the last 10 trials were rewarded). Reward adds 1 to a decaying dopamine level that multiplies eligibility traces (DA-modulated STDP, potentiation only, weights capped at 4 and renormalised to their mean).
- **Results** (200 motor neurons, m = 2): salience rises over time and exceeds yoked controls (time β = 0.42; reinforced vs yoked β = 1.2; interaction β = 0.43; all p < .001); syllable nuclei (an independent Praat detector) rise to about two per vocalization vs under one at baseline (interaction β = .31). Learned: higher baseline and wider range of jaw/lip activity; agonist/antagonist weight ratio 1.35 vs 1.00 yoked, T(4) = 18.11.
- **Yoked control.** Same reward times as a reinforced run, uncorrelated with the yoked model's own salience: no learning.
- **Interpretation.** The reward stands for either the infant's own interest in salient sounds or adults' greater responsiveness to them; the authors do not decide between them and predict a rising reward threshold in either case. Parameters (motor neuron count, muscle scale m) alone can produce syllabic output without learning, which the authors answer with an argument for starting from low activity.

## What it means for the engine
1. **The two readings of the reward fall on opposite sides of Proposition 1.** If salience is computed on the agent's own produced sound by the agent's own auditory model, the objective scores only the agent's own output: approval-closed (no partner path into it). If it stands for "the adult answers salient sounds", the same equations are Proposition 1(a): open. The model shows that a self-scored property can carry output learning as far as a partner's response does, with the same yoked failure.
2. **The yoked control fails here too.** Timing-matched reward uncorrelated with the learner's own output teaches nothing; the information is in the covariance of the gate with the learner's own output, which is exactly what Proposition 3 of new-core-search-9-synthesis.md isolates.
3. **The adaptive threshold is satiable only in name.** It rises with success (heterostatic, pass 7's typology): the drive never settles. A body-variable version for the engine would need a floor and satiety (Principle 6), not a ratchet.
4. **A self-scored output objective is still a scalar drive on output** and would need to be checked against Q18 like any learned expression parameter; its target is fixed by the innate auditory model, not by the partner.

## Verdict
- **background (self-scored output reward vs partner-scored reward in one model; yoked failure).** One motor degree of freedom; no perception of others; salience model trained on adult speech.
