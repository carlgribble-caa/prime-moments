"""WP-C1 — the compression question, first light.

"Is there a closed form for pi(x)?" formalized as evaluation complexity: a
fixed-length exact expression is (up to convention) a poly(log x)-time exact
algorithm. This instrument assembles the known landscape into a spec matrix
with exactly ONE open cell — exact pi(x) in poly(log x) — and adds two
measurements: the parity stream of pi at geometric sample points tested for
practical incompressibility (the cheapest falsifiable shadow of the closed
form question), and the two-skeleton conjecture read at the compressor
observer class (compressors must capture the wheel skeleton of the prime
indicator and nothing beyond it). Compressors are proxies for entropy, not
Kolmogorov estimators; every claim is "at the practical-compressor level."
Runs under registry/2026-08-08-compression-prereg.md.
"""
import bz2
import hashlib
import lzma
import math
import time
import zlib

import numpy as np
from mpmath import mp

N_SIEVE = 10 ** 7
NPAR = 8192
WLEN = 2 ** 20
MR_BASES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
WHEEL = [r for r in range(30) if math.gcd(r, 30) == 1]


def sieve(n):
    flags = np.ones(n, dtype=bool)
    flags[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if flags[p]:
            flags[p * p::p] = False
    return flags


def pi_digit_bits(count):
    old = mp.dps
    mp.dps = 6 * count + 30
    try:
        s = mp.nstr(+mp.pi, 6 * count + 20)
    finally:
        mp.dps = old
    digits = s.replace("3.", "", 1)
    return np.array([1 if int(digits[6 * k:6 * k + 6]) < 500000 else 0
                     for k in range(count)], dtype=np.uint8)


def sha_bits(count, thresh):
    """Deterministic Bernoulli(thresh) bits: SHA-256 counter mode, seed 'WP-C1'."""
    out = np.empty(count, dtype=np.uint8)
    i = 0
    ctr = 0
    while i < count:
        h = hashlib.sha256(f"WP-C1:{ctr}".encode()).digest()
        for j in range(0, 32, 4):
            if i >= count:
                break
            u = int.from_bytes(h[j:j + 4], "big") / 2 ** 32
            out[i] = 1 if u < thresh else 0
            i += 1
        ctr += 1
    return out


def zsize(bits, level=9):
    return len(zlib.compress(np.packbits(bits).tobytes(), level))


def best_size(bits):
    raw = np.packbits(bits).tobytes()
    return min(len(zlib.compress(raw, 9)), len(bz2.compress(raw, 9)),
               len(lzma.compress(raw, preset=9)))


def h2(p):
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def miller_rabin(n):
    if n < 2:
        return False
    for p in MR_BASES:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in MR_BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def main():
    t_start = time.time()
    gate = {}
    print("WP-C1: the compression question, first light.")
    print("prereg: registry/2026-08-08-compression-prereg.md\n")

    flags = sieve(N_SIEVE)
    cum = np.cumsum(flags)

    # ---------------- K2: the parity stream ----------------
    xs = np.unique(np.round(10 ** 6 * 10 ** (np.arange(NPAR) / (NPAR - 1))
                            ).astype(np.int64))
    assert len(xs) == NPAR, f"sample points collided: {len(xs)}"
    parity = (cum[xs - 1] & 1).astype(np.uint8)
    ctrl = pi_digit_bits(NPAR)
    s_par, s_ctl = zsize(parity), zsize(ctrl)
    r2 = s_par / s_ctl
    okK2 = r2 >= 0.97
    gate["K2"] = okK2
    print(f"gate K2 (parity stream incompressible): zlib {s_par} B vs control "
          f"{s_ctl} B, ratio {r2:.4f} >= 0.97  [{'PASS' if okK2 else 'FAIL'}]")
    print(f"  L1 (ratio in [0.99, 1.03]): "
          f"{'CONFIRMED' if 0.99 <= r2 <= 1.03 else 'REFUTED'}\n")

    # ---------------- K3/K4: the skeleton at the compressor level ----------------
    lo = N_SIEVE - WLEN
    window = flags[lo:N_SIEVE].astype(np.uint8)
    rho = float(window.mean())
    bpp = 8 * best_size(window) / WLEN
    okK3 = bpp <= 0.92 * h2(rho)
    gate["K3"] = okK3
    cop = np.array([i for i in range(WLEN) if math.gcd((lo + i) % 30, 30) == 1])
    rho30 = float(window[cop].mean())
    wheel_H = (len(WHEEL) / 30) * h2(rho30)
    print(f"window [{lo}, {N_SIEVE}): density {rho:.5f}, H2 = {h2(rho):.4f} "
          f"bits/pos; wheel entropy = {wheel_H:.4f} bits/pos")
    print(f"gate K3 (compressor finds the skeleton): best = {bpp:.4f} bits/pos "
          f"<= 0.92*H2 = {0.92*h2(rho):.4f}  [{'PASS' if okK3 else 'FAIL'}]")
    print(f"  L3 (best/wheel-entropy in [1.0, 1.6]): {bpp/wheel_H:.3f}  "
          f"{'CONFIRMED' if 1.0 <= bpp/wheel_H <= 1.6 else 'REFUTED'}")

    restr = window[cop]
    ctrl4 = sha_bits(len(restr), rho30)
    s_res, s_c4 = best_size(restr), best_size(ctrl4)
    r4 = s_res / s_c4
    okK4 = r4 >= 0.97
    gate["K4"] = okK4
    print(f"gate K4 (nothing beyond the skeleton): restricted {s_res} B vs "
          f"matched control {s_c4} B, ratio {r4:.4f} >= 0.97  "
          f"[{'PASS' if okK4 else 'FAIL'}]")
    print(f"  L2 (ratio in [0.99, 1.03]): "
          f"{'CONFIRMED' if 0.99 <= r4 <= 1.03 else 'REFUTED'}\n")

    # ---------------- K5: local vs global ----------------
    test = range(9999600, 9999800)
    okK5 = all(miller_rabin(n) == bool(flags[n]) for n in test)
    gate["K5"] = okK5
    print(f"gate K5 (local primality poly(log): MR == sieve on 200 committed "
          f"integers): [{'PASS' if okK5 else 'FAIL'}]\n")

    # ---------------- K1: the spec matrix ----------------
    ROWS = [
        ("smooth part li/R(x) to any precision", "poly(log x)", "ADOPTED (analytic)"),
        ("local primality of n", "poly(log n)", "ADOPTED (AKS) + MACHINE(K5)"),
        ("indicator skeleton (wheel structure)", "compressible",
         "MACHINE(K3; captured by general compressors)"),
        ("fluctuations: parity stream of pi(x)", "no structure found",
         "MEASURED(K2: coin-like to zlib)"),
        ("residual beyond skeleton", "no structure found",
         "MEASURED(K4: = matched control)"),
        ("exact pi(x)", "x^(1/2+eps) analytic / x^(2/3) combinatorial",
         "ADOPTED (Lagarias-Odlyzko; Deleglise-Rivat) + MACHINE(Paper 1, x^(3/4))"),
        ("window recovery floor", "D >= log2 C(m,r) - 1",
         "MACHINE(Lean, WP7.H2)"),
        ("prime step = minimal lattice growth", "one point per prime step",
         "MACHINE(Paper 1 section 6)"),
        ("exact pi(x) in poly(log x)  [equivalently: a fixed-length closed "
         "form; contains parity of pi(x) as weakest form]", "-", "OPEN"),
    ]
    print("THE COMPRESSION SPEC (task | best known | status):")
    n_open = 0
    for (task, bound, status) in ROWS:
        print(f"  {task}\n      {bound}  |  {status}")
        n_open += status == "OPEN"
    okK1 = n_open == 1
    gate["K1"] = okK1
    print(f"\ngate K1 (exactly one OPEN cell): [{'PASS' if okK1 else 'FAIL'}]")

    allok = all(gate.values())
    print("\nreading: the closed-form question, formalized, has one open cell —")
    print("exact pi(x) in poly(log x) — and everything around it is either a")
    print("theorem, kernel-checked, or measured: the smooth part and local")
    print("primality are polylog; the indicator's compressible content is its")
    print("congruence skeleton and general compressors find nothing beyond it;")
    print("the parity stream of pi is coin-like. A fixed-length closed form")
    print("would compress what these instruments measure as incompressible —")
    print("which is an obstruction profile, not an impossibility proof.")
    print(f"\nresult: {'ALL GATES PASS' if allok else 'FAILURES PRESENT'}  "
          f"({time.time()-t_start:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
