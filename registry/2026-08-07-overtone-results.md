# Results: the overtone theory, first light (WP-RH7)

Prereg: `2026-08-07-overtone-prereg.md`, committed at `af03b78` before first
run. Instrument: `code/overtone.py` (105 s; 500 zeros). Results are
append-only.

## Gates and predictions

- **H1a/H1b (Landau input): PASS**, far inside the gates — measured/predicted
  ratios 1.003 (r = 2), 0.995 (r = 3), 0.966 (r = 4), 0.987 (r = 5), 0.977
  (r = 9): the phase-locking input verified at the percent level over 500
  zeros.
- **H3 (never-measured overtones, out of sample): PASS — the theory's
  sharpest prediction.** m = 25 and m = 27, measured for the first time
  anywhere, are suppressed below the DW law: pooled deviations −0.339 and
  −0.176 against a committed threshold of −0.10.
- **H4 (genuine-prime controls): PASS** — pooled deviations +0.035 (m = 11)
  and −0.010 (m = 13): the suppression targets prime powers and spares
  primes.
- **H2 (persistence band): REFUTED.** Window-4 m = 9 measured 0.647, outside
  the committed band [0.22, 0.55]. Across the four windows m = 9 reads
  0.37 / 0.39 / 0.46 / 0.65 — **the anomaly decays toward the law with
  height**, the natural scaling of a second-order mixing term (ω·δ shrinks as
  the zeros densify), and exactly what the committed constant-band model
  ignored.
- **P1 CONFIRMED** (window-4 gated set obeys the DW law at mean |dev| 0.024 —
  the law's fourth out-of-sample window). **P2, P3 CONFIRMED** (pooled
  deviations at 8 and 4 negative: −0.036, −0.051).

## Verdict, per the prereg's own commitment

The drafted overtone clause required H2–H4; H2 failed, so the clause as
drafted is **withheld**. What stands, earned out of sample:

1. **Existence** (MACHINE): prime-power frequencies are suppressed below the
   transfer law — including at frequencies never previously measured — while
   genuine primes of comparable τ conform. Four windows, plus the beta-family
   m = 9 reading, concur.
2. **The phase-locking input** (MACHINE): Landau's bias at the percent level.
3. **Height decay** (recorded, unclaimed): the suppression weakens as the
   zeros densify — the quantitatively natural signature of second-order
   self-mixing, and the follow-up prereg's committed target: an overtone
   model with explicit height scaling (candidate form: deviation at
   ln p^k ∝ (line amplitude)²·ω/ρ̄, phase-locked by the Landau bias),
   promoted only if it predicts a fifth window and the beta family jointly.

## Incidental confirmation

P1 extends the transfer law's ledger: window 4 is its fourth consecutive
out-of-sample confirmation on the gated set (mean |dev| 0.024).

## Lane derivation queue after RH7

(i) the jump-point sampling weight (RH6 target — the DW law itself);
(ii) the height-scaled overtone coefficient (this WP's target);
both pair-correlation objects, both with four-window measured tables waiting,
both natural WP7-lane formal candidates.
