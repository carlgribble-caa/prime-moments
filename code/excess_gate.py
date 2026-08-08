"""WP-C3b — gating the beyond-skeleton excess, out of sample.

C3 measured, post hoc, a beyond-skeleton pairwise excess of 3 micronats —
about 3x the pure chi-square noise floor. This instrument promotes that
bound to a gated claim on the lane's template: the congruence model and
thresholds are frozen in the prereg, and the test runs on two windows never
touched by any prior instrument ([1e8, 2e8) and [2e8, 3e8)). A pass earns,
at MACHINE status: the beyond-skeleton pairwise content of the prime
indicator is <= 1e-5 nats over the full history span at heights to 3e8,
consistent with pure noise — the two-skeleton conjecture at pair level,
gated. Runs under registry/2026-08-08-excess-gate-prereg.md.
"""
import math
import time

import numpy as np
from mpmath import mp, mpf, quad, log as mlog

N_MAX = 3 * 10 ** 8
WINDOWS = [("W_A", 10 ** 8, 2 * 10 ** 8), ("W_B", 2 * 10 ** 8, 3 * 10 ** 8)]
SANITY_GAPS = [2, 6, 30, 210]
SMALLP_GAPS = [2, 4, 6, 8, 10, 12, 30]
I_GAPS = list(range(2, 91, 2))
MODEL_PRIMES = (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
                67, 71, 73, 79, 83, 89)


def sieve(n):
    flags = np.ones(n, dtype=bool)
    flags[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if flags[p]:
            flags[p * p::p] = False
    return flags


def coprime_mask(lo, length):
    pattern = np.array([math.gcd(r, 30) == 1 for r in range(30)], dtype=bool)
    reps = length // 30 + 2
    tiled = np.tile(pattern, reps)
    off = lo % 30
    return tiled[off:off + length]


def singular(d, c2):
    if d % 2:
        return 0.0
    s = 2 * c2
    dd = d
    while dd % 2 == 0:
        dd //= 2
    p = 3
    while p * p <= dd:
        if dd % p == 0:
            s *= (p - 1) / (p - 2)
            while dd % p == 0:
                dd //= p
        p += 2
    if dd > 1:
        s *= (dd - 1) / (dd - 2)
    return s


def main():
    t_start = time.time()
    gate = {}
    print("WP-C3b: gating the beyond-skeleton excess, out of sample.")
    print("prereg: registry/2026-08-08-excess-gate-prereg.md\n")

    print(f"sieving to {N_MAX} ...", flush=True)
    flags = sieve(N_MAX)
    c2 = 1.0
    for p in np.flatnonzero(sieve(10 ** 6)):
        if p > 2:
            c2 *= 1 - 1 / (p - 1) ** 2
    t7 = c2 / ((3 / 4) * (15 / 16))
    mp.dps = 20
    print(f"C2 = {c2:.9f}; T7 = {t7:.6f}  ({time.time()-t_start:.0f}s)\n")

    okV1, okV2 = True, True
    for (name, lo, hi) in WINDOWS:
        win = flags[lo:hi]
        cop = coprime_mask(lo, hi - lo)
        E = float(quad(lambda t: 1 / mlog(t) ** 2, [mpf(lo), mpf(hi)]))
        print(f"{name} = [{lo}, {hi}):")
        for d in SANITY_GAPS:
            P = int(np.count_nonzero(win[:-d] & win[d:]))
            r = P / (singular(d, c2) * E)
            okV1 &= 0.99 <= r <= 1.01
            print(f"  sanity d = {d:3d}: HL ratio {r:.4f}")

        ncop = int(cop.sum())
        rho_c = int(np.count_nonzero(win & cop)) / ncop
        excess, floor_sum, rw_small = 0.0, 0.0, []
        for d in I_GAPS:
            both = cop[:-d] & cop[d:]
            A = int(both.sum())
            n11 = int(np.count_nonzero(win[:-d] & win[d:] & both))
            p1 = int(np.count_nonzero(win[:-d] & both)) / A
            q1 = int(np.count_nonzero(win[d:] & both)) / A
            p11 = n11 / A
            rmod = t7
            for p in MODEL_PRIMES:
                if d % p == 0:
                    rmod *= (p - 1) / (p - 2)
            if d in SMALLP_GAPS:
                rw_small.append(p11 / rho_c ** 2)
            m11 = p1 * q1 * rmod
            cells = [(p11, m11), (p1 - p11, p1 - m11), (q1 - p11, q1 - m11),
                     (1 - p1 - q1 + p11, 1 - p1 - q1 + m11)]
            excess += sum(pm * math.log(pm / me) for (pm, me) in cells
                          if pm > 0 and me > 0)
            floor_sum += 1 / (2 * A)
        spread = max(rw_small) / min(rw_small)
        okV2 &= excess <= 1e-5
        print(f"  excess = {excess:.7f} nats (noise floor ~ {floor_sum:.7f}; "
              f"ratio {excess/floor_sum:.2f})")
        print(f"  X1 (excess in [5e-7, 6e-6]): "
              f"{'CONFIRMED' if 5e-7 <= excess <= 6e-6 else 'REFUTED'}; "
              f"X2 (ratio in [0.5, 6]): "
              f"{'CONFIRMED' if 0.5 <= excess/floor_sum <= 6 else 'REFUTED'}; "
              f"X3 (R_w spread {spread:.4f} <= 1.01): "
              f"{'CONFIRMED' if spread <= 1.01 else 'REFUTED'}\n")

    gate["V1"], gate["V2"] = okV1, okV2
    print(f"gate V1 (HL sanity on fresh windows): [{'PASS' if okV1 else 'FAIL'}]")
    print(f"gate V2 (excess <= 1e-5 nats, both windows): "
          f"[{'PASS' if okV2 else 'FAIL'}]")

    allok = okV1 and okV2
    print("\nreading: " + ("the micronat bound is now gated, out of sample: "
          "the beyond-skeleton\npairwise content of the prime indicator is "
          "<= 1e-5 nats over the full\nhistory span at heights to 3e8, "
          "consistent with pure statistical noise.\nThe two-skeleton "
          "conjecture at pair level holds at MACHINE status — WP6's\nfifth "
          "measured base camp."
          if allok else "the gate failed; measured structure beyond the "
          "congruence model goes\nup the audit ladder as committed."))
    print(f"\nresult: {'ALL GATES PASS' if allok else 'FAILURES PRESENT'}  "
          f"({time.time()-t_start:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
