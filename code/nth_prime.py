"""The n-th prime, worked out exactly: li-inverse seed + bisection on the
prime-free counting engine of Paper 1.

Demonstration script (no preregistration — it makes no new claims; it
exercises Paper 1's machinery in inverse mode). Given a position n:

  1. seed  x0 = li^{-1}(n)      (the smooth, arithmetic-free position);
  2. bracket and bisect on S_0 (the Linnik-based exact pi(x), no prime
     input anywhere) until the unique x with pi(x) = n, pi(x-1) = n-1;
  3. verify the answer against an independent sieve.

The demo also prints the smooth-position error — the displacement field of
the primes, i.e. the fluctuation term the WP-RH lane measured — so the
structure "cheap smooth part + zero-driven correction + exact finishing" is
visible in the output.
"""
import math
import time

import numpy as np
from mpmath import mp, li, mpf, findroot

from prime_sum_formula import S, _as_int

mp.dps = 30

POSITIONS = [100, 1000, 10000, 78498, 100000, 664579]


def li_inverse(n):
    x = mpf(max(n, 3)) * (math.log(max(n, 3)) + math.log(math.log(max(n, 6))))
    return float(findroot(lambda t: li(t) - n, x))


def pi_exact(x):
    return _as_int(S(0, int(x)))


def sieve_nth(nmax_prime_bound, positions):
    flags = np.ones(nmax_prime_bound, dtype=bool)
    flags[:2] = False
    for p in range(2, int(nmax_prime_bound ** 0.5) + 1):
        if flags[p]:
            flags[p * p::p] = False
    primes = np.flatnonzero(flags)
    return {n: int(primes[n - 1]) for n in positions}


def nth_prime(n, verbose=True):
    t0 = time.time()
    seed = li_inverse(n)
    lo = int(seed * 0.9)
    hi = int(seed * 1.1) + 10
    evals = 0
    while pi_exact(hi) < n:
        hi = int(hi * 1.1)
        evals += 1
    while pi_exact(lo) >= n:
        lo = int(lo * 0.9)
        evals += 1
    evals += 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        evals += 1
        if pi_exact(mid) >= n:
            hi = mid
        else:
            lo = mid
    if verbose:
        print(f"  n = {n:8d}: seed li^-1(n) = {seed:12.1f}  ->  p_n = {hi}"
              f"   (displacement {hi - seed:+9.1f}; {evals} formula evals, "
              f"{time.time()-t0:.1f}s)")
    return hi


def main():
    t_start = time.time()
    print("The n-th prime, exactly, from the prime-free formula engine")
    print("(seed = smooth inverse; finish = bisection on Paper 1's S_0):\n")
    computed = {n: nth_prime(n) for n in POSITIONS}
    truth = sieve_nth(10 ** 7 + 10 ** 5, POSITIONS)
    ok = all(computed[n] == truth[n] for n in POSITIONS)
    print("\nindependent sieve verification: "
          + ("ALL MATCH" if ok else f"MISMATCH: {computed} vs {truth}"))
    print(f"\nreading: position -> prime is computed exactly, with no prime")
    print("input, in ~log(x) formula evaluations from the smooth seed. The")
    print("printed displacements are the prime-side fluctuation field — the")
    print("zero-driven term; that it must be computed (bisection) rather than")
    print("written in fixed length is exactly the compression lane's OPEN cell.")
    print(f"\nresult: {'ALL PASS' if ok else 'FAILURES PRESENT'}  "
          f"({time.time()-t_start:.0f}s)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
