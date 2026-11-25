"""CS1: costate field vs deficit field vs collapsed. See PREDICTIONS.md (third batch)."""
import json
import numpy as np
ENT = ["A", "B", "C", "X", "Y"]; PEOPLE = [0, 1, 2]; TOPICS = [3, 4]; T = 0.05
rng = np.random.default_rng(0)
eps = []
for p in PEOPLE:
    for _ in range(20):
        t = rng.choice(TOPICS); k = np.zeros(5); k[p] = 0.3; k[t] = 0.2; k += rng.normal(0, 0.05, 5)
        eps.append(dict(person=p, key=k))
def onehot(i, v): k = np.zeros(5); k[i] = v; return k
cues = {"A_face": onehot(0, .3), "B_photo": onehot(1, .3), "C_photo": onehot(2, .3), "X_mention": onehot(3, .2), "Y_mention": onehot(4, .2)}
acts = {"talk_A": onehot(0, .3), "message_B": onehot(1, .3), "message_C": onehot(2, .3), "open_X": onehot(3, .2), "open_Y": onehot(4, .2), "rest": np.zeros(5)}
topic_q = 2 * (np.array([0.6, 0.6]) - np.array([0.98, 0.0]))
q_cost = np.r_[[-0.0497, 0.3062, 0.7081], topic_q]
q_def = np.r_[2 * (0.8 - np.array([0.95, 0.0, 0.15])), topic_q]
def att(q, keys):
    s = np.array([q @ k for k in keys]) / T; s -= s.max(); p = np.exp(s); return p / p.sum()
def coll_k(k): return np.array([k[PEOPLE].sum(), k[TOPICS].sum()])
q_col = np.array([np.mean([-0.0497, 0.3062, 0.7081]), topic_q.mean()])
out = {}
for name, q, ck in [("costate_field", q_cost, None), ("deficit_field", q_def, None), ("collapsed", q_col, coll_k)]:
    f = (lambda k: k) if ck is None else ck
    pe = att(q, [f(e["key"]) for e in eps]); pc = att(q, [f(k) for k in cues.values()]); pa = att(q, [f(k) for k in acts.values()])
    out[name] = dict(top5_people=[ENT[eps[i]["person"]] for i in np.argsort(-pe)[:5]], cues=dict(zip(cues, pc.round(4).tolist())), acts=dict(zip(acts, pa.round(4).tolist())))
print(json.dumps(out, indent=1))
