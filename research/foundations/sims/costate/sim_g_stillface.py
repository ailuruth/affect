"""G: still-face (Ekas 3-2-3 min), adapted S2-c. Parameters in PREDICTIONS.md."""
import json
import numpy as np

DT = 0.1; RHO = 1 / 3600; BSTAR = 0.8

def V(b, q, H=7200, step=10.0):
    v, x = 0.0, b
    for k in range(int(H / step)):
        x = x + step * (-x / 3600 + q * 0.8 * 0.01 * (1 - x)); v += np.exp(-RHO * step * (k + 1)) * (x - BSTAR) ** 2 * step
    return v

def mu_c(b, q, e=1e-4): return -(V(b + e, q) - V(b - e, q)) / (2 * e)

def run(seed, frozen=False):
    r = np.random.default_rng(seed)
    b, a, bb = 0.9, 16.0, 4.0
    T = int(480 / DT); pending = []
    rec = dict(smile=[], distress=[], bid=[])
    Vprev = V(b, a / (a + bb)); ema = 0.0; mu = mu_c(b, a / (a + bb))
    for k in range(T):
        t = k * DT; phase = 0 if t < 180 else (1 if t < 300 else 2)
        q = 0.8 if frozen else a / (a + bb)
        if k % 10 == 0: mu = mu_c(b, q)
        p_bid = 0.5 / (1 + np.exp(-((mu * q) - 0.02) / 0.01)) * DT
        bid = r.random() < p_bid; expr = r.random() < 0.3 * DT
        if bid or expr:
            resp = (phase != 1) and (r.random() < 0.8)
            pending.append((t + r.random() * 1.0, resp))
        responses = 0
        for item in list(pending):
            if item[0] <= t:
                pending.remove(item)
                if item[1]: responses += 1; a += 1
                else: bb += 1
        b = b + DT * (-b / 3600) + responses * 0.01 * (1 - b)
        if frozen: a, bb = 16.0, 4.0
        Vnow = V(b, 0.8 if frozen else a / (a + bb)) if (k % 10 == 0 or responses) else Vprev
        v = -(Vnow - Vprev) / DT; Vprev = Vnow
        ema += (DT / 2.0) * (v - ema)
        rec["smile"].append(max(ema, 0)); rec["distress"].append(max(mu, 0)); rec["bid"].append(bid)
    R = {key: np.array(val, float) for key, val in rec.items()}
    sl = lambda lo, hi: slice(int(lo / DT), int(hi / DT))
    return dict(smile=[R["smile"][sl(0,180)].mean(), R["smile"][sl(180,300)].mean(), R["smile"][sl(300,480)].mean()],
                distress=[R["distress"][sl(0,180)].mean(), R["distress"][sl(180,300)].mean(), R["distress"][sl(300,480)].mean()],
                bids_sf_first30=R["bid"][sl(180,210)].sum(), bids_sf_last30=R["bid"][sl(270,300)].sum(), bids_sf=R["bid"][sl(180,300)].sum())

out = {}
for name, frozen in [("intact", False), ("lesion_frozen_q", True)]:
    rs = [run(s, frozen) for s in range(20)]
    m = lambda f: np.mean([f(x) for x in rs], axis=0).tolist()
    out[name] = dict(smile_play_sf_reunion=m(lambda x: x["smile"]), distress_play_sf_reunion=m(lambda x: x["distress"]),
                     bids_sf_first30=m(lambda x: x["bids_sf_first30"]), bids_sf_last30=m(lambda x: x["bids_sf_last30"]), bids_sf=m(lambda x: x["bids_sf"]))
print(json.dumps(out, indent=1))
