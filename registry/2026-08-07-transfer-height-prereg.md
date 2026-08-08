# Preregistration: height dependence of the transfer attenuation (WP-RH4b)

Committed before first run. Instrument: `code/transfer_height.py`. Lane: WP-RH.

## Claim under test

WP-RH4 measured a frequency-decaying attenuation of the prime amplitudes in the
shift field of the zeros, with a post-hoc two-factor diagnosis (RvM premise
attenuation at zero-sampling; coordinate decoherence). Both candidate
mechanisms scale with `ω·δ`, and `δ ~ S/ρ̄` shrinks as the zeros densify, so
both predict: **the attenuation weakens with height**. This is committed here
as an out-of-window test on zeros the RH4 analysis never used. A refutation
(height-independent attenuation) would point away from both mechanisms and be
reported as such.

## Instrument constants (frozen)

- Windows: LOW = zeros k = 1..60; HIGH = zeros k = 141..200 (heights ≈ 310–397,
  mean density ≈ 0.63 vs ≈ 0.40). Zeros at dps 30.
- Field (exact, no mean-value approximation): `y_k = (k − 1/2) − Nbar(γ_k)`,
  which equals `−S̄(γ_k)` identically; predicted per-frequency slopes as WP-RH4:
  `β_pred(m) = Λ(m)/(π √m ln m)`.
- Regression per window: y on `{sin(γ_k ln m)}` for m ∈ {2,3,4,5,7,8,9,11,13}
  plus nuisance `{1, k̃, k̃²}` (k̃ centered/scaled per window); report
  slope/`β_pred` ratios.
- Gated subset m ∈ {2, 3, 5, 7}.

## Gates (frozen)

- **Z1 (replication on the exact field).** LOW-window ratios for the gated
  subset are all in [0.2, 1.1] and nonincreasing in ω up to tolerance 0.05
  (the RH4 post-hoc profile, now on the exact field, committed in advance).
- **Z2 (height dependence).** ratio(HIGH) > ratio(LOW) for at least 3 of the
  4 gated frequencies.

## Committed predictions (non-gating)

- **V1.** HIGH-window m = 2 ratio lands in [0.90, 1.05].
- **V2.** Mean improvement over the gated subset in [0.03, 0.25].

## Exclusions and notes

- Regression noise with 60 zeros per window is ~±0.05–0.1 per slope; Z2's
  3-of-4 form absorbs one inversion.
- Thresholds frozen; results append-only; bring-up fixes with honest notes.
- Librarian: height-dependent attenuation of shift-field frequency content is
  adjacent to Berry's semiclassical theory of spectral rigidity and the
  Montgomery form factor; no novelty is presumed for the mechanism. The
  measured two-window profile table is the deliverable.
