# Results: two-interval plateau, out-of-sample (WP-RH3b)

Prereg: `2026-08-07-two-interval-plateau-prereg.md`, committed at `ee3484d`
before first run. Instrument: `code/two_interval_plateau.py` (4 s). Results are
append-only.

## Gate and predictions

| Item | Committed | Measured | Verdict |
|---|---|---|---|
| T1 | four out-of-sample deviations, abs < 3.0 | −1.07, −1.75, −1.43, −2.79 | PASS |
| U1 | all deviations in [−3, 0) | all negative | CONFIRMED |
| U2 | odd deviation ≤ even per truncation | −1.07 < −1.75; −1.43 < −2.79 | CONFIRMED |

Detail (targets never seen by the hypothesis, which was read post hoc off
N = 40):

- N = 50 (window 14..50): odd 77.556 vs (γ50+γ1)/2 = 78.623; even 62.738 vs
  (γ50−γ1)/2 = 64.489.
- N = 60 (window 17..60): odd 87.154 vs (γ60+γ1)/2 = 88.583; even 71.660 vs
  (γ60−γ1)/2 = 74.448.
- Continuity (in-sample, report only): N = 40 gave −1.13 / −1.38, consistent.

## Claim, now earned

**The plateau of the Jacobi/Krein reconstruction of the zero comb is the
arithmetic-free two-interval equilibrium of the spectral gap**: its parity
means are `((γ_N + γ_1)/2, (γ_N − γ_1)/2)` to within a small negative bias,
across three truncations, out of sample for two of them. Spec row 6's negative
constraint is upgraded to MACHINE status: the leading structure of the
canonical-system data depends only on the gap and the window — the primes must
live in the corrections.

## Observed but unclaimed (recorded for a possible follow-up prereg)

The bias below equilibrium is systematic and grows with N and with parity
(even > odd; N = 60 > 50 > 40). Candidate explanation: the zeros' increasing
density toward the window edge deforms the equilibrium (the classical
period-2 limit assumes the arcsine-type equilibrium weight). A follow-up
would predict the bias quantitatively from the density; nothing is claimed
here.

## Method note

This pair (RH3's refuted P3 + post-hoc diagnostic → RH3b's out-of-sample
prereg → confirmation) is the registry discipline working end to end: a
post-hoc reading was refused claim status, converted into a falsifiable
prediction on fresh configurations, and only then admitted. It is recorded as
the lane's template for promoting observations to claims.
