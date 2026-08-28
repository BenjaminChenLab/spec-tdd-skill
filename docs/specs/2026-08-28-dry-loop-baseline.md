# Baseline: terminal dry-loop audit — v1.8.0

**Date:** 2026-08-28 · **Status:** observed baseline (production run) + design adopted (user-directed) · **Version target:** 1.8.0

## The observed failure

A production `spec-tdd-adversarial` run (5 slices, overnight) **passed its in-run
verification** — encoding audit, attacker loop, SPEC-DEFECT sweep, all green. A
post-completion **fresh-context audit** (clean subagent, no prior attack records)
then landed, verdict *proceed-with-changes*:

- **2 × BLOCKER — deployment/ops lens.** (1) A SQL migration whose deployment
  comment promised old-version compatibility that five `SET NOT NULL` snapshot
  columns (no defaults) made false — following the documented procedure would 500
  every order in the deploy window. (2) A required runtime object whose only
  creation path was a dev-profile controller — absent in lab/sit/prod, so the
  first production transaction would roll back after the external leg had already
  executed (GC/core divergence).
- **2 × MAJOR — test-strength lens.** (3) A crash-window recovery path permanently
  dropped: an orphaned "claimed but unbooked" row made every later retry read a
  UNIQUE collision as "already booked, skip" — violating the plan's explicit
  "intermediate failure = recoverable". (4) A defensive ERROR state polled forever
  with its manual-reconciliation alert overwritten within 60 s.
- **8 × MINOR** — error handling whose deletion kept the suite green, a missing
  mixed-scenario test, an unused mock, annotation-style violations.

The auditor self-tested 3 wrong-impls; two were killed by the existing suite —
the tests were not weak across the board. The misses were **lenses and strategies
the in-run loop never looked through**.

## Why "audit until nobody finds anything" was rejected

1. **Prove-a-negative.** On a rich surface a fresh auditor can almost always find
   *something*; the bar never terminates. This is the v1.2.1 attack-loop lesson
   re-learned.
2. **Manufactured findings.** Without a severity floor, fresh auditors under
   "find something" pressure produce MINORs — the loop audits their taste, not
   the artifact.
3. **Steep diminishing returns.** Empirically round 1 finds the bulk, round 2 the
   remainder, round 3+ marginal — while each round costs a full fresh context.
4. **Briefing contamination pressure.** The longer the loop runs, the greater the
   temptation to brief the next auditor weaker so the loop can end.

## What v1.8.0 added

**Terminal dry-loop audit** (`spec-tdd-adversarial` Phase 3 step 5; PROTOCOL I8):

- **After** the attack loop closes — a passed loop is not "done".
- **Rotating lenses, one per round:** test-strength · spec/plan fidelity ·
  deployment/ops (migration windows, environment gating, runtime-object existence
  per environment, ops-doc truth) · production quality.
- **Dry-loop breaker:** next round only on a BLOCKER/MAJOR that is not a deduped
  re-find (objective anchors: same file:line / missing case / plan clause);
  STOP at **2 consecutive clean rounds or 4 total**; MINORs never extend the loop.
- Fixes needing a plan-level decision go to the human (I12), never silently.
- Residuals + every round's report surface at the end.

**Grill amendment:** deployment/rollout is now an explicit grilled dimension
(`grill-spec-tdd` Phase 1 step 1); `adversarial-grill` Part A hunts un-grilled
deployment windows.

## The design principle

**Attack wants freshness; adoption-check wants memory; termination wants
bounded dry.** One lens missing a finding is not a failure of independence —
it is the definition of why the lenses rotate.
