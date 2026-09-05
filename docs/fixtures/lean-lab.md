# Lean-lab fixtures — v1.16.0 validation (LL-01..LL-06)

Validates the four v1.16.0 changes before they ship (the standing regression rule gates tier-behavior changes). Design + pre-registered predictions + budget: [`docs/specs/2026-09-05-v116-lean-lab.md`](../specs/2026-09-05-v116-lean-lab.md). This file is the fixture/key record, written **before any arm dispatch**. Instruments mirror the green-lie suite ([`green-lie.md`](green-lie.md)): blind staged dispatches, hidden committed oracles, mechanical scoring, a trap battery with a selftest validity gate — adapted per arm below.

**Run tree:** `docs/fixtures/lean-lab-runs/` → `reqs/LL-XX.md` (verbatim public requirements), `seed/LL-03|04/` (pre-seeded old files the harness copies into T1 arm dirs), `L1/LL-0X`, `L2-V1/LL-0X`, `L2-V2/LL-0X`, `T1/LL-0X` (arm dirs). **Oracles, traps, references, and the planted/real INTENT files are committed and hidden from arms**: [`docs/fixtures/oracle/lean-lab/`](oracle/lean-lab/) — `python <oracle> <dir>`; battery `python trap_battery_ll.py selftest|oracle <arm>|run <arm> [LL-XX]`.

**Validity gates (run before any dispatch, both green):** battery selftest **20/20** traps oracle-fail (3 per fixture + an X1 cross-cutting trap each for LL-03/LL-04); all 6 reference impls **PASS** their oracles.

## Fixtures and keys

### LL-01 payout action · L1 — module `payouts.py`
Spec: 1-page payout disposition (`RELEASE/DEFER/HOLD/ESCALATE`), weekday codes, KYC states, 100000-cent escalation threshold.
**Key.** KYC gate FIRST: weekend+UNVERIFIED → `HOLD`, large+UNVERIFIED → `HOLD` (the spec states each rule but never their relative precedence — genuinely open; the key settles it as gate-first). Escalation is strictly OVER 100000 ("exceeds"/"above") and precedes scheduling.
**Planted INTENT (2):** ① open-point silent resolution — "weekend defers before any other consideration; KYC re-checked on execution day" (→ key-wrong `DEFER`); ② contradiction — "large means at or above the threshold" (key-wrong at 100000 exactly).

### LL-02 tiered fee · L1 — module `tierfee.py`
Spec: band-table fee lookup with **recorded decisions** D1 (inclusive lower bound) and D2 (flat fees).
**Key.** Below-first-band (incl. 0) → fee 0 (spec: "no band applying, no fee"); empty table → fee 0 (spec silent — genuinely open); duplicate lower bounds → `ValueError` (decided).
**Planted INTENT (2):** ① open-point silent resolution — "empty tier table is a configuration error → ValueError" (key-wrong); ② contradiction of D1 — "notional must exceed the band edge" (exclusive lower; key-wrong at edges).

### LL-03 fee rounding extraction · T1 — module `fees.py` (+ seeded `ledger.py`, `test_ledger.py`)
Spec: `round_fee` (nearest 10, halfway up), `settle_total` (per-item round then sum); integration notes mention reversals and point at the caller file without stating sign semantics.
**Key.** Negative fees mirror about zero (halfway AWAY from zero: -145 → -150) — knowable from the seeded caller's shapes, not from the delta section. `settle_total` never mutates its argument.
**Traps:** T1 halfway-down · T2 nearest-5 · T3 sum-then-round · **X1 negatives-toward-zero** (functionally correct on all positives; invisible to delta-only tests; fails the oracle's mirror cases) — P2's out-of-delta instrument.

### LL-04 currency conversion · T1 — module `fx.py` (+ seeded `positions.py`, `test_positions.py`)
Spec: `convert` direct/inverse (half-up at whole cent), unknown pair → `ValueError`; integration notes mention the shared batch rate table and shorts.
**Key.** Sign flows through both paths (half away from zero: -103·0.5 → -52, -100/8 → -13); the rates mapping is **never mutated** (the seeded caller reuses one table per book — the batch-reuse hazard the spec never pins as a contract).
**Traps:** T1 inversion-forgotten · T2 half-down · T3 unknown-pair-passthrough · **X1 memoizes the inverse back into the caller's dict** (every value correct; fails the oracle's purity checks).

### LL-05 code normalization · L2 — module `codes.py`
Decided contract: trim; MIXED separator runs → one hyphen; uppercase fold; strict alphabet; empty/separator-only → `ValueError`; idempotent.
**Traps:** T1 same-char-runs-only (mixed run survives as 2 hyphens) · T2 no-trim · T3 case-fold dropped.

### LL-06 amount parsing · L2 — module `amounts.py`
Decided contract: parens/minus = negative (never both); strict 3-digit comma groups (when commas present); ≤2 fraction digits (else raise, no rounding); no digits → raise.
**Traps:** T1 parens-sign-lost · T2 extra-decimals-rounded · T3 group-validation skipped.

## Arms (blind; role instructions embedded — see Deviations)

- **L1 (INTENT check):** per fixture — one test-author dispatch (acceptance test + `NotImplementedError` stub, RED + RED-purity), then TWO independent audit dispatches over the SAME (req, test, planted INTENT), differing ONLY in the embedded checklist: Variant carrying the v1.15.2 audit instructions (checks 1–2) vs Variant carrying v1.16.0's (checks 1–3, the INTENT fidelity check). Audits are read-only; variant order alternates by fixture (LL-01: new-variant dispatched first; LL-02: control first) to avoid order effects. Audits never see each other or the key.
- **T1 (attacker scope):** per fixture — test-author (adversarial grade: property tests mandatory, 7-hole-class self-check, seeds) → implementer (case-list first; BOTH the delta test file and the pre-seeded old test file must pass; ERR-not-edit) → then TWO Part-A attacker dispatches on the same landed state, each in its OWN scratch copy: **full-surface** (whole suite incl. seeded old files + intent) vs **delta-scoped** (delta entry points + covering test file NAMES + intent; old files NOT readable). Run economy + hygiene embedded; hole reports to `<armdir>/attack/full-holes.md` / `scoped-holes.md`. Harness-side checks: survivors confirmed on the real dir; the X1 trap swapped into the landed suite (KILLED/SURVIVED = P2's priced miss). No strengthening dispatch (the strengthen path is not the variable under test — deviation, disclosed).
- **L2 (property sweep):** per fixture × two blind variants (V1/V2) — test-author (acceptance test + stub, RED) with the ONLY difference being the embedded Phase-1 property-test sentence: V1 carries v1.15.2's "(domain logic only) add 1–3 property/invariant tests", V2 carries v1.16.0's "property tests are part of the acceptance spec for transform logic — not optional: name the invariant and a generator whose alphabet includes real production shapes" → implementer (case-list first, ERR-not-edit). Coverage-tool re-run skipped (deviation, disclosed — the question is property presence, not branch %).

## Scoring (mechanical, harness-side)

1. Every arm's own suite re-run by the harness → GREEN? 2. Hidden oracle → PASS? 3. Battery swap-in per arm dir → trap-kill. 4. **L1:** each audit's RETURN is scored per planting: a finding is credited only if it explicitly ties the INTENT statement to the spec gap or the recorded decision (quotes required) — a generic restatement of the INTENT is not a finding. 5. **T1:** hole counts per variant by severity (in-delta yield parity) + X1 KILLED/SURVIVED per fixture + attacker token/wall-clock costs. 6. **L2:** property-test presence + non-tautology rubric (generated inputs or a differential oracle — two fixed cases don't count) + oracle + trap-kill.

Pre-registered predictions P1–P5 and GO/NO-GO: see the design doc. Results append to the design doc after scoring.

## Disclosed deviations from the design doc / live skill

- Role instructions are **embedded in dispatch prompts**; no arm reads `skills/` (the working tree carries the unshipped v1.16.0 text — embedding keeps both text variants symmetric and arms blind).
- LL-01 carries **1 open-point planting + 1 contradiction** (design doc said "2 open points"); with LL-02 that totals P1's 4 plantings (2 open + 2 contradictions) — scoring follows P1's structure.
- Battery is 20 LL traps (design doc's "54" counted the GL suite's 36 + 3×6; the two X1 cross-cutting traps are added for P2's instrument → LL total 20, program total 56).
- No strengthen dispatch in T1; coverage-tool re-run skipped in L2 (neither is the variable under test; both disclosed).
- Single maintainer-author of fixtures and keys (same authorship-bias direction as the GL suite); single session model across all arms; N=2 per arm — direction, not magnitude.
