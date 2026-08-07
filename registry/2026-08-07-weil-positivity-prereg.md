# Preregistration: Weil positivity explorer, first light (WP-RH1)

Committed before first run. Instrument: `code/weil_positivity.py`. Lane: WP-RH (the
positivity road). Background: RH is equivalent (Weil 1952; Bombieri's survey of the
quadratic functional) to positivity of the explicit-formula functional
`W(g * g~) >= 0` for all admissible test functions. The WP3 pairing engine
(`diffraction_pairing.py`) already computes `W` at Gaussian test functions as an
identity check; this instrument treats the same `W` as a **quadratic form** and
measures its positivity landscape. The words "proof of RH" do not appear in any
artifact of this lane; the deliverable is the landscape, machine-verified.

## Instrument constants (frozen)

- mpmath `dps = 30`; `NZEROS = 60` (ordinates to ~190); prime-side cut `NCUT = 40000`.
- Profile family (Part B): `phi_j(r) = exp(-(r-t_j)^2/4) + exp(-(r+t_j)^2/4)`,
  centres `t_j = 3j`, `j = 0..11`. The Gram matrix of the Weil form is
  `M_ij = W(phi_i * phi_j)`. Closed-form reduction (checked in-code): each entry is
  `w1*Wstd(c1) + w2*Wstd(c2)` with `c1 = (t_i+t_j)/2`, `w1 = exp(-(t_i-t_j)^2/8)`,
  `c2 = (t_i-t_j)/2`, `w2 = exp(-(t_i+t_j)^2/8)`, where `Wstd(c)` is exactly the
  WP3 engine's geometric side at centre `c` (width-1 even Gaussian pair). All
  needed centres lie on the grid `{1.5k : k = 0..22}` — 23 engine evaluations.
- Compact-support row (Part C): `f(u) = cos(pi*u/(2a))` on `|u| <= a`, `a = 0.34`,
  so `g = f * f~` is supported in `[-0.68, 0.68] ⊂ (-log 2, log 2)`: the prime term
  vanishes **identically** (no prime power has `log n < log 2`) and the geometric
  side is archimedean + pole only. `hC(r) = fhat(r)^2` with
  `fhat(r) = 4*pi*a*cos(a*r)/(pi^2 - 4*a^2*r^2)` (removable singularity at
  `r = pi/(2a)`, value `a`).
- Calibration universe (Part D): elliptic curve `E: y^2 = x^3 + x + 1` over
  `F_p`, `p = 10007` (discriminant nonzero mod p). Frobenius trace `a` from a full
  point count. Normalized power sums `c_m = s_m / p^(m/2)` with
  `s_0 = 2, s_1 = a, s_m = a*s_{m-1} - p*s_{m-2}`. Positivity object: the 8x8
  Toeplitz matrix `T_jk = c_{|j-k|}`, PSD iff the Frobenius spectral measure is a
  positive measure on the unit circle iff `|alpha| = sqrt(p)` (Hasse — a theorem
  in this universe). Negative control: fake data `(q, a) = (5, 5)`, which violates
  the Hasse bound (`a^2 = 25 > 20 = 4q`), i.e. "zeros off the critical line"; its
  growth ratio is `alpha/sqrt(q) = (1+sqrt(5))/2`, the golden ratio.

## Gates (PASS/FAIL, thresholds frozen)

- **A (instrument continuity).** The six WP3 pairing rows (centres 0, gamma_1,
  17.5, gamma_2, gamma_3, gamma_4) reproduce: `|zero side − geometric side| < 1e-9`
  at each.
- **B1 (Gram identity).** All 78 upper-triangle entries: `|M_geo − M_zero| < 1e-9`,
  where `M_geo` uses primes + archimedean + pole only (no zeros) and `M_zero` uses
  the first 60 zeros.
- **B2 (positivity).** `lambda_min(M_geo) > -1e-9`.
- **B3 (gap mechanism, directional).** Sorting eigenpairs ascending, the
  eigenvector centroids `sum_j |v_j|^2 * t_j` satisfy: bottom-3 centroids all < 9;
  top-1 centroid > 15.
- **C (prime-free window).** Structural: `2a = 0.68 < log 2`. Numerical:
  geometric side `W_C = arch + pole > 0`, and `|W_C − zero side (60 zeros)| < 1e-4`
  (the loose gate is the zero-side tail: `hC` decays only like `r^-4`; the
  instrument reports a tail estimate from the zero-density integral).
- **D1 (calibration, RH true).** Hasse holds for the computed `a` (sanity;
  theorem). Toeplitz `T`: two leading eigenvalues `> 1e-8`, all remaining
  `|lambda| < 1e-15`, and `lambda_min > -1e-15` (PSD of exact rank 2 — the
  spectral measure is two atoms).
- **D2 (calibration, negative control).** The Hasse-violating control's Toeplitz
  matrix has `lambda_min < -0.1` (the detector must fire where RH-analogue fails;
  already forced at the 2x2 minor since `c_1 = sqrt(5) > 2 = c_0`).

## Committed predictions (non-gating; discrepancies will be reported as such)

- P1. The spectrum of `M_geo` is an **exponential ladder climbing out of the
  zero-free gap** `(0, gamma_1 = 14.13...)`: diagonal estimates
  `M_jj ≈ 2*sum_gamma phi_j(gamma)^2` give rungs of order 1e-43 (t=0), 1e-26 (t=3),
  1e-15 (t=6), 1e-6 (t=9), 1e-1 (t=12), O(1) beyond — the bottom rungs sit below
  the numerical floor (~1e-20 at dps 30, quad-error-limited), so the smallest
  *resolved* eigenvalues will read as noise of magnitude ≲ 1e-20 of either sign
  (hence the B2 tolerance). The near-kernel of the Weil form on this family is
  spanned by profiles supported in the gap — the WP3 table's `t0 = 0` row
  (pole cancelled by archimedean + primes to 1e-23) *is* the leading near-kernel
  statement, now read as a positivity statement: **the functional's positivity
  margin is ~0 exactly on the zero-free gap.**
- P2. Eigenvalue rank correlates with eigenvector centroid throughout (small
  eigenvalue ↔ profile mass at small `|r|`).
- P3. Part C's value is dominated by the pole term `2*fhat(i/2)^2`, with the
  archimedean term a partial negative offset; predicted zero-side discrepancy
  ~1e-6..1e-4, consistent with the reported tail estimate.
- P4. Part D real-curve `lambda_3..lambda_8` read at the dps-40 numerical floor
  (~1e-35), an exact rank-2 statement: in a universe where RH is a theorem the
  positive structure is *tight* — the spectral measure has finite support, and
  positivity holds with zero margin in all but two directions. The contrast with
  Part B (infinite zero comb, strictly positive resolved spectrum, near-kernel
  only from the gap) is the finding to carry forward to WP-RH2.

## Exclusions and notes

- Thresholds above are frozen; instrument bring-up bugs (quadrature breakpoints,
  guards at removable singularities) may be fixed with an honest note in the
  script header, as with WP9b. Results are append-only.
- Prior-art note for the librarian stage: positivity of the Weil functional on
  restricted test classes is an active literature (Connes–Consani on Weil
  positivity; earlier numerics on Li coefficients). Part B's landscape on this
  particular family is, to our searches, untabulated; the gap near-kernel
  mechanism is presumably known in spirit to experts. Any candidate statement
  emerging from the ladder goes up the audit ladder before the word "candidate".
