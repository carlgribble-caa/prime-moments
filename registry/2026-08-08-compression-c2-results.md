# Results: stronger observers on the residual (WP-C2)

Prereg: `2026-08-08-compression-c2-prereg.md`, committed at `e482ace` before
first run. Instrument: `code/compression_observers.py` (39 s). Results are
append-only. All three gates PASS; all four predictions confirmed.

## Gates and predictions

| Item | Committed | Measured | Verdict |
|---|---|---|---|
| M1 (positive control) | baseline gain > 0.02 nats | **+0.1846** | PASS |
| N1 | gain ∈ [0.10, 0.25] (computed ≈ 0.166) | +0.1846 | CONFIRMED |
| M2 (two-skeleton, trained observer) | history adds < 0.002 nats | +0.00003 (logistic), +0.00000 (stumps) | PASS |
| N2 | both ≤ 0.001 | max 0.00003 | CONFIRMED |
| M3 (parity at 10^6..10^8) | ratio ≥ 0.97 | **1.0000** | PASS |
| N3 | ∈ [0.99, 1.03] | 1.0000 | CONFIRMED |
| N4 (entropy ladder, report) | expected ≤ 0.01 bits | max excess +0.0022 | CONFIRMED |

## The findings

1. **The observer ladder, quantified.** The residual's predictable content is
   real and sits exactly where the skeleton says: the congruence-flag
   observer extracts 0.185 nats/bit (against a computed divisibility estimate
   of 0.166 + conditional adjustments) — content that C1's zlib observer
   missed almost entirely (0.5%). Observer strata measured to date: zlib
   captures ~42% of the wheel-30 entropy gap and none of the residual;
   order-k contexts see ≤ 0.002 bits; the congruence-informed trained
   observer sees the full local divisibility skeleton.
2. **Two-skeleton at the trained-observer class.** Given the local congruence
   data (current + 3 preceding positions — making HL-derivable short-range
   structure baseline-representable), 24 bits of history plus rolling
   densities add +0.00003 nats: **nothing**. Combined with C1 (compressor
   class) and WP9c (feature class), the two-skeleton conjecture now holds at
   three measured observer strata.
3. **The parity stream stays coin-like an order of magnitude higher**:
   heights 10^6..10^8, ratio 1.0000 to the byte, again.

## Note on the HL worry (recorded in the prereg's design note)

The anticipated Hardy–Littlewood short-range gain either was absorbed by the
enriched baseline as designed, or sits below the ~0.001-nat resolution of a
140k-bit holdout — the run cannot distinguish these; a dedicated
higher-statistics test would. Recorded as a candidate C3, unclaimed.

## Lane status

WP-C now mirrors WP-RH structurally: a spec matrix with one OPEN cell, and
measured profiles bracketing it — the fluctuations of π are (i) full-amplitude
prime-comb in the spectral basis (WP-RH), (ii) structureless beyond the
congruence skeleton to every observer class yet tried (WP-C, three strata),
(iii) coin-like in their parity stream across two decades of height. A
fixed-length closed form would have to compress all three at once.
