# NoXi database (Cafaro et al., ICMI 2017) and NoXi+J (arXiv 2409.13726)

Sources read: the NoXi End User License Agreement PDF (full, from multimediate-challenge.org/assets/pdf/EULA-NoXi.pdf); the MultiMediate challenge dataset page for NoXi; the NoXi+J paper (arXiv 2409.13726v1 HTML). I did not read the NoXi ICMI 2017 paper itself: the Nottingham eprint link is broken and the Augsburg copy refused the connection. NoXi facts below come from the NoXi+J paper and the challenge page; for the original paper I saw only the abstract (via search results).

## What it contains
- Screen-mediated dyadic novice-expert conversations: "recordings of dyadic conversations between two interlocutors in the roles of expert and novice". Participants stand in front of 55-inch screens and are recorded with Kinect 2. Sessions run about 7-31 minutes.
- Mainly English, French and German (recorded in the UK, France and Germany). NoXi+J adds 48 Japanese and 18 Chinese sessions; the NoXi+J table lists 150 sessions and 153 participants in total.
- Familiarity: European participants came from research facilities and their "immediate social circles"; NoXi+J relationships range "from zero-acquaintance situations to spouses". Relationship level was collected, but no breakdown is given in what I read. Some participants appear in sessions in more than one language; repeat partners are not described.
- Annotations (abstract and challenge page): low-level social signals (gestures, smiles), turn-taking and dialogue acts, and continuous engagement, interest and fluidity.
- The challenge version contains "video recordings, audio recordings and annotations".

## Per-frame facial features?
Not released as far as I can tell. The challenge page lists only video, audio and annotations. NoXi+J lists 17 AUs among its extracted features (tool not named; about 25 fps implied by "two seconds (50 frames)") but does not say the features are released; its data are available "upon request from the authors". Getting AUs would mean downloading the video and running our own extractor, which the feature-only rule forbids.

## License / terms (EULA, exact)
- "released ... under specific conditions for sole purposes of scientific, non-commercial use."
- 1. "The user may not use the database for any commercial purposes."
- 2. "The signee of this document must hold a permanent position at an academic or publicly funded research institute."
- 3. "The user may not distribute the database in any way."
- 6. "Any models derived using data from the dataset may only be used for scientific, non-commercial applications."
- Per-participant consent flags ("Disseminate", "Public") restrict screenshots and use outside the consortium.
- This license restricts use: non-commercial only, and the signer must hold a permanent academic post. Whether the project qualifies is an operator decision.

## Access route
Sign the EULA, create an account, and email the signed PDF to noxi@hcai.eu. NoXi+J: email noxi+j@hcai.eu.

## Size and runs on this Mac without a GPU?
Size not stated in what I read. The data are raw Kinect video and audio, so use would require local face tracking (CPU-feasible with OpenFace or MediaPipe, but it breaks the feature-only rule).

## Verdict: reject
- No released per-frame facial features; video-only access conflicts with the project's no-raw-video rule.
- The EULA signer requirement (permanent academic position) and non-commercial model clause probably exclude this project; operator decision if reconsidered.
- The asymmetric expert-novice role is a confound for a symmetric contingency test.
