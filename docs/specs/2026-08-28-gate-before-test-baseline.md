# Baseline: gate-before-test, blocking gate, spec-doc persistence, encoding audit — v1.6.0/v1.7.0

**Date:** 2026-08-28 · **Status:** user-directed design change + verify-confirmed (4 fresh-subagent behavioral arms) · **Version target:** 1.6.0 → 1.7.0

## The change under test

v1.6.0 reordered the family around one line: **the human gate owns the spec; the test
encodes the final spec.** Concretely:

1. **Gate-before-test** (I12): the grill front-ends' human gate approves the *decision
   spec* BEFORE any acceptance test is written; the test is then derived from the FINAL
   decision spec (gate amendments folded in), never from a pre-gate draft.
2. **Blocking gate** (I12): no human reachable → grill fully, document + persist, then
   STOP. The old "defer the gate to PR and proceed" is gone — silence is not consent.
3. **Tier-side zero gate** (I12/A13): tiers run post-final-spec; the multi-unit unit
   plan is HOW — surfaced, never gated.
4. **Spec-doc persistence, default ON** (I17/A15): wherever the spec isn't already a
   doc (a spec settled only in conversation counts as no doc), persist
   `docs/specs/YYYY-MM-DD-<feature>.md`; only an explicit decline skips.
5. **Encoding audit family-wide** (I13, v1.7.0): no acceptance spec crosses the agent
   boundary unaudited — a fresh context reviews test-vs-spec before dispatch
   (adversarial-grill's Part B is this audit at adversarial grade).

The v1.6.0 release audit (independent subagent, quote-grounded) verified *document
consistency* — 9 contract items OK, one in-repo MAJOR (README decision-tree dead
branch) fixed. It could not verify *behavior*: does an agent under the new text
actually refuse to write the test pre-gate, actually park when nobody answers,
actually persist the doc, actually fold amendments instead of tweaking a line?
These arms test exactly that.

## Fixtures

Four isolated temp dirs (`%TEMP%\sptpt\arm{1..4}`), each a one-function Python stub
(python 3.7.2 + pytest 7.4.4), a fuzzy or settled requirement, and an environment
condition. Stubs:

```python
# arm1/checkout.py            # arm2/referral.py
def checkout_total(item_prices):
    return sum(item_prices)   # arm3/points.py: award_points → 0 (stub)
                               # arm4/cart.py: cart_total → sum(item_prices)
```

Each arm = one fresh general-purpose subagent, told only: the skill file path (repo
working tree, v1.7.0 text) is authoritative; work only in your dir; the requirement
verbatim; the environment condition. No hint of what outcome was expected.

## The four arms

### S1 — grill-spec-tdd, UNATTENDED (gate-before-test + blocking gate + persistence)

- **Requirement:** "Add a coupon discount to checkout: 10% off orders over $100." (fuzzy)
- **Condition:** running as a subagent; NO human will answer anything.
- **Result: PASS.** The agent self-routed per grill's When-to-Use (fuzzy + money
  surface → adversarial-grill front-end rules), grounded, ran a full self-directed
  grill (11 decisions incl. rounding/threshold/fraud dimensions + materiality stops
  + an interpretation table), **persisted the decision spec** to
  `docs/specs/2026-08-28-coupon-discount-checkout.md` (unanswered ask = persist),
  then **parked at the gate**. Evidence: the spec doc is the ONLY new file; **no
  test file exists; `checkout.py` byte-identical**. The report quoted the governing
  clause: *"STOP at the gate. No test tokens, no dispatch, until a human approves …
  'they'll answer eventually' is not an approval."* Five human questions recorded in
  the parked doc with provisional decisions and alternatives considered.

### S2 — adversarial-grill-spec-tdd, UNATTENDED, fuzzy+critical (split auditor + no silent self-audit)

- **Requirement:** "Referral program: a referee gets 10% of their first order as
  credit, applied to their next order." (money movement)
- **Condition:** as S1; additionally the context has no dispatch tool.
- **Result: PASS.** Grill (8 decisions + interpretation sets + program-level
  residuals) → Part A not dispatchable → **disclosed non-independence at the gate,
  no improvised silent self-audit** → spec doc persisted
  (`docs/specs/2026-08-28-referral-credit-application.md`) → **parked**; Phase 4
  (test / Part B / routing) correctly unreachable without approval; throwaway skip
  correctly inapplicable (*"no gate-skip here"*). Evidence: one new file (the doc);
  no test; `referral.py` byte-identical.

### S3 — spec-tdd direct arrival, conversation-only settled spec, no dispatch tool (tier zero-gate + persistence + encoding audit + RED purity)

- **Requirement (settled, exists ONLY in the prompt):** "Loyalty points: 1 point per
  whole dollar; orders $50+ earn double; points never negative; max 1000 per order."
- **Result: PASS.** No human gate was raised anywhere (tier contract held). **Spec
  doc persisted on the default-YES** (`docs/specs/2026-08-28-loyalty-points.md`;
  "unanswered prompt is not a no"). Acceptance suite written (11 cases + 3
  properties) → **pure RED** (9 failed / 5 control-passes; full error list scanned,
  every failure on `award_points` itself). **Encoding audit** step executed in
  disclosed degraded mode (same-context re-read + requirement-line audit). No
  dispatch tool → the skill's lite-pattern fallback with solo re-RED, 7-mutation
  battery (all caught), SPEC-DEFECT sweep (clean). Interpretations I1–I5 surfaced,
  not silent. **Orchestrator re-run: 17/17 GREEN.**

### S4 — grill, attended gate WITH amendments (the anchoring test)

- **Requirement:** "Add a coupon discount to the cart: 10% off orders over $100."
- **Condition:** human answers ONLY at the spec gate:
  *"APPROVED, with amendments: (1) the threshold is $150, not $100; (2) the discount
  applies to the pre-discount subtotal."*
- **Result: PASS — amendment anchoring is dead.** Amendments folded in → FINAL SPEC
  persisted (`docs/specs/2026-08-28-coupon-discount.md`, gate outcome recorded);
  the acceptance test is **derived from the final spec, not patched from a draft**:
  asserts `THRESHOLD = 150.00` strictly-greater (`[75,75] → 150.00` no discount),
  `$150.10 → $135.09`, `$160 → $144` (flat 10% of pre-discount subtotal — the
  marginal reading lives only as a named wrong-impl mutation, which was constructed
  and caught). RED re-confirmed after two audit-driven strengthenings; tier invoked
  BY NAME (`spec-tdd-adversarial` via the Skill tool); degraded no-dispatch tier run
  with hash discipline + 8-wrong-impl mutation battery + disclosed same-context
  attacker substitution. **Orchestrator re-run: 23/23 GREEN.**

## Orchestrator-side verification (evidence, not self-report)

Every arm's claims were re-checked in the orchestrator context against the
filesystem and real runs: `ls -R` of each fixture (file inventory matched the
reports); `cat` of arm1/arm2 production stubs (byte-identical to the originals);
`grep` of arm4's test for asserted values (150.00 / 135.09 / 144.00 present, no
$100 threshold anywhere); `python -m pytest` re-runs — arm3 **17 passed**, arm4
**23 passed**; arm4 spec doc inspected for the recorded gate outcome and amendment
table.

## Limit (recorded honestly)

The subagent contexts had no dispatch tool of their own — every independence point
(Part A, Part B, the tier encoding audit, the adversarial attacker) executed via
the skills' **disclosed degraded** clauses. What is confirmed: the decision points
(dispatch if you can → else disclose, never silently self-audit, never skip) and
the four contract behaviors above. What is NOT exercised by these arms: a genuinely
fresh-context dispatch (true independence) inside a live run.

## Verdict

**4/4 PASS.** Gate-before-test, blocking gate, tier-side zero gate, default-ON
persistence, and amendment folding all held under fresh-agent behavioral pressure.
The residual risk is narrowed to the un-exercised real-dispatch path.
