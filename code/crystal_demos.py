# crystal_demos.py — reproduces every numerical table in "The multiplication crystal"
# Sections run independently; total runtime a few minutes. Requires: numpy, mpmath.

# ============================================================
# ==== ucomplex.py
# ============================================================
import sys
sys.setrecursionlimit(100000)
# --- u-space layer counts via the papers' block-recursive T (j=0), inlined ---
Tmemo = {}
def T(k, y):
    if y < (1 << k): return 0
    if k == 1: return y - 1
    key = (k, y); v = Tmemo.get(key)
    if v is not None: return v
    dmax = y >> (k-1); tot = 0; d = 2
    while d <= dmax:
        q = y // d; d2 = min(y // q, dmax)
        tot += (d2 - d + 1) * T(k-1, q); d = d2 + 1
    Tmemo[key] = tot; return tot

# --- Dirichlet-series side: coefficients of (zeta(s)-1)^k by convolution ---
N = 60
b = [0]*(N+1)
for n in range(2, N+1): b[n] = 1
def dconv(u, v):
    w = [0]*(N+1)
    for a in range(2, N+1):
        if u[a]:
            for c in range(2, N//a + 1):
                if v[c]: w[a*c] += u[a]*v[c]
    return w
t = {1: b}
for k in (2, 3, 4): t[k] = dconv(t[k-1], b)

ok = all(sum(t[k][2:y+1]) == T(k, y) for k in (2, 3, 4) for y in (10, 24, 40, 60))
print(f"coefficients of (zeta-1)^k  ==  u-space layer-k counts, all tested y up to 60: {ok}")
print(f"  example: sum of t_3(n), n<=60 = {sum(t[3][2:61])}  vs  T_3(60) = {T(3,60)}")

# --- pole order at s=1 equals layer dimension k ---
from mpmath import mp, zeta, log, mpf
mp.dps = 30
print("\nlayer k | fitted blow-up exponent near s=1 (should be -k)")
for k in (1, 2, 3, 4):
    e1, e2 = mpf('1e-3'), mpf('1e-5')
    f = lambda e: (zeta(1+e) - 1)**k
    slope = (log(f(e2)) - log(f(e1))) / (log(e2) - log(e1))
    print(f"   {k}    |   {float(slope):+.4f}")

# ============================================================
# ==== interior.py
# ============================================================
from mpmath import mp, mpc, mpf, zeta, exp, log, pi, quad, euler, factorial
mp.dps = 25
y = 10**5

# (1) the real-world way: fill the 2D tetrahedron (a,b >= 2, ab <= y) with 1's
T2 = sum(y//d - 1 for d in range(2, y//2 + 1))

# (2) the complex-world way: a tiny circle around the single point s = 1
f = lambda s: (zeta(s) - 1)**2 * exp(s*log(y)) / s
r = mpf('0.4')
I = quad(lambda th: f(1 + r*exp(mpc(0,1)*th)) * mpc(0,1)*r*exp(mpc(0,1)*th),
         [0, 2*pi]) / (2*pi*mpc(0,1))

# (3) the closed-form residue at s = 1
res = y*(log(y) + 2*euler - 3)

print(f"lattice count of the tetrahedron, T_2(10^5)      = {T2}")
print(f"tiny circle around s=1 (radius 0.4)              = {mp.nstr(I.real, 18)}  (imag ~ {mp.nstr(abs(I.imag), 2)})")
print(f"closed-form residue y(log y + 2*gamma - 3)       = {mp.nstr(res, 18)}")
print(f"circle vs residue agree to                       {mp.nstr(abs(I.real - res), 2)}")
print(f"count minus residue (the leftover music)         = {mp.nstr(T2 - res, 6)}   (~{float((T2-res)/y**0.5):.1f} sqrt(y))")

print("\nfactorials as interior data of e^s: residue of e^s / s^(k+1) at 0 vs 1/k!")
for k in (2, 3, 5, 8):
    Ik = quad(lambda th: exp(exp(mpc(0,1)*th)) * mpc(0,1)*exp(mpc(0,1)*th) / exp(mpc(0,1)*th*(k+1)),
              [0, 2*pi]) / (2*pi*mpc(0,1))
    print(f"  k={k}: contour = {mp.nstr(Ik.real, 15)}   1/k! = {mp.nstr(mpf(1)/factorial(k), 15)}")

# ============================================================
# ==== crystal_dim.py
# ============================================================
from mpmath import mp, zeta, findroot
import math, time
mp.dps = 25

rho = findroot(lambda s: zeta(s) - 2, 1.7)
C = -1/(rho * zeta(rho, derivative=1))
print(f"Moran equation zeta(s) = 2  ->  crystal dimension rho = {mp.nstr(rho, 13)}")
print(f"predicted total-tower law: G(y) ~ C * y^rho with C = {mp.nstr(C, 8)}\n")

N = 10**6
t0 = time.time()
F = [0]*(N+1); F[1] = 1
for q in range(1, N//2 + 1):
    fq = F[q]
    if fq:
        for n in range(2*q, N+1, q):
            F[n] += fq
G = 0; cum = {}
targets = {10**3, 10**4, 10**5, 10**6}
for n in range(1, N+1):
    G += F[n]
    if n in targets: cum[n] = G
print(f"(sieve of all ordered factorizations to 10^6 in {time.time()-t0:.0f}s)")
print(f"{'y':>9} {'G(y) = total boxes in tower':>28} {'C*y^rho':>14} {'ratio':>7}")
for y in sorted(cum):
    pred = float(C) * y**float(rho)
    print(f"{y:>9} {cum[y]:>28} {pred:>14.4g} {cum[y]/pred:>7.4f}")
sl = (math.log(cum[10**6]) - math.log(cum[10**5])) / math.log(10)
print(f"\nmeasured dimension (slope over last decade): {sl:.4f}   vs   rho = {float(rho):.4f}")

# ============================================================
# ==== landau.py
# ============================================================
from mpmath import mp, zetazero, log, cos, sqrt, pi, mpf
import time, math
mp.dps = 15
K = 300
t0 = time.time()
gammas = [zetazero(k).imag for k in range(1, K+1)]
T = gammas[-1]
print(f"computed {K} zeros in {time.time()-t0:.0f}s; T = gamma_{K} = {float(T):.2f}, T/2pi = {float(T/(2*pi)):.1f}")

def Lam(x):
    for p in range(2, x+1):
        if p*p > x:  return math.log(x)      # x prime
        if x % p == 0:
            y = x
            while y % p == 0: y //= p
            return math.log(p) if y == 1 else 0.0
    return 0.0

print(f"{'x':>3} {'D(x)':>7} {'Lambda(x)':>10}  verdict")
sig, noise = [], []
for x in range(30, 61):
    s = sum(cos(g*log(x)) for g in gammas)
    D = float(-(2*pi/T)*sqrt(x)*s)
    L = Lam(x)
    tag = 'PRIME' if L>0 and all(x%d for d in range(2,int(x**.5)+1)) else ('prime power' if L>0 else '')
    (sig if L>0 else noise).append((x, D))
    print(f"{x:>3} {D:>7.2f} {L:>10.2f}  {tag}")
print(f"\nmin detector over primes/powers: {min(d for _,d in sig):.2f}   max over composites: {max(d for _,d in noise):.2f}")
print("clean separation:", min(d for _,d in sig) > max(d for _,d in noise))

# ============================================================
# ==== hidden.py
# ============================================================
import numpy as np, math

# ---------- Demo A: diffract the primes' log-positions; look for Bragg peaks ----------
N = 200000
spf = np.zeros(N+1, dtype=np.int64)
for i in range(2, N+1):
    if spf[i] == 0: spf[i::i][spf[i::i] == 0] = i if False else spf[i::i][spf[i::i]==0]
# simpler smallest-prime-factor sieve
spf = np.zeros(N+1, dtype=np.int64)
for i in range(2, int(N**0.5)+1):
    if spf[i] == 0: spf[i*i::i] = np.where(spf[i*i::i]==0, i, spf[i*i::i])
ns, ws = [], []
for n in range(2, N+1):
    p = spf[n] if spf[n] else n
    m = n
    while m % p == 0: m //= p
    if m == 1:
        ns.append(n); ws.append(math.log(p)/math.sqrt(n))
ns = np.array(ns, dtype=np.float64); ws = np.array(ws)
ln = np.log(ns)
ts = np.arange(10.0, 35.0, 0.005)
F = np.empty(len(ts))
for i in range(0, len(ts), 400):
    tt = ts[i:i+400][:, None]
    F[i:i+400] = np.abs((ws[None, :] * np.exp(-1j*tt*ln[None, :])).sum(axis=1))
peaks = [(ts[i], F[i]) for i in range(1, len(ts)-1) if F[i] > F[i-1] and F[i] > F[i+1] and F[i] > 0.55*F.max()]
peaks = sorted(peaks, key=lambda p: -p[1])[:5]
peaks = sorted(p[0] for p in peaks)
known = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062]
print("Bragg peaks of the diffracted prime-power positions vs the Riemann zeros:")
for pk, z in zip(peaks, known):
    print(f"   peak at t = {pk:7.3f}    zero at {z:9.6f}    off by {abs(pk-z):.3f}")

# ---------- Demo B: last digits of consecutive primes (Lemke Oliver-Soundararajan) ----------
M = 10**7
sieve = bytearray([1])*(M+1); sieve[0]=sieve[1]=0
for i in range(2, int(M**0.5)+1):
    if sieve[i]: sieve[i*i::i] = b'\x00'*len(sieve[i*i::i])
digs = [1,3,7,9]; idx = {d:i for i,d in enumerate(digs)}
C = [[0]*4 for _ in range(4)]
prev = None
for p in range(7, M+1):
    if sieve[p]:
        d = p % 10
        if prev is not None: C[idx[prev]][idx[d]] += 1
        prev = d
print(f"\nnext-prime last digit given current last digit (row-normalized %), primes to 10^7:")
print("        -> 1      -> 3      -> 7      -> 9      (naive expectation: 25% each)")
for i,d in enumerate(digs):
    row = sum(C[i])
    print(f"  {d}:  " + "  ".join(f"{100*C[i][j]/row:6.2f}%" for j in range(4)))
same = sum(C[i][i] for i in range(4)); tot = sum(sum(r) for r in C)
print(f"  same-digit pairs overall: {100*same/tot:.2f}%  (naive 25%)")

# ============================================================
# ==== hidden2.py
# ============================================================
import numpy as np, math
N = 200000
spf = np.zeros(N+1, dtype=np.int64)
for i in range(2, int(N**0.5)+1):
    if spf[i] == 0:
        sl = spf[i*i::i]; sl[sl == 0] = i; spf[i*i::i] = sl
ns, ws = [], []
for n in range(2, N+1):
    p = spf[n] if spf[n] else n
    m = n
    while m % p == 0: m //= p
    if m == 1:
        ns.append(n); ws.append(math.log(p)/math.sqrt(n))
ns = np.array(ns, dtype=np.float64); ws = np.array(ws); ln = np.log(ns)
ts = np.arange(10.0, 35.0, 0.005)
G = np.empty(len(ts))
for i in range(0, len(ts), 400):
    tt = ts[i:i+400][:, None]
    F = (ws[None, :] * np.exp(-1j*tt*ln[None, :])).sum(axis=1)            # raw diffraction
    s = 0.5 + 1j*ts[i:i+400]
    bulk = (np.exp((1-s)*math.log(N)) - np.exp((1-s)*math.log(2))) / (1-s) # the pole's shout
    G[i:i+400] = np.abs(F - bulk)
peaks = [(ts[j], G[j]) for j in range(1, len(ts)-1) if G[j] > G[j-1] and G[j] > G[j+1] and G[j] > 0.5*G.max()]
peaks = sorted(sorted(peaks, key=lambda p: -p[1])[:5])
known = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062]
print("diffraction AFTER subtracting the bulk term — peaks vs Riemann zeros:")
for (pk, h), z in zip(peaks, known):
    print(f"   peak t = {pk:7.3f} (height {h:5.1f})    zero {z:9.6f}    off by {abs(pk-z):.3f}")

# ============================================================
# ==== symmetries.py
# ============================================================
from mpmath import mp, mpc, mpf, zeta, gamma, pi, zetazero, quad, exp
import time
mp.dps = 12

# (a) the exact mirror symmetry of the reciprocal crystal: xi(s) = xi(1-s)
mp.dps = 20
def xi(s): return mpf('0.5')*s*(s-1)*pi**(-s/2)*gamma(s/2)*zeta(s)
s0 = mpc('0.3', '7.2')
d = abs(xi(s0) - xi(1 - s0))
print(f"mirror check at s = 0.3+7.2i:  |xi(s) - xi(1-s)| = {mp.nstr(d, 3)}   (|xi(s)| = {mp.nstr(abs(xi(s0)), 3)})")

# (b) symmetry class of the spectrum: level repulsion vs GUE vs Poisson
mp.dps = 12
K = 500
t0 = time.time()
g = [zetazero(k).imag for k in range(1, K+1)]
print(f"({K} zeros in {time.time()-t0:.0f}s)")
sp = []
for i in range(K-1):
    mean = 2*pi/ (mp.log(g[i]/(2*pi)))
    sp.append(float((g[i+1]-g[i])/mean))
import math
bins = [(0,0.25),(0.25,0.5),(0.5,1.0),(1.0,1.5),(1.5,2.0),(2.0,9.9)]
def gue_p(s): return (32/pi**2)*s**2*exp(-4*s**2/pi)
print(f"{'spacing bin':>12} {'observed':>9} {'GUE':>7} {'Poisson':>8}")
for a,b in bins:
    obs = sum(1 for s in sp if a <= s < b)/len(sp)
    gue = float(quad(gue_p, [a,b]))
    poi = math.exp(-a) - math.exp(-b)
    print(f"{f'[{a},{b})':>12} {obs:>9.3f} {gue:>7.3f} {poi:>8.3f}")
print(f"smallest normalized spacing among {K-1}: {min(sp):.3f}   (Poisson would expect ~{(K-1)*(1-math.exp(-min(sp))):.0f} below it; we see 1)")

# ============================================================
# ==== rh_map.py
# ============================================================
import math
# --- layer coefficients t_k(n) by Dirichlet convolution (coefficients of (zeta-1)^k) ---
N = 300
b = [0]*(N+1)
for n in range(2, N+1): b[n] = 1
def dconv(u, v):
    w = [0]*(N+1)
    for a in range(2, N+1):
        if u[a]:
            for c in range(2, N//a + 1):
                if v[c]: w[a*c] += u[a]*v[c]
    return w
t = {1: b[:]}
k = 1
while (1 << (k+1)) <= N:
    k += 1
    t[k] = dconv(t[k-1], b)

# --- true Mobius by sieve ---
mu = [1]*(N+1); mu[0] = 0
for p in range(2, N+1):
    if mu[p] == 1 or mu[p] == -1:
        pass
mu = [0]*(N+1); mu[1] = 1
primes = []
sieve = [True]*(N+1)
for p in range(2, N+1):
    if sieve[p]:
        primes.append(p)
        for q in range(2*p, N+1, p): sieve[q] = False
def mob(n):
    m = 1
    for p in primes:
        if p*p > n: break
        if n % p == 0:
            n //= p
            if n % p == 0: return 0
            m = -m
    if n > 1: m = -m
    return m
mu = [0]*(N+1); mu[1] = 1
for n in range(2, N+1): mu[n] = mob(n)

ok = all(mu[n] == sum((-1)**kk * t[kk][n] for kk in t) for n in range(2, N+1))
print(f"identity mu(n) = alternating sum of u-space layer coefficients, n <= {N}: {ok}")

# --- Mertens function: the alternating layer count's running total, x up to 10^6 ---
X = 10**6
m = [1]*(X+1)   # mu sieve via standard method
m[0] = 0
mus = [1]*(X+1); mus[0] = 0
sv = [0]*(X+1)
mus = [1]*(X+1); mus[0] = 0
for p in range(2, X+1):
    if all(True for _ in ()) and sv[p] == 0:
        for q in range(p, X+1, p): 
            sv[q] = sv[q] or p
# simpler linear mobius sieve
mus = [0]*(X+1); mus[1] = 1
smallest = [0]*(X+1)
plist = []
for i in range(2, X+1):
    if smallest[i] == 0:
        smallest[i] = i; plist.append(i); mus[i] = -1
    for p in plist:
        if p > smallest[i] or i*p > X: break
        smallest[i*p] = p
        mus[i*p] = 0 if i % p == 0 else -mus[i]
M = 0; worst = (0, 0.0)
for x in range(1, X+1):
    M += mus[x]
    if x >= 100:
        r = abs(M)/math.sqrt(x)
        if r > worst[1]: worst = (x, r)
print(f"max |M(x)|/sqrt(x) for 100 <= x <= 10^6:  {worst[1]:.3f}  at x = {worst[0]}   (M(10^6) = {M})")

# --- Lagarias's fully elementary costume of RH ---
sigma = [0]*(10**4+1)
for d in range(1, 10**4+1):
    for q in range(d, 10**4+1, d): sigma[q] += d
H = 0.0; minslack = (0, 1e18)
bad = 0
for n in range(1, 10**4+1):
    H += 1.0/n
    rhs = H + math.exp(H)*math.log(H) if H > 0 else 1.0
    slack = rhs - sigma[n]
    if slack < 0: bad += 1
    if n > 1 and slack < minslack[1]: minslack = (n, slack)
print(f"Lagarias inequality sigma(n) <= H_n + e^(H_n) log H_n holds for all n <= 10^4: {bad == 0}; tightest at n = {minslack[0]} (slack {minslack[1]:.2f})")


# ============================================================
# ==== mirror.py  (the F2[t] mirror: exact prime formula, tower, Mertens)
# ============================================================
# The mirror universe: F_2[t] — the crystal with quantized axis lengths
N = 14
def pmul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        a <<= 1; b >>= 1
    return r
def pdivmod(a, b):
    db = b.bit_length() - 1; q = 0
    while a.bit_length() - 1 >= db and a:
        sh = a.bit_length() - 1 - db
        q ^= 1 << sh; a ^= b << sh
    return q, a

monics = {d: [m | (1 << d) for m in range(1 << d)] for d in range(0, N+1)}
comp = set()
irred = {d: [] for d in range(1, N+1)}
for d in range(1, N+1):
    for f in monics[d]:
        if f not in comp: irred[d].append(f)
    for p in irred[d]:
        for e in range(d, N - d + 1):
            for m in monics[e]:
                comp.add(pmul(p, m))

def mobius_int(n):
    r, m = 1, n
    p = 2
    while p*p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0: return 0
            r = -r
        p += 1
    if m > 1: r = -r
    return r
print("(i) exact closed-form prime count:  #irred(n)  vs  (1/n) sum_{d|n} mu(d) 2^(n/d)")
ok = True
for n in range(1, N+1):
    formula = sum(mobius_int(d) * 2**(n//d) for d in range(1, n+1) if n % d == 0)//n
    ok &= (len(irred[n]) == formula)
print(f"    exact agreement for all degrees 1..{N}: {ok}   (e.g. deg 14: {len(irred[14])} irreducibles, formula {sum(mobius_int(d)*2**(14//d) for d in (1,2,7,14))//14})")

print("\n(ii) the tower (Kalmar mirror): W_n = total ordered factorizations at degree n  vs  2^(2n-1) exactly")
W = [1] + [0]*N
for n in range(1, N+1):
    W[n] = sum((1 << d) * W[n-d] for d in range(1, n+1))
print("    W_n == 2^(2n-1) for n=1..%d: %s   (dimension exactly 2 = 1 + log2/log q; no breathing)" % (N, all(W[n] == 1 << (2*n-1) for n in range(1, N+1))))

print("\n(iii) the Mertens mirror: sum of mu(f) over monic f of degree n")
def mu_poly(f):
    cnt = 0
    for d in range(1, f.bit_length()):
        for p in irred.get(d, []):
            if p.bit_length() > f.bit_length(): break
            q, r = pdivmod(f, p)
            if r == 0:
                q2, r2 = pdivmod(q, p)
                if r2 == 0: return 0
                cnt += 1; f = q
    return (-1)**cnt if f.bit_length() == 1 else 0  # fully factored
for n in range(1, 11):
    M = sum(mu_poly(f) for f in monics[n])
    print(f"    deg {n:>2}: Mertens = {M}", "(exactly zero — no random walk at all)" if n >= 2 else "")

# ============================================================
# ==== mirror2.py (layers, non-rigidity, Dirichlet, Hasse/RH, Sato-Tate)
# ============================================================
import math
# ---------- shared F2[t] machinery ----------
N = 12
def pmul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        a <<= 1; b >>= 1
    return r
def pdivmod(a, b):
    db = b.bit_length()-1; q = 0
    while a and a.bit_length()-1 >= db:
        sh = a.bit_length()-1-db; q ^= 1 << sh; a ^= b << sh
    return q, a
monics = {d: [m | (1 << d) for m in range(1 << d)] for d in range(0, N+1)}
comp = set(); irred = {d: [] for d in range(1, N+1)}
for d in range(1, N+1):
    for f in monics[d]:
        if f not in comp: irred[d].append(f)
    for p in irred[d]:
        for e in range(d, N-d+1):
            for m in monics[e]: comp.add(pmul(p, m))

# ---------- (iv) chapter 2 mirror: layer counts are exact binomials ----------
K = 6
T = [[0]*(N+1) for _ in range(K+1)]; T[0][0] = 1
for k in range(1, K+1):
    for n in range(1, N+1):
        T[k][n] = sum((1 << d)*T[k-1][n-d] for d in range(1, n+1))
ok = all(T[k][n] == (1 << n)*math.comb(n-1, k-1) for k in range(1, K+1) for n in range(k, N+1))
print(f"(iv) layer counts: t_k(deg n) == 2^n * C(n-1, k-1) exactly, all k<=6, n<=12: {ok}")
print(f"     (mirror of the divisor problems: closed-form binomials, zero error term)")

# ---------- (v) chapter 5 mirror: arithmetic is NOT rigid ----------
pw = [1]
for i in range(N+1): pw.append(pmul(pw[-1], 0b11))     # powers of (t+1)
def sub_t_plus_1(f):
    r = 0; i = 0
    while f:
        if f & 1: r ^= pw[i]
        f >>= 1; i += 1
    return r
allperm = True; fixed = {}
for d in range(1, N+1):
    img = sorted(sub_t_plus_1(f) for f in irred[d])
    allperm &= (img == sorted(irred[d]))
    fixed[d] = sum(1 for f in irred[d] if sub_t_plus_1(f) == f)
print(f"\n(v) the substitution t -> t+1 permutes the irreducibles of every degree <= {N}: {allperm}")
print(f"     fixed irreducibles by degree: {[fixed[d] for d in range(1, N+1)]}   (a genuine symmetry of the mirror's arithmetic)")

# ---------- (vi) point-group mirror: Dirichlet equidistribution mod t^2+t+1 ----------
m = 0b111
print(f"\n(vi) irreducibles by residue class mod t^2+t+1 (classes 1, t, t+1):")
for n in (6, 9, 12):
    cnt = {1:0, 2:0, 3:0}
    for f in irred[n]:
        _, r = pdivmod(f, m); cnt[r] += 1
    tot = sum(cnt.values())
    print(f"     deg {n:>2}: {cnt[1]:>5} {cnt[2]:>5} {cnt[3]:>5}   (max deviation from equal split: {max(abs(c-tot/3) for c in cnt.values())/tot*100:.2f}%)")

# ---------- (vii) chapter 4 mirror: verify RH (Hasse) on a curve ----------
P = 3000
sieve = bytearray([1])*(P+1); sieve[0]=sieve[1]=0
for i in range(2, int(P**0.5)+1):
    if sieve[i]: sieve[i*i::i] = b'\x00'*len(sieve[i*i::i])
primes = [p for p in range(3, P+1) if sieve[p] and p != 31]   # bad reduction at 2, 31
samples = []; worst = 0.0
for p in primes:
    s = 0
    for x in range(p):
        v = (x*x*x + x + 1) % p
        if v == 0: continue
        s += 1 if pow(v, (p-1)//2, p) == 1 else -1
    ap = -s
    assert ap*ap <= 4*p, ("HASSE VIOLATED", p)
    samples.append(ap/(2*math.sqrt(p)))
    worst = max(worst, abs(ap)/(2*math.sqrt(p)))
print(f"\n(vii) RH verified on E: y^2 = x^3 + x + 1 at all {len(primes)} good primes <= {P}:")
print(f"      every |a_p| <= 2*sqrt(p); tightest approach to the bound: {worst:.4f} of it")

# ---------- (viii) chapter 5 statistics mirror: Sato-Tate (a proven law) ----------
bins = [(-1,-0.6),(-0.6,-0.2),(-0.2,0.2),(0.2,0.6),(0.6,1.0)]
def semi(a, b):
    F = lambda t: (t*math.sqrt(1-t*t) + math.asin(t))/math.pi
    return F(b) - F(a)
print(f"\n(viii) angle statistics of the {len(samples)} normalized traces vs the (proven) Sato-Tate law:")
print(f"      {'bin':>14} {'observed':>9} {'Sato-Tate':>10}")
for a,b in bins:
    obs = sum(1 for x in samples if a <= x < b)/len(samples)
    print(f"      {f'[{a},{b})':>14} {obs:>9.3f} {semi(a,b):>10.3f}")

# ============================================================
# ==== tower.py (vertical RH: two zeros predict the whole extension tower)
# ============================================================
import math, time
p = 5
inv5 = [0, 1, 3, 2, 4]
def pmul(a, b):
    r = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i+j] = (r[i+j] + x*y) % p
    while len(r) > 1 and r[-1] == 0: r.pop()
    return r
def pmod(a, f):
    a = a[:]
    while len(a) >= len(f):
        c = a[-1]
        if c:
            sh = len(a)-len(f)
            for i in range(len(f)): a[sh+i] = (a[sh+i] - c*f[i]) % p
        a.pop()
    while len(a) > 1 and a[-1] == 0: a.pop()
    return a
def ppowmod(b, e, f):
    r = [1]; b = pmod(b, f)
    while e:
        if e & 1: r = pmod(pmul(r, b), f)
        b = pmod(pmul(b, b), f); e >>= 1
    return r
def norm(x):
    x = x[:]
    while len(x) > 1 and x[-1] == 0: x.pop()
    return x
def pgcd(a, b):
    a, b = norm(a), norm(b)
    while any(b):
        c = inv5[b[-1]]
        b = [(x*c) % p for x in b]
        a, b = b, norm(pmod(a, b))
    return a
def is_irred(f, n):
    u = [0, 1]
    if ppowmod(u, p**n, f) != pmod(u, f): return False
    for r in set(k for k in (2,3,5,7) if n % k == 0):
        A = ppowmod(u, p**(n//r), f); B = pmod(u, f)
        L = max(len(A), len(B))
        g = [((A[i] if i < len(A) else 0) - (B[i] if i < len(B) else 0)) % p for i in range(L)]
        g = norm(g)
        if any(g):
            h = pgcd(f[:], g)
            if len(h) > 1: return False
        else:
            return False
    return True
def find_irr(n):
    if n == 1: return [0, 1]
    for c in range(p**n):
        f = []
        cc = c
        for _ in range(n): f.append(cc % p); cc //= p
        f.append(1)
        if is_irred(f, n): return f
    raise RuntimeError

def enc(coeffs, n):
    v = 0
    for c in reversed(coeffs + [0]*(n - len(coeffs))): v = v*p + c
    return v
def dec(v, n):
    c = []
    for _ in range(n): c.append(v % p); v //= p
    return c

E = lambda w: None
print("curve E: y^2 = x^3 + x + 1 over F_5 and its extension tower")
results = []
t0 = time.time()
for n in range(1, 8):
    f = find_irr(n); q = p**n
    sq_of = [0]*q; squares = set()
    for v in range(q):
        c = dec(v, n)
        s = enc(pmod(pmul(c, c), f), n)
        sq_of[v] = s; squares.add(s)
    count = 1                                     # point at infinity
    one = enc([1], n)
    for v in range(q):
        x3 = enc(pmod(pmul(dec(sq_of[v], n), dec(v, n)), f), n)
        cw = [(a + b) % p for a, b in zip(dec(x3, n), dec(v, n))]
        cw[0] = (cw[0] + 1) % p
        w = enc(cw, n)
        if w == 0: count += 1
        elif w in squares: count += 2
    results.append((n, q, count))
N1 = results[0][2]; a = p + 1 - N1
print(f"base count over F_5: {N1} points  ->  a = {a};  zero pair alpha = ({a} +/- i*sqrt({4*p-a*a}))/2,  |alpha|^2 = {(a*a + (4*p-a*a))//4} exactly")
print(f"discriminant a^2 - 4p = {a*a-4*p} < 0: the two zeros form a conjugate pair ON the circle |alpha| = sqrt(5)  (this IS the curve's RH)\n")
t_ = [2, a]
print(f"{'n':>2} {'q=5^n':>7} {'brute-force #E':>15} {'predicted q+1-t_n':>18} {'match':>6} {'|t_n| / 2*5^(n/2)':>18}")
allok = True
for n, q, cnt in results:
    while len(t_) <= n: t_.append(a*t_[-1] - p*t_[-2])
    pred = q + 1 - t_[n]
    ok = (cnt == pred); allok &= ok
    print(f"{n:>2} {q:>7} {cnt:>15} {pred:>18} {str(ok):>6} {abs(t_[n])/(2*q**0.5):>18.4f}")
print(f"\nall seven extension counts exactly predicted by the two zeros: {allok}   ({time.time()-t0:.0f}s)")

# ============================================================
# ==== interp.py (de-quantization: the temperament ladder between universes)
# ============================================================
import math, cmath
from mpmath import mp, findroot
mp.dps = 25
L2, L3 = math.log(2), math.log(3)

# --- the temperament ladder: convergents of log2(3) ---
x = L3/L2; a = []; xx = x
for _ in range(9):
    ai = int(xx); a.append(ai); xx = 1/(xx - ai)
h, ph, k, pk = a[0], 1, 1, 0
conv = [(a[0], 1)]
for ai in a[1:]:
    h, ph, k, pk = ai*h + ph, h, ai*k + pk, k
    conv.append((h, k))
print("de-quantization ladder: two-length crystals {2, 2^(p/q)},  p/q -> log2(3) = 1.58496...")
print(f"{'p/q':>9} {'temperament q':>13} {'dimension D':>12} {'comb lines':>10} {'comb spacing':>13}")
target = float(findroot(lambda s: 2**(-s) + 3**(-s) - 1, 0.8))
for p, q in conv[2:]:
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi)/2
        if mid**q + mid**p < 1: lo = mid
        else: hi = mid
    D = -q*math.log(lo)/math.log(2)
    print(f"{p:>4}/{q:<4} {q:>13} {D:>12.6f} {p:>10} {2*math.pi*q/math.log(2):>13.1f}")
print(f"{'{2,3}':>9} {'(aperiodic)':>13} {target:>12.6f} {'infinite':>10} {'none':>13}")

# --- rung one is Fibonacci exactly ---
W = [1, 1]
for n in range(2, 61): W.append(W[-1] + W[-2])
phi = (1 + 5**0.5)/2
ok = all(W[n] == round(phi**(n+1)/5**0.5) for n in range(61))
print(f"\nrung {{2,4}}: tower counts are Fibonacci and equal round(phi^(n+1)/sqrt5) for all n <= 60: {ok}")

# --- the true {2,3} system: complex dimensions scatter (float Newton) ---
def g(s):  return cmath.exp(-s*L2) + cmath.exp(-s*L3) - 1
def gp(s): return -L2*cmath.exp(-s*L2) - L3*cmath.exp(-s*L3)
roots = {}
t = 0.0
while t <= 50:
    for s0r in (0.8, 0.4, 0.0, -0.5, -1.0):
        s = complex(s0r, t)
        try:
            for _ in range(60):
                d = gp(s)
                if abs(d) < 1e-14 or abs(s) > 60: break
                sn = s - g(s)/d
                if abs(sn - s) < 1e-13: s = sn; break
                s = sn
            if abs(s) < 60 and abs(g(s)) < 1e-11 and -2 < s.real < 1.2 and -0.01 <= s.imag <= 50:
                roots[(round(s.real, 5), round(abs(s.imag), 5))] = complex(s.real, abs(s.imag))
        except OverflowError:
            continue
    t += 0.4
rs = sorted(roots.values(), key=lambda z: z.imag)
print(f"\ncomplex dimensions of the non-lattice {{2,3}} crystal (first 12 of {len(rs)} found, t <= 50):")
for r in rs[:12]:
    print(f"   s = {r.real:+8.5f} + {r.imag:7.4f} i")
res = [r.real for r in rs]
print(f"real parts spread over [{min(res):.5f}, {max(res):.5f}]; rightmost root: {max(res):.5f} (the real dimension, alone on its line)")

# ============================================================
# ==== weldlab.py
# ============================================================
import numpy as np, math

# ---------- Mode A: add ALL primes -> the banded comet, then collapse it ----------
N = 200000
sieve = np.ones(N+1, dtype=bool); sieve[:2] = False
for i in range(2, int(N**0.5)+1):
    if sieve[i]: sieve[i*i::i] = False
ind = np.zeros(N+1); ind[sieve] = 1.0
R = np.fft.irfft(np.fft.rfft(ind, 2**19)**2, 2**19)   # ordered pair counts
C2 = 0.6601618158
def s_of(n):
    s = 1.0; m = n
    p = 3
    while p*p <= m:
        if m % p == 0:
            s *= (p-1)/(p-2)
            while m % p == 0: m //= p
        p += 2
    if m > 2 and m % 2 == 1: s *= (m-1)/(m-2)
    return s
lo, hi = 50000, 100000
ratios, band3, band_not3 = [], [], []
for n in range(lo, hi+1, 2):
    r = R[n]
    if r < 1: continue
    base = r * math.log(n)**2 / n
    (band3 if n % 3 == 0 else band_not3).append(base)
    ratios.append(base / (2*C2*s_of(n)))
ratios = np.array(ratios)
print(f"Mode A — the comet and its collapse ({len(ratios)} even N in [5e4, 1e5]):")
print(f"  raw bands:  mean R*ln^2N/N for 3|N: {np.mean(band3):.3f}   for 3 not| N: {np.mean(band_not3):.3f}   ratio {np.mean(band3)/np.mean(band_not3):.3f}  (Hardy-Littlewood predicts 2)")
print(f"  after dividing by the singular series: mean ratio {ratios.mean():.4f}, relative spread {ratios.std()/ratios.mean()*100:.2f}%  (stripes collapse to one curve)")

# ---------- Mode B: crystal-neighbor selection (safe primes) ----------
M = 10**6
sv = np.ones(M+1, dtype=bool); sv[:2] = False
for i in range(2, int(M**0.5)+1):
    if sv[i]: sv[i*i::i] = False
safes = [p for p in range(3, M+1, 2) if sv[p] and (p-1) % 2 == 0 and sv[(p-1)//2]]
mod3 = {0:0, 1:0, 2:0}
for p in safes: mod3[p % 3] += 1
print(f"\nMode B — safe primes p = 2q+1 up to 10^6: {len(safes)} of them")
print(f"  residues mod 3:  0:{mod3[0]}  1:{mod3[1]}  2:{mod3[2]}   (the mode leaks a congruence: all but the exception 7 are = 2 mod 3)")
c1, c2m = mod3[1], mod3[2]
tot = len(safes)**2
print(f"  pairwise sums mod 3:  =1: {c2m*c2m/tot*100:.3f}%   =0: {2*c1*c2m/tot*100:.4f}%   =2: {c1*c1/tot*100:.6f}%")
print(f"  derived law: the ONLY sum of two safe primes that is 2 mod 3 is 7+7 = 14  (count of such ordered pairs: {c1*c1})")

# ---------- Mode C: spectral selection (sign of a_p on E: y^2 = x^3+x+1) ----------
P = 5000
labels = {}
for p in range(3, P+1):
    if not sv[p] or p == 31: continue
    s = 0
    for x in range(p):
        v = (x*x*x + x + 1) % p
        if v: s += 1 if pow(v, (p-1)//2, p) == 1 else -1
    ap = -s
    if ap: labels[p] = 1 if ap > 0 else -1
ps = sorted(labels)
eps = np.mean([labels[p] for p in ps])
num = den = 0
pset = set(ps)
for i, p in enumerate(ps):
    for q in ps[i:]:
        if p + q > P + 3000: break
        num += labels[p]*labels[q]; den += 1
T = num/den
print(f"\nMode C — spectral labels sign(a_p), {len(ps)} primes: mean label {eps:+.4f}")
print(f"  pair-sum label correlation over {den} pairs: {T:+.5f}   vs independence prediction (mean)^2 = {eps*eps:+.5f}")
print(f"  excess structure: {abs(T - eps*eps):.5f}  (null: the spectral skeleton is additively silent)")

# ============================================================
# ==== recurse.py
# ============================================================
import math
M = 10**6
spf = list(range(M+1))
for i in range(2, int(M**0.5)+1):
    if spf[i] == i:
        for j in range(i*i, M+1, i):
            if spf[j] == j: spf[j] = i
primes = [p for p in range(2, M+1) if spf[p] == p]
pset = set(primes)

def is_prime(n):   # deterministic Miller-Rabin below 3.3e24
    if n < M+1: return n in pset if n <= M else None
    d, r = n-1, 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

# ---------- upward recursion: Cunningham chains as congruence amplifiers ----------
hist = {}
starts_by_len = {}
for q in primes:
    prev = (q-1)//2
    if q > 2 and (q-1) % 2 == 0 and prev in pset: continue      # not a chain start
    L, x = 1, q
    while True:
        nx = 2*x + 1
        if is_prime(nx): L += 1; x = nx
        else: break
    hist[L] = hist.get(L, 0) + 1
    starts_by_len.setdefault(L, []).append(q)
print("maximal Cunningham chains (first kind) starting below 10^6, by length:")
print("  " + "  ".join(f"len {k}: {hist.get(k,0)}" for k in sorted(hist)))
def support(minlen, mod):
    S = set()
    for k, qs in starts_by_len.items():
        if k >= minlen:
            for q in qs:
                if q > mod: S.add(q % mod)
    return sorted(S)
print("\nthe congruence amplifier — residues mod 30 of chain starts (small exceptions excluded):")
for k in (1, 2, 3):
    print(f"  chains of length >= {k}: support {support(k, 30)}")
print(f"  chains of length >= 4: support mod 210 has {len(support(4, 210))} of the 48 coprime residues")
print("  derived: len>=2 forces q = 5 mod 6; len>=3 adds q = 1,4 mod 5; len>=4 adds q = 2,4,5,6 mod 7 — each level halves-ish the world")

# ---------- downward recursion: Pratt trees are shallow ----------
h = {2: 0}
for p in primes[1:]:
    m = p - 1; best = 0
    while m > 1:
        f = spf[m]
        best = max(best, h[f])
        while m % f == 0: m //= f
    h[p] = 1 + best
big = [p for p in primes if p >= 10**5]
mx = max(h[p] for p in big); amax = max(big, key=lambda p: h[p])
mean = sum(h[p] for p in big)/len(big)
ll = math.log(math.log(5*10**5))
print(f"\nPratt trees for the {len(big)} primes in [10^5, 10^6]:")
print(f"  max height {mx} (at p = {amax}), mean height {mean:.2f},  mean / log log p = {mean/ll:.2f}")
print(f"  a certificate of primality for a million-scale prime is a recursion only ~{round(mean)} levels deep, grounded at 2")

# ============================================================
# ==== untargeted_scan.py
# ============================================================
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

# ============================================================
# ==== extract.py
# ============================================================
import math
N = 10**7
sieve = bytearray([1])*(N+1); sieve[0]=sieve[1]=0
for i in range(2, int(N**0.5)+1):
    if sieve[i]: sieve[i*i::i] = b'\x00'*len(sieve[i*i::i])
spf = list(range(N+1))
for i in range(2, int(N**0.5)+1):
    if spf[i] == i:
        for j in range(i*i, N+1, i):
            if spf[j] == j: spf[j] = i

def run(limit):
    h2 = {}; cls = {1: [0,0,0], -1: [0,0,0]}   # per class: [count, sum v2, sum Omega(p-1)]
    h3 = {}
    for p in range(3, limit+1):
        if not sieve[p]: continue
        m = p-1
        v2 = (m & -m).bit_length() - 1
        h2[v2] = h2.get(v2, 0) + 1
        v3 = 0; mm = m
        while mm % 3 == 0: v3 += 1; mm //= 3
        h3[v3] = h3.get(v3, 0) + 1
        Om = 0; q = m
        while q > 1:
            f = spf[q]
            while q % f == 0: q //= f; Om += 1
        c = 1 if p % 4 == 1 else -1
        cls[c][0] += 1; cls[c][1] += v2; cls[c][2] += Om
    return h2, h3, cls

for limit in (10**6, 10**7):
    h2, h3, cls = run(limit)
    tot = sum(h2.values())
    print(f"=== scale {limit:.0e}: {tot} odd primes ===")
    print("  Stage 1 — the 2-adic law, measured vs predicted 2^-k:")
    print("    k: " + "  ".join(f"{k}:{h2.get(k,0)/tot:.4f}/{2.0**-k:.4f}" for k in range(1, 7)))
    m_plus  = cls[1][1]/cls[1][0];  m_minus = cls[-1][1]/cls[-1][0]
    O_plus  = cls[1][2]/cls[1][0];  O_minus = cls[-1][2]/cls[-1][0]
    print(f"    E[v2 | chi4=+1] = {m_plus:.4f} (predict 3)    E[v2 | chi4=-1] = {m_minus:.4f} (predict 1)")
    print(f"    E[Omega(p-1)] class difference = {O_plus - O_minus:+.4f}   (theorem's corollary: -> 2)")
    tot3 = sum(h3.values())
    mean3 = sum(k*v for k, v in h3.items())/tot3
    print("  Stage 2 — PRE-REGISTERED 3-adic prediction 3^-k, mean 3/4:")
    print("    k: " + "  ".join(f"{k}:{h3.get(k,0)/tot3:.4f}/{3.0**-k if k>0 else 2/3:.4f}" for k in range(0, 5)))
    print(f"    measured mean v3 = {mean3:.4f}   (predicted 0.7500)\n")

# Stage 4 — the mirror: t-adic depth of f-1 over F2[t]
def pmul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        a <<= 1; b >>= 1
    return r
D = 12
monics = {d: [m | (1 << d) for m in range(1 << d)] for d in range(0, D+1)}
comp = set(); irr = []
irrd = {d: [] for d in range(1, D+1)}
for d in range(1, D+1):
    for f in monics[d]:
        if f not in comp: irrd[d].append(f)
    for p in irrd[d]:
        for e in range(d, D-d+1):
            for m in monics[e]: comp.add(pmul(p, m))
pool = irrd[10] + irrd[11] + irrd[12]
hv = {}
for f in pool:
    g = f ^ 1                      # f - 1 over F2
    v = (g & -g).bit_length() - 1
    hv[v] = hv.get(v, 0) + 1
tt = sum(hv.values())
mean = sum(k*v for k, v in hv.items())/tt
print(f"Stage 4 — PRE-REGISTERED mirror prediction over F2[t] ({tt} irreducibles, deg 10-12): P(v_t = k) = 2^-k, mean 2")
print("    k: " + "  ".join(f"{k}:{hv.get(k,0)/tt:.4f}/{2.0**-k:.4f}" for k in range(1, 6)))
print(f"    measured mean v_t(f-1) = {mean:.4f}   (predicted 2.0000)")
