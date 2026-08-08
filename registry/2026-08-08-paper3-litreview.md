# Literature review — Paper 3 (prime_recovery_paper.tex)

Date: 2026-08-08. Method: three parallel search agents (recovery routes; obstruction theorem
+ moment framing; bibliography verification + chase + OEIS), ~60 distinct queries plus
GitHub code searches and OEIS git-mirror fetches. Same egress caveat as the Paper 1–2
reviews; github.com/raw.githubusercontent.com reachable and used (OEIS mirror, McKenzie
repo, Rényi Institute Erdős scan reachable via search-indexed PDF).

## Verdicts

### Route I — Newton's identities decoder
**Survives.** No source recovers the primes of an interval (or any prime set) from power
sums. The machinery has two citable canons the paper should engage: the modern pure-math
study of exactly this recovery problem, Melánová–Sturmfels–Winter, "Recovery from Power
Sums" (Exp. Math. 33 (2024), 225–234; arXiv:2106.13981) — general theory, no primes — and
the CS classic of the exact-arithmetic decoder, Ben-Or–Tiwari (STOC 1988): power sums →
Hankel/Newton → integer roots. Route I is their machinery applied to a new support.

### Route II — product/θ decoder
**The decoder and its bit-accounting appear new; two uncited neighbors are mandatory.**
(1) Gandhi's formula (1971; proofs: Vanden Eynden, Amer. Math. Monthly 79 (1972);
Golomb, Pacific J. Math. 63 (1976), 401–404): the next prime recovered from the divisors of
the primorial — the classical "product of primes determines primes" statement.
(2) Fridman–Garbulsky–Glecer–Grime–Tron Florentin, "A Prime-Representing Constant"
(Amer. Math. Monthly 126 (2019), 70–73): one real (2.92005…) whose floor recurrence emits
all primes — and by OEIS A249270 the constant is a primorial-denominated series. Both are
"stores the answers" objects that live outside Definition 1's model, exactly like Mills and
Willans, and the model discussion must say so. Nobody prices θ on a window in bits or states
the exp-round-trial-divide decoder.

### Obstruction theorem (bit floor)
**No direct competitor anywhere; the counting step has canonical citable homes.**
- Pigeonhole floor ⌈log₂ C(u,n)⌉ for representing subsets: Brodnik–Munro, SIAM J. Comput.
  28 (1999), 1627–1640 (succinct data structures baseline); classical ancestor Erdős–Rényi,
  "On two problems of information theory" (1963).
- "Entropy of the primes" has an established different meaning — Kontoyiannis (ITW 2008;
  arXiv:0710.4076): entropy proofs of Chebyshev-type estimates. Cite to disambiguate.
- Closest prior art in spirit: Kolpakov–Rocke, "On the impossibility of discovering a
  formula for primes using AI" (arXiv:2308.10817, 2023/24, apparently unrefereed) —
  algorithmic-information heuristics, not a finite counting bound in a delivered-bits model.
  Cite and delimit.
- The quantitative "Mills' constant needs about as many bits as the primes it produces"
  claim has NO refereed statement anywhere found — the paper's theorem appears to be the
  first precise form of the folklore. Attribution sentence: "folklore; see Wilf, Dudley,
  Caldwell–Cheng."
- Named classics for the folklore the paper makes precise: Wilf, "What is an answer?"
  (Amer. Math. Monthly 89 (1982), 289–292); Dudley, "Formulas for primes" (Math. Mag. 56
  (1983), 17–22); Jones–Sato–Wada–Wiens, "Diophantine representation of the set of prime
  numbers" (Amer. Math. Monthly 83 (1976), 449–464); Caldwell–Cheng, "Determining Mills'
  constant..." (J. Integer Seq. 8 (2005), art. 05.4.1); modern successor Prunescu–Shunia
  (arXiv:2412.14594): fixed-length arithmetic terms for π(n) and p_n.
- Optional footnote: Barzdins' lemma (characteristic sequence of any computable set has
  K = O(log n)) — the complexity-theoretic form of the paper's own "unrestricted world"
  caveat.

### Prony remark
Currently cites only Prony 1795. The "intermediate precision" claim is exactly the
Vandermonde conditioning story: cite Moitra (STOC 2015; condition-number phase transition
in terms of node separation — the primes' gap ≥ 2 puts the windows in the well-separated
regime) and/or Batenkov–Yomdin (SIAM J. Appl. Math. 73 (2013), 134–154). Candès–
Fernandez-Granda (CPAM 67 (2014)) optional for the super-resolution frame.

### Polymath relation
Bibitem incomplete (missing no. 278, pages 1233–1246; journal byline differs from the
arXiv's "D.H.J. Polymath"). Substantive: Polymath's method extracts the PARITY of the
number of window primes in O(N^(1/2−c)) — structurally a 1-bit exact functional of the
window, i.e. a moment channel with a partial decoder; one acknowledging sentence
recommended beyond the current time-barrier citation.

## Bibliography verification (all 12 entries)

Correct as printed: Macdonald (2nd ed. 1995; optionally add "Oxford Mathematical
Monographs, Clarendon Press"), Mills (BAMS 53 (1947), 604), Willans (Math. Gaz. 48 (1964),
413–415), Erdos (Acta Litt. Sci. Szeged 5 (1932), 194–198 — verified against the Rényi
Institute scan; correct anchor for N ≤ 4^m via N | C(2m,m) < 4^m), Cheb (JMPA (1) 17
(1852), 366–390), CompanionI/II/Code (self-references, format only).
Corrections/upgrades:
1. Polymath: add no. 278, 1233–1246.
2. Prony: add the full title ("Essai expérimental et analytique: sur les lois de la
   dilatabilité des fluides élastiques...") and cahier 2 — the "cahier 22" common in the
   signal-processing literature is anachronistic (cahier 22 ≈ 1813).
3. Linnik: add "Translations of Mathematical Monographs, Vol. 4".
4. McKenzie: upgrade to the canonical two-part form (as Papers 1–2).

## OEIS / ecosystem

- A073838 = product of primes in [n, 2n] — the paper's N up to boundary convention
  (closed interval; differs from (m,2m] when m is prime). No references attached in the
  entry. A073837 is the sum analogue. Optional pointer + convention remark.
- No implementation of either decoder exists anywhere searched (GitHub code search,
  Project Euler/CP circles, Prony libraries). Confirmed absence.

## Recommended edits (pending author approval)

1. Model discussion: add Gandhi (via Vanden Eynden + Golomb) and Fridman et al. as
   "stores-the-answers" objects outside the model, alongside Mills/Willans; cite
   Jones–Sato–Wada–Wiens and Prunescu–Shunia as the polynomial/arithmetic-term forms;
   anchor the folklore to Wilf + Dudley; anchor "Mills' constant stores the answers" to
   Caldwell–Cheng; cite and delimit Kolpakov–Rocke.
2. Obstruction theorem: cite Brodnik–Munro (+ Erdős–Rényi) for the counting floor;
   cite Kontoyiannis to disambiguate "entropy of the primes".
3. Route I: cite Melánová–Sturmfels–Winter and Ben-Or–Tiwari.
4. Prony remark: cite Moitra + Batenkov–Yomdin; note the gap-≥-2 separation.
5. Polymath: fix the record; add the parity-as-1-bit-channel sentence.
6. Bibliography upgrades: Prony full title/cahier, Linnik series, McKenzie canonical form.

## Items requiring open-network full-text confirmation

1. Kolpakov–Rocke (arXiv:2308.10817) — read to delimit precisely; unrefereed status.
2. "Prime Successor Irreducibility" (arXiv:2605.12504, 2026) — conceptually adjacent
   (uniform bounded-description algorithms for prime successors); check before submission.
3. Melánová–Sturmfels–Winter — confirm no bit-budget/integer-certification content.
4. Prony 1795 cahier — resolve 2 vs 22 against Gallica if a venue demands it.
5. Gandhi's original 1971 note (the standard citations are the Vanden Eynden/Golomb proofs).
6. McKenzie PrimeSumming manuscript — carried over from the Paper 1 list.

## Overall

No claim invalidated; both decoders and the obstruction theorem stand. The review's
material yield: the model discussion has famous uncited neighbors (Gandhi, Fridman et al.,
JSWW, Wilf, Dudley) that a referee would raise on first read; the counting bound and the
Prony precision claim each acquire standard citations; and — a strengthening finding — the
quantitative form of the "no short formula" folklore appears to have no refereed precise
statement, making the paper's Theorem the first, which the revision can now say with
citations delimiting the folklore.
