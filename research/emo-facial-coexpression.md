# Human-robot facial coexpression (Emo)

Hu, Chen, Lin, Wang, Wang, Mehlman and Lipson, *Science Robotics* 9(88):eadi4724, March 2024, doi:10.1126/scirobotics.adi4724.

Read: the abstract (via Europe PMC; no open full text exists, as Europe PMC and PMC show no copy and arXiv has no version) and the GitHub repo `H-Y-H-Y-H/HR_Facial_Coexpression` (README and all `.py` files). The repo looks like the authors' evaluation code: it holds paper tables and "paper_data". Its ownership is **not verified**, because the GitHub profile has no name.

## Claims (abstract)
- Delayed facial mimicry "looks disingenuous". Coexpression, meaning a simultaneous expression, "feels more genuine because it requires correct inference of the human's emotional state for timely execution". These are the authors' claims; the paper body is not read.
- The robot learns to predict a forthcoming smile **about 839 ms** before it happens. A **learned inverse-kinematic facial self-model** then lets it smile at the same moment, on a face with 26 degrees of freedom.

## Evidence
- Paper body unread. The code shows:
  - MediaPipe face mesh, reduced to 113 two-dimensional landmarks;
  - a predictive model over a buffer of past landmark frames that outputs future landmarks, and only activates when the face departs from a static neutral face by more than a threshold;
  - `human2robot` normalization;
  - an MLP inverse model, 226 → 1024 → 512 → **11** sigmoid servo commands (11 in this code against 26 DoF in the abstract, a discrepancy I could not resolve);
  - commands sent over a socket.
- All pipelines set `device = cpu`. Trained weights and datasets are on Google Drive links, which I did not download.

## License
- Paper: © AAAS (paywalled).
- Code: **no licence file** (all rights reserved). Data is also deposited on Dryad (doi:10.5061/dryad.gxd2547t7, not opened).

## Runs on this Mac without a GPU?
Yes for the shipped pipeline (MediaPipe plus small MLPs, CPU-only in code). It needs the physical robot or a substitute renderer to be useful.

## Verdict: watch (motor layer only)
This system maps partner video straight to its own motor commands. Its *when* and *why* come from the partner's predicted landmarks, which is the anti-pattern the brief names. It can only ever be a motor or rendering layer, and its abstract frames the job as inferring "emotional state", which Principle 1 rules out as a target. Two parts are relevant to S2:
- the **learned inverse self-model** (landmarks → own actuators, learned from the robot's own random babbling), which belongs to Principle 3;
- the finding that **anticipation removes mimicry lag**.

The missing licence blocks reuse of the code.

## What it gives S1
- Nothing directly, since S1 is text only. Two lessons go into the S2 prediction now:
  - **Timing is evidence of source.** Expressions driven by $h$ and expressions driven by mimicry should be separable by latency relative to the user's onset. Coexpression is near zero lag, mimicry lags, and state-driven expressions can precede, follow or oppose. The S2 ablation ("remove the emotional pathway, only voluntary or Claude-timed expressions remain") can be scored by that latency distribution.
  - **Self-model by babbling.** Generate random AU commands, render them, and run the face-feature extractor on the result. That yields an inverse model with no human labels, consistent with Principle 1 and complementary to samuel.md.
