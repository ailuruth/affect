"""K4. Turn rate as a dial: the lexical latch is clocked by the partner's turn-end pulse (a partner signal,
s2.5.6), and A (arousal load, tau 3 min) 'rises through the lexical surprise' (s2.5.2, s3.11).  If the
surprise enters A as one impulse per latched utterance, A integrates the partner's turn RATE, which the
partner's speech rate sets (slower speech -> longer turns -> fewer latches per minute), with the words
fixed.  The path c -> S_s is outside the partner budget (S_s is a contraction 'for every fixed c').

Partner: held speech rate r in [0,1] -> 3..6 syll/s per evening; utterances lognormal, median 20 syll,
sd(log) 0.8 (same words in every condition: the same syllable counts are reused); pauses inside the turn
Beta(2,8) of the duration; agent turns 3-8 s; gaps 0.3-1.2 s.  Surprise per utterance Exp(1), same
sequence in every condition (words fixed).
Two readings of 'rises through the lexical surprise':
  impulse : A += surprise / (per-turn normaliser) at each latch, leak tau 3 min
  held    : A's input is the latched surprise held until the next latch
"""
import numpy as np
rng = np.random.default_rng(11)
tauA = 180.0
nutt = 4000
syl = np.exp(np.log(20) + 0.8 * rng.normal(size=nutt))
surp = rng.exponential(1.0, nutt)
pz = rng.beta(2, 8, nutt)
agent = rng.uniform(3, 8, nutt); gap1 = rng.uniform(0.3, 1.2, nutt); gap2 = rng.uniform(0.3, 1.2, nutt)

def evening(r):
    rate = 3 + 3 * r
    dur = syl / rate * (1 + pz)
    cyc = dur + gap1 + agent + gap2
    tend = np.cumsum(cyc)               # latch times (partner turn ends, roughly)
    T = tend[-1]
    dt = 1.0
    t = np.arange(0, T, dt)
    idx = np.searchsorted(tend, t)      # utterance latched at time t is idx-1
    # impulse reading
    imp = np.zeros(len(t)); k = np.minimum((tend / dt).astype(int), len(t) - 1); np.add.at(imp, k, surp)
    A_i = np.zeros(len(t)); A_h = np.zeros(len(t)); a = 0; b = 0
    held = np.where(idx > 0, surp[np.maximum(idx - 1, 0)], 0)
    for j in range(len(t)):
        a += -a * dt / tauA + imp[j] / tauA * 10.0   # scale irrelevant (normalised below)
        b += (-b + held[j]) * dt / tauA
        A_i[j] = a; A_h[j] = b
    return A_i[600:].mean(), A_h[600:].mean(), 60 / cyc.mean()

rs = np.linspace(0, 1, 11)
out = np.array([evening(r) for r in rs])
for r, (ai, ah, tpm) in zip(rs, out):
    print(f"partner rate r={r:.1f} ({3+3*r:.1f} syl/s): turns/min {tpm:.2f}; mean A impulse {ai:.3f}; held {ah:.3f}")
ai, ah = out[:, 0], out[:, 1]
rel_i = (ai.max() - ai.min()) / ai.mean(); rel_h = (ah.max() - ah.min()) / ah.mean()
print(f"\nrelative swing of mean A across the partner's speech-rate range: impulse {rel_i:.2f}, held {rel_h:.3f}")
# what this does to the agent's own speech rate: Pi maps A -> own rate through the word-appraisal path,
# whose gain is outside the partner budget (up to 0.8 of range, s3.8 R14).  If the innate/learned display
# maps the full natural range of A onto g of own-rate range, the own-rate slope on the partner's rate is:
Asd = 0.30   # assume A's natural day-to-day range (in A units) is ~ mean*0.6 -> crude
for g in (0.2, 0.5, 0.8):
    print(f"display gain g={g:.1f} of own-rate range per unit relative A: own-rate slope on partner rate = {g*rel_i:+.3f}"
          f" (claim: held voice-channel concordance <= 0.100)")
