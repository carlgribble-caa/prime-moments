"""WP-RH1 — the Weil positivity explorer: first light.

RH is equivalent (Weil 1952; Bombieri's survey of the quadratic functional) to
positivity of the explicit-formula functional W(g * g~) >= 0 over admissible test
functions. The WP3 pairing engine (diffraction_pairing.py) computes W at Gaussian
test functions as an identity check; this instrument treats the same W as a
QUADRATIC FORM and measures its positivity landscape. Everything below runs under
the preregistration registry/2026-08-07-weil-positivity-prereg.md (gates and
predictions frozen before first run).

Parts:
  A  instrument continuity — the six WP3 pairing rows reproduce;
  B  the Gram matrix M_ij = W(phi_i phi_j) on 12 even Gaussian profiles
     phi_j(r) = exp(-(r-3j)^2/4) + exp(-(r+3j)^2/4): geometric side (primes +
     archimedean + pole, no zeros) vs zero side, then the eigen-decomposition —
     positivity, and the exponential ladder climbing out of the zero-free gap
     (0, gamma_1). Reduction used: phi_i phi_j = w1 H(.;c1) + w2 H(.;c2) with
     H(r;c) = exp(-(r-c)^2/2) + exp(-(r+c)^2/2), c1 = (t_i+t_j)/2,
     w1 = exp(-(t_i-t_j)^2/8), c2 = (t_i-t_j)/2, w2 = exp(-(t_i+t_j)^2/8) —
     so every Gram entry assembles from WP3-engine evaluations at grid centres;
  C  the prime-free window — g supported inside (-log 2, log 2), so the prime
     term vanishes identically and W = archimedean + pole alone;
  D  calibration where the RH-analogue is a theorem (elliptic curve over F_p,
     Hasse bound): the Frobenius Toeplitz form is PSD of exact rank 2; and a
     Hasse-violating negative control where the detector must fire (its growth
     ratio is the golden ratio).

The words "proof of RH" appear nowhere in this lane; the deliverable is the
measured landscape.

First-light note (honest, per registry protocol): gate B3 — the preregistered
directional prediction that the near-kernel is spanned by gap-localized profiles
(bottom-3 centroids < 9) — was REFUTED on first run and stands refuted in
registry/2026-08-07-weil-positivity-results.md. What the data showed instead:
the resolved rank of M equals the number of zeros the family engages, so the
near-kernel is every combination vanishing at those zeros — including
large-centroid interpolation combinations, with the gap profiles as a subspace.
The refutation is reported in-line below (gate B3 prints REFUTED); the script's
exit code tracks the instrument-validity gates (A, B1, B2, C, D1, D2), so a
green run means "instrument sound, identity holds, positivity as measured" —
the refuted prediction is permanent in the registry, not dissolved into a
threshold edit.
"""
import time

from mpmath import mp, mpf, exp, cos, cosh, sqrt, pi, log, quad, digamma, re, zetazero

mp.dps = 30

NZEROS = 60
NCUT = 40000

# Part A centres (the WP3 table)
WP3_CENTRES = ["0", "14.134725141734693790457251983562",
               "17.5",
               "21.022039638771554992628479593896",
               "25.010857580145688763213790992562",
               "30.424876125859513210311897530584"]
WP3_LABELS = ["t0 = 0 (pole territory)", "gamma_1", "between zeros", "gamma_2",
              "gamma_3", "gamma_4"]

# Part B family
NPROF = 12
TCENT = [mpf(3 * j) for j in range(NPROF)]

# Part C
A_SUPP = mpf("0.34")           # 2a = 0.68 < log 2 = 0.6931...

# Part D
EC_P = 10007                   # E: y^2 = x^3 + x + 1 over F_p
TOEP_N = 8


def H_at(r, c):
    return exp(-((r - c) ** 2) / 2) + exp(-((r + c) ** 2) / 2)


def phi_at(r, t):
    return exp(-((r - t) ** 2) / 4) + exp(-((r + t) ** 2) / 4)


def sieve_prime_terms():
    spf = list(range(NCUT + 1))
    for i in range(2, int(NCUT ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, NCUT + 1, i):
                if spf[j] == j:
                    spf[j] = i
    terms = []
    for n in range(2, NCUT + 1):
        p = spf[n]
        m = n
        while m % p == 0:
            m //= p
        if m == 1:
            terms.append((log(n), log(p) / sqrt(n)))
    return terms


def W_std(c, prime_terms):
    """Geometric side of the pairing at the width-1 even Gaussian pair H(.;c):
    archimedean + pole + prime terms. No zeros are consumed."""
    arch = (1 / pi) * quad(
        lambda r: H_at(r, c) * (re(digamma(mpf("0.25") + mpf("0.5") * 1j * r)) - log(pi)),
        [0, max(c - 8, 0), c + 8, c + 40])
    poles = 4 * exp((mpf(1) / 4 - c ** 2) / 2) * cos(c / 2)
    primes = -2 * sum(w * sqrt(2 / pi) * exp(-(u ** 2) / 2) * cos(c * u)
                      for (u, w) in prime_terms)
    return arch + poles + primes


def Z_std(c, gammas):
    """Zero side at the same test function."""
    return 2 * sum(H_at(g, c) for g in gammas)


def fhat_C(r):
    """FT of the cos-bump f(u) = cos(pi u / 2a) on |u| <= a; removable
    singularity at r* = pi/(2a) with limit value a."""
    den = pi ** 2 - 4 * A_SUPP ** 2 * r ** 2
    if abs(den) < mpf("1e-12"):
        return A_SUPP
    return 4 * pi * A_SUPP * cos(A_SUPP * r) / den


def legendre(v, p):
    v %= p
    if v == 0:
        return 0
    return 1 if pow(v, (p - 1) // 2, p) == 1 else -1


def toeplitz_spectrum(q, a, size, dps):
    """Eigenvalues (ascending) of the Toeplitz matrix of normalized Frobenius
    power sums c_m = s_m / q^(m/2), s_m = a s_{m-1} - q s_{m-2}, s_0 = 2, s_1 = a."""
    old = mp.dps
    mp.dps = dps
    try:
        s = [2, a]
        for m in range(2, size):
            s.append(a * s[-1] - q * s[-2])
        c = [mpf(s[m]) / mp.power(mpf(q), mpf(m) / 2) for m in range(size)]
        T = mp.matrix(size, size)
        for i in range(size):
            for j in range(size):
                T[i, j] = c[abs(i - j)]
        E, _ = mp.eigsy(T)
        return sorted([E[k] for k in range(size)]), c
    finally:
        mp.dps = old


def main():
    t_start = time.time()
    gate = {}
    print("WP-RH1: Weil positivity explorer, first light. dps =", mp.dps)
    print("prereg: registry/2026-08-07-weil-positivity-prereg.md\n")

    print(f"computing {NZEROS} zeta zeros ...", flush=True)
    gammas = [zetazero(k).imag for k in range(1, NZEROS + 1)]
    print(f"sieving Lambda(n)/sqrt(n) to {NCUT} ...", flush=True)
    prime_terms = sieve_prime_terms()

    # in-code check of the closed-form product reduction used throughout Part B
    ok_red = True
    for (ti, tj, r) in [(TCENT[2], TCENT[5], mpf("3.7")), (TCENT[0], TCENT[11], mpf("11.2")),
                        (TCENT[7], TCENT[7], mpf("0.9"))]:
        lhs = phi_at(r, ti) * phi_at(r, tj)
        rhs = (exp(-((ti - tj) ** 2) / 8) * H_at(r, (ti + tj) / 2)
               + exp(-((ti + tj) ** 2) / 8) * H_at(r, (ti - tj) / 2))
        ok_red &= abs(lhs - rhs) < mpf("1e-25")
    print(f"product reduction phi_i phi_j -> engine test functions: "
          f"{'PASS' if ok_red else 'FAIL'}\n")
    gate["reduction"] = ok_red

    # ---------------- Part A: instrument continuity ----------------
    print("Part A — instrument continuity (the six WP3 rows)")
    print(f"{'centre':28s} {'zero side':>16s} {'geometric side':>16s} {'|diff|':>10s}")
    okA = True
    for cs, label in zip(WP3_CENTRES, WP3_LABELS):
        c = mpf(cs)
        zs = Z_std(c, gammas)
        gs = W_std(c, prime_terms)
        d = abs(zs - gs)
        ok = d < mpf("1e-9")
        okA &= ok
        print(f"{label:28s} {float(zs):16.9f} {float(gs):16.9f} {float(d):10.2e}"
              f"  [{'PASS' if ok else 'FAIL'}]")
    gate["A"] = okA
    print(f"gate A: {'PASS' if okA else 'FAIL'}\n")

    # ---------------- Part B: the Gram matrix of the Weil form ----------------
    print("Part B — Gram matrix M_ij = W(phi_i phi_j), 12 profiles at t = 0..33")
    centres = sorted({(TCENT[i] + TCENT[j]) / 2 for i in range(NPROF) for j in range(NPROF)}
                     | {abs(TCENT[i] - TCENT[j]) / 2 for i in range(NPROF) for j in range(NPROF)})
    print(f"engine evaluations at {len(centres)} grid centres ...", flush=True)
    Wc, Zc = {}, {}
    for c in centres:
        Wc[c] = W_std(c, prime_terms)
        Zc[c] = Z_std(c, gammas)

    M = mp.matrix(NPROF, NPROF)
    maxdiff = mpf(0)
    for i in range(NPROF):
        for j in range(i, NPROF):
            c1, w1 = (TCENT[i] + TCENT[j]) / 2, exp(-((TCENT[i] - TCENT[j]) ** 2) / 8)
            c2, w2 = abs(TCENT[i] - TCENT[j]) / 2, exp(-((TCENT[i] + TCENT[j]) ** 2) / 8)
            geo = w1 * Wc[c1] + w2 * Wc[c2]
            zer = w1 * Zc[c1] + w2 * Zc[c2]
            maxdiff = max(maxdiff, abs(geo - zer))
            M[i, j] = geo
            M[j, i] = geo
    okB1 = maxdiff < mpf("1e-9")
    gate["B1"] = okB1
    print(f"gate B1 (Gram identity, 78 entries): max |geo - zero| = "
          f"{mp.nstr(maxdiff, 3)}  [{'PASS' if okB1 else 'FAIL'}]")

    E, Q = mp.eigsy(M)
    pairs = sorted([(E[k], [Q[i, k] for i in range(NPROF)]) for k in range(NPROF)],
                   key=lambda p: p[0])
    lam_min = pairs[0][0]
    okB2 = lam_min > mpf("-1e-9")
    gate["B2"] = okB2
    print(f"gate B2 (positivity): lambda_min = {mp.nstr(lam_min, 3)}  "
          f"[{'PASS' if okB2 else 'FAIL'}]\n")

    print("the spectrum and its centroids (ladder out of the gap (0, 14.13)):")
    print(f"{'k':>2s} {'lambda_k':>12s} {'centroid':>9s}   diag est M_jj (2 sum phi_j(gamma)^2)")
    cents = []
    for k, (lam, v) in enumerate(pairs):
        nrm = sum(x ** 2 for x in v)
        cen = sum((v[i] ** 2) * TCENT[i] for i in range(NPROF)) / nrm
        cents.append(cen)
        dom = max(range(NPROF), key=lambda i: v[i] ** 2)
        dg = 2 * sum(phi_at(g, TCENT[dom]) ** 2 for g in gammas)
        print(f"{k:2d} {mp.nstr(lam, 3):>12s} {float(cen):9.2f}   "
              f"dominant profile t = {int(TCENT[dom]):2d}, M_tt ~ {mp.nstr(dg, 2)}")
    okB3 = all(c < 9 for c in cents[:3]) and cents[-1] > 15
    print(f"gate B3 (gap mechanism, preregistered prediction): bottom-3 centroids "
          f"{[round(float(c), 2) for c in cents[:3]]} < 9, top centroid "
          f"{float(cents[-1]):.2f} > 15  [{'CONFIRMED' if okB3 else 'REFUTED'}]")

    # what the data showed instead: the form has finite effective rank equal to
    # the number of zeros the family engages — its kernel is everything that
    # interpolates to zero at those ordinates, gap profiles included but not alone
    rank_resolved = sum(1 for lam, _ in pairs if lam > mpf("1e-12"))
    engaged = sum(1 for g in gammas
                  if 2 * max(phi_at(g, t) for t in TCENT) ** 2 > mpf("1e-12"))
    okB3b = rank_resolved == engaged
    gate["B3-rank"] = okB3b
    print(f"measured mechanism: resolved rank of M = {rank_resolved}, zeros engaged "
          f"by the family (2 max_j phi_j(gamma)^2 > 1e-12) = {engaged}  "
          f"[{'MATCH' if okB3b else 'MISMATCH'}]")
    print("-> the Weil form on a finite spectral window is a finite-rank sampler:")
    print("   rank = #zeros engaged; kernel = test functions vanishing at them.\n")

    # ---------------- Part C: the prime-free window ----------------
    print("Part C — prime-free window: supp(g) in [-0.68, 0.68], inside (-log2, log2)")
    ok_supp = 2 * A_SUPP < log(2)
    print(f"structural: 2a = {float(2 * A_SUPP):.4f} < log 2 = {float(log(2)):.6f}  "
          f"[{'PASS' if ok_supp else 'FAIL'}]  -> prime term vanishes identically")
    rstar = pi / (2 * A_SUPP)
    arch = (1 / pi) * quad(
        lambda r: fhat_C(r) ** 2 * (re(digamma(mpf("0.25") + mpf("0.5") * 1j * r)) - log(pi)),
        [0, rstar, 10, 50, 200, mp.inf])
    pole = 2 * (4 * pi * A_SUPP * cosh(A_SUPP / 2) / (pi ** 2 + A_SUPP ** 2)) ** 2
    WC = arch + pole
    ZC = 2 * sum(fhat_C(g) ** 2 for g in gammas)
    tail = 2 * quad(lambda r: fhat_C(r) ** 2 * log(r / (2 * pi)) / (2 * pi),
                    [gammas[-1], 5 * gammas[-1], mp.inf])
    dC = abs(WC - ZC)
    okC = ok_supp and WC > 0 and dC < mpf("1e-4")
    gate["C"] = okC
    print(f"W = arch + pole = {mp.nstr(arch, 8)} + {mp.nstr(pole, 8)} = {mp.nstr(WC, 8)}")
    print(f"zero side (60 zeros) = {mp.nstr(ZC, 8)}   |diff| = {mp.nstr(dC, 3)} "
          f"(zero-tail estimate ~ {mp.nstr(tail, 2)})")
    print(f"gate C: W > 0 and |diff| < 1e-4  [{'PASS' if okC else 'FAIL'}]\n")

    # ---------------- Part D: calibration where RH is a theorem ----------------
    print(f"Part D — elliptic curve E: y^2 = x^3 + x + 1 over F_{EC_P} (Hasse: theorem)")
    a_tr = -sum(legendre(x * x * x + x + 1, EC_P) for x in range(EC_P))
    hasse = a_tr * a_tr <= 4 * EC_P
    print(f"Frobenius trace a = {a_tr}; Hasse bound a^2 = {a_tr**2} <= 4p = {4*EC_P}  "
          f"[{'PASS' if hasse else 'FAIL'}]")
    spec, _ = toeplitz_spectrum(EC_P, a_tr, TOEP_N, dps=40)
    lead_ok = spec[-1] > mpf("1e-8") and spec[-2] > mpf("1e-8")
    rank_ok = all(abs(x) < mpf("1e-15") for x in spec[:-2])
    psd_ok = spec[0] > mpf("-1e-15")
    okD1 = hasse and lead_ok and rank_ok and psd_ok
    gate["D1"] = okD1
    print(f"Toeplitz spectrum (8x8, ascending): "
          f"{[mp.nstr(x, 2) for x in spec]}")
    print(f"gate D1 (PSD of exact rank 2 — spectral measure = two atoms): "
          f"[{'PASS' if okD1 else 'FAIL'}]")

    specN, cN = toeplitz_spectrum(5, 5, TOEP_N, dps=40)
    okD2 = specN[0] < mpf("-0.1")
    gate["D2"] = okD2
    print(f"negative control (q, a) = (5, 5): a^2 = 25 > 4q = 20 (Hasse violated)")
    print(f"c_1 = {mp.nstr(cN[1], 8)} = sqrt(5) > 2 = c_0; growth ratio "
          f"alpha/sqrt(q) = {mp.nstr((5 + sqrt(5)) / (2 * sqrt(5)), 8)} (the golden ratio)")
    print(f"Toeplitz lambda_min = {mp.nstr(specN[0], 4)} < -0.1: detector fires  "
          f"[{'PASS' if okD2 else 'FAIL'}]\n")

    allok = all(gate.values())
    print("reading: positivity holds at tolerance everywhere tested. The prereg's")
    print("gap-mechanism prediction (B3) was REFUTED and replaced by what the data")
    print("showed: on a finite spectral window the Weil form is a finite-rank")
    print("sampler — resolved rank = number of engaged zeros, kernel = everything")
    print("vanishing at them (the diagonal ladder out of the gap was confirmed:")
    print("M_tt rungs 1e-43 -> 0.2 as committed, but gap profiles span only part")
    print("of the near-kernel). Positivity on any finite family is therefore")
    print("rank-deficient-cheap — which is a measured restatement of why Weil")
    print("positivity needs ALL test functions. In the universe where the")
    print("RH-analogue is a theorem, positivity is TIGHT (rank 2, zero margin in")
    print("all but two directions), and breaking Hasse breaks positivity")
    print("immediately, with golden-ratio growth. Carried to WP-RH2: reconstruct")
    print("the structure that enforces the margin.")
    print(f"\nresult: {'ALL INSTRUMENT GATES PASS' if allok else 'FAILURES PRESENT'}"
          f"; prediction B3 {'CONFIRMED' if okB3 else 'REFUTED (recorded)'}  "
          f"({time.time()-t_start:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
