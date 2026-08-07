"""WP-RH4b — height dependence of the transfer attenuation.

WP-RH4 measured a frequency-decaying attenuation of the prime amplitudes in
the zeros' shift field, with a two-factor post-hoc diagnosis whose mechanisms
both scale with omega/rho. Committed test, on zeros the RH4 analysis never
used (k = 141..200): the attenuation must WEAKEN with height as the zeros
densify. The field is exact — no mean-value approximation enters. A refutation
(height-independent attenuation) would point away from both mechanisms and be
reported as such. Runs under registry/2026-08-07-transfer-height-prereg.md.

Bring-up note (honest, RH2-Abel precedent): the prereg's field formula carried
a sign error — it asserted (k - 1/2) - Nbar(gamma_k) = -Sbar(gamma_k), but the
Riemann-von Mangoldt midpoint convention gives +Sbar; the first run
implemented the prereg faithfully and produced ratios of the committed
magnitudes with flipped sign (LOW window -0.922/-0.809/-0.648/-0.554,
replicating RH4's +0.92/+0.81/+0.65/+0.55 exactly). The field below is
corrected to y = Nbar(gamma_k) - (k - 1/2) (= -Sbar = the delta*rho analogue
the predictions were written for), all thresholds unchanged; the first-run
output is recorded in the results file.
"""
import math
import time

import numpy as np
from mpmath import mp, zetazero

mp.dps = 30

BATTERY = [2, 3, 4, 5, 7, 8, 9, 11, 13]
GATED = [2, 3, 5, 7]
WINDOWS = [("LOW", 1, 60), ("HIGH", 141, 200)]


def beta_pred(m):
    spf = min(p for p in range(2, m + 1) if m % p == 0)
    return math.log(spf) / (math.pi * math.sqrt(m) * math.log(m))


def nbar(E):
    return (E / (2 * math.pi)) * (math.log(E / (2 * math.pi)) - 1) + 0.875


def window_ratios(gam, klo, khi):
    ks = np.arange(klo, khi + 1)
    g = np.array([gam[k - 1] for k in ks])
    y = np.array([nbar(x) for x in g]) - (ks - 0.5)
    kt = (ks - ks.mean()) / (ks.max() - ks.min())
    cols = [np.sin(g * math.log(m)) for m in BATTERY] + [np.ones_like(kt), kt, kt ** 2]
    X = np.vstack(cols).T
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return {m: beta[i] / beta_pred(m) for i, m in enumerate(BATTERY)}


def main():
    t_start = time.time()
    print("WP-RH4b: height dependence of the transfer attenuation. dps =", mp.dps)
    print("prereg: registry/2026-08-07-transfer-height-prereg.md\n")

    print("computing 200 zeta zeros ...", flush=True)
    gam = [float(zetazero(k).imag) for k in range(1, 201)]
    print(f"LOW window heights {gam[0]:.1f}..{gam[59]:.1f}; "
          f"HIGH window heights {gam[140]:.1f}..{gam[199]:.1f}\n")

    ratios = {}
    for (name, klo, khi) in WINDOWS:
        ratios[name] = window_ratios(gam, klo, khi)
    print(f"{'m':>4s} {'omega':>7s} {'LOW ratio':>10s} {'HIGH ratio':>11s} "
          f"{'improvement':>12s}")
    for m in BATTERY:
        lo, hi = ratios["LOW"][m], ratios["HIGH"][m]
        print(f"{m:4d} {math.log(m):7.4f} {lo:10.3f} {hi:11.3f} {hi - lo:+12.3f}")

    low = [ratios["LOW"][m] for m in GATED]
    okZ1 = all(0.2 <= r <= 1.1 for r in low) and \
        all(low[i + 1] <= low[i] + 0.05 for i in range(len(low) - 1))
    improved = sum(1 for m in GATED if ratios["HIGH"][m] > ratios["LOW"][m])
    okZ2 = improved >= 3
    print(f"\ngate Z1 (LOW replication: gated ratios in [0.2, 1.1], "
          f"nonincreasing +-0.05): [{'PASS' if okZ1 else 'FAIL'}]")
    print(f"gate Z2 (attenuation weakens with height, >= 3 of 4): "
          f"{improved}/4 improved  [{'PASS' if okZ2 else 'FAIL'}]")
    v1 = 0.90 <= ratios["HIGH"][2] <= 1.05
    imp = float(np.mean([ratios["HIGH"][m] - ratios["LOW"][m] for m in GATED]))
    v2 = 0.03 <= imp <= 0.25
    print(f"V1 (HIGH m=2 in [0.90, 1.05]): {ratios['HIGH'][2]:.3f}  "
          f"{'CONFIRMED' if v1 else 'REFUTED'}")
    print(f"V2 (mean improvement in [0.03, 0.25]): {imp:+.3f}  "
          f"{'CONFIRMED' if v2 else 'REFUTED'}")

    allok = okZ1 and okZ2
    print("\nreading: " + ("the attenuation weakens as the zeros densify, as "
          "both proposed\nmechanisms require — the transfer shape is a "
          "height-dependent sampling\neffect, not a fixed law; the "
          "explicit-formula amplitudes are recovered\nin the limit of dense "
          "sampling."
          if allok else "the committed height dependence did not hold as "
          "gated; the two-window\ntable above is the finding, reported as "
          "measured."))
    print(f"\nresult: {'ALL GATES PASS' if allok else 'FAILURES PRESENT'}  "
          f"({time.time()-t_start:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
