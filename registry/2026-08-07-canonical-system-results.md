# Results: canonical-system reconstruction, first light (WP-RH2)

Prereg: `2026-08-07-canonical-system-prereg.md`, committed at `72d1494` before
first run. Instrument: `code/canonical_system.py` (55 s final; mpmath dps 40 for
Parts A/C, float64 for Part B). Results are append-only; first-run failures and
instrument fixes are reported below in full.

## Instrument bring-up (two bugs, found by the gates, fixed with thresholds unchanged)

Run 1 failed gates B3 (49 eigenvalues counted vs 60 ± 2) and B4 (RMS 21.7 vs
< 1.0), with a *constant* delta ~ -21.9 across k. Diagnosis, in order:

1. **Abel normalization.** The preregistered inversion formula (closed form with
   divisor pi², matching its own preregistered integral definition, so B1
   passed) carried a spurious 1/pi: the correct pair is
   `x(V) = INT Nbar'(E)/sqrt(V-E) dE` with **no** prefactor, pinned by the
   harmonic-oscillator case (x = sqrt(V) <-> Phi = E/2). Correct closed form:
   divisor pi. A defining-property diagnostic (WKB phase on the built grid vs
   `Nbar + 1/8`) now guards the construction; final run: agreement to ~5e-5 at
   E = 50 and E = 150.
2. **Silent bracket saturation.** The eigenvalue search widened its bracket at
   most 10 times and then silently returned the cap — the constant -21.9 *was
   the cap*, not physics (identical E_k across runs with different potentials
   exposed it). The solver now raises on an unbracketed eigenvalue.

Instructive footnote, recorded because it is honest and diagnostic: run 1's
headline gate B5 already read r = 0.605, because gamma_k minus the cap formula
is dominated by the zeros' own fluctuations — the prime correlation reached the
gate without the solver's help. The fixed instrument measures the same
correlation through the actual spectrum, and it sharpens dramatically (below).

## Gates (final run)

| Gate | Committed criterion | Measured | Verdict |
|---|---|---|---|
| A1 (symmetry) | max \|b_n\| < 1e-20, three combs | 9.4e-37 | PASS |
| A2 (reconstruction) | eig(J_80) vs atoms < 1e-8 | 1.3e-38 | PASS |
| B1 (closed form) | vs quadrature < 1e-8 rel | 1.0e-22 | PASS |
| B2 (solver validation) | harmonic well < 1e-6 | 3.7e-9 | PASS |
| B3 (counting) | 60 ± 2 below (γ60+γ61)/2 | exactly 60 | PASS |
| B4 (tracking) | RMS(δ_k) < 1.0 | 0.537 | PASS |
| B5 (headline) | Pearson r > 0.4 | **r = 0.9999** | PASS |
| C1 (termination) | step 2, all < 1e-30 | residual 0; 4.6e-41; 1.5e-38 | PASS |

## Committed predictions, outcomes

- **Q1: REFUTED — from above.** Committed band r in [0.6, 0.95]; measured
  0.9999. The under-prediction is itself the finding: at these heights the
  damped prime sum S captures the reconstructed spectrum's residual *almost
  completely* — delta_k · rho(gamma_k) ~ 1/8 - S(gamma_k) is numerically an
  identity at the few-percent level, not a mere correlation. The smooth
  (arithmetic-free) Hamiltonian misses exactly the prime comb and essentially
  nothing else. No circularity: E_k consumes only Nbar (no primes, no zeros);
  S consumes only primes; gamma_k only the zeros.
- **Q2: CONFIRMED.** Rigidity in Hamiltonian coordinates: std ratio
  zeros/Poisson = **0.246** (< 0.7 committed) over n = 6..70 — the zeros'
  Jacobi coefficients hug the smooth comb's four times tighter than a
  density-matched Poisson comb's. Spectral rigidity, read in the
  reconstruction's coefficients.
- **Q3: CONFIRMED, sharply.** Maslov offset mean(delta*rho + S) = **+0.1251**
  against the predicted 1/8 = 0.125 from the V0 = 2pi convention.
- **Q4: CONFIRMED.** The Frobenius measure's reconstruction terminates at step
  2 with residual 0 (J_2 eigenvalues ±theta to 4.6e-41): in the universe where
  the RH-analogue is a theorem the canonical system is a **finite exact
  matrix**, while for zeta the reconstruction is infinite and its truncation's
  missing content is, by B5, the primes.

## Audit-ladder note

The B5/Q1 near-identity is the Riemann-von Mangoldt + WKB mechanism made
quantitative on a concrete operator: classification **known-theorem-derivable**
(the WS construction and the physics-of-zeta literature own the setup; we claim
the measured tables, the controls, and the discipline, not the mechanism). The
Q2 rigidity table on Jacobi coefficients of the zero comb vs pi-digit Poisson
controls is, to our searches, untabulated — it stays at stage "measured table",
below "candidate", pending a proper librarian pass against the random-Jacobi
literature (Killip-Nenciu school).

## Carried forward (WP-RH3 requirements spec, first two lines)

1. Any candidate Hilbert-Polya structure must reproduce the prime comb at
   fluctuation order in its Hamiltonian data — a smooth/arithmetic-free
   Hamiltonian accounts for the mean density and *nothing else* (B5: the
   residual is the primes, r = 0.9999).
2. In solved universes the canonical system is finite and exact with zero
   positivity margin to spare (C1 here; D1 in WP-RH1): tightness + arithmetic
   fluctuation content are the two measured properties the missing object must
   reconcile.
