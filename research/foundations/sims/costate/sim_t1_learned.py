"""T1: is the anticipatory costate learnable from 14 days? Parameters fixed in PREDICTIONS.md."""
import json, sys
import numpy as np, torch, torch.nn as nn
from env_t1 import schedule, body, cost_to_go, MIN_PER_DAY, B_STAR

torch.set_num_threads(2)
STEP = 5  # minutes per model step
SPD = MIN_PER_DAY // STEP


def stream(n_days, seed):
    rng = np.random.default_rng(seed)
    present, event = schedule(n_days, rng)
    b = body(present, 0.0)
    V = cost_to_go(b, present)
    idx = np.arange(0, len(b), STEP)
    ev = np.zeros(len(idx), dtype=int)
    for k, t in enumerate(idx):
        e = event[t:t + STEP]
        ev[k] = e.max()
    phase = 2 * np.pi * (idx % MIN_PER_DAY) / MIN_PER_DAY
    X = np.zeros((len(idx), 8), dtype=np.float32)
    X[:, 0] = b[idx]; X[:, 1] = present[idx]; X[np.arange(len(idx)), 2 + ev] = 1
    X[:, 6] = np.sin(phase); X[:, 7] = np.cos(phase)
    return X, V[idx].astype(np.float32), ev, b[idx]


class Net(nn.Module):
    def __init__(s):
        super().__init__(); s.gru = nn.GRU(8, 64, batch_first=True); s.head = nn.Linear(64, 1)
    def forward(s, x, h=None):
        y, h = s.gru(x, h); return s.head(y).squeeze(-1), h


def run(seed):
    torch.manual_seed(seed)
    Xtr, Vtr, _, _ = stream(15, 1000 + seed)
    Xte, Vte, ev, bte = stream(4, 5000 + seed)
    n_train = 14 * SPD
    net = Net(); opt = torch.optim.Adam(net.parameters(), 3e-3)
    rng = np.random.default_rng(seed)
    Xt, Vt = torch.tensor(Xtr), torch.tensor(Vtr)
    for it in range(1500):
        starts = rng.integers(0, n_train - 2 * SPD, 16)
        xb = torch.stack([Xt[s:s + 2 * SPD] for s in starts]); vb = torch.stack([Vt[s:s + 2 * SPD] for s in starts])
        pred, _ = net(xb)
        loss = ((pred[:, SPD:] - vb[:, SPD:]) ** 2).mean()
        opt.zero_grad(); loss.backward(); nn.utils.clip_grad_norm_(net.parameters(), 1.0); opt.step()
    # evaluation: hidden states along the test stream
    with torch.no_grad():
        _, hs = None, None
        y, _ = net.gru(torch.tensor(Xte)[None])
    H = torch.cat([torch.zeros(1, 1, 64), y[:, :-1]], dim=1)  # hidden before each step

    def mu_at(t, b_val=None):
        x = torch.tensor(Xte[t:t + 1])[None].clone()
        if b_val is not None: x[0, 0, 0] = b_val
        x.requires_grad_(True)
        v, _ = net(x, H[:, t:t + 1].transpose(0, 1).contiguous())
        v.sum().backward()
        return -x.grad[0, 0, 0].item()

    test = range(SPD, 4 * SPD)
    bye = [t for t in test if ev[t] == 3]; brb = [t for t in test if ev[t] == 2]
    arr = [t for t in test if ev[t] == 1 and (t - SPD) % SPD < SPD and all(ev[t - k] != 1 for k in range(1, 12 * 12))]
    mu_bye = np.mean([mu_at(t, B_STAR) for t in bye]); mu_brb = np.mean([mu_at(t, B_STAR) for t in brb])
    drops = [1 - mu_at(t) / mu_at(t - 1) for t in arr]
    db = [abs(bte[t] - bte[t - 1]) for t in arr]
    pres = Xte[:, 1]
    second_half = []
    for t in test:
        if pres[t] == 1:
            # position within the current presence block
            k = 0
            while t - k - 1 >= 0 and pres[t - k - 1] == 1: k += 1
            if k >= 6: second_half.append(t)
    sat = np.mean([mu_at(t) <= 0.02 for t in second_half])
    return dict(seed=seed, final_loss=loss.item(), mu_bye=mu_bye, mu_brb=mu_brb, diff=mu_bye - mu_brb,
                ratio=mu_bye / max(mu_brb, 0.01), drop=float(np.mean(drops)), drops=[float(d) for d in drops],
                max_db=float(max(db)), satiety_frac=float(sat), n_arr=len(arr), n_bye=len(bye), n_brb=len(brb))


if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]]
    for s in seeds:
        r = run(s); print(json.dumps(r), flush=True)
