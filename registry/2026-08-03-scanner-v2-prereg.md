# Preregistration: skeleton-null scanner v2 (WP6)

Committed before first run. Instrument: `code/scanner_v2.py`. Population: the primes
in [10^5, 10^6] (expected n = 68,906), as in scanner v1.

## Battery (12 features, tagged by observer class)

| # | feature | definition | class |
|---|---|---|---|
| 1 | Om(p-1) | number of prime factors with multiplicity | crystal |
| 2 | Om(p+1) | ditto for p+1 | crystal |
| 3 | slope | log P(p-1) / log p, P = largest prime factor | crystal |
| 4 | Pratt h | height of the Pratt certificate tree | crystal |
| 5 | gap | (next_prime - p) / log p | spacing |
| 6 | bits | binary digit sum of p | automatic |
| 7 | om(p-1) | distinct prime factors of p-1 | crystal |
| 8 | sf | 1 if (p-1)/2 squarefree else 0 | crystal |
| 9 | chi4 | +1 if p = 1 mod 4 else -1 | congruence |
| 10 | chi3 | +1 if p = 1 mod 3 else -1 | congruence |
| 11 | tm | Thue-Morse sign: +1 if bits(p) even else -1 | automatic |
| 12 | rs | Rudin-Shapiro sign: parity of "11" occurrences in binary p | automatic |

## Null model and tests

- Strata: coprime residue mod 60 (16 classes) x 4 logarithmic size bands = 64 strata.
  **Instrument upgrade over v1**: mod 60 determines p mod 4 and p mod 3, closing the
  mod-4 blindness that v1's own audit discovered (its 2-adic cluster).
- Standardize within stratum; features constant within every stratum (chi4, chi3
  same-prime) become identically 0 and their same-prime tests degenerate — predicted
  and intended: v1's same-prime chi4 cluster should be absorbed by the finer null.
- Tests: all same-prime pairs (66) and all consecutive-prime ordered pairs (144),
  210 total. Permutation nulls B = 200, rng seed 20260803 (deterministic).
- Survival: |z_disc| >= 3.9 on the full sample AND same-sign |z| >= 3.0 on both
  split halves (replication built into survival, tightened from v1).

## Exclusions (mechanical, preregistered)

Same-prime pairs within {bits, tm, rs} are definitionally entangled (tm is the parity
of bits; rs shares the digit string) — computed and reported but classified
"mechanical" without audit.

## Committed predictions

P1. chi4 x chi4 (consecutive) FIRES, negative z (Lemke Oliver–Soundararajan mod 4;
    v1 measured z = -27).
P2. chi3 x chi3 (consecutive) FIRES, negative z <= -8 (LOS repulsion mod 3 — a new
    positive control not present in v1's battery).
P3. gap x gap (consecutive) FIRES, negative z (known gap anticorrelation).
P4. THEOREM-NULL: no automatic-class feature (tm, rs, bits) survives in any
    consecutive-prime test, and none survives same-prime tests against other classes
    beyond mechanical size-budget entanglements of bits (v1's detrending lesson).
    Rationale: Mauduit–Rivat / Müllner orthogonality. A robust replicated violation
    would be instrument-bug-until-proven-otherwise, then refutation-grade.
P5. The v1 same-prime chi4 cluster (Om(p-1) x chi4 etc.) is ABSENT under the mod-60
    null (absorbed skeleton leak).
P6. The crystal-feature same-prime mechanical cluster (size-budget entanglements:
    slope x Om, Om x sf, ...) fires as in v1 and classifies mechanical.
P7. Candidates after the audit ladder: ZERO.

## Success criterion

The instrument passes first light if P1–P3 fire, P4's theorem-null holds, and every
survivor classifies at or below "known theorem" on the audit ladder.
