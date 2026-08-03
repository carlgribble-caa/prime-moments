"""WP8 — the frontier door: what characteristic zero retains of Frobenius.

(1) The integers' canonical lambda-ring structure has Adams operations psi^p = id,
    and the Frobenius-lift condition psi^p(n) = n^p (mod p) is exactly Fermat's
    little theorem — verified on a patch. The "missing symmetry" of the essay's
    final thesis survives in characteristic zero as this congruence: the ghost of
    Frobenius. (Borger's programme takes commuting Frobenius lifts as the very
    definition of descent to the absolute point.)
(2) Witt vectors make the ghost load-bearing: the addition and multiplication laws
    of W_2 and W_3 demand divisions by p and p^2 that always clear (verified
    exactly on random big integers, several primes), and the ghost map turns the
    crystal-blind Witt sum into componentwise arithmetic.
"""
import random
import time


def ghost2(p, a):
    return (a[0], a[0] ** p + p * a[1])


def witt_sum2(p, a, b):
    s0 = a[0] + b[0]
    num = a[0] ** p + b[0] ** p - s0 ** p
    assert num % p == 0, "Witt sum divisibility failed"
    return (s0, a[1] + b[1] + num // p)


def witt_mul2(p, a, b):
    return (a[0] * b[0], a[0] ** p * b[1] + b[0] ** p * a[1] + p * a[1] * b[1])


def witt_sum3(p, a, b):
    # solve ghost equations successively; Witt's theorem = the divisions clear
    w = [ga + gb for ga, gb in zip(ghost3(p, a), ghost3(p, b))]
    s0 = w[0]
    n1 = w[1] - s0 ** p
    assert n1 % p == 0
    s1 = n1 // p
    n2 = w[2] - s0 ** (p * p) - p * s1 ** p
    assert n2 % (p * p) == 0
    return (s0, s1, n2 // (p * p))


def ghost3(p, a):
    return (a[0], a[0] ** p + p * a[1],
            a[0] ** (p * p) + p * a[1] ** p + p * p * a[2])


def main():
    t0 = time.time()
    print("Witt / Frobenius-shadow checks (WP8)")
    rng = random.Random(20260803)

    ok = all(pow(n, p, p) == n % p
             for p in [q for q in range(2, 51) if all(q % r for r in range(2, q))]
             for n in range(1, 2001))
    print(f"  [{'PASS' if ok else 'FAIL'}] Fermat as Frobenius-lift condition: "
          f"psi^p(n) = n^p (mod p), all p <= 50, n <= 2000")
    allok = ok

    for p in (2, 3, 5, 7, 11):
        ok = True
        for _ in range(400):
            a = (rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6))
            b = (rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6))
            s = witt_sum2(p, a, b)          # asserts divisibility
            m = witt_mul2(p, a, b)
            ga, gb = ghost2(p, a), ghost2(p, b)
            ok &= ghost2(p, s) == (ga[0] + gb[0], ga[1] + gb[1])
            ok &= ghost2(p, m) == (ga[0] * gb[0], ga[1] * gb[1])
        allok &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] W_2 at p = {p}: denominators clear; "
              f"ghost map is a ring homomorphism (400 random pairs)")

    for p in (2, 3, 5):
        ok = True
        for _ in range(300):
            a = tuple(rng.randint(-10**4, 10**4) for _ in range(3))
            b = tuple(rng.randint(-10**4, 10**4) for _ in range(3))
            s = witt_sum3(p, a, b)          # asserts /p and /p^2 divisibility
            ok &= ghost3(p, s) == tuple(x + y for x, y in zip(ghost3(p, a), ghost3(p, b)))
        allok &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] W_3 at p = {p}: divisions by p and p^2 "
              f"clear; ghost additivity (300 random pairs)")

    print("\nreading: the mirror's engine (Frobenius) survives in characteristic zero")
    print("as a congruence and a divisibility — the lambda-ring shadow that Borger's")
    print("programme takes as the descent datum to the absolute point.")
    print(f"result: {'ALL PASS' if allok else 'FAILURES PRESENT'}  ({time.time()-t0:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
