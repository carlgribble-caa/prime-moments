"""Exact checks for Programme Note 2: the crystal engine as a formal logarithm.

Elements of a truncated crystal are exponent vectors over r axes; convolution is
vector splitting; truncation is by dimension Omega <= B, exact for every identity
checked here since all are Omega-graded. No floats, no analytic zeta anywhere.

Check (iii) uses a basis-vector trick: taking ell(m) to be the exponent vector
itself (values in Q^r) verifies Lambda = ell * mu simultaneously for EVERY
Beurling length assignment on r axes.
"""
import itertools
import time
from fractions import Fraction

def elements(r, B):
    """All exponent vectors over r axes with total degree <= B."""
    def rec(i, budget):
        if i == r:
            yield ()
            return
        for a in range(budget + 1):
            for rest in rec(i + 1, budget - a):
                yield (a,) + rest
    return list(rec(0, B))

def subvectors(m):
    """All a with 0 <= a <= m componentwise (the divisors of m)."""
    return [tuple(t) for t in itertools.product(*[range(x + 1) for x in m])]

def vsub(m, a):
    return tuple(x - y for x, y in zip(m, a))

def conv(f, g, elems):
    out = {}
    for m in elems:
        s = None
        for a in subvectors(m):
            fa = f.get(a)
            if fa:
                gb = g.get(vsub(m, a))
                if gb:
                    term = mult(fa, gb)
                    s = term if s is None else add(s, term)
        if s is not None and not is_zero(s):
            out[m] = s
    return out

# values are either Fractions or tuples of Fractions (Q^r-valued); helpers:
def mult(a, b):
    if isinstance(a, tuple):
        return tuple(x * b for x in a)
    if isinstance(b, tuple):
        return tuple(a * y for y in b)
    return a * b

def add(u, v):
    if isinstance(u, tuple):
        return tuple(x + y for x, y in zip(u, v))
    return u + v

def is_zero(v):
    if isinstance(v, tuple):
        return all(x == 0 for x in v)
    return v == 0

def check_crystal(r, B):
    t0 = time.time()
    elems = elements(r, B)
    one = (0,) * r
    zeta = {m: Fraction(1) for m in elems}
    F = {m: Fraction(1) for m in elems if m != one}

    # layers D_k = F^{*k}, k <= B
    D = {1: dict(F)}
    for k in range(2, B + 1):
        D[k] = conv(D[k - 1], F, elems)

    # kappa = log zeta = sum (-1)^{k-1}/k D_k
    kappa = {}
    for k in range(1, B + 1):
        c = Fraction((-1) ** (k - 1), k)
        for m, v in D[k].items():
            kappa[m] = kappa.get(m, Fraction(0)) + c * v
    kappa = {m: v for m, v in kappa.items() if v != 0}

    # (i) engine: kappa = 1/j on axis powers, else 0
    ok_engine = True
    for m in elems:
        nz = [x for x in m if x]
        expect = Fraction(1, nz[0]) if (len(nz) == 1) else Fraction(0)
        if m == one:
            expect = Fraction(0)
        if kappa.get(m, Fraction(0)) != expect:
            ok_engine = False
            break

    # (ii) mu: product formula value vs zeta * mu = delta
    mu = {}
    for m in elems:
        if all(x <= 1 for x in m):
            mu[m] = Fraction((-1) ** sum(m))
    zm = conv(zeta, mu, elems)
    ok_mu = all(zm.get(m, Fraction(0)) == (1 if m == one else 0) for m in elems)

    # (iii) Lambda = ell * mu with basis-valued ell (covers ALL length systems)
    zero_vec = (Fraction(0),) * r
    ell = {m: tuple(Fraction(x) for x in m) for m in elems if m != one}
    lam_expect = {}
    for m in elems:
        nz = [(i, x) for i, x in enumerate(m) if x]
        if len(nz) == 1:
            i = nz[0][0]
            lam_expect[m] = tuple(Fraction(1 if j == i else 0) for j in range(r))
    lm = conv(ell, mu, elems)
    ok_twin = all(lm.get(m, zero_vec) == lam_expect.get(m, zero_vec) for m in elems)

    # (iv) exp(kappa) = zeta at truncation
    expk = {one: Fraction(1)}
    power = {one: Fraction(1)}
    fact = 1
    for k in range(1, B + 1):
        power = conv(power, kappa, elems)
        fact *= k
        for m, v in power.items():
            expk[m] = expk.get(m, Fraction(0)) + v / fact
    ok_exp = all(expk.get(m, Fraction(0)) == 1 for m in elems)

    dt = time.time() - t0
    print(f"  crystal r={r} axes, Omega<={B}  ({len(elems)} elements, {dt:.1f}s)")
    for name, ok in [("engine kappa=1/j on axis powers", ok_engine),
                     ("mu product formula & mu*zeta=delta", ok_mu),
                     ("Lambda = ell*mu (all length systems at once)", ok_twin),
                     ("exp(kappa) = zeta", ok_exp)]:
        print(f"    [{'PASS' if ok else 'FAIL'}] {name}")
    return ok_engine and ok_mu and ok_twin and ok_exp

def check_integers(N):
    """(v) kappa at C_Z for n <= N by integer Dirichlet convolution, vs oracle."""
    t0 = time.time()
    Dk = [0] * (N + 1)
    for n in range(2, N + 1):
        Dk[n] = 1                       # D_1
    kappa = [Fraction(0)] * (N + 1)
    k = 1
    while any(Dk[2:]):
        c = Fraction((-1) ** (k - 1), k)
        for n in range(2, N + 1):
            if Dk[n]:
                kappa[n] += c * Dk[n]
        nxt = [0] * (N + 1)             # D_{k+1} = D_k * F
        for n in range(2, N + 1):
            if Dk[n]:
                for d in range(2, N // n + 1):
                    nxt[n * d] += Dk[n]
        Dk = nxt
        k += 1
    spf = list(range(N + 1))
    for i in range(2, int(N ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i
    ok = True
    for n in range(2, N + 1):
        m, p = n, spf[n]
        j = 0
        while m % p == 0:
            m //= p
            j += 1
        expect = Fraction(1, j) if m == 1 else Fraction(0)
        if kappa[n] != expect:
            ok = False
            break
    print(f"  C_Z truncation n<={N}  ({time.time() - t0:.1f}s)")
    print(f"    [{'PASS' if ok else 'FAIL'}] kappa(n) matches Lambda(n)/log n support & values")
    return ok

def main():
    print("formal engine checks (Programme Note 2): exact, no floats, no analytic zeta")
    allok = True
    for r, B in [(4, 9), (6, 6), (1, 40)]:
        allok &= check_crystal(r, B)
    allok &= check_integers(3000)
    print("result:", "ALL PASS" if allok else "FAILURES PRESENT")
    return 0 if allok else 1

if __name__ == "__main__":
    raise SystemExit(main())
