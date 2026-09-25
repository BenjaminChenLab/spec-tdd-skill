---
name: spec-tdd-task-loop
description: Use when driving a whole MULTI-TASK feature phase — a task plan split into many self-contained task docs, run one task at a time with per-task commits, a plan-doc status board, and sessions that must survive the phase. The main session stays a LIGHTWEIGHT gate (compile + `git diff --stat` + JUnit-XML number recheck — never deep review, never running the tests itself); each task dispatches a level-1 sub-agent that runs the spec-tdd-escalate/tier machinery and itself dispatches the nested implementer (no self-testing — requires CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3). Covers mock-first contract phases (the time dimension of tier choice), mid-run tier downgrades delivered by SendMessage, and resuming a half-finished task after a session break. Triggers on task loop, task-by-task spec-tdd, multi-task orchestration, per-task commit cadence, plan status board, not-yet-split requirement/blueprint needing task breakdown, multi-task loop.
---

# spec-tdd-task-loop

**REQUIRED BACKGROUND:** Understand the `spec-tdd` family first — the front-ends (`grill-spec-tdd`, `spec-tdd-escalate`), the tiers (`spec-tdd-lite` / `spec-tdd` / `spec-tdd-coverage` / `spec-tdd-adversarial`), and [PROTOCOL.md](../PROTOCOL.md) (I1–I21 / A1–A16). This skill adds no new invariant and relaxes none: each task's execution is still fully carried out by the tier machinery (**band caveat**: the lite floor is a compensated strengthening — a mandatory fresh review; the coverage ceiling over critical units is a structural non-carriage grounded in economics, not an invariant change — see the escape hatch below); what this file defines is the loop rules layered on the **outside** of the whole family — the three-layer division of labor, the lightweight gate, number recheck, mock-first, resume, and disclosure.

## Overview

A multi-task phase: one master task table, one self-contained doc per task, task-by-task development and commit, possibly spanning multiple sessions. **The top-level context is the scarcest resource of the whole phase** — the only thing that must live from start to end is it. So all deep work (acceptance-test writing, encoding audit, implementation, attack rounds) sinks into disposable sub-agent contexts; the top does only two kinds of things:

1. **Cross-task state management** — pick tasks, maintain the authoritative plan doc's status section and decisions section, write decisions back, one commit per task.
2. **The lightweight gate** — verify only "objectively checkable facts": compile, file scope, test numbers. Each item is machine-comparable; it needs neither taste nor level-1's full context.

| Layer | Who | Does | Forbidden |
|---|---|---|---|
| Top-level orchestrator | the main session (program conductor) | cross-task flow, the lightweight gate, status-section upkeep, decision write-back, commits | deep code review, running the tests itself, writing acceptance tests, implementing |
| level-1 sub-agent (**TOP**, I19; **eco exception — all MID + a TOP final audit per card, see the dedicated section**) | the spec-tdd orchestrator for ONE task (runs the escalate machinery) | write the acceptance test (RED), encoding audit, dispatch level-2, verify personally (re-run / coverage / hash), tier-required attack rounds; the lite route: solo implementation + a fresh-context review dispatch (that tier's own mechanical shape) | implementing production code itself (non-lite tiers — exception per the template's TIER BAND), git writes |
| level-2 implementer (**MID**, I19) | the implementer | implement to green + its own unit tests | touching the acceptance test (hash-locked), git writes |

When the tier is `spec-tdd-adversarial`, level-1 further dispatches attacker / dry-loop auditor inside itself — **adversarial is not carried inside the loop** (see Pre-flight 3's tier band): the default path for critical units is to **pull them out of the loop and run them standalone** (the Phase 0 sniff pre-pulls; a routing-point discovery STOPs and reports immediately); keeping one in-loop at coverage requires the user's explicit call and rides the residual-risk list.

**Why self-testing is banned (one agent writing code + tests + judging itself): circular reasoning.** The implementer's blind spots enter both the code and the test simultaneously; green becomes self-fulfilling. Separating implementer and orchestrator means the acceptance test is locked by a different context before the implementation exists — hash-locking the acceptance test, bit-identical verification before and after dispatch (I4, executed at level-1). This is the reason the whole family exists. In the task loop, tiers above lite are equally non-negotiable; **lite's solo mode is the entry tier's known trade, available again inside the loop since v1.20.0** (the compensation = a mandatory fresh-context review dispatch — loop economics settled: small cards don't pay the two-context tax); **if level-1 cannot dispatch nested dispatches (lite's review dispatch counts too), the only legal action is to stop and report — never degrade into unreviewed self-testing.**

## Eco mode (the `eco` flag — the supervisor-shaped per-card economics mode, opt-in trial)

**`eco` flag** (`/spec-tdd-task-loop eco <phase>`): active when args contain the token `eco` (stripped from the phase description); **runs without the token are byte-identical to before**. Mechanism = `spec-tdd-supervisor`'s per-unit economic shape applied to each card: **machinery all MID, and the single TOP judgment point per card moves to a read-only final audit at close**. Why an opt-in flag and not the default: the `dryout`/`timebox` precedent — economic modes trial first, promotion decided by real-run data; trial knobs at the end of this section.

- **Per-card dispatch economics**: level-1 and ALL of its nested dispatches (encoding audit, lite's fresh review, implementer) run **all MID** — every Agent call names MID explicitly, never omits it (omission = silently inheriting the session model, which breaks in both directions); the template's MODE field carries the MODEL PIN and the I21 pre-resolve (supervisor's shape). TOP per card drops from 2 (level-1 + encoding audit) to 1 (the final audit).
- **Per-card TOP final audit (after the gate, before commit)**: lightweight gate items 1–4 pass → the top dispatches **ONE TOP read-only final-audit dispatch** (background mode; at dispatch announce to the user what is being audited — no reporting and no predicting before the notification arrives). Brief = fixed checklist + doc paths, no summaries, no pre-digestion (I19(c)): the task doc path, the acceptance test path, level-1's `REPORT.md` (eco's RETURN additionally writes this file — the substrate for the final audit and for session-break resume), the JUnit XML directory, the created/modified list, the hash pair (the lite route carries a "no hash pair" note), the absolute path of `FINAL-AUDIT.md` (pasted by the top — the auditor's only write target, never self-composed). The four checklist items are verbatim the supervisor final review's a–d, **the first item fixed as the acceptance-test encoding-fidelity re-read** (the all-MID compensation control — the encoding-audit duty I19(a) originally pinned to TOP is taken over by the final audit). Evidence rules: every finding carries `file:line`; every OK names the attack it tried (I16).
- **Findings loop (bounded to one round)**: SendMessage resumes level-1 to fix (only if unresumable, re-dispatch a continuation — keep, don't rewrite) → **the SAME auditor** re-checks the delta (the adoption check needs memory, I16) → not converged escalates to the user; no infinite loop. Default-adopt arbitration: a rejection must carry the evidence the auditor lacked and surface upward; ambiguities that depend on grilling intent always go up (I12 — the auditor only sees the doc).
- **Close order**: gate 1–4 → final audit converges (or escalates) → only then commit — the task stays in-flight until the final audit converges; **commit-before-audit = all-MID with no TOP judgment point — a downgrade, not a saving**. Pure-docs tasks skip the final audit (no test to audit; they keep the shrunk gate — the same shape as supervisor's When-NOT).
- **What does not change**: the tier band (lite…coverage) and the adversarial escape hatch, Phase 0 (top-authored, I19(a)), **the I21 ask runs as usual** (the session still holds the Phase 0 breakdown and board judgment — eco only moves per-card dispatch economics, not the session's judgment premises), the lightweight gate items, **the closing batch review runs as usual and is additive, not a substitute** (the per-task final audit catches single-card holes, the closing review catches cross-card holes — both coexist), the watchdog (the final-audit dispatch registers as **read-only-class**: budget = the coarse minutes-to-tens-of-minutes cap stated at dispatch; on death, ONE fresh re-dispatch, the new auditor re-reads everything from `FINAL-AUDIT.md`, disclosed).
- **Known costs (recorded honestly, the ×N version of supervisor's opt-in) and trial knobs**: a weak test first drives a full implementation and is only caught at the final audit — the fix rides a findings re-dispatch, more expensive than I19(a)'s pre-implementation interception; the findings loop's wall-clock and the session's default-adopt arbitration load accumulate per card. **Trial knob: findings-round rate × per-round cost vs TOP saved** — the phase report records final-audit rounds, findings count, re-dispatch count; after a few real phases decide whether to promote (dag's top-context ×N quota pain point is the biggest beneficiary — see the dag delta).

## When to Use

- A feature phase split into many tasks (typically 5+), one self-contained doc per task, developed and committed task by task.
- Expected to span multiple sessions, with context compaction or breaks → needs the status section + the half-finished-task resume mode.
- An authoritative plan doc exists (single source of truth: requirement + decisions section + task-table status section).
- Entering with only a settled requirement or a plan/blueprint, not yet split into a task table + task docs → run Phase 0 first (the table is the trace base for resume / rollback / write-back).
- Upstream dependencies (external API, another team's service) unsettled → mock-first contract development (see the dedicated section).

**When NOT to use:**
- A single task / single feature → go straight to `/spec-tdd-escalate` (or pick a tier manually); the main session orchestrates itself; the outer loop is overhead.
- Clearing a batch of independent small bugs at once → `spec-tdd`'s **multi-unit run** (loops units within one session; the boundary is the unit — no per-task commits, no cross-session state).
- Time-sensitive with a genuinely parallel DAG structure (not a chain) → `spec-tdd-task-dag` (the parallel overlay; this skill remains the serial / 429-conservative mode).
- Exploratory / throwaway code → no skill needed.

## Phase 0 — task breakdown (entering with the task table un-split)

On entry, if there is only a settled requirement or a plan/blueprint, **not yet split into a task table + self-contained task docs** → run this section first; only enter Pre-flight after the control documents exist. If the trio is already there → skip. Rationale: the status section is the trace base for breakpoint resume, the task boundary is the rollback unit, the decisions section is the home for decision write-back — **a breakdown that lives only in the conversation = not broken down** (the spirit of I17); nothing landed on disk means resume / rollback / write-back have nothing to stand on.

1. **Settlement check (I20 sniff).** Scan the requirement for decision gaps (unbound quantities, either-or choices left open, TODO/TBD): gaps found → route to the grill front-end to talk them through — don't fill holes here; clean → proceed.
2. **Breakdown (top-authored — I19(a): planning never sinks).** The top reads the settled requirement / blueprint + inventories codebase anchors (a read-only Explore may run the recon), producing: (a) the authoritative plan-doc trio (Pre-flight 5's format) — the requirement body, the decisions section (existing discussion decisions settled as D1… with numbering continued), the task-table status section (all pending); (b) one self-contained doc per task (Pre-flight 6's fields). Granularity principle: **one task, one thing** — task boundary = commit boundary = rollback unit; wrong granularity deforms the rollback unit. **Critical-surface sniff (default ON)**: during breakdown, sweep all task concepts with the stakes predicate; adversarial-grade tasks get **pulled out of the loop** before it starts (the table marks them pulled/external, run standalone; commits still land at task boundaries, the gate still checks report evidence) — a silent downgrade has no source of consent, and the double payment (coverage runs once + standalone runs again) is exactly the waste this exists to kill. **Budget size feasibility**: each task's wall-clock budget must exceed its verification plan's total build time (planned run count × full-suite duration); if impossible → split the task or raise the budget (see the watchdog section).
3. **Fresh-context plan review (independent sub-agent, TOP).** Dispatch a sub-agent that did not write the plan to attack it: requirement coverage (every requirement has a task), missing tasks, dependency order, task-doc self-containment (missing contract fields), granularity deformation (one task stuffing many things / cut pointlessly fine). Findings → the top fixes → **the SAME reviewer re-audits** (bounded: audit + one re-audit, the I16 convention).
4. **Double-consent gate.** Reviewer converged (no findings) + top sign-off → enter Pre-flight; the task table is surfaced together with Pre-flight's existing asks (no separate gate). Unresolved findings after the re-audit → escalate to the user; never start the loop with an unconverged breakdown.

## Pre-flight

1. **Orchestrator tier check (I21).** Before any work, check the model THIS session runs as. A run's judgment executes entirely in the orchestrator's own context; I19 pins every dispatch tier, but nothing can upgrade the session itself. **Top tier in use, or no higher tier exists → silent, move on.** Otherwise surface this ONE ask and stop for the answer:

   > ⚠ **Orchestrator tier check** — this session runs a non-top model, and a run's planning / verification / routing all execute on it. **Upgrade** → run `/model`, pick the top tier, say "go" (the same conversation continues). **Ignore** → continue at this tier; the decline is disclosed in the final report.

   This skill's gate is light, but the level-1 dispatch must be TOP (it inherits all the planning / verification judgment) — if the top-level session itself runs a mid tier, the whole phase's routing and review judgment rides on mid too.
2. **Session commit authorization (asked once before the loop starts).** Task boundary = commit boundary is this skill's rollback design, but commit authority is always the user's — ask once explicitly before the loop starts: "Does this session authorize the top to commit at every task boundary?" **Authorized** → after the gate passes, the top commits directly (still listing file names explicitly; push is not covered by this authorization). **Not authorized** → the boundary is not skipped: at every task boundary pause, list that commit's file manifest for the user to execute manually, and record the user-reported hash in the status section — the rollback unit is unchanged, only the executor changes.
3. **Tier band (structural, not policy, not an ask).** The in-loop tier band = **lite … coverage**: escalate routing runs unchanged inside the band (including lite — the solo + fresh-review shape for small cards; the v1.18.1 in-loop lite ban was reversed as of v1.20.0: small cards don't pay the two-context tax). **Adversarial is structurally not carried**: hours-level depth × per-task multiplication contradicts the loop's wall-clock economics ("avoid idling — this is slower than a human doing it"). The convergence point for critical units is the **escape hatch** — the Phase 0 sniff pre-pulls; a level-1 whose routing discovers it (before implementing) → STOP and report, the top pulls it out, **never silently coverage**; one the user explicitly keeps in-loop at coverage → disclosure + the residual-risk list (**the payback = pulling it out standalone, NOT a board re-test row**). The user mid-run demanding adversarial for some critical task → same pull-out; in-loop unlocking does not exist.
4. **Nested spawn depth check.** The default spawn depth limit leaves the level-1 sub-agent without the Agent tool → it cannot dispatch level-2. Fix: environment variable **`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3`**, set in the top-level session's launch environment (somewhere the harness reads — the settings env block or the launching shell's environment; exporting inside some Bash call cannot affect the parent that spawns sub-agents). Verification: the dispatch template carries "if you have no Agent tool, STOP and report immediately" — if it reports having the tool on the first task, the setting is live.
5. **Authoritative documents in place.** Before the phase starts, confirm the trio exists: (a) the requirement body; (b) the **decisions section** — numbered decisions (D1, D2…); new decisions **continue the numbering**, never renumber or renumber over; (c) the **task-table status section** — one row per task: id + plain-language name + status (pending / in-flight / done + commit hash) + one evidence pointer. Missing → back to Phase 0 to produce them; never improvise a start (using a blueprint directly as the plan, or splitting verbally and running, are both improvisation).
6. **Task-doc self-containment check.** One self-contained doc per task — the sub-agent must be able to work without opening other documents. Required fields:
   - goal and scope (with explicit **non-goals**);
   - current-state anchors: file:line (line numbers drift — also give method/symbol names as anchors);
   - design notes;
   - **the complete external contract given in full at once** — full DDL text, API shapes, interface signatures; writing "same as the previous case" or "see the requirements doc" is banned;
   - **the deliverable file list** — files this task will produce / modify; mandatory and exhaustive for pure-docs tasks (the input the lightweight gate's item 5 checks against);
   - acceptance criteria (behavior descriptions convertible into an acceptance test);
   - risks and rollback.

## The loop (one round per task)

1. **Pick a task + verify anchors.** Take the next per the table's dependency order; after the previous task lands, its file:line anchors drift — quickly verify the doc's anchors still hold, fix the doc first if not (re-anchor by method name). Mark the row in-flight.
2. **Dispatch level-1 (TOP).** Use the template below. Path shorthands inside the doc must be **restored to absolute paths** in the prompt (the sub-agent's cwd cannot be relied on); the template's `{family root}` likewise — fill the absolute path of the skill family's install location; the template's **SCRATCH ROOT** field gets this run's absolute scratch root path (the convention = repo root). Record the dispatch time and delivery class into the status section's in-flight row (the watchdog's arming baseline — see the dedicated section).
3. **After the report, run the lightweight gate** (next section). Gate fails → re-dispatch with **objective evidence** (full compile error text, out-of-list files, XML number mismatches); the three-bucket routing (I10) is level-1's internal business — the top only relays facts, never judges in its place.
4. **Decision write-back + status-section update.** Business decisions the user makes during a task are written **immediately** into the authoritative doc's decisions section (numbering continued) and the relevant task doc updated — the old plan gets struck through for the record, never deleted outright. A decision that lives only in the conversation = did not happen (sessions get cleared / compacted).
5. **Commit (top-exclusive, per pre-flight authorization).** **List file names explicitly**; `git add -A` / `git add .` strictly banned — the working directory always contains sub-agent untracked scratch (`.spec-tdd/` etc.) that would be swallowed into the commit. **This round's authoritative plan-doc updates (status section, new decisions) ride the SAME commit as the task doc's changes** — rolling back a task then rolls back its status row and decision record too, so the status section never claims a restored task is done. One-line subject. Task boundary = commit boundary = rollback unit. Record the commit hash in the status row.

### Level-1 dispatch template

```
ROLE: You are the spec-tdd orchestrator for ONE task of a multi-task phase.
Run the spec-tdd-escalate machinery for THIS task only: pick the tier by
stakes, write the acceptance test (RED, RED-purity checked), dispatch a
NESTED implementer via the Agent tool, and verify it yourself (re-run GREEN,
hash check, tier-required verification). Invoke the /spec-tdd-escalate skill
BY NAME if it is available in your runtime. If it is not, do NOT improvise
a lighter version from this prompt — read FAMILY FILES below and run that
machinery exactly.

MODEL PIN — MODE: {default | eco}. default: you run TOP and your
implementer is level-2 MID (I19); your encoding-audit / fresh-review
dispatch is TOP (I19(a)). eco: you AND every dispatch you make
(encoding audit, lite fresh reviewer, implementer) run the MID tier —
name it explicitly in every Agent call, never let one silently inherit
the session model. The judgment backstop is a TOP-tier read-only
final-audit dispatch the TOP-LEVEL session runs over your deliverable
at task close, before commit — you never see it, and it changes
nothing in your machinery. ORCHESTRATOR TIER CHECK — PRE-RESOLVED
under eco (the user's flag invocation IS the recorded decline:
all-MID machinery with a TOP final-audit backstop): do NOT stop to
ask about upgrading; carry "I21 decline recorded (eco all-MID
opt-in, at invocation)" into your report disclosures. eco adds one
RETURN duty: WRITE your full RETURN report to
.spec-tdd/<task>/REPORT.md (SCRATCH ROOT-anchored) — the final audit's
brief references it by path, and it is the audit-phase resume
substrate.

No self-testing OUTSIDE the lite tier. Same-context test+implementation is
circular reasoning: the implementer's blind spots enter both the code and
the test, and green becomes self-fulfilling — which is why every tier above
lite dispatches a separate implementer, and why lite (the entry tier for
small non-critical units) compensates with a MANDATORY fresh-context review
dispatch over its test+implementation. If your escalate routing selects
lite, run the lite machinery exactly, including that review dispatch. If
you have no Agent tool, STOP and report that fact — do NOT fall back to
implementing yourself (the review dispatch needs the tool too).

TASK DOC: {absolute path} — READ IT FIRST; it is self-contained (goal,
scope, current-state anchors, design notes, full contract incl. DDL,
acceptance criteria, risks, rollback). Doc path shorthand maps to:
{abbreviation → absolute path}.

SCRATCH ROOT: {absolute path} — paste-verbatim anchor for EVERY
`.spec-tdd/` path in this prompt (repo root; under task-dag's wave
reuse, the assigned worktree root).

FAMILY FILES (if the skill is not invocable in your runtime, READ these
from disk and follow them — the machinery lives there, not in this prompt):
{family root}/skills/spec-tdd-escalate/SKILL.md (the routing you run),
{family root}/skills/PROTOCOL.md (invariants I1–I21), and the chosen
tier's {family root}/skills/<tier-name>/SKILL.md.

DOC EDITS: report proposed task-doc / plan-doc changes; do not edit the
authoritative plan doc yourself — the top-level session owns decision
writeback.

SCOPE: this task only. Prior tasks' acceptance tests are the regression
wall: adapt one only where this task's contract evolution forces it — one
file at a time, assertion SEMANTICS unchanged, each adaptation listed in
your report with its rationale.

GIT: NO git write operations (add/commit/stash/checkout/restore/...). The
top-level session owns all commits. Read-only git (status/diff/hash-object)
is fine.

TIER BAND: lite … coverage — the loop's structural band. Your escalate
routing runs UNCHANGED inside it, including lite (small non-critical
tasks: solo author-implementer plus ONE fresh-context review dispatch —
the lite machinery's own shape; disclose the tier used). The CEILING is
structural: adversarial is not carried inside the loop (hours-level depth
× per-task multiplication contradicts its wall-clock economics). A task
whose stakes would route above coverage: STOP and report BEFORE
implementing — the top's default is to pull it OUT of the loop and run it
standalone (double-pay — coverage here PLUS a standalone run later — is
exactly the waste this band exists to kill); running it AT coverage
in-loop requires the user's explicit call at that task boundary and rides
the phase report's residual list. (Pure-docs tasks excepted — no
acceptance test to write, the tier machinery does not apply; see the
loop's gate item 5.)

MOCK PHASE: {yes/no}. If yes: the contract target is the mock established
by task {id}; reduced verification depth is user-approved for mock-phase
tasks; disclose the tier actually used.

PHASE BOUNDARIES (before/after each nested dispatch, when ENTERING a wait
on a nested dispatch, after each completed long tool run, after each
delivered file): 1) touch `.spec-tdd/<task>/HEARTBEAT` (create the
directory if missing; touch or an equivalent write) — when the touch
coincides with entering a wait, write into the file: "waiting: <child-id>
expected-done <time>"; 2) re-read `.spec-tdd/POLICY-<task>.md` — ABSENT
means ONLY a confirmed file-not-found (e.g. `test -f` fails); any OTHER
read error is a STOP, not "no policy"; a PRESENT file overrides TIER
BAND above, DOWNGRADE-ONLY (raising waits for the next task boundary);
3) PATH RULE (every `.spec-tdd/` path in this prompt — the touch, the
POLICY re-read, every scratch write, incl. RETURN's logs): form it by
prefixing SCRATCH ROOT from your brief, joined with a `/`, PASTED
VERBATIM — never retype it, never resolve it against your own cwd, never
hand-compose any other absolute form; mkdir -p plus output-redirect makes
a typo'd absolute path silently succeed, materializing a parallel tree
whose heartbeat the watchdog never sees (2026-09-18 W22 incident).
Before the first such write: `git rev-parse --show-toplevel` must equal
SCRATCH ROOT — a mismatch is a STOP-and-report, never a best-effort
guess. Carry SCRATCH ROOT and this PATH RULE verbatim into every nested
brief you compose (implementer, reviewer, attacker): their templates'
`.spec-tdd/` shorthand is anchored by YOUR pasted root, never their own
cwd.

NESTED DISPATCHES (any nested child — your implementer on tiers above
lite; your fresh-context reviewer on lite): dispatch each nested child in
BACKGROUND mode — a blocking Agent call makes you unreachable and
unmonitorable, and its never returning is NOT evidence the child lives (a
child's death is silent to you). Record the expected duration with each
dispatch (floor it at the known build cost of the affected files); on
overtime with no fresh output from the child (worktree / build outputs),
treat the child as dead: TaskStop it first (a presumed death is not a
confirmed one — two agents must never write the same tree; clear
build-process locks, e.g. stale daemons, before re-dispatching), then
re-dispatch: a CONTINUATION implementer on its partial work; for a dead
lite reviewer, a FRESH reviewer — its judgment depends on fresh context,
nothing is inherited (same re-dispatch-cost disclosure shape as the
closing review). Harness without background nested dispatch: disclose
the degradation (the top's budget backstops).

VERIFICATION REPORTING (your numbers will be independently rechecked):
  - FINAL verification = ONE gradle run covering ALL related test classes —
    each run CLOBBERS the previous JUnit XML, so only the last run survives
    for recheck.
  - Report per-class numbers read from build/test-results/test/*.xml, and
    state whether counts are @Test METHODS or EXECUTED INVOCATIONS
    (@ParameterizedTest: 1 method = N invocations).

RETURN: 1) one status line per command (command + pass/fail counts), full
logs to scratch files under .spec-tdd/ (never committed; hand paths)
 2) per-class numbers  3) created/modified file list (absolute paths)
 4) disclosures: tier actually used (+ any mid-run downgrade or band
cap), deviations from the task doc (DDL deltas, mock placement,
naming/structure), locally decided rule details  5) prior-test adaptations
with per-file rationale.
```

## In-flight monitoring (anti-idle watchdog)

429 quota exhaustion plus silent death stacked together can burn a whole afternoon on one card. **Three failure modes**: hard-fail (429 terminates directly, with a notification — covered by the existing resume rules), soft-wedge (the inference request enters a backoff-retry loop: state perpetually `running`, zero notifications, transcript stops updating — zero external signal), zombie-wait (the nested child has died silently while the parent healthily waits on an Agent call that will never return — **an Agent call not returning ≠ the child alive**). Field record: three modes stacked, one card ~6 h, ~5 h zero output — slower than a human. **The ruling: zero-output duration is the first-class metric; "avoid idling" is a fundamental requirement, not a nice-to-have**; under same-tree serial code tasks, one card idling = the whole queue stalled (under task-dag, what stalls is the wave-end merge — siblings keep running — still legitimate, for a different reason). **This is process monitoring, not a verification act**: every signal is an objective fact, no content judgment.

1. **Arming (at dispatch, registering the delivery class).** Every background dispatch the top owns — each card's level-1, the Phase 0 plan-review, the closing batch review — at dispatch time: record the dispatch moment and **delivery class** into the status section's in-flight row (the board is a file; a broken session can re-arm from it), and schedule the **whole ladder** of checkpoints via the harness's one-shot wakeup mechanism (see 2; task-dag: one wakeup serves all in-flight, not per-card scheduling). **Both layers are background dispatches** (top→level-1, level-1→nested): a blocking call makes the parent unreachable and unmonitorable — mid-run redirection, POLICY re-reads, and the watchdog itself all depend on the parent keeping tool rounds. **Delivery classes**: (i) **output-type** (code tasks) — real output = tree diff, test-results changes, deliberate task scratch the agent writes (reports / ledgers; the harness's background task files and transcripts don't count); (ii) **read-only-type** (plan-review, closing review) — zero tree output and zero builds are by design; real output = growth of heartbeat / scratch reports; applying the output-type formula to them guarantees false verdicts.
2. **Two axes and the cadence.** **Real-output age** (time since the last real output) and the **wall-clock budget** (tier-derived example defaults: lite 30 / spec-tdd 60 / coverage 120 min — environment-calibrated values, user-adjustable; read-only-type budget = the expected duration stated at dispatch). One one-shot wakeup per 15 min (example default) as a checkpoint, **the ladder scheduled in advance** — schedule the whole ladder at dispatch, not a single-shot chain: fine rungs out to the budget horizon + 2–3 coarse far-fires (e.g. +90 min / +3 h / +5 h, illustrative, user-adjustable). **Field-proven: pool exhaustion kills the main session's turns too, so the single-shot chain's re-arm premise ("if it fires, I can schedule another") collapses on the spot; the reset+15 insurance point never existed because nothing could schedule it; the far-fires are the only coverage that depends on no successful turn — the soft-wedge's unknowable reset moment is covered only by this layer**. A wakeup landing inside the exhaustion window = 0-second death, consumed in place, free (rejected requests burn no tokens — no retry traces in the field record, n=1); landing after quota recovers = the top automatically regains control. A successfully landed checkpoint turn tops the ladder back up; **every rung's prompt is self-contained and self-retiring** (carries its own board path + in-flight interpretation + "no in-flight → clear leftover checkpoints and stand down" — guards against stray far-fires after close, and survives context compaction). The ladder is **session-scoped, session-lived** (one wakeup serves all in-flight; the ×N parallel economics unchanged; cross-session recovery re-arms from the board, no durable scheduling — a durable far-fire would detonate in a context that no longer owns it). **An agent's self-reported state NEVER resets the real-output clock** (field-proven: the zombie parent's "implementer running" was proven wrong — response content is not health evidence).
3. **Three-state judgment (bound to clocks, separate tolerances).** (a) **zombie-wait** — diagnosed only on the four-condition conjunct: signs of activity (fresh heartbeat or background files appearing; the ownership of background files judged against heartbeat content — could be children's output or the parent's probe residue), zero real output, build **output not advancing** (output-directory mtime rolling is the primary signal; process presence is only corroborating — an idle resident daemon like a gradle daemon lives idle for hours by default; presence ≠ activity), and the heartbeat-declared wait overdue (the waiting entry's expected-done has passed). High-confidence death, **15-min fast knife**; (b) **total freeze** — heartbeat / background files / build output all frozen: an ambiguous state (a single long reasoning request and a soft-wedge are externally indistinguishable), **long tolerance ~90 min** (example default, user-adjustable), the budget backstops; (c) **legitimate work** — real output flowing or build output advancing → re-arm. **Instantaneous signal shapes cannot distinguish zombie from a healthy in-phase wait** (a healthy parent waiting on the encoding audit hits the first three of the four conditions) — the overdue clock is the only discriminator; that is why the three states and the nested time-limit are one integrated design.
4. **Budget = hard cap (three rules).** Exceeded → terminate and re-dispatch, **no "wait a bit longer"**. But: (i) **one-time reset while flowing** — real output flowing at the moment of overrun → reset the budget once and disclose (a size mis-estimate is a plan defect, not an agent defect; once only, against indefinite extension); stalled → terminate immediately; (ii) **continuation re-dispatch re-budgets** — re-grant by the remaining scope after inventory (inheriting a burned-through budget = instant kill); (iii) **Phase 0 size feasibility** — the budget must exceed the task's verification plan's total build time; if impossible → split the task or raise the budget (already in Phase 0). **Re-dispatch cap 2** (I9's circuit-breaker shape); beyond that, escalate to the user.
5. **Diagnosed → the matching recovery (the 429 section).** zombie → start with the revival attempt; total freeze → the soft-wedge procedure; reset moment known (any 429 message in the session names it) → additionally schedule a reset+15 insurance point. **Degradation ladder (the honest version)**: no scheduling mechanism → the watchdog degrades to board budget records + best-effort checks at natural control points + disclosure; **only when re-dispatch is also unavailable** (all pools dead / harness broken) → the degraded closing of "the top runs the final verification itself" (see the 429 section) — the last rung, not a convenience shortcut.

## The lightweight gate (the top's only verification act)

After level-1 reports, before commit, the top personally:

1. **Compiles** — runs the main module's `compileJava` + `compileTestJava` once itself (e.g. `./gradlew :Core:compileJava :Core:compileTestJava`); green or it doesn't count.
2. **File scope** — `git diff --stat` + `git status --porcelain`, against level-1's reported created/modified list; out-of-list changes = inventory first (level-1 explains or reverts) before commit. Untracked scratch directories excepted.
3. **Number recheck** — read the JUnit XML (`build/test-results/test/*.xml`) against level-1's per-class numbers (see next section).
4. **Hash spot-check** — level-1 should report the acceptance test's pre-/post-dispatch hashes (bit-identical, I4); the top just compares the strings for equality.
5. **Pure-docs tasks get a proportionally shrunk gate and dispatch.** **Pure docs = the task doc says so AND the diff contains only document-class deliverables** (contract documents, usecase maps, explanatory docs) — any production / test code or config change means it is not pure docs and the whole task reverts to the regular gate (items 1–4 all run); the classification declared in Phase 0 / the task doc, the gate verifies via `diff --stat` against the **deliverable file list**, never by after-the-fact judgment. Gate: no test numbers to recheck — the numbers item is replaced by path-level checking (every listed file exists, scope matches); **deliverable content quality does not enter the top's gate** (the content-judgment-sinks principle, see the 429 section). Dispatch shrinks in sync: the template's acceptance test / hash / gradle-numbers reporting items are replaced wholesale by "deliverable file list + per-file delivery" — no test to write means no circular-reasoning concern, the tier machinery (including spec-tdd's floor) does not apply; the docs are authored by level-1 (or a dispatched level-2), the compile item still runs to guard against smuggled code changes, hash / numbers items are naturally empty. The PHASE BOUNDARIES instruction is still carried — a pure-docs task may have zero nested dispatches; the heartbeat is covered by the "after each delivered file" trigger. Content **correctness** is self-attested by the producing level-1 against upstream sources and disclosed in the report; what consuming tasks' contract tests and the plan review guard is **wiring and coverage**, not the truthfulness of the document itself.

**What it does not do**: deep code review (sunk into level-1's audit / attack rounds; cross-task deep review is carried by the closing batch review — see the dedicated section), running the tests itself (level-1 already ran them; the XML is there), re-running the full suite (except when diagnosing a gate failure). The top doing subjective review is not diligence, it is waste: it lacks level-1's full context, its conclusions won't beat the sub-agent's audit rounds, and it burns the scarcest context. The top's value is **objectivity and continuity**, not depth.

**Eco mode's close step (after gate items 1–5, before commit)**: dispatch the per-card TOP final-audit dispatch; only converged findings (or escalated to the user) close the card (brief / checklist / findings bound in the Eco mode section); pure-docs tasks skip the final audit (keeping the shrunk gate).

## Number-recheck discipline

- **Rule: test numbers reported by a sub-agent are always rechecked against the JUnit XML, never taken on faith.** Twice in the field a verbal number was wrong: once 165 reported, XML said 163; once "+6 new tests (21+6=27)" reported, XML said 30.
- **The counting-unit trap** — one `@ParameterizedTest` method = N invocations, and JUnit XML's tests count invocations. The 30 case: actually +7 methods (6 `@Test` + 1 `@ParameterizedTest` running 3 sets) = +9 executed units — the reporter did mental math in methods; the behavior wasn't inconsistent, purely a counting slip. When the recheck disagrees, first ask: **is the report in methods or invocations?**
- **The XML coverage trap — every test run clobbers the previous round's XML.** When level-1 runs multiple test batches, only the last is recheckable afterward. The countermeasure is already in the dispatch template: **final verification = ONE gradle run covering all related test classes + per-class numbers** — that round's XML is exactly what the top rechecks.

## Mock-first contract development (the time dimension of tier choice)

When upstream dependencies are unreleased / unsettled:

1. **The first task builds the mock** (mock controller / server), fixing the contract; all subsequent tasks develop against the mock instead of idling in wait.
2. **The tier may drop during the mock-first phase (user's call).** Over-investing in verification for code against a mock before the contract settles is waste — when the contract changes, the deep tests get rewritten with it. Tiers are chosen not only by blast radius (the space dimension) but also by **this code's life stage** (the time dimension).
3. **Once the real dependency settles, schedule a contract-alignment task** — go back and compare real API vs mock contract, fix deviations, and pay back the deep tests deferred during the mock phase. A downgrade must be "defer + pay back", never "skip"; disclosed throughout.
4. **External open questions get a landing spot in the plan doc (kept distinct from the decisions section).** The decisions section records user rulings; questions awaiting third-party answers (upstream API behavior, another team's reply) get their own section **inside the authoritative plan doc** (living in scratch / conversation = did not happen), one line each: **question + the interim landing (which task uses what stopgap, where the single replacement point is) + where the answer converges when it arrives**. **Answer arrives → write back to the decisions section (numbering continued, source noted as external), strike the line as converged**, and the contract-alignment task digests it — the arriving answer has a definite convergence point and is not lost, and the alignment task has a ready-made digestion list (field record: STP2's G list — "real error-code values undecided → W6's classifier single-replacement point already built; when the answer arrives, change one place").

## Mid-run redirection (delivering a tier downgrade to a running sub-agent)

The user may at any moment downgrade the tier for time pressure — including mid-task:

- **Delivery (dual channel)** — while level-1 runs in the background, use SendMessage to push the change in (e.g. "downgrade to spec-tdd, converge to green and stop, report discloses the tier change") — most immediate for a wakeful agent; **simultaneously write `.spec-tdd/POLICY-<task>.md`** (level-1 re-reads it at every phase boundary, per the template's boundary instruction). Three reasons for the file channel: backlogged messages are **delayed, not lost** (field-measured: a wedged agent only gets them, in order, on its first waking round — a time-critical instruction arriving hours late = not delivered); a fresh continuation agent **cold-starts** with no message backlog to receive, only files to read; a policy left sitting in a message queue = not yet landed. The POLICY file overrides the template's TIER BAND, **downgrade-only** (restoring the deserved tier waits for the next task boundary); it lands in scratch, not in the task doc — task-doc edits are bundled with commits, and writing operational policy into the contract pollutes the rollback unit or trips the gate's file-scope check.
- **Asset preservation** — completed tests and implementation are not discarded; converge to green and stop.
- **Disclosure** — that task's report must record the tier change (when, what was downgraded, what unverified risk remains).
- Undeliverable (not a background dispatch) → takes effect at the next task boundary, disclosed the same way.
- **In-band downgrades** — a mid-run tier drop (e.g. coverage→spec-tdd) is handled the same way: delivered via SendMessage + POLICY file, else effective at the next task boundary, disclosed as above. Restoring the deserved tier happens only at the next task boundary (upgrades never ride the mid-run channel); the band ceiling is structural — "upgrading out of coverage" does not exist.
- **Time-pressure downgrades create re-test debt.** **Any runtime downgrade for time pressure — a mid-run tier drop (e.g. coverage→spec-tdd), or per-task SendMessage downgrades — is booked identically: tasks that passed below their deserved tier enter the re-test debt list** (recorded on the board; tasks whose stakes were already below the new ceiling and untouched by the downgrade are not — diluting the list = the list stops working), and disclosed in the phase report. Payback (re-test) is a formal entry, not optional: **when time allows, schedule it straight back into this phase's task table** (new task rows, numbering continued); still unpaid at phase close → the whole list goes into the phase report handed to the user. Without the booking, a lightweight first pass silently becomes permanent; without the handover, the booking does too. Pre-flight's tier-band ceiling is structural (pre-flight 3); capped-critical tasks (kept in-loop at coverage by the user's explicit call) go on the residual-risk list — their payback = pulling them out standalone, not double-booking. This is the phase-level version of mock-first's "defer + pay back, never skip" (field record: STP2's "W11–W14 all passed lightweight = re-test candidates").

## Half-finished-task resume (after a session break)

Session break / context corruption, task stopped mid-way:

1. **Inventory first, never rewrite** — `git status` + the existing diff against the task doc; judge which changes are legitimate half-done work by path-level comparison (content-level judgment sinks — see the principle in the 429 section).
2. **spec-defect check** — tests left by the interruption that contradict the task doc → **fix the tests, never bend production** (the spirit of I15: production contorted to accommodate a defective test = a failed run).
3. **Continuation brief** — when re-dispatching level-1 (hand over any ledger / scratch log the predecessor left) explicitly instruct: **keep existing legitimate changes, fill only the gaps, never rewrite**, and attach the inventory result (diff file list + scope mapping — which diffs belong to this task's scope, at path level).
4. The status section IS the recovery point — the in-flight task is directly visible (echoing A16's resume semantics: an in-flight row = re-verify, never blindly redo).

**API-quota interruption (429) — the agent died, the session lives; different from the session-loss case above:** after quota resets / key swap, **use SendMessage to resume the SAME agent** (full context preserved) — do not re-dispatch a fresh one from scratch. Inventory the breakpoint per step 1: acceptance test written, zero production changes = a clean RED breakpoint, zero-risk resume; production partially changed → first verify the acceptance test's I4 hash is untouched. If the dead one is the nested implementer, not level-1: once the orchestrator recovers, it **re-dispatches a continuation implementer to correct-and-complete on the predecessor's half-done work** (same "keep, fill gaps, never rewrite", sunk one level down). The resume message states the current situation (which files the working tree already has, which step it broke at) — never make the agent reconstruct its understanding.

**Soft-wedge and zombie-wait — the second and third breakpoint kinds; after watchdog diagnosis, run this procedure:**

1. **Zombie-wait: try revival first (the cheap path, skip the nudge).** Send evidence by SendMessage: "your child is dead (test-results frozen at X, build output not advancing, zero active processes); stop waiting and re-dispatch a continuation implementer" + a bounded grace (one check cycle, not waiting for a reply) — a living parent can save itself in place, keeping its full context and saving the cold start + re-inventory. The parent takes **action** (a new child dispatched / heartbeat boundary touch resumes) → re-arm; its **verbal report doesn't count** (self-report never resets the real-output clock); grace expired with no action → joint surgery.
2. **Soft-wedge: reset moment known** → schedule a reset+15 nudge (SendMessage wake + convergence instruction); waking grace ≈10–15 min (field-measured children before parent — an n=1 buffer, not a precise law). **Reset moment unknown** (pure soft-wedge, no 429 message in the session) → nudge immediately (costs nothing even if undeliverable) + one grace cycle; still frozen → joint surgery, or re-dispatch on a different pool per the dispatch discipline — never wait unbounded.
3. **Joint surgery (soft-wedge confirmed / zombie revival failed).** (a) **SendMessage before the kill** — at the moment of death the backlogged messages deliver (last words): free intel on its self-state understanding (possibly wrong, but diagnostically valuable — field-proven: the last words confirmed the wrong belief); (b) TaskStop the parent; (c) **orphan sweep**: find in-flight nested children from the agent list, stop them too or confirm they already ended (independent processes may still be writing the same tree — orphans collide with the new level-2); the sweep extends to **build process locks** (residual daemon lock files collide with the new agent's builds, especially on Windows); (d) re-dispatch a fresh continuation level-1 — **prefer a different pool that still satisfies the tier pin** (I19(a): a pool change must not lower the tier; none available → same pool, budget re-granted by remaining scope), brief per the continuation mode (inventory git status + task doc + acceptance tests; keep, fill gaps, never rewrite) + **read the POLICY file first** (the cold-start policy source); (e) mechanical completion is still the dispatched agent's job.
4. **Degraded closing (the last rung).** Only when re-dispatch is also unavailable (all pools dead / harness broken) → the closing mode degrades to "**the top personally runs the single merged verification run**" — its nature is a gate exception (the same shape as task-dag's wave-end union run: new information, no existing XML to recheck, evidence = that run's XML numbers), **NOT** authorization for the top to close the card (mechanical completion is still an agent's job — on this path there is usually no agent left to dispatch; the top only verifies the acceptability of existing output); disclosed in the report. (The description's "never running the tests itself" now runs with a known exception — per the task-dag precedent, a body-level handling, routing untouched.)
5. **Waking ≠ done.** The first waking round delivers **all** backlogged messages in order — including stale policies decided hours ago; the top immediately follows with a confirmation / rescind so stale instructions don't stay in effect. And waking only begins the digestion of the backlog (nested results, messages, convergence) — the final report is still some distance away.
6. **The frozen one is a nested child (parent alive)** → existing rule: stop that child, re-dispatch a continuation implementer, sunk one level down (TaskStop before re-dispatch — a presumed death is not a confirmed one).

**Post-first-429 dispatch discipline:** any agent in the session hits a 429 (the message names pool and reset moment) → subsequent dispatches **must not silently land in that pool**: a known **different-pool model satisfying the tier pin** may be named as an override (opt-in), otherwise pause dispatching until the named reset. Codified, never left to in-the-moment judgment — other pools working normally through the exhaustion window is field-proven.

**The main session shares the pool's fate (field record: the checkpoint fired on time, but the main session's turn hit the same pool's 429 — 0-second death, the one-shot wakeup consumed in place with no re-issue — scheduling reset+15 requires a successful turn, and 429 kills exactly successful turns).** The **first successful turn after the first 429** (from any source: a ladder far-fire landing / a manual user message / quota trickle) must do three things: (i) **record the 429 event, pool, reset moment, and freeze start into the board's in-flight row** — transcript error lines get eaten by compaction; the board is the existing file base for re-arming; (ii) **schedule the reset+15 insurance point** (the existing rule, its scheduling moment codified here); (iii) **disclose the freeze**: before reset the top cannot act; ladder far-fires and manual user messages are the only levers inside the window (a manual message did get through once — n=1, not guaranteed). **That turn collects before judging**: first digest the backlog accumulated during the freeze (task notifications, agent states, board reconciliation) — cards completed during the freeze present as "total freeze" shapes; check for closure before running the three-state judgment; a known freeze window is deducted from the output-age and budget readings (the freeze is the top's account, not the agent's — a mechanical over-budget kill here is a wrongful kill; field record W16: a different-pool agent started work healthily while the top was frozen; this configuration really exists).

**The legal path that doesn't wait for reset: re-dispatch a "continuation" agent (not a restart).** When the remaining work is small and waiting for quota reset isn't worth it (field record: 3.5 h), re-dispatch a fresh agent to close out on the predecessor's half-done work — keep-don't-rewrite brief + **pointers only, no content**: the predecessor's scratch log, the diff file list, the death-point description; **content-level judgment of the deliverables (reading full text to judge completeness / quality) always sinks, done by the continuation agent itself** — this principle is universal, 429 or session loss alike. **The third path is hard-banned: the top unilaterally finishing the work itself** — "it's only a little left", "it's just docs", "my session wasn't 429-hit" constitute no exception (field incident: a 429 death at the start of deliverable 2, the top began reading a 560-line contract document post-mortem, and was stopped by the user — every deliverable the top reads is irreversible context burn). The user explicitly demands the top close it personally → comply, disclosed in the phase report as degraded mode — **what's banned is the top deciding on its own, not the user's decision authority**. Inventory principle: the top looks only at objective cheap facts (git status / `diff --stat` / file paths mapped against task scope).

## Disclosure conventions

The following must be **explicitly listed** in sub-agent reports and re-checked by the top / user — never done silently:

- tier capped (e.g. insufficient spawn depth, capped-critical under the tier band's ceiling) or downgraded mid-run;
- literal doc deviations — DDL additive deltas, mock placement differing from the doc, naming / structure adjustments;
- locally decided rule details (small rules the doc doesn't pin and level-1 decided itself);
- adaptations of prior batches' tests (next section).

Principle: **the task doc is a contract. Deviating from the contract without disclosure = the contract is void** — the next task's sub-agent still understands the system per the old contract.

## The regression wall (test assets)

- Every task's acceptance tests are the next task's existing assets — the later in the phase, the thicker the wall. This is the task loop's compound interest.
- Later tasks adjusting prior tests for constructor / contract evolution is legitimate evolution, but: (1) **recorded per file** in the report with rationale; (2) **assertion semantics must not change** — only wiring may change (a new constructor parameter, a new contract field), never expected behavior. Changed semantics = a section of that wall fell; it must be re-walked as a new test through RED→GREEN.

## The closing batch review

An all-done task table ≠ straight to the report — closing has a fixed procedure: **dispatch one closing batch review first, then produce the phase report.** Rationale: the task doc's self-containment design means every level-1 is blind to the others; the cross-task dimensions are visible to no one along the whole chain (the top being hard-banned from deep review is correct — it lacks full context and burns scarce resources); this blind spot is covered by a one-shot fresh context, not by anyone "happening to look".

1. **Trigger.** The task table all done (including re-test debt rows scheduled back) → dispatch the closing review; the review converged and findings disposed → only then produce the phase report. The user explicitly skips it → comply, but list it in the phase report's residual risks — never silently omit.
2. **Who reviews, what (bounded, read-only).** A fresh-context **TOP** sub-agent (same shape as Phase 0's plan-review), looking at the whole phase's accumulated result in one pass: all tasks' commit ranges (first..last hash), task docs, the authoritative plan doc (status/decisions/external open questions), the disclosure list (assembled and handed over by the top — the reviewer does not re-read deliverables). Read-only: git reads + file reads; no code changes, no builds, no git writes.
3. **Four attack dimensions (visible only cross-task).** (a) cross-task inconsistency — one concept implemented in multiple shapes (money handling, error-handling style, naming); (b) duplicated logic never extracted — multiple similar copies across task boundaries, later fixed in one place and missed in another; (c) the accumulated effect of regression-wall adjustments — individually legal wiring changes that together thin the wall; (d) merged patterns in disclosures — several local rulings that together contradict the decisions section (each individually reasonable).
4. **Finding disposal (auto-enters the board).** Each finding numbered (F1, F2…) → **auto-open a new task-table row** (numbering continued, source noted "closing review F#"), running through the normal loop — tier machinery judges as usual, lightweight gate, per-task commit. A finding the top judges a non-defect must **not be silently dropped**: strike through in the table + a one-line rationale (same convention as decision records). Findings are defect debt, booked separately from re-test debt (the tier-downgrade ledger); never merged.
5. **Convergence bound (the I16 convention).** All fix rows done → **the SAME reviewer runs one convergence round**, scoped to the fix rows' diffs; unresolved findings remain → escalate to the user; no infinite loop. No findings → no extra round, straight to the report.
6. **It is additive, not a substitute.** Per-task lightweight gate and tier machinery unchanged — the closing review takes over no single-task verification (a consolidated view cannot catch holes inside one task); nor does it lift the top's deep-review ban — the review is a dispatch; the top only triages findings and strikes rows. The review dispatch hits 429 → the existing resume rules apply (SendMessage continues the same agent); after a confirmed soft-wedge, what TaskStop re-dispatches is a **fresh reviewer** — "the same reviewer runs one more round" is unavailable; that re-dispatch cost is disclosed in the report. The closing review is also under watchdog monitoring (read-only class: budget = the expected duration stated at dispatch; signal = heartbeat).
7. **Cost and disclosure.** +1 TOP dispatch per phase (a follow-up round only if findings exist, cap +1). Review rounds, findings count, fix rows opened, rows struck (with reasons) all go into the phase report.

## LSP / IDE diagnostics are not evidence

After sub-agents write files, LSP / jdtls often reports stale false errors — "method undefined", "cannot be resolved", even pointing at deleted scratch files. **Always defer to gradle compile / test results** (I19(f): the BUILD is the only oracle — IDE diagnostics are noise). No level wastes time chasing LSP errors.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Taking a blueprint directly as the authoritative plan doc and starting (no status section, non-self-contained task docs) | Phase 0 first: on entry judge whether the trio exists; missing → the breakdown bootstrap produces it, only then Pre-flight. |
| Splitting tasks verbally in the conversation and starting | A breakdown living only in the conversation = not broken down (the spirit of I17): after session compaction the trace base is gone and resume / rollback / write-back have nothing to stand on. Land the trio + self-contained task docs on disk. |
| Starting the breakdown without fresh-context review | Reviewer attacks coverage / omissions / order / self-containment / granularity + top sign-off (double consent) is half the bootstrap; the cost of a bad split is the whole phase; unresolved → escalate to the user. |
| The top personally deep-reviewing code, running the tests itself | Lightweight gate only: compile, `diff --stat`, XML number recheck. Deep review sinks into level-1's audit / attack rounds, cross-task deep review into the closing batch review; the top's context is the phase's scarcest resource. |
| level-1 has no Agent tool and implements itself (self-testing) | Hard ban — stop and report to the user; the fix is `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3` (set in the top's launch environment, not some Bash call's export). |
| Taking a sub-agent's verbal test numbers on faith | Read the JUnit XML and recheck per class (field-proven: 165 reported, actually 163; "21+6" reported, XML 30). |
| Treating a number mismatch as behavioral anomaly | First ask the counting unit: `@ParameterizedTest` 1 method = N invocations, XML counts invocations; only after unit conversion still mismatching is it an anomaly. |
| level-1 runs multiple test batches and earlier XML is clobbered, unrecheckable | The dispatch template mandates: final verification = one run covering all related test classes + per-class numbers. |
| `git add -A` / `git add .` to take the commit | List file names explicitly — the working directory always contains `.spec-tdd/` etc. untracked scratch that would be swallowed into the commit. |
| The top committing at task boundaries without asking | Pre-flight asks once for session commit authorization; unauthorized → pause at the boundary, hand the file manifest to the user to commit manually, record the reported hash in the status row. |
| A sub-agent committing / stashing / checking out itself | git writes banned at every level; commits are the top's exclusive duty (task boundary = commit boundary = rollback unit). |
| User-ruled decisions left only in the conversation | Write back immediately to the authoritative doc's decisions section (numbering continued) + the relevant task doc (old plan struck through for the record). Conversations get cleared / compacted — not written back = did not happen. |
| After a session break, rewriting the half-finished work wholesale | Continuation mode: inventory existing diff vs task doc → spec-defect check (test contradicts doc → fix the test) → keep legitimate changes, fill only the gaps. 429 break (agent dead, session alive): SendMessage resumes the same agent, or immediately re-dispatch a continuation agent (not a restart); the dead one is the implementer → re-dispatch a continuation implementer, never wipe and redo. |
| A 429-dead agent's remaining work is small, the top "helpfully" finishes it itself | Not an option. Two legal paths: wait for reset and SendMessage-resume the same agent, or immediately re-dispatch a continuation agent (not a restart). The top's inventory stops at objective facts (status / `diff --stat` / path mapping); deliverable content judgment is the continuation agent's job. The user explicitly demands personal closure → comply, disclosed as degraded mode. |
| Forcing the heaviest tier "for safety" in the mock-first phase | The time dimension: deep tests before the contract settles are waste (a contract change rewrites them all). The user's call may downgrade; once the real API settles, a contract-alignment task pays it back. Downgrade = defer + pay back, never skip. |
| A long task list left to escalate's per-task self-judgment, several tasks all going full adversarial, the phase eaten by attack rounds | The tier band's ceiling is structural = coverage (pre-flight 3, not an ask); critical units take the escape hatch (Phase 0 sniff pre-pull / routing-point STOP and report), never silently coverage; kept in-loop by the user's explicit call → disclosure + residual-risk list. |
| Assuming in-loop lite is unavailable and forcing small cards onto spec-tdd (the two-context tax) | The tier band includes lite: small cards run the lite machinery (solo implementation + a **mandatory** fresh-context review dispatch), tier disclosed in the report — the v1.18.1 lite ban was reversed by v1.20.0 (loop economics: small cards don't pay the two-context tax). |
| Wanting a mid-run downgrade and just killing the running sub-agent to restart | Deliver the change by SendMessage; completed assets preserved; converge to green and stop, disclosed in the report. |
| A later task casually rewriting prior batches' tests on the way past | Regression-wall rules: only wiring adjustments allowed (forced by contract evolution), recorded per file; changed assertion semantics = a new test, re-walk RED→GREEN. |
| Table all-done goes straight to the phase report without the closing batch review | Closing procedure: all-done (including payback rows) → closing review → findings enter the board / get struck → report. The cross-task blind spot (the price of self-containment) is visible to exactly this one gate along the whole chain. |
| Treating the closing review as a substitute for per-task deep review ("it's backstopped, downgrading tiers is fine now") | Additive, not a substitute: a consolidated view cannot catch holes inside one task; tier machinery and the lightweight gate unchanged; the review takes over no single-task verification. |
| Closing-review findings silently dropped, or only listed in the phase report | Into a table row (the convergence point: on the board = will be executed) or struck through with a reason; report-only = no convergence point (the spirit of I17). |
| Allowing adversarial in-loop "for safety" | Structurally not carried: hours-level depth × per-task multiplication contradicts the anti-idle economics; critical units pull out of the loop and run standalone (the escape hatch, pre-flight 3) — mid-run demands pull out too; in-loop unlocking does not exist. |
| Zero monitoring while in-flight, idling discovered by hand | Anti-idle watchdog: armed at dispatch (delivery class registered), output-age + budget axes, three-state judgment bound to clocks. Field record: three modes stacked, one card 6 h, 5 h zero output. |
| Three-state judgment reading only instantaneous signals (zombie misjudged as a healthy in-phase wait) | The zombie conjunct includes "the heartbeat-declared wait overdue" — instantaneous shapes can't distinguish zombie from waiting; the clock is the only discriminator; total freeze keeps the ~90-min long tolerance (long reasoning vs soft-wedge indistinguishable). |
| Applying the output-type formula to a read-only reviewer (guaranteed misjudgment) | Register the delivery class at arming: read-only-type real output = heartbeat / scratch growth, budget = the expected duration stated at dispatch — not the tree diff. |
| Standing down because the agent reports "still running / all fine" | Self-reports never reset the real-output clock (field-proven: the zombie parent's "implementer running" was wrong); only actions count (a new child dispatched / boundary touch / output flowing). |
| Still "waiting a bit longer" past the wall-clock budget; or hard-killing while output flows | Stalled overrun → terminate and re-dispatch immediately; flowing overrun → one-time budget reset, disclosed (once only); continuation re-dispatch re-budgets by remaining scope; re-dispatch cap 2, beyond that escalate to the user. |
| Nested dispatch as a blocking call (the parent wedges itself) | Background mode in writing: mid-run redirection, POLICY re-read, the watchdog, and responsiveness all depend on the parent keeping tool rounds; no background nested support → disclose the degradation (the top's budget backstops). |
| Treating an overtime child as dead and re-dispatching directly | TaskStop the old child first (presumed ≠ confirmed; two implementers banned from the same tree) + clear build process locks, only then re-dispatch the continuation. |
| Mid-run changes via SendMessage only | Dual channel: backlogged messages deliver late (a time-critical instruction arriving late = never arrived); a fresh continuation agent cold-starts with no messages to receive — write the POLICY file too; it overrides the band, downgrade-only. |
| Writing POLICY into the head of the task doc | Task-doc edits bundle with commits — operational policy entering the contract pollutes the rollback unit or leaves dirty changes that trip the gate's file-scope check; POLICY lands in scratch. |
| Killing the parent directly on zombie diagnosis | Revival attempt first with evidence (child-death evidence + stop-waiting order) + a bounded grace — a living parent can save itself in place and keep its context; only on failure the joint surgery (SendMessage before the kill for last words). |
| Re-dispatching directly after TaskStop kills a wedged/zombie parent | Orphan sweep first (in-flight nested children stopped or confirmed ended) + clear build process locks (residual daemons collide with the new build); recovery re-dispatch prefers a different pool **that satisfies the tier pin**. |
| Post-first-429 dispatches still silently landing in the same pool | Dispatch discipline: name a different-pool model satisfying the tier pin (opt-in) or pause until the named reset; codified, never in-the-moment judgment. |
| Chasing LSP / jdtls "method undefined" false errors | The BUILD is the only oracle (I19(f)); defer to gradle compile / test. |
| Tier downgrade / doc deviation / local rulings undisclosed | Disclosure conventions: all explicitly listed, re-checked by the top / user — the doc is a contract; undisclosed deviation voids it. |
| A task doc saying "DDL same as the previous case" / "see the requirements doc" | Self-containment: the full contract given in full at once; the dispatch prompt restores path shorthands to absolute paths. |
| eco on, an Agent call not naming MID (silently inheriting the session model) | eco's MODEL PIN: level-1 and all nested name MID — omission breaks in both directions (a TOP bill comes back, or the shape silently runs wrong). |
| Under eco, committing once the gate passes without waiting for the per-card final audit | Close order = gate → final audit converged → commit; commit-before-audit = all-MID with no TOP judgment point — a downgrade, not a saving. |

## Red Flags — STOP

- The loop is running but the status section / task docs don't exist → STOP, back to Phase 0 to complete (existing work inventoried from the diff back into status rows) before continuing.
- The top starts reading sub-agent deliverables verbatim in full (autopsy-style content judgment; XML number recheck and path-level mapping excepted) → STOP — content judgment is a sub-agent's job (audit rounds / continuation dispatches).
- level-1 reports "I implemented it myself" (self-testing) → run void, re-dispatch.
- level-1 reports having no Agent tool → stop, report to the user to set spawn depth; never let it self-test in place.
- XML numbers disagree with the report (after counting-unit conversion) → demand an explanation or a re-run; no match, no commit.
- `git diff --stat` shows changes outside the reported list → no commit before inventory and an explanation.
- Any level's sub-agent touched git writes → first confirm the tree is undamaged, restate the discipline.
- The acceptance test is not bit-identical before vs after dispatch → I4 FAIL, route per the tier's TEST bucket even if the re-run is GREEN.
- Continuation inventory finds pre-break production changes made to accommodate a test contradicting the doc → fix the test, restore the bent production code.
- A tier was downgraded, the doc deviated, and the report doesn't say so → treat as unverified; demand the disclosure before re-review.
- A closing-review finding neither entered the table nor got struck through with a reason → STOP and complete the procedure — on the board = convergence point; booked but never looked at = not booked.
- The top extending a liveness check into content judgment (starting to read a wedged agent's output to judge "did it do it right") → STOP — monitoring stops at objective facts (mtime / git status / processes / status rows); after diagnosis, run the procedure, not an autopsy.
- A card stalled past its wall-clock budget and still "waiting a bit longer" → STOP — the budget is a hard cap; terminate and re-dispatch; re-dispatch already at the cap of 2 → escalate to the user.
- Level-1's routing finds stakes above coverage and quietly starts work → STOP and re-dispatch — report first, the top pulls it out of the loop (standalone); an in-loop critical downgrade needs the user's explicit call.
- Eco mode, no per-card final-audit notification on record before commit (or the audit dispatch dead / silent) → STOP — a dead audit is not an approved audit; after one fresh re-dispatch still nothing → report to the user.
