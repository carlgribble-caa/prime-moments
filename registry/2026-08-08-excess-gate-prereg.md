# Preregistration: gating the beyond-skeleton excess (WP-C3b)

Committed before first run. Instrument: `code/excess_gate.py`. Lane: WP-C.
Promotes C3's post-hoc micronat bound to a gated claim, on the lane's
template: the formula and thresholds are frozen here, and the test runs on
windows never touched by any prior instrument.

## Provenance and design analysis (stated plainly)

C3 measured, post hoc and in sample, a beyond-skeleton pairwise excess of
3×10⁻⁶ nats at [10⁷, 10⁸). Noise accounting, fixed here: with the model's
margins taken empirically, each gap contributes ~1 free parameter, so the
pure-noise expectation of the KL excess is ≈ (number of gaps)/(2·Ā) with Ā
the mean admissible-pair count — ≈ 9×10⁻⁷ nats for 45 gaps at these window
sizes. The in-sample 3×10⁻⁶ is ~3× that floor: consistent with noise plus at
most micronat-scale second-order structure. The out-of-sample gate is set at
10⁻⁵ — an order above the floor, 200× below C2's eps.

## Instrument constants (frozen)

- Sieve to 3×10⁸. Fresh windows: W_A = [10⁸, 2×10⁸), W_B = [2×10⁸, 3×10⁸)
  (no prior instrument has touched either).
- Coprime-to-30 mask by tiled period-30 pattern; admissible pairs and joint
  counts per even gap d ∈ {2, 4, ..., 90} exactly as C3.
- Congruence model, committed: `R_model(d) = T₇ · Π_{p|d, 7≤p≤89} (p−1)/(p−2)`
  with `T₇ = C₂ / ((3/4)(15/16))`, C₂ over primes < 10⁶; model joint
  `m11 = p1·q1·R_model(d)` with empirical margins p1, q1.
- Excess(W) = Σ_d KL(empirical 2×2 ‖ model 2×2), nats.
- Sanity rows: HL ratios (as C3's Q1, with per-window `E = ∫ dt/ln²t`) at
  gaps {2, 6, 30, 210}.

## Gates (frozen)

- **V1 (instrument sanity on fresh windows).** HL ratios ∈ [0.99, 1.01] at
  the four sanity gaps, both windows.
- **V2 (the excess, out of sample).** `excess(W) ≤ 1×10⁻⁵ nats` for BOTH
  fresh windows.

## Committed predictions (non-gating)

- **X1.** excess ∈ [5×10⁻⁷, 6×10⁻⁶] in each window.
- **X2.** excess / noise-floor ∈ [0.5, 6] in each window (noise-dominated).
- **X3.** The wheel-conditional constancy (C3's Q3 statistic) replicates on
  both fresh windows: small-prime-gap spread ≤ 1.01.

## What a pass earns

The claim, at MACHINE status: **the beyond-skeleton pairwise content of the
prime indicator over the full history span is ≤ 10⁻⁵ nats at heights up to
3×10⁸, consistent with pure statistical noise** — the two-skeleton
conjecture at the pair level, gated out of sample. This becomes WP6's fifth
measured base camp. A fail is reported as measured structure beyond the
congruence model and goes up the audit ladder.

## Exclusions and notes

- Thresholds frozen; results append-only; bring-up fixes with honest notes.
- Librarian: second-order corrections to HL pair counts (log-scale terms,
  Bogomolny–Keating-type) are the known candidate occupants of any excess
  above noise; a detected excess would be tested against them first.
