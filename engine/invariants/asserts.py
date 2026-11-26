"""Runtime assertions (spec §4.3). M0 holds A0, A3 (static part, plus the per-frame ledger form used by the
ledger tests), A10, A14 (accounting), A15 and the A17 model-hash stub. The rest arrive with their modules.

This module imports nothing from engine.config at import time (channels.py calls check_a0 while importing).
Each failure raises InvariantError naming the assertion; the caller applies the fail-safe of its row.
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
