/-
WP7.H2 — Companion III, Theorem 3 (bit floor), kernel-checked.
Paper: C. Gribble, "Recovering the primes in a dyadic interval from exact moments",
doi:10.5281/zenodo.21769107, Definition 1 and Theorem 3.

Paper statement: a `D`-bit uniform scheme for `(m, r)` is a pair (Φ, Ψ) where Φ maps each
r-element subset of the m-integer window to a bitstring of length at most D, and Ψ(Φ(S)) = S
for every such subset. Every such scheme satisfies `D ≥ log₂ C(m, r) − 1`; the proof is that
Φ must be injective on the C(m, r) configurations while there are only `2^(D+1) − 1`
bitstrings of length at most D.

Formalization shape: the window is modeled as `Fin m` — only its cardinality enters, which is
exactly the paper's model (the scheme is uniform over configurations; the window's arithmetic
is invisible to it). `bitCode` embeds bitstrings into ℕ by little-endian binary digits with a
sentinel `1` appended, giving injectivity and the range bound `[1, 2^(len+1))`; the counting
argument is then `Finset.card_le_card` on the image inside `Ico 1 (2^(D+1))`, whose size is
exactly the paper's `2^(D+1) − 1`. The real-logarithm corollary is derived at the end.
-/
import Mathlib

open Finset

namespace PrimeMoments

/-! ### Bitstrings, counted -/

/-- Injective numeral code for bitstrings: little-endian binary digits with a sentinel `1`
appended (the sentinel preserves trailing zeros, i.e. distinguishes `[false]` from `[]`). -/
def bitCode (l : List Bool) : ℕ :=
  Nat.ofDigits 2 (l.map (fun b => cond b 1 0) ++ [1])

lemma bitDigits_lt (l : List Bool) :
    ∀ d ∈ l.map (fun b => cond b 1 0) ++ [1], d < 2 := by
  intro d hd
  rcases List.mem_append.mp hd with h | h
  · rcases List.mem_map.mp h with ⟨b, -, rfl⟩
    cases b <;> simp
  · rcases List.mem_singleton.mp h with rfl
    norm_num

lemma bitCode_digits (l : List Bool) :
    Nat.digits 2 (bitCode l) = l.map (fun b => cond b 1 0) ++ [1] := by
  refine Nat.digits_ofDigits 2 one_lt_two _ (bitDigits_lt l) ?_
  intro h
  simp

lemma bitCode_injective : Function.Injective bitCode := by
  intro l₁ l₂ h
  have h2 : l₁.map (fun b => cond b 1 0) ++ [1] = l₂.map (fun b => cond b 1 0) ++ [1] := by
    rw [← bitCode_digits l₁, ← bitCode_digits l₂, h]
  have h3 : l₁.map (fun b => cond b 1 0) = l₂.map (fun b => cond b 1 0) :=
    List.append_left_injective _ h2
  have hinj : Function.Injective (fun b : Bool => (cond b 1 0 : ℕ)) := by
    intro a b hab
    cases a <;> cases b <;> simp_all
  exact List.map_injective_iff.mpr hinj h3

lemma bitCode_lt (l : List Bool) : bitCode l < 2 ^ (l.length + 1) := by
  have h := Nat.ofDigits_lt_base_pow_length (b := 2) one_lt_two (bitDigits_lt l)
  simpa [bitCode, List.length_append, List.length_map] using h

lemma one_le_bitCode (l : List Bool) : 1 ≤ bitCode l := by
  unfold bitCode
  rw [Nat.ofDigits_append]
  have h2 : 0 < 2 ^ (l.map fun b => cond b 1 0).length * Nat.ofDigits 2 [1] := by
    rw [Nat.ofDigits_singleton]
    simp
  omega

/-! ### Uniform schemes and the floor -/

/-- Definition 1 of the paper: a `D`-bit uniform scheme for `(m, r)` — an encoder to
bitstrings of length at most `D` and a decoder inverting it on every `r`-element
configuration. No other constraint: the encoder may be any quantization of any moments,
the decoder any function of the bits. -/
structure UniformScheme (m r D : ℕ) where
  encode : Finset (Fin m) → List Bool
  decode : List Bool → Finset (Fin m)
  length_le : ∀ {S : Finset (Fin m)}, S.card = r → (encode S).length ≤ D
  decode_encode : ∀ {S : Finset (Fin m)}, S.card = r → decode (encode S) = S

namespace UniformScheme

variable {m r D : ℕ}

lemma encode_injOn (sch : UniformScheme m r D) :
    Set.InjOn (fun S => bitCode (sch.encode S)) ↑(powersetCard r (univ : Finset (Fin m))) := by
  intro S₁ h₁ S₂ h₂ h
  have c₁ : S₁.card = r := (Finset.mem_powersetCard.mp (Finset.mem_coe.mp h₁)).2
  have c₂ : S₂.card = r := (Finset.mem_powersetCard.mp (Finset.mem_coe.mp h₂)).2
  have e : sch.encode S₁ = sch.encode S₂ := bitCode_injective h
  calc S₁ = sch.decode (sch.encode S₁) := (sch.decode_encode c₁).symm
    _ = sch.decode (sch.encode S₂) := by rw [e]
    _ = S₂ := sch.decode_encode c₂

/-- **Theorem 3 of the paper, exact counting form**: every `D`-bit uniform scheme for
`(m, r)` satisfies `C(m, r) ≤ 2^(D+1) − 1`. -/
theorem choose_le (sch : UniformScheme m r D) :
    m.choose r ≤ 2 ^ (D + 1) - 1 := by
  classical
  set C : Finset (Finset (Fin m)) := powersetCard r (univ : Finset (Fin m)) with hC
  have hsub : C.image (fun S => bitCode (sch.encode S)) ⊆ Finset.Ico 1 (2 ^ (D + 1)) := by
    intro n hn
    rcases Finset.mem_image.mp hn with ⟨S, hS, rfl⟩
    have hc : S.card = r := (Finset.mem_powersetCard.mp (hC ▸ hS)).2
    refine Finset.mem_Ico.mpr ⟨one_le_bitCode _, ?_⟩
    calc bitCode (sch.encode S) < 2 ^ ((sch.encode S).length + 1) := bitCode_lt _
      _ ≤ 2 ^ (D + 1) :=
        Nat.pow_le_pow_right (by norm_num) (by have := sch.length_le hc; omega)
  have himg : (C.image (fun S => bitCode (sch.encode S))).card = C.card :=
    Finset.card_image_of_injOn sch.encode_injOn
  have hle := Finset.card_le_card hsub
  rw [himg] at hle
  simpa [hC, Finset.card_powersetCard, Finset.card_univ, Nat.card_Ico] using hle

/-- The display form of the paper's proof: `2^(D+1) > C(m, r)`. -/
theorem choose_lt (sch : UniformScheme m r D) :
    m.choose r < 2 ^ (D + 1) := by
  have h := sch.choose_le
  have h1 : 0 < 2 ^ (D + 1) := pow_pos (by norm_num) _
  omega

/-- **Theorem 3, logarithmic form**: `D ≥ log₂ C(m, r) − 1`. -/
theorem logb_bound (sch : UniformScheme m r D) (hr : 0 < m.choose r) :
    Real.logb 2 (m.choose r) - 1 ≤ (D : ℝ) := by
  have hlt : (m.choose r : ℝ) ≤ (2 : ℝ) ^ ((D : ℝ) + 1) := by
    have h : (m.choose r : ℝ) < (2 : ℝ) ^ (D + 1 : ℕ) := by exact_mod_cast sch.choose_lt
    rw [show ((D : ℝ) + 1) = ((D + 1 : ℕ) : ℝ) by push_cast; ring, Real.rpow_natCast]
    exact h.le
  have hx : (0 : ℝ) < (m.choose r : ℝ) := by exact_mod_cast hr
  have hlog := (Real.logb_le_iff_le_rpow (by norm_num : (1:ℝ) < 2) hx).mpr hlt
  linarith

end UniformScheme

end PrimeMoments
