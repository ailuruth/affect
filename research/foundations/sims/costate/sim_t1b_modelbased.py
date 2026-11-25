"""T1b: model-based costate. Learn the user's presence; differentiate through the innate body model."""
import json, sys
import numpy as np, torch, torch.nn as nn
from sim_t1_learned import stream, SPD, STEP
from env_t1 import B_STAR, RHO, K_A, K_P

torch.set_num_threads(2)
K = 72; DH = STEP / 60.0


def future_presence(X):
    p = X[:, 1]; n = len(p)
    F = np.zeros((n, K), dtype=np.float32)
    for k in range(1, K + 1):
        F[:n - k, k - 1] = p[k:]
    return F


class Net(nn.Module):
    def __init__(s):
        super().__init__(); s.gru = nn.GRU(8, 64, batch_first=True); s.head = nn.Linear(64, K)
    def forward(s, x, h=None):
        y, h = s.gru(x, h); return s.head(y), h


def value(b0, logits):
    p = torch.sigmoid(logits)
    b = b0; V = 0.0
    for k in range(K):
        b = b + DH * (K_P * p[..., k] * (1 - b) - K_A * (1 - p[..., k]) * b)
        V = V + np.exp(-RHO * DH * (k + 1)) * (b - B_STAR) ** 2 * DH
    return V


def run(seed):
    torch.manual_seed(seed)
    Xtr, _, _, _ = stream(15, 1000 + seed)
    Xte, _, ev, bte = stream(4, 5000 + seed)
    Ftr = future_presence(Xtr)
    n_train = 14 * SPD
    net = Net(); opt = torch.optim.Adam(net.parameters(), 3e-3)
    rng = np.random.default_rng(seed)
    Xt, Ft = torch.tensor(Xtr), torch.tensor(Ftr)
    lossf = nn.BCEWithLogitsLoss()
    for it in range(1500):
        starts = rng.integers(0, n_train - 2 * SPD, 16)
        xb = torch.stack([Xt[s:s + 2 * SPD] for s in starts]); fb = torch.stack([Ft[s:s + 2 * SPD] for s in starts])
        pred, _ = net(xb)
        loss = lossf(pred[:, SPD:], fb[:, SPD:])
        opt.zero_grad(); loss.backward(); nn.utils.clip_grad_norm_(net.parameters(), 1.0); opt.step()
    with torch.no_grad():
        logits, _ = net(torch.tensor(Xte)[None])
    logits = logits[0]

    def mu_at(t, b_val=None):
        b0 = torch.tensor(float(Xte[t, 0] if b_val is None else b_val), requires_grad=True)
        V = value(b0, logits[t]); V.backward(); return -b0.grad.item()

    test = range(SPD, 4 * SPD)
    bye = [t for t in test if ev[t] == 3]; brb = [t for t in test if ev[t] == 2]
    arr = [t for t in test if ev[t] == 1 and all(ev[t - k] != 1 for k in range(1, 144))]
    mu_bye = np.mean([mu_at(t, B_STAR) for t in bye]); mu_brb = np.mean([mu_at(t, B_STAR) for t in brb])
    drops = [1 - mu_at(t) / mu_at(t - 1) for t in arr]
    db = [abs(bte[t] - bte[t - 1]) for t in arr]
    pres = Xte[:, 1]; second_half = []
    for t in test:
        if pres[t] == 1:
            k = 0
            while t - k - 1 >= 0 and pres[t - k - 1] == 1: k += 1
            if k >= 6: second_half.append(t)
    sat = np.mean([mu_at(t) <= 0.02 for t in second_half])
    return dict(seed=seed, final_loss=loss.item(), mu_bye=mu_bye, mu_brb=mu_brb, diff=mu_bye - mu_brb,
                ratio=mu_bye / max(mu_brb, 0.01), drop=float(np.mean(drops)), drops=[float(d) for d in drops],
                max_db=float(max(db)), satiety_frac=float(sat))


if __name__ == "__main__":
    for s in [int(a) for a in sys.argv[1:]]:
        print(json.dumps(run(s)), flush=True)
