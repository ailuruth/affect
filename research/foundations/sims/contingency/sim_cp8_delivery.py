"""CP8: regulation by delivery through self-reading. See PREDICTIONS.md."""
import json
import numpy as np
FS, TAU = 30, 1.0
def run(seed, feedback=True, legible=True):
    r = np.random.default_rng(seed); E = r.standard_normal((12, 4)); Rd = np.linalg.pinv(E)
    d = r.standard_normal(4); d /= np.linalg.norm(d)
    if legible: u = E @ d
    else:
        Q, _ = np.linalg.qr(np.c_[E, r.standard_normal((12, 1))]); v = Q[:, 4]; u = v * np.linalg.norm(E @ d)
    z = np.zeros(4); dt = 1 / FS; proj = []
    for k in range(int(30 / dt)):
        y = E @ z + u
        fb = 0.5 * (Rd @ y) if feedback else np.zeros(4)
        z = z + dt * (-z + fb) / TAU + 0.02 * np.sqrt(dt) * r.standard_normal(4)
        if k * dt >= 20: proj.append(z @ d)
    return float(np.mean(proj))
out = {name: [run(s, fb, lg) for s in range(20)] for name, fb, lg in (("intact", True, True), ("cut", False, True), ("illegible", True, False))}
out = {k: dict(mean=float(np.mean(v)), min=float(np.min(v)), max=float(np.max(v))) for k, v in out.items()}
print(json.dumps(out, indent=1))
