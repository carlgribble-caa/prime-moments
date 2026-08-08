# Results: gating the beyond-skeleton excess (WP-C3b)

Prereg: `2026-08-08-excess-gate-prereg.md`, committed at `9e43a05` before
first run. Instrument: `code/excess_gate.py` (43 s; sieve to 3×10⁸). Results
are append-only. Both gates PASS; all six prediction cells confirmed.

## Gates and predictions

| Window | HL sanity (4 gaps) | excess (nats) | noise floor | ratio | R_w spread |
|---|---|---|---|---|---|
| W_A = [1e8, 2e8) | 0.9991–1.0001 | **0.0000009** | 0.0000018 | 0.53 | 1.0011 |
| W_B = [2e8, 3e8) | 0.9992–1.0006 | **0.0000012** | 0.0000018 | 0.69 | 1.0024 |

- **V1 (sanity): PASS** — HL at the few-×10⁻⁴ level on both fresh windows.
- **V2 (the excess): PASS** — both windows an order below the 10⁻⁵ gate, and
  in fact **below the pure-noise expectation** (X2 ratios 0.53 and 0.69):
  the measured beyond-skeleton content is statistically indistinguishable
  from zero.
- X1, X2, X3 all CONFIRMED in both windows (constancy replicating at 0.1–0.2%).

## The claim, earned at MACHINE status

**The beyond-skeleton pairwise content of the prime indicator over the full
history span (gaps 2–90) is ≤ 10⁻⁵ nats at heights up to 3×10⁸, and is
consistent with pure statistical noise.** The congruence model — C₂-tail
times the (p−1)/(p−2) factors of the primes dividing the gap, nothing else —
accounts for the pair structure of the primes to the resolution of ~5×10⁶
primes per window. This is the two-skeleton conjecture at the pair level,
gated out of sample on windows no prior instrument had touched: **WP6's
fifth measured base camp**, and the sharpest.

## Chain of custody (the lane's template, completed twice over)

C2 (trained observer sees nothing beyond skeleton; resolution caveat) → C3
(caveat addressed; raw-MI gate refuted on a diagnosed design flaw; post-hoc
decomposition suggests micronats) → C3b (corrected quantity committed with
noise accounting, tested on fresh windows, gated). Every step's error is on
the record; the final claim rests only on frozen-gate, out-of-sample
measurements.

## Lane status

WP-C stands at C1–C3b complete: the spec matrix with its one OPEN cell, and
around it a measured obstruction profile now including a gated micronat
bound. Remaining candidates: the WP-C librarian pass (required before any of
this prints), and the WP6 write-up that now has five measured base camps to
stand on.
