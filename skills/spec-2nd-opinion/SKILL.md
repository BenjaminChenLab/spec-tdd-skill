---
name: spec-2nd-opinion
description: Use when the user says "spec-2nd-opinion", or a plan/design/ordering has been settled by grill or discussion (pre-implementation) and the user wants an independent audit before committing to it. Dispatches ONE read-only auditor subagent to verify the plan's claims against the codebase; the final plan is presented only when orchestrator and auditor agree.
---

# spec-2nd-opinion

**REQUIRED BACKGROUND:** A plan exists and has been grilled/discussed to a settled state — the work items, their order, and the rationale are decided; anything still owned by the user is explicitly listed as a **pending user decision**. This skill does not grill and does not implement. It audits the plan, then presents the final plan — or the honest disagreement.

## Overview

Same-context blind spots are the failure mode this skill exists to catch: the session that designed the plan verified it with the same assumptions it was built on. **Independence is the one thing a diligent same-context agent cannot give itself.** You dispatch ONE read-only auditor with a falsifiable brief; the plan ships only when you and the auditor agree.

**Core principle: audit, then gate.** The auditor verifies *facts and interactions* (claims vs the actual codebase, blueprint-vs-code drift, cross-item risks, ordering) — never re-litigates user-owned decisions (the WHAT, I12's territory): those ride the brief as "pending user decisions" and the auditor may only flag their *consequences*.

## When to Use
- User says `spec-2nd-opinion`.
- A settled plan (design doc / blueprint / agreed ordering of work items) is about to be committed to, and the user wants a second, independent set of eyes first.
- The plan rests on factual claims about the codebase ("X is not implemented", "Y already supports Z", "these two items don't interact") that are cheap to verify and expensive to be wrong about.

**When NOT to use** — route elsewhere:
- The plan still has ungrilled decision gaps → grill first (`grill-spec-tdd` family); auditing a fuzzy plan just certifies fuzz.
- Implementation is done and needs verification → the tier ladder (`spec-tdd` …), not this.
- The user wants a third adversarial opinion too → `spec-3rd-opinion` (this skill + a second, adversarial auditor).

## Pre-flight — orchestrator tier check (I21)

Before any work, check the model THIS session runs as. A run's judgment — here: distilling the falsifiable brief, merging the verdicts, arbitrating the disagreements — executes entirely in the orchestrator's own context; I19 pins the auditor dispatch TOP, but nothing can upgrade the session itself. **Top tier in use, or no higher tier exists → silent, move on.** Otherwise surface this ONE ask and stop for the answer:

> ⚠ **Orchestrator tier check** — this session runs a non-top model, and a run's planning / verification / routing all execute on it. **Upgrade** → run `/model`, pick the top tier, say "go" (the same conversation continues). **Ignore** → continue at this tier; the decline is disclosed in the final report.

Already surfaced earlier in this conversation (typically by the grill that settled the plan)? Skip it — never re-ask; a recorded decline rides into the final plan's disclosure.

## The flow

### Step 0 — Preconditions (stop if unmet)
1. The plan is settled: items + order + rationale written down (a blueprint doc, or a distilled summary if it lives only in conversation — persist it first, I17's spirit: a plan settled only in conversation is not auditable at distance).
2. Open **user-owned decisions** are enumerated as pending, not silently defaulted.
3. Nothing has been implemented yet (or the already-written piece is declared in the brief as an auditable work item — e.g. an uncommitted fix).

### Step 1 — Distill the audit brief
The brief is the auditor's entire world. It must contain, in order:

1. **Background** — repos/paths involved, established facts *each with its evidence* (log analysis, DB query, file:line — the auditor re-verifies what's cheap, takes the rest as given and says so).
2. **The plan under audit** — the work items, the proposed order, and the rationale — stated as-is, never pre-defended.
3. **Claims-to-verify** — the falsifiable factual assertions the plan rests on, each with a pointer (file/symbol/table) where checkable.
4. **Checklist** — at minimum: (a) per-claim verification, (b) blueprint-vs-code drift (docs older than recent changes to the same region — check dates/commits), (c) cross-item interaction risks, (d) ordering verdict with the strongest counter-argument, (e) one risk nobody listed.
5. **Output format demanded** — per item: VERDICT (confirmed / refuted / partially) + `file:line` evidence; final section "AUDITOR POSITION": agree / disagree with the plan + required amendments + missed risks. **Every "OK" must name the attack attempted** (I16's rule — no rubber-stamping).

Never include expected verdicts or your confidence — that's contamination, not context.

### Step 2 — Dispatch ONE auditor, read-only
- Agent type: general-purpose (or equivalent). **Read-only**: the brief says so explicitly (no file modifications, no git writes).
- Model: **TOP tier** (I19(a) — this is a review dispatch).
- Background mode; announce to the user what is being audited and that results arrive by notification. **You know nothing about its results until the completion notification arrives — never report, assume, or predict them.**
- **The notification never comes?** A background child can die silently (the family's twice-learned lesson) — a dispatch that shows failed, or sits silent past a coarse bound (read-only plan audits run minutes-to-tens), gets **ONE fresh re-dispatch** (nothing is inherited), disclosed; still nothing → report the stall to the user. A silently-dead audit is not an agreed one.
- **No dispatch tool available?** STOP and disclose: the plan may be presented only marked **UNAUDITED** — a silent self-audit is worthless by this skill's own thesis (adversarial-grill's rule); whether to proceed on an unaudited plan is the user's call (I12).

### Step 3 — Merge the verdicts (the gate)
- **Agree** (auditor's position endorses the plan, no critical claim refuted) → Step 4.
- **Disagree** → surface it per point: who claimed what, the auditor's evidence, your position. Then either (a) you side with the auditor with stated reasons and amend the plan, (b) you defend your position with evidence the auditor lacked, or (c) it's genuinely the user's call — ask. Amended points may get **ONE targeted re-audit** (fresh context, scoped to the amendments, the disagreement history written into the brief). The bound is I16's — audit plus one re-audit, never a loop — the auditor is deliberately FRESH, a stated deviation: I16 keeps the same auditor because adoption-check needs its memory, while an amended point is a new claim to verify and freshness serves that (adversarial-grill's contrast: attack wants freshness, adoption-check wants memory).

### Step 4 — Present the FINAL PLAN
Format: the items and order; the rationale; **audit amendments integrated and attributed** ("per audit: …" — never silently absorbed); pending user decisions restated; residual risks the audit surfaced but did not block on. **Write the final plan back to the persisted doc** — amendments folded in with their attribution, superseded text struck through, not deleted (task-loop's write-back shape): the handoff moves by doc path (I19(c)), and a doc still holding the pre-audit version is exactly the blueprint-vs-reality drift this skill audits in others. Then STOP — this skill plans, it does not implement; hand off explicitly (e.g. to the implementation flow of the user's choosing).

## Common Mistakes
| Mistake | Fix |
|---|---|
| Auditing a plan with open decision gaps | Grill first. An audit certifies a settled plan, not a draft. |
| Letting the auditor re-litigate user decisions | The brief scopes it: pending decisions' *consequences* only, the WHAT is the human's (I12). |
| Pre-digesting verdicts into the brief ("I'm confident X is fine, just check") | State the plan and claims; never expected verdicts. The auditor judges or the independence was theater. |
| Reporting/predicting audit results before the notification | You know nothing until the notification. Tell the user it's running and wait. |
| Watering down "partially confirmed" into "agreed" | The gate is the auditor's explicit position; partial = disagreement to resolve. |
| Absolving a disagreement by merging silently into the final plan | Disagreements are surfaced per point with your arbitration reasons — or escalated to the user. |
| Auditor edits files | The brief forbids it; this is a read-only audit. |
| Final plan presented in conversation while the doc still holds the pre-audit version | Write the amendments back (struck-through, not deleted). The next entry point receives the doc, not the chat. |
| No dispatch tool, so the session "audits" its own plan | STOP and disclose; present only marked UNAUDITED. A self-audit is worthless by this skill's own thesis. |
| Treating a silently-dead audit dispatch as "no findings" | One fresh re-dispatch, disclosed; then report the stall. Dead is not agreed. |
| Presenting the final plan and then starting implementation | This skill ends at the plan. Implementation routes elsewhere. |

## Red Flags — STOP
- About to write the final plan with no auditor notification on record.
- About to present the plan while the audit dispatch is dead or stalled — a dead audit is not an agreed one (fresh re-dispatch or report the stall).
- About to re-dispatch a second re-audit round on the same points (the bound is one).
- The auditor's report has verdicts without file:line evidence, or "OK"s that name no attempted attack — demand the evidence, don't proceed on vibes.
- About to treat a user-owned pending decision as settled because the audit didn't flag it — absence of an audit flag is not user consent.
- About to implement. Not this skill's job.
