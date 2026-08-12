---
name: spec-tdd-adversarial
description: Use when implementing a correctness-CRITICAL feature (money movement, auth/permissions, data-loss or data-integrity surface) where a subtle bug means real loss and maximum rigor is worth the token cost — the highest tier above spec-tdd and spec-tdd-coverage. Triggers on critical-path, no-cost-for-correctness, hardening acceptance tests against independent attack, "this cannot be wrong".
---

# spec-tdd-adversarial

**REQUIRED BACKGROUND:** Understand `spec-tdd` and `spec-tdd-coverage` first. This is spec-tdd-coverage with a mandatory independent ATTACKER layered on — it inherits the two-tier agent-boundary split, "must be RED first," the case-list, per-class branch coverage, and Phase-3 don't-trust-self-report.

## Overview

spec-tdd-coverage, plus: an **independent adversarial subagent** — a *third* context, not the orchestrator, not the implementer — tries to (a) write a subtly-WRONG impl that still passes the acceptance test, and (b) independently gap-check every branch of the real impl. Property/invariant tests become **mandatory**.

**Core principle: independence is the one thing a diligent same-context agent cannot give itself.** A baseline agent told "maximum rigor, spare no cost" wrote 30 scenario tests, a differential-oracle fuzz harness that caught a real bug, and an "adversarial self-review" — all excellent, all in ONE context. It never dispatched an independent attacker; that move is non-obvious. spec-tdd-coverage's Phase-3 checks run in the orchestrator's context (biased to rubber-stamp its own test), and the implementer's unit tests share context with the impl. An independent attacker removes both biases.

**The acceptance test is done when the attacker can no longer construct a wrong-but-green impl** — bounded by the **attack-loop circuit breaker** (3 rounds, or the same hole twice): a critical surface is rich enough that "no wrong-but-green impl exists" may never hold, so past the breaker you surface the residual risk to the human instead of looping. Until then, it isn't "clean done" — but it can be "done enough to ship, pending human accept".

## When to Use
- Critical path ONLY: money movement, auth/permissions, data-loss or data-integrity surface.
- The user says `spec-tdd-adversarial`, "no cost for correctness," or "this cannot be wrong."
- Otherwise use `spec-tdd` (general) or `spec-tdd-coverage` (coverage matters). This tier dispatches multiple agents per feature — don't burn it on glue/CRUD.

## The 3 Phases (delta vs spec-tdd-coverage in **bold**)

### Phase 1 — Orchestrator writes the acceptance test
> **Arrived from `grill-spec-tdd`?** The acceptance test is already written and RED — skip to Phase 2, but ENSURE the mandatory property/differential tests below exist (add them if grill-spec-tdd didn't).

As spec-tdd-coverage: ground it, behavioral black-box, MUST be RED, note the branch/exception surface. PLUS:
- **Property/invariant tests are MANDATORY** (money conservation, net-zero, monotonicity, no-silent-loss). Where an unbiased oracle exists (e.g. `BigInteger` for integer money), write a **differential property test**: random inputs, assert your result equals the oracle's. Oracles catch bugs hand-written cases miss.
- **Seed the attacker**: list the wrong-but-plausible impls you most fear ("silently wraps on overflow," "skips nulls and nets the rest," "accepts mixed currency"). Drives Phase 3.

### Phase 2 — Delegate implementation to a subagent
Unchanged from spec-tdd-coverage: case-list BEFORE impl, acceptance test GREEN, unit tests red→green, per-class branch coverage with uncovered-line justifications. The attacker is a THIRD party — not involved here.

### Phase 3 — Orchestrator verifies + dispatches the attacker
spec-tdd-coverage's checks (so SPEC-INTEGRITY holds: re-hash A2 == A4 BEFORE dispatching the attacker; the implementer must NOT edit the acceptance test, and the attacker writes a separate wrong-impl and must not edit it either; only YOU may strengthen it — always re-confirm RED→GREEN), but REPLACE the orchestrator's self gap-check with an independent attacker:
1. Run the acceptance test + property tests yourself. Must be GREEN. (Property tests must have been RED before impl — else tautologies.)
2. **DISPATCH THE ADVERSARIAL SUBAGENT** (independent context), two parts in order:
   - **Part A — test-attack:** acceptance test + INTENT only, NOT the real impl. *"Write a subtly-WRONG impl that still passes this test. Construct and run it to confirm where feasible — don't just opine. If you can, report EXACTLY which missing case let it through."*
   - **Part B — branch-hunt:** then the real impl. *"List every branch (if/loop/null-guard/early-return/catch/boundary); mark each Covered/Uncovered with its case. Report any branch with no case."*
3. **Act, then loop — bounded by an attack-loop circuit breaker (mirrors the implementer's repair cap):**
   - Every hole → strengthen the acceptance test / add cases → re-run RED→GREEN → re-attack.
   - **STOP when EITHER fires:** (i) **3 attacker rounds** run, OR (ii) **the same hole on any two rounds** — judge "same hole" objectively: the same missing acceptance-test case re-failing (the case you wrote to close it is bypassed again), NOT a rephrased wrong-impl description. Mirrors the implementer breaker's objectivity (file:line + assertion, not free text).
   - **Done clean** = the attacker cannot construct a wrong-but-green impl (the bar). **Done enough** = the breaker fires with a residual hole → STOP and surface to the human: test hardened across N rounds + property/differential tests + the attacker's final report + the **residual risk** (remaining hole(s)); the human decides accept vs. further harden. Never loop past the breaker — a correctness-critical surface always has one more boundary.
4. Surface to the user: acceptance test + property/differential tests + the attacker's final report (not the impl).

## Risk-tier
This IS the top tier: critical path gets full phases + mandatory property/differential tests + the attacker loop until unbroken OR the attack-loop circuit breaker fires (3 rounds / same hole twice) — then surface residual risk. Below critical → use `spec-tdd-coverage` or `spec-tdd`; not this skill.

## Common Mistakes
| Mistake | Fix |
|---|---|
| Orchestrator or implementer does the adversarial review itself | Independence is the entire point. It MUST be a separate agent that never saw the test or impl being written. |
| Attacker sees the real impl before test-attacking | Give ONLY test + intent for Part A; impl only for Part B. |
| Attacker opines "test looks fine" without attempting a wrong impl | Require it to construct (and run) a wrong impl, or enumerate concrete codeable wrong-impl strategies. An opinion is a rubber-stamp. |
| Property test is a tautology ("result not null") | Require a real invariant or a differential oracle. Tautologies are green lies. |
| Strengthened test not re-run RED | After any strengthening, confirm RED-then-GREEN before re-attacking. |
| Attacker loop runs past 3 rounds, or re-finds the same hole | The attack-loop circuit breaker (mirrors the implementer's) caps it: 3 rounds OR same hole twice → STOP and surface residual risk + the attacker's report to the human. Don't chase a moving target on a rich surface. |
| Used on non-critical work | Critical path only; otherwise pure token waste. |

## Red Flags — STOP
- Adversarial step done by the orchestrator or the implementer.
- Attacker returns a verdict with no attempted wrong-impl and no branch list.
- Property/differential tests absent or trivially tautological.
- A hole was found but the test was not strengthened and re-attacked.
- The attacker loop is still running past 3 rounds, or the same missing case re-failed after you closed it. (STOP — attack-loop circuit breaker; surface residual risk to the human.)
- Used on non-critical code.
