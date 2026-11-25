"""Screening runner for the published simple baselines (harness v2). One command scores every baseline row on the
pilot's validation interactions and writes research/runs/screen/<row>.json with run time and peak memory.
Usage:  uv run python run_screen.py            (L2L and REACT rows; needs pilot_v2 downloaded; refuses otherwise)
        uv run python run_screen.py --e3       (E3 coupling rows on e3_subset_v2; about 15 min per row with 8 processes)
        uv run python run_screen.py --check    (code check on the local sample pair only; never a result)"""
import json, os, re, resource, sys, time
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baselines as B, loader as Ld, metrics as M

H = "research/harness/"; OUT = "research/runs/screen/"
pat = re.compile(r"^(V\d+_S\d+_I\d+)_P")
SEED = 0

def pairs_from(entries):
    """entries: [label, url_split, file_id]; returns [(label, split, speaker_file, listener_file)] both directions."""
    inter = {}
    for label, split, f in entries: inter.setdefault(pat.match(f).group(1), []).append((label, split, f))
    out = []
    for k, mem in inter.items():
        if len(mem) != 2: continue
        (l1, s1, f1), (l2, s2, f2) = mem; out += [(l1, s1, f1, f2), (l2, s2, f2, f1)]
    return out

def load_pair(p):
    label, split, fs, fl = p; spk, vs = Ld.load_aus(label, split, fs); lis, vl = Ld.load_aus(label, split, fl)
    n = min(len(spk), len(lis)); return spk[:n], lis[:n], vs[:n] & vl[:n]

def seq256(windows):
    """UNSPEC (HARNESS v2 S2): 256-frame sequences from 4 consecutive 64-frame windows; incomplete groups dropped."""
    k = len(windows) // 4; return windows[:4 * k].reshape(k, 256, windows.shape[-1])

def score_l2l(name, pred_fn, val_pairs, bank, cent, rng):
    t0 = time.time(); P, G, S = [], [], []
    for p in val_pairs:
        spk, lis, v = load_pair(p); st = B.valid_starts(v, B.T_WIN)
        if len(st) == 0: continue
        P.append(pred_fn(spk, lis, st, rng)); G.append(np.stack([lis[s:s + B.T_WIN] for s in st])); S.append(np.stack([spk[s:s + B.T_WIN] for s in st]))
    P, G, S = np.concatenate(P), np.concatenate(G), np.concatenate(S)
    try: (fd, fb1), (pfd, fb2) = M.frechet(P, G), M.p_fd(P, S, G)
    except AssertionError: fd = pfd = None; fb1 = fb2 = False   # too few windows for a T*d covariance (check mode)
    lags = [M.tlcc_l2l(p_, s_)[0] for p_, s_ in zip(seq256(P), seq256(S))]
    floor = [M.tlcc_l2l(p_, s_)[0] for p_, s_ in zip(seq256(P), seq256(S)[rng.permutation(len(seq256(S)))])]
    return dict(row=name, n_windows=len(P), L2=M.l2(P, G), FD=fd, P_FD=pfd, fd_fallback=bool(fb1 or fb2),
                variation=M.variation(P), SI=M.si(seq256(P), cent), TLCC_mean_lag=float(np.nanmean(lags)),
                TLCC_shuffled_floor=float(np.nanmean(floor)), TLCC_undefined=int(np.isnan(lags).sum()),
                seconds=round(time.time() - t0, 1))

def score_react(name, gen, val_pairs, rng, clip=M.REACT_CLIP):
    """REACT metrics on non-overlapping fully valid clips of `clip` frames; 10 samples per clip (num_pred=10)."""
    t0 = time.time(); P, SP = [], []
    for p in val_pairs:
        spk, lis, v = load_pair(p); st = B.valid_starts(v, clip, first=0)
        if len(st): P.append(gen(spk, lis, st, rng)); SP.append(np.stack([spk[s:s + clip] for s in st]))
    P, SP = np.concatenate(P), np.concatenate(SP)
    out = dict(row=name, n_clips=len(P), FRVar=M.frvar(P), FRDiv_SMSE=M.s_mse(P), FRDvs=M.frdvs(P) if len(P) > 1 else None)
    for lagf in (49, 59):
        for pub in (True, False):
            v_, nans = M.frsyn(P, SP, lag_frames=lagf, published_path=pub)
            out[f"FRSyn_lag{lagf}_{'published' if pub else 'serial'}"] = v_; out[f"FRSyn_lag{lagf}_nan_lags"] = nans
    out["seconds"] = round(time.time() - t0, 1); return out

def full_series(method, spk, lis, valid, bank, rng):
    """Whole-series prediction for E3. Window methods tile 64-frame windows at the shared valid starts; frames not
    covered are marked invalid. Returns (pred, pred_valid)."""
    T, d = spk.shape; pv = np.zeros(T, bool); pred = np.zeros((T, d), np.float32)
    if method == "GT_listener": return lis, valid.copy()
    if method == "B4_L2L_Mirror": return spk, valid.copy()
    if method == "B5_L2L_DelayedMirror":
        pred[B.DELAY:] = spk[:-B.DELAY]; pv[B.DELAY:] = valid[:-B.DELAY] & valid[B.DELAY:]; return pred, pv
    st = B.valid_starts(valid, B.T_WIN)
    W = {"B2_L2L_Random": lambda: B.l2l_random(bank, spk, st, rng), "B3_L2L_NN": lambda: B.l2l_nn(bank, spk, st)}[method]()
    for s, w in zip(st, W): pred[s:s + B.T_WIN] = w; pv[s:s + B.T_WIN] = True
    return pred, pv

E3_ROWS = ("GT_listener", "B2_L2L_Random", "B3_L2L_NN", "B4_L2L_Mirror", "B5_L2L_DelayedMirror")
def _e3_job(args):
    method, p, bank, seed = args
    spk, lis, v = load_pair(p); pred, pv = full_series(method, spk, lis, v, bank, np.random.default_rng(seed))
    r = M.e3_test(pred, spk, 60, 60, va=pv, vb=v, n_surr=1000, seed=seed); r.update(method=method, pair=p[2] + "<-" + p[3]); return r

def run_e3(val_pairs_e3, bank, check=False):
    """E3 on one direction per interaction (listener = the second file id in sorted order). Median and B_MeanFr are
    constant: recorded 'undefined (constant)'. Returns per-row pass share."""
    n_surr_note = "1000 surrogates of each type"; rows = {}
    for method in E3_ROWS:
        t0 = time.time(); jobs = [(method, p, bank, SEED + i) for i, p in enumerate(val_pairs_e3)]
        if check: jobs = jobs[:1]
        with Pool(8) as pool: res = pool.map(_e3_job, jobs)
        ok = [r for r in res if not r["excluded"]]
        rows[method] = dict(row="E3_" + method, n=len(res), n_excluded=len(res) - len(ok), pass_share=float(np.mean([r["passes"] for r in ok])) if ok else None,
                            mean_obs=float(np.mean([r["obs"] for r in ok])) if ok else None, per_pair=res, seconds=round(time.time() - t0, 1), note=n_surr_note)
        print(json.dumps({k: v for k, v in rows[method].items() if k != "per_pair"}, default=float))
        if not check: json.dump(rows[method], open(OUT + "E3_" + method + ".json", "w"), indent=1, default=float)
    for c in ("B1_L2L_Median", "B9_REACT_MeanFr"): rows[c] = dict(row="E3_" + c, result="undefined (constant)")
    return rows

def main(check=False, e3=False):
    os.makedirs(OUT, exist_ok=True); rng = np.random.default_rng(SEED)
    if check:
        local = [["naturalistic", "dev", "V00_S0080_I00000377_P0115"], ["naturalistic", "dev", "V00_S0080_I00000377_P0116"]]
        val_pairs = pairs_from(local); train_pairs = val_pairs; bank = B.TrainBank.__new__(B.TrainBank)
        spk, lis, v = load_pair(val_pairs[0]); st = B.valid_starts(v, B.T_WIN, first=0)
        bank.spk = np.stack([spk[s:s + 64] for s in st]); bank.lis = np.stack([lis[s:s + 64] for s in st])
        bank.median = np.median(bank.lis.reshape(-1, 23), 0); bank.mean_seq = bank.lis.mean(0); bank.mean_fr = bank.mean_seq.mean(0)
        print("CHECK MODE: bank built from the query pair itself (NN will self-match); numbers are not results")
    else:
        S = json.load(open(H + "splits_v3.json")); pilot = json.load(open(H + "pilot_v2.json"))
        val = set(S["files"]["val"]); train = set(S["files"]["train"])
        for label, split, f in pilot:
            assert os.path.exists(f"{Ld.ROOT}/{label}/{split}/movement/FAUValue/{f}.npy"), "pilot not downloaded"
        val_pairs = pairs_from([e for e in pilot if e[2] in val]); train_pairs = pairs_from([e for e in pilot if e[2] in train])
        bank = B.TrainBank(train_pairs, query_files=[p[2] for p in val_pairs])
    cent = M.fit_si_kmeans(bank.lis.reshape(-1, bank.lis.shape[-1]))
    rows = {
        "GT_listener": lambda spk, lis, st, r: np.stack([lis[s:s + B.T_WIN] for s in st]),
        "B1_L2L_Median": lambda spk, lis, st, r: B.l2l_median(bank, spk, st),
        "B2_L2L_Random": lambda spk, lis, st, r: B.l2l_random(bank, spk, st, r),
        "B3_L2L_NN": lambda spk, lis, st, r: B.l2l_nn(bank, spk, st),
        "B4_L2L_Mirror": lambda spk, lis, st, r: B.l2l_mirror(spk, st),
        "B4b_L2L_Mirror_smooth5": lambda spk, lis, st, r: B.l2l_mirror(spk, st, smooth_k=5),
        "B5_L2L_DelayedMirror": lambda spk, lis, st, r: B.l2l_delayed_mirror(spk, st),
    }
    results = []
    for name, fn in rows.items():
        res = score_l2l(name, fn, val_pairs, bank, cent, rng)
        res["peak_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20, 1)
        res["check_mode"] = check; results.append(res); print(json.dumps(res, default=float))
        if not check: json.dump(res, open(OUT + name + ".json", "w"), indent=1, default=float)
    clip = 256 if check else M.REACT_CLIP   # check mode: the 2640-frame sample holds too few 750-frame clips for FRDvs
    if check:
        b7 = B.TrainBank.__new__(B.TrainBank); spk, lis, v = load_pair(val_pairs[0]); st = B.valid_starts(v, clip, first=0)
        b7.spk = np.stack([spk[s:s + clip] for s in st]); b7.lis = np.stack([lis[s:s + clip] for s in st])
        b7.mean_seq = np.concatenate([b7.spk, b7.lis]).mean(0); b7.mean_fr = b7.mean_seq.mean(0)
    else:
        b7 = B.TrainBank(train_pairs, query_files=[p[2] for p in val_pairs], length=clip)
    rrows = {
        "GT_REACT_listener": lambda spk, lis, st, r: np.repeat(np.stack([lis[s:s + clip] for s in st])[:, None], 10, 1),
        "B6_REACT_Random": lambda spk, lis, st, r: B.react_random(len(st), spk.shape[1], r, clip),
        "B7_REACT_Mime": lambda spk, lis, st, r: B.react_mime(spk, st, clip),
        "B8_REACT_MeanSeq": lambda spk, lis, st, r: B.react_mean_seq(b7, len(st)),
        "B9_REACT_MeanFr": lambda spk, lis, st, r: B.react_mean_fr(b7, len(st), clip),
    }
    for name, gen in rrows.items():
        res = score_react(name, gen, val_pairs, rng, clip=clip)
        res["peak_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20, 1)
        res["check_mode"] = check; res["clip_frames"] = clip; results.append(res); print(json.dumps(res, default=float))
        if not check: json.dump(res, open(OUT + name + ".json", "w"), indent=1, default=float)
    if e3:
        sub = set(json.load(open(H + "e3_subset_v2.json"))) if not check else None
        e3_pairs = [p for p in val_pairs if (check or pat.match(p[2]).group(1) in sub) and p[3] > p[2]]
        run_e3(e3_pairs, bank, check=check)
    return results

if __name__ == "__main__":
    main(check="--check" in sys.argv, e3="--e3" in sys.argv)
