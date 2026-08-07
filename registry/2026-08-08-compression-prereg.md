# Preregistration: the compression question, first light (WP-C1)

Committed before first run. Instrument: `code/compression_question.py`. Lane:
WP-C (opened with this prereg). Sibling of the positivity lane: same object,
information-theoretic face.

## The question, formalized

"Is there a closed form for π(x)?" is formalized as evaluation complexity: a
fixed-length exact expression is (up to convention) a poly(log x)-time exact
algorithm. The lane assembles what is known into a spec matrix with exactly
one OPEN cell — **exact π(x) in poly(log x)** (the parity of π(x) in poly(log
x) is recorded inside the same cell as the weakest unsolved form) — and adds
two measurements:

- **The parity stream.** Parity bits of π(x) at geometrically spaced points
  (enough primes between consecutive points that parity is coin-like) should
  carry no structure a practical compressor can find. This is the "closed
  form" question's cheapest falsifiable shadow: any detected structure would
  be a compression of the fluctuations.
- **The skeleton at the compressor level.** The prime indicator over a window
  is compressible exactly through its congruence skeleton (wheel structure);
  restricted to wheel-coprime positions it should compress no better than a
  density-matched control. This is the two-skeleton conjecture (WP6) read
  through general-purpose compressors as the observer class.

## Instrument constants (frozen)

- Sieve to N = 10^7 (numpy). Parity stream: points `x_i = round(10^6 ·
  10^{i/8191})`, i = 0..8191 (8192 bits; ≥ ~20 primes between consecutive
  points at the low end); bits = π(x_i) mod 2, packed, compressed with zlib
  level 9; control = 8192 Bernoulli(1/2) bits from 6-digit blocks of π's
  decimal digits (threshold 500000).
- Window for the skeleton test: [10^7 − 2^20, 10^7); indicator bits over all
  positions; compressors: best (smallest) of zlib-9, bz2-9, lzma; raw-density
  reference `H2(ρ)` with ρ the window's prime density; wheel = mod 30,
  coprime residues {1,7,11,13,17,19,23,29}; restricted indicator over
  coprime positions only, with control = Bernoulli(ρ30) bits at the measured
  coprime-position density ρ30, generated deterministically by SHA-256 in
  counter mode with seed string "WP-C1" (bulk size makes π-digit generation
  impractical; the generator is committed here).
- Local-primality demo: deterministic Miller–Rabin with bases
  {2,3,5,7,11,13,17,19,23,29,31,37} (valid far beyond 10^7) on the 200
  integers 9,999,600..9,999,799, compared bit-for-bit with the sieve.

## Gates (frozen)

- **K1 (spec completeness).** The printed matrix has exactly one OPEN cell:
  exact π(x) in poly(log x).
- **K2 (parity incompressibility).** compressed_size(parity bits) ≥ 0.97 ×
  compressed_size(π-digit coin control), zlib-9 both.
- **K3 (compressor finds the skeleton).** Best-compressor bits-per-position
  on the raw window ≤ 0.92 × H2(ρ): the compressor must beat the
  structure-blind bound (the gap to the wheel entropy (8/30)·H2(ρ30) is
  reported, not gated).
- **K4 (nothing beyond the skeleton).** compressed_size(wheel-restricted
  indicator) ≥ 0.97 × compressed_size(density-matched SHA control).
- **K5 (local vs global).** Miller–Rabin agrees with the sieve on all 200
  committed integers — local primality is poly(log) (ADOPTED: AKS;
  demonstrated here), which sharpens the OPEN cell: counting is global.

## Committed predictions (non-gating)

- **L1.** K2 ratio in [0.99, 1.03] — the parity stream is fully coin-like to
  zlib.
- **L2.** K4 ratio in [0.99, 1.03] — the two-skeleton conjecture holds at the
  compressor observer class.
- **L3.** The best compressor lands within [1.0, 1.6] × the wheel entropy on
  the raw window (reported; how much of the skeleton practical compressors
  actually capture is itself a measurement).

## Exclusions and notes

- Compressors are proxies for entropy, not estimators of Kolmogorov
  complexity; every claim is "at the practical-compressor level," and the
  spec matrix says so.
- Thresholds frozen; results append-only; bring-up fixes with honest notes.
- Librarian, upfront: the complexity rows are classical (analytic method
  ~x^{1/2+ε}; combinatorial x^{2/3}; AKS; Lagarias–Odlyzko); the bit-floor
  row is the programme's own Lean-checked theorem (WP7.H2); prime-bitmap
  compressibility via wheels is folklore. The parity-stream and
  skeleton-at-compressor tables appear untabulated; no novelty is claimed
  beyond the measured tables and the assembled matrix.
