# CANDOR corpus (Reece, Cooney et al., Science Advances 9(13) eadf3197, 2023)

Sources read: full paper (NSF PAR author copy, par.nsf.gov/servlets/purl/10557357); Hugging Face dataset card for `betterup/candor-tabular` (v1.1, November 2026) including the full "CANDOR Corpus License, Version 2.2"; HF file listings and gating metadata for `betterup/candor-tabular`, `betterup/candor-processed` and `betterup/candor-raw`; the BetterUp request page; the TalkBank CABank CANDOR page. I did not request access, so I have not seen the data dictionary (`docs/data_dictionary/audio_video_features.csv`) or any data file. I did not read the Supplementary Materials.

## What it contains
- 1,656 unscripted dyadic conversations over video chat (TokBox OpenTok), recorded in 2020, US adults recruited through Prolific. Card: "1,656 conversations among 1,460 participants, about 860 hours", "median length of 29 minutes"; paper: "1456 unique participants", 850+ hours. Prompt: "just imagine you have met someone at a social event and you're getting to know each other."
- Partners: always strangers (paper: participants confirmed they were "comfortable having a recorded conversation with a stranger"; card: "pairs of strangers"). Repeat participants, not repeat partners: "more than 50% of our sample had more than two conversations and 33% had more than three conversations. Participants who had multiple conversations did not do so back-to-back". Unmatched participants were paired by availability; a participant whose call failed could "reschedule with a new partner". I found no statement that any pair met twice. TalkBank: "the 0speakers.csv file that lists the conversations in which each speaker participated".
- Transcripts (v1.1): four turn models (Audiophile, Cliffhanger, Backbiter, NaturalTurn), columns include `turn_id`, `speaker`, `start`, `stop` ("Seconds from the start of the recording"), `pause`, `overlap`; per-word confidence from a 2024 AWS Transcribe pass.
- Per-second audio and video features: `features/audio_video_features.parquet`, "one row per participant per second: 7,118,942 rows". Video columns named on the card: `gaze_on`, `smile`, `nod_yes`, `nod_no` ("the maximum of a detector's output within the second") and eight `prob_face_*` columns ("the mean of a facial-expression model's probabilities across the second"). Paper: nods from Dlib landmarks and a rule-based detector; facial expression from "an emotion recognition model pretrained on the AffectNet corpus ... eight emotional groups", "For every second". Acoustic: `log_energy`, `intensity` ("a classifier's probability that the speech in that second is emotionally intense. It is not loudness"), others as 1-s means of 10-ms measurements.
- Surveys: pre/post conversation, per participant per conversation (3,312 rows), including partner impressions and personality.
- Known timing issues (card): v1.0 video features were shifted late; v1.1 corrects this, but "Video timing is accurate to about one second"; 75 recordings have video features that stop early.

## Per-frame facial features?
No. Facial features are per second, and they are detector maxima (`smile`, `gaze_on`, nods) or classifier outputs (`prob_face_*`, an emotion classifier, which we must not read, same rule as Seamless `emotion_scores`). No action units. Per-frame AUs would require downloading the processed video (about 350 GB) and running our own extractor, which the project's feature-only rule forbids.

## License and terms (exact)
- Paper: the article is CC BY-NC 4.0; that covers the article, not the corpus.
- Corpus: "Access to the CANDOR Corpus is governed by the CANDOR Corpus License, Version 2.2." Clause 2: "a worldwide, royalty-free, non-exclusive, non-transferable license to use the CANDOR Corpus for any lawful purpose, including research, development, and commercial purposes, subject to these terms."
- Restrictions: 3(a) "you may not redistribute, republish, sublicense, or relicense any part of the CANDOR Corpus"; 3(e) Derivatives may be created and used but not shared "without BetterUp's written permission"; 3(b)(iii) allows sharing "aggregate statistics and research findings that do not reproduce the CANDOR Corpus or identify any Participant"; 5(b) "You may not link any Participant to data outside the CANDOR Corpus"; 6(a) no "face prints, voiceprints, or other biometric identifiers"; 6(b) "General modeling of facial expression, speech, voice characteristics, and behavior is permitted, as long as it does not identify any Participant"; 8(b) "Within 30 days after BetterUp lists a removal in the removals log, you must delete all copies of the Removed Material"; termination on breach requires deleting all copies.
- This license restricts use (no redistribution, mandatory deletions, gated access with personal details). Adopting it is an operator decision.

## Access route
Gated Hugging Face repositories (`gated: manual`), reviewed by BetterUp "usually within a few days". The request form asks for full name, email, institution, country, and a 3-5 sentence description of intended use. That sends identifying information to a third party, so only the operator can submit it. Flavors: Tabular (no media) about 11 GB; Processed about 350 GB; Raw about 950 GB. Approval opens all three. TalkBank also hosts a version after BetterUp approval.

## Size and runs on this Mac without a GPU?
Tabular flavor: about 11 GB of parquet/CSV; per-second features are 7.1 M rows, which pandas handles on CPU. Nothing needs a GPU. The media flavors are out of scope.

## Verdict: watch
- Useful for turn timing (gaps, overlaps, backchannels) and per-second smile/nod/gaze contingency between strangers at scale, with a within-person repeat across different partners.
- Not a source of per-frame AUs; `prob_face_*` and `intensity` are classifier outputs and must be excluded at load like Seamless's emotion fields. No familiar pairs and no repeat partners.
- Blocked until the operator decides on the gated request and the CANDOR Corpus License 2.2 terms.
