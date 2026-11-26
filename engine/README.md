# engine (milestone M0)

The engine of research/build/spec.md (build core: research/foundations/design-cayley-ledger.md, revision 9.2).
M0 is the skeleton: configuration, invariants and the shadow ledger. Nothing here touches a camera, a microphone,
a model, Claude or the network.

## What M0 contains

- `config/channels.py`: the 33 counterpart channels (spec §1.1) as a frozen table; A0 runs at import.
- `config/innate.py`: every innate and generic constant in one table (name, value, unit, source, category,
  generic subtype, why). `config/INNATE.lock` is its canonical JSON (sorted keys, float repr, no whitespace) with
  the SHA-256 of the entries; regenerate with `make lock` (a reviewed change). `config/innate_names.txt` is the
  reviewed name allowlist. `config/models.lock` is empty until M1. `config/operator.py` holds the operator
  switches of §7.3; an unanswered one refuses to be used.
- `invariants/asserts.py`: A0; A3 (static part, plus the per-frame form); A4 per frame; A10; A14 (per-drive
  accounting); A15 (categories, subtypes, allowlist; T1); A17 (model-hash stub).
- `invariants/t1_rule.py`: T1 as an AST rule over `engine/state/` and `engine/routes/`.
- `invariants/tagged.py`: the `Tagged` provenance wrapper (§4.4).
- `state/types.py` (type declarations of the state fields), `state/drives.py` (the drive forms and the declared
  update terms A14 accounts for).
- `shadow/ledger.py`: the attenuate-only ledger, 97 keys per channel, kappa 0.70, vectorised over (33, 97). At
  10 Hz it is bit-identical to `ledger7` / `ledger9` / `w10` in research/foundations/sims.
- The other subpackages are empty placeholders, filled at their milestone (spec §6).

Outside `engine/`: `tests/` (unit tests, the ledger regression, the lint and its stem table
`tests/lint_stems.py`), `tools/lint_labels.py` (label lint), `tools/ci.py` (CI runner), `Makefile`,
`pyproject.toml` (core deps numpy, scipy, pytest; `engine` and `mac` extras; no `uv.lock` yet).

## How to run

```
make ci              # data guard, label lint, pytest (about 1 min)
make regress-full    # also the full 2-h reference regressions (several minutes)
python -m pytest -q  # tests only
```

All tests use small synthetic arrays; their results say nothing about behaviour.

## What comes at M1, on the Mac

`uv lock` (after the Xcode command line tools, for pyworld) and the pinned environment; `tools/week0/`, the
measurements of the M1 table and the branch each threshold selects, written to research/build/week0.md; the
deny-network sandbox profile and A16; `models.lock` filled once the operator approves the model downloads; the
Plan A `fast` process timed under full load.
