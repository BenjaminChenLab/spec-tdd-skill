---
name: spec-tdd
description: Use when the user says "spec-tdd" or wants acceptance-test-first development delegated to a subagent. Triggers on spec-as-test, test-first-by-orchestrator, preventing weak/green-lie AI tests, circular test+implementation reasoning.
---

# spec-tdd

## Overview
Two-tier TDD split across the agent boundary: **the orchestrator writes the acceptance test (the spec) before any implementation exists; a subagent then implements to pass it and adds its own unit tests.** This breaks the circular reasoning that makes same-agent test+impl produce *green lies* — tests that merely mirror the implementation. Near-zero human cost because the orchestrator is AI.

**Core principle:** the acceptance test is authored before any impl exists, in a different context than the implementer — so it cannot have been reverse-engineered to mirror an implementation (the structural anti-green-lie guarantee). It can still be *wrong or shallow* — a misread or under-interrogated requirement produces a bad test — but that is a different failure mode, handled by RED-first, the Phase-3 adversarial read, the grill, and the attacker. **"Must be RED first"** is the built-in green-lie detector.

**Protocol:** this skill operationally enforces the spec-TDD protocol — see [PROTOCOL.md](../../PROTOCOL.md) for the canonical artifacts (A1–A11) and invariants (I1–I12).

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
**SPEC-INTEGRITY snapshot (before dispatch):** hash the acceptance test — `sha256sum <file>` (Unix) / `certutil -hashfile <file> SHA256` (Windows) / `git hash-object <file>` — and record it. This is the immutability baseline you verify in Phase 3.

Handoff prompt:
```
TASK: Implement {feature} so the acceptance test below passes.
Do NOT modify the acceptance test — it is hashed and verified byte-for-byte on return. If it looks wrong, STOP and report back — never silently weaken it.

ACCEPTANCE TEST (written, currently RED):
{file:line or paste}

INTENT (plain language): {1–3 sentences}

READ FIRST: Entity {path}, Service {path}, Repository {path}, Pattern-to-follow {path}

DO: 1) make acceptance test GREEN  2) add your own unit tests (red→green each)  3) follow existing conventions.
CIRCUIT BREAKER: STOP if either fires — (a) the test still fails after 3 repair attempts, OR (b) **the same root cause appears on ANY two attempts** — same failing file:line AND same failing assertion (not necessarily consecutive; not a rephrased free-text trace). Don't burn a third attempt re-trying one identical misdiagnosis — each attempt must rest on a DIFFERENT root cause. Report a short structured diagnosis — tag it env/dependency (ERR-01), logic violation (ERR-02), or syntax/compile (ERR-03) — with a TRUNCATED trace and expected-vs-actual. Don't keep retrying.

RETURN: implementation + unit tests + ACTUAL test command output proving green (not a claim).
```

### Phase 3 — Orchestrator verifies
1. **SPEC-INTEGRITY check:** re-hash the acceptance test and compare to the Phase-2 snapshot. Any change → the implementer edited the spec → **FAIL**, even if a re-run is GREEN (a weakened-but-green test is the green lie) → route to **TEST** (step 6); never accept a changed test. *(This binds the implementer; your own step-3 strengthening is a separate, explicitly re-RED'd step.)*
2. **Run the acceptance test yourself** (don't trust the subagent's self-report) → must be GREEN.
3. **Adversarially read the test**: "could this pass even if the impl were subtly wrong?" If yes, strengthen — and if you change the test, re-confirm it goes RED against the current impl, then re-delegate to restore GREEN. Never declare done on a test you just edited without re-running it. Also check it fits existing architecture/conventions and any security/resilience edge cases.
4. **Surface the TEST (the spec) to the user for review — not the impl.** Reviewing the test is the cheap, high-signal human checkpoint: the human validates WHAT, the agent validates HOW.
5. Compile + relevant suite.
6. **On failure — or a hole found in a GREEN test — route by root cause, three buckets only:**
   - **SPEC** — you misread or under-interrogated the requirement; the test encodes the wrong behavior → re-open the requirement (ask the human / re-grill), rewrite the test, re-confirm RED, re-delegate.
   - **TEST** — the requirement is right but the executable spec is weak/incomplete (a missing case), or the implementer edited it → strengthen/revert the test, re-confirm RED, re-delegate. Do NOT re-open the requirement.
   - **IMPL** — the spec is right, the code is wrong → re-delegate with the failing case + the subagent's ERR tag.
   Key: SPEC re-opens the *requirement*; TEST touches only the *test*; IMPL touches only the *code*. Mis-routing (e.g. TEST when it's really SPEC) wastes a delegation on the wrong artifact.

## Risk-tier (scale verification to stakes)
- **Critical path** (money / auth / data-loss surface): full phases + property tests + adversarial impl review.
- **General feature**: phases 1–2 + run acceptance + compile.
- **Throwaway / demo**: minimal — acceptance test + compile.

## Common Mistakes
| Mistake | Fix |
|---|---|
| Orchestrator writes unit tests, not acceptance | Keep the spec/impl boundary = agent boundary. Unit tests belong to the subagent. |
| Skip "must be RED first" | Non-negotiable. Green-before-impl = the test is meaningless. |
| Subagent silently edits the acceptance test to pass | Forbid in handoff AND verify by hash: snapshot before delegating, re-hash in Phase 3 — any change = FAIL. Re-run proves GREEN, not UNCHANGED; never rely on it alone. |
| Trust self-report that "tests pass" | Always run them yourself in Phase 3. |
| Over-constrain: test couples to impl shape | Test behavior (input→output), not internals. |
| Let a failing subagent loop forever | The circuit breaker stops this — 3 attempts OR the same root cause on any two attempts. Honor it. |
| Mis-route a GREEN test's hole as SPEC (re-asking the human) | Three buckets: SPEC re-opens the requirement; TEST touches only the test; IMPL only the code. A hole found by an independent check in a passing test = TEST, not SPEC — strengthen the test, don't re-interrogate the settled requirement. |
