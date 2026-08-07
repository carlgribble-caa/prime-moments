# Results: the compression question, first light (WP-C1)

Prereg: `2026-08-08-compression-prereg.md`, committed at `f6f2e66` before
first run. Instrument: `code/compression_question.py` (3 s). Results are
append-only. All five gates passed on the first run; all three predictions
confirmed — the lane's cleanest first light.

## Gates and predictions

| Item | Committed | Measured | Verdict |
|---|---|---|---|
| K1 (spec completeness) | one OPEN cell | exact π(x) in poly(log x) | PASS |
| K2 (parity stream) | ratio ≥ 0.97 vs coin control | **1.0000** (1035 B = 1035 B) | PASS |
| K3 (skeleton found) | ≤ 0.92·H2(ρ) | 0.2971 ≤ 0.3089 bits/pos | PASS |
| K4 (nothing beyond) | ratio ≥ 0.97 vs matched control | **0.9947** | PASS |
| K5 (local polylog) | MR = sieve on 200 integers | exact | PASS |
| L1 | K2 ratio ∈ [0.99, 1.03] | 1.0000 | CONFIRMED |
| L2 | K4 ratio ∈ [0.99, 1.03] | 0.9947 | CONFIRMED |
| L3 | best/wheel-entropy ∈ [1.0, 1.6] | 1.423 | CONFIRMED |

## The findings

1. **The parity stream of π(x) is coin-like at the practical-compressor
   level** — compressed to the byte the same as a Bernoulli(1/2) control
   (8192 bits, geometric sample points with ~20+ primes between consecutive
   points). The cheapest falsifiable shadow of the closed-form question
   found nothing.
2. **The prime indicator's compressible content is its congruence skeleton,
   and general-purpose compressors capture part of it and nothing else**:
   best of zlib/bz2/lzma reaches 0.297 bits/position on the raw window
   (below the structure-blind bound 0.336, above the wheel entropy 0.209 —
   compressors get 42% of the way into the skeleton's gap), while the
   wheel-restricted residual compresses to 99.5% of a density-matched
   control. This is the **two-skeleton conjecture (WP6) confirmed at the
   compressor observer class** — a new observer stratum for the observer
   ladder, measured under prereg.
3. **The local/global contrast is the OPEN cell's sharpest edge**: primality
   of an individual n is poly(log n) (ADOPTED: AKS; demonstrated by K5),
   while exact counting is stuck at x^{1/2+ε}/x^{2/3} (Lagarias–Odlyzko;
   Deléglise–Rivat) — the open cell is *global aggregation*, not local
   detection.

## The spec matrix

Printed in full by the instrument: nine rows, every cell ADOPTED, MACHINE
(including the programme's own Lean-checked bit-floor and Paper 1's lattice
observables), or MEASURED — except **one OPEN cell: exact π(x) in
poly(log x), equivalently a fixed-length closed form, containing the parity
of π(x) as its weakest unsolved form.**

## Honest scope

Compressors are proxies for entropy, not Kolmogorov estimators; all
"incompressible" claims are at the practical-compressor observer class, and
the obstruction profile assembled here is not an impossibility proof. The
lane's connection to WP-RH is recorded: the fluctuations these instruments
measure as structureless are exactly the object whose spectral content the
positivity lane measured as the (full-amplitude, DW-attenuated) prime comb —
compressible in the spectral basis at √x length, structureless to
general-purpose observers, closed-form only if the zeros are.

## Carried forward

- WP6 gains a measured base-camp row: two-skeleton holds at the compressor
  class (this run's K4).
- Candidate next steps (unclaimed): stronger observer classes on the
  restricted residual (context-mixing compressors; the ML detector of WP9c
  re-aimed at compression); the parity stream at higher heights; a
  formalization note tying the spec matrix to the complexity-theory
  literature properly (librarian pass required before any of it prints).
