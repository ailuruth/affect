"""The nightly learning steps (spec §1.9 steps 1-8, §1.10), on the learned parts' fixed-shape stubs.

Run by engine/memory/replay.py, in this order, on the night's sessions (2-Hz moments, each weighted by the S48
sample weight; the learning rate scaled by exp(-0.5 r_bar); gradients clipped to 1; pull 0.1 to theta_0;
engine/learn/weights.py). After every step every learned part is projected onto its set and checked
(engine/learn/projections.py: A6, A7, A8); a step that leaves a set is undone (its parts restored to their values
before the step) and logged with the assertion's id.

  1  world model M by likelihood           not built (M8 needs the world model of engine/model/): skipped, reported
  2  Pi-tilde on the agent's own pairs     own face -> own loads (V, A, T), weighted least squares, pull 0.1 to its
                                           start; reader_own on the own read channels, reader_his (the same inverse
                                           of the agent's own body, applied to his face) on his read channels; no
                                           partner anchor: both are fitted on the agent's own data only
  3  calibration, H_id, adapter, word->V   calibration (session end): b_read from his low-need moments (Dp_word <
                                           0.05), tau 1 in the first three sessions, then tau 6, or tau 60 when the
                                           session's read V-hat > 0.20 (slow toward aversive readings, S38); sigma_id
                                           = 1.4826 MAD over the last 6 sessions, within [0.25, 4] sigma_ref; sigma_ref
                                           the spread of the agent's own rendered channels. H_id: ridge 2 from his
                                           calibrated face over the 20 s after each of his utterances to the frozen
                                           population reader's decoding of those words, once >= 400 utterances.
                                           Adapter: separated, partner-initiated reports only (S40). Word -> V: his
                                           words to the threat reflex's load over the 3 s after them (teacher S41)
  4  A by likelihood; W and Gamma(3,4)     A's own likelihood head is not specified beyond "by likelihood" and reads
     by L_A, then projection               the world model's z_T: A stays at its stub; W and Gamma(3,4) by L_A (the
                                           agent's own innate display 2 s ahead), projected after every step
  5  Delta by L_display                    own legibility through Pi-tilde, ||delta||^2; own-display mask
  6  L_w (words-only partner model)        not built: skipped, reported
  7  draft scorer, retrieval query by J    J needs the world model's rollout: skipped, the stubs keep their shapes
  8  omega per session                     omega_rule (S37), omega_g <- omega_g + (s - omega_g)/60
  +  E restored                            the carried energy is raised to its set point (only here, spec §1.9)
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field

import numpy as np

from engine.config.channels import TABLE
from engine.config.innate import ENTRIES
from engine.learn import objectives as O
from engine.learn import projections as PJ
from engine.learn import weights as WB
from engine.routes import appraisal as AP
from engine.routes import cone as C
from engine.routes.free_display import MASK_RISE_ONLY, MASK_ZERO, pi0_matrix
from engine.routes.learned_t import OMEGA_PRIOR, OWN_READ_IDX, READ_IDX, omega_target, omega_update
from engine.state import readers as R
from engine.state.drives import DRIVES

N = len(TABLE.codes)
SGD = ENTRIES["replay_sgd"].value
WIN = ENTRIES["replay_windows_s"].value
HID_MIN = int(ENTRIES["head_id_min_utterances"].value)
HID_RIDGE = float(ENTRIES["head_id_ridge"].value)
CAL0 = ENTRIES["calib_initial"].value
CALT = ENTRIES["calib_read_tau_sessions"].value
SIG_FLOOR = float(ENTRIES["calib_sigma_floor"].value)
MAD = float(ENTRIES["calib_mad_factor"].value)
SIG_N = int(ENTRIES["calib_sigma_sessions"].value)
E_SET = float(ENTRIES["drive_terms"].value["E"][0])
SLOW_HZ = float(ENTRIES["loop_rates_hz"].value["slow"])
AHEAD = int(round(WIN["anticipation"] * SLOW_HZ))
BODY = ("E", "A", "V", "K", "P", "I", "D", "Dp", "Dp_word", "h_word", "V_F", "drop_amp")
COL = {c: i for i, c in enumerate(BODY)}
CREDIT_TERMS = ("K", "P", "I")


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class SessionData:
    """One replayed session at the 2-Hz clock (every stream aligned to the body snapshot's ticks)."""
    sid: str
    identity: str
    t0: float
    body: np.ndarray            # (n, 12) BODY columns
    own_loads: np.ndarray       # (n, 3)
    drivers: np.ndarray         # (n, 7) the Pi_0 display drivers
    xi_A: np.ndarray            # (n, 36)
    lateral: np.ndarray         # (n, 33) his centred 20-s cone trace
    z_T: np.ndarray             # (n, 161) Delta's T inputs
    own_face: np.ndarray        # (n, 33) the agent's own face (observed)
    u: np.ndarray               # (n, 33) his face at the ticks (an input only)
    rendered: np.ndarray        # (n, 33) the agent's rendered output at the ticks
    his: list = field(default_factory=list)       # [(text, t_end)] his lines
    events: list = field(default_factory=list)

    @property
    def n(self) -> int:
        return self.body.shape[0]

    def weights(self) -> np.ndarray:
        return WB.sample_weight(self.body[:, COL["Dp_word"]])

    def tick(self, t: float) -> int:
        return int(np.clip(round((t - self.t0) * SLOW_HZ), 0, max(self.n - 1, 0)))

    def nbytes(self) -> int:
        return sum(getattr(self, a).nbytes for a in ("body", "own_loads", "drivers", "xi_A", "lateral", "z_T",
                                                     "own_face", "u", "rendered"))


def new_person() -> dict:
    n = len(READ_IDX)
    return {"omega": list(OMEGA_PRIOR), "b_read": [0.0] * n, "sigma_id": [0.0] * n, "sigma_hist": [],
            "sessions": 0, "utterances": 0}


@dataclass
class Night:
    L: object
    persons: dict                           # {"agent": {...}, "persons": {identity: {...}}}
    sessions: list
    check: object = None                    # budget check callable (raises BudgetExceeded)
    theta0: dict = field(default_factory=dict)
    lr: float = 1.0
    dyad_prior: object = None
    log: list = field(default_factory=list)

    def person(self, ident: str) -> dict:
        return self.persons["persons"].setdefault(ident, new_person())

    def omegas(self) -> list:
        return [p["omega"] for p in self.persons["persons"].values()]

    def tick_check(self) -> None:
        if self.check is not None:
            self.check()


# ---------------------------------------------------------------------------------------------------- parameters
def param_items(L) -> dict:
    """name -> (object, attribute) of every array replay may write."""
    items = {}
    for part in ("reader_own", "reader_his", "word_v"):
        for a in ("W", "b"):
            items[f"{part}.{a}"] = (getattr(L, part), a)
    items["appraisal.Wsel"] = (L.appraisal, "Wsel")
    items["appraisal.learned_bases"] = (L.appraisal, "learned_bases")
    for a in ("W1", "W2", "syn"):
        items[f"delta.{a}"] = (L.delta, a)
    items["retrieval_query.W"] = (L.retrieval_query, "W")
    for ident, h in L.head_id.items():
        items[f"head_id.{ident}.W"], items[f"head_id.{ident}.b"] = (h, "W"), (h, "b")
    for ident, ad in L.adapter.items():
        items[f"adapter.{ident}.W"], items[f"adapter.{ident}.b"] = (ad, "W"), (ad, "b")
    return items


TRAINED_PARTS = ("reader_own", "reader_his", "word_v", "appraisal", "delta", "retrieval_query")


def export(L, theta0: dict) -> dict:
    out = {k: np.array(getattr(o, a), dtype=np.float64) for k, (o, a) in param_items(L).items()}
    out.update({"theta0." + k: np.array(v, dtype=np.float64) for k, v in theta0.items()})
    for p in TRAINED_PARTS:
        out["trained." + p] = np.array([1.0 if getattr(L, p).trained else 0.0])
    for ident, h in L.head_id.items():
        out[f"trained.head_id.{ident}"] = np.array([1.0 if h.trained else 0.0])
    for ident, ad in L.adapter.items():
        out[f"trained.adapter.{ident}"] = np.array([1.0 if ad.trained else 0.0])
    return out


def restore(L, arrays: dict) -> dict:
    """Write saved arrays into L (creating per-person heads as needed); returns theta0."""
    for k in arrays:
        parts = k.split(".")
        if parts[0] in ("head_id", "adapter") and len(parts) == 3:
            d = getattr(L, parts[0])
            if parts[1] not in d:
                d[parts[1]] = R.HeadId(len(READ_IDX)) if parts[0] == "head_id" else R.Adapter()
    items = param_items(L)
    for k, v in arrays.items():
        if k in items:
            o, a = items[k]
            setattr(o, a, np.array(v, dtype=np.float64).reshape(np.shape(getattr(o, a))))
    for k, v in arrays.items():
        if k.startswith("trained."):
            path = k.split(".")[1:]
            obj = getattr(L, path[0]) if len(path) == 1 else getattr(L, path[0])[path[1]]
            obj.trained = bool(v[0] > 0.5)
    return {k[len("theta0."):]: np.array(v) for k, v in arrays.items() if k.startswith("theta0.")}


def snapshot(L, names) -> dict:
    items = param_items(L)
    return {k: copy.deepcopy(getattr(*items[k])) for k in items if k.split(".")[0] in names}


def put_back(L, snap: dict) -> None:
    items = param_items(L)
    for k, v in snap.items():
        if k in items:
            setattr(items[k][0], items[k][1], v)


def _theta0(night: Night, name: str, value) -> np.ndarray:
    if name not in night.theta0:
        night.theta0[name] = np.array(value, dtype=np.float64)
    return night.theta0[name]


def _descend(night: Night, params: dict, grad_fn, after=None) -> float:
    """SGD with the learning biases on {name: (obj, attr)}; grad_fn() -> (loss, {name: grad}). Returns last loss."""
    lr = float(SGD["lr"]) * night.lr
    loss = float("nan")
    for _ in range(int(SGD["steps"])):
        night.tick_check()
        loss, grads = grad_fn()
        for name, (o, a) in params.items():
            th = getattr(o, a)
            setattr(o, a, WB.biased_step(th, grads[name], _theta0(night, name, th), lr))
        if after is not None:
            after()
    return loss


def _stack(sessions, attr):
    xs = [getattr(s, attr) for s in sessions if s.n]
    return np.concatenate(xs) if xs else None


# ---------------------------------------------------------------------------------------------------- step 2
def step_pi_tilde(night: Night) -> str:
    S = [s for s in night.sessions if s.n]
    if not S:
        return "no data"
    Y, w = _stack(S, "own_loads"), np.concatenate([s.weights() for s in S])
    F = _stack(S, "own_face")
    out = []
    for name, idx in (("reader_own", OWN_READ_IDX), ("reader_his", READ_IDX)):
        part = getattr(night.L, name)
        X = F[:, list(idx)]

        def g(part=part, X=X, name=name):
            loss, dW, db = O.wls_grad(X, Y, w, part.W, part.b)
            return loss, {f"{name}.W": dW, f"{name}.b": db}
        loss = _descend(night, {f"{name}.W": (part, "W"), f"{name}.b": (part, "b")}, g)
        part.trained = True
        out.append(f"{name} loss {loss:.4g}")
    return "; ".join(out)


# ---------------------------------------------------------------------------------------------------- step 3
def calibrated(x, b_read, sigma_id, sigma_ref):
    """x~ = ref + (x - b_read) sigma_ref / max(sigma_id, 0.25 sigma_ref), ref = the agent's rest (0)."""
    sr = np.asarray(sigma_ref, dtype=np.float64)
    den = np.maximum(np.asarray(sigma_id, dtype=np.float64), SIG_FLOOR * sr)
    gain = np.divide(sr, den, out=np.zeros_like(sr), where=den > 0)
    return (np.asarray(x) - np.asarray(b_read)) * gain


def step_calibration(night: Night) -> str:
    agent = night.persons["agent"]
    hist = agent.setdefault("sigma_ref_hist", [])
    for s in night.sessions:
        if s.n:
            r = s.rendered[:, list(READ_IDX)]
            hist.append(list(MAD * np.median(np.abs(r - np.median(r, 0)), 0)))
    del hist[:-SIG_N]
    sigma_ref = np.median(np.array(hist), 0) if hist else np.zeros(len(READ_IDX))
    agent["sigma_ref"] = list(sigma_ref)
    done = 0
    for s in night.sessions:
        if not s.n:
            continue
        p = night.person(s.identity)
        u = s.u[:, list(READ_IDX)]
        low = s.body[:, COL["Dp_word"]] < CAL0["need_max"]
        sample = u[low] if np.any(low) else u
        m_s = np.median(sample, 0)
        v_hat = float(np.mean(np.clip(u @ night.L.reader_his.W + night.L.reader_his.b, 0.0, 1.0)[:, 0]))
        need = float(np.mean(s.body[:, COL["Dp_word"]]))
        if p["sessions"] < CAL0["sessions"] and need < CAL0["need_max"]:
            tau = CAL0["tau_sessions"]
        else:
            tau = CALT["high_need"] if v_hat > CALT["V_threshold"] else CALT["low_need"]
        b = np.asarray(p["b_read"], dtype=np.float64)
        p["b_read"] = list(b + (m_s - b) / tau)
        p["sigma_hist"] = (p["sigma_hist"] + [list(MAD * np.median(np.abs(sample - m_s), 0))])[-SIG_N:]
        sig = np.median(np.array(p["sigma_hist"]), 0)
        p["sigma_id"] = list(np.maximum(sig, SIG_FLOOR * sigma_ref))      # at most x4 amplification
        p["sessions"] += 1
        p["utterances"] += len(s.his)
        done += 1
    return f"{done} session(s) calibrated"


def _decode(L, text: str):
    e = np.asarray(L.enc.encode(text), dtype=np.float64)
    tc = R.topic_code(L.enc.topic(text))
    return e, tc, np.asarray(L.pop(e, tc), dtype=np.float64)


def step_head_id(night: Night) -> str:
    out = []
    by_id = {}
    for s in night.sessions:
        by_id.setdefault(s.identity, []).append(s)
    sigma_ref = night.persons["agent"].get("sigma_ref", [0.0] * len(READ_IDX))
    for ident, S in by_id.items():
        p = night.person(ident)
        if p["utterances"] < HID_MIN:
            out.append(f"{ident}: {p['utterances']} < {HID_MIN} utterances, H_id not trained")
            continue
        X, Y, w = [], [], []
        for s in S:
            ws = s.weights()
            for text, t_end in s.his:
                night.tick_check()
                i0, i1 = s.tick(t_end), s.tick(t_end + WIN["head_id"])
                face = calibrated(s.u[i0:i1 + 1, list(READ_IDX)], p["b_read"], p["sigma_id"], sigma_ref).mean(0)
                X.append(face)
                Y.append(_decode(night.L, text)[2])
                w.append(ws[i0])
        if not X:
            continue
        W, b = O.ridge(np.array(X), np.array(Y), np.array(w), HID_RIDGE)
        h = night.L.head_id.setdefault(ident, R.HeadId(len(READ_IDX)))
        h.W, h.b, h.trained = W, b, True
        out.append(f"{ident}: H_id on {len(X)} utterances")
    return "; ".join(out) or "no data"


def step_adapter(night: Night) -> str:
    out = []
    for ident in sorted({s.identity for s in night.sessions}):
        X, Y, w = [], [], []
        for s in [s for s in night.sessions if s.identity == ident]:
            ws = s.weights()
            for ev in s.events:
                if ev.get("kind") != "report" or not ev.get("separated", False):
                    continue                         # credit only from separated, partner-initiated reports (S40)
                i, j = ev.get("utt", -1), ev.get("of", -1)
                if not (0 <= i < len(s.his) and 0 <= j < len(s.his)):
                    continue
                _, tc, r_earlier = _decode(night.L, s.his[j][0])
                _, _, r_report = _decode(night.L, s.his[i][0])
                X.append(tc)
                Y.append(np.clip(r_report - r_earlier, -0.15, 0.15))
                w.append(ws[s.tick(s.his[i][1])])
        if not X:
            out.append(f"{ident}: no separated report")
            continue
        ad = night.L.adapter.setdefault(ident, R.Adapter())
        X, Y, w = np.array(X), np.array(Y), np.array(w)

        def g(ad=ad, X=X, Y=Y, w=w, ident=ident):
            loss, dW, db = O.wls_grad(X, Y, w, ad.W, ad.b)
            return loss, {f"adapter.{ident}.W": dW, f"adapter.{ident}.b": db}
        loss = _descend(night, {f"adapter.{ident}.W": (ad, "W"), f"adapter.{ident}.b": (ad, "b")}, g)
        ad.trained = True
        out.append(f"{ident}: adapter on {len(X)} reports, loss {loss:.4g}")
    return "; ".join(out) or "no data"


def step_word_v(night: Night) -> str:
    X, Y, w = [], [], []
    for s in night.sessions:
        ws = s.weights()
        for text, t_end in s.his:
            e, tc, _ = _decode(night.L, text)
            i0, i1 = s.tick(t_end), s.tick(t_end + WIN["teacher"])
            X.append(np.concatenate([e, tc]))
            Y.append([float(np.max(s.body[i0:i1 + 1, COL["V_F"]]))])
            w.append(ws[i0])
    if not X:
        return "no data"
    part = night.L.word_v
    X, Y, w = np.array(X), np.array(Y), np.array(w)

    def g():
        loss, dW, db = O.wls_grad(X, Y, w, part.W, part.b)
        return loss, {"word_v.W": dW, "word_v.b": db}
    loss = _descend(night, {"word_v.W": (part, "W"), "word_v.b": (part, "b")}, g)
    part.trained = True
    return f"word -> V on {len(X)} utterances, loss {loss:.4g}"


# ---------------------------------------------------------------------------------------------------- step 4
def _refl() -> np.ndarray:
    m = np.zeros((N, C.N_IN))
    for k in range(N):
        for j in range(C.N_IN):
            if C.is_reflected(k, j):
                m[k, j] = 1.0
    return m


def appraisal_batches(night: Night):
    """Per session: (innate+learned bases' innate part, alpha, xi, side, target, w)."""
    P0 = pi0_matrix(True)
    net = night.L.appraisal
    out = []
    for s in night.sessions:
        if s.n <= AHEAD:
            continue
        om = np.asarray(night.person(s.identity)["omega"], dtype=np.float64)
        m = s.n - AHEAD
        b7 = s.body[:m][:, [COL[c] for c in ("E", "A", "V", "K", "P", "I", "Dp_word")]]
        x = np.concatenate([s.xi_A[:m], np.zeros((m, 64)), b7, np.tile(om, (m, 1))], axis=1)
        alpha = np.tanh(x @ net.W1 + net.b1) @ net.W2
        target = (s.drivers[AHEAD:] - s.drivers[:m]) @ P0.T
        out.append((AP.innate_bases(om), alpha, s.xi_A[:m], -np.sign(s.lateral[:m]), target, s.weights()[:m]))
    return out


def step_appraisal(night: Night) -> str:
    batches = appraisal_batches(night)
    if not batches:
        return "no data"
    net = night.L.appraisal
    refl = _refl()
    S = C.pair_sign(np.zeros((N, N)) if night.dyad_prior is None else night.dyad_prior)
    wsum = sum(float(np.sum(b[5])) for b in batches)

    def g():
        loss, dG, dW = 0.0, np.zeros_like(net.learned_bases), np.zeros_like(net.Wsel)
        for innate, alpha, xi, side, target, w in batches:
            bases = np.concatenate([innate, net.learned_bases])
            l, a, b = O.appraisal_loss(bases, net.Wsel, alpha, xi, side, refl, target, w)
            f = float(np.sum(w)) / wsum
            loss, dG, dW = loss + f * l, dG + f * a, dW + f * b
        return loss, {"appraisal.learned_bases": dG, "appraisal.Wsel": dW}
    loss = _descend(night, {"appraisal.learned_bases": (net, "learned_bases"), "appraisal.Wsel": (net, "Wsel")}, g,
                    after=lambda: PJ.project_appraisal(net, night.omegas(), S))
    net.trained = True
    return f"Gamma(3,4) and W by L_A, loss {loss:.4g} (A's own likelihood: not specified, stub kept)"


# ---------------------------------------------------------------------------------------------------- step 5
def _init_delta(night: Night) -> None:
    d = night.L.delta
    if d.trained or np.any(d.W1) or np.any(d.W2) or np.any(d.syn):
        return
    r = np.random.default_rng(int(SGD["seed"]))
    sc = float(SGD["init_scale"])
    d.W1 = sc * r.standard_normal(d.W1.shape)
    d.W2 = sc * r.standard_normal(d.W2.shape)
    d.syn = sc * r.standard_normal(d.syn.shape)
    PJ.project_delta(d)
    for a in ("W1", "W2", "syn"):
        night.theta0[f"delta.{a}"] = np.array(getattr(d, a))


def step_delta(night: Night) -> str:
    S = [s for s in night.sessions if s.n]
    if not S:
        return "no data"
    _init_delta(night)
    d, rd = night.L.delta, night.L.reader_own
    z, rise = _stack(S, "z_T"), _stack(S, "drivers")[:, 1]
    base = _stack(S, "own_face") - O.delta_output(d, z, rise, MASK_ZERO, MASK_RISE_ONLY)
    Y, w = _stack(S, "own_loads"), np.concatenate([s.weights() for s in S])

    def g():
        loss, dW1, dW2, dsyn = O.display_loss(d, z, rise, base, rd.W, rd.b, list(OWN_READ_IDX), Y, w, MASK_ZERO,
                                              MASK_RISE_ONLY)
        return loss, {"delta.W1": dW1, "delta.W2": dW2, "delta.syn": dsyn}
    loss = _descend(night, {"delta.W1": (d, "W1"), "delta.W2": (d, "W2"), "delta.syn": (d, "syn")}, g,
                    after=lambda: PJ.project_delta(d))
    d.trained = True
    return f"Delta by L_display, loss {loss:.4g} (anticipation term: no P_ant head, 0)"


# ---------------------------------------------------------------------------------------------------- step 8, energy
def step_omega(night: Night) -> str:
    out = []
    for s in sorted(night.sessions, key=lambda s: s.t0):
        if not s.n:
            continue
        p = night.person(s.identity)
        amps = sum(float(ev.get("amp", 0.0)) for ev in s.events if ev.get("kind") == "drop_event" and (
            ev.get("term") in CREDIT_TERMS or (ev.get("term") == "Dp_word" and ev.get("credited", False))))
        rho = amps / max(float(s.body[0, COL["D"]]), 1e-6)
        h_bar = float(np.mean(s.body[:, COL["h_word"]]))
        target = omega_target(rho, h_bar)
        p["omega"] = list(omega_update(p["omega"], target))
        out.append(f"{s.sid}: s = {target:+.3f}")
    return "; ".join(out) or "no data"


def step_energy(night: Night) -> str:
    S = sorted([s for s in night.sessions if s.n], key=lambda s: s.t0)
    agent = night.persons["agent"]
    E = float(S[-1].body[-1, COL["E"]]) if S else float(agent.get("E", E_SET))
    agent["E"] = float(np.clip(max(E, E_SET), 0.0, 1.0))
    return f"E {E:.3f} -> {agent['E']:.3f}"


def carried_levels_in_range(persons: dict) -> list:
    """A14's range part for the levels the next session starts from (drives in [0, 1], omega in [-1, 1])."""
    out = []
    E = persons["agent"].get("E", E_SET)
    if not 0.0 <= E <= 1.0:
        out.append(("A14", "carried E outside [0, 1]"))
    for ident, p in persons["persons"].items():
        if np.any(np.abs(p["omega"]) > 1.0):
            out.append(("A6", f"omega of {ident} outside [-1, 1]"))
    assert DRIVES[0] == "E"
    return out


STEPS = (
    ("world_model", None, "the world model is not built"),
    ("pi_tilde", step_pi_tilde, ("reader_own", "reader_his")),
    ("calibration", step_calibration, ()),
    ("head_id", step_head_id, ("head_id",)),
    ("adapter", step_adapter, ("adapter",)),
    ("word_v", step_word_v, ("word_v",)),
    ("appraisal", step_appraisal, ("appraisal",)),
    ("delta", step_delta, ("delta",)),
    ("words_model", None, "the words-only partner model is not built"),
    ("scorer_query", None, "J needs the world model's rollout"),
    ("omega", step_omega, ()),
    ("energy", step_energy, ()),
)
