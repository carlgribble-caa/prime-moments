/-
WP7.H1 — Companion III, Theorem 1 (prime-free individual recovery), kernel-checked core.
Paper: C. Gribble, "Recovering the primes in a dyadic interval from exact moments",
doi:10.5281/zenodo.21769107, Theorem 1.

Paper statement: with r = |P(W)| and s_1, ..., s_r the power sums of the window primes,
Newton's recursion produces integers e_k which are the elementary symmetric functions of
P(W); the monic polynomial f(x) = Σ (-1)^k e_k x^(r-k) equals Π (x - p); and the integer
roots of f in the window are exactly the window primes.

Formalization shape: `S : Finset ℤ` is any finite set of distinct integers — the theorem
is uniform over configurations, exactly as the paper's obstruction model (Definition 1
there) requires: the decoder uses no property of primes. Here

  * `e_k` is realized as `S.val.esymm k` (an integer by construction — the paper's
    integrality claim is absorbed into the definition);
  * `newton_recursion` certifies that these integers satisfy the recursion the paper's
    decoder runs (in the division-cleared form `k * e_k = ...`, whence the paper's
    "divisions by k are exact");
  * `recoveryPoly_coeff` / `recoveryPoly_eq_sum` are Vieta: the monic polynomial built
    from the e_k is `∏ p ∈ S, (X - C p)`;
  * `isRoot_recoveryPoly_iff` and `recovery_eq_filter` are root reading: evaluating over
    the window recovers exactly `S`, with no primality test anywhere.
-/
import Mathlib

open Polynomial Finset

namespace PrimeMoments

/-- The recovery polynomial of a finite set of integers: `∏ p ∈ S, (X - C p)`. -/
noncomputable def recoveryPoly (S : Finset ℤ) : ℤ[X] :=
  ∏ p ∈ S, (X - C p)

theorem recoveryPoly_monic (S : Finset ℤ) : (recoveryPoly S).Monic :=
  monic_prod_of_monic _ _ fun p _ => monic_X_sub_C p

theorem recoveryPoly_natDegree (S : Finset ℤ) :
    (recoveryPoly S).natDegree = S.card := by
  unfold recoveryPoly
  rw [Finset.prod_eq_multiset_prod]
  exact natDegree_multiset_prod_X_sub_C_eq_card S.val

/-- Vieta, coefficient form: the coefficients of the recovery polynomial are the signed
elementary symmetric functions of the configuration. This identifies the paper's integers
`e_k` with the coefficients of `f`. -/
theorem recoveryPoly_coeff (S : Finset ℤ) {k : ℕ} (h : k ≤ S.card) :
    (recoveryPoly S).coeff k = (-1) ^ (S.card - k) * S.val.esymm (S.card - k) := by
  unfold recoveryPoly
  rw [Finset.prod_eq_multiset_prod]
  simpa using Multiset.prod_X_sub_C_coeff S.val (by simpa using h)

/-- Vieta, expanded form: `f = Σ_j (-1)^j e_j X^(r-j)`, the display in the paper's
Theorem 1. -/
theorem recoveryPoly_eq_sum (S : Finset ℤ) :
    recoveryPoly S =
      ∑ j ∈ Finset.range (S.card + 1),
        (-1) ^ j * (C (S.val.esymm j) * X ^ (S.card - j)) := by
  unfold recoveryPoly
  rw [Finset.prod_eq_multiset_prod]
  simpa using Multiset.prod_X_sub_X_eq_sum_esymm S.val

/-- Newton's recursion, specialized from mathlib's generic Newton identities to a
concrete integer configuration: the paper's decoder recursion, in division-cleared form.
`s_i = ∑ p ∈ S, p^i` are the delivered power-sum moments. -/
theorem newton_recursion (S : Finset ℤ) (k : ℕ) :
    (k : ℤ) * S.val.esymm k =
      (-1) ^ (k + 1) *
        ∑ a ∈ (antidiagonal k).filter (fun a => a.1 < k),
          (-1) ^ a.1 * S.val.esymm a.1 * ∑ p ∈ S, p ^ a.2 := by
  classical
  have base := MvPolynomial.mul_esymm_eq_sum (σ := {x // x ∈ S}) (R := ℤ) k
  have happ := congrArg (MvPolynomial.aeval (fun i : {x // x ∈ S} => (i : ℤ))) base
  have hmap :
      Multiset.map (fun i : {x // x ∈ S} => (i : ℤ)) Finset.univ.val = S.val := by
    rw [Finset.univ_eq_attach, Finset.attach_val]
    exact Multiset.attach_map_val S.val
  have hesymm : ∀ n, MvPolynomial.aeval (fun i : {x // x ∈ S} => (i : ℤ))
      (MvPolynomial.esymm {x // x ∈ S} ℤ n) = S.val.esymm n := by
    intro n
    rw [MvPolynomial.aeval_esymm_eq_multiset_esymm, hmap]
  have hpsum : ∀ n, MvPolynomial.aeval (fun i : {x // x ∈ S} => (i : ℤ))
      (MvPolynomial.psum {x // x ∈ S} ℤ n) = ∑ p ∈ S, p ^ n := by
    intro n
    have h := Finset.sum_attach S fun p => p ^ n
    simp [MvPolynomial.psum, map_sum, map_pow, MvPolynomial.aeval_X, h]
  simpa [map_mul, map_sum, map_pow, map_natCast, hesymm, hpsum] using happ

/-- Root reading: the integer roots of the recovery polynomial are exactly the members
of `S`. No primality enters. -/
theorem isRoot_recoveryPoly_iff {S : Finset ℤ} {c : ℤ} :
    (recoveryPoly S).IsRoot c ↔ c ∈ S := by
  unfold recoveryPoly
  simp [IsRoot, eval_prod, eval_sub, eval_X, Finset.prod_eq_zero_iff,
    sub_eq_zero]

/-- The paper's final clause, `P(W) = { c ∈ W : f(c) = 0 }`: evaluating the recovery
polynomial across any window containing the configuration returns the configuration
exactly. The decoder is uniform over arbitrary finite sets of distinct integers. -/
theorem recovery_eq_filter (S W : Finset ℤ) (hSW : S ⊆ W) :
    W.filter (fun c => (recoveryPoly S).eval c = 0) = S := by
  ext c
  simp only [Finset.mem_filter]
  constructor
  · exact fun h => isRoot_recoveryPoly_iff.mp h.2
  · exact fun h => ⟨hSW h, isRoot_recoveryPoly_iff.mpr h⟩

end PrimeMoments
