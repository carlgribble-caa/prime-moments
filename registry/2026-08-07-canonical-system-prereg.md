# Preregistration: canonical-system reconstruction, first light (WP-RH2)

Committed before first run. Instrument: `code/canonical_system.py`. Lane: WP-RH.
RH is equivalent to the zero comb being the spectral measure of a canonical system
(de Branges/Krein) whose Hamiltonian nobody has exhibited. This instrument
computes the two tractable shadows of that object and measures what the
arithmetic-free version is missing:

- **Part A (discrete Krein/Jacobi).** The three-term recurrence coefficients of
  orthogonal polynomials for the symmetric atomic measure on the first zeros —
  the discretized Hamiltonian data — reconstructed by Stieltjes orthogonalization,
  with two control combs of identical mean density.
- **Part B (semiclassical inverse + forward solve).** The smooth (arithmetic-free)
  potential whose WKB counting matches the zeros' mean counting function, built by
  Abel inversion in closed form, solved forward by Numerov shooting; committed
  measurement: the spectral residuals correlate with the prime comb — in operator
  language, **what the smooth Hamiltonian lacks is exactly the primes**.
- **Part C (solved universe).** The elliptic-curve Frobenius measure, where the
  reconstruction terminates: the Hamiltonian is finite and exact (RH1's tightness
  finding in Hamiltonian coordinates).

## Instrument constants (frozen)

- Part A: first `N_A = 40` zeros, symmetric equal-weight atoms `{±γ_k}`; Stieltjes
  at `dps = 40`, full length `M = 80`; recurrence `x p_n = a_{n+1} p_{n+1} + b_n p_n
  + a_n p_{n-1}`. Controls, same construction: (i) smooth comb at
  `Nbar^{-1}(k − 1/2)`; (ii) Poisson comb from deterministic uniforms (consecutive
  6-digit blocks of π's decimal digits, `u_k = block/10^6`), unfolded positions
  `x̃_k = (Σ_{j≤k} −ln u_j) − 1/2` (shifted by `0.3 − x̃_1` if `x̃_1 < 0.3`), mapped
  through `Nbar^{-1}`. Here `Nbar(E) = (E/2π)(ln(E/2π) − 1) + 7/8`.
- Part B: first 62 zeros; `V0 = 2π`; Abel-inverted half-width in closed form
  (derived by parts from `x(V) = (1/π)∫_{V0}^{V} (ln(E/2π)/2π)/sqrt(V−E) dE`):

      x(V) = [ −2u + sqrt(V) ln( (sqrt(V)+u)/(sqrt(V)−u) ) ] / π²,   u = sqrt(V − 2π)

  domain half-length `L = x(450)`; Numerov shooting on `[0, L]`, 8000 steps, parity
  split (even/odd from the origin), eigenvalue `k` selected by half-line node count
  (predicate: sign-change count ≥ ⌊(k−1)/2⌋ + 1), 60 bisection iterations, float64.
  Validation well: `V = x²` on `[0, 8]`, 8000 steps (exact eigenvalues `2n+1`).
  Prime side: `S(E) = −(1/π) Σ_{2≤n≤1000} Λ(n)/(sqrt(n) ln n) sin(E ln n)
  exp(−(ln n)²/18)`; mean density `ρ̄(E) = ln(E/2π)/(2π)`. Residuals
  `δ_k = γ_k − E_k` by index (node count fixes the index unambiguously).
  Correlation window `k = 10..60`; both series linearly detrended in `k`
  (least squares) before Pearson — this absorbs smooth WKB systematics,
  including the expected 1/8 Maslov/normalization offset of the `V0 = 2π`
  convention (`Nbar(E_k) ≈ k − 5/8` vs `Nbar(γ_k) ≈ k − 1/2 − S(γ_k)`).
- Part C: curve and prime as WP-RH1 (`y² = x³ + x + 1` over `F_10007`, trace
  `a = −57`), Frobenius line measure `{±θ}`, `θ = arccos(a/(2·sqrt(p)))`, `dps = 40`.

## Gates (PASS/FAIL, thresholds frozen)

- **A1 (symmetry).** All three combs: `max |b_n| < 1e-20`.
- **A2 (exact reconstruction).** Zero comb: eigenvalues of the full 80×80 Jacobi
  matrix reproduce the atoms, `max |sorted eig − atoms| < 1e-8`.
- **B1 (closed form).** Closed-form `x(V)` vs direct quadrature at
  `V ∈ {10, 30, 80, 200, 400}`: max relative difference `< 1e-8`.
- **B2 (solver validation).** Harmonic well: first 10 eigenvalues within `1e-6`
  of `2n+1`.
- **B3 (counting).** Number of reconstructed eigenvalues `≤ C = (γ_60+γ_61)/2`
  within `60 ± 2`.
- **B4 (tracking).** `RMS(δ_k), k = 10..60` `< 1.0`.
- **B5 (the primes are the residual — headline).** Pearson correlation of the
  detrended series `δ_k·ρ̄(γ_k)` against detrended `−S(γ_k)`, `k = 10..60`:
  `r > 0.4`.
- **C1 (termination in the solved universe).** Stieltjes on the Frobenius
  measure terminates at step 2 (residual `< 1e-30`); `J_2` eigenvalues `= ±θ`
  to `1e-30`; moments `m ≤ 6` reproduced to `1e-30`.

## Committed predictions (non-gating; discrepancies reported as such)

- Q1. `r` (gate B5) lands in `[0.6, 0.95]`: the arithmetic-free canonical object
  tracks the zeros at the mean-density level and fails at fluctuation order by
  the prime comb, quantitatively.
- Q2. Rigidity in Hamiltonian coordinates:
  `std(a_n^zeros − a_n^smooth) / std(a_n^Poisson − a_n^smooth) < 0.7` over
  `n = 6..70` — the zeros' Jacobi coefficients hug the smooth comb's tighter
  than Poisson's do (spectral rigidity read in the reconstruction).
- Q3. Maslov offset: `mean(δ_k·ρ̄(γ_k) + S(γ_k))` over the window lands in
  `[0.0, 0.25]` (predicted center 1/8, from the `V0 = 2π` convention).
- Q4. Part C terminates exactly, sharpening RH1-P4: in the universe where the
  RH-analogue is a theorem the canonical system is a finite matrix; for ζ the
  reconstruction is infinite and its truncations' missing content is measured
  by B5 to be the primes. Carried to WP-RH3 as a requirements-spec line: any
  candidate Hilbert–Pólya structure must carry the prime comb at fluctuation
  order in its Hamiltonian data.

## Exclusions and notes

- Part B runs in float64 (residuals are O(0.1); double precision is honest for
  every gated quantity there); Parts A and C run in mpmath at dps 40.
- Bring-up bugs (bracket widening, node-count edge cases, quadrature breakpoints)
  may be fixed with an honest note in the script header; thresholds are frozen;
  results are append-only.
- Librarian, upfront: Wu–Sprung potentials (1993) and the physics-of-zeta
  literature (Schumayer–Hutchinson review; Berry–Keating) own Part B's
  construction; random-Jacobi spectral theory (Killip–Nenciu) is adjacent to Q2.
  Novelty presumption low throughout; the value is the measured tables, the
  controls, and the requirements-spec line carried to WP-RH3. Any candidate
  statement goes up the audit ladder before the word "candidate".
