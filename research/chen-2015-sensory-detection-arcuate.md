# Chen, Lin, Kuo & Knight 2015, "Sensory detection of food rapidly modulates arcuate feeding circuits" (Cell 160:829-841)

Source read: the NIH author manuscript in PMC (PMC4373539), fetched as full-text XML on 2026-11-24 and read in full: summary, introduction, all Results sections, Discussion, Experimental Procedures and the seven main figure legends. Not read: the supplementary figures S1-S4, the supplementary movies and the extended methods. Numbers quoted from Figures S2-S3 below come from the main text, which cites them. The figures themselves were not viewed, only their legends.

## Claims
- Fasting puts AgRP neurons in an activated state. The sight and smell of food reverses that state within seconds, before any food is eaten: "the sensory detection of food is sufficient to rapidly reverse the activation state of these neurons induced by energy deficit".
- The drop is anticipatory and contingent. The neurons "anticipate the change in their activity that will occur following food consumption, taking into account factors such as the food's energy density, perceived accessibility, and the nutritional state of the mouse".
- If the food is detected but then removed before it is eaten, the activity returns to the hungry level, and it does so about ten times more slowly than it fell.
- The authors offer two readings of the purpose. Their main one is that the drop "represents a mechanism to rapidly inhibit foraging and other appetitive behaviors once food has been discovered". They also float a learning reading: "If AgRP activity has negative motivational valence (analogous to the unpleasant sensation of hunger), then this might enable animals to learn the consequences of failing to eat after obtaining food." They say this second idea is untested. Betley et al. 2015 test it (see betley-2015-agrp-negative-valence.md).

## Evidence
Fiber photometry (GCaMP6s) of AgRP and POMC populations in awake mice. Typical n: "AgRP, n=10; POMC, n=5" for the fasting experiments; "n=7 ... n=5" for ghrelin.

Speed and size of the response to food detection:
- After ghrelin, presenting chow "rapidly reversed much of the effect of ghrelin treatment (ΔF/F = −29 +/− 3% at 2 min for AgRP neurons ...)", with "τ = 12 +/− 2s for AgRP neurons; τ = 44 +/− 3s for POMC neurons". By comparison, ghrelin itself raised AgRP activity with "τ = 76 +/− 12s".
- Overnight fast, then chow: "ΔF/F = −37 +/− 4%, at 5 min" for AgRP, with "τ = 20 +/− 4s for AgRP neurons and τ = 42 +/− 18s for POMC neurons".
- Most of the change happens before eating: "96 +/− 6% complete before feeding in AgRP neurons, 85 +/− 5% in POMC neurons". The response appeared "in the first trial of each mouse", so it needs no training.
- The response is specific to food. An inedible object gave "ΔF/F = 4.9 +/− 2.2%" in AgRP neurons.

Dependence on hunger state and palatability:
- In ad libitum fed mice, chow had no effect on AgRP neurons: "ΔF/F = −4.7 +/− 1.0%, p=0.21 compared to object".
- Peanut butter in fasted mice: "ΔF/F = −54 +/− 6% at 5 min", with "τ = 23 +/− 6s for AgRP". This is "comparable in magnitude (but opposite in sign) to the effect of injection with pharmacologic doses of ghrelin".
- Peanut butter still worked in fed mice: "ΔF/F = −24% +/− 4%, at 5 min, p<0.001 compared to chow". The response is not purely a readout of the deficit.
- Peanut butter first "could completely block the subsequent neural response to presentation of chow". Chow first "only partially diminished the response in AgRP neurons".
- With repeated chocolate trials the response became faster, which suggests learning: "τ = 40 +/− 8s in trial 1 versus 17 +/− 2s in trial 4, p<0.01".

Food detected but not eaten:
- Peanut butter visible and smellable but out of reach: "ΔF/F = −39 +/− 4% after 2 min; τ = 21 +/− 4s". The response was "somewhat smaller in magnitude" than with accessible food, and the POMC response was "less durable".
- Smell only ("hidden peanut butter"): "ΔF/F = −12 +/− 5% after 1 min in AgRP neurons". Activity returned to baseline "within eight minutes" ("ΔF/F = 8.3 +/− 4.5% after 8 min").
- Food removed after presentation: activity reverted, with hysteresis "approximately ten-fold more slowly than the initial response to food presentation". For AgRP neurons, "τ =15 +/− 1s versus 258 +/− 26s, p<0.0001". After 30 min of access the reversal was smaller, "consistent with food consumption during the feeding interval partially resetting the activation state".

Within meals (liquid diet, lickometer): "17 +/− 2 feeding bouts" per hour. AgRP activity "declined in activity until the moment of the first lick and then their activity flattened".

## License
© 2015 Elsevier Inc., all rights reserved. The PMC record states "available for text mining" and use "consistent with the principles of fair use". No code or data release in the text I read.

## Runs on this Mac without a GPU?
n.a. (empirical neuroscience).

## Verdict: adopt (as the empirical anchor for an anticipatory need signal)
This is the cleanest measured case of a need signal that drops before the body changes.
- For (b), the anticipatory drop: the need-related activity a model broadcasts should be able to fall in seconds on a reliable predictor of the outcome, with no change in the body variable. Seconds versus minutes is the empirical scale: τ ≈ 12-23 s on detection, against about 76 s for a hormonal rise and about 258 s for the relapse after removal. The size of the drop should scale with expected nutritive value (peanut butter > chow > object), with the current deficit (none for chow when fed), and with perceived access (inaccessible and smell-only food give smaller drops, and the smell-only drop is transient). If the predicted outcome does not arrive, the signal must relapse to the level the body state implies, and more slowly than it fell.
- For (a), the costate: this behaves like a value-based quantity that already includes the expected intake. It does not behave like the raw deficit. A gradient of the value function with respect to the body variables, evaluated after the predicted intake, would show this pattern. The paper does not make that claim; it is our reading.
- Caution: the fed-mouse response to peanut butter means the signal is not purely deficit-gated. The authors attribute this to "hedonic properties". A pure costate of a drive function would give zero in a sated state, so this is one measured point against a strict drive reading (compare Berridge 2004).
- Photometry is a population average. The authors themselves note that it "can mask heterogeneity". Betley et al. 2015 report single-cell data.
