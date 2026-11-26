# The inhibition of automatic imitation: a meta-analysis and synthesis of fMRI studies (Darda & Ramsey)

Kohinoor M. Darda & Richard Ramsey, *NeuroImage* 197:320–329, 2019, doi:10.1016/j.neuroimage.2019.04.059. Read as the bioRxiv preprint, 10.1101/334938 v3. Data and code: osf.io/dbuwr.

## What was read
The full text of bioRxiv v3 (HTML): abstract, Introduction, Methods, Results, Discussion, Limitations, Theoretical implications and Conclusion. Tables 1–3 (study list, contrasts, cluster coordinates) are images or pop-ups and were **not** seen, so no coordinates are given here. The published NeuroImage version may differ in wording.

## The computation, precisely
**Framing.** "Imitation control can be divided into at least two component processes – action representation and action selection." The paper asks only which network does *selection*: the theory-of-mind network (mPFC, rTPJ: the "specialist" view of Brass et al. 2009, in which "the rTPJ distinguishes between self- and other-generated actions, and the mPFC enforces the self-generated action") or the domain-general multiple-demand (MD) network.

**Method.** MKDA (Wager et al. 2007): 10 mm kernels, weighted by √n and by random vs fixed effects, 5000 Monte Carlo iterations, FWE height and extent thresholds. **12 studies, 300 participants**, 13 contrasts / 142 foci for the general compatibility effect. Exploratory: 4 contrasts (42 foci) for spatial, **3 contrasts (20 foci) for imitative compatibility**. Brass 2009 was excluded (no whole-brain coordinates).

**Results.**
- General compatibility: right IPL, supramarginal gyrus, STG and rTPJ (height and extent p < .001); right SFG and MFG; bilateral insula (extent only); right IFG (lenient extent only).
- Imitative compatibility: left IPL, right IPL. Spatial: left IPL, right SFG.
- "For all compatibility types ... all regions that passed height or extent-based thresholding overlapped with regions in the MD network." One general-compatibility cluster also overlapped rTPJ. "**There was no overlap with the mPFC node of the ToM network for any compatibility type.**"
- Unthresholded indicator maps: general and **spatial** compatibility overlap the rTPJ mask; **imitative compatibility does not**.
- Descriptively, "only 28.6% of fMRI studies on imitation control to date (4/14)" report rTPJ, all with n of 10–20.

**The authors' stated caveats.** Few imitative-only contrasts (n = 3). The MD mask is larger than the ToM mask. fMRI conflicts with stimulation studies (Sowden & Catmur; Hogeveen) that do implicate rTPJ. mPFC "has been demonstrated to exert a top-down influence during modulation of imitation via direct gaze (Wang et al., 2011)", so mPFC/rTPJ "may play a regulatory role ... without being directly engaged".

**Proposed architecture (their Figure 1, conclusion):** domain-specific *input* (face, body, biological motion, mirror system) feeding a domain-general *selection* mechanism. "Although the perceptual input is social, a domain-general selection mechanism may still operate." They cite Heyes's 2011 dual-route model, in which imitation control needs no self–other distinction, and Cooper et al. 2012 (imitative and spatial compatibility from one dual-route model with different input nodes).

## What it means for the designs
- **Selection is ordinary.** The reliable neural signature of resolving "the partner's movement conflicts with my intention" is the generic conflict and selection machinery. A design needs no dedicated anti-copy inhibitor. It needs (a) the other-derived activation to be *represented as distinct* (input specificity) and (b) ordinary competitive selection in favour of the agent's own intention.
- **The weak point of a selection-only guard.** Selection resists the mirrored input only when an own intention is active and in conflict. With no competing intention (an idle face), nothing selects against the mirrored activation. My inference, not the authors': **the guard is weakest when the agent is idle**, the state in which avatars most often copy. A design must keep an own intention always present (a set-point face, rhythms, homeostatic tone).
- **Where the self/other tag lives is open.** Stimulation evidence puts it in rTPJ; fMRI does not. For the design this does not matter: the tag can be a learned input feature (Cooper's "different input nodes"). What matters is that it exists before selection.
- **Time scale:** within trial.

## Verdict
**adopt (as a constraint).** Build attribution as an input property plus generic selection, not a special inhibitor, and guarantee an own intention to select for. The imitative-only analysis rests on 3 studies.
