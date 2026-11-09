---
name: spec-tdd-secretary
description: Use when the user says "spec-tdd-secretary", or wants ONE discussed non-critical unit run as a fast two-station chain — settled plan → independent plan audit (spec-2nd-opinion's machinery, verbatim) → in-session implementation (spec-tdd-lite, verbatim) — where a CLEAN audit agreement fires the implementation immediately in the same session with no fresh go-ahead ask (the invocation is the recorded consent; this skill's clean path is a standing, scoped exception to always-ask-before-implementation, disclosed in the final report). Any non-clean state (disagreement, folded amendments, pending user decisions, residual risks) stops for the user per the audit skill's own machinery. Upgrade ceiling spec-tdd — a too-big-but-non-critical unit is audited then implemented by delegated spec-tdd (an announced economic route, never an ask); lite's own stall breaker promotes mid-run. Referrals OUT at entry — fuzzy requirement → grill family; critical predicate (a silent bug MOVES money / CHANGES authorization / IRREVERSIBLY corrupts data) or IRREVERSIBLE shapes → spec-tdd-escalate / spec-tdd-manager; multi-unit batch → spec-tdd's multi-unit run. NOT for the full pipeline with breakdown and gates (spec-tdd-manager), NOT for standalone plan audits (spec-2nd-opinion / spec-3rd-opinion), NOT for critical surfaces (adversarial-grade standalone runs), NOT for plain tier routing of a settled requirement (spec-tdd-escalate). Triggers on the light fast pipeline, audit then implement in one chain, secretary mode, discussed plan straight into the build.
---

# spec-tdd-secretary

**REQUIRED BACKGROUND:** Understand the `spec-tdd` family first — in particular the two stations this skill sequences: `spec-2nd-opinion` (whose machinery it runs verbatim) and `spec-tdd-lite` (the in-session tier it fires). This skill adds no new protocol invariant and relaxes none. It is a pure two-station sequencer on `spec-tdd-manager`'s sequence-and-route-only pattern, carrying exactly ONE recorded opt-in (the clean-fire consent, below). All machinery lives in the invoked skills; this skill personally writing an acceptance test, implementing, or reviewing = an out-of-authority deformation.

## Overview

The light fast pipeline for one discussed unit: take the settled plan, run it through ONE independent TOP read-only audit (2nd-opinion's machinery), and on a **clean agreement** fire the implementation **immediately, in the same session** (lite by default) — the lite route costs two TOP dispatches (the plan audit + lite's fresh test review; the spec-tdd upgrade route costs three) and zero go-ahead stops on the clean path. That is the design's whole trade: independence at the two cheapest, highest-leverage blind-spot positions (plan-level before any implementation tokens, test-strength after GREEN), with the expensive middle — delegated implementation — removed.

**The recorded opt-in (the clean-fire consent).** Invoking this skill pre-registers the handoff from the audit station to the implementation station: on a clean audit close the session announces one line and fires — **no fresh go-ahead ask**. This is an explicit, recorded exception to the family's never-implement-before-an-approved-gate landing (and to the maintainer's standing rule that an agreed plan is still not approval to build): here the invocation IS the approval, scoped to this skill's clean path only. Every non-clean state still stops (below), and the close report discloses that the run was fired on this consent.

**Clean defined (the fire predicate — all four, from the audit's close):**
1. The auditor's position **endorses** the plan (no critical claim refuted);
2. **Zero amendments** folded into the write-back;
3. **Zero pending user decisions** restated at the close;
4. **Zero residual risks** the audit surfaced.

Any miss → the non-clean path. A grill-coverage finding (a dimension the plan decides nothing about) creates a pending user decision by construction → always non-clean.

## When to Use
- User says `spec-tdd-secretary <feature>`.
- ONE small/medium non-critical unit whose plan was settled by discussion (this conversation, or a doc on hand) — the discussed-entry shape: you talked it through, now you want it audited and built in one continuous chain without ceremony.
- The session that discussed the plan is the session that runs this skill (lite implements in-session; that is the point).

**When NOT to use — route elsewhere:**
- The requirement is still fuzzy (un-grilled decision gaps) → grill family first; auditing fuzz certifies fuzz (2nd-opinion's own refusal).
- Critical predicate — a silent wrong result MOVES money / CHANGES authorization / IRREVERSIBLY corrupts data (money-adjacent display/reporting does NOT qualify) — or IRREVERSIBLE shapes (DDL/migration, external contracts, security posture, money-movement semantics) → out of this pipeline: `spec-tdd-escalate` (picks the adversarial tier, its own confirm ask) or `spec-tdd-manager` (the full pipeline).
- A multi-unit batch or split feature → `spec-tdd`'s multi-unit run.
- You want the whole feature's pipeline (breakdown, gates, routed drivers) → `spec-tdd-manager`.
- You want the plan audited, not implemented → `spec-2nd-opinion` directly.
- You are live-testing and streaming fixes below lite's test-first cycle → `spec-tdd-quickfix` (the entry sniff suggests it; your call stands).

## Pre-flight — orchestrator tier check (I21)

Before any work, check the model THIS session runs as. This skill's entry sniff, the fire decision, and (on the lite route) the entire implementation inner loop execute in the orchestrator's own context; the stations' dispatches are tier-pinned, but nothing can upgrade the session itself. **Top tier — or any tier above it — in use, or no higher tier exists → silent, move on.** (Tier map, maintainer ruling 2026-10-13: TOP = the top workhorse tier — opus-class; the flagship-experimental tier above it, fable-class, is never required for a pin.) Otherwise surface this ONE ask and stop for the answer:

> ⚠ **Orchestrator tier check** — this session runs a non-top model, and a run's planning / verification / routing all execute on it. **Upgrade** → run `/model`, pick the top tier, say "go" (the same conversation continues). **Ignore** → continue at this tier; the decline is disclosed in the final report.

The answer carries downstream: both stations' own checks skip a check already surfaced this conversation (their handoff clauses), and a recorded decline rides into the final report's disclosures.

## Entry sniff (the routing table — every rule is an existing family boundary, none invented here)

Announce the verdict in one line + one-line rationale; every exit is a referral, the user's call stands.

- **Fuzzy** (decision gaps, or a doc that only looks settled) → ONE-line referral to the grill family. Forced: 2nd-opinion refuses fuzzy plans.
- **Critical predicate or IRREVERSIBLE shapes** → referral out (`spec-tdd-escalate` / `spec-tdd-manager`). Forced: lite refuses critical units; this pipeline's ceiling is spec-tdd, adversarial never rides it.
- **Multi-unit** (a batch, a split feature) → referral out to `spec-tdd`'s multi-unit run. Forced: lite's second-unit rule.
- **Quickfix shape** (the user is live-testing the product AND the request sits below lite's test-first cycle — a wiring/cosmetic/config swap, zero business rules, zero boundary policy; copying an existing precedent verbatim qualifies — AND outside quickfix's exclusions: money/auth/data-loss logic, anything needing an acceptance test) → ONE-line suggestion to exit to `spec-tdd-quickfix`; continue on the user's word.
- **ONE non-critical unit** → in lane. Size call (an economic route, announced never asked — manager S2's pattern): fits lite (small/medium, a session you'll clear after) → **the implementation station = lite** (the default); too big for lite but single and non-critical → **the implementation station = spec-tdd** (the upgrade ceiling) — the audit still runs first either way.

## Step 0 — persist the plan

The audit's precondition is a plan on disk (I17: settled only in conversation = not auditable). Plan already a doc → use it. Conversation-only → persist it now per project convention (family default `docs/specs/YYYY-MM-DD-<feature>.md`), announced in one line — this same doc satisfies lite's Phase-1 persistence, so that prompt never fires. Pending user decisions, if any, are enumerated as pending, never silently defaulted.

## Step 1 — the audit station

Run `spec-2nd-opinion` **verbatim**: brief assembly (its Step 1 — background with evidence, the plan as-is, falsifiable claims, its checklist, output format, the standing file-tools rule), the ONE read-only TOP background dispatch (its death/re-dispatch rules), the merge-and-gate (its Step 3), and the write-back. Then one addition of this skill's own (manager S4's resume discipline, reused): the **close stamp** — a line in the plan doc, "per audit (spec-2nd-opinion, YYYY-MM-DD): agreed, no amendments" (with amendments, the write-back itself is the on-disk trace).

**No checklist extension.** Manager extends the brief with decomposition dimensions because it audits a breakdown trio; this pipeline audits ONE unit's plan — the stock checklist (claims, drift, interactions, ordering, the unlisted-risk probe, grill coverage) fits as-is.

## Step 2 — the fire decision (the one mechanism this skill owns)

**The doc-state guard (both paths):** before any fire, the plan doc must sit exactly as the audit left it — the write-back (or the clean close) is the last write. A post-audit edit — yours or the user's — voids the close: fold it per the write-back shape and disclose; a substantive change (touching audited claims) takes 2nd-opinion's ONE targeted re-audit bound. Never fire on an unaudited edit (manager Gate 2's amend-and-fold moment, restated for the unattended gap between audit and fire).

- **Clean (all four predicate items on record)** → ONE-line announcement — audit clean, firing the implementation station now, per the invocation consent — then append the **fire stamp** to the plan doc ("implementation fired (YYYY-MM-DD, lite|spec-tdd): clean-fire consent — predicate verified (endorse / 0 amendments / 0 pending / 0 residual)") and proceed to Step 3 immediately. No ask. The consent's disclosure lands in the close report.
- **Non-clean (any miss)** → 2nd-opinion's own machinery carries: per-point arbitration with stated reasons, user-owned items surfaced to the user, ONE targeted re-audit on amended points (the bound is one round). After resolution, the fire decision is the user's once — the stop has them present; they say go, the fire stamp records "explicit go" in place of the consent, and Step 3 fires.

## Step 3 — the implementation station

Invoke the routed skill **verbatim**; this skill adds nothing to its run and owns none of its asks (its SPEC-bucket questions, its exit rules, its final surface-WHAT report — all its own):

- **Default — `spec-tdd-lite`**: Phase 1 writes the acceptance test against the persisted spec doc (RED; no persistence prompt — Step 0 satisfied it), Phase 2 implements in-session, Phase 3 dispatches the fresh TOP test review (the second of the chain's two dispatches). Its exit rules govern: solo re-RED, the SPEC-DEFECT sweep, the stall breaker.
- **Upgrade route — `spec-tdd`** (entry-sniffed too-big, or lite's stall breaker promoting mid-run): its three-phase machinery (acceptance test → delegated implementer → orchestrator verification) runs unchanged. This is the ceiling — never beyond spec-tdd on this pipeline.
- **A critical surface discovered mid-run** (the litmus hits during implementation) → STOP and refer out — lite refuses critical units and so does this pipeline; the ceiling does not stretch.

## Close — stamps and resume

After the station's exit, append the close stamp — "secretary pipeline closed (YYYY-MM-DD): audited spec-2nd-opinion, implemented lite|spec-tdd" — and deliver the close report: the station's own final report **plus one line disclosing that the run was fired on the clean-fire consent** (when it was). A run leaving no on-disk trace is byte-identical to never-run after `/clear` — the stamps are the resume state:

- **Audit stamp only, no fire stamp** → the session died between the audit close and the fire decision: re-enter Step 2 and verify the four predicate items from the doc (the write-back, the pending-decisions section) — the audit stamp alone covers only items 1–2; never blind-fire on it. Nothing re-audited.
- **Fire stamp present** → the fire basis is on record (clean-consent = the predicate was verified at fire time; explicit go = the user's decided override): the implementation station was entered. Implementation absent or partial → the station skill's own artifacts and state govern the continuation; this skill re-runs no preamble.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Skipping the audit ("the discussion was thorough") | The audit IS the chain's point — the consent covers the FIRE, never the audit. A self-audit is worthless by 2nd-opinion's own thesis. |
| Firing with a non-clean state unresolved | The four-part predicate — pending user decisions included; a grill-coverage finding is a pending decision by construction. |
| The non-clean path continuing without the user's go | The exception path keeps its one ask — the stop has the user present; they fire it. |
| Firing on a plan doc edited after the audit close | The doc-state guard: the write-back is the last write — a post-audit edit voids the close (fold + disclose; substantive → ONE targeted re-audit). |
| This skill writing the test / implementing / reviewing | Sequence-and-route-only — the machinery lives in the two stations. |
| Extending the audit brief's checklist | Stock checklist fits a single unit's plan; manager's extension is for breakdown trios. |
| Re-asking lite's persistence prompt, or re-running tier checks | Step 0 persisted the doc; the I21 answer carries (both stations' skip clauses). |
| Routing critical / multi-unit / fuzzy into the lane | The sniff's exits are forced referrals — the boundaries belong to the refused skills, not to this skill's discretion. |
| Upgrading beyond spec-tdd, or stretching the ceiling on a mid-run critical discovery | The ceiling is spec-tdd; a critical discovery STOPs and refers out. |
| The too-big route becoming an ask | An announced economic route with a one-line rationale (manager S2's pattern) — the audit still gates it. |
| Resume blind-firing on an audit-only stamp | The audit stamp records items 1–2 only; the fire stamp is the predicate's on-disk proof — no fire stamp, re-verify all four at Step 2. |
| Resume redoing the audit or re-presenting a stamped clean close | Stamps are the state (I17): stamped = exists; redo nothing stamped. |
| Forgetting the stamps (audit close, fire, pipeline close) | An unstamped run is indistinguishable from never-run after `/clear`. |

## Red Flags — STOP

- About to fire the implementation station with any of the four clean conditions unmet — or unverified — on record, unless the user's explicit go is on record (the sanctioned non-clean fire).
- About to skip or self-substitute the audit dispatch (no dispatch tool → 2nd-opinion's own rule: UNAUDITED marking, the user's call).
- A critical predicate or IRREVERSIBLE shape discovered at ANY point → stop, refer out.
- About to edit the plan doc's audited content silently — amendments fold attributed, struck-through for the record (2nd-opinion's write-back shape).
- About to write an acceptance test, implement, or review personally → not this skill's job.
- About to run a second re-audit round on the same points (the bound is one — 2nd-opinion's).
