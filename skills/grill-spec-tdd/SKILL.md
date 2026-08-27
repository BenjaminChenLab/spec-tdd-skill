---
name: grill-spec-tdd
description: Use when the user says "grill-spec-tdd", or wants to interrogate/grill requirements before a test-first delegated implementation — especially for fuzzy or high-stakes (money/auth/data) features. Triggers on requirement grilling before coding, spec-as-test, test-first-by-orchestrator, and avoiding wasted subagent runs on wrong-direction specs.
---

# grill-spec-tdd

## Overview
**The requirement-grilling front-end for the `spec-tdd` family.** Interrogate the requirement until it's unambiguous ("grill"), get a human OK on the **decision spec** — the grilled decisions — **BEFORE any test is written**, then derive the acceptance test from the **final** (gate-approved) decision spec, still before any implementation exists — THEN route to the verification tier that fits the stakes and size: `spec-tdd-lite` (one small non-critical unit — in-session), `spec-tdd` (default; multi-unit for batches), `spec-tdd-coverage`, or `spec-tdd-adversarial`. That tier carries the handoff, circuit breaker, and failure routing (lite: in-session loop + review dispatch).

**Why a separate front-end:** under pressure, agents skip grilling and hand a subagent a fuzzy spec, or collapse it to "sensible defaults." Grilling first forces every dimension (incl. NFR + security) explicit and gets a human OK on direction before tokens are burned — on the test-authoring run AND the subagent run.

**Core principle (inherited from `spec-tdd`):** the acceptance test is authored before any impl, in a different context than the implementer — so it cannot have been reverse-engineered to mirror an implementation (it can still be *wrong*; that's a different failure mode). **"Must be RED first"** is the green-lie detector. **Plus (this front-end): the gate owns the spec; the test encodes the final spec.** A test written before the gate anchors to the draft — a gate amendment then lands as a one-line tweak instead of a re-derivation, and the test encodes the draft, not what the human approved. So: no acceptance-test tokens before the gate says yes.

## When to Use
- User says `grill-spec-tdd <feature>`.
- Requirement is fuzzy, high-stakes (money / auth / data-loss), or a wrong-direction subagent run would be expensive.
- For an already-settled requirement (no grilling needed), skip this: low-stakes and you know the tier → `spec-tdd` directly; want the tier auto-picked by stakes → `spec-tdd-escalate`.
- Fuzzy requirement on a CRITICAL surface (money movement / auth-permissions / data-loss) → **`adversarial-grill-spec-tdd`** — the upgraded front-end that dispatches an independent auditor to attack the grill's decisions BEFORE the gate and the final-spec acceptance test after it (pre-dispatch).

## Phase 1 — Grill the requirement, gate the SPEC (no test yet)
1. **Grill in batches** — interrogate EVERY dimension, not just the obvious ones: business logic, boundary/edge cases, state transitions, **NFRs (perf / scale / cost)**, and **security / fraud / abuse**. Force an explicit decision on each. *If you can't state a decision for a dimension, you haven't grilled it.*
   - **Grilling ≠ silent defaults.** Deciding deliberately after interrogating every dimension is the grill; collapsing to "sensible defaults" without hitting NFR/security is the failure mode. A missed dimension isn't a design decision — it's an absent one (e.g. coupon fraud, lockout-DoS).
   - **The grill is self-directed.** Stakeholders unreachable tonight? You still grill — you interrogate and decide. Their reachability affects the *gate* (step 3), not the grill.
   - **STOP GRILLING when remaining open questions cannot materially change** observable behavior, state transitions, failure semantics, data integrity, security/authorization, compatibility, or explicit NFRs. The grill is bounded by *materiality*, not by asking until exhausted — a question that wouldn't change any of those is bureaucracy, not grilling. Note it and move on; don't let the grill devolve into an endless question loop.
2. **Ground it**: read the relevant entities/services/repos/patterns first; the decisions must fit the real architecture, and so must the test that follows.
3. **Spec gate — human OK on the decisions, BEFORE any test is written.** Surface the grilled decisions in plain language — the decision spec — bundled with the routing choice (Phase 3) and the spec-doc ask (below) as ONE go-ahead. The gate checks **direction** (is this the right spec?) so you don't burn test-authoring and subagent tokens on the wrong thing — executable tests catch *logic* bugs, not wrong-direction work, so "my tests will encode my assumptions" is **not** a substitute for the gate. Approval with amendments folded in = the **FINAL SPEC** — the single source the acceptance test is derived from.
   - **Persist the spec doc (default ON).** Write the final spec to a doc — `docs/specs/YYYY-MM-DD-<feature>.md` (follow the project's convention if it has one) — so later recall (SPEC-bucket re-opens, PR review, audits) doesn't depend on session memory. Bundle the ask into this gate ("persist to <path>?"); skip ONLY on an explicit decline — an unanswered ask is not a decline, persist.
   - **No human reachable?** Grill fully (it's self-directed), document + persist every decision — then **STOP at the gate**. No test tokens, no dispatch, until a human approves. The gate is **blocking**: "they'll answer eventually" is not an approval, and a slow answer never licenses proceeding on guesses — the parked decision doc is exactly what makes the eventual review a fast one. Never use "no one's reachable" to skip the grill either — the grill is what produces the artifact the gate will review.
   - **Throwaway tier** may skip the gate — the grilled decisions are then the final spec (throwaway stakes don't justify the stop). The spec-doc default (above) still applies: persist unless explicitly declined.

## Phase 2 — Write the acceptance test FROM the FINAL SPEC
1. **Derive BEHAVIORAL acceptance tests from the final spec** — black-box, input→output/state. Test WHAT, not HOW; don't couple to internal method shapes. **Every gate amendment included** — re-derive from the final spec; there is no earlier draft to patch. **Multi-unit route:** write the specs writable NOW (bug batch: every repro test; feature split: the first unit's) — later units' specs are just-in-time at the tier, grounded in the codebase as it exists after earlier units land. Test-writing surfaces a decision neither grill nor gate made? Test-local mechanics (fixtures, naming, arrange details) are yours to decide; anything that changes observable behavior, state transitions, failure semantics, data, security, compatibility, or NFRs goes back to the human — never decided silently into the test.
2. (Domain logic only) add 1–3 **property/invariant tests** (e.g. money conservation). Properties can't become green lies.
3. **Run it — MUST be RED.** Green with no impl = fake test (vacuous / over-mocked); rewrite it.
   - **RED-purity check:** scan the FULL compiler/runner error list, not just the tail. Every error must point at symbols the feature will create. Any error about EXISTING symbols — wrong constructor arity, ambiguous method overloads, unused imports — is a defect in YOUR test, not feature absence. Exception: if the spec itself explicitly calls for changing that existing symbol (a breaking-change feature), the error points at the shape the feature will create — the RED is good. Otherwise fix the test before routing; a defective RED masquerades as "feature missing" and the tier's implementer will bend production to accommodate it. (The tier skips its Phase 1 on arrival from here — this check is the only RED audit the test gets.)

## Phase 3 — Route to the verification tier (INVOKE the skill — don't hunt for files)
The spec gate (Phase 1, step 3) was the ONE human checkpoint. Now route by INVOKING the chosen tier as a skill. **Do NOT search the filesystem for `SKILL.md` files or wonder "how are these skills organized?"** — skills are loaded BY NAME through the Skill tool. (Fallback only if a name truly won't load: read `~/.claude/skills/<name>/SKILL.md`.)

Pick by stakes and size, then call the Skill tool with the exact name:
- **Correctness-CRITICAL** (money movement / auth-permissions / data-loss) → invoke **`spec-tdd-adversarial`**.
- **Need branch-coverage EVIDENCE** (large/subtle branch surface: concurrency/parsing/state machines; weak unit tests; compliance proof) → invoke **`spec-tdd-coverage`**.
- **One small non-critical unit** (a single bugfix-scale item in a session you'll clear after — one dispatch costs more than it saves) → invoke **`spec-tdd-lite`** (the in-session tier; it keeps the grilled acceptance test and skips the implementer dispatch).
- **Multiple units** (a bug list, or a feature split into slices) → invoke **`spec-tdd`** as a **multi-unit run** (its Multi-unit section takes over; specs not yet writable are written just-in-time per unit).
- **Otherwise** → invoke **`spec-tdd`** (the default).

When the tier loads:
- **The grilled acceptance test is already written and RED** → SKIP the tier's Phase 1 (orchestrator-writes-test); go straight to its Phase 2 (delegated tiers: hand off to the subagent; `spec-tdd-lite`: implement in-session). Don't re-write or re-confirm the test.
- The gate already passed → execute per the tier's handoff (delegated tiers: dispatch; `spec-tdd-lite`: implement in-session). **Do NOT come back asking "should I hand this to a subagent?"** — that decision is made; you're executing it.
- Hand off the grilled acceptance test as the contract; the tier implements, it does not re-litigate decisions the grill already locked.

## Red Flags — STOP
- "The failure mode isn't a wrong design decision, so I'll skip grilling."
- "I'll just pick sensible defaults and note them." (did you hit NFR + security?)
- "No one's reachable tonight, so I'll skip the grill / proceed past the gate." (the grill is self-directed; the gate is blocking — park with decisions persisted, don't proceed)
- "I still have more questions to ask." — but none would change behavior, state, failure semantics, data, security, compatibility, or NFRs. (STOP GRILLING — materiality bounds the grill, not exhaustion)
- About to write the acceptance test and the spec gate hasn't approved the decisions. (No test tokens before the gate — the test encodes the FINAL spec, amendments included.)
- "The human amended a decision — I'll adjust the matching test line and move on." (The test is derived from the final spec as a whole; a patched draft encodes the draft.)

## Common Mistakes
| Mistake | Fix |
|---|---|
| Skip the grill, hand a subagent a fuzzy spec | Grill every dimension (incl. NFR + security) first; a fuzzy spec wastes the whole subagent run. |
| Collapse the grill to "sensible defaults" | Deciding deliberately after interrogating ≠ assuming silently. |
| Writes the acceptance test before the spec gate | Gate the decisions first — the gate may amend the spec, and a pre-gate test anchors to the draft. The test is derived from the FINAL spec, after the gate. |
| A test-writing question the grill/gate didn't decide, resolved silently in the test | Test-local mechanics are yours; anything that changes behavior/state/failure/data/security/compat/NFR goes back to the human. |
| Spec doc skipped because "the test file records it" | Tests are for running, docs are for recalling. Default ON; only an explicit decline skips. |
| Skip the approval gate because "tests encode my assumptions" | The gate checks direction on the decisions; tests catch logic. No human? PARK at the gate — the grill already ran and is persisted; that's what they'll review when they arrive. |
| Route everything to base `spec-tdd` | A fuzzy+critical feature goes to `spec-tdd-adversarial`; fuzzy+coverage-needed to `spec-tdd-coverage`. Pick the tier by stakes. |
| Re-litigate grill decisions inside the tier | The acceptance test + grilled decisions are the contract; the tier implements, not re-decides. |
| After RED, come back and vaguely ask "hand off to a subagent?" | The gate (Phase 1, step 3) is the single checkpoint and must bundle the routing choice; once approved, INVOKE the tier — don't re-ask. |
| Hunt the filesystem for `SKILL.md` / "how are these skills organized?" to route | Invoke the tier BY NAME via the Skill tool; never search the disk for skill files. |
| Reads only the tail of the RED error list, then routes | Full-list RED-purity check: errors about EXISTING symbols (wrong ctor arity, ambiguous overloads, unused imports) = your test's defect — fix before routing (unless the spec itself explicitly changes that symbol — breaking-change feature, good RED). The tier skips its Phase 1, so no one downstream re-audits the RED. |
| Fuzzy + critical requirement ran the plain grill | The blind-spot risk sits on the decisions themselves — `adversarial-grill-spec-tdd` attacks them (pre-gate) and the final-spec test (pre-dispatch) with an independent context. |
