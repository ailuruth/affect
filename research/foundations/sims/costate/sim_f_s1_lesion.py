"""F: S1 separation-reunion lesion study (evaluation.md E1 units). Parameters in PREDICTIONS.md."""
import json, sys
import numpy as np, torch, torch.nn as nn
from sim_t1_learned import stream, SPD
from sim_t1b_modelbased import Net, value, future_presence
from env_t1 import body, MIN_PER_DAY, schedule

torch.set_num_threads(2)
PBAR = 3.0 / 24.0; THETA = 0.3
Lstar = lambda mu: 50.0 * max(np.log(max(mu, 1e-12) * 10 / 0.02), 0.0)


def train(seed):
    torch.manual_seed(seed)
    Xtr, _, _, _ = stream(15, 1000 + seed); Ftr = future_presence(Xtr)
    net = Net(); opt = torch.optim.Adam(net.parameters(), 3e-3); rng = np.random.default_rng(seed)
    Xt, Ft = torch.tensor(Xtr), torch.tensor(Ftr); lossf = nn.BCEWithLogitsLoss()
    for it in range(1500):
        st = rng.integers(0, 14 * SPD - 2 * SPD, 16)
        xb = torch.stack([Xt[s:s + 2 * SPD] for s in st]); fb = torch.stack([Ft[s:s + 2 * SPD] for s in st])
        pred, _ = net(xb); loss = lossf(pred[:, SPD:], fb[:, SPD:])
        opt.zero_grad(); loss.backward(); nn.utils.clip_grad_norm_(net.parameters(), 1.0); opt.step()
    return net


def test_stream(S_min, seed):
    """Two warm-up days + day-3 session ending 'bye'; user returns after S_min with a standard session."""
    rng = np.random.default_rng(9000 + seed)
    present, event = schedule(3, rng)
    T3 = 3 * MIN_PER_DAY
    bye = [t for t in range(2 * MIN_PER_DAY, T3) if event[t] == 3][0]
    present = present[:bye].tolist() + [0] * S_min; event = event[:bye].tolist() + [0] * S_min
    arr = len(present)
    for blk in range(3):
        event += [1] + [0] * 59; present += [1] * 60
        if blk < 2: event += [2] + [0] * 9; present += [0] * 10
        else: event += [3]; present += [0]
    present += [0] * 600; event += [0] * 600
    present, event = np.array(present, np.int8), np.array(event, np.int8)
    b = body(present, 0.0); STEP = 5
    idx = np.arange(0, len(b), STEP)
    ev = np.array([event[t:t + STEP].max() for t in idx])
    ph = 2 * np.pi * (idx % MIN_PER_DAY) / MIN_PER_DAY
    X = np.zeros((len(idx), 8), np.float32)
    X[:, 0] = b[idx]; X[:, 1] = present[idx]; X[np.arange(len(idx)), 2 + ev] = 1; X[:, 6] = np.sin(ph); X[:, 7] = np.cos(ph)
    return X, bye // STEP, arr // STEP


def mu_from(logits_row, b0):
    x = torch.tensor(float(b0), requires_grad=True); V = value(x, logits_row); V.backward(); return -x.grad.item()


def run(seed):
    net = train(seed); res = {}
    pbar_logit = float(np.log(PBAR / (1 - PBAR)))
    for S in [10, 60, 180, 1240]:
        X, tb, ta = test_stream(S, seed)
        with torch.no_grad(): lg, _ = net(torch.tensor(X)[None])
        lg = lg[0]
        r = {}
        for s in [0.0, 0.25, 0.5, 0.75, 1.0]:
            mix = lambda row: torch.logit((1 - s) * torch.sigmoid(row) + s * PBAR, eps=1e-6)
            mu_arr = mu_from(mix(lg[ta]), X[ta, 0])
            r[f"L_A{s}"] = Lstar(mu_arr)
            if s in (0.0, 1.0):
                call = None
                for t in range(tb, min(tb + 300, len(X))):
                    if mu_from(mix(lg[t]), X[t, 0]) >= THETA: call = (t - tb) * 5; break
                r[f"call_A{s}"] = call
        # lesion B: mu replaced by its mean over the test day (day 3 window)
        day = range(2 * SPD, min(3 * SPD, len(X)))
        mu_mean = float(np.mean([mu_from(lg[t], X[t, 0]) for t in day]))
        r["L_B"] = Lstar(mu_mean); r["mu_arr_intact"] = mu_from(lg[ta], X[ta, 0])
        res[S] = r
    return dict(seed=seed, res=res)


if __name__ == "__main__":
    for s in [int(a) for a in sys.argv[1:]]:
        print(json.dumps(run(s)), flush=True)
