"""ES2: relations, episodes and anticipation in a learned space. See PREDICTIONS.md."""
import json
import numpy as np
NP, T, K, F = 400, 2000, 3, 8
W = 0.5 * np.array([[1, 0.8, 0, 0], [0, 0, 1, 0.8]]); R = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0.0]])
def run(seed, arm, world):
    r = np.random.default_rng(seed); Z = r.standard_normal((NP, 4)); A = r.standard_normal((F, 4)) / 2
    X = Z @ A.T + 0.3 * r.standard_normal((NP, F)); DB = Z @ W.T
    if world == "companion":
        C = np.array([int(np.argmin(np.where(np.arange(NP) == i, np.inf, np.linalg.norm(Z - R @ Z[i], axis=1)))) for i in range(NP)])
    else: C = r.integers(0, NP, NP)
    ra = np.random.default_rng(seed + 1000); pres = [np.where(ra.random(K) < 0.7, ra.integers(0, 20, K), ra.integers(20, NP, K)) for _ in range(T)]
    arr = ra.random(T) < 0.8
    re = np.random.default_rng(seed + 2000)
    b = np.zeros(2); XtX = np.eye(F); XtY = np.zeros((F, 2)); MtM = np.eye(F); MtY = np.zeros((F, F)); n_app = 0; n_arr = 0
    mem = {}; met = set(); pending = None; last = None
    cost, magree, rel_p, rel_t = [], [], [], []
    scal = arm == "scalar"; antic = arm in ("costate", "scalar", "nomem"); usemem = arm != "nomem"
    for t in range(T):
        drift = np.array([0.18, 0.1]) if (t // 50) % 2 == 0 else np.array([0.1, 0.18])
        b = np.minimum(b - drift, 1.0); e = np.maximum(-b, 0); P = pres[t].copy()
        if pending is not None:
            P[0] = pending; MtM += np.outer(X[last], X[last]); MtY += np.outer(X[last], X[pending]); n_arr += 1
        pending = None
        Wh = np.linalg.solve(XtX, XtY).T; Mh = np.linalg.solve(MtM, MtY).T; ph = (n_arr + 1) / (n_app + 2)
        q = (lambda v: v.sum(-1) * e.sum()) if scal else (lambda v: v @ e)
        direct = q(X[P] @ Wh.T); comp = q((X[P] @ Mh.T) @ Wh.T)
        val = direct + (ph * np.maximum(0, comp) if antic else 0)
        mbest, mval = None, -np.inf
        if usemem and mem:
            ids = list(mem); keys = np.array([np.mean(mem[i], 0) for i in ids]); sc = q(keys); k = int(np.argmax(sc)); mbest, mval = ids[k], 0.6 * sc[k]
        explore = np.linalg.norm(e) > 0.1 and re.random() < 0.1
        if explore: act = ("p", int(re.integers(0, K)))
        elif max(val.max(), mval) <= 0.01: act = ("rest", None)
        elif mval > val.max(): act = ("m", mbest)
        else: act = ("p", int(np.argmax(val)))
        if t >= 500:
            cost.append(0.5 * e @ e)
            if act[0] == "m":
                ids = list(mem); magree.append(ids[int(np.argmax(DB[ids] @ e))] == act[1])
            if act[0] == "p" and world == "companion" and P[act[1]] not in met and not scal:
                i = P[act[1]]; rel_p.append(float(comp[act[1]])); rel_t.append(float(DB[C[i]] @ e))
        if act[0] == "p":
            i = P[act[1]]; obs = DB[i] + 0.1 * re.standard_normal(2); b = np.minimum(b + obs, 1.0)
            XtX += np.outer(X[i], X[i]); XtY += np.outer(X[i], obs); mem.setdefault(i, []).append(obs); met.add(i); n_app += 1
            if arr[t]: pending = C[i]; last = i
        elif act[0] == "m":
            i = act[1]; obs = 0.6 * DB[i] + 0.1 * re.standard_normal(2); b = np.minimum(b + obs, 1.0)
    return dict(cost=float(np.mean(cost)), magree=magree, rel_p=rel_p, rel_t=rel_t, n_seek=len(magree))
out = {}
for world in ("companion", "random"):
    for arm in ("costate", "rr", "scalar", "nomem"):
        Rs = [run(s, arm, world) for s in range(20)]; c = [x["cost"] for x in Rs]; mg = sum((x["magree"] for x in Rs), [])
        rp = sum((x["rel_p"] for x in Rs), []); rt = sum((x["rel_t"] for x in Rs), [])
        out[f"{world}/{arm}"] = dict(median_cost=float(np.median(c)), mean_cost=float(np.mean(c)), runaway=int(sum(x > 5 for x in c)), costs=[round(x, 4) for x in c],
                                     mem_agree=float(np.mean(mg)) if mg else None, n_seek=len(mg), rel_r=float(np.corrcoef(rp, rt)[0, 1]) if len(rp) > 2 else None, n_rel=len(rp))
o = out; out["checks"] = dict(ES2_1_ratio=o["companion/costate"]["median_cost"] / o["companion/rr"]["median_cost"], ES2_2_ratio=o["random/costate"]["median_cost"] / o["random/rr"]["median_cost"],
    ES2_3_costate=o["companion/costate"]["mem_agree"], ES2_3_scalar=o["companion/scalar"]["mem_agree"], ES2_4_ratio=o["companion/costate"]["median_cost"] / o["companion/nomem"]["median_cost"], ES2_5_r=o["companion/costate"]["rel_r"])
print(json.dumps(out, indent=1))
