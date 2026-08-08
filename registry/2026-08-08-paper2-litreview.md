# Literature review — Paper 2 (prime_ladder_paper.tex)

Date: 2026-08-08. Method: three parallel search agents (assembly claim; certified protocol;
bibliography verification + citation chase + OEIS), ~65 distinct queries. Same egress caveat
as the Paper 1 review (registry/2026-08-08-paper1-litreview.md): most external pages
unreachable, assessments from search excerpts plus GitHub-hosted sources (OEIS git mirror
`oeis/oeisdata` was reachable and used directly).

## Verdicts

### The assembly claim (§1: "moment ladder + certified integer determination not in the literature")
**Survives on every front searched.** Nothing found using Chebyshev-rescaled (or any
polynomial) exponent sequences in factorial-like products to extract prime moments; nothing
resembling a moment ladder for primes; no elementary method closing exact moments into an
integer determination; no certified computation of interval prime *sums* anywhere (the
certified neighbors are counts and θ/ψ). Nearest structural relatives, all now cited:
- Lagarias–Mehta (IJNT 12, 2016; arXiv:1409.4145) and Du–Lagarias (IJNT 18 (2022), 691–728;
  arXiv:2006.15439): threshold-split valuations of products of binomial coefficients —
  same objects, asymptotic goals (PNT/RH), no exact functionals, no ladder. Full-text check
  of both remains the highest-value manual follow-up.
- The Chebyshev–Sylvester weight lineage — Sylvester, Erdős–Kalmár (1937, lost),
  Diamond–Erdős (Enseign. Math. 26, 1980), recent computational revival (Gantumur,
  arXiv:2512.02466): optimized finitely supported weights on log⌊x⌋!, always one-sided
  bounds, never exact window functionals.
- Xylouris (arXiv:0709.4676): a family of interval-count identities from binomial
  valuations, with O(√k) errors — inexact, count-valued.
- Gelfond–Schnirelman–Nair method (Pritsker's survey): the other polynomial-approximation
  route to prime bounds; inequalities only. Not cited (judged optional).
- Terminology collision: Bhargava's "generalized factorials" (AMM 107, 2000) are a different
  construction — now disambiguated in a footnote.

### The certified protocol
**Novel for prime sums; the closure pattern itself has a published precedent now cited.**
Johansson's Hardy–Ramanujan–Rademacher implementation (LMS JCM 15, 2012) computes p(n) as a
certified ball and verifies it contains a unique integer — the identical
enclosure-plus-integrality closure, in additive number theory. The analytic π(x) tradition
(Lagarias–Odlyzko 1987; Platt 2015; Büthe) uses the same principle, as the paper already
said; rigorous θ(x) computations (Platt–Trudgian, Math. Comp. 85, 2016) are the nearest
certified prime-sum-like objects (log-weighted, whole-range). No prior application of
moment-problem/Gauss-quadrature bounds (Chebyshev–Markov–Stieltjes; Krein–Nudelman;
Karlin–Studden; Golub–Meurant) to window primes found — a remark now records the connection
and the open possibility of quadrature-tightened windows.

The 3+2√2 floor: no source attaches the constant to this setup, but it equals the classical
Chebyshev rate (√κ+1)/(√κ−1) at condition ratio κ=2 (Chebyshev's best approximation of 1/x;
modern writeup Kraus–Vassilevski–Zikatanov arXiv:1002.1859) — the paper now says so
explicitly to avoid appearing to claim a classical constant.

Trust-base finding: mpmath's interval (iv) context is documented as experimental. Verified
against code/certified_snap.py: the pipeline uses only interval + − × ÷ and iv.log. The
trust-base paragraph now cites mpmath, states that operation surface, and points to Arb and
Tucker's Validated Numerics.

Motivation finding: Deléglise's 2009 sum-of-primes-below-10^21 was withdrawn in 2011 after
an off-by-one discrepancy (documented in the primesum README, already cited) — now cited in
the introduction as concrete motivation for certification.

### Bibliography verification (all 18 entries checked)
Correct as printed: Cheb (JMPA (1) 17 (1852), 366–390, confirmed against the Numdam scan),
DR, Orlov, primesum, Platt (84 (2015), 1521–1535), HypVal1 (Onnis), HypVal2 (Pain), Bend
(Acta Math. 61 (1933), 263–322), Adam (JCAM 100 (1998), 191–199), Linnik, Tref.
Corrected in this pass:
1. Lucy bibitem: blog author "G. Broxey" was a mis-expansion of the GitHub handle `gbroxey`;
   the author is Griffin Macris → "G. Macris". PE deep link added.
2. Büthe: pages 1991–2009 added for the Math. Comp. 87 entry.
3. Coppo: "art. 8" replaced by the DOI 10.1007/s40993-023-00505-2 (evidence pointed to
   art. no. 15; DOI is unambiguous).
4. Staple: Dalhousie MSc thesis (2015) added.
5. McKenzie: upgraded to the canonical two-part form established in the Paper 1 review.
6. DR: extended with Deléglise–Rivat "Computing ψ(x)" (Math. Comp. 67 (1998), 1691–1696),
   the nearer neighbor to prime sums.

### Citation chase / OEIS
- Onnis is cited only by Pain; Pain only by OEIS A002109/A046882. Nobody applies
  hyperfactorial valuations to prime moments.
- No citer of Platt/Büthe certifies interval prime sums.
- OEIS: A073837 is "sum of primes p, n ≤ p ≤ 2n" (note: inclusive at both ends — boundary
  convention differs from S(m) over (m,2m] when m is prime); A073838 the product analogue
  (rung 0's object); A034387 sum of primes ≤ n; A002109 hyperfactorial (lists Pain but not
  Onnis — a possible OEIS contribution). No certified-method references in any entry.
- primesum computes dyadic *thresholds* (sums below 2^n up to 2^80) but has no
  interval/window functionality — the community treats windows by differencing.

## Edits applied 2026-08-08 (same day, commit follows this memo)

1. Intro: Lagarias–Odlyzko now cited (was named without a bibitem — the review's one outright
   citation error); Johansson HRR cited as the closure-pattern precedent; Platt–Trudgian
   cited for certified θ; withdrawn-10^21 anecdote added.
2. Bhargava disambiguation footnote at first "generalized factorials".
3. Prop. (geometric decay) proof sketch: 3+2√2 identified as the classical κ=2 rate, KVZ cited.
4. New remark (Moment-problem reading): Chebyshev–Markov–Stieltjes circle, Krein–Nudelman,
   Karlin–Studden, Golub–Meurant; quadrature-tightening flagged as unpursued.
5. Trust base: mpmath cited, iv-experimental acknowledged, operation surface stated, Arb and
   Tucker pointed to.
6. Related identities: nearest-relatives passage (Lagarias–Mehta, Du–Lagarias,
   Diamond–Erdős, Gantumur, Xylouris).
7. Bibliography: 6 corrections (above) + 16 new bibitems (LO, PT, JohanssonHRR, mpmath, Arb,
   Tucker, KVZ, KN, KS, GM, Bhargava, LM, DuL, DE, Gantumur, Xylouris).

## Items requiring open-network full-text confirmation

1. Du–Lagarias (arXiv:2006.15439) and Lagarias–Mehta (arXiv:1409.4145) — the closest
   structural neighbors; confirm no exact-functional assembly hides inside.
2. Gantumur (arXiv:2512.02466) — its bibliography likely maps the whole Sylvester
   weight-scheme literature; harvest for anything missed.
3. Coppo article number (15 vs 8) — resolve if a venue requires it; the DOI now cited is
   unambiguous either way.
4. McKenzie's PrimeSumming manuscript — same item as the Paper 1 list.
5. Raman arXiv:2012.00882 (generalized superfactorial towers) — abstract suggests no
   prime-moment use; confirm.

## Overall

No claim invalidated; no theorem touched. The paper's three-claims/two-non-claims
architecture survives, and its central novelty — certified exact interval prime sums from an
elementary moment ladder — has no occupant in the searched literature. The review's material
findings were bibliographic (one uncited named source, one wrong author name, one wrong
article number) and positional (the closure pattern has a citable precedent in Johansson;
the rate constant is classical) — all now repaired in the source.
