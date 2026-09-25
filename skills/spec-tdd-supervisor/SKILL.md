---
name: spec-tdd-supervisor
description: Use when the user says "spec-tdd-supervisor", or wants ONE settled unit implemented with the WHOLE spec-tdd machinery delegated to a subagent while the final comprehensive review itself is a TOP-tier read-only audit dispatch — supervisor mode / full delegation of a single unit; every machinery dispatch (level-1 orchestrator, nested implementer, encoding audit, lite fresh review) is pinned to the MID tier as a recorded user opt-in, and the session's own tier is never a premise of the shape (any-tier session; no upgrade ask — the deep review runs in the TOP-pinned dispatch, the session keeps the objective gate + brief + arbitration). NOT for multi-task phases (spec-tdd-task-loop / -task-dag), NOT for machinery run in-session (spec-tdd-escalate), NOT for fuzzy requirements (grill front-ends). Triggers on supervisor mode, full delegation, delegate the whole run, all-MID run, top reviews only, main session does only the final review, mid model handles everything.
---

# spec-tdd-supervisor

**REQUIRED BACKGROUND:** Understand the `spec-tdd` family first — the front-ends (`grill-spec-tdd`, `spec-tdd-escalate`), the tiers (`spec-tdd-lite` / `spec-tdd` / `spec-tdd-coverage` / `spec-tdd-adversarial`), and [PROTOCOL.md](../PROTOCOL.md) (I1–I21). This skill adds no new invariant and relaxes none: the tier machinery sinks to level-1 unchanged; what this file defines is the run **shape** layered on the family's outside — who sits at which layer, where judgment tokens are spent, and two recorded opt-ins (all-MID deviating from I19(a); the final review outsourced to a TOP auditor with the I21 ask retired — the session tier is no longer a premise of the shape). The outer drivers have three **parallel peers**: `spec-tdd-task-loop` (multi-task serial), `spec-tdd-task-dag` (multi-task parallel DAG), and this skill (single-unit full delegation) — the three never reference or dispatch each other: loop / dag level-1 runs the escalate machinery and never dispatches a sub-agent executing this skill; this skill likewise doesn't depend on their bodies (the monitoring and recovery machinery is self-contained in this file).

## Overview

ONE settled unit, one full delegation. The main session (supervisor) sinks the whole escalate machinery — sniff, tier pick, acceptance test (RED), encoding-audit dispatch, nested implementer dispatch, personal verification — **in one shot** into a MID level-1 subagent; at close it does only three things itself: **run the objective items personally, outsource the final review, arbitrate and relay findings**. The economics: machinery tokens all land in a disposable MID context; TOP judgment tokens are spent inside one TOP-pinned final-auditor dispatch — **the session's own tier is irrelevant from start to finish** (any tier of session can run it; the `/model` upgrade dance disappears), and the deep review's reading load lands in a disposable auditor context instead of pouring into the main session.

Contrast with task-loop (the two converge to the same deep-review shape): task-loop's closing batch review is a dispatch, and this skill's final review is a dispatch too — **the deep review is the reason this skill exists**; the difference is what the dispatch compensates for: task-loop compensates the cross-task perspective, this skill compensates the all-MID machinery's single TOP judgment point (the encoding-fidelity re-read is its fixed first item). Outsourcing buys two things no in-session shape can: **fresh-context independence** (the top is the requirement-doc author and the entry router — a stakeholder; the family's own thesis: a designer verifying their own design with the same assumptions they built it under) and **the disappearance of the decline hole** (in the old shape a non-top session answering Continue became MID self-review + disclosure — after outsourcing, the deep review is pinned TOP; a dispatch's tier cannot be declined).

Two recorded opt-ins (the shape's known costs; they hold the moment the user invokes this skill, and the final report must disclose them):

1. **All MID (an explicit deviation from I19(a)).** level-1, the nested implementer, the encoding audit, and the lite fresh review run **all MID** — the run's only TOP judgment point is the final review. The cost, recorded honestly: a weak test first drives a full implementation and is only caught at the final review; the fix rides a findings re-dispatch (more expensive than I19(a)'s pre-implementation interception). The compensation control: the final review's first deep-check item is fixed as the **acceptance-test encoding-fidelity re-read** — the original TOP encoding audit's duty is taken over by the final review (the auditor dispatch); it does not vanish because a dispatch was saved.
2. **The final review is outsourced to a TOP auditor; the I21 ask is retired (its second repositioning).** The deep review becomes a TOP-pinned dispatch, and **the session tier is no longer a premise of the shape** — there is no judgment-dense act left in-session: the top's remaining duties are either mechanical (running the objective items personally; the brief as a fixed checklist of doc paths — I19(c), no summaries, no pre-digestion) or user-owned (findings arbitration **default-adopt**; a rejection must carry the evidence the auditor lacked and surface to the user; ambiguities depending on grilling intent always go up — I12). Consent is invocation-based (same source as opt-in 1): the user invoking this skill consents to the review running in a TOP dispatch rather than in the session. Known cost: the auditor sees only persisted docs, not the grilling conversation — intent must already live in the doc (I17's standing claim; a doc that doesn't carry it is itself a finding), and the top manages one more resumable background child. Degradation path: at review time dispatching is impossible (Agent tool broken) → fall back to an in-session final review, **the I21 ask revives at that moment** (asked once), disclosed. **It is a convergence, not a relaxation**: the old shape's weakest legal configuration (non-top decline → MID session self-review) does not exist in the new shape.

| Layer | Who | Does | Forbidden |
|---|---|---|---|
| top-level supervisor (main session, **any tier** — this shape has no session-tier premise) | entry routing, the one-shot dispatch, report relaying, **running the objective items personally**, **the outsourced final-audit dispatch (brief = fixed checklist + doc paths)**, findings arbitration (default-adopt, objections escalated), **listing the commit manifest for the user (no auto-commit)** | running the machinery (writing tests / dispatching implementers / mid-run verification), **in-session deep review (absorbing the review — the price of saving one dispatch is the judgment tier falling back into the session)**, silently overruling the TOP auditor, fixing findings by hand, **git writes (incl. commit — unless the user explicitly asks)** |
| level-1 sub-agent (**MID**) | the unit's spec-tdd orchestrator (runs the escalate machinery): sniff, tier pick, acceptance test (RED), encoding-audit dispatch, level-2 dispatch, personal verification (re-run / hash / tier-required evidence) | git writes, routing out of band (above-coverage → STOP and report), stopping to wait for the user (unreachable — the report IS the ask) |
| level-2 implementer (**MID**) | implement to green + its own unit tests | touching the acceptance test (hash-locked), git writes |
| final-audit auditor (**TOP**, read-only) | the four deep-check items (checklist in final review 2) + the post-fix **delta re-check** (the SAME auditor — the adoption check needs memory, I16) | editing any file, re-running compiles (that's the session's machinery), re-litigating user-owned decisions (I12) |

**Why self-testing is banned (one agent writing code + tests + judging itself): circular reasoning** — the implementer's blind spots enter both the code and the test simultaneously; green becomes self-fulfilling. The lite route's solo mode is the entry tier's known trade; the compensation = a mandatory fresh-context review dispatch; **if level-1 cannot dispatch nested dispatches (lite's review dispatch counts too), the only legal action is to stop and report — never degrade into unreviewed self-testing.**

## When to Use

- ONE settled unit (requirement on file, decisions converged) where you want the main session's judgment tokens spent only on arbitration and relaying — the deep review outsourced to a TOP auditor, no session-tier premise.
- You accept the all-MID cost: machinery quality is guaranteed by the tier machinery's own structural controls (agent boundary, hashes, XML recheck) + the final review, not by TOP's mid-run judgment.
- The main session still has much else to do in this conversation — context should remain in stock after the run.

**When NOT to use — route elsewhere:**
- Multi-task phase → `spec-tdd-task-loop` (serial) / `spec-tdd-task-dag` (parallel). Under many tasks the top's context is the scarce resource; sinking the deep review contradicts this skill's shape.
- Multi-unit batch (bug list / a feature in slices) → `spec-tdd`'s multi-unit run (main session runs it) — this skill's one-shot dispatch shape doesn't carry multiple units (the template's band carve-out is the second interception; entry routing blocks first).
- One very small unit, a session you'll clear right after → `spec-tdd-lite` (in-session, 1 review dispatch). The lite-vs-supervisor fork: does the session have other things to do afterward — yes → supervisor (protect the context); no → lite.
- Pure-docs deliverable (no production/test code to test) → the tier machinery has no object; don't enter this skill; dispatch a docs-writing task directly or write by hand.
- A unit against an unsettled upstream dependency, developed against a mock → strictly speaking not settled (the contract isn't fixed); go through grill to converge the contract first. The user explicitly says run it against the mock: verification depth may drop (user's call, disclosed, paid back once the real dependency settles — the unit version of mock-first), not the default.
- Requirement fuzzy → `grill-spec-tdd`; fuzzy AND blast-radius-critical → `adversarial-grill-spec-tdd`. Grilled and the user wants the full-delegation shape → then this skill.
- Machinery to be run personally in the main session (judgment in the top context throughout, weak tests intercepted before implementation) → `/spec-tdd-escalate`. The choice between the two is **who pays the judgment tokens**: escalate = machinery TOP; supervisor = machinery MID + a TOP final-audit dispatch (any-tier session can run it).
- Session cannot dispatch sub-agents (no Agent tool / insufficient spawn depth, unfixable) → `/spec-tdd-escalate` in-session, disclosed degradation.
- Exploratory / throwaway code → no skill needed.

## Pre-flight (main session)

1. **Entry routing.** Walk the When/When-NOT above item by item; proceed only if this skill is the right door.
2. **Session tier not checked, not recorded.** This shape has no session-tier premise (opt-in 2): the deep review lives in the TOP dispatch, not in the session.
3. **Dispatch capability check.** The main session needs the Agent tool; level-1 must dispatch level-2 → **`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3`** set in the top's launch environment (the settings env block or the launching shell; an export inside some Bash call cannot affect spawning). Unfixable → degrade: run `/spec-tdd-escalate` in-session instead, disclosed in the report.
4. **Commit mode (the difference from loop/dag — no auto-commit).** Loop/dag's task boundary = commit boundary, landed by the top automatically once authorized; this skill's single unit has exactly one commit, **by default executed manually by the user**: after the final review passes, the top lists the deliverable file manifest (including the written-back requirement doc), the user commits themselves and reports the hash, and the top records it in the final report and RUN-STATE. **Zero git writes across the whole chain** — neither the top nor any sub-agent touches git (read-only git remains fine). The user explicitly asks the top to commit on their behalf → comply, recorded as a disclosed mode (the user's decision authority is not lost by this clause).
5. **Requirement on file confirmed (I17).** The settled conclusion must already be a doc (requirement verbatim + decisions); existing only in the conversation = not on file → land it first, then start (planning never sinks — the spirit of I19(a), top-authored). Handoff uses the doc path (I19(c)), never a full-text paste.

## The dispatch (one-shot, background mode)

Dispatch level-1 with the template below (**background mode** — a blocking call makes the top unreachable and unmonitorable). **The Agent call's model parameter must explicitly name the MID tier** (harness-relative, e.g. sonnet) — omission = silently inheriting the session model; if the session is TOP, the whole MID economy collapses on the spot (this skill's version of I19(a)'s name-the-model rule: what gets named here is MID). In the template, `{family root}` and doc-path shorthands are always restored to absolute paths (the sub-agent's cwd cannot be relied on; the template's **SCRATCH ROOT** field gets this run's absolute scratch root = repo root); `{unit}` is a kebab-case unit name the top picks (e.g. `payment-retry`), used consistently throughout the run.

At dispatch time the top writes `.spec-tdd/<unit>/RUN-STATE.md`: unit name, requirement doc path, dispatch moment, expected duration (estimated by unit size — tier still unknown here; aligned to the tier budget once level-1 routes), commit mode (default manual; recorded when the user explicitly requests a proxy commit). **This is this skill's re-arm base**: re-arming after a session break, continuation re-dispatch, and freeze accounting all take it as the authority (this skill has no task boundaries and no board — this one page is the state carrier).

### Level-1 dispatch template

```
ROLE: You are the spec-tdd orchestrator for ONE settled unit — the
supervisor run-shape: the WHOLE machinery is delegated to you; the
top-level session will relay a TOP-tier final-audit dispatch at close
(it does not review you in-session). Run the
spec-tdd-escalate machinery for THIS unit only: sniff the requirement,
pick the tier by stakes, write the acceptance test (RED, RED-purity
checked), dispatch the encoding audit, dispatch a NESTED implementer
via the Agent tool, and verify it yourself (re-run GREEN, hash check,
tier-required verification). Invoke the /spec-tdd-escalate skill BY
NAME if it is available in your runtime. If it is not, do NOT improvise
a lighter version from this prompt — read FAMILY FILES below and run
that machinery exactly.

MODEL PIN (recorded user opt-in — supervisor shape, a disclosed
deviation from I19(a) made by the user's explicit skill choice): you
run the MID tier, and EVERY dispatch you make — encoding audit, fresh
reviewer (lite route), implementer — is ALSO the MID tier. Name the MID
tier explicitly in every Agent call; never let a dispatch silently
inherit the session model.

ORCHESTRATOR TIER CHECK — PRE-RESOLVED: treat the I21 pre-flight of
escalate AND of the chosen tier as already answered-decline. No ask
was surfaced to any user, and none was needed: the user's explicit
invocation of the supervisor skill-shape IS the recorded decline
(the machinery runs MID on purpose; a TOP-tier final-audit DISPATCH
backstops judgment — not the session, whose own tier is irrelevant
in this shape). Do NOT stop to ask about upgrading;
carry "I21 decline recorded (supervisor all-MID opt-in, at
invocation)" into your report disclosures.

No self-testing OUTSIDE the lite tier. Same-context test+implementation
is circular reasoning: the implementer's blind spots enter both the
code and the test, and green becomes self-fulfilling — every tier above
lite dispatches a separate implementer, and lite (the entry tier for
small non-critical units) compensates with a MANDATORY fresh-context
review dispatch over its test+implementation. If your escalate routing
selects lite, run the lite machinery exactly, including that review
dispatch. If you have no Agent tool, STOP and report that fact — do
NOT fall back to implementing yourself (the review dispatch needs the
tool too).

REQUIREMENT DOC: {absolute path} — READ IT FIRST; it is settled
(requirement verbatim + decisions). Path shorthand maps to:
{abbreviation → absolute path}.

SCRATCH ROOT: {absolute path} — paste-verbatim anchor for EVERY
`.spec-tdd/` path in this prompt (repo root).

USER-FLAGGED GAPS: {none | gap list + the user's recorded
"settled, route" call}. If present, the requirement only LOOKS
settled: these decision gaps were surfaced by the sniff and the
user chose to route anyway — let Phase 1 see them (I20's handoff
shape).

FAMILY FILES (if the skill is not invocable in your runtime, READ these
from disk and follow them — the machinery lives there, not in this
prompt):
{family root}/skills/spec-tdd-escalate/SKILL.md (the routing you run),
{family root}/skills/PROTOCOL.md (invariants I1–I21), and the chosen
tier's {family root}/skills/<tier-name>/SKILL.md.

DOC EDITS: report proposed requirement-doc edits; do not edit the doc
yourself — the top-level session owns decision writeback.

SCOPE: this unit only. Existing acceptance tests this unit touches
are the regression wall: adapt one only where this unit's contract
evolution forces it — one file at a time, assertion SEMANTICS
unchanged, each adaptation listed in your report with its rationale.

GIT: NO git write operations (add/commit/stash/checkout/restore/...)
at ANY level of this run — you, your nested children, and the
top-level session alike. The USER commits manually at close, from
the file list the top delivers. Read-only git
(status/diff/hash-object) is fine.

TIER BAND: lite … coverage — structural. Your escalate routing runs
inside it, including lite (small
non-critical units: solo author-implementer plus ONE fresh-context
review dispatch; disclose the tier used), with ONE carve-out:
escalate's MULTI-UNIT route (a bug list, a feature split into
slices) does not fit this skill's single-dispatch shape — a
requirement that is actually several units: STOP and report BEFORE
anything; the top exits to a spec-tdd multi-unit run in-session.
The CEILING is structural: adversarial is not carried in this
run-shape either (hours-level attack depth contradicts the
MID-delegation economics). A unit whose stakes would route above
coverage: STOP and report BEFORE implementing — the top's default
is to EXIT this skill and run spec-tdd-adversarial standalone
(re-routing at coverage here would be an unconsented downgrade; on
exit, the requirement doc plus any already-written test hand over
as REFERENCE INPUTS — the standalone run executes its own Phase 1,
treating a MID-written test as a draft to re-derive or harden, not
an intake).

ASKS YOU CANNOT REACH (escalate's routing-hygiene asks, dispatched):
the fuzziness-sniff ask (gaps in the "settled" doc) and the top-tier
adversarial confirmation have no user to reach. STOP and report — the
report IS the ask; the top relays it to the user. Do NOT guess, do NOT
silently absorb gaps, do NOT invoke adversarial on your own say-so.

PHASE BOUNDARIES (before/after each nested dispatch, when ENTERING a
wait on a nested dispatch, after each completed long tool run, after
each delivered file): 1) touch `.spec-tdd/<unit>/HEARTBEAT` (create the
directory if missing; touch or an equivalent write) — when the touch
coincides with entering a wait, write into the file: "waiting:
<child-id> expected-done <time>"; 2) re-read
`.spec-tdd/POLICY-<unit>.md` — ABSENT means ONLY a confirmed
file-not-found (e.g. `test -f` fails); any OTHER read error is a STOP,
not "no policy"; a PRESENT file overrides TIER BAND above,
DOWNGRADE-ONLY; 3) PATH RULE (every `.spec-tdd/` path in this prompt —
the touch, the POLICY re-read, every scratch write, incl. RETURN's logs
and REPORT.md): form it by prefixing SCRATCH ROOT from your brief,
joined with a `/`, PASTED VERBATIM — never retype it, never resolve it
against your own cwd, never hand-compose any other absolute form;
mkdir -p plus output-redirect makes a typo'd absolute path silently
succeed, materializing a parallel tree whose heartbeat the watchdog
never sees (2026-09-18 W22 incident). Before the first such write:
`git rev-parse --show-toplevel` must equal SCRATCH ROOT — a mismatch is
a STOP-and-report, never a best-effort guess. Carry SCRATCH ROOT and
this PATH RULE verbatim into every nested brief you compose
(implementer, reviewer, attacker): their templates' `.spec-tdd/`
shorthand is anchored by YOUR pasted root, never their own cwd.

NESTED DISPATCHES (any nested child — your implementer on tiers above
lite; your fresh-context reviewer on lite): dispatch each nested child
in BACKGROUND mode — a blocking Agent call makes you unreachable and
unmonitorable, and its never returning is NOT evidence the child lives.
Record the expected duration with each dispatch (floor it at the known
build cost of the affected files); on overtime with no fresh output from
the child (build outputs, task scratch), treat the child as dead:
TaskStop it first (a presumed death is not a confirmed one — two agents
must never write the same tree; clear build-process locks, e.g. stale
daemons, before re-dispatching), then re-dispatch: a CONTINUATION
implementer on its partial work; for a dead lite reviewer, a FRESH
reviewer — its judgment depends on fresh context, nothing is inherited.
Harness without background nested dispatch: disclose the degradation.

VERIFICATION REPORTING (your numbers will be independently rechecked):
  - FINAL verification = ONE gradle run covering ALL related test
    classes — each run CLOBBERS the previous JUnit XML, so only the
    last run survives for recheck.
  - Report per-class numbers read from build/test-results/test/*.xml
    (or your build system's equivalents), and state whether counts
    are @Test METHODS or EXECUTED INVOCATIONS
    (@ParameterizedTest: 1 method = N invocations).

RETURN (also WRITE the full report to .spec-tdd/<unit>/REPORT.md —
the resume substrate; a broken session recovers the numbers and
hashes from it): 1) one status line per command (command + pass/fail
counts), full logs to scratch files under .spec-tdd/ (never
committed; hand paths)  2) per-class numbers  3) created/modified
file list (absolute paths)  4) the acceptance test's dispatch-time
and post-run hashes (the bit-identical pair; on the lite route,
state "solo re-RED discipline applies — no hash pair")  5)
prior-test adaptations with per-file rationale (per SCOPE)  6)
disclosures: tier actually used (+ any mid-run downgrade or band
cap; the all-MID opt-in and the I21 recorded decline), deviations
from the requirement doc (DDL deltas, naming/structure), locally
decided rule details, and your proposed requirement-doc edits for
the top's writeback.
```

## In-flight monitoring (single-dispatch scope — self-contained here, no other skill referenced)

Stacked failure modes can burn a whole afternoon: hard-fail (429 terminates directly, with a notification), soft-wedge (an inference backoff-retry loop: perpetually running, zero notifications, transcript frozen), zombie-wait (the nested child died silently while the parent healthily waits on a never-returning Agent call — **an Agent call not returning ≠ the child alive**). **Zero-output duration is the first-class metric**; this is process monitoring, not a verification act — every signal is an objective fact, no content judgment. This section's machinery also covers the **final-audit auditor dispatch** (the other background child in flight at the close stage): a read-only deep review gets a coarse minutes-to-tens-of-minutes cap and the same three-state judgment; at most ONE fresh re-dispatch on death (fresh — the auditor's judgment depends on fresh context, nothing inherited; when that breaks the findings loop's adoption check, the new auditor re-reads everything from `FINAL-AUDIT.md`, disclosed).

1. **Periodic checks (checkpoint ladder, the whole ladder scheduled at dispatch).** One one-shot wakeup per ~15 min (example default, user-adjustable), **the ladder scheduled in advance** rather than a single-shot chain: fine rungs out to the budget horizon + 2–3 coarse far-fires (e.g. +90 min / +3 h / +5 h, illustrative). **The main session shares the pool's fate** — inside a 429 window even the top's turns die, the single-shot checkpoint's re-arm premise (if it fires I can schedule another) collapses on the spot, and the far-fires are the only coverage depending on no successful turn. Every rung's prompt is self-contained and self-retiring: carries its own RUN-STATE path + in-flight interpretation + "no in-flight → clear leftover checkpoints and stand down" (guards against stray far-fires after close, and survives context compaction). A wakeup landing inside the freeze window = 0-second death, free (rejected requests burn no tokens); landing after quota recovers = the top automatically regains control.

2. **What each rung checks (objective signals, read-only throughout).** (a) `.spec-tdd/<unit>/HEARTBEAT`'s mtime and content (incl. any "waiting: <child> expected-done <time>" declaration); (b) growth of `.spec-tdd/<unit>/` background scratch (REPORT.md, logs); (c) build output directory mtime (test-results rolling = advancing; process presence is only corroborating — an idle daemon lives for hours); (d) `git status` / `diff --stat` (real output). **An agent's self-reported state NEVER resets the real-output clock** ("implementer running" is not health evidence).

3. **Three-state judgment (bound to clocks, separate tolerances).** (a) **legitimate work** — real output flowing or the build advancing → re-arm (a successfully landed checkpoint turn tops the ladder back up); (b) **zombie-wait** — diagnosed only on the four-condition conjunct: signs of activity (fresh heartbeat or background files appearing), zero real output, build not advancing, the heartbeat-declared wait overdue. **Instantaneous signals cannot distinguish zombie from a healthy in-phase wait — the overdue clock is the only discriminator.** High-confidence death → the 15-min fast knife, but **try revival first** (the cheap path): an evidence-carrying SendMessage (objective evidence the child is dead + a stop-waiting order) + a bounded grace — a living parent can save itself in place and keep its context; only actions count as revival (a new child dispatched / a heartbeat boundary touch), never a verbal report. Revival failed → **joint surgery**: SendMessage before the kill for last words (backlog delivers at the moment of death — free self-state intel) → TaskStop → orphan sweep (in-flight nested children stopped or confirmed ended — independent processes may still write the same tree; the sweep extends to build process locks; residual Windows daemon locks collide with new builds) → re-dispatch a fresh continuation level-1 (keep-don't-rewrite, read the POLICY file first, prefer a different pool that still satisfies the **MID** pin); (c) **total freeze** — heartbeat / background files / build all frozen: an ambiguous state (a single long reasoning request vs soft-wedge is externally indistinguishable) → **long tolerance ~90 min** (example default, user-adjustable), the budget backstops.

4. **Soft-wedge recovery.** Reset moment known (any 429 message in the session names it) → schedule a reset+15 nudge (SendMessage wake + convergence instruction); waking grace ≈10–15 min (children before the parent, an n=1 buffer); reset moment unknown → nudge immediately (costs nothing even if undeliverable) + one grace cycle; still frozen → the joint surgery of 3(c), **never an unbounded wait**. **Waking ≠ done**: the first waking round delivers the entire backlog in order (including hours-old policy — the top immediately follows with a confirmation / rescind), and the final report is still some distance away.

5. **Budget = hard cap (three rules).** Tier-derived example defaults: lite 30 / spec-tdd 60 / coverage 120 min (user-adjustable; unknown before tier routing — the initial value is a size estimate, aligned once level-1 routes). Exceeded → terminate and re-dispatch, **no "wait a bit longer"**; but: (i) a one-time reset while flowing — real output flowing at the moment of overrun → reset once and disclose (a size mis-estimate is a plan defect; once only); (ii) a continuation re-dispatch re-budgets by remaining scope (inheriting a burned-through budget = an instant kill); (iii) the budget must exceed the unit's verification plan's total build time. **Re-dispatch cap 2** (I9's shape); beyond that, escalate to the user.

6. **Freeze auto-recovery (freeze SOP).** The main session and level-1 may share a pool — during a 429 freeze the top cannot act either; the only levers inside the window are the far-fires and manual user messages. **The first successful turn (from any source: a far-fire landing / a manual user message / quota trickle) must do three things**: (i) record the 429 event, pool, reset moment, and freeze start into `RUN-STATE.md` (transcript error lines get eaten by compaction — the file is the re-arm base); (ii) schedule the reset+15 insurance point; (iii) disclose the freeze. **That turn collects before judging**: first digest the backlog from the freeze window (task notifications, agent states, RUN-STATE reconciliation) — a level-1 that finished during the freeze presents as a "total freeze" shape; check for closure before running the three states, or you'll wrongfully kill your own healthy card; a known freeze window is **deducted** from the output-age and budget readings (the freeze is the top's account, not the agent's — a mechanical over-budget kill here is a wrongful kill). **Post-first-429 dispatch discipline**: subsequent dispatches must not silently land in that pool — a known different-pool model satisfying the MID pin may be named, otherwise pause until the named reset.

7. **This skill's degraded closing (the last rung): exit, never run it yourself.** Re-dispatch also unavailable (pools dead / harness broken) → report to the user and run `/spec-tdd-escalate` in-session instead. The top personally taking over the machinery (writing tests / dispatching implementers) destroys this skill's two opt-in premises; that option does not exist.

## Report handling (the top only relays, never judges in level-1's place)

Escalate's routing-hygiene asks cannot reach the user from inside a dispatched context — I21 was pre-resolved by the handoff (not relayed); the sniff and the adversarial confirm follow **the v1.20.3 general rule: the report IS the ask, relayed by the top**. Level-1's STOP reports:

- **Sniff gaps** (the doc only looks settled) → relay the gap list verbatim and ask the user "grill first, or settled and continue": **settled** → re-dispatch with the flag (a fresh level-1; the handoff notes the user's approval + the gap list; the gaps are visible to Phase 1); **grill** → exit this skill into the grill front-end.
- **Multi-unit true shape** (the doc is really a bug list / a feature in slices — caught by the template's band carve-out) → relay, exit this skill, run a `spec-tdd` multi-unit run in the main session instead.
- **Above-band stakes** (adversarial grade) → relay the stakes grounds (one line) and ask the user: **Confirm adversarial** → **exit this skill**, run `spec-tdd-adversarial` standalone (a normal standalone tier run — attack rounds are hours-level depth, not carried in MID economics; this shape's session may be any tier, and adversarial's own I21 pre-flight takes over there as usual; the requirement doc and any written test hand over as **reference inputs** — the standalone run runs its own Phase 1 (direct-arrival shape), and the MID-written test is a draft to re-derive / harden, not an intake); **Downgrade → coverage**, re-dispatch with the recorded call, disclosed in the final report. Any other user ruling stands per I12.
- **No Agent tool** → fix spawn depth / environment and re-dispatch; never let level-1 self-test in place.
- **Other terminal reports (catch-all)** — failure reports after the I9 breaker trips (3 failed repairs, a designed normal ending), SPEC-bucket decision needs (I10: re-opening the requirement is the user's call), every non-GREEN terminal not covered above: **relay verbatim (with objective evidence); the user decides**. A user-mandated re-dispatch is a fresh mandate and does not burn the watchdog's re-dispatch cap. **Counting is divided, three separate ledgers**: death re-dispatches (watchdog / recovery procedure) count against the cap of 2; the findings loop's re-dispatch is bounded by the final review's one round; user-mandated re-dispatches rest on the user's explicit call (disclosed) — never borrow across.

A GREEN report → enter the final review.

## Half-finished-work resume (after a session break)

Session break / context corruption, the run stopped mid-way. This skill has no board — **the trace base = `RUN-STATE.md` + `REPORT.md` + git**:

1. **Inventory first, never rewrite** — read `RUN-STATE.md` (in-flight facts: unit, dispatch moment, budget, commit mode) + `git status` / `diff --stat` against the requirement doc, path-level mapping to judge which changes are legitimate half-done work; if level-1 already wrote `REPORT.md`, recover the numbers and hashes from it — never dig through a dead conversation.
2. **Level-1 still alive → prefer SendMessage to resume the same agent** (a background dispatch keeps its full context; the existing 429-break rule: agent dead, session alive → SendMessage resumes). The dead one is the nested implementer → the recovered level-1 re-dispatches a continuation implementer itself, sunk one level down.
3. **Re-dispatch a continuation level-1 (keep-don't-rewrite)** — attach the inventory result (diff file list + scope mapping) + "keep existing legitimate changes, fill only the gaps, never rewrite" + read `.spec-tdd/POLICY-<unit>.md` first (the cold-start policy source) + carry USER-FLAGGED GAPS. Budget re-granted by remaining scope (inheriting a burned-through budget = an instant kill).
4. **Re-arm** — the checkpoint ladder rescheduled whole against the new dispatch moment; RUN-STATE gets the breakpoint record (break moment, re-dispatch generation).
5. **Interrupted at the final-audit stage** — auditor in flight → same rule, SendMessage-resume preferred (its context holds the deep-review memory); `FINAL-AUDIT.md` already written (findings complete or partial) → recover from the file, never re-dispatch a completed review; audit not yet dispatched → the new session simply dispatches it (objective items re-run — the machinery is cheap).

## The final review (review gate — this skill's core)

**0. Review-gate tier check — retired (v1.23.0).** With the deep review outsourced, the shape has no in-session judgment-dense act left: the objective items are mechanical, the deep review lives in the TOP dispatch, arbitration defaults to adopt with objections escalated — the I21 ask's object is gone (opt-in 2's account, invocation-based). **The only revival point**: at review time dispatching is impossible (Agent tool broken) → fall back to an in-session final review; the I21 ask is asked once at that moment, disclosed.

**1. Objective items (mechanical and cheap, run first — numbers failing means no TOP audit dispatch is spent).**
   (a) **Compile** — run the main module's compile + compileTestJava once personally; green or it doesn't count;
   (b) **File scope** — `git diff --stat` + `git status --porcelain` against level-1's reported created/modified list; out-of-list changes inventoried first (explained or reverted); untracked scratch (`.spec-tdd/`) excepted;
   (c) **Number recheck** — read the JUnit XML (`build/test-results/test/*.xml`) against the reported per-class numbers; the counting-unit trap (methods vs invocations) converted before judging; a mismatch closes nothing;
   (d) **Hash comparison** — the level-1-reported pre-/post-dispatch acceptance-test hashes compare equal as strings (bit-identical, I4); the lite route excepted — no implementer dispatch to sandwich a hash around; I14's solo re-RED discipline replaces this item (reporting "no hash pair" is compliant).

**2. The deep review — an outsourced TOP auditor dispatch (this skill's value-add; the in-session deep review retired as of v1.23.0).**
   - **Dispatch spec**: **TOP**-pinned (I19(a) orthodox — the review dispatch names top), read-only, background mode; at dispatch announce to the user (what is being audited; results arrive by notification), and before the notification arrives, know nothing about the findings — no reporting, no predicting. RUN-STATE records the audit dispatch moment and the auditor's identity (the resume account for a session break).
   - **Brief = fixed checklist + doc paths, no summaries, no pre-digestion** (I19(c) — evidence as files; framing power taken out of any-tier session hands): the requirement doc path, the acceptance test path, level-1's `REPORT.md`, the JUnit XML directory, the created/modified file list, the hash pair (the lite route carries a "no hash pair" note), **the absolute path of `FINAL-AUDIT.md` (pasted by the top — the auditor's only write target)**. The checklist is verbatim items a–d below.
   - **Auditor checklist (four items, fixed order)**:
     a. **Acceptance-test encoding-fidelity re-read** (the all-MID compensation control, fixed first item): does every requirement line have a discriminating assertion? Can you name one wrong-but-plausible implementation that would pass? Over-assertion / silent interpretation? — the landing point, in this shape, of the encoding audit I19(a) originally pinned to TOP (the review duty defined in I13).
     b. **Impl diff correctness + SPEC-DEFECT sweep (I15)**: any production changes bent to accommodate the tests (test-defect traces); is the diff inside the deliverable scope only.
     c. **Disclosure consistency**: tier actually used, doc deviations, local rulings — each reasonable alone, but **together** do they contradict the requirement / decisions?
     d. **Residual-risk inventory**: band caps, mid-run downgrades, unverified dimensions — all into the report.
   - **Output and evidence rules**: the findings' full text goes to `.spec-tdd/<unit>/FINAL-AUDIT.md` (the resume substrate; the path is the absolute path given in the brief — SCRATCH ROOT pasted, never retyped, **the auditor never composes paths itself**) + a returned summary; every finding carries `file:line` evidence; every "OK" names the attack tried (the I16 rule — an OK without an attempted counterexample is a rubber stamp). The auditor can read the XML numbers (the brief carries the path) but **never re-runs compiles** — that's the session's machinery.
   - **Arbitration (once findings arrive)**: **default-adopt**; a rejection must carry the evidence the auditor lacked and **surface to the user** — a session of any tier never silently overrules a TOP auditor; ambiguities depending on grilling intent that the doc doesn't carry → always up to the user (I12 — the auditor sees only the doc; intent ambiguity is outside its judgment scope).

**3. Findings loop (the top only relays, never fixes by hand; two resumable children).** A finding → **SendMessage to level-1 to continue** (a completed agent is resumable — it holds the full context; the cheapest route) or a continuation re-dispatch (when its context is gone, keep-don't-rewrite); the top only hands over facts and the finding — the I10 three-bucket judgment is level-1's business. Fix reported → **the SAME auditor** re-checks the delta via SendMessage (the adoption check needs memory — this skill's version of I16: only the one who reviewed knows whether a finding was really handled, not papered over); only when the auditor is unresumable, a fresh re-dispatch (the new auditor re-reads everything from `FINAL-AUDIT.md` — one extra read, disclosed). **Bound: one fix round → delta re-check** (the I16 convention); not converged → escalate to the user; no infinite loop.

**4. Decision write-back + commit manifest + final report.** The requirement-doc edit proposals level-1 reported (DDL deviations, locally ruled details) are **applied and written back by the top** — the old text struck through for the record, never deleted outright (the family convention); left only in the conversation = did not happen (the spirit of I17), and the next run will understand the system per the old contract. **The commit is executed manually by the user (default)**: the top lists the **deliverable file manifest** (paths listed explicitly, including the written-back requirement doc; `.spec-tdd/` marked scratch, never in the list — even a manual user commit shouldn't `git add -A`); after committing, the user reports the hash and the top records it in the final report and RUN-STATE. The user explicitly asks the top to commit → comply (files listed explicitly, `-A` banned), recorded as a disclosed mode. The final report must carry: evidence (XML numbers, hashes), the disclosure list (tier actually used, **the all-MID opt-in (machinery)**, **the final TOP audit dispatch (+ death re-dispatch / fresh delta re-check if any)**, doc deviations, local rulings, re-test recommendation, proxy-commit disclosure if any), findings disposal, residual risks.

## Mid-run redirection (tier downgrade)

The user downgrades the tier mid-run under time pressure → **dual channel**: SendMessage into the background level-1 + simultaneously write `.spec-tdd/POLICY-<unit>.md` (level-1 re-reads it at boundaries; it overrides the TIER BAND, downgrade-only); completed assets preserved; converge to green and stop. Passed below the deserved tier → the final report lists a **re-test recommendation** (the unit-version ledger — no board here; the report IS the ledger; unbooked, a lightweight first pass silently becomes permanent).

## Common Mistakes

| Mistake | Fix |
|---|---|
| After dispatching, the top starts reading level-1's scratch / deep-reading deliverables mid-run | Stop at objective signals (heartbeat / XML / mtime / report relaying) — the deep review is the auditor dispatch's duty; mid-run deep reading = preempting the judgment + burning context for nothing |
| An Agent call omitting the model parameter (relying on defaults) | Silent session-model inheritance — level-1 and nested children name **MID**, the final-audit auditor names **TOP** (this skill's version of I19(a): omission breaks in both directions) |
| The top personally writing the acceptance test / dispatching implementers / running verification | All machinery is in level-1; the top running machinery = destroying the run shape (judgment tokens burned in the wrong place) |
| Level-1 stopping to ask about a tier upgrade / switching tiers on its own | The template pre-resolves it (ORCHESTRATOR TIER CHECK + MODEL PIN); restate the handoff on re-dispatch |
| Taking level-1's verbal test numbers on faith | Read the JUnit XML and recheck per class; only after unit conversion (methods vs invocations) still mismatching is it an anomaly |
| The top fixing findings by hand | SendMessage to resume, or re-dispatch — the top only hands over facts; fixing by hand = the agent boundary collapsing |
| A computed adversarial route making do at coverage inside this skill | Exit and run `spec-tdd-adversarial` standalone — attack rounds aren't carried in MID economics; the doc and any written test hand over as reference inputs (the standalone run runs its own Phase 1) |
| To save one dispatch, the top deep-reviews in-session itself | The deep review is a TOP dispatch — absorbing it = the judgment tier falling back into the session (the pre-v1.23.0 decline hole revives); the only exception: the no-dispatch degradation path (I21 ask revived, disclosed) |
| The top silently overruling an auditor finding | Arbitration defaults to adopt; a rejection must carry the evidence the auditor lacked and surface to the user — a session of any tier never silently overrules a TOP auditor |
| Writing summaries / pre-digested conclusions into the audit brief | Fixed checklist + doc paths (I19(c)) — a summary hands the session framing power; the auditor reads originals |
| After fixes, dispatching a fresh auditor to re-check the delta | The adoption check needs memory (I16) — the SAME auditor re-checks via SendMessage; only when unresumable, fresh (re-reads everything from FINAL-AUDIT.md, disclosed) |
| The top touching git writes itself ("just one quick commit") | Zero git writes across the chain: default = list the manifest, the user commits manually, reports the hash; a proxy commit only on the user's explicit request, recorded as a disclosed mode |
| The deliverable manifest missing files or mixing in scratch | The manifest lists absolute paths per file (including the written-back requirement doc); `.spec-tdd/` marked scratch, out of the list — the manifest is the user's only input for the manual commit |
| Running this skill in a session that cannot dispatch sub-agents at all | The degradation = `/spec-tdd-escalate` in-session, disclosed; "the top runs the machinery itself" is not an option |
| Scheduling only single-shot checkpoints in-flight | The checkpoint ladder's far-fires (the v1.20.2 shape) — the main session shares the pool's fate; only far-fires depend on no successful turn |
| Starting the run with the requirement only in the conversation | I17: land it first (requirement verbatim + decisions); the handoff uses the doc path |
| A bug list / multi-unit doc entering this skill directly | Entry routing blocks first (When-NOT); if it slips through → the template's band carve-out STOPs and reports; exit to a `spec-tdd` multi-unit run — the one-shot dispatch shape doesn't multiply by unit count |
| After a session break, digging state out of a dead conversation | `RUN-STATE.md` + `REPORT.md` + git are the trace base — the conversation died, the ledger lives; see "Half-finished-work resume" |

## Red Flags — STOP

- The top starts deep-reading deliverables verbatim before the final review → STOP — the deep review is the auditor dispatch's duty; objective signals and report relaying excepted.
- Closing without having dispatched the final auditor (or the auditor dead / notification not arrived) → STOP — a deep review with no TOP dispatch on record = the pre-v1.23.0 decline hole reviving.
- Overruling an auditor finding without the objection surfaced to the user → STOP — arbitration defaults to adopt; a rejection carries evidence and goes up (I12).
- Level-1 reports self-testing, or continues with no Agent tool → run void / fix the environment and re-dispatch.
- The acceptance test not bit-identical before vs after dispatch → I4 FAIL, route per the TEST bucket — even with a GREEN re-run.
- XML numbers don't match (after unit conversion) → no close; demand an explanation or a re-run.
- Level-1's routing finds above-band stakes and quietly starts → STOP and re-dispatch — report first; the top relays to the user.
- The final review finds a weak test but the implementation is GREEN, and the top wants to edit the test itself → STOP — re-dispatch level-1 through the TEST bucket (re-RED); the top never fixes by hand.
- The re-dispatch cap of 2 already reached and another one is tempting → escalate to the user.
- Catching yourself (the top) running any step of the machinery → STOP — back into the run shape, or degrade and exit this skill.
- The top executing any git write (incl. commit) beyond the user's explicit request → STOP — this skill's git-write authority is zero across the chain; the commit is the user's manual close.
