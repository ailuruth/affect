# Seamless Interaction: the paper's own limitations and evaluation caveats (Meta, arXiv 2506.22554, 2025)

Seamless Interaction team (Meta FAIR). "Seamless Interaction: Dyadic Audiovisual Motion Modeling and Large-Scale Dataset." arXiv 2506.22554, 2025. This complements seamless-interaction.md (dataset and features). Here I collect only what the paper itself says about where its models fall short, and how its evaluation could mislead.

## What was read
- From the arXiv PDF (pdftotext): Sec. 2.4.5 "Known Limitations and Areas of Future Work" (dataset); Sec. 4.1, 4.2, 4.3 (start), 4.4.1 "Emotion Controllability", 4.5 and 4.5.1 (speech-LLM integration); Sec. 5.2.3 (body adapter receptive field) and 5.2.5 "Limitations" (3D rendering); Sec. 6.1.2-6.1.3 (face-dyadic and body-dyadic human studies, analysis and discussion); Sec. 6.2.1 results paragraph; Sec. 6.3 and Table 20 (automatic metrics against human preference); Sec. 9 Conclusion. I did not read Sec. 4.4.2-4.4.3 in full, Sec. 5.1, Sec. 7-8, or the appendices beyond A.1.4's heading.

## Claims
- Dyadic Motion Models generate face (Imitator code, 137-d) and body (SMPL-H) motion from both speakers' speech tokens. The audiovisual variant also takes the user's visual features (Imitator latent, SMPL-H pose). Conclusion: the models "take into consideration the visual behaviors of the interlocutor" and "can adapt emotional responses and expressivity levels".

## Evidence and the limitations the paper states
- **Emotion is an external knob.** Sec. 4.4.1: "We use an internal tool to extract arousal and valence sequences for each sample ... in the numerical range from −1 to 1", discretised into buckets. The model learns p(lat_t | lat_{t−1}, b_a, b_v). At inference the emotion is either absent, set "on constant values (a_c, v_c) for stable emotional profiles", or "externally generated sequences (a, v) (e.g., from audio features or semantic analysis)".
- **Language to motion is one-way.** Sec. 4.5: "we always freeze the speech model to ground our diffusion generation ... we feed the generated dialogue (in the form of speech tokens) to ground our dyadic motion models." In 4.5.1 an adapter reads the speech LLM's hidden states and predicts valence, arousal and gesture tokens for the diffusion model. No path described runs back from the generated face to the speech model.
- **No spatial or gaze coupling between partners.** Sec. 5.2.5: "the training data for the dyadic motion model are two independent monocular videos ... not spatially calibrated ... the motion model has no awareness of the spatial relationship between the two interlocutors. As a result ... they will not necessarily establish eye contact."
- **Body-shape unawareness** (self-interpenetration), and decoders that "struggle with large non-articulated motions" (hair, loose clothing).
- **Human ratings may favour activity over fidelity.** Sec. 6.1.2: "low-activity (i.e., boring) segments of actual GT human behavior is typically dispreferred when compared to more active synthetic behavior." GT renderings also carry extraction artifacts ("jitter, stretching ... misalignment between the head and shoulders") that "may be responsible, in part, for the closeness of ratings to GT". Face study: n = 81 raters, 61 segments of 20 s. Body study: n = 105 raters, 71 segments, with two models "virtually indistinguishable from GT mesh renderings".
- **A lip-sync metric runs against perceived lifelikeness.** Table 20: correlation of human "Overall lifelikeness" preference with metric deltas. FFD r = 0.562 (ρ = 0.573*, τ = 0.406*); Sync-C r = −0.307 (ρ = −0.328*, τ = −0.223*).
- **Dataset timing.** Sec. 2.4.5: misaligned interaction time-stamps "impact approximately 10% of interactions after our attempts at correction". Participant IDs are sometimes duplicated or split. The "meta time" between prompts is unreleased.

## Failures documented
- No internal emotional state: affect is a classifier-derived A-V condition chosen from outside. The face nods and smiles because the training video did, at that point in the speech.
- The language model never learns what its face did. The coupling runs from frozen LLM to adapter to motion, with no return path.
- Gaze and spatial mutuality are absent by construction.
- Human-preference evaluation is confounded by an "activeness preference" and by GT rendering artifacts, so "close to GT" ratings do not show human-equivalent interaction.
- The paper reports no interpersonal synchrony statistics for its generated output against surrogates (see seamless-interaction.md, 2026-11-24 entry).
