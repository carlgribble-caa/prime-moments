# Results: ML detector (WP9c)

Prereg: `2026-08-03-ml-detector-prereg.md`, commit `3a52d21` (not edited since).
Run: deterministic; 45 s.

| task | model | baseline | challenger | improvement | verdict |
|---|---|---|---|---|---|
| T1 chi4(next) | logistic | 0.66963 | 0.66978 | −0.00015 | below eps: PASS |
| T1 chi4(next) | stumps | 0.67089 | 0.67089 | +0.00000 | below eps: PASS |
| T2 large gap | logistic | 0.68956 | 0.68934 | +0.00022 | below eps: PASS |
| T2 large gap | stumps | 0.68683 | 0.68683 | +0.00001 | below eps: PASS |

- **Q1 PASS** — no crystal-native advantage ≥ eps (0.002 nats) on any task/model; the
  largest observed improvement (+0.00022) is an order below threshold and consistent
  with the prereg's power note.
- **Q2 PASS** — positive control: the skeleton-only baseline beats the coin on
  chi4(next) by 0.0235 nats. The detector *can* see structure of this size, and sees
  it exactly where the two-skeleton conjecture says it lives (the congruence chain).
- **Q3** — not triggered; nothing to audit.

Verdict: null harvest as predicted. The two-skeleton conjecture survives its first
nonlinear-detector audit: crystal-native features carry no next-prime information
beyond the skeleton, at the resolution this scale affords.
