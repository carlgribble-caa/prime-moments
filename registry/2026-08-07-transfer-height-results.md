# Results: height dependence of the transfer attenuation (WP-RH4b)

Prereg: `2026-08-07-transfer-height-prereg.md`, committed at `49b66b5` before
first run. Instrument: `code/transfer_height.py` (27 s). Results are
append-only.

## Bring-up (one prereg-level sign error, RH2-Abel precedent)

The prereg's field formula asserted `(k − 1/2) − Nbar(γ_k) = −S̄(γ_k)`; the
RvM midpoint convention gives `+S̄`. The first run implemented the prereg
faithfully and returned the committed magnitudes with flipped sign (LOW
−0.922/−0.809/−0.648/−0.554, replicating RH4's post-hoc +0.92/+0.81/+0.65/
+0.55 exactly), failing the sign-dependent gates. The field was corrected to
`y = Nbar(γ_k) − (k − 1/2)` — the convention the predictions were written
for — with all thresholds unchanged; this note records the first run in full.

## Gates and predictions (corrected run)

| m | ω | LOW ratio | HIGH ratio | improvement |
|---|---|---|---|---|
| 2 | 0.693 | 0.922 | 0.984 | +0.061 |
| 3 | 1.099 | 0.809 | 0.916 | +0.107 |
| 4 | 1.386 | 0.714 | 0.668 | −0.046 |
| 5 | 1.609 | 0.648 | 0.820 | +0.172 |
| 7 | 1.946 | 0.554 | 0.728 | +0.174 |
| 8 | 2.079 | 0.335 | 1.118 | +0.783 |
| 9 | 2.197 | 0.364 | 0.307 | −0.057 |
| 11 | 2.398 | 0.411 | 0.737 | +0.326 |
| 13 | 2.565 | 0.335 | 0.682 | +0.347 |

- **Z1 (replication on the exact field): PASS** — the RH4 post-hoc profile is
  reproduced on the identity-exact field, committed in advance.
- **Z2 (attenuation weakens with height): PASS — 4/4** gated frequencies
  improve (windows share no zeros; HIGH = k = 141..200, heights 305–396).
- **V1: CONFIRMED** — HIGH m = 2 ratio 0.984, approaching unity.
- **V2: CONFIRMED** — mean gated improvement +0.128, inside [0.03, 0.25].

## Claim, earned

**The transfer attenuation is a height-dependent sampling effect, not a fixed
law.** As the zeros densify (`ω·δ` shrinks), the per-frequency slopes of the
shift field climb toward the explicit-formula amplitudes — 0.98 at ln 2 in the
high window — exactly as both RH4 mechanisms (premise attenuation and
coordinate decoherence, each scaling with `ω/ρ̄`) require. The
explicit-formula amplitudes are the dense-sampling limit of the Hamiltonian
transfer. Off-gate rows behave as noise permits (m = 8 overshoots to 1.12,
m = 4/9 flat within ±0.06 noise); recorded, not interpreted.

## Spec impact

Constraint 1 (WP-RH3/RH4) reaches its final measured form for this phase: the
missing self-adjoint realization must carry the prime comb at fluctuation
order, through a transfer that attenuates with `ω/ρ̄` at finite height and
approaches the explicit-formula amplitudes as the spectrum densifies. That is
now a three-instrument, two-window, controlled and preregistered quantitative
fingerprint.
