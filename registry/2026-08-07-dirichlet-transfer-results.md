# Results: the transfer law on a second family (WP-RH5b)

Prereg: `2026-08-07-dirichlet-transfer-prereg.md`, committed at `c00a255`
before first run. Instrument: `code/dirichlet_transfer.py` (150 s; 150 zeros of
Dirichlet beta located to heights 6.02–234.35, indexing verified). Results are
append-only.

## Gates and predictions

| m | χ | τ | measured ratio | χ·Law (a = 1.1416) | dev |
|---|---|---|---|---|---|
| 2 | 0 | 0.163 | +0.001 | 0 | 0.001 |
| 3 | −1 | 0.258 | −0.905 | −0.927 | 0.022 |
| 4 | 0 | 0.326 | +0.023 | 0 | 0.023 |
| 5 | +1 | 0.379 | +0.823 | +0.849 | 0.026 |
| 7 | −1 | 0.458 | −0.738 | −0.787 | 0.050 |
| 8 | 0 | 0.489 | +0.228 | 0 | 0.228 |
| 9 | +1 | 0.517 | +0.387 | +0.737 | 0.350 |
| 11 | −1 | 0.564 | −0.611 | −0.695 | 0.084 |
| 13 | +1 | 0.603 | +0.577 | +0.660 | 0.083 |

- **D0 (indexing): PASS** (max field excursion 0.503).
- **D1 (forced nulls): PASS** — m = 2 silent to 0.001, m = 4 to 0.023, m = 8
  at 0.228 (inside the gate; see the harmonic note below).
- **D2 (character sign pattern): PASS** — −, +, −, −, + exactly as χ₋₄ demands.
- **D3 (law magnitudes, same recorded a): PASS** — 0.022 / 0.026 / 0.050.
- **E1: REFUTED** — the zero-parameter mechanism variant (a₃ = 2π²⟨y²⟩ = 0.680
  from this window's own variance) fits *worse* than the fixed recorded
  a = 1.1416. The constant transferred across families better than the naive
  local-variance Debye–Waller reading predicts: **a appears more universal
  than the mechanism identification claimed.** The conjecture's mechanism
  clause (`a ≈ 2π² Var(S̄)`) is weakened accordingly; its law clause is
  strengthened.
- **E2: CONFIRMED** — m = 13 conforms here (0.083): the zeta window-3 anomaly
  at m = 13 is window- or family-specific.
- **E3: CONFIRMED** — gated mean magnitude deviation 0.032.

## The cross-family verdict

The conjecture survives falsification item (iii): on a second zeta family the
transfer obeys the same Debye–Waller law with the SAME constant, the even
frequencies are silent exactly as the character demands, and the signs are the
character's. **The law is a property of the prime–zero coupling, not of ζ
alone.**

## Post-hoc observation (recorded, unclaimed): the overtone pattern

Across all measurements to date, the anomalous frequencies are exactly the
prime-power ones: m = 4, 8 (harmonics of ln 2), m = 9 (harmonic of ln 3) —
because `ln p^k = k ln p`, the prime-power frequencies coincide exactly with
the harmonics of the strong prime lines, and second-order terms of the shift
expansion generate content at precisely those harmonics. Consistent here:
m = 9 sits far below its Λ(9) prediction in a family where the ln 3 line is
strong, and m = 8 shows nonzero content in a family where χ kills its own
first-order line entirely. Candidate refinement for a future prereg: a
second-order transfer theory predicting the overtone corrections at p^k from
the p-line amplitudes. Nothing is claimed here.

## Conjecture status after RH5 + RH5b

Transfer law: **confirmed out of sample at a third ζ window and across a
second family with a single recorded constant.** Protocol items remaining:
a fourth ζ window at greater height; the overtone refinement above (which
would absorb the m = 4/8/9 exclusions into the law rather than around it);
derivation from explicit formula + pair correlation (the partial-theorem
target, WP7-lane candidate).
