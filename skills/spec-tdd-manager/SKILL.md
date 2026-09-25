---
name: spec-tdd-manager
description: Use when the user says "spec-tdd-manager", or wants ONE feature walked end-to-end through the family's whole running order as a single invocation — inventory-resume → grill the requirement if fuzzy (the grill's spec gate is Gate 1) → size route (one unit vs multi-task) → top-layer breakdown in the Phase-0 shape (authoritative plan trio + self-contained task docs, dag-ready columns) → independent plan audit via spec-2nd-opinion (auto-escalates to spec-3rd-opinion when any decision carries an IRREVERSIBLE blast-radius tag) → ONE merged go-ahead gate (final plan + audit verdict + implementation route) → delegated implementation (spec-tdd-supervisor / spec-tdd-task-loop eco / spec-tdd-task-dag eco). A sequence-and-route-only pipeline front door: it owns the two gates and the stage handoffs, nothing else — every mechanism lives in the invoked skill. NOT for routing one settled requirement to a tier (spec-tdd-escalate), NOT for plain multi-unit bug batches (spec-tdd's multi-unit run), NOT for standalone plan audits (spec-2nd/3rd-opinion), NOT for resuming an in-flight implementation phase (invoke the driver skill directly), NOT for adversarial-grade features (standalone tier run). Triggers on the full pipeline in one go, grill to implementation all in one hand, end-to-end feature management, one command from requirement to landing, process manager, manage it to the end for me.
---

# spec-tdd-manager

**REQUIRED BACKGROUND:** Understand the `spec-tdd` family first — the front-ends (`grill-spec-tdd`, `adversarial-grill-spec-tdd`, `spec-tdd-escalate`, `spec-2nd-opinion`, `spec-3rd-opinion`), the tiers (`spec-tdd-lite` / `spec-tdd` / `spec-tdd-coverage` / `spec-tdd-adversarial`), the outer drivers (`spec-tdd-task-loop` / `spec-tdd-task-dag` / `spec-tdd-supervisor`), and [PROTOCOL.md](../PROTOCOL.md) (I1–I21). This skill adds no new invariant and relaxes none: it is a pure sequencer layered on the **very outside** of the whole family — stage relays, auto routing, two gates. All machinery lives in the invoked skills; this skill personally running any machinery (writing acceptance tests, deep review, implementation) = an out-of-authority deformation.

## Overview

One feature's full-pipeline manager: from requirement intake to implementation landing, one running order to the end —

**S0 inventory** (the resume starting point) → **S1 grill** (when needed; Gate 1 = the grill's spec gate) → **S2 size route** (one unit or many tasks) → **S3 breakdown** (multi-task only; top-authored) → **S4 independent audit** (2nd/3rd-opinion) → **Gate 2: the merged go-ahead gate** (the only ask it owns) → **S5 implementation hand-off** (supervisor / task-loop eco / task-dag eco).

Four design pillars:

1. **Sequence-and-route-only** (a generalization of escalate's route-only principle). What this skill owns is "who is the next station" and "the two gates" — no machinery.
2. **Break down first, then audit.** On the multi-task path the plan body (the trio + task docs) comes first, and the audit reviews **the finished artifact implementation actually consumes**; the trio then enters task-loop, whose Phase 0 is skipped by its own entry condition (trio present → skip) — removing the second plan review — **one TOP audit in place of two** (2nd-opinion + Phase 0 step 3); this is this skill's main economics for multi-task phases. Extending the audit brief with the decomposition dimensions is a legal "at minimum" expansion of 2nd-opinion's checklist.
3. **Two gates, no more, no less.** Gate 1 is inherited from grill (the spec gate — direction approval, a family invariant); Gate 2 is this skill's only owned ask (final plan + audit verdict + implementation route + go-ahead, one approval). The breakdown gets no separate gate — the task table rides Gate 2's presentation.
4. **Zero new deviations (wording per the audit).** The breakdown is top-authored (I19(a)'s letter), the audit brief is assembled in-session (2nd-opinion's letter), and every invoked skill runs verbatim — PROTOCOL untouched, the existing twelve untouched. The implementation stage **always riding eco economics** is a reuse of the existing opt-in (v1.26.0's invocation token), not a new deviation: it holds the moment the user invokes this skill (supervisor is natively this shape; loop/dag carry the `eco` token), and the phase report follows the target skill's existing disclosure duties. **The `longrun` flag carries two additional recorded opt-ins** (S3 drafting, S4 audit-running delegated — see that section); without the flag this pillar stands as-is.

**Stage boundaries = session boundaries.** Every stage's output is an on-disk document (spec doc, trio, audit write-back): between any two stages you can `/clear`, switch sessions, and re-invoke this skill — S0 resumes from the documents on disk, nothing redone (the spirit of I17: existing only in the conversation = does not exist).

**Ask ledger (the honest list).** Gate 1 (grill's), Gate 2 (owned), the I21 tier check (asked once on this skill's entry, suppressed downstream along the handoff; **known friction, per the audit's record**: task-loop's pre-flight has no skip clause — a non-top session that already answered may still be asked once more; just answer, and disclose), the target skills' own asks (loop's commit authorization, dag's time-band mode). Everything else is automatic — every automatic decision gets a one-line announcement + a one-line rationale, never an ask (the `longrun` flag adds no ask; dispatch ≠ ask).

## When to Use

- One feature you want walked from requirement to landing in a single invocation, appearing only at the two gates.
- Entry material unrestricted: a fuzzy requirement in the conversation, a settled spec already on file, or anything between.

**When NOT to use — route elsewhere:**

- You only want to route one settled requirement to a tier, no plan audit → `spec-tdd-escalate`.
- A pure bug list / multi-unit batch (many independent small fixes) → `spec-tdd`'s **multi-unit run** (user ruling 2026-09-22: manager's value is a feature's plan audit; a batch needs no per-task commit / board / watchdog / per-card final audit).
- You only want an existing plan audited, not implemented → `spec-2nd-opinion` / `spec-3rd-opinion` directly.
- The implementation phase is already in flight (board / RUN-STATE has in-flight) → invoke that driver directly for the resume (S0 would only point the way, not rerun the preamble).
- The whole feature is adversarial-grade → grill still runs, but implementation **exits the pipeline** to a standalone tier run (grill Phase 3's routing and confirmation machinery stays as-is) — hours-level attack depth is not carried by the eco economics or this pipeline.
- Exploratory / throwaway code → no skill needed.

## Pre-flight — orchestrator tier check (I21)

Before any work, check the model THIS session runs as. This skill's S3 breakdown, S4 brief assembly and arbitration, and S2/S5 routing judgments all execute in the orchestrator's own context (**with the `longrun` flag, S3 drafting and S4 audit-running judgment move into TOP-pinned dispatches — the flag's invocation = recorded consent; the judgment the session keeps: the grill conversation, Gates 1/2, routing, user-finding relays**); I19 pins every dispatch's tier, but nothing can upgrade the session itself. **Top tier in use, or no higher tier exists → silent, move on.** Otherwise surface this ONE ask and stop for the answer:

> ⚠ **Orchestrator tier check** — this session runs a non-top model, and a run's planning / verification / routing all execute on it. **Upgrade** → run `/model`, pick the top tier, say "go" (the same conversation continues). **Ignore** → continue at this tier; the decline is disclosed in the final report.

Already asked in this conversation (by this skill or an invoked skill) → skip, never re-ask; the handoff record carries it along, and the decline goes into the final report's disclosures.

## S0 — entry inventory (the resume starting point)

A pure document inventory; announce the conclusion in one line:

- **FINAL SPEC doc present** → take S1's sniff route (clean → announce grill skipped, enter S2), plus run the irreversible-shape scan (end of S1).
- **Trio present** → already audited and written back (amendment attribution, struck-through on file) → Gate 2; not audited → S4.
- **Any driver's board / RUN-STATE in flight** → point the way: invoke that driver to resume; this skill reruns no preamble stages.
- **None of these** → S1.

Branch priority (per the audit's revision): **trio present > spec doc present** — when both exist (the norm after S3) take the trio branch; no grill rerun, no re-breakdown. Documents contradicting each other / multiple same-day specs with no way to decide → ask once (rare). A grill interrupted and re-entered = the conversation never existed; restart from S1 (I17).

## S1 — Grill (when needed; Gate 1 lives here)

- With the `longrun` flag → grounding is delegated first (see §longrun); the conversation, the questions, the recommendations, Gate 1 unchanged.
- Entry is a **conversational requirement** (no doc) → grill needed: the critical predicate (a silent wrong result MOVES money / CHANGES authorization / IRREVERSIBLY corrupts data) hits → `adversarial-grill-spec-tdd`; otherwise `grill-spec-tdd`. Its Phase 1's spec gate IS **Gate 1**. **Grill runs Phase 1 only (per the audit's revision)** — its Phase 2 (writing the acceptance test) and Phase 3 (invoking a tier) are superseded by this pipeline's S2–S5: the test is written by the downstream machinery, the routing is this skill's S5 table; the sole exception is the Phase 3 routing reuse when an all-adversarial feature exits (see When-NOT).
- Entry brings a **doc claiming to be settled** (a document in the user's hands, or a spec doc S0 determined present) → fuzziness sniff (escalate I20's shape): clean → announce grill skipped; gaps → ONE ask (grill to fill them, or settled and continue) — settled holds and you continue (I12), the gap flags riding along to the downstream. A FINAL SPEC landed by the grill gate is decided by construction — the sniff passes it silently; no bypass is created.
- **One added line in the Gate 1 bundle (the audit preview; made conditional by the audit's revision).** Append to grill's gate presentation: "Audit: 2nd / 3rd (reason: decision D_k carries an IRREVERSIBLE tag)" — **present only when the pipeline continues** (an all-adversarial feature already exited via grill Phase 3; don't preview an audit that won't be spent); the 3rd's double-TOP cost is visible and vetoable **before the spend**. On settled entry (no Gate 1), this skill scans the spec doc's **irreversible shapes** itself (data migration / DDL, external contracts, security posture, money-movement semantics), the scan branching two ways: **irreversible but not all-adversarial** → 3rd triggers, announced in one line; **all-adversarial shape** → exit announcement (standalone tier run; escalate's adversarial-confirm convention per family rules). The user may change it on the spot (their call always stands); no separate ask.

## S2 — size route

- **Multi-task**: feature slices, more than one self-contained unit expected → S3. **A pure bug list (multi-unit batch) is not this skill** — route it straight out to `spec-tdd`'s multi-unit run (user ruling 2026-09-22: manager's value is a feature's plan audit; a batch takes the family's existing lighter shape).
- **One unit**: a single self-contained unit → skip S3 (the plan under audit = the spec doc itself; S4 still runs).
- **Adversarial-grade** → S2 does not re-judge (per the audit's revision): grilled entries already exited at Gate 1 via grill Phase 3; settled entries exited by the S1 scan. **Late-discovered** adversarial (S3's critical-surface sniff pulls them all, or the audit reveals one) → take the exit row of the S5 table.

One-line announcement + one-line rationale, no ask.

## S3 — breakdown (multi-task only; top-authored — I19(a))

In the format of task-loop's **Phase 0 / Pre-flight 5–6**, authored by this session (planning never sinks; fact recon may go to a read-only Explore, as task-loop's letter allows; **with the `longrun` flag → drafting delegated, session does presentation-level review — superseding this line's "authored by this session", see §longrun**):

- **The authoritative plan trio**: the requirement body, the decisions section (existing decisions settled as D1… numbering continued), the task-table status section (all pending).
- **One self-contained doc per task** (fields per task-loop Pre-flight 6: goal and non-goals, current-state anchors file:line + method names, design notes, the complete external contract given in full at once, the deliverable file list, acceptance criteria, risks and rollback).
- The task table gains dag's two columns: **depends-on** and **expected files** — switching the Gate 2 route (loop ↔ dag) costs zero.
- **Critical-surface sniff** (Phase 0's machinery): adversarial-grade tasks marked pulled/external in the table, run standalone, commits still landing at task boundaries.
- File paths follow the project's convention (I17: project convention wins).

## S4 — independent audit

- With the `longrun` flag → the audit run is delegated (see §longrun).
- Invoke **`spec-2nd-opinion`** (IRREVERSIBLE trigger → **`spec-3rd-opinion`**, previewed in S1).
- **The brief's checklist gains the decomposition dimensions** (allowed by 2nd-opinion's "at minimum"): task coverage (every requirement has a task), missing tasks, dependency-order correctness, task-doc self-containment, granularity deformation, expected-file column disjointness.
- 2nd / 3rd-opinion's machinery **runs verbatim**: brief assembly (Step 1, the session's living work), the auditor dispatch, the merge, disagreement arbitration, the grill-coverage finding's user routing (I12), write-back (struck-through for the record), the ONE targeted re-audit bound.
- Single-unit route (S3 skipped): claims-vs-codebase, blueprint-vs-code drift, grill-coverage hunt all run — the plan = the spec doc.
- **The close stamp (the resume basis, per the audit's revision).** When agreement holds, the session records one line in the plan document (the trio or the spec doc): "per audit (spec-2nd-opinion, YYYY-MM-DD): agreed, no amendments" (with amendments, the existing write-back is already the on-disk trace). A clean agreement leaving no trace = byte-identical to "never audited" after `/clear` — an I17-shaped hole.

## Gate 2 — the merged go-ahead gate (the only ask it owns)

Presented at once:

1. **The final plan** — multi-task: the task table (id + plain-language name + one line each) + pulled/external marks; one unit: the unit scope in one line. Irreversible tags named.
2. **The audit verdict** — verdict, folded amendments (attributed "per audit: …", never silently absorbed), residual risks.
3. **The implementation route + one-line rationale** (the S5 table).
4. **The go-ahead approval.**

- The user amends the plan → fold in + disclose; a substantive change (touching audited claims) → 2nd-opinion's ONE targeted re-audit bound applies.
- The route vetoed → recompute on the same table (e.g. adding "there is time pressure" → dag eco).
- **The pass stamp (per the audit's revision).** After approval, before the S5 invocation, the plan document gains one line: "Gate 2 approved (YYYY-MM-DD): route = <choice>" — an approval living only in the conversation = re-asked after `/clear`.
- **Gate 2 not passed → no implementation skill may be invoked.**

## S5 — implementation hand-off

| Shape | Invocation |
|---|---|
| One unit, non-adversarial | `spec-tdd-supervisor` (requirement doc = spec doc; I17 already satisfied; its pre-flight runs as usual) |
| Multi-task, default | `spec-tdd-task-loop eco <phase>` (serial = the ×1-quota-pressure 429-safe mode; Windows worktree friction is a known dag knob, defaulting to serial) |
| Multi-task + a true DAG + the user's stated time pressure | `spec-tdd-task-dag eco <phase>` (its own time-band mode ask runs; this skill never pre-answers) |
| Adversarial-grade (late-discovered: the S3 sniff pulled them all, or the audit revealed one) | out of the pipeline: standalone tier run, doc handover |

- **eco always rides** (invocation-based consent; supervisor is natively this shape).
- **Invocation = hand-off.** The phase's resume, watchdog, commit authorization, mid-run redirection, closing batch review are all the target skill's business. `<phase>` carries the doc path + a one-line phase description (the handoff uses the doc path, I19(c)).

## longrun mode — the context-longevity flag

`/spec-tdd-manager longrun` — an optional flag. **Runs without the flag are byte-identical to the sections above**; with the flag, S1 grounding, S3 drafting, and the S4 audit run become delegated shapes; S2, Gate 2, S5, and the two gates' presentation and approval are unchanged. Motive: **shrink the main session's context footprint so the run lives longer** — not token economy (boundary duplication raises total spend and wall-clock; carrying the flag accepts that trade). **The flag's invocation = recorded consent for the delegated judgment stages (S3 drafting, S4 arbitration)** (loop `eco`'s shape; the Pre-flight keeps applying to the judgment the session still holds).

- **S1 grounding → read-only MID dispatch** (legal basis: task-loop Phase 0's "inventory codebase anchors — a read-only Explore may run the recon" + grill's letter "(or dispatched)" — grounding's fact gathering is not I19(a)'s planning object). The output is a **facts digest landed on disk** (same directory as the spec doc — where a settled entry already keeps it; for fuzzy entry, the project's spec-convention directory, the same place the doc lands): each established fact with `file:line`, relevant symbol/table/config, neighboring conventions, blast-radius surfaces, a **coverage statement (self-reporting what it does NOT cover)**; conclusions and recommendations forbidden — judging is planning leaking downward. Grill works from the digest, keeping **pull rights** (decision-critical specific files may be read directly; an exception, not a bulk-read backdoor) and **follow-up rights** (SendMessage to keep querying the same agent; I18 stands as usual). **Re-entering with the flag + digest already present → reuse, don't re-dispatch, disclosed in one line.** The digest path = an S3 brief input, S0 resume material.
- **S3 drafting → TOP-pinned background drafter dispatch** (recorded opt-in #1, superseding S3's "authored by this session" under the flag; compensation = the TOP pin + the S4 audit already attacking the decomposition dimensions + Gate 2). Brief = the FINAL SPEC path + the digest path + the Phase 0 / Pre-flight 5–6 format + the per-card sniff + the two dag columns; the trio and every task doc are **written to disk**, plus a **claims annex** (falsifiable claims with `file:line`, for the S4 brief to reference). **On completion, stamp "draft complete (YYYY-MM-DD)" in the plan document — no stamp = partial; S0 sends nothing to audit and re-dispatches the drafter.** An adversarial discovery → STOP and report (the report IS the ask; the top relays to the user; a machine's say-so never launches). The session does **presentation-level review and amendments only** (amendments = attributed deltas). **The single-unit route (S3 skipped) does not use this item.**
- **S4 audit run → TOP-pinned background runner dispatch** (recorded opt-in #2; compensation = the TOP pin + the I12 hard carve-out + Gate 2 + **an informed-consent line on the independence regression**: the claims annex is authored by the drafter, raising the auditee's framing power over the audit's questions — bounded by: the checklist dimensions are manager-fixed, the auditor owns its (b)(e)(f) dimensions, and without the flag the claims are session-authored too, so the regression is limited to the distiller grounding). The runner reads `spec-2nd-opinion` / `spec-3rd-opinion`'s SKILL.md from disk by absolute path and **runs it verbatim** (the task-loop handoff pattern; the invoked skills untouched); brief material = the trio + the claims annex + pending decisions, the decomposition dimensions added as in S4. **The findings↔amend↔re-audit loop lives entirely inside the runner**: findings land as files (I19(b)); when the trio needs changes the top only relays paths — a one-line SendMessage to the drafter dispatch (which holds the author's context), the change lands on disk + a delta summary, a one-line call for the runner to re-check; **the single-unit route has no drafter — spec-doc amendments are made by the session (attributed deltas)**. The runner's announce-to-user step degrades to the session's one-line at-dispatch announcement (the I19(e) shape, disclosed). **The RETURN is exactly three things: the final plan path, the Gate 2 triple (verdict, folded amendments with attribution, residual risks), and user-owned findings verbatim** (I12: the runner never decides; relay to the user). The close stamp is runner-written; the session verifies the stamp before Gate 2. **A targeted re-audit for a substantive change made AT Gate 2: the session dispatches a fresh scoped auditor directly** (2nd-opinion's deliberate-fresh letter). Environment premise `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3` (the runner dispatches an auditor child internally; the loop's same requirement). **Overflow = STOP and report** (user ruling 2026-09-24): truncate-never; never digest the trio into the brief (the no-digests rule); the session arbitrates — /clear between stages, or re-run that leg without the flag.
- **Silent-death discipline** (all three dispatches alike, 2nd-opinion class: coarse bound — the runner's in tens-of-minutes — + ONE fresh re-dispatch (nothing inherited, disclosed) + stall-report): **dead ≠ no findings**.
- **The non-delegable list (always in the session)**: the grill conversation and its recommendations, Gate 1, S2 routing, the relaying of user-owned findings, Gate 2's presentation and approval, the S5 hand-off.
- On resume, re-carry the flag; the digest and findings documents are S0's on-disk material. **Mixed-mode resume (the flag not re-carried) → one-line disclosure, not blocking.**

## Common Mistakes

| Mistake | Fix |
|---|---|
| This skill personally writing acceptance tests / deep-reviewing / implementing | Sequence-and-route-only — the machinery lives in the invoked skills; exceeding authority deforms the run |
| Auditing the high-level blueprint first, then letting Phase 0 re-break and re-audit it | Break down first, then audit: what's audited is the trio itself; Phase 0 skips by its entry condition — every multi-task phase saves one TOP audit |
| Invoking an implementation skill before Gate 2 passes | The go-ahead gate is the only implementation authorization point (the family-side landing of never-code-before-approval) |
| The 3rd upgrade disclosed only after the audit | The Gate 1 bundle previews it first (settled entry: a one-line announcement) — visible and vetoable before the spend |
| Entering Gate 2 with the audit not in agreement (a disagreement unresolved) | 2nd-opinion's gate is agreement, not a report; without agreement, arbitrate first or go up |
| Re-interrogating an on-disk spec (without running the sniff) | I20: clean → proceed; the user's settled call stands |
| After grill, following its Phase 2/3 (writing tests, invoking a tier directly) | Grill runs Phase 1 only (gate = Gate 1); Phases 2/3 are superseded by S2–S5 — the sole exception is the routing reuse on an adversarial exit (per the audit's revision) |
| A pure bug list routed into loop eco | Out it goes: `spec-tdd`'s multi-unit run (user ruling 2026-09-22); a batch needs no per-task commit / board / watchdog |
| Re-running preamble stages when on-disk artifacts already exist | S0: landed = exists; a resume doesn't redo |
| Adding a third gate yourself (one more confirmation after the breakdown) | Two gates is the design; the task table rides Gate 2's presentation |
| eco without the loop/dag token | Invoking this skill = choosing eco economics; the token always rides; the phase report follows the target skill's disclosure duties |
| An adversarial-grade feature forced into the eco pipeline | Out of the pipeline, standalone — hours-level attack depth is out of scope |
| Under longrun, the session bulk-reading the codebase itself (bypassing the digest) | The digest is the base; reuse, don't re-dispatch; a targeted read is the exception for decision-critical single files, not a bulk backdoor |
| A runner digesting user-owned findings inside itself | The I12 carve-out: such findings' verbatim text must return to the top for relaying; the runner never decides |
| A delegated dispatch dying silently and being read as "no findings / closed" | ONE fresh re-dispatch + disclosure; still dead → stall-report — dead ≠ no findings |

## Red Flags — STOP

- Writing an acceptance test, dispatching an implementer, deep-reading deliverables → STOP — not this skill's job.
- Entering S3's breakdown before Gate 1 passes → STOP — the grill gate is the breakdown's premise.
- Invoking any implementation skill before Gate 2 passes — supervisor / task-loop / task-dag **or any tier** (grill Phase 3 invoking a tier directly is equally guilty, per the audit's revision) → STOP.
- No spec on disk and no sniff run, skipping grill → STOP.
- An irreversible tag on record but only a 2nd scheduled (no user veto on record) → STOP.
- Starting work with an unconverged audit disagreement → STOP.
- Catching yourself inventing a stage or an ask outside the running order → STOP — the running order is a closed set: S0–S5 + two gates; everything else belongs to the invoked skills.
- Under the `longrun` flag, the session personally doing recon (reading whole swaths of code before S3) or reassembling the S4 brief's full text → STOP — the flag's purpose is being eaten by its own hands (the digest / claims annex exist exactly for this).
