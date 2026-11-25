"""CP2: water-filling mimicry. See PREDICTIONS.md."""
import json
import numpy as np, torch
nu = torch.tensor([0.1, 0.2, 0.4, 0.8, 1.6, 3.2]); P = 2.0; n = 6
def objective(K):
    K2 = K ** 2; tot = K2.sum(1) + nu; off = tot - torch.diagonal(K2)
    return 0.5 * torch.log(tot / off).sum()
res = []
for seed in range(20):
    torch.manual_seed(seed); K = torch.randn(n, n) * 0.3
    K = (K * np.sqrt(P) / K.norm()).requires_grad_(True); opt = torch.optim.SGD([K], lr=0.01)
    for it in range(20000):
        loss = -objective(K); opt.zero_grad(); loss.backward(); opt.step()
        with torch.no_grad():
            nrm = K.norm()
            if nrm ** 2 > P: K.mul_(np.sqrt(P) / nrm)
    K2 = (K.detach() ** 2).numpy()
    res.append(dict(off_frac=float((K2.sum() - np.trace(K2)) / P), diag=np.diag(K2).round(4).tolist(), obj=float(objective(K.detach()))))
wf = np.maximum(0.875 - nu.numpy(), 0)
out = dict(max_off_frac=max(r["off_frac"] for r in res), max_diag_err=max(float(np.max(np.abs(np.array(r["diag"]) - wf))) for r in res),
           max_k56=max(max(r["diag"][4], r["diag"][5]) for r in res), example=res[0], waterfill=wf.tolist())
print(json.dumps(out, indent=1))
