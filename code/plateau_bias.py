"""WP-RH3c — the plateau bias is a density effect.

WP-RH3b earned, out of sample, the claim that the Jacobi/Krein reconstruction's
plateau is the two-interval equilibrium of the spectral gap, with a systematic
negative bias recorded as observed-but-unclaimed. This instrument tests the
recorded candidate mechanism: the bias is a property of the MEAN DENSITY, not
of the primes — the smooth comb Nbar^{-1}(k - 1/2), same density and no
arithmetic, must reproduce it cell by cell. Confirmation deepens the spec's
negative constraint: even the deviation from the universal limit is
arithmetic-free; the primes are confined to the rigidity-scale residual
fluctuations measured in WP-RH2. A refutation would mean the bias carries
arithmetic beyond density — reported as such, not dissolved.
Runs under registry/2026-08-07-plateau-bias-prereg.md.
"""
import time

import numpy as np
from mpmath import mp, mpf, sqrt, log, pi, zetazero

mp.dps = 30

CONFIGS = [(50, 14, 50), (60, 17, 60)]   # (N, window lo, window hi), frozen


def nbar_mp(E):
    return (E / (2 * pi)) * (log(E / (2 * pi)) - 1) + mpf(7) / 8


def nbar_inv_mp(y):
    lo, hi = 2 * pi * (1 + mpf("1e-12")), mpf(4000)
    for _ in range(160):
        mid = (lo + hi) / 2
        if nbar_mp(mid) < y:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


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


def plateau_means(positions, N, lo, hi):
    atoms = sorted([-g for g in positions[:N]] + list(positions[:N]))
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
    print("WP-RH3c: the plateau bias as a density effect. dps =", mp.dps)
    print("prereg: registry/2026-08-07-plateau-bias-prereg.md\n")

    nmax = max(c[0] for c in CONFIGS)
    print(f"computing {nmax} zeta zeros and the smooth comb ...", flush=True)
    gammas = [zetazero(k).imag for k in range(1, nmax + 1)]
    smooth = [nbar_inv_mp(mpf(k) - mpf(1) / 2) for k in range(1, nmax + 1)]
    g1 = float(gammas[0])

    cells = []
    print(f"{'N':>3s} {'parity':>6s} {'bias(zeros)':>12s} {'bias(smooth)':>13s} "
          f"{'|difference|':>13s}")
    for (N, lo, hi) in CONFIGS:
        gN = float(gammas[N - 1])
        targets = {"odd": (gN + g1) / 2, "even": (gN - g1) / 2}
        mz = dict(zip(("odd", "even"), plateau_means(gammas, N, lo, hi)))
        ms = dict(zip(("odd", "even"), plateau_means(smooth, N, lo, hi)))
        for par in ("odd", "even"):
            bz = mz[par] - targets[par]
            bs = ms[par] - targets[par]
            cells.append((N, par, bz, bs))
            print(f"{N:3d} {par:>6s} {bz:12.3f} {bs:13.3f} {abs(bz - bs):13.3f}")

    okV1 = all(abs(bz - bs) < 1.0 for (_, _, bz, bs) in cells)
    okV2 = all(bs < 0 for (_, _, _, bs) in cells)
    print(f"\ngate V1 (density reproduces the bias, all four |diff| < 1.0): "
          f"[{'PASS' if okV1 else 'FAIL'}]")
    print(f"gate V2 (smooth-comb bias negative in all four): "
          f"[{'PASS' if okV2 else 'FAIL'}]")
    w1 = sum(1 for (_, _, bz, bs) in cells if abs(bz - bs) < 0.5) >= 3
    print(f"W1 (|diff| < 0.5 in >= 3 of 4): {'CONFIRMED' if w1 else 'REFUTED'}")
    ez = [bz for (N, p, bz, _) in cells if p == "even"]
    es = [bs for (N, p, _, bs) in cells if p == "even"]
    w2 = (abs(ez[1]) > abs(ez[0])) == (abs(es[1]) > abs(es[0]))
    print(f"W2 (even-bias growth with N matches between combs): "
          f"{'CONFIRMED' if w2 else 'REFUTED'}")

    allok = okV1 and okV2
    print("\nreading: " + ("the smooth comb — same density, no arithmetic — "
          "reproduces the\nplateau bias cell by cell: the deviation from the "
          "two-interval universal\nis density-driven, so the arithmetic content "
          "of the canonical-system\ndata is confined to the rigidity-scale "
          "residual fluctuations (RH2).\nThe spec's negative constraint deepens: "
          "smoothness accounts for the\ngap, the window, AND the bias; only the "
          "corrections know the primes."
          if allok else "the bias is NOT reproduced by density alone — it "
          "carries content\nbeyond the mean density; escalating up the audit "
          "ladder as committed."))
    print(f"\nresult: {'ALL GATES PASS' if allok else 'FAILURES PRESENT'}  "
          f"({time.time()-t_start:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
