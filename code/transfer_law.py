"""WP-RH5 — the transfer law, out of sample.

WP-RH4/4b measured the per-frequency transfer T(omega) of the prime comb into
the zeros' shift field at two windows. Two candidate laws in the scaling
variable tau = omega/(2 pi rho_w) were fitted on those windows and RECORDED in
the prereg before this instrument ran:

  Law A (Debye-Waller):     T = exp(-a tau^2),  a = 1.1416   (in-sample SSE 8x better)
  Law B (linear/form-factor): T = 1 - c tau,    c = 0.5255

This instrument sends both to a window neither has seen — zeros 301..400,
heights ~542..680 — after re-deriving the fits from scratch and asserting they
match the recorded constants (integrity check). If Law A survives, the lane
states its first formally labeled CONJECTURE: the prime-to-zero transfer is
the Debye-Waller factor of the zeros' displacement field, a ~ 2 pi^2 Var(S).
Runs under registry/2026-08-07-transfer-law-prereg.md.
"""
import math
import time

import numpy as np
from mpmath import mp, zetazero

mp.dps = 30

BAT = [2, 3, 4, 5, 7, 8, 9, 11, 13]
GATED = [2, 3, 5, 7]
EXT = [4, 11, 13]
A_REC, C_REC = 1.1416, 0.5255
FIT_WINDOWS = [(1, 60), (141, 200)]
TEST_WINDOW = (301, 400)


def beta_pred(m):
    s = min(p for p in range(2, m + 1) if m % p == 0)
    return math.log(s) / (math.pi * math.sqrt(m) * math.log(m))


def nbar(E):
    return (E / (2 * math.pi)) * (math.log(E / (2 * math.pi)) - 1) + 0.875


def rho(E):
    return math.log(E / (2 * math.pi)) / (2 * math.pi)


def window(gam, klo, khi):
    ks = np.arange(klo, khi + 1)
    g = np.array([gam[k - 1] for k in ks])
    y = np.array([nbar(x) for x in g]) - (ks - 0.5)
    kt = (ks - ks.mean()) / (ks.max() - ks.min())
    cols = [np.sin(g * math.log(m)) for m in BAT] + [np.ones_like(kt), kt, kt ** 2]
    b, *_ = np.linalg.lstsq(np.vstack(cols).T, y, rcond=None)
    ratios = {m: b[i] / beta_pred(m) for i, m in enumerate(BAT)}
    return ratios, float(np.mean([rho(x) for x in g])), float(np.mean(y ** 2))


def main():
    t_start = time.time()
    print("WP-RH5: the transfer law, out of sample. dps =", mp.dps)
    print("prereg: registry/2026-08-07-transfer-law-prereg.md\n")

    print("computing 400 zeta zeros ...", flush=True)
    gam = [float(zetazero(k).imag) for k in range(1, 401)]

    taus, Ts = [], []
    for (klo, khi) in FIT_WINDOWS:
        r, rw, _ = window(gam, klo, khi)
        for m in GATED:
            taus.append(math.log(m) / (2 * math.pi * rw))
            Ts.append(r[m])
    taus, Ts = np.array(taus), np.array(Ts)
    c_fit = float(np.sum(taus * (1 - Ts)) / np.sum(taus ** 2))
    a_fit = float(np.sum(taus ** 2 * (-np.log(Ts))) / np.sum(taus ** 4))
    ok_int = abs(a_fit - A_REC) < 1e-3 and abs(c_fit - C_REC) < 1e-3
    print(f"integrity: refit a = {a_fit:.4f} (recorded {A_REC}), c = {c_fit:.4f} "
          f"(recorded {C_REC})  [{'PASS' if ok_int else 'FAIL'}]\n")

    r3, rho3, u2 = window(gam, *TEST_WINDOW)
    print(f"OUT-OF-SAMPLE window: zeros {TEST_WINDOW[0]}..{TEST_WINDOW[1]}, heights "
          f"{gam[TEST_WINDOW[0]-1]:.1f}..{gam[TEST_WINDOW[1]-1]:.1f}, "
          f"rho_w = {rho3:.4f}\n")
    a3 = 2 * math.pi ** 2 * u2
    print(f"{'m':>4s} {'tau':>7s} {'T_meas':>8s} {'Law A':>8s} {'Law B':>8s} "
          f"{'mech':>8s} {'|dev A|':>8s}")
    devA, devB, devM = {}, {}, {}
    for m in BAT:
        tau = math.log(m) / (2 * math.pi * rho3)
        tA = math.exp(-A_REC * tau ** 2)
        tB = 1 - C_REC * tau
        tM = math.exp(-a3 * tau ** 2)
        devA[m], devB[m], devM[m] = r3[m] - tA, r3[m] - tB, r3[m] - tM
        print(f"{m:4d} {tau:7.3f} {r3[m]:8.3f} {tA:8.3f} {tB:8.3f} {tM:8.3f} "
              f"{abs(devA[m]):8.3f}")

    okS1 = all(abs(devA[m]) < 0.08 for m in GATED)
    sseA = sum(devA[m] ** 2 for m in GATED)
    sseB = sum(devB[m] ** 2 for m in GATED)
    okS2 = sseA < sseB
    print(f"\ngate S1 (Law A out of sample, gated |dev| < 0.08): "
          f"[{'PASS' if okS1 else 'FAIL'}]")
    print(f"gate S2 (model selection, gated SSE: A = {sseA:.5f} vs B = "
          f"{sseB:.5f}): [{'PASS' if okS2 else 'FAIL'}]")
    q1 = float(np.mean([abs(devA[m]) for m in GATED]))
    print(f"Q1 (gated mean |dev| < 0.04): {q1:.4f}  "
          f"{'CONFIRMED' if q1 < 0.04 else 'REFUTED'}")
    q2 = all(abs(devA[m]) < 0.12 for m in EXT)
    print(f"Q2 (extended m in {EXT} within 0.12): "
          f"{'CONFIRMED' if q2 else 'REFUTED'}")
    q3 = all(abs(devM[m]) < 0.10 for m in GATED)
    print(f"Q3 (zero-parameter mechanism variant, a3 = 2 pi^2 <u^2> = {a3:.3f}, "
          f"gated within 0.10): {'CONFIRMED' if q3 else 'REFUTED'}")

    allok = ok_int and okS1 and okS2
    print("\nreading: " + ("the Debye-Waller law predicted a window it had "
          "never seen. The lane\nstates its first labeled CONJECTURE: the "
          "prime-to-zero transfer is the\nDebye-Waller factor of the zeros' "
          "displacement field, T = exp(-a tau^2),\na ~ 2 pi^2 Var(S) — "
          "falsifiable at further windows, larger batteries,\nand other "
          "L-functions. The explicit-formula amplitudes are its tau -> 0\n"
          "limit; criticality (v2 problem statement) is its tau -> dense "
          "reading."
          if allok else "the committed law did not survive out of sample as "
          "gated; the table\nabove is the finding, reported as measured."))
    print(f"\nresult: {'ALL GATES PASS' if allok else 'FAILURES PRESENT'}  "
          f"({time.time()-t_start:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
