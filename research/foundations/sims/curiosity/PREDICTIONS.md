# Shared curiosity toy: learning progress as a satiable body variable (sim_lp.py)

Written 2026-11-25, before any run. This answers the limit TH7 found, which all three candidates share: surprisal minimization gives the dark room, and a predictability set point gives the noisy TV.

## Channels (one choice per step, 600 steps)

- **L1:** learnable fast. Error e = 0.05 + 0.95·exp(−n/20) after n visits.
- **L2:** learnable slow. e = 0.05 + 0.95·exp(−n/80).
- **N:** noise. e = 1.0 + N(0, 0.3²) on each visit; nothing to learn.
- **B:** boring. e = 0.05 + N(0, 0.01²).

## Learning progress (the windowed comparison of Oudeyer et al.'s IAC, stated as ours until the source note exists)

- For each channel, LP_ch = mean error over the last 5 visits minus mean error over the 5 visits before those.
- The expected LP of an unvisited or rarely visited channel starts optimistic: 0.2 until it has 10 visits.

## Agents

1. **LP body variable** (proposed).
   - b_lp is an exponential moving average, τ = 10 steps, of the LP actually obtained.
   - Set point b_lp* = 0.01; d = (b_lp − 0.01)².
   - The agent picks the channel maximizing −d′(b_lp)·(E[LP_ch] − b_lp).
   - Two-sided: when learning is above the set point, it prefers low-LP channels.
2. **Predictability set point** (TH7's agent 2, same channels).
3. **Surprisal minimizer** (TH7's agent 1, with a 200-step forecast).

## Predictions

- **LP-1.** The LP agent chooses N in < 5% and B in < 10% of steps while any learnable channel still has e > 0.1.
- **LP-2.** The LP agent learns both learnable channels: both reach e < 0.1 by step 600. It visits L1 before L2. The first time L1's share of choices exceeds 50% over a 20-step window comes earlier than for L2.
- **LP-3.** Once both learnable channels are learned, no channel holds a persistent preference: neither N nor B exceeds 80% of the remaining steps. **Satiation without a dark room:** the deficit persists as boredom, but nothing is pursued without end.
- **LP-4.** The predictability set-point agent chooses N in > 20% of steps (the noisy TV, as in TH7), and the surprisal minimizer chooses B in > 95% (the dark room).
