# The Prime Moments Series

Exact prime counts, prime sums, and prime recovery from moment data — four papers whose numerical
claims are machine-verified, together with the code that reproduces every table.

## Papers (canonical sources in `papers/`)

| # | Paper | Verification script |
|---|---|---|
| 1 | *Prime counts and prime sums from multiplication tables: a self-similar formula system* | `code/prime_sum_formula.py` |
| 2 | *Certified exact sums of primes over dyadic intervals via a ladder of generalized factorials* | `code/certified_snap.py` |
| 3 | *Recovering the primes in a dyadic interval from exact moments: two constructive routes and an obstruction theorem* | `code/prime_recovery.py` |
| 4 | *The multiplication crystal: dimension, diffraction, and the symmetries of arithmetic* (expository) | `code/crystal_demos.py`, `code/untargeted_scan.py` |

Author: Carl Gribble. Developed in collaboration with Claude (Anthropic); each paper carries a full
AI-use disclosure section. Provenance of the canonical sources: `papers/PROVENANCE.md`.

## Reproduction

Requires Python 3.10+ with `numpy` and `mpmath`.

```
python run_all.py          # run every verification suite in paper order
python run_all.py --list   # list the scripts without running them
```

Each script is standalone and prints PASS/FAIL lines or tables matching the corresponding paper.
Individual scripts run from seconds to a few minutes at their default scales; Paper 1's full
40-test suite (to 10^7) is the longest.

## Roadmap

The formalization programme — work packages, dependencies, milestones, status ledger — lives in
[PROGRAMME.md](PROGRAMME.md).
