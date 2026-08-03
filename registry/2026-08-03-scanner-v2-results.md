# Results: skeleton-null scanner v2 (WP6)

Prereg: `2026-08-03-scanner-v2-prereg.md`, commit `930a091` (not edited since).
Full deterministic output: `2026-08-03-scanner-v2-output.txt` (seeds fixed in the script).

## Instrument revision v2.0 → v2.1 (before any prediction was scored)

First light of v2.0 caught the instrument in two errors, reported per protocol:

1. **Over-stratification bug.** The mod-60 strata determine p mod 4 and p mod 3, so the
   congruence features standardized to zero everywhere — nulling exactly the positive
   controls (P1, P2) the prereg predicted would fire. Fix (v2.1): two-tier
   standardization — congruence features standardize within size bands only; consecutive
   nulls permute whole rows within size bands.
2. **Checker misalignment.** The P4 checker enforced a stricter automatic-class carve-out
   than the prereg's text ("mechanical size-budget entanglements of bits" were counted as
   violations). Fix: checker aligned to the prereg wording.

v2.0 also produced one instructive reading: rs × rs (consecutive) at z = −12.8,
replicated. Diagnosis: consecutive primes share binary prefixes, so the Rudin–Shapiro
sequence's own shift-autocorrelation — an integer phenomenon — leaks through prime gaps.
v2.1's control population settled it exactly as diagnosed (reproduced off the primes).

v2.1 also adds the **control population** m = p + 30: identical mod-60 classes, sizes,
and gap chain; overwhelmingly composite. Survivors reproduced by the control with the
same sign are classified *not prime-specific*. Pratt height is undefined off the primes
and excluded from control comparison.

## v2.1 outcomes against the committed predictions

| prediction | outcome |
|---|---|
| P1 chi4×chi4 consecutive fires, z<0 | **PASS**, z = −37.8 (control −38.5) |
| P2 chi3×chi3 consecutive fires, z≤−8 | **PASS**, z = −41.3 (control −41.5) — new positive control |
| P3 gap×gap consecutive fires, z<0 | **PASS**, z = −10.8 |
| P4 theorem-null (automatic class clean of prime-specific survivors) | **PASS**, 0 violations |
| P5 v1 same-prime chi cluster absorbed by finer null | **PASS** |
| P6 mechanical same-prime crystal cluster fires, classifies mechanical | **PASS** (control-reproduced) |
| P7 candidates after audit: zero | **PASS** (zero confirmed; three readings remain in audit, below) |

Note on P1/P2 controls: the control *reproduces* the repulsion, as it must — m = p + 30
inherits the primes' residue chain, and the repulsion lives in the skeleton +
Hardy–Littlewood layer the control copies. The control separates prime-specific
structure from skeleton-borne structure; it does not erase the skeleton.

## Audit summary (57 survivors)

- **43 control-reproduced** — integer smoothness autocorrelations at small shifts,
  size-budget entanglements, and the skeleton-borne controls. Not prime-specific.
- **11 Pratt-height entanglements** — control-blind (Pratt needs primality). Same-prime
  members are definitional (Pratt height is built from the factorization of p−1);
  consecutive members plausibly inherit the control-reproduced smoothness
  autocorrelations through that entanglement. Classified mechanical/derived.
- **3 in audit** — gap/log p × {om(p−1), Om(p−1), slope} (consecutive), |z| = 5.0–5.4,
  replicated, control disagrees (gap-of-primes is a prime-only observable). Retained for
  next-scale replication; **not promoted to candidate**. Plausible home:
  Hardy–Littlewood gap–smoothness interaction (skeleton layer); to be tested at 10^7.

## Verdict

Second first light: clean under the committed predictions, two instrument bugs found and
documented, zero confirmed candidates. The two-skeleton conjecture survives its second
audit, now with its ladder attached (Programme Note 3).
