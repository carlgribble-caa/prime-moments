# Preregistration: ML detector (WP9c)

Committed before first run. Instrument: `code/ml_detector.py`. Population: the primes
in [10^5, 10^6] with the scanner-v2 feature battery; chronological split — first half
train, second half holdout.

## Tasks (binary, on the *next* prime)

- T1: chi4(p_next) = +1 vs −1.
- T2: large gap — (p_next − p)/log p above the train-half median.

## Feature sets

- BASELINE (skeleton only): chi4(p), chi3(p), one-hot coprime class of p mod 60
  (16), size band (scaled log p). 19 columns.
- CHALLENGER: baseline + crystal-native features Om(p−1), Om(p+1), slope P(p−1),
  Pratt h, om(p−1), sf((p−1)/2), bits(p). 26 columns.

## Models (hyperparameters fixed here)

- Logistic regression, IRLS 20 iterations, ridge 1e−3.
- Gradient-boosted stumps, logistic loss, T = 120 rounds, learning rate 0.1,
  8 quantile thresholds per feature per round.

## Metric and threshold

Holdout mean log-loss (nats). Improvement = baseline − challenger on the same model
class and task. Preregistered detection threshold: eps = 0.002 nats.

## Committed predictions

Q1. On both tasks and both model classes, challenger improvement < eps: the
    crystal-native features add nothing beyond the skeleton (two-skeleton
    conjecture, detector form).
Q2. On T1 the BASELINE beats the coin (log-loss < ln 2 − 1e−4 on holdout): the
    Lemke Oliver–Soundararajan signal lives in the skeleton features and the
    detector must see it there (positive control).
Q3. Any improvement ≥ eps goes up the audit ladder (leakage, entanglement,
    skeleton-derivable, known theorem) before the word "candidate".

## Power note (honest)

The scanner's three in-audit gap×smoothness readings have |z| ≈ 5 at n = 68,906,
i.e. correlation r ≈ 0.02 and an available log-loss improvement of order r²/2 ≈
2×10⁻⁴ — an order below eps. This detector at this scale cannot see them; Q1 is a
claim about structure of practical size, not about those readings.
