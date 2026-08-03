# Tier 4 verification: exact recovery of interval primes from moments
import sys, math, time
from fractions import Fraction
sys.setrecursionlimit(1000000)

# ---------- Companion I system (prime-free integer moments), embedded ----------
def iroot(y, a):
    if y <= 0: return 0
    if a == 1: return y
    r = int(y ** (1.0/a))
    while r > 0 and r**a > y: r -= 1
    while (r+1)**a <= y: r += 1
    return r

Tmemo, Smemo = {}, {}
def T(k, j, y):
    if y < (1 << k): return 0
    if k == 1:
        if j == 0: return y - 1
        if j == 1: return y*(y+1)//2 - 1
        return sum(n**j for n in range(2, y+1))
    key = (k, j, y)
    v = Tmemo.get(key)
    if v is not None: return v
    dmax = y >> (k-1); tot = 0; d = 2
    while d <= dmax:
        q = y // d; d2 = min(y // q, dmax)
        if j == 0: w = d2 - d + 1
        elif j == 1: w = (d + d2)*(d2 - d + 1)//2
        else: w = sum(t**j for t in range(d, d2+1))
        tot += w * T(k-1, j, q); d = d2 + 1
    Tmemo[key] = tot; return tot

def S(j, y):
    if y < 2: return 0
    key = (j, y); v = Smemo.get(key)
    if v is not None: return v
    L = y.bit_length() - 1
    Pi = Fraction(0)
    for k in range(1, L+1):
        t = T(k, j, y)
        if t: Pi += Fraction((-1)**(k-1), k) * t
    dust = Fraction(0)
    for a in range(2, L+1):
        r = iroot(y, a)
        if r >= 2: dust += Fraction(S(a*j, r), a)
    val = Pi - dust
    assert val.denominator == 1, (j, y)
    Smemo[key] = int(val); return int(val)

def sieve(n):
    bs = bytearray([1])*(n+1); bs[0]=bs[1]=0
    for i in range(2, math.isqrt(n)+1):
        if bs[i]: bs[i*i::i] = b'\x00'*len(bs[i*i::i])
    return [p for p in range(2, n+1) if bs[p]]

# ================= THEOREM 1: integer route (fully prime-free) =================
def route_integer(m):
    n = 2*m
    t0 = time.time()
    r = S(0, n) - S(0, m)
    s = [r] + [S(k, n) - S(k, m) for k in range(1, r+1)]
    e = [1] + [0]*r
    for k in range(1, r+1):
        acc = sum((-1)**(i-1) * e[k-i] * s[i] for i in range(1, k+1))
        assert acc % k == 0, ("Newton divisibility fails", k)
        e[k] = acc // k
    def f(x):  # Horner on sum (-1)^k e_k x^(r-k)
        v = 0
        for k in range(0, r+1): v = v*x + (-1)**k * e[k]
        return v
    rec = [c for c in range(m+1, n+1) if f(c) == 0]
    return r, s, e, rec, time.time()-t0

m = 500
r, s, e, rec, dt = route_integer(m)
true = [p for p in sieve(2*m) if p > m]
print(f"[Route I] m={m}: r={r}, recovered {len(rec)} integers in {dt:.1f}s; matches sieve: {rec == true}")
print(f"[Route I] e_r bit length = {e[r].bit_length()}, total moment bits = {sum(x.bit_length() for x in s)}")
prodN = 1
for p in true: prodN *= p
print(f"[Route I] e_r == prod(window primes): {e[r] == prodN}")

# ================= THEOREM 2: single-moment route (Chebyshev rung 0) =================
from mpmath import mp, mpf, log as mlog, exp as mexp, nint
def route_product(m):
    n = 2*m
    ps_lo = sieve(m)
    mp.prec = int(2.2*m) + 200
    t0 = time.time()
    M0 = mpf(0)
    for i in range(2, n+1): M0 += mlog(i)          # log n!  (anchor)
    for p in ps_lo:                                 # Legendre corrections
        v = 0; pa = p
        while pa <= n: v += n//pa; pa *= p
        M0 -= v*mlog(p)
    N = mexp(M0); Ni = int(nint(N))
    gap = abs(N - Ni)
    rec = [c for c in range(m+1, n+1) if Ni % c == 0]
    return Ni, float(gap), rec, time.time()-t0

Ni, gap, rec2, dt2 = route_product(m)
print(f"[Route II] m={m}: N has {Ni.bit_length()} bits, |exp(M0)-N| = {gap:.1e}, "
      f"recovered {len(rec2)} in {dt2:.1f}s; matches sieve: {rec2 == true}; N==prod: {Ni == prodN}")

# ================= PRONY route at m=50 (2r moments, intermediate precision) =================
import mpmath
def prony(m, prec):
    n = 2*m
    ps_lo = sieve(m)
    rr = S(0, n) - S(0, m)
    mp.prec = prec
    smom = []
    for k in range(0, 2*rr):
        anchor = mpf(0)
        for i in range(2, n+1): anchor += (i**k) * mlog(i)
        corr = mpf(0)
        for p in ps_lo:
            tot = 0; pa = p
            while pa <= n:
                tot += sum((pa*t)**k for t in range(1, n//pa + 1)); pa *= p
            corr += tot*mlog(p)
        smom.append(anchor - corr)
    A = mpmath.matrix(rr, rr); b = mpmath.matrix(rr, 1)
    for i in range(rr):
        for j in range(rr): A[i, j] = smom[i+j]
        b[i] = -smom[rr+i]
    try: c = mpmath.lu_solve(A, b)
    except Exception: return rr, None, None
    coeffs, ok = [], True
    for j in range(rr):
        cj = c[j]; cint = int(nint(cj))
        if abs(cj - cint) > mpf('0.25'): ok = False
        coeffs.append(cint)
    if not ok: return rr, None, None
    def f(x):
        v = 1
        for j in range(rr-1, -1, -1): v = v  # placeholder
        v = x**rr
        for j in range(rr): v += coeffs[j]*x**j
        return v
    recp = [cc for cc in range(m+1, n+1) if f(cc) == 0]
    return rr, coeffs, recp

m2 = 50
true2 = [p for p in sieve(100) if p > 50]
minprec = None
for prec in range(80, 641, 40):
    rr, coeffs, recp = prony(m2, prec)
    if coeffs is not None and recp == true2:
        minprec = prec; break
print(f"[Prony] m={m2}: r={rr}, 2r={2*rr} moments; minimal working precision ~{minprec} bits; recovered = sieve: {recp == true2}")

# ================= accounting table =================
ent = math.log2(math.comb(m, r))   # r-subsets of the m integers in (m, 2m]
print(f"[Accounting] m={m}: entropy log2 C({m},{r}) = {ent:.1f} bits")
print(f"[Accounting] Route I total = {sum(x.bit_length() for x in s)} bits over {r+1} integer moments")
print(f"[Accounting] Route II total = {Ni.bit_length()+2} bits over 1 real moment")
print(f"[Accounting] Prony (m={m2}) = {2*rr} moments x ~{minprec} bits = ~{2*rr*minprec} bits; entropy there = {math.log2(math.comb(m2, rr)):.1f}")
