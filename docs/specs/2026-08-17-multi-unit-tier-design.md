# Design: `spec-tdd` multi-unit runs — v1.4.0

**Date:** 2026-08-17 · **Status:** approved in session · **Version target:** 1.4.0

## Motivation

Two real usage patterns emerged after v1.3.0 shipped `spec-tdd-lite`:

1. **One small bug in a disposable session** — lite fits: the inner loop's
   main-context pollution is bounded (one loop, session cleared after).
2. **A batch of units** (bug list, or a feature deliberately split into task
   slices) — lite's structure fails here: N in-session inner loops scale
   pollution linearly with N, and the user must `/clear` mid-stream.

Current routing actively misroutes case 2: `grill-spec-tdd`,
`spec-tdd-escalate`, and `spec-tdd` itself all say "bugfix-scale → lite
(delegation overhead would dominate)" — true only for an *isolated single*
unit. It is false for batches: a repro-test-first bug dispatch is cheap (the
subagent receives a failing test + trace; grounding is minimal). Nothing in
the family defines how to run a batch, so agents improvise: one mega-dispatch
(moves the drowning into the implementer; all-or-nothing circuit breaker) or
ad-hoc loops.

## The frame that settled the debate

Two orthogonal axes — *(implementation in-session vs delegated) ×
(verification by executable spec vs by prose)*:

| | Executable verification | Prose verification |
|---|---|---|
| Delegated | `spec-tdd` (one dispatch per feature) | superpowers SDD (per-task dispatch + prose review) |
| In-session | `spec-tdd-lite` (sole occupant) | bare TDD — the family's anti-pattern |

Replacing lite with SDD would jump quadrants and surrender the executable
oracle — the family's core identity. The user's actual want ("bugs to
subagents, main session reviews each") is not SDD: it is **`spec-tdd` at unit
granularity** (repro test = acceptance spec; orchestrator review = re-run +
hash + diff-scan — stronger and cheaper than a prose spec-review). SDD's real
advantage over `spec-tdd` is task granularity + between-task checkpoints, not
prose; a multi-unit mode captures that advantage while keeping the oracle.

Rejected alternatives: (c) demote lite to dispatch-unavailable-only — kills a
real, in-use quadrant (single-bug disposable sessions); (a) routing fix alone
— corrects the lie but leaves batches homeless (improvisation is the failure
mode being fixed); (b) as a new sibling skill — adds routing surface, a
redirect hop on direct `spec-tdd <bug list>` invocation, and a full extra
TDD-for-docs baseline, for no invariant gain.

## Decision

Multi-unit runs live **inside `spec-tdd`** as a loop over the existing 3
phases. The agent boundary moves from per-feature to per-unit; the invariants
do not change — their granularity does. Routing at three sites becomes
honest (single-unit vs multi-unit), and `spec-tdd-lite` re-scopes to "one
unit, disposable session" with an explicit escape rule. Version 1.4.0.

## Changes

### 1. `skills/spec-tdd/SKILL.md` — new section (after the 3 Phases, before Risk-tier)

```markdown
### Multi-unit runs (bug batches, task-split features)
The work is a batch of independently-testable units — a bug list, or a
feature deliberately split into slices? **The agent boundary is per unit,
not per feature.** Never mega-dispatch the batch (one implementer drowning =
all-or-nothing breaker), never run `spec-tdd-lite` per unit in-session
(N inner loops drown YOUR context). Loop the 3 phases:

1. **Unit plan.** Unit = one independently-testable behavioral slice.
   Bug list: one bug = one unit, its repro test = the acceptance spec.
   Feature: slice **vertically** — each unit delivers observable behavior;
   infra/scaffolding belongs to the first behavioral unit that needs it
   (a standalone infra unit has no black-box spec — forbidden). Pure
   refactor = one unit; characterization tests are its spec. Group
   same-module bugs into one dispatch (shared grounding); unrelated units
   dispatch separately.
2. **One checkpoint up front** (where the entry allows a gate): surface the
   unit plan + every spec writable NOW (bug batch: all repro tests, RED
   against current code; feature split: only the first unit's — later
   specs are written just-in-time, grounded in the codebase as it exists
   after earlier units land). ONE human OK covers the batch — not N.
   Arrived full-auto (`spec-tdd-escalate`)? No ask — carry the unit plan
   into the batch summary at the end instead.
3. **Loop per unit/group:** Phase 1 (this unit only) → Phase 2 dispatch
   (hash per unit spec) → Phase 3 verify (re-run, re-hash, diff-scan).
   A critical/branchy unit runs its Phase 2–3 at that tier's verification
   depth (e.g. the adversarial attacker dispatch) — applied to that unit
   inside this loop, not a re-invocation of another skill; the tier
   attaches to the unit, not the batch.
4. **Breaker per unit.** A stuck unit parks after the circuit breaker fires
   (3 attempts / same root cause twice) — report it, continue the batch.
   On a grouped dispatch that trips, split the group and retry the unstuck
   members.
5. **End: batch summary** — per unit: spec + green evidence; parked units
   surfaced with their diagnosis.

Per-unit orchestrator cost stays: write spec, hash, dispatch, re-run.
That is the point.
```

`When to Use` gains one line: "Multiple units — bug list or task-split
feature? Stay HERE (Multi-unit runs below), don't `spec-tdd-lite` ×N."

### 2. `skills/spec-tdd-lite/SKILL.md` — honest re-scoping

- **When to Use:** add the boundary condition — "ONE small unit in a
  session you'll clear/compact after — lite's inner loop lives in the main
  context **by design**. A SECOND unit in the same session → stop liting:
  switch to `spec-tdd` multi-unit (delegation is what keeps the main
  context clean)."
- **"What this gives up"** ledger gains a third entry: main-context
  pollution — the inner loop stays in your session; budget a clear/compact
  after.
- **Common Mistakes** gains a row: "Lite ×N in one session → pollution
  scales with N; second unit = multi-unit `spec-tdd`."

### 3. Routing honesty — three sites + escalate's mistakes table

Replace the single-condition "bugfix-scale → lite (delegation overhead
would dominate)" with a two-condition route. Example (grill Phase 2; the
other sites get the equivalent wording):

- **One small unit, non-critical** (single bugfix-scale item in a session
  you'll clear after — one dispatch costs more than it saves) →
  `spec-tdd-lite`
- **Multiple units** (bug list, task-split feature) → `spec-tdd`
  **multi-unit run**

- `grill-spec-tdd` Phase 2 route list: split the "Small + non-critical"
  bullet as above.
- `spec-tdd-escalate` route table: split the lite row into the two rows
  above; mistakes table gains "Multiple small items → `spec-tdd`
  multi-unit, not `spec-tdd-lite` ×N."
- `spec-tdd` When to Use line 18 (currently sends bugfix-scale to lite):
  apply the same split, pointing multi-unit at the new section.

### 4. `PROTOCOL.md` — A13 + granularity annotations (no new invariant)

- **A13 — Unit plan** (multi-unit runs): the units, their order and
  grouping, and which specs are writable now vs just-in-time. Produced by
  the orchestrator; gated once before the first dispatch.
- Artifacts A2/A3/A4/A9 gain the column note "(per unit in multi-unit
  runs)".
- Scope-per-tier table gains a footnote: in a multi-unit run, I1–I5, I9,
  I10 apply per unit; I12's single gate = unit plan + specs writable now.
- Deliberately **no new invariant**: multi-unit is a granularity change of
  existing guarantees, not a new guarantee. Version → 1.4.0.

### 5. README / CHANGELOG / sync

- README: version header; family table (lite row: "ONE small unit …
  session you'll clear after"; `spec-tdd` row gains "multi-unit runs for
  bug batches / task-split features"); decision tree splits "one small
  unit" vs "multiple units"; rule of thumb updated; superpowers-comparison
  section notes multi-unit closes SDD's cadence gap at
  executable-verification strength.
- CHANGELOG: 1.4.0 entry per existing format.
- After implementation: sync `skills/*` to `~/.claude/skills/` (both
  locations stay identical). **No git commit** (user rule).

## Verification (TDD-for-docs, per project memory)

Baseline the §1 section:

- **RED:** without the section, hand an agent a 5-bug batch under current
  skills. Expected failure modes: one mega-dispatch, an improvised loop,
  or `spec-tdd-lite` ×N. Record which occurs.
- **GREEN:** with the section, the same prompt produces: unit plan, one
  gate, per-unit (or grouped) dispatches with per-unit hashes, per-unit
  breaker behavior, batch summary.
- §2/§3 routing wording is exercised by the same runs (where does the
  agent route the batch before/after).
- Follow `superpowers:writing-skills` RED → GREEN → REFACTOR for the doc
  edits; sync both locations when green.

## Outcomes (as built, 2026-08-17)

The TDD-for-docs loop ran one baseline + four verify rounds + one
dispatch-path execution (sandbox: 5-bug Python cart, evidence in
`B:\spec-tdd-baseline\`):

- **RED (v1.3.0):** batch undefined → improvised spec-tdd/lite hybrid, one
  mega-edit for five fixes, monolithic suite, hash ceremony inverted.
- **GREEN round 1 failed — recognition, not content:** the section existed
  and was never engaged ("five bugs" ≠ "bug list" in the agent's reading).
  Closed by: When-to-Use count rule, Phase-1 mega-collapse tripwire,
  section-opening "more than one bug/fix = you are here".
- **Rounds 2–3:** per-unit green written as a sequence ("fix one unit →
  GREEN → next"), explicit counter for the "tiny disjoint fixes" combined-edit
  rationalization, control-case-green clarification, Phase-2 no-dispatch
  fallback split (single unit → lite pattern; batch → multi-unit degraded
  path), Phase-3 constants-correction rule. Round 4: full compliance.
- **Dispatch path executed by the orchestrator in the main session:** unit
  plan (5 units, same module → one grouped dispatch) → per-unit specs RED →
  A4 hashes → one implementer dispatch → A9 re-hash byte-identical, own
  re-run green, diff-scan clean → batch summary. Zero improvisation.

