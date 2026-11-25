# DiffListener: Discrete Diffusion Model for Listener Generation (Jung & Kim; ICASSP 2025; arXiv 2502.06822)

Sources read: arXiv 2502.06822 HTML (input, output, metrics, Table I) via a summarising fetch, so quotes are from that tool's extraction; github.com/SiyeolJung/DiffListener README (full) and license field; Google Drive folder listing (names and sizes only).

## What it predicts, from what
- Output: listener 3DMM expression coefficients and head rotation through a VQ-VAE decoder (the LM-Listener/L2L representation; EMOCA used for rendering).
- Input: "the speaker's facial information, audio, and text", plus frame differences of the speaker face; audio as MFCC, text via BERT. Non-autoregressive discrete diffusion over 8 s (240-frame) clips.
- Data: Trevor and Stephen listeners from the L2L / LM-Listener datasets; uses both repos' environments.

## Released code and weights
- Code: MIT.
- Weights: Drive folder `ckpt`: `trevor_difflistener.pth` **8.8 GB**, `trevor_vqvae.pth` 103 MB. Trevor only. No weights license.

## Published metrics (Table I, as extracted)
- L2, FD, P-FD ("distribution distance between listener and speaker"), Diversity, Variation (definitions follow LM-Listener; not restated in the paper).
- Trevor: DiffListener L2 0.40, FD 15.75, P-FD 17.22, Diversity 2.96, Variation 0.10; L2L 0.62 / 25.28 / 27.11; LM-Listener 0.69 / 28.67 / 30.56; ViCo baseline 0.41 / 17.94 / 19.22. GT diversity 2.59.
- Stephen: DiffListener 0.65 / 26.47 / 28.47; L2L 0.65 / 28.69 / 30.33.
- Its LM-Listener numbers differ from LM-Listener's own Table 1 (L2 0.43, FD 18.22), so they are a re-run, not quoted.

## Runs on this Mac as published?
- No. Built on the L2L (CUDA 9, Python 3.6, `.cuda()` calls) and LM-Listener (CUDA, bf16) environments; an 8.8 GB checkpoint would take more than half the 16 GB memory in fp32 and breaks the 6 GB budget in machine.md.

## Runnable on Seamless features as published?
- No. Needs speaker 3DMM from video and raw audio (MFCC); outputs FLAME-family coefficients. Text is the only Seamless-available input.

## Verdict: not runnable (video 3DMM + audio in, FLAME out; CUDA; 8.8 GB checkpoint)
