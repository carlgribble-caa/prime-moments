# Results: the derivation bridge (WP-RH6)

Prereg: `2026-08-07-transfer-theory-prereg.md`, committed at `8016883` before
first run. Instrument: `code/transfer_theory.py` (230 s). Results are
append-only. **The committed bridge gates were REFUTED, the prereg's own
contingency clause applies, and the refutation localizes the mechanism — this
is the lane's most informative negative result.**

## Bring-up (one inconsistent prereg spec, RH2-Abel precedent)

Part A2's committed amplitude scale (0.5) made the displacement field
non-contractive (Σ α·ν ≈ 1.6); the first run's fixed-point iteration never
converged (residual 0.33) and its marginal gate failure (ratios 0.961–1.074)
was an artifact. Corrected scale 0.15 (Σ ≈ 0.47) with a loud convergence
assert; thresholds unchanged. First-run table preserved here for the record.

## Gates and predictions (corrected run)

- **G-A1 (single-line lemma): PASS** — self-recovery ratio 1.0000.
- **G-A2 (nine-line prime-like field): PASS** — all nine ratios exactly 1.000:
  **sampling displacement cannot attenuate in-span lines; machine-checked.**
- **G-B1 (continuous = sampled, zeta): REFUTED** — max cell difference 0.435.
  The continuous line content of S(t) is **full**: 0.974–1.006 in all 12
  cells (mean 0.994), while the zero-sampled ratios attenuate as measured in
  RH4b/RH5 (0.554–0.984, reproduced in-code).
- **G-C1 (continuous = sampled, beta): REFUTED** — same pattern: continuous
  −1.006/+1.008/−0.988 at m = 3/5/7 (full, χ-signed) vs sampled
  −0.905/+0.823/−0.738.
- **P1: REFUTED** (continuous does not obey the DW law — it needs none).
- **P2: REFUTED**, decisively — fitted `a` on the continuous points is
  0.002–0.094 ≈ 0: *no attenuation exists in continuous time.*
- **P3: CONFIRMED** (universal a beats local-variance on the sampled side's
  comparison, as before).

## The localization (what the refutation established)

Three facts now stand, each machine-checked under prereg:

1. In-span sampling cannot attenuate (A1/A2, exact).
2. The counting fluctuation S(t) carries every prime line at **full
   explicit-formula amplitude at every height tested, in both families**
   (15/15 continuous cells at 0.99 ± 0.02) — consistent with the classical
   Landau/Goldston asymptotics.
3. The Debye–Waller attenuation exists **only in the zero-sampled displacement
   sequence** u_k — the values of the fluctuation field read at its own jump
   points.

## Conjecture, localized restatement (supersedes the v2 draft the prereg
withheld)

**CONJECTURE (transfer law, localized).** The prime lines enter the counting
function S(t) at full amplitude at all heights. The per-frequency content of
the *zero-position displacement sequence* is attenuated by
`T = exp(−a (ω/2πρ̄)²)` with `a ≈ 1.14` universal across heights and families
— the Debye–Waller price of reading the primes from the zeros' positions
rather than from counts. Since the canonical-system reconstruction (the
Hamiltonian data of WP-RH2 onward) consumes exactly the zero positions, this
law remains the correct fingerprint for the spec's OPEN cell. **Derivation
target, now precise:** the discrete-vs-continuous weight for sampling a
counting sawtooth at its own jump points — a pair-correlation object
(Montgomery–Goldston), whose conjectured GUE universality explains the
family-independence of `a` that refuted the variance mechanism (RH5b E1,
RH6 P3). Falsification protocol unchanged plus: derive the jump-point
sampling weight under GUE and match a = 1.14; any failure of universality at
further families or heights.

## Status

"Refine": done — the law is localized onto its true object, the universal-a
clause replaces the retired variance clause, and the overtone anomalies stay
flagged (RH7 candidate). "Derive": bridged — the mechanism is localized by
machine-checked exclusion, the continuous side is fully explained by
classical results, and the remaining unexplained object (the jump-point
sampling weight) is precisely specified for the formal lane (WP7). A full
derivation was not reached and is not claimed. Note 4 revision folding
RH6 in: queued.
