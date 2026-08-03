"""Prime sums over arbitrary intervals from the inductive U-space formula system.

Three lines of mathematics, no primality tests anywhere:
  base:  T_1^(j)(y) = sum_{n=2..y} n^j                       (Faulhaber)
  step:  T_k^(j)(y) = sum_{d=2..y/2^(k-1)} d^j T_{k-1}^(j)(y//d)
  extract: S_j(y) = sum_k (-1)^(k-1)/k T_k^(j)(y) - sum_{a>=2} (1/a) S_{a j}(floor(y^(1/a)))
Then  sum of primes in (A,B] = S_1(B) - S_1(A);  count = S_0(B) - S_0(A).
"""
import time, random, sys
from fractions import Fraction
import numpy as np

sys.setrecursionlimit(100000)
SMALL = 512

def iroot(n, a):
    r = int(round(n ** (1.0 / a)))
    while r ** a > n: r -= 1
    while (r + 1) ** a <= n: r += 1
    return r

def F(j, m):
    if m <= 0: return 0
    if j == 0: return m
    if j == 1: return m * (m + 1) // 2
    return sum(n ** j for n in range(1, m + 1))

memoT, memoS = {}, {}

def T(k, j, y):
    if y < (1 << k): return 0
    key = (k, j, y)
    if key in memoT: return memoT[key]
    if k == 1:
        v = F(j, y) - 1
    elif y <= SMALL or j > 1:
        v = 0
        for d in range(2, (y >> (k - 1)) + 1):
            v += d ** j * T(k - 1, j, y // d)
    else:
        v, d, dmax = 0, 2, y >> (k - 1)
        while d <= dmax:
            q = y // d
            d2 = min(y // q, dmax)
            v += (F(j, d2) - F(j, d - 1)) * T(k - 1, j, q)
            d = d2 + 1
    memoT[key] = v
    return v

def S(j, y):
    if y < 2: return Fraction(0)
    key = (j, y)
    if key in memoS: return memoS[key]
    c = sum(Fraction((-1) ** (k - 1), k) * T(k, j, y) for k in range(1, y.bit_length()))
    a = 2
    while (1 << a) <= y:
        c -= Fraction(1, a) * S(a * j, iroot(y, a))
        a += 1
    memoS[key] = c
    return c

def _as_int(x):
    assert x.denominator == 1, f"non-integer result: {x}"
    return int(x)

def prime_sum(A, B):   return _as_int(S(1, B) - S(1, A))
def prime_count(A, B): return _as_int(S(0, B) - S(0, A))

def main():
    M = 10 ** 7
    print(f"building sieve oracle to {M:,} ...")
    sv = np.ones(M + 1, bool); sv[:2] = False
    for i in range(2, int(M ** 0.5) + 1):
        if sv[i]: sv[i * i::i] = False
    Pc = np.cumsum(np.where(sv, np.arange(M + 1, dtype=np.int64), 0))
    Cc = np.cumsum(sv)
    oracle_sum = lambda A, B: int(Pc[B] - Pc[A])
    oracle_cnt = lambda A, B: int(Cc[B] - Cc[A])

    passed = failed = 0
    def check(label, got, want, t):
        nonlocal passed, failed
        ok = (got == want)
        passed += ok; failed += (not ok)
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:<28} formula = {got:<16} sieve = {want:<16} ({t:.2f}s)")

    print("\n1. dyadic windows (2^(j-1), 2^j], sums:")
    for jj in range(1, 21):
        A, B = 1 << (jj - 1), 1 << jj
        t0 = time.time(); got = prime_sum(A, B)
        check(f"({A}, {B}]", got, oracle_sum(A, B), time.time() - t0)

    print("\n2. edge cases, sums:")
    for A, B in [(500, 500), (113, 126), (12, 13), (1020, 1030), (1, 2)]:
        t0 = time.time(); got = prime_sum(A, B)
        check(f"({A}, {B}]", got, oracle_sum(A, B), time.time() - t0)

    print("\n3. random intervals in [1, 10^6], sums:")
    rng = random.Random(42)
    for _ in range(8):
        A = rng.randint(1, 10 ** 6 - 1); B = rng.randint(A + 1, 10 ** 6)
        t0 = time.time(); got = prime_sum(A, B)
        check(f"({A}, {B}]", got, oracle_sum(A, B), time.time() - t0)

    print("\n4. prime counts (weight j = 0):")
    for A, B in [(1, 100), (512, 1024), (1234, 5678), (113, 126), (1, 10 ** 6)]:
        t0 = time.time(); got = prime_count(A, B)
        check(f"count ({A}, {B}]", got, oracle_cnt(A, B), time.time() - t0)

    print("\n5. grand finale:")
    for A, B in [(10 ** 6, 10 ** 7), (1, 10 ** 7)]:
        t0 = time.time(); got = prime_sum(A, B)
        check(f"({A}, {B}]", got, oracle_sum(A, B), time.time() - t0)

    lat = len({k[2] for k in memoT})
    print(f"\nresult: {passed} passed, {failed} failed; evaluation lattice touched {lat} points")

if __name__ == "__main__":
    main()
