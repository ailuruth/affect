# Hasson & Frith 2016, "Mirroring and beyond: coupled dynamics as a generalized framework for modelling social interactions" (Phil Trans R Soc B 371:20150366, doi 10.1098/rstb.2015.0366)

Source read, 2026-11-25: the full text (PMC4843605, CC BY 4.0) via the Europe PMC full-text XML service. All sections were read; figure images were not seen, only their captions. The reference list was not read. This is a perspective piece. Its data are the authors' earlier fMRI work and others' behavioural studies, cited and not re-analysed. Stephens, Silbert & Hasson 2010 and Konvalinka et al. 2010 were not read here, only as reported.

## Claims
- **Mirroring is one special case of coupling.** "we need to go beyond simple, symmetric (mirror) alignment once we start interacting. Interactions are dynamic processes, which involve continuous mutual adaptation, development of complementary behaviour and division of labour such as leader–follower roles."
- **Neural coupling, defined.** It denotes "neural processes that have lawful relationship across the sender's and receiver's brains. This can include correlated activity (neural alignment), as well as complementary actions and other lawful transformations".
- **Three forms of coupling** (final section):
  - "(i) alignment, when the receiver's neural patterns match those of the sender";
  - "(ii) conditional transformations, when the receiver's patterns reflect a predictable relation to the sender's neural patterns";
  - "(iii) synergies, when the activities of the two brains dynamically influence and constrain each other to optimize information sharing."
- **Synchrony is not interaction.**
  - Two players driven by a common metronome can be "highly synchronized" with "no exchange of information".
  - A one-way leader→follower chain is also synchronized. So "synchronized behaviour is not a necessary marker of two-way social interaction."
  - "phase synchrony may reflect a common driving signal rather than brain-to-brain coupling", and "this measure will not pick-up complementary behaviour."
- **Too much alignment hurts.**
  - It causes information cascades ("folly of crowds").
  - It causes automatic mirroring in rock–paper–scissors, which "prevents players from achieving optimal performance".
  - Prior rhythmic priming that facilitates motor coupling "can impede attainment of the dynamic coordination needed for joint task performance".
  - "for many tasks, the appropriate actions for the individuals in the group should be complementary rather than aligned."
- **Leadership.**
  - Leaders are those who adapt less, or who decide earlier.
  - Division of labour produces roles: one partner keeps the beat, the other keeps the synchrony.
  - Task asymmetry assigns roles: in Vesper et al.'s jumping task, the partner with the easier jump "took on a follower role and did all the adapting".
- **Hierarchy of time scales.** More abstract representations have longer integration windows. "the exact form of this coupling is likely to be different for different levels". There may be mirroring at the top (shared meaning) and synergy below, such as rephrasing to check understanding.

## Evidence (as reported in this paper)
- **Speaker–listener fMRI** (Stephens et al. 2010; Silbert et al.). The speaker was scanned telling a story, and listeners were later scanned hearing the recording.
  - "the listener's brain activity mirrors that of the speaker with a typical delay of 3 s".
  - The coupling "was eliminated when the communication signals were misaligned".
  - "The strength of mirroring was positively correlated with story comprehension."
  - No r values or n are given in this paper.
- **Cross-language ISC.** Russian and English listeners hearing the same story share high-order responses, and a shared interpretation raises inter-subject similarity.
- **Synchronized tapping** (Konvalinka et al.).
  - The cross-correlation of inter-tap intervals is "typically negative" at lag 0 and positive at lag ±1: each partner corrects toward the other's previous interval.
  - The asymmetry between lag +1 and lag −1 shows who adapts more (the follower).
  - In EEG, frontal alpha was reduced only in the leader (the partner who adapted less).
- **String quartet** (Wing et al.). In one of two professional quartets, the first violin led: the others adapted to her more than she did to them.
- **Group benefit.** Aligning confidence vocabulary lets a pair beat its best member (Bahrami et al.). Pigeon pairs and fish shoals do better than individuals.

## Formal models
No equations. The tools proposed are:
- inter-subject correlation (ISC), including lagged speaker→listener ISC, for alignment;
- lagged cross-correlation of interval series, with the lag ±1 asymmetry as a directional leader/follower index;
- inter-subject mutual information and transfer entropy for "conditional transformations";
- for synergy, centre-manifold theory and the "segregation versus coupling" tension (citing Tognoli & Kelso);
- hierarchical Bayesian models of mutual inference. The recursive "model of me in you" regress "dissolves once both brains have a common model for predicting each other's behaviour."

The authors' own conclusion: "So far, we have only sketches of the underlying mechanisms."

## What it implies for a dyadic affective core
- **The coupling space has at least three kinds.** The project's one-gain sketches all live in kind (i), alignment: the partner's state is copied with a gain and a lag.
  - Kind (ii), conditional transformation, is a lawful map that is not identity. Threat in one face predicts fear, not threat, in the other. That is a matrix with off-diagonal and sign-flipped entries, not a scalar.
  - Kind (iii), synergy, is mutual constraint toward a joint function.
- **Two-way adaptation creates the tapping signature, and a copier cannot.** Mutual error correction gives negative lag-0 and positive lag-1 correlation. A Bot that only copies with a delay gives positive correlation at the copy lag and nothing negative. A Bot whose partner-gain runs to 1 tracks the partner and stops correcting.
  - Directional asymmetry (lag +1 vs −1) gives a leader/follower index that the dyad negotiates.
  - The index changes with task asymmetry, a role-dependent coupling that one fixed gain cannot represent.
- **Leader and follower are states of the dyad, not traits of the gain.** Who follows depends on task difficulty and division of labour. A dyadic core should be able to occupy either role and switch between them. Under a symmetric scalar coupling, the asymmetry comes only from the two agents' own gains, so it cannot change with context.
- **Per-level coupling on different time scales.** Mirroring may belong at the slow, high level (shared appraisal or meaning) while fast levels are complementary. A single time constant and a single gain cannot express this split.
- **Measurement constraint.** Synchrony against shuffles does not show interaction (common drive, one-way drive). This matches the project's adoption of transfer entropy with its caveats (Schreiber; James et al. 2016) and the surrogate rules (Moulder 2018).
- **Not shown.**
  - No affect data. The tapping and quartet results are timing only, and the fMRI is one-way (recorded speaker, so no feedback).
  - The three-way taxonomy is a proposal; no study here separates (ii) from (iii) quantitatively.

## Verdict: adopt (as the framing and the tapping/lag-asymmetry signature)
- It is open access, short, and states the alignment / transformation / synergy split that the "not one gain" target needs.
- The negative lag-0, positive lag-±1 pattern, with its asymmetry, is a concrete human signature that a delayed copier fails. It can be computed on Seamless AU or prosody interval series under the existing surrogate rules.
- It provides no mechanism, so it does not serve Principle 10 directly.
