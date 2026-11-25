# Watson 1997, "Contingency and its two indices within conditional probability analysis" (The Behavior Analyst 20(2):129-140, doi:10.1007/BF03392770, PMC2733560)

Source read: the full article, all 12 pages, from the PMC PDF via its Wayback Machine snapshot of 2022-06-18 (PMC itself served a bot check). This is Watson's own short statement of the contingency analysis he developed in Watson 1979 (in Thoman, ed., Origins of the Infant's Social Responsiveness), 1985 (in Field & Fox, eds., Social Perception in Infants, pp. 157-176) and 1994 ("Detection of self: the perfect algorithm", in Parker, Mitchell & Boccia, eds., pp. 131-148). Those three chapters were NOT read: no free copy exists. One sentence of the 1994 chapter is quoted below from Stoytchev 2011 (Robotica, "Self-detection in robots", author PDF, read for its Watson passages only).

## Claims
- Four ways a device could detect that its outputs affect its inputs (pp. 130-133):
  - Contiguity: CD = f(time_M − time_K), the delay between kick K and mobile movement M. Blind to both kinds of dissociation; gives superstition when the stimulus is frequent by chance; fails with delays.
  - Correlation: CD = f(r_KM) of amounts over time windows; can find a fixed delay (correlate behaviour now with stimulus 10 s later), but sums both kinds of dissociation into one number.
  - Conditional probability: two indices, kept separate. Stated by Watson as the most powerful option.
  - Logical implication (Bower 1989): judges from the four cells K/not-K × M/not-M; no notion of chance, so "vulnerable to errors of detection in a noisy, probabilistic world due to imprecise control by multiple controllers".
- The two indices (Figure 3, pp. 132, 136):
  - Forward time, sufficiency index: p(M | K t), "the probability of mobile movement (M) in a specified time span (t) following a kick (K)".
  - Backward time, necessity index: p(K | t M), "the probability of a kick (K) in a specified time span (t) preceding a mobile movement (M)".
  - Each is judged against the unconditional probability of its target event, not against zero (p. 134). He rejects ΔP = p(A|B) − p(A|not B) because it needs counts of non-events, while granting it has "the same implications" under its assumptions (footnote 2).
  - The time base must be explicit: "time-based conditional probability analysis must make an explicit reference to its time base if it is to develop an appropriate evaluation of statistical reliability" (p. 134).
- The two indices are nearly independent. Worked examples (p. 136): an experimenter pulls the ribbon after a random half of kicks and never otherwise: forward .5, backward 1.0. The experimenter pulls after every kick and also about as often at random: forward 1.0, backward .5. Psychology manipulated almost only the forward index; schedules that lower the backward index (free, response-independent rewards) also impair learning (Maier, Seligman & Solomon 1969; Seligman 1975; Watson 1977).
- Why the backward index matters socially (p. 134): "in a world in which others are capable of controlling the same outcomes as the individual in question, coincidental conjunction of the individual's behavior and stimuli produced by others seems to be an inevitable likelihood."
- Computational asymmetry (pp. 137-138): the two are "mathematically equivalent" but "not computationally equivalent when instantiated in a causal device that is by nature constrained by the unidirectional vector of time".
- Developmental proposal (untested): contiguity → correlation → forward conditional probability → backward conditional probability → logical implication, each added to, not replacing, the earlier ones. From his own infant work (1979, 1985), infants show sensitivity to both kinds of dissociation by 4-6 months.
- From the 1994 chapter, as quoted by Stoytchev 2011: "imperfect contingency between efferent and afferent activity implies out-of-body sources of stimulation, perfect contingency implies in-body sources, and noncontingent stimuli are ambiguous" (Watson 1994, p. 134). Stoytchev also reports Watson's suggestion of an imprinting period in which the efferent-afferent delay is learned; not verified.

## Evidence with numbers
- Simulation (pp. 137-138): an Elman recurrent network (1 response input, 3 hidden units fed back as 3 context inputs, 1 output) on a 1,000-s series with a response every other second on average and a stimulus exactly 2 s after each response. Trained on the first 100 s by backpropagation: about 50 epochs to perfect prediction (10 random restarts), and near-perfect generalisation on the remaining 900 s. Given the backward task (predict the response from the stimulus series), the same architecture "failed completely", because the teacher signal (a response now) is unrelated to stimuli in memory: the stimulus that the response causes has not happened yet. Fixing it needs a device that searches memory for its teacher signal.
- Cited human data: variation in the forward index affects infants (Diethelm 1991) and adults (Lewicka 1988) more than variation in the backward index. Not read.
- No new infant data in this paper.

## Mechanism
For events on a common clock with window t:
- sufficiency S = P(stimulus occurs in (τ, τ + t] | response at τ), compared with P(stimulus in any window of length t);
- necessity N = P(response occurred in [τ − t, τ) | stimulus at τ), compared with P(response in any window of length t);
- maximal, "perfect" contingency (self): S = N = 1 at a fixed delay. Imperfect but high (a responsive other): both well above base rate, at least one below 1. The maximising rule (narrow the response class when N > S, widen it when S > N) is in Gergely & Watson 1996, not here.

## What it implies for an engine that learns a partner model and its own self–other face map from contingencies in live interaction
- The two indices are cheap and inspectable and they split "the partner answers me" (S) from "only I move the partner" (N). In an engine they are trivial to compute because the engine keeps exact logs of its own acts; Watson's network failure on the backward index is a fact about forward-predicting recurrent nets, not about an engine with an event buffer. Keep explicit event logs and compute both directions.
- The backward index does NOT protect against the confound in the critique. N falls when the partner's acts have other causes; it does not ask whether the agent's act was itself caused by the partner. If the agent follows the partner (acts at τ because the partner acted at τ − δ) and the partner's acts come in bursts, the partner tends to act again shortly after the agent's act, so S rises above base rate with no causal path from agent to partner. Watson's examples all assume the response is generated independently of the stimulus (an infant kicking, an experimenter pulling a ribbon). The guard he does give is comparison with the unconditional base rate; that removes chance coincidence but not following plus autocorrelation. The engine needs, in addition:
  - a baseline conditioned on the partner's own recent history, not the unconditional rate (compare P(partner act in (τ, τ+t] | agent act at τ, partner history) with P(partner act | partner history)), which is what time-series "self- vs interactive contingency" models do (see beebe-2016-self-interactive-contingency.md);
  - and, better, counting only agent acts that were not triggered by the partner: its spontaneous, internally timed acts (micro-variations, endogenous fluctuations). Those are the condition under which Watson's analysis is valid as written, and they work as an instrument.
- Self-other face map: perfect two-way contingency at a fixed delay labels the engine's own rendered face or voice when it comes back through its senses. That channel can calibrate the efferent-afferent delay (the 1994 "perfect algorithm") before any partner learning, and it must be excluded from the partner model. Stoytchev's robot (Robotica 2011) implemented exactly this with thresholds on S and N per visual feature and noted two practical corrections: count only commands that can move the feature, and only when the feature is visible; without them N never gets near 1.
- The time base must be explicit and short for "self" (perfect contingency), and the window for "partner" should be estimated, not assumed; the lag must be strictly positive so that no act at τ is credited with an effect at τ.

## License
The Behavior Analyst / Springer, all rights reserved; free to read on PMC.

## Runs on this Mac without a GPU?
Yes: two conditional frequencies over event logs.

## Verdict: adopt (the two indices and their base-rate comparison, as the engine's contingency readout), with the caveat that they do not by themselves separate "I follow it" from "it follows me"
Primary for the definitions read in full; Watson's 1979/1985/1994 chapters, which hold his infant data and the "perfect algorithm", not read.
