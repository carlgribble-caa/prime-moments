"""WP-RH3b — the two-interval plateau, out of sample.

Claim under test (provenance in the prereg, stated plainly there: the
hypothesis was read post hoc off the N = 40 reconstruction of WP-RH2/RH3):
the plateau of the Jacobi/Krein reconstruction of the zero comb is the
arithmetic-free two-interval equilibrium of the spectral gap — parity-split
means equal to ((gamma_N + gamma_1)/2, (gamma_N - gamma_1)/2) — so the
leading Hamiltonian structure depends only on the gap and the truncation,
not on where the primes are. Test: the law must PREDICT the plateau of fresh
reconstructions at N = 50 and N = 60, whose targets it has never seen.
Runs under registry/2026-08-07-two-interval-plateau-prereg.md.
"""
import time

import numpy as np
from mpmath import mp, mpf, sqrt, zetazero

mp.dps = 30

CONFIGS = [(50, 14, 50), (60, 17, 60)]   # (N, window lo, window hi), frozen
CONTINUITY_N = (40, 11, 40)              # in-sample, report only


def stieltjes_a(atoms, M):
    npts = len(atoms)
    p_prev = [mpf(0)] * npts
    p_cur = [1 / sqrt(mpf(npts))] * npts
    a_list = []
    for n in range(M - 1):
        xp = [atoms[i] * p_cur[i] for i in range(npts)]
        b_n = sum(xp[i] * p_cur[i] for i in range(npts))
        a_prev = a_list[-1] if a_list else mpf(0)
        r = [xp[i] - b_n * p_cur[i] - a_prev * p_prev[i] for i in range(npts)]
        a_next = sqrt(sum(x * x for x in r))
        a_list.append(a_next)
        p_prev, p_cur = p_cur, [x / a_next for x in r]
    return a_list


def plateau_means(gammas, N, lo, hi):
    atoms = sorted([-g for g in gammas[:N]] + list(gammas[:N]))
    old = mp.dps
    mp.dps = 40
    try:
        a_list = stieltjes_a([mpf(x) for x in atoms], 2 * N)
    finally:
        mp.dps = old
    odd = float(np.mean([float(a_list[n - 1]) for n in range(lo, hi + 1) if n % 2 == 1]))
    even = float(np.mean([float(a_list[n - 1]) for n in range(lo, hi + 1) if n % 2 == 0]))
    return odd, even


def main():
    t_start = time.time()
    print("WP-RH3b: two-interval plateau, out of sample. dps =", mp.dps)
    print("prereg: registry/2026-08-07-two-interval-plateau-prereg.md\n")

    nmax = max(c[0] for c in CONFIGS)
    print(f"computing {nmax} zeta zeros ...", flush=True)
    gammas = [zetazero(k).imag for k in range(1, nmax + 1)]
    g1 = float(gammas[0])

    N, lo, hi = CONTINUITY_N
    odd, even = plateau_means(gammas, N, lo, hi)
    gN = float(gammas[N - 1])
    print(f"continuity (in-sample, NOT a gate): N = {N}, window {lo}..{hi}: "
          f"odd {odd:.3f} vs {(gN+g1)/2:.3f} ({odd-(gN+g1)/2:+.2f}), "
          f"even {even:.3f} vs {(gN-g1)/2:.3f} ({even-(gN-g1)/2:+.2f})\n")

    devs = []
    for (N, lo, hi) in CONFIGS:
        odd, even = plateau_means(gammas, N, lo, hi)
        gN = float(gammas[N - 1])
        t_odd, t_even = (gN + g1) / 2, (gN - g1) / 2
        d_odd, d_even = odd - t_odd, even - t_even
        devs += [(N, "odd", d_odd), (N, "even", d_even)]
        print(f"OUT OF SAMPLE N = {N} (window {lo}..{hi}): "
              f"odd {odd:.3f} vs target {t_odd:.3f} ({d_odd:+.3f}); "
              f"even {even:.3f} vs target {t_even:.3f} ({d_even:+.3f})")

    okT1 = all(abs(d) < 3.0 for (_, _, d) in devs)
    print(f"\ngate T1 (all four |deviations| < 3.0): "
          f"{[round(d, 2) for (_, _, d) in devs]}  [{'PASS' if okT1 else 'FAIL'}]")
    u1 = all(-3.0 <= d < 0 for (_, _, d) in devs)
    print(f"U1 (all deviations in [-3, 0), below equilibrium): "
          f"{'CONFIRMED' if u1 else 'REFUTED'}")
    u2 = all(abs(devs[i][2]) <= abs(devs[i + 1][2]) + 0.5
             for i in range(0, len(devs), 2))
    print(f"U2 (odd deviation <= even, per truncation, tol 0.5): "
          f"{'CONFIRMED' if u2 else 'REFUTED'}")

    print("\nreading: " + ("the two-interval law predicted plateaus it had never "
          "seen — the\nreconstructed Hamiltonian's leading structure is the "
          "arithmetic-free\nuniversal of the gap; the primes live in the "
          "corrections (spec row 6,\nnow MACHINE status)."
          if okT1 else "the out-of-sample prediction FAILED; the N = 40 plateau "
          "reading\nstands recorded as a coincidence of that window."))
    print(f"\nresult: {'ALL GATES PASS' if okT1 else 'FAILURES PRESENT'}  "
          f"({time.time()-t_start:.0f}s)")
    return 0 if okT1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
