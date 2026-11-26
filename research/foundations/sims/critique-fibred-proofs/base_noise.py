"""Critique check K1: does the base of design-fibred-attribution-core.md persist under its own noise?

Design constants (section 2.1): beta_b=200, d_min=0.5, eps_b=0.2 /s, sigma_b=0.09, n_b=24, t_max=0.05.
SDE: db = -eps_b grad V(b) dt + sigma_b dW, V = -(1/beta) log sum_c exp(-beta|b-mu_c|^2/2).
Worst admissible placement used by the design's own Kramers estimate: neighbours at d_min.
Five centres on a line (-1,-0.5,0,0.5,1) along e1 (|mu|<=1, separation 0.5).
Not evidence about behaviour; a check of the design's stated estimate (6-19 h).
Run: python3 -I base_noise.py
"""
import numpy as np

beta, eps, sig, nb, dt = 200.0, 0.2, 0.09, 24, 1 / 30
centres = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])


def grad1(x):
    a = -beta * (x[:, None] - centres[None, :]) ** 2 / 2
    p = np.exp(a - a.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
    return (p * (x[:, None] - centres[None, :])).sum(1)


def run(tilt, n=400, hours=1.0, seed=0):
    r = np.random.default_rng(seed)
    T = int(hours * 3600 / dt)
    x = np.zeros(n)                      # coordinate along the line of centres (start at centre 0)
    perp = np.zeros((n, nb - 1))         # the other 23 coordinates: pure OU (V separates)
    well = np.full(n, 2); switches = np.zeros(n); occ = np.zeros(5)
    inside = 0.0; rad = 0.0
    for t in range(T):
        x += -eps * (grad1(x) - tilt) * dt + sig * np.sqrt(dt) * r.normal(size=n)
        perp += -eps * perp * dt + sig * np.sqrt(dt) * r.normal(size=(n, nb - 1))
        near = np.argmin(np.abs(x[:, None] - centres[None, :]), 1)
        # count a switch only when the state is within 0.1 of a different centre (hysteresis)
        d = np.abs(x - centres[near])
        new = (near != well) & (d < 0.1)
        switches += new; well = np.where(new, near, well)
        if t > T // 10:
            occ += np.bincount(well, minlength=5)
            dist = np.sqrt(d ** 2 + (perp ** 2).sum(1))
            inside += np.mean(dist < 0.1); rad += np.mean(dist)
    m = T - T // 10 - 1
    return switches.mean() / hours, occ / occ.sum(), inside / m, rad / m


if __name__ == "__main__":
    s0, occ0, ins0, rad0 = run(0.0)
    print(f"no tilt: switches per hour {s0:.1f} (mean residence {3600/s0:.0f} s); "
          f"fraction of time within r=0.1 of a centre {ins0:.4f}; mean distance from nearest centre {rad0:.2f}")
    print(f"  design's Kramers estimate used exp(2 dV/sigma^2)=exp({2*0.031/sig**2:.2f}); "
          f"with eps_b the exponent is 2 eps dV/sigma^2 = {2*eps*0.031/sig**2:.2f}")
    for tl in (0.05, -0.05):
        s, occ, _, _ = run(tl, seed=1)
        print(f"tilt {tl:+.2f} along the line (t_max): switches/h {s:.1f}; occupancy of wells -1..1: "
              + " ".join(f"{o:.3f}" for o in occ) + f"; ratio end wells {occ[4]/max(occ[0],1e-9):.1f}")
