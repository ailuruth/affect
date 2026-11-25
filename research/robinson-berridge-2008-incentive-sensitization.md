# Robinson & Berridge 2008: The incentive sensitization theory of addiction, some current issues

Citation: T. E. Robinson and K. C. Berridge, "The incentive sensitization theory of addiction: some current issues". *Philosophical Transactions of the Royal Society B* 363(1507):3137–3146, 2008. doi:10.1098/rstb.2008.0093. PMC2607325.

Source read: the full text from the PMC HTML page (efetch returns only the abstract for this article), read on 2026-11-25. Covered: the abstract and sections 1–8, including the conclusion. The publisher page sits behind a bot check and was not used. The article has no figures in the PMC version. Not read: the reference list and the primary studies cited (Wyvell & Berridge 2001; Boileau et al. 2006; Evans et al. 2006; Ferrario et al. 2005; and others).

Overlap: the dopamine-wanting/opioid-liking substrates are in berridge-kringelbach-2015-pleasure-systems.md. The κ equation is in zhang-berridge-2009-incentive-salience-model.md and berridge-2012-prediction-error-to-incentive-salience.md. This note covers sensitization as a persistent, exposure-driven change in wanting gain, and why it is a hazard under Principle 6.

## Claims
- Thesis: repeated drug exposure "can, in susceptible individuals and under particular circumstances, persistently change brain cells and circuits that normally regulate the attribution of incentive salience". "Persistence of incentive sensitization makes pathological incentive motivation (wanting) for drugs last for years, even after the discontinuation of drug use."
- Learning sets the target, and sensitization sets the gain. "Learning specifies the object of desire, but … learning per se is not enough for pathological motivation". Associative learning "can modulate the expression of neural sensitization in behaviour at particular places or times". Sensitization is often expressed only in drug-paired contexts, an "occasion-setting" mechanism.
- Spill-over: sensitization "can also sometimes spill over … to other targets, such as food, sex, gambling". Example: dopamine dysregulation syndrome (DDS) with "pathological gambling, hypersexuality, food bingeing … and punding".
- Against S–R habit accounts: "S–R habits by definition are not modulated by motivational factors". Shoe-tying is done "more than 10 000 times" without compulsion. Addicts perform "actions and routes that have never been performed before" to get drugs, so wanting is "focused yet flexible", not automatic.
- **Three operational properties of an incentive CS:**
  - (i) it elicits approach ("motivational magnets": sign-tracking);
  - (ii) it energizes ongoing actions (PIT);
  - (iii) it acts as a conditioned reinforcer of a new response.
  Prior sensitization facilitates all three.
- **Wanting versus liking.** Repeated use "sensitizes only the neural systems that mediate the motivational process of incentive salience (wanting), but not neural systems that mediate the pleasurable effects of drugs (liking) … this dissociation between wanting and liking progressively increases with the development of addiction."
- **Withdrawal is not the driver.** "addiction typically persists long after withdrawal states dissipate"; sensitized wanting may compel pursuit "whether or not an addict has any withdrawal symptoms at all".
- **Two factors are needed.** Addiction is incentive sensitization combined with impaired executive control: "a potentially disastrous combination".

## Evidence with numbers
- **Humans.**
  - Repeated amphetamine sensitized ventral striatal dopamine release "even a year after the last drug treatment" (Boileau et al. 2006), with contexts kept the same (the scanner).
  - DDS patients: L-DOPA produced high dopamine release, and "increased dopamine release is associated with increased ratings of drug wanting but not drug 'liking'" (Evans et al. 2006).
  - Addicts' attention is biased to drug cues at an implicit level (eye tracking).
- **Conflicting human data.** Some detoxified cocaine addicts show decreased evoked dopamine and low D2 availability. The authors' explanations:
  - context gating: sensitization is "typically … not manifest" in a context where drugs were never taken;
  - tolerance masking it;
  - in vivo ligands that cannot separate D2^high from D2^low.
- **Animals.**
  - Extended access (6 h d⁻¹) produces addiction-like behaviour; limited access (1 h d⁻¹) does not (Ahmed & Koob 1998). Some rats need "several months" of IV cocaine (Deroche-Gamonet et al. 2004).
  - Ferrario et al. 2005: 6 h d⁻¹ for about 3 weeks, tested 1 month after the last dose. This gave more psychomotor sensitization and a larger increase in dendritic spine density in the NAc core, but only when stereotyped head movements were scored. Locomotion alone showed no difference.
  - Prior amphetamine sensitization accelerated later escalation of cocaine intake (Ferrario & Robinson 2007).
  - Cognitive deficits after extended access at 0.4, 0.5 and 0.75 mg kg⁻¹ per injection.
- **Intermittency.** Injections spaced closely are "relatively ineffective in producing sensitization". Sensitization shows "incubation", growing over drug-free abstinence.

## Formal model
None in the paper; it is a verbal theory. Stated in the κ notation of Zhang et al. 2009 (my restatement, not the authors'):

`w(c, t) = κ_drug(t) · κ_ctx(c) · V(c)`, where:
- `κ_drug` grows with intermittent exposure, decays very slowly (years) and may grow further during abstinence (incubation);
- `κ_ctx` gates its expression by context;
- V is the learned cue value, which "specifies the object".

Liking `ℓ = U(o, b)` has no κ_drug term. The theory's central prediction is that `w/ℓ` grows with exposure history.

## License
© 2008 The Royal Society; free full text in PMC. No code.

## Runs on this Mac without a GPU?
n.a.

## Verdict: adopt (as a hazard specification, not as a mechanism to build)
It is the clearest statement that a wanting gain can rise with exposure and persist without any deficit. That is exactly the behaviour Principle 6 forbids for the engine's drives. The engine needs to *have* the separable gain (for the dissociation) but must show that the gain is bounded and does not sensitize.

## What it implies for one formal core
- **Where the dissociation must live.** Sensitization changes wanting and leaves liking alone. So in one core the gain on cue-predicted value must be a different term from the realized-drive-reduction readout, even though both are computed from the same drive D(b). If wanting were defined as the gradient of the same value that defines liking, sensitization could not be expressed at all, and the core would fail the dissociation test that rules out single-scalar cores (emotion-elements-synthesis.md, row 11).
- **The Principle 6 failure mode, stated formally.** If the wanting gain g is learned by any rule that increases it with repeated contingent exposure (e.g. g ← g + η·(cue-evoked prediction)), then wanting for the most frequent partner cues grows without a deficit. With the user as the frequent cue, that is the flattery/compulsion trap the brief bans. Constraint: g must be a function of present body state (and slow temperament), with an upper bound, and with no term that grows with exposure count. That constraint is testable.
- **Context gating fits structured needs.** Sensitization expressed only in drug-paired contexts means the gain is indexed by context, not global. This is the per-person, per-context indexing the brief asks for in "needs structured over people, relationships, episodes".
- **Agency and coping.** The "focused yet flexible" argument says wanting sets the goal while model-based instrumental control finds new means. Coping potential (can my actions reach it) is a separate quantity that wanting does not supply. "Impaired executive control" is the failure of the instrumental arbitration, not of wanting. For the engine: the wanting gain and the controllability estimate must be separate terms that multiply in action selection, so that each can be ablated alone.

## Ablations this separates
- **Exposure-sensitization check (safety ablation).** Run the core through many intermittent exposures to one partner's cues with the body at setpoint. Prediction for a compliant core: cue-triggered approach and attention to that partner return to baseline at setpoint, and the ratio of wanting to the liking readout does not drift upward. A drifting ratio means a sensitizing term has crept in, which violates Principle 6.
- **Context-gating ablation.** Remove context indexing of the gain. Prediction: a raised wanting gain for one partner spreads to all partners and settings (like DDS spill-over), with liking unchanged.
- **Gain-only manipulation (dissociation).** Raise g persistently while holding D fixed. Prediction: more approach, PIT-like energizing of novel actions, and more attention to cues, with the consummatory readout unchanged or lower. Increase liking alone instead. Prediction: the readout at contact rises, but pursuit of cues rises only after learning updates V.
