# Preregistration registry

Scans and detector runs in this programme are preregistered. The protocol:

1. **Commit before measurement.** A preregistration file (battery, null model,
   thresholds, exclusions, and committed predictions) is added to this directory and
   committed to git *before* the corresponding code is run. The git commit hash and
   timestamp are the commitment device; the prereg file is never edited afterwards.
2. **Results are append-only.** Each run adds a separate results file referencing the
   prereg commit. Discrepancies between prediction and measurement are reported as
   discrepancies — surfaced, not dissolved into hindsight.
3. **Audit ladder.** Every survivor is classified up the ladder before the word
   "candidate" is used: instrument artifact → mechanical feature entanglement →
   skeleton-derivable → known theorem → candidate.

Index:

| Prereg | Run | Results |
|---|---|---|
| `2026-08-03-scanner-v2-prereg.md` | `code/scanner_v2.py` | `2026-08-03-scanner-v2-results.md` |
| `2026-08-03-ml-detector-prereg.md` | `code/ml_detector.py` | `2026-08-03-ml-detector-results.md` |
| `2026-08-07-weil-positivity-prereg.md` | `code/weil_positivity.py` | `2026-08-07-weil-positivity-results.md` |
| `2026-08-07-canonical-system-prereg.md` | `code/canonical_system.py` | `2026-08-07-canonical-system-results.md` |
| `2026-08-07-requirements-spec-prereg.md` | `code/requirements_spec.py` | `2026-08-07-requirements-spec-results.md` |
| `2026-08-07-two-interval-plateau-prereg.md` | `code/two_interval_plateau.py` | `2026-08-07-two-interval-plateau-results.md` |
| `2026-08-07-plateau-bias-prereg.md` | `code/plateau_bias.py` | `2026-08-07-plateau-bias-results.md` |
