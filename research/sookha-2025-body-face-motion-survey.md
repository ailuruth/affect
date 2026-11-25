# A Survey of Body and Face Motion: Datasets, Performance Evaluation Metrics and Generative Techniques (Sookha, Pakhale, Ganaie, Dhall; arXiv 2512.09005, 2025)

Sookha, L. R., Pakhale, N., Ganaie, M., Dhall, A. "A Survey of Body and Face Motion: Datasets, Performance Evaluation Metrics and Generative Techniques." arXiv 2512.09005v1, Dec 2025 (formatted for IEEE TVCG).

## What was read
- Abstract; introduction (scope paragraphs); diversity and subjective-evaluation metric subsections; the face-animation subsection on listener models; the full "Challenges and Future Directions" section with Fig. 5. I did not read the dataset tables or the body-animation and text-to-motion method sections. It is the only survey I found that covers listener-face generation alongside body motion. I found no dedicated survey of listening-head or facial reaction generation.

## Claims
- "generating expressive and coherent face and body dynamics remains challenging due to the complex interplay of verbal/non-verbal cues and individual personality traits."
- Fig. 5 challenge summary: "Limited scope on personalization. Ignores person-specific traits"; "Limited context focus. Context is limited to short contextual cues"; "Temporal and detail limitation. Difficulty in maintaining consistency and microexpression"; "High Computational cost. Limits real-time use"; "Over-representation of English language".
- Avatar customization: recent work "generally do[es] not account for user-specific personality traits. Existing approaches tend to focus on short, context-dependent descriptions tied to conversations and anticipated reactions, without modeling deeper individual differences."
- Diversity: "Low diversity often indicates mode collapse, where the model generates overly similar motions."
- Evaluation: the GENEA challenges "highlighted the limitations of relying solely on objective metrics".
- Deployment: diversity, realism and controllability "often come at the expense of high computational cost ... hinder their deployment in real-time or resource-constrained environments".
- Data: Audio2Photoreal's "limited participant pool, consisting of only four individuals, restricts the diversity and generalizability of human behaviors captured."

## Evidence
- A narrative survey: no new experiments and no pooled numbers. Its value here is as a field-level statement of the same failures that the primary papers show.

## Failures documented
- No person- or relationship-specific behaviour. Context limited to short cues. Mode collapse as a recurring risk. Real-time cost. Objective metrics insufficient.
