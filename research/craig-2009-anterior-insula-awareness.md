# How do you feel — now? The anterior insula and human awareness

A. D. (Bud) Craig, *Nature Reviews Neuroscience* 10(1):59–70, 2009, doi:10.1038/nrn2555. Read from a copy in a Chilean university repository (repositorio.unab.cl). The live site sits behind a bot check, so I used the Internet Archive snapshot. I could not confirm that the copy was authorized. © Macmillan; quote sparingly.

## What was read
Extracted with pdftotext: the abstract, introduction, "The role of the AIC", the clinical observations, the model for awareness in the AIC, Box 2 (VENs) and Box 3 (forebrain asymmetry). I skimmed the long review of imaging studies by category (Table 1 and the category paragraphs) and did not read it in full. I did not read the supplementary table.

## Claims
- The AIC's "re-representation of interoception offers one possible basis for its involvement in all subjective feelings". "The accumulated evidence compels the hypothesis that the AIC engenders human awareness."
- **Model.**
  1. Lamina I and solitary-nucleus input gives a primary representation of the body's condition in the posterior insula.
  2. In the mid-insula this is integrated with emotionally salient exteroceptive input (amygdala, temporal pole) and an incentive or hedonic signal from the ventral striatum.
  3. Integration "culminates in a unified final meta-representation of the 'global emotional moment'" in the AIC and frontal operculum. Craig calls this "the sentient self at one moment in time".
- **Salience** is "determined by its significance for the maintenance and advancement of the individual and the species", which at base means "the energy-efficient maintenance of the health of the physical body ... homeostasis".
- **Time.** Global emotional moments are repeated meta-representations "indexed by an endogenous timebase". This gives continuity over "a finite present". Craig says there must be **storage buffers** that let present, past and anticipated feelings be compared. "The anticipatory global emotional moments must be influenced by stored representations of expectations ... of one's own and others' behaviour."
- **Evolutionary function.** Each stage of integration improved "emotional communication between conspecifics".
- **Asymmetry (Box 3).**
  - The right forebrain is tied to energy expenditure, sympathetic activity, arousal, withdrawal and individual (survival) emotions.
  - The left is tied to energy nourishment, parasympathetic activity, approach and affiliative emotions.
  - The two are coordinated "opponency", like the sympathetic and parasympathetic control of the heart. Positive emotion can block negative and vice versa.

## Evidence
- A very broad imaging literature: interoception, heartbeat awareness (right AIC), pain, empathy, music, time estimation, risk prediction and its error, the feeling of knowing, error awareness, and self-recognition.
- **Clinical:**
  - anosognosia with mid-insula damage;
  - frontotemporal dementia, where loss of emotional self-awareness goes with degeneration of von Economo neurons (Seeley et al.);
  - anergia after AIC infarcts.
- Craig concedes that "the localization of awareness ... in a single substrate might seem unlikely".

## Mechanistic commitments
1. **Hierarchical re-representation** of body state, integrated in stages with exteroceptive salience and hedonic incentive.
2. **A single integrated snapshot** of the self per time step: a global summary vector.
3. **A buffer of recent snapshots plus predicted future ones**, with a comparator.
4. **Opponent energy-budget axes** (expenditure versus nourishment) as the root of valence and arousal.

## What it implies for a single formal core
Craig's integrated snapshot plus buffer maps directly onto a filtered state $h_t$ with a short history and a predicted next state. In that form it is a property of any recurrent latent with a predictive head, so nothing new is needed.

What he adds is the **comparator between felt-now and felt-predicted**. That is a temporal-difference signal on the agent's own state, and it ties in with Hesp et al.'s affective charge (hesp-2021-deeply-felt-affect.md).

His opponent-energy reading of valence suggests that the core's valence readout should line up with the sign of predicted net energy change (expenditure versus replenishment). That is a check on whether valence came out right, not something to build in.

The claim that the AIC is **necessary** for awareness is disputed directly by Damasio & Carvalho 2013 (Patient B) and by Barrett & Simmons 2015 (Roger and Boswell, degeneracy). For the engine this becomes an architectural question: does the core have one integration bottleneck, or several paths that can stand in for each other?

## What an ablation could separate
- **Buffer and comparator.** Remove the agent's memory of its own recent state (the history of $h$) while keeping $h$. Felt-now against felt-predicted signals should then disappear: no relief when a predicted bad state does not arrive, and no disappointment. Present-moment valence should still be there.
- **Opponency.** Collapse the two energy axes into one bipolar variable. Craig predicts that mixed states (simultaneous approach and withdrawal) and mutual inhibition would no longer appear. This can be tested if the core's latent has room for co-activation.
- **Bottleneck versus degeneracy.** Lesion the single integrating layer. If every readout fails, Craig's bottleneck structure holds. If readouts survive through other paths, the Barrett and Damasio structure holds.

## Verdict: watch (bottleneck claim disputed by two later sources; buffer and comparator adopted as a test)
The awareness claim is beyond what the brief claims. The buffer comparing present with predicted states, and the integration of incentive into salience, are useful functional elements.
