---
name: grill-spec
description: Use when the user says "grill-spec", or wants to interrogate/grill requirements before a test-first delegated implementation — especially for fuzzy or high-stakes (money/auth/data) features. Triggers on requirement grilling before coding, spec-as-test, test-first-by-orchestrator, and avoiding wasted subagent runs on wrong-direction specs.
---

# grill-spec

## Overview
**The requirement-grilling front-end for the `spec-tdd` family.** Interrogate the requirement until it's unambiguous ("grill"), write the acceptance test — the spec — before any implementation exists, gate it, THEN route to the verification tier that fits the stakes: `spec-tdd` (default), `spec-tdd-coverage`, or `spec-tdd-adversarial`. That tier carries the delegation handoff, circuit breaker, and failure routing.

**Why a separate front-end:** under pressure, agents skip grilling and hand a subagent a fuzzy spec, or collapse it to "sensible defaults." Grilling first forces every dimension (incl. NFR + security) explicit and gets a human OK on direction before a subagent burns tokens on the wrong thing.

**Core principle (inherited from `spec-tdd`):** the acceptance test is authored before any impl, in a different context than the implementer — so it cannot mirror an implementation. **"Must be RED first"** is the green-lie detector.

## When to Use
- User says `grill-spec <feature>`.
- Requirement is fuzzy, high-stakes (money / auth / data-loss), or a wrong-direction subagent run would be expensive.
- For crisp, already-specified, low-stakes features, skip this and use `spec-tdd` directly.

## Phase 1 — Grill, write the acceptance test, gate
1. **Grill in batches** — interrogate EVERY dimension, not just the obvious ones: business logic, boundary/edge cases, state transitions, **NFRs (perf / scale / cost)**, and **security / fraud / abuse**. Force an explicit decision on each. *If you can't state a decision for a dimension, you haven't grilled it.*
   - **Grilling ≠ silent defaults.** Deciding deliberately after interrogating every dimension is the grill; collapsing to "sensible defaults" without hitting NFR/security is the failure mode. A missed dimension isn't a design decision — it's an absent one (e.g. coupon fraud, lockout-DoS).
   - **The grill is self-directed.** Stakeholders unreachable tonight? You still grill — you interrogate and decide. Their reachability affects the *gate* (step 6), not the grill.
2. **Ground it**: read the relevant entities/services/repos/patterns first; the test must fit the real architecture.
3. **Write BEHAVIORAL acceptance tests** — black-box, input→output/state. Test WHAT, not HOW; don't couple to internal method shapes.
4. (Domain logic only) add 1–3 **property/invariant tests** (e.g. money conservation). Properties can't become green lies.
5. **Run it — MUST be RED.** Green with no impl = fake test (vacuous / over-mocked); rewrite it.
6. **Approval gate** (critical/general tiers): surface the test + grilled decisions for a quick human OK *before* delegating. The gate checks **direction** (is this the right spec?) so you don't burn a subagent run on the wrong thing. Executable tests catch *logic* bugs, not wrong-direction work — so "my tests encode my assumptions" is **not** a substitute for the gate. No human reachable on a critical path? Grill fully, document every decision, defer the gate to PR — but never use "no one's reachable" to skip the grill. Throwaway tier may skip the gate.

## Phase 2 — Route to the verification tier
Pick by stakes, then follow that skill's Phase 2–3 (it carries the delegation handoff, circuit breaker, and failure routing):
- **Correctness-CRITICAL** (money movement / auth-permissions / data-loss) → `spec-tdd-adversarial` (independent attacker + mandatory property/differential tests).
- **Need branch-coverage EVIDENCE** (large/subtle branch surface: concurrency/parsing/state machines; weak unit tests; compliance proof) → `spec-tdd-coverage` (case-list + per-class branch % + gap-check).
- **Otherwise** → `spec-tdd` (the default).

Hand off the grilled acceptance test as the contract; the tier implements, it does not re-litigate decisions the grill already locked.

## Red Flags — STOP
- "The failure mode isn't a wrong design decision, so I'll skip grilling."
- "I'll just pick sensible defaults and note them." (did you hit NFR + security?)
- "No one's reachable tonight, so I'll skip the grill/gate." (grill is self-directed)
- "My tests encode my assumptions, so I don't need a human OK before delegating." (tests catch logic, not direction)

## Common Mistakes
| Mistake | Fix |
|---|---|
| Skip the grill, hand a subagent a fuzzy spec | Grill every dimension (incl. NFR + security) first; a fuzzy spec wastes the whole subagent run. |
| Collapse the grill to "sensible defaults" | Deciding deliberately after interrogating ≠ assuming silently. |
| Skip the approval gate because "tests encode my assumptions" | The gate checks direction; tests catch logic. No human? Defer the gate to PR, don't skip the grill. |
| Route everything to base `spec-tdd` | A fuzzy+critical feature goes to `spec-tdd-adversarial`; fuzzy+coverage-needed to `spec-tdd-coverage`. Pick the tier by stakes. |
| Re-litigate grill decisions inside the tier | The acceptance test + grilled decisions are the contract; the tier implements, not re-decides. |
