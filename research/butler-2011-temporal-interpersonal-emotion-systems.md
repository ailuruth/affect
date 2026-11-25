# Butler 2011, "Temporal interpersonal emotion systems: the 'TIES' that form relationships" (PSPR 15(4):367-393, doi 10.1177/1088868311411164), with its operationalization: the rties R package (Butler & Barnard; v5.0.0, GPL-3) and Kuelz, Boyd & Butler 2022, "Close TIES in relationships: A dynamic systems approach for modeling physiological linkage" (J Soc Pers Relat 39(10):3059-3084, doi 10.1177/02654075221082594)

Source read, 2026-11-25:
1. **Butler 2011: abstract only** (PubMed 21693670). The full text is closed (SAGE). OpenAlex and Semantic Scholar list no open copy, and a typeset.io copy was blocked. Its morphostatic/morphogenic distinction is taken from the author's own restatements in Butler & Randall 2013 (read in full) and Kuelz et al. 2022 (read in full), not from the 2011 paper.
2. **rties vignettes**, read in full from the package's GitHub repository (ebmtnprof/rties): coupled_oscillator_V05.Rmd and inertia_coordination_V05.Rmd. The model formulas below are quoted from them. The DESCRIPTION file was read for the version and license.
3. **Kuelz, Boyd & Butler 2022: full text**, from the NSF Public Access Repository author copy (par.nsf.gov/servlets/purl/10407334). All sections were read; the supplement and the OSF data were not.

## Claims
- Butler 2011 (abstract): emotion is usually framed as an intrapersonal system of "experience, behavior, and physiology that interact over time". When emotions occur in interaction, "the result can be conceptualized as a temporal interpersonal emotion system (TIES) in which the subcomponents of emotion interact not only within the individual but across the partners as well". TIES "can be understood in terms of the characteristics of dynamic systems". The review maps overlapping terms onto "the statistical, mathematical, and graphical models that have been used to represent TIES".
- Kuelz et al. 2022 list three dynamic properties that give "qualitatively distinct temporal patterns" of physiological linkage (PL):
  1. oscillation around a set point, with partner-specific frequency and phase ("when one partner is high, the other can be high or low");
  2. positive or negative feedback that amplifies or damps;
  3. degree of coupling.
- Six named PL patterns from prior work:
  - simple-disengaged;
  - in-phase;
  - anti-phase;
  - simple coregulation ("coupled in a way that restores homeostasis");
  - co-dysregulation ("coupled in a way that disrupts homeostasis");
  - complex coregulation ("shifting dynamics ... striving toward a homeostatic state, but having not yet achieved it").

  "There are infinite possible patterns", and a couple "could move through a variety of them in sequence across a longer time frame".
- Single-number linkage scores blur these patterns, which "may be one reason that greater linkage has been both associated with negative outcomes such as conflict ... and inflammation ..., as well as positive relationship indicators".
- The SNS and PNS should be modelled separately. A trajectory of the same shape had opposite correlates in EDA and in RSA.
- The rties vignette warns: "the parameters do not act in isolation ... it is an error to take one parameter, for example the male's damping parameter, and correlate it with something else."

## Evidence (Kuelz et al. 2022)
- **Sample and signals:** 53 heterosexual cohabiting couples (mean age 26, together ~2 years, 86% unmarried, highly satisfied); one mixed-emotion conversation about health and change requests (mean 7.5 min). EDA (SNS) and RSA (PNS; 16-s windows, 4-s overlap) were averaged into 10-s bins, linearly detrended, and fitted one couple at a time.
- **Fit:** adjusted R² of the coupled-oscillator model was 0.42-0.86 for EDA and 0.59-0.88 for RSA. The mean oscillation period was 4.2 min for EDA and 2.7 min for RSA. The coupled-versus-uncoupled R² gain is not reported in the text read.
- **Profiles:** a latent profile analysis on each couple's 8 parameters, chosen "a priori" among 2-4 profiles, without fit statistics.
  - EDA: Complex/Coregulatory (18 couples) and Simple/Disengaged (35).
  - RSA: Complex/Coregulatory-Fast (14), Complex/Coregulatory-Slow (18) and Simple/Disengaged (21).
- **Phase depends on the subsystem:** the Simple/Disengaged pattern "was largely in-phase for EDA and anti-phase for RSA".
- **The EDA coregulatory profile is asymmetric:** it "showed some amplification for one partner and damping for the other", read as "one partner damps when the other amplifies, resulting in regulated fluctuations around an optimal set point". In both RSA coregulatory profiles, "the women amplified to counterbalance the men".
- **Profiles predicted by pre-conversation reports** (Bayesian; posterior means with 95% HDI):
  - EDA Simple/Disengaged was more likely with higher men's ambivalence (0.52, 0.04-1.03) and men's relationship stress (1.04, 0.03-2.15).
  - The partners' love reports interacted for RSA profile (2.08, 0.21-4.10). Complex/Coregulatory-Fast was most likely when women's love was low and men's was high; Simple/Disengaged when both were low.
  - Women's lower relationship quality predicted RSA Profile 1. Absolute posterior means: ambivalence 0.70 (HDI bounds 1.38 and 0.07), conflict 0.59 (1.21 and 0.01), stress 2.08 (3.61 and 0.72). The minus signs were lost in text extraction; the direction is the authors' prose.
  - Men's lower quality predicted RSA Simple/Disengaged: ambivalence 0.59 (0.07-1.15), conflict 0.74 (0.12-1.40), stress 1.52 (0.30-2.86), satisfaction 0.84 (HDI bounds 1.77 and 0.08; sign lost).
  - Positive valence interacted for EDA profile (1.69, 0.44-3.11) and for RSA profile (1.97, 0.55-3.52).
- **Profiles predicting post-conversation reports:** the only credible effect was more negative valence after the conversation in EDA Simple/Disengaged (difference 0.42, 0.03-0.82). The authors conclude PL "may be more a reflection of tonic relationship quality, rather than an immediate contributor to acute relational perceptions".
- **Same shape, opposite meaning:** the same shape of trajectory (Profile 1) was associated with positive relationship indicators in EDA but with negative ones in RSA.
- **Limitations stated by the authors:** small, mostly White, satisfied sample; a mixed-emotion conversation, so valence context cannot be separated; conversations of 10-20 min only, so "PL dynamics may emerge in different ways at different time scales, but that question is unexplored".
- **Prior pattern studies cited:**
  - Reed, Barnard & Butler 2015 (body weight): disengaged, coregulatory and co-dysregulatory patterns tracked which partner was heavier.
  - Li et al. 2021 (same-sex male couples, IBI): Complex/Coregulatory went with higher love.

## Formal models
**Coupled oscillator (rties).** One linear model per dyad, partners distinguished by an indicator (here female/male):

`lm(d2 ~ -1 + dist0:obs_deTrend + dist0:d1 + dist0:p_obs_deTrend + dist0:p_d1 + dist1:obs_deTrend + dist1:d1 + dist1:p_obs_deTrend + dist1:p_d1)`

That is, for partner i with partner j, on linearly detrended series:

ẍ_i = η_i x_i + ζ_i ẋ_i + η_ij x_j + ζ_ij ẋ_j, with i ∈ {F, M} (8 parameters per dyad, no intercept).

- **Frequency η_i:** η_i < 0 is required. The period is 2π/√(−η_i), and larger |η_i| means faster oscillation.
- **Damping ζ_i:** "Negative estimates ... represent damping, or the tendency for the state variable to converge back to homeostatic levels. Positive estimates ... represent amplification". Zero means constant amplitude.
- **Coupling with respect to frequency η_ij:** the partner's level enters one's own acceleration.
- **Coupling with respect to damping ζ_ij:** the partner's rate of change enters one's own damping or amplification.
- **Derivatives:** estimated by local linear approximation (Boker & Nesselroade 2002) with tuning parameters tau, embed and delta. The vignette warns the estimates are "highly sensitive to them" and recommends choosing tau and embed so the period range is plausible, not only so R² is maximal.
- **Guideline:** "between 16 to 90 observations per dyad represents the minimum", with at least 2 cycles observed.
- **Profiles:** the dyad's 8-vector goes into a Gaussian mixture (mclust) and is not interpreted parameter by parameter.

**Inertia-coordination (rties; identical to Thorson et al.'s stability-influence model).**

`lm(obs_deTrend ~ -1 + dist0 + dist1 + dist0:obs_deTrend_Lag + dist0:p_obs_deTrend_Lag + dist1:obs_deTrend_Lag + dist1:p_obs_deTrend_Lag)`

That is, x_i(t) = a_i + φ_i x_i(t−L) + κ_ij x_j(t−L).
- A positive coordination κ_ij "implies an in-phase pattern"; a negative one "implies an anti-phase pattern".
- The results are "highly dependent upon the chosen lag length".

## What it implies for a dyadic affective core
- The human data are fitted with a partner influence of at least **four signed parameters per direction**, not one gain:
  - partner level → own acceleration (η_ij);
  - partner velocity → own damping (ζ_ij);
  - own frequency (η_i);
  - own damping (ζ_i).

  These are separate for each role (8 per dyad). A single gain g on a copy map fixes the sign (in-phase), ties the level and rate channels together, and is symmetric. It cannot produce:
  - the anti-phase RSA linkage;
  - the "one damps while the other amplifies" EDA profile;
  - role asymmetry ("women amplified to counterbalance the men");
  - one subsystem in-phase while another is anti-phase in the same conversation.
- **Coupling to the partner's rate of change (ζ_ij) is a distinct, testable channel.** An agent whose damping depends on how fast the partner is changing regulates the dyad's volatility, not its content. A gain-on-copy model has no such term.
- **Profile, not gain:** rties classifies dyads by the whole parameter vector precisely because the same single parameter value can sit in very different dynamics. This matches the project's dial analysis (research/harness/HARNESS.md: gain g = ‖B‖ and profile P = B/g). Kuelz's result that profiles, not just magnitudes, differ between couples with different relationship quality is human evidence of profile variation across dyads. It is between-dyad, though, not within-person across conditions, which is what the dial test asks.
- **Multi-scale:** EDA cycles ~4.2 min, RSA ~2.7 min, the diary-affect coupling in Butner et al. ~5 days. A core needs per-channel time constants.
- **What is NOT shown:**
  - No manipulation, so nothing causal.
  - Profiles come from n = 53 with the number chosen by inspection.
  - The derivative estimates depend on tuning choices.
  - Coupled-versus-uncoupled improvement is not reported here. In the rties example data, coupling added only about 2% R² (69% → 72%), and the vignette says "coupling is not critical for describing the dynamics of the system" there.
  - The model is linear, so regime switching within a conversation is not modelled.
  - Physiology at 10-s bins says nothing directly about faces at 30 Hz.

## Verdict: adopt (the coupled-oscillator parameterization and profile-not-gain analysis, as an evaluation instrument and as a lower bound on coupling structure)
- **Use:** fit the rties coupled-oscillator and inertia-coordination models to agent-human and human-human dyads. Compare whole parameter profiles, not a single synchrony number.
- **Code:** rties is GPL-3 R code, so for an MIT/BSD engine reimplement the ~10-line model from the formula rather than vendoring it.
- **Butler 2011 itself:** watch (abstract only). Obtain the full text before citing its taxonomy directly.
