# Preregistration: the transfer law on a second family (WP-RH5b)

Committed before first run. Instrument: `code/dirichlet_transfer.py`. Lane:
WP-RH. This executes item (iii) of the WP-RH5 conjecture's falsification
protocol: the same law, on a different zeta family.

## Claim under test

The transfer-law conjecture, applied to `L(s, χ₋₄)` (the Dirichlet beta
function): the per-frequency transfer of the χ-weighted prime comb into the
zeros' shift field obeys the same Debye–Waller law
`T = exp(−a (ω/2πρ̄_W)²)` with the recorded `a = 1.1416`, where now the
explicit-formula amplitudes carry the character: predicted regression ratio at
frequency `ln m` equals `χ₋₄(m) · T(ln m)`. Structural consequences unique to
this family, all committed: the even frequencies are **forced nulls**
(χ(2^k) = 0), and the odd frequencies carry the **character sign pattern**
−, +, −, −, + at m = 3, 5, 7, 11, 13.

## Instrument constants (frozen)

- Family: `β(s) = L(s, χ₋₄) = 4^{−s}(ζ(s, 1/4) − ζ(s, 3/4))` (Hurwitz), dps 30.
  Completed function `Λ(s) = (4/π)^{(s+1)/2} Γ((s+1)/2) β(s)`, real on the
  critical line (ε = 1); zeros located by sign changes of `Z(t) = Re Λ(1/2+it)`
  on a scan of step 0.25 over `t ∈ [2, 260]`, refined by 60 bisections; the
  first 150 zeros are used (assert ≥ 150 found; assert `|Im Λ|` negligible).
- Smooth phase: `θ(t) = (t/2) ln(4/π) + Im ln Γ(3/4 + it/2)`;
  `N̄(t) = θ(t)/π` (additive constant absorbed by the nuisance intercept);
  density `ρ̄(t) = θ'(t)/π` with `θ'(t) = (1/2) ln(4/π) + (1/2) Re ψ(3/4 + it/2)`.
- Field and regression exactly as WP-RH4b/RH5: `y_k = N̄(γ_k) − (k − 1/2)` on
  `{sin(γ_k ln m)}`, m ∈ {2, 3, 4, 5, 7, 8, 9, 11, 13}, nuisance {1, k̃, k̃²};
  ratios vs `β_pred(m) = Λ(m)/(π √m ln m)`; `ρ̄_W` = window mean of `ρ̄(γ_k)`.
- Recorded law constant: `a = 1.1416` (WP-RH5). Zero-parameter mechanism
  variant `a₃ = 2π²⟨y²⟩` from this window's own field (reported).

## Gates (frozen)

- **D0 (indexing integrity).** `max_k |y_k − mean(y)| < 0.9` (a missed zero
  shifts the field by 1; the instrument must fail loudly, not mis-index).
- **D1 (forced nulls).** `|ratio(m)| < 0.30` for m ∈ {2, 4, 8}.
- **D2 (character sign pattern).** `sign(ratio(m)) = χ₋₄(m)` for all
  m ∈ {3, 5, 7, 11, 13}: −, +, −, −, +.
- **D3 (the law's magnitudes).** For m ∈ {3, 5, 7}:
  `| |ratio(m)| − exp(−1.1416 τ_m²) | < 0.12`.

## Committed predictions (non-gating)

- **E1.** Mechanism variant `a₃` reproduces m ∈ {3, 5, 7} within 0.10.
- **E2.** m = 13 conforms to the law within 0.15 (probing whether the zeta
  window-3 anomaly at m = 13 is family-specific or persistent).
- **E3.** Gated mean magnitude deviation (D3 set) < 0.06.

## Exclusions and notes

- m = 9 (χ = +1 but tiny amplitude, β_pred = 0.053 against slope noise ~0.04)
  is reported, not gated. Slope noise at 150 zeros is ~±0.04.
- Thresholds frozen; results append-only; bring-up fixes (zero-finder scan
  step, bisection brackets) with honest notes only.
- A pass extends the conjecture across families as its protocol demands; a
  fail is a falsification event and will be recorded exactly as such in the
  conjecture's registry entry.
