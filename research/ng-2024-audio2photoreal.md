# From Audio to Photoreal Embodiment (Ng, Romero, Bagautdinov, Bai, Darrell, Kanazawa, Richard; CVPR 2024; arXiv 2401.01885)

Sources read: arXiv 2401.01885 PDF (Sec. 3 method on audio conditioning, Sec. 4 dataset, Sec. 5.1 metric list); github.com/facebookresearch/audio2photoreal README (dataset, pretrained-model sections) and LICENSE header; HTTP HEAD on one model tar. Included as the L2L authors' follow-up that models listening and speaking together.

## What it predicts, from what
- Output: one person's face as a 256-d Codec Avatar expression code per frame ("each f_t ∈ R^256 represents a face expression"), plus 104-d body joint angles; rendered photoreally by the Codec Avatar body decoder.
- Input: audio of both people: "the audio of the conversation partner as a_other. For both audio streams, we extract Wav2Vec features such that the audio input is A = (a_self, a_other)" (Sec. 3). The face diffusion model is also conditioned on lip vertices from a pre-trained audio-to-lip regressor. The partner's face is not an input.
- Data: 8 h of studio conversations from 4 participants (2 h each), person-specific models.

## Released code and weights
- Code and data: CC BY-NC 4.0 (LICENSE). Weights: `http://audio2photoreal_models.berkeleyvision.org/<person_id>_models.tar`, e.g. `PXB184_models.tar` 1.35 GB (Content-Length), plus Codec Avatar rendering assets per person.
- Metrics (Sec. 5.1): geometric FD, diversity, and others; I did not read the results tables.

## Runs on this Mac as published?
- No. "tested with CUDA 11.7 and python 3.9, gcc/++ 9.0"; pytorch3d and the CA body renderer.

## Runnable on Seamless features as published?
- No. Needs raw audio of both partners (Wav2Vec) and outputs Codec Avatar codes of four specific people.

## Verdict: not runnable (raw audio in, person-specific Codec Avatar codes out; noncommercial)
