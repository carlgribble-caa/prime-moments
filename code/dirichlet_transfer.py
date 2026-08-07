"""WP-RH5b — the transfer law on a second family: L(s, chi_-4).

Executes item (iii) of the WP-RH5 conjecture's falsification protocol. The
Debye-Waller transfer law, with the RECORDED constant a = 1.1416, is applied
to the Dirichlet beta function's zeros: predicted regression ratio at
frequency ln m equals chi_-4(m) * exp(-a tau^2). The family adds structure
zeta could not test: forced nulls at even frequencies (chi(2^k) = 0) and the
character sign pattern -, +, -, -, + at m = 3, 5, 7, 11, 13 — all committed
in the prereg. A pass extends the conjecture across families as its protocol
demands; a fail is a falsification event.
Runs under registry/2026-08-07-dirichlet-transfer-prereg.md.
"""
import math
import time

import numpy as np
from mpmath import mp, mpf, mpc, gamma, digamma, zeta, pi as mppi

mp.dps = 30

NZEROS = 150
SCAN_LO, SCAN_HI, SCAN_STEP = 2.0, 260.0, 0.25
A_REC = 1.1416
BAT = [2, 3, 4, 5, 7, 8, 9, 11, 13]
NULLS = [2, 4, 8]
SIGNS = {3: -1, 5: 1, 7: -1, 11: -1, 13: 1}
MAGS = [3, 5, 7]
CHI = {m: (0 if m % 2 == 0 else (1 if m % 4 == 1 else -1)) for m in BAT}


def beta_L(s):
    return 4 ** (-s) * (zeta(s, mpf(1) / 4) - zeta(s, mpf(3) / 4))


def Z_hardy(t):
    s = mpc(mpf(1) / 2, t)
    lam = (4 / mppi) ** ((s + 1) / 2) * gamma((s + 1) / 2) * beta_L(s)
    assert abs(lam.imag) < mpf("1e-10") * (1 + abs(lam.real)), "Lambda not real"
    return lam.real


def theta_phase(t):
    return float(t / 2 * mp.log(4 / mppi) +
                 mp.im(mp.loggamma(mpc(mpf(3) / 4, t / 2))))


def rho_chi(t):
    return float((mp.log(4 / mppi) / 2 +
                  mp.re(digamma(mpc(mpf(3) / 4, t / 2))) / 2) / mppi)


def find_zeros():
    zeros = []
    t = SCAN_LO
    z_prev = Z_hardy(mpf(t))
    while t < SCAN_HI and len(zeros) < NZEROS:
        t2 = t + SCAN_STEP
        z_next = Z_hardy(mpf(t2))
        if z_prev * z_next < 0:
            lo, hi = mpf(t), mpf(t2)
            zlo = z_prev
            for _ in range(60):
                mid = (lo + hi) / 2
                zm = Z_hardy(mid)
                if zlo * zm < 0:
                    hi = mid
                else:
                    lo, zlo = mid, zm
            zeros.append(float((lo + hi) / 2))
        t, z_prev = t2, z_next
    return zeros


def beta_pred(m):
    s = min(p for p in range(2, m + 1) if m % p == 0)
    return math.log(s) / (math.pi * math.sqrt(m) * math.log(m))


def main():
    t_start = time.time()
    print("WP-RH5b: the transfer law on L(s, chi_-4). dps =", mp.dps)
    print("prereg: registry/2026-08-07-dirichlet-transfer-prereg.md\n")

    print(f"locating the first {NZEROS} zeros of Dirichlet beta ...", flush=True)
    gam = find_zeros()
    assert len(gam) >= NZEROS, f"only {len(gam)} zeros found"
    print(f"found {len(gam)}; heights {gam[0]:.3f} .. {gam[-1]:.3f} "
          f"({time.time()-t_start:.0f}s)\n")

    ks = np.arange(1, NZEROS + 1)
    g = np.array(gam[:NZEROS])
    y = np.array([theta_phase(x) / math.pi for x in g]) - (ks - 0.5)
    y_c = y - np.mean(y)
    okD0 = float(np.max(np.abs(y_c))) < 0.9
    print(f"gate D0 (indexing integrity): max |y - mean| = "
          f"{float(np.max(np.abs(y_c))):.3f} < 0.9  [{'PASS' if okD0 else 'FAIL'}]")

    kt = (ks - ks.mean()) / (ks.max() - ks.min())
    cols = [np.sin(g * math.log(m)) for m in BAT] + [np.ones_like(kt), kt, kt ** 2]
    b, *_ = np.linalg.lstsq(np.vstack(cols).T, y, rcond=None)
    ratios = {m: b[i] / beta_pred(m) for i, m in enumerate(BAT)}
    rho_w = float(np.mean([rho_chi(x) for x in g]))
    a3 = 2 * math.pi ** 2 * float(np.mean(y_c ** 2))
    print(f"rho_w = {rho_w:.4f}; mechanism a3 = 2 pi^2 <y^2> = {a3:.3f}\n")

    print(f"{'m':>4s} {'chi':>4s} {'tau':>7s} {'ratio':>8s} {'chi*Law':>9s} "
          f"{'chi*mech':>9s}")
    law, mech = {}, {}
    for m in BAT:
        tau = math.log(m) / (2 * math.pi * rho_w)
        law[m] = CHI[m] * math.exp(-A_REC * tau ** 2)
        mech[m] = CHI[m] * math.exp(-a3 * tau ** 2)
        print(f"{m:4d} {CHI[m]:+4d} {tau:7.3f} {ratios[m]:+8.3f} {law[m]:+9.3f} "
              f"{mech[m]:+9.3f}")

    okD1 = all(abs(ratios[m]) < 0.30 for m in NULLS)
    okD2 = all((ratios[m] > 0) == (SIGNS[m] > 0) for m in SIGNS)
    okD3 = all(abs(abs(ratios[m]) - abs(law[m])) < 0.12 for m in MAGS)
    print(f"\ngate D1 (forced nulls m in {NULLS}, |ratio| < 0.30): "
          f"{[round(abs(ratios[m]), 3) for m in NULLS]}  "
          f"[{'PASS' if okD1 else 'FAIL'}]")
    print(f"gate D2 (character sign pattern -,+,-,-,+ at {sorted(SIGNS)}): "
          f"[{'PASS' if okD2 else 'FAIL'}]")
    print(f"gate D3 (law magnitudes m in {MAGS}, |dev| < 0.12): "
          f"{[round(abs(abs(ratios[m]) - abs(law[m])), 3) for m in MAGS]}  "
          f"[{'PASS' if okD3 else 'FAIL'}]")
    e1 = all(abs(abs(ratios[m]) - abs(mech[m])) < 0.10 for m in MAGS)
    e2 = abs(abs(ratios[13]) - abs(law[13])) < 0.15
    e3 = float(np.mean([abs(abs(ratios[m]) - abs(law[m])) for m in MAGS]))
    print(f"E1 (mechanism variant within 0.10): {'CONFIRMED' if e1 else 'REFUTED'}")
    print(f"E2 (m = 13 within 0.15 — is the zeta anomaly family-specific?): "
          f"{'CONFIRMED' if e2 else 'REFUTED'}")
    print(f"E3 (gated mean magnitude dev < 0.06): {e3:.4f}  "
          f"{'CONFIRMED' if e3 < 0.06 else 'REFUTED'}")
    print(f"(m = 9 reported, not gated: ratio {ratios[9]:+.3f} vs law {law[9]:+.3f})")

    allok = okD0 and okD1 and okD2 and okD3
    print("\nreading: " + ("the conjecture survives its cross-family test: on a "
          "second zeta\nfamily the transfer obeys the same Debye-Waller law "
          "with the SAME\nrecorded constant, the even frequencies are silent "
          "exactly as the\ncharacter demands, and the sign pattern is the "
          "character's. The law\nis a property of the prime-zero coupling, "
          "not of zeta alone."
          if allok else "the conjecture FAILED its cross-family test as "
          "gated; this is a\nfalsification event and is recorded as such in "
          "the conjecture's\nregistry entry."))
    print(f"\nresult: {'ALL GATES PASS' if allok else 'FAILURES PRESENT'}  "
          f"({time.time()-t_start:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
