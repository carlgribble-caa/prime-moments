# Results: Weil positivity explorer, first light (WP-RH1)

Prereg: `2026-08-07-weil-positivity-prereg.md`, committed at `8252b9a` before first
run. Instrument: `code/weil_positivity.py` (34 s, mpmath dps 30). Results are
append-only; the discrepancy below is reported as a discrepancy.

## Gates

| Gate | Committed criterion | Measured | Verdict |
|---|---|---|---|
| A (continuity) | six WP3 rows, diff < 1e-9 | max diff 1.3e-23 | PASS |
| B1 (Gram identity) | 78 entries, geo vs zero < 1e-9 | max diff 2.6e-23 | PASS |
| B2 (positivity) | lambda_min > -1e-9 | lambda_min = -8.5e-24 | PASS |
| B3 (gap mechanism) | bottom-3 centroids < 9; top > 15 | centroids 13.56, 16.59, 9.27; top 31.75 | **REFUTED** |
| C (prime-free window) | W > 0, diff < 1e-4 | W = 9.10e-4 > 0; diff 4.2e-6 | PASS |
| D1 (EC, RH true) | PSD rank 2 | a = -57; spectrum {8.8, 7.2, ±1e-40...} | PASS |
| D2 (EC control) | lambda_min < -0.1 | lambda_min = -38.96 | PASS |

## The refutation, and what the data showed instead

B3 predicted the near-kernel of the Weil form on the family would be spanned by
gap-localized profiles (mass below gamma_1 = 14.13). Partially right, mostly
wrong. Right: the diagonal ladder out of the gap is exactly as committed in P1 —
M_tt rungs measured at ~3e-43 (t=0), 2e-27 (t=3), 9e-15 (t=6), 4e-6 (t=9),
0.2 (t=12) — and the gap profiles do sit in the near-kernel (eigenpairs k=3,4,5,
centroids 5.48, 3.07, 0.45). Wrong: they do not span it. The bottom eigenpairs
k=0,1,2 have centroids 13.56, 16.59, 9.27 — large-centroid *interpolation
combinations* of overlapping profiles that cancel at the engaged zeros.

The measured mechanism: **resolved rank of M = 6 = number of zeros engaged by
the family** (2 max_j phi_j(gamma)^2 > 1e-12 selects gamma_1..gamma_6; the
eigenvalue count above 1e-12 is also 6, with the soft edge lambda_6 = 1.8e-9
carried by the weakly-engaged gamma_6 = 37.58). On a finite spectral window the
Weil form is a finite-rank sampler: rank = #zeros engaged, kernel = every test
combination vanishing at those ordinates.

Audit-ladder classification of this finding: **known-theorem-derivable** (given
the explicit formula, M is the Gram matrix of point evaluations at the zeros, so
the rank statement follows; we do not claim novelty). Its value here is
calibration, and it sharpens the lane's framing: positivity on any finite family
is rank-deficient-cheap — the form barely has to try — which is a *measured*
restatement of why the Weil criterion quantifies over all test functions, and of
where the difficulty of RH actually lives (the margin, not the sign, cf. the
Rodgers–Tao Lambda >= 0 "barely true" reading).

## Committed predictions, outcomes

- P1 (ladder): CONFIRMED for the diagonal (rungs as committed, spanning ~43
  orders); the near-kernel claim folded into the B3 refutation above.
- P2 (rank-centroid correlation): REFUTED as stated (the interpolation
  combinations break monotonicity below the noise floor); holds for the resolved
  block k=6..11 only in the weak sense that the top block lives at large t.
- P3 (prime-free window): CONFIRMED — value dominated by the pole term
  (0.37686) against the archimedean offset (-0.37595), leaving 9.1e-4; zero-side
  discrepancy 4.2e-6 against tail estimate 3.8e-6.
- P4 (EC tightness): CONFIRMED — rank exactly 2 at the dps-40 floor (~1e-40);
  in the universe where the RH-analogue is a theorem, positivity holds with zero
  margin in all but two directions. Negative control fired at -38.96 with the
  committed golden-ratio growth signature (c_1 = sqrt(5), ratio phi).

## Carried forward (WP-RH2)

The landscape's lesson: finite families cannot distinguish "RH-positive" from
"barely positive" — the information is in the margin structure as the spectral
window grows, and in the object that *enforces* the margin. WP-RH2 (canonical
system / inverse spectral reconstruction of the Hamiltonian from the zeros, with
the EC and Selberg universes as solved calibrations) targets that object
directly. Exit-code note, honest: the script's exit code tracks the instrument
gates (A, B1, B2, C, D1, D2, and the rank-match diagnostic); B3's refutation is
recorded here permanently and printed as REFUTED on every run — a threshold was
not edited to make a red light green.
