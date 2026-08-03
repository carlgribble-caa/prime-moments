"""WP9a — the graph universe: the third dictionary column, exact.

The crystal on a finite graph has axes the primitive backtrackless tailless closed
geodesics (up to rotation, with orientation), integer lengths — a lattice crystal.
Its zeta is Ihara's, rational by Bass's theorem:

    zeta_G(u)^(-1) = (1 - u^2)^(|E| - |V|) * det(I - A u + (d-1) u^2 I)     (d-regular)

Checks per graph, all exact integer arithmetic unless stated:
  (1) N_m == tr(T^m): geodesic counts from the Bass polynomial's logarithmic
      derivative equal the traces of the Hashimoto nonbacktracking edge matrix.
  (2) Euler product: Prod_d (1 - u^d)^(pi(d)) reproduces the Bass determinant to u^L,
      where pi(d) (primitive classes) comes from N_m by Moebius inversion —
      the free-monoid (crystal) structure verified directly.
  (3) RH <=> Ramanujan: nontrivial poles on |u| = 1/sqrt(q) exactly when every
      nontrivial adjacency eigenvalue has |lambda| <= 2 sqrt(q)  (float, 1e-7).
      Tested in BOTH directions: four Ramanujan graphs and one non-Ramanujan
      (the circular ladder CL16, spectral radius 2 cos(pi/8) + 1 > 2 sqrt(2)).
  (4) tower exponent: the real solution of zeta_G(e^(-rho)) = 2 (crystal invariant
      of Programme Note 1), reported per graph.

All graphs are 3-regular (q = 2), so the critical circle is |u| = 1/sqrt(2) and the
Ramanujan bound is 2 sqrt(2) = 2.8284... throughout.
"""
import math
from fractions import Fraction

import numpy as np

L = 12  # series/count depth


# ---------- graphs (adjacency matrices, 3-regular) ----------

def K4():
    A = np.ones((4, 4), int) - np.eye(4, dtype=int)
    return "K4", A

def K33():
    A = np.zeros((6, 6), int)
    for i in range(3):
        for j in range(3, 6):
            A[i][j] = A[j][i] = 1
    return "K33", A

def cube():
    A = np.zeros((8, 8), int)
    for i in range(8):
        for b in range(3):
            j = i ^ (1 << b)
            A[i][j] = 1
    return "Q3 cube", A

def petersen():
    A = np.zeros((10, 10), int)
    for i in range(5):
        A[i][(i + 1) % 5] = A[(i + 1) % 5][i] = 1        # outer C5
        A[5 + i][5 + (i + 2) % 5] = A[5 + (i + 2) % 5][5 + i] = 1  # pentagram
        A[i][5 + i] = A[5 + i][i] = 1                     # spokes
    return "Petersen", A

def circular_ladder(n):
    A = np.zeros((2 * n, 2 * n), int)
    for i in range(n):
        A[i][(i + 1) % n] = A[(i + 1) % n][i] = 1
        A[n + i][n + (i + 1) % n] = A[n + (i + 1) % n][n + i] = 1
        A[i][n + i] = A[n + i][i] = 1
    return f"CL{n} ladder", A


# ---------- exact polynomial helpers (python ints / Fractions) ----------

def polymul(a, b, cut=None):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i + j] += x * y
    return out[:cut] if cut else out

def polypow(a, k, cut):
    out = [1]
    for _ in range(k):
        out = polymul(out, a, cut)
    return out

def det_int(M):
    """Bareiss fraction-free determinant of an integer matrix."""
    M = [row[:] for row in M]
    n = len(M)
    sign, prev = 1, 1
    for k in range(n - 1):
        if M[k][k] == 0:
            for i in range(k + 1, n):
                if M[i][k]:
                    M[k], M[i] = M[i], M[k]
                    sign = -sign
                    break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]

def bass_polynomial(A, q):
    """det(I - A u + q u^2 I) as an integer polynomial, by interpolation."""
    n = len(A)
    deg = 2 * n
    xs = list(range(deg + 1))
    ys = []
    for u in xs:
        M = [[(1 + q * u * u if i == j else 0) - A[i][j] * u for j in range(n)]
             for i in range(n)]
        ys.append(det_int(M))
    coeffs = [Fraction(0)] * (deg + 1)
    for i, xi in enumerate(xs):
        num, den = [Fraction(1)], Fraction(1)
        for j, xj in enumerate(xs):
            if j != i:
                num = polymul(num, [Fraction(-xj), Fraction(1)])
                den *= xi - xj
        w = Fraction(ys[i]) / den
        for k, c in enumerate(num):
            coeffs[k] += w * c
    assert all(c.denominator == 1 for c in coeffs), "Bass interpolation non-integer"
    return [int(c) for c in coeffs]

def series_inverse(Z, cut):
    assert Z[0] == 1
    inv = [1] + [0] * (cut - 1)
    for m in range(1, cut):
        inv[m] = -sum(Z[k] * inv[m - k] for k in range(1, min(m, len(Z) - 1) + 1))
    return inv

def geodesic_counts(Z, cut):
    """N_m from -u Z'(u)/Z(u): N_m = sum_k (-k Z_k) inv_{m-k}."""
    inv = series_inverse(Z, cut + 1)
    N = [0] * (cut + 1)
    for m in range(1, cut + 1):
        N[m] = sum(-k * Z[k] * inv[m - k] for k in range(1, min(m, len(Z) - 1) + 1))
    return N

def moebius(n):
    m, res = n, 1
    p = 2
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0:
                return 0
            res = -res
        p += 1
    return -res if m > 1 else res


# ---------- per-graph verification ----------

def hashimoto_traces(A, cut):
    n = len(A)
    dirs = [(i, j) for i in range(n) for j in range(n) if A[i][j]]
    idx = {e: k for k, e in enumerate(dirs)}
    m = len(dirs)
    T = np.zeros((m, m), dtype=np.int64)
    for (u, v) in dirs:
        for w in range(n):
            if A[v][w] and w != u:
                T[idx[(u, v)], idx[(v, w)]] = 1
    tr = [0] * (cut + 1)
    P = np.eye(m, dtype=np.int64)
    for k in range(1, cut + 1):
        P = P @ T
        tr[k] = int(np.trace(P))
    return tr

def check_graph(make):
    name, A = make()
    n = len(A)
    d = int(A.sum(axis=0)[0])
    assert all(int(x) == d for x in A.sum(axis=0)), "not regular"
    q = d - 1
    E = int(A.sum()) // 2

    P = bass_polynomial(A.tolist(), q)
    Z = polymul(P, polypow([1, 0, -1], E - n, len(P) + 2 * (E - n) + 1))
    N = geodesic_counts(Z, L)
    tr = hashimoto_traces(A, L)
    ok_counts = N[1:] == tr[1:]

    # Euler product over primitive geodesic classes
    pi = {}
    for m in range(1, L + 1):
        s = sum(moebius(m // e) * N[e] for e in range(1, m + 1) if m % e == 0)
        assert s % m == 0, "Moebius inversion non-integer"
        pi[m] = s // m
    assert all(v >= 0 for v in pi.values())
    Zrec = [1] + [0] * L
    for m, cnt in pi.items():
        if cnt:
            base = [0] * (L + 1)
            base[0] = 1
            base[m] = -1
            Zrec = polymul(Zrec, polypow(base, cnt, L + 1), L + 1)
    ok_euler = Zrec[:L + 1] == (Z + [0] * L)[:L + 1]

    # RH <=> Ramanujan
    eigs = np.linalg.eigvalsh(A.astype(float))
    nontriv = [l for l in eigs if abs(abs(l) - d) > 1e-8]
    ram = all(abs(l) <= 2 * math.sqrt(q) + 1e-9 for l in nontriv)
    devs = []
    for l in nontriv:
        disc = complex(l * l - 4 * q)
        for root in [(l + disc ** 0.5) / (2 * q), (l - disc ** 0.5) / (2 * q)]:
            devs.append(abs(abs(root) - 1 / math.sqrt(q)))
    on_circle = max(devs) < 1e-7
    ok_rh = on_circle == ram

    # tower exponent: Z(u) = 1/2 on (0, 1/q)
    lo, hi = 0.0, 1.0 / q - 1e-12
    for _ in range(200):
        mid = (lo + hi) / 2
        val = sum(c * mid ** k for k, c in enumerate(Z))
        if val > 0.5:
            lo = mid
        else:
            hi = mid
    rho = -math.log((lo + hi) / 2)

    print(f"{name:12s} n={n:2d} |E|={E:2d} d={d}  Ramanujan={str(ram):5s} "
          f"(max nontrivial |eig| = {max(abs(l) for l in nontriv):.4f} vs 2*sqrt(q) = {2*math.sqrt(q):.4f})")
    for label, ok in [("N_m == tr(T^m), m <= %d" % L, ok_counts),
                      ("Euler product over primitives == Bass determinant", ok_euler),
                      ("RH (poles on |u| = 1/sqrt(q)) <=> Ramanujan", ok_rh)]:
        print(f"    [{'PASS' if ok else 'FAIL'}] {label}")
    print(f"    poles: max deviation from critical circle = {max(devs):.2e} "
          f"({'on' if on_circle else 'OFF'} circle)")
    print(f"    primitive geodesics by length: "
          + " ".join(f"{m}:{pi[m]}" for m in range(3, 9)))
    print(f"    tower exponent rho (zeta_G(e^-rho) = 2): {rho:.6f}")
    return ok_counts and ok_euler and ok_rh, ram

def main():
    print(__doc__.strip().splitlines()[0])
    print(f"series depth L = {L}; all graphs 3-regular, critical circle |u| = 1/sqrt(2)\n")

    # micro-check: K4 has 4 triangles x 2 orientations x 3 starting edges = 24
    _, A = K4()
    assert hashimoto_traces(A, 3)[3] == 24, "K4 triangle count sanity failed"

    allok, rams = True, []
    for make in (K4, K33, cube, petersen, lambda: circular_ladder(16)):
        ok, ram = check_graph(make)
        allok &= ok
        rams.append(ram)
        print()
    both_directions = (not all(rams)) and any(rams)
    print(f"[{'PASS' if both_directions else 'FAIL'}] equivalence exercised in both "
          f"directions (Ramanujan and non-Ramanujan instances present)")
    allok &= both_directions
    print("result:", "ALL PASS" if allok else "FAILURES PRESENT")
    return 0 if allok else 1

if __name__ == "__main__":
    raise SystemExit(main())
