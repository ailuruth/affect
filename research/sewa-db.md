# SEWA DB (Kossaifi et al., IEEE TPAMI, online 2019; arXiv 1901.02839)

Sources read: arXiv 1901.02839 full PDF (sections 1, 3 and 3.3, via text extraction); iBUG resource page (ibug.doc.ic.ac.uk/resources/sewa-database/); sewaproject.eu/resources. The database site named in the paper, http://db.sewaproject.eu/, returned HTTP 404 on 2026-11-25, so I could not read its EULA or terms.

## What it contains
- 398 subjects (iBUG page: 408) from six cultures (British, German, Hungarian, Serbian, Greek, Chinese), 198 successful sessions, recorded on participants' own computers via WebRTC/OpenTok.
- Two parts per pair: four advert-watching clips each (1,600 min in total) and one video chat discussing the last advert (1,057 min in total; "On average, the recorded conversation was 3 minutes long").
- Pairs are familiar by design: "participants within each pair were required to know each other personally in advance of the experiment"; familiarity was recorded in the sign-up questionnaire. Each pair has one chat; no repeat sessions.
- Video 320x240 to 640x360, "frame rate is between 20 and 30 fps"; audio 44.1 or 48 kHz.
- Annotations: facial landmarks, acoustic LLDs, hand and head gestures, AUs, transcripts with non-verbal cues, continuous valence/arousal/liking (human raters), agreement/disagreement and mimicry episodes.

## Per-frame facial features?
Partly, and only on small subsets.
- Landmarks: 49-point, for the 538 short (10-30 s) segments of the "basic SEWA dataset", obtained by tracking (Chehra) plus manual correction.
- AUs: semi-automatic annotation of AU1, AU2, AU4, AU12 and AU17 on "500 sequences (150 frames each)" (the SEWA AU dataset); "the AU annotation is not exhaustive, meaning that some AU activations may be missed". I saw no statement that AU intensities were released for whole conversations.
- Full conversations of both partners with per-frame AUs: not described.

## License / terms
Not seen. sewaproject.eu says only that the database "is released ... for research purposes". The iBUG page states no license. The EULA page is offline, so the terms are unknown. If access is restored, the operator would need to review the terms.

## Access route
Paper and project page point to http://db.sewaproject.eu/ (404 today). No other mirror found.

## Size and runs on this Mac without a GPU?
Feature annotations would be small; the full corpus size is not stated. Any per-frame AUs beyond the 500-sequence subset would need our own extraction from video, which the feature-only rule forbids.

## Verdict: reject
- Access route is dead and the terms are unreadable.
- Per-frame AUs cover only 500 × 150-frame clips, and the conversations are about 3 minutes, one per pair. That is too short for windowed synchrony with surrogates (moulder-2018-synchrony-surrogates.md wants at least 500 samples per window set).
- Its one advantage, familiar pairs across six cultures, is covered by Seamless naturalistic (`relationship` = `familiar`).
