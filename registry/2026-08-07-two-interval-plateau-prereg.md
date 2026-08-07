# Preregistration: two-interval plateau, out-of-sample (WP-RH3b)

Committed before first run. Instrument: `code/two_interval_plateau.py`. Lane: WP-RH.

## Provenance of the hypothesis (stated plainly)

WP-RH3's committed prediction P3 was REFUTED (window in the truncation-decay
regime), and a **post-hoc** diagnostic on the same data showed the earlier
plateau (n = 11..40 of the N = 40 reconstruction) matching the universal
two-interval equilibrium `((γ_N + γ_1)/2, (γ_N − γ_1)/2)` to within 1.4. Under
the registry discipline a post-hoc reading on in-sample data cannot be claimed.
This prereg converts it into a falsifiable out-of-sample test: the two-interval
law must *predict* the plateau of reconstructions it has never seen — new
truncations N = 50 and N = 60, whose equilibrium targets
`(78.62, 64.49)` and `(88.58, 74.45)` differ substantially from the N = 40
values the hypothesis was read from.

Claim under test: **the plateau of the reconstructed Hamiltonian is the
arithmetic-free two-interval equilibrium of the spectral gap** — the leading
structure of the canonical-system data depends only on (γ_1, γ_N), not on
where the primes are. If confirmed, this becomes the MACHINE-status form of
spec row 6's negative constraint (smoothness accounts for the gap and the
window; arithmetic must live in the corrections).

## Instrument constants (frozen)

- Reconstructions: Stieltjes (dps 40, equal weights) on symmetric atoms
  `{±γ_1..±γ_N}` for `N ∈ {50, 60}`; zeros at dps 30 via `zetazero` (reused
  convention of WP-RH2/RH3).
- Plateau windows, scaled from the N = 40 post-hoc window (11..40 of 2N−1):
  N = 50 → `n = 14..50`; N = 60 → `n = 17..60`. Parity split: odd-n mean vs
  `(γ_N + γ_1)/2`, even-n mean vs `(γ_N − γ_1)/2`.
- Continuity row (report only, NOT a gate — in-sample): the N = 40 plateau
  means from WP-RH3's diagnostic.

## Gates (frozen)

- **T1.** All four out-of-sample deviations `|parity mean − target| < 3.0`
  (two truncations × two parities).

## Committed predictions (non-gating)

- **U1.** All four signed deviations are negative (means sit below equilibrium,
  as both N = 40 parities did: −1.13, −1.38), in `[−3, 0]`.
- **U2.** Per truncation, the odd deviation is smaller in magnitude than or
  comparable to the even (as at N = 40); no crossing above equilibrium.

## Exclusions and notes

- A REFUTED T1 kills the claim; the post-hoc N = 40 reading would then stand
  recorded as a coincidence of that window. Results append-only; thresholds
  frozen; bring-up fixes with honest notes only.
- Librarian: period-2 recurrence asymptotics on two-interval essential support
  is classical orthogonal-polynomial theory (Chebyshev-type/Akhiezer;
  Turán-school; see also Simon's szegő-class treatments). The claim here is
  not the asymptotic theorem but the measured identification of the zeros'
  reconstruction plateau with it at finite N, out of sample.
