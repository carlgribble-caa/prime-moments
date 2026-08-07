# Preregistration: the derivation bridge (WP-RH6)

Committed before first run. Instrument: `code/transfer_theory.py`. Lane: WP-RH.
This executes the "derive it" step of the transfer-law conjecture at the level
the data permits: prune the candidate mechanisms by controlled experiment, and
relocate the law onto the object it is actually about.

## The structural lemma, and what it forces (fixed before any run)

Least squares of a field on its own components *evaluated at the true sample
points* returns the full coefficients identically — displacement of the sample
points cannot attenuate a self-line (the field lies in the regressor span).
Therefore, IF the zeros' shift field were the full prime-line superposition
evaluated at the zeros, the RH4b/RH5 regressions would have returned ratio 1.
They returned 0.55–0.98. Forced conclusion, to be tested head-on here: **the
attenuation lives in S(t)'s own line content at finite height, not in
sampling.** And S(t) is exactly computable in continuous t between zeros
(S = N − N̄ with N a step function of the located zeros), so the line content
can be measured with no zero-sampling anywhere in the estimator.

If the continuous and zero-sampled measurements agree, the conjecture's object
simplifies: T(ω) is the height-local relative line amplitude of the
fluctuation field itself — and the cross-family universality of `a` (RH5b's
E1 refutation of the variance mechanism) points to pair-correlation (GUE)
universality as the mechanism, with the Goldston-type covariance lemma +
Montgomery's form factor as the formal derivation target (WP7 lane).

## Instrument constants (frozen)

- **Part A (negative control / lemma check).** Unfolded displaced lattice
  `x_k = xi_k + u(x_k)`, `xi_k = k − 1/2`, k = 1..400, fixed point by 60
  iterations. (A1) single line `u = 0.15 sin(1.3 x)`; regression of
  `x_k − xi_k` on `sin(1.3 x_k)` + nuisance {1, k̃, k̃²}. (A2) prime-like
  field `u = Σ_m 0.5 (A_m/π) sin((ln m/0.5) x)`, m over the battery
  {2,3,4,5,7,8,9,11,13}, `A_m = Λ(m)/(√m ln m)`; regression on all nine
  columns + nuisance.
- **Part B (continuous vs sampled, zeta).** Zeros 1..400 (dps 30). Windows
  W1 = [γ1, γ60], W2 = [γ141, γ200], W3 = [γ301, γ400]. Continuous field
  `S(t) = #{γ ≤ t} − Nbar(t)` on a grid of step 0.02; LSQ on
  {sin(t ln m)} + {1, t̃, t̃²}; ratios `T_cont(m) = slope/(−A_m/π)`.
  Sampled ratios recomputed in-code exactly as WP-RH4b/RH5.
- **Part C (continuous, second family).** The 150 beta zeros (finder as
  WP-RH5b, same constants); continuous `S_χ(t) = #{γ ≤ t} − θ(t)/π` on the
  full range, grid 0.02; same regression; comparison against the sampled
  RH5b ratios (signs must match χ; magnitudes compared).
- Recorded law constant a = 1.1416 throughout for reference curves.

## Gates (frozen)

- **G-A1.** Single-line self-recovery: ratio in [0.98, 1.02].
- **G-A2.** Prime-like synthetic: all nine ratios in [0.95, 1.05] — the
  displaced-lattice model shows NO attenuation, excluding sampling as the
  mechanism.
- **G-B1.** Continuous vs sampled agreement, zeta: |T_cont − T_sampled| < 0.10
  in all 12 gated cells (m ∈ {2,3,5,7} × three windows).
- **G-C1.** Continuous vs sampled agreement, beta: |T_cont − T_sampled| < 0.10
  for m ∈ {3, 5, 7} (magnitudes; signs must equal χ's).

## Committed predictions (non-gating)

- **P1.** The continuous ratios obey the recorded law: mean over the 12 zeta
  cells of |T_cont − exp(−1.1416 τ²)| < 0.06.
- **P2.** Per-window fitted `a` from the continuous gated points lands in
  [0.9, 1.5] for all three zeta windows and for beta (universality clause).
- **P3.** For beta, the universal a = 1.1416 fits the continuous points better
  (SSE) than the local-variance variant a₃ = 2π²⟨S_χ²⟩ — replicating RH5b's
  E1 refutation in continuous form.

## Exclusions and notes

- Thresholds frozen; results append-only; bring-up fixes with honest notes.
- If G-B1/G-C1 PASS, the conjecture is restated (v2) in the results: T is the
  height-local line content of S itself; `a` universal across families;
  variance mechanism retired; pair-correlation derivation flagged as the
  formal target. If they FAIL, the discrepancy localizes the mechanism into
  the sampling after all, and the v2 restatement is withheld.
- Librarian: the covariance objects here are classical (Landau; Goldston's
  lemmas on S(t); Montgomery's F). The measured continuous/sampled agreement
  table and the synthetic exclusion are the deliverables.
