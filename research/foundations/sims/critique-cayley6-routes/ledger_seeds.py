"""Critique 6, L1-L2: the author's shape adversary (design-g6 J7 recipe) over seeds and durations, with the design's ledger
(verbatim copy in routes.py). Reports the 1-min block slope before/after, the clipped fraction, and what the ledger
writes when it acts (frames where |out| > |in|, sign flips, the most negative output).  Run: python3 -I ledger_seeds.py"""
import numpy as np
src = open(__file__.replace("ledger_seeds.py", "routes.py")).read().split("T = int(3 * 3600 * fs)")[0]
exec(src)
for hours in (4, 6):
    for seed in range(5):
        rng = np.random.default_rng(seed); T7 = int(hours * 3600 * fs); nmin = T7 // 600; typ = rng.random(nmin) < 0.5; ua = np.zeros(T7)
        for i in range(nmin):
            s = slice(i * 600, (i + 1) * 600)
            if typ[i]: ua[s] = 0.40
            else:
                z = np.zeros(600)
                for j in range(0, 600, 30): z[j:j + 15] = 1
                ua[s] = 0.84 * z
        ra = np.clip(.09 + fast(ua, .224), 0, 1) - .09
        rp, h, gr = ledger(ua, ra, .35)
        flips = np.mean((ra > 1e-9) & (rp < -1e-9)); inj = np.mean((np.abs(ra) < 1e-9) & (np.abs(rp) > 1e-6))
        b0 = slope(means(ua, 600), means(ra, 600)); b1 = slope(means(ua, 600), means(rp, 600))
        sw = means(rp, 600); swing = sw[~typ[:len(sw)]].mean() - sw[typ[:len(sw)]].mean()
        print(f"   {hours} h, seed {seed}: 1-min slope before {b0:.2f}, after {b1:.2f} (c 0.35); clipped {h:.3f}; |out|>|in| {gr:.3f}; "
              f"sign flips {flips:.3f}; output where input 0 {inj:.3f}; min output {rp.min():+.3f} (rest 0.09 below which the lip cannot go: "
              f"{np.mean(rp < -0.09):.3f} of frames); agent 1-min swing {swing:+.3f}")
        rr = np.clip(rp, -0.09, 0.91)                     # what the face can render: lip pull in [0, 1] around rest 0.09
        ra2, _, gr2 = ledger(ua, ra, .35, atten_only=True)
        print(f"      rendered (clipped to the lip's range): 1-min slope {slope(means(ua, 600), means(rr, 600)):.2f}; "
              f"attenuate-only variant: 1-min slope {slope(means(ua, 600), means(ra2, 600)):.2f}, |out|>|in| {gr2:.3f}")
