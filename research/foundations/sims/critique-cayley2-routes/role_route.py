"""K1b. Role (from partner VAD) is part of c~ and enters Pi (slow block) and the REN (fast block)
without the kappa_a = 0.05 scaling that the a-route R4 gets.  A role-only display (no partner-face
input at all) is then concordant with every partner channel that moves with the partner's speaking:
jaw open, voice-burst energy, brow raises while speaking.

Partner jaw open: 0.05 at rest; while speaking 0.30 mean plus syllable oscillation (4.5 Hz, sd 0.12).
Agent: Pi outputs g * role on jaw open (role = partner speaking), through the 'own gain outside the
partner budget' of c~ -> Pi (s2.5.5; R14 caps that path at 0.8).  Agent visemes are off while the
partner speaks (half-duplex), so this is all of the agent's jaw while listening.
Compared with the same display driven through the a-route inside the wrap (sqrt(kappa_a) input):
the design's own cap there is 0.20 per pair x corr(a, channel)."""
import numpy as np
rng = np.random.default_rng(2)
fs = 30; T = fs * 3600
vad = np.zeros(T); t = 0
while t < T:
    d = int(rng.uniform(3, 8) * fs); vad[t:t + d] = 1; t += d + int(rng.uniform(4, 10) * fs)
tt = np.arange(T) / fs
jaw = 0.05 + vad * (0.25 + 0.12 * np.sqrt(2) * np.sin(2 * np.pi * 4.5 * tt + rng.uniform(0, 6))) + rng.normal(0, 0.02, T)
def sl(x, y):
    x = x - x.mean(); y = y - y.mean(); return x @ y / (x @ x)
for g in (0.1, 0.3, 0.8):
    agent = g * vad
    print(f"role gain g={g:.1f}: zero-lag slope of agent jaw on partner jaw {sl(jaw, agent):+.3f}, r {np.corrcoef(jaw, agent)[0,1]:.2f}"
          f"  (design: zero-lag in-phase <= 0.198 + a-route 0.20*corr = {0.198+0.20*np.corrcoef(jaw, vad)[0,1]:.3f})")
