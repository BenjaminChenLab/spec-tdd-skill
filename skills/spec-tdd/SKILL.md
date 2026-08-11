---
name: spec-tdd
description: Use when the user says "spec-tdd" or wants acceptance-test-first development delegated to a subagent. Triggers on spec-as-test, test-first-by-orchestrator, preventing weak/green-lie AI tests, circular test+implementation reasoning.
---

# spec-tdd

## Overview
Two-tier TDD split across the agent boundary: **the orchestrator writes the acceptance test (the spec) before any implementation exists; a subagent then implements to pass it and adds its own unit tests.** This breaks the circular reasoning that makes same-agent test+impl produce *green lies* — tests that merely mirror the implementation. Near-zero human cost because the orchestrator is AI.

**Core principle:** the acceptance test is authored before any impl exists, in a different context than the implementer — so it cannot mirror an implementation. **"Must be RED first"** is the built-in green-lie detector.

## When to Use
- User says `spec-tdd <feature>` (the agreed trigger).
- Implementing a feature where weak/vacuous AI-generated tests are a risk.
- Any stack. Risk-tier how much verification you run (see below).

## The 3 Phases

### Phase 1 — Orchestrator writes the acceptance test
> **Arrived from `grill-spec-tdd`?** The acceptance test is already written and RED — skip this phase, go straight to Phase 2.

1. Requirement unclear? **Ask, don't guess.** (Can't write the test = the spec is unclear — that's the signal, surfaced before coding.)
2. **Ground it**: read relevant entities/services/repos/existing patterns first; the test must fit the real architecture.
3. **Write BEHAVIORAL acceptance tests** — black-box, input→output/state. Test WHAT, not HOW. Don't couple to internal method shapes.
4. (Domain logic only) add 1–3 **property/invariant tests** (e.g. money conservation, net-zero offset). Properties can't become green lies and don't over-constrain design.
5. **Run it — MUST be RED.** Green with no impl = fake test (vacuous / over-mocked); rewrite it.

### Phase 2 — Delegate to subagent (Agent tool)
Handoff prompt:
```
TASK: Implement {feature} so the acceptance test below passes.
Do NOT modify the acceptance test. If it looks wrong, STOP and report back — never silently weaken it.

ACCEPTANCE TEST (written, currently RED):
{file:line or paste}

INTENT (plain language): {1–3 sentences}

READ FIRST: Entity {path}, Service {path}, Repository {path}, Pattern-to-follow {path}

DO: 1) make acceptance test GREEN  2) add your own unit tests (red→green each)  3) follow existing conventions.
CIRCUIT BREAKER: if the test still fails after 3 repair attempts, STOP. Report a short structured diagnosis — tag it env/dependency (ERR-01), logic violation (ERR-02), or syntax/compile (ERR-03) — with a TRUNCATED trace and expected-vs-actual. Don't keep retrying.

RETURN: implementation + unit tests + ACTUAL test command output proving green (not a claim).
```

### Phase 3 — Orchestrator verifies
1. **Run the acceptance test yourself** (don't trust the subagent's self-report) → must be GREEN.
2. **Adversarially read the test**: "could this pass even if the impl were subtly wrong?" If yes, strengthen. Also check it fits existing architecture/conventions and any security/resilience edge cases.
3. **Surface the TEST (the spec) to the user for review — not the impl.** Reviewing the test is the cheap, high-signal human checkpoint.
4. Compile + relevant suite.
5. **On failure, route by root cause** — don't flail: **spec-flawed** (test/spec wrong or incomplete) → back to Phase 1, fix the test, re-confirm RED, re-delegate; **impl-flawed** (test right, code wrong) → re-delegate with the failing case + the subagent's ERR tag.

## Risk-tier (scale verification to stakes)
- **Critical path** (money / auth / data-loss surface): full phases + property tests + adversarial impl review.
- **General feature**: phases 1–2 + run acceptance + compile.
- **Throwaway / demo**: minimal — acceptance test + compile.

## Common Mistakes
| Mistake | Fix |
|---|---|
| Orchestrator writes unit tests, not acceptance | Keep the spec/impl boundary = agent boundary. Unit tests belong to the subagent. |
| Skip "must be RED first" | Non-negotiable. Green-before-impl = the test is meaningless. |
| Subagent silently edits the acceptance test to pass | Forbid in handoff; require report-back. Re-run to confirm the test is unchanged. |
| Trust self-report that "tests pass" | Always run them yourself in Phase 3. |
| Over-constrain: test couples to impl shape | Test behavior (input→output), not internals. |
| Let a failing subagent loop forever | The 3-strike circuit breaker stops this — honor it. |
