# Results: the transfer law, out of sample (WP-RH5)

Prereg: `2026-08-07-transfer-law-prereg.md`, committed at `25e5e9e` before first
run. Instrument: `code/transfer_law.py` (77 s). Results are append-only.

## Gates and predictions

Out-of-sample window: zeros 301..400 (heights 544–680, ρ̄_w = 0.7285), disjoint
from every prior analysis. Integrity refit matched the recorded constants to
1e-4.

| m | τ | T_meas | Law A (DW) | Law B (linear) | \|dev A\| |
|---|---|---|---|---|---|
| 2 | 0.151 | 0.971 | 0.974 | 0.920 | 0.003 |
| 3 | 0.240 | 0.940 | 0.936 | 0.874 | 0.004 |
| 5 | 0.352 | 0.832 | 0.868 | 0.815 | 0.036 |
| 7 | 0.425 | 0.818 | 0.814 | 0.777 | 0.004 |

- **S1 (Law A out of sample): PASS** — all gated deviations < 0.08; three of
  four are < 0.005.
- **S2 (model selection): PASS** — gated SSE 0.00135 (A) vs 0.00892 (B): the
  Debye–Waller shape beats the linear/form-factor shape 6.6× on data neither
  fit ever saw.
- **Q1: CONFIRMED** — gated mean |dev| = 0.0119, three times inside the band.
- **Q2: REFUTED** — extended battery: m = 4 (0.029) and m = 11 (0.017) conform,
  but m = 13 deviates by 0.148; non-gated m = 8, 9 deviate by 0.25–0.29 (they
  were also anomalous in the HIGH window: 1.118, 0.307). Recorded as measured;
  candidate explanations (same-window deterministic fluctuations of the
  S-components; column correlations at 100 samples) are NOT adjudicated here.
  These frequencies are explicitly flagged in the conjecture's falsification
  protocol.
- **Q3: CONFIRMED** — the zero-parameter mechanism variant
  (a₃ = 2π²⟨u²⟩ = 1.317 from the window's own shifts) lands within 0.10 on the
  gated set.

## The lane's first labeled conjecture (per the programme's claims taxonomy)

**CONJECTURE (transfer law, WP-RH5).** Over a height window W with mean zero
density ρ̄_W, the per-frequency transfer of the prime comb into the zeros'
shift field satisfies

    T(ω; W) = exp( −a · (ω / 2π ρ̄_W)² ),   a = 2π² Var(S̄) + o(1)
    (a ≈ 1.14 at heights 14–680),

i.e. the transfer is the Debye–Waller factor of the zeros' unfolded
displacement field; the explicit-formula amplitudes are its τ → 0 limit.

**Falsification protocol:** (i) a fourth window at greater height with the same
frozen battery and gates; (ii) the anomalous frequencies m = 8, 9, 13 — the
conjecture as stated does not explain them, and a law that cannot be extended
to them (or a principled reason for their exclusion) fails the protocol;
(iii) the same measurement on Dirichlet L-functions, where the conjecture
predicts the same law with the corresponding density; (iv) derivation from the
explicit formula plus a pair-correlation input, which would promote it toward
ADOPTED/MACHINE and is the natural WP7-lane target.

Provenance chain, for the audit ladder: RH4 (slope-1 law refuted; attenuation
measured) → RH4b (height dependence confirmed, 4/4) → RH5 (two candidate laws
fitted in-sample and recorded, DW law confirmed out of sample). Three
preregistered instruments, three disjoint zero sets.

## Tie to the lane's restated problem (v2)

The v2 problem statement reads RH as criticality of the prime–zero feedback
loop. This conjecture is the loop's measured gain law: attenuated by the
Debye–Waller factor of the displacement field at finite height, tending to
lossless (T → 1) as the spectrum densifies. Proving the law from the explicit
formula plus a rigidity input is the partial-theorem target the lane's honest
pricing always pointed at.
