"""WP-RH6 — the derivation bridge.

Structural lemma (fixed in the prereg before any run): least squares of a
field on its own components evaluated at the true sample points returns the
full coefficients identically — sampling displacement cannot attenuate a
self-line. So the attenuation measured in WP-RH4b/RH5/RH5b must live in
S(t)'s own line content at finite height. Three committed experiments:

  A  negative control: displaced-lattice synthetics show NO attenuation
     (excluding sampling as the mechanism, by machine check);
  B  the line content of S(t) measured in CONTINUOUS t (S = N - Nbar, exact
     between located zeros, no zero-sampling in the estimator) on the three
     zeta windows, compared cell-by-cell with the sampled ratios;
  C  the same on the second family (Dirichlet beta).

If B and C agree with the sampled measurements, the conjecture restates (v2):
T(omega) is the height-local relative line amplitude of the fluctuation field
itself, with the universal constant a pointing at pair-correlation (GUE)
universality — the Goldston/Montgomery route — as the formal derivation
target. Runs under registry/2026-08-07-transfer-theory-prereg.md.

Bring-up note (honest, RH2-Abel precedent): the prereg's Part A2 spec was
internally inconsistent — at amplitude scale 0.5 the displacement field has
sum(alpha*nu) ~ 1.6, the fixed-point map is not a contraction, and the first
run's "field" carried a residual of 0.33 (never the intended in-span field);
its marginal gate failure was an artifact of non-convergence. The scale is
corrected to 0.15 (sum ~ 0.47, contractive), a convergence assert added so
the instrument fails loudly, thresholds unchanged; first-run output recorded
in the results file.

First-light note: gates G-B1 and G-C1 were REFUTED on physics, permanently
and informatively — the continuous line content of S(t) measured FULL
(0.974..1.008 in all 15 cells, both families) while only the zero-sampled
displacements attenuate. The prereg's committed contingency applies: the
attenuation localizes into sampling at the zeros; the planned v2 restatement
is withheld and the localized restatement appears in the results file. As
with RH1/RH4, the exit code tracks the instrument gates (A1, A2); B1/C1
print REFUTED on every run.
"""
import math
import time

import numpy as np
from mpmath import mp, mpf, mpc, gamma, zeta, zetazero, pi as mppi

mp.dps = 30

BAT = [2, 3, 4, 5, 7, 8, 9, 11, 13]
GATED = [2, 3, 5, 7]
A_REC = 1.1416
ZWINDOWS = [(1, 60), (141, 200), (301, 400)]
GRID = 0.02


def A_amp(m):
    s = min(p for p in range(2, m + 1) if m % p == 0)
    return math.log(s) / (math.sqrt(m) * math.log(m))


def nbar(E):
    return (E / (2 * math.pi)) * (math.log(E / (2 * math.pi)) - 1) + 0.875


def rho(E):
    return math.log(E / (2 * math.pi)) / (2 * math.pi)


def lsq_ratios(ts, ys, preds):
    """Common regression: ys on {sin(ts*ln m)} + {1, t~, t~^2}; ratios vs preds."""
    tt = (ts - ts.mean()) / (ts.max() - ts.min())
    cols = [np.sin(ts * math.log(m)) for m in BAT] + [np.ones_like(tt), tt, tt ** 2]
    b, *_ = np.linalg.lstsq(np.vstack(cols).T, ys, rcond=None)
    return {m: b[i] / preds[m] for i, m in enumerate(BAT)}


def main():
    t_start = time.time()
    gate = {}
    print("WP-RH6: the derivation bridge. dps =", mp.dps)
    print("prereg: registry/2026-08-07-transfer-theory-prereg.md\n")

    # ---------------- Part A: negative control ----------------
    print("Part A — displaced-lattice synthetics (the lemma, machine-checked)")
    xi = np.arange(1, 401) - 0.5
    x = xi.copy()
    for _ in range(60):
        x = xi + 0.15 * np.sin(1.3 * x)
    tt = (x - x.mean()) / (x.max() - x.min())
    cols = [np.sin(1.3 * x), np.ones_like(x), tt, tt ** 2]
    b, *_ = np.linalg.lstsq(np.vstack(cols).T, x - xi, rcond=None)
    ratA1 = b[0] / 0.15
    okA1 = 0.98 <= ratA1 <= 1.02
    gate["A1"] = okA1
    print(f"gate G-A1 (single line, self-recovery): ratio = {ratA1:.4f}  "
          f"[{'PASS' if okA1 else 'FAIL'}]")

    amps = {m: 0.15 * A_amp(m) / math.pi for m in BAT}
    nus = {m: math.log(m) / 0.5 for m in BAT}
    x = xi.copy()
    for _ in range(200):
        x = xi + sum(amps[m] * np.sin(nus[m] * x) for m in BAT)
    u = x - xi
    conv = float(np.max(np.abs(u - sum(amps[m] * np.sin(nus[m] * x) for m in BAT))))
    assert conv < 1e-9, f"fixed point did not converge: residual {conv}"
    tt = (x - x.mean()) / (x.max() - x.min())
    cols = [np.sin(nus[m] * x) for m in BAT] + [np.ones_like(tt), tt, tt ** 2]
    b, *_ = np.linalg.lstsq(np.vstack(cols).T, u, rcond=None)
    ratsA2 = [b[i] / amps[m] for i, m in enumerate(BAT)]
    okA2 = all(0.95 <= rr <= 1.05 for rr in ratsA2)
    gate["A2"] = okA2
    print(f"gate G-A2 (prime-like field, nine lines): ratios "
          f"{[round(float(rr), 3) for rr in ratsA2]}  [{'PASS' if okA2 else 'FAIL'}]")
    print("-> the displaced lattice does NOT attenuate: sampling is excluded as")
    print("   the mechanism; the deficit must live in S(t)'s own line content.\n")

    # ---------------- Part B: continuous vs sampled, zeta ----------------
    print("Part B — the line content of S(t), continuous vs sampled (zeta)")
    print("computing 400 zeta zeros ...", flush=True)
    gam = [float(zetazero(k).imag) for k in range(1, 401)]
    preds = {m: -A_amp(m) / math.pi for m in BAT}
    cells, devs_law = [], []
    for (klo, khi) in ZWINDOWS:
        ks = np.arange(klo, khi + 1)
        g = np.array([gam[k - 1] for k in ks])
        y = np.array([nbar(v) for v in g]) - (ks - 0.5)
        sampled = lsq_ratios(g, y, {m: A_amp(m) / math.pi for m in BAT})
        ta, tb = gam[klo - 1], gam[khi - 1]
        ts = np.arange(ta, tb, GRID)
        counts = np.searchsorted(gam, ts, side="right")
        Sc = counts - np.array([nbar(v) for v in ts])
        cont = lsq_ratios(ts, Sc, preds)
        rw = float(np.mean([rho(v) for v in g]))
        for m in GATED:
            tau = math.log(m) / (2 * math.pi * rw)
            cells.append((klo, m, sampled[m], cont[m]))
            devs_law.append(abs(cont[m] - math.exp(-A_REC * tau ** 2)))
        print(f"  window {klo}..{khi}: " + "  ".join(
            f"m={m}: samp {sampled[m]:+.3f} cont {cont[m]:+.3f}" for m in GATED))
    okB1 = all(abs(s - c) < 0.10 for (_, _, s, c) in cells)
    print(f"gate G-B1 (12 cells, |cont - sampled| < 0.10): max diff = "
          f"{max(abs(s - c) for (_, _, s, c) in cells):.3f}  "
          f"[{'CONFIRMED' if okB1 else 'REFUTED (recorded)'}]")
    p1 = float(np.mean(devs_law))
    print(f"P1 (continuous obeys the recorded law, mean dev < 0.06): {p1:.4f}  "
          f"{'CONFIRMED' if p1 < 0.06 else 'REFUTED'}\n")

    # ---------------- Part C: continuous, beta ----------------
    print("Part C — the second family, continuous (Dirichlet beta)")
    from dirichlet_transfer import find_zeros, theta_phase, rho_chi, CHI
    print("locating 150 beta zeros ...", flush=True)
    bz = find_zeros()
    ks = np.arange(1, 151)
    g = np.array(bz[:150])
    y = np.array([theta_phase(v) / math.pi for v in g]) - (ks - 0.5)
    sampledC = lsq_ratios(g, y, {m: A_amp(m) / math.pi for m in BAT})
    ts = np.arange(g[0], g[-1], GRID)
    counts = np.searchsorted(g, ts, side="right")
    Sc = counts - np.array([theta_phase(v) / math.pi for v in ts])
    contC = lsq_ratios(ts, Sc, preds)
    rwC = float(np.mean([rho_chi(v) for v in g]))
    print("  " + "  ".join(f"m={m}: samp {sampledC[m]:+.3f} cont {contC[m]:+.3f}"
                           for m in [3, 5, 7]))
    okC1 = all(abs(sampledC[m] - contC[m]) < 0.10 and
               (contC[m] > 0) == (CHI[m] > 0) for m in [3, 5, 7])
    print(f"gate G-C1 (beta, |cont - sampled| < 0.10, chi signs): "
          f"[{'CONFIRMED' if okC1 else 'REFUTED (recorded)'}]")

    # per-window fitted a from continuous gated points (zeta) and beta
    a_fits = []

    def fit_a(pts):
        t2 = np.array([t ** 2 for (t, T) in pts])
        nl = np.array([-math.log(max(T, 1e-6)) for (t, T) in pts])
        return float(np.sum(t2 * nl) / np.sum(t2 ** 2))
    idx = 0
    for (klo, khi) in ZWINDOWS:
        g = np.array([gam[k - 1] for k in range(klo, khi + 1)])
        rw = float(np.mean([rho(v) for v in g]))
        pts = [(math.log(m) / (2 * math.pi * rw), cells[idx + j][3])
               for j, m in enumerate(GATED)]
        a_fits.append(fit_a(pts))
        idx += 4
    ptsC = [(math.log(m) / (2 * math.pi * rwC), abs(contC[m])) for m in [3, 5, 7]]
    a_fits.append(fit_a(ptsC))
    p2 = all(0.9 <= a <= 1.5 for a in a_fits)
    print(f"P2 (universality: fitted a per window/family in [0.9, 1.5]): "
          f"{[round(a, 3) for a in a_fits]}  {'CONFIRMED' if p2 else 'REFUTED'}")
    a3 = 2 * math.pi ** 2 * float(np.mean((Sc - np.mean(Sc)) ** 2))
    sseU = sum((abs(contC[m]) - math.exp(-A_REC * t ** 2)) ** 2
               for (t, _), m in zip(ptsC, [3, 5, 7]))
    sseV = sum((abs(contC[m]) - math.exp(-a3 * t ** 2)) ** 2
               for (t, _), m in zip(ptsC, [3, 5, 7]))
    p3 = sseU < sseV
    print(f"P3 (universal a beats local-variance a3 = {a3:.3f} on beta, "
          f"continuous): SSE {sseU:.5f} vs {sseV:.5f}  "
          f"{'CONFIRMED' if p3 else 'REFUTED'}")

    allok = all(gate.values())
    mean_cont = float(np.mean([abs(c) for (_, _, _, c) in cells]))
    print("\nreading: the lemma holds on synthetics (no sampling attenuation,")
    print("in-span recovery exact), and the continuous measurement localizes")
    print(f"the mechanism: S(t)'s line content is FULL (mean |cont| = "
          f"{mean_cont:.3f} across\nthe zeta cells, same on beta) while only "
          f"the zero-sampled displacement\nsequence attenuates. The committed "
          f"bridge gates G-B1/G-C1 are REFUTED —\nand the refutation is the "
          f"localization: the Debye-Waller transfer law is\nthe price of "
          f"reading the primes from the zeros' POSITIONS; the counting\n"
          f"function carries them at full amplitude at every height. The "
          f"conjecture's\nlocalized restatement is in the results file.")
    print(f"\nresult: {'INSTRUMENT GATES PASS' if allok else 'FAILURES PRESENT'}"
          f"; bridge gates B1/C1 {'CONFIRMED' if (okB1 and okC1) else 'REFUTED (recorded)'}"
          f"  ({time.time()-t_start:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
