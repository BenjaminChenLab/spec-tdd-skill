---
name: spec-tdd-lite
description: Use when the user says "spec-tdd-lite", or wants test-first development WITHOUT delegating to a subagent — ONE small/medium non-critical unit (a single feature, bugfix, or refactor) in a session you'll clear after, where full spec-tdd is overkill but shallow same-context tests are still a risk. Triggers on in-session acceptance-test-first, "too small for spec-tdd", light tier, quick feature work with green-lie risk.
---

# spec-tdd-lite

**REQUIRED BACKGROUND:** Understand the `spec-tdd` family first — `spec-tdd` in particular (acceptance-test-first, must-be-RED, the green lie). This skill is the family's **in-session tier**: the same discipline with zero delegation, plus ONE fresh-context review dispatch.

## Overview

The acceptance test (the spec) is written **before any impl exists**, then implemented **in the same session**, then — after GREEN — **one subagent that never saw the implementation reviews the test**: could it stay green under a subtly-wrong impl, and does it assert the requirement?

**Core principle:** written-first blocks the test mirroring the impl; the fresh-context review blocks the shallow assertion. Those are the two green-lie vectors — covered at a fraction of full `spec-tdd`'s cost.

**What this gives up vs `spec-tdd` (honest):** no fresh implementer re-reading your spec (a misread requirement can sail green — the review's test-vs-requirement question is the mitigation), no SPEC-INTEGRITY hash (test immutability here is the solo re-RED discipline, not structure), and the inner loop stays in your main context — pollution is the price; budget a clear/compact after the session's work.

## The gap this closes

Observed baseline: a diligent plain-TDD agent, on a small coupon feature, shipped a 6/6-green suite in which (a) "written first, failed first" was an **unverifiable self-report**; (b) an ambiguous requirement line ("integer 0–100; outside that range → throw") was silently interpreted ("non-integers also throw — a reasonable strict reading") and **self-approved**, never surfaced; (c) a mutation check — deleting the never-below-0 guard — **kept the suite green**: the requirement's assertion had zero discriminating power; (d) nothing was shown to the human. Green, diligent — and still an unverifiable claim, a self-approved interpretation, and a vacuous assertion, with no human checkpoint. Lite exists for exactly this: one unit too small to delegate, too exposed for bare TDD.

## When to Use
- User says `spec-tdd-lite <feature>`.
- ONE small/medium non-critical unit — no money/auth/data-loss surface, no branch-coverage-evidence demand — in a session you'll clear/compact after (the inner loop lives in the main context **by design**). A SECOND unit in the same session → stop liting: switch to `spec-tdd` multi-unit (delegation is what keeps the main context clean).
- Routed here from `grill-spec-tdd` / `spec-tdd-escalate`: same rules; you are the tier now.

**When NOT to use** — correctness-critical → `spec-tdd-adversarial`; need coverage evidence → `spec-tdd-coverage`; the work is big enough that delegation pays for itself → `spec-tdd`.

## Phase 1 — Write the acceptance test
> **Arrived from `grill-spec-tdd`?** The acceptance test is already written and RED — skip this phase, start at Phase 2 (keep the grill's interpretation notes; Phase 3 re-examines them).

As `spec-tdd` Phase 1: ground it in the real architecture; behavioral black-box (WHAT, not HOW); run it — **MUST be RED** (a not-yet-existing module erroring is a valid first RED; GREEN is the only invalid state). **RED-purity check:** scan the FULL error list, not just the tail — every error must point at symbols the feature will create; any error about EXISTING symbols (wrong constructor arity, ambiguous method overloads, unused imports) is a defect in YOUR test, not feature absence. Fix the test before implementing — a defective RED masquerades as "feature missing" and you will bend the impl to accommodate it. Domain logic: add 1–3 property/invariant tests. **Write down every interpretation you make of ambiguous requirement wording** — Phase 3 re-examines them.

## Phase 2 — Implement in-session (inner loop)
Unit tests one at a time, red→green:
- **RED verified personally, failing for the right reason.** A RED round you did not watch fail is void — an unverified ordering *claim* is the baseline failure, not evidence.
- Minimal code to GREEN. Test fails → fix the code, not the test.
- **Test-defect exception (SPEC-DEFECT):** if the failure comes from a defect in the TEST itself — wrong constructor arity, ambiguous overload matchers, unused stubs under strict stubs, assertions contradicting the requirement — fix the TEST, never bend production to make a defective test compile or pass (no compat constructors, no renamed public methods, no logic beyond the spec). Bending production to a test defect = a failed run.
- Refactor only while green.

## Phase 3 — Fresh-context test review (the one structural check)
Dispatch ONE subagent that has seen none of your reasoning:

```
REVIEW an acceptance test you did NOT write and must not trust.
Acceptance test: {file}
REQUIREMENT (verbatim, do not paraphrase): {paste}
Impl (may read, to judge what's tested — the TEST is the subject): {paths}

Answer two questions with concrete cases:
1. TEST vs IMPL — name a subtly-WRONG implementation that still passes every test,
   or show none exists. Probe untested dimensions: boundaries, error paths, input shapes,
   assertions with no discriminating power (would fail nothing if the requirement were violated).
2. TEST vs REQUIREMENT — does every requirement line have an assertion? List: vacuously-tested
   requirements, silent interpretations the author made that a human should confirm, missing lines.

RETURN: findings list (missing case / vacuous assertion / silent interpretation / none).
Do NOT edit any file.
```

**No dispatch tool available** (you are running inside a subagent — lite normally runs in the main session)? Degraded mode, and it must be disclosed: run Q1 as concrete mutation checks (break the impl, re-run, expect RED) and Q2 as a line-by-line audit against the pasted requirement — then state in the final report that the review was **same-context, not fresh-context**. A silent improvised review is worse than a disclosed degraded one.

Then, in session: **verify each finding yourself** (re-run; don't trust the report either) → strengthen the test → **re-confirm RED** — a strengthening that cannot go RED has no teeth; rewrite it → repair the impl → GREEN. A finding that is really a *requirement* question → ask the human (SPEC bucket); never resolve it alone.

## Exit rules
- **Solo re-RED.** ANY acceptance-test edit after impl exists must be re-confirmed RED before it counts. This replaces the hash — it is discipline, not structure. Honor it.
- **Stall breaker.** 3 failed repair attempts, OR the same root cause twice → stop in-session work and **promote to full `spec-tdd`** (delegation is the forced fresh context) or surface to the human.
- **SPEC-DEFECT sweep.** Before reporting done, diff your production changes against the spec: any change the spec cannot trace (helper/compat constructors, renamed public methods, logic beyond spec scope) is an accommodation of a test defect — fix the test (solo re-RED applies), restore production to the spec'd shape.
- **Surface WHAT.** End by showing the user the acceptance test + the review findings summary. The human validates WHAT; you validated HOW.

## Common Mistakes
| Mistake | Fix |
|---|---|
| Skip Phase 3 — "tests are green, done" | Green proves nothing about test *strength*. The review is the only structural check lite has; the baseline's vacuous assertion was green too. |
| Hand the reviewer YOUR summary of the requirement | Paste the requirement verbatim. Your summary launders your interpretations — exactly what Q2 hunts. |
| Strengthen the test but skip re-RED | A strengthening that stays instantly green is vacuous — rewrite until it can fail for the right reason. |
| Edit the acceptance test to make it pass | Solo re-RED: every post-impl edit re-confirms RED or reverts. |
| Reads only the tail of the RED error list | Full-list RED-purity check: errors about EXISTING symbols (wrong ctor arity, ambiguous overloads, unused imports) = your test's defect — fix it before implementing. |
| Mid-loop failure turns out to be a test defect → bent the impl to make it compile/pass | That's SPEC-DEFECT: fix the TEST (no compat constructors, no renamed methods); the exit-rule sweep double-checks the diff before you report done. |
| Resolve an ambiguous requirement alone | Baseline failure #2. Ask the human — the reviewer surfaces it, the human decides it. |
| Grind a stuck repair loop | Stall breaker fires → promote to `spec-tdd` or ask. |
| Lite ×N in one session (a bug list, a batch of small items) | Pollution scales with N. The second unit belongs to a `spec-tdd` multi-unit run. |
| Lite on a money/auth/data-loss feature | Wrong tier — `spec-tdd-adversarial`. |

## Red Flags — STOP
- About to report done with no Phase-3 review on record (dispatch, or a disclosed degraded mode).
- Reviewer returned "none" and you wrote the test yourself — re-read its two questions; "none" is earned by concrete probes, never assumed.
- You are silently interpreting an ambiguous requirement the review hasn't surfaced.
