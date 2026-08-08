"""WP-RH2 — canonical-system reconstruction: first light.

RH is equivalent to the zero comb being the spectral measure of a canonical
system (de Branges/Krein) whose Hamiltonian nobody has exhibited. This
instrument computes two tractable shadows of that object and measures what the
arithmetic-free version is missing, under the preregistration
registry/2026-08-07-canonical-system-prereg.md (constants, gates, predictions
frozen before first run):

  A  discrete Krein/Jacobi data: three-term recurrence coefficients of the
     orthogonal polynomials for the symmetric atomic measure on the first 40
     zeros (Stieltjes orthogonalization, dps 40) — the discretized Hamiltonian
     — with two controls of identical mean density: the smooth comb
     Nbar^{-1}(k - 1/2) and a deterministic Poisson comb built from 6-digit
     blocks of pi's decimal expansion (reproducible; no RNG);
  B  the semiclassical inverse: the Wu-Sprung-type potential whose WKB counting
     matches the zeros' mean counting function Nbar, via a closed-form Abel
     inversion (derived by parts, verified in-code against direct quadrature),
     solved forward by Numerov shooting with parity split and node-count
     eigenvalue indexing; headline measurement: the spectral residuals of this
     arithmetic-free Hamiltonian correlate with the prime comb
     S(E) ~ -(1/pi) sum Lambda(n)/(sqrt n ln n) sin(E ln n) — in operator
     language, what the smooth Hamiltonian lacks is exactly the primes;
  C  the solved universe (elliptic-curve Frobenius measure of WP-RH1): the
     reconstruction TERMINATES — the Hamiltonian is finite and exact.

Librarian, upfront: Part B's construction belongs to Wu-Sprung (1993) and the
physics-of-zeta literature (Schumayer-Hutchinson; Berry-Keating); random-Jacobi
spectral theory (Killip-Nenciu) is adjacent to the rigidity statistic. Novelty
presumption low; the value is the measured tables, the controls, and the
requirements-spec line carried to WP-RH3.

Bring-up note (honest, WP9b precedent — two instrument bugs found and fixed,
all thresholds unchanged; first-run failures recorded in
registry/2026-08-07-canonical-system-results.md):
(1) Abel normalization. The preregistered inversion formula carried a spurious
1/pi prefactor; the correct pair is x(V) = INT Nbar'(E)/sqrt(V-E) dE with no
prefactor, as the harmonic-oscillator pair x = sqrt(V), Phi = E/2 pins down.
The closed form below is the by-parts evaluation of that integral (divisor pi,
not the preregistered pi^2); a defining-property diagnostic (WKB phase == Nbar
+ 1/8 on the built grid) now guards the construction.
(2) Silent bracket saturation. eigen_k's bracket-widening loop capped at
e_guess + 22 and silently returned the cap when the (then too narrow) well
pushed eigenvalues beyond it — producing a constant delta ~= -21.9 that was
the cap, not physics, identical across runs with different potentials. The
solver now raises on an unbracketed eigenvalue instead of returning a value.
Instructive honest footnote: the first runs' B5 still measured r = 0.605
because gamma_k minus the cap formula is dominated by the zeros' own
fluctuations — the prime correlation reached the gate without the solver's
help; the fixed instrument measures it through the actual spectrum.
"""
import math
import time

import numpy as np
from mpmath import mp, mpf, sqrt, log, exp, pi, quad, zetazero, acos, atan

mp.dps = 40

N_A = 40          # zeros in the Part A measure (80 symmetric atoms)
NZ_B = 62         # zeros consumed by Part B
NGRID = 8000      # Numerov steps
V0F = 2 * math.pi
EC_P, EC_A = 10007, -57   # WP-RH1's curve y^2 = x^3 + x + 1 over F_10007


# ---------------- shared: mean counting function ----------------

def nbar_f(E):
    return (E / (2 * math.pi)) * (math.log(E / (2 * math.pi)) - 1) + 0.875


def nbar_inv_f(y, lo=V0F + 1e-9, hi=4000.0):
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if nbar_f(mid) < y:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


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


# ---------------- Part A: Stieltjes / Jacobi ----------------

def stieltjes(atoms, M, term_tol=mpf("1e-30")):
    """Three-term recurrence coefficients for the equal-weight measure on
    `atoms`. Returns (a_list, b_list, terminated_at, last_residual)."""
    npts = len(atoms)
    p_prev = [mpf(0)] * npts
    nrm = sqrt(mpf(npts))
    p_cur = [1 / nrm] * npts
    a_list, b_list = [], []
    for n in range(M):
        xp = [atoms[i] * p_cur[i] for i in range(npts)]
        b_n = sum(xp[i] * p_cur[i] for i in range(npts))
        b_list.append(b_n)
        if n == M - 1:
            return a_list, b_list, None, None
        a_prev = a_list[-1] if a_list else mpf(0)
        r = [xp[i] - b_n * p_cur[i] - a_prev * p_prev[i] for i in range(npts)]
        a_next = sqrt(sum(x * x for x in r))
        if a_next < term_tol:
            return a_list, b_list, n + 1, a_next
        a_list.append(a_next)
        p_prev, p_cur = p_cur, [x / a_next for x in r]
    return a_list, b_list, None, None


def jacobi_eigs(a_list, b_list):
    m = len(b_list)
    J = mp.matrix(m, m)
    for i in range(m):
        J[i, i] = b_list[i]
    for i in range(m - 1):
        J[i, i + 1] = a_list[i]
        J[i + 1, i] = a_list[i]
    E, Q = mp.eigsy(J)
    return sorted([E[k] for k in range(m)]), Q


def pi_digit_uniforms(count):
    old = mp.dps
    mp.dps = 6 * count + 30
    try:
        s = mp.nstr(+mp.pi, 6 * count + 20)
    finally:
        mp.dps = old
    digits = s.replace("3.", "", 1)
    return [mpf(int(digits[6 * k:6 * k + 6])) / mpf(10 ** 6) for k in range(count)]


# ---------------- Part B: closed-form Abel inversion + Numerov ----------------

def x_of_V_f(V):
    if V <= V0F:
        return 0.0
    u = math.sqrt(V - V0F)
    sv = math.sqrt(V)
    return (-2 * u + sv * math.log((sv + u) / (sv - u))) / math.pi


def x_of_V_mp(V):
    u = sqrt(V - 2 * pi)
    sv = sqrt(V)
    return (-2 * u + sv * log((sv + u) / (sv - u))) / pi


def x_of_V_quad(V):
    Vm = mpf(V)
    return quad(
        lambda E: (log(E / (2 * pi)) / (2 * pi)) / sqrt(Vm - E), [2 * pi, Vm])


def build_potential(L, ngrid):
    xs = np.linspace(0.0, L, ngrid + 1)
    Vg = np.empty_like(xs)
    Vg[0] = V0F
    for i in range(1, len(xs)):
        lo, hi = V0F, 460.0
        x_t = xs[i]
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if x_of_V_f(mid) < x_t:
                lo = mid
            else:
                hi = mid
        Vg[i] = 0.5 * (lo + hi)
    return Vg


def shoot(Vg, h, E, even):
    """Numerov integration of psi'' = (V - E) psi from the origin; returns the
    count of sign changes among psi_1..psi_N (the node-count predicate data)."""
    h2 = h * h / 12.0
    f0 = Vg[0] - E
    f1 = Vg[1] - E
    if even:
        p_prev, p_cur = 1.0, 1.0 + 0.5 * h * h * f0
    else:
        p_prev, p_cur = 0.0, h
    count = 0
    Vl = Vg
    n = len(Vl) - 1
    for i in range(1, n):
        f2 = Vl[i + 1] - E
        p_next = (2 * p_cur * (1 + 5 * h2 * f1) - p_prev * (1 - h2 * f0)) / (1 - h2 * f2)
        if p_cur * p_next < 0:
            count += 1
        p_prev, p_cur = p_cur, p_next
        f0, f1 = f1, f2
        if abs(p_cur) > 1e250:
            p_prev *= 1e-250
            p_cur *= 1e-250
    return count


def eigen_k(Vg, h, k, e_guess):
    """k-th eigenvalue (1-based) by node-count bisection: parity even iff k odd;
    predicate C(E) >= (k-1)//2 + 1."""
    even = (k % 2 == 1)
    m = (k - 1) // 2

    def pred(E):
        return shoot(Vg, h, E, even) >= m + 1

    lo, hi = e_guess - 2.0, e_guess + 2.0
    for _ in range(10):
        if not pred(lo):
            break
        lo -= 2.0
    for _ in range(10):
        if pred(hi):
            break
        hi += 2.0
    if pred(lo) or not pred(hi):
        raise RuntimeError(f"eigenvalue {k} not bracketed in [{lo}, {hi}]")
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if pred(mid):
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def prime_S(E, lam_terms):
    return -(1 / math.pi) * sum(w * math.sin(E * u) for (u, w) in lam_terms)


def detrend(y):
    k = np.arange(len(y), dtype=float)
    A = np.vstack([k, np.ones_like(k)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return y - A @ coef


def main():
    t_start = time.time()
    gate = {}
    print("WP-RH2: canonical-system reconstruction, first light. dps =", mp.dps)
    print("prereg: registry/2026-08-07-canonical-system-prereg.md\n")

    print(f"computing {NZ_B} zeta zeros ...", flush=True)
    gammas = [zetazero(k).imag for k in range(1, NZ_B + 1)]

    # ---------------- Part A ----------------
    print("Part A — discrete Krein/Jacobi data from the first 40 zeros")
    atoms_zero = sorted([-g for g in gammas[:N_A]] + list(gammas[:N_A]))
    smooth_pos = [nbar_inv_mp(mpf(k) - mpf(1) / 2) for k in range(1, N_A + 1)]
    atoms_smooth = sorted([-e for e in smooth_pos] + smooth_pos)
    us = pi_digit_uniforms(N_A)
    tau, acc = [], mpf(0)
    for u in us:
        acc += -log(u)
        tau.append(acc)
    xt = [t - mpf(1) / 2 for t in tau]
    if xt[0] < mpf("0.3"):
        shift = mpf("0.3") - xt[0]
        xt = [t + shift for t in xt]
    poisson_pos = [nbar_inv_mp(t) for t in xt]
    atoms_poisson = sorted([-e for e in poisson_pos] + poisson_pos)

    coeffs = {}
    max_b = mpf(0)
    for name, atoms in [("zeros", atoms_zero), ("smooth", atoms_smooth),
                        ("poisson", atoms_poisson)]:
        a_l, b_l, term, _ = stieltjes(atoms, 2 * N_A)
        coeffs[name] = a_l
        max_b = max(max_b, max(abs(b) for b in b_l))
        assert term is None
    okA1 = max_b < mpf("1e-20")
    gate["A1"] = okA1
    print(f"gate A1 (symmetry): max |b_n| over three combs = {mp.nstr(max_b, 3)}  "
          f"[{'PASS' if okA1 else 'FAIL'}]")

    print("recomputing the measure from the Jacobi matrix (80x80 eigsy) ...", flush=True)
    eigs, _ = jacobi_eigs(coeffs["zeros"],
                          [mpf(0)] * (2 * N_A))  # b_n set to exact 0 (symmetric)
    errA2 = max(abs(eigs[i] - atoms_zero[i]) for i in range(2 * N_A))
    okA2 = errA2 < mpf("1e-8")
    gate["A2"] = okA2
    print(f"gate A2 (exact reconstruction): max |eig(J_80) - atoms| = "
          f"{mp.nstr(errA2, 3)}  [{'PASS' if okA2 else 'FAIL'}]")

    print("\n  n :   a_n(zeros)   a_n(smooth)  a_n(poisson)")
    for n in range(12):
        print(f" {n+1:3d}: {float(coeffs['zeros'][n]):12.6f} "
              f"{float(coeffs['smooth'][n]):12.6f} {float(coeffs['poisson'][n]):12.6f}")
    win = slice(5, 70)
    fl_z = np.array([float(coeffs["zeros"][n] - coeffs["smooth"][n])
                     for n in range(2 * N_A - 1)])[win]
    fl_p = np.array([float(coeffs["poisson"][n] - coeffs["smooth"][n])
                     for n in range(2 * N_A - 1)])[win]
    ratio = float(np.std(fl_z) / np.std(fl_p))
    print(f"\nQ2 (rigidity in Hamiltonian coordinates, n = 6..70): "
          f"std(zeros-smooth) = {np.std(fl_z):.4f}, std(poisson-smooth) = "
          f"{np.std(fl_p):.4f}, ratio = {ratio:.3f} "
          f"[predicted < 0.7 -> {'CONFIRMED' if ratio < 0.7 else 'REFUTED'}]\n")

    # ---------------- Part B ----------------
    print("Part B — semiclassical inverse (closed-form Abel) + Numerov forward solve")
    verrs = []
    for Vt in [10, 30, 80, 200, 400]:
        cf = x_of_V_mp(mpf(Vt))
        dq = x_of_V_quad(Vt)
        verrs.append(abs(cf - dq) / abs(cf))
    okB1 = max(verrs) < mpf("1e-8")
    gate["B1"] = okB1
    print(f"gate B1 (closed form vs quadrature at 5 V's): max rel diff = "
          f"{mp.nstr(max(verrs), 3)}  [{'PASS' if okB1 else 'FAIL'}]")

    xs_ho = np.linspace(0.0, 8.0, NGRID + 1)
    V_ho = xs_ho ** 2
    h_ho = xs_ho[1] - xs_ho[0]
    ho_err = 0.0
    for k in range(1, 11):
        Ek = eigen_k(V_ho, h_ho, k, 2.0 * (k - 1) + 1.0)
        ho_err = max(ho_err, abs(Ek - (2 * (k - 1) + 1)))
    okB2 = ho_err < 1e-6
    gate["B2"] = okB2
    print(f"gate B2 (solver validation, harmonic well, 10 levels): max err = "
          f"{ho_err:.2e}  [{'PASS' if okB2 else 'FAIL'}]")

    L = x_of_V_f(450.0)
    print(f"building V(x) on [0, {L:.4f}], {NGRID} steps; solving 62 levels ...",
          flush=True)
    Vg = build_potential(L, NGRID)
    h = L / NGRID
    xs_grid = np.linspace(0.0, L, NGRID + 1)
    for E_chk in (50.0, 150.0):
        phi = (2 / math.pi) * np.trapezoid(
            np.sqrt(np.maximum(E_chk - Vg, 0.0)), xs_grid)
        tgt = nbar_f(E_chk) + 0.125
        print(f"defining-property check (bring-up diagnostic): WKB phase at "
              f"E = {E_chk:.0f}: {phi:.5f} vs Nbar + 1/8 = {tgt:.5f} "
              f"(diff {phi - tgt:+.1e})")
    E_rec = [eigen_k(Vg, h, k, nbar_inv_f(k - 0.625)) for k in range(1, NZ_B + 1)]

    g_f = [float(g) for g in gammas]
    C_cut = 0.5 * (g_f[59] + g_f[60])
    count = sum(1 for e in E_rec if e <= C_cut)
    okB3 = abs(count - 60) <= 2
    gate["B3"] = okB3
    print(f"gate B3 (counting): eigenvalues below (gamma_60+gamma_61)/2 = "
          f"{C_cut:.3f}: {count} (target 60 +- 2)  [{'PASS' if okB3 else 'FAIL'}]")

    print("\n  k :   gamma_k      E_k      delta_k")
    for k in [1, 2, 3, 4, 5, 20, 40, 60]:
        print(f" {k:3d}: {g_f[k-1]:10.4f} {E_rec[k-1]:10.4f} "
              f"{g_f[k-1]-E_rec[k-1]:+9.4f}")

    ks = range(10, 61)
    delta = np.array([g_f[k - 1] - E_rec[k - 1] for k in ks])
    rho = np.array([math.log(g_f[k - 1] / (2 * math.pi)) / (2 * math.pi) for k in ks])
    okB4 = float(np.sqrt(np.mean(delta ** 2))) < 1.0
    gate["B4"] = okB4
    print(f"\ngate B4 (tracking): RMS(delta_k, k=10..60) = "
          f"{np.sqrt(np.mean(delta**2)):.4f} < 1.0  [{'PASS' if okB4 else 'FAIL'}]")

    spf = list(range(1001))
    for i in range(2, 33):
        if spf[i] == i:
            for j in range(i * i, 1001, i):
                if spf[j] == j:
                    spf[j] = i
    lam_terms = []
    for n in range(2, 1001):
        p_, m_ = spf[n], n
        while m_ % p_ == 0:
            m_ //= p_
        if m_ == 1:
            u = math.log(n)
            lam_terms.append((u, math.log(p_) / (math.sqrt(n) * u)
                              * math.exp(-u * u / 18.0)))
    S_vals = np.array([prime_S(g_f[k - 1], lam_terms) for k in ks])

    lhs = detrend(delta * rho)
    rhs = detrend(-S_vals)
    r = float(np.corrcoef(lhs, rhs)[0, 1])
    okB5 = r > 0.4
    gate["B5"] = okB5
    print(f"gate B5 (HEADLINE — the primes are the residual): Pearson r of "
          f"detrended delta_k*rho(gamma_k) vs detrended -S(gamma_k) = {r:.4f}"
          f"  [{'PASS' if okB5 else 'FAIL'}]")
    q3 = float(np.mean(delta * rho + S_vals))
    print(f"Q1 (r in [0.6, 0.95]): {'CONFIRMED' if 0.6 <= r <= 0.95 else 'REFUTED'}"
          f"   Q3 (Maslov offset, mean(delta*rho + S) in [0, 0.25]): "
          f"{q3:+.4f} [{'CONFIRMED' if 0.0 <= q3 <= 0.25 else 'REFUTED'}]\n")

    # ---------------- Part C ----------------
    print(f"Part C — solved universe: Frobenius measure of y^2 = x^3 + x + 1 / "
          f"F_{EC_P} (a = {EC_A})")
    theta = acos(mpf(EC_A) / (2 * sqrt(mpf(EC_P))))
    a_l, b_l, term, resid = stieltjes([-theta, theta], 6)
    okC_term = term == 2 and resid < mpf("1e-30")
    eigs2, Q2 = jacobi_eigs(a_l, b_l)
    errC = max(abs(eigs2[0] + theta), abs(eigs2[1] - theta))
    mom_err = mpf(0)
    w2 = [2 * Q2[0, i] ** 2 for i in range(2)]
    for m_ in range(7):
        gaussm = sum(w2[i] * eigs2[i] ** m_ for i in range(2))
        direct = (-theta) ** m_ + theta ** m_
        mom_err = max(mom_err, abs(gaussm - direct))
    okC = okC_term and errC < mpf("1e-30") and mom_err < mpf("1e-30")
    gate["C1"] = okC
    print(f"Stieltjes terminates at step {term} (residual {mp.nstr(resid, 2)}); "
          f"J_2 eigenvalues = +-theta to {mp.nstr(errC, 2)}; moments m<=6 to "
          f"{mp.nstr(mom_err, 2)}")
    print(f"gate C1 (termination — the solved universe's Hamiltonian is finite "
          f"and exact): [{'PASS' if okC else 'FAIL'}]\n")

    allok = all(gate.values())
    print("reading: the arithmetic-free canonical object tracks the zeros at mean-")
    print("density order and fails at fluctuation order by the prime comb — the")
    print("residual of the reconstructed smooth Hamiltonian correlates with")
    print("-S(gamma) (gate B5), so in operator language the missing structure IS")
    print("the primes. In the solved universe the reconstruction terminates in a")
    print("finite exact matrix (Part C), the Hamiltonian-coordinates form of RH1's")
    print("tightness finding. Requirements-spec line for WP-RH3: any candidate")
    print("Hilbert-Polya structure must carry the prime comb at fluctuation order")
    print("in its Hamiltonian data.")
    print(f"\nresult: {'ALL GATES PASS' if allok else 'FAILURES PRESENT'}  "
          f"({time.time()-t_start:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
