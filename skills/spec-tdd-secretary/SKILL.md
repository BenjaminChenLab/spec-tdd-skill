---
name: spec-tdd-secretary
description: Use when the user says "spec-tdd-secretary", or wants ONE discussed non-critical unit run as a fast two-station chain — settled plan → independent plan audit (spec-2nd-opinion's machinery, verbatim) → in-session implementation (spec-tdd-lite, verbatim) — where a CLEAN audit agreement fires the implementation immediately in the same session with no fresh go-ahead ask (the invocation is the recorded consent; this skill's clean path is a standing, scoped exception to always-ask-before-implementation, disclosed in the final report). Any non-clean state (disagreement, folded amendments, pending user decisions, residual risks) stops for the user per the audit skill's own machinery. Upgrade ceiling spec-tdd — a too-big-but-non-critical unit is audited then implemented by delegated spec-tdd (an announced economic route, never an ask) with a TOP final deliverable audit after the orchestrator's verification; lite's own stall breaker promotes mid-run. Referrals OUT at entry — fuzzy requirement → grill family; critical predicate (a silent bug MOVES money / CHANGES authorization / IRREVERSIBLY corrupts data) or IRREVERSIBLE shapes → spec-tdd-escalate / spec-tdd-manager; multi-unit batch → spec-tdd's multi-unit run. NOT for the full pipeline with breakdown and gates (spec-tdd-manager), NOT for standalone plan audits (spec-2nd-opinion / spec-3rd-opinion), NOT for critical surfaces (adversarial-grade standalone runs), NOT for plain tier routing of a settled requirement (spec-tdd-escalate). Triggers on the light fast pipeline, audit then implement in one chain, secretary mode, discussed plan straight into the build.
---

# spec-tdd-secretary

**REQUIRED BACKGROUND:** Understand the `spec-tdd` family first — in particular the two stations this skill sequences: `spec-2nd-opinion` (whose machinery it runs verbatim) and the implementation tier it fires (`spec-tdd-lite` by default, `spec-tdd` on the upgrade route). This skill adds no new protocol invariant and relaxes none. It is a two-station sequencer on `spec-tdd-manager`'s sequence-and-route-only pattern, carrying ONE recorded opt-in (the clean-fire consent, below) and ONE owned mechanism on the upgrade route (the final deliverable audit, Step 3 — supervisor's final-review shape, reused). All other machinery lives in the invoked skills; this skill personally writing an acceptance test, implementing, or fixing production = an out-of-authority deformation.

## Overview

The light fast pipeline for one discussed unit: take the settled plan, run it through ONE independent TOP read-only audit (2nd-opinion's machinery), and on a **clean agreement** fire the implementation **immediately, in the same session** (lite by default) — the lite route costs two TOP dispatches (the plan audit + lite's fresh test review; the spec-tdd upgrade route costs four: plan audit + encoding audit + the MID implementer + **the final TOP deliverable audit, v1.42.0**) and zero go-ahead stops on the clean path. That is the design's whole trade: independence at the two cheapest, highest-leverage blind-spot positions (plan-level before any implementation tokens, test-strength after GREEN), with the expensive middle — delegated implementation — removed; the upgrade route adds the third position (deliverable-level after the orchestrator's own verification) so the two TOP audits bracket the implementation.

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
- Critical predicate — a silent wrong result MOVES money / CHANGES authorization / IRREVERSIBLY corrupts data (money-adjacent display/reporting does NOT qualify) — or IRREVERSIBLE shapes (DDL/migration, external contracts, security posture, money-movement semantics) → out of this pipeline: `spec-tdd-escalate` (picks the adversarial tier, its own I22 authorization ask) or `spec-tdd-manager` (the full pipeline — its entry scans carry the same ask, I22).
- A multi-unit batch or split feature → `spec-tdd`'s multi-unit run.
- You want the whole feature's pipeline (breakdown, gates, routed drivers) → `spec-tdd-manager`.
- You want the plan audited, not implemented → `spec-2nd-opinion` directly.
- You are live-testing and streaming fixes below lite's test-first cycle → `spec-tdd-quickfix` (the entry sniff suggests it; your call stands).

## Pre-flight — tier disclosure (no ask anywhere, family-wide v1.41.0)

This skill surfaces NO orchestrator-tier question — and since v1.41.0 (maintainer ruling 2026-11-25) neither does anything else in the family: every entry point's I21 check announces a non-top session in one line and never stops. The chain's two judgment-dense dispatches (the plan audit, lite's test review) are TOP-pinned by their own skills whatever the session holds, and the in-session economics — the entry sniff, the fire decision, and (on the lite route) the implementation inner loop — run on the session's model, chosen by the person who invoked it. The close report discloses the session's tier.

## Entry sniff (the routing table — every rule is an existing family boundary, none invented here)

Announce the verdict in one line + one-line rationale; every exit is a referral, the user's call stands.

- **Fuzzy** (decision gaps, or a doc that only looks settled) → ONE-line referral to the grill family. Forced: 2nd-opinion refuses fuzzy plans.
- **Critical predicate or IRREVERSIBLE shapes** → referral out (`spec-tdd-escalate` / `spec-tdd-manager`). Forced: lite refuses critical units; this pipeline's ceiling is spec-tdd, adversarial never rides it.
- **Multi-unit** (a batch, a split feature) → referral out to `spec-tdd`'s multi-unit run. Forced: lite's second-unit rule.
- **Quickfix shape** (the user is live-testing the product AND the request sits below lite's test-first cycle — a wiring/cosmetic/config swap, zero business rules, zero boundary policy; copying an existing precedent verbatim qualifies — AND outside quickfix's exclusions: money/auth/data-loss logic, anything needing an acceptance test) → ONE-line suggestion to exit to `spec-tdd-quickfix`; continue on the user's word.
- **ONE non-critical unit** → in lane. Size call (an economic route, announced never asked — manager S2's pattern): fits lite (small/medium, a session you'll clear after) → **the implementation station = lite** (the default); too big for lite but single and non-critical → **the implementation station = spec-tdd** (the upgrade ceiling) — the audit still runs first either way.

## Step 0 — persist the plan

The audit's precondition is a plan on disk (I17: settled only in conversation = not auditable). Plan already a doc → use it. Conversation-only → persist it now per project convention (family default `docs/specs/YYYY-MM-DD-<feature>.md`), announced in one line — this same doc satisfies lite's Phase-1 persistence (auto-persisted family-wide; there is no prompt to fire, v1.41.0). Pending user decisions, if any, are enumerated as pending, never silently defaulted.

## Step 1 — the audit station

Run `spec-2nd-opinion` **verbatim**: brief assembly (its Step 1 — background with evidence, the plan as-is, falsifiable claims, its checklist, output format, the standing file-tools rule), the ONE read-only TOP background dispatch (its death/re-dispatch rules), the merge-and-gate (its Step 3), and the write-back. Then one addition of this skill's own (manager S4's resume discipline, reused): the **close stamp** — a line in the plan doc, "per audit (spec-2nd-opinion, YYYY-MM-DD): agreed, no amendments" (with amendments, the write-back itself is the on-disk trace).

**No checklist extension.** Manager extends the brief with decomposition dimensions because it audits a breakdown trio; this pipeline audits ONE unit's plan — the stock checklist (claims, drift, interactions, ordering, the unlisted-risk probe, grill coverage) fits as-is.

## Step 2 — the fire decision (the one mechanism this skill owns)

**The doc-state guard (both paths):** before any fire, the plan doc must sit exactly as the audit left it — the write-back (or the clean close) is the last write. A post-audit edit — yours or the user's — voids the close: fold it per the write-back shape and disclose; a substantive change (touching audited claims) takes 2nd-opinion's ONE targeted re-audit bound. Never fire on an unaudited edit (manager Gate 2's amend-and-fold moment, restated for the unattended gap between audit and fire).

- **Clean (all four predicate items on record)** → ONE-line announcement — audit clean, firing the implementation station now, per the invocation consent — then append the **fire stamp** to the plan doc ("implementation fired (YYYY-MM-DD, lite|spec-tdd): clean-fire consent — predicate verified (endorse / 0 amendments / 0 pending / 0 residual)") and proceed to Step 3 immediately. No ask. The consent's disclosure lands in the close report.
- **Non-clean (any miss)** → 2nd-opinion's own machinery carries: per-point arbitration with stated reasons, user-owned items surfaced to the user, ONE targeted re-audit on amended points (the bound is one round). After resolution, the fire decision is the user's once — the stop has them present; they say go, the fire stamp records "explicit go" in place of the consent, and Step 3 fires.

## Step 3 — the implementation station

Invoke the routed skill **verbatim**; this skill owns none of its asks (its SPEC-bucket questions, its exit rules, its final surface-WHAT report — all its own) and adds exactly one thing to a station's run — the final deliverable audit on the upgrade route below:

- **Default — `spec-tdd-lite`**: Phase 1 writes the acceptance test against the persisted spec doc (RED; persistence already satisfied by Step 0), Phase 2 implements in-session, Phase 3 dispatches the fresh TOP test review (the second of the chain's two dispatches). Its exit rules govern: solo re-RED, the SPEC-DEFECT sweep, the stall breaker. **Nothing is added on this route** — its tail already carries the fresh-context review.
- **Upgrade route — `spec-tdd`** (entry-sniffed too-big, or lite's stall breaker promoting mid-run): its three-phase machinery (acceptance test → delegated implementer → orchestrator verification) runs unchanged, **plus the final deliverable audit below** — this route's tail otherwise has no fresh-context dispatch (the orchestrator's own Phase-3 verification is mechanical: re-run, re-hash, sweep), and the implementation diff would go to the close unread by any context other than the one that wrote the test. This is the ceiling — never beyond spec-tdd on this pipeline.
- **A critical surface discovered mid-run** (the litmus hits during implementation, on either route) → STOP and refer out — lite refuses critical units and so does this pipeline; the ceiling does not stretch.

**The final deliverable audit (upgrade route only; v1.42.0 — supervisor's final-review shape on spec-tdd's machinery, the one addition this skill makes to a station's run).** Runs AFTER spec-tdd's Phase 3 steps 1–6 pass (hash pair equal, orchestrator's own re-run GREEN, sweep clean, compile + relevant suite green) and BEFORE the close stamp:

- **Dispatch spec**: **TOP**-pinned (I19(a) — a review dispatch), read-only, background mode; at dispatch announce in one line what is being audited and that results arrive by notification — and until the notification arrives, know nothing about the findings (no reporting, no predicting). A dispatch that shows failed or sits silent past a coarse bound (read-only deliverable audits run minutes-to-tens) gets **ONE fresh re-dispatch** (nothing inherited), disclosed; still nothing → report the stall. **No dispatch tool available** → no silent self-audit: the close report marks the deliverable **UNAUDITED** (the orchestrator's own Phase-3 verification stands as the only verification; whether that suffices is the user's call, I12).
- **Brief = fixed checklist + doc paths, no summaries, no pre-digestion** (I19(c) — the framing power stays out of the authoring session's hands): the persisted plan/spec doc path, the acceptance test path, the implementer's RETURN report or scratch run log path, the JUnit XML directory, the created/modified file list, the hash pair, the production diff (`git diff` output written to a scratch file, path handed over — never pasted into the brief), **the absolute path of `FINAL-AUDIT.md`** (`.spec-tdd/<feature>/FINAL-AUDIT.md`, SCRATCH ROOT pasted verbatim — the auditor's only write target, never self-composed), plus the standing file-tools rule verbatim — local files are read ONLY with Read/Glob/Grep (Bash cat as fallback); NEVER open file:// URLs with any browser tool (Playwright MCP, webReader, or similar); if native file tools seem missing or unloadable, STOP and report back 'missing file tools' — never improvise with a browser (dispatched contexts receive no global CLAUDE.md — the brief is the carrier).
- **Auditor checklist (three items, fixed order; item a is the main course — the encoding audit already ran pre-dispatch on this route):**
  - a. **Impl diff correctness + fidelity to the requirement (I15's sweep at deliverable grade)**: does the production diff do what the spec doc says, no more (accommodations of test defects, logic beyond the spec, bent existing code) and no less; is every change inside the deliverable scope; name one wrong-but-plausible implementation the GREEN tests would still let through.
  - b. **Disclosure consistency**: the implementer's notable decisions, the orchestrator's test corrections, locally ruled details — each reasonable alone, but **together** do they contradict the requirement or the audited plan?
  - c. **Encoding-fidelity delta re-read** (bounded — the pre-dispatch TOP encoding audit is the full check; this item only re-examines a test the orchestrator edited during Phase 3): if the test was strengthened or corrected after the encoding audit, does the edited part still carry discriminating power; a test untouched since the audit → one-line "untouched, audit stands".
- **Output and evidence rules**: findings' full text to `FINAL-AUDIT.md` + a returned summary; every finding carries `file:line` evidence; every "OK" names the attack tried (I16 — an OK without an attempted counterexample is a rubber stamp). The auditor reads the XML numbers (path in the brief) but **never re-runs compiles** — that is the orchestrator's machinery, already run.
- **Arbitration (once findings arrive)**: **default-adopt**; a rejection must carry the evidence the auditor lacked and **surface to the user** — the session never silently overrules a TOP auditor; ambiguities depending on grilling intent that the doc doesn't carry → always up to the user (I12 — the auditor sees only the doc).
- **Findings loop (one fix round → delta re-check; the I16 bound)**: a finding routes through spec-tdd's own I10 three buckets (SPEC → the requirement re-opens, the user's call; TEST → the orchestrator strengthens the test, re-RED; IMPL → **a continuation implementer dispatch**, keep-don't-rewrite, the finding + evidence in its brief — the orchestrator never fixes production by hand, the agent boundary stands); the fix lands and the orchestrator's Phase-3 items re-run on the delta → **the SAME auditor** re-checks the delta (SendMessage — the adoption check needs memory); only when the auditor is unresumable, a fresh auditor re-reads everything from `FINAL-AUDIT.md` (one extra read, disclosed). **Bound: one fix round**; not converged → escalate to the user with both sides' evidence; no infinite loop. A clean audit (zero findings) → no round, straight to the close.
- **Costs disclosed in the close report**: the final TOP audit dispatch (+ any death re-dispatch, delta re-check, or UNAUDITED marking), the findings count and their disposal, residual risks.

## Close — stamps and resume

After the station's exit, append the close stamp — "secretary pipeline closed (YYYY-MM-DD): audited spec-2nd-opinion, implemented lite|spec-tdd" — and deliver the close report: the station's own final report **plus one line disclosing that the run was fired on the clean-fire consent** (when it was) **and the session's tier** (no tier ask exists — I21 discloses family-wide, v1.41.0); **on the upgrade route, plus the final-audit disclosure** (the TOP dispatch, any death re-dispatch / delta re-check, findings count and disposal, residual risks — or the UNAUDITED marking when no dispatch was possible). A run leaving no on-disk trace is byte-identical to never-run after `/clear` — the stamps are the resume state:

- **Audit stamp only, no fire stamp** → the session died between the audit close and the fire decision: re-enter Step 2 and verify the four predicate items from the doc (the write-back, the pending-decisions section) — the audit stamp alone covers only items 1–2; never blind-fire on it. Nothing re-audited.
- **Fire stamp present** → the fire basis is on record (clean-consent = the predicate was verified at fire time; explicit go = the user's decided override): the implementation station was entered. Implementation absent or partial → the station skill's own artifacts and state govern the continuation; this skill re-runs no preamble. **On the upgrade route, a fire stamp with no close stamp → check `FINAL-AUDIT.md`**: present with findings disposed → only the close remains; present with findings open → resume at the findings loop (the SAME auditor re-checks, never a fresh full audit); absent → the station's own Phase-3 state decides whether the audit dispatches now or the implementation finishes first — never skip it, never redo a completed audit.

## Common Mistakes

| Mistake | Fix |
|---|---|
| The upgrade route closing on the orchestrator's own verification alone ("Phase 3 already re-ran everything") | The final deliverable audit is the upgrade route's third TOP position (v1.42.0) — the orchestrator's Phase 3 is mechanical and same-context; the implementation diff goes to no other reader without it. No dispatch tool → UNAUDITED marking, the user's call. |
| The orchestrator fixing a final-audit finding by hand | The agent boundary stands — IMPL findings ride a continuation implementer dispatch (keep-don't-rewrite), then the SAME auditor re-checks the delta; one round, then the user. |
| Writing summaries or expected verdicts into the final-audit brief | Fixed checklist + doc paths (I19(c)) — the diff as a scratch file, never pasted; a summary hands the auditor the author's framing. |
| Resume redoing a completed final audit, or skipping it because Phase 3 passed | `FINAL-AUDIT.md` is the state: findings disposed → close; open → the findings loop; absent → dispatch it after Phase 3. Stamped = exists. |
| Skipping the audit ("the discussion was thorough") | The audit IS the chain's point — the consent covers the FIRE, never the audit. A self-audit is worthless by 2nd-opinion's own thesis. |
| Firing with a non-clean state unresolved | The four-part predicate — pending user decisions included; a grill-coverage finding is a pending decision by construction. |
| The non-clean path continuing without the user's go | The exception path keeps its one ask — the stop has the user present; they fire it. |
| Firing on a plan doc edited after the audit close | The doc-state guard: the write-back is the last write — a post-audit edit voids the close (fold + disclose; substantive → ONE targeted re-audit). |
| This skill writing the test / implementing / fixing production by hand | Sequence-and-route-only — the machinery lives in the two stations; the one thing this skill owns is the upgrade route's final audit dispatch, and its findings ride the stations (a continuation implementer), never the session's own hands. |
| Extending the audit brief's checklist | Stock checklist fits a single unit's plan; manager's extension is for breakdown trios. |
| Re-asking lite's persistence, or either station's tier check | Step 0 persisted the doc (persistence is automatic family-wide, v1.41.0) and the tier check never asks — there is nothing to re-ask. |
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
- About to close the upgrade route with the implementation diff read by no context but its author's — the final deliverable audit runs after Phase 3, or the close report says UNAUDITED (v1.42.0).
