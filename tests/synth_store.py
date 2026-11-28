"""Synthetic sessions written into a temporary feature store (tests only; constructed arrays, never evidence about
behaviour or people). Every stream is a small smooth random signal of its schema's width."""
from __future__ import annotations

import dataclasses

import numpy as np

from engine.config import operator as op
from engine.config.channels import TABLE
from engine.memory.store import SCHEMAS, Store
from engine.state import types as T
from synth import lp

LP, CR = TABLE.index("LP"), TABLE.index("CR")
GAZE = tuple(TABLE.index(c) for c in ("HG", "VG", "YAW"))
DAY = 86400.0


def answered(**over):
    sw = dict(op.SWITCHES)
    for k in ("feature_retention_days", "keep_slot_snippets", "nightly_schedule"):
        sw[k] = dataclasses.replace(sw[k], answered=True)
    for k, v in over.items():
        sw[k] = dataclasses.replace(sw[k], value=v, answered=True)
    return sw


def smooth(n, w, r, tau_rows=5.0, lo=0.0, hi=1.0):
    x = lp(r.uniform(lo, hi, (n, w)), tau_rows, 1.0)
    return np.clip(x, lo, hi)


def write_session(store: Store, sid: str, identity: str = "op", t0: float = 0.0, seconds: float = 60.0, seed: int = 0,
                  flag=None, his_face=None, Dp_scale: float = 0.04, Dp_word_scale: float = 0.08, extra_quiet_s: float = 0.0):
    """One closed session. `his_face(u)` may rewrite his face stream before it is stored (e.g. more smiling)."""
    r = np.random.default_rng(seed)
    n2 = int(seconds * 2)
    n30 = int(seconds * 30)
    n10 = int(seconds * 10)
    w = store.open_session(sid, identity, t0)
    u = smooth(n30, 33, r, 15.0)
    if his_face is not None:
        u = his_face(u)
    w.append("u", u)
    w.append("f_der", smooth(n30, 5, r, 15.0))
    w.append("breath", smooth(int(seconds * 10), 2, r))
    for s in ("y", "y_bar", "rendered"):
        w.append(s, smooth(n30, 33, np.random.default_rng(seed + 7), 15.0) * 0.3)
    own10 = smooth(n10, 33, np.random.default_rng(seed + 11), 5.0) * 0.4
    w.append("own_face", own10)
    own2 = own10[::5][:n2]
    M = np.random.default_rng(99).normal(0, 0.3, (33, 3))
    loads = np.clip(own2 @ M + 0.2, 0.0, 1.0)
    w.append("own_loads", loads)
    body = np.zeros((n2, 12))
    body[:, 0] = np.linspace(0.8, 0.75, n2)                 # E
    body[:, 1:6] = smooth(n2, 5, r) * 0.3
    body[:, 6] = 0.05                                       # D
    body[:, 7] = smooth(n2, 1, r)[:, 0] * Dp_scale          # Dp
    body[:, 8] = smooth(n2, 1, r)[:, 0] * Dp_word_scale     # Dp_word
    body[:, 9] = smooth(n2, 1, r)[:, 0] * 0.1               # h_word
    body[:, 10] = (r.uniform(size=n2) > 0.9) * r.uniform(0.2, 0.8, n2)   # V_F
    body[:, 11] = (r.uniform(size=n2) > 0.95) * 0.5         # drop_amp
    w.append("body", body)
    w.append("drivers", smooth(n2, 7, r))
    w.append("xi_A", smooth(n2, 36, r, 5.0, -0.2, 0.2))
    w.append("cone_lateral", smooth(n2, 33, r, 5.0, -0.2, 0.2))
    w.append("z_T", smooth(n2, 161, r, 5.0, -1.0, 1.0))
    w.append("voice_phrase", smooth(10, 8, r))
    w.append("state_T", smooth(n2, 40, r))
    words = ("we planted beans", "the train was late", "my sister called", "it rained all day", "a long walk")
    lines = 0
    for i, t in enumerate(np.arange(3.0, seconds - 4.0, 7.0)):
        txt = words[i % len(words)]
        utt = T.Utterance("him", (), txt, t0 + float(t), txt)
        w.append_transcript(T.his_text(utt), [(x, t0 + float(t)) for x in txt.split()])
        w.append_event(kind="turn_event", t=t0 + float(t), turn="his_utterance_end")
        if i % 2:
            w.append_transcript(T.agent_text(T._chosen_reply("I see.", t0 + float(t) + 1.0)), [("I", t0 + t + 1.0)])
        lines += 1
    for t in np.arange(5.0, seconds, 11.0):
        w.append_event(kind="drop_event", t=t0 + float(t), amp=0.3, term="K")
    w.append_event(kind="report", t=t0 + 20.0, utt=2, of=0, separated=True)
    w.append_event(kind="report", t=t0 + 25.0, utt=3, of=1, separated=False)
    w.append_omega(t=t0 + 4.0, drafts=["I see.", "Go on."], winner=0, timings={"first_sentence_s": 1.2},
                   telemetry={"tokens": 1800})
    if extra_quiet_s:
        k = int(extra_quiet_s * 2)
        tail = np.repeat(body[-1:], k, 0)
        tail[:, 9:12] = 0.0
        w.append("body", tail)
    if flag:
        w.flag(flag)
    w.close(t0 + seconds + extra_quiet_s)
    return w


__all__ = ["answered", "write_session", "SCHEMAS", "DAY", "LP", "CR", "GAZE"]
