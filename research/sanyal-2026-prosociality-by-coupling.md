# Sanyal 2026: Prosociality by Coupling, Not Mere Observation (inspectable recurrent ALife agent)

Source read: arXiv 2604.10760v2 (cs.MA, 9 Jun 2026), full text. Code read: `core/social_homeostat.py` in github.com/xcellect/recips.

## Claims
- Reproduces Yoshida & Man's observation-versus-coupling dissociation in a small, hand-specified, non-learning controller (ReCoN-Ipsundrum plus a scalar homeostat).
- The planner scores only the actor's own predicted internal variables. Partner distress enters upstream, through the homeostatic error, not as a welfare term in the objective.
- Lesions that cut the coupling (coupling-off, shuffled partner signal) abolish helping; a sham lesion does not.
- Coupling is not "more is better": whether helping succeeds depends on metabolic load.

## Evidence
- FoodShareToy (one step, exact solver): the choice switches from EAT to PASS at `lambda* ≈ 0.91`. Default energies are possessor 0.55 and partner 0.20.
- SocialCorridorWorld (1-D, hazard in the middle): planner horizon 10, 18-step episodes. Uncoupled conditions never help (help rate 0, soft viability 0.15). Coupled conditions always help (rescue at t=9, viability 0.3286); actor final energy falls 0.745 to 0.605 and partner energy rises 0.02 to 0.27.
- Coupling sweep `lambda ∈ {0, .25, .5, .75, 1}` at low, medium and high load: helping appears from 0.25 at low load and never at medium or high load.
- Deterministic tasks, rerun with 64 seeds, outcomes identical. There is no learning, no memory and no partner decoder (stated limitations).

## Update rule worth copying (eq. 1; defaults from code)
```
E_true' = clip(E_true - c_b - c_m*move - c_h*hazard + g_e*eat + g_p*pass, 0, 1)
d_self  = max(0, s - E_model);  d_other = max(0, s - E_other_hat)
d_cpl   = d_self + lambda*d_other
E_pred  = clip(E_model - k_h*d_cpl, 0, 1)
PE      = E_true' - E_pred
E_model'= clip(E_model + k_pe*PE, 0, 1)
```
Defaults: `s = 0.70`, `c_b = 0.01`, `c_m = 0.005`, `c_h = 0.05`, `g = 0.25`, `k_h = 0.25`, `k_pe = 0.50`.

Scorer: `J = sum_tau (2.0*V - 1.2*A - 0.8*N_s - 0.4*B)`.

## License
- Paper: CC BY 4.0.
- Code repo: no license file, so all rights are reserved by default. Reimplement from the paper.

## Runs on this Mac without a GPU?
Yes. Pure Python, small deterministic rollouts.

## Verdict: watch
- Against: valence and arousal are hand-set functions of distress (`V = 1 - clip(d/0.5)`, `A = clip(d)` in code), which Principle 2 forbids. Nothing is learned.
- For: the lesion suite is a working template for Principle 5. Sham, coupling-off and shuffled-signal lesions keep the planner fixed and remove one channel. The separation between the body's true value, the agent's internal estimate, and the prediction error is the right structure for S1.

## What it gives S1
- Keep three separate quantities per body variable: true `b` (simulated), the Bot's estimate `b_model`, and the prediction error `PE`. PE feeds `h`, which matches the brief's "learns online from prediction error on b".
- Put user coupling in the error term, not the objective: `d_cpl = d_self + lambda*d_user_hat`. A shuffled-user control (feed another session's user signal) is a cheap S1 ablation and tells "coupled to this user" apart from "has an extra input".
- Load matters. Coupling only produced helping at low metabolic load. In S1, a Bot whose activity budget is depleted should not respond to a returning user's need. State that as a prediction, not as a bug.
- Do not copy the V/A formulas or the fixed scorer weights. Read valence out of `h` instead (see `hesp-2021-deeply-felt-affect.md`).
