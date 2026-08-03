"""WP3 — the diffraction identity on the bench: Guinand-Weil as an exact pairing.

The rigorous statement behind the essay's diffraction chapter is the explicit
formula as an identity of tempered distributions: paired against an even test
function h (here a Gaussian of width 1 centred at +-t0), with
g(u) = (1/2pi) int h(r) e^{-iur} dr,

  sum_gamma h(gamma)  =  (1/2pi) int h(r) [Re psi(1/4 + ir/2) - log pi] dr
                          + h(i/2) + h(-i/2)
                          - 2 sum_{n>=2} Lambda(n)/sqrt(n) * g(log n),

the left sum over all nontrivial-zero ordinates (+-gamma, with multiplicity).
The left side is the zero comb read at h ("diffraction"); the right side is the
archimedean term, the pole term, and the Lambda/sqrt(n)-weighted log-prime comb.
The identity holds unconditionally (gamma complex if RH fails; all known zeros
are on the line, so the numerical left side samples real ordinates).

This script verifies the identity to ~1e-12 at six test centres: on-zero centres
(the "Bragg peaks"), off-zero centres (the identity holds there too — it is an
identity, not a fit), and t0 = 0, where the pole term h(+-i/2) carries the mass —
the essay's "bulk" subtraction, now a derivation rather than an instrument fix.

Test function: h(r) = exp(-(r-t0)^2/2) + exp(-(r+t0)^2/2)   (even, width 1)
  g(u)          = sqrt(2/pi) exp(-u^2/2) cos(t0 u)
  h(i/2)+h(-i/2) = 4 exp((1/4 - t0^2)/2) cos(t0/2)
"""
import time

from mpmath import mp, mpf, exp, cos, sqrt, pi, log, quad, digamma, re, zetazero

mp.dps = 30

NZEROS = 60          # zeros of zeta on the line, ordinates to ~190
NCUT = 40000         # prime side cut: exp(-(log n)^2/2) < 1e-24 beyond log n ~ 10.5
CENTRES = ["0", "14.134725141734693790457251983562",
           "17.5",
           "21.022039638771554992628479593896",
           "25.010857580145688763213790992562",
           "30.424876125859513210311897530584"]
LABELS = ["t0 = 0 (pole territory)", "gamma_1", "between zeros", "gamma_2",
          "gamma_3", "gamma_4"]


def h_at(r, t0):
    return exp(-((r - t0) ** 2) / 2) + exp(-((r + t0) ** 2) / 2)


def main():
    t_start = time.time()
    print("Guinand-Weil pairing checks (WP3): identity, not fit. dps =", mp.dps)

    print(f"computing {NZEROS} zeta zeros ...", flush=True)
    gammas = [zetazero(k).imag for k in range(1, NZEROS + 1)]

    print(f"sieving Lambda(n)/sqrt(n) to {NCUT} ...", flush=True)
    lam = [None] * (NCUT + 1)
    spf = list(range(NCUT + 1))
    for i in range(2, int(NCUT ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, NCUT + 1, i):
                if spf[j] == j:
                    spf[j] = i
    prime_terms = []   # (log n, Lambda(n)/sqrt(n))
    for n in range(2, NCUT + 1):
        p = spf[n]
        m = n
        while m % p == 0:
            m //= p
        if m == 1:
            prime_terms.append((log(n), log(p) / sqrt(n)))

    allok = True
    print()
    print(f"{'centre':34s} {'zero side':>16s} {'prime+smooth side':>18s} {'|diff|':>10s}")
    for t0s, label in zip(CENTRES, LABELS):
        t0 = mpf(t0s)

        zero_side = 2 * sum(h_at(g, t0) for g in gammas)

        arch = (1 / pi) * quad(
            lambda r: h_at(r, t0) * (re(digamma(mpf("0.25") + mpf("0.5") * 1j * r)) - log(pi)),
            [0, max(t0 - 8, 0), t0 + 8, t0 + 40])
        poles = 4 * exp((mpf(1) / 4 - t0 ** 2) / 2) * cos(t0 / 2)
        primes = -2 * sum(w * sqrt(2 / pi) * exp(-(u ** 2) / 2) * cos(t0 * u)
                          for (u, w) in prime_terms)
        rhs = arch + poles + primes

        diff = abs(zero_side - rhs)
        ok = diff < mpf("1e-9")
        allok &= ok
        print(f"{label:34s} {float(zero_side):16.9f} {float(rhs):18.9f} {float(diff):10.2e}"
              f"  [{'PASS' if ok else 'FAIL'}]")

    print()
    print("reading: at gamma_k centres the pairing is ~2 (the h-mass of one zero of the")
    print("comb); between zeros it is small but NONZERO and still matched exactly — the")
    print("equation is an identity of distributions, of which the essay's peak scan and")
    print("bulk subtraction are corollaries. At t0 = 0 the pole term h(+-i/2) carries")
    print("the budget: the 'bulk' of the raw experiment is the pole's exact term.")
    print(f"\nresult: {'ALL PASS' if allok else 'FAILURES PRESENT'}  ({time.time()-t_start:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
