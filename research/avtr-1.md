# AVTR-1: Open Stack for Real-Time Interactive Avatars (Kravtsov et al., Avaturn Live; arXiv 2609.22913, Sep 2026)

Sources read: arXiv 2609.22913v1 full PDF; github.com/avaturn-live/avtr-1 README, LICENSE.md, LICENSE-MODEL.md, LICENSE-RENDERER.md, LICENSE-STREAMER.md, PATENTS.md.

## Claims
- A 153M-parameter autoregressive flow-matching transformer predicts 5-frame (200 ms) chunks of head and face motion from both participants' audio; a renderer turns motion into video; a streamer syncs it with an external voice agent and handles interruptions.
- Leads compared dyadic systems on visual quality and most listening metrics; real time on datacenter and consumer GPUs.
- New metric, Reference-Based Directed Granger Gain (R-DGG): extra predictive information that speaker speech carries about listener motion beyond listener history and speaker motion.

## Evidence
- Motion target: 42-D per frame = head rotation (3) + 39 LivePortrait keypoint-deformation coordinates (brow, eyes, mouth), z-scored. Trained on "an internal corpus of 926 hours" of dyadic conversation.
- Table 2 (one 200 ms chunk): L40S 71 ms (2.81x real time), A100 91 ms, RTX 4060 Ti 162 ms (1.24x), RTX 4060 232 ms (0.86x, below real time).
- README: requires "NVIDIA GPU (Ampere or later recommended)", CUDA 12.x and TensorRT 10.x; LivePortrait weights are pulled as ONNX from a third-party HF repo.
- R-DGG finds speech dependence for real listeners and dyadic models but not for talking-head generators or mismatched pairs; the authors say it "should not be interpreted as listening quality or causal influence".

## License (paper, code, model weights)
- Weights and scripts/: AVTR-1 Community License (commercial use only under USD 10M revenue).
- Renderer and Streamer: PolyForm Noncommercial 1.0.0; Streamer also has a patent notice (pending application) with a noncommercial-only patent grant.
- Paper: arXiv.

## Runs on this Mac without a GPU?
- No. TensorRT engines on NVIDIA hardware only.

## Verdict: reject (component); watch the R-DGG metric
- It maps partner audio straight to face motion, so under the item rule it could only be a motor or rendering layer, and it cannot run here.
- R-DGG is useful for S2 evaluation: it can test whether the user's speech or face predicts the Bot's face beyond the Bot's own history, with and without the emotional pathway. That fits the brief's "observe, never grade from inside" stance.

## Role in S2
- none (evaluation idea only)
