# Preregistration: the requirements spec (WP-RH3)

Committed before first run. Instrument: `code/requirements_spec.py`. Lane: WP-RH.
Goal: the minimal machine-checked property list that the sought positive
structure ("the Hilbert–Polya object for zeta") must satisfy, extracted from the
universes where the RH-analogue is a theorem and measured for zeta where it is
not. Deliverable: the spec matrix — one row per property, columns EC/Frobenius,
graph/Ihara, zeta — every cell labeled ADOPTED(citation) / MACHINE(check id) /
MEASURED(run id) / OPEN. The lane's standing rule holds: "proof of RH" appears
nowhere; exactly one cell is expected OPEN, and naming it precisely is the point.

## Mining redirect (recorded honestly, before the run)

WP-RH2's summary proposed constant-mining (PSLQ) the Jacobi-coefficient limits
of the reconstructed Hamiltonian. Analysis before this prereg dissolved that
target: for the symmetric measure on `{±γ_1..±γ_N}` the recurrence coefficients
approach the *universal two-interval equilibrium* of the support
`[−γ_N, −γ_1] ∪ [γ_1, γ_N]` — parity-alternating limits `(γ_N ± γ_1)/2` — i.e.
the tail is set by the truncation window and the spectral gap, not by
arithmetic. PSLQ on those limits would mine `γ_1` and `γ_N` back out — circular.
The miner is therefore redirected to a structure-identification prediction (P3
below), and the dissolution itself becomes spec row 6's sharpening: **the
Hamiltonian tail forgets arithmetic; the prime content must live in the decaying
corrections.** PSLQ is deferred until the lane owns a truncation-free constant.

## Instrument constants (frozen)

- Zeta column: first `100` zeros (mpmath `zetazero`, dps 30);
  `Nbar(E) = (E/2π)(ln(E/2π) − 1) + 7/8`; unfolded spacings
  `s_k = Nbar(γ_{k+1}) − Nbar(γ_k)`, `k = 1..99`; population variance (ddof 0).
  Poisson control: 99 gaps `−ln u_k`, `u_k` = consecutive 6-digit blocks of π's
  decimal digits (as WP-RH2). Picket control: the smooth comb (spacings exactly
  1; variance 0 by construction, reported).
- Graph column: the Petersen graph (3-regular, n = 10, E = 15, girth 5;
  adjacency spectrum {3, 1×5, −2×4}, verified in-code). Hashimoto matrix B on
  30 directed edges, integer powers. Ihara–Bass spectral side:
  `tr(B^m) = (E−n)(1 + (−1)^m) + Σ_j (μ+^m + μ−^m)`,
  `μ± = (λ_j ± sqrt(λ_j² − 8))/2`. Tree return counts `t_m` by exact DP on
  distance-from-root (k = 3: k branches from the root, k−1 forward / 1 back
  elsewhere).
- EC column: fresh small-field trace-formula check at `p = 13`,
  `E: y² = x³ + x + 1` (discriminant nonzero mod 13): trace `a` from the F_13
  count; `N_2` counted directly over `F_169` built as `F_13(sqrt 2)` (2 a
  nonresidue mod 13); Euler test `z^84 = 1` for squareness. Large-p rows cite
  WP-RH1 D1 / WP-RH2 C1.
- Part D: Stieltjes (dps 40) on the first 40 zeros exactly as WP-RH2 Part A;
  tail windows `n = 41..70` split by parity; two-interval equilibrium values
  `(γ_40 + γ_1)/2` and `(γ_40 − γ_1)/2`.

## Gates (PASS/FAIL, thresholds frozen)

- **G1 (mean density law, zeta).** `max_{k≤100} |Nbar(γ_k) − (k − 1/2)| < 1.0`.
- **G2 (rigidity ordering, zeta).** `var(s, zeros) < var(s, Poisson)`.
- **G3 (spectrum ↔ geodesics, graph).** Petersen, `m = 1..12`: integer
  `tr(B^m)` equals the Ihara–Bass spectral side to `< 1e-18`.
- **G4 (smooth split, graph).** `tr(A^m) = 10·t_m` exactly for `m = 1..4`
  (girth 5: the tree accounts for everything below the shortest geodesic), and
  the first excess `tr(A^5) − 10·t_5 = 120` (= 12 pentagons × 5 base points ×
  2 orientations): the first correction to the smooth spectral law counts the
  shortest geodesics.
- **G5 (trace formula, EC, fresh code).** `N_2 = p² + 1 − (a² − 2p)` at p = 13,
  both sides by direct count.
- **G6 (spec completeness).** Every cell of the printed matrix carries exactly
  one label from {ADOPTED, MACHINE, MEASURED, OPEN}; the only OPEN cell is
  (row: self-adjoint realization, column: zeta).

## Committed predictions (non-gating; discrepancies reported as such)

- **P1 (GUE adjacency).** `var(s, zeros) ∈ [0.12, 0.25]` (GUE spacing variance
  ≈ 0.18); `var(s, Poisson) ∈ [0.5, 1.6]` (exponential: 1).
- **P2 (S bound).** `max_{k≤100} |Nbar(γ_k) − (k − 1/2)| ∈ [0.3, 0.8]`.
- **P3 (Hamiltonian tail is the universal gap limit).** Parity means of the
  Jacobi tail (n = 41..70) land within ±4 of the two-interval equilibrium
  `((γ_40 + γ_1)/2, (γ_40 − γ_1)/2) ≈ (68.5, 54.4)` — arithmetic-free
  universality of the tail; the arithmetic lives in the corrections (spec row 6).

## Exclusions and notes

- Bring-up bugs fixable with an honest header note (WP9b/RH2 precedent);
  thresholds frozen; results append-only.
- Librarian: the spec rows are individually classical (Hasse; Ihara–Bass; the
  Serre/McKay tree-vs-geodesic split; RvM; Montgomery/Odlyzko for GUE
  adjacency; Alon–Boppana/LPS for graph tightness). What this WP claims is the
  assembled, machine-checked matrix and the naming of the single OPEN cell —
  a scope statement, not a novelty claim. Any candidate emerging later must
  clear the full audit ladder.
