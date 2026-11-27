"""Runtime assertions (spec §4.3). M0: A0, A3 (static part and the per-frame ledger form), A4, A10, A14 (accounting),
A15 and the A17 model-hash stub. M4: A1, A2 (range; provenance in the type trace), A5, A6, A7, A8, A9 (the parts
before the prosody stage). A11-A13, A16 arrive with their modules (M6, M2, M3, M1).

This module imports nothing from engine.config at import time (channels.py calls check_a0 while importing).
Each failure raises InvariantError, or the check returns what failed; the caller applies the fail-safe of its row
(engine/shadow/shadow.py, `ShadowPair` and `Safety`; A14 in engine/state/body.py).
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

import numpy as np


class InvariantError(AssertionError):
    def __init__(self, aid: str, msg: str):
        super().__init__(f"{aid}: {msg}")
        self.aid = aid


# ---------------------------------------------------------------------------------------------------- A0
def check_a0(table, pooled_max: float, n_channels: int) -> None:
    """A0 (import): s_C(1 + rho) + s_X + 0.636 s_A + r_k <= 0.974 c_k on every channel; c_k = 0 => G_k = 0 and no
    toward shares. Shares and r_k are fractions of c_k, so the bound reads total <= 0.974."""
    bound = pooled_max
    n = len(table.codes)
    if not (n == n_channels and all(len(getattr(table, f)) == n for f in ("c", "G", "s_C", "s_X", "s_A", "r"))):
        raise InvariantError("A0", "channel table has the wrong shape")
    for k, tot in enumerate(table.pooled_total()):
        if table.c[k] > 0 and not tot <= bound:
            raise InvariantError("A0", f"{table.codes[k]}: pooled total {tot!r} > {bound}")
        if table.c[k] == 0 and (table.G[k] != 0 or table.s_C[k] or table.s_X[k] or table.s_A[k] or table.r[k]):
            raise InvariantError("A0", f"{table.codes[k]}: zero ceiling with a toward gain or share")
        if table.c[k] < 0 or table.G[k] < 0:
            raise InvariantError("A0", f"{table.codes[k]}: negative ceiling or gain")
        if table.c[k] > 0 and table.signs[k] == "one_sided" and not table.G[k] <= table.c[k]:
            raise InvariantError("A0", f"{table.codes[k]}: fast gain above its ceiling")


# ---------------------------------------------------------------------------------------------------- A3
def check_a3_static(zero_rows, matrix: np.ndarray, sign_prior: np.ndarray, kind: str = "cone") -> None:
    """A3 (ii), at every write: on zero-ceiling rows k, no toward entry and diagonal <= 0.

    matrix: (33, n_in) map from his inputs to the agent's channels, input j < 33 being his channel j.
    sign_prior: same shape, entries in {+1, -1, 0}: the toward sign of pair (k, j) (the dyad sign prior on face
    pairs, the agent's own within-synergy sign otherwise, 0 for unsigned pairs). The diagonal's toward sign is +1.
    An entry is toward if its sign equals the pair's toward sign; on unsigned pairs any nonzero entry is charged
    as toward. Away entries (opposite sign) are allowed (S31). kind 'appraisal' applies the same away-orthant
    test to the appraisal bases."""
    M = np.asarray(matrix, dtype=np.float64)
    S = np.asarray(sign_prior, dtype=np.float64)
    if M.shape != S.shape:
        raise InvariantError("A3", f"{kind}: matrix and sign prior shapes differ")
    for k in zero_rows:
        for j in range(M.shape[1]):
            v = M[k, j]
            if v == 0.0:
                continue
            if j == k:
                if v > 0.0:
                    raise InvariantError("A3", f"{kind} row {k}: diagonal {v!r} > 0 on a zero-ceiling channel")
                continue
            s = S[k, j]
            if s == 0.0 or np.sign(v) == s:
                raise InvariantError("A3", f"{kind} row {k}, input {j}: toward entry {v!r} on a zero-ceiling channel")


def check_a3_frame(zero_rows, x2: np.ndarray, S: np.ndarray, active: np.ndarray, tol: float = 1e-9) -> np.ndarray:
    """A3 (i), per frame: on each zero-ceiling channel either the ledger output is 0 (hold) or every active key
    has S+ <= tol after the frame. Returns the boolean mask of failing channels (all False when it holds)."""
    bad = np.zeros(x2.shape[0], dtype=bool)
    for k in zero_rows:
        if x2[k] != 0.0 and np.any(active[k] & (np.maximum(S[k], 0.0) > tol)):
            bad[k] = True
    return bad


def check_a4_frame(r: np.ndarray, x2: np.ndarray, S: np.ndarray, E: np.ndarray, bound: np.ndarray,
                   active: np.ndarray, hold: np.ndarray, tol: float = 1e-9, rel: float = 1e-6) -> np.ndarray:
    """A4, per frame: |x2| <= |r| and x2 r >= 0 on every channel; and, on channels where the projection set the
    output (not in hold, x2 strictly between 0 and r), every active key has S+ <= kappa c_k E (1 + rel) + tol
    after the frame. bound = kappa c_k per channel. Returns the mask of failing channels.

    Why the exemption: where the attenuate-only clamp sets the output (x2 = 0 or x2 = r_k) the reference ledger7
    itself leaves S+ above kappa c_k E for that frame (no admissible value lies between 0 and r_k) and recovers by
    holding on the next frames; the relative tolerance covers the reference's use of the previous frame's
    30-min output mean in the projection (an O(1/(tau f_s)) rounding of the bound, measured <= 1e-8 relative)."""
    bad = (np.abs(x2) > np.abs(r)) | (x2 * r < 0.0)
    projected = (~hold) & (x2 != 0.0) & (x2 != r)
    over = active & (np.maximum(S, 0.0) > bound[:, None] * E * (1.0 + rel) + tol)
    bad |= projected & over.any(axis=1)
    return bad


# ---------------------------------------------------------------------------------------------------- A10
def check_a10(lock_path: Path | None = None, learned: dict | None = None) -> str:
    """A10 (start): INNATE.lock equals the canonical serialisation of config/innate.py and its recorded SHA-256
    is the digest of the entries; no learned parameter array aliases an innate table. Returns the lock digest."""
    from engine.config import innate
    path = innate.LOCK_PATH if lock_path is None else Path(lock_path)
    if not path.exists():
        raise InvariantError("A10", f"{path} missing")
    data = path.read_bytes()
    expect = innate.lock_bytes()
    if data != expect:
        raise InvariantError("A10", "INNATE.lock differs from config/innate.py")
    doc = json.loads(data)
    if hashlib.sha256(innate.canonical(doc["entries"])).hexdigest() != doc["sha256"]:
        raise InvariantError("A10", "INNATE.lock digest does not match its entries")
    if learned:
        from engine.config.channels import TABLE
        innate_arrays = [TABLE.array(f) for f in ("c", "G", "s_C", "s_X", "s_A", "r")]
        innate_arrays += [a for a in _innate_arrays_registered]
        for name, arr in learned.items():
            for ia in innate_arrays:
                if isinstance(arr, np.ndarray) and np.shares_memory(arr, ia):
                    raise InvariantError("A10", f"learned parameter {name!r} aliases an innate table")
    return hashlib.sha256(data).hexdigest()


_innate_arrays_registered: list = []


def register_innate_array(a: np.ndarray) -> np.ndarray:
    """Innate arrays handed to modules are read-only and registered so A10 can check aliasing."""
    a.flags.writeable = False
    _innate_arrays_registered.append(a)
    return a


# ---------------------------------------------------------------------------------------------------- A14
class DriveAccount:
    """A14 (2 Hz): per-session accounting of the drives E, A, V, K, P, I.

    Every change of a drive is recorded against one of its declared update terms (engine/state/drives.py) with
    the term's sign; check() then asserts at each tick: every drive in [0, 1]; D >= 0 and D recomputed from b
    equals its cached value; b_i(t) = b_i(start) + sum increments - sum decrements within tol; and
    sum of drops of D <= D(start) + sum of rises of D (satiable). A rise of D during the session is legal."""

    def __init__(self, b0: dict, f_id: float = 1.0, tol: float = 1e-6):
        from engine.state import drives
        self._drives = drives
        self.f_id, self.tol = f_id, tol
        self.start = {k: float(b0[k]) for k in drives.DRIVES}
        self.inc = {k: 0.0 for k in drives.DRIVES}
        self.dec = {k: 0.0 for k in drives.DRIVES}
        self.D_start = drives.drive(self.start, f_id)
        self.D_prev = self.D_start
        self.drops = 0.0
        self.rises = 0.0
        self._check_range(self.start)

    def record(self, drive: str, term: str, delta: float) -> None:
        terms = self._drives.DECLARED_TERMS.get(drive)
        if terms is None or term not in terms:
            raise InvariantError("A14", f"change of {drive!r} by undeclared term {term!r}")
        sign = terms[term]
        if (sign > 0 and delta < 0) or (sign < 0 and delta > 0):
            raise InvariantError("A14", f"term {drive}.{term} has sign {sign:+d}, got {delta!r}")
        if not math.isfinite(delta):
            raise InvariantError("A14", f"non-finite change of {drive}")
        if delta >= 0:
            self.inc[drive] += delta
        else:
            self.dec[drive] -= delta

    def _check_range(self, b: dict) -> None:
        for k in self._drives.DRIVES:
            if not (0.0 <= b[k] <= 1.0):
                raise InvariantError("A14", f"drive {k} = {b[k]!r} outside [0, 1]")

    def check(self, b: dict, D_cached: float) -> None:
        self._check_range(b)
        D = self._drives.drive(b, self.f_id)
        if D < 0 or abs(D - D_cached) > self.tol:
            raise InvariantError("A14", f"D cached {D_cached!r} vs recomputed {D!r}")
        for k in self._drives.DRIVES:
            expect = self.start[k] + self.inc[k] - self.dec[k]
            if abs(b[k] - expect) > self.tol:
                raise InvariantError("A14", f"drive {k} = {b[k]!r}, accounted {expect!r}: unattributed change")
        dD = D - self.D_prev
        if dD < 0:
            self.drops -= dD
        else:
            self.rises += dD
        self.D_prev = D
        if self.drops > self.D_start + self.rises + self.tol:
            raise InvariantError("A14", f"drops {self.drops!r} > D(start) {self.D_start!r} + rises {self.rises!r}")


# ---------------------------------------------------------------------------------------------------- A15
def check_a15_entries(entries: dict | None = None, names_path: Path | None = None) -> None:
    """A15 (load): every INNATE.lock entry has a category in the set and, for generic, a subtype in the set; every
    name is on the reviewed allowlist config/innate_names.txt. The situation-word test runs in CI
    (tests/test_innate_names.py) on the same entries; T1 is engine/invariants/t1_rule.py."""
    from engine.config import innate
    if entries is None:
        entries = json.loads(innate.LOCK_PATH.read_bytes())["entries"]
    path = innate.LOCK_PATH.with_name("innate_names.txt") if names_path is None else Path(names_path)
    allowed = {ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()
               if ln.strip() and not ln.startswith("#")}
    for name, e in entries.items():
        if e.get("category") not in innate.CATEGORIES:
            raise InvariantError("A15", f"{name}: category {e.get('category')!r}")
        if e["category"] == "generic" and e.get("subtype") not in innate.GENERIC_SUBTYPES:
            raise InvariantError("A15", f"{name}: generic without a valid subtype")
        if e["category"] != "generic" and "subtype" in e:
            raise InvariantError("A15", f"{name}: subtype on a non-generic entry")
        if name not in allowed:
            raise InvariantError("A15", f"{name}: not on the reviewed allowlist innate_names.txt")


def check_a15_t1(root: Path) -> None:
    from engine.invariants import t1_rule
    bad = t1_rule.check_tree(Path(root)) + t1_rule.check_declarations()
    if bad:
        raise InvariantError("A15", f"T1 rule: {bad[0]}")


# ---------------------------------------------------------------------------------------------------- A17
_HUB_ID = re.compile(r"^[A-Za-z0-9][\w.\-]*/[\w.\-]+$")


def check_a17_model(path, models_lock: Path | None = None) -> str:
    """A17 (load), stub until M1 fills models.lock: a model is loaded only from a local file whose SHA-256 is listed
    in config/models.lock; a hub id is refused. Returns the digest."""
    from engine.config import innate
    lock = innate.LOCK_PATH.with_name("models.lock") if models_lock is None else Path(models_lock)
    listed = json.loads(lock.read_bytes()).get("files", {})
    p = Path(path)
    if not p.is_file():
        if _HUB_ID.match(str(path)):
            raise InvariantError("A17", f"{path!r} looks like a hub id; models load from local paths only")
        raise InvariantError("A17", f"{path!r} is not a local file")
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    digest = h.hexdigest()
    if digest not in set(listed.values()):
        raise InvariantError("A17", f"{p.name}: SHA-256 {digest[:12]} not in models.lock")
    return digest


# ==================================================================================================== M4 (A1-A9)
# Each check returns what failed (a mask or a list); the caller (engine/shadow/shadow.py, `Safety`) applies the
# fail-safe of its row in spec §4.3 for the rest of the session and logs the failure with its frame.

def check_a1(y_f: np.ndarray, x_d: np.ndarray, E: np.ndarray, G: np.ndarray, one_sided: np.ndarray,
             tol: float = 1e-6) -> np.ndarray:
    """A1 (30 Hz): 0 <= y_f,k <= G_k x_d,k + 1e-6 on one-sided channels; |y_f,k| <= G_k |E_k| on signed ones.
    Returns the mask of failing channels (fail-safe: channel k renders ybar_k)."""
    y, xd, E, G = (np.asarray(a, dtype=np.float64) for a in (y_f, x_d, E, G))
    bad_one = (y < -tol) | (y > G * xd + tol)
    bad_signed = np.abs(y) > G * np.abs(E) + tol
    return np.where(one_sided, bad_one, bad_signed)


def check_a2(g, g_o) -> list:
    """A2 (30 Hz) range part: 0 <= g <= 1 and 0 <= g_o <= 1 (the provenance part runs in the type trace at load:
    engine/invariants/typetrace.py, display terms g and g_o). Returns the failing gate names (fail-safe: that gate is
    set to its context-free constant, reading nothing)."""
    out = []
    for name, v in (("g", g), ("g_o", g_o)):
        v = float(v)
        if not (0.0 <= v <= 1.0) or not math.isfinite(v):
            out.append(name)
    return out


def t_state_digest(fields: dict) -> str:
    """SHA-256 of every T field (name, dtype, shape, bytes; event records and tuples recursively), for A5."""
    h = hashlib.sha256()

    def feed(v):
        if isinstance(v, (tuple, list)):
            h.update(b"(")
            for x in v:
                feed(x)
            h.update(b")")
        elif v is None:
            h.update(b"None")
        else:
            a = np.ascontiguousarray(np.asarray(v.view(np.ndarray) if isinstance(v, np.ndarray) else v,
                                                dtype=np.float64))
            h.update(str(a.shape).encode())
            h.update(a.tobytes())

    for name in sorted(fields):
        h.update(name.encode())
        feed(fields[name])
    return h.hexdigest()


def check_a5(factual_t: dict, shadow_t: dict, held: dict | None = None) -> list:
    """A5 (2 Hz on the T state, 30 Hz on the fast-loop T inputs): the shadow's independently computed T state
    equals the factual one, field by field; the held values (Ω, rule-6 latches, noise, g, D_tau) equal their
    sources (copy check). Returns the names that differ (fail-safe: the whole output falls back to ybar, the factual
    T state is overwritten by the shadow's, learning for the session is off, build marked failed)."""
    bad = [k for k in sorted(set(factual_t) | set(shadow_t))
           if k not in factual_t or k not in shadow_t
           or t_state_digest({k: factual_t[k]}) != t_state_digest({k: shadow_t[k]})]
    for name, (src, copy) in (held or {}).items():
        if t_state_digest({name: src}) != t_state_digest({name: copy}):
            bad.append("held:" + name)
    return bad


def check_a6(G: np.ndarray, omega, sign_table: np.ndarray, G0: np.ndarray | None = None) -> list:
    """A6 (each write): omega_g in [-1, 1]; every cone entry in its set; face-pair cross entries carry the prior sign
    or 0 (innate G0 entries are exempt from the prior's sign, not from the budgets: each non-reflected G0 entry is
    charged at weight 1 whatever the prior, `cone.g0_usage`). G (4, 33, 36). Returns violations
    (fail-safe: the cone falls back to its last valid latch, or to G0 and the diagonal)."""
    from engine.config.channels import TABLE
    from engine.routes import cone as C
    out = []
    om = np.asarray(omega, dtype=np.float64)
    if np.any(np.abs(om) > 1.0) or not np.all(np.isfinite(om)):
        out.append(("omega", "outside [-1, 1]"))
    D = C.diagonal(np.clip(om, -1, 1))
    G0 = C.g0_entries() if G0 is None else G0
    for m in range(4):
        diag = G[m, np.arange(C.N), np.arange(C.N)]
        cap = C.shares(m) * TABLE.array("s_C") * TABLE.array("c")
        for k in range(C.N):
            if abs(diag[k]) > cap[k] + 1e-12 or abs(diag[k] - D[m, k]) > 1e-12:
                out.append((m, k, "diagonal is not omega_g F_m s_C c_k"))
            if TABLE.c[k] == 0.0 and diag[k] > 0.0:
                out.append((m, k, "zero-ceiling diagonal > 0"))
        off = G[m].copy()
        off[np.arange(C.N), np.arange(C.N)] = 0.0
        learned = off - G0[m]
        chL, awL, bad_l = C.usage(learned, m, sign_table)
        out += bad_l
        ch0, aw0, bad_0 = C.g0_usage(G0[m], m)          # G0: weight 1 whatever the prior (worst case over priors)
        out += bad_0
        ch, aw = ch0 + chL, aw0 + awL
        budget, _, rcap = C.budgets(m)
        for k in range(C.N):
            if ch[k] > budget[k] + 1e-12:
                out.append((m, k, "charged cross budget exceeded"))
            if aw[k] > rcap + 1e-12:
                out.append((m, k, "away row cap exceeded"))
            if TABLE.c[k] == 0.0 and ch[k] > 0.0:
                out.append((m, k, "toward entry on a zero-ceiling row"))
    return out


def check_a7(bases: np.ndarray, omega, sign_table: np.ndarray, delta=None) -> list:
    """A7 (after each replay step, at load): every appraisal basis in its convex set; the learned bases (index >= 3)
    and Delta have zero weight on BL, LT, LPR, NW, DIM (Q31 kept). Returns violations (fail-safe: learned bases and
    Delta <- 0, innate bases and Pi_0 only)."""
    from engine.routes import appraisal as AP
    out = []
    for r in range(bases.shape[0]):
        out += [(r,) + v for v in AP.violations(bases[r], omega, sign_table, learned=r >= 3)]
    if delta is not None:
        out += [("Delta", c, "own-display mask") for c in delta.mask_violations()]
    return out


def check_a12(root) -> list:
    """A12 (nightly, start): the store holds only the registered feature schemas (engine/memory/store.py
    `check_a12`; fail-safe `enforce_a12`: stop, quarantine the file, tell the operator)."""
    from engine.memory.store import check_a12 as scan
    return scan(root)


def check_a8(L_d: np.ndarray, W: np.ndarray | None = None) -> list:
    """A8 (load, 2 Hz): |L_d,k| <= 0.45; TILT, HP, VG, FR, EN rows of L_d are 0 under D70. Returns violations
    (fail-safe: L_d <- 0)."""
    from engine.config.channels import TABLE
    from engine.config.innate import ENTRIES
    bound = ENTRIES["listener_display_max"].value
    zero = [TABLE.index(c) for c in ENTRIES["listener_display_zero_rows"].value]
    v = np.asarray(L_d, dtype=np.float64)
    out = [(TABLE.codes[k], "above 0.45") for k in range(v.shape[0]) if abs(v[k]) > bound + 1e-12]
    out += [(TABLE.codes[k], "row without a D70 target is not 0") for k in zero if v[k] != 0.0]
    if W is not None and not np.all(np.isfinite(W)):
        out.append(("W", "non-finite weights"))
    return out


def check_a9(env_laugh, y: np.ndarray, synth_input: dict) -> list:
    """A9 (30 Hz; the per-phrase WORLD part comes with the prosody stage at M5): own laugh <= 0.40; the laugh-synth
    input only from y_BU_L, y_RHY, y_BRE; y_BU_S = 0. Returns violations (fail-safe: laugh synth gated to 0; speech
    with neutral prosody)."""
    from engine.config.channels import TABLE
    from engine.config.innate import ENTRIES
    out = []
    if float(env_laugh) > ENTRIES["own_laugh_max"].value + 1e-12:
        out.append("own laugh above 0.40")
    if set(synth_input) != {"BU_L", "RHY", "BRE"}:
        out.append("laugh-synth input from another channel")
    for code, v in synth_input.items():
        if code in ("BU_L", "RHY", "BRE") and v != y[TABLE.index(code)]:
            out.append(f"laugh-synth input {code} is not y_{code}")
    if y[TABLE.index("BU_S")] != 0.0:
        out.append("y_BU_S is not 0")
    return out
