# Breazeal 2003, "Emotion and sociable humanoid robots" (Kismet)

Cynthia Breazeal, *International Journal of Human-Computer Studies* 59(1–2):119–155, 2003, doi:10.1016/S1071-5819(03)00018-1.

Source read: the author's preprint ("Preprint submitted to Elsevier Science 3 November 2002", 42 pages), linked from her MIT Media Lab publications page as `Breazeal-ijhcs02-final.pdf`. The PDF uses Type 3 fonts with no text layer, so I rendered every page and ran OCR (tesseract). I read all 42 pages, including tables, captions and references. The OCR garbled some table cells and the subscripts in the equations. I rebuilt the equations from the surrounding prose and say below where a number is reconstructed. The published journal version was not read. The behavior system and the affective-intent speech recognizer are described only in other papers (Breazeal 2002 book; Breazeal & Aryananda 2002), which I did not read.

## Claims
- A robot can regulate face-to-face interaction with a person using drives, emotions and expressions modeled on ethology and emotion theory. The person reads the robot's face and adjusts the stimulus (type and intensity) until the robot's drives are back in their homeostatic range. The result is a "mutually regulated" exchange.
- One three-dimensional "affect space", arousal, valence and stance [A, V, S], serves as a "common currency". The same space is used to appraise inputs (releasers), to select an emotion and to generate the facial expression.
- Adding a third dimension, stance (approach versus withdraw), separates anger from fear and allows expressions such as a sly grin. On a valence–arousal plane alone, anger and fear sit close together.
- Naive people can read Kismet's expressions well above chance.

## Architecture (as given)
Hardware: 21 DoF (3 gaze, 3 neck, 15 face: eyelids, eyebrows, lips, ears); four color CCD cameras (narrow field behind each pupil, two wide-field cameras between the eyes); two ear microphones, plus a lavalier microphone worn by the person.

Pipeline (Fig. 4): feature extractors (color, motion, pitch, skin tone, ...) → high-level perceptual system of **releasers** → **affective appraisal** (somatic-marker tagging) → **emotion elicitors** → **emotion activation** → **winner-take-all emotion arbitration** → expressive motor system (face, voice, posture) and behavior system.

- **Drives** (three: social, stimulation, fatigue). Each drive is a separate process with activation A_drive in [A_min, A_max]. It rises with time unless its satiatory stimulus is present at the right intensity. Large positive means under-stimulated; large negative means overwhelmed. There are three regimes, and each feeds a fixed affect tag:
  - homeostatic: positive valence, balanced arousal ("content");
  - under-stimulated: negative valence, low arousal ("bored", decaying to "sorrow");
  - overwhelmed: negative valence, high arousal ("distress").

  Fatigue triggers sleep, and sleep returns all drives to homeostasis. Drives act on a slower time scale and are said to make up "mood".
- **Releasers**: "each hand-crafted". A releaser fires when its perceptual and internal conditions exceed a threshold. It combines features with the active drive, the current affective state and the active behavior. Examples:
  - The same toy activates desired-toy if the stimulation drive is active, undesired-toy if the social drive is active, and threatening-toy if it is too close and too fast.
  - soothing-speech is active only if Kismet is already distressed. This is used to reduce confusion between the "soothing" and "neutral" classes of the speech classifier.
- **Somatic markers**: each active releaser gets designer-set tags A, V and S, each in [−1250, +1250], "fixed constants, or linearly varying quantities". For example, threatening-toy gets A = 1200, V = −1000, S = −1000. Praise gets positive V and slightly high A; scolding gets negative V and low A; attentional bids get medium A. Goal success gets positive V. Frustration gets negative V, with stance rising slowly over time so that the robot drifts toward anger.
- **Elicitors**: each emotion has an [A, V, S] region (Fig. 5). Its elicitor averages the tagged contributions that pass its per-dimension filter. Activation is how deeply the net point lies inside the region, scaled by region size. It is zero if any dimension is unrepresented; otherwise the A, V and S contributions are summed. An earlier version that averaged all inputs globally was dropped. With high fatigue (low arousal) and a threatening toy, it gave near-neutral arousal and no fear.
- **Emotion activation**: A_emotion = E_emotion + B_emotion + P_active − δ_t. Here E is the elicitor activation, B a per-emotion constant bias, P_active a persistence bonus while the emotion is active, and δ_t a decay back to baseline over seconds. All values are "determined empirically". There are nine emotion processes: joy, anger, disgust, fear, sorrow, surprise, interest, boredom, calm.
- **Arbitration**: winner-take-all. Each emotion has two thresholds, and the expression threshold is lower than the behavior threshold. The face therefore changes before the behavior does: a fearful face first, then escape (eyes closed, head turned away).
- **Expression**: the winner's net [A, V, S] point is sent to the motor system, which blends nine hand-designed basis postures:
  - P_net = C_arousal + C_valence + C_stance;
  - C_arousal = α P_high + (1−α) P_low;
  - C_valence = β P_positive + (1−β) P_negative;
  - C_stance = F(A,V,S,N) + (1−δ)(γ P_open + (1−γ) P_closed);
  - F = Σ_i f_i(A,V,S,N) P_i and δ = Σ_i f_i, for i ∈ {anger, fear, disgust}.

  Each f_i ∈ [0,1] decays linearly with distance from posture i's location, within radius N. The six axis prototypes map to surprise (high arousal), fatigue (low), content (positive), unhappy (negative), accepting (open) and stern (closed). Posture also follows arousal (erect versus slouch) and stance (lean forward versus shrink back).
- **Voice input**: a classifier labels the person's prosody as praise, prohibition, attentional bid, soothing or neutral (from Breazeal & Aryananda 2002). Each label feeds a releaser.

## Evidence with numbers
- **Static images**: 17 subjects (12 children about 12 years old, 5 adults), 7 photos, forced choice among 10 labels (chance 10%). Correct as printed: anger 76.5, disgust 70.6, fear 47.1, joy 82.4, sorrow 83.4, stern 53.8, surprise 82.4. Mean 70.9%. Fear was confused with joy and surprise; stern with anger and sorrow.
- **Video clips** of face and posture: 7 subjects (6 children, 1 adult), 7 labels (chance 14%). Anger, disgust, fear and sorrow were 86% each. The OCR garbled the joy, interest and surprise cells. From the reported mean of 77.6%, they sum to about 199; the row structure suggests joy 57, interest 71, surprise 71 (reconstructed). No statistics beyond "significantly above chance". The author notes the small n.
- **Live interaction** (from Breazeal & Aryananda 2002, summarized here): 5 female subjects aged 23–54, speaking 5 languages, conveyed praise, prohibition, attention and soothing. The results are qualitative only:
  - All subjects repeated and varied their prosody until the robot's expression changed, and exaggerated it when the wrong expression appeared.
  - Several felt "guilty" after a successful prohibition.
  - The paper reports an escalating "affective mirroring" loop. The subject lowered her head with each prohibition, the robot dipped further, and the loop continued "until it bottoms out" with both in mirrored dramatic postures.
- No quantitative measure of the live interaction is reported (no timing, no coupling statistic, no comparison condition).

## Failure modes (reported or evident)
- **Assembled modules, not one principle.** Drives, releasers, somatic markers, elicitors, emotion processes, a separate behavior system and a motor blender are each designed separately. They are linked by designer-set constants ("determined empirically"). The [A, V, S] "common currency" is a shared coordinate system, not an objective from which the parts follow.
- **Everything is hand-named and hand-tagged.** Nine named emotion processes come from Ekman, Izard and Plutchik. Releasers are "each hand-crafted", and every affect tag is set by the designer. Valence and arousal are inputs written into the tags, not read out of a learned state. This is the reverse of Principle 2.
- **Classifier on the partner.** The person's voice is reduced to five intent labels. The person's face is used only as a skin-tone or face percept; there is no reading of the partner's expression at all. This violates Principle 1, and the paper says so in its Future Work: "Currently, Kismet does not reason about the emotional state of others."
- **Expression mapping wired, not learned.** The nine basis postures and their locations in affect space were designed by hand. No self–other map exists, and no mimicry exists in the robot. The "affective mirroring" reported is the human mirroring Kismet.
- **No learning anywhere.** Learning from caregivers, social referencing and learning "the significance its actions and expressions have for others" are all listed as future work.
- **No persistence.** Emotions decay in seconds, and drives cycle and reset during sleep. Nothing carries over across sessions; no long-term state is described.
- **No ablations.** The one design comparison (global averaging versus the elicitor scheme) is reported as an anecdote from development, not as an experiment. The live evaluation has no control condition.
- **Winner-take-all by choice.** Only one emotion is expressed at a time ("by choice"). Blends come only from where that winner's [A, V, S] point falls.
- **Positive-feedback escalation.** The mirroring loop ran until both parties bottomed out. Nothing in the robot damps it, because the robot does not model the human.

## License
Elsevier journal article. The author preprint is hosted on the MIT Media Lab site. No code released.

## Runs on this Mac without a GPU?
n.a. There is no code; the architecture is small scalar arithmetic, but it depends on the physical robot and hand-tuned constants.

## Verdict: reject as architecture; adopt two mechanisms
Kismet is the canonical example of what Principle 10 names: a well-built assembly of hand-named parts, with no learning, no persistence and no ablation. Two mechanisms survive, restated as constraints on a single core rather than modules:
- **Two-sided drives.** Each drive has an under-stimulated regime and an overwhelmed regime, and staying in balance needs the right stimulus at the right intensity. This is satiable homeostasis with an upper bound, which fits Principle 6. It also rules out a "more contact is better" reward.
- **Expression leads action.** The expression threshold sits below the behavior threshold, so the face signals the coming act and lets the partner change course first. In the engine this should fall out of the dynamics: a faster, lower-gain face channel than the action channel. It should not be a second threshold added by hand.

## What it implies for this engine
- **Kismet confirms the prior-work gap the brief claims for assemblies.** A complete, published sociable-robot emotion system was evaluated only by label recognition of posed photos and videos (n = 17 and n = 7) and by qualitative anecdotes. A claim tested by ablation and by coupling measures on the human (S5) would be new against this baseline.
- **The parental-mirroring signal was already present, and nothing used it.** Kismet's subjects matched its posture and escalated with it. That is the contingent mirroring from which the engine is meant to learn its self–other face map. Breazeal's own future-work paragraph (citing Bullowa 1979) describes this: treat the robot as responsive before it is, so that "routine and predictable sequences" let it "learn the significance its actions and expressions have for others". She did not build it. The engine's learned map should be trained on exactly these episodes: the robot acts, and the partner reflects the act back with a lag.
- **Damping is needed.** The escalation loop shows that two mirroring agents without a model of each other drive each other to extremes. In a coupled-dynamics core, mirroring must be bounded by the agent's own homeostasis, for example as a satiable coupling term. Otherwise S5 contagion becomes runaway.
- **A three-dimensional affect space is too small and was hand-set.** Kismet needed a third axis (stance) just to keep anger and fear apart, plus three special-case postures for anger, fear and disgust. This is direct evidence for the brief's warning about low-dimensional cores: a few hand-named axes were not enough even for a hand-designed face.
- **Not to copy**: the classifier on the person's voice, the named emotion processes, the designer-set affect tags, and the winner-take-all emotion choice.
