"""WP-C2 — stronger observers on the wheel-restricted residual.

C1 showed general compressors capture part of the wheel skeleton and nothing
beyond it. This instrument climbs the observer ladder: a trained observer
GIVEN the local congruence data (divisibility flags at the current and three
preceding positions — so skeleton-derivable structure, including the
Hardy-Littlewood short-range correlations, is baseline-representable) is
asked whether sequence HISTORY adds anything. WP9c hyperparameters and eps.
Plus: the parity stream of pi extended tenfold in height (10^6..10^8), and an
order-k entropy ladder (report only). A failed M2 goes up the audit ladder,
not into a headline. Runs under
registry/2026-08-08-compression-c2-prereg.md.
"""
import math
import time
import zlib

import numpy as np
from mpmath import mp

WLEN = 2 ** 20
N_LO = 10 ** 7 - WLEN
FLAG_PRIMES = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
NHIST = 24
EPS = 0.002
N_BIG = 10 ** 8
NPAR = 8192


def sieve_flags(lo, hi):
    n = hi
    flags = np.ones(n, dtype=bool)
    flags[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if flags[p]:
            flags[p * p::p] = False
    return flags[lo:hi]


def pi_digit_bits(count):
    old = mp.dps
    mp.dps = 6 * count + 30
    try:
        s = mp.nstr(+mp.pi, 6 * count + 20)
    finally:
        mp.dps = old
    digits = s.replace("3.", "", 1)
    return np.array([1 if int(digits[6 * k:6 * k + 6]) < 500000 else 0
                     for k in range(count)], dtype=np.uint8)


def logloss(p, y):
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def logistic_fit(X, y, iters=20, ridge=1e-3):
    Xb = np.hstack([X, np.ones((len(X), 1))])
    w = np.zeros(Xb.shape[1])
    for _ in range(iters):
        z = Xb @ w
        p = 1 / (1 + np.exp(-z))
        W = p * (1 - p) + 1e-9
        H = Xb.T @ (Xb * W[:, None]) + ridge * np.eye(Xb.shape[1])
        g = Xb.T @ (y - p) - ridge * w
        w = w + np.linalg.solve(H, g)
    return w


def logistic_pred(X, w):
    Xb = np.hstack([X, np.ones((len(X), 1))])
    return 1 / (1 + np.exp(-(Xb @ w)))


def stumps_fit(X, y, T=60, lr=0.1, nthresh=8):
    F = np.full(len(y), math.log(max(y.mean(), 1e-9) / max(1 - y.mean(), 1e-9)))
    model = [("bias", float(F[0]))]
    thresh = {}
    for j in range(X.shape[1]):
        qs = np.quantile(X[:, j], np.linspace(0.1, 0.9, nthresh))
        thresh[j] = np.unique(qs)
    for _ in range(T):
        p = 1 / (1 + np.exp(-F))
        r = y - p
        best = (0.0, None)
        for j in range(X.shape[1]):
            xj = X[:, j]
            for t in thresh[j]:
                m = xj <= t
                s1, s2 = abs(r[m].sum()), abs(r[~m].sum())
                score = s1 + s2
                if score > best[0]:
                    best = (score, (j, t))
        j, t = best[1]
        m = X[:, j] <= t
        p_ = 1 / (1 + np.exp(-F))
        h = p_ * (1 - p_) + 1e-9
        gL = r[m].sum() / h[m].sum()
        gR = r[~m].sum() / h[~m].sum()
        F = F + lr * np.where(m, gL, gR)
        model.append((j, float(t), float(lr * gL), float(lr * gR)))
    return model


def stumps_pred(X, model):
    F = np.full(len(X), model[0][1])
    for (j, t, gL, gR) in model[1:]:
        F = F + np.where(X[:, j] <= t, gL, gR)
    return 1 / (1 + np.exp(-F))


def cond_entropy(bits, k):
    if k == 0:
        p = bits.mean()
        return 0.0 if p in (0, 1) else float(
            -p * math.log2(p) - (1 - p) * math.log2(1 - p))
    ctx = np.zeros(len(bits) - k, dtype=np.int64)
    for j in range(k):
        ctx = ctx * 2 + bits[j:len(bits) - k + j]
    tgt = bits[k:]
    H, total = 0.0, len(tgt)
    for c in np.unique(ctx):
        m = ctx == c
        n1 = tgt[m].sum()
        n = m.sum()
        p = n1 / n
        if 0 < p < 1:
            H += (n / total) * (-p * math.log2(p) - (1 - p) * math.log2(1 - p))
    return float(H)


def main():
    t_start = time.time()
    gate = {}
    print("WP-C2: stronger observers on the residual.")
    print("prereg: registry/2026-08-08-compression-c2-prereg.md\n")

    window = sieve_flags(N_LO, 10 ** 7).astype(np.uint8)
    pos = np.array([i for i in range(WLEN) if math.gcd((N_LO + i) % 30, 30) == 1])
    bits = window[pos]
    nvals = N_LO + pos

    # features
    flags = np.stack([(nvals % p == 0).astype(float) for p in FLAG_PRIMES], axis=1)
    base_cols = [flags]
    for back in (1, 2, 3):
        rolled = np.roll(flags, back, axis=0)
        rolled[:back] = 0
        base_cols.append(rolled)
    trend = ((np.arange(len(bits)) - len(bits) / 2) / len(bits)).reshape(-1, 1)
    X_base = np.hstack(base_cols + [trend])
    hist = np.stack([np.concatenate([np.zeros(b, dtype=np.uint8), bits[:-b]])
                     for b in range(1, NHIST + 1)], axis=1).astype(float)
    dens = []
    for wlen in (64, 256):
        c = np.convolve(bits, np.ones(wlen), mode="full")[:len(bits)] / wlen
        dens.append(np.concatenate([[0.0], c[:-1]]).reshape(-1, 1))
    X_chal = np.hstack([X_base, hist] + dens)

    half = len(bits) // 2
    ytr, yho = bits[:half].astype(float), bits[half:].astype(float)
    results = {}
    for name, X in [("baseline", X_base), ("challenger", X_chal)]:
        Xtr, Xho = X[:half], X[half:]
        w = logistic_fit(Xtr, ytr)
        ll_log = logloss(logistic_pred(Xho, w), yho)
        model = stumps_fit(Xtr, ytr)
        ll_stump = logloss(stumps_pred(Xho, model), yho)
        results[name] = (ll_log, ll_stump)
        print(f"{name:>11s}: holdout log-loss  logistic {ll_log:.5f}  "
              f"stumps {ll_stump:.5f}")
    rho_tr = ytr.mean()
    ll_const = logloss(np.full(len(yho), rho_tr), yho)
    print(f"{'constant':>11s}: holdout log-loss {ll_const:.5f} (train-rate coin)")

    gain_base = ll_const - min(results["baseline"])
    okM1 = gain_base > 0.02
    gate["M1"] = okM1
    print(f"\ngate M1 (positive control, baseline gain > 0.02 nats): "
          f"{gain_base:+.4f}  [{'PASS' if okM1 else 'FAIL'}]")
    print(f"  N1 (gain in [0.10, 0.25]): "
          f"{'CONFIRMED' if 0.10 <= gain_base <= 0.25 else 'REFUTED'}")
    imp_log = results["baseline"][0] - results["challenger"][0]
    imp_stp = results["baseline"][1] - results["challenger"][1]
    okM2 = imp_log < EPS and imp_stp < EPS
    gate["M2"] = okM2
    print(f"gate M2 (history adds < {EPS} nats beyond skeleton): logistic "
          f"{imp_log:+.5f}, stumps {imp_stp:+.5f}  [{'PASS' if okM2 else 'FAIL'}]")
    print(f"  N2 (both <= 0.001): "
          f"{'CONFIRMED' if max(imp_log, imp_stp) <= 0.001 else 'REFUTED'}\n")

    # parity at height
    print(f"sieving to {N_BIG} for the parity stream ...", flush=True)
    n = N_BIG
    big = np.ones(n, dtype=bool)
    big[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if big[p]:
            big[p * p::p] = False
    xs = np.unique(np.round(10 ** 6 * 100 ** (np.arange(NPAR) / (NPAR - 1))
                            ).astype(np.int64))
    assert len(xs) == NPAR
    seg = np.add.reduceat(big.astype(np.int8), np.concatenate([[0], xs[:-1]]))
    parity = (np.cumsum(seg.astype(np.int64)) & 1).astype(np.uint8)
    ctrl = pi_digit_bits(NPAR)
    s_par = len(zlib.compress(np.packbits(parity).tobytes(), 9))
    s_ctl = len(zlib.compress(np.packbits(ctrl).tobytes(), 9))
    r3 = s_par / s_ctl
    okM3 = r3 >= 0.97
    gate["M3"] = okM3
    print(f"gate M3 (parity at height 10^6..10^8): ratio {r3:.4f} >= 0.97  "
          f"[{'PASS' if okM3 else 'FAIL'}]")
    print(f"  N3 (in [0.99, 1.03]): "
          f"{'CONFIRMED' if 0.99 <= r3 <= 1.03 else 'REFUTED'}\n")

    # entropy ladder (report only)
    import hashlib
    ctrl_bits = np.empty(len(bits), dtype=np.uint8)
    i, c = 0, 0
    rho = bits.mean()
    while i < len(bits):
        h = hashlib.sha256(f"WP-C2:{c}".encode()).digest()
        for j in range(0, 32, 4):
            if i >= len(bits):
                break
            ctrl_bits[i] = 1 if int.from_bytes(h[j:j + 4], "big") / 2 ** 32 < rho else 0
            i += 1
        c += 1
    print("entropy ladder (report; H_k residual vs matched control, bits/bit):")
    maxex = 0.0
    for k in [0, 2, 4, 8, 12]:
        hr, hc = cond_entropy(bits, k), cond_entropy(ctrl_bits, k)
        maxex = max(maxex, hc - hr)
        print(f"  k = {k:2d}: residual {hr:.4f}  control {hc:.4f}  "
              f"excess {hc - hr:+.4f}")
    print(f"  N4 (max excess reported): {maxex:+.4f} bits "
          f"(expected <= 0.01)\n")

    allok = all(gate.values())
    print("reading: the trained observer, handed the local congruence skeleton,")
    print("extracts the predicted divisibility content that zlib missed — and")
    print("sequence history adds " + ("nothing beyond it: the two-skeleton "
          "conjecture holds\nat the trained-observer class, and the parity "
          "stream stays coin-like\nan order of magnitude higher."
          if okM2 else "MORE than eps: the gain goes up the audit\nladder "
          "(leakage -> HL/skeleton-derivable -> known theorem -> candidate)\n"
          "before any word stronger than 'reading' is used."))
    print(f"\nresult: {'ALL GATES PASS' if allok else 'FAILURES PRESENT'}  "
          f"({time.time()-t_start:.0f}s)")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
