# Yoshida, Sprekeler & Gutkin 2025: Linking Homeostasis to Reinforcement Learning (HRRL perspective)

Source read: arXiv 2507.04998v1, full text. The drive-function equation is garbled by PDF text extraction. It is reconstructed below from the surrounding text ("m and n are free parameters. When m = n = 2, it becomes the Euclidean distance").

## Claims
- Reward should be defined from interoception: reward = reduction of a drive, where the drive is the distance of the internal state from its setpoint (Keramati & Gutkin).
- Maximising discounted drive-reduction reward is equivalent to minimising discounted deviation from the setpoint, so HRRL is optimal predictive homeostatic control. The equivalence requires discounting.
- *[Unverified, 2026-11-25]* This note records `m > n > 1`. VERIFICATION-5 confirms the paper states it in clean prose (p. 7), so it was not a reading error. Keramati & Gutkin 2014 and Dulberg et al. 2023, both read in primary, give `n > m > 1`. The conventions differ between these papers, and the reason is unresolved. The candidates follow Keramati & Gutkin's original n > m > 1.
- With `m > n > 1` (as recorded) the reward has four properties:
  - it increases with outcome size;
  - it is potentiated by deprivation;
  - it is inhibited by an unrelated deficit;
  - it is concave in the outcome (risk-averse).
  The authors also call the value function prospect-theory-like.
- A "partially model-based" HRRL is possible: the agent knows its internal dynamics and preferences but must learn the external world.
- Anticipatory (allostatic-looking) responses emerge from homeostatic reward plus prediction. Example: predictive shivering to a bell that precedes cold (Keramati & Gutkin 2014, reproduced as Fig. 2c).
- Social extension is speculative. The paper cites Yoshida & Man for cross-agent drive coupling, and hypothalamic and dopaminergic evidence that social state is signalled "homeostatically".

## Evidence
A perspective with no new experiments. Figures reuse earlier results (Keramati & Gutkin 2011/2014). Deep-RL scaling claims point to Yoshida et al. 2017/2023/2024 and were not checked here.

## Equations worth copying
- State `H = (h_1..h_N)`, setpoint `H*`, drive `d(H) = ( sum_i |h*_i - h_i|^n )^(1/m)`, with `m > n > 1` for the listed properties.
- Outcome `K`: `H_{t+1} = H_t + K_t`; reward `r = d(H_t) - d(H_t + K_t)`.
- Overshoot is punished: consuming at or beyond the setpoint raises the drive and gives negative reward. Satiety is built in.

## License
Paper: CC BY 4.0 (arXiv). No code (perspective).

## Runs on this Mac without a GPU?
n.a. for the paper. The formalism is a few lines of arithmetic, and tabular or small-network RL on it runs on CPU.

## Verdict: adopt (as the formal basis for body-variable value)
This is Principle 6 stated mathematically: every variable is satiable because the drive has a minimum at the setpoint and overshoot costs reward. Reward comes from the agent's own body, never from the user's behaviour.

## What it gives S1
- S1 body variables `b = (contact, predictability, activity_budget)` with setpoints `b*`. Use `d(b)` with, for example, `n = 2` and `m = 3` (the paper fixes only `m > n > 1`) as the single scalar that `pi_theta` learns to reduce.
- Cross-need inhibition is free: when the activity budget is depleted, the reward for contact gets smaller. In S1 that means a tired Bot values a returning user's message less, with no hand-written rule.
- Risk aversion and deprivation potentiation give a testable prediction for the silence protocol. After a long silence the contact deficit is large, so the first exchange is worth more and the Bot should invest more in it. A sated Bot should not chase further contact, because overshoot is negative. Ablation: replace `d` with a linear, non-satiable reward and the Bot should keep seeking contact when sated, which is the flattery/engagement failure.
- Partially model-based split: S1 can hard-code the internal dynamics (drift and decay of `b`) and learn only the user-side dynamics. That gives a clean ablation boundary between "body known, world learned".
