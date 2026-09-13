---
name: spec-tdd-escalate
description: Use when the user says "spec-tdd-escalate", or has a SETTLED requirement (plan/spec/design doc already locked — no grilling wanted) and wants the spec-tdd tier picked for them automatically. Triggers on requirement-already-decided, auto-pick tier, skip grilling, route to spec-tdd-lite / spec-tdd / spec-tdd-coverage / spec-tdd-adversarial.
---

# spec-tdd-escalate

**REQUIRED BACKGROUND:** You MUST understand the `spec-tdd` family first — `spec-tdd` (general), `spec-tdd-coverage` (branch-coverage evidence), `spec-tdd-adversarial` (correctness-critical: money/auth/data-loss, independent attacker), and `spec-tdd-lite` (in-session: one small non-critical unit, no delegation). This skill is the **no-grill front-end**: it only routes.

## Overview

The requirement is already settled (a locked plan, spec, or doc). Your ENTIRE job is to **run the I21 pre-flight (below), read it, run the fuzziness sniff, pick the tier that fits the stakes, and invoke that tier by name.** Then stop.

**Core principle: route-only.** You do NOT grill, do NOT write the acceptance test, do NOT delegate, do NOT gate. The tier you invoke runs its own Phase 1 (it writes the test) and executes from there — the delegated tiers dispatch an implementer; `spec-tdd-lite` implements in-session. Escalate adds exactly four things over calling a tier directly: **the machine picks the tier, the I21 pre-flight refuses to run this protocol on a non-top-tier orchestrator unheard, the fuzziness sniff refuses to silently route a doc that only looks settled, and the top tier costs a confirmation — a computed `spec-tdd-adversarial` route stops for ONE ask before invoking** (the family's most expensive run never launches on a machine's say-so alone) — a clean doc never triggers the sniff's question.

> Sibling front-end: `grill-spec-tdd` = requirement FUZZY → grill + gate the spec + write the test from the final spec + route. **escalate = requirement SETTLED → route only.** If you'd need to interrogate, you're in grill-spec-tdd territory, not here. (The sniff's single grill-or-route ask and I21's tier-check pre-flight excepted.)

## When to Use
- User says `spec-tdd-escalate <feature>`.
- Requirement is already locked (plan / design doc / crisp ticket) and the user wants it routed automatically.
- User explicitly does NOT want to pick the tier or be asked ("just pick the right one and go").

**When NOT to use** — route elsewhere:
- Requirement is fuzzy / ambiguous / missing dimensions → `grill-spec-tdd` (grill first); fuzzy AND blast-radius-critical (the adversarial tier's predicate) → `adversarial-grill-spec-tdd` (grill + independent audits: decisions pre-gate, test pre-dispatch). A user who answers the sniff's ask with "settled, route" wins — route per their call (I12), passing the flagged gaps along.
- You (or the user) already know which tier → invoke that tier directly. Escalate exists for "you decide for me"; if the decision is made, escalate adds nothing.

## Pre-flight — orchestrator tier check (I21)

Before any work, check the model THIS session runs as. A run's judgment — the test/spec, the verification, the failure routing — executes entirely in the orchestrator's own context; I19 pins every dispatch tier, but nothing can upgrade the session itself. **Top tier in use, or no higher tier exists → silent, move on.** Otherwise surface this ONE ask and stop for the answer:

> ⚠ **Orchestrator tier check** — this session runs a non-top model, and a run's planning / verification / routing all execute on it. **Upgrade** → run `/model`, pick the top tier, say "go" (the same conversation continues). **Ignore** → continue at this tier; the decline is disclosed in the final report.

Arrived from a front-end that already surfaced this check? Skip it — never re-ask (a handoff-recorded decline rides into your final-report disclosure).

## Before routing — the fuzziness sniff (one read, zero dispatches)
**"Settled" must mean decided.** Before invoking the tier, scan the requirement/doc for decision-shaped gaps it never closed:
- **Unbound quantities** — a limit/threshold/timeout/retry-count/batch-size named but never numbered ("a reasonable timeout", "retry a few times").
- **Unchosen options** — an either/or named with no pick ("email or SMS", "queue or direct write", "truncate or reject").
- **Escape-hatch wording** — "as appropriate" / "if needed" / "properly" / "handle gracefully" sitting over behavior this feature owns.
- **TODO / TBD / placeholder markers** anywhere in scope.

**Clean → route silently** (the sniff is not a gate — the only ask a clean doc can still draw is I21's pre-flight above, on a non-top session). **Gaps found → ONE ask:** "these look undecided — `grill-spec-tdd` first, or treat as settled and route?" The user's "settled, route" wins (their call, I12); pass the flagged gaps along so the tier's Phase 1 sees them. A doc that can't survive the sniff isn't settled — routing it anyway just moves the grilling downstream to where it costs dispatches.

## The route (pick by stakes and size, then invoke by name)

| Signal in the requirement | Invoke |
|---|---|
| Blast-radius-CRITICAL: a silent wrong result MOVES money, CHANGES authorization, or IRREVERSIBLY corrupts data (money movement / auth-permissions / data-loss-data-integrity logic itself; equivalently the unit's decisions carry an IRREVERSIBLE blast-radius tag) | `spec-tdd-adversarial` (confirm first — the ask below) |
| Needs branch-coverage EVIDENCE: concurrency, parsing, state machines, large/subtle branch surface, weak-unit-test risk, compliance proof | `spec-tdd-coverage` |
| ONE small unit — a single bugfix-scale item or small refactor, non-critical, session will be cleared after (one dispatch costs more than it saves) | `spec-tdd-lite` |
| Multiple units — a bug list, or a feature split into slices | `spec-tdd` (**multi-unit run**) |
| Anything else (incl. larger refactors / no behavior change) | `spec-tdd` (default) |

**Computed `spec-tdd-adversarial` → STOP and ask first — a cost gate, not a stake re-litigation.** Adversarial is the family's most expensive run (independent attack rounds, hours-level depth), and its predicate has a known over-trigger (money-adjacent misread as money-movement). Escalate is the family's only SILENT adversarial launcher — the grill front-ends surface the routing choice at their spec gates, and a direct tier invocation is the user's own pick. Before invoking it, surface ONE ask carrying the stakes basis in one line: **Confirm** → invoke `spec-tdd-adversarial`; **Downgrade** → the named alternative is `spec-tdd-coverage` (the band directly below — branch evidence, no attacker), disclosed in the final report; any other call the user makes wins (I12). This is the only ask a clean critical doc draws. A dispatched context with no user reach never invokes adversarial from here: the task-loop/dag tier band caps in-loop routing at coverage (above-coverage stakes hit the routing-point STOP long before invocation), and any other dispatched escalate that cannot ask stops and reports up — the report IS the ask, relayed by the top.

A blast-radius-critical feature that is ALSO branchy (e.g. money math with concurrency) goes to `spec-tdd-adversarial` — it's the top tier and subsumes coverage. **Money-adjacent is NOT money-movement** (the over-routing trap — observed: a fintech codebase routed nearly everything here): display / reporting / reference data / internal tooling that READ the money system but cannot corrupt it → `spec-tdd-coverage` (branchy/compliance) or `spec-tdd`. A pre-settlement safety net (reconciliation, monitoring, dual-control) bounds the blast radius → one tier down. Multi-unit batches route PER UNIT — the payments batch's movement units adversarial, its statement/display units coverage.

**Invoke the chosen tier via the Skill tool, BY NAME.** Do NOT search the filesystem for `SKILL.md`, do NOT wonder how the skills are organized — skills load by name.

## Common Mistakes
| Mistake | Fix |
|---|---|
| Writes the acceptance test itself | Route-only — the invoked tier writes it in its own Phase 1. Writing it yourself collapses the agent boundary and duplicates grill-spec-tdd. |
| Grills a settled requirement ("I need to confirm X first") | Route up instead. The requirement is settled; an unconfirmed-but-risky dimension is a **routing signal, not a grill trigger** (adversarial for security/auth, coverage for branchy logic). |
| Asks "should I proceed?" / gates before invoking | Full-auto below the top tier — the user chose auto-routing so they don't decide. Announce the tier + a ONE-line stakes reason, then invoke. Not a briefing. (Three carved-out asks, all routing hygiene: the sniff's "grill or route?" on an undecided doc, I21's orchestrator tier check, and the top-tier confirmation when the machine computes adversarial — a cost gate on the family's most expensive run, never a stake re-litigation.) |
| Over-thinks and exits the family ("just a refactor, I'll just do it") | Always pick one of the four. Small refactor → `spec-tdd-lite`; larger refactor / no behavior change → `spec-tdd` (base). Don't invent a fifth path. |
| Starts planning the implementation / writing characterization tests | Job ends the instant you invoke the tier. |
| Briefs the tier on HOW — test ideas, attacker seeds, property invariants | Pass the RAW requirement; let the tier form its own Phase-1 plan. Pre-digesting contaminates the tier's independent judgment (the agent-boundary principle). |
| Routes a money/auth/data-loss feature to base `spec-tdd` | That's correctness-critical → `spec-tdd-adversarial`. |
| Routes a bug list to `spec-tdd-lite` ×N — or one mega-dispatch of every unit | Multiple units = `spec-tdd` **multi-unit run** — the boundary is per unit. |
| Hunts the disk for a tier's `SKILL.md` | Invoke by name via the Skill tool. |
| Routed a "settled" doc carrying open decision gaps (unnumbered limits, unchosen options, TODO markers) | The fuzziness sniff catches them pre-route: surface the gaps in ONE ask (grill or route); the user's "settled" wins and the flags ride the handoff. Absorbing the gaps silently is the failure. |

## Red Flags — STOP
- You're about to write an acceptance test, grill the user, or ask "proceed?" — none of these are escalate's job. (Three exceptions, all routing hygiene, never a grill question: the sniff's ONE "grill or route?" ask, I21's orchestrator tier check, and the adversarial confirmation.)
- About to invoke a tier with sniff findings unresolved and no user "settled" on record.
- You invoked `spec-tdd-adversarial` with no user confirm on record — the one tier that never launches on the machine's say-so alone.
- You're planning the implementation, writing scaffolding tests, OR briefing the tier on how to test (seeding attacker strategies, suggesting property invariants) — you've gone past routing. Pass the raw requirement and stop.
- You picked a tier other than the four, or "none, I'll just do it."
- You can't even tell the stakes because the requirement is too vague — that means the user should have used `grill-spec-tdd`; say so and stop, don't guess-route.
