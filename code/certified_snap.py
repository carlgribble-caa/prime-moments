import time, math
import numpy as np
from math import comb, log
import mpmath
from mpmath import iv

iv.prec = 260

def IV(a, b):
    try:
        return iv.mpf([a, b])
    except Exception:
        return mpmath.mpi(a, b)

def sieve(M):
    s = np.ones(M+1, bool); s[:2] = False
    for i in range(2, int(M**0.5)+1):
        if s[i]: s[i*i::i] = False
    return np.flatnonzero(s).astype(np.int64)

def stirling2_table(K):
    S = [[0]*(K+1) for _ in range(K+1)]
    S[0][0] = 1
    for r in range(1, K+1):
        for q in range(1, r+1):
            S[r][q] = q*S[r-1][q] + S[r-1][q-1]
    return S

FACT = [math.factorial(q) for q in range(20)]

def powersum(T, r, S2):
    if r == 0:
        return T
    tot = 0
    for q in range(1, r+1):
        tot += FACT[q]*S2[r][q]*comb(T+1, q+1)
    return tot

def cheb_int_polys(m, K):
    polys = [[1], [-3*m, 2]]
    for j in range(1, K):
        A = polys[j]; B = polys[j-1]
        C = [0]*(len(A)+1)
        for r, c in enumerate(A):
            C[r+1] += 4*c
            C[r]   += -6*m*c
        for r, c in enumerate(B):
            C[r] -= m*m*c
        polys.append(C)
    return polys[:K+1]

def poly_eval_int(coefs, x):
    v = 0
    for c in reversed(coefs):
        v = v*x + c
    return v

def extract_moments(m, Kmax, primes_below, S2):
    """Enclosures of  Mt[j] = sum over primes p in (m,2m] of Q_j(p)*ln p.
    Inputs: only m, primes <= m, and logs of ALL integers <= 2m.
    No prime in (m,2m] is ever identified."""
    n = 2*m
    Q = cheb_int_polys(m, Kmax)
    L = [iv.mpf(0) for _ in range(Kmax+1)]
    for i in range(2, n+1):
        li = iv.log(iv.mpf(i))
        base = 2*i - 3*m
        L[0] += li
        prev, cur = 1, base
        if Kmax >= 1:
            L[1] += cur*li
        for j in range(2, Kmax+1):
            nxt = 2*base*cur - m*m*prev
            L[j] += nxt*li
            prev, cur = cur, nxt
    Mt = list(L)
    for p in primes_below:
        p = int(p)
        lp = iv.log(iv.mpf(p))
        v = [0]*(Kmax+1)
        pa = p
        while pa <= n:
            T = n // pa
            PS = [powersum(T, r, S2) for r in range(Kmax+1)]
            for j in range(Kmax+1):
                acc = 0
                par = 1
                for r, c in enumerate(Q[j]):
                    acc += c * par * PS[r]
                    par *= pa
                v[j] += acc
            pa *= p
        for j in range(Kmax+1):
            Mt[j] -= v[j]*lp
    return Mt, Q

def design_P(m, K):
    j = np.arange(K+1); th = np.pi*(j+0.5)/(K+1); un = np.cos(th)
    tn = m*(un+3)/2; fn = tn/np.log(tn)
    return [float((2-(k == 0))/(K+1)*np.sum(fn*np.cos(k*th))) for k in range(K+1)]

def certify_residual(m, a, nodes, step):
    """Rigorous outer bounds for min/max of g(t)=t/ln t - P(t) on [m,2m].
    nodes: list of (t, fpart) with fpart an enclosure of t/ln t at integer t.
    Uses |g''| <= 1/(m ln^2 m) + (4/m^2) * sum |a_j| j^2(j^2-1)/3."""
    K = len(a)-1
    gl = None; gh = None
    mm = iv.mpf(m)
    for t, fpart in nodes:
        u = (iv.mpf(2*t) - iv.mpf(3*m))/mm
        s = iv.mpf(a[0])
        prev = iv.mpf(1); cur = u
        if K >= 1:
            s += iv.mpf(a[1])*u
        for jj in range(2, K+1):
            nxt = 2*u*cur - prev
            s += iv.mpf(a[jj])*nxt
            prev, cur = cur, nxt
        g = fpart - s
        lo, hi = g.a, g.b
        if gl is None or lo < gl: gl = lo
        if gh is None or hi > gh: gh = hi
    B2 = 1.0/(m*log(m)**2) + (4.0/m**2)*sum(abs(a[jj])*jj*jj*(jj*jj-1)/3.0 for jj in range(K+1))
    slack = mpmath.mpf(step*step)/8*mpmath.mpf(B2)*(1+mpmath.mpf('1e-12'))
    return gl - slack, gh + slack, float(slack)

def run(m, Kcands, step_div=4000):
    t0 = time.time()
    n = 2*m
    allp = sieve(n)
    below = allp[allp <= m]
    Kmax = max(Kcands)
    S2 = stirling2_table(Kmax)

    print(f"===== interval ({m}, {2*m}] =====")
    print(f"pipeline inputs: integer m, the {len(below)} primes <= {m}, logs of all integers <= {n}. interval primes: never touched.")

    Mt, Q = extract_moments(m, Kmax, below, S2)
    w = [float(x.b - x.a) for x in Mt]
    print(f"moment enclosure widths (absolute): min={min(w):.1e}  max={max(w):.1e}")

    step = max(1, m // step_div)
    nodes = []
    for t in range(m, n+1, step):
        tv = iv.mpf(t)
        nodes.append((t, tv/iv.log(tv)))
    if nodes[-1][0] != n:
        tv = iv.mpf(n); nodes.append((n, tv/iv.log(tv)))

    mu0 = Mt[0]
    for K in Kcands:
        a = design_P(m, K)
        gl, gh, slack = certify_residual(m, a, nodes, step)
        Shat = iv.mpf(0)
        for j in range(K+1):
            Shat += iv.mpf(a[j]) * (Mt[j] / iv.mpf(m**j))
        Senc = Shat + mu0*IV(gl, gh)
        lo, hi = Senc.a, Senc.b
        width = float(hi - lo)
        cl = int(mpmath.ceil(lo)); fl = int(mpmath.floor(hi))
        print(f"K={K}: certified residual range [{float(gl):+.3e}, {float(gh):+.3e}] (grid slack {slack:.1e})")
        print(f"      certified window width = {width:.4f}")
        if cl == fl:
            print(f"      >>> CERTIFIED DETERMINATION: sum of primes in ({m},{2*m}] = {fl}")
            det = fl
            break
        else:
            print(f"      window [{mpmath.nstr(lo,12)}, {mpmath.nstr(hi,12)}] holds more than one integer; raising K")
            det = None

    I = allp[(allp > m) & (allp <= n)]
    truth = int(I.sum())
    print(f"verification (sieve, OUTSIDE pipeline): true sum = {truth}  ->  match = {det == truth}")

    lnp = np.log(I.astype(float))
    maxdiff = 0.0
    for j in range(Kmax+1):
        direct = float(sum(poly_eval_int(Q[j], int(p))*lp for p, lp in zip(I, lnp)))
        loj, hij = float(Mt[j].a), float(Mt[j].b)
        mid = (loj + hij)/2
        rel = abs(direct-mid)/max(1.0, abs(direct))
        maxdiff = max(maxdiff, rel)
        assert loj - 1e-6*max(1, abs(mid)) <= direct <= hij + 1e-6*max(1, abs(mid))
    print(f"cross-check: extracted moments vs direct interval-prime computation, max rel diff = {maxdiff:.1e} (float-limited)")
    print(f"elapsed: {time.time()-t0:.1f}s\n")

if __name__ == "__main__":
    S2t = stirling2_table(6)
    for T in (7, 19):
        for r in range(0, 7):
            assert powersum(T, r, S2t) == sum(t**r for t in range(1, T+1))
    mtest = 30
    Qt = cheb_int_polys(mtest, 4)
    for i in (7, 31, 45, 60):
        u = (2*i - 3*mtest)/mtest
        for j in range(5):
            assert abs(poly_eval_int(Qt[j], i) - mtest**j*float(mpmath.chebyt(j, u))) < 1e-6*max(1, mtest**j*abs(float(mpmath.chebyt(j, u))))
    print("self-tests passed: exact Faulhaber power sums, integer Chebyshev ladder polys\n")

    run(1000, [5, 6, 7])
    run(10000, [7, 8])
    run(100000, [9, 10], step_div=20000)
