---
name: spec-tdd-coverage
description: Use when delegating test-first feature work to a subagent and you need EVIDENCE the new code is fully branch-covered — not just passing tests. Use when "good coverage" / "high coverage" matters, when weak or incomplete unit tests are a risk, or when spec-tdd's green-tests-but-no-coverage-evidence gap matters.
---

# spec-tdd-coverage

**REQUIRED BACKGROUND:** Understand `spec-tdd` first. This is spec-tdd with a coverage discipline layered on — it inherits the two-tier agent-boundary split, "must be RED first," and Phase-3 don't-trust-self-report. Only read this when you already know spec-tdd.

## Overview

spec-tdd, plus: the subagent **declares a case-list BEFORE implementing** and **reports per-class branch coverage after**; the orchestrator **gap-checks** the case-list against the impl's real branches.

**Core principle: coverage must be measured and reported evidence — never a hopeful side-effect of green tests.**

## The gap this closes

spec-tdd's handoff says *"add your own unit tests"* — no case-list, no coverage report. Observed baseline: a diligent subagent wrote **18 green tests and hit 100% branch coverage, yet reported none of it.** Coverage was *luck*, not *evidence*, and the orchestrator had no case-list to audit. A less-diligent subagent on a branchier function leaves holes with nobody the wiser — spec-tdd Phase 3 audits only the acceptance test, so unit coverage is a blind spot.

## The 3 Phases (delta vs spec-tdd in **bold**)

### Phase 1 — Orchestrator writes the acceptance test
As spec-tdd: ground it, write behavioral black-box tests, **MUST be RED**. **Note the branch/exception surface you expect** — it feeds your Phase-3 gap-check.

### Phase 2 — Delegate to subagent (extended handoff)
```
TASK: Implement {feature} so the acceptance test passes. Do NOT modify it;
if it looks wrong, STOP and report — never silently weaken it.

ACCEPTANCE TEST (RED): {file}
INTENT: {1–3 sentences}
READ FIRST: {entity/service/repo/pattern paths}

BEFORE ANY IMPL — write a CASE-LIST of every branch + boundary you will cover:
  happy path; each branch (if/loop/null-guard/early-return/catch);
  boundaries (empty, single, max, off-by-one, sign, rounding edges);
  exception/invalid/null/NaN/non-finite inputs. Return it FIRST.

DO:
1) make the acceptance test GREEN
2) write unit tests red→green, one per case
3) run the coverage tool; quote, FOR THE NEW/CHANGED CLASS(ES) ONLY
   (never whole-module): line % AND branch %, plus every uncovered line with
   a one-line justification (dead code / defensive / unreachable / SHOULD-test).
   Tools: Java → ./gradlew :Core:jacocoTestReport ;
   JS → node --test --experimental-test-coverage ; Python → pytest --cov
CIRCUIT BREAKER: if the test still fails after 3 repair attempts, STOP. Report a short structured diagnosis — tag it env/dependency (ERR-01), logic violation (ERR-02), or syntax/compile (ERR-03) — with a TRUNCATED trace and expected-vs-actual. Don't keep retrying.

RETURN: case-list + impl + unit tests + ACTUAL green output
        + per-class coverage excerpt (branch %, uncovered lines + justifications).
        Paste real output. Do not claim.
```

### Phase 3 — Orchestrator verifies
spec-tdd's checks, PLUS:
1. **GAP-CHECK** — read the impl's actual branches; confirm each has a case. Any branch with no case → add one. *(Same agent wrote case-list and impl, so this cross-context check stops a case-list that quietly mirrors the impl.)*
2. **SPOT-CHECK** the coverage excerpt against a real run — don't trust self-report.
3. **Insist on BRANCH %, not line %.** Line % can read 100% while branches are uncovered (probe: line 100% / branch 66% on the same file).
4. Surface **both** the acceptance test **and** the case-list to the user.

## Risk-tier (scale to stakes)
- **Critical path** (money / auth / data-loss): full phases + property tests + gap-check + coverage spot-check.
- **General feature**: phases 1–3 incl. case-list + coverage excerpt.
- **Throwaway / demo**: minimal — acceptance test + compile. **No case-list, no coverage burden.**

## Common Mistakes
| Mistake | Fix |
|---|---|
| Orchestrator writes the case-list | No — it belongs to the **subagent** (before impl). Orchestrator only gap-checks; dictating unit cases blurs the agent boundary. |
| Case-list written after impl | Must be **before** impl, else it's reverse-engineered to match what got built — a unit-level green lie. Require it as the first RETURN artifact. |
| Subagent quotes whole-module % | Require **per-class for NEW/changed classes only**. Whole-module % is diluted by existing untested code. |
| Trusting line % | Require **branch %**. line 100% can hide uncovered branches. |
| "100%" with no uncovered-line list | Require the list + justification **even when empty** ("none" stated, not omitted). |
| Trusting self-reported coverage | Run it yourself in Phase 3. |
| % gate incentivizes low-value tests | The **case-list** is the gate, not %. Each case must map to a real branch. |

## Red Flags — STOP
- Impl + tests returned but **no case-list**.
- Coverage excerpt shows **whole-module %** or **omits branch %**.
- **Uncovered lines with no justification.**
- Case-list appears **after** impl, or mirrors impl branches with no gap-check.
