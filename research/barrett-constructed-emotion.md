# The theory of constructed emotion: an active inference account of interoception and categorization

Lisa Feldman Barrett, *Social Cognitive and Affective Neuroscience* 12(1):1–23, 2017, doi:10.1093/scan/nsw154 (PMC5390700; read in full text).

## Claims
- A brain's core task is **allostasis**: predictively regulating the body's resources "according to costs and benefits", anticipating needs "before they arise". (The phrase "body budget" does not appear in this paper.)
- The brain runs an internal model of the body in the world. **Interoception** (the representation of the internal milieu) is at its core. Interoceptive sensations are usually experienced as low-dimensional **affect** (valence and arousal), which "are not unique to instances of emotion".
- Prediction, not stimulus→response. Predictions are **concepts**. A completed prediction is a categorization that regulates physiology, guides action and constructs perception. "When the internal model creates an emotion concept, the eventual categorization results in an instance of emotion."
- Prediction error is "encoded and consolidated whenever it is predicted to result in a physiological change in state of perceiver". In other words, learning is gated by relevance to allostasis.
- There are no emotion essences. Categories are populations of variable instances ("degeneracy"). A classifier pattern for "sadness" "is not the brain state for sadness but merely a statistical summary". The **mental inference fallacy** is treating an action (freezing) as the emotion (fear).
- Reappraisal and regulation are themselves predictions that categorize inputs with concepts. Amygdala output signals uncertainty, not "emotion".

## Evidence
A theoretical synthesis. It cites tract-tracing (Barbas' structural model), meta-analyses showing no consistent region per emotion (Lindquist et al. 2012), non-replicating MVPA classifiers, simulation fMRI (N=16), the patient S.M. and decorticate "sham rage". There is no new experiment and no computational implementation.

## License
- Paper: CC BY-NC 4.0.
- Code: none.

## Runs on this Mac without a GPU?
n.a.

## Verdict: adopt
Adopted as the stated basis for three components:
1. Body variables regulated predictively (allostasis).
2. Valence and arousal as low-dimensional **read-outs** of a learned state, not set variables (Principle 2).
3. Claude as the conceptual layer that categorizes a state in context (Principle 4).

It also supplies the argument for Principle 1: an emotion classifier commits the essentialist error. It is a theory, not a mechanism. Smith, Parr and Friston and Hesp et al. must supply the equations.

## What it gives S1
- **Body variables as allostatic quantities.** Social contact, predictability and activity budget should carry a predicted trajectory as well as a current value. The Bot acts on predicted deficit ("contact will run low tonight"), not only on present error.
- **Learning gated by body relevance.** Update $f_\theta, g_\theta$ more strongly on turns whose prediction error moved $b$. This is the same signal the brief's replay weighting uses.
- **What Claude sees.** Show low-dimensional affect read out of $h$, the body variables with their predicted course, and the situation (who, how long since contact, what happened). Then ask Claude to *categorize* it, offering several candidate concepts, since a category is a population. Never pass a single pre-chosen word.
- **Reappraisal feeds back as prediction.** Claude's chosen concept and its reappraisal enter $f_\theta$ as an input that changes predicted $b$. An example: "the user is travelling" lowers the predicted contact deficit. The feedback does not overwrite $h$.
- **Ablation link.** After silence, the same elapsed time should produce different reunion behavior depending on the predicted versus observed contact the Bot has learned for this user. Removing $h$ removes that history-dependence.
