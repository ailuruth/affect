# Gagliardi 2022, "Human attachment as a multi-dimensional control system: A computational implementation" (Frontiers in Psychology, doi:10.3389/fpsyg.2022.844012, PMC9521434)

Source read: PMC full text retrieved via NCBI E-utilities. Read: the introduction on the Strange Situation, the model summary, simulation setup, results headings and figure captions, and the limitations. The equations were NOT checked.

## Claims
- A 2D agent-based "child" and "mother" (dot agents) with attachment and caregiving drives reproduce avoidant and ambivalent patterns along continuous dimensions.
- The Strange Situation is described accurately: "the child is the protagonist of eight three-minute episodes in which they are either alone or can interact with a caregiver or a stranger".

## Evidence
What was adapted:
- A square "lab" with an object of interest per agent.
- The agents start "in the central part of the lab" and run 1,000 iterations, of which "All graphs refer to iterations 800–1,000".
- No separation, reunion or stranger episodes are simulated.
- The dimension levels (Av, Am) are set by hand, and the child is "assumed to have already been" shaped by the caregiver (Av = In, Am = Un).

How it was scored:
- Qualitatively, by trajectories, distances and need levels against literature descriptions.
- The author states: "The evaluation approach adopted for this model is merely qualitative. And, therefore, to be considered only preliminary. A goal for future work is being able to compare simulations to quantitative measures in real situations – such as frequency of attachment and exploration behaviors in a given SSP episode."

## License
CC BY 4.0.

## Runs on this Mac without a GPU?
n.a. as an instrument.

## Verdict: reject (as an evaluation precedent)
It does not run the Strange Situation, and its scoring is the author's qualitative judgment, which the author says is preliminary. It is the conceptual basis for Htet et al. 2024 (htet-2024-coupled-oscillator-attachment-robots.md).
