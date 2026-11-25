# Ho, Avila-García & Nehaniv 2005: Assessing the performance of different behavior selection architectures in a large and complex virtual environment

Citation: W. C. Ho, O. Avila-García, C. L. Nehaniv. *2005 IEEE Congress on Evolutionary Computation* (CEC 2005), pp. 359-365. doi:10.1109/CEC.2005.1554706. Copy read: University of Hertfordshire repository, uhra.herts.ac.uk/id/eprint/12720.

Source read: the full text, extracted from the repository PDF. The results figures (lifespan, overall comfort, physiological variance) came out as unreadable scan fragments, so no numbers are quoted. The earlier primary comparisons were not obtained and are unread: Avila-García & Cañamero 2002, and Avila-García, Cañamero & te Boekhorst, ECAL 2003, "Analyzing the performance of 'winner-take-all' and 'voting-based' action selection policies within the two-resource problem".

## Claims
- The study compares three hand-built (not learned) behaviour-selection schemes for an agent with four essential variables: Energy, Moisture, Glucose and Temperature.
  - Static-Threshold (ST): consume when a variable falls below a fixed threshold, until it reaches its upper limit.
  - Winner-Takes-All (WTA): `Motivation = Deficit + (Deficit * Cue)` for each motivation, where Cue grows as the agent nears the matching stimulus. "The motivation with the highest value triggers the relevant behavior".
  - Voting-Based (VB): each behaviour sums the motivations it serves, weighted by consumption rate (`Motivation1 * Rate1 + Motivation2 * Rate2`).
- Findings:
  - ST and WTA "obtained approximately the same performance in terms of the lifespan."
  - WTA "produces less variance in the satisfaction of its internal motivations". The authors describe WTA's competition as "creating dynamic thresholds".
  - VB "obtained higher average satisfaction of their internal needs (OvC) than WTA in all the settings", but "worse PhV than WTA".
  - VB "is significantly sensitive to the balance of rates at which various environmental resources can serve to satisfy an agent's physiological needs".
- VB depends on the apple's nutritional rate, the apple being the one resource that serves two needs:
  - at 1:2 the agent "simply ignores the existence of the apple";
  - at 1:1 it "only looks for apple but ignores the existence of water and mushroom";
  - at 4:7 it "consumes Apples, Mushroom and Water stimuli". Only at that balanced point is VB's lifespan "very close to that obtained by ST and WTA."
- Both WTA and VB showed "extra persistence for their consummatory behaviors": agents stayed in water areas even when they could have moved on.

## Evidence
- Environment: a VRML/Java world with oasis, desert, mountain, river, lake, waterfall and caves, and two seasons. Sensing is limited to seven ray sensors plus landform and season sensors, and the agent has no memory. Some resources serve two needs (an apple raises both Moisture and Glucose), and some needs have several sources.
- Runs: 10 per architecture per setting, 4 settings. Each run took about 15 minutes on a Pentium 4.

## License
Paper: IEEE copyright; author repository copy. No code released.

## Runs on this Mac without a GPU?
n.a. There is no code. The selection rules are a few lines each.

## Verdict: watch (evidence on WTA against combining; no learning involved)
It is the only primary comparison found in this scan of WTA-on-the-neediest against combining needs in one agent. The evidence is weak: one environment, 10 runs per cell, results only in figures, and hand-set rules with no learning.

## What it implies for the open question
- With hand-set rules, neither WTA nor combining dominates. They trade off.
  - WTA keeps needs balanced (lower variance) and is robust to resource rates. It misses opportunities.
  - Voting raises average satisfaction and is opportunistic when one resource serves several needs. It is fragile to the relative payoff rates and can lock onto one resource.
- The advantage of combining appears only when the world contains multi-need resources and the rates are balanced.
- Read next to Dulberg et al. 2023: the fragility of voting comes from fixed, hand-set rates. When the per-need values are learned (Dulberg's summed Q-values), combining wins.
- For the Bot: a winner-take-all on the most-depleted need is a defensible baseline for variance, but it cannot exploit an action that serves several needs at once. A single exchange can serve contact, predictability and topic interest together. So the ablation should report balance (variance across needs) as well as mean satisfaction.
