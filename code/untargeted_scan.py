import numpy as np, math
M = 1010003
spf = list(range(M+1))
for i in range(2, int(M**0.5)+1):
    if spf[i] == i:
        for j in range(i*i, M+1, i):
            if spf[j] == j: spf[j] = i
allp = [p for p in range(2, M+1) if spf[p] == p]
h = {2: 0}
for p in allp[1:]:
    m = p-1; best = 0
    while m > 1:
        f = spf[m]; best = max(best, h[f])
        while m % f == 0: m //= f
    h[p] = 1 + best
def stats(n):
    Om = om = 0; Pm = 1; sf = 1; m = n
    while m > 1:
        f = spf[m]; om += 1; e = 0
        while m % f == 0: m //= f; e += 1
        Om += e; Pm = f
        if e > 1: sf = 0
    return Om, om, Pm, sf
P = [p for p in allp if 10**5 <= p < 10**6]
nxt = {allp[i]: allp[i+1] for i in range(len(allp)-1)}
names = ["Om(p-1)", "Om(p+1)", "slope P(p-1)", "Pratt h", "gap/log p", "bits(p)", "om(p-1)", "sf((p-1)/2)", "chi4(p)"]
rows = []
for p in P:
    O1, o1, Pm1, _ = stats(p-1)
    O2, _, _, _ = stats(p+1)
    _, _, _, s2 = stats((p-1)//2)
    rows.append([O1, O2, math.log(Pm1)/math.log(p), h[p], (nxt[p]-p)/math.log(p),
                 bin(p).count("1"), o1, float(s2), 1.0 if p % 4 == 1 else -1.0])
X = np.array(rows); n, K = X.shape
strat = np.array([(p % 30)*4 + min(3, int((math.log(p)-math.log(1e5))/(math.log(1e6)-math.log(1e5))*4)) for p in P])
half = n // 2
def standardized(idx):
    Y = X[idx].copy(); st = strat[idx]
    for s in np.unique(st):
        m = st == s
        Y[m] = (Y[m] - Y[m].mean(axis=0)) / (Y[m].std(axis=0) + 1e-12)
    return Y, st
def measure(Y):
    same = {(i, j): float(np.mean(Y[:, i]*Y[:, j])) for i in range(K) for j in range(i+1, K)}
    cons = {(i, j): float(np.mean(Y[:-1, i]*Y[1:, j])) for i in range(K) for j in range(K)}
    return same, cons
rng = np.random.default_rng(20260803)
def nulls(Y, st, B=200):
    groups = [np.where(st == s)[0] for s in np.unique(st)]
    sA = {k: [] for k in [(i, j) for i in range(K) for j in range(i+1, K)]}
    sB = {k: [] for k in [(i, j) for i in range(K) for j in range(K)]}
    for _ in range(B):
        Ya = Y.copy()
        for g in groups:
            for f in range(K): Ya[g, f] = Y[rng.permutation(g), f]
        for k, v in measure(Ya)[0].items(): sA[k].append(v)
        Yb = Y.copy()
        for g in groups: Yb[g] = Y[rng.permutation(g)]
        for k, v in measure(Yb)[1].items(): sB[k].append(v)
    return sA, sB
res = {}
for tag, idx in (("disc", np.arange(half)), ("val", np.arange(half, n))):
    Y, st = standardized(idx)
    same, cons = measure(Y)
    sA, sB = nulls(Y, st)
    z = {}
    for k, v in same.items(): z[("same",)+k] = (v - np.mean(sA[k]))/(np.std(sA[k]) + 1e-15)
    for k, v in cons.items(): z[("cons",)+k] = (v - np.mean(sB[k]))/(np.std(sB[k]) + 1e-15)
    res[tag] = z
print(f"scan: {n} primes, {len(res['disc'])} pre-registered tests, thresholds |z|>=3.9 (disc) and |z|>=3.0 same sign (val)")
surv = [(k, res["disc"][k], res["val"][k]) for k in res["disc"]
        if abs(res["disc"][k]) >= 3.9 and abs(res["val"][k]) >= 3.0 and res["disc"][k]*res["val"][k] > 0]
surv.sort(key=lambda t: -abs(t[1]))
print(f"\nsurvivors: {len(surv)}")
for k, zd, zv in surv:
    typ, i, j = k
    lab = f"{names[i]} x {names[j]}" + ("  (same prime)" if typ == "same" else "  (consecutive)")
    print(f"  z_disc {zd:+7.1f}  z_val {zv:+7.1f}   {lab}")
near = sorted(((k, res["disc"][k], res["val"][k]) for k in res["disc"]), key=lambda t: -abs(t[1]))[len(surv):len(surv)+3]
print("\nloudest non-survivors (context):")
for k, zd, zv in near:
    typ, i, j = k
    print(f"  z_disc {zd:+7.1f}  z_val {zv:+7.1f}   {names[i]} x {names[j]}  ({'same' if typ=='same' else 'consec'})")
