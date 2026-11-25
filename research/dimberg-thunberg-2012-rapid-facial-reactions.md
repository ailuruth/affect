# Dimberg & Thunberg 2012, "Empathy, emotional contagion, and rapid facial reactions to angry and happy facial expressions" (PsyCh Journal 1:118-127, doi 10.1002/pchj.4)

Source read: full article PDF (Uppsala reprint hosted on an Arizona course server), all sections. This is the most recent primary paper from Dimberg's lab that I could read in full. I could NOT read Dimberg 1982 (Psychophysiology 19:643-647), Dimberg & Thunberg 1998 (Scand J Psychol 39:39-45) or Dimberg, Thunberg & Elmehed 2000 (Psychol Sci 11:86-89); everything below about those three is what this paper says about them, not what they say.

## Claims
- Rapid facial mimicry: viewers respond to happy faces with zygomaticus major (smile) activity and to angry faces with corrugator supercilii (brow) activity within the first second.
- Earlier work used "longer stimulus intervals (5-8 s)", but "distinct facial reactions can be evoked as early as after 400-500 ms of exposure to happy and angry facial stimuli (e.g. Dimberg, 1997; Dimberg & Thunberg, 1998; Dimberg, Thunberg, & Elmehed, 2000)".
- The effect held only in the high-empathy group; "The low empathy participants, in contrast, did not differentiate between the happy and angry stimuli with either facial muscles or in their self experience of emotion."

## Evidence
- N = 96 Uppsala students; the 24 highest- and lowest-scoring men and women on the QMEE empathy scale. Ekman & Friesen pictures, "six consecutive presentations of one slide of an angry face and one slide of a happy face"; intertrial intervals 25-35 s. Cover story: "sweat gland activity" was being measured.
- Recording: Ag/AgCl miniature electrodes "bipolarly attached to the left and right zygomatic and corrugator muscle regions (Fridlund & Cacioppo, 1986)"; "band pass filtered from 10 Hz to 1,000 Hz"; "contour-following integrators with a time constant of 20 ms"; "sampling frequency of 100 Hz".
- Scoring: "scored and averaged in 100-ms intervals during the first second after stimulus onset. The facial reactions were expressed as the change in activity in microvolts from the prestimulus level, which was defined as the mean activity during the last second before stimulus onset."
- What counts as mimicry: the differential response. "a sensitive and probably an optimal measure ... is to compare the zygomatic response to happy faces with the response to an angry control stimulus", and likewise corrugator to angry versus a happy control.
- Two windows: "0-500 ms and 500-1,000 ms". The corrugator's early rise in the first 100-ms bins "does not differentiate between the emotional content" and is read as "an eye movement or a startle reaction"; "the most clear-cut difference between the stimuli appears after 500 ms".
- Statistics: per-muscle ANOVAs, Group (between) x Emotion (within), trials collapsed over the six presentations and both sides of the face; Geisser-Greenhouse conservative df (1, n-1); planned "Bonferroni's t-test" per 100-ms bin.
- Results: 500-1,000 ms zygomatic Emotion F(1, 94) = 4.58, p < .05, Group x Emotion F(1, 94) = 5.13, p < .05; high-empathy group separated happy from angry "as early as during the 400-500-ms interval". Corrugator 500-1,000 ms Emotion F(1, 94) = 9.31, p < .01, Group x Emotion F(1, 94) = 4.52, p < .05; high-empathy separation "as early as during the 300-400-ms interval".

## License
Journal article, (c) 2012 Institute of Psychology, CAS and Blackwell. No code or data.

## Runs on this Mac without a GPU?
The analysis is trivial. The instrument is not on this Mac: it needs a surface-EMG amplifier (10-1,000 Hz band, so at least 2 kHz raw sampling) and Ag/AgCl electrodes.

## Verdict: adopt (as the definition of a mimicry effect and its scoring)
- Mimicry effect = a larger zygomatic change from a 1-s pre-onset baseline to the agent's smile than to its frown, and the reverse for corrugator, in the 500-1,000 ms window (100-ms bins), within subject. A rise that does not differ between expressions is not mimicry.
- The effect is microvolt-scale and was absent in low-empathy viewers, so a null in a small or unselected sample is weak evidence. Camera AU coders were not used here and are not validated at this amplitude (my inference, not the paper's).
- The agent's expression onset must be time-stamped to at least 100 ms resolution for this scoring to apply.
