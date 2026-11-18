# Fintech routing — v1.40.0 sampled rerun (I22 adversarial authorization gate)

Date: 2026-11-19 · Release: v1.40.0 · Suite: [fintech-routing](../fixtures/fintech-routing.md)

## Why sampled, not full

v1.40.0 adds **I22** (adversarial spend is authorization-gated; the ask rides the entry stop of an already-computed route) — it does **not move any tier boundary or routing predicate**: every fixture's expected tier is unchanged by construction. Per the v1.38.x read-check precedent (no predicate moved → suite not rerun), a full 13-arm rerun would re-probe unchanged predicates. The one genuinely new mechanism on escalate's path — the reworded **Authorize/Decline ask with the adversarial-debt decline branch** — is what the sample verifies, in both firing directions.

Method: identical to the v1.12.1 run — each fixture routed by a fresh blind subagent playing `spec-tdd-escalate` (reads the working-tree skill text only; no answer key). Each arm additionally asked to enumerate every stop it would make, so the ask machinery is observable, not just the tier.

## Arms

| # | Fixture | Expected | Routed | Ask machinery | Verdict |
|---|---|---|---|---|---|
| 4 | Retention purge (7y completed transactions) | **adversarial** | adversarial | I22 ask FORMED correctly: one-line stakes basis; carve-out verdict stated (does NOT apply — deletion is data-loss logic); Authorize → invoke; Decline → coverage + the adversarial-debt record persisted and surfaced in residuals; dispatched-context rule self-applied (report IS the ask) | ✅ |
| 7 | Cash-position snapshot endpoint (read-only) | **coverage** | coverage | I22 ask NEVER FORMS — the carve-out kills the adversarial computation at routing, before any ask exists; counterfactual branch correctly described | ✅ |
| 11 | Cut-off-times back-office CRUD | **base/coverage, NOT adversarial** | coverage (in range) | I22 never forms (money-adjacent, not movement) | ✅ |

**3/3.** The true-critical arm forms the ask with the exact v1.40.0 shape; the money-adjacent and boundary arms never form it. No false-adversarial, no over-asking.

## Disclosure

- `spec-tdd-manager`'s frontmatter description changed one clause this release (auto-escalates → escalates on the recorded I22 authorization). The routing arms read escalate's text only, so this sample is unaffected; the change is truth-telling about behavior, not a trigger/predicate move.
- Green-lie suite not rerun: no tier's verification machinery changed.
