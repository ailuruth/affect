# Maier & Seligman 2016: Learned helplessness at fifty — insights from neuroscience

Citation: S. F. Maier, M. E. P. Seligman. *Psychological Review* 123(4): 349–367, 2016. doi:10.1037/rev0000033. Author manuscript: PMC4920136.

Source read: the full author manuscript via NCBI PMC (efetch XML, stripped to text), covering the abstract, every section from "Defining helplessness" to "Why versus whither", and the five figure captions. The figures themselves (microdialysis curves, circuit cartoons) were not seen, only their captions. The primary studies it reviews (Amat et al. 2005, 2006, 2008, 2010, 2014; Baratta et al. 2007, 2009; Christianson et al. 2008, 2014; Rozeske et al. 2011) were not read. All numbers below are as the review reports them.

## Claims
- The original theory "got it backwards". "Passivity in response to shock is not learned. It is the default, unlearned response to prolonged aversive events and it is mediated by the serotonergic activity of the dorsal raphe nucleus." What is learned is control: "the presence of control, not the absence of control, … is detected by prelimbic medial prefrontal circuits."
- Four functions in place of the old two (DETECT, EXPECT):
  - PASSIVITY/ANXIETY. Aversive input excites DRN 5-HT neurons. 5-HT in dPAG and striatum inhibits active escape, and 5-HT in amygdala/BNST potentiates fear. Intense activation desensitizes 5-HT1A autoreceptors, which sensitizes the DRN for days.
  - DETECT. A prelimbic (PL) ↔ dorsomedial striatum (DMS) act/outcome circuit detects that the response changes the outcome.
  - ACT. A separate PL population projects to DRN GABA interneurons and inhibits the 5-HT cells.
  - EXPECT. After the joint occurrence of control and shock, protein-synthesis-dependent plasticity in the PL→DRN pathway makes later uncontrollable stressors engage it anyway ("a circuit that EXPECTS control"). The authors note this "may not be a cognitive process … It is a circuit that provides an expectational function."
- The definition of control is unchanged since 1976: "control being present whenever the probability of (O), given a response (R) is different from the probability of (O) given the absence of that response (notR)". They note it is the same as the instrumental contingency definition later used in appetitive learning (Liljeholm et al. 2011).
- "There is nothing in the brain that is selectively turned on by a lack of control, only something that turns things off when there is the presence of control."
- Control is not safety. The safety-signal effect runs through insula, and the control effect through vmPFC (a double dissociation).
- An open caveat they raise themselves: under extreme aversion the brain may detect the presence of control only, but "this does not mean that the brain cannot detect lack of control in other types of circumstances".

## Evidence (as reported in the review)
- Triadic design: escapable (ESC), yoked inescapable (INESC, identical shocks), no shock. In the original dog work, "two-thirds of the animals from the INESC group failed to learn to escape, whereas 90% of the animals in both the ESC and 0 groups easily learned to escape." The same pattern holds in rats, and in humans with noise and with unsolvable anagrams (Hiroto & Seligman 1975).
- Not superstition: an ESC group whose shock ended when it *held still* later escaped normally in the shuttlebox (Maier 1970).
- DRN microdialysis (Fig. 1 caption): both ESC and INESC raise DRN 5-HT at first. Under INESC it stays raised after the session. Under ESC it "dropped precipitously as the escapable subjects learned the instrumental wheel-turn escape response, even though the shocks continued."
- Necessity: DRN lesion, or drugs blocking DRN 5-HT activation during INESC, prevents later passivity and anxiety. So does a 5-HT1A antagonist in the DRN during shock, and so do 5-HT2C antagonists in target regions at test. Sufficiency: picrotoxin or β-carboline in the DRN reproduces the outcomes.
- Input to the DRN does not differ by control. Locus coeruleus NE input is required, but "both escapable and inescapable shock produced exactly equal levels of locus coeruleus NE activation". The same holds for the other inputs measured.
- PL→DRN cells (retrograde label plus c-fos) are activated by ESC and not by INESC (Baratta et al. 2009). Inactivating PL during ESC: "the subjects with control learned the escape response perfectly, [but] this learning was no longer protective". Activating PL during INESC: "turned an animal without control into an animal with control".
- DMS inactivation during ESC left the escape response intact (acquired by the habit system) but removed the protection. DLS inactivation did not remove it. So protection requires *detecting* the contingency, not performing the response.
- DETECT and ACT neurons are separate. Dual retrograde tracers from DMS and DRN showed "no colocalization at all" (unpublished, Baratta).
- Time course: 5-HT1A desensitization recovers "within 3 days", and passivity and anxiety last "just this period of time".
- Immunization: ESC seven days earlier blocked the effects of social defeat (no shock, a different floor, different experimenters) and the defeat-induced DRN 5-HT rise. PL activation alone without shock did not immunize. PL activation *during* INESC did. Protein-synthesis or pERK blockade in PL after ESC removed immunization but not the acute protection.
- Prior ESC did more than cancel INESC's potentiation of fear conditioning. It *retarded* fear conditioning and sped extinction seven days later (Baratta et al. 2007, vmPFC-dependent).
- HPA: in rodents, control changes neither corticosterone, ACTH nor hypothalamic CRH. They explain this anatomically: DRN does not project to PVN, and the vmPFC→BNST relay is not sensitive to control.
- Humans (Kerr et al. 2012, yoked snake-phobia design): vmPFC rose only on controllable *snake* trials, not on controllable neutral trials. vmPFC and amygdala were negatively related.
- Scale: about 25,000 DRN 5-HT cells in the rat and about 150,000 in humans. The control-relevant caudal DRN holds about 8,000 in the rat and about 50,000 in humans, too few to image.

## Formal model
The review gives no equations beyond the contingency definition. Written out, with the circuit claims turned into a dynamical sketch (my reconstruction, not the authors'):
- Contingency (quoted definition): `ΔP = P(O | R) − P(O | ¬R)`. Control exists when `ΔP ≠ 0` for some R. Objective helplessness is `ΔP = 0` for all R.
- Default integrator (reconstructed): `ṡ = −s/τ_s + g(s_hist)·u_aversive − k·c`. Here `s` is DRN output, `u_aversive` is summed aversive drive, `g` rises with the integrated history of `s` (autoreceptor desensitization, τ of about 3 days), and `c` is the PL ACT signal. Passivity is the outcome when `s` crosses a threshold in its targets.
- Detection: `c = f(ΔP̂)`, where `ΔP̂` is estimated by the act/outcome (model-based) system, not the habit system.
- Expectation (immunization): a slow weight `w_PL` that grows when `c` and `u_aversive` are both high (Hebbian, protein-synthesis-dependent), so that later `c ≈ w_PL·u_aversive` even when `ΔP = 0`.

## License
APA journal article. The PMC author manuscript is free to read but not openly licensed. No code or data.

## Runs on this Mac without a GPU?
n.a. This is a review.

## Verdict: adopt (as a constraint on direction and on the time scales of coping potential)
- It is the strongest causal dissection available of what "coping potential" does in a body. It fixes the sign. The default under prolonged unrelieved aversion is withdrawal and conservation. Detected control is a learned inhibitor of that default.
- It also gives three dissociable parts, each with its own lesion: detecting contingency, acting on it, and a persistent prior.
- It is a review of one lab's rat work. The human claims rest on very few studies.

## What it implies for the engine (controllability without a named variable)
- **Controllability is not a gauge. It is the action-dependence of the model that predicts need reduction.** The DETECT function needs ΔP to be computed by the *model-based* system (DMS inactivation leaves the habit-learned escape intact but unprotective). In a single core, ΔP̂ = how much better a predictor of need reduction that conditions on the agent's action does than one that does not. Huys & Dayan 2009, Dorfman & Gershman 2019 and Ligneul et al. 2022 give three formal versions. No variable named "control" is required.
- **Passivity must come from the core, not from a "helplessness" state.** A satiable core already has the needed parts. Prolonged unreduced drive error is the input. A slow, sensitizing integrator of that error (time constant of days) gives the persistence. Energy conservation is itself a homeostatic objective: the authors frame 5-HT as "controlling and shifting the balance and flow of energy". If the expected *controllable* reduction of the drive is low, the cost of action outweighs it, and withdrawal is the optimal policy. This is what Huys & Dayan's controllable-reinforcement fraction χ does to Q values, plus an action cost that Huys & Dayan leave out.
- **The default-passivity finding conflicts with a purely normative prior.** Huys & Dayan's Fig. 4 shows that only *under*estimating control is costly, which favours a high-control default prior. Maier & Seligman find a low-control default in the body. The two agree only if action has an energetic cost, so that conservation pays when control is unknown and the aversion is prolonged. The engine should derive the default from that cost and not hard-wire it.
- **Interoception is not gated by control, but behaviour is.** Control changes passivity, fear and DRN, but not the HPA axis. In the engine, body variables should respond to an aversive input equally whatever the control. Only the policy, vigilance and expression readouts should depend on the controllability term. That is a testable signature of where the term enters.
- **Control ≠ safety.** A Pavlovian predictor of a need-free interval (a safety cue) and an action-contingency term must be separate terms in the equations, because they have separate lesions.
- **Development.** "A default of helplessness eventually overcome by the experience of mastery … is compatible with the ontogeny of the human species." This fits the appraisal account that infant distress differentiates once agency is perceived (Moors et al. 2013). The engine should start with low or unknown control and acquire the contingency term by living.

## Ablations that separate it (each predicted from the equations above)
1. **Remove DETECT.** Feed the policy a cached (habit) value and no action-conditioned versus action-free model comparison. The agent still learns the response that ends the aversive input, but its integrator sensitizes as if the input were uncontrollable. Prediction: after a controllable episode, the agent's later withdrawal and fear readouts match those of a yoked agent (the Amat 2014 pattern).
2. **Remove the sensitizing gain g** (make the integrator linear). Yoked exposure no longer produces a multi-day after-effect. Passivity tracks only current aversion.
3. **Freeze the slow prior weight w_PL.** Acute protection by control stays, and immunization (transfer to a new stressor, for example a partner's withdrawal after earlier mastery) disappears.
4. **Separate safety from control.** Remove the safety-cue predictor, and the protection from control stays (and vice versa).
5. **Check that body variables are unchanged.** For an equal aversive input, body variables should not differ between the controllable and yoked conditions. If they do, the controllability term is entering at the wrong place.
