"""WP4 — symmetry breaking, literally: the primon gas, the Hagedorn point, and the
Bost-Connes order parameter on the bench.

(1) Free gas (Julia): partition function zeta(beta); mean-energy identity
    -zeta'/zeta(beta) = sum Lambda(n) n^(-beta), checked numerically.
(2) Tower gas: Z(beta) = 1/(2 - zeta(beta)) — every ordered factorization a
    microstate. Its Hagedorn point is the crystal's dimension: divergence at
    zeta(rho) = 2, rho = 1.7286... (Kalmar). Checks: thermal sums of the exact
    factorization counts K(n) to 10^6 against 1/(2 - zeta(beta)), with the
    deficit matching the y^rho density-of-states prediction C*rho*N^(rho-beta)
    /(beta-rho); pole residue 1/(-zeta'(rho)) = rho * C with C = -1/(rho zeta'(rho))
    the Kalmar constant of the essay's Section 3 table.
(3) Bost-Connes order parameter: the Gibbs state at inverse temperature beta > 1
    evaluated on the phase observable e(a/b) = exp(2 pi i a/b of the congruence
    point group), computed exactly through Hurwitz zetas:
        phi_beta(e(a/b)) = b^(-beta) sum_{r=1..b} e(2 pi i r a/b) zetaH(beta, r/b) / zeta(beta).
    Frozen limit beta -> infinity: the values are the primitive roots of unity, and
    the Galois group of the cyclotomic field permutes them (the KMS_infinity orbit).
    Symmetry restoration beta -> 1+: the phase expectation falls to 0 — the unique
    high-temperature state is symmetric. The classification theorems (uniqueness for
    beta <= 1, free transitive Galois action on extremal KMS states for beta > 1)
    are Bost and Connes's, cited not reproved; what is machine-checked here is the
    Gibbs-state order parameter they govern.
"""
import time

import numpy as np
from mpmath import mp, mpf, mpc, zeta, exp, cos, sin, pi, findroot, fabs

mp.dps = 25

NK = 10 ** 6      # factorization-count sieve depth
NLAM = 200000     # von Mangoldt check depth


def hurwitz_phase(beta, a, b):
    """phi_beta(e(a/b)) via Hurwitz zetas, exact up to mp precision."""
    num = mpc(0)
    for r in range(1, b + 1):
        num += exp(2j * pi * r * a / b) * zeta(beta, mpf(r) / b)
    return num * mpf(b) ** (-beta) / zeta(beta)


def main():
    t0 = time.time()
    print("primon gas / Bost-Connes checks (WP4). dps =", mp.dps)
    allok = True

    # ---- (1) free gas ----
    print("\n(1) free gas: Z = zeta(beta); mean energy -zeta'/zeta = sum Lambda n^-beta")
    spf = list(range(NLAM + 1))
    for i in range(2, int(NLAM ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, NLAM + 1, i):
                if spf[j] == j:
                    spf[j] = i
    lam_sum = mpf(0)
    for n in range(2, NLAM + 1):
        p, m = spf[n], n
        while m % p == 0:
            m //= p
        if m == 1:
            lam_sum += mp.log(p) * mpf(n) ** (-3)
    truth = -zeta(3, derivative=1) / zeta(3)
    ok = fabs(lam_sum - truth) < mpf("1e-9")
    allok &= ok
    print(f"    beta = 3: |sum_(n<=2e5) - (-zeta'/zeta)| = {float(fabs(lam_sum - truth)):.2e}  "
          f"[{'PASS' if ok else 'FAIL'}]   (free Hagedorn point: the pole at beta = 1)")

    # ---- (2) tower gas ----
    print("\n(2) tower gas: Z = 1/(2 - zeta(beta)); Hagedorn point = crystal dimension")
    rho = findroot(lambda b: zeta(b) - 2, 1.7)
    zprho = zeta(rho, derivative=1)
    C = -1 / (rho * zprho)
    ok = fabs(rho - mpf("1.728647238998")) < mpf("1e-11")
    allok &= ok
    print(f"    rho (zeta(rho) = 2)      = {mp.nstr(rho, 16)}   [{'PASS' if ok else 'FAIL'}]")
    ok = fabs(C - mpf("0.3181736")) < mpf("1e-6")
    allok &= ok
    print(f"    Kalmar constant C = -1/(rho zeta'(rho)) = {mp.nstr(C, 10)}  "
          f"[{'PASS' if ok else 'FAIL'}]  (essay Section 3)")
    print(f"    pole residue 1/(-zeta'(rho)) = {mp.nstr(1 / (-zprho), 10)} = rho * C  "
          f"(thermal residue == counting constant)")
    # residue approach
    b1 = rho + mpf("0.01")
    ratio = (b1 - rho) / (2 - zeta(b1)) * (-zprho)
    ok = fabs(ratio - 1) < mpf("0.02")
    allok &= ok
    print(f"    (beta - rho) * Z(beta) * (-zeta'(rho)) at beta = rho + 0.01: "
          f"{mp.nstr(ratio, 8)}  [{'PASS' if ok else 'FAIL'}]")

    print(f"    sieving ordered-factorization counts K(n) to {NK:,} ...", flush=True)
    K = np.zeros(NK + 1)
    K[1] = 1.0
    for q in range(1, NK // 2 + 1):
        kq = K[q]
        if kq:
            K[2 * q::q][: NK // q - 1] += kq
    # cross-check against the essay's Section-3 tower masses
    G3, G4 = int(K[: 10 ** 3 + 1].sum()), int(K[: 10 ** 4 + 1].sum())
    ok = (G3, G4) == (48614, 2602393)
    allok &= ok
    print(f"    tower masses G(10^3), G(10^4) = {G3:,}, {G4:,}  "
          f"[{'PASS' if ok else 'FAIL'}]  (match essay Section 3 table)")

    n_arr = np.arange(NK + 1, dtype=float)
    n_arr[0] = 1.0
    print(f"    {'beta':>6s} {'Z = 1/(2-zeta)':>15s} {'partial sum':>13s} {'deficit':>10s} "
          f"{'predicted tail':>15s} {'ratio':>7s}")
    for beta in ("2.4", "2.2", "2.0", "1.9"):
        b = mpf(beta)
        Z = 1 / (2 - zeta(b))
        S = float((K[1:] * n_arr[1:] ** (-float(b))).sum())
        deficit = float(Z) - S
        tail = float(C * rho * mpf(NK) ** (rho - b) / (b - rho))
        ratio = deficit / tail
        ok = 0.7 < ratio < 1.4
        allok &= ok
        print(f"    {beta:>6s} {float(Z):15.8f} {S:13.8f} {deficit:10.2e} {tail:15.2e} "
              f"{ratio:7.3f}  [{'PASS' if ok else 'FAIL'}]")
    print("    (deficit tracks the y^rho density-of-states law; the wobble in the ratio")
    print("     is the breathing of the complex dimensions, as in the counting table)")

    # ---- (3) Bost-Connes order parameter ----
    print("\n(3) Bost-Connes order parameter: phi_beta(e(1/3)), exact via Hurwitz zetas")
    print(f"    {'beta':>6s} {'|phi|':>12s}")
    prev = None
    mono = True
    vals = {}
    for beta in ("60", "4", "2", "1.5", "1.2", "1.1", "1.05", "1.01"):
        v = abs(hurwitz_phase(mpf(beta), 1, 3))
        vals[beta] = v
        if prev is not None and v > prev + mpf("1e-20"):
            mono = False
        prev = v
        print(f"    {beta:>6s} {float(v):12.6f}")
    frozen = fabs(hurwitz_phase(mpf(60), 1, 3) - exp(2j * pi / 3))
    ok = frozen < mpf("1e-15")
    allok &= ok
    print(f"    frozen limit: |phi_60(e(1/3)) - e^(2 pi i/3)| = {float(frozen):.1e}  "
          f"[{'PASS' if ok else 'FAIL'}]  (KMS_infinity value = root of unity)")
    ok = vals["1.01"] < mpf("0.02")
    allok &= ok
    print(f"    symmetry restoration: |phi| at beta = 1.01 is {float(vals['1.01']):.4f} < 0.02  "
          f"[{'PASS' if ok else 'FAIL'}]  (unique symmetric state below beta = 1)")
    allok &= mono
    print(f"    order parameter monotone in beta: [{'PASS' if mono else 'FAIL'}]")

    print("    Galois orbit at b = 5, beta -> infinity: the four extremal frozen states")
    orbit_ok = True
    for k in range(1, 5):
        d = fabs(hurwitz_phase(mpf(60), k, 5) - exp(2j * pi * k / 5))
        orbit_ok &= d < mpf("1e-15")
    allok &= orbit_ok
    print(f"    each frozen value = the primitive 5th root e^(2 pi i k/5), k = 1..4  "
          f"[{'PASS' if orbit_ok else 'FAIL'}]  — the orbit Gal(Q(zeta_5)/Q) permutes")

    print("\nclaims: computed here — Gibbs values, order parameter, Hagedorn data.")
    print("cited, not reproved — the KMS classification and the free transitive Galois")
    print("action on extremal states above the transition (Bost-Connes 1995).")
    print(f"\nresult: {'ALL PASS' if allok else 'FAILURES PRESENT'}  ({time.time()-t0:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
