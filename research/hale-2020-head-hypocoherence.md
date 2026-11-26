# Are you on my wavelength? Interpersonal coordination in dyadic conversations (Hale, Ward et al.)

Joanna Hale, Jamie A. Ward, Francesco Buccheri, Dominic Oliver & Antonia F. de C. Hamilton, *Journal of Nonverbal Behavior* 44(1):63–83, 2020 (online 2019), doi:10.1007/s10919-019-00320-3 (PMC7054373). Pre-registered (Hale & Hamilton 2016).

## What was read
The full PMC open-access text: abstract, introduction, background, methods (participants, setup, procedure, preprocessing, wavelet coherence, pseudo-trial construction), all results, discussion, limitations and future directions. Figure captions were read; figures and the supplementary PDF (fast-nod detector details, monologue/dialogue split, roll/yaw plots) were not seen. Statements below that cite "Figure S1" come from the main text's description of it.

## Findings, precisely

**Design.** 31 dyads recruited, 26 analysed after pre-registered exclusions (strangers; 34 F, 18 M; mean age 22.3). Seated ~1.5 m apart. 16 trials of 90 s each: 30 s monologue (Leader describes a picture, Follower silent), then 60 s free dialogue; roles alternate. Polhemus magnetic sensors on forehead and upper back at 60 Hz. Pre-registered analysis: head **pitch** (nodding) only.

**Chance baseline — the strict one.** Pseudo-trials pair trial *i* of a dyad with trial *j* of the **same dyad with the same Leader/Follower assignment**. So the baseline keeps the people, the roles, the task and the spectral power, and removes only the live coupling. Coherence (Grinsted toolbox, Morlet w = 6, cone of influence removed) averaged over time into 89 bins over 0.2–8 Hz; real vs pseudo by paired t-test per bin, FDR-corrected.

**Two bands, opposite signs.**
- **0.2–1.1 Hz (periods ~1–5 s): coherence above chance.** Present in monologue and dialogue alike. Not seen for roll or yaw at low frequency (pitch only).
- **2.6–6.5 Hz (periods ~0.15–0.4 s): coherence below chance ("hypo-coherence").** Replicated from the pilot (n = 20) in the pre-registered sample; also present in roll and yaw (exploratory). Not explained by global power differences between partners (Figure S1, as described). Reliable in dialogue; "only weakly present" in monologue, with no significant monologue–dialogue difference (less data in monologue).
- The authors stress what below-chance coherence means for wavelets: coherence is high when both signals have energy at the same frequency regardless of phase, so hypo-coherence means **the two people move at different frequencies** — "not the same as anti-phase coherence".

**The low band is a reactive copy with a constant lag, not a phase lock.**
- Leader→Follower cross-correlation over ±4 s: real > pseudo from −3 s to +0.8 s, peak at **−0.63 s** (Follower follows Leader by ~600 ms).
- Phase analysis: excess coherence at 0.2–0.5 Hz with the Follower **30–90° behind** the Leader.
- Model comparison on the phase–frequency map (0.15–0.9 Hz): a **constant-delay** model beat a constant-phase model on RMSE; fitted delay **0.588 s**.
- Little evidence of the 2–10 s "behavioural mimicry" lags of earlier video studies (the slowest is ~2 s, at 0.2 Hz and 90°); the authors note 90-s trials could miss longer lags.

**The high band is a role-locked complementary signal: fast nods by the listener.**
- A zero-crossing detector coded each 1-s window as containing a fast nod (2.6–6.5 Hz) or not.
- Followers fast-nodded during **22%** of the trial vs Leaders **10%** (t(25) = 5.83, p < .00001, d = 1.39). 67% of fast nods come from the person in the Follower role.
- Using audio (who is speaking), irrespective of role: people fast-nod more while their partner speaks (**17%** vs **11%** of time; t(23) = 4.08, p < .001, d = 0.84). Precision **94%**: if one person is fast-nodding, the other is almost always speaking.
- Authors: "fast-nodding is a complementary action, which is performed by one member of a dyad when the other performs something different"; small, quick, at about speech frequency, probably not under voluntary control and not consciously noticed (untested).

**Limitations stated.** One task (structured picture description), head pitch only, 90-s trials, no analysis of liking (underpowered), strangers only.

## What it means for the designs
1. **Copying and non-copying coexist in one channel, separated by frequency.** The same head-pitch signal carries a positive, lagged coupling at 0.2–1.1 Hz and a **below-chance** coupling at 2.6–6.5 Hz. A design whose partner→self map has one sign per channel cannot produce this. Required property: the cross-spectrum between the agent's and partner's output must be **band-signed** — above a matched surrogate in a slow band, below it in a fast band — in the same channel at the same time.
2. **Below chance is the target, not zero.** The strict within-dyad, within-role surrogate makes "below chance" a measurable test: the agent's fast-band head motion must have *lower* coherence with the real partner than with the same partner's other trials. A model that merely ignores the partner at high frequency scores at chance and fails.
3. **The divergence is a role-gated complement, not noise.** Fast nodding is switched on by the *partner's* speaking (94% precision). The required structure is a conditional: partner state (speaking) → own output in a band and form the partner is *not* using. This is the sign-depends-on-role property: the same partner input (voice activity) drives a non-matching motor pattern in the listener and nothing in the speaker.
4. **The slow coupling is a fixed delay (~0.6 s), not a phase relation.** A constant-lag reactive path fits better than a phase oscillator. For a design this argues against a Kuramoto-style phase coupling as the source of head matching, and for a delayed, lagged response whose delay does not scale with movement frequency. It also places the matching component at the timescale of the fast matching route of Principle 3 (cf. Hale & Hamilton 2016: mimicry at 1 s was detected by 30.5% of people vs 3.8% at 3 s).
5. **Time scales:** matching ≈ 0.6 s lag on 1–5 s movements; divergence on 0.15–0.4 s movements; both hold over 90-s exchanges. No evidence here about minutes or sessions.

## Verdict
**adopt** — the cleanest quantitative signature of non-copying in a nonverbal channel: same channel, two frequency bands, opposite signs against a strict surrogate, with the fast band set by the partner's speaking state. Pre-registered and replicated across pilot and main samples; head pitch only, one task, strangers.
