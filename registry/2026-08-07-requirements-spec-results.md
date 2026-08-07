# Results: the requirements spec (WP-RH3)

Prereg: `2026-08-07-requirements-spec-prereg.md`, committed at `8675814` before
first run. Instrument: `code/requirements_spec.py` (9 s, mpmath dps 30; Stieltjes
at dps 40). Results are append-only.

## Gates

| Gate | Committed criterion | Measured | Verdict |
|---|---|---|---|
| G1 (mean density, zeta) | max dev < 1.0 over 100 zeros | 0.4979 | PASS |
| G2 (rigidity ordering, zeta) | var(zeros) < var(Poisson) | 0.1253 < 1.0755 | PASS |
| G3 (spectrum↔geodesics, graph) | tr(B^m) vs Ihara–Bass < 1e-18, m ≤ 12 | 6.3e-29 | PASS |
| G4 (smooth split, graph) | 0 below girth; excess_5 = 120 | [0,0,0,0,120] | PASS |
| G5 (EC trace formula, p = 13) | N_2 direct = p²+1−(a²−2p) | 180 = 180 (a = −4) | PASS |
| G6 (spec completeness) | exactly one OPEN cell, (row 1, zeta) | as committed | PASS |

## Committed predictions, outcomes

- **P1: CONFIRMED.** Unfolded spacing variance of the first 100 zeros = 0.1253,
  inside [0.12, 0.25] (GUE ≈ 0.18; just above the band floor); π-digit Poisson
  control 1.0755, inside [0.5, 1.6]; picket 0 by construction. Rigidity ordering
  picket < zeros < Poisson as the spec's row 7 requires.
- **P2: CONFIRMED.** max |Nbar(γ_k) − (k − 1/2)| = 0.4979 ∈ [0.3, 0.8].
- **P3: REFUTED — by window choice, and the refutation is instructive.** The
  committed tail window (n = 41..70 of 79 coefficients) gave odd mean 68.120
  (within 0.42 of the two-interval equilibrium 68.541) but even mean 38.042 vs
  54.406: that window sits in the *truncation-decay regime* of the finite
  80-atom measure, where coefficients are dominated by finite-N effects and no
  limit at all. Post-hoc diagnostic (recorded as post-hoc, NOT a claim): on the
  earlier plateau n = 11..40 the parity means are 67.412 / 53.028 — both within
  1.4 of the two-interval equilibrium (68.541 / 54.406). The structure
  identification therefore *appears* correct on the plateau but stays unclaimed
  under the registry discipline; a follow-up prereg would be required to claim
  it. Net effect on the spec: the "tail forgets arithmetic" constraint is
  *strengthened* — the truncated reconstruction's late coefficients carry
  neither arithmetic nor even the universal limit, only truncation.

## The deliverable: the spec matrix

Printed in full by the instrument (8 property rows × 3 universe columns, every
cell ADOPTED/MACHINE/MEASURED/OPEN). Status: **35 of 36 half-cells resolved;
exactly one OPEN cell — (row 1: self-adjoint realization exists, column:
zeta).** The zeta column as measured/checked: real spectrum (as tested),
functional equation (adopted), trace formula at 1e-23 (WP3/RH1), RvM mean
density (G1), prime-comb fluctuation content (RH2 B5, r = 0.9999), GUE-adjacent
rigidity (G2/P1), finite-window tightness (RH1). New machine checks this run:
G1, G2, G3, G4, G5.

Two constraint lines the matrix pins on the OPEN cell's occupant:

1. It cannot be smooth: an arithmetic-free Hamiltonian reproduces the mean
   density and nothing else (RH2 B5); the prime comb must appear at
   fluctuation order in its Hamiltonian data.
2. It must be tight: every solved-universe realization is finite/exact with
   zero positivity margin to spare (RH1 D1, RH2 C1), while zeta's margin as
   measured is ~0 on every finite window (RH1 B) — consistent with the
   Rodgers–Tao "barely true" reading.

## Audit-ladder note

Every row of the matrix is individually classical (Hasse; Ihara–Bass;
Kesten–McKay/Serre; RvM; Montgomery–Odlyzko; Alon–Boppana/LPS); the assembled
machine-checked matrix with its named OPEN cell is a scope statement, not a
novelty claim. The G4 identity (first spectral excess = 120 = the Petersen
pentagon count traversed) is the graph-universe miniature of RH2's headline:
the first correction to the smooth spectral law counts the shortest geodesics.

## Lane status after RH1–RH3

The WP-RH lane's first-light phase is complete: the positivity landscape
(RH1), the reconstruction and its prime-comb residual (RH2), and the
requirements spec with one named OPEN cell (RH3), all under prereg, all in
run_all, with every refuted prediction recorded. Honest pricing unchanged:
instruments and calibrations delivered; novel labeled conjectures possible
from here; partial theorems the realistic summit; RH itself priced at epsilon
throughout.
