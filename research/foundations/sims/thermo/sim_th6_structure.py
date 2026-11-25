"""TH6: need field over entities + need-conditioned attention vs collapsed gauges. See PREDICTIONS.md."""
import json
import numpy as np
ENT = ["A", "B", "C", "X", "Y"]; PEOPLE = [0, 1, 2]; TOPICS = [3, 4]
BSTAR = np.array([0.8, 0.8, 0.8, 0.6, 0.6]); T = 0.05
rng = np.random.default_rng(0)
# episodes
eps = []
for p in PEOPLE:
    for _ in range(20):
        t = rng.choice(TOPICS); k = np.zeros(5); k[p] = 0.3; k[t] = 0.2; k += rng.normal(0, 0.05, 5)
        eps.append(dict(person=p, topic=int(t), key=k))
cues = {"A_face": np.array([0.3, 0, 0, 0, 0.]), "B_photo": np.array([0, 0.3, 0, 0, 0.]), "X_mention": np.array([0, 0, 0, 0.2, 0]), "Y_mention": np.array([0, 0, 0, 0, 0.2])}
acts = {"talk_A": np.array([0.3, 0, 0, 0, 0.]), "message_B": np.array([0, 0.3, 0, 0, 0.]), "open_X": np.array([0, 0, 0, 0.2, 0]), "open_Y": np.array([0, 0, 0, 0, 0.2]), "rest": np.zeros(5)}

def force_field(b): return -2 * (b - BSTAR)
def collapse_b(b): return np.array([b[PEOPLE].mean(), b[TOPICS].mean()])
def collapse_k(k): return np.array([k[PEOPLE].sum(), k[TOPICS].sum()])
def force_col(bc): return -2 * (bc - np.array([0.8, 0.6]))

def attend(F, keys):
    s = np.array([F @ k for k in keys]) / T; s -= s.max(); p = np.exp(s); return p / p.sum()

def analyse(b):
    F = force_field(b); Fc = force_col(collapse_b(b))
    pe = attend(F, [e["key"] for e in eps]); pec = attend(Fc, [collapse_k(e["key"]) for e in eps])
    top = np.argsort(-pe)[:5]; topc = np.argsort(-pec)[:5]
    pc = attend(F, list(cues.values())); pcc = attend(Fc, [collapse_k(k) for k in cues.values()])
    pa = attend(F, list(acts.values())); pac = attend(Fc, [collapse_k(k) for k in acts.values()])
    by_person = lambda p_, P: [float(sum(P[i] for i, e in enumerate(eps) if e["person"] == q)) for q in PEOPLE]
    return dict(normF=float(np.linalg.norm(F)), top5_people=[eps[i]["person"] for i in top], top5_people_collapsed=[eps[i]["person"] for i in topc],
                ranks_collapsed=np.argsort(-pec).tolist(),
                mass_by_person=by_person(None, pe), mass_by_person_collapsed=by_person(None, pec),
                cues=dict(zip(cues, pc.round(4).tolist())), cues_collapsed=dict(zip(cues, pcc.round(4).tolist())),
                acts=dict(zip(acts, pa.round(4).tolist())), acts_collapsed=dict(zip(acts, pac.round(4).tolist())))

b1 = np.array([0.95, 0.0, 0.15, 0.98, 0.0])
b2 = np.array([0.0, 0.95, 0.15, 0.98, 0.0])
out = {"scenario": analyse(b1), "swapped": analyse(b2)}
# TH6-5 participation ratio over a simulated week (1-min steps)
r = np.random.default_rng(1); b = np.array([0.5, 0.5, 0.5, 0.5, 0.5]); traj = []
for day in range(7):
    present = {p: (r.random() < 0.5, r.integers(60, 181), r.integers(8 * 60, 20 * 60)) for p in PEOPLE}
    for m in range(1440):
        for p in PEOPLE:
            on, dur, start = present[p]
            if on and start <= m < start + dur: b[p] += (1 - b[p]) / 60
            else: b[p] -= b[p] / 360
        topic = r.choice(TOPICS) if m % 60 == 0 else (topic if m else 3)
        for t in TOPICS:
            if t == topic and any(present[p][0] and present[p][2] <= m < present[p][2] + present[p][1] for p in PEOPLE): b[t] += 2 * (1 - b[t]) / 60
            else: b[t] -= b[t] / 720
        traj.append(b.copy())
traj = np.array(traj)
def pr(X):
    ev = np.linalg.eigvalsh(np.cov(X.T)); return float(ev.sum() ** 2 / (ev ** 2).sum())
out["PR_field"] = pr(traj); out["PR_collapsed"] = pr(np.stack([traj[:, PEOPLE].mean(1), traj[:, TOPICS].mean(1)], 1))
print(json.dumps(out, indent=1))
