# Preregistration: the overtone theory, first light (WP-RH7)

Committed before first run. Instrument: `code/overtone.py`. Lane: WP-RH. This
executes the conjecture's falsification-protocol item on the anomalous
prime-power frequencies, as a theory with out-of-sample teeth.

## The mechanism (fixed before the run)

Because `ln p^k = k ln p` exactly, the regressor at a prime-power frequency is
a pointwise harmonic of the base-prime phase: `sin(γ ln 9) = sin(2 γ ln 3)`.
The zeros' phase distribution along each prime line is biased — Landau's
theorem: `Σ_{γ≤T} cos(γ ln r) ≈ −(T/2π) Λ(r)/√r` — so second-order
self-mixing of a strong p-line deposits phase-locked content at the
frequencies `k ln p`, i.e. exactly at the prime powers. Hypothesis
(the overtone theory): the persistent departures from the Debye–Waller law at
prime-power frequencies (m = 9 low in all four datasets to date; m = 8
erratic) are this mixing, so: (i) they persist at new windows; (ii) they
appear at prime-power frequencies never yet measured (25 = 5², 27 = 3³);
(iii) genuine primes of comparable τ (11, 13) stay on the law.

## Instrument constants (frozen)

- Zeros 1..500 (dps 30). Window 4 = zeros 401..500 (never measured in any
  prior instrument). Extended battery m ∈ {2,3,4,5,7,8,9,11,13,25,27} —
  the last two never measured anywhere. Field, regression, nuisance as
  WP-RH4b/RH5; ratios vs `β_pred(m) = Λ(m)/(π √m ln m)`; DW law with the
  recorded a = 1.1416; per-window ρ̄_w from the zeros.
- Pooled deviations: mean over windows W1..W4 of `ratio(m) − law(m)`.
- Landau input over all 500 zeros with T = γ_500: predicted
  `Σ cos(γ ln r) = −(T/2π) Λ(r)/√r`.

## Gates (frozen)

- **H1a (Landau input, strong lines).** measured/predicted ∈ [0.5, 1.5] for
  r = 2, 3 (signal ≈ 4σ, 500 zeros).
- **H1b (Landau input, signs).** `Σ cos(γ ln r) < 0` for r ∈ {4, 5, 9}.
- **H2 (persistence, out of sample).** Window-4 ratio at m = 9 lands in
  [0.22, 0.55] — the persistent overtone band — while the DW law predicts
  ≥ 0.70 there (reported).
- **H3 (new overtones, out of sample).** Pooled deviations at the
  never-measured frequencies: `mean dev(25) < −0.10` AND `mean dev(27) < −0.10`.
- **H4 (controls).** Pooled |mean dev| ≤ 0.10 for the genuine primes
  m = 11 and m = 13.

## Committed predictions (non-gating)

- **P1.** Window-4 gated set m ∈ {2, 3, 5, 7} still obeys the DW law:
  mean |dev| < 0.06 (continuity of RH5).
- **P2.** Pooled dev(8) is negative (reported either way; m = 8 has been
  erratic and is not gated).
- **P3.** Pooled dev(4) is negative (the 2² overtone; small expected).

## Exclusions and notes

- Slope noise: ~±0.04 absolute per window; ratio noise at the small-amplitude
  lines (25, 27, 9) is proportionally larger — hence pooled gates for H3 and
  a band (not a point) for H2.
- Thresholds frozen; results append-only; bring-up fixes with honest notes.
- If H2–H4 pass, the conjecture gains its overtone clause (v3): at prime-power
  frequencies the displacement-sequence content departs from the smooth DW
  law via phase-locked harmonics of the base-prime lines, with the Landau
  bias as the phase-locking agent; the quantitative overtone coefficient is
  left for derivation alongside the jump-point weight (RH6 target). If they
  fail, the anomalies stand unexplained and the clause is withheld.
- Librarian: Landau (1912) owns Part H1; the harmonic-content reading of
  prime-power lines in the zeros' displacement sequence is, to our searches,
  untabulated. No novelty is claimed beyond the measured tables.
