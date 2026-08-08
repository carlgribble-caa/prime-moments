# Literature review — Paper 1 (prime_sum_formula_paper.tex, at review time named u_space_prime_formula_paper.tex)

Date: 2026-08-08. Method: three parallel search agents (claims 1–2; claims 3–5 + OEIS;
computational thread + citation chasing), ~110 distinct queries across arXiv, general web,
OEIS, GitHub, Google Scholar/Semantic Scholar surfaces; one synthesis round. Environment
caveat: the session's egress proxy blocked direct fetching of most external pages (arXiv,
OEIS, McKenzie's sites, Codeforces, archive.org); GitHub/raw.githubusercontent were
reachable. Page-level assessments therefore rest on search-index excerpts plus fetched
GitHub sources; items needing open-network full-text confirmation are listed at the end.

## Per-claim verdicts

### Claim 1 — Linnik's identity derived as multiplication-table de-duplication
**Survives.** No source found presenting Linnik's identity as the exact resolution of the
table's duplication ledger; standard derivations (Friedlander–Iwaniec, Tao's notes, arXiv
expositions) all go through log ζ or convolution inversion. The *founding observation*
(primes = what the table cannot make; entry m appears with multiplicity tied to d(m)) is
pedagogical folklore: Illustrative Mathematics task 1493; Dan MacKinnon, "A deep dive into
the multiplication table" (mathrecreation.com, 2012); Sieve of Sundaram (1934) as a literal
"table-complement" sieve. The de-duplicated table's *cardinality* has a named literature —
the Erdős multiplication table problem (Erdős 1955/1960; K. Ford, Ann. of Math. 2008;
Brent–Pomerance et al., arXiv:1908.04251) — asymptotic, no exact identity, no Linnik.
Residual risk: McKenzie's expository pages (below) could not be full-text read.

### Claim 2 — uniform weight-j system (counts/sums/power sums via Linnik)
**Substance anticipated by McKenzie — which the paper already concedes in the abstract and
§1/§7.** New finding: the concession is even more literal than the current bibliography
shows. McKenzie's companion manuscript `PrimeSumming_NathanMcKenzie.pdf` and code
`primesumcount.cpp` (github.com/NathanMcKenzie/InitalTest, dated 2011-11-26; header fetched
verbatim) compute "summation of primes raised to a non-negative integer power up to n" in
"the ballpark of O(n^2/3 log n) time and O(n^1/3 log n) space" via Linnik — i.e. the
monomial weight dial p^j, counts and power sums, in one program, for prefix ranges [1, x].
What remains un-anticipated anywhere found: the single three-line induction presentation,
arbitrary intervals (A, B], and the self-similar prime-free dust closure
S_{aj}(⌊y^{1/a}⌋). Adjacent non-Linnik unifications (should be acknowledged): Min_25 sieve
(~2017, CP ecosystem); Hirsch–Kessler–Mendlovic, arXiv:2212.09857 (elementary Õ(√N),
unifies counts/sums/Mertens/totient — asymptotically best elementary method); Orlov
(cited); Lucy_Hedgehog (cited) + gbroxey's 2023 Lucy+Fenwick x^(2/3) upgrade with prime
sums and arithmetic-progression extensions.

### Claim 3 — duplicated-mass cancellation theorem
**Survives.** No prior statement found under any searched phrasing. Honest framing (which
the paper already uses): an elementary consequence of Linnik's identity not found stated
elsewhere.

### Claim 4 — interval taxonomy + layer-birth law
**Packaging survives; every ingredient is known and now has nameable citations.** The
quotient set {⌊N/d⌋}: cardinality 2√N + O(1) exactly in R. Heyman, "Cardinality of a floor
function set", INTEGERS 19 (2019) #A67 (arXiv:1905.00533); structural theory in
J. C. Lagarias & D. H. Richman, "The floor quotient partial order", Adv. Appl. Math. 2023
(arXiv:2212.11689) and sequel arXiv:2403.04342. Smallest k-almost-prime = 2^k: folklore
(Wikipedia/MathWorld; OEIS A014612/A014613 first terms; equivalently d'_k(n) = 0 for
n < 2^k, present in McKenzie as the truncation of Linnik's sum at ⌊log₂ n⌋). The
"birthday/single-newborn" dyadic organization: not found anywhere. OEIS checked: A055086,
A036378, A078840, A125149, A014612/3, A001358, A067514 — no birth framing, no
prime-increment commentary surfaced.

### Claim 5 — lattice-growth observable (prime step ⇒ single new point)
**Survives as stated, but is one lemma away from folklore and sits inside an active
uncited literature — engaging it is the most important revision.** Ingredients that are
folklore: ⌊(n+1)/k⌋ = ⌊n/k⌋ + [k | n+1]; d(n) = 2 iff n prime; the Physics Forums remark
that D(n) − D(n−1) = 2 detects primes (divisor summatory function — same spirit, different
lattice). The directly relevant literature the paper does not cite: "primes in floor
function sets" (Bordellès–Dai–Heyman–Pan–Shparlinski origin paper; R. Heyman,
arXiv:2111.00408; Ma–Wu, arXiv:2112.12426, Bull. Aust. Math. Soc.; Runbo Li,
arXiv:2308.16301; Saito–Suzuki–Takeda–Yoshida, arXiv:2312.15642) — asymptotics of primes
inside {⌊x/n⌋}, no increment/growth observable found in any excerpt, but it is the same
object. Distinguishing note for the revision: A055086 (distinct ⌊n/k⌋ values) does NOT
increment specially at primes; the paper's observable concerns its specific evaluation
lattice (closure under floor-division/roots), where growth is exactly at divisors of y+1.

## Computational-thread verification

- **McKenzie citation (canonical form).** Web exposition: "Counting Primes Quickly with
  Linnik's Identity", 2011-03-24, icecreambreakfast.com/page/dirmath/primecounting.php
  (URL that OEIS A000720 links). PDF manuscript: "Computing the Prime Counting Function
  with Linnik's Identity in O(n^(2/3) log n) Time and O(n^(1/3) log n) Space" (~2011-11-23),
  primecounting.com/prime-counting-algorithms/PrimeCounting_NathanMcKenzie.pdf. Power sums:
  PrimeSumming manuscript + primesumcount.cpp (2011-11-26), github.com/NathanMcKenzie/InitalTest.
  No arXiv version, no refereed publication. x^(2/3) attribution fair, with caveats: the
  bound is McKenzie's own estimate in an unrefereed manuscript, and the power-sum code is a
  floating-point demonstration he himself flagged as not scale-ready. "Pioneered the
  computational route" is accurate — nothing earlier found. A 2013 McKenzie manuscript
  "Linnik's Identity and Various Explicit Prime Counting Formulas" exists (docplayer
  141264368) — unread, see below.
- **Post-2013 Linnik thread.** Only two genuinely Linnik-based items found: R. Sladkey's
  Dirichlet project (github.com/ricksladkey/Dirichlet; π(n) mod 2/3 from D_k via Linnik;
  notes credit "From Nathan McKenzie" / "From Mark Lewko"), underpinned by Sladkey,
  arXiv:1206.3369 (D(n) in O(n^(1/3))); and adamant's Codeforces entry 117783 (2023),
  π(n) in O(n^(2/3)) by logarithms of Dirichlet series. Everything else active is
  Legendre–Meissel-family. Nobody found computes interval/arbitrary-weight prime power
  sums via Linnik with a prime-free recursion.
- **Practical state of the art (uncited).** K. Walisch's primesum (modified Deléglise–Rivat;
  records to 10^26 with D. Baugh; OEIS A046731/A099824/A130739). primecount/primesum
  reference lists contain no Linnik/McKenzie — the two traditions are disjoint in practice.
- **Citation chase.** Orlov (arXiv:2111.15545, confirmed): essentially uncited. Staple
  (arXiv:1503.01839; fuller form: MSc thesis, Dalhousie, Aug 2015): cited by primecount
  docs, Aggarwal arXiv:2510.16285 (marginal). Deléglise–Rivat: most relevant citers are
  primesum and Hirsch–Kessler–Mendlovic.

## Recommended edits (pending author approval)

1. **Bibliography — widen the McKenzie bibitem** to its canonical two-part form (counting
   PDF with full title/URL + PrimeSumming manuscript/code) so the abstract's concession is
   bibliographically backed.
2. **Section 6 / related work — add** Hirsch–Kessler–Mendlovic (arXiv:2212.09857),
   Sladkey (arXiv:1206.3369), and Walisch's primesum to the Legendre–Meissel paragraph;
   optionally adamant CF 117783 and gbroxey's Lucy+Fenwick post as the modern non-journal
   thread (the latter is directly relevant to the paper's residue-classes remark).
3. **Lattice-growth remark (Claim 5) — add citations** to Heyman (1905.00533 for 2√N;
   2111.00408), Ma–Wu (2112.12426), and Lagarias–Richman (2212.11689 "floor quotient
   partial order"), with one distinguishing sentence (evaluation-lattice growth at divisors
   vs. the non-discriminating count A055086; kinship with D(n) − D(n−1) = d(n) folklore).
4. **Introduction — one context sentence** citing the Erdős multiplication table problem
   (Erdős; Ford 2008) as the named tradition on the de-duplicated table, and optionally
   Sundaram's sieve as the classical table-complement device.
5. **Optional footnote**: "hyperbola shells" collides with "hyperbolic shells" of the
   quadratic-forms literature (Bentkus–Götze); a disambiguating word would prevent
   referee confusion.
6. **Optional precision**: where x^(2/3) is attributed to McKenzie, "in an unrefereed
   manuscript" or "(heuristic analysis)" would be maximally honest; current wording is
   defensible as is.

## Items requiring open-network full-text confirmation (egress-blocked here)

1. McKenzie, icecreambreakfast.com/page/dirmath/primecounting.php — read end-to-end for
   any table/de-duplication framing (Claim 1's single residual risk).
2. McKenzie, PrimeCounting_NathanMcKenzie.pdf and PrimeSumming_NathanMcKenzie.pdf — same
   check + confirm power-sum scope (prefix vs interval).
3. McKenzie 2013, "Linnik's Identity and Various Explicit Prime Counting Formulas"
   (docplayer.net/amp/141264368) — check for interval/weight extensions.
4. Lagarias–Richman (2212.11689, 2403.04342) — check for any n → n+1 increment lemma.
5. Ma–Wu (2112.12426), Heyman (2111.00408), Li (2308.16301) — confirm no growth-at-primes
   observable; harvest exact statements for the distinguishing sentence.
6. OEIS A067514 comment field (primes of the form ⌊n/k⌋).
7. mersenneforum prime-counting threads ca. 2012–2016 (likely McKenzie–Sladkey–Lewko
   exchange venue).

## Overall

No finding invalidates any theorem or forces retraction of a claim. The paper's
"claims and non-claims" architecture survives contact with the literature; the abstract's
McKenzie concession is exactly right and predates this review. Required work is additive:
one bibitem repair, ~6 added citations, and two or three distinguishing sentences,
concentrated on the lattice-growth remark.
