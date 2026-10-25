---
name: spec-tdd-manager
description: Use when the user says "spec-tdd-manager", or wants ONE feature walked end-to-end through the family's whole running order as a single invocation — inventory-resume → grill the requirement if fuzzy (the grill's spec gate is Gate 1) → size route (one unit vs multi-task) → top-layer breakdown in the Phase-0 shape (authoritative plan trio + self-contained task docs, dag-ready columns) → independent plan audit via spec-2nd-opinion (auto-escalates to spec-3rd-opinion when any decision carries an IRREVERSIBLE blast-radius tag) → ONE merged go-ahead gate (final plan + audit verdict + implementation route) → delegated implementation (spec-tdd-supervisor / spec-tdd-task-dag eco — multi-task always parallel-first, serial a mode inside it). A sequence-and-route-only pipeline front door: it owns the two gates and the stage handoffs, nothing else — every mechanism lives in the invoked skill. NOT for routing one settled requirement to a tier (spec-tdd-escalate), NOT for plain multi-unit bug batches (spec-tdd's multi-unit run), NOT for standalone plan audits (spec-2nd/3rd-opinion), NOT for resuming an in-flight implementation phase (invoke the driver skill directly), NOT for adversarial-grade features (standalone tier run). Triggers on the full pipeline in one go, grill to implementation all in one hand, end-to-end feature management, one command from requirement to landing, process manager, manage it to the end for me.
---

# spec-tdd-manager

**REQUIRED BACKGROUND:** Understand the `spec-tdd` family first — the front-ends (`grill-spec-tdd`, `adversarial-grill-spec-tdd`, `spec-tdd-escalate`, `spec-2nd-opinion`, `spec-3rd-opinion`), the tiers (`spec-tdd-lite` / `spec-tdd` / `spec-tdd-coverage` / `spec-tdd-adversarial`), the outer drivers (`spec-tdd-task-loop` / `spec-tdd-task-dag` / `spec-tdd-supervisor`), and [PROTOCOL.md](../PROTOCOL.md) (I1–I21). This skill adds no new invariant and relaxes none (one recorded deviation, v1.31.0: the discussed-entry fast lane merges the two gates' STOPS into Gate 2's single presentation — an approval is merged, never skipped; the entry shape is the consent): it is a pure sequencer layered on the **very outside** of the whole family — stage relays, auto routing, two gates. All machinery lives in the invoked skills; this skill personally running any machinery (writing acceptance tests, deep review, implementation) = an out-of-authority deformation.

## Overview

One feature's full-pipeline manager: from requirement intake to implementation landing, one running order to the end —

**S0 inventory** (the resume starting point) → **S1 grill** (when needed; Gate 1 = the grill's spec gate — on the discussed-entry fast lane Gate 1's stop rides Gate 2, see S1) → **S2 size route** (one unit or many tasks) → **S3 breakdown** (multi-task only; top-authored) → **S4 independent audit** (2nd/3rd-opinion) → **Gate 2: the merged go-ahead gate** (the only ask it owns) → **S5 implementation hand-off** (supervisor / task-dag eco).

Four design pillars:

1. **Sequence-and-route-only** (a generalization of escalate's route-only principle). What this skill owns is "who is the next station" and "the two gates" — no machinery.
2. **Break down first, then audit.** On the multi-task path the plan body (the trio + task docs) comes first, and the audit reviews **the finished artifact implementation actually consumes**; the trio then enters dag (whose base task-loop's Phase 0 is skipped by its own entry condition — trio present → skip) — removing the second plan review — **one TOP audit in place of two** (2nd-opinion + Phase 0 step 3); this is this skill's main economics for multi-task phases. Extending the audit brief with the decomposition dimensions is a legal "at minimum" expansion of 2nd-opinion's checklist.
3. **Two gates, no more, no less** (the discussed-entry lane may merge their two STOPS into Gate 2's single presentation — an approval is merged, never skipped; see S1). Gate 1 is inherited from grill (the spec gate — direction approval, a family invariant); Gate 2 is this skill's only owned ask (final plan + audit verdict + implementation route + go-ahead, one approval). The breakdown gets no separate gate — the task table rides Gate 2's presentation.
4. **Zero new deviations except the recorded fast lane (wording per the audit).** The breakdown is top-authored (I19(a)'s letter), the audit brief is assembled in-session (2nd-opinion's letter), and every invoked skill runs verbatim — untouched by THIS skill's mechanics (the family-wide tier map of v1.31.0 is a PROTOCOL-level definition change reaching every tier-check sentence, this file's included — not a manager deviation). The implementation stage **always riding eco economics** is a reuse of the existing opt-in (v1.26.0's invocation token), not a new deviation: it holds the moment the user invokes this skill (supervisor is natively this shape; dag carries the `eco` token), and the phase report follows the target skill's existing disclosure duties. **The `longrun` flag carries two additional recorded opt-ins** (S3 drafting, S4 audit-running delegated — see that section); without the flag this pillar stands as-is.

**Stage boundaries = session boundaries.** Every stage's output is an on-disk document (spec doc, trio, audit write-back): between any two stages you can `/clear`, switch sessions, and re-invoke this skill — S0 resumes from the documents on disk, nothing redone (the spirit of I17: existing only in the conversation = does not exist).

**Ask ledger (the honest list).** Gate 1 (grill's; on the discussed-entry lane its stop rides Gate 2), Gate 2 (owned), the I21 tier check (asked once on this skill's entry, suppressed downstream along the handoff — the drivers' v1.31.0 entry clauses honor a carried answer, closing the former no-skip-clause friction), the target skill's own asks (dag's commit authorization + time-band mode — pre-ruled at a going-dark gate and carried on the hand-off when S5 fires unattended, per the unattended-window section). Everything else is automatic — every automatic decision gets a one-line announcement + a one-line rationale, never an ask (the `longrun` flag adds no ask; dispatch ≠ ask).

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

Before any work, check the model THIS session runs as. This skill's S3 breakdown, S4 brief assembly and arbitration, and S2/S5 routing judgments all execute in the orchestrator's own context (**with the `longrun` flag, S3 drafting and S4 audit-running judgment move into TOP-pinned dispatches — the flag's invocation = recorded consent; the judgment the session keeps: the grill conversation, Gates 1/2, routing, user-finding relays**); I19 pins every dispatch's tier, but nothing can upgrade the session itself. **Top tier — or any tier above it — in use, or no higher tier exists → silent, move on.** (Tier map, maintainer ruling 2026-10-13: TOP = the top workhorse tier — opus-class; the flagship-experimental tier above it, fable-class, is never required for a pin.) Otherwise surface this ONE ask and stop for the answer:

> ⚠ **Orchestrator tier check** — this session runs a non-top model, and a run's planning / verification / routing all execute on it. **Upgrade** → run `/model`, pick the top tier, say "go" (the same conversation continues). **Ignore** → continue at this tier; the decline is disclosed in the final report.

Already asked in this conversation (by this skill or an invoked skill) → skip, never re-ask; the handoff record carries it along, and the decline goes into the final report's disclosures.

## S0 — entry inventory (the resume starting point)

A pure document inventory; announce the conclusion in one line:

- **FINAL SPEC doc present** → take S1's sniff route (clean → announce grill skipped, enter S2), plus run the irreversible-shape scan (end of S1). A fast-lane stamp on file holds: Gate 1 never re-fires; the direction approval rides Gate 2.
- **Trio present** → already audited and written back (amendment attribution, struck-through on file) → Gate 2 — **a Gate 2 stamp on file (attended approval, or the going-dark pre-approval record) → Gate 2 is not re-presented; S5 has fired or fires now**; not audited → S4.
- **Any driver's board / RUN-STATE in flight** → point the way: invoke that driver to resume; this skill reruns no preamble stages.
- **None of these** → S1.

Branch priority (per the audit's revision): **trio present > spec doc present** — when both exist (the norm after S3) take the trio branch; no grill rerun, no re-breakdown. Documents contradicting each other / multiple same-day specs with no way to decide → ask once (rare). A grill interrupted and re-entered = the conversation never existed; restart from S1 (I17).

## S1 — Grill (when needed; Gate 1 lives here)

- With the `longrun` flag → grounding is delegated first (see §longrun); the conversation, the questions, the recommendations, Gate 1 unchanged.
- Entry is a **conversational requirement** (no doc) → grill needed: the critical predicate (a silent wrong result MOVES money / CHANGES authorization / IRREVERSIBLY corrupts data) hits → `adversarial-grill-spec-tdd`; otherwise `grill-spec-tdd`. Its Phase 1's spec gate IS **Gate 1**. **Grill runs Phase 1 only (per the audit's revision)** — its Phase 2 (writing the acceptance test) and Phase 3 (invoking a tier) are superseded by this pipeline's S2–S5: the test is written by the downstream machinery, the routing is this skill's S5 table; the sole exception is the Phase 3 routing reuse when an all-adversarial feature exits (see When-NOT).
- **The discussed-entry fast lane (v1.31.0).** On a conversational entry whose discussion already settled every material dimension — the scan anchored to I11's materiality canon (observable behavior, state transitions, failure semantics, data integrity, security/authorization, compatibility, explicit NFRs) — the lane runs: **formalize the spec doc from the discussion FIRST**, then the materiality scan reads the doc plus the conversation (I17's spirit — disk state, not chat memory). Grounding still runs. A dimension the conversation left open → the lane's residual ONE ask (recommendations attached — the ask shape is new to this path; the settled-doc sniff always had it); answered → settled, the lane continues. **An IRREVERSIBLE-tagged decision not explicitly settled in the conversation gets its named confirmation in that same ask; an unanswered one still parks, and a bulk "all defaults" reply does not cover it** (grill's I12 letter, restated for this ask shape). Converged with nothing open → **no standalone Gate 1 stop**: the spec doc gains the lane stamp `fast lane declared (YYYY-MM-DD): direction approval rides Gate 2`, and the direction approval rides Gate 2's presentation. The Gate 1 audit-preview line (below) moves to the lane's one-line entry announcement — the 3rd's double-TOP cost stays visible and vetoable before the spend. Known lane cost: session death between discussion and the stamp → the conversation never existed → full re-grill (I17 as-is).
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
- The task table gains dag's two columns: **depends-on** and **expected files** — the multi-task route (dag) consumes them natively.
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
3. **The implementation route + one-line rationale + the estimated wall-clock** (the S5 table; cards × per-card tier estimate + the phase-end total-coverage pass + audit/build overhead — an interval while calibration is thin; expectation management, never the tier budget, which is a kill cap).
4. **The go-ahead approval.**

- **On the discussed-entry lane** the presentation additionally carries the spec-direction approval (the merged stop covers it — the pass stamp notes so when the lane stamp is on file).
- **Under a granted going-dark pre-approval** (see Unattended window) the verified three conditions stand in for this presentation: the session writes the pre-approval stamp and fires S5 — never re-presented.
- The user amends the plan → fold in + disclose; a substantive change (touching audited claims) → 2nd-opinion's ONE targeted re-audit bound applies.
- The route vetoed → recompute on the same table — the multi-task route is dag alone; quota pressure belongs to dag's own mode ask (all-serial / per-wave / auto time band), never a route change. A user who wants the bare serial driver invokes task-loop directly for the phase.
- **The pass stamp (per the audit's revision).** After approval, before the S5 invocation, the plan document gains one line: "Gate 2 approved (YYYY-MM-DD): route = <choice>" — an approval living only in the conversation = re-asked after `/clear`.
- **Gate 2 not passed → no implementation skill may be invoked.**

## S5 — implementation hand-off

| Shape | Invocation |
|---|---|
| One unit, non-adversarial | `spec-tdd-supervisor` (requirement doc = spec doc; I17 already satisfied; its pre-flight runs as usual) |
| Multi-task (default) | `spec-tdd-task-dag eco <phase>` — parallel-first (user ruling 2026-10-25: manager always picks supervisor or dag; quota pressure is dag's own mode ask's business — all-serial / per-wave / auto time band — never a route change; a chain-shaped plan self-skips the ask and runs serial; Windows worktree friction a known knob). This skill never pre-answers the ask, except the going-dark pre-ruled shape riding the hand-off, per the unattended-window section |
| Adversarial-grade (late-discovered: the S3 sniff pulled them all, or the audit revealed one) | out of the pipeline: standalone tier run, doc handover |

- **eco always rides** (invocation-based consent; supervisor is natively this shape).
- **Invocation = hand-off.** The phase's resume, watchdog, commit authorization, mid-run redirection, closing procedure (total-coverage pass + closing batch review) are all the target skill's business. An unattended S5 fire carries the going-dark gate's pre-ruled rulings on the `<phase>` hand-off; the drivers' v1.31.0 entry clauses treat them as answered. `<phase>` carries the doc path + a one-line phase description (the handoff uses the doc path, I19(c)).

## Unattended window (going-dark)

The user announces leaving / sleeping / going offline at ANY pipeline point — a dispatch in flight OR a run declared at entry (overnight included), with or without the `longrun` flag → read `{family root}/skills/GOING-DARK.md` and execute its gate NOW, in the manager dialect: the batched ask covers expected return / recovery actions (under `longrun`, the delegated-dispatch items — the runner's ONE fresh re-dispatch, different-pool overrides — per the longrun letters) / open Gate-1/Gate-2 decisions pre-ruled or explicitly deferred / run scope (what state the return should see — through which cards / what counts as closed, v1.32.1) / substrate choice and optional OS-level fallback arming. If the file is unreadable, still run the gate: batch-ask those items once and disclose that the protocol file was unread. A going-dark before the grill conversation has settled the decisions → grill's own "no human reachable → park at the gate" letter governs (the fast lane does not apply). Commit authority before Gate 2 is structurally N/A (no implementation has started); it goes live only under a granted pre-approval, pre-ruled in the same ask. **The gates themselves (Gate 1's approval, Gate 2) never run unattended — user-owned, they wait for the return; the sole exception is the Gate 2 pre-approval below.**

- **Gate 2 pre-approval (v1.31.0, the sole unattended exception).** Offered as an item of the same batched ask; default hold-until-return. Granted, it stands in for Gate 2's presentation **only when all three conditions hold at audit close**: (1) the audit closed "agreed, no amendments"; (2) no user-owned findings pending (I12); (3) every IRREVERSIBLE-tagged decision named-confirmed inside that same ask. The session verifies the three itself (under `longrun`: against the runner's RETURN — close stamp + user-owned findings verbatim), and with all holding writes the stamp `Gate 2 pre-approved (going-dark gate YYYY-MM-DD; conditions verified YYYY-MM-DD): route = <choice>` (+ `covers Gate 1's direction approval` when the lane stamp is on file) into the plan doc and fires S5. Any miss → the gate waits for the return. **Per-absence only — never carries over** (GOING-DARK item 1's shape).
- **Pre-ruling the S5 target's entry asks.** When pre-approving, the same ask pre-rules: dag's commit authorization (inherited from task-loop's pre-flight) + time-band mode (**auto-band only — the peak/off-peak bands themselves ride the hand-off; per-wave mode cannot be pre-ruled**, it asks at every wave boundary); and the session's I21 answer (a carried decline pre-answers the driver's check — the attended known-friction closes too). The rulings ride the `<phase>` hand-off; the drivers' v1.31.0 entry clauses treat them as answered.

## longrun mode — the context-longevity flag

`/spec-tdd-manager longrun` — an optional flag. **Runs without the flag are byte-identical to the sections above**; with the flag, S1 grounding, S3 drafting, and the S4 audit run become delegated shapes; S2, Gate 2, S5, and the two gates' presentation and approval are unchanged. Motive: **shrink the main session's context footprint so the run lives longer** — not token economy (boundary duplication raises total spend and wall-clock; carrying the flag accepts that trade). **The flag's invocation = recorded consent for the delegated judgment stages (S3 drafting, S4 arbitration)** (loop `eco`'s shape; the Pre-flight keeps applying to the judgment the session still holds).

- **S1 grounding → read-only MID dispatch** (legal basis: task-loop Phase 0's "inventory codebase anchors — a read-only Explore may run the recon" + grill's letter "(or dispatched)" — grounding's fact gathering is not I19(a)'s planning object). The output is a **facts digest landed on disk** (same directory as the spec doc — where a settled entry already keeps it; for fuzzy entry, the project's spec-convention directory, the same place the doc lands): each established fact with `file:line`, relevant symbol/table/config, neighboring conventions, blast-radius surfaces, a **coverage statement (self-reporting what it does NOT cover)**; conclusions and recommendations forbidden — judging is planning leaking downward. Grill works from the digest, keeping **pull rights** (decision-critical specific files may be read directly; an exception, not a bulk-read backdoor) and **follow-up rights** (SendMessage to keep querying the same agent; I18 stands as usual). **Re-entering with the flag + digest already present → reuse, don't re-dispatch, disclosed in one line.** The digest path = an S3 brief input, S0 resume material.
- **S3 drafting → TOP-pinned background drafter dispatch** (recorded opt-in #1, superseding S3's "authored by this session" under the flag; compensation = the TOP pin + the S4 audit already attacking the decomposition dimensions + Gate 2). Brief = the FINAL SPEC path + the digest path + the Phase 0 / Pre-flight 5–6 format + the per-card sniff + the two dag columns; the trio and every task doc are **written to disk**, plus a **claims annex** (falsifiable claims with `file:line`, for the S4 brief to reference). **On completion, stamp "draft complete (YYYY-MM-DD)" in the plan document — no stamp = partial; S0 sends nothing to audit and re-dispatches the drafter.** An adversarial discovery → STOP and report (the report IS the ask; the top relays to the user; a machine's say-so never launches). The session does **presentation-level review and amendments only** (amendments = attributed deltas). **The single-unit route (S3 skipped) does not use this item.**
- **S4 audit run → TOP-pinned background runner dispatch** (recorded opt-in #2; compensation = the TOP pin + the I12 hard carve-out + Gate 2 + **an informed-consent line on the independence regression**: the claims annex is authored by the drafter, raising the auditee's framing power over the audit's questions — bounded by: the checklist dimensions are manager-fixed, the auditor owns its (b)(e)(f) dimensions, and without the flag the claims are session-authored too, so the regression is limited to the distiller grounding). The runner reads `spec-2nd-opinion` / `spec-3rd-opinion`'s SKILL.md from disk by absolute path and **runs it verbatim** (the task-loop handoff pattern; the invoked skills untouched); brief material = the trio + the claims annex + pending decisions, the decomposition dimensions added as in S4. **The findings↔amend↔re-audit loop lives entirely inside the runner**: findings land as files (I19(b)); when the trio needs changes the top only relays paths — a one-line SendMessage to the drafter dispatch (which holds the author's context), the change lands on disk + a delta summary, a one-line call for the runner to re-check; **the single-unit route has no drafter — spec-doc amendments are made by the session (attributed deltas)**. The runner's announce-to-user step degrades to the session's one-line at-dispatch announcement (the I19(e) shape, disclosed). **The RETURN is exactly three things: the final plan path, the Gate 2 triple (verdict, folded amendments with attribution, residual risks), and user-owned findings verbatim** (I12: the runner never decides; relay to the user). The close stamp is runner-written; the session verifies the stamp before Gate 2. **A targeted re-audit for a substantive change made AT Gate 2: the session dispatches a fresh scoped auditor directly** (2nd-opinion's deliberate-fresh letter). Environment premise `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=3` (the runner dispatches an auditor child internally; the loop's same requirement). **Overflow = STOP and report** (user ruling 2026-09-24): truncate-never; never digest the trio into the brief (the no-digests rule); the session arbitrates — /clear between stages, or re-run that leg without the flag.
- **Silent-death discipline** (all three dispatches alike, 2nd-opinion class: coarse bound — the runner's in tens-of-minutes — + ONE fresh re-dispatch (nothing inherited, disclosed) + stall-report): **dead ≠ no findings**.
- **Unattended window.** The pipeline-level going-dark rule (the section above this one) applies with or without this flag; under the flag the dialect adds the delegated-dispatch items — grounding / drafter / runner recovery per their letters above, and a granted Gate 2 pre-approval is verified against the runner's RETURN.
- **The non-delegable list (always in the session)**: the grill conversation and its recommendations (incl. the fast lane's residual ask and IRREVERSIBLE named confirmations), Gate 1 (incl. the lane's merged direction approval), S2 routing, the relaying of user-owned findings, Gate 2's presentation and approval (incl. verifying the pre-approval's three conditions), the S5 hand-off.
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
| A pure bug list routed into dag eco | Out it goes: `spec-tdd`'s multi-unit run (user ruling 2026-09-22); a batch needs no per-task commit / board / watchdog |
| Re-running preamble stages when on-disk artifacts already exist | S0: landed = exists; a resume doesn't redo |
| Adding a third gate yourself (one more confirmation after the breakdown) | Two gates is the design; the task table rides Gate 2's presentation |
| eco without the dag token | Invoking this skill = choosing eco economics; the token always rides; the phase report follows the target skill's disclosure duties |
| An adversarial-grade feature forced into the eco pipeline | Out of the pipeline, standalone — hours-level attack depth is out of scope |
| Under longrun, the session bulk-reading the codebase itself (bypassing the digest) | The digest is the base; reuse, don't re-dispatch; a targeted read is the exception for decision-critical single files, not a bulk backdoor |
| A runner digesting user-owned findings inside itself | The I12 carve-out: such findings' verbatim text must return to the top for relaying; the runner never decides |
| A delegated dispatch dying silently and being read as "no findings / closed" | ONE fresh re-dispatch + disclosure; still dead → stall-report — dead ≠ no findings |
| Re-asking the bulk spec approval on a converged discussed entry (or re-firing Gate 1 past a lane stamp) | The lane's rule: converged + stamped → the direction approval rides Gate 2; the stamp is the on-disk state S0 reads |
| A granted going-dark pre-approval treated as unconditional, or carried to the next absence | Three conditions at audit close, any miss waits; per-absence only, never carries over |

## Red Flags — STOP

- Writing an acceptance test, dispatching an implementer, deep-reading deliverables → STOP — not this skill's job.
- Entering S3's breakdown before Gate 1 passes → STOP — the grill gate is the breakdown's premise (the fast lane's exception: converged + lane stamped — the direction approval rides Gate 2).
- Invoking any implementation skill before Gate 2 passes — supervisor / task-loop / task-dag **or any tier** (grill Phase 3 invoking a tier directly is equally guilty, per the audit's revision) → STOP.
- No spec on disk and no sniff run, skipping grill → STOP.
- An irreversible tag on record but only a 2nd scheduled (no user veto on record) → STOP.
- Starting work with an unconverged audit disagreement → STOP.
- Firing S5 unattended on anything but a granted Gate 2 pre-approval with all three conditions verified → STOP — the going-dark exception is the only unattended crossing.
- Catching yourself inventing a stage or an ask outside the running order → STOP — the running order is a closed set: S0–S5 + two gates; everything else belongs to the invoked skills.
- Under the `longrun` flag, the session personally doing recon (reading whole swaths of code before S3) or reassembling the S4 brief's full text → STOP — the flag's purpose is being eaten by its own hands (the digest / claims annex exist exactly for this).
