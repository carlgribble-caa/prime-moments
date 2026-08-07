"""WP-RH — uncertainty quantification for the transfer-law measurements.

Deterministic block-jackknife (no RNG, per repo discipline) for the quantities
the paper quotes: the gated per-window slope ratios, the fitted law constant
a, and the pooled overtone deviations. This script makes NO new claims and
runs under no preregistration: it quantifies the precision of measurements
already recorded in the registry (RH4b/RH5/RH7). Method: split each window
into 5 contiguous blocks; delete-one-block refits; jackknife standard error
SE = sqrt((B-1)/B * sum (theta_b - mean)^2).
"""
import math
import time

import numpy as np
from mpmath import mp, zetazero

mp.dps = 30

BAT = [2, 3, 4, 5, 7, 8, 9, 11, 13, 25, 27]
GATED = [2, 3, 5, 7]
WINDOWS = [(1, 60), (141, 200), (301, 400), (401, 500)]
NBLOCKS = 5
A_REC = 1.1416


def lam(m):
    s = min(p for p in range(2, m + 1) if m % p == 0)
    return math.log(s)


def beta_pred(m):
    return lam(m) / (math.pi * math.sqrt(m) * math.log(m))


def nbar(E):
    return (E / (2 * math.pi)) * (math.log(E / (2 * math.pi)) - 1) + 0.875


def rho(E):
    return math.log(E / (2 * math.pi)) / (2 * math.pi)


def ratios(gam, ks_list):
    ks = np.array(ks_list)
    g = np.array([gam[k - 1] for k in ks])
    y = np.array([nbar(v) for v in g]) - (ks - 0.5)
    kt = (ks - ks.mean()) / (ks.max() - ks.min())
    cols = [np.sin(g * math.log(m)) for m in BAT] + [np.ones_like(kt), kt, kt ** 2]
    b, *_ = np.linalg.lstsq(np.vstack(cols).T, y, rcond=None)
    rw = float(np.mean([rho(v) for v in g]))
    return {m: b[i] / beta_pred(m) for i, m in enumerate(BAT)}, rw


def blocks(klo, khi):
    ks = list(range(klo, khi + 1))
    size = len(ks) // NBLOCKS
    return [ks[i * size:(i + 1) * size] if i < NBLOCKS - 1 else ks[i * size:]
            for i in range(NBLOCKS)]


def jackknife(vals):
    v = np.array(vals)
    return float(np.sqrt((len(v) - 1) / len(v) * np.sum((v - v.mean()) ** 2)))


def fit_a(points):
    t2 = np.array([t ** 2 for (t, T) in points])
    nl = np.array([-math.log(max(T, 1e-6)) for (t, T) in points])
    return float(np.sum(t2 * nl) / np.sum(t2 ** 2))


def main():
    t_start = time.time()
    print("WP-RH uncertainty quantification: block jackknife (deterministic).")
    print("computing 500 zeta zeros ...", flush=True)
    gam = [float(zetazero(k).imag) for k in range(1, 501)]

    # per-window gated slope SEs
    full, rws, win_blocks = [], [], []
    for (klo, khi) in WINDOWS:
        r, rw = ratios(gam, list(range(klo, khi + 1)))
        full.append(r)
        rws.append(rw)
        win_blocks.append(blocks(klo, khi))
    print("\nper-window gated ratios with jackknife SEs:")
    print(f"{'window':>10s} " + " ".join(f"{'m='+str(m):>14s}" for m in GATED))
    jk_store = []
    for wi, (klo, khi) in enumerate(WINDOWS):
        ks_all = list(range(klo, khi + 1))
        reps = []
        for bl in win_blocks[wi]:
            keep = [k for k in ks_all if k not in bl]
            r, _ = ratios(gam, keep)
            reps.append(r)
        jk_store.append(reps)
        row = " ".join(
            f"{full[wi][m]:+.3f}±{jackknife([r[m] for r in reps]):.3f}"
            for m in GATED)
        print(f"{klo:>4d}..{khi:<4d} {row}")

    # SE of the fitted constant a (fit windows 1-2, as recorded in RH5)
    def a_from(r1, rw1, r2, rw2):
        pts = [(math.log(m) / (2 * math.pi * rw1), r1[m]) for m in GATED] + \
              [(math.log(m) / (2 * math.pi * rw2), r2[m]) for m in GATED]
        return fit_a(pts)
    a_full = a_from(full[0], rws[0], full[1], rws[1])
    a_reps = []
    for wi in (0, 1):
        for rep in jk_store[wi]:
            rs = [full[0], full[1]]
            rs[wi] = rep
            a_reps.append(a_from(rs[0], rws[0], rs[1], rws[1]))
    se_a = jackknife(a_reps)
    print(f"\nfitted law constant: a = {a_full:.4f} ± {se_a:.4f} "
          f"(recorded {A_REC}; jackknife over 10 delete-block refits)")

    # pooled overtone deviations with SEs
    print("\npooled deviations (mean over four windows) with jackknife SEs:")
    for m in [9, 25, 27, 8, 4]:
        devs_full = []
        for wi in range(4):
            tau = math.log(m) / (2 * math.pi * rws[wi])
            devs_full.append(full[wi][m] - math.exp(-A_REC * tau ** 2))
        reps = []
        for wi in range(4):
            for rep in jk_store[wi]:
                d = list(devs_full)
                tau = math.log(m) / (2 * math.pi * rws[wi])
                d[wi] = rep[m] - math.exp(-A_REC * tau ** 2)
                reps.append(float(np.mean(d)))
        print(f"  m = {m:2d}: pooled dev = {float(np.mean(devs_full)):+.3f} "
              f"± {jackknife(reps):.3f}")

    print(f"\ndone ({time.time()-t_start:.0f}s); quantities as quoted in the "
          f"paper draft.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
