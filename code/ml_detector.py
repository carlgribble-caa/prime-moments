"""WP9c — ML detector, run under registry/2026-08-03-ml-detector-prereg.md
(prereg commit 3a52d21). Does any model using crystal-native features beat the
congruence-skeleton baseline at predicting next-prime data? Logistic regression and
boosted stumps, chronological holdout, eps = 0.002 nats.
"""
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scanner_v2 import ALLP, features_for, strata_for  # noqa: E402

EPS = 0.002


def logloss(y, p):
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return float(-np.mean(np.where(y > 0, np.log(p), np.log(1 - p))))


def fit_logistic(X, y, iters=20, ridge=1e-3):
    X1 = np.hstack([X, np.ones((len(X), 1))])
    w = np.zeros(X1.shape[1])
    for _ in range(iters):
        z = X1 @ w
        p = 1 / (1 + np.exp(-z))
        g = X1.T @ (p - (y > 0)) + ridge * w
        W = p * (1 - p) + 1e-6
        H = (X1 * W[:, None]).T @ X1 + ridge * np.eye(X1.shape[1])
        w -= np.linalg.solve(H, g)
    return lambda Xt: 1 / (1 + np.exp(-(np.hstack([Xt, np.ones((len(Xt), 1))]) @ w)))


def fit_stumps(X, y, T=120, nu=0.1, nthr=8, rng=None):
    n, d = X.shape
    thresholds = [np.quantile(X[:, j], np.linspace(0.1, 0.9, nthr)) for j in range(d)]
    F = np.zeros(n)
    model = []
    ybin = (y > 0).astype(float)
    for _ in range(T):
        p = 1 / (1 + np.exp(-F))
        r = ybin - p
        best = (0.0, None)
        for j in range(d):
            xj = X[:, j]
            for t in thresholds[j]:
                mask = xj <= t
                nl, nr = mask.sum(), n - mask.sum()
                if nl < 50 or nr < 50:
                    continue
                gl, gr = r[mask].mean(), r[~mask].mean()
                gain = nl * gl * gl + nr * gr * gr
                if gain > best[0]:
                    best = (gain, (j, t, gl, gr))
        if best[1] is None:
            break
        j, t, gl, gr = best[1]
        F += nu * np.where(X[:, j] <= t, gl, gr) * 4.0
        model.append((j, t, gl, gr))

    def predict(Xt):
        Ft = np.zeros(len(Xt))
        for j, t, gl, gr in model:
            Ft += nu * np.where(Xt[:, j] <= t, gl, gr) * 4.0
        return 1 / (1 + np.exp(-Ft))
    return predict


def main():
    t0 = time.time()
    print("ML detector (WP9c) under prereg 3a52d21: skeleton baseline vs crystal challenger")
    P = [p for p in ALLP if 10 ** 5 <= p < 10 ** 6]
    nxt = {ALLP[i]: ALLP[i + 1] for i in range(len(ALLP) - 1)}
    gaps = [nxt[p] - p for p in P]
    X = features_for(P, gaps, use_pratt=True)
    fine, band = strata_for(P)
    n = len(P)

    coprime60 = sorted(r for r in range(60) if math.gcd(r, 60) == 1)
    onehot = np.zeros((n, 16))
    for i, p in enumerate(P):
        onehot[i, coprime60.index(p % 60)] = 1.0
    sizecol = (np.log(np.array(P, float)) - math.log(1e5)) / (math.log(1e6) - math.log(1e5))

    base_cols = np.hstack([X[:, [8, 9]], onehot, sizecol[:, None]])
    crystal_cols = X[:, [0, 1, 2, 3, 6, 7, 5]]
    chall_cols = np.hstack([base_cols, crystal_cols])

    y1 = X[:, 8].copy()
    y1[:-1] = X[1:, 8]          # chi4 of next prime
    glog = np.array(gaps) / np.log(np.array(P, float))

    half = n // 2
    med = np.median(glog[:half])
    y2 = np.where(glog > med, 1.0, -1.0)

    usable = n - 1              # last prime has no next
    tr = slice(0, half)
    ho = slice(half, usable)

    results = {}
    for task, y in [("T1 chi4(next)", y1), ("T2 large gap", y2)]:
        for mname, fitter in [("logistic", fit_logistic), ("stumps", fit_stumps)]:
            for fname, cols in [("baseline", base_cols), ("challenger", chall_cols)]:
                mdl = fitter(cols[tr], y[tr])
                ll = logloss(y[ho], mdl(cols[ho]))
                results[(task, mname, fname)] = ll
    ln2 = math.log(2)
    print(f"\n{'task':14s} {'model':9s} {'baseline':>9s} {'challenger':>10s} {'improve':>9s}  verdict")
    q1 = True
    for task in ("T1 chi4(next)", "T2 large gap"):
        for mname in ("logistic", "stumps"):
            b = results[(task, mname, "baseline")]
            c = results[(task, mname, "challenger")]
            imp = b - c
            ok = imp < EPS
            q1 &= ok
            print(f"{task:14s} {mname:9s} {b:9.5f} {c:10.5f} {imp:+9.5f}  "
                  f"[{'below eps: PASS' if ok else 'ABOVE eps -> AUDIT'}]")
    b_lr = results[("T1 chi4(next)", "logistic", "baseline")]
    q2 = b_lr < ln2 - 1e-4
    print(f"\nQ2 positive control: baseline T1 log-loss {b_lr:.5f} vs coin {ln2:.5f}  "
          f"[{'PASS' if q2 else 'FAIL'}]  (LOS lives in the skeleton features)")
    print(f"Q1 no crystal advantage >= eps on any task/model: [{'PASS' if q1 else 'FAIL'}]")
    print(f"\nresult: {'NULL HARVEST AS PREDICTED' if q1 and q2 else 'DISCREPANCY - AUDIT'}"
          f"  ({time.time()-t0:.0f}s)")
    return 0 if q1 and q2 else 1


if __name__ == "__main__":
    raise SystemExit(main())
