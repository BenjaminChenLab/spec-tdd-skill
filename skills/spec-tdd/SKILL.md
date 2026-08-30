---
name: spec-tdd
description: Use when the user says "spec-tdd" or wants acceptance-test-first development delegated to a subagent — one feature, or a multi-unit batch (bug list, task-split feature). Triggers on spec-as-test, test-first-by-orchestrator, preventing weak/green-lie AI tests, circular test+implementation reasoning.
---

# spec-tdd

## Overview
Two-tier TDD split across the agent boundary: **the orchestrator writes the acceptance test (the spec) before any implementation exists; a subagent then implements to pass it and adds its own unit tests.** This breaks the circular reasoning that makes same-agent test+impl produce *green lies* — tests that merely mirror the implementation. Near-zero human cost because the orchestrator is AI.

**Core principle:** the acceptance test is authored before any impl exists, in a different context than the implementer — so it cannot have been reverse-engineered to mirror an implementation (the structural anti-green-lie guarantee). It can still be *wrong or shallow* — a misread or under-interrogated requirement produces a bad test — but that is a different failure mode, handled by RED-first, the Phase-3 adversarial read, the grill, and the attacker. **"Must be RED first"** is the built-in green-lie detector.

**Protocol:** this skill operationally enforces the spec-TDD protocol — see [PROTOCOL.md](../../PROTOCOL.md) for the canonical artifacts (A1–A16) and invariants (I1–I20).

## When to Use
- User says `spec-tdd <feature>` (the agreed trigger).
- Implementing a feature where weak/vacuous AI-generated tests are a risk.
- ONE small unit (a single bugfix-scale item, non-critical, in a session you'll clear after)? Use **`spec-tdd-lite`**, the family's in-session tier — acceptance test first, implement yourself, one fresh-context review.
- MULTIPLE independent units — a bug list, several separate fixes, or a feature split into slices? Stay HERE: **Multi-unit runs** (below) loops the phases per unit. **Count before you run:** if the task names more than one bug/fix, you are multi-unit — do NOT write one acceptance suite over the whole batch, and do NOT `spec-tdd-lite` ×N.
- Any stack. Risk-tier how much verification you run (see below).

## The 3 Phases

### Phase 1 — Orchestrator writes the acceptance test
> **Arrived from `grill-spec-tdd` / `adversarial-grill-spec-tdd`?** The acceptance test is already written and RED — skip this phase, go straight to Phase 2.

> **About to write one suite covering SEVERAL bugs/fixes at once?** STOP — that is the mega-collapse. A task naming more than one independent fix is a **multi-unit run**: go to the Multi-unit section (below) and loop per unit.

> **Spec not a doc — settled only in this conversation, nothing on disk?** Prompt once: "persist a spec doc?" — default **YES**. A conversation is not durable recall (sessions get cleared/compacted); the doc survives. After the test is RED, write the requirement verbatim + your interpretation decisions + the acceptance-test path to `docs/specs/YYYY-MM-DD-<feature>.md` (follow the project's convention if it has one) — it is what later recall reads (SPEC-bucket re-opens, PR review, audits). Only an explicit "no" skips it — an unanswered prompt is not a no. Arrived from either grill front-end? The final decision spec was already persisted at the gate — skip this.

1. Requirement unclear? **Ask, don't guess.** (Can't write the test = the spec is unclear — that's the signal, surfaced before coding.)
2. **Ground it**: read relevant entities/services/repos/existing patterns first; the test must fit the real architecture.
3. **Write BEHAVIORAL acceptance tests** — black-box, input→output/state. Test WHAT, not HOW. Don't couple to internal method shapes.
4. (Domain logic only) add 1–3 **property/invariant tests** (e.g. money conservation, net-zero offset). Properties can't become green lies and don't over-constrain design.
5. **Run it — MUST be RED.** Green with no impl = fake test (vacuous / over-mocked); rewrite it. Intermittently green with no impl (fails, then passes on a re-run — e.g. after any audit-fix re-RED) = same verdict: pre-impl the non-determinism is test-side (unpinned seed, wall clock, live dependency, suite interference); pin it before dispatch.
   - **RED-purity check:** scan the FULL compiler/runner error list, not just the tail. Every error must point at symbols the feature will create. Any error about EXISTING symbols — wrong constructor arity, ambiguous method overloads, unused imports — is a defect in YOUR test, not feature absence. Exception: if the spec itself explicitly calls for changing that existing symbol (a breaking-change feature), the error points at the shape the feature will create — the RED is good. Otherwise fix the test before dispatch; a defective RED masquerades as "feature missing" and the implementer will bend production to accommodate it.
6. **Encoding audit — dispatch it, TOP-TIER model (grill arrivals skip: already audited at the front-end; throwaway risk-tier may skip).** No human gates this test, so before dispatch a fresh context checks it encodes the settled spec (I13 — no unaudited test crosses the boundary; I19 — every review dispatch names the top tier). Persist the spec doc FIRST if you haven't (I17 — RED is done at step 5; the auditor reads the doc):
   ```
   REVIEW an acceptance test you did NOT write.
   SETTLED SPEC: {spec doc path — READ it; it holds the requirement verbatim + decisions (A15). Paste only when persistence was declined}
   ACCEPTANCE TEST (+ property tests), currently RED: {file or paste}
   READ FIRST: {codebase paths}
   1. Does every spec line have an assertion with discriminating power? Name a
      wrong-but-plausible reading of the spec this test still satisfies.
   2. Surface anything asserted BEYOND the spec, and every silent interpretation.
   RETURN: findings (missing line / vacuous assertion / over-assertion / silent
   interpretation / none), each quoting what it rests on. Do NOT edit any file.
   ```
   Adopt findings → fix the test → **re-confirm RED**. No dispatch tool? Disclosed same-context re-read + requirement-line audit, noted in the handoff — never silent.

### Phase 2 — Delegate to subagent (Agent tool)
**No dispatch tool available** (you are running inside a subagent)? Don't improvise a protocol: single-unit work → the `spec-tdd-lite` pattern (in-session implement, solo re-RED, its disclosed degraded review); a batch → the Multi-unit degraded path (below). Say so in the report either way.

**SPEC-INTEGRITY snapshot (before dispatch):** hash the acceptance test — `sha256sum <file>` (Unix) / `certutil -hashfile <file> SHA256` (Windows) / `git hash-object <file>` — and record it. This is the immutability baseline you verify in Phase 3.

**Dispatch model: MID tier, stated on the dispatch (I19).** The implementer's tier is not a quality lever — the acceptance test enforces the spec and every reviewer of this output runs top-tier; an unstated model silently inherits the session's most expensive.

Handoff prompt:
```
TASK: Implement {feature} so the acceptance test below passes.
Do NOT modify the acceptance test — it is hashed and verified byte-for-byte on return. If it looks wrong, STOP and report back — never silently weaken it.
If the acceptance test cannot compile or pass because of a defect in the TEST itself (wrong constructor arity, ambiguous overload matchers, unused stubs under strict stubs, assertions contradicting the spec), STOP and report it as SPEC-DEFECT with evidence — do NOT change production code to make a defective test compile or pass. Production changes that exist solely to accommodate a test defect count as a FAILED run. Reporting a genuine SPEC-DEFECT is the correct outcome, not a failure to implement — you will not be penalized for it. Note: an arity/signature error on a symbol the requirement itself explicitly changes is NOT a test defect — implement the change.

ACCEPTANCE TEST (written, currently RED):
{file:line or paste}

INTENT (plain language): {1–3 sentences}

READ FIRST: Entity {path}, Service {path}, Repository {path}, Pattern-to-follow {path}

DO: 1) make acceptance test GREEN  2) add your own unit tests (red→green each)  3) follow existing conventions.
CIRCUIT BREAKER: STOP if either fires — (a) the test still fails after 3 repair attempts, OR (b) **the same root cause appears on ANY two attempts** — same failing file:line AND same failing assertion (not necessarily consecutive; not a rephrased free-text trace). Don't burn a third attempt re-trying one identical misdiagnosis — each attempt must rest on a DIFFERENT root cause. Report a short structured diagnosis — tag it env/dependency (ERR-01), logic violation (ERR-02), or syntax/compile (ERR-03) — with a TRUNCATED trace and expected-vs-actual. Don't keep retrying.

RETURN: impl + unit-test PATHS + notable decisions (every deviation from the spec'd shape: symbols added/renamed/moved beyond the spec) + ONE status line per command (command + pass/fail counts) with the FULL output in a scratch log file (e.g. `.spec-tdd/<feature>-run.log` — working notes, never committed; hand its path) — the orchestrator re-runs everything itself and compares against your status lines (I19: evidence as files, verification by re-run) — or, if you stopped on SPEC-DEFECT, the defect report with evidence instead of green output.
```

### Phase 3 — Orchestrator verifies
1. **SPEC-INTEGRITY check:** re-hash the acceptance test and compare to the Phase-2 snapshot. Any change → the implementer edited the spec → **FAIL**, even if a re-run is GREEN (a weakened-but-green test is the green lie) → route to **TEST** (step 7); never accept a changed test. *(This binds the implementer; your own step-3 strengthening and step-4 SPEC-DEFECT correction are separate, explicitly re-RED'd steps.)*
2. **Run the acceptance test yourself** (don't trust the subagent's self-report) → must be GREEN.
3. **Adversarially read the test**: "could this pass even if the impl were subtly wrong?" If yes, strengthen — and if you change the test, re-confirm it goes RED against the current impl, then re-delegate to restore GREEN. Never declare done on a test you just edited without re-running it. Also check it fits existing architecture/conventions and any security/resilience edge cases. **Correcting expected values mid-verification?** Legitimate only when justified against the requirement itself (re-derive the arithmetic independently) — never "to match what the impl returns"; disclose the correction in the report.
4. **SPEC-DEFECT sweep:** diff the returned production changes against the spec/plan. The sweep's subject is changes to code this dispatch did not create — new code is the feature's own shape. The tell: a change no production behavior needs — it exists only to satisfy the acceptance test, and the test is not a production caller — is an accommodation of a test defect, whatever shape it takes: helper/compat constructors, renamed public methods, logic beyond what the spec asks for. (When the test itself is defective, the implementer's only lever is production — it will bend production instead of reporting.) Any accommodation → fix the acceptance test (the orchestrator's own artifact: correct it, re-hash, note the correction) and restore production to the spec'd shape. Scrutinize the implementer's "notable decisions" list specifically for this failure mode.
5. **Surface the TEST (the spec) to the user for review — not the impl.** Reviewing the test is the cheap, high-signal human checkpoint: the human validates WHAT, the agent validates HOW.
6. Compile + relevant suite.
7. **On failure — or a hole found in a GREEN test — route by root cause, three buckets only:**
   - **SPEC** — you misread or under-interrogated the requirement; the test encodes the wrong behavior → re-open the requirement (ask the human / re-grill), rewrite the test, re-confirm RED, re-delegate.
   - **TEST** — the requirement is right but the executable spec is weak/incomplete (a missing case), defective (a SPEC-DEFECT), or the implementer edited it → strengthen/revert/correct the test, re-confirm RED, re-delegate. Do NOT re-open the requirement.
   - **IMPL** — the spec is right, the code is wrong → re-delegate with the failing case + the subagent's ERR tag.
   Key: SPEC re-opens the *requirement*; TEST touches only the *test*; IMPL touches only the *code*. Mis-routing (e.g. TEST when it's really SPEC) wastes a delegation on the wrong artifact. SPEC vs TEST: a defect you can fix by consulting artifacts you already hold (the requirement/plan) is TEST; a test fix that requires deciding something the requirement doesn't decide is SPEC — ask the human.
   **Flaky — a failure that flips across identical re-runs** — diagnose the side before bucketing: non-determinism in the TEST itself (unpinned seed, wall clock, a live network the test calls) = TEST — pin it, re-run, then trust the verdict; a deterministic test still flipping = IMPL non-determinism (a real race — the flake IS the bug) → re-delegate with the flake as evidence. Re-running-until-green buries the signal either way.

## Multi-unit runs (bug batches, task-split features)
The work is a batch of independently-testable units — a bug list, several separate fixes, or a feature deliberately split into slices? **If the task names more than one bug/fix, you are here.** **The agent boundary is per unit, not per feature.** Never mega-dispatch the batch (one implementer drowning = all-or-nothing circuit breaker), never run `spec-tdd-lite` per unit in-session (N inner loops drown YOUR context), never write one monolithic suite over the batch. Loop the 3 phases per unit:

1. **Unit plan.** Unit = one independently-testable behavioral slice. Bug list: one bug = one unit, its repro test = the acceptance spec. Feature: slice **vertically** — each unit delivers observable behavior; infra/scaffolding belongs to the first behavioral unit that needs it (a standalone infra unit has no black-box spec — forbidden). Pure refactor = one unit; characterization tests are its spec. Group same-module bugs into one dispatch (shared grounding); unrelated units dispatch separately.
2. **Plan up front — surfaced, not gated.** Tiers run AFTER the spec is final (a front-end's gate, or the requirement arrived settled) — **no human gate here**; the unit plan is HOW, not WHAT (I12). Write the unit plan + every spec writable NOW (bug batch: all repro tests, RED against current code — a control case asserting still-correct behavior may pass pre-fix; fine, as long as each unit's bug-specific cases fail; feature split: only the first unit's — later specs are written just-in-time, grounded in the codebase as it exists after earlier units land), surface both at the start and carry them in the batch summary — an interactive human can redirect on sight; the batch does not wait for an OK. **Running ledger (A16):** open a row per unit AT DISPATCH (unit, spec path, hash, dispatch model) in a scratch file (e.g. `.spec-tdd/batch-ledger.md` — working notes, never committed); update verdict + evidence log path as the unit's phases complete. It survives context compaction — a compacted orchestrator re-reads it and RESUMES (a row with no verdict = the unit was in flight: re-run its Phase 3, don't blindly redo) — and step 5's summary is generated from it.
3. **Loop per unit/group:** Phase 1 (this unit only) → Phase 2 dispatch (hash per unit spec) → Phase 3 verify (re-run, re-hash, SPEC-DEFECT sweep). A critical/branchy unit runs its Phase 2–3 at that tier's verification depth (e.g. the adversarial attacker dispatch) — applied to that unit inside this loop, not a re-invocation of another skill; the tier attaches to the unit, not the batch.
4. **Breaker per unit.** A stuck unit parks after the circuit breaker fires (3 attempts / same root cause twice) — report it, continue the batch. A grouped dispatch that trips gets split; retry the unstuck members.
5. **End: batch summary (from the ledger)** — per unit: spec + green-evidence log path (+ any SPEC-DEFECT corrections); parked units surfaced with their diagnosis.

**No dispatch tool available** (you are running inside a subagent)? Per-unit boundaries still hold: per-unit spec, per-unit RED, then **fix one unit → its spec goes GREEN → next unit** — yes, even for tiny disjoint fixes in one small file: the sequence IS the boundary, "they're tiny and disjoint" is the rationalization, not the exception. Solo re-RED replaces the hash here (as in `spec-tdd-lite`); the degradation is **disclosed** in the batch summary (no fresh implementer context, no fresh reviewer). Never collapse the batch into one monolithic suite "for efficiency" — a unit that then fails has no boundary of its own.

Per-unit orchestrator cost stays: write spec, review (encoding audit), hash, dispatch, re-run. That is the point.

## Risk-tier (scale verification to stakes)
- **Critical path** (money / auth / data-loss surface): full phases + property tests + adversarial impl review.
- **General feature**: phases 1–2 + run acceptance + compile.
- **Throwaway / demo**: minimal — acceptance test + compile.

## Common Mistakes
| Mistake | Fix |
|---|---|
| A batch arrives → one mega-dispatch with every unit, or `spec-tdd-lite` ×N in-session | Multi-unit runs: the boundary is **per unit** — loop the phases per unit; group same-module bugs per dispatch. |
| "The fixes are tiny and disjoint — one combined edit, then verify everything" | Per-unit green is the boundary: fix one unit → its spec GREEN → next. A combined edit is the mega-collapse with extra steps. |
| Orchestrator writes unit tests, not acceptance | Keep the spec/impl boundary = agent boundary. Unit tests belong to the subagent. |
| Skip "must be RED first" | Non-negotiable. Green-before-impl = the test is meaningless. |
| Subagent silently edits the acceptance test to pass | Forbid in handoff AND verify by hash: snapshot before delegating, re-hash in Phase 3 — any change = FAIL. Re-run proves GREEN, not UNCHANGED; never rely on it alone. |
| Trust self-report that "tests pass" | Always run them yourself in Phase 3. |
| Over-constrain: test couples to impl shape | Test behavior (input→output), not internals. |
| Let a failing subagent loop forever | The circuit breaker stops this — 3 attempts OR the same root cause on any two attempts. Honor it. |
| Mis-route a GREEN test's hole as SPEC (re-asking the human) | Three buckets: SPEC re-opens the requirement; TEST touches only the test; IMPL only the code. A hole found by an independent check in a passing test = TEST, not SPEC — strengthen the test, don't re-interrogate the settled requirement. |
| Reads only the tail of the RED error list, then dispatches | Full-list RED-purity check (Phase 1): every error must point at symbols the feature will create; errors about EXISTING symbols (wrong ctor arity, ambiguous overloads, unused imports) = your test's defect — fix the test before dispatch (unless the spec itself explicitly changes that symbol — breaking-change feature, good RED). |
| GREEN accepted without diffing the returned production changes against the spec | SPEC-DEFECT sweep (Phase 3): a compat constructor, renamed public method, or logic beyond spec scope passing green = a bent production, not a passing spec — fix the test (re-hash, note the correction), restore production. |
| Dispatch sent with no model stated — it silently inherits the session's most expensive (a whole run can land top-tier unnoticed) | Every dispatch names its model (I19): implementers MID, every review/audit/attack dispatch TOP. |
| Green evidence returned as a pasted full log, parked permanently in the orchestrator's context | RETURN = status lines + a log file path (I19); the proof is the orchestrator's own re-run (I5), never the paste. |
| Flaky failure re-run until green, or bucketed blind | Diagnose the side first: test-side non-determinism (unpinned seed / wall clock / live network the test calls) = TEST — pin it; a deterministic test still flipping = IMPL race (the flake IS the bug). Re-run-until-green is the anti-pattern. |
