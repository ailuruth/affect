# CI-style targets (spec §7.6). Synthetic arrays only.
PY ?= python3

.PHONY: ci test lint lock regress-full

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
