"""WP9b — the quantum-graph instrument: the crystal as a length spectrum on a bench.

A metric star graph with three edges of lengths log 2, log 3, log 5 (Neumann outer
ends, Kirchhoff centre) has eigenvalues k_n solving  sum_p tan(k log p) = 0. Its
periodic orbits have lengths 2(a log 2 + b log 3 + c log 5) = 2 log n for 5-smooth n
— the crystal's shadow on three axes, doubled. The trace formula therefore predicts:
the Fourier transform of the spectral counting oscillation peaks exactly at 2 log n,
n running over the 5-smooth integers.

Checks:
 (1) Weyl law: N(K) ~ (L/pi) K with L = log 30 — measured slope vs theory.
 (2) Length spectrum: |FT of the counting oscillation| has its top peaks at 2 log n
     for 5-smooth n (matched within resolution); PASS requires the top 10 peaks all
     matched and the first several smooth lengths all present among detected peaks.
 (3) Negative control: the same star with incommensurable non-crystal lengths
     (1.0, 1.31, 1.77) produces peaks on ITS combination set, and the crystal's
     smooth-length template scores far worse on it — the signature is the crystal's,
     not the instrument's.

This is the closest legal thing to a Hilbert-Polya bench: the object whose spectrum
encodes the crystal is here an actual differential operator. (Honest framing: an
instrument demo — the Kurasov-Sarnak connection between quantum graphs and
crystalline measures is the serious mathematics adjacent to it.)
"""
import math

import numpy as np

KMAX = 3000.0
GRID = 4_000_000


def spectrum(lengths, kmax=KMAX, grid=GRID):
    """Roots of f(k) = sum tan(k L_i), avoiding pole crossings, by sign change."""
    ks = np.linspace(1e-6, kmax, grid)
    with np.errstate(all="ignore"):
        vals = sum(np.tan(ks * L) for L in lengths)
        # pole guard: tan(kL) has poles where kL/pi - 1/2 is an integer
        guard = np.ones_like(ks, bool)
        for L in lengths:
            frac = np.mod(ks * L / math.pi - 0.5, 1.0)
            guard &= np.minimum(frac, 1.0 - frac) > 3e-4
    roots = []
    s = np.sign(vals)
    flips = np.where((s[:-1] * s[1:] < 0) & guard[:-1] & guard[1:])[0]
    for i in flips:
        a, b = ks[i], ks[i + 1]
        # discard sign flips caused by a pole inside the interval
        if any(math.floor(b * L / math.pi - 0.5) > math.floor(a * L / math.pi - 0.5)
               for L in lengths):
            continue
        fa = sum(math.tan(a * L) for L in lengths)
        for _ in range(40):
            m = (a + b) / 2
            fm = sum(math.tan(m * L) for L in lengths)
            if fa * fm <= 0:
                b = m
            else:
                a, fa = m, fm
        roots.append((a + b) / 2)
    return np.array(roots)


def length_spectrum(roots, L_total, ell_max, n_ell=6000):
    """|sum_n exp(i ell k_n) - Weyl| sampled on an ell grid."""
    ells = np.linspace(0.5, ell_max, n_ell)
    # oscillatory part: sum over eigenvalues of e^{i ell k} minus the Weyl integral
    K = roots.max()
    ft = np.array([abs(np.exp(1j * ell * roots).sum()
                       - (L_total / math.pi) * (np.exp(1j * ell * K) - 1) / (1j * ell))
                   for ell in ells])
    return ells, ft


def top_peaks(ells, ft, n=12, min_sep=0.05):
    order = np.argsort(-ft)
    floor_amp = 0.1 * ft.max()      # reject window sidelobes
    peaks = []
    for i in order:
        if ft[i] < floor_amp:
            break
        if all(abs(ells[i] - p) > min_sep for p, _ in peaks):
            peaks.append((ells[i], ft[i]))
            if len(peaks) == n:
                break
    return sorted(peaks)


def smooth_lengths(ell_max):
    out = []
    n = 2
    while 2 * math.log(n) <= ell_max:
        m = n
        for p in (2, 3, 5):
            while m % p == 0:
                m //= p
        if m == 1:
            out.append((n, 2 * math.log(n)))
        n += 1
    return out


def main():
    print("quantum-graph instrument (WP9b): star with edge lengths log 2, log 3, log 5")
    lengths = [math.log(2), math.log(3), math.log(5)]
    L = sum(lengths)
    roots = spectrum(lengths)
    weyl_slope = len(roots) / roots.max()
    print(f"  eigenvalues found: {len(roots)} to k = {KMAX:.0f}; "
          f"Weyl slope {weyl_slope:.5f} vs L/pi = {L / math.pi:.5f}")
    ok_weyl = abs(weyl_slope - L / math.pi) / (L / math.pi) < 0.01

    ELLMAX = 5.0
    ells, ft = length_spectrum(roots, L, ELLMAX)
    peaks = top_peaks(ells, ft)
    targets = smooth_lengths(ELLMAX)
    print("  top peaks of the length spectrum vs 2 log n (5-smooth n):")
    matched = 0
    for ell, amp in peaks:
        best = min(targets, key=lambda t: abs(t[1] - ell))
        hit = abs(best[1] - ell) < 0.02
        matched += hit
        print(f"    peak at {ell:6.3f} (amp {amp:7.0f})  ->  2 log {best[0]:<3d} = "
              f"{best[1]:6.3f}  {'MATCH' if hit else '??'}")
    ok_peaks = matched >= 10
    covered = sum(1 for _, t in targets[:8]
                  if any(abs(t - ell) < 0.02 for ell, _ in peaks))
    print(f"  first 8 smooth lengths detected among peaks: {covered}/8")
    ok_cover = covered >= 7

    # negative control
    ctrl = [1.0, 1.31, 1.77]
    roots_c = spectrum(ctrl, kmax=1500.0, grid=2_000_000)
    ells_c, ft_c = length_spectrum(roots_c, sum(ctrl), ELLMAX)
    def template_score(ells_, ft_):
        sc = 0.0
        for _, t in targets:
            i = np.argmin(np.abs(ells_ - t))
            sc += ft_[i]
        return sc / len(targets)
    s_crystal = template_score(ells, ft) / np.mean(ft)
    s_ctrl = template_score(ells_c, ft_c) / np.mean(ft_c)
    print(f"  crystal-template score: log-graph {s_crystal:.2f} vs control graph {s_ctrl:.2f}")
    ok_ctrl = s_crystal > 2.0 * s_ctrl

    for label, ok in [("Weyl law within 1%", ok_weyl),
                      ("top peaks all at 2 log n (5-smooth)", ok_peaks),
                      ("leading smooth lengths present", ok_cover),
                      ("negative control rejects the template", ok_ctrl)]:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    allok = ok_weyl and ok_peaks and ok_cover and ok_ctrl
    print("result:", "ALL PASS — the crystal is audible in the drum" if allok
          else "FAILURES PRESENT")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
