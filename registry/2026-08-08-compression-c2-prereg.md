# Preregistration: stronger observers on the residual (WP-C2)

Committed before first run. Instrument: `code/compression_observers.py`. Lane:
WP-C. Follow-up to C1 committed there: stronger observer classes on the
wheel-restricted residual, and the parity stream at greater height.

## Design note (fixed before the run, and part of the claim)

The wheel-30-restricted residual is NOT structureless in principle: it carries
(i) divisibility structure for primes outside the wheel (a position divisible
by 7 is never prime — ~0.038 nats of predictable content from p = 7 alone),
and (ii) short-range Hardy–Littlewood pair correlations (singular-series
enhancements at small gaps), both of which are **skeleton-derivable** in the
sense of WP6's ladder. C1's zlib observer missed essentially all of it (K4
ratio 0.9947) — general compressors are a weak observer. The two-skeleton
question at the trained-observer class is therefore: once the observer is
GIVEN the local congruence data, does sequence history add anything? The
baseline is deliberately enriched so that skeleton-derivable structure
(including HL short-range correlations, which are congruence-driven) is
representable by the baseline: any challenger gain ≥ eps would be evidence of
structure beyond the local congruence skeleton and would go up the audit
ladder, not into a headline.

## Instrument constants (frozen)

- Residual: wheel-30 coprime positions in [10^7 − 2^20, 10^7) (as C1;
  ~280k bits). Chronological split: first half train, second half holdout.
- Models (WP9c hyperparameters): logistic regression, IRLS 20 iterations,
  ridge 1e-3; gradient-boosted stumps, logistic loss, T = 60 rounds,
  learning rate 0.1, 8 quantile thresholds per feature per round.
- BASELINE (skeleton observer): divisibility flags `p | n` for
  p ∈ {7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47} at the current and
  three preceding restricted positions (48 columns) + scaled position
  (1 column).
- CHALLENGER: baseline + previous 24 residual bits + rolling densities over
  the last 64 and 256 restricted positions (26 columns).
- Metric: holdout mean log-loss (nats); eps = 0.002 (WP9c convention).
- Parity at height: sieve to 10^8 (segment counting via reduceat; no full
  cumsum); 8192 parity bits of π at geometric points 10^6..10^8; zlib-9 vs
  the π-digit coin control of C1.
- Entropy ladder (report only, not gated): order-k conditional entropy of
  residual vs a density-matched SHA-256 ("WP-C2" seed) control, k = 0..12.

## Gates (frozen)

- **M1 (positive control).** The baseline beats the constant-rate model by
  > 0.02 nats on holdout: the skeleton observer must see the known
  divisibility structure that zlib missed.
- **M2 (two-skeleton at the trained-observer class).** Challenger − baseline
  holdout improvement < eps = 0.002 nats for BOTH model classes.
- **M3 (parity at height).** zlib ratio ≥ 0.97 vs the coin control for the
  10^6..10^8 parity stream.

## Committed predictions (non-gating)

- **N1.** Baseline gain over constant rate lands in [0.10, 0.25] nats (the
  computable divisibility content: Σ (1/p)·(−ln(1−ρ30)) over the feature
  primes ≈ 0.166 nats, plus conditional-density adjustments).
- **N2.** Challenger improvement ≤ 0.001 nats on both models.
- **N3.** Parity ratio ∈ [0.99, 1.03].
- **N4.** Entropy ladder: max over k ≤ 12 of (H_k(control) − H_k(residual))
  reported; expected ≤ 0.01 bits (the mod-p structures are long-period phase
  information largely invisible to short contexts).

## Exclusions and notes

- A failed M2 is not dissolved: the gain is diagnosed up the audit ladder
  (leakage → HL/skeleton-derivable → known theorem → candidate), per WP9c.
- Thresholds frozen; results append-only; bring-up fixes with honest notes.
- Librarian: divisibility content of the residual is elementary; HL
  correlations are Hardy–Littlewood; the observer-ladder framing is WP6's.
  The measured tables (what each observer class captures, quantified) are
  the deliverable.
