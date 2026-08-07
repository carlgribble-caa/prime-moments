# Preregistration: the primes in the Hamiltonian coefficients (WP-RH4)

Committed before first run. Instrument: `code/coefficient_primes.py`. Lane: WP-RH.

## Claim under test, and its grounding

WP-RH2/3b/3c established that every leading structure of the Jacobi/Krein
reconstruction (gap, window, plateau, bias) is arithmetic-free, confining the
primes to the rigidity-scale coefficient residual `c_n = a_n(zeros) −
a_n(smooth)`. This instrument tests whether the primes are *individually
legible* there, at their explicit-formula amplitudes.

Grounding (fixed before any measurement): the two combs differ by position
shifts `δ_k = γ_k − E_k ≈ −S(γ_k)/ρ̄(γ_k)` (Riemann–von Mangoldt; no WKB
enters), and `S(E) ≈ −(1/π) Σ_m Λ(m)/(√m ln m) sin(E ln m)`. So `c_n` should be
a superposition of coefficient-space responses to per-frequency position
modulations, with **committed amplitudes** `β_pred(m) = Λ(m)/(π √m ln m)` at
frequencies `ω = ln m`, m over prime powers — and nothing at off-prime
frequencies. The response templates are computed by finite differences (below),
so the entire analysis is a committed linear model; nothing is fit by eye.

If confirmed: the canonical-system coefficients carry von Mangoldt's function —
prime powers at their `Λ`-weights, the "overtone" structure included — which is
spec constraint 1 (WP-RH3) measured directly in the Hamiltonian data. A partial
or failed detection is reported as measured (leakage/nonlinearity diagnosed),
not dissolved.

## Instrument constants (frozen)

- Truncation N = 60; zeros at dps 30; all Stieltjes runs at dps 40, equal
  weights, symmetric atoms, M = 2N.
- Smooth comb: `Nbar^{-1}(k − 1/2)`. Residual `c_n = a_n(zeros) − a_n(smooth)`.
- Templates: `T_n(ω) = [a_n(smooth positions E_k + ε sin(ω E_k)/ρ̄(E_k)) −
  a_n(smooth)]/ε`, `ε = 1e-6`, `ρ̄(E) = ln(E/2π)/(2π)`.
- Battery (prime powers): ω = ln m for m ∈ {2, 3, 4, 5, 7, 8, 9, 11, 13}.
  Controls (off-prime): ω ∈ {0.90, 1.25, 1.80, 2.30}.
- Committed amplitudes: β_pred(m) = Λ(m)/(π √m ln m):
  m=2: 0.22508; 3: 0.18378; 4: 0.07958; 5: 0.14235; 7: 0.12026; 8: 0.03751;
  9: 0.05305; 11: 0.09598; 13: 0.08828. Controls: 0.
- Analysis window n = 15..75. Joint least squares of `c_n` on the 13 templates
  plus 6 nuisance regressors: {1, ñ, ñ², (−1)^n, (−1)^n ñ, (−1)^n ñ²},
  ñ = (n − 45)/30. Design condition number reported (not gated).

## Gates (frozen)

- **X1 (linearity).** The m = 2 template from ε and ε/10 agrees to 1e-3
  relative (max-norm).
- **X2 (detection).** For m ∈ {2, 3, 5, 7}: β(m) positive and
  `0.6 ≤ β(m)/β_pred(m) ≤ 1.4`.
- **X3 (nulls).** All four control amplitudes `|β| < 0.06` (half the smallest
  gated prime prediction).

## Committed predictions (non-gating)

- **Y1.** m = 2 and m = 3 land in the tight band `[0.8, 1.2] × β_pred`.
- **Y2.** The prime-power overtones m ∈ {4, 8, 9} are detected within ±50% of
  their Λ-weighted predictions — the coefficients know von Mangoldt's weights,
  not merely prime positions.
- **Y3.** The committed model (battery + nuisance) explains most of the
  residual: R² > 0.8 over the window.

## Exclusions and notes

- Second-order effects (shift² / spacing ~ 4%) and leakage from unmodeled
  prime powers m ≥ 16 (amplitudes ≤ 0.04) are the known noise floor; the gates
  are set with those margins.
- Thresholds frozen; bring-up fixes with honest notes only; results
  append-only.
- Librarian: the mechanism chain (RvM + linear response of recurrence
  coefficients to spectral perturbations; Szegő-class asymptotics adjacent
  \[Simon; Damanik–Killip–Simon\]) is classical; a table reading Λ(m) off the
  zero comb's Jacobi coefficients with committed matched filters is, to our
  searches, untabulated. Any claim of novelty would still require the full
  librarian pass; the result stands as a measured table regardless.
