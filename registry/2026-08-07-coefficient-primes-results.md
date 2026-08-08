# Results: the primes in the Hamiltonian coefficients (WP-RH4)

Prereg: `2026-08-07-coefficient-primes-prereg.md`, committed at `26f66ab` before
first run. Instrument: `code/coefficient_primes.py` (7 s). Results are
append-only. **Headline gate X2 REFUTED — on physics, not on instrument error —
and the refutation profile is the finding.**

## Gates and predictions

| Item | Committed | Measured | Verdict |
|---|---|---|---|
| X1 (linearity) | template ε vs ε/10 < 1e-3 | 6.6e-7 | PASS |
| X2 (detection at slope 1) | m ∈ {2,3,5,7}: ratio ∈ [0.6, 1.4], sign + | 0.642, 0.634, 0.414, 0.308 | **REFUTED** |
| X3 (nulls) | four controls \|β\| < 0.06 | max 0.049 | PASS |
| Y1 | m = 2, 3 in [0.8, 1.2] | 0.64, 0.63 | REFUTED |
| Y2 | overtones ±50% | 0.74, 1.12, 0.20 | REFUTED |
| Y3 | R² > 0.8 | **0.9308** | CONFIRMED |

Full per-frequency table in the instrument output. Design condition number 74.

## What was detected, and what was refuted

Detected: every gated prime frequency carries a positive amplitude; all four
off-prime controls are null; the committed model explains 93% of the
coefficient residual's variance. The primes are legible in the Hamiltonian
coefficients — in sign, frequency, and null structure.

Refuted: the committed amplitudes. The naive linear-response premise —
`δ_k ≈ −S(γ_k)/ρ̄` transferred at slope 1 through smooth-comb templates —
over-predicts systematically, with a monotone attenuation profile in frequency:
ratio ≈ 0.64 at ln 2 and ln 3, falling to ≈ 0.31 at ln 7, noise-level by ln 13.
**The transfer function from prime comb to Hamiltonian coefficients is not
unity; its attenuation profile is the measured object this instrument
actually delivered.**

## Post-hoc diagnostic (labeled as such; run after the gates, no reconstruction
involved)

The shift series `δ_k = γ_k − E_k` was regressed per-frequency on sinusoids
sampled two ways:

| m | ω | slope/pred at zeros γ_k | slope/pred at smooth E_k |
|---|---|---|---|
| 2 | 0.693 | +0.922 | +0.688 |
| 3 | 1.099 | +0.809 | +0.634 |
| 4 | 1.386 | +0.714 | +0.646 |
| 5 | 1.609 | +0.648 | +0.479 |
| 7 | 1.946 | +0.554 | +0.391 |
| 11 | 2.398 | +0.411 | +0.250 |
| 13 | 2.565 | +0.335 | +0.068 |

Two attenuation mechanisms separate:

1. **Premise attenuation.** Even sampled at the zeros, the RvM slopes are below
   unity and decay with ω (0.92 → 0.33): the first-order relation
   `δ = −S/ρ̄` degrades with frequency (candidate contributors, all post-hoc:
   second-order shift feedback `S·S'/ρ̄²`, whose cross-terms live on the
   log-additive prime-frequency lattice; the undamped high-m tail; the strongly
   varying `ρ̄` at low height where `δ` reaches ~2).
2. **Coordinate decoherence.** Re-expressing the field in smooth-comb
   coordinates (which the committed templates did) multiplies in a further
   Debye–Waller-type factor — `sin(ωγ)` vs `sin(ωE)` dephase once
   `ω·RMS(δ) ~ 1` — and the smooth-sampled column reproduces the
   coefficient-level measurements (0.69/0.63/0.65/0.48/0.39 vs the instrument's
   0.64/0.63/0.74/0.41/0.31): the Stieltjes transfer itself is close to
   faithful; the attenuation happens in the field description, not in the
   reconstruction.

## Status and carried forward

Under the audit ladder this stands as: measured table (the attenuation
profile), with the detection itself (signs, frequencies, nulls) solid at
MACHINE level and the amplitude law OPEN. A follow-up prereg would commit a
corrected transfer model — zero-sampled phases with an explicit
decoherence factor `e^{−ω²⟨δ²⟩/2}` and a second-order feedback term — and
predict the full profile; care is needed to keep such templates non-circular
(they consume zero positions). Nothing beyond the table above is claimed.

The spec's constraint 1 sharpens rather than closes: the prime comb is present
in the Hamiltonian data at every tested frequency, but the missing object's
coefficients encode it through a nontrivial, frequency-decaying transfer — a
quantitative shape any candidate Hilbert–Pólya structure must now also match.
