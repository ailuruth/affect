# Mauersberger, Kastendieck, Hetmann, Schöll & Hess 2022, "The different shades of laughter: when do we laugh and when do we mimic other's laughter?" (Philosophical Transactions of the Royal Society B 377:20210188, doi 10.1098/rstb.2021.0188)

Source read: full article PDF (author-hosted, ursulakhess.com/resources/MKHSH22.pdf): introduction, method, results text, discussion. I could not cleanly extract the numbers in Table 1 and Figures 1-2 from the PDF text layer, so no coefficients are quoted below.

## Claims
- The same, morphologically identical laughter is mimicked or not depending on what the laugher is laughing at. Laughter after funny scenes was judged most appropriate, produced most closeness and most mimicry; laughter after schadenfreude scenes less; after disgust scenes least.
- Appropriateness and perceived closeness (and individual differences such as trait schadenfreude) explain laughter mimicry within each scene type.
- Mimicry "occurred within the first second" of the reaction video, even though the context had to be remembered from a scene seen seconds to minutes earlier. "laughter in response to disgust scenes was not commonly mimicked, whereas almost every single participant mimicked laughter in response to funny scenes."
- Mimicking someone's schadenfreude laughter affiliates with the laugher and signals exclusion of the target.

## Evidence
- Online, pre-registered (OSF sge8n), Prolific UK, N = 329 (final 309-326 depending on dataset), mean age 35.4.
- Participants watched funny, schadenfreude and disgust clips (5-15 s), then three "reactions" per scene from a laughter database (laughter, smile or neutral; mean 4.63 s), presented as people who had watched the same scene. No sound.
- Webcam video analysed with OpenFace 2.0, frames with detection confidence below 75% dropped; positive pattern score = mean(AU12, AU6) minus AU4, baseline-corrected against a 1.5 s fixation; reaction videos binned in 500 ms intervals. Linear mixed models and mediation models.

## What it implies for the design
- Direct evidence that identical partner input should produce different agent output depending on the agent's appraisal of the partner's reason for the expression. A map from partner face to agent face cannot be a function of the partner's face alone; it needs the shared context as an input.
- The method is close to what this project can run: webcam, OpenFace AU12, AU6 and AU4, 500 ms bins, a positive-pattern contrast. It shows context effects large enough to see without EMG, within the first second.
- Limits: not a live interaction (recorded reactions), no audio, OpenFace cannot separate laughing from smiling, and the "partner" is a stranger on video.

## Verdict: adopt (as evidence that meaning, not morphology, sets the response; and as a webcam-feasible protocol)
