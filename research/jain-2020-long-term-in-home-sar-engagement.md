# Jain, Thiagarajan, Shi, Clabaugh & Matarić 2020: engagement over a month of in-home socially assistive robot use

S. Jain, B. Thiagarajan, Z. Shi, C. Clabaugh, M. J. Matarić. "Modeling Engagement in Long-Term, In-Home Socially Assistive Robot Interventions for Children with Autism Spectrum Disorders." *Science Robotics* 5(39):eaaz3791 (2020). Read as arXiv:2002.02453v2 (accepted manuscript, 11 Apr 2020). https://arxiv.org/abs/2002.02453

**How fully read (2026-11-28):** the arXiv v2 PDF, text-extracted. The abstract, introduction, results (engagement over time, model results, temporal patterns), discussion and materials and methods were read. The supplementary materials were not read. Figures by caption.

This was chosen in place of Kanda et al. 2004 and Leite, Martinho & Paiva 2013, which were not reachable (see the pass-18 synthesis).

## What it says
- **Study.** 7 children with autism (mild to moderate). A month in their homes, playing math games on a tablet with a desktop robot (Kiwi) that gave verbal and expressive feedback. The robot's challenge levels were personalised by reinforcement learning. About 3 h of data per child over many sessions. Engagement was annotated per frame, binary (Fleiss κ = 0.84).
- **Engagement fell for everyone.** Mean 65 % engaged (range 48–84 %, SD 14 %). "All participants had a significant (p < 0.01) decrease in engagement over the month-long intervention." Example: participant 2 was engaged 82 % of the time in the first tenth and 19 % in the last tenth.
- **The robot's speech brought engagement back:** about 70 % engaged when the robot had spoken in the previous minute, under 50 % after more than a minute without robot speech. The authors read this as validating "appropriately-timed robot speech as a tool for eliciting and maintaining user engagement".
- **Models.** Generalised and individualised engagement classifiers reached AUROC ≈ 0.90 but had lower recall for disengagement. The authors propose online detection of disengagement to trigger re-engagement actions.
- All children improved in reasoning skills and retention of content (reported from the companion papers, not re-analysed here).

## What matters for this engine
1. **Novelty decline over a month is the norm**, even with personalisation and a task the children were assigned. The operator will likely talk less with the agent after the first weeks. The brief's S6 claim (a relationship specific to him forms over months) needs enough sessions per week, so this is a project risk.
2. **The field's standard fix is the harm this engine must not adopt.** Detecting disengagement and timing the robot's speech to recapture attention is an engagement objective. Here it was benign, inside a therapy task. Applied to a companion's free time, it is De Freitas's retention mechanism. The engine's initiative is tilted only by its own drives through the 𝓜 rollout. His face and replies are imputed there (r4 §2.10), and nothing reads his engagement as a target (Principle 6). Keep it so: decline in his use is an outcome to report, never an error to correct.
3. **Speech raises engagement mechanically.** Any learned initiative policy whose credit can see his engagement will learn to speak more. The once-per-lapse bound was removed in revision 9 (S34). So nothing now bounds how often the agent speaks into his silence except the learned hazard and the daily call cap.

## Verdict: watch
It is a small clinical sample of children with a task, not adult companionship. It is used for two facts: engagement falls over a month, and robot speech re-engages. It also shows that the standard HRI response is a re-engagement controller, which this engine excludes by Principle 6.
