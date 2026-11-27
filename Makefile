# CI-style targets (spec §7.6). Synthetic arrays only.
PY ?= python3

.PHONY: ci test lint lock regress-full week0 eval-dry

ci:            ## data guard, label lint, pytest (fast suite)
	$(PY) tools/ci.py

test:
	$(PY) -m pytest -q -p no:cacheprovider

lint:
	$(PY) tools/lint_labels.py

lock:          ## regenerate engine/config/INNATE.lock from engine/config/innate.py (a reviewed change)
	$(PY) -m engine.config.innate --write

regress-full:  ## full 2-h ledger regressions against the sims reference (several minutes)
	$(PY) tools/ci.py --slow

week0:         ## M1 on the operator's Mac: every week-0 check in order, then the summary in research/build/week0.md
	$(PY) -m tools.week0.run_all

eval-dry:      ## M9 harness self-test: every eval/ harness end to end on synthetic stand-ins (a few minutes; not evidence)
	$(PY) -m eval.dry_run
