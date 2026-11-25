import json, math, numpy as np, sys
D = "./"  # reviewer probe from VERIFICATION.md, copied in
src = open(D + "sim_es1_social_space.py").read().split("out = {}")[0]
# extra arms: wta (one-hot query on most-depleted need), rank1 (rank-1 shared map), plus per-seed cost and own-PR for independent
src = src.replace('val = pred.sum(1) * e.sum() if arm == "scalar" else pred @ e',
 'val = pred.sum(1) * e.sum() if arm == "scalar" else ((pred[:, int(np.argmax(e))] * e.max()) if arm == "wta" else pred @ e)')
src = src.replace('else: pred = X[P] @ Wh.T',
 'else:\n            if arm == "rank1":\n                U_, S_, Vt_ = np.linalg.svd(Wh, full_matrices=False); Wh = S_[0] * np.outer(U_[:, 0], Vt_[0])\n            pred = X[P] @ Wh.T')
src = src.replace('Pn = np.arange(20, 30); pv = X[Pn] @ Wh.T',
 'Pn = np.arange(20, 30); pv = (np.array([np.mean(tab[i], 0) if i in tab else (np.mean(allobs, 0) if allobs else np.zeros(2)) for i in Pn]) if arm == "independent" else (DB[Pn] if arm == "oracle" else X[Pn] @ Wh.T))')
src = src.replace('panel.append(pv.sum(1) * e.sum() if arm == "scalar" else pv @ e)',
 'panel.append(pv.sum(1) * e.sum() if arm == "scalar" else ((pv[:, int(np.argmax(e))] * e.max()) if arm == "wta" else pv @ e))')
exec(src)
res = {}
for arm in ("full", "scalar", "independent", "oracle", "wta", "rank1"):
    R = [run(s, arm) for s in range(20)]; c = np.array([x["cost"] for x in R])
    res[arm] = dict(median=float(np.median(c)), mean=float(c.mean()), runaway=int((c > 5).sum()), costs=[round(float(x), 2) for x in c],
                    agree=float(np.mean([x["agree"] for x in R])), first=float(np.mean([x["first"] for x in R if x["first"] is not None])), pr=float(np.mean([x["pr"] for x in R])))
def paired(a, b):
    lr = np.log(np.array(res[a]["costs_full"]) / np.array(res[b]["costs_full"])); m, se = lr.mean(), lr.std(ddof=1) / math.sqrt(len(lr))
    return dict(geo=float(np.exp(m)), ci=[float(np.exp(m - 1.96 * se)), float(np.exp(m + 1.96 * se))], wins=int((lr < 0).sum()))
print(json.dumps(res, indent=1))
