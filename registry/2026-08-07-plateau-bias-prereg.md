# Preregistration: the plateau bias is a density effect (WP-RH3c)

Committed before first run. Instrument: `code/plateau_bias.py`. Lane: WP-RH.

## Provenance and claim

WP-RH3b confirmed, out of sample, that the Jacobi/Krein reconstruction's plateau
is the two-interval equilibrium of the spectral gap, with a systematic negative
bias recorded as observed-but-unclaimed: deviations from equilibrium of
(−1.13, −1.38) at N = 40, (−1.07, −1.75) at N = 50, (−1.43, −2.79) at N = 60
(odd, even). Candidate mechanism recorded there: the zeros' density grows toward
the outer window edge, deforming the classical (arcsine-weight) equilibrium —
i.e. the bias is a property of the *mean density*, not of the primes.

Claim under test: **the bias is arithmetic-free** — the smooth comb
`Nbar^{-1}(k − 1/2)`, which carries the same mean density and no arithmetic,
reproduces it. If confirmed, the "primes live in the corrections" constraint
deepens one level: not only the plateau's location but its *deviation from the
universal limit* is density-driven, so the arithmetic content of the
canonical-system data is confined to the residual fluctuations already measured
in WP-RH2 (rigidity scale, std ≈ 2.2 per coefficient).

## Instrument constants (frozen)

- Reconstructions: Stieltjes (dps 40, equal weights) on symmetric atoms for the
  zeros and for the smooth comb `Nbar^{-1}(k − 1/2)` (bisection at mp precision,
  `Nbar(E) = (E/2π)(ln(E/2π) − 1) + 7/8`), truncations `N ∈ {50, 60}`,
  plateau windows as WP-RH3b: N = 50 → n = 14..50; N = 60 → n = 17..60;
  parity-split means; equilibrium targets `(γ_N ± γ_1)/2` computed from the
  zeros in both cases (the smooth comb approximates the same support; using the
  zeros' targets for both keeps the comparison on one scale).
- Bias := (parity mean) − (equilibrium target), per comb, truncation, parity.

## Gates (frozen)

- **V1 (density reproduces the bias).** `|bias(zeros) − bias(smooth)| < 1.0`
  in all four cells (2 truncations × 2 parities).
- **V2 (sign).** `bias(smooth) < 0` in all four cells.

## Committed predictions (non-gating)

- **W1.** `|bias(zeros) − bias(smooth)| < 0.5` in at least 3 of 4 cells (the
  residual difference is the rigidity-scale fluctuation of window means,
  expected ≈ 2.2/sqrt(#coefficients in window) ≈ 0.5).
- **W2.** The bias magnitude ordering across truncations matches between combs
  (even-parity bias grows with N in both).

## Exclusions and notes

- A REFUTED V1 would mean the bias carries arithmetic content beyond density —
  itself a significant finding, to be reported as such and escalated up the
  audit ladder rather than dissolved.
- Thresholds frozen; bring-up fixes with honest notes only; results append-only.
- Librarian: recurrence-coefficient asymptotics under non-equilibrium weights
  is classical potential-theory territory (Kuijlaars–Van Assche school on
  varying weights); the claim here is the measured attribution of the bias to
  density, not the asymptotic theory.
