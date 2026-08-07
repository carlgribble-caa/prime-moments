# Preregistration: the transfer law (WP-RH5)

Committed before first run. Instrument: `code/transfer_law.py`. Lane: WP-RH.

## Provenance and the two candidate laws (fitted on existing data, recorded here)

WP-RH4/4b measured the per-frequency transfer `T(ω)` of the prime comb into the
zeros' shift field at two windows and showed it attenuates with `τ =
ω/(2π ρ̄_w)`. Fitting the two windows' gated points (m ∈ {2, 3, 5, 7}, eight
points; `ρ̄_w` = window mean of `ρ̄(γ_k)`; field and regression exactly as
WP-RH4b's corrected convention):

- **Law A (Debye–Waller):** `T = exp(−a τ²)`, fitted `a = 1.1416`,
  in-sample SSE 0.00231. Mechanism reading: `a = 2π²⟨u²⟩` gives RMS unfolded
  shift 0.240 vs 0.200 measured on the LOW window — the attenuation as the
  Debye–Waller factor of the zeros' displacement field.
- **Law B (linear / form-factor):** `T = 1 − c τ`, fitted `c = 0.5255`
  (strikingly near 1/2), in-sample SSE 0.01905.

Law A wins in-sample by 8×; this prereg sends both to a window neither has
seen. If Law A survives, the lane states its first formally labeled
**CONJECTURE** (the programme's third claim-state): the prime-to-zero transfer
is the Debye–Waller factor of the displacement field, `T = exp(−a τ²)` with
`a ≈ 2π² Var(S̄)` (slowly height-dependent through `Var(S̄) ~ ln ln`), with
falsification protocol: further windows, larger batteries, and other
L-functions.

## Instrument constants (frozen)

- Out-of-sample window: zeros k = 301..400 (heights ≈ 542–680), dps 30;
  disjoint from every prior analysis in the lane. The instrument also
  recomputes both windows 1–2 fits from scratch and asserts agreement with the
  recorded `a`, `c` to 1e-3 (integrity check on this prereg's provenance).
- Field, battery, nuisance, and regression exactly as WP-RH4b (corrected
  convention): `y = Nbar(γ_k) − (k − 1/2)` on `{sin(γ_k ln m)}`,
  m ∈ {2,3,4,5,7,8,9,11,13}, nuisance {1, k̃, k̃²}; ratios vs
  `β_pred(m) = Λ(m)/(π √m ln m)`; `ρ̄_w` from the window's zeros.

## Gates (frozen)

- **S1 (the law holds out of sample).** For all gated m ∈ {2, 3, 5, 7}:
  `|T_meas(m) − exp(−1.1416 τ_m²)| < 0.08`.
- **S2 (model selection).** Over the gated set, `SSE(Law A) < SSE(Law B)`.

## Committed predictions (non-gating)

- **Q1.** Mean absolute deviation from Law A over the gated set < 0.04.
- **Q2.** Extended battery m ∈ {4, 11, 13} within 0.12 of Law A.
- **Q3.** The zero-parameter mechanism variant — `a₃ = 2π²⟨u²⟩` computed from
  the third window's own shifts — predicts the gated points within 0.10
  (reported; this variant consumes same-window data and is a mechanism check,
  not an independent law test).

## Exclusions and notes

- Slope noise at 100 zeros is ~±0.03–0.05 per frequency; the S1 band and Q1
  reflect that.
- Thresholds frozen; results append-only; bring-up fixes with honest notes.
- Librarian: Debye–Waller factors for displaced combs are textbook scattering
  theory; the linear-in-τ alternative echoes the Montgomery form factor. The
  claim, if earned, is the measured law for the zeros' shift field with its
  fitted constant and mechanism identification — to our searches untabulated —
  and it would enter the audit ladder as CONJECTURE with the stated protocol,
  not as a theorem.
