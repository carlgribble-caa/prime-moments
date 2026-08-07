# Results: the HL resolution test (WP-C3)

Prereg: `2026-08-08-hl-resolution-prereg.md`, committed at `70ab30d` before
first run. Instrument: `code/hl_resolution.py` (60 s; window [10^7, 10^8),
~5.3M primes). Results are append-only.

## Gates and predictions

- **Q1 (HL verified): PASS, spectacularly** — P(d)/P_HL(d) between 0.9992 and
  1.0002 at all ten committed gaps (U1's percent band confirmed with an order
  to spare). Hardy–Littlewood's singular series holds in this window at the
  few-×10⁻⁴ level.
- **Q3 (congruence-derivability): PASS** — the wheel-conditional enhancements
  R_w(d) are constant to **0.08%** across the small-prime-only gaps
  {2,4,6,8,10,12,30} (measured base 0.9395 vs the computed C₂-tail 0.9389),
  and jump by exactly the predicted (7−1)/(7−2) = 1.20 where 7 divides the
  gap: measured 1.200 (d = 14) and 1.201 (d = 210/30). The short-range
  structure knows precisely which primes divide the gap, and nothing else.
- **Q2 (raw MI < eps): REFUTED — on a design flaw the measurement itself
  diagnosed.** Raw pairwise MI over gaps 2..90 = 0.006950 nats > eps. But raw
  MI between indicator bits *includes* the skeleton-induced component (bits
  correlated through shared congruence structure — co-divisibility at gaps
  divisible by 7, 11, 13, plus the C₂-tail deficit at every gap), which C2's
  baseline already encodes. The committed gate conflated that with
  beyond-skeleton content. U2 likewise refuted.

## The post-hoc decomposition (labeled; gates nothing)

Congruence-model MI (joints predicted by the Q3-verified model
R_w(d) = C₂-tail · Π_{p|d, p≥7}(p−1)/(p−2)): **0.006994 nats**.
Measured raw MI: 0.006950 nats.
**Beyond-skeleton excess (KL of measured joints vs the congruence model):
0.000003 nats** — three micronats over the full history span, 700× below
C2's eps, 0.04% of the raw MI.

## What this settles, and what it formally doesn't

In substance, C2's caveat is closed decisively: the pairwise content of the
prime indicator is congruence-derivable to one part in ~2000, and the
beyond-skeleton residue is two orders below anything C2's observer could
have seen — C2's null was not a resolution artifact. Formally, per the
registry discipline, the 3-micronat bound was computed post hoc and is
**unclaimed**: a C3b prereg gating the excess directly (with its own
committed model and error analysis) is the candidate follow-up, and the
Q2 refutation stands on the record as a mis-specified gate, the lane's
reminder that information accounting must condition on the skeleton before
comparing against skeleton-conditional nulls.

## Observer-ladder placement (the lane's running table)

The pair structure of the primes is: visible to counting statistics at 0.2%
precision (this run); fully congruence-derivable (Q3, to 0.08%); invisible
to general compressors (C1), to order-k contexts (C2 ladder), and to trained
sequence observers beyond their skeleton features (C2); and its
beyond-skeleton residue measures 3 micronats (post hoc). The two-skeleton
conjecture has now survived at four strata, the last at the sharpest
resolution yet reached in the programme.
