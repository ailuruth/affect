"""H: prioritized vs uniform nightly replay for the presence world model. Parameters in PREDICTIONS.md."""
import json, sys
import numpy as np, torch, torch.nn as nn
from sim_t1_learned import stream, SPD
from sim_t1b_modelbased import Net, value, future_presence
from env_t1 import B_STAR

torch.set_num_threads(2)


def c1_diff(net, Xte, ev):
    with torch.no_grad(): lg, _ = net(torch.tensor(Xte)[None])
    lg = lg[0]
    def mu(t):
        x = torch.tensor(B_STAR, requires_grad=True); V = value(x, lg[t]); V.backward(); return -x.grad.item()
    test = range(SPD, 4 * SPD)
    return float(np.mean([mu(t) for t in test if ev[t] == 3]) - np.mean([mu(t) for t in test if ev[t] == 2]))


def run(seed, prioritized):
    torch.manual_seed(seed); rng = np.random.default_rng(seed)
    Xtr, _, _, _ = stream(15, 1000 + seed); Ftr = future_presence(Xtr)
    Xte, _, ev, _ = stream(4, 5000 + seed)
    Xt, Ft = torch.tensor(Xtr), torch.tensor(Ftr)
    net = Net(); opt = torch.optim.Adam(net.parameters(), 3e-3)
    lossf = nn.BCEWithLogitsLoss(reduction="none")
    prio = {}; curve = []
    for night in range(2, 15):
        starts = np.arange(0, night * SPD - 2 * SPD + 1, 6)  # candidate window starts (every 30 min)
        for s in starts:
            prio.setdefault(int(s), 1.0)  # new windows enter at max-ish priority
        for it in range(200):
            if prioritized:
                p = np.array([prio[int(s)] for s in starts]) ** 0.6; P = p / p.sum()
                pick = rng.choice(len(starts), 16, p=P); w = (1.0 / (len(starts) * P[pick])); w = w / w.max()
            else:
                pick = rng.choice(len(starts), 16); w = np.ones(16)
            st = starts[pick]
            xb = torch.stack([Xt[s:s + 2 * SPD] for s in st]); fb = torch.stack([Ft[s:s + 2 * SPD] for s in st])
            pred, _ = net(xb); l = lossf(pred[:, SPD:], fb[:, SPD:]).mean(dim=(1, 2))
            loss = (torch.tensor(w, dtype=torch.float32) * l).mean()
            opt.zero_grad(); loss.backward(); nn.utils.clip_grad_norm_(net.parameters(), 1.0); opt.step()
            for s, li in zip(st, l.detach().numpy()): prio[int(s)] = float(li) + 1e-3
        curve.append(c1_diff(net, Xte, ev))
    return curve


if __name__ == "__main__":
    for s in [int(a) for a in sys.argv[1:]]:
        print(json.dumps(dict(seed=s, uniform=run(s, False), prioritized=run(s, True))), flush=True)
