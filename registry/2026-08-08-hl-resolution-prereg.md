# Preregistration: the HL resolution test (WP-C3)

Committed before first run. Instrument: `code/hl_resolution.py`. Lane: WP-C.
Closes the caveat recorded in C2's results: the Hardy–Littlewood short-range
content of the residual was either absorbed by the enriched baseline or below
the ~0.001-nat holdout resolution — pair counts decide, at ~0.2% precision.

## Instrument constants (frozen)

- Sieve to 10^8; window W = [10^7, 10^8) (~9×10^7 positions, ~5.3M primes).
- Pair counts `P(d)` = #{n ∈ W : n, n+d both prime} by shifted AND.
- HL prediction: `P_HL(d) = S(d) · E`, `E = ∫_W dt/ln²t` (d ≪ scale, so one
  integral serves all gaps), `S(d) = 2 C₂ Π_{p|d, p>2} (p−1)/(p−2)` for even
  d, with `C₂ = Π_{p>2} (1 − (p−1)^{-2})` computed over primes < 10^6.
- Committed gaps: d ∈ {2, 4, 6, 8, 10, 12, 14, 18, 30, 210}.
- Wheel-conditional enhancement: `R_w(d) = P(d) / (ρ_c² · A(d))` with ρ_c the
  prime density among wheel-30-coprime positions and `A(d)` the exact count
  of positions n ∈ W with n and n+d both coprime to 30.
- Information accounting: for even d = 2..90, the mutual information `I(d)`
  between the two indicator bits of admissible pairs at gap d, from measured
  joint counts; `total_I = Σ_d I(d)` (nats) — the pairwise information
  available to a 24-restricted-position history, upper-bounding what C2's
  challenger could have gained from pair structure.

## Gates (frozen)

- **Q1 (HL verified quantitatively).** `P(d)/P_HL(d) ∈ [0.97, 1.03]` for all
  ten committed gaps.
- **Q2 (the C2 caveat closed).** `0 < total_I < 0.002` nats: the pairwise
  content is real but below C2's eps — C2's null stands validated. (If
  total_I ≥ 0.002, C2's M2 conclusion is reopened and the results file says
  so.)
- **Q3 (congruence-derivability of the enhancements).** (a) `R_w(d)` is
  constant across the small-prime-only gaps {2, 4, 6, 8, 10, 12, 30}:
  max/min ≤ 1.04; (b) the mod-7 jump: `R_w(14)/mean(R_w small-prime gaps)`
  ∈ [1.14, 1.26], and the same for `R_w(210)/R_w(30)` (both predicted
  (7−1)/(7−2) = 1.20): the short-range structure is exactly the congruence
  skeleton's, down to which primes divide the gap.

## Committed predictions (non-gating)

- **U1.** `P(d)/P_HL(d) ∈ [0.99, 1.01]` at all ten gaps (HL at the percent
  level in this window).
- **U2.** `total_I ∈ [0.0002, 0.0015]` nats.
- **U3.** Small-prime-gap constancy spread ≤ 1.5%.

## Exclusions and notes

- Librarian, upfront: HL (1923) own the conjectured law; numerical
  verification of S(d) is classic. The deliverables are the nats accounting
  (closing C2), the wheel-conditional constancy/jump table as the
  audit-ladder's "skeleton-derivable" stage made quantitative, and the
  observer-ladder placement: pairwise content exists at ~10^{-3} nats,
  visible to counting statistics, invisible to every observer class C1/C2
  tested. Thresholds frozen; results append-only; bring-up fixes with
  honest notes.
