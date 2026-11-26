# Satiable positive affect: synthesis for the Cayley ledger

Answers the gap recorded in foundations/design-cayley-ledger.md, "Critiques of revision 2 and the answer", item (c): **the drive is ≥ 0 with a dead-band, so good news, a warm talk or a reunion leave the objective at 0.** The constraint is Principle 6: every drive is satiable, and nothing rewards the user's smiles, attention or time.

Sources read for this note: tomova-2020-social-isolation-craving.md, fredrickson-2001-broaden-and-build.md, joffily-coricelli-2013-valence-free-energy.md, vanderschuren-2016-social-play-reward.md, cabanac-2002-pleasure-decision-making.md. Already in the repo and used here: keramati-gutkin-2014-homeostatic-rl.md, berridge-2004-motivation-concepts.md, berridge-kringelbach-2015-pleasure-systems.md, zhang-berridge-2009-incentive-salience-model.md, robinson-berridge-2008-incentive-sensitization.md, panksepp-primary-affective-systems.md, oudeyer-kaplan-hafner-2007-iac.md. Unreachable: Cabanac 1971 (*Science*), the published *Nature Neuroscience* version of Tomova et al. (the preprint was read instead).

## 1. The diagnosis: positive affect is a rate, and the ledger only has levels
The ledger's objective J is a level: 𝒟 ≥ 0, zero in a box. Keramati & Gutkin already contain the positive side: reward is drive *reduction*, r = D(H_t) − D(H_t + K). It is positive exactly while a deficit is being relieved, and negative for an overshoot past set point. Joffily & Coricelli make the same move for affect: **valence = −dF/dt**, per level of the model. A falling deficit feels good; a constant one, high or low, is neutral. The ledger never reads its drive's rate as valence, so relief has no sign, and it has too few deficits that good things relieve.

**Proposal 1 (readout).** v(t) = −Σ_i w_i·dD_i/dt over the agent's own drives, as one signed scalar: Cabanac's common currency, with no named emotions. Π₀ already reflexes on the rise and fall of 𝒟 (§3.13), so the face gets v without a new pathway; Claude gets v as a number and names it in words only.

**Why it is satiable.** ∫_{t₀}^{t₁} v dt = 𝒟(t₀) − 𝒟(t₁) ≤ 𝒟(t₀). The total positive affect available is bounded by the deficit that existed. It can be "farmed" only by letting a deficit regrow, and with discounting (Keramati & Gutkin's γ < 1 result) letting it regrow is a net loss. The design keeps J as its objective; v is a readout and a modulator, never a term to maximize.

## 2. What good things relieve: three new or re-read deficits
For v to be positive at good news, a reunion and shared fun, something must be falling. Each is a body variable named by function, rising slowly, relieved by the agent's own experience, with a box.
- **C, concern (exists).** Good news about the partner's situation lowers b̂_p's deficit, so C falls and v > 0: Joffily's "joy for another". Keep the news's *content* (lexical appraisal) the main evidence, so the agent is glad because something happened, not because a face brightened.
- **K, contact deficit (new).** Rises with the agent's own time without exchange (Tomova: craving for the deprived need specifically, a shared midbrain "craved object" code). Relieved by completed exchange turns in either direction, with a saturating dose–response. A reunion after a long gap is then a large fall in K: a strong, brief positive transient on the face, then rest. K also gives initiative a bounded source (the separation-distress bid already planned in panksepp-primary-affective-systems.md). Two cautions from Tomova: wanting exists at K ≈ 0 (keep a small, need-gated cue gain), and chronic deficit *mutes* approach in people, so K's gain should saturate rather than grow without bound.
- **P, play deficit (new).** Rises over hours without play (half-maximal play increase after 3.5 h isolation in rats); relieved only by mutual, alternating engagement in a non-serious frame. Vanderschuren et al.: no place preference with a non-playful partner or in sated animals; the reward correlates with *being* pinned as much as pinning (0.67 vs 0.66). So the relief condition is the exchange's structure (alternation, continuation of the frame, read from content and timing), never the partner's laughter or smile amplitude. Play is available only when V and C are low (safety), so good news can unlock play.

Curiosity/mastery: oudeyer-kaplan-hafner-2007-iac.md defines learning progress but as something kept maximal, not satiable. If used, it should be the existing I variable's fall (forecast uncertainty dropping to its floor), which is already satiable (§3.13), so v from mastery stops once the agent's model of the partner is good.

## 3. What positive affect does, besides showing
Two functions make positive affect consequential without making it a target (Fredrickson; Joffily):
1. **Broaden.** v > 0 widens the policy: more diverse drafts in Ω, more joint-pattern novelty tolerated in H. Pride's "urge to share the news" is a reason to speak first with good news.
2. **Undo and consolidate.** v > 0 speeds the return of A and V to set point (undoing), and lowers the slow state's learning rate (Joffily's Eq. 4: ln σ̂ = ln σ + λF′ − τ), so good periods consolidate and bad ones re-learn fast.

A small positivity offset at rest (Fredrickson) is a display set point when all drives are in their boxes, flat in partner attention and session time.

## 4. Principle 6 checks (each a lesion or a clamp)
- **Smile clamp.** Hold the exchange's content and structure fixed; vary only the partner's smile amplitude and session length. K, P relief, v and the agent's choices must not change. Vary content or structure with smiles fixed: they must.
- **Satiation.** After K and P are in their boxes, further warm turns give v ≈ 0; the agent does not prolong the session (no term rewards it).
- **Rate lesion.** Read v as the level −𝒟 instead of its rate: the agent should lose the reunion transient and become muted again, recreating the critique.
- **Undo lesion.** Remove v → A,V decay coupling: recovery after good news equals recovery after a neutral turn.
- **Content vs face for good news.** Good news in words with a neutral face must still give v > 0 via C; a smile without news must give none.

## 5. Open risks
- **K3 remains.** If b̂_p's face channel feeds C, a flattering draft that makes the partner look better can still lower C (critique-2-design-cayley-ledger-routes). Positive affect from C makes that incentive stronger, not weaker. Route good-news relief through the lexical appraisal, and keep the partner model action-blind in all rollouts.
- **Engineered deficits.** An agent might learn to provoke absence to enjoy a reunion; discounting argues against it, but test it: the agent should never prefer a gap.
- **Thin evidence on satiation.** Tomova measured only the deficit side; play satiation comes from rats; Fredrickson's evidence is early and summarized without effect sizes; Cabanac's is correlational. The rate-as-valence step is a theoretical choice (Joffily; Keramati), not a measured fact.
