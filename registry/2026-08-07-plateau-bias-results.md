# Results: the plateau bias is a density effect (WP-RH3c)

Prereg: `2026-08-07-plateau-bias-prereg.md`, committed at `abb3d39` before first
run. Instrument: `code/plateau_bias.py` (5 s). Results are append-only.

## Gates and predictions

| N | parity | bias(zeros) | bias(smooth) | difference | |
|---|---|---|---|---|---|
| 50 | odd | −1.067 | −0.988 | 0.079 | |
| 50 | even | −1.751 | −1.774 | 0.024 | |
| 60 | odd | −1.429 | −1.208 | 0.221 | |
| 60 | even | −2.788 | −2.672 | 0.117 | |

- **V1** (all four |bias(zeros) − bias(smooth)| < 1.0): PASS — max difference
  0.221, an order inside the gate.
- **V2** (smooth bias negative in all four): PASS.
- **W1** (< 0.5 in ≥ 3 of 4): CONFIRMED — all four, max 0.221, well inside the
  rigidity-scale expectation ~0.5.
- **W2** (even-bias growth with N matches between combs): CONFIRMED.

## Claim, earned

**The plateau bias is arithmetic-free.** The smooth comb — identical mean
density, no primes — reproduces the deviation from the two-interval equilibrium
cell by cell to ~0.1. Combined with RH3b, the ledger for the canonical-system
data now reads: the gap location, the window, the universal plateau, *and* the
deviation from it are all density-driven; the arithmetic content is confined to
the rigidity-scale residual fluctuations (WP-RH2: per-coefficient std ≈ 2.2,
four times tighter than Poisson). Spec row 6's negative constraint in its
strongest measured form: **every leading structure of the reconstructed
Hamiltonian is smooth-derivable; only the corrections know the primes.**

## Carried forward

The natural next target in this thread is the corrections themselves: the
residual sequence a_n(zeros) − a_n(smooth) on the plateau, whose variance RH2
measured (rigidity 0.246 vs Poisson) but whose *spectral content* is unmeasured
— the analogue, one level down, of RH2's B5 (which found the primes in the
eigenvalue residual). A future prereg would commit a target for the Fourier
content of the coefficient residual against the prime frequencies log p. Nothing
is claimed here.

## Note

Same-session context: Programme Note 4 (`papers/positivity_lane.tex`) was
compile-verified before this run (pdflatex ×2 clean, cite cross-check 33/33);
this result belongs to a future revision of that note, not the current draft.
