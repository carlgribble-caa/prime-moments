"""WP5 — the logic column: the weld as a theorem-triple, walked by machine.

The trichotomy (theorems, cited in the essay):
  bare ruler   (N, +)      DECIDABLE    — Presburger 1929
  bare crystal (N, x)      DECIDABLE    — Skolem 1930 (via per-axis reduction to
                                          ruler questions about exponents)
  the weld     (N, +, x)   UNDECIDABLE  — Goedel 1931 / Church 1936; and fatal
                                          already with bare successor: addition is
                                          definable from S and x (J. Robinson 1949)

Machine content, one demonstration per part:
 (1) Ruler: a decision procedure for Frobenius representability ("is every n > F
     a value of ax + by?") — the Presburger-decidable frontier F = ab - a - b for
     coprime a, b — cross-checked against exhaustive search.
 (2) Crystal: a decision procedure for sentences  E x,y >= 1 : x^i = c y^j,
     decided axiswise (Feferman-Vaught): solvable iff gcd(i, j) | e_p(c) for every
     prime p. Decides the irrationality of sqrt(2) mechanically (the parity of one
     exponent); witnesses constructed for the solvable cases; exhaustive search
     corroborates the refutations the procedure has already proved.
 (3) Weld: Julia Robinson's definitional collapse verified on a finite patch —
     for c != 0:   a + b = c   <=>   S(ac) S(bc) = S(c^2 S(ab)),
     checked at all 226,981 triples a, b, c <= 60. Addition rides in on one tick
     of the ruler; undecidability follows with it.

Also printed: the reverse-mathematics ledger of the trilogy (informal, claims
level), and the mirror caveat — (F_2[t], +, x) is undecidable too (R. Robinson
1951): the logic column separates the structures, not the universes.
"""
import math
import time


def frobenius_check(a, b):
    g = math.gcd(a, b)
    bound = a * b + 50
    reachable = [False] * (bound + 1)
    reachable[0] = True
    for n in range(bound + 1):
        if reachable[n]:
            if n + a <= bound:
                reachable[n + a] = True
            if n + b <= bound:
                reachable[n + b] = True
    if g > 1:
        # decision: misses every n not divisible by g — infinitely many
        ok = all(not reachable[n] for n in range(1, bound + 1) if n % g)
        return None, ok
    frontier = a * b - a - b
    brute = max(n for n in range(bound + 1) if not reachable[n])
    return frontier, brute == frontier


def factorize(c):
    f = {}
    d = 2
    while d * d <= c:
        while c % d == 0:
            f[d] = f.get(d, 0) + 1
            c //= d
        d += 1
    if c > 1:
        f[c] = f.get(c, 0) + 1
    return f


def decide_power_equation(i, c, j):
    """Decide  E x,y >= 1 : x^i = c * y^j  axiswise; return (bool, witness|None)."""
    g = math.gcd(i, j)
    fac = factorize(c)
    if any(e % g for e in fac.values()):
        return False, None
    x = y = 1
    for p, e in fac.items():
        u = 0
        while (i * u - e) % j or i * u < e:
            u += 1
        v = (i * u - e) // j
        x *= p ** u
        y *= p ** v
    return True, (x, y)


def main():
    t0 = time.time()
    print("logic column checks (WP5): ruler decidable, crystal decidable, weld undecidable")
    allok = True

    # (1) ruler
    print("\n(1) ruler (Presburger): Frobenius frontiers, decided then brute-forced")
    for a, b in [(6, 35), (4, 9), (20, 27), (6, 10)]:
        frontier, ok = frobenius_check(a, b)
        allok &= ok
        if frontier is None:
            print(f"    {a}x + {b}y : gcd > 1 — decision: no frontier (misses every "
                  f"non-multiple of {math.gcd(a, b)})  [{'PASS' if ok else 'FAIL'}]")
        else:
            print(f"    {a}x + {b}y : decided frontier = {frontier}; brute-force largest "
                  f"miss agrees  [{'PASS' if ok else 'FAIL'}]")

    # (2) crystal
    print("\n(2) crystal (Skolem via per-axis reduction): decide  E x,y : x^i = c y^j")
    cases = [(2, 2, 2, "sqrt(2) rational?"), (2, 12, 2, "sqrt(12) rational?"),
             (3, 8, 3, "cbrt(8) rational?"), (2, 16, 4, "x^2 = 16 y^4?"),
             (6, 108, 4, "x^6 = 108 y^4?")]
    for i, c, j, label in cases:
        dec, wit = decide_power_equation(i, c, j)
        if dec:
            x, y = wit
            ok = x ** i == c * y ** j
            verdict = f"YES, witness x = {x}, y = {y} (verified exactly)"
        else:
            ok = all((x ** i) % c or round((x ** i / c) ** (1 / j)) ** j * c != x ** i
                     for x in range(1, 2001))
            verdict = "NO (proved axiswise; search to x = 2000 corroborates)"
        allok &= ok
        print(f"    {label:22s} x^{i} = {c} y^{j}: {verdict}  [{'PASS' if ok else 'FAIL'}]")
    print("    (the crystal decides the irrationality of sqrt(2) mechanically;")
    print("     the question 'is x + 1 a square' it cannot even pose)")

    # (3) weld
    print("\n(3) weld (J. Robinson): a + b = c  <=>  S(ac) S(bc) = S(c^2 S(ab)), c != 0")
    bad = 0
    total = 0
    for a in range(61):
        for b in range(61):
            for c in range(61):
                total += 1
                if c == 0:
                    continue
                lhs = a + b == c
                rhs = (a * c + 1) * (b * c + 1) == c * c * (a * b + 1) + 1
                if lhs != rhs:
                    bad += 1
    ok = bad == 0
    allok &= ok
    print(f"    verified at all {total:,} triples a, b, c <= 60: {bad} failures  "
          f"[{'PASS' if ok else 'FAIL'}]")
    print("    (addition is definable from successor and multiplication alone; the")
    print("     full ruler rides in on one tick, and undecidability rides with it)")

    # reverse-mathematics ledger
    print("\nreverse-mathematics ledger of the trilogy (informal, claims level):")
    print("    Companion I  identities        finitary formal algebra (Programme Note 2)")
    print("    Companion I  evaluations       finite arithmetic + Faulhaber; no analysis")
    print("    Companion II moments/sandwich  elementary real analysis (interval bounds,")
    print("                                   Bernstein ellipse); certificates finitary")
    print("    Companion III Thm 1, Thm 3     finitary; kernel-checked in Lean (WP7.H1-H2)")
    print("    Companion III Thm 2            elementary real analysis (exp, rounding)")
    print("mirror caveat: (F_2[t], +, x) is undecidable too (R. Robinson 1951) — the")
    print("logic column separates the structures, not the universes.")

    print(f"\nresult: {'ALL PASS' if allok else 'FAILURES PRESENT'}  ({time.time()-t0:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
