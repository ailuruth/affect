# Dyadic Interaction Modeling for Social Behavior Generation, DIM (Tran, Chang, Siniukov, Soleymani; ECCV 2024; arXiv 2403.09069)

Sources read: arXiv 2403.09069 PDF (Sec. 3 representation, Sec. 4 setup, metrics paragraph, Tables 1-2); github.com/Boese0601/Dyadic-Interaction-Modeling README, LICENSE.txt, file tree (no checkpoint files), issues #1-#2.

## What it predicts, from what
- Output: listener (and speaker) EMOCA (FLAME) expression and pose parameters; PIRender for video.
- Input: speaker EMOCA motion and HuBERT audio features; pre-trained jointly on speaker and listener motion on CANDOR ("over 850 hours"), then fine-tuned on ViCo or LM_Listener data.

## Released code and weights
- Code: yes, USC research license ("educational, research and non-profit purposes"; commercial use by request).
- Weights: not released. README has no checkpoint link; issue #2 (Dec 2024) "Is there any plan for providing pretrained VQ-VAE?" and later comments ("will the model checkpoints be released for inference?", Jun 2025) have no answer.

## Published metrics
- "Frechet Distance (FD), Paired FD (P-FD) for synchrony, Mean Squared Error (MSE), SI for Diversity (SID), Variance (Var), and Residual Pearson Correlation Coefficient (rPCC)"; details in supplementary (not read).
- ViCo (Table 1), expression: DIM-Listener FD 23.88, P-FD 24.39, MSE 0.70; L2L† (CANDOR-pretrained) 31.03 / 33.02 / 0.87; RLHG 39.02 / 40.18 / 0.86.
- LM_Listener data (Table 2): DIM-Listener FD 12.49, P-FD 12.95, MSE 0.29; L2L† 21.63 / 22.03 / 0.73; Mirror 69.25 / 87.11.

## Runs on this Mac as published?
- Not applicable (no weights). Tested "on 2 x NVIDIA L40S" with CUDA 12.5.

## Runnable on Seamless features as published?
- No. Needs EMOCA from video and raw audio (HuBERT); outputs EMOCA.

## Verdict: not runnable (no weights; needs video-derived EMOCA and raw audio)
- Strongest published numbers on the L2L-family benchmarks I found, but unusable here.
