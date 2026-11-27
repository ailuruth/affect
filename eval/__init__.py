"""The evaluation battery (spec §5, milestone M9). Never imported by engine/ (tests/test_imports.py).

Every test here is judged on the engine's internal state (its T, F and K fields, its route terms, the ledger's
frames and the rendered partner-caused part), never on how closely the agent's face matches a human face (spec §5,
brief, Q19). No module here uses an affect label (label lint, spec §7.4), calls Claude or opens a network
connection.

In this cloud session the battery runs only on small synthetic stand-ins (`eval/synthetic.py`) to test the harness
itself; those runs are marked `synthetic` and are never evidence (results.py refuses to write them into
research/build/results/). The evidence runs happen on the operator's Mac at the stages eval/flist.py lists.

  registry.py   predictions written with a timestamp and hash before the run; scoring refuses late or changed ones
  results.py    JSON / CSV result files (no arrays); synthetic results kept out of research/build/results/
  drive.py      one engine session (engine.shadow.ShadowPair) with lesion, steering and mirror hooks; readouts
  switches.py   the documented lesion switches (spec §5.2) and their shams
  lesions.py    E1: lesion harness          steering.py   E2: steering and input clamps
  surrogates.py E3: pooled slopes against segment-shuffle, data-sliding, partner-swap, timing-resample, month-swap
  mirror.py     the mirror-only partner against no partner (the G-mirror test, spec §5.4)
  f22_delayed_copy.py  F22: ledger-only injected delayed copies, with the §5.5 pilot and plan
  flist.py      every falsifier of spec §5.1 -> its test, data source, machine and stage
  planner.py    the run planner (machine.md: ask before any sitting over about 6 h; plan each sitting <= 5 h)
  metrics.py    block-mean slopes, frames changed, monotone drift
  dry_run.py    `make eval-dry`: every harness end to end on synthetic stand-ins
"""
