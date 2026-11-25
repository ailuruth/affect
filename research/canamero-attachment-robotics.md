# Cañamero group: arousal regulation, comfort seeking and adaptation to caregiver responsiveness

Primary source read in full: Hiolle, Lewis and Cañamero, "Arousal regulation and affective adaptation to human responsiveness by a robot that explores and learns a novel environment", *Frontiers in Neurorobotics* 8:17, 2014 (PMC4030164). For the group's later direction I also read the abstract and limitations of Khan and Cañamero, "The long-term efficacy of 'social buffering' in artificial social agents", *Frontiers in Robotics and AI* 2022 (PMC9520257).

## Claims (Hiolle et al. 2014)
- A Nao "infant" explores objects on a table. **Arousal** is an exponential average of *Stimulation*, the novelty or prediction error of two learners: Hopfield recall error plus the change in self-organizing-map weights.
- **Comfort** comes from a human face (OpenCV detection) or a head touch. Both are exponentially decaying traces, and comfort lowers arousal.
- Behavior follows arousal thresholds:
  - high: Find-Human (search for a face, then gaze);
  - medium: stay and learn;
  - low: step sideways and explore.
- "Needy" and "independent" profiles differ only in how long comfort lasts (trace rate $\beta_h$, window $\tau_h$). Needy robots learned more; independent robots explored more. Neither profile is better.
- Adaptive version: a **responsiveness** estimate $Resp_h$ rises when comfort follows a request and falls when it does not. It shifts $\beta_h = 0.7 + (1-Resp_h)R_{\beta}$ and $\tau_h$, moving the robot toward needy under a responsive caregiver and toward independent when requests go unanswered. This is inspired by Ainsworth's attachment patterns.

## Evidence
- Profiles were tested with 10 runs per profile per environment, using an automated caregiver that responds one second after each request. Only "representative runs" are shown, with no statistics.
- The adaptive test had 5 runs with the experimenter as caregiver, alternating responsive and unresponsive periods. One typical run is plotted: responsiveness rose until about 150 s, then fell after unanswered requests at about 170 s and 240 s. Comfort's effect then lasted longer.
- A study with naive users (children aged 8–12) was planned but not reported in this paper.
- Khan and Cañamero 2022 (abstract only): six simulated agents with oxytocin-like and cortisol-like signals. Long-term outcomes depended on early-stage interactions with bond partners. The authors list overfitting to empirically tuned parameters as a limitation.

## License
- Papers: CC BY 3.0 (2014) and CC BY 4.0 (2022).
- Code: none for 2014. The 2022 paper has a data/model availability statement.

## Runs on this Mac without a GPU?
Yes in principle. The 2014 model is a handful of scalar equations, a Hopfield net and a SOM. No code was released for 2014, so it would have to be re-implemented, which is trivial.

## Verdict: adopt (the mechanism, renamed)
Adopted as the theory and mechanism basis for **contact seeking** and **adaptation to the user's responsiveness**.
- The dynamics are homeostatic and satiable: comfort lowers a drive and never rewards the robot (Principle 6).
- Their "arousal" is a hand-named variable set from novelty, which Principle 2 forbids. We keep the *mechanism*: novelty or prediction error feeds a **predictability** body variable, and user contact feeds a **social-contact** body variable. The scalar "arousal" itself goes.
- Evidence is thin (no statistics, n=5 for adaptation). Use it as a design source, not as proof.

## What it gives S1
- **Contact as a decaying trace.** User messages restore social contact; the trace decays with time. Its decay constants are learned per user from responsiveness, as $Resp_h$ is. This gives a concrete, falsifiable *separation and reunion* prediction:
  - User A answered the Bot's past bids. The Bot becomes "needy": contact decays faster, it bids sooner after silence and shows a stronger reunion response.
  - User B ignored bids. The Bot becomes "independent": it makes fewer bids and gives a milder reunion.
  - **Ablation:** remove $h$ (or the responsiveness coupling), and A and B get identical reunion behavior for the same silence length.
- **Prediction error as a separate body input.** Surprising user behavior should raise the predictability deficit and push the Bot toward seeking contact or reassurance. Familiar behavior pushes it toward exploration (new topics, initiative). This splits "unsettled" from "lonely" without naming either.
- **Do not reward responsiveness.** Responsiveness should only reshape decay. It must not become a quantity the Bot maximizes, or the Bot learns to fish for replies.
