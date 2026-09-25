---
name: spec-tdd-quickfix
description: Use when the user is LIVE-TESTING the product (UAT, live field testing) and streaming small fix requests — "quick fix", "small tweak", "change a word here" — one at a time or a handful, while they keep testing. Triggers on time-pressed small defects, cosmetic/string/config tweaks, wiring restorations too small for spec-tdd-lite's write-test-first cycle. NOT for anything needing an acceptance test.
---

# spec-tdd-quickfix

**REQUIRED BACKGROUND:** the `spec-tdd` family — `spec-tdd-lite` in particular (the tier directly above this one). This skill is the family's **floor tier**: below lite, below every test-first cycle.

## Overview

The user is testing the product and finding small defects in real time. Speed is the requirement; **the user's own live testing is the acceptance net** — that is what makes skipping test-first honest rather than a green lie. The orchestrator:

1. **One-sentence fix plan first, never code** — file + intent. The user's "go" is the only gate (their standing never-code-before-approval rule; there is no doc, no Gate 2).
2. **Dispatches ONE subagent per fix (MID tier, stated on the dispatch — I19).** Brief = scope fence (exact files/regions) + decisions already made (the agent must NOT re-litigate; unknowns → report, never guess-code).
3. **Verifies personally** — reads every hunk of the diff, compiles, and per the tiering below may re-run scoped tests. NEVER trusts the agent's self-report.

**What this gives up vs `spec-tdd-lite` (honest):** no acceptance test, no fresh-context review dispatch, no RED evidence. The substitutes: the orchestrator's personal diff read + the user's live testing. **Disclose this in the final report** — "quickfix tier: diff review + your testing stood in for the family's audit machinery" — never let it pass silently as a full-verification run.

## When to Use / NOT

- Use: the user is live-testing and streams a small fix request (string/cosmetic/config swap, small wiring, tiny defect) where "the original modes are all too slow".
- NOT: anything touching money/auth/data-loss logic → `spec-tdd-adversarial`; anything where a wrong-but-green result could hide → `spec-tdd-lite` and up; a settled requirement needing a tier picked → `spec-tdd-escalate`; feature-grade or multi-task work → `spec-tdd-manager`.
- **Escape valve:** mid-fix it turns out NOT to be small (structural change, new behavior needing test design, blast-radius surface) → stop, leave the quickfix lane, route that one fix to lite or above. The lane must never be the excuse for the upgrade-dodge.

## Tiered verification (the floor, per fix)

- **Text/config-only change** (strings, labels, config values): compile + orchestrator's full diff read. Done.
- **Logic touch** (any branch, boundary, or data-shaping line): additionally re-run the scoped `--tests` for the touched class(es) AFTER the agent is down (build contention; the agent was told to wait — so must you).

## The dispatch brief (every fix)

- Scope fence: exact files/regions it may touch; **hard hands-off list** for anything else in flight in the tree.
- Pinned decisions from the one-sentence plan; unknowns → report, never guess-code.
- Standing discipline: NO git of any kind (the orchestrator commits per fix only on explicit user go, explicit paths, never `-A`); gradle lock = wait, never kill daemons; build/test output redirected to a file (pipes swallow exit codes); foreign compile failures = wait 90s ×2 then report honestly; comments in English, report in the user's language.
- Report format: files + line anchors, what was changed, problems seen but not touched.

## Parallel (only when it actually happens)

Multiple live requests whose touched-file sets are disjoint → dispatch concurrently. Any shared file: max 2 concurrent editors, each brief saying "re-Read the file immediately before EVERY edit; an Edit failure means someone else changed it — re-Read and retry once, then report"; same region or a not-yet-landed dependency → queue behind the other's completion.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Quickfix used for a logic change with no scoped test | Tiered floor: logic touch → scoped test re-run, personally. |
| Trusting the agent's "done, green" | Read every hunk yourself; verify compile/test output you ran or re-ran. |
| Fix grows mid-flight, agent keeps grinding | Escape valve: stop, re-route that fix to lite or above. |
| Ticket doc / plan doc written anyway | The one-sentence plan + the user's go IS the gate. Docs here are overhead, not safety. |
| Commit by the agent or `-A` commit | NO git for agents; orchestrator commits per explicit user go, explicit paths only. |
| Quickfix presented as a fully-verified run | Disclose the substitution (diff read + user's testing) in the final report. |
