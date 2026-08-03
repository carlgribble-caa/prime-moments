"""WP6 — skeleton-null scanner v2.1, run under registry/2026-08-03-scanner-v2-prereg.md
(prereg commit 930a091; predictions unchanged).

Instrument revision v2.0 -> v2.1, forced by first light (documented in the results
file): (a) two-tier standardization — congruence features (chi4, chi3) standardize
within size bands only, since mod-60 strata make them constant and v2.0 nulled their
own consecutive signal (the scanner finding its own bug, again); (b) consecutive
nulls permute whole rows within size bands; (c) a matched CONTROL population m = p+30
(identical mod-60 class, sizes, and gap chain; overwhelmingly composite) runs the
same battery, automating the audit question "is this survivor prime-specific?" —
survivors reproduced by the control are classified mechanical/skeleton, not
candidates. Pratt height is undefined off the primes and excluded from control
comparisons.
"""
import math

import numpy as np

M = 1010040
SEED = 20260803
B = 200
CONG = {8, 9}
AUTO = {5, 10, 11}
MECH_SAME = {frozenset({5, 10}), frozenset({5, 11}), frozenset({10, 11})}
NAMES = ["Om(p-1)", "Om(p+1)", "slope P(p-1)", "Pratt h", "gap/log p", "bits(p)",
         "om(p-1)", "sf((p-1)/2)", "chi4(p)", "chi3(p)", "tm(p)", "rs(p)"]
CLASSES = {0: "crystal", 1: "crystal", 2: "crystal", 3: "crystal", 4: "spacing",
           5: "automatic", 6: "crystal", 7: "crystal", 8: "congruence",
           9: "congruence", 10: "automatic", 11: "automatic"}


def sieve_spf(limit):
    spf = list(range(limit + 1))
    for i in range(2, int(limit ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


SPF = sieve_spf(M)
ALLP = [p for p in range(2, M + 1) if SPF[p] == p]
PRATT = {2: 0}
for p in ALLP[1:]:
    m, best = p - 1, 0
    while m > 1:
        f = SPF[m]
        best = max(best, PRATT[f])
        while m % f == 0:
            m //= f
    PRATT[p] = 1 + best


def stats(n):
    Om = om = 0
    Pm, sf = 1, 1
    m = n
    while m > 1:
        f = SPF[m]
        om += 1
        e = 0
        while m % f == 0:
            m //= f
            e += 1
        Om += e
        Pm = f
        if e > 1:
            sf = 0
    return Om, om, Pm, sf


def features_for(seq, gaps, use_pratt):
    rows = []
    for idx, p in enumerate(seq):
        O1, o1, Pm1, _ = stats(p - 1)
        O2, _, _, _ = stats(p + 1)
        _, _, _, s2 = stats((p - 1) // 2)
        bits = bin(p).count("1")
        pr = PRATT[p] if use_pratt else 0.0
        rows.append([O1, O2, math.log(Pm1) / math.log(p), pr,
                     gaps[idx] / math.log(p), bits, o1, float(s2),
                     1.0 if p % 4 == 1 else -1.0, 1.0 if p % 3 == 1 else -1.0,
                     1.0 if bits % 2 == 0 else -1.0,
                     1.0 if bin(p).count("11") % 2 == 0 else -1.0])
    return np.array(rows)


def strata_for(seq):
    coprime60 = sorted(r for r in range(60) if math.gcd(r, 60) == 1)
    cid = {r: i for i, r in enumerate(coprime60)}
    lo, hi = math.log(1e5), math.log(1e6)
    fine, band = [], []
    for p in seq:
        b = min(3, int((math.log(p) - lo) / (hi - lo) * 4))
        fine.append(cid[p % 60] * 4 + b)
        band.append(b)
    return np.array(fine), np.array(band)


def standardize(X, fine, band):
    Y = X.astype(float).copy()
    for f in range(X.shape[1]):
        strat = band if f in CONG else fine
        for s in np.unique(strat):
            m = strat == s
            Y[m, f] = (Y[m, f] - Y[m, f].mean()) / (Y[m, f].std() + 1e-12)
    return Y


def measure(Y, K):
    same = {(i, j): float(np.mean(Y[:, i] * Y[:, j])) for i in range(K)
            for j in range(i + 1, K)}
    cons = {(i, j): float(np.mean(Y[:-1, i] * Y[1:, j])) for i in range(K)
            for j in range(K)}
    return same, cons


def null_z(Y, fine, band, K, rng):
    fine_groups = [np.where(fine == s)[0] for s in np.unique(fine)]
    band_groups = [np.where(band == s)[0] for s in np.unique(band)]
    sA = {k: [] for k in [(i, j) for i in range(K) for j in range(i + 1, K)]}
    sB = {k: [] for k in [(i, j) for i in range(K) for j in range(K)]}
    for _ in range(B):
        Ya = Y.copy()
        for f in range(K):
            for g in (band_groups if f in CONG else fine_groups):
                Ya[g, f] = Y[rng.permutation(g), f]
        for k, v in measure(Ya, K)[0].items():
            sA[k].append(v)
        Yb = Y.copy()
        for g in band_groups:
            Yb[g] = Y[rng.permutation(g)]
        for k, v in measure(Yb, K)[1].items():
            sB[k].append(v)
    obs_same, obs_cons = measure(Y, K)
    z = {}
    for k, v in obs_same.items():
        z[("same", k)] = (v - np.mean(sA[k])) / (np.std(sA[k]) + 1e-15)
    for k, v in obs_cons.items():
        z[("cons", k)] = (v - np.mean(sB[k])) / (np.std(sB[k]) + 1e-15)
    return z


def main():
    print("scanner v2.1 (WP6) under prereg 930a091; instrument revisions documented")
    P = [p for p in ALLP if 10 ** 5 <= p < 10 ** 6]
    nxt = {ALLP[i]: ALLP[i + 1] for i in range(len(ALLP) - 1)}
    gaps = [nxt[p] - p for p in P]
    n = len(P)
    print(f"population: {n} primes; control: m = p + 30 (same mod-60 class, sizes, gaps)")

    X = features_for(P, gaps, use_pratt=True)
    fine, band = strata_for(P)
    Y = standardize(X, fine, band)
    K = X.shape[1]

    rng = np.random.default_rng(SEED)
    z_full = null_z(Y, fine, band, K, rng)
    half = n // 2
    z_h1 = null_z(Y[:half], fine[:half], band[:half], K, np.random.default_rng(SEED + 1))
    z_h2 = null_z(Y[half:], fine[half:], band[half:], K, np.random.default_rng(SEED + 2))

    # control population: p + 30 (skeleton-matched, overwhelmingly composite)
    C = [p + 30 for p in P]
    prime_frac = sum(1 for m in C if SPF[m] == m) / n
    Xc = features_for(C, gaps, use_pratt=False)
    fc, bc = strata_for(C)
    Yc = standardize(Xc, fc, bc)
    zc = null_z(Yc, fc, bc, K, np.random.default_rng(SEED + 3))

    survivors = []
    for key, z in z_full.items():
        if abs(z) >= 3.9:
            z1, z2 = z_h1[key], z_h2[key]
            if abs(z1) >= 3.0 and abs(z2) >= 3.0 and np.sign(z1) == np.sign(z) == np.sign(z2):
                survivors.append((key, z, z1, z2))
    survivors.sort(key=lambda t: -abs(t[1]))

    print(f"\nsurvivors: {len(survivors)}; control prime-contamination {prime_frac:.1%}")
    auto_violations = []
    counts = {"mechanical(prereg)": 0, "control-reproduced": 0, "prime-specific": 0}
    prime_specific = []
    for key, z, z1, z2 in survivors:
        kind, (i, j) = key
        name = f"{NAMES[i]} x {NAMES[j]} ({kind})"
        cls = "x".join(sorted({CLASSES[i], CLASSES[j]}))
        if kind == "same" and frozenset({i, j}) in MECH_SAME:
            verdict = "mechanical(prereg)"
        elif 3 not in (i, j) and abs(zc[key]) >= 3.0 and np.sign(zc[key]) == np.sign(z):
            verdict = "control-reproduced"
        else:
            verdict = "prime-specific"
            prime_specific.append((key, z))
        counts[verdict] += 1
        zc_txt = "   n/a" if 3 in (i, j) else f"{zc[key]:+6.1f}"
        print(f"  z={z:+8.1f} (halves {z1:+6.1f}/{z2:+6.1f}, control {zc_txt})  "
              f"{name:38s} [{cls}; {verdict}]")
        if verdict == "prime-specific" and (i in AUTO or j in AUTO):
            if not (kind == "same" and 5 in (i, j)):   # prereg carve-out: bits same-prime
                auto_violations.append((key, z))

    zc4, zc3, zgap = z_full[("cons", (8, 8))], z_full[("cons", (9, 9))], z_full[("cons", (4, 4))]
    fired = {k for k, _, _, _ in survivors}
    p1 = ("cons", (8, 8)) in fired and zc4 < 0
    p2 = ("cons", (9, 9)) in fired and zc3 <= -8
    p3 = ("cons", (4, 4)) in fired and zgap < 0
    p4 = len(auto_violations) == 0
    p5 = not any(kind == "same" and 8 in (i, j) for (kind, (i, j)), *_ in survivors)

    print(f"\ncommitted predictions (prereg 930a091):")
    print(f"  P1 chi4xchi4 cons fires, z<0:   z = {zc4:+6.1f}  [{'PASS' if p1 else 'FAIL'}]"
          f"   (control: {zc[('cons', (8, 8))]:+.1f})")
    print(f"  P2 chi3xchi3 cons fires, z<=-8: z = {zc3:+6.1f}  [{'PASS' if p2 else 'FAIL'}]"
          f"   (control: {zc[('cons', (9, 9))]:+.1f})")
    print(f"  P3 gapxgap cons fires, z<0:     z = {zgap:+6.1f}  [{'PASS' if p3 else 'FAIL'}]")
    print(f"  P4 theorem-null, automatic class: {len(auto_violations)} prime-specific "
          f"violations  [{'PASS' if p4 else 'FAIL'}]")
    print(f"  P5 v1 same-prime chi4 cluster absorbed: [{'PASS' if p5 else 'FAIL'}]")
    print(f"\naudit summary: {counts['mechanical(prereg)']} mechanical(prereg), "
          f"{counts['control-reproduced']} control-reproduced (not prime-specific), "
          f"{counts['prime-specific']} prime-specific")
    print("prime-specific survivors (for the ladder's upper stages):")
    for key, z in prime_specific:
        kind, (i, j) = key
        print(f"    z={z:+8.1f}  {NAMES[i]} x {NAMES[j]} ({kind})")

    allok = p1 and p2 and p3 and p4 and p5
    print(f"\nresult: {'P1-P5 ALL HOLD' if allok else 'DISCREPANCIES (report honestly)'}")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
